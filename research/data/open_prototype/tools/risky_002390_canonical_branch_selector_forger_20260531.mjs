// Stress-tests a pre-specified branch table for the `002-390-X` frame: branches
// 125/530/590 are claimed to be "open" (the text continues after X) and
// 072/095/140/346/692/705/707 "closed" (the text ends at X). The script reads
// metadata_filtered.csv, collapses duplicate sign sequences, extracts every sign X
// that follows `002-390`, and checks how many frames the table predicts correctly.
// Three nulls attack the claim. First, a 100,000-iteration forger replaces each
// frame's terminal label with one sampled from the same sign's behavior outside the
// frame — this prices the chance that each branch just carries its ordinary
// terminality into the frame. Second, an exact frame-internal permutation of
// terminal labels prices both the pre-specified table and any branch-deterministic
// table a data-dredger could have discovered. Third, leave-one-site and
// matched-predecessor tables check the pattern is not one site's or one template's
// artifact. Each frame is also tagged by how well its reading is source-verified
// (strict image, route pressure, or metadata only). Writes a bet summary
// (JSON + CSV) plus frame, per-branch, and matched-predecessor CSVs to reports/.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_002390_canonical_branch_selector_forger_20260531';
const RUN_DATE = '2026-05-31';
const ITERATIONS = 100000;

const OPEN_BRANCHES = new Set(['125', '530', '590']);
const CLOSED_BRANCHES = new Set(['072', '095', '140', '346', '692', '705', '707']);

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
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`, 'utf8');
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function norm(value, fallback = 'NA') {
  const text = String(value ?? '').trim();
  return text && text !== '-' && text !== 'None' ? text : fallback;
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function sourceStatus(object) {
  const strict = new Set(['M-70', 'M-71', 'M-119', 'M-735']);
  const routePressure = new Map([
    ['H-1993', 'route_pressure_supplement_row_no_strict_image'],
    ['H-773', 'route_pressure_panel_compatible_not_strict'],
    ['Sktd-1', 'route_pressure_public_panel_order_not_strict'],
    ['M-1825', 'route_pressure_secondary_icon_only_no_signband'],
    ['-:4237.1', 'route_pressure_dholavira_cluster_unbound'],
  ]);
  if (strict.has(object)) return 'strict_source_visible';
  return routePressure.get(object) ?? 'metadata_only';
}

function sourceBucket(status) {
  if (status === 'strict_source_visible') return 'strict';
  if (status === 'metadata_only') return 'metadata_only';
  return 'route_pressure';
}

function mulberry32(seed) {
  return function rand() {
    let t = (seed += 0x6D2B79F5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function choose(rand, arr) {
  return arr[Math.floor(rand() * arr.length)];
}

function combinations(items, k) {
  const out = [];
  const combo = [];
  function rec(start) {
    if (combo.length === k) {
      out.push([...combo]);
      return;
    }
    for (let i = start; i <= items.length - (k - combo.length); i += 1) {
      combo.push(items[i]);
      rec(i + 1);
      combo.pop();
    }
  }
  rec(0);
  return out;
}

function exactClassScore(frames, continuingIndexes, openBranches) {
  const continuing = new Set(continuingIndexes);
  return frames.filter((frame, idx) => openBranches.has(frame.branch) === continuing.has(idx)).length;
}

function bestBranchDeterminismScore(frames, continuingIndexes) {
  const continuing = new Set(continuingIndexes);
  const byBranch = new Map();
  frames.forEach((frame, idx) => {
    if (!byBranch.has(frame.branch)) byBranch.set(frame.branch, []);
    byBranch.get(frame.branch).push(continuing.has(idx));
  });
  let score = 0;
  for (const labels of byBranch.values()) {
    const cont = labels.filter(Boolean).length;
    score += Math.max(cont, labels.length - cont);
  }
  return score;
}

function internalPermutationP(frames, openBranches) {
  const continuingCount = frames.filter((frame) => !frame.terminal).length;
  const combos = combinations(frames.map((_, idx) => idx), continuingCount);
  const exactHits = combos.filter((combo) => exactClassScore(frames, combo, openBranches) === frames.length).length;
  const deterministicHits = combos.filter((combo) => bestBranchDeterminismScore(frames, combo) === frames.length).length;
  return {
    combinations: combos.length,
    prespecified_class_p: exactHits / combos.length,
    branch_determinism_discovery_p: deterministicHits / combos.length,
  };
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()];

const frames = [];
const nonFrameTerminalPools = new Map();

for (const row of canonicalRows) {
  const signs = row.signs;
  signs.forEach((sign, idx) => {
    const after002390 = signs[idx - 2] === '002' && signs[idx - 1] === '390';
    const terminal = idx === signs.length - 1;
    if (after002390) {
      const branch = sign;
      const tail = signs.slice(idx + 1);
      const object = objectId(row);
      const status = sourceStatus(object);
      frames.push({
        row_id: row.id,
        object,
        site: norm(row.site),
        type: norm(row.type),
        symbol: norm(row.symbol),
        cult: norm(row.cult),
        material: norm(row.material),
        shape: norm(row.shape),
        prev_before_002: signs[idx - 3] ?? '<START>',
        branch,
        branch_class: OPEN_BRANCHES.has(branch) ? 'open_continue' : CLOSED_BRANCHES.has(branch) ? 'close_terminal' : 'unclassified',
        tail: tail.length ? tail.join(' ') : '<END>',
        terminal,
        hit: OPEN_BRANCHES.has(branch) ? !terminal : terminal,
        source_status: status,
        source_bucket: sourceBucket(status),
        exact_sequence: signs.join(' '),
        text: row.text,
      });
    } else if (sign !== '002' && sign !== '390') {
      if (!nonFrameTerminalPools.has(sign)) nonFrameTerminalPools.set(sign, []);
      nonFrameTerminalPools.get(sign).push(terminal);
    }
  });
}

const targetFrames = frames.filter((frame) => frame.branch_class !== 'unclassified');
const repeatedFrames = targetFrames.filter((frame) => targetFrames.filter((other) => other.branch === frame.branch).length > 1);
const poolComplete = targetFrames.filter((frame) => (nonFrameTerminalPools.get(frame.branch) ?? []).length);
const strictFrames = targetFrames.filter((frame) => frame.source_bucket === 'strict');
const routedFrames = targetFrames.filter((frame) => frame.source_bucket !== 'metadata_only');

const rand = mulberry32(0x2390125);
let gePoolComplete = 0;
let geRepeated = 0;
let geRouted = 0;
for (let iter = 0; iter < ITERATIONS; iter += 1) {
  const score = (set) => set.filter((frame) => {
    const sampledTerminal = choose(rand, nonFrameTerminalPools.get(frame.branch));
    return OPEN_BRANCHES.has(frame.branch) ? !sampledTerminal : sampledTerminal;
  }).length;
  if (score(poolComplete) >= poolComplete.length) gePoolComplete += 1;
  if (score(repeatedFrames) >= repeatedFrames.length) geRepeated += 1;
  if (score(routedFrames) >= routedFrames.length) geRouted += 1;
}

const internalAll = internalPermutationP(targetFrames, OPEN_BRANCHES);
const internalRepeated = internalPermutationP(repeatedFrames, new Set(['125']));

const byBranch = [...new Set(targetFrames.map((frame) => frame.branch))].sort().map((branch) => {
  const group = targetFrames.filter((frame) => frame.branch === branch);
  const pool = nonFrameTerminalPools.get(branch) ?? [];
  return {
    branch,
    class: OPEN_BRANCHES.has(branch) ? 'open_continue' : 'close_terminal',
    frame_rows: group.length,
    frame_terminal: group.filter((frame) => frame.terminal).length,
    frame_continuing: group.filter((frame) => !frame.terminal).length,
    nonframe_pool: pool.length,
    nonframe_terminal: pool.filter(Boolean).length,
    nonframe_continuing: pool.filter((value) => !value).length,
    sites: [...new Set(group.map((frame) => frame.site))].join(';'),
    objects: group.map((frame) => `${frame.object}:${frame.terminal ? 'T' : 'C'}`).join(';'),
  };
});

const leaveOneSite = [...new Set(targetFrames.map((frame) => frame.site))].sort().map((site) => {
  const kept = targetFrames.filter((frame) => frame.site !== site);
  return {
    left_out_site: site,
    kept_rows: kept.length,
    kept_hits: kept.filter((frame) => frame.hit).length,
  };
});

const matchedPredecessors = [...new Set(targetFrames.map((frame) => frame.prev_before_002))].sort()
  .map((prev) => {
    const group = targetFrames.filter((frame) => frame.prev_before_002 === prev);
    return {
      prev_before_002: prev,
      rows: group.length,
      branches: [...new Set(group.map((frame) => frame.branch))].join(';'),
      terminal_pattern: group.map((frame) => `${frame.object}:${frame.branch}:${frame.terminal ? 'T' : 'C'}:${frame.source_bucket}`).join('|'),
      contrastive: new Set(group.map((frame) => frame.branch)).size > 1 && new Set(group.map((frame) => frame.terminal)).size > 1,
    };
  })
  .filter((group) => group.rows > 1);

const tier =
  gePoolComplete / ITERATIONS <= 0.01 &&
  geRepeated / ITERATIONS <= 0.01 &&
  internalAll.branch_determinism_discovery_p <= 0.05
    ? 'candidate'
    : 'wild shot';

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V2_SLOT_002390_CANONICAL_BRANCH_SELECTOR_20260531',
  vector: 'V2 effective-unicity / slot grammar',
  confidence_tier: tier,
  risky_bet:
    '`002-390-X` is a canonical branch-selector frame. `125/530/590` select continuation, while `072/095/140/346/692/705/707` select closure.',
  observed:
    `Canonical rows=${canonicalRows.length}; target frames=${targetFrames.length}; hits=${targetFrames.filter((frame) => frame.hit).length}/${targetFrames.length}; ` +
    `repeated branch hits=${repeatedFrames.filter((frame) => frame.hit).length}/${repeatedFrames.length}; route-or-strict hits=${routedFrames.filter((frame) => frame.hit).length}/${routedFrames.length}; ` +
    `strict hits=${strictFrames.filter((frame) => frame.hit).length}/${strictFrames.length}.`,
  adversarial_test:
    `Canonical numeric-sequence collapse, sign-specific non-frame terminality forger (${ITERATIONS}), repeated-branch-only forger, frame-internal terminal-label permutation, leave-one-site and matched-predecessor stress.`,
  false_positive_rate: gePoolComplete / ITERATIONS,
  repeated_branch_false_positive_rate: geRepeated / ITERATIONS,
  route_or_strict_false_positive_rate: geRouted / ITERATIONS,
  frame_internal_prespecified_class_p: internalAll.prespecified_class_p,
  frame_internal_branch_determinism_discovery_p: internalAll.branch_determinism_discovery_p,
  repeated_internal_prespecified_class_p: internalRepeated.prespecified_class_p,
  repeated_internal_branch_determinism_discovery_p: internalRepeated.branch_determinism_discovery_p,
  branch_table:
    '`125/530/590` continue; `072/095/140/346/692/705/707` close. The strongest governed reversals are `095` and `705`: both are mostly nonterminal outside this frame but terminal after `002-390`.',
  falsifier:
    'Any source-bound terminal `002-390-125/530/590`, source-bound continuing `002-390-072/095/140/346/692/705/707`, or source-normalized canonical collapse that mixes a repeated branch demotes the bet.',
  next_prediction:
    'New `002-390-125/530/590` rows should carry at least one tail sign; new `002-390-095/692/705` rows should close. H-773 should remain continuing if its `530-741` reading is strict-source confirmed.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({ ...summary, frames: targetFrames, by_branch: byBranch, leave_one_site: leaveOneSite, matched_predecessors: matchedPredecessors }, null, 2),
  'utf8',
);
writeCsv(path.join(OUT_DIR, `${PREFIX}.csv`), [summary], [
  'run_date',
  'bet_id',
  'vector',
  'confidence_tier',
  'risky_bet',
  'observed',
  'adversarial_test',
  'false_positive_rate',
  'repeated_branch_false_positive_rate',
  'route_or_strict_false_positive_rate',
  'frame_internal_prespecified_class_p',
  'frame_internal_branch_determinism_discovery_p',
  'repeated_internal_prespecified_class_p',
  'repeated_internal_branch_determinism_discovery_p',
  'branch_table',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_frames.csv`), targetFrames, [
  'row_id',
  'object',
  'site',
  'type',
  'symbol',
  'cult',
  'material',
  'shape',
  'prev_before_002',
  'branch',
  'branch_class',
  'tail',
  'terminal',
  'hit',
  'source_status',
  'source_bucket',
  'exact_sequence',
  'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_by_branch.csv`), byBranch, [
  'branch',
  'class',
  'frame_rows',
  'frame_terminal',
  'frame_continuing',
  'nonframe_pool',
  'nonframe_terminal',
  'nonframe_continuing',
  'sites',
  'objects',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_matched_predecessors.csv`), matchedPredecessors, [
  'prev_before_002',
  'rows',
  'branches',
  'terminal_pattern',
  'contrastive',
]);

console.log(JSON.stringify(summary, null, 2));
