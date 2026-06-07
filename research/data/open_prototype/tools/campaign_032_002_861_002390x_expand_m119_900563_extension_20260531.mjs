import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_m119_900563_extension_20260531';
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

function containsAt(tokens, start, pattern) {
  return pattern.every((token, offset) => tokens[start + offset] === token);
}

fs.mkdirSync(reportsDir, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  tokens: signs(row.text),
}));
const rows = [...new Map(rawRows.map((row) => [row.tokens.join(' '), row])).values()];

const signRows = [];
const patternRows = [];
const patterns = [
  { label: '900-563', tokens: ['900', '563'] },
  { label: '032-900-563', tokens: ['032', '900', '563'] },
  { label: '632-032-900-563', tokens: ['632', '032', '900', '563'] },
  { label: '125-632-032-900-563', tokens: ['125', '632', '032', '900', '563'] },
];

for (const row of rows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
    if (row.tokens[i] === '900' || row.tokens[i] === '563') {
      signRows.push({
        checked_date: checkedDate,
        sign: row.tokens[i],
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        cult: row.cult,
        prev: row.tokens[i - 1] ?? '<START>',
        next: row.tokens[i + 1] ?? '<END>',
        terminal_after_sign: String(i + 1 >= row.tokens.length),
        text: row.text,
      });
    }

    for (const pattern of patterns) {
      if (!containsAt(row.tokens, i, pattern.tokens)) continue;
      patternRows.push({
        checked_date: checkedDate,
        pattern: pattern.label,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        cult: row.cult,
        prev_before_pattern: row.tokens[i - 1] ?? '<START>',
        next_after_pattern: row.tokens[i + pattern.tokens.length] ?? '<END>',
        terminal_after_pattern: String(i + pattern.tokens.length >= row.tokens.length),
        text: row.text,
      });
    }
  }
}

const exact900563 = patternRows.filter((row) => row.pattern === '900-563');
const exact125632032900563 = patternRows.filter((row) => row.pattern === '125-632-032-900-563');
const sign900 = signRows.filter((row) => row.sign === '900');
const sign563 = signRows.filter((row) => row.sign === '563');
const m119Pattern = exact125632032900563.filter((row) => row.object === 'M-119');

const summaryRows = [
  {
    checked_date: checkedDate,
    bucket: 'sign_900',
    rows: String(sign900.length),
    prev: countBy(sign900, 'prev'),
    next: countBy(sign900, 'next'),
    terminal_share: sign900.length
      ? (sign900.filter((row) => row.terminal_after_sign === 'true').length / sign900.length).toFixed(6)
      : 'NA',
    examples: examples(sign900),
  },
  {
    checked_date: checkedDate,
    bucket: 'sign_563',
    rows: String(sign563.length),
    prev: countBy(sign563, 'prev'),
    next: countBy(sign563, 'next'),
    terminal_share: sign563.length
      ? (sign563.filter((row) => row.terminal_after_sign === 'true').length / sign563.length).toFixed(6)
      : 'NA',
    examples: examples(sign563),
  },
  {
    checked_date: checkedDate,
    bucket: 'pattern_900_563',
    rows: String(exact900563.length),
    prev: countBy(exact900563, 'prev_before_pattern'),
    next: countBy(exact900563, 'next_after_pattern'),
    terminal_share: exact900563.length
      ? (exact900563.filter((row) => row.terminal_after_pattern === 'true').length / exact900563.length).toFixed(6)
      : 'NA',
    examples: examples(exact900563),
  },
  {
    checked_date: checkedDate,
    bucket: 'pattern_125_632_032_900_563',
    rows: String(exact125632032900563.length),
    prev: countBy(exact125632032900563, 'prev_before_pattern'),
    next: countBy(exact125632032900563, 'next_after_pattern'),
    terminal_share: exact125632032900563.length
      ? (
          exact125632032900563.filter((row) => row.terminal_after_pattern === 'true').length /
          exact125632032900563.length
        ).toFixed(6)
      : 'NA',
    examples: examples(exact125632032900563),
  },
];

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_M119_900563_SECONDARY_EXTENSION',
    tier: exact900563.length === 1 && m119Pattern.length === 1 ? 'wild_shot_singleton' : 'candidate',
    risky_bet:
      'M-119 extends a completed 125-632-032 package with a secondary terminal tail 900-563.',
    current_test:
      `exact 900-563 rows=${exact900563.length}; exact 125-632-032-900-563 rows=${exact125632032900563.length}; sign900 rows=${sign900.length}; sign563 rows=${sign563.length}.`,
    evidence: examples(exact900563),
    destructive_prediction:
      'If 900-563 appears in unrelated contexts, demote the M-119-specific extension parse; if M-119 source loses 900-563, kill it.',
    promotion_prediction:
      'A second governed 125-632-032-900-563 or post-title 900-563 row would promote the secondary-extension parse.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_563_IS_NOT_CURRENTLY_A_SIGN_VALUE',
    tier: sign563.length <= 2 ? 'candidate_negative' : 'wild_shot',
    risky_bet:
      '563 currently has no stable sign-function evidence; in M-119 it is only the terminal member of a singleton 900-563 tail.',
    current_test: `sign563 rows=${sign563.length}; prev=${countBy(sign563, 'prev')}; next=${countBy(sign563, 'next')}.`,
    evidence: examples(sign563),
    destructive_prediction:
      'More independent 563 rows with repeated neighbors would revive a sign-level function bet.',
    promotion_prediction:
      'No promotion from current evidence; this is a negative guardrail against semanticizing 563.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_900_IS_TOO_PRODUCTIVE_TO_EXPLAIN_M119_ALONE',
    tier: sign900.length > 50 ? 'candidate_negative' : 'wild_shot',
    risky_bet:
      '900 is too productive and heterogeneous to explain M-119 by itself; only exact 900-563 is relevant to the extension bet.',
    current_test: `sign900 rows=${sign900.length}; top next=${countBy(sign900, 'next')}.`,
    evidence: examples(sign900),
    destructive_prediction:
      'If exact 900-563 repeats in the same post-tail slot, promote the exact compound while keeping raw 900 broad.',
    promotion_prediction:
      'A repeated exact tail, not raw 900 frequency, is required for promotion.',
  },
];

writeCsv(
  path.join(reportsDir, `${prefix}_sign_rows.csv`),
  signRows,
  [
    'checked_date',
    'sign',
    'object',
    'row_id',
    'site',
    'type',
    'symbol',
    'cult',
    'prev',
    'next',
    'terminal_after_sign',
    'text',
  ],
);
writeCsv(
  path.join(reportsDir, `${prefix}_pattern_rows.csv`),
  patternRows,
  [
    'checked_date',
    'pattern',
    'object',
    'row_id',
    'site',
    'type',
    'symbol',
    'cult',
    'prev_before_pattern',
    'next_after_pattern',
    'terminal_after_pattern',
    'text',
  ],
);
writeCsv(
  path.join(reportsDir, `${prefix}_summary_rows.csv`),
  summaryRows,
  ['checked_date', 'bucket', 'rows', 'prev', 'next', 'terminal_share', 'examples'],
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
  status: 'expand_m119_900563_extension',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: rows.length,
    sign_900_rows: sign900.length,
    sign_563_rows: sign563.length,
    exact_900_563_rows: exact900563.length,
    exact_125_632_032_900_563_rows: exact125632032900563.length,
  },
  bets: betRows.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
