// Asks whether sign `125` is a portable element of the phrases governed by sign
// `002` — recurring in several different templates, across sites, and not just as
// copies of one text. The script reads metadata_filtered.csv, collapses duplicate
// sign sequences, and for every `002` occurrence records the 4-sign template that
// follows it. Templates are grouped into families; a family counts for the bet only
// if it repeats, spans more than one site, and is not dominated (>50%) by a single
// exact text. Every sign appearing in these template cells is ranked the same way,
// so 125 competes against the whole field and against frequency-comparable signs
// (half to twice its cell count). A 100,000-iteration forger draws random template
// cells (matching 125's cell count) and asks how often chance yields as many
// repeated, cross-site, non-copy families. Writes a bet summary (JSON + CSV) plus
// target-family and per-sign tables to the reports directory.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_125_governed_crosssite_template_forger_20260531';
const RUN_DATE = '2026-05-31';
const ITERATIONS = 100000;
const TARGET = '125';

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
      if (row.some((value) => value.length)) rows.push(row);
      row = [];
      cell = '';
    } else {
      cell += ch;
    }
  }
  if (cell.length || row.length) {
    row.push(cell.replace(/\r$/, ''));
    if (row.some((value) => value.length)) rows.push(row);
  }
  const [header, ...body] = rows;
  return body.map((cols) => Object.fromEntries(header.map((name, idx) => [name, cols[idx] ?? ''])));
}

function writeCsv(file, rows, fields) {
  const esc = (value) => {
    const text = String(value ?? '');
    return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
  };
  const body = rows.map((row) => fields.map((field) => esc(row[field])).join(',')).join('\n');
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`, 'utf8');
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function norm(value, fallback = 'NA') {
  const text = String(value ?? '').trim();
  return text && text !== '-' && text !== 'None' ? text : fallback;
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function countBy(items, fn) {
  const counts = new Map();
  for (const item of items) {
    const key = fn(item);
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }));
}

function topCounts(items, fn, n = 8) {
  return countBy(items, fn).slice(0, n).map(([key, value]) => `${key}:${value}`).join(';');
}

function mulberry32(seed) {
  return function rand() {
    let t = (seed += 0x6D2B79F5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function sampleWithoutReplacement(rand, n, k) {
  const selected = new Set();
  while (selected.size < k) {
    selected.add(Math.floor(rand() * n));
  }
  return selected;
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()];

const governed = [];
let cellIndex = 0;
for (const row of canonicalRows) {
  row.signs.forEach((sign, idx) => {
    if (sign !== '002' || !row.signs[idx + 1]) return;
    const phrase = row.signs.slice(idx + 1);
    const template = [
      row.signs[idx + 1] ?? '<END>',
      row.signs[idx + 2] ?? '<END>',
      row.signs[idx + 3] ?? '<END>',
      row.signs[idx + 4] ?? '<END>',
    ];
    const cells = template.map((value, pos) => ({
      cell_index: cellIndex++,
      pos: pos + 1,
      sign: value,
    }));
    governed.push({
      row_id: row.id,
      object: objectId(row),
      site: norm(row.site),
      type: norm(row.type),
      symbol: norm(row.symbol),
      cult: norm(row.cult),
      material: norm(row.material),
      shape: norm(row.shape),
      prev_before_002: row.signs[idx - 1] ?? '<START>',
      template_4: template.join('-'),
      phrase_after_002: phrase.join('-'),
      exact_sequence: row.signs.join(' '),
      cells,
      text: row.text,
    });
  });
}

const families = countBy(governed, (row) => row.template_4).map(([template, count]) => {
  const members = governed.filter((row) => row.template_4 === template);
  const topExact = countBy(members, (row) => row.exact_sequence)[0]?.[1] ?? 0;
  const distinctSites = new Set(members.map((row) => row.site)).size;
  const distinctTypes = new Set(members.map((row) => row.type)).size;
  const signs = new Set(template.split('-').filter((value) => value !== '<END>'));
  return {
    template_4: template,
    count,
    repeated: count > 1,
    cross_site: distinctSites > 1,
    cross_type: distinctTypes > 1,
    top_exact_share: topExact / count,
    exact_dominated: topExact / count > 0.5,
    contains_target: signs.has(TARGET),
    signs,
    members,
  };
});

function signStats(sign) {
  const cellCount = governed.flatMap((row) => row.cells).filter((cell) => cell.sign === sign).length;
  const containing = families.filter((family) => family.signs.has(sign));
  const repeated = containing.filter((family) => family.repeated);
  const crossSiteRepeated = repeated.filter((family) => family.cross_site);
  const crossSiteNoncopy = crossSiteRepeated.filter((family) => !family.exact_dominated);
  return {
    sign,
    cell_count: cellCount,
    containing_families: containing.length,
    repeated_families: repeated.length,
    cross_site_repeated_families: crossSiteRepeated.length,
    cross_site_noncopy_repeated_families: crossSiteNoncopy.length,
    repeated_templates: repeated.map((family) => `${family.template_4}:${family.count}`).join(';'),
    cross_site_templates: crossSiteRepeated.map((family) => `${family.template_4}:${family.count}`).join(';'),
    cross_site_noncopy_templates: crossSiteNoncopy.map((family) => `${family.template_4}:${family.count}`).join(';'),
  };
}

const allTemplateSigns = [...new Set(governed.flatMap((row) => row.cells.map((cell) => cell.sign)).filter((sign) => sign !== '<END>'))].sort();
const signTable = allTemplateSigns.map(signStats).sort((a, b) =>
  b.cross_site_noncopy_repeated_families - a.cross_site_noncopy_repeated_families ||
  b.cross_site_repeated_families - a.cross_site_repeated_families ||
  b.repeated_families - a.repeated_families ||
  b.cell_count - a.cell_count ||
  a.sign.localeCompare(b.sign, undefined, { numeric: true }),
);

const targetStats = signStats(TARGET);
const comparable = signTable.filter((row) => row.cell_count >= targetStats.cell_count / 2 && row.cell_count <= targetStats.cell_count * 2);
const targetRankAll = signTable.findIndex((row) => row.sign === TARGET) + 1;
const targetRankComparable = comparable.findIndex((row) => row.sign === TARGET) + 1;

const cells = governed.flatMap((row) => row.cells.filter((cell) => cell.sign !== '<END>'));
const targetCellCount = cells.filter((cell) => cell.sign === TARGET).length;
const cellToFamily = new Map();
for (const family of families) {
  for (const member of family.members) {
    for (const cell of member.cells.filter((c) => c.sign !== '<END>')) {
      cellToFamily.set(cell.cell_index, family);
    }
  }
}

function randomCellStats(selectedCells) {
  const containing = new Set();
  for (const cellIdx of selectedCells) {
    const family = cellToFamily.get(cells[cellIdx].cell_index);
    if (family) containing.add(family);
  }
  const containingFamilies = [...containing];
  return {
    repeated: containingFamilies.filter((family) => family.repeated).length,
    cross_site: containingFamilies.filter((family) => family.repeated && family.cross_site).length,
    cross_site_noncopy: containingFamilies.filter((family) => family.repeated && family.cross_site && !family.exact_dominated).length,
  };
}

const rand = mulberry32(0x125390);
let geRepeated = 0;
let geCrossSite = 0;
let geCrossSiteNoncopy = 0;
for (let iter = 0; iter < ITERATIONS; iter += 1) {
  const selected = sampleWithoutReplacement(rand, cells.length, targetCellCount);
  const stats = randomCellStats(selected);
  if (stats.repeated >= targetStats.repeated_families) geRepeated += 1;
  if (stats.cross_site >= targetStats.cross_site_repeated_families) geCrossSite += 1;
  if (stats.cross_site_noncopy >= targetStats.cross_site_noncopy_repeated_families) geCrossSiteNoncopy += 1;
}

const targetFamilies = families
  .filter((family) => family.signs.has(TARGET))
  .sort((a, b) => b.count - a.count || a.template_4.localeCompare(b.template_4, undefined, { numeric: true }))
  .map((family) => ({
    template_4: family.template_4,
    count: family.count,
    repeated: family.repeated,
    cross_site: family.cross_site,
    cross_type: family.cross_type,
    top_exact_share: family.top_exact_share.toFixed(6),
    exact_dominated: family.exact_dominated,
    sites: topCounts(family.members, (row) => row.site),
    types: topCounts(family.members, (row) => row.type),
    prev_before_002: topCounts(family.members, (row) => row.prev_before_002),
    objects: family.members.map((row) => `${row.object}:${row.text}`).join(' | '),
  }));

const tier =
  targetStats.cross_site_noncopy_repeated_families >= 2 && geCrossSiteNoncopy / ITERATIONS <= 0.01
    ? 'candidate'
    : 'wild shot';

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V2_V4_125_PORTABLE_GOVERNED_TEMPLATE_CROSSSITE_20260531',
  vector: 'V2 slot grammar / V4 sign semantics from context',
  confidence_tier: tier,
  risky_bet:
    '`125` is a portable governed suffix/title element inside post-`002` templates, not merely an accidental member of the `002-390` branch table. It should recur in non-copy, cross-site governed templates.',
  observed:
    `Canonical collapse rows=${canonicalRows.length}; governed 002 occurrences=${governed.length}; target template-cell count=${targetStats.cell_count}. ` +
    `Target repeated template families=${targetStats.repeated_families}, cross-site repeated=${targetStats.cross_site_repeated_families}, cross-site non-copy repeated=${targetStats.cross_site_noncopy_repeated_families}. ` +
    `Best cross-site target templates: ${targetStats.cross_site_noncopy_templates || 'none'}.`,
  adversarial_test:
    `Canonical numeric-sequence collapse; template-family exact-sequence domination control; ${ITERATIONS} random-cell forger preserving target template-cell count; frequency-comparable sign ranking.`,
  false_positive_rate: geCrossSiteNoncopy / ITERATIONS,
  repeated_family_false_positive_rate: geRepeated / ITERATIONS,
  cross_site_repeated_false_positive_rate: geCrossSite / ITERATIONS,
  target_rank_all_signs: `${targetRankAll}/${signTable.length}`,
  target_rank_frequency_comparable: `${targetRankComparable}/${comparable.length}`,
  comparable_signs_top10: comparable.slice(0, 10).map((row) => `${row.sign}:${row.cell_count}:${row.cross_site_noncopy_repeated_families}`).join(';'),
  falsifier:
    'If source-normalized rows collapse `002-610-125-032` or `002-297-350-125-413` into copies/noncomparable readings, or if frequency-matched non-125 signs routinely show the same cross-site non-copy governed-template behavior, demote the portable-125 bet.',
  next_prediction:
    'New governed post-002 templates containing `125` should be unusually likely to have a following sub-tail and to recur across site/object contexts; a terminal bare `002-H-125` class would weaken the title/suffix reading.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({ ...summary, target_stats: targetStats, target_families: targetFamilies, sign_table: signTable }, null, 2),
  'utf8',
);
writeCsv(path.join(OUT_DIR, `${PREFIX}.csv`), [summary], [
  'run_date',
  'bet_id',
  'vector',
  'confidence_tier',
  'risky_bet',
  'observed',
  'adversarial_test',
  'false_positive_rate',
  'repeated_family_false_positive_rate',
  'cross_site_repeated_false_positive_rate',
  'target_rank_all_signs',
  'target_rank_frequency_comparable',
  'comparable_signs_top10',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_target_families.csv`), targetFamilies, [
  'template_4',
  'count',
  'repeated',
  'cross_site',
  'cross_type',
  'top_exact_share',
  'exact_dominated',
  'sites',
  'types',
  'prev_before_002',
  'objects',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_sign_table.csv`), signTable, [
  'sign',
  'cell_count',
  'containing_families',
  'repeated_families',
  'cross_site_repeated_families',
  'cross_site_noncopy_repeated_families',
  'repeated_templates',
  'cross_site_templates',
  'cross_site_noncopy_templates',
]);

console.log(JSON.stringify(summary, null, 2));
