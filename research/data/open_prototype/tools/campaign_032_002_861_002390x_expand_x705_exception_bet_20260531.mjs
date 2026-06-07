import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_expand_x705_exception_bet_20260531';

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

fs.mkdirSync(reportsDir, { recursive: true });

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));
const x705Rows = [];
for (const row of metadataRows) {
  const rowSigns = signs(row.text);
  for (let index = 0; index < rowSigns.length - 2; index += 1) {
    if (rowSigns[index] !== '002' || rowSigns[index + 2] !== '705') continue;
    x705Rows.push({
      checked_date: '2026-05-31',
      object: row.cisi,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      scope_cell: `${row.site}|${row.type}|${row.shape}|${row.material}`,
      prev_before_002: rowSigns[index - 1] ?? '',
      head_after_002: rowSigns[index + 1],
      x: '705',
      x_continuing: index + 2 < rowSigns.length - 1 ? 'True' : 'False',
      x_terminal: index + 2 === rowSigns.length - 1 ? 'True' : 'False',
      tail_after_705: rowSigns.slice(index + 3).join(' ') || '<END>',
      text: row.text,
    });
  }
}

const terminalRows = x705Rows.filter((row) => row.x_terminal === 'True');
const openRows = x705Rows.filter((row) => row.x_continuing === 'True');
const bets = [
  {
    checked_date: '2026-05-31',
    bet_id: 'X705_TERMINAL_DEFAULT_WITH_HEAD320_EXCEPTION',
    tier: 'candidate',
    claim:
      '`705` is terminal by default in X-slot, but head `320` may license a `705-125` exception.',
    support: `terminal=${ratio(terminalRows.length, x705Rows.length)}; open rows=${openRows.map((row) => `${row.object}:${row.head_after_002}->${row.tail_after_705}`).join(';')}`,
    prediction:
      'Future `002-390-705`, `002-033-705`, and `002-940-705` should close; future `002-320-705` should be checked for a `125` cap.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'X705_125_CAP_EXCEPTION',
    tier: 'wild shot',
    claim:
      'The lone open `705` row closes through a following `125`, making `125` a cap/operator even outside the original `390-125` route.',
    support: openRows.map((row) => `${row.object}: ${row.text}`).join('; '),
    prediction:
      'Another `002-320-705-125` or `002-H-705-125` row promotes this; open `705` with another tail weakens it.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'DHOLAVIRA_705_SHOULD_CLOSE_IF_BOUND',
    tier: 'candidate',
    claim:
      'The Dholavira `002-390-705` candidate should be terminal if source-bound.',
    support: x705Rows.filter((row) => row.head_after_002 === '390').map((row) => `${row.object}:${row.x_terminal}`).join('; '),
    prediction:
      'If page 18 item 10 has visible continuation after `705`, demote both Dholavira terminal pressure and the `390-705` terminal class.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'EXPAND',
  status: 'x705_exception_bet',
  x705_total: x705Rows.length,
  x705_terminal_rate: ratio(terminalRows.length, x705Rows.length),
  terminal_heads: topCounts(terminalRows, (row) => row.head_after_002),
  open_heads: topCounts(openRows, (row) => row.head_after_002),
  rows: x705Rows,
  new_bets: Object.fromEntries(bets.map((row) => [row.bet_id, row.tier])),
  predictions: [
    '`002-390-705` should close.',
    '`002-320-705` should be checked for a following `125` cap.',
    'A continuing Dholavira `002-390-705-Y` is the cleanest kill shot.',
  ],
};

writeCsv(path.join(reportsDir, `${prefix}_rows.csv`), x705Rows, [
  'checked_date',
  'object',
  'site',
  'type',
  'shape',
  'material',
  'scope_cell',
  'prev_before_002',
  'head_after_002',
  'x',
  'x_continuing',
  'x_terminal',
  'tail_after_705',
  'text',
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
