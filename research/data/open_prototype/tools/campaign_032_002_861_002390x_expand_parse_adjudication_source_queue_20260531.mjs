import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const parseRowsPath = path.join(
  reportsDir,
  'campaign_032_002_861_002390x_expand_x000_null_class_20260531_parse_rows_plus_000.csv',
);
const prefix = 'campaign_032_002_861_002390x_expand_parse_adjudication_source_queue_20260531';
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

function countBy(items, keyFn) {
  const counts = new Map();
  for (const item of items) {
    const key = keyFn(item) || '-';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }))
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function rowKey(row) {
  if (row.object?.startsWith('-:')) return row.row_id;
  return row.object;
}

function targetRow(parseRows, key) {
  const row = parseRows.find((candidate) => rowKey(candidate) === key || candidate.object === key || candidate.row_id === key);
  if (!row) throw new Error(`Missing parse row for target ${key}`);
  return row;
}

const adjudicationPlan = [
  {
    key: 'H-1993',
    priority: 1,
    adjudicates_bet: 'SEM_095_RIGHT_EDGE_IDENTITY_LABEL; EXPAND_390_RIGHT_EDGE_HOST_BY_X_SUBTYPE',
    source_state_from_existing: 'CISI 3.1 supplement route and contact request exist; no artifact image/data row yet.',
    exact_source_success_implication:
      'Promotes 095 identity/class label from route-pressure to source-strict repeated 390-095 ecology, especially with M-71 as comparator.',
    variant_tail_implication:
      'If source shows 002-390-095-Y, terminal 095 dies first; 390 host may survive as an open operator context.',
    source_rejection_implication:
      'Demotes H-1993 to unusable route bait and leaves 095 dependent on L-1/M-71 only.',
    destructive_test:
      'Ask source to decide whether 095 is terminal on the inscribed side, not merely whether H-1993 exists.',
  },
  {
    key: 'M-71',
    priority: 2,
    adjudicates_bet: 'SEM_095_RIGHT_EDGE_IDENTITY_LABEL',
    source_state_from_existing: 'Earlier source-visible comparator in the 095 lane; use as same-head control for H-1993.',
    exact_source_success_implication:
      'Keeps 095 terminal under 390 even if H-1993 is still pending; strengthens the terminal identity/class label class.',
    variant_tail_implication:
      'A hidden tail after 095 would demote 095 from terminal class to open operator.',
    source_rejection_implication:
      'Removes the strongest 095 strict comparator and makes H-1993 acquisition much less interpretable.',
    destructive_test:
      'Check sign boundary after 095 and whether the preceding 390 is real, damaged, or copied from a formula lane.',
  },
  {
    key: 'L-1',
    priority: 3,
    adjudicates_bet: 'SEM_095_RIGHT_EDGE_IDENTITY_LABEL',
    source_state_from_existing: 'Local row gives non-390 head 812 with terminal 095; strictness needs separate source confidence.',
    exact_source_success_implication:
      'Shows 095 terminality is not only a 390 artifact; class-label reading becomes less head-specific.',
    variant_tail_implication:
      'If L-1 opens after 095 while 390-095 closes, 095 becomes head-conditioned rather than a general identity/class label.',
    source_rejection_implication:
      'Keeps 095 as a possible 390-only endpoint rather than a reusable X-class.',
    destructive_test:
      'Use L-1 as the non-390 holdout: 095 must close outside 390 to survive as a broader X role.',
  },
  {
    key: 'H-773',
    priority: 1,
    adjudicates_bet: 'SEM_530_GENITIVE_OR_ASSOCIATIVE_LINKER',
    source_state_from_existing: 'Panel/box-compatible route exists, but token strictness remains weaker than parser needs.',
    exact_source_success_implication:
      'Promotes 530 as one-complement linker: 002-390-530-741 reads as head plus linker plus a single governed complement.',
    variant_tail_implication:
      'If 530 takes multiple payload tails, associative-linker survives only as an open chaining operator, not one-complement grammar.',
    source_rejection_implication:
      'Demotes the 530 linker bet because H-773 is the clean 390-headed example.',
    destructive_test:
      'Force source to decide whether 741 is a complement governed by 530 or an independent following formula segment.',
  },
  {
    key: 'M-1825',
    priority: 1,
    adjudicates_bet: 'SEM_705_GROUP_OR_DEFAULT_CLASS_LABEL; EXPAND_705_ROLE_SWITCH_EXCEPTION',
    source_state_from_existing: 'CISI 3.1/source-contact route exists; public OCR gives no sign-band binding.',
    exact_source_success_implication:
      'Promotes 705 as terminal default/group class under 390 if paired with any other strict 390-705 row.',
    variant_tail_implication:
      'A visible tail after 705 demotes 705 from terminal class to head-conditioned operator or copied template.',
    source_rejection_implication:
      'Leaves Dholavira 4237.1 as the only repeated 390-705 route-pressure row; no promotion.',
    destructive_test:
      'Require exact terminal sign count after 705; secondary icon-only matches do not count.',
  },
  {
    key: '4237.1',
    priority: 1,
    adjudicates_bet: 'SEM_705_GROUP_OR_DEFAULT_CLASS_LABEL; EXPAND_705_ROLE_SWITCH_EXCEPTION',
    source_state_from_existing: 'Dholavira 8758/ZA-12:2 route is live but unbound; source reply did not have the needed page/object data.',
    exact_source_success_implication:
      'With M-1825, promotes 390-705 terminal default/group class across sites; without M-1825 it is strong pressure only.',
    variant_tail_implication:
      'If 705 continues or page-18 item 10 is a wrong-object bridge, 705 terminal class stays unpromoted.',
    source_rejection_implication:
      'Kills the Dholavira branch as a strict 705 witness and turns the page-18 route into visual-register bait.',
    destructive_test:
      'Bind accession/locus/dimensions to the exact six-sign sequence, or treat it as no evidence.',
  },
  {
    key: 'M-1668',
    priority: 2,
    adjudicates_bet: 'EXPAND_705_HEAD320_CAP_LICENSE',
    source_state_from_existing: 'Local row gives 320-705-125; source-image status not settled in the parser layer.',
    exact_source_success_implication:
      'Keeps 705 terminal-by-default but allows a head-320 cap exception where 125 closes the phrase.',
    variant_tail_implication:
      'If extra tail follows 125, the cap exception becomes an open formula and weakens role grammar.',
    source_rejection_implication:
      'Demotes the only clean 320-705-125 cap and makes 705 simpler but less explanatory.',
    destructive_test:
      'Check whether 125 is visually a cap after 705 or belongs to a separate copied formula segment.',
  },
  {
    key: 'H-74',
    priority: 2,
    adjudicates_bet: 'EXPAND_125_HEAD_CLASS_TAIL_ROUTER; EXPAND_125_ROLE_SWITCH_SURVIVES_SEAL_CONTROL',
    source_state_from_existing: 'Local Harappa seal row gives 610-125-032; use with M-1665 as repeated router pair.',
    exact_source_success_implication:
      'Promotes 610-125-032 as a title-chain route rule and supports positional role-switching for 125.',
    variant_tail_implication:
      'If 032 is absent or further payload continues, 125-router class weakens sharply.',
    source_rejection_implication:
      'Leaves M-1665 as singleton and blocks promotion of the 610 router.',
    destructive_test:
      'Verify 032 is actually after 125 and not a preposed or line-break artifact.',
  },
  {
    key: 'M-1665',
    priority: 2,
    adjudicates_bet: 'EXPAND_125_HEAD_CLASS_TAIL_ROUTER; EXPAND_125_ROLE_SWITCH_SURVIVES_SEAL_CONTROL',
    source_state_from_existing: 'Local Mohenjo-daro seal row gives 610-125-032; source status must support repeated-pair promotion.',
    exact_source_success_implication:
      'Cross-site repeat of 610-125-032 promotes the router rule from coincidence to candidate grammar.',
    variant_tail_implication:
      'A different tail after 125 under head 610 kills the clean router rule and turns 125 back into formula residue.',
    source_rejection_implication:
      'H-74 remains singleton and the 125 role-switch claim loses its most compact subrule.',
    destructive_test:
      'Check whether the long left prefix is independent of the 002-610-125-032 phrase or contaminates the segmentation.',
  },
  {
    key: '3335.1',
    priority: 1,
    adjudicates_bet: 'EXPAND_590_HEAD_ROUTED_EXTENDER; EXPAND_390_RIGHT_EDGE_HOST_BY_X_SUBTYPE',
    source_state_from_existing: 'Highest single-object matched-gate unlock, but private/unknown source and no independent bridge yet.',
    exact_source_success_implication:
      'Promotes 390-590-032 as a routed-extender exception paired against strict M-70 style 390-X terminal behavior.',
    variant_tail_implication:
      'If source order, object id, or tail differs, 590 extender is likely copied formula residue rather than grammar.',
    source_rejection_implication:
      'Kills the best non-125 continuing exception and simplifies 390-X toward terminal classes plus known 125/530 operators.',
    destructive_test:
      'Demand object/source binding and exact 590-032 order; a dataset-only row is not enough for this bet.',
  },
  {
    key: 'M-70',
    priority: 1,
    adjudicates_bet: 'EXPAND_692_HEAD455_416_EXCEPTION; EXPAND_390_RIGHT_EDGE_HOST_BY_X_SUBTYPE',
    source_state_from_existing: 'Source-visible control for 390-692 terminal behavior.',
    exact_source_success_implication:
      'Keeps 692 as terminal boundary bait under 390 and makes 3335.1 a sharper contrast if 590-032 binds.',
    variant_tail_implication:
      'A hidden tail after 692 collapses the 692/590 contrast and hurts the subtype parser.',
    source_rejection_implication:
      'Removes the clean 692 terminal control; M-70 cannot carry the branch subtype split.',
    destructive_test:
      'Use M-70 as a control, not as a discovery endpoint: terminal 692 must contrast with continuing 590.',
  },
  {
    key: 'H-609',
    priority: 2,
    adjudicates_bet: 'EXPAND_X000_ZERO_COMPLEMENT_CLASS',
    source_state_from_existing: 'Harappa seal zero-complement representative; source strictness not yet used for promotion.',
    exact_source_success_implication:
      'Promotes 000 zero-complement in a seal context with a nonzero head.',
    variant_tail_implication:
      'A meaningful non-null tail after 000 would damage the strongest high-coverage parser class.',
    source_rejection_implication:
      'Does not kill 000, but removes a useful Harappa seal representative.',
    destructive_test:
      'Look specifically for any non-null sign after final 000; damage brackets are secondary.',
  },
  {
    key: 'K-44',
    priority: 3,
    adjudicates_bet: 'EXPAND_X000_ZERO_COMPLEMENT_CLASS',
    source_state_from_existing: 'Kalibangan seal row with head 000 and X 000; useful stress test for null-chain ambiguity.',
    exact_source_success_implication:
      'Keeps zero-complement class alive even when head and X are both 000.',
    variant_tail_implication:
      'If the row has non-null continuation, double-000 is not simply null complement and may be damage/placeholder.',
    source_rejection_implication:
      'Demotes the double-000 example but leaves nonzero-head 000 rows intact.',
    destructive_test:
      'Check whether the second 000 is a real sign, missing/damaged sign marker, or segmentation placeholder.',
  },
  {
    key: 'TY-106',
    priority: 2,
    adjudicates_bet: 'EXPAND_X000_ZERO_COMPLEMENT_CLASS; TYPO_NOT_COMMODITY_NUMERAL_CORE',
    source_state_from_existing: 'Tepe Yahya pot row gives cross-domain zero-complement pressure.',
    exact_source_success_implication:
      'Promotes 000 as cross-domain parser zero and attacks a seal-only visual-register null.',
    variant_tail_implication:
      'If pot context opens after 000 with payload, 000 may be domain-conditioned rather than grammar-general.',
    source_rejection_implication:
      'Keeps zero-complement mainly seal/tablet-weighted and weakens typology extrapolation.',
    destructive_test:
      'Use pot context as a domain attack: 000 must still close or the class splits by object ecology.',
  },
  {
    key: 'Ns-66',
    priority: 2,
    adjudicates_bet: 'EXPAND_X000_ZERO_COMPLEMENT_CLASS',
    source_state_from_existing: 'Nausharo pot/graffiti row gives a reset exception after 000.',
    exact_source_success_implication:
      'Keeps the reset exception as structured grammar: 002-H-000-002 starts a new frame, not payload after 000.',
    variant_tail_implication:
      'If 002 is not a reset boundary, zero-complement exceptions become semantically diverse and the 000 class weakens.',
    source_rejection_implication:
      'Removes the clean reset exception but not the closed 000 core.',
    destructive_test:
      'The source must show whether the post-000 002 starts a separate frame or is continuous payload.',
  },
];

fs.mkdirSync(reportsDir, { recursive: true });

const parseRows = parseCsv(fs.readFileSync(parseRowsPath, 'utf8'));
const targets = adjudicationPlan.map((plan) => {
  const row = targetRow(parseRows, plan.key);
  return {
    checked_date: checkedDate,
    priority: String(plan.priority),
    target: plan.key,
    object: row.object,
    row_id: row.row_id,
    site: row.site,
    type: row.type,
    text: row.text,
    head: row.head,
    x: row.x,
    tail_after_x: row.tail_after_x,
    predicted_class: row.predicted_class,
    gloss_skeleton: row.gloss_skeleton,
    current_prediction_pass: row.prediction_pass,
    adjudicates_bet: plan.adjudicates_bet,
    source_state_from_existing: plan.source_state_from_existing,
    exact_source_success_implication: plan.exact_source_success_implication,
    variant_tail_implication: plan.variant_tail_implication,
    source_rejection_implication: plan.source_rejection_implication,
    destructive_test: plan.destructive_test,
  };
});

const classPressure = [...new Set(targets.map((row) => row.predicted_class))].map((predictedClass) => {
  const rows = targets.filter((row) => row.predicted_class === predictedClass);
  return {
    checked_date: checkedDate,
    predicted_class: predictedClass,
    targets: String(rows.length),
    priority_1_targets: String(rows.filter((row) => row.priority === '1').length),
    objects: rows.map((row) => row.target).join(';'),
    x_profile: countBy(rows, (row) => row.x),
    target_consequence: rows.map((row) => `${row.target}:${row.exact_source_success_implication}`).join(' | '),
    kill_consequence: rows.map((row) => `${row.target}:${row.variant_tail_implication}`).join(' | '),
  };
});

const bets = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_SOURCE_ADJUDICATION_AS_PARSER_DESTRUCTIVE_TEST',
    tier: 'candidate',
    risky_bet:
      'The live parser can be tested through a small set of source outcomes where exact binding, variant tail, or source rejection each changes a named parse class.',
    current_test:
      `targets=${targets.length}; priority_1=${targets.filter((row) => row.priority === '1').length}; classes=${countBy(targets, (row) => row.predicted_class)}.`,
    destructive_prediction:
      'If these target outcomes do not change parser rankings, the parser is decorative rather than falsifiable.',
    promotion_prediction:
      'If exact source success promotes the named classes and variant tails demote them, the parser has real adjudication hooks.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_HOLDOUT_SOURCE_BINDING_WILL_SPLIT_OPERATOR_CLASSES',
    tier: 'wild_shot',
    risky_bet:
      'The first source-bound surprises will not randomly damage all classes; they will split 095/705 terminal classes from 530/590/125 open operators.',
    current_test:
      `terminal targets=${targets.filter((row) => row.tail_after_x === '<END>').length}; open targets=${targets.filter((row) => row.tail_after_x !== '<END>').length}.`,
    destructive_prediction:
      'If source surprises scramble terminal and open classes equally, the branch-subtype parser is likely visual-register overfit.',
    promotion_prediction:
      'If terminal classes stay terminal and open operators keep governed tails, subtype grammar beats copied visual formula.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'parse_adjudication_source_queue',
  targets: targets.length,
  priority_1_targets: targets.filter((row) => row.priority === '1').length,
  classes: countBy(targets, (row) => row.predicted_class),
  x_profile: countBy(targets, (row) => row.x),
  rows_by_priority: countBy(targets, (row) => row.priority),
  bets: bets.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

writeCsv(path.join(reportsDir, `${prefix}_targets.csv`), targets, [
  'checked_date',
  'priority',
  'target',
  'object',
  'row_id',
  'site',
  'type',
  'text',
  'head',
  'x',
  'tail_after_x',
  'predicted_class',
  'gloss_skeleton',
  'current_prediction_pass',
  'adjudicates_bet',
  'source_state_from_existing',
  'exact_source_success_implication',
  'variant_tail_implication',
  'source_rejection_implication',
  'destructive_test',
]);
writeCsv(path.join(reportsDir, `${prefix}_class_pressure.csv`), classPressure, [
  'checked_date',
  'predicted_class',
  'targets',
  'priority_1_targets',
  'objects',
  'x_profile',
  'target_consequence',
  'kill_consequence',
]);
writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), bets, [
  'checked_date',
  'bet_id',
  'tier',
  'risky_bet',
  'current_test',
  'destructive_prediction',
  'promotion_prediction',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
