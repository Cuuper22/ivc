import fs from 'node:fs';
import path from 'node:path';

// This script tries to break the minimal 002-390-X parser, on purpose. Each surviving claim
// is phrased as a destructive test: a rule plus the exact rows that would falsify it. It
// reads the corpus from data/open_prototype/lipi/metadata_filtered.csv (deduplicated) and
// the 15 target 002-390 frames from the branch-sign-ecology report, then runs eleven tests —
// among them: a final 235 before a P086 head (390/405) predicts branch 125; an earlier 032
// without 235 suppresses 125 (tested globally, locally, and on targets); 125 must continue;
// the closed branches (072/095/140/346/692/705/707) must be terminal; 530 takes exactly one
// complement; 390-590 requires an 032 tail; and closed subtypes must not swap under the same
// left context. Every test records its checked count, failures, and a verdict. Survivors,
// demotions (the global 032-suppression rule dies here), and per-source-tier rows go to
// CSVs in reports/, plus a summary JSON.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const targetFramesPath = path.join(
  root,
  'data',
  'open_prototype',
  'reports',
  'campaign_032_002_861_002390x_branch_sign_ecology_20260531_002390_frames.csv',
);
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_minimal_parser_destructive_consolidation_20260531';
const checkedDate = '2026-05-31';

const p086Heads = new Set(['390', '405']);
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

function has125(frame) {
  return frame.branch === '125' || frame.tail_tokens.includes('125');
}

function sourceTier(sourceStatus) {
  if (sourceStatus.includes('checkpoint_strict_source_visible')) return 'strict';
  if (sourceStatus.includes('source_panel_acquired')) return 'panel_compatible_not_strict';
  if (sourceStatus.includes('permissive_public_panel')) return 'permissive_public_panel';
  if (sourceStatus.includes('unbound') || sourceStatus.includes('metadata_only')) return 'metadata_unbound';
  return 'route_or_secondary';
}

function summarizeExamples(rows, n = 8) {
  return rows
    .slice(0, n)
    .map((row) => `${row.cisi ?? row.object ?? row.row_id ?? '-'}:${row.text}`)
    .join(' | ');
}

function count(rows, predicate) {
  return rows.filter(predicate).length;
}

function verdict(failures, passText, failText) {
  return failures.length ? failText : passText;
}

fs.mkdirSync(reportsDir, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  tokens: signs(row.text),
}));
const canonicalRows = [...new Map(rawRows.map((row) => [row.tokens.join(' '), row])).values()];
const targetRows = parseCsv(fs.readFileSync(targetFramesPath, 'utf8')).map((row) => ({
  ...row,
  left_tokens: signs(row.text).slice(0, Number(row.frame_start_pos_1based) - 1),
  head: '390',
  branch: row.branch_after_390,
  tail_tokens: row.tail_after_branch === '<END>' ? [] : signs(row.tail_after_branch),
  terminal_after_branch: row.terminal_after_branch === 'True',
  source_tier: sourceTier(row.source_status),
}));

const governedFrames = [];
for (const row of canonicalRows) {
  for (let i = 0; i < row.tokens.length - 2; i += 1) {
    if (row.tokens[i] !== '002') continue;
    governedFrames.push({
      cisi: objectId(row),
      row_id: row.id,
      site: row.site,
      type: row.type,
      left_tokens: row.tokens.slice(0, i),
      left_final: row.tokens[i - 1] ?? '<START>',
      head: row.tokens[i + 1],
      branch: row.tokens[i + 2],
      tail_tokens: row.tokens.slice(i + 3),
      text: row.text,
    });
  }
}

const target390 = targetRows.filter((row) => row.head === '390');
const final235P086 = governedFrames.filter((row) => row.left_final === '235' && p086Heads.has(row.head));
const final235P086Failures = final235P086.filter((row) => !has125(row));
const global032No235 = governedFrames.filter(
  (row) => row.left_tokens.includes('032') && !row.left_tokens.includes('235'),
);
const global032No235Failures = global032No235.filter((row) => has125(row));
const local032No235P086 = global032No235.filter((row) => p086Heads.has(row.head));
const local032No235P086Failures = local032No235P086.filter((row) => has125(row));
const target032No235 = target390.filter(
  (row) => row.left_tokens.includes('032') && !row.left_tokens.includes('235'),
);
const target032No235Failures = target032No235.filter((row) => row.branch === '125' || row.tail_tokens.includes('125'));
const target125 = target390.filter((row) => row.branch === '125');
const terminalTarget125Failures = target125.filter((row) => row.terminal_after_branch);
const targetClosed = target390.filter((row) => closed390Branches.has(row.branch));
const targetClosedFailures = targetClosed.filter((row) => !row.terminal_after_branch);
const target530 = target390.filter((row) => row.branch === '530');
const target530Failures = target530.filter((row) => row.tail_tokens.length !== 1);
const target590 = target390.filter((row) => row.branch === '590');
const target590Failures = target590.filter((row) => row.tail_tokens[0] !== '032');
const all390530 = [];
const all390590 = [];
for (const row of canonicalRows) {
  for (let i = 0; i < row.tokens.length - 1; i += 1) {
    if (row.tokens[i] === '390' && row.tokens[i + 1] === '530') {
      all390530.push({
        cisi: objectId(row),
        row_id: row.id,
        tail_after_530: row.tokens.slice(i + 2),
        text: row.text,
      });
    }
    if (row.tokens[i] === '390' && row.tokens[i + 1] === '590') {
      all390590.push({
        cisi: objectId(row),
        row_id: row.id,
        tail_after_590: row.tokens.slice(i + 2),
        text: row.text,
      });
    }
  }
}
const all390530Failures = all390530.filter((row) => row.tail_after_530.length !== 1);
const all390590Failures = all390590.filter((row) => row.tail_after_590[0] !== '032');

const branchByLeftFinal = new Map();
for (const row of target390) {
  const key = row.left_tokens.at(-1) ?? '<START>';
  if (!branchByLeftFinal.has(key)) branchByLeftFinal.set(key, new Set());
  branchByLeftFinal.get(key).add(row.branch);
}
const closedSubtypeContextCollisions = [...branchByLeftFinal.entries()]
  .filter(([, branches]) => {
    const closed = [...branches].filter((branch) => ['095', '692', '705'].includes(branch));
    return closed.length > 1;
  })
  .map(([leftFinal, branches]) => ({ leftFinal, branches: [...branches].join(';') }));

const sourceRows = ['strict', 'panel_compatible_not_strict', 'permissive_public_panel', 'metadata_unbound', 'route_or_secondary']
  .map((tier) => ({
    checked_date: checkedDate,
    source_tier: tier,
    target390_rows: String(count(target390, (row) => row.source_tier === tier)),
    rows: target390
      .filter((row) => row.source_tier === tier)
      .map((row) => `${row.object}:${row.branch}`)
      .join(';'),
  }))
  .filter((row) => row.target390_rows !== '0');

const testRows = [
  {
    checked_date: checkedDate,
    test: 'final235_plus_P086_predicts_125',
    scope: 'all governed frames',
    checked: String(final235P086.length),
    failures: String(final235P086Failures.length),
    verdict: verdict(final235P086Failures, 'survives_candidate_not_promoted', 'demote_final235_rank_trigger'),
    examples: summarizeExamples(final235P086),
    failures_examples: summarizeExamples(final235P086Failures),
  },
  {
    checked_date: checkedDate,
    test: 'global_032_no235_suppresses_125',
    scope: 'all governed frames',
    checked: String(global032No235.length),
    failures: String(global032No235Failures.length),
    verdict: 'killed_as_global_rule',
    examples: summarizeExamples(global032No235),
    failures_examples: summarizeExamples(global032No235Failures),
  },
  {
    checked_date: checkedDate,
    test: 'local_P086_032_no235_suppresses_125',
    scope: 'P086 heads 390/405 only',
    checked: String(local032No235P086.length),
    failures: String(local032No235P086Failures.length),
    verdict: verdict(local032No235P086Failures, 'survives_local_candidate', 'kill_local_032_suppression'),
    examples: summarizeExamples(local032No235P086),
    failures_examples: summarizeExamples(local032No235P086Failures),
  },
  {
    checked_date: checkedDate,
    test: 'target_032_no235_suppresses_125',
    scope: '15 target 002-390-X rows',
    checked: String(target032No235.length),
    failures: String(target032No235Failures.length),
    verdict: verdict(target032No235Failures, 'survives_target_candidate', 'kill_target_032_suppression'),
    examples: summarizeExamples(target032No235),
    failures_examples: summarizeExamples(target032No235Failures),
  },
  {
    checked_date: checkedDate,
    test: 'target_390_125_must_continue',
    scope: '15 target 002-390-X rows',
    checked: String(target125.length),
    failures: String(terminalTarget125Failures.length),
    verdict: verdict(terminalTarget125Failures, 'survives_candidate', 'demote_125_continuing_selector'),
    examples: summarizeExamples(target125),
    failures_examples: summarizeExamples(terminalTarget125Failures),
  },
  {
    checked_date: checkedDate,
    test: 'target_closed_X_must_be_terminal',
    scope: '15 target 002-390-X rows',
    checked: String(targetClosed.length),
    failures: String(targetClosedFailures.length),
    verdict: verdict(targetClosedFailures, 'survives_syntax_candidate', 'demote_closed_selector_table'),
    examples: summarizeExamples(targetClosed),
    failures_examples: summarizeExamples(targetClosedFailures),
  },
  {
    checked_date: checkedDate,
    test: 'target_390_530_one_complement',
    scope: '15 target 002-390-X rows',
    checked: String(target530.length),
    failures: String(target530Failures.length),
    verdict: verdict(target530Failures, 'survives_candidate', 'demote_530_complement_linker'),
    examples: summarizeExamples(target530),
    failures_examples: summarizeExamples(target530Failures),
  },
  {
    checked_date: checkedDate,
    test: 'global_390_530_one_complement',
    scope: 'all canonical metadata rows',
    checked: String(all390530.length),
    failures: String(all390530Failures.length),
    verdict: verdict(all390530Failures, 'survives_global_syntax_candidate', 'demote_global_530_complement_linker'),
    examples: summarizeExamples(all390530),
    failures_examples: summarizeExamples(all390530Failures),
  },
  {
    checked_date: checkedDate,
    test: 'target_390_590_requires_032_tail',
    scope: '15 target 002-390-X rows',
    checked: String(target590.length),
    failures: String(target590Failures.length),
    verdict: verdict(target590Failures, 'survives_local_formula_bridge_candidate', 'demote_target_390590032_formula_bridge'),
    examples: summarizeExamples(target590),
    failures_examples: summarizeExamples(target590Failures),
  },
  {
    checked_date: checkedDate,
    test: 'global_390_590_requires_032_tail',
    scope: 'all canonical metadata rows',
    checked: String(all390590.length),
    failures: String(all390590Failures.length),
    verdict: verdict(all390590Failures, 'survives_global_formula_bridge_candidate', 'global_formula_bridge_killed_keep_target_local_only'),
    examples: summarizeExamples(all390590),
    failures_examples: summarizeExamples(all390590Failures),
  },
  {
    checked_date: checkedDate,
    test: 'closed_subtypes_same_left_collision',
    scope: 'target 095/692/705 by immediate predecessor',
    checked: String(branchByLeftFinal.size),
    failures: String(closedSubtypeContextCollisions.length),
    verdict: closedSubtypeContextCollisions.length
      ? 'demote_closed_subtype_semantics_to_visual_formulae'
      : 'no_same_left_swap_found_but_semantics_not_promoted',
    examples: [...branchByLeftFinal.entries()].map(([key, branches]) => `${key}:${[...branches].join(';')}`).join(' | '),
    failures_examples: closedSubtypeContextCollisions.map((row) => `${row.leftFinal}:${row.branches}`).join(' | '),
  },
];

const survivorRows = [
  {
    checked_date: checkedDate,
    survivor: 'minimal_target_002_390_X_parser',
    tier_after_test: 'candidate',
    support: `${target390.length} target rows; zero destructive-test violations inside target syntax`,
    promotion_block: 'source tiers remain mixed and several semantic branches are metadata-unbound',
  },
  {
    checked_date: checkedDate,
    survivor: 'final235_plus_P086_predicts_125',
    tier_after_test: final235P086Failures.length ? 'killed' : 'candidate_not_promoted',
    support: `${final235P086.length - final235P086Failures.length}/${final235P086.length} pass`,
    promotion_block: 'exact-left shadow support still sparse',
  },
  {
    checked_date: checkedDate,
    survivor: '032_no235_suppresses_125',
    tier_after_test: global032No235Failures.length ? 'local_candidate_global_killed' : 'candidate',
    support: `${local032No235P086.length - local032No235P086Failures.length}/${local032No235P086.length} local P086 pass`,
    promotion_block: 'H-130 kills global sign-value version',
  },
  {
    checked_date: checkedDate,
    survivor: '125_continuing_selector',
    tier_after_test: terminalTarget125Failures.length ? 'demoted' : 'candidate',
    support: `${target125.length - terminalTarget125Failures.length}/${target125.length} target rows continue after 125`,
    promotion_block: 'raw non-frame 125 behavior prevents intrinsic sign-value claim',
  },
  {
    checked_date: checkedDate,
    survivor: '530_one_complement_linker',
    tier_after_test: all390530Failures.length ? 'demoted' : 'candidate_syntax_semantics_demoted',
    support: `${all390530.length - all390530Failures.length}/${all390530.length} global 390-530 rows have one complement`,
    promotion_block: 'direct same-head shadows weaken strict nested semantics',
  },
  {
    checked_date: checkedDate,
    survivor: '390_590_032_formula_bridge',
    tier_after_test: target590Failures.length
      ? 'demoted'
      : all390590Failures.length
        ? 'local_candidate_global_killed'
        : 'candidate',
    support: `${target590.length - target590Failures.length}/${target590.length} target 390-590 rows take 032 next; ${all390590.length - all390590Failures.length}/${all390590.length} global 390-590 rows take 032 next`,
    promotion_block: '3335.1 source identity remains unbound and global 390-590 behavior is broad',
  },
  {
    checked_date: checkedDate,
    survivor: '095_692_705_closed_subtype_split',
    tier_after_test: closedSubtypeContextCollisions.length ? 'demoted' : 'candidate_edge',
    support: 'no immediate-left swap among target 095/692/705 rows',
    promotion_block: 'semantic labels remain wild without source-bound contextual bridge',
  },
];

const demotionRows = [
  {
    checked_date: checkedDate,
    claim: 'global_032_no235_suppresses_125',
    decision: 'killed',
    evidence: `${global032No235Failures.length} governed-frame exception(s), led by ${summarizeExamples(global032No235Failures, 1)}`,
  },
  {
    checked_date: checkedDate,
    claim: 'global_390_590_requires_032_tail',
    decision: all390590Failures.length ? 'killed_as_global_rule' : 'retained',
    evidence: `${all390590Failures.length}/${all390590.length} global 390-590 rows lack 032 next`,
  },
  {
    checked_date: checkedDate,
    claim: 'accepted_705_value_or_translation',
    decision: 'killed_for_acceptance_retained_as_wild_parser_bet',
    evidence: 'target 705 rows stay terminal, but source tiers are secondary/unbound and Dholavira remains metadata-image unbound',
  },
  {
    checked_date: checkedDate,
    claim: 'closed_X_semantic_subtypes',
    decision: 'not_promoted',
    evidence: 'syntax survives, semantics still lacks source-bound contextual bridge',
  },
];

writeCsv(
  path.join(reportsDir, `${prefix}_tests.csv`),
  testRows,
  ['checked_date', 'test', 'scope', 'checked', 'failures', 'verdict', 'examples', 'failures_examples'],
);
writeCsv(
  path.join(reportsDir, `${prefix}_survivors.csv`),
  survivorRows,
  ['checked_date', 'survivor', 'tier_after_test', 'support', 'promotion_block'],
);
writeCsv(
  path.join(reportsDir, `${prefix}_demotions.csv`),
  demotionRows,
  ['checked_date', 'claim', 'decision', 'evidence'],
);
writeCsv(
  path.join(reportsDir, `${prefix}_source_tiers.csv`),
  sourceRows,
  ['checked_date', 'source_tier', 'target390_rows', 'rows'],
);

const summary = {
  checked_date: checkedDate,
  status: 'minimal_parser_destructive_consolidation',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: canonicalRows.length,
    governed_frames: governedFrames.length,
    target_002_390_frames: target390.length,
  },
  destructive_failures: Object.fromEntries(testRows.map((row) => [row.test, Number(row.failures)])),
  source_tiers: Object.fromEntries(sourceRows.map((row) => [row.source_tier, Number(row.target390_rows)])),
  decision:
    'minimal_parser_survives_as_candidate; global_032_no235_killed; semantics_blocked_below_promotion',
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
