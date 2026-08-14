import fs from 'node:fs';
import path from 'node:path';

// The frame700 pattern is a two-sign inscription pairing sign 700 with one of three "stroke
// mark" subtypes: 032, 033, or 034. This script asks whether anything else about the object
// predicts which subtype it carries -- because if subtype is predictable from context, the
// three marks are doing systematic work, not varying freely. It reads the companion-context
// rows and the validation queue (for physical dimensions), keeps only exact two-token
// 700+subtype rows, and derives features: object type/site/sides, five size bins, side
// context (which side is short, order, side relation), and the companion long side's text
// family. It then runs leave-one-out naive Bayes (alpha 0.5) for eight feature sets, under
// two scopes (all rows, and excluding the H-2218..H-2239 series) and two leaveout modes
// (drop the artifact, or drop its whole sequence family). It also computes per-feature-value
// lift by subtype. Outputs: the assembled feature rows CSV (used by many later scripts),
// per-row predictions, an accuracy summary, feature contrasts, and a JSON summary. Context
// evidence only -- no meaning, value, or reading is claimed.

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const validationPath = path.join(reportsDir, 'lipi_multiside_mark_validation_queue.csv');
const companionPath = path.join(reportsDir, 'lipi_short_mark_companion_context_rows.csv');

const rowsPath = path.join(reportsDir, 'lipi_frame700_subtype_rows.csv');
const predictionsPath = path.join(reportsDir, 'lipi_frame700_subtype_predictions.csv');
const predictionSummaryPath = path.join(reportsDir, 'lipi_frame700_subtype_prediction_summary.csv');
const featureContrastsPath = path.join(reportsDir, 'lipi_frame700_subtype_feature_contrasts.csv');
const summaryPath = path.join(reportsDir, 'lipi_frame700_subtype_summary.json');

const hSeries = new Set(Array.from({ length: 22 }, (_, index) => `H-${2218 + index}`));
const targetSubtypes = ['032', '033', '034'];
const alpha = 0.5;

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

function readCsvRecords(filePath) {
  const rows = parseCsv(fs.readFileSync(filePath, 'utf8'));
  const header = rows[0];
  return rows.slice(1).map((row) => Object.fromEntries(header.map((name, index) => [name, row[index] ?? ''])));
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

function tokens(text) {
  return norm(text).match(/\d{3}/g) ?? [];
}

function parsePositiveNumber(value) {
  const text = norm(value);
  if (!/^(?:\d+(?:\.\d+)?|\.\d+)$/.test(text)) return null;
  const number = Number(text);
  return Number.isFinite(number) && number > 0 ? number : null;
}

function isExactFrame700Subtype(row) {
  const parsed = tokens(row.short_text);
  return parsed.length === 2 && parsed.includes('700') && targetSubtypes.includes(row.companion) && parsed.includes(row.companion);
}

function formatNumber(value, digits = 6) {
  return value === null || value === undefined || Number.isNaN(value) ? '' : Number(value.toFixed(digits));
}

function add(map, key, by = 1) {
  map.set(key, (map.get(key) ?? 0) + by);
}

function countBy(rows, keyFn) {
  const counts = new Map();
  for (const row of rows) add(counts, keyFn(row));
  return Object.fromEntries([...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])));
}

function firstOrMissing(values) {
  const clean = values.filter(Boolean);
  return clean.length ? clean.join(';') : 'MISSING';
}

function binHorizontal(value) {
  if (value === null) return 'h_missing';
  if (value < 10) return 'h_lt_10';
  if (value < 13) return 'h_10_13';
  if (value < 16) return 'h_13_16';
  return 'h_ge_16';
}

function binVertical(value) {
  if (value === null) return 'v_missing';
  if (value < 7) return 'v_lt_7';
  if (value < 8.5) return 'v_7_8p5';
  if (value < 10) return 'v_8p5_10';
  return 'v_ge_10';
}

function binThickness(value) {
  if (value === null) return 'th_missing';
  if (value < 3) return 'th_lt_3';
  if (value < 5) return 'th_3_5';
  return 'th_ge_5';
}

function binArea(horizontal, vertical) {
  if (horizontal === null || vertical === null) return 'area_missing';
  const area = horizontal * vertical;
  if (area < 80) return 'area_lt_80';
  if (area < 120) return 'area_80_120';
  if (area < 180) return 'area_120_180';
  return 'area_ge_180';
}

function binAspect(horizontal, vertical) {
  if (horizontal === null || vertical === null) return 'aspect_missing';
  const aspect = horizontal / vertical;
  if (aspect < 1.5) return 'aspect_lt_1p5';
  if (aspect < 1.9) return 'aspect_1p5_1p9';
  return 'aspect_ge_1p9';
}

function parseLongSides(text) {
  return norm(text)
    .split('|')
    .map((part) => {
      const match = part.match(/^([^:]+):(.+)$/);
      const side = match ? match[1] : '';
      const sideText = match ? match[2] : part;
      return { side, text: sideText, tokens: tokens(sideText) };
    })
    .filter((row) => row.tokens.length);
}

function longFeatures(longSides) {
  if (!longSides.length) {
    return {
      long_family: 'NO_LONGER_TEXT',
      long_token_set: 'NO_LONGER_TEXT',
      long_edge_frames: 'NO_LONGER_TEXT',
      long_first_tokens: 'NO_LONGER_TEXT',
      long_last_tokens: 'NO_LONGER_TEXT',
      long_length_bin: 'long_len_0',
      long_has_176: 'has176_false',
      long_has_400: 'has400_false',
      long_has_520: 'has520_false',
      long_has_690: 'has690_false',
      long_has_740: 'has740_false',
      long_has_861: 'has861_false',
    };
  }
  const allTokens = longSides.flatMap((side) => side.tokens);
  const tokenSet = [...new Set(allTokens)].sort((a, b) => a.localeCompare(b));
  const maxLen = Math.max(...longSides.map((side) => side.tokens.length));
  const edgeFrames = longSides.map((side) => `${side.tokens[0]}...${side.tokens.at(-1)}`).sort((a, b) => a.localeCompare(b));
  const firstTokens = [...new Set(longSides.map((side) => side.tokens[0]))].sort((a, b) => a.localeCompare(b));
  const lastTokens = [...new Set(longSides.map((side) => side.tokens.at(-1)))].sort((a, b) => a.localeCompare(b));
  const has = (token) => tokenSet.includes(token);
  return {
    long_family: longSides.map((side) => side.text).sort((a, b) => a.localeCompare(b)).join('|'),
    long_token_set: tokenSet.join(';'),
    long_edge_frames: edgeFrames.join(';'),
    long_first_tokens: firstTokens.join(';'),
    long_last_tokens: lastTokens.join(';'),
    long_length_bin: maxLen <= 3 ? 'long_len_1_3' : maxLen <= 5 ? 'long_len_4_5' : 'long_len_6_plus',
    long_has_176: `has176_${has('176')}`,
    long_has_400: `has400_${has('400')}`,
    long_has_520: `has520_${has('520')}`,
    long_has_690: `has690_${has('690')}`,
    long_has_740: `has740_${has('740')}`,
    long_has_861: `has861_${has('861')}`,
  };
}

function featureValue(row, feature) {
  return `${feature}=${row[feature] ?? 'MISSING'}`;
}

function buildModel(trainRows, features) {
  const labelCounts = new Map();
  const featureValueSpaces = new Map();
  const featureCounts = new Map();
  for (const row of trainRows) {
    add(labelCounts, row.subtype);
    for (const feature of features) {
      const value = featureValue(row, feature);
      if (!featureValueSpaces.has(feature)) featureValueSpaces.set(feature, new Set());
      featureValueSpaces.get(feature).add(value);
      add(featureCounts, `${row.subtype}\t${feature}\t${value}`);
    }
  }
  return (candidate, row) => {
    const labelCount = labelCounts.get(candidate) ?? 0;
    let score = Math.log((labelCount + alpha) / (trainRows.length + alpha * targetSubtypes.length));
    for (const feature of features) {
      const value = featureValue(row, feature);
      const valueCount = featureCounts.get(`${candidate}\t${feature}\t${value}`) ?? 0;
      const valueSpaceSize = (featureValueSpaces.get(feature)?.size ?? 0) + 1;
      score += Math.log((valueCount + alpha) / (labelCount + alpha * valueSpaceSize));
    }
    return score;
  };
}

function rank(row, trainRows, features) {
  const scorer = buildModel(trainRows, features);
  const ranked = targetSubtypes
    .map((candidate) => ({ candidate, score: scorer(candidate, row) }))
    .sort((a, b) => b.score - a.score || a.candidate.localeCompare(b.candidate));
  const index = ranked.findIndex((candidate) => candidate.candidate === row.subtype);
  return {
    rank: index + 1,
    predicted_top1: ranked[0]?.candidate ?? '',
    predicted_top2: ranked[1]?.candidate ?? '',
    top1: index === 0,
    top2: index <= 1,
  };
}

const modelFeatures = {
  frequency: [],
  object: ['type', 'site', 'sides'],
  dimensions: ['h_bin', 'v_bin', 'area_bin', 'aspect_bin', 'th_bin'],
  side_context: ['short_side_index', 'order', 'context_class', 'side_relation', 'longer_row_count'],
  long_text_family: ['long_family', 'long_token_set', 'long_edge_frames', 'long_first_tokens', 'long_last_tokens', 'long_length_bin'],
  combined_no_exact_long: [
    'type',
    'site',
    'sides',
    'h_bin',
    'v_bin',
    'area_bin',
    'aspect_bin',
    'th_bin',
    'short_side_index',
    'order',
    'context_class',
    'side_relation',
    'longer_row_count',
    'long_edge_frames',
    'long_first_tokens',
    'long_last_tokens',
    'long_length_bin',
    'long_has_176',
    'long_has_400',
    'long_has_520',
    'long_has_690',
    'long_has_740',
    'long_has_861',
  ],
  combined_with_exact_long: [
    'type',
    'site',
    'sides',
    'h_bin',
    'v_bin',
    'area_bin',
    'aspect_bin',
    'th_bin',
    'short_side_index',
    'order',
    'context_class',
    'side_relation',
    'longer_row_count',
    'long_family',
    'long_token_set',
    'long_edge_frames',
    'long_first_tokens',
    'long_last_tokens',
    'long_length_bin',
    'long_has_176',
    'long_has_400',
    'long_has_520',
    'long_has_690',
    'long_has_740',
    'long_has_861',
  ],
};

function predictScope(rows, scope, leaveoutMode) {
  const out = [];
  for (const row of rows) {
    const trainRows = rows.filter((candidate) => {
      if (candidate.row_id === row.row_id) return false;
      if (candidate.cisi === row.cisi) return false;
      if (leaveoutMode === 'sequence_family' && candidate.sequence_family_key === row.sequence_family_key) return false;
      return true;
    });
    if (!trainRows.length) continue;
    for (const [model, features] of Object.entries(modelFeatures)) {
      const prediction = rank(row, trainRows, features);
      out.push({
        scope,
        leaveout_mode: leaveoutMode,
        model,
        row_id: row.row_id,
        cisi: row.cisi,
        subtype: row.subtype,
        type: row.type,
        sides: row.sides,
        context_class: row.context_class,
        side_relation: row.side_relation,
        long_family: row.long_family,
        rank: prediction.rank,
        predicted_top1: prediction.predicted_top1,
        predicted_top2: prediction.predicted_top2,
        top1: prediction.top1,
        top2: prediction.top2,
      });
    }
  }
  return out;
}

function median(values) {
  const sorted = [...values].sort((a, b) => a - b);
  return sorted[Math.floor((sorted.length - 1) / 2)] ?? null;
}

function summarizePredictions(rows) {
  const groups = new Map();
  for (const row of rows) {
    const key = `${row.scope}\t${row.leaveout_mode}\t${row.model}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(row);
  }
  return [...groups.entries()]
    .map(([key, group]) => {
      const [scope, leaveoutMode, model] = key.split('\t');
      const top1 = group.filter((row) => row.top1).length;
      const top2 = group.filter((row) => row.top2).length;
      return {
        scope,
        leaveout_mode: leaveoutMode,
        model,
        predictions: group.length,
        top1,
        top1_accuracy: formatNumber(top1 / group.length),
        top2,
        top2_accuracy: formatNumber(top2 / group.length),
        median_rank: formatNumber(median(group.map((row) => Number(row.rank)))),
        subtype_032_top1: formatSubtypeAccuracy(group, '032'),
        subtype_033_top1: formatSubtypeAccuracy(group, '033'),
        subtype_034_top1: formatSubtypeAccuracy(group, '034'),
      };
    })
    .sort(
      (a, b) =>
        a.scope.localeCompare(b.scope) ||
        a.leaveout_mode.localeCompare(b.leaveout_mode) ||
        b.top1_accuracy - a.top1_accuracy ||
        a.model.localeCompare(b.model),
    );
}

function formatSubtypeAccuracy(group, subtype) {
  const subset = group.filter((row) => row.subtype === subtype);
  if (!subset.length) return '';
  return formatNumber(subset.filter((row) => row.top1).length / subset.length);
}

function featureContrasts(rows, scope) {
  const features = [
    'type',
    'sides',
    'h_bin',
    'v_bin',
    'area_bin',
    'aspect_bin',
    'short_side_index',
    'order',
    'context_class',
    'side_relation',
    'longer_row_count',
    'long_token_set',
    'long_edge_frames',
    'long_first_tokens',
    'long_last_tokens',
    'long_length_bin',
    'long_has_176',
    'long_has_400',
    'long_has_740',
  ];
  const out = [];
  for (const feature of features) {
    const values = [...new Set(rows.map((row) => row[feature] ?? 'MISSING'))].sort((a, b) => a.localeCompare(b));
    for (const value of values) {
      for (const subtype of targetSubtypes) {
        const inSubtype = rows.filter((row) => row.subtype === subtype);
        const outSubtype = rows.filter((row) => row.subtype !== subtype);
        const inCount = inSubtype.filter((row) => (row[feature] ?? 'MISSING') === value).length;
        const outCount = outSubtype.filter((row) => (row[feature] ?? 'MISSING') === value).length;
        if (inCount < 3) continue;
        const inShare = inCount / inSubtype.length;
        const outShare = outCount / outSubtype.length;
        out.push({
          scope,
          feature,
          value,
          subtype,
          in_subtype_count: inCount,
          subtype_total: inSubtype.length,
          in_subtype_share: inShare,
          out_subtype_count: outCount,
          out_subtype_total: outSubtype.length,
          out_subtype_share: outShare,
          lift_vs_other_subtypes: outShare === 0 ? null : inShare / outShare,
        });
      }
    }
  }
  return out.sort(
    (a, b) =>
      (b.lift_vs_other_subtypes ?? 999) - (a.lift_vs_other_subtypes ?? 999) ||
      b.in_subtype_count - a.in_subtype_count ||
      a.feature.localeCompare(b.feature) ||
      a.value.localeCompare(b.value),
  );
}

const validationRows = readCsvRecords(validationPath);
const validationByCisi = new Map(validationRows.map((row) => [row.cisi, row]));
const companionRows = readCsvRecords(companionPath);

const rows = companionRows
  .filter((row) => isExactFrame700Subtype(row))
  .map((row) => {
    const validation = validationByCisi.get(row.cisi) ?? {};
    const horizontal = parsePositiveNumber(validation.horizontal_mm);
    const vertical = parsePositiveNumber(validation.vertical_mm);
    const thickness = parsePositiveNumber(validation.thickness_mm);
    const longSides = parseLongSides(row.longer_texts);
    const long = longFeatures(longSides);
    const sequenceFamilyKey = norm(validation.sequence_signature) || norm(row.group_signature) || norm(row.longer_texts) || 'NO_SIGNATURE';
    return {
      row_id: row.id,
      cisi: row.cisi,
      subtype: row.companion,
      target_label: `FRAME700_SUBTYPE${row.companion}`,
      is_h_series: hSeries.has(row.cisi) ? 'true' : 'false',
      priority: validation.priority ?? '',
      type: row.type,
      site: row.site,
      sides: row.sides,
      direction: row.direction,
      short_side_index: row.short_side_index || 'MISSING',
      order: row.order || 'MISSING',
      short_text: row.short_text,
      context_class: row.context_class || 'MISSING',
      side_relation: row.side_relation || 'MISSING',
      longer_row_count: row.longer_row_count || '0',
      longer_side_indexes: row.longer_side_indexes,
      longer_texts: row.longer_texts,
      longer_tokens: row.longer_tokens,
      group_signature: row.group_signature,
      sequence_family_key: sequenceFamilyKey,
      horizontal_mm: horizontal,
      vertical_mm: vertical,
      thickness_mm: thickness,
      h_bin: binHorizontal(horizontal),
      v_bin: binVertical(vertical),
      th_bin: binThickness(thickness),
      area_bin: binArea(horizontal, vertical),
      aspect_bin: binAspect(horizontal, vertical),
      ...long,
    };
  })
  .sort((a, b) => a.cisi.localeCompare(b.cisi) || a.row_id.localeCompare(b.row_id));

const noHRows = rows.filter((row) => row.is_h_series !== 'true');
const predictionRows = [
  ...predictScope(rows, 'all_frame700_subtypes', 'artifact'),
  ...predictScope(noHRows, 'excluding_h2218_h2239', 'artifact'),
  ...predictScope(rows, 'all_frame700_subtypes', 'sequence_family'),
  ...predictScope(noHRows, 'excluding_h2218_h2239', 'sequence_family'),
];
const predictionSummary = summarizePredictions(predictionRows);
const contrasts = [
  ...featureContrasts(rows, 'all_frame700_subtypes'),
  ...featureContrasts(noHRows, 'excluding_h2218_h2239'),
];

fs.writeFileSync(
  rowsPath,
  toCsv([
    [
      'row_id',
      'cisi',
      'subtype',
      'target_label',
      'is_h_series',
      'priority',
      'type',
      'site',
      'sides',
      'direction',
      'short_side_index',
      'order',
      'short_text',
      'context_class',
      'side_relation',
      'longer_row_count',
      'longer_texts',
      'sequence_family_key',
      'horizontal_mm',
      'vertical_mm',
      'thickness_mm',
      'h_bin',
      'v_bin',
      'area_bin',
      'aspect_bin',
      'th_bin',
      'long_family',
      'long_token_set',
      'long_edge_frames',
      'long_first_tokens',
      'long_last_tokens',
      'long_length_bin',
    ],
    ...rows.map((row) => [
      row.row_id,
      row.cisi,
      row.subtype,
      row.target_label,
      row.is_h_series,
      row.priority,
      row.type,
      row.site,
      row.sides,
      row.direction,
      row.short_side_index,
      row.order,
      row.short_text,
      row.context_class,
      row.side_relation,
      row.longer_row_count,
      row.longer_texts,
      row.sequence_family_key,
      row.horizontal_mm,
      row.vertical_mm,
      row.thickness_mm,
      row.h_bin,
      row.v_bin,
      row.area_bin,
      row.aspect_bin,
      row.th_bin,
      row.long_family,
      row.long_token_set,
      row.long_edge_frames,
      row.long_first_tokens,
      row.long_last_tokens,
      row.long_length_bin,
    ]),
  ]),
  'utf8',
);

fs.writeFileSync(
  predictionsPath,
  toCsv([
    [
      'scope',
      'leaveout_mode',
      'model',
      'row_id',
      'cisi',
      'subtype',
      'type',
      'sides',
      'context_class',
      'side_relation',
      'long_family',
      'rank',
      'predicted_top1',
      'predicted_top2',
      'top1',
      'top2',
    ],
    ...predictionRows.map((row) => [
      row.scope,
      row.leaveout_mode,
      row.model,
      row.row_id,
      row.cisi,
      row.subtype,
      row.type,
      row.sides,
      row.context_class,
      row.side_relation,
      row.long_family,
      row.rank,
      row.predicted_top1,
      row.predicted_top2,
      row.top1,
      row.top2,
    ]),
  ]),
  'utf8',
);

fs.writeFileSync(
  predictionSummaryPath,
  toCsv([
    [
      'scope',
      'leaveout_mode',
      'model',
      'predictions',
      'top1',
      'top1_accuracy',
      'top2',
      'top2_accuracy',
      'median_rank',
      'subtype_032_top1',
      'subtype_033_top1',
      'subtype_034_top1',
    ],
    ...predictionSummary.map((row) => [
      row.scope,
      row.leaveout_mode,
      row.model,
      row.predictions,
      row.top1,
      row.top1_accuracy,
      row.top2,
      row.top2_accuracy,
      row.median_rank,
      row.subtype_032_top1,
      row.subtype_033_top1,
      row.subtype_034_top1,
    ]),
  ]),
  'utf8',
);

fs.writeFileSync(
  featureContrastsPath,
  toCsv([
    [
      'scope',
      'feature',
      'value',
      'subtype',
      'in_subtype_count',
      'subtype_total',
      'in_subtype_share',
      'out_subtype_count',
      'out_subtype_total',
      'out_subtype_share',
      'lift_vs_other_subtypes',
    ],
    ...contrasts.map((row) => [
      row.scope,
      row.feature,
      row.value,
      row.subtype,
      row.in_subtype_count,
      row.subtype_total,
      formatNumber(row.in_subtype_share),
      row.out_subtype_count,
      row.out_subtype_total,
      formatNumber(row.out_subtype_share),
      formatNumber(row.lift_vs_other_subtypes),
    ]),
  ]),
  'utf8',
);

const bestByScope = Object.values(
  predictionSummary.reduce((acc, row) => {
    const key = `${row.scope}\t${row.leaveout_mode}`;
    if (!acc[key] || Number(row.top1_accuracy) > Number(acc[key].top1_accuracy)) acc[key] = row;
    return acc;
  }, {}),
);

const summary = {
  generated_at_local: new Date().toISOString(),
  experiment: 'Lipi FRAME700 subtype discrimination',
  question:
    'Within +700-032+, +700-033+, and +700-034+ short-side contexts, can subtype be predicted from object metadata, dimensions, side context, and companion long-side text family?',
  inputs: [
    'data/open_prototype/reports/lipi_short_mark_companion_context_rows.csv',
    'data/open_prototype/reports/lipi_multiside_mark_validation_queue.csv',
  ],
  target_rows: rows.length,
  unique_artifacts: new Set(rows.map((row) => row.cisi)).size,
  h_series_rows: rows.filter((row) => row.is_h_series === 'true').length,
  no_h_series_rows: noHRows.length,
  counts_by_subtype: countBy(rows, (row) => row.subtype),
  counts_by_subtype_excluding_h2218_h2239: countBy(noHRows, (row) => row.subtype),
  counts_by_context_class: countBy(rows, (row) => row.context_class),
  counts_by_side_relation: countBy(rows, (row) => row.side_relation),
  sequence_family_keys: new Set(rows.map((row) => row.sequence_family_key)).size,
  top_sequence_families: Object.entries(countBy(rows, (row) => row.sequence_family_key)).slice(0, 12),
  prediction_summary: predictionSummary,
  best_by_scope: bestByScope,
  top_feature_contrasts: contrasts.slice(0, 25).map((row) => ({
    scope: row.scope,
    feature: row.feature,
    value: row.value,
    subtype: row.subtype,
    in_subtype_count: row.in_subtype_count,
    subtype_total: row.subtype_total,
    in_subtype_share: formatNumber(row.in_subtype_share),
    out_subtype_share: formatNumber(row.out_subtype_share),
    lift_vs_other_subtypes: formatNumber(row.lift_vs_other_subtypes),
  })),
  interpretation_boundary:
    'Subtype discrimination is functional/context evidence only. It does not establish sign meaning, numerical value, metrological reading, phonetic reading, language identity, or translation.',
  outputs: [
    'data/open_prototype/reports/lipi_frame700_subtype_rows.csv',
    'data/open_prototype/reports/lipi_frame700_subtype_predictions.csv',
    'data/open_prototype/reports/lipi_frame700_subtype_prediction_summary.csv',
    'data/open_prototype/reports/lipi_frame700_subtype_feature_contrasts.csv',
    'data/open_prototype/reports/lipi_frame700_subtype_summary.json',
  ],
};

fs.writeFileSync(summaryPath, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
