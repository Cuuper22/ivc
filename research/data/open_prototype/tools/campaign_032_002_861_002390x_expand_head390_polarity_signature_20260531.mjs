import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_head390_polarity_signature_20260531';
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

function polarityForX(x) {
  const terminalBoosters = new Set([
    '000',
    '031',
    '416',
    '575',
    '317',
    '705',
    '741',
    '491',
    '095',
    '260',
    '820',
    '140',
    '165',
    '603',
  ]);
  const openOperators = new Set(['125', '455', '530', '003', '861', '065', '035', '906', '460', '090']);
  const globalEdges = new Set(['501', '091', '692']);
  if (terminalBoosters.has(x)) return 'terminal_booster';
  if (openOperators.has(x)) return 'open_operator';
  if (globalEdges.has(x)) return 'global_edge';
  return 'mixed_or_underpowered';
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));

const occurrences = [];
for (const row of rows) {
  for (let i = 0; i < row.signs.length - 2; i += 1) {
    if (row.signs[i] !== '002') continue;
    const head = row.signs[i + 1];
    const x = row.signs[i + 2];
    occurrences.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      condition: row.condition,
      complete: row.complete,
      head,
      x,
      polarity: polarityForX(x),
      terminal: i + 2 === row.signs.length - 1,
      next1: row.signs[i + 3] ?? '<END>',
      text: row.text,
    });
  }
}

const byHead = new Map();
for (const row of occurrences) {
  const stat = byHead.get(row.head) ?? { head: row.head, rows: [] };
  stat.rows.push(row);
  byHead.set(row.head, stat);
}

const headRows = [...byHead.values()]
  .map((stat) => {
    const rowsForHead = stat.rows;
    return {
      checked_date: checkedDate,
      head: stat.head,
      occurrences: rowsForHead.length,
      terminal_rate: (rowsForHead.filter((row) => row.terminal).length / rowsForHead.length).toFixed(3),
      unique_x: uniqueCount(rowsForHead.map((row) => row.x)),
      x_values: tally(rowsForHead.map((row) => row.x)),
      polarity_mix: tally(rowsForHead.map((row) => row.polarity)),
      sites: tally(rowsForHead.map((row) => row.site)),
      types: tally(rowsForHead.map((row) => row.type)),
      next1: tally(rowsForHead.map((row) => row.next1)),
      sample_objects: rowsForHead.map((row) => row.object).slice(0, 12).join(';'),
    };
  })
  .filter((row) => Number(row.occurrences) >= 3)
  .sort((a, b) => Number(b.occurrences) - Number(a.occurrences) || a.head.localeCompare(b.head));

const head390Rows = occurrences.filter((row) => row.head === '390');
const head390ByX = [...new Set(head390Rows.map((row) => row.x))]
  .map((x) => {
    const rowsForX = head390Rows.filter((row) => row.x === x);
    return {
      checked_date: checkedDate,
      head: '390',
      x,
      polarity: polarityForX(x),
      occurrences: rowsForX.length,
      terminal: rowsForX.filter((row) => row.terminal).length,
      next1: tally(rowsForX.map((row) => row.next1)),
      sites: tally(rowsForX.map((row) => row.site)),
      types: tally(rowsForX.map((row) => row.type)),
      objects: rowsForX.map((row) => row.object).join(';'),
    };
  })
  .sort((a, b) => Number(b.occurrences) - Number(a.occurrences) || a.x.localeCompare(b.x));

const statusTitleSignature =
  head390ByX.some((row) => row.polarity === 'terminal_booster') &&
  head390ByX.some((row) => row.polarity === 'open_operator');

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_390_STATUS_HEAD',
    tier: 'wild shot',
    claim:
      'In 002-390-X, 390 is a status/title head that can take either closure classifiers or continuation linkers.',
    risky_prediction:
      'Head 390 should show a polarity split: terminal boosters like 095/705 and open operators like 125/530.',
    kill_condition:
      '390 collapses to one X family, one site/source window, or tail residue with no polarity contrast.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_002_FRAME_MARKER',
    tier: 'candidate',
    claim:
      '002 contributes the frame/license: the following head chooses an X-polarity profile, not just a fixed visual string.',
    risky_prediction:
      'Different heads after 002 should have different polarity mixes rather than one universal X distribution.',
    kill_condition:
      'Head-specific polarity profiles vanish after source/site/type collapse.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'head390_polarity_signature',
  head390_occurrences: head390Rows.length,
  head390_unique_x: uniqueCount(head390Rows.map((row) => row.x)),
  head390_polarity_mix: tally(head390Rows.map((row) => row.polarity)),
  head390_x_values: tally(head390Rows.map((row) => row.x)),
  status_title_signature: statusTitleSignature,
  provisional_read: statusTitleSignature
    ? '390 has both terminal and open X values, so status/title head remains live.'
    : '390 lacks polarity split; status/title head bet weakens immediately.',
};

writeCsv(path.join(reportsDir, `${prefix}_head_rows.csv`), headRows, [
  'checked_date',
  'head',
  'occurrences',
  'terminal_rate',
  'unique_x',
  'x_values',
  'polarity_mix',
  'sites',
  'types',
  'next1',
  'sample_objects',
]);
writeCsv(path.join(reportsDir, `${prefix}_head390_x_rows.csv`), head390ByX, [
  'checked_date',
  'head',
  'x',
  'polarity',
  'occurrences',
  'terminal',
  'next1',
  'sites',
  'types',
  'objects',
]);
writeCsv(path.join(reportsDir, `${prefix}_occurrences.csv`), occurrences, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'condition',
  'complete',
  'head',
  'x',
  'polarity',
  'terminal',
  'next1',
  'text',
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
