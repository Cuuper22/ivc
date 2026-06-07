import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const EXTERNAL_OBJECTS = path.join(ROOT, 'data/meluhha/external_indus_objects.csv');
const OUT_CSV = path.join(ROOT, 'data/meluhha/bm120573_object_bridge_audit.csv');
const OUT_JSON = path.join(ROOT, 'data/meluhha/bm120573_object_bridge_audit_summary.json');

const bm120573 = {
  object_id: 'BM_120573',
  museum_number: '120573',
  registration_number: '1928,1009.56',
  excavation_number: 'U.7683',
  codex_id: '805337',
  source_url: 'https://www.britishmuseum.org/collection/object/W_1928-1009-56',
  bibliographic_url: 'https://www.britishmuseum.org/collection/term/BIB2877',
  gadd_pdf_url: 'https://ignca.gov.in/Asi_data/33779.pdf',
  findspot: 'Diqdiqqah (Ur), surface',
  excavator: 'Sir Leonard Woolley, 1926/27',
  production_date: 'circa 2500 BC',
  material: 'green-grey mottled steatite',
  shape: 'rectangular',
  dimensions: '27 mm x 24 mm',
  iconography: 'bull standing, facing left',
  inscription_system: 'archaic cuneiform / Sumerian inscription according to BM; uncertain cuneiform reading according to Gadd',
  has_recorded_indus_sign_sequence: false,
  gadd_no: 'Gadd 1932 no.1, pp.5-6, pl.I:1',
  gadd_sign_choices: 'first sign SAG(K) or KA; second KU or possibly LU; third almost certainly SHI; possible fourth uncertain',
  gadd_best_provisional_reading_ascii: 'sak-ku-shi-?',
  gadd_decision_boundary: 'Gadd treats the reading as doubtful, says the cuneiform stands alone, and does not use it to read the Indus script.',
};

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

function verdict(row) {
  const reasons = [];
  const shape = String(row.shape || '').toLowerCase();
  if (shape && shape !== '-' && shape !== bm120573.shape) {
    reasons.push(`shape mismatch: local=${row.shape}, BM=rectangular`);
  }
  if (String(row.text || '').match(/[0-9]{3}/)) {
    reasons.push('local row has Indus numeric sign sequence but BM record/Gadd no.1 exposes cuneiform only');
  }
  if (row.site !== 'Ur') {
    reasons.push(`site mismatch: ${row.site}`);
  }
  if (!reasons.length) {
    reasons.push('insufficient local accession/publication fields to map this row to BM 120573');
  }
  return {
    verdict: 'not_mapped_to_bm120573',
    reasons: reasons.join('; '),
  };
}

const rows = parseCsv(fs.readFileSync(EXTERNAL_OBJECTS, 'utf8'));
const urRows = rows.filter(row => row.region === 'Mesopotamia' && row.site === 'Ur');
const auditRows = urRows.map(row => {
  const v = verdict(row);
  return {
    bm_object_id: bm120573.object_id,
    bm_museum_number: bm120573.museum_number,
    bm_registration_number: bm120573.registration_number,
    bm_excavation_number: bm120573.excavation_number,
    bm_shape: bm120573.shape,
    bm_findspot: bm120573.findspot,
    bm_has_recorded_indus_sign_sequence: String(bm120573.has_recorded_indus_sign_sequence),
    bm_provisional_cuneiform_reading: bm120573.gadd_best_provisional_reading_ascii,
    local_row_id: row.row_id,
    local_site: row.site,
    local_type: row.type,
    local_shape: row.shape,
    local_symbol: row.symbol,
    local_text_length: row.text_length,
    local_text: row.text,
    local_provenance_tier: row.provenance_tier,
    mapping_verdict: v.verdict,
    mapping_reasons: v.reasons,
  };
});

const fieldnames = [
  'bm_object_id',
  'bm_museum_number',
  'bm_registration_number',
  'bm_excavation_number',
  'bm_shape',
  'bm_findspot',
  'bm_has_recorded_indus_sign_sequence',
  'bm_provisional_cuneiform_reading',
  'local_row_id',
  'local_site',
  'local_type',
  'local_shape',
  'local_symbol',
  'local_text_length',
  'local_text',
  'local_provenance_tier',
  'mapping_verdict',
  'mapping_reasons',
];

fs.writeFileSync(
  OUT_CSV,
  [fieldnames.join(','), ...auditRows.map(row => fieldnames.map(field => csvEscape(row[field])).join(','))].join('\n') + '\n',
  'utf8'
);

fs.writeFileSync(
  OUT_JSON,
  JSON.stringify(
    {
      date: new Date().toISOString().slice(0, 10),
      status: 'bm120573_object_level_route_verified_not_external_phonetic_anchor',
      bm120573,
      local_ur_rows_checked: urRows.length,
      mapped_local_rows: 0,
      accepted_external_anchors: 0,
      conclusion:
        'BM 120573 is a real object-level cuneiform route, but it is not an accepted external Indus phonetic anchor in the current workspace: the object has no recorded Indus sign sequence to map, the cuneiform reading is uncertain, and none of the local Ur external-Indus rows maps to the rectangular BM object.',
      next_actions: [
        'Acquire Mitchell 1986 no.7 / fig.111 and Parpola 1994 p.131 to check whether later drawings add any sign or reading not exposed by BM/Gadd.',
        'Do not use BM 120573 as a sign-value anchor unless a source explicitly records an Indus sign sequence on the object or maps it to a local external row.',
        'Continue Ur row accession mapping separately for 3897.1, 3898.1, 3899.1, 5225.1, and 5231.1.',
      ],
      outputs: {
        csv: 'data/meluhha/bm120573_object_bridge_audit.csv',
        summary: 'data/meluhha/bm120573_object_bridge_audit_summary.json',
      },
    },
    null,
    2
  ) + '\n',
  'utf8'
);
