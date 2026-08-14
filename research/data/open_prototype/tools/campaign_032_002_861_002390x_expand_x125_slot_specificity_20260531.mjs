import fs from 'node:fs';
import path from 'node:path';

// Is sign 125 an operator only when it sits in the X slot of 002-H-X, or does it behave the
// same everywhere? This script splits every 125 occurrence in the corpus into two groups:
// x_slot (exactly two positions after a 002) and non_x_slot (everywhere else). It reads
// data/open_prototype/lipi/metadata_filtered.csv and, for each group, measures the open rate
// (how often anything follows the 125), the terminal rate, and — the more telling number —
// how constrained the tails are: how many distinct tails exist and what share the top four
// cover. The finding it encodes: non-X 125 is also often open, so the operator claim must
// rest on tail constraint, not open rate; X-slot 125 draws from a small tail family while
// non-X 125 does not, and 125 therefore cannot be given one global meaning. Writes the
// occurrence rows, the two-group summary, and three bets as CSVs plus a summary JSON in
// reports/.

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_expand_x125_slot_specificity_20260531';

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
  return text.match(/\d{3}/g) ?? [];
}

function ratio(numerator, denominator) {
  return denominator ? `${numerator}/${denominator}` : '0/0';
}

function countBy(rows, keyFn) {
  const counts = new Map();
  for (const row of rows) {
    const key = keyFn(row) || '-';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }));
}

function topCounts(rows, keyFn) {
  return countBy(rows, keyFn)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function topCoverage(rows, keyFn, n) {
  const counts = countBy(rows, keyFn);
  const covered = counts.slice(0, n).reduce((sum, [, value]) => sum + value, 0);
  return ratio(covered, rows.length);
}

fs.mkdirSync(reportsDir, { recursive: true });

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));
const rows125 = [];
for (const row of metadataRows) {
  const rowSigns = signs(row.text);
  for (let index = 0; index < rowSigns.length; index += 1) {
    if (rowSigns[index] !== '125') continue;
    const isXSlot = index >= 2 && rowSigns[index - 2] === '002';
    rows125.push({
      checked_date: '2026-05-31',
      object: row.cisi,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      scope_cell: `${row.site}|${row.type}|${row.shape}|${row.material}`,
      slot: isXSlot ? 'x_slot' : 'non_x_slot',
      head_if_x_slot: isXSlot ? rowSigns[index - 1] : '',
      prev_before_125: rowSigns[index - 1] ?? '',
      next_after_125: rowSigns[index + 1] ?? '<END>',
      open: index < rowSigns.length - 1 ? 'True' : 'False',
      terminal: index === rowSigns.length - 1 ? 'True' : 'False',
      tail_after_125: rowSigns.slice(index + 1).join(' ') || '<END>',
      text: row.text,
    });
  }
}

const groups = ['x_slot', 'non_x_slot'].map((slot) => {
  const rows = rows125.filter((row) => row.slot === slot);
  const open = rows.filter((row) => row.open === 'True').length;
  const terminal = rows.filter((row) => row.terminal === 'True').length;
  const tailTypes = countBy(rows, (row) => row.tail_after_125).length;
  const nonEndRows = rows.filter((row) => row.tail_after_125 !== '<END>');
  return {
    checked_date: '2026-05-31',
    slot,
    rows: String(rows.length),
    open_rate: ratio(open, rows.length),
    terminal_rate: ratio(terminal, rows.length),
    tail_type_count: String(tailTypes),
    non_end_tail_type_count: String(countBy(nonEndRows, (row) => row.tail_after_125).length),
    top4_tail_coverage: topCoverage(rows, (row) => row.tail_after_125, 4),
    heads_if_x_slot: topCounts(rows, (row) => row.head_if_x_slot),
    prevs: topCounts(rows, (row) => row.prev_before_125),
    tails: topCounts(rows, (row) => row.tail_after_125),
    objects: rows.map((row) => row.object).join(';'),
  };
});

const xGroup = groups.find((row) => row.slot === 'x_slot');
const nonXGroup = groups.find((row) => row.slot === 'non_x_slot');
const bets = [
  {
    checked_date: '2026-05-31',
    bet_id: 'X125_OPERATOR_SIGNAL_IS_TAIL_CONSTRAINT_NOT_OPEN_RATE',
    tier: 'candidate',
    claim:
      'The X-slot `125` operator bet should rest on tail constraint, not merely on open rate; non-X `125` is also often open.',
    support: `X open=${xGroup.open_rate}; non-X open=${nonXGroup.open_rate}; X tails=${xGroup.tail_type_count}; non-X tails=${nonXGroup.tail_type_count}`,
    prediction:
      'If X-slot `125` tails become as unconstrained as non-X `125` tails, demote the dependent-operator role.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'X125_TAIL_FAMILY_CONSTRAINT',
    tier: 'candidate',
    claim:
      'X-slot `125` uses a small dependent-tail family compared with non-X `125`.',
    support: `X top4 tails cover ${xGroup.top4_tail_coverage}; non-X top4 tails cover ${nonXGroup.top4_tail_coverage}`,
    prediction:
      'Future X-slot `125` rows should reuse or modestly extend the current tail families, not explode into arbitrary long tails.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'NON_X_125_NAME_OR_CONTENT_REMAINS_POSSIBLE',
    tier: 'wild shot',
    claim:
      'Outside the X slot, `125` may still be lexical/content-like or formulaic; the operator role is slot-conditioned, not a global sign meaning.',
    support: `non-X prevs=${nonXGroup.prevs}; non-X tails=${nonXGroup.tails}`,
    prediction:
      'Do not assign one sign meaning to `125`; future parser should distinguish X-slot `125` from non-X `125`.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'EXPAND',
  status: 'x125_slot_specificity',
  group_summary: groups,
  new_bets: Object.fromEntries(bets.map((row) => [row.bet_id, row.tier])),
  predictions: [
    'Use tail-family constraint, not open rate alone, as the X-slot `125` operator signal.',
    'Future X-slot `125` should reuse current tails or add small variants.',
    'A single global meaning for `125` is disallowed by current slot split.',
  ],
};

writeCsv(path.join(reportsDir, `${prefix}_rows.csv`), rows125, [
  'checked_date',
  'object',
  'site',
  'type',
  'shape',
  'material',
  'scope_cell',
  'slot',
  'head_if_x_slot',
  'prev_before_125',
  'next_after_125',
  'open',
  'terminal',
  'tail_after_125',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_group_summary.csv`), groups, [
  'checked_date',
  'slot',
  'rows',
  'open_rate',
  'terminal_rate',
  'tail_type_count',
  'non_end_tail_type_count',
  'top4_tail_coverage',
  'heads_if_x_slot',
  'prevs',
  'tails',
  'objects',
]);

writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), bets, [
  'checked_date',
  'bet_id',
  'tier',
  'claim',
  'support',
  'prediction',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
