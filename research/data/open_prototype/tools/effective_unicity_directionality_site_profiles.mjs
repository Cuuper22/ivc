// Per-site directionality profiles for the harsh scope.
//
// The site-balance control asks whether the corpus-wide signal survives when
// sites are weighted equally; this script asks the complementary question —
// does each individual site carry the stored-vs-reversed order asymmetry on
// its own, using only its own rows to train the model? It rebuilds the harsh
// scope from lipi_scope_rows.csv (exact collapse, top-10 edge removal,
// one-edit family collapse), groups rows by site, and for every site with at
// least 10 rows (--min-site-rows=N overrides) runs the leave-one-row-out
// smoothed bigram test within that site alone. Each site's observed
// stored-win share is compared against four shuffle nulls (500 iterations
// each by default; --iterations=N overrides). Outputs in
// data/open_prototype/reports/: a JSON summary, a per-site CSV, and null
// summary/iteration CSVs. Sites too small to include are unresolved, not
// negative evidence.

import fs from 'fs';
import path from 'path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const outSummary = path.join(reportsDir, 'effective_unicity_directionality_site_profiles_summary.json');
const outRows = path.join(reportsDir, 'effective_unicity_directionality_site_profiles.csv');
const outNullSummary = path.join(reportsDir, 'effective_unicity_directionality_site_profiles_null_summary.csv');
const outNullIterations = path.join(reportsDir, 'effective_unicity_directionality_site_profiles_null_iterations.csv');

const START = '<S>';
const END = '</S>';
const ALPHA = 0.1;
const NULL_ITERATIONS = Number(process.argv.find((arg) => arg.startsWith('--iterations='))?.split('=')[1] ?? 500);
const MIN_SITE_ROWS = Number(process.argv.find((arg) => arg.startsWith('--min-site-rows='))?.split('=')[1] ?? 10);

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
    .slice(0, 10)
    .map(([token]) => token));
  return records.filter((record) => !top.has(record.tokens[0]) && !top.has(record.tokens[record.tokens.length - 1]));
}

function makeNull(records, control, rng) {
  if (control === 'row_internal_shuffle') {
    return records.map((record, index) => ({
      ...record,
      id: `${record.id}_row_${index}`,
      tokens: shuffleInPlace([...record.tokens], rng),
    }));
  }
  if (control === 'global_token_shuffle') {
    const allTokens = shuffleInPlace(records.flatMap((record) => record.tokens), rng);
    let cursor = 0;
    return records.map((record, index) => {
      const tokens = allTokens.slice(cursor, cursor + record.tokens.length);
      cursor += record.tokens.length;
      return { ...record, id: `${record.id}_global_${index}`, tokens };
    });
  }
  if (control === 'position_slot_shuffle') {
    const pools = new Map();
    for (const record of records) {
      record.tokens.forEach((token, tokenIndex) => {
        const key = `${record.tokens.length}|${tokenIndex}`;
        if (!pools.has(key)) pools.set(key, []);
        pools.get(key).push(token);
      });
    }
    for (const pool of pools.values()) shuffleInPlace(pool, rng);
    const cursors = new Map();
    return records.map((record, index) => ({
      ...record,
      id: `${record.id}_slot_${index}`,
      tokens: record.tokens.map((_, tokenIndex) => {
        const key = `${record.tokens.length}|${tokenIndex}`;
        const cursor = cursors.get(key) ?? 0;
        cursors.set(key, cursor + 1);
        return pools.get(key)[cursor];
      }),
    }));
  }
  if (control === 'edge_frame_shuffle') {
    const interiors = shuffleInPlace(records.flatMap((record) => record.tokens.slice(1, -1)), rng);
    let cursor = 0;
    return records.map((record, index) => {
      if (record.tokens.length <= 2) return { ...record, id: `${record.id}_edge_${index}` };
      const interior = interiors.slice(cursor, cursor + record.tokens.length - 2);
      cursor += record.tokens.length - 2;
      return {
        ...record,
        id: `${record.id}_edge_${index}`,
        tokens: [record.tokens[0], ...interior, record.tokens[record.tokens.length - 1]],
      };
    });
  }
  throw new Error(`Unknown control: ${control}`);
}

function summarize(values) {
  const sorted = [...values].sort((a, b) => a - b);
  const quantile = (p) => sorted[Math.min(sorted.length - 1, Math.max(0, Math.floor(p * (sorted.length - 1))))] ?? 0;
  return {
    mean: values.reduce((sum, value) => sum + value, 0) / values.length,
    p05: quantile(0.05),
    median: quantile(0.5),
    p95: quantile(0.95),
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
      tokens: parseTokens(row.text),
    }))
    .filter((row) => row.tokens.length >= 2));
  return oneEditFamilyCollapse(topEdgeRemoved(exact, 10));
}

const controls = ['global_token_shuffle', 'row_internal_shuffle', 'position_slot_shuffle', 'edge_frame_shuffle'];
const harshRecords = loadHarshRecords();
const bySite = groupBy(harshRecords, (record) => record.site);
const sites = [...bySite.entries()]
  .map(([site, rows]) => ({ site, records: rows }))
  .filter(({ records }) => records.length >= MIN_SITE_ROWS)
  .sort((a, b) => b.records.length - a.records.length || a.site.localeCompare(b.site));

const outputRows = [];
const nullSummaryRows = [];
const nullIterationRows = [];

for (const { site, records } of sites) {
  const observed = scoreDirection(records);
  const nullGeShares = [];
  for (const control of controls) {
    const values = [];
    for (let iteration = 0; iteration < NULL_ITERATIONS; iteration++) {
      const rng = makeRng(hashString(`${site}:${control}:${iteration}`));
      const score = scoreDirection(makeNull(records, control, rng));
      values.push(score.stored_win_share);
      nullIterationRows.push({
        site,
        control,
        iteration: iteration + 1,
        stored_win_share: round(score.stored_win_share),
        mean_diff: round(score.mean_stored_minus_reversed_per_transition),
      });
    }
    const stats = summarize(values);
    const geShare = values.filter((value) => value >= observed.stored_win_share).length / values.length;
    nullGeShares.push(geShare);
    nullSummaryRows.push({
      site,
      control,
      iterations: NULL_ITERATIONS,
      observed: round(observed.stored_win_share),
      null_mean: round(stats.mean),
      null_p05: round(stats.p05),
      null_median: round(stats.median),
      null_p95: round(stats.p95),
      null_max: round(stats.max),
      null_ge_observed_share: round(geShare),
    });
  }
  outputRows.push({
    site,
    scope: 'top10_edge_removed_one_edit_family_collapsed',
    rows: observed.rows,
    tokens: observed.tokens,
    unique_tokens: observed.unique_tokens,
    stored_higher: observed.stored_higher,
    reversed_higher: observed.reversed_higher,
    ties: observed.ties,
    stored_win_share: round(observed.stored_win_share),
    mean_stored_minus_reversed_per_transition: round(observed.mean_stored_minus_reversed_per_transition),
    max_null_ge_observed_share: round(Math.max(...nullGeShares)),
  });
}

const summary = {
  date: '2026-05-29',
  generated_at_utc: new Date().toISOString(),
  purpose: 'Per-site directionality profiles for the harsh Vector 2 directionality scope.',
  source_scope: {
    base_scope: 'top10_edge_removed_one_edit_family_collapsed',
    total_rows: harshRecords.length,
    min_site_rows: MIN_SITE_ROWS,
    included_sites: outputRows.map((row) => row.site),
  },
  method: {
    scoring: 'Within each site, score stored order versus reversed order with leave-one-row-out bigram scoring.',
    null_iterations_per_control: NULL_ITERATIONS,
    controls,
    interpretation_boundary: 'Per-site profiles test whether each site carries internal directionality. Small or excluded sites remain unresolved, not negative evidence.',
  },
  primary_results: Object.fromEntries(outputRows.map((row) => [row.site, row])),
  rows: outputRows,
  artifact_files: [
    'data/open_prototype/tools/effective_unicity_directionality_site_profiles.mjs',
    'data/open_prototype/reports/effective_unicity_directionality_site_profiles_summary.json',
    'data/open_prototype/reports/effective_unicity_directionality_site_profiles.csv',
    'data/open_prototype/reports/effective_unicity_directionality_site_profiles_null_summary.csv',
    'data/open_prototype/reports/effective_unicity_directionality_site_profiles_null_iterations.csv',
  ],
};

fs.writeFileSync(outSummary, `${JSON.stringify(summary, null, 2)}\n`);
fs.writeFileSync(outRows, toCsv(outputRows, [
  'site',
  'scope',
  'rows',
  'tokens',
  'unique_tokens',
  'stored_higher',
  'reversed_higher',
  'ties',
  'stored_win_share',
  'mean_stored_minus_reversed_per_transition',
  'max_null_ge_observed_share',
]));
fs.writeFileSync(outNullSummary, toCsv(nullSummaryRows, [
  'site',
  'control',
  'iterations',
  'observed',
  'null_mean',
  'null_p05',
  'null_median',
  'null_p95',
  'null_max',
  'null_ge_observed_share',
]));
fs.writeFileSync(outNullIterations, toCsv(nullIterationRows, [
  'site',
  'control',
  'iteration',
  'stored_win_share',
  'mean_diff',
]));

console.log(JSON.stringify(summary, null, 2));
