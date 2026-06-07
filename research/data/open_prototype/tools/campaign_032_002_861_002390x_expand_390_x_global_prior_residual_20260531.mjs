import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_expand_390_x_global_prior_residual_20260531';

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

function rate(numerator, denominator) {
  return denominator ? numerator / denominator : null;
}

function signedDelta(target, prior) {
  if (target === null || prior === null) return '';
  return (target - prior).toFixed(6);
}

function countBy(rows, keyFn) {
  const counts = new Map();
  for (const row of rows) {
    const key = keyFn(row) || '-';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }));
}

function topCounts(rows, keyFn) {
  return countBy(rows, keyFn)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

fs.mkdirSync(reportsDir, { recursive: true });

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));
const occurrences = [];
const xSlots = [];
const frames390 = [];

for (const row of metadataRows) {
  const rowSigns = signs(row.text);
  for (let index = 0; index < rowSigns.length; index += 1) {
    occurrences.push({
      checked_date: '2026-05-31',
      object: row.cisi,
      sign: rowSigns[index],
      terminal: index === rowSigns.length - 1,
      continuing: index < rowSigns.length - 1,
      tail_after_sign: rowSigns.slice(index + 1).join(' ') || '<END>',
      scope_cell: `${row.site}|${row.type}|${row.shape}|${row.material}`,
      text: row.text,
    });
    if (rowSigns[index] === '002' && rowSigns[index + 1] && rowSigns[index + 2]) {
      const slot = {
        checked_date: '2026-05-31',
        object: row.cisi,
        site: row.site,
        type: row.type,
        shape: row.shape,
        material: row.material,
        head_after_002: rowSigns[index + 1],
        x: rowSigns[index + 2],
        x_terminal: index + 2 === rowSigns.length - 1,
        x_continuing: index + 2 < rowSigns.length - 1,
        tail_after_x: rowSigns.slice(index + 3).join(' ') || '<END>',
        scope_cell: `${row.site}|${row.type}|${row.shape}|${row.material}`,
        text: row.text,
      };
      xSlots.push(slot);
      if (slot.head_after_002 === '390') frames390.push(slot);
    }
  }
}

const xValues = [...new Set(frames390.map((row) => row.x))].sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
const residualRows = xValues.map((x) => {
  const globalRows = occurrences.filter((row) => row.sign === x);
  const slotRows = xSlots.filter((row) => row.x === x);
  const rows390 = frames390.filter((row) => row.x === x);
  const globalTerminal = globalRows.filter((row) => row.terminal).length;
  const slotTerminal = slotRows.filter((row) => row.x_terminal).length;
  const terminal390 = rows390.filter((row) => row.x_terminal).length;
  const globalRate = rate(globalTerminal, globalRows.length);
  const slotRate = rate(slotTerminal, slotRows.length);
  const rate390 = rate(terminal390, rows390.length);
  let residual_class = 'insufficient_or_aligns_with_prior';
  if (rows390.length >= 1 && Math.abs((rate390 ?? 0) - (slotRate ?? 0)) >= 0.34) residual_class = '390_specific_residual';
  else if (slotRows.length >= 2 && Math.abs((slotRate ?? 0) - (globalRate ?? 0)) >= 0.34) residual_class = 'x_slot_residual';
  return {
    checked_date: '2026-05-31',
    x,
    rows_002390: String(rows390.length),
    terminal_002390: ratio(terminal390, rows390.length),
    all_x_slot_rows: String(slotRows.length),
    terminal_all_x_slots: ratio(slotTerminal, slotRows.length),
    global_occurrences: String(globalRows.length),
    terminal_global: ratio(globalTerminal, globalRows.length),
    delta_390_vs_all_x_slots: signedDelta(rate390, slotRate),
    delta_all_x_slots_vs_global: signedDelta(slotRate, globalRate),
    residual_class,
    heads_all_x_slots: topCounts(slotRows, (row) => row.head_after_002),
    tails_002390: topCounts(rows390, (row) => row.tail_after_x),
    objects_002390: rows390.map((row) => row.object).join(';'),
  };
});

const xSlotResiduals = residualRows.filter((row) => row.residual_class === 'x_slot_residual');
const specific390Residuals = residualRows.filter((row) => row.residual_class === '390_specific_residual');
const signsMatchingBroaderXSlotPrior = residualRows.filter(
  (row) =>
    Number(row.all_x_slot_rows) >= 2 &&
    row.delta_390_vs_all_x_slots !== '' &&
    Math.abs(Number(row.delta_390_vs_all_x_slots)) <= 0.2,
);

const bets = [
  {
    checked_date: '2026-05-31',
    bet_id: 'X_SLOT_PRIOR_BEATS_RAW_SIGN_PRIOR',
    tier: 'candidate',
    claim:
      'Several `002-390-X` signs are better predicted by X-slot behavior than by raw sign terminality, so X-slot function is real.',
    support: xSlotResiduals.map((row) => `${row.x}: slot ${row.terminal_all_x_slots} vs global ${row.terminal_global}`).join('; '),
    prediction:
      'If future X-slot rows for `095/705/125/530` revert to raw global rates, demote the slot-function model.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'SIGN390_SPECIFICITY_SHRINKS',
    tier: 'candidate',
    claim:
      'Most `002-390-X` closure behavior is X-slot class behavior, not unique to head `390`; `390` selects a slot inventory rather than inventing each value.',
    support: signsMatchingBroaderXSlotPrior.map((row) => `${row.x}: 390 ${row.terminal_002390}; all slots ${row.terminal_all_x_slots}`).join('; '),
    prediction:
      'Do not overfit `390`; check whether the same X classes behave similarly under other heads before assigning `390` a semantic value.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'SIGN705_TERMINAL_SLOT_CLASS_NOT_GLOBAL_FINAL_SIGN',
    tier: 'candidate',
    claim:
      '`705` is a terminal X-slot class under `002-390`, even though raw `705` is not usually terminal globally.',
    support: residualRows.filter((row) => row.x === '705').map((row) => `390 ${row.terminal_002390}; all X slots ${row.terminal_all_x_slots}; global ${row.terminal_global}`).join('; '),
    prediction:
      'A bound Dholavira `002-390-705` should close; a continuing `002-H-705-Y` outside known open exception heads would break the class.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'SIGN692_TERMINALITY_MAY_BE_RAW_SIGN_PRIOR',
    tier: 'wild shot',
    claim:
      '`692` closing after `002-390` may not be constructional; raw `692` is already strongly terminal globally.',
    support: residualRows.filter((row) => row.x === '692').map((row) => `390 ${row.terminal_002390}; all X slots ${row.terminal_all_x_slots}; global ${row.terminal_global}`).join('; '),
    prediction:
      'If `692` remains terminal outside the frame and across heads, use it as a closure sign class, not as evidence for a `390` value.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'EXPAND',
  status: 'sign390_x_global_prior_residual',
  residual_rows: residualRows,
  x_slot_residuals: xSlotResiduals.map((row) => row.x),
  specific_390_residuals: specific390Residuals.map((row) => row.x),
  signs_matching_broader_x_slot_prior: signsMatchingBroaderXSlotPrior.map((row) => row.x),
  new_bets: Object.fromEntries(bets.map((row) => [row.bet_id, row.tier])),
  predictions: [
    '`095`, `705`, `072`, and `140` should be evaluated as X-slot classes before assigning them head-390 meanings.',
    '`692` may be terminal because the sign itself has high terminal prior, so it is weaker evidence for the 390 payload parser.',
    'A source-bound continuing `002-390-705-Y` would kill the strongest Dholavira parser prediction.',
  ],
};

writeCsv(path.join(reportsDir, `${prefix}_residuals.csv`), residualRows, [
  'checked_date',
  'x',
  'rows_002390',
  'terminal_002390',
  'all_x_slot_rows',
  'terminal_all_x_slots',
  'global_occurrences',
  'terminal_global',
  'delta_390_vs_all_x_slots',
  'delta_all_x_slots_vs_global',
  'residual_class',
  'heads_all_x_slots',
  'tails_002390',
  'objects_002390',
]);

writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), bets, [
  'checked_date',
  'bet_id',
  'tier',
  'claim',
  'support',
  'prediction',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
