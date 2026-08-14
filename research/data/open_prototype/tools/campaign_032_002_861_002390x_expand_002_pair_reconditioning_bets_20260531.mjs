import fs from 'node:fs';
import path from 'node:path';

// This script tests whether sign 002 changes how the pair that follows it
// behaves. For every adjacent sign pair H-X in every text of
// lipi/metadata_filtered.csv, it records whether the pair is "gated" (a 002
// immediately precedes H) and whether the text continues after X. Pairs with
// at least 2 gated and 2 ungated rows get an open-rate delta: gated open rate
// minus ungated open rate. A shift of +0.5 or more means "002 opens this
// pair"; -0.5 or less means "002 terminalizes it"; anything between is weak.
// The bets recorded from the result: 002 is a pair-reconditioner, not a
// universal opener — it opens 390-125, closes zero-complement pairs like
// 031-000 and 817-000, and leaves pairs such as 220-455 untouched. Writes the
// pair-shift table, the raw rows for the top shifted pairs, and the bets as
// CSVs plus a summary JSON to data/open_prototype/reports.

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_expand_002_pair_reconditioning_bets_20260531';

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
      symbol: row.symbol,
      cult: row.cult,
      prev_before_h: rowSigns[index - 1] ?? '',
      h,
      x,
      pair: `${h}-${x}`,
      gated_by_002: index > 0 && rowSigns[index - 1] === '002' ? 'True' : 'False',
      x_continuing: index + 1 < rowSigns.length - 1 ? 'True' : 'False',
      x_terminal: index + 1 === rowSigns.length - 1 ? 'True' : 'False',
      tail_after_x: rowSigns.slice(index + 2).join(' ') || '<END>',
      scope_cell: `${row.site}|${row.type}|${row.shape}|${row.material}`,
      text: row.text,
    });
  }
}

const pairNames = [...new Set(pairRows.map((row) => row.pair))].sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
const pairShifts = pairNames
  .map((pair) => {
    const rows = pairRows.filter((row) => row.pair === pair);
    const gated = rows.filter((row) => row.gated_by_002 === 'True');
    const ungated = rows.filter((row) => row.gated_by_002 === 'False');
    const gatedOpen = gated.filter((row) => row.x_continuing === 'True').length;
    const ungatedOpen = ungated.filter((row) => row.x_continuing === 'True').length;
    const gatedRate = gated.length ? gatedOpen / gated.length : null;
    const ungatedRate = ungated.length ? ungatedOpen / ungated.length : null;
    const diff = gatedRate === null || ungatedRate === null ? null : gatedRate - ungatedRate;
    return {
      checked_date: '2026-05-31',
      pair,
      total_rows: String(rows.length),
      gated_rows: String(gated.length),
      gated_open_rate: ratio(gatedOpen, gated.length),
      ungated_rows: String(ungated.length),
      ungated_open_rate: ratio(ungatedOpen, ungated.length),
      open_rate_delta: diff === null ? '' : diff.toFixed(6),
      gated_objects: gated.map((row) => row.object).slice(0, 12).join(';'),
      ungated_objects_sample: ungated.map((row) => row.object).slice(0, 12).join(';'),
      gated_scopes: topCounts(gated, (row) => row.scope_cell),
      ungated_scopes: topCounts(ungated, (row) => row.scope_cell),
      shift_class:
        diff === null
          ? 'insufficient_contrast'
          : diff >= 0.5
            ? '002_opens_pair'
            : diff <= -0.5
              ? '002_terminalizes_pair'
              : 'weak_or_no_shift',
    };
  })
  .filter((row) => Number(row.gated_rows) >= 2 && Number(row.ungated_rows) >= 2)
  .sort((a, b) => Math.abs(Number(b.open_rate_delta)) - Math.abs(Number(a.open_rate_delta)) || Number(b.gated_rows) - Number(a.gated_rows));

const terminalizedZeroPairs = pairShifts.filter(
  (row) => row.shift_class === '002_terminalizes_pair' && row.pair.endsWith('-000'),
);
const openedPairs = pairShifts.filter((row) => row.shift_class === '002_opens_pair');
const stablePairs = pairShifts.filter((row) => row.shift_class === 'weak_or_no_shift' && row.gated_open_rate === row.ungated_open_rate);

const bets = [
  {
    checked_date: '2026-05-31',
    bet_id: 'SIGN002_PAIR_RECONDITIONING_OPERATOR',
    tier: 'candidate',
    claim:
      '`002` is a pair-reconditioning operator: it can push the same H-X pair toward open or terminal behavior depending on H-X identity.',
    support:
      `opens=${openedPairs.map((row) => `${row.pair}:${row.gated_open_rate}v${row.ungated_open_rate}`).join('; ')}; ` +
      `terminalizes=${terminalizedZeroPairs.map((row) => `${row.pair}:${row.gated_open_rate}v${row.ungated_open_rate}`).join('; ')}`,
    prediction:
      'Future high-confidence gated/ungated contrasts should preserve direction of shift for 390-125 and zero-complement pairs.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'SIGN002_ZERO_COMPLEMENT_TERMINALIZER',
    tier: 'wild shot',
    claim:
      '`002` terminalizes zero/unknown complements: gated `031-000`, `000-000`, `817-000`, and `820-000` should close more often than ungated versions.',
    support: terminalizedZeroPairs.map((row) => `${row.pair}:gated ${row.gated_open_rate}; ungated ${row.ungated_open_rate}`).join('; '),
    prediction:
      'A source-visible continuing gated zero-complement row, especially `002-031-000-Y`, breaks the terminalizer bet.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'SIGN002_390125_OPENING_PAIR',
    tier: 'candidate',
    claim:
      '`002` specifically opens `390-125`, while ungated `390-125` remains mixed.',
    support: openedPairs.filter((row) => row.pair === '390-125').map((row) => `gated ${row.gated_open_rate}; ungated ${row.ungated_open_rate}`).join('; '),
    prediction:
      'A strict terminal `002-390-125` kills the most important opening-pair claim.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'SIGN002_DOES_NOT_CONTROL_EVERY_OPEN_PAIR',
    tier: 'candidate',
    claim:
      'Some H-X pairs, such as `220-455`, stay open with or without `002`; this blocks a universal opener reading for `002`.',
    support: stablePairs.filter((row) => row.pair === '220-455').map((row) => `gated ${row.gated_open_rate}; ungated ${row.ungated_open_rate}`).join('; '),
    prediction:
      'If more stable-open pairs appear, parse `002` as a local reconditioner, not a general syntactic opener.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'EXPAND',
  status: 'sign002_pair_reconditioning_bets',
  shifted_pairs_ranked: pairShifts.slice(0, 10),
  opened_pairs: openedPairs.map((row) => row.pair),
  terminalized_zero_pairs: terminalizedZeroPairs.map((row) => row.pair),
  stable_open_pairs: stablePairs.filter((row) => row.gated_open_rate === '1/1' || row.gated_open_rate.endsWith(`/${row.gated_rows}`)).map((row) => row.pair).slice(0, 10),
  new_bets: Object.fromEntries(bets.map((row) => [row.bet_id, row.tier])),
  predictions: [
    '`002-390-125` should continue.',
    '`002-031-000`, `002-817-000`, `002-820-000`, and `002-000-000` should tend to close.',
    '`002-220-455` should not differ from ungated `220-455`, which means 002 is not a universal opener.',
  ],
};

writeCsv(path.join(reportsDir, `${prefix}_pair_shift_summary.csv`), pairShifts, [
  'checked_date',
  'pair',
  'total_rows',
  'gated_rows',
  'gated_open_rate',
  'ungated_rows',
  'ungated_open_rate',
  'open_rate_delta',
  'gated_objects',
  'ungated_objects_sample',
  'gated_scopes',
  'ungated_scopes',
  'shift_class',
]);

writeCsv(path.join(reportsDir, `${prefix}_focus_pair_rows.csv`), pairRows.filter((row) => pairShifts.slice(0, 12).some((shift) => shift.pair === row.pair)), [
  'checked_date',
  'object',
  'id',
  'site',
  'type',
  'shape',
  'material',
  'symbol',
  'cult',
  'prev_before_h',
  'h',
  'x',
  'pair',
  'gated_by_002',
  'x_continuing',
  'x_terminal',
  'tail_after_x',
  'scope_cell',
  'text',
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
