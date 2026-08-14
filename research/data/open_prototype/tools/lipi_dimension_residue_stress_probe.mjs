// Do the signs of an inscription carry information about the physical size of
// the object they sit on, beyond what the object's type, site, material, and
// shape already explain? If bigger seals systematically carry different signs
// even after those proxies are held fixed, that residue would be worth
// chasing. This script measures it. From the filtered metadata it builds
// clean numeric rows, collapses exact duplicate sequences into families, and
// bins each object's catalog measurements into targets: horizontal, vertical,
// and thickness bins (mm), plus area and aspect-ratio bins. It also assigns
// every sign a provisional positional class (initial/medial/terminal/single/
// edge-mixed/distributed, from where the sign sits in rows) to define an
// edge-class frame feature. Leave-one-out models from majority vote up to
// token naive Bayes predict each bin, and each observed score is compared to
// label shuffles blocked ever more tightly — up to permuting labels only
// within groups matched on length, type, site, material, shape, direction,
// and edge-class frame. Iterations default to 10 (override with the
// environment variable IVC_DIMENSION_RESIDUE_ITERATIONS). Writes sign-class,
// observed, iteration, and summary CSVs plus a JSON summary. Catalog-
// measurement scout only; no metrological or semantic reading follows.
import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const sourcePath = path.join(base, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const outSignClasses = path.join(reportsDir, 'lipi_dimension_residue_sign_classes.csv');
const outObserved = path.join(reportsDir, 'lipi_dimension_residue_observed.csv');
const outIterations = path.join(reportsDir, 'lipi_dimension_residue_iterations.csv');
const outSummary = path.join(reportsDir, 'lipi_dimension_residue_summary.csv');
const outJson = path.join(reportsDir, 'lipi_dimension_residue_summary.json');

const targets = ['horizontal_bin', 'vertical_bin', 'thickness_bin', 'area_bin', 'aspect_bin'];
const minLabelFamilies = 30;
const minSignTokens = 20;
const iterations = Number(process.env.IVC_DIMENSION_RESIDUE_ITERATIONS ?? 10);
const alpha = 1;
const seedBase = 20260527;

const modelDefinitions = [
  { name: 'majority', fields: [] },
  { name: 'length_type_site', fields: ['length', 'type', 'site'] },
  { name: 'material_shape', fields: ['material', 'shape'] },
  { name: 'edge_frame', fields: ['edge_frame'] },
  { name: 'edge_class_frame', fields: ['edge_class_frame'] },
  { name: 'hard_proxy', fields: ['length', 'type', 'site', 'material', 'shape', 'direction'] },
  {
    name: 'hard_proxy_edge_class',
    fields: ['length', 'type', 'site', 'material', 'shape', 'direction', 'edge_class_frame'],
  },
  { name: 'token_nb', fields: ['tokens'] },
];

const blockDefinitions = [
  { name: 'global', fields: [] },
  { name: 'edge_frame', fields: ['edge_frame'] },
  { name: 'edge_class_frame', fields: ['edge_class_frame'] },
  { name: 'hard_proxy', fields: ['length', 'type', 'site', 'material', 'shape', 'direction'] },
  {
    name: 'hard_proxy_edge_class',
    fields: ['length', 'type', 'site', 'material', 'shape', 'direction', 'edge_class_frame'],
  },
];

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

function majorityFromValues(values) {
  const counts = new Map();
  for (const value of values) {
    if (value !== null && value !== undefined) bump(counts, value);
  }
  if (!counts.size) return null;
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))[0][0];
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

function familyValue(family, field) {
  return majorityFromValues(family.source_records.map((record) => record[field]));
}

function classifySign(profile) {
  if (profile.token_count < minSignTokens) return 'sparse';
  const initialShare = profile.initial_count / profile.token_count;
  const terminalShare = profile.terminal_count / profile.token_count;
  const medialShare = profile.medial_count / profile.token_count;
  const singleShare = profile.single_count / profile.token_count;
  const edgeShare = initialShare + terminalShare + singleShare;
  if (singleShare >= 0.6) return 'single';
  if (initialShare >= 0.6 && terminalShare < 0.2) return 'initial';
  if (terminalShare >= 0.6 && initialShare < 0.2) return 'terminal';
  if (medialShare >= 0.7) return 'medial';
  if (edgeShare >= 0.7) return 'edge_mixed';
  return 'distributed';
}

function buildSignClasses(families) {
  const profiles = new Map();
  for (const family of families) {
    const len = family.tokens.length;
    for (let pos = 0; pos < len; pos++) {
      const token = family.tokens[pos];
      if (!profiles.has(token)) {
        profiles.set(token, {
          sign: token,
          token_count: 0,
          family_count: 0,
          initial_count: 0,
          medial_count: 0,
          terminal_count: 0,
          single_count: 0,
          family_ids: new Set(),
        });
      }
      const profile = profiles.get(token);
      profile.token_count++;
      profile.family_ids.add(family.id);
      if (len === 1) profile.single_count++;
      else if (pos === 0) profile.initial_count++;
      else if (pos === len - 1) profile.terminal_count++;
      else profile.medial_count++;
    }
  }

  const out = new Map();
  for (const profile of profiles.values()) {
    profile.family_count = profile.family_ids.size;
    profile.provisional_class = classifySign(profile);
    out.set(profile.sign, profile);
  }
  return out;
}

function signClass(token, signProfiles) {
  return signProfiles.get(token)?.provisional_class ?? 'sparse';
}

function edgeFrame(tokens) {
  if (tokens.length === 1) return 'len1';
  return `${tokens.length}:${tokens[0]}:${tokens[tokens.length - 1]}`;
}

function edgeClassFrame(tokens, signProfiles) {
  if (tokens.length === 1) return `len1:${signClass(tokens[0], signProfiles)}`;
  return `${tokens.length}:${signClass(tokens[0], signProfiles)}:${signClass(tokens.at(-1), signProfiles)}`;
}

function proxyValue(row, field) {
  if (field === 'length') return String(row.tokens.length);
  if (field === 'edge_frame') return edgeFrame(row.tokens);
  if (field === 'edge_class_frame') return row.edge_class_frame;
  if (field === 'tokens') return row.tokens.join(' ');
  const value = row[field];
  return value === null || value === undefined || value === '' ? '-' : String(value);
}

function keyForFields(row, fields) {
  if (!fields.length) return 'global';
  return fields.map((field) => proxyValue(row, field)).join('|');
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

function prepareTargetRows(families, target) {
  const rows = [];
  const counts = new Map();
  for (const family of families) {
    const label = familyValue(family, target);
    if (!label) continue;
    rows.push({ ...family, label });
    bump(counts, label);
  }
  const eligible = new Set([...counts.entries()].filter(([, count]) => count >= minLabelFamilies).map(([label]) => label));
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
    if (model.name !== 'majority' && model.name !== 'token_nb') {
      addNested(featureCounts, keyForFields(row, model.fields), row.label);
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

    if (model.name === 'majority') {
      predicted = bestLabel(fallback, labels, globalLabelCounts);
    } else if (model.name === 'token_nb') {
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
      const key = keyForFields(row, model.fields);
      const counts = new Map(featureCounts.get(key) ?? []);
      const next = (counts.get(row.label) ?? 0) - 1;
      if (next <= 0) counts.delete(row.label);
      else counts.set(row.label, next);
      predicted = bestLabel(counts, labels, fallback);
    }

    if (predicted === row.label) correct++;
    addConfusion(confusion, row.label, predicted);
  }

  const macro = macroStats(confusion, labels);
  return {
    rows: rows.length,
    labels: labels.length,
    accuracy: correct / rows.length,
    macro_f1: macro.macro_f1,
    macro_recall: macro.macro_recall,
  };
}

function shuffledRows(rows, block, iteration, target) {
  const rng = mulberry32(seedBase + hashString(`${target}|${block.name}|${iteration}`));
  const groups = new Map();
  for (const row of rows) {
    const key = keyForFields(row, block.fields);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(row);
  }

  const shuffledById = new Map();
  let unchanged = 0;
  let shuffledBlockCount = 0;
  for (const groupRows of groups.values()) {
    const labels = groupRows.map((row) => row.label);
    const nextLabels = shuffle(labels, rng);
    if (groupRows.length > 1) shuffledBlockCount++;
    groupRows.forEach((row, index) => {
      const nextLabel = nextLabels[index];
      if (nextLabel === row.label) unchanged++;
      shuffledById.set(row.id, nextLabel);
    });
  }

  return {
    rows: rows.map((row) => ({ ...row, label: shuffledById.get(row.id) })),
    block_count: groups.size,
    shuffled_block_count: shuffledBlockCount,
    unchanged_label_share: unchanged / rows.length,
  };
}

function mean(values) {
  return values.length ? values.reduce((sum, value) => sum + value, 0) / values.length : null;
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

const rawRows = parseCsv(fs.readFileSync(sourcePath, 'utf8'));
const header = rawRows[0];
const column = Object.fromEntries(header.map((name, index) => [name, index]));

const records = rawRows.slice(1).map((row) => {
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
    site: valueOrNull(row[column.site]),
    material: valueOrNull(row[column.material]),
    shape: valueOrNull(row[column.shape]),
    type: valueOrNull(row[column.type]),
    direction,
    horizontal_bin: binHorizontal(horizontal),
    vertical_bin: binVertical(vertical),
    thickness_bin: binThickness(thickness),
    area_bin: binArea(horizontal, vertical),
    aspect_bin: binAspect(horizontal, vertical),
  };
});

const cleanRecords = records.filter((record) => record.numeric_clean);
const families = exactFamilies(cleanRecords);
const signProfiles = buildSignClasses(families);
for (const family of families) {
  family.edge_class_frame = edgeClassFrame(family.tokens, signProfiles);
}

const signClassRows = [
  [
    'sign',
    'token_count',
    'family_count',
    'provisional_class',
    'initial_count',
    'medial_count',
    'terminal_count',
    'single_count',
    'initial_share',
    'medial_share',
    'terminal_share',
    'single_share',
  ],
  ...[...signProfiles.values()]
    .sort((a, b) => b.token_count - a.token_count || a.sign.localeCompare(b.sign))
    .map((profile) => [
      profile.sign,
      profile.token_count,
      profile.family_count,
      profile.provisional_class,
      profile.initial_count,
      profile.medial_count,
      profile.terminal_count,
      profile.single_count,
      formatNumber(profile.initial_count / profile.token_count),
      formatNumber(profile.medial_count / profile.token_count),
      formatNumber(profile.terminal_count / profile.token_count),
      formatNumber(profile.single_count / profile.token_count),
    ]),
];

const observedRows = [
  ['target', 'model', 'rows', 'labels', 'accuracy', 'macro_f1', 'macro_recall'],
];
const iterationRows = [
  [
    'target',
    'shuffle_block',
    'shuffle_fields',
    'iteration',
    'model',
    'rows',
    'labels',
    'accuracy',
    'macro_f1',
    'macro_recall',
    'block_count',
    'shuffled_block_count',
    'unchanged_label_share',
  ],
];
const summaryRows = [
  [
    'target',
    'shuffle_block',
    'shuffle_fields',
    'model',
    'rows',
    'labels',
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
    'unchanged_label_share_mean',
  ],
];

const observedByKey = new Map();
const iterationObjects = [];

for (const target of targets) {
  const rows = prepareTargetRows(families, target);
  if (rows.length < 2) continue;

  for (const model of modelDefinitions) {
    const result = evaluateRows(rows, model);
    if (!result) continue;
    observedByKey.set(`${target}|${model.name}`, result);
    observedRows.push([
      target,
      model.name,
      result.rows,
      result.labels,
      formatNumber(result.accuracy),
      formatNumber(result.macro_f1),
      formatNumber(result.macro_recall),
    ]);
  }

  for (const block of blockDefinitions) {
    for (let iteration = 0; iteration < iterations; iteration++) {
      const shuffled = shuffledRows(rows, block, iteration, target);
      for (const model of modelDefinitions) {
        const result = evaluateRows(shuffled.rows, model);
        if (!result) continue;
        const object = {
          target,
          shuffle_block: block.name,
          shuffle_fields: block.fields.join(';') || 'none',
          iteration,
          model: model.name,
          ...result,
          block_count: shuffled.block_count,
          shuffled_block_count: shuffled.shuffled_block_count,
          unchanged_label_share: shuffled.unchanged_label_share,
        };
        iterationObjects.push(object);
        iterationRows.push([
          object.target,
          object.shuffle_block,
          object.shuffle_fields,
          object.iteration,
          object.model,
          object.rows,
          object.labels,
          formatNumber(object.accuracy),
          formatNumber(object.macro_f1),
          formatNumber(object.macro_recall),
          object.block_count,
          object.shuffled_block_count,
          formatNumber(object.unchanged_label_share),
        ]);
      }
    }
  }
}

const grouped = new Map();
for (const row of iterationObjects) {
  const key = `${row.target}|${row.shuffle_block}|${row.model}`;
  if (!grouped.has(key)) grouped.set(key, []);
  grouped.get(key).push(row);
}

for (const [key, rows] of grouped.entries()) {
  const [target, shuffleBlock, model] = key.split('|');
  const observed = observedByKey.get(`${target}|${model}`);
  if (!observed) continue;
  const accuracies = rows.map((row) => row.accuracy);
  const macroF1s = rows.map((row) => row.macro_f1);
  const unchangedShares = rows.map((row) => row.unchanged_label_share);
  const nullAccuracyMean = mean(accuracies);
  const nullMacroF1Mean = mean(macroF1s);
  summaryRows.push([
    target,
    shuffleBlock,
    rows[0].shuffle_fields,
    model,
    observed.rows,
    observed.labels,
    formatNumber(observed.accuracy),
    formatNumber(nullAccuracyMean),
    formatNumber(quantile(accuracies, 0.95)),
    formatNumber(observed.accuracy - nullAccuracyMean),
    accuracies.filter((value) => value >= observed.accuracy).length,
    formatNumber(observed.macro_f1),
    formatNumber(nullMacroF1Mean),
    formatNumber(quantile(macroF1s, 0.95)),
    formatNumber(observed.macro_f1 - nullMacroF1Mean),
    macroF1s.filter((value) => value >= observed.macro_f1).length,
    formatNumber(mean(unchangedShares)),
  ]);
}

const targetSummaries = [];
for (const target of targets) {
  const observed = observedByKey.get(`${target}|token_nb`);
  if (!observed) continue;
  const tokenGroups = [...grouped.entries()]
    .filter(([key]) => key.startsWith(`${target}|`) && key.endsWith('|token_nb'))
    .map(([key, rows]) => {
      const [, block] = key.split('|');
      const accMean = mean(rows.map((row) => row.accuracy));
      const f1Mean = mean(rows.map((row) => row.macro_f1));
      return {
        block,
        fields: rows[0].shuffle_fields,
        null_accuracy_mean: formatNumber(accMean),
        observed_minus_null_accuracy_mean: formatNumber(observed.accuracy - accMean),
        null_macro_f1_mean: formatNumber(f1Mean),
        observed_minus_null_macro_f1_mean: formatNumber(observed.macro_f1 - f1Mean),
        unchanged_label_share_mean: formatNumber(mean(rows.map((row) => row.unchanged_label_share))),
      };
    })
    .sort((a, b) => Number(a.observed_minus_null_accuracy_mean) - Number(b.observed_minus_null_accuracy_mean));
  targetSummaries.push({
    target,
    rows: observed.rows,
    labels: observed.labels,
    observed_token_nb_accuracy: formatNumber(observed.accuracy),
    observed_token_nb_macro_f1: formatNumber(observed.macro_f1),
    hardest_token_nb_null: tokenGroups[0],
  });
}

fs.mkdirSync(reportsDir, { recursive: true });
fs.writeFileSync(outSignClasses, toCsv(signClassRows));
fs.writeFileSync(outObserved, toCsv(observedRows));
fs.writeFileSync(outIterations, toCsv(iterationRows));
fs.writeFileSync(outSummary, toCsv(summaryRows));
fs.writeFileSync(
  outJson,
  `${JSON.stringify(
    {
      source: 'filtered lipi metadata, claim columns removed',
      source_rows: records.length,
      numeric_clean_source_rows: cleanRecords.length,
      exact_sequence_families: families.length,
      min_label_families: minLabelFamilies,
      min_sign_tokens: minSignTokens,
      iterations_per_block: iterations,
      targets,
      sign_class_counts: [...signProfiles.values()].reduce((acc, profile) => {
        acc[profile.provisional_class] = (acc[profile.provisional_class] ?? 0) + 1;
        return acc;
      }, {}),
      target_summaries: targetSummaries,
      outputs: [
        path.relative(base, outSignClasses).replaceAll('\\', '/'),
        path.relative(base, outObserved).replaceAll('\\', '/'),
        path.relative(base, outIterations).replaceAll('\\', '/'),
        path.relative(base, outSummary).replaceAll('\\', '/'),
      ],
      interpretation_boundary:
        'Dimension-residue stress scout only; dimension bins are catalog measurements from a T3 planning source and do not create metrological readings, sign meanings, semantic slots, phonetic values, language identity, or translations.',
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
      min_sign_tokens: minSignTokens,
      iterations_per_block: iterations,
      sign_class_counts: [...signProfiles.values()].reduce((acc, profile) => {
        acc[profile.provisional_class] = (acc[profile.provisional_class] ?? 0) + 1;
        return acc;
      }, {}),
      target_summaries: targetSummaries,
      wrote: [
        path.relative(base, outSignClasses).replaceAll('\\', '/'),
        path.relative(base, outObserved).replaceAll('\\', '/'),
        path.relative(base, outIterations).replaceAll('\\', '/'),
        path.relative(base, outSummary).replaceAll('\\', '/'),
        path.relative(base, outJson).replaceAll('\\', '/'),
      ],
    },
    null,
    2,
  ),
);
