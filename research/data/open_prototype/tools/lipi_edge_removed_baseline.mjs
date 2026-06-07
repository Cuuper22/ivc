import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const sourcePath = path.join(reportsDir, 'lipi_scope_rows.csv');
const outInventory = path.join(reportsDir, 'lipi_edge_sign_inventory.csv');
const outSequence = path.join(reportsDir, 'lipi_edge_removed_sequence_summary.csv');
const outMasked = path.join(reportsDir, 'lipi_edge_removed_masked_summary.csv');
const outHoldout = path.join(reportsDir, 'lipi_edge_removed_holdout_summary.csv');
const outJson = path.join(reportsDir, 'lipi_edge_removed_summary.json');

const minGroupRows = 50;
const smoothing = 1;
const epsilon = 1e-9;

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

function parseTokens(text) {
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

function subtractMap(baseMap, removeMap) {
  const out = new Map(baseMap);
  for (const [key, value] of removeMap.entries()) {
    const next = (out.get(key) ?? 0) - value;
    if (next <= 0) out.delete(key);
    else out.set(key, next);
  }
  return out;
}

function subtractNested(baseMap, removeMap) {
  const out = new Map();
  for (const [key, inner] of baseMap.entries()) {
    out.set(key, new Map(inner));
  }
  for (const [key, inner] of removeMap.entries()) {
    if (!out.has(key)) continue;
    const target = out.get(key);
    for (const [token, value] of inner.entries()) {
      const next = (target.get(token) ?? 0) - value;
      if (next <= 0) target.delete(token);
      else target.set(token, next);
    }
    if (target.size === 0) out.delete(key);
  }
  return out;
}

function mapTotal(map) {
  let total = 0;
  for (const value of map.values()) total += value;
  return total;
}

function median(values) {
  if (!values.length) return null;
  const sorted = values.slice().sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
}

function formatNumber(value) {
  return value === null || value === undefined ? null : Number(value.toFixed(6));
}

function rankToken(counts, token, vocab) {
  const sorted = [...vocab].sort((a, b) => {
    const diff = (counts.get(b) ?? 0) - (counts.get(a) ?? 0);
    return diff || a.localeCompare(b);
  });
  const index = sorted.indexOf(token);
  return {
    rank: index === -1 ? sorted.length + 1 : index + 1,
    top1: index === 0,
    top5: index >= 0 && index < 5,
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

function modelRankByKey(globalNested, rowNested, key, token, vocab, fallbackCounts) {
  const countsByKey = subtractNested(globalNested, rowNested).get(key) ?? new Map();
  const counts = countsByKey.size ? countsByKey : fallbackCounts;
  return rankToken(counts, token, vocab);
}

function modelRankByKeyNoSubtract(globalNested, key, token, vocab, fallbackCounts) {
  const counts = globalNested.get(key) ?? new Map();
  return rankToken(counts.size ? counts : fallbackCounts, token, vocab);
}

function modelRankBidirectional(globalLeft, rowLeft, globalRight, rowRight, left, right, token, vocab, fallbackCounts) {
  const leftMap = subtractNested(globalLeft, rowLeft).get(left) ?? new Map();
  const rightMap = subtractNested(globalRight, rowRight).get(right) ?? new Map();
  return rankBidirectional(leftMap, rightMap, left, right, token, vocab, fallbackCounts);
}

function modelRankBidirectionalNoSubtract(globalLeft, globalRight, left, right, token, vocab, fallbackCounts) {
  const leftMap = globalLeft.get(left) ?? new Map();
  const rightMap = globalRight.get(right) ?? new Map();
  return rankBidirectional(leftMap, rightMap, left, right, token, vocab, fallbackCounts);
}

function rankBidirectional(leftMap, rightMap, left, right, token, vocab, fallbackCounts) {
  const fallbackTotal = mapTotal(fallbackCounts);
  const leftTotal = mapTotal(leftMap);
  const rightTotal = mapTotal(rightMap);
  const vocabSize = Math.max(1, vocab.length);
  const scored = [...vocab].map((candidate) => {
    const leftScore =
      leftTotal > 0
        ? Math.log(((leftMap.get(candidate) ?? 0) + smoothing) / (leftTotal + smoothing * vocabSize))
        : Math.log(((fallbackCounts.get(candidate) ?? 0) + smoothing) / (fallbackTotal + smoothing * vocabSize));
    const rightScore =
      rightTotal > 0
        ? Math.log(((rightMap.get(candidate) ?? 0) + smoothing) / (rightTotal + smoothing * vocabSize))
        : Math.log(((fallbackCounts.get(candidate) ?? 0) + smoothing) / (fallbackTotal + smoothing * vocabSize));
    return [candidate, leftScore + rightScore, left, right];
  });
  scored.sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  const index = scored.findIndex(([candidate]) => candidate === token);
  return {
    rank: index === -1 ? scored.length + 1 : index + 1,
    top1: index === 0,
    top5: index >= 0 && index < 5,
  };
}

function transitionCounts(records) {
  const counts = new Map();
  const totals = new Map();
  for (const record of records) {
    const seq = ['<s>', ...record.tokens, '</s>'];
    for (let i = 0; i < seq.length - 1; i++) {
      const from = seq[i];
      const to = seq[i + 1];
      addNested(counts, from, to);
      bump(totals, from);
    }
  }
  return { counts, totals };
}

function rowTransitionCounts(tokens) {
  return transitionCounts([{ tokens }]);
}

function subtractTransitionCounts(global, row) {
  return {
    counts: subtractNested(global.counts, row.counts),
    totals: subtractMap(global.totals, row.totals),
  };
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

function countEdgeSigns(records) {
  const signs = new Map();
  for (const record of records) {
    for (const token of record.tokens) {
      if (!signs.has(token)) {
        signs.set(token, {
          sign: token,
          total_count: 0,
          initial_count: 0,
          terminal_count: 0,
          single_sign_count: 0,
        });
      }
      signs.get(token).total_count++;
    }
    if (!record.tokens.length) continue;
    const first = record.tokens[0];
    const last = record.tokens[record.tokens.length - 1];
    signs.get(first).initial_count++;
    signs.get(last).terminal_count++;
    if (record.tokens.length === 1) signs.get(first).single_sign_count++;
  }
  return [...signs.values()]
    .map((row) => ({
      ...row,
      edge_count: row.initial_count + row.terminal_count,
      edge_share_of_total: row.total_count > 0 ? formatNumber((row.initial_count + row.terminal_count) / row.total_count) : null,
    }))
    .sort((a, b) => b.edge_count - a.edge_count || b.total_count - a.total_count || a.sign.localeCompare(b.sign));
}

function transformRecords(records, removedSigns, policy) {
  const remove = new Set(removedSigns);
  return records
    .map((record) => {
      const tokens = record.tokens.filter((token) => !remove.has(token));
      return {
        ...record,
        tokens,
        original_length: record.tokens.length,
        removed_tokens: record.tokens.length - tokens.length,
        edge_policy: policy,
      };
    })
    .filter((record) => record.tokens.length > 0);
}

function collapseRecords(records) {
  const seen = new Map();
  for (const record of records) {
    const key = record.tokens.join(' ');
    if (!seen.has(key)) {
      seen.set(key, { ...record, duplicate_weight: 1 });
    } else {
      seen.get(key).duplicate_weight++;
    }
  }
  return [...seen.values()];
}

function evaluateSequence(policy, collapsePolicy, sourceRows, records) {
  const usable = records.filter((record) => record.tokens.length > 0);
  const vocab = [...new Set(usable.flatMap((record) => record.tokens))];
  const vocabSize = vocab.length + 2;
  const globalTransitions = transitionCounts(usable);
  let storedHigher = 0;
  let reversedHigher = 0;
  let ties = 0;
  let rowsGtOne = 0;
  const diffs = [];
  for (const record of usable) {
    if (record.tokens.length <= 1) continue;
    rowsGtOne++;
    const rowTransitions = rowTransitionCounts(record.tokens);
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
    policy,
    collapse_policy: collapsePolicy,
    source_rows: sourceRows,
    evaluated_rows: usable.length,
    rows_dropped_empty: sourceRows - usable.length,
    tokens: usable.reduce((sum, record) => sum + record.tokens.length, 0),
    unique_signs: vocab.length,
    duplicate_rows_removed_after_policy: sourceRows - usable.length,
    rows_length_gt_1: rowsGtOne,
    stored_higher_than_reversed: storedHigher,
    reversed_higher_than_stored: reversedHigher,
    ties,
    stored_higher_share: rowsGtOne > 0 ? formatNumber(storedHigher / rowsGtOne) : null,
    mean_stored_minus_reversed:
      diffs.length > 0 ? formatNumber(diffs.reduce((sum, value) => sum + value, 0) / diffs.length) : null,
    median_stored_minus_reversed: diffs.length > 0 ? formatNumber(median(diffs)) : null,
  };
}

function evaluateMasked(policy, collapsePolicy, sourceRows, records) {
  const usable = records.filter((record) => record.tokens.length > 0);
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
    const fallbackCounts = subtractMap(globalCounts.tokenCounts, rowCounts.tokenCounts);
    const len = record.tokens.length;
    for (let i = 0; i < len; i++) {
      const token = record.tokens[i];
      const left = i === 0 ? '<s>' : record.tokens[i - 1];
      const right = i === len - 1 ? '</s>' : record.tokens[i + 1];
      const ranks = {
        frequency: rankToken(fallbackCounts, token, vocab),
        position: modelRankByKey(globalCounts.positionCounts, rowCounts.positionCounts, String(i), token, vocab, fallbackCounts),
        length_position: modelRankByKey(
          globalCounts.lengthPositionCounts,
          rowCounts.lengthPositionCounts,
          `${len}\t${i}`,
          token,
          vocab,
          fallbackCounts,
        ),
        bidirectional_bigram: modelRankBidirectional(
          globalCounts.leftCounts,
          rowCounts.leftCounts,
          globalCounts.rightCounts,
          rowCounts.rightCounts,
          left,
          right,
          token,
          vocab,
          fallbackCounts,
        ),
      };
      for (const [model, rank] of Object.entries(ranks)) {
        models[model].masked_tokens++;
        if (rank.top1) models[model].top1++;
        if (rank.top5) models[model].top5++;
        models[model].mrr_sum += 1 / rank.rank;
      }
    }
  }
  return Object.entries(models).map(([model, value]) => ({
    policy,
    collapse_policy: collapsePolicy,
    source_rows: sourceRows,
    evaluated_rows: usable.length,
    model,
    masked_tokens: value.masked_tokens,
    top1: value.top1,
    top1_accuracy: value.masked_tokens > 0 ? formatNumber(value.top1 / value.masked_tokens) : null,
    top5: value.top5,
    top5_accuracy: value.masked_tokens > 0 ? formatNumber(value.top5 / value.masked_tokens) : null,
    mrr: value.masked_tokens > 0 ? formatNumber(value.mrr_sum / value.masked_tokens) : null,
  }));
}

function evaluateMaskedHoldout(policy, kind, value, sourceTestRows, testRecords, trainRecordsBeforeLeakage) {
  const test = collapseRecords(testRecords.filter((record) => record.tokens.length > 0));
  const trainBefore = collapseRecords(trainRecordsBeforeLeakage.filter((record) => record.tokens.length > 0));
  const testSequences = new Set(test.map((record) => record.tokens.join(' ')));
  const train = trainBefore.filter((record) => !testSequences.has(record.tokens.join(' ')));
  const globalCounts = buildGroupCounts(train);
  const vocab = [...globalCounts.tokenCounts.keys()].sort((a, b) => a.localeCompare(b));
  const fallbackCounts = globalCounts.tokenCounts;
  const models = {
    frequency: { masked_tokens: 0, top1: 0, top5: 0, mrr_sum: 0, out_of_vocab: 0 },
    position: { masked_tokens: 0, top1: 0, top5: 0, mrr_sum: 0, out_of_vocab: 0 },
    length_position: { masked_tokens: 0, top1: 0, top5: 0, mrr_sum: 0, out_of_vocab: 0 },
    bidirectional_bigram: { masked_tokens: 0, top1: 0, top5: 0, mrr_sum: 0, out_of_vocab: 0 },
  };
  for (const record of test) {
    const len = record.tokens.length;
    for (let i = 0; i < len; i++) {
      const token = record.tokens[i];
      const left = i === 0 ? '<s>' : record.tokens[i - 1];
      const right = i === len - 1 ? '</s>' : record.tokens[i + 1];
      const tokenInVocab = globalCounts.tokenCounts.has(token);
      const ranks = tokenInVocab
        ? {
            frequency: rankToken(globalCounts.tokenCounts, token, vocab),
            position: modelRankByKeyNoSubtract(globalCounts.positionCounts, String(i), token, vocab, fallbackCounts),
            length_position: modelRankByKeyNoSubtract(
              globalCounts.lengthPositionCounts,
              `${len}\t${i}`,
              token,
              vocab,
              fallbackCounts,
            ),
            bidirectional_bigram: modelRankBidirectionalNoSubtract(
              globalCounts.leftCounts,
              globalCounts.rightCounts,
              left,
              right,
              token,
              vocab,
              fallbackCounts,
            ),
          }
        : null;
      for (const [model, row] of Object.entries(models)) {
        row.masked_tokens++;
        if (!tokenInVocab) {
          row.out_of_vocab++;
          continue;
        }
        const rank = ranks[model];
        if (rank.top1) row.top1++;
        if (rank.top5) row.top5++;
        row.mrr_sum += 1 / rank.rank;
      }
    }
  }
  return Object.entries(models).map(([model, row]) => ({
    policy,
    holdout_kind: kind,
    holdout_value: value,
    source_test_rows: sourceTestRows,
    test_rows_after_edge_removal: testRecords.filter((record) => record.tokens.length > 0).length,
    test_rows_after_collapse: test.length,
    duplicate_test_rows_removed_after_policy: testRecords.filter((record) => record.tokens.length > 0).length - test.length,
    train_rows_before_leakage_filter: trainBefore.length,
    leakage_train_sequences_removed: trainBefore.length - train.length,
    train_rows: train.length,
    test_rows: test.length,
    test_sequences_seen_in_train: 0,
    test_sequence_seen_share: 0,
    model,
    masked_tokens: row.masked_tokens,
    out_of_vocab_tokens: row.out_of_vocab,
    out_of_vocab_share: row.masked_tokens > 0 ? formatNumber(row.out_of_vocab / row.masked_tokens) : null,
    top1: row.top1,
    top1_accuracy: row.masked_tokens > 0 ? formatNumber(row.top1 / row.masked_tokens) : null,
    top5: row.top5,
    top5_accuracy: row.masked_tokens > 0 ? formatNumber(row.top5 / row.masked_tokens) : null,
    mrr: row.masked_tokens > 0 ? formatNumber(row.mrr_sum / row.masked_tokens) : null,
  }));
}

function groupValues(records, field) {
  const counts = new Map();
  for (const record of records) {
    bump(counts, record[field] || '-');
  }
  return [...counts.entries()].filter(([, count]) => count >= minGroupRows).map(([value]) => value);
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

const rows = parseCsv(fs.readFileSync(sourcePath, 'utf8'));
const header = rows[0];
const column = Object.fromEntries(header.map((name, index) => [name, index]));
const records = rows.slice(1).map((row) => ({
  id: row[column.id],
  cisi: row[column.cisi],
  region: row[column.region],
  site: row[column.site],
  type: row[column.type],
  direction: row[column.direction],
  readiness: row[column.readiness_bucket],
  tokens: parseTokens(row[column.text]),
}));

const numericClean = records.filter((record) => record.readiness === 'lipi_numeric_clean_candidate');
const edgeInventory = countEdgeSigns(numericClean);
const edgeTop2 = edgeInventory.slice(0, 2).map((row) => row.sign);
const edgeTop5 = edgeInventory.slice(0, 5).map((row) => row.sign);
const edgeTop10 = edgeInventory.slice(0, 10).map((row) => row.sign);
const policies = [
  { policy: 'no_edge_removal', removedSigns: [] },
  { policy: 'remove_top_2_edge_signs', removedSigns: edgeTop2 },
  { policy: 'remove_top_5_edge_signs', removedSigns: edgeTop5 },
  { policy: 'remove_top_10_edge_signs', removedSigns: edgeTop10 },
];

const sequenceSummary = [];
const maskedSummary = [];
const holdoutSummary = [];

for (const { policy, removedSigns } of policies) {
  const transformed = transformRecords(numericClean, removedSigns, policy);
  const collapsed = collapseRecords(transformed);
  sequenceSummary.push(evaluateSequence(policy, 'source_weighted_after_edge_policy', numericClean.length, transformed));
  sequenceSummary.push(
    evaluateSequence(policy, 'exact_sequence_collapsed_after_edge_policy', numericClean.length, collapsed),
  );
  maskedSummary.push(
    ...evaluateMasked(policy, 'exact_sequence_collapsed_after_edge_policy', numericClean.length, collapsed),
  );

  const transformedById = new Map(transformed.map((record) => [record.id, record]));
  const transformedNumericClean = numericClean
    .map((record) => transformedById.get(record.id))
    .filter(Boolean);

  for (const [kind, field] of [
    ['type', 'type'],
    ['site', 'site'],
    ['region', 'region'],
  ]) {
    for (const value of groupValues(numericClean, field)) {
      const originalTest = numericClean.filter((record) => (record[field] || '-') === value);
      const test = transformedNumericClean.filter((record) => (record[field] || '-') === value);
      const train = transformedNumericClean.filter((record) => (record[field] || '-') !== value);
      holdoutSummary.push(...evaluateMaskedHoldout(policy, kind, value, originalTest.length, test, train));
    }
  }
}

fs.writeFileSync(
  outInventory,
  toCsv([
    ['sign', 'edge_rank', 'total_count', 'initial_count', 'terminal_count', 'single_sign_count', 'edge_count', 'edge_share_of_total'],
    ...edgeInventory.map((row, index) => [
      row.sign,
      index + 1,
      row.total_count,
      row.initial_count,
      row.terminal_count,
      row.single_sign_count,
      row.edge_count,
      row.edge_share_of_total,
    ]),
  ]),
  'utf8',
);

fs.writeFileSync(
  outSequence,
  toCsv([
    [
      'policy',
      'collapse_policy',
      'source_rows',
      'evaluated_rows',
      'rows_dropped_empty',
      'tokens',
      'unique_signs',
      'duplicate_rows_removed_after_policy',
      'rows_length_gt_1',
      'stored_higher_than_reversed',
      'reversed_higher_than_stored',
      'ties',
      'stored_higher_share',
      'mean_stored_minus_reversed',
      'median_stored_minus_reversed',
    ],
    ...sequenceSummary.map((row) => [
      row.policy,
      row.collapse_policy,
      row.source_rows,
      row.evaluated_rows,
      row.rows_dropped_empty,
      row.tokens,
      row.unique_signs,
      row.duplicate_rows_removed_after_policy,
      row.rows_length_gt_1,
      row.stored_higher_than_reversed,
      row.reversed_higher_than_stored,
      row.ties,
      row.stored_higher_share,
      row.mean_stored_minus_reversed,
      row.median_stored_minus_reversed,
    ]),
  ]),
  'utf8',
);

fs.writeFileSync(
  outMasked,
  toCsv([
    [
      'policy',
      'collapse_policy',
      'source_rows',
      'evaluated_rows',
      'model',
      'masked_tokens',
      'top1',
      'top1_accuracy',
      'top5',
      'top5_accuracy',
      'mrr',
    ],
    ...maskedSummary.map((row) => [
      row.policy,
      row.collapse_policy,
      row.source_rows,
      row.evaluated_rows,
      row.model,
      row.masked_tokens,
      row.top1,
      row.top1_accuracy,
      row.top5,
      row.top5_accuracy,
      row.mrr,
    ]),
  ]),
  'utf8',
);

fs.writeFileSync(
  outHoldout,
  toCsv([
    [
      'policy',
      'holdout_kind',
      'holdout_value',
      'source_test_rows',
      'test_rows_after_edge_removal',
      'test_rows_after_collapse',
      'duplicate_test_rows_removed_after_policy',
      'train_rows_before_leakage_filter',
      'leakage_train_sequences_removed',
      'train_rows',
      'test_rows',
      'test_sequences_seen_in_train',
      'test_sequence_seen_share',
      'model',
      'masked_tokens',
      'out_of_vocab_tokens',
      'out_of_vocab_share',
      'top1',
      'top1_accuracy',
      'top5',
      'top5_accuracy',
      'mrr',
    ],
    ...holdoutSummary.map((row) => [
      row.policy,
      row.holdout_kind,
      row.holdout_value,
      row.source_test_rows,
      row.test_rows_after_edge_removal,
      row.test_rows_after_collapse,
      row.duplicate_test_rows_removed_after_policy,
      row.train_rows_before_leakage_filter,
      row.leakage_train_sequences_removed,
      row.train_rows,
      row.test_rows,
      row.test_sequences_seen_in_train,
      row.test_sequence_seen_share,
      row.model,
      row.masked_tokens,
      row.out_of_vocab_tokens,
      row.out_of_vocab_share,
      row.top1,
      row.top1_accuracy,
      row.top5,
      row.top5_accuracy,
      row.mrr,
    ]),
  ]),
  'utf8',
);

const summary = {
  generated_at_local: formatLocalIso(new Date()),
  source_file: 'data/open_prototype/reports/lipi_scope_rows.csv',
  parent_baselines: [
    'data/open_prototype/reports/lipi_dedup_order_summary.json',
    'data/open_prototype/reports/lipi_leakage_control_summary.json',
  ],
  edge_sign_policy:
    'Rank signs by initial plus terminal occurrence count in strict numeric-clean lipi rows. For each removal policy, remove those signs from every sequence, drop empty rows, optionally collapse exact duplicate resulting sequences, then rerun order, masked-sign, and leakage-controlled held-out checks.',
  top_edge_signs: edgeInventory.slice(0, 10),
  policies: policies.map((row) => ({ policy: row.policy, removed_signs: row.removedSigns })),
  sequence_summary: sequenceSummary,
  masked_summary: maskedSummary,
  holdout_summary: holdoutSummary,
  artifact_files: [
    'data/open_prototype/reports/lipi_edge_sign_inventory.csv',
    'data/open_prototype/reports/lipi_edge_removed_sequence_summary.csv',
    'data/open_prototype/reports/lipi_edge_removed_masked_summary.csv',
    'data/open_prototype/reports/lipi_edge_removed_holdout_summary.csv',
    'data/open_prototype/reports/lipi_edge_removed_summary.json',
  ],
  interpretation_boundary:
    'High-frequency-edge-removal T3 structural scout only; stored-order and masked-sign results are not sign values, semantics, phonetics, or translations.',
};

fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(
  JSON.stringify(
    {
      top_edge_signs: summary.top_edge_signs,
      sequence_rows: sequenceSummary.length,
      masked_rows: maskedSummary.length,
      holdout_rows: holdoutSummary.length,
      selected_collapsed_sequence: sequenceSummary.filter(
        (row) => row.collapse_policy === 'exact_sequence_collapsed_after_edge_policy',
      ),
      selected_collapsed_masked_bidirectional: maskedSummary.filter(
        (row) =>
          row.collapse_policy === 'exact_sequence_collapsed_after_edge_policy' &&
          row.model === 'bidirectional_bigram',
      ),
      wrote: summary.artifact_files,
    },
    null,
    2,
  ),
);
