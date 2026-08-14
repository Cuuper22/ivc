// Builds the human validation work queue for the short-side-mark hypothesis.
// Statistics alone cannot tell whether a catalog "side row" is a real
// physically separate side or a transcription artifact — someone has to look
// at photographs and excavation records. This script decides which objects to
// check first and what question to ask about each.
//
// It reads the per-side detail (lipi_multiside_mark_rows.csv) plus the raw
// lipi/metadata_filtered.csv (for raw ids, excavation numbers, and exact
// dimensions), keeps only Harappa TAB:B and TAB:I tablets, and groups rows by
// object. Each object with a short-mark side gets a priority tier: P1 for
// TAB:I three-side short series (the H-series pattern) and for objects mixing
// core short marks with focus long-text signs; P2 for other core short marks;
// P3 for the rest. Objects whose exact side-text signature recurs across many
// artifacts get a score bonus, since one photo check can settle a whole family.
//
// Outputs: lipi_multiside_mark_validation_queue.csv (ranked queue, one
// validation question per object), _sequence_families.csv (recurring
// signatures), and _validation_summary.json. Downstream audits (e.g. the
// template recurrence audit) consume the queue CSV.

import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const lipiDir = path.join(base, 'data', 'open_prototype', 'lipi');

const rowPath = path.join(reportsDir, 'lipi_multiside_mark_rows.csv');
const metadataPath = path.join(lipiDir, 'metadata_filtered.csv');

const outQueue = path.join(reportsDir, 'lipi_multiside_mark_validation_queue.csv');
const outFamilies = path.join(reportsDir, 'lipi_multiside_mark_sequence_families.csv');
const outJson = path.join(reportsDir, 'lipi_multiside_mark_validation_summary.json');

const targetStrata = new Set(['Harappa\tTAB:B', 'Harappa\tTAB:I']);
const coreShortTokens = new Set(['700', '034', '033', '032', '003', '861', '156']);
const tabISide3Tokens = new Set(['003', '156', '154']);
const longFocusTokens = new Set(['740', '400', '176', '240']);

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

function parseTokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function parseBool(value) {
  return String(value).toLowerCase() === 'true';
}

function sideFromRawId(id) {
  const match = String(id ?? '').match(/\.(\d+)$/);
  return match ? match[1] : '';
}

function naturalCisiKey(cisi) {
  const match = String(cisi ?? '').match(/^([A-Za-z]+)-(\d+)$/);
  return match ? `${match[1].padEnd(8, ' ')}${String(Number(match[2])).padStart(8, '0')}` : String(cisi ?? '');
}

function uniqueSorted(values) {
  return [...new Set(values.filter((value) => value !== '' && value !== undefined && value !== null))]
    .sort((a, b) => String(a).localeCompare(String(b), undefined, { numeric: true }));
}

function uniqueTokens(rows) {
  return uniqueSorted(rows.flatMap((row) => row.tokens));
}

function sideTextSignature(rows) {
  return rows
    .slice()
    .sort((a, b) => Number(a.side_index) - Number(b.side_index) || String(a.text).localeCompare(String(b.text)))
    .map((row) => `${row.side_index}:${row.text}`)
    .join('|');
}

function countBy(rows, keyFn) {
  const counts = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return counts;
}

function formatTopCounts(counts, limit = 10) {
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }))
    .slice(0, limit)
    .map(([key, count]) => `${key}:${count}`)
    .join(';');
}

const metadata = csvObjects(fs.readFileSync(metadataPath, 'utf8'));
const metadataBySide = new Map();
for (const row of metadata) {
  const side = sideFromRawId(row.id);
  if (!side) continue;
  metadataBySide.set(`${row.cisi}\t${side}`, row);
}

const rows = csvObjects(fs.readFileSync(rowPath, 'utf8'))
  .map((row) => {
    const raw = metadataBySide.get(`${row.cisi}\t${row.side_index}`) ?? {};
    return {
      ...row,
      raw_id: raw.id ?? '',
      excavation_idno: raw['excavation-idno'] ?? '',
      horizontal_mm: raw['horizontal(mm)'] ?? '',
      vertical_mm: raw['vertical(mm)'] ?? '',
      thickness_mm: raw['thickness(mm)'] ?? '',
      tokens: parseTokens(row.text),
      short_mark_candidate: parseBool(row.short_mark_candidate),
      long_text_candidate: parseBool(row.long_text_candidate),
    };
  })
  .filter((row) => targetStrata.has(`${row.site}\t${row.type}`));

const groups = new Map();
for (const row of rows) {
  if (!groups.has(row.cisi)) groups.set(row.cisi, []);
  groups.get(row.cisi).push(row);
}

const candidateGroups = [];
for (const [cisi, groupRows] of groups.entries()) {
  const shortRows = groupRows.filter((row) => row.short_mark_candidate);
  if (!shortRows.length) continue;
  const longRows = groupRows.filter((row) => row.long_text_candidate);
  const type = groupRows[0].type;
  const site = groupRows[0].site;
  const allRowsShortOnly = shortRows.length === groupRows.length && groupRows.length >= 2;
  const shortTokens = uniqueTokens(shortRows);
  const longTokens = uniqueTokens(longRows);
  const focusShortTokens = shortTokens.filter((token) => coreShortTokens.has(token));
  const focusLongTokens = longTokens.filter((token) => longFocusTokens.has(token));
  const hasTabISide3Focus =
    type === 'TAB:I' &&
    shortRows.some((row) => row.side_index === '3' && row.tokens.some((token) => tabISide3Tokens.has(token)));
  const hasMixedCoreLong = focusShortTokens.length > 0 && focusLongTokens.length > 0 && longRows.length > 0;
  const sequenceSignature = sideTextSignature(groupRows);

  let priority = 'P3_other_short_mark';
  let priorityScore = 30;
  let validationQuestion =
    'Check whether the catalog side rows are physically separate and whether the short row is a mark, damaged text, or entry artifact.';

  if (hasTabISide3Focus && allRowsShortOnly && groupRows.length >= 3) {
    priority = 'P1_tab_i_three_side_short_series';
    priorityScore = 100;
    validationQuestion =
      'Confirm whether all three catalog rows are distinct physical sides, whether side order is stable, and whether the repeated side-3 003/156 pattern is artifact-side structure or catalog convention.';
  } else if (hasMixedCoreLong) {
    priority = 'P1_mixed_short_long_core';
    priorityScore = 90;
    validationQuestion =
      'Confirm the physical relation between the short side mark and the longer text row, then test whether the co-occurrence survives image/source validation.';
  } else if (type === 'TAB:B' && focusShortTokens.length > 0) {
    priority = 'P2_tab_b_core_short_queue';
    priorityScore = 60;
    validationQuestion =
      'Validate whether the recurring TAB:B short marks are true side marks and whether side indexes 1 and 2 are comparable across artifacts.';
  } else if (type === 'TAB:I' && focusShortTokens.length > 0) {
    priority = 'P2_tab_i_core_short_queue';
    priorityScore = 55;
    validationQuestion =
      'Validate whether the recurring TAB:I short marks are true side marks outside the three-side short-series cluster.';
  }

  candidateGroups.push({
    cisi,
    type,
    site,
    sides: groupRows[0].sides,
    row_count: groupRows.length,
    short_mark_rows: shortRows.length,
    long_text_rows: longRows.length,
    side_indexes: uniqueSorted(groupRows.map((row) => row.side_index)).join(';'),
    short_side_texts: sideTextSignature(shortRows),
    long_side_texts: sideTextSignature(longRows),
    short_tokens: shortTokens.join(';'),
    long_tokens: longTokens.join(';'),
    focus_short_tokens: focusShortTokens.join(';'),
    focus_long_tokens: focusLongTokens.join(';'),
    sequence_signature: sequenceSignature,
    raw_ids: uniqueSorted(groupRows.map((row) => row.raw_id)).join(';'),
    excavation_ids: uniqueSorted(groupRows.map((row) => row.excavation_idno)).join(';'),
    horizontal_mm: uniqueSorted(groupRows.map((row) => row.horizontal_mm)).join(';'),
    vertical_mm: uniqueSorted(groupRows.map((row) => row.vertical_mm)).join(';'),
    thickness_mm: uniqueSorted(groupRows.map((row) => row.thickness_mm)).join(';'),
    priority,
    priority_score: priorityScore,
    validation_question: validationQuestion,
  });
}

const familyCounts = countBy(candidateGroups, (row) => `${row.type}\t${row.sequence_signature}`);
for (const row of candidateGroups) {
  row.sequence_family_count = familyCounts.get(`${row.type}\t${row.sequence_signature}`) ?? 1;
  row.priority_score = Number(row.priority_score) + Math.min(20, row.sequence_family_count);
}

candidateGroups.sort(
  (a, b) =>
    b.priority_score - a.priority_score ||
    b.sequence_family_count - a.sequence_family_count ||
    naturalCisiKey(a.cisi).localeCompare(naturalCisiKey(b.cisi)),
);

const queueRows = [
  [
    'priority',
    'priority_score',
    'cisi',
    'type',
    'site',
    'sides',
    'row_count',
    'short_mark_rows',
    'long_text_rows',
    'side_indexes',
    'short_side_texts',
    'long_side_texts',
    'short_tokens',
    'long_tokens',
    'focus_short_tokens',
    'focus_long_tokens',
    'sequence_family_count',
    'sequence_signature',
    'raw_ids',
    'excavation_ids',
    'horizontal_mm',
    'vertical_mm',
    'thickness_mm',
    'validation_question',
  ],
];

for (const row of candidateGroups) {
  queueRows.push([
    row.priority,
    row.priority_score,
    row.cisi,
    row.type,
    row.site,
    row.sides,
    row.row_count,
    row.short_mark_rows,
    row.long_text_rows,
    row.side_indexes,
    row.short_side_texts,
    row.long_side_texts,
    row.short_tokens,
    row.long_tokens,
    row.focus_short_tokens,
    row.focus_long_tokens,
    row.sequence_family_count,
    row.sequence_signature,
    row.raw_ids,
    row.excavation_ids,
    row.horizontal_mm,
    row.vertical_mm,
    row.thickness_mm,
    row.validation_question,
  ]);
}

const familyRows = [
  [
    'type',
    'sequence_signature',
    'artifact_count',
    'sample_cisi',
    'priority_counts',
    'short_tokens',
    'long_tokens',
  ],
];

const families = new Map();
for (const row of candidateGroups) {
  const key = `${row.type}\t${row.sequence_signature}`;
  if (!families.has(key)) families.set(key, []);
  families.get(key).push(row);
}

for (const [key, familyRowsForKey] of [...families.entries()].sort(
  (a, b) => b[1].length - a[1].length || a[0].localeCompare(b[0], undefined, { numeric: true }),
)) {
  const [type, sequenceSignature] = key.split('\t');
  familyRows.push([
    type,
    sequenceSignature,
    familyRowsForKey.length,
    familyRowsForKey
      .map((row) => row.cisi)
      .sort((a, b) => naturalCisiKey(a).localeCompare(naturalCisiKey(b)))
      .slice(0, 12)
      .join(';'),
    formatTopCounts(countBy(familyRowsForKey, (row) => row.priority), 5),
    uniqueSorted(familyRowsForKey.flatMap((row) => row.short_tokens.split(';').filter(Boolean))).join(';'),
    uniqueSorted(familyRowsForKey.flatMap((row) => row.long_tokens.split(';').filter(Boolean))).join(';'),
  ]);
}

const priorityCounts = Object.fromEntries(countBy(candidateGroups, (row) => row.priority));
const summary = {
  source: 'lipi multi-side mark stratified validation queue',
  target_strata: ['Harappa TAB:B', 'Harappa TAB:I'],
  artifact_groups_with_short_marks: candidateGroups.length,
  priority_counts: priorityCounts,
  top_sequence_families: [...families.entries()]
    .sort((a, b) => b[1].length - a[1].length || a[0].localeCompare(b[0], undefined, { numeric: true }))
    .slice(0, 10)
    .map(([key, rowsForKey]) => {
      const [type, sequenceSignature] = key.split('\t');
      return {
        type,
        sequence_signature: sequenceSignature,
        artifact_count: rowsForKey.length,
        sample_cisi: rowsForKey
          .map((row) => row.cisi)
          .sort((a, b) => naturalCisiKey(a).localeCompare(naturalCisiKey(b)))
          .slice(0, 12),
        priority_counts: Object.fromEntries(countBy(rowsForKey, (row) => row.priority)),
      };
    }),
  outputs: [
    path.relative(base, outQueue).replaceAll('\\', '/'),
    path.relative(base, outFamilies).replaceAll('\\', '/'),
  ],
  interpretation_boundary:
    'Artifact-side validation queue only; repeated short-mark families are not numerical values, metrological readings, physical side functions, sign meanings, phonetic values, language identity, or translations.',
};

fs.writeFileSync(outQueue, toCsv(queueRows));
fs.writeFileSync(outFamilies, toCsv(familyRows));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
