import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_consolidate_095_context_contrast_20260531';
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
    if (row.tokens[i] !== '095') continue;
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
      context: inXSlot ? '002_H_095_Xslot' : 'non_002_Xslot',
      head_if_xslot: inXSlot ? row.tokens[i - 1] : '',
      left_1: row.tokens[i - 1] ?? '<START>',
      left_2: row.tokens[i - 2] ?? '<START>',
      right_1: row.tokens[i + 1] ?? '<END>',
      terminal: String(terminal),
      tail_after_095: row.tokens.slice(i + 1).join(' ') || '<END>',
      text: row.text,
    });
  }
}

const xSlotRows = occurrences.filter((row) => row.context === '002_H_095_Xslot');
const nonXRows = occurrences.filter((row) => row.context !== '002_H_095_Xslot');
const xTerminal = xSlotRows.filter((row) => row.terminal === 'true').length;
const nonXTerminal = nonXRows.filter((row) => row.terminal === 'true').length;

const contrastRows = [
  {
    checked_date: checkedDate,
    context: '002_H_095_Xslot',
    rows: String(xSlotRows.length),
    terminal: ratio(xTerminal, xSlotRows.length),
    terminal_share: pct(xTerminal, xSlotRows.length),
    heads: countBy(xSlotRows, (row) => row.head_if_xslot),
    sites: countBy(xSlotRows, (row) => row.site),
    right_1: countBy(xSlotRows, (row) => row.right_1),
    decision: 'clean_context_terminal',
  },
  {
    checked_date: checkedDate,
    context: 'non_002_Xslot',
    rows: String(nonXRows.length),
    terminal: ratio(nonXTerminal, nonXRows.length),
    terminal_share: pct(nonXTerminal, nonXRows.length),
    heads: countBy(nonXRows, (row) => row.left_1),
    sites: countBy(nonXRows, (row) => row.site),
    right_1: countBy(nonXRows, (row) => row.right_1),
    decision: 'raw_sign_not_terminal_enough',
  },
];

const decisions = [
  {
    checked_date: checkedDate,
    candidate: 'X095_TERMINAL_CLASS_LABEL',
    decision: 'keep_rank1_candidate_not_promoted',
    evidence:
      `X-slot terminal=${ratio(xTerminal, xSlotRows.length)}; non-X-slot terminal=${ratio(nonXTerminal, nonXRows.length)}; ` +
      `X heads=${countBy(xSlotRows, (row) => row.head_if_xslot)}; X sites=${countBy(xSlotRows, (row) => row.site)}.`,
    consequence:
      '`095` is better modeled as a context-bound terminal class-label than as a raw terminal sign, but the X-slot sample is still only three rows.',
  },
  {
    checked_date: checkedDate,
    candidate: 'SIGN095_RAW_TERMINAL_VALUE',
    decision: 'kill',
    evidence: `All 095 occurrences terminal=${ratio(xTerminal + nonXTerminal, occurrences.length)}; non-X-slot terminal=${ratio(nonXTerminal, nonXRows.length)}.`,
    consequence:
      'Do not assign `095` a free-standing terminal value or translation. The risky bet remains slot-function only.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: 'consolidate_095_context_contrast',
  rows: {
    all_095_occurrences: occurrences.length,
    xslot_095_occurrences: xSlotRows.length,
    xslot_095_terminal: xTerminal,
    non_xslot_095_occurrences: nonXRows.length,
    non_xslot_095_terminal: nonXTerminal,
  },
  decisions,
  compressed_read:
    '`095` remains rank 1 because terminality concentrates in the `002-H-095` slot, not because `095` has a free-standing terminal value.',
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
  'tail_after_095',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_contrast_rows.csv`), contrastRows, [
  'checked_date',
  'context',
  'rows',
  'terminal',
  'terminal_share',
  'heads',
  'sites',
  'right_1',
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
