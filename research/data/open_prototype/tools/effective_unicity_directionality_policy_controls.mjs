// Recorded-direction policy controls for the directionality candidate.
//
// The corpus rows come with a recorded direction field (R/L or L/R) added by
// transcribers. If those labels — or the orientation conventions behind them —
// drove the stored-vs-reversed asymmetry, the signal would be an editorial
// artifact, not sequence structure. This script rebuilds the harsh scope from
// lipi_scope_rows.csv (exact collapse, top-10 edge removal, one-edit family
// collapse) and rescores the leave-one-row-out bigram test after rewriting
// token order under seven policies: stored as-is, reverse every row, flip only
// L/R rows, flip only R/L rows, and three randomized flips (per row, per site,
// per direction label; 1000 iterations each by default, --iterations=N
// overrides). Each policy runs on four scopes: all rows, R/L only, and the
// R/L rows of Mohenjo-daro and Harappa separately. Outputs go to
// data/open_prototype/reports/: a JSON summary with direction distributions,
// a per-policy CSV, and null summary/iteration CSVs. This tests sensitivity
// to recorded direction fields only; it says nothing about the physical
// reading direction on the objects.

import fs from 'fs';
import path from 'path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const outSummary = path.join(reportsDir, 'effective_unicity_directionality_policy_controls_summary.json');
const outRows = path.join(reportsDir, 'effective_unicity_directionality_policy_controls.csv');
const outNullSummary = path.join(reportsDir, 'effective_unicity_directionality_policy_null_summary.csv');
const outNullIterations = path.join(reportsDir, 'effective_unicity_directionality_policy_null_iterations.csv');

const START = '<S>';
const END = '</S>';
const ALPHA = 0.1;
const NULL_ITERATIONS = Number(process.argv.find((arg) => arg.startsWith('--iterations='))?.split('=')[1] ?? 1000);

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;
  for (let index = 0; index < text.length; index++) {
    const char = text[index];
    if (inQuotes) {
      if (char === '"') {
        if (text[index + 1] === '"') {
          field += '"';
          index++;
        } else {
          inQuotes = false;
        }
      } else {
        field += char;
      }
    } else if (char === '"') {
      inQuotes = true;
    } else if (char === ',') {
      row.push(field);
      field = '';
    } else if (char === '\n') {
      row.push(field);
      rows.push(row);
      row = [];
      field = '';
    } else if (char !== '\r') {
      field += char;
    }
  }
  if (field.length || row.length) {
    row.push(field);
    rows.push(row);
  }
  return rows;
}

function loadCsv(filePath) {
  const parsed = parseCsv(fs.readFileSync(filePath, 'utf8'));
  const header = parsed[0] ?? [];
  return parsed.slice(1).filter((row) => row.length > 1).map((row) =>
    Object.fromEntries(header.map((name, index) => [name, row[index] ?? ''])),
  );
}

function csvEscape(value) {
  const text = String(value ?? '');
  if (/[",\n\r]/.test(text)) return `"${text.replaceAll('"', '""')}"`;
  return `"${text}"`;
}

function toCsv(rows, columns) {
  return `${columns.map(csvEscape).join(',')}\n${rows
    .map((row) => columns.map((column) => csvEscape(row[column])).join(','))
    .join('\n')}\n`;
}

function parseTokens(text) {
  return [...String(text).matchAll(/\d{3}/g)].map((match) => match[0]);
}

function normalize(value) {
  return String(value || '-').trim() || '-';
}

function transitions(tokens) {
  const sequence = [START, ...tokens, END];
  const pairs = [];
  for (let index = 0; index < sequence.length - 1; index++) {
    pairs.push([sequence[index], sequence[index + 1]]);
  }
  return pairs;
}

function addCounts(map, key, delta) {
  const next = (map.get(key) ?? 0) + delta;
  if (next === 0) map.delete(key);
  else map.set(key, next);
}

function buildCounts(records) {
  const vocab = new Set();
  const bigramCounts = new Map();
  const prevCounts = new Map();
  const rowCounts = records.map((record) => {
    const bigrams = new Map();
    const prevs = new Map();
    for (const token of record.tokens) vocab.add(token);
    for (const [prev, next] of transitions(record.tokens)) {
      const key = `${prev}\t${next}`;
      addCounts(bigramCounts, key, 1);
      addCounts(prevCounts, prev, 1);
      addCounts(bigrams, key, 1);
      addCounts(prevs, prev, 1);
    }
    return { bigrams, prevs };
  });
  return { vocab, bigramCounts, prevCounts, rowCounts };
}

function logProb(tokens, counts, rowIndex) {
  const outcomeCount = counts.vocab.size + 1;
  let total = 0;
  for (const [prev, next] of transitions(tokens)) {
    const key = `${prev}\t${next}`;
    const bigramCount = (counts.bigramCounts.get(key) ?? 0) - (counts.rowCounts[rowIndex]?.bigrams.get(key) ?? 0);
    const prevCount = (counts.prevCounts.get(prev) ?? 0) - (counts.rowCounts[rowIndex]?.prevs.get(prev) ?? 0);
    total += Math.log((bigramCount + ALPHA) / (prevCount + ALPHA * outcomeCount));
  }
  return total;
}

function scoreDirection(records) {
  const usable = records.filter((record) => record.tokens.length > 1);
  const counts = buildCounts(usable);
  let storedHigher = 0;
  let reversedHigher = 0;
  let ties = 0;
  let diffSum = 0;
  for (let rowIndex = 0; rowIndex < usable.length; rowIndex++) {
    const record = usable[rowIndex];
    const stored = logProb(record.tokens, counts, rowIndex);
    const reversed = logProb([...record.tokens].reverse(), counts, rowIndex);
    const diff = (stored - reversed) / (record.tokens.length + 1);
    diffSum += diff;
    if (Math.abs(diff) < 1e-12) ties++;
    else if (diff > 0) storedHigher++;
    else reversedHigher++;
  }
  return {
    rows: usable.length,
    tokens: usable.reduce((sum, record) => sum + record.tokens.length, 0),
    unique_tokens: new Set(usable.flatMap((record) => record.tokens)).size,
    stored_higher: storedHigher,
    reversed_higher: reversedHigher,
    ties,
    stored_win_share: usable.length ? storedHigher / usable.length : 0,
    mean_stored_minus_reversed_per_transition: usable.length ? diffSum / usable.length : 0,
  };
}

function makeRng(seed) {
  let state = seed >>> 0;
  return () => {
    state = (1664525 * state + 1013904223) >>> 0;
    return state / 0x100000000;
  };
}

function hashString(text) {
  let hash = 2166136261;
  for (let index = 0; index < text.length; index++) {
    hash ^= text.charCodeAt(index);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}

function shuffleInPlace(array, rng) {
  for (let index = array.length - 1; index > 0; index--) {
    const swapIndex = Math.floor(rng() * (index + 1));
    [array[index], array[swapIndex]] = [array[swapIndex], array[index]];
  }
  return array;
}

function groupBy(records, keyFn) {
  const groups = new Map();
  for (const record of records) {
    const key = keyFn(record);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(record);
  }
  return groups;
}

function exactCollapse(records) {
  const byKey = new Map();
  for (const record of records) {
    const key = record.tokens.join(' ');
    if (!byKey.has(key)) byKey.set(key, { ...record, source_ids: [record.id], duplicate_weight: 1 });
    else {
      const current = byKey.get(key);
      current.duplicate_weight++;
      current.source_ids.push(record.id);
    }
  }
  return [...byKey.values()].sort((a, b) => a.tokens.join(' ').localeCompare(b.tokens.join(' ')));
}

function chooseRepresentatives(groups, policyName) {
  return [...groups.values()].map((members, index) => {
    const representative = [...members].sort((a, b) => {
      const weightDiff = (b.duplicate_weight ?? 1) - (a.duplicate_weight ?? 1);
      if (weightDiff) return weightDiff;
      return a.tokens.join(' ').localeCompare(b.tokens.join(' '));
    })[0];
    return {
      ...representative,
      id: `${policyName}_${String(index + 1).padStart(5, '0')}`,
      family_size: members.length,
      family_source_weight: members.reduce((sum, member) => sum + (member.duplicate_weight ?? 1), 0),
      source_ids: members.flatMap((member) => member.source_ids ?? [member.id]),
    };
  });
}

class UnionFind {
  constructor(size) {
    this.parent = Array.from({ length: size }, (_, index) => index);
    this.rank = Array.from({ length: size }, () => 0);
  }
  find(value) {
    if (this.parent[value] !== value) this.parent[value] = this.find(this.parent[value]);
    return this.parent[value];
  }
  union(a, b) {
    const rootA = this.find(a);
    const rootB = this.find(b);
    if (rootA === rootB) return;
    if (this.rank[rootA] < this.rank[rootB]) this.parent[rootA] = rootB;
    else if (this.rank[rootA] > this.rank[rootB]) this.parent[rootB] = rootA;
    else {
      this.parent[rootB] = rootA;
      this.rank[rootA]++;
    }
  }
}

function oneEditFamilyCollapse(records) {
  const uf = new UnionFind(records.length);
  const signatureToFirst = new Map();
  const addSignature = (signature, index) => {
    const first = signatureToFirst.get(signature);
    if (first === undefined) signatureToFirst.set(signature, index);
    else uf.union(first, index);
  };

  records.forEach((record, index) => {
    const tokens = record.tokens;
    for (let pos = 0; pos < tokens.length; pos++) {
      const wildcard = [...tokens];
      wildcard[pos] = '*';
      addSignature(`wild:${tokens.length}:${wildcard.join(' ')}`, index);
      addSignature(`del:${tokens.length - 1}:${tokens.filter((_, tokenIndex) => tokenIndex !== pos).join(' ')}`, index);
    }
  });

  const groups = new Map();
  records.forEach((record, index) => {
    const root = uf.find(index);
    if (!groups.has(root)) groups.set(root, []);
    groups.get(root).push(record);
  });
  return chooseRepresentatives(groups, 'one_edit_family');
}

function topEdgeRemoved(records, topN = 10) {
  const edgeCounts = new Map();
  for (const record of records) {
    const first = record.tokens[0];
    const last = record.tokens[record.tokens.length - 1];
    edgeCounts.set(first, (edgeCounts.get(first) ?? 0) + 1);
    edgeCounts.set(last, (edgeCounts.get(last) ?? 0) + 1);
  }
  const top = new Set([...edgeCounts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, topN)
    .map(([token]) => token));
  return records.filter((record) => !top.has(record.tokens[0]) && !top.has(record.tokens[record.tokens.length - 1]));
}

function transformPolicy(records, policy, rng) {
  let siteFlips;
  let directionFlips;
  if (policy === 'random_site_flips') {
    siteFlips = new Map([...new Set(records.map((record) => record.site))].map((site) => [site, rng() < 0.5]));
  }
  if (policy === 'random_direction_label_flips') {
    directionFlips = new Map([...new Set(records.map((record) => record.direction))].map((direction) => [direction, rng() < 0.5]));
  }
  return records.map((record, index) => {
    let flip = false;
    if (policy === 'reverse_all') flip = true;
    else if (policy === 'flip_LR_only') flip = record.direction === 'L/R';
    else if (policy === 'flip_RL_only') flip = record.direction === 'R/L';
    else if (policy === 'random_row_flips') flip = rng() < 0.5;
    else if (policy === 'random_site_flips') flip = siteFlips.get(record.site) ?? false;
    else if (policy === 'random_direction_label_flips') flip = directionFlips.get(record.direction) ?? false;
    else if (policy !== 'stored_as_is') throw new Error(`Unknown policy: ${policy}`);
    return {
      ...record,
      id: `${record.id}_${policy}_${index}`,
      tokens: flip ? [...record.tokens].reverse() : [...record.tokens],
      policy_flipped: flip,
    };
  });
}

function summarize(values) {
  const sorted = [...values].sort((a, b) => a - b);
  const quantile = (p) => sorted[Math.min(sorted.length - 1, Math.max(0, Math.floor(p * (sorted.length - 1))))] ?? 0;
  return {
    mean: values.reduce((sum, value) => sum + value, 0) / values.length,
    p05: quantile(0.05),
    median: quantile(0.5),
    p95: quantile(0.95),
    min: sorted[0] ?? 0,
    max: sorted[sorted.length - 1] ?? 0,
  };
}

function round(value) {
  return Number.isFinite(value) ? Number(value.toFixed(6)) : null;
}

function loadHarshRecords() {
  const exact = exactCollapse(loadCsv(path.join(reportsDir, 'lipi_scope_rows.csv'))
    .filter((row) => row.readiness_bucket === 'lipi_numeric_clean_candidate')
    .map((row, index) => ({
      id: row.id || `ivc_${index + 1}`,
      site: normalize(row.site),
      type: normalize(row.type),
      material: normalize(row.material),
      symbol: normalize(row.symbol),
      direction: normalize(row.direction),
      tokens: parseTokens(row.text),
    }))
    .filter((row) => row.tokens.length >= 2));
  return oneEditFamilyCollapse(topEdgeRemoved(exact, 10));
}

const harshRecords = loadHarshRecords();
const deterministicPolicies = ['stored_as_is', 'reverse_all', 'flip_LR_only', 'flip_RL_only'];
const randomPolicies = ['random_row_flips', 'random_site_flips', 'random_direction_label_flips'];
const scopes = [
  {
    scope: 'all_harsh',
    records: harshRecords,
  },
  {
    scope: 'R_L_only',
    records: harshRecords.filter((record) => record.direction === 'R/L'),
  },
  {
    scope: 'Mohenjo_daro_R_L_only',
    records: harshRecords.filter((record) => record.site === 'Mohenjo-daro' && record.direction === 'R/L'),
  },
  {
    scope: 'Harappa_R_L_only',
    records: harshRecords.filter((record) => record.site === 'Harappa' && record.direction === 'R/L'),
  },
];

const directionDistribution = Object.fromEntries([...groupBy(harshRecords, (record) => record.direction).entries()]
  .map(([direction, rows]) => [direction, rows.length])
  .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])));
const siteDirectionDistribution = Object.fromEntries([...groupBy(harshRecords, (record) => `${record.site}|${record.direction}`).entries()]
  .map(([key, rows]) => [key, rows.length])
  .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])));

const outputRows = [];
for (const scope of scopes) {
  for (const policy of deterministicPolicies) {
    const transformed = transformPolicy(scope.records, policy, makeRng(hashString(`${scope.scope}:${policy}:deterministic`)));
    const score = scoreDirection(transformed);
    outputRows.push({
      scope: scope.scope,
      policy,
      policy_class: 'deterministic',
      rows: score.rows,
      tokens: score.tokens,
      unique_tokens: score.unique_tokens,
      flipped_rows: transformed.filter((record) => record.policy_flipped).length,
      stored_higher: score.stored_higher,
      reversed_higher: score.reversed_higher,
      ties: score.ties,
      stored_win_share: round(score.stored_win_share),
      mean_stored_minus_reversed_per_transition: round(score.mean_stored_minus_reversed_per_transition),
      null_mean: '',
      null_p05: '',
      null_median: '',
      null_p95: '',
      null_ge_stored_as_is_share: '',
    });
  }
}

const nullSummaryRows = [];
const nullIterationRows = [];
for (const scope of scopes) {
  const baseline = outputRows.find((row) => row.scope === scope.scope && row.policy === 'stored_as_is');
  for (const policy of randomPolicies) {
    const values = [];
    for (let iteration = 0; iteration < NULL_ITERATIONS; iteration++) {
      const rng = makeRng(hashString(`${scope.scope}:${policy}:${iteration}`));
      const transformed = transformPolicy(scope.records, policy, rng);
      const score = scoreDirection(transformed);
      values.push(score.stored_win_share);
      nullIterationRows.push({
        scope: scope.scope,
        policy,
        iteration: iteration + 1,
        flipped_rows: transformed.filter((record) => record.policy_flipped).length,
        stored_win_share: round(score.stored_win_share),
        mean_diff: round(score.mean_stored_minus_reversed_per_transition),
      });
    }
    const stats = summarize(values);
    const geShare = values.filter((value) => value >= Number(baseline.stored_win_share)).length / values.length;
    nullSummaryRows.push({
      scope: scope.scope,
      policy,
      iterations: NULL_ITERATIONS,
      stored_as_is: baseline.stored_win_share,
      null_mean: round(stats.mean),
      null_p05: round(stats.p05),
      null_median: round(stats.median),
      null_p95: round(stats.p95),
      null_min: round(stats.min),
      null_max: round(stats.max),
      null_ge_stored_as_is_share: round(geShare),
    });
    outputRows.push({
      scope: scope.scope,
      policy,
      policy_class: 'randomized',
      rows: scope.records.length,
      tokens: scope.records.reduce((sum, record) => sum + record.tokens.length, 0),
      unique_tokens: new Set(scope.records.flatMap((record) => record.tokens)).size,
      flipped_rows: '',
      stored_higher: '',
      reversed_higher: '',
      ties: '',
      stored_win_share: '',
      mean_stored_minus_reversed_per_transition: '',
      null_mean: round(stats.mean),
      null_p05: round(stats.p05),
      null_median: round(stats.median),
      null_p95: round(stats.p95),
      null_ge_stored_as_is_share: round(geShare),
    });
  }
}

const primary = {
  all_harsh_stored_as_is: outputRows.find((row) => row.scope === 'all_harsh' && row.policy === 'stored_as_is'),
  all_harsh_R_L_only: outputRows.find((row) => row.scope === 'R_L_only' && row.policy === 'stored_as_is'),
  mohenjo_R_L_only: outputRows.find((row) => row.scope === 'Mohenjo_daro_R_L_only' && row.policy === 'stored_as_is'),
  harappa_R_L_only: outputRows.find((row) => row.scope === 'Harappa_R_L_only' && row.policy === 'stored_as_is'),
  all_harsh_flip_LR_only: outputRows.find((row) => row.scope === 'all_harsh' && row.policy === 'flip_LR_only'),
  all_harsh_random_row_flips: nullSummaryRows.find((row) => row.scope === 'all_harsh' && row.policy === 'random_row_flips'),
  all_harsh_random_site_flips: nullSummaryRows.find((row) => row.scope === 'all_harsh' && row.policy === 'random_site_flips'),
  all_harsh_random_direction_label_flips: nullSummaryRows.find((row) => row.scope === 'all_harsh' && row.policy === 'random_direction_label_flips'),
};

const summary = {
  date: '2026-05-29',
  generated_at_utc: new Date().toISOString(),
  purpose: 'Recorded-direction policy controls for the harsh Vector 2 directionality candidate.',
  source_scope: {
    base_scope: 'top10_edge_removed_one_edit_family_collapsed',
    rows: harshRecords.length,
    direction_distribution: directionDistribution,
    site_direction_distribution: siteDirectionDistribution,
  },
  method: {
    deterministic_policies: deterministicPolicies,
    random_policies: randomPolicies,
    null_iterations: NULL_ITERATIONS,
    interpretation_boundary: 'This tests sensitivity to recorded direction fields and row/site/direction-label orientation flips. It does not validate physical source-image direction.',
  },
  primary_results: primary,
  rows: outputRows,
  artifact_files: [
    'data/open_prototype/tools/effective_unicity_directionality_policy_controls.mjs',
    'data/open_prototype/reports/effective_unicity_directionality_policy_controls_summary.json',
    'data/open_prototype/reports/effective_unicity_directionality_policy_controls.csv',
    'data/open_prototype/reports/effective_unicity_directionality_policy_null_summary.csv',
    'data/open_prototype/reports/effective_unicity_directionality_policy_null_iterations.csv',
  ],
};

fs.writeFileSync(outSummary, `${JSON.stringify(summary, null, 2)}\n`);
fs.writeFileSync(outRows, toCsv(outputRows, [
  'scope',
  'policy',
  'policy_class',
  'rows',
  'tokens',
  'unique_tokens',
  'flipped_rows',
  'stored_higher',
  'reversed_higher',
  'ties',
  'stored_win_share',
  'mean_stored_minus_reversed_per_transition',
  'null_mean',
  'null_p05',
  'null_median',
  'null_p95',
  'null_ge_stored_as_is_share',
]));
fs.writeFileSync(outNullSummary, toCsv(nullSummaryRows, [
  'scope',
  'policy',
  'iterations',
  'stored_as_is',
  'null_mean',
  'null_p05',
  'null_median',
  'null_p95',
  'null_min',
  'null_max',
  'null_ge_stored_as_is_share',
]));
fs.writeFileSync(outNullIterations, toCsv(nullIterationRows, [
  'scope',
  'policy',
  'iteration',
  'flipped_rows',
  'stored_win_share',
  'mean_diff',
]));

console.log(JSON.stringify(summary, null, 2));
