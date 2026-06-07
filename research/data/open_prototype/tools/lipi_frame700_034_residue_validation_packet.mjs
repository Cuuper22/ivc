import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const rowsPath = path.join(reportsDir, 'lipi_frame700_subtype_rows.csv');
const publicLeadsPath = path.join(reportsDir, 'lipi_short_mark_plate_public_leads.csv');
const outCsv = path.join(reportsDir, 'lipi_frame700_034_residue_validation_packet.csv');
const outJson = path.join(reportsDir, 'lipi_frame700_034_residue_validation_packet_summary.json');

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
  return [...new Set(values.filter(Boolean))].sort((a, b) =>
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

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function hasAllTokens(row, wanted) {
  const tokenSet = new Set(tokens(row.long_token_set));
  return wanted.every((token) => tokenSet.has(token));
}

function naturalCisi(value) {
  const match = String(value).match(/^([A-Z]+)-(\d+)$/);
  return match ? [match[1], Number(match[2])] : [String(value), 0];
}

function cisiCompare(a, b) {
  const [ap, an] = naturalCisi(a);
  const [bp, bn] = naturalCisi(b);
  return ap.localeCompare(bp) || an - bn || String(a).localeCompare(String(b));
}

function rowIdNumber(row) {
  const parsed = Number(row.row_id);
  return Number.isFinite(parsed) ? parsed : 0;
}

function sourceLeadStatus(leads) {
  if (!leads.length) return 'no_checked_public_lead';
  const kinds = new Set(leads.map((lead) => lead.lead_kind));
  if (kinds.has('artifact_mention_with_candidate_images') && kinds.has('published_direction_or_corpus_note')) {
    return 'candidate_public_images_plus_direction_note';
  }
  if (kinds.has('artifact_mention_with_candidate_images')) return 'candidate_public_images';
  if (kinds.has('text_only_or_bibliographic_lead')) return 'text_only_or_bibliographic_lead';
  return 'public_lead_other';
}

function leadField(leads, field) {
  return uniqueSorted(leads.map((lead) => lead[field])).join(';');
}

function sequenceFamilyCount(rows, row) {
  return rows.filter((other) => other.sequence_family_key === row.sequence_family_key).length;
}

function startsOrEndsWith034(row) {
  return row.short_text === '+034-700+' || row.order === '700_last';
}

function is034Core(row) {
  return row.subtype === '034' && !hSeries.has(row.cisi);
}

function is033Sibling(row) {
  if (row.subtype !== '033' || hSeries.has(row.cisi)) return false;
  if (row.long_token_set === '176;400;740') return true;
  if (row.long_edge_frames.includes('400...176')) return true;
  if (['H-233', 'H-309', 'H-316', 'H-353', 'H-355', 'H-357', 'H-935', 'H-978', 'H-1302', 'H-1303', 'H-1304', 'H-1344', 'H-1345', 'H-1346', 'H-1347'].includes(row.cisi)) return true;
  return false;
}

function is032Control(row) {
  if (row.subtype !== '032' || hSeries.has(row.cisi)) return false;
  if (row.long_token_set === '001;031;140;740') return true;
  if (row.long_edge_frames.includes('740...140')) return true;
  if (row.long_edge_frames.includes('740...817')) return true;
  if (['H-1771', 'H-1772', 'H-1773', 'H-1100', 'H-697'].includes(row.cisi)) return true;
  return row.v_bin === 'v_ge_10' && row.h_bin === 'h_ge_16';
}

function validationLabels(row, allRows) {
  const labels = [];
  if (is034Core(row)) labels.push('positive_034_residue_candidate');
  if (is033Sibling(row)) labels.push('sibling_033_branch');
  if (is032Control(row)) labels.push('032_control');
  if (startsOrEndsWith034(row) || row.short_text === '+033-700+' || row.order === '700_last') {
    labels.push('allograph_direction_risk');
  }
  if (row.cisi === 'H-355' || sequenceFamilyCount(allRows, row) > 1) labels.push('duplicate_family_risk');
  return labels;
}

function score034(row, leads, familyCount) {
  let score = 100;
  const reasons = ['all non-H 034 rows are included because the blocked null left 034 recall above the relation-preserving null'];
  if (row.long_edge_frames.includes('002...416') || row.long_token_set === '002;416;861') {
    score += 60;
    reasons.push('034-specific companion family +002-861-416+ / edge 002...416');
  }
  if (row.context_class === 'all_short_or_no_longer_text') {
    score += 30;
    reasons.push('tests 034 without a longer companion row');
  }
  if (row.h_bin === 'h_10_13') {
    score += 20;
    reasons.push('falls in h_10_13 bucket enriched for 034 in no-H contrasts');
  }
  if (['area_lt_80', 'area_80_120'].includes(row.area_bin)) {
    score += 15;
    reasons.push('small-object area bucket checks whether residue is object-format only');
  }
  if (row.side_relation === 'short_before_all_longer') {
    score += 12;
    reasons.push('short-before-longer side relation needs source-side validation');
  }
  if (startsOrEndsWith034(row)) {
    score += 10;
    reasons.push('reversed +034-700+ / 700_last order is a direction/allograph hazard');
  }
  if (hasAllTokens(row, ['400', '740', '176'])) {
    score += 8;
    reasons.push('shares the 400-740-176 sibling environment previously seen with 033 controls');
  }
  if (leads.length) {
    score += 5;
    reasons.push('has a checked public acquisition lead, but not source-grade proof');
  }
  if (familyCount > 1) {
    score -= Math.min(20, (familyCount - 1) * 4);
    reasons.push(`sequence family repeats ${familyCount} times; independence must be downweighted`);
  }
  return { score, reasons };
}

function score033(row, leads, familyCount) {
  let score = 85;
  const reasons = ['matched 033 sibling branch included to test whether 033/034 are source-real contrasts'];
  if (row.long_token_set === '176;400;740' || row.long_edge_frames.includes('400...176')) {
    score += 45;
    reasons.push('canonical 033 +400-740-176+ sibling environment');
  }
  if (['H-1302', 'H-1303'].includes(row.cisi)) {
    score += 25;
    reasons.push('published direction/corpus-note lead can expose direction normalization risk');
  }
  if (row.cisi === 'H-355') {
    score += 25;
    reasons.push('duplicate +700-033+ sides must be physical sides, not catalog duplication');
  }
  if (leads.length) {
    score += 5;
    reasons.push('has a checked public acquisition lead, but not source-grade proof');
  }
  if (familyCount > 1) reasons.push(`sequence family repeats ${familyCount} times; use as visual contrast before statistical independence`);
  return { score, reasons };
}

function score032(row, leads, familyCount) {
  let score = 70;
  const reasons = ['032 control included to prevent a two-way 033/034 overfit'];
  if (row.long_token_set === '001;031;140;740' || row.long_edge_frames.includes('740...140')) {
    score += 35;
    reasons.push('explicit 032 control family +740-031-001-140+');
  }
  if (row.long_edge_frames.includes('740...817')) {
    score += 25;
    reasons.push('large-object 032 control family with edge 740...817');
  }
  if (row.v_bin === 'v_ge_10') {
    score += 15;
    reasons.push('v_ge_10 control checks the opposite side of the 034 dimension residue');
  }
  if (row.h_bin === 'h_ge_16') {
    score += 10;
    reasons.push('large horizontal-bin control');
  }
  if (leads.length) {
    score += 5;
    reasons.push('has a checked public acquisition lead, but not source-grade proof');
  }
  if (familyCount > 1) reasons.push(`sequence family repeats ${familyCount} times; use as visual contrast before statistical independence`);
  return { score, reasons };
}

function supportOutcome(row) {
  if (row.subtype === '034') {
    return [
      'source image confirms 034 is visually distinct from 033/032',
      'short side and order match corpus row',
      'side relation is physical or otherwise justified',
      'residue survives in at least one independent bucket after family-risk rows are downweighted',
    ].join('; ');
  }
  if (row.subtype === '033') {
    return [
      'source image confirms 033 is visually distinct from 034/032',
      '+400-740-176+ companion segmentation holds where present',
      '033 branch remains a stable contrast class rather than a transcription variant',
    ].join('; ');
  }
  return [
    'source image confirms 032 is visually distinct from 033/034',
    'control family and dimensions are source-real',
    '032 does not collapse into the 034 residue bucket under matched metadata',
  ].join('; ');
}

function killOutcome(row) {
  const shared = [
    'source unavailable',
    'short sign is miscopied, damaged beyond distinction, or visually collapses with sibling subtype',
    'side order is editorial/catalog-only and cannot support side-relation contrast',
    'direction normalization explains +700-subtype+ versus +subtype-700+',
    'longer text is missegmented or absent in source despite corpus row',
  ];
  if (row.subtype === '034') {
    shared.push('034-specific bucket is one copied/molded family rather than independent attestations');
    shared.push('no-longer/all-short rows turn out to have missing or unrecorded longer sides');
  }
  if (row.subtype === '033') shared.push('033/034 boundary collapses in plate-grade images');
  if (row.subtype === '032') shared.push('032 controls show the same side/context profile as 034 after source validation');
  return shared.join('; ');
}

function sourceQuestions(row) {
  const questions = [
    `Is ${row.short_text} actually visible as transcribed on catalog side ${row.short_side_index}?`,
    'Are the catalog rows distinct physical sides or a transcription/display convention?',
    'Is side order physical, photographic, editorial, or arbitrary?',
    'Is reading direction based on inscription, impression, catalog normalization, or unresolved?',
    `Do the longer-side readings survive source image check: ${row.longer_texts || 'NO_LONGER_TEXT'}?`,
    'Does this row remain independent after object family, mold/copy, and publication-cluster checks?',
  ];
  if (row.subtype === '034') {
    questions.push('Does this 034 row still belong to an enriched bucket after excluding H-2218..H-2239 and duplicate families?');
  }
  if (row.subtype === '033') questions.push('Does 033 remain visually and positionally separate from the 034 candidate bucket?');
  if (row.subtype === '032') questions.push('Does 032 behave as a genuine negative control under matched object metadata?');
  return questions.join('; ');
}

function manualFields() {
  return {
    source_found: '',
    source_citation: '',
    image_or_plate_id: '',
    image_resolution_or_quality: '',
    catalog_rows_distinct_physical_sides: '',
    side_order_basis: '',
    image_direction_basis: '',
    short_mark_verified: '',
    longer_text_verified: '',
    validation_outcome_allowed_values:
      'passes_source_check;fails_short_text_order;fails_segmentation;fails_side_relation;direction_unresolved;duplicate_or_family_only;source_unavailable',
    validation_outcome: '',
    notes: '',
  };
}

const sourceRows = parseCsv(fs.readFileSync(rowsPath, 'utf8'));
const leadRows = fs.existsSync(publicLeadsPath) ? parseCsv(fs.readFileSync(publicLeadsPath, 'utf8')) : [];

const leadsByCisi = new Map();
for (const lead of leadRows) {
  if (!leadsByCisi.has(lead.cisi)) leadsByCisi.set(lead.cisi, []);
  leadsByCisi.get(lead.cisi).push(lead);
}

const nonHRows = sourceRows.filter((row) => !hSeries.has(row.cisi));
const familyCounts = new Map();
for (const row of nonHRows) {
  familyCounts.set(row.sequence_family_key, (familyCounts.get(row.sequence_family_key) ?? 0) + 1);
}

const selectedRows = sourceRows.filter((row) => is034Core(row) || is033Sibling(row) || is032Control(row));

const packetRows = selectedRows.map((row) => {
  const labels = validationLabels(row, nonHRows);
  const leads = leadsByCisi.get(row.cisi) ?? [];
  const familyCount = familyCounts.get(row.sequence_family_key) ?? 1;
  const scored =
    row.subtype === '034'
      ? score034(row, leads, familyCount)
      : row.subtype === '033'
        ? score033(row, leads, familyCount)
        : score032(row, leads, familyCount);

  return {
    priority_score: scored.score,
    validation_label: labels.join(';'),
    cisi: row.cisi,
    row_id: row.row_id,
    subtype: row.subtype,
    short_text: row.short_text,
    order: row.order,
    type: row.type,
    site: row.site,
    sides: row.sides,
    direction: row.direction,
    short_side_index: row.short_side_index,
    context_class: row.context_class,
    side_relation: row.side_relation,
    longer_row_count: row.longer_row_count,
    longer_texts: row.longer_texts,
    long_token_set: row.long_token_set,
    long_edge_frames: row.long_edge_frames,
    sequence_family_key: row.sequence_family_key,
    sequence_family_count_no_h: familyCount,
    horizontal_mm: row.horizontal_mm,
    vertical_mm: row.vertical_mm,
    thickness_mm: row.thickness_mm,
    h_bin: row.h_bin,
    v_bin: row.v_bin,
    area_bin: row.area_bin,
    aspect_bin: row.aspect_bin,
    th_bin: row.th_bin,
    public_lead_status: sourceLeadStatus(leads),
    public_lead_kinds: leadField(leads, 'lead_kind'),
    public_source_urls: leadField(leads, 'source_url'),
    candidate_image_urls: leadField(leads, 'image_url'),
    source_tiers_seen: leadField(leads, 'source_tier'),
    why_prioritized: scored.reasons.join('; '),
    source_questions: sourceQuestions(row),
    support_outcome: supportOutcome(row),
    kill_outcome: killOutcome(row),
    source_check_status: 'source_validation_target_only_source_images_not_validated',
    ...manualFields(),
  };
});

packetRows.sort(
  (a, b) =>
    b.priority_score - a.priority_score ||
    cisiCompare(a.cisi, b.cisi) ||
    rowIdNumber(a) - rowIdNumber(b),
);

const header = [
  'rank',
  'priority_score',
  'validation_label',
  'cisi',
  'row_id',
  'subtype',
  'short_text',
  'order',
  'type',
  'site',
  'sides',
  'direction',
  'short_side_index',
  'context_class',
  'side_relation',
  'longer_row_count',
  'longer_texts',
  'long_token_set',
  'long_edge_frames',
  'sequence_family_key',
  'sequence_family_count_no_h',
  'horizontal_mm',
  'vertical_mm',
  'thickness_mm',
  'h_bin',
  'v_bin',
  'area_bin',
  'aspect_bin',
  'th_bin',
  'public_lead_status',
  'public_lead_kinds',
  'public_source_urls',
  'candidate_image_urls',
  'source_tiers_seen',
  'why_prioritized',
  'source_questions',
  'support_outcome',
  'kill_outcome',
  'source_check_status',
  'source_found',
  'source_citation',
  'image_or_plate_id',
  'image_resolution_or_quality',
  'catalog_rows_distinct_physical_sides',
  'side_order_basis',
  'image_direction_basis',
  'short_mark_verified',
  'longer_text_verified',
  'validation_outcome_allowed_values',
  'validation_outcome',
  'notes',
];

const csvRows = [header, ...packetRows.map((row, index) => header.map((key) => (key === 'rank' ? index + 1 : row[key])))];
fs.writeFileSync(outCsv, toCsv(csvRows));

const noH034 = nonHRows.filter((row) => row.subtype === '034');
const summary = {
  generated_at: '2026-05-25',
  input_rows: sourceRows.length,
  selected_packet_rows: packetRows.length,
  selected_unique_artifacts: new Set(packetRows.map((row) => row.cisi)).size,
  h_series_excluded: [...hSeries],
  h_series_rows_excluded: sourceRows.filter((row) => hSeries.has(row.cisi)).length,
  frame700_subtype_counts_all: countBy(sourceRows, (row) => row.subtype),
  frame700_subtype_counts_no_h: countBy(nonHRows, (row) => row.subtype),
  packet_counts_by_subtype: countBy(packetRows, (row) => row.subtype),
  packet_counts_by_primary_label: countBy(packetRows, (row) => row.validation_label.split(';')[0]),
  no_h_034_short_text_counts: countBy(noH034, (row) => row.short_text),
  no_h_034_context_class_counts: countBy(noH034, (row) => row.context_class),
  no_h_034_side_relation_counts: countBy(noH034, (row) => row.side_relation),
  no_h_034_h_bin_counts: countBy(noH034, (row) => row.h_bin),
  no_h_034_long_token_set_top: Object.fromEntries(
    Object.entries(countBy(noH034, (row) => row.long_token_set)).slice(0, 15),
  ),
  top_priority_rows: packetRows.slice(0, 20).map((row, index) => ({
    rank: index + 1,
    priority_score: row.priority_score,
    cisi: row.cisi,
    subtype: row.subtype,
    short_text: row.short_text,
    validation_label: row.validation_label,
    why_prioritized: row.why_prioritized,
  })),
  support_threshold:
    'Only claim a validated distributional contrast inside the FRAME700 side-mark formula if source images confirm distinct 034/033/032 signs, direction/side relation, and independence after family-risk downweighting.',
  kill_threshold:
    'Downgrade to object-format association or kill if 034 collapses into 033/032, order is direction-normalized, no-longer rows are incomplete side records, the 002...416 bucket is one copied family, or source dimensions contradict catalog bins.',
  live_public_source_check_2026_05_25: {
    checked_queries: [
      'H-2094 Indus tablet',
      'H-2097 Indus tablet',
      'H-910 Indus tablet',
      'H-307 Indus tablet',
      'site:harappa.com H-2094/H-2097/H-910/H-307',
      'CISI H-2094/H-2097/H-910/H-307',
      '+002-861-416+',
      '700-034 / 034-700 Indus',
    ],
    result:
      'No source-grade object page, plate image, or museum/Harappa archive page surfaced for the top 034 objects; route them to CISI/HARP/plate acquisition.',
  },
  source_check_status: 'packet_for_source_validation_only_source_images_not_validated',
};

fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(
  JSON.stringify(
    {
      outCsv,
      outJson,
      selected_packet_rows: summary.selected_packet_rows,
      selected_unique_artifacts: summary.selected_unique_artifacts,
      packet_counts_by_subtype: summary.packet_counts_by_subtype,
      top_priority: summary.top_priority_rows.slice(0, 5),
    },
    null,
    2,
  ),
);
