// Models sign 705 as "terminal by default, with a named exception" instead of a
// clean terminal class. Like 095, sign 705 usually ends inscriptions when it
// occupies the X slot of a 002-H-705 frame — but unlike 095 it has at least one
// X-slot row that keeps going (the 320-705-125 shape). This script deduplicates
// the local Lipi metadata by sign text, collects every 705 occurrence with its
// neighbors and X-slot status, contrasts X-slot rows against all occurrences,
// and names each open exception explicitly. Writes occurrences, contrast, and
// decisions CSVs plus a summary JSON to data/open_prototype/reports/. Recorded
// verdicts: keep 705 as a terminal-default class ranked below 095 and 530;
// kill the "clean terminal peer of 095" bundling; and register the unbound
// Dholavira 002-390-705 candidate as a destructive prediction — if it ever
// source-binds and continues after 705, the class is demoted.

import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_consolidate_705_exception_model_20260531';
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

function signs(text) {
  return [...String(text || '').matchAll(/\d{3}/g)].map((match) => match[0]);
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function ratio(numerator, denominator) {
  return denominator ? `${numerator}/${denominator}` : '0/0';
}

function pct(numerator, denominator) {
  return denominator ? (numerator / denominator).toFixed(6) : '';
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

fs.mkdirSync(reportsDir, { recursive: true });

const rows = uniqueRowsByText(
  parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
    ...row,
    object: objectId(row),
    tokens: signs(row.text),
  })),
);

const occurrences = [];
for (const row of rows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
    if (row.tokens[i] !== '705') continue;
    const inXSlot = row.tokens[i - 2] === '002';
    const terminal = i === row.tokens.length - 1;
    occurrences.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      context: inXSlot ? '002_H_705_Xslot' : 'non_002_Xslot',
      head_if_xslot: inXSlot ? row.tokens[i - 1] : '',
      left_1: row.tokens[i - 1] ?? '<START>',
      left_2: row.tokens[i - 2] ?? '<START>',
      right_1: row.tokens[i + 1] ?? '<END>',
      terminal: String(terminal),
      tail_after_705: row.tokens.slice(i + 1).join(' ') || '<END>',
      exception_shape: inXSlot && !terminal ? `${row.tokens[i - 1]}-705-${row.tokens[i + 1]}` : '',
      text: row.text,
    });
  }
}

const xSlotRows = occurrences.filter((row) => row.context === '002_H_705_Xslot');
const xTerminal = xSlotRows.filter((row) => row.terminal === 'true').length;
const xOpen = xSlotRows.length - xTerminal;
const exceptionRows = xSlotRows.filter((row) => row.terminal !== 'true');

const contrastRows = [
  {
    checked_date: checkedDate,
    context: '002_H_705_Xslot',
    rows: String(xSlotRows.length),
    terminal: ratio(xTerminal, xSlotRows.length),
    terminal_share: pct(xTerminal, xSlotRows.length),
    open: ratio(xOpen, xSlotRows.length),
    heads: countBy(xSlotRows, (row) => row.head_if_xslot),
    tails: countBy(xSlotRows, (row) => row.tail_after_705),
    sites: countBy(xSlotRows, (row) => row.site),
    decision: 'terminal_default_with_exception',
  },
  {
    checked_date: checkedDate,
    context: '705_all_occurrences',
    rows: String(occurrences.length),
    terminal: ratio(occurrences.filter((row) => row.terminal === 'true').length, occurrences.length),
    terminal_share: pct(occurrences.filter((row) => row.terminal === 'true').length, occurrences.length),
    open: ratio(occurrences.filter((row) => row.terminal !== 'true').length, occurrences.length),
    heads: countBy(occurrences, (row) => row.left_1),
    tails: countBy(occurrences, (row) => row.tail_after_705),
    sites: countBy(occurrences, (row) => row.site),
    decision: 'raw_terminal_pressure_high_but_not_interpretive',
  },
];

const decisions = [
  {
    checked_date: checkedDate,
    candidate: 'X705_TERMINAL_DEFAULT_CLASS',
    decision: 'keep_narrowed_below_095_and_530',
    evidence:
      `X-slot terminal=${ratio(xTerminal, xSlotRows.length)}; X heads=${countBy(xSlotRows, (row) => row.head_if_xslot)}; ` +
      `tails=${countBy(xSlotRows, (row) => row.tail_after_705)}; exception=${exceptionRows.map((row) => `${row.object}:${row.exception_shape}`).join(';')}.`,
    consequence:
      '`705` is a terminal-default X-slot class with a named `320-705-125` exception. It is not a clean peer of `095`.',
  },
  {
    checked_date: checkedDate,
    candidate: 'X705_CLEAN_TERMINAL_CLASS',
    decision: 'kill',
    evidence: `X-slot open exceptions=${ratio(xOpen, xSlotRows.length)}.`,
    consequence:
      'Do not bundle `705` with `095` as an equally clean terminal class.',
  },
  {
    checked_date: checkedDate,
    candidate: 'DHOLAVIRA_390_705_PARSE_PREDICTION',
    decision: 'define_as_destructive_prediction_not_proof',
    evidence: 'Current X-slot 390-705 rows are terminal in the deduped metadata; the unbound Dholavira candidate would matter only by testing that prediction.',
    consequence:
      'If Dholavira item 10 source-binds as `002-390-705` and closes, it supports terminal-default. If it continues after `705`, it demotes the class.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: 'consolidate_705_exception_model',
  rows: {
    all_705_occurrences: occurrences.length,
    xslot_705_occurrences: xSlotRows.length,
    xslot_705_terminal: xTerminal,
    xslot_705_open_exceptions: xOpen,
    xslot_705_exception_objects: exceptionRows.map((row) => row.object),
  },
  decisions,
  compressed_read:
    '`705` survives only as terminal-default with a named exception. It is below `095` and `530`, and Dholavira can only test this prediction.',
};

writeCsv(path.join(reportsDir, `${prefix}_occurrences.csv`), occurrences, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'shape',
  'material',
  'context',
  'head_if_xslot',
  'left_1',
  'left_2',
  'right_1',
  'terminal',
  'tail_after_705',
  'exception_shape',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_contrast_rows.csv`), contrastRows, [
  'checked_date',
  'context',
  'rows',
  'terminal',
  'terminal_share',
  'open',
  'heads',
  'tails',
  'sites',
  'decision',
]);

writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  'checked_date',
  'candidate',
  'decision',
  'evidence',
  'consequence',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
