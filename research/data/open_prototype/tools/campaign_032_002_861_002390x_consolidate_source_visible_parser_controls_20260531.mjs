import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_consolidate_source_visible_parser_controls_20260531';
const checkedDate = '2026-05-31';

function csvEscape(value) {
  const text = String(value ?? '');
  return /[",\n\r]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(',')];
  for (const row of rows) lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

fs.mkdirSync(reportsDir, { recursive: true });

const visualBasis = [
  'tmp/002390x_source_normalization/campaign_032_002_861_002390x_source_normalized_contrast_contact_sheet.jpg',
  'tmp/002390x_token_boundary_readiness/campaign_032_002_861_002390x_token_boundary_readiness_contact_sheet.jpg',
];

const sourceRows = [
  {
    checked_date: checkedDate,
    object: 'M-119',
    branch: '002-390-125-632-032',
    lane: '125_linker',
    source_status: 'strict_source_visible_token_box_ready_high',
    site_scope: 'Mohenjo-daro',
    parser_effect: 'supports_125_linker_and_632032_complement_but_same_site_formula_risk',
    visual_basis: visualBasis.join(';'),
  },
  {
    checked_date: checkedDate,
    object: 'M-735',
    branch: '002-390-125-195',
    lane: '125_linker',
    source_status: 'strict_source_visible_token_box_ready_high',
    site_scope: 'Mohenjo-daro',
    parser_effect: 'supports_125_linker_but_195_is_singleton_complement',
    visual_basis: visualBasis.join(';'),
  },
  {
    checked_date: checkedDate,
    object: 'Sktd-1',
    branch: '002-390-125-820',
    lane: '125_linker',
    source_status: 'panel_bound_token_box_ready_medium_downweighted',
    site_scope: 'Surkotada',
    parser_effect: 'cross_site_pressure_for_125_820_but_not_strict',
    visual_basis: visualBasis.join(';'),
  },
  {
    checked_date: checkedDate,
    object: 'M-38',
    branch: '002-390-125-632-032',
    lane: '125_linker',
    source_status: 'not_ready_weak_context_not_token_boxable',
    site_scope: 'Mohenjo-daro',
    parser_effect: 'do_not_count_for_strict_125_or_632032',
    visual_basis: visualBasis.join(';'),
  },
  {
    checked_date: checkedDate,
    object: 'M-71',
    branch: '002-390-095',
    lane: '095_terminal_classifier',
    source_status: 'strict_source_visible_token_box_ready_high',
    site_scope: 'Mohenjo-daro',
    parser_effect: 'single_strict_source_visible_095_terminal_classifier_witness',
    visual_basis: visualBasis.join(';'),
  },
  {
    checked_date: checkedDate,
    object: 'H-1993',
    branch: '002-390-095',
    lane: '095_terminal_classifier',
    source_status: 'public_transcription_route_no_image_binding',
    site_scope: 'Harappa',
    parser_effect: 'route_pressure_only_not_strict_source_visible',
    visual_basis: 'Singh_ESM2_public_transcription_route; no image in inspected local packet',
  },
  {
    checked_date: checkedDate,
    object: 'M-70',
    branch: '002-390-692',
    lane: '692_global_edge_close',
    source_status: 'strict_source_visible_token_box_ready_high',
    site_scope: 'Mohenjo-daro',
    parser_effect: 'strict non-125 terminal comparator but not 095_705_classifier support',
    visual_basis: visualBasis.join(';'),
  },
  {
    checked_date: checkedDate,
    object: 'M-1825',
    branch: '002-390-705',
    lane: '705_terminal_classifier',
    source_status: 'no_signband_no_strict_source_visible',
    site_scope: 'Mohenjo-daro',
    parser_effect: 'structural_705_only_no_strict_classifier_support',
    visual_basis: 'local/source packet search no signband binding',
  },
  {
    checked_date: checkedDate,
    object: '4237.1',
    branch: '002-390-705',
    lane: '705_terminal_classifier',
    source_status: 'source_image_candidate_unbound_metadata_cluster_found',
    site_scope: 'Dholavira',
    parser_effect: '705_acquisition_hot_but_not_strict',
    visual_basis: 'Dholavira page/item and ZA-12:2 route unbound to metadata row',
  },
  {
    checked_date: checkedDate,
    object: 'M-1668',
    branch: '002-320-705-125',
    lane: '705_nonterminal_exception',
    source_status: 'no_new_strict_classifier_chain_support',
    site_scope: 'Mohenjo-daro',
    parser_effect: '705125_chain_killed_as_general_rule_singleton_exception',
    visual_basis: 'structural singleton; no classifier-chain promotion',
  },
];

const laneRows = [
  {
    checked_date: checkedDate,
    lane: '125_linker',
    strict_witnesses: 'M-119;M-735',
    medium_or_pressure: 'Sktd-1',
    excluded: 'M-38',
    consolidated_status: 'candidate_wounded_source_visible',
    consequence: '125 is stronger than pure structural bet, but exact repeated complement remains site-local.',
  },
  {
    checked_date: checkedDate,
    lane: '095_terminal_classifier',
    strict_witnesses: 'M-71',
    medium_or_pressure: 'H-1993_route_only',
    excluded: '',
    consolidated_status: 'wild_shot_source_visible_singleton',
    consequence: '095 is source-visible once, not enough for candidate sign meaning.',
  },
  {
    checked_date: checkedDate,
    lane: '705_terminal_classifier',
    strict_witnesses: '',
    medium_or_pressure: 'M-1825_structural;4237.1_unbound_hot',
    excluded: 'M-1668_as_general_chain',
    consolidated_status: 'wild_shot_structural_only_source_blocked',
    consequence: '705 should be split from 095 in the ranking until a source image binds it.',
  },
  {
    checked_date: checkedDate,
    lane: '692_global_edge_close',
    strict_witnesses: 'M-70',
    medium_or_pressure: '',
    excluded: '',
    consolidated_status: 'strict_comparator_not_classifier_core',
    consequence: '692 supports non-125 terminal comparator behavior but not overt classifier semantics.',
  },
];

const decisionRows = [
  {
    checked_date: checkedDate,
    claim: '125_linker',
    old_status: 'candidate_wounded',
    new_status: 'candidate_wounded_source_visible',
    reason: 'M-119 and M-735 are strict token-box-ready witnesses; Sktd-1 adds downweighted cross-site pressure.',
  },
  {
    checked_date: checkedDate,
    claim: '095_705_classifiers',
    old_status: 'wild_shot_strengthened_combined',
    new_status: 'split_095_singleton_source_visible_705_structural_only',
    reason: 'M-71 gives one strict 095 witness; 705 has no strict source-visible witness yet.',
  },
  {
    checked_date: checkedDate,
    claim: 'source_visible_translation',
    old_status: 'none',
    new_status: 'blocked',
    reason: 'Strict witnesses support parse roles only, not sign values, phonetics, language identity, or translation.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: 'source_visible_parser_controls',
  source_visible_effect:
    '125 gets strict source-visible support; 095 gets one strict source-visible witness; 705 remains source-blocked.',
  accepted_claims: 0,
  parser_update:
    'split 095 and 705 ranking; keep 125 as source-visible wounded candidate; keep classifier meanings below candidate.',
};

writeCsv(path.join(reportsDir, `${prefix}_source_rows.csv`), sourceRows, [
  'checked_date',
  'object',
  'branch',
  'lane',
  'source_status',
  'site_scope',
  'parser_effect',
  'visual_basis',
]);
writeCsv(path.join(reportsDir, `${prefix}_lane_rows.csv`), laneRows, [
  'checked_date',
  'lane',
  'strict_witnesses',
  'medium_or_pressure',
  'excluded',
  'consolidated_status',
  'consequence',
]);
writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisionRows, [
  'checked_date',
  'claim',
  'old_status',
  'new_status',
  'reason',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
