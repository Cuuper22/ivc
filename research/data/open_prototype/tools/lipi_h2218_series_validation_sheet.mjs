import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const queuePath = path.join(reportsDir, 'lipi_multiside_mark_validation_queue.csv');
const outSheet = path.join(reportsDir, 'lipi_h2218_h2239_series_validation_sheet.csv');
const outSummary = path.join(reportsDir, 'lipi_h2218_h2239_series_validation_summary.json');

const seriesStart = 2218;
const seriesEnd = 2239;
const sourceUrl =
  'https://www.harappa.com/sites/default/files/pdf/KenoyerMeadow%202010%20Inscribed%20Objects%20from%20Harappa.pdf';

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

function csvObjects(text) {
  const rows = parseCsv(text);
  const header = rows.shift() ?? [];
  return rows.map((row) => Object.fromEntries(header.map((name, index) => [name, row[index] ?? ''])));
}

function naturalCisiNumber(cisi) {
  const match = String(cisi ?? '').match(/^H-(\d+)$/);
  return match ? Number(match[1]) : Number.POSITIVE_INFINITY;
}

function splitSideTexts(signature) {
  const result = new Map();
  for (const part of String(signature ?? '').split('|')) {
    const match = part.match(/^(\d+):(.+)$/);
    if (match) result.set(match[1], match[2]);
  }
  return result;
}

function parseExternalRef(externalText) {
  const text = String(externalText ?? '');
  const objectMatch = text.match(/^(H\d{2}-\d+)/);
  const figureMatch = text.match(/Figure\s+([0-9.]+)/i);
  return {
    harp_object: objectMatch ? objectMatch[1] : '',
    source_figure: figureMatch ? `Figure ${figureMatch[1]}` : '',
  };
}

function classifySignature(row) {
  const sideTexts = splitSideTexts(row.short_side_texts);
  const side1 = sideTexts.get('1') ?? '';
  const side2 = sideTexts.get('2') ?? '';
  const side3 = sideTexts.get('3') ?? '';
  const flags = [];
  if (side1 === '+861-003+' && side2 === '+700-034+' && side3 === '+156-003+') {
    flags.push('main_signature_A');
  } else if (side1 === '+700-034+' && side2 === '+861-003+' && side3 === '+156-003+') {
    flags.push('main_signature_B_side1_side2_swapped');
  } else {
    flags.push('minor_signature_variant');
  }
  if (side3.includes('154')) flags.push('side3_154_instead_of_156');
  if (side1.includes('033') || side2.includes('033') || side3.includes('033')) {
    flags.push('033_instead_of_034');
  }
  return flags.join(';');
}

const queueRows = csvObjects(fs.readFileSync(queuePath, 'utf8'))
  .filter((row) => {
    const number = naturalCisiNumber(row.cisi);
    return number >= seriesStart && number <= seriesEnd;
  })
  .sort((a, b) => naturalCisiNumber(a.cisi) - naturalCisiNumber(b.cisi));

const sheetRows = [
  [
    'cisi',
    'priority',
    'raw_ids',
    'harp_object',
    'source_figure',
    'horizontal_mm',
    'vertical_mm',
    'thickness_mm',
    'side_1_text',
    'side_2_text',
    'side_3_text',
    'local_signature_class',
    'sequence_family_count',
    'source_series_anchor',
    'source_context',
    'plate_check_status',
    'side_count_check_status',
    'side_order_check_status',
    'sign_segmentation_check_status',
    'variant_check_status',
    'interpretation_status',
    'next_manual_action',
  ],
];

const signatureCounts = new Map();
const figureCounts = new Map();
for (const row of queueRows) {
  signatureCounts.set(row.short_side_texts, (signatureCounts.get(row.short_side_texts) ?? 0) + 1);
  const { source_figure } = parseExternalRef(row.excavation_ids);
  if (source_figure) figureCounts.set(source_figure, (figureCounts.get(source_figure) ?? 0) + 1);
}

for (const row of queueRows) {
  const sideTexts = splitSideTexts(row.short_side_texts);
  const externalRef = parseExternalRef(row.excavation_ids);
  sheetRows.push([
    row.cisi,
    row.priority,
    row.raw_ids,
    externalRef.harp_object,
    externalRef.source_figure,
    row.horizontal_mm,
    row.vertical_mm,
    row.thickness_mm,
    sideTexts.get('1') ?? '',
    sideTexts.get('2') ?? '',
    sideTexts.get('3') ?? '',
    classifySignature(row),
    row.sequence_family_count,
    'Kenoyer and Meadow 2010 identifies H-2218 through H-2239 as a 22-object rectangular steatite tablet series, triangular in section.',
    'Reported as Period 3B secondary deposits outside the perimeter wall in Trench 11 on the east side of Mound E; tablet use remains unresolved.',
    'pending_plate_or_image_check',
    'pending',
    'pending',
    'pending',
    'pending_154_156_and_033_034_visual_check',
    'no_reading_admissible',
    'Locate plate/image for this figure, verify three physical sides, side order, segmentation, and visual variants before any functional test.',
  ]);
}

const summary = {
  source: 'H-2218 through H-2239 local validation sheet',
  source_url: sourceUrl,
  expected_series_size: 22,
  local_rows_found: queueRows.length,
  all_series_ids_present: queueRows.length === 22,
  priority_counts: Object.fromEntries(
    queueRows.reduce((counts, row) => {
      counts.set(row.priority, (counts.get(row.priority) ?? 0) + 1);
      return counts;
    }, new Map()),
  ),
  signature_counts: Object.fromEntries([...signatureCounts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))),
  source_figure_count: figureCounts.size,
  missing_source_figures: queueRows
    .filter((row) => !parseExternalRef(row.excavation_ids).source_figure)
    .map((row) => row.cisi),
  outputs: [path.relative(base, outSheet).replaceAll('\\', '/')],
  interpretation_boundary:
    'H-2218 through H-2239 source-anchored validation sheet only; no physical side function, numerical value, metrological reading, sign meaning, phonetic value, language identity, or translation is accepted.',
};

fs.writeFileSync(outSheet, toCsv(sheetRows));
fs.writeFileSync(outSummary, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
