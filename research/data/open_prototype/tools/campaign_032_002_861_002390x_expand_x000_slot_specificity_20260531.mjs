import fs from 'node:fs';
import path from 'node:path';

// If sign 000 were just a blank or a damage marker, it should behave the same everywhere in
// an inscription. This script checks whether it instead behaves like a zero only in specific
// slots. It reads data/open_prototype/lipi/metadata_filtered.csv, dedupes to unique sign
// sequences, and classifies every occurrence of 000 by its position relative to the first 002
// frame sign: X slot (two after 002), head slot (right after 002), prefix before the frame,
// payload after the frame, or no 002 at all. For each role it measures how often the text
// ends right after the 000. The key comparison is the terminal-rate gap between X-slot 000
// and everything else, plus a broader frame-proximal-versus-pre-frame contrast. Two bets
// ride on those gaps: 000 as a slot-specific zero, or as a frame-proximal null operator.
// Writes the occurrence CSV, a per-role summary CSV, a bets CSV, and a summary JSON to
// reports/.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_x000_slot_specificity_20260531';
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

function percentage(numerator, denominator) {
  return denominator ? (numerator / denominator).toFixed(3) : '0.000';
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

function zeroRole(tokens, index) {
  if (index >= 2 && tokens[index - 2] === '002') return 'x_slot_after_002_head';
  if (index >= 1 && tokens[index - 1] === '002') return 'head_slot_after_002';
  const firstFrame = tokens.indexOf('002');
  if (firstFrame >= 0 && index < firstFrame) return 'prefix_before_002_frame';
  if (firstFrame >= 0 && index > firstFrame) return 'post_frame_non_x_payload';
  return 'no_002_context';
}

function continuation(tokens, index) {
  const tail = tokens.slice(index + 1);
  if (!tail.length) return '<END>';
  if (tail.length === 1) return tail[0];
  return tail.join(' ');
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
  row.tokens.forEach((token, index) => {
    if (token !== '000') return;
    occurrences.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      text: row.text,
      token_index: String(index),
      prev2: row.tokens[index - 2] ?? '<START>',
      prev1: row.tokens[index - 1] ?? '<START>',
      next1: row.tokens[index + 1] ?? '<END>',
      next2: row.tokens[index + 2] ?? '<END>',
      zero_role: zeroRole(row.tokens, index),
      terminal_after_000: String(index === row.tokens.length - 1),
      continuation_after_000: continuation(row.tokens, index),
    });
  });
}

const roleRows = [...new Set(occurrences.map((row) => row.zero_role))].map((role) => {
  const subset = occurrences.filter((row) => row.zero_role === role);
  const terminal = subset.filter((row) => row.terminal_after_000 === 'true');
  return {
    checked_date: checkedDate,
    zero_role: role,
    occurrences: String(subset.length),
    terminal_after_000: ratio(terminal.length, subset.length),
    terminal_rate: percentage(terminal.length, subset.length),
    top_next1: countBy(subset, (row) => row.next1),
    top_sites: countBy(subset, (row) => row.site),
    examples: subset
      .slice(0, 8)
      .map((row) => `${row.object}:${row.prev2}-${row.prev1}-000-${row.next1}`)
      .join(' | '),
  };
});

const xSlot = occurrences.filter((row) => row.zero_role === 'x_slot_after_002_head');
const nonX = occurrences.filter((row) => row.zero_role !== 'x_slot_after_002_head');
const xTerminal = xSlot.filter((row) => row.terminal_after_000 === 'true');
const nonXTerminal = nonX.filter((row) => row.terminal_after_000 === 'true');
const terminalGap = xSlot.length && nonX.length ? xTerminal.length / xSlot.length - nonXTerminal.length / nonX.length : 0;
const frameProximal = occurrences.filter((row) =>
  ['x_slot_after_002_head', 'head_slot_after_002', 'post_frame_non_x_payload'].includes(row.zero_role),
);
const frameProximalTerminal = frameProximal.filter((row) => row.terminal_after_000 === 'true');
const prefixBeforeFrame = occurrences.filter((row) => row.zero_role === 'prefix_before_002_frame');
const prefixBeforeFrameTerminal = prefixBeforeFrame.filter((row) => row.terminal_after_000 === 'true');

const bets = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_X000_SLOT_SPECIFIC_ZERO_NOT_GENERIC_BLANK',
    tier: xSlot.length >= 20 && xTerminal.length / xSlot.length >= 0.85 && terminalGap >= 0.25 ? 'candidate' : 'wild_shot',
    risky_bet:
      '`000` is not merely a generic blank/damage sign: when it sits in X slot after `002-H`, it behaves like zero complement more strongly than all non-X `000` occurrences lumped together.',
    current_test:
      `x_slot_terminal=${ratio(xTerminal.length, xSlot.length)}; non_x_terminal=${ratio(nonXTerminal.length, nonX.length)}; terminal_gap=${terminalGap.toFixed(3)}; role_counts=${countBy(occurrences, (row) => row.zero_role)}.`,
    destructive_prediction:
      'If source-bound X-slot `000` starts carrying diverse payload tails, the zero-complement reading is placeholder overfit. If frame-proximal non-X `000` closes equally, the claim must mutate from X-specific to frame-proximal null.',
    promotion_prediction:
      'If X-slot `000` keeps closing while prefix/head/payload `000` continues freely, the parser gains a slot-specific zero rule.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_X000_FRAME_PROXIMAL_NULL_OPERATOR',
    tier:
      frameProximal.length >= 50 &&
      frameProximalTerminal.length / frameProximal.length >= 0.8 &&
      prefixBeforeFrameTerminal.length === 0
        ? 'candidate'
        : 'wild_shot',
    risky_bet:
      '`000` may be a frame-proximal null operator licensed by the `002` construction, not a purely X-slot sign: head-slot, X-slot, and post-frame `000` all terminalize, while pre-frame `000` does not.',
    current_test:
      `frame_proximal_terminal=${ratio(frameProximalTerminal.length, frameProximal.length)}; prefix_before_frame_terminal=${ratio(prefixBeforeFrameTerminal.length, prefixBeforeFrame.length)}; role_counts=${countBy(occurrences, (row) => row.zero_role)}.`,
    destructive_prediction:
      'If source-strict pre-frame `000` can close, or frame-proximal `000` repeatedly takes meaningful payload tails, the null-operator interpretation dies.',
    promotion_prediction:
      'If future rows preserve high terminality for frame-proximal `000` and zero terminality before the frame, `000` becomes a positional null operator rather than damage.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'x000_slot_specificity',
  occurrences: occurrences.length,
  x_slot_occurrences: xSlot.length,
  x_slot_terminal: xTerminal.length,
  non_x_occurrences: nonX.length,
  non_x_terminal: nonXTerminal.length,
  frame_proximal_occurrences: frameProximal.length,
  frame_proximal_terminal: frameProximalTerminal.length,
  prefix_before_frame_occurrences: prefixBeforeFrame.length,
  prefix_before_frame_terminal: prefixBeforeFrameTerminal.length,
  terminal_gap: Number(terminalGap.toFixed(3)),
  role_counts: countBy(occurrences, (row) => row.zero_role),
  bets: bets.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

writeCsv(path.join(reportsDir, `${prefix}_occurrences.csv`), occurrences, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'text',
  'token_index',
  'prev2',
  'prev1',
  'next1',
  'next2',
  'zero_role',
  'terminal_after_000',
  'continuation_after_000',
]);
writeCsv(path.join(reportsDir, `${prefix}_role_summary.csv`), roleRows, [
  'checked_date',
  'zero_role',
  'occurrences',
  'terminal_after_000',
  'terminal_rate',
  'top_next1',
  'top_sites',
  'examples',
]);
writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), bets, [
  'checked_date',
  'bet_id',
  'tier',
  'risky_bet',
  'current_test',
  'destructive_prediction',
  'promotion_prediction',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
