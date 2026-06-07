import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const parseRowsPath = path.join(
  reportsDir,
  'campaign_032_002_861_002390x_expand_x000_null_class_20260531_parse_rows_plus_000.csv',
);
const prefix = 'campaign_032_002_861_002390x_expand_xslot_terminality_null_20260531';
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

function ratio(numerator, denominator) {
  return denominator ? `${numerator}/${denominator}` : '0/0';
}

function percentage(numerator, denominator) {
  return denominator ? (numerator / denominator).toFixed(3) : '0.000';
}

function countBy(items, keyFn) {
  const counts = new Map();
  for (const item of items) {
    const key = keyFn(item) || '-';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }))
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

fs.mkdirSync(reportsDir, { recursive: true });

const parseRows = parseCsv(fs.readFileSync(parseRowsPath, 'utf8'));
const byX = [...new Set(parseRows.map((row) => row.x))].map((x) => {
  const rows = parseRows.filter((row) => row.x === x);
  const terminal = rows.filter((row) => row.tail_after_x === '<END>');
  return {
    checked_date: checkedDate,
    x,
    rows: String(rows.length),
    terminal: ratio(terminal.length, rows.length),
    terminal_rate: percentage(terminal.length, rows.length),
    open_rows: String(rows.length - terminal.length),
    head_profile: countBy(rows, (row) => row.head),
    site_profile: countBy(rows, (row) => row.site),
    examples: rows.slice(0, 8).map((row) => `${row.object}:${row.head}-${row.x}-${row.tail_after_x}`).join(' | '),
  };
});

const frequent = byX
  .filter((row) => Number(row.rows) >= 5)
  .sort((a, b) => Number(b.terminal_rate) - Number(a.terminal_rate) || Number(b.rows) - Number(a.rows));
const x000 = byX.find((row) => row.x === '000');
const frequentWithout000 = frequent.filter((row) => row.x !== '000');
const terminalRate000 = Number(x000?.terminal_rate ?? 0);
const equalOrHigher = frequentWithout000.filter((row) => Number(row.terminal_rate) >= terminalRate000);
const topTerminalNon000 = frequentWithout000[0];

const bets = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_X000_BEATS_X_SLOT_TERMINALITY_NULL',
    tier: x000 && equalOrHigher.length === 0 && terminalRate000 >= 0.85 ? 'candidate' : 'wild_shot',
    risky_bet:
      '`000` is not just riding a generic X-slot terminality bias; among frequent X signs, it is at or near the terminal extreme.',
    current_test:
      `x000_terminal=${x000?.terminal ?? '0/0'}; x000_rate=${x000?.terminal_rate ?? '0.000'}; top_non000=${topTerminalNon000?.x ?? '-'}:${topTerminalNon000?.terminal ?? '0/0'}; frequent_equal_or_higher_than_000=${equalOrHigher.map((row) => `${row.x}:${row.terminal}`).join(';') || 'none'}.`,
    destructive_prediction:
      'If multiple frequent X signs terminalize as strongly as `000`, zero-complement is probably just a generic right-edge artifact.',
    promotion_prediction:
      '`000` stays special if it remains more terminal than other frequent X signs while also showing frame-proximal role effects.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'xslot_terminality_null',
  x_signs: byX.length,
  frequent_x_signs: frequent.length,
  x000_terminal: x000?.terminal ?? '0/0',
  x000_terminal_rate: x000?.terminal_rate ?? '0.000',
  top_frequent_x: frequent.slice(0, 10).map((row) => `${row.x}:${row.terminal}`).join(';'),
  frequent_equal_or_higher_than_000: equalOrHigher.map((row) => `${row.x}:${row.terminal}`),
  bets: bets.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

writeCsv(path.join(reportsDir, `${prefix}_x_terminality.csv`), byX, [
  'checked_date',
  'x',
  'rows',
  'terminal',
  'terminal_rate',
  'open_rows',
  'head_profile',
  'site_profile',
  'examples',
]);
writeCsv(path.join(reportsDir, `${prefix}_frequent_x_terminality.csv`), frequent, [
  'checked_date',
  'x',
  'rows',
  'terminal',
  'terminal_rate',
  'open_rows',
  'head_profile',
  'site_profile',
  'examples',
]);
writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), bets, [
  'checked_date',
  'bet_id',
  'tier',
  'risky_bet',
  'current_test',
  'destructive_prediction',
  'promotion_prediction',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
