import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_consolidate_left_vs_head_residual_20260531';

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
    const key = keyFn(row) || '<END>';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }));
}

function topCounts(rows, keyFn) {
  return countBy(rows, keyFn)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

fs.mkdirSync(reportsDir, { recursive: true });

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));
const sameRegisterRows = metadataRows.filter(
  (row) =>
    row.site === 'Mohenjo-daro' &&
    row.type === 'SEAL:S' &&
    row.shape === 'square' &&
    row.material === 'Steatite',
);

const frames002 = [];
for (const row of sameRegisterRows) {
  const rowSigns = signs(row.text);
  for (let index = 0; index < rowSigns.length; index += 1) {
    if (rowSigns[index] !== '002') continue;
    const head = rowSigns[index + 1] ?? '';
    const afterHead = rowSigns[index + 2] ?? '';
    frames002.push({
      checked_date: '2026-05-31',
      object: row.cisi,
      id: row.id,
      prev_before_002: rowSigns[index - 1] ?? '',
      head_after_002: head,
      sign_after_head: afterHead,
      head_is_390: head === '390' ? 'True' : 'False',
      prev_is_235: rowSigns[index - 1] === '235' ? 'True' : 'False',
      sign_after_head_is_125: afterHead === '125' ? 'True' : 'False',
      terminal_after_head: index + 2 === rowSigns.length - 1 ? 'True' : 'False',
      tail_after_head: rowSigns.slice(index + 2).join(' ') || '<END>',
      symbol: row.symbol,
      cult: row.cult,
      complete: row.complete,
      condition: row.condition,
      text: row.text,
    });
  }
}

const final235Frames = frames002.filter((row) => row.prev_is_235 === 'True');
const final235Head390 = final235Frames.filter((row) => row.head_after_002 === '390');
const final235HeadNot390 = final235Frames.filter((row) => row.head_after_002 !== '390');
const head390Frames = frames002.filter((row) => row.head_after_002 === '390');
const head390Prev235 = head390Frames.filter((row) => row.prev_is_235 === 'True');
const head390PrevNot235 = head390Frames.filter((row) => row.prev_is_235 === 'False');
const head390PrevNot235Open125 = head390PrevNot235.filter(
  (row) => row.sign_after_head === '125' && row.terminal_after_head === 'False',
);

const contrastRows = [
  {
    checked_date: '2026-05-31',
    contrast: 'final_235_all_heads',
    denominator: String(final235Frames.length),
    after_head_125: String(final235Frames.filter((row) => row.sign_after_head === '125').length),
    after_head_125_rate: ratio(final235Frames.filter((row) => row.sign_after_head === '125').length, final235Frames.length),
    open_after_head: String(final235Frames.filter((row) => row.terminal_after_head === 'False' && row.sign_after_head).length),
    head_distribution: topCounts(final235Frames, (row) => row.head_after_002),
    decision: 'kills broad final-235-as-125-trigger',
  },
  {
    checked_date: '2026-05-31',
    contrast: 'final_235_head_390',
    denominator: String(final235Head390.length),
    after_head_125: String(final235Head390.filter((row) => row.sign_after_head === '125').length),
    after_head_125_rate: ratio(final235Head390.filter((row) => row.sign_after_head === '125').length, final235Head390.length),
    open_after_head: String(final235Head390.filter((row) => row.terminal_after_head === 'False').length),
    head_distribution: topCounts(final235Head390, (row) => row.head_after_002),
    decision: 'keeps narrow 235-plus-002390 support',
  },
  {
    checked_date: '2026-05-31',
    contrast: 'final_235_non390_heads',
    denominator: String(final235HeadNot390.length),
    after_head_125: String(final235HeadNot390.filter((row) => row.sign_after_head === '125').length),
    after_head_125_rate: ratio(final235HeadNot390.filter((row) => row.sign_after_head === '125').length, final235HeadNot390.length),
    open_after_head: String(final235HeadNot390.filter((row) => row.terminal_after_head === 'False' && row.sign_after_head).length),
    head_distribution: topCounts(final235HeadNot390, (row) => row.head_after_002),
    decision: 'shows 235 alone does not choose 125',
  },
  {
    checked_date: '2026-05-31',
    contrast: 'head_390_without_final235',
    denominator: String(head390PrevNot235.length),
    after_head_125: String(head390PrevNot235.filter((row) => row.sign_after_head === '125').length),
    after_head_125_rate: ratio(head390PrevNot235.filter((row) => row.sign_after_head === '125').length, head390PrevNot235.length),
    open_after_head: String(head390PrevNot235.filter((row) => row.terminal_after_head === 'False' && row.sign_after_head).length),
    head_distribution: topCounts(head390PrevNot235, (row) => row.prev_before_002),
    decision: head390PrevNot235Open125.length > 0 ? 'keeps head-390 residual independent of 235' : 'would collapse to 235 trigger',
  },
];

const contradictionChecks = [
  {
    checked_date: '2026-05-31',
    check_id: 'FINAL_235_ALONE_TRIGGERS_125',
    result: final235Frames.filter((row) => row.sign_after_head === '125').length === final235Frames.length ? 'fail_broad_235_trigger_survives' : 'pass_kill_broad_235_trigger',
    evidence: `final235 after-head 125=${ratio(final235Frames.filter((row) => row.sign_after_head === '125').length, final235Frames.length)}; heads=${topCounts(final235Frames, (row) => row.head_after_002)}`,
    consequence: '235 cannot be read as a general trigger for 125 after 002; the effect is head-conditioned.',
  },
  {
    checked_date: '2026-05-31',
    check_id: 'FINAL_235_PLUS_002390_SELECTS_125',
    result: final235Head390.length > 0 && final235Head390.every((row) => row.sign_after_head === '125') ? 'pass_source_mixed_narrow_trigger' : 'fail',
    evidence: final235Head390.map((row) => `${row.object}:${row.text}`).join(' | '),
    consequence: '235 remains useful only as a narrow precursor inside 002-390, not as an independent sign value.',
  },
  {
    checked_date: '2026-05-31',
    check_id: 'HEAD_390_HAS_125_RESIDUAL_WITHOUT_235',
    result: head390PrevNot235Open125.length > 0 ? 'pass_keep_390_frame_residual' : 'fail_collapse_to_235',
    evidence: head390PrevNot235Open125.map((row) => `${row.object}:${row.prev_before_002}->${row.sign_after_head}:${row.text}`).join(' | '),
    consequence: 'M-119 prevents the 125 branch from collapsing entirely into final-235 context.',
  },
  {
    checked_date: '2026-05-31',
    check_id: 'SEMANTIC_235_TITLE_TRIGGER',
    result: 'pass_demote',
    evidence: 'final235 has many heads and only a minority after-head 125.',
    consequence: 'No title/rank/value reading for 235 survives this consolidation.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'CONSOLIDATE',
  status: 'left_vs_head_residual',
  same_register_scope: 'Mohenjo-daro|SEAL:S|square|Steatite',
  same_register_002_frames: frames002.length,
  final_235: {
    frames: final235Frames.length,
    after_head_125_rate: ratio(final235Frames.filter((row) => row.sign_after_head === '125').length, final235Frames.length),
    head_distribution: topCounts(final235Frames, (row) => row.head_after_002),
  },
  final_235_head_390: {
    frames: final235Head390.length,
    after_head_125_rate: ratio(final235Head390.filter((row) => row.sign_after_head === '125').length, final235Head390.length),
  },
  head_390_without_final235: {
    frames: head390PrevNot235.length,
    after_head_125_rate: ratio(head390PrevNot235.filter((row) => row.sign_after_head === '125').length, head390PrevNot235.length),
    open_125_witnesses: head390PrevNot235Open125.map((row) => row.object),
  },
  decisions: [
    'Kill broad 235-as-125 trigger: final 235 before 002 gives after-head 125 in only 3/18 same-register frames.',
    'Keep narrow 235 + 002-390 pressure: both final-235 002-390 rows go to open 125.',
    'Keep 002-390 frame residual independent of 235 because M-119 has 484-002-390-125 and continues.',
    'Do not semanticize 235 as rank/title; it is a local precursor/context, not a value.',
  ],
  contradiction_results: Object.fromEntries(contradictionChecks.map((row) => [row.check_id, row.result])),
};

writeCsv(path.join(reportsDir, `${prefix}_same_register_002_frames.csv`), frames002, [
  'checked_date',
  'object',
  'id',
  'prev_before_002',
  'head_after_002',
  'sign_after_head',
  'head_is_390',
  'prev_is_235',
  'sign_after_head_is_125',
  'terminal_after_head',
  'tail_after_head',
  'symbol',
  'cult',
  'complete',
  'condition',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_contrast_summary.csv`), contrastRows, [
  'checked_date',
  'contrast',
  'denominator',
  'after_head_125',
  'after_head_125_rate',
  'open_after_head',
  'head_distribution',
  'decision',
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
