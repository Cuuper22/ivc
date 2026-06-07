import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const lipiDir = path.join(base, 'data', 'open_prototype', 'lipi');

const frameRowsPath = path.join(reportsDir, 'lipi_frame700_subtype_rows.csv');
const acquisitionPath = path.join(reportsDir, 'lipi_frame700_034_source_acquisition_manifest.csv');
const metadataPath = path.join(lipiDir, 'metadata_filtered.csv');
const outCsv = path.join(reportsDir, 'lipi_frame700_034_matched_control_probe.csv');
const outSummaryJson = path.join(reportsDir, 'lipi_frame700_034_matched_control_probe_summary.json');

const hSeries = new Set(Array.from({ length: 22 }, (_, index) => `H-${2218 + index}`));

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;

  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];
    const next = text[i + 1];

    if (char === '"' && inQuotes && next === '"') {
      field += '"';
      i += 1;
    } else if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === ',' && !inQuotes) {
      row.push(field);
      field = '';
    } else if ((char === '\n' || char === '\r') && !inQuotes) {
      if (char === '\r' && next === '\n') i += 1;
      row.push(field);
      if (row.some((value) => value !== '')) rows.push(row);
      row = [];
      field = '';
    } else {
      field += char;
    }
  }

  if (field !== '' || row.length > 0) {
    row.push(field);
    if (row.some((value) => value !== '')) rows.push(row);
  }

  const [header, ...records] = rows;
  return records.map((record) =>
    Object.fromEntries(header.map((name, index) => [name, record[index] ?? ''])),
  );
}

function toCsv(rows) {
  return `${rows
    .map((row) =>
      row
        .map((value) => {
          const text = String(value ?? '');
          return `"${text.replaceAll('"', '""')}"`;
        })
        .join(','),
    )
    .join('\n')}\n`;
}

function uniqueSorted(values) {
  return [...new Set(values.filter((value) => value && value !== '-' && value !== '--'))].sort((a, b) =>
    a.localeCompare(b, undefined, { numeric: true }),
  );
}

function countBy(rows, keyFn) {
  const counts = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return Object.fromEntries(
    [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])),
  );
}

function profileRows(rows) {
  if (!rows.length) {
    return {
      material: '',
      shape: '',
      cross_section: '',
      symbol: '',
      area_section: '',
      period_phase: '',
      excavation_prefix: '',
      row_texts: '',
    };
  }
  const excavationValues = rows.map((row) => row['excavation-idno']);
  const excavationPrefixes = excavationValues
    .map((value) => String(value ?? '').replace(/Figure.*$/i, '').trim())
    .filter((value) => value && value !== '-' && value !== '--')
    .map((value) => {
      const match = value.match(/^([A-Z]+\d{2,4})-/);
      return match ? match[1] : value.replace(/\d+.*$/, '');
    });
  return {
    material: uniqueSorted(rows.map((row) => row.material)).join(';'),
    shape: uniqueSorted(rows.map((row) => row.shape)).join(';'),
    cross_section: uniqueSorted(rows.map((row) => row['cross-section'])).join(';'),
    symbol: uniqueSorted(rows.map((row) => row.symbol)).join(';'),
    area_section: uniqueSorted(rows.map((row) => row['area-section'])).join(';'),
    period_phase: uniqueSorted(rows.map((row) => `${row.time}/${row.phase}`)).join(';'),
    excavation_prefix: uniqueSorted(excavationPrefixes).join(';'),
    row_texts: uniqueSorted(rows.map((row) => `${row.id}:${row.text}`)).join(';'),
  };
}

function compareField(target, candidate, field, weight, label, details) {
  const tv = target[field] ?? '';
  const cv = candidate[field] ?? '';
  if (!tv || !cv) return 0;
  if (tv === cv) {
    details.matches.push(label);
    return weight;
  }
  details.mismatches.push(`${label}:${tv}->${cv}`);
  return 0;
}

function scoreCandidate(target, candidate) {
  const details = { matches: [], mismatches: [] };
  let score = 0;

  score += compareField(target, candidate, 'type', 4, 'type', details);
  score += compareField(target, candidate, 'sides', 4, 'sides', details);
  score += compareField(target, candidate, 'site', 2, 'site', details);
  score += compareField(target.profile, candidate.profile, 'material', 3, 'material', details);
  score += compareField(target.profile, candidate.profile, 'shape', 3, 'shape', details);
  score += compareField(target.profile, candidate.profile, 'cross_section', 2, 'cross_section', details);
  score += compareField(target.profile, candidate.profile, 'symbol', 1, 'symbol', details);
  score += compareField(target.profile, candidate.profile, 'area_section', 1, 'area_section', details);
  score += compareField(target.profile, candidate.profile, 'period_phase', 1, 'period_phase', details);
  score += compareField(target.profile, candidate.profile, 'excavation_prefix', 1, 'excavation_prefix', details);
  score += compareField(target, candidate, 'h_bin', 3, 'h_bin', details);
  score += compareField(target, candidate, 'v_bin', 3, 'v_bin', details);
  score += compareField(target, candidate, 'area_bin', 3, 'area_bin', details);
  score += compareField(target, candidate, 'aspect_bin', 1, 'aspect_bin', details);
  score += compareField(target, candidate, 'context_class', 3, 'context_class', details);
  score += compareField(target, candidate, 'side_relation', 2, 'side_relation', details);
  score += compareField(target, candidate, 'order', 1, 'order', details);
  score += compareField(target, candidate, 'long_token_set', 2, 'long_token_set', details);

  return {
    score,
    matches: details.matches.join(';'),
    mismatches: details.mismatches.join(';'),
  };
}

function bestMatch(target, candidates) {
  let best = null;
  for (const candidate of candidates) {
    if (candidate.cisi === target.cisi) continue;
    if (candidate.sequence_family_key === target.sequence_family_key) continue;
    const scored = scoreCandidate(target, candidate);
    const current = {
      ...scored,
      candidate,
    };
    if (
      !best ||
      current.score > best.score ||
      (current.score === best.score && candidate.cisi.localeCompare(best.candidate.cisi, undefined, { numeric: true }) < 0)
    ) {
      best = current;
    }
  }
  return best;
}

function contrastReadiness(best033, best032) {
  const score033 = best033?.score ?? 0;
  const score032 = best032?.score ?? 0;
  if (score033 >= 28 && score032 >= 24) return 'strong_two_sibling_metadata_controls';
  if (score033 >= 28) return 'strong_033_control_only';
  if (score032 >= 24) return 'strong_032_control_only';
  if (score033 >= 22 || score032 >= 20) return 'partial_metadata_control';
  return 'weak_or_no_metadata_control';
}

const rows = parseCsv(fs.readFileSync(frameRowsPath, 'utf8')).filter((row) => !hSeries.has(row.cisi));
const acquisitionRows = parseCsv(fs.readFileSync(acquisitionPath, 'utf8'));
const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));

const metadataByCisi = new Map();
for (const row of metadataRows) {
  if (!metadataByCisi.has(row.cisi)) metadataByCisi.set(row.cisi, []);
  metadataByCisi.get(row.cisi).push(row);
}

const acquisitionByCisi = new Map(acquisitionRows.map((row) => [row.cisi, row]));

const enriched = rows.map((row) => ({
  ...row,
  profile: profileRows(metadataByCisi.get(row.cisi) ?? []),
  primary_bucket: acquisitionByCisi.get(row.cisi)?.primary_bucket ?? 'not_in_acquisition_manifest',
}));

const targets = enriched.filter((row) => row.subtype === '034');
const candidates033 = enriched.filter((row) => row.subtype === '033');
const candidates032 = enriched.filter((row) => row.subtype === '032');

const outputRows = targets.map((target) => {
  const best033 = bestMatch(target, candidates033);
  const best032 = bestMatch(target, candidates032);
  return {
    target_cisi: target.cisi,
    target_row_id: target.row_id,
    target_bucket: target.primary_bucket,
    target_short_text: target.short_text,
    target_context_class: target.context_class,
    target_side_relation: target.side_relation,
    target_long_token_set: target.long_token_set,
    target_profile: `${target.profile.material}|${target.profile.shape}|${target.profile.cross_section}|${target.profile.period_phase}|${target.profile.area_section}`,
    best_033_cisi: best033?.candidate.cisi ?? '',
    best_033_row_id: best033?.candidate.row_id ?? '',
    best_033_score: best033?.score ?? '',
    best_033_short_text: best033?.candidate.short_text ?? '',
    best_033_context_class: best033?.candidate.context_class ?? '',
    best_033_side_relation: best033?.candidate.side_relation ?? '',
    best_033_long_token_set: best033?.candidate.long_token_set ?? '',
    best_033_matches: best033?.matches ?? '',
    best_033_mismatches: best033?.mismatches ?? '',
    best_032_cisi: best032?.candidate.cisi ?? '',
    best_032_row_id: best032?.candidate.row_id ?? '',
    best_032_score: best032?.score ?? '',
    best_032_short_text: best032?.candidate.short_text ?? '',
    best_032_context_class: best032?.candidate.context_class ?? '',
    best_032_side_relation: best032?.candidate.side_relation ?? '',
    best_032_long_token_set: best032?.candidate.long_token_set ?? '',
    best_032_matches: best032?.matches ?? '',
    best_032_mismatches: best032?.mismatches ?? '',
    contrast_readiness: contrastReadiness(best033, best032),
    source_check_status: 'metadata_control_mapping_only_source_images_not_validated',
  };
});

outputRows.sort(
  (a, b) =>
    a.target_bucket.localeCompare(b.target_bucket) ||
    Number(b.best_033_score || 0) + Number(b.best_032_score || 0) - (Number(a.best_033_score || 0) + Number(a.best_032_score || 0)) ||
    a.target_cisi.localeCompare(b.target_cisi, undefined, { numeric: true }),
);

const header = [
  'target_cisi',
  'target_row_id',
  'target_bucket',
  'target_short_text',
  'target_context_class',
  'target_side_relation',
  'target_long_token_set',
  'target_profile',
  'best_033_cisi',
  'best_033_row_id',
  'best_033_score',
  'best_033_short_text',
  'best_033_context_class',
  'best_033_side_relation',
  'best_033_long_token_set',
  'best_033_matches',
  'best_033_mismatches',
  'best_032_cisi',
  'best_032_row_id',
  'best_032_score',
  'best_032_short_text',
  'best_032_context_class',
  'best_032_side_relation',
  'best_032_long_token_set',
  'best_032_matches',
  'best_032_mismatches',
  'contrast_readiness',
  'source_check_status',
];

fs.writeFileSync(outCsv, toCsv([header, ...outputRows.map((row) => header.map((key) => row[key]))]));

const byBucket = Object.fromEntries(
  Object.entries(countBy(outputRows, (row) => row.target_bucket)).map(([bucket, count]) => {
    const bucketRows = outputRows.filter((row) => row.target_bucket === bucket);
    return [
      bucket,
      {
        rows: count,
        readiness: countBy(bucketRows, (row) => row.contrast_readiness),
        avg_best_033_score:
          bucketRows.reduce((sum, row) => sum + Number(row.best_033_score || 0), 0) / bucketRows.length,
        avg_best_032_score:
          bucketRows.reduce((sum, row) => sum + Number(row.best_032_score || 0), 0) / bucketRows.length,
      },
    ];
  }),
);

const summary = {
  generated_at: '2026-05-25',
  scope: 'non-H FRAME700 034 rows matched against non-H 033 and 032 rows using current metadata/context fields',
  target_034_rows: outputRows.length,
  candidate_033_rows: candidates033.length,
  candidate_032_rows: candidates032.length,
  readiness_counts: countBy(outputRows, (row) => row.contrast_readiness),
  bucket_summary: byBucket,
  top_source_ready_rows: outputRows
    .filter((row) => row.contrast_readiness !== 'weak_or_no_metadata_control')
    .slice(0, 20)
    .map((row) => ({
      target_cisi: row.target_cisi,
      target_bucket: row.target_bucket,
      best_033: `${row.best_033_cisi}/${row.best_033_score}`,
      best_032: `${row.best_032_cisi}/${row.best_032_score}`,
      contrast_readiness: row.contrast_readiness,
      source_check_status: row.source_check_status,
    })),
  source_check_boundary:
    'metadata-matched control probe only; source images not validated; no accepted reading or value',
};

fs.writeFileSync(outSummaryJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(
  JSON.stringify(
    {
      outCsv,
      outSummaryJson,
      target_034_rows: summary.target_034_rows,
      readiness_counts: summary.readiness_counts,
      bucket_summary: summary.bucket_summary,
      top_source_ready_rows: summary.top_source_ready_rows.slice(0, 10),
    },
    null,
    2,
  ),
);
