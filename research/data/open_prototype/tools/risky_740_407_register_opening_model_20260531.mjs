// Models how the rectangular-seal/copper-tablet register (SEAL:R, TAB:C) opens.
// Two claims are tested separately. Claim one: `740` is the register's broad
// default opener — the most initial-biased sign of all. Claim two (stricter): when
// `740` and the narrower opener `407` co-occur, 740 should come first — a nesting
// hierarchy that is killed if collision rows are mixed. The script reads
// metadata_filtered.csv, collapses duplicate sign sequences, keeps register rows,
// and Fisher-ranks every sign by initial-position bias. A 3,000-iteration forger
// shuffles sign labels over occurrence slots (keeping row lengths and sign
// frequencies) and asks how often the best sign matches 740's p. Six control pools
// recheck the rank; the collision model counts orders in rows containing both
// signs and compares 407's initial rate with and without 740 present. Writes a bet
// summary (JSON + CSV) plus pool, initial-sign, support-row, and forger CSVs to
// the reports directory.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_740_407_register_opening_model_20260531';
const RUN_DATE = '2026-05-31';
const BROAD_OPENER = '740';
const NARROW_OPENER = '407';
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

function occurrenceRows(rows) {
  const occs = [];
  for (const row of rows) {
    for (let idx = 0; idx < row.signs.length; idx += 1) {
      occs.push({
        sign: row.signs[idx],
        initial: idx === 0,
        row,
      });
    }
  }
  return occs;
}

function summarizeInitial(occs) {
  const bySign = new Map();
  for (const occ of occs) {
    if (!bySign.has(occ.sign)) bySign.set(occ.sign, { sign: occ.sign, occurrences: 0, initial: 0 });
    const stat = bySign.get(occ.sign);
    stat.occurrences += 1;
    if (occ.initial) stat.initial += 1;
  }
  const totalInitial = occs.filter((occ) => occ.initial).length;
  return [...bySign.values()].map((stat) => {
    const c = totalInitial - stat.initial;
    const d = occs.length - stat.occurrences - c;
    const p = fisherRightTail(stat.initial, stat.occurrences - stat.initial, c, d);
    return {
      sign: stat.sign,
      occurrences: stat.occurrences,
      initial: stat.initial,
      initial_share: stat.initial / stat.occurrences,
      background_initial: c,
      background_occurrences: occs.length - stat.occurrences,
      fisher_p: p,
    };
  }).sort((a, b) => a.fisher_p - b.fisher_p || b.initial_share - a.initial_share || b.initial - a.initial || a.sign.localeCompare(b.sign, undefined, { numeric: true }));
}

function initialForger(rows, targetP, iterations = ITERATIONS) {
  const occs = occurrenceRows(rows);
  const labels = occs.map((occ) => occ.sign);
  const rand = mulberry32(0x740407 ^ rows.length ^ occs.length);
  const shuffled = labels.slice();
  let maxGe = 0;
  const iterationRows = [];
  for (let iter = 0; iter < iterations; iter += 1) {
    shuffleInPlace(shuffled, rand);
    const fakeOccs = occs.map((occ, idx) => ({ ...occ, sign: shuffled[idx] }));
    const top = summarizeInitial(fakeOccs)[0];
    if (top.fisher_p <= targetP) maxGe += 1;
    if (iter < 50 || top.fisher_p <= targetP) {
      iterationRows.push({
        iteration: iter,
        best_sign: top.sign,
        best_initial: top.initial,
        best_occurrences: top.occurrences,
        best_fisher_p: top.fisher_p,
        ge_target: String(top.fisher_p <= targetP),
      });
    }
  }
  return { iterations, maxstat_fpr: maxGe / iterations, iteration_rows: iterationRows };
}

function analyzePool(name, rows) {
  const occs = occurrenceRows(rows);
  const signs = summarizeInitial(occs);
  const target = signs.find((row) => row.sign === BROAD_OPENER);
  const narrow = signs.find((row) => row.sign === NARROW_OPENER);
  const targetRank = signs.findIndex((row) => row.sign === BROAD_OPENER) + 1;
  const narrowRank = signs.findIndex((row) => row.sign === NARROW_OPENER) + 1;
  return {
    pool: name,
    rows: rows.length,
    occurrences: occs.length,
    target_rank: `${targetRank}/${signs.length}`,
    narrow_rank: `${narrowRank}/${signs.length}`,
    target,
    narrow,
    top_initial_signs: signs.slice(0, 25),
  };
}

function collisionModel(rows) {
  const hasBroad = rows.filter((row) => row.signSet.has(BROAD_OPENER));
  const hasNarrow = rows.filter((row) => row.signSet.has(NARROW_OPENER));
  const both = rows.filter((row) => row.signSet.has(BROAD_OPENER) && row.signSet.has(NARROW_OPENER));
  const onlyNarrow = rows.filter((row) => row.signSet.has(NARROW_OPENER) && !row.signSet.has(BROAD_OPENER));
  const first = (row, sign) => row.signs.indexOf(sign) === 0;
  const pos = (row, sign) => row.signs.indexOf(sign);
  const onlyNarrowInitial = onlyNarrow.filter((row) => first(row, NARROW_OPENER)).length;
  const bothNarrowInitial = both.filter((row) => first(row, NARROW_OPENER)).length;
  const bothBroadBeforeNarrow = both.filter((row) => pos(row, BROAD_OPENER) < pos(row, NARROW_OPENER)).length;
  const bothNarrowBeforeBroad = both.filter((row) => pos(row, NARROW_OPENER) < pos(row, BROAD_OPENER)).length;
  const pNarrowInitialWithoutBroad = fisherRightTail(
    onlyNarrowInitial,
    onlyNarrow.length - onlyNarrowInitial,
    bothNarrowInitial,
    both.length - bothNarrowInitial,
  );
  return {
    rows: rows.length,
    has_broad_opener_rows: hasBroad.length,
    has_narrow_opener_rows: hasNarrow.length,
    both_rows: both.length,
    only_narrow_rows: onlyNarrow.length,
    only_narrow_initial: onlyNarrowInitial,
    both_narrow_initial: bothNarrowInitial,
    both_broad_before_narrow: bothBroadBeforeNarrow,
    both_narrow_before_broad: bothNarrowBeforeBroad,
    narrow_initial_without_broad_vs_with_broad_fisher_p: pNarrowInitialWithoutBroad,
    strict_nesting_tier:
      both.length >= 10 && bothBroadBeforeNarrow / both.length >= 0.8 && bothNarrowBeforeBroad / both.length <= 0.1
        ? 'candidate'
        : 'wild shot',
    strict_nesting_verdict:
      both.length >= 10 && bothBroadBeforeNarrow / both.length >= 0.8 && bothNarrowBeforeBroad / both.length <= 0.1
        ? 'not_killed'
        : 'killed_by_mixed_order_collision_rows',
  };
}

function supportRows(rows) {
  return rows
    .filter((row) => row.signSet.has(BROAD_OPENER) || row.signSet.has(NARROW_OPENER))
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
      has_740: String(row.signSet.has(BROAD_OPENER)),
      has_407: String(row.signSet.has(NARROW_OPENER)),
      first_sign: row.signs[0] ?? '',
      first_740_position: row.signs.indexOf(BROAD_OPENER) >= 0 ? row.signs.indexOf(BROAD_OPENER) : '',
      first_407_position: row.signs.indexOf(NARROW_OPENER) >= 0 ? row.signs.indexOf(NARROW_OPENER) : '',
      text: row.text,
    }));
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()]
  .map((row) => ({ ...row, signSet: new Set(row.signs) }));
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
const forger = initialForger(registerRows, main.target.fisher_p);
const collision = collisionModel(registerRows);
const strictControls = pools.slice(1, 6).filter((pool) => pool.target.fisher_p <= 0.01 && pool.target_rank.startsWith('1/')).length;
const broadTier =
  main.target_rank.startsWith('1/') &&
  main.target.fisher_p <= 0.01 &&
  forger.maxstat_fpr <= 0.01 &&
  strictControls >= 3
    ? 'promoted candidate'
    : 'candidate';

const poolSummaries = pools.map((pool) => ({
  pool: pool.pool,
  rows: pool.rows,
  occurrences: pool.occurrences,
  broad_opener_rank: pool.target_rank,
  broad_opener_occurrences: pool.target.occurrences,
  broad_opener_initial: pool.target.initial,
  broad_opener_initial_share: pool.target.initial_share,
  broad_opener_fisher_p: pool.target.fisher_p,
  narrow_opener_rank: pool.narrow_rank,
  narrow_opener_occurrences: pool.narrow.occurrences,
  narrow_opener_initial: pool.narrow.initial,
  narrow_opener_initial_share: pool.narrow.initial_share,
  narrow_opener_fisher_p: pool.narrow.fisher_p,
}));

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V2_V4_740_407_REGISTER_OPENING_MODEL_20260531',
  vector: 'V4 context-to-meaning without sound; V2 slot grammar',
  confidence_tier: broadTier,
  risky_bet:
    '`740` is the broad default opener of the SEAL:R/TAB:C register. `407` is a narrower independent opener in the same register, not a strict child of 740. The stricter hierarchy bet, where 740 should consistently precede 407 when both appear, is tested separately and is killed if collision rows are mixed.',
  observed:
    `Broad opener: ${BROAD_OPENER} is initial in ${main.target.initial}/${main.target.occurrences} register occurrences, rank ${main.target_rank}, Fisher=${main.target.fisher_p}, forger FPR=${forger.maxstat_fpr}. ` +
    `Narrow opener: ${NARROW_OPENER} is initial in ${main.narrow.initial}/${main.narrow.occurrences}, rank ${main.narrow_rank}, Fisher=${main.narrow.fisher_p}. ` +
    `Collision rows: ${collision.both_rows}; ${BROAD_OPENER} before ${NARROW_OPENER} in ${collision.both_broad_before_narrow}/${collision.both_rows}, ${NARROW_OPENER} before ${BROAD_OPENER} in ${collision.both_narrow_before_broad}/${collision.both_rows}. ` +
    `When ${NARROW_OPENER} occurs without ${BROAD_OPENER}, it is initial in ${collision.only_narrow_initial}/${collision.only_narrow_rows}; when both occur, ${NARROW_OPENER} is initial in ${collision.both_narrow_initial}/${collision.both_rows}; Fisher=${collision.narrow_initial_without_broad_vs_with_broad_fisher_p}. Strict nesting verdict: ${collision.strict_nesting_verdict}.`,
  adversarial_test:
    `Canonical numeric-sequence collapse; all-sign initial-position rank inside SEAL:R/TAB:C; ${ITERATIONS}-iteration row-preserving sign-label forger preserving row lengths and exact sign frequencies; complete-only, non-poor-only, leave-Mohenjo, leave-Harappa, SEAL:R-only, TAB:C-only controls; direct collision-row test for the stricter 740-before-407 hierarchy.`,
  false_positive_rate: forger.maxstat_fpr,
  broad_opener_fisher_p: main.target.fisher_p,
  narrow_opener_fisher_p: main.narrow.fisher_p,
  strict_nesting_tier: collision.strict_nesting_tier,
  strict_nesting_verdict: collision.strict_nesting_verdict,
  falsifier:
    'If source-checked SEAL:R/TAB:C rows no longer put 740 preferentially in first position, demote the broad-opener claim. If future 740+407 collision rows strongly converge on 740 before 407, revive the strict nesting model; if they stay mixed, keep 407 as an independent/narrow opener instead.',
  next_prediction:
    'Held-out SEAL:R/TAB:C rows should overproduce 740 in first position. Rows with 407 but without 740 should often put 407 first. Rows with both 740 and 407 should not be forced into one order; mixed order is predicted under the independent-opener model.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({
    ...summary,
    pools: poolSummaries,
    forger: { iterations: forger.iterations, maxstat_fpr: forger.maxstat_fpr },
    collision_model: collision,
    top_initial_signs: main.top_initial_signs,
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
  'broad_opener_fisher_p',
  'narrow_opener_fisher_p',
  'strict_nesting_tier',
  'strict_nesting_verdict',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_pools.csv`), poolSummaries, [
  'pool',
  'rows',
  'occurrences',
  'broad_opener_rank',
  'broad_opener_occurrences',
  'broad_opener_initial',
  'broad_opener_initial_share',
  'broad_opener_fisher_p',
  'narrow_opener_rank',
  'narrow_opener_occurrences',
  'narrow_opener_initial',
  'narrow_opener_initial_share',
  'narrow_opener_fisher_p',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_top_initial_signs.csv`), main.top_initial_signs, [
  'sign',
  'occurrences',
  'initial',
  'initial_share',
  'background_initial',
  'background_occurrences',
  'fisher_p',
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
  'has_740',
  'has_407',
  'first_sign',
  'first_740_position',
  'first_407_position',
  'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_forger_iterations.csv`), forger.iteration_rows, [
  'iteration',
  'best_sign',
  'best_initial',
  'best_occurrences',
  'best_fisher_p',
  'ge_target',
]);

console.log(JSON.stringify(summary, null, 2));
