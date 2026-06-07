import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const keyPath = path.join(reportsDir, 'campaign_002_y_branch_gap_blind_answer_key.csv');
const defaultReviewDir = path.join(reportsDir, 'campaign_002_y_branch_gap_blind_reviews');
const outSummary = path.join(reportsDir, 'campaign_002_y_branch_gap_blind_review_summary.json');
const outRows = path.join(reportsDir, 'campaign_002_y_branch_gap_blind_scored_rows.csv');

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

function reviewerName(filePath) {
  return path.basename(filePath).replace(/\.csv$/i, '');
}

function tokenCount(text) {
  return String(text ?? '')
    .replaceAll('+', '-')
    .split('-')
    .filter((part) => /^\d{3}$/.test(part)).length;
}

function parseReviewCount(value) {
  const text = String(value ?? '').trim().toLowerCase();
  const exact = text.match(/^\d+$/);
  if (exact) return { value: Number(exact[0]), uncertain: false, raw: text };
  const uncertain = text.match(/^uncertain[_\s-]*(\d+)$/);
  if (uncertain) return { value: Number(uncertain[1]), uncertain: true, raw: text };
  const embedded = text.match(/(\d+)/);
  if (embedded) return { value: Number(embedded[1]), uncertain: true, raw: text };
  return { value: null, uncertain: true, raw: text || 'missing' };
}

function roleClass(row) {
  const role = row.control_role ?? '';
  if (role.startsWith('primary_target')) return 'primary_target';
  if (role.startsWith('backup_target')) return 'backup_target';
  if (role === 'scoring_negative') return 'scoring_negative';
  if (role.startsWith('quarantine')) return 'quarantine';
  return 'other';
}

function hasHardBranchRelationNote(value) {
  const text = String(value ?? '').trim().toLowerCase();
  if (!text || text.includes('not assessed') || text.includes('cannot') || text.includes('no catalog')) return false;
  return /\b(yes|present|candidate|looks like|probable)\b/.test(text);
}

function rate(numerator, denominator) {
  return denominator ? numerator / denominator : null;
}

const keyRows = loadCsv(keyPath).map((row) => ({
  ...row,
  expected_token_count: tokenCount(row.target_text),
  role_class: roleClass(row),
}));
const keyByBlindId = new Map(keyRows.map((row) => [row.blind_id, row]));
const scoredRows = [];
const reviewerSummaries = [];

if (!reviewPaths.length) {
  const summary = {
    date: '2026-05-29',
    packet_id: 'branch_gap_source_box_v1',
    status: 'not_scored_no_review_csvs_found',
    reviewer_count: 0,
    accepted_claims_increment: 0,
    interpretation_boundary:
      'The blind packet has not been reviewed. No token stability, false-positive behavior, source-box promotion, or accepted claim follows.',
  };
  fs.writeFileSync(outSummary, `${JSON.stringify(summary, null, 2)}\n`);
  fs.writeFileSync(
    outRows,
    toCsv([
      [
        'reviewer',
        'blind_id',
        'cisi',
        'role_class',
        'expected_token_count',
        'review_token_count',
        'review_count_uncertain',
        'count_match_status',
        'hard_branch_relation_note',
        'notes',
      ],
    ]),
  );
  console.log(JSON.stringify(summary, null, 2));
  process.exit(0);
}

for (const reviewPath of reviewPaths) {
  const name = reviewerName(reviewPath);
  const reviewRows = loadCsv(reviewPath);
  const reviewIds = new Set();
  const counts = {
    rows_reviewed: 0,
    exact_count_matches: 0,
    uncertain_count_matches: 0,
    count_mismatches: 0,
    missing_counts: 0,
    primary_exact_matches: 0,
    primary_count_rows: 0,
    backup_exact_matches: 0,
    backup_count_rows: 0,
    scoring_negative_hard_branch_relation_notes: 0,
    target_hard_branch_relation_notes: 0,
    missing_rows: 0,
  };

  for (const reviewRow of reviewRows) {
    const blindId = reviewRow.blind_id;
    if (!blindId) continue;
    const key = keyByBlindId.get(blindId);
    if (!key) throw new Error(`Review ${name} contains unknown blind_id ${blindId}`);
    reviewIds.add(blindId);
    counts.rows_reviewed++;

    const parsed = parseReviewCount(reviewRow.stage1_visual_token_count);
    let countStatus = 'missing_count';
    if (parsed.value === null) {
      counts.missing_counts++;
    } else if (parsed.value === key.expected_token_count && parsed.uncertain) {
      counts.uncertain_count_matches++;
      countStatus = 'uncertain_expected_count_match';
    } else if (parsed.value === key.expected_token_count) {
      counts.exact_count_matches++;
      countStatus = 'exact_expected_count_match';
    } else {
      counts.count_mismatches++;
      countStatus = 'count_mismatch';
    }

    if (key.role_class === 'primary_target') {
      counts.primary_count_rows++;
      if (countStatus === 'exact_expected_count_match') counts.primary_exact_matches++;
    }
    if (key.role_class === 'backup_target') {
      counts.backup_count_rows++;
      if (countStatus === 'exact_expected_count_match') counts.backup_exact_matches++;
    }

    const hardBranchNote = hasHardBranchRelationNote(reviewRow.stage1_visible_002_y_candidate_notes);
    if (hardBranchNote && key.role_class === 'scoring_negative') counts.scoring_negative_hard_branch_relation_notes++;
    if (hardBranchNote && ['primary_target', 'backup_target'].includes(key.role_class)) {
      counts.target_hard_branch_relation_notes++;
    }

    scoredRows.push([
      name,
      blindId,
      key.cisi,
      key.role_class,
      key.expected_token_count,
      parsed.value ?? '',
      parsed.uncertain,
      countStatus,
      hardBranchNote,
      reviewRow.stage1_uncertainty_notes ?? '',
    ]);
  }

  const missingIds = [...keyByBlindId.keys()].filter((blindId) => !reviewIds.has(blindId));
  counts.missing_rows += missingIds.length;
  for (const blindId of missingIds) {
    const key = keyByBlindId.get(blindId);
    scoredRows.push([name, blindId, key.cisi, key.role_class, key.expected_token_count, '', true, 'missing_review_row', false, '']);
  }

  reviewerSummaries.push({
    reviewer: name,
    review_path: reviewPath,
    rows_expected: keyRows.length,
    ...counts,
    exact_count_match_rate: rate(counts.exact_count_matches, counts.rows_reviewed),
    primary_strict_count_recovery_rate: rate(counts.primary_exact_matches, counts.primary_count_rows),
    backup_strict_count_recovery_rate: rate(counts.backup_exact_matches, counts.backup_count_rows),
    scoring_negative_hard_branch_relation_note_rate: rate(
      counts.scoring_negative_hard_branch_relation_notes,
      keyRows.filter((row) => row.role_class === 'scoring_negative').length,
    ),
  });
}

const byBlindId = new Map();
for (const row of scoredRows) {
  const [reviewer, blindId, cisi, role, expected, reviewCount, uncertain, countStatus] = row;
  if (!byBlindId.has(blindId)) byBlindId.set(blindId, { blindId, cisi, role, expected, rows: [] });
  byBlindId.get(blindId).rows.push({ reviewer, reviewCount, uncertain, countStatus });
}

const targetStability = [...byBlindId.values()]
  .filter((row) => ['primary_target', 'backup_target'].includes(row.role))
  .map((row) => {
    const numericCounts = row.rows.map((entry) => Number(entry.reviewCount)).filter((value) => Number.isFinite(value));
    const strictMatches = row.rows.filter((entry) => entry.countStatus === 'exact_expected_count_match').length;
    return {
      blind_id: row.blindId,
      cisi: row.cisi,
      role_class: row.role,
      expected_token_count: row.expected,
      reviewed_numeric_counts: numericCounts,
      all_numeric_counts_same: numericCounts.length >= 2 && new Set(numericCounts).size === 1,
      all_reviewers_exact_expected_count: strictMatches === row.rows.length && row.rows.length >= 2,
    };
  });

const failedReasons = [];
if (reviewerSummaries.length < 2) failedReasons.push('fewer_than_two_independent_reviews');
if (targetStability.some((row) => !row.all_reviewers_exact_expected_count)) {
  failedReasons.push('not_all_target_and_backup_rows_have_stable_exact_token_counts');
}
if (reviewerSummaries.some((row) => row.scoring_negative_hard_branch_relation_notes > 0)) {
  failedReasons.push('scoring_negatives_have_hard_branch_relation_notes');
}
failedReasons.push('stage1_tokenization_only_no_unblinded_alignment_or_branch_relation_scoring');

const summary = {
  date: '2026-05-29',
  packet_id: 'branch_gap_source_box_v1',
  status: 'stage1_tokenization_scored_no_claim_promotion',
  key_path: keyPath,
  review_paths: reviewPaths,
  reviewer_count: reviewerSummaries.length,
  reviewer_summaries: reviewerSummaries,
  target_stability: targetStability,
  promotion_gate_decision: 'not_promotable_stage1_only_no_claim_increment',
  promotion_gate_failed_reasons: failedReasons,
  accepted_claims_increment: 0,
  interpretation_boundary:
    'This stage-1 scorer only checks blind token-count stability and hard branch-relation notes. It cannot validate source-normalized token identity, physical direction, sign meaning, phonetic value, language family, translation, or accepted structural status.',
};

fs.mkdirSync(path.dirname(outRows), { recursive: true });
fs.writeFileSync(
  outRows,
  toCsv([
    [
      'reviewer',
      'blind_id',
      'cisi',
      'role_class',
      'expected_token_count',
      'review_token_count',
      'review_count_uncertain',
      'count_match_status',
      'hard_branch_relation_note',
      'notes',
    ],
    ...scoredRows,
  ]),
);
fs.writeFileSync(outSummary, `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
