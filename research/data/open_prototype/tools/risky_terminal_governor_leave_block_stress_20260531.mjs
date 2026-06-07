import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_terminal_governor_leave_block_stress_20260531';
const TARGET_EDGES = ['002-817', '002-820', '002-861', '060-920', '060-550', '060-820', '060-692'];
const BLOCKS = [
  { name: 'NONE', predicate: () => false },
  { name: 'Mohenjo-daro|SEAL:S', predicate: (row) => row.site === 'Mohenjo-daro' && row.type === 'SEAL:S' },
  { name: 'Harappa|SEAL:S', predicate: (row) => row.site === 'Harappa' && row.type === 'SEAL:S' },
  { name: 'all|SEAL:S', predicate: (row) => row.type === 'SEAL:S' },
  { name: 'Mohenjo-daro|SEAL:R', predicate: (row) => row.site === 'Mohenjo-daro' && row.type === 'SEAL:R' },
  { name: 'Harappa|TAB', predicate: (row) => row.site === 'Harappa' && row.type.startsWith('TAB') },
  { name: 'weak_object_identity', predicate: (row) => !row.cisi || row.cisi === '-' || !row.site || row.site === '-' || row.site === 'NA' },
];

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

function score(rows) {
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
  return TARGET_EDGES.map((edge) => {
    const items = byEdge.get(edge) ?? [];
    const terminal = items.filter((item) => item.terminal).length;
    return {
      edge,
      text_families: items.length,
      terminal_families: terminal,
      terminal_share: items.length ? terminal / items.length : 0,
      sites: new Set(items.flatMap((item) => [...item.sites])).size,
      types: new Set(items.flatMap((item) => [...item.types])).size,
    };
  });
}

const allRows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const panels = BLOCKS.map((block) => {
  const kept = allRows.filter((row) => !block.predicate(row));
  const removed = allRows.length - kept.length;
  const rows = score(kept);
  return {
    leave_block: block.name,
    removed_rows: removed,
    target_edges: rows,
    strict_survivors_min20_share085: rows.filter((row) => row.text_families >= 20 && row.terminal_share >= 0.85).map((row) => row.edge),
    near_survivors_min20_share075: rows.filter((row) => row.text_families >= 20 && row.terminal_share >= 0.75 && row.terminal_share < 0.85).map((row) => row.edge),
  };
});

const report = {
  date: '2026-05-31',
  phase: 'CONSOLIDATE',
  candidate_id: PREFIX,
  tier: 'candidate_stress_table',
  bet: 'The terminal-governor model should not collapse when the skeptic removes Mohenjo-daro SEAL:S or other high-risk site/type blocks.',
  source: META,
  collapse_key: ['edge', 'next2', 'text'],
  panels,
  decision: (() => {
    const mdSeal = panels.find((row) => row.leave_block === 'Mohenjo-daro|SEAL:S');
    const strict = new Set(mdSeal.strict_survivors_min20_share085);
    const coreSurvives = strict.has('002-817') && strict.has('002-820') && strict.has('060-920');
    return coreSurvives
      ? 'core_survives_mohenjo_daro_seal_s_removal_full_shape_support_limited'
      : 'core_demoted_by_mohenjo_daro_seal_s_block_removal';
  })(),
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({
  candidate_id: PREFIX,
  decision: report.decision,
  panels: panels.map((panel) => ({
    leave_block: panel.leave_block,
    removed_rows: panel.removed_rows,
    strict: panel.strict_survivors_min20_share085,
    near: panel.near_survivors_min20_share075,
    edges: panel.target_edges,
  })),
}, null, 2));
