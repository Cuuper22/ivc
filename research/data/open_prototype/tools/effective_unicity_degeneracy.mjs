// Measures how much the corpus itself pins down each sign — "effective unicity" — and how
// much stays degenerate: interchangeable under relabeling. Two complementary measurements.
// First, label symmetry: signs whose full context profiles (counts, positions, neighbors)
// are identical could swap labels with no observable difference; we count those equivalence
// classes and their log2(n!) bits of residual freedom. Second, a masked-sign test: hide one
// sign at a time and ask a leave-one-row-out predictor (unigram + length-position + left and
// right neighbor scores, softmax-combined) to guess it, reporting top-1/top-5 accuracy,
// entropy, and the effective number of candidates. Both are traced across coverage
// fractions (10% to 100% of the exact-deduplicated clean Lipi rows from lipi_scope_rows.csv)
// and compared to six seeded forgeries — token shuffles, position-slot nulls, an
// edge-preserving shuffle, a register-blocked null, and a deliberately nonlinguistic
// administrative template — to see which metrics real structure beats. CLI positional args:
// iterations per control (default 100), seed (default 20260529), masked-sample limit for
// nulls (default 1200). The summary states the hard boundary: no external anchor means no
// phonetic values and no language ID, only structural constraint. Writes curve, null
// iteration, and null summary CSVs plus a JSON summary to data/open_prototype/reports.
import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const sourcePath = path.join(reportsDir, 'lipi_scope_rows.csv');
const outCurve = path.join(reportsDir, 'effective_unicity_degeneracy_curve.csv');
const outNullIterations = path.join(reportsDir, 'effective_unicity_degeneracy_null_iterations.csv');
const outNullSummary = path.join(reportsDir, 'effective_unicity_degeneracy_null_summary.csv');
const outJson = path.join(reportsDir, 'effective_unicity_degeneracy_summary.json');

const iterationsPerControl = Number(process.argv[2] ?? 100);
const seedBase = Number(process.argv[3] ?? 20260529);
const nullMaskedSampleLimit = Number(process.argv[4] ?? 1200);
const coverageFractions = [0.1, 0.2, 0.3, 0.4, 0.5, 0.625, 0.75, 0.875, 1.0];
const nullCoverageFractions = [0.25, 0.5, 0.75, 1.0];
const smoothing = 0.5;
const epsilon = 1e-12;

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

function sampleFrom(items, rng) {
  return items[Math.floor(rng() * items.length)];
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
  for (const [key, inner] of baseMap.entries()) out.set(key, new Map(inner));
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

function nestedCount(nested, key, token) {
  return nested.get(key)?.get(token) ?? 0;
}

function nestedTotals(nested) {
  return new Map([...nested.entries()].map(([key, inner]) => [key, mapTotal(inner)]));
}

function log2Factorial(n) {
  let total = 0;
  for (let i = 2; i <= n; i++) total += Math.log2(i);
  return total;
}

function round(value, places = 6) {
  if (value === null || value === undefined || !Number.isFinite(value)) return null;
  return Number(value.toFixed(places));
}

function percentile(sortedValues, p) {
  if (!sortedValues.length) return null;
  const idx = (sortedValues.length - 1) * p;
  const lo = Math.floor(idx);
  const hi = Math.ceil(idx);
  if (lo === hi) return sortedValues[lo];
  return sortedValues[lo] + (sortedValues[hi] - sortedValues[lo]) * (idx - lo);
}

function makeRecord(row, column) {
  const tokens = parseTokens(row[column.text]);
  return {
    id: row[column.id],
    cisi: row[column.cisi],
    region: row[column.region],
    site: row[column.site],
    type: row[column.type],
    material: row[column.material],
    direction: row[column.direction],
    readiness: row[column.readiness_bucket],
    text: row[column.text],
    tokens,
  };
}

function collapseExactSequences(records) {
  const seen = new Map();
  for (const record of records) {
    const key = record.tokens.join(' ');
    if (!seen.has(key)) {
      seen.set(key, {
        ...record,
        duplicate_weight: 1,
        source_ids: [record.id],
        source_cisi: [record.cisi],
      });
    } else {
      const existing = seen.get(key);
      existing.duplicate_weight++;
      existing.source_ids.push(record.id);
      existing.source_cisi.push(record.cisi);
    }
  }
  return [...seen.values()];
}

function countDistinctBy(records, keyFn) {
  return new Set(records.map(keyFn)).size;
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

function countArray(values) {
  const map = new Map();
  for (const value of values) bump(map, value);
  return [...map.entries()].sort((a, b) => a[0].localeCompare(b[0]));
}

function buildSignProfiles(records) {
  const profiles = new Map();
  const ensure = (token) => {
    if (!profiles.has(token)) {
      profiles.set(token, {
        count: 0,
        initials: 0,
        terminals: 0,
        lengthPositions: [],
        left: [],
        right: [],
        rowLengths: [],
      });
    }
    return profiles.get(token);
  };

  for (const record of records) {
    const len = record.tokens.length;
    for (let i = 0; i < len; i++) {
      const token = record.tokens[i];
      const profile = ensure(token);
      profile.count++;
      if (i === 0) profile.initials++;
      if (i === len - 1) profile.terminals++;
      profile.lengthPositions.push(`${len}:${i}`);
      profile.left.push(i === 0 ? '<s>' : record.tokens[i - 1]);
      profile.right.push(i === len - 1 ? '</s>' : record.tokens[i + 1]);
      profile.rowLengths.push(String(len));
    }
  }

  const signatures = new Map();
  for (const [token, profile] of profiles.entries()) {
    const signature = JSON.stringify({
      count: profile.count,
      initials: profile.initials,
      terminals: profile.terminals,
      lengthPositions: countArray(profile.lengthPositions),
      left: countArray(profile.left),
      right: countArray(profile.right),
      rowLengths: countArray(profile.rowLengths),
    });
    if (!signatures.has(signature)) signatures.set(signature, []);
    signatures.get(signature).push(token);
  }
  const groups = [...signatures.values()].map((tokens) => tokens.sort((a, b) => a.localeCompare(b)));
  groups.sort((a, b) => b.length - a.length || a[0].localeCompare(b[0]));
  const equivalentGroups = groups.filter((tokens) => tokens.length > 1);
  const equivalentSigns = equivalentGroups.reduce((sum, tokens) => sum + tokens.length, 0);
  return {
    profileGroups: groups,
    equivalentGroups,
    contextEquivLog2Bits: groups.reduce((sum, tokens) => sum + log2Factorial(tokens.length), 0),
    profileSingletonShare: profiles.size ? (profiles.size - equivalentSigns) / profiles.size : null,
    largestContextEquivClass: groups[0]?.length ?? 0,
    contextEquivClassCount: equivalentGroups.length,
    equivalentSigns,
    examples: equivalentGroups.slice(0, 6).map((tokens) => tokens.join(' ')),
  };
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

function scoreMasked(records, options) {
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
        nestedCount(globalCounts.leftCounts, left, candidate) -
          nestedCount(rowCounts.leftCounts, left, candidate),
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
    top1_accuracy: totals.top1 / n,
    top5_accuracy: totals.top5 / n,
    mean_rank: totals.rank_sum / n,
    mrr: totals.reciprocal_rank_sum / n,
    mean_true_probability: totals.true_prob_sum / n,
    mean_entropy_bits: totals.entropy_bits_sum / n,
    mean_effective_candidates: totals.effective_candidate_sum / n,
    mean_mass90_candidates: totals.mass90_sum / n,
  };
}

function analyzeRecords(records, options = {}) {
  const rows = records.length;
  const tokens = records.reduce((sum, record) => sum + record.tokens.length, 0);
  const vocab = [...new Set(records.flatMap((record) => record.tokens))].sort((a, b) => a.localeCompare(b));
  const profiles = buildSignProfiles(records);
  const masked = scoreMasked(records, options);
  return {
    rows,
    tokens,
    unique_signs: vocab.length,
    label_symmetry_log2_bits: log2Factorial(vocab.length),
    context_equiv_log2_bits: profiles.contextEquivLog2Bits,
    context_equiv_class_count: profiles.contextEquivClassCount,
    context_equiv_signs: profiles.equivalentSigns,
    largest_context_equiv_class: profiles.largestContextEquivClass,
    profile_singleton_share: profiles.profileSingletonShare,
    masked_tokens: masked.masked_tokens,
    masked_sampled: masked.masked_sampled,
    masked_top1_accuracy: masked.top1_accuracy,
    masked_top5_accuracy: masked.top5_accuracy,
    masked_mean_rank: masked.mean_rank,
    masked_mrr: masked.mrr,
    masked_mean_true_probability: masked.mean_true_probability,
    masked_mean_entropy_bits: masked.mean_entropy_bits,
    masked_mean_effective_candidates: masked.mean_effective_candidates,
    masked_mean_mass90_candidates: masked.mean_mass90_candidates,
    context_equiv_examples: profiles.examples,
  };
}

function buildPositionPools(records) {
  const all = [];
  const lengthPosition = new Map();
  const first = [];
  const medial = [];
  const terminal = [];
  for (const record of records) {
    const len = record.tokens.length;
    for (let i = 0; i < len; i++) {
      const token = record.tokens[i];
      all.push(token);
      const key = `${len}:${i}`;
      if (!lengthPosition.has(key)) lengthPosition.set(key, []);
      lengthPosition.get(key).push(token);
      if (i === 0) first.push(token);
      else if (i === len - 1) terminal.push(token);
      else medial.push(token);
    }
  }
  return { all, lengthPosition, first, medial, terminal };
}

function forgerGlobalTokenShuffle(records, rng) {
  const tokens = shuffle(records.flatMap((record) => record.tokens), rng);
  let offset = 0;
  return records.map((record, index) => {
    const next = tokens.slice(offset, offset + record.tokens.length);
    offset += record.tokens.length;
    return {
      ...record,
      id: `global_token_shuffle:${index}`,
      cisi: `forger:${index}`,
      tokens: next,
      text: `+${next.join('-')}+`,
    };
  });
}

function forgerRowInternalShuffle(records, rng) {
  return records.map((record, index) => {
    const next = shuffle(record.tokens, rng);
    return {
      ...record,
      id: `row_internal_shuffle:${index}`,
      cisi: `forger:${index}`,
      tokens: next,
      text: `+${next.join('-')}+`,
    };
  });
}

function forgerPositionSlotShuffle(records, rng) {
  const pools = buildPositionPools(records);
  return records.map((record, index) => {
    const next = record.tokens.map((_, i) => {
      const pool = pools.lengthPosition.get(`${record.tokens.length}:${i}`) ?? pools.all;
      return sampleFrom(pool, rng);
    });
    return {
      ...record,
      id: `position_slot_shuffle:${index}`,
      cisi: `forger:${index}`,
      tokens: next,
      text: `+${next.join('-')}+`,
    };
  });
}

function forgerEdgeFrameShuffle(records, rng) {
  return records.map((record, index) => {
    let next;
    if (record.tokens.length <= 2) {
      next = record.tokens.slice();
    } else {
      next = [
        record.tokens[0],
        ...shuffle(record.tokens.slice(1, -1), rng),
        record.tokens[record.tokens.length - 1],
      ];
    }
    return {
      ...record,
      id: `edge_frame_shuffle:${index}`,
      cisi: `forger:${index}`,
      tokens: next,
      text: `+${next.join('-')}+`,
    };
  });
}

function forgerRegisterBlockedPositionShuffle(records, rng) {
  const globalPools = buildPositionPools(records);
  const blockPools = new Map();
  for (const record of records) {
    const block = `${record.site || '-'}\t${record.type || '-'}\t${record.material || '-'}`;
    if (!blockPools.has(block)) blockPools.set(block, []);
    blockPools.get(block).push(record);
  }
  const poolsByBlock = new Map(
    [...blockPools.entries()].map(([block, blockRecords]) => [block, buildPositionPools(blockRecords)]),
  );
  return records.map((record, index) => {
    const block = `${record.site || '-'}\t${record.type || '-'}\t${record.material || '-'}`;
    const pools = poolsByBlock.get(block) ?? globalPools;
    const next = record.tokens.map((_, i) => {
      const blockPool = pools.lengthPosition.get(`${record.tokens.length}:${i}`);
      const globalPool = globalPools.lengthPosition.get(`${record.tokens.length}:${i}`) ?? globalPools.all;
      const pool = blockPool && blockPool.length >= 3 ? blockPool : globalPool;
      return sampleFrom(pool, rng);
    });
    return {
      ...record,
      id: `register_blocked_position_shuffle:${index}`,
      cisi: `forger:${index}`,
      tokens: next,
      text: `+${next.join('-')}+`,
    };
  });
}

function topTokens(tokens, n) {
  const counts = new Map();
  for (const token of tokens) bump(counts, token);
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, n)
    .map(([token]) => token);
}

function forgerTemplateAdminCode(records, rng) {
  const pools = buildPositionPools(records);
  const authorityPool = topTokens(pools.first.length ? pools.first : pools.all, 48);
  const officePool = topTokens(pools.medial.length ? pools.medial : pools.all, 64);
  const commodityPool = topTokens(pools.medial.length ? pools.medial : pools.all, 80);
  const terminalPool = topTokens(pools.terminal.length ? pools.terminal : pools.all, 48);
  const qualifierPool = topTokens(pools.all, 96);
  const registers = ['seal', 'tablet', 'tag', 'pot', 'other'];
  const terminalByCommodity = new Map();
  for (const commodity of commodityPool) terminalByCommodity.set(commodity, sampleFrom(terminalPool, rng));

  return records.map((record, index) => {
    const len = record.tokens.length;
    const register = sampleFrom(registers, rng);
    const authority = sampleFrom(authorityPool, rng);
    const office = sampleFrom(officePool, rng);
    const commodity = sampleFrom(commodityPool, rng);
    const terminal = terminalByCommodity.get(commodity) ?? sampleFrom(terminalPool, rng);
    const qualifier = sampleFrom(qualifierPool, rng);
    let next;
    if (len === 1) {
      next = [terminal];
    } else if (len === 2) {
      next = register === 'pot' ? [commodity, terminal] : [authority, terminal];
    } else if (len === 3) {
      next = [authority, commodity, terminal];
    } else if (len === 4) {
      next = [authority, office, commodity, terminal];
    } else {
      next = [authority, office, commodity];
      while (next.length < len - 1) next.push(sampleFrom(qualifierPool, rng));
      next.push(terminal);
    }
    return {
      ...record,
      id: `template_admin_code:${index}`,
      cisi: `forger:${index}`,
      type: register,
      tokens: next,
      text: `+${next.join('-')}+`,
    };
  });
}

const controls = [
  {
    name: 'global_token_shuffle',
    planted_structure: 'pure_noise_matched_unigram_and_length',
    description: 'Preserves the observed exact-dedup token multiset and row-length sequence, but destroys row co-occurrence and order.',
    make: forgerGlobalTokenShuffle,
  },
  {
    name: 'row_internal_shuffle',
    planted_structure: 'nonphonetic_row_bag_structure',
    description: 'Preserves each row token bag, but destroys within-row order.',
    make: forgerRowInternalShuffle,
  },
  {
    name: 'position_slot_shuffle',
    planted_structure: 'position_code_null',
    description: 'Samples every row slot independently from the observed same length-position pool.',
    make: forgerPositionSlotShuffle,
  },
  {
    name: 'edge_frame_shuffle',
    planted_structure: 'edge_preserving_nonphonetic_null',
    description: 'Preserves row length and first/last signs exactly, but shuffles interior signs inside each row.',
    make: forgerEdgeFrameShuffle,
  },
  {
    name: 'register_blocked_position_shuffle',
    planted_structure: 'site_type_material_position_code_null',
    description:
      'Samples each length-position slot inside site/type/material blocks when the block has enough examples, falling back to global length-position pools.',
    make: forgerRegisterBlockedPositionShuffle,
  },
  {
    name: 'template_admin_code',
    planted_structure: 'known_nonlinguistic_administrative_template',
    description: 'Generates formulaic authority-office-commodity-qualifier-terminal codes using observed sign pools.',
    make: forgerTemplateAdminCode,
  },
];

function curveRow(scope, coverageFraction, records, metrics) {
  return {
    scope,
    coverage_fraction: coverageFraction,
    rows: metrics.rows,
    tokens: metrics.tokens,
    unique_signs: metrics.unique_signs,
    label_symmetry_log2_bits: metrics.label_symmetry_log2_bits,
    context_equiv_log2_bits: metrics.context_equiv_log2_bits,
    context_equiv_class_count: metrics.context_equiv_class_count,
    context_equiv_signs: metrics.context_equiv_signs,
    largest_context_equiv_class: metrics.largest_context_equiv_class,
    profile_singleton_share: metrics.profile_singleton_share,
    masked_tokens: metrics.masked_tokens,
    masked_sampled: metrics.masked_sampled,
    masked_top1_accuracy: metrics.masked_top1_accuracy,
    masked_top5_accuracy: metrics.masked_top5_accuracy,
    masked_mean_rank: metrics.masked_mean_rank,
    masked_mrr: metrics.masked_mrr,
    masked_mean_true_probability: metrics.masked_mean_true_probability,
    masked_mean_entropy_bits: metrics.masked_mean_entropy_bits,
    masked_mean_effective_candidates: metrics.masked_mean_effective_candidates,
    masked_mean_mass90_candidates: metrics.masked_mean_mass90_candidates,
    context_equiv_examples: metrics.context_equiv_examples.join('; '),
  };
}

function summarizeNulls(observedRows, nullRows) {
  const metrics = [
    { key: 'context_equiv_log2_bits', direction: 'lte' },
    { key: 'profile_singleton_share', direction: 'gte' },
    { key: 'masked_top1_accuracy', direction: 'gte' },
    { key: 'masked_mean_effective_candidates', direction: 'lte' },
    { key: 'masked_mean_mass90_candidates', direction: 'lte' },
  ];
  const out = [];
  for (const coverageFraction of nullCoverageFractions) {
    const observed = observedRows.find((row) => row.coverage_fraction === coverageFraction);
    if (!observed) continue;
    for (const control of controls) {
      const rows = nullRows.filter(
        (row) => row.control === control.name && row.coverage_fraction === coverageFraction,
      );
      for (const metric of metrics) {
        const values = rows.map((row) => Number(row[metric.key])).filter((value) => Number.isFinite(value));
        const sorted = values.slice().sort((a, b) => a - b);
        const observedValue = Number(observed[metric.key]);
        const moreExtreme =
          metric.direction === 'gte'
            ? values.filter((value) => value >= observedValue - epsilon).length
            : values.filter((value) => value <= observedValue + epsilon).length;
        out.push({
          coverage_fraction: coverageFraction,
          control: control.name,
          metric: metric.key,
          direction_more_extreme: metric.direction,
          observed_value: observedValue,
          null_iterations: values.length,
          null_mean: values.reduce((sum, value) => sum + value, 0) / Math.max(1, values.length),
          null_min: sorted[0] ?? null,
          null_p05: percentile(sorted, 0.05),
          null_median: percentile(sorted, 0.5),
          null_p95: percentile(sorted, 0.95),
          null_max: sorted[sorted.length - 1] ?? null,
          false_positive_rate: moreExtreme / Math.max(1, values.length),
        });
      }
    }
  }
  return out;
}

const csvRows = parseCsv(fs.readFileSync(sourcePath, 'utf8'));
const header = csvRows[0];
const column = Object.fromEntries(header.map((name, index) => [name, index]));
const sourceRecords = csvRows
  .slice(1)
  .map((row) => makeRecord(row, column))
  .filter((record) => record.readiness === 'lipi_numeric_clean_candidate' && record.tokens.length > 0);
const exactCollapsed = collapseExactSequences(sourceRecords);
const provenanceAwareSequenceFamilies = countDistinctBy(
  sourceRecords,
  (record) =>
    `${record.tokens.join(' ')}\t${record.site || '-'}\t${record.type || '-'}\t${record.material || '-'}\t${
      record.symbol || '-'
    }`,
);
const orderedRecords = shuffle(exactCollapsed, mulberry32(seedBase));

const observedRows = [];
for (const coverageFraction of coverageFractions) {
  const take = Math.max(1, Math.round(orderedRecords.length * coverageFraction));
  const records = orderedRecords.slice(0, take);
  const metrics = analyzeRecords(records, { rng: mulberry32(seedBase + take) });
  observedRows.push(curveRow('observed_lipi_numeric_clean_exact_sequence_collapsed', coverageFraction, records, metrics));
}

const nullRows = [];
for (const coverageFraction of nullCoverageFractions) {
  const take = Math.max(1, Math.round(orderedRecords.length * coverageFraction));
  const baseRecords = orderedRecords.slice(0, take);
  for (const control of controls) {
    for (let iteration = 0; iteration < iterationsPerControl; iteration++) {
      const rng = mulberry32(seedBase + Math.round(coverageFraction * 1000) * 100000 + iteration * 97 + control.name.length);
      const forged = control.make(baseRecords, rng);
      const metrics = analyzeRecords(forged, {
        sampleLimit: nullMaskedSampleLimit,
        rng: mulberry32(seedBase + iteration * 131 + control.name.length),
      });
      nullRows.push({
        control: control.name,
        planted_structure: control.planted_structure,
        iteration,
        ...curveRow('forger_null', coverageFraction, forged, metrics),
      });
    }
  }
}

const nullSummary = summarizeNulls(observedRows, nullRows);
const curveHeaders = [
  'scope',
  'coverage_fraction',
  'rows',
  'tokens',
  'unique_signs',
  'label_symmetry_log2_bits',
  'context_equiv_log2_bits',
  'context_equiv_class_count',
  'context_equiv_signs',
  'largest_context_equiv_class',
  'profile_singleton_share',
  'masked_tokens',
  'masked_sampled',
  'masked_top1_accuracy',
  'masked_top5_accuracy',
  'masked_mean_rank',
  'masked_mrr',
  'masked_mean_true_probability',
  'masked_mean_entropy_bits',
  'masked_mean_effective_candidates',
  'masked_mean_mass90_candidates',
  'context_equiv_examples',
];
const nullHeaders = ['control', 'planted_structure', 'iteration', ...curveHeaders];
const nullSummaryHeaders = [
  'coverage_fraction',
  'control',
  'metric',
  'direction_more_extreme',
  'observed_value',
  'null_iterations',
  'null_mean',
  'null_min',
  'null_p05',
  'null_median',
  'null_p95',
  'null_max',
  'false_positive_rate',
];

fs.writeFileSync(
  outCurve,
  toCsv([
    curveHeaders,
    ...observedRows.map((row) =>
      curveHeaders.map((key) => (typeof row[key] === 'number' ? round(row[key], 9) : row[key])),
    ),
  ]),
  'utf8',
);

fs.writeFileSync(
  outNullIterations,
  toCsv([
    nullHeaders,
    ...nullRows.map((row) =>
      nullHeaders.map((key) => (typeof row[key] === 'number' ? round(row[key], 9) : row[key])),
    ),
  ]),
  'utf8',
);

fs.writeFileSync(
  outNullSummary,
  toCsv([
    nullSummaryHeaders,
    ...nullSummary.map((row) =>
      nullSummaryHeaders.map((key) => (typeof row[key] === 'number' ? round(row[key], 9) : row[key])),
    ),
  ]),
  'utf8',
);

const fullCoverage = observedRows.find((row) => row.coverage_fraction === 1.0);
const fullNullSummary = nullSummary.filter((row) => row.coverage_fraction === 1.0);
const summary = {
  generated_at_local: formatLocalIso(new Date()),
  source_file: 'data/open_prototype/reports/lipi_scope_rows.csv',
  source_scope: 'lipi_numeric_clean_candidate',
  source_rows: sourceRecords.length,
  exact_collapsed_rows: exactCollapsed.length,
  duplicate_rows_removed: sourceRecords.length - exactCollapsed.length,
  provenance_aware_sequence_families: provenanceAwareSequenceFamilies,
  provenance_aware_key: 'token_sequence + site + type + material + symbol',
  seed_base: seedBase,
  iterations_per_control: iterationsPerControl,
  null_masked_sample_limit: nullMaskedSampleLimit,
  coverage_fractions: coverageFractions,
  null_coverage_fractions: nullCoverageFractions,
  controls: controls.map(({ name, planted_structure, description }) => ({ name, planted_structure, description })),
  primary_full_coverage: fullCoverage,
  full_coverage_false_positive_rates: fullNullSummary,
  language_prior_status: {
    dravidian: 'not_run_no_frozen_primary_lexicon_or_external_value_anchor',
    indo_aryan_sanskritic: 'not_run_no_frozen_primary_lexicon_or_external_value_anchor',
    elamite_adjacent: 'not_run_no_frozen_primary_lexicon_or_external_value_anchor',
    unknown_language_null: 'internal_label_symmetry_only',
    boundary:
      'With no external value anchor, every phonetic label assignment is invariant under a global permutation of the value alphabet. Internal structure can constrain sign roles and contexts, but cannot name phonetic values or distinguish language families.',
  },
  adversarial_interpretation: {
    accepted_as_decipherment: false,
    candidate_structural_result:
      'The exact-deduplicated Lipi working corpus shows measurable context-role collapse as coverage increases, but the full corpus still has a large internal label-symmetry lower bound and structured nonlinguistic forgeries can equal or exceed several masked-sign metrics.',
    no_claims_earned: ['translations', 'phonetic_values', 'sign_meanings', 'language_identification'],
  },
  artifact_files: [
    'data/open_prototype/reports/effective_unicity_degeneracy_curve.csv',
    'data/open_prototype/reports/effective_unicity_degeneracy_null_iterations.csv',
    'data/open_prototype/reports/effective_unicity_degeneracy_null_summary.csv',
    'data/open_prototype/reports/effective_unicity_degeneracy_summary.json',
  ],
};

fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(
  JSON.stringify(
    {
      source_rows: sourceRecords.length,
      exact_collapsed_rows: exactCollapsed.length,
      observed_curve_rows: observedRows.length,
      null_iteration_rows: nullRows.length,
      primary_full_coverage: fullCoverage,
      wrote: summary.artifact_files,
    },
    null,
    2,
  ),
);
