import fs from 'node:fs';
import path from 'node:path';

// Two records in one script, both hand-written from a 2026-05-25 search of the accessible
// Internet Archive OCR of CISI volumes 1 and 2. First, the note-route rows: for each blocked
// object (H-771, H-893, H-925, H-983, H-353) they document that the OCR shows the plate
// labels but contains no object-specific catalogue note explaining them, and that the
// volumes route such notes to the CISI volume 3 detailed catalogue -- so that becomes the
// retrieval target. Second, the panel-graph rows: for all nine objects across the three
// study lanes they state the local two-row signature, the source-side node set after
// applying CISI labeling conventions, the exact blocker type, and a substitution-readiness
// verdict. The script tallies lane readiness (result: zero lanes ready) and writes two CSVs
// plus a JSON summary. It exists to convert a failed note search into precise next source
// requests instead of another blind OCR pass.

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const outNoteCsv = path.join(reportsDir, 'lipi_frame700_034_source_note_route_probe.csv');
const outGraphCsv = path.join(reportsDir, 'lipi_frame700_034_panel_graph_readiness.csv');
const outJson = path.join(
  reportsDir,
  'lipi_frame700_034_source_note_panel_graph_summary.json',
);

function toCsv(rows) {
  if (rows.length === 0) return '';
  const header = Object.keys(rows[0]);
  const lines = rows.map((row) =>
    header
      .map((key) => {
        const text = String(row[key] ?? '');
        return `"${text.replaceAll('"', '""')}"`;
      })
      .join(','),
  );
  return `${[header.map((key) => `"${key}"`).join(','), ...lines].join('\n')}\n`;
}

function countBy(rows, key) {
  const counts = new Map();
  for (const row of rows) counts.set(row[key], (counts.get(row[key]) ?? 0) + 1);
  return Object.fromEntries(
    [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])),
  );
}

const checkedDate = '2026-05-25';

const noteRouteRows = [
  {
    checked_date: checkedDate,
    row_type: 'source_route',
    scope_or_object: 'CISI_vol2_Pakistan_detailed_catalogue_route',
    ia_volume: 'CISI Collections in Pakistan',
    ocr_locator: 'Pakistan OCR table of contents line 346; introduction lines 2099-2102',
    query_terms_checked: 'Basic data; detailed catalogue; measures; material; manufacture; text; iconography; references',
    accessible_ia_ocr_result:
      'The accessible volume points detailed object catalogue work to volume 3 and later detailed catalogue material; it does not itself carry the target object notes needed here.',
    plate_label_hits_found: 'not_target_specific',
    object_specific_note_found: 'no',
    route_decision:
      'Use CISI vol. 3/detailed catalogue, library scan, archive copy, or object-level HARP/CISI plate notes for numbered-label and side-policy resolution.',
    impact_on_034_experiment:
      'Do not infer H-893/H-925 numbered-label meaning or H-983 side policy from vol. 2 plate labels alone.',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: checkedDate,
    row_type: 'source_route',
    scope_or_object: 'CISI_vol1_India_detailed_catalogue_route',
    ia_volume: 'CISI Collections in India',
    ocr_locator: 'India OCR table of contents line 307; introduction lines 1621-1623',
    query_terms_checked: 'Basic data; detailed catalogue; excavation number; museum number',
    accessible_ia_ocr_result:
      'The accessible India volume likewise routes detailed object documentation to a third-volume/detailed-catalogue layer.',
    plate_label_hits_found: 'not_target_specific',
    object_specific_note_found: 'no',
    route_decision:
      'Use CISI vol. 3/detailed catalogue or equivalent archive source before deciding why H-353 C is omitted locally.',
    impact_on_034_experiment:
      'H-353 cannot be treated as a clean two-side 033 control until the C side policy is explained.',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: checkedDate,
    row_type: 'bibliographic_route',
    scope_or_object: 'CISI_vol3_1_back_matter_route',
    ia_volume: 'CISI 3.1 Mohenjo-daro and Harappa',
    ocr_locator:
      'Book Notices record for CISI vol. 3.1; Harappa.com and University of Helsinki bibliographic pages',
    query_terms_checked:
      'CISI 3.1; data on each object; excavation number; museum or owner; source of photograph; pp. 413-443',
    accessible_ia_ocr_result:
      'Not an IA OCR result. External bibliographic route check points to CISI 3.1 back matter as the next manual lookup layer for object data.',
    plate_label_hits_found: 'not_applicable',
    object_specific_note_found: 'route_only',
    route_decision:
      'Manually inspect CISI 3.1 back matter and Harappa object data sections before deciding whether numbered labels or omitted C sides are source/copy/policy artifacts.',
    impact_on_034_experiment:
      'Turns the failed IA OCR note search into a concrete source retrieval target instead of another blind OCR pass.',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: checkedDate,
    row_type: 'target_note_probe',
    scope_or_object: 'H-771',
    ia_volume: 'CISI Collections in Pakistan',
    ocr_locator: 'Pakistan OCR target region around lines 15990-16050; IA reader leaf n358',
    query_terms_checked: 'H-771; 657678; A bis; A ter; A quater; B',
    accessible_ia_ocr_result:
      'Plate-label evidence is enough to see A/A bis/A ter/A quater plus B, but no target note in the accessible OCR explains which A photograph should anchor the local row.',
    plate_label_hits_found: 'yes',
    object_specific_note_found: 'no',
    route_decision:
      'Keep H-771 graphable only as side A with multiple photo witnesses plus side B; request catalogue/image notes for photo selection and preservation state.',
    impact_on_034_experiment:
      'The physical side-count objection is narrowed, but H-771 is still not substitution-ready.',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: checkedDate,
    row_type: 'target_note_probe',
    scope_or_object: 'H-893',
    ia_volume: 'CISI Collections in Pakistan',
    ocr_locator: 'Pakistan OCR lines 16804, 16808, 16823, and 16826; IA reader leaf n371',
    query_terms_checked: 'H-893; H-893 (1); 12581522; base A/B; numbered A/B',
    accessible_ia_ocr_result:
      'The OCR finds plate labels for base H-893 A/B and H-893 (1) A/B, but no note identifying whether (1) is a copy, sub-entry, second object, or alternate photograph group.',
    plate_label_hits_found: 'yes',
    object_specific_note_found: 'no',
    route_decision:
      'Do not attach local +700-034+ to a source side until H-893 versus H-893 (1) is resolved from catalogue notes or source plates.',
    impact_on_034_experiment:
      'The H-893/H-925/H-930 strict lane is blocked before any 034/033/032 comparison.',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: checkedDate,
    row_type: 'target_note_probe',
    scope_or_object: 'H-925',
    ia_volume: 'CISI Collections in Pakistan',
    ocr_locator: 'Pakistan OCR lines 16990, 16994, 17002, 17005, and 17008; IA reader leaf n373',
    query_terms_checked: 'H-925; H-925 (1); H-925 (2); 3286512; A bis; B bis; A ter',
    accessible_ia_ocr_result:
      'The OCR finds base, numbered, bis, and ter plate labels, but no note explaining the numbered groups before side letters.',
    plate_label_hits_found: 'yes',
    object_specific_note_found: 'no',
    route_decision:
      'Treat H-925 as a high-risk shared control until numbered groups and same-side photo witnesses are separated.',
    impact_on_034_experiment:
      'H-925 cannot serve as the clean 033 contrast for either H-893 or H-2137 yet.',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: checkedDate,
    row_type: 'target_note_probe',
    scope_or_object: 'H-983',
    ia_volume: 'CISI Collections in Pakistan',
    ocr_locator: 'Pakistan OCR around line 17446; IA reader leaf n377',
    query_terms_checked: 'H-983; 2528582; A; B; C; C bis',
    accessible_ia_ocr_result:
      'The OCR is garbled but confirms the target plate-label area, including H-983 B and C/C bis context; it does not explain why the local packet has only two sides.',
    plate_label_hits_found: 'yes_garbled',
    object_specific_note_found: 'no',
    route_decision:
      'Keep C as a real source-side hazard under CISI convention until a catalogue note proves it is non-comparable or intentionally excluded.',
    impact_on_034_experiment:
      'The H-983/H-353/H-2211 visual lane is blocked by source side-count mismatch.',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: checkedDate,
    row_type: 'target_note_probe',
    scope_or_object: 'H-353',
    ia_volume: 'CISI Collections in India',
    ocr_locator: 'India OCR lines 8412, 8437, 26968, and 26993; IA reader leaves n265/n696',
    query_terms_checked: 'H-353; 1348; A; B; C; duplicate IA leaves',
    accessible_ia_ocr_result:
      'The OCR confirms duplicate B/C label contexts on two IA leaves; prior visual inspection saw the A/B/C page. No accessible OCR note explains why local rows omit C.',
    plate_label_hits_found: 'yes_duplicate_context',
    object_specific_note_found: 'no',
    route_decision:
      'Route to CISI detailed catalogue or source plate policy notes before using H-353 as a two-side 033 control.',
    impact_on_034_experiment:
      'H-353 remains blocked because C may be inscriptional, iconographic, or otherwise policy-excluded, and that distinction matters.',
    accepted_decipherment_claim: '0',
  },
];

const panelGraphRows = [
  {
    checked_date: checkedDate,
    lane: 'independent_low_copy_H771_H789_H1123',
    object: 'H-771',
    role: '034_target',
    local_packet_signature: '1:+032-257-840+|2:+700-034+',
    source_nodes_after_convention: 'side_A{A,A_bis,A_ter,A_quater};side_B{B}',
    clean_calibration_status: 'not_clean_target',
    graph_blocker_type: 'same_side_photo_selection',
    graph_blocker_detail:
      'Need to choose which A photograph anchors the companion row and verify B maps to local +700-034+ under source direction and subtype uncertainty.',
    immediate_source_action: 'Get object/caption/catalogue note plus higher-quality plate for A/A bis/A ter/A quater/B.',
    substitution_readiness: 'blocked',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: checkedDate,
    lane: 'independent_low_copy_H771_H789_H1123',
    object: 'H-789',
    role: '033_control',
    local_packet_signature: '1:+400-520-220-016+|2:+033-700+',
    source_nodes_after_convention: 'side_A{A};side_B{B}',
    clean_calibration_status: 'clean_two_panel_calibration_control',
    graph_blocker_type: 'subtype_direction_unaccepted',
    graph_blocker_detail:
      'Clean enough for object identity, panel count, and short-versus-long split; not enough to independently validate 033 subtype or direction.',
    immediate_source_action: 'Use only as a close-read calibration control until paired objects pass source gates.',
    substitution_readiness: 'control_only_not_lane_ready',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: checkedDate,
    lane: 'independent_low_copy_H771_H789_H1123',
    object: 'H-1123',
    role: '032_control',
    local_packet_signature: '1:+525-550-220+|2:+700-032+',
    source_nodes_after_convention: 'not_located_in_checked_IA_CISI_vol1_2_OCR',
    clean_calibration_status: 'source_absent',
    graph_blocker_type: 'source_request_only',
    graph_blocker_detail:
      'The 032 comparator for this lane is not yet page-addressable from the checked IA OCR layer.',
    immediate_source_action: 'Request CISI/HARP/archive source plate or locate via detailed catalogue.',
    substitution_readiness: 'blocked',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: checkedDate,
    lane: 'strict_local_H893_H925_H930',
    object: 'H-893',
    role: '034_target',
    local_packet_signature: '1:+400-740-337+|2:+700-034+',
    source_nodes_after_convention: 'base_side_A/B plus unresolved H-893_(1)_side_A/B',
    clean_calibration_status: 'not_clean_target',
    graph_blocker_type: 'unresolved_object_number_group',
    graph_blocker_detail:
      'Cannot know whether local rows map to base H-893, H-893 (1), or some catalogue sub-entry without source notes.',
    immediate_source_action: 'Resolve H-893 (1) A/B in CISI detailed catalogue or original plate/caption notes.',
    substitution_readiness: 'blocked',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: checkedDate,
    lane: 'strict_local_H893_H925_H930',
    object: 'H-925',
    role: '033_control',
    local_packet_signature: '1:+740-840-013+|2:+700-033+',
    source_nodes_after_convention: 'base_A/B;H-925_(1)_B;H-925_(2)_A/B;A_bis;B_bis;A_ter',
    clean_calibration_status: 'not_clean_control',
    graph_blocker_type: 'unresolved_numbered_groups_plus_photo_witnesses',
    graph_blocker_detail:
      'Shared 033 control mixes base, numbered, bis, and ter labels; using it would contaminate every strict-lane comparison.',
    immediate_source_action: 'Separate physical object/sub-entry, side, and photo-witness layers from detailed notes.',
    substitution_readiness: 'blocked',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: checkedDate,
    lane: 'strict_local_H893_H925_H930',
    object: 'H-930',
    role: '032_control',
    local_packet_signature: '1:+740-900-004+|2:+700-032+',
    source_nodes_after_convention: 'side_A{A};side_B{B}',
    clean_calibration_status: 'clean_two_panel_calibration_control',
    graph_blocker_type: 'subtype_direction_unaccepted',
    graph_blocker_detail:
      'Clean enough for panel-count calibration; not enough to independently validate 032 subtype, direction, function, or value.',
    immediate_source_action: 'Use as calibration only after H-893/H-925 stop being graph-blocked.',
    substitution_readiness: 'control_only_not_lane_ready',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: checkedDate,
    lane: 'visual_local_H983_H353_H2211',
    object: 'H-983',
    role: '034_target',
    local_packet_signature: '1:+400-740-637-240+|2:+700-034+',
    source_nodes_after_convention: 'side_A{A,A_bis};side_B{B,B_bis,B_ter};side_C{C,C_bis}',
    clean_calibration_status: 'not_clean_target',
    graph_blocker_type: 'true_c_side_source_hazard',
    graph_blocker_detail:
      'C is a source side category under CISI convention, not merely an extra photo; local two-row packet is incomplete unless C is policy-excluded.',
    immediate_source_action: 'Find C-side note or source-policy explanation before comparing to H-353/H-2211.',
    substitution_readiness: 'blocked',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: checkedDate,
    lane: 'visual_local_H983_H353_H2211',
    object: 'H-353',
    role: '033_control',
    local_packet_signature: '1:+400-740-176+|2:+700-033+',
    source_nodes_after_convention: 'side_A{A};side_B{B};side_C{C};IA_leaf_duplicate{n265,n696}',
    clean_calibration_status: 'not_clean_control',
    graph_blocker_type: 'true_c_side_source_hazard',
    graph_blocker_detail:
      'C is visible as a side category in the source page, while local metadata supplies two rows; duplicate IA leaves do not solve the C-side policy problem.',
    immediate_source_action: 'Resolve whether H-353 C is inscriptional, iconographic, blank/edge, or excluded by a documented corpus policy.',
    substitution_readiness: 'blocked',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: checkedDate,
    lane: 'visual_local_H983_H353_H2211',
    object: 'H-2211',
    role: '032_control',
    local_packet_signature: '1:+700-032+|2:+700-840-032-741+',
    source_nodes_after_convention: 'CISI_3_1_or_archive_route_not_resolved_in_current_IA_probe',
    clean_calibration_status: 'source_route_pending',
    graph_blocker_type: 'source_route_pending',
    graph_blocker_detail:
      'The 032 comparator for this lane is not yet reconciled to a source-normalized side graph in the current IA vol.1/2 route.',
    immediate_source_action: 'Locate source plate and side labels before letting this lane enter a substitution test.',
    substitution_readiness: 'blocked',
    accepted_decipherment_claim: '0',
  },
];

const laneRows = panelGraphRows.filter((row) => row.role.endsWith('target'));
const lanes = [...new Set(panelGraphRows.map((row) => row.lane))];
const laneReadiness = Object.fromEntries(
  lanes.map((lane) => {
    const rows = panelGraphRows.filter((row) => row.lane === lane);
    const ready = rows.every((row) => row.substitution_readiness === 'ready');
    return [lane, ready ? 'ready' : 'blocked'];
  }),
);

const summary = {
  checked_date: checkedDate,
  artifact: 'lipi_frame700_034_source_note_panel_graph',
  note_route_rows: noteRouteRows.length,
  panel_graph_rows: panelGraphRows.length,
  lanes: lanes.length,
  lane_readiness: laneReadiness,
  strict_substitution_ready_lanes: Object.values(laneReadiness).filter((value) => value === 'ready')
    .length,
  target_034_rows_graph_blocked: laneRows.filter((row) => row.substitution_readiness !== 'ready')
    .length,
  object_specific_notes_found_in_accessible_ia_ocr: noteRouteRows.filter(
    (row) => row.object_specific_note_found === 'yes',
  ).length,
  plate_label_hits_found: noteRouteRows.filter((row) => row.plate_label_hits_found.startsWith('yes'))
    .length,
  detailed_catalogue_route_rows: noteRouteRows.filter((row) => row.row_type === 'source_route')
    .length,
  bibliographic_route_rows: noteRouteRows.filter((row) => row.row_type === 'bibliographic_route')
    .length,
  clean_calibration_controls: panelGraphRows.filter((row) =>
    row.clean_calibration_status.includes('clean_two_panel'),
  ).length,
  blocker_counts: countBy(panelGraphRows, 'graph_blocker_type'),
  accepted_decipherment_claims:
    noteRouteRows.filter((row) => row.accepted_decipherment_claim !== '0').length +
    panelGraphRows.filter((row) => row.accepted_decipherment_claim !== '0').length,
  research_conclusion:
    'Accessible IA CISI vol.1/2 OCR yields plate-label targets but zero object-specific notes for the live blockers. The source-normalized graph has 0 substitution-ready lanes; it creates the next source requests rather than a reading.',
};

fs.mkdirSync(reportsDir, { recursive: true });
fs.writeFileSync(outNoteCsv, toCsv(noteRouteRows), 'utf8');
fs.writeFileSync(outGraphCsv, toCsv(panelGraphRows), 'utf8');
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
