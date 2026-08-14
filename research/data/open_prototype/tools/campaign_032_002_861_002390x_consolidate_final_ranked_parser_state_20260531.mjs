// Writes down the final state of the 002-390-X campaign as a ranked ledger.
// This is a documentation script: it reads nothing and computes nothing — the
// eight ranked claims and five parser rules are hand-written from the results
// of the consolidate-phase runs, then serialized to CSV and JSON so downstream
// tools and future sessions have one authoritative snapshot. Each claim carries
// its tier (promoted candidate down to wild shot), the parse rule it licenses,
// why it survived, what still damages it, and the next test that could break
// it. The rank-1 claim is "002 licenses the 390 status/title frame"; accepted
// decipherment claims remain 0. Outputs go to
// data/open_prototype/reports/ as _state_rows.csv, _parser_rules.csv, and
// _summary.json under this script's prefix.

import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_consolidate_final_ranked_parser_state_20260531';
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

fs.mkdirSync(reportsDir, { recursive: true });

const stateRows = [
  {
    checked_date: checkedDate,
    rank: 1,
    claim: '002 licenses the 390 frame',
    tier: 'promoted candidate',
    parse_rule: '002 = FRAME/LICENSE marker before 390',
    why_survives: 'X-set enrichment survives 7/7 serious controls',
    main_damage: 'still metadata/statistical; not image/source proof',
    next_test: 'source-visible 002-390 rows should preserve X-set enrichment',
  },
  {
    checked_date: checkedDate,
    rank: 2,
    claim: '390 is status/title head inside 002 frame',
    tier: 'candidate',
    parse_rule: '390 = STATUS/TITLE HEAD when licensed by 002',
    why_survives: 'route split survives 6/7 serious controls and has no dangerous negative-head control',
    main_damage: 'non-Mohenjo rows damage the length-gap part of the route split',
    next_test: 'non-Mohenjo 390 rows must preserve polarity even if length gap weakens',
  },
  {
    checked_date: checkedDate,
    rank: 3,
    claim: 'X slot has polarity',
    tier: 'candidate',
    parse_rule: 'X chooses terminal/classifier lane or linker/complement lane',
    why_survives: 'terminal boosters mostly close; open operators mostly continue',
    main_damage: 'class memberships are not source-filtered enough',
    next_test: 'collapse X polarity by source/site/type and compare against random head controls',
  },
  {
    checked_date: checkedDate,
    rank: 4,
    claim: '125 is linker/complement operator',
    tier: 'candidate, wounded, source-visible',
    parse_rule: '125 opens a complement lane after the status/title head',
    why_survives: 'M-119 and M-735 are strict token-box-ready; mostly nonterminal; cross-site 032 and 820 lanes; frame-local order support',
    main_damage: 'exact 002-390-125 repeated lane is Mohenjo-daro-local 632-032',
    next_test: 'source/site collapse of 125-632-032 and held-out 125 complement rows',
  },
  {
    checked_date: checkedDate,
    rank: 5,
    claim: '095 is overt terminal classifier',
    tier: 'wild shot, singleton source-visible',
    parse_rule: '095 closes status/title frame as classifier sign',
    why_survives: 'M-71 is strict token-box-ready; H-1993 adds route-only pressure',
    main_damage: 'only one strict source-visible witness; H-1993 has no image binding',
    next_test: 'source image for H-1993 must preserve terminal 095',
  },
  {
    checked_date: checkedDate,
    rank: 6,
    claim: '705 is overt terminal classifier',
    tier: 'wild shot, structural-only source-blocked',
    parse_rule: '705 closes status/title frame as classifier sign if source binding survives',
    why_survives: 'structural terminal pattern 4/5 and Dholavira/Mohenjo-daro route pressure',
    main_damage: 'zero strict source-visible witnesses; M-1668 singleton nonterminal exception',
    next_test: 'source images for M-1825 and 4237.1 must preserve terminal 705',
  },
  {
    checked_date: checkedDate,
    rank: 7,
    claim: '632/032/820 are complement classes',
    tier: 'wild shot',
    parse_rule: 'complements after 125',
    why_survives: 'recur after 125',
    main_damage: '632-032 is site-local; 032 and 820 are tiny samples',
    next_test: 'held-out/source-visible rows must repeat complement classes after 125',
  },
  {
    checked_date: checkedDate,
    rank: 8,
    claim: '000 is zero/damaged terminal booster',
    tier: 'candidate, damaged',
    parse_rule: '000 closes or damages an X slot outside the 390 classifier core',
    why_survives: 'constructional terminal boost',
    main_damage: 'M-451 and 4148.1 exceptions still serious',
    next_test: 'M-451 crop/source and 4148.1 source binding',
  },
];

const parserRows = [
  {
    checked_date: checkedDate,
    rule_id: 'R1',
    condition: 'row contains 002-390-X',
    output: 'parse 002 as FRAME and 390 as STATUS/TITLE HEAD',
    tier: 'candidate',
  },
  {
    checked_date: checkedDate,
    rule_id: 'R2',
    condition: 'X is 095 and terminal',
    output: 'parse X as source-visible singleton overt terminal classifier',
    tier: 'wild shot singleton source-visible',
  },
  {
    checked_date: checkedDate,
    rule_id: 'R3',
    condition: 'X is 705 and terminal',
    output: 'parse X as structural-only source-blocked overt terminal classifier',
    tier: 'wild shot source-blocked',
  },
  {
    checked_date: checkedDate,
    rule_id: 'R4',
    condition: 'X is 125 and followed by tail',
    output: 'parse 125 as linker to complement tail',
    tier: 'candidate wounded source-visible',
  },
  {
    checked_date: checkedDate,
    rule_id: 'R5',
    condition: 'X is 530/590/692 or underpowered classifier',
    output: 'parse as unresolved branch, not a promoted sign role',
    tier: 'wild shot or demoted',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: 'final_ranked_parser_state',
  top_claim: '002 licenses 390 status/title frame',
  strongest_tier: 'promoted candidate',
  accepted_claims: 0,
  parser_rule:
    '002-390-X parses as FRAME + STATUS/TITLE HEAD + X polarity, with source-visible wounded 125 linker lane, singleton-source-visible 095 classifier, and source-blocked structural 705 classifier.',
};

writeCsv(path.join(reportsDir, `${prefix}_state_rows.csv`), stateRows, [
  'checked_date',
  'rank',
  'claim',
  'tier',
  'parse_rule',
  'why_survives',
  'main_damage',
  'next_test',
]);
writeCsv(path.join(reportsDir, `${prefix}_parser_rules.csv`), parserRows, [
  'checked_date',
  'rule_id',
  'condition',
  'output',
  'tier',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
