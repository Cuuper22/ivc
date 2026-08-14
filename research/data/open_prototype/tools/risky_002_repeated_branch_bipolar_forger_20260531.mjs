// Looks at `002-H-X` frames (sign 002, then head H, then branch X) and asks whether
// heads 861 and 390 show "repeated-branch bipolar purity". A branch is "repeated" if
// the same X appears in at least two distinct texts under one head. Each repeated
// branch is classed "open" (every occurrence continues past X), "closed" (every
// occurrence ends at X), or "mixed". The bet: under both `002-861` and `002-390`,
// repeated branches split cleanly into open and closed classes with no mixed class —
// branch choice deterministically decides whether the text ends. Reads
// metadata_filtered.csv, collapses each head's frames to unique texts, then runs a
// 100,000-iteration forger that shuffles terminal/continuing labels within each head
// (keeping branch layout and terminal counts) to price how often chance produces the
// same bipolar-pure pattern in both heads at once. Writes a bet summary (JSON + CSV)
// and a per-head table to the reports directory.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_002_repeated_branch_bipolar_forger_20260531';
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

function bipolarPure(group, labels, minRepeatedRows = 2) {
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

const rows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const frames = [];
for (const row of rows) {
  for (let i = 0; i < row.signs.length - 2; i += 1) {
    if (row.signs[i] !== '002') continue;
    frames.push({
      id: row.id,
      object: objectId(row),
      site: norm(row.site),
      type: norm(row.type),
      symbol: norm(row.symbol),
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

function exactCollapse(group) {
  return [...new Map(group.map((frame) => [frame.text, frame])).values()];
}

const competitive = [...byHead.entries()]
  .map(([head, group]) => [head, exactCollapse(group)])
  .filter(([, group]) => group.length >= 8 && new Set(group.map((frame) => frame.branch)).size >= 5)
  .map(([head, group]) => ({
    head,
    group,
    labels: group.map((frame) => !frame.terminal),
    observed: bipolarPure(group, group.map((frame) => !frame.terminal), 8),
  }));

const headRows = competitive.map((item) => ({
  head: item.head,
  exact_rows: item.group.length,
  terminal_rows: item.group.filter((frame) => frame.terminal).length,
  continuing_rows: item.group.filter((frame) => !frame.terminal).length,
  branch_count: new Set(item.group.map((frame) => frame.branch)).size,
  repeated_classes: item.observed.repeatedClasses,
  repeated_rows: item.observed.repeatedRows,
  bipolar_pure: item.observed.pass,
  class_table: item.observed.classes.map((row) => `${row.branch}:${row.branch_class}:${row.count}`).join(';'),
  examples: item.group.map((frame) => `${frame.object}:${frame.prev}-002-${frame.head}-${frame.branch}-${frame.tail}:${frame.terminal ? 'T' : 'C'}`).join('|'),
}));

const rand = mulberry32(0x2290861);
let specificPair = 0;
let anyPairRepeated8 = 0;
let anySpecificOrBetter = 0;
let target861Only = 0;
let target390Only = 0;
for (let iter = 0; iter < ITERATIONS; iter += 1) {
  const sim = competitive.map((item) => ({
    head: item.head,
    result: bipolarPure(item.group, shuffle(rand, item.labels), 8),
  }));
  const h861 = sim.find((item) => item.head === '861')?.result.pass ?? false;
  const h390 = sim.find((item) => item.head === '390')?.result.pass ?? false;
  if (h861) target861Only += 1;
  if (h390) target390Only += 1;
  if (h861 && h390) specificPair += 1;
  const passing = sim.filter((item) => item.result.pass);
  if (passing.length >= 2) anyPairRepeated8 += 1;
  if (passing.some((item) => item.head === '861') && passing.some((item) => item.head === '390')) anySpecificOrBetter += 1;
}

const bet = {
  run_date: RUN_DATE,
  bet_id: 'V2_002_861_390_REPEATED_BRANCH_BIPOLAR_FORGER_20260531',
  vector: 'V2 effective-unicity / solution-space degeneracy',
  confidence_tier: specificPair / ITERATIONS <= 0.01 ? 'candidate' : 'wild shot',
  risky_bet: 'The real signal in the `002` branch-table system is repeated-branch bipolar purity: both `002-861-X` and `002-390-X` contain repeated open and repeated closed branch classes, with no mixed repeated class after exact-text collapse.',
  observed: `Competitive exact-text heads: ${competitive.length}. Observed repeated-branch bipolar-pure heads with >=8 repeated rows: ${headRows.filter((row) => row.bipolar_pure).map((row) => row.head).join('/')}. ` +
    `861 repeated classes: ${headRows.find((row) => row.head === '861')?.class_table}. 390 repeated classes: ${headRows.find((row) => row.head === '390')?.class_table}.`,
  adversarial_test: `Forger shuffles terminal/continuing labels within each competitive head ${ITERATIONS} times, preserving head size, branch layout, and terminal count, then ignores singleton branches and asks whether repeated branches alone are bipolar-pure.`,
  false_positive_rate: specificPair / ITERATIONS,
  any_pair_false_positive_rate: anyPairRepeated8 / ITERATIONS,
  head_861_false_positive_rate: target861Only / ITERATIONS,
  head_390_false_positive_rate: target390Only / ITERATIONS,
  falsifier: 'A source-normalized mixed repeated branch in either head, especially 390|705 or 861|096/000, kills the repeated-branch form of the bet.',
  next_prediction: 'New exact-text-independent repeated branches under `002-861` or `002-390` should join an all-open or all-closed branch class rather than split within the same branch sign.',
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
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_heads.csv`), headRows, [
  'head',
  'exact_rows',
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
