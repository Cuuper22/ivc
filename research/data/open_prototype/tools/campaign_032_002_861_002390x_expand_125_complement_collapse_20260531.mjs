import fs from 'node:fs';
import path from 'node:path';

// If 125 in the X slot is a linker, what does it link to — and do those
// complements hold up, or collapse into one copied formula? This script scans
// lipi/metadata_filtered.csv for every 002-HEAD-125 occurrence and sorts each
// one into a lane by the sign right after the 125: the 632-032 lane, the 032
// lane, the 820 lane, terminal 125 (an exception to the linker model), or a
// singleton lane. For each lane it counts occurrences, distinct sites, and
// distinct heads, then assigns a collapse risk: a repeated lane confined to
// one site is flagged "site_local_formula_risk". The recorded read: 632-032
// is Mohenjo-daro formula risk, while the smaller 032 and 820 lanes cross
// local formula boundaries and give the linker claim real support. Writes
// occurrence, lane, and bet CSVs plus a summary JSON to
// data/open_prototype/reports.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_125_complement_collapse_20260531';
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

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function tokens(text) {
  return text.match(/\d{3}/g) ?? [];
}

function tally(values) {
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([value, count]) => `${value}:${count}`)
    .join(';');
}

function uniqueCount(values) {
  return new Set(values).size;
}

function laneFor(next1, tail) {
  if (next1 === '<END>') return 'terminal_125';
  if (next1 === '632' && tail.startsWith('632-032')) return '632_032_lane';
  if (next1 === '032') return '032_lane';
  if (next1 === '820') return '820_lane';
  return `${next1}_singleton_lane`;
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));

const x125Rows = [];
for (const row of rows) {
  for (let i = 0; i < row.signs.length - 2; i += 1) {
    if (row.signs[i] !== '002') continue;
    const head = row.signs[i + 1];
    const x = row.signs[i + 2];
    if (x !== '125') continue;
    const next1 = row.signs[i + 3] ?? '<END>';
    const tail = row.signs.slice(i + 3).join('-') || '<END>';
    x125Rows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      condition: row.condition,
      complete: row.complete,
      head,
      x,
      next1,
      tail,
      lane: laneFor(next1, tail),
      terminal: next1 === '<END>',
      text: row.text,
    });
  }
}

const laneRows = [...new Set(x125Rows.map((row) => row.lane))]
  .map((lane) => {
    const laneMembers = x125Rows.filter((row) => row.lane === lane);
    const siteCount = uniqueCount(laneMembers.map((row) => row.site));
    const headCount = uniqueCount(laneMembers.map((row) => row.head));
    return {
      checked_date: checkedDate,
      lane,
      occurrences: laneMembers.length,
      sites: tally(laneMembers.map((row) => row.site)),
      site_count: siteCount,
      heads: tally(laneMembers.map((row) => row.head)),
      head_count: headCount,
      types: tally(laneMembers.map((row) => row.type)),
      objects: laneMembers.map((row) => row.object).join(';'),
      collapse_risk:
        laneMembers.length >= 2 && siteCount === 1
          ? 'site_local_formula_risk'
          : laneMembers.length >= 2
            ? 'cross_site_or_cross_head_candidate'
            : 'singleton',
      decision:
        lane === '632_032_lane'
          ? 'candidate complement but Mohenjo-daro-local until source/site controls rescue it'
          : lane === '032_lane' || lane === '820_lane'
            ? 'small but useful complement lane because it crosses local formula boundaries'
            : lane === 'terminal_125'
              ? 'terminal 125 is exception to linker model'
              : 'do not use singleton lane as evidence yet',
    };
  })
  .sort((a, b) => Number(b.occurrences) - Number(a.occurrences) || a.lane.localeCompare(b.lane));

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_125_LANE_SPLIT',
    tier: 'candidate',
    claim:
      'X=125 is a linker, but its complements split into lanes: 632-032, 032, 820, and singleton residue.',
    risky_prediction:
      'At least two nonterminal lanes should survive outside one exact Mohenjo-daro formula family.',
    kill_condition:
      'Only 632-032 remains repeated and it collapses to a Mohenjo-daro source-window formula.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_125_632032_FORMULA_RISK',
    tier: 'wild shot',
    claim:
      'The 632-032 lane may be a Mohenjo-daro formula residue rather than a general complement.',
    risky_prediction:
      '632-032 should be less portable than 032 or 820 lanes.',
    kill_condition:
      '632-032 appears source-strong and cross-site in held-out/source-visible rows.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: '125_complement_collapse',
  x125_occurrences: x125Rows.length,
  lanes: Object.fromEntries(
    laneRows.map((row) => [
      row.lane,
      {
        occurrences: Number(row.occurrences),
        sites: row.sites,
        heads: row.heads,
        collapse_risk: row.collapse_risk,
      },
    ]),
  ),
  provisional_read:
    '125 survives as a linker candidate, but 632-032 is formula-risk while 032 and 820 provide small cross-lane support.',
};

writeCsv(path.join(reportsDir, `${prefix}_occurrences.csv`), x125Rows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'condition',
  'complete',
  'head',
  'x',
  'next1',
  'tail',
  'lane',
  'terminal',
  'text',
]);
writeCsv(path.join(reportsDir, `${prefix}_lane_rows.csv`), laneRows, [
  'checked_date',
  'lane',
  'occurrences',
  'sites',
  'site_count',
  'heads',
  'head_count',
  'types',
  'objects',
  'collapse_risk',
  'decision',
]);
writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), betRows, [
  'checked_date',
  'bet_id',
  'tier',
  'claim',
  'risky_prediction',
  'kill_condition',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
