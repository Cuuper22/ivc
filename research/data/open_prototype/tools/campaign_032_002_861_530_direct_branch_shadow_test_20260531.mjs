// Shadow test for sign 530: if a frame reads 002-H-530-Y, could Y just as well attach
// directly to the head H as 002-H-Y? If such "direct shadows" exist, 530 is only an optional
// separator; if they never occur, 530 genuinely introduces a nested complement layer.
// We read the filtered Indus inscription list (lipi/metadata_filtered.csv), keep one copy of
// each distinct sign sequence, and extract every governed frame (002 + head + branch + tail).
// For each 530 frame with a one-sign tail we count same-head frames where the complement Y
// appears as the branch itself, plus context counts for the head and the complement.
// Outputs: a per-target shadow CSV, a decision CSV, and a JSON summary in
// data/open_prototype/reports.
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_530_direct_branch_shadow_test_20260531';
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

function topCounts(items, fn, n = 12) {
  return countBy(items, fn)
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
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

const governedFrames = [];
for (const row of canonicalRows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
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
      text: row.text,
    });
  }
}

const targetRows = governedFrames.filter((row) => row.branch === '530' && row.tail_length === 1);

const shadowRows = targetRows.map((row) => {
  const directShadow = governedFrames.filter((candidate) => candidate.head === row.head && candidate.branch === row.first_tail);
  const sameHeadRows = governedFrames.filter((candidate) => candidate.head === row.head);
  const complementAsBranch = governedFrames.filter((candidate) => candidate.branch === row.first_tail);
  return {
    checked_date: checkedDate,
    cisi: row.cisi,
    site: row.site,
    type: row.type,
    head: row.head,
    branch: row.branch,
    complement: row.first_tail,
    text: row.text,
    direct_shadow_count: String(directShadow.length),
    direct_shadow_examples: formatExamples(directShadow),
    same_head_frames: String(sameHeadRows.length),
    same_head_branches: topCounts(sameHeadRows, (candidate) => candidate.branch),
    complement_as_branch_frames: String(complementAsBranch.length),
    complement_as_branch_heads: topCounts(complementAsBranch, (candidate) => candidate.head),
  };
});

const directShadowTargets = shadowRows.filter((row) => Number(row.direct_shadow_count) > 0).length;
const decision =
  directShadowTargets === 0
    ? 'candidate_530_introduces_non_direct_complement_layer'
    : directShadowTargets < shadowRows.length
      ? 'mixed_530_optional_or_partial_complement_layer'
      : 'demote_530_linker_to_optional_separator';
const confidenceTier = decision.startsWith('candidate') ? 'candidate' : 'wild shot';

const decisions = [
  {
    checked_date: checkedDate,
    bet_id: 'V6_530_NON_DIRECT_COMPLEMENT_LAYER_20260531',
    confidence_tier: confidenceTier,
    decision,
    risky_parse_bet:
      '`530` introduces a nested complement layer; its Y signs should not simply be direct `002-H-Y` alternatives for the same H.',
    what_would_promote:
      'Additional `002-H-530-Y` rows lack same-head direct `002-H-Y` shadows while Y remains closure-like elsewhere.',
    what_would_break:
      'Same-head direct `002-H-Y` rows become common for the current complements, making `530` an optional separator or copied register mark.',
  },
];

const summary = {
  checked_date: checkedDate,
  status: '530_direct_branch_shadow_test',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: canonicalRows.length,
    governed_frames: governedFrames.length,
    target_530_rows: targetRows.length,
  },
  direct_shadow_targets: `${directShadowTargets}/${shadowRows.length}`,
  shadows: shadowRows.map((row) => `${row.head}-530-${row.complement}:${row.direct_shadow_count}`).join(';'),
  decisions: decisions.map((row) => `${row.bet_id}:${row.decision}`).join(';'),
};

writeCsv(path.join(reportsDir, `${prefix}_target_shadows.csv`), shadowRows, [
  'checked_date',
  'cisi',
  'site',
  'type',
  'head',
  'branch',
  'complement',
  'text',
  'direct_shadow_count',
  'direct_shadow_examples',
  'same_head_frames',
  'same_head_branches',
  'complement_as_branch_frames',
  'complement_as_branch_heads',
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
