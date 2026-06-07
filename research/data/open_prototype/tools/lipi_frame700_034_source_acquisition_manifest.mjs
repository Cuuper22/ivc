import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const lipiDir = path.join(base, 'data', 'open_prototype', 'lipi');

const packetPath = path.join(reportsDir, 'lipi_frame700_034_residue_validation_packet.csv');
const metadataPath = path.join(lipiDir, 'metadata_filtered.csv');
const outCsv = path.join(reportsDir, 'lipi_frame700_034_source_acquisition_manifest.csv');
const outJson = path.join(reportsDir, 'lipi_frame700_034_source_acquisition_manifest_summary.json');

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
  return [...new Set(values.filter((value) => value && value !== '-'))].sort((a, b) =>
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

function cisiCompare(a, b) {
  const ma = String(a).match(/^([A-Z]+)-(\d+)$/);
  const mb = String(b).match(/^([A-Z]+)-(\d+)$/);
  if (!ma || !mb) return String(a).localeCompare(String(b), undefined, { numeric: true });
  return ma[1].localeCompare(mb[1]) || Number(ma[2]) - Number(mb[2]);
}

function figureRefs(values) {
  const refs = [];
  for (const value of values) {
    const text = String(value ?? '');
    for (const match of text.matchAll(/Figure\s*([0-9]+(?:\.[0-9]+)?(?:\s*\([a-z]\))?)/gi)) {
      refs.push(`Figure ${match[1].replace(/\s+/g, ' ')}`);
    }
  }
  return uniqueSorted(refs);
}

function excavationIds(values) {
  const ids = [];
  for (const value of values) {
    const text = String(value ?? '');
    const withoutFigure = text.replace(/Figure.*$/i, '').trim();
    if (withoutFigure && withoutFigure !== '-' && withoutFigure !== '--') ids.push(withoutFigure);
  }
  return uniqueSorted(ids);
}

function primaryBucket(rows) {
  const has034 = rows.some((row) => row.subtype === '034');
  const has033 = rows.some((row) => row.subtype === '033');
  const has032 = rows.some((row) => row.subtype === '032');
  const has002 = rows.some((row) => row.long_token_set === '002;416;861');
  const hasNoLongerSmall = rows.some(
    (row) =>
      row.subtype === '034' &&
      ['all_short_or_no_longer_text', 'single_short_no_longer_text'].includes(row.context_class) &&
      ['h_10_13', 'h_lt_10'].includes(row.h_bin),
  );
  const has034Direction = rows.some((row) => row.subtype === '034' && row.short_text === '+034-700+');
  const has400740176 = rows.some((row) => row.long_token_set === '176;400;740');

  if (has034 && has002) return 'A_034_002_861_416_companion';
  if (has034 && hasNoLongerSmall) return 'A_034_no_longer_small_object';
  if (has034 && has034Direction) return 'A_034_direction_reversal';
  if (has034 && has400740176) return 'B_034_400_740_176_bridge';
  if (has033) return 'C_033_400_740_176_sibling';
  if (has032) return 'D_032_control';
  return 'E_other_034_residue';
}

function bucketRank(bucket) {
  const ranks = {
    A_034_002_861_416_companion: 1,
    A_034_no_longer_small_object: 2,
    A_034_direction_reversal: 3,
    B_034_400_740_176_bridge: 4,
    C_033_400_740_176_sibling: 5,
    D_032_control: 6,
    E_other_034_residue: 7,
  };
  return ranks[bucket] ?? 99;
}

function sourceRoute(row) {
  if (row.public_lead_status === 'candidate_public_images_plus_direction_note') {
    return 'verify_public_direction_lead_then_CISI_HARP_plate';
  }
  if (row.public_lead_status === 'candidate_public_images') {
    return 'inspect_public_image_pointer_then_CISI_HARP_plate';
  }
  if (row.public_lead_status === 'text_only_or_bibliographic_lead') {
    return 'use_text_lead_as_bibliographic_pointer_then_CISI_HARP_plate';
  }
  return 'direct_CISI_HARP_plate_request';
}

function evidenceGrade(row) {
  if (row.public_lead_status === 'candidate_public_images_plus_direction_note') return 'T2/T4_lead_not_source_validated';
  if (row.public_lead_status === 'candidate_public_images') return 'T4_image_pointer_not_source_validated';
  if (row.public_lead_status === 'text_only_or_bibliographic_lead') return 'T4_text_pointer_not_source_validated';
  return 'no_public_lead_source_required';
}

function sourceAsk(cisi, packetRows, metadataRows) {
  const shortRows = packetRows.map((row) => `${row.row_id} ${row.short_text}`);
  const allTexts = metadataRows.map((row) => `${row.id} ${row.text}`);
  const figs = figureRefs(metadataRows.map((row) => row['excavation-idno']));
  const exIds = excavationIds(metadataRows.map((row) => row['excavation-idno']));
  const sourceIds = [...exIds, ...figs].join('; ') || 'no excavation/figure hook in filtered metadata';
  return [
    `Request source-grade images/plates for all catalog rows of ${cisi}.`,
    `Metadata source hooks: ${sourceIds}.`,
    `Packet rows to verify: ${uniqueSorted(shortRows).join('; ')}.`,
    `All local rows to reconcile: ${uniqueSorted(allTexts).join('; ')}.`,
    'Needed: side labels/order, image/impression direction, sign segmentation, object material/shape/dimensions, and proof rows are distinct physical sides.',
  ].join(' ');
}

function supportKill(row) {
  if (row.primary_bucket === 'A_034_002_861_416_companion') {
    return {
      support:
        '034 remains distinct and paired with source-confirmed +002-861-416+ across at least one independent object outside the repeated H-2094/H-2095/H-2096 family.',
      kill:
        '034 collapses visually, +002-861-416+ is missegmented, +034-700+ is only direction normalization, or the bucket is one copied/molded family.',
    };
  }
  if (row.primary_bucket === 'A_034_no_longer_small_object') {
    return {
      support:
        '034 is visible on complete all-short/no-longer objects and the small-object measurement bucket survives source dimensions.',
      kill:
        'No-longer status is missing imaging, dimensions are catalog shortcuts, or 034 is a damaged/allographic sibling.',
    };
  }
  if (row.primary_bucket === 'A_034_direction_reversal') {
    return {
      support: '+034-700+ survives image-direction checking as a real ordered variant rather than normalized reading order.',
      kill: '+034-700+ is explained by impression/copy direction or catalog normalization.',
    };
  }
  if (row.primary_bucket === 'B_034_400_740_176_bridge') {
    return {
      support: '034 is distinct while sharing +400-740-176+ context with 033, preserving a true sibling contrast.',
      kill: '033/034 distinction collapses or +400-740-176+ side relation is catalog-only.',
    };
  }
  if (row.primary_bucket === 'C_033_400_740_176_sibling') {
    return {
      support: '033 remains a visually stable sibling subtype and +400-740-176+ segmentation survives.',
      kill: '033/034 collapse visually, H-355 duplicate short rows are not physical sides, or direction notes invalidate row order.',
    };
  }
  if (row.primary_bucket === 'D_032_control') {
    return {
      support: '032 controls stay visually distinct and occupy a different source-validated object/context bucket.',
      kill: '032 behaves like 034 after source validation or dimensions/context are metadata artifacts.',
    };
  }
  return {
    support: '034 is source-real and contributes independent non-H evidence after family-risk downweighting.',
    kill: 'Source image, side order, segmentation, or family independence fails.',
  };
}

const packetRows = parseCsv(fs.readFileSync(packetPath, 'utf8'));
const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));

const metadataByCisi = new Map();
for (const row of metadataRows) {
  if (!metadataByCisi.has(row.cisi)) metadataByCisi.set(row.cisi, []);
  metadataByCisi.get(row.cisi).push(row);
}

const packetByCisi = new Map();
for (const row of packetRows) {
  if (!packetByCisi.has(row.cisi)) packetByCisi.set(row.cisi, []);
  packetByCisi.get(row.cisi).push(row);
}

const artifacts = [];
for (const [cisi, rows] of packetByCisi.entries()) {
  const metadata = metadataByCisi.get(cisi) ?? [];
  const bucket = primaryBucket(rows);
  const first = rows.slice().sort((a, b) => Number(a.rank) - Number(b.rank))[0];
  const skeleton = {
    primary_bucket: bucket,
    cisi,
  };
  const { support, kill } = supportKill(skeleton);
  artifacts.push({
    primary_bucket: bucket,
    source_route: sourceRoute(first),
    evidence_grade_now: evidenceGrade(first),
    cisi,
    packet_rank_min: Math.min(...rows.map((row) => Number(row.rank))),
    packet_row_count: rows.length,
    packet_rows: uniqueSorted(rows.map((row) => row.row_id)).join(';'),
    packet_labels: uniqueSorted(rows.flatMap((row) => row.validation_label.split(';'))).join(';'),
    subtypes: uniqueSorted(rows.map((row) => row.subtype)).join(';'),
    short_texts: uniqueSorted(rows.map((row) => `${row.row_id}:${row.short_text}`)).join(';'),
    side_relations: uniqueSorted(rows.map((row) => row.side_relation)).join(';'),
    context_classes: uniqueSorted(rows.map((row) => row.context_class)).join(';'),
    longer_texts: uniqueSorted(rows.map((row) => row.longer_texts || 'NO_LONGER_TEXT')).join(';'),
    long_token_sets: uniqueSorted(rows.map((row) => row.long_token_set)).join(';'),
    sequence_family_keys: uniqueSorted(rows.map((row) => row.sequence_family_key)).join(' || '),
    sequence_family_count_max_no_h: Math.max(...rows.map((row) => Number(row.sequence_family_count_no_h || 1))),
    metadata_row_count: metadata.length,
    metadata_rows: uniqueSorted(metadata.map((row) => row.id)).join(';'),
    excavation_ids: excavationIds(metadata.map((row) => row['excavation-idno'])).join(';'),
    figure_refs: figureRefs(metadata.map((row) => row['excavation-idno'])).join(';'),
    area_sections: uniqueSorted(metadata.map((row) => row['area-section'])).join(';'),
    room_grids: uniqueSorted(metadata.map((row) => row['room-grid'])).join(';'),
    period_phase: uniqueSorted(metadata.map((row) => `${row.time}/${row.phase}`)).join(';'),
    depth: uniqueSorted(metadata.map((row) => row.depth)).join(';'),
    material: uniqueSorted(metadata.map((row) => row.material)).join(';'),
    shape_cross_section: uniqueSorted(metadata.map((row) => `${row.shape}/${row['cross-section']}`)).join(';'),
    condition_preservation: uniqueSorted(metadata.map((row) => `${row.condition}/${row.preservation}`)).join(';'),
    dimensions_mm: uniqueSorted(
      metadata.map((row) => `${row['horizontal(mm)']} x ${row['vertical(mm)']} x ${row['thickness(mm)']}`),
    ).join(';'),
    local_rows_to_reconcile: uniqueSorted(metadata.map((row) => `${row.id}:${row.text}`)).join(';'),
    public_lead_statuses: uniqueSorted(rows.map((row) => row.public_lead_status)).join(';'),
    source_request: sourceAsk(cisi, rows, metadata),
    preserves_034_residue_if: support,
    kills_or_downgrades_if: kill,
    source_check_status: 'source_acquisition_only_source_images_not_validated',
  });
}

artifacts.sort(
  (a, b) =>
    bucketRank(a.primary_bucket) - bucketRank(b.primary_bucket) ||
    a.packet_rank_min - b.packet_rank_min ||
    cisiCompare(a.cisi, b.cisi),
);

const header = [
  'acquisition_rank',
  'primary_bucket',
  'source_route',
  'evidence_grade_now',
  'cisi',
  'packet_rank_min',
  'packet_row_count',
  'packet_rows',
  'packet_labels',
  'subtypes',
  'short_texts',
  'side_relations',
  'context_classes',
  'longer_texts',
  'long_token_sets',
  'sequence_family_keys',
  'sequence_family_count_max_no_h',
  'metadata_row_count',
  'metadata_rows',
  'excavation_ids',
  'figure_refs',
  'area_sections',
  'room_grids',
  'period_phase',
  'depth',
  'material',
  'shape_cross_section',
  'condition_preservation',
  'dimensions_mm',
  'local_rows_to_reconcile',
  'public_lead_statuses',
  'source_request',
  'preserves_034_residue_if',
  'kills_or_downgrades_if',
  'source_check_status',
];

const csvRows = [header, ...artifacts.map((row, index) => header.map((key) => (key === 'acquisition_rank' ? index + 1 : row[key])))];
fs.writeFileSync(outCsv, toCsv(csvRows));

const summary = {
  generated_at: '2026-05-25',
  input_packet_rows: packetRows.length,
  acquisition_artifacts: artifacts.length,
  counts_by_primary_bucket: countBy(artifacts, (row) => row.primary_bucket),
  counts_by_source_route: countBy(artifacts, (row) => row.source_route),
  counts_by_evidence_grade_now: countBy(artifacts, (row) => row.evidence_grade_now),
  top_acquisition_artifacts: artifacts.slice(0, 25).map((row, index) => ({
    acquisition_rank: index + 1,
    cisi: row.cisi,
    primary_bucket: row.primary_bucket,
    source_route: row.source_route,
    excavation_ids: row.excavation_ids,
    figure_refs: row.figure_refs,
    short_texts: row.short_texts,
    longer_texts: row.longer_texts,
  })),
  immediate_request_batch: artifacts
    .filter((row) => bucketRank(row.primary_bucket) <= 2)
    .slice(0, 20)
    .map((row) => `${row.cisi}: ${row.excavation_ids || 'no excavation id'} ${row.figure_refs || ''}`.trim()),
  source_check_status: 'source_acquisition_manifest_only_source_images_not_validated',
};

fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(
  JSON.stringify(
    {
      outCsv,
      outJson,
      acquisition_artifacts: summary.acquisition_artifacts,
      counts_by_primary_bucket: summary.counts_by_primary_bucket,
      top_acquisition_artifacts: summary.top_acquisition_artifacts.slice(0, 10),
    },
    null,
    2,
  ),
);
