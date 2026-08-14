// A forger attack on the terminal-governor network: could its shape arise
// from sign frequencies and row lengths alone, with no real ordering rule?
// We read the filtered corpus metadata (complete texts only, rows with at
// least 2 signs), score the raw network — edges with at least 20 cells and
// 85% terminal share, multi-closure governors, shared closures — then run
// 2000 iterations where each row's signs are shuffled internally. That
// shuffle keeps every inscription's exact sign multiset and length but
// destroys order. If the shuffled corpora rarely reproduce the live-edge
// counts or the target shape (002 with 2+ closures, 060 with 3+, 820 shared
// by both), the network depends on genuine sign order. Note this variant
// counts raw occurrence cells, without the exact-collapse used elsewhere.
// Writes one JSON report.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_terminal_governor_network_row_shuffle_forger_20260531';
const RUN_DATE = '2026-05-31';
const MIN_EDGE_CELLS = 20;
const MIN_TERMINAL_SHARE = 0.85;
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

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function mulberry32(seed) {
  return function rand() {
    let t = seed += 0x6D2B79F5;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffle(values, rand) {
  const out = values.slice();
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function scoreRows(rowTokenLists) {
  const branches = new Map();
  for (const toks of rowTokenLists) {
    for (let i = 0; i < toks.length - 1; i += 1) {
      const edge = `${toks[i]}-${toks[i + 1]}`;
      const item = branches.get(edge) ?? {
        governor: toks[i],
        closure: toks[i + 1],
        edge,
        cells: 0,
        terminal: 0,
      };
      item.cells += 1;
      if (i + 2 >= toks.length) item.terminal += 1;
      branches.set(edge, item);
    }
  }
  const edges = [...branches.values()].map((edge) => ({
    ...edge,
    terminal_share: edge.cells ? edge.terminal / edge.cells : 0,
  }));
  const liveEdges = edges.filter((edge) => edge.cells >= MIN_EDGE_CELLS && edge.terminal_share >= MIN_TERMINAL_SHARE);
  const byGovernor = new Map();
  const byClosure = new Map();
  for (const edge of liveEdges) {
    if (!byGovernor.has(edge.governor)) byGovernor.set(edge.governor, []);
    byGovernor.get(edge.governor).push(edge);
    if (!byClosure.has(edge.closure)) byClosure.set(edge.closure, []);
    byClosure.get(edge.closure).push(edge);
  }
  const multiGovernors = [...byGovernor.entries()].filter(([, items]) => items.length >= 2);
  const sharedClosures = [...byClosure.entries()].filter(([, items]) => items.length >= 2);
  return { edges, liveEdges, multiGovernors, sharedClosures };
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const rowTokenLists = rows.map((row) => tokens(row.text)).filter((toks) => toks.length >= 2);
const observed = scoreRows(rowTokenLists);
const targetEdges = new Set(['002-817', '002-820', '060-920', '060-550', '060-820']);
const observedTargetEdges = observed.liveEdges.filter((edge) => targetEdges.has(edge.edge));
const rand = mulberry32(0x20260531);

let nullGeLiveEdges = 0;
let nullGeTargetEdges = 0;
let nullGeTargetShape = 0;
let nullGeMultiGovernors = 0;
let nullGeSharedClosures = 0;

for (let iter = 0; iter < ITERATIONS; iter += 1) {
  const sim = scoreRows(rowTokenLists.map((toks) => shuffle(toks, rand)));
  if (sim.liveEdges.length >= observed.liveEdges.length) nullGeLiveEdges += 1;
  if (sim.liveEdges.filter((edge) => targetEdges.has(edge.edge)).length >= observedTargetEdges.length) nullGeTargetEdges += 1;
  if (sim.multiGovernors.length >= observed.multiGovernors.length) nullGeMultiGovernors += 1;
  if (sim.sharedClosures.length >= observed.sharedClosures.length) nullGeSharedClosures += 1;
  const has002 = sim.multiGovernors.some(([governor, items]) => governor === '002' && items.length >= 2);
  const has060 = sim.multiGovernors.some(([governor, items]) => governor === '060' && items.length >= 3);
  const has820 = sim.sharedClosures.some(([closure, items]) => closure === '820' && items.length >= 2);
  if (has002 && has060 && has820) nullGeTargetShape += 1;
}

const report = {
  date: RUN_DATE,
  phase: 'EXPAND',
  candidate_id: PREFIX,
  tier: 'candidate',
  bet: 'The terminal-governor network depends on real order, not just row lengths and sign frequencies. If row-internal order is destroyed while preserving each inscription sign multiset, the 002/060/820 network should disappear.',
  observed_raw_network: {
    live_edge_count: observed.liveEdges.length,
    target_edge_count: observedTargetEdges.length,
    target_edges: observedTargetEdges.sort((a, b) => b.cells - a.cells || a.edge.localeCompare(b.edge)),
    live_edges: observed.liveEdges.sort((a, b) => b.cells - a.cells || a.edge.localeCompare(b.edge)).slice(0, 20),
    multi_governor_count: observed.multiGovernors.length,
    shared_closure_count: observed.sharedClosures.length,
  },
  row_internal_shuffle_forger: {
    iterations: ITERATIONS,
    preserves: 'each complete row length and exact sign multiset; destroys row-internal order',
    p_ge_live_edge_count: nullGeLiveEdges / ITERATIONS,
    p_ge_target_edge_count: nullGeTargetEdges / ITERATIONS,
    p_ge_multi_governor_count: nullGeMultiGovernors / ITERATIONS,
    p_ge_shared_closure_count: nullGeSharedClosures / ITERATIONS,
    p_reproduce_target_shape_002_multi_060_multi_and_820_shared: nullGeTargetShape / ITERATIONS,
  },
  decision: observedTargetEdges.length === 5 && nullGeTargetShape === 0
    ? 'candidate_survives_row_internal_order_forger'
    : 'wild_shot_until_order_forger_is_tighter',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');

console.log(JSON.stringify({
  candidate_id: PREFIX,
  decision: report.decision,
  observed: report.observed_raw_network,
  forger: report.row_internal_shuffle_forger,
}, null, 2));
