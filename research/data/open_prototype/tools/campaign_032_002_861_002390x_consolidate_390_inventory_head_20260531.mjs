import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_consolidate_390_inventory_head_20260531';

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

function classifyHead(rows) {
  const open = rows.filter((row) => row.open).length;
  const openRate = open / rows.length;
  const uniqueX = countBy(rows, (row) => row.x).length;
  const repeatShare = countBy(rows, (row) => row.x)
    .filter(([, count]) => count >= 2)
    .reduce((sum, [, count]) => sum + count, 0) / rows.length;
  if (openRate === 0 && repeatShare >= 0.7) return 'closed_template_head';
  if (openRate >= 0.8 && repeatShare >= 0.5) return 'open_template_head';
  if (uniqueX >= 8 && repeatShare >= 0.45 && openRate > 0.2 && openRate < 0.6) return 'mixed_inventory_head';
  if (uniqueX >= 8 && repeatShare < 0.3) return 'diffuse_inventory_head';
  if (openRate <= 0.3) return 'terminal_default_head';
  if (openRate >= 0.7) return 'open_default_head';
  return 'mixed_low_count_or_unclassified';
}

fs.mkdirSync(reportsDir, { recursive: true });

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));
const frames = [];
for (const row of metadataRows) {
  const rowSigns = signs(row.text);
  for (let index = 0; index < rowSigns.length - 2; index += 1) {
    if (rowSigns[index] !== '002') continue;
    frames.push({
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

const headRows = countBy(frames, (row) => row.head)
  .filter(([, count]) => count >= 5)
  .map(([head, count]) => {
    const rows = frames.filter((row) => row.head === head);
    const xCounts = countBy(rows, (row) => row.x);
    const repeatedRows = xCounts.filter(([, xCount]) => xCount >= 2).reduce((sum, [, xCount]) => sum + xCount, 0);
    const open = rows.filter((row) => row.open).length;
    const terminalXs = xCounts
      .filter(([x]) => rows.filter((row) => row.x === x).every((row) => !row.open))
      .map(([x, xCount]) => `${x}:${xCount}`)
      .join(';');
    const openXs = xCounts
      .filter(([x]) => rows.filter((row) => row.x === x).every((row) => row.open))
      .map(([x, xCount]) => `${x}:${xCount}`)
      .join(';');
    return {
      checked_date: '2026-05-31',
      head,
      rows: String(count),
      unique_x: String(xCounts.length),
      repeated_x_row_share: ratio(repeatedRows, count),
      open_rate: ratio(open, count),
      x_inventory: xCounts.map(([x, xCount]) => `${x}:${xCount}`).join(';'),
      terminal_xs: terminalXs,
      open_xs: openXs,
      scopes: topCounts(rows, (row) => row.scope_cell),
      head_class: classifyHead(rows),
    };
  })
  .sort((a, b) => Number(b.rows) - Number(a.rows));

const head390 = headRows.find((row) => row.head === '390');
const mixedInventoryHeads = headRows.filter((row) => row.head_class === 'mixed_inventory_head');
const decisions = [
  {
    checked_date: '2026-05-31',
    candidate: 'SIGN390_X_INVENTORY_HEAD',
    decision: 'keep_but_demote_from_special_to_member_of_head_taxonomy',
    evidence: `390 class=${head390.head_class}; rows=${head390.rows}; unique X=${head390.unique_x}; repeated share=${head390.repeated_x_row_share}; open=${head390.open_rate}; other mixed inventory heads=${mixedInventoryHeads.map((row) => row.head).join(';')}`,
    consequence:
      '`390` remains useful as a mixed inventory head, but it is not special enough to assign value or function beyond the broader head taxonomy.',
  },
  {
    checked_date: '2026-05-31',
    candidate: 'SIGN390_PAYLOAD_CLASSIFIER',
    decision: 'carry_only_for_repeated_x_classes',
    evidence: `390 repeated X classes=${head390.x_inventory}; terminal=${head390.terminal_xs}; open=${head390.open_xs}`,
    consequence:
      'Under `390`, only repeated X classes `125`, `095`, and `705` carry candidate weight; singleton X values stay test bait.',
  },
  {
    checked_date: '2026-05-31',
    candidate: 'HEAD_TAXONOMY_FOR_NEXT_EXPAND',
    decision: 'use_as_destructive_frame_not_new_family',
    evidence: headRows.map((row) => `${row.head}:${row.head_class}`).join(';'),
    consequence:
      'Next expansion should compare `390` against `861`, `031`, `220`, and `405` before proposing any sign meaning for a head.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'CONSOLIDATE',
  status: '390_inventory_head',
  head_rows: headRows,
  decisions,
  compressed_read:
    '`390` survives only as one mixed inventory head in a broader head taxonomy. It should not receive meaning/function until it beats sibling heads under held-out/collapse tests.',
};

writeCsv(path.join(reportsDir, `${prefix}_head_rows.csv`), headRows, [
  'checked_date',
  'head',
  'rows',
  'unique_x',
  'repeated_x_row_share',
  'open_rate',
  'x_inventory',
  'terminal_xs',
  'open_xs',
  'scopes',
  'head_class',
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
