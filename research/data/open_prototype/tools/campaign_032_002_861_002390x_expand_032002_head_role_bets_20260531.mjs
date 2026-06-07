import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_032002_head_role_bets_20260531';
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

const frameRows = [];
for (const row of rows) {
  for (let i = 0; i < row.tokens.length - 1; i += 1) {
    if (row.tokens[i] !== '032' || row.tokens[i + 1] !== '002') continue;
    const head = row.tokens[i + 2] ?? '<END>';
    const tail = row.tokens.slice(i + 3);
    frameRows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      symbol: row.symbol,
      cult: row.cult,
      prev_before_032: row.tokens[i - 1] ?? '<START>',
      head_after_002: head,
      next_after_head: tail[0] ?? '<END>',
      tail_after_head: tail.join(' ') || '<END>',
      terminal_after_head: String(tail.length === 0),
      exact_740205_prefix: String(
        i >= 2 && row.tokens[i - 2] === '740' && row.tokens[i - 1] === '205',
      ),
      text: row.text,
    });
  }
}

const headSummary = [...new Set(frameRows.map((row) => row.head_after_002))]
  .sort((a, b) => {
    const ac = frameRows.filter((row) => row.head_after_002 === a).length;
    const bc = frameRows.filter((row) => row.head_after_002 === b).length;
    return bc - ac || a.localeCompare(b, undefined, { numeric: true });
  })
  .map((head) => {
    const subset = frameRows.filter((row) => row.head_after_002 === head);
    const terminal = subset.filter((row) => row.terminal_after_head === 'true').length;
    return {
      checked_date: checkedDate,
      head_after_002: head,
      rows: String(subset.length),
      terminal_rows: String(terminal),
      terminal_share: fixed(terminal / subset.length),
      next_entropy_bits: fixed(entropy(subset.map((row) => row.next_after_head))),
      top_next_after_head: countBy(subset, 'next_after_head'),
      prev_before_032: countBy(subset, 'prev_before_032'),
      sites: countBy(subset, 'site'),
      types: countBy(subset, 'type'),
      examples: examples(subset),
    };
  });

const closedHeads = new Set(
  headSummary
    .filter((row) => Number(row.rows) >= 5 && Number(row.terminal_share) >= 0.8)
    .map((row) => row.head_after_002),
);
const peripheralClosedHeads = new Set(
  headSummary
    .filter(
      (row) =>
        !closedHeads.has(row.head_after_002) &&
        Number(row.rows) >= 3 &&
        Number(row.terminal_share) >= 0.7,
    )
    .map((row) => row.head_after_002),
);

for (const row of frameRows) {
  row.head_class =
    row.head_after_002 === '390'
      ? 'open_target_head'
      : closedHeads.has(row.head_after_002)
        ? 'closed_frequent_head'
        : peripheralClosedHeads.has(row.head_after_002)
          ? 'peripheral_closed_dirty_head'
        : row.terminal_after_head === 'true'
          ? 'closed_singleton_or_sparse'
          : 'open_or_mixed_sparse';
}

const prevSummary = [...new Set(frameRows.map((row) => row.prev_before_032))]
  .sort((a, b) => {
    const ac = frameRows.filter((row) => row.prev_before_032 === a).length;
    const bc = frameRows.filter((row) => row.prev_before_032 === b).length;
    return bc - ac || a.localeCompare(b, undefined, { numeric: true });
  })
  .map((prev) => {
    const subset = frameRows.filter((row) => row.prev_before_032 === prev);
    const terminal = subset.filter((row) => row.terminal_after_head === 'true').length;
    const closed = subset.filter((row) => closedHeads.has(row.head_after_002)).length;
    const open390 = subset.filter((row) => row.head_after_002 === '390').length;
    return {
      checked_date: checkedDate,
      prev_before_032: prev,
      rows: String(subset.length),
      terminal_rows: String(terminal),
      terminal_share: fixed(terminal / subset.length),
      closed_frequent_head_rows: String(closed),
      closed_frequent_head_share: fixed(closed / subset.length),
      open_390_rows: String(open390),
      head_after_002: countBy(subset, 'head_after_002'),
      head_class: countBy(subset, 'head_class'),
      sites: countBy(subset, 'site'),
      examples: examples(subset),
    };
  });

const prev220 = frameRows.filter((row) => row.prev_before_032 === '220');
const prev205 = frameRows.filter((row) => row.prev_before_032 === '205');
const prev590 = frameRows.filter((row) => row.prev_before_032 === '590');
const target390 = frameRows.filter((row) => row.head_after_002 === '390');
const frequentClosed = frameRows.filter((row) => closedHeads.has(row.head_after_002));
const closedShare =
  prev220.length === 0 ? 0 : prev220.filter((row) => closedHeads.has(row.head_after_002)).length / prev220.length;
const terminalShare220 =
  prev220.length === 0 ? 0 : prev220.filter((row) => row.terminal_after_head === 'true').length / prev220.length;

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_032002_CLOSED_HEAD_SET',
    tier: frequentClosed.length >= 20 ? 'candidate' : 'wild_shot',
    risky_bet:
      `The frequent heads after 032-002 are a closed-head class: ${[...closedHeads].join('/')} behave as terminal or near-terminal classifier outputs; ${[...peripheralClosedHeads].join('/')} is dirtier peripheral pressure.`,
    current_test:
      `closed-head rows=${frequentClosed.length}/${frameRows.length}; head summaries=${headSummary
        .filter((row) => closedHeads.has(row.head_after_002))
        .map((row) => `${row.head_after_002}:${row.rows},terminal=${row.terminal_share}`)
        .join(';')}; peripheral=${[...peripheralClosedHeads].join('/') || 'none'}.`,
    evidence: examples(frequentClosed),
    destructive_prediction:
      'Source-visible rows where these heads continue productively, or a normalization collapse into one copied seal family, demote the closed-head class.',
    promotion_prediction:
      'More source-visible 032-002-817/820/861 rows ending terminally across sites promote the class.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_220032002_TERMINAL_ENVIRONMENT',
    tier: closedShare >= 0.65 && prev220.every((row) => row.head_after_002 !== '390') ? 'candidate' : 'wild_shot',
    risky_bet:
      'The left context 220-032-002 is a terminal classifier environment that suppresses open 390 selection.',
    current_test:
      `220-032-002 rows=${prev220.length}; terminal_share=${fixed(terminalShare220)}; closed_head_share=${fixed(closedShare)}; 390_rows=0; heads=${countBy(prev220, 'head_after_002')}.`,
    evidence: examples(prev220),
    destructive_prediction:
      'A strict 220-032-002-390-X row or widespread nonterminal 220-032-002-H tails demotes this environment bet.',
    promotion_prediction:
      'More independent 220-032-002 rows selecting terminal 817/820/861-like heads promote 220 as a terminal-frame conditioner.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_205032002_PAYLOAD_ALTERNATION',
    tier: prev205.length === 2 && new Set(prev205.map((row) => row.head_after_002)).size === 2 ? 'candidate_edge' : 'wild_shot',
    risky_bet:
      'The 205-032-002 environment is the local payload-alternation lane, selecting M-143 252-840 versus 3335.1 390-590-032.',
    current_test: `205-032-002 rows=${prev205.length}; heads=${countBy(prev205, 'head_after_002')}; classes=${countBy(prev205, 'head_class')}.`,
    evidence: examples(prev205),
    destructive_prediction:
      'If 3335.1 fails source-binding or more 205-032-002 rows select ordinary closed heads, demote this to coincidence.',
    promotion_prediction:
      'A source-bound 3335.1 plus another 205-032-002 open/formula payload row promotes the lane.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_390_IS_RARE_OPEN_LANE_NOT_032002_DEFAULT',
    tier: target390.length <= 3 && target390.every((row) => row.terminal_after_head === 'false') ? 'candidate' : 'wild_shot',
    risky_bet:
      '390 is a rare open lane selected by special left contexts inside 032-002, not the default value of the 032-002 frame.',
    current_test:
      `032-002-390 rows=${target390.length}/${frameRows.length}; terminal_after_390=0; prev contexts=${countBy(target390, 'prev_before_032')}.`,
    evidence: examples(target390),
    destructive_prediction:
      'Frequent source-visible 032-002-390 terminal rows or 390 after common 220-032-002 would demote the rare-open-lane parse.',
    promotion_prediction:
      'More rare-context nonterminal 032-002-390 rows promote 390 as a selected open payload lane.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_590032002_TAG_PIVOT',
    tier: prev590.length >= 3 ? 'wild_shot' : 'too_thin',
    risky_bet:
      'When 032 follows the 390-590 formula chunk, 032-002 pivots into tag-like terminal heads rather than the seal-side open 390 lane.',
    current_test: `590-032-002 rows=${prev590.length}; heads=${countBy(prev590, 'head_after_002')}; sites=${countBy(prev590, 'site')}; types=${countBy(prev590, 'type')}.`,
    evidence: examples(prev590),
    destructive_prediction:
      'If 590-032-002 appears source-visible on seals with open 390-like tails, demote the tag-pivot parse.',
    promotion_prediction:
      'More Lothal/tag 590-032-002 rows selecting terminal 000/880-like heads strengthen the pivot parse.',
  },
];

writeCsv(
  path.join(reportsDir, `${prefix}_032002_rows.csv`),
  frameRows,
  [
    'checked_date',
    'object',
    'row_id',
    'site',
    'type',
    'symbol',
    'cult',
    'prev_before_032',
    'head_after_002',
    'head_class',
    'next_after_head',
    'tail_after_head',
    'terminal_after_head',
    'exact_740205_prefix',
    'text',
  ],
);
writeCsv(
  path.join(reportsDir, `${prefix}_head_summary.csv`),
  headSummary,
  [
    'checked_date',
    'head_after_002',
    'rows',
    'terminal_rows',
    'terminal_share',
    'next_entropy_bits',
    'top_next_after_head',
    'prev_before_032',
    'sites',
    'types',
    'examples',
  ],
);
writeCsv(
  path.join(reportsDir, `${prefix}_prev_summary.csv`),
  prevSummary,
  [
    'checked_date',
    'prev_before_032',
    'rows',
    'terminal_rows',
    'terminal_share',
    'closed_frequent_head_rows',
    'closed_frequent_head_share',
    'open_390_rows',
    'head_after_002',
    'head_class',
    'sites',
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
  status: 'expand_032002_head_role_bets',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: rows.length,
    frame_032002_rows: frameRows.length,
    closed_heads: [...closedHeads],
    prev_220_rows: prev220.length,
    prev_205_rows: prev205.length,
    prev_590_rows: prev590.length,
    target_390_rows: target390.length,
    peripheral_closed_heads: [...peripheralClosedHeads],
  },
  bets: betRows.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
