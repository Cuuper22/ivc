// Tests the bet that the sign sequence 002-861-096 marks an ivory-rod
// register: a class of inscription found on ivory ROD objects rather than
// ordinary seals. We read the filtered corpus metadata, collapse rows to one
// per canonical numeric sign sequence (so exact copies count once), then find
// every row containing 002-861-096 and count how many are ivory rods. The
// null: draw the same number of rows at random from all canonical 002-861
// rows, 100000 times, and see how often that many ivory rods appear by
// chance. The bet was demoted to wild shot because the two witnesses
// (M-2089/M-2090) collapse to a single canonical sequence. Writes a JSON
// report and two CSVs (bet summary, target rows) to the reports directory.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_861096_rod_register_20260531';
const RUN_DATE = '2026-05-31';
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
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`);
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function norm(value, fallback = 'NA') {
  const text = String(value ?? '').trim();
  return text && text !== '-' && text !== 'None' ? text : fallback;
}

function hasSeq(row, seq) {
  return row.signs.some((_, idx) => seq.every((sign, j) => row.signs[idx + j] === sign));
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

function isRodIvory(row) {
  return norm(row.type) === 'ROD' && norm(row.material) === 'Ivory';
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rows.map((row) => [row.signs.join(' '), row])).values()];
const all002861 = canonicalRows.filter((row) => hasSeq(row, ['002', '861']));
const target = canonicalRows.filter((row) => hasSeq(row, ['002', '861', '096']));

const observed = target.filter(isRodIvory).length;
const rand = mulberry32(0x861096);
let geObserved = 0;
for (let iter = 0; iter < ITERATIONS; iter += 1) {
  let score = 0;
  for (let i = 0; i < target.length; i += 1) if (isRodIvory(choose(rand, all002861))) score += 1;
  if (score >= observed) geObserved += 1;
}

const targets = target.map((row) => ({
  object: objectId(row),
  site: norm(row.site),
  type: norm(row.type),
  material: norm(row.material),
  symbol: norm(row.symbol),
  shape: norm(row.shape),
  text: row.text,
}));

const bet = {
  run_date: RUN_DATE,
  bet_id: 'V4_861096_IVORY_ROD_REGISTER_20260531',
  vector: 'V4 context-to-meaning from branch grammar',
  confidence_tier: target.length >= 2 && geObserved / ITERATIONS <= 0.01 ? 'candidate' : 'wild shot',
  risky_bet: '`002-861-096` is a terminal branch for an ivory-rod register inside the `002-861` branch table.',
  observed: `Canonical numeric-sequence target rows: ${target.length}; ivory ROD rows: ${observed}/${target.length}. Canonical 002-861 background: ${all002861.filter(isRodIvory).length}/${all002861.length} ivory ROD rows. The prior two exact-text witnesses collapse to one numeric sequence.`,
  adversarial_test: `Canonical numeric-sequence collapse, then shuffle inside all canonical 002-861 rows, ${ITERATIONS} iterations.`,
  false_positive_rate: geObserved / ITERATIONS,
  copy_family_warning: 'Demoted from candidate to wild shot: M-2089/M-2090 differ by bracket/damage text but share one canonical numeric sequence.',
  falsifier: 'A second independent source-normalized `002-861-096` row on a rod-like object revives the bet; a non-rod row kills the register reading.',
  next_prediction: 'If more `002-861-096` witnesses are found, they should be rod-like/minimal-object contexts and terminal rather than normal seal iconography.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), JSON.stringify({ ...bet, targets }, null, 2));
writeCsv(path.join(OUT_DIR, `${PREFIX}.csv`), [bet], [
  'run_date',
  'bet_id',
  'vector',
  'confidence_tier',
  'risky_bet',
  'observed',
  'adversarial_test',
  'false_positive_rate',
  'copy_family_warning',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_targets.csv`), targets, [
  'object',
  'site',
  'type',
  'material',
  'symbol',
  'shape',
  'text',
]);
console.log(JSON.stringify(bet, null, 2));
