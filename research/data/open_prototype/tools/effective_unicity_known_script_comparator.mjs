// How good is our masked-sign predictor, really? A raw accuracy number on an
// unread script means little without a yardstick. This script builds that
// yardstick by lining up the Indus effective-unicity results against Linear B
// Series D — a known, readable script whose readings we hid from the model —
// under the same IVC p95 length cap. It reads five earlier report files (the
// Indus degeneracy summary and curve, the Linear B scarcity, gapped-heldout,
// and control outputs), pulls the top-1/top-5/MRR numbers from each, and adds
// a label-symmetry cost (log2 of the factorial of the sign inventory size —
// the bits needed to pin down which sign is which). It writes one comparison
// table as both CSV and JSON to data/open_prototype/reports/. This is
// calibration only: it says how the Indus numbers compare to a known script
// under matched scarcity, not what any Indus sign means.
import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const ivcSummaryPath = path.join(reportsDir, 'effective_unicity_degeneracy_summary.json');
const ivcCurvePath = path.join(reportsDir, 'effective_unicity_degeneracy_curve.csv');
const linearBScarcityPath = path.join(reportsDir, 'linear_b_series_d_scarcity_summary.json');
const linearBGappedPath = path.join(reportsDir, 'linear_b_series_d_gapped_heldout_summary.json');
const linearBControlPath = path.join(reportsDir, 'linear_b_series_d_control_summary.csv');

const outJson = path.join(reportsDir, 'effective_unicity_known_script_comparator_summary.json');
const outCsv = path.join(reportsDir, 'effective_unicity_known_script_comparator.csv');

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQuotes) {
      if (c === '"') {
        if (text[i + 1] === '"') {
          field += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        field += c;
      }
    } else if (c === '"') {
      inQuotes = true;
    } else if (c === ',') {
      row.push(field);
      field = '';
    } else if (c === '\n') {
      row.push(field);
      field = '';
      if (row.length > 1 || row[0] !== '') rows.push(row);
      row = [];
    } else if (c !== '\r') {
      field += c;
    }
  }
  if (field.length || row.length) {
    row.push(field);
    rows.push(row);
  }
  return rows;
}

function loadCsv(filePath) {
  const rows = parseCsv(fs.readFileSync(filePath, 'utf8'));
  const header = rows[0] ?? [];
  return rows.slice(1).map((row) => Object.fromEntries(header.map((name, index) => [name, row[index] ?? ''])));
}

function toCsv(rows) {
  return `${rows
    .map((row) =>
      row
        .map((value) => {
          const text = String(value ?? '');
          return `"${text.replaceAll('"', '""')}"`;
        })
        .join(','),
    )
    .join('\n')}\n`;
}

function log2Factorial(n) {
  let out = 0;
  for (let i = 2; i <= n; i++) out += Math.log2(i);
  return out;
}

function fmt(value, digits = 6) {
  return value === null || value === undefined || Number.isNaN(Number(value))
    ? null
    : Number(Number(value).toFixed(digits));
}

function maxNullGeObserved(rows, metric) {
  const values = rows
    .filter((row) => row.metric === metric)
    .map((row) => Number(row.null_ge_observed_share))
    .filter((value) => !Number.isNaN(value));
  return values.length ? Math.max(...values) : null;
}

const ivcSummary = JSON.parse(fs.readFileSync(ivcSummaryPath, 'utf8'));
const ivcCurve = loadCsv(ivcCurvePath);
const linearBScarcity = JSON.parse(fs.readFileSync(linearBScarcityPath, 'utf8'));
const linearBGapped = JSON.parse(fs.readFileSync(linearBGappedPath, 'utf8'));
const linearBControls = loadCsv(linearBControlPath).filter(
  (row) => row.tokenization === 'sign_tokens' && row.scope === 'real_series_d_513_ivc_p95_length_cap',
);

const ivcFull = ivcSummary.primary_full_coverage;
const linearBIvc = linearBScarcity.ivc_like_length_cap;
const linearBGappedSeq =
  linearBGapped.primary_results.ivc_p95_length_cap_gapped_rows__sequence_leave_one_out;
const linearBGappedRow = linearBGapped.primary_results.ivc_p95_length_cap_gapped_rows__row_leave_one_out;

const comparatorRows = [
  {
    system: 'Indus_Lipi_strict_exact_sequence_collapsed',
    experiment: 'leave_one_row_out_masked_sign',
    rows: ivcFull.rows,
    tokens_or_gaps: ivcFull.masked_tokens,
    unique_signs_or_tokens: ivcFull.unique_signs,
    label_symmetry_log2_bits: ivcFull.label_symmetry_log2_bits,
    top1: ivcFull.masked_top1_accuracy,
    top5: ivcFull.masked_top5_accuracy,
    mrr: ivcFull.masked_mrr,
    median_rank: '',
    max_control_fpr_or_null_ge_observed: 0,
    boundary: 'unread script; internal labels only; no source-normalized value anchor',
  },
  {
    system: 'Linear_B_Series_D_IVC_length_cap',
    experiment: 'clean_masked_bidirectional_bigram',
    rows: linearBIvc.rows,
    tokens_or_gaps: 1755,
    unique_signs_or_tokens: linearBIvc.unique_tokens,
    label_symmetry_log2_bits: log2Factorial(linearBIvc.unique_tokens),
    top1: linearBIvc.bidirectional_top1_accuracy,
    top5: linearBIvc.bidirectional_top5_accuracy,
    mrr: '',
    median_rank: '',
    max_control_fpr_or_null_ge_observed: maxNullGeObserved(linearBControls, 'bidirectional_top1_accuracy'),
    boundary: 'known script with readings hidden; scarcity comparator only',
  },
  {
    system: 'Linear_B_Series_D_IVC_length_cap',
    experiment: 'source_provided_gapped_sequence_leave_one_out',
    rows: linearBGapped.ivc_like_length_cap.eligible_gapped_rows,
    tokens_or_gaps: linearBGappedSeq.evaluated_gaps,
    unique_signs_or_tokens: linearBIvc.unique_tokens,
    label_symmetry_log2_bits: log2Factorial(linearBIvc.unique_tokens),
    top1: linearBGappedSeq.top1_accuracy,
    top5: linearBGappedSeq.top5_accuracy,
    mrr: linearBGappedSeq.mrr,
    median_rank: linearBGappedSeq.median_rank,
    max_control_fpr_or_null_ge_observed: '',
    boundary: 'known script source gaps; exact duplicate sequences removed from training',
  },
  {
    system: 'Linear_B_Series_D_IVC_length_cap',
    experiment: 'source_provided_gapped_row_leave_one_out',
    rows: linearBGapped.ivc_like_length_cap.eligible_gapped_rows,
    tokens_or_gaps: linearBGappedRow.evaluated_gaps,
    unique_signs_or_tokens: linearBIvc.unique_tokens,
    label_symmetry_log2_bits: log2Factorial(linearBIvc.unique_tokens),
    top1: linearBGappedRow.top1_accuracy,
    top5: linearBGappedRow.top5_accuracy,
    mrr: linearBGappedRow.mrr,
    median_rank: linearBGappedRow.median_rank,
    max_control_fpr_or_null_ge_observed: '',
    boundary: 'known script source gaps; only target row removed from training',
  },
];

const summary = {
  date: '2026-05-29',
  purpose:
    'Known-script scarcity calibration for the Vector 2 effective-unicity instrument. This is comparator evidence, not a decipherment.',
  source_files: {
    indus_effective_unicity: ivcSummaryPath,
    indus_curve: ivcCurvePath,
    linear_b_scarcity: linearBScarcityPath,
    linear_b_gapped: linearBGappedPath,
    linear_b_controls: linearBControlPath,
  },
  linear_b_source: {
    source_file: linearBGapped.source_file,
    source_md5: linearBGapped.source_md5,
    source_md5_verified: linearBGapped.source_md5_verified,
    doi: '10.5281/zenodo.7404653',
  },
  primary_comparison: {
    indus_masked_top1: fmt(ivcFull.masked_top1_accuracy),
    indus_masked_top5: fmt(ivcFull.masked_top5_accuracy),
    indus_unique_signs: ivcFull.unique_signs,
    indus_label_symmetry_log2_bits: fmt(ivcFull.label_symmetry_log2_bits),
    linear_b_clean_ivc_cap_bidirectional_top1: fmt(linearBIvc.bidirectional_top1_accuracy),
    linear_b_clean_ivc_cap_bidirectional_top5: fmt(linearBIvc.bidirectional_top5_accuracy),
    linear_b_gapped_sequence_loo_top1: fmt(linearBGappedSeq.top1_accuracy),
    linear_b_gapped_sequence_loo_top5: fmt(linearBGappedSeq.top5_accuracy),
    linear_b_ivc_cap_unique_tokens: linearBIvc.unique_tokens,
    linear_b_ivc_cap_label_symmetry_log2_bits: fmt(log2Factorial(linearBIvc.unique_tokens)),
    linear_b_bidirectional_top1_control_max_null_ge_observed: maxNullGeObserved(
      linearBControls,
      'bidirectional_top1_accuracy',
    ),
  },
  interpretation: {
    structural_calibration:
      'Indus masked top-1 is close to the Linear B source-gapped sequence-leave-one-out top-1 under the same IVC p95 length cap, but below the clean Linear B bidirectional masked score and with a much larger sign inventory and label-symmetry burden.',
    adversarial_boundary:
      'This improves the Vector 2 methods note by calibrating scale against a known readable script hidden from the model. It does not identify any Indus sign, sound, word, language family, or semantic field.',
    acceptance_status:
      'Comparator evidence strengthens the live structural candidate but does not increment accepted_claim_counts because the Indus side still uses the T3 Lipi metadata layer and lacks source-image normalization and an external value anchor.',
  },
  rows: comparatorRows.map((row) => ({
    ...row,
    label_symmetry_log2_bits: fmt(row.label_symmetry_log2_bits),
    top1: fmt(row.top1),
    top5: fmt(row.top5),
    mrr: row.mrr === '' ? '' : fmt(row.mrr),
    max_control_fpr_or_null_ge_observed:
      row.max_control_fpr_or_null_ge_observed === '' ? '' : fmt(row.max_control_fpr_or_null_ge_observed),
  })),
};

fs.writeFileSync(
  outCsv,
  toCsv([
    [
      'system',
      'experiment',
      'rows',
      'tokens_or_gaps',
      'unique_signs_or_tokens',
      'label_symmetry_log2_bits',
      'top1',
      'top5',
      'mrr',
      'median_rank',
      'max_control_fpr_or_null_ge_observed',
      'boundary',
    ],
    ...summary.rows.map((row) => [
      row.system,
      row.experiment,
      row.rows,
      row.tokens_or_gaps,
      row.unique_signs_or_tokens,
      row.label_symmetry_log2_bits,
      row.top1,
      row.top5,
      row.mrr,
      row.median_rank,
      row.max_control_fpr_or_null_ge_observed,
      row.boundary,
    ]),
  ]),
);
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
