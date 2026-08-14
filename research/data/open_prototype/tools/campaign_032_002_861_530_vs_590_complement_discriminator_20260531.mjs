// Head-to-head discriminator: is sign 530 special as a "complement linker", or does sign 590
// behave the same way? A complement linker here means a branch sign in a governed frame
// (002 + head + branch + tail) that always takes exactly one following complement sign, and
// that complement is always closure-like — a sign that tends to end things elsewhere.
// We read the filtered Indus inscription list (lipi/metadata_filtered.csv), keep one copy of
// each distinct sign sequence, extract every governed frame, and build the same profile for
// both branches: one-complement share, closure-like complement share, head/site spread.
// If 530 passes the linker test and 590 fails, 530 is a specific linker; if both pass, we
// must generalize to a linker class; if 530 fails, the bet dies. Writes branch summaries,
// per-row complement classes, a lookup table, and a decision CSV plus a JSON summary to
// data/open_prototype/reports.
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_530_vs_590_complement_discriminator_20260531';
const checkedDate = '2026-05-31';
const targetBranches = ['530', '590'];

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

function terminalClass(row) {
  const branchRows = Number(row.branch_rows);
  const branchTerminalShare = row.branch_terminal_share === 'NA' ? 0 : Number(row.branch_terminal_share);
  const headRows = Number(row.head_rows);
  const headTerminalShare = row.head_terminal_share === 'NA' ? 0 : Number(row.head_terminal_share);
  const globalTerminalShare = Number(row.global_terminal_share);
  if (branchRows >= 2 && branchTerminalShare >= 0.75) return 'branch_terminal_class';
  if (headRows >= 1 && headTerminalShare >= 0.75) return 'head_terminal_class';
  if (globalTerminalShare >= 0.5) return 'global_terminal_tendency';
  return 'not_terminal_class';
}

function formatExamples(rows) {
  return rows.map((row) => `${row.cisi}:${row.text}`).join(' | ');
}

fs.mkdirSync(reportsDir, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  tokens: signs(row.text),
}));
const canonicalRows = [...new Map(rawRows.map((row) => [row.tokens.join(' '), row])).values()];

const signOccurrences = [];
const governedFrames = [];
for (const row of canonicalRows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
    signOccurrences.push({
      sign: row.tokens[i],
      terminal: i === row.tokens.length - 1,
      cisi: objectId(row),
      site: row.site,
      type: row.type,
      text: row.text,
    });
    if (row.tokens[i] !== '002' || !row.tokens[i + 1] || !row.tokens[i + 2]) continue;
    const tail = row.tokens.slice(i + 3);
    governedFrames.push({
      checked_date: checkedDate,
      cisi: objectId(row),
      row_id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      head: row.tokens[i + 1],
      branch: row.tokens[i + 2],
      tail: tail.join(' ') || '<END>',
      tail_length: tail.length,
      first_tail: tail[0] ?? '<END>',
      terminal_after_branch: tail.length === 0,
      text: row.text,
    });
  }
}

function complementClass(sign) {
  const global = signOccurrences.filter((row) => row.sign === sign);
  const branch = governedFrames.filter((row) => row.branch === sign);
  const head = governedFrames.filter((row) => row.head === sign);
  const row = {
    checked_date: checkedDate,
    complement: sign,
    global_rows: String(global.length),
    global_terminal: String(global.filter((item) => item.terminal).length),
    global_terminal_share: safeShare(global.filter((item) => item.terminal).length, global.length),
    branch_rows: String(branch.length),
    branch_terminal: String(branch.filter((item) => item.terminal_after_branch).length),
    branch_terminal_share: safeShare(branch.filter((item) => item.terminal_after_branch).length, branch.length),
    branch_heads: topCounts(branch, (item) => item.head),
    head_rows: String(head.length),
    head_terminal: String(head.filter((item) => item.terminal_after_branch).length),
    head_terminal_share: safeShare(head.filter((item) => item.terminal_after_branch).length, head.length),
    head_branches: topCounts(head, (item) => item.branch),
    classification: '',
  };
  row.classification = terminalClass(row);
  return row;
}

const branchRows = targetBranches.flatMap((branch) =>
  governedFrames.filter((row) => row.branch === branch).map((row) => ({
    ...row,
    target_branch: branch,
  })),
);

const oneComplementRows = branchRows.filter((row) => row.tail_length === 1);
const complementSigns = [...new Set(oneComplementRows.map((row) => row.first_tail))].sort();
const complementLookup = new Map(complementSigns.map((sign) => [sign, complementClass(sign)]));

const complementRows = oneComplementRows.map((row) => ({
  checked_date: checkedDate,
  source_branch: row.branch,
  complement: row.first_tail,
  cisi: row.cisi,
  site: row.site,
  type: row.type,
  head: row.head,
  tail: row.tail,
  text: row.text,
  classification: complementLookup.get(row.first_tail).classification,
  global_terminal_share: complementLookup.get(row.first_tail).global_terminal_share,
  branch_rows: complementLookup.get(row.first_tail).branch_rows,
  branch_terminal_share: complementLookup.get(row.first_tail).branch_terminal_share,
  head_rows: complementLookup.get(row.first_tail).head_rows,
  head_terminal_share: complementLookup.get(row.first_tail).head_terminal_share,
}));

function branchStats(branch) {
  const rows = governedFrames.filter((row) => row.branch === branch);
  const oneRows = rows.filter((row) => row.tail_length === 1);
  const closureRows = oneRows.filter((row) => complementLookup.get(row.first_tail)?.classification !== 'not_terminal_class');
  const branchTerminalRows = oneRows.filter(
    (row) => complementLookup.get(row.first_tail)?.classification === 'branch_terminal_class',
  );
  return {
    checked_date: checkedDate,
    branch,
    frames: String(rows.length),
    terminal_frames: String(rows.filter((row) => row.tail_length === 0).length),
    one_complement_frames: String(oneRows.length),
    longer_frames: String(rows.filter((row) => row.tail_length > 1).length),
    one_complement_share: safeShare(oneRows.length, rows.length),
    closure_like_one_complements: String(closureRows.length),
    closure_like_one_complement_share: safeShare(closureRows.length, oneRows.length),
    branch_terminal_one_complements: String(branchTerminalRows.length),
    branch_terminal_one_complement_share: safeShare(branchTerminalRows.length, oneRows.length),
    distinct_heads: String(new Set(rows.map((row) => row.head)).size),
    distinct_sites: String(new Set(rows.map((row) => row.site)).size),
    distinct_first_tails: String(new Set(rows.map((row) => row.first_tail)).size),
    heads: topCounts(rows, (row) => row.head),
    sites: topCounts(rows, (row) => row.site),
    first_tails: topCounts(rows, (row) => row.first_tail),
    complement_classes: topCounts(
      oneRows,
      (row) => complementLookup.get(row.first_tail)?.classification ?? 'not_terminal_class',
    ),
    examples: formatExamples(rows),
  };
}

const branchSummary = targetBranches.map(branchStats);
const branchBySign = new Map(branchSummary.map((row) => [row.branch, row]));
const row530 = branchBySign.get('530');
const row590 = branchBySign.get('590');

const row530IsLinker =
  Number(row530.one_complement_share) === 1 && Number(row530.closure_like_one_complement_share) === 1;
const row590MatchesLinker =
  Number(row590.one_complement_share) === 1 && Number(row590.closure_like_one_complement_share) === 1;

let decision = 'ambiguous';
let confidenceTier = 'wild shot';
if (row530IsLinker && !row590MatchesLinker) {
  decision = 'candidate_530_specific_complement_linker_not_590';
  confidenceTier = 'candidate';
} else if (row530IsLinker && row590MatchesLinker) {
  decision = 'generalize_to_530_590_complement_linker_class';
  confidenceTier = 'candidate';
} else if (!row530IsLinker) {
  decision = 'demote_530_complement_linker';
}

const decisions = [
  {
    checked_date: checkedDate,
    bet_id: 'V5_530_BEATS_590_AS_COMPLEMENT_LINKER_20260531',
    confidence_tier: confidenceTier,
    decision,
    risky_parse_bet:
      '`530` is a governed one-complement closure-linker, while `590` is a looser bridge/branch and should fail the same discriminator.',
    what_would_promote:
      'More `530` rows keep one closure-like complement while `590` keeps showing terminal frames, multi-shape behavior, or non-closure complements.',
    what_would_break:
      '`590` also becomes all one-complement with closure-like complements, forcing a generalized branch class, or `530` gains terminal/open complement exceptions.',
  },
];

const summary = {
  checked_date: checkedDate,
  status: '530_vs_590_complement_discriminator',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: canonicalRows.length,
    governed_frames: governedFrames.length,
  },
  branch_summary: branchSummary.map((row) =>
    [
      row.branch,
      `${row.one_complement_frames}/${row.frames}_one_complement`,
      `${row.closure_like_one_complements}/${row.one_complement_frames}_closure_like`,
      `${row.terminal_frames}/${row.frames}_terminal`,
    ].join(':'),
  ).join(';'),
  complement_classes: complementRows
    .map((row) => `${row.source_branch}-${row.complement}:${row.classification}`)
    .join(';'),
  decisions: decisions.map((row) => `${row.bet_id}:${row.decision}`).join(';'),
};

writeCsv(path.join(reportsDir, `${prefix}_branch_summary.csv`), branchSummary, [
  'checked_date',
  'branch',
  'frames',
  'terminal_frames',
  'one_complement_frames',
  'longer_frames',
  'one_complement_share',
  'closure_like_one_complements',
  'closure_like_one_complement_share',
  'branch_terminal_one_complements',
  'branch_terminal_one_complement_share',
  'distinct_heads',
  'distinct_sites',
  'distinct_first_tails',
  'heads',
  'sites',
  'first_tails',
  'complement_classes',
  'examples',
]);

writeCsv(path.join(reportsDir, `${prefix}_one_complement_rows.csv`), complementRows, [
  'checked_date',
  'source_branch',
  'complement',
  'cisi',
  'site',
  'type',
  'head',
  'tail',
  'text',
  'classification',
  'global_terminal_share',
  'branch_rows',
  'branch_terminal_share',
  'head_rows',
  'head_terminal_share',
]);

writeCsv(path.join(reportsDir, `${prefix}_complement_class_lookup.csv`), [...complementLookup.values()], [
  'checked_date',
  'complement',
  'global_rows',
  'global_terminal',
  'global_terminal_share',
  'branch_rows',
  'branch_terminal',
  'branch_terminal_share',
  'branch_heads',
  'head_rows',
  'head_terminal',
  'head_terminal_share',
  'head_branches',
  'classification',
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
