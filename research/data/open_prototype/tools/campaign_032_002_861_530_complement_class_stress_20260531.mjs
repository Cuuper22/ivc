import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_530_complement_class_stress_20260531';
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

const targetRows = governedFrames.filter((row) => row.branch === targetBranch && row.tail_length === 1);
const complementSigns = [...new Set(targetRows.map((row) => row.first_tail))].sort();

const complementRows = complementSigns.map((sign) => {
  const global = signOccurrences.filter((row) => row.sign === sign);
  const branch = governedFrames.filter((row) => row.branch === sign);
  const head = governedFrames.filter((row) => row.head === sign);
  const row = {
    checked_date: checkedDate,
    complement: sign,
    target_530_rows: String(targetRows.filter((target) => target.first_tail === sign).length),
    target_heads: topCounts(targetRows.filter((target) => target.first_tail === sign), (target) => target.head),
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
    examples: targetRows.filter((target) => target.first_tail === sign).map((target) => `${target.cisi}:${target.text}`).join(' | '),
  };
  row.classification = terminalClass(row);
  return row;
});

const allBranchSigns = countBy(governedFrames, (row) => row.branch).map(([branch, n]) => {
  const rows = governedFrames.filter((row) => row.branch === branch);
  return {
    branch,
    n,
    terminalShare: rows.filter((row) => row.terminal_after_branch).length / rows.length,
  };
});

const allHeadSigns = countBy(governedFrames, (row) => row.head).map(([head, n]) => {
  const rows = governedFrames.filter((row) => row.head === head);
  return {
    head,
    n,
    terminalShare: rows.filter((row) => row.terminal_after_branch).length / rows.length,
  };
});

const complementSet = new Set(complementSigns);
const complementHits = complementRows.filter((row) => row.classification !== 'not_terminal_class').length;
const branchClassComplements = complementRows.filter((row) => row.classification === 'branch_terminal_class').length;

const exactDenominator = countBy(governedFrames, (row) => row.branch).filter(([, n]) => n >= 2).length;
const exactBranchClass = allBranchSigns.filter((row) => row.n >= 2 && row.terminalShare >= 0.75).length;
const branchClassRate = exactDenominator ? exactBranchClass / exactDenominator : 0;

const complementClassDecision =
  complementHits === complementRows.length && branchClassComplements >= 3
    ? 'candidate_closure_like_complement_class'
    : complementHits === complementRows.length
      ? 'wild_closure_like_complement_class'
      : 'mixed_complement_class';

const decisions = [
  {
    checked_date: checkedDate,
    bet_id: 'V3_530_SELECTS_CLOSURE_LIKE_COMPLEMENTS_20260531',
    confidence_tier: complementClassDecision.startsWith('candidate') ? 'candidate' : 'wild shot',
    decision: complementClassDecision,
    risky_parse_bet:
      '`530` selects a one-sign complement from a closure-like class, rather than arbitrary one-sign material.',
    what_would_promote:
      'New `002-H-530-Y` complements also classify as terminal branches/heads, while random one-sign complements do not.',
    what_would_break:
      'A new `002-H-530-Y` complement is productive/open in both branch and head roles, or current complement signs prove terminal only by copy/damage.',
  },
];

const summary = {
  checked_date: checkedDate,
  status: '530_complement_class_stress',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: canonicalRows.length,
    governed_frames: governedFrames.length,
    target_530_one_complement_rows: targetRows.length,
  },
  complement_signs: complementSigns.join(';'),
  complement_classifications: complementRows.map((row) => `${row.complement}:${row.classification}`).join(';'),
  closure_like_complements: complementHits,
  branch_terminal_complements: branchClassComplements,
  branch_terminal_class_background_rate: branchClassRate,
  decisions: decisions.map((row) => `${row.bet_id}:${row.decision}`).join(';'),
  caveat:
    '`904` is closure-like by head behavior (`002-904-346` terminal), not by branch behavior; that makes the complement-class bet narrower than the one-complement bet.',
};

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
  'tail_length',
  'first_tail',
  'terminal_after_branch',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_complements.csv`), complementRows, [
  'checked_date',
  'complement',
  'target_530_rows',
  'target_heads',
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
