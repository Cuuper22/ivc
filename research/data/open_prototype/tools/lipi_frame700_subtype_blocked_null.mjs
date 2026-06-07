import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const inputPath = path.join(reportsDir, 'lipi_frame700_subtype_rows.csv');

const iterationsPath = path.join(reportsDir, 'lipi_frame700_subtype_blocked_null_iterations.csv');
const summaryCsvPath = path.join(reportsDir, 'lipi_frame700_subtype_blocked_null_summary.csv');
const summaryJsonPath = path.join(reportsDir, 'lipi_frame700_subtype_blocked_null_summary.json');

const targetSubtypes = ['032', '033', '034'];
const alpha = 0.5;
const iterations = 100;
const seedBase = 700032033034;

const modelFeatures = {
  frequency: [],
  dimensions: ['h_bin', 'v_bin', 'area_bin', 'aspect_bin', 'th_bin'],
};

const blockPolicies = {
  global: [],
  type_sides_order: ['type', 'sides', 'order'],
  type_sides_order_context: ['type', 'sides', 'order', 'context_class'],
  type_sides_order_context_relation: ['type', 'sides', 'order', 'context_class', 'side_relation'],
};

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

function formatNumber(value, digits = 6) {
  return value === null || value === undefined || Number.isNaN(value) ? '' : Number(value.toFixed(digits));
}

function mulberry32(seed) {
  let value = seed >>> 0;
  return () => {
    value += 0x6d2b79f5;
    let t = value;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffle(values, random) {
  const copy = [...values];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

function add(map, key, by = 1) {
  map.set(key, (map.get(key) ?? 0) + by);
}

function featureValue(row, feature) {
  return `${feature}=${row[feature] || 'MISSING'}`;
}

function blockKey(row, fields) {
  return fields.length ? fields.map((field) => `${field}=${row[field] || 'MISSING'}`).join('|') : 'ALL_ROWS';
}

function median(values) {
  const sorted = [...values].sort((a, b) => a - b);
  return sorted[Math.floor((sorted.length - 1) / 2)] ?? null;
}

function quantile(values, q) {
  const sorted = [...values].sort((a, b) => a - b);
  if (!sorted.length) return null;
  const index = Math.min(sorted.length - 1, Math.max(0, Math.floor(q * (sorted.length - 1))));
  return sorted[index];
}

function precomputeTrainIndices(rows, leaveoutMode) {
  return rows.map((row, index) => {
    const train = [];
    for (let i = 0; i < rows.length; i++) {
      if (i === index) continue;
      const candidate = rows[i];
      if (candidate.cisi === row.cisi) continue;
      if (leaveoutMode === 'sequence_family' && candidate.sequence_family_key === row.sequence_family_key) continue;
      train.push(i);
    }
    return train;
  });
}

function buildModel(rows, assignedLabels, trainIndices, features) {
  const labelCounts = new Map();
  const featureValueSpaces = new Map();
  const featureCounts = new Map();
  for (const index of trainIndices) {
    const label = assignedLabels[index];
    add(labelCounts, label);
    for (const feature of features) {
      const value = featureValue(rows[index], feature);
      if (!featureValueSpaces.has(feature)) featureValueSpaces.set(feature, new Set());
      featureValueSpaces.get(feature).add(value);
      add(featureCounts, `${label}\t${feature}\t${value}`);
    }
  }
  return (candidate, row) => {
    const labelCount = labelCounts.get(candidate) ?? 0;
    let score = Math.log((labelCount + alpha) / (trainIndices.length + alpha * targetSubtypes.length));
    for (const feature of features) {
      const value = featureValue(row, feature);
      const count = featureCounts.get(`${candidate}\t${feature}\t${value}`) ?? 0;
      const valueSpaceSize = (featureValueSpaces.get(feature)?.size ?? 0) + 1;
      score += Math.log((count + alpha) / (labelCount + alpha * valueSpaceSize));
    }
    return score;
  };
}

function evaluate(rows, assignedLabels, trainIndexSets, modelName) {
  const features = modelFeatures[modelName];
  const bySubtype = new Map(targetSubtypes.map((subtype) => [subtype, { total: 0, top1: 0, top2: 0 }]));
  let top1 = 0;
  let top2 = 0;
  const ranks = [];
  for (let i = 0; i < rows.length; i++) {
    const scorer = buildModel(rows, assignedLabels, trainIndexSets[i], features);
    const ranked = targetSubtypes
      .map((candidate) => ({ candidate, score: scorer(candidate, rows[i]) }))
      .sort((a, b) => b.score - a.score || a.candidate.localeCompare(b.candidate));
    const actual = assignedLabels[i];
    const rank = ranked.findIndex((candidate) => candidate.candidate === actual) + 1;
    ranks.push(rank);
    const subtypeStats = bySubtype.get(actual);
    subtypeStats.total++;
    if (rank === 1) {
      top1++;
      subtypeStats.top1++;
    }
    if (rank <= 2) {
      top2++;
      subtypeStats.top2++;
    }
  }
  return {
    predictions: rows.length,
    top1_accuracy: top1 / rows.length,
    top2_accuracy: top2 / rows.length,
    median_rank: median(ranks),
    subtype_032_top1: bySubtype.get('032').top1 / bySubtype.get('032').total,
    subtype_033_top1: bySubtype.get('033').top1 / bySubtype.get('033').total,
    subtype_034_top1: bySubtype.get('034').top1 / bySubtype.get('034').total,
  };
}

function shuffledLabels(rows, blockFields, seed) {
  const random = mulberry32(seed);
  const groups = new Map();
  for (let i = 0; i < rows.length; i++) {
    const key = blockKey(rows[i], blockFields);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(i);
  }
  const labels = rows.map((row) => row.subtype);
  let mutableBlocks = 0;
  let singletonBlocks = 0;
  let moved = 0;
  for (const indices of groups.values()) {
    if (indices.length <= 1) {
      singletonBlocks++;
      continue;
    }
    mutableBlocks++;
    const original = indices.map((index) => labels[index]);
    const shuffled = shuffle(original, random);
    const before = [...original].sort().join(';');
    const after = [...shuffled].sort().join(';');
    if (before !== after) throw new Error(`Block label multiset changed for ${blockKey(rows[indices[0]], blockFields)}`);
    for (let i = 0; i < indices.length; i++) {
      if (labels[indices[i]] !== shuffled[i]) moved++;
      labels[indices[i]] = shuffled[i];
    }
  }
  return {
    labels,
    block_count: groups.size,
    singleton_blocks: singletonBlocks,
    mutable_blocks: mutableBlocks,
    moved_labels: moved,
  };
}

function summarizeIterations(nullRows, observedRows) {
  const groups = new Map();
  for (const row of nullRows) {
    const key = `${row.scope}\t${row.leaveout_mode}\t${row.block_policy}\t${row.model}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(row);
  }

  const out = [];
  for (const [key, group] of groups.entries()) {
    const [scope, leaveoutMode, blockPolicy, model] = key.split('\t');
    const observed = observedRows.find(
      (row) => row.scope === scope && row.leaveout_mode === leaveoutMode && row.model === model,
    );
    if (!observed) continue;
    const top1 = group.map((row) => row.top1_accuracy);
    const top2 = group.map((row) => row.top2_accuracy);
    const subtype034 = group.map((row) => row.subtype_034_top1);
    const top1Gain = group.map((row) => row.top1_gain_vs_frequency);
    const observedTop1Gain = observed.top1_gain_vs_frequency;
    out.push({
      scope,
      leaveout_mode: leaveoutMode,
      block_policy: blockPolicy,
      model,
      iterations: group.length,
      observed_top1: observed.top1_accuracy,
      null_top1_mean: mean(top1),
      null_top1_p95: quantile(top1, 0.95),
      p_ge_observed_top1: pGe(top1, observed.top1_accuracy),
      observed_top2: observed.top2_accuracy,
      null_top2_mean: mean(top2),
      null_top2_p95: quantile(top2, 0.95),
      p_ge_observed_top2: pGe(top2, observed.top2_accuracy),
      observed_034_top1: observed.subtype_034_top1,
      null_034_top1_mean: mean(subtype034),
      null_034_top1_p95: quantile(subtype034, 0.95),
      p_ge_observed_034_top1: pGe(subtype034, observed.subtype_034_top1),
      observed_top1_gain_vs_frequency: observedTop1Gain,
      null_top1_gain_mean: mean(top1Gain),
      null_top1_gain_p95: quantile(top1Gain, 0.95),
      p_ge_observed_top1_gain: pGe(top1Gain, observedTop1Gain),
      block_count: group[0].block_count,
      singleton_blocks: group[0].singleton_blocks,
      mutable_blocks: group[0].mutable_blocks,
      moved_labels_mean: mean(group.map((row) => row.moved_labels)),
    });
  }
  return out.sort(
    (a, b) =>
      a.scope.localeCompare(b.scope) ||
      a.leaveout_mode.localeCompare(b.leaveout_mode) ||
      a.block_policy.localeCompare(b.block_policy) ||
      a.model.localeCompare(b.model),
  );
}

function mean(values) {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function pGe(values, observed) {
  return values.filter((value) => value >= observed).length / values.length;
}

const rows = readCsvRecords(inputPath).filter((row) => row.is_h_series !== 'true');
const labels = rows.map((row) => row.subtype);
const scope = 'excluding_h2218_h2239';
const leaveoutMode = 'sequence_family';
const trainIndexSets = precomputeTrainIndices(rows, leaveoutMode);

const observedRows = [];
for (const modelName of Object.keys(modelFeatures)) {
  const metrics = evaluate(rows, labels, trainIndexSets, modelName);
  observedRows.push({
    scope,
    leaveout_mode: leaveoutMode,
    block_policy: 'observed',
    model: modelName,
    ...metrics,
  });
}
const observedFrequency = observedRows.find((row) => row.model === 'frequency');
for (const row of observedRows) {
  row.top1_gain_vs_frequency = row.top1_accuracy - observedFrequency.top1_accuracy;
}

const iterationRows = [];
for (const [blockPolicy, blockFields] of Object.entries(blockPolicies)) {
  for (let iteration = 1; iteration <= iterations; iteration++) {
    const shuffled = shuffledLabels(rows, blockFields, seedBase + iteration + blockPolicy.length * 1000);
    const frequencyMetrics = evaluate(rows, shuffled.labels, trainIndexSets, 'frequency');
    for (const modelName of Object.keys(modelFeatures)) {
      const metrics = modelName === 'frequency' ? frequencyMetrics : evaluate(rows, shuffled.labels, trainIndexSets, modelName);
      iterationRows.push({
        scope,
        leaveout_mode: leaveoutMode,
        block_policy: blockPolicy,
        iteration,
        model: modelName,
        block_count: shuffled.block_count,
        singleton_blocks: shuffled.singleton_blocks,
        mutable_blocks: shuffled.mutable_blocks,
        moved_labels: shuffled.moved_labels,
        ...metrics,
        top1_gain_vs_frequency: metrics.top1_accuracy - frequencyMetrics.top1_accuracy,
      });
    }
  }
}

const summaryRows = summarizeIterations(iterationRows, observedRows);

fs.writeFileSync(
  iterationsPath,
  toCsv([
    [
      'scope',
      'leaveout_mode',
      'block_policy',
      'iteration',
      'model',
      'block_count',
      'singleton_blocks',
      'mutable_blocks',
      'moved_labels',
      'predictions',
      'top1_accuracy',
      'top2_accuracy',
      'median_rank',
      'subtype_032_top1',
      'subtype_033_top1',
      'subtype_034_top1',
      'top1_gain_vs_frequency',
    ],
    ...iterationRows.map((row) => [
      row.scope,
      row.leaveout_mode,
      row.block_policy,
      row.iteration,
      row.model,
      row.block_count,
      row.singleton_blocks,
      row.mutable_blocks,
      row.moved_labels,
      row.predictions,
      formatNumber(row.top1_accuracy),
      formatNumber(row.top2_accuracy),
      row.median_rank,
      formatNumber(row.subtype_032_top1),
      formatNumber(row.subtype_033_top1),
      formatNumber(row.subtype_034_top1),
      formatNumber(row.top1_gain_vs_frequency),
    ]),
  ]),
  'utf8',
);

fs.writeFileSync(
  summaryCsvPath,
  toCsv([
    [
      'scope',
      'leaveout_mode',
      'block_policy',
      'model',
      'iterations',
      'observed_top1',
      'null_top1_mean',
      'null_top1_p95',
      'p_ge_observed_top1',
      'observed_top2',
      'null_top2_mean',
      'null_top2_p95',
      'p_ge_observed_top2',
      'observed_034_top1',
      'null_034_top1_mean',
      'null_034_top1_p95',
      'p_ge_observed_034_top1',
      'observed_top1_gain_vs_frequency',
      'null_top1_gain_mean',
      'null_top1_gain_p95',
      'p_ge_observed_top1_gain',
      'block_count',
      'singleton_blocks',
      'mutable_blocks',
      'moved_labels_mean',
    ],
    ...summaryRows.map((row) => [
      row.scope,
      row.leaveout_mode,
      row.block_policy,
      row.model,
      row.iterations,
      formatNumber(row.observed_top1),
      formatNumber(row.null_top1_mean),
      formatNumber(row.null_top1_p95),
      formatNumber(row.p_ge_observed_top1),
      formatNumber(row.observed_top2),
      formatNumber(row.null_top2_mean),
      formatNumber(row.null_top2_p95),
      formatNumber(row.p_ge_observed_top2),
      formatNumber(row.observed_034_top1),
      formatNumber(row.null_034_top1_mean),
      formatNumber(row.null_034_top1_p95),
      formatNumber(row.p_ge_observed_034_top1),
      formatNumber(row.observed_top1_gain_vs_frequency),
      formatNumber(row.null_top1_gain_mean),
      formatNumber(row.null_top1_gain_p95),
      formatNumber(row.p_ge_observed_top1_gain),
      row.block_count,
      row.singleton_blocks,
      row.mutable_blocks,
      formatNumber(row.moved_labels_mean),
    ]),
  ]),
  'utf8',
);

const keyRows = summaryRows.filter((row) => row.model === 'dimensions');
const summary = {
  generated_at_local: new Date().toISOString(),
  experiment: 'Lipi FRAME700 subtype blocked null',
  question:
    'Does the no-H-series FRAME700 subtype dimension signal exceed subtype-label shuffles inside matched object/context blocks?',
  input: 'data/open_prototype/reports/lipi_frame700_subtype_rows.csv',
  scope,
  leaveout_mode: leaveoutMode,
  target_rows: rows.length,
  iterations_per_policy: iterations,
  seed_base: seedBase,
  evaluated_models: Object.keys(modelFeatures),
  permutation_target_policy:
    'Subtype labels are shuffled within predeclared blocks and the model is scored against the shuffled labels. Row features remain fixed. This estimates feature-label association expected under the null block policy.',
  block_policies: Object.fromEntries(Object.entries(blockPolicies).map(([name, fields]) => [name, fields])),
  observed: observedRows.map((row) => ({
    model: row.model,
    top1_accuracy: formatNumber(row.top1_accuracy),
    top2_accuracy: formatNumber(row.top2_accuracy),
    subtype_034_top1: formatNumber(row.subtype_034_top1),
    top1_gain_vs_frequency: formatNumber(row.top1_gain_vs_frequency),
  })),
  dimension_null_summary: keyRows.map((row) => ({
    block_policy: row.block_policy,
    observed_top1: formatNumber(row.observed_top1),
    null_top1_mean: formatNumber(row.null_top1_mean),
    null_top1_p95: formatNumber(row.null_top1_p95),
    p_ge_observed_top1: formatNumber(row.p_ge_observed_top1),
    observed_034_top1: formatNumber(row.observed_034_top1),
    null_034_top1_mean: formatNumber(row.null_034_top1_mean),
    null_034_top1_p95: formatNumber(row.null_034_top1_p95),
    p_ge_observed_034_top1: formatNumber(row.p_ge_observed_034_top1),
    observed_top1_gain_vs_frequency: formatNumber(row.observed_top1_gain_vs_frequency),
    null_top1_gain_mean: formatNumber(row.null_top1_gain_mean),
    null_top1_gain_p95: formatNumber(row.null_top1_gain_p95),
    p_ge_observed_top1_gain: formatNumber(row.p_ge_observed_top1_gain),
    moved_labels_mean: formatNumber(row.moved_labels_mean),
  })),
  interpretation_boundary:
    'Blocked null for subtype-distribution evidence only. It accepts no sign meaning, numerical value, metrological reading, phonetic value, language identity, or translation.',
  outputs: [
    'data/open_prototype/reports/lipi_frame700_subtype_blocked_null_iterations.csv',
    'data/open_prototype/reports/lipi_frame700_subtype_blocked_null_summary.csv',
    'data/open_prototype/reports/lipi_frame700_subtype_blocked_null_summary.json',
  ],
};

fs.writeFileSync(summaryJsonPath, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
