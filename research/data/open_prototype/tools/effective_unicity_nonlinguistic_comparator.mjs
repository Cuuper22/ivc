// A predictable symbol system is not automatically a language. Bookkeeping
// codes and emblem sequences can look statistically ordered too. This script
// merges three earlier reports — the effective-unicity degeneracy summary,
// the simple synthetic shuffle comparators, and the structured nonlinguistic
// forgers (administrative/emblem generators) — into one verdict table. It
// splits the evidence in two: the masked-sign top-1 metric, which no tested
// forger has matched (so it survives as a local-constraint signal), and the
// older broad bidirectional predictability metric, which structured forgers
// can equal or beat (so it is rejected as decipherment evidence). No new
// computation happens here beyond picking maxima across the null controls;
// the output is a JSON summary and CSV of per-control null rows in
// data/open_prototype/reports/.
import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const effectivePath = path.join(reportsDir, 'effective_unicity_degeneracy_summary.json');
const syntheticPath = path.join(reportsDir, 'lipi_synthetic_comparator_summary.json');
const structuredPath = path.join(reportsDir, 'lipi_structured_null_summary.json');
const outJson = path.join(reportsDir, 'effective_unicity_nonlinguistic_comparator_summary.json');
const outCsv = path.join(reportsDir, 'effective_unicity_nonlinguistic_comparator.csv');

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
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

function formatNumber(value) {
  return value === null || value === undefined || Number.isNaN(value) ? null : Number(value.toFixed(6));
}

function findRows(summary, metrics) {
  return summary.null_summary.filter((row) => metrics.includes(row.metric));
}

function maxValue(rows, key) {
  return rows.length ? Math.max(...rows.map((row) => Number(row[key] ?? 0))) : null;
}

function summarizeRows(summary, family, metrics) {
  return findRows(summary, metrics).map((row) => ({
    family,
    control: row.control,
    metric: row.metric,
    iterations: row.iterations,
    observed_value: row.observed_value,
    null_mean: row.null_mean,
    null_p05: row.null_p05,
    null_median: row.null_median,
    null_p95: row.null_p95,
    null_max: row.null_max,
    observed_minus_null_mean: row.observed_minus_null_mean,
    null_ge_observed_share: row.null_ge_observed_share,
    null_le_observed_share: row.null_le_observed_share,
  }));
}

const effective = readJson(effectivePath);
const synthetic = readJson(syntheticPath);
const structured = readJson(structuredPath);

const maskedTop1Rows = effective.full_coverage_false_positive_rates.filter(
  (row) => row.coverage_fraction === 1 && row.metric === 'masked_top1_accuracy',
);

const broadMetrics = ['bidirectional_top1_accuracy', 'bidirectional_top5_accuracy', 'stored_higher_share'];
const syntheticRows = summarizeRows(synthetic, 'simple_matched_shuffles', broadMetrics);
const structuredRows = summarizeRows(structured, 'structured_nonlinguistic_codes', broadMetrics);
const broadRows = [...syntheticRows, ...structuredRows];

const structuredBidirectionalTop1 = structuredRows.filter((row) => row.metric === 'bidirectional_top1_accuracy');
const syntheticBidirectionalTop1 = syntheticRows.filter((row) => row.metric === 'bidirectional_top1_accuracy');

const summary = {
  date: '2026-05-29',
  generated_at_utc: new Date().toISOString(),
  purpose:
    'Integrate nonlinguistic comparator evidence for Vector 2. This separates a surviving masked-sign local-constraint metric from broad predictability metrics that structured administrative/emblem forgers can mimic or exceed.',
  source_files: {
    effective_unicity: path.relative(base, effectivePath).replaceAll('\\', '/'),
    simple_synthetic_comparators: path.relative(base, syntheticPath).replaceAll('\\', '/'),
    structured_nonlinguistic_comparators: path.relative(base, structuredPath).replaceAll('\\', '/'),
  },
  corpus_scope: {
    source_rows: effective.source_rows,
    exact_collapsed_rows: effective.exact_collapsed_rows,
    tokens: effective.primary_full_coverage.tokens,
    unique_signs: effective.primary_full_coverage.unique_signs,
    label_symmetry_log2_bits: formatNumber(effective.primary_full_coverage.label_symmetry_log2_bits),
  },
  effective_unicity_masked_top1: {
    metric: 'leave-one-row-out masked-sign top-1 accuracy',
    observed: formatNumber(effective.primary_full_coverage.masked_top1_accuracy),
    null_iterations_per_control: effective.iterations_per_control,
    null_masked_sample_limit: effective.null_masked_sample_limit,
    max_recorded_false_positive_rate: maxValue(maskedTop1Rows, 'false_positive_rate'),
    controls: maskedTop1Rows.map((row) => ({
      control: row.control,
      null_mean: formatNumber(row.null_mean),
      null_p95: formatNumber(row.null_p95),
      null_max: formatNumber(row.null_max),
      false_positive_rate: row.false_positive_rate,
    })),
    decision:
      'Survives the current specified masked-sign forger gate as local context constraint. This does not identify sounds, meanings, language family, or translations.',
  },
  broad_bidirectional_predictability: {
    metric: 'bidirectional top-1 accuracy from the older broad local predictor',
    observed: formatNumber(synthetic.observed.bidirectional_top1_accuracy),
    simple_shuffle_max_null_ge_observed_share: maxValue(syntheticBidirectionalTop1, 'null_ge_observed_share'),
    structured_nonlinguistic_max_null_ge_observed_share: maxValue(
      structuredBidirectionalTop1,
      'null_ge_observed_share',
    ),
    structured_nonlinguistic_controls: structuredBidirectionalTop1.map((row) => ({
      control: row.control,
      null_mean: formatNumber(row.null_mean),
      null_p05: formatNumber(row.null_p05),
      null_median: formatNumber(row.null_median),
      null_p95: formatNumber(row.null_p95),
      null_ge_observed_share: row.null_ge_observed_share,
    })),
    decision:
      'Rejected as language-identification or semantic evidence. Administrative, emblem, and mixed nonlinguistic generators equal or exceed the observed broad bidirectional top-1 score in every rerun iteration.',
  },
  adversarial_boundary: [
    'Simple shuffles are too weak as nonlinguistic adversaries; passing them is not enough.',
    'Structured administrative and emblem forgers can produce stronger broad predictability than the real corpus, so broad predictability is not a decipherment signal.',
    'The remaining Vector 2 candidate is narrower: masked-sign local constraint survives the current tested controls, while unanchored label symmetry still blocks phonetic and language-family claims.',
    'No accepted claim count changes follow from this comparator integration.',
  ],
  rows: broadRows,
  artifact_files: [
    'data/open_prototype/reports/effective_unicity_nonlinguistic_comparator_summary.json',
    'data/open_prototype/reports/effective_unicity_nonlinguistic_comparator.csv',
  ],
};

const csvRows = [
  [
    'family',
    'control',
    'metric',
    'iterations',
    'observed_value',
    'null_mean',
    'null_p05',
    'null_median',
    'null_p95',
    'null_max',
    'observed_minus_null_mean',
    'null_ge_observed_share',
    'null_le_observed_share',
  ],
  ...broadRows.map((row) => [
    row.family,
    row.control,
    row.metric,
    row.iterations,
    row.observed_value,
    row.null_mean,
    row.null_p05,
    row.null_median,
    row.null_p95,
    row.null_max,
    row.observed_minus_null_mean,
    row.null_ge_observed_share,
    row.null_le_observed_share,
  ]),
];

fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);
fs.writeFileSync(outCsv, toCsv(csvRows));

console.log(
  JSON.stringify(
    {
      wrote: summary.artifact_files,
      masked_top1_observed: summary.effective_unicity_masked_top1.observed,
      masked_top1_max_fpr: summary.effective_unicity_masked_top1.max_recorded_false_positive_rate,
      broad_bidirectional_observed: summary.broad_bidirectional_predictability.observed,
      structured_broad_top1_max_fpr: summary.broad_bidirectional_predictability.structured_nonlinguistic_max_null_ge_observed_share,
    },
    null,
    2,
  ),
);
