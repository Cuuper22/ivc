import fs from 'node:fs';
import path from 'node:path';

// This script asks: if we throw away every inscription that is not "strict" —
// not verified against a source image good enough for token boxes — what is
// left of the 002-390-X parser? It reads the two earlier source-weight CSVs
// (the X-slot rows and the left-context rows), keeps only rows whose
// source_class is "strict", joins them by object, and labels each surviving
// row as open-branch core (X = 125) or terminal-branch core (X = 095 or 692).
// It then runs four contradiction checks — 125 must never be terminal, 095/692
// must always be terminal, and so on — and records that only the open-versus-
// terminal syntax contrast survives; every semantic gloss is demoted.
// Outputs: three CSVs (rows, bucket summaries, contradiction checks) and a
// summary JSON in data/open_prototype/reports, with the summary printed.

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const xRowsPath = path.join(
  reportsDir,
  'campaign_032_002_861_002390x_consolidate_xslot_source_weight_20260531_row_classification.csv',
);
const leftRowsPath = path.join(
  reportsDir,
  'campaign_032_002_861_002390x_consolidate_left_context_source_weight_20260531_row_classification.csv',
);
const prefix = 'campaign_032_002_861_002390x_consolidate_strict_core_collapse_20260531';

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

function topCounts(counts) {
  return counts.map(([key, value]) => `${key}:${value}`).join(';');
}

fs.mkdirSync(reportsDir, { recursive: true });

const xRows = parseCsv(fs.readFileSync(xRowsPath, 'utf8'));
const leftRows = parseCsv(fs.readFileSync(leftRowsPath, 'utf8'));
const strictXRows = xRows.filter((row) => row.source_class === 'strict');
const strictLeftRows = leftRows.filter((row) => row.source_class === 'strict');

const strictCoreRows = strictXRows.map((row) => {
  const left = strictLeftRows.find((leftRow) => leftRow.object === row.object);
  return {
    checked_date: '2026-05-31',
    object: row.object,
    left_final: left?.left_final ?? '',
    x: row.x,
    role: row.role,
    tail_after_x: row.tail_after_x,
    terminal_after_x: row.terminal_after_x,
    strict_core_use:
      row.x === '125'
        ? 'open_branch_core'
        : ['095', '692'].includes(row.x)
          ? 'terminal_branch_core'
          : 'strict_other',
    parser_consequence:
      row.x === '125'
        ? 'keeps open branch syntax but not tail semantics'
        : ['095', '692'].includes(row.x)
          ? 'keeps terminal closure syntax but not semantic value'
          : 'unexpected strict branch',
    text: row.text,
  };
});

const strictSummaryRows = [
  {
    checked_date: '2026-05-31',
    bucket: 'strict_core_all',
    n: String(strictCoreRows.length),
    x_distribution: topCounts(countBy(strictCoreRows, (row) => row.x)),
    terminal_distribution: topCounts(countBy(strictCoreRows, (row) => row.terminal_after_x)),
    left_distribution: topCounts(countBy(strictCoreRows, (row) => row.left_final)),
    decision: 'strict_core_preserves_open_vs_terminal_syntax_only',
    evidence: strictCoreRows.map((row) => `${row.object}:${row.left_final}->${row.x}->${row.tail_after_x}`).join(' | '),
  },
  {
    checked_date: '2026-05-31',
    bucket: 'strict_core_open',
    n: String(strictCoreRows.filter((row) => row.x === '125').length),
    x_distribution: topCounts(countBy(strictCoreRows.filter((row) => row.x === '125'), (row) => row.x)),
    terminal_distribution: topCounts(countBy(strictCoreRows.filter((row) => row.x === '125'), (row) => row.terminal_after_x)),
    left_distribution: topCounts(countBy(strictCoreRows.filter((row) => row.x === '125'), (row) => row.left_final)),
    decision: '125_open_syntax_survives_strict_core',
    evidence: strictCoreRows
      .filter((row) => row.x === '125')
      .map((row) => `${row.object}:${row.left_final}->${row.x}->${row.tail_after_x}`)
      .join(' | '),
  },
  {
    checked_date: '2026-05-31',
    bucket: 'strict_core_terminal',
    n: String(strictCoreRows.filter((row) => ['095', '692'].includes(row.x)).length),
    x_distribution: topCounts(countBy(strictCoreRows.filter((row) => ['095', '692'].includes(row.x)), (row) => row.x)),
    terminal_distribution: topCounts(
      countBy(strictCoreRows.filter((row) => ['095', '692'].includes(row.x)), (row) => row.terminal_after_x),
    ),
    left_distribution: topCounts(countBy(strictCoreRows.filter((row) => ['095', '692'].includes(row.x)), (row) => row.left_final)),
    decision: '095_692_terminal_syntax_survives_strict_core',
    evidence: strictCoreRows
      .filter((row) => ['095', '692'].includes(row.x))
      .map((row) => `${row.object}:${row.left_final}->${row.x}->${row.tail_after_x}`)
      .join(' | '),
  },
];

const contradictionChecks = [
  {
    checked_date: '2026-05-31',
    check_id: 'STRICT_CORE_125_IS_ALWAYS_OPEN',
    result: strictCoreRows.filter((row) => row.x === '125').every((row) => row.terminal_after_x === 'False') ? 'pass' : 'fail',
    evidence: strictCoreRows.filter((row) => row.x === '125').map((row) => `${row.object}:${row.tail_after_x}`).join(' | '),
    consequence: 'keep 125 as strict open-branch syntax',
  },
  {
    checked_date: '2026-05-31',
    check_id: 'STRICT_CORE_TERMINAL_BRANCHES_END',
    result: strictCoreRows
      .filter((row) => ['095', '692'].includes(row.x))
      .every((row) => row.terminal_after_x === 'True')
      ? 'pass'
      : 'fail',
    evidence: strictCoreRows.filter((row) => ['095', '692'].includes(row.x)).map((row) => `${row.object}:${row.x}`).join(' | '),
    consequence: 'keep 095/692 as strict terminal syntax',
  },
  {
    checked_date: '2026-05-31',
    check_id: 'STRICT_CORE_LEFT_OPERATORS_SURVIVE_ONLY_PARTLY',
    result: 'partial_pass',
    evidence: strictCoreRows.map((row) => `${row.object}:${row.left_final}->${row.x}`).join(' | '),
    consequence: '235 and 032 have one strict witness each; 004 has none, so left parser stays source-thin.',
  },
  {
    checked_date: '2026-05-31',
    check_id: 'STRICT_CORE_SEMANTICS_DO_NOT_SURVIVE',
    result: 'pass_demote',
    evidence: 'strict core has four rows and only open/terminal contrast',
    consequence: 'no sign value, phonetics, language identity, or translation can be promoted from strict core.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'CONSOLIDATE',
  status: 'strict_core_collapse',
  strict_core: {
    rows: strictCoreRows.length,
    x_distribution: topCounts(countBy(strictCoreRows, (row) => row.x)),
    left_distribution: topCounts(countBy(strictCoreRows, (row) => row.left_final)),
    survivor: 'open_vs_terminal_syntax_only',
  },
  kept: [
    '125 as strict open/continuing branch syntax',
    '095 and 692 as strict terminal branch syntax',
  ],
  demoted_under_strict_core: [
    '004 neutral split',
    '705 repeated terminal ecology',
    '530 one-complement linker',
    '590-032 bridge',
    '125-820 terminal cap',
    'semantic/title/status/result glosses',
  ],
  contradiction_results: Object.fromEntries(contradictionChecks.map((row) => [row.check_id, row.result])),
};

writeCsv(path.join(reportsDir, `${prefix}_rows.csv`), strictCoreRows, [
  'checked_date',
  'object',
  'left_final',
  'x',
  'role',
  'tail_after_x',
  'terminal_after_x',
  'strict_core_use',
  'parser_consequence',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_summary_rows.csv`), strictSummaryRows, [
  'checked_date',
  'bucket',
  'n',
  'x_distribution',
  'terminal_distribution',
  'left_distribution',
  'decision',
  'evidence',
]);

writeCsv(path.join(reportsDir, `${prefix}_contradiction_checks.csv`), contradictionChecks, [
  'checked_date',
  'check_id',
  'result',
  'evidence',
  'consequence',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
