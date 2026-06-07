import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_405806_bull1w_icon_subtype_forger_20260531';
const RUN_DATE = '2026-05-31';
const ITERATIONS = 3000;
const TARGET_SIGNS = ['405', '806'];

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

function bull1w(row) {
  return norm(row.symbol) === 'Bull1:W';
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

function signRows(poolRows) {
  const signs = [...new Set(poolRows.flatMap((row) => row.signs))].sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
  const hits = new Map(signs.map((sign) => [sign, poolRows.map((row) => row.signSet.has(sign))]));
  const totals = new Map(signs.map((sign) => [sign, hits.get(sign).filter(Boolean).length]));
  const indexBySign = new Map(signs.map((sign, idx) => [sign, idx]));
  const uniqueSignIndexesByRow = poolRows.map((row) => [...row.signSet].map((sign) => indexBySign.get(sign)).filter((idx) => idx !== undefined));
  return { signs, hits, totals, indexBySign, uniqueSignIndexesByRow };
}

function analyzeOneSign(poolName, poolRows, sign, iterations = ITERATIONS) {
  const contextRows = poolRows.filter(bull1w);
  const contextN = contextRows.length;
  const backgroundN = poolRows.length - contextN;
  const { signs, hits, totals, uniqueSignIndexesByRow } = signRows(poolRows);
  const signStats = signs.map((candidate) => {
    const rowHits = hits.get(candidate);
    let a = 0;
    for (let i = 0; i < poolRows.length; i += 1) if (bull1w(poolRows[i]) && rowHits[i]) a += 1;
    const total = totals.get(candidate);
    const c = total - a;
    return {
      sign: candidate,
      pool: poolName,
      context_rows: contextN,
      background_rows: backgroundN,
      a,
      b: contextN - a,
      c,
      d: backgroundN - c,
      total,
      fisher_p: fisherRightTail(a, contextN - a, c, backgroundN - c),
    };
  }).sort((a, b) => a.fisher_p - b.fisher_p || b.a - a.a || a.sign.localeCompare(b.sign, undefined, { numeric: true }));
  const target = signStats.find((row) => row.sign === sign);
  const rank = signStats.findIndex((row) => row.sign === sign) + 1;
  const rand = mulberry32(0x405806 ^ poolRows.length ^ contextN ^ Number(sign));
  let maxGe = 0;
  const iterationRows = [];
  for (let iter = 0; iter < iterations; iter += 1) {
    const chosen = new Set(sampleWithoutReplacement(rand, poolRows.length, contextN));
    const chosenCounts = new Uint16Array(signs.length);
    for (const idx of chosen) {
      for (const signIdx of uniqueSignIndexesByRow[idx]) chosenCounts[signIdx] += 1;
    }
    let best = 1;
    for (let signIdx = 0; signIdx < signs.length; signIdx += 1) {
      const candidate = signs[signIdx];
      const a = chosenCounts[signIdx];
      const total = totals.get(candidate);
      const c = total - a;
      const p = fisherRightTail(a, contextN - a, c, backgroundN - c);
      if (p < best) best = p;
    }
    const ge = best <= target.fisher_p;
    if (ge) maxGe += 1;
    if (iter < 50 || ge) {
      iterationRows.push({
        pool: poolName,
        target_kind: sign,
        iteration: iter,
        best_p: best,
        ge_observed: String(ge),
      });
    }
  }
  return {
    summary: {
      target_kind: sign,
      pool: poolName,
      pool_rows: poolRows.length,
      context_rows: contextN,
      background_rows: backgroundN,
      target_a: target.a,
      target_c: target.c,
      target_total: target.total,
      fisher_p: target.fisher_p,
      bonferroni_p: Math.min(1, target.fisher_p * signs.length),
      all_sign_rank: `${rank}/${signs.length}`,
      maxstat_fpr: maxGe / iterations,
    },
    top_sign_rows: signStats.slice(0, 20),
    iteration_rows: iterationRows,
  };
}

function analyzeEither(poolName, poolRows, iterations = ITERATIONS) {
  const contextN = poolRows.filter(bull1w).length;
  const backgroundN = poolRows.length - contextN;
  const targetHit = (row) => TARGET_SIGNS.some((sign) => row.signSet.has(sign));
  let targetA = 0;
  let targetC = 0;
  for (const row of poolRows) {
    if (!targetHit(row)) continue;
    if (bull1w(row)) targetA += 1;
    else targetC += 1;
  }
  const targetP = fisherRightTail(targetA, contextN - targetA, targetC, backgroundN - targetC);
  const { signs, hits, totals } = signRows(poolRows);
  const pairRows = [];
  if (['seal_s_only', 'square_only'].includes(poolName)) {
    const rowIndexesBySign = new Map(signs.map((sign) => {
      const indexes = [];
      const rowHits = hits.get(sign);
      for (let idx = 0; idx < rowHits.length; idx += 1) {
        if (rowHits[idx]) indexes.push(idx);
      }
      return [sign, indexes];
    }));
    const contextCountsBySign = new Map(signs.map((sign) => {
      const rowHits = hits.get(sign);
      let count = 0;
      for (let idx = 0; idx < poolRows.length; idx += 1) {
        if (rowHits[idx] && bull1w(poolRows[idx])) count += 1;
      }
      return [sign, count];
    }));
    for (let i = 0; i < signs.length; i += 1) {
      for (let j = i + 1; j < signs.length; j += 1) {
        const s1 = signs[i];
        const s2 = signs[j];
        const rows1 = rowIndexesBySign.get(s1);
        const rows2 = rowIndexesBySign.get(s2);
        const smaller = rows1.length <= rows2.length ? rows1 : rows2;
        const otherHits = rows1.length <= rows2.length ? hits.get(s2) : hits.get(s1);
        let intersectTotal = 0;
        let intersectContext = 0;
        for (const idx of smaller) {
          if (!otherHits[idx]) continue;
          intersectTotal += 1;
          if (bull1w(poolRows[idx])) intersectContext += 1;
        }
        const a = contextCountsBySign.get(s1) + contextCountsBySign.get(s2) - intersectContext;
        const total = totals.get(s1) + totals.get(s2) - intersectTotal;
        const c = total - a;
        pairRows.push({
          pair: `${s1}/${s2}`,
          a,
          c,
          total,
          fisher_p: fisherRightTail(a, contextN - a, c, backgroundN - c),
        });
      }
    }
    pairRows.sort((a, b) => a.fisher_p - b.fisher_p || b.a - a.a || a.pair.localeCompare(b.pair, undefined, { numeric: true }));
  }
  const targetPair = TARGET_SIGNS.slice().sort().join('/');
  const rank = pairRows.length ? pairRows.findIndex((row) => row.pair === targetPair) + 1 : null;
  const rand = mulberry32(0xe175806 ^ poolRows.length ^ contextN);
  let targetGe = 0;
  const iterationRows = [];
  for (let iter = 0; iter < iterations; iter += 1) {
    const chosen = new Set(sampleWithoutReplacement(rand, poolRows.length, contextN));
    let a = 0;
    let c = 0;
    for (let idx = 0; idx < poolRows.length; idx += 1) {
      if (!targetHit(poolRows[idx])) continue;
      if (chosen.has(idx)) a += 1;
      else c += 1;
    }
    const p = fisherRightTail(a, contextN - a, c, backgroundN - c);
    const ge = p <= targetP;
    if (ge) targetGe += 1;
    if (iter < 50 || ge) {
      iterationRows.push({
        pool: poolName,
        target_kind: '405_or_806',
        iteration: iter,
        target_label_shuffle_p: p,
        ge_observed: String(ge),
      });
    }
  }
  return {
    summary: {
      target_kind: '405_or_806',
      pool: poolName,
      pool_rows: poolRows.length,
      context_rows: contextN,
      background_rows: backgroundN,
      target_a: targetA,
      target_c: targetC,
      target_total: targetA + targetC,
      fisher_p: targetP,
      all_pair_rank: rank === null ? 'not_scanned_control' : `${rank}/${pairRows.length}`,
      target_label_shuffle_fpr: targetGe / iterations,
    },
    top_pair_rows: pairRows.slice(0, 20),
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
};

const oneSignAnalyses = [];
const eitherAnalyses = [];
for (const [name, poolRows] of Object.entries(pools)) {
  for (const sign of TARGET_SIGNS) oneSignAnalyses.push(analyzeOneSign(name, poolRows, sign));
  eitherAnalyses.push(analyzeEither(name, poolRows));
}

const summaries = [
  ...oneSignAnalyses.map((analysis) => analysis.summary),
  ...eitherAnalyses.map((analysis) => analysis.summary),
];
const topRows = oneSignAnalyses.flatMap((analysis) => analysis.top_sign_rows.map((row) => ({ ...row, source: `${analysis.summary.pool}:${analysis.summary.target_kind}` })));
const topPairs = eitherAnalyses.flatMap((analysis) => analysis.top_pair_rows.map((row) => ({ ...row, source: analysis.summary.pool })));
const iterationRows = [
  ...oneSignAnalyses.flatMap((analysis) => analysis.iteration_rows),
  ...eitherAnalyses.flatMap((analysis) => analysis.iteration_rows),
];

const supportRows = canonicalRows
  .filter((row) => bull1w(row) && TARGET_SIGNS.some((sign) => row.signSet.has(sign)))
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
    has_405: String(row.signSet.has('405')),
    has_806: String(row.signSet.has('806')),
    text: row.text,
  }));
const outsideRows = canonicalRows
  .filter((row) => !bull1w(row) && TARGET_SIGNS.some((sign) => row.signSet.has(sign)))
  .slice(0, 80)
  .map((row) => ({
    object: objectId(row),
    site: norm(row.site),
    type: norm(row.type),
    symbol: norm(row.symbol),
    condition: norm(row.condition),
    complete: norm(row.complete),
    has_405: String(row.signSet.has('405')),
    has_806: String(row.signSet.has('806')),
    text: row.text,
  }));

const sealEither = summaries.find((row) => row.pool === 'seal_s_only' && row.target_kind === '405_or_806');
const squareEither = summaries.find((row) => row.pool === 'square_only' && row.target_kind === '405_or_806');
const completeEither = summaries.find((row) => row.pool === 'complete_only' && row.target_kind === '405_or_806');
const nonPoorEither = summaries.find((row) => row.pool === 'non_poor_only' && row.target_kind === '405_or_806');
const withoutMohenjoEither = summaries.find((row) => row.pool === 'without_mohenjo' && row.target_kind === '405_or_806');
const withoutHarappaEither = summaries.find((row) => row.pool === 'without_harappa' && row.target_kind === '405_or_806');
const seal405 = summaries.find((row) => row.pool === 'seal_s_only' && row.target_kind === '405');
const seal806 = summaries.find((row) => row.pool === 'seal_s_only' && row.target_kind === '806');

const promoted =
  sealEither.target_label_shuffle_fpr <= 0.01 &&
  seal405.maxstat_fpr <= 0.01 &&
  seal806.maxstat_fpr <= 0.01 &&
  squareEither.target_label_shuffle_fpr <= 0.01 &&
  completeEither.target_label_shuffle_fpr <= 0.01 &&
  nonPoorEither.target_label_shuffle_fpr <= 0.01 &&
  withoutMohenjoEither.target_label_shuffle_fpr <= 0.01 &&
  withoutHarappaEither.target_label_shuffle_fpr <= 0.01;

const candidate =
  sealEither.target_label_shuffle_fpr <= 0.01 &&
  seal405.maxstat_fpr <= 0.01 &&
  seal806.maxstat_fpr <= 0.01 &&
  squareEither.target_label_shuffle_fpr <= 0.01;

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V4_405806_BULL1W_ICON_SUBTYPE_20260531',
  vector: 'V4 context-to-meaning without sound',
  confidence_tier: promoted ? 'promoted candidate' : candidate ? 'candidate' : 'wild shot',
  risky_bet:
    '`405/806` are Bull1:W icon-subtype markers in square seal texts. This predicts a context class, not sound; it also predicts that `806` is context-sensitive, because a separate rectangular/copper closure-pivot use has already been detected.',
  observed:
    `SEAL:S either 405/806: ${sealEither.target_a}/${sealEither.context_rows} vs ${sealEither.target_c}/${sealEither.background_rows}, p=${sealEither.fisher_p}, pair-rank=${sealEither.all_pair_rank}, target-label FPR=${sealEither.target_label_shuffle_fpr}. ` +
    `SEAL:S 405 alone: ${seal405.target_a}/${seal405.context_rows} vs ${seal405.target_c}/${seal405.background_rows}, rank=${seal405.all_sign_rank}, Bonferroni=${seal405.bonferroni_p}, maxstat=${seal405.maxstat_fpr}. ` +
    `SEAL:S 806 alone: ${seal806.target_a}/${seal806.context_rows} vs ${seal806.target_c}/${seal806.background_rows}, rank=${seal806.all_sign_rank}, Bonferroni=${seal806.bonferroni_p}, maxstat=${seal806.maxstat_fpr}. ` +
    `Controls: square either p=${squareEither.fisher_p}, FPR=${squareEither.target_label_shuffle_fpr}; complete p=${completeEither.fisher_p}, FPR=${completeEither.target_label_shuffle_fpr}; non-poor p=${nonPoorEither.fisher_p}, FPR=${nonPoorEither.target_label_shuffle_fpr}; without Mohenjo p=${withoutMohenjoEither.fisher_p}, FPR=${withoutMohenjoEither.target_label_shuffle_fpr}; without Harappa p=${withoutHarappaEither.fisher_p}, FPR=${withoutHarappaEither.target_label_shuffle_fpr}.`,
  adversarial_test:
    `Canonical numeric-sequence collapse; target sign tests against all signs with ${ITERATIONS}-iteration Bull1:W label-shuffle maxstat; exact target-pair label-shuffle for the two-sign family; SEAL:S, square, complete, non-poor, leave-Mohenjo, and leave-Harappa controls.`,
  primary_false_positive_rate: Math.max(
    sealEither.target_label_shuffle_fpr,
    seal405.maxstat_fpr,
    seal806.maxstat_fpr,
    squareEither.target_label_shuffle_fpr,
  ),
  false_positive_rate: Math.max(
    sealEither.target_label_shuffle_fpr,
    seal405.maxstat_fpr,
    seal806.maxstat_fpr,
    squareEither.target_label_shuffle_fpr,
    completeEither.target_label_shuffle_fpr,
    nonPoorEither.target_label_shuffle_fpr,
    withoutMohenjoEither.target_label_shuffle_fpr,
    withoutHarappaEither.target_label_shuffle_fpr,
  ),
  skeptic_verdict: promoted
    ? 'Survives initial hostile controls as a promoted context-to-meaning candidate; still no phonetic value and still needs independent source-image audit before acceptance.'
    : 'Survives the SEAL:S/square maxstat gate, but leave-Harappa and preservation controls are weaker; keep as a candidate, not a promoted or accepted semantic claim.',
  falsifier:
    'If source-bound Bull1:W rows lose the 405/806 readings, or if non-Bull1:W square seals with 405/806 continue to grow while Bull1:W support does not, demote the subtype-marker bet. If leave-Harappa remains weak after source audit, treat this as a Harappan scribal-subtype convention rather than pan-IVC icon semantics.',
  next_prediction:
    'New square-seal Bull1:W rows, especially Harappa/Lothal/Lakhanjo-daro rows, should carry 405 or 806 above the square-seal background rate; non-Bull1:W rows carrying both signs should remain rare.',
  key_controls: {
    seal_s_either: sealEither,
    square_either: squareEither,
    complete_either: completeEither,
    non_poor_either: nonPoorEither,
    without_mohenjo_either: withoutMohenjoEither,
    without_harappa_either: withoutHarappaEither,
    seal_s_405: seal405,
    seal_s_806: seal806,
  },
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), JSON.stringify({
  ...summary,
  support_rows: supportRows,
  outside_target_rows_sample: outsideRows,
  target_summaries: summaries,
}, null, 2), 'utf8');
writeCsv(path.join(OUT_DIR, `${PREFIX}_summaries.csv`), summaries, [
  'target_kind',
  'pool',
  'pool_rows',
  'context_rows',
  'background_rows',
  'target_a',
  'target_c',
  'target_total',
  'fisher_p',
  'bonferroni_p',
  'all_sign_rank',
  'maxstat_fpr',
  'all_pair_rank',
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
  'has_405',
  'has_806',
  'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_outside_target_rows_sample.csv`), outsideRows, [
  'object',
  'site',
  'type',
  'symbol',
  'condition',
  'complete',
  'has_405',
  'has_806',
  'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_top_signs.csv`), topRows, [
  'source',
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
writeCsv(path.join(OUT_DIR, `${PREFIX}_top_pairs.csv`), topPairs, [
  'source',
  'pair',
  'a',
  'c',
  'total',
  'fisher_p',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_forger_iterations.csv`), iterationRows, [
  'pool',
  'target_kind',
  'iteration',
  'best_p',
  'target_label_shuffle_p',
  'ge_observed',
]);

console.log(JSON.stringify(summary, null, 2));
