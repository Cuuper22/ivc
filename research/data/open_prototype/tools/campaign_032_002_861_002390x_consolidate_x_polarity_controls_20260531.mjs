import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_consolidate_x_polarity_controls_20260531';
const checkedDate = '2026-05-31';

const terminalBoosters = new Set([
  '000',
  '031',
  '416',
  '575',
  '317',
  '705',
  '741',
  '491',
  '095',
  '260',
  '820',
  '140',
  '165',
  '603',
]);
const openOperators = new Set(['125', '455', '530', '003', '861', '065', '035', '906', '460', '090']);
const globalEdges = new Set(['501', '091', '692']);

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

function polarity(x) {
  if (terminalBoosters.has(x)) return 'terminal_booster';
  if (openOperators.has(x)) return 'open_operator';
  if (globalEdges.has(x)) return 'global_edge';
  return 'other';
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

function keepForScope(row, scope) {
  if (scope === 'all') return true;
  if (scope === 'seal_s_only') return row.type === 'SEAL:S';
  if (scope === 'mohenjo_only') return row.site === 'Mohenjo-daro';
  if (scope === 'non_mohenjo') return row.site !== 'Mohenjo-daro';
  if (scope === 'harappa_only') return row.site === 'Harappa';
  if (scope === 'complete_y') return row.complete === 'Y';
  if (scope === 'good_or_fine') return row.condition === 'Good' || row.condition === 'Fine';
  if (scope === 'cisi_named') return row.object && !row.object.startsWith('-:');
  return false;
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));

const xRows = [];
for (const row of rows) {
  for (let i = 0; i < row.signs.length - 2; i += 1) {
    if (row.signs[i] !== '002') continue;
    const x = row.signs[i + 2];
    const xPolarity = polarity(x);
    if (xPolarity === 'other') continue;
    xRows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      condition: row.condition,
      complete: row.complete,
      head: row.signs[i + 1],
      x,
      polarity: xPolarity,
      terminal: i + 2 === row.signs.length - 1,
      next1: row.signs[i + 3] ?? '<END>',
      text: row.text,
    });
  }
}

const scopes = ['all', 'seal_s_only', 'mohenjo_only', 'non_mohenjo', 'harappa_only', 'complete_y', 'good_or_fine', 'cisi_named'];

const controlRows = scopes.map((scope) => {
  const scoped = xRows.filter((row) => keepForScope(row, scope));
  const terminalRows = scoped.filter((row) => row.polarity === 'terminal_booster');
  const openRows = scoped.filter((row) => row.polarity === 'open_operator');
  const edgeRows = scoped.filter((row) => row.polarity === 'global_edge');
  const terminalRate = rate(terminalRows.filter((row) => row.terminal).length, terminalRows.length);
  const openRate = rate(openRows.filter((row) => row.terminal).length, openRows.length);
  const gap = terminalRate - openRate;
  return {
    checked_date: checkedDate,
    scope,
    terminal_booster_rows: terminalRows.length,
    terminal_booster_terminal_rate: terminalRate.toFixed(3),
    open_operator_rows: openRows.length,
    open_operator_terminal_rate: openRate.toFixed(3),
    terminal_minus_open_gap: gap.toFixed(3),
    global_edge_rows: edgeRows.length,
    global_edge_terminal_rate: rate(edgeRows.filter((row) => row.terminal).length, edgeRows.length).toFixed(3),
    terminal_signs: tally(terminalRows.map((row) => row.x)),
    open_signs: tally(openRows.map((row) => row.x)),
    sites: tally(scoped.map((row) => row.site)),
    verdict:
      terminalRows.length < 5 || openRows.length < 5
        ? 'underpowered'
        : gap >= 0.35
          ? 'survives'
          : gap >= 0.2
            ? 'weak_survival'
            : 'damaged',
  };
});

const byHeadRows = [...new Set(xRows.map((row) => row.head))]
  .map((head) => {
    const members = xRows.filter((row) => row.head === head);
    const terminalRows = members.filter((row) => row.polarity === 'terminal_booster');
    const openRows = members.filter((row) => row.polarity === 'open_operator');
    const gap =
      rate(terminalRows.filter((row) => row.terminal).length, terminalRows.length) -
      rate(openRows.filter((row) => row.terminal).length, openRows.length);
    return {
      checked_date: checkedDate,
      head,
      rows: members.length,
      terminal_booster_rows: terminalRows.length,
      open_operator_rows: openRows.length,
      gap: gap.toFixed(3),
      terminal_signs: tally(terminalRows.map((row) => row.x)),
      open_signs: tally(openRows.map((row) => row.x)),
      verdict:
        terminalRows.length >= 2 && openRows.length >= 2 && gap >= 0.35
          ? 'head_level_support'
          : terminalRows.length >= 2 && openRows.length >= 2
            ? 'head_level_weak_or_damaged'
            : 'not_comparable',
    };
  })
  .filter((row) => Number(row.rows) >= 5)
  .sort((a, b) => Number(b.rows) - Number(a.rows) || a.head.localeCompare(b.head));

const serious = controlRows.filter((row) => row.verdict !== 'underpowered');
const survived = serious.filter((row) => row.verdict === 'survives').length;
const weak = serious.filter((row) => row.verdict === 'weak_survival').length;

const decisionRows = [
  {
    checked_date: checkedDate,
    claim: 'X_polarity_slot',
    decision: survived + weak >= Math.ceil(serious.length / 2) ? 'candidate_keep' : 'demote',
    reason:
      'Terminal boosters and open operators preserve different terminality profiles across most broad controls.',
  },
  {
    checked_date: checkedDate,
    claim: 'X_polarity_is_universal',
    decision: 'blocked',
    reason:
      'Some scopes are underpowered and head-level support is uneven; carry as constructional tendency, not universal grammar.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: 'x_polarity_controls',
  serious_controls: serious.length,
  survived_controls: survived,
  weak_survivals: weak,
  controls: Object.fromEntries(
    controlRows.map((row) => [
      row.scope,
      {
        terminal_booster_rows: Number(row.terminal_booster_rows),
        open_operator_rows: Number(row.open_operator_rows),
        gap: row.terminal_minus_open_gap,
        verdict: row.verdict,
      },
    ]),
  ),
  decision: survived + weak >= Math.ceil(serious.length / 2) ? 'X_polarity_candidate_keep' : 'X_polarity_demote',
};

writeCsv(path.join(reportsDir, `${prefix}_controls.csv`), controlRows, [
  'checked_date',
  'scope',
  'terminal_booster_rows',
  'terminal_booster_terminal_rate',
  'open_operator_rows',
  'open_operator_terminal_rate',
  'terminal_minus_open_gap',
  'global_edge_rows',
  'global_edge_terminal_rate',
  'terminal_signs',
  'open_signs',
  'sites',
  'verdict',
]);
writeCsv(path.join(reportsDir, `${prefix}_head_controls.csv`), byHeadRows, [
  'checked_date',
  'head',
  'rows',
  'terminal_booster_rows',
  'open_operator_rows',
  'gap',
  'terminal_signs',
  'open_signs',
  'verdict',
]);
writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisionRows, [
  'checked_date',
  'claim',
  'decision',
  'reason',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
