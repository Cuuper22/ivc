import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const parseRowsPath = path.join(
  root,
  'data',
  'open_prototype',
  'reports',
  'campaign_032_002_861_002390x_expand_parse_skeleton_predictor_20260531_parse_rows.csv',
);
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_x000_null_class_20260531';
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

function tailTokens(row) {
  return row.tail_after_x === '<END>' ? [] : row.tail_after_x.split(' ');
}

function expectedFor000(row) {
  const tail = tailTokens(row);
  if (tail.length === 0) return 'closed_zero_complement';
  if (tail[0] === '000') return 'null_chain_or_zero_repeat';
  if (tail[0] === '002') return 'frame_reset_exception';
  if (tail[0] === '033') return 'head267_033_exception';
  return 'unexpected_non_null_tail';
}

function passFor000(row) {
  return expectedFor000(row) !== 'unexpected_non_null_tail';
}

function glossFor000(row) {
  const expectation = expectedFor000(row);
  if (expectation === 'closed_zero_complement') return `FRAME(002) HEAD(${row.head}) ZERO_COMPLEMENT(000)`;
  if (expectation === 'null_chain_or_zero_repeat') return `FRAME(002) HEAD(${row.head}) ZERO_CHAIN(000) TAIL(${row.tail_after_x})`;
  if (expectation === 'frame_reset_exception') return `FRAME(002) HEAD(${row.head}) ZERO_COMPLEMENT(000) RESET(002)`;
  if (expectation === 'head267_033_exception') return `FRAME(002) HEAD(${row.head}) ZERO_COMPLEMENT(000) EXCEPTION(033)`;
  return `FRAME(002) HEAD(${row.head}) ZERO_COMPLEMENT(000) UNEXPECTED(${row.tail_after_x})`;
}

fs.mkdirSync(reportsDir, { recursive: true });

const parseRows = parseCsv(fs.readFileSync(parseRowsPath, 'utf8'));
const x000Rows = parseRows.filter((row) => row.x === '000').map((row) => ({
  ...row,
  x000_expected: expectedFor000(row),
  x000_prediction_pass: String(passFor000(row)),
  x000_gloss_skeleton: glossFor000(row),
}));

const closed = x000Rows.filter((row) => row.x000_expected === 'closed_zero_complement');
const nullLike = x000Rows.filter((row) => row.x000_prediction_pass === 'true');

const parseRowsPlus000 = parseRows.map((row) => {
  if (row.x !== '000') return row;
  return {
    ...row,
    predicted_class: expectedFor000(row) === 'closed_zero_complement' ? 'zero_complement_class' : 'zero_complement_exception',
    expected_continuation: expectedFor000(row),
    prediction_pass: String(passFor000(row)),
    gloss_skeleton: glossFor000(row),
    failure_hook: 'meaningful non-null continuation after X=000',
  };
});

const classified = parseRowsPlus000.filter((row) => row.prediction_pass !== '');
const passing = classified.filter((row) => row.prediction_pass === 'true');

const ruleRows = [
  {
    checked_date: checkedDate,
    predicted_class: 'zero_complement_class',
    rows: String(closed.length),
    pass: ratio(closed.length, closed.length),
    heads: countBy(closed, (row) => row.head),
    sites: countBy(closed, (row) => row.site),
    examples: closed.slice(0, 8).map((row) => `${row.object}:${glossFor000(row)}`).join(' | '),
  },
  {
    checked_date: checkedDate,
    predicted_class: 'zero_complement_exception',
    rows: String(x000Rows.length - closed.length),
    pass: ratio(nullLike.length - closed.length, x000Rows.length - closed.length),
    heads: countBy(x000Rows.filter((row) => row.x000_expected !== 'closed_zero_complement'), (row) => row.head),
    sites: countBy(x000Rows.filter((row) => row.x000_expected !== 'closed_zero_complement'), (row) => row.site),
    examples: x000Rows
      .filter((row) => row.x000_expected !== 'closed_zero_complement')
      .map((row) => `${row.object}:${glossFor000(row)}`)
      .join(' | '),
  },
];

const bets = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_X000_ZERO_COMPLEMENT_CLASS',
    tier: closed.length >= 20 && nullLike.length === x000Rows.length ? 'candidate' : 'wild_shot',
    risky_bet:
      '`000` in X slot is a zero/null complement class: it normally closes, and its few continuations are null-chain/reset exceptions rather than payload.',
    current_test:
      `rows=${x000Rows.length}; closed=${ratio(closed.length, x000Rows.length)}; null_like_pass=${ratio(nullLike.length, x000Rows.length)}; ` +
      `heads=${countBy(x000Rows, (row) => row.head)}; tails=${countBy(x000Rows, (row) => row.tail_after_x)}.`,
    destructive_prediction:
      'A run of source-strict `002-H-000-Y` rows where Y is a meaningful non-null tail kills the zero-complement class.',
    promotion_prediction:
      'More closed `002-H-000` rows across heads/sites, especially source-strict, promote `000` as parser zero.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_PARSE_SKELETON_PLUS_X000',
    tier: passing.length / classified.length >= 0.95 ? 'candidate' : 'wild_shot',
    risky_bet:
      'Adding X=`000` as zero-complement materially increases parse-skeleton coverage without assigning a lexical value.',
    current_test:
      `coverage=${ratio(classified.length, parseRowsPlus000.length)}; pass=${ratio(passing.length, classified.length)}; added_x000=${x000Rows.length}.`,
    destructive_prediction:
      'If `000` exceptions become semantically diverse, the coverage gain is fake and must be rolled back.',
    promotion_prediction:
      'If zero-complement behavior predicts held-out/source-strict `000` rows, the parser gains its first high-coverage null class.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'x000_null_class',
  rows: {
    x000_rows: x000Rows.length,
    x000_closed: closed.length,
    x000_null_like_pass: nullLike.length,
    parse_rows_plus_000_classified: classified.length,
    parse_rows_plus_000_pass: passing.length,
    parse_rows_total: parseRowsPlus000.length,
  },
  bets: bets.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

writeCsv(path.join(reportsDir, `${prefix}_x000_rows.csv`), x000Rows, [
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
  'observed_continuation',
  'x000_expected',
  'x000_prediction_pass',
  'x000_gloss_skeleton',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_rule_rows.csv`), ruleRows, [
  'checked_date',
  'predicted_class',
  'rows',
  'pass',
  'heads',
  'sites',
  'examples',
]);

writeCsv(path.join(reportsDir, `${prefix}_parse_rows_plus_000.csv`), parseRowsPlus000, [
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
  'observed_continuation',
  'predicted_class',
  'expected_continuation',
  'prediction_pass',
  'gloss_skeleton',
  'failure_hook',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), bets, [
  'checked_date',
  'bet_id',
  'tier',
  'risky_bet',
  'current_test',
  'destructive_prediction',
  'promotion_prediction',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
