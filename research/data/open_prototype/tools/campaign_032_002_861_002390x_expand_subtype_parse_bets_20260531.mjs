import fs from 'node:fs';
import path from 'node:path';

// This script sharpens the 002-H-X parse into per-sign subrules and tests them. It reads
// Indus inscriptions from data/open_prototype/lipi/metadata_filtered.csv, dedupes to unique
// sign sequences, indexes every occurrence of every sign with its neighbors, and extracts all
// 002-H-X windows. From those it probes five specific claims: that 002 converts 095 into a
// terminal label (while plain 390-095 can continue); that head 320 licenses a 125 cap after
// the otherwise terminal 705; that 530 selects complements which are already terminal-biased
// signs corpus-wide; that the tail after 125 is chosen by the head class, not by 125 itself;
// and that 390 is a right-edge host whose row closes or continues according to the X subtype
// (each X gets a predicted class, and each 390 row is scored pass/fail against it). The five
// bets, the classified 390 rows, the 125 head families, and the 530 complements go to CSVs in
// reports/, plus a summary JSON.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_subtype_parse_bets_20260531';
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

function ratio(numerator, denominator) {
  return denominator ? `${numerator}/${denominator}` : '0/0';
}

function pct(numerator, denominator) {
  return denominator ? (numerator / denominator).toFixed(6) : '';
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

function uniqueRowsByText(rows) {
  return [...new Map(rows.map((row) => [row.tokens.join(' '), row])).values()];
}

function tailFamily(tail) {
  if (!tail.length) return '<END>';
  if (tail[0] === '632' && tail[1] === '032') return '632-032_family';
  if (tail[0] === '032') return '032_family';
  if (tail[0] === '820') return '820_cap';
  return tail.join(' ');
}

function examples(rows, n = 6) {
  return rows
    .slice(0, n)
    .map((row) => `${row.object}:${row.text}`)
    .join(' | ');
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = uniqueRowsByText(
  parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
    ...row,
    object: objectId(row),
    tokens: signs(row.text),
  })),
);

const xRows = [];
const occurrencesBySign = new Map();
for (const row of rows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
    const sign = row.tokens[i];
    const occurrence = {
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      sign,
      index: String(i),
      left_2: row.tokens[i - 2] ?? '<START>',
      left_1: row.tokens[i - 1] ?? '<START>',
      right_1: row.tokens[i + 1] ?? '<END>',
      terminal: String(i === row.tokens.length - 1),
      tail_after_sign: row.tokens.slice(i + 1).join(' ') || '<END>',
      text: row.text,
    };
    if (!occurrencesBySign.has(sign)) occurrencesBySign.set(sign, []);
    occurrencesBySign.get(sign).push(occurrence);
    if (row.tokens[i] !== '002' || i + 2 >= row.tokens.length) continue;
    const head = row.tokens[i + 1];
    const x = row.tokens[i + 2];
    const tail = row.tokens.slice(i + 3);
    xRows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      head,
      x,
      tail_after_x: tail.join(' ') || '<END>',
      tail_family: tailFamily(tail),
      open: String(tail.length > 0),
      text: row.text,
    });
  }
}

function globalTerminalProfile(sign) {
  const occ = occurrencesBySign.get(sign) ?? [];
  const terminal = occ.filter((row) => row.terminal === 'true').length;
  return {
    sign,
    occurrences: occ.length,
    terminal,
    terminal_share: pct(terminal, occ.length),
  };
}

const x095 = xRows.filter((row) => row.x === '095');
const x390095 = xRows.filter((row) => row.head === '390' && row.x === '095');
const nonX390095 = (occurrencesBySign.get('095') ?? []).filter(
  (row) => row.left_1 === '390' && row.left_2 !== '002',
);

const x705 = xRows.filter((row) => row.x === '705');
const x320705 = xRows.filter((row) => row.head === '320' && row.x === '705');
const x390705 = xRows.filter((row) => row.head === '390' && row.x === '705');

const x530 = xRows.filter((row) => row.x === '530');
const x530Complements = x530.map((row) => ({
  ...row,
  complement: row.tail_after_x.split(' ')[0],
  complement_global_terminal_share: globalTerminalProfile(row.tail_after_x.split(' ')[0]).terminal_share,
  complement_global_terminal: `${globalTerminalProfile(row.tail_after_x.split(' ')[0]).terminal}/${globalTerminalProfile(row.tail_after_x.split(' ')[0]).occurrences}`,
}));
const highTerminalComplements = x530Complements.filter((row) => Number(row.complement_global_terminal_share) >= 0.45).length;

const x125 = xRows.filter((row) => row.x === '125');
const x125HeadFamilies = [...new Set(x125.map((row) => row.head))].map((head) => {
  const headRows = x125.filter((row) => row.head === head);
  return {
    checked_date: checkedDate,
    head,
    rows: String(headRows.length),
    tail_families: countBy(headRows, (row) => row.tail_family),
    sites: countBy(headRows, (row) => row.site),
    objects: headRows.map((row) => row.object).join(';'),
    decision:
      headRows.length >= 2 && new Set(headRows.map((row) => row.tail_family)).size === 1
        ? 'head_selects_tail_family'
        : headRows.length >= 2
          ? 'head_has_tail_menu'
          : 'singleton_head_bait',
  };
});

function x390ClassPrediction(row) {
  if (row.x === '095') return 'terminal_label_close';
  if (row.x === '705') return 'terminal_default_close';
  if (row.x === '125') return 'tail_menu_open';
  if (row.x === '530') return 'one_complement_open';
  if (row.x === '590') return 'open_extender';
  if (['072', '140', '346', '707'].includes(row.x)) return 'terminal_bait_close';
  if (row.x === '692') return 'raw_boundary_bait';
  return 'unclassified';
}

function predictionPass(row) {
  const prediction = x390ClassPrediction(row);
  const isOpen = row.open === 'true';
  if (prediction.includes('close')) return !isOpen;
  if (prediction.includes('open')) return isOpen;
  return null;
}

const x390Rows = xRows
  .filter((row) => row.head === '390')
  .map((row) => ({
    ...row,
    predicted_class: x390ClassPrediction(row),
    prediction_pass: String(predictionPass(row)),
  }));

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_095_SLOT_POLARITY_CONVERSION',
    tier: x390095.length >= 2 && nonX390095.length >= 1 && x390095.every((row) => row.open === 'false') ? 'candidate' : 'wild_shot',
    risky_bet:
      '`002-H-095` converts `095` into a terminal class-label; without `002`, even `390-095` can continue as ordinary syntax.',
    current_test:
      `002-390-095 closes=${ratio(x390095.filter((row) => row.open === 'false').length, x390095.length)}; non-002 390-095 continues=${ratio(nonX390095.filter((row) => row.terminal === 'false').length, nonX390095.length)}.`,
    evidence: `${examples(x390095)} || non-X ${examples(nonX390095)}`,
    destructive_prediction:
      'A real `002-390-095-Y` continuation kills the conversion bet. More terminal non-002 `390-095` rows weaken it.',
    promotion_prediction:
      'Another closed `002-H-095` under a non-390 head plus another open non-002 H-095 row promotes context-function over raw sign value.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_705_HEAD320_CAP_LICENSE',
    tier: x320705.length === 1 && x320705[0]?.tail_family === '820_cap' ? 'wild_shot' : 'candidate_edge',
    risky_bet:
      '`705` is terminal-default, but head `320` specifically licenses a following `125` cap; head `390` should not.',
    current_test:
      `320-705 tails=${countBy(x320705, (row) => row.tail_after_x)}; 390-705 closes=${ratio(x390705.filter((row) => row.open === 'false').length, x390705.length)}; all 705 tails=${countBy(x705, (row) => row.tail_after_x)}.`,
    evidence: examples(x705),
    destructive_prediction:
      'A `002-390-705-Y` continuation or a `002-320-705` row without `125` breaks the head-licensed exception.',
    promotion_prediction:
      'A second `002-320-705-125` row, especially outside Mohenjo-daro square seals, promotes the exception from one-off to subrule.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_530_COMPLEMENTIZER_SELECTS_CLOSED_COMPLEMENTS',
    tier: x530.length === 4 && highTerminalComplements >= 2 ? 'candidate' : 'wild_shot',
    risky_bet:
      '`530` is not just one-complement; it selects complements that are terminal-biased or boundary-compatible signs.',
    current_test:
      `530 complements=${x530Complements.map((row) => `${row.object}:${row.complement}:${row.complement_global_terminal}`).join(';')}; high-terminal complements=${ratio(highTerminalComplements, x530Complements.length)}.`,
    evidence: examples(x530Complements),
    destructive_prediction:
      'A future `002-H-530-Y` where Y is globally continuation-biased and the row still closes would demote selection to pure positional linker.',
    promotion_prediction:
      'New 530 rows whose complements are independently terminal-biased strengthen complement-class selection.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_125_HEAD_CLASS_TAIL_ROUTER',
    tier: x125HeadFamilies.some((row) => row.decision === 'head_selects_tail_family') ? 'candidate' : 'wild_shot',
    risky_bet:
      '`125` is a tail router whose output is selected by the preceding head class, not by `125` alone.',
    current_test:
      `head-tail families=${x125HeadFamilies.map((row) => `${row.head}:${row.tail_families}`).join('|')}.`,
    evidence: examples(x125),
    destructive_prediction:
      'A new `002-610-125` row not followed by `032`, or repeated heads with incompatible tails, kills the head-router version.',
    promotion_prediction:
      'More repeated heads choosing the same tail family promotes `125` from menu operator to head-conditioned router.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_390_RIGHT_EDGE_HOST_BY_X_SUBTYPE',
    tier:
      x390Rows.filter((row) => predictionPass(row) !== null).length >= 6 &&
      x390Rows.filter((row) => predictionPass(row) === true).length >= 5
        ? 'candidate'
        : 'wild_shot',
    risky_bet:
      '`390` is a right-edge host: it contributes a structural head environment, while the X subtype predicts whether the row closes or continues.',
    current_test:
      `classified 390 rows pass=${ratio(x390Rows.filter((row) => predictionPass(row) === true).length, x390Rows.filter((row) => predictionPass(row) !== null).length)}; class counts=${countBy(x390Rows, (row) => row.predicted_class)}.`,
    evidence: examples(x390Rows),
    destructive_prediction:
      'If `390` rows with the same X subtype split unpredictably across continuation behavior, the host-by-X model dies.',
    promotion_prediction:
      'A held-out `390` row whose continuation matches its X subtype promotes `390` as structural head instead of value sign.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'subtype_parse_bets',
  rows: {
    x_rows: xRows.length,
    x095: x095.length,
    x705: x705.length,
    x530: x530.length,
    x125: x125.length,
    x390: x390Rows.length,
  },
  bets: betRows.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), betRows, [
  'checked_date',
  'bet_id',
  'tier',
  'risky_bet',
  'current_test',
  'evidence',
  'destructive_prediction',
  'promotion_prediction',
]);

writeCsv(path.join(reportsDir, `${prefix}_x390_rows.csv`), x390Rows, [
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
  'tail_family',
  'open',
  'predicted_class',
  'prediction_pass',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_x125_head_families.csv`), x125HeadFamilies, [
  'checked_date',
  'head',
  'rows',
  'tail_families',
  'sites',
  'objects',
  'decision',
]);

writeCsv(path.join(reportsDir, `${prefix}_x530_complements.csv`), x530Complements, [
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
  'tail_family',
  'open',
  'complement',
  'complement_global_terminal_share',
  'complement_global_terminal',
  'text',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
