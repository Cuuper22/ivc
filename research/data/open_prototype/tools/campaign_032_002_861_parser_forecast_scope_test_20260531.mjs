// Scope test for the whole parser: turn every rule accumulated so far into explicit,
// row-level forecasts, then count where they break. The rules cover the left side (final 235
// plus a P086 head predicts a 125 rank tail; 032 on the left without 235 suppresses 125;
// final 004 splits between 095 and 125) and the X slot (125 must continue, 530 takes exactly
// one complement, 590 requires an 032 tail, the closed branches must be terminal). We read
// the filtered Indus inscription list (lipi/metadata_filtered.csv), keep one copy of each
// distinct sign sequence, extract every governed frame, attach forecasts and violations to
// each, and run seven scope bets at widening scopes — target 002-390 only, P086 heads, all
// governed frames — to find where each rule stops holding. The point is to declare honest
// boundaries: a rule may be a local parser cue without being a global sign value. Writes
// forecast, scope-test, and decision CSVs plus a JSON summary to data/open_prototype/reports.
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_parser_forecast_scope_test_20260531';
const checkedDate = '2026-05-31';
const p086Heads = new Set(['390', '405']);
const closureHeads = new Set(['817', '820', '861']);
const closed390Branches = new Set(['072', '095', '140', '346', '692', '705', '707']);

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

function signs(text) {
  return [...String(text || '').matchAll(/\d{3}/g)].map((match) => match[0]);
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
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

function topCounts(items, fn, n = 12) {
  return countBy(items, fn)
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function safeShare(num, den) {
  return den ? (num / den).toFixed(6) : 'NA';
}

function examples(rows, n = 10) {
  return rows
    .slice(0, n)
    .map((row) => `${row.cisi}:${row.left_final}-002-${row.head}-${row.branch}-${row.tail}`)
    .join(' | ');
}

function frameForecast(frame) {
  const leftForecasts = [];
  const xForecasts = [];
  const violations = [];
  const has125 = frame.branch === '125' || frame.tail_tokens.includes('125');

  if (frame.left_final === '235') {
    if (p086Heads.has(frame.head)) {
      leftForecasts.push('final235_plus_P086_predicts_125_rank_tail');
      if (!has125) violations.push('final235_P086_missing_125');
    } else {
      leftForecasts.push('final235_nonP086_no_125_prediction');
    }
  }

  if (frame.left_tokens.includes('032') && !frame.left_tokens.includes('235')) {
    leftForecasts.push('contains032_no235_suppresses_125_in_target_scope');
    if (frame.head === '390' && has125) violations.push('target390_032_no235_has_125');
  }

  if (frame.left_final === '004') {
    leftForecasts.push('final004_neutral_qualifier_allows_status_or_rank_split');
    if (frame.head === '390' && !['095', '125'].includes(frame.branch)) {
      violations.push('target390_final004_unexpected_branch');
    }
  }

  if (frame.head === '390') {
    if (frame.branch === '125') {
      xForecasts.push('125_rank_title_selector_must_continue');
      if (frame.terminal_after_branch) violations.push('terminal_390_125');
    } else if (frame.branch === '530') {
      xForecasts.push('530_one_complement_closure_linker');
      if (frame.tail_tokens.length !== 1) violations.push('bad_530_tail_length');
    } else if (frame.branch === '590') {
      xForecasts.push('590_formula_bridge_requires_032_tail');
      if (frame.tail !== '032') violations.push('bad_590_tail');
    } else if (closed390Branches.has(frame.branch)) {
      xForecasts.push(`closed_${frame.branch}_must_be_terminal`);
      if (!frame.terminal_after_branch) violations.push(`continuing_closed_${frame.branch}`);
    } else {
      xForecasts.push('untyped_390_branch');
    }
  }

  return {
    leftForecasts,
    xForecasts,
    violations,
  };
}

fs.mkdirSync(reportsDir, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  tokens: signs(row.text),
}));
const canonicalRows = [...new Map(rawRows.map((row) => [row.tokens.join(' '), row])).values()];

const frames = [];
for (const row of canonicalRows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
    if (row.tokens[i] !== '002' || !row.tokens[i + 1] || !row.tokens[i + 2]) continue;
    const leftTokens = row.tokens.slice(0, i);
    const tailTokens = row.tokens.slice(i + 3);
    const frame = {
      checked_date: checkedDate,
      cisi: objectId(row),
      row_id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      left_tokens: leftTokens,
      left: leftTokens.join(' ') || '<START>',
      left_final: leftTokens.at(-1) ?? '<START>',
      head: row.tokens[i + 1],
      branch: row.tokens[i + 2],
      tail_tokens: tailTokens,
      tail: tailTokens.join(' ') || '<END>',
      terminal_after_branch: tailTokens.length === 0,
      text: row.text,
    };
    const forecast = frameForecast(frame);
    frame.left_forecasts = forecast.leftForecasts;
    frame.x_forecasts = forecast.xForecasts;
    frame.violations = forecast.violations;
    frames.push(frame);
  }
}

const target390 = frames.filter((frame) => frame.head === '390');
const final235 = frames.filter((frame) => frame.left_final === '235');
const final235P086 = final235.filter((frame) => p086Heads.has(frame.head));
const final235P086Missing125 = final235P086.filter(
  (frame) => frame.branch !== '125' && !frame.tail_tokens.includes('125'),
);
const final235Closure = final235.filter((frame) => closureHeads.has(frame.head));
const final235ClosureHas125 = final235Closure.filter((frame) => frame.branch === '125' || frame.tail_tokens.includes('125'));
const contains032No235 = frames.filter((frame) => frame.left_tokens.includes('032') && !frame.left_tokens.includes('235'));
const contains032No235Has125 = contains032No235.filter(
  (frame) => frame.branch === '125' || frame.tail_tokens.includes('125'),
);
const contains032No235P086 = contains032No235.filter((frame) => p086Heads.has(frame.head));
const contains032No235P086Has125 = contains032No235P086.filter(
  (frame) => frame.branch === '125' || frame.tail_tokens.includes('125'),
);
const contains032No235Target390 = contains032No235.filter((frame) => frame.head === '390');
const contains032No235Target390Has125 = contains032No235Target390.filter(
  (frame) => frame.branch === '125' || frame.tail_tokens.includes('125'),
);
const final004 = frames.filter((frame) => frame.left_final === '004');
const final004Target390 = final004.filter((frame) => frame.head === '390');
const targetViolations = target390.filter((frame) => frame.violations.length);

const forecastRows = target390.map((frame) => ({
  checked_date: checkedDate,
  cisi: frame.cisi,
  row_id: frame.row_id,
  site: frame.site,
  type: frame.type,
  shape: frame.shape,
  left: frame.left,
  left_final: frame.left_final,
  head: frame.head,
  branch: frame.branch,
  tail: frame.tail,
  terminal_after_branch: String(frame.terminal_after_branch),
  left_forecasts: frame.left_forecasts.join(';') || 'none',
  x_forecasts: frame.x_forecasts.join(';') || 'none',
  forecast_violations: frame.violations.join(';') || 'none',
  provisional_parse:
    frame.violations.length === 0
      ? `${frame.left_forecasts.join('+') || 'untyped_left'} -> ${frame.x_forecasts.join('+') || 'untyped_X'}`
      : 'forecast_violation',
  text: frame.text,
}));

const scopeRows = [
  {
    checked_date: checkedDate,
    scope_bet: 'final235_plus_P086_predicts_125',
    frame_count: String(final235P086.length),
    pass_count: String(final235P086.length - final235P086Missing125.length),
    fail_count: String(final235P086Missing125.length),
    pass_share: safeShare(final235P086.length - final235P086Missing125.length, final235P086.length),
    local_scope: 'all_governed_frames',
    decision:
      final235P086.length > 0 && final235P086Missing125.length === 0
        ? 'candidate_scope_survives'
        : 'scope_break',
    examples: examples(final235P086),
    failures: examples(final235P086Missing125),
  },
  {
    checked_date: checkedDate,
    scope_bet: 'final235_plus_closure_heads_avoid_125',
    frame_count: String(final235Closure.length),
    pass_count: String(final235Closure.length - final235ClosureHas125.length),
    fail_count: String(final235ClosureHas125.length),
    pass_share: safeShare(final235Closure.length - final235ClosureHas125.length, final235Closure.length),
    local_scope: 'all_governed_frames',
    decision:
      final235Closure.length > 0 && final235ClosureHas125.length === 0
        ? 'candidate_scope_survives'
        : 'scope_break',
    examples: examples(final235Closure),
    failures: examples(final235ClosureHas125),
  },
  {
    checked_date: checkedDate,
    scope_bet: 'contains032_no235_suppresses_125_globally',
    frame_count: String(contains032No235.length),
    pass_count: String(contains032No235.length - contains032No235Has125.length),
    fail_count: String(contains032No235Has125.length),
    pass_share: safeShare(contains032No235.length - contains032No235Has125.length, contains032No235.length),
    local_scope: 'all_governed_frames',
    decision: contains032No235Has125.length === 0 ? 'global_scope_survives' : 'global_scope_breaks',
    examples: examples(contains032No235),
    failures: examples(contains032No235Has125),
  },
  {
    checked_date: checkedDate,
    scope_bet: 'contains032_no235_suppresses_125_in_P086',
    frame_count: String(contains032No235P086.length),
    pass_count: String(contains032No235P086.length - contains032No235P086Has125.length),
    fail_count: String(contains032No235P086Has125.length),
    pass_share: safeShare(contains032No235P086.length - contains032No235P086Has125.length, contains032No235P086.length),
    local_scope: 'P086_heads_390_405',
    decision:
      contains032No235P086.length > 0 && contains032No235P086Has125.length === 0
        ? 'candidate_local_scope_survives'
        : 'local_scope_break',
    examples: examples(contains032No235P086),
    failures: examples(contains032No235P086Has125),
  },
  {
    checked_date: checkedDate,
    scope_bet: 'contains032_no235_suppresses_125_in_target390',
    frame_count: String(contains032No235Target390.length),
    pass_count: String(contains032No235Target390.length - contains032No235Target390Has125.length),
    fail_count: String(contains032No235Target390Has125.length),
    pass_share: safeShare(
      contains032No235Target390.length - contains032No235Target390Has125.length,
      contains032No235Target390.length,
    ),
    local_scope: 'target_002_390',
    decision:
      contains032No235Target390.length > 0 && contains032No235Target390Has125.length === 0
        ? 'candidate_target_scope_survives'
        : 'target_scope_break',
    examples: examples(contains032No235Target390),
    failures: examples(contains032No235Target390Has125),
  },
  {
    checked_date: checkedDate,
    scope_bet: 'final004_target390_allows_095_125_split',
    frame_count: String(final004Target390.length),
    pass_count: String(final004Target390.filter((frame) => ['095', '125'].includes(frame.branch)).length),
    fail_count: String(final004Target390.filter((frame) => !['095', '125'].includes(frame.branch)).length),
    pass_share: safeShare(
      final004Target390.filter((frame) => ['095', '125'].includes(frame.branch)).length,
      final004Target390.length,
    ),
    local_scope: 'target_002_390',
    decision:
      final004Target390.length >= 2 &&
      final004Target390.every((frame) => ['095', '125'].includes(frame.branch)) &&
      new Set(final004Target390.map((frame) => frame.branch)).size > 1
        ? 'candidate_split_scope_survives'
        : 'split_scope_weak_or_break',
    examples: examples(final004Target390),
    failures: examples(final004Target390.filter((frame) => !['095', '125'].includes(frame.branch))),
  },
  {
    checked_date: checkedDate,
    scope_bet: 'target390_parser_forecasts_no_internal_violations',
    frame_count: String(target390.length),
    pass_count: String(target390.length - targetViolations.length),
    fail_count: String(targetViolations.length),
    pass_share: safeShare(target390.length - targetViolations.length, target390.length),
    local_scope: 'target_002_390',
    decision: targetViolations.length === 0 ? 'forecast_table_internally_coherent' : 'forecast_table_has_breaks',
    examples: examples(target390),
    failures: examples(targetViolations),
  },
];

const decisions = [
  {
    checked_date: checkedDate,
    bet_id: 'V12_PARSER_FORECAST_SCOPE_20260531',
    confidence_tier:
      targetViolations.length === 0 &&
      final235P086Missing125.length === 0 &&
      contains032No235P086Has125.length === 0
        ? 'candidate'
        : 'wild shot',
    decision:
      contains032No235Has125.length > 0
        ? 'candidate_target_scope_with_global_032_exception'
        : 'candidate_forecasts_survive_current_scope',
    risky_parse_bet:
      'The current parser can generate explicit row-level forecasts for `002-390-X`, but its left-context rules have bounded scope: `235` rank trigger and `032` no-`235` suppression work locally/P086, not as accepted global sign values.',
    what_would_promote:
      'Held-out `002-390-X` rows satisfy the same forecast table, and broad governed-frame exceptions stay outside the declared local/P086 scope.',
    what_would_break:
      'Any target `002-390-X` forecast violation, especially terminal `390-125`, nonterminal closed X, or `032` no-`235` selecting `125`, breaks the current parser table.',
  },
];

const summary = {
  checked_date: checkedDate,
  status: 'parser_forecast_scope_test',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: canonicalRows.length,
    governed_frames: frames.length,
    target_002_390_frames: target390.length,
  },
  target_forecast_violations: targetViolations.length,
  global_032_no235_has125_exceptions: contains032No235Has125.length,
  p086_032_no235_has125_exceptions: contains032No235P086Has125.length,
  final235_p086_missing125: final235P086Missing125.length,
  decisions: decisions.map((row) => `${row.bet_id}:${row.decision}`).join(';'),
};

writeCsv(path.join(reportsDir, `${prefix}_target_forecasts.csv`), forecastRows, [
  'checked_date',
  'cisi',
  'row_id',
  'site',
  'type',
  'shape',
  'left',
  'left_final',
  'head',
  'branch',
  'tail',
  'terminal_after_branch',
  'left_forecasts',
  'x_forecasts',
  'forecast_violations',
  'provisional_parse',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_scope_tests.csv`), scopeRows, [
  'checked_date',
  'scope_bet',
  'frame_count',
  'pass_count',
  'fail_count',
  'pass_share',
  'local_scope',
  'decision',
  'examples',
  'failures',
]);

writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  'checked_date',
  'bet_id',
  'confidence_tier',
  'decision',
  'risky_parse_bet',
  'what_would_promote',
  'what_would_break',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
