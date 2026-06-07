import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_125_order_discriminator_20260531';
const checkedDate = '2026-05-31';
const complements = new Set(['632', '032', '820', '195', '590']);

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

function classifyOrder(signs) {
  const index390 = signs.indexOf('390');
  const index125 = signs.indexOf('125');
  const compPositions = signs
    .map((sign, index) => ({ sign, index }))
    .filter((item) => complements.has(item.sign));
  if (index390 === -1 || index125 === -1 || compPositions.length === 0) return 'not_comparable';
  const firstComp = compPositions[0].index;
  if (index390 < index125 && index125 < firstComp) return 'head_linker_complement';
  if (firstComp < index125 && index125 < index390) return 'complement_linker_head';
  if (firstComp < index390 && index390 < index125) return 'complement_head_linker';
  if (index390 < firstComp && firstComp < index125) return 'head_complement_linker';
  return 'mixed_or_repeated';
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));

const comparableRows = rows
  .filter((row) => row.signs.includes('390') && row.signs.includes('125') && row.signs.some((sign) => complements.has(sign)))
  .map((row) => {
    const compSigns = row.signs.filter((sign) => complements.has(sign));
    return {
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      order_class: classifyOrder(row.signs),
      index_390: row.signs.indexOf('390'),
      index_125: row.signs.indexOf('125'),
      complement_signs: compSigns.join('-'),
      text: row.text,
    };
  });

const frameLocalRows = [];
for (const row of rows) {
  for (let i = 0; i < row.signs.length - 3; i += 1) {
    if (row.signs[i] !== '002' || row.signs[i + 1] !== '390' || row.signs[i + 2] !== '125') continue;
    const frameTail = row.signs.slice(i + 3);
    frameLocalRows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      frame_start_index: i,
      frame_tail: frameTail.join('-') || '<END>',
      first_frame_complement: frameTail.find((sign) => complements.has(sign)) ?? '',
      local_order_class: frameTail.some((sign) => complements.has(sign))
        ? 'frame_head_linker_complement'
        : 'frame_head_linker_no_known_complement',
      broad_order_class: classifyOrder(row.signs),
      text: row.text,
    });
  }
}

const orderCounts = new Map();
for (const row of comparableRows) {
  orderCounts.set(row.order_class, (orderCounts.get(row.order_class) ?? 0) + 1);
}

const orderRows = [...orderCounts.entries()]
  .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
  .map(([orderClass, count]) => ({
    checked_date: checkedDate,
    order_class: orderClass,
    occurrences: count,
    objects: comparableRows
      .filter((row) => row.order_class === orderClass)
      .map((row) => row.object)
      .join(';'),
    decision:
      orderClass === 'head_linker_complement'
        ? 'supports 390-125 as head-linker-complement syntax'
        : 'dangerous reversal or mixed order; inspect before using family discriminator',
  }));

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_125_HEAD_LINKER_COMPLEMENT_ORDER',
    tier: 'wild shot',
    claim:
      '390-125-COMP is a head-linker-complement order, not a loose bag of repeated signs.',
    risky_prediction:
      'Rows containing 390, 125, and complement signs should overwhelmingly use 390 before 125 before complement.',
    kill_condition:
      'Complement-before-head or mixed orders occur freely in comparable rows.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_LANGUAGE_FAMILY_DISCRIMINATOR_ORDER',
    tier: 'wild shot',
    claim:
      'If 125 is a genitive/associative linker, this micro-system gives a syntax discriminator: head plus linker plus complement.',
    risky_prediction:
      'Future source-visible expansions should preserve head-linker-complement order in 390 status/title phrases.',
    kill_condition:
      'Held-out rows show the complement preceding 390 with the same 125 linker function.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: '125_order_discriminator',
  comparable_rows: comparableRows.length,
  order_counts: Object.fromEntries(orderRows.map((row) => [row.order_class, Number(row.occurrences)])),
  frame_local_002_390_125_rows: frameLocalRows.length,
  frame_local_with_known_complement: frameLocalRows.filter(
    (row) => row.local_order_class === 'frame_head_linker_complement',
  ).length,
  provisional_read:
    'Frame-local 002-390-125 rows support head-linker-complement, but broad 390/125/complement rows are mixed and block any language-family promotion.',
};

writeCsv(path.join(reportsDir, `${prefix}_comparable_rows.csv`), comparableRows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'order_class',
  'index_390',
  'index_125',
  'complement_signs',
  'text',
]);
writeCsv(path.join(reportsDir, `${prefix}_order_rows.csv`), orderRows, [
  'checked_date',
  'order_class',
  'occurrences',
  'objects',
  'decision',
]);
writeCsv(path.join(reportsDir, `${prefix}_frame_local_rows.csv`), frameLocalRows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'frame_start_index',
  'frame_tail',
  'first_frame_complement',
  'local_order_class',
  'broad_order_class',
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
