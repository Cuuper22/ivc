// Final planning step for the 17-artifact plate packet: merge the request
// packet with the public-lead search results and decide, artifact by
// artifact, where to go get a usable image. The web scout showed which
// tablets have candidate public images, which have only text mentions, and
// which are "source dark"; that determines whether the next move is a
// recheck, a manual image inspection, or a direct archive request.
//
// The script reads lipi_short_mark_plate_request_packet.csv and
// lipi_short_mark_plate_public_leads.csv, summarizes each artifact's lead
// status, and assigns an acquisition bucket: A-buckets for six named
// special cases (H-1302/H-1303 direction-note rechecks, the H-355 double
// short side, the H-933/H-960 034-contrast pair, and the H-233 TAB:B control
// with public slide leads), B for artifacts with no public lead (go straight
// to CISI/HARP archives), C for replicate 033-after cases. Each row carries a
// written action, the evidence checklist needed to fill the packet, and its
// known validation risks.
//
// Outputs: lipi_short_mark_source_acquisition_queue.csv (ranked) and
// _summary.json. Acquisition planning only; nothing here reads the signs.

import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const packetCsv = path.join(reportsDir, 'lipi_short_mark_plate_request_packet.csv');
const publicLeadsCsv = path.join(reportsDir, 'lipi_short_mark_plate_public_leads.csv');
const outCsv = path.join(reportsDir, 'lipi_short_mark_source_acquisition_queue.csv');
const outJson = path.join(reportsDir, 'lipi_short_mark_source_acquisition_summary.json');

const checkedAt = '2026-05-24';

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

function leadSummary(leads) {
  const kinds = uniqueSorted(leads.map((lead) => lead.lead_kind));
  const sourceUrls = uniqueSorted(leads.map((lead) => lead.source_url));
  const imageUrls = uniqueSorted(leads.map((lead) => lead.image_url));
  const tiers = uniqueSorted(leads.map((lead) => lead.source_tier));
  return {
    kinds,
    sourceUrls,
    imageUrls,
    tiers,
  };
}

function statusFromLeads(leads) {
  const kinds = new Set(leads.map((lead) => lead.lead_kind));
  if (kinds.has('published_direction_or_corpus_note') && kinds.has('artifact_mention_with_candidate_images')) {
    return 'candidate_image_plus_published_direction_note';
  }
  if (kinds.has('artifact_mention_with_candidate_images')) {
    return 'candidate_public_image_or_post_lead';
  }
  if (kinds.has('text_only_or_bibliographic_lead')) {
    return 'text_only_or_bibliographic_public_lead';
  }
  return 'no_public_lead_in_checked_sources';
}

function acquisitionBucket(row, leadStatus) {
  if (['H-1302', 'H-1303'].includes(row.cisi)) return 'A_direction_note_recheck';
  if (row.cisi === 'H-355') return 'A_double_short_side_case';
  if (['H-933', 'H-960'].includes(row.cisi)) return 'A_034_contrast_case';
  if (row.cisi === 'H-233') return 'A_tab_b_type_control_with_public_image_lead';
  if (leadStatus === 'no_public_lead_in_checked_sources') return 'B_source_dark_direct_cisi_or_harp';
  return 'C_replicate_033_after_case';
}

function acquisitionAction(row, leadStatus) {
  const baseAction =
    `Request plate or source image for ${row.cisi} showing all ${row.sides} catalog side rows; verify ${row.short_side_texts} and ${row.longer_texts}.`;
  if (['H-1302', 'H-1303'].includes(row.cisi)) {
    return `${baseAction} Cross-check the published direction/corpus-note lead against CISI/HARP image evidence.`;
  }
  if (row.cisi === 'H-355') {
    return `${baseAction} Confirm whether both short rows are distinct physical sides or duplicate/catalog artifacts.`;
  }
  if (['H-933', 'H-960'].includes(row.cisi)) {
    return `${baseAction} Prioritize the 034-before relation because these are the two packet contrast cases.`;
  }
  if (row.cisi === 'H-233') {
    return `${baseAction} Manually inspect the public H-233 slide leads only as acquisition pointers, then verify against a plate-grade source.`;
  }
  if (leadStatus === 'no_public_lead_in_checked_sources') {
    return `${baseAction} Skip broad public search for now and go straight to CISI, HARP, Harappa image archives, or library plate access.`;
  }
  return `${baseAction} Use public text-only lead only as a bibliographic pointer; source-grade validation still requires plates or archive images.`;
}

function requiredEvidence(row) {
  const items = [
    'source citation or image/plate ID',
    'catalog rows are distinct physical sides or source explains side convention',
    'side order basis is physical, photographic, editorial, or arbitrary',
    'short-mark direction basis is inscription, impression, catalog-normalized, or unresolved',
    `short mark visible enough to check ${row.short_side_texts}`,
    `longer text visible enough to check ${row.longer_texts}`,
    '033/034 contrast visibility recorded',
    'relation survives or fails after image-side check',
  ];
  if (row.cisi === 'H-355') items.push('both short rows checked separately');
  if (['H-1302', 'H-1303'].includes(row.cisi)) items.push('published direction/corpus-note claim reconciled with source image');
  return items.join('; ');
}

function validationRisk(row, leadStatus) {
  const risks = [];
  if (leadStatus.includes('candidate')) risks.push('public images are claim-heavy or copied and not source-grade');
  if (leadStatus === 'text_only_or_bibliographic_public_lead') risks.push('public evidence is text-only');
  if (leadStatus === 'no_public_lead_in_checked_sources') risks.push('no checked public lead');
  if (row.cisi === 'H-355') risks.push('duplicate short rows in packet');
  if (['H-933', 'H-960'].includes(row.cisi)) risks.push('contrast class depends on 034 side relation');
  if (['H-1302', 'H-1303'].includes(row.cisi)) risks.push('published direction/corpus-note lead may expose catalog direction issue');
  if (row.vertical_mm === '0' || row.horizontal_mm === '0' || row.thickness_mm === '0') {
    risks.push('one or more local dimensions recorded as zero');
  }
  return risks.join('; ');
}

function rankBucket(bucket) {
  const order = {
    A_direction_note_recheck: 1,
    A_double_short_side_case: 2,
    A_034_contrast_case: 3,
    A_tab_b_type_control_with_public_image_lead: 4,
    B_source_dark_direct_cisi_or_harp: 5,
    C_replicate_033_after_case: 6,
  };
  return order[bucket] ?? 99;
}

const packetRows = parseCsv(fs.readFileSync(packetCsv, 'utf8'));
const publicLeadRows = parseCsv(fs.readFileSync(publicLeadsCsv, 'utf8'));

const leadsByCisi = new Map();
for (const lead of publicLeadRows) {
  if (!leadsByCisi.has(lead.cisi)) leadsByCisi.set(lead.cisi, []);
  leadsByCisi.get(lead.cisi).push(lead);
}

const artifactRows = packetRows.map((row) => {
  const leads = leadsByCisi.get(row.cisi) ?? [];
  const summary = leadSummary(leads);
  const leadStatus = statusFromLeads(leads);
  const bucket = acquisitionBucket(row, leadStatus);
  return {
    cisi: row.cisi,
    type: row.type,
    site: row.site,
    packet_priority: row.priority,
    acquisition_bucket: bucket,
    public_lead_status: leadStatus,
    sides: row.sides,
    row_count_in_packet: row.row_count_in_packet,
    short_side_texts: row.short_side_texts,
    short_orders: row.short_orders,
    side_relations: row.side_relations,
    longer_texts: row.longer_texts,
    group_signature: row.group_signature,
    raw_ids: row.raw_ids,
    excavation_ids: row.excavation_ids,
    dimensions_mm: `${row.horizontal_mm} x ${row.vertical_mm} x ${row.thickness_mm}`,
    public_lead_kinds: summary.kinds.join(';'),
    public_source_urls: summary.sourceUrls.join(';'),
    candidate_image_urls: summary.imageUrls.join(';'),
    source_tiers_seen: summary.tiers.join(';'),
    acquisition_action: acquisitionAction(row, leadStatus),
    required_evidence_to_fill_packet: requiredEvidence(row),
    validation_risk: validationRisk(row, leadStatus),
    interpretation_status: 'source_acquisition_only_no_reading',
  };
});

artifactRows.sort(
  (a, b) =>
    rankBucket(a.acquisition_bucket) - rankBucket(b.acquisition_bucket) ||
    a.cisi.localeCompare(b.cisi, undefined, { numeric: true }),
);

const csvRows = [
  [
    'rank',
    'cisi',
    'type',
    'site',
    'packet_priority',
    'acquisition_bucket',
    'public_lead_status',
    'sides',
    'row_count_in_packet',
    'short_side_texts',
    'short_orders',
    'side_relations',
    'longer_texts',
    'group_signature',
    'raw_ids',
    'excavation_ids',
    'dimensions_mm',
    'public_lead_kinds',
    'public_source_urls',
    'candidate_image_urls',
    'source_tiers_seen',
    'acquisition_action',
    'required_evidence_to_fill_packet',
    'validation_risk',
    'interpretation_status',
  ],
  ...artifactRows.map((row, index) => [
    index + 1,
    row.cisi,
    row.type,
    row.site,
    row.packet_priority,
    row.acquisition_bucket,
    row.public_lead_status,
    row.sides,
    row.row_count_in_packet,
    row.short_side_texts,
    row.short_orders,
    row.side_relations,
    row.longer_texts,
    row.group_signature,
    row.raw_ids,
    row.excavation_ids,
    row.dimensions_mm,
    row.public_lead_kinds,
    row.public_source_urls,
    row.candidate_image_urls,
    row.source_tiers_seen,
    row.acquisition_action,
    row.required_evidence_to_fill_packet,
    row.validation_risk,
    row.interpretation_status,
  ]),
];

const byBucket = Object.fromEntries(
  uniqueSorted(artifactRows.map((row) => row.acquisition_bucket)).map((bucket) => [
    bucket,
    artifactRows.filter((row) => row.acquisition_bucket === bucket).map((row) => row.cisi),
  ]),
);
const byLeadStatus = Object.fromEntries(
  uniqueSorted(artifactRows.map((row) => row.public_lead_status)).map((status) => [
    status,
    artifactRows.filter((row) => row.public_lead_status === status).map((row) => row.cisi),
  ]),
);

const summary = {
  source: '17-artifact short-mark source acquisition queue',
  checked_at: checkedAt,
  input_packet: path.relative(base, packetCsv).replaceAll('\\', '/'),
  input_public_leads: path.relative(base, publicLeadsCsv).replaceAll('\\', '/'),
  queue_artifacts: artifactRows.length,
  bucket_counts: Object.fromEntries(Object.entries(byBucket).map(([bucket, values]) => [bucket, values.length])),
  public_lead_status_counts: Object.fromEntries(
    Object.entries(byLeadStatus).map(([status, values]) => [status, values.length]),
  ),
  acquisition_buckets: byBucket,
  public_lead_status_artifacts: byLeadStatus,
  first_actions: artifactRows.slice(0, 6).map((row) => ({
    cisi: row.cisi,
    acquisition_bucket: row.acquisition_bucket,
    acquisition_action: row.acquisition_action,
  })),
  key_observation:
    'The first acquisition queue should start with H-1302/H-1303 direction-note rechecks, H-355 double-short-side clarification, H-933/H-960 034 contrast cases, and H-233 as the TAB:B type-control with public slide leads.',
  interpretation_boundary:
    'This queue is for source acquisition only. It accepts no side relation, physical side function, numerical value, metrological reading, sign meaning, phonetic value, language identity, or translation.',
  outputs: [path.relative(base, outCsv).replaceAll('\\', '/')],
};

fs.writeFileSync(outCsv, toCsv(csvRows));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
