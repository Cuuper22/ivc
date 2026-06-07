import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_407_copper_tab_c_register_forger_20260531';
const RUN_DATE = '2026-05-31';
const TARGET = '407';
const ITERATIONS = 2000;

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

const logFactCache = new Map();
function getLogFact(n) {
  if (logFactCache.has(n)) return logFactCache.get(n);
  const logFact = [0];
  for (let i = 1; i <= n; i += 1) logFact[i] = logFact[i - 1] + Math.log(i);
  logFactCache.set(n, logFact);
  return logFact;
}

function fisherRightTail(a, b, c, d) {
  const n = a + b + c + d;
  const logFact = getLogFact(n);
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

function sampleWithoutReplacement(rand, n, k) {
  const arr = Array.from({ length: n }, (_, idx) => idx);
  for (let i = 0; i < k; i += 1) {
    const j = i + Math.floor(rand() * (n - i));
    const tmp = arr[i];
    arr[i] = arr[j];
    arr[j] = tmp;
  }
  return arr.slice(0, k);
}

function analyzeContext(rows, signs, totalSignCounts, name, predicate) {
  const contextRows = rows.filter(predicate);
  const contextSet = new Set(contextRows.map((row) => row._idx));
  const backgroundRows = rows.filter((row) => !contextSet.has(row._idx));
  const signRows = signs.map((sign) => {
    const a = contextRows.filter((row) => row.signSet.has(sign)).length;
    const c = totalSignCounts.get(sign) - a;
    const p = fisherRightTail(a, contextRows.length - a, c, backgroundRows.length - c);
    return {
      context: name,
      sign,
      context_rows: contextRows.length,
      a,
      b: contextRows.length - a,
      c,
      d: backgroundRows.length - c,
      share: a / contextRows.length,
      background_share: c / backgroundRows.length,
      relative_rate: c ? (a / contextRows.length) / (c / backgroundRows.length) : 'Infinity',
      fisher_p: p,
    };
  }).sort((x, y) => x.fisher_p - y.fisher_p || y.a - x.a || x.sign.localeCompare(y.sign, undefined, { numeric: true }));
  const target = signRows.find((row) => row.sign === TARGET);
  const rank = signRows.findIndex((row) => row.sign === TARGET) + 1;
  const comparable = signRows.filter((row) => {
    const total = row.a + row.c;
    const targetTotal = target.a + target.c;
    return total >= targetTotal / 2 && total <= targetTotal * 2;
  });
  const comparableGe = comparable.filter((row) => row.a >= target.a && row.sign !== TARGET);

  const rand = mulberry32(0x4072026 ^ contextRows.length ^ name.length);
  let maxStatGe = 0;
  let targetOnlyGe = 0;
  for (let iter = 0; iter < ITERATIONS; iter += 1) {
    const sampled = sampleWithoutReplacement(rand, rows.length, contextRows.length);
    const sampledCounts = new Map();
    for (const idx of sampled) {
      for (const sign of rows[idx].signSet) sampledCounts.set(sign, (sampledCounts.get(sign) ?? 0) + 1);
    }
    let bestP = 1;
    let targetP = 1;
    for (const sign of signs) {
      const a = sampledCounts.get(sign) ?? 0;
      const c = totalSignCounts.get(sign) - a;
      const p = fisherRightTail(a, contextRows.length - a, c, rows.length - contextRows.length - c);
      if (p < bestP) bestP = p;
      if (sign === TARGET) targetP = p;
    }
    if (bestP <= target.fisher_p) maxStatGe += 1;
    if (targetP <= target.fisher_p) targetOnlyGe += 1;
  }

  return {
    summary: {
      context: name,
      rows: contextRows.length,
      background_rows: backgroundRows.length,
      target_a: target.a,
      target_c: target.c,
      target_share: target.share,
      target_background_share: target.background_share,
      relative_rate: target.relative_rate,
      fisher_p: target.fisher_p,
      all_sign_rank: `${rank}/${signRows.length}`,
      bonferroni_p: Math.min(1, target.fisher_p * signRows.length),
      maxstat_permutation_fpr: maxStatGe / ITERATIONS,
      target_only_permutation_fpr: targetOnlyGe / ITERATIONS,
      comparable_ge: comparableGe.map((row) => `${row.sign}:${row.a}/${row.a + row.c}`).join(';') || 'none',
    },
    sign_rows: signRows,
    support_rows: contextRows.filter((row) => row.signSet.has(TARGET)).map((row) => ({
      object: objectId(row),
      region: norm(row.region),
      site: norm(row.site),
      type: norm(row.type),
      material: norm(row.material),
      shape: norm(row.shape),
      symbol: norm(row.symbol),
      condition: norm(row.condition),
      complete: norm(row.complete),
      text: row.text,
    })),
  };
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()]
  .map((row, idx) => ({ ...row, _idx: idx, signSet: new Set(row.signs) }));
function analyzeContextForPool(poolRows, name, predicate) {
  const poolSigns = [...new Set(poolRows.flatMap((row) => row.signs))].sort();
  const poolSignCounts = new Map(poolSigns.map((sign) => [sign, poolRows.filter((row) => row.signSet.has(sign)).length]));
  return analyzeContext(poolRows, poolSigns, poolSignCounts, name, predicate);
}

const contexts = [
  analyzeContextForPool(canonicalRows, 'material_copper', (row) => norm(row.material) === 'Copper'),
  analyzeContextForPool(canonicalRows, 'type_tab_c', (row) => norm(row.type) === 'TAB:C'),
  analyzeContextForPool(
    canonicalRows,
    'material_copper_and_type_tab_c',
    (row) => norm(row.material) === 'Copper' && norm(row.type) === 'TAB:C',
  ),
  analyzeContextForPool(
    canonicalRows.filter((row) => norm(row.site) === 'Mohenjo-daro'),
    'within_mohenjo_material_copper_and_type_tab_c',
    (row) => norm(row.material) === 'Copper' && norm(row.type) === 'TAB:C',
  ),
  analyzeContextForPool(
    canonicalRows.filter((row) => norm(row.complete) === 'Y'),
    'complete_only_material_copper_and_type_tab_c',
    (row) => norm(row.material) === 'Copper' && norm(row.type) === 'TAB:C',
  ),
  analyzeContextForPool(
    canonicalRows.filter((row) => norm(row.condition) !== 'Poor'),
    'non_poor_only_material_copper_and_type_tab_c',
    (row) => norm(row.material) === 'Copper' && norm(row.type) === 'TAB:C',
  ),
  analyzeContextForPool(
    canonicalRows.filter((row) => norm(row.site) === 'Mohenjo-daro' && norm(row.complete) === 'Y'),
    'within_mohenjo_complete_only_material_copper_and_type_tab_c',
    (row) => norm(row.material) === 'Copper' && norm(row.type) === 'TAB:C',
  ),
  analyzeContextForPool(
    canonicalRows.filter((row) => norm(row.site) === 'Mohenjo-daro' && norm(row.condition) !== 'Poor'),
    'within_mohenjo_non_poor_only_material_copper_and_type_tab_c',
    (row) => norm(row.material) === 'Copper' && norm(row.type) === 'TAB:C',
  ),
];

const copper = contexts.find((ctx) => ctx.summary.context === 'material_copper').summary;
const tabC = contexts.find((ctx) => ctx.summary.context === 'type_tab_c').summary;
const copperTabC = contexts.find((ctx) => ctx.summary.context === 'material_copper_and_type_tab_c').summary;
const mohenjoCopperTabC = contexts.find((ctx) => ctx.summary.context === 'within_mohenjo_material_copper_and_type_tab_c').summary;
const completeCopperTabC = contexts.find((ctx) => ctx.summary.context === 'complete_only_material_copper_and_type_tab_c').summary;
const nonPoorCopperTabC = contexts.find((ctx) => ctx.summary.context === 'non_poor_only_material_copper_and_type_tab_c').summary;
const mohenjoCompleteCopperTabC = contexts.find((ctx) => ctx.summary.context === 'within_mohenjo_complete_only_material_copper_and_type_tab_c').summary;
const mohenjoNonPoorCopperTabC = contexts.find((ctx) => ctx.summary.context === 'within_mohenjo_non_poor_only_material_copper_and_type_tab_c').summary;
const tier =
  copper.bonferroni_p <= 0.01 &&
  tabC.bonferroni_p <= 0.01 &&
  mohenjoCopperTabC.bonferroni_p <= 0.01 &&
  completeCopperTabC.bonferroni_p <= 0.01 &&
  mohenjoCompleteCopperTabC.bonferroni_p <= 0.01 &&
  copper.maxstat_permutation_fpr <= 0.01 &&
  tabC.maxstat_permutation_fpr <= 0.01 &&
  mohenjoCopperTabC.maxstat_permutation_fpr <= 0.01 &&
  completeCopperTabC.maxstat_permutation_fpr <= 0.01 &&
  mohenjoCompleteCopperTabC.maxstat_permutation_fpr <= 0.01
    ? 'candidate'
    : 'wild shot';

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V4_407_COPPER_TAB_C_REGISTER_20260531',
  vector: 'V4 context-to-meaning without sound',
  confidence_tier: tier,
  risky_bet:
    '`407` carries copper / TAB:C register load. This predicts material-object semantics only: `407` should recur on copper tablets and TAB:C contexts at a rate not matched by frequency-comparable signs.',
  observed:
    `Copper: ${copper.target_a}/${copper.rows} vs ${copper.target_c}/${copper.background_rows}, rank ${copper.all_sign_rank}, Bonferroni=${copper.bonferroni_p}, maxstat=${copper.maxstat_permutation_fpr}. ` +
    `TAB:C: ${tabC.target_a}/${tabC.rows} vs ${tabC.target_c}/${tabC.background_rows}, rank ${tabC.all_sign_rank}, Bonferroni=${tabC.bonferroni_p}, maxstat=${tabC.maxstat_permutation_fpr}. ` +
    `Copper+TAB:C intersection: ${copperTabC.target_a}/${copperTabC.rows} vs ${copperTabC.target_c}/${copperTabC.background_rows}, p=${copperTabC.fisher_p}. ` +
    `Within Mohenjo-daro only: ${mohenjoCopperTabC.target_a}/${mohenjoCopperTabC.rows} vs ${mohenjoCopperTabC.target_c}/${mohenjoCopperTabC.background_rows}, Bonferroni=${mohenjoCopperTabC.bonferroni_p}, maxstat=${mohenjoCopperTabC.maxstat_permutation_fpr}. ` +
    `Complete-only: ${completeCopperTabC.target_a}/${completeCopperTabC.rows} vs ${completeCopperTabC.target_c}/${completeCopperTabC.background_rows}, Bonferroni=${completeCopperTabC.bonferroni_p}, maxstat=${completeCopperTabC.maxstat_permutation_fpr}. ` +
    `Non-poor-only stress: ${nonPoorCopperTabC.target_a}/${nonPoorCopperTabC.rows} vs ${nonPoorCopperTabC.target_c}/${nonPoorCopperTabC.background_rows}, Fisher=${nonPoorCopperTabC.fisher_p}, Bonferroni=${nonPoorCopperTabC.bonferroni_p}; within-Mohenjo non-poor Fisher=${mohenjoNonPoorCopperTabC.fisher_p}.`,
  adversarial_test:
    `Canonical numeric-sequence collapse; all-sign Fisher rank; Bonferroni per context; ${ITERATIONS}-iteration max-statistic context-label forger; frequency-comparable check; within-Mohenjo site-block control; complete-only and non-poor-only preservation controls.`,
  false_positive_rate: Math.max(
    copper.maxstat_permutation_fpr,
    tabC.maxstat_permutation_fpr,
    mohenjoCopperTabC.maxstat_permutation_fpr,
    completeCopperTabC.maxstat_permutation_fpr,
    mohenjoCompleteCopperTabC.maxstat_permutation_fpr,
  ),
  copper_bonferroni_p: copper.bonferroni_p,
  tab_c_bonferroni_p: tabC.bonferroni_p,
  within_mohenjo_bonferroni_p: mohenjoCopperTabC.bonferroni_p,
  complete_only_bonferroni_p: completeCopperTabC.bonferroni_p,
  non_poor_only_bonferroni_p: nonPoorCopperTabC.bonferroni_p,
  within_mohenjo_complete_only_bonferroni_p: mohenjoCompleteCopperTabC.bonferroni_p,
  within_mohenjo_non_poor_only_bonferroni_p: mohenjoNonPoorCopperTabC.bonferroni_p,
  copper_comparable_ge: copper.comparable_ge,
  tab_c_comparable_ge: tabC.comparable_ge,
  falsifier:
    'A source-verified copper/TAB:C expansion where 407 drops to background levels, or a frequency-comparable sign matching 407 under the same context-label null, demotes the register reading.',
  next_prediction:
    'Weakly sourced or future TAB:C/copper rows should contain 407 disproportionately; non-copper tablets should not acquire 407 at the same rate. This does not license a sound value.',
};

const supportRows = contexts.flatMap((ctx) => ctx.support_rows.map((row) => ({ context: ctx.summary.context, ...row })));
const signRows = contexts.flatMap((ctx) => ctx.sign_rows);
fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({ ...summary, contexts: contexts.map((ctx) => ctx.summary), support_rows: supportRows }, null, 2),
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
  'copper_bonferroni_p',
  'tab_c_bonferroni_p',
  'within_mohenjo_bonferroni_p',
  'complete_only_bonferroni_p',
  'non_poor_only_bonferroni_p',
  'within_mohenjo_complete_only_bonferroni_p',
  'within_mohenjo_non_poor_only_bonferroni_p',
  'copper_comparable_ge',
  'tab_c_comparable_ge',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_contexts.csv`), contexts.map((ctx) => ctx.summary), [
  'context',
  'rows',
  'background_rows',
  'target_a',
  'target_c',
  'target_share',
  'target_background_share',
  'relative_rate',
  'fisher_p',
  'all_sign_rank',
  'bonferroni_p',
  'maxstat_permutation_fpr',
  'target_only_permutation_fpr',
  'comparable_ge',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_support_rows.csv`), supportRows, [
  'context',
  'object',
  'region',
  'site',
  'type',
  'material',
  'shape',
  'symbol',
  'condition',
  'complete',
  'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_sign_rows.csv`), signRows, [
  'context',
  'sign',
  'context_rows',
  'a',
  'b',
  'c',
  'd',
  'share',
  'background_share',
  'relative_rate',
  'fisher_p',
]);

console.log(JSON.stringify(summary, null, 2));
