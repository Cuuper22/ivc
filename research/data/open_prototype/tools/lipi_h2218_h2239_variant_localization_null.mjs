import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const mappingPath = path.join(reportsDir, 'lipi_h2218_h2239_fig4_mapping.csv');
const templatePath = path.join(reportsDir, 'lipi_h2218_h2239_side_role_templates.csv');
const minimalPath = path.join(reportsDir, 'lipi_h2218_h2239_minimal_contrast_packet.csv');

const objectOut = path.join(reportsDir, 'lipi_h2218_h2239_variant_localization_objects.csv');
const testOut = path.join(reportsDir, 'lipi_h2218_h2239_variant_localization_tests.csv');
const summaryOut = path.join(reportsDir, 'lipi_h2218_h2239_variant_localization_summary.json');

function parseCsv(text) {
  const rows = [];
  let row = [];
  let value = '';
  let inQuotes = false;

  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (inQuotes) {
      if (ch === '"' && next === '"') {
        value += '"';
        i += 1;
      } else if (ch === '"') {
        inQuotes = false;
      } else {
        value += ch;
      }
    } else if (ch === '"') {
      inQuotes = true;
    } else if (ch === ',') {
      row.push(value);
      value = '';
    } else if (ch === '\n') {
      row.push(value);
      rows.push(row);
      row = [];
      value = '';
    } else if (ch !== '\r') {
      value += ch;
    }
  }
  if (value.length > 0 || row.length > 0) {
    row.push(value);
    rows.push(row);
  }

  const [header, ...body] = rows.filter((entry) => entry.length > 1 || entry[0] !== '');
  return body.map((entry) =>
    Object.fromEntries(header.map((key, index) => [key, entry[index] ?? ''])),
  );
}

function readCsv(filePath) {
  return parseCsv(fs.readFileSync(filePath, 'utf8'));
}

function toCsv(rows) {
  if (rows.length === 0) return '';
  const header = Object.keys(rows[0]);
  const body = rows.map((row) =>
    header
      .map((key) => `"${String(row[key] ?? '').replaceAll('"', '""')}"`)
      .join(','),
  );
  return `${[header.map((key) => `"${key}"`).join(','), ...body].join('\n')}\n`;
}

function choose2(n) {
  return n < 2 ? 0 : (n * (n - 1)) / 2;
}

function asNumber(value) {
  const n = Number(value);
  return Number.isFinite(n) ? n : 0;
}

function pString(numerator, denominator) {
  return denominator === 0 ? '0.000000' : (numerator / denominator).toFixed(6);
}

const mappingRows = readCsv(mappingPath);
const templateRows = readCsv(templatePath);
const minimalRows = readCsv(minimalPath);

const templateByCisi = new Map(templateRows.map((row) => [row.cisi, row]));
const oneSlotControlCounts = new Map();
const exactDimensionControlCounts = new Map();
for (const row of minimalRows) {
  if (row.differing_side_count === '1') {
    oneSlotControlCounts.set(
      row.target_object,
      (oneSlotControlCounts.get(row.target_object) ?? 0) + 1,
    );
  }
  if (row.exact_dimension_control === 'true') {
    exactDimensionControlCounts.set(
      row.target_object,
      (exactDimensionControlCounts.get(row.target_object) ?? 0) + 1,
    );
  }
}

const objectRows = mappingRows.map((row) => {
  const template = templateByCisi.get(row.cisi) ?? {};
  const isVariant = row.local_signature_short === '154_variant' || row.local_signature_short === '033_variant';
  return {
    checked_date: '2026-05-25',
    cisi: row.cisi,
    fig4_number: row.fig4_number,
    manufacturing_group: row.manufacturing_group,
    template_class: template.template_class ?? '',
    local_signature_short: row.local_signature_short,
    role_700_03x_text: Object.entries(template)
      .filter(([key, value]) => key.endsWith('_role') && value === 'role_700_03x')
      .map(([key]) => template[key.replace('_role', '_text')])
      .join(';'),
    role_15x_003_text: Object.entries(template)
      .filter(([key, value]) => key.endsWith('_role') && value === 'role_15x_003')
      .map(([key]) => template[key.replace('_role', '_text')])
      .join(';'),
    is_singleton_variant: isVariant ? '1' : '0',
    variant_slot:
      row.local_signature_short === '154_variant'
        ? 'role_15x_003'
        : row.local_signature_short === '033_variant'
          ? 'role_700_03x'
          : '',
    same_group_template_single_slot_controls: String(oneSlotControlCounts.get(row.cisi) ?? 0),
    exact_dimension_single_slot_controls: String(exactDimensionControlCounts.get(row.cisi) ?? 0),
    accepted_decipherment_claim: '0',
  };
});

const totalPairs = choose2(objectRows.length);
const variants = objectRows.filter((row) => row.is_singleton_variant === '1');
const observedVariantPair = variants.map((row) => row.cisi).join(';');

function pairRows(rows) {
  const pairs = [];
  for (let i = 0; i < rows.length; i += 1) {
    for (let j = i + 1; j < rows.length; j += 1) {
      pairs.push([rows[i], rows[j]]);
    }
  }
  return pairs;
}

const pairs = pairRows(objectRows);
const observed = variants.length === 2 ? [variants[0], variants[1]] : [];

function sameManufacturingGroup(pair) {
  return pair[0].manufacturing_group === pair[1].manufacturing_group;
}

function bothGroup3(pair) {
  return pair.every((row) => row.manufacturing_group === 'group_3');
}

function sameTemplate(pair) {
  return pair[0].template_class === pair[1].template_class;
}

function bothTemplate700(pair) {
  return pair.every((row) => row.template_class === 'template_700_861_15x');
}

function bothGroup3Template700(pair) {
  return pair.every(
    (row) =>
      row.manufacturing_group === 'group_3' &&
      row.template_class === 'template_700_861_15x',
  );
}

function figAdjacent(pair) {
  return Math.abs(asNumber(pair[0].fig4_number) - asNumber(pair[1].fig4_number)) === 1;
}

function figAdjacentInGroup3(pair) {
  return figAdjacent(pair) && bothGroup3(pair);
}

function figAdjacentInGroup3Template700(pair) {
  return figAdjacent(pair) && bothGroup3Template700(pair);
}

const tests = [
  ['same_manufacturing_group', sameManufacturingGroup],
  ['both_in_group_3', bothGroup3],
  ['same_role_template_class', sameTemplate],
  ['both_in_template_700_861_15x', bothTemplate700],
  ['both_in_group_3_template_700_861_15x', bothGroup3Template700],
  ['adjacent_in_fig4_order', figAdjacent],
  ['adjacent_in_fig4_order_within_group_3', figAdjacentInGroup3],
  ['adjacent_in_fig4_order_within_group_3_template_700_861_15x', figAdjacentInGroup3Template700],
];

const testRows = tests.map(([testName, predicate]) => {
  const nullHits = pairs.filter(predicate).length;
  const observedHit = observed.length === 2 && predicate(observed) ? 1 : 0;
  return {
    checked_date: '2026-05-25',
    test_name: testName,
    observed_variant_pair: observedVariantPair,
    observed_hit: String(observedHit),
    null_pair_hits: String(nullHits),
    null_total_pairs: String(totalPairs),
    exact_pair_probability: pString(nullHits, totalPairs),
    interpretation_boundary:
      'post_hoc_localization_pressure_only; useful for confound control, not sign meaning',
    accepted_decipherment_claim: '0',
  };
});

const groupCounts = Object.fromEntries(
  [...new Set(objectRows.map((row) => row.manufacturing_group))].map((group) => [
    group,
    objectRows.filter((row) => row.manufacturing_group === group).length,
  ]),
);
const templateCounts = Object.fromEntries(
  [...new Set(objectRows.map((row) => row.template_class))].map((template) => [
    template,
    objectRows.filter((row) => row.template_class === template).length,
  ]),
);

const summary = {
  generated_at: '2026-05-25',
  artifact: 'lipi_h2218_h2239_variant_localization_null',
  object_rows: objectRows.length,
  singleton_variant_objects: variants.map((row) => row.cisi).join(';'),
  singleton_variant_slots: variants.map((row) => `${row.cisi}:${row.variant_slot}`).join(';'),
  manufacturing_group_counts: groupCounts,
  template_counts: templateCounts,
  total_unordered_variant_pair_nulls: totalPairs,
  tests: Object.fromEntries(
    testRows.map((row) => [
      row.test_name,
      {
        observed_hit: Number(row.observed_hit),
        null_pair_hits: Number(row.null_pair_hits),
        exact_pair_probability: Number(row.exact_pair_probability),
      },
    ]),
  ),
  same_group_template_controls_for_variants: Object.fromEntries(
    variants.map((row) => [row.cisi, Number(row.same_group_template_single_slot_controls)]),
  ),
  exact_dimension_controls_for_variants: Object.fromEntries(
    variants.map((row) => [row.cisi, Number(row.exact_dimension_single_slot_controls)]),
  ),
  accepted_decipherment_claims: 0,
  research_conclusion:
    'The two singleton H-series variants are both localized in group 3, the template_700_861_15x stratum, and adjacent Fig. 4 positions. This increases batch/workshop/local-template confound pressure while keeping the controlled-slot source target alive. It does not establish sign meaning, value, side function, or translation.',
};

fs.writeFileSync(objectOut, toCsv(objectRows));
fs.writeFileSync(testOut, toCsv(testRows));
fs.writeFileSync(summaryOut, `${JSON.stringify(summary, null, 2)}\n`);

console.log(`Wrote ${objectOut}`);
console.log(`Wrote ${testOut}`);
console.log(`Wrote ${summaryOut}`);
