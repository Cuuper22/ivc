import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const sourcePath = path.join(reportsDir, 'lipi_scope_rows.csv');
const outIterations = path.join(reportsDir, 'lipi_structured_null_iterations.csv');
const outSummary = path.join(reportsDir, 'lipi_structured_null_summary.csv');
const outJson = path.join(reportsDir, 'lipi_structured_null_summary.json');

const iterations = Number(process.env.IVC_STRUCTURED_NULL_ITERATIONS ?? 5);
const seedBase = 20260524;
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

function quantile(values, q) {
  if (!values.length) return null;
  const sorted = values.slice().sort((a, b) => a - b);
  const index = (sorted.length - 1) * q;
  const lower = Math.floor(index);
  const upper = Math.ceil(index);
  if (lower === upper) return sorted[lower];
  return sorted[lower] + (sorted[upper] - sorted[lower]) * (index - lower);
}

function formatNumber(value) {
  return value === null || value === undefined || Number.isNaN(value) ? null : Number(value.toFixed(6));
}

function mulberry32(seed) {
  return function random() {
    let t = (seed += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function hashString(text) {
  let hash = 2166136261;
  for (let i = 0; i < text.length; i++) {
    hash ^= text.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}

function topCountMap(counts, limit) {
  const out = new Map();
  for (const [token, count] of [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, limit)) {
    out.set(token, count);
  }
  return out.size ? out : counts;
}

function weightedChoice(counts, rng) {
  const entries = [...counts.entries()];
  const total = entries.reduce((sum, [, count]) => sum + count, 0);
  if (total <= 0) throw new Error('Cannot sample from an empty count map.');
  let target = rng() * total;
  for (const [token, count] of entries) {
    target -= count;
    if (target <= 0) return token;
  }
  return entries[entries.length - 1][0];
}

function choice(values, rng) {
  return values[Math.floor(rng() * values.length)];
}

function makeUniqueTemplate(tokens, family, usedKeys, pools, rng) {
  let candidate = tokens.slice();
  let key = candidate.join(' ');
  if (!usedKeys.has(key)) {
    usedKeys.add(key);
    return candidate;
  }

  for (let attempt = 0; attempt < 300; attempt++) {
    candidate = tokens.slice();
    const len = candidate.length;
    if (len === 0) return candidate;
    const mutablePos = len <= 2 ? attempt % len : 1 + (attempt % (len - 2));
    candidate[mutablePos] = sampleLengthPosition(pools, len, mutablePos, rng);
    key = candidate.join(' ');
    if (!usedKeys.has(key)) {
      usedKeys.add(key);
      return candidate;
    }
  }

  for (let attempt = 0; attempt < 300; attempt++) {
    candidate = tokens.map((token, pos) => (pos === 0 && tokens.length > 1 ? token : sampleLengthPosition(pools, tokens.length, pos, rng)));
    key = candidate.join(' ');
    if (!usedKeys.has(key)) {
      usedKeys.add(key);
      return candidate;
    }
  }

  usedKeys.add(key);
  return candidate;
}

function makeRepeatedRecords(families, control, iteration, templateFn, pools, rng) {
  const records = [];
  const usedKeys = new Set();
  for (const family of families) {
    const tokens = makeUniqueTemplate(templateFn(family), family, usedKeys, pools, rng);
    for (let copy = 0; copy < family.duplicate_weight; copy++) {
      records.push({
        ...family,
        id: `${control}_${iteration}_${family.id}_${copy + 1}`,
        source_id: family.id,
        control,
        iteration,
        tokens,
      });
    }
  }
  return records;
}

function exactCollapse(records) {
  const seen = new Map();
  for (const record of records) {
    const key = record.tokens.join(' ');
    if (!seen.has(key)) {
      seen.set(key, { ...record, duplicate_weight: record.duplicate_weight ?? 1 });
    } else {
      seen.get(key).duplicate_weight += record.duplicate_weight ?? 1;
    }
  }
  return [...seen.values()];
}

function duplicateStats(records) {
  const sequenceCounts = new Map();
  for (const record of records) bump(sequenceCounts, record.tokens.join(' '));
  const duplicateGroups = [...sequenceCounts.values()].filter((count) => count > 1);
  return {
    source_rows: records.length,
    source_tokens: records.reduce((sum, record) => sum + record.tokens.length, 0),
    unique_sequences: sequenceCounts.size,
    exact_duplicate_groups: duplicateGroups.length,
    exact_duplicate_rows: duplicateGroups.reduce((sum, count) => sum + count, 0),
    exact_duplicate_row_share:
      records.length > 0 ? formatNumber(duplicateGroups.reduce((sum, count) => sum + count, 0) / records.length) : null,
    top_sequence_count: sequenceCounts.size ? Math.max(...sequenceCounts.values()) : 0,
  };
}

function buildPools(records) {
  const global = new Map();
  const first = new Map();
  const last = new Map();
  const interior = new Map();
  const byPosition = new Map();
  const byLengthPosition = new Map();
  for (const record of records) {
    const len = record.tokens.length;
    for (let pos = 0; pos < len; pos++) {
      const token = record.tokens[pos];
      bump(global, token);
      addKeyedCount(byPosition, [pos], token);
      addKeyedCount(byLengthPosition, [len, pos], token);
      if (pos === 0) bump(first, token);
      if (pos === len - 1) bump(last, token);
      if (pos > 0 && pos < len - 1) bump(interior, token);
    }
  }
  return {
    global,
    first,
    last,
    interior: interior.size ? interior : global,
    byPosition,
    byLengthPosition,
    firstTop: topCountMap(first, 120),
    lastTop: topCountMap(last, 120),
    interiorTop: topCountMap(interior.size ? interior : global, 180),
    globalTop: topCountMap(global, 220),
  };
}

function sampleLengthPosition(pools, len, pos, rng) {
  return weightedChoice(
    pools.byLengthPosition.get(`${len}\t${pos}`) ?? pools.byPosition.get(String(pos)) ?? pools.global,
    rng,
  );
}

function dependencyChoice(seedKey, options, limit) {
  const entries = [...options.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, limit);
  if (!entries.length) throw new Error(`No dependency options for ${seedKey}`);
  return entries[hashString(seedKey) % entries.length][0];
}

function makeAdminTemplateFactory(pools, rng) {
  const officeChoices = new Map();
  const commodityChoices = new Map();
  const quantityChoices = new Map();
  const qualifierChoices = new Map();
  const terminalChoices = new Map();

  function getChoice(map, key, options, limit, salt) {
    if (!map.has(key)) map.set(key, dependencyChoice(`${salt}:${key}`, options, limit));
    return map.get(key);
  }

  return function adminTemplate(family) {
    const len = family.tokens.length;
    if (len <= 0) return [];
    const issuer = weightedChoice(pools.firstTop, rng);
    if (len === 1) return [issuer];
    const office = getChoice(officeChoices, issuer, pools.interiorTop, 60, 'office');
    const commodity = getChoice(commodityChoices, office, pools.interiorTop, 90, 'commodity');
    const quantity = getChoice(quantityChoices, commodity, pools.interiorTop, 70, 'quantity');
    const qualifier = getChoice(qualifierChoices, `${issuer}:${commodity}`, pools.globalTop, 120, 'qualifier');
    const terminal = getChoice(terminalChoices, `${issuer}:${quantity}`, pools.lastTop, 90, 'terminal');
    if (len === 2) return [issuer, terminal];
    if (len === 3) return [issuer, commodity, terminal];
    if (len === 4) return [issuer, commodity, quantity, terminal];
    const tokens = [issuer, office, commodity, quantity];
    while (tokens.length < len - 1) tokens.push(qualifier);
    tokens.push(terminal);
    return tokens.slice(0, len);
  };
}

function makeEmblemTemplateFactory(pools, rng) {
  const rankChoices = new Map();
  const deviceChoices = new Map();
  const variantChoices = new Map();
  const terminalChoices = new Map();

  function getChoice(map, key, options, limit, salt) {
    if (!map.has(key)) map.set(key, dependencyChoice(`${salt}:${key}`, options, limit));
    return map.get(key);
  }

  return function emblemTemplate(family) {
    const len = family.tokens.length;
    if (len <= 0) return [];
    const clan = weightedChoice(pools.firstTop, rng);
    if (len === 1) return [clan];
    const rank = getChoice(rankChoices, clan, pools.interiorTop, 80, 'rank');
    const device = getChoice(deviceChoices, `${clan}:${rank}`, pools.interiorTop, 100, 'device');
    const variant = getChoice(variantChoices, device, pools.globalTop, 120, 'variant');
    const terminal = getChoice(terminalChoices, `${clan}:${device}`, pools.lastTop, 100, 'terminal');
    if (len === 2) return [clan, terminal];
    if (len === 3) return [clan, device, terminal];
    if (len === 4) return [clan, rank, device, terminal];
    const tokens = [clan, rank, device];
    while (tokens.length < len - 1) tokens.push(variant);
    tokens.push(terminal);
    return tokens.slice(0, len);
  };
}

function makePositionDuplicateTemplateFactory(pools, rng) {
  return function positionTemplate(family) {
    return family.tokens.map((_, pos) => sampleLengthPosition(pools, family.tokens.length, pos, rng));
  };
}

function makeMixedTemplateFactory(pools, rng) {
  const admin = makeAdminTemplateFactory(pools, rng);
  const emblem = makeEmblemTemplateFactory(pools, rng);
  const position = makePositionDuplicateTemplateFactory(pools, rng);
  return function mixedTemplate(family) {
    const type = family.type || '';
    if (type.startsWith('TAB')) return admin(family);
    if (type.startsWith('SEAL')) return emblem(family);
    if (type.startsWith('POT') && family.tokens.length <= 3) return position(family);
    return rng() < 0.5 ? admin(family) : emblem(family);
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

function rowTransitionCounts(tokens) {
  return transitionCounts([{ tokens }]);
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
    const train = subtractTransitionCounts(globalTransitions, rowTransitionCounts(record.tokens));
    const storedScore = transitionScore(record.tokens, train, vocabSize);
    const reversedScore = transitionScore(record.tokens.slice().reverse(), train, vocabSize);
    const diff = storedScore - reversedScore;
    diffs.push(diff);
    if (diff > epsilon) storedHigher++;
    else if (diff < -epsilon) reversedHigher++;
    else ties++;
  }
  return {
    collapsed_rows: usable.length,
    collapsed_tokens: usable.reduce((sum, record) => sum + record.tokens.length, 0),
    unique_signs: vocab.length,
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

function subtractTokenCounts(globalCounts, rowCounts) {
  const out = new Map(globalCounts);
  for (const [token, value] of rowCounts.entries()) {
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
      if (better >= 5) break;
    }
  }
  const rank = better + 1;
  return {
    top1: rank === 1,
    top5: rank <= 5,
  };
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
  const usable = records.filter((record) => record.tokens.length > 0);
  const globalCounts = buildGroupCounts(usable);
  const vocab = [...globalCounts.tokenCounts.keys()].sort((a, b) => a.localeCompare(b));
  const models = {
    frequency: { masked_tokens: 0, top1: 0, top5: 0 },
    position: { masked_tokens: 0, top1: 0, top5: 0 },
    length_position: { masked_tokens: 0, top1: 0, top5: 0 },
    bidirectional_bigram: { masked_tokens: 0, top1: 0, top5: 0 },
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
      }
    }
  }
  return Object.fromEntries(
    Object.entries(models).map(([model, row]) => [
      model,
      {
        masked_tokens: row.masked_tokens,
        top1_accuracy: row.masked_tokens > 0 ? formatNumber(row.top1 / row.masked_tokens) : null,
        top5_accuracy: row.masked_tokens > 0 ? formatNumber(row.top5 / row.masked_tokens) : null,
      },
    ]),
  );
}

function evaluateDataset(control, iteration, records) {
  const duplicate = duplicateStats(records);
  const collapsed = exactCollapse(records);
  const sequence = evaluateSequence(collapsed);
  const masked = evaluateMasked(collapsed);
  return {
    control,
    iteration,
    ...duplicate,
    ...sequence,
    frequency_top1_accuracy: masked.frequency.top1_accuracy,
    frequency_top5_accuracy: masked.frequency.top5_accuracy,
    position_top1_accuracy: masked.position.top1_accuracy,
    position_top5_accuracy: masked.position.top5_accuracy,
    length_position_top1_accuracy: masked.length_position.top1_accuracy,
    length_position_top5_accuracy: masked.length_position.top5_accuracy,
    bidirectional_top1_accuracy: masked.bidirectional_bigram.top1_accuracy,
    bidirectional_top5_accuracy: masked.bidirectional_bigram.top5_accuracy,
  };
}

function summarizeMetric(control, metric, values, observed) {
  const mean = values.reduce((sum, value) => sum + value, 0) / values.length;
  const variance = values.reduce((sum, value) => sum + (value - mean) ** 2, 0) / values.length;
  return {
    control,
    metric,
    iterations: values.length,
    observed_value: observed,
    null_mean: formatNumber(mean),
    null_sd: formatNumber(Math.sqrt(variance)),
    null_min: formatNumber(Math.min(...values)),
    null_p05: formatNumber(quantile(values, 0.05)),
    null_median: formatNumber(median(values)),
    null_p95: formatNumber(quantile(values, 0.95)),
    null_max: formatNumber(Math.max(...values)),
    observed_minus_null_mean: formatNumber(observed - mean),
    null_ge_observed_share: formatNumber(values.filter((value) => value >= observed).length / values.length),
    null_le_observed_share: formatNumber(values.filter((value) => value <= observed).length / values.length),
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
const observedFamilies = exactCollapse(numericClean).sort((a, b) => String(a.id).localeCompare(String(b.id)));
const pools = buildPools(numericClean);
const iterationRows = [evaluateDataset('observed_lipi_numeric_clean_candidate', 'observed', numericClean)];

const controls = [
  {
    name: 'duplicate_matched_position_slots',
    description:
      'Matches the observed duplicate-weight and length distribution, but samples every slot independently from observed length-position pools.',
    makeFactory: makePositionDuplicateTemplateFactory,
  },
  {
    name: 'administrative_register_code',
    description:
      'Duplicate-matched administrative slot code with issuer, office, commodity, quantity, qualifier, and terminal dependencies.',
    makeFactory: makeAdminTemplateFactory,
  },
  {
    name: 'emblem_formula_code',
    description:
      'Duplicate-matched emblem formula code with clan, rank, device, variant, and terminal dependencies.',
    makeFactory: makeEmblemTemplateFactory,
  },
  {
    name: 'mixed_admin_emblem_code',
    description:
      'Duplicate-matched mixed code: tablet-like rows use administrative dependencies, seal-like rows use emblem dependencies, and short pottery rows use positional slots.',
    makeFactory: makeMixedTemplateFactory,
  },
];

for (const control of controls) {
  for (let iteration = 1; iteration <= iterations; iteration++) {
    const rng = mulberry32(seedBase + iteration * 1009 + control.name.length * 65537);
    const templateFactory = control.makeFactory(pools, rng);
    const generated = makeRepeatedRecords(observedFamilies, control.name, iteration, templateFactory, pools, rng);
    iterationRows.push(evaluateDataset(control.name, iteration, generated));
  }
}

const metricNames = [
  'unique_sequences',
  'exact_duplicate_groups',
  'exact_duplicate_rows',
  'exact_duplicate_row_share',
  'top_sequence_count',
  'collapsed_rows',
  'collapsed_tokens',
  'stored_higher_share',
  'mean_stored_minus_reversed',
  'median_stored_minus_reversed',
  'frequency_top1_accuracy',
  'position_top1_accuracy',
  'length_position_top1_accuracy',
  'bidirectional_top1_accuracy',
  'bidirectional_top5_accuracy',
];

const observedRow = iterationRows[0];
const summaryRows = [];
for (const control of controls) {
  const controlRows = iterationRows.filter((row) => row.control === control.name);
  for (const metric of metricNames) {
    summaryRows.push(summarizeMetric(control.name, metric, controlRows.map((row) => row[metric]), observedRow[metric]));
  }
}

const iterationHeader = [
  'control',
  'iteration',
  'source_rows',
  'source_tokens',
  'unique_sequences',
  'exact_duplicate_groups',
  'exact_duplicate_rows',
  'exact_duplicate_row_share',
  'top_sequence_count',
  'collapsed_rows',
  'collapsed_tokens',
  'unique_signs',
  'rows_length_gt_1',
  'stored_higher_than_reversed',
  'reversed_higher_than_stored',
  'ties',
  'stored_higher_share',
  'mean_stored_minus_reversed',
  'median_stored_minus_reversed',
  'frequency_top1_accuracy',
  'frequency_top5_accuracy',
  'position_top1_accuracy',
  'position_top5_accuracy',
  'length_position_top1_accuracy',
  'length_position_top5_accuracy',
  'bidirectional_top1_accuracy',
  'bidirectional_top5_accuracy',
];

fs.writeFileSync(
  outIterations,
  toCsv([iterationHeader, ...iterationRows.map((row) => iterationHeader.map((key) => row[key]))]),
  'utf8',
);

const summaryHeader = [
  'control',
  'metric',
  'iterations',
  'observed_value',
  'null_mean',
  'null_sd',
  'null_min',
  'null_p05',
  'null_median',
  'null_p95',
  'null_max',
  'observed_minus_null_mean',
  'null_ge_observed_share',
  'null_le_observed_share',
];

fs.writeFileSync(
  outSummary,
  toCsv([summaryHeader, ...summaryRows.map((row) => summaryHeader.map((key) => row[key]))]),
  'utf8',
);

const summary = {
  generated_at_local: formatLocalIso(new Date()),
  source_file: 'data/open_prototype/reports/lipi_scope_rows.csv',
  source_scope: 'lipi_numeric_clean_candidate',
  source_rows: numericClean.length,
  observed_exact_collapsed_families: observedFamilies.length,
  iterations_per_control: iterations,
  seed_base: seedBase,
  controls: controls.map(({ name, description }) => ({ name, description })),
  observed: observedRow,
  null_summary: summaryRows,
  artifact_files: [
    'data/open_prototype/reports/lipi_structured_null_iterations.csv',
    'data/open_prototype/reports/lipi_structured_null_summary.csv',
    'data/open_prototype/reports/lipi_structured_null_summary.json',
  ],
  interpretation_boundary:
    'Structured nonlinguistic comparator scout only. Matching or exceeding a metric weakens that metric as decipherment evidence; failing to match a metric does not create meanings, sign values, language identity, or translations.',
};

fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(
  JSON.stringify(
    {
      observed: observedRow,
      summary_rows: summaryRows.length,
      iteration_rows: iterationRows.length,
      selected_bidirectional_top1: summaryRows.filter((row) => row.metric === 'bidirectional_top1_accuracy'),
      selected_stored_order: summaryRows.filter((row) => row.metric === 'stored_higher_share'),
      wrote: summary.artifact_files,
    },
    null,
    2,
  ),
);
