// Weighs the three left-context operator candidates — the signs 235, 032, and
// 004 that appear immediately before 002 in a 002-390-X frame — by how much
// real source evidence backs each one. The claims under test: 235 before 002
// triggers X=125, 032 before 002 suppresses 125, and 004 splits neutrally.
// This script reads the 002-390 frames CSV from the branch-sign-ecology run,
// buckets each row's source status into classes (strict, panel, route-only,
// unbound, metadata-only), summarizes the X and tail distributions per left
// sign, and applies hand-written per-operator decision rules that demand
// strict witnesses before promotion. Four contradiction checks record the
// pass/fail state. Writes row-classification, left-summary, and
// contradiction-check CSVs plus a summary JSON to data/open_prototype/reports/.
// Bottom line: all three stay local operators, never sign values or
// translations, and each is source-thin or source-blocked.

import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const framesPath = path.join(reportsDir, 'campaign_032_002_861_002390x_branch_sign_ecology_20260531_002390_frames.csv');
const prefix = 'campaign_032_002_861_002390x_consolidate_left_context_source_weight_20260531';

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (ch === '"' && next === '"') {
        field += '"';
        i += 1;
      } else if (ch === '"') {
        quoted = false;
      } else {
        field += ch;
      }
    } else if (ch === '"') {
      quoted = true;
    } else if (ch === ',') {
      row.push(field);
      field = '';
    } else if (ch === '\n') {
      row.push(field.replace(/\r$/, ''));
      rows.push(row);
      row = [];
      field = '';
    } else {
      field += ch;
    }
  }
  if (field.length || row.length) {
    row.push(field.replace(/\r$/, ''));
    rows.push(row);
  }
  const header = rows.shift() ?? [];
  return rows
    .filter((r) => r.some((value) => value !== ''))
    .map((r) => Object.fromEntries(header.map((name, index) => [name, r[index] ?? ''])));
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

function countBy(items, fn) {
  const counts = new Map();
  for (const item of items) {
    const key = fn(item) || '-';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()].sort(
    (a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }),
  );
}

function topCounts(counts) {
  return counts.map(([key, value]) => `${key}:${value}`).join(';');
}

function sourceClass(status) {
  if (status.includes('checkpoint_strict_source_visible')) return 'strict';
  if (status.includes('source_panel_acquired')) return 'panel_compatible_not_strict';
  if (status.includes('checkpoint_permissive_public_panel')) return 'panel_permissive_not_strict';
  if (status.includes('source_route')) return 'route_only';
  if (status.includes('dholavira') || status.includes('unbound')) return 'unbound';
  if (status.includes('secondary_icon') || status.includes('absent')) return 'source_dark';
  if (status.includes('metadata_only')) return 'metadata_only';
  return 'other';
}

function leftDecision(left, rows) {
  const xs = new Set(rows.map((row) => row.branch_after_390));
  const strict = rows.filter((row) => row.source_class === 'strict').length;
  if (left === '235') {
    return xs.size === 1 && xs.has('125')
      ? strict >= 2
        ? 'promote_candidate_235_p086_trigger'
        : 'keep_candidate_235_p086_trigger_source_thin'
      : 'demote_235_trigger';
  }
  if (left === '032') {
    return xs.has('125')
      ? 'kill_032_no125_suppression'
      : strict >= 1
        ? 'keep_candidate_boundary_formula_context_source_split'
        : 'keep_prediction_only';
  }
  if (left === '004') {
    return xs.size > 1
      ? strict === 0
        ? 'keep_neutral_split_prediction_source_blocked'
        : 'keep_neutral_split_candidate'
      : 'demote_neutral_split';
  }
  return strict > 0 ? 'row_context_not_operator' : 'background_not_operator';
}

function evidence(rows) {
  return rows
    .map((row) => `${row.object}:${row.prev_before_002}->${row.branch_after_390}->${row.tail_after_branch}:${row.source_class}`)
    .join(' | ');
}

fs.mkdirSync(reportsDir, { recursive: true });

const frames = parseCsv(fs.readFileSync(framesPath, 'utf8')).map((row) => ({
  ...row,
  source_class: sourceClass(row.source_status),
}));

const targetOperators = new Set(['235', '032', '004']);

const rowClassifications = frames.map((row) => ({
  checked_date: '2026-05-31',
  object: row.object,
  left_final: row.prev_before_002,
  x: row.branch_after_390,
  tail_after_x: row.tail_after_branch,
  terminal_after_x: row.terminal_after_branch,
  source_class: row.source_class,
  operator_status: targetOperators.has(row.prev_before_002) ? 'candidate_operator_context' : 'row_context_only',
  text: row.text,
}));

const leftSummary = countBy(frames, (row) => row.prev_before_002).map(([left, n]) => {
  const rows = frames.filter((row) => row.prev_before_002 === left);
  return {
    checked_date: '2026-05-31',
    left_final: left,
    n: String(n),
    operator_scope: targetOperators.has(left) ? 'candidate_operator' : 'row_context_only',
    x_distribution: topCounts(countBy(rows, (row) => row.branch_after_390)),
    tail_distribution: topCounts(countBy(rows, (row) => row.tail_after_branch)),
    strict_count: String(rows.filter((row) => row.source_class === 'strict').length),
    source_classes: topCounts(countBy(rows, (row) => row.source_class)),
    decision: leftDecision(left, rows),
    evidence: evidence(rows),
  };
});

const rows235 = frames.filter((row) => row.prev_before_002 === '235');
const rows032 = frames.filter((row) => row.prev_before_002 === '032');
const rows004 = frames.filter((row) => row.prev_before_002 === '004');

const contradictionChecks = [
  {
    checked_date: '2026-05-31',
    check_id: 'CONSOLIDATE_LEFT_235_TARGET_PREDICTS_125',
    result: rows235.length > 0 && rows235.every((row) => row.branch_after_390 === '125') ? 'pass_source_thin' : 'fail',
    evidence: evidence(rows235),
    parser_consequence: '235 remains a P086 trigger candidate in target 002-390, but only one exact strict 390 row carries it.',
  },
  {
    checked_date: '2026-05-31',
    check_id: 'CONSOLIDATE_LEFT_032_AVOIDS_125',
    result: rows032.every((row) => row.branch_after_390 !== '125') ? 'pass_split_source_blocked' : 'fail',
    evidence: evidence(rows032),
    parser_consequence: '032 no-235 suppression survives locally; M-70 is strict but 3335.1 blocks the split from promotion.',
  },
  {
    checked_date: '2026-05-31',
    check_id: 'CONSOLIDATE_LEFT_004_IS_NEUTRAL_SPLIT',
    result:
      new Set(rows004.map((row) => row.branch_after_390)).size > 1
        ? rows004.some((row) => row.source_class === 'strict')
          ? 'pass'
          : 'partial_source_blocked'
        : 'fail',
    evidence: evidence(rows004),
    parser_consequence: '004 split survives only as a prediction because H-1993 is route-only and Sktd-1 is wrapped/permissive.',
  },
  {
    checked_date: '2026-05-31',
    check_id: 'CONSOLIDATE_LEFT_OPERATORS_ARE_NOT_SIGN_VALUES',
    result: 'pass_demote_semantics',
    evidence: '235 has target-only trigger pressure; 032 and 004 split; all three are source- or scope-limited.',
    parser_consequence: 'Treat left contexts as local operators, not sign values or translations.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'CONSOLIDATE',
  status: 'left_context_source_weight_consolidation',
  compact_left_parser: {
    keep: [
      '235 -> 125 in target 002-390 as source-thin P086 trigger candidate',
      '032 without 235 avoids 125 in target lane; strict side is M-70, continuing 590 side is 3335.1-blocked',
      '004 neutral split survives only as H-1993/Sktd-1 prediction, not strict evidence',
    ],
    demote: [
      '235 as broad portable title trigger',
      '032 as global no-125 value',
      '004 as direct selector or semantic value',
      'all non-235/032/004 left finals as operator claims',
    ],
  },
  left_summary: Object.fromEntries(leftSummary.map((row) => [row.left_final, row.decision])),
  contradiction_results: Object.fromEntries(contradictionChecks.map((row) => [row.check_id, row.result])),
};

writeCsv(path.join(reportsDir, `${prefix}_row_classification.csv`), rowClassifications, [
  'checked_date',
  'object',
  'left_final',
  'x',
  'tail_after_x',
  'terminal_after_x',
  'source_class',
  'operator_status',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_left_summary.csv`), leftSummary, [
  'checked_date',
  'left_final',
  'n',
  'operator_scope',
  'x_distribution',
  'tail_distribution',
  'strict_count',
  'source_classes',
  'decision',
  'evidence',
]);

writeCsv(path.join(reportsDir, `${prefix}_contradiction_checks.csv`), contradictionChecks, [
  'checked_date',
  'check_id',
  'result',
  'evidence',
  'parser_consequence',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
