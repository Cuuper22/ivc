import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_125820_terminal_cap_test_20260531';

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

function countBy(items, fn) {
  const counts = new Map();
  for (const item of items) {
    const key = fn(item) || '-';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()].sort(
    (a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }),
  );
}

function topCounts(counts, n = 12) {
  return counts
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function governedHead(tokens, signIndex) {
  for (let headIndex = signIndex - 1; headIndex >= 0 && headIndex >= signIndex - 4; headIndex -= 1) {
    if (tokens[headIndex - 1] === '002') {
      return {
        governed: true,
        head: tokens[headIndex],
        prevBefore002: tokens[headIndex - 2] ?? '<START>',
      };
    }
  }
  return { governed: false, head: '', prevBefore002: '' };
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  tokens: signs(row.text),
}));

const occurrences820 = [];
const occurrences125820 = [];
const direct820After002Head = [];

for (const row of rows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
    const sign = row.tokens[i];
    if (sign === '820') {
      const gov = governedHead(row.tokens, i);
      const prev = row.tokens[i - 1] ?? '<START>';
      const next = row.tokens[i + 1] ?? '<END>';
      occurrences820.push({
        checked_date: '2026-05-31',
        cisi: row.cisi || '-',
        row_id: row.id,
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        cult: row.cult,
        prev,
        next,
        terminal_after_820: String(next === '<END>'),
        governed_by_002: String(gov.governed),
        governed_head: gov.head,
        prev_before_002: gov.prevBefore002,
        text: row.text,
      });
    }
    if (sign === '125' && row.tokens[i + 1] === '820') {
      const gov = governedHead(row.tokens, i);
      occurrences125820.push({
        checked_date: '2026-05-31',
        cisi: row.cisi || '-',
        row_id: row.id,
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        cult: row.cult,
        prev_before_125: row.tokens[i - 1] ?? '<START>',
        next_after_820: row.tokens[i + 2] ?? '<END>',
        terminal_after_820: String((row.tokens[i + 2] ?? '<END>') === '<END>'),
        governed_by_002: String(gov.governed),
        governed_head: gov.head,
        prev_before_002: gov.prevBefore002,
        text: row.text,
      });
    }
    if (sign === '002') {
      const head = row.tokens[i + 1] ?? '<END>';
      const branch = row.tokens[i + 2] ?? '<END>';
      if (branch === '820') {
        direct820After002Head.push({
          checked_date: '2026-05-31',
          cisi: row.cisi || '-',
          row_id: row.id,
          site: row.site,
          type: row.type,
          symbol: row.symbol,
          cult: row.cult,
          prev_before_002: row.tokens[i - 1] ?? '<START>',
          governed_head: head,
          next_after_820: row.tokens[i + 3] ?? '<END>',
          terminal_after_820: String((row.tokens[i + 3] ?? '<END>') === '<END>'),
          text: row.text,
        });
      }
    }
  }
}

const terminal820 = occurrences820.filter((row) => row.terminal_after_820 === 'true');
const non125Prev820 = occurrences820.filter((row) => row.prev !== '125');
const non125PrevTerminal820 = non125Prev820.filter((row) => row.terminal_after_820 === 'true');

const bets = [
  {
    checked_date: '2026-05-31',
    bet_id: 'EXPAND_125820_TERMINAL_CAP_NOT_TITLE_VALUE',
    tier: 'candidate-edge',
    claim:
      '`125-820` is not a two-sign lexical title. `125` carries the rank/title continuation slot; `820` is a terminal cap attached to that slot.',
    support:
      `125-820 rows=${occurrences125820.length}; terminal_after_820=${occurrences125820.filter((row) => row.terminal_after_820 === 'true').length}/${occurrences125820.length}; governed=${occurrences125820.filter((row) => row.governed_by_002 === 'true').length}/${occurrences125820.length}; 820_global_terminal=${terminal820.length}/${occurrences820.length}; non125_prev_820_terminal=${non125PrevTerminal820.length}/${non125Prev820.length}.`,
    examples: occurrences125820.map((row) => `${row.cisi}:${row.text}`).join(' | '),
    kill_condition:
      'A source-visible nonterminal 125-820-Y cluster, or repeated non-governed 125-820 outside the 002 head lane, kills cap status.',
    promote_condition:
      'A third source-visible governed 390/405/near-P086 row with terminal 125-820 promotes it from edge to candidate P086 terminal-cap subtype.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'EXPAND_820_CLOSURE_BACKGROUND_DAMAGES_SEMANTIC_TITLE_GLOSS',
    tier: 'candidate-negative',
    claim:
      '`820` alone should not be glossed title/rank because it is a broad terminal closure sign across many contexts.',
    support:
      `global_820=${occurrences820.length}; terminal=${terminal820.length}; prev_before_820_top=${topCounts(countBy(occurrences820, (row) => row.prev), 10)}; direct_002_head_to_820_rows=${direct820After002Head.length}.`,
    examples: occurrences820
      .slice(0, 8)
      .map((row) => `${row.cisi}:${row.prev}-820-${row.next}:${row.text}`)
      .join(' | '),
    kill_condition:
      'If 820 turns out restricted to one title/rank register after source normalization, revive semantic title value for 820.',
    promote_condition:
      'More broad terminal 820 rows, especially direct 002-H-820 rows, strengthen the closure-background reading.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  status: '125820_terminal_cap_test',
  risky_parse_bet:
    '`125-820` is a P086/governed title-continuation plus terminal-cap subtype, not free name text and not an `820` title value.',
  key_counts: {
    global_820_occurrences: occurrences820.length,
    global_820_terminal: terminal820.length,
    non125_prev_820_occurrences: non125Prev820.length,
    non125_prev_820_terminal: non125PrevTerminal820.length,
    global_125_820_occurrences: occurrences125820.length,
    global_125_820_terminal: occurrences125820.filter((row) => row.terminal_after_820 === 'true').length,
    governed_125_820: occurrences125820.filter((row) => row.governed_by_002 === 'true').length,
    direct_002_head_to_820_rows: direct820After002Head.length,
  },
  distributions: {
    prev_before_820: topCounts(countBy(occurrences820, (row) => row.prev), 12),
    next_after_820: topCounts(countBy(occurrences820, (row) => row.next), 12),
    governed_heads_for_125_820: topCounts(countBy(occurrences125820, (row) => row.governed_head), 12),
    direct_002_heads_to_820: topCounts(countBy(direct820After002Head, (row) => row.governed_head), 12),
  },
  decisions: [
    'Keep `125-820` as a P086-family terminal-cap subtype candidate-edge, not as a broad title value.',
    'Demote semantic wording for `820`; its broad terminal behavior makes it a closure/cap background sign until source evidence says otherwise.',
    'The next destructive test is source-binding Sktd-1 and M-41: if either loses strict terminal `125-820`, the subtype collapses back to wild pressure.',
  ],
};

writeCsv(path.join(reportsDir, `${prefix}_820_occurrences.csv`), occurrences820, [
  'checked_date',
  'cisi',
  'row_id',
  'site',
  'type',
  'symbol',
  'cult',
  'prev',
  'next',
  'terminal_after_820',
  'governed_by_002',
  'governed_head',
  'prev_before_002',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_125820_rows.csv`), occurrences125820, [
  'checked_date',
  'cisi',
  'row_id',
  'site',
  'type',
  'symbol',
  'cult',
  'prev_before_125',
  'next_after_820',
  'terminal_after_820',
  'governed_by_002',
  'governed_head',
  'prev_before_002',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_direct_002_head_to_820_rows.csv`), direct820After002Head, [
  'checked_date',
  'cisi',
  'row_id',
  'site',
  'type',
  'symbol',
  'cult',
  'prev_before_002',
  'governed_head',
  'next_after_820',
  'terminal_after_820',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), bets, [
  'checked_date',
  'bet_id',
  'tier',
  'claim',
  'support',
  'examples',
  'kill_condition',
  'promote_condition',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
