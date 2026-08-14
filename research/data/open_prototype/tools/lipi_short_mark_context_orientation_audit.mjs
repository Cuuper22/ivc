// Orientation-context audit for the 700+companion short marks on Harappa
// TAB:B/TAB:I tablets. A two-sign mark can be written "700 first" or "700
// last". The earlier orientation audit showed the two orders are far from
// balanced; the question here is whether order also co-varies with context —
// do 700-first tablets carry different longer texts, side layouts, or focus
// signs than 700-last tablets?
//
// The script reads lipi_multiside_mark_rows.csv, keeps short-mark rows that
// are exactly a 700+032/033/034 pair, and attaches each row's object context:
// longer-text side count, the short side's position relative to the longer
// sides, presence of nine focus signs, and three specific recurring longer
// sequences. It then runs two-sided Fisher exact tests of 700-first vs.
// 700-last against each context feature — per companion and pooled — with
// Bonferroni and Benjamini-Hochberg corrections across all tests.
//
// Outputs: lipi_short_mark_context_orientation_rows.csv, _families.csv,
// _tests.csv, and _summary.json. Context association only; no reading of the
// marks is proposed.

import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const inputCsv = path.join(reportsDir, 'lipi_multiside_mark_rows.csv');
const outRowsCsv = path.join(reportsDir, 'lipi_short_mark_context_orientation_rows.csv');
const outFamiliesCsv = path.join(reportsDir, 'lipi_short_mark_context_orientation_families.csv');
const outTestsCsv = path.join(reportsDir, 'lipi_short_mark_context_orientation_tests.csv');
const outJson = path.join(reportsDir, 'lipi_short_mark_context_orientation_summary.json');

const targetTypes = new Set(['TAB:B', 'TAB:I']);
const coreCompanions = new Set(['032', '033', '034']);
const focusLongTokens = ['400', '740', '176', '240', '031', '001', '140', '368', '900'];
const focusLongSequences = ['+400-740-176+', '+740-031-001-140+', '+368-900+'];

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
  if (!coreCompanions.has(companion)) return null;
  return {
    companion,
    order: tokens[0] === '700' ? '700_first' : '700_last',
    unordered_pair: ['700', companion].sort().join('-'),
  };
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

function topCounts(counts, limit = 8) {
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

function applyCorrections(tests) {
  const sorted = tests
    .filter((test) => Number.isFinite(test.raw_p))
    .sort((a, b) => a.raw_p - b.raw_p);
  const m = sorted.length;
  for (const test of sorted) {
    test.bonferroni_p = Math.min(1, test.raw_p * m);
  }
  let running = 1;
  for (let i = sorted.length - 1; i >= 0; i--) {
    const rank = i + 1;
    running = Math.min(running, (sorted[i].raw_p * m) / rank);
    sorted[i].bh_fdr_p = Math.min(1, running);
  }
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

function hasLongSequence(row, sequence) {
  return row.longer_texts.split('|').includes(sequence);
}

function addFisherTest(tests, scope, companion, contextName, rows, yesFn) {
  const first = rows.filter((row) => row.order === '700_first');
  const last = rows.filter((row) => row.order === '700_last');
  if (!first.length || !last.length) return;
  const firstYes = first.filter(yesFn).length;
  const firstNo = first.length - firstYes;
  const lastYes = last.filter(yesFn).length;
  const lastNo = last.length - lastYes;
  if (firstYes + lastYes === 0 || firstNo + lastNo === 0) return;
  tests.push({
    test_family: 'orientation_context_assoc_fisher_700_first_vs_last',
    scope,
    companion,
    context: contextName,
    first_yes: firstYes,
    first_no: firstNo,
    last_yes: lastYes,
    last_no: lastNo,
    first_context_share: firstYes / first.length,
    last_context_share: lastYes / last.length,
    raw_p: fisherTwoSided(firstYes, firstNo, lastYes, lastNo),
    bonferroni_p: '',
    bh_fdr_p: '',
    interpretation: 'context_association_only_no_reading',
  });
}

const sourceRows = csvObjects(fs.readFileSync(inputCsv, 'utf8'));
const rowsByCisi = new Map();
for (const row of sourceRows) {
  if (!rowsByCisi.has(row.cisi)) rowsByCisi.set(row.cisi, []);
  rowsByCisi.get(row.cisi).push(row);
}

const targetRows = sortRows(
  sourceRows
    .filter((row) => parseBool(row.short_mark_candidate) && row.site === 'Harappa' && targetTypes.has(row.type))
    .map((row) => {
      const tokens = parseTokens(row.text);
      const o = orientation(tokens);
      return o ? { ...row, tokens, token_string: tokens.join(';'), ...o } : null;
    })
    .filter(Boolean),
);

const contextRows = targetRows.map((row) => {
  const groupRows = sortRows(rowsByCisi.get(row.cisi) ?? []);
  const longerRows = groupRows.filter((candidate) => parseBool(candidate.long_text_candidate));
  const longerTokens = [...new Set(longerRows.flatMap((candidate) => parseTokens(candidate.text)))].sort((a, b) =>
    a.localeCompare(b, undefined, { numeric: true }),
  );
  const longerTexts = longerRows.map((candidate) => candidate.text);
  const longerSideTexts = longerRows.map((candidate) => `${candidate.side_index}:${candidate.text}`);
  const allSideTexts = groupRows.map((candidate) => `${candidate.side_index}:${candidate.text}`);
  const relation = sideRelation(row.side_index, longerRows);
  const cls = contextClass(longerRows, groupRows);
  const focusTokenFlags = Object.fromEntries(focusLongTokens.map((token) => [`has_long_${token}`, longerTokens.includes(token)]));
  const focusSequenceFlags = Object.fromEntries(
    focusLongSequences.map((sequence) => [`has_sequence_${sequence.replace(/[+-]/g, '').replaceAll('-', '_')}`, longerTexts.includes(sequence)]),
  );
  return {
    ...row,
    context_class: cls,
    side_relation: relation,
    longer_row_count: longerRows.length,
    longer_side_indexes: longerRows.map((candidate) => candidate.side_index).join(';'),
    longer_texts: longerTexts.join('|'),
    longer_side_texts: longerSideTexts.join('|'),
    longer_tokens: longerTokens.join(';'),
    group_signature: allSideTexts.join('|'),
    ...focusTokenFlags,
    ...focusSequenceFlags,
  };
});

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
    'token_string',
    'context_class',
    'side_relation',
    'longer_row_count',
    'longer_side_indexes',
    'longer_texts',
    'longer_tokens',
    ...focusLongTokens.map((token) => `has_long_${token}`),
    ...focusLongSequences.map((sequence) => `has_sequence_${sequence.replace(/[+-]/g, '').replaceAll('-', '_')}`),
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
    row.token_string,
    row.context_class,
    row.side_relation,
    row.longer_row_count,
    row.longer_side_indexes,
    row.longer_texts,
    row.longer_tokens,
    ...focusLongTokens.map((token) => (row[`has_long_${token}`] ? 'true' : 'false')),
    ...focusLongSequences.map((sequence) => (row[`has_sequence_${sequence.replace(/[+-]/g, '').replaceAll('-', '_')}`] ? 'true' : 'false')),
    row.group_signature,
    'context_orientation_audit_only_no_reading',
  ]),
];

const familyMap = new Map();
for (const row of contextRows) {
  const key = [row.companion, row.order, row.type, row.context_class, row.side_relation, row.longer_side_texts || ''].join('\u0001');
  if (!familyMap.has(key)) {
    familyMap.set(key, {
      companion: row.companion,
      order: row.order,
      type: row.type,
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
    a.order.localeCompare(b.order) ||
    a.longer_side_texts.localeCompare(b.longer_side_texts, undefined, { numeric: true }),
);

const familyOut = [
  ['companion', 'order', 'type', 'context_class', 'side_relation', 'longer_side_texts', 'rows', 'sample_cisi', 'interpretation'],
  ...familyRows.map((row) => [
    row.companion,
    row.order,
    row.type,
    row.context_class,
    row.side_relation,
    row.longer_side_texts,
    row.rows,
    row.sample_cisi.join(';'),
    'context_family_only_no_reading',
  ]),
];

const tests = [];
for (const companion of [...coreCompanions].sort()) {
  const rows = contextRows.filter((row) => row.companion === companion);
  addFisherTest(tests, 'per_companion', companion, 'has_any_longer_text', rows, (row) => row.longer_row_count > 0);
  addFisherTest(tests, 'per_companion', companion, 'single_longer_text', rows, (row) => row.context_class === 'single_longer_text');
  addFisherTest(tests, 'per_companion', companion, 'multiple_longer_texts', rows, (row) => row.context_class === 'multiple_longer_texts');
  addFisherTest(tests, 'per_companion', companion, 'short_after_all_longer', rows, (row) => row.side_relation === 'short_after_all_longer');
  addFisherTest(tests, 'per_companion', companion, 'short_before_all_longer', rows, (row) => row.side_relation === 'short_before_all_longer');
  for (const token of focusLongTokens) {
    addFisherTest(tests, 'per_companion', companion, `has_long_token_${token}`, rows, (row) => row[`has_long_${token}`]);
  }
  for (const sequence of focusLongSequences) {
    const field = `has_sequence_${sequence.replace(/[+-]/g, '').replaceAll('-', '_')}`;
    addFisherTest(tests, 'per_companion', companion, `has_long_sequence_${sequence}`, rows, (row) => row[field]);
  }
}

addFisherTest(tests, 'all_core_companions', '032_033_034', 'has_any_longer_text', contextRows, (row) => row.longer_row_count > 0);
addFisherTest(tests, 'all_core_companions', '032_033_034', 'single_longer_text', contextRows, (row) => row.context_class === 'single_longer_text');
addFisherTest(tests, 'all_core_companions', '032_033_034', 'multiple_longer_texts', contextRows, (row) => row.context_class === 'multiple_longer_texts');
addFisherTest(tests, 'all_core_companions', '032_033_034', 'short_after_all_longer', contextRows, (row) => row.side_relation === 'short_after_all_longer');
addFisherTest(tests, 'all_core_companions', '032_033_034', 'short_before_all_longer', contextRows, (row) => row.side_relation === 'short_before_all_longer');
for (const token of focusLongTokens) {
  addFisherTest(tests, 'all_core_companions', '032_033_034', `has_long_token_${token}`, contextRows, (row) => row[`has_long_${token}`]);
}
for (const sequence of focusLongSequences) {
  const field = `has_sequence_${sequence.replace(/[+-]/g, '').replaceAll('-', '_')}`;
  addFisherTest(tests, 'all_core_companions', '032_033_034', `has_long_sequence_${sequence}`, contextRows, (row) => row[field]);
}

applyCorrections(tests);

const testOut = [
  [
    'test_family',
    'scope',
    'companion',
    'context',
    'first_yes',
    'first_no',
    'last_yes',
    'last_no',
    'first_context_share',
    'last_context_share',
    'raw_p',
    'bonferroni_p',
    'bh_fdr_p',
    'interpretation',
  ],
  ...tests
    .slice()
    .sort((a, b) => a.raw_p - b.raw_p || a.companion.localeCompare(b.companion, undefined, { numeric: true }) || a.context.localeCompare(b.context))
    .map((test) => [
      test.test_family,
      test.scope,
      test.companion,
      test.context,
      test.first_yes,
      test.first_no,
      test.last_yes,
      test.last_no,
      formatNumber(test.first_context_share),
      formatNumber(test.last_context_share),
      formatP(test.raw_p),
      formatP(test.bonferroni_p),
      formatP(test.bh_fdr_p),
      test.interpretation,
    ]),
];

const companionOrderContext = {};
for (const companion of [...coreCompanions].sort()) {
  companionOrderContext[companion] = {};
  for (const order of ['700_first', '700_last']) {
    const rows = contextRows.filter((row) => row.companion === companion && row.order === order);
    companionOrderContext[companion][order] = {
      rows: rows.length,
      context_class_counts: objectFromCounts(countBy(rows, (row) => row.context_class)),
      side_relation_counts: objectFromCounts(countBy(rows, (row) => row.side_relation)),
      longer_token_presence_counts: Object.fromEntries(focusLongTokens.map((token) => [token, rows.filter((row) => row[`has_long_${token}`]).length])),
      top_longer_families: topCounts(countBy(rows, (row) => row.longer_side_texts || 'NO_LONGER_TEXT'), 8),
    };
  }
}

const correctedContextFlags = tests
  .filter((test) => Number.isFinite(test.bh_fdr_p) && test.bh_fdr_p <= 0.05)
  .map((test) => `${test.scope}:${test.companion}:${test.context}`);

const summary = {
  source: 'Harappa TAB:B/TAB:I short-mark orientation-context audit',
  checked_at: '2026-05-24',
  input: 'data/open_prototype/reports/lipi_multiside_mark_rows.csv',
  target_rows: contextRows.length,
  target_type_counts: objectFromCounts(countBy(contextRows, (row) => row.type)),
  companion_counts: objectFromCounts(countBy(contextRows, (row) => row.companion)),
  order_counts: objectFromCounts(countBy(contextRows, (row) => row.order)),
  context_class_counts: objectFromCounts(countBy(contextRows, (row) => row.context_class)),
  side_relation_counts: objectFromCounts(countBy(contextRows, (row) => row.side_relation)),
  companion_order_context: companionOrderContext,
  emitted_tests: tests.length,
  corrected_context_flags: correctedContextFlags,
  key_observation:
    correctedContextFlags.length > 0
      ? 'Some 700-companion short-mark orientations are context-associated in the current planning layer, so reversed forms should be carried as separate validation targets.'
      : 'No orientation-context association survives correction in this planning-layer audit; exact order still remains a validation variable because the prior orientation audit found strong order imbalance.',
  interpretation_boundary:
    'This is an artifact-side context audit only. It accepts no physical side function, numerical value, metrological reading, sign meaning, phonetic value, language identity, or translation.',
  outputs: [
    'data/open_prototype/reports/lipi_short_mark_context_orientation_rows.csv',
    'data/open_prototype/reports/lipi_short_mark_context_orientation_families.csv',
    'data/open_prototype/reports/lipi_short_mark_context_orientation_tests.csv',
    'data/open_prototype/reports/lipi_short_mark_context_orientation_summary.json',
  ],
};

fs.writeFileSync(outRowsCsv, toCsv(rowOut));
fs.writeFileSync(outFamiliesCsv, toCsv(familyOut));
fs.writeFileSync(outTestsCsv, toCsv(testOut));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
