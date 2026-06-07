import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const checkedDate = '2026-05-31';
const prefix = 'campaign_032_002_861_002390x_expand_operator_tail_discriminator_20260531';

const terminalBoosters = new Set([
  '000',
  '031',
  '416',
  '575',
  '317',
  '705',
  '741',
  '491',
  '095',
  '260',
  '820',
  '140',
  '165',
  '603',
]);
const openOperators = new Set(['125', '455', '530', '003', '861', '065', '035', '906', '460', '090']);

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
  for (const row of rows) lines.push(fields.map((fieldName) => csvEscape(row[fieldName])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function tokens(text) {
  return text.match(/\d{3}/g) ?? [];
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function polarity(x) {
  if (terminalBoosters.has(x)) return 'terminal_booster';
  if (openOperators.has(x)) return 'open_operator';
  return 'other';
}

function tally(values) {
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([value, count]) => `${value}:${count}`)
    .join(';');
}

function topCount(values) {
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  const sorted = [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  return sorted[0] ?? ['', 0];
}

function repeatShare(values) {
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  const repeated = [...counts.values()].filter((count) => count > 1).reduce((sum, count) => sum + count, 0);
  return values.length ? repeated / values.length : 0;
}

function groupRows(rows, keyFn) {
  const groups = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(row);
  }
  return groups;
}

function groupMetricRows(rows, keyName, keyFn) {
  return [...groupRows(rows, keyFn).entries()]
    .map(([key, group]) => {
      const tailFirsts = group.map((row) => row.tail_first);
      const [topTail, topTailRows] = topCount(tailFirsts);
      return {
        checked_date: checkedDate,
        group_type: keyName,
        group_key: key,
        rows: group.length,
        nonterminal_rows: group.filter((row) => row.tail_first !== '<END>').length,
        repeated_tail_first_share: repeatShare(tailFirsts).toFixed(3),
        dominant_tail_first: topTail,
        dominant_tail_first_rows: topTailRows,
        tail_first_inventory: tally(tailFirsts),
        heads: tally(group.map((row) => row.head)),
        xs: tally(group.map((row) => row.x)),
        contexts: tally(group.map((row) => row.context_cell)),
      };
    })
    .sort((a, b) => b.rows - a.rows || a.group_key.localeCompare(b.group_key));
}

fs.mkdirSync(reportsDir, { recursive: true });

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));

const frameRows = [];
for (const row of metadataRows) {
  for (let i = 0; i < row.signs.length - 2; i += 1) {
    if (row.signs[i] !== '002') continue;
    const head = row.signs[i + 1];
    const x = row.signs[i + 2];
    const tail = row.signs.slice(i + 3);
    const xPolarity = polarity(x);
    if (xPolarity === 'other') continue;
    frameRows.push({
      checked_date: checkedDate,
      object: row.object,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      cult: row.cult,
      class: row.class,
      head,
      x,
      x_polarity: xPolarity,
      terminal: tail.length === 0,
      tail_first: tail[0] ?? '<END>',
      tail_pair: tail.slice(0, 2).join(' ') || '<END>',
      tail_len: tail.length,
      context_cell: `${row.site}|${row.type}|${row.shape}|${row.material}|${row.cult}|${row.class}`,
      text: row.text,
    });
  }
}

const openRows = frameRows.filter((row) => row.x_polarity === 'open_operator');
const terminalRows = frameRows.filter((row) => row.x_polarity === 'terminal_booster');
const openNonterminalRows = openRows.filter((row) => row.tail_first !== '<END>');

const byXRows = groupMetricRows(openRows, 'open_operator_x', (row) => row.x);
const byHeadRows = groupMetricRows(openRows, 'head', (row) => row.head);
const byContextRows = groupMetricRows(openRows, 'context_cell', (row) => row.context_cell);

const openXRepeatMean =
  byXRows.filter((row) => row.rows >= 2).reduce((sum, row) => sum + Number(row.repeated_tail_first_share), 0) /
  Math.max(1, byXRows.filter((row) => row.rows >= 2).length);
const contextRepeatMean =
  byContextRows.filter((row) => row.rows >= 2).reduce((sum, row) => sum + Number(row.repeated_tail_first_share), 0) /
  Math.max(1, byContextRows.filter((row) => row.rows >= 2).length);

const discriminatorRows = [
  {
    checked_date: checkedDate,
    discriminator: 'open_operator_tail_recurrence',
    observed: `open rows ${openRows.length}; nonterminal ${openNonterminalRows.length}; by-X repeat mean ${openXRepeatMean.toFixed(3)}; by-context repeat mean ${contextRepeatMean.toFixed(3)}`,
    favors:
      openXRepeatMean > contextRepeatMean
        ? 'head_final_linker_model'
        : openXRepeatMean < contextRepeatMean
          ? 'visual_context_formula_null'
          : 'undecided',
    risk: 'Repeat means are crude and not source-strict; use only as expansion pressure.',
  },
  {
    checked_date: checkedDate,
    discriminator: 'terminal_booster_closure',
    observed: `terminal booster rows ${terminalRows.length}; closed ${terminalRows.filter((row) => row.terminal).length}`,
    favors: terminalRows.filter((row) => row.terminal).length > openRows.filter((row) => row.terminal).length ? 'polarity_model' : 'undecided',
    risk: 'Terminal booster set was chosen from observed behavior; must survive held-out rows.',
  },
];

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_OPEN_TAIL_OPERATOR_CLASS',
    tier: openXRepeatMean > contextRepeatMean ? 'candidate' : 'wild shot',
    risky_bet: 'Open-operator tails are governed more by X/operator class than by object context.',
    reason: discriminatorRows[0].observed,
    prediction: 'Future source-strict open rows should repeat tail classes within X groups more than within site/type/cult context groups.',
    kill_condition: 'Context cells beat X groups after source-strict filtering.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_125_ASSOCIATIVE_LINKER',
    tier: 'candidate structure, wild semantics',
    risky_bet: '`125` is an associative/genitive-like linker, not just a terminal sign.',
    reason: byXRows.find((row) => row.group_key === '125')?.tail_first_inventory ?? 'no 125 rows',
    prediction: '`125` should keep taking formulaic nominal tails across heads, while terminal exceptions cluster under different heads/registers.',
    kill_condition: '`125` tails become random or context-owned under source-strict rows.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_455_065_RELATION_OPERATORS',
    tier: 'wild shot',
    risky_bet: '`455` and `065` are relation/payload operators selected by the open-template head `220`.',
    reason: `455 tails=${byXRows.find((row) => row.group_key === '455')?.tail_first_inventory ?? ''}; 065 tails=${byXRows.find((row) => row.group_key === '065')?.tail_first_inventory ?? ''}`,
    prediction: '`455/065` should stay open under `220` and resist terminal-default head contexts.',
    kill_condition: '`455/065` close freely or their tails collapse to one visual formula.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'operator_tail_discriminator',
  open_rows: openRows.length,
  terminal_booster_rows: terminalRows.length,
  open_x_repeat_mean: openXRepeatMean.toFixed(3),
  context_repeat_mean: contextRepeatMean.toFixed(3),
  discriminator:
    openXRepeatMean > contextRepeatMean
      ? 'weakly_favors_operator_tail_model'
      : openXRepeatMean < contextRepeatMean
        ? 'weakly_favors_context_formula_null'
        : 'undecided',
  new_bets: betRows.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

writeCsv(path.join(reportsDir, `${prefix}_open_rows.csv`), openRows, [
  'checked_date',
  'object',
  'site',
  'type',
  'shape',
  'material',
  'cult',
  'class',
  'head',
  'x',
  'x_polarity',
  'terminal',
  'tail_first',
  'tail_pair',
  'tail_len',
  'context_cell',
  'text',
]);
writeCsv(path.join(reportsDir, `${prefix}_by_x.csv`), byXRows, [
  'checked_date',
  'group_type',
  'group_key',
  'rows',
  'nonterminal_rows',
  'repeated_tail_first_share',
  'dominant_tail_first',
  'dominant_tail_first_rows',
  'tail_first_inventory',
  'heads',
  'xs',
  'contexts',
]);
writeCsv(path.join(reportsDir, `${prefix}_by_context.csv`), byContextRows, [
  'checked_date',
  'group_type',
  'group_key',
  'rows',
  'nonterminal_rows',
  'repeated_tail_first_share',
  'dominant_tail_first',
  'dominant_tail_first_rows',
  'tail_first_inventory',
  'heads',
  'xs',
  'contexts',
]);
writeCsv(path.join(reportsDir, `${prefix}_discriminators.csv`), discriminatorRows, [
  'checked_date',
  'discriminator',
  'observed',
  'favors',
  'risk',
]);
writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), betRows, [
  'checked_date',
  'bet_id',
  'tier',
  'risky_bet',
  'reason',
  'prediction',
  'kill_condition',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
