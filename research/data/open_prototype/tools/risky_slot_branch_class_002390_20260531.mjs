// Tests the bet that the slot after 002-390 sorts branch signs into two
// classes: open branches (125, 530, 590) that continue the text, and closed
// branches (072, 095, 140, 346, 692, 705, 707) that end it. We read the
// filtered corpus metadata, find every 002-390-X frame, and check whether
// each frame's terminal/continuing behavior matches its predicted class.
// Nulls come from several directions: a 100000-iteration Monte Carlo that
// resamples each branch sign's terminality from its behavior outside the
// frame, an exact frame-internal permutation (both with the prespecified
// class and with a post-hoc "any deterministic split" discovery version),
// plus repeated-branch, strict-source, leave-one-site, and matched-
// predecessor slices. Each frame also carries a hand-curated source status
// (strict source-visible, route pressure, or metadata-only). Writes a JSON
// report and four CSVs (bet summary, frames, per-branch table, matched
// predecessors).
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_slot_branch_class_002390_20260531';
const RUN_DATE = '2026-05-31';
const ITERATIONS = 100000;

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

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function norm(value, fallback = 'NA') {
  const text = String(value ?? '').trim();
  return text && text !== '-' && text !== 'None' ? text : fallback;
}

function sourceStatus(object) {
  const strict = new Set(['M-70', 'M-71', 'M-119', 'M-735']);
  const routePressure = new Map([
    ['H-1993', 'source_route_triaged_supplement_only_no_image'],
    ['H-773', 'source_panel_acquired_boxed_window_compatible_token_not_strict'],
    ['Sktd-1', 'checkpoint_permissive_public_panel'],
    ['M-1825', 'm1825_ia_pakistan_absent_secondary_icon_only_no_signband'],
    ['-:4237.1', 'dholavira_8758_cluster_unbound_image_conflict'],
  ]);
  if (strict.has(object)) return 'strict_source_visible';
  return routePressure.get(object) ?? 'metadata_only_unbound';
}

function sourceBucket(status) {
  if (status === 'strict_source_visible') return 'strict';
  if (status === 'metadata_only_unbound') return 'metadata_only';
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

function binomial(n, k) {
  if (k < 0 || k > n) return 0;
  const kk = Math.min(k, n - k);
  let out = 1;
  for (let i = 1; i <= kk; i += 1) out = (out * (n - kk + i)) / i;
  return out;
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

function exactClassScore(frames, continuingIndexes, openBranches) {
  const continuing = new Set(continuingIndexes);
  let score = 0;
  frames.forEach((frame, idx) => {
    const predictedContinuing = openBranches.has(frame.branch);
    if (predictedContinuing === continuing.has(idx)) score += 1;
  });
  return score;
}

function exactInternalP(frames, continuingCount, openBranches) {
  const allCombos = combinations(frames.map((_, idx) => idx), continuingCount);
  const exactHits = allCombos.filter((combo) => exactClassScore(frames, combo, openBranches) === frames.length).length;
  const deterministicHits = allCombos.filter((combo) => bestBranchDeterminismScore(frames, combo) === frames.length).length;
  return {
    combinations: allCombos.length,
    exact_prespecified_class_p: exactHits / allCombos.length,
    branch_determinism_discovery_p: deterministicHits / allCombos.length,
  };
}

function familyKey(row, prev, branch, tail) {
  return [
    norm(row.site),
    norm(row.type),
    norm(row.symbol),
    norm(row.cult),
    norm(row.shape),
    norm(row.material),
    prev,
    branch,
    tail.length ? tail.join(' ') : '<END>',
  ].join('|');
}

const metadata = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const openBranches = new Set(['125', '530', '590']);

const frames = [];
const nonFramePools = new Map();

for (const row of metadata) {
  const signs = row.signs;
  for (let i = 0; i < signs.length; i += 1) {
    const sign = signs[i];
    const terminal = i === signs.length - 1;
    const after002390 = signs[i - 2] === '002' && signs[i - 1] === '390';
    if (after002390) {
      const branch = sign;
      const tail = signs.slice(i + 1);
      const object = objectId(row);
      const status = sourceStatus(object);
      frames.push({
        id: row.id,
        object,
        site: norm(row.site),
        type: norm(row.type),
        symbol: norm(row.symbol),
        cult: norm(row.cult),
        material: norm(row.material),
        shape: norm(row.shape),
        prev: signs[i - 3] ?? '<START>',
        branch,
        tail: tail.length ? tail.join(' ') : '<END>',
        terminal,
        predicted: openBranches.has(branch) ? 'open_continue' : 'close_terminal',
        hit: openBranches.has(branch) ? !terminal : terminal,
        source_status: status,
        source_bucket: sourceBucket(status),
        family_key: familyKey(row, signs[i - 3] ?? '<START>', branch, tail),
        text: row.text,
      });
    } else if (signs[i - 2] !== '002' || signs[i - 1] !== '390') {
      if (!nonFramePools.has(sign)) nonFramePools.set(sign, []);
      nonFramePools.get(sign).push(terminal);
    }
  }
}

const targetBranches = new Set(frames.map((frame) => frame.branch));
const targetFrames = frames.filter((frame) => targetBranches.has(frame.branch));
const continuingCount = targetFrames.filter((frame) => !frame.terminal).length;
const observedHits = targetFrames.filter((frame) => frame.hit).length;
const exactTexts = [...new Map(targetFrames.map((frame) => [frame.text, frame])).values()];
const familyCollapsed = [...new Map(targetFrames.map((frame) => [frame.family_key, frame])).values()];
const branchCollapsed = [...new Map(targetFrames.map((frame) => [frame.branch, frame])).values()];
const repeatedFrames = targetFrames.filter((frame) => targetFrames.filter((other) => other.branch === frame.branch).length > 1);
const repeatedContinuing = repeatedFrames.filter((frame) => !frame.terminal).length;
const strictFrames = targetFrames.filter((frame) => frame.source_bucket === 'strict');
const routedFrames = targetFrames.filter((frame) => frame.source_bucket !== 'metadata_only');
const poolCompleteFrames = targetFrames.filter((frame) => (nonFramePools.get(frame.branch) ?? []).length);
const poolCompleteObservedHits = poolCompleteFrames.filter((frame) => frame.hit).length;

const rand = mulberry32(0x2390530);
let geObserved = 0;
let geRepeated = 0;
let geStrict = 0;
let geRouted = 0;
const missingNonFramePools = [];

for (const frame of targetFrames) {
  const pool = nonFramePools.get(frame.branch) ?? [];
  if (!pool.length) missingNonFramePools.push(frame.branch);
}

for (let iter = 0; iter < ITERATIONS; iter += 1) {
  let score = 0;
  for (const frame of poolCompleteFrames) {
    const sampledTerminal = choose(rand, nonFramePools.get(frame.branch));
    const hit = openBranches.has(frame.branch) ? !sampledTerminal : sampledTerminal;
    if (hit) score += 1;
  }
  if (score >= poolCompleteObservedHits) geObserved += 1;

  let repeatedScore = 0;
  for (const frame of repeatedFrames) {
    const sampledTerminal = choose(rand, nonFramePools.get(frame.branch));
    const hit = openBranches.has(frame.branch) ? !sampledTerminal : sampledTerminal;
    if (hit) repeatedScore += 1;
  }
  if (repeatedScore >= repeatedFrames.length) geRepeated += 1;

  let strictScore = 0;
  for (const frame of strictFrames) {
    const sampledTerminal = choose(rand, nonFramePools.get(frame.branch));
    const hit = openBranches.has(frame.branch) ? !sampledTerminal : sampledTerminal;
    if (hit) strictScore += 1;
  }
  if (strictScore >= strictFrames.length) geStrict += 1;

  let routedScore = 0;
  for (const frame of routedFrames) {
    const sampledTerminal = choose(rand, nonFramePools.get(frame.branch));
    const hit = openBranches.has(frame.branch) ? !sampledTerminal : sampledTerminal;
    if (hit) routedScore += 1;
  }
  if (routedScore >= routedFrames.length) geRouted += 1;
}

const internal = exactInternalP(targetFrames, continuingCount, openBranches);
const repeatedInternal = exactInternalP(repeatedFrames, repeatedContinuing, new Set(['125']));

const byBranch = [...targetBranches].sort().map((branch) => {
  const branchFrames = targetFrames.filter((frame) => frame.branch === branch);
  const pool = nonFramePools.get(branch) ?? [];
  return {
    branch,
    predicted_class: openBranches.has(branch) ? 'open_continue' : 'close_terminal',
    frame_rows: branchFrames.length,
    frame_terminal: branchFrames.filter((frame) => frame.terminal).length,
    frame_continuing: branchFrames.filter((frame) => !frame.terminal).length,
    frame_hits: branchFrames.filter((frame) => frame.hit).length,
    nonframe_pool: pool.length,
    nonframe_terminal: pool.filter(Boolean).length,
    nonframe_continuing: pool.filter((value) => !value).length,
    objects: branchFrames.map((frame) => frame.object).join(';'),
  };
});

const bySourceBucket = ['strict', 'route_pressure', 'metadata_only'].map((bucket) => {
  const bucketFrames = targetFrames.filter((frame) => frame.source_bucket === bucket);
  return {
    bucket,
    rows: bucketFrames.length,
    hits: bucketFrames.filter((frame) => frame.hit).length,
    objects: bucketFrames.map((frame) => `${frame.object}:${frame.branch}:${frame.terminal ? 'terminal' : 'continuing'}`).join(';'),
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

const matchedPrev = [...new Set(targetFrames.map((frame) => frame.prev))].sort()
  .map((prev) => {
    const group = targetFrames.filter((frame) => frame.prev === prev);
    return {
      prev_before_002: prev,
      rows: group.length,
      branches: [...new Set(group.map((frame) => frame.branch))].join(';'),
      terminal_pattern: group.map((frame) => `${frame.object}:${frame.branch}:${frame.terminal ? 'terminal' : 'continuing'}:${frame.source_bucket}`).join('|'),
      hits: group.filter((frame) => frame.hit).length,
      contrastive: new Set(group.map((frame) => frame.branch)).size > 1 && new Set(group.map((frame) => frame.terminal)).size > 1,
    };
  })
  .filter((group) => group.rows > 1);

const tier = geObserved / ITERATIONS <= 0.01 && internal.branch_determinism_discovery_p <= 0.05 ? 'candidate' : 'wild shot';

const bet = {
  run_date: RUN_DATE,
  bet_id: 'V2_SLOT_002390_OPEN_CLOSED_BRANCH_CLASS_20260531',
  vector: 'V2 effective-unicity / slot grammar',
  confidence_tier: tier,
  risky_bet: '`002-390-X` is a branch-class slot. `125/530/590` are open continuation branches; `072/095/140/346/692/705/707` are closed terminal branches.',
  observed: `${observedHits}/${targetFrames.length} rows fit; non-frame-pool-complete subset ${poolCompleteObservedHits}/${poolCompleteFrames.length}; exact-text collapse ${exactTexts.filter((frame) => frame.hit).length}/${exactTexts.length}; family-cell collapse ${familyCollapsed.filter((frame) => frame.hit).length}/${familyCollapsed.length}; branch collapse ${branchCollapsed.filter((frame) => frame.hit).length}/${branchCollapsed.length}; repeated-branch rows ${repeatedFrames.filter((frame) => frame.hit).length}/${repeatedFrames.length}; strict-source-visible slice ${strictFrames.filter((frame) => frame.hit).length}/${strictFrames.length}; route-pressure-or-strict slice ${routedFrames.filter((frame) => frame.hit).length}/${routedFrames.length}.`,
  adversarial_test: `Sign-specific non-frame terminality Monte Carlo on pool-complete branches only (${ITERATIONS}); frame-internal terminal-label permutation with prespecified class; post-hoc branch-determinism discovery null; repeated-branch collapse; leave-one-site and matched-predecessor checks.`,
  false_positive_rate: geObserved / ITERATIONS,
  repeated_branch_false_positive_rate: geRepeated / ITERATIONS,
  strict_source_false_positive_rate: geStrict / ITERATIONS,
  route_or_strict_false_positive_rate: geRouted / ITERATIONS,
  frame_internal_prespecified_class_p: internal.exact_prespecified_class_p,
  frame_internal_branch_determinism_discovery_p: internal.branch_determinism_discovery_p,
  repeated_internal_prespecified_class_p: repeatedInternal.exact_prespecified_class_p,
  repeated_internal_branch_determinism_discovery_p: repeatedInternal.branch_determinism_discovery_p,
  missing_nonframe_pools: [...new Set(missingNonFramePools)].join(';'),
  falsifier: 'Any source-bound terminal `002-390-125/530/590`, any source-bound continuing `002-390-072/095/140/346/692/705/707`, or a future branch sign that mixes terminal and continuing behavior within this fixed frame demotes the class rule.',
  next_prediction: 'H-773 should remain continuing if fully source-normalized as `002-390-530-741`; 3335.1 should remain continuing if identified as `002-390-590-032`; a new `002-390-125/530/590` row should carry tail material, while a new `002-390-095/692/705` row should close.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({
    ...bet,
    frame_rows: targetFrames,
    by_branch: byBranch,
    by_source_bucket: bySourceBucket,
    leave_one_site: leaveOneSite,
    matched_predecessor_groups: matchedPrev,
  }, null, 2),
);
writeCsv(path.join(OUT_DIR, `${PREFIX}.csv`), [bet], [
  'run_date',
  'bet_id',
  'vector',
  'confidence_tier',
  'risky_bet',
  'observed',
  'adversarial_test',
  'false_positive_rate',
  'repeated_branch_false_positive_rate',
  'strict_source_false_positive_rate',
  'route_or_strict_false_positive_rate',
  'frame_internal_prespecified_class_p',
  'frame_internal_branch_determinism_discovery_p',
  'repeated_internal_prespecified_class_p',
  'repeated_internal_branch_determinism_discovery_p',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_frames.csv`), targetFrames, [
  'id',
  'object',
  'site',
  'type',
  'symbol',
  'cult',
  'material',
  'shape',
  'prev',
  'branch',
  'tail',
  'terminal',
  'predicted',
  'hit',
  'source_status',
  'source_bucket',
  'family_key',
  'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_by_branch.csv`), byBranch, [
  'branch',
  'predicted_class',
  'frame_rows',
  'frame_terminal',
  'frame_continuing',
  'frame_hits',
  'nonframe_pool',
  'nonframe_terminal',
  'nonframe_continuing',
  'objects',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_matched_predecessors.csv`), matchedPrev, [
  'prev_before_002',
  'rows',
  'branches',
  'terminal_pattern',
  'hits',
  'contrastive',
]);

console.log(JSON.stringify(bet, null, 2));
