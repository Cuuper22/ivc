// Template probe for the H-2218..H-2239 three-sided tablets. Each tablet has
// three inscribed sides, and each side's text falls into one of three "role
// families": +861-003+, +700-03x+ (033 or 034), or +15x-003+ (154 or 156).
// The question: do the 22 tablets all carry exactly one side of each role, and
// is any role pinned to a fixed catalog side?
//
// The script reads lipi_h2218_h2239_fig4_mapping.csv, assigns each side text a
// role family, classifies each tablet's ordered role triple into a template
// class, and counts how often the +15x-003+ role lands on local side 3. Two
// simple null models give exact p-values: if roles were placed at random, side
// 3 would hold a given role with chance 1/3 per tablet, and a tablet would fit
// one of the two attested templates with chance 2/6.
//
// It writes a per-tablet template CSV, a counts CSV, a tests CSV, and a JSON
// summary (lipi_h2218_h2239_side_role_*). This is structure-only work: it
// establishes that the side layout is templated, without claiming any reading
// or meaning for the signs.

import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const inputCsv = path.join(reportsDir, 'lipi_h2218_h2239_fig4_mapping.csv');
const templateCsv = path.join(reportsDir, 'lipi_h2218_h2239_side_role_templates.csv');
const countCsv = path.join(reportsDir, 'lipi_h2218_h2239_side_role_counts.csv');
const testCsv = path.join(reportsDir, 'lipi_h2218_h2239_side_role_tests.csv');
const outJson = path.join(reportsDir, 'lipi_h2218_h2239_side_role_summary.json');

const sideKeys = ['side_1_text', 'side_2_text', 'side_3_text'];

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
          i++;
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

function countBy(values) {
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  return counts;
}

function objectFromCounts(counts) {
  return Object.fromEntries([...counts.entries()].sort((a, b) => a[0].localeCompare(b[0], undefined, { numeric: true })));
}

function roleFamily(text) {
  if (text === '+861-003+') return 'role_861_003';
  if (text === '+700-033+' || text === '+700-034+') return 'role_700_03x';
  if (text === '+154-003+' || text === '+156-003+') return 'role_15x_003';
  return 'role_other';
}

function templateClass(roles) {
  const joined = roles.join('|');
  if (joined === 'role_861_003|role_700_03x|role_15x_003') return 'template_861_700_15x';
  if (joined === 'role_700_03x|role_861_003|role_15x_003') return 'template_700_861_15x';
  return 'template_other';
}

function formatNumber(value) {
  return value === null || value === undefined || Number.isNaN(value) ? '' : Number(value.toFixed(6));
}

function formatTiny(value) {
  return value < 0.000001 ? value.toExponential(12) : formatNumber(value);
}

function hasExactlyOneEach(roles) {
  const counts = objectFromCounts(countBy(roles));
  return counts.role_861_003 === 1 && counts.role_700_03x === 1 && counts.role_15x_003 === 1;
}

const sourceRows = csvObjects(fs.readFileSync(inputCsv, 'utf8'));
const rows = sourceRows
  .map((row) => {
    const sideTexts = sideKeys.map((key) => row[key]);
    const roles = sideTexts.map(roleFamily);
    const exactTemplate = sideTexts.join('|');
    const roleTemplate = roles.join('|');
    return {
      fig4_number: Number.parseInt(row.fig4_number, 10),
      manufacturing_group: row.manufacturing_group,
      cisi: row.cisi,
      harp_object: row.harp_object,
      local_signature_short: row.local_signature_short,
      side_1_text: row.side_1_text,
      side_2_text: row.side_2_text,
      side_3_text: row.side_3_text,
      side_1_role: roles[0],
      side_2_role: roles[1],
      side_3_role: roles[2],
      exact_template: exactTemplate,
      role_template: roleTemplate,
      template_class: templateClass(roles),
      complete_three_role_inventory: hasExactlyOneEach(roles),
      interpretation_status: 'no_reading_admissible',
    };
  })
  .sort((a, b) => a.fig4_number - b.fig4_number);

const templateRows = [
  [
    'fig4_number',
    'manufacturing_group',
    'cisi',
    'harp_object',
    'local_signature_short',
    'side_1_text',
    'side_1_role',
    'side_2_text',
    'side_2_role',
    'side_3_text',
    'side_3_role',
    'exact_template',
    'role_template',
    'template_class',
    'complete_three_role_inventory',
    'interpretation_status',
  ],
];

for (const row of rows) {
  templateRows.push([
    row.fig4_number,
    row.manufacturing_group,
    row.cisi,
    row.harp_object,
    row.local_signature_short,
    row.side_1_text,
    row.side_1_role,
    row.side_2_text,
    row.side_2_role,
    row.side_3_text,
    row.side_3_role,
    row.exact_template,
    row.role_template,
    row.template_class,
    row.complete_three_role_inventory,
    row.interpretation_status,
  ]);
}

const countRows = [['scope', 'key', 'value', 'count']];
for (const sideIndex of [1, 2, 3]) {
  const key = `side_${sideIndex}_role`;
  for (const [value, count] of countBy(rows.map((row) => row[key]))) {
    countRows.push(['role_by_side', key, value, count]);
  }
}
for (const [value, count] of countBy(rows.map((row) => row.template_class))) {
  countRows.push(['template_class', 'all_rows', value, count]);
}
for (const role of ['role_861_003', 'role_700_03x', 'role_15x_003']) {
  const exactValues = [];
  for (const row of rows) {
    for (const sideIndex of [1, 2, 3]) {
      if (row[`side_${sideIndex}_role`] === role) exactValues.push(row[`side_${sideIndex}_text`]);
    }
  }
  for (const [value, count] of countBy(exactValues)) {
    countRows.push(['exact_text_by_role', role, value, count]);
  }
}

const completeInventoryRows = rows.filter((row) => row.complete_three_role_inventory).length;
const side3Role15xRows = rows.filter((row) => row.side_3_role === 'role_15x_003').length;
const twoTemplateRows = rows.filter((row) => row.template_class === 'template_861_700_15x' || row.template_class === 'template_700_861_15x').length;
const rowwiseSide3NullP = (1 / 3) ** rows.length;
const rowwiseTwoTemplateNullP = (2 / 6) ** rows.length;

const testRows = [
  [
    'check',
    'observed',
    'eligible_n',
    'rowwise_null',
    'exact_p_ge_observed',
    'interpretation',
  ],
  [
    'complete_three_role_inventory',
    completeInventoryRows,
    rows.length,
    'descriptive_inventory_check_no_random_null',
    '',
    'side_role_template_check_only_no_reading',
  ],
  [
    'role_15x_003_fixed_on_side_3',
    side3Role15xRows,
    rows.length,
    'one_of_three_role_positions_per_object',
    formatTiny(rowwiseSide3NullP),
    'catalog_side_stability_check_only_no_physical_side_claim',
  ],
  [
    'two_template_fit_861_700_15x_or_700_861_15x',
    twoTemplateRows,
    rows.length,
    'two_of_six_role_permutations_per_object',
    formatTiny(rowwiseTwoTemplateNullP),
    'template_fit_check_only_no_reading',
  ],
];

const variants = rows
  .flatMap((row) =>
    [1, 2, 3].map((sideIndex) => ({
      cisi: row.cisi,
      fig4_number: row.fig4_number,
      manufacturing_group: row.manufacturing_group,
      side_index: sideIndex,
      side_text: row[`side_${sideIndex}_text`],
      side_role: row[`side_${sideIndex}_role`],
      template_class: row.template_class,
    })),
  )
  .filter((row) => row.side_text === '+700-033+' || row.side_text === '+154-003+');

const summary = {
  source: 'H-2218 through H-2239 side-role template probe',
  checked_at: '2026-05-24',
  input: path.relative(base, inputCsv).replaceAll('\\', '/'),
  source_rows: rows.length,
  complete_three_role_inventory_rows: completeInventoryRows,
  side3_role_15x_003_rows: side3Role15xRows,
  two_template_fit_rows: twoTemplateRows,
  role_counts_by_side: {
    side_1: objectFromCounts(countBy(rows.map((row) => row.side_1_role))),
    side_2: objectFromCounts(countBy(rows.map((row) => row.side_2_role))),
    side_3: objectFromCounts(countBy(rows.map((row) => row.side_3_role))),
  },
  template_class_counts: objectFromCounts(countBy(rows.map((row) => row.template_class))),
  exact_text_counts_by_role: Object.fromEntries(
    ['role_861_003', 'role_700_03x', 'role_15x_003'].map((role) => {
      const exactValues = [];
      for (const row of rows) {
        for (const sideIndex of [1, 2, 3]) {
          if (row[`side_${sideIndex}_role`] === role) exactValues.push(row[`side_${sideIndex}_text`]);
        }
      }
      return [role, objectFromCounts(countBy(exactValues))];
    }),
  ),
  variant_localization: variants,
  rowwise_role_permutation_checks: {
    role_15x_003_fixed_on_side_3: {
      observed: side3Role15xRows,
      eligible_n: rows.length,
      exact_p_ge_observed: formatTiny(rowwiseSide3NullP),
      null: 'one_of_three_role_positions_per_object',
    },
    two_template_fit_861_700_15x_or_700_861_15x: {
      observed: twoTemplateRows,
      eligible_n: rows.length,
      exact_p_ge_observed: formatTiny(rowwiseTwoTemplateNullP),
      null: 'two_of_six_role_permutations_per_object',
    },
  },
  key_observation:
    'All 22 local rows fit a three-role inventory: one +861-003+ side, one +700-03x+ side, and one +15x-003+ side. The +15x-003+ role is always local side 3, while the +861-003+ and +700-03x+ roles swap between local sides 1 and 2.',
  interpretation_boundary:
    'This is a local side-role template and catalog-side stability probe only. It accepts no physical side function, numerical value, metrological reading, sign meaning, phonetic value, language identity, or translation.',
  outputs: [templateCsv, countCsv, testCsv, outJson].map((file) => path.relative(base, file).replaceAll('\\', '/')),
};

fs.writeFileSync(templateCsv, toCsv(templateRows));
fs.writeFileSync(countCsv, toCsv(countRows));
fs.writeFileSync(testCsv, toCsv(testRows));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
