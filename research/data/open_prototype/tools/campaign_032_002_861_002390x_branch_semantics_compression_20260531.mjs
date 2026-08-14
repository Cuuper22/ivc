// Compresses what we are allowed to claim about each 002-390-X branch sign,
// separating syntax from semantics. Syntax means positional behavior (does the
// branch close the sequence, continue it, or link one complement); semantics
// means any meaning gloss (rank/title, status/admin, result lane). This script
// reads the 002-390 frames CSV from the branch-sign-ecology run, tags each row
// with a source tier (strict source-visible down to metadata-unbound), groups
// rows by branch sign, and applies hand-written per-branch rules for 125, 530,
// 590, 095, 692, and 705; everything else is a form-only singleton. It writes
// a branch summary CSV, a semantic-demotions CSV, and a summary JSON to
// data/open_prototype/reports/. The headline decision: syntax survives better
// than semantics — positional roles are kept as candidates, but most meaning
// glosses are demoted to "wild" until stricter source evidence arrives.

import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const targetFramesPath = path.join(
  root,
  'data',
  'open_prototype',
  'reports',
  'campaign_032_002_861_002390x_branch_sign_ecology_20260531_002390_frames.csv',
);
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_branch_semantics_compression_20260531';
const checkedDate = '2026-05-31';

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

function sourceTier(sourceStatus) {
  if (sourceStatus.includes('checkpoint_strict_source_visible')) return 'strict';
  if (sourceStatus.includes('source_panel_acquired')) return 'panel_compatible_not_strict';
  if (sourceStatus.includes('permissive_public_panel')) return 'permissive_public_panel';
  if (sourceStatus.includes('unbound') || sourceStatus.includes('metadata_only')) return 'metadata_unbound';
  return 'route_or_secondary';
}

function countBy(rows, field) {
  const counts = new Map();
  for (const row of rows) {
    const key = row[field] || '-';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()].sort(
    (a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }),
  );
}

function topList(rows, field) {
  return countBy(rows, field)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function uniqueCount(rows, field) {
  return new Set(rows.map((row) => row[field] || '-')).size;
}

function branchDecision(branch, rows) {
  const strictRows = rows.filter((row) => row.source_tier === 'strict');
  const terminal = rows.filter((row) => row.terminal_after_branch === 'True').length;
  const continuing = rows.length - terminal;
  const typeCount = uniqueCount(rows, 'type');
  const siteCount = uniqueCount(rows, 'site');
  const cultCount = uniqueCount(rows, 'cult');
  const hasMetadataMajority = rows.filter((row) => row.source_tier === 'metadata_unbound').length >= rows.length / 2;

  if (branch === '125') {
    return {
      syntax_tier: terminal === 0 ? 'candidate_open_continuing' : 'demoted',
      semantic_tier: strictRows.length >= 2 ? 'candidate_narrow_rank_title_selector' : 'wild',
      decision: 'keep continuing-selector syntax; rank/title semantics only in final235/P086 lane',
    };
  }
  if (branch === '530') {
    return {
      syntax_tier: continuing === 1 && rows.length === 1 ? 'candidate_one_complement_linker' : 'demoted',
      semantic_tier: 'wild',
      decision: 'keep one-complement syntax; do not assign semantic value until token-strict H-773',
    };
  }
  if (branch === '590') {
    return {
      syntax_tier: continuing === 1 && rows.length === 1 ? 'local_candidate_formula_bridge' : 'demoted',
      semantic_tier: 'wild',
      decision: 'keep local bridge only if 3335.1 source-binds; global 390-590 rule is killed',
    };
  }
  if (branch === '095') {
    const heterogeneous = typeCount > 1 || siteCount > 1 || cultCount > 1;
    return {
      syntax_tier: terminal === rows.length ? 'candidate_terminal_closure' : 'demoted',
      semantic_tier: heterogeneous ? 'wild' : 'candidate_edge',
      decision: heterogeneous
        ? 'demote status/admin semantics; strict M-71 seal and route H-1993 tablet are context-heterogeneous'
        : 'retain weak status/admin semantics',
    };
  }
  if (branch === '692') {
    return {
      syntax_tier: terminal === rows.length ? 'candidate_terminal_closure' : 'demoted',
      semantic_tier: strictRows.length === 1 && rows.length === 1 ? 'candidate_edge_result_lane' : 'wild',
      decision: 'keep result/suffix semantics only as 032-lane singleton pressure from strict M-70',
    };
  }
  if (branch === '705') {
    return {
      syntax_tier: terminal === rows.length ? 'candidate_terminal_closure' : 'demoted',
      semantic_tier: hasMetadataMajority ? 'wild_to_candidate_edge' : 'candidate_edge',
      decision: 'keep terminal ecology; no semantic promotion until repeated strict M-1825/Dholavira pair',
    };
  }
  return {
    syntax_tier: terminal === rows.length ? 'form_only_terminal_wild' : 'form_only_mixed_wild',
    semantic_tier: 'wild',
    decision: 'singleton form-only branch; do not semanticize',
  };
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(targetFramesPath, 'utf8')).map((row) => ({
  ...row,
  source_tier: sourceTier(row.source_status),
}));

const byBranch = new Map();
for (const row of rows) {
  const branch = row.branch_after_390;
  if (!byBranch.has(branch)) byBranch.set(branch, []);
  byBranch.get(branch).push(row);
}

const branchRows = [...byBranch.entries()]
  .sort((a, b) => b[1].length - a[1].length || a[0].localeCompare(b[0], undefined, { numeric: true }))
  .map(([branch, branchRowsForSign]) => {
    const decision = branchDecision(branch, branchRowsForSign);
    return {
      checked_date: checkedDate,
      branch,
      target_rows: String(branchRowsForSign.length),
      strict_rows: String(branchRowsForSign.filter((row) => row.source_tier === 'strict').length),
      terminal_rows: String(branchRowsForSign.filter((row) => row.terminal_after_branch === 'True').length),
      continuing_rows: String(branchRowsForSign.filter((row) => row.terminal_after_branch !== 'True').length),
      sites: topList(branchRowsForSign, 'site'),
      types: topList(branchRowsForSign, 'type'),
      symbols: topList(branchRowsForSign, 'symbol'),
      cults: topList(branchRowsForSign, 'cult'),
      source_tiers: topList(branchRowsForSign, 'source_tier'),
      syntax_tier: decision.syntax_tier,
      semantic_tier: decision.semantic_tier,
      decision: decision.decision,
      rows: branchRowsForSign
        .map((row) => `${row.object}:${row.prev_before_002}->${branch}->${row.tail_after_branch}:${row.source_tier}`)
        .join(' | '),
    };
  });

const demotionRows = branchRows
  .filter((row) => ['wild', 'wild_to_candidate_edge'].includes(row.semantic_tier))
  .map((row) => ({
    checked_date: checkedDate,
    branch: row.branch,
    demoted_claim: row.branch === '095'
      ? '095_status_admin_semantics'
      : row.branch === '530'
        ? '530_semantic_value'
        : row.branch === '590'
          ? '590_global_formula_semantics'
          : row.branch === '705'
            ? '705_contextual_semantics'
            : `${row.branch}_semantic_value`,
    retained_claim: row.syntax_tier,
    reason: row.decision,
  }));

writeCsv(
  path.join(reportsDir, `${prefix}_branch_summary.csv`),
  branchRows,
  [
    'checked_date',
    'branch',
    'target_rows',
    'strict_rows',
    'terminal_rows',
    'continuing_rows',
    'sites',
    'types',
    'symbols',
    'cults',
    'source_tiers',
    'syntax_tier',
    'semantic_tier',
    'decision',
    'rows',
  ],
);
writeCsv(
  path.join(reportsDir, `${prefix}_semantic_demotions.csv`),
  demotionRows,
  ['checked_date', 'branch', 'demoted_claim', 'retained_claim', 'reason'],
);

const summary = {
  checked_date: checkedDate,
  status: 'branch_semantics_compression',
  target_rows: rows.length,
  branches: branchRows.length,
  semantic_demotions: demotionRows.length,
  decision:
    'syntax_survives_more_than_semantics; keep open/closed/linker/bridge roles, demote most semantic glosses below candidate',
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
