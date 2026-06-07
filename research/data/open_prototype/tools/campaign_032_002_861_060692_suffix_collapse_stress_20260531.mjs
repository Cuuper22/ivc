import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'campaign_032_002_861_060692_suffix_collapse_stress_20260531';
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

function entropy(counts) {
  const total = counts.reduce((sum, [, value]) => sum + value, 0);
  if (!total) return 0;
  return counts.reduce((sum, [, value]) => {
    const p = value / total;
    return sum - p * Math.log2(p);
  }, 0);
}

function pairOccurrences(rows) {
  const out = [];
  for (const row of rows) {
    row.signs.forEach((sign, idx) => {
      if (sign !== '060' || row.signs[idx + 1] !== '692') return;
      const before = row.signs.slice(0, idx);
      const after = row.signs.slice(idx + 2);
      const left3 = before.slice(-3);
      out.push({
        checked_date: RUN_DATE,
        row_id: row.id,
        object: objectId(row),
        site: norm(row.site),
        type: norm(row.type),
        shape: norm(row.shape),
        material: norm(row.material),
        prefix_before_060: before.join(' ') || '<START>',
        prev_before_060: before.at(-1) ?? '<START>',
        prev2_before_060: before.at(-2) ?? '<START>',
        left3_before_060: left3.join(' ') || '<START>',
        pair: '060-692',
        terminal_after_692: after.length ? 'false' : 'true',
        tail_after_692: after.join(' ') || '<END>',
        exact_sequence: row.signs.join(' '),
        text: row.text,
      });
    });
  }
  return out;
}

function uniqueCount(rows, field) {
  return new Set(rows.map((row) => row[field])).size;
}

function familySummary(name, rows, rawRowsForName, implication) {
  const terminal = rows.filter((row) => row.terminal_after_692 === 'true').length;
  const exactCounts = countBy(rows, (row) => row.exact_sequence);
  const rawExactCounts = countBy(rawRowsForName, (row) => row.exact_sequence);
  const topExact = exactCounts[0]?.[1] ?? 0;
  const rawTopExact = rawExactCounts[0]?.[1] ?? 0;
  return {
    checked_date: RUN_DATE,
    family: name,
    canonical_rows: String(rows.length),
    raw_rows: String(rawRowsForName.length),
    terminal: String(terminal),
    terminal_share: pct(terminal, rows.length),
    continuing: String(rows.length - terminal),
    sites: String(uniqueCount(rows, 'site')),
    types: String(uniqueCount(rows, 'type')),
    shapes: String(uniqueCount(rows, 'shape')),
    exact_sequences: String(exactCounts.length),
    top_exact_sequence_share: pct(topExact, rows.length),
    raw_top_exact_sequence_share: pct(rawTopExact, rawRowsForName.length),
    left3_entropy_bits: entropy(countBy(rows, (row) => row.left3_before_060)).toFixed(6),
    top_sites: top(countBy(rows, (row) => row.site)),
    top_types: top(countBy(rows, (row) => row.type)),
    top_shapes: top(countBy(rows, (row) => row.shape)),
    top_left3_before_060: top(countBy(rows, (row) => row.left3_before_060), 10),
    top_tail_after_692: top(countBy(rows, (row) => row.tail_after_692), 10),
    top_exact_sequences: top(exactCounts, 6),
    raw_top_exact_sequences: top(rawExactCounts, 6),
    implication,
  };
}

fs.mkdirSync(OUT_DIR, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()];
const rawPairs = pairOccurrences(rawRows);
const pairs = pairOccurrences(canonicalRows);

const terminalPairs = pairs.filter((row) => row.terminal_after_692 === 'true');
const continuingPairs = pairs.filter((row) => row.terminal_after_692 !== 'true');
const rawTerminalPairs = rawPairs.filter((row) => row.terminal_after_692 === 'true');
const rawContinuingPairs = rawPairs.filter((row) => row.terminal_after_692 !== 'true');
const allSummary = familySummary(
  '060-692-all',
  pairs,
  rawPairs,
  '`060-692` survives exact-sequence collapse if this family has broad sites/types/left contexts and no dominant exact text.',
);
const familyRows = [
  allSummary,
  familySummary(
    '060-692-terminal',
    terminalPairs,
    rawTerminalPairs,
    'Terminal `060-692` is the suffix-candidate core.',
  ),
  familySummary(
    '060-692-continuing-exceptions',
    continuingPairs,
    rawContinuingPairs,
    'Continuing `060-692-Y` rows are the falsifier set against absolute terminality.',
  ),
];

const continuingExceptionRows = continuingPairs.map((row) => ({
  ...row,
  exception_read:
    row.tail_after_692 === '740'
      ? 'possible panel/line break or duplicated side continuation; still a real exception until source-resolved'
      : 'true continuation after 692',
}));

const decisions = [
  {
    checked_date: RUN_DATE,
    named_bet: '`060-692` is a portable terminal suffix, not one copied formula',
    tier_after_test:
      Number(allSummary.canonical_rows) >= 20 &&
      Number(allSummary.sites) >= 4 &&
      Number(allSummary.types) >= 4 &&
      Number(allSummary.top_exact_sequence_share) <= 0.15 &&
      Number(allSummary.terminal_share) >= 0.75
        ? 'candidate_strengthened_not_promoted'
        : 'candidate_mixed',
    evidence:
      `Canonical 060-692 has ${allSummary.canonical_rows} rows across ${allSummary.sites} sites, ${allSummary.types} types, ${allSummary.shapes} shapes, and ${allSummary.exact_sequences} exact sequences; top canonical exact-sequence share is ${allSummary.top_exact_sequence_share}; terminal share is ${allSummary.terminal_share}.`,
    adversary:
      'This is still metadata/canonical collapse, not source-normalized signband collapse; some rows may be duplicated impressions, damaged continuations, or line-break artifacts.',
    falsifier_or_rescue:
      'If source-normalized images collapse the rows to a few copied/duplicate families, demote. If source-visible examples across Harappa, Mohenjo-daro, Banawali/Chanhu-daro/Nausharo preserve terminal 060-692, promote to promoted candidate suffix.',
  },
  {
    checked_date: RUN_DATE,
    named_bet: '`060-692` is always terminal',
    tier_after_test: continuingPairs.length ? 'dead_as_absolute_rule' : 'candidate',
    evidence:
      `${continuingPairs.length}/${pairs.length} canonical 060-692 rows continue after 692; tails include ${top(countBy(continuingPairs, (row) => row.tail_after_692), 8)}.`,
    adversary:
      'Some continuations may be side joins, uncertain damaged rows, or multi-line artifacts; this kills absoluteness, not the suffix tendency.',
    falsifier_or_rescue:
      'If all continuing exceptions are source-rejected as joins/damage, absolute terminality can be reconsidered. Until then, the parser must allow exceptions.',
  },
  {
    checked_date: RUN_DATE,
    named_bet: '`390-692` is a stripped/borrowed use of the `060-692` closure element',
    tier_after_test: 'wild_bridge_retained',
    evidence:
      '`060-692` survives simple copy collapse as a terminal suffix candidate, and M-70 gives strict local `002-390-692` terminal behavior without visible `060`.',
    adversary:
      'There is no observed 060 deletion or alternation path. `390-692` could be an independent use of the same final sign or a catalog-level accident.',
    falsifier_or_rescue:
      'A row showing 002-390-060-692, or paired formula variants with and without 060, would promote the bridge. A continuing source-bound 002-390-692-Y would kill it.',
  },
];

const summary = {
  checked_date: RUN_DATE,
  status: '060692_suffix_collapse_stress',
  hypothesis_tested:
    '`060-692` is a portable terminal suffix candidate rather than one copied formula; `390-692` may borrow the closure element.',
  totals: {
    raw_rows: rawRows.length,
    canonical_rows: canonicalRows.length,
    raw_060692_occurrences: rawPairs.length,
    canonical_060692_occurrences: pairs.length,
    continuing_exception_rows: continuingPairs.length,
  },
  family_rows: familyRows,
  continuing_exception_rows: continuingExceptionRows,
  decisions,
  confidence_after_test: {
    portable_060692_terminal_suffix: decisions[0].tier_after_test,
    absolute_060692_terminality: decisions[1].tier_after_test,
    stripped_390692_bridge: decisions[2].tier_after_test,
  },
};

writeCsv(
  path.join(OUT_DIR, `${PREFIX}_occurrences.csv`),
  pairs,
  [
    'checked_date',
    'row_id',
    'object',
    'site',
    'type',
    'shape',
    'material',
    'prefix_before_060',
    'prev2_before_060',
    'prev_before_060',
    'left3_before_060',
    'pair',
    'terminal_after_692',
    'tail_after_692',
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
    'canonical_rows',
    'raw_rows',
    'terminal',
    'terminal_share',
    'continuing',
    'sites',
    'types',
    'shapes',
    'exact_sequences',
    'top_exact_sequence_share',
    'raw_top_exact_sequence_share',
    'left3_entropy_bits',
    'top_sites',
    'top_types',
    'top_shapes',
    'top_left3_before_060',
    'top_tail_after_692',
    'top_exact_sequences',
    'raw_top_exact_sequences',
    'implication',
  ],
);
writeCsv(
  path.join(OUT_DIR, `${PREFIX}_continuing_exceptions.csv`),
  continuingExceptionRows,
  [
    'checked_date',
    'row_id',
    'object',
    'site',
    'type',
    'shape',
    'prefix_before_060',
    'left3_before_060',
    'pair',
    'tail_after_692',
    'exception_read',
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
