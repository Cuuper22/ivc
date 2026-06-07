import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const OUT = path.join(ROOT, 'data', 'meluhha');
const RUN_DATE = '2026-05-29';
const USER_AGENT = 'codex-ivc-cdli-meluhha-export/2026-05-29';

const SEARCH_TERMS = [
  { term: 'me-luh-ha', class: 'meluhha_broad' },
  { term: 'me-luh-ha{ki}', class: 'meluhha_toponym' },
  { term: 'lu2 me-luh-ha', class: 'meluhha_person_title' },
  { term: 'ma2 me-luh-ha', class: 'meluhha_ship_context' },
  { term: 'me-luh-ha-ta', class: 'meluhha_ablative' },
  { term: 'me-luh-ha-da', class: 'meluhha_comitative' },
  { term: 'lu2-sun2-zi-da', class: 'lu_sunzida_name_test' },
];

const CDLI_ARTIFACT_FIELDS = [
  'artifact_p',
  'artifact_id',
  'designation',
  'museum_no',
  'accession_no',
  'provenience',
  'period',
  'dates_referenced',
  'collections',
  'genres',
  'materials',
  'artifact_type',
  'languages',
  'publications_key',
  'publications_type',
  'publications_exact_ref',
  'external_resources',
  'external_resources_key',
  'query_terms',
  'has_meluhha_in_atf',
  'has_lu_sunzida_in_atf',
  'meluhha_line_count',
  'lu_sunzida_line_count',
  'source_url',
];

const LINE_FIELDS = [
  'context_id',
  'query_term',
  'query_class',
  'artifact_p',
  'artifact_id',
  'designation',
  'museum_no',
  'provenience',
  'period',
  'dates_referenced',
  'surface_context',
  'line_number',
  'line_index',
  'line_raw',
  'line_text',
  'previous_line',
  'following_line',
  'has_meluhha_in_artifact',
  'has_lu_sunzida_in_artifact',
  'line_has_meluhha',
  'line_has_lu_sunzida',
  'min_distance_to_meluhha_line',
  'source_url',
];

const LU_FIELDS = [
  'artifact_p',
  'artifact_id',
  'designation',
  'museum_no',
  'provenience',
  'period',
  'dates_referenced',
  'line_index',
  'surface_context',
  'line_number',
  'line_raw',
  'previous_line',
  'following_line',
  'meluhha_in_same_artifact',
  'meluhha_adjacent_distance',
  'nearest_meluhha_line',
  'detector_outcome',
  'source_url',
];

const FETCH_FIELDS = [
  'fetch_id',
  'role',
  'query_term',
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
  for (const row of rows) lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function sha256Text(text) {
  return crypto.createHash('sha256').update(text, 'utf8').digest('hex');
}

function rel(file) {
  return path.relative(ROOT, file).replaceAll(path.sep, '/');
}

function stableId(parts) {
  return crypto.createHash('sha1').update(parts.join('\u241f'), 'utf8').digest('hex').slice(0, 16);
}

function artifactP(id) {
  return `P${String(id).padStart(6, '0')}`;
}

function textValue(value) {
  if (value == null) return '';
  if (Array.isArray(value)) return value.filter(Boolean).join('; ');
  return String(value);
}

function artifactField(row, field) {
  const value = row[field];
  if (value == null) return '';
  if (Array.isArray(value)) return value.map((item) => {
    if (item == null) return '';
    if (typeof item === 'string') return item;
    if (typeof item === 'object') {
      return item[field] ?? item.name ?? item.genre ?? item.material ?? item.collection ?? item.language ?? item.artifact_type ?? item.designation ?? '';
    }
    return String(item);
  }).filter(Boolean).join('; ');
  if (typeof value === 'object') return value.artifact_type ?? value.period ?? value.provenience ?? value.collection ?? value.genre ?? value.material ?? value.language ?? '';
  return String(value);
}

function normalizeLine(line) {
  return String(line)
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[{}[\]#?!<>]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function hasMeluhha(text) {
  const normalized = normalizeLine(text);
  return normalized.includes('me-luh-ha') || normalized.includes('me-luhha') || normalized.includes('meluhha');
}

function hasLuSunzida(text) {
  const normalized = normalizeLine(text);
  return normalized.includes('lu2-sun2-zi-da') || normalized.includes('lu-sun2-zi-da');
}

function termMatches(text, term) {
  if (term === 'lu2-sun2-zi-da') return hasLuSunzida(text);
  const normalized = normalizeLine(text);
  return normalized.includes(normalizeLine(term));
}

function cleanLineText(line) {
  return String(line).replace(/^\s*\d+'?\.?\s*/, '').trim();
}

function parseAtfLines(atf) {
  const parsed = [];
  let surface = '';
  for (const rawLine of String(atf ?? '').split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line) continue;
    if (line.startsWith('@')) {
      surface = [surface, line].filter(Boolean).join(' | ');
      if (line === '@obverse' || line === '@reverse' || line === '@tablet') surface = line;
      continue;
    }
    if (line.startsWith('&') || line.startsWith('#') || line.startsWith('$') || line.startsWith('>>')) continue;
    const numberMatch = line.match(/^(\d+'?|\d+)\.\s*/);
    parsed.push({
      raw: line,
      text: cleanLineText(line),
      number: numberMatch ? numberMatch[1] : '',
      surface,
    });
  }
  return parsed;
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

function fetchLog(fetchId, role, queryTerm, url, result) {
  return {
    fetch_id: fetchId,
    role,
    query_term: queryTerm,
    url,
    http_status: result.status,
    byte_length: result.byteLength,
    sha256: result.sha256,
    error: result.error,
  };
}

function nearestMeluhha(lines, lineIndex) {
  let best = null;
  lines.forEach((line, idx) => {
    if (!hasMeluhha(line.raw)) return;
    const distance = Math.abs(idx - lineIndex);
    if (!best || distance < best.distance) best = { distance, line: line.raw };
  });
  return best;
}

async function main() {
  ensureDir(OUT);

  const fetchRows = [];
  const artifacts = new Map();
  const lineRows = [];
  const luRows = [];
  const querySummaries = [];

  for (const search of SEARCH_TERMS) {
    const url = `https://cdli.earth/search?atf_transliteration=${encodeURIComponent(search.term)}&format=json`;
    const result = await fetchText(url);
    fetchRows.push(fetchLog(`cdli_${search.class}`, 'cdli_search_json', search.term, url, result));
    if (!result.ok) {
      querySummaries.push({
        term: search.term,
        class: search.class,
        artifact_count: 0,
        matched_line_count: 0,
        fetch_error: result.error,
      });
      continue;
    }

    let rows;
    try {
      rows = JSON.parse(result.text);
    } catch (error) {
      querySummaries.push({
        term: search.term,
        class: search.class,
        artifact_count: 0,
        matched_line_count: 0,
        fetch_error: error instanceof Error ? error.message : String(error),
      });
      continue;
    }

    let matchedLineCount = 0;
    for (const row of rows) {
      const id = row.id;
      const p = artifactP(id);
      const atf = row.inscription?.atf ?? '';
      const parsed = parseAtfLines(atf);
      const meluhhaLines = parsed.filter((line) => hasMeluhha(line.raw));
      const luLines = parsed.filter((line) => hasLuSunzida(line.raw));
      const existing = artifacts.get(id) ?? {
        artifact_p: p,
        artifact_id: id,
        designation: row.designation ?? '',
        museum_no: row.museum_no ?? '',
        accession_no: row.accession_no ?? '',
        provenience: artifactField(row, 'provenience'),
        period: artifactField(row, 'period'),
        dates_referenced: textValue(row.dates_referenced),
        collections: artifactField(row, 'collections'),
        genres: artifactField(row, 'genres'),
        materials: artifactField(row, 'materials'),
        artifact_type: artifactField(row, 'artifact_type'),
        languages: artifactField(row, 'languages'),
        publications_key: textValue(row.publications_key),
        publications_type: textValue(row.publications_type),
        publications_exact_ref: textValue(row.publications_exact_ref),
        external_resources: textValue(row.external_resources),
        external_resources_key: textValue(row.external_resources_key),
        query_terms: '',
        has_meluhha_in_atf: hasMeluhha(atf) ? 'true' : 'false',
        has_lu_sunzida_in_atf: hasLuSunzida(atf) ? 'true' : 'false',
        meluhha_line_count: meluhhaLines.length,
        lu_sunzida_line_count: luLines.length,
        source_url: `https://cdli.earth/${p}`,
        _queryTerms: new Set(),
      };
      existing._queryTerms.add(search.term);
      existing.has_meluhha_in_atf = existing.has_meluhha_in_atf === 'true' || hasMeluhha(atf) ? 'true' : 'false';
      existing.has_lu_sunzida_in_atf = existing.has_lu_sunzida_in_atf === 'true' || hasLuSunzida(atf) ? 'true' : 'false';
      existing.meluhha_line_count = Math.max(Number(existing.meluhha_line_count), meluhhaLines.length);
      existing.lu_sunzida_line_count = Math.max(Number(existing.lu_sunzida_line_count), luLines.length);
      artifacts.set(id, existing);

      parsed.forEach((line, idx) => {
        if (!termMatches(line.raw, search.term)) return;
        matchedLineCount += 1;
        const nearest = nearestMeluhha(parsed, idx);
        lineRows.push({
          context_id: stableId([search.term, p, idx, line.raw]),
          query_term: search.term,
          query_class: search.class,
          artifact_p: p,
          artifact_id: id,
          designation: row.designation ?? '',
          museum_no: row.museum_no ?? '',
          provenience: artifactField(row, 'provenience'),
          period: artifactField(row, 'period'),
          dates_referenced: textValue(row.dates_referenced),
          surface_context: line.surface,
          line_number: line.number,
          line_index: idx,
          line_raw: line.raw,
          line_text: line.text,
          previous_line: parsed[idx - 1]?.raw ?? '',
          following_line: parsed[idx + 1]?.raw ?? '',
          has_meluhha_in_artifact: hasMeluhha(atf) ? 'true' : 'false',
          has_lu_sunzida_in_artifact: hasLuSunzida(atf) ? 'true' : 'false',
          line_has_meluhha: hasMeluhha(line.raw) ? 'true' : 'false',
          line_has_lu_sunzida: hasLuSunzida(line.raw) ? 'true' : 'false',
          min_distance_to_meluhha_line: nearest ? nearest.distance : '',
          source_url: `https://cdli.earth/${p}`,
        });
      });

      if (search.term === 'lu2-sun2-zi-da') {
        parsed.forEach((line, idx) => {
          if (!hasLuSunzida(line.raw)) return;
          const nearest = nearestMeluhha(parsed, idx);
          const sameArtifact = hasMeluhha(atf);
          luRows.push({
            artifact_p: p,
            artifact_id: id,
            designation: row.designation ?? '',
            museum_no: row.museum_no ?? '',
            provenience: artifactField(row, 'provenience'),
            period: artifactField(row, 'period'),
            dates_referenced: textValue(row.dates_referenced),
            line_index: idx,
            surface_context: line.surface,
            line_number: line.number,
            line_raw: line.raw,
            previous_line: parsed[idx - 1]?.raw ?? '',
            following_line: parsed[idx + 1]?.raw ?? '',
            meluhha_in_same_artifact: sameArtifact ? 'true' : 'false',
            meluhha_adjacent_distance: nearest ? nearest.distance : '',
            nearest_meluhha_line: nearest ? nearest.line : '',
            detector_outcome: sameArtifact ? 'candidate_true_positive_or_ambiguous' : 'false_positive_for_meluhha_detector',
            source_url: `https://cdli.earth/${p}`,
          });
        });
      }
    }

    querySummaries.push({
      term: search.term,
      class: search.class,
      artifact_count: rows.length,
      matched_line_count: matchedLineCount,
      fetch_error: '',
    });
  }

  const epsd2Url = 'https://oracc.museum.upenn.edu/epsd2/names/cbd/qpn/x000016710.html';
  const epsd2 = await fetchText(epsd2Url);
  fetchRows.push(fetchLog('oracc_epsd2_meluhha_qpn', 'oracc_epsd2_entry', 'Meluhha', epsd2Url, epsd2));
  const epsd2InstanceMatch = epsd2.text.match(/>(\d+)\s+instances</);
  const epsd2Instances = epsd2InstanceMatch ? Number(epsd2InstanceMatch[1]) : null;
  const epsd2SpellingsMatch = epsd2.text.match(/>(\d+)\s+different spellings</);
  const epsd2Spellings = epsd2SpellingsMatch ? Number(epsd2SpellingsMatch[1]) : null;

  const artifactRows = [...artifacts.values()].map((row) => ({
    ...Object.fromEntries(CDLI_ARTIFACT_FIELDS.map((field) => [field, row[field] ?? ''])),
    query_terms: [...row._queryTerms].sort().join('|'),
  })).sort((a, b) => String(a.artifact_p).localeCompare(String(b.artifact_p)));

  const luArtifactIds = new Set(luRows.map((row) => row.artifact_id));
  const luMeluhhaArtifactIds = new Set(luRows.filter((row) => row.meluhha_in_same_artifact === 'true').map((row) => row.artifact_id));
  const luAdjacentArtifactIds = new Set(luRows.filter((row) => row.meluhha_adjacent_distance !== '' && Number(row.meluhha_adjacent_distance) <= 1).map((row) => row.artifact_id));
  const luFalsePositiveArtifacts = luArtifactIds.size - luMeluhhaArtifactIds.size;
  const luFalsePositiveRate = luArtifactIds.size ? luFalsePositiveArtifacts / luArtifactIds.size : null;
  const luAdjacentOnlyRate = luArtifactIds.size ? (luArtifactIds.size - luAdjacentArtifactIds.size) / luArtifactIds.size : null;

  const summary = {
    date: RUN_DATE,
    status: 'cdli_current_search_exports_anchor_failure_lu_sunzida_not_meluhha_diagnostic',
    source_routes: {
      cdli_search_parameter: 'atf_transliteration',
      cdli_format: 'json',
      cdli_docs: 'https://cdli.earth/docs/search',
      epsd2_meluhha_entry: epsd2Url,
    },
    query_summaries: querySummaries,
    counts: {
      distinct_cdli_artifacts_across_queries: artifactRows.length,
      line_context_rows: lineRows.length,
      lu_sunzida_line_rows: luRows.length,
      lu_sunzida_distinct_artifacts: luArtifactIds.size,
      lu_sunzida_artifacts_with_any_meluhha_line: luMeluhhaArtifactIds.size,
      lu_sunzida_artifacts_with_adjacent_meluhha_line: luAdjacentArtifactIds.size,
      epsd2_meluhha_instances_reported: epsd2Instances,
      epsd2_meluhha_spellings_reported: epsd2Spellings,
    },
    lu_sunzida_detector_test: {
      hypothesis: 'The cuneiform string lu2-sun2-zi-da can be used as a Meluhha diagnostic personal-name anchor.',
      decision: 'rejected_as_meluhha_diagnostic_anchor',
      false_positive_artifacts_if_name_alone_marks_meluhha: luFalsePositiveArtifacts,
      false_positive_rate_if_name_alone_marks_meluhha: luFalsePositiveRate,
      non_adjacent_or_no_meluhha_rate_if_name_alone_requires_adjacent_meluhha: luAdjacentOnlyRate,
      surviving_residue: 'P212982 still preserves a locally real adjacency, lu2-sun2-zi-da immediately before lu2 me-luh-ha-ke4. It remains a cuneiform-side lead only, not an Indus sign-value anchor, because the name is not diagnostic across CDLI current hits and there is no paired external Indus object.',
    },
    files: {
      fetch_log: rel(path.join(OUT, 'cdli_current_query_fetch_log.csv')),
      artifacts: rel(path.join(OUT, 'cdli_current_meluhha_artifacts.csv')),
      line_contexts: rel(path.join(OUT, 'cdli_current_line_contexts.csv')),
      lu_sunzida_test: rel(path.join(OUT, 'cdli_current_lu_sunzida_test.csv')),
      summary: rel(path.join(OUT, 'cdli_current_anchor_failure_summary.json')),
    },
    caveats: [
      'This is a current CDLI/ORACC digital-source export, not a comprehensive Assyriological publication catalogue.',
      'CDLI search behavior is treated as an empirical source route and is source-hashed in the fetch log.',
      'The Lu-sunzida rejection concerns diagnostic use of the name alone. It does not prove that P212982 line 5 is unrelated to the Meluhha title in line 6.',
      'No Indus phonetic value, sign meaning, language identification, or translation is accepted.',
    ],
  };

  writeCsv(path.join(OUT, 'cdli_current_query_fetch_log.csv'), fetchRows, FETCH_FIELDS);
  writeCsv(path.join(OUT, 'cdli_current_meluhha_artifacts.csv'), artifactRows, CDLI_ARTIFACT_FIELDS);
  writeCsv(path.join(OUT, 'cdli_current_line_contexts.csv'), lineRows.sort((a, b) => `${a.artifact_p}:${a.line_index}:${a.query_term}`.localeCompare(`${b.artifact_p}:${b.line_index}:${b.query_term}`)), LINE_FIELDS);
  writeCsv(path.join(OUT, 'cdli_current_lu_sunzida_test.csv'), luRows.sort((a, b) => `${a.artifact_p}:${a.line_index}`.localeCompare(`${b.artifact_p}:${b.line_index}`)), LU_FIELDS);
  fs.writeFileSync(path.join(OUT, 'cdli_current_anchor_failure_summary.json'), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
