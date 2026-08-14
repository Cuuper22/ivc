// Does the three-role side template of the H-2218..H-2239 tablets appear
// anywhere else in the corpus? Those 22 tablets each carry one +861-003+ side,
// one +700-03x+ side, and one +15x-003+ side. If the same template shows up on
// other objects, the H-series is part of a wider convention; if not, it is a
// local production batch.
//
// The script reads lipi_multiside_mark_validation_queue.csv (about 397
// multi-side objects, each with a per-side sequence signature). For every
// object it checks the template two ways: "strict" matches the exact side
// texts, and "unordered" matches the same sign tokens regardless of their
// order within a side. It flags complete three-role matches and near matches
// (non-H objects with at least two of the three role families).
//
// It writes a full audit CSV, a ranked near-match CSV, and a JSON summary
// (lipi_h2218_template_recurrence_*). As with the sibling probes, this is
// pattern bookkeeping only — no reading or meaning is claimed.

import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const inputCsv = path.join(reportsDir, 'lipi_multiside_mark_validation_queue.csv');
const outRowsCsv = path.join(reportsDir, 'lipi_h2218_template_recurrence_rows.csv');
const outNearCsv = path.join(reportsDir, 'lipi_h2218_template_recurrence_near_matches.csv');
const outJson = path.join(reportsDir, 'lipi_h2218_template_recurrence_summary.json');

const hSeriesIds = new Set([
  'H-2218',
  'H-2219',
  'H-2220',
  'H-2221',
  'H-2222',
  'H-2223',
  'H-2224',
  'H-2225',
  'H-2226',
  'H-2227',
  'H-2228',
  'H-2229',
  'H-2230',
  'H-2231',
  'H-2232',
  'H-2233',
  'H-2234',
  'H-2235',
  'H-2236',
  'H-2237',
  'H-2238',
  'H-2239',
]);

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

function parseSideSignature(signature) {
  return String(signature ?? '')
    .split('|')
    .filter(Boolean)
    .map((part) => {
      const match = part.match(/^(\d+):(.+)$/);
      return match ? { side_index: match[1], text: match[2] } : { side_index: '', text: part };
    });
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function tokenKey(text) {
  return tokens(text).sort().join('-');
}

function strictRole(text) {
  if (text === '+861-003+') return 'role_861_003';
  if (text === '+700-033+' || text === '+700-034+') return 'role_700_03x';
  if (text === '+154-003+' || text === '+156-003+') return 'role_15x_003';
  return '';
}

function unorderedRole(text) {
  const key = tokenKey(text);
  if (key === '003-861') return 'role_861_003';
  if (key === '033-700' || key === '034-700') return 'role_700_03x';
  if (key === '003-154' || key === '003-156') return 'role_15x_003';
  return '';
}

function hTemplateClass(rolesBySide) {
  const roles = ['1', '2', '3'].map((side) => rolesBySide[side] ?? '').join('|');
  if (roles === 'role_861_003|role_700_03x|role_15x_003') return 'template_861_700_15x';
  if (roles === 'role_700_03x|role_861_003|role_15x_003') return 'template_700_861_15x';
  return '';
}

function unique(values) {
  return [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
}

const rows = csvObjects(fs.readFileSync(inputCsv, 'utf8'));

const audited = rows.map((row) => {
  const sides = parseSideSignature(row.sequence_signature);
  const strictRoles = sides.map((side) => strictRole(side.text)).filter(Boolean);
  const unorderedRoles = sides.map((side) => unorderedRole(side.text)).filter(Boolean);
  const strictBySide = Object.fromEntries(sides.map((side) => [side.side_index, strictRole(side.text)]));
  const unorderedBySide = Object.fromEntries(sides.map((side) => [side.side_index, unorderedRole(side.text)]));
  const strictRoleSet = unique(strictRoles);
  const unorderedRoleSet = unique(unorderedRoles);
  const strictTemplateClass = hTemplateClass(strictBySide);
  const unorderedTemplateClass = hTemplateClass(unorderedBySide);
  const isHSeries = hSeriesIds.has(row.cisi);
  const completeStrictHInventory =
    strictRoleSet.includes('role_861_003') &&
    strictRoleSet.includes('role_700_03x') &&
    strictRoleSet.includes('role_15x_003') &&
    sides.length === 3 &&
    strictRoles.length === 3;
  const completeUnorderedHInventory =
    unorderedRoleSet.includes('role_861_003') &&
    unorderedRoleSet.includes('role_700_03x') &&
    unorderedRoleSet.includes('role_15x_003') &&
    sides.length === 3 &&
    unorderedRoles.length === 3;
  return {
    ...row,
    h_series: isHSeries,
    side_count_from_signature: sides.length,
    strict_h_roles_present: strictRoleSet.join(';'),
    strict_h_role_count: strictRoleSet.length,
    unordered_h_roles_present: unorderedRoleSet.join(';'),
    unordered_h_role_count: unorderedRoleSet.length,
    strict_h_template_class: strictTemplateClass,
    unordered_h_template_class: unorderedTemplateClass,
    strict_complete_h_inventory: completeStrictHInventory,
    unordered_complete_h_inventory: completeUnorderedHInventory,
    strict_role_15x_side: Object.entries(strictBySide)
      .filter(([, role]) => role === 'role_15x_003')
      .map(([side]) => side)
      .join(';'),
    unordered_role_15x_side: Object.entries(unorderedBySide)
      .filter(([, role]) => role === 'role_15x_003')
      .map(([side]) => side)
      .join(';'),
  };
});

const rowOut = [
  [
    'cisi',
    'priority',
    'type',
    'site',
    'h_series',
    'side_count_from_signature',
    'row_count',
    'short_mark_rows',
    'long_text_rows',
    'sequence_signature',
    'strict_h_roles_present',
    'strict_h_role_count',
    'unordered_h_roles_present',
    'unordered_h_role_count',
    'strict_h_template_class',
    'unordered_h_template_class',
    'strict_complete_h_inventory',
    'unordered_complete_h_inventory',
    'strict_role_15x_side',
    'unordered_role_15x_side',
    'interpretation_status',
  ],
];

for (const row of audited) {
  rowOut.push([
    row.cisi,
    row.priority,
    row.type,
    row.site,
    row.h_series,
    row.side_count_from_signature,
    row.row_count,
    row.short_mark_rows,
    row.long_text_rows,
    row.sequence_signature,
    row.strict_h_roles_present,
    row.strict_h_role_count,
    row.unordered_h_roles_present,
    row.unordered_h_role_count,
    row.strict_h_template_class,
    row.unordered_h_template_class,
    row.strict_complete_h_inventory,
    row.unordered_complete_h_inventory,
    row.strict_role_15x_side,
    row.unordered_role_15x_side,
    'no_reading_admissible',
  ]);
}

const nearRows = audited
  .filter((row) => !row.h_series && (row.strict_h_role_count >= 2 || row.unordered_h_role_count >= 2))
  .sort(
    (a, b) =>
      b.unordered_h_role_count - a.unordered_h_role_count ||
      b.strict_h_role_count - a.strict_h_role_count ||
      Number(b.sequence_family_count) - Number(a.sequence_family_count) ||
      a.cisi.localeCompare(b.cisi, undefined, { numeric: true }),
  );

const nearOut = [
  [
    'cisi',
    'priority',
    'type',
    'site',
    'side_count_from_signature',
    'sequence_family_count',
    'sequence_signature',
    'strict_h_roles_present',
    'strict_h_role_count',
    'unordered_h_roles_present',
    'unordered_h_role_count',
    'strict_h_template_class',
    'unordered_h_template_class',
    'interpretation_status',
  ],
];
for (const row of nearRows) {
  nearOut.push([
    row.cisi,
    row.priority,
    row.type,
    row.site,
    row.side_count_from_signature,
    row.sequence_family_count,
    row.sequence_signature,
    row.strict_h_roles_present,
    row.strict_h_role_count,
    row.unordered_h_roles_present,
    row.unordered_h_role_count,
    row.strict_h_template_class,
    row.unordered_h_template_class,
    'near_match_review_only_no_reading',
  ]);
}

function countRows(filterFn) {
  return audited.filter(filterFn).length;
}

const strictCompleteRows = audited.filter((row) => row.strict_complete_h_inventory);
const unorderedCompleteRows = audited.filter((row) => row.unordered_complete_h_inventory);
const nonHStrictCompleteRows = strictCompleteRows.filter((row) => !row.h_series);
const nonHUnorderedCompleteRows = unorderedCompleteRows.filter((row) => !row.h_series);
const nonHNearRows = nearRows;

const summary = {
  source: 'H-2218 through H-2239 side-role template recurrence audit',
  checked_at: '2026-05-24',
  input: path.relative(base, inputCsv).replaceAll('\\', '/'),
  validation_queue_rows: audited.length,
  h_series_rows: countRows((row) => row.h_series),
  non_h_series_rows: countRows((row) => !row.h_series),
  strict_complete_h_inventory_rows: strictCompleteRows.length,
  strict_complete_h_inventory_non_h_rows: nonHStrictCompleteRows.length,
  unordered_complete_h_inventory_rows: unorderedCompleteRows.length,
  unordered_complete_h_inventory_non_h_rows: nonHUnorderedCompleteRows.length,
  strict_template_class_counts: objectFromCounts(countBy(audited.filter((row) => row.strict_h_template_class), (row) => row.strict_h_template_class)),
  unordered_template_class_counts: objectFromCounts(
    countBy(audited.filter((row) => row.unordered_h_template_class), (row) => row.unordered_h_template_class),
  ),
  non_h_near_match_rows: nonHNearRows.length,
  non_h_near_match_priority_counts: objectFromCounts(countBy(nonHNearRows, (row) => row.priority)),
  non_h_near_match_top_examples: nonHNearRows.slice(0, 12).map((row) => ({
    cisi: row.cisi,
    priority: row.priority,
    type: row.type,
    site: row.site,
    sequence_signature: row.sequence_signature,
    strict_h_roles_present: row.strict_h_roles_present,
    unordered_h_roles_present: row.unordered_h_roles_present,
  })),
  key_observation:
    nonHStrictCompleteRows.length === 0
      ? 'In the current 397-row validation queue, the complete strict H-2218 through H-2239 three-role template occurs only inside the H-series. No non-H row has even two of the three H-series role families under the strict or unordered role checks.'
      : 'The complete strict H-2218 through H-2239 three-role template recurs outside the H-series and needs broader source validation before treating the H-series as isolated.',
  interpretation_boundary:
    'This is a recurrence audit for a local side-role template only. It accepts no physical side function, numerical value, metrological reading, sign meaning, phonetic value, language identity, or translation.',
  outputs: [outRowsCsv, outNearCsv, outJson].map((file) => path.relative(base, file).replaceAll('\\', '/')),
};

fs.writeFileSync(outRowsCsv, toCsv(rowOut));
fs.writeFileSync(outNearCsv, toCsv(nearOut));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
