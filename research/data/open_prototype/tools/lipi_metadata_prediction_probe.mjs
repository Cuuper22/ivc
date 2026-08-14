// Can the sign sequence on an object predict that object's metadata — its
// type, site, region, material, completeness, writing direction, or class?
// If real inscriptions predict metadata better than plausible fakes do, the
// sequences carry information tied to context, which is worth knowing even
// before anyone can read them.
//
// The script reads lipi_scope_rows.csv, keeps rows in the
// 'lipi_numeric_clean_candidate' readiness bucket, and collapses exact
// duplicate sequences into families (majority-voting their labels). For each
// metadata target with at least 40 labeled rows per class, it runs four
// leave-one-out classifiers of increasing strength: majority label, sequence
// length, first/last-sign "edge frame", and a token naive Bayes.
//
// It then builds four synthetic control corpora — position-sampled slots, a
// fake "administrative register" code, a fake "emblem formula" code, and a
// mixed admin/emblem code — each matched to the observed lengths and token
// pools, and scores the same classifiers on them (5 seeded iterations per
// control by default; override with IVC_METADATA_ITERATIONS). Comparing
// observed accuracy against these null distributions shows whether the real
// corpus beats sequences that merely look statistically similar.
//
// Outputs: lipi_metadata_prediction_iterations.csv (every run),
// lipi_metadata_prediction_summary.csv and .json (observed vs. null spread).
// Prediction here never assigns meanings, sign values, or translations.

import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const sourcePath = path.join(reportsDir, 'lipi_scope_rows.csv');
const outIterations = path.join(reportsDir, 'lipi_metadata_prediction_iterations.csv');
const outSummary = path.join(reportsDir, 'lipi_metadata_prediction_summary.csv');
const outJson = path.join(reportsDir, 'lipi_metadata_prediction_summary.json');

const iterations = Number(process.env.IVC_METADATA_ITERATIONS ?? 5);
const seedBase = 20260524;
const minLabelRows = 40;
const alpha = 1;

const targets = ['type', 'site', 'region', 'material', 'complete', 'direction', 'class'];

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

function mapTotal(map) {
  let total = 0;
  for (const value of map.values()) total += value;
  return total;
}

function median(values) {
  if (!values.length) return null;
  const sorted = values.slice().sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
}

function quantile(values, q) {
  if (!values.length) return null;
  const sorted = values.slice().sort((a, b) => a - b);
  const index = (sorted.length - 1) * q;
  const lower = Math.floor(index);
  const upper = Math.ceil(index);
  if (lower === upper) return sorted[lower];
  return sorted[lower] + (sorted[upper] - sorted[lower]) * (index - lower);
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

function topCountMap(counts, limit) {
  const out = new Map();
  for (const [token, count] of [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, limit)) {
    out.set(token, count);
  }
  return out.size ? out : counts;
}

function weightedChoice(counts, rng) {
  const entries = [...counts.entries()];
  const total = entries.reduce((sum, [, count]) => sum + count, 0);
  let target = rng() * total;
  for (const [token, count] of entries) {
    target -= count;
    if (target <= 0) return token;
  }
  return entries[entries.length - 1][0];
}

function dependencyChoice(seedKey, options, limit) {
  const entries = [...options.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, limit);
  return entries[hashString(seedKey) % entries.length][0];
}

function addKeyedCount(map, keys, token, by = 1) {
  addNested(map, keys.join('\t'), token, by);
}

function buildPools(records) {
  const global = new Map();
  const first = new Map();
  const last = new Map();
  const interior = new Map();
  const byPosition = new Map();
  const byLengthPosition = new Map();
  for (const record of records) {
    const len = record.tokens.length;
    for (let pos = 0; pos < len; pos++) {
      const token = record.tokens[pos];
      bump(global, token);
      addKeyedCount(byPosition, [pos], token);
      addKeyedCount(byLengthPosition, [len, pos], token);
      if (pos === 0) bump(first, token);
      if (pos === len - 1) bump(last, token);
      if (pos > 0 && pos < len - 1) bump(interior, token);
    }
  }
  return {
    global,
    first,
    last,
    interior: interior.size ? interior : global,
    byPosition,
    byLengthPosition,
    firstTop: topCountMap(first, 120),
    lastTop: topCountMap(last, 120),
    interiorTop: topCountMap(interior.size ? interior : global, 180),
    globalTop: topCountMap(global, 220),
  };
}

function sampleLengthPosition(pools, len, pos, rng) {
  return weightedChoice(
    pools.byLengthPosition.get(`${len}\t${pos}`) ?? pools.byPosition.get(String(pos)) ?? pools.global,
    rng,
  );
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
  const sorted = [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  return sorted[0][0];
}

function makeUniqueTemplate(tokens, usedKeys, pools, rng) {
  let candidate = tokens.slice();
  let key = candidate.join(' ');
  if (!usedKeys.has(key)) {
    usedKeys.add(key);
    return candidate;
  }
  for (let attempt = 0; attempt < 300; attempt++) {
    candidate = tokens.slice();
    const len = candidate.length;
    if (len === 0) return candidate;
    const mutablePos = len <= 2 ? attempt % len : 1 + (attempt % (len - 2));
    candidate[mutablePos] = sampleLengthPosition(pools, len, mutablePos, rng);
    key = candidate.join(' ');
    if (!usedKeys.has(key)) {
      usedKeys.add(key);
      return candidate;
    }
  }
  usedKeys.add(key);
  return candidate;
}

function makeGeneratedFamilies(families, control, iteration, templateFn, pools, rng) {
  const usedKeys = new Set();
  return families.map((family) => ({
    ...family,
    id: `${control}_${iteration}_${family.id}`,
    source_id: family.id,
    control,
    iteration,
    tokens: makeUniqueTemplate(templateFn(family), usedKeys, pools, rng),
  }));
}

function makeAdminTemplateFactory(pools, rng) {
  const officeChoices = new Map();
  const commodityChoices = new Map();
  const quantityChoices = new Map();
  const qualifierChoices = new Map();
  const terminalChoices = new Map();
  const getChoice = (map, key, options, limit, salt) => {
    if (!map.has(key)) map.set(key, dependencyChoice(`${salt}:${key}`, options, limit));
    return map.get(key);
  };
  return function adminTemplate(family) {
    const len = family.tokens.length;
    if (len <= 0) return [];
    const issuer = weightedChoice(pools.firstTop, rng);
    if (len === 1) return [issuer];
    const office = getChoice(officeChoices, issuer, pools.interiorTop, 60, 'office');
    const commodity = getChoice(commodityChoices, office, pools.interiorTop, 90, 'commodity');
    const quantity = getChoice(quantityChoices, commodity, pools.interiorTop, 70, 'quantity');
    const qualifier = getChoice(qualifierChoices, `${issuer}:${commodity}`, pools.globalTop, 120, 'qualifier');
    const terminal = getChoice(terminalChoices, `${issuer}:${quantity}`, pools.lastTop, 90, 'terminal');
    if (len === 2) return [issuer, terminal];
    if (len === 3) return [issuer, commodity, terminal];
    if (len === 4) return [issuer, commodity, quantity, terminal];
    const tokens = [issuer, office, commodity, quantity];
    while (tokens.length < len - 1) tokens.push(qualifier);
    tokens.push(terminal);
    return tokens.slice(0, len);
  };
}

function makeEmblemTemplateFactory(pools, rng) {
  const rankChoices = new Map();
  const deviceChoices = new Map();
  const variantChoices = new Map();
  const terminalChoices = new Map();
  const getChoice = (map, key, options, limit, salt) => {
    if (!map.has(key)) map.set(key, dependencyChoice(`${salt}:${key}`, options, limit));
    return map.get(key);
  };
  return function emblemTemplate(family) {
    const len = family.tokens.length;
    if (len <= 0) return [];
    const clan = weightedChoice(pools.firstTop, rng);
    if (len === 1) return [clan];
    const rank = getChoice(rankChoices, clan, pools.interiorTop, 80, 'rank');
    const device = getChoice(deviceChoices, `${clan}:${rank}`, pools.interiorTop, 100, 'device');
    const variant = getChoice(variantChoices, device, pools.globalTop, 120, 'variant');
    const terminal = getChoice(terminalChoices, `${clan}:${device}`, pools.lastTop, 100, 'terminal');
    if (len === 2) return [clan, terminal];
    if (len === 3) return [clan, device, terminal];
    if (len === 4) return [clan, rank, device, terminal];
    const tokens = [clan, rank, device];
    while (tokens.length < len - 1) tokens.push(variant);
    tokens.push(terminal);
    return tokens.slice(0, len);
  };
}

function makePositionTemplateFactory(pools, rng) {
  return function positionTemplate(family) {
    return family.tokens.map((_, pos) => sampleLengthPosition(pools, family.tokens.length, pos, rng));
  };
}

function makeMixedTemplateFactory(pools, rng) {
  const admin = makeAdminTemplateFactory(pools, rng);
  const emblem = makeEmblemTemplateFactory(pools, rng);
  const position = makePositionTemplateFactory(pools, rng);
  return function mixedTemplate(family) {
    const type = majorityLabel(family, 'type') ?? family.type ?? '';
    if (type.startsWith('TAB')) return admin(family);
    if (type.startsWith('SEAL')) return emblem(family);
    if (type.startsWith('POT') && family.tokens.length <= 3) return position(family);
    return rng() < 0.5 ? admin(family) : emblem(family);
  };
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
    if (value > bestValue || (value === bestValue && label.localeCompare(best) < 0)) {
      best = label;
      bestValue = value;
    }
  }
  return best;
}

function addConfusion(confusion, actual, predicted) {
  if (!confusion.has(actual)) confusion.set(actual, { tp: 0, fp: 0, fn: 0 });
  if (!confusion.has(predicted)) confusion.set(predicted, { tp: 0, fp: 0, fn: 0 });
  if (actual === predicted) {
    confusion.get(actual).tp++;
  } else {
    confusion.get(actual).fn++;
    confusion.get(predicted).fp++;
  }
}

function macroScores(confusion, labels) {
  const f1s = [];
  const recalls = [];
  for (const label of labels) {
    const row = confusion.get(label) ?? { tp: 0, fp: 0, fn: 0 };
    const precision = row.tp + row.fp > 0 ? row.tp / (row.tp + row.fp) : 0;
    const recall = row.tp + row.fn > 0 ? row.tp / (row.tp + row.fn) : 0;
    const f1 = precision + recall > 0 ? (2 * precision * recall) / (precision + recall) : 0;
    f1s.push(f1);
    recalls.push(recall);
  }
  return {
    macro_f1: f1s.length ? formatNumber(f1s.reduce((sum, value) => sum + value, 0) / f1s.length) : null,
    macro_recall: recalls.length ? formatNumber(recalls.reduce((sum, value) => sum + value, 0) / recalls.length) : null,
  };
}

function prepareTargetRows(families, target) {
  const labeled = families
    .map((family) => ({ ...family, label: majorityLabel(family, target) }))
    .filter((family) => family.label);
  const labelCounts = new Map();
  for (const row of labeled) bump(labelCounts, row.label);
  const eligible = new Set([...labelCounts.entries()].filter(([, count]) => count >= minLabelRows).map(([label]) => label));
  return labeled.filter((row) => eligible.has(row.label));
}

function evaluateTarget(control, iteration, target, families) {
  const rows = prepareTargetRows(families, target);
  const labels = [...new Set(rows.map((row) => row.label))].sort((a, b) => a.localeCompare(b));
  if (labels.length < 2) return [];

  const globalLabelCounts = new Map();
  const lengthCounts = new Map();
  const edgeCounts = new Map();
  const tokenByLabel = new Map();
  const tokenTotalsByLabel = new Map();
  const vocab = new Set();

  for (const row of rows) {
    bump(globalLabelCounts, row.label);
    addNested(lengthCounts, String(row.tokens.length), row.label);
    const edgeKey = row.tokens.length <= 1 ? `single:${row.tokens[0] ?? ''}` : `${row.tokens.length}:${row.tokens[0]}:${row.tokens[row.tokens.length - 1]}`;
    addNested(edgeCounts, edgeKey, row.label);
    if (!tokenByLabel.has(row.label)) tokenByLabel.set(row.label, new Map());
    for (const token of row.tokens) {
      vocab.add(token);
      bump(tokenByLabel.get(row.label), token);
      bump(tokenTotalsByLabel, row.label);
    }
  }

  const models = {
    majority: { correct: 0, confusion: new Map() },
    length: { correct: 0, confusion: new Map() },
    edge_frame: { correct: 0, confusion: new Map() },
    token_nb: { correct: 0, confusion: new Map() },
  };

  for (const row of rows) {
    const trainLabelCounts = subtractLabelCount(globalLabelCounts, row.label);
    const lengthKey = String(row.tokens.length);
    const trainLengthCounts = subtractLabelCount(lengthCounts.get(lengthKey) ?? new Map(), row.label);
    const edgeKey = row.tokens.length <= 1 ? `single:${row.tokens[0] ?? ''}` : `${row.tokens.length}:${row.tokens[0]}:${row.tokens[row.tokens.length - 1]}`;
    const trainEdgeCounts = subtractLabelCount(edgeCounts.get(edgeKey) ?? new Map(), row.label);
    const predictions = {
      majority: bestLabel(trainLabelCounts, labels, globalLabelCounts),
      length: bestLabel(trainLengthCounts, labels, trainLabelCounts),
      edge_frame: bestLabel(trainEdgeCounts, labels, trainLengthCounts.size ? trainLengthCounts : trainLabelCounts),
      token_nb: null,
    };

    let bestNb = null;
    let bestScore = -Infinity;
    const vocabSize = Math.max(1, vocab.size);
    for (const label of labels) {
      const prior = ((trainLabelCounts.get(label) ?? 0) + alpha) / (Math.max(1, rows.length - 1) + alpha * labels.length);
      let score = Math.log(prior);
      const labelTokenCounts = new Map(tokenByLabel.get(label) ?? new Map());
      let labelTokenTotal = tokenTotalsByLabel.get(label) ?? 0;
      if (label === row.label) {
        for (const token of row.tokens) {
          const next = (labelTokenCounts.get(token) ?? 0) - 1;
          if (next <= 0) labelTokenCounts.delete(token);
          else labelTokenCounts.set(token, next);
          labelTokenTotal--;
        }
      }
      for (const token of row.tokens) {
        score += Math.log(((labelTokenCounts.get(token) ?? 0) + alpha) / (labelTokenTotal + alpha * vocabSize));
      }
      if (score > bestScore || (score === bestScore && label.localeCompare(bestNb) < 0)) {
        bestNb = label;
        bestScore = score;
      }
    }
    predictions.token_nb = bestNb;

    for (const [model, predicted] of Object.entries(predictions)) {
      if (predicted === row.label) models[model].correct++;
      addConfusion(models[model].confusion, row.label, predicted);
    }
  }

  const majorityLabelName = [...globalLabelCounts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))[0][0];
  return Object.entries(models).map(([model, result]) => {
    const macros = macroScores(result.confusion, labels);
    return {
      control,
      iteration,
      target,
      model,
      evaluated_rows: rows.length,
      label_count: labels.length,
      labels: labels.join(';'),
      majority_label: majorityLabelName,
      majority_share: formatNumber((globalLabelCounts.get(majorityLabelName) ?? 0) / rows.length),
      accuracy: formatNumber(result.correct / rows.length),
      macro_f1: macros.macro_f1,
      macro_recall: macros.macro_recall,
    };
  });
}

function summarize(control, target, model, values, observed) {
  const mean = values.reduce((sum, value) => sum + value, 0) / values.length;
  const variance = values.reduce((sum, value) => sum + (value - mean) ** 2, 0) / values.length;
  return {
    control,
    target,
    model,
    iterations: values.length,
    observed_value: observed,
    null_mean: formatNumber(mean),
    null_sd: formatNumber(Math.sqrt(variance)),
    null_min: formatNumber(Math.min(...values)),
    null_p05: formatNumber(quantile(values, 0.05)),
    null_median: formatNumber(median(values)),
    null_p95: formatNumber(quantile(values, 0.95)),
    null_max: formatNumber(Math.max(...values)),
    observed_minus_null_mean: formatNumber(observed - mean),
    null_ge_observed_share: formatNumber(values.filter((value) => value >= observed).length / values.length),
  };
}

function formatLocalIso(date) {
  const offsetMinutes = -date.getTimezoneOffset();
  const sign = offsetMinutes >= 0 ? '+' : '-';
  const absMinutes = Math.abs(offsetMinutes);
  const pad = (value) => String(value).padStart(2, '0');
  const offset = `${sign}${pad(Math.floor(absMinutes / 60))}:${pad(absMinutes % 60)}`;
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(
    date.getHours(),
  )}:${pad(date.getMinutes())}:${pad(date.getSeconds())}${offset}`;
}

const rows = parseCsv(fs.readFileSync(sourcePath, 'utf8'));
const header = rows[0];
const column = Object.fromEntries(header.map((name, index) => [name, index]));
const records = rows.slice(1).map((row) => ({
  id: row[column.id],
  cisi: row[column.cisi],
  region: row[column.region],
  site: row[column.site],
  type: row[column.type],
  material: row[column.material],
  complete: row[column.complete],
  direction: row[column.direction],
  class: row[column.class],
  readiness: row[column.readiness_bucket],
  tokens: parseTokens(row[column.text]),
}));

const numericClean = records.filter((record) => record.readiness === 'lipi_numeric_clean_candidate');
const observedFamilies = exactFamilies(numericClean);
const pools = buildPools(numericClean);

const controls = [
  {
    name: 'duplicate_matched_position_slots',
    description:
      'Family-level duplicate-matched position slots; samples tokens independently from observed length-position pools.',
    makeFactory: makePositionTemplateFactory,
  },
  {
    name: 'administrative_register_code',
    description:
      'Family-level administrative slot code with issuer, office, commodity, quantity, qualifier, and terminal dependencies.',
    makeFactory: makeAdminTemplateFactory,
  },
  {
    name: 'emblem_formula_code',
    description:
      'Family-level emblem formula code with clan, rank, device, variant, and terminal dependencies.',
    makeFactory: makeEmblemTemplateFactory,
  },
  {
    name: 'mixed_admin_emblem_code',
    description:
      'Family-level mixed code: tablet-like rows use administrative dependencies, seal-like rows use emblem dependencies, and short pottery rows use positional slots.',
    makeFactory: makeMixedTemplateFactory,
  },
];

const iterationRows = [];
for (const target of targets) {
  iterationRows.push(...evaluateTarget('observed_lipi_exact_families', 'observed', target, observedFamilies));
}

for (const control of controls) {
  for (let iteration = 1; iteration <= iterations; iteration++) {
    const rng = mulberry32(seedBase + iteration * 1009 + control.name.length * 65537);
    const templateFactory = control.makeFactory(pools, rng);
    const generatedFamilies = makeGeneratedFamilies(observedFamilies, control.name, iteration, templateFactory, pools, rng);
    for (const target of targets) {
      iterationRows.push(...evaluateTarget(control.name, iteration, target, generatedFamilies));
    }
  }
}

const summaryRows = [];
const observedLookup = new Map(
  iterationRows
    .filter((row) => row.control === 'observed_lipi_exact_families')
    .map((row) => [`${row.target}\t${row.model}`, row]),
);

for (const control of controls) {
  for (const target of targets) {
    for (const model of ['majority', 'length', 'edge_frame', 'token_nb']) {
      const observed = observedLookup.get(`${target}\t${model}`);
      const nullRows = iterationRows.filter((row) => row.control === control.name && row.target === target && row.model === model);
      if (!observed || !nullRows.length) continue;
      summaryRows.push(summarize(control.name, target, model, nullRows.map((row) => Number(row.accuracy)), Number(observed.accuracy)));
    }
  }
}

const iterationHeader = [
  'control',
  'iteration',
  'target',
  'model',
  'evaluated_rows',
  'label_count',
  'labels',
  'majority_label',
  'majority_share',
  'accuracy',
  'macro_f1',
  'macro_recall',
];

fs.writeFileSync(
  outIterations,
  toCsv([iterationHeader, ...iterationRows.map((row) => iterationHeader.map((key) => row[key]))]),
  'utf8',
);

const summaryHeader = [
  'control',
  'target',
  'model',
  'iterations',
  'observed_value',
  'null_mean',
  'null_sd',
  'null_min',
  'null_p05',
  'null_median',
  'null_p95',
  'null_max',
  'observed_minus_null_mean',
  'null_ge_observed_share',
];

fs.writeFileSync(
  outSummary,
  toCsv([summaryHeader, ...summaryRows.map((row) => summaryHeader.map((key) => row[key]))]),
  'utf8',
);

const summary = {
  generated_at_local: formatLocalIso(new Date()),
  source_file: 'data/open_prototype/reports/lipi_scope_rows.csv',
  source_scope: 'lipi_numeric_clean_candidate',
  source_rows: numericClean.length,
  exact_sequence_families: observedFamilies.length,
  min_label_rows: minLabelRows,
  targets,
  models: [
    'majority',
    'length',
    'edge_frame',
    'token_nb',
  ],
  iterations_per_control: iterations,
  controls: controls.map(({ name, description }) => ({ name, description })),
  observed_rows: iterationRows.filter((row) => row.control === 'observed_lipi_exact_families'),
  null_summary: summaryRows,
  artifact_files: [
    'data/open_prototype/reports/lipi_metadata_prediction_iterations.csv',
    'data/open_prototype/reports/lipi_metadata_prediction_summary.csv',
    'data/open_prototype/reports/lipi_metadata_prediction_summary.json',
  ],
  interpretation_boundary:
    'Metadata-prediction scout only. Metadata labels come from the filtered T3 planning layer and do not create meanings, sign values, language identity, or translations.',
};

fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(
  JSON.stringify(
    {
      observed_token_nb: summary.observed_rows.filter((row) => row.model === 'token_nb'),
      summary_rows: summaryRows.length,
      iteration_rows: iterationRows.length,
      selected_token_nb_summary: summaryRows.filter((row) => row.model === 'token_nb' && ['type', 'site', 'region'].includes(row.target)),
      wrote: summary.artifact_files,
    },
    null,
    2,
  ),
);
