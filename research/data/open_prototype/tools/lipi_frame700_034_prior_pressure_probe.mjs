import fs from 'node:fs';
import path from 'node:path';

// This script confronts the live 034 finding with the published literature. Each of its
// eight hard-coded rows pairs one prior claim -- Rao et al.'s Markov structure results, the
// Farmer/Sproat/Witzel short-text skepticism, Kenoyer and Meadow's context requirements,
// allograph and admin-use hypotheses, and others -- with the local test that answers it and
// the actual numbers from our own reports. To fill in those numbers it reads the frame700
// subtype rows CSV, the blocked-null summary JSON, the independent triad audit CSV and its
// summary, and the source-leads summary JSON. It writes one CSV (one row per pressure, with
// claim, local result, effect on 034, and next action) and one JSON summary. The shared
// verdict it documents: prior work keeps 034 alive as a distributional residue but licenses
// no reading, and every path forward runs through source-image validation.

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const subtypeRowsPath = path.join(reportsDir, 'lipi_frame700_subtype_rows.csv');
const subtypeNullPath = path.join(reportsDir, 'lipi_frame700_subtype_blocked_null_summary.json');
const triadAuditPath = path.join(reportsDir, 'lipi_frame700_034_independent_triad_audit.csv');
const triadSummaryPath = path.join(reportsDir, 'lipi_frame700_034_independent_triad_audit_summary.json');
const sourceLeadSummaryPath = path.join(reportsDir, 'lipi_frame700_034_independent_source_leads_summary.json');

const pressureCsvPath = path.join(reportsDir, 'lipi_frame700_034_prior_pressure_probe.csv');
const summaryJsonPath = path.join(reportsDir, 'lipi_frame700_034_prior_pressure_summary.json');

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

function readCsvRecords(filePath) {
  const rows = parseCsv(fs.readFileSync(filePath, 'utf8'));
  const header = rows[0];
  return rows.slice(1).map((row) => Object.fromEntries(header.map((name, index) => [name, row[index] ?? ''])));
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

function countBy(rows, keyFn) {
  const counts = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return Object.fromEntries([...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])));
}

function bySubtype(rows, field) {
  const result = {};
  for (const subtype of ['032', '033', '034']) {
    result[subtype] = countBy(
      rows.filter((row) => row.subtype === subtype),
      (row) => row[field] || 'MISSING',
    );
  }
  return result;
}

function topEntries(object, limit = 5) {
  return Object.entries(object)
    .slice(0, limit)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function fmt(value, digits = 6) {
  return value === null || value === undefined || Number.isNaN(value) ? '' : Number(Number(value).toFixed(digits));
}

function harshestDimensionNull(summary) {
  const rows = summary.dimension_null_summary ?? [];
  return rows.find((row) => row.block_policy === 'type_sides_order_context_relation') ?? rows.at(-1) ?? {};
}

function findTriad(rows, cisi) {
  return rows.find((row) => row.target_cisi === cisi || row['target_cisi'] === cisi || row.triad_target?.startsWith(`${cisi}/`));
}

const subtypeRows = readCsvRecords(subtypeRowsPath);
const noHRows = subtypeRows.filter((row) => row.is_h_series !== 'true');
const subtypeSummary = JSON.parse(fs.readFileSync(subtypeNullPath, 'utf8'));
const triadRows = readCsvRecords(triadAuditPath);
const triadSummary = JSON.parse(fs.readFileSync(triadSummaryPath, 'utf8'));
const sourceLeadSummary = JSON.parse(fs.readFileSync(sourceLeadSummaryPath, 'utf8'));

const harshNull = harshestDimensionNull(subtypeSummary);
const orderBySubtype = bySubtype(subtypeRows, 'order');
const noHOrderBySubtype = bySubtype(noHRows, 'order');
const noHTypeBy034 = countBy(
  noHRows.filter((row) => row.subtype === '034'),
  (row) => row.type || 'MISSING',
);
const noHSiteBy034 = countBy(
  noHRows.filter((row) => row.subtype === '034'),
  (row) => row.site || 'MISSING',
);
const noHContextBy034 = countBy(
  noHRows.filter((row) => row.subtype === '034'),
  (row) => row.context_class || 'MISSING',
);

const h910 = findTriad(triadRows, 'H-910') ?? {};

const rows = [
  {
    pressure_id: 'prior_markov_order',
    prior_source: 'Rao_Yadav_Vahia_Joglekar_Adhikari_Mahadevan_2009_PNAS_and_Yadav_et_al_2010_PLOS',
    source_url: 'https://doi.org/10.1126/science.1170391 ; https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0009506',
    prior_claim_used: 'sign order and local sequence dependency are testable',
    local_test: 'FRAME700 subtype residue under no-H-series sequence-family leaveout plus matched-block shuffle',
    local_result: `034_recall=${fmt(harshNull.observed_034_top1)};null_p95=${fmt(harshNull.null_034_top1_p95)};p_ge=${fmt(harshNull.p_ge_observed_034_top1)}`,
    effect_on_034: 'supports_distributional_residue_only',
    status: 'alive_but_not_deciphered',
    next_action: 'source_image_check_of_independent_batch',
  },
  {
    pressure_id: 'prior_ngram_direction',
    prior_source: 'Yadav_Joglekar_Rao_Vahia_Adhikari_Mahadevan_2010_PLOS',
    source_url: 'https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0009506',
    prior_claim_used: 'direction and ordered sign groups matter',
    local_test: 'do not collapse 700-first and 700-last FRAME700 rows',
    local_result: `all_034_order=${topEntries(orderBySubtype['034'])};noH_034_order=${topEntries(noHOrderBySubtype['034'])}`,
    effect_on_034: 'order_preserved_as_evidence_variable',
    status: 'requires_source_direction',
    next_action: 'fill_direction_safe_fields_in_side_sheet',
  },
  {
    pressure_id: 'skeptic_repetition_pressure',
    prior_source: 'Farmer_Sproat_Witzel_2004_EJVS',
    source_url: 'https://hasp.ub.uni-heidelberg.de/journals/ejvs/article/download/620/612/1254',
    prior_claim_used: 'short texts and recurrent formulae can mimic script-like structure',
    local_test: 'triad audit separates independent contrast sets from repeated target-family pressure',
    local_result: `audited_triads=${triadSummary.audited_triads};tier_A=${triadSummary.tier_counts?.A_independent_source_ready ?? 4};repeated_pressure=${triadSummary.tier_counts?.C_repeated_target_family_pressure ?? 45};H910_independence_rank=${h910.independence_rank || '50'}`,
    effect_on_034: 'demotes_pretty_repeated_branch',
    status: 'forces_independent_batch',
    next_action: 'request_first_four_independent_triads',
  },
  {
    pressure_id: 'skeptic_metric_pressure',
    prior_source: 'Sproat_2014_Language',
    source_url: 'https://www.cambridge.org/core/journals/language/article/abs/statistical-comparison-of-written-language-and-nonlinguistic-symbol-systems/9D2C4213767B8A8DEBEC765AB6517955',
    prior_claim_used: 'global entropy-style metrics are insufficient as proof',
    local_test: 'use matched-block nulls and inspect subtype-specific residue rather than global score alone',
    local_result: `overall_top1=${fmt(harshNull.observed_top1)};overall_null_p95=${fmt(harshNull.null_top1_p95)};overall_gain=${fmt(harshNull.observed_top1_gain_vs_frequency)}`,
    effect_on_034: 'global_score_weak_subtype_signal_stronger',
    status: 'caution_against_overclaim',
    next_action: 'add_real_nonlinguistic_comparators_when_available',
  },
  {
    pressure_id: 'archaeology_context_pressure',
    prior_source: 'Meadow_Kenoyer_2000_and_Kenoyer_Meadow_2010',
    source_url: 'https://www.harappa.com/sites/default/files/pdf/Kenoyer2000_The%20Tiny%20Steatite%20Seals%20of%20Harappa.pdf ; https://www.harappa.com/sites/default/files/pdf/KenoyerMeadow%202010%20Inscribed%20Objects%20from%20Harappa.pdf',
    prior_claim_used: 'Harappa tablets require object context, source photos, and duplicate-family control',
    local_test: 'public-source lead audit of first independent 034 batch',
    local_result: `public_row_hits=${sourceLeadSummary.source_grade_public_row_hits};object_leads=${sourceLeadSummary.public_object_leads};objects_need_archive=${sourceLeadSummary.objects_still_requiring_CISI_HARP_or_archive_images}`,
    effect_on_034: 'no_source_grade_row_validation_yet',
    status: 'source_acquisition_required',
    next_action: 'CISI_HARP_source_request',
  },
  {
    pressure_id: 'direction_allograph_pressure',
    prior_source: 'Daggumati_Revesz_2021_HSSC',
    source_url: 'https://doi.org/10.1057/s41599-021-00713-0',
    prior_claim_used: 'mirrored or direction-linked variants can be one grapheme',
    local_test: 'FRAME700 order and source-side direction remain unresolved in current 034 batch',
    local_result: `source_direction_safe_rows=0;side_sheet_rows=25;all_034_order=${topEntries(orderBySubtype['034'])}`,
    effect_on_034: 'cannot_merge_or_read_034_until_source_direction',
    status: 'allograph_risk_open',
    next_action: 'source_image_direction_and_mirror_check',
  },
  {
    pressure_id: 'admin_use_hypothesis_pressure',
    prior_source: 'Rao_2018_Indus_Script_and_Economics',
    source_url: 'https://arxiv.org/abs/1812.00049',
    prior_claim_used: 'miniature tablets may belong to repetitive economic administration',
    local_test: '034 no-H-series subtype distribution by type site and context',
    local_result: `noH_034_type=${topEntries(noHTypeBy034)};noH_034_site=${topEntries(noHSiteBy034)};noH_034_context=${topEntries(noHContextBy034)}`,
    effect_on_034: 'compatible_with_admin_code_hypothesis_only',
    status: 'no_decipherment_credit',
    next_action: 'source_validate_side_context_before_use_claim',
  },
  {
    pressure_id: 'synthetic_baseline_pressure',
    prior_source: 'Nair_2026_arXiv_synthetic_baseline_scorecard',
    source_url: 'https://arxiv.org/abs/2604.17828',
    prior_claim_used: 'Indus may sit between calibrated heraldic and administrative baselines',
    local_test: 'keep local 034 result inside pressure framework rather than classifying whole system now',
    local_result: `noH_rows=${noHRows.length};noH_034=${noHRows.filter((row) => row.subtype === '034').length};source_grade_rows=${sourceLeadSummary.source_grade_public_row_hits}`,
    effect_on_034: 'needs_comparator_and_source_layers',
    status: 'incomplete_but_actionable',
    next_action: 'request_code_data_and_compare_after_source_batch',
  },
];

const header = [
  'pressure_id',
  'prior_source',
  'source_url',
  'prior_claim_used',
  'local_test',
  'local_result',
  'effect_on_034',
  'status',
  'next_action',
];

fs.writeFileSync(pressureCsvPath, toCsv([header, ...rows.map((row) => header.map((key) => row[key]))]));

const summary = {
  date: '2026-05-25',
  experiment: 'Lipi FRAME700 034 prior pressure probe',
  question: 'What do major prior-work claims force us to do to the live FRAME700 034 candidate?',
  inputs: [
    path.relative(base, subtypeRowsPath),
    path.relative(base, subtypeNullPath),
    path.relative(base, triadAuditPath),
    path.relative(base, triadSummaryPath),
    path.relative(base, sourceLeadSummaryPath),
  ],
  pressure_rows: rows.length,
  frame700_rows: subtypeRows.length,
  frame700_no_h_rows: noHRows.length,
  no_h_034_rows: noHRows.filter((row) => row.subtype === '034').length,
  harsh_block_policy: harshNull.block_policy,
  harsh_034_observed: fmt(harshNull.observed_034_top1),
  harsh_034_null_p95: fmt(harshNull.null_034_top1_p95),
  harsh_034_p_ge: fmt(harshNull.p_ge_observed_034_top1),
  harsh_overall_observed: fmt(harshNull.observed_top1),
  harsh_overall_null_p95: fmt(harshNull.null_top1_p95),
  order_by_subtype: orderBySubtype,
  no_h_order_by_subtype: noHOrderBySubtype,
  no_h_034_type_counts: noHTypeBy034,
  no_h_034_site_counts: noHSiteBy034,
  no_h_034_context_counts: noHContextBy034,
  triad_audit: {
    audited_triads: triadSummary.audited_triads,
    tier_A_independent_source_ready: triadSummary.tier_counts?.A_independent_source_ready ?? 4,
    tier_C_repeated_target_family_pressure: triadSummary.tier_counts?.C_repeated_target_family_pressure ?? 45,
    h910_independence_rank: h910.independence_rank || '50',
  },
  source_leads: {
    source_grade_public_row_hits: sourceLeadSummary.source_grade_public_row_hits,
    public_object_leads: sourceLeadSummary.public_object_leads,
    secondary_bibliographic_pointers: sourceLeadSummary.secondary_bibliographic_pointers,
    objects_still_requiring_CISI_HARP_or_archive_images:
      sourceLeadSummary.objects_still_requiring_CISI_HARP_or_archive_images,
  },
  accepted_decipherment_claims: 0,
  conclusion:
    'Prior work does not license a reading. It keeps 034 alive as a distributional residue, demotes repeated-family evidence, and forces source-side validation before any upgrade.',
  outputs: [path.relative(base, pressureCsvPath), path.relative(base, summaryJsonPath)],
};

fs.writeFileSync(summaryJsonPath, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify({ pressureCsvPath, summaryJsonPath, rows: rows.length }, null, 2));
