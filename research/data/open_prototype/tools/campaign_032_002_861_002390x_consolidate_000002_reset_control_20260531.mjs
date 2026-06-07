import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_consolidate_000002_reset_control_20260531';
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

function previousFrameIndex(signs, index) {
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

for (const row of rows) {
  const signs = row.signs;
  for (let i = 0; i < signs.length - 1; i += 1) {
    if (signs[i] !== '000' || signs[i + 1] !== '002') continue;
    const prevFrame = previousFrameIndex(signs, i);
    const nextAfterPair = signs[i + 2] ?? '<END>';
    const finalPair = nextAfterPair === '<END>';
    const preceding = signs[i - 1] ?? '<START>';
    pairRows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      material: row.material,
      condition: row.condition,
      complete: row.complete,
      position: i,
      preceding,
      next_after_pair: nextAfterPair,
      final_pair: finalPair,
      previous_002_before_pair: prevFrame !== -1,
      previous_002_index: prevFrame === -1 ? '' : prevFrame,
      reset_candidate:
        prevFrame !== -1 && (nextAfterPair !== '<END>' || row.object === 'Ns-66'),
      text: row.text,
    });
  }
}

const finalRows = pairRows.filter((row) => row.final_pair);
const resetCandidateRows = pairRows.filter((row) => row.reset_candidate);
const finalAfterPreviousFrameRows = finalRows.filter((row) => row.previous_002_before_pair === true);
const ns66Rows = pairRows.filter((row) => row.object === 'Ns-66');

const summaryRows = [
  {
    checked_date: checkedDate,
    slice: 'all_000_002',
    occurrences: pairRows.length,
    final_pair: finalRows.length,
    previous_frame_before_pair: pairRows.filter((row) => row.previous_002_before_pair === true).length,
    sites: tally(pairRows.map((row) => row.site)),
    types: tally(pairRows.map((row) => row.type)),
    preceding: tally(pairRows.map((row) => row.preceding)),
    next_after_pair: tally(pairRows.map((row) => row.next_after_pair)),
  },
  {
    checked_date: checkedDate,
    slice: 'final_000_002',
    occurrences: finalRows.length,
    final_pair: finalRows.length,
    previous_frame_before_pair: finalAfterPreviousFrameRows.length,
    sites: tally(finalRows.map((row) => row.site)),
    types: tally(finalRows.map((row) => row.type)),
    preceding: tally(finalRows.map((row) => row.preceding)),
    next_after_pair: tally(finalRows.map((row) => row.next_after_pair)),
  },
  {
    checked_date: checkedDate,
    slice: 'reset_candidate_000_002',
    occurrences: resetCandidateRows.length,
    final_pair: resetCandidateRows.filter((row) => row.final_pair).length,
    previous_frame_before_pair: resetCandidateRows.filter((row) => row.previous_002_before_pair === true).length,
    sites: tally(resetCandidateRows.map((row) => row.site)),
    types: tally(resetCandidateRows.map((row) => row.type)),
    preceding: tally(resetCandidateRows.map((row) => row.preceding)),
    next_after_pair: tally(resetCandidateRows.map((row) => row.next_after_pair)),
  },
  {
    checked_date: checkedDate,
    slice: 'ns66_000_002',
    occurrences: ns66Rows.length,
    final_pair: ns66Rows.filter((row) => row.final_pair).length,
    previous_frame_before_pair: ns66Rows.filter((row) => row.previous_002_before_pair === true).length,
    sites: tally(ns66Rows.map((row) => row.site)),
    types: tally(ns66Rows.map((row) => row.type)),
    preceding: tally(ns66Rows.map((row) => row.preceding)),
    next_after_pair: tally(ns66Rows.map((row) => row.next_after_pair)),
  },
];

const adjudicationRows = [
  {
    checked_date: checkedDate,
    test: 'final_000_002_reset_specificity',
    result: `${finalRows.length}/${pairRows.length}_000_002_pairs_are_final; ${finalAfterPreviousFrameRows.length}_final_pairs_have_previous_002`,
    effect_on_ns66:
      finalAfterPreviousFrameRows.length > 1
        ? 'final_reset_shape_has_parallels'
        : 'ns66_final_reset_shape_is_near_singleton',
    effect_on_x000:
      finalAfterPreviousFrameRows.length > 1
        ? 'slightly_softens_ns66_as_reset_exception'
        : 'ns66_does_not_repair_x000',
    decision:
      'Broad 000-002 ecology is real, but final 000-002 after an earlier frame is too thin to rescue Ns-66.',
  },
  {
    checked_date: checkedDate,
    test: 'nonfinal_000_002_frame_restart',
    result: `${pairRows.length - finalRows.length}_nonfinal_pairs; next_after_pair=${tally(
      pairRows.filter((row) => !row.final_pair).map((row) => row.next_after_pair),
    )}`,
    effect_on_ns66: 'supports_general_reset_ecology_but_not_the_terminal_ns66_shape',
    effect_on_x000: 'keep_ns66_as_weak_exception_not_support',
    decision:
      'Use nonfinal 000-002 as evidence for frame restart ecology only when a following head is present.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: '000002_reset_control',
  all_000_002_occurrences: pairRows.length,
  final_000_002_occurrences: finalRows.length,
  final_after_previous_frame: finalAfterPreviousFrameRows.length,
  ns66_pairs: ns66Rows.length,
  ns66_final_pairs: ns66Rows.filter((row) => row.final_pair).length,
  ns66_effect: 'broad_reset_ecology_real_but_terminal_Ns66_shape_too_thin_to_repair_x000',
  x000_status_after_control: 'candidate_with_M451_damage_Ns66_no_longer_major_repair_route',
};

writeCsv(path.join(reportsDir, `${prefix}_occurrences.csv`), pairRows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'material',
  'condition',
  'complete',
  'position',
  'preceding',
  'next_after_pair',
  'final_pair',
  'previous_002_before_pair',
  'previous_002_index',
  'reset_candidate',
  'text',
]);
writeCsv(path.join(reportsDir, `${prefix}_summary_slices.csv`), summaryRows, [
  'checked_date',
  'slice',
  'occurrences',
  'final_pair',
  'previous_frame_before_pair',
  'sites',
  'types',
  'preceding',
  'next_after_pair',
]);
writeCsv(path.join(reportsDir, `${prefix}_adjudication.csv`), adjudicationRows, [
  'checked_date',
  'test',
  'result',
  'effect_on_ns66',
  'effect_on_x000',
  'decision',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
