// Discriminator for "left-context operators": do the signs sitting to the left of a governed
// 002 frame act like operators that steer what the frame selects? The specific claims: a
// final 235 before 002 plus a P086-family head (390 or 405) selects 125; 032 on the left
// without 235 pushes the frame toward boundary/formula/result closure and away from 125; and
// a final 004 is a neutral qualifier that can go either way (095 or 125). We read the
// filtered Indus inscription list (lipi/metadata_filtered.csv), keep one copy of each
// distinct sign sequence, extract every governed frame with its full left context, and tag
// each frame by left pattern. Per-tag summaries then check every condition of the operator
// model at once; the bet is only a candidate if all five hold. Writes tag-summary,
// 390-target-row, and decision CSVs plus a JSON summary to data/open_prototype/reports.
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_left_context_operator_discriminator_20260531';
const checkedDate = '2026-05-31';
const p086Heads = new Set(['390', '405']);
const closureHeads = new Set(['817', '820', '861']);

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

function topCounts(items, fn, n = 12) {
  return countBy(items, fn)
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function safeShare(num, den) {
  return den ? (num / den).toFixed(6) : 'NA';
}

function exampleRows(rows, n = 10) {
  return rows
    .slice(0, n)
    .map((row) => `${row.cisi}:${row.left_final}-002-${row.head}-${row.branch}-${row.tail}`)
    .join(' | ');
}

function tagFrame(frame) {
  const tags = [];
  if (frame.left_final === '235') tags.push('final235');
  if (frame.left_final === '032' && !frame.left_tokens.includes('235')) tags.push('final032_no235');
  if (frame.left_tokens.includes('032') && !frame.left_tokens.includes('235')) tags.push('contains032_no235');
  if (frame.left_final === '004') tags.push('final004');
  if (frame.left_tokens.includes('004')) tags.push('contains004');
  if (!tags.length) tags.push('other_left');
  return tags;
}

function target390Read(frame) {
  if (frame.left_final === '235' && frame.branch === '125') return 'rank_title_trigger';
  if (frame.left_final === '032' && ['590', '692'].includes(frame.branch)) return 'boundary_formula_or_result';
  if (frame.left_tokens.includes('032') && frame.branch === '705') return 'embedded_boundary_to_formula_reuse';
  if (frame.left_final === '004' && ['095', '125'].includes(frame.branch)) return 'neutral_qualifier_split';
  return 'untyped_left_context';
}

fs.mkdirSync(reportsDir, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  tokens: signs(row.text),
}));
const canonicalRows = [...new Map(rawRows.map((row) => [row.tokens.join(' '), row])).values()];

const frames = [];
for (const row of canonicalRows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
    if (row.tokens[i] !== '002' || !row.tokens[i + 1] || !row.tokens[i + 2]) continue;
    const leftTokens = row.tokens.slice(0, i);
    const tail = row.tokens.slice(i + 3);
    const frame = {
      checked_date: checkedDate,
      cisi: objectId(row),
      row_id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      left_tokens: leftTokens,
      left: leftTokens.join(' ') || '<START>',
      left_final: leftTokens.at(-1) ?? '<START>',
      head: row.tokens[i + 1],
      branch: row.tokens[i + 2],
      tail: tail.join(' ') || '<END>',
      tail_length: tail.length,
      terminal_after_branch: tail.length === 0,
      has_125_in_branch_or_tail: row.tokens[i + 2] === '125' || tail.includes('125'),
      is_p086_head: p086Heads.has(row.tokens[i + 1]),
      is_closure_head: closureHeads.has(row.tokens[i + 1]),
      is_target_390: row.tokens[i + 1] === '390',
      text: row.text,
    };
    frame.left_tags = tagFrame(frame);
    frame.target_390_read = frame.is_target_390 ? target390Read(frame) : '';
    frames.push(frame);
  }
}

const tagNames = ['final235', 'final032_no235', 'contains032_no235', 'final004', 'contains004', 'other_left'];

function summarizeTag(tag) {
  const rows = frames.filter((frame) => frame.left_tags.includes(tag));
  const p086Rows = rows.filter((frame) => frame.is_p086_head);
  const closureRows = rows.filter((frame) => frame.is_closure_head);
  const target390Rows = rows.filter((frame) => frame.is_target_390);
  const has125 = rows.filter((frame) => frame.has_125_in_branch_or_tail);
  const p086Has125 = p086Rows.filter((frame) => frame.has_125_in_branch_or_tail);
  const closureHas125 = closureRows.filter((frame) => frame.has_125_in_branch_or_tail);
  const targetHas125 = target390Rows.filter((frame) => frame.has_125_in_branch_or_tail);
  const terminal = rows.filter((frame) => frame.terminal_after_branch);
  return {
    checked_date: checkedDate,
    tag,
    frames: String(rows.length),
    has_125: String(has125.length),
    has_125_share: safeShare(has125.length, rows.length),
    p086_frames: String(p086Rows.length),
    p086_has_125: String(p086Has125.length),
    p086_has_125_share: safeShare(p086Has125.length, p086Rows.length),
    closure_frames: String(closureRows.length),
    closure_has_125: String(closureHas125.length),
    closure_has_125_share: safeShare(closureHas125.length, closureRows.length),
    terminal_frames: String(terminal.length),
    terminal_share: safeShare(terminal.length, rows.length),
    target_390_frames: String(target390Rows.length),
    target_390_has_125: String(targetHas125.length),
    target_390_has_125_share: safeShare(targetHas125.length, target390Rows.length),
    heads: topCounts(rows, (frame) => frame.head),
    branches: topCounts(rows, (frame) => frame.branch),
    target_390_branches: topCounts(target390Rows, (frame) => frame.branch),
    target_390_reads: topCounts(target390Rows, (frame) => frame.target_390_read),
    examples: exampleRows(rows),
  };
}

const summaries = tagNames.map(summarizeTag);

const targetRows = frames
  .filter((frame) => frame.is_target_390)
  .map((frame) => ({
    checked_date: checkedDate,
    cisi: frame.cisi,
    row_id: frame.row_id,
    site: frame.site,
    type: frame.type,
    shape: frame.shape,
    left: frame.left,
    left_final: frame.left_final,
    left_tags: frame.left_tags.join(';'),
    head: frame.head,
    branch: frame.branch,
    tail: frame.tail,
    terminal_after_branch: String(frame.terminal_after_branch),
    has_125_in_branch_or_tail: String(frame.has_125_in_branch_or_tail),
    target_390_read: frame.target_390_read,
    text: frame.text,
  }));

function numeric(row, key) {
  return row[key] === 'NA' ? 0 : Number(row[key]);
}

const final235 = summaries.find((row) => row.tag === 'final235');
const final032 = summaries.find((row) => row.tag === 'final032_no235');
const contains032 = summaries.find((row) => row.tag === 'contains032_no235');
const final004 = summaries.find((row) => row.tag === 'final004');

const final235P086Works = numeric(final235, 'p086_frames') > 0 && numeric(final235, 'p086_has_125_share') === 1;
const final235ClosureClean = numeric(final235, 'closure_frames') > 0 && numeric(final235, 'closure_has_125_share') === 0;
const final032TargetNo125 = numeric(final032, 'target_390_frames') > 0 && numeric(final032, 'target_390_has_125_share') === 0;
const contains032TargetNo125 =
  numeric(contains032, 'target_390_frames') > 0 && numeric(contains032, 'target_390_has_125_share') === 0;
const final004Mixed =
  numeric(final004, 'target_390_frames') >= 2 && final004.target_390_branches.includes('095') && final004.target_390_branches.includes('125');

let decision = 'mixed_left_context_operator_model';
let confidenceTier = 'wild shot';
if (final235P086Works && final235ClosureClean && final032TargetNo125 && contains032TargetNo125 && final004Mixed) {
  decision = 'candidate_local_left_context_operator_model';
  confidenceTier = 'candidate';
} else if (final235P086Works && final032TargetNo125) {
  decision = 'wild_partial_left_context_operator_model';
}

const decisions = [
  {
    checked_date: checkedDate,
    bet_id: 'V10_LEFT_CONTEXT_OPERATORS_20260531',
    confidence_tier: confidenceTier,
    decision,
    risky_parse_bet:
      'The left side before `002-390-X` contributes operator-like context: final `235` plus P086 head selects `125`, `032` without `235` biases toward boundary/formula/result closure, and final `004` is a neutral qualifier that can split into status closure or rank continuation.',
    what_would_promote:
      'Held-out `002-390-X` rows preserve these left-trigger behaviors, especially `235-002-390/405 -> 125` and `032`-bearing no-`235` rows avoiding `125`.',
    what_would_break:
      '`235-002-390/405` rows lack `125`, or `032` no-`235` rows commonly select `125`/rank tails, or `004` becomes a direct selector rather than a split qualifier.',
  },
];

const summary = {
  checked_date: checkedDate,
  status: 'left_context_operator_discriminator',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: canonicalRows.length,
    governed_frames: frames.length,
    target_002_390_frames: targetRows.length,
  },
  tag_summary: summaries
    .map(
      (row) =>
        `${row.tag}:${row.frames}_frames:${row.target_390_frames}_target390:${row.has_125}/${row.frames}_has125:${row.p086_has_125}/${row.p086_frames}_p086has125`,
    )
    .join(';'),
  local_conditions: {
    final235_p086_all_has_125: final235P086Works,
    final235_closure_has_no_125: final235ClosureClean,
    final032_target390_has_no_125: final032TargetNo125,
    contains032_target390_has_no_125: contains032TargetNo125,
    final004_target390_mixed_095_125: final004Mixed,
  },
  decisions: decisions.map((row) => `${row.bet_id}:${row.decision}`).join(';'),
};

writeCsv(path.join(reportsDir, `${prefix}_tag_summary.csv`), summaries, [
  'checked_date',
  'tag',
  'frames',
  'has_125',
  'has_125_share',
  'p086_frames',
  'p086_has_125',
  'p086_has_125_share',
  'closure_frames',
  'closure_has_125',
  'closure_has_125_share',
  'terminal_frames',
  'terminal_share',
  'target_390_frames',
  'target_390_has_125',
  'target_390_has_125_share',
  'heads',
  'branches',
  'target_390_branches',
  'target_390_reads',
  'examples',
]);

writeCsv(path.join(reportsDir, `${prefix}_target_390_rows.csv`), targetRows, [
  'checked_date',
  'cisi',
  'row_id',
  'site',
  'type',
  'shape',
  'left',
  'left_final',
  'left_tags',
  'head',
  'branch',
  'tail',
  'terminal_after_branch',
  'has_125_in_branch_or_tail',
  'target_390_read',
  'text',
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
