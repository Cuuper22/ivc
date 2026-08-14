import fs from 'node:fs';
import path from 'node:path';

// This script reframes the head-class results as "valency": how many
// arguments a head takes and whether its X slot must continue or must close,
// the way verbs differ in the arguments they demand. It reads the head
// summary and frame CSVs from the earlier head-class discriminator run, keeps
// heads with 3+ frames, and assigns each a valency class from exact counts:
// open_x_head (always takes X, X always continues — head 220),
// terminal_x_head (always takes X, X always closes — head 031),
// mixed_x_head (both outcomes — head 390, where only X=125 opens),
// terminal_default_head (rarely takes X at all), or mixed/low-signal. Four
// bets follow, the sharpest being that 390 is a mixed gate and that 125 is a
// local valency switch rather than a title — plus a list of the most
// embarrassing single rows that would kill each class. Writes the valency
// table and bets as CSVs plus a summary JSON to data/open_prototype/reports.

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const headSummaryPath = path.join(reportsDir, 'campaign_032_002_861_002390x_expand_002_head_class_discriminator_20260531_head_summary.csv');
const framesPath = path.join(reportsDir, 'campaign_032_002_861_002390x_expand_002_head_class_discriminator_20260531_frames.csv');
const prefix = 'campaign_032_002_861_002390x_expand_head_valency_bets_20260531';

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

function ratio(numerator, denominator) {
  return denominator ? `${numerator}/${denominator}` : '0/0';
}

function n(row, key) {
  return Number(row[key] ?? 0);
}

fs.mkdirSync(reportsDir, { recursive: true });

const headSummary = parseCsv(fs.readFileSync(headSummaryPath, 'utf8'));
const frames = parseCsv(fs.readFileSync(framesPath, 'utf8'));
const supported = headSummary.filter((row) => n(row, 'frames') >= 3);

const valencyRows = supported.map((row) => {
  const framesCount = n(row, 'frames');
  const takesX = n(row, 'takes_x_count');
  const xContinuing = n(row, 'x_continuing_count');
  const xTerminal = n(row, 'x_terminal_count');
  let valency_class = 'mixed_or_low_signal';
  if (takesX === framesCount && xContinuing === framesCount) valency_class = 'open_x_head';
  else if (takesX === framesCount && xTerminal === framesCount) valency_class = 'terminal_x_head';
  else if (takesX === framesCount && xContinuing > 0 && xTerminal > 0) valency_class = 'mixed_x_head';
  else if (takesX / framesCount <= 0.2) valency_class = 'terminal_default_head';
  return {
    checked_date: '2026-05-31',
    head: row.head,
    frames: row.frames,
    takes_x_rate: row.takes_x_rate,
    x_terminal_rate: row.x_terminal_rate,
    x_continuing_rate: row.x_continuing_rate,
    dominant_x: row.dominant_x,
    dominant_x_rate: row.dominant_x_rate,
    x_distribution: row.x_distribution,
    prior_head_class: row.head_class,
    valency_class,
    parser_pressure:
      valency_class === 'open_x_head'
        ? 'predicts X is never terminal'
        : valency_class === 'terminal_x_head'
          ? 'predicts X is always terminal'
          : valency_class === 'mixed_x_head'
            ? 'requires sign-specific X subrules'
            : valency_class === 'terminal_default_head'
              ? 'usually no X slot'
              : 'too mixed',
  };
});

const byHead = Object.fromEntries(valencyRows.map((row) => [row.head, row]));
const rowsByHead = (head) => frames.filter((row) => row.head_after_002 === head);
const sampleForHead = (head) => rowsByHead(head).map((row) => `${row.object}:${row.x_after_head}:${row.x_continuing === 'True' ? 'open' : row.x_terminal === 'True' ? 'terminal' : 'none'}`).join('; ');

const bets = [
  {
    checked_date: '2026-05-31',
    bet_id: 'VALENCY_002_220_OPEN_X_HEAD',
    tier: 'wild shot',
    claim:
      '`002-220-X` is an open-X head in the local Mohenjo-daro square steatite register: every X after 220 should continue.',
    support: `head 220: frames=${byHead['220']?.frames}; takes_x=${byHead['220']?.takes_x_rate}; x_continuing=${byHead['220']?.x_continuing_rate}; rows=${sampleForHead('220')}`,
    prediction:
      'A newly bound same-register 002-220-X row should have material after X; terminal X kills or demotes this bet.',
    implication:
      'If it survives, 125 is not uniquely "continuing"; continuation is a head-valency effect that 390 only partly exposes.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'VALENCY_002_031_TERMINAL_X_HEAD',
    tier: 'wild shot',
    claim:
      '`002-031-X` is a terminal-X head: it takes an X slot, but the X closes the line.',
    support: `head 031: frames=${byHead['031']?.frames}; takes_x=${byHead['031']?.takes_x_rate}; x_terminal=${byHead['031']?.x_terminal_rate}; rows=${sampleForHead('031')}`,
    prediction:
      'A newly bound same-register 002-031-X row should end at X; any continuing 002-031-X-Y row kills this as a head class.',
    implication:
      'If it survives, non-125 terminality under 390 may be part of a broader terminal-X head grammar, not a closure sign value.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'VALENCY_002_390_MIXED_GATE_HEAD',
    tier: 'candidate',
    claim:
      '`002-390-X` is a mixed-gate head: it always takes X, but only X=125 enters the open-X lane; other X values behave like terminal complements.',
    support: `head 390: frames=${byHead['390']?.frames}; takes_x=${byHead['390']?.takes_x_rate}; x_continuing=${byHead['390']?.x_continuing_rate}; distribution=${byHead['390']?.x_distribution}`,
    prediction:
      'New same-register 002-390-125 rows continue; new same-register 002-390-non125 rows terminate unless the binary gate is wrong.',
    implication:
      'This converts 125 from title/rank into a possible valency-switch slot under 390.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'VALENCY_125_AS_LOCAL_VALENCY_SWITCH',
    tier: 'wild shot',
    claim:
      '`125` under `390` is a local valency switch: it licenses continuation, but only in specific heads, so terminal non-frame 125 is expected.',
    support:
      'Same-register 002-390-125 is 3/3 continuing, while same-register non-frame 125 can be terminal; head 220 proves continuation can be head-driven without 125.',
    prediction:
      'A continuing 125 should cluster after branch-bearing heads; terminal 125 should be permitted outside that head class.',
    implication:
      'This is a morphology-like role bet without assigning sound, language family, or translation.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'EXPAND',
  status: 'head_valency_bets',
  source_report: path.basename(headSummaryPath),
  valency_classes: {
    open_x_heads: valencyRows.filter((row) => row.valency_class === 'open_x_head').map((row) => row.head),
    terminal_x_heads: valencyRows.filter((row) => row.valency_class === 'terminal_x_head').map((row) => row.head),
    mixed_x_heads: valencyRows.filter((row) => row.valency_class === 'mixed_x_head').map((row) => row.head),
    terminal_default_heads: valencyRows.filter((row) => row.valency_class === 'terminal_default_head').map((row) => row.head),
  },
  new_bets: Object.fromEntries(bets.map((row) => [row.bet_id, row.tier])),
  most_embarrassing_tests: [
    'Find a terminal same-register 002-220-X row.',
    'Find a continuing same-register 002-031-X-Y row.',
    'Find a continuing same-register 002-390-non125-Y row.',
    'Find a terminal same-register 002-390-125 row.',
  ],
};

writeCsv(path.join(reportsDir, `${prefix}_valency_classes.csv`), valencyRows, [
  'checked_date',
  'head',
  'frames',
  'takes_x_rate',
  'x_terminal_rate',
  'x_continuing_rate',
  'dominant_x',
  'dominant_x_rate',
  'x_distribution',
  'prior_head_class',
  'valency_class',
  'parser_pressure',
]);

writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), bets, [
  'checked_date',
  'bet_id',
  'tier',
  'claim',
  'support',
  'prediction',
  'implication',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
