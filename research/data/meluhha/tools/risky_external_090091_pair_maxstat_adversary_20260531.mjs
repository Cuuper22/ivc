import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const EXTERNAL = path.join(ROOT, 'data', 'meluhha', 'external_indus_objects.csv');
const OUT_DIR = path.join(ROOT, 'data', 'meluhha');
const PREFIX = 'risky_external_090091_pair_maxstat_adversary_20260531';
const RUN_DATE = '2026-05-31';
const TARGET = ['090', '091'];
const ITERATIONS = 5000;

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
  return text && text !== '-' && text !== 'None' ? text : fallback;
}

function isCircular(row) {
  return norm(row.shape).toLowerCase() === 'circular' || norm(row.type).toUpperCase() === 'SEAL:C';
}

function isLiteralCircular(row) {
  return norm(row.shape).toLowerCase() === 'circular';
}

function isSquareSeal(row) {
  return norm(row.type).toUpperCase() === 'SEAL:S' || norm(row.shape).toLowerCase() === 'square';
}

function isSealC(row) {
  return norm(row.type).toUpperCase() === 'SEAL:C';
}

function hasEither(row, pair) {
  return pair.some((sign) => row.signs.includes(sign));
}

function hasBoth(row, pair) {
  return pair.every((sign) => row.signs.includes(sign));
}

function fisherRightTail(a, b, c, d) {
  const logFact = [0];
  const n = a + b + c + d;
  for (let i = 1; i <= n; i += 1) logFact[i] = logFact[i - 1] + Math.log(i);
  const logChoose = (nn, kk) => logFact[nn] - logFact[kk] - logFact[nn - kk];
  const row1 = a + b;
  const row2 = c + d;
  const col1 = a + c;
  const max = Math.min(row1, col1);
  const logDen = logChoose(n, col1);
  let p = 0;
  for (let x = a; x <= max; x += 1) {
    p += Math.exp(logChoose(row1, x) + logChoose(row2, col1 - x) - logDen);
  }
  return Math.max(0, Math.min(1, p));
}

function mulberry32(seed) {
  return function rand() {
    let t = (seed += 0x6D2B79F5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffleLabels(rand, n, k) {
  const labels = Array.from({ length: n }, (_, idx) => idx < k);
  for (let i = n - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    const tmp = labels[i];
    labels[i] = labels[j];
    labels[j] = tmp;
  }
  return labels;
}

function pairKey(pair) {
  return pair.slice().sort().join('/');
}

function allPairs(rows, minEither = 1) {
  const counts = new Map();
  for (const row of rows) {
    for (const sign of new Set(row.signs)) counts.set(sign, (counts.get(sign) ?? 0) + 1);
  }
  const signs = [...counts.entries()].filter(([, count]) => count >= minEither).map(([sign]) => sign).sort();
  const pairs = [];
  for (let i = 0; i < signs.length; i += 1) {
    for (let j = i + 1; j < signs.length; j += 1) pairs.push([signs[i], signs[j]]);
  }
  return pairs;
}

function analyzeComparator(name, rowsA, rowsB, options = {}) {
  const pool = [...rowsA, ...rowsB];
  const labels = pool.map((_, idx) => idx < rowsA.length);
  const pairs = allPairs(pool, options.minEither ?? 1);
  const pairModels = pairs.map((pair) => ({
    pair,
    key: pairKey(pair),
    hits: pool.map((row) => hasEither(row, pair)),
    bothA: pool.slice(0, rowsA.length).filter((row) => hasBoth(row, pair)).length,
  }));
  const targetKey = pairKey(TARGET);
  const results = pairModels.map((model) => {
    let a = 0;
    let c = 0;
    for (let idx = 0; idx < pool.length; idx += 1) {
      if (!model.hits[idx]) continue;
      if (labels[idx]) a += 1;
      else {
        c += 1;
      }
    }
    const p = fisherRightTail(a, rowsA.length - a, c, rowsB.length - c);
    return { pair: model.key, a, b: rowsA.length - a, c, d: rowsB.length - c, bothA: model.bothA, p };
  }).sort((x, y) => x.p - y.p || y.a - x.a || x.pair.localeCompare(y.pair, undefined, { numeric: true }));

  const target = results.find((row) => row.pair === targetKey);
  const targetRank = target ? results.findIndex((row) => row.pair === targetKey) + 1 : null;
  const bonferroni = target ? Math.min(1, target.p * results.length) : null;

  const rand = mulberry32(0x90912026 ^ rowsA.length ^ (rowsB.length << 8) ^ (pool.length << 16));
  let maxGe = 0;
  let targetGe = 0;
  const permutationIterations = options.permutationIterations ?? ITERATIONS;
  for (let iter = 0; iter < permutationIterations; iter += 1) {
    const perm = shuffleLabels(rand, pool.length, rowsA.length);
    let best = 1;
    let targetPermP = 1;
    for (const model of pairModels) {
      let a = 0;
      let c = 0;
      for (let idx = 0; idx < pool.length; idx += 1) {
        if (!model.hits[idx]) continue;
        if (perm[idx]) a += 1;
        else c += 1;
      }
      const p = fisherRightTail(a, rowsA.length - a, c, rowsB.length - c);
      if (p < best) best = p;
      if (model.key === targetKey) targetPermP = p;
    }
    if (target && best <= target.p) maxGe += 1;
    if (target && targetPermP <= target.p) targetGe += 1;
  }

  return {
    comparator: name,
    rows_a: rowsA.length,
    rows_b: rowsB.length,
    pair_tests: results.length,
    target_pair: targetKey,
    target_a: target?.a ?? 0,
    target_b: target?.b ?? rowsA.length,
    target_c: target?.c ?? 0,
    target_d: target?.d ?? rowsB.length,
    target_both_a: target?.bothA ?? 0,
    fisher_p: target?.p ?? 1,
    rank: targetRank ? `${targetRank}/${results.length}` : `NA/${results.length}`,
    bonferroni_p: bonferroni,
    maxstat_permutation_fpr: permutationIterations ? maxGe / permutationIterations : null,
    target_only_permutation_fpr: permutationIterations ? targetGe / permutationIterations : null,
    top_pairs: results.slice(0, 10),
  };
}

function siteBlockedExternalCircular(externalCircular) {
  const bySite = new Map();
  for (const row of externalCircular) {
    const site = norm(row.site);
    if (!bySite.has(site)) bySite.set(site, []);
    bySite.get(site).push(row);
  }
  const rows = [...bySite.entries()].map(([site, siteRows]) => ({
    site,
    rows: siteRows.length,
    has_090: siteRows.some((row) => row.signs.includes('090')),
    has_091: siteRows.some((row) => row.signs.includes('091')),
    has_either: siteRows.some((row) => hasEither(row, TARGET)),
    has_both_any_row: siteRows.some((row) => hasBoth(row, TARGET)),
    examples: siteRows.map((row) => `${row.row_id}:${row.text}`).join(' | '),
  })).sort((a, b) => a.site.localeCompare(b.site));
  const eitherSites = rows.filter((row) => row.has_either).length;
  const bothSignsAcrossSite = rows.filter((row) => row.has_090 && row.has_091).length;
  return { sites: rows.length, either_sites: eitherSites, both_signs_across_site: bothSignsAcrossSite, rows };
}

const metadata = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, row_id: row.id, signs: tokens(row.text) }));
const external = parseCsv(fs.readFileSync(EXTERNAL, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const externalCircular = external.filter(isCircular);
const externalNonCircular = external.filter((row) => !isCircular(row));
const externalLiteralCircular = external.filter(isLiteralCircular);
const externalNotLiteralCircular = external.filter((row) => !isLiteralCircular(row));
const externalSquareSeals = external.filter(isSquareSeal);
const localCircular = metadata.filter(isCircular);
const corridorRegions = new Set(['Persian Gulf', 'Mesopotamia', 'Iranian Plateau']);
const corridorCircular = localCircular.filter((row) => corridorRegions.has(norm(row.region)));
const otherCircular = localCircular.filter((row) => !corridorRegions.has(norm(row.region)));
const corridorSealC = localCircular.filter((row) => corridorRegions.has(norm(row.region)) && isSealC(row));
const otherSealC = localCircular.filter((row) => !corridorRegions.has(norm(row.region)) && isSealC(row));

const comparators = [
  analyzeComparator('external_circular_vs_external_non_circular', externalCircular, externalNonCircular, { permutationIterations: 2000 }),
  analyzeComparator('corridor_circular_vs_other_circular', corridorCircular, otherCircular, { permutationIterations: 0 }),
  analyzeComparator('corridor_seal_c_vs_other_seal_c_same_type', corridorSealC, otherSealC, { permutationIterations: 0 }),
  analyzeComparator('external_circular_vs_external_square_or_square_seal', externalCircular, externalSquareSeals, { permutationIterations: 2000 }),
  analyzeComparator('external_literal_shape_circular_vs_external_not_literal_shape_circular', externalLiteralCircular, externalNotLiteralCircular, { permutationIterations: 2000 }),
];
const primary = comparators[0];
const siteBlocked = siteBlockedExternalCircular(externalCircular);
const sameType = comparators.find((row) => row.comparator === 'corridor_seal_c_vs_other_seal_c_same_type');
const square = comparators.find((row) => row.comparator === 'external_circular_vs_external_square_or_square_seal');
const literal = comparators.find((row) => row.comparator === 'external_literal_shape_circular_vs_external_not_literal_shape_circular');

const tier =
  primary.bonferroni_p <= 0.01 &&
  primary.maxstat_permutation_fpr <= 0.01 &&
  sameType.fisher_p <= 0.05 &&
  square.fisher_p <= 0.01 &&
  literal.fisher_p <= 0.01
    ? 'candidate'
    : 'wild shot';

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V1_EXTERNAL_090091_PAIR_MAXSTAT_ADVERSARY_20260531',
  vector: 'V1 diffuse Meluhha / Gulf external-contact bridge',
  confidence_tier: tier,
  risky_bet:
    '`090/091` is the discoverable top pair for the external circular-seal register, not just a handpicked pair. The stronger route-specific reading predicts that stricter object-shape/type comparators should not erase the signal.',
  observed:
    `Primary ${primary.comparator}: ${primary.target_a}/${primary.rows_a} vs ${primary.target_c}/${primary.rows_b}, rank ${primary.rank}, Bonferroni=${primary.bonferroni_p}, maxstat=${primary.maxstat_permutation_fpr}. ` +
    `Same-type SEAL:C: ${sameType.target_a}/${sameType.rows_a} vs ${sameType.target_c}/${sameType.rows_b}, p=${sameType.fisher_p}, Bonferroni=${sameType.bonferroni_p}. ` +
    `External circular vs square/seal-square: ${square.target_a}/${square.rows_a} vs ${square.target_c}/${square.rows_b}, p=${square.fisher_p}, Bonferroni=${square.bonferroni_p}. ` +
    `Literal circular shape only: ${literal.target_a}/${literal.rows_a} vs ${literal.target_c}/${literal.rows_b}, p=${literal.fisher_p}.`,
  adversarial_test:
    'All unordered sign-pair scan with Bonferroni; 2000-iteration max-statistic label permutation for external-row comparators; same-type SEAL:C control; external circular-vs-square control; literal-shape-circular control; site-blocked support summary.',
  false_positive_rate: primary.maxstat_permutation_fpr,
  primary_bonferroni_p: primary.bonferroni_p,
  same_type_fisher_p: sameType.fisher_p,
  same_type_bonferroni_p: sameType.bonferroni_p,
  square_fisher_p: square.fisher_p,
  square_bonferroni_p: square.bonferroni_p,
  literal_shape_fisher_p: literal.fisher_p,
  site_blocked_support:
    `${siteBlocked.either_sites}/${siteBlocked.sites} external circular sites have either sign; ${siteBlocked.both_signs_across_site} sites have both signs across site-level support.`,
  skeptic_verdict:
    tier === 'candidate'
      ? 'The pair survives the hostile broad-pair test, but source validation and site clustering still prevent acceptance.'
      : 'The pair is real under the broad external-circular comparator but demotes under stricter same-type/multiple-comparison controls; keep it as a positive bet, not a bridge anchor.',
  next_prediction:
    'New source-validated circular external seals should add 090 or 091 more often than square external seals. If same-type SEAL:C non-corridor rows continue to carry the pair, the route-specific reading collapses into generic circular-seal marking.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({ ...summary, comparators, site_blocked: siteBlocked }, null, 2),
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
  'primary_bonferroni_p',
  'same_type_fisher_p',
  'same_type_bonferroni_p',
  'square_fisher_p',
  'square_bonferroni_p',
  'literal_shape_fisher_p',
  'site_blocked_support',
  'skeptic_verdict',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_comparators.csv`), comparators, [
  'comparator',
  'rows_a',
  'rows_b',
  'pair_tests',
  'target_pair',
  'target_a',
  'target_b',
  'target_c',
  'target_d',
  'target_both_a',
  'fisher_p',
  'rank',
  'bonferroni_p',
  'maxstat_permutation_fpr',
  'target_only_permutation_fpr',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_site_blocked.csv`), siteBlocked.rows, [
  'site',
  'rows',
  'has_090',
  'has_091',
  'has_either',
  'has_both_any_row',
  'examples',
]);

console.log(JSON.stringify(summary, null, 2));
