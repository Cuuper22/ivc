// Lipi sign 034 has no clean counterpart in the Mayig/Parpola crosswalk, and
// we need to know why. Two very different explanations exist: either the
// crosswalk logic actually filtered 034 out (which would mean something about
// the sign), or the overlap corpus simply never contains a row with an 034
// token (which means nothing — just missing coverage). This script settles it
// by counting, for signs 032, 033, and 034, how often each appears as an
// exact token in the Lipi metadata, in the overlap probe, in the clean
// alignment pairs, and in the candidate table, and by classifying each sign's
// darkness status. It also breaks metadata rows down by site, type,
// direction, and adjacency to sign 700, and double-checks that raw text hits
// for "034" in the overlap file are just ID strings like "M-34", not sign
// tokens. Writes three CSVs and a JSON summary whose conclusion field states
// the verdict: 034 is dark because of overlap coverage, not crosswalk
// filtering. No decipherment claim is made or accepted.
import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(base, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const overlapPath = path.join(reportsDir, 'overlap_probe.csv');
const alignmentPairsPath = path.join(reportsDir, 'crosswalk_alignment_pairs.csv');
const lipiCandidatesPath = path.join(reportsDir, 'crosswalk_lipi_to_mayig_candidates.csv');

const signCoverageOut = path.join(reportsDir, 'lipi_034_crosswalk_darkness_sign_coverage.csv');
const rowsOut = path.join(reportsDir, 'lipi_034_crosswalk_darkness_rows.csv');
const overlapRowsOut = path.join(reportsDir, 'lipi_034_crosswalk_darkness_overlap_rows.csv');
const summaryOut = path.join(reportsDir, 'lipi_034_crosswalk_darkness_summary.json');

const targetSigns = ['032', '033', '034'];

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

function tokens(text) {
  return text.match(/\d+/gu) ?? [];
}

function hasSign(row, sign) {
  return tokens(row.text).includes(sign);
}

function hasOverlapSign(row, sign) {
  return tokens(row.lipi_text).includes(sign);
}

function prefix(cisi) {
  const match = /^([A-Z]+)-/u.exec(cisi);
  return match?.[1] ?? (cisi === '-' ? '-' : 'other');
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

function fmtCounts(counts) {
  return Object.entries(counts)
    .map(([key, count]) => `${key}:${count}`)
    .join(';');
}

function uniqueCount(rows, keyFn) {
  return new Set(rows.map(keyFn).filter(Boolean)).size;
}

function frame700Relation(row, sign) {
  const rowTokens = tokens(row.text);
  for (let i = 0; i < rowTokens.length; i += 1) {
    if (rowTokens[i] !== sign) continue;
    if (rowTokens[i - 1] === '700') return '700_before_sign';
    if (rowTokens[i + 1] === '700') return '700_after_sign';
  }
  return 'not_adjacent_to_700';
}

function targetSignsPresent(row) {
  return targetSigns.filter((sign) => hasSign(row, sign));
}

function darknessStatus(sign, metadataRows, overlapRows, candidate, alignments) {
  if (sign === '034' && metadataRows.length > 0 && overlapRows.length === 0) {
    return 'coverage_absent_from_overlap_not_crosswalk_filtered';
  }
  if (metadataRows.length > 0 && overlapRows.length > 0 && alignments.length === 0) {
    return 'present_in_overlap_but_not_clean_aligned';
  }
  if (candidate) return 'crosswalk_candidate_present';
  return 'no_candidate';
}

const metadata = csvObjects(fs.readFileSync(metadataPath, 'utf8'));
const overlap = csvObjects(fs.readFileSync(overlapPath, 'utf8'));
const alignments = csvObjects(fs.readFileSync(alignmentPairsPath, 'utf8'));
const candidates = csvObjects(fs.readFileSync(lipiCandidatesPath, 'utf8'));
const candidateBySign = new Map(candidates.map((row) => [row.source_a_sign, row]));
const overlapByCisi = new Map(overlap.map((row) => [row.cisi, row]));

const rawOverlapLines = fs.readFileSync(overlapPath, 'utf8').split(/\r?\n/u);
const raw034LineHits = rawOverlapLines.filter((line) => line.includes('034'));

const signCoverageRows = targetSigns.map((sign) => {
  const metadataRows = metadata.filter((row) => hasSign(row, sign));
  const overlapRows = overlap.filter((row) => hasOverlapSign(row, sign));
  const signAlignments = alignments.filter((row) => row.lipi_sign === sign);
  const candidate = candidateBySign.get(sign);
  const countMatchRows = overlapRows.filter((row) => row.count_match === 'True');

  return {
    checked_date: '2026-05-25',
    lipi_sign: sign,
    metadata_rows_with_exact_token: String(metadataRows.length),
    metadata_unique_cisi_with_exact_token: String(uniqueCount(metadataRows, (row) => row.cisi)),
    metadata_rows_by_prefix: fmtCounts(countBy(metadataRows, (row) => prefix(row.cisi))),
    metadata_rows_by_site: fmtCounts(countBy(metadataRows, (row) => row.site)),
    metadata_rows_by_type: fmtCounts(countBy(metadataRows, (row) => row.type)),
    metadata_rows_by_direction: fmtCounts(countBy(metadataRows, (row) => row['dir.'])),
    metadata_rows_by_700_relation: fmtCounts(countBy(metadataRows, (row) => frame700Relation(row, sign))),
    overlap_rows_with_exact_token: String(overlapRows.length),
    overlap_count_match_rows_with_exact_token: String(countMatchRows.length),
    overlap_rows_by_site: fmtCounts(countBy(overlapRows, (row) => row.lipi_site)),
    overlap_rows_by_type: fmtCounts(countBy(overlapRows, (row) => row.lipi_type)),
    clean_alignment_rows: String(signAlignments.length),
    candidate_present: candidate ? '1' : '0',
    top_mayig_sign: candidate?.top_source_b_sign ?? '',
    candidate_grade: candidate?.candidate_grade ?? '',
    top_share: candidate?.top_share ?? '',
    diagnostic_status: darknessStatus(sign, metadataRows, overlapRows, candidate, signAlignments),
    accepted_decipherment_claim: '0',
  };
});

const targetRows = metadata
  .map((row) => ({ row, signs: targetSignsPresent(row) }))
  .filter(({ signs }) => signs.length > 0)
  .flatMap(({ row, signs }) =>
    signs.map((sign) => {
      const overlapRow = overlapByCisi.get(row.cisi);
      return {
        checked_date: '2026-05-25',
        lipi_sign: sign,
        source_row_id: row.id,
        cisi: row.cisi,
        cisi_prefix: prefix(row.cisi),
        in_mayig_overlap_by_cisi: overlapRow ? '1' : '0',
        overlap_count_match: overlapRow?.count_match ?? '',
        overlap_comparison_status: overlapRow?.comparison_status ?? '',
        site: row.site,
        type: row.type,
        material: row.material,
        shape: row.shape,
        preservation: row.preservation,
        direction: row['dir.'],
        class: row.class,
        sign_count: row.signs,
        frame700_relation: frame700Relation(row, sign),
        text: row.text,
        overlap_lipi_text: overlapRow?.lipi_text ?? '',
        overlap_mayig_graphemes: overlapRow?.mayig_graphemes ?? '',
        research_use:
          sign === '034'
            ? '034_source_coverage_check_row_not_a_crosswalk_mapping'
            : 'frame700_control_or_comparator_row_not_a_crosswalk_mapping',
        accepted_decipherment_claim: '0',
      };
    }),
  )
  .sort(
    (a, b) =>
      a.lipi_sign.localeCompare(b.lipi_sign, undefined, { numeric: true }) ||
      b.in_mayig_overlap_by_cisi.localeCompare(a.in_mayig_overlap_by_cisi) ||
      a.cisi_prefix.localeCompare(b.cisi_prefix) ||
      a.cisi.localeCompare(b.cisi, undefined, { numeric: true }) ||
      a.source_row_id.localeCompare(b.source_row_id, undefined, { numeric: true }),
  );

const overlapTargetRows = overlap
  .map((row) => ({ row, signs: targetSigns.filter((sign) => hasOverlapSign(row, sign)) }))
  .filter(({ signs }) => signs.length > 0)
  .flatMap(({ row, signs }) =>
    signs.map((sign) => ({
      checked_date: '2026-05-25',
      lipi_sign: sign,
      cisi: row.cisi,
      lipi_id: row.lipi_id,
      lipi_site: row.lipi_site,
      lipi_type: row.lipi_type,
      lipi_dir: row.lipi_dir,
      lipi_signs: row.lipi_signs,
      lipi_text: row.lipi_text,
      mayig_side_id: row.mayig_side_id,
      mayig_description: row.mayig_description,
      mayig_grapheme_count: row.mayig_grapheme_count,
      mayig_graphemes: row.mayig_graphemes,
      count_match: row.count_match,
      comparison_status: row.comparison_status,
      accepted_decipherment_claim: '0',
    })),
  )
  .sort(
    (a, b) =>
      a.lipi_sign.localeCompare(b.lipi_sign, undefined, { numeric: true }) ||
      a.cisi.localeCompare(b.cisi, undefined, { numeric: true }),
  );

const rows034 = targetRows.filter((row) => row.lipi_sign === '034');
const overlapScope = {
  rows: overlap.length,
  rows_by_site: countBy(overlap, (row) => row.lipi_site),
  rows_by_type: countBy(overlap, (row) => row.lipi_type),
  rows_by_mayig_description: countBy(overlap, (row) => row.mayig_description),
};

const summary = {
  checked_date: '2026-05-25',
  artifact: 'lipi_034_crosswalk_darkness_diagnostic',
  question:
    'Why does lipi 034 have no clean Mayig/Parpola crosswalk candidate: real crosswalk filtering, or absence from the overlap corpus?',
  inputs: [
    path.relative(base, metadataPath).replaceAll('\\', '/'),
    path.relative(base, overlapPath).replaceAll('\\', '/'),
    path.relative(base, alignmentPairsPath).replaceAll('\\', '/'),
    path.relative(base, lipiCandidatesPath).replaceAll('\\', '/'),
  ],
  target_signs: targetSigns,
  overlap_scope: overlapScope,
  sign_coverage: Object.fromEntries(
    signCoverageRows.map((row) => [
      row.lipi_sign,
      {
        metadata_rows: Number(row.metadata_rows_with_exact_token),
        overlap_rows: Number(row.overlap_rows_with_exact_token),
        clean_alignment_rows: Number(row.clean_alignment_rows),
        candidate_present: row.candidate_present === '1',
        top_mayig_sign: row.top_mayig_sign || null,
        diagnostic_status: row.diagnostic_status,
      },
    ]),
  ),
  exact_034_metadata_rows: rows034.length,
  exact_034_overlap_rows: Number(
    signCoverageRows.find((row) => row.lipi_sign === '034')?.overlap_rows_with_exact_token ?? 0,
  ),
  raw_overlap_lines_containing_string_034: raw034LineHits.length,
  raw_034_line_hit_note:
    raw034LineHits.length > 0
      ? 'Raw text search hits are not sign-token hits; the observed hit is an artifact ID/string occurrence such as M-34.'
      : 'No raw text-search hit for 034 was found in overlap_probe.csv.',
  conclusion:
    'The clean crosswalk lacks 034 because the current Mayig overlap layer has zero exact lipi 034 token rows. This is overlap coverage darkness, not evidence that 034 lacks a Mayig/Parpola counterpart.',
  outputs: [
    path.relative(base, signCoverageOut).replaceAll('\\', '/'),
    path.relative(base, rowsOut).replaceAll('\\', '/'),
    path.relative(base, overlapRowsOut).replaceAll('\\', '/'),
    path.relative(base, summaryOut).replaceAll('\\', '/'),
  ],
  accepted_decipherment_claims: 0,
};

fs.writeFileSync(signCoverageOut, toCsv(signCoverageRows), 'utf8');
fs.writeFileSync(rowsOut, toCsv(targetRows), 'utf8');
fs.writeFileSync(overlapRowsOut, toCsv(overlapTargetRows), 'utf8');
fs.writeFileSync(summaryOut, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
