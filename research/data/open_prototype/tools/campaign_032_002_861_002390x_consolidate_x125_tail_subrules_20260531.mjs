import fs from 'node:fs';
import path from 'node:path';

// When sign 125 fills the X slot after 002-HEAD, the text keeps going — 125
// behaves like a linker. This script asks what it links to: does each head
// sign pick a predictable tail after 125, or can anything follow? It scans
// every text in lipi/metadata_filtered.csv for 002-HEAD-125 occurrences,
// records the full tail after the 125, and buckets each tail into a small
// family: terminal, single 032, the 632-032 family, the 820 cap, or a
// singleton. It then cross-tabulates heads against tail families. A head with
// 2+ rows and exactly one tail family is a "clean head-tail subrule" — in
// practice only head 610, which always takes tail 032. The other families are
// kept but demoted: 632-032 may be Mohenjo-daro seal formula ecology, and 820
// splits across heads. Writes row, per-head, tail-family, and decision CSVs
// plus a summary JSON to data/open_prototype/reports.

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_consolidate_x125_tail_subrules_20260531';

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

function tailFamily(tail) {
  if (tail === '<END>') return 'terminal';
  if (tail === '032') return 'single_032';
  if (tail.startsWith('632 032')) return '632032_family';
  if (tail === '820') return '820_cap';
  return 'singleton_tail';
}

fs.mkdirSync(reportsDir, { recursive: true });

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));
const x125Rows = [];
for (const row of metadataRows) {
  const rowSigns = signs(row.text);
  for (let index = 0; index < rowSigns.length - 2; index += 1) {
    if (rowSigns[index] !== '002' || rowSigns[index + 2] !== '125') continue;
    const tail = rowSigns.slice(index + 3).join(' ') || '<END>';
    x125Rows.push({
      checked_date: '2026-05-31',
      object: row.cisi,
      id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      scope_cell: `${row.site}|${row.type}|${row.shape}|${row.material}`,
      prev_before_002: rowSigns[index - 1] ?? '',
      head: rowSigns[index + 1],
      tail,
      tail_family: tailFamily(tail),
      open: index + 2 < rowSigns.length - 1 ? 'True' : 'False',
      text: row.text,
    });
  }
}

const headRows = countBy(x125Rows, (row) => row.head).map(([head, count]) => {
  const rows = x125Rows.filter((row) => row.head === head);
  const tailFamilies = distinct(rows, (row) => row.tail_family);
  return {
    checked_date: '2026-05-31',
    head,
    rows: String(count),
    tail_family_count: String(tailFamilies),
    tails: topCounts(rows, (row) => row.tail),
    tail_families: topCounts(rows, (row) => row.tail_family),
    scopes: topCounts(rows, (row) => row.scope_cell),
    objects: rows.map((row) => row.object).join(';'),
    decision:
      count >= 2 && tailFamilies === 1
        ? 'clean_head_tail_subrule'
        : count >= 2
          ? 'head_allows_multiple_tails'
          : 'singleton_head_tail',
  };
});

const tailFamilyRows = countBy(x125Rows, (row) => row.tail_family).map(([family, count]) => {
  const rows = x125Rows.filter((row) => row.tail_family === family);
  return {
    checked_date: '2026-05-31',
    tail_family: family,
    rows: String(count),
    heads: topCounts(rows, (row) => row.head),
    scopes: topCounts(rows, (row) => row.scope_cell),
    objects: rows.map((row) => row.object).join(';'),
    decision:
      count >= 2 && distinct(rows, (row) => row.head) >= 2
        ? 'multi_head_tail_family'
        : count >= 2
          ? 'repeated_single_head_tail_family'
          : 'singleton_tail_family',
  };
});

const decisions = [
  {
    checked_date: '2026-05-31',
    candidate: 'X125_TAIL_FAMILY_CONSTRAINT',
    decision: 'keep_candidate_but_make_it_small_menu_not_strict_grammar',
    evidence: `tail families=${topCounts(x125Rows, (row) => row.tail_family)}; head rows=${headRows.map((row) => `${row.head}:${row.decision}`).join(';')}`,
    consequence:
      'X-slot `125` licenses a constrained tail menu, but only head `610` currently has a clean repeated tail-selection subrule.',
  },
  {
    checked_date: '2026-05-31',
    candidate: 'X125_HEAD610_SELECTS_032_TAIL',
    decision: 'keep_cleanest_subrule',
    evidence: headRows.filter((row) => row.head === '610').map((row) => `${row.rows} rows; ${row.tails}; ${row.scopes}`).join('; '),
    consequence:
      'Future `002-610-125` is still predicted to take tail `032`; any other tail kills the cleanest X125 subrule.',
  },
  {
    checked_date: '2026-05-31',
    candidate: 'X125_632032_DEPENDENT_TAIL_FAMILY',
    decision: 'demote_to_scope_local_family',
    evidence: tailFamilyRows.filter((row) => row.tail_family === '632032_family').map((row) => `${row.rows} rows; heads ${row.heads}; scopes ${row.scopes}`).join('; '),
    consequence:
      '`632-032` family remains plausible but not head-deterministic; it may be Mohenjo-daro square-seal formula ecology.',
  },
  {
    checked_date: '2026-05-31',
    candidate: 'X125_820_CAP_IS_NOT_ONE_THING',
    decision: 'keep_wild',
    evidence: tailFamilyRows.filter((row) => row.tail_family === '820_cap').map((row) => `${row.rows} rows; heads ${row.heads}; objects ${row.objects}`).join('; '),
    consequence:
      '`820` after X125 is repeated but split across `405` and weak/source-sensitive `390`; do not assign a cap function yet.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'CONSOLIDATE',
  status: 'x125_tail_subrules',
  x125_rows: x125Rows.length,
  head_rows: headRows,
  tail_family_rows: tailFamilyRows,
  decisions,
  compressed_read:
    'X-slot `125` survives as a constrained tail-menu operator. The only clean repeated head-tail subrule is `610 -> 032`; other tails are local/singleton/wild.',
};

writeCsv(path.join(reportsDir, `${prefix}_rows.csv`), x125Rows, [
  'checked_date',
  'object',
  'id',
  'site',
  'type',
  'shape',
  'material',
  'scope_cell',
  'prev_before_002',
  'head',
  'tail',
  'tail_family',
  'open',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_head_rows.csv`), headRows, [
  'checked_date',
  'head',
  'rows',
  'tail_family_count',
  'tails',
  'tail_families',
  'scopes',
  'objects',
  'decision',
]);

writeCsv(path.join(reportsDir, `${prefix}_tail_family_rows.csv`), tailFamilyRows, [
  'checked_date',
  'tail_family',
  'rows',
  'heads',
  'scopes',
  'objects',
  'decision',
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
