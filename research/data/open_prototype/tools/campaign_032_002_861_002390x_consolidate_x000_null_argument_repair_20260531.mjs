import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_consolidate_x000_null_argument_repair_20260531';
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

function signs(text) {
  return [...String(text || '').matchAll(/\d{3}/g)].map((match) => match[0]);
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function ratio(numerator, denominator) {
  return denominator ? `${numerator}/${denominator}` : '0/0';
}

function rate(numerator, denominator) {
  return denominator ? numerator / denominator : 0;
}

function countBy(items, keyFn) {
  const counts = new Map();
  for (const item of items) {
    const key = keyFn(item) || '-';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }))
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function uniqueRowsByText(rows) {
  return [...new Map(rows.map((row) => [row.tokens.join(' '), row])).values()];
}

function occurrenceRole(tokens, index) {
  if (index >= 2 && tokens[index - 2] === '002') return 'x_slot_after_002_head';
  if (index >= 1 && tokens[index - 1] === '002') return 'head_slot_after_002';
  const firstFrame = tokens.indexOf('002');
  if (firstFrame >= 0 && index > firstFrame) return 'post_frame_non_x_payload';
  if (firstFrame >= 0 && index < firstFrame) return 'prefix_before_002_frame';
  return 'no_002_context';
}

function terminalAfter(tokens, index) {
  return index === tokens.length - 1;
}

function formatRate(value) {
  return value.toFixed(3);
}

function slotContrast(occurrences, role) {
  const roleRows = occurrences.filter((row) => row.role === role);
  const zeroRows = roleRows.filter((row) => row.sign === '000');
  const nonZeroRows = roleRows.filter((row) => row.sign !== '000');
  const zeroTerminal = zeroRows.filter((row) => row.terminal_after_sign === 'true');
  const nonZeroTerminal = nonZeroRows.filter((row) => row.terminal_after_sign === 'true');
  const zeroRate = rate(zeroTerminal.length, zeroRows.length);
  const nonZeroRate = rate(nonZeroTerminal.length, nonZeroRows.length);
  return {
    checked_date: checkedDate,
    role,
    zero_rows: String(zeroRows.length),
    zero_terminal: ratio(zeroTerminal.length, zeroRows.length),
    zero_rate: formatRate(zeroRate),
    nonzero_rows: String(nonZeroRows.length),
    nonzero_terminal: ratio(nonZeroTerminal.length, nonZeroRows.length),
    nonzero_rate: formatRate(nonZeroRate),
    rate_gap_zero_minus_nonzero: formatRate(zeroRate - nonZeroRate),
    verdict:
      role === 'prefix_before_002_frame'
        ? 'invalid_as_terminal_control_tautological'
        : zeroRows.length >= 10 && zeroRate - nonZeroRate >= 0.2
          ? 'supports_zero_specific_terminality'
          : zeroRows.length < 10
            ? 'too_few_zero_rows'
            : 'does_not_support_zero_specific_terminality',
    top_nonzero_next_or_end: countBy(nonZeroRows, (row) => (row.terminal_after_sign === 'true' ? '<END>' : row.next1)),
    zero_examples: zeroRows.slice(0, 8).map((row) => `${row.object}:${row.prev2}-${row.prev1}-000-${row.next1}`).join(' | '),
  };
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = uniqueRowsByText(
  parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
    ...row,
    object: objectId(row),
    tokens: signs(row.text),
  })),
);

const occurrences = [];
for (const row of rows) {
  row.tokens.forEach((sign, index) => {
    const role = occurrenceRole(row.tokens, index);
    occurrences.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      text: row.text,
      token_index: String(index),
      sign,
      prev2: row.tokens[index - 2] ?? '<START>',
      prev1: row.tokens[index - 1] ?? '<START>',
      next1: row.tokens[index + 1] ?? '<END>',
      next2: row.tokens[index + 2] ?? '<END>',
      role,
      terminal_after_sign: String(terminalAfter(row.tokens, index)),
    });
  });
}

const roles = [
  'x_slot_after_002_head',
  'head_slot_after_002',
  'post_frame_non_x_payload',
  'prefix_before_002_frame',
  'no_002_context',
];
const contrasts = roles.map((role) => slotContrast(occurrences, role));

const decisions = [
  {
    checked_date: checkedDate,
    decision_id: 'CONSOLIDATE_REJECT_PREFRAME_TERMINAL_CONTROL',
    action: 'demote_evidence',
    target: 'prefix_before_002_frame 000 terminal=0/147',
    reason:
      'A token counted before a later 002 frame necessarily has following tokens, so terminal_after_000=0 is not an independent null-control result.',
    model_effect:
      'Remove pre-frame terminality as support for frame-proximal null. Keep it only as a positional-continuation observation.',
  },
  {
    checked_date: checkedDate,
    decision_id: 'CONSOLIDATE_KEEP_XSLOT_000_AS_CLEAN_SUBRULE',
    action: 'keep',
    target: 'X-slot 000',
    reason:
      'X-slot 000 terminality remains higher than nonzero X-slot signs under the repaired role-matched contrast.',
    model_effect:
      'X=000 remains the cleanest zero-complement subclass.',
  },
  {
    checked_date: checkedDate,
    decision_id: 'CONSOLIDATE_DEMOTE_BROAD_FRAME_NULL_TO_EDGE_CANDIDATE',
    action: 'demote',
    target: 'broad frame-proximal null operator',
    reason:
      'Head-slot 000 and post-frame 000 are terminal, but the repaired contrast must compare them to same-role nonzero signs before they can broaden the rule.',
    model_effect:
      'The core model becomes X=000 zero-complement plus a weaker edge candidate for other frame-proximal 000 positions.',
  },
];

const xContrast = contrasts.find((row) => row.role === 'x_slot_after_002_head');
const headContrast = contrasts.find((row) => row.role === 'head_slot_after_002');
const postFrameContrast = contrasts.find((row) => row.role === 'post_frame_non_x_payload');

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: 'x000_null_argument_repair',
  repaired_findings: {
    preframe_control: 'demoted_as_tautological_for_terminality',
    x_slot_000: `${xContrast.zero_terminal} vs nonzero ${xContrast.nonzero_terminal}; gap=${xContrast.rate_gap_zero_minus_nonzero}`,
    head_slot_000: `${headContrast.zero_terminal} vs nonzero ${headContrast.nonzero_terminal}; gap=${headContrast.rate_gap_zero_minus_nonzero}`,
    post_frame_000: `${postFrameContrast.zero_terminal} vs nonzero ${postFrameContrast.nonzero_terminal}; gap=${postFrameContrast.rate_gap_zero_minus_nonzero}`,
  },
  model_consequence:
    'Keep X=000 zero-complement as strongest null rule; demote broad frame-proximal null from core to edge candidate until same-role nonzero contrasts and source-bound tails support it.',
};

writeCsv(path.join(reportsDir, `${prefix}_role_contrasts.csv`), contrasts, [
  'checked_date',
  'role',
  'zero_rows',
  'zero_terminal',
  'zero_rate',
  'nonzero_rows',
  'nonzero_terminal',
  'nonzero_rate',
  'rate_gap_zero_minus_nonzero',
  'verdict',
  'top_nonzero_next_or_end',
  'zero_examples',
]);
writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  'checked_date',
  'decision_id',
  'action',
  'target',
  'reason',
  'model_effect',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
