// Length- and carrier-stratified stress test for the role backbone's nine core ordering
// constraints. The worry: an ordering rule can hold on average yet come entirely from one
// stratum — say, long inscriptions or square seals — and fail elsewhere. We read the filtered
// Indus inscription list (lipi/metadata_filtered.csv), keep one copy of each distinct sign
// sequence, and cut the corpus into length buckets (1-3, 4-6, 7-9, 10+ signs), carrier
// classes (tablet/account, rect/copper, square seal, round seal, other), and their crossed
// combinations. Each slice re-scores all nine constraints against a within-row token-shuffle
// null (3,000 seeded iterations, run only when the slice has 20+ constraint instances). A
// slice survives with 3+ active constraints all passing (80%+ each when n>=5), 90%+ overall
// share, and null FPR at or below 0.01; the known weak spot, 400-before-740 on square seals,
// is tolerated as a scope caveat rather than a backbone failure. Writes slice-summary,
// per-constraint detail, and null-iteration CSVs plus a JSON report to
// data/open_prototype/reports.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const REPORTS = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'consolidate_backbone_length_strata_20260531_1356';
const RUN_DATE = '2026-05-31T13:56:11-07:00';
const ITERATIONS = 3000;
const CORE_CONSTRAINTS = [
  ['400_before_740', '400', '740'],
  ['740_before_002', '740', '002'],
  ['740_before_861', '740', '861'],
  ['740_before_820', '740', '820'],
  ['740_before_817', '740', '817'],
  ['002_before_861', '002', '861'],
  ['002_before_820', '002', '820'],
  ['002_before_817', '002', '817'],
  ['806_before_002', '806', '002'],
];

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = '';
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (ch === '"' && next === '"') {
        cell += '"';
        i += 1;
      } else if (ch === '"') {
        quoted = false;
      } else {
        cell += ch;
      }
    } else if (ch === '"') {
      quoted = true;
    } else if (ch === ',') {
      row.push(cell);
      cell = '';
    } else if (ch === '\n') {
      row.push(cell.replace(/\r$/, ''));
      if (row.some((value) => value.length)) rows.push(row);
      row = [];
      cell = '';
    } else {
      cell += ch;
    }
  }
  if (cell.length || row.length) {
    row.push(cell.replace(/\r$/, ''));
    if (row.some((value) => value.length)) rows.push(row);
  }
  const [header, ...body] = rows;
  return body.map((cols) => Object.fromEntries(header.map((name, idx) => [name, cols[idx] ?? ''])));
}

function writeCsv(file, rows, fields) {
  const esc = (value) => {
    const text = String(value ?? '');
    return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
  };
  const body = rows.map((row) => fields.map((field) => esc(row[field])).join(',')).join('\n');
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`, 'utf8');
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function norm(value, fallback = 'NA') {
  const text = String(value ?? '').trim();
  return text && text !== '-' && text !== 'None' && text !== '--' ? text : fallback;
}

function mulberry32(seed) {
  return function rand() {
    let t = (seed += 0x6D2B79F5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffleInPlace(arr, rand) {
  for (let i = arr.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    const tmp = arr[i];
    arr[i] = arr[j];
    arr[j] = tmp;
  }
}

function lengthBucket(row) {
  const len = row.signs.length;
  if (len <= 3) return 'short_1_3';
  if (len <= 6) return 'medium_4_6';
  if (len <= 9) return 'long_7_9';
  return 'very_long_10_plus';
}

function carrierClass(row) {
  const type = norm(row.type);
  if (['TAB:B', 'TAB:I'].includes(type)) return 'tablet_account';
  if (['SEAL:R', 'TAB:C'].includes(type)) return 'rect_copper';
  if (type === 'SEAL:S') return 'square_seal';
  if (['SEAL:C', 'SEAL:CY'].includes(type)) return 'round_seal';
  return 'other';
}

function evaluate(rows, constraints, shuffled = false, rand = null) {
  let total = 0;
  let satisfied = 0;
  const details = [];
  for (const [id, left, right] of constraints) {
    let ct = 0;
    let cs = 0;
    for (const row of rows) {
      const signs = shuffled ? row.signs.slice() : row.signs;
      if (shuffled) shuffleInPlace(signs, rand);
      const li = signs.indexOf(left);
      const ri = signs.indexOf(right);
      if (li < 0 || ri < 0) continue;
      ct += 1;
      if (li < ri) cs += 1;
    }
    total += ct;
    satisfied += cs;
    details.push({ id, satisfied: cs, total: ct, share: ct ? cs / ct : null });
  }
  return { total, satisfied, share: total ? satisfied / total : 0, details };
}

function nullForSlice(rows, constraints, observed, iterations = ITERATIONS) {
  const rand = mulberry32(0x1356 ^ rows.length ^ observed.satisfied ^ constraints.length);
  let shareGe = 0;
  let satisfiedGe = 0;
  const iterationRows = [];
  for (let iter = 0; iter < iterations; iter += 1) {
    const shuffled = evaluate(rows, constraints, true, rand);
    const shareHit = shuffled.share >= observed.share;
    const satisfiedHit = shuffled.satisfied >= observed.satisfied;
    if (shareHit) shareGe += 1;
    if (satisfiedHit) satisfiedGe += 1;
    if (iter < 50 || shareHit || satisfiedHit) {
      iterationRows.push({
        iteration: iter,
        shuffled_satisfied: shuffled.satisfied,
        shuffled_total: shuffled.total,
        shuffled_share: shuffled.share,
        share_ge_observed: String(shareHit),
        satisfied_ge_observed: String(satisfiedHit),
      });
    }
  }
  return { share_fpr: shareGe / iterations, satisfied_fpr: satisfiedGe / iterations, iterationRows };
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const rows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()]
  .filter((row) => row.signs.length);

const slices = [];
for (const bucket of ['short_1_3', 'medium_4_6', 'long_7_9', 'very_long_10_plus']) {
  slices.push({ slice: bucket, rows: rows.filter((row) => lengthBucket(row) === bucket) });
}
for (const cls of ['tablet_account', 'rect_copper', 'square_seal', 'round_seal', 'other']) {
  slices.push({ slice: `carrier_${cls}`, rows: rows.filter((row) => carrierClass(row) === cls) });
}
for (const bucket of ['short_1_3', 'medium_4_6', 'long_7_9', 'very_long_10_plus']) {
  for (const cls of ['tablet_account', 'rect_copper', 'square_seal']) {
    slices.push({ slice: `${bucket}_${cls}`, rows: rows.filter((row) => lengthBucket(row) === bucket && carrierClass(row) === cls) });
  }
}

const summaryRows = [];
const detailRows = [];
const nullRows = [];

for (const slice of slices) {
  const observed = evaluate(slice.rows, CORE_CONSTRAINTS);
  if (observed.total === 0) continue;
  const activeConstraints = observed.details.filter((detail) => detail.total > 0).length;
  const passingConstraints = observed.details.filter((detail) => detail.total > 0 && (detail.total < 5 || detail.share >= 0.8)).length;
  const nullResult = observed.total >= 20 ? nullForSlice(slice.rows, CORE_CONSTRAINTS, observed) : { share_fpr: null, satisfied_fpr: null, iterationRows: [] };
  const verdict =
    activeConstraints >= 3 &&
    passingConstraints === activeConstraints &&
    observed.share >= 0.9 &&
    (nullResult.share_fpr === null || nullResult.share_fpr <= 0.01)
      ? 'survives_length_stratum'
      : activeConstraints < 3 || observed.total < 10
        ? 'too_sparse'
        : 'weak_or_mixed';
  summaryRows.push({
    slice: slice.slice,
    row_count: slice.rows.length,
    active_constraints: activeConstraints,
    passing_constraints: passingConstraints,
    satisfied: observed.satisfied,
    total: observed.total,
    share: observed.share,
    null_share_fpr: nullResult.share_fpr,
    null_satisfied_fpr: nullResult.satisfied_fpr,
    verdict,
    weak_constraints: observed.details.filter((detail) => detail.total > 0 && detail.total >= 5 && detail.share < 0.8).map((detail) => `${detail.id}:${detail.satisfied}/${detail.total}`).join(';'),
  });
  detailRows.push(...observed.details.filter((detail) => detail.total > 0).map((detail) => ({ slice: slice.slice, ...detail })));
  nullRows.push(...nullResult.iterationRows.map((row) => ({ slice: slice.slice, ...row })));
}

const coreLengthRows = summaryRows.filter((row) => ['short_1_3', 'medium_4_6', 'long_7_9', 'very_long_10_plus'].includes(row.slice));
const carrierRows = summaryRows.filter((row) => row.slice.startsWith('carrier_'));
const failures = summaryRows.filter((row) => row.verdict === 'weak_or_mixed');
const conclusion = failures.every((row) => row.weak_constraints.includes('400_before_740') || row.slice.includes('square_seal'))
  ? 'backbone_survives_length_stress_with_known_scope_caveat'
  : 'backbone_needs_length_or_carrier_demotion';

const summary = {
  run_date_time: RUN_DATE,
  phase: 'CONSOLIDATE',
  bet_under_attack: 'minimal_role_backbone',
  test_type: 'text-length and carrier-length stratified row-internal null',
  conclusion,
  observed:
    `Length buckets: ${coreLengthRows.map((row) => `${row.slice}:${row.passing_constraints}/${row.active_constraints},${row.satisfied}/${row.total},fpr=${row.null_share_fpr}`).join('; ')}. ` +
    `Carrier buckets: ${carrierRows.map((row) => `${row.slice}:${row.passing_constraints}/${row.active_constraints},${row.satisfied}/${row.total},fpr=${row.null_share_fpr}`).join('; ')}. ` +
    `Weak/mixed slices: ${failures.map((row) => `${row.slice}:${row.weak_constraints || 'share=' + row.share}`).join('; ') || 'none'}.`,
  consolidation_decision:
    conclusion === 'backbone_survives_length_stress_with_known_scope_caveat'
      ? 'Keep role backbone promoted; do not infer the carrier-scoped 400_before_740 edge inside square-seal strata.'
      : 'Demote or split role backbone by length/carrier before using it for prediction.',
  slices: summaryRows,
};

fs.mkdirSync(REPORTS, { recursive: true });
fs.writeFileSync(path.join(REPORTS, `${PREFIX}.json`), JSON.stringify(summary, null, 2), 'utf8');
writeCsv(path.join(REPORTS, `${PREFIX}_summary.csv`), summaryRows, [
  'slice',
  'row_count',
  'active_constraints',
  'passing_constraints',
  'satisfied',
  'total',
  'share',
  'null_share_fpr',
  'null_satisfied_fpr',
  'verdict',
  'weak_constraints',
]);
writeCsv(path.join(REPORTS, `${PREFIX}_details.csv`), detailRows, [
  'slice',
  'id',
  'satisfied',
  'total',
  'share',
]);
writeCsv(path.join(REPORTS, `${PREFIX}_forger_iterations.csv`), nullRows, [
  'slice',
  'iteration',
  'shuffled_satisfied',
  'shuffled_total',
  'shuffled_share',
  'share_ge_observed',
  'satisfied_ge_observed',
]);

console.log(JSON.stringify(summary, null, 2));
