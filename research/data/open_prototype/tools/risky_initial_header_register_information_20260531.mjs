import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_initial_header_register_information_20260531';
const RUN_DATE = '2026-05-31';
const ITERATIONS = 3000;

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

function carrierClass(row) {
  const type = norm(row.type);
  if (['TAB:B', 'TAB:I'].includes(type)) return 'tablet_account_TAB_BI';
  if (['SEAL:R', 'TAB:C'].includes(type)) return 'rect_copper_SEALR_TABC';
  if (type === 'SEAL:S') return 'square_seal_SEALS';
  if (['POT:T:g', 'POT:T:s'].includes(type)) return 'pottery_graffiti_POT';
  if (['SEAL:C', 'SEAL:CY'].includes(type)) return 'round_cylinder_seal';
  if (['TAG', 'TAG:R'].includes(type)) return 'tag';
  return 'other';
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

function mutualInformation(rows, initialSelector = (row) => row.signs[0], classSelector = (row) => row.carrier_class) {
  const n = rows.length;
  const joint = new Map();
  const sx = new Map();
  const cy = new Map();
  for (const row of rows) {
    const x = initialSelector(row) ?? '<NONE>';
    const y = classSelector(row);
    joint.set(`${x}|${y}`, (joint.get(`${x}|${y}`) ?? 0) + 1);
    sx.set(x, (sx.get(x) ?? 0) + 1);
    cy.set(y, (cy.get(y) ?? 0) + 1);
  }
  let mi = 0;
  for (const [key, count] of joint.entries()) {
    const [x, y] = key.split('|');
    const pxy = count / n;
    const px = sx.get(x) / n;
    const py = cy.get(y) / n;
    mi += pxy * Math.log2(pxy / (px * py));
  }
  return mi;
}

function contributionRows(rows) {
  const n = rows.length;
  const firstCounts = new Map();
  const classCounts = new Map();
  const jointCounts = new Map();
  for (const row of rows) {
    const first = row.signs[0] ?? '<NONE>';
    const klass = row.carrier_class;
    firstCounts.set(first, (firstCounts.get(first) ?? 0) + 1);
    classCounts.set(klass, (classCounts.get(klass) ?? 0) + 1);
    jointCounts.set(`${first}|${klass}`, (jointCounts.get(`${first}|${klass}`) ?? 0) + 1);
  }
  return [...jointCounts.entries()].map(([key, count]) => {
    const [first_sign, carrier_class] = key.split('|');
    const expected = (firstCounts.get(first_sign) * classCounts.get(carrier_class)) / n;
    const log2_lift = Math.log2(count / expected);
    const mi_contribution_bits = (count / n) * log2_lift;
    return {
      first_sign,
      carrier_class,
      observed: count,
      expected,
      first_sign_total: firstCounts.get(first_sign),
      class_total: classCounts.get(carrier_class),
      log2_lift,
      mi_contribution_bits,
    };
  }).sort((a, b) => b.mi_contribution_bits - a.mi_contribution_bits || b.observed - a.observed);
}

function forgers(rows, observedMi, iterations = ITERATIONS) {
  const rand = mulberry32(0x5157a11 ^ rows.length);
  let rowInternalGe = 0;
  let classLabelGe = 0;
  const classLabels = rows.map((row) => row.carrier_class);
  const iterationRows = [];
  for (let iter = 0; iter < iterations; iter += 1) {
    const rowInternalRows = rows.map((row) => {
      const signs = row.signs.slice();
      shuffleInPlace(signs, rand);
      return { ...row, signs };
    });
    const classShuffle = classLabels.slice();
    shuffleInPlace(classShuffle, rand);
    const classShuffleRows = rows.map((row, idx) => ({ ...row, carrier_class: classShuffle[idx] }));
    const rowInternalMi = mutualInformation(rowInternalRows);
    const classLabelMi = mutualInformation(classShuffleRows);
    if (rowInternalMi >= observedMi) rowInternalGe += 1;
    if (classLabelMi >= observedMi) classLabelGe += 1;
    if (iter < 50 || rowInternalMi >= observedMi || classLabelMi >= observedMi) {
      iterationRows.push({
        iteration: iter,
        row_internal_mi_bits: rowInternalMi,
        class_label_shuffle_mi_bits: classLabelMi,
        row_internal_ge_observed: String(rowInternalMi >= observedMi),
        class_label_ge_observed: String(classLabelMi >= observedMi),
      });
    }
  }
  return {
    iterations,
    row_internal_fpr: rowInternalGe / iterations,
    class_label_shuffle_fpr: classLabelGe / iterations,
    iteration_rows: iterationRows,
  };
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()]
  .filter((row) => row.signs.length > 0)
  .map((row) => ({ ...row, carrier_class: carrierClass(row) }));
const observedMi = mutualInformation(canonicalRows);
const nulls = forgers(canonicalRows, observedMi);
const contributions = contributionRows(canonicalRows);
const classCounts = Object.entries(canonicalRows.reduce((acc, row) => {
  acc[row.carrier_class] = (acc[row.carrier_class] ?? 0) + 1;
  return acc;
}, {})).map(([carrier_class, count]) => ({ carrier_class, count })).sort((a, b) => b.count - a.count);
const topContributionText = contributions.slice(0, 10).map((row) =>
  `${row.first_sign}->${row.carrier_class}:${row.observed} obs, lift=${row.log2_lift.toFixed(3)} bits, contribution=${row.mi_contribution_bits.toFixed(4)}`,
).join('; ');

const tier =
  observedMi >= 0.1 &&
  nulls.row_internal_fpr <= 0.01 &&
  nulls.class_label_shuffle_fpr <= 0.01
    ? 'promoted candidate'
    : 'candidate';

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V2_V4_INITIAL_HEADER_REGISTER_INFORMATION_20260531',
  vector: 'V2 effective unicity / structural constraint; V4 context-to-meaning',
  confidence_tier: tier,
  risky_bet:
    'The first sign is a carrier/register header slot: its identity carries substantial information about object class, above what would be expected if sign order were arbitrary within rows or if carrier labels were unrelated to initial signs.',
  observed:
    `Canonical rows=${canonicalRows.length}; I(first sign; carrier class)=${observedMi} bits. Row-internal shuffle FPR=${nulls.row_internal_fpr}; carrier-label shuffle FPR=${nulls.class_label_shuffle_fpr}. Carrier classes: ${classCounts.map((row) => `${row.carrier_class}:${row.count}`).join(';')}. Top contributors: ${topContributionText}.`,
  adversarial_test:
    `Canonical numeric-sequence collapse; mutual information between initial sign and carrier class; ${ITERATIONS}-iteration row-internal sign shuffle preserving every row's sign multiset and length; ${ITERATIONS}-iteration carrier-label shuffle preserving first-sign and class marginals.`,
  false_positive_rate: Math.max(nulls.row_internal_fpr, nulls.class_label_shuffle_fpr),
  row_internal_shuffle_fpr: nulls.row_internal_fpr,
  class_label_shuffle_fpr: nulls.class_label_shuffle_fpr,
  observed_mi_bits: observedMi,
  falsifier:
    'If source-checked rows or expanded corpora reduce the initial-sign/carrier-class mutual information to the row-internal shuffle range, or if top contributors are mostly damaged/placeholder signs, demote this from header-slot structure to corpus/catalog artifact.',
  next_prediction:
    'Held-out object rows should retain class-specific first signs: 400 for TAB:B/I, 740 and 407 for administrative rectangular/copper rows, and separate high-contribution headers for pottery/tag/round-seal classes. This supports structural parsing but no phonetic reading.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({ ...summary, class_counts: classCounts, top_contributions: contributions.slice(0, 60) }, null, 2),
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
  'row_internal_shuffle_fpr',
  'class_label_shuffle_fpr',
  'observed_mi_bits',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_class_counts.csv`), classCounts, ['carrier_class', 'count']);
writeCsv(path.join(OUT_DIR, `${PREFIX}_top_contributions.csv`), contributions.slice(0, 100), [
  'first_sign',
  'carrier_class',
  'observed',
  'expected',
  'first_sign_total',
  'class_total',
  'log2_lift',
  'mi_contribution_bits',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_forger_iterations.csv`), nulls.iteration_rows, [
  'iteration',
  'row_internal_mi_bits',
  'class_label_shuffle_mi_bits',
  'row_internal_ge_observed',
  'class_label_ge_observed',
]);

console.log(JSON.stringify(summary, null, 2));
