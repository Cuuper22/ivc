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
const prefix = 'campaign_032_002_861_002390x_expand_unclassified_family_bets_20260531';
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

function examples(rows, n = 5) {
  return rows
    .slice(0, n)
    .map((row) => `${row.object}:${row.text}`)
    .join(' | ');
}

function firstTail(row) {
  return row.tail_after_x === '<END>' ? '<END>' : row.tail_after_x.split(' ')[0];
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(parseRowsPath, 'utf8'));
const unclassified = rows.filter((row) => row.predicted_class === 'unclassified_x_slot');
const grouped = new Map();
for (const row of unclassified) {
  if (!grouped.has(row.x)) grouped.set(row.x, []);
  grouped.get(row.x).push(row);
}

const familyRows = [...grouped.entries()]
  .map(([x, group]) => {
    const open = group.filter((row) => row.tail_after_x !== '<END>').length;
    return {
      checked_date: checkedDate,
      x,
      rows: String(group.length),
      open: ratio(open, group.length),
      heads: countBy(group, (row) => row.head),
      sites: countBy(group, (row) => row.site),
      types: countBy(group, (row) => row.type),
      first_tail: countBy(group, firstTail),
      examples: examples(group),
    };
  })
  .sort((a, b) => Number(b.rows) - Number(a.rows) || a.x.localeCompare(b.x, undefined, { numeric: true }));

const topRows = familyRows.slice(0, 6);
const byX = Object.fromEntries(topRows.map((row) => [row.x, row]));

const bets = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_X000_NULL_OR_ZERO_COMPLEMENT_CLASS',
    tier: byX['000'] && Number(byX['000'].rows) >= 20 ? 'candidate' : 'wild_shot',
    risky_bet:
      '`000` in X slot is a null/zero-complement class, not a lexical payload: it overwhelmingly closes but can repeat or route into null-like tails.',
    current_test: byX['000'] ? `rows=${byX['000'].rows}; open=${byX['000'].open}; tails=${byX['000'].first_tail}; examples=${byX['000'].examples}` : 'no rows',
    destructive_prediction:
      'Many source-strict `002-H-000-Y` rows with meaningful non-null continuations kill the null-complement class.',
    promotion_prediction:
      'More closed `000` rows across heads/sites promote `000` as the zero/null pole of the parser.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_X031_TERMINAL_CLASS_CANDIDATE',
    tier: byX['031'] ? 'wild_shot' : 'too_small',
    risky_bet:
      '`031` may be another terminal class candidate, weaker than `095` because it has a live continuation exception.',
    current_test: byX['031'] ? `rows=${byX['031'].rows}; open=${byX['031'].open}; heads=${byX['031'].heads}; examples=${byX['031'].examples}` : 'no rows',
    destructive_prediction:
      'More open `031` rows, especially outside one head/form family, prevent class promotion.',
    promotion_prediction:
      'More closed `002-H-031` rows across heads and domains promote `031` into the terminal class portfolio.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_X455_OPEN_OPERATOR_CANDIDATE',
    tier: byX['455'] ? 'wild_shot' : 'too_small',
    risky_bet:
      '`455` may be an open operator class, but its head concentration under `220` makes it vulnerable to formula/register collapse.',
    current_test: byX['455'] ? `rows=${byX['455'].rows}; open=${byX['455'].open}; heads=${byX['455'].heads}; examples=${byX['455'].examples}` : 'no rows',
    destructive_prediction:
      'If `455` open behavior is only `220`-formula behavior, kill it as a portable X class.',
    promotion_prediction:
      'Open `455` under unrelated heads promotes it as an operator peer to `125/530`.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_X032_NOT_CLASS_BUT_ROUTE_MARKER',
    tier: byX['032'] ? 'wild_shot' : 'too_small',
    risky_bet:
      '`032` in X slot is not a class/operator at all; it is a route or boundary marker whose behavior depends on surrounding formula path.',
    current_test: byX['032'] ? `rows=${byX['032'].rows}; open=${byX['032'].open}; heads=${byX['032'].heads}; tails=${byX['032'].first_tail}` : 'no rows',
    destructive_prediction:
      'Consistent closed/open behavior under many unrelated heads would make `032` class-like and kill the route-marker read.',
    promotion_prediction:
      'Mixed behavior with strong path/formula dependency promotes it as route material, not payload class.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_X350_SCOPE_FORMULA_BAIT',
    tier: byX['350'] ? 'wild_shot' : 'too_small',
    risky_bet:
      '`350` is not a portable operator yet; it may be a scope/formula bait sign because repeated tails are sparse and head spread is high.',
    current_test: byX['350'] ? `rows=${byX['350'].rows}; open=${byX['350'].open}; heads=${byX['350'].heads}; tails=${byX['350'].first_tail}` : 'no rows',
    destructive_prediction:
      'A repeated head-tail subrule for `350` promotes it; otherwise it stays formula bait.',
    promotion_prediction:
      'Two more rows sharing head and tail family promote a `350` subrule.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'unclassified_family_bets',
  rows: {
    unclassified_rows: unclassified.length,
    distinct_unclassified_x: grouped.size,
    top_unclassified_x: topRows.map((row) => `${row.x}:${row.rows}`),
  },
  bets: bets.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

writeCsv(path.join(reportsDir, `${prefix}_family_rows.csv`), familyRows, [
  'checked_date',
  'x',
  'rows',
  'open',
  'heads',
  'sites',
  'types',
  'first_tail',
  'examples',
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
