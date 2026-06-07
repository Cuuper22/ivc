import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_407_806_register_slot_split_forger_20260531';
const RUN_DATE = '2026-05-31';
const OPENER = '407';
const CLOSER = '806';
const ITERATIONS = 3000;
const MIN_PAIR_OCCURRENCES = 12;

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

const fisherCache = new Map();
function fisherRightTail(a, b, c, d) {
  const key = `${a},${b},${c},${d}`;
  if (fisherCache.has(key)) return fisherCache.get(key);
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
  const clipped = Math.max(0, Math.min(1, p));
  fisherCache.set(key, clipped);
  return clipped;
}

function minusLog10(p) {
  return -Math.log10(Math.max(p, Number.MIN_VALUE));
}

function mulberry32(seed) {
  return function rand() {
    let t = (seed += 0x6D2B79F5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffleInPlace(arr, rand) {
  for (let i = arr.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    const tmp = arr[i];
    arr[i] = arr[j];
    arr[j] = tmp;
  }
}

function registerContext(row) {
  return norm(row.type) === 'SEAL:R' || norm(row.type) === 'TAB:C';
}

function boundaryNext(next) {
  return next === '<END>' || next === '002';
}

function occurrenceRows(rows) {
  const occs = [];
  for (const row of rows) {
    for (let idx = 0; idx < row.signs.length; idx += 1) {
      occs.push({
        sign: row.signs[idx],
        object: objectId(row),
        site: norm(row.site),
        type: norm(row.type),
        material: norm(row.material),
        shape: norm(row.shape),
        condition: norm(row.condition),
        complete: norm(row.complete),
        text: row.text,
        position: idx,
        length: row.signs.length,
        prev: row.signs[idx - 1] ?? '<START>',
        next: row.signs[idx + 1] ?? '<END>',
        initial: idx === 0,
        terminal: idx === row.signs.length - 1,
        boundary: boundaryNext(row.signs[idx + 1] ?? '<END>'),
      });
    }
  }
  return occs;
}

function summarizeSigns(occs) {
  const stats = new Map();
  for (const occ of occs) {
    if (!stats.has(occ.sign)) {
      stats.set(occ.sign, { sign: occ.sign, occurrences: 0, rows: new Set(), initial: 0, terminal: 0, boundary: 0 });
    }
    const stat = stats.get(occ.sign);
    stat.occurrences += 1;
    stat.rows.add(occ.object);
    if (occ.initial) stat.initial += 1;
    if (occ.terminal) stat.terminal += 1;
    if (occ.boundary) stat.boundary += 1;
  }
  return [...stats.values()].map((stat) => ({
    sign: stat.sign,
    occurrences: stat.occurrences,
    row_count: stat.rows.size,
    initial: stat.initial,
    initial_share: stat.initial / stat.occurrences,
    terminal: stat.terminal,
    terminal_share: stat.terminal / stat.occurrences,
    boundary: stat.boundary,
    boundary_share: stat.boundary / stat.occurrences,
  }));
}

function pairScoreFromStats(opener, closer) {
  if (!opener || !closer) return null;
  const initial_p = fisherRightTail(
    opener.initial,
    opener.occurrences - opener.initial,
    closer.initial,
    closer.occurrences - closer.initial,
  );
  const boundary_p = fisherRightTail(
    closer.boundary,
    closer.occurrences - closer.boundary,
    opener.boundary,
    opener.occurrences - opener.boundary,
  );
  const terminal_p = fisherRightTail(
    closer.terminal,
    closer.occurrences - closer.terminal,
    opener.terminal,
    opener.occurrences - opener.terminal,
  );
  const composite_score = minusLog10(initial_p) + minusLog10(boundary_p);
  return {
    opener: opener.sign,
    closer: closer.sign,
    opener_occurrences: opener.occurrences,
    closer_occurrences: closer.occurrences,
    opener_initial: opener.initial,
    opener_initial_share: opener.initial_share,
    closer_initial: closer.initial,
    closer_initial_share: closer.initial_share,
    closer_boundary: closer.boundary,
    closer_boundary_share: closer.boundary_share,
    opener_boundary: opener.boundary,
    opener_boundary_share: opener.boundary_share,
    closer_terminal: closer.terminal,
    closer_terminal_share: closer.terminal_share,
    opener_terminal: opener.terminal,
    opener_terminal_share: opener.terminal_share,
    initial_fisher_p: initial_p,
    boundary_fisher_p: boundary_p,
    terminal_fisher_p: terminal_p,
    composite_score,
  };
}

function bestOrderedPairs(stats, candidateSigns) {
  const bySign = new Map(stats.map((stat) => [stat.sign, stat]));
  const rows = [];
  for (const openerSign of candidateSigns) {
    const opener = bySign.get(openerSign);
    if (!opener) continue;
    for (const closerSign of candidateSigns) {
      if (openerSign === closerSign) continue;
      const closer = bySign.get(closerSign);
      if (!closer) continue;
      const scored = pairScoreFromStats(opener, closer);
      if (!scored) continue;
      rows.push(scored);
    }
  }
  return rows.sort((a, b) => b.composite_score - a.composite_score || a.opener.localeCompare(b.opener, undefined, { numeric: true }));
}

function analyzePool(name, rows) {
  const occs = occurrenceRows(rows);
  const signRows = summarizeSigns(occs).sort((a, b) => b.occurrences - a.occurrences || a.sign.localeCompare(b.sign, undefined, { numeric: true }));
  const bySign = new Map(signRows.map((row) => [row.sign, row]));
  const target = pairScoreFromStats(bySign.get(OPENER), bySign.get(CLOSER));
  const allCandidates = signRows.filter((row) => row.occurrences >= MIN_PAIR_OCCURRENCES).map((row) => row.sign);
  const low = Math.floor(Math.min(target?.opener_occurrences ?? 0, target?.closer_occurrences ?? 0) * 0.5);
  const high = Math.ceil(Math.max(target?.opener_occurrences ?? 0, target?.closer_occurrences ?? 0) * 1.5);
  const frequencyCandidates = signRows
    .filter((row) => row.occurrences >= low && row.occurrences <= high)
    .map((row) => row.sign);
  const allPairs = target ? bestOrderedPairs(signRows, allCandidates) : [];
  const freqPairs = target ? bestOrderedPairs(signRows, frequencyCandidates) : [];
  const allRank = allPairs.findIndex((row) => row.opener === OPENER && row.closer === CLOSER);
  const freqRank = freqPairs.findIndex((row) => row.opener === OPENER && row.closer === CLOSER);
  return {
    name,
    rows: rows.length,
    occurrences: occs.length,
    sign_rows: signRows,
    target,
    all_pair_rank: target ? `${allRank >= 0 ? allRank + 1 : 'not_in_scan'}/${allPairs.length}` : 'NA',
    frequency_matched_pair_rank: target ? `${freqRank >= 0 ? freqRank + 1 : 'not_in_scan'}/${freqPairs.length}` : 'NA',
    frequency_match_min_occurrences: low,
    frequency_match_max_occurrences: high,
    top_all_pairs: allPairs.slice(0, 30),
    top_frequency_matched_pairs: freqPairs.slice(0, 30),
  };
}

function rowPreservingForger(rows, targetScore, iterations = ITERATIONS) {
  const occs = occurrenceRows(rows);
  const labels = occs.map((occ) => occ.sign);
  const signCounts = new Map();
  for (const sign of labels) signCounts.set(sign, (signCounts.get(sign) ?? 0) + 1);
  const signList = [...signCounts.entries()]
    .filter(([, count]) => count >= MIN_PAIR_OCCURRENCES)
    .map(([sign]) => sign)
    .sort();
  const targetOpenerCount = signCounts.get(OPENER) ?? 0;
  const targetCloserCount = signCounts.get(CLOSER) ?? 0;
  const low = Math.floor(Math.min(targetOpenerCount, targetCloserCount) * 0.5);
  const high = Math.ceil(Math.max(targetOpenerCount, targetCloserCount) * 1.5);
  const frequencySigns = signList.filter((sign) => {
    const count = signCounts.get(sign);
    return count >= low && count <= high;
  });
  const allIndexes = new Map(signList.map((sign, idx) => [sign, idx]));
  const frequencySet = new Set(frequencySigns);
  const rand = mulberry32(0x407806 ^ rows.length ^ occs.length);
  let allGe = 0;
  let frequencyGe = 0;
  const shuffled = labels.slice();
  const iterationRows = [];

  for (let iter = 0; iter < iterations; iter += 1) {
    shuffleInPlace(shuffled, rand);
    const stats = signList.map((sign) => ({
      sign,
      occurrences: signCounts.get(sign),
      row_count: 0,
      initial: 0,
      initial_share: 0,
      terminal: 0,
      terminal_share: 0,
      boundary: 0,
      boundary_share: 0,
    }));
    for (let i = 0; i < shuffled.length; i += 1) {
      const sign = shuffled[i];
      const statIdx = allIndexes.get(sign);
      if (statIdx === undefined) continue;
      const stat = stats[statIdx];
      if (occs[i].initial) stat.initial += 1;
      if (occs[i].terminal) stat.terminal += 1;
      if (occs[i].boundary) stat.boundary += 1;
    }
    for (const stat of stats) {
      stat.initial_share = stat.initial / stat.occurrences;
      stat.terminal_share = stat.terminal / stat.occurrences;
      stat.boundary_share = stat.boundary / stat.occurrences;
    }

    let bestAll = 0;
    let bestFrequency = 0;
    for (let i = 0; i < stats.length; i += 1) {
      const opener = stats[i];
      for (let j = 0; j < stats.length; j += 1) {
        if (i === j) continue;
        const closer = stats[j];
        const scored = pairScoreFromStats(opener, closer);
        const score = scored.composite_score;
        if (score > bestAll) bestAll = score;
        if (frequencySet.has(opener.sign) && frequencySet.has(closer.sign) && score > bestFrequency) bestFrequency = score;
      }
    }

    if (bestAll >= targetScore) allGe += 1;
    if (bestFrequency >= targetScore) frequencyGe += 1;
    if (iter < 50 || bestAll >= targetScore || bestFrequency >= targetScore) {
      iterationRows.push({
        iteration: iter,
        best_all_composite_score: bestAll,
        best_frequency_matched_composite_score: bestFrequency,
        all_ge_target: String(bestAll >= targetScore),
        frequency_ge_target: String(bestFrequency >= targetScore),
      });
    }
  }
  return {
    iterations,
    all_pair_maxstat_fpr: allGe / iterations,
    frequency_matched_pair_maxstat_fpr: frequencyGe / iterations,
    all_candidate_signs: signList.length,
    frequency_matched_candidate_signs: frequencySigns.length,
    iteration_rows: iterationRows,
  };
}

function supportRows(rows) {
  return rows
    .filter((row) => row.signSet.has(OPENER) || row.signSet.has(CLOSER))
    .map((row) => {
      const openerIndexes = row.signs.map((sign, idx) => (sign === OPENER ? idx : -1)).filter((idx) => idx >= 0);
      const closerIndexes = row.signs.map((sign, idx) => (sign === CLOSER ? idx : -1)).filter((idx) => idx >= 0);
      const openerBeforeCloser = openerIndexes.some((openerIdx) => closerIndexes.some((closerIdx) => openerIdx < closerIdx));
      const closerBeforeOpener = closerIndexes.some((closerIdx) => openerIndexes.some((openerIdx) => closerIdx < openerIdx));
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
        has_407: String(row.signSet.has(OPENER)),
        has_806: String(row.signSet.has(CLOSER)),
        has_both: String(row.signSet.has(OPENER) && row.signSet.has(CLOSER)),
        first_407_position: openerIndexes[0] ?? '',
        first_806_position: closerIndexes[0] ?? '',
        opener_before_closer: String(openerBeforeCloser),
        closer_before_opener: String(closerBeforeOpener),
        text: row.text,
      };
    });
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()]
  .map((row, idx) => ({ ...row, _idx: idx, signSet: new Set(row.signs) }));

const registerRows = canonicalRows.filter(registerContext);
const pools = [
  analyzePool('register_all_seal_r_or_tab_c', registerRows),
  analyzePool('register_complete_only', registerRows.filter((row) => norm(row.complete) === 'Y')),
  analyzePool('register_non_poor_only', registerRows.filter((row) => norm(row.condition) !== 'Poor')),
  analyzePool('register_without_mohenjo_daro', registerRows.filter((row) => norm(row.site) !== 'Mohenjo-daro')),
  analyzePool('register_without_harappa', registerRows.filter((row) => norm(row.site) !== 'Harappa')),
  analyzePool('seal_r_only', registerRows.filter((row) => norm(row.type) === 'SEAL:R')),
  analyzePool('tab_c_only', registerRows.filter((row) => norm(row.type) === 'TAB:C')),
];
const main = pools[0];
const forger = rowPreservingForger(registerRows, main.target.composite_score);

const cooccurrenceRows = registerRows.filter((row) => row.signSet.has(OPENER) && row.signSet.has(CLOSER));
const cooccurrenceSupport = supportRows(cooccurrenceRows);
const both407Before806 = cooccurrenceSupport.filter((row) => row.opener_before_closer === 'true').length;
const both806Before407 = cooccurrenceSupport.filter((row) => row.closer_before_opener === 'true').length;

const controlPasses = pools.slice(1, 6).filter((pool) =>
  pool.target &&
  pool.target.opener_occurrences >= 6 &&
  pool.target.closer_occurrences >= 6 &&
  pool.target.initial_fisher_p <= 0.01 &&
  pool.target.boundary_fisher_p <= 0.01,
).length;
const tier =
  main.target.initial_fisher_p <= 0.01 &&
  main.target.boundary_fisher_p <= 0.01 &&
  forger.frequency_matched_pair_maxstat_fpr <= 0.01 &&
  controlPasses >= 3
    ? forger.all_pair_maxstat_fpr <= 0.01 && controlPasses >= 4
      ? 'promoted candidate'
      : 'candidate'
    : 'wild shot';

const poolSummaries = pools.map((pool) => ({
  pool: pool.name,
  rows: pool.rows,
  occurrences: pool.occurrences,
  all_pair_rank: pool.all_pair_rank,
  frequency_matched_pair_rank: pool.frequency_matched_pair_rank,
  frequency_match_min_occurrences: pool.frequency_match_min_occurrences,
  frequency_match_max_occurrences: pool.frequency_match_max_occurrences,
  ...pool.target,
}));

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V4_407_806_REGISTER_SLOT_SPLIT_20260531',
  vector: 'V4 context-to-meaning without sound; V2 slot grammar',
  confidence_tier: tier,
  risky_bet:
    '`407` and `806` are not redundant rectangular/copper register tags. In the shared `SEAL:R`/`TAB:C` register, `407` behaves like an entry/opening marker while `806` behaves like a boundary/closure pivot before `END` or `002`. This predicts slot function only, not sound, language, or translation.',
  observed:
    `In ${main.rows} canonical SEAL:R/TAB:C rows, ${OPENER} has ${main.target.opener_initial}/${main.target.opener_occurrences} initial occurrences and ${main.target.opener_boundary}/${main.target.opener_occurrences} boundary-next occurrences; ` +
    `${CLOSER} has ${main.target.closer_initial}/${main.target.closer_occurrences} initial occurrences and ${main.target.closer_boundary}/${main.target.closer_occurrences} boundary-next occurrences. ` +
    `Direct 407-vs-806 initial Fisher=${main.target.initial_fisher_p}; direct 806-vs-407 boundary Fisher=${main.target.boundary_fisher_p}; composite score=${main.target.composite_score}. ` +
    `Ordered-pair rank=${main.all_pair_rank}; frequency-matched rank=${main.frequency_matched_pair_rank}. ` +
    `Co-occurrence rows=${cooccurrenceRows.length}; 407 precedes 806 in ${both407Before806}/${cooccurrenceRows.length}, 806 precedes 407 in ${both806Before407}/${cooccurrenceRows.length}.`,
  adversarial_test:
    `Canonical numeric-sequence collapse; row-position role test inside the same SEAL:R/TAB:C register; ordered-pair all-sign scan; frequency-matched ordered-pair scan; ${ITERATIONS}-iteration row-preserving sign-label forger that preserves register row lengths and exact sign frequencies; complete-only, non-poor-only, leave-Mohenjo, leave-Harappa, SEAL:R-only, and TAB:C-only controls.`,
  false_positive_rate: forger.frequency_matched_pair_maxstat_fpr,
  all_pair_maxstat_fpr: forger.all_pair_maxstat_fpr,
  frequency_matched_pair_maxstat_fpr: forger.frequency_matched_pair_maxstat_fpr,
  direct_initial_fisher_p: main.target.initial_fisher_p,
  direct_boundary_fisher_p: main.target.boundary_fisher_p,
  cooccurrence_rows: cooccurrenceRows.length,
  controls_passing_strict_direct_pair: controlPasses,
  falsifier:
    'If source-checked SEAL:R/TAB:C rows put 407 frequently before END/002, or put 806 frequently as row-initial opener, or if frequency-preserving row shuffles routinely find equally strong opener/closer splits among similarly frequent signs, kill the role split and fall back to two independent register enrichments.',
  next_prediction:
    'Held-out or newly source-checked SEAL:R/TAB:C rows containing 407 should usually place it at row start or early internal entry position; rows containing 806 should often place it before END or 002. Rows containing both should usually read with 407 before a later 806, except where a nested 154/158-806-46x pivot precedes the 407 subentry.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({
    ...summary,
    pools: poolSummaries,
    forger: {
      iterations: forger.iterations,
      all_pair_maxstat_fpr: forger.all_pair_maxstat_fpr,
      frequency_matched_pair_maxstat_fpr: forger.frequency_matched_pair_maxstat_fpr,
      all_candidate_signs: forger.all_candidate_signs,
      frequency_matched_candidate_signs: forger.frequency_matched_candidate_signs,
    },
    main_top_all_pairs: main.top_all_pairs,
    main_top_frequency_matched_pairs: main.top_frequency_matched_pairs,
    cooccurrence_support: cooccurrenceSupport,
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
  'all_pair_maxstat_fpr',
  'frequency_matched_pair_maxstat_fpr',
  'direct_initial_fisher_p',
  'direct_boundary_fisher_p',
  'cooccurrence_rows',
  'controls_passing_strict_direct_pair',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_pools.csv`), poolSummaries, [
  'pool',
  'rows',
  'occurrences',
  'all_pair_rank',
  'frequency_matched_pair_rank',
  'frequency_match_min_occurrences',
  'frequency_match_max_occurrences',
  'opener',
  'closer',
  'opener_occurrences',
  'closer_occurrences',
  'opener_initial',
  'opener_initial_share',
  'closer_initial',
  'closer_initial_share',
  'closer_boundary',
  'closer_boundary_share',
  'opener_boundary',
  'opener_boundary_share',
  'closer_terminal',
  'closer_terminal_share',
  'opener_terminal',
  'opener_terminal_share',
  'initial_fisher_p',
  'boundary_fisher_p',
  'terminal_fisher_p',
  'composite_score',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_support_rows.csv`), supportRows(registerRows), [
  'object',
  'site',
  'region',
  'type',
  'material',
  'shape',
  'symbol',
  'condition',
  'complete',
  'has_407',
  'has_806',
  'has_both',
  'first_407_position',
  'first_806_position',
  'opener_before_closer',
  'closer_before_opener',
  'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_top_all_pairs.csv`), main.top_all_pairs, [
  'opener',
  'closer',
  'opener_occurrences',
  'closer_occurrences',
  'opener_initial',
  'opener_initial_share',
  'closer_initial',
  'closer_initial_share',
  'closer_boundary',
  'closer_boundary_share',
  'opener_boundary',
  'opener_boundary_share',
  'initial_fisher_p',
  'boundary_fisher_p',
  'terminal_fisher_p',
  'composite_score',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_top_frequency_matched_pairs.csv`), main.top_frequency_matched_pairs, [
  'opener',
  'closer',
  'opener_occurrences',
  'closer_occurrences',
  'opener_initial',
  'opener_initial_share',
  'closer_initial',
  'closer_initial_share',
  'closer_boundary',
  'closer_boundary_share',
  'opener_boundary',
  'opener_boundary_share',
  'initial_fisher_p',
  'boundary_fisher_p',
  'terminal_fisher_p',
  'composite_score',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_forger_iterations.csv`), forger.iteration_rows, [
  'iteration',
  'best_all_composite_score',
  'best_frequency_matched_composite_score',
  'all_ge_target',
  'frequency_ge_target',
]);

console.log(JSON.stringify(summary, null, 2));
