// Discriminator for the seven "closed" selector signs that appear in 002-390-X frames
// (072, 095, 140, 346, 692, 705, 707). The bet: these are not one interchangeable bucket of
// terminal signs — each has its own ecology. 095 should track status/admin objects, 692
// should ride the portable 060-692 terminal suffix, 705 should reuse the wider 033-705
// formula, and the singletons should stay semantically thin. We read the filtered Indus
// inscription list (lipi/metadata_filtered.csv), keep one copy of each distinct sign
// sequence, and profile each X: its governed 002-390-X rows, its non-governed 390-X rows, and
// its global occurrences (terminal share, top predecessor, share on tablet/pot/tag-like
// "status" objects). Fixed rules assign each X a subtype classification, and the run passes
// if at least one admin, one suffix, and one formula-reuse subtype emerge. Writes ecology,
// target-row, and decision CSVs plus a JSON summary to data/open_prototype/reports.
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_closed_selector_ecology_discriminator_20260531';
const checkedDate = '2026-05-31';
const closedXs = ['072', '095', '140', '346', '692', '705', '707'];

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
  return [...String(text || '').matchAll(/\d{3}/g)].map((match) => match[0]);
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
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

function topCounts(items, fn, n = 10) {
  return countBy(items, fn)
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function safeShare(num, den) {
  return den ? (num / den).toFixed(6) : 'NA';
}

function statusLikeType(type) {
  return /TAB|POT|TAG|ROD|IMP/i.test(String(type || ''));
}

function targetKind(row) {
  const topPrevShare = row.top_prev_share === 'NA' ? 0 : Number(row.top_prev_share);
  const topPrevTerminalShare = row.top_prev_terminal_share === 'NA' ? 0 : Number(row.top_prev_terminal_share);
  const terminalShare = row.global_terminal_share === 'NA' ? 0 : Number(row.global_terminal_share);
  const statusShare = row.status_object_share === 'NA' ? 0 : Number(row.status_object_share);
  const targetCount = Number(row.target_count);
  const globalCount = Number(row.global_occurrences);

  if (row.x === '095' && statusShare >= 0.5 && row.admin_prev_share !== 'NA' && Number(row.admin_prev_share) >= 0.5) {
    return 'admin_status_closure_candidate';
  }
  if (row.x === '692' && terminalShare >= 0.65 && row.top_prev === '060' && topPrevShare >= 0.4) {
    return 'portable_terminal_suffix_candidate';
  }
  if (row.x === '705' && row.top_prev === '033' && topPrevShare >= 0.4 && topPrevTerminalShare < 0.2) {
    return 'formula_ecology_reused_as_governed_terminal';
  }
  if (targetCount === globalCount && globalCount <= 2) return 'governed_only_singleton_closure';
  if (terminalShare >= 0.65) return 'general_terminal_tendency';
  return 'weak_or_mixed_closure';
}

function exampleRows(rows, n = 8) {
  return rows
    .slice(0, n)
    .map((row) => `${row.cisi}:${row.text}`)
    .join(' | ');
}

fs.mkdirSync(reportsDir, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  tokens: signs(row.text),
}));
const canonicalRows = [...new Map(rawRows.map((row) => [row.tokens.join(' '), row])).values()];

const occurrences = [];
const targetRows = [];
const pairRows390 = [];
for (const row of canonicalRows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
    const sign = row.tokens[i];
    const prev = row.tokens[i - 1] ?? '<START>';
    const next = row.tokens[i + 1] ?? '<END>';
    occurrences.push({
      checked_date: checkedDate,
      cisi: objectId(row),
      row_id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      sign,
      prev,
      next,
      terminal: next === '<END>',
      status_like_object: statusLikeType(row.type),
      text: row.text,
    });
    if (row.tokens[i] === '390' && row.tokens[i + 1]) {
      const x = row.tokens[i + 1];
      const pair = {
        checked_date: checkedDate,
        cisi: objectId(row),
        row_id: row.id,
        site: row.site,
        type: row.type,
        shape: row.shape,
        x,
        post_002: row.tokens[i - 1] === '002',
        terminal_after_x: !row.tokens[i + 2],
        tail_after_x: row.tokens.slice(i + 2).join(' ') || '<END>',
        text: row.text,
      };
      pairRows390.push(pair);
      if (pair.post_002 && closedXs.includes(x)) targetRows.push(pair);
    }
  }
}

const ecologyRows = closedXs.map((x) => {
  const occ = occurrences.filter((row) => row.sign === x);
  const target = targetRows.filter((row) => row.x === x);
  const raw390 = pairRows390.filter((row) => row.x === x && !row.post_002);
  const prevCounts = countBy(occ, (row) => row.prev);
  const topPrev = prevCounts[0]?.[0] ?? '';
  const topPrevN = prevCounts[0]?.[1] ?? 0;
  const topPrevRows = occ.filter((row) => row.prev === topPrev);
  const adminPrevRows = occ.filter((row) => ['390', '520', '595'].includes(row.prev));
  const row = {
    checked_date: checkedDate,
    x,
    target_count: String(target.length),
    target_sites: topCounts(target, (row) => row.site),
    target_types: topCounts(target, (row) => row.type),
    target_terminal: String(target.filter((row) => row.terminal_after_x).length),
    target_terminal_share: safeShare(target.filter((row) => row.terminal_after_x).length, target.length),
    raw_non002_390x_count: String(raw390.length),
    raw_non002_390x_terminal_share: safeShare(raw390.filter((row) => row.terminal_after_x).length, raw390.length),
    global_occurrences: String(occ.length),
    global_terminal: String(occ.filter((row) => row.terminal).length),
    global_terminal_share: safeShare(occ.filter((row) => row.terminal).length, occ.length),
    status_object_count: String(occ.filter((row) => row.status_like_object).length),
    status_object_share: safeShare(occ.filter((row) => row.status_like_object).length, occ.length),
    top_prev: topPrev,
    top_prev_count: String(topPrevN),
    top_prev_share: safeShare(topPrevN, occ.length),
    top_prev_terminal_share: safeShare(topPrevRows.filter((row) => row.terminal).length, topPrevRows.length),
    admin_prev_count: String(adminPrevRows.length),
    admin_prev_share: safeShare(adminPrevRows.length, occ.length),
    prev_counts: topCounts(occ, (row) => row.prev),
    next_counts: topCounts(occ, (row) => row.next),
    site_counts: topCounts(occ, (row) => row.site),
    type_counts: topCounts(occ, (row) => row.type),
    classification: '',
    target_examples: exampleRows(target),
    global_examples: exampleRows(occ),
  };
  row.classification = targetKind(row);
  return row;
});

const adminStatus = ecologyRows.filter((row) => row.classification === 'admin_status_closure_candidate').length;
const portableSuffix = ecologyRows.filter((row) => row.classification === 'portable_terminal_suffix_candidate').length;
const formulaReuse = ecologyRows.filter((row) => row.classification === 'formula_ecology_reused_as_governed_terminal').length;
const singleton = ecologyRows.filter((row) => row.classification === 'governed_only_singleton_closure').length;
const weak = ecologyRows.filter((row) => row.classification === 'weak_or_mixed_closure').length;

const decision =
  adminStatus >= 1 && portableSuffix >= 1 && formulaReuse >= 1
    ? 'candidate_closed_selector_subtypes'
    : weak > 2
      ? 'wild_closed_selector_subtypes'
      : 'mixed_closed_selector_subtypes';
const confidenceTier = decision.startsWith('candidate') ? 'candidate' : 'wild shot';

const decisions = [
  {
    checked_date: checkedDate,
    bet_id: 'V9_CLOSED_X_SELECTOR_SUBTYPES_20260531',
    confidence_tier: confidenceTier,
    decision,
    risky_parse_bet:
      'Closed `002-390-X` signs are not one semantic bucket: `095` should behave like status/admin closure, `692` like portable terminal suffix/result, `705` like governed reuse of a larger formula ecology, and singleton closures should remain semantically thin.',
    what_would_promote:
      'New closed `002-390-X` rows preserve these ecology classes and show subtype-specific metadata/context, not interchangeable terminal signs.',
    what_would_break:
      'Closed X signs freely swap contexts, or `095/692/705` all reduce to the same copied terminal/register family.',
  },
];

const summary = {
  checked_date: checkedDate,
  status: 'closed_selector_ecology_discriminator',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: canonicalRows.length,
    closed_target_rows: targetRows.length,
  },
  classifications: ecologyRows.map((row) => `${row.x}:${row.classification}`).join(';'),
  class_counts: {
    admin_status: adminStatus,
    portable_suffix: portableSuffix,
    formula_reuse: formulaReuse,
    governed_only_singleton: singleton,
    weak_or_mixed: weak,
  },
  decisions: decisions.map((row) => `${row.bet_id}:${row.decision}`).join(';'),
};

writeCsv(path.join(reportsDir, `${prefix}_ecology.csv`), ecologyRows, [
  'checked_date',
  'x',
  'target_count',
  'target_sites',
  'target_types',
  'target_terminal',
  'target_terminal_share',
  'raw_non002_390x_count',
  'raw_non002_390x_terminal_share',
  'global_occurrences',
  'global_terminal',
  'global_terminal_share',
  'status_object_count',
  'status_object_share',
  'top_prev',
  'top_prev_count',
  'top_prev_share',
  'top_prev_terminal_share',
  'admin_prev_count',
  'admin_prev_share',
  'prev_counts',
  'next_counts',
  'site_counts',
  'type_counts',
  'classification',
  'target_examples',
  'global_examples',
]);

writeCsv(path.join(reportsDir, `${prefix}_target_rows.csv`), targetRows, [
  'checked_date',
  'cisi',
  'row_id',
  'site',
  'type',
  'shape',
  'x',
  'post_002',
  'terminal_after_x',
  'tail_after_x',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  'checked_date',
  'bet_id',
  'confidence_tier',
  'decision',
  'risky_parse_bet',
  'what_would_promote',
  'what_would_break',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
