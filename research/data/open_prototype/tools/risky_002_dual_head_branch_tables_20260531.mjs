import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_002_dual_head_branch_tables_20260531';
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

function determinismScore(frames, labels) {
  const byBranch = new Map();
  frames.forEach((frame, idx) => {
    if (!byBranch.has(frame.branch)) byBranch.set(frame.branch, []);
    byBranch.get(frame.branch).push(labels[idx]);
  });
  let score = 0;
  for (const values of byBranch.values()) {
    const cont = values.filter(Boolean).length;
    score += Math.max(cont, values.length - cont);
  }
  return score;
}

function branchClass(frames) {
  const byBranch = new Map();
  for (const frame of frames) {
    if (!byBranch.has(frame.branch)) byBranch.set(frame.branch, []);
    byBranch.get(frame.branch).push(!frame.terminal);
  }
  return [...byBranch.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([branch, labels]) => {
      const cont = labels.filter(Boolean).length;
      return `${branch}:${cont === labels.length ? 'open' : cont === 0 ? 'closed' : 'mixed'}:${labels.length}`;
    })
    .join(';');
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
      shape: norm(row.shape),
      prev: row.signs[i - 1] ?? '<START>',
      head: row.signs[i + 1],
      branch: row.signs[i + 2],
      terminal: i + 2 === row.signs.length - 1,
      tail: row.signs.slice(i + 3).join(' ') || '<END>',
      text: row.text,
    });
  }
}

function exactCollapse(group) {
  return [...new Map(group.map((frame) => [frame.text, frame])).values()];
}

const groups = new Map();
for (const frame of frames) {
  if (!groups.has(frame.head)) groups.set(frame.head, []);
  groups.get(frame.head).push(frame);
}

const competitive = [...groups.entries()]
  .map(([head, group]) => [head, exactCollapse(group)])
  .filter(([, group]) => group.length >= 8 && new Set(group.map((frame) => frame.branch)).size >= 5)
  .map(([head, group]) => {
    const labels = group.map((frame) => !frame.terminal);
    const observedScore = determinismScore(group, labels);
    return {
      head,
      group,
      labels,
      observedScore,
      rows: group.length,
      branchCount: new Set(group.map((frame) => frame.branch)).size,
    };
  });

const rand = mulberry32(0x2861390);
const scoreSamples = new Map();
for (const item of competitive) {
  const samples = [];
  for (let iter = 0; iter < ITERATIONS; iter += 1) {
    samples.push(determinismScore(item.group, shuffle(rand, item.labels)));
  }
  samples.sort((a, b) => a - b);
  scoreSamples.set(item.head, samples);
}

function sampleP(head, score) {
  const samples = scoreSamples.get(head);
  let firstGe = samples.findIndex((value) => value >= score);
  if (firstGe < 0) return 0;
  return (samples.length - firstGe) / samples.length;
}

const headRows = competitive.map((item) => ({
  head: item.head,
  rows: item.rows,
  branch_count: item.branchCount,
  terminal_rows: item.group.filter((frame) => frame.terminal).length,
  continuing_rows: item.group.filter((frame) => !frame.terminal).length,
  observed_score: item.observedScore,
  sampled_p: sampleP(item.head, item.observedScore),
  branch_classes: branchClass(item.group),
  examples: item.group.map((frame) => `${frame.object}:${frame.prev}-002-${frame.head}-${frame.branch}-${frame.tail}:${frame.terminal ? 'T' : 'C'}`).join('|'),
})).sort((a, b) => Number(a.sampled_p) - Number(b.sampled_p));

const targetHeads = new Set(['861', '390']);
const observedTargetPs = Object.fromEntries(headRows.filter((row) => targetHeads.has(row.head)).map((row) => [row.head, Number(row.sampled_p)]));
let nullAtLeastTwoUnder005 = 0;
let nullBothTargetsAsGood = 0;
let nullAnyPairAsGoodAsTargets = 0;
let nullProductAtLeastObserved = 0;
const observedProduct = observedTargetPs['861'] * observedTargetPs['390'];

for (let iter = 0; iter < ITERATIONS; iter += 1) {
  const simRows = competitive.map((item) => {
    const score = determinismScore(item.group, shuffle(rand, item.labels));
    return {
      head: item.head,
      p: sampleP(item.head, score),
    };
  });
  const under005 = simRows.filter((row) => row.p <= 0.05);
  if (under005.length >= 2) nullAtLeastTwoUnder005 += 1;
  const p861 = simRows.find((row) => row.head === '861')?.p ?? 1;
  const p390 = simRows.find((row) => row.head === '390')?.p ?? 1;
  if (p861 <= observedTargetPs['861'] && p390 <= observedTargetPs['390']) nullBothTargetsAsGood += 1;
  const sorted = simRows.map((row) => row.p).sort((a, b) => a - b);
  if (sorted[0] <= Math.min(observedTargetPs['861'], observedTargetPs['390']) && sorted[1] <= Math.max(observedTargetPs['861'], observedTargetPs['390'])) {
    nullAnyPairAsGoodAsTargets += 1;
  }
  if (sorted[0] * sorted[1] <= observedProduct) nullProductAtLeastObserved += 1;
}

const h861 = headRows.find((row) => row.head === '861');
const h390 = headRows.find((row) => row.head === '390');
const bet = {
  run_date: RUN_DATE,
  bet_id: 'V2_002_DUAL_BRANCH_TABLES_861_390_20260531',
  vector: 'V2 effective-unicity / slot grammar',
  confidence_tier: 'candidate',
  risky_bet: '`002` introduces head-specific branch tables. The live tables are `002-861-X` and `002-390-X`: branch identity predicts whether the branch closes or licenses tail material.',
  observed: `Exact-text-collapsed head 861: ${h861.rows} rows, ${h861.branch_count} branches, score ${h861.observed_score}/${h861.rows}, p=${h861.sampled_p}. Head 390: ${h390.rows} rows, ${h390.branch_count} branches, score ${h390.observed_score}/${h390.rows}, p=${h390.sampled_p}. Competitive exact-text heads tested: ${competitive.length}.`,
  adversarial_test: `Within each competitive 002-H-X head, terminal/continuing labels were shuffled ${ITERATIONS} times preserving head layout and terminal count. Multi-head nulls ask whether any two heads look as good as 861/390, and whether the specific 861+390 pair recurs by chance. This survives null pressure but is not promoted because source-stability is still incomplete.`,
  false_positive_rate: nullAnyPairAsGoodAsTargets / ITERATIONS,
  specific_pair_false_positive_rate: nullBothTargetsAsGood / ITERATIONS,
  at_least_two_under_005_rate: nullAtLeastTwoUnder005 / ITERATIONS,
  best_pair_product_rate: nullProductAtLeastObserved / ITERATIONS,
  falsifier: 'A source-normalized row that makes any repeated 861 or 390 branch mixed in terminality demotes the table; a broader scan with many comparable exact-text heads as deterministic as 861/390 demotes it to a short-row artifact.',
  next_prediction: '`002-861-416/096/603/698/533` should stay class-pure after source normalization, and new `002-390-125/530/590` should continue while `002-390-095/692/705` should close.',
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
  'specific_pair_false_positive_rate',
  'at_least_two_under_005_rate',
  'best_pair_product_rate',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_heads.csv`), headRows, [
  'head',
  'rows',
  'branch_count',
  'terminal_rows',
  'continuing_rows',
  'observed_score',
  'sampled_p',
  'branch_classes',
  'examples',
]);
console.log(JSON.stringify(bet, null, 2));
