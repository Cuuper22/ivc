import fs from 'fs';
import path from 'path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const inputRows = path.join(reportsDir, 'lipi_scope_rows.csv');
const outSummary = path.join(reportsDir, 'effective_unicity_directionality_influence_controls_summary.json');
const outRowInfluence = path.join(reportsDir, 'effective_unicity_directionality_influence_rows.csv');
const outFamilyInfluence = path.join(reportsDir, 'effective_unicity_directionality_influence_families.csv');

const START = '<S>';
const END = '</S>';
const ALPHA = 0.1;
const DATE = '2026-05-29';

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;
  for (let index = 0; index < text.length; index++) {
    const char = text[index];
    if (inQuotes) {
      if (char === '"') {
        if (text[index + 1] === '"') {
          field += '"';
          index++;
        } else {
          inQuotes = false;
        }
      } else {
        field += char;
      }
    } else if (char === '"') {
      inQuotes = true;
    } else if (char === ',') {
      row.push(field);
      field = '';
    } else if (char === '\n') {
      row.push(field);
      rows.push(row);
      row = [];
      field = '';
    } else if (char !== '\r') {
      field += char;
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

function round(value, digits = 6) {
  if (!Number.isFinite(value)) return value;
  const factor = 10 ** digits;
  return Math.round(value * factor) / factor;
}

function normalize(value) {
  return String(value || '-').trim() || '-';
}

function parseTokens(text) {
  return [...String(text).matchAll(/\d{3}/g)].map((match) => match[0]);
}

function addCounts(map, key, delta) {
  const next = (map.get(key) ?? 0) + delta;
  if (next === 0) map.delete(key);
  else map.set(key, next);
}

function transitions(tokens) {
  const sequence = [START, ...tokens, END];
  const pairs = [];
  for (let index = 0; index < sequence.length - 1; index++) {
    pairs.push([sequence[index], sequence[index + 1]]);
  }
  return pairs;
}

function emptyBundle() {
  return { bigrams: new Map(), prevs: new Map() };
}

function addRecordToBundle(record, bundle) {
  for (const [prev, next] of transitions(record.tokens)) {
    const key = `${prev}\t${next}`;
    addCounts(bundle.bigrams, key, 1);
    addCounts(bundle.prevs, prev, 1);
  }
}

function buildCounts(records) {
  const vocab = new Set();
  const bigramCounts = new Map();
  const prevCounts = new Map();
  const rowCounts = records.map((record) => {
    const rowBundle = emptyBundle();
    for (const token of record.tokens) vocab.add(token);
    for (const [prev, next] of transitions(record.tokens)) {
      const key = `${prev}\t${next}`;
      addCounts(bigramCounts, key, 1);
      addCounts(prevCounts, prev, 1);
      addCounts(rowBundle.bigrams, key, 1);
      addCounts(rowBundle.prevs, prev, 1);
    }
    return rowBundle;
  });
  return { vocab, bigramCounts, prevCounts, rowCounts };
}

function logProb(tokens, counts, excludedBundle) {
  const outcomeCount = counts.vocab.size + 1;
  let total = 0;
  for (const [prev, next] of transitions(tokens)) {
    const key = `${prev}\t${next}`;
    const bigramCount = (counts.bigramCounts.get(key) ?? 0) - (excludedBundle?.bigrams.get(key) ?? 0);
    const prevCount = (counts.prevCounts.get(prev) ?? 0) - (excludedBundle?.prevs.get(prev) ?? 0);
    total += Math.log((bigramCount + ALPHA) / (prevCount + ALPHA * outcomeCount));
  }
  return total;
}

function scoreDirection(records, options = {}) {
  const includeRowScores = options.includeRowScores ?? false;
  const usable = records.filter((record) => record.tokens.length > 1);
  const counts = buildCounts(usable);
  let storedHigher = 0;
  let reversedHigher = 0;
  let ties = 0;
  let diffSum = 0;
  let diffTotalSum = 0;
  const diffs = [];
  const rowScores = [];

  usable.forEach((record, rowIndex) => {
    const stored = logProb(record.tokens, counts, counts.rowCounts[rowIndex]);
    const reversed = logProb([...record.tokens].reverse(), counts, counts.rowCounts[rowIndex]);
    const diffTotal = stored - reversed;
    const diffPerTransition = diffTotal / (record.tokens.length + 1);
    diffSum += diffPerTransition;
    diffTotalSum += diffTotal;
    diffs.push(diffPerTransition);
    let outcome = 'tie';
    if (Math.abs(diffPerTransition) < 1e-12) {
      ties++;
    } else if (diffPerTransition > 0) {
      storedHigher++;
      outcome = 'stored';
    } else {
      reversedHigher++;
      outcome = 'reversed';
    }
    if (includeRowScores) {
      rowScores.push({
        record,
        stored_log_prob: stored,
        reversed_log_prob: reversed,
        stored_minus_reversed_total: diffTotal,
        stored_minus_reversed_per_transition: diffPerTransition,
        row_outcome: outcome,
      });
    }
  });

  diffs.sort((a, b) => a - b);
  const result = {
    rows: usable.length,
    tokens: usable.reduce((sum, record) => sum + record.tokens.length, 0),
    unique_tokens: counts.vocab.size,
    stored_higher: storedHigher,
    reversed_higher: reversedHigher,
    ties,
    stored_win_share: usable.length ? storedHigher / usable.length : 0,
    mean_stored_minus_reversed_per_transition: usable.length ? diffSum / usable.length : 0,
    median_stored_minus_reversed_per_transition: diffs[Math.floor(diffs.length / 2)] ?? 0,
    total_stored_minus_reversed: diffTotalSum,
  };
  if (includeRowScores) result.row_scores = rowScores;
  return result;
}

function exactCollapse(records) {
  const byKey = new Map();
  for (const record of records) {
    if (record.tokens.length < 2) continue;
    const key = record.tokens.join(' ');
    const current = byKey.get(key);
    if (current) {
      current.duplicate_weight += record.duplicate_weight ?? 1;
      current.source_ids.push(...(record.source_ids ?? [record.id]));
      current.source_cisi.push(record.cisi);
    } else {
      byKey.set(key, {
        ...record,
        tokens: [...record.tokens],
        duplicate_weight: record.duplicate_weight ?? 1,
        source_ids: [...(record.source_ids ?? [record.id])],
        source_cisi: [record.cisi],
      });
    }
  }
  return [...byKey.values()].sort((a, b) => a.tokens.join(' ').localeCompare(b.tokens.join(' ')));
}

function chooseRepresentatives(groups, policyName) {
  return [...groups.values()].map((members, index) => {
    const representative = [...members].sort((a, b) => {
      const weightDiff = (b.duplicate_weight ?? 1) - (a.duplicate_weight ?? 1);
      if (weightDiff) return weightDiff;
      return a.tokens.join(' ').localeCompare(b.tokens.join(' '));
    })[0];
    return {
      ...representative,
      id: `${policyName}_${String(index + 1).padStart(5, '0')}`,
      tokens: [...representative.tokens],
      duplicate_weight: representative.duplicate_weight ?? 1,
      family_size: members.length,
      family_source_weight: members.reduce((sum, member) => sum + (member.duplicate_weight ?? 1), 0),
      collapsed_member_ids: members.flatMap((member) => member.source_ids ?? [member.id]),
      collapsed_member_cisi: members.flatMap((member) => member.source_cisi ?? [member.cisi]),
      collapsed_member_texts: [...new Set(members.map((member) => member.text))],
    };
  });
}

class UnionFind {
  constructor(size) {
    this.parent = Array.from({ length: size }, (_, index) => index);
    this.rank = Array.from({ length: size }, () => 0);
  }
  find(value) {
    if (this.parent[value] !== value) this.parent[value] = this.find(this.parent[value]);
    return this.parent[value];
  }
  union(a, b) {
    const ra = this.find(a);
    const rb = this.find(b);
    if (ra === rb) return;
    if (this.rank[ra] < this.rank[rb]) {
      this.parent[ra] = rb;
    } else if (this.rank[ra] > this.rank[rb]) {
      this.parent[rb] = ra;
    } else {
      this.parent[rb] = ra;
      this.rank[ra]++;
    }
  }
}

function oneEditFamilyCollapse(records) {
  const uf = new UnionFind(records.length);
  const signatureToFirst = new Map();
  const addSignature = (signature, index) => {
    const first = signatureToFirst.get(signature);
    if (first === undefined) {
      signatureToFirst.set(signature, index);
    } else {
      uf.union(first, index);
    }
  };

  records.forEach((record, index) => {
    const tokens = record.tokens;
    for (let pos = 0; pos < tokens.length; pos++) {
      const wildcard = [...tokens];
      wildcard[pos] = '*';
      addSignature(`wild:${tokens.length}:${wildcard.join(' ')}`, index);
      const deleted = tokens.filter((_, tokenIndex) => tokenIndex !== pos);
      addSignature(`del:${tokens.length - 1}:${deleted.join(' ')}`, index);
    }
  });

  const groups = new Map();
  records.forEach((record, index) => {
    const rootIndex = uf.find(index);
    if (!groups.has(rootIndex)) groups.set(rootIndex, []);
    groups.get(rootIndex).push(record);
  });
  return chooseRepresentatives(groups, 'one_edit_family');
}

function topEdgeRemoved(records, topN = 10) {
  const edgeCounts = new Map();
  for (const record of records) {
    const first = record.tokens[0];
    const last = record.tokens[record.tokens.length - 1];
    edgeCounts.set(first, (edgeCounts.get(first) ?? 0) + 1);
    edgeCounts.set(last, (edgeCounts.get(last) ?? 0) + 1);
  }
  const topEdges = [...edgeCounts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, topN);
  const top = new Set(topEdges.map(([token]) => token));
  return {
    records: records.filter((record) => !top.has(record.tokens[0]) && !top.has(record.tokens[record.tokens.length - 1])),
    top_edges: topEdges.map(([token, count]) => ({ token, count })),
  };
}

function loadHarshRecords() {
  const candidates = loadCsv(inputRows)
    .filter((row) => row.readiness_bucket === 'lipi_numeric_clean_candidate')
    .map((row, index) => ({
      id: row.id || `ivc_${index + 1}`,
      cisi: normalize(row.cisi),
      region: normalize(row.region),
      site: normalize(row.site),
      type: normalize(row.type),
      material: normalize(row.material),
      symbol: normalize(row.symbol),
      direction: normalize(row.direction),
      class: normalize(row.class),
      text: row.text,
      tokens: parseTokens(row.text),
      duplicate_weight: 1,
    }))
    .filter((row) => row.tokens.length >= 2);
  const exact = exactCollapse(candidates);
  const top10 = topEdgeRemoved(exact, 10);
  const harsh = oneEditFamilyCollapse(top10.records);
  return { candidates, exact, top10Records: top10.records, topEdges: top10.top_edges, harsh };
}

function siteTypeSymbolKey(record) {
  return [normalize(record.site), normalize(record.type), normalize(record.symbol)].join('|');
}

function groupBy(records, keyFn) {
  const groups = new Map();
  for (const record of records) {
    const key = keyFn(record);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(record);
  }
  return groups;
}

function scopeDefinitions(harsh) {
  return [
    { scope: 'all_harsh', records: harsh },
    { scope: 'Mohenjo_daro_only', records: harsh.filter((record) => record.site === 'Mohenjo-daro') },
    { scope: 'Harappa_only', records: harsh.filter((record) => record.site === 'Harappa') },
    {
      scope: 'Mohenjo_daro_and_Harappa_only',
      records: harsh.filter((record) => record.site === 'Mohenjo-daro' || record.site === 'Harappa'),
    },
  ];
}

function publicScore(score) {
  return {
    rows: score.rows,
    tokens: score.tokens,
    unique_tokens: score.unique_tokens,
    stored_higher: score.stored_higher,
    reversed_higher: score.reversed_higher,
    ties: score.ties,
    stored_win_share: round(score.stored_win_share),
    mean_stored_minus_reversed_per_transition: round(score.mean_stored_minus_reversed_per_transition),
    median_stored_minus_reversed_per_transition: round(score.median_stored_minus_reversed_per_transition),
    total_stored_minus_reversed: round(score.total_stored_minus_reversed),
  };
}

function rankRowInfluence(scope, records, baseline) {
  const detailedBaseline = scoreDirection(records, { includeRowScores: true });
  const rowScoreById = new Map(detailedBaseline.row_scores.map((rowScore) => [rowScore.record.id, rowScore]));
  const totalDiff = detailedBaseline.total_stored_minus_reversed || 0;
  return records.map((record) => {
    const without = scoreDirection(records.filter((candidate) => candidate.id !== record.id));
    const rowScore = rowScoreById.get(record.id);
    return {
      scope,
      rank_metric: round(baseline.stored_win_share - without.stored_win_share),
      id: record.id,
      cisi: record.cisi,
      site: record.site,
      type: record.type,
      material: record.material,
      symbol: record.symbol,
      direction: record.direction,
      text: record.text,
      tokens: record.tokens.join(' '),
      token_count: record.tokens.length,
      family_key: siteTypeSymbolKey(record),
      one_edit_family_size: record.family_size ?? 1,
      one_edit_family_source_weight: record.family_source_weight ?? record.duplicate_weight ?? 1,
      stored_log_prob: round(rowScore?.stored_log_prob),
      reversed_log_prob: round(rowScore?.reversed_log_prob),
      row_stored_minus_reversed_total: round(rowScore?.stored_minus_reversed_total),
      row_stored_minus_reversed_per_transition: round(rowScore?.stored_minus_reversed_per_transition),
      row_outcome: rowScore?.row_outcome ?? '',
      row_diff_share_of_scope_total: totalDiff ? round((rowScore?.stored_minus_reversed_total ?? 0) / totalDiff) : 0,
      baseline_rows: baseline.rows,
      without_rows: without.rows,
      baseline_stored_win_share: round(baseline.stored_win_share),
      without_stored_win_share: round(without.stored_win_share),
      delta_stored_win_share: round(baseline.stored_win_share - without.stored_win_share),
      baseline_mean_diff: round(baseline.mean_stored_minus_reversed_per_transition),
      without_mean_diff: round(without.mean_stored_minus_reversed_per_transition),
      delta_mean_diff: round(baseline.mean_stored_minus_reversed_per_transition - without.mean_stored_minus_reversed_per_transition),
    };
  }).sort((a, b) =>
    Math.abs(b.delta_stored_win_share) - Math.abs(a.delta_stored_win_share)
    || Math.abs(b.delta_mean_diff) - Math.abs(a.delta_mean_diff)
    || String(a.cisi).localeCompare(String(b.cisi)),
  ).map((row, index) => ({ influence_rank: index + 1, ...row }));
}

function rankFamilyInfluence(scope, records, baseline) {
  const groups = groupBy(records, siteTypeSymbolKey);
  return [...groups.entries()].map(([familyKey, members]) => {
    const memberIds = new Set(members.map((record) => record.id));
    const without = scoreDirection(records.filter((record) => !memberIds.has(record.id)));
    return {
      scope,
      rank_metric: round(baseline.stored_win_share - without.stored_win_share),
      family_scheme: 'site|type|symbol',
      family_key: familyKey,
      representative_sites: [...new Set(members.map((record) => record.site))].sort().join('; '),
      representative_types: [...new Set(members.map((record) => record.type))].sort().join('; '),
      representative_symbols: [...new Set(members.map((record) => record.symbol))].sort().join('; '),
      rows_removed: members.length,
      source_weight_removed: members.reduce((sum, record) => sum + (record.family_source_weight ?? record.duplicate_weight ?? 1), 0),
      cisi: members.map((record) => record.cisi).sort().join('; '),
      texts: [...new Set(members.map((record) => record.text))].sort().join('; '),
      tokens: [...new Set(members.map((record) => record.tokens.join(' ')))].sort().join('; '),
      baseline_rows: baseline.rows,
      without_rows: without.rows,
      baseline_stored_win_share: round(baseline.stored_win_share),
      without_stored_win_share: round(without.stored_win_share),
      delta_stored_win_share: round(baseline.stored_win_share - without.stored_win_share),
      baseline_mean_diff: round(baseline.mean_stored_minus_reversed_per_transition),
      without_mean_diff: round(without.mean_stored_minus_reversed_per_transition),
      delta_mean_diff: round(baseline.mean_stored_minus_reversed_per_transition - without.mean_stored_minus_reversed_per_transition),
    };
  }).sort((a, b) =>
    Math.abs(b.delta_stored_win_share) - Math.abs(a.delta_stored_win_share)
    || Math.abs(b.delta_mean_diff) - Math.abs(a.delta_mean_diff)
    || a.family_key.localeCompare(b.family_key),
  ).map((row, index) => ({ influence_rank: index + 1, ...row }));
}

function influenceUnitLabel(row) {
  if (!row) return '';
  if (row.family_scheme) return row.family_key;
  return row.cisi || row.id || row.family_key || '';
}

function concentrationSummary(rows, baselineRows) {
  const supportive = rows.filter((row) => row.delta_stored_win_share > 0);
  const adverse = rows.filter((row) => row.delta_stored_win_share < 0);
  const topSupportive = supportive.slice().sort((a, b) => b.delta_stored_win_share - a.delta_stored_win_share)[0];
  const topAdverse = adverse.slice().sort((a, b) => a.delta_stored_win_share - b.delta_stored_win_share)[0];
  const topAbsolute = rows.slice().sort((a, b) =>
    Math.abs(b.delta_stored_win_share) - Math.abs(a.delta_stored_win_share)
    || Math.abs(b.delta_mean_diff) - Math.abs(a.delta_mean_diff),
  )[0];
  return {
    tested_units: rows.length,
    baseline_rows: baselineRows,
    top_supportive_delta_stored_win_share: topSupportive?.delta_stored_win_share ?? 0,
    top_supportive_unit: influenceUnitLabel(topSupportive),
    top_adverse_delta_stored_win_share: topAdverse?.delta_stored_win_share ?? 0,
    top_adverse_unit: influenceUnitLabel(topAdverse),
    max_absolute_delta_stored_win_share: topAbsolute ? round(Math.abs(topAbsolute.delta_stored_win_share)) : 0,
    max_absolute_delta_mean_diff: topAbsolute ? round(Math.abs(topAbsolute.delta_mean_diff)) : 0,
    max_absolute_unit: influenceUnitLabel(topAbsolute),
    top_5_abs_delta_sum: round(rows.slice(0, 5).reduce((sum, row) => sum + Math.abs(row.delta_stored_win_share), 0)),
  };
}

function summarizeScope(scope, records, baseline, rowRows, familyRows) {
  const rowsForScope = rowRows.filter((row) => row.scope === scope);
  const familiesForScope = familyRows.filter((row) => row.scope === scope);
  return {
    score: publicScore(baseline),
    row_influence: concentrationSummary(rowsForScope, baseline.rows),
    family_influence: concentrationSummary(familiesForScope, baseline.rows),
    largest_supportive_rows: rowsForScope
      .filter((row) => row.delta_stored_win_share > 0)
      .sort((a, b) => b.delta_stored_win_share - a.delta_stored_win_share)
      .slice(0, 5)
      .map((row) => ({
        cisi: row.cisi,
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        text: row.text,
        delta_stored_win_share: row.delta_stored_win_share,
        delta_mean_diff: row.delta_mean_diff,
      })),
    largest_supportive_families: familiesForScope
      .filter((row) => row.delta_stored_win_share > 0)
      .sort((a, b) => b.delta_stored_win_share - a.delta_stored_win_share)
      .slice(0, 5)
      .map((row) => ({
        family_key: row.family_key,
        rows_removed: row.rows_removed,
        delta_stored_win_share: row.delta_stored_win_share,
        delta_mean_diff: row.delta_mean_diff,
      })),
  };
}

const { candidates, exact, top10Records, topEdges, harsh } = loadHarshRecords();
const scopes = scopeDefinitions(harsh);
const baselines = new Map(scopes.map((scope) => [scope.scope, scoreDirection(scope.records)]));
const allRowInfluence = scopes.flatMap((scope) => rankRowInfluence(scope.scope, scope.records, baselines.get(scope.scope)));
const allFamilyInfluence = scopes.flatMap((scope) => rankFamilyInfluence(scope.scope, scope.records, baselines.get(scope.scope)));

const rowColumns = [
  'scope',
  'influence_rank',
  'id',
  'cisi',
  'site',
  'type',
  'material',
  'symbol',
  'direction',
  'text',
  'tokens',
  'token_count',
  'family_key',
  'one_edit_family_size',
  'one_edit_family_source_weight',
  'stored_log_prob',
  'reversed_log_prob',
  'row_stored_minus_reversed_total',
  'row_stored_minus_reversed_per_transition',
  'row_outcome',
  'row_diff_share_of_scope_total',
  'baseline_rows',
  'without_rows',
  'baseline_stored_win_share',
  'without_stored_win_share',
  'delta_stored_win_share',
  'baseline_mean_diff',
  'without_mean_diff',
  'delta_mean_diff',
];

const familyColumns = [
  'scope',
  'influence_rank',
  'family_scheme',
  'family_key',
  'representative_sites',
  'representative_types',
  'representative_symbols',
  'rows_removed',
  'source_weight_removed',
  'cisi',
  'texts',
  'tokens',
  'baseline_rows',
  'without_rows',
  'baseline_stored_win_share',
  'without_stored_win_share',
  'delta_stored_win_share',
  'baseline_mean_diff',
  'without_mean_diff',
  'delta_mean_diff',
];

fs.writeFileSync(outRowInfluence, toCsv(allRowInfluence, rowColumns));
fs.writeFileSync(outFamilyInfluence, toCsv(allFamilyInfluence, familyColumns));

const scopeSummaries = Object.fromEntries(scopes.map((scope) => [
  scope.scope,
  summarizeScope(scope.scope, scope.records, baselines.get(scope.scope), allRowInfluence, allFamilyInfluence),
]));

const allFamilySummary = scopeSummaries.all_harsh.family_influence;
const skepticalNote = allFamilySummary.max_absolute_delta_stored_win_share >= 0.05
  ? 'The all-harsh score shows nontrivial family sensitivity. Treat the result as concentrated until source-normalized acquisition confirms that the high-influence families are not transcription, register, or provenance artifacts.'
  : 'The all-harsh score is not controlled by one row or one site|type|symbol family under this diagnostic. The largest single-family removal changes stored-win share by less than five percentage points, but this remains structural evidence only.';

const summary = {
  date: DATE,
  generated_at_utc: new Date().toISOString(),
  purpose: 'Independent influence and concentration controls for the harsh effective-unicity directionality result.',
  source_scope: {
    input: 'data/open_prototype/reports/lipi_scope_rows.csv',
    candidate_filter: 'readiness_bucket == lipi_numeric_clean_candidate and parsed token count >= 2',
    reconstruction: 'exact-collapse, top10 edge removal, one-edit family collapse',
    candidate_rows: candidates.length,
    exact_sequence_collapsed_rows: exact.length,
    top10_edge_removed_exact_rows: top10Records.length,
    harsh_rows: harsh.length,
    top_removed_edge_tokens: topEdges,
  },
  method: {
    scoring: 'Add-alpha leave-one-row-out bigram score of stored order versus reversed order, matching the current directionality comparator family.',
    alpha: ALPHA,
    row_influence: 'Remove one harsh row from the scope, recompute aggregate stored-win share and mean stored-minus-reversed score, then rank by absolute delta.',
    family_influence: 'Remove each site|type|symbol family from the scope, recompute aggregate scores, then rank by absolute delta.',
    interpretation_boundary: 'This is a concentration diagnostic only. It does not validate source-image direction, semantics, phonetics, or accepted claims.',
  },
  baseline_scores: Object.fromEntries(scopes.map((scope) => [scope.scope, publicScore(baselines.get(scope.scope))])),
  concentration: scopeSummaries,
  skeptic_note: skepticalNote,
  artifact_files: [
    'data/open_prototype/tools/effective_unicity_directionality_influence_controls.mjs',
    'data/open_prototype/reports/effective_unicity_directionality_influence_controls_summary.json',
    'data/open_prototype/reports/effective_unicity_directionality_influence_rows.csv',
    'data/open_prototype/reports/effective_unicity_directionality_influence_families.csv',
    'docs/effective_unicity_directionality_influence_controls.md',
  ],
};

fs.writeFileSync(outSummary, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify({
  harsh_rows: harsh.length,
  baseline_scores: summary.baseline_scores,
  all_harsh_top_family_delta: allFamilySummary.max_absolute_delta_stored_win_share,
  outputs: summary.artifact_files.slice(0, 4),
}, null, 2));
