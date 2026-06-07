import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_125_tail_submodes_20260531';
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

function countBy(items, field) {
  const counts = new Map();
  for (const item of items) {
    const key = item[field] || '-';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }))
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function examples(rows, n = 12) {
  return rows
    .slice(0, n)
    .map((row) => `${row.object}:${row.text}`)
    .join(' | ');
}

function tailMode(tail) {
  if (tail[0] === '632' && tail[1] === '032') return '632_032_title_tail';
  if (tail[0] === '820') return '820_title_tail';
  if (tail[0] === '195') return '195_terminal_cap';
  if (tail.length === 0) return 'terminal_125';
  return 'other_tail';
}

fs.mkdirSync(reportsDir, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  tokens: signs(row.text),
}));
const rows = [...new Map(rawRows.map((row) => [row.tokens.join(' '), row])).values()];

const governed125Rows = [];
const all125632032Rows = [];

for (const row of rows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
    if (row.tokens[i] === '002' && row.tokens[i + 1] && row.tokens[i + 2] === '125') {
      const tail = row.tokens.slice(i + 3);
      governed125Rows.push({
        checked_date: checkedDate,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        cult: row.cult,
        head_after_002: row.tokens[i + 1],
        left_penultimate: row.tokens[i - 2] ?? '<START>',
        left_final: row.tokens[i - 1] ?? '<START>',
        left_bigram: `${row.tokens[i - 2] ?? '<START>'}-${row.tokens[i - 1] ?? '<START>'}`,
        left_contains_235: String(row.tokens.slice(0, i).includes('235')),
        left_contains_032: String(row.tokens.slice(0, i).includes('032')),
        tail_after_125: tail.join(' ') || '<END>',
        tail_mode: tailMode(tail),
        terminal_after_125: String(tail.length === 0),
        text: row.text,
      });
    }

    if (row.tokens[i] === '125' && row.tokens[i + 1] === '632' && row.tokens[i + 2] === '032') {
      const before125 = row.tokens.slice(0, i);
      const last002 = before125.lastIndexOf('002');
      all125632032Rows.push({
        checked_date: checkedDate,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        cult: row.cult,
        governed_by_002: String(last002 >= 0 && last002 === i - 2),
        head_after_002: last002 >= 0 ? row.tokens[last002 + 1] : '<NONE>',
        left_final_before_002: last002 >= 1 ? row.tokens[last002 - 1] : '<NONE>',
        post_632032_tail: row.tokens.slice(i + 3).join(' ') || '<END>',
        text: row.text,
      });
    }
  }
}

const target390125 = governed125Rows.filter((row) => row.head_after_002 === '390');
const tail632032Governed = governed125Rows.filter((row) => row.tail_mode === '632_032_title_tail');
const tail632032Target = target390125.filter((row) => row.tail_mode === '632_032_title_tail');
const tail632032Non235 = tail632032Governed.filter((row) => row.left_contains_235 === 'false');
const final235Target = target390125.filter((row) => row.left_final === '235');

const summaryRows = [
  {
    checked_date: checkedDate,
    bucket: 'all_governed_002_H_125',
    rows: String(governed125Rows.length),
    heads: countBy(governed125Rows, 'head_after_002'),
    tail_modes: countBy(governed125Rows, 'tail_mode'),
    left_finals: countBy(governed125Rows, 'left_final'),
    examples: examples(governed125Rows),
  },
  {
    checked_date: checkedDate,
    bucket: 'target_002_390_125',
    rows: String(target390125.length),
    heads: countBy(target390125, 'head_after_002'),
    tail_modes: countBy(target390125, 'tail_mode'),
    left_finals: countBy(target390125, 'left_final'),
    examples: examples(target390125),
  },
  {
    checked_date: checkedDate,
    bucket: 'governed_125_632_032_tail',
    rows: String(tail632032Governed.length),
    heads: countBy(tail632032Governed, 'head_after_002'),
    tail_modes: countBy(tail632032Governed, 'tail_mode'),
    left_finals: countBy(tail632032Governed, 'left_final'),
    examples: examples(tail632032Governed),
  },
  {
    checked_date: checkedDate,
    bucket: 'all_125_632_032_occurrences',
    rows: String(all125632032Rows.length),
    heads: countBy(all125632032Rows, 'head_after_002'),
    tail_modes: '',
    left_finals: countBy(all125632032Rows, 'left_final_before_002'),
    examples: examples(all125632032Rows),
  },
];

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_125_TWO_SUBMODE_SELECTOR',
    tier:
      final235Target.length >= 2 && tail632032Target.length >= 2 && tail632032Non235.length >= 1
        ? 'candidate'
        : 'wild_shot',
    risky_bet:
      'Target 002-390-125 has at least two submodes: a final-235 rank-trigger mode and a portable 125-632-032 title-tail mode that does not require final 235.',
    current_test:
      `target 002-390-125 rows=${target390125.length}; final235 rows=${final235Target.length}; target 632-032 tails=${tail632032Target.length}; governed 632-032 without left 235=${tail632032Non235.length}.`,
    evidence: examples(target390125),
    destructive_prediction:
      'If source-normalized M-119 or M-1692 loses 125-632-032, demote the portable title-tail mode; if new final-235 target rows lack 125, demote the trigger mode.',
    promotion_prediction:
      'A third source-visible governed head with 125-632-032, or another strict non-235 target row with 125-632-032, promotes the tail mode.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_125632032_PORTABLE_TITLE_TAIL',
    tier: tail632032Governed.length >= 3 && new Set(tail632032Governed.map((row) => row.head_after_002)).size >= 2
      ? 'candidate'
      : 'wild_shot',
    risky_bet:
      '125-632-032 is a portable title-tail selected after governed 125 across more than one head, not a private M-38 formula.',
    current_test:
      `governed 125-632-032 rows=${tail632032Governed.length}; heads=${countBy(tail632032Governed, 'head_after_002')}; left finals=${countBy(tail632032Governed, 'left_final')}.`,
    evidence: examples(tail632032Governed),
    destructive_prediction:
      'If the 190 row is a copy/damage artifact or 632-032 spreads outside governed 125 with no slot discipline, demote portable title-tail status.',
    promotion_prediction:
      'More governed 125-632-032 rows under new heads/sites promote 632-032 as a title-tail suffix.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_235_IS_TRIGGER_NOT_WHOLE_EXPLANATION',
    tier: tail632032Non235.length >= 1 ? 'candidate' : 'wild_shot',
    risky_bet:
      '235 can trigger 125 in P086 heads, but it does not explain all high-value 125 behavior; tail mode 632-032 can appear without 235.',
    current_test:
      `final235 target rows=${final235Target.length}; governed 632-032 non235 rows=${tail632032Non235.length}; all 125-632-032 rows=${all125632032Rows.length}.`,
    evidence: `final235=${examples(final235Target)} | non235632032=${examples(tail632032Non235)}`,
    destructive_prediction:
      'If non-235 632-032 rows collapse, 235 can regain explanatory priority.',
    promotion_prediction:
      'A second non-235 target 002-390-125-632-032 row or strict non-390 governed 125-632-032 row promotes the split.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_125_TAILS_ARE_SUBTYPES_NOT_FREE_NAMES',
    tier: target390125.length === 4 && new Set(target390125.map((row) => row.tail_mode)).size >= 3
      ? 'wild_shot'
      : 'too_thin',
    risky_bet:
      'The post-125 tails 632-032, 195, and 820 are subtype/title-tail choices rather than arbitrary personal-name spelling.',
    current_test:
      `target tail modes=${countBy(target390125, 'tail_mode')}.`,
    evidence: examples(target390125),
    destructive_prediction:
      'If tails proliferate with no recurrence, or recur freely outside governed 125, demote subtype-tail parsing.',
    promotion_prediction:
      'Repeated source-visible tails with stable head/left contexts promote subtype-tail parsing.',
  },
];

writeCsv(
  path.join(reportsDir, `${prefix}_governed_125_rows.csv`),
  governed125Rows,
  [
    'checked_date',
    'object',
    'row_id',
    'site',
    'type',
    'symbol',
    'cult',
    'head_after_002',
    'left_penultimate',
    'left_final',
    'left_bigram',
    'left_contains_235',
    'left_contains_032',
    'tail_after_125',
    'tail_mode',
    'terminal_after_125',
    'text',
  ],
);
writeCsv(
  path.join(reportsDir, `${prefix}_125632032_occurrences.csv`),
  all125632032Rows,
  [
    'checked_date',
    'object',
    'row_id',
    'site',
    'type',
    'symbol',
    'cult',
    'governed_by_002',
    'head_after_002',
    'left_final_before_002',
    'post_632032_tail',
    'text',
  ],
);
writeCsv(
  path.join(reportsDir, `${prefix}_summary_rows.csv`),
  summaryRows,
  ['checked_date', 'bucket', 'rows', 'heads', 'tail_modes', 'left_finals', 'examples'],
);
writeCsv(
  path.join(reportsDir, `${prefix}_bets.csv`),
  betRows,
  [
    'checked_date',
    'bet_id',
    'tier',
    'risky_bet',
    'current_test',
    'evidence',
    'destructive_prediction',
    'promotion_prediction',
  ],
);

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'expand_125_tail_submodes',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: rows.length,
    governed_002_H_125_rows: governed125Rows.length,
    target_002_390_125_rows: target390125.length,
    governed_125_632_032_rows: tail632032Governed.length,
    governed_125_632_032_heads: [...new Set(tail632032Governed.map((row) => row.head_after_002))].sort(),
    governed_125_632_032_non235_rows: tail632032Non235.length,
    all_125_632_032_occurrences: all125632032Rows.length,
  },
  bets: betRows.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
