// Tests whether sign `060` is a "terminal-cap hinge": a sign whose immediate
// successors form a paradigm of caps (920, 692, 550, 820) that normally close the
// inscription. The script reads metadata_filtered.csv (complete rows only), collapses
// every bigram occurrence to an exact cell (deduplicated on sign, next, following
// sign, text, site, type, and iconography), and calls a successor branch a "cap" if
// it has enough cells (20 for the large tier, 5 for medium) and at least 85% of them
// are terminal. Every predecessor sign in the corpus is ranked the same way, so 060
// competes against the whole corpus, not a hand-picked shortlist. A 5,000-iteration
// null shuffles terminal/nonterminal labels over all branch cells (keeping branch
// sizes) and prices both 060's cap-branch count and the corpus-wide maximum. Writes
// a JSON report plus sign-ranking and branch CSVs to the reports directory.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_060_terminal_cap_paradigm_20260531';
const RUN_DATE = '2026-05-31';
const ITERATIONS = 5000;
const LARGE_MIN_N = 20;
const MEDIUM_MIN_N = 5;
const CAP_SHARE = 0.85;

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

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function exactKey(parts) {
  return parts.join('|');
}

function esc(value) {
  const text = Array.isArray(value) ? value.join(' | ') : String(value ?? '');
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const body = rows.map((row) => fields.map((field) => esc(row[field])).join(',')).join('\n');
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`, 'utf8');
}

function mulberry32(seed) {
  return function rand() {
    let t = seed += 0x6D2B79F5;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function fisherYates(values, rand) {
  const out = values.slice();
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function summarizeBranch(items) {
  const terminal = items.filter((item) => item.next2 === '<END>').length;
  return {
    sign: items[0].sign,
    next: items[0].next,
    exact_cells: items.length,
    terminal_cells: terminal,
    terminal_share: items.length ? terminal / items.length : 0,
    sites: new Set(items.map((item) => item.site)).size,
    types: new Set(items.map((item) => item.type)).size,
    symbols: new Set(items.map((item) => item.symbol)).size,
    examples: items.slice(0, 6).map((item) => `${item.cisi}:${item.text}`),
  };
}

function scoreSign(branches, minN) {
  const capBranches = branches.filter((branch) => branch.exact_cells >= minN && branch.terminal_share >= CAP_SHARE);
  return {
    cap_branch_count: capBranches.length,
    cap_exact_cells: capBranches.reduce((sum, branch) => sum + branch.exact_cells, 0),
    cap_terminal_cells: capBranches.reduce((sum, branch) => sum + branch.terminal_cells, 0),
    cap_branches: capBranches.map((branch) => branch.next),
  };
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const cellMap = new Map();

for (const row of rows) {
  const toks = tokens(row.text);
  for (let i = 0; i < toks.length - 1; i += 1) {
    const sign = toks[i];
    const next = toks[i + 1];
    const next2 = toks[i + 2] ?? '<END>';
    const key = exactKey([sign, next, next2, row.text, row.site, row.type, row.symbol]);
    if (!cellMap.has(key)) {
      cellMap.set(key, {
        sign,
        next,
        next2,
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        text: row.text,
        cisi: row.cisi,
      });
    }
  }
}

const cells = [...cellMap.values()];
const branchesByKey = new Map();
for (const cell of cells) {
  const key = `${cell.sign}-${cell.next}`;
  if (!branchesByKey.has(key)) branchesByKey.set(key, []);
  branchesByKey.get(key).push(cell);
}

const branchRows = [...branchesByKey.values()].map(summarizeBranch)
  .sort((a, b) => b.exact_cells - a.exact_cells || b.terminal_share - a.terminal_share || a.sign.localeCompare(b.sign) || a.next.localeCompare(b.next));

const bySign = new Map();
for (const branch of branchRows) {
  if (!bySign.has(branch.sign)) bySign.set(branch.sign, []);
  bySign.get(branch.sign).push(branch);
}

const signRows = [...bySign.entries()].map(([sign, branches]) => {
  const large = scoreSign(branches, LARGE_MIN_N);
  const medium = scoreSign(branches, MEDIUM_MIN_N);
  return {
    sign,
    outgoing_exact_cells: branches.reduce((sum, branch) => sum + branch.exact_cells, 0),
    successor_branches: branches.length,
    large_cap_branch_count: large.cap_branch_count,
    large_cap_exact_cells: large.cap_exact_cells,
    large_cap_terminal_cells: large.cap_terminal_cells,
    large_cap_branches: large.cap_branches.join(' '),
    medium_cap_branch_count: medium.cap_branch_count,
    medium_cap_exact_cells: medium.cap_exact_cells,
    medium_cap_terminal_cells: medium.cap_terminal_cells,
    medium_cap_branches: medium.cap_branches.join(' '),
  };
}).sort((a, b) => (
  b.large_cap_branch_count - a.large_cap_branch_count
  || b.large_cap_exact_cells - a.large_cap_exact_cells
  || b.medium_cap_branch_count - a.medium_cap_branch_count
  || b.medium_cap_exact_cells - a.medium_cap_exact_cells
  || b.outgoing_exact_cells - a.outgoing_exact_cells
  || a.sign.localeCompare(b.sign)
));

const signRank = new Map(signRows.map((row, idx) => [row.sign, idx + 1]));
const target = signRows.find((row) => row.sign === '060');
const targetBranches = branchRows.filter((row) => row.sign === '060');
const targetNearLargeBranches = targetBranches.filter((branch) => (
  branch.exact_cells >= LARGE_MIN_N
  && branch.terminal_share >= 0.8
  && branch.terminal_share < CAP_SHARE
));

const branchDescriptors = branchRows.map((branch) => ({
  sign: branch.sign,
  exact_cells: branch.exact_cells,
}));
const terminalFlags = [];
for (const branch of branchRows) {
  for (let i = 0; i < branch.terminal_cells; i += 1) terminalFlags.push(1);
  for (let i = branch.terminal_cells; i < branch.exact_cells; i += 1) terminalFlags.push(0);
}

let nullMaxLargeCountGeTarget = 0;
let nullMaxLargeCellsGeTarget = 0;
let nullTargetLargeCountGeTarget = 0;
let nullTargetLargeCellsGeTarget = 0;
let nullMaxLargeCountSum = 0;
let nullMaxLargeCellsSum = 0;
const rand = mulberry32(0x605920);

for (let iter = 0; iter < ITERATIONS; iter += 1) {
  const shuffled = fisherYates(terminalFlags, rand);
  let cursor = 0;
  const perSign = new Map();
  for (const branch of branchDescriptors) {
    let terminal = 0;
    for (let i = 0; i < branch.exact_cells; i += 1) {
      terminal += shuffled[cursor + i];
    }
    cursor += branch.exact_cells;
    if (branch.exact_cells >= LARGE_MIN_N && terminal / branch.exact_cells >= CAP_SHARE) {
      const prior = perSign.get(branch.sign) ?? { count: 0, cells: 0 };
      prior.count += 1;
      prior.cells += branch.exact_cells;
      perSign.set(branch.sign, prior);
    }
  }
  let maxCount = 0;
  let maxCells = 0;
  for (const score of perSign.values()) {
    if (score.count > maxCount) maxCount = score.count;
    if (score.cells > maxCells) maxCells = score.cells;
  }
  const targetScore = perSign.get('060') ?? { count: 0, cells: 0 };
  nullMaxLargeCountSum += maxCount;
  nullMaxLargeCellsSum += maxCells;
  if (maxCount >= target.large_cap_branch_count) nullMaxLargeCountGeTarget += 1;
  if (maxCells >= target.large_cap_exact_cells) nullMaxLargeCellsGeTarget += 1;
  if (targetScore.count >= target.large_cap_branch_count) nullTargetLargeCountGeTarget += 1;
  if (targetScore.cells >= target.large_cap_exact_cells) nullTargetLargeCellsGeTarget += 1;
}

const report = {
  date: RUN_DATE,
  phase: 'EXPAND',
  candidate_id: PREFIX,
  tier: 'candidate',
  bet: 'Sign 060 is a terminal-cap hinge: it licenses several high-support immediate successors that normally close the inscription. The strongest branches are not one suffix but a paradigm: 060-920, 060-692, 060-550, and 060-820. If this is right, 920 should be treated as the strongest cap member rather than as the whole phenomenon.',
  exact_collapse: {
    source: META,
    complete_rows: rows.length,
    exact_bigram_cells: cells.length,
    dedupe_key: ['sign', 'next', 'next2', 'text', 'site', 'type', 'symbol'],
  },
  thresholds: {
    cap_share_minimum: CAP_SHARE,
    large_branch_min_exact_cells: LARGE_MIN_N,
    medium_branch_min_exact_cells: MEDIUM_MIN_N,
  },
  target_060: {
    rank_by_large_cap_branch_count: signRank.get('060'),
    sign_row: target,
    near_large_cap_branches_at_0_80_to_0_85: targetNearLargeBranches,
    branches: targetBranches,
  },
  whole_corpus_comparator: {
    top_20_signs_by_large_cap_branch_count: signRows.slice(0, 20),
    note: 'The rank is over all predecessor signs with exact-collapsed immediate-successor branches, not only signs inspected in advance.',
  },
  terminal_flag_shuffle_null: {
    iterations: ITERATIONS,
    preserves: 'all exact-collapsed branch sizes and sign-to-branch membership; shuffles only the terminal/nonterminal outcome labels over branch cells',
    target_large_cap_branch_count: target.large_cap_branch_count,
    target_large_cap_exact_cells: target.large_cap_exact_cells,
    mean_null_max_large_cap_branch_count: Number((nullMaxLargeCountSum / ITERATIONS).toFixed(6)),
    mean_null_max_large_cap_exact_cells: Number((nullMaxLargeCellsSum / ITERATIONS).toFixed(6)),
    maxstat_p_ge_target_branch_count: nullMaxLargeCountGeTarget / ITERATIONS,
    maxstat_p_ge_target_exact_cells: nullMaxLargeCellsGeTarget / ITERATIONS,
    fixed_sign_p_ge_target_branch_count: nullTargetLargeCountGeTarget / ITERATIONS,
    fixed_sign_p_ge_target_exact_cells: nullTargetLargeCellsGeTarget / ITERATIONS,
  },
  live_predictions: [
    'A source-visible unseen or weakly catalogued row containing 060 followed by 920, 692, 550, or 820 should usually end immediately after that cap sign.',
    'Rows with 060 followed by 368 should not be forced into the cap class; current exact cells are nonterminal, so they are a built-in contrast branch.',
    'If branch-specific icon/site conditioning appears, it should separate cap members without destroying the shared terminal behavior.',
  ],
  demoters: [
    'Demote if source review shows 060 is a segmentation artefact or that 920/692/550/820 are not independent signs in the relevant rows.',
    'Demote if a leave-one-site or source-family collapse leaves only one cap branch above the large threshold.',
    'Demote if terminal-cap rank is common under a stricter null that preserves row length and position better than the terminal-label shuffle here.',
  ],
  decision: (
    target.large_cap_branch_count >= 3
    && target.large_cap_exact_cells >= 90
    && nullMaxLargeCountGeTarget === 0
    && nullMaxLargeCellsGeTarget === 0
  )
    ? 'candidate_survives_whole_corpus_first_pass; strict cap set is 920/550/820, with 692 demoted to near-cap until its five nonterminal rows are adjudicated'
    : 'wild_shot_until_stronger_support',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
writeCsv(
  path.join(OUT_DIR, `${PREFIX}_sign_ranking.csv`),
  signRows,
  [
    'sign',
    'outgoing_exact_cells',
    'successor_branches',
    'large_cap_branch_count',
    'large_cap_exact_cells',
    'large_cap_terminal_cells',
    'large_cap_branches',
    'medium_cap_branch_count',
    'medium_cap_exact_cells',
    'medium_cap_terminal_cells',
    'medium_cap_branches',
  ],
);
writeCsv(
  path.join(OUT_DIR, `${PREFIX}_branches.csv`),
  branchRows,
  ['sign', 'next', 'exact_cells', 'terminal_cells', 'terminal_share', 'sites', 'types', 'symbols', 'examples'],
);

console.log(JSON.stringify({
  candidate_id: PREFIX,
  decision: report.decision,
  target: report.target_060.sign_row,
  null: report.terminal_flag_shuffle_null,
  top_10: signRows.slice(0, 10),
}, null, 2));
