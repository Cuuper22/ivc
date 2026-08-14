// Accession-level audit of the Gadd 1932 Ur seals: can any local Indus row be
// tied to a specific published museum object, and does any such object carry
// both an Indus sign sequence and readable cuneiform? A hand-modeled table of
// eight Gadd/BM/Penn objects (with museum numbers, plate references, findspots,
// and what each surface actually shows) is checked against the Ur rows of
// external_indus_objects.csv and the lipi metadata. Two mappings are verified by
// excavation ID (3898.1 = U.17649, 3899.1 = U.8685); the rest are candidates or
// unmapped fragments. The key asymmetry the audit documents: every Indus-
// inscribed object lacks readable cuneiform, and the one cuneiform-inscribed
// object (BM 120573) lacks any recorded Indus sequence — so no micro-bilingual
// exists and zero external phonetic anchors are accepted. Writes an audit CSV
// and a JSON summary with next acquisition steps.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const EXTERNAL_OBJECTS = path.join(ROOT, 'data/meluhha/external_indus_objects.csv');
const LIPI_METADATA = path.join(ROOT, 'data/open_prototype/lipi/metadata_filtered.csv');
const OUT_CSV = path.join(ROOT, 'data/meluhha/gadd_ur_accession_bridge_audit.csv');
const OUT_JSON = path.join(ROOT, 'data/meluhha/gadd_ur_accession_bridge_audit_summary.json');

const DATE = new Date().toISOString().slice(0, 10);

function csvEscape(value) {
  const text = String(value ?? '');
  if (/[",\n\r]/.test(text)) return `"${text.replaceAll('"', '""')}"`;
  return text;
}

function parseCsv(text) {
  const rows = [];
  let row = [];
  let value = '';
  let quoted = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (ch === '"' && next === '"') {
        value += '"';
        i++;
      } else if (ch === '"') {
        quoted = false;
      } else {
        value += ch;
      }
    } else if (ch === '"') {
      quoted = true;
    } else if (ch === ',') {
      row.push(value);
      value = '';
    } else if (ch === '\n') {
      row.push(value.replace(/\r$/, ''));
      rows.push(row);
      row = [];
      value = '';
    } else {
      value += ch;
    }
  }
  if (value.length || row.length) {
    row.push(value.replace(/\r$/, ''));
    rows.push(row);
  }
  const [header, ...body] = rows.filter(r => r.some(cell => cell.length));
  return body.map(cols => Object.fromEntries(header.map((h, idx) => [h, cols[idx] ?? ''])));
}

const sources = {
  gadd_pdf_url: 'https://ignca.gov.in/Asi_data/33779.pdf',
  gadd_pdf_local: 'tmp/gadd_ur/gadd_1932_33779.pdf',
  gadd_contact_sheet_10_24: 'tmp/gadd_ur/pages_10_24_contact.jpg',
  gadd_contact_sheet_22_34: 'tmp/gadd_ur/pages_22_34_contact.jpg',
  bm_bibliography_url: 'https://www.britishmuseum.org/collection/term/BIB2877',
  penn_woolley_1933_url: 'https://www.penn.museum/sites/journal/9405/',
};

const gaddObjects = [
  {
    object_key: 'gadd_no_01_bm_120573_u7683',
    gadd_no: '1',
    plate_ref: 'I:1',
    museum_or_collection: 'British Museum',
    museum_number: '120573',
    registration_or_excavation: '1928,1009.56 / U.7683',
    findspot: 'Diqdiqqah (Ur), surface',
    shape: 'rectangular',
    iconography: 'bull standing/facing left',
    inscription_surface: 'single line of archaic cuneiform / Sumerian according to BM and Gadd',
    has_indus_sequence: false,
    has_readable_cuneiform: true,
    cuneiform_reading_status: 'doubtful; provisional ASCII sak-ku-shi-?',
    local_row_link: 'not a local Indus numeric row',
    bridge_verdict: 'rejected_cuneiform_only_not_indus_sequence',
    evidence_note: 'BM/Gadd expose cuneiform only; no Indus sign sequence is recorded on this object.',
  },
  {
    object_key: 'gadd_no_02_bm_122187_candidate_3897',
    gadd_no: '2',
    plate_ref: 'I:2',
    museum_or_collection: 'British Museum',
    museum_number: '122187',
    registration_or_excavation: '1929,1017.725',
    findspot: 'Ur, obtained in 1928-1929 season; exact findspot not evidenced in Gadd',
    shape: 'circular',
    iconography: 'short-horned bull facing right, lowered head',
    inscription_surface: 'Indus inscription of five characters above bull',
    has_indus_sequence: true,
    has_readable_cuneiform: false,
    cuneiform_reading_status: 'none',
    local_row_link: 'candidate for 3897.1 only: Ur circular Gaur, five-sign row, no local excavation id',
    bridge_verdict: 'candidate_row_mapping_only_no_cuneiform',
    evidence_note: 'Shape/site/icon/text-length are compatible with local 3897.1, but no accession link is present in local metadata and there is no cuneiform/name bridge.',
  },
  {
    object_key: 'gadd_no_03_bm_122946_u17342',
    gadd_no: '3',
    plate_ref: 'I:3',
    museum_or_collection: 'British Museum',
    museum_number: '122946',
    registration_or_excavation: '1931,1010.14 / U.17342',
    findspot: 'Ur, 1930-1931 season; exact context not given in BM surface',
    shape: 'circular fragment',
    iconography: 'part of incised design',
    inscription_surface: 'part of Indus inscription/design on base',
    has_indus_sequence: true,
    has_readable_cuneiform: false,
    cuneiform_reading_status: 'none',
    local_row_link: 'no exact local row mapping; possible fragment lane only',
    bridge_verdict: 'source_route_only_no_cuneiform',
    evidence_note: 'Real Gadd/BM object route but no current row-level local mapping and no cuneiform/name bridge.',
  },
  {
    object_key: 'gadd_no_04_bm_122188',
    gadd_no: '4',
    plate_ref: 'I:4',
    museum_or_collection: 'British Museum',
    museum_number: '122188',
    registration_or_excavation: '1929,1017.726',
    findspot: 'Ur',
    shape: 'circular fragment',
    iconography: 'illegible design / animal head in Gadd and BM summaries',
    inscription_surface: 'fragmentary Indus inscription; only a first sign and part of another preserved in Gadd description',
    has_indus_sequence: true,
    has_readable_cuneiform: false,
    cuneiform_reading_status: 'none',
    local_row_link: 'no exact local row mapping; possible 5231.1-style fragment lane only',
    bridge_verdict: 'source_route_only_no_cuneiform',
    evidence_note: 'Publication route exists but lacks local accession mapping and cuneiform/name evidence.',
  },
  {
    object_key: 'gadd_no_15_upenn_u8685_row_3899',
    gadd_no: '15',
    plate_ref: 'III:15',
    museum_or_collection: 'University Museum of Pennsylvania',
    museum_number: '',
    registration_or_excavation: 'U.8685',
    findspot: 'Ur, 1926-1927 season; cemetery ruined grave ca. 9m below surface in Gadd',
    shape: 'circular',
    iconography: 'animal figure / Gulf-type ambiguity',
    inscription_surface: 'crowded, indistinct Indus-like inscription according to Gadd',
    has_indus_sequence: true,
    has_readable_cuneiform: false,
    cuneiform_reading_status: 'none',
    local_row_link: 'verified accession match to 3899.1 through local excavation-idno U8685',
    bridge_verdict: 'mapped_local_row_no_cuneiform',
    evidence_note: 'Object identity is real, but it has no readable cuneiform, owner, title, or Meluhha tag.',
  },
  {
    object_key: 'gadd_no_16_upenn_u17649_row_3898',
    gadd_no: '16',
    plate_ref: 'III:16 / Penn Museum Journal Plate XXX:2',
    museum_or_collection: 'University Museum of Pennsylvania',
    museum_number: '',
    registration_or_excavation: 'U.17649',
    findspot: 'Ur grave PG/1848 shaft fill / brick packing surface per Woolley 1933',
    shape: 'circular',
    iconography: 'buffalo / bull without manger',
    inscription_surface: 'Mohenjo-daro type inscription',
    has_indus_sequence: true,
    has_readable_cuneiform: false,
    cuneiform_reading_status: 'none',
    local_row_link: 'verified accession match to 3898.1 through local excavation-idno U17649',
    bridge_verdict: 'mapped_local_row_no_cuneiform',
    evidence_note: 'Best Ur object identity bridge in the current workspace, but the object is Indus-inscribed only and its nearby U.17650/U.17653 finds do not provide a name/date bridge.',
  },
  {
    object_key: 'gadd_no_17_bm_120228_babylon',
    gadd_no: '17',
    plate_ref: 'III:17',
    museum_or_collection: 'British Museum',
    museum_number: '120228',
    registration_or_excavation: '1883,1116.1',
    findspot: 'Babylon',
    shape: 'circular',
    iconography: 'bull standing over manger',
    inscription_surface: 'Indus inscription along top',
    has_indus_sequence: true,
    has_readable_cuneiform: false,
    cuneiform_reading_status: 'none',
    local_row_link: 'outside current Ur local row set; Babylon route',
    bridge_verdict: 'external_indus_only_no_cuneiform',
    evidence_note: 'Important external object route, but not cuneiform-bilingual and not tied to a local row in this audit.',
  },
  {
    object_key: 'gadd_no_18_bm_123059_baghdad_dealer',
    gadd_no: '18',
    plate_ref: 'III:18',
    museum_or_collection: 'British Museum',
    museum_number: '123059',
    registration_or_excavation: '1932,0308.1',
    findspot: 'acquired via Baghdad dealer route, not excavated context',
    shape: 'circular',
    iconography: 'figures, animal, damaged face',
    inscription_surface: 'damaged engraving; Gadd notes five characters but no cuneiform',
    has_indus_sequence: true,
    has_readable_cuneiform: false,
    cuneiform_reading_status: 'none',
    local_row_link: 'outside current Ur local row set',
    bridge_verdict: 'unprovenanced_external_indus_only_no_cuneiform',
    evidence_note: 'No object-level cuneiform or name bridge.',
  },
];

const rows = parseCsv(fs.readFileSync(EXTERNAL_OBJECTS, 'utf8'));
const metadataRows = parseCsv(fs.readFileSync(LIPI_METADATA, 'utf8'));
const urRows = rows.filter(row => row.region === 'Mesopotamia' && row.site === 'Ur');
const rowsById = new Map(rows.map(row => [row.row_id, row]));
const metadataById = new Map(metadataRows.map(row => [row.id, row]));

const localChecks = [
  {
    local_row_id: '3898.1',
    mapped_object_key: 'gadd_no_16_upenn_u17649_row_3898',
    mapping_strength: 'verified_by_excavation_id',
  },
  {
    local_row_id: '3899.1',
    mapped_object_key: 'gadd_no_15_upenn_u8685_row_3899',
    mapping_strength: 'verified_by_excavation_id',
  },
  {
    local_row_id: '3897.1',
    mapped_object_key: 'gadd_no_02_bm_122187_candidate_3897',
    mapping_strength: 'candidate_by_site_shape_icon_text_length_only',
  },
  {
    local_row_id: '5225.1',
    mapped_object_key: '',
    mapping_strength: 'unmapped_fragment',
  },
  {
    local_row_id: '5231.1',
    mapped_object_key: 'gadd_no_04_bm_122188',
    mapping_strength: 'weak_fragment_candidate_only',
  },
];

const gaddByKey = new Map(gaddObjects.map(obj => [obj.object_key, obj]));
const auditRows = localChecks.map(check => {
  const local = rowsById.get(check.local_row_id) ?? {};
  const metadata = metadataById.get(check.local_row_id) ?? {};
  const obj = gaddByKey.get(check.mapped_object_key) ?? {};
  const hasObject = Boolean(obj.object_key);
  const verdict = hasObject && obj.has_indus_sequence && obj.has_readable_cuneiform
    ? 'candidate_micro_bilingual_requires_forger'
    : hasObject
      ? obj.bridge_verdict
      : 'unmapped_local_row_no_object_bridge';
  return {
    local_row_id: check.local_row_id,
    local_excavation_idno: metadata['excavation-idno'] ?? '',
    local_site: local.site ?? '',
    local_type: local.type ?? '',
    local_shape: local.shape ?? '',
    local_symbol: local.symbol ?? '',
    local_text_length: local.text_length ?? '',
    local_text: local.text ?? '',
    mapping_strength: check.mapping_strength,
    mapped_object_key: check.mapped_object_key,
    gadd_no: obj.gadd_no ?? '',
    publication_plate: obj.plate_ref ?? '',
    museum_or_collection: obj.museum_or_collection ?? '',
    museum_number: obj.museum_number ?? '',
    registration_or_excavation: obj.registration_or_excavation ?? '',
    object_findspot: obj.findspot ?? '',
    object_inscription_surface: obj.inscription_surface ?? '',
    has_indus_sequence: String(Boolean(obj.has_indus_sequence)),
    has_readable_cuneiform: String(Boolean(obj.has_readable_cuneiform)),
    bridge_verdict: verdict,
    evidence_note: hasObject ? obj.evidence_note : 'No accession, museum number, or publication object identity is present in the current local row.',
  };
});

const fieldnames = [
  'local_row_id',
  'local_excavation_idno',
  'local_site',
  'local_type',
  'local_shape',
  'local_symbol',
  'local_text_length',
  'local_text',
  'mapping_strength',
  'mapped_object_key',
  'gadd_no',
  'publication_plate',
  'museum_or_collection',
  'museum_number',
  'registration_or_excavation',
  'object_findspot',
  'object_inscription_surface',
  'has_indus_sequence',
  'has_readable_cuneiform',
  'bridge_verdict',
  'evidence_note',
];

fs.writeFileSync(
  OUT_CSV,
  [fieldnames.join(','), ...auditRows.map(row => fieldnames.map(field => csvEscape(row[field])).join(','))].join('\n') + '\n',
  'utf8'
);

const mappedRows = auditRows.filter(row => row.mapping_strength === 'verified_by_excavation_id');
const microBilingualObjects = gaddObjects.filter(obj => obj.has_indus_sequence && obj.has_readable_cuneiform);
const cuneiformOnlyObjects = gaddObjects.filter(obj => obj.has_readable_cuneiform && !obj.has_indus_sequence);
const indusOnlyObjects = gaddObjects.filter(obj => obj.has_indus_sequence && !obj.has_readable_cuneiform);

fs.writeFileSync(
  OUT_JSON,
  JSON.stringify(
    {
      date: DATE,
      status: 'gadd_ur_accession_bridge_no_external_phonetic_anchor',
      sources,
      local_ur_rows_checked: urRows.length,
      local_rows_with_verified_excavation_mapping: mappedRows.length,
      local_rows_with_candidate_publication_mapping: auditRows.filter(row => row.mapping_strength.includes('candidate')).length,
      gadd_objects_modeled: gaddObjects.length,
      gadd_objects_with_indus_sequence_only: indusOnlyObjects.length,
      gadd_objects_with_cuneiform_only: cuneiformOnlyObjects.length,
      gadd_micro_bilingual_objects_found: microBilingualObjects.length,
      accepted_external_anchors: 0,
      conclusion:
        'The Ur/Gadd route now improves object identity for two local rows (3898.1/U17649 and 3899.1/U8685), but it yields no external phonetic anchor. In the modeled Gadd/BM/Penn surface, Indus-inscribed objects lack readable cuneiform names/titles, while the cuneiform-inscribed BM 120573 lacks a recorded Indus sign sequence.',
      next_actions: [
        'Acquire Mitchell 1986 figures 106-117 to cross-check all local Ur row mappings against Gadd numbers and images.',
        'Acquire Kjærum 1983 cat.279 and cat.319 for the Failaka row-level mapping problem.',
        'Keep U17649 and U8685 as source-validated external-object controls, not phonetic anchors.',
      ],
      audit_csv: 'data/meluhha/gadd_ur_accession_bridge_audit.csv',
      local_metadata_source: 'data/open_prototype/lipi/metadata_filtered.csv',
      modeled_gadd_objects: gaddObjects,
    },
    null,
    2
  ) + '\n',
  'utf8'
);
