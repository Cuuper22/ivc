// Null tests for the Meluhha join surface: how impressive is it, really, that
// cuneiform Meluhha texts and external Indus objects share find sites? This
// script reads the expanded cuneiform attestations and the external objects
// table, scores the observed overlap (total join rows, joins involving
// name/admin attestations, distinct joined sites), then runs two randomized
// nulls of 10000 iterations each (override with
// IVC_MELUHHA_JOIN_NULL_ITERATIONS): reassign each attestation's site aliases
// at random from all external sites, and from Mesopotamian sites only. It also
// records the decisive thought experiment: any non-Meluhha corpus with the
// same provenience distribution would reproduce the overlap exactly, so site
// overlap is infrastructure, not evidence. Writes the per-iteration CSV and a
// JSON summary whose decision is not to promote any site-overlap row.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const OUT = path.join(ROOT, 'data', 'meluhha');
const RUN_DATE = '2026-05-29';
const ITERATIONS = Number.parseInt(process.env.IVC_MELUHHA_JOIN_NULL_ITERATIONS ?? '10000', 10);

const CUNEIFORM = path.join(OUT, 'cuneiform_attestations_expanded.csv');
const EXTERNAL = path.join(OUT, 'external_indus_objects.csv');

const ITERATION_FIELDS = [
  'null_model',
  'iteration',
  'join_rows',
  'admin_or_name_join_rows',
  'distinct_join_sites',
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

function normalizePlace(text) {
  return String(text ?? '').normalize('NFD').replace(/\p{Diacritic}/gu, '');
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function siteAliases(provenience) {
  const aliases = [];
  const text = normalizePlace(provenience);
  if (/girsu/i.test(text)) aliases.push('Girsu');
  if (/tello/i.test(text)) aliases.push('Tello');
  if (/\bur\b/i.test(text)) aliases.push('Ur');
  if (/nippur/i.test(text)) aliases.push('Nippur');
  if (/irisagrig/i.test(text)) aliases.push('Irisagrig');
  return unique(aliases);
}

function mulberry32(seed) {
  return function next() {
    let t = seed += 0x6D2B79F5;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function sampleDistinct(pool, size, random) {
  const copy = [...pool];
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy.slice(0, Math.min(size, copy.length));
}

function countBy(rows, key) {
  const counts = {};
  for (const row of rows) counts[row[key]] = (counts[row[key]] ?? 0) + 1;
  return counts;
}

function isAdminOrNameRow(row) {
  return /personal_name|ethnonym_group|ethnonym_title|object_or_commodity_designation/i.test(row.token_type);
}

function scoreRows(rows, siteCounts) {
  let joinRows = 0;
  let adminOrNameJoinRows = 0;
  const sitesWithJoin = new Set();

  for (const row of rows) {
    for (const alias of row.aliases) {
      const count = siteCounts[alias] ?? 0;
      if (count > 0) sitesWithJoin.add(alias);
      joinRows += count;
      if (isAdminOrNameRow(row)) adminOrNameJoinRows += count;
    }
  }

  return {
    join_rows: joinRows,
    admin_or_name_join_rows: adminOrNameJoinRows,
    distinct_join_sites: sitesWithJoin.size,
  };
}

function summarizeNull(nullModel, rows, observed) {
  const n = rows.length;
  const mean = (field) => rows.reduce((sum, row) => sum + Number(row[field]), 0) / n;
  const ge = (field) => rows.filter((row) => Number(row[field]) >= observed[field]).length / n;
  const max = (field) => Math.max(...rows.map((row) => Number(row[field])));
  return {
    null_model: nullModel,
    iterations: n,
    means: {
      join_rows: mean('join_rows'),
      admin_or_name_join_rows: mean('admin_or_name_join_rows'),
      distinct_join_sites: mean('distinct_join_sites'),
    },
    max_values: {
      join_rows: max('join_rows'),
      admin_or_name_join_rows: max('admin_or_name_join_rows'),
      distinct_join_sites: max('distinct_join_sites'),
    },
    null_ge_observed_share: {
      join_rows: ge('join_rows'),
      admin_or_name_join_rows: ge('admin_or_name_join_rows'),
      distinct_join_sites: ge('distinct_join_sites'),
    },
  };
}

function runRandomSiteNull(cuneiformRows, sitePool, siteCounts, nullModel, seed) {
  const random = mulberry32(seed);
  const iterations = [];
  const rowsWithAliasCounts = cuneiformRows.map((row) => ({
    ...row,
    aliasCount: row.aliases.length,
  }));

  for (let iteration = 0; iteration < ITERATIONS; iteration += 1) {
    const randomized = rowsWithAliasCounts.map((row) => ({
      ...row,
      aliases: row.aliasCount ? sampleDistinct(sitePool, row.aliasCount, random) : [],
    }));
    const score = scoreRows(randomized, siteCounts);
    iterations.push({
      null_model: nullModel,
      iteration,
      ...score,
    });
  }
  return iterations;
}

function main() {
  const cuneiformRows = parseCsv(fs.readFileSync(CUNEIFORM, 'utf8'))
    .map((row) => ({ ...row, aliases: siteAliases(row.provenience) }));
  const externalRows = parseCsv(fs.readFileSync(EXTERNAL, 'utf8'));
  const siteCounts = countBy(externalRows, 'site');
  const allExternalSites = Object.keys(siteCounts);
  const mesopotamianSites = unique(externalRows
    .filter((row) => row.region === 'Mesopotamia')
    .map((row) => row.site));

  const observed = scoreRows(cuneiformRows, siteCounts);
  const allSiteIterations = runRandomSiteNull(
    cuneiformRows,
    allExternalSites,
    siteCounts,
    'random_site_aliases_all_external_sites',
    0xA11CE,
  );
  const mesopotamiaIterations = runRandomSiteNull(
    cuneiformRows,
    mesopotamianSites,
    siteCounts,
    'random_site_aliases_mesopotamia_only',
    0xBADC0DE,
  );
  const iterations = [...allSiteIterations, ...mesopotamiaIterations];

  writeCsv(path.join(OUT, 'meluhha_join_surface_null_iterations.csv'), iterations, ITERATION_FIELDS);
  const summary = {
    date: RUN_DATE,
    status: 'join_surface_forger_control_no_claim_accepted',
    iterations_per_null_model: ITERATIONS,
    observed,
    nulls: [
      summarizeNull('random_site_aliases_all_external_sites', allSiteIterations, observed),
      summarizeNull('random_site_aliases_mesopotamia_only', mesopotamiaIterations, observed),
      {
        null_model: 'provenance_preserving_non_meluhha_control',
        iterations: 1,
        null_ge_observed_share: {
          join_rows: 1,
          admin_or_name_join_rows: 1,
          distinct_join_sites: 1,
        },
        interpretation: 'Any non-Meluhha corpus with the same cuneiform provenience distribution would reproduce the site-overlap count exactly. Site overlap is therefore infrastructure, not evidence.',
      },
    ],
    files: {
      iterations: 'data/meluhha/meluhha_join_surface_null_iterations.csv',
      summary: 'data/meluhha/meluhha_join_surface_null_summary.json',
    },
    decision: 'Do not promote site-overlap rows to candidate external anchors. Add sign-sequence, object-type, date, and non-Meluhha matched controls first.',
  };
  fs.writeFileSync(path.join(OUT, 'meluhha_join_surface_null_summary.json'), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
  console.log(JSON.stringify({
    observed,
    iterations: iterations.length,
    all_site_fpr_join_rows: summary.nulls[0].null_ge_observed_share.join_rows,
    mesopotamia_fpr_join_rows: summary.nulls[1].null_ge_observed_share.join_rows,
  }, null, 2));
}

main();
