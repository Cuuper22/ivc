import fs from 'node:fs';
import path from 'node:path';

// This script turns the head-class transfer results into readable parser
// output, so we can see what the current model would actually claim for real
// inscriptions. It reads the two CSVs written by the head-class transfer-bets
// run (per-head metrics and per-frame rows), picks the frames worth showing —
// head 220, head 390 with X in 125/095/692/705, and the terminal-default and
// closed-edge heads 031, 861, 920, 405, 056 — and emits for each a structural
// parse string like "FRAME(002) + head gloss + X gloss + TAIL(...)", a
// provisional semantic gloss, a confidence tier, and a testable prediction
// (should close, or should keep its tail). The summary carries an explicit
// warning: these are structural glosses, not translations. Writes parse rows
// and three lane-level bets as CSVs plus a summary JSON to
// data/open_prototype/reports.

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const checkedDate = '2026-05-31';
const inputPrefix = 'campaign_032_002_861_002390x_expand_head_class_transfer_bets_20260531';
const prefix = 'campaign_032_002_861_002390x_expand_head_class_parser_outputs_20260531';

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
  for (const row of rows) lines.push(fields.map((fieldName) => csvEscape(row[fieldName])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function headGloss(head, headClass) {
  if (head === '390') return 'MIXED_INVENTORY_HEAD, status/title semantics only wild';
  if (head === '220') return 'OPEN_RELATION_ROUTE_HEAD wild shot';
  if (['031', '861', '920'].includes(head)) return 'TERMINAL_DEFAULT_CLASSIFIER_ZONE wild shot';
  if (['405', '056'].includes(head)) return 'CLOSED_EDGE_TEMPLATE_HEAD wild shot';
  if (['000', '368'].includes(head)) return 'MIXED_HEAD_COMPARATOR wild shot';
  if (head === '820') return 'UNRESOLVED_TERMINAL_LEANING_HEAD';
  return headClass;
}

function xGloss(row) {
  if (row.x_polarity === 'terminal_booster') return `TERMINAL_BOOSTER(${row.x})`;
  if (row.x_polarity === 'open_operator') return `OPEN_OPERATOR(${row.x})`;
  if (row.x_polarity === 'global_edge') return `EDGE_CAP(${row.x})`;
  return `UNCLASSIFIED_X(${row.x})`;
}

function isTerminal(row) {
  return row.terminal === 'true' || row.terminal === true;
}

function confidence(row) {
  if (row.head === '220' && row.x_polarity === 'open_operator' && !isTerminal(row)) return 'wild shot with strong structural pressure';
  if (row.head === '390' && ['125', '095', '692'].includes(row.x)) return 'candidate structure from prior strict rows';
  if (['405', '056', '920'].includes(row.head) && isTerminal(row)) return 'wild shot closed-template pressure';
  if (['031', '861'].includes(row.head) && row.x_polarity === 'terminal_booster') return 'wild shot terminal-default pressure';
  return 'wild shot';
}

fs.mkdirSync(reportsDir, { recursive: true });

const metricRows = parseCsv(
  fs.readFileSync(path.join(reportsDir, `${inputPrefix}_head_transfer_metrics.csv`), 'utf8'),
);
const frameRows = parseCsv(fs.readFileSync(path.join(reportsDir, `${inputPrefix}_frame_rows.csv`), 'utf8'));
const classByHead = new Map(metricRows.map((row) => [row.head, row.expanded_head_bet_class]));

const selectedRows = frameRows.filter(
  (row) =>
    row.head === '220' ||
    (row.head === '390' && ['125', '095', '692', '705'].includes(row.x)) ||
    (['031', '861', '920', '405', '056'].includes(row.head) && row.x_polarity !== 'other'),
);

const parseRows = selectedRows.map((row) => {
  const headClass = classByHead.get(row.head) ?? 'unclassified_head';
  const tail = row.tail === '<END>' ? 'NO_TAIL' : `TAIL(${row.tail})`;
  return {
    checked_date: checkedDate,
    object: row.object,
    site: row.site,
    head: row.head,
    x: row.x,
    head_class: headClass,
    structural_parse: `FRAME(002) + ${headGloss(row.head, headClass)} + ${xGloss(row)} + ${tail}`,
    provisional_semantic_gloss:
      row.head === '220'
        ? 'designation frame with relation/route payload'
        : row.head === '390'
          ? 'designation frame with mixed inventory X'
          : ['031', '861', '920'].includes(row.head)
            ? 'designation frame with terminal classifier/default cap'
            : ['405', '056'].includes(row.head)
              ? 'fixed edge/template formula'
              : 'head-class comparator',
    tier: confidence(row),
    prediction: isTerminal(row) ? 'should close unless source shows hidden tail' : 'should preserve tail under source-strict reading',
    text: row.text,
  };
});

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_PARSER_OUTPUT_220_RELATION_LANE',
    tier: 'wild shot with structural pressure',
    risky_bet: '`002-220-455/065-tail` rows parse as relation/route payloads.',
    prediction: 'The tail after 455/065 is part of the parse, not damaged residue.',
    kill_condition: 'Source-strict rows show 455/065 are visual fillers or tails are copied context artifacts.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_PARSER_OUTPUT_TERMINAL_DEFAULT_LANE',
    tier: 'wild shot',
    risky_bet: '`031/861/920` heads parse as terminal classifier/default zones.',
    prediction: 'Terminal booster X signs after these heads should close in held-out rows.',
    kill_condition: 'Open operators after these heads become productive and source-strict.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_PARSER_OUTPUT_CLOSED_EDGE_LANE',
    tier: 'wild shot',
    risky_bet: '`405/056` heads parse as fixed edge/template formulae.',
    prediction: '`405-501` and `056-091` should behave like closed templates, not lexical phrases.',
    kill_condition: 'Strict productive continuations appear after 405/056.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'head_class_parser_outputs',
  parse_rows: parseRows.length,
  new_bets: betRows.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
  strongest_new_parse: '002-220 open relation/route lane',
  warning: 'These are structural glosses, not translations or readings.',
};

writeCsv(path.join(reportsDir, `${prefix}_parse_rows.csv`), parseRows, [
  'checked_date',
  'object',
  'site',
  'head',
  'x',
  'head_class',
  'structural_parse',
  'provisional_semantic_gloss',
  'tier',
  'prediction',
  'text',
]);
writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), betRows, [
  'checked_date',
  'bet_id',
  'tier',
  'risky_bet',
  'prediction',
  'kill_condition',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
