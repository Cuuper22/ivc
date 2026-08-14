import fs from 'node:fs';
import path from 'node:path';

// This script re-weights every 002-390-X claim by how good its source evidence
// is, not just how the corpus counts fall. It reads the branch-sign-ecology
// frames CSV, maps each row's source_status string onto a tier (strict on a
// verified image, panel-but-not-strict, route-only, unbound, source-dark,
// metadata-only), and assigns each X sign a role (125 open-branch carrier,
// 095/692/705 terminal closure family, 530 one-complement linker, 590 bridge,
// or singleton filler). Only strict rows may be "load_bearing_syntax"; panel
// rows are pressure, everything else is background. Six contradiction checks
// then pin the surviving shape: 125 must always continue, the closed family
// must always end, the closed family has just two strict rows (M-70, M-71),
// 530 and 590 survive only as untested predictions, and the singleton fillers
// carry nothing. Writes row-classification, per-X summary, and contradiction-
// check CSVs plus a summary JSON to data/open_prototype/reports.

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const framesPath = path.join(reportsDir, 'campaign_032_002_861_002390x_branch_sign_ecology_20260531_002390_frames.csv');
const prefix = 'campaign_032_002_861_002390x_consolidate_xslot_source_weight_20260531';

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

function xRole(x) {
  if (x === '125') return 'open_branch_carrier_tail_conditioned';
  if (['095', '692', '705'].includes(x)) return 'terminal_closure_family';
  if (x === '530') return 'one_complement_linker';
  if (x === '590') return 'embedded_formula_bridge';
  return 'singleton_terminal_filler';
}

function xDecision(x, rows) {
  const strict = rows.filter((row) => row.source_class === 'strict').length;
  const terminals = rows.filter((row) => row.terminal_after_branch === 'True').length;
  if (x === '125') return strict >= 2 ? 'keep_candidate_open_branch_syntax_only' : 'demote_open_branch_to_source_thin';
  if (x === '095') return strict >= 1 && terminals === rows.length ? 'keep_terminal_syntax_semantics_wild' : 'route_blocked_terminal_pressure';
  if (x === '692') return strict === 1 && rows.length === 1 ? 'keep_singleton_strict_terminal_edge' : 'demote_until_second_strict_row';
  if (x === '705') return 'demote_repeated_terminal_until_source_bound';
  if (x === '530') return 'keep_one_complement_prediction_not_load_bearing';
  if (x === '590') return 'keep_bridge_prediction_source_blocked';
  return 'demote_to_wild_singleton_terminal_filler';
}

function evidence(rows) {
  return rows.map((row) => `${row.object}:${row.prev_before_002}->${row.branch_after_390}->${row.tail_after_branch}:${row.source_class}`).join(' | ');
}

fs.mkdirSync(reportsDir, { recursive: true });

const frames = parseCsv(fs.readFileSync(framesPath, 'utf8')).map((row) => ({
  ...row,
  source_class: sourceClass(row.source_status),
  role: xRole(row.branch_after_390),
}));

const rowClassifications = frames.map((row) => ({
  checked_date: '2026-05-31',
  object: row.object,
  x: row.branch_after_390,
  role: row.role,
  tail_after_x: row.tail_after_branch,
  terminal_after_x: row.terminal_after_branch,
  source_class: row.source_class,
  source_status: row.source_status,
  parser_use:
    row.source_class === 'strict'
      ? 'load_bearing_syntax'
      : row.source_class.includes('panel')
        ? 'pressure_only'
        : 'prediction_or_background_only',
  text: row.text,
}));

const xSummary = countBy(frames, (row) => row.branch_after_390).map(([x, n]) => {
  const rows = frames.filter((row) => row.branch_after_390 === x);
  return {
    checked_date: '2026-05-31',
    x,
    role: xRole(x),
    n: String(n),
    terminal_count: String(rows.filter((row) => row.terminal_after_branch === 'True').length),
    strict_count: String(rows.filter((row) => row.source_class === 'strict').length),
    source_classes: topCounts(countBy(rows, (row) => row.source_class)),
    prev_contexts: topCounts(countBy(rows, (row) => row.prev_before_002)),
    tails: topCounts(countBy(rows, (row) => row.tail_after_branch)),
    decision: xDecision(x, rows),
    evidence: evidence(rows),
  };
});

const closedRows = frames.filter((row) => ['095', '692', '705'].includes(row.branch_after_390));
const singletonRows = frames.filter((row) => ['072', '140', '346', '707'].includes(row.branch_after_390));
const rows125 = frames.filter((row) => row.branch_after_390 === '125');
const rows530 = frames.filter((row) => row.branch_after_390 === '530');
const rows590 = frames.filter((row) => row.branch_after_390 === '590');

const contradictionChecks = [
  {
    checked_date: '2026-05-31',
    check_id: 'CONSOLIDATE_125_MUST_BE_OPEN_CONTINUING',
    result: rows125.every((row) => row.terminal_after_branch === 'False') ? 'pass' : 'fail',
    evidence: evidence(rows125),
    parser_consequence: '125 can remain the only repeated open branch, but only carrier/tail-conditioned.',
  },
  {
    checked_date: '2026-05-31',
    check_id: 'CONSOLIDATE_CLOSED_FAMILY_MUST_END',
    result: closedRows.every((row) => row.terminal_after_branch === 'True') ? 'pass' : 'fail',
    evidence: evidence(closedRows),
    parser_consequence: '095/692/705 can remain terminal closure syntax; 705 remains source-thin.',
  },
  {
    checked_date: '2026-05-31',
    check_id: 'CONSOLIDATE_CLOSED_FAMILY_SOURCE_WEIGHT',
    result: closedRows.filter((row) => row.source_class === 'strict').length >= 2 ? 'partial_pass' : 'fail',
    evidence: evidence(closedRows),
    parser_consequence: 'Terminal family is real enough for syntax but not semantics; load-bearing strict rows are M-70 and M-71.',
  },
  {
    checked_date: '2026-05-31',
    check_id: 'CONSOLIDATE_530_EXACTLY_ONE_COMPLEMENT',
    result: rows530.length === 1 && rows530[0]?.tail_after_branch.split(' ').length === 1 ? 'partial_pass' : 'fail',
    evidence: evidence(rows530),
    parser_consequence: '530 linker survives as a prediction only because H-773 is not token-strict.',
  },
  {
    checked_date: '2026-05-31',
    check_id: 'CONSOLIDATE_590_REQUIRES_032_TAIL',
    result: rows590.length === 1 && rows590[0]?.tail_after_branch === '032' ? 'partial_pass' : 'fail',
    evidence: evidence(rows590),
    parser_consequence: '590 bridge survives only as source-blocked 3335.1 prediction.',
  },
  {
    checked_date: '2026-05-31',
    check_id: 'CONSOLIDATE_SINGLETONS_DO_NOT_CARRY_MODEL',
    result: singletonRows.every((row) => row.terminal_after_branch === 'True') ? 'pass_demote' : 'fail',
    evidence: evidence(singletonRows),
    parser_consequence: '072/140/346/707 are terminal fillers until repeated or source-bound.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'CONSOLIDATE',
  status: 'xslot_source_weight_consolidation',
  compact_parser: {
    core_load_bearing: [
      '125 open branch syntax through strict M-119/M-735, but carrier/tail-conditioned',
      '095 and 692 terminal syntax through strict M-71/M-70',
    ],
    pressure_only: [
      '705 repeated terminal syntax until M-1825 and Dholavira bind',
      '530 one-complement linker until H-773 is token-strict',
      '590-032 bridge until 3335.1 binds',
      '125-820 terminal cap until Sktd-1 unwraps or a third governed row appears',
    ],
    killed_or_demoted: [
      'broad 125 sign value',
      '820 title value',
      '125-195 reusable tail',
      '072/140/346/707 as meaningful X classes',
    ],
  },
  x_summary: Object.fromEntries(xSummary.map((row) => [row.x, row.decision])),
  contradiction_results: Object.fromEntries(contradictionChecks.map((row) => [row.check_id, row.result])),
};

writeCsv(path.join(reportsDir, `${prefix}_row_classification.csv`), rowClassifications, [
  'checked_date',
  'object',
  'x',
  'role',
  'tail_after_x',
  'terminal_after_x',
  'source_class',
  'source_status',
  'parser_use',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_x_summary.csv`), xSummary, [
  'checked_date',
  'x',
  'role',
  'n',
  'terminal_count',
  'strict_count',
  'source_classes',
  'prev_contexts',
  'tails',
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
