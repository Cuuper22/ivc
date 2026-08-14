// Adversarial recheck of the "002 dual-head bipolar" risky bet, run
// 2026-05-31. The bet: after sign 002, the heads 861 and 390 each split into
// branch signs that are purely "open" (text continues) or purely "closed"
// (text ends), never mixed — a switch-like pattern. Earlier support came from
// collapsing duplicate raw text strings; this recheck collapses on the
// canonical numeric sign sequence instead, which removes more near-duplicates
// and is the harsher test.
//
// The script reads lipi/metadata_filtered.csv, keeps one row per distinct
// sign sequence, extracts every 002-head-branch frame, and finds competitive
// heads (8+ frames, 5+ distinct branches). "Bipolar pure" requires 8+ rows in
// repeated branches, at least one open and one closed branch, and no mixed
// branch. A 100,000-iteration label shuffle gives false-positive rates for
// 861 and 390 individually, the specific pair, and any pair. A separate
// 100,000-draw shuffle checks whether the canonical 002-861-096 rows are more
// often ivory RODs than chance predicts.
//
// It writes risky_002_canonical_sequence_collapse_recheck_20260531.json,
// .csv (the bet card with rates, falsifier, and confidence tier), and
// _heads.csv. The tier auto-demotes to "wild shot" unless both heads pass and
// the pair false-positive rate is at most 1%.

import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_002_canonical_sequence_collapse_recheck_20260531';
const RUN_DATE = '2026-05-31';
const ITERATIONS = 100000;

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

function choose(rand, arr) {
  return arr[Math.floor(rand() * arr.length)];
}

function branchClasses(group, labels) {
  const byBranch = new Map();
  group.forEach((frame, idx) => {
    if (!byBranch.has(frame.branch)) byBranch.set(frame.branch, []);
    byBranch.get(frame.branch).push(labels[idx]);
  });
  const rows = [];
  for (const [branch, values] of byBranch.entries()) {
    if (values.length < 2) continue;
    const cont = values.filter(Boolean).length;
    rows.push({
      branch,
      count: values.length,
      branch_class: cont === values.length ? 'open' : cont === 0 ? 'closed' : 'mixed',
    });
  }
  return rows.sort((a, b) => a.branch.localeCompare(b.branch));
}

function bipolarPure(group, labels, minRepeatedRows = 8) {
  const classes = branchClasses(group, labels);
  const repeatedRows = classes.reduce((sum, row) => sum + row.count, 0);
  const hasOpen = classes.some((row) => row.branch_class === 'open');
  const hasClosed = classes.some((row) => row.branch_class === 'closed');
  const hasMixed = classes.some((row) => row.branch_class === 'mixed');
  return {
    classes,
    repeatedRows,
    repeatedClasses: classes.length,
    hasOpen,
    hasClosed,
    hasMixed,
    pass: repeatedRows >= minRepeatedRows && hasOpen && hasClosed && !hasMixed,
  };
}

function hasSeq(row, seq) {
  return row.signs.some((_, idx) => seq.every((sign, j) => row.signs[idx + j] === sign));
}

function isRodIvory(row) {
  return norm(row.type) === 'ROD' && norm(row.material) === 'Ivory';
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()];

const frames = [];
for (const row of canonicalRows) {
  for (let i = 0; i < row.signs.length - 2; i += 1) {
    if (row.signs[i] !== '002') continue;
    frames.push({
      object: objectId(row),
      site: norm(row.site),
      type: norm(row.type),
      material: norm(row.material),
      symbol: norm(row.symbol),
      canonical_sequence: row.signs.join(' '),
      prev: row.signs[i - 1] ?? '<START>',
      head: row.signs[i + 1],
      branch: row.signs[i + 2],
      terminal: i + 2 === row.signs.length - 1,
      tail: row.signs.slice(i + 3).join(' ') || '<END>',
      text: row.text,
    });
  }
}

const byHead = new Map();
for (const frame of frames) {
  if (!byHead.has(frame.head)) byHead.set(frame.head, []);
  byHead.get(frame.head).push(frame);
}

const competitive = [...byHead.entries()]
  .filter(([, group]) => group.length >= 8 && new Set(group.map((frame) => frame.branch)).size >= 5)
  .map(([head, group]) => ({
    head,
    group,
    labels: group.map((frame) => !frame.terminal),
    observed: bipolarPure(group, group.map((frame) => !frame.terminal), 8),
  }));

const headRows = competitive.map((item) => ({
  head: item.head,
  canonical_rows: item.group.length,
  terminal_rows: item.group.filter((frame) => frame.terminal).length,
  continuing_rows: item.group.filter((frame) => !frame.terminal).length,
  branch_count: new Set(item.group.map((frame) => frame.branch)).size,
  repeated_classes: item.observed.repeatedClasses,
  repeated_rows: item.observed.repeatedRows,
  bipolar_pure: item.observed.pass,
  class_table: item.observed.classes.map((row) => `${row.branch}:${row.branch_class}:${row.count}`).join(';'),
  examples: item.group.map((frame) => `${frame.object}:${frame.prev}-002-${frame.head}-${frame.branch}-${frame.tail}:${frame.terminal ? 'T' : 'C'}:${frame.canonical_sequence}`).join('|'),
}));

const rand = mulberry32(0x2002861);
let specificPair = 0;
let anyPair = 0;
let h861Count = 0;
let h390Count = 0;
for (let iter = 0; iter < ITERATIONS; iter += 1) {
  const sim = competitive.map((item) => ({
    head: item.head,
    pass: bipolarPure(item.group, shuffle(rand, item.labels), 8).pass,
  }));
  const h861 = sim.find((row) => row.head === '861')?.pass ?? false;
  const h390 = sim.find((row) => row.head === '390')?.pass ?? false;
  if (h861) h861Count += 1;
  if (h390) h390Count += 1;
  if (h861 && h390) specificPair += 1;
  if (sim.filter((row) => row.pass).length >= 2) anyPair += 1;
}

const all002861 = canonicalRows.filter((row) => hasSeq(row, ['002', '861']));
const target861096 = canonicalRows.filter((row) => hasSeq(row, ['002', '861', '096']));
let rodGe = 0;
for (let iter = 0; iter < ITERATIONS; iter += 1) {
  let score = 0;
  for (let i = 0; i < target861096.length; i += 1) if (isRodIvory(choose(rand, all002861))) score += 1;
  if (score >= target861096.filter(isRodIvory).length) rodGe += 1;
}

const h861 = headRows.find((row) => row.head === '861');
const h390 = headRows.find((row) => row.head === '390');
const bet = {
  run_date: RUN_DATE,
  bet_id: 'V2_CANONICAL_COLLAPSE_002_BRANCH_TABLE_RECHECK_20260531',
  vector: 'V2 effective-unicity / source-independent collapse control',
  confidence_tier: specificPair / ITERATIONS <= 0.01 && h861?.bipolar_pure && h390?.bipolar_pure ? 'candidate' : 'wild shot',
  risky_bet: 'The `002-861/390` repeated-branch bipolar pattern should survive canonical numeric-sequence collapse, not just raw text/bracket-string collapse.',
  observed: `Canonical collapse reduces corpus rows from ${rawRows.length} to ${canonicalRows.length}. ` +
    `Head 861: repeated ${h861?.class_table || '<none>'}; pass=${h861?.bipolar_pure}. Head 390: repeated ${h390?.class_table || '<none>'}; pass=${h390?.bipolar_pure}. ` +
    `Canonical 861|096 register target rows: ${target861096.length}, ivory ROD ${target861096.filter(isRodIvory).length}/${target861096.length}.`,
  adversarial_test: `Canonical sign-sequence collapse, then repeated-branch-only bipolar forger with ${ITERATIONS} shuffles; separate canonical 861|096 rod-register shuffle inside all canonical 002-861 rows.`,
  false_positive_rate: specificPair / ITERATIONS,
  any_pair_false_positive_rate: anyPair / ITERATIONS,
  head_861_false_positive_rate: h861Count / ITERATIONS,
  head_390_false_positive_rate: h390Count / ITERATIONS,
  rod_register_false_positive_rate: rodGe / ITERATIONS,
  falsifier: 'If canonical collapse removes either 861 or 390 from repeated bipolar purity, the dual-head bet demotes. If 861|096 collapses to one target row, rod-register evidence demotes from candidate to wild shot regardless of low shuffle p.',
  next_prediction: 'The next real promotion needs source-normalized independent witnesses for 861|096 or another repeated branch, not another raw duplicate of the same numeric sequence.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), JSON.stringify({ ...bet, heads: headRows }, null, 2));
writeCsv(path.join(OUT_DIR, `${PREFIX}.csv`), [bet], [
  'run_date',
  'bet_id',
  'vector',
  'confidence_tier',
  'risky_bet',
  'observed',
  'adversarial_test',
  'false_positive_rate',
  'any_pair_false_positive_rate',
  'head_861_false_positive_rate',
  'head_390_false_positive_rate',
  'rod_register_false_positive_rate',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_heads.csv`), headRows, [
  'head',
  'canonical_rows',
  'terminal_rows',
  'continuing_rows',
  'branch_count',
  'repeated_classes',
  'repeated_rows',
  'bipolar_pure',
  'class_table',
  'examples',
]);
console.log(JSON.stringify(bet, null, 2));
