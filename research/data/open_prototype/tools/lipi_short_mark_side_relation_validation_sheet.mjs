import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const companionRowsPath = path.join(reportsDir, 'lipi_short_mark_companion_context_rows.csv');
const queuePath = path.join(reportsDir, 'lipi_multiside_mark_validation_queue.csv');
const outRowsCsv = path.join(reportsDir, 'lipi_short_mark_side_relation_validation_sheet.csv');
const outPriorityCsv = path.join(reportsDir, 'lipi_short_mark_side_relation_priority_summary.csv');
const outJson = path.join(reportsDir, 'lipi_short_mark_side_relation_validation_summary.json');

const focusCompanions = new Set(['033', '034']);
const rawHintSequence = '+400-740-176+';

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

function hasRawHint(row) {
  return String(row.longer_texts ?? '')
    .split('|')
    .includes(rawHintSequence);
}

function priority(row) {
  const rawHint = hasRawHint(row);
  if (row.companion === '033' && row.side_relation === 'short_after_all_longer' && rawHint) {
    return ['P1_033_after_with_400_740_176', 120];
  }
  if (row.companion === '034' && row.side_relation === 'short_before_all_longer' && rawHint) {
    return ['P1_034_before_with_400_740_176', 118];
  }
  if (row.companion === '033' && row.side_relation === 'short_after_all_longer') {
    return ['P1_033_after_corrected_relation', 100];
  }
  if (row.companion === '034' && row.side_relation === 'short_before_all_longer') {
    return ['P1_034_before_contrast_relation', 96];
  }
  if (row.companion === '034' && row.side_relation === 'short_after_all_longer') {
    return ['P2_034_after_exception_control', 82];
  }
  if (row.companion === '033' && row.side_relation === 'short_before_all_longer') {
    return ['P2_033_before_exception_control', 80];
  }
  if (rawHint) {
    return ['P2_raw_400_740_176_context', 75];
  }
  if (row.side_relation === 'no_longer_text') {
    return ['P3_no_longer_text_control', 40];
  }
  return ['P3_other_033_034_context', 50];
}

function validationQuestion(row, priorityClass) {
  const baseQuestion =
    'Confirm whether the catalog side relation between the short mark and longer text is physical, photographic, editorial, or arbitrary; preserve exact short-mark order and image direction.';
  if (priorityClass.startsWith('P1_033_after')) {
    return `${baseQuestion} This row is part of the corrected 033 overrepresentation in short-after-longer contexts.`;
  }
  if (priorityClass.startsWith('P1_034_before')) {
    return `${baseQuestion} This row is part of the 034 contrast set where 034 is not concentrated in short-after-longer contexts.`;
  }
  if (priorityClass.startsWith('P2_034_after')) {
    return `${baseQuestion} This is an exception/control row for 034 appearing after longer text.`;
  }
  if (priorityClass.startsWith('P2_033_before')) {
    return `${baseQuestion} This is an exception/control row for 033 appearing before longer text.`;
  }
  if (priorityClass === 'P3_no_longer_text_control') {
    return 'Confirm whether this is truly an all-short or no-longer-text artifact before using it as a control.';
  }
  return baseQuestion;
}

const companionRows = csvObjects(fs.readFileSync(companionRowsPath, 'utf8'));
const queueRows = csvObjects(fs.readFileSync(queuePath, 'utf8'));
const queueByCisi = new Map(queueRows.map((row) => [row.cisi, row]));

const sheetRows = companionRows
  .filter((row) => focusCompanions.has(row.companion))
  .map((row) => {
    const queue = queueByCisi.get(row.cisi) ?? {};
    const [priorityClass, priorityScore] = priority(row);
    const rawHint = hasRawHint(row);
    return {
      priority: priorityClass,
      priority_score: priorityScore,
      cisi: row.cisi,
      type: row.type,
      site: row.site,
      sides: row.sides,
      short_side_index: row.short_side_index,
      companion: row.companion,
      order: row.order,
      short_text: row.short_text,
      context_class: row.context_class,
      side_relation: row.side_relation,
      longer_row_count: row.longer_row_count,
      longer_side_indexes: row.longer_side_indexes,
      longer_texts: row.longer_texts,
      has_400_740_176: rawHint ? 'true' : 'false',
      group_signature: row.group_signature,
      source_priority_from_multiside_queue: queue.priority ?? '',
      raw_ids: queue.raw_ids ?? '',
      excavation_ids: queue.excavation_ids ?? '',
      horizontal_mm: queue.horizontal_mm ?? '',
      vertical_mm: queue.vertical_mm ?? '',
      thickness_mm: queue.thickness_mm ?? '',
      validation_question: validationQuestion(row, priorityClass),
      interpretation_status: 'source_validation_target_only_no_reading',
    };
  })
  .sort(
    (a, b) =>
      b.priority_score - a.priority_score ||
      naturalCisiKey(a.cisi).localeCompare(naturalCisiKey(b.cisi)) ||
      Number(a.short_side_index || 0) - Number(b.short_side_index || 0),
  );

const rowOut = [
  [
    'priority',
    'priority_score',
    'cisi',
    'type',
    'site',
    'sides',
    'short_side_index',
    'companion',
    'order',
    'short_text',
    'context_class',
    'side_relation',
    'longer_row_count',
    'longer_side_indexes',
    'longer_texts',
    'has_400_740_176',
    'group_signature',
    'source_priority_from_multiside_queue',
    'raw_ids',
    'excavation_ids',
    'horizontal_mm',
    'vertical_mm',
    'thickness_mm',
    'validation_question',
    'interpretation_status',
  ],
  ...sheetRows.map((row) => [
    row.priority,
    row.priority_score,
    row.cisi,
    row.type,
    row.site,
    row.sides,
    row.short_side_index,
    row.companion,
    row.order,
    row.short_text,
    row.context_class,
    row.side_relation,
    row.longer_row_count,
    row.longer_side_indexes,
    row.longer_texts,
    row.has_400_740_176,
    row.group_signature,
    row.source_priority_from_multiside_queue,
    row.raw_ids,
    row.excavation_ids,
    row.horizontal_mm,
    row.vertical_mm,
    row.thickness_mm,
    row.validation_question,
    row.interpretation_status,
  ]),
];

const priorityRows = [...countBy(sheetRows, (row) => row.priority).entries()]
  .map(([priorityClass, rows]) => {
    const subset = sheetRows.filter((row) => row.priority === priorityClass);
    return {
      priority: priorityClass,
      rows,
      artifacts: new Set(subset.map((row) => row.cisi)).size,
      companion_counts: objectFromCounts(countBy(subset, (row) => row.companion)),
      side_relation_counts: objectFromCounts(countBy(subset, (row) => row.side_relation)),
      raw_hint_rows: subset.filter((row) => row.has_400_740_176 === 'true').length,
      sample_cisi: [...new Set(subset.map((row) => row.cisi))].slice(0, 15).join(';'),
    };
  })
  .sort((a, b) => {
    const maxScoreA = Math.max(...sheetRows.filter((row) => row.priority === a.priority).map((row) => row.priority_score));
    const maxScoreB = Math.max(...sheetRows.filter((row) => row.priority === b.priority).map((row) => row.priority_score));
    return maxScoreB - maxScoreA || a.priority.localeCompare(b.priority);
  });

const priorityOut = [
  ['priority', 'rows', 'artifacts', 'companion_counts', 'side_relation_counts', 'raw_400_740_176_rows', 'sample_cisi'],
  ...priorityRows.map((row) => [
    row.priority,
    row.rows,
    row.artifacts,
    Object.entries(row.companion_counts)
      .map(([key, value]) => `${key}:${value}`)
      .join(';'),
    Object.entries(row.side_relation_counts)
      .map(([key, value]) => `${key}:${value}`)
      .join(';'),
    row.raw_hint_rows,
    row.sample_cisi,
  ]),
];

const summary = {
  source: 'Harappa TAB:B/TAB:I 033/034 side-relation validation sheet',
  checked_at: '2026-05-24',
  inputs: [
    'data/open_prototype/reports/lipi_short_mark_companion_context_rows.csv',
    'data/open_prototype/reports/lipi_multiside_mark_validation_queue.csv',
  ],
  target_rows: sheetRows.length,
  target_artifacts: new Set(sheetRows.map((row) => row.cisi)).size,
  companion_counts: objectFromCounts(countBy(sheetRows, (row) => row.companion)),
  side_relation_counts: objectFromCounts(countBy(sheetRows, (row) => row.side_relation)),
  priority_counts: objectFromCounts(countBy(sheetRows, (row) => row.priority)),
  raw_400_740_176_rows: sheetRows.filter((row) => row.has_400_740_176 === 'true').length,
  raw_400_740_176_artifacts: new Set(sheetRows.filter((row) => row.has_400_740_176 === 'true').map((row) => row.cisi)).size,
  top_priority_rows: sheetRows.slice(0, 20).map((row) => ({
    priority: row.priority,
    cisi: row.cisi,
    companion: row.companion,
    side_relation: row.side_relation,
    short_text: row.short_text,
    longer_texts: row.longer_texts,
  })),
  key_observation:
    'This sheet converts the corrected 033/034 catalog-side relation contrast into source-validation targets. It does not accept physical side order, side function, numerical value, sign meaning, or translation.',
  interpretation_boundary:
    'This is a source-validation worklist only. It accepts no physical side function, numerical value, metrological reading, sign meaning, phonetic value, language identity, or translation.',
  outputs: [
    'data/open_prototype/reports/lipi_short_mark_side_relation_validation_sheet.csv',
    'data/open_prototype/reports/lipi_short_mark_side_relation_priority_summary.csv',
    'data/open_prototype/reports/lipi_short_mark_side_relation_validation_summary.json',
  ],
};

fs.writeFileSync(outRowsCsv, toCsv(rowOut));
fs.writeFileSync(outPriorityCsv, toCsv(priorityOut));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
