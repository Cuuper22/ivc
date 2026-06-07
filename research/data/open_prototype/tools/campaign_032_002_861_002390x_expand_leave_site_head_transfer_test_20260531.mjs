import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const checkedDate = '2026-05-31';
const prefix = 'campaign_032_002_861_002390x_expand_leave_site_head_transfer_test_20260531';

const terminalBoosters = new Set([
  '000',
  '031',
  '416',
  '575',
  '317',
  '705',
  '741',
  '491',
  '095',
  '260',
  '820',
  '140',
  '165',
  '603',
]);
const openOperators = new Set(['125', '455', '530', '003', '861', '065', '035', '906', '460', '090']);

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
  for (const row of rows) lines.push(fields.map((fieldName) => csvEscape(row[fieldName])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function tokens(text) {
  return text.match(/\d{3}/g) ?? [];
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function polarity(x) {
  if (terminalBoosters.has(x)) return 'terminal_booster';
  if (openOperators.has(x)) return 'open_operator';
  return 'other';
}

function tally(values) {
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([value, count]) => `${value}:${count}`)
    .join(';');
}

function majority(rows) {
  const terminal = rows.filter((row) => row.terminal).length;
  const open = rows.length - terminal;
  if (terminal === open) return { prediction: 'tie', terminal, open };
  return { prediction: terminal > open ? 'terminal' : 'open', terminal, open };
}

function accuracy(rows, field) {
  const predicted = rows.filter((row) => row[field] === 'terminal' || row[field] === 'open');
  const correct = predicted.filter((row) => row.actual === row[field]);
  return {
    predicted: predicted.length,
    correct: correct.length,
    accuracy: predicted.length ? correct.length / predicted.length : 0,
  };
}

function pct(n) {
  return n.toFixed(3);
}

fs.mkdirSync(reportsDir, { recursive: true });

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));

const frameRows = [];
for (const row of metadataRows) {
  for (let i = 0; i < row.signs.length - 2; i += 1) {
    if (row.signs[i] !== '002') continue;
    const head = row.signs[i + 1];
    const x = row.signs[i + 2];
    const xPolarity = polarity(x);
    if (xPolarity === 'other') continue;
    const tail = row.signs.slice(i + 3);
    frameRows.push({
      checked_date: checkedDate,
      object: row.object,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      cult: row.cult,
      class: row.class,
      head,
      x,
      x_polarity: xPolarity,
      actual: tail.length === 0 ? 'terminal' : 'open',
      terminal: tail.length === 0,
      context_cell: `${row.site}|${row.type}|${row.shape}|${row.material}|${row.cult}|${row.class}`,
      text: row.text,
    });
  }
}

const scoredRows = frameRows.map((row) => {
  const trainOtherSiteSameHead = frameRows.filter((other) => other.site !== row.site && other.head === row.head);
  const trainOtherSiteSameX = frameRows.filter((other) => other.site !== row.site && other.x === row.x);
  const trainOtherSiteSameContext = frameRows.filter(
    (other) => other.site !== row.site && other.type === row.type && other.shape === row.shape && other.material === row.material,
  );
  const headVote = majority(trainOtherSiteSameHead);
  const xVote = majority(trainOtherSiteSameX);
  const contextVote = majority(trainOtherSiteSameContext);
  return {
    ...row,
    head_train_rows: trainOtherSiteSameHead.length,
    head_prediction: trainOtherSiteSameHead.length >= 2 ? headVote.prediction : 'insufficient',
    head_train_terminal_open: `${headVote.terminal}/${headVote.open}`,
    x_train_rows: trainOtherSiteSameX.length,
    x_prediction: trainOtherSiteSameX.length >= 2 ? xVote.prediction : 'insufficient',
    x_train_terminal_open: `${xVote.terminal}/${xVote.open}`,
    context_train_rows: trainOtherSiteSameContext.length,
    context_prediction: trainOtherSiteSameContext.length >= 2 ? contextVote.prediction : 'insufficient',
    context_train_terminal_open: `${contextVote.terminal}/${contextVote.open}`,
  };
});

const headAcc = accuracy(scoredRows, 'head_prediction');
const xAcc = accuracy(scoredRows, 'x_prediction');
const contextAcc = accuracy(scoredRows, 'context_prediction');

const focusRows = scoredRows.filter(
  (row) =>
    row.head === '390' ||
    row.head === '220' ||
    ['031', '861', '920', '405', '056'].includes(row.head) ||
    ['125', '095', '705', '455', '065'].includes(row.x),
);

const headSummaryRows = [...new Set(scoredRows.map((row) => row.head))]
  .map((head) => {
    const rows = scoredRows.filter((row) => row.head === head);
    const headPredicted = rows.filter((row) => row.head_prediction === 'terminal' || row.head_prediction === 'open');
    const headCorrect = headPredicted.filter((row) => row.actual === row.head_prediction);
    return {
      checked_date: checkedDate,
      head,
      rows: rows.length,
      actual_terminal_open: `${rows.filter((row) => row.terminal).length}/${rows.filter((row) => !row.terminal).length}`,
      predicted_rows: headPredicted.length,
      correct: headCorrect.length,
      accuracy: headPredicted.length ? pct(headCorrect.length / headPredicted.length) : '0.000',
      x_inventory: tally(rows.map((row) => row.x)),
      sites: tally(rows.map((row) => row.site)),
    };
  })
  .filter((row) => row.rows >= 3)
  .sort((a, b) => b.rows - a.rows || a.head.localeCompare(b.head));

function headSummaryText(head) {
  const row = headSummaryRows.find((candidate) => candidate.head === head);
  if (!row) return `no ${head} summary`;
  return `actual terminal/open=${row.actual_terminal_open}; head predicted ${row.correct}/${row.predicted_rows}=${row.accuracy}; X=${row.x_inventory}; sites=${row.sites}`;
}

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_LEAVE_SITE_HEAD_TRANSFER',
    tier: headAcc.accuracy >= contextAcc.accuracy ? 'candidate test pressure' : 'wild shot damaged',
    risky_bet: 'Head identity predicts terminal/open behavior across sites better than visual context does.',
    result: `head ${headAcc.correct}/${headAcc.predicted}=${pct(headAcc.accuracy)}; context ${contextAcc.correct}/${contextAcc.predicted}=${pct(contextAcc.accuracy)}; X ${xAcc.correct}/${xAcc.predicted}=${pct(xAcc.accuracy)}`,
    prediction: 'If grammar is real, head and X transfer should beat context when leaving a site out.',
    kill_condition: 'Context predictor beats or matches head/X once source-strict rows are used.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_220_CROSS_SITE_OPEN_HEAD',
    tier: 'wild shot with strong transfer pressure',
    risky_bet: '`220` remains an open-template head across Harappa/Kalibangan/Mohenjo-daro.',
    result: headSummaryText('220'),
    prediction: 'Leaving any one site out should still predict open for 220 if enough rows exist.',
    kill_condition: '220 openness is carried by one site or one source family only.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_390_SLOT_OVER_HEAD_TRANSFER',
    tier: 'wild shot damaged',
    risky_bet: '`390` is not predictive by itself; its apparent grammar depends on X-slot identity.',
    result: headSummaryText('390'),
    prediction: '`390-095/705` should close and `390-125/530` should open even when head-only transfer ties or fails.',
    kill_condition: '390 rows become predictable by context or head alone and X-slot identity stops carrying the open/terminal split.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'leave_site_head_transfer_test',
  frame_rows: frameRows.length,
  head_accuracy: `${headAcc.correct}/${headAcc.predicted}=${pct(headAcc.accuracy)}`,
  x_accuracy: `${xAcc.correct}/${xAcc.predicted}=${pct(xAcc.accuracy)}`,
  context_accuracy: `${contextAcc.correct}/${contextAcc.predicted}=${pct(contextAcc.accuracy)}`,
  decision_pressure:
    headAcc.accuracy > contextAcc.accuracy
      ? 'head_transfer_beats_context_in_this_proxy'
      : headAcc.accuracy < contextAcc.accuracy
        ? 'context_proxy_beats_head_transfer_in_this_proxy'
        : 'head_context_tie_in_this_proxy',
  new_bets: betRows.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

writeCsv(path.join(reportsDir, `${prefix}_scored_rows.csv`), scoredRows, [
  'checked_date',
  'object',
  'site',
  'type',
  'shape',
  'material',
  'cult',
  'class',
  'head',
  'x',
  'x_polarity',
  'actual',
  'head_train_rows',
  'head_prediction',
  'head_train_terminal_open',
  'x_train_rows',
  'x_prediction',
  'x_train_terminal_open',
  'context_train_rows',
  'context_prediction',
  'context_train_terminal_open',
  'context_cell',
  'text',
]);
writeCsv(path.join(reportsDir, `${prefix}_focus_rows.csv`), focusRows, [
  'checked_date',
  'object',
  'site',
  'head',
  'x',
  'x_polarity',
  'actual',
  'head_train_rows',
  'head_prediction',
  'x_train_rows',
  'x_prediction',
  'context_train_rows',
  'context_prediction',
  'text',
]);
writeCsv(path.join(reportsDir, `${prefix}_head_summary.csv`), headSummaryRows, [
  'checked_date',
  'head',
  'rows',
  'actual_terminal_open',
  'predicted_rows',
  'correct',
  'accuracy',
  'x_inventory',
  'sites',
]);
writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), betRows, [
  'checked_date',
  'bet_id',
  'tier',
  'risky_bet',
  'result',
  'prediction',
  'kill_condition',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
