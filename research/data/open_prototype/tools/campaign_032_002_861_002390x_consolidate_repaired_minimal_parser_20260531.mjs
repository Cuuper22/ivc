import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_consolidate_repaired_minimal_parser_20260531';
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

const collapse = readJson('campaign_032_002_861_002390x_consolidate_rule_collapse_controls_20260531_summary.json');
const repair = readJson('campaign_032_002_861_002390x_consolidate_x000_null_argument_repair_20260531_summary.json');

const modelRows = [
  {
    checked_date: checkedDate,
    rank: '1',
    rule_id: 'REPAIRED_FRAME_002_HEAD_X',
    tier: 'candidate',
    status: 'core',
    rule:
      'Use FRAME(002) HEAD(H) OP(X) as the live parser scaffold, but do not infer lexical value or language identity.',
    support: 'Carries all current continuation tests and source-adjudication hooks.',
    demotion_from_previous: 'none',
    kill_condition: 'Held-out/source-bound rows repeatedly violate head/X continuation predictions.',
  },
  {
    checked_date: checkedDate,
    rank: '2',
    rule_id: 'REPAIRED_X000_ZERO_COMPLEMENT',
    tier: 'candidate',
    status: 'strongest_core_subrule',
    rule: 'Treat X=000 as the clean zero-complement operator inside the 002-H-X parser.',
    support: `Collapse control: ${collapse.strongest.join(';')}; repaired contrast: ${repair.repaired_findings.x_slot_000}.`,
    demotion_from_previous:
      'This replaces the broader frame-proximal-null core claim; frame-proximal behavior is now edge evidence only.',
    kill_condition: 'Source-bound X=000 rows carry diverse meaningful payload tails, or nonzero X terminality erases the gap.',
  },
  {
    checked_date: checkedDate,
    rank: '3',
    rule_id: 'REPAIRED_HEADSLOT_000_EDGE',
    tier: 'candidate_edge',
    status: 'edge_not_core',
    rule: 'Head-slot 000 may be a related null/zero sign, but it is not allowed to prove the X-slot rule.',
    support: repair.repaired_findings.head_slot_000,
    demotion_from_previous: 'Demoted from broad frame-proximal null core to edge candidate.',
    kill_condition: 'Head-slot 000 behaves like ordinary head-slot terminality after source/register controls.',
  },
  {
    checked_date: checkedDate,
    rank: '4',
    rule_id: 'REPAIRED_TERMINAL_CLASSES_095_705',
    tier: 'candidate_source_gated',
    status: 'live_not_load_bearing',
    rule: 'Treat 095/705 as terminal class operators only while their source rows stay terminal.',
    support: '095 and 705 pass local continuation checks but remain small and source-sensitive.',
    demotion_from_previous: 'No demotion; they remain below X=000 in rank.',
    kill_condition: 'Any source-bound continuation after 095 or 390-705.',
  },
  {
    checked_date: checkedDate,
    rank: '5',
    rule_id: 'REPAIRED_OPEN_OPERATORS_530_125',
    tier: 'candidate_formula_risk',
    status: 'live_not_load_bearing',
    rule: 'Treat 530 as complement linker and 125 as head/slot-conditioned route/title operator.',
    support: '530 and 125 pass local continuation checks but need source and formula-family attacks.',
    demotion_from_previous: 'No demotion; 125 remains formula-risked.',
    kill_condition: '530 complement count breaks, or 610-125 stops routing to 032.',
  },
  {
    checked_date: checkedDate,
    rank: '6',
    rule_id: 'REPAIRED_EXCEPTION_HOOKS_590_692_707',
    tier: 'wild_shot',
    status: 'destructive_hooks_only',
    rule: 'Use 590/692/707 only to break or promote branch subtype grammar; do not parse them as core.',
    support: 'They have target hooks but not stable source-bound grammar.',
    demotion_from_previous: 'Already demoted; unchanged.',
    kill_condition: '3335.1 false bridge/order failure or M-70 hidden continuation.',
  },
  {
    checked_date: checkedDate,
    rank: '7',
    rule_id: 'REPAIRED_BROAD_FRAME_PROXIMAL_NULL',
    tier: 'wild_shot',
    status: 'demoted_evidence_not_rule',
    rule: 'Do not use broad frame-proximal 000 as a core rule in this consolidation window.',
    support: 'Pre-frame terminality control was tautological; post-frame 000 gap is too small.',
    demotion_from_previous:
      'Demoted from candidate core in minimal_parser_v1 after repaired same-role contrasts.',
    kill_condition: 'This only revives if future role-matched/source-bound controls show 000-specific null behavior outside X slot.',
  },
];

const decisions = [
  {
    checked_date: checkedDate,
    decision_id: 'REPAIR_CORE_NULL_RULE',
    decision: 'core_null_is_x000_not_broad_frame_proximal',
    reason:
      'The pre-frame control was not valid evidence, and post-frame 000 does not beat same-role nonzero signs enough.',
  },
  {
    checked_date: checkedDate,
    decision_id: 'REPAIR_RANKING',
    decision: 'rank_x000_above_all_other_parse_components',
    reason:
      'X=000 is the only component that survives collapse controls and the repaired terminality null.',
  },
  {
    checked_date: checkedDate,
    decision_id: 'REPAIR_NEXT_EXPAND_PRIORITY',
    decision: 'next_expand_should_try_to_kill_x000_first',
    reason:
      'A serious model attacks its strongest surviving rule before decorating weaker ones.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: 'repaired_minimal_parser_v2',
  core: ['REPAIRED_FRAME_002_HEAD_X', 'REPAIRED_X000_ZERO_COMPLEMENT'],
  edge_or_live: ['REPAIRED_HEADSLOT_000_EDGE', 'REPAIRED_TERMINAL_CLASSES_095_705', 'REPAIRED_OPEN_OPERATORS_530_125'],
  demoted: ['REPAIRED_EXCEPTION_HOOKS_590_692_707', 'REPAIRED_BROAD_FRAME_PROXIMAL_NULL'],
  parser:
    'FRAME(002) HEAD(H) OP(X), with X=000 zero-complement as strongest core subrule; 095/705 terminal classes and 530/125 open operators live but not load-bearing.',
};

writeCsv(path.join(reportsDir, `${prefix}_model.csv`), modelRows, [
  'checked_date',
  'rank',
  'rule_id',
  'tier',
  'status',
  'rule',
  'support',
  'demotion_from_previous',
  'kill_condition',
]);
writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  'checked_date',
  'decision_id',
  'decision',
  'reason',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
