// Tests whether sign `520` is linked to the elephant icon ("Elep" in the corpus
// iconography field) — a header/classifier for elephant-seal texts, possibly a
// mostly-Mohenjo-daro convention rather than a pan-corpus one. This is a context
// claim only; no sound value. The script reads metadata_filtered.csv, collapses
// duplicate sign sequences, and Fisher-tests 520-presence against elephant rows in
// eight pools (all, SEAL:S, square, complete, non-poor, leave-Mohenjo,
// leave-Harappa, Mohenjo only) plus two initial-position-only variants (does the
// row *start* with 520?). Every pool runs a 3,000-iteration null that redraws the
// elephant rows at random, scoring both the exact 520 test and the best p over all
// signs (max-stat). The tier ladder — wild shot, candidate, promoted candidate —
// depends on which controls pass. Writes a JSON report plus summary, support-row,
// elephant-without-520, top-sign, and forger-iteration CSVs to reports/.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_520_elephant_icon_header_forger_20260531';
const RUN_DATE = '2026-05-31';
const TARGET = '520';
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

function isElephant(row) {
  return norm(row.symbol) === 'Elep';
}

function hasInitial520(row) {
  return row.signs[0] === TARGET;
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
  const logChoose = (nn, kk) => {
    if (kk < 0 || kk > nn) return -Infinity;
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

function analyze(poolName, poolRows, hitFn = (row) => row.signSet.has(TARGET), iterations = ITERATIONS) {
  const contextN = poolRows.filter(isElephant).length;
  const backgroundN = poolRows.length - contextN;
  const signs = [...new Set(poolRows.flatMap((row) => row.signs))].sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
  const indexBySign = new Map(signs.map((sign, idx) => [sign, idx]));
  const uniqueSignIndexesByRow = poolRows.map((row) => [...row.signSet].map((sign) => indexBySign.get(sign)).filter((idx) => idx !== undefined));
  const totals = new Uint16Array(signs.length);
  const contextCounts = new Uint16Array(signs.length);
  for (let rowIdx = 0; rowIdx < poolRows.length; rowIdx += 1) {
    for (const signIdx of uniqueSignIndexesByRow[rowIdx]) {
      totals[signIdx] += 1;
      if (isElephant(poolRows[rowIdx])) contextCounts[signIdx] += 1;
    }
  }
  const signStats = signs.map((sign, signIdx) => {
    const a = contextCounts[signIdx];
    const c = totals[signIdx] - a;
    return {
      pool: poolName,
      sign,
      context_rows: contextN,
      background_rows: backgroundN,
      a,
      b: contextN - a,
      c,
      d: backgroundN - c,
      total: totals[signIdx],
      fisher_p: fisherRightTail(a, contextN - a, c, backgroundN - c),
    };
  }).sort((a, b) => a.fisher_p - b.fisher_p || b.a - a.a || a.sign.localeCompare(b.sign, undefined, { numeric: true }));
  let targetA = 0;
  let targetC = 0;
  for (const row of poolRows) {
    if (!hitFn(row)) continue;
    if (isElephant(row)) targetA += 1;
    else targetC += 1;
  }
  const targetP = fisherRightTail(targetA, contextN - targetA, targetC, backgroundN - targetC);
  const targetRank = hitFn === hasInitial520
    ? 'not_all_sign_ranked_initial_only'
    : `${signStats.findIndex((row) => row.sign === TARGET) + 1}/${signs.length}`;
  const rand = mulberry32(0x520e1e ^ poolRows.length ^ contextN ^ poolName.length);
  let maxGe = 0;
  let targetGe = 0;
  const iterationRows = [];
  for (let iter = 0; iter < iterations; iter += 1) {
    const chosen = new Set(sampleWithoutReplacement(rand, poolRows.length, contextN));
    const chosenCounts = new Uint16Array(signs.length);
    let targetShuffleA = 0;
    let targetShuffleC = 0;
    for (let rowIdx = 0; rowIdx < poolRows.length; rowIdx += 1) {
      const inContext = chosen.has(rowIdx);
      if (inContext) {
        for (const signIdx of uniqueSignIndexesByRow[rowIdx]) chosenCounts[signIdx] += 1;
      }
      if (hitFn(poolRows[rowIdx])) {
        if (inContext) targetShuffleA += 1;
        else targetShuffleC += 1;
      }
    }
    let best = 1;
    for (let signIdx = 0; signIdx < signs.length; signIdx += 1) {
      const a = chosenCounts[signIdx];
      const c = totals[signIdx] - a;
      const p = fisherRightTail(a, contextN - a, c, backgroundN - c);
      if (p < best) best = p;
    }
    const targetShuffleP = fisherRightTail(targetShuffleA, contextN - targetShuffleA, targetShuffleC, backgroundN - targetShuffleC);
    const maxHit = best <= targetP;
    const targetHit = targetShuffleP <= targetP;
    if (maxHit) maxGe += 1;
    if (targetHit) targetGe += 1;
    if (iter < 50 || maxHit || targetHit) {
      iterationRows.push({
        pool: poolName,
        hit: hitFn === hasInitial520 ? 'initial_520' : 'any_520',
        iteration: iter,
        best_p: best,
        target_shuffle_p: targetShuffleP,
        max_ge_observed: String(maxHit),
        target_ge_observed: String(targetHit),
      });
    }
  }
  return {
    summary: {
      pool: poolName,
      hit: hitFn === hasInitial520 ? 'initial_520' : 'any_520',
      pool_rows: poolRows.length,
      elephant_rows: contextN,
      background_rows: backgroundN,
      target_a: targetA,
      target_c: targetC,
      target_total: targetA + targetC,
      fisher_p: targetP,
      rank: targetRank,
      bonferroni_p: hitFn === hasInitial520 ? null : Math.min(1, targetP * signs.length),
      maxstat_fpr: maxGe / iterations,
      target_label_shuffle_fpr: targetGe / iterations,
    },
    top_rows: signStats.slice(0, 20),
    iteration_rows: iterationRows,
  };
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()]
  .filter((row) => row.signs.length)
  .map((row) => ({ ...row, signSet: new Set(row.signs) }));

const pools = {
  all: canonicalRows,
  seal_s_only: canonicalRows.filter((row) => norm(row.type) === 'SEAL:S'),
  square_only: canonicalRows.filter((row) => norm(row.shape) === 'square'),
  complete_only: canonicalRows.filter((row) => norm(row.complete) === 'Y'),
  non_poor_only: canonicalRows.filter((row) => norm(row.condition) !== 'Poor'),
  without_mohenjo: canonicalRows.filter((row) => norm(row.site) !== 'Mohenjo-daro'),
  without_harappa: canonicalRows.filter((row) => norm(row.site) !== 'Harappa'),
  mohenjo_only: canonicalRows.filter((row) => norm(row.site) === 'Mohenjo-daro'),
};

const analyses = [];
for (const [name, poolRows] of Object.entries(pools)) analyses.push(analyze(name, poolRows));
analyses.push(analyze('all_initial_only', canonicalRows, hasInitial520));
analyses.push(analyze('seal_s_initial_only', pools.seal_s_only, hasInitial520));

const summaries = analyses.map((analysis) => analysis.summary);
const allAny = summaries.find((row) => row.pool === 'all' && row.hit === 'any_520');
const sealAny = summaries.find((row) => row.pool === 'seal_s_only' && row.hit === 'any_520');
const squareAny = summaries.find((row) => row.pool === 'square_only' && row.hit === 'any_520');
const completeAny = summaries.find((row) => row.pool === 'complete_only' && row.hit === 'any_520');
const nonPoorAny = summaries.find((row) => row.pool === 'non_poor_only' && row.hit === 'any_520');
const withoutMohenjoAny = summaries.find((row) => row.pool === 'without_mohenjo' && row.hit === 'any_520');
const withoutHarappaAny = summaries.find((row) => row.pool === 'without_harappa' && row.hit === 'any_520');
const mohenjoAny = summaries.find((row) => row.pool === 'mohenjo_only' && row.hit === 'any_520');
const allInitial = summaries.find((row) => row.pool === 'all_initial_only');
const sealInitial = summaries.find((row) => row.pool === 'seal_s_initial_only');

const candidate =
  allAny.target_label_shuffle_fpr <= 0.01 &&
  allAny.maxstat_fpr <= 0.1 &&
  sealAny.target_label_shuffle_fpr <= 0.05 &&
  sealAny.maxstat_fpr <= 0.1 &&
  squareAny.target_label_shuffle_fpr <= 0.05 &&
  squareAny.maxstat_fpr <= 0.1 &&
  mohenjoAny.target_label_shuffle_fpr <= 0.05;
const promoted =
  candidate &&
  completeAny.target_label_shuffle_fpr <= 0.01 &&
  nonPoorAny.target_label_shuffle_fpr <= 0.01 &&
  withoutMohenjoAny.target_label_shuffle_fpr <= 0.01 &&
  withoutHarappaAny.target_label_shuffle_fpr <= 0.01;

const supportRows = canonicalRows
  .filter((row) => isElephant(row) && row.signSet.has(TARGET))
  .map((row) => ({
    object: objectId(row),
    site: norm(row.site),
    region: norm(row.region),
    type: norm(row.type),
    material: norm(row.material),
    shape: norm(row.shape),
    symbol: norm(row.symbol),
    condition: norm(row.condition),
    complete: norm(row.complete),
    initial_520: String(hasInitial520(row)),
    text: row.text,
  }));
const elephantWithout520 = canonicalRows
  .filter((row) => isElephant(row) && !row.signSet.has(TARGET))
  .map((row) => ({
    object: objectId(row),
    site: norm(row.site),
    type: norm(row.type),
    condition: norm(row.condition),
    complete: norm(row.complete),
    text: row.text,
  }));

const topRows = analyses.flatMap((analysis) => analysis.top_rows.map((row) => ({
  source_pool: analysis.summary.pool,
  source_hit: analysis.summary.hit,
  ...row,
})));
const iterationRows = analyses.flatMap((analysis) => analysis.iteration_rows);

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V4_520_ELEPHANT_ICON_HEADER_20260531',
  vector: 'V4 context-to-meaning without sound',
  confidence_tier: promoted ? 'promoted candidate' : candidate ? 'candidate' : 'wild shot',
  risky_bet:
    '`520` is an elephant-icon associated header/classifier sign, with a stronger Mohenjo-daro component than a pan-corpus semantic claim. This predicts context only, not sound.',
  observed:
    `All elephant any-520: ${allAny.target_a}/${allAny.elephant_rows} vs ${allAny.target_c}/${allAny.background_rows}, rank=${allAny.rank}, Bonferroni=${allAny.bonferroni_p}, maxstat=${allAny.maxstat_fpr}, target-FPR=${allAny.target_label_shuffle_fpr}. ` +
    `SEAL:S any-520: ${sealAny.target_a}/${sealAny.elephant_rows} vs ${sealAny.target_c}/${sealAny.background_rows}, p=${sealAny.fisher_p}, target-FPR=${sealAny.target_label_shuffle_fpr}. ` +
    `Mohenjo any-520: ${mohenjoAny.target_a}/${mohenjoAny.elephant_rows} vs ${mohenjoAny.target_c}/${mohenjoAny.background_rows}, p=${mohenjoAny.fisher_p}, target-FPR=${mohenjoAny.target_label_shuffle_fpr}. ` +
    `Without Mohenjo any-520: ${withoutMohenjoAny.target_a}/${withoutMohenjoAny.elephant_rows} vs ${withoutMohenjoAny.target_c}/${withoutMohenjoAny.background_rows}, p=${withoutMohenjoAny.fisher_p}, target-FPR=${withoutMohenjoAny.target_label_shuffle_fpr}. ` +
    `Initial-520 all: ${allInitial.target_a}/${allInitial.elephant_rows} vs ${allInitial.target_c}/${allInitial.background_rows}, p=${allInitial.fisher_p}, target-FPR=${allInitial.target_label_shuffle_fpr}; SEAL:S initial p=${sealInitial.fisher_p}.`,
  adversarial_test:
    `Canonical numeric-sequence collapse; all-sign label-shuffle maxstat and exact target-label shuffle across all/SEAL:S/square/complete/non-poor/leave-site controls; separate initial-only target test. ${ITERATIONS} iterations per pool.`,
  primary_false_positive_rate: Math.max(allAny.target_label_shuffle_fpr, sealAny.target_label_shuffle_fpr, squareAny.target_label_shuffle_fpr),
  false_positive_rate: Math.max(
    allAny.target_label_shuffle_fpr,
    sealAny.target_label_shuffle_fpr,
    squareAny.target_label_shuffle_fpr,
    completeAny.target_label_shuffle_fpr,
    nonPoorAny.target_label_shuffle_fpr,
    withoutMohenjoAny.target_label_shuffle_fpr,
    withoutHarappaAny.target_label_shuffle_fpr,
    mohenjoAny.target_label_shuffle_fpr,
  ),
  skeptic_verdict: promoted
    ? 'Survives hostile controls as a promoted context candidate; still requires source-image audit before semantic acceptance.'
    : candidate
      ? 'Survives first-pass elephant association, but leave-Mohenjo and complete/non-poor controls keep it below promotion.'
      : 'Killed as a semantic candidate by same-type/square all-sign maxstat and leave-Mohenjo controls; keep only as a wild shot unless new source-bound elephant rows strengthen it.',
  falsifier:
    'If additional source-bound elephant rows outside Mohenjo-daro do not carry 520, or if incomplete/poor rows account for the enrichment, demote this to a Mohenjo/condition artifact. If new complete elephant square seals carry initial 520, promote.',
  next_prediction:
    'New Mohenjo-daro elephant seal rows should carry 520, often initially or secondarily near the header zone; non-Mohenjo elephant rows are the decisive held-out test.',
  key_controls: {
    all_any_520: allAny,
    seal_s_any_520: sealAny,
    square_any_520: squareAny,
    complete_any_520: completeAny,
    non_poor_any_520: nonPoorAny,
    without_mohenjo_any_520: withoutMohenjoAny,
    without_harappa_any_520: withoutHarappaAny,
    mohenjo_any_520: mohenjoAny,
    all_initial_520: allInitial,
    seal_s_initial_520: sealInitial,
  },
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), JSON.stringify({
  ...summary,
  support_rows: supportRows,
  elephant_without_520_rows: elephantWithout520,
  target_summaries: summaries,
}, null, 2), 'utf8');
writeCsv(path.join(OUT_DIR, `${PREFIX}_summaries.csv`), summaries, [
  'pool',
  'hit',
  'pool_rows',
  'elephant_rows',
  'background_rows',
  'target_a',
  'target_c',
  'target_total',
  'fisher_p',
  'rank',
  'bonferroni_p',
  'maxstat_fpr',
  'target_label_shuffle_fpr',
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
  'initial_520',
  'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_elephant_without_520_rows.csv`), elephantWithout520, [
  'object',
  'site',
  'type',
  'condition',
  'complete',
  'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_top_signs.csv`), topRows, [
  'source_pool',
  'source_hit',
  'pool',
  'sign',
  'context_rows',
  'background_rows',
  'a',
  'b',
  'c',
  'd',
  'total',
  'fisher_p',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_forger_iterations.csv`), iterationRows, [
  'pool',
  'hit',
  'iteration',
  'best_p',
  'target_shuffle_p',
  'max_ge_observed',
  'target_ge_observed',
]);

console.log(JSON.stringify(summary, null, 2));
