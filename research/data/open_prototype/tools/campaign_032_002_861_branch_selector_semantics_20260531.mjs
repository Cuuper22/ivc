// Semantics probe for ten candidate "branch selector" signs (125, 095, 705, 692, 707, 140,
// 346, 072, 530, 590) — signs proposed to fill the X slot in 002-390-X frames. For each one
// we ask: what company does it keep globally, and does that support a semantic label such as
// rank/title (125), administrative status (095), or hard terminal closure (692)? We read the
// filtered Indus inscription list (lipi/metadata_filtered.csv) and profile every occurrence
// of each selector: predecessors, successors, terminal share, object types, sites, and cult
// imagery, plus its specific 002-390 rows. A second pass studies "left qualifiers" — the sign
// just before 002 — to test whether signs like 235 steer which head and selector follow.
// Class labels and confidence-movement notes are assigned by fixed rules in the code.
// Writes selector-context, selector-row, and left-qualifier CSVs plus a JSON summary to
// data/open_prototype/reports.
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_branch_selector_semantics_20260531';

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

function topCounts(counts, n = 10) {
  return counts
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function share(count, total) {
  return total ? (count / total).toFixed(6) : '0.000000';
}

function signClassFromContext(sign, stats) {
  if (sign === '125') return 'rank_title_selector_candidate';
  if (sign === '095') return 'admin_status_selector_candidate';
  if (sign === '705') return 'terminal_390_selector_candidate_semantics_wild';
  if (sign === '692') return 'hard_terminal_closure_candidate';
  if (sign === '590') return 'embedded_formula_bridge_candidate';
  if (stats.after002390Count === 1 && stats.globalCount <= 6 && stats.terminalShare >= 0.6) {
    return 'rare_terminal_selector_wild';
  }
  if (stats.after002390Count === 1 && stats.terminalShare < 0.5) return 'continuation_selector_wild';
  return 'singleton_or_unclassified_selector_wild';
}

function confidenceMovement(sign, stats) {
  if (sign === '095') {
    return 'upgrade semantic class to candidate: global contexts are tablet/copper-heavy and 2/2 after 002-390 are terminal; generic closure narrowed';
  }
  if (sign === '705') {
    return 'formal terminal selector candidate under 002-390 because every 390-705 is after 002; remote/transfer semantics remain wild';
  }
  if (sign === '692') {
    return 'new candidate hard-terminal closure selector: high global terminal share and M-70 is terminal after 002-390';
  }
  if (sign === '125') return 'unchanged: candidate semantic rank/title, promoted only in narrow 235-002-(390/405)-...125 rule';
  if (sign === '590') return 'unchanged candidate bridge: after 002-390 it opens inherited 390-590-032 formula';
  if (stats.after002390Count === 1) return 'stays wild shot until a second comparable row appears or source morphology constrains it';
  return 'background selector';
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  tokens: signs(row.text),
}));

const selectorSigns = ['125', '095', '705', '692', '707', '140', '346', '072', '530', '590'];
const selectorContexts = [];
const selectorRows = [];
const before002 = [];

for (const row of rows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
    if (row.tokens[i] === '002') {
      before002.push({
        row,
        i,
        prev: row.tokens[i - 1] ?? '<START>',
        head: row.tokens[i + 1] ?? '<END>',
        x: row.tokens[i + 2] ?? '<END>',
        tail: row.tokens.slice(i + 1),
      });
    }
  }
}

for (const sign of selectorSigns) {
  const occurrences = [];
  for (const row of rows) {
    for (let i = 0; i < row.tokens.length; i += 1) {
      if (row.tokens[i] === sign) {
        occurrences.push({
          row,
          index: i,
          prev: row.tokens[i - 1] ?? '<START>',
          next: row.tokens[i + 1] ?? '<END>',
          prev2: row.tokens[i - 2] ?? '<START>',
        });
      }
    }
  }

  const after390 = occurrences.filter((occ) => occ.prev === '390');
  const after002390 = occurrences.filter((occ) => occ.prev2 === '002' && occ.prev === '390');
  const terminal = occurrences.filter((occ) => occ.next === '<END>');
  const nonSquareRectSeal = occurrences.filter((occ) => !['SEAL:S', 'SEAL:R'].includes(occ.row.type));
  const topPrev = countBy(occurrences, (occ) => occ.prev);
  const topNext = countBy(occurrences, (occ) => occ.next);
  const topType = countBy(occurrences, (occ) => occ.row.type);
  const topSite = countBy(occurrences, (occ) => occ.row.site);
  const topCult = countBy(occurrences, (occ) => occ.row.cult);
  const topPrevShare = topPrev.length ? topPrev[0][1] / occurrences.length : 0;
  const terminalShare = occurrences.length ? terminal.length / occurrences.length : 0;

  const stats = {
    globalCount: occurrences.length,
    after390Count: after390.length,
    after002390Count: after002390.length,
    terminalShare,
  };

  selectorContexts.push({
    checked_date: '2026-05-31',
    sign,
    global_count: String(occurrences.length),
    after_390_count: String(after390.length),
    after_002_390_count: String(after002390.length),
    terminal_count: String(terminal.length),
    terminal_share: terminalShare.toFixed(6),
    non_square_or_rect_seal_count: String(nonSquareRectSeal.length),
    non_square_or_rect_seal_share: share(nonSquareRectSeal.length, occurrences.length),
    top_prev_share: topPrevShare.toFixed(6),
    top_prev: topCounts(topPrev),
    top_next: topCounts(topNext),
    top_type: topCounts(topType),
    top_site: topCounts(topSite),
    top_cult: topCounts(topCult),
    model_class: signClassFromContext(sign, stats),
    confidence_movement: confidenceMovement(sign, stats),
    after_002_390_rows: after002390.map((occ) => `${occ.row.cisi || '-'}:${occ.row.text}`).join(' | '),
  });

  for (const occ of after002390) {
    selectorRows.push({
      checked_date: '2026-05-31',
      sign,
      cisi: occ.row.cisi || '-',
      row_id: occ.row.id,
      site: occ.row.site,
      type: occ.row.type,
      symbol: occ.row.symbol,
      cult: occ.row.cult,
      prev_before_002: occ.row.tokens[occ.index - 3] ?? '<START>',
      next_after_selector: occ.next,
      terminal_after_selector: String(occ.next === '<END>'),
      proposed_parse_class: signClassFromContext(sign, stats),
      text: occ.row.text,
    });
  }
}

const leftQualifierRows = [];
for (const [prev, cases] of countBy(before002, (item) => item.prev).map(([key]) => [
  key,
  before002.filter((item) => item.prev === key),
])) {
  const topHead = countBy(cases, (item) => item.head);
  const topHeadX = countBy(cases, (item) => `${item.head}-${item.x}`);
  const count235PromotedFamily = cases.filter(
    (item) => item.prev === '235' && ['390', '405'].includes(item.head) && item.tail.includes('125'),
  ).length;
  const count390705 = cases.filter((item) => item.head === '390' && item.x === '705').length;
  const count390125 = cases.filter((item) => item.head === '390' && item.x === '125').length;
  const count390095 = cases.filter((item) => item.head === '390' && item.x === '095').length;
  let modelImplication = 'background_left_qualifier';
  if (prev === '235') {
    modelImplication =
      'promoted_left_qualifier_rule_only_for_390_405: 235 before 002 selects 125 under P086-family heads but not under closure heads';
  } else if (['031', '388'].includes(prev)) {
    modelImplication =
      '705_steering_not_promoted: 031/388 before 002 mostly target closure heads; 390-705 remains head-conditioned not left-qualifier-conditioned';
  } else if (prev === '004') {
    modelImplication = 'neutral_qualifier_candidate: same left sign permits 390-095 and 390-125';
  } else if (prev === '032') {
    modelImplication = 'hinge_qualifier_candidate: can feed 390-692 and 390-590 bridge but mostly feeds closure heads';
  }

  leftQualifierRows.push({
    checked_date: '2026-05-31',
    prev_before_002: prev,
    cases: String(cases.length),
    top_head_after_002: topCounts(topHead),
    top_head_x_after_002: topCounts(topHeadX),
    count_390_125: String(count390125),
    count_390_095: String(count390095),
    count_390_705: String(count390705),
    count_235_390_405_tail_has_125: String(count235PromotedFamily),
    model_implication: modelImplication,
    examples: cases
      .slice(0, 12)
      .map((item) => `${item.row.cisi || '-'}:${item.tail.join('-')}:${item.row.type}:${item.row.site}`)
      .join(' | '),
  });
}

leftQualifierRows.sort((a, b) => Number(b.cases) - Number(a.cases) || a.prev_before_002.localeCompare(b.prev_before_002));
selectorContexts.sort((a, b) => Number(b.after_002_390_count) - Number(a.after_002_390_count) || a.sign.localeCompare(b.sign, undefined, { numeric: true }));
selectorRows.sort((a, b) => a.sign.localeCompare(b.sign, undefined, { numeric: true }) || a.cisi.localeCompare(b.cisi));

const selectorBySign = Object.fromEntries(selectorContexts.map((row) => [row.sign, row]));
const summary = {
  checked_date: '2026-05-31',
  status: 'branch_selector_semantics_probe',
  hypotheses_tested: [
    '095 as administrative/status selector rather than personal name',
    '705 as remote/transfer selector versus copied 033-705 formula leakage',
    '692 as hard terminal closure selector',
    'left qualifier steering: 235 is special; 031/388 -> 705 is only a wild head-conditioned effect',
  ],
  decisions: [
    '095 moves from wild shot to candidate for administrative/status class; closure is narrowed to the 002-390 environment.',
    '705 moves to candidate only as a formal terminal selector under 002-390; remote/transfer semantics remain wild shot.',
    '692 becomes a candidate hard-terminal closure selector.',
    '031/388 steering into 705 is not promoted because 031/388 before 002 mostly feed closure heads, not 390-705.',
    '004 behaves as a neutral qualifier candidate because it permits both 390-095 and 390-125.',
  ],
  key_counts: {
    sign_095: selectorBySign['095'],
    sign_705: selectorBySign['705'],
    sign_692: selectorBySign['692'],
    sign_125: selectorBySign['125'],
  },
};

writeCsv(path.join(reportsDir, `${prefix}_selector_contexts.csv`), selectorContexts, [
  'checked_date',
  'sign',
  'global_count',
  'after_390_count',
  'after_002_390_count',
  'terminal_count',
  'terminal_share',
  'non_square_or_rect_seal_count',
  'non_square_or_rect_seal_share',
  'top_prev_share',
  'top_prev',
  'top_next',
  'top_type',
  'top_site',
  'top_cult',
  'model_class',
  'confidence_movement',
  'after_002_390_rows',
]);

writeCsv(path.join(reportsDir, `${prefix}_after002390_selector_rows.csv`), selectorRows, [
  'checked_date',
  'sign',
  'cisi',
  'row_id',
  'site',
  'type',
  'symbol',
  'cult',
  'prev_before_002',
  'next_after_selector',
  'terminal_after_selector',
  'proposed_parse_class',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_left_qualifier_steering.csv`), leftQualifierRows, [
  'checked_date',
  'prev_before_002',
  'cases',
  'top_head_after_002',
  'top_head_x_after_002',
  'count_390_125',
  'count_390_095',
  'count_390_705',
  'count_235_390_405_tail_has_125',
  'model_implication',
  'examples',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
