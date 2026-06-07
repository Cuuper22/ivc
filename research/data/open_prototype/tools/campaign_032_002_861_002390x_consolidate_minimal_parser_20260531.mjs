import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_consolidate_minimal_parser_20260531';
const checkedDate = '2026-05-31';

function csvEscape(value) {
  const text = String(value ?? '');
  return /[",\n\r]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(',')];
  for (const row of rows) lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function readJson(name) {
  return JSON.parse(fs.readFileSync(path.join(reportsDir, name), 'utf8'));
}

fs.mkdirSync(reportsDir, { recursive: true });

const parseSummary = readJson('campaign_032_002_861_002390x_expand_x000_null_class_20260531_summary.json');
const adjudicationSummary = readJson(
  'campaign_032_002_861_002390x_expand_parse_adjudication_source_queue_20260531_summary.json',
);
const zeroSlotSummary = readJson('campaign_032_002_861_002390x_expand_x000_slot_specificity_20260531_summary.json');
const xTerminalitySummary = readJson('campaign_032_002_861_002390x_expand_xslot_terminality_null_20260531_summary.json');

const modelRows = [
  {
    checked_date: checkedDate,
    rank: '1',
    model_layer: 'frame',
    rule_id: 'MIN_FRAME_002_HEAD_X',
    tier: 'candidate',
    keep_status: 'keep_core',
    compressed_rule: 'Parse every live row as FRAME(002) HEAD(H) OPERATOR_OR_CLASS(X) TAIL(...).',
    support_now:
      `classified=${parseSummary.rows.parse_rows_plus_000_classified}/${parseSummary.rows.parse_rows_total}; pass=${parseSummary.rows.parse_rows_plus_000_pass}/${parseSummary.rows.parse_rows_plus_000_classified}.`,
    contradiction_now: 'No lexical/sign value yet; frame rule can still be a visual-register segmentation artifact.',
    kill_condition: 'Held-out/source-strict rows repeatedly refuse head/X continuation predictions.',
  },
  {
    checked_date: checkedDate,
    rank: '2',
    model_layer: 'null',
    rule_id: 'MIN_FRAME_PROXIMAL_NULL_000',
    tier: 'candidate',
    keep_status: 'merge_and_keep',
    compressed_rule:
      'Treat X=000 as the zero-complement subclass of a broader 002-licensed frame-proximal null operator.',
    support_now:
      `X000=${parseSummary.rows.x000_closed}/${parseSummary.rows.x000_rows} closed; frame_proximal=${zeroSlotSummary.frame_proximal_terminal}/${zeroSlotSummary.frame_proximal_occurrences} terminal; prefix_before_frame=${zeroSlotSummary.prefix_before_frame_terminal}/${zeroSlotSummary.prefix_before_frame_occurrences} terminal; xslot_null=${xTerminalitySummary.x000_terminal}.`,
    contradiction_now:
      'Head-slot and post-frame 000 also terminalize, so a purely X-specific explanation is too narrow.',
    kill_condition:
      'Source-strict pre-frame 000 closes, or frame-proximal 000 repeatedly carries meaningful non-null payload tails.',
  },
  {
    checked_date: checkedDate,
    rank: '3',
    model_layer: 'terminal_class',
    rule_id: 'MIN_TERMINAL_CLASS_095_705',
    tier: 'candidate',
    keep_status: 'keep_but_source_gate',
    compressed_rule:
      'Treat 095 and 705 as terminal identity/default-class operators unless source binding shows continuation.',
    support_now: '095 closes 3/3 in parser; 705 terminal default class has repeated 390-705 pressure but source gates remain live.',
    contradiction_now: '095 has H-1993 route pressure; 705 depends on M-1825 plus Dholavira 4237.1 binding.',
    kill_condition: 'Any source-bound 002-H-095-Y or 002-390-705-Y tail demotes the terminal-class rule.',
  },
  {
    checked_date: checkedDate,
    rank: '4',
    model_layer: 'open_operator',
    rule_id: 'MIN_OPEN_OPERATORS_530_125',
    tier: 'candidate',
    keep_status: 'keep_but_formula_risk',
    compressed_rule:
      'Treat 530 as one-complement linker and 125 as title/route operator whose behavior depends strongly on slot/head.',
    support_now: '530 one-complement rows pass 4/4; 610-125-032 repeats 2/2; 390-125 has tail-menu behavior.',
    contradiction_now: '125 is high formula-risk; 530 needs source-strict complement segmentation.',
    kill_condition:
      'Source-strict 530 takes zero/multiple payload complements, or 610-125 stops routing to 032.',
  },
  {
    checked_date: checkedDate,
    rank: '5',
    model_layer: 'exception_layer',
    rule_id: 'MIN_EXCEPTION_BAITS_590_692_707',
    tier: 'wild_shot',
    keep_status: 'demote_to_adjudication_hooks',
    compressed_rule:
      'Do not put 590/692/707 in the core parser yet; keep them as destructive controls for branch subtype behavior.',
    support_now: '3335.1 can promote 590 routed-extender only if source-bound; M-70 keeps 692 as terminal control.',
    contradiction_now: '3335.1 is unbound/private-source; 707 is singleton bait.',
    kill_condition: '3335.1 fails source binding or M-70 gains hidden continuation.',
  },
];

const decisions = [
  {
    checked_date: checkedDate,
    decision_id: 'CONSOLIDATE_KEEP_FRAME',
    action: 'keep',
    target: '002-H-X frame parser',
    reason: 'It is the smallest structure that carries all live parse bets and gives continuation predictions.',
    next_status: 'candidate',
  },
  {
    checked_date: checkedDate,
    decision_id: 'CONSOLIDATE_MERGE_000_RULES',
    action: 'merge',
    target: 'X=000 zero-complement + frame-proximal null operator',
    reason:
      'X=000 is real but too narrow: head-slot and post-frame 000 also terminalize, while pre-frame 000 never closes in the scan.',
    next_status: 'candidate',
  },
  {
    checked_date: checkedDate,
    decision_id: 'CONSOLIDATE_DEMOTE_NARROW_X000_ONLY',
    action: 'demote',
    target: 'purely X-specific 000 explanation',
    reason: 'The X-slot rule survives as a subclass, not as the full explanation.',
    next_status: 'demoted_to_subrule',
  },
  {
    checked_date: checkedDate,
    decision_id: 'CONSOLIDATE_KEEP_TERMINAL_CLASSES',
    action: 'keep',
    target: '095/705 terminal class layer',
    reason: 'They explain terminal behavior and have direct destructive source targets.',
    next_status: 'candidate_source_gated',
  },
  {
    checked_date: checkedDate,
    decision_id: 'CONSOLIDATE_KEEP_OPEN_OPERATORS',
    action: 'keep',
    target: '530/125 open operator layer',
    reason: 'They explain governed complements/routes and contrast with terminal classes.',
    next_status: 'candidate_formula_risk',
  },
  {
    checked_date: checkedDate,
    decision_id: 'CONSOLIDATE_DEMOTE_031_575_317',
    action: 'demote',
    target: '031/575/317 terminal near-misses',
    reason: 'They are terminality pressure from the null scan, but no independent role/function bet has survived yet.',
    next_status: 'next_expand_only_not_core',
  },
  {
    checked_date: checkedDate,
    decision_id: 'CONSOLIDATE_DEMOTE_590_692_707',
    action: 'demote',
    target: '590/692/707 exception baits',
    reason: 'They are useful destructive controls, not stable core grammar until source-bound.',
    next_status: 'wild_shot_adjudication_hooks',
  },
];

const nextTests = [
  {
    checked_date: checkedDate,
    test_id: 'NEXT_DESTROY_NULL_OPERATOR',
    phase_for_test: 'next_expand',
    target_rule: 'MIN_FRAME_PROXIMAL_NULL_000',
    exact_test:
      'Find or source-bind rows where pre-frame 000 closes, or where frame-proximal 000 has meaningful non-null payload tails.',
    promotion_result: 'No pre-frame terminal 000 plus continued X=000 closure promotes 000 null operator.',
    kill_result: 'Pre-frame terminal 000 or diverse post-000 payload kills positional null.',
  },
  {
    checked_date: checkedDate,
    test_id: 'NEXT_DESTROY_TERMINAL_CLASSES',
    phase_for_test: 'next_expand',
    target_rule: 'MIN_TERMINAL_CLASS_095_705',
    exact_test: 'Source-bind H-1993/M-71/L-1 and M-1825/4237.1 for terminal sign count after 095/705.',
    promotion_result: 'Terminal 095/705 across heads/sites promotes terminal-class layer.',
    kill_result: 'Any source-bound continuation after 095 or 390-705 demotes the layer.',
  },
  {
    checked_date: checkedDate,
    test_id: 'NEXT_DESTROY_OPEN_OPERATORS',
    phase_for_test: 'next_expand',
    target_rule: 'MIN_OPEN_OPERATORS_530_125',
    exact_test: 'Bind H-773 complement segmentation and H-74/M-1665 610-125-032 order.',
    promotion_result: 'One complement after 530 and repeated 610-125-032 promotes open-operator layer.',
    kill_result: 'Multiple/zero complements after 530 or non-032 tails after 610-125 kills the compact operator split.',
  },
  {
    checked_date: checkedDate,
    test_id: 'NEXT_DESTROY_EXCEPTION_LAYER',
    phase_for_test: 'next_expand',
    target_rule: 'MIN_EXCEPTION_BAITS_590_692_707',
    exact_test: 'Resolve 3335.1 source/order and use M-70 as terminal 692 control.',
    promotion_result: '3335.1 exact 590-032 plus M-70 terminal 692 promotes branch subtype split.',
    kill_result: '3335.1 false bridge/order failure or M-70 hidden tail collapses the exception layer.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: 'minimal_parser_v1',
  kept_core_rules: modelRows.filter((row) => row.keep_status.startsWith('keep') || row.keep_status === 'merge_and_keep').length,
  demoted_or_hook_rules: modelRows.filter((row) => row.keep_status.includes('demote')).length,
  decisions: decisions.length,
  next_tests: nextTests.length,
  source_adjudication_targets: adjudicationSummary.targets,
  compressed_parser:
    'FRAME(002) HEAD(H) OP(X): NULL(000/frame-proximal), TERMINAL_CLASS(095/705), OPEN_OPERATOR(530/125), EXCEPTION_HOOK(590/692/707).',
};

writeCsv(path.join(reportsDir, `${prefix}_model.csv`), modelRows, [
  'checked_date',
  'rank',
  'model_layer',
  'rule_id',
  'tier',
  'keep_status',
  'compressed_rule',
  'support_now',
  'contradiction_now',
  'kill_condition',
]);
writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  'checked_date',
  'decision_id',
  'action',
  'target',
  'reason',
  'next_status',
]);
writeCsv(path.join(reportsDir, `${prefix}_next_tests.csv`), nextTests, [
  'checked_date',
  'test_id',
  'phase_for_test',
  'target_rule',
  'exact_test',
  'promotion_result',
  'kill_result',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
