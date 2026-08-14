// Null test for the third slot in 520-220-X sequences: does the sign X predict whether the
// inscription closes right there or continues, better than knowing the site and object type
// would? We load the extraction rows from campaign_520_220_x_extraction_addendum.csv, keep
// only rows with a clean behavior label (terminal_closed versus medial_with_closed_tail),
// and score a leave-one-out majority-vote predictor twice — once keyed on the third-slot
// sign, once on site+type — in two scopes: raw rows, and rows collapsed to one per exact
// inscription text (so copies cannot vote twice). Five seeded null models then shuffle the
// closure labels globally or within site/type/material/shape blocks (5,000 iterations each,
// overridable via the IVC_520_220_CONTEXT_ITERATIONS environment variable) to see how often
// chance matches the observed accuracy and its gain over the site+type baseline. The claim
// under test is contextual only — slot behavior, not sign meaning. Writes iteration and
// scope-row CSVs plus a JSON summary to data/open_prototype/reports.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const REPORTS = path.join(ROOT, 'data', 'open_prototype', 'reports');
const INPUT = path.join(REPORTS, 'campaign_520_220_x_extraction_addendum.csv');
const RUN_DATE = '2026-05-29';
const ITERATIONS = Number.parseInt(process.env.IVC_520_220_CONTEXT_ITERATIONS ?? '5000', 10);

const ITERATION_FIELDS = [
  'scope',
  'null_model',
  'iteration',
  'third_slot_accuracy',
  'site_type_accuracy',
  'gain_vs_site_type',
];

const ROW_FIELDS = [
  'scope',
  'id',
  'cisi',
  'site',
  'type',
  'material',
  'shape',
  'text',
  'third_slot',
  'x_position_behavior',
  'closure_binary',
  'tail_token_count',
  'tail_tokens',
  'companion_formula_classes',
  'duplicate_weight',
  'source_ids',
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

function mulberry32(seed) {
  return function next() {
    let t = seed += 0x6D2B79F5;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffle(values, random) {
  const out = values.slice();
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function normalizeValue(value) {
  const text = String(value ?? '').trim();
  return text && text !== '-' ? text : 'NA';
}

function closureBinary(row) {
  if (row.x_position_behavior === 'terminal_closed') return 'terminal_closed';
  if (row.x_position_behavior === 'medial_with_closed_tail') return 'continues_after_x';
  return '';
}

function majority(values) {
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))[0]?.[0] ?? '';
}

function fieldKey(row, fields) {
  if (!fields.length) return '__global__';
  return fields.map((field) => normalizeValue(row[field])).join('|');
}

function scoreLoo(rows, predictorFields) {
  let correct = 0;
  for (let i = 0; i < rows.length; i += 1) {
    const target = rows[i].closure_binary;
    const predictor = fieldKey(rows[i], predictorFields);
    const peerTargets = [];
    const globalTargets = [];
    for (let j = 0; j < rows.length; j += 1) {
      if (i === j) continue;
      globalTargets.push(rows[j].closure_binary);
      if (fieldKey(rows[j], predictorFields) === predictor) peerTargets.push(rows[j].closure_binary);
    }
    const predicted = peerTargets.length ? majority(peerTargets) : majority(globalTargets);
    if (predicted === target) correct += 1;
  }
  return correct / rows.length;
}

function scoreRows(rows) {
  const thirdSlotAccuracy = scoreLoo(rows, ['third_slot']);
  const siteTypeAccuracy = scoreLoo(rows, ['site', 'type']);
  return {
    third_slot_accuracy: thirdSlotAccuracy,
    site_type_accuracy: siteTypeAccuracy,
    gain_vs_site_type: thirdSlotAccuracy - siteTypeAccuracy,
  };
}

function groupIndexes(rows, blockFields) {
  const groups = new Map();
  rows.forEach((row, index) => {
    const key = fieldKey(row, blockFields);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(index);
  });
  return [...groups.values()];
}

function shuffledRows(rows, blockFields, random) {
  const out = rows.map((row) => ({ ...row }));
  for (const indexes of groupIndexes(rows, blockFields)) {
    const labels = shuffle(indexes.map((index) => rows[index].closure_binary), random);
    indexes.forEach((index, offset) => {
      out[index].closure_binary = labels[offset];
    });
  }
  return out;
}

function collapseExactText(rows) {
  const families = new Map();
  for (const row of rows) {
    if (!families.has(row.text)) {
      families.set(row.text, {
        ...row,
        duplicate_weight: 0,
        source_ids: [],
      });
    }
    const family = families.get(row.text);
    family.duplicate_weight += 1;
    family.source_ids.push(row.id);
  }
  return [...families.values()].map((row) => ({
    ...row,
    source_ids: row.source_ids.join('|'),
  }));
}

function countsBy(rows, field) {
  const counts = {};
  for (const row of rows) counts[row[field]] = (counts[row[field]] ?? 0) + 1;
  return counts;
}

function summarizeNull(nullModel, rows, observed) {
  const n = rows.length;
  const mean = (field) => rows.reduce((sum, row) => sum + row[field], 0) / n;
  const max = (field) => Math.max(...rows.map((row) => row[field]));
  const ge = (field) => rows.filter((row) => row[field] >= observed[field]).length / n;
  return {
    null_model: nullModel,
    iterations: n,
    means: {
      third_slot_accuracy: mean('third_slot_accuracy'),
      site_type_accuracy: mean('site_type_accuracy'),
      gain_vs_site_type: mean('gain_vs_site_type'),
    },
    max_values: {
      third_slot_accuracy: max('third_slot_accuracy'),
      site_type_accuracy: max('site_type_accuracy'),
      gain_vs_site_type: max('gain_vs_site_type'),
    },
    null_ge_observed_share: {
      third_slot_accuracy: ge('third_slot_accuracy'),
      gain_vs_site_type: ge('gain_vs_site_type'),
    },
  };
}

function runScope(scopeName, rows, seed) {
  const observed = scoreRows(rows);
  const nullDefs = [
    { name: 'closure_shuffle_global', fields: [] },
    { name: 'closure_shuffle_within_site', fields: ['site'] },
    { name: 'closure_shuffle_within_type', fields: ['type'] },
    { name: 'closure_shuffle_within_site_type', fields: ['site', 'type'] },
    { name: 'closure_shuffle_within_site_type_material_shape', fields: ['site', 'type', 'material', 'shape'] },
  ];
  const iterations = [];
  const summaries = [];
  nullDefs.forEach((def, defIndex) => {
    const random = mulberry32(seed + defIndex * 1000003);
    const perNull = [];
    for (let iteration = 0; iteration < ITERATIONS; iteration += 1) {
      const score = scoreRows(shuffledRows(rows, def.fields, random));
      const entry = {
        scope: scopeName,
        null_model: def.name,
        iteration,
        ...score,
      };
      iterations.push(entry);
      perNull.push(score);
    }
    summaries.push(summarizeNull(def.name, perNull, observed));
  });

  return {
    observed: {
      scope: scopeName,
      rows: rows.length,
      third_slot_counts: countsBy(rows, 'third_slot'),
      closure_counts: countsBy(rows, 'closure_binary'),
      ...observed,
    },
    summaries,
    iterations,
    rows: rows.map((row) => ({ scope: scopeName, ...row })),
  };
}

function main() {
  const sourceRows = parseCsv(fs.readFileSync(INPUT, 'utf8'))
    .map((row) => ({
      ...row,
      site: normalizeValue(row.site),
      type: normalizeValue(row.type),
      material: normalizeValue(row.material),
      shape: normalizeValue(row.shape),
      closure_binary: closureBinary(row),
      duplicate_weight: 1,
      source_ids: row.id,
    }))
    .filter((row) => row.third_slot && row.closure_binary);

  const scopes = [
    ['raw_clean_behavior', sourceRows],
    ['exact_text_collapsed_clean_behavior', collapseExactText(sourceRows)],
  ];

  const scopeResults = scopes.map(([name, rows], index) => runScope(name, rows, 0x520220 + index * 0x10000));
  const iterations = scopeResults.flatMap((result) => result.iterations);
  const rowsOut = scopeResults.flatMap((result) => result.rows);
  const summary = {
    date: RUN_DATE,
    status: 'vector4_context_slot_candidate_not_sign_meaning',
    input: 'data/open_prototype/reports/campaign_520_220_x_extraction_addendum.csv',
    iterations_per_null_model: ITERATIONS,
    scopes: scopeResults.map((result) => ({
      observed: result.observed,
      nulls: result.summaries,
    })),
    interpretation_boundary: 'This tests closure/continuation context in the 520-220-X slot only. It is not a sign meaning, phonetic value, language identification, or translation.',
    files: {
      summary: 'data/open_prototype/reports/campaign_520_220_x_context_slot_null_summary.json',
      iterations: 'data/open_prototype/reports/campaign_520_220_x_context_slot_null_iterations.csv',
      scope_rows: 'data/open_prototype/reports/campaign_520_220_x_context_slot_scope_rows.csv',
    },
  };

  writeCsv(path.join(REPORTS, 'campaign_520_220_x_context_slot_null_iterations.csv'), iterations, ITERATION_FIELDS);
  writeCsv(path.join(REPORTS, 'campaign_520_220_x_context_slot_scope_rows.csv'), rowsOut, ROW_FIELDS);
  fs.writeFileSync(
    path.join(REPORTS, 'campaign_520_220_x_context_slot_null_summary.json'),
    `${JSON.stringify(summary, null, 2)}\n`,
    'utf8',
  );
  console.log(JSON.stringify({
    raw_rows: scopeResults[0].observed.rows,
    collapsed_rows: scopeResults[1].observed.rows,
    raw_observed: scopeResults[0].observed,
    collapsed_observed: scopeResults[1].observed,
  }, null, 2));
}

main();
