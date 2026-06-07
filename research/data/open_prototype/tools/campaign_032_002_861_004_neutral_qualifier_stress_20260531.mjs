import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const BRANCH_FRAMES = path.join(
  ROOT,
  'data',
  'open_prototype',
  'reports',
  'risky_002390_canonical_branch_selector_forger_20260531_frames.csv',
);
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'campaign_032_002_861_004_neutral_qualifier_stress_20260531';
const RUN_DATE = '2026-05-31';

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

function csvEscape(value) {
  const text = String(value ?? '');
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(',')];
  for (const row of rows) lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function countBy(items, fn) {
  const counts = new Map();
  for (const item of items) {
    const key = fn(item);
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()].sort(
    (a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }),
  );
}

function top(counts, n = 8) {
  return counts
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function entropy(counts) {
  const total = counts.reduce((sum, [, value]) => sum + value, 0);
  if (!total) return 0;
  return counts.reduce((sum, [, value]) => {
    const p = value / total;
    return sum - p * Math.log2(p);
  }, 0);
}

function frameClass(frame) {
  if (frame.prev_before_002 === '004' && frame.head_after_002 === '390') return '004_002_390_split';
  if (frame.prev_before_002 === '004') return '004_002_other';
  if (frame.head_after_002 === '390') return 'non004_002_390';
  return 'background';
}

fs.mkdirSync(OUT_DIR, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));
const rows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()];
const sourceBranchRows = parseCsv(fs.readFileSync(BRANCH_FRAMES, 'utf8'));
const sourceStatusByObjectBranch = new Map(
  sourceBranchRows.map((row) => [`${row.object}|${row.branch}`, row.source_status]),
);
const sourceBucketByObjectBranch = new Map(
  sourceBranchRows.map((row) => [`${row.object}|${row.branch}`, row.source_bucket]),
);

const frames = [];
for (const row of rows) {
  row.signs.forEach((sign, idx) => {
    if (sign !== '002' || !row.signs[idx + 1]) return;
    const head = row.signs[idx + 1];
    const branch = row.signs[idx + 2] ?? '<END>';
    const tailAfterBranch = row.signs.slice(idx + 3).join(' ') || '<END>';
    const prev = row.signs[idx - 1] ?? '<START>';
    const prev2 = row.signs.slice(Math.max(0, idx - 2), idx).join(' ') || '<START>';
    const object = row.object;
    const key = `${object}|${branch}`;
    const terminalAfterHead = branch === '<END>';
    frames.push({
      checked_date: RUN_DATE,
      row_id: row.id,
      object,
      site: row.site || 'NA',
      type: row.type || 'NA',
      symbol: row.symbol || 'NA',
      cult: row.cult || 'NA',
      prev_before_002: prev,
      prev2_before_002: prev2,
      head_after_002: head,
      branch_after_head: branch,
      tail_after_branch: tailAfterBranch,
      terminal_after_head: terminalAfterHead ? 'true' : 'false',
      local_frame_class: '',
      source_status: sourceStatusByObjectBranch.get(key) ?? 'metadata_or_unrouted',
      source_bucket: sourceBucketByObjectBranch.get(key) ?? 'metadata_or_unrouted',
      exact_text: row.text,
    });
  });
}

for (const frame of frames) frame.local_frame_class = frameClass(frame);

const prev004Frames = frames.filter((frame) => frame.prev_before_002 === '004');
const prev004Head390 = prev004Frames.filter((frame) => frame.head_after_002 === '390');
const exact390004002 = frames.filter((frame) => frame.prev2_before_002 === '390 004');
const non004Head390 = frames.filter((frame) => frame.head_after_002 === '390' && frame.prev_before_002 !== '004');

const prevRows = [...new Set(frames.map((frame) => frame.prev_before_002))]
  .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }))
  .map((prev) => {
    const group = frames.filter((frame) => frame.prev_before_002 === prev);
    const headCounts = countBy(group, (frame) => frame.head_after_002);
    const branchCounts = countBy(group, (frame) => `${frame.head_after_002}-${frame.branch_after_head}`);
    const exactCounts = countBy(group, (frame) => frame.exact_text);
    const terminal = group.filter((frame) => frame.terminal_after_head === 'true').length;
    return {
      checked_date: RUN_DATE,
      prev_before_002: prev,
      rows: String(group.length),
      terminal_after_head: String(terminal),
      terminal_share: (terminal / group.length).toFixed(6),
      head_count: String(headCounts.length),
      head_entropy_bits: entropy(headCounts).toFixed(6),
      top_head_share: (headCounts[0][1] / group.length).toFixed(6),
      top_heads: top(headCounts),
      branch_count: String(branchCounts.length),
      top_branches: top(branchCounts),
      exact_text_count: String(exactCounts.length),
      top_exact_text_share: (exactCounts[0][1] / group.length).toFixed(6),
      top_exact_texts: top(exactCounts, 4),
    };
  });

const familyRows = [
  {
    checked_date: RUN_DATE,
    family: '004-002-all',
    rows: String(prev004Frames.length),
    terminal_after_head: String(prev004Frames.filter((frame) => frame.terminal_after_head === 'true').length),
    head_count: String(new Set(prev004Frames.map((frame) => frame.head_after_002)).size),
    branch_count: String(new Set(prev004Frames.map((frame) => `${frame.head_after_002}-${frame.branch_after_head}`)).size),
    top_heads: top(countBy(prev004Frames, (frame) => frame.head_after_002)),
    top_branches: top(countBy(prev004Frames, (frame) => `${frame.head_after_002}-${frame.branch_after_head}`)),
    implication:
      '`004` before `002` is compatible with multiple heads and outcomes; it is not a direct `X` selector by itself.',
  },
  {
    checked_date: RUN_DATE,
    family: '004-002-390',
    rows: String(prev004Head390.length),
    terminal_after_head: String(prev004Head390.filter((frame) => frame.terminal_after_head === 'true').length),
    head_count: '1',
    branch_count: String(new Set(prev004Head390.map((frame) => frame.branch_after_head)).size),
    top_heads: top(countBy(prev004Head390, (frame) => frame.head_after_002)),
    top_branches: top(countBy(prev004Head390, (frame) => `${frame.head_after_002}-${frame.branch_after_head}`)),
    implication:
      '`004-002-390` splits into `095` closure and `125-820` continuation, so `004` is not determining the branch sign under `390`.',
  },
  {
    checked_date: RUN_DATE,
    family: '390-004-002-exact-prefix',
    rows: String(exact390004002.length),
    terminal_after_head: String(exact390004002.filter((frame) => frame.terminal_after_head === 'true').length),
    head_count: String(new Set(exact390004002.map((frame) => frame.head_after_002)).size),
    branch_count: String(new Set(exact390004002.map((frame) => `${frame.head_after_002}-${frame.branch_after_head}`)).size),
    top_heads: top(countBy(exact390004002, (frame) => frame.head_after_002)),
    top_branches: top(countBy(exact390004002, (frame) => `${frame.head_after_002}-${frame.branch_after_head}`)),
    implication:
      'The exact `390-004-002` prefix is closure-heavy but branch-diverse; copied-prefix pressure remains, but it does not collapse to one tail.',
  },
  {
    checked_date: RUN_DATE,
    family: 'non004-002-390',
    rows: String(non004Head390.length),
    terminal_after_head: String(non004Head390.filter((frame) => frame.terminal_after_head === 'true').length),
    head_count: '1',
    branch_count: String(new Set(non004Head390.map((frame) => frame.branch_after_head)).size),
    top_heads: top(countBy(non004Head390, (frame) => frame.head_after_002)),
    top_branches: top(countBy(non004Head390, (frame) => `${frame.head_after_002}-${frame.branch_after_head}`)),
    implication:
      'Non-`004` `002-390` rows are also branch-diverse; selector choice is not reducible to `004`.',
  },
];

const decisionRows = [
  {
    checked_date: RUN_DATE,
    named_bet: '`004` is a neutral qualifier before `002`, not the selector of `X`',
    tier_after_test: 'candidate_mixed',
    evidence:
      '`004-002` has multiple heads; the exact `004-002-390` pair splits into `095` terminal closure (H-1993) and `125-820` continuation (Sktd-1).',
    adversary:
      '`004-002` is closure-heavy and exact-prefix `390-004-002` has formula pressure, so neutral does not mean free or semantically solved.',
    falsifier_or_rescue:
      'A source-bound failure of H-1993 or Sktd-1 kills the clean `004-002-390` split; a third sourced `004-002-390` branch with a new X strengthens neutrality.',
  },
  {
    checked_date: RUN_DATE,
    named_bet: '`004` directly selects `125` under `002-390`',
    tier_after_test: 'dead',
    evidence:
      'Same immediate predecessor `004` and same head `390` produce both `095` and `125`; selector choice cannot be assigned to `004` alone.',
    adversary:
      'Sktd-1 is only route-pressure/panel-order weak, so this death is model-level, not accepted source fact.',
    falsifier_or_rescue:
      'If Sktd-1 is source-rejected and H-1993 source-binds as the only clean `004-002-390` row, the direct-selector bet becomes underdetermined rather than dead.',
  },
  {
    checked_date: RUN_DATE,
    named_bet: '`390-004-002` is a copied prefix that determines closure',
    tier_after_test: 'wild_shot_demoted',
    evidence:
      'The exact prefix is closure-heavy but still branches into `817`, `820`, `861`, `390-125-820`, `031-376`, and `705-127` in canonical rows.',
    adversary:
      'Several rows are metadata-only or source-limited, and `817` dominates, so formula-prefix pressure remains a live adversary.',
    falsifier_or_rescue:
      'Source-normalized collapse to one copied `390-004-002-817` family would revive copied-prefix closure; source-preserved branch diversity kills it.',
  },
];

const summary = {
  checked_date: RUN_DATE,
  status: '004_neutral_qualifier_stress',
  hypothesis_tested:
    '`004` before `002` is a neutral qualifier that permits head/branch choice rather than directly selecting the `002-390-X` branch.',
  totals: {
    all_002_frames: frames.length,
    prev004_frames: prev004Frames.length,
    prev004_002390_frames: prev004Head390.length,
    exact_390004002_frames: exact390004002.length,
  },
  key_rows: prev004Head390.map((frame) => ({
    object: frame.object,
    text: frame.exact_text,
    branch_after_head: frame.branch_after_head,
    tail_after_branch: frame.tail_after_branch,
    terminal_after_head: frame.terminal_after_head,
    source_status: frame.source_status,
  })),
  family_rows: familyRows,
  decisions: decisionRows,
  confidence_after_test: {
    '004_neutral_qualifier': 'candidate_mixed',
    '004_selects_125_under_390': 'dead',
    '390004002_copied_prefix_closure': 'wild_shot_demoted',
  },
};

writeCsv(path.join(OUT_DIR, `${PREFIX}_frames.csv`), frames, [
  'checked_date',
  'row_id',
  'object',
  'site',
  'type',
  'symbol',
  'cult',
  'prev_before_002',
  'prev2_before_002',
  'head_after_002',
  'branch_after_head',
  'tail_after_branch',
  'terminal_after_head',
  'local_frame_class',
  'source_status',
  'source_bucket',
  'exact_text',
]);

writeCsv(path.join(OUT_DIR, `${PREFIX}_prev_summary.csv`), prevRows, [
  'checked_date',
  'prev_before_002',
  'rows',
  'terminal_after_head',
  'terminal_share',
  'head_count',
  'head_entropy_bits',
  'top_head_share',
  'top_heads',
  'branch_count',
  'top_branches',
  'exact_text_count',
  'top_exact_text_share',
  'top_exact_texts',
]);

writeCsv(path.join(OUT_DIR, `${PREFIX}_families.csv`), familyRows, [
  'checked_date',
  'family',
  'rows',
  'terminal_after_head',
  'head_count',
  'branch_count',
  'top_heads',
  'top_branches',
  'implication',
]);

writeCsv(path.join(OUT_DIR, `${PREFIX}_decisions.csv`), decisionRows, [
  'checked_date',
  'named_bet',
  'tier_after_test',
  'evidence',
  'adversary',
  'falsifier_or_rescue',
]);

fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
