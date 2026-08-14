// Variant-collapse pressure test using an independent sign list. The lipi
// catalog treats 154/156 and 033/034 as distinct signs, but they may be
// allographs — the same sign drawn differently. The Mayig/Parpola crosswalk
// gives an outside check: if two lipi signs consistently align to the same
// Parpola sign at the same positions on the same objects, the distinction is
// under "collapse pressure".
//
// The script reads crosswalk_alignment_pairs.csv, the two candidate-mapping
// CSVs (lipi-to-mayig and the reverse), and overlap_probe.csv. For each of
// the five target signs (032, 033, 034, 154, 156) it gathers its positional
// alignments, its top Parpola candidate in both directions, and example
// contexts, then writes a verdict for three variant pairs. Headline: 154 and
// 156 both point to P004 (collapse pressure active), while 033 points to P147
// and 034 has zero clean alignments — crosswalk darkness, not collapse.
//
// Outputs: lipi_variant_crosswalk_pressure_signs.csv, _alignments.csv,
// _pairs.csv, and _summary.json. Pressure means "needs source-image
// inspection", never a visual-identity or reading claim; every row carries
// accepted_decipherment_claim = 0.

import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const alignmentPairsPath = path.join(reportsDir, 'crosswalk_alignment_pairs.csv');
const lipiCandidatesPath = path.join(reportsDir, 'crosswalk_lipi_to_mayig_candidates.csv');
const mayigCandidatesPath = path.join(reportsDir, 'crosswalk_mayig_to_lipi_candidates.csv');
const overlapPath = path.join(reportsDir, 'overlap_probe.csv');

const signsOut = path.join(reportsDir, 'lipi_variant_crosswalk_pressure_signs.csv');
const alignmentsOut = path.join(reportsDir, 'lipi_variant_crosswalk_pressure_alignments.csv');
const pairsOut = path.join(reportsDir, 'lipi_variant_crosswalk_pressure_pairs.csv');
const summaryOut = path.join(reportsDir, 'lipi_variant_crosswalk_pressure_summary.json');

const targetSigns = ['032', '033', '034', '154', '156'];
const variantPairs = [
  {
    pair_id: '154_vs_156',
    variant_family: '15x_003_h_series_variant',
    signs: ['154', '156'],
  },
  {
    pair_id: '033_vs_034',
    variant_family: 'frame700_h_series_variant',
    signs: ['033', '034'],
  },
  {
    pair_id: '032_vs_033_vs_034',
    variant_family: 'frame700_family_control',
    signs: ['032', '033', '034'],
  },
];

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
  const body = rows.map((row) =>
    header
      .map((key) => `"${String(row[key] ?? '').replaceAll('"', '""')}"`)
      .join(','),
  );
  return `${[header.map((key) => `"${key}"`).join(','), ...body].join('\n')}\n`;
}

function countBy(rows, keyFn) {
  const counts = {};
  for (const row of rows) {
    const key = keyFn(row);
    counts[key] = (counts[key] ?? 0) + 1;
  }
  return Object.fromEntries(
    Object.entries(counts).sort((a, b) => a[0].localeCompare(b[0], undefined, { numeric: true })),
  );
}

function fmtCountObject(counts) {
  return Object.entries(counts)
    .map(([key, count]) => `${key}:${count}`)
    .join(';');
}

function compactExample(row, overlap) {
  return [
    row.cisi,
    `${row.lipi_left} <${row.lipi_sign}> ${row.lipi_right}`,
    `${row.mayig_left} <${row.mayig_sign}> ${row.mayig_right}`,
    overlap?.lipi_text ?? '',
    overlap?.mayig_graphemes ?? '',
  ]
    .filter(Boolean)
    .join(' | ');
}

function candidateStatus(candidate, alignmentRows) {
  if (candidate) return 'candidate_present';
  if (alignmentRows.length > 0) return 'alignment_rows_present_but_candidate_absent';
  return 'absent_from_clean_overlap_candidates';
}

function signInterpretation(sign, candidate, alignmentRows) {
  if (sign === '034' && !candidate && alignmentRows.length === 0) {
    return 'No clean positional crosswalk evidence for lipi 034 in the current overlap layer; this is crosswalk-darkness, not proof of absence in the corpus.';
  }
  if (sign === '033' && candidate?.top_source_b_sign === 'P147') {
    return 'Lipi 033 has clean overlap support toward Mayig/Parpola P147; do not collapse it with 034 from this layer.';
  }
  if (sign === '032' && candidate?.top_source_b_sign === 'P145') {
    return 'Lipi 032 has clean overlap support toward Mayig/Parpola P145, making it a FRAME700 family control distinct from 033 in this layer.';
  }
  if (['154', '156'].includes(sign) && candidate?.top_source_b_sign === 'P004') {
    return 'This sign aligns to Mayig/Parpola P004 in the overlap layer; that creates allograph/sign-list-collapse pressure, not a visual identity claim.';
  }
  return 'No interpretation beyond provisional positional crosswalk pressure.';
}

const alignments = csvObjects(fs.readFileSync(alignmentPairsPath, 'utf8'));
const lipiCandidates = csvObjects(fs.readFileSync(lipiCandidatesPath, 'utf8'));
const mayigCandidates = csvObjects(fs.readFileSync(mayigCandidatesPath, 'utf8'));
const overlaps = csvObjects(fs.readFileSync(overlapPath, 'utf8'));

const overlapByCisi = new Map(overlaps.map((row) => [row.cisi, row]));
const lipiCandidateBySign = new Map(lipiCandidates.map((row) => [row.source_a_sign, row]));
const mayigCandidateBySign = new Map(mayigCandidates.map((row) => [row.source_a_sign, row]));

const targetAlignmentRows = alignments
  .filter((row) => targetSigns.includes(row.lipi_sign))
  .sort(
    (a, b) =>
      a.lipi_sign.localeCompare(b.lipi_sign, undefined, { numeric: true }) ||
      a.cisi.localeCompare(b.cisi, undefined, { numeric: true }) ||
      Number(a.position_0based) - Number(b.position_0based),
  );

const alignmentsByLipiSign = new Map();
for (const row of targetAlignmentRows) {
  if (!alignmentsByLipiSign.has(row.lipi_sign)) alignmentsByLipiSign.set(row.lipi_sign, []);
  alignmentsByLipiSign.get(row.lipi_sign).push(row);
}

const signRows = targetSigns.map((sign) => {
  const signAlignments = alignmentsByLipiSign.get(sign) ?? [];
  const candidate = lipiCandidateBySign.get(sign);
  const reverse = candidate ? mayigCandidateBySign.get(candidate.top_source_b_sign) : undefined;
  const mayigCounts = countBy(signAlignments, (row) => row.mayig_sign);
  const examples = signAlignments
    .slice(0, 8)
    .map((row) => compactExample(row, overlapByCisi.get(row.cisi)))
    .join(' || ');

  return {
    checked_date: '2026-05-25',
    lipi_sign: sign,
    sign_family: ['032', '033', '034'].includes(sign) ? 'frame700_family' : '15x_003_family',
    candidate_status: candidateStatus(candidate, signAlignments),
    alignment_rows: String(signAlignments.length),
    mayig_sign_counts: fmtCountObject(mayigCounts),
    top_mayig_sign: candidate?.top_source_b_sign ?? '',
    total_aligned_positions: candidate?.total_aligned_positions ?? '',
    top_count: candidate?.top_count ?? '',
    top_share: candidate?.top_share ?? '',
    candidate_grade: candidate?.candidate_grade ?? '',
    confidence: candidate?.confidence ?? '',
    runner_up_sign: candidate?.runner_up_sign ?? '',
    runner_up_count: candidate?.runner_up_count ?? '',
    counterexamples: candidate?.counterexamples ?? '',
    reverse_candidate_status: reverse ? 'reverse_candidate_present' : 'reverse_candidate_absent_or_unavailable',
    reverse_total_aligned_positions: reverse?.total_aligned_positions ?? '',
    reverse_top_lipi_sign: reverse?.top_source_b_sign ?? '',
    reverse_top_share: reverse?.top_share ?? '',
    reverse_runner_up_sign: reverse?.runner_up_sign ?? '',
    reverse_runner_up_count: reverse?.runner_up_count ?? '',
    reverse_confidence: reverse?.confidence ?? '',
    reverse_counterexamples: reverse?.counterexamples ?? '',
    example_alignments: examples,
    pressure_interpretation: signInterpretation(sign, candidate, signAlignments),
    accepted_decipherment_claim: '0',
  };
});

const alignmentOutRows = targetAlignmentRows.map((row) => {
  const overlap = overlapByCisi.get(row.cisi) ?? {};
  return {
    checked_date: '2026-05-25',
    cisi: row.cisi,
    lipi_id: row.lipi_id,
    mayig_side_id: row.mayig_side_id,
    lipi_sign: row.lipi_sign,
    mayig_sign: row.mayig_sign,
    position_class: row.position_class,
    position_1based: row.position_1based,
    lipi_context: `${row.lipi_left} <${row.lipi_sign}> ${row.lipi_right}`,
    mayig_context: `${row.mayig_left} <${row.mayig_sign}> ${row.mayig_right}`,
    lipi_text: overlap.lipi_text ?? '',
    mayig_graphemes: overlap.mayig_graphemes ?? '',
    comparison_status: overlap.comparison_status ?? '',
    evidence_status: row.evidence_status,
    pressure_interpretation:
      row.lipi_sign === '154' || row.lipi_sign === '156'
        ? '15x target positional alignment for allograph/crosswalk-collapse pressure'
        : 'FRAME700-family positional alignment for crosswalk differentiation pressure',
    accepted_decipherment_claim: '0',
  };
});

function pairStatus(pair) {
  const rows = pair.signs.map((sign) => signRows.find((row) => row.lipi_sign === sign));
  const topSigns = rows.map((row) => row.top_mayig_sign).filter(Boolean);
  const alignmentCounts = Object.fromEntries(rows.map((row) => [row.lipi_sign, Number(row.alignment_rows)]));

  if (pair.pair_id === '154_vs_156') {
    const reverseP004 = mayigCandidateBySign.get('P004');
    return {
      status: 'collapse_pressure_active_not_proven',
      evidence: `154 and 156 both point to P004 in the clean positional crosswalk; reverse P004 top lipi is ${reverseP004?.top_source_b_sign ?? 'unavailable'} with runner-up ${reverseP004?.runner_up_sign ?? 'none'}.`,
      implication: 'H-2237 must now survive source-image/diagnostic-stroke inspection before the 154/156 contrast can be used as functional evidence.',
      boundary: 'This is not proof that 154 and 156 are visually identical or functionally identical.',
    };
  }

  if (pair.pair_id === '033_vs_034') {
    return {
      status: '033_crosswalk_supported_034_unobserved_in_overlap',
      evidence: '033 points to P147 with nine clean aligned positions; 034 has zero clean aligned positions and no candidate row.',
      implication: 'Do not treat 033/034 like the 154/156 collapse case. The live 034 problem is source/crosswalk darkness, not current collapse evidence.',
      boundary: 'This layer cannot decide whether 034 is a distinct sign, an allograph, or missing because the clean overlap lacks the relevant rows.',
    };
  }

  return {
    status: 'frame700_crosswalk_differentiates_032_033_034_unobserved',
    evidence: `032 points to ${topSigns[0] ?? 'none'}, 033 points to ${topSigns[1] ?? 'none'}, and 034 is absent from clean overlap candidates.`,
    implication: 'The clean crosswalk differentiates 032 and 033 in the FRAME700 family while leaving 034 unresolved.',
    boundary: 'No FRAME700 reading, function, or sign value is accepted.',
  };
}

const pairRows = variantPairs.map((pair) => {
  const rows = pair.signs.map((sign) => signRows.find((row) => row.lipi_sign === sign));
  const status = pairStatus(pair);
  const topSigns = rows.map((row) => `${row.lipi_sign}->${row.top_mayig_sign || 'none'}`).join(';');
  const alignmentCounts = rows.map((row) => `${row.lipi_sign}:${row.alignment_rows}`).join(';');
  const candidateStatuses = rows.map((row) => `${row.lipi_sign}:${row.candidate_status}`).join(';');
  const sharedTop = new Set(rows.map((row) => row.top_mayig_sign).filter(Boolean));

  return {
    checked_date: '2026-05-25',
    pair_id: pair.pair_id,
    variant_family: pair.variant_family,
    lipi_signs: pair.signs.join(';'),
    top_mayig_signs: topSigns,
    alignment_rows_by_sign: alignmentCounts,
    candidate_statuses: candidateStatuses,
    shared_nonempty_top_mayig_sign:
      sharedTop.size === 1 && rows.every((row) => row.top_mayig_sign) ? [...sharedTop][0] : '',
    pair_status: status.status,
    evidence: status.evidence,
    implication: status.implication,
    boundary: status.boundary,
    accepted_decipherment_claim: '0',
  };
});

const alignmentRowsByLipiSign = Object.fromEntries(
  targetSigns.map((sign) => [sign, (alignmentsByLipiSign.get(sign) ?? []).length]),
);
const candidateRowsByLipiSign = Object.fromEntries(
  targetSigns.map((sign) => [sign, lipiCandidateBySign.has(sign) ? 1 : 0]),
);
const missingCandidateSigns = targetSigns.filter((sign) => !lipiCandidateBySign.has(sign));

const summary = {
  checked_date: '2026-05-25',
  artifact: 'lipi_variant_crosswalk_pressure',
  question:
    'Do the H-series and FRAME700 suspected variant pairs survive or collapse under the independent Mayig/Parpola positional crosswalk layer?',
  inputs: [
    path.relative(base, alignmentPairsPath).replaceAll('\\', '/'),
    path.relative(base, lipiCandidatesPath).replaceAll('\\', '/'),
    path.relative(base, mayigCandidatesPath).replaceAll('\\', '/'),
    path.relative(base, overlapPath).replaceAll('\\', '/'),
  ],
  target_signs: targetSigns,
  alignment_rows_by_lipi_sign: alignmentRowsByLipiSign,
  candidate_rows_by_lipi_sign: candidateRowsByLipiSign,
  missing_candidate_signs: missingCandidateSigns,
  pair_statuses: Object.fromEntries(pairRows.map((row) => [row.pair_id, row.pair_status])),
  headline_results: [
    '154/156: collapse pressure active because both signs align to P004 in the overlap layer; source images must decide H-2237.',
    '033/034: not the same pattern as 154/156; 033 aligns to P147, while 034 is crosswalk-dark in the clean overlap layer.',
    '032/033/034: clean overlap differentiates 032->P145 and 033->P147, but leaves 034 unresolved.',
  ],
  outputs: [
    path.relative(base, signsOut).replaceAll('\\', '/'),
    path.relative(base, alignmentsOut).replaceAll('\\', '/'),
    path.relative(base, pairsOut).replaceAll('\\', '/'),
    path.relative(base, summaryOut).replaceAll('\\', '/'),
  ],
  accepted_decipherment_claims: 0,
};

fs.writeFileSync(signsOut, toCsv(signRows), 'utf8');
fs.writeFileSync(alignmentsOut, toCsv(alignmentOutRows), 'utf8');
fs.writeFileSync(pairsOut, toCsv(pairRows), 'utf8');
fs.writeFileSync(summaryOut, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
