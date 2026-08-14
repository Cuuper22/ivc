// Synthetic forgers are one test; real symbol systems that we know are not
// writing are a harder one. This script runs the masked-sign instrument on six
// real-world corpora from Sproat's 2014 nonlinguistic-symbols bundle (Pictish
// stones, kudurru deity symbols, totem poles, barn stars, Vinca signs, weather
// icons), which must already sit as XML files under
// data/open_prototype/nonlinguistic/sproat2014/. For each corpus it extracts
// document-level symbol sequences from the XML, keeps lengths 2-8, collapses
// exact duplicates, then scores masked-token prediction (leave-one-row-out,
// combining unigram, length-position, left-neighbor, and right-neighbor
// evidence) and runs four shuffle nulls against it. The Indus corpus numbers
// are pulled in as a reference row, and the summary flags any nonlinguistic
// system that matches or beats Indus masked top-1 — if one does, that metric
// alone cannot count as language evidence. Optional CLI args: null iterations
// (default 40), masked sample limit (1500), seed base (20260529). Writes a
// manifest with zip hashes, the extracted sequences CSV, and comparator +
// null summary CSVs/JSON under reports/.
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const sourceDir = path.join(base, 'data', 'open_prototype', 'nonlinguistic', 'sproat2014');
const corpusDir = path.join(sourceDir, 'corpora', 'corpora');
const sourceZipPath = path.join(sourceDir, 'corpora.zip');
const sourceUrl = 'https://rws.xoba.com/data/non-linguistic-symbols/corpora.zip';
const outManifest = path.join(sourceDir, 'sproat2014_manifest.json');
const outSequences = path.join(sourceDir, 'sproat2014_extracted_sequences.csv');
const outSummary = path.join(reportsDir, 'effective_unicity_realworld_nonlinguistic_comparator_summary.json');
const outCsv = path.join(reportsDir, 'effective_unicity_realworld_nonlinguistic_comparator.csv');
const outNullSummary = path.join(reportsDir, 'effective_unicity_realworld_nonlinguistic_null_summary.csv');
const outNullIterations = path.join(reportsDir, 'effective_unicity_realworld_nonlinguistic_null_iterations.csv');

const nullIterations = Number(process.argv[2] ?? 40);
const nullMaskedSampleLimit = Number(process.argv[3] ?? 1500);
const seedBase = Number(process.argv[4] ?? 20260529);
const smoothing = 0.5;
const epsilon = 1e-12;

const corpora = [
  {
    file: 'Pictish.xml',
    corpus: 'Pictish_stones',
    system_class: 'ambiguous_symbol_system',
    source_note: 'University of Strathclyde Pictish Stone Database as encoded in Sproat 2014 XML bundle.',
  },
  {
    file: 'Kudurrus.xml',
    corpus: 'Mesopotamian_kudurru_deity_symbols',
    system_class: 'known_nonwriting_pictorial_symbol_system',
    source_note: 'Seidl 1989 kudurru deity symbols as encoded in Sproat 2014 XML bundle.',
  },
  {
    file: 'TotemPoles.xml',
    corpus: 'Totem_poles',
    system_class: 'known_nonwriting_emblematic_symbol_system',
    source_note: 'Barbeau, Malin, and Stewart sources as encoded in Sproat 2014 XML bundle.',
  },
  {
    file: 'BarnStars.xml',
    corpus: 'Barn_stars_hex_signs',
    system_class: 'known_nonwriting_decorative_symbol_system',
    source_note: 'Pennsylvania German barn stars / hex signs as encoded in Sproat 2014 XML bundle.',
  },
  {
    file: 'Vinca.xml',
    corpus: 'Vinca_symbols',
    system_class: 'ambiguous_archaeological_symbol_system',
    source_note: 'Winn 1981 Vinca sign corpus as encoded in Sproat 2014 XML bundle.',
  },
  {
    file: 'WeatherIcons.xml',
    corpus: 'Weather_icons',
    system_class: 'modern_nonlinguistic_icon_sequence_system',
    source_note: 'Weather icon sequences downloaded from Weather Underground as encoded in Sproat 2014 XML bundle.',
  },
];

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

function round(value, places = 6) {
  if (value === null || value === undefined || !Number.isFinite(Number(value))) return null;
  return Number(Number(value).toFixed(places));
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

function decodeXml(text) {
  return String(text ?? '')
    .replaceAll('&amp;', '&')
    .replaceAll('&lt;', '<')
    .replaceAll('&gt;', '>')
    .replaceAll('&quot;', '"')
    .replaceAll('&apos;', "'")
    .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(Number(n)))
    .replace(/&#x([0-9a-fA-F]+);/g, (_, n) => String.fromCodePoint(parseInt(n, 16)));
}

function getAttr(attrs, name) {
  const re = new RegExp(`${name}\\s*=\\s*"([^"]*)"`);
  return decodeXml(attrs.match(re)?.[1] ?? '');
}

function stripTagBlocks(text, tag) {
  const re = new RegExp(`<${tag}\\b[^>]*>[\\s\\S]*?<\\/${tag}>`, 'gi');
  return text.replace(re, '');
}

function extractTagText(text, tag) {
  const re = new RegExp(`<${tag}\\b[^>]*>([\\s\\S]*?)<\\/${tag}>`, 'gi');
  return [...text.matchAll(re)].map((match) => decodeXml(match[1].replace(/<[^>]+>/g, '').trim()));
}

function extractDocuments(xml, meta) {
  const records = [];
  const documentRe = /<document\b([^>]*)>([\s\S]*?)<\/document>/gi;
  let docIndex = 0;
  for (const match of xml.matchAll(documentRe)) {
    docIndex++;
    const attrs = match[1] ?? '';
    const body = match[2] ?? '';
    const docText = body.match(/<docText\b[^>]*>([\s\S]*?)<\/docText>/i)?.[1] ?? '';
    const cleanDocText = stripTagBlocks(docText, 'alternative');
    const description = extractTagText(body, 'description')[0] ?? `${meta.corpus}_${docIndex}`;
    const tokens = extractTagText(cleanDocText, 'title')
      .map((value) => value.replace(/\s+/g, ' ').trim())
      .filter(Boolean);
    if (!tokens.length) continue;
    records.push({
      id: `${meta.corpus}_${String(docIndex).padStart(5, '0')}`,
      corpus: meta.corpus,
      system_class: meta.system_class,
      source_file: meta.file,
      description,
      document_type: getAttr(attrs, 'type'),
      region: getAttr(attrs, 'region'),
      class_or_group: getAttr(attrs, 'class') || getAttr(attrs, 'group'),
      tokens,
      source_note: meta.source_note,
    });
  }
  return records;
}

function collapseExact(records) {
  const seen = new Map();
  for (const record of records) {
    const key = record.tokens.join('\u0001');
    if (!seen.has(key)) {
      seen.set(key, {
        ...record,
        duplicate_weight: 1,
        source_ids: [record.id],
        descriptions: [record.description],
      });
    } else {
      const existing = seen.get(key);
      existing.duplicate_weight++;
      existing.source_ids.push(record.id);
      existing.descriptions.push(record.description);
    }
  }
  return [...seen.values()].map((record, index) => ({
    ...record,
    id: `${record.corpus}_exact_${String(index + 1).padStart(5, '0')}`,
  }));
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
  const masked = records.length && tokens ? scoreMasked(records, options) : {};
  return {
    rows: records.length,
    tokens,
    unique_signs_or_symbols: vocab.length,
    label_symmetry_log2_bits: log2Factorial(vocab.length),
    masked_tokens: masked.masked_tokens ?? 0,
    masked_top1_accuracy: masked.masked_top1_accuracy ?? null,
    masked_top5_accuracy: masked.masked_top5_accuracy ?? null,
    masked_mean_rank: masked.masked_mean_rank ?? null,
    masked_mrr: masked.masked_mrr ?? null,
    masked_mean_effective_candidates: masked.masked_mean_effective_candidates ?? null,
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
  throw new Error(`Unknown control: ${control}`);
}

function summarizeNulls(nullRows, observedByKey) {
  const out = [];
  const keys = [...new Set(nullRows.map((row) => `${row.corpus}|${row.scope}|${row.control}`))].sort();
  for (const key of keys) {
    const [corpus, scope, control] = key.split('|');
    const rows = nullRows.filter((row) => row.corpus === corpus && row.scope === scope && row.control === control);
    const observed = observedByKey.get(`${corpus}|${scope}`);
    for (const metric of ['masked_top1_accuracy', 'masked_top5_accuracy', 'masked_mrr']) {
      const values = rows
        .map((row) => row[metric])
        .filter((value) => value !== null)
        .sort((a, b) => a - b);
      out.push({
        corpus,
        scope,
        control,
        metric,
        iterations: values.length,
        observed: observed?.[metric] ?? null,
        null_mean: values.reduce((sum, value) => sum + value, 0) / Math.max(1, values.length),
        null_p05: percentile(values, 0.05),
        null_median: percentile(values, 0.5),
        null_p95: percentile(values, 0.95),
        null_max: values.length ? values[values.length - 1] : null,
        null_ge_observed_share:
          values.filter((value) => value >= (observed?.[metric] ?? Infinity) - epsilon).length /
          Math.max(1, values.length),
      });
    }
  }
  return out;
}

function fileHash(filePath, algorithm) {
  return crypto.createHash(algorithm).update(fs.readFileSync(filePath)).digest('hex');
}

function readIndusRow() {
  const summary = JSON.parse(fs.readFileSync(path.join(reportsDir, 'effective_unicity_degeneracy_summary.json'), 'utf8'));
  const full = summary.primary_full_coverage;
  return {
    corpus: 'Indus_Lipi_strict_exact_sequence_collapsed',
    system_class: 'unread_working_corpus',
    scope: 'exact_collapsed_ivc_working_scope',
    rows: full.rows,
    tokens: full.tokens,
    unique_signs_or_symbols: full.unique_signs,
    label_symmetry_log2_bits: full.label_symmetry_log2_bits,
    masked_top1_accuracy: full.masked_top1_accuracy,
    masked_top5_accuracy: full.masked_top5_accuracy,
    masked_mrr: full.masked_mrr,
    max_top1_null_ge_observed_share: 0,
    boundary: 'Indus working corpus; not source-normalized; included only as reference row.',
  };
}

function main() {
  fs.mkdirSync(reportsDir, { recursive: true });
  if (!fs.existsSync(sourceZipPath)) {
    throw new Error(`Missing ${sourceZipPath}. Download ${sourceUrl} and extract it under ${corpusDir}.`);
  }
  if (!fs.existsSync(corpusDir)) {
    throw new Error(`Missing extracted corpus directory ${corpusDir}.`);
  }

  const extractedByCorpus = [];
  const sequenceRows = [];
  for (const meta of corpora) {
    const xmlPath = path.join(corpusDir, meta.file);
    const xml = fs.readFileSync(xmlPath, 'utf8');
    const rawRecords = extractDocuments(xml, meta);
    const lengthCappedRaw = rawRecords.filter((record) => record.tokens.length >= 2 && record.tokens.length <= 8);
    const exactRecords = collapseExact(lengthCappedRaw);
    extractedByCorpus.push({ meta, rawRecords, lengthCappedRaw, exactRecords, xmlPath });
    for (const record of exactRecords) {
      sequenceRows.push({
        corpus: record.corpus,
        system_class: record.system_class,
        sequence_id: record.id,
        description: record.description,
        document_type: record.document_type,
        region: record.region,
        class_or_group: record.class_or_group,
        length: record.tokens.length,
        duplicate_weight: record.duplicate_weight,
        tokens: record.tokens.join(' | '),
        source_ids: record.source_ids.join('|'),
      });
    }
  }

  const controls = ['global_token_shuffle', 'row_internal_shuffle', 'position_slot_shuffle', 'edge_frame_shuffle'];
  const observedRows = [];
  const observedByKey = new Map();
  const nullRows = [];

  for (const corpus of extractedByCorpus) {
    const records = corpus.exactRecords;
    if (records.length < 2) continue;
    const observed = analyzeRecords(records);
    const key = `${corpus.meta.corpus}|exact_collapsed_length_2_to_8`;
    observedByKey.set(key, observed);
    observedRows.push({
      corpus: corpus.meta.corpus,
      system_class: corpus.meta.system_class,
      scope: 'exact_collapsed_length_2_to_8',
      source_file: corpus.meta.file,
      raw_documents: corpus.rawRecords.length,
      length_capped_documents: corpus.lengthCappedRaw.length,
      exact_collapsed_sequences: records.length,
      rows: observed.rows,
      tokens: observed.tokens,
      unique_signs_or_symbols: observed.unique_signs_or_symbols,
      label_symmetry_log2_bits: observed.label_symmetry_log2_bits,
      masked_top1_accuracy: observed.masked_top1_accuracy,
      masked_top5_accuracy: observed.masked_top5_accuracy,
      masked_mrr: observed.masked_mrr,
      masked_mean_effective_candidates: observed.masked_mean_effective_candidates,
      source_note: corpus.meta.source_note,
    });

    for (const control of controls) {
      for (let iteration = 0; iteration < nullIterations; iteration++) {
        const seed = seedBase + 1000 * corpora.findIndex((item) => item.corpus === corpus.meta.corpus);
        const rng = mulberry32(seed + 101 * controls.indexOf(control) + iteration);
        const controlled = controlRecords(records, control, rng);
        const result = analyzeRecords(controlled, {
          sampleLimit: nullMaskedSampleLimit,
          rng: mulberry32(seed + 100000 + 101 * controls.indexOf(control) + iteration),
        });
        nullRows.push({
          corpus: corpus.meta.corpus,
          scope: 'exact_collapsed_length_2_to_8',
          control,
          iteration,
          rows: result.rows,
          tokens: result.tokens,
          unique_signs_or_symbols: result.unique_signs_or_symbols,
          masked_tokens: result.masked_tokens,
          masked_top1_accuracy: result.masked_top1_accuracy,
          masked_top5_accuracy: result.masked_top5_accuracy,
          masked_mrr: result.masked_mrr,
        });
      }
    }
  }

  const nullSummary = summarizeNulls(nullRows, observedByKey);
  const observedWithNulls = observedRows.map((row) => {
    const top1Rows = nullSummary.filter(
      (item) => item.corpus === row.corpus && item.scope === row.scope && item.metric === 'masked_top1_accuracy',
    );
    const maxTop1 = top1Rows.length ? Math.max(...top1Rows.map((item) => item.null_ge_observed_share)) : null;
    const maxNullMean = top1Rows.length ? Math.max(...top1Rows.map((item) => item.null_mean)) : null;
    return {
      ...row,
      max_top1_null_ge_observed_share: maxTop1,
      max_top1_null_mean: maxNullMean,
    };
  });

  const indusRow = readIndusRow();
  const comparatorRows = [indusRow, ...observedWithNulls];
  const nonlingAboveIndus = observedWithNulls
    .filter((row) => row.masked_top1_accuracy >= indusRow.masked_top1_accuracy - epsilon)
    .map((row) => row.corpus);

  const manifest = {
    date: '2026-05-29',
    generated_at_local: formatLocalIso(new Date()),
    generated_at_utc: new Date().toISOString(),
    source_url: sourceUrl,
    source_page: 'https://rws.xoba.com/data/non-linguistic-symbols/',
    source_citation:
      'Richard Sproat (2014), A Statistical Comparison of Written Language and Nonlinguistic Symbol Systems, Language 90(2):457-481.',
    companion_citation:
      'Katherine Wu, Jennifer Solman, Ruth Linehan, and Richard Sproat (2012), Corpora of Non-Linguistic Symbol Systems.',
    local_zip: 'data/open_prototype/nonlinguistic/sproat2014/corpora.zip',
    zip_sha256: fileHash(sourceZipPath, 'sha256'),
    zip_md5: fileHash(sourceZipPath, 'md5'),
    extracted_corpora: extractedByCorpus.map((item) => ({
      corpus: item.meta.corpus,
      file: item.meta.file,
      system_class: item.meta.system_class,
      source_note: item.meta.source_note,
      file_size_bytes: fs.statSync(item.xmlPath).size,
      raw_documents: item.rawRecords.length,
      length_capped_documents_2_to_8: item.lengthCappedRaw.length,
      exact_collapsed_sequences: item.exactRecords.length,
    })),
    extraction_policy: {
      text_unit: 'document-level symbol order from XML docText after removing alternative transcription blocks',
      included_symbols: 'primary symbol/title tags only, including uncertain primary titles as encoded',
      excluded: ['alternative transcription blocks', 'IndusBarSeals.xml'],
      main_scope: 'length 2..8 inclusive, exact sequence collapsed',
    },
  };

  const summary = {
    date: '2026-05-29',
    generated_at_utc: new Date().toISOString(),
    purpose:
      'Real-world nonlinguistic and ambiguous symbol-system comparator battery for the Vector 2 masked-sign effective-unicity instrument.',
    source_files: {
      manifest: 'data/open_prototype/nonlinguistic/sproat2014/sproat2014_manifest.json',
      extracted_sequences: 'data/open_prototype/nonlinguistic/sproat2014/sproat2014_extracted_sequences.csv',
      indus_effective_unicity: 'data/open_prototype/reports/effective_unicity_degeneracy_summary.json',
    },
    source_summary: {
      source_url: manifest.source_url,
      zip_sha256: manifest.zip_sha256,
      corpora: manifest.extracted_corpora,
    },
    indus_reference: {
      rows: indusRow.rows,
      tokens: indusRow.tokens,
      unique_signs: indusRow.unique_signs_or_symbols,
      masked_top1: round(indusRow.masked_top1_accuracy),
      masked_top5: round(indusRow.masked_top5_accuracy),
    },
    realworld_comparator_boundary: {
      comparator_systems_at_or_above_indus_masked_top1: nonlingAboveIndus,
      interpretation:
        nonlingAboveIndus.length > 0
          ? 'At least one real-world nonlinguistic/ambiguous comparator matches or exceeds Indus masked top-1, so masked-sign top-1 alone cannot be promoted as language evidence.'
          : 'No tested real-world nonlinguistic/ambiguous comparator matches Indus masked top-1 in this scope, but mismatch is not acceptance because corpus sizes, symbol inventories, and source normalization are not matched.',
      acceptance_status:
        'No accepted claim count changes. This is adversarial calibration, not a decipherment, sign meaning, or language-family result.',
    },
    rows: comparatorRows.map((row) => ({
      ...row,
      label_symmetry_log2_bits: round(row.label_symmetry_log2_bits),
      masked_top1_accuracy: round(row.masked_top1_accuracy),
      masked_top5_accuracy: round(row.masked_top5_accuracy),
      masked_mrr: round(row.masked_mrr),
      masked_mean_effective_candidates: round(row.masked_mean_effective_candidates),
      max_top1_null_ge_observed_share:
        row.max_top1_null_ge_observed_share === undefined ? '' : round(row.max_top1_null_ge_observed_share),
      max_top1_null_mean: row.max_top1_null_mean === undefined ? '' : round(row.max_top1_null_mean),
    })),
    artifact_files: [
      'data/open_prototype/tools/effective_unicity_realworld_nonlinguistic_comparator.mjs',
      'data/open_prototype/nonlinguistic/sproat2014/corpora.zip',
      'data/open_prototype/nonlinguistic/sproat2014/sproat2014_manifest.json',
      'data/open_prototype/nonlinguistic/sproat2014/sproat2014_extracted_sequences.csv',
      'data/open_prototype/reports/effective_unicity_realworld_nonlinguistic_comparator_summary.json',
      'data/open_prototype/reports/effective_unicity_realworld_nonlinguistic_comparator.csv',
      'data/open_prototype/reports/effective_unicity_realworld_nonlinguistic_null_summary.csv',
      'data/open_prototype/reports/effective_unicity_realworld_nonlinguistic_null_iterations.csv',
    ],
  };

  fs.writeFileSync(outManifest, `${JSON.stringify(manifest, null, 2)}\n`);
  fs.writeFileSync(
    outSequences,
    toCsv([
      [
        'corpus',
        'system_class',
        'sequence_id',
        'description',
        'document_type',
        'region',
        'class_or_group',
        'length',
        'duplicate_weight',
        'tokens',
        'source_ids',
      ],
      ...sequenceRows.map((row) => [
        row.corpus,
        row.system_class,
        row.sequence_id,
        row.description,
        row.document_type,
        row.region,
        row.class_or_group,
        row.length,
        row.duplicate_weight,
        row.tokens,
        row.source_ids,
      ]),
    ]),
  );
  fs.writeFileSync(
    outCsv,
    toCsv([
      [
        'corpus',
        'system_class',
        'scope',
        'rows',
        'tokens',
        'unique_signs_or_symbols',
        'label_symmetry_log2_bits',
        'masked_top1_accuracy',
        'masked_top5_accuracy',
        'masked_mrr',
        'max_top1_null_ge_observed_share',
        'max_top1_null_mean',
        'boundary',
      ],
      ...summary.rows.map((row) => [
        row.corpus,
        row.system_class,
        row.scope,
        row.rows,
        row.tokens,
        row.unique_signs_or_symbols,
        row.label_symmetry_log2_bits,
        row.masked_top1_accuracy,
        row.masked_top5_accuracy,
        row.masked_mrr,
        row.max_top1_null_ge_observed_share,
        row.max_top1_null_mean,
        row.boundary ?? row.source_note ?? '',
      ]),
    ]),
  );
  fs.writeFileSync(
    outNullIterations,
    toCsv([
      [
        'corpus',
        'scope',
        'control',
        'iteration',
        'rows',
        'tokens',
        'unique_signs_or_symbols',
        'masked_tokens',
        'masked_top1_accuracy',
        'masked_top5_accuracy',
        'masked_mrr',
      ],
      ...nullRows.map((row) => [
        row.corpus,
        row.scope,
        row.control,
        row.iteration,
        row.rows,
        row.tokens,
        row.unique_signs_or_symbols,
        row.masked_tokens,
        round(row.masked_top1_accuracy),
        round(row.masked_top5_accuracy),
        round(row.masked_mrr),
      ]),
    ]),
  );
  fs.writeFileSync(
    outNullSummary,
    toCsv([
      [
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
      ],
      ...nullSummary.map((row) => [
        row.corpus,
        row.scope,
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
  fs.writeFileSync(outSummary, `${JSON.stringify(summary, null, 2)}\n`);
  console.log(JSON.stringify(summary, null, 2));
}

main();
