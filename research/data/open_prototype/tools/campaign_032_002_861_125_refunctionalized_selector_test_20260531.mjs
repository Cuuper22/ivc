import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_125_refunctionalized_selector_test_20260531';
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

function signs(text) {
  return [...String(text || '').matchAll(/\d{3}/g)].map((match) => match[0]);
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
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

function topCounts(items, fn, n = 10) {
  return countBy(items, fn)
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function safeShare(num, den) {
  return den ? (num / den).toFixed(6) : 'NA';
}

function formatExamples(rows) {
  return rows.map((row) => `${row.cisi}:${row.text}`).join(' | ');
}

fs.mkdirSync(reportsDir, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  tokens: signs(row.text),
}));
const canonicalRows = [...new Map(rawRows.map((row) => [row.tokens.join(' '), row])).values()];

const rows390125 = [];
for (const row of canonicalRows) {
  for (let i = 0; i < row.tokens.length - 1; i += 1) {
    if (row.tokens[i] !== '390' || row.tokens[i + 1] !== '125') continue;
    const isPost002 = row.tokens[i - 1] === '002';
    const tail = row.tokens.slice(i + 2);
    rows390125.push({
      checked_date: checkedDate,
      cisi: objectId(row),
      row_id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      lane: isPost002 ? 'post_002_390_125' : 'raw_non002_390_125',
      left_before_390: row.tokens.slice(0, i).join(' ') || '<START>',
      tail_after_125: tail.join(' ') || '<END>',
      tail_length_after_125: tail.length,
      continues_after_125: tail.length > 0,
      starts_632_032: tail[0] === '632' && tail[1] === '032',
      immediate_tail: tail[0] ?? '<END>',
      text: row.text,
    });
  }
}

function laneSummary(lane) {
  const rows = rows390125.filter((row) => row.lane === lane);
  const continuing = rows.filter((row) => row.continues_after_125);
  const starts632032 = rows.filter((row) => row.starts_632_032);
  return {
    checked_date: checkedDate,
    lane,
    rows: String(rows.length),
    continuing_rows: String(continuing.length),
    continuing_share: safeShare(continuing.length, rows.length),
    terminal_rows: String(rows.length - continuing.length),
    terminal_share: safeShare(rows.length - continuing.length, rows.length),
    starts_632_032_rows: String(starts632032.length),
    starts_632_032_share: safeShare(starts632032.length, rows.length),
    distinct_sites: String(new Set(rows.map((row) => row.site)).size),
    distinct_tails: String(new Set(rows.map((row) => row.tail_after_125)).size),
    sites: topCounts(rows, (row) => row.site),
    tails: topCounts(rows, (row) => row.tail_after_125),
    immediate_tails: topCounts(rows, (row) => row.immediate_tail),
    examples: formatExamples(rows),
  };
}

const summaries = [laneSummary('post_002_390_125'), laneSummary('raw_non002_390_125')];
const target = summaries.find((row) => row.lane === 'post_002_390_125');
const raw = summaries.find((row) => row.lane === 'raw_non002_390_125');

const targetContinuing = Number(target.continuing_share);
const rawContinuing = Number(raw.continuing_share);
const target632 = Number(target.starts_632_032_share);
const raw632 = Number(raw.starts_632_032_share);
const tailOverlap = new Set(
  rows390125.filter((row) => row.lane === 'post_002_390_125').map((row) => row.tail_after_125),
);
const rawTailOverlap = rows390125
  .filter((row) => row.lane === 'raw_non002_390_125')
  .filter((row) => tailOverlap.has(row.tail_after_125)).length;

let decision = 'mixed_125_inheritance_pressure';
let confidenceTier = 'wild shot';
if (targetContinuing === 1 && targetContinuing - rawContinuing >= 0.5 && rawTailOverlap === 0) {
  decision = 'candidate_125_refunctionalized_open_selector';
  confidenceTier = 'candidate';
} else if (target632 > raw632 && targetContinuing > rawContinuing) {
  decision = 'wild_125_refunctionalized_open_selector';
}

const decisions = [
  {
    checked_date: checkedDate,
    bet_id: 'V8_125_REFUNCTIONALIZED_OPEN_SELECTOR_20260531',
    confidence_tier: confidenceTier,
    decision,
    risky_parse_bet:
      '`002` refunctionalizes inherited raw `390-125` into an open rank/title selector: post-`002` rows should continue after `125` and use different tails from raw non-`002` `390-125`.',
    what_would_promote:
      'More `002-390-125-Y` rows continue with rank/title-like tails such as `632-032`, while raw `390-125` stays terminal or differently-tailed.',
    what_would_break:
      'Raw non-`002` `390-125` shares the same tails at comparable rates, or source-visible target rows turn out terminal after `125`.',
  },
];

const summary = {
  checked_date: checkedDate,
  status: '125_refunctionalized_selector_test',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: canonicalRows.length,
    all_390_125_pairs: rows390125.length,
  },
  lane_summary: summaries.map((row) => `${row.lane}:${row.continuing_rows}/${row.rows}_continuing:${row.starts_632_032_rows}/${row.rows}_632032`).join(';'),
  exact_tail_overlap_raw_with_target: rawTailOverlap,
  decisions: decisions.map((row) => `${row.bet_id}:${row.decision}`).join(';'),
};

writeCsv(path.join(reportsDir, `${prefix}_rows.csv`), rows390125, [
  'checked_date',
  'cisi',
  'row_id',
  'site',
  'type',
  'shape',
  'lane',
  'left_before_390',
  'tail_after_125',
  'tail_length_after_125',
  'continues_after_125',
  'starts_632_032',
  'immediate_tail',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_lane_summary.csv`), summaries, [
  'checked_date',
  'lane',
  'rows',
  'continuing_rows',
  'continuing_share',
  'terminal_rows',
  'terminal_share',
  'starts_632_032_rows',
  'starts_632_032_share',
  'distinct_sites',
  'distinct_tails',
  'sites',
  'tails',
  'immediate_tails',
  'examples',
]);

writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  'checked_date',
  'bet_id',
  'confidence_tier',
  'decision',
  'risky_parse_bet',
  'what_would_promote',
  'what_would_break',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
