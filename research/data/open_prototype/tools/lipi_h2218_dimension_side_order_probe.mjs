import fs from 'node:fs';
import path from 'node:path';

// The H-2218..H-2239 tablets split into a canonical text arrangement ("A") and a side-swapped
// variant ("B_side_swap"). If the side-swapped tablets were also a different physical size,
// side order might just track a manufacturing batch rather than a writing convention. This
// script checks that confound. It reads the Fig. 4 mapping CSV for the 22-object series and
// computes four size metrics per tablet: horizontal mm, vertical mm, area, and aspect ratio
// (thickness is absent from the source, so it is excluded). It compares A versus B_side_swap
// with exact two-sided permutation tests (enumerating every group assignment), and tests the
// three manufacturing groups with a one-way F statistic against 20,000 seeded Monte Carlo
// label shuffles. Outputs: a per-tablet detail CSV, group summary CSV, test CSV, and JSON
// summary whose key observation states whether any size contrast is small enough (p < 0.05)
// to demand source validation. Size control only; no side function or reading is accepted.

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const inputCsv = path.join(reportsDir, 'lipi_h2218_h2239_fig4_mapping.csv');
const detailCsv = path.join(reportsDir, 'lipi_h2218_h2239_dimension_side_order.csv');
const classSummaryCsv = path.join(reportsDir, 'lipi_h2218_h2239_dimension_side_order_class_summary.csv');
const testCsv = path.join(reportsDir, 'lipi_h2218_h2239_dimension_side_order_tests.csv');
const outJson = path.join(reportsDir, 'lipi_h2218_h2239_dimension_side_order_summary.json');

const metrics = [
  { key: 'horizontal_mm', label: 'horizontal_mm' },
  { key: 'vertical_mm', label: 'vertical_mm' },
  { key: 'area_mm2', label: 'area_mm2' },
  { key: 'aspect_h_over_v', label: 'aspect_h_over_v' },
];

const monteCarloIterations = Number(process.env.IVC_H2218_DIMENSION_ITERATIONS ?? 20000);
const seedBase = 20260528;

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
      field = '';
      if (row.length > 1 || row[0] !== '') rows.push(row);
      row = [];
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

function csvObjects(text) {
  const rows = parseCsv(text);
  const header = rows.shift() ?? [];
  return rows.map((row) => Object.fromEntries(header.map((name, index) => [name, row[index] ?? ''])));
}

function toCsv(rows) {
  return `${rows
    .map((row) =>
      row
        .map((value) => {
          const text = String(value ?? '');
          return `"${text.replaceAll('"', '""')}"`;
        })
        .join(','),
    )
    .join('\n')}\n`;
}

function formatNumber(value) {
  return value === null || value === undefined || Number.isNaN(value) ? '' : Number(value.toFixed(6));
}

function parseNumber(value) {
  const n = Number.parseFloat(String(value ?? '').trim());
  return Number.isFinite(n) ? n : null;
}

function mean(values) {
  const clean = values.filter((v) => Number.isFinite(v));
  if (!clean.length) return null;
  return clean.reduce((sum, value) => sum + value, 0) / clean.length;
}

function variance(values) {
  const clean = values.filter((v) => Number.isFinite(v));
  if (clean.length <= 1) return null;
  const avg = mean(clean);
  return clean.reduce((sum, value) => sum + (value - avg) ** 2, 0) / (clean.length - 1);
}

function min(values) {
  const clean = values.filter((v) => Number.isFinite(v));
  return clean.length ? Math.min(...clean) : null;
}

function max(values) {
  const clean = values.filter((v) => Number.isFinite(v));
  return clean.length ? Math.max(...clean) : null;
}

function countBy(rows, keyFn) {
  const counts = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return counts;
}

function objectFromCounts(counts) {
  return Object.fromEntries([...counts.entries()].sort((a, b) => a[0].localeCompare(b[0], undefined, { numeric: true })));
}

function signatureFamily(signature) {
  if (signature === 'A') return 'A';
  if (signature === 'B_side_swap') return 'B_side_swap';
  return 'variant';
}

function chooseCombinations(n, k, visit) {
  const combo = [];
  function step(start, need) {
    if (need === 0) {
      visit(combo);
      return;
    }
    for (let i = start; i <= n - need; i++) {
      combo.push(i);
      step(i + 1, need - 1);
      combo.pop();
    }
  }
  step(0, k);
}

function exactTwoGroupPermutation(rows, labelKey, labelA, labelB, metricKey) {
  const selected = rows.filter((row) => row[labelKey] === labelA || row[labelKey] === labelB);
  const values = selected.map((row) => row[metricKey]).filter((value) => Number.isFinite(value));
  if (values.length !== selected.length) return null;

  const nA = selected.filter((row) => row[labelKey] === labelA).length;
  const nB = selected.filter((row) => row[labelKey] === labelB).length;
  if (nA < 2 || nB < 2) return null;

  const observedA = selected.filter((row) => row[labelKey] === labelA).map((row) => row[metricKey]);
  const observedB = selected.filter((row) => row[labelKey] === labelB).map((row) => row[metricKey]);
  const meanA = mean(observedA);
  const meanB = mean(observedB);
  const observedAbs = Math.abs(meanB - meanA);

  let total = 0;
  let extreme = 0;
  const allSum = values.reduce((sum, value) => sum + value, 0);
  chooseCombinations(values.length, nA, (combo) => {
    const inA = new Set(combo);
    let sumA = 0;
    for (const index of combo) sumA += values[index];
    const permMeanA = sumA / nA;
    const permMeanB = (allSum - sumA) / nB;
    const diff = Math.abs(permMeanB - permMeanA);
    total++;
    if (diff + 1e-12 >= observedAbs) extreme++;
    inA.clear();
  });

  return {
    n_a: nA,
    n_b: nB,
    mean_a: meanA,
    mean_b: meanB,
    mean_b_minus_a: meanB - meanA,
    abs_mean_diff: observedAbs,
    permutation_p_two_sided: extreme / total,
    permutation_space: total,
  };
}

function mulberry32(seed) {
  return function random() {
    let t = (seed += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
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

function shuffle(values, rng) {
  const out = values.slice();
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function oneWayF(rows, labelKey, metricKey) {
  const values = rows.map((row) => row[metricKey]).filter((value) => Number.isFinite(value));
  if (values.length !== rows.length) return null;
  const groups = [...countBy(rows, (row) => row[labelKey]).keys()].sort();
  if (groups.length < 2) return null;

  const grandMean = mean(values);
  let between = 0;
  let within = 0;
  for (const group of groups) {
    const groupValues = rows.filter((row) => row[labelKey] === group).map((row) => row[metricKey]);
    const groupMean = mean(groupValues);
    between += groupValues.length * (groupMean - grandMean) ** 2;
    within += groupValues.reduce((sum, value) => sum + (value - groupMean) ** 2, 0);
  }
  const dfBetween = groups.length - 1;
  const dfWithin = rows.length - groups.length;
  if (dfWithin <= 0 || within === 0) return null;
  return (between / dfBetween) / (within / dfWithin);
}

function monteCarloGroupF(rows, labelKey, metricKey, iterations, seed) {
  const observed = oneWayF(rows, labelKey, metricKey);
  if (observed === null) return null;
  const labels = rows.map((row) => row[labelKey]);
  const rng = mulberry32(seed);
  let extreme = 0;
  for (let i = 0; i < iterations; i++) {
    const shuffled = shuffle(labels, rng);
    const permRows = rows.map((row, index) => ({ ...row, [labelKey]: shuffled[index] }));
    const f = oneWayF(permRows, labelKey, metricKey);
    if (f !== null && f + 1e-12 >= observed) extreme++;
  }
  return {
    observed_f: observed,
    permutation_p_ge_observed_f: extreme / iterations,
    iterations,
  };
}

function metricSummary(rows, groupKey, metricKey) {
  const out = [];
  const groups = [...countBy(rows, (row) => row[groupKey]).keys()].sort();
  for (const group of groups) {
    const values = rows.filter((row) => row[groupKey] === group).map((row) => row[metricKey]);
    out.push({
      group_key: groupKey,
      group,
      metric: metricKey,
      n: values.length,
      mean: mean(values),
      variance: variance(values),
      min: min(values),
      max: max(values),
    });
  }
  return out;
}

const sourceRows = csvObjects(fs.readFileSync(inputCsv, 'utf8'));

const rows = sourceRows
  .map((row) => {
    const horizontal = parseNumber(row.local_horizontal_mm);
    const vertical = parseNumber(row.local_vertical_mm);
    const area = horizontal !== null && vertical !== null ? horizontal * vertical : null;
    const aspect = horizontal !== null && vertical !== null && vertical !== 0 ? horizontal / vertical : null;
    const signature = row.local_signature_short;
    return {
      cisi: row.cisi,
      fig4_number: Number.parseInt(row.fig4_number, 10),
      manufacturing_group: row.manufacturing_group,
      local_signature_short: signature,
      local_signature_family: signatureFamily(signature),
      side_1_text: row.side_1_text,
      side_2_text: row.side_2_text,
      side_3_text: row.side_3_text,
      horizontal_mm: horizontal,
      vertical_mm: vertical,
      area_mm2: area,
      aspect_h_over_v: aspect,
      interpretation_status: 'no_reading_admissible',
    };
  })
  .sort((a, b) => a.fig4_number - b.fig4_number);

const detailRows = [
  [
    'fig4_number',
    'manufacturing_group',
    'cisi',
    'local_signature_short',
    'local_signature_family',
    'horizontal_mm',
    'vertical_mm',
    'area_mm2',
    'aspect_h_over_v',
    'side_1_text',
    'side_2_text',
    'side_3_text',
    'interpretation_status',
  ],
];
for (const row of rows) {
  detailRows.push([
    row.fig4_number,
    row.manufacturing_group,
    row.cisi,
    row.local_signature_short,
    row.local_signature_family,
    formatNumber(row.horizontal_mm),
    formatNumber(row.vertical_mm),
    formatNumber(row.area_mm2),
    formatNumber(row.aspect_h_over_v),
    row.side_1_text,
    row.side_2_text,
    row.side_3_text,
    row.interpretation_status,
  ]);
}

const summaryRows = [
  ['group_key', 'group', 'metric', 'n', 'mean', 'variance', 'min', 'max'],
];
const summaries = [];
for (const groupKey of ['local_signature_short', 'local_signature_family', 'manufacturing_group']) {
  for (const metric of metrics) {
    summaries.push(...metricSummary(rows, groupKey, metric.key));
  }
}
for (const row of summaries) {
  summaryRows.push([
    row.group_key,
    row.group,
    row.metric,
    row.n,
    formatNumber(row.mean),
    formatNumber(row.variance),
    formatNumber(row.min),
    formatNumber(row.max),
  ]);
}

const testRows = [
  [
    'comparison',
    'metric',
    'group_a',
    'n_a',
    'mean_a',
    'group_b',
    'n_b',
    'mean_b',
    'mean_b_minus_a',
    'abs_mean_diff',
    'permutation_p',
    'permutation_detail',
    'interpretation',
  ],
];

const exactTests = [];
for (const metric of metrics) {
  const canonical = exactTwoGroupPermutation(rows, 'local_signature_short', 'A', 'B_side_swap', metric.key);
  if (canonical) {
    exactTests.push({
      comparison: 'canonical_A_vs_B_side_swap',
      metric: metric.key,
      group_a: 'A',
      group_b: 'B_side_swap',
      ...canonical,
    });
  }
  const family = exactTwoGroupPermutation(rows, 'local_signature_family', 'A', 'B_side_swap', metric.key);
  if (family) {
    exactTests.push({
      comparison: 'family_A_vs_B_side_swap',
      metric: metric.key,
      group_a: 'A',
      group_b: 'B_side_swap',
      ...family,
    });
  }
}

for (const test of exactTests) {
  testRows.push([
    test.comparison,
    test.metric,
    test.group_a,
    test.n_a,
    formatNumber(test.mean_a),
    test.group_b,
    test.n_b,
    formatNumber(test.mean_b),
    formatNumber(test.mean_b_minus_a),
    formatNumber(test.abs_mean_diff),
    formatNumber(test.permutation_p_two_sided),
    `exact_space=${test.permutation_space}`,
    'descriptive_size_control_only_no_reading',
  ]);
}

const groupTests = [];
for (const metric of metrics) {
  const result = monteCarloGroupF(
    rows,
    'manufacturing_group',
    metric.key,
    monteCarloIterations,
    seedBase + hashString(`manufacturing_group:${metric.key}`),
  );
  if (result) {
    groupTests.push({
      comparison: 'manufacturing_group_one_way',
      metric: metric.key,
      group_a: 'group_1;group_2;group_3',
      group_b: '',
      n_a: rows.length,
      n_b: '',
      mean_a: '',
      mean_b: '',
      mean_b_minus_a: '',
      abs_mean_diff: result.observed_f,
      permutation_p: result.permutation_p_ge_observed_f,
      permutation_detail: `monte_carlo_iterations=${result.iterations};observed_f=${formatNumber(result.observed_f)}`,
    });
  }
}

for (const test of groupTests) {
  testRows.push([
    test.comparison,
    test.metric,
    test.group_a,
    test.n_a,
    test.mean_a,
    test.group_b,
    test.n_b,
    test.mean_b,
    test.mean_b_minus_a,
    formatNumber(test.abs_mean_diff),
    formatNumber(test.permutation_p),
    test.permutation_detail,
    'descriptive_manufacturing_size_control_only_no_reading',
  ]);
}

const canonicalRows = rows.filter((row) => row.local_signature_short === 'A' || row.local_signature_short === 'B_side_swap');
const canonicalMinP = Math.min(
  ...exactTests
    .filter((test) => test.comparison === 'canonical_A_vs_B_side_swap')
    .map((test) => test.permutation_p_two_sided),
);
const strongestCanonical = exactTests
  .filter((test) => test.comparison === 'canonical_A_vs_B_side_swap')
  .sort((a, b) => a.permutation_p_two_sided - b.permutation_p_two_sided)[0];

const summary = {
  source: 'H-2218 through H-2239 dimension and side-order probe',
  input: path.relative(base, inputCsv).replaceAll('\\', '/'),
  source_rows: rows.length,
  canonical_signature_rows: canonicalRows.length,
  local_signature_counts: objectFromCounts(countBy(rows, (row) => row.local_signature_short)),
  manufacturing_group_counts: objectFromCounts(countBy(rows, (row) => row.manufacturing_group)),
  available_dimensions: {
    horizontal_mm_rows: rows.filter((row) => Number.isFinite(row.horizontal_mm)).length,
    vertical_mm_rows: rows.filter((row) => Number.isFinite(row.vertical_mm)).length,
    thickness_note: 'The local source has zero thickness values for this series, so thickness is excluded from this probe.',
  },
  exact_canonical_a_vs_b_tests: exactTests
    .filter((test) => test.comparison === 'canonical_A_vs_B_side_swap')
    .map((test) => ({
      metric: test.metric,
      n_a: test.n_a,
      mean_a: formatNumber(test.mean_a),
      n_b: test.n_b,
      mean_b: formatNumber(test.mean_b),
      mean_b_minus_a: formatNumber(test.mean_b_minus_a),
      permutation_p_two_sided: formatNumber(test.permutation_p_two_sided),
      permutation_space: test.permutation_space,
    })),
  strongest_canonical_size_difference: strongestCanonical
    ? {
        metric: strongestCanonical.metric,
        permutation_p_two_sided: formatNumber(strongestCanonical.permutation_p_two_sided),
        mean_b_minus_a: formatNumber(strongestCanonical.mean_b_minus_a),
      }
    : null,
  manufacturing_group_dimension_tests: groupTests.map((test) => ({
    metric: test.metric,
    observed_f: formatNumber(test.abs_mean_diff),
    permutation_p_ge_observed_f: formatNumber(test.permutation_p),
    iterations: monteCarloIterations,
  })),
  key_observation:
    canonicalMinP < 0.05
      ? 'At least one descriptive A versus side-swap dimension contrast is small enough to require image/source validation before treating side-order variation as independent of object size.'
      : 'In this 22-object source-anchored series, the A versus side-swap side-order split is not strongly separated by the available horizontal, vertical, area, or aspect measurements.',
  interpretation_boundary:
    'This is a size and manufacturing-control probe only. It accepts no physical side function, numerical value, metrological reading, sign meaning, phonetic value, language identity, or translation.',
  outputs: [detailCsv, classSummaryCsv, testCsv].map((file) => path.relative(base, file).replaceAll('\\', '/')),
};

fs.writeFileSync(detailCsv, toCsv(detailRows));
fs.writeFileSync(classSummaryCsv, toCsv(summaryRows));
fs.writeFileSync(testCsv, toCsv(testRows));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
