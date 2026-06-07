import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const outCsv = path.join(reportsDir, 'lipi_frame700_034_clean_two_panel_close_read.csv');
const outJson = path.join(
  reportsDir,
  'lipi_frame700_034_clean_two_panel_close_read_summary.json',
);

function toCsv(rows) {
  if (rows.length === 0) return '';
  const header = Object.keys(rows[0]);
  const body = rows.map((row) =>
    header
      .map((key) => {
        const text = String(row[key] ?? '');
        return `"${text.replaceAll('"', '""')}"`;
      })
      .join(','),
  );
  return `${[header.map((key) => `"${key}"`).join(','), ...body].join('\n')}\n`;
}

function countBy(rows, key) {
  const counts = new Map();
  for (const row of rows) counts.set(row[key], (counts.get(row[key]) ?? 0) + 1);
  return Object.fromEntries(
    [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])),
  );
}

const rows = [
  {
    checked_date: '2026-05-25',
    cisi: 'H-930',
    priority: 'core',
    packet_lane: 'local_contrast_stress',
    packet_role: 'control_032',
    packet_batch: 'local_893_925_930;local_2137_925_930',
    ia_volume: 'CISI Collections in Pakistan',
    ia_leaf: '374',
    ia_reader_page_url:
      'https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/n374/mode/1up',
    source_page_heading: 'HARAPPA 927-942 TABLETS incised no iconography',
    local_frame700_row: '+700-032+',
    local_companion_row: '+740-900-004+',
    local_frame700_side: 'side_2',
    local_companion_side: 'side_1',
    source_labels_visible: 'H-930 A; H-930 B',
    source_panel_count_observed: '2',
    local_metadata_sides: '2',
    source_count_vs_local: 'matches',
    companion_panel_candidate_label: 'H-930 A',
    short_panel_candidate_label: 'H-930 B',
    catalog_compatible_source_mapping: 'A_matches_longer_companion_row;B_matches_short_frame700_row',
    close_read_observation:
      'H-930 A is the longer companion panel. H-930 B is the shorter two-sign panel; a left curved/V-shaped mark and a right vertical-bar/oval-like mark are visible, but the scan does not independently establish the catalog subtype 032.',
    image_quality_for_close_read:
      'good_for_object_identity_panel_count_and_short_vs_long_split;insufficient_for_subtype_or_direction',
    frame700_panel_visible: 'short_panel_visible_on_H-930_B',
    diagnostic_strokes_status: 'not_secure_enough_for_032_vs_033_vs_034_from_scan',
    side_order_basis_visible: 'printed_A_B_labels_only',
    direction_basis_visible: 'no_independent_direction_basis_visible',
    physical_side_mapping_status: 'catalog_compatible_but_not_source_proven',
    copy_variant_status: 'no_H-930_bis_numbered_or_ter_variant_visible_on_page',
    close_read_grade: 'B_plus_clean_two_panel_locator_not_subtype_validation',
    research_decision: 'use_as_clean_control_for_calibrating_next_source_close_reads',
    next_action:
      'compare against H-893 and H-925 only after their variant panels are disambiguated; keep exact order +700-032+ as catalog data, not a visual-source value',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: '2026-05-25',
    cisi: 'H-789',
    priority: 'core',
    packet_lane: 'independent_low_copy',
    packet_role: 'control_033',
    packet_batch: 'independent_771_789_1123',
    ia_volume: 'CISI Collections in Pakistan',
    ia_leaf: '359',
    ia_reader_page_url:
      'https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/n359/mode/1up',
    source_page_heading: 'HARAPPA 778-793 TABLETS in bas-relief no iconography',
    local_frame700_row: '+033-700+',
    local_companion_row: '+400-520-220-016+',
    local_frame700_side: 'side_2',
    local_companion_side: 'side_1',
    source_labels_visible: 'H-789 A; H-789 B',
    source_panel_count_observed: '2',
    local_metadata_sides: '2',
    source_count_vs_local: 'matches',
    companion_panel_candidate_label: 'H-789 A',
    short_panel_candidate_label: 'H-789 B',
    catalog_compatible_source_mapping: 'A_matches_longer_companion_row;B_matches_short_frame700_row',
    close_read_observation:
      'H-789 A is the longer companion panel. H-789 B is the shorter panel; the short panel is clear enough to separate it from the longer side, but bas-relief texture and scan contrast leave the 033-versus-neighbor diagnostic strokes unresolved.',
    image_quality_for_close_read:
      'good_for_object_identity_panel_count_and_short_vs_long_split;lower_than_H-930_for_stroke_diagnostics',
    frame700_panel_visible: 'short_panel_visible_on_H-789_B',
    diagnostic_strokes_status: 'not_secure_enough_for_032_vs_033_vs_034_from_scan',
    side_order_basis_visible: 'printed_A_B_labels_only',
    direction_basis_visible: 'no_independent_direction_basis_visible',
    physical_side_mapping_status: 'catalog_compatible_but_not_source_proven',
    copy_variant_status: 'no_H-789_bis_numbered_or_ter_variant_visible_on_page',
    close_read_grade: 'B_clean_two_panel_locator_lower_stroke_confidence',
    research_decision: 'use_as_independent_lane_control_after_preserving_scan_uncertainty',
    next_action:
      'pair with H-771 only after H-771 multiple-A-impression hazard is resolved; keep exact order +033-700+ as catalog data, not a visual-source value',
    accepted_decipherment_claim: '0',
  },
];

const summary = {
  checked_date: '2026-05-25',
  artifact: 'lipi_frame700_034_clean_two_panel_close_read',
  source_scope: 'manual close-read of IA CISI page images for H-930 and H-789',
  input_objects: rows.length,
  close_read_rows: rows.length,
  source_panel_count_matches_local_side_count: rows.filter(
    (row) => row.source_count_vs_local === 'matches',
  ).length,
  short_panel_candidate_on_printed_B: rows.filter((row) =>
    row.short_panel_candidate_label.endsWith('B'),
  ).length,
  companion_panel_candidate_on_printed_A: rows.filter((row) =>
    row.companion_panel_candidate_label.endsWith('A'),
  ).length,
  grade_counts: countBy(rows, 'close_read_grade'),
  decision_counts: countBy(rows, 'research_decision'),
  accepted_decipherment_claims: rows.filter((row) => row.accepted_decipherment_claim !== '0')
    .length,
  upgraded_evidence:
    'H-930 and H-789 are upgraded from page-located clean two-panel candidates to close-read clean controls for panel-count and short-vs-long side calibration.',
  still_blocked:
    'Neither scan independently establishes 032/033 subtype, reading direction, physical side order, sign meaning, phonetic value, or translation.',
  immediate_research_consequence:
    'H-930 should calibrate strict-local source close-reading; H-789 should calibrate independent-lane controls. Messy targets H-771, H-893, H-925, H-983, and H-353 cannot inherit these upgrades without variant/side reconciliation.',
};

fs.mkdirSync(reportsDir, { recursive: true });
fs.writeFileSync(outCsv, toCsv(rows));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
