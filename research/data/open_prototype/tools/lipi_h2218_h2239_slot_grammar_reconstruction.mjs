import fs from 'node:fs';
import path from 'node:path';

// If the H-2218..H-2239 tablets really follow a three-slot template -- each object carrying
// one 861-003 side, one 700-03x side, and one 15x-003 side -- then hiding any one side of
// any tablet should let us reconstruct it from the other two. This script runs that test.
// It reads the side-role template CSV and, for every object and every hidden side, predicts
// the missing side two ways: the role is whichever of the three roles the visible sides do
// not cover, and the exact text is the majority text for that role in a leave-one-out
// training set (the object itself excluded). Two baselines -- majority text per side index
// and one global majority -- give comparison floors. It writes every prediction, a failures
// CSV, and a JSON summary with accuracies. The expected shape of the result: role
// prediction succeeds everywhere, and the only exact-text failures are the two singleton
// variants (H-2237's 154 and H-2238's 033), which stay flagged as source-validation
// targets. Catalog-side structure only; no side function or reading is accepted.

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const inputCsv = path.join(reportsDir, 'lipi_h2218_h2239_side_role_templates.csv');
const predictionCsv = path.join(reportsDir, 'lipi_h2218_h2239_slot_grammar_predictions.csv');
const failureCsv = path.join(reportsDir, 'lipi_h2218_h2239_slot_grammar_failures.csv');
const summaryJson = path.join(reportsDir, 'lipi_h2218_h2239_slot_grammar_summary.json');

const roles = ['role_861_003', 'role_700_03x', 'role_15x_003'];
const sides = [1, 2, 3];

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQuotes) {
      if (c === '"') {
        if (text[i + 1] === '"') {
          field += '"';
          i += 1;
        } else {
          inQuotes = false;
        }
      } else {
        field += c;
      }
    } else if (c === '"') {
      inQuotes = true;
    } else if (c === ',') {
      row.push(field);
      field = '';
    } else if (c === '\n') {
      row.push(field);
      field = '';
      if (row.length > 1 || row[0] !== '') rows.push(row);
      row = [];
    } else if (c !== '\r') {
      field += c;
    }
  }
  if (field.length || row.length) {
    row.push(field);
    rows.push(row);
  }
  return rows;
}

function csvObjects(text) {
  const rows = parseCsv(text);
  const header = rows.shift() ?? [];
  return rows.map((row) => Object.fromEntries(header.map((name, index) => [name, row[index] ?? ''])));
}

function toCsv(rows) {
  return `${rows
    .map((row) =>
      row
        .map((value) => {
          const text = String(value ?? '');
          return `"${text.replaceAll('"', '""')}"`;
        })
        .join(','),
    )
    .join('\n')}\n`;
}

function mode(values) {
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], undefined, { numeric: true }))[0]?.[0] ?? '';
}

function groupCounts(rows, key) {
  const counts = {};
  for (const row of rows) counts[row[key]] = (counts[row[key]] ?? 0) + 1;
  return Object.fromEntries(Object.entries(counts).sort((a, b) => a[0].localeCompare(b[0], undefined, { numeric: true })));
}

function roleTextRows(rows, role) {
  const values = [];
  for (const row of rows) {
    for (const side of sides) {
      if (row[`side_${side}_role`] === role) values.push(row[`side_${side}_text`]);
    }
  }
  return values;
}

function exactTextModeForRole(trainingRows, role) {
  return mode(roleTextRows(trainingRows, role));
}

function missingRole(observedRoles) {
  const remaining = roles.filter((role) => !observedRoles.includes(role));
  return remaining.length === 1 ? remaining[0] : 'ambiguous_or_not_three_role_inventory';
}

function majorityBySide(rows, side) {
  return mode(rows.map((row) => row[`side_${side}_text`]));
}

function globalMajority(rows) {
  return mode(rows.flatMap((row) => sides.map((side) => row[`side_${side}_text`])));
}

const rows = csvObjects(fs.readFileSync(inputCsv, 'utf8')).sort((a, b) => Number(a.fig4_number) - Number(b.fig4_number));
const globalBaselineText = globalMajority(rows);
const sideBaselines = Object.fromEntries(sides.map((side) => [side, majorityBySide(rows, side)]));

const predictions = [];

for (const row of rows) {
  const trainingRows = rows.filter((candidate) => candidate.cisi !== row.cisi);
  for (const hiddenSide of sides) {
    const observedSides = sides.filter((side) => side !== hiddenSide);
    const observedRoles = observedSides.map((side) => row[`side_${side}_role`]);
    const predictedRole = missingRole(observedRoles);
    const predictedText = exactTextModeForRole(trainingRows, predictedRole);
    const actualRole = row[`side_${hiddenSide}_role`];
    const actualText = row[`side_${hiddenSide}_text`];
    const sideBaselineText = sideBaselines[hiddenSide];
    predictions.push({
      checked_date: '2026-05-25',
      cisi: row.cisi,
      fig4_number: row.fig4_number,
      manufacturing_group: row.manufacturing_group,
      template_class: row.template_class,
      local_signature_short: row.local_signature_short,
      hidden_side: hiddenSide,
      observed_side_roles: observedRoles.join(';'),
      actual_role: actualRole,
      predicted_role: predictedRole,
      role_prediction_correct: String(predictedRole === actualRole),
      actual_text: actualText,
      predicted_text_role_majority_loo: predictedText,
      exact_text_prediction_correct: String(predictedText === actualText),
      side_index_majority_text: sideBaselineText,
      side_index_majority_correct: String(sideBaselineText === actualText),
      global_majority_text: globalBaselineText,
      global_majority_correct: String(globalBaselineText === actualText),
      failure_type:
        predictedRole !== actualRole
          ? 'role_failure'
          : predictedText !== actualText
            ? 'singleton_exact_text_failure'
            : 'none',
      accepted_decipherment_claim: '0',
    });
  }
}

const predictionHeader = [
  'checked_date',
  'cisi',
  'fig4_number',
  'manufacturing_group',
  'template_class',
  'local_signature_short',
  'hidden_side',
  'observed_side_roles',
  'actual_role',
  'predicted_role',
  'role_prediction_correct',
  'actual_text',
  'predicted_text_role_majority_loo',
  'exact_text_prediction_correct',
  'side_index_majority_text',
  'side_index_majority_correct',
  'global_majority_text',
  'global_majority_correct',
  'failure_type',
  'accepted_decipherment_claim',
];

const predictionRows = [
  predictionHeader,
  ...predictions.map((row) => predictionHeader.map((key) => row[key])),
];

const failures = predictions.filter((row) => row.failure_type !== 'none');
const failureHeader = [
  'checked_date',
  'cisi',
  'fig4_number',
  'manufacturing_group',
  'template_class',
  'hidden_side',
  'actual_role',
  'actual_text',
  'predicted_text_role_majority_loo',
  'failure_type',
  'research_consequence',
  'accepted_decipherment_claim',
];
const failureRows = [
  failureHeader,
  ...failures.map((row) => [
    row.checked_date,
    row.cisi,
    row.fig4_number,
    row.manufacturing_group,
    row.template_class,
    row.hidden_side,
    row.actual_role,
    row.actual_text,
    row.predicted_text_role_majority_loo,
    row.failure_type,
    row.failure_type === 'singleton_exact_text_failure'
      ? 'exactly the two singleton minimal-contrast variants remain as source-validation targets'
      : 'role inventory failed and the three-role grammar would need downgrade',
    row.accepted_decipherment_claim,
  ]),
];

function countCorrect(key) {
  return predictions.filter((row) => row[key] === 'true').length;
}

const roleCorrect = countCorrect('role_prediction_correct');
const exactCorrect = countCorrect('exact_text_prediction_correct');
const sideBaselineCorrect = countCorrect('side_index_majority_correct');
const globalBaselineCorrect = countCorrect('global_majority_correct');

const summary = {
  checked_date: '2026-05-25',
  artifact: 'lipi_h2218_h2239_slot_grammar_reconstruction',
  input: path.relative(base, inputCsv).replaceAll('\\', '/'),
  object_rows: rows.length,
  hidden_side_prediction_rows: predictions.length,
  role_inventory: roles,
  role_prediction_correct: roleCorrect,
  role_prediction_accuracy: roleCorrect / predictions.length,
  exact_text_prediction_correct: exactCorrect,
  exact_text_prediction_accuracy: exactCorrect / predictions.length,
  side_index_majority_correct: sideBaselineCorrect,
  side_index_majority_accuracy: sideBaselineCorrect / predictions.length,
  global_majority_correct: globalBaselineCorrect,
  global_majority_accuracy: globalBaselineCorrect / predictions.length,
  failure_counts: groupCounts(predictions, 'failure_type'),
  exact_text_failures: failures.map((row) => ({
    cisi: row.cisi,
    fig4_number: Number(row.fig4_number),
    hidden_side: Number(row.hidden_side),
    actual_role: row.actual_role,
    actual_text: row.actual_text,
    predicted_text: row.predicted_text_role_majority_loo,
    failure_type: row.failure_type,
  })),
  interpretation_boundary:
    'This is a catalog-side slot grammar reconstruction only. It shows object-internal role predictability and isolates singleton variants; it accepts no physical side role, sign value, function, language, or translation without source images.',
  accepted_decipherment_claims: 0,
  outputs: [
    path.relative(base, predictionCsv).replaceAll('\\', '/'),
    path.relative(base, failureCsv).replaceAll('\\', '/'),
    path.relative(base, summaryJson).replaceAll('\\', '/'),
  ],
};

fs.writeFileSync(predictionCsv, toCsv(predictionRows));
fs.writeFileSync(failureCsv, toCsv(failureRows));
fs.writeFileSync(summaryJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
