import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_032_clamp_head_productivity_20260531';
const checkedDate = '2026-05-31';
const heads = new Set(['817', '820', '861', '390']);

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

function examples(rows, n = 10) {
  return rows
    .slice(0, n)
    .map((row) => `${row.object}:${row.text}`)
    .join(' | ');
}

function entropy(values) {
  if (!values.length) return 0;
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  let e = 0;
  for (const value of counts.values()) {
    const p = value / values.length;
    e -= p * Math.log2(p);
  }
  return e;
}

function fixed(value) {
  return Number.isFinite(value) ? value.toFixed(6) : 'NA';
}

fs.mkdirSync(reportsDir, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  tokens: signs(row.text),
}));
const rows = [...new Map(rawRows.map((row) => [row.tokens.join(' '), row])).values()];

const targetRows = [];
for (const row of rows) {
  for (let i = 0; i < row.tokens.length - 1; i += 1) {
    if (row.tokens[i] !== '002' || !heads.has(row.tokens[i + 1])) continue;
    const head = row.tokens[i + 1];
    const tail = row.tokens.slice(i + 2);
    const prev = row.tokens[i - 1] ?? '<START>';
    targetRows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      symbol: row.symbol,
      cult: row.cult,
      head_after_002: head,
      prev_before_002: prev,
      preceded_by_032: String(prev === '032'),
      next_after_head: tail[0] ?? '<END>',
      tail_after_head: tail.join(' ') || '<END>',
      terminal_after_head: String(tail.length === 0),
      text: row.text,
    });
  }
}

const summaryRows = [];
for (const head of heads) {
  for (const precededBy032 of ['true', 'false']) {
    const subset = targetRows.filter(
      (row) => row.head_after_002 === head && row.preceded_by_032 === precededBy032,
    );
    const terminal = subset.filter((row) => row.terminal_after_head === 'true').length;
    summaryRows.push({
      checked_date: checkedDate,
      head_after_002: head,
      preceded_by_032: precededBy032,
      rows: String(subset.length),
      terminal_rows: String(terminal),
      terminal_share: subset.length ? fixed(terminal / subset.length) : 'NA',
      next_entropy_bits: subset.length ? fixed(entropy(subset.map((row) => row.next_after_head))) : 'NA',
      top_next_after_head: countBy(subset, 'next_after_head'),
      prev_before_002: countBy(subset, 'prev_before_002'),
      sites: countBy(subset, 'site'),
      types: countBy(subset, 'type'),
      examples: examples(subset),
    });
  }
}

function subset(head, precededBy032) {
  return targetRows.filter(
    (row) => row.head_after_002 === head && row.preceded_by_032 === String(precededBy032),
  );
}

function terminalShare(head, precededBy032) {
  const rowsForHead = subset(head, precededBy032);
  if (!rowsForHead.length) return 0;
  return rowsForHead.filter((row) => row.terminal_after_head === 'true').length / rowsForHead.length;
}

const clampHeads = ['817', '820', '861'];
const clampRows032 = clampHeads.flatMap((head) => subset(head, true));
const clampRowsNo032 = clampHeads.flatMap((head) => subset(head, false));
const clampTerminal032 =
  clampRows032.length === 0
    ? 0
    : clampRows032.filter((row) => row.terminal_after_head === 'true').length / clampRows032.length;
const clampTerminalNo032 =
  clampRowsNo032.length === 0
    ? 0
    : clampRowsNo032.filter((row) => row.terminal_after_head === 'true').length / clampRowsNo032.length;
const rows861No032 = subset('861', false);
const rows861032 = subset('861', true);
const rows390032 = subset('390', true);

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_032_CLAMPS_CLOSED_HEAD_PRODUCTIVITY',
    tier: clampTerminal032 > clampTerminalNo032 + 0.2 ? 'candidate' : 'wild_shot',
    risky_bet:
      '032 before 002 clamps frequent classifier heads 817/820/861 toward terminal readings, instead of simply introducing any head.',
    current_test:
      `032-preceded closed-head rows=${clampRows032.length}, terminal_share=${fixed(clampTerminal032)}; non-032 rows=${clampRowsNo032.length}, terminal_share=${fixed(clampTerminalNo032)}.`,
    evidence: examples(clampRows032),
    destructive_prediction:
      'More source-visible 032-002-817/820/861 rows with productive tails, or non-032 rows that are equally terminal, demote clamp function.',
    promotion_prediction:
      'More source-visible 032-002 closed-head rows ending terminally while non-032 002-H rows keep tails promote 032 as clamp/boundary operator.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_861_PRODUCTIVE_HEAD_SUPPRESSED_BY_032',
    tier: rows861No032.length >= 5 && terminalShare('861', true) > terminalShare('861', false) ? 'candidate' : 'wild_shot',
    risky_bet:
      '861 is productive after plain 002, but 032-002-861 suppresses that productivity and often closes the phrase.',
    current_test:
      `032-002-861 rows=${rows861032.length}, terminal_share=${fixed(terminalShare('861', true))}; non-032 002-861 rows=${rows861No032.length}, terminal_share=${fixed(terminalShare('861', false))}; non-032 next=${countBy(rows861No032, 'next_after_head')}.`,
    evidence: `032=${examples(rows861032)} | non032=${examples(rows861No032)}`,
    destructive_prediction:
      'A source-visible crop showing the 032-002-861 terminal rows are truncated, or many new 032-002-861-Y rows, kills suppression.',
    promotion_prediction:
      'More pairs where plain 002-861 takes known tails but 032-002-861 ends terminally promote the head-conditioned clamp.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_861_416_AND_603_ARE_REAL_DEPENDENT_TAILS',
    tier:
      rows861No032.filter((row) => row.next_after_head === '416' || row.next_after_head === '603').length >= 4
        ? 'candidate'
        : 'wild_shot',
    risky_bet:
      'The 861 continuations 416 and 603 are reusable dependent tails, not random residue after 861.',
    current_test:
      `non-032 002-861 next signs=${countBy(rows861No032, 'next_after_head')}.`,
    evidence: examples(rows861No032.filter((row) => row.next_after_head === '416' || row.next_after_head === '603')),
    destructive_prediction:
      'If 416/603 rows collapse to duplicate tablets or damaged snippets, demote 861 dependent-tail status.',
    promotion_prediction:
      'If 416/603 recur on independent source-visible 002-861 rows, parse them as dependent tail classes.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_032_CLAMP_IS_HEAD_CONDITIONED_NOT_GLOBAL',
    tier: rows390032.length === 2 && rows390032.every((row) => row.terminal_after_head === 'false') ? 'candidate' : 'wild_shot',
    risky_bet:
      '032 is not a global terminalizer: it clamps 817/820/861 but can feed the rare open 390 lane under special left contexts.',
    current_test:
      `032-002-390 rows=${rows390032.length}; terminal_share=${fixed(terminalShare('390', true))}; tails=${countBy(rows390032, 'next_after_head')}.`,
    evidence: examples(rows390032),
    destructive_prediction:
      'Frequent terminal 032-002-390 rows or productive 032-002-817/820/861 rows flatten the head-conditioned split.',
    promotion_prediction:
      'More evidence that 032 closes some heads but feeds open 390 under 205/226 promotes head-conditioned parsing.',
  },
];

writeCsv(
  path.join(reportsDir, `${prefix}_target_rows.csv`),
  targetRows,
  [
    'checked_date',
    'object',
    'row_id',
    'site',
    'type',
    'symbol',
    'cult',
    'head_after_002',
    'prev_before_002',
    'preceded_by_032',
    'next_after_head',
    'tail_after_head',
    'terminal_after_head',
    'text',
  ],
);
writeCsv(
  path.join(reportsDir, `${prefix}_head_032_contrast.csv`),
  summaryRows,
  [
    'checked_date',
    'head_after_002',
    'preceded_by_032',
    'rows',
    'terminal_rows',
    'terminal_share',
    'next_entropy_bits',
    'top_next_after_head',
    'prev_before_002',
    'sites',
    'types',
    'examples',
  ],
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
  status: 'expand_032_clamp_head_productivity',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: rows.length,
    target_occurrences: targetRows.length,
    clamp_heads_032_rows: clampRows032.length,
    clamp_heads_032_terminal_share: fixed(clampTerminal032),
    clamp_heads_non032_rows: clampRowsNo032.length,
    clamp_heads_non032_terminal_share: fixed(clampTerminalNo032),
    non032_002861_rows: rows861No032.length,
    preceded032_002390_rows: rows390032.length,
  },
  bets: betRows.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
