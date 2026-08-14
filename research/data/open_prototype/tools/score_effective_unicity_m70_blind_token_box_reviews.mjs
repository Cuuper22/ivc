// Scores blind reviews for the M-70 order-window pilot. Reviewers judged
// seal images under blind IDs, calling yes/no/uncertain on whether the
// target sign relation is present. The packet mixes real targets, positive
// calibrators (planted easy positives that competent reviewers should
// catch), scoring negatives (where "yes" is a false positive), and
// quarantined negatives kept out of the false-positive denominator. This
// script joins each review CSV (CLI arguments, or the default reviews
// directory) against the answer key, tallies outcomes per reviewer, and
// computes target recovery rates plus yes-only and conservative false-
// positive rates. The gate fails on fewer than two reviewers, any target
// not strictly recovered, or any hard hit on a scoring negative — and even
// a pass adds zero accepted claims. Writes a JSON summary and a scored-rows
// CSV; with no reviews present it writes a not-scored summary and exits.
import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const keyPath = path.join(reportsDir, 'effective_unicity_m70_blind_token_box_answer_key.csv');
const defaultReviewDir = path.join(reportsDir, 'effective_unicity_m70_blind_reviews');
const outSummary = path.join(reportsDir, 'effective_unicity_m70_blind_token_box_review_summary.json');
const outRows = path.join(reportsDir, 'effective_unicity_m70_blind_token_box_scored_rows.csv');

const reviewArgs = process.argv.slice(2);
const reviewPaths = reviewArgs.length
  ? reviewArgs.map((arg) => path.resolve(base, arg))
  : fs.existsSync(defaultReviewDir)
    ? fs
        .readdirSync(defaultReviewDir)
        .filter((name) => name.toLowerCase().endsWith('.csv'))
        .map((name) => path.join(defaultReviewDir, name))
        .sort((a, b) => a.localeCompare(b))
    : [];

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

function normalizeCall(value) {
  const text = String(value ?? '').trim().toLowerCase();
  if (['yes', 'y', 'true', 'present', 'target_present', '1'].includes(text)) return 'yes';
  if (['no', 'n', 'false', 'absent', 'target_absent', '0'].includes(text)) return 'no';
  if (['uncertain', 'unknown', 'maybe', 'ambiguous', '?'].includes(text)) return 'uncertain';
  return text || 'missing';
}

function reviewerName(filePath) {
  return path.basename(filePath).replace(/\.csv$/i, '');
}

function rate(numerator, denominator) {
  return denominator ? numerator / denominator : null;
}

function roleClass(row) {
  const role = row.control_role ?? '';
  if (role.startsWith('primary_target')) return 'target';
  if (role.startsWith('positive_calibrator')) return 'positive_calibrator';
  if (role === 'scoring_negative') return 'scoring_negative';
  if (role.startsWith('quarantine_negative')) return 'quarantine_negative';
  return 'other';
}

const keyRows = loadCsv(keyPath);
const keyByBlindId = new Map(keyRows.map((row) => [row.blind_id, row]));
const scoredRows = [];
const reviewerSummaries = [];

if (!reviewPaths.length) {
  const summary = {
    date: '2026-05-29',
    packet_id: 'm70_order_window_pilot_v1',
    status: 'not_scored_no_review_csvs_found',
    key_path: keyPath,
    review_dir: defaultReviewDir,
    reviewer_count: 0,
    accepted_claims_increment: 0,
    interpretation_boundary:
      'The blind packet has not been reviewed. No false-positive rate, target recovery rate, source-boxed order-window promotion, or accepted claim follows.',
  };
  fs.mkdirSync(path.dirname(outSummary), { recursive: true });
  fs.writeFileSync(outSummary, `${JSON.stringify(summary, null, 2)}\n`);
  fs.writeFileSync(
    outRows,
    toCsv([['reviewer', 'blind_id', 'cisi', 'role_class', 'call', 'outcome', 'confidence', 'notes']]),
  );
  console.log(JSON.stringify(summary, null, 2));
  process.exit(0);
}

for (const reviewPath of reviewPaths) {
  const name = reviewerName(reviewPath);
  const reviewRows = loadCsv(reviewPath);
  const reviewIds = new Set();
  const counts = {
    target_yes: 0,
    target_no: 0,
    target_uncertain: 0,
    positive_calibrator_yes: 0,
    positive_calibrator_no: 0,
    positive_calibrator_uncertain: 0,
    scoring_negative_yes: 0,
    scoring_negative_no: 0,
    scoring_negative_uncertain: 0,
    quarantine_yes: 0,
    quarantine_no: 0,
    quarantine_uncertain: 0,
    missing: 0,
  };

  for (const reviewRow of reviewRows) {
    const blindId = reviewRow.blind_id;
    if (!blindId) continue;
    reviewIds.add(blindId);
    const key = keyByBlindId.get(blindId);
    if (!key) throw new Error(`Review ${name} contains unknown blind_id ${blindId}`);
    const role = roleClass(key);
    const call = normalizeCall(
      reviewRow.stage2_target_relation_present_yes_no_uncertain ??
        reviewRow.call_yes_no_uncertain ??
        reviewRow.call ??
        reviewRow.judgment,
    );

    let outcome = 'not_scored';
    if (role === 'target') {
      if (call === 'yes') {
        counts.target_yes++;
        outcome = 'target_recovered';
      } else if (call === 'no') {
        counts.target_no++;
        outcome = 'target_missed';
      } else {
        counts.target_uncertain++;
        outcome = 'target_uncertain';
      }
    } else if (role === 'positive_calibrator') {
      if (call === 'yes') {
        counts.positive_calibrator_yes++;
        outcome = 'calibrator_recovered';
      } else if (call === 'no') {
        counts.positive_calibrator_no++;
        outcome = 'calibrator_missed';
      } else {
        counts.positive_calibrator_uncertain++;
        outcome = 'calibrator_uncertain';
      }
    } else if (role === 'scoring_negative') {
      if (call === 'yes') {
        counts.scoring_negative_yes++;
        outcome = 'false_positive_scoring_negative';
      } else if (call === 'no') {
        counts.scoring_negative_no++;
        outcome = 'true_negative_scoring_negative';
      } else {
        counts.scoring_negative_uncertain++;
        outcome = 'uncertain_scoring_negative';
      }
    } else if (role === 'quarantine_negative') {
      if (call === 'yes') counts.quarantine_yes++;
      else if (call === 'no') counts.quarantine_no++;
      else counts.quarantine_uncertain++;
      outcome = `quarantine_${call}`;
    }

    scoredRows.push([
      name,
      blindId,
      key.cisi,
      role,
      call,
      outcome,
      reviewRow.stage2_confidence ?? reviewRow.confidence ?? '',
      reviewRow.stage2_notes ?? reviewRow.stage1_uncertainty_notes ?? reviewRow.notes ?? '',
    ]);
  }

  const missingIds = [...keyByBlindId.keys()].filter((blindId) => !reviewIds.has(blindId));
  counts.missing += missingIds.length;
  for (const blindId of missingIds) {
    const key = keyByBlindId.get(blindId);
    scoredRows.push([name, blindId, key.cisi, roleClass(key), 'missing', 'missing_review_row', '', '']);
  }

  reviewerSummaries.push({
    reviewer: name,
    review_path: reviewPath,
    rows_expected: keyRows.length,
    rows_reviewed: reviewIds.size,
    ...counts,
    target_recovery_rate: rate(counts.target_yes, counts.target_yes + counts.target_no),
    target_strict_recovery_rate: rate(
      counts.target_yes,
      counts.target_yes + counts.target_no + counts.target_uncertain,
    ),
    positive_calibrator_strict_recovery_rate: rate(
      counts.positive_calibrator_yes,
      counts.positive_calibrator_yes + counts.positive_calibrator_no + counts.positive_calibrator_uncertain,
    ),
    scoring_negative_yes_only_false_positive_rate: rate(
      counts.scoring_negative_yes,
      counts.scoring_negative_yes + counts.scoring_negative_no,
    ),
    scoring_negative_conservative_false_positive_or_uncertain_rate: rate(
      counts.scoring_negative_yes + counts.scoring_negative_uncertain,
      counts.scoring_negative_yes + counts.scoring_negative_no + counts.scoring_negative_uncertain,
    ),
  });
}

const hardFpRates = reviewerSummaries
  .map((row) => row.scoring_negative_yes_only_false_positive_rate)
  .filter((value) => value !== null);
const conservativeFpRates = reviewerSummaries
  .map((row) => row.scoring_negative_conservative_false_positive_or_uncertain_rate)
  .filter((value) => value !== null);
const targetRates = reviewerSummaries.map((row) => row.target_recovery_rate).filter((value) => value !== null);
const strictTargetRates = reviewerSummaries.map((row) => row.target_strict_recovery_rate).filter((value) => value !== null);

const failedReasons = [];
if (reviewerSummaries.length < 2) {
  failedReasons.push('fewer_than_two_independent_reviews');
}
if (strictTargetRates.some((value) => value < 1)) {
  failedReasons.push('not_all_targets_strictly_recovered');
}
if (reviewerSummaries.some((row) => row.scoring_negative_yes > 0)) {
  failedReasons.push('scoring_negatives_produced_hard_target_like_hits');
}

const summary = {
  date: '2026-05-29',
  packet_id: 'm70_order_window_pilot_v1',
  status: 'scored_reviews_present_not_acceptance_by_itself',
  key_path: keyPath,
  review_paths: reviewPaths,
  reviewer_count: reviewerSummaries.length,
  reviewer_summaries: reviewerSummaries,
  min_target_recovery_rate: targetRates.length ? Math.min(...targetRates) : null,
  min_target_strict_recovery_rate: strictTargetRates.length ? Math.min(...strictTargetRates) : null,
  max_scoring_negative_yes_only_false_positive_rate: hardFpRates.length ? Math.max(...hardFpRates) : null,
  max_scoring_negative_conservative_false_positive_or_uncertain_rate: conservativeFpRates.length
    ? Math.max(...conservativeFpRates)
    : null,
  promotion_gate_decision: failedReasons.length ? 'failed_packet_gate_no_promotion' : 'passes_packet_gate_no_claim_increment',
  promotion_gate_failed_reasons: failedReasons,
  accepted_claims_increment: 0,
  interpretation_boundary:
    'Scoring this packet can only measure target recovery and false-positive behavior for the M-70 order-window gate. It cannot assign signs, sounds, meanings, language, translation, or accepted structural status.',
};

fs.mkdirSync(path.dirname(outRows), { recursive: true });
fs.writeFileSync(
  outRows,
  toCsv([['reviewer', 'blind_id', 'cisi', 'role_class', 'call', 'outcome', 'confidence', 'notes'], ...scoredRows]),
);
fs.writeFileSync(outSummary, `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
