import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_consolidate_390_route_split_controls_20260531';
const checkedDate = '2026-05-31';
const terminalClassifiers = new Set(['095', '705', '072', '140', '346', '692', '707']);
const linkers = new Set(['125', '530', '590']);

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

function keepForScope(row, scope) {
  if (scope === 'all') return true;
  if (scope === 'seal_s_only') return row.type === 'SEAL:S';
  if (scope === 'mohenjo_only') return row.site === 'Mohenjo-daro';
  if (scope === 'non_mohenjo') return row.site !== 'Mohenjo-daro';
  if (scope === 'complete_y') return row.complete === 'Y';
  if (scope === 'good_or_fine') return row.condition === 'Good' || row.condition === 'Fine';
  if (scope === 'cisi_named') return row.object && !row.object.startsWith('-:');
  return false;
}

function routeFor(x) {
  if (terminalClassifiers.has(x)) return 'terminal_classifier';
  if (linkers.has(x)) return 'linker';
  return 'other';
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));

const branchRows = [];
for (const row of rows) {
  for (let i = 0; i < row.signs.length - 2; i += 1) {
    if (row.signs[i] !== '002' || row.signs[i + 1] !== '390') continue;
    const x = row.signs[i + 2];
    branchRows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      condition: row.condition,
      complete: row.complete,
      x,
      route: routeFor(x),
      terminal: i + 2 === row.signs.length - 1,
      total_length: row.signs.length,
      text: row.text,
    });
  }
}

const scopes = ['all', 'seal_s_only', 'mohenjo_only', 'non_mohenjo', 'complete_y', 'good_or_fine', 'cisi_named'];
const controlRows = scopes.map((scope) => {
  const scoped = branchRows.filter((row) => keepForScope(row, scope));
  const terminalRows = scoped.filter((row) => row.route === 'terminal_classifier');
  const linkerRows = scoped.filter((row) => row.route === 'linker');
  const terminalRate = terminalRows.length
    ? terminalRows.filter((row) => row.terminal).length / terminalRows.length
    : 0;
  const linkerTerminalRate = linkerRows.length
    ? linkerRows.filter((row) => row.terminal).length / linkerRows.length
    : 0;
  const lengthGap = avg(linkerRows.map((row) => row.total_length)) - avg(terminalRows.map((row) => row.total_length));
  const survives = terminalRows.length >= 2 && linkerRows.length >= 2 && terminalRate === 1 && linkerTerminalRate === 0 && lengthGap > 0;
  return {
    checked_date: checkedDate,
    scope,
    terminal_rows: terminalRows.length,
    terminal_rate: terminalRate.toFixed(3),
    terminal_avg_length: avg(terminalRows.map((row) => row.total_length)).toFixed(3),
    linker_rows: linkerRows.length,
    linker_terminal_rate: linkerTerminalRate.toFixed(3),
    linker_avg_length: avg(linkerRows.map((row) => row.total_length)).toFixed(3),
    length_gap_linker_minus_terminal: lengthGap.toFixed(3),
    verdict:
      terminalRows.length < 2 || linkerRows.length < 2
        ? 'underpowered'
        : survives
          ? 'survives'
          : 'damaged',
  };
});

const serious = controlRows.filter((row) => row.verdict !== 'underpowered');
const survived = serious.filter((row) => row.verdict === 'survives').length;

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: '390_route_split_controls',
  serious_controls: serious.length,
  survived_controls: survived,
  controls: Object.fromEntries(
    controlRows.map((row) => [
      row.scope,
      {
        terminal_rows: Number(row.terminal_rows),
        linker_rows: Number(row.linker_rows),
        length_gap: row.length_gap_linker_minus_terminal,
        verdict: row.verdict,
      },
    ]),
  ),
  provisional_read:
    survived >= Math.max(1, Math.ceil(serious.length / 2))
      ? '390 status/title route split survives basic controls.'
      : '390 route split is damaged by controls.',
};

writeCsv(path.join(reportsDir, `${prefix}_controls.csv`), controlRows, [
  'checked_date',
  'scope',
  'terminal_rows',
  'terminal_rate',
  'terminal_avg_length',
  'linker_rows',
  'linker_terminal_rate',
  'linker_avg_length',
  'length_gap_linker_minus_terminal',
  'verdict',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
