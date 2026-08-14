import fs from 'node:fs';
import path from 'node:path';

// The sign directly left of a 002-390 frame does not reliably predict which
// branch X gets selected — the same final sign can precede different
// branches. This script tests whether widening the window to two signs (the
// "left bigram") removes those collisions, making branch selection a
// compound-left routing rule. It reads lipi/metadata_filtered.csv,
// deduplicates by sign sequence, collects every 002-390-X frame with its left
// bigram and a branch-shape label (rank-continue 125, one-complement 530,
// formula payload 590-032, terminal selectors, other), and summarizes branch
// diversity per final-left sign and per left bigram. If finals collide but
// bigrams do not, the router bet earns "candidate_edge". Three narrower bets
// ride along: 235 as a direct rank trigger while 032/004 need compound
// disambiguation, 004 routed by its previous sign (220-004 closes via 095,
// 390-004 continues via 125), and 032 routed likewise (226-032 to 692,
// 205-032 to 590-032). Writes frames, both summaries, and bets as CSVs plus a
// summary JSON to data/open_prototype/reports.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_compound_left_context_router_20260531';
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
    .map((row) => `${row.object}:${row.left_bigram}-002-390-${row.branch_after_390}${row.tail_after_branch === '<END>' ? '' : `-${row.tail_after_branch}`}`)
    .join(' | ');
}

function uniq(values) {
  return [...new Set(values)].sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
}

function branchShape(row) {
  if (row.branch_after_390 === '125') return 'rank_continue_125';
  if (row.branch_after_390 === '530') return 'one_complement_linker';
  if (row.branch_after_390 === '590' && row.tail_after_branch === '032') return 'formula_payload_590032';
  if (['072', '095', '140', '346', '692', '705', '707'].includes(row.branch_after_390)) return 'terminal_selector';
  return row.tail_after_branch === '<END>' ? 'other_terminal' : 'other_continuing';
}

fs.mkdirSync(reportsDir, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  tokens: signs(row.text),
}));
const rows = [...new Map(rawRows.map((row) => [row.tokens.join(' '), row])).values()];

const frames = [];
for (const row of rows) {
  for (let i = 0; i < row.tokens.length - 2; i += 1) {
    if (row.tokens[i] !== '002' || row.tokens[i + 1] !== '390') continue;
    const branch = row.tokens[i + 2];
    const tail = row.tokens.slice(i + 3);
    const leftFinal = row.tokens[i - 1] ?? '<START>';
    const leftPenultimate = row.tokens[i - 2] ?? '<START>';
    frames.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      symbol: row.symbol,
      cult: row.cult,
      left_penultimate: leftPenultimate,
      left_final: leftFinal,
      left_bigram: `${leftPenultimate}-${leftFinal}`,
      left_contains_032: String(row.tokens.slice(0, i).includes('032')),
      left_contains_235: String(row.tokens.slice(0, i).includes('235')),
      branch_after_390: branch,
      tail_after_branch: tail.join(' ') || '<END>',
      terminal_after_branch: String(tail.length === 0),
      branch_shape: '',
      text: row.text,
    });
  }
}
for (const frame of frames) frame.branch_shape = branchShape(frame);

function summarize(groupField) {
  return uniq(frames.map((row) => row[groupField])).map((key) => {
    const group = frames.filter((row) => row[groupField] === key);
    const branchValues = uniq(group.map((row) => row.branch_after_390));
    const shapes = uniq(group.map((row) => row.branch_shape));
    return {
      checked_date: checkedDate,
      group_field: groupField,
      group_key: key,
      rows: String(group.length),
      branch_values: branchValues.join(';'),
      branch_value_count: String(branchValues.length),
      branch_shapes: shapes.join(';'),
      branch_shape_count: String(shapes.length),
      sites: countBy(group, 'site'),
      types: countBy(group, 'type'),
      examples: examples(group),
    };
  });
}

const leftFinalSummary = summarize('left_final');
const leftBigramSummary = summarize('left_bigram');
const dirtyFinals = leftFinalSummary.filter((row) => Number(row.branch_value_count) > 1);
const dirtyBigrams = leftBigramSummary.filter((row) => Number(row.branch_value_count) > 1);

function groupRows(field, key) {
  return frames.filter((row) => row[field] === key);
}

const final235 = groupRows('left_final', '235');
const final032 = groupRows('left_final', '032');
const final004 = groupRows('left_final', '004');
const bigram220004 = groupRows('left_bigram', '220-004');
const bigram390004 = groupRows('left_bigram', '390-004');
const bigram226032 = groupRows('left_bigram', '226-032');
const bigram205032 = groupRows('left_bigram', '205-032');

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_COMPOUND_LEFT_CONTEXT_ROUTER',
    tier: dirtyFinals.length > 0 && dirtyBigrams.length === 0 ? 'candidate_edge' : 'wild_shot',
    risky_bet:
      'Inside 002-390-X, final-left signs like 032 and 004 are not direct selectors; the two-sign left environment routes the branch.',
    current_test:
      `final-left collision groups=${dirtyFinals.map((row) => `${row.group_key}:${row.branch_values}`).join('|') || 'none'}; left-bigram collision groups=${dirtyBigrams.map((row) => `${row.group_key}:${row.branch_values}`).join('|') || 'none'}.`,
    evidence: examples(frames),
    destructive_prediction:
      'If the same left bigram selects different branch values in strict comparable rows, demote compound-left routing.',
    promotion_prediction:
      'More repeated left bigrams that preserve branch choice while final signs split promote compound-left routing.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_235_DIRECT_TRIGGER_VS_032004_COMPOUND',
    tier:
      final235.length >= 2 &&
      uniq(final235.map((row) => row.branch_after_390)).join(';') === '125' &&
      dirtyFinals.some((row) => row.group_key === '032') &&
      dirtyFinals.some((row) => row.group_key === '004')
        ? 'candidate'
        : 'wild_shot',
    risky_bet:
      '235 behaves more like a direct P086 rank trigger, while 032 and 004 require compound-left disambiguation.',
    current_test:
      `235 branches=${countBy(final235, 'branch_after_390')}; 032 branches=${countBy(final032, 'branch_after_390')}; 004 branches=${countBy(final004, 'branch_after_390')}.`,
    evidence: `235=${examples(final235)} | 032=${examples(final032)} | 004=${examples(final004)}`,
    destructive_prediction:
      'A comparable 235-002-390 row without 125 kills direct-trigger status; repeated final-032 or final-004 rows with one branch only demote compound treatment.',
    promotion_prediction:
      'A new 235-002-390/405 row with 125 and new 032/004 compound splits strengthen the asymmetry.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_004_BIGRAM_STATUS_RANK_SPLIT',
    tier:
      bigram220004.some((row) => row.branch_after_390 === '095') &&
      bigram390004.some((row) => row.branch_after_390 === '125')
        ? 'candidate_edge'
        : 'wild_shot',
    risky_bet:
      '004 is a neutral qualifier whose previous sign routes it: 220-004 closes through 095, while 390-004 continues through 125.',
    current_test:
      `220-004 branches=${countBy(bigram220004, 'branch_after_390')}; 390-004 branches=${countBy(bigram390004, 'branch_after_390')}.`,
    evidence: `220-004=${examples(bigram220004)} | 390-004=${examples(bigram390004)}`,
    destructive_prediction:
      'A strict 220-004 row selecting 125 or a 390-004 row selecting 095 demotes the bigram split.',
    promotion_prediction:
      'Another source-visible 220-004 -> 095 or 390-004 -> 125 row promotes 004 as neutral-plus-router context.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_032_BIGRAM_RESULT_FORMULA_SPLIT',
    tier:
      bigram226032.some((row) => row.branch_after_390 === '692') &&
      bigram205032.some((row) => row.branch_after_390 === '590' && row.tail_after_branch === '032')
        ? 'candidate_edge'
        : 'wild_shot',
    risky_bet:
      '032 is a head-selection context whose previous sign routes target 390: 226-032 selects terminal/result 692, while 205-032 selects formula payload 590-032.',
    current_test:
      `226-032 branches=${countBy(bigram226032, 'branch_after_390')}; 205-032 branches=${countBy(bigram205032, 'branch_after_390')}.`,
    evidence: `226-032=${examples(bigram226032)} | 205-032=${examples(bigram205032)}`,
    destructive_prediction:
      'A strict 226-032 row selecting 590-032 or a strict 205-032 row selecting 692 collapses this split.',
    promotion_prediction:
      'Source-bound 3335.1 plus another 205-032 formula-payload row promotes the 032 bigram router.',
  },
];

writeCsv(
  path.join(reportsDir, `${prefix}_target_frames.csv`),
  frames,
  [
    'checked_date',
    'object',
    'row_id',
    'site',
    'type',
    'symbol',
    'cult',
    'left_penultimate',
    'left_final',
    'left_bigram',
    'left_contains_032',
    'left_contains_235',
    'branch_after_390',
    'tail_after_branch',
    'terminal_after_branch',
    'branch_shape',
    'text',
  ],
);
writeCsv(
  path.join(reportsDir, `${prefix}_left_final_summary.csv`),
  leftFinalSummary,
  [
    'checked_date',
    'group_field',
    'group_key',
    'rows',
    'branch_values',
    'branch_value_count',
    'branch_shapes',
    'branch_shape_count',
    'sites',
    'types',
    'examples',
  ],
);
writeCsv(
  path.join(reportsDir, `${prefix}_left_bigram_summary.csv`),
  leftBigramSummary,
  [
    'checked_date',
    'group_field',
    'group_key',
    'rows',
    'branch_values',
    'branch_value_count',
    'branch_shapes',
    'branch_shape_count',
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
  status: 'expand_compound_left_context_router',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: rows.length,
    target_002390_frames: frames.length,
    final_left_collision_groups: dirtyFinals.map((row) => ({ key: row.group_key, branches: row.branch_values })),
    left_bigram_collision_groups: dirtyBigrams.map((row) => ({ key: row.group_key, branches: row.branch_values })),
  },
  bets: betRows.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
