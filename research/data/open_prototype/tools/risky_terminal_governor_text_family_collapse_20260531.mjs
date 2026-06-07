import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_terminal_governor_text_family_collapse_20260531';
const ITERATIONS = 5000;
const STRICT_MIN = 20;
const STRICT_SHARE = 0.85;
const TARGET_SIGNS = new Set(['002', '060']);
const TARGET_EDGES = new Set(['002-817', '002-820', '002-861', '060-920', '060-550', '060-820', '060-692']);

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

function summarize(edge, items) {
  const terminal = items.filter((item) => item.terminal).length;
  return {
    edge,
    text_families: items.length,
    terminal_families: terminal,
    terminal_share: items.length ? terminal / items.length : 0,
    sites: new Set(items.flatMap((item) => [...item.sites])).size,
    types: new Set(items.flatMap((item) => [...item.types])).size,
    examples: items.slice(0, 8).map((item) => item.text),
  };
}

function shapeScore(edgeRows) {
  const strict = edgeRows.filter((row) => row.text_families >= STRICT_MIN && row.terminal_share >= STRICT_SHARE);
  const byGov = new Map();
  for (const row of strict) {
    const [gov, closure] = row.edge.split('-');
    if (!byGov.has(gov)) byGov.set(gov, []);
    byGov.get(gov).push(closure);
  }
  const incoming = new Map();
  for (const row of strict) {
    const [gov, closure] = row.edge.split('-');
    if (!incoming.has(closure)) incoming.set(closure, []);
    incoming.get(closure).push(gov);
  }
  const multiGovernors = [...byGov.entries()].filter(([gov, closures]) => TARGET_SIGNS.has(gov) && closures.length >= 2);
  const sharedClosures = [...incoming.entries()].filter(([, govs]) => govs.includes('002') && govs.includes('060'));
  return {
    strict,
    multi_governor_count: multiGovernors.length,
    shared_closure_count: sharedClosures.length,
    has_target_shape: (byGov.get('002') ?? []).includes('817')
      && (byGov.get('002') ?? []).includes('820')
      && (byGov.get('060') ?? []).includes('920')
      && (byGov.get('060') ?? []).includes('550')
      && (byGov.get('060') ?? []).includes('820')
      && sharedClosures.some(([closure]) => closure === '820'),
  };
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const familyMap = new Map();

for (const row of rows) {
  const toks = tokens(row.text);
  for (let i = 0; i < toks.length - 1; i += 1) {
    const edge = `${toks[i]}-${toks[i + 1]}`;
    const next2 = toks[i + 2] ?? '<END>';
    const key = `${edge}|${next2}|${row.text}`;
    if (!familyMap.has(key)) {
      familyMap.set(key, {
        edge,
        terminal: next2 === '<END>',
        text: row.text,
        sites: new Set(),
        types: new Set(),
      });
    }
    const item = familyMap.get(key);
    item.sites.add(row.site);
    item.types.add(row.type);
  }
}

const byEdge = new Map();
for (const item of familyMap.values()) {
  if (!byEdge.has(item.edge)) byEdge.set(item.edge, []);
  byEdge.get(item.edge).push(item);
}

const edgeRows = [...byEdge.entries()].map(([edge, items]) => summarize(edge, items))
  .sort((a, b) => b.text_families - a.text_families || b.terminal_share - a.terminal_share || a.edge.localeCompare(b.edge));

const liveShape = shapeScore(edgeRows);
const branchDescriptors = edgeRows.map((row) => ({
  edge: row.edge,
  text_families: row.text_families,
}));
const terminalFlags = [];
for (const row of edgeRows) {
  for (let i = 0; i < row.terminal_families; i += 1) terminalFlags.push(1);
  for (let i = row.terminal_families; i < row.text_families; i += 1) terminalFlags.push(0);
}

const rand = mulberry32(0x7E27F17);
let geStrict = 0;
let geMulti = 0;
let geShared = 0;
let targetShape = 0;
for (let iter = 0; iter < ITERATIONS; iter += 1) {
  const shuffled = fisherYates(terminalFlags, rand);
  let cursor = 0;
  const simRows = [];
  for (const branch of branchDescriptors) {
    let term = 0;
    for (let i = 0; i < branch.text_families; i += 1) term += shuffled[cursor + i];
    cursor += branch.text_families;
    simRows.push({
      edge: branch.edge,
      text_families: branch.text_families,
      terminal_families: term,
      terminal_share: branch.text_families ? term / branch.text_families : 0,
    });
  }
  const simShape = shapeScore(simRows);
  if (simShape.strict.length >= liveShape.strict.length) geStrict += 1;
  if (simShape.multi_governor_count >= liveShape.multi_governor_count) geMulti += 1;
  if (simShape.shared_closure_count >= liveShape.shared_closure_count) geShared += 1;
  if (simShape.has_target_shape) targetShape += 1;
}

const report = {
  date: '2026-05-31',
  phase: 'CONSOLIDATE',
  candidate_id: PREFIX,
  tier: liveShape.has_target_shape ? 'promoted_candidate_strengthener' : 'demoter',
  bet: 'The terminal-governor graph survives a harsher text-family collapse where each exact inscription text contributes at most once to an edge, regardless of object count, site, type, or symbol.',
  source: META,
  collapse_key: ['edge', 'next2', 'text'],
  strict_rule: {
    min_text_families: STRICT_MIN,
    min_terminal_share: STRICT_SHARE,
  },
  target_edges: edgeRows.filter((row) => TARGET_EDGES.has(row.edge)),
  live_shape: {
    strict_edges: liveShape.strict.map((row) => `${row.edge}:${row.text_families}/${row.terminal_families}`),
    strict_edge_count: liveShape.strict.length,
    multi_governor_count: liveShape.multi_governor_count,
    shared_closure_count: liveShape.shared_closure_count,
    has_target_shape: liveShape.has_target_shape,
  },
  text_family_terminal_shuffle_null: {
    iterations: ITERATIONS,
    preserves: 'text-family branch sizes and sign identities; shuffles only terminal/nonterminal outcomes',
    p_ge_strict_edge_count: geStrict / ITERATIONS,
    p_ge_multi_governor_count: geMulti / ITERATIONS,
    p_ge_shared_closure_count: geShared / ITERATIONS,
    p_reproduce_target_shape: targetShape / ITERATIONS,
  },
  decision: liveShape.has_target_shape
    ? 'candidate_survives_text_family_collapse'
    : 'candidate_demoted_by_text_family_collapse',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
writeCsv(path.join(OUT_DIR, `${PREFIX}_edges.csv`), edgeRows, [
  'edge',
  'text_families',
  'terminal_families',
  'terminal_share',
  'sites',
  'types',
  'examples',
]);

console.log(JSON.stringify({
  candidate_id: PREFIX,
  decision: report.decision,
  target_edges: report.target_edges,
  live_shape: report.live_shape,
  null: report.text_family_terminal_shuffle_null,
}, null, 2));
