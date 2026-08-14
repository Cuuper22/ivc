// Stress-tests the claim that sign 002 "reconditions" the pair that follows it,
// i.e. changes whether a pair like 390-125 keeps the inscription open or ends
// it. The danger is double counting: repeated formulaic inscriptions can make a
// weak effect look strong. So this script lists every adjacent sign pair in the
// local Lipi metadata, marks whether it is gated by a preceding 002 and whether
// the inscription continues after it, then recomputes the gated-versus-ungated
// open-rate difference under four levels of duplicate collapsing (raw rows down
// to one row per pair+gate). Six focus pairs get individual verdicts. Writes
// focus shifts, all shifts, and decisions CSVs plus a summary JSON to
// data/open_prototype/reports/. Recorded outcome: the 390-125 "opening" effect
// mostly belongs to 125's own tail behavior, so 002 survives only as a weak
// reconditioner whose cleanest effect is terminalizing zero complements.

import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_consolidate_002_reconditioning_collapse_20260531';
const focusPairs = new Set(['390-125', '031-000', '000-000', '820-000', '817-000', '220-455']);

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

function collapseRows(rows, keyFn) {
  const seen = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    if (!seen.has(key)) seen.set(key, row);
  }
  return [...seen.values()];
}

function countOpen(rows) {
  return rows.filter((row) => row.open).length;
}

function shiftRows(setName, rows) {
  const pairs = [...new Set(rows.map((row) => row.pair))].sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
  return pairs
    .map((pair) => {
      const pairRows = rows.filter((row) => row.pair === pair);
      const gated = pairRows.filter((row) => row.gated_by_002);
      const ungated = pairRows.filter((row) => !row.gated_by_002);
      if (!gated.length || !ungated.length) return null;
      const gatedOpen = countOpen(gated);
      const ungatedOpen = countOpen(ungated);
      const gatedRate = rate(gatedOpen, gated.length);
      const ungatedRate = rate(ungatedOpen, ungated.length);
      const delta = gatedRate - ungatedRate;
      return {
        checked_date: '2026-05-31',
        set_name: setName,
        pair,
        gated_rows: String(gated.length),
        gated_open_rate: ratio(gatedOpen, gated.length),
        ungated_rows: String(ungated.length),
        ungated_open_rate: ratio(ungatedOpen, ungated.length),
        open_rate_delta: delta.toFixed(6),
        gated_objects: gated.map((row) => row.object).join(';'),
        ungated_objects_sample: ungated.map((row) => row.object).slice(0, 12).join(';'),
        decision:
          delta >= 0.5
            ? 'strong_opening_shift'
            : delta >= 0.25
              ? 'weak_opening_shift'
              : delta <= -0.5
                ? 'strong_terminalizing_shift'
                : delta <= -0.25
                  ? 'weak_terminalizing_shift'
                  : 'no_shift',
      };
    })
    .filter(Boolean);
}

fs.mkdirSync(reportsDir, { recursive: true });

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));
const pairRows = [];
for (const row of metadataRows) {
  const rowSigns = signs(row.text);
  for (let index = 0; index < rowSigns.length - 1; index += 1) {
    const h = rowSigns[index];
    const x = rowSigns[index + 1];
    pairRows.push({
      checked_date: '2026-05-31',
      object: row.cisi,
      id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      scope_cell: `${row.site}|${row.type}|${row.shape}|${row.material}`,
      prev_before_h: rowSigns[index - 1] ?? '',
      h,
      x,
      pair: `${h}-${x}`,
      gated_by_002: index > 0 && rowSigns[index - 1] === '002',
      open: index + 1 < rowSigns.length - 1,
      tail_after_x: rowSigns.slice(index + 2).join(' ') || '<END>',
      text: row.text,
    });
  }
}

const sets = [
  ['raw', pairRows],
  ['collapse_scope_pair_tail_gate', collapseRows(pairRows, (row) => `${row.scope_cell}|${row.pair}|${row.tail_after_x}|${row.gated_by_002}`)],
  ['collapse_pair_tail_gate', collapseRows(pairRows, (row) => `${row.pair}|${row.tail_after_x}|${row.gated_by_002}`)],
  ['collapse_pair_gate', collapseRows(pairRows, (row) => `${row.pair}|${row.gated_by_002}`)],
];

const shifts = sets.flatMap(([setName, rows]) => shiftRows(setName, rows));
const focus = shifts.filter((row) => focusPairs.has(row.pair));

function focusMetric(setName, pair) {
  return focus.find((row) => row.set_name === setName && row.pair === pair);
}

const decisions = [
  {
    checked_date: '2026-05-31',
    candidate: 'SIGN002_PAIR_RECONDITIONING_OPERATOR',
    decision: 'narrow_to_zero_complement_terminalizer_plus_weak_pair_reconditioner',
    evidence:
      `390-125 raw ${focusMetric('raw', '390-125').open_rate_delta}; ` +
      `390-125 pair-tail ${focusMetric('collapse_pair_tail_gate', '390-125').open_rate_delta}; ` +
      `390-125 pair-only ${focusMetric('collapse_pair_gate', '390-125').open_rate_delta}; ` +
      `031-000 pair-tail ${focusMetric('collapse_pair_tail_gate', '031-000').open_rate_delta}; ` +
      `000-000 pair-tail ${focusMetric('collapse_pair_tail_gate', '000-000').open_rate_delta}`,
    consequence:
      '`002` can stay as a reconditioning frame, but `390-125` opening should be carried mainly by X-slot `125`; zero-complement terminalization is the cleaner `002` effect.',
  },
  {
    checked_date: '2026-05-31',
    candidate: 'SIGN002_390125_OPENING_PAIR',
    decision: 'demote_from_core_to_supporting',
    evidence:
      `raw delta ${focusMetric('raw', '390-125').open_rate_delta}; pair-tail delta ${focusMetric('collapse_pair_tail_gate', '390-125').open_rate_delta}; pair-only delta ${focusMetric('collapse_pair_gate', '390-125').open_rate_delta}`,
    consequence:
      'Do not use `002` alone to explain `390-125`; require X-slot tail-family evidence.',
  },
  {
    checked_date: '2026-05-31',
    candidate: 'SIGN002_ZERO_COMPLEMENT_TERMINALIZER',
    decision: 'keep_candidate_but_note_low_gated_family_counts',
    evidence:
      `031-000 raw ${focusMetric('raw', '031-000').open_rate_delta}; pair-tail ${focusMetric('collapse_pair_tail_gate', '031-000').open_rate_delta}; ` +
      `817-000 pair-tail ${focusMetric('collapse_pair_tail_gate', '817-000').open_rate_delta}; 820-000 pair-tail ${focusMetric('collapse_pair_tail_gate', '820-000').open_rate_delta}`,
    consequence:
      'Terminalizer survives directionally, but gated families collapse to singletons for harsh tests; next expansion needs new gated zero-complement rows.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'CONSOLIDATE',
  status: '002_reconditioning_collapse',
  focus_pairs: [...focusPairs],
  focus,
  decisions,
  compressed_read:
    '`002` remains a frame/reconditioner candidate, but its cleanest surviving effect is terminalizing zero/unknown complements; `390-125` opening is reassigned mostly to X-slot `125` tail behavior.',
};

writeCsv(path.join(reportsDir, `${prefix}_focus_shifts.csv`), focus, [
  'checked_date',
  'set_name',
  'pair',
  'gated_rows',
  'gated_open_rate',
  'ungated_rows',
  'ungated_open_rate',
  'open_rate_delta',
  'gated_objects',
  'ungated_objects_sample',
  'decision',
]);

writeCsv(path.join(reportsDir, `${prefix}_all_shifts.csv`), shifts, [
  'checked_date',
  'set_name',
  'pair',
  'gated_rows',
  'gated_open_rate',
  'ungated_rows',
  'ungated_open_rate',
  'open_rate_delta',
  'gated_objects',
  'ungated_objects_sample',
  'decision',
]);

writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  'checked_date',
  'candidate',
  'decision',
  'evidence',
  'consequence',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
