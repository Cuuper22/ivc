import fs from 'fs';
import path from 'path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const knownScriptsDir = path.join(root, 'data', 'open_prototype', 'known_scripts');
const nonlingDir = path.join(root, 'data', 'open_prototype', 'nonlinguistic', 'sproat2014');
const outSummary = path.join(reportsDir, 'effective_unicity_directionality_comparator_summary.json');
const outRows = path.join(reportsDir, 'effective_unicity_directionality_comparator.csv');
const outNullSummary = path.join(reportsDir, 'effective_unicity_directionality_null_summary.csv');
const outNullIterations = path.join(reportsDir, 'effective_unicity_directionality_null_iterations.csv');

const START = '<S>';
const END = '</S>';
const ALPHA = 0.1;
const NULL_ITERATIONS = Number(process.argv.find((arg) => arg.startsWith('--iterations='))?.split('=')[1] ?? 80);

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQuotes) {
      if (c === '"') {
        if (text[i + 1] === '"') {
          field += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        field += c;
      }
    } else if (c === '"') {
      inQuotes = true;
    } else if (c === ',') {
      row.push(field);
      field = '';
    } else if (c === '\n') {
      row.push(field);
      rows.push(row);
      row = [];
      field = '';
    } else if (c !== '\r') {
      field += c;
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
  if (/[",\n\r]/.test(text)) {
    return `"${text.replaceAll('"', '""')}"`;
  }
  return `"${text}"`;
}

function toCsv(rows, columns) {
  return `${columns.map(csvEscape).join(',')}\n${rows
    .map((row) => columns.map((column) => csvEscape(row[column])).join(','))
    .join('\n')}\n`;
}

function parseLipiTokens(text) {
  return [...String(text).matchAll(/\d{3}/g)].map((match) => match[0]);
}

function parseLinearBSignTokens(line) {
  return String(line).trim().split(/\s+/).filter(Boolean).flatMap((token) => token.split('-').filter(Boolean));
}

function exactCollapse(records) {
  const byKey = new Map();
  for (const record of records) {
    if (record.tokens.length < 2) continue;
    const key = record.tokens.join(' ');
    const current = byKey.get(key);
    if (current) {
      current.duplicate_weight += record.duplicate_weight ?? 1;
      current.source_ids.push(...(record.source_ids ?? [record.id]));
    } else {
      byKey.set(key, {
        ...record,
        id: record.id,
        tokens: [...record.tokens],
        duplicate_weight: record.duplicate_weight ?? 1,
        source_ids: [...(record.source_ids ?? [record.id])],
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
    };
  });
}

function edgeFrameCollapse(records) {
  const groups = new Map();
  for (const record of records) {
    const tokens = record.tokens;
    const key = tokens.length <= 2 ? `exact:${tokens.join(' ')}` : `edge:${tokens.length}:${tokens[0]}:${tokens[tokens.length - 1]}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(record);
  }
  return chooseRepresentatives(groups, 'edge_frame');
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
    const ra = this.find(a);
    const rb = this.find(b);
    if (ra === rb) return;
    if (this.rank[ra] < this.rank[rb]) {
      this.parent[ra] = rb;
    } else if (this.rank[ra] > this.rank[rb]) {
      this.parent[rb] = ra;
    } else {
      this.parent[rb] = ra;
      this.rank[ra]++;
    }
  }
}

function oneEditFamilyCollapse(records) {
  const uf = new UnionFind(records.length);
  const signatureToFirst = new Map();
  const addSignature = (signature, index) => {
    const first = signatureToFirst.get(signature);
    if (first === undefined) {
      signatureToFirst.set(signature, index);
    } else {
      uf.union(first, index);
    }
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
  const top = new Set([...edgeCounts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, topN).map(([token]) => token));
  return records.filter((record) => !top.has(record.tokens[0]) && !top.has(record.tokens[record.tokens.length - 1]));
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

function logProb(tokens, counts, excludeIndex) {
  const outcomeCount = counts.vocab.size + 1;
  let total = 0;
  for (const [prev, next] of transitions(tokens)) {
    const key = `${prev}\t${next}`;
    const excludedBigram = counts.rowCounts[excludeIndex]?.bigrams.get(key) ?? 0;
    const excludedPrev = counts.rowCounts[excludeIndex]?.prevs.get(prev) ?? 0;
    const bigramCount = (counts.bigramCounts.get(key) ?? 0) - excludedBigram;
    const prevCount = (counts.prevCounts.get(prev) ?? 0) - excludedPrev;
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
  const diffs = [];
  for (let index = 0; index < usable.length; index++) {
    const record = usable[index];
    const stored = logProb(record.tokens, counts, index);
    const reversedTokens = [...record.tokens].reverse();
    const reversed = logProb(reversedTokens, counts, index);
    const diff = (stored - reversed) / (record.tokens.length + 1);
    diffs.push(diff);
    diffSum += diff;
    if (Math.abs(diff) < 1e-12) ties++;
    else if (diff > 0) storedHigher++;
    else reversedHigher++;
  }
  diffs.sort((a, b) => a - b);
  const median = diffs.length ? diffs[Math.floor(diffs.length / 2)] : 0;
  return {
    rows: usable.length,
    tokens: usable.reduce((sum, record) => sum + record.tokens.length, 0),
    unique_tokens: counts.vocab.size,
    stored_higher: storedHigher,
    reversed_higher: reversedHigher,
    ties,
    stored_win_share: usable.length ? storedHigher / usable.length : 0,
    mean_stored_minus_reversed_per_transition: usable.length ? diffSum / usable.length : 0,
    median_stored_minus_reversed_per_transition: median,
  };
}

function makeRng(seed) {
  let state = seed >>> 0;
  return () => {
    state = (1664525 * state + 1013904223) >>> 0;
    return state / 0x100000000;
  };
}

function shuffleInPlace(array, rng) {
  for (let index = array.length - 1; index > 0; index--) {
    const swapIndex = Math.floor(rng() * (index + 1));
    [array[index], array[swapIndex]] = [array[swapIndex], array[index]];
  }
  return array;
}

function makeNull(records, control, rng) {
  if (control === 'row_internal_shuffle') {
    return records.map((record, index) => ({
      ...record,
      id: `${record.id}_row_shuffle_${index}`,
      tokens: shuffleInPlace([...record.tokens], rng),
    }));
  }
  if (control === 'global_token_shuffle') {
    const allTokens = shuffleInPlace(records.flatMap((record) => record.tokens), rng);
    let cursor = 0;
    return records.map((record, index) => {
      const tokens = allTokens.slice(cursor, cursor + record.tokens.length);
      cursor += record.tokens.length;
      return { ...record, id: `${record.id}_global_shuffle_${index}`, tokens };
    });
  }
  if (control === 'edge_frame_shuffle') {
    const interiors = shuffleInPlace(records.flatMap((record) => record.tokens.slice(1, -1)), rng);
    let cursor = 0;
    return records.map((record, index) => {
      if (record.tokens.length <= 2) return { ...record, id: `${record.id}_edge_shuffle_${index}` };
      const interior = interiors.slice(cursor, cursor + record.tokens.length - 2);
      cursor += record.tokens.length - 2;
      return { ...record, id: `${record.id}_edge_shuffle_${index}`, tokens: [record.tokens[0], ...interior, record.tokens[record.tokens.length - 1]] };
    });
  }
  if (control === 'position_slot_shuffle') {
    const pools = new Map();
    for (const record of records) {
      record.tokens.forEach((token, index) => {
        const key = `${record.tokens.length}\t${index}`;
        if (!pools.has(key)) pools.set(key, []);
        pools.get(key).push(token);
      });
    }
    for (const pool of pools.values()) shuffleInPlace(pool, rng);
    const cursors = new Map();
    return records.map((record, rowIndex) => ({
      ...record,
      id: `${record.id}_slot_shuffle_${rowIndex}`,
      tokens: record.tokens.map((_, index) => {
        const key = `${record.tokens.length}\t${index}`;
        const cursor = cursors.get(key) ?? 0;
        cursors.set(key, cursor + 1);
        return pools.get(key)[cursor];
      }),
    }));
  }
  throw new Error(`Unknown control: ${control}`);
}

function summarize(values) {
  const sorted = [...values].sort((a, b) => a - b);
  const quantile = (p) => sorted[Math.min(sorted.length - 1, Math.max(0, Math.floor(p * (sorted.length - 1))))] ?? 0;
  const mean = values.reduce((sum, value) => sum + value, 0) / values.length;
  return { mean, p05: quantile(0.05), median: quantile(0.5), p95: quantile(0.95), max: sorted[sorted.length - 1] ?? 0 };
}

function runNulls(corpusName, scopeName, records, observed) {
  const controls = ['global_token_shuffle', 'row_internal_shuffle', 'position_slot_shuffle', 'edge_frame_shuffle'];
  const iterationRows = [];
  const summaryRows = [];
  for (const control of controls) {
    const values = [];
    for (let iteration = 0; iteration < NULL_ITERATIONS; iteration++) {
      const rng = makeRng(hashString(`${corpusName}:${scopeName}:${control}:${iteration}`));
      const score = scoreDirection(makeNull(records, control, rng));
      values.push(score.stored_win_share);
      iterationRows.push({
        corpus: corpusName,
        scope: scopeName,
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

function hashString(text) {
  let hash = 2166136261;
  for (let index = 0; index < text.length; index++) {
    hash ^= text.charCodeAt(index);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}

function round(value) {
  return Number.isFinite(value) ? Number(value.toFixed(6)) : null;
}

function formatRecord(corpus, systemClass, scope, source, records, score, nullSummaryRows) {
  const maxNullGe = Math.max(...nullSummaryRows.map((row) => Number(row.null_ge_observed_share)), 0);
  return {
    corpus,
    system_class: systemClass,
    scope,
    source,
    rows: score.rows,
    tokens: score.tokens,
    unique_tokens: score.unique_tokens,
    stored_higher: score.stored_higher,
    reversed_higher: score.reversed_higher,
    ties: score.ties,
    stored_win_share: round(score.stored_win_share),
    mean_stored_minus_reversed_per_transition: round(score.mean_stored_minus_reversed_per_transition),
    median_stored_minus_reversed_per_transition: round(score.median_stored_minus_reversed_per_transition),
    max_null_ge_observed_share: round(maxNullGe),
    input_records: records.length,
  };
}

function loadIndusExact() {
  const rows = loadCsv(path.join(reportsDir, 'lipi_scope_rows.csv'))
    .filter((row) => row.readiness_bucket === 'lipi_numeric_clean_candidate')
    .map((row, index) => ({
      id: row.id || `ivc_${index + 1}`,
      tokens: parseLipiTokens(row.text),
      duplicate_weight: 1,
      source_ids: [row.id || `ivc_${index + 1}`],
    }))
    .filter((row) => row.tokens.length >= 2);
  return exactCollapse(rows);
}

function loadLinearB() {
  const rows = loadCsv(path.join(reportsDir, 'linear_b_series_d_row_inventory.csv'))
    .filter((row) => row.dataset_slice === 'real_series_d_default_clean' && row.ivc_p95_length_eligible === 'true')
    .map((row) => ({
      id: `linear_b_${row.row_index_1based}`,
      tokens: parseLinearBSignTokens(row.raw_sequence),
      duplicate_weight: 1,
      source_ids: [`linear_b_${row.row_index_1based}`],
    }))
    .filter((row) => row.tokens.length >= 2 && row.tokens.length <= 8);
  return exactCollapse(rows);
}

function loadSumTablets() {
  return loadCsv(path.join(knownScriptsDir, 'sumtablets', 'sumtablets_line_sequences.csv'))
    .map((row) => ({
      id: row.line_id,
      tokens: row.tokens.split(/\s+/).filter(Boolean),
      duplicate_weight: Number(row.duplicate_weight) || 1,
      source_ids: row.source_tablet_ids ? row.source_tablet_ids.split('|') : [row.line_id],
    }))
    .filter((row) => row.tokens.length >= 2);
}

function loadMayigP() {
  const rows = loadCsv(path.join(root, 'data', 'open_prototype', 'mayig', 'records_index.csv'))
    .map((row) => ({
      id: row.side_id,
      tokens: row.graphemes.split(/\s+/).filter(Boolean),
      duplicate_weight: 1,
      source_ids: [row.source_path || row.side_id],
    }))
    .filter((row) => row.tokens.length >= 2 && row.tokens.length <= 8);
  return exactCollapse(rows);
}

function loadCrosswalkPairedLayers() {
  const rows = loadCsv(path.join(reportsDir, 'crosswalk_alignment_pairs.csv'));
  const groups = new Map();
  for (const row of rows) {
    const key = `${row.lipi_id}\t${row.mayig_side_id}`;
    if (!groups.has(key)) {
      groups.set(key, {
        lipi_id: row.lipi_id,
        mayig_side_id: row.mayig_side_id,
        cisi: row.cisi,
        lipi: [],
        mayig: [],
      });
    }
    const group = groups.get(key);
    group.lipi.push({ position: Number(row.position_0based), token: row.lipi_sign });
    group.mayig.push({ position: Number(row.position_0based), token: row.mayig_sign });
  }

  const lipi = [];
  const mayig = [];
  for (const group of groups.values()) {
    const lipiTokens = group.lipi.sort((a, b) => a.position - b.position).map((entry) => entry.token).filter(Boolean);
    const mayigTokens = group.mayig.sort((a, b) => a.position - b.position).map((entry) => entry.token).filter(Boolean);
    if (lipiTokens.length >= 2 && lipiTokens.length <= 8 && mayigTokens.length === lipiTokens.length) {
      lipi.push({
        id: `crosswalk_lipi_${group.lipi_id}_${group.mayig_side_id}`,
        tokens: lipiTokens,
        duplicate_weight: 1,
        source_ids: [`${group.cisi}:${group.lipi_id}:${group.mayig_side_id}`],
      });
      mayig.push({
        id: `crosswalk_mayig_${group.lipi_id}_${group.mayig_side_id}`,
        tokens: mayigTokens,
        duplicate_weight: 1,
        source_ids: [`${group.cisi}:${group.lipi_id}:${group.mayig_side_id}`],
      });
    }
  }
  return { lipi: exactCollapse(lipi), mayig: exactCollapse(mayig) };
}

function loadSproat() {
  const rows = loadCsv(path.join(nonlingDir, 'sproat2014_extracted_sequences.csv'));
  const grouped = new Map();
  for (const row of rows) {
    const tokens = row.tokens.split('|').map((token) => token.trim()).filter(Boolean);
    if (tokens.length < 2) continue;
    if (!grouped.has(row.corpus)) grouped.set(row.corpus, []);
    grouped.get(row.corpus).push({
      id: row.sequence_id,
      tokens,
      duplicate_weight: Number(row.duplicate_weight) || 1,
      source_ids: row.source_ids ? row.source_ids.split('|') : [row.sequence_id],
    });
  }
  return grouped;
}

const corpusScopes = [];
const indusExact = loadIndusExact();
corpusScopes.push({
  corpus: 'Indus_Lipi',
  systemClass: 'unread_working_corpus',
  scope: 'exact_sequence_collapsed',
  source: 'data/open_prototype/reports/lipi_scope_rows.csv',
  records: indusExact,
});
corpusScopes.push({
  corpus: 'Indus_Lipi',
  systemClass: 'unread_working_corpus',
  scope: 'edge_frame_collapsed',
  source: 'data/open_prototype/reports/lipi_scope_rows.csv',
  records: edgeFrameCollapse(indusExact),
});
corpusScopes.push({
  corpus: 'Indus_Lipi',
  systemClass: 'unread_working_corpus',
  scope: 'one_edit_family_collapsed',
  source: 'data/open_prototype/reports/lipi_scope_rows.csv',
  records: oneEditFamilyCollapse(indusExact),
});
const indusTopEdgeRemoved = topEdgeRemoved(indusExact, 10);
corpusScopes.push({
  corpus: 'Indus_Lipi',
  systemClass: 'unread_working_corpus',
  scope: 'top10_edge_removed_exact_sequence_collapsed',
  source: 'data/open_prototype/reports/lipi_scope_rows.csv',
  records: indusTopEdgeRemoved,
});
corpusScopes.push({
  corpus: 'Indus_Lipi',
  systemClass: 'unread_working_corpus',
  scope: 'top10_edge_removed_one_edit_family_collapsed',
  source: 'data/open_prototype/reports/lipi_scope_rows.csv',
  records: oneEditFamilyCollapse(indusTopEdgeRemoved),
});
const mayigExact = loadMayigP();
const crosswalkPaired = loadCrosswalkPairedLayers();
corpusScopes.push({
  corpus: 'Mayig_P_open_wip',
  systemClass: 'unread_open_wip_transcription_layer',
  scope: 'p_namespace_length_2_to_8_exact_sequence_collapsed',
  source: 'data/open_prototype/mayig/records_index.csv',
  records: mayigExact,
});
corpusScopes.push({
  corpus: 'Mayig_P_open_wip',
  systemClass: 'unread_open_wip_transcription_layer',
  scope: 'p_namespace_top10_edge_removed_one_edit_family_collapsed',
  source: 'data/open_prototype/mayig/records_index.csv',
  records: oneEditFamilyCollapse(topEdgeRemoved(mayigExact, 10)),
});
corpusScopes.push({
  corpus: 'Lipi_Mayig_overlap_Lipi_side',
  systemClass: 'unread_matched_crosswalk_layer',
  scope: 'crosswalk_aligned_artifacts_lipi_signs_exact_collapsed',
  source: 'data/open_prototype/reports/crosswalk_alignment_pairs.csv',
  records: crosswalkPaired.lipi,
});
corpusScopes.push({
  corpus: 'Lipi_Mayig_overlap_Mayig_side',
  systemClass: 'unread_matched_crosswalk_layer',
  scope: 'crosswalk_aligned_artifacts_mayig_signs_exact_collapsed',
  source: 'data/open_prototype/reports/crosswalk_alignment_pairs.csv',
  records: crosswalkPaired.mayig,
});
corpusScopes.push({
  corpus: 'Linear_B_Series_D',
  systemClass: 'known_readable_script',
  scope: 'sign_tokens_ivc_length_cap_exact_sequence_collapsed',
  source: 'data/open_prototype/reports/linear_b_series_d_row_inventory.csv',
  records: loadLinearB(),
});
corpusScopes.push({
  corpus: 'SumTablets',
  systemClass: 'known_readable_administrative_script',
  scope: 'glyph_only_line_sequences_exact_collapsed',
  source: 'data/open_prototype/known_scripts/sumtablets/sumtablets_line_sequences.csv',
  records: loadSumTablets(),
});
for (const [corpus, records] of loadSproat().entries()) {
  corpusScopes.push({
    corpus,
    systemClass: 'real_world_nonlinguistic_or_ambiguous',
    scope: 'exact_collapsed_length_2_to_8',
    source: 'data/open_prototype/nonlinguistic/sproat2014/sproat2014_extracted_sequences.csv',
    records,
  });
}

const outputRows = [];
const allNullSummaries = [];
const allNullIterations = [];
for (const corpusScope of corpusScopes) {
  const score = scoreDirection(corpusScope.records);
  const { iterationRows, summaryRows } = runNulls(corpusScope.corpus, corpusScope.scope, corpusScope.records, score);
  allNullIterations.push(...iterationRows);
  allNullSummaries.push(...summaryRows);
  outputRows.push(formatRecord(
    corpusScope.corpus,
    corpusScope.systemClass,
    corpusScope.scope,
    corpusScope.source,
    corpusScope.records,
    score,
    summaryRows,
  ));
}

const indusPrimary = outputRows.find((row) => row.corpus === 'Indus_Lipi' && row.scope === 'top10_edge_removed_one_edit_family_collapsed');
const comparatorsAtOrAbove = outputRows
  .filter((row) => ![
    'Indus_Lipi',
    'Mayig_P_open_wip',
    'Lipi_Mayig_overlap_Lipi_side',
    'Lipi_Mayig_overlap_Mayig_side',
  ].includes(row.corpus) && Number(row.stored_win_share) >= Number(indusPrimary.stored_win_share))
  .map((row) => `${row.corpus}:${row.scope}`);
const mayigPrimary = outputRows.find((row) => row.corpus === 'Mayig_P_open_wip' && row.scope === 'p_namespace_top10_edge_removed_one_edit_family_collapsed');
const pairedLipi = outputRows.find((row) => row.corpus === 'Lipi_Mayig_overlap_Lipi_side');
const pairedMayig = outputRows.find((row) => row.corpus === 'Lipi_Mayig_overlap_Mayig_side');

const summary = {
  date: '2026-05-29',
  generated_at_utc: new Date().toISOString(),
  purpose: 'Directionality comparator for Vector 2: stored-order versus reversed-order likelihood under leave-one-row-out bigram scoring.',
  method: {
    scoring: 'For each row, subtract that row from the bigram model, score the stored token order and the reversed token order with add-alpha smoothing, and count stored-order wins.',
    alpha: ALPHA,
    controls: ['global_token_shuffle', 'row_internal_shuffle', 'position_slot_shuffle', 'edge_frame_shuffle'],
    null_iterations_per_control: NULL_ITERATIONS,
    interpretation_boundary: 'Directionality is structural evidence only. It is not phonetic, semantic, or language-family evidence without an external anchor.',
  },
  primary_boundary: {
    indus_primary_scope: 'top10_edge_removed_one_edit_family_collapsed',
    indus_primary_stored_win_share: indusPrimary?.stored_win_share,
    mayig_pressure_scope: 'p_namespace_top10_edge_removed_one_edit_family_collapsed',
    mayig_pressure_stored_win_share: mayigPrimary?.stored_win_share,
    paired_crosswalk_lipi_stored_win_share: pairedLipi?.stored_win_share,
    paired_crosswalk_mayig_stored_win_share: pairedMayig?.stored_win_share,
    comparator_systems_at_or_above_indus_primary: comparatorsAtOrAbove,
    interpretation: comparatorsAtOrAbove.length
      ? 'At least one comparator matches or exceeds the harsh Indus directionality scope, so directionality alone is not a writing-specific diagnostic.'
      : 'The harsh Indus directionality scope exceeds all current real-world comparators in this battery; this would still be structural-only until source normalization and stronger controls.',
  },
  rows: outputRows,
  artifact_files: [
    'data/open_prototype/tools/effective_unicity_directionality_comparator.mjs',
    'data/open_prototype/reports/effective_unicity_directionality_comparator_summary.json',
    'data/open_prototype/reports/effective_unicity_directionality_comparator.csv',
    'data/open_prototype/reports/effective_unicity_directionality_null_summary.csv',
    'data/open_prototype/reports/effective_unicity_directionality_null_iterations.csv',
  ],
};

fs.writeFileSync(outSummary, `${JSON.stringify(summary, null, 2)}\n`);
fs.writeFileSync(outRows, toCsv(outputRows, [
  'corpus',
  'system_class',
  'scope',
  'source',
  'rows',
  'tokens',
  'unique_tokens',
  'stored_higher',
  'reversed_higher',
  'ties',
  'stored_win_share',
  'mean_stored_minus_reversed_per_transition',
  'median_stored_minus_reversed_per_transition',
  'max_null_ge_observed_share',
  'input_records',
]));
fs.writeFileSync(outNullSummary, toCsv(allNullSummaries, [
  'corpus',
  'scope',
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
fs.writeFileSync(outNullIterations, toCsv(allNullIterations, [
  'corpus',
  'scope',
  'control',
  'iteration',
  'stored_win_share',
  'mean_diff',
]));

console.log(JSON.stringify(summary, null, 2));
