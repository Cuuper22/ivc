import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_400740_tablet_hierarchy_forger_20260531';
const RUN_DATE = '2026-05-31';
const FRAME = '400';
const INNER = '740';
const ITERATIONS = 2000;
const MIN_PAIR_ROWS = 20;

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

function tabletAccountContext(row) {
  return ['TAB:B', 'TAB:I'].includes(norm(row.type));
}

function accountOrRectRegister(row) {
  return ['TAB:B', 'TAB:I', 'SEAL:R', 'TAB:C'].includes(norm(row.type));
}

function binomialRightTail(k, n, p = 0.5) {
  let prob = 0;
  for (let x = k; x <= n; x += 1) {
    let logComb = 0;
    for (let i = 1; i <= x; i += 1) logComb += Math.log((n - x + i) / i);
    prob += Math.exp(logComb + x * Math.log(p) + (n - x) * Math.log(1 - p));
  }
  return Math.max(0, Math.min(1, prob));
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

function signBefore(row, a, b) {
  const ai = row.signs.indexOf(a);
  const bi = row.signs.indexOf(b);
  if (ai < 0 || bi < 0) return null;
  return ai < bi;
}

function pairDirectionRows(rows) {
  const pairMap = new Map();
  for (const row of rows) {
    const unique = [...new Set(row.signs)].sort();
    for (let i = 0; i < unique.length; i += 1) {
      for (let j = i + 1; j < unique.length; j += 1) {
        const a = unique[i];
        const b = unique[j];
        const key = `${a}|${b}`;
        if (!pairMap.has(key)) pairMap.set(key, { a, b, n: 0, a_before_b: 0, rows: [] });
        const rec = pairMap.get(key);
        const before = signBefore(row, a, b);
        if (before === null) continue;
        rec.n += 1;
        if (before) rec.a_before_b += 1;
        rec.rows.push(row);
      }
    }
  }
  return [...pairMap.values()]
    .filter((row) => row.n >= MIN_PAIR_ROWS)
    .map((row) => {
      const forward = row.a_before_b;
      const reverse = row.n - row.a_before_b;
      const dominant_forward = forward >= reverse;
      const dominant_count = Math.max(forward, reverse);
      return {
        pair: `${row.a}|${row.b}`,
        left: dominant_forward ? row.a : row.b,
        right: dominant_forward ? row.b : row.a,
        n: row.n,
        dominant_count,
        opposite_count: row.n - dominant_count,
        dominant_share: dominant_count / row.n,
        binomial_p: binomialRightTail(dominant_count, row.n),
      };
    })
    .sort((x, y) => x.binomial_p - y.binomial_p || y.dominant_share - x.dominant_share || y.n - x.n);
}

function rowShuffleForger(rows, targetP, iterations = ITERATIONS) {
  const rand = mulberry32(0x400740 ^ rows.length);
  let maxGe = 0;
  const iterationRows = [];
  for (let iter = 0; iter < iterations; iter += 1) {
    const fakeRows = rows.map((row) => {
      const signs = row.signs.slice();
      shuffleInPlace(signs, rand);
      return { ...row, signs };
    });
    const top = pairDirectionRows(fakeRows)[0];
    if (top && top.binomial_p <= targetP) maxGe += 1;
    if (iter < 50 || (top && top.binomial_p <= targetP)) {
      iterationRows.push({
        iteration: iter,
        best_pair: top?.pair ?? '',
        best_left: top?.left ?? '',
        best_right: top?.right ?? '',
        best_n: top?.n ?? '',
        best_dominant_count: top?.dominant_count ?? '',
        best_binomial_p: top?.binomial_p ?? '',
        ge_target: String(Boolean(top && top.binomial_p <= targetP)),
      });
    }
  }
  return { iterations, maxstat_fpr: maxGe / iterations, iteration_rows: iterationRows };
}

function analyzePool(name, rows) {
  const bothRows = rows.filter((row) => row.signSet.has(FRAME) && row.signSet.has(INNER));
  const frameBefore = bothRows.filter((row) => signBefore(row, FRAME, INNER)).length;
  const innerBefore = bothRows.length - frameBefore;
  const p = binomialRightTail(Math.max(frameBefore, innerBefore), bothRows.length);
  const pairRows = pairDirectionRows(rows);
  const rank = pairRows.findIndex((row) => row.left === FRAME && row.right === INNER) + 1;
  return {
    pool: name,
    rows: rows.length,
    both_rows: bothRows.length,
    frame_before_inner: frameBefore,
    inner_before_frame: innerBefore,
    frame_before_share: frameBefore / Math.max(1, bothRows.length),
    binomial_p: p,
    all_pair_direction_rank: rank > 0 ? `${rank}/${pairRows.length}` : `not_in_top/${pairRows.length}`,
    top_direction_pairs: pairRows.slice(0, 25),
  };
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()]
  .map((row) => ({ ...row, signSet: new Set(row.signs) }));

const pools = [
  analyzePool('all_canonical', canonicalRows),
  analyzePool('account_or_rect_register_only', canonicalRows.filter(accountOrRectRegister)),
  analyzePool('tablet_account_only', canonicalRows.filter(tabletAccountContext)),
  analyzePool('complete_only', canonicalRows.filter((row) => norm(row.complete) === 'Y')),
  analyzePool('non_poor_only', canonicalRows.filter((row) => norm(row.condition) !== 'Poor')),
  analyzePool('without_harappa', canonicalRows.filter((row) => norm(row.site) !== 'Harappa')),
  analyzePool('without_mohenjo_daro', canonicalRows.filter((row) => norm(row.site) !== 'Mohenjo-daro')),
];
const main = pools[0];
const account = pools[1];
const tablet = pools[2];
const forger = rowShuffleForger(canonicalRows, main.binomial_p);

const supportRows = canonicalRows
  .filter((row) => row.signSet.has(FRAME) && row.signSet.has(INNER))
  .map((row) => ({
    object: objectId(row),
    site: norm(row.site),
    region: norm(row.region),
    type: norm(row.type),
    material: norm(row.material),
    shape: norm(row.shape),
    symbol: norm(row.symbol),
    condition: norm(row.condition),
    complete: norm(row.complete),
    frame_before_inner: String(signBefore(row, FRAME, INNER)),
    first_sign: row.signs[0] ?? '',
    text: row.text,
  }));

const controlsPassing = pools.slice(1).filter((pool) => pool.both_rows >= 10 && pool.frame_before_share >= 0.8 && pool.binomial_p <= 0.01).length;
const tier =
  main.both_rows >= 40 &&
  main.frame_before_share >= 0.8 &&
  main.binomial_p <= 0.01 &&
  forger.maxstat_fpr <= 0.01 &&
  controlsPassing >= 4
    ? 'promoted candidate'
    : 'candidate';

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V2_V4_400740_TABLET_HIERARCHY_20260531',
  vector: 'V4 context-to-meaning without sound; V2 slot grammar',
  confidence_tier: tier,
  risky_bet:
    '`400` is not merely an alternative to `740`. In the tablet/account register it is a higher-level frame opener, and `740` can occur under it as an inner/default opener. Therefore rows containing both signs should overwhelmingly place `400` before `740`, especially in TAB:B/TAB:I.',
  observed:
    `All canonical co-occurrence rows=${main.both_rows}; 400 before 740=${main.frame_before_inner}, 740 before 400=${main.inner_before_frame}, binomial=${main.binomial_p}, all-pair rank=${main.all_pair_direction_rank}, row-shuffle maxstat=${forger.maxstat_fpr}. ` +
    `Account/rectangular universe: ${account.frame_before_inner}/${account.both_rows}; tablet-account only: ${tablet.frame_before_inner}/${tablet.both_rows}. Controls passing strict directional test=${controlsPassing}/6.`,
  adversarial_test:
    `Canonical numeric-sequence collapse; all-sign co-occurring pair direction scan with minimum ${MIN_PAIR_ROWS} rows; ${ITERATIONS}-iteration row-internal sign-shuffle forger preserving each row's sign multiset and all co-occurrences; account/rectangular-only, tablet-only, complete-only, non-poor-only, leave-Harappa, and leave-Mohenjo controls.`,
  false_positive_rate: forger.maxstat_fpr,
  direct_binomial_p: main.binomial_p,
  cooccurrence_rows: main.both_rows,
  controls_passing_strict_direction: controlsPassing,
  falsifier:
    'If source-checked 400+740 rows stop ordering 400 before 740, or if the order collapses outside Harappa/tablet material, kill the hierarchy and treat 400/740 as unordered co-register signs.',
  next_prediction:
    'New TAB:B/TAB:I rows containing both 400 and 740 should normally put 400 first. Rows starting with 740 but lacking 400 are more likely to belong to the SEAL:R/TAB:C register or to square-seal leakage; rows starting 400-740 are likely non-copper tablet/account rows.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({ ...summary, pools, forger: { iterations: forger.iterations, maxstat_fpr: forger.maxstat_fpr }, support_rows: supportRows }, null, 2),
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
  'direct_binomial_p',
  'cooccurrence_rows',
  'controls_passing_strict_direction',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_pools.csv`), pools.map((pool) => ({
  pool: pool.pool,
  rows: pool.rows,
  both_rows: pool.both_rows,
  frame_before_inner: pool.frame_before_inner,
  inner_before_frame: pool.inner_before_frame,
  frame_before_share: pool.frame_before_share,
  binomial_p: pool.binomial_p,
  all_pair_direction_rank: pool.all_pair_direction_rank,
})), [
  'pool',
  'rows',
  'both_rows',
  'frame_before_inner',
  'inner_before_frame',
  'frame_before_share',
  'binomial_p',
  'all_pair_direction_rank',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_top_direction_pairs.csv`), main.top_direction_pairs, [
  'pair',
  'left',
  'right',
  'n',
  'dominant_count',
  'opposite_count',
  'dominant_share',
  'binomial_p',
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
  'frame_before_inner',
  'first_sign',
  'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_forger_iterations.csv`), forger.iteration_rows, [
  'iteration',
  'best_pair',
  'best_left',
  'best_right',
  'best_n',
  'best_dominant_count',
  'best_binomial_p',
  'ge_target',
]);

console.log(JSON.stringify(summary, null, 2));
