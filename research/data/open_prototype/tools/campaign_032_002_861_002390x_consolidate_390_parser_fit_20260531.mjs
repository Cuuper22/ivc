import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_consolidate_390_parser_fit_20260531';

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

function signs(text) {
  return text.match(/\d{3}/g) ?? [];
}

function parserRule(x) {
  if (x === '125') {
    return {
      predicted: 'open',
      rule_class: 'core_open_dependent_tail_operator',
      tier: 'candidate',
      parse: '390 selects X=125; X=125 licenses dependent tail',
    };
  }
  if (x === '095' || x === '705') {
    return {
      predicted: 'terminal',
      rule_class: 'core_terminal_class_label',
      tier: 'candidate',
      parse: `390 selects terminal class-label X=${x}`,
    };
  }
  if (x === '530') {
    return {
      predicted: 'open',
      rule_class: 'open_operator_from_broader_x_slot',
      tier: 'candidate',
      parse: '390 selects open X=530; tail is licensed but not 390-specific',
    };
  }
  if (x === '590') {
    return {
      predicted: 'open',
      rule_class: 'open_extender_wild_shot',
      tier: 'wild shot',
      parse: '390 selects possible open extender X=590; singleton under 390',
    };
  }
  if (x === '692') {
    return {
      predicted: 'terminal',
      rule_class: 'raw_boundary_closer',
      tier: 'wild shot',
      parse: 'X=692 closes, but likely because 692 is raw-terminal-heavy',
    };
  }
  return {
    predicted: 'terminal',
    rule_class: 'singleton_terminal_payload',
    tier: 'wild shot',
    parse: `X=${x} is singleton terminal under 390; do not promote without repeats`,
  };
}

fs.mkdirSync(reportsDir, { recursive: true });

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));
const parseRows = [];
for (const row of metadataRows) {
  const rowSigns = signs(row.text);
  for (let index = 0; index < rowSigns.length - 2; index += 1) {
    if (rowSigns[index] !== '002' || rowSigns[index + 1] !== '390') continue;
    const x = rowSigns[index + 2];
    const actual = index + 2 < rowSigns.length - 1 ? 'open' : 'terminal';
    const rule = parserRule(x);
    parseRows.push({
      checked_date: '2026-05-31',
      object: row.cisi,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      scope_cell: `${row.site}|${row.type}|${row.shape}|${row.material}`,
      prev_before_002: rowSigns[index - 1] ?? '',
      frame: '002-390-X',
      x,
      tail_after_x: rowSigns.slice(index + 3).join(' ') || '<END>',
      actual,
      predicted: rule.predicted,
      correct: rule.predicted === actual ? 'True' : 'False',
      rule_class: rule.rule_class,
      tier: rule.tier,
      parse: rule.parse,
      text: row.text,
    });
  }
}

const correctRows = parseRows.filter((row) => row.correct === 'True');
const coreRows = parseRows.filter((row) => row.tier === 'candidate');
const weakRows = parseRows.filter((row) => row.tier !== 'candidate');

const decisions = [
  {
    checked_date: '2026-05-31',
    decision: 'core_parser_covers_repeated_classes',
    rows: String(coreRows.length),
    support: coreRows.map((row) => `${row.object}:${row.x}->${row.actual}`).join('; '),
  },
  {
    checked_date: '2026-05-31',
    decision: 'weak_rows_are_singleton_or_raw_prior',
    rows: String(weakRows.length),
    support: weakRows.map((row) => `${row.object}:${row.x}:${row.rule_class}`).join('; '),
  },
  {
    checked_date: '2026-05-31',
    decision: 'fit_is_not_validation',
    rows: String(parseRows.length),
    support: 'Rules were derived from this small set; next phase must break them with new/source-bound rows.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'CONSOLIDATE',
  status: 'consolidate_390_parser_fit',
  rows: parseRows.length,
  current_fit: `${correctRows.length}/${parseRows.length}`,
  core_candidate_rows: coreRows.length,
  weak_or_wild_rows: weakRows.length,
  decisions,
};

writeCsv(path.join(reportsDir, `${prefix}_parse_rows.csv`), parseRows, [
  'checked_date',
  'object',
  'site',
  'type',
  'shape',
  'material',
  'scope_cell',
  'prev_before_002',
  'frame',
  'x',
  'tail_after_x',
  'actual',
  'predicted',
  'correct',
  'rule_class',
  'tier',
  'parse',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  'checked_date',
  'decision',
  'rows',
  'support',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
