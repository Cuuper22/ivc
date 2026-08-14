// Tests whether sign `740` is the corpus's main "precedence hub": the sign that
// reliably comes before the largest number of other signs, i.e. a broad default
// header rather than a carrier-specific semantic sign. The script reads
// metadata_filtered.csv, collapses duplicate sign sequences, and builds a directed
// order graph: for every sign pair sharing at least 50 rows, an edge qualifies if
// one order dominates in at least 80% of rows with binomial p <= 0.001. Signs are
// ranked by qualified outgoing edges, and 740's rank is checked in seven pools
// (all rows, complete only, non-poor, leave-Harappa, leave-Mohenjo-daro, square
// seals only, account/rectangular register only). A 1,500-iteration forger
// shuffles the signs inside each row and asks how often any sign accumulates as
// many outgoing edges as 740 (max-stat). Writes a bet summary (JSON + CSV) plus
// pool, edge, hub, support-row, and forger-iteration CSVs to the reports directory.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_740_precedence_hub_forger_20260531';
const RUN_DATE = '2026-05-31';
const TARGET = '740';
const MIN_PAIR_ROWS = 50;
const MIN_SHARE = 0.8;
const MAX_P = 0.001;
const ITERATIONS = 1500;

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = '';
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (ch === '"' && next === '"') {
        cell += '"';
        i += 1;
      } else if (ch === '"') {
        quoted = false;
      } else {
        cell += ch;
      }
    } else if (ch === '"') {
      quoted = true;
    } else if (ch === ',') {
      row.push(cell);
      cell = '';
    } else if (ch === '\n') {
      row.push(cell.replace(/\r$/, ''));
      if (row.some((value) => value.length)) rows.push(row);
      row = [];
      cell = '';
    } else {
      cell += ch;
    }
  }
  if (cell.length || row.length) {
    row.push(cell.replace(/\r$/, ''));
    if (row.some((value) => value.length)) rows.push(row);
  }
  const [header, ...body] = rows;
  return body.map((cols) => Object.fromEntries(header.map((name, idx) => [name, cols[idx] ?? ''])));
}

function writeCsv(file, rows, fields) {
  const esc = (value) => {
    const text = String(value ?? '');
    return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
  };
  const body = rows.map((row) => fields.map((field) => esc(row[field])).join(',')).join('\n');
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`, 'utf8');
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function norm(value, fallback = 'NA') {
  const text = String(value ?? '').trim();
  return text && text !== '-' && text !== 'None' && text !== '--' ? text : fallback;
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

const binomCache = new Map();
function binomialRightTail(k, n, p = 0.5) {
  const key = `${k}|${n}|${p}`;
  if (binomCache.has(key)) return binomCache.get(key);
  let prob = 0;
  for (let x = k; x <= n; x += 1) {
    let logComb = 0;
    for (let i = 1; i <= x; i += 1) logComb += Math.log((n - x + i) / i);
    prob += Math.exp(logComb + x * Math.log(p) + (n - x) * Math.log(1 - p));
  }
  const clipped = Math.max(0, Math.min(1, prob));
  binomCache.set(key, clipped);
  return clipped;
}

function mulberry32(seed) {
  return function rand() {
    let t = (seed += 0x6D2B79F5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffleInPlace(arr, rand) {
  for (let i = arr.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    const tmp = arr[i];
    arr[i] = arr[j];
    arr[j] = tmp;
  }
}

function pairDirectionRows(rows) {
  const pairMap = new Map();
  for (const row of rows) {
    const firstPos = new Map();
    row.signs.forEach((sign, idx) => {
      if (!firstPos.has(sign)) firstPos.set(sign, idx);
    });
    const unique = [...firstPos.keys()].sort();
    for (let i = 0; i < unique.length; i += 1) {
      for (let j = i + 1; j < unique.length; j += 1) {
        const a = unique[i];
        const b = unique[j];
        const key = `${a}|${b}`;
        if (!pairMap.has(key)) pairMap.set(key, { a, b, n: 0, a_before_b: 0 });
        const rec = pairMap.get(key);
        rec.n += 1;
        if (firstPos.get(a) < firstPos.get(b)) rec.a_before_b += 1;
      }
    }
  }
  const directed = [];
  for (const rec of pairMap.values()) {
    if (rec.n < MIN_PAIR_ROWS) continue;
    const aBefore = rec.a_before_b;
    const bBefore = rec.n - rec.a_before_b;
    const left = aBefore >= bBefore ? rec.a : rec.b;
    const right = aBefore >= bBefore ? rec.b : rec.a;
    const dominant = Math.max(aBefore, bBefore);
    const share = dominant / rec.n;
    const p = binomialRightTail(dominant, rec.n);
    directed.push({
      left,
      right,
      pair: `${rec.a}|${rec.b}`,
      n: rec.n,
      dominant_count: dominant,
      opposite_count: rec.n - dominant,
      dominant_share: share,
      binomial_p: p,
    });
  }
  return directed.sort((a, b) => a.binomial_p - b.binomial_p || b.dominant_share - a.dominant_share || b.n - a.n);
}

function hubStats(rows) {
  const directed = pairDirectionRows(rows);
  const qualified = directed.filter((row) => row.dominant_share >= MIN_SHARE && row.binomial_p <= MAX_P);
  const byLeft = new Map();
  for (const edge of qualified) {
    if (!byLeft.has(edge.left)) byLeft.set(edge.left, []);
    byLeft.get(edge.left).push(edge);
  }
  const hubs = [...byLeft.entries()].map(([sign, edges]) => ({
    sign,
    out_edges: edges.length,
    total_edge_rows: edges.reduce((sum, edge) => sum + edge.n, 0),
    min_edge_p: Math.min(...edges.map((edge) => edge.binomial_p)),
  })).sort((a, b) => b.out_edges - a.out_edges || b.total_edge_rows - a.total_edge_rows || a.sign.localeCompare(b.sign, undefined, { numeric: true }));
  const target = hubs.find((row) => row.sign === TARGET) ?? { sign: TARGET, out_edges: 0, total_edge_rows: 0, min_edge_p: 1 };
  const targetEdges = (byLeft.get(TARGET) ?? []).sort((a, b) => a.binomial_p - b.binomial_p || b.n - a.n);
  return {
    directed,
    qualified,
    hubs,
    target,
    target_rank: `${hubs.findIndex((row) => row.sign === TARGET) + 1}/${hubs.length}`,
    target_edges: targetEdges,
  };
}

function forger(rows, observedOutEdges, iterations = ITERATIONS) {
  const rand = mulberry32(0x740111 ^ rows.length);
  let maxGe = 0;
  const iterationRows = [];
  for (let iter = 0; iter < iterations; iter += 1) {
    const fakeRows = rows.map((row) => {
      const signs = row.signs.slice();
      shuffleInPlace(signs, rand);
      return { ...row, signs };
    });
    const stats = hubStats(fakeRows);
    const best = stats.hubs[0] ?? { sign: '', out_edges: 0, total_edge_rows: 0 };
    if (best.out_edges >= observedOutEdges) maxGe += 1;
    if (iter < 50 || best.out_edges >= observedOutEdges) {
      iterationRows.push({
        iteration: iter,
        best_sign: best.sign,
        best_out_edges: best.out_edges,
        best_total_edge_rows: best.total_edge_rows,
        ge_observed: String(best.out_edges >= observedOutEdges),
      });
    }
  }
  return { iterations, maxstat_fpr: maxGe / iterations, iteration_rows: iterationRows };
}

function analyzePool(name, rows) {
  const stats = hubStats(rows);
  return {
    pool: name,
    rows: rows.length,
    directed_pairs: stats.directed.length,
    qualified_edges: stats.qualified.length,
    target_rank: stats.target_rank,
    target_out_edges: stats.target.out_edges,
    target_total_edge_rows: stats.target.total_edge_rows,
    target_min_edge_p: stats.target.min_edge_p,
    top_hubs: stats.hubs.slice(0, 15),
    target_edges: stats.target_edges,
  };
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()]
  .filter((row) => row.signs.length > 1);

const pools = [
  analyzePool('all_canonical', canonicalRows),
  analyzePool('complete_only', canonicalRows.filter((row) => norm(row.complete) === 'Y')),
  analyzePool('non_poor_only', canonicalRows.filter((row) => norm(row.condition) !== 'Poor')),
  analyzePool('without_harappa', canonicalRows.filter((row) => norm(row.site) !== 'Harappa')),
  analyzePool('without_mohenjo_daro', canonicalRows.filter((row) => norm(row.site) !== 'Mohenjo-daro')),
  analyzePool('square_seal_only', canonicalRows.filter((row) => norm(row.type) === 'SEAL:S')),
  analyzePool('account_or_rect_register_only', canonicalRows.filter((row) => ['TAB:B', 'TAB:I', 'SEAL:R', 'TAB:C'].includes(norm(row.type)))),
];
const main = pools[0];
const nulls = forger(canonicalRows, main.target_out_edges);
const controlsPassing = pools.slice(1, 5).filter((pool) => pool.target_out_edges >= 8 && pool.target_rank.startsWith('1/')).length;
const supportRows = canonicalRows.filter((row) => row.signs.includes(TARGET)).map((row) => ({
  object: objectId(row),
  site: norm(row.site),
  region: norm(row.region),
  type: norm(row.type),
  material: norm(row.material),
  shape: norm(row.shape),
  symbol: norm(row.symbol),
  condition: norm(row.condition),
  complete: norm(row.complete),
  first_sign: row.signs[0] ?? '',
  target_position: row.signs.indexOf(TARGET),
  text: row.text,
}));

const tier =
  main.target_rank.startsWith('1/') &&
  main.target_out_edges >= 10 &&
  nulls.maxstat_fpr <= 0.01 &&
  controlsPassing >= 3
    ? 'promoted candidate'
    : 'candidate';

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V2_V4_740_PRECEDENCE_HUB_20260531',
  vector: 'V2 slot grammar; V4 context-to-meaning without sound',
  confidence_tier: tier,
  risky_bet:
    '`740` is the main left-edge/preposed header hub in the sign-order graph. It is not a carrier-specific semantic sign by itself; it precedes many other signs as a broad default header, while narrower registers can place stronger frame signs such as `400` before it.',
  observed:
    `All canonical: ${TARGET} rank ${main.target_rank} among precedence hubs with ${main.target_out_edges} qualified outgoing edges and ${main.target_total_edge_rows} total edge rows. Row-internal shuffle maxstat FPR=${nulls.maxstat_fpr}. Controls passing=${controlsPassing}/4. Top target edges: ${main.target_edges.slice(0, 12).map((edge) => `${TARGET}->${edge.right}:${edge.dominant_count}/${edge.n},p=${edge.binomial_p}`).join(';')}.`,
  adversarial_test:
    `Canonical numeric-sequence collapse; all co-occurring pair direction scan requiring n>=${MIN_PAIR_ROWS}, dominant share>=${MIN_SHARE}, p<=${MAX_P}; ${ITERATIONS}-iteration row-internal sign-shuffle forger preserving each row's signs and all row-level co-occurrences; complete-only, non-poor-only, leave-Harappa, leave-Mohenjo, square-seal-only, and account/rectangular-register controls.`,
  false_positive_rate: nulls.maxstat_fpr,
  target_out_edges: main.target_out_edges,
  target_total_edge_rows: main.target_total_edge_rows,
  controls_passing: controlsPassing,
  falsifier:
    'If source-checked rows reduce 740 outgoing precedence below other hubs, or if the row-internal shuffle routinely creates equivalent hubs, demote 740 from default header to a frequent sign with accidental position.',
  next_prediction:
    'New rows containing 740 and any of its high-support partners should usually place 740 before that partner, unless a stronger frame opener such as 400 in tablet-account rows precedes 740.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({
    ...summary,
    pools: pools.map((pool) => ({
      pool: pool.pool,
      rows: pool.rows,
      directed_pairs: pool.directed_pairs,
      qualified_edges: pool.qualified_edges,
      target_rank: pool.target_rank,
      target_out_edges: pool.target_out_edges,
      target_total_edge_rows: pool.target_total_edge_rows,
      target_min_edge_p: pool.target_min_edge_p,
      top_hubs: pool.top_hubs,
      target_edges: pool.target_edges,
    })),
    forger: { iterations: nulls.iterations, maxstat_fpr: nulls.maxstat_fpr },
    support_rows: supportRows,
  }, null, 2),
  'utf8',
);
writeCsv(path.join(OUT_DIR, `${PREFIX}.csv`), [summary], [
  'run_date',
  'bet_id',
  'vector',
  'confidence_tier',
  'risky_bet',
  'observed',
  'adversarial_test',
  'false_positive_rate',
  'target_out_edges',
  'target_total_edge_rows',
  'controls_passing',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_pools.csv`), pools.map((pool) => ({
  pool: pool.pool,
  rows: pool.rows,
  directed_pairs: pool.directed_pairs,
  qualified_edges: pool.qualified_edges,
  target_rank: pool.target_rank,
  target_out_edges: pool.target_out_edges,
  target_total_edge_rows: pool.target_total_edge_rows,
  target_min_edge_p: pool.target_min_edge_p,
})), [
  'pool',
  'rows',
  'directed_pairs',
  'qualified_edges',
  'target_rank',
  'target_out_edges',
  'target_total_edge_rows',
  'target_min_edge_p',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_target_edges.csv`), main.target_edges, [
  'left',
  'right',
  'pair',
  'n',
  'dominant_count',
  'opposite_count',
  'dominant_share',
  'binomial_p',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_top_hubs.csv`), main.top_hubs, [
  'sign',
  'out_edges',
  'total_edge_rows',
  'min_edge_p',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_support_rows.csv`), supportRows, [
  'object',
  'site',
  'region',
  'type',
  'material',
  'shape',
  'symbol',
  'condition',
  'complete',
  'first_sign',
  'target_position',
  'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_forger_iterations.csv`), nulls.iteration_rows, [
  'iteration',
  'best_sign',
  'best_out_edges',
  'best_total_edge_rows',
  'ge_observed',
]);

console.log(JSON.stringify(summary, null, 2));
