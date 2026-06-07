import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_terminal_governor_network_20260531';
const RUN_DATE = '2026-05-31';
const MIN_EDGE_CELLS = 20;
const MIN_TERMINAL_SHARE = 0.85;
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

function summarizeBranches(branches, terminalOverride = null) {
  const out = [];
  let cursor = 0;
  for (const branch of branches) {
    let terminal = 0;
    if (terminalOverride) {
      for (let i = 0; i < branch.cells.length; i += 1) terminal += terminalOverride[cursor + i];
      cursor += branch.cells.length;
    } else {
      terminal = branch.cells.filter((cell) => cell.next2 === '<END>').length;
    }
    out.push({
      governor: branch.governor,
      closure: branch.closure,
      edge: `${branch.governor}-${branch.closure}`,
      exact_cells: branch.cells.length,
      terminal_cells: terminal,
      terminal_share: branch.cells.length ? terminal / branch.cells.length : 0,
      sites: new Set(branch.cells.map((cell) => cell.site)).size,
      types: new Set(branch.cells.map((cell) => cell.type)).size,
      examples: branch.cells.slice(0, 5).map((cell) => `${cell.cisi}:${cell.text}`),
    });
  }
  return out;
}

function scoreNetwork(edgeRows) {
  const liveEdges = edgeRows.filter((row) => row.exact_cells >= MIN_EDGE_CELLS && row.terminal_share >= MIN_TERMINAL_SHARE);
  const byGovernor = new Map();
  const byClosure = new Map();
  for (const edge of liveEdges) {
    if (!byGovernor.has(edge.governor)) byGovernor.set(edge.governor, []);
    byGovernor.get(edge.governor).push(edge);
    if (!byClosure.has(edge.closure)) byClosure.set(edge.closure, []);
    byClosure.get(edge.closure).push(edge);
  }
  const multiGovernors = [...byGovernor.entries()]
    .filter(([, edges]) => edges.length >= 2)
    .map(([governor, edges]) => ({
      governor,
      closure_count: edges.length,
      closure_cells: edges.reduce((sum, edge) => sum + edge.exact_cells, 0),
      closures: edges.map((edge) => `${edge.closure}:${edge.exact_cells}/${edge.terminal_cells}`).join(' '),
    }))
    .sort((a, b) => b.closure_count - a.closure_count || b.closure_cells - a.closure_cells || a.governor.localeCompare(b.governor));
  const sharedClosures = [...byClosure.entries()]
    .filter(([, edges]) => edges.length >= 2)
    .map(([closure, edges]) => ({
      closure,
      governor_count: edges.length,
      governor_cells: edges.reduce((sum, edge) => sum + edge.exact_cells, 0),
      governors: edges.map((edge) => `${edge.governor}:${edge.exact_cells}/${edge.terminal_cells}`).join(' '),
    }))
    .sort((a, b) => b.governor_count - a.governor_count || b.governor_cells - a.governor_cells || a.closure.localeCompare(b.closure));
  return { liveEdges, multiGovernors, sharedClosures };
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const cellMap = new Map();
for (const row of rows) {
  const toks = tokens(row.text);
  for (let i = 0; i < toks.length - 1; i += 1) {
    const governor = toks[i];
    const closure = toks[i + 1];
    const next2 = toks[i + 2] ?? '<END>';
    const key = exactKey([governor, closure, next2, row.text, row.site, row.type, row.symbol]);
    if (!cellMap.has(key)) {
      cellMap.set(key, {
        governor,
        closure,
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
  const key = `${cell.governor}-${cell.closure}`;
  if (!byBranch.has(key)) byBranch.set(key, { governor: cell.governor, closure: cell.closure, cells: [] });
  byBranch.get(key).cells.push(cell);
}

const branchCells = [...byBranch.values()];
const edgeRows = summarizeBranches(branchCells);
const observed = scoreNetwork(edgeRows);
const targetEdges = observed.liveEdges
  .filter((edge) => ['002-817', '002-820', '060-920', '060-550', '060-820'].includes(edge.edge))
  .sort((a, b) => a.edge.localeCompare(b.edge));

const terminalFlags = [];
for (const branch of branchCells) {
  for (const cell of branch.cells) terminalFlags.push(cell.next2 === '<END>' ? 1 : 0);
}

const rand = mulberry32(0x260820);
let nullGeLiveEdges = 0;
let nullGeMultiGovernors = 0;
let nullGeSharedClosures = 0;
let nullGeTargetShape = 0;

for (let iter = 0; iter < ITERATIONS; iter += 1) {
  const shuffled = fisherYates(terminalFlags, rand);
  const sim = scoreNetwork(summarizeBranches(branchCells, shuffled));
  if (sim.liveEdges.length >= observed.liveEdges.length) nullGeLiveEdges += 1;
  if (sim.multiGovernors.length >= observed.multiGovernors.length) nullGeMultiGovernors += 1;
  if (sim.sharedClosures.length >= observed.sharedClosures.length) nullGeSharedClosures += 1;
  const has002 = sim.multiGovernors.some((row) => row.governor === '002' && row.closure_count >= 2);
  const has060 = sim.multiGovernors.some((row) => row.governor === '060' && row.closure_count >= 3);
  const has820 = sim.sharedClosures.some((row) => row.closure === '820' && row.governor_count >= 2);
  if (has002 && has060 && has820) nullGeTargetShape += 1;
}

const report = {
  date: RUN_DATE,
  phase: 'EXPAND',
  candidate_id: PREFIX,
  tier: 'candidate',
  bet: 'The strongest terminal grammar is a small governor-closure network: 002 governs closure signs 817 and 820; 060 governs closure signs 920, 550, and 820; 820 is shared by both governors. This is a structural reading of slot function, not a phonetic reading.',
  thresholds: {
    minimum_exact_cells_per_edge: MIN_EDGE_CELLS,
    minimum_terminal_share: MIN_TERMINAL_SHARE,
  },
  observed_network: {
    live_edge_count: observed.liveEdges.length,
    live_edges: observed.liveEdges.sort((a, b) => b.exact_cells - a.exact_cells || a.edge.localeCompare(b.edge)),
    multi_closure_governors: observed.multiGovernors,
    shared_closures: observed.sharedClosures,
    target_edges: targetEdges,
  },
  terminal_flag_shuffle_null: {
    iterations: ITERATIONS,
    preserves: 'exact-collapsed branch sizes and sign identities; shuffles only terminal/nonterminal outcomes',
    p_ge_live_edge_count: nullGeLiveEdges / ITERATIONS,
    p_ge_multi_governor_count: nullGeMultiGovernors / ITERATIONS,
    p_ge_shared_closure_count: nullGeSharedClosures / ITERATIONS,
    p_reproduce_target_shape_002_multi_060_multi_and_820_shared: nullGeTargetShape / ITERATIONS,
  },
  predictions: [
    'New exact 002-817, 002-820, 060-920, 060-550, and 060-820 rows should be terminal-heavy under source-normalized review.',
    '820 should remain the only high-support shared closure between two high-support governors unless more data add a third governor.',
    'If 060-692 is added as near-cap/internal boundary, it should not be merged blindly into the strict terminal network until its restart rows are source-adjudicated.'
  ],
  demoters: [
    'Demote if leave-site/source-family collapse removes either 002 or 060 from multi-closure status.',
    'Demote if exact source review shows 820 is not a stable sign across 002 and 060 contexts.',
    'Demote if a row-length/position-preserving null reproduces the target network shape at comparable rates.'
  ],
  decision: targetEdges.length === 5 && observed.sharedClosures.some((row) => row.closure === '820') && nullGeTargetShape === 0
    ? 'candidate_survives_first_terminal_governor_network_test'
    : 'wild_shot_until_network_shape_survives',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
writeCsv(path.join(OUT_DIR, `${PREFIX}_edges.csv`), edgeRows.sort((a, b) => b.exact_cells - a.exact_cells || a.edge.localeCompare(b.edge)), [
  'governor',
  'closure',
  'edge',
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
  observed_network: {
    live_edge_count: report.observed_network.live_edge_count,
    live_edges: report.observed_network.live_edges,
    multi_closure_governors: report.observed_network.multi_closure_governors,
    shared_closures: report.observed_network.shared_closures,
  },
  null: report.terminal_flag_shuffle_null,
}, null, 2));
