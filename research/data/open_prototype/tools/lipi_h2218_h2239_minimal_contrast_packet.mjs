import fs from 'node:fs';
import path from 'node:path';

// Within the near-identical H-2218..H-2239 tablets, two objects deviate from the shared
// template by exactly one sign: H-2237 writes +154-003+ where its siblings write +156-003+,
// and H-2238 writes +700-033+ where they write +700-034+. Those are the closest things to
// minimal pairs this series offers. This script builds the control packet for them. It reads
// the side-role template CSV and the Fig. 4 mapping (for manufacturing group, HARP IDs, and
// dimensions), then, for each variant, finds every control tablet from the same
// manufacturing group and template class that differs on exactly the one contrast slot with
// exactly the expected normal text. Controls are ranked by physical closeness (horizontal,
// vertical, area deltas, then Fig. 4 distance), and flagged when the dimension match is
// exact. Output is a CSV of target/control pairs with the source question and admissibility
// rule each pair must pass, plus a JSON summary naming H-2237/H-2233 as the strongest pair.
// These are source-validation targets, not readings.

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const templatePath = path.join(reportsDir, 'lipi_h2218_h2239_side_role_templates.csv');
const fig4Path = path.join(reportsDir, 'lipi_h2218_h2239_fig4_mapping.csv');
const outCsv = path.join(reportsDir, 'lipi_h2218_h2239_minimal_contrast_packet.csv');
const outJson = path.join(reportsDir, 'lipi_h2218_h2239_minimal_contrast_summary.json');

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    if (inQuotes) {
      if (char === '"') {
        if (text[i + 1] === '"') {
          field += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        field += char;
      }
    } else if (char === '"') {
      inQuotes = true;
    } else if (char === ',') {
      row.push(field);
      field = '';
    } else if (char === '\n') {
      row.push(field);
      field = '';
      if (row.length > 1 || row[0] !== '') rows.push(row);
      row = [];
    } else if (char !== '\r') {
      field += char;
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
  return rows.map((row) => Object.fromEntries(header.map((key, index) => [key, row[index] ?? ''])));
}

function toCsv(rows) {
  if (rows.length === 0) return '';
  const header = Object.keys(rows[0]);
  const lines = rows.map((row) =>
    header
      .map((key) => {
        const text = String(row[key] ?? '');
        return `"${text.replaceAll('"', '""')}"`;
      })
      .join(','),
  );
  return `${[header.map((key) => `"${key}"`).join(','), ...lines].join('\n')}\n`;
}

function num(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function absDiff(a, b) {
  if (a === null || b === null) return '';
  return Math.abs(a - b);
}

function fmt(value) {
  if (value === '') return '';
  return Number(value).toFixed(6).replace(/\.?0+$/u, '');
}

function area(row) {
  const h = num(row.local_horizontal_mm);
  const v = num(row.local_vertical_mm);
  return h === null || v === null ? null : h * v;
}

function sideTexts(row) {
  return [row.side_1_text, row.side_2_text, row.side_3_text];
}

function diffSlots(target, control) {
  return sideTexts(target)
    .map((text, index) => ({
      side: index + 1,
      target: text,
      control: sideTexts(control)[index],
    }))
    .filter((item) => item.target !== item.control);
}

const templates = csvObjects(fs.readFileSync(templatePath, 'utf8'));
const fig4 = csvObjects(fs.readFileSync(fig4Path, 'utf8'));
const fig4ByCisi = new Map(fig4.map((row) => [row.cisi, row]));
const rowsByCisi = new Map(
  templates.map((row) => {
    const figure = fig4ByCisi.get(row.cisi) ?? {};
    return [
      row.cisi,
      {
        ...row,
        local_horizontal_mm: figure.local_horizontal_mm ?? '',
        local_vertical_mm: figure.local_vertical_mm ?? '',
        local_signature_class: figure.local_signature_class ?? '',
        harp_object_full: figure.harp_object_full ?? '',
        source_figure: figure.source_figure ?? '',
        local_source_figure: figure.local_source_figure ?? '',
      },
    ];
  }),
);

const normalTextByRole = {
  role_700_03x: '+700-034+',
  role_15x_003: '+156-003+',
};

const variants = [
  {
    cisi: 'H-2237',
    contrast_slot: 'role_15x_003_side_3',
    target_variant: '+154-003+',
    normal_text: '+156-003+',
    source_question:
      'Is the 154/156 side-3 difference visually real on the same physical side role?',
  },
  {
    cisi: 'H-2238',
    contrast_slot: 'role_700_03x_side_1',
    target_variant: '+700-033+',
    normal_text: '+700-034+',
    source_question:
      'Is the 033/034 side-1 difference visually real in the same 700 side-role environment?',
  },
];

function isCanonicalControl(target, control, variant) {
  if (control.cisi === target.cisi) return false;
  if (control.manufacturing_group !== target.manufacturing_group) return false;
  if (control.template_class !== target.template_class) return false;
  const diffs = diffSlots(target, control);
  if (diffs.length !== 1) return false;
  const [diff] = diffs;
  return diff.target === variant.target_variant && diff.control === variant.normal_text;
}

function rankControl(target, control) {
  const hDelta = absDiff(num(target.local_horizontal_mm), num(control.local_horizontal_mm));
  const vDelta = absDiff(num(target.local_vertical_mm), num(control.local_vertical_mm));
  const areaDelta = absDiff(area(target), area(control));
  const figDelta = absDiff(num(target.fig4_number), num(control.fig4_number));
  return {
    hDelta,
    vDelta,
    areaDelta,
    figDelta,
    rank:
      Number(hDelta || 0) * 1000 +
      Number(vDelta || 0) * 100 +
      Number(areaDelta || 0) +
      Number(figDelta || 0) / 1000,
  };
}

const packetRows = [];
for (const variant of variants) {
  const target = rowsByCisi.get(variant.cisi);
  const controls = templates
    .map((row) => rowsByCisi.get(row.cisi))
    .filter((control) => isCanonicalControl(target, control, variant))
    .map((control) => ({
      control,
      rank: rankControl(target, control),
    }))
    .sort((a, b) => a.rank.rank - b.rank.rank);

  for (const { control, rank } of controls) {
    const diffs = diffSlots(target, control);
    const exactDimensionControl =
      rank.hDelta === 0 && rank.vDelta === 0 && rank.areaDelta === 0 ? 'true' : 'false';
    packetRows.push({
      checked_date: '2026-05-25',
      target_object: target.cisi,
      control_object: control.cisi,
      contrast_slot: variant.contrast_slot,
      target_variant_text: variant.target_variant,
      control_normal_text: variant.normal_text,
      differing_side_count: diffs.length,
      differing_side_numbers: diffs.map((item) => item.side).join(';'),
      invariant_side_texts: sideTexts(target)
        .map((text, index) => (text === sideTexts(control)[index] ? `side_${index + 1}:${text}` : ''))
        .filter(Boolean)
        .join(';'),
      target_fig4_number: target.fig4_number,
      control_fig4_number: control.fig4_number,
      target_group: target.manufacturing_group,
      control_group: control.manufacturing_group,
      target_template: target.template_class,
      control_template: control.template_class,
      target_harp_object: target.harp_object_full,
      control_harp_object: control.harp_object_full,
      target_dimensions: `${target.local_horizontal_mm}x${target.local_vertical_mm}`,
      control_dimensions: `${control.local_horizontal_mm}x${control.local_vertical_mm}`,
      horizontal_delta_mm: fmt(rank.hDelta),
      vertical_delta_mm: fmt(rank.vDelta),
      area_delta_mm2: fmt(rank.areaDelta),
      fig4_distance: fmt(rank.figDelta),
      exact_dimension_control: exactDimensionControl,
      source_question: variant.source_question,
      admissibility_rule:
        'Admissible only if high-resolution source images confirm same physical side role, direction basis, and diagnostic stroke separation for the differing slot.',
      accepted_decipherment_claim: '0',
    });
  }
}

const summary = {
  checked_date: '2026-05-25',
  artifact: 'lipi_h2218_h2239_minimal_contrast_packet',
  variant_targets: variants.length,
  contrast_rows: packetRows.length,
  exact_dimension_single_slot_controls: packetRows.filter(
    (row) => row.exact_dimension_control === 'true' && Number(row.differing_side_count) === 1,
  ).length,
  same_group_template_single_slot_controls: packetRows.filter(
    (row) => Number(row.differing_side_count) === 1,
  ).length,
  h2237_controls: packetRows.filter((row) => row.target_object === 'H-2237').map((row) => row.control_object).join(';'),
  h2238_controls: packetRows.filter((row) => row.target_object === 'H-2238').map((row) => row.control_object).join(';'),
  accepted_decipherment_claims: packetRows.filter((row) => row.accepted_decipherment_claim !== '0').length,
  research_conclusion:
    'H-2237 and H-2238 are narrow minimal-contrast candidates inside the H-2218 through H-2239 side-role template. H-2237/H-2233 is the strongest local pair because it is same group, same template, single-slot, and exact-dimension matched. This is a source-validation target, not a reading.',
};

fs.mkdirSync(reportsDir, { recursive: true });
fs.writeFileSync(outCsv, toCsv(packetRows), 'utf8');
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
