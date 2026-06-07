import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const EXTERNAL = path.join(ROOT, 'data', 'meluhha', 'external_indus_objects.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_090_external_740_deletion_forger_20260531';

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

function fisherRightTail(a, b, c, d) {
  const logFact = [0];
  const n = a + b + c + d;
  for (let i = 1; i <= n; i += 1) logFact[i] = logFact[i - 1] + Math.log(i);
  const logChoose = (nn, kk) => {
    if (kk < 0 || kk > nn) return Number.NEGATIVE_INFINITY;
    return logFact[nn] - logFact[kk] - logFact[nn - kk];
  };
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

function isCircular(row) {
  return row.shape.toLowerCase() === 'circular' || row.type === 'SEAL:C';
}

const externalIds = new Set(parseCsv(fs.readFileSync(EXTERNAL, 'utf8')).map((row) => row.row_id));
const raw = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({
  id: row.id,
  object: row.cisi && row.cisi !== '-' ? row.cisi : row.id,
  region: norm(row.region),
  site: norm(row.site),
  type: norm(row.type),
  shape: norm(row.shape),
  symbol: norm(row.symbol),
  condition: norm(row.condition),
  complete: norm(row.complete),
  text: row.text,
  signs: tokens(row.text),
}));
const canonical = [...new Map(raw.map((row) => [row.signs.join(' '), row])).values()].filter((row) => row.signs.length);
const local090 = canonical.filter((row) => !externalIds.has(row.id) && row.signs.includes('090'));
const externalCircular090 = canonical.filter((row) => externalIds.has(row.id) && isCircular(row) && row.signs.includes('090'));

const localWith740 = local090.filter((row) => row.signs.includes('740')).length;
const externalWith740 = externalCircular090.filter((row) => row.signs.includes('740')).length;
const p = fisherRightTail(
  localWith740,
  local090.length - localWith740,
  externalWith740,
  externalCircular090.length - externalWith740,
);

const tier =
  local090.length >= 50 &&
  externalCircular090.length >= 5 &&
  localWith740 / local090.length >= 0.5 &&
  externalWith740 === 0 &&
  p <= 0.05
    ? 'candidate'
    : 'wild shot';

const report = {
  run_date: '2026-05-31T15:07:00-07:00',
  phase: 'EXPAND',
  bet_id: 'V1_V2_090_EXTERNAL_740_DELETION_20260531',
  vector: 'V1 external-contact discriminator + V2 slot grammar',
  confidence_tier: tier,
  risky_bet: 'External circular `090` rows preserve the local pre-740 register marker but drop the normal `740` continuation. This predicts a western abbreviated/copying register, not a new phonetic value.',
  observed: {
    local_090_rows: local090.length,
    local_090_with_740: localWith740,
    local_090_with_740_share: local090.length ? localWith740 / local090.length : null,
    external_circular_090_rows: externalCircular090.length,
    external_circular_090_with_740: externalWith740,
    external_circular_090_with_740_share: externalCircular090.length ? externalWith740 / externalCircular090.length : null,
  },
  fisher_local_090_has_740_vs_external_has_740_p: p,
  adversarial_test: 'Canonical exact-text collapse; compare local 090 rows against external circular 090 rows; one-sided Fisher asks whether local 090 retains 740 far more than the external circular 090 branch.',
  falsifier: 'Source-validated external circular 090 rows containing 740 at local-like rates kill the deletion model. Local source collapse that removes the 090-740 association also kills it.',
  next_prediction: 'New source-bound external circular 090 rows should usually lack 740, while local non-external 090 rows should often keep 740 immediately or soon after 090.',
};

const support = [
  ...local090.map((row) => ({
    scope: 'local_090',
    object: row.object,
    id: row.id,
    site: row.site,
    region: row.region,
    type: row.type,
    shape: row.shape,
    has_740: String(row.signs.includes('740')),
    text: row.text,
  })),
  ...externalCircular090.map((row) => ({
    scope: 'external_circular_090',
    object: row.object,
    id: row.id,
    site: row.site,
    region: row.region,
    type: row.type,
    shape: row.shape,
    has_740: String(row.signs.includes('740')),
    text: row.text,
  })),
];

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
writeCsv(path.join(OUT_DIR, `${PREFIX}_support_rows.csv`), support, [
  'scope', 'object', 'id', 'site', 'region', 'type', 'shape', 'has_740', 'text',
]);

console.log(JSON.stringify({
  confidence_tier: tier,
  observed: report.observed,
  fisher_local_090_has_740_vs_external_has_740_p: p,
  report: path.join(OUT_DIR, `${PREFIX}.json`),
}, null, 2));
