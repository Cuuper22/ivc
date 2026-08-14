// Assembles the master witness matrix for the 032-002-Y source-visibility
// campaign. Three earlier artifacts feed in: the source-route probe (which
// objects have any route to a source image), the current source-function
// table (is the sequence visible on the actual object, on one physical
// line?), and the token-box scaffold (per-sign boxes drawn on source images,
// with status and confidence). This script joins them by CISI number,
// grades each row's admissibility from "not_source_visible" up through
// weak/lowres/medium-low/medium token-box candidate tiers, and checks
// whether the source-visible set covers all three structural categories,
// 4+ Y values, and 3+ sites. An exploratory null (iterations and seed from
// the CLI, default 10000) redraws the same number of visible rows at random
// to show how unsurprising that coverage shape is — explicitly not an
// accepted false-positive rate, since acquisition was target-driven.
// Writes the witness-matrix CSV, the null-iterations CSV, and a JSON
// summary.
import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const routePath = path.join(reportsDir, 'campaign_032_002_y_source_route_probe.csv');
const currentPath = path.join(reportsDir, 'campaign_032_002_y_source_function_current_table.csv');
const boxesPath = path.join(reportsDir, 'campaign_032_002_y_token_box_scaffold_v1.csv');
const outMatrix = path.join(reportsDir, 'source_visible_032_002_y_witness_matrix.csv');
const outNulls = path.join(reportsDir, 'source_visible_032_002_y_coverage_null_iterations.csv');
const outSummary = path.join(reportsDir, 'source_visible_032_002_y_summary.json');

const iterations = Number(process.argv[2] ?? 10000);
const seedBase = Number(process.argv[3] ?? 20260529);

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

function loadCsv(filePath) {
  const rows = parseCsv(fs.readFileSync(filePath, 'utf8'));
  const header = rows[0] ?? [];
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

function mulberry32(seed) {
  let value = seed >>> 0;
  return () => {
    value += 0x6d2b79f5;
    let t = value;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function sampleWithoutReplacement(items, n, rng) {
  const copy = items.slice();
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy.slice(0, n);
}

function countBy(rows, key) {
  const out = new Map();
  for (const row of rows) out.set(row[key] ?? '', (out.get(row[key] ?? '') ?? 0) + 1);
  return Object.fromEntries([...out.entries()].sort((a, b) => a[0].localeCompare(b[0])));
}

function unique(rows, key) {
  return [...new Set(rows.map((row) => row[key]).filter(Boolean))].sort((a, b) => a.localeCompare(b));
}

function tokenBoxIndex(rows) {
  const out = new Map();
  for (const row of rows) {
    const cisi = row.cisi;
    if (!out.has(cisi)) {
      out.set(cisi, {
        statuses: new Map(),
        confidences: new Set(),
        overlays: new Set(),
        source_images: new Set(),
        notes: new Set(),
        token_labels: new Set(),
      });
    }
    const target = out.get(cisi);
    target.statuses.set(row.status, (target.statuses.get(row.status) ?? 0) + 1);
    if (row.confidence) target.confidences.add(row.confidence);
    if (row.overlay_image) target.overlays.add(row.overlay_image);
    if (row.source_image_abs) target.source_images.add(row.source_image_abs);
    if (row.note) target.notes.add(row.note);
    if (row.token_label) target.token_labels.add(row.token_label);
  }
  return out;
}

function summarizeBox(box) {
  if (!box) {
    return {
      token_box_status: 'none',
      token_box_confidence: '',
      token_box_tier: 'none',
      token_box_overlay: '',
      token_box_labels: '',
      token_box_note: '',
    };
  }
  const statuses = [...box.statuses.entries()].map(([k, v]) => `${k}:${v}`).join(';');
  const confidences = [...box.confidences].sort().join(';');
  const statusNames = [...box.statuses.keys()];
  const tier =
    statusNames.includes('candidate_pass') && [...box.confidences].some((c) => c === 'medium')
      ? 'medium_candidate_token_box'
      : statusNames.includes('candidate_pass') && [...box.confidences].some((c) => c === 'medium_low')
        ? 'medium_low_candidate_token_box'
        : statusNames.includes('candidate_pass_lowres')
          ? 'lowres_candidate_token_box'
          : statusNames.includes('candidate_weak')
            ? 'weak_token_box'
            : 'none';
  return {
    token_box_status: statuses,
    token_box_confidence: confidences,
    token_box_tier: tier,
    token_box_overlay: [...box.overlays].sort().join(';'),
    token_box_labels: [...box.token_labels].sort().join(';'),
    token_box_note: [...box.notes].sort().join(' | '),
  };
}

function classifyRow(route, current, box) {
  const sourceVisible = current?.source_visible ?? 'not_checked';
  const samePhysicalLine = current?.same_physical_line ?? 'not_checked';
  const rowUsable = sourceVisible === 'yes' && samePhysicalLine === 'yes';
  const boxSummary = summarizeBox(box);
  let admissibility = 'not_source_visible';
  if (rowUsable && boxSummary.token_box_tier === 'medium_candidate_token_box') {
    admissibility = 'source_visible_medium_token_box_candidate';
  } else if (rowUsable && boxSummary.token_box_tier === 'medium_low_candidate_token_box') {
    admissibility = 'source_visible_medium_low_token_box_candidate';
  } else if (rowUsable && boxSummary.token_box_tier === 'lowres_candidate_token_box') {
    admissibility = 'source_visible_lowres_token_box_candidate';
  } else if (rowUsable && boxSummary.token_box_tier === 'weak_token_box') {
    admissibility = 'source_visible_weak_token_box_candidate';
  } else if (rowUsable) {
    admissibility = 'source_visible_row_level_only';
  } else if (sourceVisible === 'partial') {
    admissibility = 'partial_source_object_visible_side_unresolved';
  } else if (route?.route_status) {
    admissibility = route.route_status;
  }
  return { rowUsable, admissibility, ...boxSummary };
}

function coverageStats(rows) {
  const sourceRows = rows.filter((row) => row.source_visible === 'yes' && row.same_physical_line === 'yes');
  const mediumRows = sourceRows.filter((row) => row.token_box_tier === 'medium_candidate_token_box');
  const mediumOrBetterRows = sourceRows.filter((row) =>
    ['medium_candidate_token_box', 'medium_low_candidate_token_box'].includes(row.token_box_tier),
  );
  return {
    source_visible_rows: sourceRows.length,
    medium_token_box_rows: mediumRows.length,
    medium_or_medium_low_token_box_rows: mediumOrBetterRows.length,
    source_visible_categories: unique(sourceRows, 'category'),
    source_visible_y_values: unique(sourceRows, 'y_after_002'),
    source_visible_sites: unique(sourceRows, 'site'),
    source_visible_category_counts: countBy(sourceRows, 'category'),
    source_visible_y_counts: countBy(sourceRows, 'y_after_002'),
    source_visible_site_counts: countBy(sourceRows, 'site'),
    token_box_tier_counts: countBy(sourceRows, 'token_box_tier'),
    admissibility_counts: countBy(rows, 'admissibility'),
  };
}

function coverageCriterion(rows) {
  const categories = unique(rows, 'category');
  const yValues = unique(rows, 'y_after_002');
  const sites = unique(rows, 'site');
  return {
    has_all_three_categories:
      categories.includes('target_240_220_032') &&
      categories.includes('non240_a_220_032') &&
      categories.includes('outside_a_220_x_032'),
    has_at_least_four_y_values: yValues.length >= 4,
    has_at_least_three_sites: sites.length >= 3,
    has_target_and_non240_817: rows.some((row) => row.category === 'target_240_220_032' && row.y_after_002 === '817') &&
      rows.some((row) => row.category === 'non240_a_220_032' && row.y_after_002 === '817'),
    has_outside_861_multisite: new Set(
      rows
        .filter((row) => row.category === 'outside_a_220_x_032' && row.y_after_002 === '861')
        .map((row) => row.site),
    ).size >= 3,
  };
}

function runCoverageNull(routeRows, sourceVisibleCount) {
  const out = [];
  for (let iteration = 0; iteration < iterations; iteration++) {
    const rng = mulberry32(seedBase + iteration * 17);
    const sample = sampleWithoutReplacement(routeRows, sourceVisibleCount, rng);
    const criteria = coverageCriterion(sample);
    out.push({
      iteration,
      ...criteria,
      categories: unique(sample, 'category').join(';'),
      y_values: unique(sample, 'y_after_002').join(';'),
      sites: unique(sample, 'site').join(';'),
    });
  }
  return out;
}

const routeRows = loadCsv(routePath);
const currentRows = loadCsv(currentPath);
const boxRows = loadCsv(boxesPath);
const currentByCisi = new Map(currentRows.map((row) => [row.cisi, row]));
const boxesByCisi = tokenBoxIndex(boxRows);

const matrixRows = routeRows.map((route) => {
  const current = currentByCisi.get(route.cisi) ?? {};
  const classification = classifyRow(route, current, boxesByCisi.get(route.cisi));
  return {
    cisi: route.cisi,
    object_ids: route.object_ids,
    category: route.category,
    site: route.site,
    type: route.type,
    symbol: route.symbol,
    material: route.material,
    condition: route.condition,
    text: route.text,
    y_after_002: route.y_after_002,
    y_terminal: route.y_terminal,
    route_status: route.route_status,
    source_visible: current.source_visible ?? 'not_checked',
    same_physical_line: current.same_physical_line ?? 'not_checked',
    side_mapping_status: current.side_mapping_status ?? '',
    source_page: current.source_page ?? '',
    source_crop: current.crop_file ?? '',
    packet_status: current.packet_status ?? '',
    admissibility: classification.admissibility,
    token_box_tier: classification.token_box_tier,
    token_box_status: classification.token_box_status,
    token_box_confidence: classification.token_box_confidence,
    token_box_labels: classification.token_box_labels,
    token_box_overlay: classification.token_box_overlay,
    route_next_action: route.next_action,
    note: current.note ?? '',
    token_box_note: classification.token_box_note,
  };
});

const stats = coverageStats(matrixRows);
const sourceVisibleRows = matrixRows.filter(
  (row) => row.source_visible === 'yes' && row.same_physical_line === 'yes',
);
const observedCriteria = coverageCriterion(sourceVisibleRows);
const nullRows = runCoverageNull(routeRows, sourceVisibleRows.length);
const nullSummary = Object.fromEntries(
  Object.keys(observedCriteria).map((key) => [
    key,
    nullRows.filter((row) => row[key] === true).length / Math.max(1, nullRows.length),
  ]),
);

const matrixHeaders = [
  'cisi',
  'object_ids',
  'category',
  'site',
  'type',
  'symbol',
  'material',
  'condition',
  'text',
  'y_after_002',
  'y_terminal',
  'route_status',
  'source_visible',
  'same_physical_line',
  'side_mapping_status',
  'source_page',
  'source_crop',
  'packet_status',
  'admissibility',
  'token_box_tier',
  'token_box_status',
  'token_box_confidence',
  'token_box_labels',
  'token_box_overlay',
  'route_next_action',
  'note',
  'token_box_note',
];
fs.writeFileSync(outMatrix, toCsv([matrixHeaders, ...matrixRows.map((row) => matrixHeaders.map((key) => row[key]))]), 'utf8');
const nullHeaders = ['iteration', ...Object.keys(observedCriteria), 'categories', 'y_values', 'sites'];
fs.writeFileSync(outNulls, toCsv([nullHeaders, ...nullRows.map((row) => nullHeaders.map((key) => row[key]))]), 'utf8');

const summary = {
  generated_at_local: new Date().toISOString(),
  route_rows: routeRows.length,
  source_visible_count: sourceVisibleRows.length,
  stats,
  observed_coverage_criteria: observedCriteria,
  coverage_null: {
    interpretation_boundary:
      'Exploratory only: acquisition was target-driven, not random. These rates diagnose how unsurprising the coverage shape is under random row visibility, not an accepted false-positive rate for the source claim.',
    iterations,
    source_visible_count: sourceVisibleRows.length,
    false_positive_rates: nullSummary,
  },
  accepted_boundary:
    'Current evidence supports a candidate source-normalized structural packet: 032-002-Y is source-visible on a same physical line across target, non-240 A-220, and outside-032 contexts. It does not support token values, phonetics, translations, language identity, or accepted sign meanings.',
  artifact_files: [
    'data/open_prototype/reports/source_visible_032_002_y_witness_matrix.csv',
    'data/open_prototype/reports/source_visible_032_002_y_coverage_null_iterations.csv',
    'data/open_prototype/reports/source_visible_032_002_y_summary.json',
  ],
};
fs.writeFileSync(outSummary, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
