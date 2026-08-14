import fs from 'node:fs';
import path from 'node:path';

// This script replaces one big claim with many small ones. The big claim was
// that the X slot (the sign two after 002) carries "function classes" as an
// umbrella system. Here we grade every X sign on its own. The script scans
// lipi/metadata_filtered.csv for all 002-HEAD-X occurrences, keeps X signs
// with at least 3 rows, and for each one measures: its open rate (how often
// text continues after it), a leave-one-out test of predicting open-versus-
// closed from the sign's other rows, and how many distinct heads, scope cells
// (site|type|shape|material), and tails it spans. Signs that predict
// perfectly across 2+ heads and 2+ scopes become portable open or terminal
// classes; signs that only work under one head or one scope are flagged as
// templates or local classes; signs at or below 34% accuracy are bad
// predictors and killed as portable classes. Writes class-row and decision
// CSVs plus a summary JSON to data/open_prototype/reports.

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_consolidate_xslot_class_portfolio_20260531';

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

function pct(numerator, denominator) {
  return denominator ? (numerator / denominator).toFixed(6) : '';
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

function distinct(rows, keyFn) {
  return new Set(rows.map(keyFn).filter(Boolean)).size;
}

function classify({ rows, open, correct, covered, heads, scopes, tails }) {
  const openRate = rows.length ? open / rows.length : 0;
  const acc = covered ? correct / covered : 0;
  if (rows.length >= 3 && acc === 1 && open === 0 && heads >= 2 && scopes >= 2 && tails === 1) return 'portable_terminal_class';
  if (rows.length >= 3 && acc === 1 && open === rows.length && heads >= 2 && scopes >= 2) return 'portable_open_class';
  if (rows.length >= 3 && acc === 1 && heads === 1) return 'head_template_not_portable_class';
  if (rows.length >= 3 && acc === 1 && scopes === 1) return 'scope_local_class_not_portable';
  if (rows.length >= 3 && acc >= 0.75 && heads >= 3 && scopes >= 3) return 'portable_biased_class';
  if (rows.length >= 3 && acc <= 0.34) return 'bad_x_predictor';
  return 'weak_or_unresolved_x_class';
}

fs.mkdirSync(reportsDir, { recursive: true });

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));
const xRows = [];
for (const row of metadataRows) {
  const rowSigns = signs(row.text);
  for (let index = 0; index < rowSigns.length - 2; index += 1) {
    if (rowSigns[index] !== '002') continue;
    xRows.push({
      checked_date: '2026-05-31',
      object: row.cisi,
      id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      scope_cell: `${row.site}|${row.type}|${row.shape}|${row.material}`,
      head: rowSigns[index + 1],
      x: rowSigns[index + 2],
      open: index + 2 < rowSigns.length - 1,
      tail_after_x: rowSigns.slice(index + 3).join(' ') || '<END>',
      text: row.text,
    });
  }
}

const xSigns = countBy(xRows, (row) => row.x)
  .filter(([, count]) => count >= 3)
  .map(([x]) => x);

const classRows = xSigns.map((x) => {
  const rows = xRows.filter((row) => row.x === x);
  let covered = 0;
  let correct = 0;
  for (const test of rows) {
    const train = rows.filter((row) => row !== test);
    if (!train.length) continue;
    const trainOpen = train.filter((row) => row.open).length;
    const predictedOpen = trainOpen >= train.length - trainOpen;
    covered += 1;
    if (predictedOpen === test.open) correct += 1;
  }
  const open = rows.filter((row) => row.open).length;
  const heads = distinct(rows, (row) => row.head);
  const scopes = distinct(rows, (row) => row.scope_cell);
  const tails = distinct(rows, (row) => row.tail_after_x);
  return {
    checked_date: '2026-05-31',
    x,
    rows: String(rows.length),
    open_rate: ratio(open, rows.length),
    loo_covered: String(covered),
    loo_accuracy: pct(correct, covered),
    heads: String(heads),
    scopes: String(scopes),
    tails: String(tails),
    head_counts: topCounts(rows, (row) => row.head),
    scope_counts: topCounts(rows, (row) => row.scope_cell),
    tail_counts: topCounts(rows, (row) => row.tail_after_x),
    objects: rows.map((row) => row.object).join(';'),
    class_decision: classify({ rows, open, correct, covered, heads, scopes, tails }),
  };
}).sort((a, b) => Number(b.rows) - Number(a.rows) || a.x.localeCompare(b.x, undefined, { numeric: true }));

const decisions = [
  {
    checked_date: '2026-05-31',
    candidate: 'X_SLOT_FUNCTION_CLASSES',
    decision: 'demote_umbrella_to_portfolio',
    evidence: classRows.map((row) => `${row.x}:${row.class_decision}`).join(';'),
    consequence:
      'Do not keep a rank-1 umbrella claim. Carry only sign-specific classes with their own nulls and scope limits.',
  },
  {
    checked_date: '2026-05-31',
    candidate: 'PORTABLE_X_CLASSES',
    decision: 'keep_sign_specific',
    evidence: classRows
      .filter((row) => row.class_decision.startsWith('portable'))
      .map((row) => `${row.x}:${row.class_decision}:acc=${row.loo_accuracy}:open=${row.open_rate}`)
      .join(';'),
    consequence:
      'Portable class candidates are sign-specific; `095`, `125`, `530`, and `705` remain relevant to the current campaign, while other portable classes are controls unless they attack the live parser.',
  },
  {
    checked_date: '2026-05-31',
    candidate: 'BAD_OR_LOCAL_X_CLASSES',
    decision: 'kill_as_portable_classes',
    evidence: classRows
      .filter((row) => row.class_decision === 'bad_x_predictor' || row.class_decision.includes('not_portable'))
      .map((row) => `${row.x}:${row.class_decision}:acc=${row.loo_accuracy}`)
      .join(';'),
    consequence:
      'Signs such as `032`, `550`, `615`, `632`, `692`, `840`, and `892` cannot be used as portable X classes in the parser.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'CONSOLIDATE',
  status: 'xslot_class_portfolio',
  class_rows: classRows,
  decisions,
  compressed_read:
    'The broad X-slot class hypothesis is demoted to a sign-specific portfolio. Only sign-level classes survive; the umbrella is not itself a candidate.',
};

writeCsv(path.join(reportsDir, `${prefix}_class_rows.csv`), classRows, [
  'checked_date',
  'x',
  'rows',
  'open_rate',
  'loo_covered',
  'loo_accuracy',
  'heads',
  'scopes',
  'tails',
  'head_counts',
  'scope_counts',
  'tail_counts',
  'objects',
  'class_decision',
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
