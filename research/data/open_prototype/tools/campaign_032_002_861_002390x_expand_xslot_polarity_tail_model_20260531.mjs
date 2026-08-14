import fs from 'node:fs';
import path from 'node:path';

// This script builds a polarity model of the X slot: every X sign in the Indus 002-H-X
// construction either pushes the inscription shut or holds it open. It reads
// data/open_prototype/lipi/metadata_filtered.csv, computes each sign's global terminal rate
// as a baseline, then classifies every X sign with at least 3 occurrences into one of four
// polarity classes — terminal_booster (closes far more inside the frame than outside),
// open_operator (usually continues), global_edge (terminal everywhere, so the frame adds
// nothing), or mixed. For open signs it also measures the Shannon entropy of their tails:
// low entropy means the continuations repeat, which looks like grammar; high entropy looks
// like noise. Class-level rows then map polarity to rough roles (closure classifier,
// valency/linker operator, borrowed edge sign), and three bets stake the model, with 095/705
// as classifier candidates and 530/125 as linkers. Writes per-sign, per-class, occurrence,
// and bets CSVs plus a summary JSON to reports/.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_xslot_polarity_tail_model_20260531';
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

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function tokens(text) {
  return text.match(/\d{3}/g) ?? [];
}

function tally(values) {
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([value, count]) => `${value}:${count}`)
    .join(';');
}

function uniqueCount(values) {
  return new Set(values).size;
}

function entropy(values) {
  if (!values.length) return 0;
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  let total = 0;
  for (const count of counts.values()) {
    const p = count / values.length;
    total -= p * Math.log2(p);
  }
  return total;
}

function polarity(terminalRate, globalTerminalRate, count) {
  const delta = terminalRate - globalTerminalRate;
  if (count < 3) return 'underpowered';
  if (terminalRate >= 0.75 && delta >= 0.2) return 'terminal_booster';
  if (terminalRate <= 0.35 || delta <= -0.2) return 'open_operator';
  if (terminalRate >= 0.6 && Math.abs(delta) < 0.15) return 'global_edge';
  return 'mixed';
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));

const global = new Map();
const xRows = [];

for (const row of rows) {
  for (let i = 0; i < row.signs.length; i += 1) {
    const sign = row.signs[i];
    const stat = global.get(sign) ?? { count: 0, terminal: 0 };
    stat.count += 1;
    if (i === row.signs.length - 1) stat.terminal += 1;
    global.set(sign, stat);
  }
}

for (const row of rows) {
  for (let i = 0; i < row.signs.length - 2; i += 1) {
    if (row.signs[i] !== '002') continue;
    xRows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      head: row.signs[i + 1],
      x: row.signs[i + 2],
      terminal: i + 2 === row.signs.length - 1,
      next1: row.signs[i + 3] ?? '<END>',
      tail: row.signs.slice(i + 3).join('-') || '<END>',
      text: row.text,
    });
  }
}

const byX = new Map();
for (const row of xRows) {
  const stat = byX.get(row.x) ?? {
    x: row.x,
    rows: [],
  };
  stat.rows.push(row);
  byX.set(row.x, stat);
}

const polarityRows = [...byX.values()]
  .map((stat) => {
    const g = global.get(stat.x);
    const count = stat.rows.length;
    const terminal = stat.rows.filter((row) => row.terminal).length;
    const terminalRate = terminal / count;
    const globalTerminalRate = g.terminal / g.count;
    const nonterminalRows = stat.rows.filter((row) => !row.terminal);
    const p = polarity(terminalRate, globalTerminalRate, count);
    return {
      checked_date: checkedDate,
      x: stat.x,
      polarity: p,
      x_count: count,
      x_terminal_rate: terminalRate.toFixed(3),
      global_terminal_rate: globalTerminalRate.toFixed(3),
      terminal_delta: (terminalRate - globalTerminalRate).toFixed(3),
      nonterminal_count: nonterminalRows.length,
      nonterminal_next1: tally(nonterminalRows.map((row) => row.next1)),
      nonterminal_tail_entropy: entropy(nonterminalRows.map((row) => row.tail)).toFixed(3),
      unique_heads: uniqueCount(stat.rows.map((row) => row.head)),
      heads: tally(stat.rows.map((row) => row.head)),
      sites: tally(stat.rows.map((row) => row.site)),
      types: tally(stat.rows.map((row) => row.type)),
      sample_objects: stat.rows.map((row) => row.object).slice(0, 12).join(';'),
    };
  })
  .filter((row) => Number(row.x_count) >= 3)
  .sort((a, b) => a.polarity.localeCompare(b.polarity) || Number(b.x_count) - Number(a.x_count));

const classRows = ['terminal_booster', 'open_operator', 'global_edge', 'mixed'].map((klass) => {
  const members = polarityRows.filter((row) => row.polarity === klass);
  const occurrences = members.reduce((sum, row) => sum + Number(row.x_count), 0);
  const nonterminal = members.reduce((sum, row) => sum + Number(row.nonterminal_count), 0);
  return {
    checked_date: checkedDate,
    polarity: klass,
    members: members.map((row) => row.x).join(';'),
    member_count: members.length,
    x_occurrences: occurrences,
    nonterminal_count: nonterminal,
    median_tail_entropy:
      members.length === 0
        ? '0.000'
        : members
            .map((row) => Number(row.nonterminal_tail_entropy))
            .sort((a, b) => a - b)[Math.floor(members.length / 2)]
            .toFixed(3),
    rough_role:
      klass === 'terminal_booster'
        ? 'closure/classifier operator'
        : klass === 'open_operator'
          ? 'valency/linker/payload operator'
          : klass === 'global_edge'
            ? 'borrowed edge sign'
            : 'unresolved mixed operator',
  };
});

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_X_POLARITY_GRAMMAR',
    tier: 'candidate',
    claim:
      '002-H-X has polarity: terminal boosters close the frame, open operators license a following tail.',
    risky_prediction:
      'Terminal_booster rows should have tiny nonterminal tails; open_operator rows should have recurrent next signs instead of random continuation.',
    kill_condition:
      'Polarity classes do not separate tail behavior, or open operators have no repeated next-tail structure.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_705_095_CLASSIFIERS',
    tier: 'wild shot',
    claim:
      '095 and 705 are better candidates than 000 for overt terminal classifiers in the frame.',
    risky_prediction:
      '095/705 stay terminal-boosted after source filtering and do not collapse into one-site copying.',
    kill_condition:
      'Source-visible rows show 095/705 are damaged, repeated visual formula, or ordinary terminal edge signs.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_530_125_VALENCY',
    tier: 'wild shot',
    claim:
      '530 and 125 are open/linker operators, not terminal names.',
    risky_prediction:
      'Their following tails should be recurrent and interpretable as governed complements.',
    kill_condition:
      'Their tails are unrelated object-specific residue with no repeated next-tail behavior.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'xslot_polarity_tail_model',
  polarity_classes: Object.fromEntries(classRows.map((row) => [row.polarity, row.members])),
  strongest_new_parse_bet:
    'X slot has polarity: terminal boosters 000/095/705 versus open operators 125/530/861.',
  immediate_risk:
    'Terminal_booster set may collapse under source filtering; open_operator tails may be formula residue rather than valency.',
};

writeCsv(path.join(reportsDir, `${prefix}_polarity_rows.csv`), polarityRows, [
  'checked_date',
  'x',
  'polarity',
  'x_count',
  'x_terminal_rate',
  'global_terminal_rate',
  'terminal_delta',
  'nonterminal_count',
  'nonterminal_next1',
  'nonterminal_tail_entropy',
  'unique_heads',
  'heads',
  'sites',
  'types',
  'sample_objects',
]);
writeCsv(path.join(reportsDir, `${prefix}_class_rows.csv`), classRows, [
  'checked_date',
  'polarity',
  'members',
  'member_count',
  'x_occurrences',
  'nonterminal_count',
  'median_tail_entropy',
  'rough_role',
]);
writeCsv(path.join(reportsDir, `${prefix}_occurrences.csv`), xRows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'head',
  'x',
  'terminal',
  'next1',
  'tail',
  'text',
]);
writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), betRows, [
  'checked_date',
  'bet_id',
  'tier',
  'claim',
  'risky_prediction',
  'kill_condition',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
