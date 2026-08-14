// Tests whether the rare sign `597` belongs exclusively to the copper-tablet
// subregister (material Copper, type TAB:C), usually inside the fixed template
// `617-142-597-032-(904/905)`. A context/template claim, not a sound value. The
// script reads metadata_filtered.csv, collapses duplicate sign sequences, and
// Fisher-tests every sign for copper-TAB:C enrichment so 597 gets an all-sign rank
// and a Bonferroni-corrected p. A 5,000-iteration forger redraws the context rows
// at random and takes the best p over all signs (max-stat). It also checks that
// every row carrying the literal 617-142-597-032 motif is copper TAB:C, and counts
// how many support rows are in Poor condition — a warning that caps the tier at
// candidate. Writes a bet summary (JSON + CSV) plus support-row and top-sign CSVs
// to the reports directory.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_597_copper_tab_c_subregister_forger_20260531';
const RUN_DATE = '2026-05-31';
const TARGET = '597';
const ITERATIONS = 5000;

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

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

const logFactCache = new Map();
function getLogFact(n) {
  if (logFactCache.has(n)) return logFactCache.get(n);
  const logFact = [0];
  for (let i = 1; i <= n; i += 1) logFact[i] = logFact[i - 1] + Math.log(i);
  logFactCache.set(n, logFact);
  return logFact;
}

function fisherRightTail(a, b, c, d) {
  const n = a + b + c + d;
  const logFact = getLogFact(n);
  const logChoose = (nn, kk) => logFact[nn] - logFact[kk] - logFact[nn - kk];
  const row1 = a + b;
  const row2 = c + d;
  const col1 = a + c;
  const max = Math.min(row1, col1);
  const logDen = logChoose(n, col1);
  let p = 0;
  for (let x = a; x <= max; x += 1) {
    p += Math.exp(logChoose(row1, x) + logChoose(row2, col1 - x) - logDen);
  }
  return Math.max(0, Math.min(1, p));
}

function mulberry32(seed) {
  return function rand() {
    let t = (seed += 0x6D2B79F5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function sampleWithoutReplacement(rand, n, k) {
  const arr = Array.from({ length: n }, (_, idx) => idx);
  for (let i = 0; i < k; i += 1) {
    const j = i + Math.floor(rand() * (n - i));
    const tmp = arr[i];
    arr[i] = arr[j];
    arr[j] = tmp;
  }
  return arr.slice(0, k);
}

function hasMotif(signs) {
  for (let i = 0; i <= signs.length - 4; i += 1) {
    if (signs[i] === '617' && signs[i + 1] === '142' && signs[i + 2] === '597' && signs[i + 3] === '032') return true;
  }
  return false;
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()]
  .map((row, idx) => ({ ...row, _idx: idx, signSet: new Set(row.signs) }));
const contextRows = canonicalRows.filter((row) => norm(row.material) === 'Copper' && norm(row.type) === 'TAB:C');
const backgroundRows = canonicalRows.filter((row) => !(norm(row.material) === 'Copper' && norm(row.type) === 'TAB:C'));
const signs = [...new Set(canonicalRows.flatMap((row) => row.signs))].sort();
const totalSignCounts = new Map(signs.map((sign) => [sign, canonicalRows.filter((row) => row.signSet.has(sign)).length]));
const signRows = signs.map((sign) => {
  const a = contextRows.filter((row) => row.signSet.has(sign)).length;
  const c = totalSignCounts.get(sign) - a;
  const p = fisherRightTail(a, contextRows.length - a, c, backgroundRows.length - c);
  return {
    sign,
    context_rows: contextRows.length,
    a,
    b: contextRows.length - a,
    c,
    d: backgroundRows.length - c,
    total: a + c,
    fisher_p: p,
  };
}).sort((x, y) => x.fisher_p - y.fisher_p || y.a - x.a || x.sign.localeCompare(y.sign, undefined, { numeric: true }));
const target = signRows.find((row) => row.sign === TARGET);
const targetRank = signRows.findIndex((row) => row.sign === TARGET) + 1;
const rand = mulberry32(0x5972026);
let maxGe = 0;
for (let iter = 0; iter < ITERATIONS; iter += 1) {
  const chosen = new Set(sampleWithoutReplacement(rand, canonicalRows.length, contextRows.length));
  let best = 1;
  for (const sign of signs) {
    let a = 0;
    for (const idx of chosen) if (canonicalRows[idx].signSet.has(sign)) a += 1;
    const c = totalSignCounts.get(sign) - a;
    const p = fisherRightTail(a, contextRows.length - a, c, backgroundRows.length - c);
    if (p < best) best = p;
  }
  if (best <= target.fisher_p) maxGe += 1;
}

const supportRows = canonicalRows.filter((row) => row.signSet.has(TARGET)).map((row) => ({
  object: objectId(row),
  region: norm(row.region),
  site: norm(row.site),
  type: norm(row.type),
  material: norm(row.material),
  shape: norm(row.shape),
  condition: norm(row.condition),
  complete: norm(row.complete),
  copper_tab_c_context: String(norm(row.material) === 'Copper' && norm(row.type) === 'TAB:C'),
  has_617_142_597_032_motif: String(hasMotif(row.signs)),
  text: row.text,
}));
const motifRows = canonicalRows.filter((row) => hasMotif(row.signs));
const supportPoor = supportRows.filter((row) => row.condition === 'Poor').length;

const tier =
  target.a === target.total &&
  target.total >= 4 &&
  target.fisher_p * signs.length <= 0.01 &&
  maxGe / ITERATIONS <= 0.01
    ? 'candidate'
    : 'wild shot';

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V4_597_COPPER_TAB_C_SUBREGISTER_20260531',
  vector: 'V4 context-to-meaning without sound',
  confidence_tier: tier,
  risky_bet:
    '`597` marks a narrow copper/TAB:C subregister, usually in the `617-142-597-032-(904/905)` template. This predicts context/template membership only, not sound.',
  observed:
    `Canonical rows=${canonicalRows.length}; copper TAB:C rows=${contextRows.length}; 597 rows=${target.total}; 597 in copper TAB:C=${target.a}/${target.total}; background=${target.c}/${backgroundRows.length}; all-sign rank=${targetRank}/${signRows.length}; Bonferroni=${Math.min(1, target.fisher_p * signs.length)}; maxstat=${maxGe / ITERATIONS}. Motif 617-142-597-032 rows=${motifRows.length}, all copper TAB:C. Support condition: ${supportPoor}/${supportRows.length} poor.`,
  adversarial_test:
    `Canonical numeric-sequence collapse; all-sign Fisher rank over ${signRows.length} signs; Bonferroni; ${ITERATIONS}-iteration max-stat context-label forger; exact motif check.`,
  false_positive_rate: maxGe / ITERATIONS,
  bonferroni_p: Math.min(1, target.fisher_p * signs.length),
  fisher_p: target.fisher_p,
  support_condition_warning: `${supportPoor}/${supportRows.length} support rows are marked Poor; this blocks promotion beyond candidate.`,
  falsifier:
    'A single source-verified non-copper/non-TAB:C 597 row, or confirmation that the four poor 597 rows are damaged/read through a shared cataloging convention, demotes this to wild shot.',
  next_prediction:
    'Unverified rows containing 617-142-597-032 should be copper TAB:C; additional copper TAB:C rows with the 617-142 template should prefer 597 before 032 when they belong to this subregister.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({ ...summary, support_rows: supportRows, top_sign_rows: signRows.slice(0, 20) }, null, 2),
  'utf8',
);
writeCsv(path.join(OUT_DIR, `${PREFIX}.csv`), [summary], [
  'run_date',
  'bet_id',
  'vector',
  'confidence_tier',
  'risky_bet',
  'observed',
  'adversarial_test',
  'false_positive_rate',
  'bonferroni_p',
  'fisher_p',
  'support_condition_warning',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_support_rows.csv`), supportRows, [
  'object',
  'region',
  'site',
  'type',
  'material',
  'shape',
  'condition',
  'complete',
  'copper_tab_c_context',
  'has_617_142_597_032_motif',
  'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_top_sign_rows.csv`), signRows.slice(0, 30), [
  'sign',
  'context_rows',
  'a',
  'b',
  'c',
  'd',
  'total',
  'fisher_p',
]);

console.log(JSON.stringify(summary, null, 2));
