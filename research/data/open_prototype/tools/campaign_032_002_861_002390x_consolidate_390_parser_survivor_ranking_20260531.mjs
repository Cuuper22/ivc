// Consolidation scorecard for the 002-390-X campaign: after a dozen expand-phase
// experiments, which model pieces survived, and in what shape? This script does
// no new analysis of inscriptions. It reads twelve earlier expand-phase summary
// JSONs from data/open_prototype/reports/ (edge transfer, polarity tails, head
// signatures, negative controls, chain tests, frame-marker controls, and more)
// and hand-ranks the surviving pieces: the 002 frame license, 390 as a
// status/title head, the X polarity slot, 125 as a wounded linker, 095/705 as
// strengthened wild-shot terminal classifiers, and 000 as a damaged terminal.
// It also lists the claims that were killed, demoted, or blocked, and states
// the smallest parser that still stands. Writes model, killed, and
// minimal-parser CSVs plus a summary JSON with the next consolidation tests.

import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_consolidate_390_parser_survivor_ranking_20260531';
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
  const file = path.join(reportsDir, `${name}_summary.json`);
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

fs.mkdirSync(reportsDir, { recursive: true });

const summaries = {
  edge: readJson('campaign_032_002_861_002390x_expand_xslot_edge_transfer_20260531'),
  polarity: readJson('campaign_032_002_861_002390x_expand_xslot_polarity_tail_model_20260531'),
  head390: readJson('campaign_032_002_861_002390x_expand_head390_polarity_signature_20260531'),
  open: readJson('campaign_032_002_861_002390x_expand_open_operator_tail_complements_20260531'),
  c125: readJson('campaign_032_002_861_002390x_expand_125_complement_collapse_20260531'),
  function390: readJson('campaign_032_002_861_002390x_expand_390_function_bet_20260531'),
  negative: readJson('campaign_032_002_861_002390x_expand_390_negative_head_controls_20260531'),
  sourceClassifiers: readJson('campaign_032_002_861_002390x_expand_095705_classifier_source_surface_20260531'),
  parserRows: readJson('campaign_032_002_861_002390x_expand_390_provisional_parser_outputs_20260531'),
  order: readJson('campaign_032_002_861_002390x_expand_125_order_discriminator_20260531'),
  chain705: readJson('campaign_032_002_861_002390x_expand_705125_chain_test_20260531'),
  frame002: readJson('campaign_032_002_861_002390x_expand_002_frame_marker_control_20260531'),
};

const modelRows = [
  {
    checked_date: checkedDate,
    rank: 1,
    model_piece: '002_FRAME_LICENSE',
    tier: 'candidate',
    decision: 'keep',
    evidence:
      `002-framed 390 X-set enrichment ${summaries.frame002.enrichment}; framed in-set ${summaries.frame002.framed_390.in_set_rate} vs unframed ${summaries.frame002.unframed_390.in_set_rate}`,
    risk: 'source/type collapse could reduce enrichment',
  },
  {
    checked_date: checkedDate,
    rank: 2,
    model_piece: '390_STATUS_TITLE_HEAD',
    tier: 'candidate',
    decision: 'keep',
    evidence:
      `route split score ${summaries.negative.head390_route_separation_score}; no dangerous negative heads; terminal route 9/9 terminal, linker route 0/6 terminal`,
    risk: 'seal/tablet register could still fake status/title behavior',
  },
  {
    checked_date: checkedDate,
    rank: 3,
    model_piece: 'X_POLARITY_OPERATOR_SLOT',
    tier: 'candidate',
    decision: 'keep',
    evidence:
      'terminal boosters 84 rows with 7 nonterminal tails; open operators 44 rows with 35 nonterminal tails',
    risk: 'polarity classes may collapse under source/site/type controls',
  },
  {
    checked_date: checkedDate,
    rank: 4,
    model_piece: '125_LINKER_COMPLEMENT',
    tier: 'candidate_wounded',
    decision: 'keep',
    evidence:
      '125 has repeated complements 632/032/820; frame-local 002-390-125 rows are 4/4 head-linker-complement',
    risk: '632-032 lane is Mohenjo-daro-local; terminal 125 exceptions exist',
  },
  {
    checked_date: checkedDate,
    rank: 5,
    model_piece: '095_705_TERMINAL_CLASSIFIERS',
    tier: 'wild_shot_strengthened',
    decision: 'keep_but_do_not_promote',
    evidence:
      '095 is 3/3 terminal with public transcription-level H-1993; 705 is 4/5 terminal across Harappa/Mohenjo-daro/Dholavira',
    risk: 'source image binding missing for most rows; 705 has singleton nonterminal M-1668',
  },
  {
    checked_date: checkedDate,
    rank: 6,
    model_piece: '000_ZERO_DAMAGED_TERMINAL',
    tier: 'candidate_damaged',
    decision: 'keep_outside_390_core',
    evidence: '000 has constructional terminal boost but M-451 and 4148.1 remain damage',
    risk: 'source-bound M-451 may demote it further',
  },
];

const killedRows = [
  {
    checked_date: checkedDate,
    claim: '705_125_GENERAL_CHAIN',
    result: 'killed_as_general_rule',
    reason: `only ${summaries.chain705.chain_occurrences} 705-125 chain; M-1668 remains exception`,
  },
  {
    checked_date: checkedDate,
    claim: '000_AS_MERE_GLOBAL_EDGE_COPY',
    result: 'killed',
    reason: '000 has +0.452 constructional terminal delta in X slot',
  },
  {
    checked_date: checkedDate,
    claim: '390_COMMODITY_LABEL',
    result: 'demoted',
    reason: '390 route split is seal/tablet-heavy and status/title-like; commodity route has no current support',
  },
  {
    checked_date: checkedDate,
    claim: 'LANGUAGE_FAMILY_PROMOTION_FROM_125_ORDER',
    result: 'blocked',
    reason: 'frame-local order is head-linker-complement but broad 390/125/complement order is mixed',
  },
  {
    checked_date: checkedDate,
    claim: '590_AS_NORMAL_002_390_CLASSIFIER',
    result: 'demoted_to_leakage_or_mixed',
    reason: '390-590 dominates unframed 390 but appears once in 002-framed 390',
  },
];

const minimalParserRows = [
  {
    checked_date: checkedDate,
    slot: 'FRAME',
    sign: '002',
    parse: 'licenses status/title frame',
    tier: 'candidate',
  },
  {
    checked_date: checkedDate,
    slot: 'HEAD',
    sign: '390',
    parse: 'status/title head inside 002 frame',
    tier: 'candidate',
  },
  {
    checked_date: checkedDate,
    slot: 'X_TERMINAL',
    sign: '095/705',
    parse: 'overt terminal classifiers',
    tier: 'wild shot strengthened',
  },
  {
    checked_date: checkedDate,
    slot: 'X_LINKER',
    sign: '125',
    parse: 'linker to complement lane',
    tier: 'candidate wounded',
  },
  {
    checked_date: checkedDate,
    slot: 'COMPLEMENT',
    sign: '632/032/820',
    parse: 'complement classes after 125',
    tier: 'wild shot',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: '390_parser_survivor_ranking',
  smallest_parser:
    '002 FRAME -> 390 STATUS/TITLE HEAD -> X terminal-classifier or linker-complement polarity',
  kept_candidate_pieces: modelRows.filter((row) => row.decision.startsWith('keep')).map((row) => row.model_piece),
  killed_or_demoted: killedRows.map((row) => `${row.claim}:${row.result}`),
  next_consolidation_tests: [
    'source/type collapse of 002-framed 390 enrichment',
    'source binding for H-1993/M-1825/4237.1 classifier rows',
    'collapse 125 complement lanes by source/site',
  ],
};

writeCsv(path.join(reportsDir, `${prefix}_model_rows.csv`), modelRows, [
  'checked_date',
  'rank',
  'model_piece',
  'tier',
  'decision',
  'evidence',
  'risk',
]);
writeCsv(path.join(reportsDir, `${prefix}_killed_rows.csv`), killedRows, [
  'checked_date',
  'claim',
  'result',
  'reason',
]);
writeCsv(path.join(reportsDir, `${prefix}_minimal_parser_rows.csv`), minimalParserRows, [
  'checked_date',
  'slot',
  'sign',
  'parse',
  'tier',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
