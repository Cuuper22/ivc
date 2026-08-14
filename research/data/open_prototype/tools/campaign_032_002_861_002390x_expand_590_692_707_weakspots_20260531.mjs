import fs from 'node:fs';
import path from 'node:path';

// This script attacks the three weakest X signs in the 002 frame — 590, 692,
// and 707 — where the row counts are so small that any claim is fragile. It
// reads lipi/metadata_filtered.csv, deduplicates by sign sequence, and
// gathers two views: every occurrence of the three signs anywhere (with two
// signs of left context and terminal status) and every 002-HEAD-X frame where
// one of them fills the X slot. From those rows it stakes three explicitly
// thin bets: 590 is a head-routed extender (heads 390/798 route it to 032,
// 392 to 125, 368 to 900, while 125/540/705 close), 692 is terminal by
// default with a single head-455-licenses-416 exception, and 707 is only
// "terminal bait" — one X-slot row, so its sole use is a prediction about the
// next 002-H-707. Each bet self-downgrades to "too_small" if its counts do
// not match. Writes X-slot rows, raw occurrences, and bets as CSVs plus a
// summary JSON to data/open_prototype/reports.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_590_692_707_weakspots_20260531';
const checkedDate = '2026-05-31';
const weakXs = new Set(['590', '692', '707']);

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
  return [...String(text || '').matchAll(/\d{3}/g)].map((match) => match[0]);
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function ratio(numerator, denominator) {
  return denominator ? `${numerator}/${denominator}` : '0/0';
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

function uniqueRowsByText(rows) {
  return [...new Map(rows.map((row) => [row.tokens.join(' '), row])).values()];
}

function examples(rows, n = 8) {
  return rows
    .slice(0, n)
    .map((row) => `${row.object}:${row.text}`)
    .join(' | ');
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = uniqueRowsByText(
  parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
    ...row,
    object: objectId(row),
    tokens: signs(row.text),
  })),
);

const xRows = [];
const occurrences = [];
for (const row of rows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
    if (weakXs.has(row.tokens[i])) {
      occurrences.push({
        checked_date: checkedDate,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        shape: row.shape,
        material: row.material,
        sign: row.tokens[i],
        left_2: row.tokens[i - 2] ?? '<START>',
        left_1: row.tokens[i - 1] ?? '<START>',
        right_1: row.tokens[i + 1] ?? '<END>',
        terminal: String(i === row.tokens.length - 1),
        tail_after_sign: row.tokens.slice(i + 1).join(' ') || '<END>',
        in_002_xslot: String(row.tokens[i - 2] === '002'),
        text: row.text,
      });
    }
    if (row.tokens[i] !== '002' || i + 2 >= row.tokens.length || !weakXs.has(row.tokens[i + 2])) continue;
    const tail = row.tokens.slice(i + 3);
    xRows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      head: row.tokens[i + 1],
      x: row.tokens[i + 2],
      tail_after_x: tail.join(' ') || '<END>',
      first_after_x: tail[0] ?? '<END>',
      open: String(tail.length > 0),
      text: row.text,
    });
  }
}

const rows590 = xRows.filter((row) => row.x === '590');
const rows692 = xRows.filter((row) => row.x === '692');
const rows707 = xRows.filter((row) => row.x === '707');
const rows590To032 = rows590.filter((row) => row.first_after_x === '032');
const rows692Terminal = rows692.filter((row) => row.open === 'false');
const rows692Open = rows692.filter((row) => row.open === 'true');
const occ707 = occurrences.filter((row) => row.sign === '707');

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_590_HEAD_ROUTED_EXTENDER',
    tier: rows590.length >= 7 && rows590To032.length === 2 ? 'wild_shot' : 'too_small',
    risky_bet:
      '`590` is a head-routed extender, not a value: heads `390/798` route it to `032`, `392` routes it to `125`, `368` routes it to `900`, while `125/540/705` close.',
    current_test:
      `rows=${rows590.length}; head->tail=${rows590.map((row) => `${row.head}->${row.first_after_x}`).join(';')}; to032=${ratio(rows590To032.length, rows590.length)}.`,
    evidence: examples(rows590),
    destructive_prediction:
      'A second `002-390-590` that does not go to `032`, or many unrelated `H-590-032` rows, kills the routed-extender bet.',
    promotion_prediction:
      'Another `390/798-590-032` row, especially source-strict, promotes `590-032` as a route rather than an accident.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_692_HEAD455_416_EXCEPTION',
    tier: rows692.length === 3 && rows692Open.length === 1 ? 'wild_shot' : 'too_small',
    risky_bet:
      '`692` is terminal by default in X-slot, except head `455` licenses a following `416` continuation.',
    current_test:
      `692 rows=${rows692.length}; terminal=${ratio(rows692Terminal.length, rows692.length)}; open=${rows692Open.map((row) => `${row.object}:${row.head}-692-${row.first_after_x}`).join(';')}.`,
    evidence: examples(rows692),
    destructive_prediction:
      'Any `002-390-692-Y` continuation or a second non-455 open tail makes the exception model collapse.',
    promotion_prediction:
      'Another `455-692-416` row or terminal rows under unrelated heads promotes a weak 692 default/exception rule.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_707_TERMINAL_CLASS_BAIT',
    tier: rows707.length === 1 && occ707.length >= 1 ? 'wild_shot' : 'too_small',
    risky_bet:
      '`707` is terminal-bait under `390`, but there is not enough X-slot evidence; the only useful prediction is that a future `002-H-707` should close unless a head-specific exception appears.',
    current_test:
      `X-slot 707 rows=${rows707.length}; all 707 occurrences=${occ707.length}; occurrence terminal=${ratio(occ707.filter((row) => row.terminal === 'true').length, occ707.length)}.`,
    evidence: `${examples(rows707)} || all ${examples(occ707)}`,
    destructive_prediction:
      'A future `002-H-707-Y` continuation prevents `707` from entering the terminal class portfolio.',
    promotion_prediction:
      'Two more closed `002-H-707` rows under non-390 heads promote it from bait to terminal-class candidate.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'weakspot_bets_590_692_707',
  rows: {
    weak_x_rows: xRows.length,
    rows590: rows590.length,
    rows692: rows692.length,
    rows707: rows707.length,
    all707Occurrences: occ707.length,
  },
  bets: betRows.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

writeCsv(path.join(reportsDir, `${prefix}_x_rows.csv`), xRows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'shape',
  'material',
  'head',
  'x',
  'tail_after_x',
  'first_after_x',
  'open',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_occurrences.csv`), occurrences, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'shape',
  'material',
  'sign',
  'left_2',
  'left_1',
  'right_1',
  'terminal',
  'tail_after_sign',
  'in_002_xslot',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), betRows, [
  'checked_date',
  'bet_id',
  'tier',
  'risky_bet',
  'current_test',
  'evidence',
  'destructive_prediction',
  'promotion_prediction',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
