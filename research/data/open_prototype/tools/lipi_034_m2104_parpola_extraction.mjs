import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const lipiPath = path.join(base, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const candidatesPath = path.join(reportsDir, 'crosswalk_lipi_to_mayig_candidates.csv');

const rowsOut = path.join(reportsDir, 'lipi_034_m2104_parpola_context_rows.csv');
const hypothesesOut = path.join(reportsDir, 'lipi_034_m2104_parpola_mapping_hypotheses.csv');
const summaryOut = path.join(reportsDir, 'lipi_034_m2104_parpola_extraction_summary.json');

const checkedDate = '2026-05-25';

function parseCsv(text) {
  const rows = [];
  let row = [];
  let value = '';
  let inQuotes = false;

  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (inQuotes) {
      if (ch === '"' && next === '"') {
        value += '"';
        i += 1;
      } else if (ch === '"') {
        inQuotes = false;
      } else {
        value += ch;
      }
    } else if (ch === '"') {
      inQuotes = true;
    } else if (ch === ',') {
      row.push(value);
      value = '';
    } else if (ch === '\n') {
      row.push(value);
      if (row.length > 1 || row[0] !== '') rows.push(row);
      row = [];
      value = '';
    } else if (ch !== '\r') {
      value += ch;
    }
  }
  if (value.length > 0 || row.length > 0) {
    row.push(value);
    rows.push(row);
  }
  return rows;
}

function csvObjects(text) {
  const [header, ...body] = parseCsv(text);
  return body.map((row) =>
    Object.fromEntries(header.map((key, index) => [key, row[index] ?? ''])),
  );
}

function toCsv(rows) {
  if (rows.length === 0) return '';
  const header = Object.keys(rows[0]);
  const body = rows.map((row) =>
    header
      .map((key) => `"${String(row[key] ?? '').replaceAll('"', '""')}"`)
      .join(','),
  );
  return `${[header.map((key) => `"${key}"`).join(','), ...body].join('\n')}\n`;
}

function tokens(text) {
  return String(text ?? '')
    .replaceAll('+', '')
    .replaceAll('[', '')
    .replaceAll(']', '')
    .split('-')
    .map((token) => token.trim())
    .filter(Boolean);
}

function countBy(rows, keyFn) {
  const counts = {};
  for (const row of rows) {
    const key = keyFn(row);
    counts[key] = (counts[key] ?? 0) + 1;
  }
  return Object.fromEntries(
    Object.entries(counts).sort((a, b) => a[0].localeCompare(b[0], undefined, { numeric: true })),
  );
}

const lipiRows = csvObjects(fs.readFileSync(lipiPath, 'utf8'));
const candidates = csvObjects(fs.readFileSync(candidatesPath, 'utf8'));
const byCisi = new Map(lipiRows.map((row) => [row.cisi, row]));
const candidateBySign = new Map(candidates.map((row) => [row.source_a_sign, row]));

const contextSpecs = [
  {
    cisi: 'M-2104',
    parpola_role: 'text_12_target',
    parpola_extract:
      'Fig. 1 text no. 12; prose says rod text begins with UIII (three pots), followed by signs 15 and 1.',
    local_grouping:
      '151=sign_1_candidate;097=sign_15_candidate;700-034=UIII_candidate',
    comparison_status: 'target_matches_parpola_prose_under_compound_grouping',
  },
  {
    cisi: 'M-478',
    parpola_role: 'text_12_tablet_parallel',
    parpola_extract:
      'Named tablet parallel to text no. 12; prose says tablet text begins with UIIII (four pots), followed by signs 15 and 107.',
    local_grouping:
      '400=sign_107_candidate;097=sign_15_candidate;700-004=UIIII_candidate',
    comparison_status: 'parallel_matches_target_frame_with_count_and_final_sign_swap',
  },
  {
    cisi: 'M-480',
    parpola_role: 'text_12_tablet_parallel',
    parpola_extract:
      'Named tablet parallel to text no. 12; prose says tablet text begins with UIIII (four pots), followed by signs 15 and 107.',
    local_grouping:
      '400=sign_107_candidate;097=sign_15_candidate;700-004=UIIII_candidate',
    comparison_status: 'parallel_matches_target_frame_with_count_and_final_sign_swap',
  },
  {
    cisi: 'M-1425',
    parpola_role: 'text_12_tablet_parallel',
    parpola_extract:
      'Named tablet parallel to text no. 12; prose says tablet text begins with UIIII (four pots), followed by signs 15 and 107.',
    local_grouping:
      '400=sign_107_candidate;097=sign_15_candidate;700-004=UIIII_candidate',
    comparison_status: 'parallel_matches_target_frame_with_count_and_final_sign_swap',
  },
  {
    cisi: 'H-543',
    parpola_role: 'sign_15_1_control',
    parpola_extract:
      'Parpola prose says signs 15 and 1 form the sole text of unicorn seals H-543 and H-544.',
    local_grouping: '151-097 visible in local damaged text; R/L reading gives 097 then 151',
    comparison_status: 'supports_097_as_sign_15_and_151_as_sign_1_if_direction_RL',
  },
  {
    cisi: 'H-544',
    parpola_role: 'sign_15_1_control',
    parpola_extract:
      'Parpola prose says signs 15 and 1 form the sole text of unicorn seals H-543 and H-544.',
    local_grouping: '151-097 visible in local damaged text; R/L reading gives 097 then 151',
    comparison_status: 'supports_097_as_sign_15_and_151_as_sign_1_if_direction_RL',
  },
  {
    cisi: 'M-915',
    parpola_role: 'sign_15_1_named_seal_control',
    parpola_extract:
      'Parpola prose names M-915 among seals where the signs 15 and 1 occur at the end of the text.',
    local_grouping: '151-097-031 in local text; R/L reading gives 031 then 097 then 151',
    comparison_status: 'supports_final_097_151_under_RL_reading',
  },
  {
    cisi: 'M-715',
    parpola_role: 'named_context_conflict_or_unresolved',
    parpola_extract:
      'Parpola prose says signs 15 and 1 begin the text in M-715.',
    local_grouping: 'local row does not expose a 151/097 pair in current filtered text',
    comparison_status: 'unresolved_conflict_requires_source_check',
  },
  {
    cisi: 'M-896',
    parpola_role: 'named_context_conflict_or_unresolved',
    parpola_extract:
      'Parpola prose names M-896 among seals where signs 15 and 1 occur at the end of the text.',
    local_grouping: 'local row begins with 151 but does not expose a 151/097 pair',
    comparison_status: 'unresolved_conflict_requires_source_check',
  },
];

const contextRows = contextSpecs.map((spec) => {
  const row = byCisi.get(spec.cisi) ?? {};
  const tokenList = tokens(row.text);
  return {
    checked_date: checkedDate,
    cisi: spec.cisi,
    lipi_id: row.id ?? '',
    site: row.site ?? '',
    object_type: row.type ?? '',
    material: row.material ?? '',
    preservation: row.preservation ?? '',
    complete: row.complete ?? '',
    direction: row['dir.'] ?? '',
    local_text: row.text ?? '',
    local_tokens_left_to_right: tokenList.join(' '),
    local_tokens_if_RL_reading: [...tokenList].reverse().join(' '),
    parpola_role: spec.parpola_role,
    parpola_extract: spec.parpola_extract,
    local_grouping: spec.local_grouping,
    comparison_status: spec.comparison_status,
    source_basis:
      'Parpola 2019 Fig. 1 visual row 12 plus prose on text no. 12 and named parallels/controls',
    accepted_decipherment_claim: '0',
  };
});

const hypotheses = [
  {
    local_sign_or_group: '151',
    parpola_candidate: 'sign_1',
    hypothesis_type: 'single_sign_mapping',
    supporting_objects: 'M-2104;H-543;H-544;M-915',
    contradicting_or_unresolved_objects: 'M-715;M-896',
    prior_crosswalk_support: candidateBySign.get('151')?.top_source_b_sign === 'P001' ? '151_to_P001' : '',
    evidence_grade: 'B_strong_local_prior_but_source_image_pending',
    reason:
      'M-2104 final prose unit is sign 1 while local target has 151 in the matching non-pot slot; H-543/H-544 and M-915 support 097-151 under R/L reading.',
    next_test:
      'Inspect CISI images or authoritative Parpola sign-list rows for M-2104, H-543, H-544, M-915, M-715, and M-896.',
    accepted_mapping: '0',
  },
  {
    local_sign_or_group: '097',
    parpola_candidate: 'sign_15',
    hypothesis_type: 'single_sign_mapping',
    supporting_objects: 'M-2104;M-478;M-480;M-1425;H-543;H-544;M-915',
    contradicting_or_unresolved_objects: '',
    prior_crosswalk_support: '',
    evidence_grade: 'B_strong_local_prior_but_source_image_pending',
    reason:
      '097 is the invariant sign between M-2104 and the three named tablet parallels exactly where Parpola says signs 15 follows the pot-count cluster; H-543/H-544/M-915 controls support the same slot with 151.',
    next_test:
      'Check Parpola Fig. 1 row 12 and the source photos for diagnostic visual identity of sign 15.',
    accepted_mapping: '0',
  },
  {
    local_sign_or_group: '700',
    parpola_candidate: 'U_or_pot_component_of_UIII_UIIII_cluster',
    hypothesis_type: 'compound_component_mapping',
    supporting_objects: 'M-2104;M-478;M-480;M-1425',
    contradicting_or_unresolved_objects: '',
    prior_crosswalk_support: candidateBySign.get('700')?.top_source_b_sign
      ? `weak_${candidateBySign.get('700').top_source_b_sign}`
      : '',
    evidence_grade: 'C_compound_component_hypothesis',
    reason:
      '700 is shared in the local 700-034 and 700-004 groups where Parpola contrasts UIII with UIIII.',
    next_test:
      'Do not map 700 alone until the U/V pot sign and numeral strokes are separable in source imagery.',
    accepted_mapping: '0',
  },
  {
    local_sign_or_group: '034',
    parpola_candidate: 'three_stroke_count_component_in_UIII',
    hypothesis_type: 'compound_component_mapping',
    supporting_objects: 'M-2104',
    contradicting_or_unresolved_objects: '',
    prior_crosswalk_support: '',
    evidence_grade: 'C_single_target_but_high_value_for_034',
    reason:
      'M-2104 has 700-034 where Parpola says the rod has UIII, while the tablet parallels have 700-004 where Parpola says UIIII.',
    next_test:
      'Acquire M-2104 source image and compare 034 stroke count against 004 in M-478/M-480/M-1425.',
    accepted_mapping: '0',
  },
  {
    local_sign_or_group: '004',
    parpola_candidate: 'four_stroke_count_component_in_UIIII',
    hypothesis_type: 'compound_component_mapping',
    supporting_objects: 'M-478;M-480;M-1425',
    contradicting_or_unresolved_objects: '',
    prior_crosswalk_support: '',
    evidence_grade: 'C_parallel_only_component_hypothesis',
    reason:
      '004 occupies the same local group position as 034 in the three named tablet parallels, where Parpola says the count is four pots instead of three.',
    next_test:
      'Inspect named tablet images to check whether 004 is visually four strokes in the same cluster class as 034.',
    accepted_mapping: '0',
  },
  {
    local_sign_or_group: '400',
    parpola_candidate: 'sign_107',
    hypothesis_type: 'single_sign_mapping',
    supporting_objects: 'M-478;M-480;M-1425',
    contradicting_or_unresolved_objects: '',
    prior_crosswalk_support: '',
    evidence_grade: 'C_parallel_tail_hypothesis',
    reason:
      '400 is the local non-shared sign in all three tablet parallels where Parpola says the counterpart to rod sign 1 is sign 107.',
    next_test:
      'Check whether local 400 is visually the comb/wing-like sign 107 in the tablet source photos.',
    accepted_mapping: '0',
  },
];

const summary = {
  checked_date: checkedDate,
  artifact: 'lipi_034_m2104_parpola_extraction',
  question:
    'Can Parpola 2019 text no. 12 and named parallels explain the local lipi M-2104 row +151-097-700-034+?',
  source_pdf:
    'https://tuhat.helsinki.fi/ws/portalfiles/portal/129602857/Parpola_A_2019_Inscriptions_incised_on_the_Harappan_bone_rods_Proceedings_of_EASAA_22.pdf',
  rendered_visual_check:
    'tmp/pdfs/parpola_2019_page2-2.png; tmp/pdfs/parpola_2019_fig1_text12_crop3.png',
  target: 'M-2104',
  target_local_text: byCisi.get('M-2104')?.text ?? '',
  named_tablet_parallel_texts: 'M-478:+400-097-700-004+;M-480:+400-097-700-004+;M-1425:+400-097-700-004+',
  main_extraction:
    'M-2104 +151-097-700-034+ aligns structurally with tablet parallels +400-097-700-004+: 151 vs 400 is Parpola sign 1 vs sign 107; 097 is sign 15 candidate; 700-034 vs 700-004 is the UIII vs UIIII pot-count cluster candidate.',
  context_row_count: contextRows.length,
  hypothesis_row_count: hypotheses.length,
  context_status_counts: countBy(contextRows, (row) => row.comparison_status),
  accepted_mappings: 0,
  accepted_decipherment_claims: 0,
  outputs: [
    path.relative(base, rowsOut).replaceAll('\\', '/'),
    path.relative(base, hypothesesOut).replaceAll('\\', '/'),
    path.relative(base, summaryOut).replaceAll('\\', '/'),
  ],
};

fs.writeFileSync(rowsOut, toCsv(contextRows), 'utf8');
fs.writeFileSync(hypothesesOut, toCsv(hypotheses), 'utf8');
fs.writeFileSync(summaryOut, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
