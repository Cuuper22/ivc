// Seed scaffold for the Meluhha research vector, run 2026-05-29. Meluhha is the
// Mesopotamian name for a land usually identified with the Indus civilization,
// so the experiment's hope is a bilingual bridge: a cuneiform text about Meluhha
// tied to an Indus-inscribed object. This script only lays the groundwork. It
// extracts every Indus-style object from regions outside the Indus valley
// (Mesopotamia, Persian Gulf, Iranian Plateau, Central Asia) out of the lipi
// metadata, tagging each as tier T3 quarantined pending source validation. It
// also hard-codes five verified cuneiform seed attestations (P212982's
// Lu-sunzida lines, BDTNS 000128's "son of Meluhha", the Shu-ilishu interpreter
// seal route), five source routes (CDLI, ORACC, BDTNS, ETCSL) with their access
// status, and five control toponyms (Dilmun, Magan, Marhasi, Elam, Gutium) for
// later false-positive testing. Writes four CSVs plus manifest.json under
// data/meluhha/; the manifest records zero accepted external anchors.
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const OUT = path.join(ROOT, 'data', 'meluhha');
const LIPI = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = '';
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (ch === '"' && next === '"') {
        cell += '"';
        i += 1;
      } else if (ch === '"') {
        quoted = false;
      } else {
        cell += ch;
      }
    } else if (ch === '"') {
      quoted = true;
    } else if (ch === ',') {
      row.push(cell);
      cell = '';
    } else if (ch === '\n') {
      row.push(cell.replace(/\r$/, ''));
      rows.push(row);
      row = [];
      cell = '';
    } else {
      cell += ch;
    }
  }
  if (cell.length || row.length) {
    row.push(cell.replace(/\r$/, ''));
    rows.push(row);
  }
  if (!rows.length) return [];
  const header = rows[0];
  return rows.slice(1).filter((r) => r.some((v) => v !== '')).map((r) => {
    const out = {};
    header.forEach((h, i) => {
      out[h] = r[i] ?? '';
    });
    return out;
  });
}

function csvEscape(value) {
  const text = String(value ?? '');
  if (/[",\n\r]/.test(text)) return `"${text.replaceAll('"', '""')}"`;
  return text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(',')];
  for (const row of rows) lines.push(fields.map((f) => csvEscape(row[f])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function sha256(file) {
  if (!fs.existsSync(file)) return '';
  return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
}

function rel(file) {
  return path.relative(ROOT, file).replaceAll(path.sep, '/');
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function main() {
  ensureDir(OUT);
  const lipiRows = parseCsv(fs.readFileSync(LIPI, 'utf8'));

  const externalRegions = new Set([
    'Mesopotamia',
    'Persian Gulf',
    'Iranian Plateau',
    'Central Asia',
  ]);
  const externalObjects = lipiRows
    .filter((row) => externalRegions.has(row.region))
    .map((row) => ({
      row_id: row.id,
      cisi: row.cisi,
      region: row.region,
      site: row.site,
      type: row.type,
      material: row.material,
      shape: row.shape,
      symbol: row.symbol,
      condition: row.condition,
      complete: row.complete,
      direction: row['dir.'],
      class: row.class,
      text_length: row['text length'],
      text: row.text,
      provenance_tier: 'T3_quarantined_lipi_metadata',
      source_ref: rel(LIPI),
      note: 'External Indus-style object candidate; requires source-image and catalogue validation before joining to cuneiform attestations.',
    }));

  const cuneiformSeedAttestations = [
    {
      attestation_id: 'cun_seed_cdli_p212982_lu2_sun2_zi_da',
      source_system: 'CDLI',
      source_id: 'P212982 / CT 50, 076',
      source_url: 'https://cdli.earth/inscriptions/2191016',
      line_ref: 'obverse 5',
      transliteration: 'lu2-sun2-zi-da',
      normalized_token: 'Lu-sunzida',
      token_type: 'personal_name',
      meluhha_relation: 'line immediately before lu2 me-luh-ha-ke4 in same text',
      date_or_period: '',
      provenience: '',
      language: 'Sumerian',
      verification_status: 'verified_primary_page_2026_05_29',
      extraction_priority: 'P0',
      notes: 'CDLI page lists line 5 lu2-sun2-zi-da and line 6 lu2 me-luh-ha-ke4.',
    },
    {
      attestation_id: 'cun_seed_cdli_p212982_lu2_me_luh_ha_ke4',
      source_system: 'CDLI',
      source_id: 'P212982 / CT 50, 076',
      source_url: 'https://cdli.earth/inscriptions/2191016',
      line_ref: 'obverse 6',
      transliteration: 'lu2 me-luh-ha-ke4',
      normalized_token: 'man/person of Meluhha',
      token_type: 'ethnonym_title_or_origin',
      meluhha_relation: 'direct Meluhha-tagged expression',
      date_or_period: '',
      provenience: '',
      language: 'Sumerian',
      verification_status: 'verified_primary_page_2026_05_29',
      extraction_priority: 'P0',
      notes: 'Primary page is readable without JavaScript and exposes ATF transliteration.',
    },
    {
      attestation_id: 'cun_seed_bdtns_000128_ur_lamma_dumu_meluhha',
      source_system: 'BDTNS',
      source_id: '000128 / BM 014594',
      source_url: 'https://bdtns.cesga.es/000128',
      line_ref: 'line 4',
      transliteration: 'Ur-dLamma dumu Me-luh-ha',
      normalized_token: 'Ur-Lamma son of Meluhha',
      token_type: 'personal_name_with_origin_or_patronymic',
      meluhha_relation: 'direct Meluhha-tagged expression',
      date_or_period: 'Ur III',
      provenience: 'Girsu',
      language: 'Sumerian',
      verification_status: 'verified_primary_page_2026_05_29',
      extraction_priority: 'P0',
      notes: 'BDTNS page lists Period Ur III, Language Sumerian, Provenance Girsu, and transliteration line 4.',
    },
    {
      attestation_id: 'cun_seed_bdtns_000128_me_luh_ha_sze3',
      source_system: 'BDTNS',
      source_id: '000128 / BM 014594',
      source_url: 'https://bdtns.cesga.es/000128',
      line_ref: 'reverse 3',
      transliteration: 'mu Ur-dLamma dumu Me-luh-ha-sze3',
      normalized_token: 'to/for Ur-Lamma son of Meluhha',
      token_type: 'personal_name_with_meluhha_relation',
      meluhha_relation: 'direct Meluhha-tagged expression',
      date_or_period: 'Ur III',
      provenience: 'Girsu',
      language: 'Sumerian',
      verification_status: 'verified_primary_page_2026_05_29',
      extraction_priority: 'P0',
      notes: 'BDTNS page line r.3 has Me-luh-ha-še3 in the transaction formula.',
    },
    {
      attestation_id: 'cun_seed_shu_ilishu_interpreter_route',
      source_system: 'object_route',
      source_id: 'Louvre AO 22310 / Shu-ilishu seal',
      source_url: 'https://www.penn.museum/sites/expedition/shu-ilishus-cylinder-seal/',
      line_ref: '',
      transliteration: 'eme-bal me-luh-ha',
      normalized_token: 'interpreter of Meluhha',
      token_type: 'profession_title',
      meluhha_relation: 'direct Meluhha language/profession formula',
      date_or_period: '',
      provenience: '',
      language: 'Akkadian/Sumerian context',
      verification_status: 'route_seed_needs_primary_object_inscription_check',
      extraction_priority: 'P0',
      notes: 'Seed route only until object inscription and edition are independently checked.',
    },
  ];

  const sourceRoutes = [
    {
      route_id: 'route_cdli_api_exact_transliteration',
      source_system: 'CDLI',
      url: 'https://www.cdli.earth/docs/api',
      access_status: 'route_unverified_502_in_web_open_2026_05_29',
      target_queries: 'me-luh-ha;me-luḫ-ḫa;lu2 me-luh-ha;lu2-sun2-zi-da;ma2 me-luh-ha',
      fields_to_capture: 'CDLI/P number;publication;ATF/JTF;language;period;provenience;collection;line context;image links',
      notes: 'CDLI docs API route still needs endpoint check; direct inscription ATF and artifact JSON routes are verified separately.',
    },
    {
      route_id: 'route_cdli_inscription_atf_json',
      source_system: 'CDLI',
      url: 'https://cdli.earth/inscriptions/{inscription_id}/atf;https://cdli.earth/artifacts/{artifact_id}/json',
      access_status: 'verified_10_pages_18_fetches_2026_05_29',
      target_queries: 'me-luh-ha;lu2 me-luh-ha;ma2-gan me-luh-ha;gug me-luh-ha;me-luh-ha{ki}',
      fields_to_capture: 'line context;translation when exposed;period;date;provenience;artifact type;material;language;genre;source hash',
      notes: 'Used by data/meluhha/tools/expand_meluhha_attestations.mjs; fetch log records URL status bytes and SHA-256.',
    },
    {
      route_id: 'route_oracc_json_epsd2',
      source_system: 'ORACC',
      url: 'https://oracc.museum.upenn.edu/json/',
      access_status: 'route_unverified_502_in_web_open_2026_05_29',
      target_queries: 'me-luḫ-ḫa;me-luḫ-ḫa{ki};me-luḫ-ḫa-ta;me-luḫ-ḫa-da',
      fields_to_capture: 'project;lemma/form;period;corpus text id;line context;translation when present',
      notes: 'Use JSON zip acquisition if reachable; keep lexical texts separate from administrative/personal-name attestations.',
    },
    {
      route_id: 'route_bdtns_exact',
      source_system: 'BDTNS',
      url: 'https://bdtns.cesga.es/000128',
      access_status: 'verified_seed_page_2026_05_29',
      target_queries: 'Me-luh-ha;dumu Me-luh-ha',
      fields_to_capture: 'BDTNS number;period;language;provenience;object;collection;linked CDLI/ePSD/eBL;transliteration',
      notes: 'Initial verified seed: BDTNS 000128, Girsu, Ur III, BM 014594.',
    },
    {
      route_id: 'route_etcsl_background',
      source_system: 'ETCSL',
      url: 'https://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?charenc=gcirc',
      access_status: 'route_pending',
      target_queries: 'Meluhha literary/toponym background',
      fields_to_capture: 'composition;line;form;translation;genre',
      notes: 'Background only unless a text supplies a name/title bridge.',
    },
  ];

  const controlToponyms = [
    {
      control_id: 'control_dilmun',
      name: 'Dilmun',
      purpose: 'Co-route Gulf trade control for false-positive bilingual matching.',
      exact_forms_seed: 'dilmun;tilmun;dilmun{ki}',
    },
    {
      control_id: 'control_magan',
      name: 'Magan',
      purpose: 'Co-route trade/toponym control for ships and commodities.',
      exact_forms_seed: 'magan;magan{ki}',
    },
    {
      control_id: 'control_marhasi',
      name: 'Marhasi',
      purpose: 'Eastern polity/toponym control.',
      exact_forms_seed: 'mar-ha-si;marhasi',
    },
    {
      control_id: 'control_elam',
      name: 'Elam',
      purpose: 'Iranian Plateau control for Susa and neighboring contexts.',
      exact_forms_seed: 'elam;elam{ki}',
    },
    {
      control_id: 'control_gutium',
      name: 'Gutium',
      purpose: 'Non-Meluhha ethnonym/toponym control for personal-name/origin formulas.',
      exact_forms_seed: 'gu-ti;gutium',
    },
  ];

  const files = {
    cuneiform_seed_attestations: path.join(OUT, 'cuneiform_seed_attestations.csv'),
    cuneiform_source_routes: path.join(OUT, 'cuneiform_source_routes.csv'),
    external_indus_objects: path.join(OUT, 'external_indus_objects.csv'),
    control_toponyms: path.join(OUT, 'control_toponyms.csv'),
    manifest: path.join(OUT, 'manifest.json'),
  };

  writeCsv(files.cuneiform_seed_attestations, cuneiformSeedAttestations, [
    'attestation_id',
    'source_system',
    'source_id',
    'source_url',
    'line_ref',
    'transliteration',
    'normalized_token',
    'token_type',
    'meluhha_relation',
    'date_or_period',
    'provenience',
    'language',
    'verification_status',
    'extraction_priority',
    'notes',
  ]);
  writeCsv(files.cuneiform_source_routes, sourceRoutes, [
    'route_id',
    'source_system',
    'url',
    'access_status',
    'target_queries',
    'fields_to_capture',
    'notes',
  ]);
  writeCsv(files.external_indus_objects, externalObjects, [
    'row_id',
    'cisi',
    'region',
    'site',
    'type',
    'material',
    'shape',
    'symbol',
    'condition',
    'complete',
    'direction',
    'class',
    'text_length',
    'text',
    'provenance_tier',
    'source_ref',
    'note',
  ]);
  writeCsv(files.control_toponyms, controlToponyms, [
    'control_id',
    'name',
    'purpose',
    'exact_forms_seed',
  ]);

  const regionCounts = {};
  const siteCounts = {};
  for (const row of externalObjects) {
    regionCounts[row.region] = (regionCounts[row.region] || 0) + 1;
    siteCounts[row.site] = (siteCounts[row.site] || 0) + 1;
  }

  const manifest = {
    date: '2026-05-29',
    status: 'vector1_seed_scaffold_no_accepted_external_anchor',
    counts: {
      cuneiform_seed_attestations: cuneiformSeedAttestations.length,
      cuneiform_routes: sourceRoutes.length,
      external_indus_objects: externalObjects.length,
      control_toponyms: controlToponyms.length,
      accepted_external_anchors: 0,
    },
    external_object_counts: {
      by_region: regionCounts,
      by_site: Object.fromEntries(Object.entries(siteCounts).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))),
    },
    files: Object.fromEntries(Object.entries(files).map(([k, v]) => [k, rel(v)])),
    source_hashes: {
      lipi_metadata_filtered: sha256(LIPI),
    },
    caveats: [
      'Only CDLI P212982 and BDTNS 000128 line content is verified in this scaffold.',
      'Shu-ilishu is a route seed until the primary object inscription/edition is checked.',
      'External Indus objects come from T3 quarantined Lipi metadata and require source-image/catalogue validation.',
      'Dilmun/Magan/Marhasi/Elam/Gutium controls must be extracted before scoring any Meluhha-Indus pairing.',
    ],
  };
  fs.writeFileSync(files.manifest, `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
  console.log(JSON.stringify(manifest, null, 2));
}

main();
