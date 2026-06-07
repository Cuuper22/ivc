import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_consolidate_530_open_control_20260531';
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

function ratio(numerator, denominator) {
  return denominator ? `${numerator}/${denominator}` : '0/0';
}

function uniqueRowsByText(rows) {
  return [...new Map(rows.map((row) => [row.tokens.join(' '), row])).values()];
}

function findPatternRows(rows, pattern) {
  const hits = [];
  for (const row of rows) {
    for (let i = 0; i <= row.tokens.length - pattern.length; i += 1) {
      if (pattern.every((token, offset) => row.tokens[i + offset] === token)) {
        hits.push(row);
        break;
      }
    }
  }
  return hits;
}

function governedRows(rows, xSign) {
  const hits = [];
  for (const row of rows) {
    for (let i = 0; i < row.tokens.length - 2; i += 1) {
      if (row.tokens[i] !== '002' || row.tokens[i + 2] !== xSign) continue;
      const tail = row.tokens.slice(i + 3);
      const head = row.tokens[i + 1];
      const complement = tail[0] ?? '<END>';
      const directShadows =
        complement === '<END>' ? [] : findPatternRows(rows, ['002', head, complement]);
      hits.push({
        checked_date: checkedDate,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        shape: row.shape,
        material: row.material,
        head_after_002: head,
        x: xSign,
        first_after_x: complement,
        tail_after_x: tail.join(' ') || '<END>',
        tail_after_first: tail.slice(1).join(' ') || '<END>',
        tail_length_after_x: String(tail.length),
        one_complement_then_end: String(tail.length === 1),
        direct_shadow_count: String(directShadows.length),
        direct_shadow_objects: directShadows.map((shadow) => shadow.object).join(';'),
        text: row.text,
      });
    }
  }
  return hits;
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = uniqueRowsByText(
  parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
    ...row,
    object: objectId(row),
    tokens: signs(row.text),
  })),
);

const rows530 = governedRows(rows, '530');
const rows125 = governedRows(rows, '125');

const oneComplement530 = rows530.filter((row) => row.one_complement_then_end === 'true').length;
const oneComplement125 = rows125.filter((row) => row.one_complement_then_end === 'true').length;
const terminal125 = rows125.filter((row) => row.tail_after_x === '<END>').length;
const directShadow530 = rows530.filter((row) => row.direct_shadow_count !== '0').length;
const directShadow390530741 = findPatternRows(rows, ['002', '390', '741']).length;

const comparisonRows = [
  {
    checked_date: checkedDate,
    x: '530',
    rows: String(rows530.length),
    open_after_x: ratio(rows530.filter((row) => row.tail_after_x !== '<END>').length, rows530.length),
    one_complement_then_end: ratio(oneComplement530, rows530.length),
    direct_shadow_rows: ratio(directShadow530, rows530.length),
    heads: countBy(rows530, (row) => row.head_after_002),
    first_after_x: countBy(rows530, (row) => row.first_after_x),
    tail_after_first: countBy(rows530, (row) => row.tail_after_first),
    decision: 'one_complement_linker_candidate',
  },
  {
    checked_date: checkedDate,
    x: '125',
    rows: String(rows125.length),
    open_after_x: ratio(rows125.filter((row) => row.tail_after_x !== '<END>').length, rows125.length),
    one_complement_then_end: ratio(oneComplement125, rows125.length),
    direct_shadow_rows: ratio(rows125.filter((row) => row.direct_shadow_count !== '0').length, rows125.length),
    heads: countBy(rows125, (row) => row.head_after_002),
    first_after_x: countBy(rows125, (row) => row.first_after_x),
    tail_after_first: countBy(rows125, (row) => row.tail_after_first),
    decision: 'different_from_530_tail_menu_operator',
  },
];

const decisions = [
  {
    checked_date: checkedDate,
    candidate: 'X530_OPEN_OPERATOR_CONTROL',
    decision: 'keep_but_rename_to_one_complement_linker',
    evidence:
      `530 rows=${rows530.length}; open=${ratio(rows530.filter((row) => row.tail_after_x !== '<END>').length, rows530.length)}; ` +
      `one_complement_then_end=${ratio(oneComplement530, rows530.length)}; ` +
      `heads=${countBy(rows530, (row) => row.head_after_002)}; first_after_x=${countBy(rows530, (row) => row.first_after_x)}; ` +
      `direct_shadow_rows=${ratio(directShadow530, rows530.length)}.`,
    consequence:
      '`530` is not a generic open class. In this campaign it is a one-complement linker/control: it opens exactly one slot and then closes.',
  },
  {
    checked_date: checkedDate,
    candidate: 'X530_AS_125_PEER',
    decision: 'kill',
    evidence:
      `530 one-complement=${ratio(oneComplement530, rows530.length)} versus 125 one-complement=${ratio(oneComplement125, rows125.length)}; ` +
      `125 terminal=${ratio(terminal125, rows125.length)} and has multi-sign tails.`,
    consequence:
      '`530` cannot be merged with `125`; it becomes the clean control that proves open X signs can have different operator subtypes.',
  },
  {
    checked_date: checkedDate,
    candidate: 'H773_390_530_741',
    decision: 'keep_as_subcase_only',
    evidence: `direct 002-390-741 shadows=${directShadow390530741}; governed row H-773 has 002-390-530-741.`,
    consequence:
      'H-773 supports `530` as a separable linker, but it is not a stand-alone translation claim.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: 'consolidate_530_open_control',
  rows: {
    governed_530: rows530.length,
    governed_125: rows125.length,
    governed_530_one_complement_then_end: oneComplement530,
    governed_125_one_complement_then_end: oneComplement125,
    governed_530_direct_shadow_rows: directShadow530,
    direct_002390741_shadow_rows: directShadow390530741,
  },
  decisions,
  compressed_read:
    '`530` survives, but only after being narrowed from open class to one-complement linker/control. It is not a peer of `125`.',
};

writeCsv(path.join(reportsDir, `${prefix}_target_rows.csv`), rows530, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'shape',
  'material',
  'head_after_002',
  'x',
  'first_after_x',
  'tail_after_x',
  'tail_after_first',
  'tail_length_after_x',
  'one_complement_then_end',
  'direct_shadow_count',
  'direct_shadow_objects',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_comparison_rows.csv`), comparisonRows, [
  'checked_date',
  'x',
  'rows',
  'open_after_x',
  'one_complement_then_end',
  'direct_shadow_rows',
  'heads',
  'first_after_x',
  'tail_after_first',
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
