import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const outCsv = path.join(reportsDir, 'lipi_frame700_034_cisi_variant_convention_probe.csv');
const outJson = path.join(
  reportsDir,
  'lipi_frame700_034_cisi_variant_convention_probe_summary.json',
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

const conventionRows = [
  {
    checked_date: '2026-05-25',
    row_type: 'source_convention',
    cisi_or_scope: 'CISI_vol1_and_vol2_original_vs_impression',
    source_volume: 'CISI Collections in India; CISI Collections in Pakistan',
    source_locator:
      'India OCR lines 1409-1442; Pakistan OCR lines 1857-1889; IA bundle metadata and djvu text',
    source_url:
      'https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan',
    convention_applied:
      'original_and_impression_complement_each_other;original_remains_authority;do_not_replace_bad_impression_by_reversed_original_print',
    reconciled_component:
      'direction and visual sign form cannot be inferred by silently reversing or normalizing source photographs',
    still_unresolved:
      'target objects still need direct panel-to-local-row mapping from source photographs or notes',
    effect_on_034_packet:
      'blocks direction normalization and subtype reading from current IA scans',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: '2026-05-25',
    row_type: 'source_convention',
    cisi_or_scope: 'CISI_side_letters',
    source_volume: 'CISI Collections in India; CISI Collections in Pakistan',
    source_locator:
      'India OCR lines 1476-1499; Pakistan OCR lines 1934-1958; IA bundle metadata and djvu text',
    source_url:
      'https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan',
    convention_applied:
      'capital_letters_normally_mark_sides_A_obverse_B_reverse_C_upper_D_right_E_lower_F_left;three_sided_prisms_use_A_B_C_for_principal_rectangular_sides',
    reconciled_component:
      'A/B/C labels are side labels under normal CISI convention, not arbitrary catalog row names',
    still_unresolved:
      'object-specific type and physical side mapping must still be checked before side function is accepted',
    effect_on_034_packet:
      'C labels on H-983 and H-353 are source-side hazards, not harmless text variants',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: '2026-05-25',
    row_type: 'source_convention',
    cisi_or_scope: 'CISI_multiple_photos_same_side',
    source_volume: 'CISI Collections in India; CISI Collections in Pakistan',
    source_locator:
      'India OCR lines 1506-1536; Pakistan OCR lines 1964-1973; IA bundle metadata and djvu text',
    source_url:
      'https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan',
    convention_applied:
      'bis_ter_quater_quinquies_mark_second_third_fourth_fifth_photographs_of_same_side;usually_temporal_order_oldest_to_latest',
    reconciled_component:
      'bis/ter/quater labels should be treated as multiple photographs of a side, not automatically as extra physical sides',
    still_unresolved:
      'which photograph best maps to the local row and whether preservation changed between photographs',
    effect_on_034_packet:
      'refines H-771/H-925/H-983 blockers from extra-side claims to same-side photo-selection and preservation checks where applicable',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: '2026-05-25',
    row_type: 'source_convention',
    cisi_or_scope: 'CISI_numbering_parentheses',
    source_volume: 'CISI Collections in India; CISI Collections in Pakistan',
    source_locator:
      'India OCR lines 1501-1504 and 1531-1536; Pakistan OCR lines 1959-1963 and 1967-1973',
    source_url:
      'https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan',
    convention_applied:
      'arabic_numerals_after_side_letter_mark_different_inscriptions_on_one_side;parentheses_after_side_letter_mark_same-side_parts_or_enlargement',
    reconciled_component:
      'standard rule explains letter-following numerals, not object-number labels like H-893 (1) A or H-925 (2) B',
    still_unresolved:
      'H-893 (1) A/B and H-925 (1)/(2) A/B need object-specific catalog notes',
    effect_on_034_packet:
      'numbered target/control labels remain unreconciled and cannot support a substitution test',
    accepted_decipherment_claim: '0',
  },
];

const targetRows = [
  {
    checked_date: '2026-05-25',
    row_type: 'target_reconciliation',
    cisi_or_scope: 'H-771',
    source_volume: 'CISI Collections in Pakistan',
    source_locator: 'Pakistan OCR lines 15990-16050; IA reader page n358',
    source_url:
      'https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/n358/mode/1up',
    convention_applied:
      'A/A_bis/A_ter/A_quater_are_multiple_photos_of_side_A_under_CISI_convention;B_is_a_distinct_side_label',
    reconciled_component:
      'not_four_extra_physical_A_sides;the local two-side shape is less broken than first panel-count wording suggested',
    still_unresolved:
      'which A photograph should anchor the companion row and whether preservation differences affect the local +032-257-840+ mapping',
    effect_on_034_packet:
      'H-771 remains blocked, but the blocker is same-side photo selection plus source-direction/subtype uncertainty, not physical side count',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: '2026-05-25',
    row_type: 'target_reconciliation',
    cisi_or_scope: 'H-893',
    source_volume: 'CISI Collections in Pakistan',
    source_locator: 'Pakistan OCR lines 16795-16832; IA reader page n371',
    source_url:
      'https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/n371/mode/1up',
    convention_applied:
      'base_A/B_are_side_labels;object-number_form_(1)_before_side_letter_is_not_resolved_by_standard_parentheses-after-side convention',
    reconciled_component:
      'the standard CISI side-letter rule confirms that A/B are sides in the base record',
    still_unresolved:
      'whether H-893 (1) A/B is a separate object, copy, alternate photograph group, or catalog sub-entry',
    effect_on_034_packet:
      'H-893 cannot serve as a strict 034 target until base versus (1) mapping is resolved',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: '2026-05-25',
    row_type: 'target_reconciliation',
    cisi_or_scope: 'H-925',
    source_volume: 'CISI Collections in Pakistan',
    source_locator: 'Pakistan OCR lines 16980-17012; IA reader page n373',
    source_url:
      'https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/n373/mode/1up',
    convention_applied:
      'A_bis/B_bis/A_ter_are_multiple_photos_of_sides_A_or_B;H-925_(1)/(2)_before_side_letter_remains_unexplained_by_general_rule',
    reconciled_component:
      'bis/ter elements are no longer counted as extra sides by themselves',
    still_unresolved:
      'the numbered H-925 groups must be identified before H-925 can act as a clean shared 033 control',
    effect_on_034_packet:
      'H-925 remains the dangerous control because it mixes base labels, unexplained numbered labels, and same-side photo variants',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: '2026-05-25',
    row_type: 'target_reconciliation',
    cisi_or_scope: 'H-983',
    source_volume: 'CISI Collections in Pakistan',
    source_locator: 'Pakistan OCR lines 17435-17452; IA reader page n377',
    source_url:
      'https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/n377/mode/1up',
    convention_applied:
      'A/B/C_are_side_labels_under_CISI_convention;A_bis/B_bis/B_ter/C_bis_are_multiple_photos_of_those_sides',
    reconciled_component:
      'bis/ter are same-side photo variants, but C remains a real source side category',
    still_unresolved:
      'why local two-side packet omits the C side and which B photograph maps to local +700-034+',
    effect_on_034_packet:
      'H-983 has a genuine source-side mismatch for any two-side comparison with H-353/H-2211',
    accepted_decipherment_claim: '0',
  },
  {
    checked_date: '2026-05-25',
    row_type: 'target_reconciliation',
    cisi_or_scope: 'H-353',
    source_volume: 'CISI Collections in India',
    source_locator:
      'India OCR lines 8390-8450 and 26950-27005; IA reader pages n265/n696; transient w1200 hashes identical',
    source_url:
      'https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India/page/n265/mode/1up',
    convention_applied:
      'A/B/C_are_side_labels_under_CISI_convention;duplicate_IA_leafs_n265_and_n696_have_identical_w1200_SHA256_5422DE7097106AA1AEF205A067924D153321F7DD91ED1A60BC7A77D2312A4AA6',
    reconciled_component:
      'duplicate IA locators are the same visual page at w1200; C is still a real source side category',
    still_unresolved:
      'why local two-side packet omits H-353 C and whether C is inscriptional, iconographic, or otherwise excluded by the local corpus policy',
    effect_on_034_packet:
      'H-353 remains unusable as the clean 033 control for H-983 until the C side is accounted for',
    accepted_decipherment_claim: '0',
  },
];

const rows = [...conventionRows, ...targetRows];

const targetOnly = targetRows;
const summary = {
  checked_date: '2026-05-25',
  artifact: 'lipi_frame700_034_cisi_variant_convention_probe',
  source_scope:
    'CISI vol. 1/2 introduction conventions plus target OCR/page-label evidence for H-771/H-893/H-925/H-983/H-353',
  rows: rows.length,
  convention_rows: conventionRows.length,
  target_rows: targetRows.length,
  bis_ter_quater_reclassified_as_same_side_photos: targetOnly.filter((row) =>
    /_bis|_ter|_quater/.test(row.convention_applied),
  ).length,
  true_c_side_source_hazards: targetOnly.filter((row) =>
    row.cisi_or_scope === 'H-983' || row.cisi_or_scope === 'H-353',
  ).length,
  object_number_labels_unresolved: targetOnly.filter((row) =>
    row.still_unresolved.includes('(1)') || row.still_unresolved.includes('numbered H-925'),
  ).length,
  h353_duplicate_w1200_sha256:
    '5422DE7097106AA1AEF205A067924D153321F7DD91ED1A60BC7A77D2312A4AA6',
  target_decision_counts: countBy(targetRows, 'effect_on_034_packet'),
  accepted_decipherment_claims: rows.filter((row) => row.accepted_decipherment_claim !== '0')
    .length,
  correction_to_previous_gate:
    'Replace blanket extra-side language with a split: bis/ter/quater are same-side photograph variants; A/B/C labels are side categories; object-number forms like H-893 (1) A and H-925 (2) B remain unreconciled.',
  immediate_research_consequence:
    'H-771 is less physically side-mismatched than first described, but still blocked by photo selection and direction/subtype uncertainty. H-983 and H-353 have genuine C-side hazards. H-893 and H-925 remain blocked by unexplained numbered labels.',
};

fs.mkdirSync(reportsDir, { recursive: true });
fs.writeFileSync(outCsv, toCsv(rows));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
