// Corpus scoping survey: before any analysis, we need to know how much of the
// lipi metadata is actually usable. This script reads every row of
// lipi/metadata_filtered.csv and grades it into one of three readiness
// buckets. A "lipi_numeric_clean_candidate" has a catalog id, a fully parsed
// numeric sign sequence, complete=Y, an R/L or L/R direction, no uncertainty
// markers (?, brackets, slashes, or the unknown-sign code 000), and a stated
// text length that matches the parsed sign count. A
// "lipi_direction_clean_candidate" relaxes completeness and some markers;
// everything else is "audit_or_scope_only".
//
// It also cross-tabulates rows by object type, site, region, direction, and
// text length, and counts every data-quality flag (length disagreements,
// question marks, brackets, slashes, 000 signs).
//
// Outputs: lipi_scope_rows.csv (the per-row grading that most downstream
// probes consume) plus nine breakdown CSVs and lipi_scope_summary.json.
// Pure inventory work — it makes no claim about what any sign means.

import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const sourcePath = path.join(base, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const outRows = path.join(reportsDir, 'lipi_scope_rows.csv');
const outType = path.join(reportsDir, 'lipi_scope_by_type.csv');
const outSite = path.join(reportsDir, 'lipi_scope_by_site.csv');
const outRegion = path.join(reportsDir, 'lipi_scope_by_region.csv');
const outTypeDirection = path.join(reportsDir, 'lipi_scope_by_type_direction.csv');
const outLengthType = path.join(reportsDir, 'lipi_scope_length_by_type.csv');
const outReadiness = path.join(reportsDir, 'lipi_scope_readiness_summary.csv');
const outCandidateType = path.join(reportsDir, 'lipi_scope_candidates_by_type.csv');
const outCandidateSite = path.join(reportsDir, 'lipi_scope_candidates_by_site.csv');
const outJson = path.join(reportsDir, 'lipi_scope_summary.json');

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQuotes) {
      if (c === '"') {
        if (text[i + 1] === '"') {
          field += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        field += c;
      }
    } else if (c === '"') {
      inQuotes = true;
    } else if (c === ',') {
      row.push(field);
      field = '';
    } else if (c === '\n') {
      row.push(field);
      field = '';
      if (row.length > 1 || row[0] !== '') rows.push(row);
      row = [];
    } else if (c !== '\r') {
      field += c;
    }
  }
  if (field.length || row.length) {
    row.push(field);
    rows.push(row);
  }
  return rows;
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

function norm(value) {
  const text = String(value ?? '').trim();
  return text === '' ? '-' : text;
}

function cleanDirection(value) {
  const text = norm(value).replace(/\s+/g, '').toUpperCase();
  if (text === 'R/L' || text === 'L/R' || text === 'T/B') return text;
  return text || '-';
}

function parseTokens(text) {
  const raw = norm(text);
  const tokens = raw.match(/\d{3}/g) ?? [];
  const nonDigits = raw.replace(/[0-9+\-/[\]().?A-Za-z\s:;,_]/g, '');
  return {
    tokens,
    tokenCount: tokens.length,
    hasUnknownZero: tokens.includes('000'),
    hasQuestion: raw.includes('?'),
    hasBracket: raw.includes('[') || raw.includes(']') || raw.includes('(') || raw.includes(')'),
    hasSlash: raw.includes('/'),
    hasText: raw !== '-' && raw !== '',
    nonDigits,
  };
}

function normalizeLength(value) {
  const text = norm(value);
  const match = text.match(/^(\d+)/);
  return match ? Number.parseInt(match[1], 10) : null;
}

function bump(map, key, by = 1) {
  map.set(key, (map.get(key) ?? 0) + by);
}

function formatLocalIso(date) {
  const offsetMinutes = -date.getTimezoneOffset();
  const sign = offsetMinutes >= 0 ? '+' : '-';
  const absMinutes = Math.abs(offsetMinutes);
  const pad = (value) => String(value).padStart(2, '0');
  const offset = `${sign}${pad(Math.floor(absMinutes / 60))}:${pad(absMinutes % 60)}`;
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(
    date.getHours(),
  )}:${pad(date.getMinutes())}:${pad(date.getSeconds())}${offset}`;
}

function mapRows(map, headers) {
  return [
    headers,
    ...[...map.entries()]
      .map(([key, count]) => [...key.split('\t'), count])
      .sort((a, b) => Number(b.at(-1)) - Number(a.at(-1)) || a.join('\t').localeCompare(b.join('\t'))),
  ];
}

function ensureCandidateBucket(map, key) {
  if (!map.has(key)) {
    map.set(key, {
      rows: 0,
      lipi_numeric_clean_candidates: 0,
      lipi_direction_clean_candidates: 0,
      audit_or_scope_only: 0,
    });
  }
  return map.get(key);
}

function candidateRows(map, firstHeader) {
  return [
    [
      firstHeader,
      'rows',
      'lipi_numeric_clean_candidates',
      'lipi_direction_clean_candidates',
      'direction_extra_after_numeric_clean',
      'audit_or_scope_only',
    ],
    ...[...map.entries()]
      .map(([key, counts]) => [
        key,
        counts.rows,
        counts.lipi_numeric_clean_candidates,
        counts.lipi_direction_clean_candidates,
        Math.max(0, counts.lipi_direction_clean_candidates - counts.lipi_numeric_clean_candidates),
        counts.audit_or_scope_only,
      ])
      .sort((a, b) => Number(b[2]) - Number(a[2]) || Number(b[1]) - Number(a[1]) || a[0].localeCompare(b[0])),
  ];
}

const rows = parseCsv(fs.readFileSync(sourcePath, 'utf8'));
const header = rows[0];
const column = Object.fromEntries(header.map((name, index) => [name, index]));

const scopedRows = [];
const byType = new Map();
const bySite = new Map();
const byRegion = new Map();
const byTypeDirection = new Map();
const byLengthType = new Map();
const byReadiness = new Map();
const candidateByType = new Map();
const candidateBySite = new Map();

let rowsWithCisi = 0;
let rowsWithText = 0;
let rowsWithNumericText = 0;
let rowsCompleteY = 0;
let rowsDirectional = 0;
let rowsDirectionRl = 0;
let rowsDirectionLr = 0;
let rowsDirectionTb = 0;
let rowsLipiNumericCleanCandidates = 0;
let rowsLipiDirectionCleanCandidates = 0;
let rowsLengthMatchesParsed = 0;
let rowsLengthDisagreesParsed = 0;
let rowsComplexText = 0;
let rowsUnknownZero = 0;
let rowsSlash = 0;
let rowsQuestion = 0;
let rowsBracket = 0;

for (const row of rows.slice(1)) {
  const id = norm(row[column.id]);
  const cisi = norm(row[column.cisi]);
  const region = norm(row[column.region]);
  const site = norm(row[column.site]);
  const type = norm(row[column.type]);
  const material = norm(row[column.material]);
  const symbol = norm(row[column.symbol]);
  const cult = norm(row[column.cult]);
  const complete = norm(row[column.complete]);
  const direction = cleanDirection(row[column['dir.']]);
  const classValue = norm(row[column.class]);
  const lengthRaw = norm(row[column['text length']]);
  const signsRaw = norm(row[column.signs]);
  const text = norm(row[column.text]);
  const parsed = parseTokens(text);
  const lengthNumeric = normalizeLength(lengthRaw);
  const signsNumeric = normalizeLength(signsRaw);

  const hasCisi = cisi !== '-' && cisi !== '';
  const directional = direction === 'R/L' || direction === 'L/R' || direction === 'T/B';
  const directionRlLr = direction === 'R/L' || direction === 'L/R';
  const textNumeric = parsed.hasText && parsed.tokenCount > 0;
  const lengthMatches =
    lengthNumeric !== null && parsed.tokenCount > 0 && lengthNumeric === parsed.tokenCount;
  const hasComplexText =
    parsed.hasQuestion || parsed.hasBracket || parsed.hasSlash || parsed.hasUnknownZero;
  const lipiNumericCleanCandidate =
    hasCisi &&
    textNumeric &&
    complete === 'Y' &&
    directionRlLr &&
    !hasComplexText &&
    lengthMatches;
  const lipiDirectionCleanCandidate =
    hasCisi && textNumeric && directionRlLr && !parsed.hasQuestion && !parsed.hasBracket && lengthMatches;

  if (hasCisi) rowsWithCisi++;
  if (parsed.hasText) rowsWithText++;
  if (textNumeric) rowsWithNumericText++;
  if (complete === 'Y') rowsCompleteY++;
  if (directional) rowsDirectional++;
  if (direction === 'R/L') rowsDirectionRl++;
  if (direction === 'L/R') rowsDirectionLr++;
  if (direction === 'T/B') rowsDirectionTb++;
  if (lipiNumericCleanCandidate) rowsLipiNumericCleanCandidates++;
  if (lipiDirectionCleanCandidate) rowsLipiDirectionCleanCandidates++;
  if (lengthMatches) rowsLengthMatchesParsed++;
  if (lengthNumeric !== null && parsed.tokenCount > 0 && lengthNumeric !== parsed.tokenCount) {
    rowsLengthDisagreesParsed++;
  }
  if (hasComplexText) rowsComplexText++;
  if (parsed.hasUnknownZero) rowsUnknownZero++;
  if (parsed.hasSlash) rowsSlash++;
  if (parsed.hasQuestion) rowsQuestion++;
  if (parsed.hasBracket) rowsBracket++;

  const readiness = lipiNumericCleanCandidate
    ? 'lipi_numeric_clean_candidate'
    : lipiDirectionCleanCandidate
      ? 'lipi_direction_clean_candidate'
      : 'audit_or_scope_only';
  bump(byReadiness, readiness);
  bump(byType, type);
  bump(bySite, site);
  bump(byRegion, region);
  bump(byTypeDirection, `${type}\t${direction}`);
  bump(byLengthType, `${type}\t${lengthRaw}`);

  const typeCandidate = ensureCandidateBucket(candidateByType, type);
  const siteCandidate = ensureCandidateBucket(candidateBySite, site);
  for (const candidate of [typeCandidate, siteCandidate]) {
    candidate.rows++;
    if (lipiNumericCleanCandidate) candidate.lipi_numeric_clean_candidates++;
    if (lipiDirectionCleanCandidate) candidate.lipi_direction_clean_candidates++;
    if (!lipiDirectionCleanCandidate) candidate.audit_or_scope_only++;
  }

  scopedRows.push([
    id,
    cisi,
    region,
    site,
    type,
    material,
    symbol,
    cult,
    complete,
    direction,
    classValue,
    lengthRaw,
    signsRaw,
    parsed.tokenCount,
    lengthMatches,
    parsed.hasUnknownZero,
    parsed.hasQuestion,
    parsed.hasBracket,
    parsed.hasSlash,
    hasComplexText,
    readiness,
    text,
  ]);
}

const totalRows = rows.length - 1;
const summary = {
  generated_at_local: formatLocalIso(new Date()),
  source_file: 'data/open_prototype/lipi/metadata_filtered.csv',
  rows: totalRows,
  rows_with_cisi: rowsWithCisi,
  rows_with_text: rowsWithText,
  rows_with_numeric_text: rowsWithNumericText,
  rows_complete_Y: rowsCompleteY,
  rows_directional_RL_LR_TB: rowsDirectional,
  rows_direction_RL: rowsDirectionRl,
  rows_direction_LR: rowsDirectionLr,
  rows_direction_TB: rowsDirectionTb,
  rows_lipi_numeric_clean_candidates: rowsLipiNumericCleanCandidates,
  rows_lipi_direction_clean_candidates: rowsLipiDirectionCleanCandidates,
  rows_length_matches_parsed: rowsLengthMatchesParsed,
  rows_length_disagrees_parsed: rowsLengthDisagreesParsed,
  rows_complex_text: rowsComplexText,
  rows_with_000_unknown: rowsUnknownZero,
  rows_with_slash: rowsSlash,
  rows_with_question: rowsQuestion,
  rows_with_bracket: rowsBracket,
  top_types: [...byType.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, 20)
    .map(([value, count]) => ({ value, count })),
  top_sites: [...bySite.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, 20)
    .map(([value, count]) => ({ value, count })),
  top_regions: [...byRegion.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([value, count]) => ({ value, count })),
  readiness_counts: [...byReadiness.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([value, count]) => ({ value, count })),
  artifact_files: [
    'data/open_prototype/reports/lipi_scope_rows.csv',
    'data/open_prototype/reports/lipi_scope_by_type.csv',
    'data/open_prototype/reports/lipi_scope_by_site.csv',
    'data/open_prototype/reports/lipi_scope_by_region.csv',
    'data/open_prototype/reports/lipi_scope_by_type_direction.csv',
    'data/open_prototype/reports/lipi_scope_length_by_type.csv',
    'data/open_prototype/reports/lipi_scope_readiness_summary.csv',
    'data/open_prototype/reports/lipi_scope_candidates_by_type.csv',
    'data/open_prototype/reports/lipi_scope_candidates_by_site.csv',
    'data/open_prototype/reports/lipi_scope_summary.json',
  ],
  interpretation_boundary:
    'Claim-free scope survey only; no sign value, semantic, phonetic, or translation claim.',
};

fs.writeFileSync(
  outRows,
  toCsv([
    [
      'id',
      'cisi',
      'region',
      'site',
      'type',
      'material',
      'symbol',
      'cult',
      'complete',
      'direction',
      'class',
      'text_length_raw',
      'signs_raw',
      'parsed_token_count',
      'length_matches_parsed',
      'has_000_unknown',
      'has_question',
      'has_bracket',
      'has_slash',
      'has_complex_text',
      'readiness_bucket',
      'text',
    ],
    ...scopedRows,
  ]),
  'utf8',
);
fs.writeFileSync(outType, toCsv(mapRows(byType, ['type', 'rows'])), 'utf8');
fs.writeFileSync(outSite, toCsv(mapRows(bySite, ['site', 'rows'])), 'utf8');
fs.writeFileSync(outRegion, toCsv(mapRows(byRegion, ['region', 'rows'])), 'utf8');
fs.writeFileSync(outTypeDirection, toCsv(mapRows(byTypeDirection, ['type', 'direction', 'rows'])), 'utf8');
fs.writeFileSync(outLengthType, toCsv(mapRows(byLengthType, ['type', 'text_length_raw', 'rows'])), 'utf8');
fs.writeFileSync(outReadiness, toCsv(mapRows(byReadiness, ['readiness_bucket', 'rows'])), 'utf8');
fs.writeFileSync(outCandidateType, toCsv(candidateRows(candidateByType, 'type')), 'utf8');
fs.writeFileSync(outCandidateSite, toCsv(candidateRows(candidateBySite, 'site')), 'utf8');
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(
  JSON.stringify(
    {
      rows: summary.rows,
      rows_lipi_numeric_clean_candidates: summary.rows_lipi_numeric_clean_candidates,
      rows_lipi_direction_clean_candidates: summary.rows_lipi_direction_clean_candidates,
      top_types: summary.top_types.slice(0, 5),
      wrote: summary.artifact_files,
    },
    null,
    2,
  ),
);
