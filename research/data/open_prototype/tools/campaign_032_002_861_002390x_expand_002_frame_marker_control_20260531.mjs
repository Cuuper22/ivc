import fs from 'node:fs';
import path from 'node:path';

// Does sign 002 actually do something when it stands before 390, or is it
// decoration? This control tests the frame-marker idea by comparing what
// follows 390 in two contexts. The script scans every text in
// lipi/metadata_filtered.csv for occurrences of 390, splits them into
// "002-framed" (a 002 immediately precedes the 390) and "unframed", and
// records each successor sign, whether it belongs to the proposed X set
// (095, 705, 125, 530, 590, 692), and whether it ends the text. If 002 really
// licenses the frame, framed 390 should be enriched for that X set relative
// to unframed 390; identical successor ecologies would be the kill condition.
// Writes successor rows, per-context comparison, and the bet definition as
// CSVs plus a summary JSON (with the enrichment delta and a provisional
// verdict) to data/open_prototype/reports.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_002_frame_marker_control_20260531';
const checkedDate = '2026-05-31';
const framedXValues = new Set(['095', '705', '125', '530', '590', '692']);

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

const successorRows = [];
for (const row of rows) {
  for (let i = 0; i < row.signs.length - 1; i += 1) {
    if (row.signs[i] !== '390') continue;
    const successor = row.signs[i + 1];
    const framedBy002 = i > 0 && row.signs[i - 1] === '002';
    successorRows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      context: framedBy002 ? '002_framed_390' : 'unframed_390',
      successor,
      successor_in_framed_x_set: framedXValues.has(successor),
      terminal_successor: i + 1 === row.signs.length - 1,
      next_after_successor: row.signs[i + 2] ?? '<END>',
      prev_before_390: row.signs[i - 1] ?? '<START>',
      text: row.text,
    });
  }
}

const contextRows = ['002_framed_390', 'unframed_390'].map((context) => {
  const members = successorRows.filter((row) => row.context === context);
  const inSet = members.filter((row) => row.successor_in_framed_x_set).length;
  return {
    checked_date: checkedDate,
    context,
    occurrences: members.length,
    successor_in_framed_x_set: inSet,
    in_set_rate: members.length ? (inSet / members.length).toFixed(3) : '0.000',
    terminal_successor_rate: members.length
      ? (members.filter((row) => row.terminal_successor).length / members.length).toFixed(3)
      : '0.000',
    successors: tally(members.map((row) => row.successor)),
    sites: tally(members.map((row) => row.site)),
    types: tally(members.map((row) => row.type)),
    objects: members.map((row) => row.object).slice(0, 20).join(';'),
  };
});

const framed = contextRows.find((row) => row.context === '002_framed_390');
const unframed = contextRows.find((row) => row.context === 'unframed_390');

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_002_FRAME_LICENSES_390',
    tier: 'candidate',
    claim:
      '002 licenses 390 as a status/title frame; unframed 390 has a different successor ecology.',
    risky_prediction:
      '002-framed 390 should be enriched for the X-set 095/705/125/530/590/692 compared with unframed 390.',
    kill_condition:
      'Unframed 390 has the same successor distribution and route behavior as 002-framed 390.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: '002_frame_marker_control',
  framed_390: framed,
  unframed_390: unframed,
  enrichment:
    framed && unframed
      ? (Number(framed.in_set_rate) - Number(unframed.in_set_rate)).toFixed(3)
      : '',
  provisional_read:
    framed && unframed && Number(framed.in_set_rate) > Number(unframed.in_set_rate)
      ? '002-framed 390 is enriched for the proposed X-set; 002 frame marker survives first control.'
      : '002 frame marker not supported by successor enrichment.',
};

writeCsv(path.join(reportsDir, `${prefix}_successor_rows.csv`), successorRows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'context',
  'successor',
  'successor_in_framed_x_set',
  'terminal_successor',
  'next_after_successor',
  'prev_before_390',
  'text',
]);
writeCsv(path.join(reportsDir, `${prefix}_context_rows.csv`), contextRows, [
  'checked_date',
  'context',
  'occurrences',
  'successor_in_framed_x_set',
  'in_set_rate',
  'terminal_successor_rate',
  'successors',
  'sites',
  'types',
  'objects',
]);
writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), betRows, [
  'checked_date',
  'bet_id',
  'tier',
  'claim',
  'risky_prediction',
  'kill_condition',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
