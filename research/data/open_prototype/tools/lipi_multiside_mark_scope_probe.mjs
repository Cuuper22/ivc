// First-pass census of "short side marks": objects with two or more inscribed
// sides where one side carries only one or two signs. The working question is
// whether these short marks are a distinct functional layer (labels, tallies,
// batch marks) rather than ordinary text, so this probe maps where they occur
// and which signs they favor.
//
// The script reads lipi/metadata_filtered.csv, parses each side row's sign
// tokens (three-digit codes), grades each row as clean / usable-uncertain /
// audit-only, and groups rows by CISI object id. Within multi-side objects it
// splits clean rows into short-mark candidates (1-2 signs) and long-text
// candidates (3+ signs), then computes, for each sign seen at least 5 times in
// short marks, a smoothed enrichment ratio: how much more often the sign
// appears in short marks than in longer text. It also tabulates each enriched
// sign's typical object types, sites, side indexes, and binned dimensions, and
// counts short-sign/long-sign co-occurrence pairs on the same object.
//
// Outputs: lipi_multiside_mark_rows.csv (per-side detail), _token_counts.csv
// (enrichment table), _pair_counts.csv, _type_summary.csv, and _summary.json.
// The probe only scopes the phenomenon; it assigns no values or meanings.

import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const sourcePath = path.join(base, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const outRows = path.join(reportsDir, 'lipi_multiside_mark_rows.csv');
const outTokenCounts = path.join(reportsDir, 'lipi_multiside_mark_token_counts.csv');
const outPairCounts = path.join(reportsDir, 'lipi_multiside_mark_pair_counts.csv');
const outTypeSummary = path.join(reportsDir, 'lipi_multiside_mark_type_summary.csv');
const outJson = path.join(reportsDir, 'lipi_multiside_mark_summary.json');

const minShortTokenCount = 5;

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
  const tokens = raw.match(/\d{3}/g) ?? [];
  return {
    raw,
    tokens,
    tokenCount: tokens.length,
    hasUnknownZero: tokens.includes('000'),
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

function parseSideIndex(id) {
  const match = norm(id).match(/\.(\d+)$/);
  return match ? Number.parseInt(match[1], 10) : null;
}

function parseInteger(value) {
  const num = Number.parseInt(norm(value), 10);
  return Number.isFinite(num) ? num : null;
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

function bump(map, key, by = 1) {
  map.set(key, (map.get(key) ?? 0) + by);
}

function addNested(map, keyA, keyB, by = 1) {
  if (!map.has(keyA)) map.set(keyA, new Map());
  bump(map.get(keyA), keyB, by);
}

function formatNumber(value) {
  return value === null || value === undefined || Number.isNaN(value) ? null : Number(value.toFixed(6));
}

function joinTop(counts, limit = 5) {
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, limit)
    .map(([key, count]) => `${key}:${count}`)
    .join(';');
}

function rowStatus(record) {
  const directional = record.direction === 'R/L' || record.direction === 'L/R' || record.direction === 'T/B';
  const lengthMatches =
    record.length_numeric !== null && record.parsed.tokenCount > 0 && record.length_numeric === record.parsed.tokenCount;
  const clean =
    record.parsed.hasText &&
    record.parsed.tokenCount > 0 &&
    record.complete === 'Y' &&
    directional &&
    lengthMatches &&
    !record.parsed.hasUnknownZero &&
    !record.parsed.hasQuestion &&
    !record.parsed.hasBracket &&
    !record.parsed.hasSlash;
  if (clean) return 'clean_side_row';
  if (record.parsed.tokenCount > 0 && !record.parsed.hasQuestion && !record.parsed.hasBracket && !record.parsed.hasSlash) {
    return 'usable_uncertain_side_row';
  }
  return 'audit_only_side_row';
}

const rows = parseCsv(fs.readFileSync(sourcePath, 'utf8'));
const header = rows[0];
const column = Object.fromEntries(header.map((name, index) => [name, index]));

const records = rows.slice(1).map((row) => {
  const parsed = parseTokens(row[column.text]);
  const horizontal = parsePositiveNumber(row[column['horizontal(mm)']]);
  const vertical = parsePositiveNumber(row[column['vertical(mm)']]);
  const thickness = parsePositiveNumber(row[column['thickness(mm)']]);
  const record = {
    id: valueOrDash(row[column.id]),
    cisi: valueOrNull(row[column.cisi]),
    side_index: parseSideIndex(row[column.id]),
    sides: parseInteger(row[column.sides]),
    region: valueOrNull(row[column.region]),
    site: valueOrNull(row[column.site]),
    type: valueOrNull(row[column.type]),
    material: valueOrNull(row[column.material]),
    shape: valueOrNull(row[column.shape]),
    complete: valueOrDash(row[column.complete]),
    direction: cleanDirection(row[column['dir.']]),
    length_raw: valueOrDash(row[column['text length']]),
    length_numeric: parseLeadingInteger(row[column['text length']]),
    signs_raw: valueOrDash(row[column.signs]),
    parsed,
    text: valueOrDash(row[column.text]),
    horizontal_bin: binHorizontal(horizontal),
    vertical_bin: binVertical(vertical),
    thickness_bin: binThickness(thickness),
  };
  record.status = rowStatus(record);
  record.short_mark_candidate =
    record.status === 'clean_side_row' &&
    record.sides !== null &&
    record.sides >= 2 &&
    record.parsed.tokenCount > 0 &&
    record.parsed.tokenCount <= 2;
  record.long_text_candidate =
    record.status === 'clean_side_row' &&
    record.sides !== null &&
    record.sides >= 2 &&
    record.parsed.tokenCount >= 3;
  return record;
});

const rowsWithCisi = records.filter((record) => record.cisi);
const groups = new Map();
for (const record of rowsWithCisi) {
  if (!groups.has(record.cisi)) groups.set(record.cisi, []);
  groups.get(record.cisi).push(record);
}

const multiGroups = [...groups.entries()].filter(([, group]) => group.length > 1 || group.some((record) => (record.sides ?? 1) > 1));
const multiRecords = multiGroups.flatMap(([, group]) => group);
const shortRows = multiRecords.filter((record) => record.short_mark_candidate);
const longRows = multiRecords.filter((record) => record.long_text_candidate);

const rowTable = [
  [
    'id',
    'cisi',
    'side_index',
    'sides',
    'site',
    'type',
    'material',
    'shape',
    'complete',
    'direction',
    'token_count',
    'status',
    'short_mark_candidate',
    'long_text_candidate',
    'horizontal_bin',
    'vertical_bin',
    'thickness_bin',
    'text',
  ],
  ...multiRecords
    .sort((a, b) => a.cisi.localeCompare(b.cisi) || (a.side_index ?? 0) - (b.side_index ?? 0) || a.id.localeCompare(b.id))
    .map((record) => [
      record.id,
      record.cisi,
      record.side_index ?? '',
      record.sides ?? '',
      record.site ?? '-',
      record.type ?? '-',
      record.material ?? '-',
      record.shape ?? '-',
      record.complete,
      record.direction,
      record.parsed.tokenCount,
      record.status,
      record.short_mark_candidate,
      record.long_text_candidate,
      record.horizontal_bin ?? '-',
      record.vertical_bin ?? '-',
      record.thickness_bin ?? '-',
      record.text,
    ]),
];

const shortTokenCounts = new Map();
const longTokenCounts = new Map();
const shortTokenTypes = new Map();
const shortTokenSites = new Map();
const shortTokenSideIndex = new Map();
const shortTokenHorizontalBins = new Map();
const shortTokenVerticalBins = new Map();
const shortTokenThicknessBins = new Map();

for (const record of shortRows) {
  for (const token of record.parsed.tokens) {
    bump(shortTokenCounts, token);
    addNested(shortTokenTypes, token, record.type ?? '-');
    addNested(shortTokenSites, token, record.site ?? '-');
    addNested(shortTokenSideIndex, token, String(record.side_index ?? '-'));
    addNested(shortTokenHorizontalBins, token, record.horizontal_bin ?? '-');
    addNested(shortTokenVerticalBins, token, record.vertical_bin ?? '-');
    addNested(shortTokenThicknessBins, token, record.thickness_bin ?? '-');
  }
}

for (const record of multiRecords.filter((record) => !record.short_mark_candidate && record.status !== 'audit_only_side_row')) {
  for (const token of record.parsed.tokens) bump(longTokenCounts, token);
}

const shortTotal = [...shortTokenCounts.values()].reduce((sum, count) => sum + count, 0);
const longTotal = [...longTokenCounts.values()].reduce((sum, count) => sum + count, 0);
const vocabulary = new Set([...shortTokenCounts.keys(), ...longTokenCounts.keys()]);

const tokenRows = [
  [
    'token',
    'short_mark_token_count',
    'non_short_token_count',
    'short_mark_share',
    'non_short_share',
    'enrichment_ratio_smoothed',
    'top_types',
    'top_sites',
    'top_side_indexes',
    'top_horizontal_bins',
    'top_vertical_bins',
    'top_thickness_bins',
  ],
];

const tokenObjects = [];
for (const token of vocabulary) {
  const shortCount = shortTokenCounts.get(token) ?? 0;
  const longCount = longTokenCounts.get(token) ?? 0;
  if (shortCount < minShortTokenCount) continue;
  const shortShare = shortCount / Math.max(1, shortTotal);
  const longShare = longCount / Math.max(1, longTotal);
  const enrichment = ((shortCount + 0.5) / (shortTotal + vocabulary.size * 0.5)) /
    ((longCount + 0.5) / (longTotal + vocabulary.size * 0.5));
  tokenObjects.push({
    token,
    shortCount,
    longCount,
    shortShare,
    longShare,
    enrichment,
  });
}

for (const row of tokenObjects.sort((a, b) => b.enrichment - a.enrichment || b.shortCount - a.shortCount || a.token.localeCompare(b.token))) {
  tokenRows.push([
    row.token,
    row.shortCount,
    row.longCount,
    formatNumber(row.shortShare),
    formatNumber(row.longShare),
    formatNumber(row.enrichment),
    joinTop(shortTokenTypes.get(row.token) ?? new Map()),
    joinTop(shortTokenSites.get(row.token) ?? new Map()),
    joinTop(shortTokenSideIndex.get(row.token) ?? new Map()),
    joinTop(shortTokenHorizontalBins.get(row.token) ?? new Map()),
    joinTop(shortTokenVerticalBins.get(row.token) ?? new Map()),
    joinTop(shortTokenThicknessBins.get(row.token) ?? new Map()),
  ]);
}

const pairCounts = new Map();
for (const [, group] of multiGroups) {
  const groupShort = group.filter((record) => record.short_mark_candidate);
  const groupLong = group.filter((record) => record.long_text_candidate);
  if (!groupShort.length || !groupLong.length) continue;
  const shortTokens = new Set(groupShort.flatMap((record) => record.parsed.tokens));
  const longTokens = new Set(groupLong.flatMap((record) => record.parsed.tokens));
  for (const shortToken of shortTokens) {
    for (const longToken of longTokens) {
      const key = `${shortToken}\t${longToken}`;
      bump(pairCounts, key);
    }
  }
}

const pairRows = [
  ['short_mark_token', 'long_text_token', 'artifact_group_count'],
  ...[...pairCounts.entries()]
    .map(([key, count]) => [...key.split('\t'), count])
    .filter((row) => row[2] >= 3)
    .sort((a, b) => b[2] - a[2] || a[0].localeCompare(b[0]) || a[1].localeCompare(b[1])),
];

const typeRows = [['type', 'multi_side_rows', 'short_mark_rows', 'long_text_rows', 'multi_side_artifacts']];
const typeMap = new Map();
for (const [, group] of multiGroups) {
  const types = new Set(group.map((record) => record.type ?? '-'));
  for (const type of types) {
    if (!typeMap.has(type)) {
      typeMap.set(type, {
        rows: 0,
        shortRows: 0,
        longRows: 0,
        artifacts: 0,
      });
    }
    const bucket = typeMap.get(type);
    bucket.artifacts++;
    bucket.rows += group.filter((record) => (record.type ?? '-') === type).length;
    bucket.shortRows += group.filter((record) => (record.type ?? '-') === type && record.short_mark_candidate).length;
    bucket.longRows += group.filter((record) => (record.type ?? '-') === type && record.long_text_candidate).length;
  }
}

for (const [type, counts] of [...typeMap.entries()].sort((a, b) => b[1].shortRows - a[1].shortRows || b[1].rows - a[1].rows || a[0].localeCompare(b[0]))) {
  typeRows.push([type, counts.rows, counts.shortRows, counts.longRows, counts.artifacts]);
}

const summary = {
  source: 'filtered lipi metadata, claim columns removed',
  source_rows: records.length,
  rows_with_cisi: rowsWithCisi.length,
  cisi_groups: groups.size,
  multiside_or_multirow_cisi_groups: multiGroups.length,
  multiside_rows: multiRecords.length,
  clean_multiside_rows: multiRecords.filter((record) => record.status === 'clean_side_row').length,
  short_mark_candidate_rows: shortRows.length,
  long_text_candidate_rows: longRows.length,
  short_mark_token_total: shortTotal,
  non_short_token_total: longTotal,
  enriched_short_mark_tokens: tokenObjects.length,
  top_short_mark_tokens: tokenObjects
    .sort((a, b) => b.shortCount - a.shortCount || b.enrichment - a.enrichment || a.token.localeCompare(b.token))
    .slice(0, 12)
    .map((row) => ({
      token: row.token,
      short_mark_token_count: row.shortCount,
      non_short_token_count: row.longCount,
      enrichment_ratio_smoothed: formatNumber(row.enrichment),
    })),
  highest_enrichment_tokens: tokenObjects
    .sort((a, b) => b.enrichment - a.enrichment || b.shortCount - a.shortCount || a.token.localeCompare(b.token))
    .slice(0, 12)
    .map((row) => ({
      token: row.token,
      short_mark_token_count: row.shortCount,
      non_short_token_count: row.longCount,
      enrichment_ratio_smoothed: formatNumber(row.enrichment),
    })),
  outputs: [
    path.relative(base, outRows).replaceAll('\\', '/'),
    path.relative(base, outTokenCounts).replaceAll('\\', '/'),
    path.relative(base, outPairCounts).replaceAll('\\', '/'),
    path.relative(base, outTypeSummary).replaceAll('\\', '/'),
  ],
  interpretation_boundary:
    'Multi-side mark scope and enrichment queue only; short side marks are not numerical values, metrological readings, sign meanings, phonetic values, language identity, or translations.',
};

fs.mkdirSync(reportsDir, { recursive: true });
fs.writeFileSync(outRows, toCsv(rowTable));
fs.writeFileSync(outTokenCounts, toCsv(tokenRows));
fs.writeFileSync(outPairCounts, toCsv(pairRows));
fs.writeFileSync(outTypeSummary, toCsv(typeRows));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
