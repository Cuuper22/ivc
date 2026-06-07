import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const targetsPath = path.join(reportsDir, 'lipi_034_mayig_acquisition_priority_objects.csv');

const leadsOut = path.join(reportsDir, 'lipi_034_p0_public_leads.csv');
const summaryOut = path.join(reportsDir, 'lipi_034_p0_public_leads_summary.json');

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

const priorityObjects = csvObjects(fs.readFileSync(targetsPath, 'utf8'));
const p0Objects = priorityObjects.filter(
  (row) => row.max_priority_lane === 'P0_mohenjo_034_missing_from_current_mayig',
);
const p0ByCisi = new Map(p0Objects.map((row) => [row.cisi, row]));

const leadRows = [
  {
    cisi: 'M-2104',
    public_lead_grade: 'B_object_level_prior_work',
    lead_status: 'object_level_public_hit',
    lead_source: 'Parpola 2019, Inscriptions Incised on the Harappan Ivory/Bone Rods',
    lead_url:
      'https://tuhat.helsinki.fi/ws/portalfiles/portal/129602857/Parpola_A_2019_Inscriptions_incised_on_the_Harappan_bone_rods_Proceedings_of_EASAA_22.pdf',
    lead_detail:
      'Mentions text no. 12 (M-2104), compares it with M-478, M-480, and M-1425, and gives standardized signs/direction in Fig. 1.',
    source_line_or_page: 'Parpola 2019 PDF p. 2 text; Fig. 1 caption on same page',
    extracted_public_data:
      'Text no. 12 is M-2104. Parpola describes the rod text as beginning with UIII (three pots), followed by signs 15 and 1; the tablet parallels M-478, M-480, and M-1425 begin with UIIII (four pots), followed by signs 15 and 107.',
    usable_for_crosswalk: 'partial_prior_sign_system_only',
    next_action: 'Extract Parpola sign numbers for text no. 12 and compare against lipi +151-097-700-034+ without accepting a mapping.',
  },
  {
    cisi: 'M-315',
    public_lead_grade: 'B_source_visible_followup',
    lead_status: 'object_level_image_lead',
    lead_source: 'Kenoyer and Meadow 2010, Inscribed Objects from Harappa Excavations 1986-2007',
    lead_url:
      'https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India/page/n113/mode/1up',
    lead_detail:
      'Kenoyer/Meadow routes M-315 to CISI 1 p. 78; follow-up inspection of IA CISI Vol. 1 leaf n113 labels M-315 A/a and leaf n403 shows the M-315 data row.',
    source_line_or_page: 'CISI Vol. 1 printed p. 78 / IA leaf n113; data p. 368 / IA leaf n403',
    extracted_public_data:
      'CISI p. 78 labels M-315 A and M-315 a under MOHENJO-DARO 313-317 SEALS / no iconography; silver. CISI p. 368 shows M-315 1395 VS 1190 ASI 63.10.117 HU 318. Numeric sign mapping remains unaccepted.',
    usable_for_crosswalk: 'source_visible_object_binding_only',
    next_action: 'Use the M-315 source probe; high-resolution/source-transcription request sent as gmail:[redacted-msgid] to verify direction, sign-list convention, and VS1190/1395 vs local VS1190395.',
  },
  {
    cisi: 'M-1206',
    public_lead_grade: 'B_image_lead_secondary',
    lead_status: 'object_level_image_lead',
    lead_source: 'Bhaskar 2022, Indus zoomorphism and its avatars',
    lead_url: 'https://www.harappa.com/sites/default/files/pdf/Bhaskar2022_IJHS_57_3_1.pdf',
    lead_detail:
      'Figure 3 caption identifies M-1206 and says images are from CISI; useful image lead, not a sign crosswalk.',
    source_line_or_page: 'Bhaskar 2022 PDF p. 18, Fig. 3 caption',
    extracted_public_data:
      'Fig. 3 identifies M-1206 as the right-hand image in a two-object figure with M-635 and states that the images are from CISI; no sign transcription is supplied.',
    usable_for_crosswalk: 'source_image_lead_only',
    next_action: 'Inspect Fig. 3 visually for object identity and request underlying CISI image/record for sign-level mapping.',
  },
  {
    cisi: 'M-685',
    public_lead_grade: 'B_source_visible_followup',
    lead_status: 'object_level_image_lead',
    lead_source: 'CISI Vol. 2 IA leaf n71 plus Bhaskar 2022 supplemental S1 catalogue',
    lead_url:
      'https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/n71/mode/1up',
    lead_detail:
      'Follow-up inspection of IA CISI Vol. 2 leaf n71 labels M-685 A/a under unicorn II / SEALS / MOHENJO-DARO 683-686; Bhaskar S1 independently lists M-685 as text-present marker b Unicorn.',
    source_line_or_page: 'CISI Vol. 2 printed p. 37 / IA leaf n71; Bhaskar 2022 S1 extracted table row',
    extracted_public_data:
      'CISI p.37 labels M-685 A and M-685 a; Bhaskar S1 lists M-685 with a text-present checkmark, marker b, and Unicorn. Local row is fragmentary ]034-204+ and local iconography Bull1 conflicts with the source/secondary Unicorn route.',
    usable_for_crosswalk: 'source_visible_object_binding_only',
    next_action: 'Use the M-685 source probe; high-resolution/source-transcription request sent as gmail:[redacted-msgid] to verify direction, ]034-204+ token convention, HR4244276 bridge, and iconography conflict.',
  },
  {
    cisi: 'M-1584',
    public_lead_grade: 'D_no_public_object_hit',
    lead_status: 'no_relevant_public_hit_in_checked_queries',
    lead_source: 'checked web queries',
    lead_url: '',
    lead_detail:
      'No relevant object-level public hit found in checked queries for M-1584 / CISI / Mohenjo-daro / Indus.',
    source_line_or_page: 'public web exact-object queries, 2026-05-25',
    extracted_public_data: 'No public source datum extracted.',
    usable_for_crosswalk: 'no',
    next_action: 'Resolve via CISI/HARP/local corpus source route; this is a pottery single-sign row, not first structural evidence.',
  },
  {
    cisi: 'M-1963',
    public_lead_grade: 'D_no_public_object_hit',
    lead_status: 'no_relevant_public_hit_in_checked_queries',
    lead_source: 'checked web queries',
    lead_url: '',
    lead_detail:
      'No relevant object-level public hit found in checked queries for M-1963 / CISI / Mohenjo-daro / Indus.',
    source_line_or_page: 'public web exact-object queries, 2026-05-25',
    extracted_public_data: 'No public source datum extracted.',
    usable_for_crosswalk: 'no',
    next_action: 'Request CISI 3.1 or HARP/Mohenjo-daro catalogue data; row contains uncertainty token 000 in lipi.',
  },
].map((lead) => {
  const target = p0ByCisi.get(lead.cisi) ?? {};
  return {
    checked_date: checkedDate,
    cisi: lead.cisi,
    p0_text: target.texts ?? '',
    p0_priority_score: target.max_priority_score ?? '',
    public_lead_grade: lead.public_lead_grade,
    lead_status: lead.lead_status,
    lead_source: lead.lead_source,
    lead_url: lead.lead_url,
    lead_detail: lead.lead_detail,
    source_line_or_page: lead.source_line_or_page,
    extracted_public_data: lead.extracted_public_data,
    usable_for_crosswalk: lead.usable_for_crosswalk,
    next_action: lead.next_action,
    accepted_decipherment_claim: '0',
  };
});

const summary = {
  checked_date: checkedDate,
  artifact: 'lipi_034_p0_public_lead_search',
  question:
    'Do the six P0 Mohenjo-daro 034 crosswalk-acquisition targets have public object/source leads?',
  inputs: [path.relative(base, targetsPath).replaceAll('\\', '/')],
  checked_queries: [
    '"M-2104" "Indus Script"',
    '"M-2104" "CISI"',
    '"M-315" "Indus Script"',
    '"M-315" "CISI"',
    '"M-1206" "Indus Script"',
    '"M-685" "CISI"',
    '"S1-IndusZoomorphicIconCatalogue.pdf" "M-685"',
    '"M-1584" "CISI" "Indus"',
    '"M-1963" "CISI" "Indus"',
  ],
  p0_target_count: p0Objects.length,
  public_lead_rows: leadRows.length,
  lead_status_counts: countBy(leadRows, (row) => row.lead_status),
  lead_grade_counts: countBy(leadRows, (row) => row.public_lead_grade),
  object_level_or_image_leads: leadRows
    .filter((row) => ['object_level_public_hit', 'object_level_image_lead'].includes(row.lead_status))
    .map((row) => row.cisi)
    .join(';'),
  extractable_prior_sign_data_objects: leadRows
    .filter((row) => row.usable_for_crosswalk === 'partial_prior_sign_system_only')
    .map((row) => row.cisi)
    .join(';'),
  public_image_lead_objects: leadRows
    .filter((row) => ['source_image_lead_only', 'source_visible_object_binding_only'].includes(row.usable_for_crosswalk))
    .map((row) => row.cisi)
    .join(';'),
  route_or_catalogue_leads: leadRows
    .filter((row) => ['source_route_public_hit', 'catalogue_public_hit'].includes(row.lead_status))
    .map((row) => row.cisi)
    .join(';'),
  no_relevant_public_hit_objects: leadRows
    .filter((row) => row.lead_status === 'no_relevant_public_hit_in_checked_queries')
    .map((row) => row.cisi)
    .join(';'),
  conclusion:
    'Public search gives usable leads for M-2104, M-315, M-1206, and M-685, but none yet yields an accepted 034 mapping. M-1584 and M-1963 remain direct source-request targets.',
  outputs: [
    path.relative(base, leadsOut).replaceAll('\\', '/'),
    path.relative(base, summaryOut).replaceAll('\\', '/'),
  ],
  accepted_decipherment_claims: 0,
};

fs.writeFileSync(leadsOut, toCsv(leadRows), 'utf8');
fs.writeFileSync(summaryOut, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
