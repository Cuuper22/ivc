import fs from 'node:fs';
import path from 'node:path';

// A negative control for the 390 status-head bet: if the classifier-versus-
// linker route split shows up after every frequent head, it says nothing
// special about 390. This script scans lipi/metadata_filtered.csv for every
// 002-HEAD-X occurrence, routes X into terminal classifiers or linkers using
// the campaign's sign lists, and computes for each head (5+ occurrences) a
// route-separation score: the classifier terminal rate minus the linker
// terminal rate, plus a small bonus when linker texts run longer than
// classifier texts, requiring at least 3 rows on each side. A non-390 head
// scoring 1.0 or higher is a "dangerous_negative_control" — evidence the
// split is generic. The summary reports 390's own score and whether any
// dangerous controls exist. Writes the head-control table and the bet as
// CSVs plus a summary JSON to data/open_prototype/reports.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_390_negative_head_controls_20260531';
const checkedDate = '2026-05-31';

const terminalClassifiers = new Set(['095', '705', '000', '031', '416', '575', '317', '741', '491', '260', '820', '140', '165', '603']);
const linkers = new Set(['125', '455', '530', '003', '861', '065', '035', '906', '460', '090']);

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

function avg(values) {
  if (!values.length) return 0;
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function rate(count, total) {
  return total ? count / total : 0;
}

function tally(values) {
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([value, count]) => `${value}:${count}`)
    .join(';');
}

function routeFor(x) {
  if (terminalClassifiers.has(x)) return 'terminal_classifier';
  if (linkers.has(x)) return 'linker_complement';
  return 'other';
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));

const occurrences = [];
for (const row of rows) {
  for (let i = 0; i < row.signs.length - 2; i += 1) {
    if (row.signs[i] !== '002') continue;
    const head = row.signs[i + 1];
    const x = row.signs[i + 2];
    occurrences.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      head,
      x,
      route: routeFor(x),
      terminal: i + 2 === row.signs.length - 1,
      total_length: row.signs.length,
      text: row.text,
    });
  }
}

const byHead = new Map();
for (const row of occurrences) {
  const stat = byHead.get(row.head) ?? { head: row.head, rows: [] };
  stat.rows.push(row);
  byHead.set(row.head, stat);
}

const headControlRows = [...byHead.values()]
  .map((stat) => {
    const terminalRows = stat.rows.filter((row) => row.route === 'terminal_classifier');
    const linkerRows = stat.rows.filter((row) => row.route === 'linker_complement');
    const terminalRate = rate(terminalRows.filter((row) => row.terminal).length, terminalRows.length);
    const linkerTerminalRate = rate(linkerRows.filter((row) => row.terminal).length, linkerRows.length);
    const terminalAvgLen = avg(terminalRows.map((row) => row.total_length));
    const linkerAvgLen = avg(linkerRows.map((row) => row.total_length));
    const separationScore =
      terminalRows.length >= 3 && linkerRows.length >= 3
        ? terminalRate - linkerTerminalRate + Math.max(0, linkerAvgLen - terminalAvgLen) / 10
        : 0;
    return {
      checked_date: checkedDate,
      head: stat.head,
      occurrences: stat.rows.length,
      terminal_classifier_count: terminalRows.length,
      terminal_classifier_terminal_rate: terminalRate.toFixed(3),
      terminal_classifier_avg_length: terminalAvgLen.toFixed(3),
      linker_count: linkerRows.length,
      linker_terminal_rate: linkerTerminalRate.toFixed(3),
      linker_avg_length: linkerAvgLen.toFixed(3),
      route_separation_score: separationScore.toFixed(3),
      x_values: tally(stat.rows.map((row) => row.x)),
      sites: tally(stat.rows.map((row) => row.site)),
      types: tally(stat.rows.map((row) => row.type)),
      status_head_control_result:
        stat.head === '390'
          ? 'target'
          : separationScore >= 1
            ? 'dangerous_negative_control'
            : terminalRows.length >= 3 && linkerRows.length >= 3
              ? 'partial_negative_control'
              : 'not_comparable',
    };
  })
  .filter((row) => Number(row.occurrences) >= 5)
  .sort(
    (a, b) =>
      Number(b.route_separation_score) - Number(a.route_separation_score) ||
      Number(b.occurrences) - Number(a.occurrences) ||
      a.head.localeCompare(b.head),
  );

const dangerousControls = headControlRows.filter((row) => row.status_head_control_result === 'dangerous_negative_control');
const head390 = headControlRows.find((row) => row.head === '390');

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_390_STATUS_NEGATIVE_CONTROL',
    tier: 'candidate if no dangerous controls',
    claim:
      'The 390 route split is not a generic property of all frequent 002 heads.',
    risky_prediction:
      'Few or no non-390 heads should match 390 with both classifier closure and linker-complement length separation.',
    kill_condition:
      'Several unrelated heads show the same split with equal or better separation scores.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: '390_negative_head_controls',
  head390_route_separation_score: head390?.route_separation_score ?? '',
  dangerous_negative_controls: dangerousControls.map((row) => row.head),
  top_controls: headControlRows.slice(0, 8).map((row) => ({
    head: row.head,
    score: row.route_separation_score,
    occurrences: row.occurrences,
    result: row.status_head_control_result,
  })),
  provisional_read:
    dangerousControls.length === 0
      ? '390 route split is not obviously generic among frequent heads.'
      : '390 status/title bet is threatened by comparable non-390 heads.',
};

writeCsv(path.join(reportsDir, `${prefix}_head_controls.csv`), headControlRows, [
  'checked_date',
  'head',
  'occurrences',
  'terminal_classifier_count',
  'terminal_classifier_terminal_rate',
  'terminal_classifier_avg_length',
  'linker_count',
  'linker_terminal_rate',
  'linker_avg_length',
  'route_separation_score',
  'x_values',
  'sites',
  'types',
  'status_head_control_result',
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
