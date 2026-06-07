import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_expand_x125_scope_split_20260531';

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
const frames = [];
for (const row of metadataRows) {
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
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      symbol: row.symbol,
      cult: row.cult,
      prev_before_002: rowSigns[index - 1] ?? '',
      head_after_002: head,
      x_after_head: x,
      x_is_125: x === '125' ? 'True' : 'False',
      x_continuing: takesX && index + 2 < rowSigns.length - 1 ? 'True' : 'False',
      x_terminal: takesX && index + 2 === rowSigns.length - 1 ? 'True' : 'False',
      tail_after_x: takesX ? rowSigns.slice(index + 3).join(' ') || '<END>' : '<NONE>',
      scope_cell: `${row.site}|${row.type}|${row.shape}|${row.material}`,
      text: row.text,
    });
  }
}

const x125Rows = frames.filter((row) => row.x_after_head === '125');
const x125Open = x125Rows.filter((row) => row.x_continuing === 'True');
const x125Terminal = x125Rows.filter((row) => row.x_terminal === 'True');

const scopeSummary = countBy(x125Rows, (row) => row.scope_cell).map(([scope, count]) => {
  const rows = x125Rows.filter((row) => row.scope_cell === scope);
  const open = rows.filter((row) => row.x_continuing === 'True').length;
  const terminal = rows.filter((row) => row.x_terminal === 'True').length;
  return {
    checked_date: '2026-05-31',
    scope_cell: scope,
    rows: String(count),
    open: String(open),
    open_rate: ratio(open, count),
    terminal: String(terminal),
    terminal_rate: ratio(terminal, count),
    heads: topCounts(rows, (row) => row.head_after_002),
    objects: rows.map((row) => row.object).join(';'),
    decision:
      open === count
        ? 'open_scope'
        : terminal === count
          ? 'terminal_scope'
          : 'mixed_scope',
  };
});

const headSummary = countBy(x125Rows, (row) => row.head_after_002).map(([head, count]) => {
  const rows = x125Rows.filter((row) => row.head_after_002 === head);
  const open = rows.filter((row) => row.x_continuing === 'True').length;
  const terminal = rows.filter((row) => row.x_terminal === 'True').length;
  return {
    checked_date: '2026-05-31',
    head,
    rows: String(count),
    open: String(open),
    open_rate: ratio(open, count),
    terminal: String(terminal),
    terminal_rate: ratio(terminal, count),
    scopes: topCounts(rows, (row) => row.scope_cell),
    objects: rows.map((row) => row.object).join(';'),
    decision:
      open === count
        ? 'x125_open_under_this_head'
        : terminal === count
          ? 'x125_terminal_under_this_head'
          : 'x125_mixed_under_this_head',
  };
});

const bets = [
  {
    checked_date: '2026-05-31',
    bet_id: 'X125_UNIVERSAL_SWITCH_KILLED',
    tier: 'killed',
    claim:
      'Universal `002-H-125 -> continuation` across the current filtered corpus is false.',
    support: `global X=125 continuing=${ratio(x125Open.length, x125Rows.length)}; terminal exceptions=${x125Terminal.map((row) => `${row.object}:${row.head_after_002}`).join(';')}`,
    prediction:
      'Do not use X=125 as script-wide sufficiency; use it only inside a scoped/head-conditioned parser.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'X125_HEAD_CONDITIONED_SWITCH',
    tier: 'candidate',
    claim:
      '`125` is a head-conditioned X-slot switch: open under heads `190/390/405/407/610`, terminal under `861/906` in current data.',
    support: `open heads=${topCounts(x125Open, (row) => row.head_after_002)}; terminal heads=${topCounts(x125Terminal, (row) => row.head_after_002)}`,
    prediction:
      'Future `002-390-125`, `002-405-125`, or `002-610-125` rows should continue; future `002-861-125` rows should terminate unless head class is wrong.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'X125_SCOPE_SPLIT_SITE_REGISTER',
    tier: 'wild shot',
    claim:
      'The X=125 switch has a register/site split: Mohenjo-daro square SEAL:S preserves open X=125, while Harappa square SEAL:S and Mohenjo-daro cuboid-convex SEAL:R provide terminal pressure.',
    support: `scopes=${scopeSummary.map((row) => `${row.scope_cell}:${row.open_rate}`).join(' | ')}`,
    prediction:
      'A new Harappa square seal `002-H-125` should be suspicious for terminal behavior; a new Mohenjo-daro square seal `002-H-125` should continue unless the local rule dies.',
  },
  {
    checked_date: '2026-05-31',
    bet_id: 'X125_TAIL_CLASS_BY_HEAD',
    tier: 'wild shot',
    claim:
      'Open X=125 tails are head-conditioned dependent tails, not translations: `390` prefers `632-032`/`195`, `405` gives `820`, `610` gives `032`, `407` gives a copper-tablet tail.',
    support: `open X=125 rows=${x125Open.map((row) => `${row.object}:${row.head_after_002}->${row.tail_after_x}`).join(';')}`,
    prediction:
      'If tails do not cluster by head or register after source collapse, keep only head-conditioned continuation and kill tail-class morphology.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'EXPAND',
  status: 'x125_scope_split',
  global_x125: {
    rows: x125Rows.length,
    continuing_rate: ratio(x125Open.length, x125Rows.length),
    terminal_rate: ratio(x125Terminal.length, x125Rows.length),
    open_heads: topCounts(x125Open, (row) => row.head_after_002),
    terminal_heads: topCounts(x125Terminal, (row) => row.head_after_002),
  },
  scope_summary: scopeSummary,
  new_bets: Object.fromEntries(bets.map((row) => [row.bet_id, row.tier])),
  predictions: [
    'Same-register Mohenjo-daro square seal `002-H-125` should continue.',
    'Universal X=125 sufficiency is dead unless terminal exceptions are source/corpus errors.',
    'Head-conditioned switch survives if future 861/906 terminal and 190/390/405/407/610 open behavior repeats.',
  ],
};

writeCsv(path.join(reportsDir, `${prefix}_x125_global_rows.csv`), x125Rows, [
  'checked_date',
  'object',
  'id',
  'site',
  'type',
  'shape',
  'material',
  'symbol',
  'cult',
  'prev_before_002',
  'head_after_002',
  'x_after_head',
  'x_is_125',
  'x_continuing',
  'x_terminal',
  'tail_after_x',
  'scope_cell',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_scope_summary.csv`), scopeSummary, [
  'checked_date',
  'scope_cell',
  'rows',
  'open',
  'open_rate',
  'terminal',
  'terminal_rate',
  'heads',
  'objects',
  'decision',
]);

writeCsv(path.join(reportsDir, `${prefix}_head_summary.csv`), headSummary, [
  'checked_date',
  'head',
  'rows',
  'open',
  'open_rate',
  'terminal',
  'terminal_rate',
  'scopes',
  'objects',
  'decision',
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
