// Checks whether the terminal-governor edges survive object-level dedupe.
// The worry: identical texts stamped on many objects (or one object listed
// many times) could inflate an edge's counts. Here each CISI object may
// contribute at most one count per bigram edge; if the same object shows an
// edge both terminally and internally, the terminal witness wins. We read
// the filtered corpus metadata (complete texts only), rebuild the per-edge
// counts on that basis, and ask whether the seven target edges (002-817,
// 002-820, 002-861, 060-920, 060-550, 060-820, 060-692) still clear 20
// object cells with 85% terminal share (strict) or 75-85% (near). Five or
// more strict survivors keeps the network candidate-tier. Writes a JSON
// report and an edges CSV.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_terminal_governor_object_dedupe_20260531';
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
  const text = String(value ?? '');
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const body = rows.map((row) => fields.map((field) => esc(row[field])).join(',')).join('\n');
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`, 'utf8');
}

function summarize(edge, items) {
  const terminalObjects = items.filter((item) => item.terminal).length;
  return {
    edge,
    object_cells: items.length,
    terminal_objects: terminalObjects,
    terminal_share: items.length ? terminalObjects / items.length : 0,
    sites: new Set(items.map((item) => item.site)).size,
    types: new Set(items.map((item) => item.type)).size,
    examples: items.slice(0, 8).map((item) => `${item.cisi}:${item.text}`).join(' | '),
  };
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const objectEdge = new Map();

for (const row of rows) {
  const toks = tokens(row.text);
  for (let i = 0; i < toks.length - 1; i += 1) {
    const edge = `${toks[i]}-${toks[i + 1]}`;
    const next2 = toks[i + 2] ?? '<END>';
    const key = `${row.cisi}|${edge}`;
    const prior = objectEdge.get(key);
    const item = {
      edge,
      cisi: row.cisi,
      terminal: next2 === '<END>',
      site: row.site,
      type: row.type,
      symbol: row.symbol,
      text: row.text,
    };
    if (!prior || (item.terminal && !prior.terminal)) objectEdge.set(key, item);
  }
}

const byEdge = new Map();
for (const item of objectEdge.values()) {
  if (!byEdge.has(item.edge)) byEdge.set(item.edge, []);
  byEdge.get(item.edge).push(item);
}

const edgeRows = [...byEdge.entries()].map(([edge, items]) => summarize(edge, items))
  .sort((a, b) => b.object_cells - a.object_cells || b.terminal_share - a.terminal_share || a.edge.localeCompare(b.edge));

const targetRows = edgeRows.filter((row) => TARGET_EDGES.has(row.edge));
const strictSurvivors = targetRows.filter((row) => row.object_cells >= 20 && row.terminal_share >= 0.85);
const nearSurvivors = targetRows.filter((row) => row.object_cells >= 20 && row.terminal_share >= 0.75 && row.terminal_share < 0.85);

const report = {
  date: '2026-05-31',
  phase: 'EXPAND',
  candidate_id: PREFIX,
  tier: strictSurvivors.length >= 5 ? 'candidate_strengthener' : 'demoter',
  bet: 'The terminal-governor graph is not only a repeated-text artifact: it survives when each CISI/object contributes at most one count per edge.',
  source: META,
  object_dedupe_key: ['cisi', 'edge'],
  target_edges: targetRows,
  strict_survivors_min20_share085: strictSurvivors,
  near_survivors_min20_share075: nearSurvivors,
  strongest_global_edges_min20: edgeRows.filter((row) => row.object_cells >= 20).slice(0, 40),
  decision: strictSurvivors.length >= 5
    ? 'candidate_survives_object_level_edge_dedupe'
    : 'candidate_demoted_by_object_level_edge_dedupe',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
writeCsv(path.join(OUT_DIR, `${PREFIX}_edges.csv`), edgeRows, [
  'edge',
  'object_cells',
  'terminal_objects',
  'terminal_share',
  'sites',
  'types',
  'examples',
]);

console.log(JSON.stringify({
  candidate_id: PREFIX,
  decision: report.decision,
  target_edges: targetRows,
  strict_survivors: strictSurvivors.map((row) => row.edge),
  near_survivors: nearSurvivors.map((row) => row.edge),
}, null, 2));
