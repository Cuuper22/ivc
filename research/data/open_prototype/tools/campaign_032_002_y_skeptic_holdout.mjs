// Skeptic's battery for the 002-Y closure/branch claim, run after the forger pass. The claim:
// the fixed Y-sign classes (hard closure 817, leaky closure 820/861, branch heads
// 390/368/031/220/900/300, plus a small-n closure-like set) predict whether an inscription
// ends right after 002-Y. This script attacks that from four angles. (1) Model comparison:
// leave-one-out terminality prediction from Y class versus register (site/type/symbol)
// baselines, including variants that exclude the test row's own register or prefix family
// from training. (2) Matched contrasts: closure-vs-branch terminal-rate gaps inside blocks
// matched on register, left context, position, and length. (3) Removal attacks: rerun the
// comparison with Mohenjo-daro, Harappa, SEAL:S, or unnamed-CISI rows dropped. (4) A
// right-edge audit that flags matchings which are tautological — where matching on length
// and 002 position already fixes the terminal outcome. Reads the strict, deduplicated rows
// from the campaign_032_002_post_y report CSVs; writes model, contrast, removal, and audit
// CSVs plus a JSON summary to data/open_prototype/reports.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const REPORTS = path.join(ROOT, 'data', 'open_prototype', 'reports');
const ALL_ROWS = path.join(REPORTS, 'campaign_032_002_post_y_all_002_rows.csv');
const BRANCH_ROWS = path.join(REPORTS, 'campaign_032_002_post_y_branch_rows.csv');

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
    const idx002 = Number(row.idx_002);
    rows.push({
      ...row,
      scope,
      tokens,
      text_len: tokens.length,
      idx_002_num: idx002,
      idx_002_from_right: tokens.length - idx002 - 1,
      terminal: row.y_terminal === 'true' ? 1 : 0,
      y_class: yClass(row.y_after_002),
      y_binary: yBinary(row.y_after_002),
      prefix_before_002: tokens.slice(0, idx002).join(' '),
      prefix2_before_002: tokens.slice(Math.max(0, idx002 - 2), idx002).join(' '),
      prefix3_before_002: tokens.slice(Math.max(0, idx002 - 3), idx002).join(' '),
      tail_after_y: tokens.slice(idx002 + 2).join(' '),
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

function keyOf(row, keys) {
  return keys.map((k) => row[k] ?? '').join('\u241f');
}

function looScore(rows, featureKeys, excludeBlockKeys = []) {
  const alpha = 1.0;
  let acc = 0;
  let brier = 0;
  let logloss = 0;
  for (const row of rows) {
    const featureKey = keyOf(row, featureKeys);
    const excluded = excludeBlockKeys.length ? keyOf(row, excludeBlockKeys) : null;
    const train = rows.filter((candidate) => {
      if (candidate === row) return false;
      if (!featureKeys.length) return true;
      if (keyOf(candidate, featureKeys) !== featureKey) return false;
      if (excluded !== null && keyOf(candidate, excludeBlockKeys) === excluded) return false;
      return true;
    });
    const fallback = rows.filter((candidate) => {
      if (candidate === row) return false;
      if (excluded !== null && keyOf(candidate, excludeBlockKeys) === excluded) return false;
      return true;
    });
    const usable = train.length ? train : fallback;
    const n = usable.length;
    const t = usable.reduce((s, r) => s + r.terminal, 0);
    const p = Math.min(Math.max((t + alpha) / (n + 2 * alpha), 1e-6), 1 - 1e-6);
    const y = row.terminal;
    acc += Number((p >= 0.5) === Boolean(y));
    brier += (p - y) ** 2;
    logloss += -(y * Math.log(p) + (1 - y) * Math.log(1 - p));
  }
  return {
    rows: rows.length,
    terminal_rows: rows.reduce((s, r) => s + r.terminal, 0),
    accuracy: rows.length ? acc / rows.length : null,
    brier: rows.length ? brier / rows.length : null,
    logloss: rows.length ? logloss / rows.length : null,
  };
}

function modelRows(rows, scope) {
  const models = [
    ['global', [], []],
    ['register', ['site', 'type', 'symbol'], []],
    ['register_prev1', ['site', 'type', 'symbol', 'prev1_before_002'], []],
    ['y_binary', ['y_binary'], []],
    ['y_class', ['y_class'], []],
    ['y_class_leave_site_type_symbol', ['y_class'], ['site', 'type', 'symbol']],
    ['y_class_leave_site_type_symbol_prefix2', ['y_class'], ['site', 'type', 'symbol', 'prefix2_before_002']],
    ['y_class_leave_prefix3', ['y_class'], ['prefix3_before_002']],
    ['register_plus_y_class_leave_site_type_symbol_prefix2', ['site', 'type', 'symbol', 'y_class'], ['site', 'type', 'symbol', 'prefix2_before_002']],
  ];
  return models.map(([model, features, excluded]) => ({
    scope,
    model,
    features: features.join(';'),
    excluded_block: excluded.join(';'),
    ...looScore(rows, features, excluded),
  }));
}

function contrastRows(rows, scope) {
  const specs = [
    ['site_type_symbol', ['site', 'type', 'symbol']],
    ['site_type_symbol_prev1', ['site', 'type', 'symbol', 'prev1_before_002']],
    ['site_type_symbol_prefix2', ['site', 'type', 'symbol', 'prefix2_before_002']],
    ['site_type_symbol_idx002', ['site', 'type', 'symbol', 'idx_002']],
    ['site_type_symbol_len_bucket', ['site', 'type', 'symbol', 'text_len']],
  ];
  const out = [];
  for (const [name, keys] of specs) {
    const groups = groupBy(rows.filter((r) => ['closure_family', 'branch_family'].includes(r.y_binary)), (row) => keyOf(row, keys));
    for (const [blockKey, members] of groups) {
      const closure = members.filter((r) => r.y_binary === 'closure_family');
      const branch = members.filter((r) => r.y_binary === 'branch_family');
      if (!closure.length || !branch.length) continue;
      const cTerm = closure.reduce((s, r) => s + r.terminal, 0);
      const bTerm = branch.reduce((s, r) => s + r.terminal, 0);
      const cRate = cTerm / closure.length;
      const bRate = bTerm / branch.length;
      out.push({
        scope,
        block_name: name,
        block_key: blockKey.replaceAll('\u241f', '|'),
        rows: members.length,
        closure_rows: closure.length,
        closure_terminal: cTerm,
        closure_rate: cRate,
        branch_rows: branch.length,
        branch_terminal: bTerm,
        branch_rate: bRate,
        closure_minus_branch: cRate - bRate,
        closure_y_counts: [...groupBy(closure, (r) => r.y_after_002)].map(([k, v]) => `${k}:${v.length}`).join(';'),
        branch_y_counts: [...groupBy(branch, (r) => r.y_after_002)].map(([k, v]) => `${k}:${v.length}`).join(';'),
        examples: members.slice(0, 12).map((r) => r.cisi || r.id).join(';'),
      });
    }
  }
  return out;
}

function removalRows(rows, scope) {
  const removals = [
    ['remove_mohenjo_daro_seal_s', (r) => !(r.site === 'Mohenjo-daro' && r.type === 'SEAL:S')],
    ['remove_harappa', (r) => r.site !== 'Harappa'],
    ['remove_mohenjo_daro', (r) => r.site !== 'Mohenjo-daro'],
    ['remove_seal_s', (r) => r.type !== 'SEAL:S'],
    ['only_named_cisi', (r) => r.cisi && r.cisi !== '-'],
  ];
  return removals.map(([attack, keep]) => {
    const kept = rows.filter(keep);
    const score = looScore(kept, ['y_class']);
    const register = looScore(kept, ['site', 'type', 'symbol']);
    return {
      scope,
      attack,
      rows: kept.length,
      y_class_accuracy: score.accuracy,
      y_class_brier: score.brier,
      y_class_logloss: score.logloss,
      register_accuracy: register.accuracy,
      register_brier: register.brier,
      register_logloss: register.logloss,
      y_class_minus_register_accuracy: score.accuracy - register.accuracy,
      y_class_brier_advantage: register.brier - score.brier,
    };
  });
}

function rightEdgeAudit(rows, scope) {
  const specs = [
    ['text_len_idx002', ['text_len', 'idx_002']],
    ['site_type_symbol_text_len_idx002', ['site', 'type', 'symbol', 'text_len', 'idx_002']],
    ['site_type_symbol_idx002_from_right', ['site', 'type', 'symbol', 'idx_002_from_right']],
  ];
  const out = [];
  for (const [name, keys] of specs) {
    const groups = groupBy(rows, (row) => keyOf(row, keys));
    let variableBlocks = 0;
    let variableRows = 0;
    let closureBranchVariableBlocks = 0;
    for (const members of groups.values()) {
      const terminalStates = new Set(members.map((r) => r.terminal));
      if (terminalStates.size > 1) {
        variableBlocks += 1;
        variableRows += members.length;
      }
      const hasClosure = members.some((r) => r.y_binary === 'closure_family');
      const hasBranch = members.some((r) => r.y_binary === 'branch_family');
      if (terminalStates.size > 1 && hasClosure && hasBranch) closureBranchVariableBlocks += 1;
    }
    out.push({
      scope,
      match_name: name,
      keys: keys.join(';'),
      blocks: groups.size,
      variable_terminality_blocks: variableBlocks,
      variable_terminality_rows: variableRows,
      closure_branch_variable_blocks: closureBranchVariableBlocks,
      interpretation: variableBlocks === 0
        ? 'No valid terminality test: matching these right-edge fields fixes the terminal outcome.'
        : 'Terminality still varies inside some matched blocks; use only those as non-tautological contrast blocks.',
    });
  }
  return out;
}

function summarize(scope, rows, models, contrasts, removals, rightEdge) {
  const bestYClass = models.find((r) => r.model === 'y_class');
  const bestBlocked = models.find((r) => r.model === 'y_class_leave_site_type_symbol_prefix2');
  const register = models.find((r) => r.model === 'register');
  const contrastByName = {};
  for (const row of contrasts) {
    const acc = contrastByName[row.block_name] ?? { blocks: 0, weightedGap: 0, rows: 0 };
    acc.blocks += 1;
    acc.weightedGap += Number(row.closure_minus_branch) * Number(row.rows);
    acc.rows += Number(row.rows);
    contrastByName[row.block_name] = acc;
  }
  for (const acc of Object.values(contrastByName)) {
    acc.weighted_mean_closure_minus_branch = acc.rows ? acc.weightedGap / acc.rows : null;
    delete acc.weightedGap;
  }
  return {
    scope,
    rows: rows.length,
    y_class_accuracy: bestYClass?.accuracy ?? null,
    y_class_brier: bestYClass?.brier ?? null,
    register_accuracy: register?.accuracy ?? null,
    register_brier: register?.brier ?? null,
    family_blocked_y_class_accuracy: bestBlocked?.accuracy ?? null,
    family_blocked_y_class_brier: bestBlocked?.brier ?? null,
    contrast_summary: contrastByName,
    removal_attacks: removals,
    right_edge_audit: rightEdge,
    decision: 'skeptic_holdout_strengthens_but_does_not_accept_without_source_normalized_image_direction_gate',
  };
}

function runScope(rows, scope) {
  const models = modelRows(rows, scope);
  const contrasts = contrastRows(rows, scope);
  const removals = removalRows(rows, scope);
  const rightEdge = rightEdgeAudit(rows, scope);
  return { models, contrasts, removals, rightEdge, summary: summarize(scope, rows, models, contrasts, removals, rightEdge) };
}

function main() {
  const scopes = [
    runScope(loadRows(ALL_ROWS, 'all_002_strict_dedup'), 'all_002_strict_dedup'),
    runScope(loadRows(BRANCH_ROWS, 'after_032_strict_dedup'), 'after_032_strict_dedup'),
  ];
  const modelPath = path.join(REPORTS, 'campaign_032_002_y_skeptic_holdout_models.csv');
  const contrastPath = path.join(REPORTS, 'campaign_032_002_y_skeptic_holdout_matched_contrasts.csv');
  const removalPath = path.join(REPORTS, 'campaign_032_002_y_skeptic_holdout_removals.csv');
  const rightEdgePath = path.join(REPORTS, 'campaign_032_002_y_skeptic_holdout_right_edge_audit.csv');
  const summaryPath = path.join(REPORTS, 'campaign_032_002_y_skeptic_holdout_summary.json');

  writeCsv(modelPath, scopes.flatMap((s) => s.models), [
    'scope',
    'model',
    'features',
    'excluded_block',
    'rows',
    'terminal_rows',
    'accuracy',
    'brier',
    'logloss',
  ]);
  writeCsv(contrastPath, scopes.flatMap((s) => s.contrasts), [
    'scope',
    'block_name',
    'block_key',
    'rows',
    'closure_rows',
    'closure_terminal',
    'closure_rate',
    'branch_rows',
    'branch_terminal',
    'branch_rate',
    'closure_minus_branch',
    'closure_y_counts',
    'branch_y_counts',
    'examples',
  ]);
  writeCsv(removalPath, scopes.flatMap((s) => s.removals), [
    'scope',
    'attack',
    'rows',
    'y_class_accuracy',
    'y_class_brier',
    'y_class_logloss',
    'register_accuracy',
    'register_brier',
    'register_logloss',
    'y_class_minus_register_accuracy',
    'y_class_brier_advantage',
  ]);
  writeCsv(rightEdgePath, scopes.flatMap((s) => s.rightEdge), [
    'scope',
    'match_name',
    'keys',
    'blocks',
    'variable_terminality_blocks',
    'variable_terminality_rows',
    'closure_branch_variable_blocks',
    'interpretation',
  ]);

  const summary = {
    date: '2026-05-29',
    purpose: 'Hostile tests for 002-Y closure/branch candidate after forger pass.',
    caveat: 'Exact right-edge matching by text_len and idx_002 is tautological for terminality; this script records that failure mode instead of pretending it is a valid holdout.',
    scopes: Object.fromEntries(scopes.map((scope) => [scope.summary.scope, scope.summary])),
    outputs: {
      models_csv: path.resolve(modelPath),
      matched_contrasts_csv: path.resolve(contrastPath),
      removals_csv: path.resolve(removalPath),
      right_edge_audit_csv: path.resolve(rightEdgePath),
      summary_json: path.resolve(summaryPath),
    },
  };
  fs.writeFileSync(summaryPath, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
  console.log(JSON.stringify(summary, null, 2));
}

main();
