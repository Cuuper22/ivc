import fs from 'node:fs';
import path from 'node:path';

// This script stakes the first functional (not just syntactic) bet on 390:
// that 002-390-X is an authority/status formula, with 390 as a status or
// title head — rather than a commodity label. It scans
// lipi/metadata_filtered.csv for every 002-390-X occurrence and routes each
// row by its X sign: terminal classifiers (095, 705, 000, 140, 692, 707,
// 072, 346), linkers (125, 530, 590), or other. Per route it profiles counts,
// terminal share, average text length, prefix length before the frame, and
// the spread across sites, object types, and iconography. The function
// reading only holds if the routes differ the predicted way: classifier
// closures short, linker branches longer and complement-bearing, and rows
// concentrated on seals and tablets rather than pottery or tags. Three wild-
// shot bets with kill conditions are recorded alongside. Writes route
// summaries, raw occurrences, and bets as CSVs plus a summary JSON to
// data/open_prototype/reports.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_390_function_bet_20260531';
const checkedDate = '2026-05-31';

const terminalClassifiers = new Set(['095', '705', '000', '140', '692', '707', '072', '346']);
const linkers = new Set(['125', '530', '590']);

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

function avg(values) {
  if (!values.length) return '0.000';
  return (values.reduce((sum, value) => sum + value, 0) / values.length).toFixed(3);
}

function routeFor(x) {
  if (terminalClassifiers.has(x)) return 'terminal_classifier';
  if (linkers.has(x)) return 'linker_complement';
  return 'other_or_underpowered';
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));

const head390Rows = [];
for (const row of rows) {
  for (let i = 0; i < row.signs.length - 2; i += 1) {
    if (row.signs[i] !== '002' || row.signs[i + 1] !== '390') continue;
    const x = row.signs[i + 2];
    const route = routeFor(x);
    head390Rows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      symbol: row.symbol,
      condition: row.condition,
      complete: row.complete,
      route,
      x,
      terminal: i + 2 === row.signs.length - 1,
      tail: row.signs.slice(i + 3).join('-') || '<END>',
      total_length: row.signs.length,
      prefix_length_before_frame: i,
      text: row.text,
    });
  }
}

const routeRows = [...new Set(head390Rows.map((row) => row.route))]
  .map((route) => {
    const members = head390Rows.filter((row) => row.route === route);
    return {
      checked_date: checkedDate,
      route,
      occurrences: members.length,
      terminal: members.filter((row) => row.terminal).length,
      avg_total_length: avg(members.map((row) => row.total_length)),
      avg_prefix_length: avg(members.map((row) => row.prefix_length_before_frame)),
      sites: tally(members.map((row) => row.site)),
      types: tally(members.map((row) => row.type)),
      symbols: tally(members.map((row) => row.symbol)),
      x_values: tally(members.map((row) => row.x)),
      objects: members.map((row) => row.object).join(';'),
      function_read:
        route === 'terminal_classifier'
          ? 'short authority/status closure'
          : route === 'linker_complement'
            ? 'status head with affiliation/complement tail'
            : 'unclassified 390 branch',
    };
  })
  .sort((a, b) => Number(b.occurrences) - Number(a.occurrences) || a.route.localeCompare(b.route));

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_390_AUTHORITY_STATUS_FUNCTION',
    tier: 'wild shot',
    claim:
      '002-390-X is an authority/status formula, not a commodity label: 390 is a status/title head.',
    risky_prediction:
      'Rows should concentrate in seals/tablets, with terminal classifier branches shorter than linker-complement branches.',
    kill_condition:
      '390 routes appear heavily on commodity-like pottery/tags or lack route-dependent length/function behavior.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_095_705_CLASSIFIER_FUNCTION',
    tier: 'wild shot',
    claim:
      '095 and 705 are overt terminal classifiers for the 390 status/title head.',
    risky_prediction:
      '095/705 should be terminal, short, and seal/tablet-heavy after source filtering.',
    kill_condition:
      '095/705 rows are source-weak visual copies or artifact-type random.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_125_AFFILIATION_COMPLEMENT',
    tier: 'wild shot',
    claim:
      '390-125 introduces an affiliation/complement lane, not a second title/name.',
    risky_prediction:
      '390-125 rows should be longer than classifier closures and followed by recurrent complement classes.',
    kill_condition:
      '390-125 tails do not survive source/site controls as complement lanes.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: '390_function_bet',
  head390_occurrences: head390Rows.length,
  routes: Object.fromEntries(
    routeRows.map((row) => [
      row.route,
      {
        occurrences: Number(row.occurrences),
        terminal: Number(row.terminal),
        avg_total_length: row.avg_total_length,
        types: row.types,
        x_values: row.x_values,
      },
    ]),
  ),
  provisional_read:
    '390 authority/status function survives if terminal-classifier routes stay shorter and linker routes stay complement-bearing.',
};

writeCsv(path.join(reportsDir, `${prefix}_route_rows.csv`), routeRows, [
  'checked_date',
  'route',
  'occurrences',
  'terminal',
  'avg_total_length',
  'avg_prefix_length',
  'sites',
  'types',
  'symbols',
  'x_values',
  'objects',
  'function_read',
]);
writeCsv(path.join(reportsDir, `${prefix}_occurrences.csv`), head390Rows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'symbol',
  'condition',
  'complete',
  'route',
  'x',
  'terminal',
  'tail',
  'total_length',
  'prefix_length_before_frame',
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
