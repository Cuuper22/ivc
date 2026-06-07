import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const REPORTS = path.join(ROOT, 'data', 'open_prototype', 'reports');
const INPUT = path.join(REPORTS, 'campaign_032_002_post_y_all_002_rows.csv');
const OUT_SUMMARY = path.join(REPORTS, 'campaign_032_002_y_posthoc_partition_forger_summary.json');
const OUT_ITERATIONS = path.join(REPORTS, 'campaign_032_002_y_posthoc_partition_forger_iterations.csv');
const OUT_OBSERVED = path.join(REPORTS, 'campaign_032_002_y_posthoc_partition_forger_observed.csv');

const RUN_DATE = '2026-05-29';
const ITERATIONS = Number.parseInt(process.argv[2] ?? '10000', 10);
const SEED = Number.parseInt(process.argv[3] ?? '20260529', 10);

const SCOPE_CONFIGS = [
  {
    name: 'all_002_strict_dedup',
    filter: () => true,
    min_y_rows: 8,
    min_closure_rows: 50,
    min_branch_rows: 20,
    min_closure_signs: 2,
    min_branch_signs: 2,
  },
  {
    name: 'after_032_strict_dedup',
    filter: (row) => row.prev1_before_002 === '032',
    min_y_rows: 2,
    min_closure_rows: 8,
    min_branch_rows: 3,
    min_closure_signs: 2,
    min_branch_signs: 2,
  },
];

const ITERATION_FIELDS = [
  'scope',
  'null_model',
  'iteration',
  'rows',
  'eligible_signs',
  'best_z',
  'best_gap',
  'best_closure_rate',
  'best_branch_rate',
  'best_closure_rows',
  'best_branch_rows',
  'best_closure_signs',
  'best_branch_signs',
  'best_high_threshold',
  'best_low_threshold',
];

const OBSERVED_FIELDS = [
  ...ITERATION_FIELDS.filter((field) => !['null_model', 'iteration'].includes(field)),
  'closure_sign_list',
  'branch_sign_list',
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
      rows.push(row);
      row = [];
      cell = '';
    } else {
      cell += ch;
    }
  }
  if (cell.length || row.length) {
    row.push(cell.replace(/\r$/, ''));
    rows.push(row);
  }
  if (!rows.length) return [];
  const header = rows[0];
  return rows.slice(1).filter((r) => r.some((v) => v !== '')).map((r) => {
    const out = {};
    header.forEach((h, i) => {
      out[h] = r[i] ?? '';
    });
    return out;
  });
}

function csvEscape(value) {
  const text = String(value ?? '');
  if (/[",\n\r]/.test(text)) return `"${text.replaceAll('"', '""')}"`;
  return text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(',')];
  for (const row of rows) lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function mulberry32(seed) {
  let a = seed >>> 0;
  return () => {
    a += 0x6d2b79f5;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffle(values, rng) {
  const out = values.slice();
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rng() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function groupBy(rows, keyFn) {
  const groups = new Map();
  rows.forEach((row, index) => {
    const key = keyFn(row);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push({ row, index });
  });
  return groups;
}

function norm(value) {
  const text = String(value ?? '').trim();
  return text && text !== '-' ? text : 'NA';
}

function loadRows() {
  const seen = new Set();
  const rows = [];
  for (const row of parseCsv(fs.readFileSync(INPUT, 'utf8'))) {
    if (row.strict_complete_closed !== 'true') continue;
    const key = [row.text_dedup_key, row.site, row.type, row.idx_002].join('\u241f');
    if (seen.has(key)) continue;
    seen.add(key);
    rows.push({
      ...row,
      terminal: row.y_terminal === 'true' ? 1 : 0,
      site: norm(row.site),
      type: norm(row.type),
      symbol: norm(row.symbol),
      material: norm(row.material),
      y_after_002: norm(row.y_after_002),
    });
  }
  return rows;
}

function signStats(rows, minYRows) {
  const stats = new Map();
  for (const row of rows) {
    const key = row.y_after_002;
    const current = stats.get(key) ?? { y: key, rows: 0, terminals: 0 };
    current.rows += 1;
    current.terminals += row.terminal;
    stats.set(key, current);
  }
  return [...stats.values()]
    .filter((row) => row.rows >= minYRows)
    .map((row) => ({
      ...row,
      continuing: row.rows - row.terminals,
      terminal_rate: row.terminals / row.rows,
    }))
    .sort((a, b) => b.rows - a.rows || a.y.localeCompare(b.y));
}

function scorePartition(closure, branch, config) {
  const closureRows = closure.reduce((sum, row) => sum + row.rows, 0);
  const branchRows = branch.reduce((sum, row) => sum + row.rows, 0);
  if (
    closure.length < config.min_closure_signs ||
    branch.length < config.min_branch_signs ||
    closureRows < config.min_closure_rows ||
    branchRows < config.min_branch_rows
  ) return null;
  const closureTerminals = closure.reduce((sum, row) => sum + row.terminals, 0);
  const branchTerminals = branch.reduce((sum, row) => sum + row.terminals, 0);
  const closureRate = closureTerminals / closureRows;
  const branchRate = branchTerminals / branchRows;
  const gap = closureRate - branchRate;
  if (gap <= 0) return null;
  const pooled = (closureTerminals + branchTerminals) / (closureRows + branchRows);
  const variance = Math.max(1e-12, pooled * (1 - pooled) * ((1 / closureRows) + (1 / branchRows)));
  const z = gap / Math.sqrt(variance);
  return {
    z,
    gap,
    closure_rate: closureRate,
    branch_rate: branchRate,
    closure_rows: closureRows,
    branch_rows: branchRows,
    closure_signs: closure.length,
    branch_signs: branch.length,
    closure_sign_list: closure.map((row) => `${row.y}:${row.terminals}/${row.rows}`).join(';'),
    branch_sign_list: branch.map((row) => `${row.y}:${row.terminals}/${row.rows}`).join(';'),
  };
}

function bestPosthocPartition(rows, config) {
  const stats = signStats(rows, config.min_y_rows);
  const rates = [...new Set(stats.map((row) => row.terminal_rate))].sort((a, b) => a - b);
  let best = null;
  for (const low of rates) {
    for (const high of rates) {
      if (low > high) continue;
      const branch = stats.filter((row) => row.terminal_rate <= low);
      const closure = stats.filter((row) => row.terminal_rate >= high);
      const score = scorePartition(closure, branch, config);
      if (!score) continue;
      const candidate = {
        rows: rows.length,
        eligible_signs: stats.length,
        best_z: score.z,
        best_gap: score.gap,
        best_closure_rate: score.closure_rate,
        best_branch_rate: score.branch_rate,
        best_closure_rows: score.closure_rows,
        best_branch_rows: score.branch_rows,
        best_closure_signs: score.closure_signs,
        best_branch_signs: score.branch_signs,
        best_high_threshold: high,
        best_low_threshold: low,
        closure_sign_list: score.closure_sign_list,
        branch_sign_list: score.branch_sign_list,
      };
      if (
        !best ||
        candidate.best_z > best.best_z ||
        (candidate.best_z === best.best_z && candidate.best_gap > best.best_gap)
      ) best = candidate;
    }
  }
  return best ?? {
    rows: rows.length,
    eligible_signs: stats.length,
    best_z: 0,
    best_gap: 0,
    best_closure_rate: 0,
    best_branch_rate: 0,
    best_closure_rows: 0,
    best_branch_rows: 0,
    best_closure_signs: 0,
    best_branch_signs: 0,
    best_high_threshold: '',
    best_low_threshold: '',
    closure_sign_list: '',
    branch_sign_list: '',
  };
}

function withGlobalTerminalShuffle(rows, rng) {
  const terminals = shuffle(rows.map((row) => row.terminal), rng);
  return rows.map((row, index) => ({ ...row, terminal: terminals[index] }));
}

function withBlockTerminalShuffle(rows, rng, keyFn) {
  const out = rows.map((row) => ({ ...row }));
  for (const members of groupBy(rows, keyFn).values()) {
    const terminals = shuffle(members.map(({ row }) => row.terminal), rng);
    members.forEach(({ index }, offset) => {
      out[index].terminal = terminals[offset];
    });
  }
  return out;
}

function withGlobalYShuffle(rows, rng) {
  const ys = shuffle(rows.map((row) => row.y_after_002), rng);
  return rows.map((row, index) => ({ ...row, y_after_002: ys[index] }));
}

function withBlockYShuffle(rows, rng, keyFn) {
  const out = rows.map((row) => ({ ...row }));
  for (const members of groupBy(rows, keyFn).values()) {
    const ys = shuffle(members.map(({ row }) => row.y_after_002), rng);
    members.forEach(({ index }, offset) => {
      out[index].y_after_002 = ys[offset];
    });
  }
  return out;
}

function withRegisterBernoulliTerminals(rows, rng) {
  const groups = groupBy(rows, (row) => `${row.site}\t${row.type}\t${row.symbol}`);
  const rates = new Map();
  for (const [key, members] of groups) {
    rates.set(key, members.reduce((sum, { row }) => sum + row.terminal, 0) / members.length);
  }
  return rows.map((row) => {
    const rate = rates.get(`${row.site}\t${row.type}\t${row.symbol}`);
    return { ...row, terminal: rng() < rate ? 1 : 0 };
  });
}

function round(value) {
  return Number.isFinite(value) ? Number(value.toFixed(6)) : value;
}

function summarizeNull(rows, observed, metric) {
  const values = rows.map((row) => row[metric]).sort((a, b) => a - b);
  return {
    iterations: rows.length,
    observed: observed[metric],
    null_mean: rows.reduce((sum, row) => sum + row[metric], 0) / rows.length,
    null_p95: values[Math.min(values.length - 1, Math.ceil(values.length * 0.95) - 1)],
    null_max: Math.max(...rows.map((row) => row[metric])),
    fpr_ge_observed: rows.filter((row) => row[metric] >= observed[metric]).length / rows.length,
  };
}

function runScope(allRows, config, scopeIndex) {
  const rows = allRows.filter(config.filter);
  const observed = {
    scope: config.name,
    ...bestPosthocPartition(rows, config),
  };

  const nullDefs = [
    {
      name: 'terminal_shuffle_global',
      make: (rng) => withGlobalTerminalShuffle(rows, rng),
    },
    {
      name: 'terminal_shuffle_site_type_symbol',
      make: (rng) => withBlockTerminalShuffle(rows, rng, (row) => `${row.site}\t${row.type}\t${row.symbol}`),
    },
    {
      name: 'terminal_shuffle_site_type_symbol_prev1',
      make: (rng) => withBlockTerminalShuffle(rows, rng, (row) => `${row.site}\t${row.type}\t${row.symbol}\t${row.prev1_before_002}`),
    },
    {
      name: 'y_shuffle_global',
      make: (rng) => withGlobalYShuffle(rows, rng),
    },
    {
      name: 'y_shuffle_site_type_symbol',
      make: (rng) => withBlockYShuffle(rows, rng, (row) => `${row.site}\t${row.type}\t${row.symbol}`),
    },
    {
      name: 'register_bernoulli_terminals',
      make: (rng) => withRegisterBernoulliTerminals(rows, rng),
    },
  ];

  const iterationRows = [];
  const nullSummaries = {};
  nullDefs.forEach((def, defIndex) => {
    const rng = mulberry32(SEED + (scopeIndex + 1) * 0x100000 + defIndex * 0x9e3779b1);
    const rowsForNull = [];
    for (let iteration = 0; iteration < ITERATIONS; iteration += 1) {
      const score = bestPosthocPartition(def.make(rng), config);
      const iterationRow = {
        scope: config.name,
        null_model: def.name,
        iteration,
        ...score,
      };
      iterationRows.push(iterationRow);
      rowsForNull.push(iterationRow);
    }
    nullSummaries[def.name] = {
      best_z: summarizeNull(rowsForNull, observed, 'best_z'),
      best_gap: summarizeNull(rowsForNull, observed, 'best_gap'),
    };
  });

  return { rows, observed, iterationRows, nullSummaries };
}

function main() {
  const allRows = loadRows();
  const observedRows = [];
  const iterationRows = [];
  const scopes = {};

  SCOPE_CONFIGS.forEach((config, index) => {
    const result = runScope(allRows, config, index);
    observedRows.push(result.observed);
    iterationRows.push(...result.iterationRows);
    scopes[config.name] = {
      config: {
        min_y_rows: config.min_y_rows,
        min_closure_rows: config.min_closure_rows,
        min_branch_rows: config.min_branch_rows,
        min_closure_signs: config.min_closure_signs,
        min_branch_signs: config.min_branch_signs,
      },
      observed: result.observed,
      nulls: result.nullSummaries,
      worst_fpr_best_z: Math.max(...Object.values(result.nullSummaries).map((row) => row.best_z.fpr_ge_observed)),
      worst_fpr_best_gap: Math.max(...Object.values(result.nullSummaries).map((row) => row.best_gap.fpr_ge_observed)),
    };
  });

  writeCsv(OUT_OBSERVED, observedRows.map((row) => ({
    ...row,
    best_z: round(row.best_z),
    best_gap: round(row.best_gap),
    best_closure_rate: round(row.best_closure_rate),
    best_branch_rate: round(row.best_branch_rate),
  })), OBSERVED_FIELDS);

  writeCsv(OUT_ITERATIONS, iterationRows.map((row) => ({
    ...row,
    best_z: round(row.best_z),
    best_gap: round(row.best_gap),
    best_closure_rate: round(row.best_closure_rate),
    best_branch_rate: round(row.best_branch_rate),
  })), ITERATION_FIELDS);

  const summary = {
    date: RUN_DATE,
    seed: SEED,
    iterations_per_null_model: ITERATIONS,
    purpose:
      'Family-wise post-hoc forger for the 002-Y closure/branch candidate: each null corpus gets to discover its own best high-terminal versus low-terminal Y-sign partition under the same support thresholds.',
    input: 'data/open_prototype/reports/campaign_032_002_post_y_all_002_rows.csv',
    dedupe:
      'strict_complete_closed rows deduplicated by text_dedup_key + site + type + idx_002, matching campaign_032_002_y_forger_nulls.mjs',
    score:
      'Search all terminal-rate threshold pairs among eligible Y signs; require minimum signs and rows in both poles; score by two-proportion z and closure-minus-branch terminal-rate gap.',
    scopes,
    outputs: {
      observed_csv: path.relative(ROOT, OUT_OBSERVED).replaceAll('\\', '/'),
      iterations_csv: path.relative(ROOT, OUT_ITERATIONS).replaceAll('\\', '/'),
      summary_json: path.relative(ROOT, OUT_SUMMARY).replaceAll('\\', '/'),
    },
  };
  fs.writeFileSync(OUT_SUMMARY, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
  console.log(JSON.stringify({
    iterations_per_null_model: ITERATIONS,
    scopes: Object.fromEntries(Object.entries(scopes).map(([name, scope]) => [
      name,
      {
        observed_best_z: round(scope.observed.best_z),
        observed_best_gap: round(scope.observed.best_gap),
        worst_fpr_best_z: round(scope.worst_fpr_best_z),
        worst_fpr_best_gap: round(scope.worst_fpr_best_gap),
      },
    ])),
  }, null, 2));
}

main();
