import fs from 'node:fs';
import path from 'node:path';

// This script sharpens the 002 story into a "valency gate" hypothesis: 002
// does not simply mean "keep going" — it sets up a frame that changes what
// the following H-X pair does. It scans lipi/metadata_filtered.csv for eight
// hand-picked focus pairs (390-125, 610-125, 405-125, 861-125, 906-125,
// 031-000, 031-032, 220-455) and contrasts each pair's open rate when a 002
// immediately precedes it versus when it does not. A side table does the same
// for every head sign that appears before 125. From the contrasts it records
// four bets with explicit falsifiers: 002 refunctionalizes 390-125 from mixed
// to open, terminalizes 031-000, may license the rare 610-125-032
// construction, and is a valency gate rather than a generic opener. Writes
// focus-pair rows, pair contrasts, the head-before-125 summary, and the bets
// as CSVs plus a summary JSON to data/open_prototype/reports.

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_expand_002_valency_gate_20260531';
const focusPairs = [
  ['390', '125'],
  ['610', '125'],
  ['405', '125'],
  ['861', '125'],
  ['906', '125'],
  ['031', '000'],
  ['031', '032'],
  ['220', '455'],
];

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
    const gatedBy002 = index > 0 && rowSigns[index - 1] === '002';
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
      gated_by_002: gatedBy002 ? 'True' : 'False',
      x_continuing: index + 1 < rowSigns.length - 1 ? 'True' : 'False',
      x_terminal: index + 1 === rowSigns.length - 1 ? 'True' : 'False',
      tail_after_x: rowSigns.slice(index + 2).join(' ') || '<END>',
      scope_cell: `${row.site}|${row.type}|${row.shape}|${row.material}`,
      text: row.text,
    });
  }
}

const focusPairRows = focusPairs.flatMap(([h, x]) => pairRows.filter((row) => row.h === h && row.x === x));

const pairContrasts = focusPairs.map(([h, x]) => {
  const rows = pairRows.filter((row) => row.h === h && row.x === x);
  const gated = rows.filter((row) => row.gated_by_002 === 'True');
  const ungated = rows.filter((row) => row.gated_by_002 === 'False');
  const gatedOpen = gated.filter((row) => row.x_continuing === 'True').length;
  const ungatedOpen = ungated.filter((row) => row.x_continuing === 'True').length;
  return {
    checked_date: '2026-05-31',
    pair: `${h}-${x}`,
    total_rows: String(rows.length),
    gated_rows: String(gated.length),
    gated_open_rate: ratio(gatedOpen, gated.length),
    gated_terminal_rate: ratio(gated.length - gatedOpen, gated.length),
    ungated_rows: String(ungated.length),
    ungated_open_rate: ratio(ungatedOpen, ungated.length),
    ungated_terminal_rate: ratio(ungated.length - ungatedOpen, ungated.length),
    gated_objects: gated.map((row) => row.object).join(';'),
    ungated_objects_sample: ungated.map((row) => row.object).slice(0, 12).join(';'),
    decision:
      gated.length > 0 && ungated.length > 0 && ratio(gatedOpen, gated.length) !== ratio(ungatedOpen, ungated.length)
        ? '002_changes_pair_behavior'
        : gated.length > 0 && ungated.length === 0
          ? '002_only_currently'
          : 'no_clear_gate_effect',
  };
});

const hBefore125Rows = pairRows.filter((row) => row.x === '125');
const hBefore125Summary = countBy(hBefore125Rows, (row) => row.h).map(([h, count]) => {
  const rows = hBefore125Rows.filter((row) => row.h === h);
  const gated = rows.filter((row) => row.gated_by_002 === 'True');
  const open = rows.filter((row) => row.x_continuing === 'True').length;
  return {
    checked_date: '2026-05-31',
    h_before_125: h,
    rows: String(count),
    gated_rows: String(gated.length),
    open_rate: ratio(open, count),
    gated_open_rate: ratio(gated.filter((row) => row.x_continuing === 'True').length, gated.length),
    ungated_open_rate: ratio(rows.filter((row) => row.gated_by_002 === 'False' && row.x_continuing === 'True').length, rows.length - gated.length),
    scopes: topCounts(rows, (row) => row.scope_cell),
    objects: rows.map((row) => row.object).join(';'),
  };
});

const pair390125 = pairContrasts.find((row) => row.pair === '390-125');
const pair031000 = pairContrasts.find((row) => row.pair === '031-000');
const pair610125 = pairContrasts.find((row) => row.pair === '610-125');

const bets = [
  {
    checked_date: '2026-05-31',
    bet_id: 'SIGN002_VALENCY_GATE_NOT_GENERIC_OPENER',
    tier: 'candidate',
    claim:
      '`002` marks a valency frame: it reconditions the following `H-X` pair rather than simply meaning "open" or "continue".',
    support:
      `390-125 gated open=${pair390125?.gated_open_rate} vs ungated open=${pair390125?.ungated_open_rate}; ` +
      `031-000 gated open=${pair031000?.gated_open_rate} vs ungated open=${pair031000?.ungated_open_rate}`,
    falsifier:
      'If source/family collapse makes gated and ungated H-X pairs behave the same, delete the 002 valency-frame role.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'SIGN002_REFUNCTIONALIZES_390125',
    tier: 'candidate',
    claim:
      '`002` refunctionalizes raw `390-125`: after `002`, `390-125` is open; outside `002`, `390-125` is mixed and often terminal.',
    support: `390-125 gated=${pair390125?.gated_open_rate}; ungated=${pair390125?.ungated_open_rate}; gated_objects=${pair390125?.gated_objects}`,
    falsifier:
      'One strict terminal `002-390-125` or source-collapse of ungated terminal `390-125` rows kills the refunctionalization bet.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'SIGN002_TERMINALIZES_031000',
    tier: 'wild shot',
    claim:
      '`002` can terminalize a pair too: `031-000` is terminal when gated by `002`, but usually open without `002`.',
    support: `031-000 gated=${pair031000?.gated_open_rate}; ungated=${pair031000?.ungated_open_rate}`,
    falsifier:
      'A source-visible continuing `002-031-000-Y` row kills this terminalizing branch of the 002 role.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'SIGN002_RARE_HEAD610_CONSTRUCTION',
    tier: 'candidate',
    claim:
      '`610-125-032` is currently only attested inside a `002` frame, so `002` may license the rare head `610` construction.',
    support: `610-125 gated=${pair610125?.gated_rows}; ungated=${pair610125?.ungated_rows}; gated_objects=${pair610125?.gated_objects}`,
    falsifier:
      'A credible ungated `610-125-032`, or a gated `002-610-125` with another tail, breaks this construction bet.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'EXPAND',
  status: 'sign002_valency_gate',
  focus_pairs: Object.fromEntries(pairContrasts.map((row) => [row.pair, row.decision])),
  headline_contrasts: {
    '390-125': {
      gated_open_rate: pair390125?.gated_open_rate,
      ungated_open_rate: pair390125?.ungated_open_rate,
    },
    '031-000': {
      gated_open_rate: pair031000?.gated_open_rate,
      ungated_open_rate: pair031000?.ungated_open_rate,
    },
    '610-125': {
      gated_rows: pair610125?.gated_rows,
      ungated_rows: pair610125?.ungated_rows,
    },
  },
  new_bets: Object.fromEntries(bets.map((row) => [row.bet_id, row.tier])),
  predictions: [
    '`002-390-125` should remain open while ungated `390-125` may terminate.',
    '`002-031-000` should be terminal unless the terminalizing branch is wrong.',
    '`610-125-032` should remain gated by `002` unless rare-head construction is wrong.',
  ],
};

writeCsv(path.join(reportsDir, `${prefix}_focus_pair_rows.csv`), focusPairRows, [
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

writeCsv(path.join(reportsDir, `${prefix}_pair_contrasts.csv`), pairContrasts, [
  'checked_date',
  'pair',
  'total_rows',
  'gated_rows',
  'gated_open_rate',
  'gated_terminal_rate',
  'ungated_rows',
  'ungated_open_rate',
  'ungated_terminal_rate',
  'gated_objects',
  'ungated_objects_sample',
  'decision',
]);

writeCsv(path.join(reportsDir, `${prefix}_h_before_125_summary.csv`), hBefore125Summary, [
  'checked_date',
  'h_before_125',
  'rows',
  'gated_rows',
  'open_rate',
  'gated_open_rate',
  'ungated_open_rate',
  'scopes',
  'objects',
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
