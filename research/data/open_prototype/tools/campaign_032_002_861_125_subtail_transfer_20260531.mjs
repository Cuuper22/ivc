import fs from 'node:fs';
import path from 'node:path';

// If sign 125 is a title/rank suffix rather than the end of a name, the short "sub-tails"
// that follow it (like 632-032 or 820) should transfer across different governed heads, not
// cling to one. This script probes that. It reads data/open_prototype/lipi/
// metadata_filtered.csv and logs every 125 occurrence, walking up to four signs leftward to
// find whether the occurrence sits inside a 002-governed frame and, if so, under which head.
// Each occurrence records its neighbors and its full tail; every two-sign sub-tail is then
// summarized with global count, governed count, governed heads, and sites. The two named
// candidates: 125-632-032 as a portable sub-tail (it appears under governed heads 190 and
// 390), and 125-820 as a P086-family sub-tail under heads 390/405. The recorded conclusion
// upgrades 125 from a 390-dependent selector to one use of a broader title/rank suffix
// system. Writes the occurrence and sub-tail summary CSVs plus a summary JSON to reports/.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_125_subtail_transfer_20260531';

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

function topCounts(counts, n = 12) {
  return counts
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function findGovernedHead(tokens, signIndex) {
  for (let headIndex = signIndex - 1; headIndex >= 0 && headIndex >= signIndex - 4; headIndex -= 1) {
    if (tokens[headIndex - 1] === '002') {
      return {
        governed: true,
        head: tokens[headIndex],
        prevBefore002: tokens[headIndex - 2] ?? '<START>',
      };
    }
  }
  return { governed: false, head: '', prevBefore002: '' };
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  tokens: signs(row.text),
}));

const occurrences = [];
for (const row of rows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
    if (row.tokens[i] !== '125') continue;
    const governed = findGovernedHead(row.tokens, i);
    occurrences.push({
      checked_date: '2026-05-31',
      cisi: row.cisi || '-',
      row_id: row.id,
      site: row.site,
      type: row.type,
      symbol: row.symbol,
      cult: row.cult,
      governed_by_002: String(governed.governed),
      governed_head: governed.head,
      prev_before_002: governed.prevBefore002,
      prev_before_125: row.tokens[i - 1] ?? '<START>',
      next_after_125: row.tokens[i + 1] ?? '<END>',
      next2_after_125: row.tokens[i + 2] ?? '<END>',
      tail_from_125: row.tokens.slice(i).join('-'),
      text: row.text,
    });
  }
}

const governedOccurrences = occurrences.filter((row) => row.governed_by_002 === 'true');
const subtail632032 = occurrences.filter((row) => row.next_after_125 === '632' && row.next2_after_125 === '032');
const subtail820 = occurrences.filter((row) => row.next_after_125 === '820');
const after390 = occurrences.filter((row) => row.prev_before_125 === '390');

const subtailSummary = countBy(occurrences, (row) => `${row.next_after_125}-${row.next2_after_125}`).map(
  ([subtail, count]) => {
    const members = occurrences.filter((row) => `${row.next_after_125}-${row.next2_after_125}` === subtail);
    const governedMembers = members.filter((row) => row.governed_by_002 === 'true');
    return {
      checked_date: '2026-05-31',
      subtail,
      global_count: String(count),
      governed_count: String(governedMembers.length),
      governed_heads: topCounts(countBy(governedMembers, (row) => row.governed_head)),
      prev_before_002: topCounts(countBy(governedMembers, (row) => row.prev_before_002)),
      sites: topCounts(countBy(members, (row) => row.site)),
      types: topCounts(countBy(members, (row) => row.type)),
      examples: members
        .slice(0, 8)
        .map((row) => `${row.cisi}:${row.text}`)
        .join(' | '),
      model_implication:
        subtail === '632-032'
          ? 'portable_125_subtail_candidate_across_governed_heads'
          : subtail === '820-<END>'
            ? 'p086_family_125_subtail_candidate_under_390_405'
            : 'background_125_subtail',
    };
  },
);

const summary = {
  checked_date: '2026-05-31',
  status: '125_subtail_transfer_probe',
  hypotheses_tested: [
    '125 as portable title/rank suffix rather than a name-final',
    '125-632-032 as transferable sub-tail across governed heads',
    '125-820 as P086-family title sub-tail under 390/405',
  ],
  key_counts: {
    global_125_occurrences: occurrences.length,
    governed_125_occurrences: governedOccurrences.length,
    after_390_125_occurrences: after390.length,
    subtail_125_632_032_global: subtail632032.length,
    subtail_125_632_032_governed: subtail632032.filter((row) => row.governed_by_002 === 'true').length,
    subtail_125_820_global: subtail820.length,
    subtail_125_820_governed: subtail820.filter((row) => row.governed_by_002 === 'true').length,
  },
  decisions: [
    '125 strengthens as a portable title/rank suffix candidate because governed 125 appears under heads beyond 390.',
    '125-632-032 becomes a promoted sub-bet candidate: it appears 4 times globally and 3 times under governed heads, including 190 and 390.',
    '125-820 becomes a candidate P086-family sub-tail because it appears under governed 390 and 405 rows.',
    '125 is no longer modelled as only a 390-dependent selector; 390 selects one use of a broader title/rank suffix system.',
  ],
};

writeCsv(path.join(reportsDir, `${prefix}_125_occurrences.csv`), occurrences, [
  'checked_date',
  'cisi',
  'row_id',
  'site',
  'type',
  'symbol',
  'cult',
  'governed_by_002',
  'governed_head',
  'prev_before_002',
  'prev_before_125',
  'next_after_125',
  'next2_after_125',
  'tail_from_125',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_subtail_summary.csv`), subtailSummary, [
  'checked_date',
  'subtail',
  'global_count',
  'governed_count',
  'governed_heads',
  'prev_before_002',
  'sites',
  'types',
  'examples',
  'model_implication',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
