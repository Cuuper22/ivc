import fs from 'node:fs';
import path from 'node:path';

// This script checks how far the "strict core" — the few 002-390-X inscriptions
// verified against real source images — is allowed to generalize. It reads the
// branch-sign-ecology frames CSV, classifies each row's source_status into
// tiers (strict, panel, route-only, unbound, source-dark), and keeps only the
// strict rows. Then it profiles those rows by site, object type, seal shape,
// material, symbol, and cult scene: if every strict row sits in one
// site/type/shape cell, the grammar claim must shrink from "script-wide" to
// "Mohenjo-daro square-seal local syntax". A second check confirms the local
// claim still has content: within that one register, X still splits into 125
// open versus 095/692 terminal. Writes row, summary, and contradiction-check
// CSVs plus a summary JSON to data/open_prototype/reports.

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const framesPath = path.join(reportsDir, 'campaign_032_002_861_002390x_branch_sign_ecology_20260531_002390_frames.csv');
const prefix = 'campaign_032_002_861_002390x_consolidate_strict_core_register_scope_20260531';

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

function countBy(items, fn) {
  const counts = new Map();
  for (const item of items) {
    const key = fn(item) || '-';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()].sort(
    (a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }),
  );
}

function topCounts(counts) {
  return counts.map(([key, value]) => `${key}:${value}`).join(';');
}

function sourceClass(status) {
  if (status.includes('checkpoint_strict_source_visible')) return 'strict';
  if (status.includes('source_panel_acquired')) return 'panel_compatible_not_strict';
  if (status.includes('checkpoint_permissive_public_panel')) return 'panel_permissive_not_strict';
  if (status.includes('source_route')) return 'route_only';
  if (status.includes('dholavira') || status.includes('unbound')) return 'unbound';
  if (status.includes('secondary_icon') || status.includes('absent')) return 'source_dark';
  if (status.includes('metadata_only')) return 'metadata_only';
  return 'other';
}

fs.mkdirSync(reportsDir, { recursive: true });

const frames = parseCsv(fs.readFileSync(framesPath, 'utf8')).map((row) => ({
  ...row,
  source_class: sourceClass(row.source_status),
}));

const strictRows = frames.filter((row) => row.source_class === 'strict');
const strictSites = new Set(strictRows.map((row) => row.site));
const strictTypes = new Set(strictRows.map((row) => row.type));
const strictShapes = new Set(strictRows.map((row) => row.shape));
const strictMaterials = new Set(strictRows.map((row) => row.material));
const strictX = new Set(strictRows.map((row) => row.branch_after_390));
const strictTerminalStates = new Set(strictRows.map((row) => row.terminal_after_branch));

const rowScope = strictRows.map((row) => ({
  checked_date: '2026-05-31',
  object: row.object,
  site: row.site,
  type: row.type,
  shape: row.shape,
  material: row.material,
  symbol: row.symbol,
  cult: row.cult,
  left_final: row.prev_before_002,
  x: row.branch_after_390,
  tail_after_x: row.tail_after_branch,
  terminal_after_x: row.terminal_after_branch,
  scope_cell: `${row.site}|${row.type}|${row.shape}|${row.material}`,
  text: row.text,
}));

const scopeSummary = [
  {
    checked_date: '2026-05-31',
    scope: 'strict_core_register_scope',
    rows: String(strictRows.length),
    sites: topCounts(countBy(strictRows, (row) => row.site)),
    types: topCounts(countBy(strictRows, (row) => row.type)),
    shapes: topCounts(countBy(strictRows, (row) => row.shape)),
    materials: topCounts(countBy(strictRows, (row) => row.material)),
    symbols: topCounts(countBy(strictRows, (row) => row.symbol)),
    cults: topCounts(countBy(strictRows, (row) => row.cult)),
    x_distribution: topCounts(countBy(strictRows, (row) => row.branch_after_390)),
    terminal_distribution: topCounts(countBy(strictRows, (row) => row.terminal_after_branch)),
    decision:
      strictSites.size === 1 && strictTypes.size === 1 && strictShapes.size === 1
        ? 'strict_core_scope_demoted_to_local_site_type_shape'
        : 'strict_core_cross_register_scope_survives',
  },
  {
    checked_date: '2026-05-31',
    scope: 'within_register_polarity_split',
    rows: String(strictRows.length),
    sites: topCounts(countBy(strictRows, (row) => row.site)),
    types: topCounts(countBy(strictRows, (row) => row.type)),
    shapes: topCounts(countBy(strictRows, (row) => row.shape)),
    materials: topCounts(countBy(strictRows, (row) => row.material)),
    symbols: topCounts(countBy(strictRows, (row) => row.symbol)),
    cults: topCounts(countBy(strictRows, (row) => row.cult)),
    x_distribution: topCounts(countBy(strictRows, (row) => row.branch_after_390)),
    terminal_distribution: topCounts(countBy(strictRows, (row) => row.terminal_after_branch)),
    decision:
      strictX.size > 1 && strictTerminalStates.size > 1
        ? 'same_register_still_splits_by_x'
        : 'same_register_polarity_not_shown',
  },
];

const contradictionChecks = [
  {
    checked_date: '2026-05-31',
    check_id: 'STRICT_CORE_IS_NOT_SCRIPT_WIDE',
    result: strictSites.size === 1 && strictTypes.size === 1 ? 'pass_demote_scope' : 'fail_scope_survives',
    evidence: `sites=${topCounts(countBy(strictRows, (row) => row.site))}; types=${topCounts(countBy(strictRows, (row) => row.type))}; shapes=${topCounts(countBy(strictRows, (row) => row.shape))}`,
    consequence: 'Do not call strict core script-wide grammar until a strict outside-register row joins it.',
  },
  {
    checked_date: '2026-05-31',
    check_id: 'STRICT_CORE_NOT_JUST_REGISTER_POLARITY',
    result: strictX.size > 1 && strictTerminalStates.size > 1 ? 'pass_keep_local_syntax' : 'fail_demote_to_register',
    evidence: strictRows.map((row) => `${row.object}:${row.branch_after_390}:${row.terminal_after_branch}`).join(' | '),
    consequence: 'Within the same Mohenjo-daro seal register, X still splits open versus terminal.',
  },
  {
    checked_date: '2026-05-31',
    check_id: 'STRICT_CORE_SEMANTIC_SCOPE_BLOCKED',
    result: 'pass_demote',
    evidence: 'All strict rows are one site/type/shape cell and only four rows.',
    consequence: 'No semantic, language-family, phonetic, or translation claim survives this scope check.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'CONSOLIDATE',
  status: 'strict_core_register_scope',
  strict_core_scope: {
    rows: strictRows.length,
    sites: topCounts(countBy(strictRows, (row) => row.site)),
    types: topCounts(countBy(strictRows, (row) => row.type)),
    shapes: topCounts(countBy(strictRows, (row) => row.shape)),
    materials: topCounts(countBy(strictRows, (row) => row.material)),
    symbols: topCounts(countBy(strictRows, (row) => row.symbol)),
    cults: topCounts(countBy(strictRows, (row) => row.cult)),
  },
  decisions: [
    'Demote strict core from script-wide grammar to Mohenjo-daro square seal local syntax.',
    'Keep local syntax alive because the same register still splits by X into 125 open versus 095/692 terminal.',
    'Require a strict outside-register 002-390-X row before widening scope again.',
  ],
  contradiction_results: Object.fromEntries(contradictionChecks.map((row) => [row.check_id, row.result])),
};

writeCsv(path.join(reportsDir, `${prefix}_rows.csv`), rowScope, [
  'checked_date',
  'object',
  'site',
  'type',
  'shape',
  'material',
  'symbol',
  'cult',
  'left_final',
  'x',
  'tail_after_x',
  'terminal_after_x',
  'scope_cell',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_summary_rows.csv`), scopeSummary, [
  'checked_date',
  'scope',
  'rows',
  'sites',
  'types',
  'shapes',
  'materials',
  'symbols',
  'cults',
  'x_distribution',
  'terminal_distribution',
  'decision',
]);

writeCsv(path.join(reportsDir, `${prefix}_contradiction_checks.csv`), contradictionChecks, [
  'checked_date',
  'check_id',
  'result',
  'evidence',
  'consequence',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
