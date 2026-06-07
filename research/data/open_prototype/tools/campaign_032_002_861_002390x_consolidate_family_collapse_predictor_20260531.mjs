import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_consolidate_family_collapse_predictor_20260531';

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

function collapseRows(rows, keyFn) {
  const seen = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    if (!seen.has(key)) seen.set(key, row);
  }
  return [...seen.values()];
}

function evaluate(setName, rows, predictorName, keyFn) {
  let covered = 0;
  let correct = 0;
  for (let index = 0; index < rows.length; index += 1) {
    const test = rows[index];
    const key = keyFn(test);
    const train = rows.filter((row, rowIndex) => rowIndex !== index && keyFn(row) === key);
    if (!train.length) continue;
    const predictedOpen = majorityPredict(train);
    covered += 1;
    if (predictedOpen === test.open) correct += 1;
  }
  return {
    checked_date: '2026-05-31',
    set_name: setName,
    predictor: predictorName,
    rows: String(rows.length),
    covered: String(covered),
    coverage_rate: pct(covered, rows.length),
    correct: String(correct),
    wrong: String(covered - correct),
    accuracy: pct(correct, covered),
  };
}

fs.mkdirSync(reportsDir, { recursive: true });

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));
const frames = [];
for (const row of metadataRows) {
  const rowSigns = signs(row.text);
  for (let index = 0; index < rowSigns.length - 2; index += 1) {
    if (rowSigns[index] !== '002') continue;
    const head = rowSigns[index + 1];
    const x = rowSigns[index + 2];
    frames.push({
      checked_date: '2026-05-31',
      object: row.cisi,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      scope_cell: `${row.site}|${row.type}|${row.shape}|${row.material}`,
      prev_before_002: rowSigns[index - 1] ?? '',
      head,
      x,
      head_x_pair: `${head}-${x}`,
      tail_after_x: rowSigns.slice(index + 3).join(' ') || '<END>',
      open: index + 2 < rowSigns.length - 1,
      text: row.text,
    });
  }
}

const sets = [
  ['raw', frames],
  ['collapse_scope_pair_tail', collapseRows(frames, (row) => `${row.scope_cell}|${row.head_x_pair}|${row.tail_after_x}`)],
  ['collapse_scope_pair', collapseRows(frames, (row) => `${row.scope_cell}|${row.head_x_pair}`)],
  ['collapse_pair_tail', collapseRows(frames, (row) => `${row.head_x_pair}|${row.tail_after_x}`)],
  ['collapse_pair', collapseRows(frames, (row) => row.head_x_pair)],
];

const predictors = [
  ['head_x_pair', (row) => row.head_x_pair],
  ['x_slot_sign', (row) => row.x],
  ['scope_cell', (row) => row.scope_cell],
  ['scope_x', (row) => `${row.scope_cell}|${row.x}`],
];

const metricRows = [];
for (const [setName, rows] of sets) {
  for (const [predictorName, keyFn] of predictors) {
    metricRows.push(evaluate(setName, rows, predictorName, keyFn));
  }
}

function metric(setName, predictor) {
  return metricRows.find((row) => row.set_name === setName && row.predictor === predictor);
}

const decisions = [
  {
    checked_date: '2026-05-31',
    candidate: 'HEAD_X_PAIR_MICROGRAMMAR',
    decision: 'narrow_to_scope_local_candidate',
    reason:
      `raw pair accuracy ${metric('raw', 'head_x_pair').accuracy}; ` +
      `scope-pair-tail collapse ${metric('collapse_scope_pair_tail', 'head_x_pair').accuracy}; ` +
      `global pair-tail collapse ${metric('collapse_pair_tail', 'head_x_pair').accuracy}`,
    next_test:
      'Treat repeated H-X pairs as parser candidates only after checking whether they survive collapse outside exact scope/tail families.',
  },
  {
    checked_date: '2026-05-31',
    candidate: 'X_SIGN_PREDICTOR_BEATS_SCOPE_AND_LEFT_NULLS',
    decision: 'keep_but_require_scope_correction',
    reason:
      `raw X accuracy ${metric('raw', 'x_slot_sign').accuracy}; ` +
      `scope-pair-tail collapse X ${metric('collapse_scope_pair_tail', 'x_slot_sign').accuracy}; ` +
      `pair-tail collapse X ${metric('collapse_pair_tail', 'x_slot_sign').accuracy}`,
    next_test:
      'Do not use X alone as a parser; use X plus head/scope correction until source/family collapse improves it.',
  },
  {
    checked_date: '2026-05-31',
    candidate: 'VISUAL_SCOPE_NULL_STILL_LIVE',
    decision: 'strengthen_adversary',
    reason:
      `scope+X raw ${metric('raw', 'scope_x').accuracy}; pair-tail collapse scope+X ${metric('collapse_pair_tail', 'scope_x').accuracy}; scope predictors remain competitive under strict collapse`,
    next_test:
      'Every high-confidence parse must report whether scope-conditioned predictors explain the same row.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'CONSOLIDATE',
  status: 'family_collapse_predictor',
  metrics: metricRows,
  decisions,
  compressed_model_change: [
    'H-X pair accuracy is real but scope/tail-family sensitive.',
    'X-sign prediction survives as a candidate only with scope correction.',
    'Visual-register null gets stronger, not weaker, under consolidation.',
  ],
};

writeCsv(path.join(reportsDir, `${prefix}_metrics.csv`), metricRows, [
  'checked_date',
  'set_name',
  'predictor',
  'rows',
  'covered',
  'coverage_rate',
  'correct',
  'wrong',
  'accuracy',
]);

writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  'checked_date',
  'candidate',
  'decision',
  'reason',
  'next_test',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
