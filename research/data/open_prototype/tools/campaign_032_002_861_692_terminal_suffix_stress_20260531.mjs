import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'campaign_032_002_861_692_terminal_suffix_stress_20260531';
const RUN_DATE = '2026-05-31';
const FOCUS = '692';

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

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function norm(value, fallback = 'NA') {
  const text = String(value ?? '').trim();
  return text && text !== '-' && text !== 'None' ? text : fallback;
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

function occurrenceRows(rows) {
  const out = [];
  for (const row of rows) {
    row.signs.forEach((sign, idx) => {
      if (sign === '000') return;
      const prev = row.signs[idx - 1] ?? '<START>';
      const prev2 = row.signs[idx - 2] ?? '<START>';
      const next = row.signs[idx + 1] ?? '<END>';
      out.push({
        checked_date: RUN_DATE,
        sign,
        row_id: row.id,
        object: objectId(row),
        site: norm(row.site),
        type: norm(row.type),
        shape: norm(row.shape),
        material: norm(row.material),
        prev,
        prev2,
        next,
        next2: row.signs[idx + 2] ?? '<END>',
        terminal: idx === row.signs.length - 1 ? 'true' : 'false',
        in_002_390_frame: prev === '390' && prev2 === '002' ? 'true' : 'false',
        in_060_692_suffix: prev === '060' ? 'true' : 'false',
        exact_sequence: row.signs.join(' '),
        text: row.text,
      });
    });
  }
  return out;
}

function summarizeSign(sign, occs, rawRows) {
  const group = occs.filter((occ) => occ.sign === sign);
  const rawOccs = occurrenceRows(rawRows).filter((occ) => occ.sign === sign);
  const total = group.length;
  const terminal = group.filter((occ) => occ.terminal === 'true').length;
  const prev060 = group.filter((occ) => occ.prev === '060');
  const non060 = group.filter((occ) => occ.prev !== '060');
  const prevCounts = countBy(group, (occ) => occ.prev);
  const nextCounts = countBy(group, (occ) => occ.next);
  const exactCounts = countBy(rawOccs, (occ) => occ.exact_sequence);
  return {
    checked_date: RUN_DATE,
    sign,
    raw_occurrences: String(rawOccs.length),
    canonical_occurrences: String(total),
    terminal: String(terminal),
    terminal_share: pct(terminal, total),
    continuing: String(total - terminal),
    prev_060: String(prev060.length),
    prev_060_share: pct(prev060.length, total),
    prev_060_terminal: String(prev060.filter((occ) => occ.terminal === 'true').length),
    prev_060_terminal_share: pct(prev060.filter((occ) => occ.terminal === 'true').length, prev060.length),
    non060_occurrences: String(non060.length),
    non060_terminal: String(non060.filter((occ) => occ.terminal === 'true').length),
    non060_terminal_share: pct(non060.filter((occ) => occ.terminal === 'true').length, non060.length),
    in_002_390_frame: String(group.filter((occ) => occ.in_002_390_frame === 'true').length),
    top_prev: prevCounts[0]?.[0] ?? '',
    top_prev_count: String(prevCounts[0]?.[1] ?? 0),
    top_prev_share: pct(prevCounts[0]?.[1] ?? 0, total),
    top_next: nextCounts[0]?.[0] ?? '',
    top_next_count: String(nextCounts[0]?.[1] ?? 0),
    top_next_share: pct(nextCounts[0]?.[1] ?? 0, total),
    raw_top_exact_sequence_count: String(exactCounts[0]?.[1] ?? 0),
    raw_top_exact_sequence_share: pct(exactCounts[0]?.[1] ?? 0, rawOccs.length),
    top_prevs: top(prevCounts),
    top_nexts: top(nextCounts),
    top_raw_exact_sequences: top(exactCounts, 5),
  };
}

function rankValue(rows, sign, field, direction = 'desc') {
  const sorted = [...rows].sort((a, b) => {
    const av = Number(a[field]);
    const bv = Number(b[field]);
    return direction === 'desc' ? bv - av : av - bv;
  });
  return sorted.findIndex((row) => row.sign === sign) + 1;
}

fs.mkdirSync(OUT_DIR, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()];
const occs = occurrenceRows(canonicalRows);
const signs = [...new Set(occs.map((occ) => occ.sign))].sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
const summaries = signs.map((sign) => summarizeSign(sign, occs, rawRows));
const focusSummary = summaries.find((row) => row.sign === FOCUS);
const focusCount = Number(focusSummary.canonical_occurrences);
const lower = Math.max(20, focusCount - 20);
const upper = focusCount + 20;
const baseline = summaries
  .filter((row) => {
    const n = Number(row.canonical_occurrences);
    return row.sign !== FOCUS && n >= lower && n <= upper;
  })
  .map((row) => ({ ...row, focus_count_window: `${lower}-${upper}` }));
const baselineWindow = [focusSummary, ...baseline];
const focusOccs = occs.filter((occ) => occ.sign === FOCUS);
const prev060Occs = focusOccs.filter((occ) => occ.prev === '060');
const non060Occs = focusOccs.filter((occ) => occ.prev !== '060');
const frameOccs = focusOccs.filter((occ) => occ.in_002_390_frame === 'true');

const families = [
  {
    checked_date: RUN_DATE,
    family: '002-390-692',
    rows: String(frameOccs.length),
    terminal: String(frameOccs.filter((occ) => occ.terminal === 'true').length),
    top_rows: frameOccs.map((occ) => `${occ.object}:${occ.prev2}-${occ.prev}-${occ.sign}->${occ.next}`).join(';'),
    parse_implication:
      '`692` is strict-source local evidence for a terminal branch under `002-390`, but the family has one known row.',
  },
  {
    checked_date: RUN_DATE,
    family: '060-692',
    rows: String(prev060Occs.length),
    terminal: String(prev060Occs.filter((occ) => occ.terminal === 'true').length),
    top_rows: prev060Occs
      .slice(0, 18)
      .map((occ) => `${occ.object}:060-692->${occ.next}`)
      .join(';'),
    parse_implication:
      '`060-692` is the dominant portable terminal suffix ecology; it can explain much of global 692 terminality.',
  },
  {
    checked_date: RUN_DATE,
    family: 'non060-692',
    rows: String(non060Occs.length),
    terminal: String(non060Occs.filter((occ) => occ.terminal === 'true').length),
    top_rows: countBy(non060Occs, (occ) => `${occ.prev}-692->${occ.next}`)
      .slice(0, 10)
      .map(([key, value]) => `${key}:${value}`)
      .join(';'),
    parse_implication:
      'Even outside `060-692`, the sign remains often terminal, but much less cleanly than the dominant suffix family.',
  },
];

const decisions = [
  {
    checked_date: RUN_DATE,
    named_bet: '`692` is a hard terminal closure selector under `002-390`',
    tier_after_test:
      frameOccs.length === 1 &&
      frameOccs[0]?.terminal === 'true' &&
      Number(focusSummary.terminal_share) >= 0.65
        ? 'candidate_narrowed'
        : 'wild_shot_only',
    evidence:
      `Canonical 692 has ${focusSummary.canonical_occurrences} occurrences and ${focusSummary.terminal} are terminal; the one 002-390-692 row is terminal.`,
    adversary:
      `Dominant 060-692 accounts for ${focusSummary.prev_060}/${focusSummary.canonical_occurrences} canonical occurrences and ${focusSummary.prev_060_terminal}/${focusSummary.prev_060} are terminal, so global closure is partly a suffix-family effect.`,
    falsifier_or_rescue:
      'A source-bound 002-390-692 continuation kills the local terminal selector. A second strict 002-390-692 terminal row outside the 060 family promotes the branch rule.',
  },
  {
    checked_date: RUN_DATE,
    named_bet: '`060-692` is a portable terminal suffix and `390-692` borrows its final closure element',
    tier_after_test: Number(focusSummary.prev_060_share) >= 0.35 ? 'candidate' : 'wild_shot_only',
    evidence:
      `060 is the top predecessor of 692: ${focusSummary.prev_060}/${focusSummary.canonical_occurrences}; terminal after 060 is ${focusSummary.prev_060_terminal}/${focusSummary.prev_060}.`,
    adversary:
      '`390-692` has no visible `060`; the borrowing/stripping story is a semantic bridge, not directly observed morphology.',
    falsifier_or_rescue:
      'If 060-692 source-normalizes to a narrow copied family, this demotes. If independent sites/forms preserve 060-692 terminality, keep it as a suffix candidate.',
  },
  {
    checked_date: RUN_DATE,
    named_bet: '`692` is just an ordinary sign whose terminality is accidental',
    tier_after_test: rankValue(baselineWindow, FOCUS, 'terminal_share') <= Math.ceil(baselineWindow.length * 0.2)
      ? 'demoted'
      : 'candidate_retained',
    evidence:
      `Among ${baselineWindow.length} count-matched signs including 692, it ranks ${rankValue(baselineWindow, FOCUS, 'terminal_share')}/${baselineWindow.length} by terminal share.`,
    adversary:
      'Count matching does not control for inherited formula families, so this only attacks the lazy accidental-terminal null.',
    falsifier_or_rescue:
      'If count-matched signs routinely show the same terminal share once formula-collapsed, ordinary-sign null revives.',
  },
];

const summary = {
  checked_date: RUN_DATE,
  status: '692_terminal_suffix_stress',
  hypothesis_tested:
    '`692` is a hard terminal selector under `002-390`, but its global behavior may be driven by a portable `060-692` suffix.',
  totals: {
    raw_rows: rawRows.length,
    canonical_rows: canonicalRows.length,
    focus_raw_occurrences: Number(focusSummary.raw_occurrences),
    focus_canonical_occurrences: Number(focusSummary.canonical_occurrences),
    count_matched_baseline_signs: baseline.length,
  },
  focus_summary: focusSummary,
  baseline_ranks_among_count_matched_plus_focus: {
    by_terminal_share: `${rankValue(baselineWindow, FOCUS, 'terminal_share')}/${baselineWindow.length}`,
    by_prev_060_share: `${rankValue(baselineWindow, FOCUS, 'prev_060_share')}/${baselineWindow.length}`,
    by_top_prev_share: `${rankValue(baselineWindow, FOCUS, 'top_prev_share')}/${baselineWindow.length}`,
  },
  family_rows: families,
  decisions,
  confidence_after_test: {
    hard_terminal_692_under_002390: decisions[0].tier_after_test,
    portable_060_692_terminal_suffix: decisions[1].tier_after_test,
    accidental_terminal_null: decisions[2].tier_after_test,
  },
};

writeCsv(
  path.join(OUT_DIR, `${PREFIX}_occurrences.csv`),
  focusOccs,
  [
    'checked_date',
    'row_id',
    'object',
    'site',
    'type',
    'shape',
    'material',
    'prev2',
    'prev',
    'sign',
    'next',
    'next2',
    'terminal',
    'in_002_390_frame',
    'in_060_692_suffix',
    'exact_sequence',
    'text',
  ],
);
writeCsv(
  path.join(OUT_DIR, `${PREFIX}_sign_baselines.csv`),
  baselineWindow,
  [
    'checked_date',
    'sign',
    'raw_occurrences',
    'canonical_occurrences',
    'terminal',
    'terminal_share',
    'continuing',
    'prev_060',
    'prev_060_share',
    'prev_060_terminal',
    'prev_060_terminal_share',
    'non060_occurrences',
    'non060_terminal',
    'non060_terminal_share',
    'in_002_390_frame',
    'top_prev',
    'top_prev_count',
    'top_prev_share',
    'top_next',
    'top_next_count',
    'top_next_share',
    'raw_top_exact_sequence_count',
    'raw_top_exact_sequence_share',
    'top_prevs',
    'top_nexts',
    'top_raw_exact_sequences',
    'focus_count_window',
  ],
);
writeCsv(
  path.join(OUT_DIR, `${PREFIX}_families.csv`),
  families,
  ['checked_date', 'family', 'rows', 'terminal', 'top_rows', 'parse_implication'],
);
writeCsv(
  path.join(OUT_DIR, `${PREFIX}_decisions.csv`),
  decisions,
  ['checked_date', 'named_bet', 'tier_after_test', 'evidence', 'adversary', 'falsifier_or_rescue'],
);
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
