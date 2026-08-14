// A "risky bet" forger test (2026-05-31): do external Indus-style objects split
// into two export registers? The bet: circular western seals carry the 090/091
// route pair, while non-circular external objects carry the internal
// administrative set 740/407/806/400 — two different document types leaving the
// Indus world by two lanes. The script reads the lipi metadata and the external
// objects table, collapses exact duplicate texts, splits external rows by
// circular/SEAL:C status, and counts hits for each sign set. The forger: 25000
// iterations that replace each external row with a random non-external row of
// the same object type, measuring how often chance matches the observed
// circular-route and non-circular-admin enrichments (separately and jointly).
// Grades itself candidate only with 10+ hits on each side and both
// false-positive rates at or below 0.01. Writes a JSON report and a support-row
// CSV listing every external row's sign hits.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const EXTERNAL = path.join(ROOT, 'data', 'meluhha', 'external_indus_objects.csv');
const OUT_DIR = path.join(ROOT, 'data', 'meluhha');
const PREFIX = 'risky_external_register_bifurcation_forger_20260531';
const ITERATIONS = 25000;
const ADMIN_SIGNS = new Set(['740', '407', '806', '400']);
const CIRCULAR_SIGNS = new Set(['090', '091']);

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

function isCircular(row) {
  return row.shape.toLowerCase() === 'circular' || row.type === 'SEAL:C';
}

function hit(row, set) {
  return row.signs.some((sign) => set.has(sign));
}

function mulberry32(seed) {
  return function rand() {
    let t = (seed += 0x6D2B79F5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function groupBy(rows, field) {
  const out = new Map();
  for (const row of rows) {
    if (!out.has(row[field])) out.set(row[field], []);
    out.get(row[field]).push(row);
  }
  return out;
}

function sampleLike(rows, backgroundByType, background, rand) {
  return rows.map((row) => {
    const pool = backgroundByType.get(row.type) ?? background;
    return pool[Math.floor(rand() * pool.length)];
  });
}

function score(rows) {
  return {
    rows: rows.length,
    admin_hits: rows.filter((row) => hit(row, ADMIN_SIGNS)).length,
    circular_hits: rows.filter((row) => hit(row, CIRCULAR_SIGNS)).length,
  };
}

const externalIds = new Set(parseCsv(fs.readFileSync(EXTERNAL, 'utf8')).map((row) => row.row_id));
const allRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({
  id: row.id,
  object: row.cisi && row.cisi !== '-' ? row.cisi : row.id,
  region: norm(row.region),
  site: norm(row.site),
  type: norm(row.type),
  material: norm(row.material),
  shape: norm(row.shape),
  symbol: norm(row.symbol),
  text: row.text,
  signs: tokens(row.text),
})).filter((row) => row.signs.length);

const canonical = [...new Map(allRows.map((row) => [row.signs.join(' '), row])).values()];
const externalRows = canonical.filter((row) => externalIds.has(row.id));
const backgroundRows = canonical.filter((row) => !externalIds.has(row.id));
const externalCircular = externalRows.filter(isCircular);
const externalNonCircular = externalRows.filter((row) => !isCircular(row));
const backgroundByType = groupBy(backgroundRows, 'type');
const observedCircular = score(externalCircular);
const observedNonCircular = score(externalNonCircular);

const rand = mulberry32(0xE740090);
let circularRouteGe = 0;
let nonCircularAdminGe = 0;
let bothGe = 0;
for (let i = 0; i < ITERATIONS; i += 1) {
  const fakeCircular = score(sampleLike(externalCircular, backgroundByType, backgroundRows, rand));
  const fakeNonCircular = score(sampleLike(externalNonCircular, backgroundByType, backgroundRows, rand));
  const routePass = fakeCircular.circular_hits >= observedCircular.circular_hits;
  const adminPass = fakeNonCircular.admin_hits >= observedNonCircular.admin_hits;
  if (routePass) circularRouteGe += 1;
  if (adminPass) nonCircularAdminGe += 1;
  if (routePass && adminPass) bothGe += 1;
}

const tier =
  observedCircular.circular_hits >= 10 &&
  observedNonCircular.admin_hits >= 10 &&
  circularRouteGe / ITERATIONS <= 0.01 &&
  nonCircularAdminGe / ITERATIONS <= 0.01
    ? 'candidate'
    : 'wild shot';

const supportRows = externalRows.map((row) => ({
  object: row.object,
  id: row.id,
  site: row.site,
  region: row.region,
  type: row.type,
  shape: row.shape,
  symbol: row.symbol,
  circular_class: String(isCircular(row)),
  admin_hit: String(hit(row, ADMIN_SIGNS)),
  route_hit_090091: String(hit(row, CIRCULAR_SIGNS)),
  admin_signs: row.signs.filter((sign) => ADMIN_SIGNS.has(sign)).join(' '),
  route_signs: row.signs.filter((sign) => CIRCULAR_SIGNS.has(sign)).join(' '),
  text: row.text,
}));

const report = {
  run_date: '2026-05-31T15:10:00-07:00',
  phase: 'EXPAND',
  bet_id: 'V1_V4_EXTERNAL_REGISTER_BIFURCATION_20260531',
  vector: 'V1 diffuse Meluhha bridge + V4 context-to-meaning',
  confidence_tier: tier,
  risky_bet: 'External Indus-style objects split into two export registers: circular western seals carry the 090/091 route-emulation pair, while non-circular external objects carry the internal administrative set 740/407/806/400.',
  observed: {
    external_circular: observedCircular,
    external_non_circular: observedNonCircular,
  },
  observed_readable: `External circular: 090/091 ${observedCircular.circular_hits}/${observedCircular.rows}, admin-set ${observedCircular.admin_hits}/${observedCircular.rows}. External non-circular: admin-set ${observedNonCircular.admin_hits}/${observedNonCircular.rows}, 090/091 ${observedNonCircular.circular_hits}/${observedNonCircular.rows}.`,
  circular_route_type_matched_fpr: circularRouteGe / ITERATIONS,
  non_circular_admin_type_matched_fpr: nonCircularAdminGe / ITERATIONS,
  joint_false_positive_rate: bothGe / ITERATIONS,
  adversarial_test: 'Exact-text canonical collapse; split external rows by circular/SEAL:C status; sample same-type non-external background rows for each external row; require both circular 090/091 enrichment and non-circular 740/407/806/400 enrichment.',
  falsifier: 'If non-circular external rows are not admin-sign enriched, the cuneiform register bridge prior cannot ride external objects generally. If circular rows lose 090/091 under source validation, the circular export branch also dies.',
  next_prediction: 'New non-circular external Indus-style objects should prefer 740/407/806/400; new circular Gulf/Dilmun objects should prefer 090/091 and often omit 740.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
writeCsv(path.join(OUT_DIR, `${PREFIX}_support_rows.csv`), supportRows, [
  'object', 'id', 'site', 'region', 'type', 'shape', 'symbol', 'circular_class',
  'admin_hit', 'route_hit_090091', 'admin_signs', 'route_signs', 'text',
]);

console.log(JSON.stringify({
  confidence_tier: tier,
  observed: report.observed_readable,
  circular_route_type_matched_fpr: report.circular_route_type_matched_fpr,
  non_circular_admin_type_matched_fpr: report.non_circular_admin_type_matched_fpr,
  joint_false_positive_rate: report.joint_false_positive_rate,
  report: path.join(OUT_DIR, `${PREFIX}.json`),
}, null, 2));
