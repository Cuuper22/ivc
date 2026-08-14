// Does the sign after an `002-H` pair decide whether the inscription stops there?
// This script reads the filtered corpus (data/open_prototype/lipi/metadata_filtered.csv),
// finds every frame of the form `002-H-X` (sign 002, then a "head" H, then a "branch" X),
// and asks, for each head: does knowing the branch X predict whether the text is
// terminal (ends right after X) or continues? The "determinism score" counts how many
// frames the best branch->terminal rule explains; a permutation test (exact when the
// label combinations fit under 200k, otherwise 50,000 Monte Carlo shuffles) gives a
// p-value. The point of the experiment is to check whether head 390 is special: if
// `002-390-X` picks terminality far better than chance, and few rival heads match it,
// then `002-390-X` behaves like a real grammatical slot, not just a frequent trigram.
// Outputs go to data/open_prototype/reports/: a bet summary (JSON + CSV), a per-head
// scan CSV, and the raw frames CSV.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_002_head_branch_determinism_scan_20260531';
const RUN_DATE = '2026-05-31';
const ITERATIONS = 50000;

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
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`);
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function norm(value, fallback = 'NA') {
  const text = String(value ?? '').trim();
  return text && text !== '-' && text !== 'None' ? text : fallback;
}

function mulberry32(seed) {
  return function rand() {
    let t = (seed += 0x6D2B79F5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffle(rand, arr) {
  const out = [...arr];
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function combinations(items, k, limit = 200000) {
  const out = [];
  const combo = [];
  function rec(start) {
    if (out.length > limit) return;
    if (combo.length === k) {
      out.push([...combo]);
      return;
    }
    for (let i = start; i <= items.length - (k - combo.length); i += 1) {
      combo.push(items[i]);
      rec(i + 1);
      combo.pop();
    }
  }
  rec(0);
  return out;
}

function determinismScore(frames, continuingSet) {
  const byBranch = new Map();
  frames.forEach((frame, idx) => {
    if (!byBranch.has(frame.branch)) byBranch.set(frame.branch, []);
    byBranch.get(frame.branch).push(continuingSet.has(idx));
  });
  let score = 0;
  let pureBranches = 0;
  for (const labels of byBranch.values()) {
    const cont = labels.filter(Boolean).length;
    if (cont === 0 || cont === labels.length) pureBranches += 1;
    score += Math.max(cont, labels.length - cont);
  }
  return { score, pureBranches };
}

function determinismP(frames) {
  const observedContinuing = new Set(frames.map((frame, idx) => (!frame.terminal ? idx : -1)).filter((idx) => idx >= 0));
  const observed = determinismScore(frames, observedContinuing);
  const n = frames.length;
  const k = observedContinuing.size;
  const indexes = frames.map((_, idx) => idx);
  const combos = combinations(indexes, k);
  if (combos.length <= 200000) {
    let ge = 0;
    for (const combo of combos) {
      const score = determinismScore(frames, new Set(combo));
      if (score.score >= observed.score) ge += 1;
    }
    return { ...observed, p: ge / combos.length, method: `exact_${combos.length}_label_permutations` };
  }
  const labels = frames.map((frame) => !frame.terminal);
  const rand = mulberry32(0x2002 + n + k);
  let ge = 0;
  for (let iter = 0; iter < ITERATIONS; iter += 1) {
    const shuffled = shuffle(rand, labels);
    const continuing = new Set(shuffled.map((value, idx) => (value ? idx : -1)).filter((idx) => idx >= 0));
    const score = determinismScore(frames, continuing);
    if (score.score >= observed.score) ge += 1;
  }
  return { ...observed, p: ge / ITERATIONS, method: `monte_carlo_${ITERATIONS}_label_permutations` };
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const frames = [];

for (const row of rows) {
  for (let i = 0; i < row.signs.length - 2; i += 1) {
    if (row.signs[i] !== '002') continue;
    const head = row.signs[i + 1];
    const branch = row.signs[i + 2];
    const tail = row.signs.slice(i + 3);
    frames.push({
      id: row.id,
      object: objectId(row),
      site: norm(row.site),
      type: norm(row.type),
      symbol: norm(row.symbol),
      cult: norm(row.cult),
      shape: norm(row.shape),
      material: norm(row.material),
      prev: row.signs[i - 1] ?? '<START>',
      head,
      branch,
      terminal: i + 2 === row.signs.length - 1,
      tail: tail.length ? tail.join(' ') : '<END>',
      text: row.text,
    });
  }
}

const byHead = new Map();
for (const frame of frames) {
  if (!byHead.has(frame.head)) byHead.set(frame.head, []);
  byHead.get(frame.head).push(frame);
}

const headRows = [];
for (const [head, group] of byHead.entries()) {
  const exactTextCollapsed = [...new Map(group.map((frame) => [frame.text, frame])).values()];
  const branchCounts = new Map();
  for (const frame of group) branchCounts.set(frame.branch, (branchCounts.get(frame.branch) ?? 0) + 1);
  const repeatedBranches = [...branchCounts.values()].filter((count) => count > 1).length;
  const test = group.length >= 6 && branchCounts.size >= 3 ? determinismP(group) : null;
  const collapsedTest =
    exactTextCollapsed.length >= 6 && new Set(exactTextCollapsed.map((frame) => frame.branch)).size >= 3
      ? determinismP(exactTextCollapsed)
      : null;
  headRows.push({
    head,
    frame_rows: group.length,
    exact_text_rows: exactTextCollapsed.length,
    branch_count: branchCounts.size,
    repeated_branch_count: repeatedBranches,
    terminal_rows: group.filter((frame) => frame.terminal).length,
    continuing_rows: group.filter((frame) => !frame.terminal).length,
    determinism_score: test?.score ?? '',
    determinism_p: test?.p ?? '',
    determinism_method: test?.method ?? '',
    exact_text_determinism_score: collapsedTest?.score ?? '',
    exact_text_determinism_p: collapsedTest?.p ?? '',
    exact_text_method: collapsedTest?.method ?? '',
    pure_branches: test?.pureBranches ?? '',
    branch_counts: [...branchCounts.entries()].map(([branch, count]) => `${branch}:${count}`).join(';'),
    examples: group.slice(0, 12).map((frame) => `${frame.object}:${frame.prev}-002-${frame.head}-${frame.branch}-${frame.tail}:${frame.terminal ? 'T' : 'C'}`).join('|'),
  });
}

headRows.sort((a, b) => {
  const ap = a.determinism_p === '' ? 2 : Number(a.determinism_p);
  const bp = b.determinism_p === '' ? 2 : Number(b.determinism_p);
  return ap - bp || Number(b.frame_rows) - Number(a.frame_rows);
});

const head390 = headRows.find((row) => row.head === '390');
const competitive = headRows.filter((row) => row.determinism_p !== '' && Number(row.frame_rows) >= 10 && Number(row.branch_count) >= 5);
const betterOrEqual = competitive.filter((row) => Number(row.determinism_p) <= Number(head390.determinism_p));
const bet = {
  run_date: RUN_DATE,
  bet_id: 'V2_002_HEAD_BRANCH_DETERMINISM_390_20260531',
  vector: 'V2 effective-unicity / slot grammar',
  confidence_tier: Number(head390.determinism_p) <= 0.05 && betterOrEqual.length <= 3 ? 'candidate' : 'wild shot',
  risky_bet: '`390` is not merely frequent after `002`; among multi-branch `002-H-X` heads it is an unusually deterministic branch-choice head, making `002-390-X` a real slot grammar object.',
  observed: `head 390: ${head390.frame_rows} rows, ${head390.branch_count} branches, determinism score ${head390.determinism_score}/${head390.frame_rows}, exact-text score ${head390.exact_text_determinism_score}/${head390.exact_text_rows}; p=${head390.determinism_p}; exact-text p=${head390.exact_text_determinism_p}; competitive heads with p <= 390: ${betterOrEqual.map((row) => row.head).join('/')}.`,
  adversarial_test: 'All `002-H-X` frames were scanned. For heads with >=6 rows and >=3 branches, terminal/continuing labels were permuted while preserving branch layout and continuation count; exact-text collapsed version repeated the test.',
  false_positive_rate: head390.determinism_p,
  exact_text_false_positive_rate: head390.exact_text_determinism_p,
  falsifier: 'If many other `002-H-X` heads with comparable row and branch counts show equal or stronger deterministic terminality, the 390 slot claim demotes to generic short-row artifact.',
  next_prediction: 'New or source-normalized `002-390-X` rows should keep branch-determined terminality; other heads with strong p-values should reveal their own branch classes rather than random mixed behavior.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), JSON.stringify({
  ...bet,
  head390,
  competitive_heads: competitive,
  all_heads: headRows,
}, null, 2));
writeCsv(path.join(OUT_DIR, `${PREFIX}.csv`), [bet], [
  'run_date',
  'bet_id',
  'vector',
  'confidence_tier',
  'risky_bet',
  'observed',
  'adversarial_test',
  'false_positive_rate',
  'exact_text_false_positive_rate',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_heads.csv`), headRows, [
  'head',
  'frame_rows',
  'exact_text_rows',
  'branch_count',
  'repeated_branch_count',
  'terminal_rows',
  'continuing_rows',
  'determinism_score',
  'determinism_p',
  'determinism_method',
  'exact_text_determinism_score',
  'exact_text_determinism_p',
  'exact_text_method',
  'pure_branches',
  'branch_counts',
  'examples',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_frames.csv`), frames, [
  'id',
  'object',
  'site',
  'type',
  'symbol',
  'cult',
  'shape',
  'material',
  'prev',
  'head',
  'branch',
  'terminal',
  'tail',
  'text',
]);
console.log(JSON.stringify(bet, null, 2));
