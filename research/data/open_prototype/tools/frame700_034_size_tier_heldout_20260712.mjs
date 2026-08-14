import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const inputPath = path.join(root, 'research', 'data', 'open_prototype', 'reports', 'lipi_frame700_subtype_rows.csv');
const reportsDir = path.join(root, 'research', 'data', 'open_prototype', 'reports');
const predictionsPath = path.join(reportsDir, 'frame700_034_size_tier_heldout_20260712_predictions.csv');
const nullsPath = path.join(reportsDir, 'frame700_034_size_tier_heldout_20260712_null_iterations.csv');
const summaryPath = path.join(reportsDir, 'frame700_034_size_tier_heldout_20260712_summary.json');

const DESIGN = Object.freeze({
  date: '2026-07-12',
  hypothesis:
    'Within Harappa multi-side TAB:B/TAB:I artifacts carrying exact 700-032, 700-033, or 700-034 short marks, subtype 034 identifies a reproducible smaller-object or administrative-size tier that generalizes beyond copied/source families.',
  target: '034 versus pooled 032/033',
  eligibility: [
    'Rows from lipi_frame700_subtype_rows.csv',
    'Subtype is 032, 033, or 034',
    'Positive scalar horizontal_mm and vertical_mm are both present',
    'One artifact vote: duplicate rows from the same CISI object and subtype collapse deterministically',
  ],
  source_family_holdout: [
    'All H-2218 through H-2239 rows form one held-out source series',
    'Otherwise rows with a longer text are grouped by exact longer-text family, regardless of short subtype',
    'Rows without a longer text are grouped by their complete sequence_family_key',
  ],
  models: {
    dimension_target: 'balanced-prior nearest centroid over training-standardized log horizontal and log vertical dimensions',
    administrative_format_baseline: 'balanced-prior categorical Naive Bayes over type, sides, 700 order, context class, and side relation',
    emblem_formula_baseline: 'balanced-prior categorical Naive Bayes over type, 700 order, longer token set, edge frames, first/last signs, and longer-text length bin',
  },
  matched_nulls: {
    administrative_format:
      'Shuffle 034 labels within type|sides|700-order|context-class|side-relation blocks, retaining format and dimension composition.',
    emblem_copy_family:
      'Shuffle labels within recurrent held-out source families; singleton families are pooled by type|sides|700-order|context-class.',
  },
  bootstrap_iterations: 5000,
  null_iterations_per_policy: 2000,
  bootstrap_seed: 34072026,
  administrative_null_seed: 34072027,
  emblem_null_seed: 34072028,
  pass_gate: [
    'Grouped-bootstrap 95% lower bound for dimension-model ROC AUC is greater than 0.50',
    'Grouped-bootstrap 95% lower bound for dimension AUC minus administrative-format baseline AUC is greater than 0',
    'Grouped-bootstrap 95% lower bound for dimension AUC minus emblem-formula baseline AUC is greater than 0',
    'Dimension AUC exceeds at least 95% of each matched-null distribution',
    'On the completely held-out H-2218 through H-2239 series, 034 recall is at least 0.80 and the one 033 control is correctly rejected',
  ],
});

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;
  for (let index = 0; index < text.length; index++) {
    const char = text[index];
    if (inQuotes) {
      if (char === '"') {
        if (text[index + 1] === '"') {
          field += '"';
          index++;
        } else {
          inQuotes = false;
        }
      } else {
        field += char;
      }
    } else if (char === '"') {
      inQuotes = true;
    } else if (char === ',') {
      row.push(field);
      field = '';
    } else if (char === '\n') {
      row.push(field);
      field = '';
      if (row.length > 1 || row[0] !== '') rows.push(row);
      row = [];
    } else if (char !== '\r') {
      field += char;
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

function csvEscape(value) {
  return `"${String(value ?? '').replaceAll('"', '""')}"`;
}

function writeCsv(filePath, header, rows) {
  const lines = [header.map(csvEscape).join(',')];
  for (const row of rows) lines.push(header.map((key) => csvEscape(row[key])).join(','));
  fs.writeFileSync(filePath, `${lines.join('\n')}\n`);
}

function positiveNumber(value) {
  const text = String(value ?? '').trim();
  if (!/^(?:\d+(?:\.\d+)?|\.\d+)$/.test(text)) return null;
  const number = Number(text);
  return Number.isFinite(number) && number > 0 ? number : null;
}

function isHSeries(cisi) {
  const match = String(cisi).match(/^H-(\d+)$/);
  if (!match) return false;
  const number = Number(match[1]);
  return number >= 2218 && number <= 2239;
}

function sourceGroup(row) {
  if (isHSeries(row.cisi)) return 'series:H-2218-H-2239';
  if (row.long_family && row.long_family !== 'NO_LONGER_TEXT') return `long:${row.long_family}`;
  return `no_long:${row.sequence_family_key}`;
}

function mulberry32(seed) {
  let state = seed >>> 0;
  return () => {
    state += 0x6d2b79f5;
    let value = state;
    value = Math.imul(value ^ (value >>> 15), value | 1);
    value ^= value + Math.imul(value ^ (value >>> 7), value | 61);
    return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffle(values, rng) {
  const result = [...values];
  for (let index = result.length - 1; index > 0; index--) {
    const swapIndex = Math.floor(rng() * (index + 1));
    [result[index], result[swapIndex]] = [result[swapIndex], result[index]];
  }
  return result;
}

function groupIndices(rows, keyFn) {
  const groups = new Map();
  rows.forEach((row, index) => {
    const key = keyFn(row);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(index);
  });
  return groups;
}

function mean(values) {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function sampleSd(values, center = mean(values)) {
  if (values.length < 2) return 1;
  const variance = values.reduce((sum, value) => sum + (value - center) ** 2, 0) / (values.length - 1);
  return Math.sqrt(variance) || 1;
}

function quantile(values, probability) {
  if (!values.length) return null;
  const sorted = [...values].sort((a, b) => a - b);
  const position = (sorted.length - 1) * probability;
  const lower = Math.floor(position);
  const upper = Math.ceil(position);
  if (lower === upper) return sorted[lower];
  return sorted[lower] + (sorted[upper] - sorted[lower]) * (position - lower);
}

function rounded(value, digits = 6) {
  if (value === null || value === undefined || !Number.isFinite(value)) return null;
  return Number(value.toFixed(digits));
}

function binaryMetrics(labels, scores, predicted = scores.map((score) => (score >= 0 ? 1 : 0))) {
  let tp = 0;
  let tn = 0;
  let fp = 0;
  let fn = 0;
  for (let index = 0; index < labels.length; index++) {
    if (labels[index] === 1 && predicted[index] === 1) tp++;
    else if (labels[index] === 0 && predicted[index] === 0) tn++;
    else if (labels[index] === 0 && predicted[index] === 1) fp++;
    else fn++;
  }
  const recall = tp + fn ? tp / (tp + fn) : null;
  const specificity = tn + fp ? tn / (tn + fp) : null;
  const precisionPositive = tp + fp ? tp / (tp + fp) : 0;
  const precisionNegative = tn + fn ? tn / (tn + fn) : 0;
  const f1Positive = precisionPositive + recall ? (2 * precisionPositive * recall) / (precisionPositive + recall) : 0;
  const negativeRecall = specificity;
  const f1Negative = precisionNegative + negativeRecall ? (2 * precisionNegative * negativeRecall) / (precisionNegative + negativeRecall) : 0;

  const positives = [];
  const negatives = [];
  labels.forEach((label, index) => (label === 1 ? positives : negatives).push(scores[index]));
  let auc = null;
  if (positives.length && negatives.length) {
    let wins = 0;
    for (const positive of positives) {
      for (const negative of negatives) {
        if (positive > negative) wins += 1;
        else if (positive === negative) wins += 0.5;
      }
    }
    auc = wins / (positives.length * negatives.length);
  }

  return {
    rows: labels.length,
    positives: positives.length,
    negatives: negatives.length,
    tp,
    tn,
    fp,
    fn,
    accuracy: (tp + tn) / labels.length,
    balanced_accuracy: recall === null || specificity === null ? null : (recall + specificity) / 2,
    recall_034: recall,
    specificity_non034: specificity,
    macro_f1: (f1Positive + f1Negative) / 2,
    roc_auc: auc,
  };
}

function dimensionFoldScores(rows, labels, testIndices) {
  const testSet = new Set(testIndices);
  const trainIndices = rows.map((_, index) => index).filter((index) => !testSet.has(index));
  const logH = trainIndices.map((index) => rows[index].log_h);
  const logV = trainIndices.map((index) => rows[index].log_v);
  const hMean = mean(logH);
  const vMean = mean(logV);
  const hSd = sampleSd(logH, hMean);
  const vSd = sampleSd(logV, vMean);
  const standardized = (row) => [(row.log_h - hMean) / hSd, (row.log_v - vMean) / vSd];
  const classPoints = [[], []];
  for (const index of trainIndices) classPoints[labels[index]].push(standardized(rows[index]));
  if (!classPoints[0].length || !classPoints[1].length) throw new Error('A held-out fold removed an entire target class.');
  const centroid = classPoints.map((points) => [mean(points.map((point) => point[0])), mean(points.map((point) => point[1]))]);
  return testIndices.map((index) => {
    const point = standardized(rows[index]);
    const distance0 = (point[0] - centroid[0][0]) ** 2 + (point[1] - centroid[0][1]) ** 2;
    const distance1 = (point[0] - centroid[1][0]) ** 2 + (point[1] - centroid[1][1]) ** 2;
    return distance0 - distance1;
  });
}

function categoricalFoldScores(rows, labels, testIndices, features, alpha = 0.5) {
  const testSet = new Set(testIndices);
  const trainIndices = rows.map((_, index) => index).filter((index) => !testSet.has(index));
  const classCounts = [0, 0];
  const spaces = new Map(features.map((feature) => [feature, new Set()]));
  const counts = new Map();
  for (const index of trainIndices) {
    const label = labels[index];
    classCounts[label]++;
    for (const feature of features) {
      const value = String(rows[index][feature] ?? 'MISSING');
      spaces.get(feature).add(value);
      const key = `${label}\t${feature}\t${value}`;
      counts.set(key, (counts.get(key) ?? 0) + 1);
    }
  }
  return testIndices.map((index) => {
    const classScores = [0, 1].map((label) => {
      let score = Math.log(0.5);
      for (const feature of features) {
        const value = String(rows[index][feature] ?? 'MISSING');
        const count = counts.get(`${label}\t${feature}\t${value}`) ?? 0;
        const spaceSize = spaces.get(feature).size + 1;
        score += Math.log((count + alpha) / (classCounts[label] + alpha * spaceSize));
      }
      return score;
    });
    return classScores[1] - classScores[0];
  });
}

function groupedOutOfFold(rows, labels, model) {
  const groups = groupIndices(rows, (row) => row.source_group);
  const scores = Array(rows.length).fill(null);
  for (const indices of groups.values()) {
    const foldScores =
      model.kind === 'dimension'
        ? dimensionFoldScores(rows, labels, indices)
        : categoricalFoldScores(rows, labels, indices, model.features);
    indices.forEach((rowIndex, position) => {
      scores[rowIndex] = foldScores[position];
    });
  }
  if (scores.some((score) => score === null)) throw new Error(`Missing out-of-fold scores for ${model.name}.`);
  return scores;
}

function shuffledLabels(rows, labels, blockFn, seed) {
  const rng = mulberry32(seed);
  const blocks = groupIndices(rows, blockFn);
  const result = [...labels];
  for (const indices of blocks.values()) {
    const values = shuffle(indices.map((index) => labels[index]), rng);
    indices.forEach((rowIndex, position) => {
      result[rowIndex] = values[position];
    });
  }
  const unchanged = result.filter((label, index) => label === labels[index]).length / labels.length;
  return { labels: result, unchanged_share: unchanged, blocks: blocks.size };
}

function bootstrapMetrics(rows, labels, modelScores, iterations, seed) {
  const rng = mulberry32(seed);
  const groups = [...groupIndices(rows, (row) => row.source_group).values()];
  const output = [];
  for (let iteration = 0; iteration < iterations; iteration++) {
    const indices = [];
    for (let sample = 0; sample < groups.length; sample++) {
      const group = groups[Math.floor(rng() * groups.length)];
      indices.push(...group);
    }
    const sampleLabels = indices.map((index) => labels[index]);
    if (!sampleLabels.includes(0) || !sampleLabels.includes(1)) {
      iteration--;
      continue;
    }
    const metrics = {};
    for (const [name, scores] of Object.entries(modelScores)) {
      metrics[name] = binaryMetrics(sampleLabels, indices.map((index) => scores[index]));
    }
    output.push({
      dimension_auc: metrics.dimension.roc_auc,
      dimension_balanced_accuracy: metrics.dimension.balanced_accuracy,
      dimension_minus_format_auc: metrics.dimension.roc_auc - metrics.administrative_format.roc_auc,
      dimension_minus_emblem_auc: metrics.dimension.roc_auc - metrics.emblem_formula.roc_auc,
    });
  }
  const interval = (key) => ({
    low: rounded(quantile(output.map((row) => row[key]), 0.025)),
    median: rounded(quantile(output.map((row) => row[key]), 0.5)),
    high: rounded(quantile(output.map((row) => row[key]), 0.975)),
  });
  return {
    iterations: output.length,
    dimension_auc: interval('dimension_auc'),
    dimension_balanced_accuracy: interval('dimension_balanced_accuracy'),
    dimension_minus_format_auc: interval('dimension_minus_format_auc'),
    dimension_minus_emblem_auc: interval('dimension_minus_emblem_auc'),
  };
}

const rawRows = readCsvRecords(inputPath);
const eligible = rawRows
  .map((row) => ({ ...row, horizontal: positiveNumber(row.horizontal_mm), vertical: positiveNumber(row.vertical_mm) }))
  .filter((row) => ['032', '033', '034'].includes(row.subtype) && row.horizontal !== null && row.vertical !== null)
  .sort((a, b) => a.cisi.localeCompare(b.cisi) || a.subtype.localeCompare(b.subtype) || a.row_id.localeCompare(b.row_id));

const deduplicated = [];
const seen = new Set();
for (const row of eligible) {
  const key = `${row.cisi}\t${row.subtype}`;
  if (seen.has(key)) continue;
  seen.add(key);
  deduplicated.push({
    ...row,
    target_034: row.subtype === '034' ? 1 : 0,
    log_h: Math.log(row.horizontal),
    log_v: Math.log(row.vertical),
    area: row.horizontal * row.vertical,
    aspect: row.horizontal / row.vertical,
    source_group: sourceGroup(row),
  });
}

const rows = deduplicated;
const labels = rows.map((row) => row.target_034);
const sourceGroups = groupIndices(rows, (row) => row.source_group);
const sourceGroupSizes = new Map([...sourceGroups].map(([key, indices]) => [key, indices.length]));
rows.forEach((row) => {
  row.emblem_null_block =
    sourceGroupSizes.get(row.source_group) >= 2
      ? row.source_group
      : `singleton_pool:${row.type}|${row.sides}|${row.order}|${row.context_class}`;
  row.administrative_null_block = `${row.type}|${row.sides}|${row.order}|${row.context_class}|${row.side_relation}`;
});

const models = {
  dimension: { name: 'dimension', kind: 'dimension' },
  administrative_format: {
    name: 'administrative_format',
    kind: 'categorical',
    features: ['type', 'sides', 'order', 'context_class', 'side_relation'],
  },
  emblem_formula: {
    name: 'emblem_formula',
    kind: 'categorical',
    features: ['type', 'order', 'long_token_set', 'long_edge_frames', 'long_first_tokens', 'long_last_tokens', 'long_length_bin'],
  },
};

const scores = Object.fromEntries(Object.entries(models).map(([name, model]) => [name, groupedOutOfFold(rows, labels, model)]));
const observed = Object.fromEntries(Object.entries(scores).map(([name, modelScores]) => [name, binaryMetrics(labels, modelScores)]));
const bootstrap = bootstrapMetrics(rows, labels, scores, DESIGN.bootstrap_iterations, DESIGN.bootstrap_seed);

const nullRows = [];
const nullSummaries = {};
const nullPolicies = [
  {
    name: 'administrative_format',
    seed: DESIGN.administrative_null_seed,
    block: (row) => row.administrative_null_block,
  },
  {
    name: 'emblem_copy_family',
    seed: DESIGN.emblem_null_seed,
    block: (row) => row.emblem_null_block,
  },
];

for (const policy of nullPolicies) {
  const aucs = [];
  const balanced = [];
  const recalls = [];
  const unchanged = [];
  let blockCount = null;
  for (let iteration = 0; iteration < DESIGN.null_iterations_per_policy; iteration++) {
    const shuffled = shuffledLabels(rows, labels, policy.block, policy.seed + iteration);
    blockCount = shuffled.blocks;
    const nullScores = groupedOutOfFold(rows, shuffled.labels, models.dimension);
    const metrics = binaryMetrics(shuffled.labels, nullScores);
    aucs.push(metrics.roc_auc);
    balanced.push(metrics.balanced_accuracy);
    recalls.push(metrics.recall_034);
    unchanged.push(shuffled.unchanged_share);
    nullRows.push({
      policy: policy.name,
      iteration,
      seed: policy.seed + iteration,
      blocks: shuffled.blocks,
      unchanged_label_share: rounded(shuffled.unchanged_share),
      roc_auc: rounded(metrics.roc_auc),
      balanced_accuracy: rounded(metrics.balanced_accuracy),
      recall_034: rounded(metrics.recall_034),
      specificity_non034: rounded(metrics.specificity_non034),
    });
  }
  const observedAuc = observed.dimension.roc_auc;
  nullSummaries[policy.name] = {
    iterations: DESIGN.null_iterations_per_policy,
    blocks: blockCount,
    mean_unchanged_label_share: rounded(mean(unchanged)),
    auc_mean: rounded(mean(aucs)),
    auc_p95: rounded(quantile(aucs, 0.95)),
    auc_null_ge_observed_share: rounded(aucs.filter((value) => value >= observedAuc).length / aucs.length),
    balanced_accuracy_mean: rounded(mean(balanced)),
    balanced_accuracy_p95: rounded(quantile(balanced, 0.95)),
    recall_034_mean: rounded(mean(recalls)),
    recall_034_p95: rounded(quantile(recalls, 0.95)),
  };
}

const hSeriesIndices = rows.map((row, index) => (isHSeries(row.cisi) ? index : null)).filter((index) => index !== null);
const hSeriesMetrics = binaryMetrics(
  hSeriesIndices.map((index) => labels[index]),
  hSeriesIndices.map((index) => scores.dimension[index]),
);

const gateChecks = {
  dimension_auc_ci_low_gt_chance: bootstrap.dimension_auc.low > 0.5,
  dimension_minus_format_auc_ci_low_gt_zero: bootstrap.dimension_minus_format_auc.low > 0,
  dimension_minus_emblem_auc_ci_low_gt_zero: bootstrap.dimension_minus_emblem_auc.low > 0,
  dimension_auc_beats_administrative_null_95pct: nullSummaries.administrative_format.auc_null_ge_observed_share <= 0.05,
  dimension_auc_beats_emblem_null_95pct: nullSummaries.emblem_copy_family.auc_null_ge_observed_share <= 0.05,
  h_series_034_recall_ge_0p80: hSeriesMetrics.recall_034 >= 0.8,
  h_series_033_control_correct: hSeriesMetrics.specificity_non034 === 1,
};
const pass = Object.values(gateChecks).every(Boolean);

const subtypeSummary = Object.fromEntries(
  ['032', '033', '034'].map((subtype) => {
    const subset = rows.filter((row) => row.subtype === subtype);
    return [
      subtype,
      {
        rows: subset.length,
        median_horizontal_mm: rounded(quantile(subset.map((row) => row.horizontal), 0.5)),
        median_vertical_mm: rounded(quantile(subset.map((row) => row.vertical), 0.5)),
        median_area_mm2: rounded(quantile(subset.map((row) => row.area), 0.5)),
        h_series_rows: subset.filter((row) => isHSeries(row.cisi)).length,
      },
    ];
  }),
);

const predictionRows = rows.map((row, index) => ({
  cisi: row.cisi,
  row_id: row.row_id,
  subtype: row.subtype,
  target_034: row.target_034,
  source_group: row.source_group,
  source_group_size: sourceGroupSizes.get(row.source_group),
  is_h_series: isHSeries(row.cisi),
  type: row.type,
  sides: row.sides,
  order: row.order,
  context_class: row.context_class,
  side_relation: row.side_relation,
  long_family: row.long_family,
  horizontal_mm: row.horizontal,
  vertical_mm: row.vertical,
  area_mm2: rounded(row.area),
  aspect: rounded(row.aspect),
  dimension_score: rounded(scores.dimension[index]),
  dimension_prediction_034: scores.dimension[index] >= 0 ? 1 : 0,
  administrative_format_score: rounded(scores.administrative_format[index]),
  administrative_format_prediction_034: scores.administrative_format[index] >= 0 ? 1 : 0,
  emblem_formula_score: rounded(scores.emblem_formula[index]),
  emblem_formula_prediction_034: scores.emblem_formula[index] >= 0 ? 1 : 0,
}));

const summary = {
  design: DESIGN,
  input: {
    path: path.relative(root, inputPath).replaceAll('\\', '/'),
    raw_rows: rawRows.length,
    positive_dimension_rows_before_artifact_collapse: eligible.length,
    eligible_artifact_rows: rows.length,
    collapsed_duplicate_artifact_rows: eligible.length - rows.length,
    source_groups: sourceGroups.size,
    h_series_rows: hSeriesIndices.length,
    subtype_summary: subtypeSummary,
  },
  observed: Object.fromEntries(
    Object.entries(observed).map(([name, metrics]) => [name, Object.fromEntries(Object.entries(metrics).map(([key, value]) => [key, rounded(value)]))]),
  ),
  grouped_bootstrap_95ci: bootstrap,
  matched_nulls: nullSummaries,
  h_series_complete_holdout: Object.fromEntries(Object.entries(hSeriesMetrics).map(([key, value]) => [key, rounded(value)])),
  gate: {
    checks: gateChecks,
    pass,
    decision: pass
      ? 'RETAIN_034_SIZE_OR_ADMINISTRATIVE_TIER_AS_DISTRIBUTIONAL_CANDIDATE_ONLY'
      : 'CLOSE_034_OBJECT_SIZE_OR_METROLOGICAL_TIER_UNDER_CURRENT_LOCAL_EVIDENCE',
  },
  interpretation: pass
    ? 'The pre-registered held-out-family gate passed. This supports only a reproducible size/form-context subtype association; it does not assign a number, unit, commodity, sign meaning, or translation.'
    : 'The pre-registered held-out-family gate failed. The earlier 034 size association does not generalize strongly enough beyond source/formula families and matched administrative/emblem confounds to support a numerical, metrological, or object-size-tier interpretation.',
};

writeCsv(predictionsPath, Object.keys(predictionRows[0]), predictionRows);
writeCsv(nullsPath, Object.keys(nullRows[0]), nullRows);
fs.writeFileSync(summaryPath, `${JSON.stringify(summary, null, 2)}\n`);

process.stdout.write(
  `${JSON.stringify(
    {
      eligible_artifact_rows: rows.length,
      source_groups: sourceGroups.size,
      observed: summary.observed,
      bootstrap: summary.grouped_bootstrap_95ci,
      matched_nulls: summary.matched_nulls,
      h_series_complete_holdout: summary.h_series_complete_holdout,
      gate: summary.gate,
    },
    null,
    2,
  )}\n`,
);
