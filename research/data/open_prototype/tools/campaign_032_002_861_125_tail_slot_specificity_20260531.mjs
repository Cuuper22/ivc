import fs from 'node:fs';
import path from 'node:path';

// Two probes into how specific the tails after sign 125 really are. First, a terminality
// control: if 125 were a generic line-closer, governed and ungoverned 125 should differ —
// but this script shows both close within two signs most of the time, which kills the
// generic-closer model and forces tail-class scoring instead. Second, a motif audit: it
// scans data/open_prototype/lipi/metadata_filtered.csv for nine exact sign motifs
// (297-350, 350-125, 125-413, 610-125-032, 125-032, 390-125-632-032, 190-125-632-032,
// 390-125-820, 405-125-820) and, for each hit, records its context and whether it supports
// or breaks a named sub-hypothesis — for example, 297-350 counts as a pair head only when
// flanked by 002 and 125, and 125-413 must be terminal inside that template. Every 125
// occurrence is also logged with its governed head (found by walking up to four signs left
// for a 002). Writes motif rows, motif summaries, 125 occurrences, and the governed-versus-
// ungoverned terminality comparison as CSVs plus a summary JSON in reports/.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_125_tail_slot_specificity_20260531';

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

function topCounts(counts, n = 10) {
  return counts
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function findGovernedHead(tokens, signIndex) {
  for (let headIndex = signIndex - 1; headIndex >= 0 && headIndex >= signIndex - 4; headIndex -= 1) {
    if (tokens[headIndex - 1] === '002') {
      return {
        governed: true,
        headIndex,
        head: tokens[headIndex],
        prevBefore002: tokens[headIndex - 2] ?? '<START>',
      };
    }
  }
  return { governed: false, headIndex: -1, head: '', prevBefore002: '' };
}

function motifHits(rows, motif) {
  const motifTokens = motif.split('-');
  const hits = [];
  for (const row of rows) {
    for (let i = 0; i <= row.tokens.length - motifTokens.length; i += 1) {
      if (!motifTokens.every((token, offset) => row.tokens[i + offset] === token)) continue;
      hits.push({
        checked_date: '2026-05-31',
        motif,
        cisi: row.cisi || '-',
        row_id: row.id,
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        cult: row.cult,
        prev_before_motif: row.tokens[i - 1] ?? '<START>',
        next_after_motif: row.tokens[i + motifTokens.length] ?? '<END>',
        left_prefix: row.tokens.slice(0, i).join('-') || '<START>',
        right_suffix: row.tokens.slice(i + motifTokens.length).join('-') || '<END>',
        local_context: row.tokens.slice(Math.max(0, i - 3), Math.min(row.tokens.length, i + motifTokens.length + 3)).join('-'),
        model_implication: implicationForMotif(motif, row.tokens[i - 1] ?? '<START>', row.tokens[i + motifTokens.length] ?? '<END>'),
        text: row.text,
      });
    }
  }
  return hits;
}

function implicationForMotif(motif, prev, next) {
  if (motif === '297-350') {
    return prev === '002' && next === '125'
      ? 'supports_297_350_as_pair_head_selecting_125'
      : 'breaks_297_350_pair_head';
  }
  if (motif === '350-125') {
    return prev === '297' && next === '413'
      ? 'inside_297_350_title_template'
      : 'adversary_for_350_125_as_independent_title_pair';
  }
  if (motif === '125-413') return next === '<END>' ? 'terminal_tail_inside_297_350_template' : 'breaks_413_terminal_tail';
  if (motif === '610-125-032') return prev === '002' ? 'supports_610_as_governed_head' : 'breaks_610_governed_head';
  if (motif === '125-032') {
    return prev === '610' && next === '<END>'
      ? 'terminal_tail_under_610'
      : 'adversary_for_032_as_title_specific_tail';
  }
  if (motif === '390-125-632-032') return 'supports_390_title_tail';
  if (motif === '190-125-632-032') return 'supports_632_032_as_portable_cross_head_tail';
  if (motif === '390-125-820' || motif === '405-125-820') return 'supports_p086_family_125_820_tail';
  return 'background';
}

function summarizeMotif(motif, hits) {
  const uniqueLeftPrefixes = new Set(hits.map((hit) => hit.left_prefix)).size;
  const uniqueTexts = new Set(hits.map((hit) => hit.text)).size;
  return {
    checked_date: '2026-05-31',
    motif,
    hits: String(hits.length),
    sites: topCounts(countBy(hits, (hit) => hit.site)),
    types: topCounts(countBy(hits, (hit) => hit.type)),
    prev_before_motif: topCounts(countBy(hits, (hit) => hit.prev_before_motif)),
    next_after_motif: topCounts(countBy(hits, (hit) => hit.next_after_motif)),
    unique_left_prefixes: String(uniqueLeftPrefixes),
    unique_texts: String(uniqueTexts),
    confidence_effect: confidenceEffectForMotif(motif, hits),
    examples: hits.map((hit) => `${hit.cisi}:${hit.text}`).join(' | '),
  };
}

function confidenceEffectForMotif(motif, hits) {
  if (motif === '297-350') {
    const clean = hits.length === 2 && hits.every((hit) => hit.prev_before_motif === '002' && hit.next_after_motif === '125');
    return clean
      ? 'promotes_pair_specificity_but_source_visual_pending'
      : 'demotes_pair_specificity';
  }
  if (motif === '350-125') {
    const adversaries = hits.filter((hit) => hit.prev_before_motif !== '297' || hit.next_after_motif !== '413').length;
    return adversaries ? 'kills_350_125_as_independent_title_pair' : 'supports_350_125_pair';
  }
  if (motif === '125-413') return hits.every((hit) => hit.next_after_motif === '<END>') ? 'supports_413_only_inside_exact_template' : 'demotes_413_terminal_tail';
  if (motif === '610-125-032') return hits.every((hit) => hit.prev_before_motif === '002') ? 'keeps_610_candidate_rare_governed_head' : 'demotes_610_candidate';
  if (motif === '125-032') {
    const adversaries = hits.filter((hit) => hit.prev_before_motif !== '610' || hit.next_after_motif !== '<END>').length;
    return adversaries ? 'keeps_032_as_pivot_not_title_specific_tail' : 'promotes_032_terminal_tail';
  }
  if (motif === '190-125-632-032') return hits.length ? 'keeps_190_as_wild_sibling_head_for_632_032' : 'no_sibling_head_support';
  if (motif === '390-125-820' || motif === '405-125-820') return hits.length ? 'keeps_125_820_as_p086_family_candidate' : 'no_p086_tail_support';
  return 'background';
}

function summarizeBucket(label, rows) {
  const n = rows.length;
  const end0 = rows.filter((row) => row.signs_after_125 === 0).length;
  const within1 = rows.filter((row) => row.signs_after_125 <= 1).length;
  const within2 = rows.filter((row) => row.signs_after_125 <= 2).length;
  return {
    checked_date: '2026-05-31',
    bucket: label,
    n: String(n),
    terminal_immediate: String(end0),
    closes_within_1_sign: String(within1),
    closes_within_2_signs: String(within2),
    closes_within_2_share: n ? (within2 / n).toFixed(6) : '0.000000',
    top_heads: topCounts(countBy(rows, (row) => row.governed_head || '<UNGOVERNED>')),
    top_tail2_after_125: topCounts(countBy(rows, (row) => row.tail2_after_125)),
    model_implication:
      label === 'governed_125'
        ? 'governed_125_is_right_edge_heavy_but_terminality_alone_cannot_define_it'
        : 'nongoverned_125_also_closes_often_so_generic_terminal_closer_model_dies',
  };
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  tokens: signs(row.text),
}));

const motifs = [
  '297-350',
  '350-125',
  '125-413',
  '610-125-032',
  '125-032',
  '390-125-632-032',
  '190-125-632-032',
  '390-125-820',
  '405-125-820',
];

const motifRows = [];
const motifSummary = [];
for (const motif of motifs) {
  const hits = motifHits(rows, motif);
  motifRows.push(...hits);
  motifSummary.push(summarizeMotif(motif, hits));
}

const occurrence125Rows = [];
for (const row of rows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
    if (row.tokens[i] !== '125') continue;
    const governed = findGovernedHead(row.tokens, i);
    const signsAfter = row.tokens.length - i - 1;
    occurrence125Rows.push({
      checked_date: '2026-05-31',
      cisi: row.cisi || '-',
      row_id: row.id,
      site: row.site,
      type: row.type,
      symbol: row.symbol,
      cult: row.cult,
      governed_by_002: String(governed.governed),
      governed_head: governed.head,
      prev_before_002: governed.prevBefore002,
      prev_before_125: row.tokens[i - 1] ?? '<START>',
      next_after_125: row.tokens[i + 1] ?? '<END>',
      next2_after_125: row.tokens[i + 2] ?? '<END>',
      tail2_after_125: `${row.tokens[i + 1] ?? '<END>'}-${row.tokens[i + 2] ?? '<END>'}`,
      signs_after_125: signsAfter,
      closes_within_2_signs: String(signsAfter <= 2),
      model_implication:
        governed.governed && signsAfter <= 2
          ? 'governed_125_right_edge_tail'
          : !governed.governed && signsAfter <= 2
            ? 'terminality_adversary_for_generic_125_closer'
            : governed.governed
              ? 'governed_125_continuing_tail'
              : 'nongoverned_125_background',
      text: row.text,
    });
  }
}

const governed125 = occurrence125Rows.filter((row) => row.governed_by_002 === 'true');
const nongoverned125 = occurrence125Rows.filter((row) => row.governed_by_002 !== 'true');
const terminalitySummary = [summarizeBucket('governed_125', governed125), summarizeBucket('nongoverned_125', nongoverned125)];

const summary = {
  checked_date: '2026-05-31',
  status: '125_tail_slot_specificity_test',
  hypotheses_tested: [
    '`125` is a generic terminal closer',
    '`125` is a governed rank/title suffix whose value depends on head+tail',
    '`297-350` is the real head pair, not `297` or `350-125` alone',
    '`032` is a terminal/pivot tail under `610`, not a title-specific suffix everywhere',
  ],
  decisions: [
    'Kill generic `125 = terminal closer`: governed `125` closes within two signs in 16/17 cases, but nongoverned `125` also closes within two signs in 33/42 cases.',
    '`297-350` is the correct current unit for the Bala-kot/Nausharo template: both global `297-350` hits are `002-297-350-125-413`, while `350-125` has two adversarial non-297 continuations.',
    '`125-413` is terminal only inside the `297-350-125-413` template; keep `413` as template-tail candidate, not independent sign value.',
    '`610` survives as a candidate rare governed head: both `610-125-032` rows are after `002` and terminal.',
    '`032` stays a pivot/terminal-tail candidate only under `610`; the `420-125-032-820` row blocks a title-specific `032` reading.',
    '`632-032` and `820` remain the better tail bets than raw terminality: they recur across governed heads (`390/190` and `390/405`).',
  ],
  confidence_after_test: {
    '125_generic_terminal_closer': 'dead',
    '125_governed_rank_title_suffix': 'candidate',
    '297_350_pair_head_selecting_125_413': 'candidate_with_pair_specificity_strengthened',
    '610_rare_governed_head_selecting_125_032': 'candidate',
    '032_title_specific_tail': 'dead',
    '032_terminal_pivot_under_610': 'candidate',
  },
  next_prediction:
    'A new `297-350` row should either continue to select `125-413` or directly damage the pair-head bet; a new `610` row outside `002-610-125-032` directly damages the rare-head bet; a new governed `125` row should be scored by its specific tail class, not by whether it merely ends the line.',
};

writeCsv(path.join(reportsDir, `${prefix}_motif_rows.csv`), motifRows, [
  'checked_date',
  'motif',
  'cisi',
  'row_id',
  'site',
  'type',
  'symbol',
  'cult',
  'prev_before_motif',
  'next_after_motif',
  'left_prefix',
  'right_suffix',
  'local_context',
  'model_implication',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_motif_summary.csv`), motifSummary, [
  'checked_date',
  'motif',
  'hits',
  'sites',
  'types',
  'prev_before_motif',
  'next_after_motif',
  'unique_left_prefixes',
  'unique_texts',
  'confidence_effect',
  'examples',
]);

writeCsv(path.join(reportsDir, `${prefix}_125_occurrences.csv`), occurrence125Rows, [
  'checked_date',
  'cisi',
  'row_id',
  'site',
  'type',
  'symbol',
  'cult',
  'governed_by_002',
  'governed_head',
  'prev_before_002',
  'prev_before_125',
  'next_after_125',
  'next2_after_125',
  'tail2_after_125',
  'signs_after_125',
  'closes_within_2_signs',
  'model_implication',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_terminality_summary.csv`), terminalitySummary, [
  'checked_date',
  'bucket',
  'n',
  'terminal_immediate',
  'closes_within_1_sign',
  'closes_within_2_signs',
  'closes_within_2_share',
  'top_heads',
  'top_tail2_after_125',
  'model_implication',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
