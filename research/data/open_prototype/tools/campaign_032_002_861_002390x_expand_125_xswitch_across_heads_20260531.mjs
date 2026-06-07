import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const framesPath = path.join(reportsDir, 'campaign_032_002_861_002390x_expand_002_head_class_discriminator_20260531_frames.csv');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_expand_125_xswitch_across_heads_20260531';

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
    const key = keyFn(row) || '<END>';
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

const frames = parseCsv(fs.readFileSync(framesPath, 'utf8'));
const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));
const sameRegisterRows = metadataRows.filter(
  (row) =>
    row.site === 'Mohenjo-daro' &&
    row.type === 'SEAL:S' &&
    row.shape === 'square' &&
    row.material === 'Steatite',
);

const x125Rows = frames
  .filter((row) => row.x_after_head === '125')
  .map((row) => ({
    checked_date: '2026-05-31',
    object: row.object,
    id: row.id,
    prev_before_002: row.prev_before_002,
    head_after_002: row.head_after_002,
    x_after_head: row.x_after_head,
    x_continuing: row.x_continuing,
    x_terminal: row.x_terminal,
    tail_after_x: row.tail_after_x,
    symbol: row.symbol,
    cult: row.cult,
    text: row.text,
  }));

const non125XRows = frames.filter((row) => row.takes_x === 'True' && row.x_after_head !== '125');
const all125Occurrences = [];
for (const row of sameRegisterRows) {
  const rowSigns = signs(row.text);
  for (let index = 0; index < rowSigns.length; index += 1) {
    if (rowSigns[index] !== '125') continue;
    const post002X = index >= 2 && rowSigns[index - 2] === '002';
    all125Occurrences.push({
      checked_date: '2026-05-31',
      object: row.cisi,
      id: row.id,
      occurrence_role: post002X ? 'post_002_h_x125' : 'non_xslot_125',
      head_if_xslot: post002X ? rowSigns[index - 1] : '',
      prev2: rowSigns[index - 2] ?? '',
      prev: rowSigns[index - 1] ?? '',
      next: rowSigns[index + 1] ?? '',
      terminal: index === rowSigns.length - 1 ? 'True' : 'False',
      continuing: index < rowSigns.length - 1 ? 'True' : 'False',
      symbol: row.symbol,
      cult: row.cult,
      complete: row.complete,
      condition: row.condition,
      text: row.text,
    });
  }
}

const xslot125Occurrences = all125Occurrences.filter((row) => row.occurrence_role === 'post_002_h_x125');
const nonXslot125Occurrences = all125Occurrences.filter((row) => row.occurrence_role === 'non_xslot_125');
const x125Open = x125Rows.filter((row) => row.x_continuing === 'True').length;
const non125Open = non125XRows.filter((row) => row.x_continuing === 'True').length;
const nonXslot125Continuing = nonXslot125Occurrences.filter((row) => row.continuing === 'True').length;

const contrastRows = [
  {
    checked_date: '2026-05-31',
    contrast: 'post_002_h_x125',
    denominator: String(x125Rows.length),
    continuing: String(x125Open),
    continuing_rate: ratio(x125Open, x125Rows.length),
    terminal: String(x125Rows.length - x125Open),
    heads: topCounts(x125Rows, (row) => row.head_after_002),
    tails: topCounts(x125Rows, (row) => row.tail_after_x),
    decision: 'candidate_sufficient_continuation_switch',
  },
  {
    checked_date: '2026-05-31',
    contrast: 'post_002_h_non125_x',
    denominator: String(non125XRows.length),
    continuing: String(non125Open),
    continuing_rate: ratio(non125Open, non125XRows.length),
    terminal: String(non125XRows.length - non125Open),
    heads: topCounts(non125XRows.filter((row) => row.x_continuing === 'True'), (row) => row.head_after_002),
    tails: topCounts(non125XRows.filter((row) => row.x_continuing === 'True'), (row) => row.tail_after_x),
    decision: 'non125_can_continue_but_not_sufficient',
  },
  {
    checked_date: '2026-05-31',
    contrast: 'non_xslot_125',
    denominator: String(nonXslot125Occurrences.length),
    continuing: String(nonXslot125Continuing),
    continuing_rate: ratio(nonXslot125Continuing, nonXslot125Occurrences.length),
    terminal: String(nonXslot125Occurrences.length - nonXslot125Continuing),
    heads: topCounts(nonXslot125Occurrences, (row) => row.prev),
    tails: topCounts(nonXslot125Occurrences, (row) => row.next || '<END>'),
    decision: 'kills_intrinsic_open_value_but_allows_xslot_switch',
  },
];

const bets = [
  {
    checked_date: '2026-05-31',
    bet_id: 'X125_SUFFICIENT_CONTINUATION_SWITCH',
    tier: 'candidate',
    claim:
      'Inside this local register, when `125` is the X after `002-H`, it licenses continuation regardless of H; current heads are 190, 390, 405, and 610.',
    support: `post-002-H-125 continuing=${ratio(x125Open, x125Rows.length)}; heads=${topCounts(x125Rows, (row) => row.head_after_002)}; tails=${topCounts(x125Rows, (row) => row.tail_after_x)}`,
    falsifier:
      'Any same-register source-visible `002-H-125` row that terminates kills sufficiency.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'X125_NOT_INTRINSICALLY_OPEN',
    tier: 'candidate',
    claim:
      '`125` is not an intrinsic continuation sign; its continuation effect appears only in the post-`002-H-X` slot.',
    support: `non-X-slot 125 continuing=${ratio(nonXslot125Continuing, nonXslot125Occurrences.length)} while X-slot 125 continuing=${ratio(x125Open, x125Rows.length)}`,
    falsifier:
      'If non-X-slot source-visible `125` rows become overwhelmingly continuing after source collapse, the slot-specific switch interpretation weakens.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'X125_TAIL_ALLOMORPHY',
    tier: 'wild shot',
    claim:
      '`125` opens a dependent-tail slot whose fillers vary by head or left context: `632-032`, `820`, `032`, and `195` are not equivalent translations but allomorph-like tail outcomes.',
    support: `X-slot 125 tails=${topCounts(x125Rows, (row) => row.tail_after_x)}`,
    falsifier:
      'If the tails collapse into unrelated source/copy families, drop allomorphy and keep only continuation polarity.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'EXPAND',
  status: 'x125_switch_across_heads',
  same_register_scope: 'Mohenjo-daro|SEAL:S|square|Steatite',
  xslot_125: {
    rows: x125Rows.length,
    continuing_rate: ratio(x125Open, x125Rows.length),
    heads: topCounts(x125Rows, (row) => row.head_after_002),
    tails: topCounts(x125Rows, (row) => row.tail_after_x),
  },
  xslot_non125: {
    rows: non125XRows.length,
    continuing_rate: ratio(non125Open, non125XRows.length),
  },
  non_xslot_125: {
    rows: nonXslot125Occurrences.length,
    continuing_rate: ratio(nonXslot125Continuing, nonXslot125Occurrences.length),
    terminal_rate: ratio(nonXslot125Occurrences.length - nonXslot125Continuing, nonXslot125Occurrences.length),
  },
  new_bets: Object.fromEntries(bets.map((row) => [row.bet_id, row.tier])),
  predictions: [
    'New same-register `002-H-125` rows should continue.',
    'Terminal `125` remains possible outside the post-002-H-X slot.',
    'If `002-H-125` tail fillers cluster by H or left context after source collapse, treat them as tail allomorph candidates.',
  ],
};

writeCsv(path.join(reportsDir, `${prefix}_x125_rows.csv`), x125Rows, [
  'checked_date',
  'object',
  'id',
  'prev_before_002',
  'head_after_002',
  'x_after_head',
  'x_continuing',
  'x_terminal',
  'tail_after_x',
  'symbol',
  'cult',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_all_125_occurrences.csv`), all125Occurrences, [
  'checked_date',
  'object',
  'id',
  'occurrence_role',
  'head_if_xslot',
  'prev2',
  'prev',
  'next',
  'terminal',
  'continuing',
  'symbol',
  'cult',
  'complete',
  'condition',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_contrasts.csv`), contrastRows, [
  'checked_date',
  'contrast',
  'denominator',
  'continuing',
  'continuing_rate',
  'terminal',
  'heads',
  'tails',
  'decision',
]);

writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), bets, [
  'checked_date',
  'bet_id',
  'tier',
  'claim',
  'support',
  'falsifier',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
