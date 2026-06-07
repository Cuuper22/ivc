import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_expand_002_head_class_discriminator_20260531';

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

function ratio(numerator, denominator) {
  return denominator ? `${numerator}/${denominator}` : '0/0';
}

function countBy(rows, keyFn) {
  const counts = new Map();
  for (const row of rows) {
    const key = keyFn(row) || '<END>';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }));
}

function topCounts(rows, keyFn, limit = 8) {
  return countBy(rows, keyFn)
    .slice(0, limit)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function headClass(row) {
  const immediateEndRate = Number(row.immediate_end_count) / Number(row.frames);
  const branchBearingRate = Number(row.takes_x_count) / Number(row.frames);
  const continuingRate = Number(row.x_continuing_count) / Number(row.frames);
  if (row.head === '390') return 'branch_selector_candidate';
  if (Number(row.frames) >= 3 && immediateEndRate >= 0.8) return 'terminal_default_head';
  if (Number(row.frames) >= 3 && branchBearingRate >= 0.8 && continuingRate >= 0.25) return 'branch_bearing_head';
  if (Number(row.frames) >= 3 && branchBearingRate >= 0.8) return 'branch_taking_terminal_head';
  return 'low_support_or_mixed';
}

fs.mkdirSync(reportsDir, { recursive: true });

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));
const sameRegisterRows = metadataRows.filter(
  (row) =>
    row.site === 'Mohenjo-daro' &&
    row.type === 'SEAL:S' &&
    row.shape === 'square' &&
    row.material === 'Steatite',
);

const frames = [];
for (const row of sameRegisterRows) {
  const rowSigns = signs(row.text);
  for (let index = 0; index < rowSigns.length; index += 1) {
    if (rowSigns[index] !== '002' || !rowSigns[index + 1]) continue;
    const head = rowSigns[index + 1];
    const x = rowSigns[index + 2] ?? '<END>';
    const takesX = x !== '<END>';
    frames.push({
      checked_date: '2026-05-31',
      object: row.cisi,
      id: row.id,
      prev_before_002: rowSigns[index - 1] ?? '',
      head_after_002: head,
      x_after_head: x,
      takes_x: takesX ? 'True' : 'False',
      x_terminal: takesX && index + 2 === rowSigns.length - 1 ? 'True' : 'False',
      x_continuing: takesX && index + 2 < rowSigns.length - 1 ? 'True' : 'False',
      tail_after_x: takesX ? rowSigns.slice(index + 3).join(' ') || '<END>' : '<NONE>',
      symbol: row.symbol,
      cult: row.cult,
      complete: row.complete,
      condition: row.condition,
      text: row.text,
    });
  }
}

const headValues = [...new Set(frames.map((row) => row.head_after_002))].sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
const headRows = headValues.map((head) => {
  const rows = frames.filter((row) => row.head_after_002 === head);
  const takesX = rows.filter((row) => row.takes_x === 'True');
  const xTerminal = rows.filter((row) => row.x_terminal === 'True');
  const xContinuing = rows.filter((row) => row.x_continuing === 'True');
  const nextCounts = countBy(rows, (row) => row.x_after_head);
  const dominant = nextCounts[0] ?? ['<NONE>', 0];
  const summary = {
    checked_date: '2026-05-31',
    head,
    frames: String(rows.length),
    immediate_end_count: String(rows.length - takesX.length),
    immediate_end_rate: ratio(rows.length - takesX.length, rows.length),
    takes_x_count: String(takesX.length),
    takes_x_rate: ratio(takesX.length, rows.length),
    x_terminal_count: String(xTerminal.length),
    x_terminal_rate: ratio(xTerminal.length, rows.length),
    x_continuing_count: String(xContinuing.length),
    x_continuing_rate: ratio(xContinuing.length, rows.length),
    dominant_x: dominant[0],
    dominant_x_rate: ratio(dominant[1], rows.length),
    x_distribution: topCounts(rows, (row) => row.x_after_head),
    sample_objects: rows.map((row) => row.object).slice(0, 12).join(';'),
  };
  return { ...summary, head_class: headClass(summary) };
});

const supportedHeads = headRows.filter((row) => Number(row.frames) >= 3);
const head390 = headRows.find((row) => row.head === '390');
const terminalDefaults = supportedHeads.filter((row) => row.head_class === 'terminal_default_head');
const branchBearing = supportedHeads.filter((row) => row.head_class === 'branch_bearing_head' || row.head_class === 'branch_selector_candidate');

const bets = [
  {
    checked_date: '2026-05-31',
    bet_id: 'HEAD_CLASS_390_BRANCH_SELECTOR',
    tier: 'candidate',
    claim:
      'Inside Mohenjo-daro square steatite SEAL:S, 002-390 is a branch-selector head: it always takes an X slot, and only X=125 continues.',
    support: `390 frames=${head390?.frames}; takes_x=${head390?.takes_x_rate}; x_continuing=${head390?.x_continuing_rate}; x_distribution=${head390?.x_distribution}`,
    falsifier:
      'A strict same-register 002-390 row with no X, or a strict non-125 X that continues, demotes this to ordinary formula variation.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'TERMINAL_DEFAULT_HEADS_861_817_820',
    tier: 'wild shot',
    claim:
      'Heads 861, 817, and 820 are terminal-default heads after 002 in this register, contrasting with branch-selector 390.',
    support: terminalDefaults
      .filter((row) => ['861', '817', '820'].includes(row.head))
      .map((row) => `${row.head}:immediate_end=${row.immediate_end_rate}`)
      .join('; '),
    falsifier:
      'A source-visible same-register batch where 861/817/820 often take productive X branches, or where 390 often ends immediately.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'BRANCH_HEAD_CLASS_NOT_SIGN_MEANING',
    tier: 'candidate',
    claim:
      'The useful unit is not the sign value of 390 or 125; it is a local head-class rule: terminal-default heads versus branch-selector heads.',
    support: `supported_heads=${supportedHeads.length}; terminal_default=${terminalDefaults.map((row) => row.head).join(';')}; branch_bearing=${branchBearing.map((row) => row.head).join(';')}`,
    falsifier:
      'If head classes fail after text-family/source collapse, abandon head-class grammar and fall back to object/register formulas.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'EXPAND',
  status: '002_head_class_discriminator',
  same_register_scope: 'Mohenjo-daro|SEAL:S|square|Steatite',
  frames: frames.length,
  supported_heads: supportedHeads.length,
  head_390: head390,
  terminal_default_heads: terminalDefaults.map((row) => row.head),
  branch_bearing_heads: branchBearing.map((row) => row.head),
  new_bets: Object.fromEntries(bets.map((row) => [row.bet_id, row.tier])),
  immediate_tests: [
    'Source-collapse terminal-default heads 861/817/820 to make sure they are not duplicate/register artifacts.',
    'Hunt strict same-register 002-390 with no X; that kills branch-selector 390.',
    'Hunt strict same-register 002-390-non125-Y continuation; that kills binary 125/non125 parser.',
  ],
};

writeCsv(path.join(reportsDir, `${prefix}_frames.csv`), frames, [
  'checked_date',
  'object',
  'id',
  'prev_before_002',
  'head_after_002',
  'x_after_head',
  'takes_x',
  'x_terminal',
  'x_continuing',
  'tail_after_x',
  'symbol',
  'cult',
  'complete',
  'condition',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_head_summary.csv`), headRows, [
  'checked_date',
  'head',
  'frames',
  'immediate_end_count',
  'immediate_end_rate',
  'takes_x_count',
  'takes_x_rate',
  'x_terminal_count',
  'x_terminal_rate',
  'x_continuing_count',
  'x_continuing_rate',
  'dominant_x',
  'dominant_x_rate',
  'x_distribution',
  'sample_objects',
  'head_class',
]);

writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), bets, [
  'checked_date',
  'bet_id',
  'tier',
  'claim',
  'support',
  'falsifier',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
