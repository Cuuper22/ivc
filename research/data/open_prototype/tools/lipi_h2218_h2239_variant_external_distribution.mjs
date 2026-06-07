import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const inputPath = path.join(base, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const rowsOut = path.join(reportsDir, 'lipi_h2218_h2239_variant_external_distribution_rows.csv');
const contextsOut = path.join(
  reportsDir,
  'lipi_h2218_h2239_variant_external_distribution_contexts.csv',
);
const pairsOut = path.join(reportsDir, 'lipi_h2218_h2239_variant_external_distribution_pairs.csv');
const summaryOut = path.join(
  reportsDir,
  'lipi_h2218_h2239_variant_external_distribution_summary.json',
);

const targetSigns = new Set(['033', '034', '154', '156']);
const targetPatterns = new Set([
  '700_033',
  '700_034',
  '033_700',
  '034_700',
  '154_003',
  '156_003',
  '003_154',
  '003_156',
]);
const exactTargetTexts = [
  '+700-033+',
  '+700-034+',
  '+033-700+',
  '+034-700+',
  '+154-003+',
  '+156-003+',
  '+003-154+',
  '+003-156+',
];

function parseCsv(text) {
  const rows = [];
  let row = [];
  let value = '';
  let inQuotes = false;

  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (inQuotes) {
      if (ch === '"' && next === '"') {
        value += '"';
        i += 1;
      } else if (ch === '"') {
        inQuotes = false;
      } else {
        value += ch;
      }
    } else if (ch === '"') {
      inQuotes = true;
    } else if (ch === ',') {
      row.push(value);
      value = '';
    } else if (ch === '\n') {
      row.push(value);
      if (row.length > 1 || row[0] !== '') rows.push(row);
      row = [];
      value = '';
    } else if (ch !== '\r') {
      value += ch;
    }
  }
  if (value.length > 0 || row.length > 0) {
    row.push(value);
    rows.push(row);
  }
  return rows;
}

function csvObjects(text) {
  const [header, ...body] = parseCsv(text);
  return body.map((row) =>
    Object.fromEntries(header.map((key, index) => [key, row[index] ?? ''])),
  );
}

function toCsv(rows) {
  if (rows.length === 0) return '';
  const header = Object.keys(rows[0]);
  const body = rows.map((row) =>
    header
      .map((key) => `"${String(row[key] ?? '').replaceAll('"', '""')}"`)
      .join(','),
  );
  return `${[header.map((key) => `"${key}"`).join(','), ...body].join('\n')}\n`;
}

function tokens(text) {
  return text.match(/\d+/gu) ?? [];
}

function adjacentPatterns(signs) {
  const patterns = [];
  for (let i = 0; i < signs.length - 1; i += 1) {
    const pattern = `${signs[i]}_${signs[i + 1]}`;
    if (targetPatterns.has(pattern)) patterns.push(pattern);
  }
  return patterns;
}

function cisiNumber(cisi) {
  const match = /^H-(\d+)$/u.exec(cisi);
  return match ? Number(match[1]) : null;
}

function isH2218To2239(row) {
  const number = cisiNumber(row.cisi);
  return number !== null && number >= 2218 && number <= 2239;
}

function cisiPrefix(cisi) {
  const match = /^([A-Z]+)-/u.exec(cisi);
  return match ? match[1] : cisi === '-' ? '-' : 'other';
}

function objectGroupKey(row) {
  return row.cisi && row.cisi !== '-' ? `cisi:${row.cisi}` : `row:${row.id}`;
}

function familyFor(patternOrSign) {
  if (/(^|_)0?33($|_)|(^|_)0?34($|_)/u.test(patternOrSign)) return '033_vs_034';
  if (/(^|_)154($|_)|(^|_)156($|_)/u.test(patternOrSign)) return '154_vs_156';
  return 'other_target_sign';
}

function exactTextClass(text) {
  return exactTargetTexts.includes(text) ? text : 'non_exact_or_longer';
}

function addCount(map, keys, n = 1) {
  const key = JSON.stringify(keys);
  map.set(key, (map.get(key) ?? 0) + n);
}

function countsObject(rows, keyFn) {
  const counts = {};
  for (const row of rows) {
    const key = keyFn(row);
    counts[key] = (counts[key] ?? 0) + 1;
  }
  return Object.fromEntries(
    Object.entries(counts).sort((a, b) => a[0].localeCompare(b[0], undefined, { numeric: true })),
  );
}

function countRows(rows, predicate) {
  return rows.filter(predicate).length;
}

function sameCisiTexts(groupRows) {
  return [...new Set(groupRows.map((row) => row.text).filter(Boolean))].sort().join(';');
}

function companionFlag(groupRows, exactText) {
  return groupRows.some((row) => row.text === exactText) ? '1' : '0';
}

const rows = csvObjects(fs.readFileSync(inputPath, 'utf8'));
const byCisi = new Map();
for (const row of rows) {
  const key = objectGroupKey(row);
  if (!byCisi.has(key)) byCisi.set(key, []);
  byCisi.get(key).push(row);
}

const analyzedRows = rows.map((row) => {
  const rowTokens = tokens(row.text);
  const presentTargets = [...new Set(rowTokens.filter((sign) => targetSigns.has(sign)))].sort();
  const patterns = adjacentPatterns(rowTokens);
  const groupRows = byCisi.get(objectGroupKey(row)) ?? [row];
  return {
    source_row_id: row.id,
    cisi: row.cisi,
    cisi_prefix: cisiPrefix(row.cisi),
    is_h2218_h2239: isH2218To2239(row) ? '1' : '0',
    region: row.region,
    site: row.site,
    period: row.period,
    phase: row.phase,
    material: row.material,
    shape: row.shape,
    preservation: row.preservation,
    type: row.type,
    sides: row.sides,
    direction: row['dir.'],
    class: row.class,
    sign_count: row.signs,
    horizontal_mm: row['horizontal(mm)'],
    vertical_mm: row['vertical(mm)'],
    thickness_mm: row['thickness(mm)'],
    text: row.text,
    tokens: rowTokens.join(' '),
    target_signs_present: presentTargets.join(';'),
    adjacent_target_patterns: patterns.join(';'),
    exact_text_class: exactTextClass(row.text),
    same_cisi_texts: sameCisiTexts(groupRows),
    has_companion_861_003: companionFlag(groupRows, '+861-003+'),
    has_companion_156_003: companionFlag(groupRows, '+156-003+'),
    has_companion_154_003: companionFlag(groupRows, '+154-003+'),
    has_companion_400_740_176: companionFlag(groupRows, '+400-740-176+'),
    accepted_decipherment_claim: '0',
  };
});

const targetRows = analyzedRows.filter(
  (row) => row.target_signs_present !== '' || row.adjacent_target_patterns !== '',
);

const contextCounts = new Map();
for (const row of targetRows) {
  const patternKeys =
    row.adjacent_target_patterns === '' ? ['target_sign_without_target_pair'] : row.adjacent_target_patterns.split(';');
  for (const pattern of patternKeys) {
    addCount(contextCounts, [
      familyFor(pattern === 'target_sign_without_target_pair' ? row.target_signs_present : pattern),
      pattern,
      row.exact_text_class,
      row.cisi_prefix,
      row.is_h2218_h2239,
      row.site,
      row.type,
      row.shape,
      row.material,
      row.has_companion_861_003,
      row.has_companion_156_003,
      row.has_companion_154_003,
      row.has_companion_400_740_176,
    ]);
  }
}

const contextRows = [...contextCounts.entries()]
  .map(([key, count]) => {
    const [
      variant_family,
      adjacent_pattern,
      exact_text_class_value,
      cisi_prefix_value,
      is_h2218_h2239_value,
      site,
      type,
      shape,
      material,
      has_companion_861_003,
      has_companion_156_003,
      has_companion_154_003,
      has_companion_400_740_176,
    ] = JSON.parse(key);
    return {
      checked_date: '2026-05-25',
      variant_family,
      adjacent_pattern,
      exact_text_class: exact_text_class_value,
      cisi_prefix: cisi_prefix_value,
      is_h2218_h2239: is_h2218_h2239_value,
      site,
      type,
      shape,
      material,
      has_companion_861_003,
      has_companion_156_003,
      has_companion_154_003,
      has_companion_400_740_176,
      row_count: String(count),
      accepted_decipherment_claim: '0',
    };
  })
  .sort(
    (a, b) =>
      a.variant_family.localeCompare(b.variant_family) ||
      a.adjacent_pattern.localeCompare(b.adjacent_pattern) ||
      a.exact_text_class.localeCompare(b.exact_text_class) ||
      a.site.localeCompare(b.site) ||
      a.type.localeCompare(b.type) ||
      a.shape.localeCompare(b.shape) ||
      a.material.localeCompare(b.material),
  );

function pairRow(pattern, label) {
  const family = familyFor(pattern);
  const exactText = `+${pattern.replace('_', '-')}+`;
  const adjacentRows = targetRows.filter((row) => row.adjacent_target_patterns.split(';').includes(pattern));
  const exactRows = targetRows.filter((row) => row.text === exactText);
  const nonHAdjacentRows = adjacentRows.filter((row) => row.is_h2218_h2239 === '0');
  const nonHExactRows = exactRows.filter((row) => row.is_h2218_h2239 === '0');
  return {
    checked_date: '2026-05-25',
    label,
    variant_family: family,
    adjacent_pattern: pattern,
    strict_exact_text: exactText,
    adjacent_row_count: String(adjacentRows.length),
    strict_exact_text_row_count: String(exactRows.length),
    non_h2218_h2239_adjacent_row_count: String(nonHAdjacentRows.length),
    non_h2218_h2239_strict_exact_text_row_count: String(nonHExactRows.length),
    h2218_h2239_adjacent_cisi: [...new Set(adjacentRows.filter((row) => row.is_h2218_h2239 === '1').map((row) => row.cisi))]
      .sort()
      .join(';'),
    non_h2218_h2239_sample_cisi: [...new Set(nonHAdjacentRows.map((row) => row.cisi))]
      .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }))
      .slice(0, 40)
      .join(';'),
    type_counts: JSON.stringify(countsObject(adjacentRows, (row) => row.type)),
    site_counts: JSON.stringify(countsObject(adjacentRows, (row) => row.site)),
    interpretation_boundary:
      'External distribution can support sign-pair reality or raise copy/catalog confounds; it does not assign sign value, language, function, or translation.',
    accepted_decipherment_claim: '0',
  };
}

const pairRows = [
  pairRow('700_033', 'H-2238 singleton-side candidate comparator'),
  pairRow('700_034', 'H-2238 local-majority comparator'),
  pairRow('033_700', 'reversed 033/034 family comparator'),
  pairRow('034_700', 'reversed 033/034 family comparator'),
  pairRow('154_003', 'H-2237 singleton-side candidate comparator'),
  pairRow('156_003', 'H-2237 local-majority comparator'),
  pairRow('003_154', 'reversed 154/156 family comparator'),
  pairRow('003_156', 'reversed 154/156 family comparator'),
];

const exactTextCounts = Object.fromEntries(
  exactTargetTexts.map((text) => [text, countRows(targetRows, (row) => row.text === text)]),
);
const adjacentPatternCounts = Object.fromEntries(
  [...targetPatterns].map((pattern) => [
    pattern,
    countRows(targetRows, (row) => row.adjacent_target_patterns.split(';').includes(pattern)),
  ]),
);
const nonHAdjacentPatternCounts = Object.fromEntries(
  [...targetPatterns].map((pattern) => [
    pattern,
    countRows(
      targetRows,
      (row) => row.is_h2218_h2239 === '0' && row.adjacent_target_patterns.split(';').includes(pattern),
    ),
  ]),
);
const hSeriesVariantRows = targetRows.filter(
  (row) => row.cisi === 'H-2237' || row.cisi === 'H-2238',
);

const summary = {
  checked_date: '2026-05-25',
  artifact: 'lipi_h2218_h2239_variant_external_distribution',
  input: path.relative(base, inputPath).replaceAll('\\', '/'),
  total_metadata_rows: rows.length,
  rows_with_any_target_sign: targetRows.length,
  exact_text_counts: exactTextCounts,
  adjacent_pattern_counts: adjacentPatternCounts,
  non_h2218_h2239_adjacent_pattern_counts: nonHAdjacentPatternCounts,
  h2238_700_033_external_support: nonHAdjacentPatternCounts['700_033'] > 0,
  h2238_700_033_strict_exact_external_support:
    countRows(targetRows, (row) => row.is_h2218_h2239 === '0' && row.text === '+700-033+') > 0,
  h2237_154_003_external_support: nonHAdjacentPatternCounts['154_003'] > 0,
  h2237_154_003_strict_exact_external_support:
    countRows(targetRows, (row) => row.is_h2218_h2239 === '0' && row.text === '+154-003+') > 0,
  h_series_variant_rows: hSeriesVariantRows.map((row) => ({
    cisi: row.cisi,
    source_row_id: row.source_row_id,
    text: row.text,
    adjacent_target_patterns: row.adjacent_target_patterns,
    same_cisi_texts: row.same_cisi_texts,
  })),
  outputs: [
    path.relative(base, rowsOut).replaceAll('\\', '/'),
    path.relative(base, contextsOut).replaceAll('\\', '/'),
    path.relative(base, pairsOut).replaceAll('\\', '/'),
    path.relative(base, summaryOut).replaceAll('\\', '/'),
  ],
  interpretation_boundary:
    'This is external distribution evidence for variant reality and source-priority ranking. It accepts no sign reading, function, language, or translation.',
  accepted_decipherment_claims: 0,
};

fs.mkdirSync(reportsDir, { recursive: true });
fs.writeFileSync(rowsOut, toCsv(targetRows), 'utf8');
fs.writeFileSync(contextsOut, toCsv(contextRows), 'utf8');
fs.writeFileSync(pairsOut, toCsv(pairRows), 'utf8');
fs.writeFileSync(summaryOut, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
