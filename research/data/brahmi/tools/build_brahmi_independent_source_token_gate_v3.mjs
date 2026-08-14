// The v3 "independence preflight" for the Indus-to-Brahmi descent test.
// Before any sign family can even be considered as a phonetic anchor (an Indus
// sign whose shape plausibly carries its sound value into Brahmi), it must show
// its evidence is not one artifact counted many times. This script reads the v2
// family descent summary, the v2 duplicate-collapse audit, and the v2 source-token
// segments, then applies seven blocking rules per family: at least 3 unique image
// hashes, 3 unique CISI objects, and 3 unique source paths; unanimity that survives
// duplicate collapse; a modal label that does not change after collapse; and the
// original shape-null and label-null shares both at or below 0.01. Families that
// clear every rule are marked "review_packet_eligible_not_accepted" — eligible for
// a future blind visual review, never auto-promoted. It writes one CSV row per
// family plus a JSON summary; in this run zero anchors are accepted.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const OUT = path.join(ROOT, 'data', 'brahmi');
const RUN_DATE = '2026-05-30';

const FAMILY_SUMMARY = path.join(OUT, 'source_token_family_descent_summary_v2.csv');
const DUP_AUDIT = path.join(OUT, 'source_token_duplicate_collapse_audit_v2.csv');
const SEGMENTS = path.join(OUT, 'source_token_segments_v2.csv');

const CSV_OUT = path.join(OUT, 'brahmi_independent_source_token_gate_v3.csv');
const SUMMARY_OUT = path.join(OUT, 'brahmi_independent_source_token_gate_v3_summary.json');

const FIELDS = [
  'sign_id',
  'orientation_policy',
  'raw_sample_count',
  'unique_sha256_count',
  'unique_cisi_count',
  'raw_modal_label',
  'raw_modal_share',
  'sha_modal_label',
  'sha_modal_share',
  'cisi_modal_label',
  'cisi_modal_share',
  'original_shape_null_share',
  'original_label_null_share',
  'duplicate_collapse_status',
  'independence_status',
  'unanimity_after_collapse',
  'preflight_decision',
  'review_packet_eligible',
  'blocked_reasons',
  'cisis',
  'token_ids',
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

function num(value) {
  if (value === '' || value == null) return NaN;
  return Number(value);
}

function key(row) {
  return `${row.sign_id}::${row.orientation_policy}`;
}

function main() {
  const families = parseCsv(fs.readFileSync(FAMILY_SUMMARY, 'utf8'));
  const audits = parseCsv(fs.readFileSync(DUP_AUDIT, 'utf8'));
  const segments = parseCsv(fs.readFileSync(SEGMENTS, 'utf8'));

  const auditByKey = new Map(audits.map((row) => [key(row), row]));
  const sourcePathByToken = new Map(segments.map((row) => [row.token_id, row.source_path]));

  const rows = families.map((family) => {
    const audit = auditByKey.get(key(family));
    if (!audit) {
      throw new Error(`Missing duplicate audit row for ${key(family)}`);
    }

    const uniqueSha = num(audit.unique_sha256_count);
    const uniqueCisi = num(audit.unique_cisi_count);
    const shaShare = num(audit.sha_modal_share);
    const cisiShare = num(audit.cisi_modal_share);
    const rawShare = num(audit.raw_modal_share);
    const shapeNull = num(audit.original_shape_null_share);
    const labelNull = num(audit.original_label_null_share);

    const tokens = String(audit.token_ids || '').split('|').filter(Boolean);
    const cisis = String(audit.cisis || '').split('|').filter(Boolean);
    const sourcePaths = new Set(tokens.map((token) => sourcePathByToken.get(token)).filter(Boolean));

    const blocked = [];
    if (uniqueSha < 3) blocked.push('fewer_than_3_unique_token_hashes');
    if (uniqueCisi < 3) blocked.push('fewer_than_3_unique_cisis');
    if (sourcePaths.size < 3) blocked.push('fewer_than_3_unique_source_paths');
    if (!(rawShare === 1 && shaShare === 1 && cisiShare === 1)) blocked.push('not_unanimous_after_duplicate_collapse');
    if (!(audit.raw_modal_label === audit.sha_modal_label && audit.sha_modal_label === audit.cisi_modal_label)) blocked.push('modal_label_changes_after_collapse');
    if (!(shapeNull <= 0.01)) blocked.push('shape_null_above_0_01');
    if (!(labelNull <= 0.01)) blocked.push('label_null_above_0_01');

    const independenceStatus = uniqueSha >= 3 && uniqueCisi >= 3 && sourcePaths.size >= 3
      ? 'passes_min_independence'
      : 'fails_min_independence';
    const unanimityAfterCollapse = rawShare === 1 && shaShare === 1 && cisiShare === 1
      && audit.raw_modal_label === audit.sha_modal_label
      && audit.sha_modal_label === audit.cisi_modal_label
      ? 'unanimous'
      : 'not_unanimous';

    const preflightDecision = blocked.length === 0
      ? 'review_packet_eligible_not_accepted'
      : 'blocked_before_review';

    return {
      sign_id: family.sign_id,
      orientation_policy: family.orientation_policy,
      raw_sample_count: audit.raw_sample_count,
      unique_sha256_count: audit.unique_sha256_count,
      unique_cisi_count: audit.unique_cisi_count,
      raw_modal_label: audit.raw_modal_label,
      raw_modal_share: audit.raw_modal_share,
      sha_modal_label: audit.sha_modal_label,
      sha_modal_share: audit.sha_modal_share,
      cisi_modal_label: audit.cisi_modal_label,
      cisi_modal_share: audit.cisi_modal_share,
      original_shape_null_share: audit.original_shape_null_share,
      original_label_null_share: audit.original_label_null_share,
      duplicate_collapse_status: audit.duplicate_collapse_status,
      independence_status: independenceStatus,
      unanimity_after_collapse: unanimityAfterCollapse,
      preflight_decision: preflightDecision,
      review_packet_eligible: preflightDecision === 'review_packet_eligible_not_accepted' ? 'true' : 'false',
      blocked_reasons: blocked.join(';'),
      cisis: cisis.join('|'),
      token_ids: tokens.join('|'),
    };
  });

  const decisionCounts = rows.reduce((acc, row) => {
    acc[row.preflight_decision] = (acc[row.preflight_decision] || 0) + 1;
    return acc;
  }, {});

  const reasonCounts = {};
  for (const row of rows) {
    for (const reason of row.blocked_reasons.split(';').filter(Boolean)) {
      reasonCounts[reason] = (reasonCounts[reason] || 0) + 1;
    }
  }

  const nearMissSigns = new Set(['817', '527', '472', '060', '061']);
  const topNearMissRows = rows.filter((row) => nearMissSigns.has(row.sign_id));
  const eligibleRows = rows.filter((row) => row.review_packet_eligible === 'true');

  const summary = {
    date: RUN_DATE,
    status: 'brahmi_independent_source_token_gate_v3_no_phonetic_anchor',
    input_family_rows: families.length,
    duplicate_audit_rows: audits.length,
    source_segment_rows: segments.length,
    preflight_rule: '>=3 unique token hashes, >=3 unique CISIs, >=3 unique source paths, unanimity after duplicate collapse, unchanged modal label after collapse, original shape-null <=0.01, original label-null <=0.01',
    decision_counts: decisionCounts,
    blocked_reason_counts: reasonCounts,
    review_packet_eligible_rows: eligibleRows.length,
    candidate_only_rows: 0,
    accepted_phonetic_anchors: 0,
    top_v2_near_misses: topNearMissRows.map((row) => ({
      sign_id: row.sign_id,
      orientation_policy: row.orientation_policy,
      label: row.cisi_modal_label,
      unique_sha256_count: Number(row.unique_sha256_count),
      unique_cisi_count: Number(row.unique_cisi_count),
      preflight_decision: row.preflight_decision,
      blocked_reasons: row.blocked_reasons,
    })),
    eligible_for_future_blind_review: eligibleRows.map((row) => ({
      sign_id: row.sign_id,
      orientation_policy: row.orientation_policy,
      label: row.cisi_modal_label,
      unique_sha256_count: Number(row.unique_sha256_count),
      unique_cisi_count: Number(row.unique_cisi_count),
      original_shape_null_share: Number(row.original_shape_null_share),
      original_label_null_share: Number(row.original_label_null_share),
    })),
    conclusion: 'The independence preflight promotes no phonetic anchor. Rows that pass are only eligible for a future blind visual packet with matched Brahmi negatives; they are not candidate-only anchors.',
  };

  writeCsv(CSV_OUT, rows, FIELDS);
  fs.writeFileSync(SUMMARY_OUT, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
}

main();
