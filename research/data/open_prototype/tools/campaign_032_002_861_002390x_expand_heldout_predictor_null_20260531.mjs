import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_expand_heldout_predictor_null_20260531';

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
  return text.match(/\d{3}/g) ?? [];
}

function ratio(numerator, denominator) {
  return denominator ? `${numerator}/${denominator}` : '0/0';
}

function pct(numerator, denominator) {
  return denominator ? (numerator / denominator).toFixed(6) : '';
}

function majorityPredict(rows) {
  const open = rows.filter((row) => row.open).length;
  return open >= rows.length - open;
}

fs.mkdirSync(reportsDir, { recursive: true });

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));
const frames = [];
for (const row of metadataRows) {
  const rowSigns = signs(row.text);
  for (let index = 0; index < rowSigns.length - 2; index += 1) {
    if (rowSigns[index] !== '002' || !rowSigns[index + 1] || !rowSigns[index + 2]) continue;
    frames.push({
      checked_date: '2026-05-31',
      object: row.cisi,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      scope_cell: `${row.site}|${row.type}|${row.shape}|${row.material}`,
      prev_before_002: rowSigns[index - 1] ?? '',
      head_after_002: rowSigns[index + 1],
      x: rowSigns[index + 2],
      head_x_pair: `${rowSigns[index + 1]}-${rowSigns[index + 2]}`,
      scope_x: `${row.site}|${row.type}|${row.shape}|${row.material}|${rowSigns[index + 2]}`,
      scope_head: `${row.site}|${row.type}|${row.shape}|${row.material}|${rowSigns[index + 1]}`,
      tail_after_x: rowSigns.slice(index + 3).join(' ') || '<END>',
      open: index + 2 < rowSigns.length - 1,
      actual: index + 2 < rowSigns.length - 1 ? 'open' : 'terminal',
      text: row.text,
    });
  }
}

const predictors = [
  ['x_slot_sign', (row) => row.x],
  ['head_after_002', (row) => row.head_after_002],
  ['head_x_pair', (row) => row.head_x_pair],
  ['prev_before_002', (row) => row.prev_before_002],
  ['scope_cell', (row) => row.scope_cell],
  ['scope_x', (row) => row.scope_x],
  ['scope_head', (row) => row.scope_head],
];

const predictionRows = [];
const metricRows = [];

for (const [name, keyFn] of predictors) {
  let covered = 0;
  let correct = 0;
  for (let index = 0; index < frames.length; index += 1) {
    const test = frames[index];
    const key = keyFn(test);
    const train = frames.filter((row, rowIndex) => rowIndex !== index && keyFn(row) === key);
    if (!train.length) continue;
    const predOpen = majorityPredict(train);
    const isCorrect = predOpen === test.open;
    covered += 1;
    if (isCorrect) correct += 1;
    predictionRows.push({
      checked_date: '2026-05-31',
      predictor: name,
      key,
      object: test.object,
      head_after_002: test.head_after_002,
      x: test.x,
      head_x_pair: test.head_x_pair,
      scope_cell: test.scope_cell,
      prev_before_002: test.prev_before_002,
      training_rows: String(train.length),
      training_open_rate: ratio(train.filter((row) => row.open).length, train.length),
      predicted: predOpen ? 'open' : 'terminal',
      actual: test.actual,
      correct: isCorrect ? 'True' : 'False',
      text: test.text,
    });
  }
  metricRows.push({
    checked_date: '2026-05-31',
    predictor: name,
    covered: String(covered),
    total: String(frames.length),
    coverage_rate: pct(covered, frames.length),
    correct: String(correct),
    wrong: String(covered - correct),
    accuracy: pct(correct, covered),
  });
}

const metricByName = Object.fromEntries(metricRows.map((row) => [row.predictor, row]));
const bets = [
  {
    checked_date: '2026-05-31',
    bet_id: 'X_SIGN_PREDICTOR_BEATS_SCOPE_AND_LEFT_NULLS',
    tier: 'candidate',
    claim:
      'X-slot sign alone predicts held-out open/terminal behavior better than left context, head alone, or broad visual scope.',
    support:
      `x=${metricByName.x_slot_sign.accuracy} (${metricByName.x_slot_sign.correct}/${metricByName.x_slot_sign.covered}); ` +
      `scope=${metricByName.scope_cell.accuracy}; left=${metricByName.prev_before_002.accuracy}; head=${metricByName.head_after_002.accuracy}`,
    prediction:
      'After adding source-bound rows, X-sign prediction should stay above broad scope and left-context baselines if the grammar model is real.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'HEAD_X_PAIR_MICROGRAMMAR',
    tier: 'candidate',
    claim:
      'Repeated H-X pairs behave like microgrammar rules: when a pair repeats, it predicts held-out continuation very strongly.',
    support: `head_x_pair=${metricByName.head_x_pair.accuracy} (${metricByName.head_x_pair.correct}/${metricByName.head_x_pair.covered})`,
    prediction:
      'Family collapse should not erase most repeated pair behavior; if it does, demote microgrammar to copied formula family.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'VISUAL_SCOPE_NULL_STILL_LIVE',
    tier: 'candidate',
    claim:
      'The copied-register adversary is not dead: scope+X and scope+head are competitive, though lower coverage than X-sign.',
    support: `scope_x=${metricByName.scope_x.accuracy} (${metricByName.scope_x.covered} covered); scope_head=${metricByName.scope_head.accuracy} (${metricByName.scope_head.covered} covered)`,
    prediction:
      'If scope-conditioned predictors dominate after family/source collapse, grammar bets must be demoted to register templates.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'LEFT_CONTEXT_ROUTER_WEAKENS',
    tier: 'candidate',
    claim:
      'Immediate left context before `002` is weaker than X-sign for predicting open/terminal behavior.',
    support: `left=${metricByName.prev_before_002.accuracy}; x=${metricByName.x_slot_sign.accuracy}`,
    prediction:
      'If future rows sharing left signs split by X again, do not promote a left-context-only parser.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'EXPAND',
  status: 'heldout_predictor_null',
  frame_count: frames.length,
  metrics: metricRows,
  new_bets: Object.fromEntries(bets.map((row) => [row.bet_id, row.tier])),
  predictions: [
    'X-sign and H-X pair predictors should keep beating broad scope and left-context baselines.',
    'Scope-conditioned predictors staying competitive means copied visual-register null remains alive.',
    'If head-X pair accuracy collapses under family/source checks, kill microgrammar and treat repeated pairs as formula copies.',
  ],
};

writeCsv(path.join(reportsDir, `${prefix}_metrics.csv`), metricRows, [
  'checked_date',
  'predictor',
  'covered',
  'total',
  'coverage_rate',
  'correct',
  'wrong',
  'accuracy',
]);

writeCsv(path.join(reportsDir, `${prefix}_predictions.csv`), predictionRows, [
  'checked_date',
  'predictor',
  'key',
  'object',
  'head_after_002',
  'x',
  'head_x_pair',
  'scope_cell',
  'prev_before_002',
  'training_rows',
  'training_open_rate',
  'predicted',
  'actual',
  'correct',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), bets, [
  'checked_date',
  'bet_id',
  'tier',
  'claim',
  'support',
  'prediction',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
