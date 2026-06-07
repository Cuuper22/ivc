import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const EXTERNAL = path.join(ROOT, 'data', 'meluhha', 'external_indus_objects.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_090_pre740_external_edge_shift_forger_20260531';
const ITERATIONS = 50000;

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
  const logChoose = (nn, kk) => logFact[nn] - logFact[kk] - logFact[kk > nn ? 0 : nn - kk];
  const safeLogChoose = (nn, kk) => {
    if (kk < 0 || kk > nn) return Number.NEGATIVE_INFINITY;
    return logFact[nn] - logFact[kk] - logFact[nn - kk];
  };
  const row1 = a + b;
  const row2 = c + d;
  const col1 = a + c;
  const max = Math.min(row1, col1);
  const logDen = safeLogChoose(n, col1);
  let p = 0;
  for (let x = a; x <= max; x += 1) {
    p += Math.exp(safeLogChoose(row1, x) + safeLogChoose(row2, col1 - x) - logDen);
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

function shuffle(values, rand) {
  const out = values.slice();
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function isCircular(row) {
  return row.shape.toLowerCase() === 'circular' || row.type === 'SEAL:C';
}

function positionClass(signs, sign) {
  const idx = signs.indexOf(sign);
  if (idx < 0) return 'absent';
  if (idx === 0) return 'initial';
  if (idx === signs.length - 1) return 'terminal';
  if (idx === signs.length - 2) return 'near_terminal';
  return 'internal';
}

function nearEdge(signs, sign) {
  const cls = positionClass(signs, sign);
  return cls === 'initial' || cls === 'terminal' || cls === 'near_terminal';
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

const canonical = [...new Map(raw.map((row) => [row.signs.join(' '), row])).values()]
  .filter((row) => row.signs.length);
const local = canonical.filter((row) => !externalIds.has(row.id));
const external = canonical.filter((row) => externalIds.has(row.id));

const local090740 = local.filter((row) => row.signs.includes('090') && row.signs.includes('740'));
const local090Before740 = local090740.filter((row) => row.signs.indexOf('090') < row.signs.indexOf('740')).length;
const local090Rows = local.filter((row) => row.signs.includes('090'));
const externalCircular090Rows = external.filter((row) => isCircular(row) && row.signs.includes('090'));
const localNearEdge = local090Rows.filter((row) => nearEdge(row.signs, '090')).length;
const externalNearEdge = externalCircular090Rows.filter((row) => nearEdge(row.signs, '090')).length;

const rand = mulberry32(0x090740);
let directionGe = 0;
for (let i = 0; i < ITERATIONS; i += 1) {
  let hits = 0;
  for (const row of local090740) {
    const shuffled = shuffle(row.signs, rand);
    if (shuffled.indexOf('090') < shuffled.indexOf('740')) hits += 1;
  }
  if (hits >= local090Before740) directionGe += 1;
}

const edgeP = fisherRightTail(
  externalNearEdge,
  externalCircular090Rows.length - externalNearEdge,
  localNearEdge,
  local090Rows.length - localNearEdge,
);

const tier =
  local090740.length >= 40 &&
  local090Before740 / local090740.length >= 0.8 &&
  directionGe / ITERATIONS <= 0.01 &&
  externalCircular090Rows.length >= 5 &&
  externalNearEdge / externalCircular090Rows.length >= 0.5 &&
  edgeP <= 0.05
    ? 'candidate'
    : 'wild shot';

const supportRows = [
  ...local090740.map((row) => ({
    scope: 'local_090_740',
    object: row.object,
    id: row.id,
    site: row.site,
    region: row.region,
    type: row.type,
    shape: row.shape,
    symbol: row.symbol,
    position_class: positionClass(row.signs, '090'),
    order: row.signs.indexOf('090') < row.signs.indexOf('740') ? '090_before_740' : '740_before_090',
    text: row.text,
  })),
  ...externalCircular090Rows.map((row) => ({
    scope: 'external_circular_090',
    object: row.object,
    id: row.id,
    site: row.site,
    region: row.region,
    type: row.type,
    shape: row.shape,
    symbol: row.symbol,
    position_class: positionClass(row.signs, '090'),
    order: row.signs.includes('740') ? (row.signs.indexOf('090') < row.signs.indexOf('740') ? '090_before_740' : '740_before_090') : 'no_740',
    text: row.text,
  })),
];

const report = {
  run_date: '2026-05-31T15:05:00-07:00',
  phase: 'EXPAND',
  bet_id: 'V2_V4_V1_090_PRE740_EXTERNAL_EDGE_SHIFT_20260531',
  vector: 'V2 slot grammar + V4 context + V1 external-contact discriminator',
  confidence_tier: tier,
  risky_bet: '`090` is a pre-opener/register qualifier before `740` in local rows, but shifts toward the edge in external circular seals. This predicts function and copying/register behavior, not sound.',
  observed: {
    local_090_740_rows: local090740.length,
    local_090_before_740: local090Before740,
    local_090_before_740_share: local090740.length ? local090Before740 / local090740.length : null,
    external_circular_090_rows: externalCircular090Rows.length,
    external_circular_090_near_edge: externalNearEdge,
    external_circular_090_near_edge_share: externalCircular090Rows.length ? externalNearEdge / externalCircular090Rows.length : null,
    local_090_rows: local090Rows.length,
    local_090_near_edge: localNearEdge,
    local_090_near_edge_share: local090Rows.length ? localNearEdge / local090Rows.length : null,
  },
  direction_shuffle_false_positive_rate: directionGe / ITERATIONS,
  external_edge_vs_local_fisher_p: edgeP,
  adversarial_test: 'Canonical exact-text collapse; exclude known external rows for the local 090>740 test; row-internal sign shuffle preserving every local 090+740 row multiset; Fisher test for external circular 090 near-edge pressure against all local 090 rows.',
  falsifier: 'If source-visible external circular 090 rows are not edge/near-edge, or local 090+740 rows do not preserve 090-before-740 after source/copy-family collapse, demote to a generic 090+740 formula with no external position-shift claim.',
  next_prediction: 'New local 090+740 rows should usually place 090 before 740; new external circular 090 rows should often put 090 at an edge or near-edge and should not need 740 to carry the route/register function.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
writeCsv(path.join(OUT_DIR, `${PREFIX}_support_rows.csv`), supportRows, [
  'scope', 'object', 'id', 'site', 'region', 'type', 'shape', 'symbol', 'position_class', 'order', 'text',
]);

console.log(JSON.stringify({
  confidence_tier: tier,
  observed: report.observed,
  direction_shuffle_false_positive_rate: report.direction_shuffle_false_positive_rate,
  external_edge_vs_local_fisher_p: report.external_edge_vs_local_fisher_p,
  report: path.join(OUT_DIR, `${PREFIX}.json`),
}, null, 2));
