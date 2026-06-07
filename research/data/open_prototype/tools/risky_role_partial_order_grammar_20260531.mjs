import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_role_partial_order_grammar_20260531';
const RUN_DATE = '2026-05-31';
const ITERATIONS = 3000;

const CONSTRAINTS = [
  { id: '400_before_740', left: '400', right: '740', source: 'tablet-account frame before broad opener' },
  { id: '400_before_002', left: '400', right: '002', source: 'tablet-account frame before preterminal bridge' },
  { id: '740_before_002', left: '740', right: '002', source: 'broad opener before preterminal bridge' },
  { id: '740_before_861', left: '740', right: '861', source: 'broad opener before terminal partner' },
  { id: '740_before_820', left: '740', right: '820', source: 'broad opener before terminal partner' },
  { id: '740_before_817', left: '740', right: '817', source: 'broad opener before terminal partner' },
  { id: '002_before_861', left: '002', right: '861', source: 'preterminal bridge before terminal partner' },
  { id: '002_before_820', left: '002', right: '820', source: 'preterminal bridge before terminal partner' },
  { id: '002_before_817', left: '002', right: '817', source: 'preterminal bridge before terminal partner' },
  { id: '407_before_806', left: '407', right: '806', source: 'rectangular/copper entry before closure pivot' },
  { id: '806_before_002', left: '806', right: '002', source: 'closure pivot before preterminal bridge when both occur' },
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

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
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

function before(row, left, right) {
  const li = row.signs.indexOf(left);
  const ri = row.signs.indexOf(right);
  if (li < 0 || ri < 0) return null;
  return li < ri;
}

function analyzeConstraints(rows) {
  const constraintRows = CONSTRAINTS.map((constraint) => {
    const local = rows.filter((row) => row.signSet.has(constraint.left) && row.signSet.has(constraint.right));
    const satisfied = local.filter((row) => before(row, constraint.left, constraint.right)).length;
    const total = local.length;
    const p = total ? binomialRightTail(Math.max(satisfied, total - satisfied), total) : 1;
    return {
      ...constraint,
      total,
      satisfied,
      violated: total - satisfied,
      satisfied_share: total ? satisfied / total : 0,
      binomial_p: p,
      passed_direction: total >= 10 && satisfied / total >= 0.8 && p <= 0.01,
    };
  });
  const usable = constraintRows.filter((row) => row.total >= 10);
  const passed = usable.filter((row) => row.passed_direction);
  const evidenceRows = usable.reduce((sum, row) => sum + row.total, 0);
  const satisfiedRows = usable.reduce((sum, row) => sum + row.satisfied, 0);
  return {
    constraintRows,
    usable_constraints: usable.length,
    passed_constraints: passed.length,
    evidenceRows,
    satisfiedRows,
    satisfiedShare: evidenceRows ? satisfiedRows / evidenceRows : 0,
  };
}

function forger(rows, observedPassed, observedSatisfiedShare, iterations = ITERATIONS) {
  const rand = mulberry32(0x500400 ^ rows.length);
  let passedGe = 0;
  let shareGe = 0;
  const iterationRows = [];
  for (let iter = 0; iter < iterations; iter += 1) {
    const fakeRows = rows.map((row) => {
      const signs = row.signs.slice();
      shuffleInPlace(signs, rand);
      return { ...row, signs, signSet: new Set(signs) };
    });
    const stats = analyzeConstraints(fakeRows);
    if (stats.passed_constraints >= observedPassed) passedGe += 1;
    if (stats.satisfiedShare >= observedSatisfiedShare) shareGe += 1;
    if (iter < 50 || stats.passed_constraints >= observedPassed || stats.satisfiedShare >= observedSatisfiedShare) {
      iterationRows.push({
        iteration: iter,
        passed_constraints: stats.passed_constraints,
        satisfied_share: stats.satisfiedShare,
        passed_ge_observed: String(stats.passed_constraints >= observedPassed),
        share_ge_observed: String(stats.satisfiedShare >= observedSatisfiedShare),
      });
    }
  }
  return { iterations, passed_constraints_fpr: passedGe / iterations, satisfied_share_fpr: shareGe / iterations, iteration_rows: iterationRows };
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()]
  .filter((row) => row.signs.length > 1)
  .map((row) => ({ ...row, signSet: new Set(row.signs) }));

const main = analyzeConstraints(canonicalRows);
const nulls = forger(canonicalRows, main.passed_constraints, main.satisfiedShare);
const failedConstraints = main.constraintRows.filter((row) => row.total >= 10 && !row.passed_direction);
const supportRows = canonicalRows.filter((row) => CONSTRAINTS.some((constraint) => row.signSet.has(constraint.left) && row.signSet.has(constraint.right))).map((row) => {
  const statuses = CONSTRAINTS
    .filter((constraint) => row.signSet.has(constraint.left) && row.signSet.has(constraint.right))
    .map((constraint) => `${constraint.id}:${before(row, constraint.left, constraint.right) ? 'pass' : 'fail'}`)
    .join(';');
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
    constraint_statuses: statuses,
    text: row.text,
  };
});

const tier =
  main.passed_constraints >= 8 &&
  main.satisfiedShare >= 0.9 &&
  nulls.passed_constraints_fpr <= 0.01 &&
  nulls.satisfied_share_fpr <= 0.01
    ? 'promoted candidate'
    : 'candidate';

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V2_V4_ROLE_PARTIAL_ORDER_GRAMMAR_20260531',
  vector: 'V2 slot grammar; V4 context-to-meaning without sound',
  confidence_tier: tier,
  risky_bet:
    'A small role grammar is emerging: frame/opening signs precede bridge signs, bridge signs precede terminal partners, and register-specific closure pivots sit before final bridges or ends. This should survive as a partial order over named signs, not just isolated pair facts.',
  observed:
    `Usable constraints=${main.usable_constraints}; passed=${main.passed_constraints}; satisfied rows=${main.satisfiedRows}/${main.evidenceRows} (${main.satisfiedShare}). ` +
    `Row-internal shuffle FPRs: passed-constraints=${nulls.passed_constraints_fpr}, satisfied-share=${nulls.satisfied_share_fpr}. Failed usable constraints: ${failedConstraints.map((row) => `${row.id}:${row.satisfied}/${row.total}`).join(';') || 'none'}.`,
  adversarial_test:
    `Named constraints from prior promoted/candidate results, tested together against ${ITERATIONS}-iteration row-internal sign shuffles that preserve each row's sign multiset and all row-level co-occurrences. A constraint must have >=10 co-occurrence rows, >=0.8 satisfaction share, and binomial p<=0.01 to pass.`,
  false_positive_rate: Math.max(nulls.passed_constraints_fpr, nulls.satisfied_share_fpr),
  passed_constraints_fpr: nulls.passed_constraints_fpr,
  satisfied_share_fpr: nulls.satisfied_share_fpr,
  falsifier:
    'If source-checked or expanded rows break more than a small minority of these pair orders, especially 400->740, 740->002, 002->terminal, or 407->806, demote the finite role grammar back to isolated pairwise tendencies.',
  next_prediction:
    'Held-out rows containing multiple named role signs should usually respect the partial order: 400 before 740, openers before 002, 002 before 861/820/817, and 407 before 806. This is structural parsing only, not translation.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({ ...summary, constraints: main.constraintRows, support_rows: supportRows }, null, 2),
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
  'passed_constraints_fpr',
  'satisfied_share_fpr',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_constraints.csv`), main.constraintRows, [
  'id',
  'left',
  'right',
  'source',
  'total',
  'satisfied',
  'violated',
  'satisfied_share',
  'binomial_p',
  'passed_direction',
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
  'constraint_statuses',
  'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_forger_iterations.csv`), nulls.iteration_rows, [
  'iteration',
  'passed_constraints',
  'satisfied_share',
  'passed_ge_observed',
  'share_ge_observed',
]);

console.log(JSON.stringify(summary, null, 2));
