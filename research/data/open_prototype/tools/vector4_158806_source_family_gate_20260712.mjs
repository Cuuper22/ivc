#!/usr/bin/env node

// Adjudicates the queued 158-806 / Phyt item: does it have enough independent
// support to justify a new pre-registered test, or is it closed? It reads
// reports/lipi_scope_rows.csv and the pinned null table
// reports/vector4_targeted_context_nulls_20260531.csv, plus two cached
// publication extractions under evidence/tmp/ (Parpola 2019 on bone rods, and
// Kenoyer & Meadow 2010 on inscribed objects at Harappa). Each of the seven
// hard-coded witness objects must still match exactly one clean scope row with the
// expected Phyt source label, Harappa site, and TAB:B type, and the pinned null row
// must still show support 3 and a worst null tail of 0.0075; any drift throws
// rather than reporting a stale result. The witnesses are then counted two ways —
// by exact text family, and by a deliberately conservative form/motif stratum that
// treats look-alike objects as one witness — and checked against a support floor of
// 5 with a demand for a source-grade panel behind every text family. It writes a
// witnesses CSV and a summary JSON with input SHA-256 hashes and the decision. The
// gate fails: support 3 is below the floor, source independence is unresolved, and
// the claim ledger increment is zero on every line.

import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..', '..', '..', '..');
const REPORTS = path.join(ROOT, 'research', 'data', 'open_prototype', 'reports');
const INPUT_ROWS = path.join(REPORTS, 'lipi_scope_rows.csv');
const INPUT_NULLS = path.join(REPORTS, 'vector4_targeted_context_nulls_20260531.csv');
const PARPOLA_TEXT = path.join(ROOT, 'evidence', 'tmp', 'parpola_2019_bone_rods.txt');
const KENOYER_TEXT = path.join(
  ROOT,
  'evidence',
  'tmp',
  'h2148_h2100_h2152_110_route',
  'kenoyer_meadow_2010_inscribed_objects_harappa.txt',
);
const OUT_WITNESSES = path.join(REPORTS, 'vector4_158806_source_family_gate_20260712_witnesses.csv');
const OUT_SUMMARY = path.join(REPORTS, 'vector4_158806_source_family_gate_20260712_summary.json');

const WITNESSES = [
  {
    cisi: 'H-1980',
    text: '+400-158-806-475+',
    text_family: '400-158-806-475',
    form_motif_stratum: 'almost_cylindrical_H1979_H1981_form_sensitivity_stratum',
    panel_status: 'no_local_source_grade_panel_CISI_3_1_route',
    evidence: 'Kenoyer_Meadow_2010_printed_p6',
  },
  {
    cisi: 'H-1979',
    text: '+740-158-806-467+',
    text_family: '740-158-806-467',
    form_motif_stratum: 'almost_cylindrical_H1979_H1981_form_sensitivity_stratum',
    panel_status: 'no_local_source_grade_panel_CISI_3_1_route',
    evidence: 'Kenoyer_Meadow_2010_printed_p6',
  },
  ...['H-1104', 'H-1105', 'H-190', 'H-724', 'H-726'].map((cisi) => ({
    cisi,
    text: '+158-806-465+',
    text_family: '158-806-465',
    form_motif_stratum: 'shared_text_sacred_tree_reverse_motif_sensitivity_stratum',
    panel_status: ['H-190', 'H-724', 'H-726'].includes(cisi)
      ? 'derivative_local_panel_not_token_box_source_grade'
      : 'no_local_source_grade_panel_CISI_3_1_route',
    evidence: 'Parpola_2019_published_text_lines_121_123',
  })),
];

function sha256(file) {
  return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
}

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = '';
  let quoted = false;
  for (let index = 0; index < text.length; index += 1) {
    const character = text[index];
    const next = text[index + 1];
    if (quoted) {
      if (character === '"' && next === '"') {
        cell += '"';
        index += 1;
      } else if (character === '"') {
        quoted = false;
      } else {
        cell += character;
      }
    } else if (character === '"') {
      quoted = true;
    } else if (character === ',') {
      row.push(cell);
      cell = '';
    } else if (character === '\n') {
      row.push(cell.replace(/\r$/, ''));
      if (row.some((value) => value !== '')) rows.push(row);
      row = [];
      cell = '';
    } else {
      cell += character;
    }
  }
  if (cell || row.length) {
    row.push(cell.replace(/\r$/, ''));
    rows.push(row);
  }
  const header = rows.shift();
  return rows.map((values) => Object.fromEntries(header.map((field, index) => [field, values[index] ?? ''])));
}

function csvEscape(value) {
  const text = String(value ?? '');
  return /[",\n\r]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(',')];
  for (const row of rows) lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function requireCondition(condition, message) {
  if (!condition) throw new Error(message);
}

function repoRelative(file) {
  return path.relative(ROOT, file).split(path.sep).join('/');
}

for (const input of [INPUT_ROWS, INPUT_NULLS, PARPOLA_TEXT, KENOYER_TEXT]) {
  requireCondition(fs.existsSync(input), `Required input is missing: ${input}`);
}

const scopeRows = parseCsv(fs.readFileSync(INPUT_ROWS, 'utf8'));
const nullRows = parseCsv(fs.readFileSync(INPUT_NULLS, 'utf8'));
const parpola = fs.readFileSync(PARPOLA_TEXT, 'utf8');
const kenoyer = fs.readFileSync(KENOYER_TEXT, 'utf8');

requireCondition(
  /H-189, H-190, H-724, H-725,[\s\S]{0,120}H-726, H-727, H-1104, H-1105, H-1106/.test(parpola),
  'Parpola series evidence no longer contains the expected Harappa catalogue sequence.',
);
requireCondition(
  /H-1956\s*&\s*H-1957 and H-1979, H-1980\s*&\s*H\s*1981/.test(kenoyer),
  'Kenoyer/Meadow form-series evidence no longer contains the expected H-1979/H-1980 sequence.',
);
requireCondition(
  /copies of the same signs and\/or motifs[\s\S]{0,160}duplicate bas-relief tablets/.test(kenoyer),
  'Kenoyer/Meadow dependence warning is missing from the pinned extraction.',
);

const audited = WITNESSES.map((witness) => {
  const matches = scopeRows.filter((row) => row.cisi === witness.cisi && row.text === witness.text);
  requireCondition(matches.length === 1, `Expected exactly one clean row for ${witness.cisi} ${witness.text}; found ${matches.length}.`);
  const row = matches[0];
  requireCondition(row.readiness_bucket === 'lipi_numeric_clean_candidate', `${witness.cisi} left the clean planning bucket.`);
  requireCondition(row.symbol === 'Phyt', `${witness.cisi} no longer carries the Phyt source label.`);
  requireCondition(row.site === 'Harappa', `${witness.cisi} no longer has the asserted Harappa site metadata.`);
  requireCondition(row.type === 'TAB:B', `${witness.cisi} no longer has the asserted TAB:B object type.`);
  return {
    catalogue_id: witness.cisi,
    lipi_row_id: row.id,
    text: witness.text,
    text_family: witness.text_family,
    form_motif_stratum: witness.form_motif_stratum,
    panel_status: witness.panel_status,
    evidence: witness.evidence,
    source_label: row.symbol,
    contains_158_806: witness.text.includes('158-806') ? 'yes' : 'no',
    independence_treatment: 'same_form_motif_stratum_counts_once_for_sensitivity_not_as_proven_common_source',
  };
});

const targetedRows = nullRows.filter((row) => row.target_id === 'text_only_158806_symbol_phyt');
requireCondition(targetedRows.length === 1, `Expected one pinned text-only null row; found ${targetedRows.length}.`);
const targeted = targetedRows[0];
requireCondition(targeted.collapse_mode === 'text_only', 'Pinned null collapse mode changed.');
requireCondition(targeted.unit_kind === 'bigram' && targeted.unit === '158-806', 'Pinned null unit changed.');
requireCondition(targeted.context_field === 'symbol' && targeted.context_value === 'Phyt', 'Pinned null context changed.');
requireCondition(Number(targeted.support) === 3, `Pinned text-only support changed from 3 to ${targeted.support}.`);
requireCondition(
  Math.abs(Number(targeted.worst_z_ge_observed_share) - 0.0075) < 1e-12,
  `Pinned worst null tail changed from 0.0075 to ${targeted.worst_z_ge_observed_share}.`,
);
requireCondition(
  targeted.worst_z_null_model === 'shuffle_units_within_site_type',
  `Pinned worst null model changed to ${targeted.worst_z_null_model}.`,
);
requireCondition(targeted.claim_eligible === 'no', 'The pinned null row unexpectedly became claim-eligible.');

const textFamilies = new Set(audited.map((row) => row.text_family));
const formMotifStrata = new Set(audited.map((row) => row.form_motif_stratum));
const sourceGradePanelFamilies = new Set(
  audited.filter((row) => row.panel_status.startsWith('source_grade')).map((row) => row.text_family),
);
const supportFloor = 5;
const gates = {
  text_family_support_at_least_5: textFamilies.size >= supportFloor,
  conservative_form_motif_sensitivity_strata_at_least_5: formMotifStrata.size >= supportFloor,
  source_grade_panel_for_every_text_family: sourceGradePanelFamilies.size >= textFamilies.size,
  matched_iconographic_negative_packet_present: false,
};
const decision = Object.values(gates).every(Boolean)
  ? 'eligible_for_new_preregistered_familywise_test_only'
  : 'closed_not_claim_eligible_support_below_floor_source_independence_unresolved';

writeCsv(OUT_WITNESSES, audited, [
  'catalogue_id',
  'lipi_row_id',
  'text',
  'text_family',
  'form_motif_stratum',
  'panel_status',
  'evidence',
  'source_label',
  'contains_158_806',
  'independence_treatment',
]);

const summary = {
  run_date: '2026-07-12',
  target: '158-806 / Phyt',
  operation: 'support_source_and_form_motif_sensitivity_adjudication_of_the_existing_text_collapsed_queue_item',
  reran_targeted_nulls: false,
  object_rows: audited.length,
  exact_text_families: textFamilies.size,
  conservative_form_motif_sensitivity_strata: formMotifStrata.size,
  source_grade_text_families_locally_validated: sourceGradePanelFamilies.size,
  broad_scanner_support_floor: supportFloor,
  pinned_text_only_support: Number(targeted.support),
  pinned_worst_fixed_pair_null_share: Number(targeted.worst_z_ge_observed_share),
  gates,
  decision,
  decision_reason: (
    'The decisive failure is exact-text support 3 below the pre-existing floor 5. All witnesses are Harappan TAB:B rows, '
    + 'source-grade token-box coverage and matched iconographic negatives remain absent, and source independence is unresolved. '
    + 'Grouping them into two form/motif strata is a conservative sensitivity analysis, not proof of a common production source.'
  ),
  claim_ledger_increment: {
    translations: 0,
    phonetic_values: 0,
    sign_meanings: 0,
    language_identification: 0,
    structural_findings: 0,
    external_anchors: 0,
  },
  evidence_boundaries: [
    'Form/motif grouping is a sensitivity analysis, not proof of common manufacture, copying, or production source.',
    'Phyt is inherited source metadata, not a decoded semantic label.',
    'The previous null result was a queue trigger, never an accepted sign meaning.',
  ],
  inputs: {
    lipi_scope_rows: { path: repoRelative(INPUT_ROWS), sha256: sha256(INPUT_ROWS) },
    targeted_nulls: { path: repoRelative(INPUT_NULLS), sha256: sha256(INPUT_NULLS) },
    parpola_extraction: { path: repoRelative(PARPOLA_TEXT), sha256: sha256(PARPOLA_TEXT) },
    kenoyer_meadow_extraction: { path: repoRelative(KENOYER_TEXT), sha256: sha256(KENOYER_TEXT) },
  },
  outputs: {
    witnesses: repoRelative(OUT_WITNESSES),
    summary: repoRelative(OUT_SUMMARY),
  },
};
fs.writeFileSync(OUT_SUMMARY, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({
  decision,
  exact_text_families: textFamilies.size,
  form_motif_sensitivity_strata: formMotifStrata.size,
}));
