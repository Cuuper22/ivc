// Tests the bet that the sign sequence 002-861-533-717 marks an aniconic
// register: inscriptions on rectangular seals (SEAL:R) that carry no animal
// symbol, inside the wider 002-861 branch table. We read the filtered corpus
// metadata, collapse rows to one per exact text, find every row containing
// the full four-sign sequence, and count how many are symbol-free rectangular
// seals (and how many are symbol-free at all). The null: draw the same number
// of rows at random from all exact-collapsed 002-861 rows, 100000 times, and
// see how often those counts appear by chance. The bet stays wild-shot tier
// by construction; the report records falsifiers and predictions. Writes a
// JSON report and two CSVs (bet summary, target rows).
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_861533_register_context_20260531';
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

const rows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));

function hasSeq(row, seq) {
  return row.signs.some((_, idx) => seq.every((sign, j) => row.signs[idx + j] === sign));
}

function isNoSymbolRect(row) {
  return String(row.type).startsWith('SEAL:R') && norm(row.symbol) === 'NA';
}

function isNoSymbol(row) {
  return norm(row.symbol) === 'NA';
}

const target = rows.filter((row) => hasSeq(row, ['002', '861', '533', '717']));
const all002861 = rows.filter((row) => hasSeq(row, ['002', '861']));
const all002861Exact = [...new Map(all002861.map((row) => [row.text, row])).values()];
const targetExact = [...new Map(target.map((row) => [row.text, row])).values()];
const nonTarget002861 = all002861Exact.filter((row) => !hasSeq(row, ['002', '861', '533', '717']));

const rand = mulberry32(0x861533);
let geRect = 0;
let geNoSymbol = 0;
for (let iter = 0; iter < ITERATIONS; iter += 1) {
  let rect = 0;
  let noSymbol = 0;
  for (let i = 0; i < targetExact.length; i += 1) {
    const sampled = choose(rand, all002861Exact);
    if (isNoSymbolRect(sampled)) rect += 1;
    if (isNoSymbol(sampled)) noSymbol += 1;
  }
  if (rect >= targetExact.filter(isNoSymbolRect).length) geRect += 1;
  if (noSymbol >= targetExact.filter(isNoSymbol).length) geNoSymbol += 1;
}

const bet = {
  run_date: RUN_DATE,
  bet_id: 'V4_861533_ANICONIC_REGISTER_CONTEXT_20260531',
  vector: 'V4 context-to-meaning from branch grammar',
  confidence_tier: 'wild shot',
  risky_bet: '`002-861-533-717` is not only a restricted structural tail; it marks an aniconic rectangular-seal register within the `002-861` table.',
  observed: `Target exact rows ${targetExact.length}: ${targetExact.filter(isNoSymbolRect).length}/${targetExact.length} are SEAL:R with no symbol, ${targetExact.filter(isNoSymbol).length}/${targetExact.length} no-symbol. Background exact ` + 
    `002-861 rows ${all002861Exact.length}: ${all002861Exact.filter(isNoSymbolRect).length}/${all002861Exact.length} SEAL:R no-symbol, ${all002861Exact.filter(isNoSymbol).length}/${all002861Exact.length} no-symbol.`,
  adversarial_test: `Exact-text-collapsed shuffle within all 002-861 rows, ${ITERATIONS} iterations.`,
  false_positive_rate: geRect / ITERATIONS,
  no_symbol_false_positive_rate: geNoSymbol / ITERATIONS,
  falsifier: 'A source-normalized third `002-861-533-717` row with animal iconography, or proof that M-376/M-391 are one copied object family, kills the context bet while leaving the structural tail candidate alive.',
  next_prediction: 'Future independent `002-861-533-717` witnesses should be aniconic rectangular/cuboid-convex seals more often than ordinary 002-861 rows.',
};

const targetRows = targetExact.map((row) => ({
  object: objectId(row),
  site: norm(row.site),
  type: norm(row.type),
  symbol: norm(row.symbol),
  shape: norm(row.shape),
  material: norm(row.material),
  text: row.text,
}));

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), JSON.stringify({
  ...bet,
  target_rows: targetRows,
  non_target_002861_examples: nonTarget002861.slice(0, 30).map((row) => `${objectId(row)}:${norm(row.type)}:${norm(row.symbol)}:${row.text}`),
}, null, 2));
writeCsv(path.join(OUT_DIR, `${PREFIX}.csv`), [bet], [
  'run_date',
  'bet_id',
  'vector',
  'confidence_tier',
  'risky_bet',
  'observed',
  'adversarial_test',
  'false_positive_rate',
  'no_symbol_false_positive_rate',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_targets.csv`), targetRows, [
  'object',
  'site',
  'type',
  'symbol',
  'shape',
  'material',
  'text',
]);
console.log(JSON.stringify(bet, null, 2));
