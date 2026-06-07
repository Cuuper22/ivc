import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_xslot_edge_transfer_20260531';
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

function pct(numerator, denominator) {
  return denominator ? (numerator / denominator).toFixed(3) : '0.000';
}

function classify(xCount, xTerminalRate, globalTerminalRate, delta) {
  if (xCount < 3) return 'underpowered';
  if (delta >= 0.2) return 'constructional_terminal_boost';
  if (delta <= -0.2) return 'constructional_anti_terminal_or_payload';
  if (xTerminalRate >= 0.6 && Math.abs(delta) < 0.15) return 'global_edge_transfer';
  if (xTerminalRate < 0.5 && Math.abs(delta) < 0.15) return 'open_or_payload_transfer';
  return 'mixed';
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));

const xOccurrences = [];
const globalStats = new Map();
const xStats = new Map();

for (const row of rows) {
  const signs = row.signs;
  for (let i = 0; i < signs.length; i += 1) {
    const sign = signs[i];
    const stat = globalStats.get(sign) ?? {
      sign,
      occurrences: 0,
      terminal: 0,
      sites: [],
      types: [],
    };
    stat.occurrences += 1;
    if (i === signs.length - 1) stat.terminal += 1;
    stat.sites.push(row.site);
    stat.types.push(row.type);
    globalStats.set(sign, stat);
  }

  for (let i = 0; i < signs.length - 2; i += 1) {
    if (signs[i] !== '002') continue;
    const head = signs[i + 1];
    const x = signs[i + 2];
    const terminal = i + 2 === signs.length - 1;
    const occurrence = {
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      head,
      x,
      terminal,
      next1: signs[i + 3] ?? '<END>',
      text: row.text,
    };
    xOccurrences.push(occurrence);
    const stat = xStats.get(x) ?? {
      x,
      occurrences: 0,
      terminal: 0,
      heads: [],
      sites: [],
      types: [],
      next1: [],
      objects: [],
    };
    stat.occurrences += 1;
    if (terminal) stat.terminal += 1;
    stat.heads.push(head);
    stat.sites.push(row.site);
    stat.types.push(row.type);
    stat.next1.push(occurrence.next1);
    stat.objects.push(row.object);
    xStats.set(x, stat);
  }
}

const xRows = [...xStats.values()]
  .map((stat) => {
    const global = globalStats.get(stat.x);
    const xTerminalRate = stat.terminal / stat.occurrences;
    const globalTerminalRate = global.terminal / global.occurrences;
    const delta = xTerminalRate - globalTerminalRate;
    return {
      checked_date: checkedDate,
      x: stat.x,
      x_occurrences: stat.occurrences,
      x_terminal: stat.terminal,
      x_terminal_rate: xTerminalRate.toFixed(3),
      global_occurrences: global.occurrences,
      global_terminal: global.terminal,
      global_terminal_rate: globalTerminalRate.toFixed(3),
      terminal_delta: delta.toFixed(3),
      classification: classify(stat.occurrences, xTerminalRate, globalTerminalRate, delta),
      heads: tally(stat.heads),
      sites: tally(stat.sites),
      types: tally(stat.types),
      next1: tally(stat.next1),
      sample_objects: stat.objects.slice(0, 12).join(';'),
    };
  })
  .sort((a, b) => Number(b.x_occurrences) - Number(a.x_occurrences) || a.x.localeCompare(b.x));

const focusSigns = ['000', '033', '095', '125', '530', '590', '692', '705', '861'];
const focusRows = xRows.filter((row) => focusSigns.includes(row.x));

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_EDGE_STATE_XSLOT',
    tier: 'wild shot',
    claim:
      'The X slot is an edge-state operator slot: some X values are inherited global edge markers, while others become terminal only inside 002-H-X.',
    risky_prediction:
      'Known branch signs should split into global_edge_transfer versus constructional_terminal_boost classes by terminal_delta.',
    kill_condition:
      'All frequent X values show near-zero delta and no interpretable split; then the slot is mostly copied visual register.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_000_EDGE_TRANSFER_NOT_GRAMMAR_CORE',
    tier: 'candidate if delta is small',
    claim:
      'X=000 is partly inherited edge behavior, not a clean grammatical null by itself.',
    risky_prediction:
      '000 terminality in X slot should be close to its global terminality or only moderately boosted.',
    kill_condition:
      '000 has a very large construction-specific terminal boost while comparable edge signs do not.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_NON000_CONSTRUCTIONAL_BRANCH',
    tier: 'wild shot',
    claim:
      'A non-000 X sign with high positive terminal_delta is a better grammar candidate than 000.',
    risky_prediction:
      'At least one of 095/705/530/125/590/692 has a stronger constructional boost than 000.',
    kill_condition:
      'No non-000 focus sign has positive terminal_delta with at least 3 X-slot occurrences.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'xslot_edge_transfer',
  total_x_occurrences: xOccurrences.length,
  frequent_x_signs: xRows.filter((row) => Number(row.x_occurrences) >= 3).length,
  focus: Object.fromEntries(
    focusRows.map((row) => [
      row.x,
      {
        x_occurrences: Number(row.x_occurrences),
        x_terminal_rate: row.x_terminal_rate,
        global_terminal_rate: row.global_terminal_rate,
        terminal_delta: row.terminal_delta,
        classification: row.classification,
      },
    ]),
  ),
  provisional_read:
    'If 000 looks like global edge transfer and a non-000 sign has constructional boost, move the parser away from null-core toward edge/operator classes.',
};

writeCsv(path.join(reportsDir, `${prefix}_x_rows.csv`), xRows, [
  'checked_date',
  'x',
  'x_occurrences',
  'x_terminal',
  'x_terminal_rate',
  'global_occurrences',
  'global_terminal',
  'global_terminal_rate',
  'terminal_delta',
  'classification',
  'heads',
  'sites',
  'types',
  'next1',
  'sample_objects',
]);
writeCsv(path.join(reportsDir, `${prefix}_focus_rows.csv`), focusRows, [
  'checked_date',
  'x',
  'x_occurrences',
  'x_terminal',
  'x_terminal_rate',
  'global_occurrences',
  'global_terminal',
  'global_terminal_rate',
  'terminal_delta',
  'classification',
  'heads',
  'sites',
  'types',
  'next1',
  'sample_objects',
]);
writeCsv(path.join(reportsDir, `${prefix}_occurrences.csv`), xOccurrences, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'head',
  'x',
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
