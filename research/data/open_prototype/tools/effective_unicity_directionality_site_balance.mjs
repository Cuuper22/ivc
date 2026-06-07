import fs from 'fs';
import path from 'path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const outSummary = path.join(reportsDir, 'effective_unicity_directionality_site_balance_summary.json');
const outRows = path.join(reportsDir, 'effective_unicity_directionality_site_balance.csv');
const outIterations = path.join(reportsDir, 'effective_unicity_directionality_site_balance_iterations.csv');
const outNullSummary = path.join(reportsDir, 'effective_unicity_directionality_site_balance_null_summary.csv');

const START = '<S>';
const END = '</S>';
const ALPHA = 0.1;
const ITERATIONS = Number(process.argv.find((arg) => arg.startsWith('--iterations='))?.split('=')[1] ?? 500);

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

function sampleWithoutReplacement(records, count, rng) {
  return shuffleInPlace([...records], rng).slice(0, count);
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
  if (control === 'position_slot_shuffle' || control === 'site_position_shuffle') {
    const pools = new Map();
    const poolKey = (record, tokenIndex) => {
      const base = `${record.tokens.length}|${tokenIndex}`;
      return control === 'site_position_shuffle' ? `${normalize(record.site)}|${base}` : base;
    };
    for (const record of records) {
      record.tokens.forEach((token, tokenIndex) => {
        const key = poolKey(record, tokenIndex);
        if (!pools.has(key)) pools.set(key, []);
        pools.get(key).push(token);
      });
    }
    for (const pool of pools.values()) shuffleInPlace(pool, rng);
    const cursors = new Map();
    return records.map((record, index) => ({
      ...record,
      id: `${record.id}_${control}_${index}`,
      tokens: record.tokens.map((_, tokenIndex) => {
        const key = poolKey(record, tokenIndex);
        const cursor = cursors.get(key) ?? 0;
        cursors.set(key, cursor + 1);
        return pools.get(key)[cursor];
      }),
    }));
  }
  if (control === 'edge_frame_shuffle' || control === 'site_edge_interior_shuffle') {
    const pools = new Map();
    for (const record of records) {
      if (record.tokens.length <= 2) continue;
      const key = control === 'site_edge_interior_shuffle'
        ? `${normalize(record.site)}|${record.tokens.length}|${record.tokens[0]}|${record.tokens[record.tokens.length - 1]}`
        : 'all';
      if (!pools.has(key)) pools.set(key, []);
      pools.get(key).push(...record.tokens.slice(1, -1));
    }
    for (const pool of pools.values()) shuffleInPlace(pool, rng);
    const cursors = new Map();
    return records.map((record, index) => {
      if (record.tokens.length <= 2) return { ...record, id: `${record.id}_${control}_${index}` };
      const key = control === 'site_edge_interior_shuffle'
        ? `${normalize(record.site)}|${record.tokens.length}|${record.tokens[0]}|${record.tokens[record.tokens.length - 1]}`
        : 'all';
      const cursor = cursors.get(key) ?? 0;
      cursors.set(key, cursor + record.tokens.length - 2);
      const interior = pools.get(key).slice(cursor, cursor + record.tokens.length - 2);
      return {
        ...record,
        id: `${record.id}_${control}_${index}`,
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
      cisi: row.cisi,
      site: normalize(row.site),
      type: normalize(row.type),
      material: normalize(row.material),
      symbol: normalize(row.symbol),
      tokens: parseTokens(row.text),
    }))
    .filter((row) => row.tokens.length >= 2));
  return oneEditFamilyCollapse(topEdgeRemoved(exact, 10));
}

function siteCounts(records) {
  return [...groupBy(records, (record) => record.site).entries()]
    .map(([site, rows]) => ({ site, rows: rows.length }))
    .sort((a, b) => b.rows - a.rows || a.site.localeCompare(b.site));
}

const harshRecords = loadHarshRecords();
const bySite = groupBy(harshRecords, (record) => record.site);
const siteInventory = siteCounts(harshRecords);

const designs = [
  {
    design: 'mohenjo_harappa_balanced',
    sites: ['Mohenjo-daro', 'Harappa'],
  },
  {
    design: 'mohenjo_harappa_lothal_balanced',
    sites: ['Mohenjo-daro', 'Harappa', 'Lothal'],
  },
  {
    design: 'top5_sites_balanced',
    sites: ['Mohenjo-daro', 'Harappa', 'Lothal', 'Chanhu-daro', 'Kalibangan'],
  },
].map((design) => {
  const cap = Math.min(...design.sites.map((site) => bySite.get(site)?.length ?? 0));
  return { ...design, cap, rows_per_iteration: cap * design.sites.length };
});

const controls = [
  'global_token_shuffle',
  'row_internal_shuffle',
  'position_slot_shuffle',
  'edge_frame_shuffle',
  'site_position_shuffle',
  'site_edge_interior_shuffle',
];

const iterationRows = [];
const summaryRows = [];
const nullSummaryRows = [];

for (const design of designs) {
  const observedScores = [];
  const observedDiffs = [];
  const nullScoresByControl = Object.fromEntries(controls.map((control) => [control, []]));
  const pairedNullGeByControl = Object.fromEntries(controls.map((control) => [control, 0]));

  for (let iteration = 0; iteration < ITERATIONS; iteration++) {
    const rng = makeRng(hashString(`${design.design}:sample:${iteration}`));
    const sampled = design.sites.flatMap((site) => sampleWithoutReplacement(bySite.get(site) ?? [], design.cap, rng));
    const observed = scoreDirection(sampled);
    observedScores.push(observed.stored_win_share);
    observedDiffs.push(observed.mean_stored_minus_reversed_per_transition);

    const row = {
      design: design.design,
      iteration: iteration + 1,
      sites: design.sites.join('|'),
      rows: observed.rows,
      tokens: observed.tokens,
      unique_tokens: observed.unique_tokens,
      observed_stored_win_share: round(observed.stored_win_share),
      observed_mean_diff: round(observed.mean_stored_minus_reversed_per_transition),
    };

    for (const control of controls) {
      const nullRng = makeRng(hashString(`${design.design}:${control}:${iteration}`));
      const nullScore = scoreDirection(makeNull(sampled, control, nullRng));
      nullScoresByControl[control].push(nullScore.stored_win_share);
      if (nullScore.stored_win_share >= observed.stored_win_share) pairedNullGeByControl[control]++;
      row[`${control}_stored_win_share`] = round(nullScore.stored_win_share);
    }
    iterationRows.push(row);
  }

  const observedStats = summarize(observedScores);
  const diffStats = summarize(observedDiffs);
  const nullGeShares = controls.map((control) => pairedNullGeByControl[control] / ITERATIONS);
  summaryRows.push({
    design: design.design,
    scope: 'top10_edge_removed_one_edit_family_collapsed',
    sites: design.sites.join('|'),
    cap_per_site: design.cap,
    rows_per_iteration: design.rows_per_iteration,
    iterations: ITERATIONS,
    observed_mean: round(observedStats.mean),
    observed_p05: round(observedStats.p05),
    observed_median: round(observedStats.median),
    observed_p95: round(observedStats.p95),
    observed_min: round(observedStats.min),
    observed_max: round(observedStats.max),
    mean_diff_mean: round(diffStats.mean),
    max_paired_null_ge_observed_share: round(Math.max(...nullGeShares)),
  });

  for (const control of controls) {
    const stats = summarize(nullScoresByControl[control]);
    nullSummaryRows.push({
      design: design.design,
      control,
      iterations: ITERATIONS,
      observed_median: round(observedStats.median),
      null_mean: round(stats.mean),
      null_p05: round(stats.p05),
      null_median: round(stats.median),
      null_p95: round(stats.p95),
      null_max: round(stats.max),
      paired_null_ge_observed_share: round(pairedNullGeByControl[control] / ITERATIONS),
    });
  }
}

const summary = {
  date: '2026-05-29',
  generated_at_utc: new Date().toISOString(),
  purpose: 'Site-balanced resampling control for the harsh Vector 2 directionality candidate.',
  source_scope: {
    base_scope: 'top10_edge_removed_one_edit_family_collapsed',
    rows: harshRecords.length,
    site_inventory: siteInventory,
  },
  method: {
    iterations: ITERATIONS,
    sampling: 'For each design, sample an equal number of rows without replacement from each listed site, score stored order versus reversed order with leave-one-row-out bigram scoring, and compare paired null scores on the same sampled rows.',
    controls,
    interpretation_boundary: 'A positive result shows the signal is not only caused by raw site imbalance in the sampled sites. It does not prove source-normalized direction or site-generalization outside the sampled sites.',
  },
  primary_results: Object.fromEntries(summaryRows.map((row) => [row.design, row])),
  rows: summaryRows,
  artifact_files: [
    'data/open_prototype/tools/effective_unicity_directionality_site_balance.mjs',
    'data/open_prototype/reports/effective_unicity_directionality_site_balance_summary.json',
    'data/open_prototype/reports/effective_unicity_directionality_site_balance.csv',
    'data/open_prototype/reports/effective_unicity_directionality_site_balance_iterations.csv',
    'data/open_prototype/reports/effective_unicity_directionality_site_balance_null_summary.csv',
  ],
};

fs.writeFileSync(outSummary, `${JSON.stringify(summary, null, 2)}\n`);
fs.writeFileSync(outRows, toCsv(summaryRows, [
  'design',
  'scope',
  'sites',
  'cap_per_site',
  'rows_per_iteration',
  'iterations',
  'observed_mean',
  'observed_p05',
  'observed_median',
  'observed_p95',
  'observed_min',
  'observed_max',
  'mean_diff_mean',
  'max_paired_null_ge_observed_share',
]));
fs.writeFileSync(outIterations, toCsv(iterationRows, [
  'design',
  'iteration',
  'sites',
  'rows',
  'tokens',
  'unique_tokens',
  'observed_stored_win_share',
  'observed_mean_diff',
  ...controls.map((control) => `${control}_stored_win_share`),
]));
fs.writeFileSync(outNullSummary, toCsv(nullSummaryRows, [
  'design',
  'control',
  'iterations',
  'observed_median',
  'null_mean',
  'null_p05',
  'null_median',
  'null_p95',
  'null_max',
  'paired_null_ge_observed_share',
]));

console.log(JSON.stringify(summary, null, 2));
