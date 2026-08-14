// Turns the terminal-governor network into checkable predictions about
// damaged signs. In this corpus, 000 is the code for an unreadable sign. If
// governor 002 really closes texts with 817/820 (near-closure 861), and 060
// with 920/550/820 (near-cap 692), then a damaged row reading 002-000 or
// 060-000 at the end should usually resolve — on physical inspection of the
// object — to one of those closure sets. This script scans the filtered
// corpus metadata for every governor-then-000 position, classifies it
// (terminal unknown, damaged multi-unknown, or nonterminal), attaches the
// predicted closure set, and flags rows in Good/Fair condition as high
// priority for source inspection. It computes no statistics and never fills
// in the 000s; it only writes the prediction list as a JSON report and CSV.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_terminal_governor_damage_predictions_20260531';
const RUN_DATE = '2026-05-31';

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = '';
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (ch === '"' && next === '"') {
        cell += '"';
        i += 1;
      } else if (ch === '"') {
        quoted = false;
      } else {
        cell += ch;
      }
    } else if (ch === '"') {
      quoted = true;
    } else if (ch === ',') {
      row.push(cell);
      cell = '';
    } else if (ch === '\n') {
      row.push(cell.replace(/\r$/, ''));
      if (row.some((value) => value.length)) rows.push(row);
      row = [];
      cell = '';
    } else {
      cell += ch;
    }
  }
  if (cell.length || row.length) {
    row.push(cell.replace(/\r$/, ''));
    if (row.some((value) => value.length)) rows.push(row);
  }
  const [header, ...body] = rows;
  return body.map((cols) => Object.fromEntries(header.map((name, idx) => [name, cols[idx] ?? ''])));
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function esc(value) {
  const text = Array.isArray(value) ? value.join(' | ') : String(value ?? '');
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const body = rows.map((row) => fields.map((field) => esc(row[field])).join(',')).join('\n');
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`, 'utf8');
}

const closureSets = {
  '002': {
    strict: ['817', '820'],
    near: ['861'],
    rationale: 'strict terminal-governor network: 002-817 and 002-820; leaky near-closure 002-861',
  },
  '060': {
    strict: ['920', '550', '820'],
    near: ['692'],
    rationale: 'strict terminal-governor network: 060-920, 060-550, 060-820; 060-692 is near-cap/internal-boundary',
  },
};

const rows = parseCsv(fs.readFileSync(META, 'utf8'));
const predictions = [];

for (const row of rows) {
  const toks = tokens(row.text);
  for (let i = 0; i < toks.length - 1; i += 1) {
    const governor = toks[i];
    if (!closureSets[governor] || toks[i + 1] !== '000') continue;
    const next2 = toks[i + 2] ?? '<END>';
    const terminalUnknown = next2 === '<END>' || /[\[\]]/.test(row.text);
    const predictionClass = next2 === '<END>'
      ? 'terminal_unknown_after_governor'
      : next2 === '000'
        ? 'damaged_multi_unknown_after_governor'
        : 'nonterminal_unknown_after_governor';
    const predictedValues = next2 === '<END>'
      ? [...closureSets[governor].strict, ...closureSets[governor].near].join(' ')
      : closureSets[governor].strict.join(' ');
    predictions.push({
      id: row.id,
      cisi: row.cisi,
      site: row.site,
      type: row.type,
      symbol: row.symbol,
      condition: row.condition,
      complete: row.complete,
      text: row.text,
      governor,
      position_index_zero_based: i,
      following_after_unknown: next2,
      prediction_class: predictionClass,
      predicted_closure_set: predictedValues,
      rationale: closureSets[governor].rationale,
      source_priority: row.condition === 'Good' || row.condition === 'Fair' ? 'high' : 'normal',
      terminal_unknown: terminalUnknown ? 'yes' : 'no',
    });
  }
}

const highPriority = predictions.filter((row) => row.source_priority === 'high' && row.terminal_unknown === 'yes');
const summary = {
  date: RUN_DATE,
  phase: 'EXPAND',
  candidate_id: PREFIX,
  tier: 'wild shot',
  bet: 'Damaged terminal rows with 002-000 or 060-000 are not arbitrary unknowns. Under the terminal-governor network, terminal 002-000 rows should often resolve to 817, 820, or leaky near-closure 861, while terminal 060-000 rows should often resolve to 920, 550, 820, or near-cap 692. This is a falsifiable source-inspection prediction, not a filled-in reading.',
  prediction_counts: {
    total_governor_unknown_rows: predictions.length,
    terminal_or_open_terminal_unknown_rows: predictions.filter((row) => row.terminal_unknown === 'yes').length,
    high_priority_source_rows: highPriority.length,
    by_governor: Object.fromEntries(Object.keys(closureSets).map((governor) => [
      governor,
      predictions.filter((row) => row.governor === governor).length,
    ])),
  },
  high_priority_rows: highPriority,
  falsifier: 'If source inspection of high-priority 002-000/060-000 terminal rows routinely yields signs outside the predicted closure sets, demote the terminal-governor network or split it by site/type.',
  non_claim: 'The script does not replace 000 in the corpus and does not count predictions as observed data.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
writeCsv(path.join(OUT_DIR, `${PREFIX}.csv`), predictions, [
  'id',
  'cisi',
  'site',
  'type',
  'symbol',
  'condition',
  'complete',
  'text',
  'governor',
  'position_index_zero_based',
  'following_after_unknown',
  'prediction_class',
  'predicted_closure_set',
  'rationale',
  'source_priority',
  'terminal_unknown',
]);

console.log(JSON.stringify({
  candidate_id: PREFIX,
  counts: summary.prediction_counts,
  high_priority_rows: highPriority.slice(0, 20),
}, null, 2));
