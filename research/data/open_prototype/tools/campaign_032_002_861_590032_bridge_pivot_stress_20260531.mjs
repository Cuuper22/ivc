import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'campaign_032_002_861_590032_bridge_pivot_stress_20260531';
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

function logChoose(n, k) {
  if (k < 0 || k > n) return Number.NEGATIVE_INFINITY;
  let out = 0;
  for (let i = 1; i <= k; i += 1) out += Math.log(n - k + i) - Math.log(i);
  return out;
}

function hypergeomPmf(successesInDraw, population, successes, draws) {
  return Math.exp(
    logChoose(successes, successesInDraw) +
      logChoose(population - successes, draws - successesInDraw) -
      logChoose(population, draws),
  );
}

function hypergeomGreaterEqual(observed, population, successes, draws) {
  let sum = 0;
  const max = Math.min(successes, draws);
  for (let k = observed; k <= max; k += 1) sum += hypergeomPmf(k, population, successes, draws);
  return sum;
}

function sourceHint(object) {
  if (object === '-:3335.1') return 'source_blocked_private_collection_contact_sent';
  if (object === 'M-746' || object === 'M-965') return 'prior_source_visible_nonframe_formula_control';
  return 'metadata_or_unchecked_for_this_gate';
}

function pairOccurrences(rows) {
  const out = [];
  for (const row of rows) {
    row.signs.forEach((sign, idx) => {
      if (sign !== '590' || row.signs[idx + 1] !== '032') return;
      const prev = row.signs[idx - 1] ?? '<START>';
      const prev2 = row.signs[idx - 2] ?? '<START>';
      const prev3 = row.signs[idx - 3] ?? '<START>';
      const next = row.signs[idx + 2] ?? '<END>';
      const next2 = row.signs[idx + 3] ?? '<END>';
      const object = objectId(row);
      const bridgeBefore = prev3 === '032' && prev2 === '002' && prev === '390';
      const bridgeAfter = prev === '390' && next === '002';
      const governedFrame = prev2 === '002' && prev === '390';
      const formulaChunk = prev === '390';
      out.push({
        checked_date: RUN_DATE,
        row_id: row.id,
        object,
        site: norm(row.site),
        region: norm(row.region),
        type: norm(row.type),
        shape: norm(row.shape),
        material: norm(row.material),
        symbol: norm(row.symbol),
        cult: norm(row.cult),
        prev3,
        prev2,
        prev,
        pair: '590-032',
        next_after_032: next,
        next2_after_032: next2,
        terminal_after_032: next === '<END>' ? 'true' : 'false',
        is_390_590_032: formulaChunk ? 'true' : 'false',
        is_002_390_590_032: governedFrame ? 'true' : 'false',
        is_390_590_032_002: bridgeAfter ? 'true' : 'false',
        is_032_002_390_590_032: bridgeBefore ? 'true' : 'false',
        pivot_side:
          bridgeBefore && bridgeAfter
            ? 'both'
            : bridgeBefore
              ? '002_before_chunk'
              : bridgeAfter
                ? '002_after_chunk'
                : 'none',
        source_hint: sourceHint(object),
        exact_sequence: row.signs.join(' '),
        text: row.text,
      });
    });
  }
  return out;
}

function chunkOccurrences(rows) {
  const out = [];
  for (const row of rows) {
    row.signs.forEach((sign, idx) => {
      if (sign !== '390' || row.signs[idx + 1] !== '590' || row.signs[idx + 2] !== '032') return;
      const prev = row.signs[idx - 1] ?? '<START>';
      const prev2 = row.signs[idx - 2] ?? '<START>';
      const next = row.signs[idx + 3] ?? '<END>';
      const object = objectId(row);
      out.push({
        checked_date: RUN_DATE,
        row_id: row.id,
        object,
        site: norm(row.site),
        region: norm(row.region),
        type: norm(row.type),
        shape: norm(row.shape),
        symbol: norm(row.symbol),
        cult: norm(row.cult),
        prev2_before_390: prev2,
        prev_before_390: prev,
        chunk: '390-590-032',
        next_after_032: next,
        terminal_after_032: next === '<END>' ? 'true' : 'false',
        has_002_before_390: prev === '002' ? 'true' : 'false',
        has_032_002_before_390: prev2 === '032' && prev === '002' ? 'true' : 'false',
        has_002_after_032: next === '002' ? 'true' : 'false',
        pivot_side:
          prev2 === '032' && prev === '002'
            ? '002_before_chunk'
            : next === '002'
              ? '002_after_chunk'
              : 'none',
        source_hint: sourceHint(object),
        exact_sequence: row.signs.join(' '),
        text: row.text,
      });
    });
  }
  return out;
}

function familySummary(name, rows, implication) {
  const exactCounts = countBy(rows, (row) => row.exact_sequence);
  const terminal = rows.filter((row) => row.terminal_after_032 === 'true').length;
  const after002 = rows.filter((row) => row.next_after_032 === '002').length;
  const before002 = rows.filter((row) => row.is_032_002_390_590_032 === 'true' || row.has_032_002_before_390 === 'true').length;
  return {
    checked_date: RUN_DATE,
    family: name,
    rows: String(rows.length),
    terminal_after_032: String(terminal),
    terminal_share: pct(terminal, rows.length),
    next_002_after_032: String(after002),
    next_002_share: pct(after002, rows.length),
    pivot_032_002_before_chunk: String(before002),
    sites: String(new Set(rows.map((row) => row.site)).size),
    regions: String(new Set(rows.map((row) => row.region)).size),
    types: String(new Set(rows.map((row) => row.type)).size),
    exact_sequences: String(exactCounts.length),
    top_exact_sequence_share: pct(exactCounts[0]?.[1] ?? 0, rows.length),
    source_hints: top(countBy(rows, (row) => row.source_hint)),
    top_sites: top(countBy(rows, (row) => row.site)),
    top_regions: top(countBy(rows, (row) => row.region)),
    top_types: top(countBy(rows, (row) => row.type)),
    top_next_after_032: top(countBy(rows, (row) => row.next_after_032)),
    top_pivot_side: top(countBy(rows, (row) => row.pivot_side)),
    top_exact_sequences: top(exactCounts, 8),
    rows_preview: rows.map((row) => `${row.object}:${row.exact_sequence}->${row.next_after_032}`).join(';'),
    implication,
  };
}

fs.mkdirSync(OUT_DIR, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()];
const pairRows = pairOccurrences(canonicalRows);
const rawPairRows = pairOccurrences(rawRows);
const chunkRows = chunkOccurrences(canonicalRows);
const prev390PairRows = pairRows.filter((row) => row.is_390_590_032 === 'true');
const non390PairRows = pairRows.filter((row) => row.is_390_590_032 !== 'true');
const governedRows = pairRows.filter((row) => row.is_002_390_590_032 === 'true');
const pivotAfterRows = prev390PairRows.filter((row) => row.next_after_032 === '002');
const pivotBeforeRows = chunkRows.filter((row) => row.has_032_002_before_390 === 'true');
const pivotRows = [...pivotAfterRows, ...pivotBeforeRows];

const population = pairRows.length;
const successes = pairRows.filter((row) => row.next_after_032 === '002').length;
const draws = prev390PairRows.length;
const observed = pivotAfterRows.length;
const next002EnrichmentP = hypergeomGreaterEqual(observed, population, successes, draws);

const familyRows = [
  familySummary(
    'all-590-032',
    pairRows,
    'All adjacent `590-032` pairs define the background for whether `390-590-032` is special.',
  ),
  familySummary(
    '390-590-032',
    prev390PairRows,
    '`390-590-032` is the inherited formula chunk that `3335.1` may embed under `002-390`.',
  ),
  familySummary(
    'non390-590-032',
    non390PairRows,
    'Non-`390` `590-032` pairs are the control for whether `032 -> 002` is general after `590-032`.',
  ),
  familySummary(
    '390-590-032-002',
    pivotAfterRows,
    'Rows where the final `032` of the formula chunk opens a following `002` dependency.',
  ),
  familySummary(
    '032-002-390-590-032',
    pivotBeforeRows,
    '`3335.1` mirror row where `032-002` precedes the formula chunk rather than following it.',
  ),
];

const decisions = [
  {
    checked_date: RUN_DATE,
    named_bet: '`3335.1` embeds inherited `390-590-032` under `032-002` governance',
    tier_after_test: governedRows.length === 1 && governedRows[0]?.object === '-:3335.1'
      ? 'candidate_form_source_blocked'
      : 'wild_shot_only',
    evidence:
      `There is exactly one canonical 002-390-590-032 row, ${governedRows.map((row) => row.object).join(';')}; 390-590-032 has ${prev390PairRows.length} rows and ${pivotAfterRows.length}/${prev390PairRows.length} put 002 immediately after final 032.`,
    adversary:
      '`3335.1` remains source-blocked and no-object; the bridge rests on metadata plus formula ecology, not strict signband evidence.',
    falsifier_or_rescue:
      'If 3335.1 source rejects 590-032 or row order, this bridge dies. A source-bound replacement with Y-032-002-390-590-032 or 390-590-032-002-Y promotes it.',
  },
  {
    checked_date: RUN_DATE,
    named_bet: '`032` is a pivot/delimiter around the `390-590-032` formula and `002` dependency',
    tier_after_test: pivotAfterRows.length >= 3 && pivotBeforeRows.length >= 1 ? 'candidate_mixed' : 'wild_shot_only',
    evidence:
      `Among 590-032 pairs, next-002 is ${observed}/${draws} when preceded by 390 versus ${successes - observed}/${population - draws} otherwise; hypergeometric p>=observed is ${next002EnrichmentP.toFixed(6)}. 3335.1 supplies the mirror 032-002-before-chunk pattern.`,
    adversary:
      'The after-chunk pivot rows are all Lothal tags, while the mirror row is an unbound unknown-site seal; this may be register/source mixing.',
    falsifier_or_rescue:
      'A second source-bound mirror row or source-visible Lothal pivot rows promote this. If Lothal tag rows collapse as damaged/table convention only, demote.',
  },
  {
    checked_date: RUN_DATE,
    named_bet: '`590` is an ordinary single X branch like `125` or `530`',
    tier_after_test: prev390PairRows.length >= 5 && governedRows.length === 1 ? 'demoted_to_wild_shot' : 'candidate_retained',
    evidence:
      '`590` in the target frame appears only as `590-032`, and that pair is embedded in the wider `390-590-032` formula family.',
    adversary:
      'A one-row frame branch cannot prove chunk grammar; future `002-390-590-Y` rows without `032` would revive ordinary X behavior.',
    falsifier_or_rescue:
      'Any source-bound `002-390-590` branch with a non-032 tail revives ordinary branch status. Repeated `002-390-590-032` keeps the inherited-chunk parse.',
  },
  {
    checked_date: RUN_DATE,
    named_bet: 'Failure of `3335.1` kills the whole `002-390-X` branch-selector model',
    tier_after_test: 'dead',
    evidence:
      '`3335.1` only carries the inherited-formula bridge lane; the branch-selector table still has independent 125/095/692/705/530 evidence.',
    adversary:
      'If multiple source-gated branches fail together, the broader table weakens, but this single row is not load-bearing for the whole construction.',
    falsifier_or_rescue:
      'Use 3335.1 failure to demote the 590 bridge, not to erase 002-390-X wholesale.',
  },
];

const summary = {
  checked_date: RUN_DATE,
  status: '590032_bridge_pivot_stress',
  hypothesis_tested:
    '`3335.1` embeds inherited `390-590-032` under `032-002` governance; `032` may pivot between formula closure and dependency opening.',
  totals: {
    raw_rows: rawRows.length,
    canonical_rows: canonicalRows.length,
    raw_590032_pairs: rawPairRows.length,
    canonical_590032_pairs: pairRows.length,
    canonical_390590032_chunks: chunkRows.length,
    governed_002390590032_rows: governedRows.length,
    pivot_after_rows: pivotAfterRows.length,
    pivot_before_rows: pivotBeforeRows.length,
  },
  enrichment: {
    next002_after_590032_given_prev390: `${observed}/${draws}`,
    next002_after_590032_given_nonprev390: `${successes - observed}/${population - draws}`,
    hypergeom_greater_equal_p: next002EnrichmentP,
  },
  family_rows: familyRows,
  chunk_rows: chunkRows,
  decisions,
  confidence_after_test: {
    governed_3335_formula_bridge: decisions[0].tier_after_test,
    sign_032_pivot_delimiter: decisions[1].tier_after_test,
    sign_590_ordinary_branch: decisions[2].tier_after_test,
    bridge_failure_kills_whole_model: decisions[3].tier_after_test,
  },
};

writeCsv(
  path.join(OUT_DIR, `${PREFIX}_590032_occurrences.csv`),
  pairRows,
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
    'prev3',
    'prev2',
    'prev',
    'pair',
    'next_after_032',
    'next2_after_032',
    'terminal_after_032',
    'is_390_590_032',
    'is_002_390_590_032',
    'is_390_590_032_002',
    'is_032_002_390_590_032',
    'pivot_side',
    'source_hint',
    'exact_sequence',
    'text',
  ],
);
writeCsv(
  path.join(OUT_DIR, `${PREFIX}_390590032_chunks.csv`),
  chunkRows,
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
    'prev2_before_390',
    'prev_before_390',
    'chunk',
    'next_after_032',
    'terminal_after_032',
    'has_002_before_390',
    'has_032_002_before_390',
    'has_002_after_032',
    'pivot_side',
    'source_hint',
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
    'terminal_after_032',
    'terminal_share',
    'next_002_after_032',
    'next_002_share',
    'pivot_032_002_before_chunk',
    'sites',
    'regions',
    'types',
    'exact_sequences',
    'top_exact_sequence_share',
    'source_hints',
    'top_sites',
    'top_regions',
    'top_types',
    'top_next_after_032',
    'top_pivot_side',
    'top_exact_sequences',
    'rows_preview',
    'implication',
  ],
);
writeCsv(
  path.join(OUT_DIR, `${PREFIX}_decisions.csv`),
  decisions,
  ['checked_date', 'named_bet', 'tier_after_test', 'evidence', 'adversary', 'falsifier_or_rescue'],
);
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
