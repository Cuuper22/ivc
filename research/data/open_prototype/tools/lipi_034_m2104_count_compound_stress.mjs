import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const corpusPath = path.join(base, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');

const contextsOut = path.join(reportsDir, 'lipi_034_m2104_count_compound_contexts.csv');
const framesOut = path.join(reportsDir, 'lipi_034_m2104_count_compound_frames.csv');
const testsOut = path.join(reportsDir, 'lipi_034_m2104_count_compound_tests.csv');
const summaryOut = path.join(reportsDir, 'lipi_034_m2104_count_compound_summary.json');

const checkedDate = '2026-05-25';

function parseCsv(text) {
  const rows = [];
  let row = [];
  let value = '';
  let inQuotes = false;

  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (inQuotes) {
      if (ch === '"' && next === '"') {
        value += '"';
        i += 1;
      } else if (ch === '"') {
        inQuotes = false;
      } else {
        value += ch;
      }
    } else if (ch === '"') {
      inQuotes = true;
    } else if (ch === ',') {
      row.push(value);
      value = '';
    } else if (ch === '\n') {
      row.push(value);
      if (row.length > 1 || row[0] !== '') rows.push(row);
      row = [];
      value = '';
    } else if (ch !== '\r') {
      value += ch;
    }
  }
  if (value.length > 0 || row.length > 0) {
    row.push(value);
    rows.push(row);
  }
  return rows;
}

function csvObjects(text) {
  const [header, ...body] = parseCsv(text);
  return body.map((row) =>
    Object.fromEntries(header.map((key, index) => [key, row[index] ?? ''])),
  );
}

function toCsv(rows) {
  if (rows.length === 0) return '';
  const header = Object.keys(rows[0]);
  const quote = (value) => `"${String(value ?? '').replaceAll('"', '""')}"`;
  return `${[
    header.map(quote).join(','),
    ...rows.map((row) => header.map((key) => quote(row[key])).join(',')),
  ].join('\n')}\n`;
}

function tokens(text) {
  return text.match(/\d{3}/g) ?? [];
}

function countBy(rows, keyFn) {
  const counts = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return Object.fromEntries(
    [...counts].sort((a, b) => String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true })),
  );
}

function hasSubsequence(rowTokens, subsequence) {
  return rowTokens.some((_, index) => subsequence.every((token, offset) => rowTokens[index + offset] === token));
}

function logChoose(n, k) {
  if (k < 0 || k > n) return Number.NEGATIVE_INFINITY;
  let out = 0;
  for (let i = 1; i <= k; i += 1) {
    out += Math.log(n - k + i) - Math.log(i);
  }
  return out;
}

function hypergeom(a, row1, col1, total) {
  return Math.exp(logChoose(col1, a) + logChoose(total - col1, row1 - a) - logChoose(total, row1));
}

function fisherRightTail(a, b, c, d) {
  const row1 = a + b;
  const row2 = c + d;
  const col1 = a + c;
  const total = row1 + row2;
  const maxA = Math.min(row1, col1);
  let p = 0;
  for (let x = a; x <= maxA; x += 1) p += hypergeom(x, row1, col1, total);
  return p;
}

function cleanObject(row) {
  return {
    id: row.id,
    cisi: row.cisi,
    site: row.site,
    region: row.region,
    type: row.type,
    material: row.material,
    preservation: row.preservation,
    condition: row.condition,
    complete: row.complete,
    direction: row['dir.'],
    class: row.class,
    signs: row.signs,
    text: row.text,
  };
}

const rows = csvObjects(fs.readFileSync(corpusPath, 'utf8')).map((row) => ({
  ...row,
  _tokens: tokens(row.text),
}));

const candidatePairs = [
  ['700', '034'],
  ['034', '700'],
  ['700', '004'],
  ['004', '700'],
];

const contextRows = [];
for (const row of rows) {
  for (let index = 0; index < row._tokens.length - 1; index += 1) {
    const pair = [row._tokens[index], row._tokens[index + 1]];
    if (!candidatePairs.some(([a, b]) => pair[0] === a && pair[1] === b)) continue;
    const prev = row._tokens[index - 1] ?? 'BOS';
    const next = row._tokens[index + 2] ?? 'EOS';
    const variant =
      pair[0] === '700' && pair[1] === '034'
        ? '700-034'
        : pair[0] === '034' && pair[1] === '700'
          ? '034-700'
          : pair[0] === '700' && pair[1] === '004'
            ? '700-004'
            : '004-700';
    contextRows.push({
      checked_date: checkedDate,
      variant,
      order: pair.join('-'),
      prev_token: prev,
      next_token: next,
      immediate_frame: `${prev}|${pair[0]}-${pair[1]}|${next}`,
      variant_wildcard_frame: `${prev}|700-X|${next}`,
      exact_sequence_frame: row._tokens
        .map((token, tokenIndex) => (tokenIndex === index + 1 && pair[0] === '700' ? 'X' : token))
        .join('-'),
      contains_097_700_variant:
        index > 0 && row._tokens[index - 1] === '097' && pair[0] === '700' && ['034', '004'].includes(pair[1])
          ? '1'
          : '0',
      parpola_named_or_target: ['M-2104', 'M-478', 'M-480', 'M-1425'].includes(row.cisi) ? '1' : '0',
      local_extra_same_parallel: row.cisi === 'M-479' ? '1' : '0',
      ...cleanObject(row),
    });
  }
}

function rowsWithSubsequence(sequence) {
  return rows.filter((row) => hasSubsequence(row._tokens, sequence));
}

const exactSubsequences = [
  ['097', '700', '034'],
  ['097', '700', '004'],
  ['151', '097', '700', '034'],
  ['400', '097', '700', '004'],
  ['700', '034'],
  ['700', '004'],
  ['034', '700'],
  ['004', '700'],
];

const frameRows = [];
for (const sequence of exactSubsequences) {
  const hits = rowsWithSubsequence(sequence);
  frameRows.push({
    checked_date: checkedDate,
    frame_type: 'exact_subsequence',
    frame: sequence.join('-'),
    variant: sequence.includes('034') ? '034' : sequence.includes('004') ? '004' : '',
    row_count: hits.length,
    unique_cisi_count: new Set(hits.map((row) => row.cisi)).size,
    unique_exact_text_count: new Set(hits.map((row) => row.text)).size,
    sites: JSON.stringify(countBy(hits, (row) => row.site)),
    types: JSON.stringify(countBy(hits, (row) => row.type)),
    rows: hits.map((row) => `${row.cisi || '-'}:${row.id}:${row.text}`).join(';'),
  });
}

const wildcardFrames = new Map();
for (const row of contextRows.filter((row) => row.order.startsWith('700-'))) {
  const current = wildcardFrames.get(row.variant_wildcard_frame) ?? [];
  current.push(row);
  wildcardFrames.set(row.variant_wildcard_frame, current);
}

for (const [frame, hits] of wildcardFrames) {
  const variants = countBy(hits, (row) => row.variant);
  frameRows.push({
    checked_date: checkedDate,
    frame_type: 'immediate_wildcard_700_X',
    frame,
    variant: Object.keys(variants).join(';'),
    row_count: hits.length,
    unique_cisi_count: new Set(hits.map((row) => row.cisi)).size,
    unique_exact_text_count: new Set(hits.map((row) => row.text)).size,
    sites: JSON.stringify(countBy(hits, (row) => row.site)),
    types: JSON.stringify(countBy(hits, (row) => row.type)),
    rows: hits.map((row) => `${row.cisi || '-'}:${row.id}:${row.text}`).join(';'),
  });
}

const exactFrames = new Map();
for (const row of contextRows.filter((row) => row.order.startsWith('700-'))) {
  const current = exactFrames.get(row.exact_sequence_frame) ?? [];
  current.push(row);
  exactFrames.set(row.exact_sequence_frame, current);
}

for (const [frame, hits] of exactFrames) {
  const variants = countBy(hits, (row) => row.variant);
  if (Object.keys(variants).length < 2 && hits.length < 2) continue;
  frameRows.push({
    checked_date: checkedDate,
    frame_type: 'exact_sequence_wildcard_after_700',
    frame,
    variant: Object.keys(variants).join(';'),
    row_count: hits.length,
    unique_cisi_count: new Set(hits.map((row) => row.cisi)).size,
    unique_exact_text_count: new Set(hits.map((row) => row.text)).size,
    sites: JSON.stringify(countBy(hits, (row) => row.site)),
    types: JSON.stringify(countBy(hits, (row) => row.type)),
    rows: hits.map((row) => `${row.cisi || '-'}:${row.id}:${row.text}`).join(';'),
  });
}

const forward034 = contextRows.filter((row) => row.variant === '700-034');
const forward004 = contextRows.filter((row) => row.variant === '700-004');
const reversed034 = contextRows.filter((row) => row.variant === '034-700');
const reversed004 = contextRows.filter((row) => row.variant === '004-700');
const prev097034 = forward034.filter((row) => row.prev_token === '097');
const prev097004 = forward004.filter((row) => row.prev_token === '097');
const mSite034 = forward034.filter((row) => row.site === 'Mohenjo-daro');
const mSite004 = forward004.filter((row) => row.site === 'Mohenjo-daro');
const parpolaSet = rows.filter((row) => ['M-2104', 'M-478', 'M-480', 'M-1425'].includes(row.cisi));
const parpolaPlusLocalM479 = rows.filter((row) => ['M-2104', 'M-478', 'M-479', 'M-480', 'M-1425'].includes(row.cisi));

const tests = [
  {
    checked_date: checkedDate,
    test: 'adjacent_pair_counts',
    result: `700-034=${forward034.length};034-700=${reversed034.length};700-004=${forward004.length};004-700=${reversed004.length}`,
    support_for_count_hypothesis: 'weak',
    adversarial_read: '700-034 is mostly a Harappa short-mark/tablet pattern, while 700-004 is rare. This blocks treating the contrast as a broad count system without source-normalized subsetting.',
    accepted_mapping: '0',
    accepted_translation: '0',
  },
  {
    checked_date: checkedDate,
    test: '097_left_context_enrichment',
    result: `prev097 among 700-004=${prev097004.length}/${forward004.length}; prev097 among 700-034=${prev097034.length}/${forward034.length}; right-tail Fisher p=${fisherRightTail(prev097004.length, forward004.length - prev097004.length, prev097034.length, forward034.length - prev097034.length).toPrecision(6)}`,
    support_for_count_hypothesis: 'moderate_for_narrow_frame',
    adversarial_read: 'The 097-700-X frame is sharply enriched for 004, but the 034 side is a singleton M-2104 and the 004 side collapses to one exact sequence family.',
    accepted_mapping: '0',
    accepted_translation: '0',
  },
  {
    checked_date: checkedDate,
    test: 'mohenjo_daro_forward_pair_scope',
    result: `Mohenjo-daro 700-034=${mSite034.length}; Mohenjo-daro 700-004=${mSite004.length}; rows=${[...mSite034, ...mSite004].map((row) => `${row.cisi}:${row.text}`).join(';')}`,
    support_for_count_hypothesis: 'moderate_for_mohenjo_scope',
    adversarial_read: 'Inside Mohenjo-daro, all 700-004 rows are the same local text and M-2104 is the only 700-034 row. This is a good source-targeted contrast, not independent proof.',
    accepted_mapping: '0',
    accepted_translation: '0',
  },
  {
    checked_date: checkedDate,
    test: 'parpola_named_set',
    result: parpolaSet.map((row) => `${row.cisi}:${row.text}`).join(';'),
    support_for_count_hypothesis: 'strongest_current_support',
    adversarial_read: 'The named set preserves the exact local alignment Parpola predicts, but M-2104 still lacks raw CISI 3.1 confirmation and the target object has a five-character/four-token warning in the public Marshall route.',
    accepted_mapping: '0',
    accepted_translation: '0',
  },
  {
    checked_date: checkedDate,
    test: 'local_extra_m479',
    result: parpolaPlusLocalM479.map((row) => `${row.cisi}:${row.text}`).join(';'),
    support_for_count_hypothesis: 'supportive_but_duplicate_family_heavy',
    adversarial_read: 'Local M-479 silently joins the same +400-097-700-004+ family. It increases corpus coverage but also shows the 004 evidence is an exact repeated formula, not four independent substitutions.',
    accepted_mapping: '0',
    accepted_translation: '0',
  },
  {
    checked_date: checkedDate,
    test: 'exact_sequence_wildcard_after_700',
    result: 'The bare short-mark frame +700-X+ contains both variants, dominated by Harappa tablet rows. No Parpola-like multi-token full-sequence frame contains both 700-034 and 700-004. The closest non-bare shared frame is suffix 097-700-X, with different first signs 151 versus 400.',
    support_for_count_hypothesis: 'limited',
    adversarial_read: 'A true M-2104-style minimal-pair count substitution is not present in the local corpus. The broad +700-X+ shared frame is a different Harappa short-mark problem, so the count claim rests on Parpola prose plus named Mohenjo-daro parallels.',
    accepted_mapping: '0',
    accepted_translation: '0',
  },
];

fs.writeFileSync(contextsOut, toCsv(contextRows));
fs.writeFileSync(framesOut, toCsv(frameRows));
fs.writeFileSync(testsOut, toCsv(tests));

const summary = {
  checked_date: checkedDate,
  artifact: 'lipi_034_m2104_count_compound_stress',
  question: 'Does the local corpus support or kill the M-2104 hypothesis that 700-034 corresponds to Parpola UIII while 700-004 corresponds to UIIII?',
  core_result: {
    forward_700_034_rows: forward034.length,
    reversed_034_700_rows: reversed034.length,
    forward_700_004_rows: forward004.length,
    reversed_004_700_rows: reversed004.length,
    exact_097_700_034_rows: rowsWithSubsequence(['097', '700', '034']).map((row) => cleanObject(row)),
    exact_097_700_004_rows: rowsWithSubsequence(['097', '700', '004']).map((row) => cleanObject(row)),
    parpola_named_rows: parpolaSet.map((row) => cleanObject(row)),
    local_extra_same_004_family: rows.filter((row) => row.cisi === 'M-479').map((row) => cleanObject(row)),
  },
  statistical_pressure: {
    prev097_among_700_004: `${prev097004.length}/${forward004.length}`,
    prev097_among_700_034: `${prev097034.length}/${forward034.length}`,
    fisher_right_tail_p_for_097_enrichment_in_700_004: Number(
      fisherRightTail(prev097004.length, forward004.length - prev097004.length, prev097034.length, forward034.length - prev097034.length).toPrecision(8),
    ),
  },
  adjudication: {
    survives_as_narrow_source_target: true,
    upgraded_to_mapping: false,
    upgraded_to_count_value: false,
    upgraded_to_translation: false,
    strongest_support: 'The exact suffix frame 097-700-X has M-2104 as the only 034 row and four 004 rows, all Mohenjo-daro, matching Parpola 2019 prose and named parallels; M-479 adds a local unmentioned row in the same +400-097-700-004+ family.',
    strongest_downgrade: 'The only exact full-sequence wildcard frame containing both variants is the bare +700-X+ short-mark frame, which is dominated by Harappa tablets and is not the Parpola/M-2104 frame. The 004 evidence in the 097-700-X lane collapses to one repeated exact sequence family, while the 034 side is one source-gated M-2104 target with unresolved raw-image and five-character/four-token hazards.',
    safe_claim: 'The M-2104 count-compound hypothesis survives as the best current 034 crosswalk target, but it is not yet an accepted mapping. It demands CISI 3.1 or equivalent raw-source confirmation for M-2104 and blind segmentation of the existing 004 parallel crops.',
  },
  outputs: [
    'data/open_prototype/reports/lipi_034_m2104_count_compound_contexts.csv',
    'data/open_prototype/reports/lipi_034_m2104_count_compound_frames.csv',
    'data/open_prototype/reports/lipi_034_m2104_count_compound_tests.csv',
    'data/open_prototype/reports/lipi_034_m2104_count_compound_summary.json',
  ],
  accepted_decipherment_claims: 0,
};

fs.writeFileSync(summaryOut, `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify({
  status: 'wrote_m2104_count_compound_stress',
  context_rows: contextRows.length,
  frame_rows: frameRows.length,
  test_rows: tests.length,
  forward_700_034: forward034.length,
  forward_700_004: forward004.length,
  exact_097_700_034: summary.core_result.exact_097_700_034_rows.length,
  exact_097_700_004: summary.core_result.exact_097_700_004_rows.length,
}, null, 2));
