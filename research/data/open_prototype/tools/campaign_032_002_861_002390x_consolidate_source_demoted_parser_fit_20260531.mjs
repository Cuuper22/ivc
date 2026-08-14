// Re-scores the 002-390-X parser fit after applying source discipline. The
// earlier parser-fit run counted every metadata row equally; this one reads
// those parse rows plus the source-visible controls table, buckets each row by
// how good its source really is (strict source-visible, panel-bound,
// route-only, unbound, excluded), and demotes tiers accordingly: only
// strict-countable rows may support promotion, everything else is pressure.
// Each X sign gets a role (125 open linker, 095/705 terminal boosters, 692
// comparator, 530/590 extenders, singleton payloads) and a per-role capacity
// verdict. A destructive-tests table lists exactly which source bindings would
// promote or kill each claim. Writes row-reclassification, role-capacity, and
// destructive-tests CSVs plus a summary JSON to data/open_prototype/reports/.
// Headline: the structural self-fit stays 15/15, but only 4 rows survive as
// strict-countable — the parser must earn promotion from those 4 plus
// held-out tests, and accepted claims remain 0.

import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const checkedDate = '2026-05-31';
const prefix = 'campaign_032_002_861_002390x_consolidate_source_demoted_parser_fit_20260531';

const fitRowsPath = path.join(
  reportsDir,
  'campaign_032_002_861_002390x_consolidate_390_parser_fit_20260531_parse_rows.csv',
);
const sourceRowsPath = path.join(
  reportsDir,
  'campaign_032_002_861_002390x_consolidate_source_visible_parser_controls_20260531_source_rows.csv',
);

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
  for (const row of rows) lines.push(fields.map((fieldName) => csvEscape(row[fieldName])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function countBy(rows, key) {
  const counts = new Map();
  for (const row of rows) counts.set(row[key], (counts.get(row[key]) ?? 0) + 1);
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([value, count]) => `${value}:${count}`)
    .join(';');
}

function sourceKey(row) {
  if (row.object === '-' && row.site === 'Dholavira' && row.x === '705') return '4237.1';
  return row.object;
}

function sourceBucket(status) {
  if (status.startsWith('strict_source_visible')) return 'strict_countable';
  if (status.startsWith('panel_bound')) return 'downweighted_pressure';
  if (status.startsWith('not_ready')) return 'excluded_visual';
  if (status.startsWith('public_transcription')) return 'route_only';
  if (status.startsWith('source_image_candidate_unbound')) return 'unbound_candidate';
  if (status.startsWith('no_signband')) return 'source_blocked';
  if (status.startsWith('no_new_strict')) return 'exception_only';
  if (status === 'private_or_unknown_source_unbound') return 'unbound_private';
  return 'structural_only';
}

function roleClass(row) {
  if (row.x === '125') return '125_open_linker';
  if (row.x === '095') return '095_terminal_booster';
  if (row.x === '705') return '705_terminal_booster';
  if (row.x === '692') return '692_terminal_comparator';
  if (row.x === '530') return '530_open_extender';
  if (row.x === '590') return '590_open_extender_unbound';
  return 'singleton_terminal_payload';
}

function demotedTier(row, bucket, role) {
  if (role === '125_open_linker') {
    if (bucket === 'strict_countable') return 'candidate_source_visible';
    if (bucket === 'downweighted_pressure') return 'candidate_pressure_only';
    if (bucket === 'excluded_visual') return 'excluded_from_strict_counts';
  }
  if (role === '095_terminal_booster') {
    if (bucket === 'strict_countable') return 'wild_shot_singleton_source_visible';
    if (bucket === 'route_only') return 'route_pressure_only';
  }
  if (role === '705_terminal_booster') return 'wild_shot_source_blocked';
  if (role === '692_terminal_comparator') return 'strict_comparator_not_classifier';
  if (role === '530_open_extender') return 'candidate_structural_only';
  if (role === '590_open_extender_unbound') return 'wild_shot_unbound_private';
  return 'wild_shot_structural_singleton';
}

function roleDecision(role, rows) {
  const strict = rows.filter((row) => row.source_bucket === 'strict_countable').length;
  const blocked = rows.filter((row) =>
    ['source_blocked', 'unbound_candidate', 'unbound_private', 'route_only'].includes(row.source_bucket),
  ).length;
  if (role === '125_open_linker') {
    return strict >= 2
      ? 'keep as wounded candidate; strict support exists but formula/site risk remains'
      : 'demote; no strict repeated linker support';
  }
  if (role === '095_terminal_booster') {
    return strict === 1
      ? 'keep as wild shot singleton source-visible; do not promote'
      : 'demote to route/structural pressure only';
  }
  if (role === '705_terminal_booster') {
    return strict === 0 && blocked
      ? 'keep as structural wild shot only; source binding is destructive test'
      : 're-score if strict source witness appears';
  }
  if (role === '692_terminal_comparator') return 'keep as strict terminal comparator, not classifier';
  if (role === '530_open_extender') return 'keep as open-lane comparator; source-dark for this campaign';
  if (role === '590_open_extender_unbound') return 'demote to adjudication hook until 3335.1 source binds';
  return 'keep as singleton bait only';
}

fs.mkdirSync(reportsDir, { recursive: true });

const fitRows = parseCsv(fs.readFileSync(fitRowsPath, 'utf8'));
const sourceRows = parseCsv(fs.readFileSync(sourceRowsPath, 'utf8'));
const sourceByObject = new Map(sourceRows.map((row) => [row.object, row]));

const reclassifiedRows = fitRows.map((row) => {
  const key = sourceKey(row);
  const source = sourceByObject.get(key);
  const sourceStatus =
    source?.source_status ?? (row.object === '-' && row.site === 'Unknown' ? 'private_or_unknown_source_unbound' : 'not_in_source_visible_recheck');
  const bucket = sourceBucket(sourceStatus);
  const role = roleClass(row);
  const tier = demotedTier(row, bucket, role);
  return {
    checked_date: checkedDate,
    object: key,
    original_object: row.object,
    site: row.site,
    x: row.x,
    tail_after_x: row.tail_after_x,
    actual: row.actual,
    old_tier: row.tier,
    old_rule_class: row.rule_class,
    role,
    source_status: sourceStatus,
    source_bucket: bucket,
    demoted_tier: tier,
    parse_after_demotion:
      bucket === 'strict_countable'
        ? 'strictly_countable_for_role_shape'
        : bucket === 'excluded_visual'
          ? 'do_not_count_for_parser_fit'
          : 'pressure_only_not_promotion',
    text: row.text,
  };
});

const roles = [...new Set(reclassifiedRows.map((row) => row.role))].sort();
const roleRows = roles.map((role) => {
  const rows = reclassifiedRows.filter((row) => row.role === role);
  return {
    checked_date: checkedDate,
    role,
    rows: rows.length,
    strict_countable: rows.filter((row) => row.source_bucket === 'strict_countable').length,
    downweighted_pressure: rows.filter((row) => row.source_bucket === 'downweighted_pressure').length,
    route_or_unbound: rows.filter((row) =>
      ['route_only', 'unbound_candidate', 'unbound_private', 'source_blocked'].includes(row.source_bucket),
    ).length,
    excluded: rows.filter((row) => row.source_bucket === 'excluded_visual').length,
    structural_only: rows.filter((row) => row.source_bucket === 'structural_only').length,
    source_buckets: countBy(rows, 'source_bucket'),
    demoted_tiers: countBy(rows, 'demoted_tier'),
    decision: roleDecision(role, rows),
  };
});

const testRows = [
  {
    checked_date: checkedDate,
    test: 'H-1993 image binding',
    promotes_if: 'source image preserves terminal 002-390-095',
    kills_or_demotes_if: 'image lacks sequence, shows continuation, or row is mis-bound',
    affected_claim: '095 terminal booster',
  },
  {
    checked_date: checkedDate,
    test: 'M-1825 or 4237.1 source binding',
    promotes_if: 'at least one strict source image preserves terminal 002-390-705',
    kills_or_demotes_if: 'source-bound 705 is absent, nonterminal, or metadata-merged wrong',
    affected_claim: '705 terminal booster',
  },
  {
    checked_date: checkedDate,
    test: 'new strict 125 complement outside Mohenjo-daro 632-032',
    promotes_if: 'source-visible 002-390-125 takes a non-632032 complement at another site',
    kills_or_demotes_if: 'all strict 125 evidence collapses to Mohenjo-daro formula family',
    affected_claim: '125 open linker',
  },
  {
    checked_date: checkedDate,
    test: 'held-out 002-390-X polarity',
    promotes_if: 'terminal boosters close and open operators continue in source-strict rows',
    kills_or_demotes_if: 'held-out source-strict rows erase the terminal/open gap',
    affected_claim: 'X polarity slot',
  },
];

const strictRows = reclassifiedRows.filter((row) => row.source_bucket === 'strict_countable');
const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: 'source_demoted_parser_fit',
  total_002390x_rows: reclassifiedRows.length,
  strict_countable_rows: strictRows.length,
  strict_countable_objects: strictRows.map((row) => row.object),
  source_demoted_core:
    'Self-fit stays 15/15 structurally, but only 4 rows are strict-countable after source demotion; parser promotion must come from those 4 plus held-out tests.',
  keep: ['002_FRAME_LICENSE', '390_STATUS_TITLE_HEAD', 'X_POLARITY_SLOT', '125_OPEN_LINKER_SOURCE_VISIBLE_WOUNDED'],
  demote: ['705_TERMINAL_CLASSIFIER_TO_SOURCE_BLOCKED_WILD_SHOT', '095_TERMINAL_CLASSIFIER_TO_SINGLETON_WILD_SHOT'],
  accepted_claims: 0,
};

writeCsv(path.join(reportsDir, `${prefix}_row_reclassifications.csv`), reclassifiedRows, [
  'checked_date',
  'object',
  'original_object',
  'site',
  'x',
  'tail_after_x',
  'actual',
  'old_tier',
  'old_rule_class',
  'role',
  'source_status',
  'source_bucket',
  'demoted_tier',
  'parse_after_demotion',
  'text',
]);
writeCsv(path.join(reportsDir, `${prefix}_role_capacity.csv`), roleRows, [
  'checked_date',
  'role',
  'rows',
  'strict_countable',
  'downweighted_pressure',
  'route_or_unbound',
  'excluded',
  'structural_only',
  'source_buckets',
  'demoted_tiers',
  'decision',
]);
writeCsv(path.join(reportsDir, `${prefix}_destructive_tests.csv`), testRows, [
  'checked_date',
  'test',
  'promotes_if',
  'kills_or_demotes_if',
  'affected_claim',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
