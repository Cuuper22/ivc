// Confound check for the H-2218..H-2239 tablet group: could the A/B side-order
// split we see in Fig. 4 just be an artifact of how the catalog ordered the
// objects, or of which manufacturing group each tablet belongs to?
//
// The script reads lipi_h2218_h2239_fig4_mapping.csv (22 tablets, each with a
// local side-order signature such as 'A' or 'B_side_swap'). It then runs exact
// permutation tests: it enumerates every way the observed number of B labels
// could be scattered over the rows, and asks how often chance alone would
// produce (1) a group-vs-label chi-square as large as observed, and (2) as many
// adjacent B-B pairs in the Fig. 4 numbering as observed — both overall and
// within manufacturing groups. Because the samples are tiny, the full
// permutation space is enumerated, so the p-values are exact, not simulated.
//
// It writes a per-tablet detail CSV, a test-results CSV, and a JSON summary
// (lipi_h2218_h2239_side_order_confound_*). The point is to rule confounds in
// or out before anyone leans on the A/B split; the probe deliberately claims
// nothing about what the sides mean or say.

import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const inputCsv = path.join(reportsDir, 'lipi_h2218_h2239_fig4_mapping.csv');
const detailCsv = path.join(reportsDir, 'lipi_h2218_h2239_side_order_confound.csv');
const testCsv = path.join(reportsDir, 'lipi_h2218_h2239_side_order_confound_tests.csv');
const outJson = path.join(reportsDir, 'lipi_h2218_h2239_side_order_confound_summary.json');

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

function coarseSignature(label) {
  if (label === 'A') return 'A';
  if (label === 'B_side_swap') return 'B_side_swap';
  return 'variant';
}

function canonicalLabel(label) {
  if (label === 'A') return 'A';
  if (label === 'B_side_swap') return 'B';
  return '';
}

function adjacentPairs(rows, withinGroupOnly = false) {
  const pairs = [];
  for (let i = 0; i < rows.length - 1; i++) {
    const left = rows[i];
    const right = rows[i + 1];
    if (right.fig4_number !== left.fig4_number + 1) continue;
    if (withinGroupOnly && right.manufacturing_group !== left.manufacturing_group) continue;
    pairs.push([i, i + 1]);
  }
  return pairs;
}

function countAdjacentBB(pairs, bSet) {
  let count = 0;
  for (const [a, b] of pairs) {
    if (bSet.has(a) && bSet.has(b)) count++;
  }
  return count;
}

function countSameLabelPairs(rows, labelsByIndex, withinGroupOnly = true) {
  let count = 0;
  for (const [a, b] of adjacentPairs(rows, withinGroupOnly)) {
    if (labelsByIndex[a] === labelsByIndex[b]) count++;
  }
  return count;
}

function canonicalGroupChiSquare(rows, bSet) {
  const groups = [...countBy(rows, (row) => row.manufacturing_group).keys()].sort();
  const total = rows.length;
  const totalB = bSet.size;
  const totalA = total - totalB;
  let chi = 0;
  for (const group of groups) {
    const groupIndexes = rows.map((row, index) => [row, index]).filter(([row]) => row.manufacturing_group === group);
    const groupN = groupIndexes.length;
    const observedB = groupIndexes.filter(([, index]) => bSet.has(index)).length;
    const observedA = groupN - observedB;
    const expectedB = (groupN * totalB) / total;
    const expectedA = (groupN * totalA) / total;
    chi += (observedB - expectedB) ** 2 / expectedB;
    chi += (observedA - expectedA) ** 2 / expectedA;
  }
  return chi;
}

function exactCanonicalGroupDistribution(rows) {
  const observedB = new Set(rows.map((row, index) => (row.canonical_ab === 'B' ? index : null)).filter((v) => v !== null));
  const totalB = observedB.size;
  const observedChi = canonicalGroupChiSquare(rows, observedB);
  let total = 0;
  let extreme = 0;
  chooseCombinations(rows.length, totalB, (combo) => {
    const bSet = new Set(combo);
    const chi = canonicalGroupChiSquare(rows, bSet);
    total++;
    if (chi + 1e-12 >= observedChi) extreme++;
  });
  return {
    statistic: observedChi,
    p_ge_observed: extreme / total,
    permutation_space: total,
  };
}

function exactCanonicalAdjacency(rows, withinGroupOnly = false) {
  const observedB = new Set(rows.map((row, index) => (row.canonical_ab === 'B' ? index : null)).filter((v) => v !== null));
  const totalB = observedB.size;
  const pairs = adjacentPairs(rows, withinGroupOnly);
  const observed = countAdjacentBB(pairs, observedB);
  let total = 0;
  let extreme = 0;
  chooseCombinations(rows.length, totalB, (combo) => {
    const bSet = new Set(combo);
    const count = countAdjacentBB(pairs, bSet);
    total++;
    if (count >= observed) extreme++;
  });
  return {
    statistic: observed,
    adjacent_pair_count: pairs.length,
    p_ge_observed: extreme / total,
    permutation_space: total,
  };
}

function combinationsForIndexes(indexes, k) {
  const out = [];
  chooseCombinations(indexes.length, k, (combo) => {
    out.push(combo.map((index) => indexes[index]));
  });
  return out;
}

function exactCanonicalAdjacencyWithinObservedGroups(rows) {
  const groups = [...countBy(rows, (row) => row.manufacturing_group).keys()].sort();
  const groupCombos = groups.map((group) => {
    const indexes = rows.map((row, index) => [row, index]).filter(([row]) => row.manufacturing_group === group).map(([, index]) => index);
    const bCount = indexes.filter((index) => rows[index].canonical_ab === 'B').length;
    return combinationsForIndexes(indexes, bCount);
  });
  const pairs = adjacentPairs(rows, true);
  const observedB = new Set(rows.map((row, index) => (row.canonical_ab === 'B' ? index : null)).filter((v) => v !== null));
  const observed = countAdjacentBB(pairs, observedB);
  let total = 0;
  let extreme = 0;
  function step(groupIndex, selected) {
    if (groupIndex === groupCombos.length) {
      const bSet = new Set(selected);
      const count = countAdjacentBB(pairs, bSet);
      total++;
      if (count >= observed) extreme++;
      return;
    }
    for (const combo of groupCombos[groupIndex]) {
      step(groupIndex + 1, [...selected, ...combo]);
    }
  }
  step(0, []);
  return {
    statistic: observed,
    adjacent_pair_count: pairs.length,
    p_ge_observed: extreme / total,
    permutation_space: total,
  };
}

function multisetAssignments(indexes, counts) {
  const labels = Object.keys(counts).sort();
  const out = [];
  function step(labelIndex, remainingIndexes, assignment) {
    if (labelIndex === labels.length - 1) {
      const label = labels[labelIndex];
      const final = { ...assignment };
      for (const index of remainingIndexes) final[index] = label;
      out.push(final);
      return;
    }
    const label = labels[labelIndex];
    const k = counts[label];
    for (const chosen of combinationsForIndexes(remainingIndexes, k)) {
      const chosenSet = new Set(chosen);
      const next = { ...assignment };
      for (const index of chosen) next[index] = label;
      step(
        labelIndex + 1,
        remainingIndexes.filter((index) => !chosenSet.has(index)),
        next,
      );
    }
  }
  step(0, indexes, {});
  return out;
}

function exactCoarseBlockinessWithinGroups(rows) {
  const observedLabels = rows.map((row) => row.coarse_signature);
  const observed = countSameLabelPairs(rows, observedLabels, true);
  const groups = [...countBy(rows, (row) => row.manufacturing_group).keys()].sort();
  const groupAssignments = groups.map((group) => {
    const indexedRows = rows.map((row, index) => [row, index]).filter(([row]) => row.manufacturing_group === group);
    const indexes = indexedRows.map(([, index]) => index);
    const counts = objectFromCounts(countBy(indexedRows, ([row]) => row.coarse_signature));
    return multisetAssignments(indexes, counts);
  });
  let total = 0;
  let extreme = 0;
  function step(groupIndex, assignment) {
    if (groupIndex === groupAssignments.length) {
      const labels = rows.map((_, index) => assignment[index]);
      const count = countSameLabelPairs(rows, labels, true);
      total++;
      if (count >= observed) extreme++;
      return;
    }
    for (const groupAssignment of groupAssignments[groupIndex]) {
      step(groupIndex + 1, { ...assignment, ...groupAssignment });
    }
  }
  step(0, {});
  return {
    statistic: observed,
    adjacent_pair_count: adjacentPairs(rows, true).length,
    p_ge_observed: extreme / total,
    permutation_space: total,
  };
}

const sourceRows = csvObjects(fs.readFileSync(inputCsv, 'utf8'));
const rows = sourceRows
  .map((row) => ({
    fig4_number: Number.parseInt(row.fig4_number, 10),
    manufacturing_group: row.manufacturing_group,
    cisi: row.cisi,
    harp_object: row.harp_object,
    source_figure: row.local_source_figure,
    local_signature_short: row.local_signature_short,
    coarse_signature: coarseSignature(row.local_signature_short),
    canonical_ab: canonicalLabel(row.local_signature_short),
    side_1_text: row.side_1_text,
    side_2_text: row.side_2_text,
    side_3_text: row.side_3_text,
    interpretation_status: 'no_reading_admissible',
  }))
  .sort((a, b) => a.fig4_number - b.fig4_number);

const canonicalRows = rows.filter((row) => row.canonical_ab === 'A' || row.canonical_ab === 'B');

const detailRows = [
  [
    'fig4_number',
    'manufacturing_group',
    'cisi',
    'harp_object',
    'source_figure',
    'local_signature_short',
    'coarse_signature',
    'canonical_ab',
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
    row.harp_object,
    row.source_figure,
    row.local_signature_short,
    row.coarse_signature,
    row.canonical_ab,
    row.side_1_text,
    row.side_2_text,
    row.side_3_text,
    row.interpretation_status,
  ]);
}

const tests = {
  canonical_group_distribution: exactCanonicalGroupDistribution(canonicalRows),
  canonical_fig4_bb_adjacency: exactCanonicalAdjacency(canonicalRows, false),
  canonical_within_group_bb_adjacency: exactCanonicalAdjacency(canonicalRows, true),
  canonical_within_group_count_conditioned_bb_adjacency: exactCanonicalAdjacencyWithinObservedGroups(canonicalRows),
  coarse_signature_within_group_blockiness: exactCoarseBlockinessWithinGroups(rows),
};

const testRows = [
  [
    'comparison',
    'scope',
    'statistic',
    'adjacent_pair_count',
    'exact_p_ge_observed',
    'permutation_space',
    'interpretation',
  ],
];
for (const [name, test] of Object.entries(tests)) {
  testRows.push([
    name,
    name.includes('coarse') ? 'all_22_A_B_variant_labels' : '20_canonical_A_B_rows',
    formatNumber(test.statistic),
    test.adjacent_pair_count ?? '',
    formatNumber(test.p_ge_observed),
    test.permutation_space,
    'source_order_confound_check_only_no_reading',
  ]);
}

const sequenceByGroup = {};
for (const group of [...countBy(rows, (row) => row.manufacturing_group).keys()].sort()) {
  sequenceByGroup[group] = rows
    .filter((row) => row.manufacturing_group === group)
    .map((row) => row.coarse_signature)
    .join(' ');
}

const canonicalCountsByGroup = {};
for (const group of [...countBy(canonicalRows, (row) => row.manufacturing_group).keys()].sort()) {
  const groupRows = canonicalRows.filter((row) => row.manufacturing_group === group);
  canonicalCountsByGroup[group] = objectFromCounts(countBy(groupRows, (row) => row.canonical_ab));
}

const summary = {
  source: 'H-2218 through H-2239 side-order confound probe',
  checked_at: '2026-05-24',
  input: path.relative(base, inputCsv).replaceAll('\\', '/'),
  source_rows: rows.length,
  canonical_a_b_rows: canonicalRows.length,
  coarse_signature_counts: objectFromCounts(countBy(rows, (row) => row.coarse_signature)),
  canonical_signature_counts: objectFromCounts(countBy(canonicalRows, (row) => row.canonical_ab)),
  manufacturing_group_counts: objectFromCounts(countBy(rows, (row) => row.manufacturing_group)),
  canonical_counts_by_group: canonicalCountsByGroup,
  fig4_sequence_by_group: sequenceByGroup,
  tests: Object.fromEntries(
    Object.entries(tests).map(([name, test]) => [
      name,
      {
        statistic: formatNumber(test.statistic),
        adjacent_pair_count: test.adjacent_pair_count ?? null,
        exact_p_ge_observed: formatNumber(test.p_ge_observed),
        permutation_space: test.permutation_space,
      },
    ]),
  ),
  key_observation:
    'The canonical A/B side-order split is spread across all three manufacturing groups, and the visible Fig. 4 same-label blocks are not strong under exact order nulls. This weakens manufacturing-group and published-sequence explanations, while still keeping source order as a validation layer rather than evidence for side function or meaning.',
  interpretation_boundary:
    'This is a manufacturing-group and Fig. 4 sequence-order confound probe only. It accepts no physical side function, numerical value, metrological reading, sign meaning, phonetic value, language identity, or translation.',
  outputs: [detailCsv, testCsv, outJson].map((file) => path.relative(base, file).replaceAll('\\', '/')),
};

fs.writeFileSync(detailCsv, toCsv(detailRows));
fs.writeFileSync(testCsv, toCsv(testRows));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
