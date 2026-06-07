import fs from 'fs';
import path from 'path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');

const sourceQueuePath = path.join(reportsDir, 'effective_unicity_directionality_source_queue.csv');
const routeStatusPath = path.join(reportsDir, 'effective_unicity_directionality_public_route_probe_status.csv');
const v2ePath = path.join(reportsDir, 'effective_unicity_directionality_signband_pool_v2e_candidates.csv');

const outSummary = path.join(reportsDir, 'effective_unicity_directionality_route_conditioned_control_summary.json');
const outRows = path.join(reportsDir, 'effective_unicity_directionality_route_conditioned_control.csv');
const outNullSummary = path.join(reportsDir, 'effective_unicity_directionality_route_conditioned_null_summary.csv');
const outNullIterations = path.join(reportsDir, 'effective_unicity_directionality_route_conditioned_null_iterations.csv');

const DATE = '2026-05-29';
const NULL_ITERATIONS = Number(process.argv.find((arg) => arg.startsWith('--iterations='))?.split('=')[1] ?? 5000);
const ROUTE_PROBE_ID = 'directionality_public_route_probe_v1';
const ROUTE_PRIORITY_BANDS = new Set(['P1_acquire_high_positive_source', 'P1_audit_reversed_anomaly']);
const V2E_SIGNBAND_BUCKETS = new Set([
  'strong_signband_like_geometry_needs_visual_qc',
  'possible_signband_like_geometry_needs_visual_qc',
]);

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
  return Number.isFinite(value) ? Number(value.toFixed(digits)) : null;
}

function number(value) {
  const n = Number(value);
  return Number.isFinite(n) ? n : 0;
}

function normalize(value) {
  return String(value || '-').trim() || '-';
}

function tokenCount(row) {
  return String(row.tokens || row.text || '').match(/\d{3}/g)?.length ?? 0;
}

function tokenBin(count) {
  if (count <= 3) return 'len_le_3';
  if (count <= 5) return 'len_4_5';
  return 'len_ge_6';
}

function outcomeValue(row) {
  return row.direction_outcome === 'stored_higher' ? 1 : 0;
}

function pageKey(row) {
  return `${normalize(row.best_volume)}|${normalize(row.best_page_index)}`;
}

function sourceConventionKey(row) {
  return [
    normalize(row.site),
    normalize(row.type),
    normalize(row.material),
    normalize(row.symbol),
    normalize(row.direction),
  ].join('|');
}

function sourceRegisterKey(row) {
  return [
    normalize(row.site),
    normalize(row.type),
    normalize(row.symbol),
    normalize(row.direction),
  ].join('|');
}

function groupBy(rows, keyFn) {
  const groups = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(row);
  }
  return groups;
}

function sortedRepresentative(rows) {
  return [...rows].sort((a, b) => {
    const rankDiff = number(a.queue_rank) - number(b.queue_rank);
    if (rankDiff) return rankDiff;
    return String(a.representative_cisi).localeCompare(String(b.representative_cisi));
  })[0];
}

function collapseRows(rows, keyFn, label) {
  return [...groupBy(rows, keyFn).entries()].map(([key, members]) => ({
    ...sortedRepresentative(members),
    collapsed_key: key,
    collapsed_policy: label,
    collapsed_member_count: members.length,
    collapsed_member_cisis: members.map((row) => row.representative_cisi).join(';'),
  }));
}

function summarizeRows(name, rows, note = '') {
  const stored = rows.filter((row) => row.direction_outcome === 'stored_higher').length;
  const reversed = rows.filter((row) => row.direction_outcome === 'reversed_higher').length;
  const ties = rows.filter((row) => row.direction_outcome === 'tie').length;
  const sites = Object.fromEntries([...groupBy(rows, (row) => row.site).entries()].map(([k, v]) => [k, v.length]).sort());
  const directions = Object.fromEntries([...groupBy(rows, (row) => row.direction).entries()].map(([k, v]) => [k, v.length]).sort());
  const pages = [...new Set(rows.filter((row) => row.best_volume || row.best_page_index).map(pageKey))].length;
  return {
    subset: name,
    rows: rows.length,
    stored_higher: stored,
    reversed_higher: reversed,
    ties,
    stored_win_share: rows.length ? round(stored / rows.length) : null,
    mean_diff_per_transition: rows.length ? round(rows.reduce((sum, row) => sum + number(row.diff_per_transition), 0) / rows.length) : null,
    route_rows: rows.filter((row) => row.is_public_route).length,
    no_route_rows: rows.filter((row) => !row.is_public_route).length,
    unique_cisis: new Set(rows.map((row) => row.representative_cisi)).size,
    source_pages: pages,
    sites,
    directions,
    note,
  };
}

function makeRandom(seed = 0x5eedc0de) {
  let state = seed >>> 0;
  return function random() {
    state = (Math.imul(state, 1664525) + 1013904223) >>> 0;
    return state / 2 ** 32;
  };
}

function shuffle(values, random) {
  const copy = [...values];
  for (let index = copy.length - 1; index > 0; index--) {
    const swapIndex = Math.floor(random() * (index + 1));
    [copy[index], copy[swapIndex]] = [copy[swapIndex], copy[index]];
  }
  return copy;
}

function routeLabelNull(rows, blockKeyFn, label) {
  const random = makeRandom(0x51a7e000 ^ label.length ^ rows.length);
  const observedRouteRows = rows.filter((row) => row.is_public_route);
  const observedNoRouteRows = rows.filter((row) => !row.is_public_route);
  const observedRouteShare = observedRouteRows.length
    ? observedRouteRows.reduce((sum, row) => sum + outcomeValue(row), 0) / observedRouteRows.length
    : 0;
  const observedNoRouteShare = observedNoRouteRows.length
    ? observedNoRouteRows.reduce((sum, row) => sum + outcomeValue(row), 0) / observedNoRouteRows.length
    : 0;
  const observedDiff = observedRouteShare - observedNoRouteShare;

  const groups = groupBy(rows, blockKeyFn);
  const iterations = [];
  let geRouteShare = 0;
  let geDiff = 0;
  let geAbsDiff = 0;
  let usableIterations = 0;

  for (let iteration = 0; iteration < NULL_ITERATIONS; iteration++) {
    const assigned = [];
    for (const members of groups.values()) {
      const labels = shuffle(members.map((row) => row.is_public_route), random);
      members.forEach((row, index) => {
        assigned.push({ row, is_public_route: labels[index] });
      });
    }
    const route = assigned.filter((item) => item.is_public_route);
    const noRoute = assigned.filter((item) => !item.is_public_route);
    if (!route.length || !noRoute.length) continue;
    usableIterations++;
    const routeShare = route.reduce((sum, item) => sum + outcomeValue(item.row), 0) / route.length;
    const noRouteShare = noRoute.reduce((sum, item) => sum + outcomeValue(item.row), 0) / noRoute.length;
    const diff = routeShare - noRouteShare;
    if (routeShare >= observedRouteShare - 1e-12) geRouteShare++;
    if (diff >= observedDiff - 1e-12) geDiff++;
    if (Math.abs(diff) >= Math.abs(observedDiff) - 1e-12) geAbsDiff++;
    iterations.push({
      null_label: label,
      iteration,
      route_share: round(routeShare),
      no_route_share: round(noRouteShare),
      diff_route_minus_no_route: round(diff),
    });
  }

  return {
    summary: {
      null_label: label,
      block_count: groups.size,
      rows: rows.length,
      route_rows: observedRouteRows.length,
      no_route_rows: observedNoRouteRows.length,
      observed_route_share: round(observedRouteShare),
      observed_no_route_share: round(observedNoRouteShare),
      observed_diff_route_minus_no_route: round(observedDiff),
      iterations: usableIterations,
      null_ge_observed_route_share: usableIterations ? round(geRouteShare / usableIterations) : null,
      null_ge_observed_diff: usableIterations ? round(geDiff / usableIterations) : null,
      null_ge_abs_observed_diff: usableIterations ? round(geAbsDiff / usableIterations) : null,
    },
    iterations,
  };
}

function annotateRows(statusRows, queueByCisi, v2eCisis) {
  return statusRows.map((row) => {
    const queueRow = queueByCisi.get(row.representative_cisi) ?? {};
    const count = tokenCount(row);
    return {
      ...row,
      material: queueRow.material || '',
      cult: queueRow.cult || '',
      token_count: count,
      token_count_bin: tokenBin(count),
      is_public_route: row.source_status_rank === 'public_cisi_plate_route_candidate',
      is_v2e_possible_or_strong: v2eCisis.has(row.representative_cisi),
      page_key: pageKey(row),
      source_convention_key: sourceConventionKey({ ...row, material: queueRow.material || '' }),
    };
  });
}

const sourceQueue = loadCsv(sourceQueuePath);
const routeStatus = loadCsv(routeStatusPath);
const v2e = loadCsv(v2ePath);

const queueByCisi = new Map(sourceQueue.map((row) => [row.representative_cisi, row]));
const v2eCisis = new Set(v2e
  .filter((row) => V2E_SIGNBAND_BUCKETS.has(row.signband_like_bucket))
  .map((row) => row.cisi));

const allMajorHarshRows = sourceQueue.map((row) => ({
  ...row,
  is_public_route: false,
  is_v2e_possible_or_strong: false,
  token_count: tokenCount(row),
  token_count_bin: tokenBin(tokenCount(row)),
  page_key: '',
  source_convention_key: sourceConventionKey(row),
}));

const topProbeRows = annotateRows(routeStatus
  .filter((row) =>
    row.probe_id === ROUTE_PROBE_ID
    && ROUTE_PRIORITY_BANDS.has(row.priority_band)
    && number(row.queue_rank) <= 80)
  .sort((a, b) => number(a.queue_rank) - number(b.queue_rank)), queueByCisi, v2eCisis);

const publicRouteRows = topProbeRows.filter((row) => row.is_public_route);
const noPublicRouteRows = topProbeRows.filter((row) => !row.is_public_route);
const publicRoutePageCollapsed = collapseRows(publicRouteRows, pageKey, 'best_volume|best_page_index');
const publicRouteSourceRegisterCollapsed = collapseRows(publicRouteRows, sourceRegisterKey, 'site|type|symbol|direction');
const publicRouteSourceConventionCollapsed = collapseRows(publicRouteRows, sourceConventionKey, 'site|type|material|symbol|direction');
const v2eRows = publicRouteRows.filter((row) => row.is_v2e_possible_or_strong);
const v2ePageCollapsed = collapseRows(v2eRows, pageKey, 'best_volume|best_page_index');
const v2eSourceRegisterCollapsed = collapseRows(v2eRows, sourceRegisterKey, 'site|type|symbol|direction');
const v2eSourceConventionCollapsed = collapseRows(v2eRows, sourceConventionKey, 'site|type|material|symbol|direction');

const summaries = [
  summarizeRows('all_324_harsh_major_site_rows', allMajorHarshRows, 'Baseline source queue rows; not a route-conditioned subset.'),
  summarizeRows('top79_public_route_probe_rows', topProbeRows, 'Frozen public-route probe universe.'),
  summarizeRows('public_route_38_rows', publicRouteRows, 'Rows with public CISI plate-route candidates inside the frozen probe universe.'),
  summarizeRows('no_public_route_41_rows', noPublicRouteRows, 'Rows not found in public CISI OCR layer inside the frozen probe universe.'),
  summarizeRows('public_route_38_page_collapsed', publicRoutePageCollapsed, 'One deterministic representative per public CISI source page.'),
  summarizeRows('public_route_38_source_register_collapsed', publicRouteSourceRegisterCollapsed, 'One deterministic representative per site/type/symbol/direction source-register key.'),
  summarizeRows('public_route_38_source_convention_collapsed', publicRouteSourceConventionCollapsed, 'One deterministic representative per metadata source-convention key.'),
  summarizeRows('v2e_possible_or_strong_31_rows', v2eRows, 'Public-route rows that also have possible or strong signband-like v2e geometry.'),
  summarizeRows('v2e_possible_or_strong_page_collapsed', v2ePageCollapsed, 'v2e possible/strong rows collapsed by source page.'),
  summarizeRows('v2e_possible_or_strong_source_register_collapsed', v2eSourceRegisterCollapsed, 'v2e possible/strong rows collapsed by site/type/symbol/direction source-register key.'),
  summarizeRows('v2e_possible_or_strong_source_convention_collapsed', v2eSourceConventionCollapsed, 'v2e possible/strong rows collapsed by source-convention key.'),
];

const nullRuns = [
  routeLabelNull(topProbeRows, (row) => row.priority_band, 'route_label_shuffle__priority_band'),
  routeLabelNull(topProbeRows, (row) => [row.priority_band, row.site].join('|'), 'route_label_shuffle__priority_site'),
  routeLabelNull(topProbeRows, (row) => [row.priority_band, row.site, row.type].join('|'), 'route_label_shuffle__priority_site_type'),
  routeLabelNull(topProbeRows, (row) => [
    row.priority_band,
    row.site,
    row.type,
    row.symbol,
    row.direction,
    row.token_count_bin,
  ].join('|'), 'route_label_shuffle__priority_site_type_symbol_direction_lenbin'),
];

const nullSummaries = nullRuns.map((run) => run.summary);
const nullIterations = nullRuns.flatMap((run) => run.iterations);

const publicRouteShare = summaries.find((row) => row.subset === 'public_route_38_rows').stored_win_share;
const publicRoutePageShare = summaries.find((row) => row.subset === 'public_route_38_page_collapsed').stored_win_share;
const publicRouteRegisterShare = summaries.find((row) => row.subset === 'public_route_38_source_register_collapsed').stored_win_share;
const publicRouteConventionShare = summaries.find((row) => row.subset === 'public_route_38_source_convention_collapsed').stored_win_share;
const v2eRegisterShare = summaries.find((row) => row.subset === 'v2e_possible_or_strong_source_register_collapsed').stored_win_share;
const v2eConventionShare = summaries.find((row) => row.subset === 'v2e_possible_or_strong_source_convention_collapsed').stored_win_share;
const maxRouteNullGe = Math.max(...nullSummaries.map((row) => row.null_ge_observed_route_share ?? 0));

const failReasons = [];
if ((publicRouteShare ?? 0) < 0.7) failReasons.push('public_route_stored_win_share_below_0_70');
if ((publicRoutePageShare ?? 0) < 0.7) failReasons.push('page_collapsed_public_route_share_below_0_70');
if ((publicRouteRegisterShare ?? 0) < 0.7) failReasons.push('source_register_collapsed_public_route_share_below_0_70');
if ((publicRouteConventionShare ?? 0) < 0.7) failReasons.push('source_convention_collapsed_public_route_share_below_0_70');
if ((v2eRegisterShare ?? 0) < 0.7) failReasons.push('v2e_source_register_collapsed_share_below_0_70');
if ((v2eConventionShare ?? 0) < 0.7) failReasons.push('v2e_source_convention_collapsed_share_below_0_70');
if (maxRouteNullGe > 0.1) failReasons.push('route_label_null_reproduces_or_exceeds_observed_route_share');

const decision = failReasons.length
  ? 'failed_promotion_route_conditioned_subset_not_source_normalized_evidence'
  : 'survived_route_conditioned_gate_candidate_only';

const summary = {
  date: DATE,
  generated_at_utc: new Date().toISOString(),
  purpose: 'Route-conditioned control for the Vector 2 directionality candidate. Tests whether public CISI route availability or page/source-convention clustering can support a source-visible directionality promotion.',
  inputs: {
    source_queue: sourceQueuePath,
    public_route_probe_status: routeStatusPath,
    signband_pool_v2e_candidates: v2ePath,
  },
  frozen_subset_definition: {
    route_probe_id: ROUTE_PROBE_ID,
    priority_bands: [...ROUTE_PRIORITY_BANDS],
    max_queue_rank: 80,
    public_route_status_rank: 'public_cisi_plate_route_candidate',
    v2e_signband_buckets: [...V2E_SIGNBAND_BUCKETS],
  },
  controls: {
    null_iterations: NULL_ITERATIONS,
    route_label_nulls: nullSummaries.map((row) => row.null_label),
    collapses: [
      'best_volume|best_page_index',
      'site|type|material|symbol|direction',
    ],
    fail_gates: [
      'public route stored-win share < 0.70',
      'page-collapsed public route stored-win share < 0.70',
      'source-register-collapsed public route stored-win share < 0.70',
      'source-convention-collapsed public route stored-win share < 0.70',
      'v2e source-register-collapsed stored-win share < 0.70',
      'v2e source-convention-collapsed stored-win share < 0.70',
      'any matched route-label null reproduces observed route share at > 0.10',
    ],
  },
  primary_results: Object.fromEntries(summaries.map((row) => [row.subset, row])),
  null_summary: Object.fromEntries(nullSummaries.map((row) => [row.null_label, row])),
  decision,
  fail_reasons: failReasons,
  interpretation_boundary: 'This is a route-conditioned source-availability audit only. It does not validate physical source direction, source-normalized token order, sign identity, meaning, phonetics, language family, or translation.',
  accepted_claims_increment: 0,
  artifact_files: [
    'data/open_prototype/tools/effective_unicity_directionality_route_conditioned_control.mjs',
    'data/open_prototype/reports/effective_unicity_directionality_route_conditioned_control_summary.json',
    'data/open_prototype/reports/effective_unicity_directionality_route_conditioned_control.csv',
    'data/open_prototype/reports/effective_unicity_directionality_route_conditioned_null_summary.csv',
    'data/open_prototype/reports/effective_unicity_directionality_route_conditioned_null_iterations.csv',
  ],
};

const rowColumns = [
  'subset',
  'rows',
  'stored_higher',
  'reversed_higher',
  'ties',
  'stored_win_share',
  'mean_diff_per_transition',
  'route_rows',
  'no_route_rows',
  'unique_cisis',
  'source_pages',
  'note',
];
const nullColumns = [
  'null_label',
  'block_count',
  'rows',
  'route_rows',
  'no_route_rows',
  'observed_route_share',
  'observed_no_route_share',
  'observed_diff_route_minus_no_route',
  'iterations',
  'null_ge_observed_route_share',
  'null_ge_observed_diff',
  'null_ge_abs_observed_diff',
];
const iterationColumns = [
  'null_label',
  'iteration',
  'route_share',
  'no_route_share',
  'diff_route_minus_no_route',
];

fs.writeFileSync(outSummary, `${JSON.stringify(summary, null, 2)}\n`);
fs.writeFileSync(outRows, toCsv(summaries, rowColumns));
fs.writeFileSync(outNullSummary, toCsv(nullSummaries, nullColumns));
fs.writeFileSync(outNullIterations, toCsv(nullIterations, iterationColumns));

console.log(JSON.stringify({
  decision,
  fail_reasons: failReasons,
  public_route_38_share: publicRouteShare,
  public_route_page_collapsed_share: publicRoutePageShare,
  public_route_source_register_collapsed_share: publicRouteRegisterShare,
  public_route_source_convention_collapsed_share: publicRouteConventionShare,
  v2e_source_register_collapsed_share: v2eRegisterShare,
  v2e_source_convention_collapsed_share: v2eConventionShare,
  max_route_label_null_ge_observed_route_share: round(maxRouteNullGe),
}, null, 2));
