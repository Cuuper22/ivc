import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const outCsv = path.join(reportsDir, 'lipi_frame700_034_ia_cisi_visual_inspection.csv');
const outJson = path.join(reportsDir, 'lipi_frame700_034_ia_cisi_visual_inspection_summary.json');

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
    cisi: 'H-771',
    priority: 'core',
    packet_lane: 'independent_low_copy',
    packet_role: 'target_034',
    packet_batch: 'independent_771_789_1123',
    ia_volume: 'CISI Collections in Pakistan',
    ia_leafs_inspected: '358',
    page_kind: 'visual_plate_page',
    source_page_heading: 'HARAPPA 768-777 TABLETS in bas-relief no iconography',
    source_labels_visible:
      'H-771 A; H-771 A bis; H-771 A ter; H-771 A quater; H-771 B',
    source_panel_count_observed: '5',
    local_metadata_sides: '2',
    local_frame700_row: '+700-034+',
    local_companion_row: '+032-257-840+',
    visual_object_identity_status: 'source_page_label_visible',
    source_side_label_status: 'A_B_labels_plus_multiple_A_impressions',
    source_side_count_status: 'source_panels_exceed_local_side_count',
    frame700_candidate_visible: 'rough_short_mark_panel_visible_on_H-771_B',
    diagnostic_subtype_status: 'not_accepted_from_scan',
    side_order_status: 'unresolved_A_B_labels_not_mapped_to_local_side_indices',
    copy_or_variant_risk: 'multiple_A_impressions_or_plate_variants',
    source_coding_decision: 'visual_source_found_but_disambiguation_required',
    decision_reason:
      'Page gives object-labeled panels, but multiple A impressions make local two-side coding unsafe until panel-to-row mapping is checked.',
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
    ia_leafs_inspected: '359',
    page_kind: 'visual_plate_page',
    source_page_heading: 'HARAPPA 778-793 TABLETS in bas-relief no iconography',
    source_labels_visible: 'H-789 A; H-789 B',
    source_panel_count_observed: '2',
    local_metadata_sides: '2',
    local_frame700_row: '+033-700+',
    local_companion_row: '+400-520-220-016+',
    visual_object_identity_status: 'source_page_label_visible',
    source_side_label_status: 'A_B_labels_visible',
    source_side_count_status: 'source_panel_count_matches_local_side_count',
    frame700_candidate_visible: 'rough_short_mark_panel_visible_on_H-789_B',
    diagnostic_subtype_status: 'not_accepted_from_scan',
    side_order_status: 'unresolved_A_B_labels_not_mapped_to_local_side_indices',
    copy_or_variant_risk: 'low_on_page_no_bis_or_numbered_variant_for_object',
    source_coding_decision: 'visual_source_found_two_panel_object',
    decision_reason:
      'Page gives two labeled panels matching local side count, but direction and 033-versus-neighbor diagnostic strokes still need close inspection.',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: '2026-05-25',
    cisi: 'H-893',
    priority: 'core',
    packet_lane: 'local_contrast_stress',
    packet_role: 'target_034',
    packet_batch: 'local_893_925_930',
    ia_volume: 'CISI Collections in Pakistan',
    ia_leafs_inspected: '371',
    page_kind: 'visual_plate_page',
    source_page_heading: 'HARAPPA 886-898 TABLETS incised no iconography',
    source_labels_visible: 'H-893 A; H-893 B; H-893 (1) A; H-893 (1) B',
    source_panel_count_observed: '4',
    local_metadata_sides: '2',
    local_frame700_row: '+700-034+',
    local_companion_row: '+400-740-337+',
    visual_object_identity_status: 'source_page_label_visible',
    source_side_label_status: 'A_B_labels_plus_numbered_variant',
    source_side_count_status: 'source_panels_exceed_local_side_count',
    frame700_candidate_visible: 'rough_short_mark_panel_visible_on_H-893_B_or_variant_B',
    diagnostic_subtype_status: 'not_accepted_from_scan',
    side_order_status: 'unresolved_A_B_labels_not_mapped_to_local_side_indices',
    copy_or_variant_risk: 'numbered_variant_present',
    source_coding_decision: 'visual_source_found_but_variant_disambiguation_required',
    decision_reason:
      'This is a strict local-contrast target, but the page exposes H-893 and H-893(1) variants; the correct physical object/panel must be selected before upgrade.',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: '2026-05-25',
    cisi: 'H-925',
    priority: 'core',
    packet_lane: 'local_contrast_stress',
    packet_role: 'control_033',
    packet_batch: 'local_893_925_930;local_2137_925_930',
    ia_volume: 'CISI Collections in Pakistan',
    ia_leafs_inspected: '373',
    page_kind: 'visual_plate_page',
    source_page_heading: 'HARAPPA 912-920 TABLETS incised no iconography',
    source_labels_visible:
      'H-925 A; H-925 B; H-925 (1) A; H-925 (2) A; H-925 (2) B; H-925 (1) B; H-925 A bis; H-925 B bis; H-925 A ter',
    source_panel_count_observed: '9',
    local_metadata_sides: '2',
    local_frame700_row: '+700-033+',
    local_companion_row: '+740-840-013+',
    visual_object_identity_status: 'source_page_label_visible',
    source_side_label_status: 'A_B_labels_with_numbered_and_bis_ter_variants',
    source_side_count_status: 'source_panels_far_exceed_local_side_count',
    frame700_candidate_visible: 'rough_short_mark_panels_visible_but_multiple_candidates',
    diagnostic_subtype_status: 'not_accepted_from_scan',
    side_order_status: 'unresolved_many_A_B_variant_labels_not_mapped_to_local_side_indices',
    copy_or_variant_risk: 'high_many_numbered_bis_ter_variants',
    source_coding_decision: 'visual_source_found_but_high_copy_variant_risk',
    decision_reason:
      'H-925 is a shared control, but the source page shows many variants; it cannot be used as a clean local control until one panel and copy-family status are resolved.',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: '2026-05-25',
    cisi: 'H-930',
    priority: 'core',
    packet_lane: 'local_contrast_stress',
    packet_role: 'control_032',
    packet_batch: 'local_893_925_930;local_2137_925_930',
    ia_volume: 'CISI Collections in Pakistan',
    ia_leafs_inspected: '374',
    page_kind: 'visual_plate_page',
    source_page_heading: 'HARAPPA 927-942 TABLETS incised no iconography',
    source_labels_visible: 'H-930 A; H-930 B',
    source_panel_count_observed: '2',
    local_metadata_sides: '2',
    local_frame700_row: '+700-032+',
    local_companion_row: '+740-900-004+',
    visual_object_identity_status: 'source_page_label_visible',
    source_side_label_status: 'A_B_labels_visible',
    source_side_count_status: 'source_panel_count_matches_local_side_count',
    frame700_candidate_visible: 'rough_short_mark_panel_visible_on_H-930_B',
    diagnostic_subtype_status: 'not_accepted_from_scan',
    side_order_status: 'unresolved_A_B_labels_not_mapped_to_local_side_indices',
    copy_or_variant_risk: 'low_on_page_no_bis_or_numbered_variant_for_object',
    source_coding_decision: 'visual_source_found_two_panel_object',
    decision_reason:
      'This is the cleanest IA page in the first local contrast triad: two labeled panels and no visible object variant, but subtype and direction remain unaccepted.',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: '2026-05-25',
    cisi: 'H-983',
    priority: 'core',
    packet_lane: 'local_contrast_stress',
    packet_role: 'target_034',
    packet_batch: 'local_983_353_2211',
    ia_volume: 'CISI Collections in Pakistan',
    ia_leafs_inspected: '377',
    page_kind: 'visual_plate_page',
    source_page_heading: 'HARAPPA 974-984 TABLETS incised gharial; fish; geom.',
    source_labels_visible: 'H-983 A; H-983 A bis; H-983 B; H-983 B bis; H-983 B ter; H-983 C; H-983 C bis',
    source_panel_count_observed: '7',
    local_metadata_sides: '2',
    local_frame700_row: '+700-034+',
    local_companion_row: '+400-740-637-240+',
    visual_object_identity_status: 'source_page_label_visible',
    source_side_label_status: 'A_B_C_labels_with_bis_ter_variants',
    source_side_count_status: 'source_panels_exceed_local_side_count',
    frame700_candidate_visible: 'rough_short_mark_panels_visible_but_multiple_candidates',
    diagnostic_subtype_status: 'not_accepted_from_scan',
    side_order_status: 'unresolved_A_B_C_variant_labels_not_mapped_to_local_side_indices',
    copy_or_variant_risk: 'high_multiple_B_and_C_variants',
    source_coding_decision: 'visual_source_found_but_variant_disambiguation_required',
    decision_reason:
      'The page confirms object-labeled panels, but local two-side coding suppresses a visible source C side and multiple B/C variants.',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: '2026-05-25',
    cisi: 'H-353',
    priority: 'core',
    packet_lane: 'local_contrast_stress',
    packet_role: 'control_033',
    packet_batch: 'local_983_353_2211',
    ia_volume: 'CISI Collections in India',
    ia_leafs_inspected: '265;696',
    page_kind: 'visual_plate_page_duplicate_locator_pair',
    source_page_heading: 'HARAPPA 345-354 TABLETS incised',
    source_labels_visible: 'H-353 A; H-353 B; H-353 C',
    source_panel_count_observed: '3',
    local_metadata_sides: '2',
    local_frame700_row: '+700-033+',
    local_companion_row: '+400-740-176+',
    visual_object_identity_status: 'source_page_label_visible',
    source_side_label_status: 'A_B_C_labels_visible',
    source_side_count_status: 'source_panel_count_exceeds_local_side_count',
    frame700_candidate_visible: 'rough_short_mark_panel_visible_on_H-353_B',
    diagnostic_subtype_status: 'not_accepted_from_scan',
    side_order_status: 'unresolved_A_B_C_labels_not_mapped_to_local_side_indices',
    copy_or_variant_risk: 'extra_C_side_or_iconographic_side_not_in_local_packet',
    source_coding_decision: 'visual_source_found_but_local_side_count_mismatch',
    decision_reason:
      'The source page shows three labeled panels while the local packet records two sides, so H-353 must be reconciled before it can serve as a clean control.',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: '2026-05-25',
    cisi: 'H-212',
    priority: 'core',
    packet_lane: 'local_contrast_stress',
    packet_role: 'control_032',
    packet_batch: 'local_1824_1883_212',
    ia_volume: 'CISI Collections in India',
    ia_leafs_inspected: '406;837',
    page_kind: 'data_register_page_duplicate_locator_pair',
    source_page_heading: 'DATA H-157 to H-321',
    source_labels_visible: 'H-212 register row only',
    source_panel_count_observed: '0',
    local_metadata_sides: '2',
    local_frame700_row: '+032-700+',
    local_companion_row: '+400-156-118+',
    visual_object_identity_status: 'register_row_visible_no_image_panel',
    source_side_label_status: 'register_cross_reference_only',
    source_side_count_status: 'not_available_from_page',
    frame700_candidate_visible: 'not_visible',
    diagnostic_subtype_status: 'not_available_from_register_page',
    side_order_status: 'not_available_from_register_page',
    copy_or_variant_risk: 'unknown_register_page_points_to_other_source_reference',
    source_coding_decision: 'data_locator_only_no_visual_validation',
    decision_reason:
      'The IA hit is a data/register page rather than a plate page. It can help route H-212 but fills no visual sign fields.',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: '2026-05-25',
    cisi: 'H-910',
    priority: 'optional',
    packet_lane: 'repeated_branch_check',
    packet_role: 'target_034',
    packet_batch: 'optional_910_916_1294',
    ia_volume: 'CISI Collections in Pakistan',
    ia_leafs_inspected: '372',
    page_kind: 'visual_plate_page',
    source_page_heading: 'HARAPPA 899-911 TABLETS incised no iconography',
    source_labels_visible: 'H-910 A; H-910 B',
    source_panel_count_observed: '2',
    local_metadata_sides: '2',
    local_frame700_row: '+700-034+',
    local_companion_row: '+002-861-416+',
    visual_object_identity_status: 'source_page_label_visible',
    source_side_label_status: 'A_B_labels_visible',
    source_side_count_status: 'source_panel_count_matches_local_side_count',
    frame700_candidate_visible: 'rough_short_mark_panel_visible_on_H-910_B',
    diagnostic_subtype_status: 'not_accepted_from_scan',
    side_order_status: 'unresolved_A_B_labels_not_mapped_to_local_side_indices',
    copy_or_variant_risk: 'high_context_repetition_pressure_from_packet_even_if_page_has_two_panels',
    source_coding_decision: 'optional_visual_source_found_repeated_branch_only',
    decision_reason:
      'The page gives a clean two-panel visual locator, but this object remains optional because the +002-861-416+ branch is repetition pressured.',
    accepted_decipherment_claim: '0',
  },
];

const visualRows = rows.filter((row) => row.page_kind.includes('visual_plate_page'));
const sideCountMismatches = rows.filter(
  (row) =>
    row.source_panel_count_observed !== '0' &&
    row.source_panel_count_observed !== row.local_metadata_sides,
);

const summary = {
  checked_date: '2026-05-25',
  question: 'What does the first manual visual pass over IA-located CISI pages establish?',
  inspected_objects: rows.length,
  core_objects: rows.filter((row) => row.priority === 'core').length,
  optional_objects: rows.filter((row) => row.priority === 'optional').length,
  visual_plate_objects: visualRows.length,
  data_register_only_objects: rows.filter((row) => row.page_kind.includes('data_register_page')).length,
  source_panel_count_matches_local_side_count: rows.filter(
    (row) => row.source_side_count_status === 'source_panel_count_matches_local_side_count',
  ).length,
  source_panel_count_exceeds_local_side_count: sideCountMismatches.length,
  high_or_variant_risk_objects: rows.filter(
    (row) => row.copy_or_variant_risk.includes('high') || row.copy_or_variant_risk.includes('variant'),
  ).length,
  source_coding_decision_counts: countBy(rows, 'source_coding_decision'),
  accepted_decipherment_claims: 0,
  immediate_consequence:
    'H-789, H-930, and optional H-910 have two labeled source panels matching local side count; H-771, H-893, H-925, H-983, and H-353 require side-count or variant reconciliation; H-212 is a register locator only.',
  source_boundary:
    'This visual pass confirms page/panel availability and reconciliation risks only. It does not accept 032/033/034 subtype readings, direction, side function, meaning, number, language, or translation.',
};

fs.writeFileSync(outCsv, toCsv(rows));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
