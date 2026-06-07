import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_400740_collision_register_order_forger_20260531';
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

function mulberry32(seed) {
  return function rand() {
    let t = (seed += 0x6D2B79F5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
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

function shuffle(values, rand) {
  const out = values.slice();
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function registerClass(row) {
  if (row.type === 'TAB:B' || row.type === 'TAB:I') return 'tablet_account';
  if (row.type === 'SEAL:R' || row.type === 'TAB:C') return 'rectangular_copper_admin';
  return 'other';
}

function orderOf(signs) {
  const i400 = signs.indexOf('400');
  const i740 = signs.indexOf('740');
  if (i400 < 0 || i740 < 0) return null;
  if (i400 < i740) return '400_before_740';
  if (i740 < i400) return '740_before_400';
  return 'same_position';
}

function score(rows, labels = null) {
  let tabletTotal = 0;
  let tabletHits = 0;
  let rectTotal = 0;
  let rectHits = 0;
  for (let i = 0; i < rows.length; i += 1) {
    const cls = labels ? labels[i] : rows[i].register_class;
    if (cls === 'tablet_account') {
      tabletTotal += 1;
      if (rows[i].order === '400_before_740') tabletHits += 1;
    } else if (cls === 'rectangular_copper_admin') {
      rectTotal += 1;
      if (rows[i].order === '740_before_400') rectHits += 1;
    }
  }
  return {
    tablet_total: tabletTotal,
    tablet_400_before_740: tabletHits,
    rect_total: rectTotal,
    rect_740_before_400: rectHits,
    aligned_hits: tabletHits + rectHits,
    aligned_total: tabletTotal + rectTotal,
  };
}

const raw = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({
  id: row.id,
  cisi: row.cisi || '-',
  site: norm(row.site),
  region: norm(row.region),
  type: norm(row.type),
  material: norm(row.material),
  shape: norm(row.shape),
  symbol: norm(row.symbol),
  condition: norm(row.condition),
  complete: norm(row.complete),
  text: row.text,
  signs: tokens(row.text),
}));

const canonical = [...new Map(raw.map((row) => [row.signs.join(' '), row])).values()]
  .filter((row) => row.signs.includes('400') && row.signs.includes('740'))
  .map((row) => ({
    ...row,
    order: orderOf(row.signs),
    register_class: registerClass(row),
  }))
  .filter((row) => row.order);

const focused = canonical.filter((row) => row.register_class !== 'other');
const observed = score(focused);
const labels = focused.map((row) => row.register_class);
const rand = mulberry32(0x400740);
let ge = 0;
for (let i = 0; i < ITERATIONS; i += 1) {
  const s = score(focused, shuffle(labels, rand));
  if (s.aligned_hits >= observed.aligned_hits) ge += 1;
}

const tablet = focused.filter((row) => row.register_class === 'tablet_account');
const rect = focused.filter((row) => row.register_class === 'rectangular_copper_admin');
const fisher = fisherRightTail(
  tablet.filter((row) => row.order === '400_before_740').length,
  tablet.filter((row) => row.order !== '400_before_740').length,
  rect.filter((row) => row.order === '400_before_740').length,
  rect.filter((row) => row.order !== '400_before_740').length,
);

const tier =
  observed.tablet_total >= 5 &&
  observed.rect_total >= 5 &&
  observed.tablet_400_before_740 / observed.tablet_total >= 0.8 &&
  observed.rect_740_before_400 / observed.rect_total >= 0.6 &&
  ge / ITERATIONS <= 0.01
    ? 'candidate'
    : 'wild shot';

const rows = canonical.map((row) => ({
  object: row.cisi !== '-' ? row.cisi : row.id,
  id: row.id,
  site: row.site,
  region: row.region,
  type: row.type,
  material: row.material,
  shape: row.shape,
  symbol: row.symbol,
  condition: row.condition,
  complete: row.complete,
  register_class: row.register_class,
  order: row.order,
  first_400_position: row.signs.indexOf('400'),
  first_740_position: row.signs.indexOf('740'),
  text: row.text,
}));

const byClass = ['tablet_account', 'rectangular_copper_admin', 'other'].map((cls) => {
  const classRows = canonical.filter((row) => row.register_class === cls);
  return {
    register_class: cls,
    rows: classRows.length,
    order_400_before_740: classRows.filter((row) => row.order === '400_before_740').length,
    order_740_before_400: classRows.filter((row) => row.order === '740_before_400').length,
  };
});

const report = {
  run_date: '2026-05-31T15:00:00-07:00',
  phase: 'EXPAND',
  bet_id: 'V2_V4_400740_COLLISION_REGISTER_ORDER_20260531',
  vector: 'V2 slot grammar + V4 context-to-meaning',
  confidence_tier: tier,
  risky_bet: '`400` and `740` are competing register openers whose collision order diagnoses carrier/register class: TAB:B/I account rows should prefer 400-before-740, while SEAL:R/TAB:C rectangular/copper administrative rows should prefer 740-before-400.',
  observed,
  observed_readable: `Focused 400+740 collision rows: tablet/account ${observed.tablet_400_before_740}/${observed.tablet_total} have 400-before-740; rectangular/copper admin ${observed.rect_740_before_400}/${observed.rect_total} have 740-before-400; aligned ${observed.aligned_hits}/${observed.aligned_total}.`,
  fisher_tablet_400_before_vs_rect_400_before_p: fisher,
  label_shuffle_false_positive_rate: ge / ITERATIONS,
  adversarial_test: 'Canonical numeric-sequence collapse; restrict to rows containing both 400 and 740; split only by pre-declared register classes TAB:B/I versus SEAL:R/TAB:C; shuffle register labels over collision rows while preserving row order/sign sequences.',
  falsifier: 'If either class has mixed collision order after source-checking, or if the aligned-order shuffle rate rises above 0.01 under leave-site controls, this hierarchy dies and 400/740 revert to independent context openers.',
  next_prediction: 'New TAB:B/I rows containing both 400 and 740 should usually start with 400 before 740; new SEAL:R/TAB:C rows containing both should more often put 740 before 400, except rows where 407 independently takes the opener slot.',
  by_class: byClass,
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
writeCsv(path.join(OUT_DIR, `${PREFIX}_rows.csv`), rows, [
  'object', 'id', 'site', 'region', 'type', 'material', 'shape', 'symbol', 'condition', 'complete',
  'register_class', 'order', 'first_400_position', 'first_740_position', 'text',
]);

console.log(JSON.stringify({
  confidence_tier: tier,
  observed: report.observed_readable,
  fisher_tablet_400_before_vs_rect_400_before_p: fisher,
  label_shuffle_false_positive_rate: ge / ITERATIONS,
  report: path.join(OUT_DIR, `${PREFIX}.json`),
}, null, 2));
