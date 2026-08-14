import fs from 'node:fs';
import path from 'node:path';

// A full ecological workup of sign 095 across the whole corpus, testing whether it behaves
// like a governed administrative/status marker rather than a personal name or title. It
// reads data/open_prototype/lipi/metadata_filtered.csv, indexes every sign occurrence with
// neighbors and object context, and profiles 095 on several axes: how often it follows the
// status stems 390/520/595, how much of it sits on tablets/pots/tags/rods/implements rather
// than square or rectangular seals (where names would live), and how the clipped terminal
// 002-390-095 frame contrasts with the longer 520-095 and 595-095 trails that usually
// continue. To keep the comparison honest, 095 is ranked against every sign of similar
// frequency (within +/-10 canonical occurrences), and raw-versus-canonical counts expose
// copy pressure from repeated Mohenjo-daro tablet strings. Three verdicts: status-marker is
// candidate_mixed, the name/title reading is demoted, and "002-390-095 is a clipped status
// trail" stays a wild shot. Writes occurrences, sign baselines, family rows, and decisions
// as CSVs plus a summary JSON in reports/.

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'campaign_032_002_861_095_status_ecology_stress_20260531';
const RUN_DATE = '2026-05-31';
const FOCUS = '095';
const STATUS_STEMS = new Set(['390', '520', '595']);

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

function entropy(counts) {
  const total = counts.reduce((sum, [, value]) => sum + value, 0);
  if (!total) return 0;
  return counts.reduce((sum, [, value]) => {
    const p = value / total;
    return sum - p * Math.log2(p);
  }, 0);
}

function isSquareOrRectSeal(row) {
  const type = norm(row.type);
  const shape = norm(row.shape).toLowerCase();
  return type.startsWith('SEAL:') && (shape === 'square' || shape === 'rectangular');
}

function isTabletPotTagRodImpl(row) {
  const type = norm(row.type);
  return /^(TAB|POT|TAG|ROD|IMPL)/.test(type);
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
        square_or_rect_seal: isSquareOrRectSeal(row) ? 'true' : 'false',
        tablet_pot_tag_rod_impl: isTabletPotTagRodImpl(row) ? 'true' : 'false',
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
  const prevCounts = countBy(group, (occ) => occ.prev);
  const nextCounts = countBy(group, (occ) => occ.next);
  const exactCounts = countBy(rawOccs, (occ) => occ.exact_sequence);
  const total = group.length;
  const topPrevCount = prevCounts[0]?.[1] ?? 0;
  const topExactRawCount = exactCounts[0]?.[1] ?? 0;
  const statusStemCount = group.filter((occ) => STATUS_STEMS.has(occ.prev)).length;
  const prev520or595Count = group.filter((occ) => occ.prev === '520' || occ.prev === '595').length;
  return {
    checked_date: RUN_DATE,
    sign,
    raw_occurrences: String(rawOccs.length),
    canonical_occurrences: String(total),
    terminal: String(group.filter((occ) => occ.terminal === 'true').length),
    terminal_share: pct(group.filter((occ) => occ.terminal === 'true').length, total),
    continuing: String(group.filter((occ) => occ.terminal !== 'true').length),
    square_or_rect_seal: String(group.filter((occ) => occ.square_or_rect_seal === 'true').length),
    outside_square_or_rect_seal: String(group.filter((occ) => occ.square_or_rect_seal !== 'true').length),
    outside_square_or_rect_seal_share: pct(group.filter((occ) => occ.square_or_rect_seal !== 'true').length, total),
    tablet_pot_tag_rod_impl: String(group.filter((occ) => occ.tablet_pot_tag_rod_impl === 'true').length),
    tablet_pot_tag_rod_impl_share: pct(group.filter((occ) => occ.tablet_pot_tag_rod_impl === 'true').length, total),
    prev_390: String(group.filter((occ) => occ.prev === '390').length),
    prev_520: String(group.filter((occ) => occ.prev === '520').length),
    prev_595: String(group.filter((occ) => occ.prev === '595').length),
    prev_status_stems_390_520_595: String(statusStemCount),
    prev_status_stems_share: pct(statusStemCount, total),
    prev_520_or_595_share: pct(prev520or595Count, total),
    in_002_390_frame: String(group.filter((occ) => occ.in_002_390_frame === 'true').length),
    nonframe_prev390: String(group.filter((occ) => occ.prev === '390' && occ.in_002_390_frame !== 'true').length),
    top_prev: prevCounts[0]?.[0] ?? '',
    top_prev_count: String(topPrevCount),
    top_prev_share: pct(topPrevCount, total),
    prev_entropy_bits: entropy(prevCounts).toFixed(6),
    top_next: nextCounts[0]?.[0] ?? '',
    top_next_count: String(nextCounts[0]?.[1] ?? 0),
    top_next_share: pct(nextCounts[0]?.[1] ?? 0, total),
    next_entropy_bits: entropy(nextCounts).toFixed(6),
    raw_top_exact_sequence_count: String(topExactRawCount),
    raw_top_exact_sequence_share: pct(topExactRawCount, rawOccs.length),
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
const rawOccs = occurrenceRows(rawRows);
const signs = [...new Set(occs.map((occ) => occ.sign))].sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
const summaries = signs.map((sign) => summarizeSign(sign, occs, rawRows));
const focusSummary = summaries.find((row) => row.sign === FOCUS);
const focusCount = Number(focusSummary.canonical_occurrences);
const baseline = summaries
  .filter((row) => {
    const n = Number(row.canonical_occurrences);
    return row.sign !== FOCUS && n >= Math.max(10, focusCount - 10) && n <= focusCount + 10;
  })
  .map((row) => ({
    ...row,
    focus_count_window: `${Math.max(10, focusCount - 10)}-${focusCount + 10}`,
  }));

const focusOccs = occs.filter((occ) => occ.sign === FOCUS);
const focusRawOccs = rawOccs.filter((occ) => occ.sign === FOCUS);
const families = [
  {
    checked_date: RUN_DATE,
    family: '002-390-095',
    rows: String(focusOccs.filter((occ) => occ.in_002_390_frame === 'true').length),
    terminal: String(focusOccs.filter((occ) => occ.in_002_390_frame === 'true' && occ.terminal === 'true').length),
    top_rows: focusOccs
      .filter((occ) => occ.in_002_390_frame === 'true')
      .map((occ) => `${occ.object}:${occ.prev2}-${occ.prev}-${occ.sign}->${occ.next}`)
      .join(';'),
    parse_implication:
      '`095` can surface as a bare terminal status/result selector when immediately governed by `002-390`.',
  },
  {
    checked_date: RUN_DATE,
    family: '520-095',
    rows: String(focusOccs.filter((occ) => occ.prev === '520').length),
    terminal: String(focusOccs.filter((occ) => occ.prev === '520' && occ.terminal === 'true').length),
    top_rows: focusOccs
      .filter((occ) => occ.prev === '520')
      .map((occ) => `${occ.object}:520-095->${occ.next}`)
      .join(';'),
    parse_implication:
      '`520-095` is the dominant non-frame ecology and usually opens a longer tablet/tag trail rather than closing.',
  },
  {
    checked_date: RUN_DATE,
    family: '595-095',
    rows: String(focusOccs.filter((occ) => occ.prev === '595').length),
    terminal: String(focusOccs.filter((occ) => occ.prev === '595' && occ.terminal === 'true').length),
    top_rows: focusOccs
      .filter((occ) => occ.prev === '595')
      .map((occ) => `${occ.object}:595-095->${occ.next}`)
      .join(';'),
    parse_implication:
      '`595-095` is a secondary administrative-looking ecology, mostly on Mohenjo-daro tablet rows.',
  },
  {
    checked_date: RUN_DATE,
    family: 'raw-copy-pressure',
    rows: String(focusRawOccs.length),
    terminal: String(focusRawOccs.filter((occ) => occ.terminal === 'true').length),
    top_rows: countBy(focusRawOccs, (occ) => occ.exact_sequence)
      .slice(0, 5)
      .map(([key, value]) => `${key}:${value}`)
      .join(';'),
    parse_implication:
      'The status-marker bet must be copy-family aware because repeated Mohenjo-daro tablet strings inflate raw `520-095` counts.',
  },
];

const baselineWindow = [focusSummary, ...baseline].sort(
  (a, b) => Number(b.prev_status_stems_share) - Number(a.prev_status_stems_share) || a.sign.localeCompare(b.sign, undefined, { numeric: true }),
);
const decisions = [
  {
    checked_date: RUN_DATE,
    named_bet: '`095` is a governed administrative/status marker, not merely a terminal sign',
    tier_after_test:
      Number(focusSummary.prev_status_stems_share) >= 0.45 &&
      Number(focusSummary.tablet_pot_tag_rod_impl_share) >= 0.45 &&
      Number(focusSummary.in_002_390_frame) >= 2
        ? 'candidate_mixed'
        : 'wild_shot_only',
    evidence:
      `Canonical 095 has ${focusSummary.canonical_occurrences} occurrences; ${focusSummary.prev_status_stems_390_520_595}/${focusSummary.canonical_occurrences} follow 390/520/595, ${focusSummary.tablet_pot_tag_rod_impl}/${focusSummary.canonical_occurrences} are on tablet/pot/tag/rod/implement rows, and both 002-390-095 rows are terminal.`,
    adversary:
      'Raw copy pressure is real: repeated Mohenjo-daro tablet C strings inflate the 520-095 ecology, and the H-1993 half of 002-390-095 is still route-pressure only.',
    falsifier_or_rescue:
      'A source-bound 002-390-095 continuation with a name-like tail demotes terminal-status wording; source-preserved 520/595 diversity plus a strict H-1993 terminal side promotes status-marker semantics.',
  },
  {
    checked_date: RUN_DATE,
    named_bet: '`095` in 002-390-095 is a personal-name/title branch like 125',
    tier_after_test: Number(focusSummary.tablet_pot_tag_rod_impl_share) >= 0.45 ? 'demoted_to_wild_shot' : 'candidate_retained',
    evidence:
      `095 is not concentrated in name-like square/rectangular seal environments: ${focusSummary.outside_square_or_rect_seal}/${focusSummary.canonical_occurrences} canonical occurrences are outside square/rectangular seal rows, and its dominant non-frame ecology is 520/595 before 095.`,
    adversary:
      'M-71 is a square seal with a 002-390-095 terminal branch, so a title reading is not impossible; the evidence only makes it less natural than status/result.',
    falsifier_or_rescue:
      'A cluster of source-visible 002-390-095 seal rows with varied personal-tail continuations would revive a name/title analysis.',
  },
  {
    checked_date: RUN_DATE,
    named_bet: '`002-390-095` is the clipped terminal version of the longer 520/595-095 status trails',
    tier_after_test: 'wild_shot_retained',
    evidence:
      'The local frame strips 095 to terminal position, while the main non-frame stems 520 and 595 usually continue through 033/585/760/717-style trails.',
    adversary:
      'The governing stems are different; 390 may be selecting a homographic branch sign with a different value rather than clipping the same formula class.',
    falsifier_or_rescue:
      'A non-frame 390-095 row with an admin/status trail, or a sourced H-1993 terminal side plus comparable Sktd-1 125 continuation, would make this sharper.',
  },
];

const summary = {
  checked_date: RUN_DATE,
  status: '095_status_ecology_stress',
  hypothesis_tested:
    '`095` is a governed administrative/status marker: extended after 520/595, clipped terminal after 002-390.',
  totals: {
    raw_rows: rawRows.length,
    canonical_rows: canonicalRows.length,
    focus_raw_occurrences: Number(focusSummary.raw_occurrences),
    focus_canonical_occurrences: Number(focusSummary.canonical_occurrences),
    count_matched_baseline_signs: baseline.length,
  },
  focus_summary: focusSummary,
  baseline_ranks_among_count_matched_plus_focus: {
    by_prev_status_stems_share: `${rankValue(baselineWindow, FOCUS, 'prev_status_stems_share')}/${baselineWindow.length}`,
    by_tablet_pot_tag_rod_impl_share: `${rankValue(baselineWindow, FOCUS, 'tablet_pot_tag_rod_impl_share')}/${baselineWindow.length}`,
    by_outside_square_or_rect_seal_share: `${rankValue(baselineWindow, FOCUS, 'outside_square_or_rect_seal_share')}/${baselineWindow.length}`,
    by_top_prev_share: `${rankValue(baselineWindow, FOCUS, 'top_prev_share')}/${baselineWindow.length}`,
  },
  family_rows: families,
  decisions,
  confidence_after_test: {
    governed_095_status_marker: decisions[0].tier_after_test,
    name_or_title_095_branch: decisions[1].tier_after_test,
    clipped_status_trail_under_002390: decisions[2].tier_after_test,
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
    'square_or_rect_seal',
    'tablet_pot_tag_rod_impl',
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
    'square_or_rect_seal',
    'outside_square_or_rect_seal',
    'outside_square_or_rect_seal_share',
    'tablet_pot_tag_rod_impl',
    'tablet_pot_tag_rod_impl_share',
    'prev_390',
    'prev_520',
    'prev_595',
    'prev_status_stems_390_520_595',
    'prev_status_stems_share',
    'prev_520_or_595_share',
    'in_002_390_frame',
    'nonframe_prev390',
    'top_prev',
    'top_prev_count',
    'top_prev_share',
    'prev_entropy_bits',
    'top_next',
    'top_next_count',
    'top_next_share',
    'next_entropy_bits',
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
