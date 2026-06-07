import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const inputCsv = path.join(reportsDir, 'lipi_multiside_mark_rows.csv');
const outRowsCsv = path.join(reportsDir, 'lipi_short_mark_companion_context_rows.csv');
const outFamiliesCsv = path.join(reportsDir, 'lipi_short_mark_companion_context_families.csv');
const outTestsCsv = path.join(reportsDir, 'lipi_short_mark_companion_context_tests.csv');
const outJson = path.join(reportsDir, 'lipi_short_mark_companion_context_summary.json');

const targetTypes = new Set(['TAB:B', 'TAB:I']);
const coreCompanions = ['032', '033', '034'];
const focusLongTokens = ['400', '740', '176', '240', '031', '001', '140', '368', '900', '002', '861', '416'];
const permutationIterations = 5000;
const seed = 20260524;

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
  const header = rows.shift() ?? [];
  return rows.map((row) => Object.fromEntries(header.map((name, index) => [name, row[index] ?? ''])));
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

function parseBool(value) {
  return String(value).toLowerCase() === 'true';
}

function numeric(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function naturalCisiKey(cisi) {
  const match = String(cisi ?? '').match(/^([A-Za-z?]+)-(\d+)$/);
  return match ? `${match[1].padEnd(8, ' ')}${String(Number(match[2])).padStart(8, '0')}` : String(cisi ?? '');
}

function sortRows(rows) {
  return rows.slice().sort((a, b) => {
    const cisiCmp = naturalCisiKey(a.cisi).localeCompare(naturalCisiKey(b.cisi));
    if (cisiCmp) return cisiCmp;
    return Number(a.side_index || 0) - Number(b.side_index || 0);
  });
}

function orientation(tokens) {
  if (tokens.length !== 2 || !tokens.includes('700')) return null;
  const companion = tokens[0] === '700' ? tokens[1] : tokens[0];
  if (!coreCompanions.includes(companion)) return null;
  return {
    companion,
    order: tokens[0] === '700' ? '700_first' : '700_last',
    unordered_pair: ['700', companion].sort().join('-'),
  };
}

function sideRelation(shortSideIndex, longerRows) {
  if (!longerRows.length) return 'no_longer_text';
  const shortSide = numeric(shortSideIndex);
  const longSides = longerRows.map((row) => numeric(row.side_index)).filter((value) => value !== null);
  if (shortSide === null || longSides.length !== longerRows.length) return 'longer_text_side_unknown';
  if (longSides.every((side) => shortSide > side)) return 'short_after_all_longer';
  if (longSides.every((side) => shortSide < side)) return 'short_before_all_longer';
  if (longSides.includes(shortSide)) return 'same_catalog_side_as_longer';
  return 'short_between_longer_sides';
}

function contextClass(longerRows, allRows) {
  if (!longerRows.length) {
    const shortRows = allRows.filter((row) => parseBool(row.short_mark_candidate)).length;
    return shortRows > 1 ? 'all_short_or_no_longer_text' : 'single_short_no_longer_text';
  }
  if (longerRows.length === 1) return 'single_longer_text';
  return 'multiple_longer_texts';
}

function countBy(rows, keyFn) {
  const counts = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return counts;
}

function objectFromCounts(counts) {
  return Object.fromEntries([...counts.entries()].sort((a, b) => a[0].localeCompare(b[0], undefined, { numeric: true })));
}

function topCounts(counts, limit = 12) {
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], undefined, { numeric: true }))
    .slice(0, limit)
    .map(([key, value]) => `${key}:${value}`);
}

function formatNumber(value) {
  return value === null || value === undefined || Number.isNaN(value) ? '' : Number(value.toFixed(6));
}

function formatP(value) {
  if (value === null || value === undefined || Number.isNaN(value)) return '';
  return value < 0.000001 ? value.toExponential(12) : formatNumber(value);
}

function buildLogFacts(max) {
  const logFacts = Array(max + 1).fill(0);
  for (let i = 1; i <= max; i++) logFacts[i] = logFacts[i - 1] + Math.log(i);
  return logFacts;
}

const logFacts = buildLogFacts(10000);

function logChoose(n, k) {
  if (k < 0 || k > n) return Number.NEGATIVE_INFINITY;
  return logFacts[n] - logFacts[k] - logFacts[n - k];
}

function hypergeometric(a, b, c, d) {
  const n = a + b + c + d;
  const r1 = a + b;
  const c1 = a + c;
  return Math.exp(logChoose(c1, a) + logChoose(n - c1, r1 - a) - logChoose(n, r1));
}

function fisherTwoSided(a, b, c, d) {
  const r1 = a + b;
  const r2 = c + d;
  const c1 = a + c;
  const c2 = b + d;
  const minA = Math.max(0, c1 - r2);
  const maxA = Math.min(r1, c1);
  const observed = hypergeometric(a, b, c, d);
  let total = 0;
  for (let x = minA; x <= maxA; x++) {
    const y = r1 - x;
    const z = c1 - x;
    const w = c2 - y;
    const p = hypergeometric(x, y, z, w);
    if (p <= observed + 1e-12) total += p;
  }
  return Math.min(1, total);
}

function mulberry32(initialSeed) {
  let t = initialSeed;
  return () => {
    t += 0x6d2b79f5;
    let x = t;
    x = Math.imul(x ^ (x >>> 15), x | 1);
    x ^= x + Math.imul(x ^ (x >>> 7), x | 61);
    return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffle(values, random) {
  const copy = values.slice();
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

function shareDifference(rows, labels, companion, feature) {
  let compYes = 0;
  let compTotal = 0;
  let otherYes = 0;
  let otherTotal = 0;
  for (let i = 0; i < rows.length; i++) {
    const yes = rows[i].features[feature] ? 1 : 0;
    if (labels[i] === companion) {
      compYes += yes;
      compTotal++;
    } else {
      otherYes += yes;
      otherTotal++;
    }
  }
  if (!compTotal || !otherTotal) return 0;
  return Math.abs(compYes / compTotal - otherYes / otherTotal);
}

function blockPermutationP(rows, companion, feature, observedDiff) {
  const random = mulberry32(seed + companion.charCodeAt(0) * 1000 + feature.length * 17);
  const blocks = new Map();
  for (let i = 0; i < rows.length; i++) {
    const key = `${rows[i].type}|${rows[i].order}`;
    if (!blocks.has(key)) blocks.set(key, []);
    blocks.get(key).push(i);
  }
  const blockEntries = [...blocks.values()].map((indexes) => ({
    indexes,
    labels: indexes.map((index) => rows[index].companion),
  }));
  let ge = 0;
  for (let iter = 0; iter < permutationIterations; iter++) {
    const labels = Array(rows.length);
    for (const block of blockEntries) {
      const shuffled = shuffle(block.labels, random);
      for (let i = 0; i < block.indexes.length; i++) labels[block.indexes[i]] = shuffled[i];
    }
    const diff = shareDifference(rows, labels, companion, feature);
    if (diff >= observedDiff - 1e-12) ge++;
  }
  return (ge + 1) / (permutationIterations + 1);
}

function applyCorrections(tests, sourceField, bonferroniField, bhField) {
  const sorted = tests
    .filter((test) => Number.isFinite(test[sourceField]))
    .sort((a, b) => a[sourceField] - b[sourceField]);
  const m = sorted.length;
  for (const test of sorted) {
    test[bonferroniField] = Math.min(1, test[sourceField] * m);
  }
  let running = 1;
  for (let i = sorted.length - 1; i >= 0; i--) {
    const rank = i + 1;
    running = Math.min(running, (sorted[i][sourceField] * m) / rank);
    sorted[i][bhField] = Math.min(1, running);
  }
}

const sourceRows = csvObjects(fs.readFileSync(inputCsv, 'utf8'));
const rowsByCisi = new Map();
for (const row of sourceRows) {
  if (!rowsByCisi.has(row.cisi)) rowsByCisi.set(row.cisi, []);
  rowsByCisi.get(row.cisi).push(row);
}

const baseRows = sortRows(
  sourceRows
    .filter((row) => parseBool(row.short_mark_candidate) && row.site === 'Harappa' && targetTypes.has(row.type))
    .map((row) => {
      const tokens = parseTokens(row.text);
      const o = orientation(tokens);
      return o ? { ...row, tokens, token_string: tokens.join(';'), ...o } : null;
    })
    .filter(Boolean),
);

const contextRows = baseRows.map((row) => {
  const groupRows = sortRows(rowsByCisi.get(row.cisi) ?? []);
  const longerRows = groupRows.filter((candidate) => parseBool(candidate.long_text_candidate));
  const longerTokens = [...new Set(longerRows.flatMap((candidate) => parseTokens(candidate.text)))].sort((a, b) =>
    a.localeCompare(b, undefined, { numeric: true }),
  );
  const longerTexts = [...new Set(longerRows.map((candidate) => candidate.text))].sort((a, b) =>
    a.localeCompare(b, undefined, { numeric: true }),
  );
  const longerSideTexts = longerRows.map((candidate) => `${candidate.side_index}:${candidate.text}`);
  const allSideTexts = groupRows.map((candidate) => `${candidate.side_index}:${candidate.text}`);
  return {
    ...row,
    context_class: contextClass(longerRows, groupRows),
    side_relation: sideRelation(row.side_index, longerRows),
    longer_row_count: longerRows.length,
    longer_side_indexes: longerRows.map((candidate) => candidate.side_index).join(';'),
    longer_texts: longerTexts.join('|'),
    longer_side_texts: longerSideTexts.join('|'),
    longer_tokens: longerTokens.join(';'),
    group_signature: allSideTexts.join('|'),
    features: {},
  };
});

const sequenceCounts = new Map();
for (const row of contextRows) {
  for (const sequence of row.longer_texts.split('|').filter(Boolean)) {
    sequenceCounts.set(sequence, (sequenceCounts.get(sequence) ?? 0) + 1);
  }
}
const focusLongSequences = [...sequenceCounts.entries()]
  .filter(([, count]) => count >= 3)
  .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], undefined, { numeric: true }))
  .map(([sequence]) => sequence);

const baseFeatures = [
  { name: 'has_any_longer_text', label: 'any longer text', fn: (row) => row.longer_row_count > 0 },
  { name: 'single_longer_text', label: 'single longer text', fn: (row) => row.context_class === 'single_longer_text' },
  { name: 'multiple_longer_texts', label: 'multiple longer texts', fn: (row) => row.context_class === 'multiple_longer_texts' },
  { name: 'no_longer_text', label: 'no longer text', fn: (row) => row.side_relation === 'no_longer_text' },
  { name: 'short_after_all_longer', label: 'short after all longer rows', fn: (row) => row.side_relation === 'short_after_all_longer' },
  { name: 'short_before_all_longer', label: 'short before all longer rows', fn: (row) => row.side_relation === 'short_before_all_longer' },
  { name: 'short_between_longer_sides', label: 'short between longer sides', fn: (row) => row.side_relation === 'short_between_longer_sides' },
];

const tokenFeatures = focusLongTokens.map((token) => ({
  name: `has_long_token_${token}`,
  label: `longer text has token ${token}`,
  fn: (row) => row.longer_tokens.split(';').includes(token),
}));

const sequenceFeatures = focusLongSequences.map((sequence) => ({
  name: `has_long_sequence_${sequence.replace(/[+-]/g, '').replaceAll('-', '_')}`,
  label: `longer text has sequence ${sequence}`,
  fn: (row) => row.longer_texts.split('|').includes(sequence),
}));

const features = [...baseFeatures, ...tokenFeatures, ...sequenceFeatures];
for (const row of contextRows) {
  row.features = Object.fromEntries(features.map((feature) => [feature.name, feature.fn(row)]));
}

const rowOut = [
  [
    'id',
    'cisi',
    'type',
    'site',
    'short_side_index',
    'sides',
    'direction',
    'companion',
    'order',
    'short_text',
    'context_class',
    'side_relation',
    'longer_row_count',
    'longer_side_indexes',
    'longer_texts',
    'longer_tokens',
    'group_signature',
    'interpretation_status',
  ],
  ...contextRows.map((row) => [
    row.id,
    row.cisi,
    row.type,
    row.site,
    row.side_index,
    row.sides,
    row.direction,
    row.companion,
    row.order,
    row.text,
    row.context_class,
    row.side_relation,
    row.longer_row_count,
    row.longer_side_indexes,
    row.longer_texts,
    row.longer_tokens,
    row.group_signature,
    'companion_context_audit_only_no_reading',
  ]),
];

const familyMap = new Map();
for (const row of contextRows) {
  const key = [row.companion, row.type, row.order, row.context_class, row.side_relation, row.longer_side_texts || ''].join('\u0001');
  if (!familyMap.has(key)) {
    familyMap.set(key, {
      companion: row.companion,
      type: row.type,
      order: row.order,
      context_class: row.context_class,
      side_relation: row.side_relation,
      longer_side_texts: row.longer_side_texts,
      rows: 0,
      sample_cisi: [],
    });
  }
  const entry = familyMap.get(key);
  entry.rows++;
  if (entry.sample_cisi.length < 12 && !entry.sample_cisi.includes(row.cisi)) entry.sample_cisi.push(row.cisi);
}

const familyRows = [...familyMap.values()].sort(
  (a, b) =>
    b.rows - a.rows ||
    a.companion.localeCompare(b.companion, undefined, { numeric: true }) ||
    a.type.localeCompare(b.type) ||
    a.order.localeCompare(b.order) ||
    a.longer_side_texts.localeCompare(b.longer_side_texts, undefined, { numeric: true }),
);

const familyOut = [
  ['companion', 'type', 'order', 'context_class', 'side_relation', 'longer_side_texts', 'rows', 'sample_cisi', 'interpretation'],
  ...familyRows.map((row) => [
    row.companion,
    row.type,
    row.order,
    row.context_class,
    row.side_relation,
    row.longer_side_texts,
    row.rows,
    row.sample_cisi.join(';'),
    'companion_context_family_only_no_reading',
  ]),
];

const tests = [];
for (const companion of coreCompanions) {
  for (const feature of features) {
    const compRows = contextRows.filter((row) => row.companion === companion);
    const otherRows = contextRows.filter((row) => row.companion !== companion);
    const compYes = compRows.filter((row) => row.features[feature.name]).length;
    const compNo = compRows.length - compYes;
    const otherYes = otherRows.filter((row) => row.features[feature.name]).length;
    const otherNo = otherRows.length - otherYes;
    if (compYes + otherYes === 0 || compNo + otherNo === 0) continue;
    const observedDiff = Math.abs(compYes / compRows.length - otherYes / otherRows.length);
    tests.push({
      test_family: 'companion_context_assoc_one_vs_rest',
      companion,
      feature: feature.name,
      feature_label: feature.label,
      companion_yes: compYes,
      companion_no: compNo,
      other_yes: otherYes,
      other_no: otherNo,
      companion_share: compYes / compRows.length,
      other_share: otherYes / otherRows.length,
      abs_share_difference: observedDiff,
      fisher_raw_p: fisherTwoSided(compYes, compNo, otherYes, otherNo),
      fisher_bonferroni_p: '',
      fisher_bh_fdr_p: '',
      block_permutation_p: blockPermutationP(contextRows, companion, feature.name, observedDiff),
      block_permutation_bonferroni_p: '',
      block_permutation_bh_fdr_p: '',
      block_model: 'shuffle companion labels within type|700_order blocks',
      interpretation: 'companion_context_association_only_no_reading',
    });
  }
}

applyCorrections(tests, 'fisher_raw_p', 'fisher_bonferroni_p', 'fisher_bh_fdr_p');
applyCorrections(tests, 'block_permutation_p', 'block_permutation_bonferroni_p', 'block_permutation_bh_fdr_p');

const testOut = [
  [
    'test_family',
    'companion',
    'feature',
    'feature_label',
    'companion_yes',
    'companion_no',
    'other_yes',
    'other_no',
    'companion_share',
    'other_share',
    'abs_share_difference',
    'fisher_raw_p',
    'fisher_bonferroni_p',
    'fisher_bh_fdr_p',
    'block_permutation_p',
    'block_permutation_bonferroni_p',
    'block_permutation_bh_fdr_p',
    'block_model',
    'interpretation',
  ],
  ...tests
    .slice()
    .sort(
      (a, b) =>
        a.block_permutation_p - b.block_permutation_p ||
        a.fisher_raw_p - b.fisher_raw_p ||
        a.companion.localeCompare(b.companion, undefined, { numeric: true }) ||
        a.feature.localeCompare(b.feature),
    )
    .map((test) => [
      test.test_family,
      test.companion,
      test.feature,
      test.feature_label,
      test.companion_yes,
      test.companion_no,
      test.other_yes,
      test.other_no,
      formatNumber(test.companion_share),
      formatNumber(test.other_share),
      formatNumber(test.abs_share_difference),
      formatP(test.fisher_raw_p),
      formatP(test.fisher_bonferroni_p),
      formatP(test.fisher_bh_fdr_p),
      formatP(test.block_permutation_p),
      formatP(test.block_permutation_bonferroni_p),
      formatP(test.block_permutation_bh_fdr_p),
      test.block_model,
      test.interpretation,
    ]),
];

const companionSummaries = {};
for (const companion of coreCompanions) {
  const rows = contextRows.filter((row) => row.companion === companion);
  companionSummaries[companion] = {
    rows: rows.length,
    type_counts: objectFromCounts(countBy(rows, (row) => row.type)),
    order_counts: objectFromCounts(countBy(rows, (row) => row.order)),
    context_class_counts: objectFromCounts(countBy(rows, (row) => row.context_class)),
    side_relation_counts: objectFromCounts(countBy(rows, (row) => row.side_relation)),
    longer_token_presence_counts: Object.fromEntries(focusLongTokens.map((token) => [token, rows.filter((row) => row.longer_tokens.split(';').includes(token)).length])),
    top_longer_families: topCounts(countBy(rows, (row) => row.longer_side_texts || 'NO_LONGER_TEXT')),
  };
}

const correctedFisherFlags = tests
  .filter((test) => Number.isFinite(test.fisher_bh_fdr_p) && test.fisher_bh_fdr_p <= 0.05)
  .map((test) => `${test.companion}:${test.feature}`);
const correctedBlockFlags = tests
  .filter((test) => Number.isFinite(test.block_permutation_bh_fdr_p) && test.block_permutation_bh_fdr_p <= 0.05)
  .map((test) => `${test.companion}:${test.feature}`);

const summary = {
  source: 'Harappa TAB:B/TAB:I short-mark companion-context audit',
  checked_at: '2026-05-24',
  input: 'data/open_prototype/reports/lipi_multiside_mark_rows.csv',
  target_rows: contextRows.length,
  target_type_counts: objectFromCounts(countBy(contextRows, (row) => row.type)),
  companion_counts: objectFromCounts(countBy(contextRows, (row) => row.companion)),
  order_counts: objectFromCounts(countBy(contextRows, (row) => row.order)),
  context_class_counts: objectFromCounts(countBy(contextRows, (row) => row.context_class)),
  side_relation_counts: objectFromCounts(countBy(contextRows, (row) => row.side_relation)),
  focus_long_tokens: focusLongTokens,
  focus_long_sequences: focusLongSequences,
  permutation_model: {
    iterations: permutationIterations,
    seed,
    block: 'type|700_order',
  },
  emitted_tests: tests.length,
  corrected_fisher_flags: correctedFisherFlags,
  corrected_block_permutation_flags: correctedBlockFlags,
  companion_summaries: companionSummaries,
  key_observation:
    correctedBlockFlags.length > 0
      ? 'Some short-mark companions retain longer-context associations after preserving artifact type and 700-order blocks. These are validation-priority contrasts only.'
      : 'No short-mark companion longer-context association survives the type/order blocked permutation correction. Companion-specific raw contexts remain useful for validation targeting, not interpretation.',
  interpretation_boundary:
    'This is a companion-context audit only. It accepts no physical side function, numerical value, metrological reading, sign meaning, phonetic value, language identity, or translation.',
  outputs: [
    'data/open_prototype/reports/lipi_short_mark_companion_context_rows.csv',
    'data/open_prototype/reports/lipi_short_mark_companion_context_families.csv',
    'data/open_prototype/reports/lipi_short_mark_companion_context_tests.csv',
    'data/open_prototype/reports/lipi_short_mark_companion_context_summary.json',
  ],
};

fs.writeFileSync(outRowsCsv, toCsv(rowOut));
fs.writeFileSync(outFamiliesCsv, toCsv(familyOut));
fs.writeFileSync(outTestsCsv, toCsv(testOut));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
