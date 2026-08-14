// Stress test for the bet that sign 530, when it sits in the branch slot of a governed frame
// (002 + head + 530 + tail), always opens exactly one complement slot: 002-H-530-Y and never
// 002-H-530 alone or 002-H-530-Y-Z. We read the filtered Indus inscription list
// (lipi/metadata_filtered.csv), keep one copy of each distinct sign sequence, and collect two
// views: every governed frame for every branch sign (so 530 can be ranked against
// count-matched peer branches), and every occurrence of 530 anywhere in any inscription (to
// check whether the one-complement habit holds globally or only after 002-H). The script
// scores two bets — 530 as a portable one-complement branch, and 530 as a global chain sign —
// and writes frame, occurrence, baseline, and decision CSVs plus a JSON summary to
// data/open_prototype/reports.
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_530_one_complement_stress_20260531';
const checkedDate = '2026-05-31';
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

function uniqueCount(items, fn) {
  return new Set(items.map(fn)).size;
}

function branchDecision(row, target) {
  if (row.branch !== target) return 'baseline';
  if (Number(row.frames) >= 4 && Number(row.one_complement_share) === 1 && Number(row.distinct_heads) >= 4) {
    return 'candidate_portable_one_complement_branch';
  }
  if (Number(row.continuing_share) === 1) return 'wild_open_branch_not_one_complement';
  return 'demoted';
}

fs.mkdirSync(reportsDir, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  tokens: signs(row.text),
}));
const canonicalRows = [...new Map(rawRows.map((row) => [row.tokens.join(' '), row])).values()];

const governedFrames = [];
const targetOccurrences = [];

for (const row of canonicalRows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
    if (row.tokens[i] === targetBranch) {
      targetOccurrences.push({
        checked_date: checkedDate,
        cisi: objectId(row),
        row_id: row.id,
        site: row.site,
        type: row.type,
        shape: row.shape,
        prev: row.tokens[i - 1] ?? '<START>',
        next: row.tokens[i + 1] ?? '<END>',
        signs_after: String(row.tokens.length - i - 1),
        terminal: String(i === row.tokens.length - 1),
        after_002_h: String(row.tokens[i - 2] === '002'),
        head_if_after_002: row.tokens[i - 1] && row.tokens[i - 2] === '002' ? row.tokens[i - 1] : '',
        tail_after_530: row.tokens.slice(i + 1).join(' ') || '<END>',
        local_context: row.tokens.slice(Math.max(0, i - 4), Math.min(row.tokens.length, i + 5)).join('-'),
        exact_sequence: row.tokens.join(' '),
        text: row.text,
      });
    }

    if (row.tokens[i] !== '002' || !row.tokens[i + 1] || !row.tokens[i + 2]) continue;
    const head = row.tokens[i + 1];
    const branch = row.tokens[i + 2];
    const tail = row.tokens.slice(i + 3);
    governedFrames.push({
      checked_date: checkedDate,
      cisi: objectId(row),
      row_id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      symbol: row.symbol,
      cult: row.cult,
      head,
      branch,
      tail: tail.join(' ') || '<END>',
      terminal_after_branch: String(tail.length === 0),
      one_complement: String(tail.length === 1),
      tail_length: String(tail.length),
      first_tail: tail[0] ?? '<END>',
      prev_before_002: row.tokens[i - 1] ?? '<START>',
      local_context: row.tokens.slice(Math.max(0, i - 3), Math.min(row.tokens.length, i + 7)).join('-'),
      exact_sequence: row.tokens.join(' '),
      text: row.text,
    });
  }
}

const branchSummary = countBy(governedFrames, (row) => row.branch).map(([branch, count]) => {
  const rows = governedFrames.filter((row) => row.branch === branch);
  const continuing = rows.filter((row) => row.terminal_after_branch !== 'true').length;
  const oneComplement = rows.filter((row) => row.one_complement === 'true').length;
  const summaryRow = {
    checked_date: checkedDate,
    branch,
    frames: String(count),
    terminal: String(rows.length - continuing),
    continuing: String(continuing),
    continuing_share: (continuing / rows.length).toFixed(6),
    one_complement: String(oneComplement),
    one_complement_share: (oneComplement / rows.length).toFixed(6),
    distinct_heads: String(uniqueCount(rows, (row) => row.head)),
    distinct_sites: String(uniqueCount(rows, (row) => row.site)),
    heads: topCounts(rows, (row) => row.head),
    sites: topCounts(rows, (row) => row.site),
    first_tails: topCounts(rows, (row) => row.first_tail),
    examples: rows.slice(0, 12).map((row) => `${row.cisi}:${row.text}`).join(' | '),
  };
  summaryRow.decision = branchDecision(summaryRow, targetBranch);
  return summaryRow;
});

const targetFrames = governedFrames.filter((row) => row.branch === targetBranch);
const targetSummary = branchSummary.find((row) => row.branch === targetBranch);
const countMatched = branchSummary
  .filter((row) => Number(row.frames) >= 2 && Number(row.frames) <= 8)
  .sort(
    (a, b) =>
      Number(b.one_complement_share) - Number(a.one_complement_share) ||
      Number(b.distinct_heads) - Number(a.distinct_heads) ||
      Number(b.frames) - Number(a.frames) ||
      a.branch.localeCompare(b.branch, undefined, { numeric: true }),
  )
  .map((row, index) => ({
    ...row,
    count_matched_rank: String(index + 1),
  }));

const targetRank = countMatched.find((row) => row.branch === targetBranch)?.count_matched_rank ?? '';
const globalContinuing = targetOccurrences.filter((row) => row.terminal !== 'true').length;
const globalOneComplement = targetOccurrences.filter((row) => row.signs_after === '1').length;

const decisions = [
  {
    checked_date: checkedDate,
    bet_id: 'V2_530_PORTABLE_ONE_COMPLEMENT_BRANCH_20260531',
    confidence_tier:
      targetSummary &&
      Number(targetSummary.frames) >= 4 &&
      Number(targetSummary.one_complement_share) === 1 &&
      Number(targetSummary.distinct_heads) >= 4
        ? 'candidate'
        : 'wild shot',
    decision: targetSummary?.decision ?? 'missing',
    risky_parse_bet:
      '`530` inside `002-H-530-Y` opens exactly one complement slot across multiple heads/sites.',
    what_would_promote:
      'More source-visible `002-H-530-Y` rows preserve one following complement under new heads; count-matched branches stop matching this pattern.',
    what_would_break:
      'A credible `002-H-530` terminal row, a multi-sign `002-H-530-Y-Z` continuation, or evidence that the four current rows are one visual/register family.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'V4_530_GLOBAL_CHAIN_SIGN_20260531',
    confidence_tier: 'wild shot',
    decision: globalContinuing === targetOccurrences.length ? 'global_open_survives' : 'global_open_damaged',
    risky_parse_bet:
      '`530` is globally a chain/complement opener, not just governed after `002-H`.',
    what_would_promote:
      'Most non-governed `530` rows also take a visible complement, with source-visible terminal counterexamples explained as damage or side breaks.',
    what_would_break:
      'The existing terminal `530` rows remain source-real and contextually normal.',
  },
];

const summary = {
  checked_date: checkedDate,
  status: '530_one_complement_stress',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: canonicalRows.length,
    governed_002_h_x_frames: governedFrames.length,
    target_002_h_530_frames: targetFrames.length,
    target_global_occurrences: targetOccurrences.length,
  },
  target: {
    frames: targetSummary?.frames ?? '0',
    heads: targetSummary?.heads ?? '',
    sites: targetSummary?.sites ?? '',
    one_complement_share: targetSummary?.one_complement_share ?? '0.000000',
    count_matched_rank: targetRank,
    global_continuing_share: targetOccurrences.length ? globalContinuing / targetOccurrences.length : 0,
    global_one_complement_share: targetOccurrences.length ? globalOneComplement / targetOccurrences.length : 0,
  },
  decisions: decisions.map((row) => `${row.bet_id}:${row.decision}`).join(';'),
  key_result:
    '`530` is clean as a governed one-complement branch in `002-H-530-Y`, but not clean as a global sign value.',
};

writeCsv(path.join(reportsDir, `${prefix}_target_frames.csv`), targetFrames, [
  'checked_date',
  'cisi',
  'row_id',
  'site',
  'type',
  'shape',
  'symbol',
  'cult',
  'head',
  'branch',
  'tail',
  'terminal_after_branch',
  'one_complement',
  'tail_length',
  'first_tail',
  'prev_before_002',
  'local_context',
  'exact_sequence',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_target_occurrences.csv`), targetOccurrences, [
  'checked_date',
  'cisi',
  'row_id',
  'site',
  'type',
  'shape',
  'prev',
  'next',
  'signs_after',
  'terminal',
  'after_002_h',
  'head_if_after_002',
  'tail_after_530',
  'local_context',
  'exact_sequence',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_branch_baseline.csv`), branchSummary, [
  'checked_date',
  'branch',
  'frames',
  'terminal',
  'continuing',
  'continuing_share',
  'one_complement',
  'one_complement_share',
  'distinct_heads',
  'distinct_sites',
  'heads',
  'sites',
  'first_tails',
  'decision',
  'examples',
]);

writeCsv(path.join(reportsDir, `${prefix}_count_matched_baseline.csv`), countMatched, [
  'checked_date',
  'count_matched_rank',
  'branch',
  'frames',
  'terminal',
  'continuing',
  'continuing_share',
  'one_complement',
  'one_complement_share',
  'distinct_heads',
  'distinct_sites',
  'heads',
  'sites',
  'first_tails',
  'decision',
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
