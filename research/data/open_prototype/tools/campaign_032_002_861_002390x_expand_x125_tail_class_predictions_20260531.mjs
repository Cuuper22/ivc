import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const x125RowsPath = path.join(reportsDir, 'campaign_032_002_861_002390x_expand_x125_scope_split_20260531_x125_global_rows.csv');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_expand_x125_tail_class_predictions_20260531';

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

function tailClass(tail) {
  if (tail === '<END>') return 'terminal_125';
  if (tail === '032') return 'single_032_tail';
  if (tail.startsWith('632 032')) return '632032_tail_family';
  if (tail === '820') return '820_terminal_cap_tail';
  if (tail === '195') return 'single_195_tail';
  if (tail === '590 831') return 'copper_590831_tail';
  return 'other_tail';
}

fs.mkdirSync(reportsDir, { recursive: true });

const x125Rows = parseCsv(fs.readFileSync(x125RowsPath, 'utf8')).map((row) => ({
  ...row,
  tail_class: tailClass(row.tail_after_x),
  open_or_terminal: row.x_continuing === 'True' ? 'open' : 'terminal',
}));

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));
const tailOccurrences = [];
for (const row of metadataRows) {
  const rowSigns = signs(row.text);
  for (let index = 0; index < rowSigns.length; index += 1) {
    if (rowSigns[index] !== '125') continue;
    const tail = rowSigns.slice(index + 1).join(' ') || '<END>';
    tailOccurrences.push({
      checked_date: '2026-05-31',
      object: row.cisi,
      id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      role: index >= 2 && rowSigns[index - 2] === '002' ? 'xslot_125' : 'non_xslot_125',
      head_if_xslot: index >= 2 && rowSigns[index - 2] === '002' ? rowSigns[index - 1] : '',
      terminal: index === rowSigns.length - 1 ? 'True' : 'False',
      tail_after_125: tail,
      tail_class: tailClass(tail),
      text: row.text,
    });
  }
}

const openRows = x125Rows.filter((row) => row.open_or_terminal === 'open');
const terminalRows = x125Rows.filter((row) => row.open_or_terminal === 'terminal');
const headTailSummary = countBy(x125Rows, (row) => row.head_after_002).map(([head, count]) => {
  const rows = x125Rows.filter((row) => row.head_after_002 === head);
  const open = rows.filter((row) => row.open_or_terminal === 'open').length;
  return {
    checked_date: '2026-05-31',
    head,
    rows: String(count),
    open_rate: ratio(open, count),
    tails: topCounts(rows, (row) => row.tail_after_x),
    tail_classes: topCounts(rows, (row) => row.tail_class),
    scopes: topCounts(rows, (row) => row.scope_cell),
    objects: rows.map((row) => row.object).join(';'),
    prediction:
      head === '610'
        ? 'next xslot 125 under head 610 should continue with 032 tail'
        : head === '390'
          ? 'next xslot 125 under head 390 should continue, tail may split by left/register'
          : head === '861' || head === '906'
            ? 'next xslot 125 under this terminal head should end'
            : 'singleton head: predict by tail class only',
  };
});

const tailClassSummary = countBy(x125Rows, (row) => row.tail_class).map(([tail_class, count]) => {
  const rows = x125Rows.filter((row) => row.tail_class === tail_class);
  const open = rows.filter((row) => row.open_or_terminal === 'open').length;
  const globalSameTail = tailOccurrences.filter((row) => row.tail_class === tail_class);
  return {
    checked_date: '2026-05-31',
    tail_class,
    xslot_rows: String(count),
    xslot_open_rate: ratio(open, count),
    heads: topCounts(rows, (row) => row.head_after_002),
    scopes: topCounts(rows, (row) => row.scope_cell),
    global_125_rows_same_tail_class: String(globalSameTail.length),
    global_roles: topCounts(globalSameTail, (row) => row.role),
    objects: rows.map((row) => row.object).join(';'),
  };
});

const bets = [
  {
    checked_date: '2026-05-31',
    bet_id: 'X125_HEAD610_SELECTS_032_TAIL',
    tier: 'candidate',
    claim:
      '`002-610-125` selects tail `032` across sites; current witnesses are H-74 and M-1665.',
    support: headTailSummary.find((row) => row.head === '610')?.tails ?? '',
    prediction:
      'A future `002-610-125` row should continue as `125-032`; terminal `125`, `125-820`, or `125-632-032` under 610 kills this selection bet.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'X125_632032_DEPENDENT_TAIL_FAMILY',
    tier: 'wild shot',
    claim:
      '`125-632-032` is a dependent-tail family shared by heads `190` and `390`, with `900-563` as an optional extension rather than a separate parse.',
    support: `xslot 632032 rows=${openRows.filter((row) => row.tail_class === '632032_tail_family').map((row) => `${row.object}:${row.head_after_002}->${row.tail_after_x}`).join(';')}`,
    prediction:
      'A new `125-632-032` tail should occur after an open X=125 head; free non-Xslot spread demotes this to copied formula.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'X125_820_CAP_IS_NOT_ONE_THING',
    tier: 'wild shot',
    claim:
      '`125-820` is not a single value: under `405`/possibly Surkotada `390` it is an open dependent tail, while terminal/non-Xslot uses of `820` are a broader cap background.',
    support: `xslot 820 rows=${x125Rows.filter((row) => row.tail_class === '820_terminal_cap_tail').map((row) => `${row.object}:${row.head_after_002}:${row.open_or_terminal}`).join(';')}`,
    prediction:
      'If source-bound `002-405-125-820` or Sktd-1 lose continuation, kill the dependent-tail reading and keep only cap pressure.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'X125_TAILS_ARE_PARSER_FEATURES_NOT_TRANSLATIONS',
    tier: 'candidate',
    claim:
      'The tail after X-slot `125` is a parser feature conditioned by head/scope; none of `032`, `632-032`, `820`, `195`, or `590-831` is a translation value yet.',
    support: `tail_classes=${topCounts(x125Rows, (row) => row.tail_class)}`,
    prediction:
      'Future rows should preserve head/scope-conditioned tail choices better than a global sign-value table; if not, kill tail morphology.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'EXPAND',
  status: 'x125_tail_class_predictions',
  xslot_125_rows: x125Rows.length,
  xslot_open_rows: openRows.length,
  xslot_terminal_rows: terminalRows.length,
  head_tail_summary: headTailSummary,
  tail_class_summary: tailClassSummary,
  new_bets: Object.fromEntries(bets.map((row) => [row.bet_id, row.tier])),
  most_embarrassing_tests: [
    'Find `002-610-125` with any tail other than `032`.',
    'Find source-visible free non-Xslot `125-632-032` spread that ignores head/scope.',
    'Source-bind `002-405-125-820` and Sktd-1; if either loses continuation, kill the 820 dependent-tail bet.',
  ],
};

writeCsv(path.join(reportsDir, `${prefix}_x125_tail_rows.csv`), x125Rows, [
  'checked_date',
  'object',
  'id',
  'site',
  'type',
  'shape',
  'material',
  'symbol',
  'cult',
  'prev_before_002',
  'head_after_002',
  'x_after_head',
  'x_continuing',
  'x_terminal',
  'tail_after_x',
  'tail_class',
  'open_or_terminal',
  'scope_cell',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_head_tail_summary.csv`), headTailSummary, [
  'checked_date',
  'head',
  'rows',
  'open_rate',
  'tails',
  'tail_classes',
  'scopes',
  'objects',
  'prediction',
]);

writeCsv(path.join(reportsDir, `${prefix}_tail_class_summary.csv`), tailClassSummary, [
  'checked_date',
  'tail_class',
  'xslot_rows',
  'xslot_open_rate',
  'heads',
  'scopes',
  'global_125_rows_same_tail_class',
  'global_roles',
  'objects',
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
