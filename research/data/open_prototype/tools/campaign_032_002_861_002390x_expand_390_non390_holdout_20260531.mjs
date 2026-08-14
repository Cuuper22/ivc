import fs from 'node:fs';
import path from 'node:path';

// A holdout test that deliberately ignores 390. If the open-or-closed
// behavior of a 002-390-X frame can be predicted from how the same X behaves
// under every other head, then 390 contributes nothing of its own — it is a
// host environment, and the X subtype carries the behavior. The script reads
// lipi/metadata_filtered.csv, deduplicates by sign sequence, and collects all
// 002-HEAD-X frames. For each 390 row it takes the non-390 rows sharing the
// same X as training data, predicts open versus closed by majority vote, and
// scores the prediction against what the 390 row actually does (ties and
// uncovered X values are left blank rather than guessed). The claim
// "survives_first_holdout" only if every covered row passes and at least 6
// do. Writes the per-row holdout table and the decision as CSVs plus a
// summary JSON to data/open_prototype/reports.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_390_non390_holdout_20260531';
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

fs.mkdirSync(reportsDir, { recursive: true });

const rows = uniqueRowsByText(
  parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
    ...row,
    object: objectId(row),
    tokens: signs(row.text),
  })),
);

const xRows = [];
for (const row of rows) {
  for (let i = 0; i < row.tokens.length - 2; i += 1) {
    if (row.tokens[i] !== '002') continue;
    const tail = row.tokens.slice(i + 3);
    xRows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      head: row.tokens[i + 1],
      x: row.tokens[i + 2],
      observed_open: String(tail.length > 0),
      tail_after_x: tail.join(' ') || '<END>',
      text: row.text,
    });
  }
}

const targetRows = xRows.filter((row) => row.head === '390').map((row) => {
  const train = xRows.filter((other) => other.head !== '390' && other.x === row.x);
  const trainOpen = train.filter((other) => other.observed_open === 'true').length;
  const trainClosed = train.length - trainOpen;
  const predictedOpen =
    train.length === 0 ? 'uncovered' : trainOpen === trainClosed ? 'tie' : String(trainOpen > trainClosed);
  const pass = predictedOpen === 'uncovered' || predictedOpen === 'tie' ? '' : String(predictedOpen === row.observed_open);
  return {
    ...row,
    non390_train_rows: String(train.length),
    non390_train_open: ratio(trainOpen, train.length),
    non390_train_objects: train.map((other) => other.object).join(';'),
    predicted_open_from_non390_same_x: predictedOpen,
    prediction_pass: pass,
  };
});

const coveredRows = targetRows.filter((row) => row.prediction_pass !== '');
const passRows = coveredRows.filter((row) => row.prediction_pass === 'true');
const decisions = [
  {
    checked_date: checkedDate,
    candidate: 'EXPAND_390_RIGHT_EDGE_HOST_BY_X_SUBTYPE',
    decision: passRows.length >= 6 && passRows.length === coveredRows.length ? 'survives_first_holdout' : 'stays_wild_or_damaged',
    evidence:
      `non390 same-X covered=${ratio(coveredRows.length, targetRows.length)}; pass=${ratio(passRows.length, coveredRows.length)}; ` +
      `uncovered_or_tie=${targetRows.filter((row) => row.prediction_pass === '').map((row) => `${row.object}:${row.x}:${row.predicted_open_from_non390_same_x}`).join(';')}.`,
    consequence:
      'If this holds, `390` is more likely a host environment whose continuation behavior is inherited from X subtype rather than from a `390` value.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: '390_non390_holdout',
  rows: {
    target_390_rows: targetRows.length,
    covered_by_non390_same_x: coveredRows.length,
    holdout_pass: passRows.length,
    x_distribution: countBy(targetRows, (row) => row.x),
  },
  decisions,
};

writeCsv(path.join(reportsDir, `${prefix}_target_rows.csv`), targetRows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'shape',
  'material',
  'head',
  'x',
  'observed_open',
  'tail_after_x',
  'non390_train_rows',
  'non390_train_open',
  'non390_train_objects',
  'predicted_open_from_non390_same_x',
  'prediction_pass',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  'checked_date',
  'candidate',
  'decision',
  'evidence',
  'consequence',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
