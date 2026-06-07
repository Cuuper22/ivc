import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_407_rectangular_copper_register_forger_20260531';
const RUN_DATE = '2026-05-31';
const TARGET = '407';
const ITERATIONS = 3000;

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

function registerContext(row) {
  return norm(row.type) === 'SEAL:R' || norm(row.type) === 'TAB:C';
}

function analyzePool(name, poolRows, iterations = ITERATIONS) {
  const contextRows = poolRows.filter(registerContext);
  const backgroundRows = poolRows.filter((row) => !registerContext(row));
  const signs = [...new Set(poolRows.flatMap((row) => row.signs))].sort();
  const totalSignCounts = new Map(signs.map((sign) => [sign, poolRows.filter((row) => row.signSet.has(sign)).length]));
  const signRows = signs.map((sign) => {
    const a = contextRows.filter((row) => row.signSet.has(sign)).length;
    const c = totalSignCounts.get(sign) - a;
    const p = fisherRightTail(a, contextRows.length - a, c, backgroundRows.length - c);
    return {
      pool: name,
      sign,
      pool_rows: poolRows.length,
      context_rows: contextRows.length,
      a,
      b: contextRows.length - a,
      c,
      d: backgroundRows.length - c,
      total: a + c,
      fisher_p: p,
      bonferroni_p: Math.min(1, p * signs.length),
    };
  }).sort((x, y) => x.fisher_p - y.fisher_p || y.a - x.a || x.sign.localeCompare(y.sign, undefined, { numeric: true }));
  const target = signRows.find((row) => row.sign === TARGET);
  const rank = signRows.findIndex((row) => row.sign === TARGET) + 1;
  const rand = mulberry32(0x407444 ^ poolRows.length ^ contextRows.length ^ name.length);
  let maxGe = 0;
  for (let iter = 0; iter < iterations; iter += 1) {
    const chosen = new Set(sampleWithoutReplacement(rand, poolRows.length, contextRows.length));
    let best = 1;
    for (const sign of signs) {
      let a = 0;
      for (const idx of chosen) if (poolRows[idx].signSet.has(sign)) a += 1;
      const c = totalSignCounts.get(sign) - a;
      const p = fisherRightTail(a, contextRows.length - a, c, backgroundRows.length - c);
      if (p < best) best = p;
    }
    if (best <= target.fisher_p) maxGe += 1;
  }
  return {
    summary: {
      pool: name,
      pool_rows: poolRows.length,
      context_rows: contextRows.length,
      target_a: target.a,
      target_c: target.c,
      target_total: target.total,
      fisher_p: target.fisher_p,
      bonferroni_p: target.bonferroni_p,
      all_sign_rank: `${rank}/${signRows.length}`,
      maxstat_fpr: maxGe / iterations,
    },
    top_sign_rows: signRows.slice(0, 20),
  };
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()]
  .map((row, idx) => ({ ...row, _idx: idx, signSet: new Set(row.signs) }));

const pools = [
  analyzePool('all_canonical', canonicalRows),
  analyzePool('complete_only', canonicalRows.filter((row) => norm(row.complete) === 'Y')),
  analyzePool('non_poor_only', canonicalRows.filter((row) => norm(row.condition) !== 'Poor')),
  analyzePool('without_mohenjo_daro', canonicalRows.filter((row) => norm(row.site) !== 'Mohenjo-daro')),
  analyzePool('without_harappa', canonicalRows.filter((row) => norm(row.site) !== 'Harappa')),
  analyzePool('mohenjo_daro_only', canonicalRows.filter((row) => norm(row.site) === 'Mohenjo-daro')),
  analyzePool('harappa_only', canonicalRows.filter((row) => norm(row.site) === 'Harappa')),
];
const main = pools.find((pool) => pool.summary.pool === 'all_canonical').summary;
const complete = pools.find((pool) => pool.summary.pool === 'complete_only').summary;
const nonPoor = pools.find((pool) => pool.summary.pool === 'non_poor_only').summary;
const withoutMohenjo = pools.find((pool) => pool.summary.pool === 'without_mohenjo_daro').summary;
const withoutHarappa = pools.find((pool) => pool.summary.pool === 'without_harappa').summary;

const supportRows = canonicalRows.filter((row) => row.signSet.has(TARGET)).map((row) => ({
  object: objectId(row),
  region: norm(row.region),
  site: norm(row.site),
  type: norm(row.type),
  material: norm(row.material),
  shape: norm(row.shape),
  symbol: norm(row.symbol),
  condition: norm(row.condition),
  complete: norm(row.complete),
  register_context: String(registerContext(row)),
  text: row.text,
}));
const byType = Object.entries(supportRows.reduce((acc, row) => {
  acc[row.type] = (acc[row.type] ?? 0) + 1;
  return acc;
}, {})).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k}:${v}`).join(';');
const bySite = Object.entries(supportRows.reduce((acc, row) => {
  acc[row.site] = (acc[row.site] ?? 0) + 1;
  return acc;
}, {})).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k}:${v}`).join(';');

const tier =
  main.bonferroni_p <= 0.01 &&
  main.maxstat_fpr <= 0.01 &&
  complete.bonferroni_p <= 0.01 &&
  nonPoor.bonferroni_p <= 0.01 &&
  withoutMohenjo.bonferroni_p <= 0.01 &&
  withoutHarappa.bonferroni_p <= 0.01
    ? 'promoted candidate'
    : 'candidate';

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V4_407_RECTANGULAR_COPPER_REGISTER_20260531',
  vector: 'V4 context-to-meaning without sound',
  confidence_tier: tier,
  risky_bet:
    '`407` is not merely a copper sign; it marks a broader rectangular/copper administrative register spanning rectangular seals (`SEAL:R`) and copper tablets (`TAB:C`). This predicts carrier/register class only, not sound.',
  observed:
    `All canonical: ${main.target_a}/${main.context_rows} register rows vs ${main.target_c}/${main.pool_rows - main.context_rows} background, rank ${main.all_sign_rank}, Bonferroni=${main.bonferroni_p}, maxstat=${main.maxstat_fpr}. ` +
    `Complete-only: ${complete.target_a}/${complete.context_rows} vs ${complete.target_c}/${complete.pool_rows - complete.context_rows}, Bonferroni=${complete.bonferroni_p}. ` +
    `Non-poor-only: ${nonPoor.target_a}/${nonPoor.context_rows} vs ${nonPoor.target_c}/${nonPoor.pool_rows - nonPoor.context_rows}, Bonferroni=${nonPoor.bonferroni_p}. ` +
    `Without Mohenjo-daro: ${withoutMohenjo.target_a}/${withoutMohenjo.context_rows} vs ${withoutMohenjo.target_c}/${withoutMohenjo.pool_rows - withoutMohenjo.context_rows}, Bonferroni=${withoutMohenjo.bonferroni_p}. Without Harappa: ${withoutHarappa.target_a}/${withoutHarappa.context_rows} vs ${withoutHarappa.target_c}/${withoutHarappa.pool_rows - withoutHarappa.context_rows}, Bonferroni=${withoutHarappa.bonferroni_p}. Support by type: ${byType}. Support by site: ${bySite}.`,
  adversarial_test:
    `Canonical numeric-sequence collapse; all-sign Fisher rank; Bonferroni; ${ITERATIONS}-iteration max-stat context-label forger; complete-only and non-poor-only preservation controls; leave-Mohenjo and leave-Harappa site controls.`,
  false_positive_rate: Math.max(main.maxstat_fpr, complete.maxstat_fpr, nonPoor.maxstat_fpr, withoutMohenjo.maxstat_fpr, withoutHarappa.maxstat_fpr),
  main_bonferroni_p: main.bonferroni_p,
  complete_bonferroni_p: complete.bonferroni_p,
  non_poor_bonferroni_p: nonPoor.bonferroni_p,
  without_mohenjo_bonferroni_p: withoutMohenjo.bonferroni_p,
  without_harappa_bonferroni_p: withoutHarappa.bonferroni_p,
  falsifier:
    'If source-checked SEAL:R rows lose 407, or if non-register contexts accumulate 407 at comparable rates under the same leave-site controls, demote back to the narrower copper/TAB:C reading or kill the register reading entirely.',
  next_prediction:
    'Unverified rectangular seal rows should be enriched for 407 even outside Mohenjo-daro; unverified copper TAB:C rows should be enriched for 407 as the copper subtype of the same carrier/register family.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({ ...summary, pools: pools.map((pool) => pool.summary), support_rows: supportRows, top_sign_rows: pools[0].top_sign_rows }, null, 2),
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
  'main_bonferroni_p',
  'complete_bonferroni_p',
  'non_poor_bonferroni_p',
  'without_mohenjo_bonferroni_p',
  'without_harappa_bonferroni_p',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_pools.csv`), pools.map((pool) => pool.summary), [
  'pool',
  'pool_rows',
  'context_rows',
  'target_a',
  'target_c',
  'target_total',
  'fisher_p',
  'bonferroni_p',
  'all_sign_rank',
  'maxstat_fpr',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_support_rows.csv`), supportRows, [
  'object',
  'region',
  'site',
  'type',
  'material',
  'shape',
  'symbol',
  'condition',
  'complete',
  'register_context',
  'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_top_sign_rows.csv`), pools[0].top_sign_rows, [
  'pool',
  'sign',
  'pool_rows',
  'context_rows',
  'a',
  'b',
  'c',
  'd',
  'total',
  'fisher_p',
  'bonferroni_p',
]);

console.log(JSON.stringify(summary, null, 2));
