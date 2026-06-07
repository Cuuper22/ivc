import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const SUMMARY_PATH = path.join(ROOT, 'data/open_prototype/reports/effective_unicity_degeneracy_summary.json');
const EXTERNAL_CANDIDATES = path.join(ROOT, 'data/meluhha/external_phonetic_anchor_candidates.csv');
const OBJECT_ONOMASTIC_SUMMARY = path.join(ROOT, 'data/meluhha/object_level_onomastic_value_summary.json');
const OBJECT_ONOMASTIC_CANDIDATES = path.join(ROOT, 'data/meluhha/object_level_onomastic_value_attempts.csv');
const BRAHMI_SUMMARY = path.join(ROOT, 'data/brahmi/brahmi_shape_descent_null_summary.json');
const BRAHMI_V2_SUMMARY = path.join(ROOT, 'data/brahmi/source_token_brahmi_descent_v2_summary.json');
const BRAHMI_V2_FAMILIES = path.join(ROOT, 'data/brahmi/source_token_family_descent_summary_v2.csv');
const BRAHMI_V3_SUMMARY = path.join(ROOT, 'data/brahmi/brahmi_independent_source_token_gate_v3_summary.json');
const OUT_CSV = path.join(ROOT, 'data/open_prototype/reports/anchored_constraint_collapse_stress.csv');
const OUT_JSON = path.join(ROOT, 'data/open_prototype/reports/anchored_constraint_collapse_stress_summary.json');

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function csvEscape(value) {
  const text = String(value ?? '');
  if (/[",\n\r]/.test(text)) return `"${text.replaceAll('"', '""')}"`;
  return text;
}

function parseCsv(text) {
  const rows = [];
  let row = [];
  let value = '';
  let quoted = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (ch === '"' && next === '"') {
        value += '"';
        i++;
      } else if (ch === '"') {
        quoted = false;
      } else {
        value += ch;
      }
    } else if (ch === '"') {
      quoted = true;
    } else if (ch === ',') {
      row.push(value);
      value = '';
    } else if (ch === '\n') {
      row.push(value.replace(/\r$/, ''));
      rows.push(row);
      row = [];
      value = '';
    } else {
      value += ch;
    }
  }
  if (value.length || row.length) {
    row.push(value.replace(/\r$/, ''));
    rows.push(row);
  }
  const [header, ...body] = rows.filter(r => r.some(cell => cell.length));
  return body.map(cols => Object.fromEntries(header.map((h, idx) => [h, cols[idx] ?? ''])));
}

function parseAssignments(text) {
  const assignments = [];
  for (const part of String(text || '').split(';')) {
    const [sign, value] = part.split('=').map(s => s?.trim());
    if (sign && value) assignments.push({ sign, value });
  }
  return assignments;
}

function log2Factorial(n) {
  let total = 0;
  for (let i = 2; i <= n; i++) total += Math.log2(i);
  return total;
}

function scenarioRecord({ scenario_id, source, status, assignments, note }, totalSigns, baseBits) {
  const bySign = new Map();
  const conflicts = [];
  for (const a of assignments) {
    if (bySign.has(a.sign) && bySign.get(a.sign) !== a.value) {
      conflicts.push(`${a.sign}:${bySign.get(a.sign)}!=${a.value}`);
    }
    bySign.set(a.sign, a.value);
  }
  const distinctAnchoredSigns = bySign.size;
  const residualBits = log2Factorial(Math.max(0, totalSigns - distinctAnchoredSigns));
  const reductionBits = baseBits - residualBits;
  return {
    scenario_id,
    source,
    status,
    attempted_anchor_count: assignments.length,
    distinct_anchored_signs: distinctAnchoredSigns,
    conflicts: conflicts.join(';'),
    base_label_symmetry_log2_bits: baseBits,
    residual_label_symmetry_log2_bits: residualBits,
    reduction_log2_bits: reductionBits,
    residual_share_of_base: residualBits / baseBits,
    assignments: assignments.map(a => `${a.sign}=${a.value}`).join(';'),
    note,
    decision: status === 'accepted' ? 'not_applicable_no_accepted_phonetic_anchors_exist' : 'stress_only_rejected_anchor_not_admissible',
  };
}

const degeneracy = readJson(SUMMARY_PATH);
const totalSigns = degeneracy.primary_full_coverage.unique_signs;
const baseBits = degeneracy.primary_full_coverage.label_symmetry_log2_bits;
const externalRows = fs.existsSync(EXTERNAL_CANDIDATES)
  ? parseCsv(fs.readFileSync(EXTERNAL_CANDIDATES, 'utf8'))
  : [];
const objectOnomastic = fs.existsSync(OBJECT_ONOMASTIC_SUMMARY) ? readJson(OBJECT_ONOMASTIC_SUMMARY) : null;
const objectOnomasticRows = fs.existsSync(OBJECT_ONOMASTIC_CANDIDATES)
  ? parseCsv(fs.readFileSync(OBJECT_ONOMASTIC_CANDIDATES, 'utf8'))
  : [];
const brahmi = fs.existsSync(BRAHMI_SUMMARY) ? readJson(BRAHMI_SUMMARY) : null;
const brahmiV2 = fs.existsSync(BRAHMI_V2_SUMMARY) ? readJson(BRAHMI_V2_SUMMARY) : null;
const brahmiV3 = fs.existsSync(BRAHMI_V3_SUMMARY) ? readJson(BRAHMI_V3_SUMMARY) : null;
const brahmiV2FamilyRows = fs.existsSync(BRAHMI_V2_FAMILIES)
  ? parseCsv(fs.readFileSync(BRAHMI_V2_FAMILIES, 'utf8'))
  : [];

const scenarios = [];
scenarios.push({
  scenario_id: 'accepted_anchors_only',
  source: 'claim_ledger',
  status: 'accepted',
  assignments: [],
  note: 'No external phonetic or Brahmi-derived phonetic anchors are accepted.',
});

for (const row of externalRows) {
  if (
    [
      'cand_c5b412735788647e',
      'cand_f2065d16be860e5d',
      'cand_62a50aebe8534ac5',
      'cand_d98836e53bf9081a',
    ].includes(row.candidate_id)
  ) {
    scenarios.push({
      scenario_id: `weak_${row.target_id}_${row.external_row_id.replaceAll('.', '_')}`,
      source: 'retracted_external_phonetic_anchor_length_pattern_values_2026_05_29',
      status: 'retracted',
      assignments: parseAssignments(row.candidate_values),
      note: `${row.target_label} on ${row.external_site} ${row.external_row_id}; ${row.decision}.`,
    });
  }
}

const strictObjectOnomasticRows = objectOnomasticRows.filter(row =>
  row.decision === 'rejected_mapped_indus_object_has_no_readable_script_bridge'
);
for (const row of strictObjectOnomasticRows) {
  scenarios.push({
    scenario_id: `weak_object_onomastic_${row.target_id}_${row.external_row_id.replaceAll('.', '_')}`,
    source: 'retracted_object_level_onomastic_value_attempts_2026_05_30',
    status: 'retracted',
    assignments: parseAssignments(row.candidate_values),
    note:
      `${row.target_label} on ${row.external_site} ${row.external_row_id}; ${row.decision}; ` +
      `object bridge state ${row.object_bridge_state}; target-site null >= observed share ` +
      `${objectOnomastic?.forger?.null_ge_observed_share ?? 'missing'}.`,
  });
}

const brahmiRows = brahmi?.family_consistency?.local_220_source_top1_rows ?? [];
for (const row of brahmiRows) {
  scenarios.push({
    scenario_id: `weak_brahmi_local220_${row.probe_id}`,
    source: 'retracted_brahmi_shape_descent_nearest_neighbors_2026_05_29',
    status: 'retracted',
    assignments: [{ sign: '220', value: row.brahmi_transliteration }],
    note: `Top-1 Brahmi neighbor for ${row.probe_id}; rejected by family inconsistency and shape null.`,
  });
}

const brahmiV2NearMisses = brahmiV2FamilyRows
  .filter(row => Number(row.sample_count) >= 2 && Number(row.modal_share) >= 1)
  .sort((a, b) => {
    const shape = Number(a.shape_modal_distance_le_observed_share) - Number(b.shape_modal_distance_le_observed_share);
    if (shape) return shape;
    const label = Number(a.label_null_ge_observed_modal_count_share) - Number(b.label_null_ge_observed_modal_count_share);
    if (label) return label;
    const sample = Number(b.sample_count) - Number(a.sample_count);
    if (sample) return sample;
    return Number(a.mean_top1_distance) - Number(b.mean_top1_distance);
  })
  .slice(0, 5);

for (const row of brahmiV2NearMisses) {
  scenarios.push({
    scenario_id: `weak_brahmi_v2_${row.sign_id}_${row.orientation_policy}`,
    source: 'retracted_brahmi_source_token_descent_v2_2026_05_30',
    status: 'retracted',
    assignments: [{ sign: row.sign_id, value: row.modal_brahmi_label }],
    note:
      `V2 source-token near-miss; samples=${row.sample_count}, shape_null=${row.shape_modal_distance_le_observed_share}, ` +
      `label_null=${row.label_null_ge_observed_modal_count_share}; ${row.gate_decision}.`,
  });
}

const v2SeenSigns = new Set();
const v2TopNonconflicting = [];
for (const row of brahmiV2NearMisses) {
  if (v2SeenSigns.has(row.sign_id)) continue;
  v2SeenSigns.add(row.sign_id);
  v2TopNonconflicting.push({ sign: row.sign_id, value: row.modal_brahmi_label });
}
if (v2TopNonconflicting.length) {
  scenarios.push({
    scenario_id: 'weak_brahmi_v2_top_nearmiss_nonconflicting_set',
    source: 'retracted_brahmi_source_token_descent_v2_2026_05_30',
    status: 'retracted',
    assignments: v2TopNonconflicting,
    note:
      `Top ${v2TopNonconflicting.length} nonconflicting V2 source-token near-misses forced as an inadmissible stress set; ` +
      `summary status ${brahmiV2?.status ?? 'missing_summary'}.`,
  });
}

const firstExternal = scenarios.find(s => s.scenario_id === 'weak_ship_ma2_meluhha_147_1');
const firstBrahmi = scenarios.find(s => s.scenario_id.startsWith('weak_brahmi_local220_'));
if (firstExternal && firstBrahmi) {
  scenarios.push({
    scenario_id: 'weak_combined_ship_failaka147_plus_one_brahmi220',
    source: 'combined_retracted_stress',
    status: 'retracted',
    assignments: [...firstExternal.assignments, ...firstBrahmi.assignments],
    note: 'Maximal illustrative nonconflicting stress from one four-sign external candidate plus one weak Brahmi local-220 candidate.',
  });
}

const strongestObjectOnomastic = scenarios.find(s => s.scenario_id === 'weak_object_onomastic_ur_guna_meluhha_3898_1');
if (strongestObjectOnomastic && v2TopNonconflicting.length) {
  scenarios.push({
    scenario_id: 'weak_combined_object_onomastic3898_plus_brahmi_v2_nearmiss_set',
    source: 'combined_retracted_stress',
    status: 'retracted',
    assignments: [...strongestObjectOnomastic.assignments, ...v2TopNonconflicting],
    note:
      'Maximal current rejected-anchor stress from the strict mapped U17649 onomastic value attempt plus the top nonconflicting Brahmi v2 near-miss set. ' +
      'Both source lanes are retracted and inadmissible.',
  });
}

for (const k of [1, 2, 3, 4, 5, 8, 10, 20, 50]) {
  scenarios.push({
    scenario_id: `idealized_${k}_accepted_independent_anchors`,
    source: 'idealized_lower_bound',
    status: 'hypothetical',
    assignments: Array.from({ length: k }, (_, idx) => ({ sign: `S${idx + 1}`, value: `V${idx + 1}` })),
    note: 'Idealized lower-bound curve: independent accepted sign-value anchors with no homophony, allography, or polyvalence.',
  });
}

const records = scenarios.map(s => scenarioRecord(s, totalSigns, baseBits));
fs.writeFileSync(
  OUT_CSV,
  [
    [
      'scenario_id',
      'source',
      'status',
      'attempted_anchor_count',
      'distinct_anchored_signs',
      'conflicts',
      'base_label_symmetry_log2_bits',
      'residual_label_symmetry_log2_bits',
      'reduction_log2_bits',
      'residual_share_of_base',
      'assignments',
      'note',
      'decision',
    ].join(','),
    ...records.map(r =>
      [
        r.scenario_id,
        r.source,
        r.status,
        r.attempted_anchor_count,
        r.distinct_anchored_signs,
        r.conflicts,
        r.base_label_symmetry_log2_bits.toFixed(6),
        r.residual_label_symmetry_log2_bits.toFixed(6),
        r.reduction_log2_bits.toFixed(6),
        r.residual_share_of_base.toFixed(6),
        r.assignments,
        r.note,
        r.decision,
      ].map(csvEscape).join(',')
    ),
  ].join('\n') + '\n',
  'utf8'
);

const accepted = records.find(r => r.scenario_id === 'accepted_anchors_only');
const weakMax = records
  .filter(r => r.status === 'retracted')
  .sort((a, b) => b.reduction_log2_bits - a.reduction_log2_bits)[0];
const idealized = records.filter(r => r.status === 'hypothetical');

fs.writeFileSync(
  OUT_JSON,
  JSON.stringify(
    {
      date: '2026-05-30',
      status: 'anchored_constraint_collapse_no_admissible_anchor',
      total_signs: totalSigns,
      base_label_symmetry_log2_bits: baseBits,
      accepted_anchor_scenario: accepted,
      strongest_retracted_stress_scenario: weakMax,
      brahmi_v2_status: brahmiV2
        ? {
            status: brahmiV2.status,
            candidate_only_rows: brahmiV2.counts?.candidate_only_rows ?? null,
            accepted_phonetic_anchors: brahmiV2.counts?.accepted_phonetic_anchors ?? null,
          }
        : null,
      brahmi_v3_status: brahmiV3
        ? {
            status: brahmiV3.status,
            review_packet_eligible_rows: brahmiV3.review_packet_eligible_rows ?? null,
            candidate_only_rows: brahmiV3.candidate_only_rows ?? null,
            accepted_phonetic_anchors: brahmiV3.accepted_phonetic_anchors ?? null,
          }
        : null,
      object_level_onomastic_status: objectOnomastic
        ? {
            status: objectOnomastic.status,
            strict_mapped_indus_only_value_attempts: objectOnomastic.strict_mapped_indus_only_value_attempts,
            accepted_external_anchors: objectOnomastic.accepted_external_anchors,
            null_ge_observed_share: objectOnomastic.forger?.null_ge_observed_share ?? null,
          }
        : null,
      idealized_curve: idealized,
      decision:
        'No anchored partial reading is admissible because all external and Brahmi phonetic candidates are retracted. The object-level onomastic harness produced zero accepted external anchors, and Brahmi V3 blocks every source-token family before review. Forcing rejected near-misses remains stress-only and does not create a reading.',
      files: {
        csv: 'data/open_prototype/reports/anchored_constraint_collapse_stress.csv',
        summary: 'data/open_prototype/reports/anchored_constraint_collapse_stress_summary.json',
      },
    },
    null,
    2
  ),
  'utf8'
);
