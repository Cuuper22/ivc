// A "risky bet" probe (2026-05-31): do signs 090 and 091 split the external
// circular-seal corpus into two mutually exclusive route lanes? The bet, which
// predicts context class and never sound: 090 marks the Failaka/Bahrain/Susa/Ur
// lane, 091 a Karzakan/Saar/Kalba-plus-Luristan branch, and no seal carries
// both. The script reads the lipi metadata and external objects table, counts
// 090/091/either/both on external circular vs non-circular rows and on corridor
// (Persian Gulf, Mesopotamia, Iranian Plateau) circular vs other local circular
// rows, and builds a per-site split table. Two one-sided Fisher exact tests
// give the enrichment false-positive rates. The bet self-grades: "candidate"
// only if both-signs count is zero, at least 10 either-sign rows exist, and
// both Fisher rates are at or below 0.01; otherwise "wild shot". Writes a JSON
// bet record with row lists, a one-row summary CSV, and the by-site CSV.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const EXTERNAL = path.join(ROOT, 'data', 'meluhha', 'external_indus_objects.csv');
const OUT_DIR = path.join(ROOT, 'data', 'meluhha');
const PREFIX = 'risky_external_090091_circular_route_split_20260531';
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
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`, 'utf8');
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function norm(value, fallback = 'NA') {
  const text = String(value ?? '').trim();
  return text && text !== '-' && text !== 'None' ? text : fallback;
}

function isCircular(row) {
  return norm(row.shape).toLowerCase() === 'circular' || norm(row.type).toUpperCase() === 'SEAL:C';
}

function has(row, sign) {
  return tokens(row.text).includes(sign);
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

function brief(row) {
  return `${row.row_id ?? row.id}:${norm(row.site)}:${norm(row.region)}:${norm(row.type)}:${norm(row.shape)}:${row.text}`;
}

const metadata = parseCsv(fs.readFileSync(META, 'utf8'));
const external = parseCsv(fs.readFileSync(EXTERNAL, 'utf8'));
const externalCircular = external.filter(isCircular);
const externalNonCircular = external.filter((row) => !isCircular(row));
const localCircular = metadata.filter(isCircular);
const corridorRegions = new Set(['Persian Gulf', 'Mesopotamia', 'Iranian Plateau']);
const corridorCircular = localCircular.filter((row) => corridorRegions.has(norm(row.region)));
const otherCircular = localCircular.filter((row) => !corridorRegions.has(norm(row.region)));

const extCirc090 = externalCircular.filter((row) => has(row, '090'));
const extCirc091 = externalCircular.filter((row) => has(row, '091'));
const extCircEither = externalCircular.filter((row) => has(row, '090') || has(row, '091'));
const extCircBoth = externalCircular.filter((row) => has(row, '090') && has(row, '091'));
const extNonCircEither = externalNonCircular.filter((row) => has(row, '090') || has(row, '091'));
const corridorEither = corridorCircular.filter((row) => has(row, '090') || has(row, '091'));
const otherEither = otherCircular.filter((row) => has(row, '090') || has(row, '091'));

const bySite = [...new Set(externalCircular.map((row) => norm(row.site)))].sort().map((site) => {
  const rows = externalCircular.filter((row) => norm(row.site) === site);
  return {
    site,
    rows: rows.length,
    has_090: rows.filter((row) => has(row, '090')).length,
    has_091: rows.filter((row) => has(row, '091')).length,
    has_either: rows.filter((row) => has(row, '090') || has(row, '091')).length,
    examples: rows.map(brief).join(' | '),
  };
});

const externalEitherP = fisherRightTail(
  extCircEither.length,
  externalCircular.length - extCircEither.length,
  extNonCircEither.length,
  externalNonCircular.length - extNonCircEither.length,
);
const corridorEitherP = fisherRightTail(
  corridorEither.length,
  corridorCircular.length - corridorEither.length,
  otherEither.length,
  otherCircular.length - otherEither.length,
);

const tier =
  extCircBoth.length === 0 &&
  extCircEither.length >= 10 &&
  externalEitherP <= 0.01 &&
  corridorEitherP <= 0.01
    ? 'candidate'
    : 'wild shot';

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V1_EXTERNAL_090091_CIRCULAR_ROUTE_SPLIT_20260531',
  vector: 'V1 diffuse Meluhha / Gulf external-contact bridge',
  confidence_tier: tier,
  risky_bet:
    '`090` and `091` behave as a mutually exclusive external circular-seal route/register pair. This predicts context class, not sound: `090` covers the Failaka/Bahrain/Susa/Ur lane; `091` covers a Karzakan/Saar/Kalba plus Luristan Gulf-adjacent circular branch.',
  observed:
    `External circular rows=${externalCircular.length}; 090=${extCirc090.length}; 091=${extCirc091.length}; either=${extCircEither.length}; both=${extCircBoth.length}. ` +
    `External non-circular either=${extNonCircEither.length}/${externalNonCircular.length}. Corridor circular either=${corridorEither.length}/${corridorCircular.length}; other circular either=${otherEither.length}/${otherCircular.length}.`,
  adversarial_test:
    'Fisher right-tail enrichment of {090,091} in external circular versus external non-circular, and in corridor circular versus other local circular; mutual-exclusion check inside external circular rows; site split table.',
  false_positive_rate: externalEitherP,
  corridor_false_positive_rate: corridorEitherP,
  falsifier:
    'Any source-bound external circular row containing both 090 and 091 weakens the split; several verified external circular rows lacking both signs weakens the route-register reading; a non-circular external concentration of either sign kills circular specificity.',
  next_prediction:
    'New Failaka/Bahrain/Susa/Ur circular seal rows should prefer 090, while Karzakan/Saar/Kalba/Luristan-style circular rows should prefer 091; neither sign should be read phonetically from this result.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({
    ...summary,
    external_circular_090: extCirc090.map(brief),
    external_circular_091: extCirc091.map(brief),
    external_circular_neither: externalCircular.filter((row) => !has(row, '090') && !has(row, '091')).map(brief),
    by_site: bySite,
  }, null, 2),
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
  'corridor_false_positive_rate',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_by_site.csv`), bySite, ['site', 'rows', 'has_090', 'has_091', 'has_either', 'examples']);

console.log(JSON.stringify(summary, null, 2));
