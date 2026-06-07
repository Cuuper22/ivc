import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const parseRowsPath = path.join(
  reportsDir,
  'campaign_032_002_861_002390x_expand_x000_null_class_20260531_parse_rows_plus_000.csv',
);
const prefix = 'campaign_032_002_861_002390x_consolidate_x000_exception_targets_20260531';
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

function exceptionType(tail) {
  const tokens = tail === '<END>' ? [] : tail.split(' ');
  if (!tokens.length) return 'closed_control';
  if (tokens[0] === '000') return 'zero_chain_exception';
  if (tokens[0] === '002') return 'frame_reset_exception';
  if (tokens[0] === '033') return 'nonzero_payload_exception';
  return 'other_payload_exception';
}

function sourceImplication(row) {
  const kind = exceptionType(row.tail_after_x);
  if (kind === 'zero_chain_exception') {
    return 'If source confirms the whole tail as continuous, X=000 becomes zero-chain/reset notation rather than simple closure; if 906/388 are governed payload, the rule is damaged.';
  }
  if (kind === 'frame_reset_exception') {
    return 'If post-000 002 starts a new frame, zero-complement survives; if 002 is payload after 000, the rule is damaged.';
  }
  if (kind === 'nonzero_payload_exception') {
    return 'If 033 is real payload after X=000, this is the cleanest killer row; if it is side/frame separation or mistranscription, the rule survives.';
  }
  return 'Closed control row.';
}

function severity(row) {
  const kind = exceptionType(row.tail_after_x);
  if (kind === 'nonzero_payload_exception') return 'high';
  if (kind === 'zero_chain_exception') return 'high';
  if (kind === 'frame_reset_exception') return 'medium';
  return 'control';
}

fs.mkdirSync(reportsDir, { recursive: true });

const parseRows = parseCsv(fs.readFileSync(parseRowsPath, 'utf8'));
const x000 = parseRows.filter((row) => row.x === '000');
const open = x000.filter((row) => row.tail_after_x !== '<END>');
const terminalControls = x000.filter((row) => row.tail_after_x === '<END>');
const targets = open.map((row) => ({
  checked_date: checkedDate,
  target: row.object.startsWith('-:') ? row.row_id : row.object,
  object: row.object,
  row_id: row.row_id,
  site: row.site,
  type: row.type,
  text: row.text,
  head: row.head,
  tail_after_x: row.tail_after_x,
  exception_type: exceptionType(row.tail_after_x),
  severity: severity(row),
  current_gloss: row.gloss_skeleton,
  source_success_for_rule: sourceImplication(row),
  rule_damage_outcome:
    'A source-bound meaningful payload tail after X=000 demotes zero-complement from core to register/formula-limited candidate.',
  rule_promotion_outcome:
    'A source-bound reset, side break, zero-chain, or transcription correction keeps X=000 as the strongest core subrule.',
}));

const controls = terminalControls.map((row) => ({
  checked_date: checkedDate,
  target: row.object.startsWith('-:') ? row.row_id : row.object,
  object: row.object,
  row_id: row.row_id,
  site: row.site,
  type: row.type,
  text: row.text,
  head: row.head,
  tail_after_x: row.tail_after_x,
  exception_type: 'closed_control',
  severity: 'control',
  current_gloss: row.gloss_skeleton,
  source_success_for_rule: 'If source confirms terminal 000, it supports the zero-complement core.',
  rule_damage_outcome: 'A hidden payload tail after final 000 damages the rule.',
  rule_promotion_outcome: 'Terminal source-bound X=000 promotes zero-complement behavior.',
}));

const decisions = [
  {
    checked_date: checkedDate,
    decision_id: 'CONSOLIDATE_X000_EXCEPTION_TARGETS_FIRST',
    action: 'rank_next_destructive_tests',
    target: targets.map((row) => row.target).join(';'),
    reason: 'These are the only current X=000 rows that actually continue after 000.',
    next_status: 'attack_before_expanding_new_null_claims',
  },
  {
    checked_date: checkedDate,
    decision_id: 'CONSOLIDATE_X000_NONZERO_PAYLOAD_KILL_SWITCH',
    action: 'define_kill_switch',
    target: targets.filter((row) => row.exception_type === 'nonzero_payload_exception').map((row) => row.target).join(';') || '-',
    reason: 'A real nonzero payload after X=000 is the sharpest possible local kill condition.',
    next_status: 'highest_priority_if_source_available',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: 'x000_exception_targets',
  x000_rows: x000.length,
  open_exceptions: targets.length,
  closed_controls: controls.length,
  exception_types: targets.map((row) => `${row.target}:${row.exception_type}`).join(';'),
  highest_priority_targets: targets.filter((row) => row.severity === 'high').map((row) => row.target),
  conclusion:
    'X=000 consolidation now hinges on three open exceptions: zero-chain M-451, reset Ns-66, and nonzero-payload 4148.1.',
};

writeCsv(path.join(reportsDir, `${prefix}_exceptions.csv`), targets, [
  'checked_date',
  'target',
  'object',
  'row_id',
  'site',
  'type',
  'text',
  'head',
  'tail_after_x',
  'exception_type',
  'severity',
  'current_gloss',
  'source_success_for_rule',
  'rule_damage_outcome',
  'rule_promotion_outcome',
]);
writeCsv(path.join(reportsDir, `${prefix}_closed_controls.csv`), controls, [
  'checked_date',
  'target',
  'object',
  'row_id',
  'site',
  'type',
  'text',
  'head',
  'tail_after_x',
  'exception_type',
  'severity',
  'current_gloss',
  'source_success_for_rule',
  'rule_damage_outcome',
  'rule_promotion_outcome',
]);
writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  'checked_date',
  'decision_id',
  'action',
  'target',
  'reason',
  'next_status',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
