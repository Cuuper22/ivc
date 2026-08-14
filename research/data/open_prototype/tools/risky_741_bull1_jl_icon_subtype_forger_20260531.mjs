// Tests whether sign `741` marks the Bull1:J / Bull1:L iconographic subtypes
// specifically, rather than bull imagery in general — an icon-class claim with no
// sound value. The script reads metadata_filtered.csv, collapses duplicate sign
// sequences, and Fisher-tests every sign for Bull1:J/L enrichment in seven pools:
// all rows, complete only, non-poor, leave-Mohenjo-daro, leave-Harappa, SEAL:S
// only, and — the sharpest control — rows restricted to Bull1 variants only, so
// 741 must separate J/L from its sibling bull subtypes. Each pool applies
// Bonferroni over all signs and a 3,000-iteration max-stat forger that redraws the
// context rows at random. It also checks how tightly the sub-motif `741-060-920`
// stays inside Bull1:J/L rows. Candidate status requires every pool's test to pass
// at 0.01. Writes a bet summary (JSON + CSV) plus pool, support-row, motif-row,
// and top-sign CSVs to the reports directory.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_741_bull1_jl_icon_subtype_forger_20260531';
const RUN_DATE = '2026-05-31';
const TARGET = '741';
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

function bullJL(row) {
  return ['Bull1:J', 'Bull1:L'].includes(norm(row.symbol));
}

function bull1Variant(row) {
  return norm(row.symbol).startsWith('Bull1');
}

function hasNgram(row, gram) {
  return row.signs.join('-').includes(gram);
}

function analyzePool(name, poolRows, predicate, iterations = ITERATIONS) {
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
  const rand = mulberry32(0x7412026 ^ poolRows.length ^ contextRows.length ^ name.length);
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
  analyzePool('bull1_jl_all', canonicalRows, bullJL),
  analyzePool('bull1_jl_complete_only', canonicalRows.filter((row) => norm(row.complete) === 'Y'), bullJL),
  analyzePool('bull1_jl_non_poor_only', canonicalRows.filter((row) => norm(row.condition) !== 'Poor'), bullJL),
  analyzePool('bull1_jl_without_mohenjo', canonicalRows.filter((row) => norm(row.site) !== 'Mohenjo-daro'), bullJL),
  analyzePool('bull1_jl_without_harappa', canonicalRows.filter((row) => norm(row.site) !== 'Harappa'), bullJL),
  analyzePool('bull1_jl_seal_s_only', canonicalRows.filter((row) => norm(row.type) === 'SEAL:S'), bullJL),
  analyzePool('bull1_jl_vs_other_bull1_variants', canonicalRows.filter(bull1Variant), bullJL),
];
const main = pools[0].summary;
const complete = pools[1].summary;
const nonPoor = pools[2].summary;
const withoutMohenjo = pools[3].summary;
const withoutHarappa = pools[4].summary;
const sealSOnly = pools[5].summary;
const bullVariant = pools[6].summary;

const supportRows = canonicalRows.filter((row) => bullJL(row) && row.signSet.has(TARGET)).map((row) => ({
  object: objectId(row),
  site: norm(row.site),
  region: norm(row.region),
  type: norm(row.type),
  material: norm(row.material),
  shape: norm(row.shape),
  symbol: norm(row.symbol),
  condition: norm(row.condition),
  complete: norm(row.complete),
  has_741_060_920: String(hasNgram(row, '741-060-920')),
  text: row.text,
}));
const ngramRows = canonicalRows.filter((row) => hasNgram(row, '741-060-920')).map((row) => ({
  object: objectId(row),
  site: norm(row.site),
  symbol: norm(row.symbol),
  type: norm(row.type),
  text: row.text,
}));
const ngramBullJl = ngramRows.filter((row) => ['Bull1:J', 'Bull1:L'].includes(row.symbol)).length;

const tier =
  main.bonferroni_p <= 0.01 &&
  main.maxstat_fpr <= 0.01 &&
  complete.fisher_p <= 0.01 &&
  nonPoor.fisher_p <= 0.01 &&
  withoutMohenjo.fisher_p <= 0.01 &&
  withoutHarappa.fisher_p <= 0.01 &&
  sealSOnly.fisher_p <= 0.01 &&
  bullVariant.fisher_p <= 0.01
    ? 'candidate'
    : 'wild shot';

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V4_741_BULL1_JL_ICON_SUBTYPE_20260531',
  vector: 'V4 context-to-meaning without sound',
  confidence_tier: tier,
  risky_bet:
    '`741` marks a Bull1 J/L iconographic subtype rather than a generic bull sign. This predicts icon class association only, not sound.',
  observed:
    `Bull1:J/L all: ${main.target_a}/${main.context_rows} vs ${main.target_c}/${main.pool_rows - main.context_rows}, rank ${main.all_sign_rank}, Bonferroni=${main.bonferroni_p}, maxstat=${main.maxstat_fpr}. ` +
    `Complete fisher=${complete.fisher_p}; non-poor fisher=${nonPoor.fisher_p}; without Mohenjo fisher=${withoutMohenjo.fisher_p}; without Harappa fisher=${withoutHarappa.fisher_p}. ` +
    `Same-type SEAL:S fisher=${sealSOnly.fisher_p}, Bonferroni=${sealSOnly.bonferroni_p}. Bull1-variants-only fisher=${bullVariant.fisher_p}, Bonferroni=${bullVariant.bonferroni_p}. ` +
    `Sub-motif 741-060-920 rows=${ngramRows.length}; Bull1:J/L rows=${ngramBullJl}/${ngramRows.length}.`,
  adversarial_test:
    `Canonical numeric-sequence collapse; all-sign Bull1:J/L enrichment with ${ITERATIONS}-iteration max-stat label forger; complete-only, non-poor-only, leave-site controls; same-type SEAL:S control; Bull1-variants-only control; 741-060-920 sub-motif check.`,
  false_positive_rate: main.maxstat_fpr,
  main_bonferroni_p: main.bonferroni_p,
  seal_s_same_type_bonferroni_p: sealSOnly.bonferroni_p,
  bull1_variant_bonferroni_p: bullVariant.bonferroni_p,
  falsifier:
    'If source-checked Bull1:J/L rows lose 741, or if other Bull1 variants acquire 741 at the same rate under same-type controls, demote this to generic bull-icon noise. If 741-060-920 continues to spread outside Bull1:J/L, it cannot be used as a subtype formula.',
  next_prediction:
    'Unverified Bull1:J and Bull1:L rows should be enriched for 741 compared with other Bull1 variants, but not categorically; the expected support is probabilistic, not mandatory.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({ ...summary, pools: pools.map((pool) => pool.summary), support_rows: supportRows, ngram_rows: ngramRows, top_sign_rows: pools[0].top_sign_rows }, null, 2),
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
  'seal_s_same_type_bonferroni_p',
  'bull1_variant_bonferroni_p',
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
  'site',
  'region',
  'type',
  'material',
  'shape',
  'symbol',
  'condition',
  'complete',
  'has_741_060_920',
  'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_ngram_rows.csv`), ngramRows, [
  'object',
  'site',
  'symbol',
  'type',
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
