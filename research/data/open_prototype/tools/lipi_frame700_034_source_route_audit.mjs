import fs from 'node:fs';
import path from 'node:path';

// For each object in the two-lane source packet, this script answers one practical question:
// through which door can we actually get source-grade images of it? It reads the packet CSV,
// collapses its rows to unique CISI objects, and joins each to a hand-researched route table
// built on 2026-05-25. Every route names a class (Internet Archive OCR hit in the scanned
// CISI volume 1 or 2, a CISI 3.1 library-or-purchase request, a public Harappa.com or
// Kenoyer 1997 Table 2 identity lead, or "source request only" when nothing public
// surfaced), the target volume, a URL, OCR hit counts where applicable, and a note. Output
// is one CSV sorted core-first and one JSON summary with route-class counts. The routes are
// acquisition paths only -- an OCR hit locates a plate, it validates nothing about the
// signs on it.

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const packetPath = path.join(reportsDir, 'lipi_frame700_034_two_lane_source_packet.csv');
const outCsv = path.join(reportsDir, 'lipi_frame700_034_source_route_audit.csv');
const outJson = path.join(reportsDir, 'lipi_frame700_034_source_route_audit_summary.json');

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
  if (rows.length === 0) return '';
  const header = Object.keys(rows[0]);
  const body = rows.map((row) =>
    header
      .map((key) => {
        const text = String(row[key] ?? '');
        return `"${text.replaceAll('"', '""')}"`;
      })
      .join(','),
  );
  return `${[header.map((key) => `"${key}"`).join(','), ...body].join('\n')}\n`;
}

function uniqueSorted(values) {
  return [...new Set(values.filter(Boolean))].sort((a, b) =>
    a.localeCompare(b, undefined, { numeric: true }),
  );
}

function countBy(rows, key) {
  const counts = new Map();
  for (const row of rows) counts.set(row[key], (counts.get(row[key]) ?? 0) + 1);
  return Object.fromEntries(
    [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])),
  );
}

const sources = {
  ia_metadata: 'https://archive.org/metadata/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan',
  ia_reader:
    'https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan',
  harappa_cisi31:
    'https://www.harappa.com/content/corpus-indus-seals-and-inscriptions-vol-31',
  helsinki_cisi31:
    'https://researchportal.helsinki.fi/en/publications/corpus-of-indus-seals-and-inscriptions-volume-3-new-material-untr/',
  cisi_advertisement:
    'https://list.indology.info/pipermail/indology/attachments/20200116/6fb825d1/attachment.pdf',
  harappa_harp: 'https://www.harappa.com/content/harp',
  harappa_inscribed_objects:
    'https://www.harappa.com/content/inscribed-objects-harappa-excavations-1987-2007',
  vats_harappa: 'https://www.harappa.com/content/Excavations-at-Harappa',
  harappa_recent: 'https://www.harappa.com/indus4/e3.html',
  kenoyer_1997:
    'https://www.harappa.com/sites/default/files/pdf/Kenoyer1997_Excavations%20at%20Harappa%201994-1995%20New%20Perspective.pdf',
  icit: 'https://www.epigraphica.de/indus/menueindus.htm',
  parpola_2019:
    'https://tuhat.helsinki.fi/ws/portalfiles/portal/129602857/Parpola_A_2019_Inscriptions_incised_on_the_Harappan_bone_rods_Proceedings_of_EASAA_22.pdf',
};

const routes = {
  'H-1850': {
    route_class: 'cisi_3_1_library_or_purchase_request',
    cisi_volume_target: 'CISI_3_1_Mohenjo-daro_and_Harappa',
    public_evidence_class: 'bibliographic_primary_book_route_only',
    source_route_url: sources.harappa_cisi31,
    route_note: 'HARP excavation hook H2001-5141 and Figure 48.07; no direct public object page found in checked exact searches.',
  },
  'H-1842': {
    route_class: 'cisi_3_1_library_or_purchase_request',
    cisi_volume_target: 'CISI_3_1_Mohenjo-daro_and_Harappa',
    public_evidence_class: 'bibliographic_primary_book_route_only',
    source_route_url: sources.harappa_cisi31,
    route_note: 'HARP excavation hook H95-2416 and Figure 26.07; exact public object search stayed source-dark.',
  },
  'H-1772': {
    route_class: 'cisi_3_1_library_or_purchase_request',
    cisi_volume_target: 'CISI_3_1_Mohenjo-daro_and_Harappa',
    public_evidence_class: 'bibliographic_primary_book_route_only',
    source_route_url: sources.harappa_cisi31,
    route_note: 'HARP excavation hook H2000-4437 and Figure 39.05; route is the 2010 CISI 3.1 volume or archive request.',
  },
  'H-771': {
    route_class: 'internet_archive_cisi_vol1_2_ocr_lead',
    cisi_volume_target: 'CISI_2_Collections_in_Pakistan',
    public_evidence_class: 'public_cisi_ocr_hit_only',
    source_route_url: sources.ia_reader,
    ia_ocr_source: 'CISI_Collections_in_Pakistan_djvu.txt',
    ia_ocr_hits: 4,
    route_note: 'Internet Archive OCR finds H-771 in the CISI Pakistan scan; image-level row still must be checked manually.',
  },
  'H-789': {
    route_class: 'internet_archive_cisi_vol1_2_ocr_lead',
    cisi_volume_target: 'CISI_2_Collections_in_Pakistan',
    public_evidence_class: 'public_cisi_ocr_hit_only',
    source_route_url: sources.ia_reader,
    ia_ocr_source: 'CISI_Collections_in_Pakistan_djvu.txt',
    ia_ocr_hits: 2,
    route_note: 'Internet Archive OCR finds H-789 in the CISI Pakistan scan; use only as a plate locator.',
  },
  'H-1123': {
    route_class: 'cisi_vol2_archive_request_no_public_ocr_hit',
    cisi_volume_target: 'CISI_2_Collections_in_Pakistan',
    public_evidence_class: 'source_request_only',
    source_route_url: sources.ia_metadata,
    ia_ocr_source: 'checked_CISI_vol1_vol2_and_Mahadevan_ocr',
    ia_ocr_hits: 0,
    route_note: 'No exact H-1123 hit in checked IA OCR; source hook 9015360 keeps it in the CISI/HARP/Vats crosswalk request batch.',
  },
  'H-1943': {
    route_class: 'cisi_3_1_library_or_purchase_request',
    cisi_volume_target: 'CISI_3_1_Mohenjo-daro_and_Harappa',
    public_evidence_class: 'bibliographic_primary_book_route_only',
    source_route_url: sources.harappa_cisi31,
    route_note: 'HARP excavation hook H2000-4482 and Figure 42.10; prior CISI-page pointer remains secondary until the plate is consulted.',
  },
  'H-1940': {
    route_class: 'cisi_3_1_library_or_purchase_request',
    cisi_volume_target: 'CISI_3_1_Mohenjo-daro_and_Harappa',
    public_evidence_class: 'bibliographic_primary_book_route_only',
    source_route_url: sources.harappa_cisi31,
    route_note: 'HARP excavation hook H2001-5072 and Figure 44.05; no object-level public source found.',
  },
  'H-854': {
    route_class: 'cisi_vol2_archive_request_no_public_ocr_hit',
    cisi_volume_target: 'CISI_2_Collections_in_Pakistan',
    public_evidence_class: 'source_request_only',
    source_route_url: sources.ia_metadata,
    ia_ocr_source: 'checked_CISI_vol1_vol2_and_Mahadevan_ocr',
    ia_ocr_hits: 0,
    route_note: 'No exact H-854 hit in checked IA OCR; request by CISI ID plus source hook 10010647, with Vats plates checked if CISI vol. 2 points backward.',
  },
  'H-2204': {
    route_class: 'harappa_harp_public_object_lead_plus_cisi_3_1_reconcile',
    cisi_volume_target: 'CISI_3_1_Mohenjo-daro_and_Harappa',
    public_evidence_class: 'direct_public_object_identity_lead',
    source_route_url: sources.harappa_recent,
    route_note: 'Harappa article names H95-2482/4419-05 as an incised steatite tablet; Kenoyer 1997 table also links H95-2482 to H-977-family comparisons. Reconcile against local H-2204/Fig 27.06 before using it.',
  },
  'H-2209': {
    route_class: 'cisi_3_1_library_or_purchase_request',
    cisi_volume_target: 'CISI_3_1_Mohenjo-daro_and_Harappa',
    public_evidence_class: 'bibliographic_primary_book_route_only',
    source_route_url: sources.harappa_cisi31,
    route_note: 'HARP hook H95-2423; no direct public object page found in checked exact searches.',
  },
  'H-2217': {
    route_class: 'cisi_3_1_library_or_purchase_request',
    cisi_volume_target: 'CISI_3_1_Mohenjo-daro_and_Harappa',
    public_evidence_class: 'bibliographic_primary_book_route_only',
    source_route_url: sources.harappa_cisi31,
    route_note: 'HARP hook H95-2521 and Figure 27.09; route is CISI 3.1 or archive request.',
  },
  'H-893': {
    route_class: 'internet_archive_cisi_vol1_2_ocr_lead',
    cisi_volume_target: 'CISI_2_Collections_in_Pakistan',
    public_evidence_class: 'public_cisi_ocr_hit_only',
    source_route_url: sources.ia_reader,
    ia_ocr_source: 'CISI_Collections_in_Pakistan_djvu.txt',
    ia_ocr_hits: 3,
    route_note: 'Internet Archive OCR finds H-893 in the CISI Pakistan scan; route is plate lookup, not validation.',
  },
  'H-925': {
    route_class: 'internet_archive_cisi_vol1_2_ocr_plus_secondary_text_lead',
    cisi_volume_target: 'CISI_2_Collections_in_Pakistan',
    public_evidence_class: 'public_cisi_ocr_hit_plus_secondary_text',
    source_route_url: sources.ia_reader,
    ia_ocr_source: 'CISI_Collections_in_Pakistan_djvu.txt',
    ia_ocr_hits: 7,
    route_note: 'IA OCR finds H-925; Parpola 2019 gives a secondary textual mention useful for request wording only.',
  },
  'H-930': {
    route_class: 'internet_archive_cisi_vol1_2_ocr_lead',
    cisi_volume_target: 'CISI_2_Collections_in_Pakistan',
    public_evidence_class: 'public_cisi_ocr_hit_only',
    source_route_url: sources.ia_reader,
    ia_ocr_source: 'CISI_Collections_in_Pakistan_djvu.txt',
    ia_ocr_hits: 1,
    route_note: 'IA OCR finds H-930 once in the CISI Pakistan scan; needs page/image inspection.',
  },
  'H-1824': {
    route_class: 'cisi_3_1_library_or_purchase_request',
    cisi_volume_target: 'CISI_3_1_Mohenjo-daro_and_Harappa',
    public_evidence_class: 'bibliographic_primary_book_route_only',
    source_route_url: sources.harappa_cisi31,
    route_note: 'HARP hook H95-2434 and Figure 26.10; also carries the uncorrected 060 long-context source-check note.',
  },
  'H-1883': {
    route_class: 'cisi_3_1_library_or_purchase_request',
    cisi_volume_target: 'CISI_3_1_Mohenjo-daro_and_Harappa',
    public_evidence_class: 'bibliographic_primary_book_route_only',
    source_route_url: sources.harappa_cisi31,
    route_note: 'HARP hook H98-3498 and Figure 24.10; no direct public object row found.',
  },
  'H-212': {
    route_class: 'kenoyer_1997_table2_plus_cisi_scan_lead',
    cisi_volume_target: 'CISI_1_or_2_legacy_Harappa_entry',
    public_evidence_class: 'public_table2_identity_lead_plus_cisi_ocr',
    source_route_url: sources.kenoyer_1997,
    ia_ocr_source: 'CISI_Collections_in_India_djvu.txt',
    ia_ocr_hits: 4,
    route_note: 'Kenoyer 1997 Table 2 lists H94-2188 against H-212; IA OCR also finds H-212 in the CISI India scan. Needs exact CISI/Vats plate-side reconciliation.',
  },
  'H-2137': {
    route_class: 'cisi_3_1_library_or_purchase_request',
    cisi_volume_target: 'CISI_3_1_Mohenjo-daro_and_Harappa',
    public_evidence_class: 'bibliographic_primary_book_route_only',
    source_route_url: sources.harappa_cisi31,
    route_note: 'HARP hook H95-2480 and Figure 30.09; route is CISI 3.1 or archive request.',
  },
  'H-983': {
    route_class: 'internet_archive_cisi_vol1_2_ocr_lead',
    cisi_volume_target: 'CISI_2_Collections_in_Pakistan',
    public_evidence_class: 'public_cisi_ocr_hit_only',
    source_route_url: sources.ia_reader,
    ia_ocr_source: 'CISI_Collections_in_Pakistan_djvu.txt',
    ia_ocr_hits: 1,
    route_note: 'IA OCR finds H-983 once in the CISI Pakistan scan; use as plate locator only.',
  },
  'H-353': {
    route_class: 'internet_archive_cisi_vol1_2_ocr_plus_secondary_text_lead',
    cisi_volume_target: 'CISI_1_or_2_legacy_Harappa_entry',
    public_evidence_class: 'public_cisi_ocr_hit_plus_secondary_text',
    source_route_url: sources.ia_reader,
    ia_ocr_source: 'CISI_Collections_in_India_djvu.txt',
    ia_ocr_hits: 4,
    route_note: 'IA OCR finds H-353; Parpola 2019 mentions it only as a secondary textual lead. Images remain decisive.',
  },
  'H-2211': {
    route_class: 'cisi_3_1_library_or_purchase_request',
    cisi_volume_target: 'CISI_3_1_Mohenjo-daro_and_Harappa',
    public_evidence_class: 'bibliographic_primary_book_route_only',
    source_route_url: sources.harappa_cisi31,
    route_note: 'HARP hook H97-3285 and Figure 16.02; no direct public object page found.',
  },
  'H-910': {
    route_class: 'internet_archive_cisi_vol1_2_ocr_lead',
    cisi_volume_target: 'CISI_2_Collections_in_Pakistan',
    public_evidence_class: 'public_cisi_ocr_hit_only',
    source_route_url: sources.ia_reader,
    ia_ocr_source: 'CISI_Collections_in_Pakistan_djvu.txt',
    ia_ocr_hits: 1,
    route_note: 'Optional repeated-branch target; IA OCR finds H-910 once, but repetition pressure keeps it below the core packet.',
  },
  'H-916': {
    route_class: 'kenoyer_1997_table2_public_lead',
    cisi_volume_target: 'CISI_2_Collections_in_Pakistan_with_HARP_comparison',
    public_evidence_class: 'public_table2_identity_lead',
    source_route_url: sources.kenoyer_1997,
    route_note: 'Kenoyer 1997 Table 2 lists H94-2172 / Fig. 10.01 against H-916 and related H95 comparisons. Useful optional branch check, not first evidence.',
  },
  'H-1294': {
    route_class: 'cisi_vol2_archive_request_no_public_ocr_hit',
    cisi_volume_target: 'CISI_2_Collections_in_Pakistan_or_later_addenda',
    public_evidence_class: 'source_request_only',
    source_route_url: sources.ia_metadata,
    ia_ocr_source: 'checked_CISI_vol1_vol2_and_Mahadevan_ocr',
    ia_ocr_hits: 0,
    route_note: 'Optional repeated-branch control with source hook PII-1499; no direct public OCR/object route found in this pass. Check CISI vol. 2/addenda and Vats/PII crosswalk routes.',
  },
};

const packetRows = parseCsv(fs.readFileSync(packetPath, 'utf8'));
const byObject = new Map();
for (const row of packetRows) {
  const cisi = row.cisi;
  if (!byObject.has(cisi)) {
    byObject.set(cisi, {
      cisi,
      priority: row.priority,
      lanes: [],
      roles: [],
      batch_ids: [],
      source_hooks: [],
    });
  }
  const entry = byObject.get(cisi);
  entry.priority = entry.priority === 'core' || row.priority === 'core' ? 'core' : 'optional';
  entry.lanes.push(row.lane);
  entry.roles.push(row.role);
  entry.batch_ids.push(row.batch_id);
  entry.source_hooks.push(row.source_hooks);
}

const outRows = [...byObject.values()]
  .map((entry) => {
    const route = routes[entry.cisi];
    if (!route) throw new Error(`Missing route for ${entry.cisi}`);
    return {
      checked_date: '2026-05-25',
      cisi: entry.cisi,
      priority: entry.priority,
      lanes: uniqueSorted(entry.lanes).join(';'),
      roles: uniqueSorted(entry.roles).join(';'),
      batch_ids: uniqueSorted(entry.batch_ids).join(';'),
      packet_source_hooks: uniqueSorted(entry.source_hooks).join(';'),
      route_class: route.route_class,
      public_evidence_class: route.public_evidence_class,
      cisi_volume_target: route.cisi_volume_target,
      source_route_url: route.source_route_url,
      ia_ocr_source: route.ia_ocr_source ?? '',
      ia_ocr_hits: route.ia_ocr_hits ?? '',
      source_action: route.source_action ?? 'inspect_or_request_source_images_before_coding_sheet',
      route_note: route.route_note,
      accepted_decipherment_claim: '0',
    };
  })
  .sort((a, b) => {
    if (a.priority !== b.priority) return a.priority === 'core' ? -1 : 1;
    return a.cisi.localeCompare(b.cisi, undefined, { numeric: true });
  });

const summary = {
  checked_date: '2026-05-25',
  question:
    'Which currently visible source-acquisition route exists for each FRAME700_034 two-lane packet object?',
  packet_objects: outRows.length,
  core_objects: outRows.filter((row) => row.priority === 'core').length,
  optional_objects: outRows.filter((row) => row.priority === 'optional').length,
  route_class_counts: countBy(outRows, 'route_class'),
  public_evidence_class_counts: countBy(outRows, 'public_evidence_class'),
  cisi_volume_target_counts: countBy(outRows, 'cisi_volume_target'),
  ia_ocr_hit_objects: outRows.filter((row) => Number(row.ia_ocr_hits) > 0).length,
  ia_ocr_hit_total: outRows.reduce((sum, row) => sum + (Number(row.ia_ocr_hits) || 0), 0),
  direct_or_table_public_identity_leads: outRows.filter((row) =>
    ['direct_public_object_identity_lead', 'public_table2_identity_lead', 'public_table2_identity_lead_plus_cisi_ocr'].includes(
      row.public_evidence_class,
    ),
  ).length,
  secondary_textual_lead_objects: outRows.filter((row) =>
    row.public_evidence_class.includes('secondary_text'),
  ).length,
  source_request_only_objects: outRows.filter((row) => row.public_evidence_class === 'source_request_only')
    .length,
  accepted_decipherment_claims: 0,
  immediate_next_action:
    'Use the route audit to fill or request the 51-row two-lane source coding sheet; do not upgrade 034 until source images decide sign visibility, side order, direction, and copy pressure.',
  sources,
};

fs.mkdirSync(reportsDir, { recursive: true });
fs.writeFileSync(outCsv, toCsv(outRows));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
