// Tests whether sign `091` is tied to a specific object class: circular seals
// (shape "circular" or type SEAL:C / SEAL:CY). The bet claims nothing about sound —
// only that 091 concentrates on round-seal objects, which would mark it as a
// register or context sign. The script reads metadata_filtered.csv, collapses
// duplicate sign sequences, and measures the circular-seal share of rows containing
// 091 against all other rows with a right-tail Fisher test. Two adversaries guard
// the result: a 100,000-iteration forger that redraws the same number of rows at
// random from the corpus and asks how often they are this circular, and a rank
// comparison against every other sign — especially signs of comparable frequency
// (between half and twice 091's row count). Writes a bet summary (JSON + CSV),
// support rows, and the full per-sign circular table to the reports directory.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_091_circular_seal_context_forger_20260531';
const RUN_DATE = '2026-05-31';
const TARGET = '091';
const ITERATIONS = 100000;

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
  return text && text !== '-' && text !== 'None' ? text : fallback;
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function isStrictCircularSeal(row) {
  return norm(row.shape).toLowerCase() === 'circular' || ['SEAL:C', 'SEAL:CY'].includes(norm(row.type).toUpperCase());
}

function fisherRightTail(a, b, c, d) {
  const logFact = [0];
  const n = a + b + c + d;
  for (let i = 1; i <= n; i += 1) logFact[i] = logFact[i - 1] + Math.log(i);
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

function choose(rand, arr) {
  return arr[Math.floor(rand() * arr.length)];
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()];
const targetRows = canonicalRows.filter((row) => row.signs.includes(TARGET));
const targetCircular = targetRows.filter(isStrictCircularSeal);
const nonTargetRows = canonicalRows.filter((row) => !row.signs.includes(TARGET));
const nonTargetCircular = nonTargetRows.filter(isStrictCircularSeal);

const signRows = new Map();
for (const row of canonicalRows) {
  for (const sign of new Set(row.signs)) {
    if (!signRows.has(sign)) signRows.set(sign, []);
    signRows.get(sign).push(row);
  }
}

const signTable = [...signRows.entries()].map(([sign, rows]) => ({
  sign,
  rows: rows.length,
  circular_rows: rows.filter(isStrictCircularSeal).length,
  circular_share: rows.filter(isStrictCircularSeal).length / rows.length,
  examples: rows.filter(isStrictCircularSeal).slice(0, 8).map((row) => `${objectId(row)}:${row.site}:${row.type}:${row.shape}:${row.text}`).join(' | '),
})).sort((a, b) => b.circular_rows - a.circular_rows || b.circular_share - a.circular_share || a.sign.localeCompare(b.sign, undefined, { numeric: true }));

const targetStats = signTable.find((row) => row.sign === TARGET);
const comparable = signTable.filter((row) => row.rows >= targetStats.rows / 2 && row.rows <= targetStats.rows * 2);
const comparableGe = comparable.filter((row) => row.circular_rows >= targetStats.circular_rows && row.sign !== TARGET);
const allGe = signTable.filter((row) => row.circular_rows >= targetStats.circular_rows && row.sign !== TARGET);

const rand = mulberry32(0x0912026);
let geRandomRows = 0;
for (let iter = 0; iter < ITERATIONS; iter += 1) {
  let score = 0;
  for (let i = 0; i < targetRows.length; i += 1) {
    if (isStrictCircularSeal(choose(rand, canonicalRows))) score += 1;
  }
  if (score >= targetCircular.length) geRandomRows += 1;
}

const fisherP = fisherRightTail(
  targetCircular.length,
  targetRows.length - targetCircular.length,
  nonTargetCircular.length,
  nonTargetRows.length - nonTargetCircular.length,
);
const comparableRank = `${comparable.filter((row) => row.circular_rows >= targetStats.circular_rows).length}/${comparable.length}`;
const allRank = `${signTable.filter((row) => row.circular_rows >= targetStats.circular_rows).length}/${signTable.length}`;
const tier = fisherP <= 0.01 && geRandomRows / ITERATIONS <= 0.01 && comparableGe.length <= 2 ? 'candidate' : 'wild shot';

const supportRows = targetRows.map((row) => ({
  object: objectId(row),
  region: norm(row.region),
  site: norm(row.site),
  type: norm(row.type),
  shape: norm(row.shape),
  material: norm(row.material),
  symbol: norm(row.symbol),
  circular_seal_context: String(isStrictCircularSeal(row)),
  text: row.text,
}));

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V4_091_CIRCULAR_SEAL_CONTEXT_20260531',
  vector: 'V4 context-to-meaning without sound',
  confidence_tier: tier,
  risky_bet:
    '`091` carries circular-seal / round-seal register load. This predicts object/register context only: `091` should appear disproportionately on SEAL:C/SEAL:CY or circular-shape objects.',
  observed:
    `Canonical rows=${canonicalRows.length}; target rows=${targetRows.length}; target circular-seal rows=${targetCircular.length}/${targetRows.length}; background circular-seal rows=${nonTargetCircular.length}/${nonTargetRows.length}. Frequency-comparable signs >= target circular count: ${comparableGe.map((row) => `${row.sign}:${row.rows}/${row.circular_rows}`).join(';') || 'none'}.`,
  adversarial_test:
    `Canonical numeric-sequence collapse; Fisher right-tail target-vs-background; random-row forger preserving target row count (${ITERATIONS}); frequency-comparable all-sign rank.`,
  false_positive_rate: fisherP,
  random_row_false_positive_rate: geRandomRows / ITERATIONS,
  all_sign_rank: allRank,
  frequency_comparable_rank: comparableRank,
  falsifier:
    'Several new source-bound non-circular 091 rows, or frequency-matched signs with equal circular concentration after source review, demote the circular-register reading.',
  next_prediction:
    'Unverified or future 091-bearing objects should skew toward circular seal, cylinder seal, or external Gulf circular registers; the result does not license a sound value.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({ ...summary, target_stats: targetStats, comparable_ge: comparableGe, all_ge: allGe, support_rows: supportRows, sign_table: signTable }, null, 2),
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
  'random_row_false_positive_rate',
  'all_sign_rank',
  'frequency_comparable_rank',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_support_rows.csv`), supportRows, [
  'object',
  'region',
  'site',
  'type',
  'shape',
  'material',
  'symbol',
  'circular_seal_context',
  'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_sign_table.csv`), signTable, ['sign', 'rows', 'circular_rows', 'circular_share', 'examples']);

console.log(JSON.stringify(summary, null, 2));
