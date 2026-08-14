// A "forger" test: can chance alone forge the shape we credit to sign 530? The observed
// claim is that every 002-H-530 frame carries exactly one complement sign, spread across
// several heads, sites, and complement signs. If random draws of frames often show the same
// shape, the claim is worthless. We read the filtered Indus inscription list
// (lipi/metadata_filtered.csv), keep one copy of each distinct sign sequence, extract every
// governed frame (002 + head + branch + tail), and profile each branch sign. Then we compare
// 530 against branches with matching frame counts, and draw 100,000 random frame samples of
// the same size (seeded PRNG, so runs repeat exactly) to estimate how often chance matches
// or beats the 530 shape. Writes branch tables, target rows, passers, and a decision CSV plus
// a JSON summary to data/open_prototype/reports.
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_530_one_complement_forger_20260531';
const checkedDate = '2026-05-31';
const iterations = 100000;
const targetBranch = '530';

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (ch === '"' && next === '"') {
        field += '"';
        i += 1;
      } else if (ch === '"') {
        quoted = false;
      } else {
        field += ch;
      }
    } else if (ch === '"') {
      quoted = true;
    } else if (ch === ',') {
      row.push(field);
      field = '';
    } else if (ch === '\n') {
      row.push(field.replace(/\r$/, ''));
      rows.push(row);
      row = [];
      field = '';
    } else {
      field += ch;
    }
  }
  if (field.length || row.length) {
    row.push(field.replace(/\r$/, ''));
    rows.push(row);
  }
  const header = rows.shift() ?? [];
  return rows
    .filter((r) => r.some((value) => value !== ''))
    .map((r) => Object.fromEntries(header.map((name, index) => [name, r[index] ?? ''])));
}

function csvEscape(value) {
  const text = String(value ?? '');
  return /[",\n\r]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(',')];
  for (const row of rows) lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function signs(text) {
  return [...String(text || '').matchAll(/\d{3}/g)].map((match) => match[0]);
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function countBy(items, fn) {
  const counts = new Map();
  for (const item of items) {
    const key = fn(item) || '-';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()].sort(
    (a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }),
  );
}

function topCounts(items, fn, n = 10) {
  return countBy(items, fn)
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function mulberry32(seed) {
  return function rand() {
    let t = (seed += 0x6D2B79F5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function sampleIndexes(rand, n, k) {
  const out = new Set();
  while (out.size < k) out.add(Math.floor(rand() * n));
  return [...out];
}

function stats(rows) {
  return {
    n: rows.length,
    oneComplement: rows.filter((row) => row.tailLength === 1).length,
    continuing: rows.filter((row) => row.tailLength > 0).length,
    distinctHeads: new Set(rows.map((row) => row.head)).size,
    distinctSites: new Set(rows.map((row) => row.site)).size,
    distinctTypes: new Set(rows.map((row) => row.type)).size,
    firstTails: new Set(rows.map((row) => row.firstTail)).size,
  };
}

function passesTargetShape(s, target) {
  return (
    s.oneComplement >= target.oneComplement &&
    s.distinctHeads >= target.distinctHeads &&
    s.distinctSites >= target.distinctSites &&
    s.firstTails >= target.firstTails
  );
}

fs.mkdirSync(reportsDir, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  tokens: signs(row.text),
}));
const canonicalRows = [...new Map(rawRows.map((row) => [row.tokens.join(' '), row])).values()];

const governedFrames = [];
for (const row of canonicalRows) {
  for (let i = 0; i < row.tokens.length - 2; i += 1) {
    if (row.tokens[i] !== '002') continue;
    const tail = row.tokens.slice(i + 3);
    governedFrames.push({
      checked_date: checkedDate,
      cisi: objectId(row),
      row_id: row.id,
      site: row.site || '-',
      type: row.type || '-',
      shape: row.shape || '-',
      head: row.tokens[i + 1],
      branch: row.tokens[i + 2],
      tail: tail.join(' ') || '<END>',
      tailLength: tail.length,
      firstTail: tail[0] ?? '<END>',
      text: row.text,
    });
  }
}

const byBranch = countBy(governedFrames, (row) => row.branch).map(([branch, count]) => {
  const rows = governedFrames.filter((row) => row.branch === branch);
  const s = stats(rows);
  return {
    checked_date: checkedDate,
    branch,
    frames: String(count),
    one_complement: String(s.oneComplement),
    one_complement_share: (s.oneComplement / s.n).toFixed(6),
    continuing: String(s.continuing),
    continuing_share: (s.continuing / s.n).toFixed(6),
    distinct_heads: String(s.distinctHeads),
    distinct_sites: String(s.distinctSites),
    distinct_types: String(s.distinctTypes),
    distinct_first_tails: String(s.firstTails),
    heads: topCounts(rows, (row) => row.head),
    sites: topCounts(rows, (row) => row.site),
    first_tails: topCounts(rows, (row) => row.firstTail),
    examples: rows.slice(0, 10).map((row) => `${row.cisi}:${row.text}`).join(' | '),
  };
});

const targetRows = governedFrames.filter((row) => row.branch === targetBranch);
const target = stats(targetRows);
const exactCountPeers = byBranch.filter((row) => Number(row.frames) === target.n);
const countWindowPeers = byBranch.filter((row) => Number(row.frames) >= 2 && Number(row.frames) <= 8);
const exactCountPass = exactCountPeers.filter((row) =>
  passesTargetShape(
    {
      oneComplement: Number(row.one_complement),
      distinctHeads: Number(row.distinct_heads),
      distinctSites: Number(row.distinct_sites),
      firstTails: Number(row.distinct_first_tails),
    },
    target,
  ),
);
const windowPass = countWindowPeers.filter((row) =>
  passesTargetShape(
    {
      oneComplement: Number(row.one_complement),
      distinctHeads: Number(row.distinct_heads),
      distinctSites: Number(row.distinct_sites),
      firstTails: Number(row.distinct_first_tails),
    },
    target,
  ),
);

const rand = mulberry32(0x5302026);
let randomPass = 0;
let randomOneComplementPass = 0;
for (let i = 0; i < iterations; i += 1) {
  const sample = sampleIndexes(rand, governedFrames.length, target.n).map((idx) => governedFrames[idx]);
  const s = stats(sample);
  if (s.oneComplement >= target.oneComplement) randomOneComplementPass += 1;
  if (passesTargetShape(s, target)) randomPass += 1;
}

const decision =
  exactCountPass.length === 1 && windowPass.length <= 1 && randomPass / iterations <= 0.01
    ? 'candidate_strengthened_against_penultimate_null'
    : randomPass / iterations <= 0.05
      ? 'candidate_retained_but_not_strengthened'
      : 'demote_to_wild_shot_common_shape';

const decisions = [
  {
    checked_date: checkedDate,
    bet_id: 'V2_530_ONE_COMPLEMENT_NOT_PENULTIMATE_NULL_20260531',
    confidence_tier: decision.startsWith('candidate') ? 'candidate' : 'wild shot',
    decision,
    risky_parse_bet:
      '`530` is not merely occupying a common penultimate branch slot; its governed rows combine one-complement shape with four heads, four sites, and four complement signs.',
    what_would_promote:
      'A fifth source-visible `002-H-530-Y` row under a new head/site also has exactly one complement, while no other count-matched branch catches up.',
    what_would_break:
      'Count-matched branches with comparable head/site spread routinely match the same shape, or a current `530` row is source-collapsed as non-comparable.',
  },
];

const summary = {
  checked_date: checkedDate,
  status: '530_one_complement_forger',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: canonicalRows.length,
    governed_frames: governedFrames.length,
    target_frames: target.n,
  },
  target: {
    one_complement: target.oneComplement,
    distinct_heads: target.distinctHeads,
    distinct_sites: target.distinctSites,
    distinct_first_tails: target.firstTails,
    examples: targetRows.map((row) => `${row.cisi}:${row.text}`).join(' | '),
  },
  exact_count_peers: exactCountPeers.length,
  exact_count_passers: exactCountPass.map((row) => row.branch).join(';'),
  count_window_peers: countWindowPeers.length,
  count_window_passers: windowPass.map((row) => row.branch).join(';'),
  random_one_complement_false_positive_rate: randomOneComplementPass / iterations,
  random_shape_false_positive_rate: randomPass / iterations,
  decisions: decisions.map((row) => `${row.bet_id}:${row.decision}`).join(';'),
};

writeCsv(path.join(reportsDir, `${prefix}_branch_table.csv`), byBranch, [
  'checked_date',
  'branch',
  'frames',
  'one_complement',
  'one_complement_share',
  'continuing',
  'continuing_share',
  'distinct_heads',
  'distinct_sites',
  'distinct_types',
  'distinct_first_tails',
  'heads',
  'sites',
  'first_tails',
  'examples',
]);

writeCsv(path.join(reportsDir, `${prefix}_target_rows.csv`), targetRows, [
  'checked_date',
  'cisi',
  'row_id',
  'site',
  'type',
  'shape',
  'head',
  'branch',
  'tail',
  'firstTail',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_passers.csv`), windowPass, [
  'checked_date',
  'branch',
  'frames',
  'one_complement',
  'one_complement_share',
  'continuing',
  'continuing_share',
  'distinct_heads',
  'distinct_sites',
  'distinct_types',
  'distinct_first_tails',
  'heads',
  'sites',
  'first_tails',
  'examples',
]);

writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  'checked_date',
  'bet_id',
  'confidence_tier',
  'decision',
  'risky_parse_bet',
  'what_would_promote',
  'what_would_break',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
