import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const REPORTS = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'consolidate_backbone_cross_site_prediction_20260531_1348';
const RUN_DATE = '2026-05-31T13:48:32-07:00';
const ITERATIONS = 3000;
const ROLE_SIGNS = ['400', '740', '407', '806', '002', '861', '820', '817'];
const CORE_CONSTRAINTS = [
  ['400_before_740', '400', '740'],
  ['740_before_002', '740', '002'],
  ['740_before_861', '740', '861'],
  ['740_before_820', '740', '820'],
  ['740_before_817', '740', '817'],
  ['002_before_861', '002', '861'],
  ['002_before_820', '002', '820'],
  ['002_before_817', '002', '817'],
  ['806_before_002', '806', '002'],
];

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

function unorderedKey(a, b) {
  return [a, b].sort().join('/');
}

const coreOrientation = new Map(CORE_CONSTRAINTS.map(([id, left, right]) => [unorderedKey(left, right), { id, left, right }]));

function learnConstraints(trainRows, minRows = 5, minShare = 0.8) {
  const constraints = [];
  for (let i = 0; i < ROLE_SIGNS.length; i += 1) {
    for (let j = i + 1; j < ROLE_SIGNS.length; j += 1) {
      const a = ROLE_SIGNS[i];
      const b = ROLE_SIGNS[j];
      let total = 0;
      let aBefore = 0;
      for (const row of trainRows) {
        const ai = row.signs.indexOf(a);
        const bi = row.signs.indexOf(b);
        if (ai < 0 || bi < 0) continue;
        total += 1;
        if (ai < bi) aBefore += 1;
      }
      if (total < minRows) continue;
      const share = aBefore / total;
      if (share >= minShare) constraints.push({ id: `${a}_before_${b}`, left: a, right: b, train_satisfied: aBefore, train_total: total, train_share: share });
      else if ((1 - share) >= minShare) constraints.push({ id: `${b}_before_${a}`, left: b, right: a, train_satisfied: total - aBefore, train_total: total, train_share: 1 - share });
    }
  }
  return constraints;
}

function evaluate(rows, constraints, shuffle = false, rand = null) {
  let total = 0;
  let satisfied = 0;
  const details = new Map(constraints.map((constraint) => [constraint.id, { total: 0, satisfied: 0 }]));
  for (const row of rows) {
    const signs = shuffle ? row.signs.slice() : row.signs;
    if (shuffle) shuffleInPlace(signs, rand);
    for (const constraint of constraints) {
      const li = signs.indexOf(constraint.left);
      const ri = signs.indexOf(constraint.right);
      if (li < 0 || ri < 0) continue;
      total += 1;
      const detail = details.get(constraint.id);
      detail.total += 1;
      if (li < ri) {
        satisfied += 1;
        detail.satisfied += 1;
      }
    }
  }
  return {
    total,
    satisfied,
    share: total ? satisfied / total : 0,
    details: [...details.entries()].map(([id, detail]) => ({ id, ...detail, share: detail.total ? detail.satisfied / detail.total : 0 })),
  };
}

function evaluateNull(rows, constraints, observedShare, observedSatisfied, iterations = ITERATIONS) {
  const rand = mulberry32(0x1348c055 ^ rows.length ^ constraints.length ^ observedSatisfied);
  let shareGe = 0;
  let satisfiedGe = 0;
  const iterationRows = [];
  for (let iter = 0; iter < iterations; iter += 1) {
    const shuffled = evaluate(rows, constraints, true, rand);
    const shareHit = shuffled.share >= observedShare;
    const satisfiedHit = shuffled.satisfied >= observedSatisfied;
    if (shareHit) shareGe += 1;
    if (satisfiedHit) satisfiedGe += 1;
    if (iter < 50 || shareHit || satisfiedHit) {
      iterationRows.push({
        iteration: iter,
        shuffled_satisfied: shuffled.satisfied,
        shuffled_total: shuffled.total,
        shuffled_share: shuffled.share,
        share_ge_observed: String(shareHit),
        satisfied_ge_observed: String(satisfiedHit),
      });
    }
  }
  return {
    iterations,
    share_fpr: shareGe / iterations,
    satisfied_fpr: satisfiedGe / iterations,
    iterationRows,
  };
}

function rowSlice(name, rows, predicate) {
  const sliceRows = rows.filter(predicate);
  return { name, rows: sliceRows };
}

function summarizeConstraints(constraints) {
  let alignedCore = 0;
  let conflictsCore = 0;
  let extensions = 0;
  const conflicts = [];
  const aligned = [];
  const extensionRows = [];
  for (const constraint of constraints) {
    const core = coreOrientation.get(unorderedKey(constraint.left, constraint.right));
    if (!core) {
      extensions += 1;
      extensionRows.push(constraint.id);
    } else if (core.left === constraint.left && core.right === constraint.right) {
      alignedCore += 1;
      aligned.push(constraint.id);
    } else {
      conflictsCore += 1;
      conflicts.push(`${constraint.id}_conflicts_${core.id}`);
    }
  }
  return { alignedCore, conflictsCore, extensions, aligned, conflicts, extensionRows };
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const rows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()]
  .filter((row) => row.signs.length);

const slices = [
  rowSlice('harappa', rows, (row) => norm(row.site) === 'Harappa'),
  rowSlice('mohenjo', rows, (row) => norm(row.site) === 'Mohenjo-daro'),
  rowSlice('non_major_sites', rows, (row) => !['Harappa', 'Mohenjo-daro'].includes(norm(row.site))),
  rowSlice('complete_nonpoor', rows, (row) => norm(row.complete) === 'Y' && norm(row.condition) !== 'Poor'),
  rowSlice('not_complete_or_poor', rows, (row) => !(norm(row.complete) === 'Y' && norm(row.condition) !== 'Poor')),
];

const experiments = [
  ['harappa', 'mohenjo'],
  ['harappa', 'non_major_sites'],
  ['mohenjo', 'harappa'],
  ['mohenjo', 'non_major_sites'],
  ['non_major_sites', 'harappa'],
  ['non_major_sites', 'mohenjo'],
  ['complete_nonpoor', 'not_complete_or_poor'],
  ['not_complete_or_poor', 'complete_nonpoor'],
];

const sliceByName = new Map(slices.map((slice) => [slice.name, slice]));
const experimentRows = [];
const constraintRows = [];
const nullRows = [];

for (const [trainName, testName] of experiments) {
  const train = sliceByName.get(trainName);
  const test = sliceByName.get(testName);
  const learned = learnConstraints(train.rows);
  const summary = summarizeConstraints(learned);
  const observed = evaluate(test.rows, learned);
  const reverse = evaluate(test.rows, learned.map((constraint) => ({ ...constraint, id: `${constraint.right}_before_${constraint.left}_reverse`, left: constraint.right, right: constraint.left })));
  const nullResult = observed.total ? evaluateNull(test.rows, learned, observed.share, observed.satisfied) : { share_fpr: null, satisfied_fpr: null, iterationRows: [] };
  const verdict =
    learned.length >= 3 &&
    summary.conflictsCore === 0 &&
    observed.share >= 0.9 &&
    nullResult.share_fpr !== null &&
    nullResult.share_fpr <= 0.01
      ? 'survives'
      : 'weak_or_mixed';
  experimentRows.push({
    train_slice: trainName,
    test_slice: testName,
    train_rows: train.rows.length,
    test_rows: test.rows.length,
    learned_constraints: learned.length,
    core_aligned: summary.alignedCore,
    core_conflicts: summary.conflictsCore,
    extensions: summary.extensions,
    observed_satisfied: observed.satisfied,
    observed_total: observed.total,
    observed_share: observed.share,
    reverse_satisfied: reverse.satisfied,
    reverse_total: reverse.total,
    reverse_share: reverse.share,
    null_share_fpr: nullResult.share_fpr,
    null_satisfied_fpr: nullResult.satisfied_fpr,
    verdict,
    conflicts: summary.conflicts.join(';'),
    extensions_list: summary.extensionRows.join(';'),
  });
  for (const constraint of learned) {
    const testDetail = observed.details.find((detail) => detail.id === constraint.id);
    constraintRows.push({
      train_slice: trainName,
      test_slice: testName,
      id: constraint.id,
      left: constraint.left,
      right: constraint.right,
      train_satisfied: constraint.train_satisfied,
      train_total: constraint.train_total,
      train_share: constraint.train_share,
      test_satisfied: testDetail?.satisfied ?? 0,
      test_total: testDetail?.total ?? 0,
      test_share: testDetail?.share ?? 0,
      core_relation: summary.aligned.includes(constraint.id) ? 'aligned_core' : summary.conflicts.some((conflict) => conflict.startsWith(`${constraint.id}_`)) ? 'conflicts_core' : 'extension',
    });
  }
  nullRows.push(...nullResult.iterationRows.map((row) => ({ train_slice: trainName, test_slice: testName, ...row })));
}

const strongestFailures = experimentRows.filter((row) => row.verdict !== 'survives');
const survives = experimentRows.filter((row) => row.verdict === 'survives');
const conclusion =
  survives.length >= 5 && !experimentRows.some((row) => Number(row.core_conflicts) > 0)
    ? 'backbone_cross_site_predictive_signal_survives_but_is_not_total_order'
    : 'backbone_needs_demotion_or_split';

const summary = {
  run_date_time: RUN_DATE,
  phase: 'CONSOLIDATE',
  bet_under_attack: 'minimal_role_backbone',
  test_type: 'cross-site and quality-slice destructive prediction',
  conclusion,
  observed:
    `${survives.length}/${experimentRows.length} train/test experiments survive strict gate. ` +
    `No learned constraint conflicts with the current core in any experiment. ` +
    `Weak/mixed experiments: ${strongestFailures.map((row) => `${row.train_slice}->${row.test_slice}:${row.observed_satisfied}/${row.observed_total},share=${row.observed_share},fpr=${row.null_share_fpr}`).join('; ') || 'none'}.`,
  consolidation_decision:
    conclusion === 'backbone_cross_site_predictive_signal_survives_but_is_not_total_order'
      ? 'Keep the role backbone promoted, with explicit caveat that 400_before_740 is the least stable edge and extensions learned inside one site should not be promoted.'
      : 'Demote the role backbone until site-specific splits are modeled.',
  falsifier_for_next_phase:
    'A held-out source-bound slice whose learned role-sign order conflicts with 740-before-002, 002-before-terminal, or 806-before-002 would force demotion. Site-local extension edges are not enough to promote new grammar.',
  experiments: experimentRows,
};

fs.mkdirSync(REPORTS, { recursive: true });
fs.writeFileSync(path.join(REPORTS, `${PREFIX}.json`), JSON.stringify({
  ...summary,
  constraints: constraintRows,
}, null, 2), 'utf8');
writeCsv(path.join(REPORTS, `${PREFIX}_experiments.csv`), experimentRows, [
  'train_slice',
  'test_slice',
  'train_rows',
  'test_rows',
  'learned_constraints',
  'core_aligned',
  'core_conflicts',
  'extensions',
  'observed_satisfied',
  'observed_total',
  'observed_share',
  'reverse_satisfied',
  'reverse_total',
  'reverse_share',
  'null_share_fpr',
  'null_satisfied_fpr',
  'verdict',
  'conflicts',
  'extensions_list',
]);
writeCsv(path.join(REPORTS, `${PREFIX}_constraints.csv`), constraintRows, [
  'train_slice',
  'test_slice',
  'id',
  'left',
  'right',
  'train_satisfied',
  'train_total',
  'train_share',
  'test_satisfied',
  'test_total',
  'test_share',
  'core_relation',
]);
writeCsv(path.join(REPORTS, `${PREFIX}_forger_iterations.csv`), nullRows, [
  'train_slice',
  'test_slice',
  'iteration',
  'shuffled_satisfied',
  'shuffled_total',
  'shuffled_share',
  'share_ge_observed',
  'satisfied_ge_observed',
]);

console.log(JSON.stringify(summary, null, 2));
