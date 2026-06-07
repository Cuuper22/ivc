import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_consolidate_906388_boundary_control_20260531';
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

function tokens(text) {
  return (text.match(/\d{3}/g) ?? []).map((token) => token.padStart(3, '0'));
}

function tally(values) {
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([value, count]) => `${value}:${count}`)
    .join(';');
}

function nearestFrameBefore(signs, index) {
  for (let i = index - 1; i >= 0; i -= 1) {
    if (signs[i] === '002') return i;
  }
  return -1;
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));

const pairRows = [];
const sign906Rows = [];
const sign388Rows = [];

for (const row of rows) {
  const signs = row.signs;
  for (let i = 0; i < signs.length; i += 1) {
    const prev1 = signs[i - 1] ?? '<START>';
    const next1 = signs[i + 1] ?? '<END>';
    const frameIndex = nearestFrameBefore(signs, i);
    const within002AfterZero =
      frameIndex !== -1 &&
      signs.slice(frameIndex + 1, i).includes('000') &&
      signs[frameIndex] === '002';

    if (signs[i] === '906') {
      sign906Rows.push({
        checked_date: checkedDate,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        sign: '906',
        position: i,
        prev1,
        next1,
        at_end: next1 === '<END>',
        text: row.text,
      });
    }
    if (signs[i] === '388') {
      sign388Rows.push({
        checked_date: checkedDate,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        sign: '388',
        position: i,
        prev1,
        next1,
        at_end: next1 === '<END>',
        text: row.text,
      });
    }
    if (signs[i] === '906' && signs[i + 1] === '388') {
      pairRows.push({
        checked_date: checkedDate,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        position: i,
        prev1,
        next1_after_pair: signs[i + 2] ?? '<END>',
        pair_at_end: signs[i + 2] === undefined,
        nearest_frame_before: frameIndex === -1 ? '' : frameIndex,
        within_002_frame_after_000: within002AfterZero,
        text: row.text,
      });
    }
  }
}

const pairTerminal = pairRows.filter((row) => row.pair_at_end).length;
const sign906FollowedBy388 = sign906Rows.filter((row) => row.next1 === '388').length;
const sign388After906 = sign388Rows.filter((row) => row.prev1 === '906').length;
const uniqueSites = new Set(pairRows.map((row) => row.site)).size;
const uniqueTypes = new Set(pairRows.map((row) => row.type)).size;
const uniquePrevs = new Set(pairRows.map((row) => row.prev1)).size;

const componentRows = [
  {
    checked_date: checkedDate,
    component: '906',
    occurrences: sign906Rows.length,
    terminal: sign906Rows.filter((row) => row.at_end).length,
    followed_by_388: sign906FollowedBy388,
    prev1: tally(sign906Rows.map((row) => row.prev1)),
    next1: tally(sign906Rows.map((row) => row.next1)),
    sites: tally(sign906Rows.map((row) => row.site)),
    types: tally(sign906Rows.map((row) => row.type)),
  },
  {
    checked_date: checkedDate,
    component: '388',
    occurrences: sign388Rows.length,
    terminal: sign388Rows.filter((row) => row.at_end).length,
    preceded_by_906: sign388After906,
    prev1: tally(sign388Rows.map((row) => row.prev1)),
    next1: tally(sign388Rows.map((row) => row.next1)),
    sites: tally(sign388Rows.map((row) => row.site)),
    types: tally(sign388Rows.map((row) => row.type)),
  },
  {
    checked_date: checkedDate,
    component: '906-388',
    occurrences: pairRows.length,
    terminal: pairTerminal,
    preceded_by_906: '',
    followed_by_388: '',
    prev1: tally(pairRows.map((row) => row.prev1)),
    next1: tally(pairRows.map((row) => row.next1_after_pair)),
    sites: tally(pairRows.map((row) => row.site)),
    types: tally(pairRows.map((row) => row.type)),
  },
];

const adjudicationRows = [
  {
    checked_date: checkedDate,
    test: '906388_pair_terminal_boundary',
    result: `${pairTerminal}/${pairRows.length}_terminal_unique_prevs_${uniquePrevs}_sites_${uniqueSites}_types_${uniqueTypes}`,
    effect_on_m451:
      pairRows.length === 3 && pairTerminal === pairRows.length && uniquePrevs === 3
        ? 'softens_tail_as_terminal_suffix_candidate'
        : 'does_not_soften_tail',
    effect_on_x000:
      pairRows.length === 3 && pairTerminal === pairRows.length && uniquePrevs === 3
        ? 'M451_damage_reduced_but_not_removed_because_suffix_is_site_local_and_rare'
        : 'M451_damage_remains_direct_payload_threat',
    decision:
      '906-388 is allowed as weak terminal boundary material, but not enough to restore clean X000 zero-complement.',
  },
  {
    checked_date: checkedDate,
    test: '906_component_lock',
    result: `${sign906FollowedBy388}/${sign906Rows.length}_906_tokens_followed_by_388`,
    effect_on_m451:
      sign906FollowedBy388 === sign906Rows.length
        ? '906_behaves_as_first_half_of_fixed_terminal_pair'
        : '906_has_independent_contexts',
    effect_on_x000:
      sign906FollowedBy388 === sign906Rows.length
        ? 'tail_can_be_treated_as_formulaic_suffix_more_than_payload'
        : 'tail_payload_threat_stronger',
    decision: 'Use 906-388 as a fixed pair in the next parser, not as two independent payload signs.',
  },
  {
    checked_date: checkedDate,
    test: '388_component_lock',
    result: `${sign388After906}/${sign388Rows.length}_388_tokens_preceded_by_906`,
    effect_on_m451: '388_is_not_exclusive_to_906_so_pair_boundary_status_depends_on_the_pair_not_388_alone',
    effect_on_x000: 'does_not_repair_M451_by_itself',
    decision: 'Do not overgeneralize from sign 388; only the exact 906-388 pair gets boundary credit.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: '906388_boundary_control',
  exact_pair_occurrences: pairRows.length,
  exact_pair_terminal: `${pairTerminal}/${pairRows.length}`,
  exact_pair_preceding_signs: tally(pairRows.map((row) => row.prev1)),
  exact_pair_sites: tally(pairRows.map((row) => row.site)),
  exact_pair_types: tally(pairRows.map((row) => row.type)),
  m451_effect:
    '906-388 weakly softens M451 as a terminal suffix candidate, but count/site limits prevent repair',
  x000_status_after_control: 'candidate_with_serious_M451_damage_slightly_softened_not_promoted',
};

writeCsv(path.join(reportsDir, `${prefix}_pair_occurrences.csv`), pairRows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'position',
  'prev1',
  'next1_after_pair',
  'pair_at_end',
  'nearest_frame_before',
  'within_002_frame_after_000',
  'text',
]);
writeCsv(path.join(reportsDir, `${prefix}_component_contexts.csv`), componentRows, [
  'checked_date',
  'component',
  'occurrences',
  'terminal',
  'preceded_by_906',
  'followed_by_388',
  'prev1',
  'next1',
  'sites',
  'types',
]);
writeCsv(path.join(reportsDir, `${prefix}_adjudication.csv`), adjudicationRows, [
  'checked_date',
  'test',
  'result',
  'effect_on_m451',
  'effect_on_x000',
  'decision',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
