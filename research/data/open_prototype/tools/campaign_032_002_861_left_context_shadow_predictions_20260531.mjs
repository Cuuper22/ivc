import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_left_context_shadow_predictions_20260531';
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

function groupBy(items, fn) {
  const groups = new Map();
  for (const item of items) {
    const key = fn(item);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(item);
  }
  return groups;
}

function tailOf(tokens, n) {
  if (!tokens.length) return '<START>';
  return tokens.slice(Math.max(0, tokens.length - n)).join(' ');
}

function exampleRows(rows, n = 10) {
  return rows
    .slice(0, n)
    .map((row) => `${row.cisi}:${row.left_final}-002-${row.head}-${row.branch}-${row.tail}`)
    .join(' | ');
}

function classifyTarget(frame) {
  if (frame.left_final === '235' && p086Heads.has(frame.head) && frame.has_125) return 'predict_rank_title';
  if (frame.left_tokens.includes('032') && !frame.left_tokens.includes('235') && !frame.has_125) {
    return 'predict_boundary_formula_result';
  }
  if (frame.left_final === '004') return 'predict_neutral_qualifier_split';
  return 'unpredicted_by_current_left_model';
}

function shadowSupport(target, rows, level) {
  const shadows = rows.filter((row) => row.row_key !== target.row_key);
  if (!shadows.length) return 'no_shadow';

  if (target.left_final === '235' && target.has_125 && p086Heads.has(target.head)) {
    const p086Bad = shadows.filter((row) => p086Heads.has(row.head) && !row.has_125);
    const closureGood = shadows.filter((row) => closureHeads.has(row.head) && !row.has_125);
    const nonP086Good = shadows.filter((row) => !p086Heads.has(row.head) && !row.has_125);
    if (p086Bad.length) return `breaks_rank_trigger_at_${level}`;
    if (closureGood.length || nonP086Good.length) return `supports_rank_trigger_head_switch_at_${level}`;
    return `uninformative_rank_shadow_at_${level}`;
  }

  if (target.left_tokens.includes('032') && !target.left_tokens.includes('235') && !target.has_125) {
    const bad125 = shadows.filter((row) => row.has_125);
    if (bad125.length) return `breaks_032_suppression_at_${level}`;
    return `supports_032_no125_context_at_${level}`;
  }

  if (target.left_final === '004') {
    const branchKinds = new Set(shadows.map((row) => (row.has_125 ? 'rank' : row.branch)));
    if (branchKinds.size > 0) return `supports_004_neutral_shadow_at_${level}`;
    return `uninformative_004_shadow_at_${level}`;
  }

  return `untyped_shadow_at_${level}`;
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
      row_key: `${row.id}:${i}`,
      site: row.site,
      type: row.type,
      shape: row.shape,
      left_tokens: leftTokens,
      left: leftTokens.join(' ') || '<START>',
      left_final: leftTokens.at(-1) ?? '<START>',
      left_suffix_2: tailOf(leftTokens, 2),
      left_suffix_3: tailOf(leftTokens, 3),
      head: row.tokens[i + 1],
      branch: row.tokens[i + 2],
      tail: tail.join(' ') || '<END>',
      terminal_after_branch: tail.length === 0,
      has_125: row.tokens[i + 2] === '125' || tail.includes('125'),
      text: row.text,
    };
    frame.left_prediction = frame.head === '390' ? classifyTarget(frame) : '';
    frames.push(frame);
  }
}

const exactGroups = groupBy(frames, (row) => row.left);
const suffix3Groups = groupBy(frames, (row) => row.left_suffix_3);
const suffix2Groups = groupBy(frames, (row) => row.left_suffix_2);
const target390 = frames.filter((row) => row.head === '390');

const shadowRows = [];
for (const target of target390) {
  const levels = [
    ['exact_left', target.left, exactGroups.get(target.left) ?? []],
    ['suffix3_left', target.left_suffix_3, suffix3Groups.get(target.left_suffix_3) ?? []],
    ['suffix2_left', target.left_suffix_2, suffix2Groups.get(target.left_suffix_2) ?? []],
  ];
  for (const [level, key, rows] of levels) {
    const shadows = rows.filter((row) => row.row_key !== target.row_key);
    shadowRows.push({
      checked_date: checkedDate,
      target_cisi: target.cisi,
      target_text: target.text,
      target_left: target.left,
      target_head: target.head,
      target_branch: target.branch,
      target_tail: target.tail,
      target_prediction: target.left_prediction,
      shadow_level: level,
      shadow_key: key,
      shadow_count: String(shadows.length),
      shadow_heads: topCounts(shadows, (row) => row.head),
      shadow_branches: topCounts(shadows, (row) => row.branch),
      shadow_has_125: String(shadows.filter((row) => row.has_125).length),
      shadow_terminal: String(shadows.filter((row) => row.terminal_after_branch).length),
      support_call: shadowSupport(target, rows, level),
      shadow_examples: exampleRows(shadows),
    });
  }
}

const exactDuplicateGroups = [...exactGroups.entries()]
  .filter(([, rows]) => rows.length > 1)
  .map(([left, rows]) => ({
    checked_date: checkedDate,
    left,
    frames: String(rows.length),
    heads: topCounts(rows, (row) => row.head),
    branches: topCounts(rows, (row) => row.branch),
    has_125: String(rows.filter((row) => row.has_125).length),
    terminal: String(rows.filter((row) => row.terminal_after_branch).length),
    p086_has_125: String(rows.filter((row) => p086Heads.has(row.head) && row.has_125).length),
    closure_has_125: String(rows.filter((row) => closureHeads.has(row.head) && row.has_125).length),
    examples: exampleRows(rows),
  }));

const supportCounts = countBy(shadowRows, (row) => row.support_call);
const exactRankSupport = shadowRows.some((row) => row.support_call === 'supports_rank_trigger_head_switch_at_exact_left');
const exactRankBreak = shadowRows.some((row) => row.support_call === 'breaks_rank_trigger_at_exact_left');
const suffix032Break = shadowRows.some((row) => row.support_call.startsWith('breaks_032_suppression'));
const exact004Support = shadowRows.some((row) => row.support_call === 'supports_004_neutral_shadow_at_exact_left');

let decision = 'mixed_shadow_support_for_left_context';
let confidenceTier = 'wild shot';
if (exactRankSupport && !exactRankBreak && !suffix032Break) {
  decision = 'candidate_left_context_operator_shadow_support';
  confidenceTier = 'candidate';
} else if (exactRankBreak || suffix032Break) {
  decision = 'demote_left_context_operator_model';
}

const decisions = [
  {
    checked_date: checkedDate,
    bet_id: 'V11_LEFT_CONTEXT_SHADOW_PREDICTIONS_20260531',
    confidence_tier: confidenceTier,
    decision,
    risky_parse_bet:
      'Exact or near left-context shadows should support compositional parsing: the same final `235` left material can switch from closure under non-P086 heads to `125` rank/title under P086 heads, while `032` without `235` should keep suppressing `125`.',
    what_would_promote:
      'More exact-left shadows show P086 heads selecting `125` and closure/non-P086 heads avoiding it, while `032` no-`235` shadows continue avoiding rank tails.',
    what_would_break:
      'Exact-left P086 shadows without `125`, or `032` no-`235` shadows with repeated `125` rank tails, would collapse the left-context operator model.',
  },
];

const summary = {
  checked_date: checkedDate,
  status: 'left_context_shadow_predictions',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: canonicalRows.length,
    governed_frames: frames.length,
    target_002_390_frames: target390.length,
    exact_duplicate_left_groups: exactDuplicateGroups.length,
  },
  support_counts: Object.fromEntries(supportCounts),
  exact_rank_support: exactRankSupport,
  exact_rank_break: exactRankBreak,
  suffix_032_break: suffix032Break,
  exact_004_support: exact004Support,
  decisions: decisions.map((row) => `${row.bet_id}:${row.decision}`).join(';'),
};

writeCsv(path.join(reportsDir, `${prefix}_shadow_rows.csv`), shadowRows, [
  'checked_date',
  'target_cisi',
  'target_text',
  'target_left',
  'target_head',
  'target_branch',
  'target_tail',
  'target_prediction',
  'shadow_level',
  'shadow_key',
  'shadow_count',
  'shadow_heads',
  'shadow_branches',
  'shadow_has_125',
  'shadow_terminal',
  'support_call',
  'shadow_examples',
]);

writeCsv(path.join(reportsDir, `${prefix}_exact_duplicate_left_groups.csv`), exactDuplicateGroups, [
  'checked_date',
  'left',
  'frames',
  'heads',
  'branches',
  'has_125',
  'terminal',
  'p086_has_125',
  'closure_has_125',
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
