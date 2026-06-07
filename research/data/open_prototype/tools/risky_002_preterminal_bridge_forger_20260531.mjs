import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_002_preterminal_bridge_forger_20260531';
const RUN_DATE = '2026-05-31';
const TARGET = '002';
const TERMINAL_PARTNERS = new Set(['861', '820', '817']);
const MIN_PAIR_ROWS = 30;
const MIN_SHARE = 0.75;
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

function fisherRightTail(a, b, c, d) {
  const n = a + b + c + d;
  const logFact = [0];
  for (let i = 1; i <= n; i += 1) logFact[i] = logFact[i - 1] + Math.log(i);
  const logChoose = (nn, kk) => logFact[nn] - logFact[kk] - logFact[nn - kk];
  const row1 = a + b;
  const row2 = c + d;
  const col1 = a + c;
  const max = Math.min(row1, col1);
  const logDen = logChoose(n, col1);
  let p = 0;
  for (let x = a; x <= max; x += 1) p += Math.exp(logChoose(row1, x) + logChoose(row2, col1 - x) - logDen);
  return Math.max(0, Math.min(1, p));
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
    const bBefore = rec.n - aBefore;
    const left = aBefore >= bBefore ? rec.a : rec.b;
    const right = aBefore >= bBefore ? rec.b : rec.a;
    const dominant = Math.max(aBefore, bBefore);
    const share = dominant / rec.n;
    const p = binomialRightTail(dominant, rec.n);
    if (share >= MIN_SHARE && p <= MAX_P) {
      directed.push({ left, right, pair: `${rec.a}|${rec.b}`, n: rec.n, dominant_count: dominant, opposite_count: rec.n - dominant, dominant_share: share, binomial_p: p });
    }
  }
  return directed.sort((a, b) => a.binomial_p - b.binomial_p || b.n - a.n);
}

function bridgeStats(rows) {
  const edges = pairDirectionRows(rows);
  const bySign = new Map();
  for (const edge of edges) {
    if (!bySign.has(edge.left)) bySign.set(edge.left, { sign: edge.left, in_edges: 0, out_edges: 0, in_rows: 0, out_rows: 0 });
    if (!bySign.has(edge.right)) bySign.set(edge.right, { sign: edge.right, in_edges: 0, out_edges: 0, in_rows: 0, out_rows: 0 });
    const left = bySign.get(edge.left);
    const right = bySign.get(edge.right);
    left.out_edges += 1;
    left.out_rows += edge.n;
    right.in_edges += 1;
    right.in_rows += edge.n;
  }
  const bridges = [...bySign.values()].map((row) => ({
    ...row,
    bridge_edges: Math.min(row.in_edges, row.out_edges),
    bridge_rows: Math.min(row.in_rows, row.out_rows),
  })).sort((a, b) => b.bridge_edges - a.bridge_edges || b.bridge_rows - a.bridge_rows || a.sign.localeCompare(b.sign, undefined, { numeric: true }));
  const target = bridges.find((row) => row.sign === TARGET) ?? { sign: TARGET, in_edges: 0, out_edges: 0, in_rows: 0, out_rows: 0, bridge_edges: 0, bridge_rows: 0 };
  return {
    edges,
    bridges,
    target,
    target_rank: `${bridges.findIndex((row) => row.sign === TARGET) + 1}/${bridges.length}`,
    target_incoming: edges.filter((edge) => edge.right === TARGET),
    target_outgoing: edges.filter((edge) => edge.left === TARGET),
  };
}

function immediateNextStats(rows) {
  const occs = [];
  for (const row of rows) {
    for (let idx = 0; idx < row.signs.length; idx += 1) {
      occs.push({ sign: row.signs[idx], next: row.signs[idx + 1] ?? '<END>' });
    }
  }
  const targetOccs = occs.filter((occ) => occ.sign === TARGET);
  const background = occs.filter((occ) => occ.sign !== TARGET);
  const targetTerminalNext = targetOccs.filter((occ) => TERMINAL_PARTNERS.has(occ.next)).length;
  const backgroundTerminalNext = background.filter((occ) => TERMINAL_PARTNERS.has(occ.next)).length;
  const p = fisherRightTail(
    targetTerminalNext,
    targetOccs.length - targetTerminalNext,
    backgroundTerminalNext,
    background.length - backgroundTerminalNext,
  );
  const nextCounts = Object.entries(targetOccs.reduce((acc, occ) => {
    acc[occ.next] = (acc[occ.next] ?? 0) + 1;
    return acc;
  }, {})).map(([next, count]) => ({ next, count })).sort((a, b) => b.count - a.count || a.next.localeCompare(b.next, undefined, { numeric: true }));
  return {
    target_occurrences: targetOccs.length,
    target_terminal_next: targetTerminalNext,
    background_terminal_next: backgroundTerminalNext,
    background_occurrences: background.length,
    fisher_p: p,
    next_counts: nextCounts,
  };
}

function forger(rows, observedBridgeEdges, observedTerminalNextP, iterations = ITERATIONS) {
  const rand = mulberry32(0x222002 ^ rows.length);
  let bridgeGe = 0;
  let terminalNextGe = 0;
  const iterationRows = [];
  for (let iter = 0; iter < iterations; iter += 1) {
    const fakeRows = rows.map((row) => {
      const signs = row.signs.slice();
      shuffleInPlace(signs, rand);
      return { ...row, signs };
    });
    const stats = bridgeStats(fakeRows);
    const best = stats.bridges[0] ?? { sign: '', bridge_edges: 0, bridge_rows: 0 };
    const next = immediateNextStats(fakeRows);
    if (best.bridge_edges >= observedBridgeEdges) bridgeGe += 1;
    if (next.fisher_p <= observedTerminalNextP) terminalNextGe += 1;
    if (iter < 50 || best.bridge_edges >= observedBridgeEdges || next.fisher_p <= observedTerminalNextP) {
      iterationRows.push({
        iteration: iter,
        best_bridge_sign: best.sign,
        best_bridge_edges: best.bridge_edges,
        best_bridge_rows: best.bridge_rows,
        target_terminal_next_fisher_p: next.fisher_p,
        bridge_ge_observed: String(best.bridge_edges >= observedBridgeEdges),
        terminal_next_le_observed: String(next.fisher_p <= observedTerminalNextP),
      });
    }
  }
  return { iterations, bridge_maxstat_fpr: bridgeGe / iterations, terminal_next_fpr: terminalNextGe / iterations, iteration_rows: iterationRows };
}

function analyzePool(name, rows) {
  const bridge = bridgeStats(rows);
  const next = immediateNextStats(rows);
  return {
    pool: name,
    rows: rows.length,
    target_rank: bridge.target_rank,
    target_in_edges: bridge.target.in_edges,
    target_out_edges: bridge.target.out_edges,
    target_bridge_edges: bridge.target.bridge_edges,
    target_in_rows: bridge.target.in_rows,
    target_out_rows: bridge.target.out_rows,
    target_bridge_rows: bridge.target.bridge_rows,
    terminal_next: next.target_terminal_next,
    target_occurrences: next.target_occurrences,
    terminal_next_fisher_p: next.fisher_p,
    target_incoming: bridge.target_incoming,
    target_outgoing: bridge.target_outgoing,
    next_counts: next.next_counts,
    top_bridges: bridge.bridges.slice(0, 20),
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
];
const main = pools[0];
const nulls = forger(canonicalRows, main.target_bridge_edges, main.terminal_next_fisher_p);
const controlsPassing = pools.slice(1, 5).filter((pool) => pool.target_bridge_edges >= 2 && pool.terminal_next_fisher_p <= 0.01).length;
const supportRows = canonicalRows.filter((row) => row.signs.includes(TARGET)).map((row) => {
  const idx = row.signs.indexOf(TARGET);
  return {
    object: objectId(row),
    site: norm(row.site),
    region: norm(row.region),
    type: norm(row.type),
    material: norm(row.material),
    shape: norm(row.shape),
    symbol: norm(row.symbol),
    condition: norm(row.condition),
    complete: norm(row.complete),
    prev: row.signs[idx - 1] ?? '<START>',
    next: row.signs[idx + 1] ?? '<END>',
    next_is_terminal_partner: String(TERMINAL_PARTNERS.has(row.signs[idx + 1] ?? '<END>')),
    text: row.text,
  };
});

const tier =
  main.target_bridge_edges >= 2 &&
  main.terminal_next_fisher_p <= 0.01 &&
  nulls.bridge_maxstat_fpr <= 0.05 &&
  nulls.terminal_next_fpr <= 0.01 &&
  controlsPassing >= 3
    ? 'candidate'
    : 'wild shot';

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V2_V4_002_PRETERMINAL_BRIDGE_20260531',
  vector: 'V2 slot grammar; V4 context-to-meaning without sound',
  confidence_tier: tier,
  risky_bet:
    '`002` is a pre-terminal boundary bridge rather than a terminal sign by itself: many signs feed into it, and it preferentially feeds terminal partners `861`, `820`, and `817`.',
  observed:
    `All canonical: ${TARGET} bridge rank ${main.target_rank}; in_edges=${main.target_in_edges}, out_edges=${main.target_out_edges}, bridge_edges=${main.target_bridge_edges}. ` +
    `Immediate next terminal partners=${main.terminal_next}/${main.target_occurrences}, Fisher=${main.terminal_next_fisher_p}. ` +
    `Bridge maxstat FPR=${nulls.bridge_maxstat_fpr}; terminal-next FPR=${nulls.terminal_next_fpr}; controls passing=${controlsPassing}/4. ` +
    `Incoming: ${main.target_incoming.slice(0, 10).map((edge) => `${edge.left}->${TARGET}:${edge.dominant_count}/${edge.n}`).join(';')}. ` +
    `Outgoing: ${main.target_outgoing.slice(0, 10).map((edge) => `${TARGET}->${edge.right}:${edge.dominant_count}/${edge.n}`).join(';')}.`,
  adversarial_test:
    `Canonical numeric-sequence collapse; directed co-occurrence graph requiring n>=${MIN_PAIR_ROWS}, share>=${MIN_SHARE}, p<=${MAX_P}; ${ITERATIONS}-iteration row-internal sign-shuffle forger preserving row signs and co-occurrences; immediate-next enrichment for terminal partners ${[...TERMINAL_PARTNERS].join('/')}; complete-only, non-poor-only, leave-Harappa, leave-Mohenjo, and square-seal controls.`,
  false_positive_rate: Math.max(nulls.bridge_maxstat_fpr, nulls.terminal_next_fpr),
  bridge_maxstat_fpr: nulls.bridge_maxstat_fpr,
  terminal_next_fpr: nulls.terminal_next_fpr,
  terminal_next_fisher_p: main.terminal_next_fisher_p,
  falsifier:
    'If source-checked rows often place 002 finally without terminal partners, or if incoming/outgoing bridge structure disappears under expanded data, demote this to an ordinary sign participating in one narrow 002-861 terminal formula.',
  next_prediction:
    'Rows with 002 should often place it after a broad/preposed sign and before a terminal partner, especially 861/820/817. A fluent reading is not earned; this is a slot-function prediction.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({ ...summary, pools, forger: { iterations: nulls.iterations, bridge_maxstat_fpr: nulls.bridge_maxstat_fpr, terminal_next_fpr: nulls.terminal_next_fpr }, support_rows: supportRows }, null, 2),
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
  'bridge_maxstat_fpr',
  'terminal_next_fpr',
  'terminal_next_fisher_p',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_pools.csv`), pools.map((pool) => ({
  pool: pool.pool,
  rows: pool.rows,
  target_rank: pool.target_rank,
  target_in_edges: pool.target_in_edges,
  target_out_edges: pool.target_out_edges,
  target_bridge_edges: pool.target_bridge_edges,
  target_bridge_rows: pool.target_bridge_rows,
  terminal_next: pool.terminal_next,
  target_occurrences: pool.target_occurrences,
  terminal_next_fisher_p: pool.terminal_next_fisher_p,
})), [
  'pool',
  'rows',
  'target_rank',
  'target_in_edges',
  'target_out_edges',
  'target_bridge_edges',
  'target_bridge_rows',
  'terminal_next',
  'target_occurrences',
  'terminal_next_fisher_p',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_target_incoming.csv`), main.target_incoming, [
  'left',
  'right',
  'pair',
  'n',
  'dominant_count',
  'opposite_count',
  'dominant_share',
  'binomial_p',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_target_outgoing.csv`), main.target_outgoing, [
  'left',
  'right',
  'pair',
  'n',
  'dominant_count',
  'opposite_count',
  'dominant_share',
  'binomial_p',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_next_counts.csv`), main.next_counts, ['next', 'count']);
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
  'prev',
  'next',
  'next_is_terminal_partner',
  'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_forger_iterations.csv`), nulls.iteration_rows, [
  'iteration',
  'best_bridge_sign',
  'best_bridge_edges',
  'best_bridge_rows',
  'target_terminal_next_fisher_p',
  'bridge_ge_observed',
  'terminal_next_le_observed',
]);

console.log(JSON.stringify(summary, null, 2));
