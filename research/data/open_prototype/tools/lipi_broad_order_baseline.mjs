// This is the broad structural baseline for the Indus corpus itself: a first
// wide sweep over lipi_scope_rows.csv measuring how much internal order the
// inscriptions carry, before any comparator or null-model work. For the clean
// numeric rows (plus a direction-clean sensitivity scope) it computes, per
// group — the whole corpus and every type, site, and region with at least 50
// rows — three things: duplicate-sequence statistics, a stored-vs-reversed
// direction score using a leave-one-out smoothed bigram model, and masked-
// sign prediction under four models (frequency, position, length-position,
// bidirectional bigram). It then repeats the masked test as a true holdout:
// train on all other types/sites/regions, test on the held-out group. Every
// analysis runs three times with increasing strictness: raw rows; exact
// duplicate sequences collapsed to one representative; and leakage-
// controlled, where any training sequence identical to a held-out test
// sequence is removed. Writes fifteen sequence/masked/holdout/group CSVs and
// three JSON summaries. A claim-free structural scout — none of these
// numbers are sign values, sounds, or translations.
import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const sourcePath = path.join(reportsDir, 'lipi_scope_rows.csv');
const outSequence = path.join(reportsDir, 'lipi_broad_order_sequence_summary.csv');
const outMasked = path.join(reportsDir, 'lipi_broad_order_masked_summary.csv');
const outHoldout = path.join(reportsDir, 'lipi_broad_order_holdout_summary.csv');
const outGroups = path.join(reportsDir, 'lipi_broad_order_group_inventory.csv');
const outJson = path.join(reportsDir, 'lipi_broad_order_summary.json');
const outDedupSequence = path.join(reportsDir, 'lipi_dedup_order_sequence_summary.csv');
const outDedupMasked = path.join(reportsDir, 'lipi_dedup_order_masked_summary.csv');
const outDedupHoldout = path.join(reportsDir, 'lipi_dedup_order_holdout_summary.csv');
const outDedupGroups = path.join(reportsDir, 'lipi_dedup_order_group_inventory.csv');
const outDedupJson = path.join(reportsDir, 'lipi_dedup_order_summary.json');
const outLeakageHoldout = path.join(reportsDir, 'lipi_leakage_control_holdout_summary.csv');
const outLeakageJson = path.join(reportsDir, 'lipi_leakage_control_summary.json');

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
  const key = keys.join('\t');
  addNested(map, key, token, by);
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

function modelRankFrequency(globalCounts, rowCounts, token, vocab) {
  return rankToken(subtractMap(globalCounts, rowCounts), token, vocab);
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
    return [candidate, leftScore + rightScore];
  });
  scored.sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  const index = scored.findIndex(([candidate]) => candidate === token);
  return {
    rank: index === -1 ? scored.length + 1 : index + 1,
    top1: index === 0,
    top5: index >= 0 && index < 5,
  };
}

function modelRankBidirectionalNoSubtract(globalLeft, globalRight, left, right, token, vocab, fallbackCounts) {
  const leftMap = globalLeft.get(left) ?? new Map();
  const rightMap = globalRight.get(right) ?? new Map();
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
    return [candidate, leftScore + rightScore];
  });
  scored.sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  const index = scored.findIndex(([candidate]) => candidate === token);
  return {
    rank: index === -1 ? scored.length + 1 : index + 1,
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

function subtractTransitionCounts(global, row) {
  const counts = subtractNested(global.counts, row.counts);
  const totals = subtractMap(global.totals, row.totals);
  return { counts, totals };
}

function median(values) {
  if (!values.length) return null;
  const sorted = values.slice().sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
}

function lengthBucket(length) {
  if (length <= 3) return '1-3';
  if (length <= 5) return '4-5';
  if (length <= 8) return '6-8';
  return '9+';
}

function evaluateSequence(group) {
  const records = group.records.filter((record) => record.tokens.length > 0);
  const vocab = [...new Set(records.flatMap((record) => record.tokens))];
  const vocabSize = vocab.length + 2;
  const globalTransitions = transitionCounts(records);
  const sequenceCounts = new Map();
  for (const record of records) {
    bump(sequenceCounts, record.tokens.join(' '));
  }
  let exactDuplicateGroups = 0;
  let exactDuplicateRows = 0;
  let topSequenceCount = 0;
  for (const count of sequenceCounts.values()) {
    topSequenceCount = Math.max(topSequenceCount, count);
    if (count > 1) {
      exactDuplicateGroups++;
      exactDuplicateRows += count;
    }
  }
  const diffs = [];
  const byBucket = new Map();
  let storedHigher = 0;
  let reversedHigher = 0;
  let ties = 0;
  let rowsGtOne = 0;
  for (const record of records) {
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
    const bucket = lengthBucket(record.tokens.length);
    if (!byBucket.has(bucket)) {
      byBucket.set(bucket, { rows: 0, stored_higher: 0, reversed_higher: 0, ties: 0 });
    }
    const row = byBucket.get(bucket);
    row.rows++;
    if (diff > epsilon) row.stored_higher++;
    else if (diff < -epsilon) row.reversed_higher++;
    else row.ties++;
  }
  return {
    scope: group.scope,
    group_kind: group.groupKind,
    group_value: group.groupValue,
    rows: records.length,
    tokens: records.reduce((sum, record) => sum + record.tokens.length, 0),
    unique_signs: vocab.length,
    exact_sequence_groups: sequenceCounts.size,
    exact_duplicate_groups: exactDuplicateGroups,
    exact_duplicate_rows: exactDuplicateRows,
    top_sequence_count: topSequenceCount,
    rows_length_gt_1: rowsGtOne,
    stored_higher_than_reversed: storedHigher,
    reversed_higher_than_stored: reversedHigher,
    ties,
    stored_higher_share:
      rowsGtOne > 0 ? Number((storedHigher / rowsGtOne).toFixed(6)) : null,
    mean_stored_minus_reversed:
      diffs.length > 0 ? Number((diffs.reduce((sum, value) => sum + value, 0) / diffs.length).toFixed(6)) : null,
    median_stored_minus_reversed: diffs.length > 0 ? Number(median(diffs).toFixed(6)) : null,
    by_length_bucket: [...byBucket.entries()].map(([bucket, value]) => ({ bucket, ...value })),
  };
}

function evaluateMasked(group) {
  const records = group.records.filter((record) => record.tokens.length > 0);
  const globalCounts = buildGroupCounts(records);
  const vocab = [...globalCounts.tokenCounts.keys()].sort((a, b) => a.localeCompare(b));
  const models = {
    frequency: { masked_tokens: 0, top1: 0, top5: 0, mrr_sum: 0 },
    position: { masked_tokens: 0, top1: 0, top5: 0, mrr_sum: 0 },
    length_position: { masked_tokens: 0, top1: 0, top5: 0, mrr_sum: 0 },
    bidirectional_bigram: { masked_tokens: 0, top1: 0, top5: 0, mrr_sum: 0 },
  };

  for (const record of records) {
    const rowCounts = recordCounts(record);
    const fallbackCounts = subtractMap(globalCounts.tokenCounts, rowCounts.tokenCounts);
    const len = record.tokens.length;
    for (let i = 0; i < len; i++) {
      const token = record.tokens[i];
      const left = i === 0 ? '<s>' : record.tokens[i - 1];
      const right = i === len - 1 ? '</s>' : record.tokens[i + 1];
      const ranks = {
        frequency: modelRankFrequency(globalCounts.tokenCounts, rowCounts.tokenCounts, token, vocab),
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
    scope: group.scope,
    group_kind: group.groupKind,
    group_value: group.groupValue,
    rows: records.length,
    model,
    masked_tokens: value.masked_tokens,
    top1: value.top1,
    top1_accuracy: Number((value.top1 / value.masked_tokens).toFixed(6)),
    top5: value.top5,
    top5_accuracy: Number((value.top5 / value.masked_tokens).toFixed(6)),
    mrr: Number((value.mrr_sum / value.masked_tokens).toFixed(6)),
  }));
}

function evaluateMaskedHoldout(testGroup, trainRecords) {
  const train = trainRecords.filter((record) => record.tokens.length > 0);
  const test = testGroup.records.filter((record) => record.tokens.length > 0);
  const trainSequenceSet = new Set(train.map((record) => record.tokens.join(' ')));
  const testSequencesSeenInTrain = test.filter((record) => trainSequenceSet.has(record.tokens.join(' '))).length;
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
      for (const [model, value] of Object.entries(models)) {
        value.masked_tokens++;
        if (!tokenInVocab) {
          value.out_of_vocab++;
          continue;
        }
        const rank = ranks[model];
        if (rank.top1) value.top1++;
        if (rank.top5) value.top5++;
        value.mrr_sum += 1 / rank.rank;
      }
    }
  }

  return Object.entries(models).map(([model, value]) => ({
    scope: testGroup.scope,
    holdout_kind: testGroup.groupKind,
    holdout_value: testGroup.groupValue,
    train_rows: train.length,
    test_rows: test.length,
    test_sequences_seen_in_train: testSequencesSeenInTrain,
    test_sequence_seen_share: Number((testSequencesSeenInTrain / test.length).toFixed(6)),
    model,
    masked_tokens: value.masked_tokens,
    out_of_vocab_tokens: value.out_of_vocab,
    out_of_vocab_share: Number((value.out_of_vocab / value.masked_tokens).toFixed(6)),
    top1: value.top1,
    top1_accuracy: Number((value.top1 / value.masked_tokens).toFixed(6)),
    top5: value.top5,
    top5_accuracy: Number((value.top5 / value.masked_tokens).toFixed(6)),
    mrr: Number((value.mrr_sum / value.masked_tokens).toFixed(6)),
  }));
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
const directionClean = records.filter(
  (record) =>
    record.readiness === 'lipi_numeric_clean_candidate' ||
    record.readiness === 'lipi_direction_clean_candidate',
);

function groupBy(recordsForScope, field, groupKind, scope) {
  const map = new Map();
  for (const record of recordsForScope) {
    const value = record[field] || '-';
    if (!map.has(value)) map.set(value, []);
    map.get(value).push(record);
  }
  return [...map.entries()]
    .filter(([, grouped]) => grouped.length >= minGroupRows)
    .map(([value, grouped]) => ({
      scope,
      groupKind,
      groupValue: value,
      records: grouped,
    }));
}

function collapseRecords(recordsForScope) {
  const seen = new Map();
  for (const record of recordsForScope) {
    const key = record.tokens.join(' ');
    if (!seen.has(key)) {
      seen.set(key, { ...record, duplicate_weight: 1 });
    } else {
      seen.get(key).duplicate_weight++;
    }
  }
  return [...seen.values()];
}

function collapseGroup(group) {
  return {
    ...group,
    sourceRows: group.records.length,
    records: collapseRecords(group.records),
  };
}

function writeSequenceSummary(filePath, rowsForOutput, includeSourceRows = false) {
  fs.writeFileSync(
    filePath,
    toCsv([
      [
        'scope',
        'group_kind',
        'group_value',
        ...(includeSourceRows ? ['source_rows', 'duplicate_rows_removed'] : []),
        'rows',
        'tokens',
        'unique_signs',
        'exact_sequence_groups',
        'exact_duplicate_groups',
        'exact_duplicate_rows',
        'top_sequence_count',
        'rows_length_gt_1',
        'stored_higher_than_reversed',
        'reversed_higher_than_stored',
        'ties',
        'stored_higher_share',
        'mean_stored_minus_reversed',
        'median_stored_minus_reversed',
      ],
      ...rowsForOutput.map((row) => [
        row.scope,
        row.group_kind,
        row.group_value,
        ...(includeSourceRows ? [row.source_rows, row.duplicate_rows_removed] : []),
        row.rows,
        row.tokens,
        row.unique_signs,
        row.exact_sequence_groups,
        row.exact_duplicate_groups,
        row.exact_duplicate_rows,
        row.top_sequence_count,
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
}

function writeMaskedSummary(filePath, rowsForOutput, includeSourceRows = false) {
  fs.writeFileSync(
    filePath,
    toCsv([
      [
        'scope',
        'group_kind',
        'group_value',
        ...(includeSourceRows ? ['source_rows', 'duplicate_rows_removed'] : []),
        'rows',
        'model',
        'masked_tokens',
        'top1',
        'top1_accuracy',
        'top5',
        'top5_accuracy',
        'mrr',
      ],
      ...rowsForOutput.map((row) => [
        row.scope,
        row.group_kind,
        row.group_value,
        ...(includeSourceRows ? [row.source_rows, row.duplicate_rows_removed] : []),
        row.rows,
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
}

function writeHoldoutSummary(filePath, rowsForOutput, includeSourceRows = false) {
  fs.writeFileSync(
    filePath,
    toCsv([
      [
        'scope',
        'holdout_kind',
        'holdout_value',
        ...(includeSourceRows ? ['source_test_rows', 'duplicate_test_rows_removed'] : []),
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
      ...rowsForOutput.map((row) => [
        row.scope,
        row.holdout_kind,
        row.holdout_value,
        ...(includeSourceRows ? [row.source_test_rows, row.duplicate_test_rows_removed] : []),
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
}

function writeLeakageHoldoutSummary(filePath, rowsForOutput) {
  fs.writeFileSync(
    filePath,
    toCsv([
      [
        'scope',
        'holdout_kind',
        'holdout_value',
        'source_test_rows',
        'duplicate_test_rows_removed',
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
      ...rowsForOutput.map((row) => [
        row.scope,
        row.holdout_kind,
        row.holdout_value,
        row.source_test_rows,
        row.duplicate_test_rows_removed,
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
}

const sequenceGroups = [
  { scope: 'lipi_numeric_clean_candidate', groupKind: 'all', groupValue: 'all', records: numericClean },
  { scope: 'lipi_direction_clean_candidate_total', groupKind: 'all', groupValue: 'all', records: directionClean },
  ...groupBy(numericClean, 'type', 'type', 'lipi_numeric_clean_candidate'),
  ...groupBy(numericClean, 'site', 'site', 'lipi_numeric_clean_candidate'),
  ...groupBy(numericClean, 'region', 'region', 'lipi_numeric_clean_candidate'),
];

const maskedGroups = [
  { scope: 'lipi_numeric_clean_candidate', groupKind: 'all', groupValue: 'all', records: numericClean },
  ...groupBy(numericClean, 'type', 'type', 'lipi_numeric_clean_candidate'),
  ...groupBy(numericClean, 'site', 'site', 'lipi_numeric_clean_candidate'),
  ...groupBy(numericClean, 'region', 'region', 'lipi_numeric_clean_candidate'),
];

const sequenceSummary = sequenceGroups.map(evaluateSequence);
const maskedSummary = maskedGroups.flatMap(evaluateMasked);
const holdoutGroups = [
  ...groupBy(numericClean, 'type', 'type', 'lipi_numeric_clean_candidate_type_holdout'),
  ...groupBy(numericClean, 'site', 'site', 'lipi_numeric_clean_candidate_site_holdout'),
  ...groupBy(numericClean, 'region', 'region', 'lipi_numeric_clean_candidate_region_holdout'),
];
const holdoutSummary = holdoutGroups.flatMap((group) =>
  evaluateMaskedHoldout(
    group,
    numericClean.filter((record) => {
      if (group.groupKind === 'type') return record.type !== group.groupValue;
      if (group.groupKind === 'site') return record.site !== group.groupValue;
      if (group.groupKind === 'region') return record.region !== group.groupValue;
      return true;
    }),
  ),
);

function asDedupScope(scope) {
  return `${scope}_exact_sequence_collapsed`;
}

function markDedup(group) {
  const collapsed = collapseGroup(group);
  return {
    ...collapsed,
    scope: asDedupScope(group.scope),
  };
}

function addDedupGroupFields(row, group) {
  const sourceRows = group.sourceRows ?? group.records.length;
  return {
    ...row,
    source_rows: sourceRows,
    duplicate_rows_removed: sourceRows - group.records.length,
  };
}

function addDedupHoldoutFields(row, group) {
  const sourceRows = group.sourceRows ?? group.records.length;
  return {
    ...row,
    source_test_rows: sourceRows,
    duplicate_test_rows_removed: sourceRows - group.records.length,
  };
}

const dedupSequenceGroups = sequenceGroups.map(markDedup);
const dedupMaskedGroups = maskedGroups.map(markDedup);
const dedupHoldoutGroups = holdoutGroups.map(markDedup);

const dedupSequenceSummary = dedupSequenceGroups.map((group) =>
  addDedupGroupFields(evaluateSequence(group), group),
);
const dedupMaskedSummary = dedupMaskedGroups.flatMap((group) =>
  evaluateMasked(group).map((row) => addDedupGroupFields(row, group)),
);
const dedupHoldoutSummary = dedupHoldoutGroups.flatMap((group) => {
  const trainRecords = collapseRecords(
    numericClean.filter((record) => {
      if (group.groupKind === 'type') return record.type !== group.groupValue;
      if (group.groupKind === 'site') return record.site !== group.groupValue;
      if (group.groupKind === 'region') return record.region !== group.groupValue;
      return true;
    }),
  );
  return evaluateMaskedHoldout(group, trainRecords).map((row) => addDedupHoldoutFields(row, group));
});

const leakageControlHoldoutSummary = dedupHoldoutGroups.flatMap((group) => {
  const testSequences = new Set(group.records.map((record) => record.tokens.join(' ')));
  const trainRecordsBeforeLeakageFilter = collapseRecords(
    numericClean.filter((record) => {
      if (group.groupKind === 'type') return record.type !== group.groupValue;
      if (group.groupKind === 'site') return record.site !== group.groupValue;
      if (group.groupKind === 'region') return record.region !== group.groupValue;
      return true;
    }),
  );
  const trainRecords = trainRecordsBeforeLeakageFilter.filter(
    (record) => !testSequences.has(record.tokens.join(' ')),
  );
  return evaluateMaskedHoldout(group, trainRecords).map((row) => ({
    ...addDedupHoldoutFields(row, group),
    scope: `${row.scope}_leakage_controlled`,
    train_rows_before_leakage_filter: trainRecordsBeforeLeakageFilter.length,
    leakage_train_sequences_removed: trainRecordsBeforeLeakageFilter.length - trainRecords.length,
  }));
});

fs.writeFileSync(
  outSequence,
  toCsv([
    [
      'scope',
      'group_kind',
      'group_value',
      'rows',
      'tokens',
      'unique_signs',
      'exact_sequence_groups',
      'exact_duplicate_groups',
      'exact_duplicate_rows',
      'top_sequence_count',
      'rows_length_gt_1',
      'stored_higher_than_reversed',
      'reversed_higher_than_stored',
      'ties',
      'stored_higher_share',
      'mean_stored_minus_reversed',
      'median_stored_minus_reversed',
    ],
    ...sequenceSummary.map((row) => [
      row.scope,
      row.group_kind,
      row.group_value,
      row.rows,
      row.tokens,
      row.unique_signs,
      row.exact_sequence_groups,
      row.exact_duplicate_groups,
      row.exact_duplicate_rows,
      row.top_sequence_count,
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
      'scope',
      'group_kind',
      'group_value',
      'rows',
      'model',
      'masked_tokens',
      'top1',
      'top1_accuracy',
      'top5',
      'top5_accuracy',
      'mrr',
    ],
    ...maskedSummary.map((row) => [
      row.scope,
      row.group_kind,
      row.group_value,
      row.rows,
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
      'scope',
      'holdout_kind',
      'holdout_value',
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
      row.scope,
      row.holdout_kind,
      row.holdout_value,
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

fs.writeFileSync(
  outGroups,
  toCsv([
    ['scope', 'group_kind', 'group_value', 'rows', 'tokens', 'masked_evaluated'],
    ...sequenceGroups.map((group) => [
      group.scope,
      group.groupKind,
      group.groupValue,
      group.records.length,
      group.records.reduce((sum, record) => sum + record.tokens.length, 0),
      maskedGroups.some(
        (maskedGroup) =>
          maskedGroup.scope === group.scope &&
          maskedGroup.groupKind === group.groupKind &&
          maskedGroup.groupValue === group.groupValue,
      ),
    ]),
  ]),
  'utf8',
);

writeSequenceSummary(outDedupSequence, dedupSequenceSummary, true);
writeMaskedSummary(outDedupMasked, dedupMaskedSummary, true);
writeHoldoutSummary(outDedupHoldout, dedupHoldoutSummary, true);
writeLeakageHoldoutSummary(outLeakageHoldout, leakageControlHoldoutSummary);
fs.writeFileSync(
  outDedupGroups,
  toCsv([
    [
      'scope',
      'group_kind',
      'group_value',
      'source_rows',
      'collapsed_rows',
      'duplicate_rows_removed',
      'tokens',
      'masked_evaluated',
    ],
    ...dedupSequenceGroups.map((group) => [
      group.scope,
      group.groupKind,
      group.groupValue,
      group.sourceRows,
      group.records.length,
      group.sourceRows - group.records.length,
      group.records.reduce((sum, record) => sum + record.tokens.length, 0),
      dedupMaskedGroups.some(
        (maskedGroup) =>
          maskedGroup.scope === group.scope &&
          maskedGroup.groupKind === group.groupKind &&
          maskedGroup.groupValue === group.groupValue,
      ),
    ]),
  ]),
  'utf8',
);

const summary = {
  generated_at_local: formatLocalIso(new Date()),
  source_file: 'data/open_prototype/reports/lipi_scope_rows.csv',
  min_group_rows: minGroupRows,
  primary_scope: 'lipi_numeric_clean_candidate',
  sensitivity_scope: 'lipi_direction_clean_candidate_total',
  sequence_summary: sequenceSummary,
  masked_summary: maskedSummary,
  holdout_summary: holdoutSummary,
  artifact_files: [
    'data/open_prototype/reports/lipi_broad_order_sequence_summary.csv',
    'data/open_prototype/reports/lipi_broad_order_masked_summary.csv',
    'data/open_prototype/reports/lipi_broad_order_holdout_summary.csv',
    'data/open_prototype/reports/lipi_broad_order_group_inventory.csv',
    'data/open_prototype/reports/lipi_broad_order_summary.json',
  ],
  interpretation_boundary:
    'T3 claim-free broad-structure scout only; stored-order and masked-sign results are not sign values, semantics, phonetics, or translations.',
};

fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

const dedupSummary = {
  generated_at_local: formatLocalIso(new Date()),
  source_file: 'data/open_prototype/reports/lipi_scope_rows.csv',
  parent_baseline: 'data/open_prototype/reports/lipi_broad_order_summary.json',
  collapse_policy: 'Within each evaluated scope/split, exact duplicate numeric sign sequences are collapsed to one representative row.',
  min_group_rows_source_weighted: minGroupRows,
  primary_scope: 'lipi_numeric_clean_candidate_exact_sequence_collapsed',
  sensitivity_scope: 'lipi_direction_clean_candidate_total_exact_sequence_collapsed',
  sequence_summary: dedupSequenceSummary,
  masked_summary: dedupMaskedSummary,
  holdout_summary: dedupHoldoutSummary,
  artifact_files: [
    'data/open_prototype/reports/lipi_dedup_order_sequence_summary.csv',
    'data/open_prototype/reports/lipi_dedup_order_masked_summary.csv',
    'data/open_prototype/reports/lipi_dedup_order_holdout_summary.csv',
    'data/open_prototype/reports/lipi_dedup_order_group_inventory.csv',
    'data/open_prototype/reports/lipi_dedup_order_summary.json',
  ],
  interpretation_boundary:
    'Exact-duplicate-collapsed T3 structural scout only; stored-order and masked-sign results are not sign values, semantics, phonetics, or translations.',
};

fs.writeFileSync(outDedupJson, `${JSON.stringify(dedupSummary, null, 2)}\n`, 'utf8');

const leakageControlSummary = {
  generated_at_local: formatLocalIso(new Date()),
  source_file: 'data/open_prototype/reports/lipi_scope_rows.csv',
  parent_baseline: 'data/open_prototype/reports/lipi_dedup_order_summary.json',
  leakage_policy:
    'For each exact-duplicate-collapsed held-out split, remove from the training set any exact numeric sign sequence that appears in the held-out test split.',
  min_group_rows_source_weighted: minGroupRows,
  holdout_summary: leakageControlHoldoutSummary,
  artifact_files: [
    'data/open_prototype/reports/lipi_leakage_control_holdout_summary.csv',
    'data/open_prototype/reports/lipi_leakage_control_summary.json',
  ],
  interpretation_boundary:
    'Leakage-controlled T3 structural scout only; held-out masked-sign results are not sign values, semantics, phonetics, or translations.',
};

fs.writeFileSync(outLeakageJson, `${JSON.stringify(leakageControlSummary, null, 2)}\n`, 'utf8');

console.log(
  JSON.stringify(
    {
      sequence_groups: sequenceSummary.length,
      masked_rows: maskedSummary.length,
      holdout_rows: holdoutSummary.length,
      dedup_sequence_groups: dedupSequenceSummary.length,
      dedup_masked_rows: dedupMaskedSummary.length,
      dedup_holdout_rows: dedupHoldoutSummary.length,
      leakage_control_holdout_rows: leakageControlHoldoutSummary.length,
      primary_all_sequence: sequenceSummary.find(
        (row) => row.scope === 'lipi_numeric_clean_candidate' && row.group_kind === 'all',
      ),
      primary_all_masked: maskedSummary.filter(
        (row) => row.scope === 'lipi_numeric_clean_candidate' && row.group_kind === 'all',
      ),
      dedup_primary_all_sequence: dedupSequenceSummary.find(
        (row) =>
          row.scope === 'lipi_numeric_clean_candidate_exact_sequence_collapsed' &&
          row.group_kind === 'all',
      ),
      dedup_primary_all_masked: dedupMaskedSummary.filter(
        (row) =>
          row.scope === 'lipi_numeric_clean_candidate_exact_sequence_collapsed' &&
          row.group_kind === 'all',
      ),
      wrote: [...summary.artifact_files, ...dedupSummary.artifact_files, ...leakageControlSummary.artifact_files],
    },
    null,
    2,
  ),
);
