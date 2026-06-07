import fs from 'fs';
import path from 'path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const outSummary = path.join(reportsDir, 'effective_unicity_directionality_block_controls_summary.json');
const outRows = path.join(reportsDir, 'effective_unicity_directionality_block_controls.csv');
const outNullSummary = path.join(reportsDir, 'effective_unicity_directionality_block_null_summary.csv');
const outNullIterations = path.join(reportsDir, 'effective_unicity_directionality_block_null_iterations.csv');

const START = '<S>';
const END = '</S>';
const ALPHA = 0.1;
const NULL_ITERATIONS = Number(process.argv.find((arg) => arg.startsWith('--iterations='))?.split('=')[1] ?? 100);

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

function normalizeBlockValue(value) {
  return String(value || '-').trim() || '-';
}

function registerKey(record) {
  return [
    normalizeBlockValue(record.site),
    normalizeBlockValue(record.type),
    normalizeBlockValue(record.material),
    normalizeBlockValue(record.symbol),
  ].join('|');
}

function edgeKey(record) {
  const last = record.tokens[record.tokens.length - 1] ?? '';
  return `${record.tokens.length}|${record.tokens[0] ?? ''}|${last}`;
}

function addCounts(map, key, delta) {
  const next = (map.get(key) ?? 0) + delta;
  if (next === 0) map.delete(key);
  else map.set(key, next);
}

function transitions(tokens) {
  const sequence = [START, ...tokens, END];
  const pairs = [];
  for (let index = 0; index < sequence.length - 1; index++) {
    pairs.push([sequence[index], sequence[index + 1]]);
  }
  return pairs;
}

function emptyCountBundle() {
  return { bigrams: new Map(), prevs: new Map() };
}

function buildCounts(records, holdoutKeyFn) {
  const vocab = new Set();
  const bigramCounts = new Map();
  const prevCounts = new Map();
  const rowCounts = [];
  const holdoutCounts = new Map();

  records.forEach((record, rowIndex) => {
    const rowBundle = emptyCountBundle();
    const holdoutKey = holdoutKeyFn(record, rowIndex);
    if (!holdoutCounts.has(holdoutKey)) holdoutCounts.set(holdoutKey, emptyCountBundle());
    const holdoutBundle = holdoutCounts.get(holdoutKey);

    for (const token of record.tokens) vocab.add(token);
    for (const [prev, next] of transitions(record.tokens)) {
      const key = `${prev}\t${next}`;
      addCounts(bigramCounts, key, 1);
      addCounts(prevCounts, prev, 1);
      addCounts(rowBundle.bigrams, key, 1);
      addCounts(rowBundle.prevs, prev, 1);
      addCounts(holdoutBundle.bigrams, key, 1);
      addCounts(holdoutBundle.prevs, prev, 1);
    }
    rowCounts.push(rowBundle);
  });

  return { vocab, bigramCounts, prevCounts, rowCounts, holdoutCounts };
}

function logProb(tokens, counts, excludedBundle) {
  const outcomeCount = counts.vocab.size + 1;
  let total = 0;
  for (const [prev, next] of transitions(tokens)) {
    const key = `${prev}\t${next}`;
    const bigramCount = (counts.bigramCounts.get(key) ?? 0) - (excludedBundle?.bigrams.get(key) ?? 0);
    const prevCount = (counts.prevCounts.get(prev) ?? 0) - (excludedBundle?.prevs.get(prev) ?? 0);
    total += Math.log((bigramCount + ALPHA) / (prevCount + ALPHA * outcomeCount));
  }
  return total;
}

function scoreDirection(records, holdoutKeyFn) {
  const usable = records.filter((record) => record.tokens.length > 1);
  const counts = buildCounts(usable, holdoutKeyFn);
  let storedHigher = 0;
  let reversedHigher = 0;
  let ties = 0;
  let diffSum = 0;
  const diffs = [];
  const heldOutSizes = [];

  usable.forEach((record, rowIndex) => {
    const holdoutKey = holdoutKeyFn(record, rowIndex);
    const excludedBundle = counts.holdoutCounts.get(holdoutKey) ?? counts.rowCounts[rowIndex];
    const heldOutTransitionCount = [...excludedBundle.prevs.values()].reduce((sum, value) => sum + value, 0);
    heldOutSizes.push(heldOutTransitionCount);
    const stored = logProb(record.tokens, counts, excludedBundle);
    const reversed = logProb([...record.tokens].reverse(), counts, excludedBundle);
    const diff = (stored - reversed) / (record.tokens.length + 1);
    diffs.push(diff);
    diffSum += diff;
    if (Math.abs(diff) < 1e-12) ties++;
    else if (diff > 0) storedHigher++;
    else reversedHigher++;
  });

  diffs.sort((a, b) => a - b);
  heldOutSizes.sort((a, b) => a - b);
  return {
    rows: usable.length,
    tokens: usable.reduce((sum, record) => sum + record.tokens.length, 0),
    unique_tokens: counts.vocab.size,
    stored_higher: storedHigher,
    reversed_higher: reversedHigher,
    ties,
    stored_win_share: usable.length ? storedHigher / usable.length : 0,
    mean_stored_minus_reversed_per_transition: usable.length ? diffSum / usable.length : 0,
    median_stored_minus_reversed_per_transition: diffs[Math.floor(diffs.length / 2)] ?? 0,
    median_heldout_transitions: heldOutSizes[Math.floor(heldOutSizes.length / 2)] ?? 0,
    max_heldout_transitions: heldOutSizes[heldOutSizes.length - 1] ?? 0,
    holdout_blocks: counts.holdoutCounts.size,
  };
}

function exactCollapse(records) {
  const byKey = new Map();
  for (const record of records) {
    const key = record.tokens.join(' ');
    const current = byKey.get(key);
    if (current) {
      current.duplicate_weight += record.duplicate_weight ?? 1;
      current.source_ids.push(record.id);
    } else {
      byKey.set(key, {
        ...record,
        tokens: [...record.tokens],
        duplicate_weight: record.duplicate_weight ?? 1,
        source_ids: [record.id],
      });
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

function collapseByKey(records, keyFn, policyName) {
  const groups = new Map();
  for (const record of records) {
    const key = keyFn(record);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(record);
  }
  return chooseRepresentatives(groups, policyName);
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
      const deleted = tokens.filter((_, tokenIndex) => tokenIndex !== pos);
      addSignature(`del:${tokens.length - 1}:${deleted.join(' ')}`, index);
    }
  });

  const groups = new Map();
  records.forEach((record, index) => {
    const rootIndex = uf.find(index);
    if (!groups.has(rootIndex)) groups.set(rootIndex, []);
    groups.get(rootIndex).push(record);
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

function poolShuffle(records, poolKeyFn, rng, label) {
  const pools = new Map();
  for (const record of records) {
    record.tokens.forEach((token, tokenIndex) => {
      const key = poolKeyFn(record, tokenIndex);
      if (!pools.has(key)) pools.set(key, []);
      pools.get(key).push(token);
    });
  }
  for (const pool of pools.values()) shuffleInPlace(pool, rng);
  const cursors = new Map();
  return records.map((record, rowIndex) => ({
    ...record,
    id: `${record.id}_${label}_${rowIndex}`,
    tokens: record.tokens.map((_, tokenIndex) => {
      const key = poolKeyFn(record, tokenIndex);
      const cursor = cursors.get(key) ?? 0;
      cursors.set(key, cursor + 1);
      return pools.get(key)[cursor];
    }),
  }));
}

function makeNull(records, control, rng) {
  if (control === 'global_token_shuffle') {
    const allTokens = shuffleInPlace(records.flatMap((record) => record.tokens), rng);
    let cursor = 0;
    return records.map((record, rowIndex) => {
      const tokens = allTokens.slice(cursor, cursor + record.tokens.length);
      cursor += record.tokens.length;
      return { ...record, id: `${record.id}_global_${rowIndex}`, tokens };
    });
  }
  if (control === 'row_internal_shuffle') {
    return records.map((record, rowIndex) => ({
      ...record,
      id: `${record.id}_row_${rowIndex}`,
      tokens: shuffleInPlace([...record.tokens], rng),
    }));
  }
  if (control === 'position_slot_shuffle') {
    return poolShuffle(records, (record, tokenIndex) => `${record.tokens.length}|${tokenIndex}`, rng, 'slot');
  }
  if (control === 'edge_frame_shuffle') {
    const interiors = shuffleInPlace(records.flatMap((record) => record.tokens.slice(1, -1)), rng);
    let cursor = 0;
    return records.map((record, rowIndex) => {
      if (record.tokens.length <= 2) return { ...record, id: `${record.id}_edge_${rowIndex}` };
      const interior = interiors.slice(cursor, cursor + record.tokens.length - 2);
      cursor += record.tokens.length - 2;
      return {
        ...record,
        id: `${record.id}_edge_${rowIndex}`,
        tokens: [record.tokens[0], ...interior, record.tokens[record.tokens.length - 1]],
      };
    });
  }
  if (control === 'register_position_shuffle') {
    return poolShuffle(records, (record, tokenIndex) => `${registerKey(record)}|${record.tokens.length}|${tokenIndex}`, rng, 'regslot');
  }
  if (control === 'register_edge_interior_shuffle') {
    const pools = new Map();
    for (const record of records) {
      if (record.tokens.length <= 2) continue;
      const key = `${registerKey(record)}|${edgeKey(record)}`;
      if (!pools.has(key)) pools.set(key, []);
      pools.get(key).push(...record.tokens.slice(1, -1));
    }
    for (const pool of pools.values()) shuffleInPlace(pool, rng);
    const cursors = new Map();
    return records.map((record, rowIndex) => {
      if (record.tokens.length <= 2) return { ...record, id: `${record.id}_regedge_${rowIndex}` };
      const key = `${registerKey(record)}|${edgeKey(record)}`;
      const cursor = cursors.get(key) ?? 0;
      cursors.set(key, cursor + record.tokens.length - 2);
      const interior = pools.get(key).slice(cursor, cursor + record.tokens.length - 2);
      return {
        ...record,
        id: `${record.id}_regedge_${rowIndex}`,
        tokens: [record.tokens[0], ...interior, record.tokens[record.tokens.length - 1]],
      };
    });
  }
  throw new Error(`Unknown control ${control}`);
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

function loadIndusExact() {
  return exactCollapse(loadCsv(path.join(reportsDir, 'lipi_scope_rows.csv'))
    .filter((row) => row.readiness_bucket === 'lipi_numeric_clean_candidate')
    .map((row, index) => ({
      id: row.id || `ivc_${index + 1}`,
      cisi: row.cisi,
      site: row.site,
      type: row.type,
      material: row.material,
      symbol: row.symbol,
      direction: row.direction,
      tokens: parseTokens(row.text),
      duplicate_weight: 1,
    }))
    .filter((row) => row.tokens.length >= 2));
}

function runNulls(corpusName, scopeName, holdoutPolicy, records, holdoutKeyFn, observed) {
  const controls = [
    'global_token_shuffle',
    'row_internal_shuffle',
    'position_slot_shuffle',
    'edge_frame_shuffle',
    'register_position_shuffle',
    'register_edge_interior_shuffle',
  ];
  const iterationRows = [];
  const summaryRows = [];

  for (const control of controls) {
    const values = [];
    for (let iteration = 0; iteration < NULL_ITERATIONS; iteration++) {
      const rng = makeRng(hashString(`${corpusName}:${scopeName}:${holdoutPolicy}:${control}:${iteration}`));
      const score = scoreDirection(makeNull(records, control, rng), holdoutKeyFn);
      values.push(score.stored_win_share);
      iterationRows.push({
        corpus: corpusName,
        scope: scopeName,
        holdout_policy: holdoutPolicy,
        control,
        iteration: iteration + 1,
        stored_win_share: round(score.stored_win_share),
        mean_diff: round(score.mean_stored_minus_reversed_per_transition),
      });
    }
    const stats = summarize(values);
    summaryRows.push({
      corpus: corpusName,
      scope: scopeName,
      holdout_policy: holdoutPolicy,
      control,
      metric: 'stored_win_share',
      iterations: NULL_ITERATIONS,
      observed: round(observed.stored_win_share),
      null_mean: round(stats.mean),
      null_p05: round(stats.p05),
      null_median: round(stats.median),
      null_p95: round(stats.p95),
      null_max: round(stats.max),
      null_ge_observed_share: round(values.filter((value) => value >= observed.stored_win_share).length / values.length),
    });
  }
  return { iterationRows, summaryRows };
}

function formatResult(corpus, scope, holdoutPolicy, source, records, score, nullRows) {
  return {
    corpus,
    scope,
    holdout_policy: holdoutPolicy,
    source,
    rows: score.rows,
    tokens: score.tokens,
    unique_tokens: score.unique_tokens,
    holdout_blocks: score.holdout_blocks,
    median_heldout_transitions: score.median_heldout_transitions,
    max_heldout_transitions: score.max_heldout_transitions,
    stored_higher: score.stored_higher,
    reversed_higher: score.reversed_higher,
    ties: score.ties,
    stored_win_share: round(score.stored_win_share),
    mean_stored_minus_reversed_per_transition: round(score.mean_stored_minus_reversed_per_transition),
    median_stored_minus_reversed_per_transition: round(score.median_stored_minus_reversed_per_transition),
    max_null_ge_observed_share: round(Math.max(...nullRows.map((row) => Number(row.null_ge_observed_share)), 0)),
    input_records: records.length,
  };
}

const exactRecords = loadIndusExact();
const top10Records = topEdgeRemoved(exactRecords, 10);
const harshRecords = oneEditFamilyCollapse(top10Records);
const registerEdgeCollapsed = collapseByKey(
  top10Records,
  (record) => `${registerKey(record)}|${edgeKey(record)}`,
  'register_edge_family',
);

const scopes = [
  {
    corpus: 'Indus_Lipi',
    scope: 'exact_sequence_collapsed',
    source: 'data/open_prototype/reports/lipi_scope_rows.csv',
    records: exactRecords,
  },
  {
    corpus: 'Indus_Lipi',
    scope: 'top10_edge_removed_one_edit_family_collapsed',
    source: 'data/open_prototype/reports/lipi_scope_rows.csv',
    records: harshRecords,
  },
  {
    corpus: 'Indus_Lipi',
    scope: 'top10_edge_removed_register_edge_family_collapsed',
    source: 'data/open_prototype/reports/lipi_scope_rows.csv',
    records: registerEdgeCollapsed,
  },
];

const holdoutPolicies = [
  {
    name: 'leave_one_row_out',
    key: (record, rowIndex) => `row:${rowIndex}`,
  },
  {
    name: 'leave_site_out',
    key: (record) => `site:${normalizeBlockValue(record.site)}`,
  },
  {
    name: 'leave_site_type_out',
    key: (record) => `site_type:${normalizeBlockValue(record.site)}|${normalizeBlockValue(record.type)}`,
  },
  {
    name: 'leave_site_type_symbol_out',
    key: (record) => `site_type_symbol:${normalizeBlockValue(record.site)}|${normalizeBlockValue(record.type)}|${normalizeBlockValue(record.symbol)}`,
  },
  {
    name: 'leave_register_edge_out',
    key: (record) => `register_edge:${registerKey(record)}|${edgeKey(record)}`,
  },
];

const outputRows = [];
const allNullSummaryRows = [];
const allNullIterationRows = [];

for (const scope of scopes) {
  for (const policy of holdoutPolicies) {
    const observed = scoreDirection(scope.records, policy.key);
    const { iterationRows, summaryRows } = runNulls(scope.corpus, scope.scope, policy.name, scope.records, policy.key, observed);
    outputRows.push(formatResult(scope.corpus, scope.scope, policy.name, scope.source, scope.records, observed, summaryRows));
    allNullSummaryRows.push(...summaryRows);
    allNullIterationRows.push(...iterationRows);
  }
}

const primaryRows = Object.fromEntries(outputRows.map((row) => [`${row.scope}__${row.holdout_policy}`, row]));
const summary = {
  date: '2026-05-29',
  generated_at_utc: new Date().toISOString(),
  purpose: 'Hostile block-holdout controls for the Vector 2 directionality candidate. These test whether stored-order asymmetry survives when whole provenance/register/edge families are removed from the training model.',
  method: {
    scoring: 'For each row, score stored order against reversed order after excluding all rows in the selected holdout block from the bigram model.',
    null_iterations_per_control: NULL_ITERATIONS,
    controls: [
      'global_token_shuffle',
      'row_internal_shuffle',
      'position_slot_shuffle',
      'edge_frame_shuffle',
      'register_position_shuffle',
      'register_edge_interior_shuffle',
    ],
    warning: 'This is still a Lipi T3 metadata/sign-layer result, not source-normalized direction evidence.',
  },
  primary_results: {
    exact_leave_site_type_symbol_out: primaryRows.exact_sequence_collapsed__leave_site_type_symbol_out,
    harsh_leave_site_type_symbol_out: primaryRows.top10_edge_removed_one_edit_family_collapsed__leave_site_type_symbol_out,
    harsh_leave_register_edge_out: primaryRows.top10_edge_removed_one_edit_family_collapsed__leave_register_edge_out,
    register_edge_collapsed_leave_site_type_symbol_out: primaryRows.top10_edge_removed_register_edge_family_collapsed__leave_site_type_symbol_out,
    register_edge_collapsed_leave_register_edge_out: primaryRows.top10_edge_removed_register_edge_family_collapsed__leave_register_edge_out,
  },
  rows: outputRows,
  artifact_files: [
    'data/open_prototype/tools/effective_unicity_directionality_block_controls.mjs',
    'data/open_prototype/reports/effective_unicity_directionality_block_controls_summary.json',
    'data/open_prototype/reports/effective_unicity_directionality_block_controls.csv',
    'data/open_prototype/reports/effective_unicity_directionality_block_null_summary.csv',
    'data/open_prototype/reports/effective_unicity_directionality_block_null_iterations.csv',
  ],
};

fs.writeFileSync(outSummary, `${JSON.stringify(summary, null, 2)}\n`);
fs.writeFileSync(outRows, toCsv(outputRows, [
  'corpus',
  'scope',
  'holdout_policy',
  'source',
  'rows',
  'tokens',
  'unique_tokens',
  'holdout_blocks',
  'median_heldout_transitions',
  'max_heldout_transitions',
  'stored_higher',
  'reversed_higher',
  'ties',
  'stored_win_share',
  'mean_stored_minus_reversed_per_transition',
  'median_stored_minus_reversed_per_transition',
  'max_null_ge_observed_share',
  'input_records',
]));
fs.writeFileSync(outNullSummary, toCsv(allNullSummaryRows, [
  'corpus',
  'scope',
  'holdout_policy',
  'control',
  'metric',
  'iterations',
  'observed',
  'null_mean',
  'null_p05',
  'null_median',
  'null_p95',
  'null_max',
  'null_ge_observed_share',
]));
fs.writeFileSync(outNullIterations, toCsv(allNullIterationRows, [
  'corpus',
  'scope',
  'holdout_policy',
  'control',
  'iteration',
  'stored_win_share',
  'mean_diff',
]));

console.log(JSON.stringify(summary, null, 2));
