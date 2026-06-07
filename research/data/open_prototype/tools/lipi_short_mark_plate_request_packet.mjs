import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const validationSheetPath = path.join(reportsDir, 'lipi_short_mark_side_relation_validation_sheet.csv');
const outPacketCsv = path.join(reportsDir, 'lipi_short_mark_plate_request_packet.csv');
const outJson = path.join(reportsDir, 'lipi_short_mark_plate_request_packet_summary.json');

const topPriorityClasses = new Set(['P1_033_after_with_400_740_176', 'P1_034_before_with_400_740_176']);

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

function naturalCisiKey(cisi) {
  const match = String(cisi ?? '').match(/^([A-Za-z?]+)-(\d+)$/);
  return match ? `${match[1].padEnd(8, ' ')}${String(Number(match[2])).padStart(8, '0')}` : String(cisi ?? '');
}

function unique(values) {
  return [...new Set(values.filter((value) => value !== ''))];
}

function countBy(rows, keyFn) {
  const counts = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return counts;
}

function objectFromCounts(counts) {
  return Object.fromEntries([...counts.entries()].sort((a, b) => a[0].localeCompare(b[0], undefined, { numeric: true })));
}

const sourceRows = csvObjects(fs.readFileSync(validationSheetPath, 'utf8'));
const topRows = sourceRows.filter((row) => topPriorityClasses.has(row.priority));

const grouped = new Map();
for (const row of topRows) {
  if (!grouped.has(row.cisi)) grouped.set(row.cisi, []);
  grouped.get(row.cisi).push(row);
}

const packetRows = [...grouped.entries()]
  .map(([cisi, rows]) => {
    const first = rows[0];
    const shortSideTexts = rows.map((row) => `${row.short_side_index}:${row.short_text}`).join('|');
    const shortOrders = unique(rows.map((row) => `${row.companion}:${row.order}`)).join(';');
    const sideRelations = unique(rows.map((row) => row.side_relation)).join(';');
    const priorities = unique(rows.map((row) => row.priority)).join(';');
    return {
      request_tier: first.priority.startsWith('P1_033') ? 'tier_1_033_after_with_400_740_176' : 'tier_1_034_before_with_400_740_176',
      cisi,
      type: first.type,
      site: first.site,
      row_count_in_packet: rows.length,
      sides: first.sides,
      priority: priorities,
      short_side_texts: shortSideTexts,
      short_orders: shortOrders,
      side_relations: sideRelations,
      longer_texts: first.longer_texts,
      group_signature: first.group_signature,
      raw_ids: first.raw_ids,
      excavation_ids: first.excavation_ids,
      horizontal_mm: first.horizontal_mm,
      vertical_mm: first.vertical_mm,
      thickness_mm: first.thickness_mm,
      source_found: '',
      source_citation: '',
      image_or_plate_id: '',
      image_resolution_or_quality: '',
      catalog_rows_distinct_physical_sides: '',
      side_order_basis: '',
      image_direction_basis: '',
      short_mark_verified: '',
      longer_text_verified: '',
      sign_033_034_contrast_visible: '',
      relation_survives_image_check: '',
      validation_outcome: '',
      notes: '',
      allowed_validation_outcomes:
        'passes_source_check;fails_side_relation;fails_segmentation;fails_033_034_contrast;direction_unresolved;source_unavailable',
      interpretation_status: 'manual_plate_request_only_no_reading',
    };
  })
  .sort((a, b) => {
    const tierCmp = a.request_tier.localeCompare(b.request_tier);
    if (tierCmp) return tierCmp;
    return naturalCisiKey(a.cisi).localeCompare(naturalCisiKey(b.cisi));
  });

const packetOut = [
  [
    'request_tier',
    'cisi',
    'type',
    'site',
    'row_count_in_packet',
    'sides',
    'priority',
    'short_side_texts',
    'short_orders',
    'side_relations',
    'longer_texts',
    'group_signature',
    'raw_ids',
    'excavation_ids',
    'horizontal_mm',
    'vertical_mm',
    'thickness_mm',
    'source_found',
    'source_citation',
    'image_or_plate_id',
    'image_resolution_or_quality',
    'catalog_rows_distinct_physical_sides',
    'side_order_basis',
    'image_direction_basis',
    'short_mark_verified',
    'longer_text_verified',
    'sign_033_034_contrast_visible',
    'relation_survives_image_check',
    'validation_outcome',
    'notes',
    'allowed_validation_outcomes',
    'interpretation_status',
  ],
  ...packetRows.map((row) => [
    row.request_tier,
    row.cisi,
    row.type,
    row.site,
    row.row_count_in_packet,
    row.sides,
    row.priority,
    row.short_side_texts,
    row.short_orders,
    row.side_relations,
    row.longer_texts,
    row.group_signature,
    row.raw_ids,
    row.excavation_ids,
    row.horizontal_mm,
    row.vertical_mm,
    row.thickness_mm,
    row.source_found,
    row.source_citation,
    row.image_or_plate_id,
    row.image_resolution_or_quality,
    row.catalog_rows_distinct_physical_sides,
    row.side_order_basis,
    row.image_direction_basis,
    row.short_mark_verified,
    row.longer_text_verified,
    row.sign_033_034_contrast_visible,
    row.relation_survives_image_check,
    row.validation_outcome,
    row.notes,
    row.allowed_validation_outcomes,
    row.interpretation_status,
  ]),
];

const summary = {
  source: '033/034 short-mark side-relation first plate request packet',
  checked_at: '2026-05-24',
  input: 'data/open_prototype/reports/lipi_short_mark_side_relation_validation_sheet.csv',
  packet_artifacts: packetRows.length,
  packet_rows_from_validation_sheet: topRows.length,
  request_tier_counts: objectFromCounts(countBy(packetRows, (row) => row.request_tier)),
  type_counts: objectFromCounts(countBy(packetRows, (row) => row.type)),
  artifact_ids: packetRows.map((row) => row.cisi),
  duplicated_artifacts_in_packet: packetRows.filter((row) => row.row_count_in_packet > 1).map((row) => row.cisi),
  blank_manual_fields: [
    'source_found',
    'source_citation',
    'image_or_plate_id',
    'image_resolution_or_quality',
    'catalog_rows_distinct_physical_sides',
    'side_order_basis',
    'image_direction_basis',
    'short_mark_verified',
    'longer_text_verified',
    'sign_033_034_contrast_visible',
    'relation_survives_image_check',
    'validation_outcome',
    'notes',
  ],
  allowed_validation_outcomes: [
    'passes_source_check',
    'fails_side_relation',
    'fails_segmentation',
    'fails_033_034_contrast',
    'direction_unresolved',
    'source_unavailable',
  ],
  key_observation:
    'This packet is the first manual source-validation request for the 033/034 side-relation contrast. It contains prefilled artifact context and blank evidence fields, so source inspection can accept, weaken, or reject the planning-layer contrast.',
  interpretation_boundary:
    'This is a manual plate request packet only. It accepts no physical side function, numerical value, metrological reading, sign meaning, phonetic value, language identity, or translation.',
  outputs: [
    'data/open_prototype/reports/lipi_short_mark_plate_request_packet.csv',
    'data/open_prototype/reports/lipi_short_mark_plate_request_packet_summary.json',
  ],
};

fs.writeFileSync(outPacketCsv, toCsv(packetOut));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
