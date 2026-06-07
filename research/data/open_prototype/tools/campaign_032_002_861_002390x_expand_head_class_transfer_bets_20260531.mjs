import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const checkedDate = '2026-05-31';
const prefix = 'campaign_032_002_861_002390x_expand_head_class_transfer_bets_20260531';

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
const globalEdges = new Set(['501', '091', '692']);
const focusHeads = ['390', '861', '000', '220', '405', '031', '820', '056', '920', '368'];

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
  if (globalEdges.has(x)) return 'global_edge';
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

function rate(count, total) {
  return total ? count / total : 0;
}

function pct(count, total) {
  return total ? `${count}/${total}` : '0/0';
}

function headBetClass(metrics) {
  if (metrics.rows < 5) return 'underpowered';
  if (metrics.open_operator_rows >= 5 && metrics.terminal_booster_rows <= 2) return 'open_template_head';
  if (metrics.terminal_booster_rows >= 5 && metrics.open_operator_rows <= 2) return 'terminal_default_head';
  if (metrics.terminal_booster_rows >= 2 && metrics.open_operator_rows >= 2) return 'mixed_inventory_head';
  if (metrics.global_edge_rows >= 5) return 'closed_edge_template_head';
  return 'unresolved_head';
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
    if (!focusHeads.includes(head)) continue;
    const tail = row.signs.slice(i + 3);
    frameRows.push({
      checked_date: checkedDate,
      object: row.object,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      head,
      x,
      x_polarity: polarity(x),
      terminal: tail.length === 0,
      tail: tail.join(' ') || '<END>',
      text: row.text,
    });
  }
}

const metricRows = focusHeads
  .map((head) => {
    const rows = frameRows.filter((row) => row.head === head);
    const terminalRows = rows.filter((row) => row.terminal);
    const terminalBoosterRows = rows.filter((row) => row.x_polarity === 'terminal_booster');
    const openOperatorRows = rows.filter((row) => row.x_polarity === 'open_operator');
    const globalEdgeRows = rows.filter((row) => row.x_polarity === 'global_edge');
    const recognizedRows = rows.filter((row) => row.x_polarity !== 'other');
    const terminalBoostClosed = terminalBoosterRows.filter((row) => row.terminal).length;
    const openOperatorsContinue = openOperatorRows.filter((row) => !row.terminal).length;
    const metrics = {
      checked_date: checkedDate,
      head,
      rows: rows.length,
      terminal_rows: terminalRows.length,
      terminal_rate: rate(terminalRows.length, rows.length).toFixed(3),
      recognized_x_rows: recognizedRows.length,
      terminal_booster_rows: terminalBoosterRows.length,
      terminal_booster_close_rate: pct(terminalBoostClosed, terminalBoosterRows.length),
      open_operator_rows: openOperatorRows.length,
      open_operator_continue_rate: pct(openOperatorsContinue, openOperatorRows.length),
      global_edge_rows: globalEdgeRows.length,
      unique_x: new Set(rows.map((row) => row.x)).size,
      top_x: tally(rows.map((row) => row.x)),
      x_polarities: tally(rows.map((row) => row.x_polarity)),
      sites: tally(rows.map((row) => row.site)),
    };
    return {
      ...metrics,
      expanded_head_bet_class: headBetClass(metrics),
    };
  })
  .filter((row) => row.rows > 0);

const byHead = new Map(metricRows.map((row) => [row.head, row]));

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_TRANSFER_002_H_X_GRAMMAR',
    tier: 'candidate',
    risky_bet: '`002-H-X` is a transferable frame grammar, not a `390` island.',
    reason: 'Multiple heads carry reusable X polarity classes: 390/000/368 are mixed, 220 is open-template, 405/056 are closed-edge/template-like, and 031/861/920 are terminal-default in this pass.',
    prediction: 'Held-out source-visible `002-H-X` rows should preserve head-class behavior better than a 390-only parser.',
    kill_condition: 'Sibling heads fail to preserve terminal/open behavior once source/site/type controls are strict.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_390_AS_MIXED_INVENTORY_NOT_TITLE',
    tier: 'candidate structure, wild shot semantics',
    risky_bet: '`390` is a mixed inventory head; any status/title reading is only a wild semantic gloss.',
    reason: `390 metrics: rows=${byHead.get('390')?.rows}; class=${byHead.get('390')?.expanded_head_bet_class}; top_x=${byHead.get('390')?.top_x}`,
    prediction: '`390` should pattern closer to mixed heads `000` and `368` than to terminal-default heads `031/861/920` or closed-edge head `405`.',
    kill_condition: '`390` separates cleanly from mixed heads under held-out/source-strict X behavior.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_220_OPEN_RELATION_HEAD',
    tier: 'wild shot',
    risky_bet: '`220` is an open relation/route head in the 002 frame.',
    reason: `220 metrics: open operators=${byHead.get('220')?.open_operator_rows}; top_x=${byHead.get('220')?.top_x}`,
    prediction: 'Future `002-220-455/065/...` rows should continue into payload tails more often than they close.',
    kill_condition: 'Source-strict `002-220-X` rows close at terminal-default rates or open tails are only one copied formula.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_TERMINAL_DEFAULT_HEADS_CLASSIFIER_ZONE',
    tier: 'wild shot',
    risky_bet: '`031`, `861`, and `920` are terminal-default classifier-zone heads, not open relation heads.',
    reason: `031=${byHead.get('031')?.expanded_head_bet_class};861=${byHead.get('861')?.expanded_head_bet_class};920=${byHead.get('920')?.expanded_head_bet_class};820=${byHead.get('820')?.expanded_head_bet_class}`,
    prediction: 'Their repeated X signs should close unless an open operator is visibly embedded or damaged.',
    kill_condition: 'New rows show these heads carrying productive open tails across sites/registers.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_CLOSED_EDGE_TEMPLATE_HEADS',
    tier: 'wild shot',
    risky_bet: '`405` and `056` are closed edge-template heads that select fixed terminal caps.',
    reason: `405 top_x=${byHead.get('405')?.top_x}; 056 top_x=${byHead.get('056')?.top_x}`,
    prediction: 'If a future `002-405-X` or `002-056-X` row continues, it should be treated as a destructive exception first, not normal variation.',
    kill_condition: 'Any source-strict productive continuation after 405/056.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_HEAD_FINAL_LINKER_DISCRIMINATOR',
    tier: 'wild shot',
    risky_bet: 'The parser is closer to a head-final linker/classifier grammar than to pure copied visual formulae.',
    reason: 'Open operators continue after the head while terminal boosters close; this is a syntactic directionality bet, not a reading.',
    prediction: 'Open-operator tails should recur by operator class across heads; pure visual-copy null should collapse them by object type/left picture instead.',
    kill_condition: 'Tail classes follow animal/register/source clusters better than head and X polarity.',
  },
];

const predictionRows = [
  {
    checked_date: checkedDate,
    target: 'held_out_mixed_heads',
    prediction: '`000` and `368` should preserve mixed terminal/open X behavior under source-strict checks.',
    relevant_bets: 'EXPAND_TRANSFER_002_H_X_GRAMMAR;EXPAND_390_AS_MIXED_INVENTORY_NOT_TITLE',
  },
  {
    checked_date: checkedDate,
    target: 'held_out_open_head_220',
    prediction: '`002-220-455/065` rows should continue, not close, unless a source defect intervenes.',
    relevant_bets: 'EXPAND_220_OPEN_RELATION_HEAD',
  },
  {
    checked_date: checkedDate,
    target: 'terminal_default_heads',
    prediction: '`002-031-X`, `002-861-X`, and `002-920-X` should prefer terminal/default caps over open tails.',
    relevant_bets: 'EXPAND_TERMINAL_DEFAULT_HEADS_CLASSIFIER_ZONE',
  },
  {
    checked_date: checkedDate,
    target: 'closed_edge_heads',
    prediction: '`002-405-X` and `002-056-X` should behave like closed templates.',
    relevant_bets: 'EXPAND_CLOSED_EDGE_TEMPLATE_HEADS',
  },
  {
    checked_date: checkedDate,
    target: 'visual_formula_null',
    prediction: 'If visual copying is primary, head/X polarity should lose to site/register/animal controls.',
    relevant_bets: 'EXPAND_HEAD_FINAL_LINKER_DISCRIMINATOR',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'head_class_transfer_bets',
  head_rows: metricRows.length,
  new_bets: betRows.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
  strongest_risky_bet: '002-H-X transferable frame grammar',
  most_embarrassing_kill_condition:
    'Sibling heads fail polarity under source-strict rows, reducing the parser back to a local 390 artifact.',
};

writeCsv(path.join(reportsDir, `${prefix}_head_transfer_metrics.csv`), metricRows, [
  'checked_date',
  'head',
  'rows',
  'terminal_rows',
  'terminal_rate',
  'recognized_x_rows',
  'terminal_booster_rows',
  'terminal_booster_close_rate',
  'open_operator_rows',
  'open_operator_continue_rate',
  'global_edge_rows',
  'unique_x',
  'top_x',
  'x_polarities',
  'sites',
  'expanded_head_bet_class',
]);
writeCsv(path.join(reportsDir, `${prefix}_frame_rows.csv`), frameRows, [
  'checked_date',
  'object',
  'site',
  'type',
  'shape',
  'material',
  'head',
  'x',
  'x_polarity',
  'terminal',
  'tail',
  'text',
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
writeCsv(path.join(reportsDir, `${prefix}_predictions.csv`), predictionRows, [
  'checked_date',
  'target',
  'prediction',
  'relevant_bets',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
