import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const inputCsv = path.join(reportsDir, 'lipi_tab_i_mixed_400_740_176_side_context.csv');
const outRowsCsv = path.join(reportsDir, 'lipi_tab_i_mixed_400_740_176_dimension_probe_rows.csv');
const outTestsCsv = path.join(reportsDir, 'lipi_tab_i_mixed_400_740_176_dimension_probe_tests.csv');
const outJson = path.join(reportsDir, 'lipi_tab_i_mixed_400_740_176_dimension_probe_summary.json');

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

function positiveNumber(value) {
  const text = String(value ?? '').trim();
  if (!/^(?:\d+(?:\.\d+)?|\.\d+)$/.test(text)) return null;
  const n = Number(text);
  return Number.isFinite(n) && n > 0 ? n : null;
}

function mean(values) {
  return values.reduce((a, b) => a + b, 0) / values.length;
}

function median(values) {
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
}

function round6(value) {
  if (value === null || value === undefined || Number.isNaN(value)) return '';
  return Number(value).toFixed(6);
}

function summarize(values) {
  if (!values.length) {
    return { n: 0, mean: '', median: '', min: '', max: '' };
  }
  return {
    n: values.length,
    mean: round6(mean(values)),
    median: round6(median(values)),
    min: round6(Math.min(...values)),
    max: round6(Math.max(...values)),
  };
}

function combinations(n, k, visitor) {
  const combo = [];
  function rec(start, remaining) {
    if (remaining === 0) {
      visitor(combo);
      return;
    }
    for (let i = start; i <= n - remaining; i++) {
      combo.push(i);
      rec(i + 1, remaining - 1);
      combo.pop();
    }
  }
  rec(0, k);
}

function exactMeanDiffTest(rows, metric, subset = 'all_target') {
  const eligible = rows
    .map((row) => ({ label: row.short_mark_class, value: row[metric] }))
    .filter((row) => (row.label === '033' || row.label === '034') && row.value !== null);
  const group033 = eligible.filter((row) => row.label === '033').map((row) => row.value);
  const group034 = eligible.filter((row) => row.label === '034').map((row) => row.value);
  if (!group033.length || !group034.length) {
    return {
      subset,
      metric,
      eligible_n: eligible.length,
      group_033_n: group033.length,
      group_034_n: group034.length,
      observed_mean_033: '',
      observed_mean_034: '',
      observed_abs_mean_diff: '',
      exact_two_sided_p: '',
      permutations: 0,
    };
  }

  const values = eligible.map((row) => row.value);
  const total = values.reduce((a, b) => a + b, 0);
  const k = group033.length;
  const observedDiff = Math.abs(mean(group033) - mean(group034));
  let permutations = 0;
  let extreme = 0;
  const epsilon = 1e-12;

  combinations(values.length, k, (combo) => {
    const selected = new Set(combo);
    let sumA = 0;
    for (const index of selected) sumA += values[index];
    const sumB = total - sumA;
    const diff = Math.abs(sumA / k - sumB / (values.length - k));
    permutations++;
    if (diff + epsilon >= observedDiff) extreme++;
  });

  return {
    subset,
    metric,
    eligible_n: eligible.length,
    group_033_n: group033.length,
    group_034_n: group034.length,
    observed_mean_033: round6(mean(group033)),
    observed_mean_034: round6(mean(group034)),
    observed_abs_mean_diff: round6(observedDiff),
    exact_two_sided_p: round6(extreme / permutations),
    permutations,
  };
}

function logFactorials(n) {
  const logs = [0];
  for (let i = 1; i <= n; i++) logs[i] = logs[i - 1] + Math.log(i);
  return logs;
}

function logChoose(logs, n, k) {
  if (k < 0 || k > n) return Number.NEGATIVE_INFINITY;
  return logs[n] - logs[k] - logs[n - k];
}

function hypergeomProb(logs, a, row1, col1, total) {
  const col2 = total - col1;
  return Math.exp(logChoose(logs, col1, a) + logChoose(logs, col2, row1 - a) - logChoose(logs, total, row1));
}

function fisherTwoSided(a, b, c, d) {
  const row1 = a + b;
  const row2 = c + d;
  const col1 = a + c;
  const total = row1 + row2;
  const logs = logFactorials(total);
  const observed = hypergeomProb(logs, a, row1, col1, total);
  const minA = Math.max(0, row1 - (total - col1));
  const maxA = Math.min(row1, col1);
  let p = 0;
  for (let x = minA; x <= maxA; x++) {
    const prob = hypergeomProb(logs, x, row1, col1, total);
    if (prob <= observed + 1e-12) p += prob;
  }
  return p;
}

function exactPlacementTest(rows, positiveFn, name, subset = 'all_target') {
  const eligible = rows.filter((row) => row.short_mark_class === '033' || row.short_mark_class === '034');
  const a = eligible.filter((row) => row.short_mark_class === '033' && positiveFn(row)).length;
  const b = eligible.filter((row) => row.short_mark_class === '033' && !positiveFn(row)).length;
  const c = eligible.filter((row) => row.short_mark_class === '034' && positiveFn(row)).length;
  const d = eligible.filter((row) => row.short_mark_class === '034' && !positiveFn(row)).length;
  return {
    subset,
    metric: name,
    eligible_n: eligible.length,
    group_033_n: a + b,
    group_034_n: c + d,
    observed_mean_033: `${a}/${a + b}`,
    observed_mean_034: `${c}/${c + d}`,
    observed_abs_mean_diff: round6(Math.abs(a / (a + b) - c / (c + d))),
    exact_two_sided_p: round6(fisherTwoSided(a, b, c, d)),
    permutations: 'fisher_exact',
  };
}

function addCorrections(tests) {
  const corrected = tests.map((test) => ({ ...test }));
  const numericTests = corrected.filter((test) => Number.isFinite(Number.parseFloat(test.exact_two_sided_p)));
  const m = numericTests.length;
  for (const test of numericTests) {
    const p = Number.parseFloat(test.exact_two_sided_p);
    test.bonferroni_p = round6(Math.min(1, p * m));
  }

  const sorted = [...numericTests].sort(
    (a, b) => Number.parseFloat(a.exact_two_sided_p) - Number.parseFloat(b.exact_two_sided_p),
  );
  let previous = 1;
  for (let i = sorted.length - 1; i >= 0; i--) {
    const p = Number.parseFloat(sorted[i].exact_two_sided_p);
    const adjusted = Math.min(previous, (p * m) / (i + 1));
    sorted[i].bh_fdr_p = round6(Math.min(1, adjusted));
    previous = adjusted;
  }

  for (const test of corrected) {
    test.bonferroni_p ??= '';
    test.bh_fdr_p ??= '';
    test.raw_p_lte_005 = Number.parseFloat(test.exact_two_sided_p) <= 0.05 ? 'true' : 'false';
    test.bonferroni_lte_005 = Number.parseFloat(test.bonferroni_p) <= 0.05 ? 'true' : 'false';
    test.bh_fdr_lte_005 = Number.parseFloat(test.bh_fdr_p) <= 0.05 ? 'true' : 'false';
  }
  return corrected;
}

const rows = csvObjects(fs.readFileSync(inputCsv, 'utf8')).map((row) => {
  const h = positiveNumber(row.horizontal_mm);
  const v = positiveNumber(row.vertical_mm);
  const area = h !== null && v !== null ? h * v : null;
  const aspect = h !== null && v !== null ? h / v : null;
  return {
    ...row,
    horizontal_value: h,
    vertical_value: v,
    area_value: area,
    aspect_value: aspect,
    is_two_side: row.context_class === 'two_side_long1_short2' || row.context_class === 'two_side_short1_long2',
    is_long1_short2: row.context_class === 'two_side_long1_short2',
    has_extra_side: row.row_count !== '2',
  };
});

const rowCsv = [
  [
    'cisi',
    'short_mark_class',
    'context_class',
    'horizontal_value',
    'vertical_value',
    'area_value',
    'aspect_value',
    'dimension_status',
    'source_status',
  ],
];
for (const row of rows) {
  rowCsv.push([
    row.cisi,
    row.short_mark_class,
    row.context_class,
    round6(row.horizontal_value),
    round6(row.vertical_value),
    round6(row.area_value),
    round6(row.aspect_value),
    row.horizontal_value !== null && row.vertical_value !== null ? 'positive_horizontal_and_vertical' : 'missing_or_zero_dimension',
    row.source_status,
  ]);
}

const twoSideRows = rows.filter((row) => row.is_two_side);
const canonicalRows = rows.filter((row) => row.context_class === 'two_side_long1_short2');

const tests = addCorrections([
  exactPlacementTest(rows, (row) => row.is_long1_short2, 'short_mark_predicts_two_side_long1_short2'),
  exactPlacementTest(rows, (row) => row.has_extra_side, 'short_mark_predicts_extra_side_case'),
  exactMeanDiffTest(rows, 'horizontal_value'),
  exactMeanDiffTest(rows, 'vertical_value'),
  exactMeanDiffTest(rows, 'area_value'),
  exactMeanDiffTest(rows, 'aspect_value'),
  exactMeanDiffTest(twoSideRows, 'horizontal_value', 'two_side_only'),
  exactMeanDiffTest(twoSideRows, 'vertical_value', 'two_side_only'),
  exactMeanDiffTest(twoSideRows, 'area_value', 'two_side_only'),
  exactMeanDiffTest(twoSideRows, 'aspect_value', 'two_side_only'),
  exactMeanDiffTest(canonicalRows, 'horizontal_value', 'two_side_long1_short2_only'),
  exactMeanDiffTest(canonicalRows, 'vertical_value', 'two_side_long1_short2_only'),
  exactMeanDiffTest(canonicalRows, 'area_value', 'two_side_long1_short2_only'),
  exactMeanDiffTest(canonicalRows, 'aspect_value', 'two_side_long1_short2_only'),
]);

const testsCsv = [
  [
    'subset',
    'metric',
    'eligible_n',
    'group_033_n',
    'group_034_n',
    'observed_mean_033',
    'observed_mean_034',
    'observed_abs_mean_diff',
    'exact_two_sided_p',
    'bonferroni_p',
    'bh_fdr_p',
    'raw_p_lte_005',
    'bonferroni_lte_005',
    'bh_fdr_lte_005',
    'permutations',
  ],
];
for (const test of tests) {
  testsCsv.push([
    test.subset,
    test.metric,
    test.eligible_n,
    test.group_033_n,
    test.group_034_n,
    test.observed_mean_033,
    test.observed_mean_034,
    test.observed_abs_mean_diff,
    test.exact_two_sided_p,
    test.bonferroni_p,
    test.bh_fdr_p,
    test.raw_p_lte_005,
    test.bonferroni_lte_005,
    test.bh_fdr_lte_005,
    test.permutations,
  ]);
}

const byShort = {};
for (const label of ['033', '034']) {
  const subset = rows.filter((row) => row.short_mark_class === label);
  byShort[label] = {
    artifacts: subset.length,
    context_counts: Object.fromEntries(
      [...new Set(rows.map((row) => row.context_class))]
        .sort()
        .map((context) => [context, subset.filter((row) => row.context_class === context).length]),
    ),
    horizontal: summarize(subset.map((row) => row.horizontal_value).filter((value) => value !== null)),
    vertical: summarize(subset.map((row) => row.vertical_value).filter((value) => value !== null)),
    area: summarize(subset.map((row) => row.area_value).filter((value) => value !== null)),
    aspect: summarize(subset.map((row) => row.aspect_value).filter((value) => value !== null)),
  };
}

const summary = {
  source: 'TAB:I mixed +400-740-176+ pre-validation dimension probe',
  checked_at: '2026-05-24',
  input: path.relative(base, inputCsv).replaceAll('\\', '/'),
  target_artifacts: rows.length,
  two_side_artifacts: twoSideRows.length,
  canonical_long1_short2_artifacts: canonicalRows.length,
  short_mark_summary: byShort,
  tests: Object.fromEntries(tests.map((test) => [`${test.subset}:${test.metric}`, test])),
  raw_p_lte_005_tests: tests
    .filter((test) => Number.parseFloat(test.exact_two_sided_p) <= 0.05)
    .map((test) => `${test.subset}:${test.metric}`),
  bonferroni_lte_005_tests: tests
    .filter((test) => Number.parseFloat(test.bonferroni_p) <= 0.05)
    .map((test) => `${test.subset}:${test.metric}`),
  bh_fdr_lte_005_tests: tests
    .filter((test) => Number.parseFloat(test.bh_fdr_p) <= 0.05)
    .map((test) => `${test.subset}:${test.metric}`),
  multiple_test_note:
    'Bonferroni and Benjamini-Hochberg corrections are applied across the emitted exact tests. Surviving no corrected threshold is not proof of no structure; it blocks promotion from triage flag to evidence.',
  key_observation:
    'In the current T3 planning layer, +700-033+ and +700-034+ show weak raw horizontal/aspect splits in the all-target layer, weaker two-side-only echoes, and no surviving corrected signal; the canonical long1-short2 subset weakens the signal.',
  interpretation_boundary:
    'This probe is a pre-validation stress test only. It accepts no numerical value, metrological reading, physical side function, sign meaning, phonetic value, language identity, or translation.',
  outputs: [
    path.relative(base, outRowsCsv).replaceAll('\\', '/'),
    path.relative(base, outTestsCsv).replaceAll('\\', '/'),
    path.relative(base, outJson).replaceAll('\\', '/'),
  ],
};

fs.writeFileSync(outRowsCsv, toCsv(rowCsv));
fs.writeFileSync(outTestsCsv, toCsv(testsCsv));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
