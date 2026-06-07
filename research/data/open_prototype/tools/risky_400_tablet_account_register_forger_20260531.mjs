import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_400_tablet_account_register_forger_20260531';
const RUN_DATE = '2026-05-31';
const TARGET = '400';
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

function shuffleInPlace(arr, rand) {
  for (let i = arr.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    const tmp = arr[i];
    arr[i] = arr[j];
    arr[j] = tmp;
  }
}

function tabletAccountContext(row) {
  return ['TAB:B', 'TAB:I'].includes(norm(row.type));
}

function occurrenceRows(rows) {
  const occs = [];
  for (const row of rows) {
    for (let idx = 0; idx < row.signs.length; idx += 1) {
      occs.push({ sign: row.signs[idx], initial: idx === 0, row });
    }
  }
  return occs;
}

function analyzeContextPool(name, poolRows, iterations = ITERATIONS) {
  const contextRows = poolRows.filter(tabletAccountContext);
  const backgroundRows = poolRows.filter((row) => !tabletAccountContext(row));
  const signs = [...new Set(poolRows.flatMap((row) => row.signs))].sort();
  const signHits = new Map(signs.map((sign) => [sign, poolRows.map((row) => row.signSet.has(sign))]));
  const totalSignCounts = new Map(signs.map((sign) => [sign, signHits.get(sign).filter(Boolean).length]));
  const signRows = signs.map((sign) => {
    const hits = signHits.get(sign);
    let a = 0;
    let c = 0;
    for (let i = 0; i < poolRows.length; i += 1) {
      if (!hits[i]) continue;
      if (tabletAccountContext(poolRows[i])) a += 1;
      else c += 1;
    }
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
      context_share: a / Math.max(1, a + c),
      fisher_p: p,
      bonferroni_p: Math.min(1, p * signs.length),
    };
  }).sort((x, y) => x.fisher_p - y.fisher_p || y.a - x.a || x.sign.localeCompare(y.sign, undefined, { numeric: true }));
  const target = signRows.find((row) => row.sign === TARGET);
  const rank = signRows.findIndex((row) => row.sign === TARGET) + 1;
  const rand = mulberry32(0x400acc ^ poolRows.length ^ contextRows.length ^ name.length);
  let maxGe = 0;
  for (let iter = 0; iter < iterations; iter += 1) {
    const chosen = new Set(sampleWithoutReplacement(rand, poolRows.length, contextRows.length));
    let best = 1;
    for (const sign of signs) {
      const hits = signHits.get(sign);
      let a = 0;
      for (const idx of chosen) if (hits[idx]) a += 1;
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
      target_context_share: target.context_share,
      fisher_p: target.fisher_p,
      bonferroni_p: target.bonferroni_p,
      all_sign_rank: `${rank}/${signs.length}`,
      maxstat_fpr: maxGe / iterations,
    },
    top_sign_rows: signRows.slice(0, 25),
  };
}

function analyzeInitialPool(name, rows, iterations = ITERATIONS) {
  const occs = occurrenceRows(rows);
  const signs = [...new Set(occs.map((occ) => occ.sign))].sort();
  const signCounts = new Map();
  for (const occ of occs) signCounts.set(occ.sign, (signCounts.get(occ.sign) ?? 0) + 1);
  const totalInitial = occs.filter((occ) => occ.initial).length;
  const signRows = signs.map((sign) => {
    const local = occs.filter((occ) => occ.sign === sign);
    const a = local.filter((occ) => occ.initial).length;
    const c = totalInitial - a;
    const p = fisherRightTail(a, local.length - a, c, occs.length - local.length - c);
    return {
      pool: name,
      sign,
      occurrences: local.length,
      initial: a,
      initial_share: a / local.length,
      background_initial: c,
      background_occurrences: occs.length - local.length,
      fisher_p: p,
      bonferroni_p: Math.min(1, p * signs.length),
    };
  }).sort((x, y) => x.fisher_p - y.fisher_p || y.initial_share - x.initial_share || x.sign.localeCompare(y.sign, undefined, { numeric: true }));
  const target = signRows.find((row) => row.sign === TARGET);
  const rank = signRows.findIndex((row) => row.sign === TARGET) + 1;
  const labels = occs.map((occ) => occ.sign);
  const rand = mulberry32(0x400111 ^ rows.length ^ occs.length ^ name.length);
  const shuffled = labels.slice();
  let maxGe = 0;
  for (let iter = 0; iter < iterations; iter += 1) {
    shuffleInPlace(shuffled, rand);
    const counts = new Map(signs.map((sign) => [sign, { total: signCounts.get(sign), initial: 0 }]));
    for (let i = 0; i < shuffled.length; i += 1) {
      if (occs[i].initial) counts.get(shuffled[i]).initial += 1;
    }
    let best = 1;
    for (const [sign, count] of counts.entries()) {
      const a = count.initial;
      const c = totalInitial - a;
      const p = fisherRightTail(a, count.total - a, c, occs.length - count.total - c);
      if (p < best) best = p;
    }
    if (best <= target.fisher_p) maxGe += 1;
  }
  return {
    summary: {
      pool: name,
      rows: rows.length,
      occurrences: occs.length,
      target_occurrences: target.occurrences,
      target_initial: target.initial,
      target_initial_share: target.initial_share,
      fisher_p: target.fisher_p,
      bonferroni_p: target.bonferroni_p,
      all_sign_rank: `${rank}/${signs.length}`,
      maxstat_fpr: maxGe / iterations,
    },
    top_initial_rows: signRows.slice(0, 25),
  };
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()]
  .map((row, idx) => ({ ...row, _idx: idx, signSet: new Set(row.signs) }));

const contextPools = [
  analyzeContextPool('all_canonical', canonicalRows),
  analyzeContextPool('complete_only', canonicalRows.filter((row) => norm(row.complete) === 'Y')),
  analyzeContextPool('non_poor_only', canonicalRows.filter((row) => norm(row.condition) !== 'Poor')),
  analyzeContextPool('without_harappa', canonicalRows.filter((row) => norm(row.site) !== 'Harappa')),
  analyzeContextPool('without_mohenjo_daro', canonicalRows.filter((row) => norm(row.site) !== 'Mohenjo-daro')),
  analyzeContextPool('harappa_only', canonicalRows.filter((row) => norm(row.site) === 'Harappa')),
  analyzeContextPool('mohenjo_daro_only', canonicalRows.filter((row) => norm(row.site) === 'Mohenjo-daro')),
];
const accountRows = canonicalRows.filter(tabletAccountContext);
const initialPools = [
  analyzeInitialPool('tablet_account_rows_only', accountRows),
  analyzeInitialPool('tablet_account_complete_only', accountRows.filter((row) => norm(row.complete) === 'Y')),
  analyzeInitialPool('tablet_account_non_poor_only', accountRows.filter((row) => norm(row.condition) !== 'Poor')),
  analyzeInitialPool('tablet_account_without_harappa', accountRows.filter((row) => norm(row.site) !== 'Harappa')),
];

const main = contextPools[0].summary;
const complete = contextPools[1].summary;
const nonPoor = contextPools[2].summary;
const withoutHarappa = contextPools[3].summary;
const withoutMohenjo = contextPools[4].summary;
const initialMain = initialPools[0].summary;
const supportRows = canonicalRows.filter((row) => row.signSet.has(TARGET)).map((row) => ({
  object: objectId(row),
  site: norm(row.site),
  region: norm(row.region),
  type: norm(row.type),
  material: norm(row.material),
  shape: norm(row.shape),
  symbol: norm(row.symbol),
  condition: norm(row.condition),
  complete: norm(row.complete),
  tablet_account_context: String(tabletAccountContext(row)),
  first_sign: row.signs[0] ?? '',
  target_initial: String(row.signs[0] === TARGET),
  text: row.text,
}));

function groupCounts(rows, field) {
  return Object.entries(rows.reduce((acc, row) => {
    acc[row[field]] = (acc[row[field]] ?? 0) + 1;
    return acc;
  }, {})).sort((a, b) => b[1] - a[1]).map(([key, value]) => `${key}:${value}`).join(';');
}

const tier =
  main.bonferroni_p <= 0.01 &&
  main.maxstat_fpr <= 0.01 &&
  complete.bonferroni_p <= 0.01 &&
  nonPoor.bonferroni_p <= 0.01 &&
  withoutHarappa.bonferroni_p <= 0.05 &&
  withoutMohenjo.bonferroni_p <= 0.05 &&
  initialMain.bonferroni_p <= 0.01 &&
  initialMain.maxstat_fpr <= 0.01
    ? 'promoted candidate'
    : 'candidate';

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V4_400_TABLET_ACCOUNT_REGISTER_OPENER_20260531',
  vector: 'V4 context-to-meaning without sound; V2 slot grammar',
  confidence_tier: tier,
  risky_bet:
    '`400` marks a non-copper tablet/account register, especially `TAB:B` and `TAB:I`, and normally functions as an opening classifier in that register. This predicts carrier/register and slot role, not sound.',
  observed:
    `All canonical: ${main.target_a}/${main.context_rows} TAB:B/I rows vs ${main.target_c}/${main.pool_rows - main.context_rows} background, rank ${main.all_sign_rank}, Bonferroni=${main.bonferroni_p}, maxstat=${main.maxstat_fpr}. ` +
    `Complete-only Bonferroni=${complete.bonferroni_p}; non-poor Bonferroni=${nonPoor.bonferroni_p}; without Harappa Bonferroni=${withoutHarappa.bonferroni_p}; without Mohenjo-daro Bonferroni=${withoutMohenjo.bonferroni_p}. ` +
    `Inside TAB:B/I rows, ${TARGET} is initial in ${initialMain.target_initial}/${initialMain.target_occurrences}, rank ${initialMain.all_sign_rank}, Bonferroni=${initialMain.bonferroni_p}, maxstat=${initialMain.maxstat_fpr}. ` +
    `Support by type: ${groupCounts(supportRows, 'type')}. Support by material: ${groupCounts(supportRows, 'material')}. Support by shape: ${groupCounts(supportRows, 'shape')}. Support by site: ${groupCounts(supportRows, 'site')}.`,
  adversarial_test:
    `Canonical numeric-sequence collapse; all-sign Fisher rank for TAB:B/I context; ${ITERATIONS}-iteration max-stat context-label forger; complete-only and non-poor controls; leave-Harappa and leave-Mohenjo controls; within-register all-sign initial-position test with row-preserving sign-label forger.`,
  false_positive_rate: Math.max(main.maxstat_fpr, initialMain.maxstat_fpr),
  context_maxstat_fpr: main.maxstat_fpr,
  initial_position_maxstat_fpr: initialMain.maxstat_fpr,
  main_bonferroni_p: main.bonferroni_p,
  initial_bonferroni_p: initialMain.bonferroni_p,
  falsifier:
    'If source-checked TAB:B/I rows do not preserve 400, if 400-heavy rows outside TAB:B/I accumulate at comparable rates, or if 400 stops being the preferred initial sign inside TAB:B/I under expanded data, demote to a Harappa tablet-style marker or kill the account-register reading.',
  next_prediction:
    'Unverified TAB:B/I rows, especially faience/steatite rectangular, cylindrical, or prism tablets, should often begin with 400. Non-copper tablet rows containing both 400 and 740 should usually have 400 first, unlike the SEAL:R/TAB:C register where 740 is the broad opener.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({
    ...summary,
    context_pools: contextPools.map((pool) => pool.summary),
    initial_pools: initialPools.map((pool) => pool.summary),
    top_context_signs: contextPools[0].top_sign_rows,
    top_initial_signs: initialPools[0].top_initial_rows,
    support_rows: supportRows,
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
  'context_maxstat_fpr',
  'initial_position_maxstat_fpr',
  'main_bonferroni_p',
  'initial_bonferroni_p',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_context_pools.csv`), contextPools.map((pool) => pool.summary), [
  'pool',
  'pool_rows',
  'context_rows',
  'target_a',
  'target_c',
  'target_total',
  'target_context_share',
  'fisher_p',
  'bonferroni_p',
  'all_sign_rank',
  'maxstat_fpr',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_initial_pools.csv`), initialPools.map((pool) => pool.summary), [
  'pool',
  'rows',
  'occurrences',
  'target_occurrences',
  'target_initial',
  'target_initial_share',
  'fisher_p',
  'bonferroni_p',
  'all_sign_rank',
  'maxstat_fpr',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_top_context_signs.csv`), contextPools[0].top_sign_rows, [
  'pool',
  'sign',
  'pool_rows',
  'context_rows',
  'a',
  'b',
  'c',
  'd',
  'total',
  'context_share',
  'fisher_p',
  'bonferroni_p',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_top_initial_signs.csv`), initialPools[0].top_initial_rows, [
  'pool',
  'sign',
  'occurrences',
  'initial',
  'initial_share',
  'background_initial',
  'background_occurrences',
  'fisher_p',
  'bonferroni_p',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_support_rows.csv`), supportRows, [
  'object',
  'site',
  'region',
  'type',
  'material',
  'shape',
  'symbol',
  'condition',
  'complete',
  'tablet_account_context',
  'first_sign',
  'target_initial',
  'text',
]);

console.log(JSON.stringify(summary, null, 2));
