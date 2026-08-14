// Formula-family controls for the directionality candidate.
//
// A formula family is a cluster of near-copy inscriptions — the same seal
// text with one sign swapped, or many seals cut under one workshop
// convention. If the corpus is mostly such families, the stored-vs-reversed
// order asymmetry could be a copying artifact rather than sequence
// structure. This script reads the clean numeric rows from
// lipi_scope_rows.csv and rescores the leave-block-out bigram test after
// collapsing families three ways: exact-text collapse, a one-edit collapse
// (rows joined by a one-substitution or one-deletion signature after
// removing the top-10 edge tokens), and a source-convention collapse that
// keeps one representative per site|type|material|symbol|cult|direction key.
// Ten scopes x three holdout policies are each tested against six shuffle
// nulls (200 iterations by default; --iterations=N overrides); nulls that
// exactly preserve the observed score are flagged degenerate and dropped
// from the admissible maximum. The summary embeds explicit fail gates (for
// example, stored-win share below 0.70 after the harshest collapse is
// fatal). Outputs: a JSON summary, per-cell CSV, family-membership CSV, and
// null summary/iteration CSVs in data/open_prototype/reports/. Survival
// narrows the formula-family objection; it proves nothing about reading
// direction, sign identity, or language.

import fs from 'fs';
import path from 'path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const inputRows = path.join(reportsDir, 'lipi_scope_rows.csv');
const outSummary = path.join(reportsDir, 'effective_unicity_directionality_formula_family_controls_summary.json');
const outRows = path.join(reportsDir, 'effective_unicity_directionality_formula_family_controls.csv');
const outFamilies = path.join(reportsDir, 'effective_unicity_directionality_formula_family_members.csv');
const outNullSummary = path.join(reportsDir, 'effective_unicity_directionality_formula_family_null_summary.csv');
const outNullIterations = path.join(reportsDir, 'effective_unicity_directionality_formula_family_null_iterations.csv');

const START = '<S>';
const END = '</S>';
const ALPHA = 0.1;
const DATE = '2026-05-29';
const NULL_ITERATIONS = Number(process.argv.find((arg) => arg.startsWith('--iterations='))?.split('=')[1] ?? 200);

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

function registerKey(record) {
  return [
    normalize(record.site),
    normalize(record.type),
    normalize(record.material),
    normalize(record.symbol),
    normalize(record.cult),
    normalize(record.direction),
  ].join('|');
}

function siteTypeSymbolKey(record) {
  return [normalize(record.site), normalize(record.type), normalize(record.symbol)].join('|');
}

function edgeKey(record) {
  return `${record.tokens.length}|${record.tokens[0] ?? ''}|${record.tokens.at(-1) ?? ''}`;
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

function emptyBundle() {
  return { bigrams: new Map(), prevs: new Map() };
}

function buildCounts(records, holdoutKeyFn) {
  const vocab = new Set();
  const bigramCounts = new Map();
  const prevCounts = new Map();
  const rowCounts = [];
  const holdoutCounts = new Map();

  records.forEach((record, rowIndex) => {
    const rowBundle = emptyBundle();
    const holdoutKey = holdoutKeyFn(record, rowIndex);
    if (!holdoutCounts.has(holdoutKey)) holdoutCounts.set(holdoutKey, emptyBundle());
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
    holdout_blocks: counts.holdoutCounts.size,
    median_heldout_transitions: heldOutSizes[Math.floor(heldOutSizes.length / 2)] ?? 0,
    max_heldout_transitions: heldOutSizes.at(-1) ?? 0,
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
      current.source_cisi.push(record.cisi);
    } else {
      byKey.set(key, {
        ...record,
        tokens: [...record.tokens],
        duplicate_weight: record.duplicate_weight ?? 1,
        source_ids: [record.id],
        source_cisi: [record.cisi],
      });
    }
  }
  return [...byKey.values()].sort((a, b) => a.tokens.join(' ').localeCompare(b.tokens.join(' ')));
}

function chooseRepresentatives(groups, policyName, familyRows) {
  return [...groups.values()].map((members, index) => {
    const familyId = `${policyName}_${String(index + 1).padStart(5, '0')}`;
    const representative = [...members].sort((a, b) => {
      const weightDiff = (b.duplicate_weight ?? 1) - (a.duplicate_weight ?? 1);
      if (weightDiff) return weightDiff;
      const lengthDiff = b.tokens.length - a.tokens.length;
      if (lengthDiff) return lengthDiff;
      return a.tokens.join(' ').localeCompare(b.tokens.join(' '));
    })[0];
    const allIds = members.flatMap((member) => member.source_ids ?? [member.id]);
    const allCisis = members.flatMap((member) => member.source_cisi ?? [member.cisi]);
    const texts = [...new Set(members.map((member) => member.text))].sort();
    familyRows.push({
      policy: policyName,
      family_id: familyId,
      family_size: members.length,
      family_source_weight: members.reduce((sum, member) => sum + (member.duplicate_weight ?? 1), 0),
      representative_cisi: representative.cisi,
      representative_text: representative.text,
      representative_tokens: representative.tokens.join(' '),
      source_convention_key: registerKey(representative),
      site_type_symbol_key: siteTypeSymbolKey(representative),
      direction: normalize(representative.direction),
      member_cisis: [...new Set(allCisis)].sort().join(';'),
      member_ids: [...new Set(allIds)].sort().join(';'),
      member_text_count: texts.length,
      member_texts: texts.slice(0, 40).join(';'),
    });
    return {
      ...representative,
      id: familyId,
      tokens: [...representative.tokens],
      duplicate_weight: representative.duplicate_weight ?? 1,
      family_id: familyId,
      family_policy: policyName,
      family_size: members.length,
      family_source_weight: members.reduce((sum, member) => sum + (member.duplicate_weight ?? 1), 0),
      source_ids: allIds,
      source_cisi: allCisis,
      family_member_texts: texts,
    };
  });
}

function collapseByKey(records, keyFn, policyName, familyRows) {
  const groups = new Map();
  for (const record of records) {
    const key = keyFn(record);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(record);
  }
  return chooseRepresentatives(groups, policyName, familyRows);
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

function editDistance(a, b) {
  let prev = Array.from({ length: b.length + 1 }, (_, index) => index);
  for (let i = 1; i <= a.length; i++) {
    const cur = [i];
    for (let j = 1; j <= b.length; j++) {
      cur.push(Math.min(
        prev[j] + 1,
        cur[j - 1] + 1,
        prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1),
      ));
    }
    prev = cur;
  }
  return prev[b.length];
}

function jaccard(a, b) {
  const sa = new Set(a);
  const sb = new Set(b);
  let intersection = 0;
  for (const token of sa) if (sb.has(token)) intersection++;
  const union = new Set([...sa, ...sb]).size;
  return union ? intersection / union : 0;
}

function formulaFamilyCollapse(records, policyName, maxEditDistance, familyRows) {
  const uf = new UnionFind(records.length);
  const byRegister = new Map();
  records.forEach((record, index) => {
    const key = registerKey(record);
    if (!byRegister.has(key)) byRegister.set(key, []);
    byRegister.get(key).push(index);
  });

  for (const indexes of byRegister.values()) {
    for (let left = 0; left < indexes.length; left++) {
      for (let right = left + 1; right < indexes.length; right++) {
        const a = records[indexes[left]].tokens;
        const b = records[indexes[right]].tokens;
        if (Math.abs(a.length - b.length) > maxEditDistance) continue;
        if (editDistance(a, b) <= maxEditDistance || jaccard(a, b) >= 0.75) {
          uf.union(indexes[left], indexes[right]);
        }
      }
    }
  }

  const groups = new Map();
  records.forEach((record, index) => {
    const rootIndex = uf.find(index);
    if (!groups.has(rootIndex)) groups.set(rootIndex, []);
    groups.get(rootIndex).push(record);
  });
  return chooseRepresentatives(groups, policyName, familyRows);
}

function oneEditFamilyCollapse(records, policyName, familyRows) {
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
  return chooseRepresentatives(groups, policyName, familyRows);
}

function topEdgeRemoved(records, topN = 10) {
  const edgeCounts = new Map();
  for (const record of records) {
    const first = record.tokens[0];
    const last = record.tokens.at(-1);
    edgeCounts.set(first, (edgeCounts.get(first) ?? 0) + 1);
    edgeCounts.set(last, (edgeCounts.get(last) ?? 0) + 1);
  }
  const top = new Set([...edgeCounts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, topN)
    .map(([token]) => token));
  return {
    records: records.filter((record) => !top.has(record.tokens[0]) && !top.has(record.tokens.at(-1))),
    removed_edge_tokens: [...top],
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
        tokens: [record.tokens[0], ...interior, record.tokens.at(-1)],
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
      const interior = (pools.get(key) ?? []).slice(cursor, cursor + record.tokens.length - 2);
      return {
        ...record,
        id: `${record.id}_regedge_${rowIndex}`,
        tokens: [record.tokens[0], ...interior, record.tokens.at(-1)],
      };
    });
  }
  throw new Error(`Unknown control ${control}`);
}

function summarize(values) {
  const sorted = [...values].sort((a, b) => a - b);
  const quantile = (p) => sorted[Math.min(sorted.length - 1, Math.max(0, Math.floor(p * (sorted.length - 1))))] ?? 0;
  return {
    mean: values.reduce((sum, value) => sum + value, 0) / Math.max(1, values.length),
    p05: quantile(0.05),
    median: quantile(0.5),
    p95: quantile(0.95),
    max: sorted.at(-1) ?? 0,
  };
}

function round(value) {
  return Number.isFinite(value) ? Number(value.toFixed(6)) : null;
}

function runNulls(scopeName, holdoutPolicy, records, holdoutKeyFn, observed) {
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
      const rng = makeRng(hashString(`${scopeName}:${holdoutPolicy}:${control}:${iteration}`));
      const score = scoreDirection(makeNull(records, control, rng), holdoutKeyFn);
      values.push(score.stored_win_share);
      iterationRows.push({
        corpus: 'Indus_Lipi',
        scope: scopeName,
        holdout_policy: holdoutPolicy,
        control,
        iteration: iteration + 1,
        stored_win_share: round(score.stored_win_share),
        mean_diff: round(score.mean_stored_minus_reversed_per_transition),
      });
    }
    const stats = summarize(values);
    const degenerateIdentity = values.every((value) => Math.abs(value - observed.stored_win_share) < 1e-12);
    summaryRows.push({
      corpus: 'Indus_Lipi',
      scope: scopeName,
      holdout_policy: holdoutPolicy,
      control,
      null_control_status: degenerateIdentity
        ? 'degenerate_identity_preserving_control_excluded_from_admissible_max'
        : 'admissible',
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

function formatResult(scope, holdoutPolicy, records, score, nullRows) {
  const admissibleRows = nullRows.filter((row) => row.null_control_status === 'admissible');
  const degenerateControls = nullRows
    .filter((row) => row.null_control_status !== 'admissible')
    .map((row) => row.control);
  return {
    corpus: 'Indus_Lipi',
    scope,
    holdout_policy: holdoutPolicy,
    source: 'data/open_prototype/reports/lipi_scope_rows.csv',
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
    max_null_ge_observed_share: round(Math.max(...admissibleRows.map((row) => Number(row.null_ge_observed_share)), 0)),
    max_admissible_null_ge_observed_share: round(Math.max(...admissibleRows.map((row) => Number(row.null_ge_observed_share)), 0)),
    max_all_null_ge_observed_share: round(Math.max(...nullRows.map((row) => Number(row.null_ge_observed_share)), 0)),
    degenerate_null_controls: degenerateControls.join(';'),
    input_records: records.length,
  };
}

const rawRecords = loadCsv(inputRows)
  .filter((row) => row.readiness_bucket === 'lipi_numeric_clean_candidate')
  .map((row, index) => ({
    id: row.id || `ivc_${index + 1}`,
    cisi: row.cisi,
    site: row.site,
    type: row.type,
    material: row.material,
    symbol: row.symbol,
    cult: row.cult,
    direction: row.direction,
    text: row.text,
    tokens: parseTokens(row.text),
    duplicate_weight: 1,
  }))
  .filter((row) => row.tokens.length >= 2);

const exactRecords = exactCollapse(rawRecords);
const edgeFiltered = topEdgeRemoved(exactRecords, 10);
const top10Records = edgeFiltered.records;
const familyRows = [];
const harshOneEditRecords = oneEditFamilyCollapse(top10Records, 'one_edit_family_global', familyRows);

const scopes = [
  {
    name: 'exact_text_collapsed',
    records: exactRecords,
  },
  {
    name: 'top10_edge_removed_exact_text_collapsed',
    records: top10Records,
  },
  {
    name: 'top10_edge_removed_one_edit_family_collapsed',
    records: harshOneEditRecords,
  },
  {
    name: 'exact_text_source_convention_collapsed',
    records: collapseByKey(exactRecords, (record) => registerKey(record), 'exact_source_convention', familyRows),
  },
  {
    name: 'top10_edge_removed_source_convention_collapsed',
    records: collapseByKey(top10Records, (record) => registerKey(record), 'top10_source_convention', familyRows),
  },
  {
    name: 'top10_edge_removed_one_edit_family_source_convention_collapsed',
    records: collapseByKey(harshOneEditRecords, (record) => registerKey(record), 'harsh_one_edit_source_convention', familyRows),
  },
  {
    name: 'exact_text_collapsed_RL_only',
    records: exactRecords.filter((record) => normalize(record.direction) === 'R/L'),
  },
  {
    name: 'exact_text_collapsed_LR_only',
    records: exactRecords.filter((record) => normalize(record.direction) === 'L/R'),
  },
  {
    name: 'top10_edge_removed_one_edit_family_collapsed_RL_only',
    records: harshOneEditRecords.filter((record) => normalize(record.direction) === 'R/L'),
  },
  {
    name: 'top10_edge_removed_one_edit_family_collapsed_LR_only',
    records: harshOneEditRecords.filter((record) => normalize(record.direction) === 'L/R'),
  },
];

const holdoutPolicies = [
  {
    name: 'leave_one_unit_out',
    key: (record, rowIndex) => `family:${record.family_id ?? record.id ?? rowIndex}`,
  },
  {
    name: 'leave_source_convention_out',
    key: (record) => `source_convention:${registerKey(record)}`,
  },
  {
    name: 'leave_edge_frame_out',
    key: (record) => `edge_frame:${edgeKey(record)}`,
  },
];

const outputRows = [];
const allNullSummaryRows = [];
const allNullIterationRows = [];

for (const scope of scopes) {
  for (const policy of holdoutPolicies) {
    const observed = scoreDirection(scope.records, policy.key);
    const { iterationRows, summaryRows } = runNulls(scope.name, policy.name, scope.records, policy.key, observed);
    outputRows.push(formatResult(scope.name, policy.name, scope.records, observed, summaryRows));
    allNullSummaryRows.push(...summaryRows);
    allNullIterationRows.push(...iterationRows);
  }
}

const primaryRows = Object.fromEntries(outputRows.map((row) => [`${row.scope}__${row.holdout_policy}`, row]));
const summary = {
  date: DATE,
  generated_at_utc: new Date().toISOString(),
  purpose: 'Hostile source/formula-family controls for the Vector 2 directionality candidate. These test whether stored-order asymmetry survives after collapsing near-copy formula families built only from available Lipi metadata fields.',
  source_scope: {
    input: 'data/open_prototype/reports/lipi_scope_rows.csv',
    raw_lipi_numeric_clean_rows_with_len_ge_2: rawRecords.length,
    exact_sequence_collapsed_rows: exactRecords.length,
    top10_edge_removed_exact_rows: top10Records.length,
    top10_edge_removed_one_edit_family_rows: harshOneEditRecords.length,
    top_removed_edge_tokens: edgeFiltered.removed_edge_tokens,
  },
  method: {
    scoring: 'For each row, score stored order against reversed order after excluding either the row/family, source-convention block, or edge-frame block from the bigram model.',
    alpha: ALPHA,
    null_iterations_per_control: NULL_ITERATIONS,
    controls: [
      'global_token_shuffle',
      'row_internal_shuffle',
      'position_slot_shuffle',
      'edge_frame_shuffle',
      'register_position_shuffle',
      'register_edge_interior_shuffle',
    ],
    null_control_policy: 'Controls that exactly preserve the observed score in every iteration are marked degenerate and excluded from max_admissible_null_ge_observed_share. This matters after source-convention collapse, where source-convention-preserving position shuffles can become identity controls.',
    formula_family_definitions: {
      source_convention_key: 'site|type|material|symbol|cult|direction; this is the strongest metadata-only proxy used here for source/workshop/register/editorial convention.',
      one_edit_family_global: 'After top-edge removal, connect rows sharing a one-substitution wildcard or one-token-deletion signature, matching the existing harsh directionality scope.',
      source_convention_collapsed: 'One deterministic representative per source_convention_key; applied to exact text, top-edge removed, and top-edge-plus-one-edit scopes.',
    },
    fail_gates: {
      fatal: [
        'harsh source-convention-collapsed stored-win share < 0.70',
        'mean stored-minus-reversed per transition <= 0',
        'any null/control has null_ge_observed_share > 0.10',
        'signal survives only in R/L while L/R is reversed, tied, or too small to interpret unless claim is explicitly R/L-limited',
        'top-edge removal changes survival into failure',
      ],
      warning_not_fatal: [
        'harsh source-convention-collapsed stored-win share between 0.70 and 0.80',
        'L/R subset is positive but underpowered',
        'source-convention collapse drops stored-win share by more than 0.10 from row/family holdout',
      ],
    },
    interpretation_boundary: 'This remains a Lipi T3 metadata/sign-layer test. Survival narrows formula-family objections but does not validate physical source direction, sign identity, sign meaning, phonetics, language family, or translation.',
  },
  primary_results: {
    exact_leave_source_convention: primaryRows.exact_text_collapsed__leave_source_convention_out,
    top10_leave_source_convention: primaryRows.top10_edge_removed_exact_text_collapsed__leave_source_convention_out,
    harsh_leave_source_convention: primaryRows.top10_edge_removed_one_edit_family_collapsed__leave_source_convention_out,
    exact_source_convention_collapsed: primaryRows.exact_text_source_convention_collapsed__leave_one_unit_out,
    top10_source_convention_collapsed: primaryRows.top10_edge_removed_source_convention_collapsed__leave_one_unit_out,
    harsh_source_convention_collapsed: primaryRows.top10_edge_removed_one_edit_family_source_convention_collapsed__leave_one_unit_out,
    harsh_source_convention_collapsed_leave_edge_frame: primaryRows.top10_edge_removed_one_edit_family_source_convention_collapsed__leave_edge_frame_out,
    exact_RL_only: primaryRows.exact_text_collapsed_RL_only__leave_source_convention_out,
    exact_LR_only: primaryRows.exact_text_collapsed_LR_only__leave_source_convention_out,
    harsh_RL_only: primaryRows.top10_edge_removed_one_edit_family_collapsed_RL_only__leave_source_convention_out,
    harsh_LR_only: primaryRows.top10_edge_removed_one_edit_family_collapsed_LR_only__leave_source_convention_out,
  },
  rows: outputRows,
  artifact_files: [
    'data/open_prototype/tools/effective_unicity_directionality_formula_family_controls.mjs',
    'data/open_prototype/reports/effective_unicity_directionality_formula_family_controls_summary.json',
    'data/open_prototype/reports/effective_unicity_directionality_formula_family_controls.csv',
    'data/open_prototype/reports/effective_unicity_directionality_formula_family_members.csv',
    'data/open_prototype/reports/effective_unicity_directionality_formula_family_null_summary.csv',
    'data/open_prototype/reports/effective_unicity_directionality_formula_family_null_iterations.csv',
  ],
  accepted_claims_increment: 0,
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
  'max_admissible_null_ge_observed_share',
  'max_all_null_ge_observed_share',
  'degenerate_null_controls',
  'input_records',
]));
fs.writeFileSync(outFamilies, toCsv(familyRows, [
  'policy',
  'family_id',
  'family_size',
  'family_source_weight',
  'representative_cisi',
  'representative_text',
  'representative_tokens',
  'source_convention_key',
  'site_type_symbol_key',
  'direction',
  'member_cisis',
  'member_ids',
  'member_text_count',
  'member_texts',
]));
fs.writeFileSync(outNullSummary, toCsv(allNullSummaryRows, [
  'corpus',
  'scope',
  'holdout_policy',
  'control',
  'null_control_status',
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
