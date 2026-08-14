import fs from 'node:fs';
import path from 'node:path';

// When we see 002-390-X, is the X chosen by the governed frame, or did the writer simply
// copy an ordinary 390-X pair that exists all over the corpus? This discriminator settles
// it sign by sign. It reads data/open_prototype/lipi/metadata_filtered.csv, dedupes to
// canonical sequences, and collects every 390-X pair, split by whether a 002 immediately
// precedes the 390. For each X that occurs in the governed frame it compares governed
// versus outside counts, terminal shares, and tail profiles, then classifies the X:
// governed_only_selector (never occurs outside), governed_weighted_selector,
// inherited_formula_pressure (outside rows dominate and repeat one tail — 590 is the
// predicted case), or background_collocation_pressure. The overall bet — 002-390-X is a
// governed branch table, not raw 390 inheritance — is promoted to candidate only if at
// least 70 percent of non-590 X values are selector-like with at most one inherited-formula
// case. Writes the branch table, governed pair rows, and the decision as CSVs plus a
// summary JSON in reports/.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_390x_inheritance_discriminator_20260531';
const checkedDate = '2026-05-31';

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

function safeShare(num, den) {
  return den ? (num / den).toFixed(6) : 'NA';
}

function formatExamples(rows, n = 8) {
  return rows
    .slice(0, n)
    .map((row) => `${row.cisi}:${row.text}`)
    .join(' | ');
}

fs.mkdirSync(reportsDir, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  tokens: signs(row.text),
}));
const canonicalRows = [...new Map(rawRows.map((row) => [row.tokens.join(' '), row])).values()];

const pairRows = [];
const targetRows = [];
for (const row of canonicalRows) {
  for (let i = 0; i < row.tokens.length - 1; i += 1) {
    if (row.tokens[i] !== '390') continue;
    const x = row.tokens[i + 1];
    const isPost002 = row.tokens[i - 1] === '002';
    const tail = row.tokens.slice(i + 2);
    const record = {
      checked_date: checkedDate,
      cisi: objectId(row),
      row_id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      x,
      is_post_002: isPost002,
      tail_after_x: tail.join(' ') || '<END>',
      tail_length_after_x: tail.length,
      terminal_after_x: tail.length === 0,
      left_before_390: row.tokens.slice(0, i).join(' ') || '<START>',
      text: row.text,
    };
    pairRows.push(record);
    if (isPost002) targetRows.push(record);
  }
}

const targetXs = [...new Set(targetRows.map((row) => row.x))].sort();

function classify(row) {
  const target = Number(row.target_pair_count);
  const outside = Number(row.non002_pair_count);
  const all = Number(row.global_390x_pair_count);
  const outsideTopShare = row.non002_top_tail_share === 'NA' ? 0 : Number(row.non002_top_tail_share);
  if (outside === 0) return 'governed_only_selector';
  if (target >= outside) return 'governed_weighted_selector';
  if (outsideTopShare >= 0.5 && outside >= 5) return 'inherited_formula_pressure';
  if (outside > target) return 'background_collocation_pressure';
  if (all) return 'mixed';
  return 'missing';
}

const branchRows = targetXs.map((x) => {
  const target = targetRows.filter((row) => row.x === x);
  const global = pairRows.filter((row) => row.x === x);
  const outside = global.filter((row) => !row.is_post_002);
  const outsideTailCounts = countBy(outside, (row) => row.tail_after_x);
  const outsideTopTail = outsideTailCounts[0]?.[0] ?? '';
  const outsideTopTailN = outsideTailCounts[0]?.[1] ?? 0;
  const row = {
    checked_date: checkedDate,
    x,
    target_pair_count: String(target.length),
    global_390x_pair_count: String(global.length),
    non002_pair_count: String(outside.length),
    target_share_of_global_390x: safeShare(target.length, global.length),
    target_terminal_after_x: String(target.filter((item) => item.terminal_after_x).length),
    target_terminal_share: safeShare(target.filter((item) => item.terminal_after_x).length, target.length),
    non002_terminal_after_x: String(outside.filter((item) => item.terminal_after_x).length),
    non002_terminal_share: safeShare(outside.filter((item) => item.terminal_after_x).length, outside.length),
    target_sites: topCounts(target, (item) => item.site),
    non002_sites: topCounts(outside, (item) => item.site),
    target_tails: topCounts(target, (item) => item.tail_after_x),
    non002_tails: topCounts(outside, (item) => item.tail_after_x),
    non002_top_tail: outsideTopTail,
    non002_top_tail_share: safeShare(outsideTopTailN, outside.length),
    target_examples: formatExamples(target),
    non002_examples: formatExamples(outside),
    classification: '',
  };
  row.classification = classify(row);
  return row;
});

const governedOnly = branchRows.filter((row) => row.classification === 'governed_only_selector').length;
const governedWeighted = branchRows.filter((row) => row.classification === 'governed_weighted_selector').length;
const inheritedFormula = branchRows.filter((row) => row.classification === 'inherited_formula_pressure').length;
const backgroundPressure = branchRows.filter((row) => row.classification === 'background_collocation_pressure').length;
const selectorLike = governedOnly + governedWeighted;
const selectorLikeWithout590 = branchRows.filter(
  (row) => row.x !== '590' && ['governed_only_selector', 'governed_weighted_selector'].includes(row.classification),
).length;
const non590Rows = branchRows.filter((row) => row.x !== '590').length;

let decision = 'mixed_branch_table';
let confidenceTier = 'wild shot';
if (selectorLikeWithout590 >= Math.ceil(non590Rows * 0.7) && inheritedFormula <= 1) {
  decision = 'candidate_branch_table_not_raw_390_inheritance';
  confidenceTier = 'candidate';
} else if (backgroundPressure + inheritedFormula >= selectorLike) {
  decision = 'demote_to_raw_390_inheritance';
}

const decisions = [
  {
    checked_date: checkedDate,
    bet_id: 'V7_002_390_X_NOT_RAW_390_INHERITANCE_20260531',
    confidence_tier: confidenceTier,
    decision,
    risky_parse_bet:
      '`002-390-X` is a governed branch table; most X values are selected in the `002-390` frame rather than inherited from ordinary raw `390-X` collocations. `590` is the predicted exception.',
    what_would_promote:
      'New source-visible `002-390-X` rows use selector-only or governed-weighted X values while inherited `390-590-032` remains the main exception.',
    what_would_break:
      'Most `002-390-X` branches show strong non-002 `390-X` background collocations with the same tails, making the branch table copied raw `390` formulae.',
  },
];

const summary = {
  checked_date: checkedDate,
  status: '390x_inheritance_discriminator',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: canonicalRows.length,
    all_390x_pairs: pairRows.length,
    post_002_390x_pairs: targetRows.length,
    target_x_values: targetXs.length,
  },
  x_classifications: branchRows.map((row) => `${row.x}:${row.classification}`).join(';'),
  selector_like_x_values: selectorLike,
  selector_like_without_590: `${selectorLikeWithout590}/${non590Rows}`,
  inherited_formula_x_values: inheritedFormula,
  background_pressure_x_values: backgroundPressure,
  decisions: decisions.map((row) => `${row.bet_id}:${row.decision}`).join(';'),
};

writeCsv(path.join(reportsDir, `${prefix}_branch_table.csv`), branchRows, [
  'checked_date',
  'x',
  'target_pair_count',
  'global_390x_pair_count',
  'non002_pair_count',
  'target_share_of_global_390x',
  'target_terminal_after_x',
  'target_terminal_share',
  'non002_terminal_after_x',
  'non002_terminal_share',
  'target_sites',
  'non002_sites',
  'target_tails',
  'non002_tails',
  'non002_top_tail',
  'non002_top_tail_share',
  'classification',
  'target_examples',
  'non002_examples',
]);

writeCsv(path.join(reportsDir, `${prefix}_target_pairs.csv`), targetRows, [
  'checked_date',
  'cisi',
  'row_id',
  'site',
  'type',
  'shape',
  'x',
  'is_post_002',
  'tail_after_x',
  'tail_length_after_x',
  'terminal_after_x',
  'left_before_390',
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
