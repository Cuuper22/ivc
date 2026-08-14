// We have a candidate claim that Indus inscriptions read better in their stored
// order than reversed (the "Vector 2 directionality" signal). This script plays
// the skeptic. It rebuilds the direction test on two hard subsets: the tiny
// source-visible 861 terminal-tail rows (from the campaign 032 attachment and
// bare-edge CSVs) and the matched lipi/mayig crosswalk overlap, then attacks
// each with shuffle nulls — global token shuffle, within-row shuffle,
// position-slot shuffle, and edge-preserving shuffles that keep first/last
// signs, length, symbol/type/material block, and catalog block fixed. The
// direction score is leave-one-out: for each row we ask whether a smoothed
// bigram model trained on all other rows gives the stored order a higher log
// probability than the reversed order, and report the share of rows where
// stored wins. If a null that preserves edge structure matches the observed
// win share, the "directionality" could just be edge-sign convention, not
// reading order. Writes a JSON summary plus per-scope, per-control, and
// per-iteration CSVs into data/open_prototype/reports/.
import fs from 'fs';
import path from 'path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const outSummary = path.join(reportsDir, 'effective_unicity_directionality_skeptic_controls_summary.json');
const outRows = path.join(reportsDir, 'effective_unicity_directionality_skeptic_controls.csv');
const outNullSummary = path.join(reportsDir, 'effective_unicity_directionality_skeptic_null_summary.csv');
const outNullIterations = path.join(reportsDir, 'effective_unicity_directionality_skeptic_null_iterations.csv');
const outSourceVisibleRows = path.join(reportsDir, 'effective_unicity_directionality_source_visible_861_rows.csv');

const START = '<S>';
const END = '</S>';
const ALPHA = 0.1;
const NULL_ITERATIONS = Number(process.argv.find((arg) => arg.startsWith('--iterations='))?.split('=')[1] ?? 200);

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
  if (/[",\n\r]/.test(text)) return `"${text.replaceAll('"', '""')}"`;
  return `"${text}"`;
}

function toCsv(rows, columns) {
  return `${columns.map(csvEscape).join(',')}\n${rows
    .map((row) => columns.map((column) => csvEscape(row[column])).join(','))
    .join('\n')}\n`;
}

function parseTokens(text) {
  return [...String(text).matchAll(/\d{3}/g)].map((match) => match[0]);
}

function exactCollapse(records) {
  const byKey = new Map();
  for (const record of records) {
    if (record.tokens.length < 2) continue;
    const key = record.tokens.join(' ');
    if (byKey.has(key)) {
      const current = byKey.get(key);
      current.duplicate_weight += record.duplicate_weight ?? 1;
      current.source_ids.push(...record.source_ids);
      current.labels.add(record.label);
    } else {
      byKey.set(key, {
        ...record,
        tokens: [...record.tokens],
        source_ids: [...record.source_ids],
        labels: new Set([record.label]),
        duplicate_weight: record.duplicate_weight ?? 1,
      });
    }
  }
  return [...byKey.values()].sort((a, b) => a.tokens.join(' ').localeCompare(b.tokens.join(' ')));
}

function topEdgeRemoved(records, topN = 10) {
  const counts = new Map();
  for (const record of records) {
    counts.set(record.tokens[0], (counts.get(record.tokens[0]) ?? 0) + 1);
    counts.set(record.tokens[record.tokens.length - 1], (counts.get(record.tokens[record.tokens.length - 1]) ?? 0) + 1);
  }
  const top = new Set([...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, topN)
    .map(([token]) => token));
  return records.filter((record) => !top.has(record.tokens[0]) && !top.has(record.tokens[record.tokens.length - 1]));
}

function transitions(tokens) {
  const framed = [START, ...tokens, END];
  const out = [];
  for (let i = 0; i < framed.length - 1; i++) out.push([framed[i], framed[i + 1]]);
  return out;
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
      bigramCounts.set(key, (bigramCounts.get(key) ?? 0) + 1);
      prevCounts.set(prev, (prevCounts.get(prev) ?? 0) + 1);
      bigrams.set(key, (bigrams.get(key) ?? 0) + 1);
      prevs.set(prev, (prevs.get(prev) ?? 0) + 1);
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
  for (let index = 0; index < usable.length; index++) {
    const record = usable[index];
    const stored = logProb(record.tokens, counts, index);
    const reversed = logProb([...record.tokens].reverse(), counts, index);
    const diff = (stored - reversed) / (record.tokens.length + 1);
    diffSum += diff;
    if (Math.abs(diff) < 1e-12) ties++;
    else if (diff > 0) storedHigher++;
    else reversedHigher++;
  }
  const rows = usable.length;
  return {
    rows,
    tokens: usable.reduce((sum, record) => sum + record.tokens.length, 0),
    unique_tokens: new Set(usable.flatMap((record) => record.tokens)).size,
    stored_higher: storedHigher,
    reversed_higher: reversedHigher,
    ties,
    stored_win_share: rows ? storedHigher / rows : 0,
    mean_stored_minus_reversed_per_transition: rows ? diffSum / rows : 0,
  };
}

function makeRng(seed) {
  let state = seed >>> 0;
  return () => {
    state = (1664525 * state + 1013904223) >>> 0;
    return state / 0x100000000;
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

function shuffleInPlace(array, rng) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

function cloneRecord(record) {
  return {
    ...record,
    tokens: [...record.tokens],
    source_ids: [...record.source_ids],
    labels: new Set(record.labels ?? [record.label]),
  };
}

function makeNull(records, control, rng) {
  if (control === 'global_token_shuffle') {
    const pool = shuffleInPlace(records.flatMap((record) => record.tokens), rng);
    let cursor = 0;
    return records.map((record) => {
      const next = cloneRecord(record);
      next.tokens = pool.slice(cursor, cursor + record.tokens.length);
      cursor += record.tokens.length;
      return next;
    });
  }
  if (control === 'row_internal_shuffle') {
    return records.map((record) => {
      const next = cloneRecord(record);
      next.tokens = shuffleInPlace([...record.tokens], rng);
      return next;
    });
  }
  if (control === 'position_slot_shuffle') {
    return slotShuffle(records, rng, (record, pos) => `${record.tokens.length}\t${pos}`, false);
  }
  if (control === 'edge_frame_shuffle') {
    return edgeInteriorShuffle(records, rng, () => 'all');
  }
  if (control === 'edge_length_position_shuffle') {
    return slotShuffle(records, rng, (record, pos) => `${record.tokens.length}\t${pos}`, true);
  }
  if (control === 'edge_symbol_catalog_position_shuffle') {
    return slotShuffle(
      records,
      rng,
      (record, pos) => `${record.tokens.length}\t${record.symbol_block}\t${record.catalog_block}\t${pos}`,
      true,
    );
  }
  if (control === 'edge_symbol_catalog_interior_shuffle') {
    return edgeInteriorShuffle(records, rng, (record) => `${record.tokens.length}\t${record.symbol_block}\t${record.catalog_block}`);
  }
  throw new Error(`Unknown control: ${control}`);
}

function slotShuffle(records, rng, keyFn, preserveEdges) {
  const pools = new Map();
  const cursors = new Map();
  for (const record of records) {
    record.tokens.forEach((token, pos) => {
      if (preserveEdges && (pos === 0 || pos === record.tokens.length - 1)) return;
      const key = keyFn(record, pos);
      if (!pools.has(key)) pools.set(key, []);
      pools.get(key).push(token);
    });
  }
  for (const pool of pools.values()) shuffleInPlace(pool, rng);
  return records.map((record) => {
    const next = cloneRecord(record);
    next.tokens = record.tokens.map((token, pos) => {
      if (preserveEdges && (pos === 0 || pos === record.tokens.length - 1)) return token;
      const key = keyFn(record, pos);
      const cursor = cursors.get(key) ?? 0;
      cursors.set(key, cursor + 1);
      return pools.get(key)[cursor];
    });
    return next;
  });
}

function edgeInteriorShuffle(records, rng, blockFn) {
  const pools = new Map();
  const cursors = new Map();
  for (const record of records) {
    if (record.tokens.length <= 2) continue;
    const key = blockFn(record);
    if (!pools.has(key)) pools.set(key, []);
    pools.get(key).push(...record.tokens.slice(1, -1));
  }
  for (const pool of pools.values()) shuffleInPlace(pool, rng);
  return records.map((record) => {
    const next = cloneRecord(record);
    if (record.tokens.length > 2) {
      const key = blockFn(record);
      const cursor = cursors.get(key) ?? 0;
      cursors.set(key, cursor + record.tokens.length - 2);
      next.tokens = [record.tokens[0], ...pools.get(key).slice(cursor, cursor + record.tokens.length - 2), record.tokens[record.tokens.length - 1]];
    }
    return next;
  });
}

function summarize(values) {
  const sorted = [...values].sort((a, b) => a - b);
  const mean = values.reduce((sum, value) => sum + value, 0) / values.length;
  const q = (p) => sorted[Math.min(sorted.length - 1, Math.max(0, Math.floor(p * (sorted.length - 1))))] ?? 0;
  return { mean, p05: q(0.05), median: q(0.5), p95: q(0.95), max: sorted[sorted.length - 1] ?? 0 };
}

function runNulls(records, corpus, scope, controls) {
  const observed = scoreDirection(records);
  const nullRows = [];
  const iterationRows = [];
  for (const control of controls) {
    const values = [];
    for (let iteration = 0; iteration < NULL_ITERATIONS; iteration++) {
      const rng = makeRng(hashString(`${corpus}:${scope}:${control}:${iteration}`));
      const score = scoreDirection(makeNull(records, control, rng));
      values.push(score.stored_win_share);
      iterationRows.push({
        corpus,
        scope,
        control,
        iteration: iteration + 1,
        stored_win_share: round(score.stored_win_share),
      });
    }
    const stats = summarize(values);
    nullRows.push({
      corpus,
      scope,
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
  return { observed, nullRows, iterationRows };
}

function round(value) {
  return Number.isFinite(value) ? Number(value.toFixed(6)) : null;
}

function catalogBlock(cisi) {
  const match = String(cisi ?? '').match(/^([A-Za-z]+)-?(\d+)/);
  if (!match) return 'UNKNOWN';
  const start = Math.floor((Number(match[2]) - 1) / 50) * 50 + 1;
  return `${match[1].toUpperCase()}-${String(start).padStart(4, '0')}-${String(start + 49).padStart(4, '0')}`;
}

function loadSourceVisible861() {
  const tailed = loadCsv(path.join(reportsDir, 'campaign_032_002_861_source_token_attachment_verdicts.csv'))
    .map((row) => ({
      corpus: 'source_visible_861_terminal_tail_probe',
      scope: 'tailed_and_bare_source_visible_rows',
      id: row.cisi,
      label: 'tailed',
      cisi: row.cisi,
      family: row.tail_family,
      visual_status: row.attachment_verdict,
      source_status: row.source_quality,
      tokens: parseTokens(row.text),
      duplicate_weight: 1,
      source_ids: [row.source_image_abs],
      symbol_block: row.tail_family,
      catalog_block: catalogBlock(row.cisi),
    }));
  const bareWanted = new Set(['H-444', 'M-723', 'M-1044', 'M-77', 'M-118', 'M-15']);
  const bare = loadCsv(path.join(reportsDir, 'campaign_032_002_861_bare_edge_source_controls_rows.csv'))
    .filter((row) => bareWanted.has(row.cisi) && row.visual_status === 'bare_terminal_edge_visible')
    .map((row) => ({
      corpus: 'source_visible_861_terminal_tail_probe',
      scope: 'tailed_and_bare_source_visible_rows',
      id: row.cisi,
      label: 'bare',
      cisi: row.cisi,
      family: row.family,
      visual_status: row.visual_status,
      source_status: row.route_status,
      tokens: parseTokens(row.text),
      duplicate_weight: 1,
      source_ids: [row.source_image_abs],
      symbol_block: row.family,
      catalog_block: catalogBlock(row.cisi),
    }));
  return [...tailed, ...bare].filter((row) => row.tokens.length >= 2);
}

function loadLipiMetadata() {
  const byId = new Map();
  for (const row of loadCsv(path.join(reportsDir, 'lipi_scope_rows.csv'))) {
    byId.set(row.id, row);
  }
  return byId;
}

function loadCrosswalkLayers() {
  const lipiMeta = loadLipiMetadata();
  const groups = new Map();
  for (const row of loadCsv(path.join(reportsDir, 'crosswalk_alignment_pairs.csv'))) {
    const key = `${row.lipi_id}\t${row.mayig_side_id}`;
    if (!groups.has(key)) {
      const meta = lipiMeta.get(row.lipi_id) ?? {};
      groups.set(key, {
        cisi: row.cisi,
        lipi_id: row.lipi_id,
        mayig_side_id: row.mayig_side_id,
        symbol: meta.symbol || 'UNKNOWN',
        type: meta.type || 'UNKNOWN',
        material: meta.material || 'UNKNOWN',
        lipi: [],
        mayig: [],
      });
    }
    const group = groups.get(key);
    group.lipi.push({ pos: Number(row.position_0based), token: row.lipi_sign });
    group.mayig.push({ pos: Number(row.position_0based), token: row.mayig_sign });
  }
  const lipi = [];
  const mayig = [];
  for (const group of groups.values()) {
    const lipiTokens = group.lipi.sort((a, b) => a.pos - b.pos).map((entry) => entry.token);
    const mayigTokens = group.mayig.sort((a, b) => a.pos - b.pos).map((entry) => entry.token);
    if (lipiTokens.length < 2 || lipiTokens.length > 8 || lipiTokens.length !== mayigTokens.length) continue;
    const common = {
      duplicate_weight: 1,
      source_ids: [`${group.cisi}:${group.lipi_id}:${group.mayig_side_id}`],
      cisi: group.cisi,
      label: 'matched_overlap',
      symbol_block: `${group.symbol}|${group.type}|${group.material}`,
      catalog_block: catalogBlock(group.cisi),
    };
    lipi.push({ ...common, id: `lipi:${group.lipi_id}:${group.mayig_side_id}`, tokens: lipiTokens });
    mayig.push({ ...common, id: `mayig:${group.lipi_id}:${group.mayig_side_id}`, tokens: mayigTokens });
  }
  return {
    lipi: exactCollapse(lipi),
    mayig: exactCollapse(mayig),
  };
}

const standardControls = ['global_token_shuffle', 'row_internal_shuffle', 'position_slot_shuffle', 'edge_frame_shuffle'];
const overlapControls = [
  ...standardControls,
  'edge_length_position_shuffle',
  'edge_symbol_catalog_position_shuffle',
  'edge_symbol_catalog_interior_shuffle',
];

const sourceVisible = loadSourceVisible861();
const crosswalk = loadCrosswalkLayers();
const scopes = [
  {
    corpus: 'source_visible_861_terminal_tail_probe',
    scope: 'tailed_and_bare_source_visible_rows',
    records: sourceVisible,
    controls: standardControls,
    source: 'campaign_032_002_861_source_token_attachment_verdicts.csv + campaign_032_002_861_bare_edge_source_controls_rows.csv',
  },
  {
    corpus: 'matched_overlap_lipi_side',
    scope: 'exact_collapsed',
    records: crosswalk.lipi,
    controls: overlapControls,
    source: 'crosswalk_alignment_pairs.csv joined to lipi_scope_rows.csv',
  },
  {
    corpus: 'matched_overlap_mayig_side',
    scope: 'exact_collapsed',
    records: crosswalk.mayig,
    controls: overlapControls,
    source: 'crosswalk_alignment_pairs.csv joined to lipi_scope_rows.csv',
  },
  {
    corpus: 'matched_overlap_lipi_side',
    scope: 'top10_edge_removed',
    records: topEdgeRemoved(crosswalk.lipi, 10),
    controls: overlapControls,
    source: 'crosswalk_alignment_pairs.csv joined to lipi_scope_rows.csv',
  },
  {
    corpus: 'matched_overlap_mayig_side',
    scope: 'top10_edge_removed',
    records: topEdgeRemoved(crosswalk.mayig, 10),
    controls: overlapControls,
    source: 'crosswalk_alignment_pairs.csv joined to lipi_scope_rows.csv',
  },
];

const resultRows = [];
const nullRows = [];
const iterationRows = [];
for (const item of scopes) {
  const { observed, nullRows: scopeNullRows, iterationRows: scopeIterationRows } = runNulls(
    item.records,
    item.corpus,
    item.scope,
    item.controls,
  );
  const maxNullShare = Math.max(...scopeNullRows.map((row) => Number(row.null_ge_observed_share)));
  resultRows.push({
    corpus: item.corpus,
    scope: item.scope,
    source: item.source,
    rows: observed.rows,
    tokens: observed.tokens,
    unique_tokens: observed.unique_tokens,
    stored_higher: observed.stored_higher,
    reversed_higher: observed.reversed_higher,
    ties: observed.ties,
    stored_win_share: round(observed.stored_win_share),
    mean_stored_minus_reversed_per_transition: round(observed.mean_stored_minus_reversed_per_transition),
    max_null_ge_observed_share: round(maxNullShare),
  });
  nullRows.push(...scopeNullRows);
  iterationRows.push(...scopeIterationRows);
}

const sourceRowsForCsv = sourceVisible.map((row) => ({
  cisi: row.cisi,
  class: row.label,
  family: row.family,
  text: `+${row.tokens.join('-')}+`,
  tokens: row.tokens.join(' '),
  visual_status: row.visual_status,
  source_status: row.source_status,
  source_image_abs: row.source_ids[0],
}));

const sourceProbe = resultRows.find((row) => row.corpus === 'source_visible_861_terminal_tail_probe');
const overlapMayigTopRemoved = resultRows.find((row) => row.corpus === 'matched_overlap_mayig_side' && row.scope === 'top10_edge_removed');
const overlapLipiTopRemoved = resultRows.find((row) => row.corpus === 'matched_overlap_lipi_side' && row.scope === 'top10_edge_removed');
const strongestOverlapNull = nullRows
  .filter((row) => row.corpus.startsWith('matched_overlap'))
  .sort((a, b) => Number(b.null_ge_observed_share) - Number(a.null_ge_observed_share))[0];

const summary = {
  date: '2026-05-29',
  generated_at_utc: new Date().toISOString(),
  purpose: 'Skeptic controls for the Vector 2 directionality candidate: source-visible 861 terminal/tail sensitivity and matched-overlap block-conditioned edge/slot nulls.',
  method: {
    null_iterations_per_control: NULL_ITERATIONS,
    source_visible_boundary: 'The 861 subset is target-selected and tiny. It is a source-visible sensitivity probe only, not source-normalized directionality evidence.',
    matched_overlap_boundary: 'The matched overlap uses provisional position alignment and zero accepted crosswalk edges. Block-conditioned nulls preserve edge signs, length-position slots, symbol/type/material block, and catalog block where specified.',
  },
  primary_results: {
    source_visible_861_terminal_tail_probe: sourceProbe,
    matched_overlap_lipi_top10_edge_removed: overlapLipiTopRemoved,
    matched_overlap_mayig_top10_edge_removed: overlapMayigTopRemoved,
    strongest_overlap_null_attack: strongestOverlapNull,
  },
  rows: resultRows,
  artifact_files: [
    'data/open_prototype/tools/effective_unicity_directionality_skeptic_controls.mjs',
    'data/open_prototype/reports/effective_unicity_directionality_skeptic_controls_summary.json',
    'data/open_prototype/reports/effective_unicity_directionality_skeptic_controls.csv',
    'data/open_prototype/reports/effective_unicity_directionality_skeptic_null_summary.csv',
    'data/open_prototype/reports/effective_unicity_directionality_skeptic_null_iterations.csv',
    'data/open_prototype/reports/effective_unicity_directionality_source_visible_861_rows.csv',
  ],
};

fs.writeFileSync(outSummary, `${JSON.stringify(summary, null, 2)}\n`);
fs.writeFileSync(outRows, toCsv(resultRows, [
  'corpus',
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
  'max_null_ge_observed_share',
]));
fs.writeFileSync(outNullSummary, toCsv(nullRows, [
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
fs.writeFileSync(outNullIterations, toCsv(iterationRows, [
  'corpus',
  'scope',
  'control',
  'iteration',
  'stored_win_share',
]));
fs.writeFileSync(outSourceVisibleRows, toCsv(sourceRowsForCsv, [
  'cisi',
  'class',
  'family',
  'text',
  'tokens',
  'visual_status',
  'source_status',
  'source_image_abs',
]));

console.log(JSON.stringify(summary, null, 2));
