import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

// A permutation test: how easily could chance forge the branch-125 pattern we observe after
// 002-390? The observed event is specific — a branch with at least 4 rows, at least 2 of
// them strict source-visible, and zero terminal rows (every row continues). This script
// reads the source-normalized contrast rows CSV from reports/, computes that event on the
// real branch labels, then reshuffles the branch labels 50,000 times under five null models
// of increasing harshness: freely across all rows, within terminal/continuing strata, within
// source-visibility strata, within site|type cells, and within site|type|terminal cells
// (each null preserves more of the real structure, so it is harder to fool). For each null
// it reports the share of shuffles that reproduce the event — an empirical false-positive
// rate. Randomness is seeded from a fixed string, so reruns are identical. The verdict
// stays "candidate_live_not_accepted": the harsh nulls and the register overlap of the
// strict pair (M-119/M-735) block acceptance. Writes observed branch stats and null-model
// rates as CSVs plus a summary JSON (with input SHA-256) to reports/.

const ROOT = process.cwd();
const REPORTS = path.join(ROOT, 'data', 'open_prototype', 'reports');
const ROWS_CSV = path.join(REPORTS, 'campaign_032_002_861_002390x_source_normalized_contrast_rows.csv');
const OUT_PREFIX = 'campaign_032_002_861_002390x_replacement_branch_forger';
const OUT_CSV = path.join(REPORTS, `${OUT_PREFIX}_nulls.csv`);
const OUT_BRANCH_CSV = path.join(REPORTS, `${OUT_PREFIX}_observed_branches.csv`);
const OUT_JSON = path.join(REPORTS, `${OUT_PREFIX}_summary.json`);

const ITERATIONS = 50000;
const TARGET_BRANCH = '125';

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
      rows.push(row);
      row = [];
      cell = '';
    } else {
      cell += ch;
    }
  }
  if (cell.length || row.length) {
    row.push(cell.replace(/\r$/, ''));
    rows.push(row);
  }
  if (!rows.length) return [];
  const header = rows[0];
  return rows.slice(1).filter((r) => r.some((v) => v !== '')).map((r) => {
    const out = {};
    header.forEach((h, i) => {
      out[h] = r[i] ?? '';
    });
    return out;
  });
}

function csvEscape(value) {
  const text = String(value ?? '');
  if (/[",\n\r]/.test(text)) return `"${text.replaceAll('"', '""')}"`;
  return text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(',')];
  for (const row of rows) lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function seededRandom(seedText) {
  let state = crypto.createHash('sha256').update(seedText).digest().readUInt32LE(0);
  return () => {
    state = (state * 1664525 + 1013904223) >>> 0;
    return state / 2 ** 32;
  };
}

function shuffle(values, rand) {
  const out = [...values];
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function groupBy(rows, keyFn) {
  const groups = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(row);
  }
  return groups;
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `${row.site}:${row.id}`;
}

function terminalAfterBranch(row) {
  return row.tail_after_next === '<END>';
}

function strictVisible(row) {
  return row.strict_source_visible === 'True' || row.strict_source_visible === 'true';
}

function permissiveVisible(row) {
  return row.permissive_public_panel === 'True' || row.permissive_public_panel === 'true';
}

function broadRegisterKey(row) {
  return [row.site, row.type, row.shape, row.material].join('|');
}

function sourceConventionKey(row) {
  return [row.site, row.type, row.symbol, row.cult, row.shape, row.material].join('|');
}

function branchStats(rows, labels) {
  const byBranch = new Map();
  rows.forEach((row, i) => {
    const branch = labels[i];
    if (!byBranch.has(branch)) byBranch.set(branch, []);
    byBranch.get(branch).push(row);
  });

  const out = [];
  for (const [branch, group] of byBranch.entries()) {
    const strictRows = group.filter(strictVisible);
    const permissiveRows = group.filter(permissiveVisible);
    const terminals = group.filter(terminalAfterBranch);
    out.push({
      branch_after_390: branch,
      raw_rows: group.length,
      objects: group.map(objectId).join(' '),
      terminal_rows: terminals.length,
      continuation_rows: group.length - terminals.length,
      strict_source_visible_rows: strictRows.length,
      strict_source_visible_objects: strictRows.map(objectId).join(' '),
      permissive_public_rows: permissiveRows.length,
      broad_register_cells: new Set(group.map(broadRegisterKey)).size,
      strict_broad_register_cells: new Set(strictRows.map(broadRegisterKey)).size,
      strict_source_convention_cells: new Set(strictRows.map(sourceConventionKey)).size,
      tails: [...new Set(group.map((row) => row.tail_after_next))].sort().join(' | '),
      branch_score: group.length * 100 + strictRows.length * 10 + (group.length - terminals.length),
    });
  }
  return out.sort((a, b) => b.raw_rows - a.raw_rows
    || b.strict_source_visible_rows - a.strict_source_visible_rows
    || a.branch_after_390.localeCompare(b.branch_after_390));
}

function eventFlags(stats) {
  const target = stats.find((row) => row.branch_after_390 === TARGET_BRANCH);
  const any = stats.some((row) => row.raw_rows >= 4
    && row.strict_source_visible_rows >= 2
    && row.terminal_rows === 0);
  const anyBroadIndependent = stats.some((row) => row.raw_rows >= 4
    && row.strict_source_visible_rows >= 2
    && row.terminal_rows === 0
    && row.strict_broad_register_cells >= 2);
  return {
    target_raw_ge4_strict_ge2_continuation_only: !!target
      && target.raw_rows >= 4
      && target.strict_source_visible_rows >= 2
      && target.terminal_rows === 0,
    target_raw_ge4_strict_ge2_continuation_only_broad_independent: !!target
      && target.raw_rows >= 4
      && target.strict_source_visible_rows >= 2
      && target.terminal_rows === 0
      && target.strict_broad_register_cells >= 2,
    any_raw_ge4_strict_ge2_continuation_only: any,
    any_raw_ge4_strict_ge2_continuation_only_broad_independent: anyBroadIndependent,
    max_raw_rows: Math.max(...stats.map((row) => row.raw_rows)),
    max_strict_source_visible_rows: Math.max(...stats.map((row) => row.strict_source_visible_rows)),
  };
}

function permuteLabels(rows, mode, rand) {
  const labels = rows.map((row) => row.next_after_390);
  const out = [...labels];
  const groupedModes = {
    all_rows: () => new Map([['all', rows.map((_, i) => i)]]),
    terminal_status: () => groupBy(rows.map((row, i) => ({ row, i })), (item) => terminalAfterBranch(item.row) ? 'terminal' : 'continuing'),
    source_visibility: () => groupBy(rows.map((row, i) => ({ row, i })), (item) => strictVisible(item.row) ? 'strict' : 'non_strict'),
    site_type: () => groupBy(rows.map((row, i) => ({ row, i })), (item) => `${item.row.site}|${item.row.type}`),
    site_type_terminal: () => groupBy(rows.map((row, i) => ({ row, i })), (item) => `${item.row.site}|${item.row.type}|${terminalAfterBranch(item.row) ? 'terminal' : 'continuing'}`),
  };
  const groups = groupedModes[mode]();
  for (const group of groups.values()) {
    const indexes = typeof group[0] === 'number' ? group : group.map((item) => item.i);
    const shuffled = shuffle(indexes.map((i) => labels[i]), rand);
    indexes.forEach((idx, pos) => {
      out[idx] = shuffled[pos];
    });
  }
  return out;
}

const rows = parseCsv(fs.readFileSync(ROWS_CSV, 'utf8'));
const observedLabels = rows.map((row) => row.next_after_390);
const observedStats = branchStats(rows, observedLabels);
const observedFlags = eventFlags(observedStats);
const rand = seededRandom('002390x-replacement-branch-forger-20260531');

const modes = ['all_rows', 'terminal_status', 'source_visibility', 'site_type', 'site_type_terminal'];
const nullRows = [];
for (const mode of modes) {
  const counts = {
    target_raw_ge4_strict_ge2_continuation_only: 0,
    target_raw_ge4_strict_ge2_continuation_only_broad_independent: 0,
    any_raw_ge4_strict_ge2_continuation_only: 0,
    any_raw_ge4_strict_ge2_continuation_only_broad_independent: 0,
  };
  let maxRawGeObserved = 0;
  let maxStrictGeObserved = 0;
  for (let iteration = 0; iteration < ITERATIONS; iteration += 1) {
    const labels = permuteLabels(rows, mode, rand);
    const flags = eventFlags(branchStats(rows, labels));
    for (const key of Object.keys(counts)) {
      if (flags[key]) counts[key] += 1;
    }
    if (flags.max_raw_rows >= observedFlags.max_raw_rows) maxRawGeObserved += 1;
    if (flags.max_strict_source_visible_rows >= observedFlags.max_strict_source_visible_rows) maxStrictGeObserved += 1;
  }
  nullRows.push({
    null_model: mode,
    iterations: ITERATIONS,
    target_event_ge_observed_share: (counts.target_raw_ge4_strict_ge2_continuation_only / ITERATIONS).toFixed(6),
    target_event_broad_independent_ge_observed_share: (counts.target_raw_ge4_strict_ge2_continuation_only_broad_independent / ITERATIONS).toFixed(6),
    discovery_event_ge_observed_share: (counts.any_raw_ge4_strict_ge2_continuation_only / ITERATIONS).toFixed(6),
    discovery_event_broad_independent_ge_observed_share: (counts.any_raw_ge4_strict_ge2_continuation_only_broad_independent / ITERATIONS).toFixed(6),
    max_raw_rows_ge_observed_share: (maxRawGeObserved / ITERATIONS).toFixed(6),
    max_strict_source_visible_rows_ge_observed_share: (maxStrictGeObserved / ITERATIONS).toFixed(6),
  });
}

const targetObserved = observedStats.find((row) => row.branch_after_390 === TARGET_BRANCH);
const summary = {
  date: '2026-05-31',
  run_id: 'replacement_20260531',
  input: 'data/open_prototype/reports/campaign_032_002_861_002390x_source_normalized_contrast_rows.csv',
  input_sha256: crypto.createHash('sha256').update(fs.readFileSync(ROWS_CSV)).digest('hex'),
  rows: rows.length,
  iterations_per_null: ITERATIONS,
  target_branch: TARGET_BRANCH,
  observed_target: targetObserved,
  observed_flags: observedFlags,
  null_rows: nullRows,
  skeptic_boundary: [
    'The low all-row shuffle FPR is not enough by itself because terminal-preserving and site/type/terminal-preserving nulls are the harsher controls for a continuation-only branch.',
    'The strict M-119/M-735 target pair shares broad site/type/shape/material register, so broad-register independence is false.',
    'No sound, meaning, language family, translation, or sign value is inferred.',
  ],
  decision: 'candidate_live_not_accepted',
  accepted_claim_increment: 0,
};

writeCsv(OUT_BRANCH_CSV, observedStats, [
  'branch_after_390',
  'raw_rows',
  'objects',
  'terminal_rows',
  'continuation_rows',
  'strict_source_visible_rows',
  'strict_source_visible_objects',
  'permissive_public_rows',
  'broad_register_cells',
  'strict_broad_register_cells',
  'strict_source_convention_cells',
  'tails',
  'branch_score',
]);
writeCsv(OUT_CSV, nullRows, [
  'null_model',
  'iterations',
  'target_event_ge_observed_share',
  'target_event_broad_independent_ge_observed_share',
  'discovery_event_ge_observed_share',
  'discovery_event_broad_independent_ge_observed_share',
  'max_raw_rows_ge_observed_share',
  'max_strict_source_visible_rows_ge_observed_share',
]);
fs.writeFileSync(OUT_JSON, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
