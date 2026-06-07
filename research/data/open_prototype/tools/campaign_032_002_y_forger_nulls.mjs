import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const REPORTS = path.join(ROOT, 'data', 'open_prototype', 'reports');
const ALL_ROWS = path.join(REPORTS, 'campaign_032_002_post_y_all_002_rows.csv');
const BRANCH_ROWS = path.join(REPORTS, 'campaign_032_002_post_y_branch_rows.csv');
const ITERATIONS = Number(process.argv[2] || 2000);
const SEED = Number(process.argv[3] || 20260529);

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
  for (const row of rows) {
    lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  }
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function yClass(y) {
  if (y === '817') return 'hard_closure';
  if (y === '820' || y === '861') return 'leaky_closure';
  if (new Set(['390', '368', '031', '220', '900', '300']).has(y)) return 'branch_head';
  if (new Set(['824', '880', '003', '112', '142', '144', '221', '281', '326', '370']).has(y)) {
    return 'small_n_closure_like';
  }
  return 'other';
}

function yBinary(y) {
  const cls = yClass(y);
  if (cls === 'hard_closure' || cls === 'leaky_closure') return 'closure_family';
  if (cls === 'branch_head') return 'branch_family';
  return 'other';
}

function loadRows(file, scope) {
  const parsed = parseCsv(fs.readFileSync(file, 'utf8'));
  const seen = new Set();
  const rows = [];
  for (const row of parsed) {
    if (row.strict_complete_closed !== 'true') continue;
    const key = [row.text_dedup_key, row.site, row.type, row.idx_002].join('\u241f');
    if (seen.has(key)) continue;
    seen.add(key);
    const tokens = row.text_dedup_key.split(/\s+/).filter(Boolean);
    rows.push({
      ...row,
      scope,
      text_len: tokens.length,
      terminal: row.y_terminal === 'true' ? 1 : 0,
      y_class: yClass(row.y_after_002),
      y_binary: yBinary(row.y_after_002),
    });
  }
  return rows;
}

function groupBy(rows, keyFn) {
  const groups = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(row);
  }
  return groups;
}

function shuffled(values, rng) {
  const out = values.slice();
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rng() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function sample(values, rng) {
  return values[Math.floor(rng() * values.length)];
}

function cloneWithY(row, y) {
  return {
    ...row,
    y_after_002: y,
    y_class: yClass(y),
    y_binary: yBinary(y),
  };
}

function cloneWithTerminal(row, terminal) {
  return {
    ...row,
    terminal,
    y_terminal: terminal ? 'true' : 'false',
  };
}

function applyGlobalTerminalShuffle(rows, rng) {
  const terminals = shuffled(rows.map((r) => r.terminal), rng);
  return rows.map((row, i) => cloneWithTerminal(row, terminals[i]));
}

function applyBlockTerminalShuffle(rows, rng, blockKey) {
  const out = rows.map((r) => ({ ...r }));
  const groups = groupBy(rows.map((row, i) => ({ row, i })), ({ row }) => blockKey(row));
  for (const members of groups.values()) {
    const terminals = shuffled(members.map(({ row }) => row.terminal), rng);
    members.forEach(({ i }, j) => {
      out[i] = cloneWithTerminal(out[i], terminals[j]);
    });
  }
  return out;
}

function applyGlobalYShuffle(rows, rng) {
  const ys = shuffled(rows.map((r) => r.y_after_002), rng);
  return rows.map((row, i) => cloneWithY(row, ys[i]));
}

function applyBlockYShuffle(rows, rng, blockKey) {
  const out = rows.map((r) => ({ ...r }));
  const groups = groupBy(rows.map((row, i) => ({ row, i })), ({ row }) => blockKey(row));
  for (const members of groups.values()) {
    const ys = shuffled(members.map(({ row }) => row.y_after_002), rng);
    members.forEach(({ i }, j) => {
      out[i] = cloneWithY(out[i], ys[j]);
    });
  }
  return out;
}

function applyIndependentRegisterGenerator(rows, rng, blockKey) {
  const globalYs = rows.map((r) => r.y_after_002);
  const globalTerminalRate = rows.reduce((s, r) => s + r.terminal, 0) / rows.length;
  const groups = groupBy(rows, blockKey);
  const byKey = new Map();
  for (const [key, members] of groups) {
    byKey.set(key, {
      ys: members.map((r) => r.y_after_002),
      terminalRate: members.reduce((s, r) => s + r.terminal, 0) / members.length,
    });
  }
  return rows.map((row) => {
    const stats = byKey.get(blockKey(row));
    const ys = stats?.ys?.length ? stats.ys : globalYs;
    const rate = Number.isFinite(stats?.terminalRate) ? stats.terminalRate : globalTerminalRate;
    return cloneWithTerminal(cloneWithY(row, sample(ys, rng)), rng() < rate ? 1 : 0);
  });
}

function looScore(rows, keys) {
  const alpha = 1.0;
  const globalN = rows.length;
  const globalT = rows.reduce((s, r) => s + r.terminal, 0);
  const groups = new Map();
  for (const row of rows) {
    const key = keys.map((k) => row[k] ?? '').join('\u241f');
    const g = groups.get(key) ?? { n: 0, t: 0 };
    g.n += 1;
    g.t += row.terminal;
    groups.set(key, g);
  }

  let brier = 0;
  let logloss = 0;
  let acc = 0;
  for (const row of rows) {
    const y = row.terminal;
    const key = keys.map((k) => row[k] ?? '').join('\u241f');
    let { n, t } = groups.get(key);
    n -= 1;
    t -= y;
    if (n <= 0) {
      n = globalN - 1;
      t = globalT - y;
    }
    const p = Math.min(Math.max((t + alpha) / (n + 2 * alpha), 1e-6), 1 - 1e-6);
    brier += (p - y) ** 2;
    logloss += -(y * Math.log(p) + (1 - y) * Math.log(1 - p));
    acc += Number((p >= 0.5) === Boolean(y));
  }
  return {
    rows: rows.length,
    terminal_rows: globalT,
    accuracy: acc / rows.length,
    brier: brier / rows.length,
    logloss: logloss / rows.length,
  };
}

function closureBranchGap(rows) {
  const closure = rows.filter((r) => r.y_binary === 'closure_family');
  const branch = rows.filter((r) => r.y_binary === 'branch_family');
  const rate = (rs) => (rs.length ? rs.reduce((s, r) => s + r.terminal, 0) / rs.length : NaN);
  return {
    closure_rows: closure.length,
    branch_rows: branch.length,
    closure_terminal_rate: rate(closure),
    branch_terminal_rate: rate(branch),
    closure_minus_branch: rate(closure) - rate(branch),
  };
}

const registerKey = (row) => [row.site, row.type, row.symbol].join('\u241f');

function summarizeNull(observed, nullRows) {
  const geAcc = nullRows.filter((r) => r.accuracy >= observed.accuracy).length;
  const leBrier = nullRows.filter((r) => r.brier <= observed.brier).length;
  const leLogloss = nullRows.filter((r) => r.logloss <= observed.logloss).length;
  const geGap = nullRows.filter((r) => r.closure_minus_branch >= observed.closure_minus_branch).length;
  const values = (field) => nullRows.map((r) => r[field]).sort((a, b) => a - b);
  const quantile = (field, q) => {
    const xs = values(field);
    if (!xs.length) return null;
    return xs[Math.min(xs.length - 1, Math.max(0, Math.floor(q * (xs.length - 1))))];
  };
  return {
    iterations: nullRows.length,
    observed_accuracy: observed.accuracy,
    observed_brier: observed.brier,
    observed_logloss: observed.logloss,
    observed_closure_minus_branch: observed.closure_minus_branch,
    fpr_accuracy_ge_observed: geAcc / nullRows.length,
    fpr_brier_le_observed: leBrier / nullRows.length,
    fpr_logloss_le_observed: leLogloss / nullRows.length,
    fpr_gap_ge_observed: geGap / nullRows.length,
    null_accuracy_mean: nullRows.reduce((s, r) => s + r.accuracy, 0) / nullRows.length,
    null_accuracy_p95: quantile('accuracy', 0.95),
    null_brier_mean: nullRows.reduce((s, r) => s + r.brier, 0) / nullRows.length,
    null_brier_p05: quantile('brier', 0.05),
    null_logloss_mean: nullRows.reduce((s, r) => s + r.logloss, 0) / nullRows.length,
    null_logloss_p05: quantile('logloss', 0.05),
    null_gap_mean: nullRows.reduce((s, r) => s + r.closure_minus_branch, 0) / nullRows.length,
    null_gap_p95: quantile('closure_minus_branch', 0.95),
  };
}

function runScope(rows, scope, rng) {
  const observedMetrics = looScore(rows, ['y_class']);
  const observedGap = closureBranchGap(rows);
  const observed = { scope, null_model: 'observed', iteration: 0, ...observedMetrics, ...observedGap };
  const iterations = [];
  const nullModels = [
    ['terminal_shuffle_global', (rs) => applyGlobalTerminalShuffle(rs, rng)],
    ['terminal_shuffle_register', (rs) => applyBlockTerminalShuffle(rs, rng, registerKey)],
    ['y_shuffle_global', (rs) => applyGlobalYShuffle(rs, rng)],
    ['y_shuffle_register', (rs) => applyBlockYShuffle(rs, rng, registerKey)],
    ['independent_register_admin', (rs) => applyIndependentRegisterGenerator(rs, rng, registerKey)],
  ];

  for (let iteration = 1; iteration <= ITERATIONS; iteration += 1) {
    for (const [name, mutate] of nullModels) {
      const forged = mutate(rows);
      const metrics = looScore(forged, ['y_class']);
      const gap = closureBranchGap(forged);
      iterations.push({ scope, null_model: name, iteration, ...metrics, ...gap });
    }
  }

  const summary = {};
  for (const [name] of nullModels) {
    summary[name] = summarizeNull(observed, iterations.filter((r) => r.null_model === name));
  }
  return { observed, iterations, summary };
}

function main() {
  const rng = mulberry32(SEED);
  const scopes = [
    runScope(loadRows(ALL_ROWS, 'all_002_strict_dedup'), 'all_002_strict_dedup', rng),
    runScope(loadRows(BRANCH_ROWS, 'after_032_strict_dedup'), 'after_032_strict_dedup', rng),
  ];

  const iterationPath = path.join(REPORTS, 'campaign_032_002_y_forger_null_iterations.csv');
  const summaryPath = path.join(REPORTS, 'campaign_032_002_y_forger_null_summary.json');
  const iterationRows = scopes.flatMap((scope) => scope.iterations);
  writeCsv(iterationPath, iterationRows, [
    'scope',
    'null_model',
    'iteration',
    'rows',
    'terminal_rows',
    'accuracy',
    'brier',
    'logloss',
    'closure_rows',
    'branch_rows',
    'closure_terminal_rate',
    'branch_terminal_rate',
    'closure_minus_branch',
  ]);

  const summary = {
    date: '2026-05-29',
    seed: SEED,
    iterations_per_null_model: ITERATIONS,
    observed_model: 'leave-one-out terminality prediction from y_class',
    y_class_policy_source: 'tmp/run_032_002_y_matched_terminality.py fixed Y-class bins',
    scopes: Object.fromEntries(scopes.map((scope) => [
      scope.observed.scope,
      {
        observed: scope.observed,
        nulls: scope.summary,
      },
    ])),
    outputs: {
      iterations_csv: path.resolve(iterationPath),
      summary_json: path.resolve(summaryPath),
    },
  };
  fs.writeFileSync(summaryPath, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
  console.log(JSON.stringify(summary, null, 2));
}

main();
