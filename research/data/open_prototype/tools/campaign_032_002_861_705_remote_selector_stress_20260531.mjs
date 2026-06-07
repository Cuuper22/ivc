import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const BRANCH_FRAMES = path.join(
  ROOT,
  'data',
  'open_prototype',
  'reports',
  'risky_002390_canonical_branch_selector_forger_20260531_frames.csv',
);
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'campaign_032_002_861_705_remote_selector_stress_20260531';
const RUN_DATE = '2026-05-31';

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

function csvEscape(value) {
  const text = String(value ?? '');
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(',')];
  for (const row of rows) lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function norm(value, fallback = 'NA') {
  const text = String(value ?? '').trim();
  return text && text !== '-' && text !== 'None' ? text : fallback;
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function countBy(items, fn) {
  const counts = new Map();
  for (const item of items) {
    const key = fn(item);
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()].sort(
    (a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }),
  );
}

function top(counts, n = 8) {
  return counts
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function pct(value, total) {
  return total ? (value / total).toFixed(6) : '0.000000';
}

function sourceStatus(object) {
  const branchRows = sourceRows.filter((row) => row.object === object && row.branch === '705');
  return branchRows[0]?.source_status ?? 'metadata_or_nonframe';
}

function sourceBucket(object) {
  const branchRows = sourceRows.filter((row) => row.object === object && row.branch === '705');
  return branchRows[0]?.source_bucket ?? 'metadata_or_nonframe';
}

function occurrenceRows(rows) {
  const out = [];
  for (const row of rows) {
    row.signs.forEach((sign, idx) => {
      if (sign === '000') return;
      const prev = row.signs[idx - 1] ?? '<START>';
      const prev2 = row.signs[idx - 2] ?? '<START>';
      const next = row.signs[idx + 1] ?? '<END>';
      const object = objectId(row);
      out.push({
        checked_date: RUN_DATE,
        sign,
        row_id: row.id,
        object,
        site: norm(row.site),
        region: norm(row.region),
        type: norm(row.type),
        shape: norm(row.shape),
        material: norm(row.material),
        symbol: norm(row.symbol),
        cult: norm(row.cult),
        prev,
        prev2,
        next,
        next2: row.signs[idx + 2] ?? '<END>',
        terminal: idx === row.signs.length - 1 ? 'true' : 'false',
        in_002_390_frame: prev2 === '002' && prev === '390' ? 'true' : 'false',
        in_033_705_formula: prev === '033' ? 'true' : 'false',
        source_status: sourceStatus(object),
        source_bucket: sourceBucket(object),
        exact_sequence: row.signs.join(' '),
        text: row.text,
      });
    });
  }
  return out;
}

function familySummary(name, rows, implication) {
  const terminal = rows.filter((row) => row.terminal === 'true').length;
  const exactCounts = countBy(rows, (row) => row.exact_sequence);
  const prevCounts = countBy(rows, (row) => row.prev);
  const nextCounts = countBy(rows, (row) => row.next);
  return {
    checked_date: RUN_DATE,
    family: name,
    rows: String(rows.length),
    terminal: String(terminal),
    terminal_share: pct(terminal, rows.length),
    sites: String(new Set(rows.map((row) => row.site)).size),
    regions: String(new Set(rows.map((row) => row.region)).size),
    types: String(new Set(rows.map((row) => row.type)).size),
    symbols: String(new Set(rows.map((row) => row.symbol)).size),
    exact_sequences: String(exactCounts.length),
    top_exact_sequence_share: pct(exactCounts[0]?.[1] ?? 0, rows.length),
    source_buckets: top(countBy(rows, (row) => row.source_bucket)),
    top_sites: top(countBy(rows, (row) => row.site)),
    top_regions: top(countBy(rows, (row) => row.region)),
    top_types: top(countBy(rows, (row) => row.type)),
    top_symbols: top(countBy(rows, (row) => row.symbol)),
    top_prevs: top(prevCounts),
    top_nexts: top(nextCounts),
    top_exact_sequences: top(exactCounts, 6),
    rows_preview: rows.map((row) => `${row.object}:${row.prev2}-${row.prev}-705->${row.next}`).join(';'),
    implication,
  };
}

fs.mkdirSync(OUT_DIR, { recursive: true });

const sourceRows = fs.existsSync(BRANCH_FRAMES) ? parseCsv(fs.readFileSync(BRANCH_FRAMES, 'utf8')) : [];
const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()];
const rawOccs = occurrenceRows(rawRows).filter((occ) => occ.sign === '705');
const occs = occurrenceRows(canonicalRows).filter((occ) => occ.sign === '705');
const frameRows = occs.filter((occ) => occ.in_002_390_frame === 'true');
const formula033Rows = occs.filter((occ) => occ.in_033_705_formula === 'true');
const non033Rows = occs.filter((occ) => occ.in_033_705_formula !== 'true');
const nonframe390Rows = occs.filter((occ) => occ.prev === '390' && occ.in_002_390_frame !== 'true');
const strictOrRouteFrameRows = frameRows.filter((occ) => occ.source_bucket !== 'metadata_only');

const familyRows = [
  familySummary(
    '002-390-705',
    frameRows,
    '`705` is a repeated terminal branch after `002-390` with two different left stems and two regions, but both rows are route-pressure only.',
  ),
  familySummary(
    '033-705-global-formula',
    formula033Rows,
    'The dominant global `705` ecology is `033-705`, mostly not terminal; this is the main leakage adversary.',
  ),
  familySummary(
    'non033-705',
    non033Rows,
    '`705` outside the dominant `033` formula is still widespread; `390-705` is a tiny special lane inside it.',
  ),
  familySummary(
    'nonframe-390-705',
    nonframe390Rows,
    'There are no non-frame `390-705` rows; every `390-705` occurrence is immediately after `002`.',
  ),
];

const globalPrevCounts = countBy(occs, (occ) => occ.prev);
const globalNextCounts = countBy(occs, (occ) => occ.next);
const decisions = [
  {
    checked_date: RUN_DATE,
    named_bet: '`705` is a formal terminal selector under `002-390`, not `033-705` formula leakage',
    tier_after_test:
      frameRows.length === 2 &&
      frameRows.every((row) => row.terminal === 'true') &&
      nonframe390Rows.length === 0
        ? 'candidate_form_source_weak'
        : 'wild_shot_only',
    evidence:
      `Canonical 705 has ${occs.length} occurrences; 390-705 occurs ${frameRows.length} times, both after 002 and both terminal. The dominant global predecessor is ${globalPrevCounts[0][0]} with ${globalPrevCounts[0][1]} rows, but the frame rows do not use that predecessor.`,
    adversary:
      'Both `002-390-705` rows are route-pressure rather than strict signband evidence, and 705 has heavy formula ecology outside the frame.',
    falsifier_or_rescue:
      'Source-bound continuation after `002-390-705` kills the terminal-selector rule. Strict source-binding of both M-1825 and Dholavira 4237.1 as terminal promotes the formal branch selector.',
  },
  {
    checked_date: RUN_DATE,
    named_bet: '`705` marks remote/transfer/regional class under `002-390`',
    tier_after_test: frameRows.length === 2 && new Set(frameRows.map((row) => row.region)).size === 2
      ? 'wild_shot_retained'
      : 'wild_shot_weakened',
    evidence:
      `The two frame rows are Mohenjo-daro/Lower Indus and Dholavira/Gujarat-Kutch square seals with different left stems, both terminal.`,
    adversary:
      'Two rows are too few, both are bull square seals, and both are source-gated. Cross-region does not by itself mean remote/transfer semantics.',
    falsifier_or_rescue:
      'A third terminal `002-390-705` from a different region or administrative context promotes the semantic guess to candidate. A source-bound copied tail or local duplicate collapse kills it.',
  },
  {
    checked_date: RUN_DATE,
    named_bet: '`390-705` is generic post-390 behavior independent of `002`',
    tier_after_test: nonframe390Rows.length === 0 ? 'dead_for_now' : 'candidate_retained',
    evidence:
      `There are ${nonframe390Rows.length} non-frame 390-705 rows; all 390-705 cases are immediately preceded by 002.`,
    adversary:
      'Absence in this dataset may be sampling, not grammar; the null can revive if new non-002 390-705 rows appear.',
    falsifier_or_rescue:
      'A non-002 390-705 row with the same terminal behavior revives generic post-390 behavior and weakens 002-conditioning.',
  },
  {
    checked_date: RUN_DATE,
    named_bet: '`033-705` formula leakage explains the `002-390-705` branch',
    tier_after_test: frameRows.some((row) => row.prev === '033' || row.prev2 === '033') ? 'candidate_retained' : 'demoted',
    evidence:
      `033-705 has ${formula033Rows.length} canonical rows, but neither 002-390-705 row contains 033 adjacent to 705; frame left stems are ${frameRows.map((row) => row.prev2).join('/')}.`,
    adversary:
      '705 could still be a visual/cultural template reused in a different syntactic frame rather than a branch selector.',
    falsifier_or_rescue:
      'If source images show the frame rows are copied from longer 033-705 formulae or preserve hidden 033 material, revive this leakage explanation.',
  },
];

const summary = {
  checked_date: RUN_DATE,
  status: '705_remote_selector_stress',
  hypothesis_tested:
    '`705` is a formal terminal selector under `002-390`; remote/transfer/regional semantics remain a wild shot unless cross-region source binding improves.',
  totals: {
    raw_rows: rawRows.length,
    canonical_rows: canonicalRows.length,
    raw_705_occurrences: rawOccs.length,
    canonical_705_occurrences: occs.length,
    frame_002390705_rows: frameRows.length,
    route_or_strict_frame_rows: strictOrRouteFrameRows.length,
    nonframe_390705_rows: nonframe390Rows.length,
  },
  global_ecology: {
    terminal: occs.filter((occ) => occ.terminal === 'true').length,
    terminal_share: pct(occs.filter((occ) => occ.terminal === 'true').length, occs.length),
    top_prevs: top(globalPrevCounts, 12),
    top_nexts: top(globalNextCounts, 12),
  },
  family_rows: familyRows,
  frame_rows: frameRows,
  decisions,
  confidence_after_test: {
    formal_705_terminal_selector_under_002390: decisions[0].tier_after_test,
    remote_transfer_regional_semantics: decisions[1].tier_after_test,
    generic_post390_705: decisions[2].tier_after_test,
    formula033_leakage: decisions[3].tier_after_test,
  },
};

writeCsv(
  path.join(OUT_DIR, `${PREFIX}_occurrences.csv`),
  occs,
  [
    'checked_date',
    'row_id',
    'object',
    'site',
    'region',
    'type',
    'shape',
    'material',
    'symbol',
    'cult',
    'prev2',
    'prev',
    'sign',
    'next',
    'next2',
    'terminal',
    'in_002_390_frame',
    'in_033_705_formula',
    'source_status',
    'source_bucket',
    'exact_sequence',
    'text',
  ],
);
writeCsv(
  path.join(OUT_DIR, `${PREFIX}_families.csv`),
  familyRows,
  [
    'checked_date',
    'family',
    'rows',
    'terminal',
    'terminal_share',
    'sites',
    'regions',
    'types',
    'symbols',
    'exact_sequences',
    'top_exact_sequence_share',
    'source_buckets',
    'top_sites',
    'top_regions',
    'top_types',
    'top_symbols',
    'top_prevs',
    'top_nexts',
    'top_exact_sequences',
    'rows_preview',
    'implication',
  ],
);
writeCsv(
  path.join(OUT_DIR, `${PREFIX}_frame_rows.csv`),
  frameRows,
  [
    'checked_date',
    'row_id',
    'object',
    'site',
    'region',
    'type',
    'shape',
    'symbol',
    'cult',
    'prev2',
    'prev',
    'sign',
    'next',
    'terminal',
    'source_status',
    'source_bucket',
    'exact_sequence',
    'text',
  ],
);
writeCsv(
  path.join(OUT_DIR, `${PREFIX}_decisions.csv`),
  decisions,
  ['checked_date', 'named_bet', 'tier_after_test', 'evidence', 'adversary', 'falsifier_or_rescue'],
);
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
