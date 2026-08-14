import fs from 'node:fs';
import path from 'node:path';

// This script tests which signs really deserve a "terminal class" label — a
// sign that closes an inscription when it fills the X slot after 002-HEAD —
// versus signs that just look terminal because they end texts everywhere.
// It reads the full corpus (lipi/metadata_filtered.csv), splits each text into
// 3-digit sign codes, and for seven focus signs (095, 705, 140, 072, 692, 125,
// 530) compares two rates: how often the sign is text-final anywhere in the
// corpus (the global prior) versus how often it is final specifically in the
// X slot. A sign earns "terminal_class_candidate" only with at least 3 X-slot
// rows, an X-slot terminal rate of 0.8+, a lift of 0.3+ over its global rate,
// and witnesses at 2+ sites. Verdicts here unbundle the old 095/705 claim:
// 095 stays a candidate, 705 narrows to terminal-default-with-exception, and
// 692 is explained by the raw prior. Writes class-row and decision CSVs plus a
// summary JSON to data/open_prototype/reports.

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_consolidate_terminal_class_labels_20260531';
const focusSigns = ['095', '705', '140', '072', '692', '125', '530'];

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

function delta(a, b) {
  if (a === null || b === null) return '';
  return (a - b).toFixed(6);
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

function distinctCount(rows, keyFn) {
  return new Set(rows.map(keyFn).filter(Boolean)).size;
}

function sourceWeakRows(rows) {
  return rows.filter((row) => row.object === '-' || row.material === '-' || row.type === '-');
}

fs.mkdirSync(reportsDir, { recursive: true });

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));
const globalRows = [];
const xSlotRows = [];
for (const row of metadataRows) {
  const rowSigns = signs(row.text);
  for (let index = 0; index < rowSigns.length; index += 1) {
    globalRows.push({
      checked_date: '2026-05-31',
      object: row.cisi,
      id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      sign: rowSigns[index],
      terminal: index === rowSigns.length - 1,
      scope_cell: `${row.site}|${row.type}|${row.shape}|${row.material}`,
      text: row.text,
    });
    if (rowSigns[index] === '002' && rowSigns[index + 1] && rowSigns[index + 2]) {
      xSlotRows.push({
        checked_date: '2026-05-31',
        object: row.cisi,
        id: row.id,
        site: row.site,
        type: row.type,
        shape: row.shape,
        material: row.material,
        head: rowSigns[index + 1],
        x: rowSigns[index + 2],
        x_terminal: index + 2 === rowSigns.length - 1,
        tail_after_x: rowSigns.slice(index + 3).join(' ') || '<END>',
        scope_cell: `${row.site}|${row.type}|${row.shape}|${row.material}`,
        text: row.text,
      });
    }
  }
}

const classRows = focusSigns.map((sign) => {
  const global = globalRows.filter((row) => row.sign === sign);
  const xRows = xSlotRows.filter((row) => row.x === sign);
  const globalTerminal = global.filter((row) => row.terminal).length;
  const xTerminal = xRows.filter((row) => row.x_terminal).length;
  const xRate = rate(xTerminal, xRows.length);
  const globalRate = rate(globalTerminal, global.length);
  const weak = sourceWeakRows(xRows);
  let verdict = 'not_terminal_class';
  if (xRows.length >= 3 && xRate >= 0.8 && xRate - globalRate >= 0.3 && distinctCount(xRows, (row) => row.site) >= 2) {
    verdict = 'terminal_class_candidate';
  } else if (xRows.length >= 2 && xRate === 1 && xRate - globalRate >= 0.3) {
    verdict = 'terminal_class_wild_or_low_count';
  } else if (globalRate >= 0.65 && xRate >= 0.65) {
    verdict = 'raw_terminal_prior_explains';
  } else if (xRows.length >= 3 && xRate <= 0.25) {
    verdict = 'open_operator_control';
  }
  return {
    checked_date: '2026-05-31',
    sign,
    global_rows: String(global.length),
    global_terminal_rate: ratio(globalTerminal, global.length),
    x_slot_rows: String(xRows.length),
    x_slot_terminal_rate: ratio(xTerminal, xRows.length),
    x_minus_global_terminal_delta: delta(xRate, globalRate),
    x_slot_sites: String(distinctCount(xRows, (row) => row.site)),
    x_slot_heads: String(distinctCount(xRows, (row) => row.head)),
    weak_x_slot_rows: String(weak.length),
    heads: topCounts(xRows, (row) => row.head),
    sites: topCounts(xRows, (row) => row.site),
    tails: topCounts(xRows, (row) => row.tail_after_x),
    objects: xRows.map((row) => row.object).join(';'),
    verdict,
  };
});

const decisions = [
  {
    checked_date: '2026-05-31',
    candidate: 'X095_TERMINAL_CLASS_LABEL',
    decision: 'keep_candidate',
    evidence: classRows.filter((row) => row.sign === '095').map((row) => `X terminal ${row.x_slot_terminal_rate}; global terminal ${row.global_terminal_rate}; sites ${row.sites}; heads ${row.heads}`).join('; '),
    consequence:
      '`095` is the cleaner terminal-class candidate: all current X-slot rows close and raw global terminality is low.',
  },
  {
    checked_date: '2026-05-31',
    candidate: 'X705_TERMINAL_CLASS_LABEL',
    decision: 'split_and_narrow',
    evidence: classRows.filter((row) => row.sign === '705').map((row) => `X terminal ${row.x_slot_terminal_rate}; global terminal ${row.global_terminal_rate}; weak rows ${row.weak_x_slot_rows}; tails ${row.tails}`).join('; '),
    consequence:
      '`705` becomes terminal-default-with-320-705-125-exception, not a clean terminal class equal to `095`.',
  },
  {
    checked_date: '2026-05-31',
    candidate: 'X095_X705_TERMINAL_CLASS_LABELS',
    decision: 'unbundle',
    evidence:
      `095 verdict ${classRows.find((row) => row.sign === '095').verdict}; 705 verdict ${classRows.find((row) => row.sign === '705').verdict}; 692 verdict ${classRows.find((row) => row.sign === '692').verdict}`,
    consequence:
      'Do not state bundled `095/705` as one claim; carry `095` stronger, `705` narrower, and keep `692` demoted.',
  },
  {
    checked_date: '2026-05-31',
    candidate: 'X692_BOUNDARY_CLOSER_NOT_390_VALUE',
    decision: 'keep_demoted',
    evidence: classRows.filter((row) => row.sign === '692').map((row) => `X terminal ${row.x_slot_terminal_rate}; global terminal ${row.global_terminal_rate}`).join('; '),
    consequence:
      '`692` remains explained by raw terminal prior, not by a useful `390` payload role.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'CONSOLIDATE',
  status: 'terminal_class_labels',
  class_rows: classRows,
  decisions,
  compressed_read:
    '`095` is the clean terminal-class candidate; `705` is terminal-default with a named exception and source weakness; bundled `095/705` should be unbundled.',
};

writeCsv(path.join(reportsDir, `${prefix}_class_rows.csv`), classRows, [
  'checked_date',
  'sign',
  'global_rows',
  'global_terminal_rate',
  'x_slot_rows',
  'x_slot_terminal_rate',
  'x_minus_global_terminal_delta',
  'x_slot_sites',
  'x_slot_heads',
  'weak_x_slot_rows',
  'heads',
  'sites',
  'tails',
  'objects',
  'verdict',
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
