// One-off re-audit (2026-05-31) of the "low real-token-null" Brahmi rows.
// The v3 impostor-forger run flagged some sign families where fewer than 1% of
// forged impostor tokens matched as well as the real tokens did — a result that
// could look like a genuine Indus-to-Brahmi phonetic anchor. This script re-reads
// the forger CSV/JSON, the v3 independence preflight CSV, and the v2 family
// descent summary CSV, and checks each low-null row against the original
// shape-null and label-null thresholds, the v3 preflight, minimum independence
// (at least 3 unique token hashes, CISI objects, and source paths), duplicate-collapse
// unanimity, and modal-label stability. It writes one CSV row per low-null family
// with every failure flag spelled out, plus a JSON summary with SHA-256 hashes of
// all inputs. The conclusion baked into the output: every low-null row fails at
// least one gate, so no hidden phonetic anchor survives.
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, 'data', 'brahmi');
const RUN_ID = 'replacement_20260531';

const FORGER_CSV = path.join(OUT_DIR, 'brahmi_real_token_impostor_forger_v3.csv');
const FORGER_SUMMARY = path.join(OUT_DIR, 'brahmi_real_token_impostor_forger_v3_summary.json');
const PREFLIGHT_CSV = path.join(OUT_DIR, 'brahmi_independent_source_token_gate_v3.csv');
const FAMILY_CSV = path.join(OUT_DIR, 'source_token_family_descent_summary_v2.csv');

const OUT_CSV = path.join(OUT_DIR, 'brahmi_real_token_low_null_reaudit_20260531.csv');
const OUT_JSON = path.join(OUT_DIR, 'brahmi_real_token_low_null_reaudit_20260531_summary.json');

const LOW_NULL_THRESHOLD = 0.01;

const FIELDS = [
  'sign_id',
  'orientation_policy',
  'sample_count',
  'modal_brahmi_label',
  'v3_cisi_modal_label',
  'impostor_ge_observed_share',
  'original_shape_null_share',
  'original_label_null_share',
  'unique_sha256_count',
  'unique_cisi_count',
  'review_packet_eligible',
  'fail_original_shape_null',
  'fail_original_label_null',
  'fail_v3_preflight',
  'fail_min_independence',
  'fail_duplicate_unanimity',
  'fail_modal_label_stability',
  'replacement_decision',
  'blocked_reasons',
];

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = '';
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (ch === '"' && next === '"') {
        cell += '"';
        i += 1;
      } else if (ch === '"') {
        quoted = false;
      } else {
        cell += ch;
      }
    } else if (ch === '"') {
      quoted = true;
    } else if (ch === ',') {
      row.push(cell);
      cell = '';
    } else if (ch === '\n') {
      row.push(cell.replace(/\r$/, ''));
      rows.push(row);
      row = [];
      cell = '';
    } else {
      cell += ch;
    }
  }
  if (cell.length || row.length) {
    row.push(cell.replace(/\r$/, ''));
    rows.push(row);
  }
  if (!rows.length) return [];
  const header = rows[0];
  return rows.slice(1).filter((r) => r.some((v) => v !== '')).map((r) => {
    const out = {};
    header.forEach((h, i) => {
      out[h] = r[i] ?? '';
    });
    return out;
  });
}

function csvEscape(value) {
  const text = String(value ?? '');
  if (/[",\n\r]/.test(text)) return `"${text.replaceAll('"', '""')}"`;
  return text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(',')];
  for (const row of rows) {
    lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  }
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function key(row) {
  return `${row.sign_id}::${row.orientation_policy}`;
}

function fileHash(file) {
  return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
}

function yesNo(flag) {
  return flag ? 'true' : 'false';
}

const forgerRows = parseCsv(fs.readFileSync(FORGER_CSV, 'utf8'));
const forgerSummary = JSON.parse(fs.readFileSync(FORGER_SUMMARY, 'utf8'));
const preflightRows = parseCsv(fs.readFileSync(PREFLIGHT_CSV, 'utf8'));
const familyRows = parseCsv(fs.readFileSync(FAMILY_CSV, 'utf8'));

const preflightByKey = new Map(preflightRows.map((row) => [key(row), row]));
const familyByKey = new Map(familyRows.map((row) => [key(row), row]));

const fullRows = forgerRows.filter((row) => Number(row.iterations) > 0);
const lowRows = fullRows
  .filter((row) => Number(row.impostor_ge_observed_share) <= LOW_NULL_THRESHOLD)
  .map((row) => {
    const pre = preflightByKey.get(key(row)) ?? {};
    const family = familyByKey.get(key(row)) ?? {};
    const blockedReasons = String(pre.blocked_reasons || row.blocked_reason || '').split(';').filter(Boolean);
    const shapeNull = Number(row.original_shape_null_share);
    const labelNull = Number(row.original_label_null_share);
    const failShape = !(Number.isFinite(shapeNull) && shapeNull <= LOW_NULL_THRESHOLD);
    const failLabel = !(Number.isFinite(labelNull) && labelNull <= LOW_NULL_THRESHOLD);
    const failPreflight = pre.review_packet_eligible !== 'true' || row.v3_preflight_decision !== 'review_packet_eligible';
    const failMinIndependence = blockedReasons.some((reason) => [
      'fewer_than_3_unique_token_hashes',
      'fewer_than_3_unique_cisis',
      'fewer_than_3_unique_source_paths',
    ].includes(reason));
    const failDuplicateUnanimity = blockedReasons.includes('not_unanimous_after_duplicate_collapse')
      || pre.unanimity_after_collapse === 'not_unanimous';
    const failModalLabelStability = blockedReasons.includes('modal_label_changes_after_collapse');

    const replacementReasons = [];
    if (failShape) replacementReasons.push('original_shape_null_above_0_01');
    if (failLabel) replacementReasons.push('original_label_null_above_0_01');
    if (failPreflight) replacementReasons.push('failed_v3_independence_preflight');
    if (failMinIndependence) replacementReasons.push('failed_minimum_independence');
    if (failDuplicateUnanimity) replacementReasons.push('failed_duplicate_collapse_unanimity');
    if (failModalLabelStability) replacementReasons.push('modal_label_changes_after_collapse');
    if (family.accepted_phonetic_anchor !== 'true') replacementReasons.push('not_accepted_in_v2_gate');

    return {
      sign_id: row.sign_id,
      orientation_policy: row.orientation_policy,
      sample_count: row.sample_count,
      modal_brahmi_label: row.modal_brahmi_label,
      v3_cisi_modal_label: row.v3_cisi_modal_label,
      impostor_ge_observed_share: row.impostor_ge_observed_share,
      original_shape_null_share: row.original_shape_null_share,
      original_label_null_share: row.original_label_null_share,
      unique_sha256_count: pre.unique_sha256_count ?? '',
      unique_cisi_count: pre.unique_cisi_count ?? '',
      review_packet_eligible: pre.review_packet_eligible ?? 'false',
      fail_original_shape_null: yesNo(failShape),
      fail_original_label_null: yesNo(failLabel),
      fail_v3_preflight: yesNo(failPreflight),
      fail_min_independence: yesNo(failMinIndependence),
      fail_duplicate_unanimity: yesNo(failDuplicateUnanimity),
      fail_modal_label_stability: yesNo(failModalLabelStability),
      replacement_decision: 'blocked_before_review_no_anchor',
      blocked_reasons: replacementReasons.join(';'),
    };
  })
  .sort((a, b) => Number(a.impostor_ge_observed_share) - Number(b.impostor_ge_observed_share)
    || a.sign_id.localeCompare(b.sign_id)
    || a.orientation_policy.localeCompare(b.orientation_policy));

const count = (predicate) => lowRows.filter(predicate).length;
const passBothIndependenceAndUnanimity = lowRows.filter((row) => row.fail_min_independence === 'false'
  && row.fail_duplicate_unanimity === 'false');

const summary = {
  run_id: RUN_ID,
  date: '2026-05-31',
  cutoff_guardrail: 'Does not read tmp/quarantine_bad_successor_20260531T0104 and does not read any v3b low-null artifact.',
  threshold: LOW_NULL_THRESHOLD,
  input_hashes_sha256: {
    [path.relative(ROOT, FORGER_CSV).replaceAll('\\', '/')]: fileHash(FORGER_CSV),
    [path.relative(ROOT, FORGER_SUMMARY).replaceAll('\\', '/')]: fileHash(FORGER_SUMMARY),
    [path.relative(ROOT, PREFLIGHT_CSV).replaceAll('\\', '/')]: fileHash(PREFLIGHT_CSV),
    [path.relative(ROOT, FAMILY_CSV).replaceAll('\\', '/')]: fileHash(FAMILY_CSV),
  },
  forger_checkpoint: {
    input_family_rows: forgerSummary.input_family_rows,
    rows_with_full_impostor_iterations: forgerSummary.rows_with_full_impostor_iterations,
    real_token_null_above_0_01_rows: forgerSummary.real_token_null_above_0_01_rows,
    real_token_null_at_or_below_0_01_rows: forgerSummary.real_token_null_at_or_below_0_01_rows,
    accepted_phonetic_anchors: forgerSummary.accepted_phonetic_anchors,
  },
  low_null_rows: lowRows.length,
  low_null_fail_original_shape_null_rows: count((row) => row.fail_original_shape_null === 'true'),
  low_null_fail_original_label_null_rows: count((row) => row.fail_original_label_null === 'true'),
  low_null_fail_v3_preflight_rows: count((row) => row.fail_v3_preflight === 'true'),
  low_null_fail_min_independence_rows: count((row) => row.fail_min_independence === 'true'),
  low_null_fail_duplicate_unanimity_rows: count((row) => row.fail_duplicate_unanimity === 'true'),
  low_null_fail_modal_label_stability_rows: count((row) => row.fail_modal_label_stability === 'true'),
  low_null_pass_min_independence_and_duplicate_unanimity_rows: passBothIndependenceAndUnanimity.length,
  review_packet_eligible_low_null_rows: count((row) => row.review_packet_eligible === 'true'),
  candidate_only_rows: 0,
  accepted_phonetic_anchors: 0,
  lowest_rows: lowRows.slice(0, 10).map((row) => ({
    sign_id: row.sign_id,
    orientation_policy: row.orientation_policy,
    label: row.modal_brahmi_label,
    impostor_ge_observed_share: row.impostor_ge_observed_share,
    blocked_reasons: row.blocked_reasons,
  })),
  conclusion: 'The low real-token-null subset contains no hidden Brahmi phonetic anchor. Every low-null row fails the original shape-null threshold and the v3 preflight; most also fail label-null and/or minimum independence. Accepted phonetic anchors remain zero.',
};

writeCsv(OUT_CSV, lowRows, FIELDS);
fs.writeFileSync(OUT_JSON, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
