// Experiment E5.3a: can simple statistical models fill gaps in a known script?
// The Linear B Series D bundle (Samples.txt, MD5-pinned) contains 513 clean
// sign sequences and, further down the same file, the same 513 rows each with
// exactly one sign replaced by "*". This script aligns each gapped row to its
// clean original, verifies the gap is the only difference, and then tries to
// predict the missing sign with four models: raw sign frequency, position
// frequency, length-and-position frequency, and a smoothed bidirectional
// bigram using the left and right neighbors. Each gap is scored under two
// holdout rules — row leave-one-out (only the target row leaves training) and
// the stricter sequence leave-one-out (every exact duplicate of the target
// sequence leaves too) — and within two scopes: all 513 rows, and only rows
// no longer than the Indus corpus's 95th-percentile length, so the comparison
// to Indus is length-matched. Writes the alignment, per-gap predictions, and
// summary CSVs plus a JSON summary. Comparator evidence about a known script;
// it validates nothing about any Indus sign.
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const sourcePath = path.join(base, 'data', 'open_prototype', 'known_scripts', 'linear_b_series_d', 'Samples.txt');
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const lipiScopePath = path.join(reportsDir, 'lipi_scope_rows.csv');

const alignmentPath = path.join(reportsDir, 'linear_b_series_d_gapped_alignment.csv');
const predictionsPath = path.join(reportsDir, 'linear_b_series_d_gapped_heldout_predictions.csv');
const summaryCsvPath = path.join(reportsDir, 'linear_b_series_d_gapped_heldout_summary.csv');
const summaryJsonPath = path.join(reportsDir, 'linear_b_series_d_gapped_heldout_summary.json');

const expectedMd5 = '0c9b9190b86840c82cafdbf4f4b8c827';
const smoothing = 1;

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

function md5(filePath) {
  return crypto.createHash('md5').update(fs.readFileSync(filePath)).digest('hex');
}

function parseWordTokens(line) {
  return line.trim().split(/\s+/).filter(Boolean);
}

function parseSignTokens(line) {
  return parseWordTokens(line).flatMap((token) => token.split('-').filter(Boolean));
}

function parseLipiNumericTokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
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

function formatNumber(value, digits = 6) {
  return value === null || value === undefined || Number.isNaN(value) ? null : Number(value.toFixed(digits));
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

function topRank(vocab, target, scoreFn) {
  const scored = vocab
    .map((candidate) => ({ candidate, score: scoreFn(candidate) }))
    .sort((a, b) => b.score - a.score || a.candidate.localeCompare(b.candidate));
  const targetIndex = scored.findIndex((row) => row.candidate === target);
  const rank = targetIndex >= 0 ? targetIndex + 1 : scored.length + 1;
  return {
    rank,
    top1: rank === 1,
    top5: rank <= 5,
    predicted_top1: scored[0]?.candidate ?? '',
    target_in_vocab: targetIndex >= 0,
  };
}

function rankCountMap(counts, target, vocab) {
  return topRank(vocab, target, (candidate) => counts.get(candidate) ?? 0);
}

function rankBidirectional(leftMap, rightMap, target, vocab, fallbackCounts) {
  const fallbackTotal = mapTotal(fallbackCounts);
  const leftTotal = mapTotal(leftMap);
  const rightTotal = mapTotal(rightMap);
  const vocabSize = Math.max(1, vocab.length);
  return topRank(vocab, target, (candidate) => {
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

function evaluatePairs(pairs, cleanRecords, fullVocab, scopeName, holdoutPolicy) {
  const rows = [];
  for (const pair of pairs) {
    const train =
      holdoutPolicy === 'sequence_leave_one_out'
        ? cleanRecords.filter((record) => record.sequence_key !== pair.sequence_key)
        : cleanRecords.filter((record) => record.row_index_1based !== pair.row_index_1based);
    const counts = buildGroupCounts(train);
    const positionCounts = counts.positionCounts.get(String(pair.gap_position_0based)) ?? counts.tokenCounts;
    const lengthPositionCounts =
      counts.lengthPositionCounts.get(`${pair.sign_token_count}\t${pair.gap_position_0based}`) ?? counts.tokenCounts;
    const leftCounts = counts.leftCounts.get(pair.left_context) ?? new Map();
    const rightCounts = counts.rightCounts.get(pair.right_context) ?? new Map();
    const ranks = {
      frequency: rankCountMap(counts.tokenCounts, pair.target_sign, fullVocab),
      position: rankCountMap(positionCounts, pair.target_sign, fullVocab),
      length_position: rankCountMap(lengthPositionCounts, pair.target_sign, fullVocab),
      bidirectional_bigram: rankBidirectional(leftCounts, rightCounts, pair.target_sign, fullVocab, counts.tokenCounts),
    };
    for (const [model, rank] of Object.entries(ranks)) {
      rows.push({
        scope: scopeName,
        holdout_policy: holdoutPolicy,
        row_index_1based: pair.row_index_1based,
        sign_token_count: pair.sign_token_count,
        gap_position_0based: pair.gap_position_0based,
        target_sign: pair.target_sign,
        left_context: pair.left_context,
        right_context: pair.right_context,
        exact_sequence_count: pair.exact_sequence_count,
        model,
        rank: rank.rank,
        top1: rank.top1,
        top5: rank.top5,
        predicted_top1: rank.predicted_top1,
        target_in_vocab: rank.target_in_vocab,
      });
    }
  }
  return rows;
}

function summarizePredictions(rows) {
  const groups = new Map();
  for (const row of rows) {
    const key = [row.scope, row.holdout_policy, row.model].join('\t');
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(row);
  }
  return [...groups.entries()]
    .map(([key, group]) => {
      const [scope, holdout_policy, model] = key.split('\t');
      const ranks = group.map((row) => Number(row.rank));
      return {
        scope,
        holdout_policy,
        model,
        evaluated_gaps: group.length,
        target_rows_from_exact_duplicate_sequences: group.filter((row) => Number(row.exact_sequence_count) > 1).length,
        top1: group.filter((row) => row.top1).length,
        top1_accuracy: formatNumber(group.filter((row) => row.top1).length / group.length),
        top5: group.filter((row) => row.top5).length,
        top5_accuracy: formatNumber(group.filter((row) => row.top5).length / group.length),
        mrr: formatNumber(mean(ranks.map((rank) => 1 / rank))),
        median_rank: formatNumber(median(ranks)),
        target_oov: group.filter((row) => !row.target_in_vocab).length,
      };
    })
    .sort(
      (a, b) =>
        a.scope.localeCompare(b.scope) ||
        a.holdout_policy.localeCompare(b.holdout_policy) ||
        a.model.localeCompare(b.model),
    );
}

const actualMd5 = md5(sourcePath);
if (actualMd5 !== expectedMd5) {
  throw new Error(`MD5 mismatch for Samples.txt: expected ${expectedMd5}, got ${actualMd5}`);
}

const sourceText = fs.readFileSync(sourcePath, 'utf8');
const physicalLines = sourceText.split(/\r?\n/);
const cleanLines = physicalLines.slice(0, 513);
const gappedLines = physicalLines.slice(2569, 3082).filter((line) => line.trim().length > 0);
if (gappedLines.length !== 513) throw new Error(`Expected 513 gapped rows, got ${gappedLines.length}`);

const lipiRows = parseCsv(fs.readFileSync(lipiScopePath, 'utf8'));
const lipiHeader = lipiRows[0];
const lipiColumn = Object.fromEntries(lipiHeader.map((name, index) => [name, index]));
const ivcLengths = lipiRows
  .slice(1)
  .filter((row) => row[lipiColumn.readiness_bucket] === 'lipi_numeric_clean_candidate')
  .map((row) => parseLipiNumericTokens(row[lipiColumn.text]).length)
  .filter((length) => length > 0);
const ivcP95Length = Math.ceil(quantile(ivcLengths, 0.95));

const cleanRecords = cleanLines.map((line, index) => {
  const tokens = parseSignTokens(line);
  return {
    row_index_1based: index + 1,
    raw_sequence: line.trim(),
    tokens,
    sequence_key: tokens.join(' '),
  };
});
const sequenceCounts = new Map();
for (const record of cleanRecords) bump(sequenceCounts, record.sequence_key);
const fullVocab = [...new Set(cleanRecords.flatMap((record) => record.tokens))].sort((a, b) => a.localeCompare(b));

const pairs = gappedLines.map((line, index) => {
  const original = cleanRecords[index];
  const gappedTokens = parseSignTokens(line);
  const gapPositions = gappedTokens.map((token, pos) => (token === '*' ? pos : null)).filter((pos) => pos !== null);
  if (gapPositions.length !== 1) {
    throw new Error(`Expected exactly one synthetic gap in row ${index + 1}, got ${gapPositions.length}`);
  }
  if (gappedTokens.length !== original.tokens.length) {
    throw new Error(`Token length mismatch in row ${index + 1}`);
  }
  const gap = gapPositions[0];
  for (let pos = 0; pos < gappedTokens.length; pos++) {
    if (pos !== gap && gappedTokens[pos] !== original.tokens[pos]) {
      throw new Error(`Non-gap token mismatch in row ${index + 1}, position ${pos}`);
    }
  }
  return {
    row_index_1based: index + 1,
    original_sequence: original.raw_sequence,
    gapped_sequence: line.trim(),
    sign_token_count: original.tokens.length,
    gap_position_0based: gap,
    target_sign: original.tokens[gap],
    left_context: gap === 0 ? '<s>' : gappedTokens[gap - 1],
    right_context: gap === gappedTokens.length - 1 ? '</s>' : gappedTokens[gap + 1],
    ivc_p95_length_eligible: original.tokens.length <= ivcP95Length,
    exact_sequence_count: sequenceCounts.get(original.sequence_key),
    sequence_key: original.sequence_key,
  };
});

const scopes = [
  ['all_513_gapped_rows', pairs],
  ['ivc_p95_length_cap_gapped_rows', pairs.filter((pair) => pair.ivc_p95_length_eligible)],
];
const holdoutPolicies = ['row_leave_one_out', 'sequence_leave_one_out'];

const predictionRows = [];
for (const [scopeName, scopedPairs] of scopes) {
  for (const holdoutPolicy of holdoutPolicies) {
    predictionRows.push(...evaluatePairs(scopedPairs, cleanRecords, fullVocab, scopeName, holdoutPolicy));
  }
}
const summaryRows = summarizePredictions(predictionRows);

fs.writeFileSync(
  alignmentPath,
  toCsv([
    [
      'row_index_1based',
      'sign_token_count',
      'gap_position_0based',
      'target_sign',
      'left_context',
      'right_context',
      'ivc_p95_length_eligible',
      'exact_sequence_count',
      'original_sequence',
      'gapped_sequence',
    ],
    ...pairs.map((pair) => [
      pair.row_index_1based,
      pair.sign_token_count,
      pair.gap_position_0based,
      pair.target_sign,
      pair.left_context,
      pair.right_context,
      pair.ivc_p95_length_eligible,
      pair.exact_sequence_count,
      pair.original_sequence,
      pair.gapped_sequence,
    ]),
  ]),
  'utf8',
);

fs.writeFileSync(
  predictionsPath,
  toCsv([
    [
      'scope',
      'holdout_policy',
      'row_index_1based',
      'sign_token_count',
      'gap_position_0based',
      'target_sign',
      'left_context',
      'right_context',
      'exact_sequence_count',
      'model',
      'rank',
      'top1',
      'top5',
      'predicted_top1',
      'target_in_vocab',
    ],
    ...predictionRows.map((row) => [
      row.scope,
      row.holdout_policy,
      row.row_index_1based,
      row.sign_token_count,
      row.gap_position_0based,
      row.target_sign,
      row.left_context,
      row.right_context,
      row.exact_sequence_count,
      row.model,
      row.rank,
      row.top1,
      row.top5,
      row.predicted_top1,
      row.target_in_vocab,
    ]),
  ]),
  'utf8',
);

fs.writeFileSync(
  summaryCsvPath,
  toCsv([
    [
      'scope',
      'holdout_policy',
      'model',
      'evaluated_gaps',
      'target_rows_from_exact_duplicate_sequences',
      'top1',
      'top1_accuracy',
      'top5',
      'top5_accuracy',
      'mrr',
      'median_rank',
      'target_oov',
    ],
    ...summaryRows.map((row) => [
      row.scope,
      row.holdout_policy,
      row.model,
      row.evaluated_gaps,
      row.target_rows_from_exact_duplicate_sequences,
      row.top1,
      row.top1_accuracy,
      row.top5,
      row.top5_accuracy,
      row.mrr,
      row.median_rank,
      row.target_oov,
    ]),
  ]),
  'utf8',
);

const summary = {
  generated_at_local: formatLocalIso(new Date()),
  experiment: 'E5.3a Linear B Series D Gapped Held-Out Test',
  source_file: 'data/open_prototype/known_scripts/linear_b_series_d/Samples.txt',
  source_md5: actualMd5,
  source_md5_verified: actualMd5 === expectedMd5,
  gapped_rows: pairs.length,
  gap_encoding: 'exact sign token "*" after hyphen splitting; asterisk-number signs such as *56 are preserved as real tokens',
  gap_count_per_row: {
    exactly_one_gap_rows: pairs.length,
    other_gap_count_rows: 0,
  },
  ivc_like_length_cap: {
    cap_sign_tokens: ivcP95Length,
    ivc_numeric_clean_rows: ivcLengths.length,
    ivc_length_mean: formatNumber(mean(ivcLengths)),
    ivc_length_median: formatNumber(median(ivcLengths)),
    ivc_length_p95: formatNumber(quantile(ivcLengths, 0.95)),
    eligible_gapped_rows: pairs.filter((pair) => pair.ivc_p95_length_eligible).length,
  },
  duplicate_exposure: {
    exact_duplicate_sequence_rows_in_targets: pairs.filter((pair) => pair.exact_sequence_count > 1).length,
    row_leave_one_out: 'removes only the target row from training; exact duplicate sequences can remain',
    sequence_leave_one_out: 'removes every clean-row training sequence identical to the target original sequence',
  },
  primary_results: Object.fromEntries(
    summaryRows
      .filter((row) => row.model === 'bidirectional_bigram')
      .map((row) => [
        `${row.scope}__${row.holdout_policy}`,
        {
          evaluated_gaps: row.evaluated_gaps,
          top1_accuracy: row.top1_accuracy,
          top5_accuracy: row.top5_accuracy,
          mrr: row.mrr,
          median_rank: row.median_rank,
        },
      ]),
  ),
  interpretation_boundary:
    'Known-script comparator only. This evaluates recovery of source-provided synthetic Linear B gaps with known readings hidden. It does not validate any IVC sign, side relation, semantic field, phonetic value, language identity, or translation.',
  artifact_files: [
    'data/open_prototype/reports/linear_b_series_d_gapped_alignment.csv',
    'data/open_prototype/reports/linear_b_series_d_gapped_heldout_predictions.csv',
    'data/open_prototype/reports/linear_b_series_d_gapped_heldout_summary.csv',
    'data/open_prototype/reports/linear_b_series_d_gapped_heldout_summary.json',
  ],
};
fs.writeFileSync(summaryJsonPath, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
