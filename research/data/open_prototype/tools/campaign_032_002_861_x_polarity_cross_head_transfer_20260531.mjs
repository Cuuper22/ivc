import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_x_polarity_cross_head_transfer_20260531';
const checkedDate = '2026-05-31';

const branchClass = new Map([
  ['125', 'open_continue'],
  ['530', 'open_continue'],
  ['590', 'open_continue'],
  ['072', 'close_terminal'],
  ['095', 'close_terminal'],
  ['140', 'close_terminal'],
  ['346', 'close_terminal'],
  ['692', 'close_terminal'],
  ['705', 'close_terminal'],
  ['707', 'close_terminal'],
]);

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

function hitFor(branch, terminal) {
  const predicted = branchClass.get(branch);
  if (predicted === 'open_continue') return !terminal;
  if (predicted === 'close_terminal') return terminal;
  return false;
}

function decisionForBranch(branch, non390Rows) {
  if (!non390Rows.length) return 'no_cross_head_evidence';
  const hits = non390Rows.filter((row) => row.hit === 'true').length;
  const share = hits / non390Rows.length;
  if (non390Rows.length >= 3 && share >= 0.8) return 'supports_portable_slot_polarity';
  if (non390Rows.length >= 3 && share <= 0.5) return 'damages_portable_slot_polarity';
  if (share === 1) return 'weak_support_singleton_or_pair';
  if (share === 0) return 'weak_counterexample_singleton_or_pair';
  return 'mixed_cross_head_evidence';
}

function globalDecision(summaryRows) {
  const tested = summaryRows.filter((row) => Number(row.non390_rows) > 0);
  const rows = tested.reduce((sum, row) => sum + Number(row.non390_rows), 0);
  const hits = tested.reduce((sum, row) => sum + Number(row.non390_hits), 0);
  const damaged = tested.filter((row) => row.decision.includes('damages') || row.decision.includes('counterexample')).length;
  if (!rows) return 'no_cross_head_test';
  const share = hits / rows;
  if (share >= 0.75 && damaged === 0) return 'portable_slot_polarity_candidate';
  if (share >= 0.6) return 'portable_slot_polarity_wild_mixed';
  return 'head_specific_390_table_preferred';
}

fs.mkdirSync(reportsDir, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  tokens: signs(row.text),
}));
const canonicalRows = [...new Map(rawRows.map((row) => [row.tokens.join(' '), row])).values()];

const frameRows = [];
for (const row of canonicalRows) {
  for (let i = 0; i < row.tokens.length - 2; i += 1) {
    if (row.tokens[i] !== '002') continue;
    const head = row.tokens[i + 1];
    const branch = row.tokens[i + 2];
    if (!branchClass.has(branch)) continue;
    const tail = row.tokens.slice(i + 3);
    const terminal = tail.length === 0;
    frameRows.push({
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
      predicted_class: branchClass.get(branch),
      tail: tail.join(' ') || '<END>',
      terminal: String(terminal),
      hit: String(hitFor(branch, terminal)),
      is_390_head: String(head === '390'),
      prev_before_002: row.tokens[i - 1] ?? '<START>',
      local_context: row.tokens.slice(Math.max(0, i - 3), Math.min(row.tokens.length, i + 7)).join('-'),
      exact_sequence: row.tokens.join(' '),
      text: row.text,
    });
  }
}

const branchRows = [...branchClass.keys()].map((branch) => {
  const rows = frameRows.filter((row) => row.branch === branch);
  const target = rows.filter((row) => row.is_390_head === 'true');
  const non390 = rows.filter((row) => row.is_390_head !== 'true');
  const non390Hits = non390.filter((row) => row.hit === 'true').length;
  return {
    checked_date: checkedDate,
    branch,
    predicted_class: branchClass.get(branch),
    all_002_h_x_rows: String(rows.length),
    target_390_rows: String(target.length),
    non390_rows: String(non390.length),
    non390_hits: String(non390Hits),
    non390_hit_share: non390.length ? (non390Hits / non390.length).toFixed(6) : '0.000000',
    non390_heads: topCounts(non390, (row) => row.head),
    non390_terminal: String(non390.filter((row) => row.terminal === 'true').length),
    non390_continuing: String(non390.filter((row) => row.terminal !== 'true').length),
    decision: decisionForBranch(branch, non390),
    examples: non390.slice(0, 16).map((row) => `${row.cisi}:${row.text}`).join(' | '),
  };
});

const non390Rows = frameRows.filter((row) => row.is_390_head !== 'true');
const non390Hits = non390Rows.filter((row) => row.hit === 'true').length;
const openNon390 = non390Rows.filter((row) => row.predicted_class === 'open_continue');
const closedNon390 = non390Rows.filter((row) => row.predicted_class === 'close_terminal');

const decisions = [
  {
    checked_date: checkedDate,
    bet_id: 'V2_X_POLARITY_PORTABLE_ACROSS_002_HEADS_20260531',
    confidence_tier: globalDecision(branchRows) === 'portable_slot_polarity_candidate' ? 'candidate' : 'wild shot',
    decision: globalDecision(branchRows),
    risky_parse_bet:
      'The open/closed value of a target branch sign transfers across `002-H-X` heads, not only inside `002-390-X`.',
    what_would_promote:
      'More non-390 `002-H-X` rows preserve open branches as continuing and closed branches as terminal, especially for repeated signs.',
    what_would_break:
      'Repeated non-390 rows for `125/530/590` ending immediately, or `095/692/705` continuing productively after other heads.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'V2_002390_HEAD_SPECIFIC_BRANCH_TABLE_20260531',
    confidence_tier: globalDecision(branchRows) === 'head_specific_390_table_preferred' ? 'candidate' : 'wild shot',
    decision: globalDecision(branchRows) === 'head_specific_390_table_preferred'
      ? 'candidate_head_specific_table'
      : 'retained_as_local_candidate_not_global',
    risky_parse_bet:
      '`002-390-X` has a local head-specific branch table; other `002-H-X` heads may reuse the same signs with different polarity.',
    what_would_promote:
      'Non-390 target-branch rows repeatedly violate the `002-390` open/closed polarity while the 390 table stays intact.',
    what_would_break:
      'Clean cross-head transfer of the same polarity under multiple non-390 heads.',
  },
];

const summary = {
  checked_date: checkedDate,
  status: 'x_polarity_cross_head_transfer',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: canonicalRows.length,
    target_branch_frames: frameRows.length,
    non390_target_branch_frames: non390Rows.length,
  },
  non390_hit_share: non390Rows.length ? non390Hits / non390Rows.length : 0,
  open_non390_hit_share: openNon390.length
    ? openNon390.filter((row) => row.hit === 'true').length / openNon390.length
    : null,
  closed_non390_hit_share: closedNon390.length
    ? closedNon390.filter((row) => row.hit === 'true').length / closedNon390.length
    : null,
  decisions: decisions.map((row) => `${row.bet_id}:${row.decision}`).join(';'),
  key_result:
    'This tests whether `125/530/590` and `072/095/140/346/692/705/707` carry polarity across heads, or whether `390` owns the table.',
};

writeCsv(path.join(reportsDir, `${prefix}_frame_rows.csv`), frameRows, [
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
  'predicted_class',
  'tail',
  'terminal',
  'hit',
  'is_390_head',
  'prev_before_002',
  'local_context',
  'exact_sequence',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_branch_summary.csv`), branchRows, [
  'checked_date',
  'branch',
  'predicted_class',
  'all_002_h_x_rows',
  'target_390_rows',
  'non390_rows',
  'non390_hits',
  'non390_hit_share',
  'non390_heads',
  'non390_terminal',
  'non390_continuing',
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
