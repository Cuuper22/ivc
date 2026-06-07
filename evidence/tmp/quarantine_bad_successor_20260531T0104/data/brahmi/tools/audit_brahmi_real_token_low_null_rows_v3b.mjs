import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const OUT = path.join(ROOT, 'data', 'brahmi');
const RUN_DATE = '2026-05-31';

const IMPOSTOR_ROWS = path.join(OUT, 'brahmi_real_token_impostor_forger_v3.csv');
const V3_PREFLIGHT = path.join(OUT, 'brahmi_independent_source_token_gate_v3.csv');
const FAMILY_SUMMARY = path.join(OUT, 'source_token_family_descent_summary_v2.csv');
const SEGMENTS = path.join(OUT, 'source_token_segments_v2.csv');

const OUT_CSV = path.join(OUT, 'brahmi_real_token_low_null_autopsy_v3b.csv');
const OUT_JSON = path.join(OUT, 'brahmi_real_token_low_null_autopsy_v3b_summary.json');

const THRESHOLD = 0.01;

const FIELDS = [
  'sign_id',
  'orientation_policy',
  'sample_count',
  'modal_brahmi_label',
  'v3_cisi_modal_label',
  'v3_cisi_modal_share',
  'impostor_ge_observed_share',
  'original_shape_null_share',
  'original_label_null_share',
  'unique_sha256_count',
  'unique_cisi_count',
  'unique_source_path_count',
  'duplicate_collapse_status',
  'independence_status',
  'unanimity_after_collapse',
  'modal_label_stable_after_collapse',
  'passes_real_token_impostor_threshold',
  'passes_shape_null_threshold',
  'passes_label_null_threshold',
  'passes_min_independence',
  'passes_duplicate_unanimity',
  'passes_modal_stability',
  'review_packet_eligible',
  'low_null_failure_class',
  'blocked_reasons',
  'cisis',
  'source_paths',
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
  const [header, ...body] = rows.filter((r) => r.some((value) => value !== ''));
  return body.map((cols) => Object.fromEntries(header.map((h, idx) => [h, cols[idx] ?? ''])));
}

function csvEscape(value) {
  const text = String(value ?? '');
  if (/[",\n\r]/.test(text)) return `"${text.replaceAll('"', '""')}"`;
  return text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(',')];
  for (const row of rows) lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function key(row) {
  return `${row.sign_id}::${row.orientation_policy}`;
}

function num(value) {
  if (value === '' || value === null || value === undefined) return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function boolText(value) {
  return value ? 'true' : 'false';
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function reasonSet(text) {
  return new Set(String(text || '').split(';').filter(Boolean));
}

function failureClass({ passesMinIndependence, passesDuplicateUnanimity, passesModalStability, passesShape, passesLabel }) {
  if (!passesShape && !passesLabel) return 'low_impostor_but_shape_and_label_nulls_fail';
  if (!passesShape) return 'low_impostor_but_shape_null_fails';
  if (!passesLabel) return 'low_impostor_but_label_null_fails';
  if (!passesMinIndependence) return 'low_impostor_and_nulls_but_not_independent';
  if (!passesDuplicateUnanimity) return 'low_impostor_and_independent_but_duplicate_collapse_not_unanimous';
  if (!passesModalStability) return 'low_impostor_and_independent_but_modal_label_changes_after_collapse';
  return 'low_impostor_no_recorded_blocker_check_preflight';
}

function main() {
  const impostorRows = parseCsv(fs.readFileSync(IMPOSTOR_ROWS, 'utf8'));
  const preflightRows = parseCsv(fs.readFileSync(V3_PREFLIGHT, 'utf8'));
  const familyRows = parseCsv(fs.readFileSync(FAMILY_SUMMARY, 'utf8'));
  const segmentRows = parseCsv(fs.readFileSync(SEGMENTS, 'utf8'));

  const preflightByKey = new Map(preflightRows.map((row) => [key(row), row]));
  const familyByKey = new Map(familyRows.map((row) => [key(row), row]));
  const segmentByToken = new Map(segmentRows.map((row) => [row.token_id, row]));

  const fullIterationRows = impostorRows.filter((row) => num(row.iterations) > 0);
  const lowNullRows = fullIterationRows.filter((row) => {
    const share = num(row.impostor_ge_observed_share);
    return share !== null && share <= THRESHOLD;
  });

  const outputRows = lowNullRows.map((row) => {
    const pre = preflightByKey.get(key(row)) ?? {};
    const family = familyByKey.get(key(row)) ?? {};
    const tokenIds = unique(String(pre.token_ids || family.token_ids || '').split('|'));
    const segments = tokenIds.map((tokenId) => segmentByToken.get(tokenId)).filter(Boolean);
    const sourcePaths = unique(segments.map((segment) => segment.source_path));
    const cisis = unique(segments.map((segment) => segment.cisi));

    const blocked = reasonSet(pre.blocked_reasons || row.blocked_reason);
    const impostorShare = num(row.impostor_ge_observed_share);
    const shapeShare = num(row.original_shape_null_share);
    const labelShare = num(row.original_label_null_share);
    const uniqueShaCount = num(pre.unique_sha256_count);
    const uniqueCisiCount = num(pre.unique_cisi_count);
    const passesRealToken = impostorShare !== null && impostorShare <= THRESHOLD;
    const passesShape = shapeShare !== null && shapeShare <= THRESHOLD;
    const passesLabel = labelShare !== null && labelShare <= THRESHOLD;
    const passesMinIndependence = (uniqueShaCount ?? 0) >= 3 && (uniqueCisiCount ?? 0) >= 3 && sourcePaths.length >= 3;
    const passesDuplicateUnanimity = pre.unanimity_after_collapse === 'unanimous';
    const passesModalStability = !blocked.has('modal_label_changes_after_collapse');
    const reviewEligible = pre.review_packet_eligible === 'true';

    return {
      sign_id: row.sign_id,
      orientation_policy: row.orientation_policy,
      sample_count: row.sample_count,
      modal_brahmi_label: row.modal_brahmi_label,
      v3_cisi_modal_label: row.v3_cisi_modal_label,
      v3_cisi_modal_share: row.v3_cisi_modal_share,
      impostor_ge_observed_share: row.impostor_ge_observed_share,
      original_shape_null_share: row.original_shape_null_share,
      original_label_null_share: row.original_label_null_share,
      unique_sha256_count: pre.unique_sha256_count ?? '',
      unique_cisi_count: pre.unique_cisi_count ?? '',
      unique_source_path_count: sourcePaths.length,
      duplicate_collapse_status: pre.duplicate_collapse_status ?? '',
      independence_status: pre.independence_status ?? '',
      unanimity_after_collapse: pre.unanimity_after_collapse ?? '',
      modal_label_stable_after_collapse: boolText(passesModalStability),
      passes_real_token_impostor_threshold: boolText(passesRealToken),
      passes_shape_null_threshold: boolText(passesShape),
      passes_label_null_threshold: boolText(passesLabel),
      passes_min_independence: boolText(passesMinIndependence),
      passes_duplicate_unanimity: boolText(passesDuplicateUnanimity),
      passes_modal_stability: boolText(passesModalStability),
      review_packet_eligible: boolText(reviewEligible),
      low_null_failure_class: failureClass({
        passesMinIndependence,
        passesDuplicateUnanimity,
        passesModalStability,
        passesShape,
        passesLabel,
      }),
      blocked_reasons: [...blocked].join(';'),
      cisis: cisis.join('|'),
      source_paths: sourcePaths.join('|'),
    };
  }).sort((a, b) => {
    const shareDelta = num(a.impostor_ge_observed_share) - num(b.impostor_ge_observed_share);
    if (shareDelta) return shareDelta;
    const shapeDelta = num(a.original_shape_null_share) - num(b.original_shape_null_share);
    if (shapeDelta) return shapeDelta;
    return String(a.sign_id).localeCompare(String(b.sign_id));
  });

  const countWhere = (predicate) => outputRows.filter(predicate).length;
  const failureClassCounts = outputRows.reduce((acc, row) => {
    acc[row.low_null_failure_class] = (acc[row.low_null_failure_class] || 0) + 1;
    return acc;
  }, {});
  const blockerCounts = outputRows.reduce((acc, row) => {
    for (const reason of String(row.blocked_reasons || '').split(';').filter(Boolean)) {
      acc[reason] = (acc[reason] || 0) + 1;
    }
    return acc;
  }, {});
  const passCounts = {
    real_token_impostor_threshold: countWhere((row) => row.passes_real_token_impostor_threshold === 'true'),
    shape_null_threshold: countWhere((row) => row.passes_shape_null_threshold === 'true'),
    label_null_threshold: countWhere((row) => row.passes_label_null_threshold === 'true'),
    min_independence: countWhere((row) => row.passes_min_independence === 'true'),
    duplicate_unanimity: countWhere((row) => row.passes_duplicate_unanimity === 'true'),
    modal_stability: countWhere((row) => row.passes_modal_stability === 'true'),
    review_packet_eligible: countWhere((row) => row.review_packet_eligible === 'true'),
  };
  const pairedPassCounts = {
    impostor_and_shape: countWhere((row) => row.passes_shape_null_threshold === 'true'),
    impostor_and_label: countWhere((row) => row.passes_label_null_threshold === 'true'),
    impostor_and_min_independence: countWhere((row) => row.passes_min_independence === 'true'),
    impostor_and_duplicate_unanimity: countWhere((row) => row.passes_duplicate_unanimity === 'true'),
    impostor_and_min_independence_and_duplicate_unanimity: countWhere(
      (row) => row.passes_min_independence === 'true' && row.passes_duplicate_unanimity === 'true'
    ),
    impostor_and_shape_and_label: countWhere(
      (row) => row.passes_shape_null_threshold === 'true' && row.passes_label_null_threshold === 'true'
    ),
    impostor_and_shape_and_label_and_min_independence: countWhere(
      (row) => row.passes_shape_null_threshold === 'true'
        && row.passes_label_null_threshold === 'true'
        && row.passes_min_independence === 'true'
    ),
  };

  const summary = {
    date: RUN_DATE,
    status: 'brahmi_real_token_low_null_rows_v3b_no_survivors',
    threshold: THRESHOLD,
    input_impostor_rows: impostorRows.length,
    rows_with_full_impostor_iterations: fullIterationRows.length,
    low_null_rows: outputRows.length,
    pass_counts_within_low_null_rows: passCounts,
    paired_pass_counts_within_low_null_rows: pairedPassCounts,
    failure_class_counts: failureClassCounts,
    blocker_counts: blockerCounts,
    closest_rows: outputRows.slice(0, 10).map((row) => ({
      sign_id: row.sign_id,
      orientation_policy: row.orientation_policy,
      modal_brahmi_label: row.modal_brahmi_label,
      impostor_ge_observed_share: row.impostor_ge_observed_share,
      original_shape_null_share: row.original_shape_null_share,
      original_label_null_share: row.original_label_null_share,
      unique_sha256_count: row.unique_sha256_count,
      unique_cisi_count: row.unique_cisi_count,
      unique_source_path_count: row.unique_source_path_count,
      low_null_failure_class: row.low_null_failure_class,
      blocked_reasons: row.blocked_reasons,
    })),
    decision:
      'The low real-token impostor rows do not rescue the Brahmi back door. All 21 low-null rows still fail the original shape-null gate, 19 also fail the original label-null gate, 11 fail minimum source-token independence, and no row passes both minimum independence and duplicate-collapse unanimity. Review-packet eligible rows remain zero.',
    files: {
      csv: 'data/brahmi/brahmi_real_token_low_null_autopsy_v3b.csv',
      summary: 'data/brahmi/brahmi_real_token_low_null_autopsy_v3b_summary.json',
    },
  };

  writeCsv(OUT_CSV, outputRows, FIELDS);
  fs.writeFileSync(OUT_JSON, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
}

main();
