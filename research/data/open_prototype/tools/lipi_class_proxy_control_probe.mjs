// Can the sign sequence of an inscription predict its (undefined) lipi.class
// label, beyond what boring proxies like object type, find site, or text
// length already predict? If yes, the class field encodes something about the
// text itself; if no, it is probably just a metadata echo. This script tests
// that. It collapses the clean numeric rows into exact-sequence families,
// gives each family a majority class label (keeping labels with at least 12
// families), and runs leave-one-out classifiers of increasing ambition:
// majority vote, then single-feature predictors (length, type, site, and
// combinations, plus first/last-sign edge frame), and finally a token naive
// Bayes over the signs themselves. Each observed accuracy and macro-F1 is
// compared to label-shuffle nulls that permute labels within blocks (global,
// length, type, site, and combinations — the blocked shuffles preserve the
// proxy structure), 20 iterations by default via IVC_CLASS_PROXY_ITERATIONS.
// Two extra label filters drop classes that the field audit showed are
// nearly pure proxies (top type/site/length share >= 0.80 or 0.65). Writes
// observed, iteration, and summary CSVs plus a JSON summary. Even a surviving
// signal is not semantic evidence, because class itself is unverified.
import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const sourcePath = path.join(reportsDir, 'lipi_scope_rows.csv');
const classCountsPath = path.join(reportsDir, 'lipi_class_field_counts.csv');
const outObserved = path.join(reportsDir, 'lipi_class_proxy_control_observed.csv');
const outIterations = path.join(reportsDir, 'lipi_class_proxy_control_iterations.csv');
const outSummary = path.join(reportsDir, 'lipi_class_proxy_control_summary.csv');
const outJson = path.join(reportsDir, 'lipi_class_proxy_control_summary.json');

const minLabelRows = 12;
const iterations = Number(process.env.IVC_CLASS_PROXY_ITERATIONS ?? 20);
const alpha = 1;
const seedBase = 20260525;

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

function csvObjects(text) {
  const rows = parseCsv(text);
  const headers = rows.shift() ?? [];
  return rows.map((row) => Object.fromEntries(headers.map((header, index) => [header, row[index] ?? ''])));
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

function parseTokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
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

function mulberry32(seed) {
  return function random() {
    let t = (seed += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function hashString(text) {
  let hash = 2166136261;
  for (let i = 0; i < text.length; i++) {
    hash ^= text.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}

function shuffle(values, rng) {
  const out = values.slice();
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
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
  return [...seen.values()].sort((a, b) => String(a.id).localeCompare(String(b.id)));
}

function majorityLabel(family, target) {
  const counts = new Map();
  for (const record of family.source_records ?? [family]) {
    const label = String(record[target] ?? '').trim();
    if (!label || label === '-' || label === 'None' || label === '??') continue;
    bump(counts, label);
  }
  if (!counts.size) return null;
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))[0][0];
}

function edgeFrame(tokens) {
  if (tokens.length === 1) return 'len1';
  return `${tokens.length}:${tokens[0]}:${tokens[tokens.length - 1]}`;
}

function subtractLabelCount(counts, label) {
  const out = new Map(counts);
  const next = (out.get(label) ?? 0) - 1;
  if (next <= 0) out.delete(label);
  else out.set(label, next);
  return out;
}

function bestLabel(counts, labels, fallbackCounts) {
  const source = counts && counts.size ? counts : fallbackCounts;
  let best = null;
  let bestValue = -Infinity;
  for (const label of labels) {
    const value = source.get(label) ?? 0;
    if (value > bestValue || (value === bestValue && (!best || label.localeCompare(best) < 0))) {
      best = label;
      bestValue = value;
    }
  }
  return best;
}

function addConfusion(confusion, actual, predicted) {
  if (!confusion.has(actual)) confusion.set(actual, { tp: 0, fp: 0, fn: 0 });
  if (!confusion.has(predicted)) confusion.set(predicted, { tp: 0, fp: 0, fn: 0 });
  if (actual === predicted) confusion.get(actual).tp++;
  else {
    confusion.get(actual).fn++;
    confusion.get(predicted).fp++;
  }
}

function macroStats(confusion, labels) {
  let f1Sum = 0;
  let recallSum = 0;
  for (const label of labels) {
    const row = confusion.get(label) ?? { tp: 0, fp: 0, fn: 0 };
    const precision = row.tp + row.fp ? row.tp / (row.tp + row.fp) : 0;
    const recall = row.tp + row.fn ? row.tp / (row.tp + row.fn) : 0;
    const f1 = precision + recall ? (2 * precision * recall) / (precision + recall) : 0;
    f1Sum += f1;
    recallSum += recall;
  }
  return {
    macro_f1: f1Sum / labels.length,
    macro_recall: recallSum / labels.length,
  };
}

function featureKey(row, feature) {
  if (feature === 'length') return String(row.tokens.length);
  if (feature === 'edge_frame') return edgeFrame(row.tokens);
  if (feature === 'type') return row.type ?? '';
  if (feature === 'site') return row.site ?? '';
  if (feature === 'type_site') return `${row.type ?? ''}|${row.site ?? ''}`;
  if (feature === 'length_type_site') return `${row.tokens.length}|${row.type ?? ''}|${row.site ?? ''}`;
  throw new Error(`Unknown feature ${feature}`);
}

function prepareRows(families, labelFilter) {
  const rows = families
    .map((family) => ({
      ...family,
      label: family.label,
    }))
    .filter((row) => row.label && labelFilter.allowedLabels.has(row.label));

  const counts = new Map();
  for (const row of rows) bump(counts, row.label);
  const eligible = new Set([...counts.entries()].filter(([, count]) => count >= minLabelRows).map(([label]) => label));
  return rows.filter((row) => eligible.has(row.label));
}

function evaluateRows(rows, model) {
  const labels = [...new Set(rows.map((row) => row.label))].sort((a, b) => a.localeCompare(b));
  if (labels.length < 2) return null;

  const globalLabelCounts = new Map();
  const featureCounts = new Map();
  const tokenByLabel = new Map();
  const labelTokenTotals = new Map();
  const vocabulary = new Set();

  for (const row of rows) {
    bump(globalLabelCounts, row.label);
    if (model !== 'majority' && model !== 'token_nb') {
      addNested(featureCounts, featureKey(row, model), row.label);
    }
    for (const token of row.tokens) {
      vocabulary.add(token);
      addNested(tokenByLabel, row.label, token);
      bump(labelTokenTotals, row.label);
    }
  }

  let correct = 0;
  const confusion = new Map();
  const vocabSize = vocabulary.size;

  for (const row of rows) {
    const fallback = subtractLabelCount(globalLabelCounts, row.label);
    let predicted = null;

    if (model === 'majority') {
      predicted = bestLabel(fallback, labels, globalLabelCounts);
    } else if (model === 'token_nb') {
      let best = null;
      let bestScore = -Infinity;
      for (const label of labels) {
        const labelCount = (globalLabelCounts.get(label) ?? 0) - (label === row.label ? 1 : 0);
        const prior = Math.log((labelCount + alpha) / (rows.length - 1 + alpha * labels.length));
        const tokenCounts = new Map(tokenByLabel.get(label) ?? []);
        let total = labelTokenTotals.get(label) ?? 0;
        if (label === row.label) {
          for (const token of row.tokens) {
            const next = (tokenCounts.get(token) ?? 0) - 1;
            if (next <= 0) tokenCounts.delete(token);
            else tokenCounts.set(token, next);
            total--;
          }
        }
        let score = prior;
        for (const token of row.tokens) {
          score += Math.log(((tokenCounts.get(token) ?? 0) + alpha) / (total + alpha * vocabSize));
        }
        if (score > bestScore || (score === bestScore && (!best || label.localeCompare(best) < 0))) {
          best = label;
          bestScore = score;
        }
      }
      predicted = best;
    } else {
      const key = featureKey(row, model);
      const counts = subtractLabelCount(featureCounts.get(key) ?? new Map(), row.label);
      predicted = bestLabel(counts, labels, fallback);
    }

    if (predicted === row.label) correct++;
    addConfusion(confusion, row.label, predicted);
  }

  const macro = macroStats(confusion, labels);
  return {
    evaluated_rows: rows.length,
    label_count: labels.length,
    labels: labels.join(';'),
    majority_label: bestLabel(globalLabelCounts, labels, globalLabelCounts),
    majority_share: Math.max(...globalLabelCounts.values()) / rows.length,
    accuracy: correct / rows.length,
    macro_f1: macro.macro_f1,
    macro_recall: macro.macro_recall,
  };
}

function blockKey(row, block) {
  if (block === 'global') return 'global';
  if (block === 'length') return String(row.tokens.length);
  if (block === 'type') return row.type ?? '';
  if (block === 'site') return row.site ?? '';
  if (block === 'type_site') return `${row.type ?? ''}|${row.site ?? ''}`;
  if (block === 'length_type_site') return `${row.tokens.length}|${row.type ?? ''}|${row.site ?? ''}`;
  throw new Error(`Unknown block ${block}`);
}

function shuffledRows(rows, block, seed) {
  const rng = mulberry32(seed);
  const groups = new Map();
  for (let i = 0; i < rows.length; i++) {
    const key = blockKey(rows[i], block);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(i);
  }
  const out = rows.map((row) => ({ ...row }));
  for (const [key, indexes] of groups.entries()) {
    const labels = indexes.map((index) => rows[index].label);
    const shuffled = shuffle(labels, mulberry32(seed ^ hashString(key)));
    for (let i = 0; i < indexes.length; i++) {
      out[indexes[i]].label = shuffled[i];
    }
  }
  return out;
}

function summarize(values) {
  const sorted = values.slice().sort((a, b) => a - b);
  const mean = values.reduce((sum, value) => sum + value, 0) / values.length;
  const q = (p) => {
    const index = (sorted.length - 1) * p;
    const lower = Math.floor(index);
    const upper = Math.ceil(index);
    if (lower === upper) return sorted[lower];
    return sorted[lower] + (sorted[upper] - sorted[lower]) * (index - lower);
  };
  return {
    mean,
    min: sorted[0],
    p05: q(0.05),
    median: q(0.5),
    p95: q(0.95),
    max: sorted[sorted.length - 1],
  };
}

const sourceRows = csvObjects(fs.readFileSync(sourcePath, 'utf8'));
const classCounts = csvObjects(fs.readFileSync(classCountsPath, 'utf8'));
const classPurity = new Map(
  classCounts.map((row) => [
    row.class,
    Math.max(Number(row.top_type_share || 0), Number(row.top_site_share || 0), Number(row.top_length_share || 0)),
  ]),
);

const numericClean = sourceRows
  .filter((row) => row.readiness_bucket === 'lipi_numeric_clean_candidate')
  .map((row) => ({
    ...row,
    tokens: parseTokens(row.text),
    direction: String(row['dir.'] ?? '').trim(),
  }))
  .filter((row) => row.tokens.length > 0);

const families = exactFamilies(numericClean).map((family) => ({
  ...family,
  label: majorityLabel(family, 'class'),
  type: majorityLabel(family, 'type'),
  site: majorityLabel(family, 'site'),
  region: majorityLabel(family, 'region'),
  material: majorityLabel(family, 'material'),
  complete: majorityLabel(family, 'complete'),
}));

const allLabels = new Set(
  [...families.reduce((counts, family) => {
    if (family.label) bump(counts, family.label);
    return counts;
  }, new Map()).entries()]
    .filter(([, count]) => count >= minLabelRows)
    .map(([label]) => label),
);

const labelFilters = [
  {
    name: 'all_eligible',
    description: 'All class labels with at least min_label_rows after exact-sequence collapse.',
    allowedLabels: allLabels,
  },
  {
    name: 'source_proxy_ge_0_80_removed',
    description: 'Remove class labels whose top type/site/length share in the source audit is at least 0.80.',
    allowedLabels: new Set([...allLabels].filter((label) => (classPurity.get(label) ?? 0) < 0.8)),
  },
  {
    name: 'source_proxy_ge_0_65_removed',
    description: 'Remove class labels whose top type/site/length share in the source audit is at least 0.65.',
    allowedLabels: new Set([...allLabels].filter((label) => (classPurity.get(label) ?? 0) < 0.65)),
  },
];

const models = ['majority', 'length', 'type', 'site', 'type_site', 'length_type_site', 'edge_frame', 'token_nb'];
const shuffleBlocks = ['global', 'length', 'type', 'site', 'type_site', 'length_type_site'];

const observedRows = [
  [
    'label_filter',
    'model',
    'evaluated_rows',
    'label_count',
    'labels',
    'majority_label',
    'majority_share',
    'accuracy',
    'macro_f1',
    'macro_recall',
    'removed_labels',
  ],
];
const iterationRows = [
  [
    'label_filter',
    'shuffle_block',
    'iteration',
    'model',
    'evaluated_rows',
    'label_count',
    'accuracy',
    'macro_f1',
    'macro_recall',
  ],
];
const summaryRows = [
  [
    'label_filter',
    'shuffle_block',
    'model',
    'observed_accuracy',
    'null_accuracy_mean',
    'null_accuracy_p95',
    'observed_minus_null_mean',
    'null_iterations_ge_observed_accuracy',
    'observed_macro_f1',
    'null_macro_f1_mean',
    'null_macro_f1_p95',
    'observed_minus_null_macro_f1_mean',
    'null_iterations_ge_observed_macro_f1',
  ],
];

const jsonSummary = {
  generated_at_local: new Date().toISOString(),
  source_file: 'data/open_prototype/reports/lipi_scope_rows.csv',
  source_scope: 'lipi_numeric_clean_candidate',
  source_rows: numericClean.length,
  exact_sequence_families: families.length,
  min_label_rows: minLabelRows,
  iterations,
  label_filters: [],
  shuffle_blocks: shuffleBlocks,
  models,
  observed: [],
  summaries: [],
  interpretation_boundary:
    'Class proxy-control scout only. lipi.class is an unverified source-code field, so surviving signal is not semantic evidence.',
  artifact_files: [
    'data/open_prototype/reports/lipi_class_proxy_control_observed.csv',
    'data/open_prototype/reports/lipi_class_proxy_control_iterations.csv',
    'data/open_prototype/reports/lipi_class_proxy_control_summary.csv',
    'data/open_prototype/reports/lipi_class_proxy_control_summary.json',
  ],
};

for (const labelFilter of labelFilters) {
  const rows = prepareRows(families, labelFilter);
  const labels = new Set(rows.map((row) => row.label));
  const removedLabels = [...allLabels].filter((label) => !labelFilter.allowedLabels.has(label)).sort();
  jsonSummary.label_filters.push({
    name: labelFilter.name,
    description: labelFilter.description,
    evaluated_rows: rows.length,
    labels: [...labels].sort(),
    removed_labels: removedLabels,
  });

  const observedByModel = new Map();
  for (const model of models) {
    const result = evaluateRows(rows, model);
    if (!result) continue;
    observedByModel.set(model, result);
    const row = [
      labelFilter.name,
      model,
      result.evaluated_rows,
      result.label_count,
      result.labels,
      result.majority_label,
      formatNumber(result.majority_share),
      formatNumber(result.accuracy),
      formatNumber(result.macro_f1),
      formatNumber(result.macro_recall),
      removedLabels.join(';'),
    ];
    observedRows.push(row);
    jsonSummary.observed.push(Object.fromEntries(observedRows[0].map((key, index) => [key, row[index]])));
  }

  for (const block of shuffleBlocks) {
    const perModel = new Map(models.map((model) => [model, { accuracy: [], macro_f1: [], macro_recall: [] }]));
    for (let iteration = 0; iteration < iterations; iteration++) {
      const shuffled = shuffledRows(rows, block, seedBase + iteration + hashString(`${labelFilter.name}:${block}`));
      for (const model of models) {
        const result = evaluateRows(shuffled, model);
        if (!result) continue;
        perModel.get(model).accuracy.push(result.accuracy);
        perModel.get(model).macro_f1.push(result.macro_f1);
        perModel.get(model).macro_recall.push(result.macro_recall);
        iterationRows.push([
          labelFilter.name,
          block,
          iteration,
          model,
          result.evaluated_rows,
          result.label_count,
          formatNumber(result.accuracy),
          formatNumber(result.macro_f1),
          formatNumber(result.macro_recall),
        ]);
      }
    }

    for (const model of models) {
      const observed = observedByModel.get(model);
      const values = perModel.get(model);
      if (!observed || !values.accuracy.length) continue;
      const acc = summarize(values.accuracy);
      const f1 = summarize(values.macro_f1);
      const row = [
        labelFilter.name,
        block,
        model,
        formatNumber(observed.accuracy),
        formatNumber(acc.mean),
        formatNumber(acc.p95),
        formatNumber(observed.accuracy - acc.mean),
        values.accuracy.filter((value) => value >= observed.accuracy).length,
        formatNumber(observed.macro_f1),
        formatNumber(f1.mean),
        formatNumber(f1.p95),
        formatNumber(observed.macro_f1 - f1.mean),
        values.macro_f1.filter((value) => value >= observed.macro_f1).length,
      ];
      summaryRows.push(row);
      jsonSummary.summaries.push(Object.fromEntries(summaryRows[0].map((key, index) => [key, row[index]])));
    }
  }
}

fs.writeFileSync(outObserved, toCsv(observedRows), 'utf8');
fs.writeFileSync(outIterations, toCsv(iterationRows), 'utf8');
fs.writeFileSync(outSummary, toCsv(summaryRows), 'utf8');
fs.writeFileSync(outJson, `${JSON.stringify(jsonSummary, null, 2)}\n`, 'utf8');

console.log(
  JSON.stringify(
    {
      source_rows: numericClean.length,
      exact_sequence_families: families.length,
      label_filters: jsonSummary.label_filters,
      token_nb_summaries: jsonSummary.summaries.filter((row) => row.model === 'token_nb'),
      wrote: jsonSummary.artifact_files,
    },
    null,
    2,
  ),
);
