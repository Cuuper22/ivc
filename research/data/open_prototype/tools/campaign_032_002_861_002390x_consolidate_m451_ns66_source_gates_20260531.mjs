// Records the source gates on the two exceptions that wound the X=000 terminal
// candidate: M-451 (a zero chain with tail 906-388 after 000) and Ns-66 (a
// final 002 after 000-002 that could be a frame reset). For each, this script
// pulls the full metadata row, carries over the matching rows from the earlier
// x000 exception-family-collapse sequence summary, and logs the public search
// results. The one real find, baked in here: a public Parpola SAA 2001 PDF
// binds M-451 to object DK-B 960 and describes a single-line inscription, so
// the 906-388 tail probably is on the same line — source-bound damage to the
// simple zero-complement rule, though the poor photo prevents a full kill.
// Ns-66 found no public bridge and stays a metadata-only exception. Writes
// targets, sequence gates, public searches, and adjudication CSVs plus a
// summary JSON (with the next destructive tests) to data/open_prototype/reports/.

import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const familyPrefix = 'campaign_032_002_861_002390x_consolidate_x000_exception_family_collapse_20260531';
const prefix = 'campaign_032_002_861_002390x_consolidate_m451_ns66_source_gates_20260531';
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

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function sourceStrength(row) {
  if (row.cisi === 'M-451') {
    return [
      'public_source_bound',
      'parpola_2005_fig1_dk_b_960_m451',
      'layout_single_line_indus_inscription',
      'photo_poor_sign_level_not_fully_adjudicated',
    ].join(';');
  }
  if (row.cisi === 'Ns-66') {
    return [
      'metadata_with_cisi',
      'nausharo_period_and_material_present',
      'dimensions_excavation_public_bridge_missing',
    ].join(';');
  }
  return 'not_target';
}

fs.mkdirSync(reportsDir, { recursive: true });

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
}));
const sequenceRows = parseCsv(
  fs.readFileSync(path.join(reportsDir, `${familyPrefix}_sequence_summary.csv`), 'utf8'),
);

const targets = ['M-451', 'Ns-66'];
const targetRows = targets.map((target) => {
  const row = metadataRows.find((candidate) => candidate.object === target);
  if (!row) throw new Error(`Missing ${target} in metadata_filtered.csv`);
  return {
    checked_date: checkedDate,
    target,
    row_id: row.id,
    site: row.site,
    region: row.region,
    type: row.type,
    symbol: row.symbol,
    condition: row.condition,
    complete: row.complete,
    dir: row['dir.'],
    material: row.material,
    shape: row.shape,
    excavation_idno: row['excavation-idno'],
    area_section: row['area-section'],
    block_house: row['block-house'],
    room_grid: row['room-grid'],
    horizontal_mm: row['horizontal(mm)'],
    vertical_mm: row['vertical(mm)'],
    thickness_mm: row['thickness(mm)'],
    text: row.text,
    source_strength: sourceStrength(row),
  };
});

const sequenceGateRows = sequenceRows
  .filter((row) => targets.includes(row.target))
  .map((row) => ({
    checked_date: checkedDate,
    target: row.target,
    label: row.label,
    occurrences: row.occurrences,
    sites: row.sites,
    types: row.types,
    prev1: row.prev1,
    next1: row.next1,
    at_end: row.at_end,
    consequence_for_x000:
      row.target === 'M-451'
        ? 'tests_zero_chain_payload_after_x000'
        : 'tests_frame_reset_after_x000',
    adjudication: row.adjudication,
  }));

const publicSearchRows = [
  {
    checked_date: checkedDate,
    target: 'M-451',
    query: '"+000-002-520-000-000-000-906-388"',
    result: 'no exact transcription bridge found',
    strongest_source: 'none',
    parse_effect: 'no_sign_level_adjudication',
  },
  {
    checked_date: checkedDate,
    target: 'M-451',
    query: '"000-002-520-000-000-000-906-388"',
    result: 'no exact transcription bridge found',
    strongest_source: 'none',
    parse_effect: 'no_sign_level_adjudication',
  },
  {
    checked_date: checkedDate,
    target: 'M-451',
    query: '"M-451" "DK-B 960" Indus',
    result:
      'public Parpola SAA 2001 PDF binds DK-B 960 to M-451/Fig.1 and describes one side as an Indus seal impression with a single-line inscription',
    strongest_source:
      'https://tuhat.helsinki.fi/ws/portalfiles/portal/127257571/Parpola_A_2005._Contact_between_Harappans_Bactrians._SAA_2001.pdf',
    parse_effect:
      'damages_simple_zero_complement_if_local_tail_906_388_is_correct_payload_but_poor_photo_prevents_full_kill',
  },
  {
    checked_date: checkedDate,
    target: 'M-451',
    query: '"M-451" Mohenjo-daro "906-388"',
    result: 'no public sign-level bridge for 906-388 found',
    strongest_source: 'none',
    parse_effect: 'tail_payload_status_unresolved',
  },
  {
    checked_date: checkedDate,
    target: 'Ns-66',
    query: '"+033-999-400-090-740-100-000-002-892-000-002"',
    result: 'no exact transcription bridge found',
    strongest_source: 'none',
    parse_effect: 'no_source_adjudication',
  },
  {
    checked_date: checkedDate,
    target: 'Ns-66',
    query: '"033-999-400-090-740-100-000-002-892-000-002"',
    result: 'no exact transcription bridge found',
    strongest_source: 'none',
    parse_effect: 'no_source_adjudication',
  },
  {
    checked_date: checkedDate,
    target: 'Ns-66',
    query: '"Ns-66" Nausharo Indus',
    result: 'false-positive NS-66 product/legal pages; no Nausharo IVC object bridge found',
    strongest_source: 'none',
    parse_effect: 'reset_exception_remains_metadata_only',
  },
  {
    checked_date: checkedDate,
    target: 'Ns-66',
    query: '"Nausharo" "892-000-002"',
    result: 'no target row/source bridge found',
    strongest_source: 'none',
    parse_effect: 'reset_exception_remains_metadata_only',
  },
];

const adjudicationRows = [
  {
    checked_date: checkedDate,
    target: 'M-451',
    source_state: 'object_source_bound_layout_source_bound_sign_level_not_fully_readable',
    previous_status: 'zero_chain_singleton_pressure',
    new_status: 'source_bound_damage_to_simple_zero_complement',
    effect_on_x000:
      'demote_from_strong_core_subrule_to_candidate_with_serious_M451_damage_unless_tail_is_damage_or_terminal_material',
    reason:
      'Parpola binds DK-B 960/M-451 and describes a single-line Indus inscription; if local 906-388 tail is correct, material after X=000 is not merely a separate side.',
  },
  {
    checked_date: checkedDate,
    target: 'M-451',
    source_state: 'poor_photo_originally_longer_inscription',
    previous_status: 'unresolved_tail_payload',
    new_status: 'not_a_full_kill',
    effect_on_x000: 'do_not_accept_do_not_promote',
    reason:
      'The same source also leaves sign-level uncertainty because the object is poor/incomplete and the publication says the line originally had more signs than now visible.',
  },
  {
    checked_date: checkedDate,
    target: 'Ns-66',
    source_state: 'no_public_bridge_found',
    previous_status: 'reset_singleton_pressure',
    new_status: 'unresolved_metadata_only_reset_exception',
    effect_on_x000: 'less_weight_than_M451_or_4148_but_still_blocks_promotion',
    reason:
      'Final 002 could be frame reset, but no source/layout evidence currently decides whether it starts a new frame or remains payload.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: 'm451_ns66_source_gates',
  strongest_new_result: 'M451_public_source_bound_DKB960_Fig1_single_line_layout_damage',
  m451_effect:
    'simple_X000_zero_complement_demoted_to_candidate_with_serious_source_bound_M451_damage_not_fully_killed',
  ns66_effect: 'metadata_only_reset_exception_unresolved_less_dangerous_than_M451',
  current_smallest_model:
    'FRAME(002)-HEAD(H)-X with X000 as zero_or_damaged_terminal_operator_candidate, no longer strong core without explaining M451',
  next_destructive_tests: [
    'read or crop Parpola Fig1/M-451 sign line closely enough to decide whether 906-388 is local tail payload',
    'test whether 906-388 behaves as independent terminal boundary material outside M-451',
    'test whether post-X000 002 usually restarts frames in source-visible rows before using Ns-66 as repair',
  ],
};

writeCsv(path.join(reportsDir, `${prefix}_targets.csv`), targetRows, [
  'checked_date',
  'target',
  'row_id',
  'site',
  'region',
  'type',
  'symbol',
  'condition',
  'complete',
  'dir',
  'material',
  'shape',
  'excavation_idno',
  'area_section',
  'block_house',
  'room_grid',
  'horizontal_mm',
  'vertical_mm',
  'thickness_mm',
  'text',
  'source_strength',
]);
writeCsv(path.join(reportsDir, `${prefix}_sequence_gates.csv`), sequenceGateRows, [
  'checked_date',
  'target',
  'label',
  'occurrences',
  'sites',
  'types',
  'prev1',
  'next1',
  'at_end',
  'consequence_for_x000',
  'adjudication',
]);
writeCsv(path.join(reportsDir, `${prefix}_public_searches.csv`), publicSearchRows, [
  'checked_date',
  'target',
  'query',
  'result',
  'strongest_source',
  'parse_effect',
]);
writeCsv(path.join(reportsDir, `${prefix}_adjudication.csv`), adjudicationRows, [
  'checked_date',
  'target',
  'source_state',
  'previous_status',
  'new_status',
  'effect_on_x000',
  'reason',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
