import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const inputCsv = path.join(reportsDir, 'lipi_multiside_mark_rows.csv');
const outRowsCsv = path.join(reportsDir, 'lipi_short_mark_orientation_rows.csv');
const outCompanionCsv = path.join(reportsDir, 'lipi_short_mark_orientation_companions.csv');
const outTestsCsv = path.join(reportsDir, 'lipi_short_mark_orientation_tests.csv');
const outJson = path.join(reportsDir, 'lipi_short_mark_orientation_summary.json');

const targetTypes = new Set(['TAB:B', 'TAB:I']);
const coreCompanions = new Set(['032', '033', '034']);

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

function formatNumber(value) {
  return value === null || value === undefined || Number.isNaN(value) ? '' : Number(value.toFixed(6));
}

function formatP(value) {
  if (value === null || value === undefined || Number.isNaN(value)) return '';
  return value < 0.000001 ? value.toExponential(12) : formatNumber(value);
}

function orientation(tokens) {
  if (tokens.length !== 2 || !tokens.includes('700')) {
    return {
      orientation_class: tokens.includes('700') ? 'other_700_row' : 'non_700_short_mark',
      companion: '',
      order: '',
      unordered_pair: tokens.slice().sort().join('-'),
    };
  }
  const companion = tokens[0] === '700' ? tokens[1] : tokens[0];
  return {
    orientation_class: 'two_token_700_companion',
    companion,
    order: tokens[0] === '700' ? '700_first' : '700_last',
    unordered_pair: ['700', companion].sort().join('-'),
  };
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

function binomialTwoSided(k, n, p = 0.5) {
  if (n <= 0) return null;
  const logP = (x) => logChoose(n, x) + x * Math.log(p) + (n - x) * Math.log(1 - p);
  const observed = logP(k);
  let total = 0;
  for (let x = 0; x <= n; x++) {
    const lp = logP(x);
    if (lp <= observed + 1e-12) total += Math.exp(lp);
  }
  return Math.min(1, total);
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

function count(rows, filterFn) {
  return rows.filter(filterFn).length;
}

const sourceRows = csvObjects(fs.readFileSync(inputCsv, 'utf8'));
const targetRows = sourceRows
  .filter((row) => parseBool(row.short_mark_candidate) && row.site === 'Harappa' && targetTypes.has(row.type))
  .map((row) => {
    const parsedTokens = parseTokens(row.text);
    const o = orientation(parsedTokens);
    return {
      ...row,
      tokens: parsedTokens,
      token_string: parsedTokens.join(';'),
      ...o,
    };
  });

const rowOut = [
  [
    'id',
    'cisi',
    'type',
    'site',
    'side_index',
    'sides',
    'direction',
    'token_count',
    'text',
    'token_string',
    'orientation_class',
    'companion',
    'order',
    'unordered_pair',
    'interpretation_status',
  ],
];
for (const row of targetRows) {
  rowOut.push([
    row.id,
    row.cisi,
    row.type,
    row.site,
    row.side_index,
    row.sides,
    row.direction,
    row.token_count,
    row.text,
    row.token_string,
    row.orientation_class,
    row.companion,
    row.order,
    row.unordered_pair,
    'orientation_audit_only_no_reading',
  ]);
}

const twoTokenRows = targetRows.filter((row) => row.orientation_class === 'two_token_700_companion');
const companionRows = [
  [
    'scope',
    'type',
    'side_index',
    'companion',
    'rows',
    'first_700',
    'last_700',
    'first_share',
    'sample_cisi',
    'interpretation',
  ],
];

function addCompanionSummary(scope, rows, type = 'ALL', sideIndex = 'ALL') {
  const companions = [...countBy(rows, (row) => row.companion).keys()].sort((a, b) =>
    a.localeCompare(b, undefined, { numeric: true }),
  );
  for (const companion of companions) {
    const selected = rows.filter((row) => row.companion === companion);
    const first = count(selected, (row) => row.order === '700_first');
    const last = count(selected, (row) => row.order === '700_last');
    companionRows.push([
      scope,
      type,
      sideIndex,
      companion,
      selected.length,
      first,
      last,
      formatNumber(first / selected.length),
      selected
        .map((row) => row.cisi)
        .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }))
        .slice(0, 12)
        .join(';'),
      'orientation_summary_only_no_reading',
    ]);
  }
}

addCompanionSummary('all_target_rows', twoTokenRows);
for (const type of ['TAB:B', 'TAB:I']) {
  addCompanionSummary(`type_${type}`, twoTokenRows.filter((row) => row.type === type), type);
}
for (const type of ['TAB:B', 'TAB:I']) {
  for (const sideIndex of ['1', '2', '3']) {
    addCompanionSummary(
      `type_${type}_side_${sideIndex}`,
      twoTokenRows.filter((row) => row.type === type && row.side_index === sideIndex),
      type,
      sideIndex,
    );
  }
}

const tests = [];
for (const companion of [...countBy(twoTokenRows, (row) => row.companion).keys()].sort((a, b) =>
  a.localeCompare(b, undefined, { numeric: true }),
)) {
  const selected = twoTokenRows.filter((row) => row.companion === companion);
  if (selected.length >= 5) {
    const first = count(selected, (row) => row.order === '700_first');
    const last = count(selected, (row) => row.order === '700_last');
    tests.push({
      comparison: 'orientation_balance_binomial_700_first_vs_last',
      companion,
      scope: 'all_target_rows',
      a_label: '700_first',
      a_count: first,
      b_label: '700_last',
      b_count: last,
      raw_p: binomialTwoSided(first, first + last, 0.5),
      detail: 'two_sided_binomial_p_0_5',
    });
  }
}

for (const companion of [...coreCompanions]) {
  const selected = twoTokenRows.filter((row) => row.companion === companion);
  if (selected.length >= 10) {
    const tabIFirst = count(selected, (row) => row.type === 'TAB:I' && row.order === '700_first');
    const tabILast = count(selected, (row) => row.type === 'TAB:I' && row.order === '700_last');
    const tabBFirst = count(selected, (row) => row.type === 'TAB:B' && row.order === '700_first');
    const tabBLast = count(selected, (row) => row.type === 'TAB:B' && row.order === '700_last');
    tests.push({
      comparison: 'type_orientation_assoc_fisher_TAB_I_vs_TAB_B',
      companion,
      scope: 'TAB:I_vs_TAB:B',
      a_label: 'TAB:I_700_first;TAB:I_700_last',
      a_count: `${tabIFirst};${tabILast}`,
      b_label: 'TAB:B_700_first;TAB:B_700_last',
      b_count: `${tabBFirst};${tabBLast}`,
      raw_p: fisherTwoSided(tabIFirst, tabILast, tabBFirst, tabBLast),
      detail: 'two_sided_fisher_exact',
    });
  }
}

for (const companion of [...coreCompanions]) {
  for (const type of ['TAB:B', 'TAB:I']) {
    const selected = twoTokenRows.filter((row) => row.companion === companion && row.type === type);
    if (selected.length >= 10) {
      const side1First = count(selected, (row) => row.side_index === '1' && row.order === '700_first');
      const side1Last = count(selected, (row) => row.side_index === '1' && row.order === '700_last');
      const side2First = count(selected, (row) => row.side_index === '2' && row.order === '700_first');
      const side2Last = count(selected, (row) => row.side_index === '2' && row.order === '700_last');
      if (side1First + side1Last > 0 && side2First + side2Last > 0) {
        tests.push({
          comparison: 'side_index_orientation_assoc_fisher_side1_vs_side2',
          companion,
          scope: type,
          a_label: 'side1_700_first;side1_700_last',
          a_count: `${side1First};${side1Last}`,
          b_label: 'side2_700_first;side2_700_last',
          b_count: `${side2First};${side2Last}`,
          raw_p: fisherTwoSided(side1First, side1Last, side2First, side2Last),
          detail: 'two_sided_fisher_exact',
        });
      }
    }
  }
}

applyCorrections(tests);

const testRows = [
  [
    'comparison',
    'companion',
    'scope',
    'a_label',
    'a_count',
    'b_label',
    'b_count',
    'raw_p',
    'bonferroni_p',
    'bh_fdr_p',
    'detail',
    'interpretation',
  ],
];
for (const test of tests) {
  testRows.push([
    test.comparison,
    test.companion,
    test.scope,
    test.a_label,
    test.a_count,
    test.b_label,
    test.b_count,
    formatP(test.raw_p),
    formatP(test.bonferroni_p),
    formatP(test.bh_fdr_p),
    test.detail,
    'orientation_control_only_no_reading',
  ]);
}

const coreRows = twoTokenRows.filter((row) => coreCompanions.has(row.companion));
const summary = {
  source: 'Harappa TAB:B/TAB:I short-mark orientation audit',
  checked_at: '2026-05-24',
  input: path.relative(base, inputCsv).replaceAll('\\', '/'),
  target_short_mark_rows: targetRows.length,
  two_token_700_companion_rows: twoTokenRows.length,
  core_032_033_034_rows: coreRows.length,
  target_type_counts: objectFromCounts(countBy(targetRows, (row) => row.type)),
  orientation_class_counts: objectFromCounts(countBy(targetRows, (row) => row.orientation_class)),
  two_token_order_counts: objectFromCounts(countBy(twoTokenRows, (row) => row.order)),
  core_companion_order_counts: Object.fromEntries(
    [...coreCompanions].map((companion) => {
      const selected = twoTokenRows.filter((row) => row.companion === companion);
      return [
        companion,
        {
          rows: selected.length,
          order_counts: objectFromCounts(countBy(selected, (row) => row.order)),
          type_counts: objectFromCounts(countBy(selected, (row) => row.type)),
          side_counts: objectFromCounts(countBy(selected, (row) => row.side_index)),
        },
      ];
    }),
  ),
  corrected_orientation_flags: tests
    .filter((test) => Number.isFinite(test.bh_fdr_p) && test.bh_fdr_p <= 0.05)
    .map((test) => `${test.comparison}:${test.scope}:${test.companion}`),
  key_observation:
    'In the Harappa TAB:B/TAB:I short-mark queue, two-token 700 companion marks are strongly 700-first overall, but reversed 033/032/034 forms are present. Orientation is therefore a validation variable, not a value or reading.',
  interpretation_boundary:
    'This is a local side-mark orientation audit only. It accepts no physical side function, numerical value, metrological reading, sign meaning, phonetic value, language identity, or translation.',
  outputs: [outRowsCsv, outCompanionCsv, outTestsCsv, outJson].map((file) => path.relative(base, file).replaceAll('\\', '/')),
};

fs.writeFileSync(outRowsCsv, toCsv(rowOut));
fs.writeFileSync(outCompanionCsv, toCsv(companionRows));
fs.writeFileSync(outTestsCsv, toCsv(testRows));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
