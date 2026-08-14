import fs from 'node:fs';
import path from 'node:path';

// Are the signs that fill the X slot of 002-H-X function words or a list of names?
// This script assigns each of eight focus signs (125, 095, 692, 705, 590, 530, 140, 072) a
// provisional functional role. It reads data/open_prototype/lipi/metadata_filtered.csv, logs
// every sign occurrence in the whole corpus (to get each sign's global terminal rate — how
// often it ends an inscription anywhere), and separately collects every 002-H-X window.
// A threshold rule then labels each focus sign: dependent_tail_operator if it usually opens
// a tail in the X slot, terminal_class_label if it reliably closes across sites,
// raw_boundary_closer if it closes everywhere even outside the construction, open_extender,
// or unresolved_payload. Five bets follow, the headline one being that function classes beat
// a name-list reading. Writes a per-sign role CSV, a bets CSV, and a summary JSON to reports/.

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_expand_x_function_role_bets_20260531';
const focusSigns = ['125', '095', '692', '705', '590', '530', '140', '072'];

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

function roleFor({ globalRows, xRows }) {
  const xOpen = xRows.filter((row) => row.x_continuing).length;
  const xTerminal = xRows.filter((row) => row.x_terminal).length;
  const globalTerminal = globalRows.filter((row) => row.terminal).length;
  const nonEndTails = xRows.filter((row) => row.tail_after_x !== '<END>').length;
  const xOpenRate = xRows.length ? xOpen / xRows.length : 0;
  const xTerminalRate = xRows.length ? xTerminal / xRows.length : 0;
  const globalTerminalRate = globalRows.length ? globalTerminal / globalRows.length : 0;
  const xSites = new Set(xRows.map((row) => row.site).filter(Boolean));
  if (xRows.length >= 4 && xOpenRate >= 0.7 && nonEndTails >= 3) return 'dependent_tail_operator';
  if (xRows.length >= 3 && xTerminalRate >= 0.8 && globalRows.length >= 20 && xSites.size >= 2) return 'terminal_class_label';
  if (xRows.length >= 2 && xTerminalRate >= 0.8 && globalTerminalRate >= 0.65) return 'raw_boundary_closer';
  if (xRows.length >= 3 && xOpenRate >= 0.7 && nonEndTails >= 2) return 'open_extender';
  return 'unresolved_payload';
}

fs.mkdirSync(reportsDir, { recursive: true });

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));
const globalOccurrences = [];
const xSlotRows = [];

for (const row of metadataRows) {
  const rowSigns = signs(row.text);
  for (let index = 0; index < rowSigns.length; index += 1) {
    const scope = `${row.site}|${row.type}|${row.shape}|${row.material}`;
    globalOccurrences.push({
      checked_date: '2026-05-31',
      object: row.cisi,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      sign: rowSigns[index],
      prev: rowSigns[index - 1] ?? '',
      next: rowSigns[index + 1] ?? '',
      terminal: index === rowSigns.length - 1,
      continuing: index < rowSigns.length - 1,
      scope_cell: scope,
      text: row.text,
    });
    if (rowSigns[index] === '002' && rowSigns[index + 1] && rowSigns[index + 2]) {
      xSlotRows.push({
        checked_date: '2026-05-31',
        object: row.cisi,
        site: row.site,
        type: row.type,
        shape: row.shape,
        material: row.material,
        head: rowSigns[index + 1],
        x: rowSigns[index + 2],
        x_terminal: index + 2 === rowSigns.length - 1,
        x_continuing: index + 2 < rowSigns.length - 1,
        tail_after_x: rowSigns.slice(index + 3).join(' ') || '<END>',
        scope_cell: scope,
        text: row.text,
      });
    }
  }
}

const roleRows = focusSigns.map((sign) => {
  const globalRows = globalOccurrences.filter((row) => row.sign === sign);
  const xRows = xSlotRows.filter((row) => row.x === sign);
  const xOpen = xRows.filter((row) => row.x_continuing).length;
  const xTerminal = xRows.filter((row) => row.x_terminal).length;
  const globalTerminal = globalRows.filter((row) => row.terminal).length;
  return {
    checked_date: '2026-05-31',
    sign,
    provisional_role: roleFor({ globalRows, xRows }),
    global_occurrences: String(globalRows.length),
    global_terminal_rate: ratio(globalTerminal, globalRows.length),
    x_slot_rows: String(xRows.length),
    x_slot_open_rate: ratio(xOpen, xRows.length),
    x_slot_terminal_rate: ratio(xTerminal, xRows.length),
    x_slot_heads: topCounts(xRows, (row) => row.head),
    x_slot_sites: topCounts(xRows, (row) => row.site),
    x_slot_scopes: topCounts(xRows, (row) => row.scope_cell),
    x_slot_tails: topCounts(xRows, (row) => row.tail_after_x),
    x_slot_objects: xRows.map((row) => row.object).join(';'),
  };
});

const bets = [
  {
    checked_date: '2026-05-31',
    bet_id: 'X125_DEPENDENT_OPERATOR_NOT_NAME',
    tier: 'candidate',
    claim:
      '`125` in the X slot behaves like a dependent-tail operator, not a personal name, title, or commodity label.',
    support: roleRows.filter((row) => row.sign === '125').map((row) => `role=${row.provisional_role}; x open=${row.x_slot_open_rate}; tails=${row.x_slot_tails}`).join('; '),
    prediction:
      'Future X-slot `125` should usually license a following tail; terminal X-slot `125` should remain head-conditioned exceptions.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'X095_X705_TERMINAL_CLASS_LABELS',
    tier: 'candidate',
    claim:
      '`095` and `705` behave like terminal class/office/commodity labels in the X slot, not unique names.',
    support: roleRows.filter((row) => row.sign === '095' || row.sign === '705').map((row) => `${row.sign}: role=${row.provisional_role}; x terminal=${row.x_slot_terminal_rate}; sites=${row.x_slot_sites}`).join('; '),
    prediction:
      'A new cross-site X-slot `095` or `705` should terminate unless it appears under a specific open-exception head.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'X692_BOUNDARY_CLOSER_NOT_390_VALUE',
    tier: 'wild shot',
    claim:
      '`692` is more likely a boundary closer than a `390`-selected semantic payload because raw `692` is already terminal-heavy.',
    support: roleRows.filter((row) => row.sign === '692').map((row) => `role=${row.provisional_role}; global terminal=${row.global_terminal_rate}; x terminal=${row.x_slot_terminal_rate}`).join('; '),
    prediction:
      '`692` should keep closing across non-390 environments; if it opens with dependent tails under other heads, revive it as a payload class.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'X590_OPEN_EXTENDER_NOT_NAME',
    tier: 'wild shot',
    claim:
      '`590` may be an open extender/linker in selected X slots, not a name, because it licenses tails under `390` and other heads.',
    support: roleRows.filter((row) => row.sign === '590').map((row) => `role=${row.provisional_role}; x open=${row.x_slot_open_rate}; heads=${row.x_slot_heads}; tails=${row.x_slot_tails}`).join('; '),
    prediction:
      'If new `002-390-590` rows terminate, kill the extender reading; if they continue with `032` or another stable tail, promote it.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'X_FUNCTION_CLASSES_BEAT_NAME_LIST',
    tier: 'candidate',
    claim:
      'The branch signs under `002-H-X` should be parsed first as function classes, not as a list of names.',
    support: roleRows.map((row) => `${row.sign}:${row.provisional_role}`).join('; '),
    prediction:
      'A name-list model wins only if X signs become object/site-specific and stop carrying stable open/terminal behavior across heads and registers.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'EXPAND',
  status: 'x_function_role_bets',
  role_rows: roleRows,
  new_bets: Object.fromEntries(bets.map((row) => [row.bet_id, row.tier])),
  predictions: [
    '`125` should behave like a dependent-tail operator in X slots.',
    '`095` and `705` should behave like terminal class labels across sites/registers.',
    '`692` should be treated as a weak payload bet because raw terminal prior can explain it.',
    '`590` is the next open-extender sign to try to break.',
  ],
};

writeCsv(path.join(reportsDir, `${prefix}_role_summary.csv`), roleRows, [
  'checked_date',
  'sign',
  'provisional_role',
  'global_occurrences',
  'global_terminal_rate',
  'x_slot_rows',
  'x_slot_open_rate',
  'x_slot_terminal_rate',
  'x_slot_heads',
  'x_slot_sites',
  'x_slot_scopes',
  'x_slot_tails',
  'x_slot_objects',
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
