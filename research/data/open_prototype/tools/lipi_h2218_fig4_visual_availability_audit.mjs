import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const mappingCsv = path.join(reportsDir, 'lipi_h2218_h2239_fig4_mapping.csv');
const imageLeadSummaryPath = path.join(reportsDir, 'h2218_h2239_public_image_lead_search_summary.json');
const outCsv = path.join(reportsDir, 'lipi_h2218_h2239_fig4_visual_availability.csv');
const outJson = path.join(reportsDir, 'lipi_h2218_h2239_fig4_visual_availability_summary.json');

const sourceUrl =
  'https://www.harappa.com/sites/default/files/pdf/Kenoyer2000_The%20Tiny%20Steatite%20Seals%20of%20Harappa.pdf';

const checkedAt = '2026-05-24';
const visualCheck = {
  source_pdf_url: sourceUrl,
  public_pdf_direct_download_status: '403_forbidden_via_shell_on_2026-05-24',
  public_pdf_web_visual_status: 'page_14_inspected_in_web_viewer',
  local_image_storage_status: 'no_pdf_or_figure_image_stored_in_repo',
  observed_figure_scope:
    'The public Fig. 4 image shows seal no. 1 plus tablet nos. 2-23; each tablet item appears as three side panels with a triangular/end-profile marker to the right.',
  legibility_limit:
    'The public PDF figure is coarse. It supports source coverage and plate-request targeting, but not segmentation-grade visual validation.',
};

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

const mappingRows = csvObjects(fs.readFileSync(mappingCsv, 'utf8')).sort(
  (a, b) => Number.parseInt(a.fig4_number, 10) - Number.parseInt(b.fig4_number, 10),
);

const imageLeadSummary = fs.existsSync(imageLeadSummaryPath)
  ? JSON.parse(fs.readFileSync(imageLeadSummaryPath, 'utf8'))
  : { unique_cisi_candidates_found: [] };
const publicLeadObjects = new Set(imageLeadSummary.unique_cisi_candidates_found ?? []);

const rows = mappingRows.map((row) => {
  const hasObjectLevelLead = publicLeadObjects.has(row.cisi);
  return {
    fig4_number: row.fig4_number,
    manufacturing_group: row.manufacturing_group,
    cisi: row.cisi,
    harp_object_full: row.harp_object_full,
    local_signature_short: row.local_signature_short,
    source_pdf_page_checked: 'web_viewer_page_14',
    fig4_tablet_panel_status: 'three_side_panels_visible_in_public_fig4',
    end_profile_marker_status: 'triangular_end_profile_marker_visible',
    legibility_status: 'coarse_not_segmentation_grade',
    object_level_public_image_lead_status: hasObjectLevelLead
      ? 'object_level_public_A_B_C_lead_found_for_H-2219'
      : 'no_object_level_public_A_B_C_lead_in_checked_RSS_blog_pages',
    admissible_use: 'series coverage, Fig. 4 item coverage, side-panel presence, plate-request targeting',
    non_admissible_use:
      'sign segmentation, allography, stroke counts, side orientation, physical side function, numerical value, metrological reading, sign meaning, phonetic value, language identity, translation',
    interpretation_status: 'no_reading_admissible',
  };
});

const csvRows = [
  [
    'fig4_number',
    'manufacturing_group',
    'cisi',
    'harp_object_full',
    'local_signature_short',
    'source_pdf_page_checked',
    'fig4_tablet_panel_status',
    'end_profile_marker_status',
    'legibility_status',
    'object_level_public_image_lead_status',
    'admissible_use',
    'non_admissible_use',
    'interpretation_status',
  ],
];

for (const row of rows) {
  csvRows.push([
    row.fig4_number,
    row.manufacturing_group,
    row.cisi,
    row.harp_object_full,
    row.local_signature_short,
    row.source_pdf_page_checked,
    row.fig4_tablet_panel_status,
    row.end_profile_marker_status,
    row.legibility_status,
    row.object_level_public_image_lead_status,
    row.admissible_use,
    row.non_admissible_use,
    row.interpretation_status,
  ]);
}

const rowsWithObjectLevelPublicLeads = rows.filter((row) =>
  row.object_level_public_image_lead_status.startsWith('object_level_public'),
).length;

const summary = {
  source: 'H-2218 through H-2239 Fig. 4 visual availability audit',
  checked_at: checkedAt,
  visual_check: visualCheck,
  source_rows: rows.length,
  expected_fig4_tablet_items: 22,
  visible_three_side_panel_rows: rows.filter(
    (row) => row.fig4_tablet_panel_status === 'three_side_panels_visible_in_public_fig4',
  ).length,
  visible_end_profile_marker_rows: rows.filter(
    (row) => row.end_profile_marker_status === 'triangular_end_profile_marker_visible',
  ).length,
  rows_with_object_level_public_image_leads: rowsWithObjectLevelPublicLeads,
  rows_without_object_level_public_image_leads: rows.length - rowsWithObjectLevelPublicLeads,
  object_level_public_image_lead_objects: [...publicLeadObjects].sort(),
  key_observation:
    'The public Fig. 4 image gives coarse visual coverage for all 22 tablet items, but object-level public A/B/C image leads were found only for H-2219 in the checked RSS/blog pages.',
  interpretation_boundary:
    'This audit accepts only public visual availability and source-coverage facts. It accepts no sign segmentation, allography, stroke counts, side orientation, physical side function, numerical value, metrological reading, sign meaning, phonetic value, language identity, or translation.',
  outputs: [
    path.relative(base, outCsv).replaceAll('\\', '/'),
    path.relative(base, outJson).replaceAll('\\', '/'),
  ],
};

fs.writeFileSync(outCsv, toCsv(csvRows));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
