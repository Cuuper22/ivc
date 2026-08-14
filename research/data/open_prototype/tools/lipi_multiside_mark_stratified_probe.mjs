// Follow-up to lipi_multiside_mark_scope_probe.mjs. The corpus-wide short-mark
// enrichment numbers could be driven by a few dominant site/type combinations,
// so this probe reruns the same analysis inside two homogeneous strata:
// Harappa TAB:B tablets and Harappa TAB:I tablets. If a sign is genuinely a
// short-mark sign, its enrichment should survive within a single stratum.
//
// The script reads lipi_multiside_mark_rows.csv (the per-side detail written
// by the scope probe), filters to each stratum, and recomputes per-sign
// short-mark vs. long-text counts, smoothed enrichment ratios (signs need at
// least 5 short-mark occurrences), side-index placement, binned dimensions,
// and same-object short/long sign pairs (pairs kept at 3+ objects).
//
// Outputs: lipi_multiside_mark_stratified_token_counts.csv, _pair_counts.csv,
// _side_index.csv, and _summary.json. Descriptive stratified counts only —
// no sign values or readings are proposed.

import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const sourcePath = path.join(reportsDir, 'lipi_multiside_mark_rows.csv');

const outTokenCounts = path.join(reportsDir, 'lipi_multiside_mark_stratified_token_counts.csv');
const outPairCounts = path.join(reportsDir, 'lipi_multiside_mark_stratified_pair_counts.csv');
const outSideIndex = path.join(reportsDir, 'lipi_multiside_mark_stratified_side_index.csv');
const outJson = path.join(reportsDir, 'lipi_multiside_mark_stratified_summary.json');

const strata = [
  { name: 'harappa_tab_b', site: 'Harappa', type: 'TAB:B' },
  { name: 'harappa_tab_i', site: 'Harappa', type: 'TAB:I' },
];
const minShortTokenCount = 5;

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

function csvObjects(text) {
  const rows = parseCsv(text);
  const header = rows.shift() ?? [];
  return rows.map((row) => Object.fromEntries(header.map((name, index) => [name, row[index] ?? ''])));
}

function parseTokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function parseBool(value) {
  return String(value).toLowerCase() === 'true';
}

function bump(map, key, by = 1) {
  map.set(key, (map.get(key) ?? 0) + by);
}

function addNested(map, keyA, keyB, by = 1) {
  if (!map.has(keyA)) map.set(keyA, new Map());
  bump(map.get(keyA), keyB, by);
}

function formatNumber(value) {
  return value === null || value === undefined || Number.isNaN(value) ? null : Number(value.toFixed(6));
}

function joinTop(counts, limit = 5) {
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, limit)
    .map(([key, count]) => `${key}:${count}`)
    .join(';');
}

function stratumRows(rows, stratum) {
  return rows.filter((row) => row.site === stratum.site && row.type === stratum.type);
}

const rows = csvObjects(fs.readFileSync(sourcePath, 'utf8')).map((row) => ({
  ...row,
  tokens: parseTokens(row.text),
  short_mark_candidate: parseBool(row.short_mark_candidate),
  long_text_candidate: parseBool(row.long_text_candidate),
}));

const tokenRows = [
  [
    'stratum',
    'token',
    'short_mark_token_count',
    'long_text_token_count',
    'short_mark_share',
    'long_text_share',
    'enrichment_ratio_smoothed',
    'top_side_indexes',
    'top_horizontal_bins',
    'top_vertical_bins',
    'top_thickness_bins',
  ],
];
const pairRows = [['stratum', 'short_mark_token', 'long_text_token', 'artifact_group_count']];
const sideRows = [['stratum', 'side_index', 'short_mark_rows', 'top_tokens']];
const summary = [];

for (const stratum of strata) {
  const scoped = stratumRows(rows, stratum);
  const shortRows = scoped.filter((row) => row.short_mark_candidate);
  const longRows = scoped.filter((row) => row.long_text_candidate);

  const shortTokenCounts = new Map();
  const longTokenCounts = new Map();
  const sideIndexTokenCounts = new Map();
  const tokenSideIndexes = new Map();
  const tokenHorizontalBins = new Map();
  const tokenVerticalBins = new Map();
  const tokenThicknessBins = new Map();

  for (const row of shortRows) {
    for (const token of row.tokens) {
      bump(shortTokenCounts, token);
      addNested(sideIndexTokenCounts, row.side_index || '-', token);
      addNested(tokenSideIndexes, token, row.side_index || '-');
      addNested(tokenHorizontalBins, token, row.horizontal_bin || '-');
      addNested(tokenVerticalBins, token, row.vertical_bin || '-');
      addNested(tokenThicknessBins, token, row.thickness_bin || '-');
    }
  }

  for (const row of longRows) {
    for (const token of row.tokens) bump(longTokenCounts, token);
  }

  const shortTotal = [...shortTokenCounts.values()].reduce((sum, count) => sum + count, 0);
  const longTotal = [...longTokenCounts.values()].reduce((sum, count) => sum + count, 0);
  const vocab = new Set([...shortTokenCounts.keys(), ...longTokenCounts.keys()]);
  const tokenObjects = [];

  for (const token of vocab) {
    const shortCount = shortTokenCounts.get(token) ?? 0;
    const longCount = longTokenCounts.get(token) ?? 0;
    if (shortCount < minShortTokenCount) continue;
    const shortShare = shortCount / Math.max(1, shortTotal);
    const longShare = longCount / Math.max(1, longTotal);
    const enrichment = ((shortCount + 0.5) / (shortTotal + vocab.size * 0.5)) /
      ((longCount + 0.5) / (longTotal + vocab.size * 0.5));
    tokenObjects.push({ token, shortCount, longCount, shortShare, longShare, enrichment });
  }

  for (const tokenObject of tokenObjects.sort((a, b) => b.enrichment - a.enrichment || b.shortCount - a.shortCount || a.token.localeCompare(b.token))) {
    tokenRows.push([
      stratum.name,
      tokenObject.token,
      tokenObject.shortCount,
      tokenObject.longCount,
      formatNumber(tokenObject.shortShare),
      formatNumber(tokenObject.longShare),
      formatNumber(tokenObject.enrichment),
      joinTop(tokenSideIndexes.get(tokenObject.token) ?? new Map()),
      joinTop(tokenHorizontalBins.get(tokenObject.token) ?? new Map()),
      joinTop(tokenVerticalBins.get(tokenObject.token) ?? new Map()),
      joinTop(tokenThicknessBins.get(tokenObject.token) ?? new Map()),
    ]);
  }

  for (const [sideIndex, counts] of [...sideIndexTokenCounts.entries()].sort((a, b) => Number(a[0]) - Number(b[0]) || a[0].localeCompare(b[0]))) {
    const rowCount = shortRows.filter((row) => (row.side_index || '-') === sideIndex).length;
    sideRows.push([stratum.name, sideIndex, rowCount, joinTop(counts, 8)]);
  }

  const groups = new Map();
  for (const row of scoped) {
    if (!groups.has(row.cisi)) groups.set(row.cisi, []);
    groups.get(row.cisi).push(row);
  }

  const pairCounts = new Map();
  for (const groupRows of groups.values()) {
    const shortTokens = new Set(groupRows.filter((row) => row.short_mark_candidate).flatMap((row) => row.tokens));
    const longTokens = new Set(groupRows.filter((row) => row.long_text_candidate).flatMap((row) => row.tokens));
    if (!shortTokens.size || !longTokens.size) continue;
    for (const shortToken of shortTokens) {
      for (const longToken of longTokens) bump(pairCounts, `${shortToken}\t${longToken}`);
    }
  }

  for (const [key, count] of [...pairCounts.entries()]
    .filter(([, count]) => count >= 3)
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))) {
    pairRows.push([stratum.name, ...key.split('\t'), count]);
  }

  summary.push({
    stratum: stratum.name,
    site: stratum.site,
    type: stratum.type,
    rows: scoped.length,
    short_mark_rows: shortRows.length,
    long_text_rows: longRows.length,
    short_mark_token_total: shortTotal,
    long_text_token_total: longTotal,
    candidate_tokens: tokenObjects.length,
    top_by_count: tokenObjects
      .slice()
      .sort((a, b) => b.shortCount - a.shortCount || b.enrichment - a.enrichment || a.token.localeCompare(b.token))
      .slice(0, 8)
      .map((row) => ({
        token: row.token,
        short_mark_token_count: row.shortCount,
        long_text_token_count: row.longCount,
        enrichment_ratio_smoothed: formatNumber(row.enrichment),
      })),
    top_by_enrichment: tokenObjects
      .slice()
      .sort((a, b) => b.enrichment - a.enrichment || b.shortCount - a.shortCount || a.token.localeCompare(b.token))
      .slice(0, 8)
      .map((row) => ({
        token: row.token,
        short_mark_token_count: row.shortCount,
        long_text_token_count: row.longCount,
        enrichment_ratio_smoothed: formatNumber(row.enrichment),
      })),
  });
}

const output = {
  source: 'lipi multi-side mark row report',
  strata,
  min_short_token_count: minShortTokenCount,
  summaries: summary,
  outputs: [
    path.relative(base, outTokenCounts).replaceAll('\\', '/'),
    path.relative(base, outPairCounts).replaceAll('\\', '/'),
    path.relative(base, outSideIndex).replaceAll('\\', '/'),
  ],
  interpretation_boundary:
    'Stratified multi-side mark queue only; recurrent short marks are not numerical values, metrological readings, sign meanings, phonetic values, language identity, or translations.',
};

fs.writeFileSync(outTokenCounts, toCsv(tokenRows));
fs.writeFileSync(outPairCounts, toCsv(pairRows));
fs.writeFileSync(outSideIndex, toCsv(sideRows));
fs.writeFileSync(outJson, `${JSON.stringify(output, null, 2)}\n`);

console.log(JSON.stringify(output, null, 2));
