import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_820_portable_closure_sign_20260531';
const RUN_DATE = '2026-05-31';
const MIN_BRANCH_CELLS = 20;
const MIN_TERMINAL_SHARE = 0.9;
const ITERATIONS = 5000;

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

function summarizeBranches(branchCells, terminalOverride = null) {
  const branchRows = [];
  let cursor = 0;
  for (const branch of branchCells) {
    let terminal = 0;
    if (terminalOverride) {
      for (let i = 0; i < branch.cells.length; i += 1) terminal += terminalOverride[cursor + i];
      cursor += branch.cells.length;
    } else {
      terminal = branch.cells.filter((cell) => cell.next2 === '<END>').length;
    }
    branchRows.push({
      target: branch.target,
      prev: branch.prev,
      exact_cells: branch.cells.length,
      terminal_cells: terminal,
      terminal_share: branch.cells.length ? terminal / branch.cells.length : 0,
      sites: new Set(branch.cells.map((cell) => cell.site)).size,
      types: new Set(branch.cells.map((cell) => cell.type)).size,
      examples: branch.cells.slice(0, 5).map((cell) => `${cell.cisi}:${cell.prev}-${cell.target}-${cell.next2}:${cell.text}`),
    });
  }
  return branchRows;
}

function scoreTargets(branchRows) {
  const byTarget = new Map();
  for (const branch of branchRows) {
    if (!byTarget.has(branch.target)) byTarget.set(branch.target, []);
    byTarget.get(branch.target).push(branch);
  }
  return [...byTarget.entries()].map(([target, branches]) => {
    const qualified = branches.filter((branch) => branch.exact_cells >= MIN_BRANCH_CELLS && branch.terminal_share >= MIN_TERMINAL_SHARE);
    return {
      target,
      qualified_governor_count: qualified.length,
      qualified_governor_cells: qualified.reduce((sum, branch) => sum + branch.exact_cells, 0),
      qualified_terminal_cells: qualified.reduce((sum, branch) => sum + branch.terminal_cells, 0),
      qualified_governors: qualified.map((branch) => `${branch.prev}:${branch.exact_cells}/${branch.terminal_cells}`).join(' '),
      total_incoming_exact_cells: branches.reduce((sum, branch) => sum + branch.exact_cells, 0),
      incoming_branches: branches.length,
    };
  }).sort((a, b) => (
    b.qualified_governor_count - a.qualified_governor_count
    || b.qualified_governor_cells - a.qualified_governor_cells
    || b.total_incoming_exact_cells - a.total_incoming_exact_cells
    || a.target.localeCompare(b.target)
  ));
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const cellMap = new Map();
for (const row of rows) {
  const toks = tokens(row.text);
  for (let i = 0; i < toks.length - 1; i += 1) {
    const prev = toks[i];
    const target = toks[i + 1];
    const next2 = toks[i + 2] ?? '<END>';
    const key = exactKey([prev, target, next2, row.text, row.site, row.type, row.symbol]);
    if (!cellMap.has(key)) {
      cellMap.set(key, {
        prev,
        target,
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

const byBranch = new Map();
for (const cell of cellMap.values()) {
  const key = `${cell.prev}-${cell.target}`;
  if (!byBranch.has(key)) byBranch.set(key, { prev: cell.prev, target: cell.target, cells: [] });
  byBranch.get(key).cells.push(cell);
}
const branchCells = [...byBranch.values()];
const branchRows = summarizeBranches(branchCells);
const targetRows = scoreTargets(branchRows);
const target820 = targetRows.find((row) => row.target === '820');
const target820Incoming = branchRows.filter((row) => row.target === '820')
  .sort((a, b) => b.exact_cells - a.exact_cells || a.prev.localeCompare(b.prev));

const terminalFlags = [];
for (const branch of branchCells) {
  for (const cell of branch.cells) terminalFlags.push(cell.next2 === '<END>' ? 1 : 0);
}

const rand = mulberry32(0x820820);
let maxstatGe820GovernorCount = 0;
let maxstatGe820Cells = 0;
let fixed820GeGovernorCount = 0;
let fixed820GeCells = 0;

for (let iter = 0; iter < ITERATIONS; iter += 1) {
  const shuffled = fisherYates(terminalFlags, rand);
  const simulatedTargets = scoreTargets(summarizeBranches(branchCells, shuffled));
  const sim820 = simulatedTargets.find((row) => row.target === '820');
  const maxGovernorCount = Math.max(...simulatedTargets.map((row) => row.qualified_governor_count));
  const maxCells = Math.max(...simulatedTargets.map((row) => row.qualified_governor_cells));
  if (maxGovernorCount >= target820.qualified_governor_count) maxstatGe820GovernorCount += 1;
  if (maxCells >= target820.qualified_governor_cells) maxstatGe820Cells += 1;
  if (sim820.qualified_governor_count >= target820.qualified_governor_count) fixed820GeGovernorCount += 1;
  if (sim820.qualified_governor_cells >= target820.qualified_governor_cells) fixed820GeCells += 1;
}

const report = {
  date: RUN_DATE,
  phase: 'EXPAND',
  candidate_id: PREFIX,
  tier: 'candidate',
  bet: 'Sign 820 is a portable closure sign shared by at least two governors: 002 and 060. It is not simply the terminal partner of one local formula. In exact-collapsed bigram cells, 002-820 and 060-820 both exceed 20 cells and 0.90 terminal share.',
  thresholds: {
    minimum_exact_cells_per_governor_branch: MIN_BRANCH_CELLS,
    minimum_terminal_share_per_governor_branch: MIN_TERMINAL_SHARE,
  },
  target_820: {
    target_rank: targetRows.findIndex((row) => row.target === '820') + 1,
    score: target820,
    incoming_branches: target820Incoming,
  },
  whole_corpus_comparator: {
    top_20_targets_by_qualified_multigovernor_closure: targetRows.slice(0, 20),
  },
  terminal_flag_shuffle_null: {
    iterations: ITERATIONS,
    preserves: 'exact-collapsed predecessor-target branch sizes; shuffles only terminal/nonterminal outcomes',
    fixed_820_p_ge_governor_count: fixed820GeGovernorCount / ITERATIONS,
    fixed_820_p_ge_qualified_cells: fixed820GeCells / ITERATIONS,
    maxstat_p_any_target_ge_820_governor_count: maxstatGe820GovernorCount / ITERATIONS,
    maxstat_p_any_target_ge_820_qualified_cells: maxstatGe820Cells / ITERATIONS,
  },
  predictions: [
    'Future exact-collapsed 060-820 and 002-820 rows should remain overwhelmingly terminal even under source normalization.',
    'If a third high-support governor of 820 appears, it should also be terminal-heavy rather than a random continuation context.',
    'The visual/source review of 820 should not require it to be a private allograph tied only to 002 or only to 060.',
  ],
  demoters: [
    'Demote if source review merges 060-820 with a different sign class or shows 002-820 is a copying cluster only.',
    'Demote if leave-one-site collapse removes either 002 or 060 as a qualified governor.',
    'Demote if stricter position-preserving nulls make two qualified governors common.',
  ],
  decision: target820.qualified_governor_count >= 2 && target820.qualified_governor_cells >= 90
    ? 'candidate_survives_multigovernor_closure_test'
    : 'wild_shot_until_multigovernor_support_improves',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
writeCsv(path.join(OUT_DIR, `${PREFIX}_target_ranking.csv`), targetRows, [
  'target',
  'qualified_governor_count',
  'qualified_governor_cells',
  'qualified_terminal_cells',
  'qualified_governors',
  'total_incoming_exact_cells',
  'incoming_branches',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_incoming_branches.csv`), branchRows, [
  'target',
  'prev',
  'exact_cells',
  'terminal_cells',
  'terminal_share',
  'sites',
  'types',
  'examples',
]);

console.log(JSON.stringify({
  candidate_id: PREFIX,
  decision: report.decision,
  target_820: report.target_820.score,
  null: report.terminal_flag_shuffle_null,
  top_10: targetRows.slice(0, 10),
}, null, 2));
