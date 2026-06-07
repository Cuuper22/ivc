import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const sourcePath = path.join(base, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const artifactRowsPath = path.join(reportsDir, 'lipi_short_mark_dimension_artifact_rows.csv');
const tokenTestsPath = path.join(reportsDir, 'lipi_short_mark_dimension_token_tests.csv');
const summaryJsonPath = path.join(reportsDir, 'lipi_short_mark_dimension_stress_summary.json');
const ablationTokenTestsPath = path.join(reportsDir, 'lipi_short_mark_dimension_no_h_series_token_tests.csv');
const ablationSummaryJsonPath = path.join(reportsDir, 'lipi_short_mark_dimension_no_h_series_summary.json');

const iterations = Number(process.env.IVC_SHORT_MARK_DIMENSION_ITERATIONS ?? 5000);
const minPresent = Number(process.env.IVC_SHORT_MARK_DIMENSION_MIN_PRESENT ?? 10);
const minAbsent = Number(process.env.IVC_SHORT_MARK_DIMENSION_MIN_ABSENT ?? 10);
const seedBase = 20260525;

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
  return String(value ?? '').trim();
}

function valueOrNull(value) {
  const text = norm(value);
  if (!text || text === '-' || text === 'None' || text === '??' || text === '?') return null;
  return text;
}

function valueOrDash(value) {
  return valueOrNull(value) ?? '-';
}

function parseInteger(value) {
  const num = Number.parseInt(norm(value), 10);
  return Number.isFinite(num) ? num : null;
}

function parseLeadingInteger(value) {
  const match = norm(value).match(/^(\d+)/);
  return match ? Number.parseInt(match[1], 10) : null;
}

function parsePositiveNumber(value) {
  const text = norm(value);
  if (!/^(?:\d+(?:\.\d+)?|\.\d+)$/.test(text)) return null;
  const num = Number(text);
  return Number.isFinite(num) && num > 0 ? num : null;
}

function parseSideIndex(id) {
  const match = norm(id).match(/\.(\d+)$/);
  return match ? Number.parseInt(match[1], 10) : null;
}

function cleanDirection(value) {
  const text = norm(value).replace(/\s+/g, '').toUpperCase();
  if (text === 'R/L' || text === 'L/R' || text === 'T/B') return text;
  return text || '-';
}

function parseTokens(text) {
  const raw = norm(text);
  const tokens = raw.match(/\d{3}/g) ?? [];
  return {
    raw,
    tokens,
    tokenCount: tokens.length,
    hasUnknownZero: tokens.includes('000'),
    hasQuestion: raw.includes('?'),
    hasBracket: raw.includes('[') || raw.includes(']') || raw.includes('(') || raw.includes(')'),
    hasSlash: raw.includes('/'),
    hasText: raw !== '' && raw !== '-',
  };
}

function rowStatus(record) {
  const directional = record.direction === 'R/L' || record.direction === 'L/R' || record.direction === 'T/B';
  const lengthMatches =
    record.length_numeric !== null && record.parsed.tokenCount > 0 && record.length_numeric === record.parsed.tokenCount;
  const clean =
    record.parsed.hasText &&
    record.parsed.tokenCount > 0 &&
    record.complete === 'Y' &&
    directional &&
    lengthMatches &&
    !record.parsed.hasUnknownZero &&
    !record.parsed.hasQuestion &&
    !record.parsed.hasBracket &&
    !record.parsed.hasSlash;
  if (clean) return 'clean_side_row';
  if (record.parsed.tokenCount > 0 && !record.parsed.hasQuestion && !record.parsed.hasBracket && !record.parsed.hasSlash) {
    return 'usable_uncertain_side_row';
  }
  return 'audit_only_side_row';
}

function mean(values) {
  return values.length ? values.reduce((sum, value) => sum + value, 0) / values.length : null;
}

function formatNumber(value, digits = 6) {
  return value === null || value === undefined || Number.isNaN(value) ? null : Number(value.toFixed(digits));
}

function bump(map, key, by = 1) {
  map.set(key, (map.get(key) ?? 0) + by);
}

function joinSorted(values) {
  return [...values].sort((a, b) => a.localeCompare(b)).join(';');
}

function mulberry32(seed) {
  return function random() {
    let t = (seed += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffle(array, rng) {
  const out = array.slice();
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function blockKey(row) {
  return [row.type, row.site, row.shape, row.material, row.sides].map((value) => value || '-').join('|');
}

function meanDifference(rows, token, dimension) {
  const present = rows.filter((row) => row.short_tokens.has(token) && row[dimension] !== null).map((row) => row[dimension]);
  const absent = rows.filter((row) => !row.short_tokens.has(token) && row[dimension] !== null).map((row) => row[dimension]);
  return {
    present,
    absent,
    mean_present: mean(present),
    mean_absent: mean(absent),
    signed_diff: present.length && absent.length ? mean(present) - mean(absent) : null,
    abs_diff: present.length && absent.length ? Math.abs(mean(present) - mean(absent)) : null,
  };
}

function permutationP(rows, token, dimension, observedAbsDiff, rng) {
  const byBlock = new Map();
  for (const row of rows.filter((candidate) => candidate[dimension] !== null)) {
    const key = row.block_key;
    if (!byBlock.has(key)) byBlock.set(key, []);
    byBlock.get(key).push(row);
  }
  const values = rows
    .filter((row) => row[dimension] !== null)
    .map((row) => ({
      id: row.cisi,
      value: row[dimension],
      block_key: row.block_key,
      present: row.short_tokens.has(token),
    }));
  let ge = 0;
  for (let iter = 0; iter < iterations; iter++) {
    const permutedPresence = new Map();
    for (const [key, blockRows] of byBlock.entries()) {
      const flags = shuffle(
        blockRows.map((row) => row.short_tokens.has(token)),
        rng,
      );
      blockRows.forEach((row, index) => permutedPresence.set(`${key}\t${row.cisi}`, flags[index]));
    }
    const present = [];
    const absent = [];
    for (const row of values) {
      if (permutedPresence.get(`${row.block_key}\t${row.id}`)) present.push(row.value);
      else absent.push(row.value);
    }
    const diff = present.length && absent.length ? Math.abs(mean(present) - mean(absent)) : 0;
    if (diff >= observedAbsDiff - 1e-12) ge++;
  }
  return (ge + 1) / (iterations + 1);
}

function addBenjaminiHochberg(rows) {
  const sorted = rows
    .filter((row) => row.permutation_p_ge_abs_diff !== null)
    .slice()
    .sort((a, b) => a.permutation_p_ge_abs_diff - b.permutation_p_ge_abs_diff);
  let minQ = 1;
  for (let i = sorted.length - 1; i >= 0; i--) {
    const rank = i + 1;
    const q = Math.min(minQ, (sorted[i].permutation_p_ge_abs_diff * sorted.length) / rank);
    sorted[i].bh_q = q;
    minQ = q;
  }
  return rows.map((row) => ({
    ...row,
    bh_q: row.bh_q === undefined ? null : formatNumber(row.bh_q),
    survives_bh_05: row.bh_q !== undefined && row.bh_q <= 0.05,
  }));
}

function testTokenDimensions(rowsForScope) {
  const counts = new Map();
  for (const row of rowsForScope) {
    for (const token of row.short_tokens) bump(counts, token);
  }
  const tokens = [...counts.entries()]
    .filter(([, count]) => count >= minPresent && rowsForScope.length - count >= minAbsent)
    .map(([token]) => token)
    .sort((a, b) => a.localeCompare(b));
  const dimensions = ['horizontal', 'vertical', 'area', 'aspect', 'thickness'];
  const out = [];
  for (const token of tokens) {
    for (const dimension of dimensions) {
      const dimensionRows = rowsForScope.filter((row) => row[dimension] !== null);
      const stats = meanDifference(dimensionRows, token, dimension);
      if (stats.present.length < minPresent || stats.absent.length < minAbsent || stats.abs_diff === null) continue;
      const rng = mulberry32(seedBase + Number(token) * 101 + dimension.length * 1009 + rowsForScope.length);
      const p = permutationP(dimensionRows, token, dimension, stats.abs_diff, rng);
      out.push({
        token,
        dimension,
        artifacts_with_dimension: dimensionRows.length,
        present_artifacts: stats.present.length,
        absent_artifacts: stats.absent.length,
        mean_present: formatNumber(stats.mean_present),
        mean_absent: formatNumber(stats.mean_absent),
        signed_diff: formatNumber(stats.signed_diff),
        abs_diff: formatNumber(stats.abs_diff),
        permutation_p_ge_abs_diff: formatNumber(p),
        iterations,
      });
    }
  }
  return { targetTokens: tokens, tests: addBenjaminiHochberg(out) };
}

function summarizeTests(rows, scopeRows, scopeName, targetTokens) {
  const correctedFlags = rows.filter((row) => row.survives_bh_05);
  const lowP = rows
    .slice()
    .sort(
      (a, b) =>
        Number(a.permutation_p_ge_abs_diff) - Number(b.permutation_p_ge_abs_diff) ||
        a.token.localeCompare(b.token) ||
        a.dimension.localeCompare(b.dimension),
    )
    .slice(0, 12);
  return {
    generated_at_local: new Date().toISOString(),
    experiment: 'Lipi short-mark dimension stress audit',
    scope: scopeName,
    source: 'data/open_prototype/lipi/metadata_filtered.csv',
    source_status: 'T3 filtered lipi planning layer; claim columns removed; image/plate validation pending',
    artifact_level_design: 'one row per CISI artifact with at least one clean multi-side short-mark row',
    artifact_rows: scopeRows.length,
    artifacts_with_horizontal: scopeRows.filter((row) => row.horizontal !== null).length,
    artifacts_with_vertical: scopeRows.filter((row) => row.vertical !== null).length,
    artifacts_with_thickness: scopeRows.filter((row) => row.thickness !== null).length,
    target_tokens: targetTokens,
    token_tests: rows.length,
    permutation_iterations_per_test: iterations,
    permutation_block: 'type|site|shape|material|sides',
    corrected_flags_bh_05: correctedFlags.map((row) => ({
      token: row.token,
      dimension: row.dimension,
      permutation_p_ge_abs_diff: row.permutation_p_ge_abs_diff,
      bh_q: row.bh_q,
      present_artifacts: row.present_artifacts,
      absent_artifacts: row.absent_artifacts,
      mean_present: row.mean_present,
      mean_absent: row.mean_absent,
    })),
    lowest_p_tests: lowP.map((row) => ({
      token: row.token,
      dimension: row.dimension,
      permutation_p_ge_abs_diff: row.permutation_p_ge_abs_diff,
      bh_q: row.bh_q,
      present_artifacts: row.present_artifacts,
      absent_artifacts: row.absent_artifacts,
      mean_present: row.mean_present,
      mean_absent: row.mean_absent,
    })),
    interpretation_boundary:
      'Artifact-level measurement stress audit only. Any surviving association is a source-validation target, not a numerical value, metrological reading, semantic reading, phonetic value, language identity, or translation.',
  };
}

const rows = parseCsv(fs.readFileSync(sourcePath, 'utf8'));
const header = rows[0];
const column = Object.fromEntries(header.map((name, index) => [name, index]));

const records = rows.slice(1).map((row) => {
  const parsed = parseTokens(row[column.text]);
  const horizontal = parsePositiveNumber(row[column['horizontal(mm)']]);
  const vertical = parsePositiveNumber(row[column['vertical(mm)']]);
  const thickness = parsePositiveNumber(row[column['thickness(mm)']]);
  const record = {
    id: valueOrDash(row[column.id]),
    cisi: valueOrNull(row[column.cisi]),
    site: valueOrNull(row[column.site]),
    type: valueOrNull(row[column.type]),
    material: valueOrNull(row[column.material]),
    shape: valueOrNull(row[column.shape]),
    complete: valueOrDash(row[column.complete]),
    direction: cleanDirection(row[column['dir.']]),
    sides: parseInteger(row[column.sides]),
    side_index: parseSideIndex(row[column.id]),
    length_numeric: parseLeadingInteger(row[column['text length']]),
    horizontal,
    vertical,
    thickness,
    area: horizontal !== null && vertical !== null ? horizontal * vertical : null,
    aspect: horizontal !== null && vertical !== null ? horizontal / vertical : null,
    parsed,
    text: valueOrDash(row[column.text]),
  };
  record.status = rowStatus(record);
  record.short_mark_candidate =
    record.status === 'clean_side_row' &&
    record.sides !== null &&
    record.sides >= 2 &&
    record.parsed.tokenCount > 0 &&
    record.parsed.tokenCount <= 2;
  return record;
});

const byCisi = new Map();
for (const record of records.filter((record) => record.cisi)) {
  if (!byCisi.has(record.cisi)) byCisi.set(record.cisi, []);
  byCisi.get(record.cisi).push(record);
}

const artifactRows = [];
for (const [cisi, group] of byCisi.entries()) {
  const shortRows = group.filter((record) => record.short_mark_candidate);
  if (!shortRows.length) continue;
  const dimensionSource = group.find((record) => record.horizontal !== null || record.vertical !== null || record.thickness !== null) ?? group[0];
  const row = {
    cisi,
    site: valueOrDash(dimensionSource.site),
    type: valueOrDash(dimensionSource.type),
    material: valueOrDash(dimensionSource.material),
    shape: valueOrDash(dimensionSource.shape),
    sides: dimensionSource.sides ?? '',
    horizontal: dimensionSource.horizontal,
    vertical: dimensionSource.vertical,
    thickness: dimensionSource.thickness,
    area: dimensionSource.area,
    aspect: dimensionSource.aspect,
    short_texts: shortRows.map((record) => `${record.side_index ?? '?'}:${record.text}`),
    short_tokens: new Set(shortRows.flatMap((record) => record.parsed.tokens)),
  };
  row.block_key = blockKey(row);
  artifactRows.push(row);
}

const fullRun = testTokenDimensions(artifactRows);
const targetTokens = fullRun.targetTokens;
const correctedTests = fullRun.tests;
const hSeries = new Set(Array.from({ length: 22 }, (_, index) => `H-${2218 + index}`));
const noHSeriesRows = artifactRows.filter((row) => !hSeries.has(row.cisi));
const ablationRun = testTokenDimensions(noHSeriesRows);

fs.writeFileSync(
  artifactRowsPath,
  toCsv([
    [
      'cisi',
      'site',
      'type',
      'material',
      'shape',
      'sides',
      'horizontal_mm',
      'vertical_mm',
      'thickness_mm',
      'area',
      'aspect',
      'block_key',
      'short_tokens',
      'short_texts',
    ],
    ...artifactRows.map((row) => [
      row.cisi,
      row.site,
      row.type,
      row.material,
      row.shape,
      row.sides,
      row.horizontal ?? '',
      row.vertical ?? '',
      row.thickness ?? '',
      row.area ?? '',
      row.aspect ?? '',
      row.block_key,
      joinSorted(row.short_tokens),
      row.short_texts.join('|'),
    ]),
  ]),
  'utf8',
);

fs.writeFileSync(
  tokenTestsPath,
  toCsv([
    [
      'token',
      'dimension',
      'artifacts_with_dimension',
      'present_artifacts',
      'absent_artifacts',
      'mean_present',
      'mean_absent',
      'signed_diff',
      'abs_diff',
      'permutation_p_ge_abs_diff',
      'bh_q',
      'survives_bh_05',
      'iterations',
    ],
    ...correctedTests.map((row) => [
      row.token,
      row.dimension,
      row.artifacts_with_dimension,
      row.present_artifacts,
      row.absent_artifacts,
      row.mean_present,
      row.mean_absent,
      row.signed_diff,
      row.abs_diff,
      row.permutation_p_ge_abs_diff,
      row.bh_q,
      row.survives_bh_05,
      row.iterations,
    ]),
  ]),
  'utf8',
);

fs.writeFileSync(
  ablationTokenTestsPath,
  toCsv([
    [
      'token',
      'dimension',
      'artifacts_with_dimension',
      'present_artifacts',
      'absent_artifacts',
      'mean_present',
      'mean_absent',
      'signed_diff',
      'abs_diff',
      'permutation_p_ge_abs_diff',
      'bh_q',
      'survives_bh_05',
      'iterations',
    ],
    ...ablationRun.tests.map((row) => [
      row.token,
      row.dimension,
      row.artifacts_with_dimension,
      row.present_artifacts,
      row.absent_artifacts,
      row.mean_present,
      row.mean_absent,
      row.signed_diff,
      row.abs_diff,
      row.permutation_p_ge_abs_diff,
      row.bh_q,
      row.survives_bh_05,
      row.iterations,
    ]),
  ]),
  'utf8',
);

const summary = {
  ...summarizeTests(correctedTests, artifactRows, 'all_short_mark_artifacts', targetTokens),
  outputs: [
    'data/open_prototype/reports/lipi_short_mark_dimension_artifact_rows.csv',
    'data/open_prototype/reports/lipi_short_mark_dimension_token_tests.csv',
    'data/open_prototype/reports/lipi_short_mark_dimension_stress_summary.json',
    'data/open_prototype/reports/lipi_short_mark_dimension_no_h_series_token_tests.csv',
    'data/open_prototype/reports/lipi_short_mark_dimension_no_h_series_summary.json',
  ],
};
const ablationSummary = {
  ...summarizeTests(
    ablationRun.tests,
    noHSeriesRows,
    'excluding_h2218_h2239',
    ablationRun.targetTokens,
  ),
  removed_h_series_artifacts: artifactRows.length - noHSeriesRows.length,
};

fs.writeFileSync(summaryJsonPath, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
fs.writeFileSync(ablationSummaryJsonPath, `${JSON.stringify(ablationSummary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
console.log(JSON.stringify(ablationSummary, null, 2));
