import fs from 'node:fs';
import path from 'node:path';

// This script boils the 002-390-X parser down to its most defensible fragment.
// It reads the source-visible parser-controls CSV written earlier in the
// campaign, keeps only rows rated "strict_source_visible_token_box_ready_high"
// (inscriptions we verified on a real image, sharp enough to draw token
// boxes), and sorts each survivor into one of three lane classes: 125 linker,
// 095 terminal classifier, or 692 terminal comparator. The resulting
// "microparser" is tiny but honest: 125 keeps strict support as a continuing
// lane, 095 closure rests on a single witness, and 705 has zero strict
// witnesses, so the old joint 095/705 classifier lane is split. Writes strict
// rows, per-class rollups, and decision CSVs plus a summary JSON to
// data/open_prototype/reports.

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const sourceRowsPath = path.join(
  reportsDir,
  'campaign_032_002_861_002390x_consolidate_source_visible_parser_controls_20260531_source_rows.csv',
);
const prefix = 'campaign_032_002_861_002390x_consolidate_strict_source_visible_microparser_20260531';
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

function laneClass(row) {
  if (row.lane === '125_linker') return 'linker';
  if (row.lane === '095_terminal_classifier') return 'terminal_classifier';
  if (row.lane === '692_global_edge_close') return 'terminal_comparator';
  return 'excluded_or_pressure';
}

fs.mkdirSync(reportsDir, { recursive: true });

const sourceRows = parseCsv(fs.readFileSync(sourceRowsPath, 'utf8'));
const strictRows = sourceRows
  .filter((row) => row.source_status.includes('strict_source_visible_token_box_ready_high'))
  .map((row) => ({
    checked_date: checkedDate,
    object: row.object,
    branch: row.branch,
    lane: row.lane,
    lane_class: laneClass(row),
    site_scope: row.site_scope,
    parser_effect: row.parser_effect,
  }));

const classRows = ['linker', 'terminal_classifier', 'terminal_comparator'].map((laneClassName) => {
  const members = strictRows.filter((row) => row.lane_class === laneClassName);
  return {
    checked_date: checkedDate,
    lane_class: laneClassName,
    strict_rows: members.length,
    objects: members.map((row) => row.object).join(';'),
    branches: members.map((row) => row.branch).join(';'),
    sites: [...new Set(members.map((row) => row.site_scope))].join(';'),
    microparser_effect:
      laneClassName === 'linker'
        ? 'strict support for continuing 125 lane'
        : laneClassName === 'terminal_classifier'
          ? 'singleton strict support for 095 closure'
          : 'strict non-125 terminal comparator, not classifier meaning',
  };
});

const decisionRows = [
  {
    checked_date: checkedDate,
    claim: 'strict_source_visible_microparser',
    status: 'survives_tiny',
    reason:
      'Strict subset preserves a continuing 125 lane and terminal non-125 comparators, but 705 is absent.',
  },
  {
    checked_date: checkedDate,
    claim: '095_705_joint_classifier_lane',
    status: 'split',
    reason: '095 has one strict witness; 705 has zero strict witnesses.',
  },
  {
    checked_date: checkedDate,
    claim: 'source_visible_accepted_translation',
    status: 'blocked',
    reason: 'Strict source visibility still only supports parse role contrast, not values or readings.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: 'strict_source_visible_microparser',
  strict_rows: strictRows.length,
  strict_linker_rows: strictRows.filter((row) => row.lane_class === 'linker').length,
  strict_terminal_non125_rows: strictRows.filter((row) => row.lane_class !== 'linker').length,
  strict_705_rows: strictRows.filter((row) => row.lane === '705_terminal_classifier').length,
  microparser:
    'Strict source-visible subset preserves 125 continuing lane versus non-125 terminal comparator, but not 705.',
};

writeCsv(path.join(reportsDir, `${prefix}_strict_rows.csv`), strictRows, [
  'checked_date',
  'object',
  'branch',
  'lane',
  'lane_class',
  'site_scope',
  'parser_effect',
]);
writeCsv(path.join(reportsDir, `${prefix}_class_rows.csv`), classRows, [
  'checked_date',
  'lane_class',
  'strict_rows',
  'objects',
  'branches',
  'sites',
  'microparser_effect',
]);
writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisionRows, [
  'checked_date',
  'claim',
  'status',
  'reason',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
