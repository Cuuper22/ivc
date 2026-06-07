import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const sourceDir = path.join(base, 'data', 'open_prototype', 'known_scripts', 'linear_b_series_d');
const sourcePath = path.join(sourceDir, 'Samples.txt');
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const lipiScopePath = path.join(reportsDir, 'lipi_scope_rows.csv');

const manifestPath = path.join(reportsDir, 'linear_b_series_d_source_manifest.json');
const rowInventoryPath = path.join(reportsDir, 'linear_b_series_d_row_inventory.csv');
const lengthDistributionPath = path.join(reportsDir, 'linear_b_series_d_length_distribution.csv');
const sequenceSummaryPath = path.join(reportsDir, 'linear_b_series_d_sequence_summary.csv');
const maskedSummaryPath = path.join(reportsDir, 'linear_b_series_d_masked_summary.csv');
const positionEntropyPath = path.join(reportsDir, 'linear_b_series_d_position_entropy.csv');
const controlIterationsPath = path.join(reportsDir, 'linear_b_series_d_control_iterations.csv');
const controlSummaryPath = path.join(reportsDir, 'linear_b_series_d_control_summary.csv');
const summaryJsonPath = path.join(reportsDir, 'linear_b_series_d_scarcity_summary.json');

const iterations = Number(process.env.IVC_LINEAR_B_CONTROL_ITERATIONS ?? 50);
const seedBase = 20260524;
const smoothing = 1;
const epsilon = 1e-9;

function toCsv(rows) {
  return `${rows
    .map((row) =>
      row
        .map((value) => {
          const text = String(value ?? '');
          return `"${text.replaceAll('"', '""')}"`;
        })
        .join(','),
    )
    .join('\n')}\n`;
}

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
      field = '';
      if (row.length > 1 || row[0] !== '') rows.push(row);
      row = [];
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

function parseLipiNumericTokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function parseWordTokens(line) {
  return line.trim().split(/\s+/).filter(Boolean);
}

function parseSignTokens(line) {
  return parseWordTokens(line).flatMap((token) => token.split('-').filter(Boolean));
}

function md5(filePath) {
  return crypto.createHash('md5').update(fs.readFileSync(filePath)).digest('hex');
}

function bump(map, key, by = 1) {
  map.set(key, (map.get(key) ?? 0) + by);
}

function addNested(map, keyA, keyB, by = 1) {
  if (!map.has(keyA)) map.set(keyA, new Map());
  bump(map.get(keyA), keyB, by);
}

function addKeyedCount(map, keys, token, by = 1) {
  addNested(map, keys.join('\t'), token, by);
}

function mapTotal(map) {
  let total = 0;
  for (const value of map.values()) total += value;
  return total;
}

function formatNumber(value, digits = 6) {
  return value === null || value === undefined || Number.isNaN(value) ? null : Number(value.toFixed(digits));
}

function mean(values) {
  return values.length ? values.reduce((sum, value) => sum + value, 0) / values.length : null;
}

function median(values) {
  if (!values.length) return null;
  const sorted = values.slice().sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
}

function quantile(values, q) {
  if (!values.length) return null;
  const sorted = values.slice().sort((a, b) => a - b);
  const index = (sorted.length - 1) * q;
  const lower = Math.floor(index);
  const upper = Math.ceil(index);
  if (lower === upper) return sorted[lower];
  return sorted[lower] + (sorted[upper] - sorted[lower]) * (index - lower);
}

function entropyBits(counts) {
  const total = mapTotal(counts);
  if (!total) return 0;
  let entropy = 0;
  for (const count of counts.values()) {
    const p = count / total;
    entropy -= p * Math.log2(p);
  }
  return entropy;
}

function mulberry32(seed) {
  return function random() {
    let t = (seed += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffle(array, rng) {
  const out = array.slice();
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function tokenBag(records) {
  return records.flatMap((record) => record.tokens);
}

function makeGeneratedRecord(source, tokens, control, iteration) {
  return {
    ...source,
    id: `${control}_${iteration}_${source.id}`,
    source_id: source.id,
    control,
    iteration,
    tokens,
  };
}

function generateLengthFrequencyShuffle(records, rng, iteration) {
  const bag = shuffle(tokenBag(records), rng);
  let offset = 0;
  return records.map((record) => {
    const tokens = bag.slice(offset, offset + record.tokens.length);
    offset += record.tokens.length;
    return makeGeneratedRecord(record, tokens, 'length_frequency_shuffle', iteration);
  });
}

function generateEdgeFrameShuffle(records, rng, iteration) {
  const singles = [];
  const interiors = [];
  for (const record of records) {
    if (record.tokens.length === 1) singles.push(record.tokens[0]);
    else interiors.push(...record.tokens.slice(1, -1));
  }
  const singleBag = shuffle(singles, rng);
  const interiorBag = shuffle(interiors, rng);
  let si = 0;
  let ii = 0;
  return records.map((record) => {
    const len = record.tokens.length;
    const tokens =
      len === 1
        ? [singleBag[si++]]
        : [record.tokens[0], ...interiorBag.slice(ii, ii + len - 2), record.tokens[len - 1]];
    if (len > 1) ii += len - 2;
    return makeGeneratedRecord(record, tokens, 'edge_frame_shuffle', iteration);
  });
}

function generatePositionSlotShuffle(records, rng, iteration) {
  const bags = new Map();
  for (const record of records) {
    for (let pos = 0; pos < record.tokens.length; pos++) {
      const key = `${record.tokens.length}\t${pos}`;
      if (!bags.has(key)) bags.set(key, []);
      bags.get(key).push(record.tokens[pos]);
    }
  }
  const shuffled = new Map([...bags.entries()].map(([key, values]) => [key, shuffle(values, rng)]));
  const offsets = new Map();
  return records.map((record) => {
    const tokens = [];
    for (let pos = 0; pos < record.tokens.length; pos++) {
      const key = `${record.tokens.length}\t${pos}`;
      const offset = offsets.get(key) ?? 0;
      tokens.push(shuffled.get(key)[offset]);
      offsets.set(key, offset + 1);
    }
    return makeGeneratedRecord(record, tokens, 'position_slot_shuffle', iteration);
  });
}

function exactCollapse(records) {
  const seen = new Map();
  for (const record of records) {
    const key = record.tokens.join(' ');
    if (!seen.has(key)) seen.set(key, { ...record, duplicate_weight: 1 });
    else seen.get(key).duplicate_weight++;
  }
  return [...seen.values()];
}

function duplicateStats(records) {
  const sequenceCounts = new Map();
  for (const record of records) bump(sequenceCounts, record.tokens.join(' '));
  const duplicateGroups = [...sequenceCounts.values()].filter((count) => count > 1);
  return {
    rows: records.length,
    tokens: records.reduce((sum, record) => sum + record.tokens.length, 0),
    unique_tokens: new Set(records.flatMap((record) => record.tokens)).size,
    exact_sequence_groups: sequenceCounts.size,
    exact_duplicate_groups: duplicateGroups.length,
    exact_duplicate_rows: duplicateGroups.reduce((sum, count) => sum + count, 0),
    exact_duplicate_row_share:
      records.length > 0 ? formatNumber(duplicateGroups.reduce((sum, count) => sum + count, 0) / records.length) : null,
    top_sequence_count: sequenceCounts.size ? Math.max(...sequenceCounts.values()) : 0,
  };
}

function transitionCounts(records) {
  const counts = new Map();
  const totals = new Map();
  for (const record of records) {
    const seq = ['<s>', ...record.tokens, '</s>'];
    for (let i = 0; i < seq.length - 1; i++) {
      addNested(counts, seq[i], seq[i + 1]);
      bump(totals, seq[i]);
    }
  }
  return { counts, totals };
}

function subtractTransitionCounts(global, row) {
  const counts = new Map();
  for (const [from, inner] of global.counts.entries()) counts.set(from, new Map(inner));
  const totals = new Map(global.totals);
  for (const [from, inner] of row.counts.entries()) {
    const target = counts.get(from);
    if (target) {
      for (const [to, value] of inner.entries()) {
        const next = (target.get(to) ?? 0) - value;
        if (next <= 0) target.delete(to);
        else target.set(to, next);
      }
      if (target.size === 0) counts.delete(from);
    }
  }
  for (const [from, value] of row.totals.entries()) {
    const next = (totals.get(from) ?? 0) - value;
    if (next <= 0) totals.delete(from);
    else totals.set(from, next);
  }
  return { counts, totals };
}

function transitionScore(tokens, train, vocabSize) {
  const seq = ['<s>', ...tokens, '</s>'];
  let score = 0;
  for (let i = 0; i < seq.length - 1; i++) {
    const from = seq[i];
    const to = seq[i + 1];
    const count = train.counts.get(from)?.get(to) ?? 0;
    const total = train.totals.get(from) ?? 0;
    score += Math.log((count + smoothing) / (total + smoothing * vocabSize));
  }
  return score;
}

function evaluateSequence(records) {
  const usable = records.filter((record) => record.tokens.length > 0);
  const collapsed = exactCollapse(usable);
  const vocab = [...new Set(collapsed.flatMap((record) => record.tokens))];
  const vocabSize = vocab.length + 2;
  const globalTransitions = transitionCounts(collapsed);
  const diffs = [];
  let rowsGtOne = 0;
  let storedHigher = 0;
  let reversedHigher = 0;
  let ties = 0;
  for (const record of collapsed) {
    if (record.tokens.length <= 1) continue;
    rowsGtOne++;
    const rowTransitions = transitionCounts([{ tokens: record.tokens }]);
    const train = subtractTransitionCounts(globalTransitions, rowTransitions);
    const storedScore = transitionScore(record.tokens, train, vocabSize);
    const reversedScore = transitionScore(record.tokens.slice().reverse(), train, vocabSize);
    const diff = storedScore - reversedScore;
    diffs.push(diff);
    if (diff > epsilon) storedHigher++;
    else if (diff < -epsilon) reversedHigher++;
    else ties++;
  }
  return {
    ...duplicateStats(usable),
    collapsed_rows: collapsed.length,
    collapsed_tokens: collapsed.reduce((sum, record) => sum + record.tokens.length, 0),
    collapsed_unique_tokens: vocab.length,
    rows_length_gt_1: rowsGtOne,
    stored_higher_than_reversed: storedHigher,
    reversed_higher_than_stored: reversedHigher,
    ties,
    stored_higher_share: rowsGtOne ? formatNumber(storedHigher / rowsGtOne) : null,
    mean_stored_minus_reversed: diffs.length ? formatNumber(mean(diffs)) : null,
    median_stored_minus_reversed: diffs.length ? formatNumber(median(diffs)) : null,
  };
}

function recordCounts(record) {
  const tokenCounts = new Map();
  const positionCounts = new Map();
  const lengthPositionCounts = new Map();
  const leftCounts = new Map();
  const rightCounts = new Map();
  const len = record.tokens.length;
  for (let i = 0; i < len; i++) {
    const token = record.tokens[i];
    bump(tokenCounts, token);
    addKeyedCount(positionCounts, [i], token);
    addKeyedCount(lengthPositionCounts, [len, i], token);
    addKeyedCount(leftCounts, [i === 0 ? '<s>' : record.tokens[i - 1]], token);
    addKeyedCount(rightCounts, [i === len - 1 ? '</s>' : record.tokens[i + 1]], token);
  }
  return { tokenCounts, positionCounts, lengthPositionCounts, leftCounts, rightCounts };
}

function buildGroupCounts(records) {
  const counts = {
    tokenCounts: new Map(),
    positionCounts: new Map(),
    lengthPositionCounts: new Map(),
    leftCounts: new Map(),
    rightCounts: new Map(),
  };
  for (const record of records) {
    const rowCounts = recordCounts(record);
    for (const [token, value] of rowCounts.tokenCounts.entries()) bump(counts.tokenCounts, token, value);
    for (const [key, inner] of rowCounts.positionCounts.entries()) {
      for (const [token, value] of inner.entries()) addNested(counts.positionCounts, key, token, value);
    }
    for (const [key, inner] of rowCounts.lengthPositionCounts.entries()) {
      for (const [token, value] of inner.entries()) addNested(counts.lengthPositionCounts, key, token, value);
    }
    for (const [key, inner] of rowCounts.leftCounts.entries()) {
      for (const [token, value] of inner.entries()) addNested(counts.leftCounts, key, token, value);
    }
    for (const [key, inner] of rowCounts.rightCounts.entries()) {
      for (const [token, value] of inner.entries()) addNested(counts.rightCounts, key, token, value);
    }
  }
  return counts;
}

function subtractTokenCounts(globalCounts, rowCounts) {
  const out = new Map(globalCounts);
  for (const [token, value] of rowCounts.entries()) {
    const next = (out.get(token) ?? 0) - value;
    if (next <= 0) out.delete(token);
    else out.set(token, next);
  }
  return out;
}

function subtractCountMapForKey(globalNested, rowNested, key) {
  const baseMap = globalNested.get(key) ?? new Map();
  const removeMap = rowNested.get(key) ?? new Map();
  if (removeMap.size === 0) return baseMap;
  const out = new Map(baseMap);
  for (const [token, value] of removeMap.entries()) {
    const next = (out.get(token) ?? 0) - value;
    if (next <= 0) out.delete(token);
    else out.set(token, next);
  }
  return out;
}

function rankFromScores(vocab, token, scoreFn) {
  const tokenScore = scoreFn(token);
  let better = 0;
  for (const candidate of vocab) {
    if (candidate === token) continue;
    const candidateScore = scoreFn(candidate);
    if (candidateScore > tokenScore || (candidateScore === tokenScore && candidate.localeCompare(token) < 0)) {
      better++;
    }
  }
  const rank = better + 1;
  return { rank, top1: rank === 1, top5: rank <= 5 };
}

function rankCountMap(counts, token, vocab) {
  return rankFromScores(vocab, token, (candidate) => counts.get(candidate) ?? 0);
}

function rankBidirectional(leftMap, rightMap, token, vocab, fallbackCounts) {
  const fallbackTotal = mapTotal(fallbackCounts);
  const leftTotal = mapTotal(leftMap);
  const rightTotal = mapTotal(rightMap);
  const vocabSize = Math.max(1, vocab.length);
  return rankFromScores(vocab, token, (candidate) => {
    const leftScore =
      leftTotal > 0
        ? Math.log(((leftMap.get(candidate) ?? 0) + smoothing) / (leftTotal + smoothing * vocabSize))
        : Math.log(((fallbackCounts.get(candidate) ?? 0) + smoothing) / (fallbackTotal + smoothing * vocabSize));
    const rightScore =
      rightTotal > 0
        ? Math.log(((rightMap.get(candidate) ?? 0) + smoothing) / (rightTotal + smoothing * vocabSize))
        : Math.log(((fallbackCounts.get(candidate) ?? 0) + smoothing) / (fallbackTotal + smoothing * vocabSize));
    return leftScore + rightScore;
  });
}

function evaluateMasked(records) {
  const usable = exactCollapse(records.filter((record) => record.tokens.length > 0));
  const globalCounts = buildGroupCounts(usable);
  const vocab = [...globalCounts.tokenCounts.keys()].sort((a, b) => a.localeCompare(b));
  const models = {
    frequency: { masked_tokens: 0, top1: 0, top5: 0, mrr_sum: 0 },
    position: { masked_tokens: 0, top1: 0, top5: 0, mrr_sum: 0 },
    length_position: { masked_tokens: 0, top1: 0, top5: 0, mrr_sum: 0 },
    bidirectional_bigram: { masked_tokens: 0, top1: 0, top5: 0, mrr_sum: 0 },
  };
  for (const record of usable) {
    const rowCounts = recordCounts(record);
    const fallbackCounts = subtractTokenCounts(globalCounts.tokenCounts, rowCounts.tokenCounts);
    const len = record.tokens.length;
    for (let i = 0; i < len; i++) {
      const token = record.tokens[i];
      const left = i === 0 ? '<s>' : record.tokens[i - 1];
      const right = i === len - 1 ? '</s>' : record.tokens[i + 1];
      const positionCounts = subtractCountMapForKey(globalCounts.positionCounts, rowCounts.positionCounts, String(i));
      const lengthPositionCounts = subtractCountMapForKey(
        globalCounts.lengthPositionCounts,
        rowCounts.lengthPositionCounts,
        `${len}\t${i}`,
      );
      const leftCounts = subtractCountMapForKey(globalCounts.leftCounts, rowCounts.leftCounts, left);
      const rightCounts = subtractCountMapForKey(globalCounts.rightCounts, rowCounts.rightCounts, right);
      const ranks = {
        frequency: rankCountMap(fallbackCounts, token, vocab),
        position: rankCountMap(positionCounts.size ? positionCounts : fallbackCounts, token, vocab),
        length_position: rankCountMap(lengthPositionCounts.size ? lengthPositionCounts : fallbackCounts, token, vocab),
        bidirectional_bigram: rankBidirectional(leftCounts, rightCounts, token, vocab, fallbackCounts),
      };
      for (const [model, rank] of Object.entries(ranks)) {
        models[model].masked_tokens++;
        if (rank.top1) models[model].top1++;
        if (rank.top5) models[model].top5++;
        models[model].mrr_sum += 1 / rank.rank;
      }
    }
  }
  return Object.entries(models).map(([model, row]) => ({
    model,
    masked_tokens: row.masked_tokens,
    top1: row.top1,
    top1_accuracy: row.masked_tokens ? formatNumber(row.top1 / row.masked_tokens) : null,
    top5: row.top5,
    top5_accuracy: row.masked_tokens ? formatNumber(row.top5 / row.masked_tokens) : null,
    mrr: row.masked_tokens ? formatNumber(row.mrr_sum / row.masked_tokens) : null,
  }));
}

function positionEntropy(records, tokenization, scope) {
  const rows = [];
  const byAbsolute = new Map();
  const byLengthPosition = new Map();
  for (const record of records) {
    for (let pos = 0; pos < record.tokens.length; pos++) {
      const token = record.tokens[pos];
      if (!byAbsolute.has(pos)) byAbsolute.set(pos, new Map());
      bump(byAbsolute.get(pos), token);
      const lp = `${record.tokens.length}\t${pos}`;
      if (!byLengthPosition.has(lp)) byLengthPosition.set(lp, new Map());
      bump(byLengthPosition.get(lp), token);
    }
  }
  for (const [pos, counts] of byAbsolute.entries()) {
    const total = mapTotal(counts);
    rows.push({
      tokenization,
      scope,
      position_type: 'absolute',
      length: '',
      position: pos,
      observations: total,
      unique_tokens: counts.size,
      entropy_bits: formatNumber(entropyBits(counts)),
      normalized_entropy: counts.size > 1 ? formatNumber(entropyBits(counts) / Math.log2(counts.size)) : 0,
    });
  }
  for (const [key, counts] of byLengthPosition.entries()) {
    const [length, pos] = key.split('\t');
    const total = mapTotal(counts);
    rows.push({
      tokenization,
      scope,
      position_type: 'length_position',
      length,
      position: pos,
      observations: total,
      unique_tokens: counts.size,
      entropy_bits: formatNumber(entropyBits(counts)),
      normalized_entropy: counts.size > 1 ? formatNumber(entropyBits(counts) / Math.log2(counts.size)) : 0,
    });
  }
  return rows.sort((a, b) =>
    a.tokenization.localeCompare(b.tokenization) ||
    a.scope.localeCompare(b.scope) ||
    a.position_type.localeCompare(b.position_type) ||
    Number(a.length || 0) - Number(b.length || 0) ||
    Number(a.position) - Number(b.position),
  );
}

function lengthDistribution(records, tokenization, scope) {
  const counts = new Map();
  for (const record of records) bump(counts, record.tokens.length);
  return [...counts.entries()]
    .sort((a, b) => a[0] - b[0])
    .map(([length, rows]) => ({ tokenization, scope, length, rows }));
}

function summarizeMetric(control, metric, values, observed) {
  return {
    control,
    metric,
    iterations: values.length,
    observed_value: observed,
    null_mean: formatNumber(mean(values)),
    null_sd: formatNumber(Math.sqrt(mean(values.map((value) => (value - mean(values)) ** 2)))),
    null_min: formatNumber(Math.min(...values)),
    null_median: formatNumber(median(values)),
    null_max: formatNumber(Math.max(...values)),
    observed_minus_null_mean: formatNumber(observed - mean(values)),
    null_ge_observed_share: formatNumber(values.filter((value) => value >= observed).length / values.length),
  };
}

function evaluateObserved(tokenization, scope, records) {
  const sequence = evaluateSequence(records);
  const masked = evaluateMasked(records);
  return {
    tokenization,
    scope,
    sequence,
    masked,
  };
}

function evaluateControlDataset(tokenization, scope, control, iteration, records) {
  const sequence = evaluateSequence(records);
  const masked = evaluateMasked(records);
  const maskedByModel = Object.fromEntries(masked.map((row) => [row.model, row]));
  return {
    tokenization,
    scope,
    control,
    iteration,
    ...sequence,
    frequency_top1_accuracy: maskedByModel.frequency.top1_accuracy,
    position_top1_accuracy: maskedByModel.position.top1_accuracy,
    length_position_top1_accuracy: maskedByModel.length_position.top1_accuracy,
    bidirectional_top1_accuracy: maskedByModel.bidirectional_bigram.top1_accuracy,
    bidirectional_top5_accuracy: maskedByModel.bidirectional_bigram.top5_accuracy,
  };
}

function formatLocalIso(date) {
  const offsetMinutes = -date.getTimezoneOffset();
  const sign = offsetMinutes >= 0 ? '+' : '-';
  const absMinutes = Math.abs(offsetMinutes);
  const pad = (value) => String(value).padStart(2, '0');
  const offset = `${sign}${pad(Math.floor(absMinutes / 60))}:${pad(absMinutes % 60)}`;
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(
    date.getHours(),
  )}:${pad(date.getMinutes())}:${pad(date.getSeconds())}${offset}`;
}

const sourceText = fs.readFileSync(sourcePath, 'utf8');
const physicalLines = sourceText.split(/\r?\n/);
const sequenceLines = physicalLines.slice(0, 2565);
const gappedTestLines = physicalLines.slice(2569, 3082).filter((line) => line.trim().length > 0);

const expectedMd5 = '0c9b9190b86840c82cafdbf4f4b8c827';
const actualMd5 = md5(sourcePath);
if (actualMd5 !== expectedMd5) {
  throw new Error(`MD5 mismatch for Samples.txt: expected ${expectedMd5}, got ${actualMd5}`);
}

const lipiRows = parseCsv(fs.readFileSync(lipiScopePath, 'utf8'));
const lipiHeader = lipiRows[0];
const lipiColumn = Object.fromEntries(lipiHeader.map((name, index) => [name, index]));
const ivcLengths = lipiRows
  .slice(1)
  .filter((row) => row[lipiColumn.readiness_bucket] === 'lipi_numeric_clean_candidate')
  .map((row) => parseLipiNumericTokens(row[lipiColumn.text]).length)
  .filter((length) => length > 0);
const ivcP95Length = Math.ceil(quantile(ivcLengths, 0.95));

const allRows = sequenceLines.map((line, index) => {
  let datasetSlice = 'duplicate_excluded_default';
  if (index < 513) datasetSlice = 'real_series_d_default_clean';
  else if (index < 1238) datasetSlice = 'augmented_excluded_default';
  return {
    row_index_1based: index + 1,
    dataset_slice: datasetSlice,
    raw_sequence: line.trim(),
    word_tokens: parseWordTokens(line),
    sign_tokens: parseSignTokens(line),
  };
});

const cleanRows = allRows.filter((row) => row.dataset_slice === 'real_series_d_default_clean');
const rowInventory = allRows.map((row) => ({
  row_index_1based: row.row_index_1based,
  dataset_slice: row.dataset_slice,
  word_token_count: row.word_tokens.length,
  sign_token_count: row.sign_tokens.length,
  ivc_p95_length_eligible: row.sign_tokens.length <= ivcP95Length,
  raw_sequence: row.raw_sequence,
}));

const tokenizations = [
  ['sign_tokens', (row) => row.sign_tokens],
  ['word_tokens', (row) => row.word_tokens],
];
const scopes = [
  ['real_series_d_513_all_lengths', cleanRows],
  ['real_series_d_513_ivc_p95_length_cap', cleanRows.filter((row) => row.sign_tokens.length <= ivcP95Length)],
];

const observedOutputs = [];
const lengthRows = [];
const entropyRows = [];
const controlRows = [];
const controlSummaryRows = [];
const controls = [
  ['length_frequency_shuffle', generateLengthFrequencyShuffle],
  ['edge_frame_shuffle', generateEdgeFrameShuffle],
  ['position_slot_shuffle', generatePositionSlotShuffle],
];

for (const [tokenization, tokenGetter] of tokenizations) {
  for (const [scope, rowSet] of scopes) {
    const records = rowSet.map((row) => ({
      id: `linear_b_${row.row_index_1based}`,
      source_row_index: row.row_index_1based,
      tokens: tokenGetter(row),
    }));
    observedOutputs.push(evaluateObserved(tokenization, scope, records));
    lengthRows.push(...lengthDistribution(records, tokenization, scope));
    entropyRows.push(...positionEntropy(records, tokenization, scope));
    const observed = controlRows.length;
    const observedControlRow = evaluateControlDataset(tokenization, scope, 'observed', 'observed', records);
    controlRows.push(observedControlRow);
    for (const [control, generator] of controls) {
      for (let iteration = 1; iteration <= iterations; iteration++) {
        const rng = mulberry32(seedBase + iteration * 1009 + control.length * 65537 + tokenization.length * 17 + scope.length);
        const generated = generator(records, rng, iteration);
        controlRows.push(evaluateControlDataset(tokenization, scope, control, iteration, generated));
      }
    }
    const observedRow = controlRows[observed];
    const metricNames = [
      'unique_tokens',
      'exact_sequence_groups',
      'exact_duplicate_groups',
      'exact_duplicate_rows',
      'top_sequence_count',
      'collapsed_rows',
      'stored_higher_share',
      'frequency_top1_accuracy',
      'position_top1_accuracy',
      'length_position_top1_accuracy',
      'bidirectional_top1_accuracy',
      'bidirectional_top5_accuracy',
    ];
    for (const [control] of controls) {
      const rowsForControl = controlRows.filter(
        (row) => row.tokenization === tokenization && row.scope === scope && row.control === control,
      );
      for (const metric of metricNames) {
        controlSummaryRows.push({
          tokenization,
          scope,
          ...summarizeMetric(
            control,
            metric,
            rowsForControl.map((row) => row[metric]),
            observedRow[metric],
          ),
        });
      }
    }
  }
}

fs.writeFileSync(
  rowInventoryPath,
  toCsv([
    ['row_index_1based', 'dataset_slice', 'word_token_count', 'sign_token_count', 'ivc_p95_length_eligible', 'raw_sequence'],
    ...rowInventory.map((row) => [
      row.row_index_1based,
      row.dataset_slice,
      row.word_token_count,
      row.sign_token_count,
      row.ivc_p95_length_eligible,
      row.raw_sequence,
    ]),
  ]),
  'utf8',
);

fs.writeFileSync(
  lengthDistributionPath,
  toCsv([
    ['tokenization', 'scope', 'length', 'rows'],
    ...lengthRows.map((row) => [row.tokenization, row.scope, row.length, row.rows]),
  ]),
  'utf8',
);

fs.writeFileSync(
  sequenceSummaryPath,
  toCsv([
    [
      'tokenization',
      'scope',
      'rows',
      'tokens',
      'unique_tokens',
      'exact_sequence_groups',
      'exact_duplicate_groups',
      'exact_duplicate_rows',
      'exact_duplicate_row_share',
      'top_sequence_count',
      'collapsed_rows',
      'collapsed_tokens',
      'collapsed_unique_tokens',
      'rows_length_gt_1',
      'stored_higher_than_reversed',
      'reversed_higher_than_stored',
      'ties',
      'stored_higher_share',
      'mean_stored_minus_reversed',
      'median_stored_minus_reversed',
    ],
    ...observedOutputs.map(({ tokenization, scope, sequence }) => [
      tokenization,
      scope,
      sequence.rows,
      sequence.tokens,
      sequence.unique_tokens,
      sequence.exact_sequence_groups,
      sequence.exact_duplicate_groups,
      sequence.exact_duplicate_rows,
      sequence.exact_duplicate_row_share,
      sequence.top_sequence_count,
      sequence.collapsed_rows,
      sequence.collapsed_tokens,
      sequence.collapsed_unique_tokens,
      sequence.rows_length_gt_1,
      sequence.stored_higher_than_reversed,
      sequence.reversed_higher_than_stored,
      sequence.ties,
      sequence.stored_higher_share,
      sequence.mean_stored_minus_reversed,
      sequence.median_stored_minus_reversed,
    ]),
  ]),
  'utf8',
);

fs.writeFileSync(
  maskedSummaryPath,
  toCsv([
    ['tokenization', 'scope', 'model', 'masked_tokens', 'top1', 'top1_accuracy', 'top5', 'top5_accuracy', 'mrr'],
    ...observedOutputs.flatMap(({ tokenization, scope, masked }) =>
      masked.map((row) => [
        tokenization,
        scope,
        row.model,
        row.masked_tokens,
        row.top1,
        row.top1_accuracy,
        row.top5,
        row.top5_accuracy,
        row.mrr,
      ]),
    ),
  ]),
  'utf8',
);

fs.writeFileSync(
  positionEntropyPath,
  toCsv([
    ['tokenization', 'scope', 'position_type', 'length', 'position', 'observations', 'unique_tokens', 'entropy_bits', 'normalized_entropy'],
    ...entropyRows.map((row) => [
      row.tokenization,
      row.scope,
      row.position_type,
      row.length,
      row.position,
      row.observations,
      row.unique_tokens,
      row.entropy_bits,
      row.normalized_entropy,
    ]),
  ]),
  'utf8',
);

fs.writeFileSync(
  controlIterationsPath,
  toCsv([
    [
      'tokenization',
      'scope',
      'control',
      'iteration',
      'rows',
      'tokens',
      'unique_tokens',
      'exact_sequence_groups',
      'exact_duplicate_groups',
      'exact_duplicate_rows',
      'top_sequence_count',
      'collapsed_rows',
      'stored_higher_share',
      'frequency_top1_accuracy',
      'position_top1_accuracy',
      'length_position_top1_accuracy',
      'bidirectional_top1_accuracy',
      'bidirectional_top5_accuracy',
    ],
    ...controlRows.map((row) => [
      row.tokenization,
      row.scope,
      row.control,
      row.iteration,
      row.rows,
      row.tokens,
      row.unique_tokens,
      row.exact_sequence_groups,
      row.exact_duplicate_groups,
      row.exact_duplicate_rows,
      row.top_sequence_count,
      row.collapsed_rows,
      row.stored_higher_share,
      row.frequency_top1_accuracy,
      row.position_top1_accuracy,
      row.length_position_top1_accuracy,
      row.bidirectional_top1_accuracy,
      row.bidirectional_top5_accuracy,
    ]),
  ]),
  'utf8',
);

fs.writeFileSync(
  controlSummaryPath,
  toCsv([
    [
      'tokenization',
      'scope',
      'control',
      'metric',
      'iterations',
      'observed_value',
      'null_mean',
      'null_sd',
      'null_min',
      'null_median',
      'null_max',
      'observed_minus_null_mean',
      'null_ge_observed_share',
    ],
    ...controlSummaryRows.map((row) => [
      row.tokenization,
      row.scope,
      row.control,
      row.metric,
      row.iterations,
      row.observed_value,
      row.null_mean,
      row.null_sd,
      row.null_min,
      row.null_median,
      row.null_max,
      row.observed_minus_null_mean,
      row.null_ge_observed_share,
    ]),
  ]),
  'utf8',
);

const fileStats = fs.statSync(sourcePath);
const manifest = {
  generated_at_local: formatLocalIso(new Date()),
  source_url: 'https://zenodo.org/records/7404653/files/Samples.txt?download=1',
  zenodo_record: 'https://zenodo.org/records/7404653',
  doi: '10.5281/zenodo.7404653',
  version: '1.0',
  license: 'CC-BY 4.0',
  local_file: 'data/open_prototype/known_scripts/linear_b_series_d/Samples.txt',
  bytes: fileStats.size,
  md5: actualMd5,
  expected_md5: expectedMd5,
  md5_verified: actualMd5 === expectedMd5,
  physical_lines: physicalLines.length,
  nonempty_lines: physicalLines.filter((line) => line.trim().length > 0).length,
  published_sequence_rows: sequenceLines.length,
  gapped_test_rows_detected_after_sequence_block: gappedTestLines.length,
  row_policy: {
    real_series_d_default_clean: 'rows 1-513',
    augmented_excluded_default: 'rows 514-1238',
    duplicate_excluded_default: 'rows 1239-2565',
    gapped_test_detected_not_used: '513 rows after the blank/header section',
  },
};
fs.writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');

const primary = observedOutputs.find(
  (row) => row.tokenization === 'sign_tokens' && row.scope === 'real_series_d_513_all_lengths',
);
const primaryIvcLike = observedOutputs.find(
  (row) => row.tokenization === 'sign_tokens' && row.scope === 'real_series_d_513_ivc_p95_length_cap',
);
const primaryMaskedByModel = Object.fromEntries(primary.masked.map((row) => [row.model, row]));
const primaryIvcMaskedByModel = Object.fromEntries(primaryIvcLike.masked.map((row) => [row.model, row]));

const summary = {
  generated_at_local: formatLocalIso(new Date()),
  experiment: 'E5.3a Linear B Series D Scarcity Baseline',
  source_manifest: 'data/open_prototype/reports/linear_b_series_d_source_manifest.json',
  clean_default: {
    tokenization: 'sign_tokens',
    scope: 'real_series_d_513_all_lengths',
    rows: primary.sequence.rows,
    tokens: primary.sequence.tokens,
    unique_tokens: primary.sequence.unique_tokens,
    exact_sequence_groups: primary.sequence.exact_sequence_groups,
    exact_duplicate_rows: primary.sequence.exact_duplicate_rows,
    stored_higher_share: primary.sequence.stored_higher_share,
    frequency_top1_accuracy: primaryMaskedByModel.frequency.top1_accuracy,
    position_top1_accuracy: primaryMaskedByModel.position.top1_accuracy,
    length_position_top1_accuracy: primaryMaskedByModel.length_position.top1_accuracy,
    bidirectional_top1_accuracy: primaryMaskedByModel.bidirectional_bigram.top1_accuracy,
    bidirectional_top5_accuracy: primaryMaskedByModel.bidirectional_bigram.top5_accuracy,
  },
  ivc_like_length_cap: {
    source: 'current lipi_numeric_clean_candidate p95 length',
    cap_sign_tokens: ivcP95Length,
    ivc_numeric_clean_rows: ivcLengths.length,
    ivc_length_mean: formatNumber(mean(ivcLengths)),
    ivc_length_median: formatNumber(median(ivcLengths)),
    ivc_length_p95: formatNumber(quantile(ivcLengths, 0.95)),
    tokenization: 'sign_tokens',
    scope: 'real_series_d_513_ivc_p95_length_cap',
    rows: primaryIvcLike.sequence.rows,
    tokens: primaryIvcLike.sequence.tokens,
    unique_tokens: primaryIvcLike.sequence.unique_tokens,
    stored_higher_share: primaryIvcLike.sequence.stored_higher_share,
    frequency_top1_accuracy: primaryIvcMaskedByModel.frequency.top1_accuracy,
    position_top1_accuracy: primaryIvcMaskedByModel.position.top1_accuracy,
    length_position_top1_accuracy: primaryIvcMaskedByModel.length_position.top1_accuracy,
    bidirectional_top1_accuracy: primaryIvcMaskedByModel.bidirectional_bigram.top1_accuracy,
    bidirectional_top5_accuracy: primaryIvcMaskedByModel.bidirectional_bigram.top5_accuracy,
  },
  controls: {
    iterations_per_control: iterations,
    names: controls.map(([name]) => name),
    note: 'Controls run for both sign_tokens and word_tokens, and for all-length plus IVC-p95-length scopes. They are structural-only nulls, not translation tests.',
  },
  tokenization_caveat:
    'The primary sign_tokens view splits hyphenated transliteration tokens into opaque sign labels while preserving logograms and composite labels such as OVIS:f as single labels. This is a scarcity comparator tokenization, not a claim about Linear B philology.',
  interpretation_boundary:
    'Known-script comparator only. Results estimate what structural methods recover when known readings are hidden. They do not validate any IVC sign, side relation, semantic field, language identity, phonetic value, or translation.',
  artifact_files: [
    'data/open_prototype/known_scripts/linear_b_series_d/Samples.txt',
    'data/open_prototype/reports/linear_b_series_d_source_manifest.json',
    'data/open_prototype/reports/linear_b_series_d_row_inventory.csv',
    'data/open_prototype/reports/linear_b_series_d_length_distribution.csv',
    'data/open_prototype/reports/linear_b_series_d_sequence_summary.csv',
    'data/open_prototype/reports/linear_b_series_d_masked_summary.csv',
    'data/open_prototype/reports/linear_b_series_d_position_entropy.csv',
    'data/open_prototype/reports/linear_b_series_d_control_iterations.csv',
    'data/open_prototype/reports/linear_b_series_d_control_summary.csv',
    'data/open_prototype/reports/linear_b_series_d_scarcity_summary.json',
  ],
};
fs.writeFileSync(summaryJsonPath, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
