import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const EXTERNAL = path.join(ROOT, 'data', 'meluhha', 'external_indus_objects.csv');
const OUT_DIR = path.join(ROOT, 'data', 'meluhha');
const PREFIX = 'risky_external_090_route_register_20260531';
const RUN_DATE = '2026-05-31';

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

function norm(value, fallback = 'NA') {
  const text = String(value ?? '').trim();
  return text && text !== '-' && text !== 'None' ? text : fallback;
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

function has090(row) {
  return tokens(row.text).includes('090');
}

function isCircular(row) {
  return norm(row.shape).toLowerCase() === 'circular' || norm(row.type).toUpperCase() === 'SEAL:C';
}

const externalCorridorRegions = new Set(['Persian Gulf', 'Mesopotamia', 'Iranian Plateau']);
const metadata = parseCsv(fs.readFileSync(META, 'utf8'));
const external = parseCsv(fs.readFileSync(EXTERNAL, 'utf8'));

const localCircular = metadata.filter(isCircular);
const mgsCircular = localCircular.filter((row) => externalCorridorRegions.has(norm(row.region)));
const otherCircular = localCircular.filter((row) => !externalCorridorRegions.has(norm(row.region)));
const externalCircular = external.filter(isCircular);
const externalNonCircular = external.filter((row) => !isCircular(row));

const mgsCirc090 = mgsCircular.filter(has090);
const otherCirc090 = otherCircular.filter(has090);
const extCirc090 = externalCircular.filter(has090);
const extNonCirc090 = externalNonCircular.filter(has090);

function brief(row) {
  return `${row.row_id ?? row.id}:${norm(row.site)}:${norm(row.type)}:${norm(row.shape)}:${row.text}`;
}

const mgsP = fisherRightTail(mgsCirc090.length, mgsCircular.length - mgsCirc090.length, otherCirc090.length, otherCircular.length - otherCirc090.length);
const externalP = fisherRightTail(extCirc090.length, externalCircular.length - extCirc090.length, extNonCirc090.length, externalNonCircular.length - extNonCirc090.length);
const positionScatter = mgsCirc090.map((row) => {
  const signs = tokens(row.text);
  const idx = signs.indexOf('090');
  return idx === 0 ? 'initial' : idx === signs.length - 1 ? 'terminal' : 'internal';
});
const positionCounts = Object.fromEntries([...new Set(positionScatter)].sort().map((pos) => [pos, positionScatter.filter((x) => x === pos).length]));

const bet = {
  run_date: RUN_DATE,
  bet_id: 'V1_EXTERNAL_090_ROUTE_REGISTER_20260531',
  vector: 'V1 diffuse Meluhha / Gulf external-contact bridge',
  confidence_tier: 'weak wild shot',
  risky_bet: '`090` marks a west-contact circular-seal route/register association, not a stable formula slot and not a phonetic value.',
  observed: `Persian Gulf/Mesopotamia/Iranian Plateau circular rows with 090: ${mgsCirc090.length}/${mgsCircular.length}; other local circular rows with 090: ${otherCirc090.length}/${otherCircular.length}; external circular rows with 090: ${extCirc090.length}/${externalCircular.length}; external non-circular rows with 090: ${extNonCirc090.length}/${externalNonCircular.length}; corridor circular 090 positions: ${JSON.stringify(positionCounts)}.`,
  adversarial_test: 'Fisher right-tail enrichment checks against other local circular seals and against external non-circular objects; slot-position scatter check kills the stronger formula-marker bet.',
  false_positive_rate: mgsP,
  external_shape_false_positive_rate: externalP,
  falsifier: 'Source-bound Failaka/Kjaerum rows 147.1 or 148.1 losing 090, or additional verified west-contact circular seals without 090 overwhelming the current enrichment, demotes the route/register bet.',
  next_prediction: 'Kjaerum 1983 Failaka cat. 279/319 should preserve 090 if the local rows 147.1/148.1 are correctly mapped; if source-bound mappings point elsewhere, the bet dies.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), JSON.stringify({
  ...bet,
  support_rows_mgs_circular_090: mgsCirc090.map(brief),
  external_circular_090: extCirc090.map(brief),
  external_circular_without_090: externalCircular.filter((row) => !has090(row)).map(brief),
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
  'external_shape_false_positive_rate',
  'falsifier',
  'next_prediction',
]);
console.log(JSON.stringify(bet, null, 2));
