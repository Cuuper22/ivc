import fs from 'node:fs';
import path from 'node:path';

// This script records the outcome of trying to reconcile the five "messy" objects -- H-771,
// H-893, H-925, H-983, and H-353 -- against their CISI page scans, using the clean two-panel
// objects H-930 and H-789 as the standard to meet. Each hard-coded row lists the panel
// labels actually visible on the scan, the observed panel count versus the local metadata's
// two sides, which panel could plausibly carry the short frame700 row, and exactly why the
// mapping is blocked (four A photographs for one companion row, numbered variants like
// H-893 (1), an extra C side, and so on). The script tallies these into a JSON summary and
// writes the rows as a CSV. The result is deliberately negative: all five objects fail the
// clean standard, so none of them can yet anchor the 034 substitution test. Preserving that
// failure, with reasons, is the point.

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const outCsv = path.join(reportsDir, 'lipi_frame700_034_messy_panel_reconciliation.csv');
const outJson = path.join(
  reportsDir,
  'lipi_frame700_034_messy_panel_reconciliation_summary.json',
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
    cisi: 'H-771',
    priority: 'core',
    packet_lane: 'independent_low_copy',
    packet_role: 'target_034',
    packet_batch: 'independent_771_789_1123',
    ia_volume: 'CISI Collections in Pakistan',
    ia_leafs_inspected: '358',
    source_page_heading: 'HARAPPA 768-777 TABLETS in bas-relief no iconography',
    local_frame700_row: '+700-034+',
    local_companion_row: '+032-257-840+',
    local_metadata_sides: '2',
    source_labels_visible: 'H-771 A; H-771 A bis; H-771 A ter; H-771 A quater; H-771 B',
    source_panel_count_observed: '5',
    source_count_vs_local: 'visible_photo_labels_exceed_local_side_count',
    short_candidate_label: 'H-771 B',
    short_candidate_visibility: 'single_B_short_candidate_visible',
    long_or_companion_candidate_labels: 'H-771 A; H-771 A bis; H-771 A ter; H-771 A quater',
    extra_panel_or_variant_labels: 'H-771 A bis; H-771 A ter; H-771 A quater',
    companion_mapping_status:
      'blocked_by_four_A_photographs_for_one_local_companion_row',
    variant_failure_mode: 'multiple_A_photographs_plus_B',
    meets_clean_H930_H789_standard: '0',
    source_research_decision:
      'partial_short_candidate_visible_but_failed_clean_two_panel_standard',
    close_read_observation:
      'The printed B panel is a plausible short-side candidate for the local +700-034+ row, but the source page also shows four A-labeled photographs where the local packet has one companion row.',
    next_action:
      'request or inspect catalog notes that explain A/A bis/A ter/A quater before pairing H-771 against H-789 or H-1123',
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
    source_page_heading: 'HARAPPA 886-898 TABLETS incised no iconography',
    local_frame700_row: '+700-034+',
    local_companion_row: '+400-740-337+',
    local_metadata_sides: '2',
    source_labels_visible: 'H-893 A; H-893 B; H-893 (1) A; H-893 (1) B',
    source_panel_count_observed: '4',
    source_count_vs_local: 'visible_photo_labels_exceed_local_side_count',
    short_candidate_label: 'H-893 B or H-893 (1) B',
    short_candidate_visibility: 'multiple_B_candidates_visible',
    long_or_companion_candidate_labels: 'H-893 A; H-893 (1) A',
    extra_panel_or_variant_labels: 'H-893 (1) A; H-893 (1) B',
    companion_mapping_status: 'blocked_by_numbered_variant_for_same_H_number',
    variant_failure_mode: 'base_AB_plus_numbered_variant_AB',
    meets_clean_H930_H789_standard: '0',
    source_research_decision:
      'failed_clean_standard_numbered_variant_blocks_strict_local_target',
    close_read_observation:
      'The page visibly separates base H-893 A/B from H-893 (1) A/B. That is enough to confirm object-label visibility, but not enough to choose which B-like panel corresponds to the local +700-034+ row.',
    next_action:
      'reconcile base versus numbered H-893 variant against CISI notes before using H-893 as a strict local 034 target against H-925/H-930',
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
    source_page_heading: 'HARAPPA 912-920 TABLETS incised no iconography',
    local_frame700_row: '+700-033+',
    local_companion_row: '+740-840-013+',
    local_metadata_sides: '2',
    source_labels_visible:
      'H-925 A; H-925 B; H-925 (1) A; H-925 (2) A; H-925 (2) B; H-925 (1) B; H-925 A bis; H-925 B bis; H-925 A ter',
    source_panel_count_observed: '9',
    source_count_vs_local: 'visible_photo_labels_far_exceed_local_side_count',
    short_candidate_label: 'multiple_B_labeled_H-925_candidates',
    short_candidate_visibility: 'multiple_B_candidates_visible',
    long_or_companion_candidate_labels:
      'H-925 A; H-925 (1) A; H-925 (2) A; H-925 A bis; H-925 A ter',
    extra_panel_or_variant_labels:
      'H-925 (1) A; H-925 (2) A; H-925 (2) B; H-925 (1) B; H-925 A bis; H-925 B bis; H-925 A ter',
    companion_mapping_status: 'blocked_by_many_numbered_bis_and_ter_variants',
    variant_failure_mode: 'high_copy_variant_pressure_on_shared_control',
    meets_clean_H930_H789_standard: '0',
    source_research_decision:
      'failed_clean_standard_shared_control_variant_soup',
    close_read_observation:
      'H-925 is too crowded to inherit H-930 control confidence. The source page shows many A/B variants, so the local +700-033+ control row cannot be attached to one source panel yet.',
    next_action:
      'treat H-925 as a high-risk shared control until CISI notes identify the base object, numbered objects, and bis/ter copy status',
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
    source_page_heading: 'HARAPPA 974-984 TABLETS incised gharial; fish; geom.',
    local_frame700_row: '+700-034+',
    local_companion_row: '+400-740-637-240+',
    local_metadata_sides: '2',
    source_labels_visible:
      'H-983 A; H-983 A bis; H-983 B; H-983 B bis; H-983 B ter; H-983 C; H-983 C bis',
    source_panel_count_observed: '7',
    source_count_vs_local: 'visible_photo_labels_exceed_local_side_count',
    short_candidate_label: 'multiple_B_labeled_H-983_candidates',
    short_candidate_visibility: 'multiple_B_candidates_visible',
    long_or_companion_candidate_labels: 'H-983 A; H-983 A bis; H-983 C; H-983 C bis',
    extra_panel_or_variant_labels: 'H-983 A bis; H-983 B bis; H-983 B ter; H-983 C; H-983 C bis',
    companion_mapping_status:
      'blocked_by_A_B_C_panel_set_and_multiple_B_C_variants',
    variant_failure_mode: 'extra_C_side_plus_bis_ter_variants',
    meets_clean_H930_H789_standard: '0',
    source_research_decision:
      'failed_clean_standard_extra_C_and_B_variants',
    close_read_observation:
      'The local packet records two sides, but the source page shows A, B, and C panels with bis/ter variants. The visible C side means the local packet is incomplete at source level.',
    next_action:
      'reconcile the suppressed C side and B variants before using H-983 against H-353/H-2211',
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
    source_page_heading: 'HARAPPA 345-354 TABLETS incised',
    local_frame700_row: '+700-033+',
    local_companion_row: '+400-740-176+',
    local_metadata_sides: '2',
    source_labels_visible: 'H-353 A; H-353 B; H-353 C',
    source_panel_count_observed: '3',
    source_count_vs_local: 'visible_side_labels_exceed_local_side_count',
    short_candidate_label: 'H-353 B',
    short_candidate_visibility: 'single_B_short_candidate_visible',
    long_or_companion_candidate_labels: 'H-353 A',
    extra_panel_or_variant_labels: 'H-353 C',
    companion_mapping_status: 'blocked_by_extra_C_panel_not_in_local_two_side_packet',
    variant_failure_mode: 'three_source_panels_for_two_local_sides',
    meets_clean_H930_H789_standard: '0',
    source_research_decision:
      'failed_clean_standard_source_three_panels',
    close_read_observation:
      'The printed B panel is a plausible short-side candidate for the local +700-033+ row, and printed A is a plausible longer companion candidate. The printed C panel is not represented in the local two-side packet and blocks clean-control use.',
    next_action:
      'reconcile H-353 C and duplicate India leaf locators before using H-353 as the 033 control for H-983',
    accepted_decipherment_claim: '0',
  },
];

const summary = {
  checked_date: '2026-05-25',
  artifact: 'lipi_frame700_034_messy_panel_reconciliation',
  source_scope:
    'manual close-read of IA CISI page images for the messy H-771/H-893/H-925/H-983/H-353 source-gate objects',
  input_objects: rows.length,
  messy_reconciliation_rows: rows.length,
  objects_meeting_clean_H930_H789_standard: rows.filter(
    (row) => row.meets_clean_H930_H789_standard !== '0',
  ).length,
  visible_photo_or_side_label_count_exceeds_local_side_count: rows.filter((row) =>
    row.source_count_vs_local.includes('exceed'),
  ).length,
  variant_or_extra_side_failures: rows.filter(
    (row) => row.variant_failure_mode !== '',
  ).length,
  single_B_short_candidate_visible: rows.filter(
    (row) => row.short_candidate_visibility === 'single_B_short_candidate_visible',
  ).length,
  multiple_B_candidates_visible: rows.filter(
    (row) => row.short_candidate_visibility === 'multiple_B_candidates_visible',
  ).length,
  duplicate_locator_pairs_reconciled_as_same_visual_page: 1,
  clean_standard_counts: countBy(rows, 'meets_clean_H930_H789_standard'),
  failure_mode_counts: countBy(rows, 'variant_failure_mode'),
  decision_counts: countBy(rows, 'source_research_decision'),
  accepted_decipherment_claims: rows.filter((row) => row.accepted_decipherment_claim !== '0')
    .length,
  upgraded_evidence:
    'None of the five messy objects is upgraded to clean source-control status.',
  negative_result:
    'Every checked object fails because the source page exposes extra photo labels, extra side categories, unresolved numbered labels, or same-side bis/ter/quater photographs where the local packet has two rows.',
  immediate_research_consequence:
    'H-771, H-893, H-925, H-983, and H-353 cannot inherit the H-930/H-789 calibration upgrade. The 034 residue remains live but source-unvalidated for these lanes.',
};

fs.mkdirSync(reportsDir, { recursive: true });
fs.writeFileSync(outCsv, toCsv(rows));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
