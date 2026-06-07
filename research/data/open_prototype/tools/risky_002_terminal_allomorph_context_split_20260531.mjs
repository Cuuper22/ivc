import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_002_terminal_allomorph_context_split_20260531';
const RUN_DATE = '2026-05-31';
const TERMINALS = ['861', '820', '817'];
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
  for (let x = a; x <= max; x += 1) p += Math.exp(logChoose(row1, x) + logChoose(row2, col1 - x) - logDen);
  return Math.max(0, Math.min(1, p));
}

function entropy(counts) {
  const n = counts.reduce((sum, value) => sum + value, 0);
  let h = 0;
  for (const count of counts) {
    if (!count) continue;
    const p = count / n;
    h -= p * Math.log2(p);
  }
  return h;
}

function mutualInformation(rows, feature) {
  const partnerCounts = new Map();
  const featureCounts = new Map();
  const joint = new Map();
  for (const row of rows) {
    const p = row.partner;
    const f = row[feature];
    partnerCounts.set(p, (partnerCounts.get(p) ?? 0) + 1);
    featureCounts.set(f, (featureCounts.get(f) ?? 0) + 1);
    joint.set(`${p}|${f}`, (joint.get(`${p}|${f}`) ?? 0) + 1);
  }
  const n = rows.length;
  let mi = 0;
  for (const [key, count] of joint.entries()) {
    const [p, f] = key.split('|');
    const pxy = count / n;
    const px = partnerCounts.get(p) / n;
    const py = featureCounts.get(f) / n;
    mi += pxy * Math.log2(pxy / (px * py));
  }
  return mi;
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

const FEATURE_FIELDS = ['type', 'site', 'symbol', 'material', 'shape', 'condition', 'complete', 'prev', 'first'];

function featureRows(rows) {
  const out = [];
  for (const feature of FEATURE_FIELDS) {
    const values = [...new Set(rows.map((row) => row[feature]))].filter((value) => value && value !== 'NA');
    for (const value of values) {
      for (const terminal of TERMINALS) {
        const partnerRows = rows.filter((row) => row.partner === terminal);
        const otherRows = rows.filter((row) => row.partner !== terminal);
        const a = partnerRows.filter((row) => row[feature] === value).length;
        const b = otherRows.filter((row) => row[feature] === value).length;
        if (a < 5) continue;
        const p = fisherRightTail(a, partnerRows.length - a, b, otherRows.length - b);
        out.push({
          terminal,
          feature,
          value,
          a,
          terminal_rows: partnerRows.length,
          b,
          other_rows: otherRows.length,
          terminal_share: a / partnerRows.length,
          other_share: b / otherRows.length,
          fisher_p: p,
        });
      }
    }
  }
  return out.sort((x, y) => x.fisher_p - y.fisher_p || y.a - x.a);
}

function maxFeatureForger(rows, observedP, observedMaxMi, iterations = ITERATIONS) {
  const rand = mulberry32(0x002817 ^ rows.length);
  const partners = rows.map((row) => row.partner);
  const iterationRows = [];
  let pLe = 0;
  let miGe = 0;
  for (let iter = 0; iter < iterations; iter += 1) {
    const shuffled = partners.slice();
    shuffleInPlace(shuffled, rand);
    const fakeRows = rows.map((row, idx) => ({ ...row, partner: shuffled[idx] }));
    const top = featureRows(fakeRows)[0] ?? { fisher_p: 1, terminal: '', feature: '', value: '', a: 0 };
    const maxMi = Math.max(...FEATURE_FIELDS.map((feature) => mutualInformation(fakeRows, feature)));
    if (top.fisher_p <= observedP) pLe += 1;
    if (maxMi >= observedMaxMi) miGe += 1;
    if (iter < 50 || top.fisher_p <= observedP || maxMi >= observedMaxMi) {
      iterationRows.push({
        iteration: iter,
        best_terminal: top.terminal,
        best_feature: top.feature,
        best_value: top.value,
        best_a: top.a,
        best_fisher_p: top.fisher_p,
        max_mi_bits: maxMi,
        p_le_observed: String(top.fisher_p <= observedP),
        mi_ge_observed: String(maxMi >= observedMaxMi),
      });
    }
  }
  return { iterations, feature_maxstat_fpr: pLe / iterations, mi_maxstat_fpr: miGe / iterations, iteration_rows: iterationRows };
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()];
const terminalRows = [];
for (const row of canonicalRows) {
  for (let idx = 0; idx < row.signs.length - 1; idx += 1) {
    const next = row.signs[idx + 1];
    if (row.signs[idx] !== '002' || !TERMINALS.includes(next)) continue;
    terminalRows.push({
      object: objectId(row),
      site: norm(row.site),
      region: norm(row.region),
      type: norm(row.type),
      material: norm(row.material),
      shape: norm(row.shape),
      symbol: norm(row.symbol),
      condition: norm(row.condition),
      complete: norm(row.complete),
      first: row.signs[0] ?? '<NONE>',
      prev: row.signs[idx - 1] ?? '<START>',
      partner: next,
      text: row.text,
    });
  }
}

const features = featureRows(terminalRows);
const observedTop = features[0];
const miRows = FEATURE_FIELDS.map((feature) => ({
  feature,
  mi_bits: mutualInformation(terminalRows, feature),
})).sort((a, b) => b.mi_bits - a.mi_bits);
const nulls = maxFeatureForger(terminalRows, observedTop.fisher_p, miRows[0].mi_bits);
const partnerCounts = TERMINALS.map((terminal) => ({
  terminal,
  count: terminalRows.filter((row) => row.partner === terminal).length,
}));

const positiveBetKilled =
  observedTop.fisher_p * features.length > 0.05 &&
  nulls.feature_maxstat_fpr > 0.05 &&
  nulls.mi_maxstat_fpr > 0.05;
const tier = positiveBetKilled ? 'wild shot killed' : 'candidate';

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V2_V4_002_TERMINAL_ALLOMORPH_CONTEXT_SPLIT_20260531',
  vector: 'V2 slot grammar; V4 context-to-meaning without sound',
  confidence_tier: tier,
  risky_bet:
    'Positive bet tested: the three `002` terminal partners `861`, `820`, and `817` encode context-conditioned terminal allomorph classes, separable by object type, site, iconography, material, shape, preservation, previous sign, or first sign.',
  observed:
    `Terminal rows=${terminalRows.length}; partner counts=${partnerCounts.map((row) => `${row.terminal}:${row.count}`).join(';')}. ` +
    `Best feature=${observedTop.terminal}/${observedTop.feature}:${observedTop.value} with ${observedTop.a}/${observedTop.terminal_rows} vs ${observedTop.b}/${observedTop.other_rows}, Fisher=${observedTop.fisher_p}, Bonferroni=${Math.min(1, observedTop.fisher_p * features.length)}. ` +
    `Best MI feature=${miRows[0].feature}, MI=${miRows[0].mi_bits} bits. Feature max-stat FPR=${nulls.feature_maxstat_fpr}; MI max-stat FPR=${nulls.mi_maxstat_fpr}.`,
  adversarial_test:
    `Exhaustive scan over ${FEATURE_FIELDS.join('/')} for each terminal partner; Bonferroni over ${features.length} tested feature-partner cells; ${ITERATIONS}-iteration partner-label shuffle preserving terminal partner counts and all row features; parallel max-stat over best Fisher feature and max mutual information.`,
  false_positive_rate: Math.max(nulls.feature_maxstat_fpr, nulls.mi_maxstat_fpr),
  feature_maxstat_fpr: nulls.feature_maxstat_fpr,
  mi_maxstat_fpr: nulls.mi_maxstat_fpr,
  positive_bet_verdict: positiveBetKilled ? 'killed_by_maxstat_partner_label_forger' : 'survives_as_candidate',
  falsifier:
    'If a future source-checked or expanded terminal corpus yields a partner/context feature whose max-stat FPR is <=0.01 and survives leave-site controls, revive context-conditioned terminal classes. Current data does not earn that split.',
  next_prediction:
    'Until stronger evidence appears, treat 861/820/817 as a weakly differentiated terminal-partner set after 002, not as context-readable semantic classes. The earned claim remains the 002 pre-terminal bridge, not the meaning of each terminal partner.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({ ...summary, partner_counts: partnerCounts, top_features: features.slice(0, 80), mi_rows: miRows, terminal_rows: terminalRows }, null, 2),
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
  'feature_maxstat_fpr',
  'mi_maxstat_fpr',
  'positive_bet_verdict',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_top_features.csv`), features.slice(0, 120), [
  'terminal',
  'feature',
  'value',
  'a',
  'terminal_rows',
  'b',
  'other_rows',
  'terminal_share',
  'other_share',
  'fisher_p',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_mi.csv`), miRows, ['feature', 'mi_bits']);
writeCsv(path.join(OUT_DIR, `${PREFIX}_terminal_rows.csv`), terminalRows, [
  'object',
  'site',
  'region',
  'type',
  'material',
  'shape',
  'symbol',
  'condition',
  'complete',
  'first',
  'prev',
  'partner',
  'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_forger_iterations.csv`), nulls.iteration_rows, [
  'iteration',
  'best_terminal',
  'best_feature',
  'best_value',
  'best_a',
  'best_fisher_p',
  'max_mi_bits',
  'p_le_observed',
  'mi_ge_observed',
]);

console.log(JSON.stringify(summary, null, 2));
