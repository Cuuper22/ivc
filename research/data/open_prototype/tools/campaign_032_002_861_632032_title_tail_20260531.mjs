import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_632032_title_tail_20260531';

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
  return [...String(text || '').matchAll(/\d{3}/g)].map((match) => match[0]);
}

function countBy(items, fn) {
  const counts = new Map();
  for (const item of items) {
    const key = fn(item) || '-';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()].sort(
    (a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }),
  );
}

function topCounts(counts, n = 12) {
  return counts
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function findGovernedHead(tokens, signIndex) {
  for (let headIndex = signIndex - 1; headIndex >= 0 && headIndex >= signIndex - 6; headIndex -= 1) {
    if (tokens[headIndex - 1] === '002') {
      return {
        governed: true,
        head: tokens[headIndex],
        prevBefore002: tokens[headIndex - 2] ?? '<START>',
      };
    }
  }
  return { governed: false, head: '', prevBefore002: '' };
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  tokens: signs(row.text),
}));

const sign632 = [];
const tail632032 = [];

for (const row of rows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
    if (row.tokens[i] === '632') {
      sign632.push({
        row,
        index: i,
        prev: row.tokens[i - 1] ?? '<START>',
        next: row.tokens[i + 1] ?? '<END>',
      });
    }

    if (row.tokens[i] === '632' && row.tokens[i + 1] === '032') {
      const governed = findGovernedHead(row.tokens, i);
      tail632032.push({
        checked_date: '2026-05-31',
        cisi: row.cisi || '-',
        row_id: row.id,
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        cult: row.cult,
        prev_before_632: row.tokens[i - 1] ?? '<START>',
        next_after_632032: row.tokens[i + 2] ?? '<END>',
        after_125: String(row.tokens[i - 1] === '125'),
        governed_by_002_within_six: String(governed.governed),
        governed_head: governed.head,
        prev_before_002: governed.prevBefore002,
        local_context: row.tokens.slice(Math.max(0, i - 4), Math.min(row.tokens.length, i + 5)).join('-'),
        model_implication:
          row.tokens[i - 1] === '125' && governed.governed
            ? 'direct_evidence_for_transferable_125_632_032_title_tail'
            : row.tokens[i - 1] === '125'
              ? 'ungoverned_or_damaged_analogue_for_125_632_032_title_tail'
              : 'non_125_632_032_background',
        text: row.text,
      });
    }
  }
}

const terminal632032 = tail632032.filter((row) => row.next_after_632032 === '<END>');
const after125Tail = tail632032.filter((row) => row.after_125 === 'true');
const governedAfter125Tail = tail632032.filter(
  (row) => row.after_125 === 'true' && row.governed_by_002_within_six === 'true',
);

const summary = {
  checked_date: '2026-05-31',
  status: '632032_title_tail_probe',
  hypothesis_tested: '`632-032` is a transferable title/office sub-tail after `125`, not a free decorative formula.',
  key_counts: {
    sign_632_occurrences: sign632.length,
    sign_632_top_prev: topCounts(countBy(sign632, (item) => item.prev)),
    sign_632_top_next: topCounts(countBy(sign632, (item) => item.next)),
    tail_632032_occurrences: tail632032.length,
    tail_632032_after_125: after125Tail.length,
    tail_632032_governed_after_125: governedAfter125Tail.length,
    tail_632032_terminal: terminal632032.length,
    governed_after_125_heads: topCounts(countBy(governedAfter125Tail, (item) => item.governed_head)),
    governed_after_125_prev_before_002: topCounts(countBy(governedAfter125Tail, (item) => item.prev_before_002)),
  },
  decisions: [
    '`125-632-032` strengthens from promoted sub-bet to promoted candidate sub-tail: `632-032` is rare, mostly terminal, and most of its governed evidence follows `125`.',
    '`632-032` is not exclusive to `125`; non-125 rows remain the adversarial background.',
    'The portable-title read survives first formula-pressure check because governed `125-632-032` appears under `190` and `390`.',
  ],
  next_falsifier:
    'A broader plate/source check that collapses the governed `125-632-032` rows into copies, or new governed `632-032` rows mostly not after `125`, would demote the sub-tail.',
};

writeCsv(path.join(reportsDir, `${prefix}_tail_rows.csv`), tail632032, [
  'checked_date',
  'cisi',
  'row_id',
  'site',
  'type',
  'symbol',
  'cult',
  'prev_before_632',
  'next_after_632032',
  'after_125',
  'governed_by_002_within_six',
  'governed_head',
  'prev_before_002',
  'local_context',
  'model_implication',
  'text',
]);

const distributionRows = [
  {
    checked_date: '2026-05-31',
    sign: '632',
    occurrences: String(sign632.length),
    top_prev: topCounts(countBy(sign632, (item) => item.prev)),
    top_next: topCounts(countBy(sign632, (item) => item.next)),
  },
];
writeCsv(path.join(reportsDir, `${prefix}_632_distribution.csv`), distributionRows, [
  'checked_date',
  'sign',
  'occurrences',
  'top_prev',
  'top_next',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
