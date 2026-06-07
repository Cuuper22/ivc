import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_open_operator_tail_complements_20260531';
const checkedDate = '2026-05-31';
const openOperators = new Set(['125', '455', '530', '003', '861', '065', '035', '906', '460', '090']);
const focusOpenOperators = new Set(['125', '530', '861']);

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

function counts(values) {
  const map = new Map();
  for (const value of values) map.set(value, (map.get(value) ?? 0) + 1);
  return map;
}

function tally(values) {
  return [...counts(values).entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([value, count]) => `${value}:${count}`)
    .join(';');
}

function topShare(values) {
  if (!values.length) return 0;
  return Math.max(...counts(values).values()) / values.length;
}

function entropy(values) {
  if (!values.length) return 0;
  const map = counts(values);
  let total = 0;
  for (const count of map.values()) {
    const p = count / values.length;
    total -= p * Math.log2(p);
  }
  return total;
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));

const xOpenRows = [];
const globalRows = [];

for (const row of rows) {
  for (let i = 0; i < row.signs.length; i += 1) {
    const sign = row.signs[i];
    if (openOperators.has(sign)) {
      globalRows.push({
        checked_date: checkedDate,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        sign,
        next1: row.signs[i + 1] ?? '<END>',
        terminal: i === row.signs.length - 1,
        in_x_slot: i >= 2 && row.signs[i - 2] === '002',
        text: row.text,
      });
    }
  }

  for (let i = 0; i < row.signs.length - 2; i += 1) {
    if (row.signs[i] !== '002') continue;
    const head = row.signs[i + 1];
    const x = row.signs[i + 2];
    if (!openOperators.has(x)) continue;
    xOpenRows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      head,
      x,
      next1: row.signs[i + 3] ?? '<END>',
      terminal: i + 2 === row.signs.length - 1,
      tail: row.signs.slice(i + 3).join('-') || '<END>',
      focus: focusOpenOperators.has(x),
      text: row.text,
    });
  }
}

const operatorRows = [...new Set(xOpenRows.map((row) => row.x))]
  .map((x) => {
    const local = xOpenRows.filter((row) => row.x === x);
    const global = globalRows.filter((row) => row.sign === x);
    const localNonterminal = local.filter((row) => !row.terminal);
    const globalNonterminal = global.filter((row) => !row.terminal);
    const repeatedLocalComplements = [...counts(localNonterminal.map((row) => row.next1)).entries()]
      .filter(([, count]) => count >= 2)
      .map(([sign, count]) => `${sign}:${count}`)
      .join(';');
    return {
      checked_date: checkedDate,
      x,
      focus: focusOpenOperators.has(x),
      x_slot_occurrences: local.length,
      x_slot_nonterminal: localNonterminal.length,
      x_slot_next1: tally(localNonterminal.map((row) => row.next1)),
      x_slot_top_next_share: topShare(localNonterminal.map((row) => row.next1)).toFixed(3),
      x_slot_tail_entropy: entropy(localNonterminal.map((row) => row.tail)).toFixed(3),
      repeated_local_complements: repeatedLocalComplements || '',
      global_occurrences: global.length,
      global_nonterminal: globalNonterminal.length,
      global_next1: tally(globalNonterminal.map((row) => row.next1)),
      global_top_next_share: topShare(globalNonterminal.map((row) => row.next1)).toFixed(3),
      heads: tally(local.map((row) => row.head)),
      sites: tally(local.map((row) => row.site)),
      types: tally(local.map((row) => row.type)),
      objects: local.map((row) => row.object).slice(0, 16).join(';'),
      provisional_role:
        localNonterminal.length >= 3 && repeatedLocalComplements
          ? 'linker_with_repeated_complements'
          : localNonterminal.length >= 3
            ? 'open_but_tail_residue_risk'
            : 'underpowered_open_operator',
    };
  })
  .sort((a, b) => Number(b.x_slot_occurrences) - Number(a.x_slot_occurrences) || a.x.localeCompare(b.x));

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_125_COMPLEMENT_LINKER',
    tier: 'candidate',
    claim:
      'X=125 is a linker/valency operator whose complements include repeated 632/032/820 tails.',
    risky_prediction:
      '125 should show recurrent next signs in X slot, not random one-off continuations.',
    kill_condition:
      '125 tails collapse to one site/source formula or become random under source filtering.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_530_OPEN_BUT_UNRESOLVED',
    tier: 'wild shot',
    claim:
      'X=530 is an open operator, but its complement class is not identified yet.',
    risky_prediction:
      'More 530 rows should appear with nonterminal tails; at least one tail should repeat in wider/held-out data.',
    kill_condition:
      '530 remains a handful of unrelated singleton continuations.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_861_PAYLOAD_OPERATOR',
    tier: 'wild shot',
    claim:
      'X=861 is not terminal-class 861; inside X it behaves as payload/open operator.',
    risky_prediction:
      'X-slot 861 should continue more often than global 861 and align with open-operator tails.',
    kill_condition:
      'X-slot 861 rows are damaged/source-weak or collapse into unrelated formulas.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'open_operator_tail_complements',
  focus: Object.fromEntries(
    operatorRows
      .filter((row) => focusOpenOperators.has(row.x))
      .map((row) => [
        row.x,
        {
          x_slot_occurrences: Number(row.x_slot_occurrences),
          x_slot_next1: row.x_slot_next1,
          repeated_local_complements: row.repeated_local_complements,
          provisional_role: row.provisional_role,
        },
      ]),
  ),
  strongest_new_parse_bet:
    '125 is the first open X operator with repeated governed-complement candidates.',
};

writeCsv(path.join(reportsDir, `${prefix}_operator_rows.csv`), operatorRows, [
  'checked_date',
  'x',
  'focus',
  'x_slot_occurrences',
  'x_slot_nonterminal',
  'x_slot_next1',
  'x_slot_top_next_share',
  'x_slot_tail_entropy',
  'repeated_local_complements',
  'global_occurrences',
  'global_nonterminal',
  'global_next1',
  'global_top_next_share',
  'heads',
  'sites',
  'types',
  'objects',
  'provisional_role',
]);
writeCsv(path.join(reportsDir, `${prefix}_x_occurrences.csv`), xOpenRows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'head',
  'x',
  'next1',
  'terminal',
  'tail',
  'focus',
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
