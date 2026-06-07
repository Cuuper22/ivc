import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const dataDir = path.join(base, 'data', 'open_prototype');
const reportsDir = path.join(dataDir, 'reports');
const lipiAuditPath = path.join(dataDir, 'lipi', 'audit_summary.json');
const filteredPath = path.join(dataDir, 'lipi', 'metadata_filtered.csv');
const scopePath = path.join(reportsDir, 'lipi_scope_rows.csv');

const outClassCounts = path.join(reportsDir, 'lipi_class_field_counts.csv');
const outByType = path.join(reportsDir, 'lipi_class_field_by_type.csv');
const outBySite = path.join(reportsDir, 'lipi_class_field_by_site.csv');
const outByLength = path.join(reportsDir, 'lipi_class_field_by_length.csv');
const outExamples = path.join(reportsDir, 'lipi_class_field_examples.csv');
const outJson = path.join(reportsDir, 'lipi_class_field_audit_summary.json');

const repo = 'yajnadevam/lipi';
const branch = 'main';
const rawBase = `https://raw.githubusercontent.com/${repo}/${branch}`;
const apiBase = `https://api.github.com/repos/${repo}`;
const checkedAt = new Date().toISOString();

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

function csvObjects(text) {
  const rows = parseCsv(text);
  const headers = rows.shift() ?? [];
  return rows.map((row) => Object.fromEntries(headers.map((header, index) => [header, row[index] ?? ''])));
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

function bump(map, key, by = 1) {
  map.set(key, (map.get(key) ?? 0) + by);
}

function nestedBump(map, keyA, keyB, by = 1) {
  if (!map.has(keyA)) map.set(keyA, new Map());
  bump(map.get(keyA), keyB, by);
}

function topEntries(map, limit = 5) {
  return [...map.entries()].sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]))).slice(0, limit);
}

function countValues(rows, field) {
  const counts = new Map();
  for (const row of rows) {
    const value = String(row[field] ?? '').trim() || '(blank)';
    bump(counts, value);
  }
  return counts;
}

function numericTokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function round(value) {
  return Number(value.toFixed(6));
}

async function fetchText(url) {
  const response = await fetch(url, {
    headers: {
      'User-Agent': 'codex-ivc-research',
      Accept: 'text/plain, application/vnd.github+json',
    },
  });
  if (!response.ok) throw new Error(`Fetch failed ${response.status}: ${url}`);
  return response.text();
}

async function fetchJson(url) {
  const response = await fetch(url, {
    headers: {
      'User-Agent': 'codex-ivc-research',
      Accept: 'application/vnd.github+json',
    },
  });
  if (!response.ok) throw new Error(`Fetch failed ${response.status}: ${url}`);
  return response.json();
}

function scanTextFile(pathName, text, patterns) {
  const lines = text.split(/\r?\n/);
  const matches = [];
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    for (const pattern of patterns) {
      if (pattern.regex.test(line)) {
        matches.push({
          path: pathName,
          line_number: i + 1,
          pattern: pattern.name,
          line: line.trim().slice(0, 240),
        });
        break;
      }
    }
  }
  return matches;
}

function isDefinitionLike(match) {
  const line = match.line.toLowerCase();
  if (line.includes('class="') || line.includes(':class') || line.includes('classlist')) return false;
  if (line.includes('headers:') || line.includes('headerprops') || line.includes('cellprops')) return false;
  return (
    line.includes('class') &&
    (line.includes('means') ||
      line.includes('meaning') ||
      line.includes('definition') ||
      line.includes('legend') ||
      line.includes('code') ||
      line.includes('abbrev') ||
      line.includes('category') ||
      line.includes('type'))
  );
}

const lipiAudit = JSON.parse(fs.readFileSync(lipiAuditPath, 'utf8'));
const filteredRows = csvObjects(fs.readFileSync(filteredPath, 'utf8'));
const scopeRows = csvObjects(fs.readFileSync(scopePath, 'utf8'));
const numericCleanRows = scopeRows.filter((row) => row.readiness_bucket === 'lipi_numeric_clean_candidate');

const branchInfo = await fetchJson(`${apiBase}/branches/${branch}`);
const treeInfo = await fetchJson(`${apiBase}/git/trees/${branch}?recursive=1`);
const rawCsvText = await fetchText(lipiAudit.source_url);
const rawRows = csvObjects(rawCsvText);
const rawNonemptyLineRows = rawCsvText.split(/\r?\n/).filter((line) => line.trim().length > 0).length - 1;

const textPaths = treeInfo.tree
  .filter((entry) => entry.type === 'blob')
  .map((entry) => entry.path)
  .filter((pathName) => {
    if (pathName.startsWith('public/seal_images/')) return false;
    if (pathName.includes('mw.xml') || pathName.includes('dhatuforms_')) return false;
    return /\.(md|txt|csv|json|js|ts|vue)$/i.test(pathName);
  })
  .filter((pathName) => {
    if (pathName.startsWith('dev-tools/ashtadhyayi/assets/')) return false;
    if (pathName.startsWith('src/assets/data/dhatu')) return false;
    if (pathName.startsWith('src/assets/data/mw')) return false;
    if (pathName.startsWith('src/assets/data/prakriyas')) return false;
    return true;
  });

const classCodes = [...countValues(filteredRows, 'class').keys()].filter((code) => code !== '(blank)');
const codeRegex = new RegExp(`\\b(${classCodes.map((code) => code.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|')})\\b`);
const patterns = [
  { name: 'class_field', regex: /\bclass\b/i },
  { name: 'known_class_code', regex: codeRegex },
];

const sourceMatches = [];
for (const pathName of textPaths) {
  if (pathName === 'src/assets/data/inscriptions.csv') continue;
  try {
    const text = await fetchText(`${rawBase}/${pathName}`);
    sourceMatches.push(...scanTextFile(pathName, text, patterns));
  } catch {
    // GitHub rate limits and occasional binary/text mismatches should not block local source-field audit.
  }
}

const definitionMatches = sourceMatches.filter(isDefinitionLike);
const readme = await fetchText(`${rawBase}/README.md`);
const indexVue = await fetchText(`${rawBase}/src/pages/index.vue`);
const headerLine = rawCsvText.split(/\r?\n/)[0];

const allClassCounts = countValues(filteredRows, 'class');
const numericClassCounts = countValues(numericCleanRows, 'class');

const numericByClass = new Map();
const typeByClass = new Map();
const siteByClass = new Map();
const lengthByClass = new Map();
const completeByClass = new Map();

for (const row of filteredRows) {
  const cls = String(row.class ?? '').trim() || '(blank)';
  nestedBump(typeByClass, cls, String(row.type ?? '').trim() || '(blank)');
  nestedBump(siteByClass, cls, String(row.site ?? '').trim() || '(blank)');
  nestedBump(lengthByClass, cls, String(row['text length'] ?? '').trim() || '(blank)');
  nestedBump(completeByClass, cls, String(row.complete ?? '').trim() || '(blank)');
}

for (const row of numericCleanRows) {
  const cls = String(row.class ?? '').trim() || '(blank)';
  nestedBump(numericByClass, cls, 'rows');
}

const classCountRows = [
  ['class', 'all_rows', 'numeric_clean_rows', 'complete_y_rows', 'complete_y_share', 'top_type', 'top_type_share', 'top_site', 'top_site_share', 'top_length', 'top_length_share'],
];

for (const [cls, allCount] of topEntries(allClassCounts, allClassCounts.size)) {
  const numericCount = numericClassCounts.get(cls) ?? 0;
  const completeCounts = completeByClass.get(cls) ?? new Map();
  const completeY = completeCounts.get('Y') ?? 0;
  const topType = topEntries(typeByClass.get(cls) ?? new Map(), 1)[0] ?? ['', 0];
  const topSite = topEntries(siteByClass.get(cls) ?? new Map(), 1)[0] ?? ['', 0];
  const topLength = topEntries(lengthByClass.get(cls) ?? new Map(), 1)[0] ?? ['', 0];
  classCountRows.push([
    cls,
    allCount,
    numericCount,
    completeY,
    allCount ? round(completeY / allCount) : null,
    topType[0],
    allCount ? round(topType[1] / allCount) : null,
    topSite[0],
    allCount ? round(topSite[1] / allCount) : null,
    topLength[0],
    allCount ? round(topLength[1] / allCount) : null,
  ]);
}

function nestedRows(map, firstName, secondName) {
  const rows = [[firstName, secondName, 'count', 'share_within_class']];
  for (const [key, counts] of [...map.entries()].sort((a, b) => String(a[0]).localeCompare(String(b[0])))) {
    const total = [...counts.values()].reduce((sum, count) => sum + count, 0);
    for (const [value, count] of topEntries(counts, counts.size)) {
      rows.push([key, value, count, total ? round(count / total) : null]);
    }
  }
  return rows;
}

const exampleRows = [['class', 'id', 'cisi', 'type', 'site', 'complete', 'direction', 'text_length', 'signs', 'text']];
const seenExamples = new Map();
for (const row of filteredRows) {
  const cls = String(row.class ?? '').trim() || '(blank)';
  const count = seenExamples.get(cls) ?? 0;
  if (count >= 5) continue;
  seenExamples.set(cls, count + 1);
  exampleRows.push([
    cls,
    row.id,
    row.cisi,
    row.type,
    row.site,
    row.complete,
    row['dir.'],
    row['text length'],
    row.signs,
    row.text,
  ]);
}

const dataTableHeaderMentionsClass = /key:\s*["']class["']/.test(indexVue);
const readmeClaimsDeciphered = /deciphered/i.test(readme) && /translates/i.test(readme);
const rawColumns = headerLine.split(',');
const translationColumnsPresent = rawColumns.includes('sanskrit') && rawColumns.includes('translation') && rawColumns.includes('notes');
const classAdjacentToClaimColumns =
  rawColumns.indexOf('class') > -1 && rawColumns.indexOf('sanskrit') > -1 && rawColumns.indexOf('class') < rawColumns.indexOf('sanskrit');

const sourceAudit = {
  generated_at_local: checkedAt,
  repo,
  branch,
  branch_head_sha: branchInfo.commit.sha,
  source_url: lipiAudit.source_url,
  local_filtered_rows: filteredRows.length,
  remote_raw_nonempty_line_rows: rawNonemptyLineRows,
  remote_raw_parser_rows: rawRows.length,
  local_numeric_clean_rows: numericCleanRows.length,
  class_values_all_rows: allClassCounts.size,
  class_values_numeric_clean: numericClassCounts.size,
  raw_columns: rawColumns,
  quarantined_columns: lipiAudit.quarantined_columns,
  source_context: {
    readme_claims_deciphered: readmeClaimsDeciphered,
    translation_columns_present: translationColumnsPresent,
    remote_raw_parser_matches_local_line_count: rawRows.length === rawNonemptyLineRows,
    class_column_in_raw_csv: rawColumns.includes('class'),
    class_column_hidden_from_main_table_headers: !dataTableHeaderMentionsClass,
    class_column_before_claim_columns: classAdjacentToClaimColumns,
    class_definition_matches_found: definitionMatches.length,
    class_definition_matches: definitionMatches.slice(0, 25),
    source_matches_scanned: sourceMatches.length,
    scanned_text_files: textPaths.length,
  },
  interpretation_boundary:
    'No upstream definition for the class codes was found in the scanned repository text. Treat lipi.class as an unverified source code, not an independent semantic label. Counts use the local filtered layer, not the raw claim-bearing CSV.',
  artifact_files: [
    'data/open_prototype/reports/lipi_class_field_counts.csv',
    'data/open_prototype/reports/lipi_class_field_by_type.csv',
    'data/open_prototype/reports/lipi_class_field_by_site.csv',
    'data/open_prototype/reports/lipi_class_field_by_length.csv',
    'data/open_prototype/reports/lipi_class_field_examples.csv',
    'data/open_prototype/reports/lipi_class_field_audit_summary.json',
  ],
};

fs.writeFileSync(outClassCounts, toCsv(classCountRows), 'utf8');
fs.writeFileSync(outByType, toCsv(nestedRows(typeByClass, 'class', 'type')), 'utf8');
fs.writeFileSync(outBySite, toCsv(nestedRows(siteByClass, 'class', 'site')), 'utf8');
fs.writeFileSync(outByLength, toCsv(nestedRows(lengthByClass, 'class', 'text_length')), 'utf8');
fs.writeFileSync(outExamples, toCsv(exampleRows), 'utf8');
fs.writeFileSync(outJson, `${JSON.stringify(sourceAudit, null, 2)}\n`, 'utf8');

console.log(
  JSON.stringify(
    {
      repo,
      branch_head_sha: branchInfo.commit.sha,
      local_filtered_rows: filteredRows.length,
      remote_raw_nonempty_line_rows: rawNonemptyLineRows,
      remote_raw_parser_rows: rawRows.length,
      local_numeric_clean_rows: numericCleanRows.length,
      class_values_all_rows: allClassCounts.size,
      class_values_numeric_clean: numericClassCounts.size,
      source_context: sourceAudit.source_context,
      top_classes: classCountRows.slice(1, 11),
      wrote: sourceAudit.artifact_files,
    },
    null,
    2,
  ),
);
