import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const sourceDir = path.join(base, 'data', 'open_prototype', 'known_scripts', 'sumtablets');

const datasetId = 'colesimmons/SumTablets';
const encodedDatasetId = encodeURIComponent(datasetId);
const hfDatasetApi = `https://huggingface.co/api/datasets/${datasetId}`;
const datasetServer = 'https://datasets-server.huggingface.co';
const split = 'train';
const config = 'default';

const pageCount = Number(process.argv[2] ?? 20);
const rowsPerPage = Number(process.argv[3] ?? 100);
const selectedLineCap = Number(process.argv[4] ?? 1798);
const nullIterations = Number(process.argv[5] ?? 40);
const nullMaskedSampleLimit = Number(process.argv[6] ?? 1500);
const seedBase = Number(process.argv[7] ?? 20260529);
const smoothing = 0.5;
const epsilon = 1e-12;

const outManifest = path.join(sourceDir, 'sumtablets_source_manifest.json');
const outSampleRows = path.join(sourceDir, 'sumtablets_sample_rows.jsonl');
const outLineSequences = path.join(sourceDir, 'sumtablets_line_sequences.csv');
const outSummaryJson = path.join(reportsDir, 'effective_unicity_sumtablets_comparator_summary.json');
const outComparatorCsv = path.join(reportsDir, 'effective_unicity_sumtablets_comparator.csv');
const outNullIterations = path.join(reportsDir, 'effective_unicity_sumtablets_null_iterations.csv');
const outNullSummary = path.join(reportsDir, 'effective_unicity_sumtablets_null_summary.csv');

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

function loadCsv(filePath) {
  const rows = parseCsv(fs.readFileSync(filePath, 'utf8'));
  const header = rows[0] ?? [];
  return rows.slice(1).map((row) => Object.fromEntries(header.map((name, index) => [name, row[index] ?? ''])));
}

function round(value, places = 6) {
  if (value === null || value === undefined || !Number.isFinite(Number(value))) return null;
  return Number(Number(value).toFixed(places));
}

function formatLocalIso(date) {
  const offsetMinutes = -date.getTimezoneOffset();
  const sign = offsetMinutes >= 0 ? '+' : '-';
  const absMinutes = Math.abs(offsetMinutes);
  const pad = (value) => String(value).padStart(2, '0');
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(
    date.getHours(),
  )}:${pad(date.getMinutes())}:${pad(date.getSeconds())}${sign}${pad(Math.floor(absMinutes / 60))}:${pad(
    absMinutes % 60,
  )}`;
}

function log2Factorial(n) {
  let total = 0;
  for (let i = 2; i <= n; i++) total += Math.log2(i);
  return total;
}

function percentile(sortedValues, p) {
  if (!sortedValues.length) return null;
  const idx = (sortedValues.length - 1) * p;
  const lo = Math.floor(idx);
  const hi = Math.ceil(idx);
  if (lo === hi) return sortedValues[lo];
  return sortedValues[lo] + (sortedValues[hi] - sortedValues[lo]) * (idx - lo);
}

function mulberry32(seed) {
  let value = seed >>> 0;
  return () => {
    value += 0x6d2b79f5;
    let t = value;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffle(items, rng) {
  const out = items.slice();
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function bump(map, key, by = 1) {
  map.set(key, (map.get(key) ?? 0) + by);
}

function addNested(map, key, token, by = 1) {
  if (!map.has(key)) map.set(key, new Map());
  bump(map.get(key), token, by);
}

function mapTotal(map) {
  let total = 0;
  for (const value of map.values()) total += value;
  return total;
}

function nestedTotals(nested) {
  return new Map([...nested.entries()].map(([key, inner]) => [key, mapTotal(inner)]));
}

function nestedCount(nested, key, token) {
  return nested.get(key)?.get(token) ?? 0;
}

function stableHash(text) {
  let hash = 0x811c9dc5;
  for (const char of text) {
    hash ^= char.codePointAt(0);
    hash = Math.imul(hash, 0x01000193) >>> 0;
  }
  return hash;
}

async function fetchJson(url) {
  const response = await fetch(url, { headers: { accept: 'application/json' } });
  if (!response.ok) throw new Error(`Fetch failed ${response.status} ${response.statusText}: ${url}`);
  return response.json();
}

function splitRows(totalRows, pageN, pageSize) {
  if (pageN <= 1) return [0];
  const maxOffset = Math.max(0, totalRows - pageSize);
  return [...new Set(Array.from({ length: pageN }, (_, i) => Math.floor((i * maxOffset) / (pageN - 1))))];
}

function isCuneiformGlyph(char) {
  const codePoint = char.codePointAt(0);
  return codePoint >= 0x12000 && codePoint <= 0x1247f;
}

function tokenizeGlyphLine(line) {
  return [...String(line ?? '')].filter(isCuneiformGlyph);
}

function extractLineRecords(sampleRows) {
  const rawLines = [];
  const exclusionCounts = new Map();
  for (const row of sampleRows) {
    const lines = String(row.glyphs ?? '').split(/\r?\n/);
    for (let lineIndex = 0; lineIndex < lines.length; lineIndex++) {
      const line = lines[lineIndex].trim();
      if (!line) {
        bump(exclusionCounts, 'blank_line');
        continue;
      }
      const tokens = tokenizeGlyphLine(line);
      if (!tokens.length) {
        bump(exclusionCounts, 'structural_or_no_cuneiform_line');
        continue;
      }
      if (tokens.length < 2) {
        bump(exclusionCounts, 'length_lt_2');
        continue;
      }
      if (tokens.length > 8) {
        bump(exclusionCounts, 'length_gt_8_ivc_cap');
        continue;
      }
      rawLines.push({
        source_tablet_id: row.id,
        source_row_index: row.source_row_index,
        source_page_offset: row.source_page_offset,
        split: row.split,
        period: row.period,
        genre: row.genre,
        line_index: lineIndex,
        line_text: line,
        tokens,
      });
    }
  }

  const collapsed = new Map();
  for (const line of rawLines) {
    const key = line.tokens.join(' ');
    if (!collapsed.has(key)) {
      collapsed.set(key, {
        line_id: `sum_${String(collapsed.size + 1).padStart(5, '0')}`,
        tokens: line.tokens,
        duplicate_weight: 1,
        first_source_tablet_id: line.source_tablet_id,
        first_period: line.period,
        first_genre: line.genre,
        source_tablet_ids: [line.source_tablet_id],
        source_row_indices: [line.source_row_index],
        source_line_indices: [line.line_index],
        periods: new Set([line.period]),
        genres: new Set([line.genre]),
      });
    } else {
      const existing = collapsed.get(key);
      existing.duplicate_weight++;
      existing.source_tablet_ids.push(line.source_tablet_id);
      existing.source_row_indices.push(line.source_row_index);
      existing.source_line_indices.push(line.line_index);
      existing.periods.add(line.period);
      existing.genres.add(line.genre);
    }
  }

  const uniqueLines = [...collapsed.values()]
    .map((record) => ({
      ...record,
      periods: [...record.periods].sort(),
      genres: [...record.genres].sort(),
      hash: stableHash(record.tokens.join(' ')),
    }))
    .sort((a, b) => a.hash - b.hash || a.tokens.join(' ').localeCompare(b.tokens.join(' ')));

  const selected = uniqueLines.slice(0, selectedLineCap).map((record, index) => ({
    ...record,
    line_id: `sum_${String(index + 1).padStart(5, '0')}`,
  }));

  return {
    rawLines,
    uniqueLines,
    selected,
    exclusionCounts: Object.fromEntries([...exclusionCounts.entries()].sort((a, b) => a[0].localeCompare(b[0]))),
  };
}

function recordCounts(record) {
  const tokenCounts = new Map();
  const lengthPositionCounts = new Map();
  const leftCounts = new Map();
  const rightCounts = new Map();
  const len = record.tokens.length;
  for (let i = 0; i < len; i++) {
    const token = record.tokens[i];
    const left = i === 0 ? '<s>' : record.tokens[i - 1];
    const right = i === len - 1 ? '</s>' : record.tokens[i + 1];
    bump(tokenCounts, token);
    addNested(lengthPositionCounts, `${len}:${i}`, token);
    addNested(leftCounts, left, token);
    addNested(rightCounts, right, token);
  }
  return { tokenCounts, lengthPositionCounts, leftCounts, rightCounts };
}

function buildCounts(records) {
  const counts = {
    tokenCounts: new Map(),
    lengthPositionCounts: new Map(),
    leftCounts: new Map(),
    rightCounts: new Map(),
  };
  for (const record of records) {
    const rowCounts = recordCounts(record);
    for (const [token, value] of rowCounts.tokenCounts.entries()) bump(counts.tokenCounts, token, value);
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

function chooseMaskedPositions(records, sampleLimit, rng) {
  const positions = [];
  for (let rowIndex = 0; rowIndex < records.length; rowIndex++) {
    for (let i = 0; i < records[rowIndex].tokens.length; i++) {
      positions.push([rowIndex, i]);
    }
  }
  if (!sampleLimit || positions.length <= sampleLimit) return positions;
  return shuffle(positions, rng).slice(0, sampleLimit);
}

function softmaxStats(scored, trueToken) {
  const maxScore = Math.max(...scored.map(([, score]) => score));
  const weights = scored.map(([token, score]) => [token, Math.exp(score - maxScore)]);
  const total = weights.reduce((sum, [, weight]) => sum + weight, 0);
  const probs = weights.map(([token, weight]) => [token, weight / total]);
  probs.sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  const rank = probs.findIndex(([token]) => token === trueToken) + 1;
  const trueProb = probs.find(([token]) => token === trueToken)?.[1] ?? 0;
  const entropyBits = -probs.reduce((sum, [, prob]) => (prob > 0 ? sum + prob * Math.log2(prob) : sum), 0);
  let cumulative = 0;
  let mass90 = 0;
  for (const [, prob] of probs) {
    mass90++;
    cumulative += prob;
    if (cumulative >= 0.9 - epsilon) break;
  }
  return {
    rank,
    trueProb,
    top1: rank === 1,
    top5: rank > 0 && rank <= 5,
    entropyBits,
    effectiveCandidates: 2 ** entropyBits,
    mass90,
  };
}

function scoreMasked(records, options = {}) {
  const rng = options.rng ?? mulberry32(seedBase);
  const globalCounts = buildCounts(records);
  const globalTotals = {
    token: mapTotal(globalCounts.tokenCounts),
    lengthPosition: nestedTotals(globalCounts.lengthPositionCounts),
    left: nestedTotals(globalCounts.leftCounts),
    right: nestedTotals(globalCounts.rightCounts),
  };
  const vocab = [...globalCounts.tokenCounts.keys()].sort((a, b) => a.localeCompare(b));
  const vocabSize = Math.max(1, vocab.length);
  const positions = chooseMaskedPositions(records, options.sampleLimit, rng);
  const rowCountsCache = new Map();

  function getRowCounts(rowIndex) {
    if (!rowCountsCache.has(rowIndex)) {
      const counts = recordCounts(records[rowIndex]);
      rowCountsCache.set(rowIndex, {
        ...counts,
        totals: {
          token: mapTotal(counts.tokenCounts),
          lengthPosition: nestedTotals(counts.lengthPositionCounts),
          left: nestedTotals(counts.leftCounts),
          right: nestedTotals(counts.rightCounts),
        },
      });
    }
    return rowCountsCache.get(rowIndex);
  }

  const totals = {
    masked_tokens: 0,
    top1: 0,
    top5: 0,
    rank_sum: 0,
    reciprocal_rank_sum: 0,
    true_prob_sum: 0,
    entropy_bits_sum: 0,
    effective_candidate_sum: 0,
    mass90_sum: 0,
  };

  for (const [rowIndex, i] of positions) {
    const record = records[rowIndex];
    const rowCounts = getRowCounts(rowIndex);
    const trainTotal = Math.max(0, globalTotals.token - rowCounts.totals.token);
    const len = record.tokens.length;
    const token = record.tokens[i];
    const left = i === 0 ? '<s>' : record.tokens[i - 1];
    const right = i === len - 1 ? '</s>' : record.tokens[i + 1];
    const lengthPositionKey = `${len}:${i}`;
    const lengthPositionTotal = Math.max(
      0,
      (globalTotals.lengthPosition.get(lengthPositionKey) ?? 0) -
        (rowCounts.totals.lengthPosition.get(lengthPositionKey) ?? 0),
    );
    const leftTotal = Math.max(
      0,
      (globalTotals.left.get(left) ?? 0) - (rowCounts.totals.left.get(left) ?? 0),
    );
    const rightTotal = Math.max(
      0,
      (globalTotals.right.get(right) ?? 0) - (rowCounts.totals.right.get(right) ?? 0),
    );

    const scored = vocab.map((candidate) => {
      const unigramCount = Math.max(
        0,
        (globalCounts.tokenCounts.get(candidate) ?? 0) - (rowCounts.tokenCounts.get(candidate) ?? 0),
      );
      const lengthPositionCount = Math.max(
        0,
        nestedCount(globalCounts.lengthPositionCounts, lengthPositionKey, candidate) -
          nestedCount(rowCounts.lengthPositionCounts, lengthPositionKey, candidate),
      );
      const leftCount = Math.max(
        0,
        nestedCount(globalCounts.leftCounts, left, candidate) - nestedCount(rowCounts.leftCounts, left, candidate),
      );
      const rightCount = Math.max(
        0,
        nestedCount(globalCounts.rightCounts, right, candidate) -
          nestedCount(rowCounts.rightCounts, right, candidate),
      );
      const unigram = Math.log((unigramCount + smoothing) / (trainTotal + smoothing * vocabSize));
      const lengthPosition = Math.log(
        (lengthPositionCount + smoothing) / (lengthPositionTotal + smoothing * vocabSize),
      );
      const leftScore = Math.log((leftCount + smoothing) / (leftTotal + smoothing * vocabSize));
      const rightScore = Math.log((rightCount + smoothing) / (rightTotal + smoothing * vocabSize));
      return [candidate, 0.35 * unigram + lengthPosition + leftScore + rightScore];
    });

    const stats = softmaxStats(scored, token);
    totals.masked_tokens++;
    if (stats.top1) totals.top1++;
    if (stats.top5) totals.top5++;
    totals.rank_sum += stats.rank;
    totals.reciprocal_rank_sum += 1 / stats.rank;
    totals.true_prob_sum += stats.trueProb;
    totals.entropy_bits_sum += stats.entropyBits;
    totals.effective_candidate_sum += stats.effectiveCandidates;
    totals.mass90_sum += stats.mass90;
  }

  const n = Math.max(1, totals.masked_tokens);
  return {
    masked_tokens: totals.masked_tokens,
    masked_sampled: Boolean(options.sampleLimit && positions.length === options.sampleLimit),
    masked_top1_accuracy: totals.top1 / n,
    masked_top5_accuracy: totals.top5 / n,
    masked_mean_rank: totals.rank_sum / n,
    masked_mrr: totals.reciprocal_rank_sum / n,
    masked_mean_true_probability: totals.true_prob_sum / n,
    masked_mean_entropy_bits: totals.entropy_bits_sum / n,
    masked_mean_effective_candidates: totals.effective_candidate_sum / n,
    masked_mean_mass90_candidates: totals.mass90_sum / n,
  };
}

function analyzeRecords(records, options = {}) {
  const tokens = records.reduce((sum, record) => sum + record.tokens.length, 0);
  const vocab = [...new Set(records.flatMap((record) => record.tokens))].sort((a, b) => a.localeCompare(b));
  const masked = scoreMasked(records, options);
  return {
    rows: records.length,
    tokens,
    unique_signs_or_glyphs: vocab.length,
    label_symmetry_log2_bits: log2Factorial(vocab.length),
    ...masked,
  };
}

function cloneWithTokens(records, tokensByRecord) {
  return records.map((record, index) => ({ ...record, tokens: tokensByRecord[index] }));
}

function buildPositionPools(records) {
  const pools = new Map();
  for (const record of records) {
    const len = record.tokens.length;
    for (let i = 0; i < len; i++) {
      const key = `${len}:${i}`;
      if (!pools.has(key)) pools.set(key, []);
      pools.get(key).push(record.tokens[i]);
    }
  }
  return pools;
}

function controlRecords(records, control, rng) {
  const lengths = records.map((record) => record.tokens.length);
  if (control === 'global_token_shuffle') {
    const tokens = shuffle(records.flatMap((record) => record.tokens), rng);
    let cursor = 0;
    return cloneWithTokens(
      records,
      lengths.map((len) => {
        const next = tokens.slice(cursor, cursor + len);
        cursor += len;
        return next;
      }),
    );
  }

  if (control === 'row_internal_shuffle') {
    return cloneWithTokens(
      records,
      records.map((record) => shuffle(record.tokens, rng)),
    );
  }

  if (control === 'position_slot_shuffle') {
    const pools = new Map([...buildPositionPools(records).entries()].map(([key, pool]) => [key, shuffle(pool, rng)]));
    const cursors = new Map();
    return cloneWithTokens(
      records,
      records.map((record) => {
        const len = record.tokens.length;
        return record.tokens.map((token, i) => {
          const key = `${len}:${i}`;
          const pool = pools.get(key) ?? [token];
          const cursor = cursors.get(key) ?? 0;
          cursors.set(key, cursor + 1);
          return pool[cursor % pool.length];
        });
      }),
    );
  }

  if (control === 'edge_frame_shuffle') {
    const interiors = shuffle(
      records.flatMap((record) => record.tokens.slice(1, -1)),
      rng,
    );
    let cursor = 0;
    return cloneWithTokens(
      records,
      records.map((record) => {
        if (record.tokens.length <= 2) return record.tokens.slice();
        const interiorLength = record.tokens.length - 2;
        const next = [
          record.tokens[0],
          ...interiors.slice(cursor, cursor + interiorLength),
          record.tokens[record.tokens.length - 1],
        ];
        cursor += interiorLength;
        return next;
      }),
    );
  }

  if (control === 'period_genre_position_shuffle') {
    const pools = new Map();
    for (const record of records) {
      const len = record.tokens.length;
      const block = `${record.first_period ?? 'unknown'}|${record.first_genre ?? 'unknown'}`;
      for (let i = 0; i < len; i++) {
        const key = `${block}|${len}:${i}`;
        if (!pools.has(key)) pools.set(key, []);
        pools.get(key).push(record.tokens[i]);
      }
    }
    const shuffled = new Map([...pools.entries()].map(([key, pool]) => [key, shuffle(pool, rng)]));
    const cursors = new Map();
    return cloneWithTokens(
      records,
      records.map((record) => {
        const len = record.tokens.length;
        const block = `${record.first_period ?? 'unknown'}|${record.first_genre ?? 'unknown'}`;
        return record.tokens.map((token, i) => {
          const key = `${block}|${len}:${i}`;
          const pool = shuffled.get(key) ?? [token];
          const cursor = cursors.get(key) ?? 0;
          cursors.set(key, cursor + 1);
          return pool[cursor % pool.length];
        });
      }),
    );
  }

  throw new Error(`Unknown control: ${control}`);
}

function summarizeNulls(nullRows, observed) {
  const out = [];
  const controls = [...new Set(nullRows.map((row) => row.control))].sort();
  for (const control of controls) {
    const rows = nullRows.filter((row) => row.control === control);
    for (const metric of ['masked_top1_accuracy', 'masked_top5_accuracy', 'masked_mrr']) {
      const values = rows.map((row) => row[metric]).sort((a, b) => a - b);
      out.push({
        control,
        metric,
        iterations: values.length,
        observed: observed[metric],
        null_mean: values.reduce((sum, value) => sum + value, 0) / Math.max(1, values.length),
        null_p05: percentile(values, 0.05),
        null_median: percentile(values, 0.5),
        null_p95: percentile(values, 0.95),
        null_max: values.length ? values[values.length - 1] : null,
        null_ge_observed_share:
          values.filter((value) => value >= observed[metric] - epsilon).length / Math.max(1, values.length),
      });
    }
  }
  return out;
}

function readIndusAndLinearBRows() {
  const indusSummary = JSON.parse(
    fs.readFileSync(path.join(reportsDir, 'effective_unicity_degeneracy_summary.json'), 'utf8'),
  );
  const knownScriptSummary = JSON.parse(
    fs.readFileSync(path.join(reportsDir, 'effective_unicity_known_script_comparator_summary.json'), 'utf8'),
  );
  return {
    indus: {
      system: 'Indus_Lipi_strict_exact_sequence_collapsed',
      experiment: 'leave_one_row_out_masked_sign',
      rows: indusSummary.primary_full_coverage.rows,
      tokens_or_gaps: indusSummary.primary_full_coverage.tokens,
      unique_signs_or_tokens: indusSummary.primary_full_coverage.unique_signs,
      label_symmetry_log2_bits: indusSummary.primary_full_coverage.label_symmetry_log2_bits,
      top1: indusSummary.primary_full_coverage.masked_top1_accuracy,
      top5: indusSummary.primary_full_coverage.masked_top5_accuracy,
      mrr: indusSummary.primary_full_coverage.masked_mrr,
      max_control_fpr_or_null_ge_observed: 0,
      boundary: 'unread script; internal labels only; no source-normalized value anchor',
    },
    linearB: knownScriptSummary.rows.filter((row) => row.system.startsWith('Linear_B')),
  };
}

async function main() {
  fs.mkdirSync(sourceDir, { recursive: true });
  fs.mkdirSync(reportsDir, { recursive: true });

  const [datasetApi, validity, splits, size, parquet] = await Promise.all([
    fetchJson(hfDatasetApi),
    fetchJson(`${datasetServer}/is-valid?dataset=${encodedDatasetId}`),
    fetchJson(`${datasetServer}/splits?dataset=${encodedDatasetId}`),
    fetchJson(`${datasetServer}/size?dataset=${encodedDatasetId}`),
    fetchJson(`${datasetServer}/parquet?dataset=${encodedDatasetId}`),
  ]);

  const targetSplit =
    size.size?.splits?.find((item) => item.config === config && item.split === split) ??
    size.splits?.find((item) => item.config === config && item.split === split) ??
    size.size?.splits?.find((item) => item.split === split) ??
    size.splits?.find((item) => item.split === split);
  const trainRows = targetSplit?.num_rows ?? 82452;
  const offsets = splitRows(trainRows, pageCount, rowsPerPage);
  const fetchedPages = [];
  for (const offset of offsets) {
    const page = await fetchJson(
      `${datasetServer}/rows?dataset=${encodedDatasetId}&config=${encodeURIComponent(config)}&split=${encodeURIComponent(
        split,
      )}&offset=${offset}&length=${rowsPerPage}`,
    );
    fetchedPages.push({ offset, response: page });
  }

  const sampleRows = fetchedPages.flatMap(({ offset, response }) =>
    response.rows.map((item) => ({
      source_row_index: item.row_idx,
      source_page_offset: offset,
      split,
      id: item.row.id,
      period: item.row.period,
      genre: item.row.genre,
      glyphs: item.row.glyphs,
    })),
  );

  const extracted = extractLineRecords(sampleRows);
  const selected = extracted.selected;
  const observed = analyzeRecords(selected);
  const controls = [
    'global_token_shuffle',
    'row_internal_shuffle',
    'position_slot_shuffle',
    'edge_frame_shuffle',
    'period_genre_position_shuffle',
  ];

  const nullRows = [];
  for (const control of controls) {
    for (let iteration = 0; iteration < nullIterations; iteration++) {
      const rng = mulberry32(seedBase + 101 * controls.indexOf(control) + iteration);
      const controlled = controlRecords(selected, control, rng);
      const result = analyzeRecords(controlled, {
        sampleLimit: nullMaskedSampleLimit,
        rng: mulberry32(seedBase + 100000 + 101 * controls.indexOf(control) + iteration),
      });
      nullRows.push({
        control,
        iteration,
        rows: result.rows,
        tokens: result.tokens,
        unique_signs_or_glyphs: result.unique_signs_or_glyphs,
        masked_tokens: result.masked_tokens,
        masked_top1_accuracy: result.masked_top1_accuracy,
        masked_top5_accuracy: result.masked_top5_accuracy,
        masked_mrr: result.masked_mrr,
        masked_mean_effective_candidates: result.masked_mean_effective_candidates,
      });
    }
  }

  const nullSummary = summarizeNulls(nullRows, observed);
  const maxTop1NullGeObserved = Math.max(
    ...nullSummary
      .filter((row) => row.metric === 'masked_top1_accuracy')
      .map((row) => row.null_ge_observed_share),
  );

  const { indus, linearB } = readIndusAndLinearBRows();
  const sumTabletsRow = {
    system: 'SumTablets_Ur_III_cuneiform_admin_lines',
    experiment: 'glyph_only_ivc_length_capped_line_leave_one_out_masked_glyph',
    rows: observed.rows,
    tokens_or_gaps: observed.tokens,
    unique_signs_or_tokens: observed.unique_signs_or_glyphs,
    label_symmetry_log2_bits: observed.label_symmetry_log2_bits,
    top1: observed.masked_top1_accuracy,
    top5: observed.masked_top5_accuracy,
    mrr: observed.masked_mrr,
    median_rank: '',
    max_control_fpr_or_null_ge_observed: maxTop1NullGeObserved,
    boundary:
      'known readable administrative cuneiform; transliteration and glyph_names hidden; sampled line-level scarcity comparator, not a nonlinguistic null',
  };
  const comparatorRows = [indus, ...linearB, sumTabletsRow];

  const manifest = {
    date: '2026-05-29',
    generated_at_local: formatLocalIso(new Date()),
    generated_at_utc: new Date().toISOString(),
    purpose:
      'Pinned glyph-only known-script administrative comparator for the Vector 2 effective-unicity instrument. Transliteration and glyph_names are intentionally excluded from local cache and scoring.',
    dataset: {
      id: datasetId,
      huggingface_url: `https://huggingface.co/datasets/${datasetId}`,
      github_url: 'https://github.com/colesimmons/SumTablets',
      license: datasetApi.cardData?.license ?? datasetApi.tags?.find((tag) => String(tag).startsWith('license:')) ?? null,
      sha: datasetApi.sha,
      created_at: datasetApi.createdAt,
      last_modified: datasetApi.lastModified,
      tags: datasetApi.tags,
      viewer_validity: validity,
      split_metadata: splits,
      size_metadata: size,
      parquet_metadata: parquet,
    },
    sampling: {
      split,
      config,
      split_rows: trainRows,
      page_count_requested: pageCount,
      rows_per_page: rowsPerPage,
      offsets,
      fetched_rows: sampleRows.length,
      fields_retained: ['id', 'period', 'genre', 'glyphs'],
      fields_intentionally_excluded: ['transliteration', 'glyph_names'],
      line_filter: 'visible cuneiform glyph code points only; keep line lengths 2..8 inclusive',
      exact_sequence_collapse: true,
      selection_policy_after_collapse: `stable FNV-1a hash order, cap ${selectedLineCap}`,
    },
    extraction: {
      raw_line_records_after_length_filter: extracted.rawLines.length,
      exact_unique_line_sequences: extracted.uniqueLines.length,
      selected_line_sequences: selected.length,
      exclusion_counts: extracted.exclusionCounts,
    },
  };

  const summary = {
    date: '2026-05-29',
    generated_at_utc: new Date().toISOString(),
    purpose:
      'Add SumTablets as a pinned known-script administrative comparator for the Vector 2 effective-unicity instrument. This broadens calibration; it is not a nonlinguistic comparator and not Indus evidence.',
    source_files: {
      manifest: 'data/open_prototype/known_scripts/sumtablets/sumtablets_source_manifest.json',
      sampled_rows: 'data/open_prototype/known_scripts/sumtablets/sumtablets_sample_rows.jsonl',
      line_sequences: 'data/open_prototype/known_scripts/sumtablets/sumtablets_line_sequences.csv',
      indus_effective_unicity: 'data/open_prototype/reports/effective_unicity_degeneracy_summary.json',
      known_script_comparator_prior: 'data/open_prototype/reports/effective_unicity_known_script_comparator_summary.json',
    },
    source_manifest_summary: {
      dataset_id: datasetId,
      sha: datasetApi.sha,
      license: manifest.dataset.license,
      split,
      split_rows: trainRows,
      fetched_rows: sampleRows.length,
      raw_line_records_after_length_filter: extracted.rawLines.length,
      exact_unique_line_sequences: extracted.uniqueLines.length,
      selected_line_sequences: selected.length,
      transliteration_hidden: true,
      glyph_names_hidden: true,
    },
    sumtablets_observed: {
      rows: observed.rows,
      tokens: observed.tokens,
      unique_glyphs: observed.unique_signs_or_glyphs,
      label_symmetry_log2_bits: round(observed.label_symmetry_log2_bits),
      masked_top1: round(observed.masked_top1_accuracy),
      masked_top5: round(observed.masked_top5_accuracy),
      masked_mrr: round(observed.masked_mrr),
      masked_mean_effective_candidates: round(observed.masked_mean_effective_candidates),
    },
    sumtablets_forger_controls: {
      iterations_per_control: nullIterations,
      null_masked_sample_limit: nullMaskedSampleLimit,
      controls,
      masked_top1_max_null_ge_observed_share: round(maxTop1NullGeObserved),
      rows: nullSummary.map((row) => ({
        ...row,
        observed: round(row.observed),
        null_mean: round(row.null_mean),
        null_p05: round(row.null_p05),
        null_median: round(row.null_median),
        null_p95: round(row.null_p95),
        null_max: round(row.null_max),
        null_ge_observed_share: round(row.null_ge_observed_share),
      })),
    },
    primary_comparison: {
      indus_masked_top1: round(indus.top1),
      indus_masked_top5: round(indus.top5),
      indus_unique_signs: indus.unique_signs_or_tokens,
      linear_b_clean_ivc_cap_bidirectional_top1: linearB.find(
        (row) => row.experiment === 'clean_masked_bidirectional_bigram',
      )?.top1,
      linear_b_gapped_sequence_loo_top1: linearB.find(
        (row) => row.experiment === 'source_provided_gapped_sequence_leave_one_out',
      )?.top1,
      sumtablets_glyph_only_top1: round(observed.masked_top1_accuracy),
      sumtablets_glyph_only_top5: round(observed.masked_top5_accuracy),
      sumtablets_unique_glyphs: observed.unique_signs_or_glyphs,
      sumtablets_top1_max_control_null_ge_observed_share: round(maxTop1NullGeObserved),
    },
    interpretation: {
      calibration:
        'SumTablets supplies a known readable administrative-script comparator at Indus-like line lengths with transliteration hidden. Its glyph-only masked top-1/top-5 can be compared to Indus and Linear B as a scarcity/predictability calibration.',
      boundary:
        'Because SumTablets is a known writing system, it cannot serve as the requested real-world nonlinguistic comparator. It also does not identify any Indus sign, value, language family, or semantic field.',
      acceptance_status:
        'The Vector 2 candidate remains unaccepted. This comparator narrows one skeptic objection from single known-script coverage to broader known-script/admin coverage, but source-normalization and real-world nonlinguistic comparators are still open.',
    },
    rows: comparatorRows.map((row) => ({
      ...row,
      label_symmetry_log2_bits: round(row.label_symmetry_log2_bits),
      top1: round(row.top1),
      top5: round(row.top5),
      mrr: row.mrr === '' ? '' : round(row.mrr),
      max_control_fpr_or_null_ge_observed:
        row.max_control_fpr_or_null_ge_observed === ''
          ? ''
          : round(row.max_control_fpr_or_null_ge_observed),
    })),
    artifact_files: [
      'data/open_prototype/tools/effective_unicity_sumtablets_comparator.mjs',
      'data/open_prototype/known_scripts/sumtablets/sumtablets_source_manifest.json',
      'data/open_prototype/known_scripts/sumtablets/sumtablets_sample_rows.jsonl',
      'data/open_prototype/known_scripts/sumtablets/sumtablets_line_sequences.csv',
      'data/open_prototype/reports/effective_unicity_sumtablets_comparator_summary.json',
      'data/open_prototype/reports/effective_unicity_sumtablets_comparator.csv',
      'data/open_prototype/reports/effective_unicity_sumtablets_null_iterations.csv',
      'data/open_prototype/reports/effective_unicity_sumtablets_null_summary.csv',
    ],
  };

  fs.writeFileSync(outManifest, `${JSON.stringify(manifest, null, 2)}\n`);
  fs.writeFileSync(outSampleRows, `${sampleRows.map((row) => JSON.stringify(row)).join('\n')}\n`);
  fs.writeFileSync(
    outLineSequences,
    toCsv([
      [
        'line_id',
        'tokens',
        'length',
        'duplicate_weight',
        'first_source_tablet_id',
        'first_period',
        'first_genre',
        'periods',
        'genres',
        'source_tablet_ids',
        'source_row_indices',
        'source_line_indices',
      ],
      ...selected.map((record) => [
        record.line_id,
        record.tokens.join(' '),
        record.tokens.length,
        record.duplicate_weight,
        record.first_source_tablet_id,
        record.first_period,
        record.first_genre,
        record.periods.join('|'),
        record.genres.join('|'),
        record.source_tablet_ids.join('|'),
        record.source_row_indices.join('|'),
        record.source_line_indices.join('|'),
      ]),
    ]),
  );
  fs.writeFileSync(
    outNullIterations,
    toCsv([
      [
        'control',
        'iteration',
        'rows',
        'tokens',
        'unique_signs_or_glyphs',
        'masked_tokens',
        'masked_top1_accuracy',
        'masked_top5_accuracy',
        'masked_mrr',
        'masked_mean_effective_candidates',
      ],
      ...nullRows.map((row) => [
        row.control,
        row.iteration,
        row.rows,
        row.tokens,
        row.unique_signs_or_glyphs,
        row.masked_tokens,
        round(row.masked_top1_accuracy),
        round(row.masked_top5_accuracy),
        round(row.masked_mrr),
        round(row.masked_mean_effective_candidates),
      ]),
    ]),
  );
  fs.writeFileSync(
    outNullSummary,
    toCsv([
      [
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
      ],
      ...nullSummary.map((row) => [
        row.control,
        row.metric,
        row.iterations,
        round(row.observed),
        round(row.null_mean),
        round(row.null_p05),
        round(row.null_median),
        round(row.null_p95),
        round(row.null_max),
        round(row.null_ge_observed_share),
      ]),
    ]),
  );
  fs.writeFileSync(
    outComparatorCsv,
    toCsv([
      [
        'system',
        'experiment',
        'rows',
        'tokens_or_gaps',
        'unique_signs_or_tokens',
        'label_symmetry_log2_bits',
        'top1',
        'top5',
        'mrr',
        'median_rank',
        'max_control_fpr_or_null_ge_observed',
        'boundary',
      ],
      ...summary.rows.map((row) => [
        row.system,
        row.experiment,
        row.rows,
        row.tokens_or_gaps,
        row.unique_signs_or_tokens,
        row.label_symmetry_log2_bits,
        row.top1,
        row.top5,
        row.mrr,
        row.median_rank,
        row.max_control_fpr_or_null_ge_observed,
        row.boundary,
      ]),
    ]),
  );
  fs.writeFileSync(outSummaryJson, `${JSON.stringify(summary, null, 2)}\n`);
  console.log(JSON.stringify(summary, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
