import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const lipiDir = path.join(base, 'data', 'open_prototype', 'lipi');

const matchedPath = path.join(reportsDir, 'lipi_frame700_034_matched_control_probe.csv');
const frameRowsPath = path.join(reportsDir, 'lipi_frame700_subtype_rows.csv');
const metadataPath = path.join(lipiDir, 'metadata_filtered.csv');
const outCsv = path.join(reportsDir, 'lipi_frame700_034_source_triad_packet.csv');
const outJson = path.join(reportsDir, 'lipi_frame700_034_source_triad_packet_summary.json');

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

function figureRefs(values) {
  const refs = [];
  for (const value of values) {
    const text = String(value ?? '');
    for (const match of text.matchAll(/Figure\s*([0-9]+(?:\.[0-9]+)?(?:\s*\([a-z]\))?)/gi)) {
      refs.push(`Figure ${match[1].replace(/\s+/g, ' ')}`);
    }
  }
  return uniqueSorted(refs).join(';');
}

function excavationIds(values) {
  const ids = [];
  for (const value of values) {
    const text = String(value ?? '');
    const withoutFigure = text.replace(/Figure.*$/i, '').trim();
    if (withoutFigure && withoutFigure !== '-' && withoutFigure !== '--') ids.push(withoutFigure);
  }
  return uniqueSorted(ids).join(';');
}

function metadataSummary(cisi, metadataByCisi) {
  const rows = metadataByCisi.get(cisi) ?? [];
  return {
    metadata_rows: uniqueSorted(rows.map((row) => row.id)).join(';'),
    excavation_ids: excavationIds(rows.map((row) => row['excavation-idno'])),
    figure_refs: figureRefs(rows.map((row) => row['excavation-idno'])),
    material_shape: uniqueSorted(rows.map((row) => `${row.material}/${row.shape}/${row['cross-section']}`)).join(';'),
    period_phase_depth: uniqueSorted(rows.map((row) => `${row.time}/${row.phase}/${row.depth}`)).join(';'),
    local_rows: uniqueSorted(rows.map((row) => `${row.id}:${row.text}`)).join(';'),
    dimensions_mm: uniqueSorted(
      rows.map((row) => `${row['horizontal(mm)']} x ${row['vertical(mm)']} x ${row['thickness(mm)']}`),
    ).join(';'),
  };
}

function rowById(rows, cisi, rowId) {
  return rows.find((row) => row.cisi === cisi && row.row_id === rowId) ?? null;
}

function artifactBucketRank(bucket) {
  const ranks = {
    A_034_002_861_416_companion: 1,
    A_034_no_longer_small_object: 2,
    A_034_direction_reversal: 3,
    B_034_400_740_176_bridge: 4,
    E_other_034_residue: 5,
  };
  return ranks[bucket] ?? 99;
}

function readinessRank(readiness) {
  const ranks = {
    strong_two_sibling_metadata_controls: 1,
    strong_033_control_only: 2,
    strong_032_control_only: 3,
    partial_metadata_control: 4,
    weak_or_no_metadata_control: 5,
  };
  return ranks[readiness] ?? 99;
}

function sourceNeed(cisi, meta) {
  const hooks = [meta.excavation_ids, meta.figure_refs].filter(Boolean).join('; ') || 'no local source hook';
  return `${cisi}: all sides, source plate/image ID, side labels/order, inscription/impression direction, segmentation; hooks ${hooks}`;
}

function triadQuestion(row) {
  return [
    `Does target ${row.target_cisi} ${row.target_short_text} remain visually distinct from matched 033 ${row.best_033_cisi} ${row.best_033_short_text} and matched 032 ${row.best_032_cisi} ${row.best_032_short_text}?`,
    `After source direction and side-order checks, is the target's context (${row.target_side_relation}; ${row.target_long_token_set}) still different from both controls?`,
    'If not, is the residue better explained by object format, direction/allography, or duplicate-family copying?',
  ].join(' ');
}

function preserveIf(row) {
  return [
    'all three source images confirm 034/033/032 are visually distinct',
    'target and controls are comparable object formats',
    'target keeps a source-visible side/companion contrast after direction checks',
    'target is not only one copied/molded local family',
  ].join('; ');
}

function downgradeIf(row) {
  return [
    '034 is visible but matched 033/032 controls show the same side/context behavior',
    'only dimensions or object form differ after source correction',
    'control matches fail because source metadata or measurements are wrong',
  ].join('; ');
}

function killIf(row) {
  return [
    '034 collapses visually into 033/032',
    '+034-700+ versus +700-034+ is only image/corpus direction normalization',
    'longer companion rows are missegmented',
    'no-longer status is missing side coverage',
    'the contrast is confined to duplicate/copy family rows',
  ].join('; ');
}

const matchedRows = parseCsv(fs.readFileSync(matchedPath, 'utf8'));
const frameRows = parseCsv(fs.readFileSync(frameRowsPath, 'utf8'));
const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));

const metadataByCisi = new Map();
for (const row of metadataRows) {
  if (!metadataByCisi.has(row.cisi)) metadataByCisi.set(row.cisi, []);
  metadataByCisi.get(row.cisi).push(row);
}

const triadRows = matchedRows.map((row) => {
  const targetFrame = rowById(frameRows, row.target_cisi, row.target_row_id);
  const frame033 = rowById(frameRows, row.best_033_cisi, row.best_033_row_id);
  const frame032 = rowById(frameRows, row.best_032_cisi, row.best_032_row_id);
  const targetMeta = metadataSummary(row.target_cisi, metadataByCisi);
  const meta033 = metadataSummary(row.best_033_cisi, metadataByCisi);
  const meta032 = metadataSummary(row.best_032_cisi, metadataByCisi);
  const totalScore = Number(row.best_033_score || 0) + Number(row.best_032_score || 0);
  return {
    target_bucket: row.target_bucket,
    contrast_readiness: row.contrast_readiness,
    triad_score: totalScore,
    target_cisi: row.target_cisi,
    target_row_id: row.target_row_id,
    target_short_text: row.target_short_text,
    target_context_class: row.target_context_class,
    target_side_relation: row.target_side_relation,
    target_long_token_set: row.target_long_token_set,
    target_hva_bins: targetFrame
      ? `${targetFrame.h_bin}/${targetFrame.v_bin}/${targetFrame.area_bin}/${targetFrame.aspect_bin}`
      : '',
    target_source_hooks: [targetMeta.excavation_ids, targetMeta.figure_refs].filter(Boolean).join(';'),
    target_material_shape: targetMeta.material_shape,
    target_period_phase_depth: targetMeta.period_phase_depth,
    target_dimensions_mm: targetMeta.dimensions_mm,
    target_local_rows: targetMeta.local_rows,
    control_033_cisi: row.best_033_cisi,
    control_033_row_id: row.best_033_row_id,
    control_033_score: row.best_033_score,
    control_033_short_text: row.best_033_short_text,
    control_033_context_class: row.best_033_context_class,
    control_033_side_relation: row.best_033_side_relation,
    control_033_long_token_set: row.best_033_long_token_set,
    control_033_hva_bins: frame033 ? `${frame033.h_bin}/${frame033.v_bin}/${frame033.area_bin}/${frame033.aspect_bin}` : '',
    control_033_source_hooks: [meta033.excavation_ids, meta033.figure_refs].filter(Boolean).join(';'),
    control_033_material_shape: meta033.material_shape,
    control_033_period_phase_depth: meta033.period_phase_depth,
    control_033_dimensions_mm: meta033.dimensions_mm,
    control_033_local_rows: meta033.local_rows,
    control_033_matches: row.best_033_matches,
    control_033_mismatches: row.best_033_mismatches,
    control_032_cisi: row.best_032_cisi,
    control_032_row_id: row.best_032_row_id,
    control_032_score: row.best_032_score,
    control_032_short_text: row.best_032_short_text,
    control_032_context_class: row.best_032_context_class,
    control_032_side_relation: row.best_032_side_relation,
    control_032_long_token_set: row.best_032_long_token_set,
    control_032_hva_bins: frame032 ? `${frame032.h_bin}/${frame032.v_bin}/${frame032.area_bin}/${frame032.aspect_bin}` : '',
    control_032_source_hooks: [meta032.excavation_ids, meta032.figure_refs].filter(Boolean).join(';'),
    control_032_material_shape: meta032.material_shape,
    control_032_period_phase_depth: meta032.period_phase_depth,
    control_032_dimensions_mm: meta032.dimensions_mm,
    control_032_local_rows: meta032.local_rows,
    control_032_matches: row.best_032_matches,
    control_032_mismatches: row.best_032_mismatches,
    source_request_bundle: [sourceNeed(row.target_cisi, targetMeta), sourceNeed(row.best_033_cisi, meta033), sourceNeed(row.best_032_cisi, meta032)].join(' | '),
    triad_question: triadQuestion(row),
    preserves_source_contrast_if: preserveIf(row),
    downgrades_to_object_format_if: downgradeIf(row),
    kills_034_residue_if: killIf(row),
    source_check_status: 'source_triad_only_source_images_not_validated_no_interpretive_claims',
  };
});

triadRows.sort(
  (a, b) =>
    artifactBucketRank(a.target_bucket) - artifactBucketRank(b.target_bucket) ||
    readinessRank(a.contrast_readiness) - readinessRank(b.contrast_readiness) ||
    b.triad_score - a.triad_score ||
    a.target_cisi.localeCompare(b.target_cisi, undefined, { numeric: true }),
);

const header = [
  'triad_rank',
  'target_bucket',
  'contrast_readiness',
  'triad_score',
  'target_cisi',
  'target_row_id',
  'target_short_text',
  'target_context_class',
  'target_side_relation',
  'target_long_token_set',
  'target_hva_bins',
  'target_source_hooks',
  'target_material_shape',
  'target_period_phase_depth',
  'target_dimensions_mm',
  'target_local_rows',
  'control_033_cisi',
  'control_033_row_id',
  'control_033_score',
  'control_033_short_text',
  'control_033_context_class',
  'control_033_side_relation',
  'control_033_long_token_set',
  'control_033_hva_bins',
  'control_033_source_hooks',
  'control_033_material_shape',
  'control_033_period_phase_depth',
  'control_033_dimensions_mm',
  'control_033_local_rows',
  'control_033_matches',
  'control_033_mismatches',
  'control_032_cisi',
  'control_032_row_id',
  'control_032_score',
  'control_032_short_text',
  'control_032_context_class',
  'control_032_side_relation',
  'control_032_long_token_set',
  'control_032_hva_bins',
  'control_032_source_hooks',
  'control_032_material_shape',
  'control_032_period_phase_depth',
  'control_032_dimensions_mm',
  'control_032_local_rows',
  'control_032_matches',
  'control_032_mismatches',
  'source_request_bundle',
  'triad_question',
  'preserves_source_contrast_if',
  'downgrades_to_object_format_if',
  'kills_034_residue_if',
  'source_check_status',
];

fs.writeFileSync(outCsv, toCsv([header, ...triadRows.map((row, index) => header.map((key) => (key === 'triad_rank' ? index + 1 : row[key])))]));

const summary = {
  generated_at: '2026-05-25',
  input_matched_rows: matchedRows.length,
  triad_rows: triadRows.length,
  counts_by_bucket: countBy(triadRows, (row) => row.target_bucket),
  counts_by_readiness: countBy(triadRows, (row) => row.contrast_readiness),
  top_triads: triadRows.slice(0, 25).map((row, index) => ({
    triad_rank: index + 1,
    target: `${row.target_cisi}/${row.target_short_text}/${row.target_long_token_set}`,
    control_033: `${row.control_033_cisi}/${row.control_033_short_text}/${row.control_033_score}`,
    control_032: `${row.control_032_cisi}/${row.control_032_short_text}/${row.control_032_score}`,
    target_hooks: row.target_source_hooks,
    control_033_hooks: row.control_033_source_hooks,
    control_032_hooks: row.control_032_source_hooks,
    contrast_readiness: row.contrast_readiness,
  })),
  source_check_boundary:
    'source-image triad packet only; source rows, order, direction, segmentation, and object metadata still require plate/image validation; no interpretive claim is encoded',
};

fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(
  JSON.stringify(
    {
      outCsv,
      outJson,
      triad_rows: summary.triad_rows,
      counts_by_bucket: summary.counts_by_bucket,
      counts_by_readiness: summary.counts_by_readiness,
      top_triads: summary.top_triads.slice(0, 10),
    },
    null,
    2,
  ),
);
