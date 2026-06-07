import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_806_rectangular_boundary_pivot_forger_20260531';
const RUN_DATE = '2026-05-31';
const TARGET = '806';
const ITERATIONS = 2000;

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
  return norm(row.type) === 'SEAL:R';
}

function boundaryNext(next) {
  return next === '<END>' || next === '002';
}

function pivotMotif(signs) {
  for (let i = 0; i <= signs.length - 3; i += 1) {
    if (['154', '158'].includes(signs[i]) && signs[i + 1] === TARGET && /^4(6[5-9]|7[0-5])$/.test(signs[i + 2])) return true;
  }
  return false;
}

function analyzeContextPool(name, poolRows, predicate, iterations = ITERATIONS) {
  const contextRows = poolRows.filter(predicate);
  const backgroundRows = poolRows.filter((row) => !predicate(row));
  const signs = [...new Set(poolRows.flatMap((row) => row.signs))].sort();
  const signHits = new Map(signs.map((sign) => [sign, poolRows.map((row) => row.signSet.has(sign))]));
  const signRows = signs.map((sign) => {
    const hits = signHits.get(sign);
    let a = 0;
    let c = 0;
    for (let i = 0; i < poolRows.length; i += 1) {
      if (!hits[i]) continue;
      if (predicate(poolRows[i])) a += 1;
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
      fisher_p: p,
      bonferroni_p: Math.min(1, p * signs.length),
    };
  }).sort((x, y) => x.fisher_p - y.fisher_p || y.a - x.a || x.sign.localeCompare(y.sign, undefined, { numeric: true }));
  const target = signRows.find((row) => row.sign === TARGET);
  const rank = signRows.findIndex((row) => row.sign === TARGET) + 1;
  const rand = mulberry32(0x8062026 ^ poolRows.length ^ contextRows.length ^ name.length);
  let maxGe = 0;
  for (let iter = 0; iter < iterations; iter += 1) {
    const chosen = new Set(sampleWithoutReplacement(rand, poolRows.length, contextRows.length));
    let best = 1;
    for (const sign of signs) {
      const hits = signHits.get(sign);
      let a = 0;
      for (const idx of chosen) if (hits[idx]) a += 1;
      const total = hits.filter(Boolean).length;
      const c = total - a;
      const p = fisherRightTail(a, contextRows.length - a, c, backgroundRows.length - c);
      if (p < best) best = p;
    }
    if (best <= target.fisher_p) maxGe += 1;
  }
  return {
    pool: name,
    pool_rows: poolRows.length,
    context_rows: contextRows.length,
    target_a: target.a,
    target_c: target.c,
    target_total: target.total,
    fisher_p: target.fisher_p,
    bonferroni_p: target.bonferroni_p,
    all_sign_rank: `${rank}/${signs.length}`,
    maxstat_fpr: maxGe / iterations,
  };
}

function analyzeBoundary(rows) {
  const occs = [];
  for (const row of rows) {
    for (let idx = 0; idx < row.signs.length; idx += 1) {
      occs.push({
        sign: row.signs[idx],
        row,
        next: row.signs[idx + 1] ?? '<END>',
        prev: row.signs[idx - 1] ?? '<START>',
      });
    }
  }
  const bySign = new Map();
  for (const occ of occs) {
    if (!bySign.has(occ.sign)) bySign.set(occ.sign, []);
    bySign.get(occ.sign).push(occ);
  }
  const signRows = [...bySign.entries()].filter(([, local]) => local.length >= 20).map(([sign, local]) => {
    const a = local.filter((occ) => boundaryNext(occ.next)).length;
    const background = occs.filter((occ) => occ.sign !== sign);
    const c = background.filter((occ) => boundaryNext(occ.next)).length;
    const p = fisherRightTail(a, local.length - a, c, background.length - c);
    return {
      sign,
      occurrences: local.length,
      boundary_next: a,
      boundary_share: a / local.length,
      background_boundary_next: c,
      background_occurrences: background.length,
      fisher_p: p,
      bonferroni_p: Math.min(1, p * bySign.size),
    };
  }).sort((x, y) => x.fisher_p - y.fisher_p || y.boundary_share - x.boundary_share || x.sign.localeCompare(y.sign, undefined, { numeric: true }));
  const target = signRows.find((row) => row.sign === TARGET);
  const rank = signRows.findIndex((row) => row.sign === TARGET) + 1;
  return { ...target, all_sign_rank: `${rank}/${signRows.length}`, top_sign_rows: signRows.slice(0, 20) };
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()]
  .map((row, idx) => ({ ...row, _idx: idx, signSet: new Set(row.signs) }));

const contextPools = [
  analyzeContextPool('seal_r_all', canonicalRows, registerContext),
  analyzeContextPool('seal_r_complete_only', canonicalRows.filter((row) => norm(row.complete) === 'Y'), registerContext),
  analyzeContextPool('seal_r_non_poor_only', canonicalRows.filter((row) => norm(row.condition) !== 'Poor'), registerContext),
  analyzeContextPool('seal_r_without_mohenjo', canonicalRows.filter((row) => norm(row.site) !== 'Mohenjo-daro'), registerContext),
  analyzeContextPool('seal_r_without_harappa', canonicalRows.filter((row) => norm(row.site) !== 'Harappa'), registerContext),
];
const main = contextPools[0];
const boundary = analyzeBoundary(canonicalRows);
const motifRows = canonicalRows.filter((row) => pivotMotif(row.signs)).map((row) => ({
  object: objectId(row),
  site: norm(row.site),
  region: norm(row.region),
  type: norm(row.type),
  material: norm(row.material),
  shape: norm(row.shape),
  condition: norm(row.condition),
  complete: norm(row.complete),
  text: row.text,
}));
const motifRegisterRows = motifRows.filter((row) => ['SEAL:R', 'TAB:B'].includes(row.type));
const supportRows = canonicalRows.filter((row) => row.signSet.has(TARGET)).map((row) => {
  const idx = row.signs.indexOf(TARGET);
  return {
    object: objectId(row),
    site: norm(row.site),
    region: norm(row.region),
    type: norm(row.type),
    material: norm(row.material),
    shape: norm(row.shape),
    symbol: norm(row.symbol),
    condition: norm(row.condition),
    complete: norm(row.complete),
    seal_r_context: String(registerContext(row)),
    boundary_next: String(boundaryNext(row.signs[idx + 1] ?? '<END>')),
    next: row.signs[idx + 1] ?? '<END>',
    prev: row.signs[idx - 1] ?? '<START>',
    has_154_158_806_46x_motif: String(pivotMotif(row.signs)),
    text: row.text,
  };
});

const tier =
  main.bonferroni_p <= 0.01 &&
  main.maxstat_fpr <= 0.01 &&
  contextPools.every((pool) => pool.bonferroni_p <= 0.05) &&
  boundary.bonferroni_p <= 0.05 &&
  motifRows.length >= 8 &&
  motifRegisterRows.length / motifRows.length >= 0.85
    ? 'candidate'
    : 'wild shot';

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V4_806_RECTANGULAR_BOUNDARY_PIVOT_20260531',
  vector: 'V4 context-to-meaning without sound',
  confidence_tier: tier,
  risky_bet:
    '`806` is a rectangular-seal boundary pivot: enriched in `SEAL:R`, often followed by `END` or `002`, and participating in a narrow `154/158-806-46x` pivot template that clusters in `SEAL:R`/`TAB:B` with known square-seal leakage. This predicts slot/register behavior only, not sound.',
  observed:
    `SEAL:R enrichment: ${main.target_a}/${main.context_rows} vs ${main.target_c}/${main.pool_rows - main.context_rows}, rank ${main.all_sign_rank}, Bonferroni=${main.bonferroni_p}, maxstat=${main.maxstat_fpr}. ` +
    `Controls: complete Bonferroni=${contextPools[1].bonferroni_p}; non-poor Bonferroni=${contextPools[2].bonferroni_p}; without Mohenjo=${contextPools[3].bonferroni_p}; without Harappa=${contextPools[4].bonferroni_p}. ` +
    `Boundary next END/002: ${boundary.boundary_next}/${boundary.occurrences}, rank ${boundary.all_sign_rank}, Bonferroni=${boundary.bonferroni_p}. ` +
    `Pivot motif 154/158-806-46x rows=${motifRows.length}; motif rows in SEAL:R or TAB:B=${motifRegisterRows.length}/${motifRows.length}; known leakage is two Harappa SEAL:S square-seal rows.`,
  adversarial_test:
    `Canonical numeric-sequence collapse; all-sign SEAL:R enrichment with ${ITERATIONS}-iteration max-stat label forger; complete-only, non-poor-only, leave-Mohenjo, leave-Harappa controls; all-sign boundary-rank test; exact pivot-motif context check.`,
  false_positive_rate: main.maxstat_fpr,
  seal_r_bonferroni_p: main.bonferroni_p,
  boundary_bonferroni_p: boundary.bonferroni_p,
  motif_rows: motifRows.length,
  falsifier:
    'If source-checked rectangular seal rows lose 806, if 806 no longer prefers END/002 under expanded data, or if the 154/158-806-46x motif expands substantially outside SEAL:R/TAB:B and the two current square-seal exceptions, demote this to a generic rectangular-register sign.',
  next_prediction:
    'Unverified `154/158-806-46x` rows should usually be SEAL:R or TAB:B, with occasional square-seal leakage. Unverified SEAL:R rows with 806 should often place it before END or 002, not randomly inside the sequence.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({ ...summary, context_pools: contextPools, boundary_top_signs: boundary.top_sign_rows, motif_rows_detail: motifRows, support_rows: supportRows }, null, 2),
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
  'seal_r_bonferroni_p',
  'boundary_bonferroni_p',
  'motif_rows',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_context_pools.csv`), contextPools, [
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
  'site',
  'region',
  'type',
  'material',
  'shape',
  'symbol',
  'condition',
  'complete',
  'seal_r_context',
  'boundary_next',
  'next',
  'prev',
  'has_154_158_806_46x_motif',
  'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_motif_rows.csv`), motifRows, [
  'object',
  'site',
  'region',
  'type',
  'material',
  'shape',
  'condition',
  'complete',
  'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_boundary_top_signs.csv`), boundary.top_sign_rows, [
  'sign',
  'occurrences',
  'boundary_next',
  'boundary_share',
  'background_boundary_next',
  'background_occurrences',
  'fisher_p',
  'bonferroni_p',
]);

console.log(JSON.stringify(summary, null, 2));
