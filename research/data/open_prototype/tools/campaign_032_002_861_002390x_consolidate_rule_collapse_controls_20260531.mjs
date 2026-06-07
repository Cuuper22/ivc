import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const parseRowsPath = path.join(
  reportsDir,
  'campaign_032_002_861_002390x_expand_x000_null_class_20260531_parse_rows_plus_000.csv',
);
const adjudicationTargetsPath = path.join(
  reportsDir,
  'campaign_032_002_861_002390x_expand_parse_adjudication_source_queue_20260531_targets.csv',
);
const prefix = 'campaign_032_002_861_002390x_consolidate_rule_collapse_controls_20260531';
const checkedDate = '2026-05-31';

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

function ratio(numerator, denominator) {
  return denominator ? `${numerator}/${denominator}` : '0/0';
}

function percentage(numerator, denominator) {
  return denominator ? numerator / denominator : 0;
}

function countMap(items, keyFn) {
  const counts = new Map();
  for (const item of items) {
    const key = keyFn(item) || '-';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return counts;
}

function countBy(items, keyFn) {
  return [...countMap(items, keyFn).entries()]
    .sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }))
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function topShare(items, keyFn) {
  if (!items.length) return 0;
  const counts = [...countMap(items, keyFn).values()];
  return Math.max(...counts) / items.length;
}

function distinctCount(items, keyFn) {
  return countMap(items, keyFn).size;
}

function ruleForRow(row) {
  if (row.x === '000') return 'NULL_000';
  if (row.predicted_class === 'terminal_identity_or_class_label') return 'TERMINAL_095';
  if (row.predicted_class === 'terminal_default_group_or_class_label') return 'TERMINAL_705';
  if (row.predicted_class === 'one_complement_associative_linker') return 'OPEN_530';
  if (
    ['head610_032_tail_router', 'head390_tail_menu_operator', 'dependent_title_chain_operator'].includes(
      row.predicted_class,
    )
  ) {
    return 'OPEN_125';
  }
  if (['head_routed_extender_bait', 'terminal_default_exception_bait', 'terminal_class_bait'].includes(row.predicted_class)) {
    return 'EXCEPTION_HOOKS';
  }
  return '';
}

function statusFor(rows, ruleId) {
  const covered = rows.filter((row) => row.prediction_pass !== '');
  const passing = covered.filter((row) => row.prediction_pass === 'true');
  const passRate = percentage(passing.length, covered.length);
  const siteN = distinctCount(rows, (row) => row.site);
  const headN = distinctCount(rows, (row) => row.head);
  const topSite = topShare(rows, (row) => row.site);
  const topHead = topShare(rows, (row) => row.head);
  if (ruleId === 'EXCEPTION_HOOKS') return 'demote_to_destructive_hooks';
  if (passRate < 0.95) return 'demote_prediction_failure';
  if (rows.length >= 20 && siteN >= 5 && topSite <= 0.5) return 'survives_collapse_control';
  if (rows.length >= 3 && siteN >= 2 && topSite < 0.75 && topHead < 0.75) return 'keep_candidate_but_source_gate';
  return 'keep_only_as_fragile_subrule';
}

function collapseReason(rows, ruleId) {
  const topSite = topShare(rows, (row) => row.site).toFixed(3);
  const topHead = topShare(rows, (row) => row.head).toFixed(3);
  if (ruleId === 'EXCEPTION_HOOKS') return 'These rows were already demoted; the control keeps them as kill switches only.';
  if (Number(topSite) >= 0.75) return `High site concentration: top_site_share=${topSite}.`;
  if (Number(topHead) >= 0.75) return `High head concentration: top_head_share=${topHead}.`;
  if (rows.length < 3) return 'Too few rows for rule-level promotion.';
  return `No immediate collapse: top_site_share=${topSite}; top_head_share=${topHead}.`;
}

fs.mkdirSync(reportsDir, { recursive: true });

const parseRows = parseCsv(fs.readFileSync(parseRowsPath, 'utf8'));
const adjudicationTargets = parseCsv(fs.readFileSync(adjudicationTargetsPath, 'utf8'));
const targetKeys = new Set(adjudicationTargets.map((row) => row.target));

const ruleIds = ['NULL_000', 'TERMINAL_095', 'TERMINAL_705', 'OPEN_530', 'OPEN_125', 'EXCEPTION_HOOKS'];
const rowsByRule = new Map(ruleIds.map((ruleId) => [ruleId, []]));
for (const row of parseRows) {
  const ruleId = ruleForRow(row);
  if (ruleId) rowsByRule.get(ruleId).push(row);
}

const ruleRows = ruleIds.map((ruleId) => {
  const rows = rowsByRule.get(ruleId);
  const covered = rows.filter((row) => row.prediction_pass !== '');
  const passing = covered.filter((row) => row.prediction_pass === 'true');
  const targetHits = rows.filter((row) => targetKeys.has(row.object) || targetKeys.has(row.row_id) || targetKeys.has(row.object.replace(/^-:/, '')));
  return {
    checked_date: checkedDate,
    rule_id: ruleId,
    rows: String(rows.length),
    pass: ratio(passing.length, covered.length),
    sites: String(distinctCount(rows, (row) => row.site)),
    heads: String(distinctCount(rows, (row) => row.head)),
    top_site_share: topShare(rows, (row) => row.site).toFixed(3),
    top_head_share: topShare(rows, (row) => row.head).toFixed(3),
    type_profile: countBy(rows, (row) => row.type),
    site_profile: countBy(rows, (row) => row.site),
    head_profile: countBy(rows, (row) => row.head),
    adjudication_targets: targetHits.map((row) => (row.object.startsWith('-:') ? row.row_id : row.object)).join(';') || '-',
    collapse_status: statusFor(rows, ruleId),
    collapse_reason: collapseReason(rows, ruleId),
    examples: rows.slice(0, 8).map((row) => `${row.object}:${row.gloss_skeleton}`).join(' | '),
  };
});

const decisions = ruleRows.map((row) => {
  const action =
    row.collapse_status === 'survives_collapse_control'
      ? 'rank_up_within_candidate'
      : row.collapse_status === 'demote_to_destructive_hooks' || row.collapse_status === 'demote_prediction_failure'
        ? 'demote'
        : 'keep_with_warning';
  return {
    checked_date: checkedDate,
    rule_id: row.rule_id,
    action,
    next_status: row.collapse_status,
    consequence:
      action === 'rank_up_within_candidate'
        ? 'Rule becomes the strongest current parser component, still below acceptance.'
        : action === 'demote'
          ? 'Rule cannot be a core parser component in this consolidation window.'
          : 'Rule remains live but cannot carry the parser without source or broader controls.',
    next_destructive_test:
      row.rule_id === 'NULL_000'
        ? 'Attack frame-proximal null with pre-frame terminal 000 or source-bound payload tails.'
        : row.rule_id === 'TERMINAL_095'
          ? 'Attack 095 with source-bound continuations and non-390 heads.'
          : row.rule_id === 'TERMINAL_705'
            ? 'Attack 705 with source-bound M-1825/4237.1 continuation or wrong-object binding.'
            : row.rule_id === 'OPEN_530'
              ? 'Attack 530 with complement count on H-773 and other 530 rows.'
              : row.rule_id === 'OPEN_125'
                ? 'Attack 125 with same-head tail inconsistency, especially 610 not followed by 032.'
                : 'Attack exception hooks with 3335.1 source/order and M-70 terminality.',
  };
});

const strongest = ruleRows.filter((row) => row.collapse_status === 'survives_collapse_control').map((row) => row.rule_id);
const fragile = ruleRows
  .filter((row) => ['keep_candidate_but_source_gate', 'keep_only_as_fragile_subrule'].includes(row.collapse_status))
  .map((row) => row.rule_id);
const demoted = ruleRows
  .filter((row) => row.collapse_status.startsWith('demote'))
  .map((row) => row.rule_id);

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: 'rule_collapse_controls',
  strongest,
  fragile,
  demoted,
  rule_count: ruleRows.length,
  compressed_consequence:
    'NULL_000 is the only rule that currently survives broad collapse controls; terminal/open layers remain live but source-gated or fragile; exception hooks stay demoted.',
};

writeCsv(path.join(reportsDir, `${prefix}_rules.csv`), ruleRows, [
  'checked_date',
  'rule_id',
  'rows',
  'pass',
  'sites',
  'heads',
  'top_site_share',
  'top_head_share',
  'type_profile',
  'site_profile',
  'head_profile',
  'adjudication_targets',
  'collapse_status',
  'collapse_reason',
  'examples',
]);
writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  'checked_date',
  'rule_id',
  'action',
  'next_status',
  'consequence',
  'next_destructive_test',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
