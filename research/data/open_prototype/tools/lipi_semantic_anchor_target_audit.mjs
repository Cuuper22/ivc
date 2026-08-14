// Pre-flight audit for semantic-anchor prediction: which catalog fields are
// even worth trying to predict from sign sequences? A field is a useful
// "anchor" only if it has enough labeled data, more than one common label, no
// single label that dominates, and no metadata proxy that would let a model
// cheat (e.g. if every 'symbol' label maps almost one-to-one onto an object
// type, predicting symbol just re-predicts type).
//
// The script reads lipi/metadata_filtered.csv, keeps numeric-clean rows,
// collapses duplicate sequences into exact families, and for each of 18
// candidate fields computes: family counts per label (labels need 30+
// families; targets need 150+ eligible families), majority share, normalized
// entropy, and the worst-case proxy concentration — for every label, the
// share captured by its most common value of each other metadata field and of
// three sign-derived features (first sign, last sign, edge frame). Each field
// then gets a status: candidate anchor, candidate-needs-proxy-blocks,
// majority-dominated, control field, or too sparse.
//
// Outputs: lipi_semantic_anchor_target_summary.csv/.json,
// _label_proxy.csv (every label-proxy pair), and _dimension_bins.csv (the
// mm-bin definitions and their populations). The follow-up probe
// (lipi_semantic_anchor_prediction_probe.mjs) consumes these decisions.

import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const sourcePath = path.join(base, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const outSummaryCsv = path.join(reportsDir, 'lipi_semantic_anchor_target_summary.csv');
const outLabelProxyCsv = path.join(reportsDir, 'lipi_semantic_anchor_label_proxy.csv');
const outDimensionCsv = path.join(reportsDir, 'lipi_semantic_anchor_dimension_bins.csv');
const outJson = path.join(reportsDir, 'lipi_semantic_anchor_target_summary.json');

const minLabelFamilies = 30;
const minTargetFamilies = 150;

const targets = [
  { name: 'symbol', role: 'iconography_anchor' },
  { name: 'cult', role: 'iconography_anchor' },
  { name: 'material', role: 'material_anchor' },
  { name: 'shape', role: 'object_form_anchor' },
  { name: 'color', role: 'object_form_anchor' },
  { name: 'boss', role: 'object_form_anchor' },
  { name: 'condition', role: 'preservation_control' },
  { name: 'type', role: 'artifact_context_anchor' },
  { name: 'site', role: 'archaeological_context_control' },
  { name: 'region', role: 'archaeological_context_control' },
  { name: 'period', role: 'chronological_context_control' },
  { name: 'phase', role: 'chronological_context_control' },
  { name: 'direction', role: 'catalog_direction_control' },
  { name: 'horizontal_bin', role: 'dimension_anchor' },
  { name: 'vertical_bin', role: 'dimension_anchor' },
  { name: 'thickness_bin', role: 'dimension_anchor' },
  { name: 'area_bin', role: 'dimension_anchor' },
  { name: 'aspect_bin', role: 'dimension_anchor' },
];

const metadataProxyFields = [
  'length',
  'type',
  'site',
  'region',
  'material',
  'shape',
  'symbol',
  'cult',
  'period',
  'phase',
  'direction',
  'horizontal_bin',
  'vertical_bin',
  'thickness_bin',
  'area_bin',
  'aspect_bin',
];

const signProxyFields = ['first_sign', 'last_sign', 'edge_frame'];

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQuotes) {
      if (c === '"') {
        if (text[i + 1] === '"') {
          field += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        field += c;
      }
    } else if (c === '"') {
      inQuotes = true;
    } else if (c === ',') {
      row.push(field);
      field = '';
    } else if (c === '\n') {
      row.push(field);
      field = '';
      if (row.length > 1 || row[0] !== '') rows.push(row);
      row = [];
    } else if (c !== '\r') {
      field += c;
    }
  }
  if (field.length || row.length) {
    row.push(field);
    rows.push(row);
  }
  return rows;
}

function toCsv(rows) {
  return `${rows
    .map((row) =>
      row
        .map((value) => {
          const text = String(value ?? '');
          return `"${text.replaceAll('"', '""')}"`;
        })
        .join(','),
    )
    .join('\n')}\n`;
}

function norm(value) {
  return String(value ?? '').trim();
}

function valueOrNull(value) {
  const text = norm(value);
  if (!text || text === '-' || text === 'None' || text === '??' || text === '?') return null;
  return text;
}

function valueOrDash(value) {
  return valueOrNull(value) ?? '-';
}

function parseTokens(text) {
  const raw = norm(text);
  return {
    raw,
    tokens: raw.match(/\d{3}/g) ?? [],
    hasUnknownZero: raw.match(/\d{3}/g)?.includes('000') ?? false,
    hasQuestion: raw.includes('?'),
    hasBracket: raw.includes('[') || raw.includes(']') || raw.includes('(') || raw.includes(')'),
    hasSlash: raw.includes('/'),
    hasText: raw !== '' && raw !== '-',
  };
}

function parseLeadingInteger(value) {
  const match = norm(value).match(/^(\d+)/);
  return match ? Number.parseInt(match[1], 10) : null;
}

function cleanDirection(value) {
  const text = norm(value).replace(/\s+/g, '').toUpperCase();
  if (text === 'R/L' || text === 'L/R' || text === 'T/B') return text;
  return text || '-';
}

function parsePositiveNumber(value) {
  const num = Number.parseFloat(norm(value));
  return Number.isFinite(num) && num > 0 ? num : null;
}

function binHorizontal(value) {
  if (value === null) return null;
  if (value <= 15) return 'h_000_015';
  if (value <= 25) return 'h_015_025';
  if (value <= 35) return 'h_025_035';
  return 'h_gt_035';
}

function binVertical(value) {
  if (value === null) return null;
  if (value <= 10) return 'v_000_010';
  if (value <= 20) return 'v_010_020';
  if (value <= 30) return 'v_020_030';
  return 'v_gt_030';
}

function binThickness(value) {
  if (value === null) return null;
  if (value <= 3) return 'th_000_003';
  if (value <= 7) return 'th_003_007';
  if (value <= 12) return 'th_007_012';
  return 'th_gt_012';
}

function binArea(horizontal, vertical) {
  if (horizontal === null || vertical === null) return null;
  const area = horizontal * vertical;
  if (area <= 200) return 'area_0000_0200';
  if (area <= 500) return 'area_0200_0500';
  if (area <= 1000) return 'area_0500_1000';
  return 'area_gt_1000';
}

function binAspect(horizontal, vertical) {
  if (horizontal === null || vertical === null || vertical === 0) return null;
  const aspect = horizontal / vertical;
  if (aspect <= 0.8) return 'aspect_tall';
  if (aspect <= 1.25) return 'aspect_squareish';
  if (aspect <= 2) return 'aspect_wide';
  return 'aspect_very_wide';
}

function bump(map, key, by = 1) {
  map.set(key, (map.get(key) ?? 0) + by);
}

function majorityFromValues(values) {
  const counts = new Map();
  for (const value of values) {
    if (value !== null && value !== undefined) bump(counts, value);
  }
  if (!counts.size) return null;
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))[0][0];
}

function entropy(counts) {
  const total = [...counts.values()].reduce((sum, value) => sum + value, 0);
  if (!total) return 0;
  let h = 0;
  for (const count of counts.values()) {
    const p = count / total;
    h -= p * Math.log2(p);
  }
  return h;
}

function formatNumber(value) {
  return value === null || value === undefined || Number.isNaN(value) ? '' : Number(value.toFixed(6));
}

function exactFamilies(records) {
  const seen = new Map();
  for (const record of records) {
    const key = record.tokens.join(' ');
    if (!seen.has(key)) {
      seen.set(key, {
        ...record,
        duplicate_weight: 0,
        source_records: [],
      });
    }
    const family = seen.get(key);
    family.duplicate_weight++;
    family.source_records.push(record);
  }
  return [...seen.values()].sort((a, b) => a.id.localeCompare(b.id));
}

function familyTargetLabel(family, targetName) {
  return majorityFromValues(family.source_records.map((record) => record[targetName]));
}

function familyProxyValue(family, proxyName) {
  if (proxyName === 'length') return String(family.tokens.length);
  if (proxyName === 'first_sign') return family.tokens[0] ?? null;
  if (proxyName === 'last_sign') return family.tokens.at(-1) ?? null;
  if (proxyName === 'edge_frame') {
    if (!family.tokens.length) return null;
    return `${family.tokens[0]}...${family.tokens.at(-1)}`;
  }
  return majorityFromValues(family.source_records.map((record) => record[proxyName]));
}

function topProxyForLabel(families, targetName, label, proxyName) {
  const counts = new Map();
  let total = 0;
  for (const family of families) {
    if (familyTargetLabel(family, targetName) !== label) continue;
    const proxyValue = familyProxyValue(family, proxyName);
    if (proxyValue === null || proxyValue === undefined || proxyValue === '-') continue;
    bump(counts, proxyValue);
    total++;
  }
  if (!counts.size) return null;
  const [topValue, topCount] = [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))[0];
  return {
    topValue,
    topCount,
    total,
    share: topCount / total,
  };
}

function targetStatus({ role, eligibleLabelCount, eligibleFamilies, majorityShare, worstMetadataProxyShare }) {
  if (eligibleLabelCount < 2) return 'not_eligible_too_few_labels';
  if (eligibleFamilies < minTargetFamilies) return 'not_eligible_too_sparse';
  if (role.endsWith('_control')) return 'control_field_not_semantic_anchor';
  if (majorityShare >= 0.85) return 'majority_dominated';
  if (worstMetadataProxyShare >= 0.9) return 'candidate_requires_proxy_block_controls';
  return 'candidate_anchor_for_next_prediction';
}

const rows = parseCsv(fs.readFileSync(sourcePath, 'utf8'));
const header = rows[0];
const column = Object.fromEntries(header.map((name, index) => [name, index]));

const records = rows.slice(1).map((row) => {
  const parsed = parseTokens(row[column.text]);
  const lengthNumeric = parseLeadingInteger(row[column['text length']]);
  const cisi = valueOrNull(row[column.cisi]);
  const complete = valueOrDash(row[column.complete]);
  const direction = cleanDirection(row[column['dir.']]);
  const horizontal = parsePositiveNumber(row[column['horizontal(mm)']]);
  const vertical = parsePositiveNumber(row[column['vertical(mm)']]);
  const thickness = parsePositiveNumber(row[column['thickness(mm)']]);
  const numericClean =
    cisi !== null &&
    parsed.hasText &&
    parsed.tokens.length > 0 &&
    complete === 'Y' &&
    (direction === 'R/L' || direction === 'L/R') &&
    lengthNumeric === parsed.tokens.length &&
    !parsed.hasUnknownZero &&
    !parsed.hasQuestion &&
    !parsed.hasBracket &&
    !parsed.hasSlash;
  return {
    id: valueOrDash(row[column.id]),
    cisi: cisi ?? '-',
    tokens: parsed.tokens,
    length: parsed.tokens.length,
    numeric_clean: numericClean,
    region: valueOrNull(row[column.region]),
    site: valueOrNull(row[column.site]),
    material: valueOrNull(row[column.material]),
    color: valueOrNull(row[column.color]),
    shape: valueOrNull(row[column.shape]),
    preservation: valueOrNull(row[column.preservation]),
    symbol: valueOrNull(row[column.symbol]),
    cult: valueOrNull(row[column.cult]),
    type: valueOrNull(row[column.type]),
    condition: valueOrNull(row[column.condition]),
    complete: valueOrNull(row[column.complete]),
    direction,
    period: valueOrNull(row[column.period]),
    phase: valueOrNull(row[column.phase]),
    boss: valueOrNull(row[column.boss]),
    horizontal_mm: horizontal,
    vertical_mm: vertical,
    thickness_mm: thickness,
    horizontal_bin: binHorizontal(horizontal),
    vertical_bin: binVertical(vertical),
    thickness_bin: binThickness(thickness),
    area_bin: binArea(horizontal, vertical),
    aspect_bin: binAspect(horizontal, vertical),
  };
});

const cleanRecords = records.filter((record) => record.numeric_clean);
const families = exactFamilies(cleanRecords);

const dimensionRows = [
  [
    'metric',
    'nonzero_clean_source_rows',
    'nonzero_exact_sequence_families',
    'bin',
    'source_rows',
    'families',
    'definition',
  ],
];

const dimensionDefinitions = {
  horizontal_bin: {
    h_000_015: '0 < horizontal(mm) <= 15',
    h_015_025: '15 < horizontal(mm) <= 25',
    h_025_035: '25 < horizontal(mm) <= 35',
    h_gt_035: 'horizontal(mm) > 35',
  },
  vertical_bin: {
    v_000_010: '0 < vertical(mm) <= 10',
    v_010_020: '10 < vertical(mm) <= 20',
    v_020_030: '20 < vertical(mm) <= 30',
    v_gt_030: 'vertical(mm) > 30',
  },
  thickness_bin: {
    th_000_003: '0 < thickness(mm) <= 3',
    th_003_007: '3 < thickness(mm) <= 7',
    th_007_012: '7 < thickness(mm) <= 12',
    th_gt_012: 'thickness(mm) > 12',
  },
  area_bin: {
    area_0000_0200: '0 < horizontal(mm) * vertical(mm) <= 200',
    area_0200_0500: '200 < horizontal(mm) * vertical(mm) <= 500',
    area_0500_1000: '500 < horizontal(mm) * vertical(mm) <= 1000',
    area_gt_1000: 'horizontal(mm) * vertical(mm) > 1000',
  },
  aspect_bin: {
    aspect_tall: 'horizontal(mm) / vertical(mm) <= 0.8',
    aspect_squareish: '0.8 < horizontal(mm) / vertical(mm) <= 1.25',
    aspect_wide: '1.25 < horizontal(mm) / vertical(mm) <= 2',
    aspect_very_wide: 'horizontal(mm) / vertical(mm) > 2',
  },
};

for (const metric of Object.keys(dimensionDefinitions)) {
  const sourceCounts = new Map();
  const familyCounts = new Map();
  for (const record of cleanRecords) {
    if (record[metric] !== null) bump(sourceCounts, record[metric]);
  }
  for (const family of families) {
    const value = familyTargetLabel(family, metric);
    if (value !== null) bump(familyCounts, value);
  }
  const sourceTotal = [...sourceCounts.values()].reduce((sum, count) => sum + count, 0);
  const familyTotal = [...familyCounts.values()].reduce((sum, count) => sum + count, 0);
  for (const [bin, definition] of Object.entries(dimensionDefinitions[metric])) {
    dimensionRows.push([
      metric,
      sourceTotal,
      familyTotal,
      bin,
      sourceCounts.get(bin) ?? 0,
      familyCounts.get(bin) ?? 0,
      definition,
    ]);
  }
}

const summaryRows = [
  [
    'target',
    'role',
    'source_clean_rows_with_label',
    'exact_sequence_families_with_label',
    'eligible_families',
    'eligible_labels',
    'majority_label',
    'majority_share',
    'normalized_entropy',
    'worst_metadata_proxy_field',
    'worst_metadata_proxy_label',
    'worst_metadata_proxy_value',
    'worst_metadata_proxy_share',
    'worst_sign_proxy_field',
    'worst_sign_proxy_label',
    'worst_sign_proxy_value',
    'worst_sign_proxy_share',
    'status',
  ],
];
const labelProxyRows = [
  [
    'target',
    'role',
    'label',
    'label_families',
    'proxy_kind',
    'proxy_field',
    'top_proxy_value',
    'top_proxy_count',
    'proxy_total_for_label',
    'top_proxy_share',
  ],
];

const summary = [];

for (const target of targets) {
  const sourceRowsWithLabel = cleanRecords.filter((record) => record[target.name] !== null).length;
  const labelCounts = new Map();
  for (const family of families) {
    const label = familyTargetLabel(family, target.name);
    if (label !== null) bump(labelCounts, label);
  }
  const familyRowsWithLabel = [...labelCounts.values()].reduce((sum, count) => sum + count, 0);
  const eligibleLabels = [...labelCounts.entries()]
    .filter(([, count]) => count >= minLabelFamilies)
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  const eligibleCounts = new Map(eligibleLabels);
  const eligibleFamilies = [...eligibleCounts.values()].reduce((sum, count) => sum + count, 0);
  const [majorityLabel, majorityCount] = eligibleLabels[0] ?? ['', 0];
  const majorityShare = eligibleFamilies ? majorityCount / eligibleFamilies : null;
  const normalizedEntropy =
    eligibleLabels.length > 1 ? entropy(eligibleCounts) / Math.log2(eligibleLabels.length) : 0;

  let worstMetadata = null;
  let worstSign = null;
  for (const [label, labelFamilies] of eligibleLabels) {
    for (const proxyName of metadataProxyFields) {
      if (proxyName === target.name) continue;
      const proxy = topProxyForLabel(families, target.name, label, proxyName);
      if (!proxy) continue;
      const row = {
        target: target.name,
        role: target.role,
        label,
        labelFamilies,
        proxyKind: 'metadata',
        proxyName,
        ...proxy,
      };
      if (!worstMetadata || row.share > worstMetadata.share) worstMetadata = row;
      labelProxyRows.push([
        row.target,
        row.role,
        row.label,
        row.labelFamilies,
        row.proxyKind,
        row.proxyName,
        row.topValue,
        row.topCount,
        row.total,
        formatNumber(row.share),
      ]);
    }
    for (const proxyName of signProxyFields) {
      const proxy = topProxyForLabel(families, target.name, label, proxyName);
      if (!proxy) continue;
      const row = {
        target: target.name,
        role: target.role,
        label,
        labelFamilies,
        proxyKind: 'sign',
        proxyName,
        ...proxy,
      };
      if (!worstSign || row.share > worstSign.share) worstSign = row;
      labelProxyRows.push([
        row.target,
        row.role,
        row.label,
        row.labelFamilies,
        row.proxyKind,
        row.proxyName,
        row.topValue,
        row.topCount,
        row.total,
        formatNumber(row.share),
      ]);
    }
  }

  const status = targetStatus({
    role: target.role,
    eligibleLabelCount: eligibleLabels.length,
    eligibleFamilies,
    majorityShare: majorityShare ?? 1,
    worstMetadataProxyShare: worstMetadata?.share ?? 0,
  });

  const row = {
    target: target.name,
    role: target.role,
    source_clean_rows_with_label: sourceRowsWithLabel,
    exact_sequence_families_with_label: familyRowsWithLabel,
    eligible_families: eligibleFamilies,
    eligible_labels: eligibleLabels.length,
    majority_label: majorityLabel,
    majority_share: formatNumber(majorityShare),
    normalized_entropy: formatNumber(normalizedEntropy),
    worst_metadata_proxy_field: worstMetadata?.proxyName ?? '',
    worst_metadata_proxy_label: worstMetadata?.label ?? '',
    worst_metadata_proxy_value: worstMetadata?.topValue ?? '',
    worst_metadata_proxy_share: formatNumber(worstMetadata?.share),
    worst_sign_proxy_field: worstSign?.proxyName ?? '',
    worst_sign_proxy_label: worstSign?.label ?? '',
    worst_sign_proxy_value: worstSign?.topValue ?? '',
    worst_sign_proxy_share: formatNumber(worstSign?.share),
    status,
  };

  summary.push(row);
  summaryRows.push([
    row.target,
    row.role,
    row.source_clean_rows_with_label,
    row.exact_sequence_families_with_label,
    row.eligible_families,
    row.eligible_labels,
    row.majority_label,
    row.majority_share,
    row.normalized_entropy,
    row.worst_metadata_proxy_field,
    row.worst_metadata_proxy_label,
    row.worst_metadata_proxy_value,
    row.worst_metadata_proxy_share,
    row.worst_sign_proxy_field,
    row.worst_sign_proxy_label,
    row.worst_sign_proxy_value,
    row.worst_sign_proxy_share,
    row.status,
  ]);
}

fs.mkdirSync(reportsDir, { recursive: true });
fs.writeFileSync(outSummaryCsv, toCsv(summaryRows));
fs.writeFileSync(outLabelProxyCsv, toCsv(labelProxyRows));
fs.writeFileSync(outDimensionCsv, toCsv(dimensionRows));
fs.writeFileSync(
  outJson,
  `${JSON.stringify(
    {
      source: 'filtered lipi metadata, claim columns removed',
      source_rows: records.length,
      numeric_clean_source_rows: cleanRecords.length,
      exact_sequence_families: families.length,
      min_label_families: minLabelFamilies,
      min_target_families: minTargetFamilies,
      targets: summary,
      outputs: [
        path.relative(base, outSummaryCsv).replaceAll('\\', '/'),
        path.relative(base, outLabelProxyCsv).replaceAll('\\', '/'),
        path.relative(base, outDimensionCsv).replaceAll('\\', '/'),
      ],
      interpretation_boundary:
        'Semantic-anchor target audit only; labels are catalog metadata from a T3 planning source and do not create sign meanings, phonetic values, language identity, or translations.',
    },
    null,
    2,
  )}\n`,
);

console.log(
  JSON.stringify(
    {
      source_rows: records.length,
      numeric_clean_source_rows: cleanRecords.length,
      exact_sequence_families: families.length,
      min_label_families: minLabelFamilies,
      candidate_targets: summary
        .filter(
          (row) =>
            row.status === 'candidate_anchor_for_next_prediction' ||
            row.status === 'candidate_requires_proxy_block_controls',
        )
        .map((row) => row.target),
      control_targets: summary
        .filter((row) => row.status === 'control_field_not_semantic_anchor')
        .map((row) => row.target),
      wrote: [
        path.relative(base, outSummaryCsv).replaceAll('\\', '/'),
        path.relative(base, outLabelProxyCsv).replaceAll('\\', '/'),
        path.relative(base, outDimensionCsv).replaceAll('\\', '/'),
        path.relative(base, outJson).replaceAll('\\', '/'),
      ],
    },
    null,
    2,
  ),
);
