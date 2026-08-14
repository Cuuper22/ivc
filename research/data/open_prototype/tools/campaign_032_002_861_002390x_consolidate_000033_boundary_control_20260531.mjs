// Control study for row 4148.1, the potential kill switch against reading sign
// 000 as a boundary marker (the X=000 hypothesis). That row contains
// 267-000-033: if 033 there is meaningful payload governed by 000, then 000 is
// not a clean boundary. This script scans the local Lipi metadata for every
// 000-033 pair and every bare 033, recording neighbors and whether each sits at
// the end of its inscription. If most 000-033 pairs are terminal, 033 looks
// like boundary furniture and the 4148 damage softens. Writes pair occurrences,
// a context summary, an adjudication CSV, and a summary JSON to
// data/open_prototype/reports/. The recorded verdict: 000-033 does show
// boundary pressure, but the exact 267-000-033 frame is a singleton with no
// source image, so 4148 stays a source-bound kill switch — not yet fired.

import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_consolidate_000033_boundary_control_20260531';
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
  return text.match(/\d{3}/g) ?? [];
}

function tally(values) {
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([value, count]) => `${value}:${count}`)
    .join(';');
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));

const pairRows = [];
const sign033Rows = [];

for (const row of rows) {
  const signs = row.signs;
  for (let i = 0; i < signs.length; i += 1) {
    if (signs[i] === '033') {
      sign033Rows.push({
        checked_date: checkedDate,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        position: i,
        prev1: signs[i - 1] ?? '<START>',
        next1: signs[i + 1] ?? '<END>',
        at_end: signs[i + 1] === undefined,
        text: row.text,
      });
    }
    if (signs[i] === '000' && signs[i + 1] === '033') {
      pairRows.push({
        checked_date: checkedDate,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        condition: row.condition,
        complete: row.complete,
        position: i,
        prev1: signs[i - 1] ?? '<START>',
        next_after_pair: signs[i + 2] ?? '<END>',
        pair_at_end: signs[i + 2] === undefined,
        is_4148_1: row.id === '4148.1',
        text: row.text,
      });
    }
  }
}

const pairTerminal = pairRows.filter((row) => row.pair_at_end).length;
const target4148 = pairRows.find((row) => row.is_4148_1);

const contextRows = [
  {
    checked_date: checkedDate,
    slice: '000-033_pair',
    occurrences: pairRows.length,
    terminal: pairTerminal,
    terminal_rate: pairRows.length ? (pairTerminal / pairRows.length).toFixed(3) : '0.000',
    sites: tally(pairRows.map((row) => row.site)),
    types: tally(pairRows.map((row) => row.type)),
    prev1: tally(pairRows.map((row) => row.prev1)),
    next_after_pair: tally(pairRows.map((row) => row.next_after_pair)),
  },
  {
    checked_date: checkedDate,
    slice: '033_sign',
    occurrences: sign033Rows.length,
    terminal: sign033Rows.filter((row) => row.at_end).length,
    terminal_rate: sign033Rows.length
      ? (sign033Rows.filter((row) => row.at_end).length / sign033Rows.length).toFixed(3)
      : '0.000',
    sites: tally(sign033Rows.map((row) => row.site)),
    types: tally(sign033Rows.map((row) => row.type)),
    prev1: tally(sign033Rows.map((row) => row.prev1)),
    next_after_pair: tally(sign033Rows.map((row) => row.next1)),
  },
];

const adjudicationRows = [
  {
    checked_date: checkedDate,
    test: '000033_boundary_pressure',
    result: `${pairTerminal}/${pairRows.length}_000033_pairs_terminal`,
    effect_on_4148:
      pairTerminal / pairRows.length >= 0.6
        ? 'softens_033_as_boundary_candidate'
        : '033_remains_payload_threat',
    effect_on_x000:
      pairTerminal / pairRows.length >= 0.6
        ? '4148_damage_softened_but_not_removed_because_267_000_033_is_singleton'
        : '4148_remains_clean_payload_kill_switch_if_source_bound',
    decision:
      '000-033 has boundary pressure, but the exact 267-000-033 frame is singleton and source-unbound.',
  },
  {
    checked_date: checkedDate,
    test: '4148_specific_context',
    result: target4148
      ? `prev=${target4148.prev1}; next_after_pair=${target4148.next_after_pair}; pair_at_end=${target4148.pair_at_end}`
      : '4148_not_found_in_000033_pair_rows',
    effect_on_4148: target4148?.pair_at_end
      ? 'local_pair_is_terminal_which_softens_payload_reading'
      : 'local_pair_is_not_terminal_or_missing',
    effect_on_x000:
      'source still decides whether terminal 033 is a boundary sign or meaningful governed payload',
    decision: 'Do not kill X=000 from 4148 until a source image proves continuous governed payload.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: '000033_boundary_control',
  pair_occurrences: pairRows.length,
  pair_terminal: `${pairTerminal}/${pairRows.length}`,
  pair_sites: tally(pairRows.map((row) => row.site)),
  pair_types: tally(pairRows.map((row) => row.type)),
  target_4148_pair_terminal: target4148?.pair_at_end ?? false,
  x000_status_after_control:
    '4148_softened_by_000033_boundary_pressure_but_remains_source_bound_kill_switch',
};

writeCsv(path.join(reportsDir, `${prefix}_pair_occurrences.csv`), pairRows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'condition',
  'complete',
  'position',
  'prev1',
  'next_after_pair',
  'pair_at_end',
  'is_4148_1',
  'text',
]);
writeCsv(path.join(reportsDir, `${prefix}_context_summary.csv`), contextRows, [
  'checked_date',
  'slice',
  'occurrences',
  'terminal',
  'terminal_rate',
  'sites',
  'types',
  'prev1',
  'next_after_pair',
]);
writeCsv(path.join(reportsDir, `${prefix}_adjudication.csv`), adjudicationRows, [
  'checked_date',
  'test',
  'result',
  'effect_on_4148',
  'effect_on_x000',
  'decision',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
