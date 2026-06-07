import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_705125_chain_test_20260531';
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

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));

const chainRows = [];
const x705Rows = [];

for (const row of rows) {
  for (let i = 0; i < row.signs.length - 1; i += 1) {
    if (row.signs[i] === '705' && row.signs[i + 1] === '125') {
      chainRows.push({
        checked_date: checkedDate,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        condition: row.condition,
        complete: row.complete,
        prev1: row.signs[i - 1] ?? '<START>',
        next_after_chain: row.signs[i + 2] ?? '<END>',
        at_end: i + 2 === row.signs.length,
        in_x_slot: i >= 2 && row.signs[i - 2] === '002',
        head_if_x_slot: i >= 2 && row.signs[i - 2] === '002' ? row.signs[i - 1] : '',
        text: row.text,
      });
    }
  }
  for (let i = 0; i < row.signs.length - 2; i += 1) {
    if (row.signs[i] === '002' && row.signs[i + 2] === '705') {
      x705Rows.push({
        checked_date: checkedDate,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        head: row.signs[i + 1],
        next_after_705: row.signs[i + 3] ?? '<END>',
        terminal: i + 2 === row.signs.length - 1,
        text: row.text,
      });
    }
  }
}

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_705_125_CHAIN',
    tier: 'wild shot',
    claim:
      '705 can chain into 125 as classifier-to-linker: class-705 plus affiliation/complement linker.',
    risky_prediction:
      '705-125 should recur, preferably in X-slot contexts or with governed complements after 125.',
    kill_condition:
      '705-125 is singleton or source-weak; then M-1668 is an exception, not a rule.',
  },
];

const adjudicationRows = [
  {
    checked_date: checkedDate,
    test: '705_125_recurrence',
    result: `${chainRows.length}_705125_chains; ${x705Rows.filter((row) => !row.terminal).length}_nonterminal_x705_rows`,
    effect_on_705_classifier:
      chainRows.length >= 2
        ? 'classifier_to_linker_chain_survives_first_check'
        : 'classifier_to_linker_chain_not_established',
    effect_on_parser:
      chainRows.length >= 2
        ? 'allow 705-125 as a real operator chain'
        : 'treat M1668 as exception/source-test, not grammar',
    decision:
      chainRows.length >= 2
        ? 'keep 705-125 chain live'
        : 'do not build parser rules on singleton 705-125',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: '705125_chain_test',
  chain_occurrences: chainRows.length,
  x705_occurrences: x705Rows.length,
  x705_terminal: x705Rows.filter((row) => row.terminal).length,
  x705_next_after: tally(x705Rows.map((row) => row.next_after_705)),
  provisional_read:
    chainRows.length >= 2
      ? '705-125 chain remains live as classifier-to-linker.'
      : '705-125 is singleton; M-1668 is an exception, not a parser rule.',
};

writeCsv(path.join(reportsDir, `${prefix}_chain_rows.csv`), chainRows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'condition',
  'complete',
  'prev1',
  'next_after_chain',
  'at_end',
  'in_x_slot',
  'head_if_x_slot',
  'text',
]);
writeCsv(path.join(reportsDir, `${prefix}_x705_rows.csv`), x705Rows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'head',
  'next_after_705',
  'terminal',
  'text',
]);
writeCsv(path.join(reportsDir, `${prefix}_adjudication.csv`), adjudicationRows, [
  'checked_date',
  'test',
  'result',
  'effect_on_705_classifier',
  'effect_on_parser',
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
