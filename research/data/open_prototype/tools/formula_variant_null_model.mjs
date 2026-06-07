import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const seqPath = path.join(reportsDir, 'formula_pattern_sequences.csv');
const outIterations = path.join(reportsDir, 'formula_variant_null_iterations.csv');
const outSummaryCsv = path.join(reportsDir, 'formula_variant_null_summary.csv');
const outSummaryJson = path.join(reportsDir, 'formula_variant_null_summary.json');

const iterations = Number.parseInt(process.argv[2] ?? '500', 10);
const seed = Number.parseInt(process.argv[3] ?? '20260524', 10);

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

function mulberry32(seedValue) {
  return function nextRandom() {
    let t = (seedValue += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffleCopy(values, rng) {
  const out = values.slice();
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function boundedEditLe2(a, b) {
  const m = a.length;
  const n = b.length;
  if (Math.abs(m - n) > 2) return 3;

  let previous = Array.from({ length: n + 1 }, (_, index) => index);
  for (let i = 1; i <= m; i++) {
    const current = new Array(n + 1).fill(3);
    current[0] = i;
    const from = Math.max(1, i - 2);
    const to = Math.min(n, i + 2);
    for (let j = from; j <= to; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      current[j] = Math.min(
        previous[j] + 1,
        current[j - 1] + 1,
        previous[j - 1] + cost,
      );
    }
    if (Math.min(...current) > 2) return 3;
    previous = current;
  }
  return previous[n] <= 2 ? previous[n] : 3;
}

function hammingDistance(a, b) {
  let diff = 0;
  for (let i = 0; i < a.length; i++) {
    if (a[i] !== b[i]) diff++;
  }
  return diff;
}

function isSingleIndel(a, b) {
  if (Math.abs(a.length - b.length) !== 1) return false;
  const short = a.length < b.length ? a : b;
  const long = a.length < b.length ? b : a;
  let i = 0;
  let j = 0;
  let skipped = 0;
  while (i < short.length && j < long.length) {
    if (short[i] === long[j]) {
      i++;
      j++;
    } else {
      skipped++;
      j++;
      if (skipped > 1) return false;
    }
  }
  return true;
}

function computeMetrics(records) {
  const seqMap = new Map();
  const frameMap = new Map();
  for (const record of records) {
    const sequenceKey = record.tokens.join(' ');
    seqMap.set(sequenceKey, (seqMap.get(sequenceKey) || 0) + 1);
    const frame = `${record.tokens[0]}...${record.tokens.at(-1)}`;
    frameMap.set(frame, (frameMap.get(frame) || 0) + 1);
  }

  let exactGroups = 0;
  let exactPairs = 0;
  for (const count of seqMap.values()) {
    if (count > 1) {
      exactGroups++;
      exactPairs += (count * (count - 1)) / 2;
    }
  }

  let frameFamilies = 0;
  let topFrameRows = 0;
  for (const count of frameMap.values()) {
    if (count > 1) {
      frameFamilies++;
      topFrameRows = Math.max(topFrameRows, count);
    }
  }

  let nearPairs = 0;
  let singleSub = 0;
  let twoSub = 0;
  let singleIndel = 0;
  let sameEdge = 0;
  let variantPairs = 0;
  const slotContexts = new Map();

  for (let i = 0; i < records.length; i++) {
    const a = records[i].tokens;
    for (let j = i + 1; j < records.length; j++) {
      const b = records[j].tokens;
      const edge = a[0] === b[0] && a.at(-1) === b.at(-1);
      if (edge) sameEdge++;

      const editDistance = Math.abs(a.length - b.length) <= 2 ? boundedEditLe2(a, b) : 3;
      if (editDistance <= 2) nearPairs++;
      if (editDistance <= 2 || edge) variantPairs++;

      if (a.length === b.length) {
        const diff = hammingDistance(a, b);
        if (diff === 1) {
          singleSub++;
          const slot = a.findIndex((token, index) => token !== b[index]);
          const left = slot === 0 ? '<s>' : a[slot - 1];
          const right = slot === a.length - 1 ? '</s>' : a[slot + 1];
          const context = `${a.length}\t${slot}\t${left}\t${right}`;
          const signs = [a[slot], b[slot]].sort().join(';');
          if (!slotContexts.has(context)) slotContexts.set(context, new Set());
          slotContexts.get(context).add(signs);
        } else if (diff === 2) {
          twoSub++;
        }
      } else if (editDistance === 1 && isSingleIndel(a, b)) {
        singleIndel++;
      }
    }
  }

  return {
    strict_records: records.length,
    exact_duplicate_sequence_groups: exactGroups,
    exact_duplicate_pairs: exactPairs,
    variant_pairs_total: variantPairs,
    near_pairs_edit_distance_le_2: nearPairs,
    single_substitution_pairs: singleSub,
    two_substitution_pairs: twoSub,
    single_insertion_deletion_pairs: singleIndel,
    shared_edge_frame_pairs: sameEdge,
    frame_families_count: frameFamilies,
    top_frame_rows: topFrameRows,
    slot_candidate_groups: slotContexts.size,
  };
}

function quantile(sorted, q) {
  const pos = (sorted.length - 1) * q;
  const lo = Math.floor(pos);
  const hi = Math.ceil(pos);
  if (lo === hi) return sorted[lo];
  return sorted[lo] + (sorted[hi] - sorted[lo]) * (pos - lo);
}

function summarize(values, observed) {
  const sorted = values.slice().sort((a, b) => a - b);
  const mean = values.reduce((sum, value) => sum + value, 0) / values.length;
  const variance =
    values.reduce((sum, value) => sum + (value - mean) ** 2, 0) / values.length;
  const ge = values.filter((value) => value >= observed).length;
  const le = values.filter((value) => value <= observed).length;
  return {
    observed,
    null_mean: mean,
    null_sd: Math.sqrt(variance),
    null_min: sorted[0],
    null_p05: quantile(sorted, 0.05),
    null_p50: quantile(sorted, 0.5),
    null_p95: quantile(sorted, 0.95),
    null_max: sorted.at(-1),
    observed_minus_mean: observed - mean,
    empirical_p_ge: (ge + 1) / (values.length + 1),
    empirical_p_le: (le + 1) / (values.length + 1),
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

function makeLengthFrequency(records, rng) {
  const tokens = shuffleCopy(
    records.flatMap((record) => record.tokens),
    rng,
  );
  let cursor = 0;
  return records.map((record) => {
    const sequence = tokens.slice(cursor, cursor + record.tokens.length);
    cursor += record.tokens.length;
    return { id: record.id, tokens: sequence };
  });
}

function makeEdgePreserving(records, rng) {
  const firsts = shuffleCopy(
    records.map((record) => record.tokens[0]),
    rng,
  );
  const lasts = shuffleCopy(
    records.map((record) => record.tokens.at(-1)),
    rng,
  );
  const interiors = shuffleCopy(
    records.flatMap((record) => record.tokens.slice(1, -1)),
    rng,
  );
  let cursor = 0;
  return records.map((record, index) => {
    if (record.tokens.length === 1) return { id: record.id, tokens: [firsts[index]] };
    const interiorLength = record.tokens.length - 2;
    const sequence = [
      firsts[index],
      ...interiors.slice(cursor, cursor + interiorLength),
      lasts[index],
    ];
    cursor += interiorLength;
    return { id: record.id, tokens: sequence };
  });
}

const rows = parseCsv(fs.readFileSync(seqPath, 'utf8'));
const header = rows[0];
const column = Object.fromEntries(header.map((name, index) => [name, index]));
const observedRecords = rows
  .slice(1)
  .filter((row) => row[column.policy] === 'mayig_observed_parpola')
  .map((row) => ({
    id: row[column.cisi],
    tokens: row[column.sequence].trim().split(/\s+/).filter(Boolean),
  }))
  .filter((record) => record.tokens.length > 0);

const observedMetrics = computeMetrics(observedRecords);
const rng = mulberry32(seed);
const models = [
  ['length_frequency_shuffle', makeLengthFrequency],
  ['edge_position_preserving_shuffle', makeEdgePreserving],
];
const metricNames = Object.keys(observedMetrics).filter((metric) => metric !== 'strict_records');

const iterationRows = [['model', 'iteration', ...metricNames]];
const samples = Object.fromEntries(
  models.map(([name]) => [
    name,
    Object.fromEntries(metricNames.map((metric) => [metric, []])),
  ]),
);

for (let iteration = 1; iteration <= iterations; iteration++) {
  for (const [modelName, maker] of models) {
    const sampleRecords = maker(observedRecords, rng);
    const metrics = computeMetrics(sampleRecords);
    iterationRows.push([
      modelName,
      iteration,
      ...metricNames.map((metric) => metrics[metric]),
    ]);
    for (const metric of metricNames) {
      samples[modelName][metric].push(metrics[metric]);
    }
  }
}

const summaryRows = [
  [
    'model',
    'metric',
    'observed',
    'null_mean',
    'null_sd',
    'null_min',
    'null_p05',
    'null_p50',
    'null_p95',
    'null_max',
    'observed_minus_mean',
    'empirical_p_ge',
    'empirical_p_le',
  ],
];
const summary = {
  generated_at_local: formatLocalIso(new Date()),
  source_file: 'data/open_prototype/reports/formula_pattern_sequences.csv',
  policy: 'mayig_observed_parpola',
  iterations,
  seed,
  strict_records: observedRecords.length,
  null_models: {
    length_frequency_shuffle:
      'Preserves observed row lengths and the global sign-token frequency distribution, but not edge positions.',
    edge_position_preserving_shuffle:
      'Preserves row lengths, the first-sign multiset, the last-sign multiset, and the interior-token multiset.',
  },
  observed_metrics: observedMetrics,
  summary: {},
  artifact_files: [
    'data/open_prototype/reports/formula_variant_null_iterations.csv',
    'data/open_prototype/reports/formula_variant_null_summary.csv',
    'data/open_prototype/reports/formula_variant_null_summary.json',
  ],
  interpretation_boundary:
    'Null-model structural screen only; no sign value, semantic, phonetic, or translation claim.',
};

for (const [modelName] of models) {
  summary.summary[modelName] = {};
  for (const metric of metricNames) {
    const stats = summarize(samples[modelName][metric], observedMetrics[metric]);
    summary.summary[modelName][metric] = stats;
    summaryRows.push([
      modelName,
      metric,
      stats.observed,
      stats.null_mean.toFixed(6),
      stats.null_sd.toFixed(6),
      stats.null_min,
      stats.null_p05.toFixed(6),
      stats.null_p50.toFixed(6),
      stats.null_p95.toFixed(6),
      stats.null_max,
      stats.observed_minus_mean.toFixed(6),
      stats.empirical_p_ge.toFixed(6),
      stats.empirical_p_le.toFixed(6),
    ]);
  }
}

fs.writeFileSync(outIterations, toCsv(iterationRows), 'utf8');
fs.writeFileSync(outSummaryCsv, toCsv(summaryRows), 'utf8');
fs.writeFileSync(outSummaryJson, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(
  JSON.stringify(
    {
      iterations,
      rows: observedRecords.length,
      metrics: observedMetrics,
      wrote: summary.artifact_files,
    },
    null,
    2,
  ),
);
