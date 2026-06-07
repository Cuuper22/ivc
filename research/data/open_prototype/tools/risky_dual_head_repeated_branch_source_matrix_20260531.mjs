import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const HEADS = path.join(ROOT, 'data', 'open_prototype', 'reports', 'risky_002_dual_head_branch_tables_20260531_heads.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_dual_head_repeated_branch_source_matrix_20260531';
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

function writeCsv(file, rows, fields) {
  const esc = (value) => {
    const text = String(value ?? '');
    return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
  };
  const body = rows.map((row) => fields.map((field) => esc(row[field])).join(',')).join('\n');
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`);
}

function parseClasses(text) {
  return String(text ?? '').split(';').filter(Boolean).map((entry) => {
    const [branch, branch_class, count] = entry.split(':');
    return { branch, branch_class, count: Number(count) };
  });
}

const sourceStatus = new Map([
  ['861|416', { status: 'not_source_stable_yet', evidence: 'repeated Harappa TAB:I formula +002-861-416; exact text collapses to one family; no current strict source-token proof in this branch-table artifact', action: 'source-normalize one H-2094/H-2097/H-910 panel and check terminal closure' }],
  ['861|096', { status: 'not_source_stable_yet', evidence: 'two Mohenjo-daro ivory rod rows M-2089/M-2090; no current strict token/source adjudication here', action: 'bind rod images and check both remain terminal 002-861-096' }],
  ['861|603', { status: 'source_visible_pressure', evidence: 'M-240/M-714/M-1273 have prior public source-visible attachment pressure as terminal post-861 rows', action: 'tighten token boundary; any 603 row with extra tail material breaks closure class' }],
  ['861|698', { status: 'not_source_stable_yet', evidence: 'M-329/M-330 exact pair; no strict source-token proof in current matrix', action: 'source-bind pair or demote exact-pair pressure' }],
  ['861|533', { status: 'source_visible_pressure', evidence: 'M-376/M-391 are the accepted restricted-tail structural witnesses; here they function as open branch 533 followed by 717', action: 'guard that 533-717 remains a two-token open-tail class, not a single terminal branch' }],
  ['861|000', { status: 'not_source_stable_yet', evidence: 'Ad-8 and Shikarpur row differ by site/object; no strict source-token proof here', action: 'source-bind either row; any continuation after 000 breaks closure class' }],
  ['390|125', { status: 'partial_strict_source_pressure', evidence: 'M-119 and M-735 are strict source-visible pressure; M-38 weak, Sktd-1 panel-bound; all four continue', action: 'token-box M-119/M-735 and keep Sktd-1 out of strict count until side/order stable' }],
  ['390|095', { status: 'partial_strict_source_pressure', evidence: 'M-71 strict source-visible; H-1993 route-only; both terminal in metadata', action: 'H-1993 source image is the promotion gate; a continuing H-1993 kills closure class' }],
  ['390|705', { status: 'not_source_stable_yet', evidence: 'M-1825 and Dholavira 4237.1 remain source-gated; both terminal in metadata', action: 'source-bind either repeated 705 row; any tail material kills closure class' }],
]);

const headRows = parseCsv(fs.readFileSync(HEADS, 'utf8')).filter((row) => row.head === '861' || row.head === '390');
const repeated = [];
for (const head of headRows) {
  for (const branch of parseClasses(head.branch_classes).filter((entry) => entry.count > 1)) {
    const key = `${head.head}|${branch.branch}`;
    const src = sourceStatus.get(key) ?? { status: 'unclassified_source_gap', evidence: 'no current source-status classification', action: 'classify before promotion' };
    repeated.push({
      run_date: RUN_DATE,
      head: head.head,
      branch: branch.branch,
      branch_class: branch.branch_class,
      exact_text_count: branch.count,
      source_status: src.status,
      evidence: src.evidence,
      promotion_or_kill_action: src.action,
    });
  }
}

const sourcePressure = repeated.filter((row) => ['source_visible_pressure', 'partial_strict_source_pressure'].includes(row.source_status)).length;
const stillGated = repeated.length - sourcePressure;
const bet = {
  run_date: RUN_DATE,
  bet_id: 'V2_DUAL_HEAD_REPEATED_BRANCH_SOURCE_STABILITY_20260531',
  vector: 'V2 effective-unicity / slot grammar',
  confidence_tier: 'candidate',
  risky_bet: 'The dual branch-table bet should survive first on repeated branches, not singleton branches. Repeated `861` and `390` branches are the source-stability battleground.',
  observed: `Exact-text repeated branch classes tested: ${repeated.length}. Current source-pressure rows: ${sourcePressure}; still source-gated: ${stillGated}. Highest-value repeated-branch kill gates are 390|705, 861|000, and 861|096; raw-repeat-only 861|416 and 861|698 are duplicate-family checks, not exact-text repeated branches.`,
  adversarial_test: 'Collapse to repeated branch classes only, then mark which branches already have source-visible pressure versus which are still catalog-mediated. Promotion is forbidden until repeated classes source-bind without mixed terminality.',
  falsifier: 'Any exact-text repeated branch class that becomes mixed under source-normalized token order breaks the dual-head table. The fastest kills are terminal-with-tail for 390|705 or continuation after 861|000/096; raw-repeat-only 861|416/698 can only kill duplicate-family support unless a second exact-text family appears.',
  next_prediction: '`390|125`, `390|095`, `861|603`, and `861|533` should survive stricter source review; the source-gated repeated branches should not introduce mixed behavior.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), JSON.stringify({ ...bet, repeated_branches: repeated }, null, 2));
writeCsv(path.join(OUT_DIR, `${PREFIX}.csv`), [bet], [
  'run_date',
  'bet_id',
  'vector',
  'confidence_tier',
  'risky_bet',
  'observed',
  'adversarial_test',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_branches.csv`), repeated, [
  'run_date',
  'head',
  'branch',
  'branch_class',
  'exact_text_count',
  'source_status',
  'evidence',
  'promotion_or_kill_action',
]);
console.log(JSON.stringify(bet, null, 2));
