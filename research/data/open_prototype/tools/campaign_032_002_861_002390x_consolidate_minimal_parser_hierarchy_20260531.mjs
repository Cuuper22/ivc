// Pits the minimal parser against register-based null models as backoff
// hierarchies. A hierarchy is an ordered chain of predictors: try the most
// specific key first (say, the exact head-X pair), and if too few training
// rows match, back off to the next key (X alone, then the visual scope cell).
// This script builds every 002-H-X frame from the local Lipi metadata, then
// scores four hierarchies — grammar-first, scope-first, X-then-scope, and
// scope-only — by leave-one-out majority vote on four collapse levels of the
// data (raw down to one row per head-X pair). It records per-step usage counts
// and up to 20 mistakes per combination. Writes metrics, mistakes-sample, and
// decisions CSVs plus a summary JSON to data/open_prototype/reports/.
// Recorded verdict: the grammar hierarchy is real enough to guide bets but its
// edge over scope-first nulls is small and collapse-sensitive, so the minimal
// parser stays a candidate and every future claim must beat the scope null.

import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const prefix = 'campaign_032_002_861_002390x_consolidate_minimal_parser_hierarchy_20260531';

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (ch === '"' && next === '"') {
        field += '"';
        i += 1;
      } else if (ch === '"') {
        quoted = false;
      } else {
        field += ch;
      }
    } else if (ch === '"') {
      quoted = true;
    } else if (ch === ',') {
      row.push(field);
      field = '';
    } else if (ch === '\n') {
      row.push(field.replace(/\r$/, ''));
      rows.push(row);
      row = [];
      field = '';
    } else {
      field += ch;
    }
  }
  if (field.length || row.length) {
    row.push(field.replace(/\r$/, ''));
    rows.push(row);
  }
  const header = rows.shift() ?? [];
  return rows
    .filter((r) => r.some((value) => value !== ''))
    .map((r) => Object.fromEntries(header.map((name, index) => [name, r[index] ?? ''])));
}

function csvEscape(value) {
  const text = String(value ?? '');
  return /[",\n\r]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(',')];
  for (const row of rows) lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function signs(text) {
  return text.match(/\d{3}/g) ?? [];
}

function pct(numerator, denominator) {
  return denominator ? (numerator / denominator).toFixed(6) : '';
}

function majority(rows) {
  const open = rows.filter((row) => row.open).length;
  return {
    predicted_open: open >= rows.length - open,
    training_open_rate: pct(open, rows.length),
    training_rows: rows.length,
  };
}

function collapseRows(rows, keyFn) {
  const seen = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    if (!seen.has(key)) seen.set(key, row);
  }
  return [...seen.values()];
}

function predict(train, test, chain) {
  for (const step of chain) {
    const key = step.key(test);
    const rows = train.filter((row) => step.key(row) === key);
    if (rows.length >= step.min) return { ...majority(rows), step: step.name, key };
  }
  return { ...majority(train), step: 'global', key: '*' };
}

function evaluate(setName, rows, hierarchyName, chain) {
  let correct = 0;
  const mistakes = [];
  const stepCounts = new Map();
  for (let index = 0; index < rows.length; index += 1) {
    const test = rows[index];
    const train = rows.filter((_, rowIndex) => rowIndex !== index);
    const prediction = predict(train, test, chain);
    const actual = test.open ? 'open' : 'terminal';
    const predicted = prediction.predicted_open ? 'open' : 'terminal';
    stepCounts.set(prediction.step, (stepCounts.get(prediction.step) ?? 0) + 1);
    if (predicted === actual) {
      correct += 1;
    } else {
      mistakes.push({
        checked_date: '2026-05-31',
        set_name: setName,
        hierarchy: hierarchyName,
        object: test.object,
        id: test.id,
        pair: test.pair,
        x: test.x,
        scope_cell: test.scope_cell,
        tail_after_x: test.tail_after_x,
        step: prediction.step,
        key: prediction.key,
        training_rows: String(prediction.training_rows),
        training_open_rate: prediction.training_open_rate,
        predicted,
        actual,
        text: test.text,
      });
    }
  }
  return {
    metric: {
      checked_date: '2026-05-31',
      set_name: setName,
      hierarchy: hierarchyName,
      rows: String(rows.length),
      correct: String(correct),
      wrong: String(rows.length - correct),
      accuracy: pct(correct, rows.length),
      step_counts: [...stepCounts.entries()].map(([key, value]) => `${key}:${value}`).join(';'),
    },
    mistakes,
  };
}

fs.mkdirSync(reportsDir, { recursive: true });

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));
const frames = [];
for (const row of metadataRows) {
  const rowSigns = signs(row.text);
  for (let index = 0; index < rowSigns.length - 2; index += 1) {
    if (rowSigns[index] !== '002') continue;
    const head = rowSigns[index + 1];
    const x = rowSigns[index + 2];
    frames.push({
      checked_date: '2026-05-31',
      object: row.cisi,
      id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      scope_cell: `${row.site}|${row.type}|${row.shape}|${row.material}`,
      prev_before_002: rowSigns[index - 1] ?? '',
      head,
      x,
      pair: `${head}-${x}`,
      scope_x: `${row.site}|${row.type}|${row.shape}|${row.material}|${x}`,
      scope_pair: `${row.site}|${row.type}|${row.shape}|${row.material}|${head}-${x}`,
      tail_after_x: rowSigns.slice(index + 3).join(' ') || '<END>',
      open: index + 2 < rowSigns.length - 1,
      text: row.text,
    });
  }
}

const sets = [
  ['raw', frames],
  ['collapse_scope_pair_tail', collapseRows(frames, (row) => `${row.scope_cell}|${row.pair}|${row.tail_after_x}`)],
  ['collapse_pair_tail', collapseRows(frames, (row) => `${row.pair}|${row.tail_after_x}`)],
  ['collapse_pair', collapseRows(frames, (row) => row.pair)],
];

const hierarchies = [
  [
    'grammar_pair_x_scope',
    [
      { name: 'pair', min: 2, key: (row) => row.pair },
      { name: 'x', min: 3, key: (row) => row.x },
      { name: 'scope', min: 3, key: (row) => row.scope_cell },
    ],
  ],
  [
    'scope_first_null',
    [
      { name: 'scope_x', min: 2, key: (row) => row.scope_x },
      { name: 'scope_pair', min: 2, key: (row) => row.scope_pair },
      { name: 'scope', min: 3, key: (row) => row.scope_cell },
      { name: 'x', min: 3, key: (row) => row.x },
    ],
  ],
  [
    'x_then_scope',
    [
      { name: 'x', min: 3, key: (row) => row.x },
      { name: 'scope', min: 3, key: (row) => row.scope_cell },
    ],
  ],
  ['scope_only_null', [{ name: 'scope', min: 3, key: (row) => row.scope_cell }]],
];

const metrics = [];
const mistakeRows = [];
for (const [setName, rows] of sets) {
  for (const [hierarchyName, chain] of hierarchies) {
    const result = evaluate(setName, rows, hierarchyName, chain);
    metrics.push(result.metric);
    mistakeRows.push(...result.mistakes.slice(0, 20));
  }
}

function metric(setName, hierarchy) {
  return metrics.find((row) => row.set_name === setName && row.hierarchy === hierarchy);
}

const decisions = [
  {
    checked_date: '2026-05-31',
    decision: 'minimal_parser_not_promoted',
    tier_change: 'candidate_not_promoted',
    evidence:
      `raw grammar=${metric('raw', 'grammar_pair_x_scope').accuracy}; raw scope_null=${metric('raw', 'scope_first_null').accuracy}; ` +
      `pair-collapse grammar=${metric('collapse_pair', 'grammar_pair_x_scope').accuracy}; pair-collapse scope_null=${metric('collapse_pair', 'scope_first_null').accuracy}`,
    consequence:
      'The hierarchy is useful but too close to scope nulls under collapse; keep it as candidate only.',
  },
  {
    checked_date: '2026-05-31',
    decision: 'h_x_pair_rule_requires_repeat_and_scope_audit',
    tier_change: 'narrowed_candidate',
    evidence:
      `scope-pair-tail grammar=${metric('collapse_scope_pair_tail', 'grammar_pair_x_scope').accuracy}; pair-tail grammar=${metric('collapse_pair_tail', 'grammar_pair_x_scope').accuracy}`,
    consequence:
      'Any H-X rule must report whether it survives outside exact scope/tail families.',
  },
  {
    checked_date: '2026-05-31',
    decision: 'scope_null_remains_destructive_test',
    tier_change: 'adversary_strengthened',
    evidence:
      `scope-first null raw=${metric('raw', 'scope_first_null').accuracy}; pair-collapse scope-first=${metric('collapse_pair', 'scope_first_null').accuracy}`,
    consequence:
      'Future parser claims must beat a scope-first null on the same held-out/collapse split.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'CONSOLIDATE',
  status: 'minimal_parser_hierarchy',
  metrics,
  decisions,
  compressed_read:
    'The minimal parser is real enough to guide bets, but not strong enough to promote: its edge over scope nulls is small and collapse-sensitive.',
};

writeCsv(path.join(reportsDir, `${prefix}_metrics.csv`), metrics, [
  'checked_date',
  'set_name',
  'hierarchy',
  'rows',
  'correct',
  'wrong',
  'accuracy',
  'step_counts',
]);

writeCsv(path.join(reportsDir, `${prefix}_mistakes_sample.csv`), mistakeRows, [
  'checked_date',
  'set_name',
  'hierarchy',
  'object',
  'id',
  'pair',
  'x',
  'scope_cell',
  'tail_after_x',
  'step',
  'key',
  'training_rows',
  'training_open_rate',
  'predicted',
  'actual',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  'checked_date',
  'decision',
  'tier_change',
  'evidence',
  'consequence',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
