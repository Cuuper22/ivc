// Side-context sheet for the most focused artifact family found so far:
// Harappa TAB:I tablets that combine the longer text +400-740-176+ with a
// short mark of +700-033+ or +700-034+. Before comparing 033 vs. 034 tablets
// in any way, we need to know exactly how each object's sides are laid out in
// the catalog and which layout variants exist.
//
// The script reads lipi_multiside_mark_validation_queue.csv, keeps the
// P1 mixed short-long TAB:I rows whose side signature contains the long mark
// plus one of the two short marks, and classifies each artifact's layout:
// canonical two-side long1-short2, reversed short1-long2, three-side with a
// double short mark, three-side with an extra longer text, or other. Each row
// keeps its raw ids, excavation ids, and dimensions, and carries an explicit
// validation-need note.
//
// Outputs: lipi_tab_i_mixed_400_740_176_side_context.csv (consumed by the
// dimension probe) and _summary.json. Current census: 26 artifacts, 20 of
// them canonical. A validation sheet only — no readings are accepted.

import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const queuePath = path.join(reportsDir, 'lipi_multiside_mark_validation_queue.csv');
const outCsv = path.join(reportsDir, 'lipi_tab_i_mixed_400_740_176_side_context.csv');
const outJson = path.join(reportsDir, 'lipi_tab_i_mixed_400_740_176_side_context_summary.json');

const longMark = '+400-740-176+';
const shortMarks = new Set(['+700-033+', '+700-034+']);

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
  const match = String(cisi ?? '').match(/^([A-Za-z]+)-(\d+)$/);
  return match ? `${match[1].padEnd(8, ' ')}${String(Number(match[2])).padStart(8, '0')}` : String(cisi ?? '');
}

function parseSideTexts(signature) {
  return String(signature ?? '')
    .split('|')
    .filter(Boolean)
    .map((part) => {
      const match = part.match(/^(\d+):(.+)$/);
      return match ? { side: match[1], text: match[2] } : { side: '', text: part };
    });
}

function countBy(rows, keyFn) {
  const counts = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return counts;
}

function countObject(counts) {
  return Object.fromEntries(
    [...counts.entries()].sort((a, b) => String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true })),
  );
}

function positiveNumber(value) {
  const n = Number.parseFloat(value);
  return Number.isFinite(n) && n > 0 ? n : null;
}

function numberRange(values) {
  const nums = values.map(positiveNumber).filter((value) => value !== null);
  if (!nums.length) return '';
  return `${Math.min(...nums)}-${Math.max(...nums)}`;
}

function classifyContext(sideTexts) {
  const longSides = sideTexts.filter((side) => side.text === longMark).map((side) => side.side);
  const shortSides = sideTexts.filter((side) => shortMarks.has(side.text)).map((side) => side.side);
  const otherSides = sideTexts.filter((side) => side.text !== longMark && !shortMarks.has(side.text));
  const shortTexts = sideTexts.filter((side) => shortMarks.has(side.text)).map((side) => side.text);
  const has033 = shortTexts.includes('+700-033+');
  const has034 = shortTexts.includes('+700-034+');

  let contextClass = 'other_context';
  if (sideTexts.length === 2 && longSides[0] === '1' && shortSides[0] === '2') {
    contextClass = 'two_side_long1_short2';
  } else if (sideTexts.length === 2 && shortSides[0] === '1' && longSides[0] === '2') {
    contextClass = 'two_side_short1_long2';
  } else if (sideTexts.length === 3 && longSides.includes('1') && shortSides.includes('2') && shortSides.includes('3')) {
    contextClass = 'three_side_long1_double_short';
  } else if (sideTexts.length === 3 && longSides.includes('3') && shortSides.includes('2') && otherSides.length === 1) {
    contextClass = 'three_side_extra_long_text';
  }

  return {
    context_class: contextClass,
    long_side_indexes: longSides.join(';'),
    short_side_indexes: shortSides.join(';'),
    other_side_texts: otherSides.map((side) => `${side.side}:${side.text}`).join('|'),
    short_mark_class: has033 && has034 ? '033_and_034' : has033 ? '033' : has034 ? '034' : 'none',
  };
}

const queueRows = csvObjects(fs.readFileSync(queuePath, 'utf8'));
const targetRows = queueRows
  .filter(
    (row) =>
      row.priority === 'P1_mixed_short_long_core' &&
      row.type === 'TAB:I' &&
      row.sequence_signature.includes(longMark) &&
      [...shortMarks].some((shortMark) => row.sequence_signature.includes(shortMark)),
  )
  .map((row) => {
    const sideTexts = parseSideTexts(row.sequence_signature);
    const context = classifyContext(sideTexts);
    return {
      cisi: row.cisi,
      type: row.type,
      site: row.site,
      row_count: row.row_count,
      side_indexes: row.side_indexes,
      sequence_signature: row.sequence_signature,
      context_class: context.context_class,
      long_mark: longMark,
      long_side_indexes: context.long_side_indexes,
      short_mark_class: context.short_mark_class,
      short_side_indexes: context.short_side_indexes,
      other_side_texts: context.other_side_texts,
      raw_ids: row.raw_ids,
      excavation_ids: row.excavation_ids,
      horizontal_mm: row.horizontal_mm,
      vertical_mm: row.vertical_mm,
      thickness_mm: row.thickness_mm,
      source_status: 'T3_lipi_planning_layer_pending_image_or_plate_validation',
      validation_need:
        'Confirm physical side relation, side order, sign segmentation, 033/034 contrast, and whether the short mark is a true side mark before any functional test.',
      interpretation_status: 'no_reading_admissible',
    };
  })
  .sort((a, b) => naturalCisiKey(a.cisi).localeCompare(naturalCisiKey(b.cisi)));

const csvRows = [
  [
    'cisi',
    'type',
    'site',
    'row_count',
    'side_indexes',
    'sequence_signature',
    'context_class',
    'long_mark',
    'long_side_indexes',
    'short_mark_class',
    'short_side_indexes',
    'other_side_texts',
    'raw_ids',
    'excavation_ids',
    'horizontal_mm',
    'vertical_mm',
    'thickness_mm',
    'source_status',
    'validation_need',
    'interpretation_status',
  ],
];

for (const row of targetRows) {
  csvRows.push([
    row.cisi,
    row.type,
    row.site,
    row.row_count,
    row.side_indexes,
    row.sequence_signature,
    row.context_class,
    row.long_mark,
    row.long_side_indexes,
    row.short_mark_class,
    row.short_side_indexes,
    row.other_side_texts,
    row.raw_ids,
    row.excavation_ids,
    row.horizontal_mm,
    row.vertical_mm,
    row.thickness_mm,
    row.source_status,
    row.validation_need,
    row.interpretation_status,
  ]);
}

const contextCounts = countObject(countBy(targetRows, (row) => row.context_class));
const shortMarkCounts = countObject(countBy(targetRows, (row) => row.short_mark_class));
const positiveHorizontal = targetRows.filter((row) => positiveNumber(row.horizontal_mm) !== null).length;
const positiveVertical = targetRows.filter((row) => positiveNumber(row.vertical_mm) !== null).length;
const positiveThickness = targetRows.filter((row) => positiveNumber(row.thickness_mm) !== null).length;

const summary = {
  source: 'TAB:I mixed +400-740-176+ side-context audit',
  checked_at: '2026-05-24',
  input_queue: path.relative(base, queuePath).replaceAll('\\', '/'),
  target_definition:
    'Harappa TAB:I P1 mixed short-long core artifacts whose side signature contains +400-740-176+ and either +700-033+ or +700-034+.',
  target_artifacts: targetRows.length,
  context_class_counts: contextCounts,
  short_mark_class_counts: shortMarkCounts,
  positive_horizontal_measurements: positiveHorizontal,
  positive_vertical_measurements: positiveVertical,
  positive_thickness_measurements: positiveThickness,
  horizontal_mm_positive_range: numberRange(targetRows.map((row) => row.horizontal_mm)),
  vertical_mm_positive_range: numberRange(targetRows.map((row) => row.vertical_mm)),
  thickness_mm_positive_range: numberRange(targetRows.map((row) => row.thickness_mm)),
  cisi_by_context_class: Object.fromEntries(
    Object.keys(contextCounts).map((contextClass) => [
      contextClass,
      targetRows.filter((row) => row.context_class === contextClass).map((row) => row.cisi),
    ]),
  ),
  key_observation:
    'The +400-740-176+ mixed TAB:I family has 26 target artifacts in the current planning layer: 20 canonical long-side-1/short-side-2 pairs, 4 reversed two-side pairs, 1 double-short-side case, and 1 three-side case with an extra longer text.',
  next_test:
    'After image or stronger catalog-side validation, test whether +700-033+ versus +700-034+ predicts dimensions, side placement, longer-text family, find context, or duplicate-family membership better than artifact/source controls.',
  interpretation_boundary:
    'This is a side-context validation sheet only. It accepts no numerical value, metrological reading, physical side function, sign meaning, phonetic value, language identity, or translation.',
  outputs: [
    path.relative(base, outCsv).replaceAll('\\', '/'),
    path.relative(base, outJson).replaceAll('\\', '/'),
  ],
};

fs.writeFileSync(outCsv, toCsv(csvRows));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
