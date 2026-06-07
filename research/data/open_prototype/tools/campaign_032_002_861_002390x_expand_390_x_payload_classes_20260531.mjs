import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_expand_390_x_payload_classes_20260531';

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

function payloadClass(rows) {
  const open = rows.filter((row) => row.x_continuing === 'True').length;
  if (open === rows.length) return 'open_payload';
  if (open === 0) return 'terminal_payload';
  return 'mixed_payload';
}

fs.mkdirSync(reportsDir, { recursive: true });

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));
const frames390 = [];
for (const row of metadataRows) {
  const rowSigns = signs(row.text);
  for (let index = 0; index < rowSigns.length - 2; index += 1) {
    if (rowSigns[index] !== '002' || rowSigns[index + 1] !== '390') continue;
    const x = rowSigns[index + 2];
    frames390.push({
      checked_date: '2026-05-31',
      object: row.cisi,
      id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      symbol: row.symbol,
      cult: row.cult,
      prev1_before_002: rowSigns[index - 1] ?? '',
      prev2_before_002: rowSigns[index - 2] ?? '',
      x,
      x_continuing: index + 2 < rowSigns.length - 1 ? 'True' : 'False',
      x_terminal: index + 2 === rowSigns.length - 1 ? 'True' : 'False',
      tail_after_x: rowSigns.slice(index + 3).join(' ') || '<END>',
      scope_cell: `${row.site}|${row.type}|${row.shape}|${row.material}`,
      text: row.text,
    });
  }
}

const xValues = [...new Set(frames390.map((row) => row.x))].sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
const xSummary = xValues.map((x) => {
  const rows = frames390.filter((row) => row.x === x);
  const open = rows.filter((row) => row.x_continuing === 'True').length;
  const terminal = rows.filter((row) => row.x_terminal === 'True').length;
  return {
    checked_date: '2026-05-31',
    x,
    rows: String(rows.length),
    open_rate: ratio(open, rows.length),
    terminal_rate: ratio(terminal, rows.length),
    class: payloadClass(rows),
    prev1s: topCounts(rows, (row) => row.prev1_before_002),
    prev2s: topCounts(rows, (row) => row.prev2_before_002),
    tails: topCounts(rows, (row) => row.tail_after_x),
    scopes: topCounts(rows, (row) => row.scope_cell),
    objects: rows.map((row) => row.object).join(';'),
  };
});

const leftContextSummary = countBy(frames390, (row) => row.prev1_before_002).map(([prev1, count]) => {
  const rows = frames390.filter((row) => row.prev1_before_002 === prev1);
  const open = rows.filter((row) => row.x_continuing === 'True').length;
  const terminal = rows.filter((row) => row.x_terminal === 'True').length;
  return {
    checked_date: '2026-05-31',
    prev1_before_002: prev1,
    rows: String(count),
    open_rate: ratio(open, count),
    terminal_rate: ratio(terminal, count),
    xs: topCounts(rows, (row) => row.x),
    tails: topCounts(rows, (row) => row.tail_after_x),
    objects: rows.map((row) => row.object).join(';'),
    decision:
      open === count
        ? 'left_context_open_only'
        : terminal === count
          ? 'left_context_terminal_only'
          : 'left_context_splits_by_x',
  };
});

const terminalXs = xSummary.filter((row) => row.class === 'terminal_payload').map((row) => row.x);
const openXs = xSummary.filter((row) => row.class === 'open_payload').map((row) => row.x);
const repeatedTerminalXs = xSummary.filter((row) => row.class === 'terminal_payload' && Number(row.rows) >= 2).map((row) => row.x);
const repeatedOpenXs = xSummary.filter((row) => row.class === 'open_payload' && Number(row.rows) >= 2).map((row) => row.x);
const splitLeftContexts = leftContextSummary.filter((row) => row.decision === 'left_context_splits_by_x');

const bets = [
  {
    checked_date: '2026-05-31',
    bet_id: 'SIGN390_X_PAYLOAD_CLASSIFIER',
    tier: 'candidate',
    claim:
      '`002-390-X` is a payload-classifier construction: X controls whether the frame closes or opens a dependent tail.',
    support: `terminal X=${terminalXs.join(';')}; open X=${openXs.join(';')}`,
    prediction:
      'Future strict `002-390-095` and `002-390-705` rows should close; future strict `002-390-125` rows should continue.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'SIGN390_125_DEPENDENT_TAIL_PAYLOAD',
    tier: 'candidate',
    claim:
      'Under `002-390`, X=`125` is an open dependent-tail payload, not a standalone terminal name or commodity marker.',
    support: xSummary.filter((row) => row.x === '125').map((row) => `rows=${row.rows}; open=${row.open_rate}; tails=${row.tails}`).join('; '),
    prediction:
      'A strict terminal `002-390-125` kills this payload class; a new row should have a tail such as `632-032`, `195`, or `820` until a new tail class is discovered.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'SIGN390_095705_TERMINAL_PAYLOADS',
    tier: 'candidate',
    claim:
      '`095` and `705` are terminal payloads under `002-390`, with `705` making the Dholavira candidate a closing X-slot if source-bound.',
    support: xSummary.filter((row) => row.x === '095' || row.x === '705').map((row) => `${row.x}: rows=${row.rows}; terminal=${row.terminal_rate}; objects=${row.objects}`).join('; '),
    prediction:
      'If Dholavira item 10 binds to `+151-032-388-002-390-705+`, it supports terminal `705`; a visible continuation after `705` kills this bet.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'SIGN390_530590_OPEN_EXTENDER_PAYLOADS',
    tier: 'wild shot',
    claim:
      '`530` and `590` are open extender payloads under `002-390`, separate from `125` but still tail-licensing.',
    support: xSummary.filter((row) => row.x === '530' || row.x === '590').map((row) => `${row.x}: rows=${row.rows}; open=${row.open_rate}; tails=${row.tails}`).join('; '),
    prediction:
      'A strict terminal `002-390-530` or `002-390-590` kills the extender class unless register can explain it.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'SIGN390_X_SLOT_BEATS_LEFT_CONTEXT',
    tier: 'candidate',
    claim:
      'The X slot, not the immediate left context alone, controls continuation under `002-390`; the same left sign can split by X.',
    support: splitLeftContexts.map((row) => `${row.prev1_before_002}: ${row.xs}; open=${row.open_rate}`).join(' | '),
    prediction:
      'New rows sharing left contexts `004` or `032` should still follow X-class behavior: `125`/`590` open, `095`/`692` terminal.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'EXPAND',
  status: 'sign390_x_payload_classes',
  total_002390x_rows: frames390.length,
  x_summary: xSummary,
  payload_classes: {
    terminal_xs: terminalXs,
    repeated_terminal_xs: repeatedTerminalXs,
    open_xs: openXs,
    repeated_open_xs: repeatedOpenXs,
  },
  split_left_contexts: splitLeftContexts,
  new_bets: Object.fromEntries(bets.map((row) => [row.bet_id, row.tier])),
  predictions: [
    '`002-390-125` should continue with a dependent tail.',
    '`002-390-095` and `002-390-705` should terminate.',
    'If Dholavira item 10 binds to `+151-032-388-002-390-705+`, it is evidence for terminal `705`, not for a generic 125-like branch.',
    '`002-390-530` and `002-390-590` should continue if the open-extender wild shot is real.',
  ],
};

writeCsv(path.join(reportsDir, `${prefix}_rows.csv`), frames390, [
  'checked_date',
  'object',
  'id',
  'site',
  'type',
  'shape',
  'material',
  'symbol',
  'cult',
  'prev1_before_002',
  'prev2_before_002',
  'x',
  'x_continuing',
  'x_terminal',
  'tail_after_x',
  'scope_cell',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_x_summary.csv`), xSummary, [
  'checked_date',
  'x',
  'rows',
  'open_rate',
  'terminal_rate',
  'class',
  'prev1s',
  'prev2s',
  'tails',
  'scopes',
  'objects',
]);

writeCsv(path.join(reportsDir, `${prefix}_left_context_summary.csv`), leftContextSummary, [
  'checked_date',
  'prev1_before_002',
  'rows',
  'open_rate',
  'terminal_rate',
  'xs',
  'tails',
  'objects',
  'decision',
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
