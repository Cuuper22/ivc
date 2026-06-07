import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const OUT = path.join(ROOT, 'data', 'meluhha');

const RUN_DATE = '2026-05-29';
const USER_AGENT = 'codex-ivc-meluhha-inventory/2026-05-29';

const CDLI_SOURCES = [
  {
    key: 'cdli_p212982_ct_50_076',
    source_id: 'P212982 / CT 50, 076',
    page_url: 'https://cdli.earth/P212982',
    atf_url: 'https://cdli.earth/inscriptions/2191016/atf',
    metadata_url: 'https://cdli.earth/artifacts/212982/json',
    token_type: 'ethnonym_title_or_origin',
    meluhha_relation: 'direct Meluhha-tagged expression; adjacent line supplies a personal-name candidate',
    notes: 'Includes adjacent personal-name line only because it immediately precedes the direct Meluhha expression in the same text.',
    adjacent_patterns: [
      {
        pattern: /^lu2-sun2-zi-da$/i,
        token_type: 'personal_name_adjacent_to_meluhha_title',
        meluhha_relation: 'line immediately before lu2 me-luh-ha-ke4 in same text',
        normalized_token: 'Lu-sunzida',
      },
    ],
  },
  {
    key: 'cdli_p516138_cusas_40_1354',
    source_id: 'P516138 / CUSAS 40, 1354',
    page_url: 'https://cdli.earth/P516138',
    atf_url: 'https://cdli.earth/inscriptions/2334411/atf',
    metadata_url: 'https://cdli.earth/artifacts/516138/json',
    token_type: 'ethnonym_group_or_title',
    meluhha_relation: 'direct Meluhha-tagged expression in administrative oil-ration text',
    notes: 'Publication metadata describes oil rations to shepherds/men of Meluhha; use as source inventory only.',
  },
  {
    key: 'cdli_p232277_rime_3_1_01_07_st_d',
    source_id: 'P232277 / RIME 3/1.01.07, St D witness',
    page_url: 'https://cdli.earth/P232277',
    atf_url: 'https://cdli.earth/inscriptions/2187023/atf',
    metadata_url: 'https://cdli.earth/artifacts/232277/json',
    token_type: 'toponym_in_route_list',
    meluhha_relation: 'direct Meluhha toponym in co-route list with Magan, Gubi, Dilmun',
    notes: 'Royal-inscription route context, not a name bridge.',
  },
  {
    key: 'cdli_p431881_gudea_cyl_a_composite',
    source_id: 'P431881 / RIME 3/1.01.07, Cyl A composite',
    page_url: 'https://cdli.earth/P431881',
    atf_url: 'https://cdli.earth/inscriptions/2238733/atf',
    metadata_url: 'https://cdli.earth/artifacts/431881/json',
    token_type: 'toponym_or_commodity_route_context',
    meluhha_relation: 'direct Meluhha toponym in royal-inscription route and commodity contexts',
    notes: 'Composite literary/royal text; use to define cuneiform-side contexts and controls only.',
  },
  {
    key: 'cdli_p431882_gudea_cyl_b_composite',
    source_id: 'P431882 / RIME 3/1.01.07, Cyl B composite',
    page_url: 'https://cdli.earth/P431882',
    atf_url: 'https://cdli.earth/inscriptions/2312920/atf',
    metadata_url: 'https://cdli.earth/artifacts/431882/json',
    token_type: 'commodity_route_context',
    meluhha_relation: 'direct Meluhha adjective/toponym in commodity list',
    notes: 'Composite text; commodity line is inventory only until tied to an external Indus object by controls.',
  },
  {
    key: 'cdli_p469516_enki_world_order',
    source_id: 'P469516 / CDLI Literary 000334 (Enki and World Order)',
    page_url: 'https://cdli.earth/P469516',
    atf_url: 'https://cdli.earth/inscriptions/2257941/atf',
    metadata_url: 'https://cdli.earth/artifacts/469516/json',
    token_type: 'literary_toponym_or_ship_context',
    meluhha_relation: 'direct Meluhha toponym in literary trade-route and ship contexts',
    notes: 'Literary source; useful for route vocabulary and controls, not an external anchor by itself.',
  },
  {
    key: 'cdli_p469679_curse_of_agade',
    source_id: 'P469679 / CDLI Literary 000375 (Curse of Agade)',
    page_url: 'https://cdli.earth/P469679',
    atf_url: 'https://cdli.earth/inscriptions/2257987/atf',
    metadata_url: 'https://cdli.earth/artifacts/469679/json',
    token_type: 'ethnonym_in_literary_trade_context',
    meluhha_relation: 'direct Meluhha ethnonym/toponym in literary import context',
    notes: 'Literary source; captures an ethnonym phrase and imported-goods context.',
  },
  {
    key: 'cdli_p432309_rime_3_2_01_05_04',
    source_id: 'P432309 / RIME 3/2.01.05.04 composite',
    page_url: 'https://cdli.earth/P432309',
    atf_url: 'https://cdli.earth/inscriptions/2316970/atf',
    metadata_url: 'https://cdli.earth/artifacts/432309/json',
    token_type: 'animal_or_object_label_with_meluhha_modifier',
    meluhha_relation: 'direct Meluhha modifier in tribute object/animal context',
    notes: 'Translation glosses the phrase as a speckled Meluhha dog; kept as contextual inventory only.',
  },
];

const BDTNS_SOURCES = [
  {
    key: 'bdtns_000128_bm_014594',
    source_id: 'BDTNS 000128 / BM 014594',
    page_url: 'https://bdtns.cesga.es/000128',
    token_type: 'personal_name_with_origin_or_patronymic',
    meluhha_relation: 'direct Meluhha-tagged personal-name/origin formula',
    notes: 'BDTNS page links CDLI P108448 as a resource and gives Girsu/Ur III metadata.',
  },
  {
    key: 'bdtns_011069_im_u_03884',
    source_id: 'BDTNS 011069 / IM U. 03884',
    page_url: 'https://bdtns.cesga.es/011069',
    token_type: 'object_or_commodity_designation_with_meluhha',
    meluhha_relation: 'direct Meluhha-tagged line in administrative text',
    notes: 'BDTNS page links CDLI P137088 as a resource and gives Ur/Ur III metadata.',
  },
];

const ATTESTATION_FIELDS = [
  'attestation_id',
  'source_system',
  'source_id',
  'source_url',
  'text_source_url',
  'metadata_source_url',
  'line_ref',
  'line_number',
  'surface_context',
  'transliteration',
  'english_translation',
  'normalized_meluhha_forms',
  'normalized_token',
  'token_type',
  'meluhha_relation',
  'co_route_tokens',
  'previous_lines',
  'following_lines',
  'period',
  'date_or_period',
  'dates_referenced',
  'provenience',
  'artifact_type',
  'material',
  'language',
  'genre',
  'collection_or_museum',
  'source_text_sha256',
  'metadata_sha256',
  'verification_status',
  'notes',
];

const FETCH_LOG_FIELDS = [
  'source_key',
  'source_system',
  'role',
  'url',
  'http_status',
  'byte_length',
  'sha256',
  'error',
];

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
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

function sha256Text(text) {
  return crypto.createHash('sha256').update(text, 'utf8').digest('hex');
}

function rel(file) {
  return path.relative(ROOT, file).replaceAll(path.sep, '/');
}

function sanitizeId(text) {
  return String(text)
    .toLowerCase()
    .replaceAll('{', '')
    .replaceAll('}', '')
    .replaceAll('#', '')
    .replaceAll('!', '')
    .replaceAll('?', '')
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '')
    .slice(0, 96);
}

function uniqueJoined(values) {
  return [...new Set(values.filter(Boolean))].join('|');
}

async function fetchText(url) {
  try {
    const response = await fetch(url, { headers: { 'user-agent': USER_AGENT } });
    const text = await response.text();
    return {
      ok: response.ok,
      status: response.status,
      text,
      byteLength: Buffer.byteLength(text, 'utf8'),
      sha256: sha256Text(text),
      error: response.ok ? '' : `HTTP ${response.status}`,
    };
  } catch (error) {
    return {
      ok: false,
      status: '',
      text: '',
      byteLength: 0,
      sha256: '',
      error: error instanceof Error ? error.message : String(error),
    };
  }
}

function sourceLog(source, sourceSystem, role, url, result) {
  return {
    source_key: source.key,
    source_system: sourceSystem,
    role,
    url,
    http_status: result.status,
    byte_length: result.byteLength,
    sha256: result.sha256,
    error: result.error,
  };
}

function stripHtml(html) {
  return html
    .replace(/<small><sup>(.*?)<\/sup><\/small>/gi, '{$1}')
    .replace(/<sup>(.*?)<\/sup>/gi, '$1')
    .replace(/<sub>(.*?)<\/sub>/gi, '_$1')
    .replace(/&nbsp;/g, ' ')
    .replace(/&scaron;/g, 'š')
    .replace(/&Scaron;/g, 'Š')
    .replace(/&#269;/g, 'č')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function extractCdliMetadata(text) {
  if (!text) return {};
  try {
    const parsed = JSON.parse(text);
    const artifact = Array.isArray(parsed) ? parsed[0] : parsed;
    if (!artifact || typeof artifact !== 'object') return {};
    return {
      designation: artifact.designation ?? '',
      museum_no: artifact.museum_no ?? '',
      period: artifact.period?.period ?? '',
      date_or_period: artifact.period?.name ?? artifact.period?.period ?? '',
      dates_referenced: artifact.dates_referenced ?? '',
      provenience: artifact.provenience?.provenience ?? '',
      artifact_type: artifact.artifact_type?.artifact_type ?? '',
      material: joinNamed(artifact.materials, 'material'),
      language: joinNamed(artifact.languages, 'language'),
      genre: joinNamed(artifact.genres, 'genre'),
      collection_or_museum: joinCollections(artifact.collections) || artifact.museum_no || '',
      publication_comments: joinPublicationComments(artifact.publications),
    };
  } catch {
    return {};
  }
}

function joinNamed(values, key) {
  if (!Array.isArray(values)) return '';
  return uniqueJoined(values.map((value) => {
    const direct = value?.[key];
    if (typeof direct === 'string') return direct;
    if (direct && typeof direct === 'object' && typeof direct[key] === 'string') return direct[key];
    const singular = key.replace(/s$/, '');
    const nested = value?.[singular];
    if (typeof nested === 'string') return nested;
    if (nested && typeof nested === 'object' && typeof nested[singular] === 'string') return nested[singular];
    return '';
  }));
}

function joinCollections(values) {
  if (!Array.isArray(values)) return '';
  return uniqueJoined(values.map((value) => value?.collection?.collection ?? value?.collection ?? ''));
}

function joinPublicationComments(values) {
  if (!Array.isArray(values)) return '';
  return uniqueJoined(values.map((value) => value?.publication_comments ?? ''));
}

function normalizeMeluhhaForms(text) {
  const matches = String(text).match(/me-luh-ha(?:\{ki[#?!]*\})?(?:-[a-z0-9#{}!?]+)*/gi) ?? [];
  return uniqueJoined(matches);
}

function coRouteTokens(text) {
  const tokenSpecs = [
    ['Magan', /ma2-gan(?:\{ki[#?!]*\})?/i],
    ['Dilmun', /dilmun(?:\{ki[#?!]*\})?/i],
    ['Marhasi', /mar[#?!]?-ha[#?!]?-szi(?:\{ki[#?!]*\})?|mar-ha-si/i],
    ['Elam', /elam(?:\{ki[#?!]*\})?/i],
    ['Susa', /szuszin(?:\{ki[#?!]*\})?/i],
    ['Gubi', /gu-bi(?:\{ki[#?!]*\})?/i],
  ];
  return uniqueJoined(tokenSpecs.filter(([, regex]) => regex.test(text)).map(([name]) => name));
}

function parseAtfRecords(atf) {
  const records = [];
  const lines = atf.split(/\r?\n/);
  const context = [];
  for (let i = 0; i < lines.length; i += 1) {
    const raw = lines[i].trim();
    if (!raw) continue;
    if (raw.startsWith('@')) {
      context.push(raw.replace(/^@/, ''));
      if (context.length > 4) context.shift();
      continue;
    }
    const match = raw.match(/^(\d+[a-z]?)\.\s+(.*)$/i);
    if (!match) continue;
    const next = lines[i + 1]?.trim() ?? '';
    const translation = next.startsWith('#tr.en:') ? next.replace(/^#tr\.en:\s*/i, '') : '';
    records.push({
      index: i,
      lineNumber: match[1],
      text: match[2].trim(),
      lineRef: match[1],
      surfaceContext: context.join(' > '),
      translation,
    });
  }
  return records;
}

function contextWindow(records, recordIndex, side) {
  const start = side === 'previous' ? Math.max(0, recordIndex - 2) : recordIndex + 1;
  const end = side === 'previous' ? recordIndex : Math.min(records.length, recordIndex + 3);
  return records.slice(start, end).map((record) => `${record.lineRef}. ${record.text}`).join(' || ');
}

function classifyCdliRow(source, record, combinedContext) {
  const text = `${record.text} ${record.translation}`.toLowerCase();
  if (/lu2\s+me-luh-ha|me-luh-ha\{ki\}-me/.test(record.text)) return source.token_type;
  if (/gug|carnelian|carneol/.test(text)) return 'commodity_route_context';
  if (/ma2|ship/.test(text)) return 'ship_or_trade_route_context';
  if (/lu2|people|melu/.test(text) && /people|lu2/.test(text)) return 'ethnonym_in_literary_trade_context';
  if (/ur\s+gun3-a|dog/.test(text)) return 'animal_or_object_label_with_meluhha_modifier';
  if (/ma2-gan|dilmun|gu-bi|elam|szuszin/.test(combinedContext)) return 'toponym_in_route_list';
  return source.token_type;
}

function buildCdliRows(source, atfResult, metadataResult) {
  if (!atfResult.ok) return [];
  const metadata = extractCdliMetadata(metadataResult.text);
  const records = parseAtfRecords(atfResult.text);
  const rows = [];
  for (let i = 0; i < records.length; i += 1) {
    const record = records[i];
    const previous = contextWindow(records, i, 'previous');
    const following = contextWindow(records, i, 'following');
    const combinedContext = `${previous} ${record.text} ${record.translation} ${following}`;
    if (/me-luh-ha/i.test(record.text)) {
      const lineSlug = sanitizeId(`${record.lineRef}_${record.text}`);
      rows.push({
        attestation_id: `mel_${source.key}_${lineSlug}`,
        source_system: 'CDLI',
        source_id: source.source_id,
        source_url: source.page_url,
        text_source_url: source.atf_url,
        metadata_source_url: source.metadata_url,
        line_ref: record.lineRef,
        line_number: record.lineNumber,
        surface_context: record.surfaceContext,
        transliteration: record.text,
        english_translation: record.translation,
        normalized_meluhha_forms: normalizeMeluhhaForms(record.text),
        normalized_token: '',
        token_type: classifyCdliRow(source, record, combinedContext),
        meluhha_relation: source.meluhha_relation,
        co_route_tokens: coRouteTokens(combinedContext),
        previous_lines: previous,
        following_lines: following,
        period: metadata.period,
        date_or_period: metadata.date_or_period,
        dates_referenced: metadata.dates_referenced,
        provenience: metadata.provenience,
        artifact_type: metadata.artifact_type,
        material: metadata.material,
        language: metadata.language,
        genre: metadata.genre,
        collection_or_museum: metadata.collection_or_museum,
        source_text_sha256: atfResult.sha256,
        metadata_sha256: metadataResult.sha256,
        verification_status: `fetched_primary_digital_source_${RUN_DATE}`,
        notes: uniqueJoined([source.notes, metadata.publication_comments]),
      });
    }

    for (const adjacent of source.adjacent_patterns ?? []) {
      if (!adjacent.pattern.test(record.text)) continue;
      const next = records[i + 1];
      if (!next || !/me-luh-ha/i.test(next.text)) continue;
      const lineSlug = sanitizeId(`${record.lineRef}_${record.text}`);
      rows.push({
        attestation_id: `mel_${source.key}_${lineSlug}_adjacent`,
        source_system: 'CDLI',
        source_id: source.source_id,
        source_url: source.page_url,
        text_source_url: source.atf_url,
        metadata_source_url: source.metadata_url,
        line_ref: record.lineRef,
        line_number: record.lineNumber,
        surface_context: record.surfaceContext,
        transliteration: record.text,
        english_translation: record.translation,
        normalized_meluhha_forms: '',
        normalized_token: adjacent.normalized_token,
        token_type: adjacent.token_type,
        meluhha_relation: adjacent.meluhha_relation,
        co_route_tokens: coRouteTokens(`${previous} ${following}`),
        previous_lines: previous,
        following_lines: following,
        period: metadata.period,
        date_or_period: metadata.date_or_period,
        dates_referenced: metadata.dates_referenced,
        provenience: metadata.provenience,
        artifact_type: metadata.artifact_type,
        material: metadata.material,
        language: metadata.language,
        genre: metadata.genre,
        collection_or_museum: metadata.collection_or_museum,
        source_text_sha256: atfResult.sha256,
        metadata_sha256: metadataResult.sha256,
        verification_status: `fetched_primary_digital_source_${RUN_DATE}`,
        notes: source.notes,
      });
    }
  }
  return rows;
}

function parseBdtnsRows(html) {
  const tableRows = [...html.matchAll(/<tr\b[\s\S]*?<\/tr>/gi)].map((match) => match[0]);
  return tableRows.map((row) => [...row.matchAll(/<td\b[\s\S]*?<\/td>/gi)].map((cell) => stripHtml(cell[0])));
}

function extractBdtnsMetadata(rows) {
  const metadata = {};
  for (let i = 0; i < rows.length; i += 1) {
    const cells = rows[i];
    if (cells.join('|') === 'Period|Language|Provenance|Object|Genre') {
      const values = rows[i + 1] ?? [];
      metadata.period = values[0] ?? '';
      metadata.date_or_period = values[0] ?? '';
      metadata.language = values[1] ?? '';
      metadata.provenience = values[2] ?? '';
      metadata.artifact_type = values[3] ?? '';
      metadata.genre = values[4] ?? '';
    }
    if (cells.join('|') === 'Date|Dates Referenced|Measurements|Seal') {
      const values = rows[i + 1] ?? [];
      metadata.dates_referenced = values[0] ?? '';
    }
    if (cells.join('|') === 'Collection|Museum No.|Accession No.|Excavation No.') {
      const values = rows[i + 1] ?? [];
      metadata.collection_or_museum = [values[0], values[1], values[3]].filter(Boolean).join(' | ');
    }
    const cdliCell = cells.find((cell) => /CDLI\s+P\d+/i.test(cell));
    if (cdliCell && !metadata.cdli_resource) metadata.cdli_resource = cdliCell;
  }
  return metadata;
}

function buildBdtnsRows(source, htmlResult) {
  if (!htmlResult.ok) return [];
  const parsedRows = parseBdtnsRows(htmlResult.text);
  const metadata = extractBdtnsMetadata(parsedRows);
  const transliterationRows = parsedRows
    .filter((cells) => cells.length === 2 && /Me-luh-ha/i.test(cells[1]))
    .map((cells) => ({ lineRef: cells[0], text: cells[1] }));

  return transliterationRows.map((row) => {
    const lineSlug = sanitizeId(`${row.lineRef}_${row.text}`);
    return {
      attestation_id: `mel_${source.key}_${lineSlug}`,
      source_system: 'BDTNS',
      source_id: source.source_id,
      source_url: source.page_url,
      text_source_url: source.page_url,
      metadata_source_url: source.page_url,
      line_ref: row.lineRef,
      line_number: row.lineRef,
      surface_context: '',
      transliteration: row.text,
      english_translation: '',
      normalized_meluhha_forms: normalizeMeluhhaForms(row.text),
      normalized_token: '',
      token_type: source.token_type,
      meluhha_relation: source.meluhha_relation,
      co_route_tokens: coRouteTokens(row.text),
      previous_lines: '',
      following_lines: '',
      period: metadata.period ?? '',
      date_or_period: metadata.date_or_period ?? '',
      dates_referenced: metadata.dates_referenced ?? '',
      provenience: metadata.provenience ?? '',
      artifact_type: metadata.artifact_type ?? '',
      material: '',
      language: metadata.language ?? '',
      genre: metadata.genre ?? '',
      collection_or_museum: metadata.collection_or_museum ?? '',
      source_text_sha256: htmlResult.sha256,
      metadata_sha256: htmlResult.sha256,
      verification_status: `fetched_primary_digital_source_${RUN_DATE}`,
      notes: uniqueJoined([source.notes, metadata.cdli_resource]),
    };
  });
}

function summarizeInventory(rows, fetchLogs) {
  const bySystem = {};
  const byTokenType = {};
  const bySource = {};
  for (const row of rows) {
    bySystem[row.source_system] = (bySystem[row.source_system] ?? 0) + 1;
    byTokenType[row.token_type] = (byTokenType[row.token_type] ?? 0) + 1;
    bySource[row.source_id] = (bySource[row.source_id] ?? 0) + 1;
  }
  return {
    date: RUN_DATE,
    status: 'expanded_meluhha_cuneiform_inventory_no_accepted_external_anchor',
    counts: {
      sources_requested: CDLI_SOURCES.length + BDTNS_SOURCES.length,
      fetches_attempted: fetchLogs.length,
      fetches_failed: fetchLogs.filter((log) => log.error).length,
      cuneiform_attestations_expanded: rows.length,
      accepted_external_anchors: 0,
    },
    by_system: bySystem,
    by_token_type: byTokenType,
    by_source: bySource,
    files: {
      cuneiform_attestations_expanded: 'data/meluhha/cuneiform_attestations_expanded.csv',
      cuneiform_fetch_log: 'data/meluhha/cuneiform_fetch_log.csv',
      meluhha_token_inventory: 'data/meluhha/meluhha_token_inventory.json',
    },
    caveats: [
      'This inventory is source-side evidence only and contains no accepted Indus external anchor.',
      'Composite literary texts are separated as context sources; they are not treated as object-level bilinguals.',
      'Line translations are whatever the fetched digital edition exposes; blank translation means the fetch did not expose one.',
      'Any Meluhha-Indus pairing still requires a forger false-positive gate and skeptic review before ledger promotion.',
    ],
  };
}

async function main() {
  ensureDir(OUT);
  const fetchLogs = [];
  const attestations = [];

  for (const source of CDLI_SOURCES) {
    const atfResult = await fetchText(source.atf_url);
    fetchLogs.push(sourceLog(source, 'CDLI', 'atf', source.atf_url, atfResult));

    const metadataResult = source.metadata_url
      ? await fetchText(source.metadata_url)
      : { ok: false, status: '', text: '', byteLength: 0, sha256: '', error: 'no metadata url' };
    if (source.metadata_url) fetchLogs.push(sourceLog(source, 'CDLI', 'metadata', source.metadata_url, metadataResult));

    attestations.push(...buildCdliRows(source, atfResult, metadataResult));
  }

  for (const source of BDTNS_SOURCES) {
    const htmlResult = await fetchText(source.page_url);
    fetchLogs.push(sourceLog(source, 'BDTNS', 'html', source.page_url, htmlResult));
    attestations.push(...buildBdtnsRows(source, htmlResult));
  }

  attestations.sort((a, b) => a.attestation_id.localeCompare(b.attestation_id));
  writeCsv(path.join(OUT, 'cuneiform_attestations_expanded.csv'), attestations, ATTESTATION_FIELDS);
  writeCsv(path.join(OUT, 'cuneiform_fetch_log.csv'), fetchLogs, FETCH_LOG_FIELDS);

  const summary = summarizeInventory(attestations, fetchLogs);
  fs.writeFileSync(path.join(OUT, 'meluhha_token_inventory.json'), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

  console.log(JSON.stringify({
    attestations: attestations.length,
    fetches: fetchLogs.length,
    failed_fetches: fetchLogs.filter((log) => log.error).length,
    output: rel(path.join(OUT, 'cuneiform_attestations_expanded.csv')),
  }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
