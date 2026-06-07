import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const FRAMES = path.join(
  ROOT,
  'data',
  'open_prototype',
  'reports',
  'risky_002390_canonical_branch_selector_forger_20260531_frames.csv',
);
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'campaign_032_002_861_x_tail_ecology_20260531';
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

function csvEscape(value) {
  const text = String(value ?? '');
  return /[",\n\r]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(',')];
  for (const row of rows) lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function countBy(items, fn) {
  const counts = new Map();
  for (const item of items) {
    const key = fn(item);
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()].sort(
    (a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }),
  );
}

function top(counts, n = 8) {
  return counts
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function inferTailStatus(frame) {
  if (frame.tail === '<END>') return 'terminal';
  return 'continuing';
}

function classifyTailEcology({ frameCount, exactTailHits, firstTailHits, globalN, globalExactTailN, topNextShare }) {
  if (!frameCount) return 'no_frame_tail';
  if (!globalN) return 'no_global_successor_pool';
  if (exactTailHits === frameCount) return 'exact_tail_reused_elsewhere';
  if (firstTailHits === frameCount) return 'first_tail_reused_elsewhere';
  if (globalExactTailN > 0) return 'partial_global_tail_match';
  if (topNextShare >= 0.75) return 'formula_locked_tail_risk';
  return 'frame_tail_not_seen_elsewhere';
}

fs.mkdirSync(OUT_DIR, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({
  ...row,
  row_object: objectId(row),
  row_tokens: tokens(row.text),
}));
const rows = [...new Map(rawRows.map((row) => [row.row_tokens.join(' '), row])).values()];
const frameRows = parseCsv(fs.readFileSync(FRAMES, 'utf8'));

const targetFrames = frameRows
  .filter((frame) => frame.branch_class !== 'unclassified')
  .map((frame) => ({
    ...frame,
    frame_tail_tokens: frame.tail === '<END>' ? [] : frame.tail.split(/\s+/).filter(Boolean),
    frame_status: inferTailStatus(frame),
  }));

const branchSet = new Set(targetFrames.map((frame) => frame.branch));
const occurrenceRows = [];

for (const row of rows) {
  row.row_tokens.forEach((sign, idx) => {
    if (!branchSet.has(sign)) return;
    const nextSign = row.row_tokens[idx + 1] ?? '<END>';
    const next2 = row.row_tokens.slice(idx + 1, idx + 3).join(' ') || '<END>';
    const next4 = row.row_tokens.slice(idx + 1, idx + 5).join(' ') || '<END>';
    const inTargetFrame = row.row_tokens[idx - 2] === '002' && row.row_tokens[idx - 1] === '390';
    occurrenceRows.push({
      checked_date: RUN_DATE,
      branch: sign,
      row_id: row.id,
      object: row.row_object,
      site: row.site || 'NA',
      type: row.type || 'NA',
      prev2: row.row_tokens.slice(Math.max(0, idx - 2), idx).join(' ') || '<START>',
      next1: nextSign,
      next2,
      next4,
      terminal: nextSign === '<END>' ? 'true' : 'false',
      in_002390_frame: inTargetFrame ? 'true' : 'false',
      text: row.text,
    });
  });
}

const frameTailRows = [];
const branchRows = [];

for (const branch of [...branchSet].sort()) {
  const frames = targetFrames.filter((frame) => frame.branch === branch);
  const occurrences = occurrenceRows.filter((row) => row.branch === branch && row.in_002390_frame === 'false');
  const allOccurrences = occurrenceRows.filter((row) => row.branch === branch);
  const nextCounts = countBy(occurrences, (row) => row.next1);
  const next2Counts = countBy(occurrences, (row) => row.next2);
  const siteCounts = countBy(allOccurrences, (row) => row.site);
  const globalN = occurrences.length;
  const topNextShare = globalN && nextCounts.length ? nextCounts[0][1] / globalN : 0;
  let exactTailFrameHits = 0;
  let firstTailFrameHits = 0;

  for (const frame of frames) {
    const firstTail = frame.frame_tail_tokens[0] ?? '<END>';
    const exactTail = frame.frame_tail_tokens.join(' ') || '<END>';
    const exactPoolHits = occurrences.filter((row) => row.next4 === exactTail || row.next2 === exactTail || row.next1 === exactTail).length;
    const firstPoolHits = occurrences.filter((row) => row.next1 === firstTail).length;
    if (exactPoolHits > 0) exactTailFrameHits += 1;
    if (firstPoolHits > 0) firstTailFrameHits += 1;
    frameTailRows.push({
      checked_date: RUN_DATE,
      branch,
      branch_class: frame.branch_class,
      frame_object: frame.object,
      frame_row_id: frame.row_id,
      frame_source_bucket: frame.source_bucket,
      frame_tail: exactTail,
      frame_status: frame.frame_status,
      global_nonframe_occurrences: String(globalN),
      exact_tail_seen_nonframe: exactPoolHits > 0 ? 'true' : 'false',
      exact_tail_nonframe_hits: String(exactPoolHits),
      first_tail_seen_nonframe: firstPoolHits > 0 ? 'true' : 'false',
      first_tail_nonframe_hits: String(firstPoolHits),
      top_nonframe_next1: top(nextCounts),
      text: frame.text,
    });
  }

  const terminalFrames = frames.filter((frame) => frame.frame_status === 'terminal').length;
  const continuingFrames = frames.length - terminalFrames;
  const globalTerminal = occurrences.filter((row) => row.terminal === 'true').length;
  const ecology = classifyTailEcology({
    frameCount: frames.length,
    exactTailHits: exactTailFrameHits,
    firstTailHits: firstTailFrameHits,
    globalN,
    globalExactTailN: exactTailFrameHits,
    topNextShare,
  });
  branchRows.push({
    checked_date: RUN_DATE,
    branch,
    branch_class: frames[0]?.branch_class ?? 'NA',
    frame_rows: String(frames.length),
    frame_terminal: String(terminalFrames),
    frame_continuing: String(continuingFrames),
    global_nonframe_occurrences: String(globalN),
    global_nonframe_terminal: String(globalTerminal),
    global_nonframe_terminal_share: globalN ? (globalTerminal / globalN).toFixed(6) : 'NA',
    top_nonframe_next1_share: globalN ? topNextShare.toFixed(6) : 'NA',
    frame_exact_tail_rows_reused: String(exactTailFrameHits),
    frame_first_tail_rows_reused: String(firstTailFrameHits),
    tail_ecology_result: ecology,
    top_nonframe_next1: top(nextCounts),
    top_nonframe_next2: top(next2Counts),
    all_sites: top(siteCounts),
    frame_objects: frames.map((frame) => `${frame.object}:${frame.tail}`).join(';'),
  });
}

const openRows = branchRows.filter((row) => row.branch_class === 'open_continue');
const closedRows = branchRows.filter((row) => row.branch_class === 'close_terminal');
const openTailReuseFrames = frameTailRows.filter(
  (row) => row.frame_status === 'continuing' && row.first_tail_seen_nonframe === 'true' && ['125', '530', '590'].includes(row.branch),
).length;
const openContinuingFrames = frameTailRows.filter(
  (row) => row.frame_status === 'continuing' && ['125', '530', '590'].includes(row.branch),
).length;
const formulaRiskBranches = branchRows.filter((row) => Number(row.top_nonframe_next1_share) >= 0.75);

const decisions = [];
if (openTailReuseFrames === openContinuingFrames && openContinuingFrames > 0) {
  decisions.push('Every open/continuing `002-390-X` frame has a first tail sign that is also seen after the same X outside the frame.');
} else {
  decisions.push('The open/continuing tail-reuse bet is incomplete: at least one open frame tail is not seen after the same X outside the frame.');
}
if (formulaRiskBranches.length) {
  decisions.push(
    `Formula risk is active for ${formulaRiskBranches.map((row) => `${row.branch}:${row.top_nonframe_next1_share}`).join(', ')}; do not promote these as free lexical heads yet.`,
  );
} else {
  decisions.push('No branch has a >=0.75 nonframe top-next share; this weakens a simple formula-lock null.');
}

const summary = {
  checked_date: RUN_DATE,
  status: 'x_tail_ecology_test',
  hypothesis_tested:
    'If X is a branch head in `002-390-X`, then continuing frame tails should reuse X-specific successor ecology outside the target frame more often than a copied-template null predicts.',
  branch_rows: branchRows.length,
  open_continuing_frames: openContinuingFrames,
  open_continuing_frames_with_first_tail_reuse: openTailReuseFrames,
  formula_risk_branches: formulaRiskBranches.map((row) => ({
    branch: row.branch,
    top_nonframe_next1_share: row.top_nonframe_next1_share,
    top_nonframe_next1: row.top_nonframe_next1,
  })),
  decisions,
  confidence_after_test: {
    'X_as_branch_head_not_filler':
      openTailReuseFrames === openContinuingFrames && formulaRiskBranches.length === 0
        ? 'candidate_strengthened'
        : 'candidate_mixed',
    '125_open_title_tail': openRows.find((row) => row.branch === '125')?.tail_ecology_result ?? 'missing',
    '530_open_title_tail': openRows.find((row) => row.branch === '530')?.tail_ecology_result ?? 'missing',
    '590_open_bridge_tail': openRows.find((row) => row.branch === '590')?.tail_ecology_result ?? 'missing',
    'closed_branches_as_frame_governed_closures': closedRows.every((row) => row.frame_continuing === '0')
      ? 'candidate_unchanged'
      : 'demoted',
  },
  falsifier:
    'A new source-bound continuing frame whose X-tail is absent from X successor ecology, or a high-share formula tail that covers the open rows, demotes the branch-head parse toward copied-register template.',
};

writeCsv(path.join(OUT_DIR, `${PREFIX}_branch_summary.csv`), branchRows, [
  'checked_date',
  'branch',
  'branch_class',
  'frame_rows',
  'frame_terminal',
  'frame_continuing',
  'global_nonframe_occurrences',
  'global_nonframe_terminal',
  'global_nonframe_terminal_share',
  'top_nonframe_next1_share',
  'frame_exact_tail_rows_reused',
  'frame_first_tail_rows_reused',
  'tail_ecology_result',
  'top_nonframe_next1',
  'top_nonframe_next2',
  'all_sites',
  'frame_objects',
]);

writeCsv(path.join(OUT_DIR, `${PREFIX}_frame_tail_checks.csv`), frameTailRows, [
  'checked_date',
  'branch',
  'branch_class',
  'frame_object',
  'frame_row_id',
  'frame_source_bucket',
  'frame_tail',
  'frame_status',
  'global_nonframe_occurrences',
  'exact_tail_seen_nonframe',
  'exact_tail_nonframe_hits',
  'first_tail_seen_nonframe',
  'first_tail_nonframe_hits',
  'top_nonframe_next1',
  'text',
]);

writeCsv(path.join(OUT_DIR, `${PREFIX}_occurrences.csv`), occurrenceRows, [
  'checked_date',
  'branch',
  'row_id',
  'object',
  'site',
  'type',
  'prev2',
  'next1',
  'next2',
  'next4',
  'terminal',
  'in_002390_frame',
  'text',
]);

fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
