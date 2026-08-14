import fs from 'node:fs';
import path from 'node:path';

// Meadow and Kenoyer 2000 published a photograph (their Fig. 4) of the tiny steatite tablets
// behind the H-2218..H-2239 catalog series, and sorted them into three manufacturing groups.
// This script joins that published figure to our local data. The fig4Map table transcribes,
// by hand from the PDF, each figure position's HARP excavation number and manufacturing
// group; the script matches those against the local series validation sheet by compact HARP
// ID and carries over each tablet's side texts, side-order signature class (canonical A,
// side-swapped B, or a variant), and dimensions. It writes the merged mapping CSV and a JSON
// summary that cross-tabulates manufacturing group against signature class. The finding it
// records: the manufacturing groups do not line up with the side-order classes -- every
// group mixes them -- so side order is not just a batch artifact. No reading is accepted.

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const sheetPath = path.join(reportsDir, 'lipi_h2218_h2239_series_validation_sheet.csv');
const outCsv = path.join(reportsDir, 'lipi_h2218_h2239_fig4_mapping.csv');
const outJson = path.join(reportsDir, 'lipi_h2218_h2239_fig4_mapping_summary.json');

const sourceUrl =
  'https://www.harappa.com/sites/default/files/pdf/Kenoyer2000_The%20Tiny%20Steatite%20Seals%20of%20Harappa.pdf';

const fig4Map = [
  { fig4_number: 2, harp_object_full: 'H97-3304/8040-01', manufacturing_group: 'group_1' },
  { fig4_number: 3, harp_object_full: 'H97-3305/8040-02', manufacturing_group: 'group_1' },
  { fig4_number: 4, harp_object_full: 'H97-3312/8040-05', manufacturing_group: 'group_1' },
  { fig4_number: 5, harp_object_full: 'H97-3314/8040-07', manufacturing_group: 'group_1' },
  { fig4_number: 6, harp_object_full: 'H97-3290/8010-03', manufacturing_group: 'group_1' },
  { fig4_number: 7, harp_object_full: 'H97-3315/8040-08', manufacturing_group: 'group_1' },
  { fig4_number: 8, harp_object_full: 'H97-3318/8040-12', manufacturing_group: 'group_2' },
  { fig4_number: 9, harp_object_full: 'H97-3333/8038-01', manufacturing_group: 'group_2' },
  { fig4_number: 10, harp_object_full: 'H97-3317/8040-11', manufacturing_group: 'group_2' },
  { fig4_number: 11, harp_object_full: 'H97-3319/8040-13', manufacturing_group: 'group_2' },
  { fig4_number: 12, harp_object_full: 'H97-3316/8040-09', manufacturing_group: 'group_2' },
  { fig4_number: 13, harp_object_full: 'H97-3313/8040-06', manufacturing_group: 'group_2' },
  { fig4_number: 14, harp_object_full: 'H97-3306/8040-03', manufacturing_group: 'group_2' },
  { fig4_number: 15, harp_object_full: 'H97-3307/8040-04', manufacturing_group: 'group_2' },
  { fig4_number: 16, harp_object_full: 'H96-3046/6951-04', manufacturing_group: 'group_2' },
  { fig4_number: 17, harp_object_full: 'H96-3125/6937-16', manufacturing_group: 'group_3' },
  { fig4_number: 18, harp_object_full: 'H95-2613/6560-01', manufacturing_group: 'group_3' },
  { fig4_number: 19, harp_object_full: 'H97-3311/8040-10', manufacturing_group: 'group_3' },
  { fig4_number: 20, harp_object_full: 'H97-3341/8039-10', manufacturing_group: 'group_3' },
  { fig4_number: 21, harp_object_full: 'H97-3320/8040-14', manufacturing_group: 'group_3' },
  { fig4_number: 22, harp_object_full: 'H97-3322/8040-16', manufacturing_group: 'group_3' },
  { fig4_number: 23, harp_object_full: 'H97-3321/8040-15', manufacturing_group: 'group_3' },
];

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

function compactHarpId(full) {
  const match = String(full ?? '').match(/^(H\d{2}-\d+)/);
  return match ? match[1] : String(full ?? '');
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

function signatureShortName(localClass) {
  if (localClass === 'main_signature_A') return 'A';
  if (localClass === 'main_signature_B_side1_side2_swapped') return 'B_side_swap';
  if (localClass.includes('side3_154_instead_of_156')) return '154_variant';
  if (localClass.includes('033_instead_of_034')) return '033_variant';
  return 'other';
}

const sheetRows = csvObjects(fs.readFileSync(sheetPath, 'utf8'));
const sheetByHarp = new Map(sheetRows.map((row) => [row.harp_object, row]));

const rows = [];
const missing = [];
for (const sourceRow of fig4Map) {
  const compact = compactHarpId(sourceRow.harp_object_full);
  const local = sheetByHarp.get(compact);
  if (!local) {
    missing.push(sourceRow);
    continue;
  }
  rows.push({
    fig4_number: sourceRow.fig4_number,
    manufacturing_group: sourceRow.manufacturing_group,
    cisi: local.cisi,
    harp_object: compact,
    harp_object_full: sourceRow.harp_object_full,
    source_figure: 'Meadow and Kenoyer 2000 Fig. 4',
    local_source_figure: local.source_figure,
    side_1_text: local.side_1_text,
    side_2_text: local.side_2_text,
    side_3_text: local.side_3_text,
    local_signature_class: local.local_signature_class,
    local_signature_short: signatureShortName(local.local_signature_class),
    local_horizontal_mm: local.horizontal_mm,
    local_vertical_mm: local.vertical_mm,
    plate_visual_check_status: 'coarse_public_fig4_available_pending_detailed_check',
    interpretation_status: 'no_reading_admissible',
  });
}

rows.sort((a, b) => a.fig4_number - b.fig4_number);

const outRows = [
  [
    'fig4_number',
    'manufacturing_group',
    'cisi',
    'harp_object',
    'harp_object_full',
    'source_figure',
    'local_source_figure',
    'side_1_text',
    'side_2_text',
    'side_3_text',
    'local_signature_class',
    'local_signature_short',
    'local_horizontal_mm',
    'local_vertical_mm',
    'plate_visual_check_status',
    'interpretation_status',
  ],
];

for (const row of rows) {
  outRows.push([
    row.fig4_number,
    row.manufacturing_group,
    row.cisi,
    row.harp_object,
    row.harp_object_full,
    row.source_figure,
    row.local_source_figure,
    row.side_1_text,
    row.side_2_text,
    row.side_3_text,
    row.local_signature_class,
    row.local_signature_short,
    row.local_horizontal_mm,
    row.local_vertical_mm,
    row.plate_visual_check_status,
    row.interpretation_status,
  ]);
}

const groupSignatureCounts = {};
for (const [group, groupRows] of countBy(rows, (row) => row.manufacturing_group)) {
  const subset = rows.filter((row) => row.manufacturing_group === group);
  groupSignatureCounts[group] = {
    artifact_count: groupRows,
    local_signature_counts: objectFromCounts(countBy(subset, (row) => row.local_signature_short)),
    cisi: subset.map((row) => row.cisi),
  };
}

const summary = {
  source: 'H-2218 through H-2239 Fig. 4 source mapping',
  source_url: sourceUrl,
  mapped_fig4_items: rows.length,
  expected_fig4_tablet_items: 22,
  missing_fig4_items: missing,
  manufacturing_group_signature_counts: groupSignatureCounts,
  key_observation:
    'The Meadow and Kenoyer 2000 manufacturing groups do not collapse to the local side-order signature classes; every group contains a mix of local signature classes or variants.',
  outputs: [path.relative(base, outCsv).replaceAll('\\', '/')],
  interpretation_boundary:
    'Fig. 4 mapping and coarse visual-source availability only; no physical side function, numerical value, metrological reading, sign meaning, phonetic value, language identity, or translation is accepted.',
};

fs.writeFileSync(outCsv, toCsv(outRows));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
