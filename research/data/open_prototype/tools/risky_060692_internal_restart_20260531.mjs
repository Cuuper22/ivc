import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_060692_internal_restart_20260531';
const RUN_DATE = '2026-05-31';
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

function countBy(rows, field) {
  return Object.fromEntries([...rows.reduce((acc, row) => {
    const key = row[field] || '';
    acc.set(key, (acc.get(key) ?? 0) + 1);
    return acc;
  }, new Map()).entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])));
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const occurrenceBySign = new Map();
const initialBySign = new Map();

for (const row of rows) {
  const toks = tokens(row.text);
  for (let i = 0; i < toks.length; i += 1) {
    occurrenceBySign.set(toks[i], (occurrenceBySign.get(toks[i]) ?? 0) + 1);
    if (i === 0) initialBySign.set(toks[i], (initialBySign.get(toks[i]) ?? 0) + 1);
  }
}

const openerRows = [...occurrenceBySign.entries()].map(([sign, occurrences]) => ({
  sign,
  occurrences,
  initial_occurrences: initialBySign.get(sign) ?? 0,
  initial_share: (initialBySign.get(sign) ?? 0) / occurrences,
})).sort((a, b) => b.initial_occurrences - a.initial_occurrences || b.initial_share - a.initial_share || a.sign.localeCompare(b.sign));

const openerClass = new Set(openerRows
  .filter((row) => row.occurrences >= 5 && row.initial_share >= 0.5)
  .map((row) => row.sign));

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
        branch: `${sign}-${next}`,
        sign,
        next,
        next2,
        is_terminal: next2 === '<END>',
        tail_is_opener: next2 !== '<END>' && openerClass.has(next2),
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
  if (!byBranch.has(cell.branch)) byBranch.set(cell.branch, []);
  byBranch.get(cell.branch).push(cell);
}

const branchRows = [...byBranch.entries()].map(([branch, cells]) => {
  const nonterminal = cells.filter((cell) => !cell.is_terminal);
  const openerTails = nonterminal.filter((cell) => cell.tail_is_opener);
  return {
    branch,
    exact_cells: cells.length,
    terminal_cells: cells.length - nonterminal.length,
    terminal_share: cells.length ? (cells.length - nonterminal.length) / cells.length : 0,
    nonterminal_tail_cells: nonterminal.length,
    opener_tail_cells: openerTails.length,
    opener_tail_share: nonterminal.length ? openerTails.length / nonterminal.length : null,
    nonterminal_tails: nonterminal.map((cell) => cell.next2).join(' '),
    sites: new Set(cells.map((cell) => cell.site)).size,
    types: new Set(cells.map((cell) => cell.type)).size,
    examples: cells.slice(0, 6).map((cell) => `${cell.cisi}:${cell.text}`),
  };
}).sort((a, b) => (
  b.opener_tail_cells - a.opener_tail_cells
  || b.opener_tail_share - a.opener_tail_share
  || b.exact_cells - a.exact_cells
  || a.branch.localeCompare(b.branch)
));

const competitors = branchRows.filter((row) => (
  row.exact_cells >= 20
  && row.nonterminal_tail_cells >= 3
  && row.nonterminal_tail_cells <= 10
  && row.terminal_share >= 0.5
  && row.terminal_share < 1
));

const target = branchRows.find((row) => row.branch === '060-692');
const competitorRank = competitors.findIndex((row) => row.branch === '060-692') + 1;
const nonterminalTailPool = [...cellMap.values()].filter((cell) => !cell.is_terminal).map((cell) => cell.next2);
const openerPoolFlags = nonterminalTailPool.map((sign) => openerClass.has(sign) ? 1 : 0);
let fixedGeTarget = 0;
let maxstatGeTarget = 0;
const rand = mulberry32(0x060692);

for (let iter = 0; iter < ITERATIONS; iter += 1) {
  let fixedHits = 0;
  for (let j = 0; j < target.nonterminal_tail_cells; j += 1) {
    fixedHits += openerPoolFlags[Math.floor(rand() * openerPoolFlags.length)];
  }
  if (fixedHits >= target.opener_tail_cells) fixedGeTarget += 1;

  let maxHits = 0;
  for (const competitor of competitors) {
    let hits = 0;
    for (let j = 0; j < competitor.nonterminal_tail_cells; j += 1) {
      hits += openerPoolFlags[Math.floor(rand() * openerPoolFlags.length)];
    }
    if (hits > maxHits) maxHits = hits;
  }
  if (maxHits >= target.opener_tail_cells) maxstatGeTarget += 1;
}

const targetCells = [...cellMap.values()].filter((cell) => cell.branch === '060-692');
const targetNonterminal = targetCells.filter((cell) => !cell.is_terminal);

const report = {
  date: RUN_DATE,
  phase: 'EXPAND',
  candidate_id: PREFIX,
  tier: 'candidate',
  bet: 'The five nonterminal 060-692 rows are not random failures of a terminal cap. They behave like internal-boundary restarts: every sign after 060-692 in those exceptions belongs to an objective high-initial opener class, mainly 520 and 740. This promotes 692 from a failed terminal cap to a near-cap that can close a local unit inside longer inscriptions.',
  opener_class_definition: {
    occurrence_minimum: 5,
    initial_share_minimum: 0.5,
    opener_class_size: openerClass.size,
    relevant_tail_signs: ['520', '401', '740'].map((sign) => openerRows.find((row) => row.sign === sign)),
  },
  target_060_692: {
    comparator_rank_among_branches_with_20plus_cells_3to10_nonterminal_tails_and_halfplus_terminal_share: competitorRank,
    summary: target,
    terminal_rows: targetCells.filter((cell) => cell.is_terminal).length,
    nonterminal_rows: targetNonterminal.map((cell) => ({
      cisi: cell.cisi,
      text: cell.text,
      site: cell.site,
      type: cell.type,
      symbol: cell.symbol,
      tail_after_692: cell.next2,
      tail_initial_profile: openerRows.find((row) => row.sign === cell.next2),
    })),
  },
  comparator: {
    competitor_count: competitors.length,
    top_20_competitor_rows: competitors.slice(0, 20),
  },
  tail_opener_null: {
    iterations: ITERATIONS,
    tail_pool: 'all observed nonterminal next2 signs after exact-collapsed bigrams',
    fixed_branch_p_ge_5_of_5_opener_tails: fixedGeTarget / ITERATIONS,
    maxstat_p_any_competitor_ge_5_opener_tails: maxstatGeTarget / ITERATIONS,
  },
  predictions: [
    'Source images of the five nonterminal 060-692 rows should look compatible with a phrase or line restart after 692, especially before 520 or 740.',
    'New or weakly sourced 060-692-X rows should preferentially have X in the high-initial opener class; random continuation tails would kill the internal-boundary reading.',
    '060-692 should pattern visually with the strict caps 920/550/820 on the pre-692 side, not with the continuation branches 060-297 or 060-368.',
  ],
  demoters: [
    'If source review shows the five nonterminal tails are cataloguing/line-division artefacts, demote.',
    'If a stricter null preserving sign position and row length makes 5/5 opener tails common, demote.',
    'If 520 and 740 are not valid opener signs after source-normalized initial-position collapse, demote.',
  ],
  decision: target.opener_tail_cells === target.nonterminal_tail_cells && target.nonterminal_tail_cells === 5
    ? 'candidate_survives_first_internal_restart_test'
    : 'wild_shot_until_restart_tail_pattern_tightens',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
writeCsv(path.join(OUT_DIR, `${PREFIX}_branch_comparator.csv`), branchRows, [
  'branch',
  'exact_cells',
  'terminal_cells',
  'terminal_share',
  'nonterminal_tail_cells',
  'opener_tail_cells',
  'opener_tail_share',
  'nonterminal_tails',
  'sites',
  'types',
  'examples',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_opener_class.csv`), openerRows, [
  'sign',
  'occurrences',
  'initial_occurrences',
  'initial_share',
]);

console.log(JSON.stringify({
  candidate_id: PREFIX,
  decision: report.decision,
  target: report.target_060_692.summary,
  nonterminal_rows: report.target_060_692.nonterminal_rows,
  null: report.tail_opener_null,
  top_competitors: competitors.slice(0, 10),
}, null, 2));
