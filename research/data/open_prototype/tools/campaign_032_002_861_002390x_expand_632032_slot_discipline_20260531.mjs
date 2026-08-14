import fs from 'node:fs';
import path from 'node:path';

// Is 632-032 a private tail that only exists after the 125 linker, or a
// general-purpose terminal compound that the 125 slot merely borrows? This
// script settles which framing the corpus supports. It reads
// lipi/metadata_filtered.csv, deduplicates by sign sequence, and collects
// every occurrence of sign 632 (with neighbors) and every 632-032 bigram,
// tagging each chunk with whether a 125 immediately precedes it, whether that
// 125 sits inside a governed 002 frame, what follows the chunk, and whether
// it ends the text. Summary buckets compare after-125 chunks against
// everything else. The four bets: 632-032 is a general terminal compound;
// 125-632-032 is governed reuse of it, not a unique invention; a warning that
// title-tail semantics must stay below promotion because most chunks occur
// outside 125; and M-119's trailing 900-563 may be a second dependent tail
// rather than proof the compound is nonterminal. Writes occurrence, chunk,
// bucket-summary, and bet CSVs plus a summary JSON to
// data/open_prototype/reports.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_632032_slot_discipline_20260531';
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

fs.mkdirSync(reportsDir, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  tokens: signs(row.text),
}));
const rows = [...new Map(rawRows.map((row) => [row.tokens.join(' '), row])).values()];

const chunkRows = [];
const sign632Rows = [];

for (const row of rows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
    if (row.tokens[i] === '632') {
      sign632Rows.push({
        checked_date: checkedDate,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        cult: row.cult,
        prev_before_632: row.tokens[i - 1] ?? '<START>',
        next_after_632: row.tokens[i + 1] ?? '<END>',
        terminal_after_632: String(i + 1 >= row.tokens.length),
        text: row.text,
      });
    }

    if (row.tokens[i] === '632' && row.tokens[i + 1] === '032') {
      const last002 = row.tokens.slice(0, i).lastIndexOf('002');
      const isGovernedBy125 = row.tokens[i - 1] === '125';
      const isAfterGoverned125 = isGovernedBy125 && last002 >= 0 && last002 < i - 1;
      chunkRows.push({
        checked_date: checkedDate,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        cult: row.cult,
        prev_before_632032: row.tokens[i - 1] ?? '<START>',
        next_after_632032: row.tokens[i + 2] ?? '<END>',
        terminal_after_632032: String(i + 2 >= row.tokens.length),
        after_125: String(isGovernedBy125),
        after_governed_125: String(isAfterGoverned125),
        governed_head: isAfterGoverned125 ? row.tokens[last002 + 1] : '<NONE>',
        left_final_before_002: isAfterGoverned125 && last002 > 0 ? row.tokens[last002 - 1] : '<NONE>',
        text: row.text,
      });
    }
  }
}

const after125 = chunkRows.filter((row) => row.after_125 === 'true');
const notAfter125 = chunkRows.filter((row) => row.after_125 === 'false');
const afterGoverned125 = chunkRows.filter((row) => row.after_governed_125 === 'true');
const terminalChunks = chunkRows.filter((row) => row.terminal_after_632032 === 'true');
const cleanTerminalOrPostTail = chunkRows.filter(
  (row) => row.terminal_after_632032 === 'true' || row.next_after_632032 === '900',
);

const summaryRows = [
  {
    checked_date: checkedDate,
    bucket: 'all_632_occurrences',
    rows: String(sign632Rows.length),
    prev: countBy(sign632Rows, 'prev_before_632'),
    next: countBy(sign632Rows, 'next_after_632'),
    terminal_share: sign632Rows.length
      ? (sign632Rows.filter((row) => row.terminal_after_632 === 'true').length / sign632Rows.length).toFixed(6)
      : 'NA',
    examples: examples(sign632Rows),
  },
  {
    checked_date: checkedDate,
    bucket: 'all_632_032_chunks',
    rows: String(chunkRows.length),
    prev: countBy(chunkRows, 'prev_before_632032'),
    next: countBy(chunkRows, 'next_after_632032'),
    terminal_share: chunkRows.length ? (terminalChunks.length / chunkRows.length).toFixed(6) : 'NA',
    examples: examples(chunkRows),
  },
  {
    checked_date: checkedDate,
    bucket: 'after_125_632_032_chunks',
    rows: String(after125.length),
    prev: countBy(after125, 'prev_before_632032'),
    next: countBy(after125, 'next_after_632032'),
    terminal_share: after125.length
      ? (after125.filter((row) => row.terminal_after_632032 === 'true').length / after125.length).toFixed(6)
      : 'NA',
    examples: examples(after125),
  },
  {
    checked_date: checkedDate,
    bucket: 'non_125_632_032_chunks',
    rows: String(notAfter125.length),
    prev: countBy(notAfter125, 'prev_before_632032'),
    next: countBy(notAfter125, 'next_after_632032'),
    terminal_share: notAfter125.length
      ? (notAfter125.filter((row) => row.terminal_after_632032 === 'true').length / notAfter125.length).toFixed(6)
      : 'NA',
    examples: examples(notAfter125),
  },
];

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_632032_GENERAL_TERMINAL_COMPOUND',
    tier: chunkRows.length >= 6 && terminalChunks.length / chunkRows.length >= 0.5 ? 'candidate' : 'wild_shot',
    risky_bet:
      '632-032 is a general terminal compound that can be borrowed into post-125 title-tail slots, not an exclusive 125 invention.',
    current_test:
      `632-032 chunks=${chunkRows.length}; after125=${after125.length}; non125=${notAfter125.length}; terminal_share=${chunkRows.length ? (terminalChunks.length / chunkRows.length).toFixed(6) : 'NA'}.`,
    evidence: examples(chunkRows),
    destructive_prediction:
      'If non-125 632-032 rows source-collapse as damaged joins, demote general compound; if 632-032 usually continues productively, demote terminal compound.',
    promotion_prediction:
      'More source-visible terminal 632-032 chunks in non-125 and post-125 slots promote the compound-tail model.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_125632032_IS_GOVERNED_REUSE_NOT_UNIQUE_TAIL',
    tier: afterGoverned125.length >= 3 && notAfter125.length >= 3 ? 'candidate' : 'wild_shot',
    risky_bet:
      '125-632-032 is governed reuse of an existing terminal compound; the 125 slot selects the compound rather than creating it.',
    current_test:
      `after governed 125=${afterGoverned125.length}; non125 632-032=${notAfter125.length}; governed heads=${countBy(afterGoverned125, 'governed_head')}.`,
    evidence: `governed=${examples(afterGoverned125)} | non125=${examples(notAfter125)}`,
    destructive_prediction:
      'If governed 125 rows lose 632-032 under source normalization, demote reuse; if non-125 632-032 is random/damaged, fall back to 125-specific tail.',
    promotion_prediction:
      'A new governed head selecting 125-632-032 plus a clean non-125 terminal 632-032 row promotes reuse.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_632032_SLOT_DISCIPLINE_WARNING',
    tier: notAfter125.length > after125.length ? 'warning' : 'wild_shot',
    risky_bet:
      'The title-tail semantics must stay below promotion because 632-032 is more common outside 125 than after 125.',
    current_test:
      `non125 chunks=${notAfter125.length}; after125 chunks=${after125.length}; all 632 occurrences=${sign632Rows.length}.`,
    evidence: examples(notAfter125),
    destructive_prediction:
      'If non-125 chunks remain numerous and heterogeneous, semantic title-tail stays candidate-only at best.',
    promotion_prediction:
      'If non-125 chunks collapse but governed 125 chunks survive, revive 125-specific title-tail semantics.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_M119_POSTTAIL_900563_EXTENSION',
    tier: after125.some((row) => row.next_after_632032 === '900') ? 'wild_shot' : 'too_thin',
    risky_bet:
      'M-119 may extend a complete 125-632-032 title-tail with a second dependent tail 900-563, rather than making 632-032 nonterminal.',
    current_test:
      `after125 next signs=${countBy(after125, 'next_after_632032')}; clean-terminal-or-900 rows=${cleanTerminalOrPostTail.length}/${chunkRows.length}.`,
    evidence: examples(after125.filter((row) => row.next_after_632032 === '900')),
    destructive_prediction:
      'If 900-563 appears as ordinary continuation after many non-title chunks, demote this extension parse.',
    promotion_prediction:
      'Another 125-632-032-900-like row would make post-tail extension a candidate.',
  },
];

writeCsv(
  path.join(reportsDir, `${prefix}_632_occurrences.csv`),
  sign632Rows,
  [
    'checked_date',
    'object',
    'row_id',
    'site',
    'type',
    'symbol',
    'cult',
    'prev_before_632',
    'next_after_632',
    'terminal_after_632',
    'text',
  ],
);
writeCsv(
  path.join(reportsDir, `${prefix}_632032_chunks.csv`),
  chunkRows,
  [
    'checked_date',
    'object',
    'row_id',
    'site',
    'type',
    'symbol',
    'cult',
    'prev_before_632032',
    'next_after_632032',
    'terminal_after_632032',
    'after_125',
    'after_governed_125',
    'governed_head',
    'left_final_before_002',
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
  status: 'expand_632032_slot_discipline',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: rows.length,
    sign_632_occurrences: sign632Rows.length,
    chunk_632032_occurrences: chunkRows.length,
    chunk_after_125: after125.length,
    chunk_after_governed_125: afterGoverned125.length,
    chunk_not_after_125: notAfter125.length,
    terminal_632032_chunks: terminalChunks.length,
  },
  bets: betRows.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
