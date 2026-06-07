import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const OUT = path.join(ROOT, 'data', 'meluhha');
const RUN_DATE = '2026-05-29';
const USER_AGENT = 'codex-ivc-cdli-context-lead-negatives/2026-05-29';
const PAGE_LIMIT = 100;
const MAX_PAGES = 5;

const QUERY_PLAN_IN = path.join(OUT, 'cdli_meluhha_context_lead_query_plan.csv');
const SUMMARY_CSV = path.join(OUT, 'cdli_context_lead_matched_negative_summary.csv');
const ARTIFACTS_CSV = path.join(OUT, 'cdli_context_lead_matched_negative_artifacts.csv');
const FETCH_LOG_CSV = path.join(OUT, 'cdli_context_lead_matched_negative_fetch_log.csv');
const SUMMARY_JSON = path.join(OUT, 'cdli_context_lead_matched_negative_summary.json');

const SKIP_OVERBROAD_QUERIES = new Set([
  'ma2',
  'gug',
  'uruda',
  'nagga',
  'ku3',
  'NE',
  'i3-ba',
  'dumu',
  'kiszib3',
  'ugula',
  'sipa',
  'a-ru-a',
  'i3-dub',
  'e2-duru5',
  'eme-bal',
  '{gesz}guzza',
  '{gesz}ab-ba',
  '{gesz}kiri6',
  'dilmun{ki}',
  'ma2-gan{ki}',
]);

const EXTRA_NEGATIVE_QUERIES = [
  {
    rank: 1,
    lead_label: 'Shu-ilishu interpreter seal',
    lead_class: 'onomastic_interpreter_title',
    query_role: 'matched_negative',
    query_text: 'szu-i3-li2-su',
    rationale: 'Does the interpreter personal name occur away from the Meluhha title?',
  },
  {
    rank: 2,
    lead_label: 'Irisagrig Meluhha ration group',
    lead_class: 'ration_group_person_cluster',
    query_role: 'matched_negative',
    query_text: 'a-li-a-hi dam-a-ni',
    rationale: 'Does the adjacent name-plus-relation phrase occur away from Meluhha?',
  },
  {
    rank: 3,
    lead_label: 'Meluhha ship/work context',
    lead_class: 'ship_labor_context',
    query_role: 'matched_negative',
    query_text: 'lu2-tukul',
    rationale: 'Does the work/title lead occur without the Meluhha ship phrase?',
  },
  {
    rank: 3,
    lead_label: 'Meluhha ship/work context',
    lead_class: 'ship_labor_context',
    query_role: 'matched_negative',
    query_text: 'gurusz',
    rationale: 'Broad laborer control; retained only if CDLI result size stays manageable.',
  },
  {
    rank: 3,
    lead_label: 'Meluhha ship/work context',
    lead_class: 'ship_labor_context',
    query_role: 'matched_negative',
    query_text: 'nu-banda3',
    rationale: 'Supervisor/control title around Meluhha ships.',
  },
  {
    rank: 4,
    lead_label: 'Carnelian from Meluhha',
    lead_class: 'commodity_material_context',
    query_role: 'matched_negative',
    query_text: 'gug gi-rin',
    rationale: 'Does carnelian cluster specifically with Meluhha or broadly with prestige commodities?',
  },
  {
    rank: 6,
    lead_label: 'Meluhha copper',
    lead_class: 'commodity_material_context',
    query_role: 'matched_negative',
    query_text: 'nagga uruda',
    rationale: 'Matched material-control phrase near the copper lead.',
  },
  {
    rank: 7,
    lead_label: 'i3-dub Meluhha formula',
    lead_class: 'administrative_formula',
    query_role: 'matched_negative',
    query_text: 'i3-dub me-luh-ha',
    rationale: 'Meluhha-attached formula; retained as source-side cuneiform context only.',
  },
  {
    rank: 8,
    lead_label: 'e2-duru5 Meluhha estate',
    lead_class: 'estate_settlement_context',
    query_role: 'matched_negative',
    query_text: 'e2-duru5 me-luh-ha',
    rationale: 'Meluhha-attached estate phrase; retained as source-side cuneiform context only.',
  },
  {
    rank: 9,
    lead_label: 'sons of Meluhha',
    lead_class: 'patronymic_origin_formula',
    query_role: 'matched_negative',
    query_text: 'ur-{d}lamma dumu me-luh-ha',
    rationale: 'Specific name-plus-origin formula in the current export.',
  },
  {
    rank: 10,
    lead_label: 'ugula Meluhha title',
    lead_class: 'title_singleton',
    query_role: 'matched_negative',
    query_text: '_ARAD2_ {d}nansze-me',
    rationale: 'Adjacent name/control for the damaged `ugula# me-luh-ha` singleton.',
  },
  {
    rank: 13,
    lead_label: 'Meluhha route-control lane',
    lead_class: 'route_toponym_control',
    query_role: 'matched_negative',
    query_text: 'ma2-gan me-luh-ha',
    rationale: 'Route-control phrase involving Meluhha and Magan.',
  },
  {
    rank: 14,
    lead_label: 'Meluhha speckled dog/object',
    lead_class: 'animal_object_modifier',
    query_role: 'matched_negative',
    query_text: 'ur gun3-a',
    rationale: 'Object/animal modifier control for the speckled Meluhha lead.',
  },
];

const SUMMARY_FIELDS = [
  'query_id',
  'rank',
  'lead_label',
  'lead_class',
  'query_role',
  'query_text',
  'status',
  'cdli_url',
  'http_status',
  'byte_length',
  'page_count',
  'page_cap_reached',
  'returned_artifacts',
  'query_line_artifacts',
  'unique_inscription_hashes',
  'duplicate_cluster_count',
  'max_duplicate_cluster_size',
  'artifacts_with_meluhha_anywhere',
  'artifacts_with_query_line_and_meluhha_anywhere',
  'artifacts_with_query_line_adjacent_to_meluhha',
  'artifacts_with_query_line_same_as_meluhha',
  'query_line_anywhere_false_positive_rate',
  'query_line_adjacency_false_positive_rate',
  'passes_negative_gate',
  'gate_reason',
  'meluhha_artifact_ps',
  'non_meluhha_artifact_ps',
  'rationale',
];

const ARTIFACT_FIELDS = [
  'query_id',
  'query_text',
  'lead_label',
  'query_role',
  'artifact_p',
  'artifact_id',
  'designation',
  'museum_no',
  'provenience',
  'period',
  'dates_referenced',
  'query_line_count',
  'meluhha_line_count',
  'min_query_to_meluhha_distance',
  'has_meluhha_anywhere',
  'query_line_same_as_meluhha',
  'query_line_adjacent_to_meluhha',
  'inscription_hash',
  'source_url',
  'query_lines',
  'meluhha_lines',
];

const FETCH_FIELDS = [
  'fetch_id',
  'query_id',
  'query_text',
  'url',
  'page',
  'http_status',
  'byte_length',
  'sha256',
  'error',
];

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
  for (const row of rows) lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function sha256Text(text) {
  return crypto.createHash('sha256').update(text, 'utf8').digest('hex');
}

function stableId(parts) {
  return crypto.createHash('sha1').update(parts.join('\u241f'), 'utf8').digest('hex').slice(0, 16);
}

function textValue(value) {
  if (value == null) return '';
  if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') return String(value);
  if (Array.isArray(value)) return value.map(textValue).filter(Boolean).join('|');
  if (typeof value === 'object') {
    for (const key of ['label', 'name', 'term', 'value', 'designation']) {
      if (value[key]) return textValue(value[key]);
    }
    return JSON.stringify(value);
  }
  return String(value);
}

function artifactField(row, field) {
  return textValue(row[field] ?? row.artifact?.[field] ?? row.metadata?.[field]);
}

function artifactP(id) {
  return `P${String(id).padStart(6, '0')}`;
}

function cleanLineText(line) {
  return String(line ?? '').replace(/^\s*\d+'?\.?\s*/, '').trim();
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

function normalizeAtf(text) {
  return cleanLineText(text)
    .toLowerCase()
    .replace(/[#?!]/g, '')
    .replace(/\[[^\]]*?\]/g, '')
    .replace(/[.,;:]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function normalizeLoose(text) {
  return normalizeAtf(text).replace(/[{()}_]/g, '').replace(/\s+/g, ' ').trim();
}

function termMatches(text, query) {
  const normalizedText = normalizeAtf(text);
  const normalizedQuery = normalizeAtf(query);
  if (normalizedText.includes(normalizedQuery)) return true;
  return normalizeLoose(text).includes(normalizeLoose(query));
}

function hasMeluhha(text) {
  return /me-luh-ha/.test(normalizeAtf(text));
}

function minDistance(queryIndexes, meluhhaIndexes) {
  if (!queryIndexes.length || !meluhhaIndexes.length) return '';
  let best = Infinity;
  for (const q of queryIndexes) {
    for (const m of meluhhaIndexes) best = Math.min(best, Math.abs(q - m));
  }
  return String(best);
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

function shouldIncludeQuery(row) {
  const query = row.query_text;
  if (!query) return false;
  if (SKIP_OVERBROAD_QUERIES.has(query)) return false;
  const verified = Number(row.verified_context_count ?? 0);
  const role = row.query_role;
  if (role === 'diagnostic' && verified > 0) return true;
  if (role === 'anchor' && verified > 0) return true;
  if (role === 'control' && verified > 0 && query.split(/\s+/).length > 1) return true;
  return false;
}

function dedupeQueries(rows) {
  const byKey = new Map();
  for (const row of rows) {
    const key = row.query_text;
    const existing = byKey.get(key);
    if (!existing) {
      byKey.set(key, row);
      continue;
    }
    const priority = { anchor: 0, matched_negative: 1, diagnostic: 2, control: 3 };
    const existingPriority = priority[existing.query_role] ?? 9;
    const rowPriority = priority[row.query_role] ?? 9;
    if (Number(row.rank) < Number(existing.rank) || (Number(row.rank) === Number(existing.rank) && rowPriority < existingPriority)) {
      byKey.set(key, row);
    }
  }
  return [...byKey.values()].sort((a, b) => Number(a.rank) - Number(b.rank) || a.query_text.localeCompare(b.query_text));
}

function artifactDecision(artifacts) {
  const queryLineArtifacts = artifacts.filter((row) => Number(row.query_line_count) > 0);
  const queryLineArtifactCount = queryLineArtifacts.length;
  const withMeluhha = queryLineArtifacts.filter((row) => row.has_meluhha_anywhere === 'true');
  const adjacent = queryLineArtifacts.filter((row) => row.query_line_adjacent_to_meluhha === 'true');
  const same = queryLineArtifacts.filter((row) => row.query_line_same_as_meluhha === 'true');
  const anywhereFpr = queryLineArtifactCount ? (queryLineArtifactCount - withMeluhha.length) / queryLineArtifactCount : null;
  const adjacentFpr = queryLineArtifactCount ? (queryLineArtifactCount - adjacent.length) / queryLineArtifactCount : null;

  if (queryLineArtifactCount === 0) {
    return {
      passes: 'false',
      reason: 'No parseable returned artifacts contain an exact query line after local normalization.',
      anywhereFpr,
      adjacentFpr,
    };
  }
  if (queryLineArtifactCount < 2) {
    return {
      passes: 'false',
      reason: 'Singleton or non-replicated source-side hit; retained as a lead, not accepted evidence.',
      anywhereFpr,
      adjacentFpr,
    };
  }
  if (anywhereFpr > 0.2) {
    return {
      passes: 'false',
      reason: `Anchor is not Meluhha-diagnostic: ${(anywhereFpr * 100).toFixed(1)}% of query-line artifacts lack any Meluhha line.`,
      anywhereFpr,
      adjacentFpr,
    };
  }
  if (adjacentFpr > 0.5) {
    return {
      passes: 'false',
      reason: `Anchor is not adjacency-diagnostic: ${(adjacentFpr * 100).toFixed(1)}% of query-line artifacts lack adjacent Meluhha.`,
      anywhereFpr,
      adjacentFpr,
    };
  }
  return {
    passes: 'candidate_only',
    reason: 'Matched-negative gate did not reject this source-side cuneiform lead; it still requires duplicate-edition review and external-object linkage before any claim.',
    anywhereFpr,
    adjacentFpr,
  };
}

async function main() {
  const planRows = parseCsv(fs.readFileSync(QUERY_PLAN_IN, 'utf8'));
  const extraRows = EXTRA_NEGATIVE_QUERIES.map((row) => ({
    lead_id: `extra_${stableId([row.lead_label, row.query_text])}`,
    ...row,
    verified_context_count: '',
    artifact_count: '',
    artifact_ps: '',
  }));
  const queries = dedupeQueries([...planRows.filter(shouldIncludeQuery), ...extraRows]);

  const summaryRows = [];
  const artifactRows = [];
  const fetchRows = [];

  for (const queryRow of queries) {
    const queryId = `mn_${stableId([queryRow.rank, queryRow.lead_label, queryRow.query_role, queryRow.query_text])}`;
    const baseUrl = `https://cdli.earth/search?atf_transliteration=${encodeURIComponent(queryRow.query_text)}&format=json&limit=${PAGE_LIMIT}`;
    const rowsById = new Map();
    let fetchError = '';
    let parseError = '';
    let lastStatus = '';
    let totalBytes = 0;
    let pageCount = 0;
    let pageCapReached = false;

    for (let page = 1; page <= MAX_PAGES; page += 1) {
      const url = `${baseUrl}&page=${page}`;
      const result = await fetchText(url);
      pageCount = page;
      lastStatus = result.status;
      totalBytes += result.byteLength;
      fetchRows.push({
        fetch_id: `fetch_${stableId([queryId, url])}`,
        query_id: queryId,
        query_text: queryRow.query_text,
        url,
        page,
        http_status: result.status,
        byte_length: result.byteLength,
        sha256: result.sha256,
        error: result.error,
      });

      if (!result.ok) {
        fetchError = result.error;
        break;
      }

      let pageRows;
      try {
        pageRows = JSON.parse(result.text);
      } catch (error) {
        parseError = error instanceof Error ? error.message : String(error);
        break;
      }
      if (!Array.isArray(pageRows)) {
        parseError = 'CDLI JSON response was not an array.';
        break;
      }
      for (const row of pageRows) rowsById.set(row.id, row);
      if (pageRows.length < PAGE_LIMIT) break;
      if (page === MAX_PAGES) pageCapReached = true;
    }

    if (fetchError) {
      summaryRows.push({
        query_id: queryId,
        rank: queryRow.rank,
        lead_label: queryRow.lead_label,
        lead_class: queryRow.lead_class,
        query_role: queryRow.query_role,
        query_text: queryRow.query_text,
        status: 'fetch_error',
        cdli_url: baseUrl,
        http_status: lastStatus,
        byte_length: totalBytes,
        page_count: pageCount,
        page_cap_reached: pageCapReached ? 'true' : 'false',
        returned_artifacts: 0,
        gate_reason: fetchError,
        rationale: queryRow.rationale,
      });
      continue;
    }

    if (parseError) {
      summaryRows.push({
        query_id: queryId,
        rank: queryRow.rank,
        lead_label: queryRow.lead_label,
        lead_class: queryRow.lead_class,
        query_role: queryRow.query_role,
        query_text: queryRow.query_text,
        status: 'parse_error',
        cdli_url: baseUrl,
        http_status: lastStatus,
        byte_length: totalBytes,
        page_count: pageCount,
        page_cap_reached: pageCapReached ? 'true' : 'false',
        returned_artifacts: 0,
        gate_reason: parseError,
        rationale: queryRow.rationale,
      });
      continue;
    }

    const rows = [...rowsById.values()];
    const localArtifacts = [];
    const hashCounts = new Map();
    for (const row of rows) {
      const id = row.id;
      const p = artifactP(id);
      const atf = row.inscription?.atf ?? '';
      const inscriptionHash = sha256Text(atf);
      hashCounts.set(inscriptionHash, (hashCounts.get(inscriptionHash) ?? 0) + 1);
      const lines = parseAtfLines(atf);
      const queryIndexes = [];
      const meluhhaIndexes = [];
      lines.forEach((line, idx) => {
        if (termMatches(line.raw, queryRow.query_text)) queryIndexes.push(idx);
        if (hasMeluhha(line.raw)) meluhhaIndexes.push(idx);
      });
      const sameAsMeluhha = queryIndexes.some((idx) => meluhhaIndexes.includes(idx));
      const adjacentToMeluhha = queryIndexes.some((q) => meluhhaIndexes.some((m) => Math.abs(q - m) <= 1));
      const artifact = {
        query_id: queryId,
        query_text: queryRow.query_text,
        lead_label: queryRow.lead_label,
        query_role: queryRow.query_role,
        artifact_p: p,
        artifact_id: id,
        designation: row.designation ?? '',
        museum_no: row.museum_no ?? '',
        provenience: artifactField(row, 'provenience'),
        period: artifactField(row, 'period'),
        dates_referenced: textValue(row.dates_referenced),
        query_line_count: queryIndexes.length,
        meluhha_line_count: meluhhaIndexes.length,
        min_query_to_meluhha_distance: minDistance(queryIndexes, meluhhaIndexes),
        has_meluhha_anywhere: meluhhaIndexes.length ? 'true' : 'false',
        query_line_same_as_meluhha: sameAsMeluhha ? 'true' : 'false',
        query_line_adjacent_to_meluhha: adjacentToMeluhha ? 'true' : 'false',
        inscription_hash: inscriptionHash,
        source_url: `https://cdli.earth/${p}`,
        query_lines: queryIndexes.map((idx) => lines[idx]?.raw).filter(Boolean).join(' | '),
        meluhha_lines: meluhhaIndexes.map((idx) => lines[idx]?.raw).filter(Boolean).join(' | '),
      };
      localArtifacts.push(artifact);
      artifactRows.push(artifact);
    }

    const decision = artifactDecision(localArtifacts);
    const queryLineArtifacts = localArtifacts.filter((row) => Number(row.query_line_count) > 0);
    const meluhhaArtifactPs = queryLineArtifacts.filter((row) => row.has_meluhha_anywhere === 'true').map((row) => row.artifact_p);
    const nonMeluhhaArtifactPs = queryLineArtifacts.filter((row) => row.has_meluhha_anywhere !== 'true').map((row) => row.artifact_p);
    const duplicateClusterSizes = [...hashCounts.values()].filter((count) => count > 1);

    summaryRows.push({
      query_id: queryId,
      rank: queryRow.rank,
      lead_label: queryRow.lead_label,
      lead_class: queryRow.lead_class,
      query_role: queryRow.query_role,
      query_text: queryRow.query_text,
      status: 'ok',
      cdli_url: baseUrl,
      http_status: lastStatus,
      byte_length: totalBytes,
      page_count: pageCount,
      page_cap_reached: pageCapReached ? 'true' : 'false',
      returned_artifacts: rows.length,
      query_line_artifacts: queryLineArtifacts.length,
      unique_inscription_hashes: hashCounts.size,
      duplicate_cluster_count: duplicateClusterSizes.length,
      max_duplicate_cluster_size: duplicateClusterSizes.length ? Math.max(...duplicateClusterSizes) : 1,
      artifacts_with_meluhha_anywhere: localArtifacts.filter((row) => row.has_meluhha_anywhere === 'true').length,
      artifacts_with_query_line_and_meluhha_anywhere: meluhhaArtifactPs.length,
      artifacts_with_query_line_adjacent_to_meluhha: queryLineArtifacts.filter((row) => row.query_line_adjacent_to_meluhha === 'true').length,
      artifacts_with_query_line_same_as_meluhha: queryLineArtifacts.filter((row) => row.query_line_same_as_meluhha === 'true').length,
      query_line_anywhere_false_positive_rate: decision.anywhereFpr == null ? '' : decision.anywhereFpr.toFixed(6),
      query_line_adjacency_false_positive_rate: decision.adjacentFpr == null ? '' : decision.adjacentFpr.toFixed(6),
      passes_negative_gate: decision.passes,
      gate_reason: decision.reason,
      meluhha_artifact_ps: [...new Set(meluhhaArtifactPs)].sort().join('|'),
      non_meluhha_artifact_ps: [...new Set(nonMeluhhaArtifactPs)].sort().join('|'),
      rationale: queryRow.rationale,
    });
  }

  const candidateOnly = summaryRows.filter((row) => row.passes_negative_gate === 'candidate_only');
  const summary = {
    run_date: RUN_DATE,
    query_count: queries.length,
    ok_query_count: summaryRows.filter((row) => row.status === 'ok').length,
    candidate_only_count: candidateOnly.length,
    accepted_external_anchor_count: 0,
    outputs: {
      summary_csv: path.relative(ROOT, SUMMARY_CSV).replaceAll('\\', '/'),
      artifacts_csv: path.relative(ROOT, ARTIFACTS_CSV).replaceAll('\\', '/'),
      fetch_log_csv: path.relative(ROOT, FETCH_LOG_CSV).replaceAll('\\', '/'),
    },
    candidate_only_queries: candidateOnly.map((row) => ({
      query_text: row.query_text,
      lead_label: row.lead_label,
      query_line_artifacts: Number(row.query_line_artifacts),
      adjacency_false_positive_rate: row.query_line_adjacency_false_positive_rate,
      gate_reason: row.gate_reason,
    })),
    decision: 'No Indus phonetic value, sign meaning, language identification, translation, or external anchor is accepted from this matched-negative run.',
    caveats: [
      'Queries that already contain `me-luh-ha` are source-side cuneiform contexts, not negative controls.',
      'Broad one-token controls likely to return very large CDLI result sets were skipped and recorded in the script constant.',
      'A source-side candidate_only result means the CDLI matched-negative gate did not reject the phrase; it does not bypass duplicate-edition review or object-level external linkage.',
    ],
  };

  writeCsv(SUMMARY_CSV, summaryRows, SUMMARY_FIELDS);
  writeCsv(ARTIFACTS_CSV, artifactRows, ARTIFACT_FIELDS);
  writeCsv(FETCH_LOG_CSV, fetchRows, FETCH_FIELDS);
  fs.writeFileSync(SUMMARY_JSON, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
