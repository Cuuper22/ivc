#!/usr/bin/env node

// The negative gate for eight named Vector 4 leads that came out of the
// broad discovery scan looking tempting — such as 407 with copper tablets,
// 400 with TAB:B tablets, and the 158-806 plant-icon (Phyt) lead. Where the
// discovery scan asks "does anything associate?", this script fixes each
// unit-context pair in advance and asks "does THIS pair survive its own
// nulls?" It reads the clean lipi scope rows, collapses them both ways
// (exact text-plus-context, and text only), computes each target's support,
// lift, and finite-population z, then runs the same four null models as the
// scan (three context shuffles, one unit shuffle) for 2000 iterations each
// (IVC_VECTOR4_TARGET_ITERATIONS overrides), keeping the worst-case null
// share. Every row is hard-coded claim_eligible = "no": surviving here only
// earns a place in the source-check queue, never a promoted meaning. Writes
// a per-target CSV, an iterations CSV, and a JSON summary.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const REPORTS = path.join(ROOT, 'data', 'open_prototype', 'reports');
const INPUT = path.join(REPORTS, 'lipi_scope_rows.csv');
const RUN_DATE = '2026-05-31';
const ITERATIONS = Number.parseInt(process.env.IVC_VECTOR4_TARGET_ITERATIONS ?? '2000', 10);
const OUT_ROWS = path.join(REPORTS, 'vector4_targeted_context_nulls_20260531.csv');
const OUT_ITERATIONS = path.join(REPORTS, 'vector4_targeted_context_nulls_20260531_iterations.csv');
const OUT_SUMMARY = path.join(REPORTS, 'vector4_targeted_context_nulls_20260531_summary.json');

const CONTEXT_FIELDS = ['type', 'material', 'symbol', 'cult', 'type_symbol', 'material_type', 'site_type', 'site_type_symbol'];
const TARGETS = [
  {
    target_id: 'context_exact_407_material_copper',
    collapse_mode: 'context_exact',
    unit_kind: 'unigram',
    unit: '407',
    context_field: 'material',
    context_value: 'Copper',
    rationale: 'top V4 copper/TAB:C register lead; tests whether the association survives as material rather than site label',
  },
  {
    target_id: 'context_exact_407_type_tabc',
    collapse_mode: 'context_exact',
    unit_kind: 'unigram',
    unit: '407',
    context_field: 'type',
    context_value: 'TAB:C',
    rationale: 'same 407 family, object-type form',
  },
  {
    target_id: 'context_exact_061845_material_copper',
    collapse_mode: 'context_exact',
    unit_kind: 'bigram',
    unit: '061-845',
    context_field: 'material',
    context_value: 'Copper',
    rationale: 'high-precision TAB:C/Copper bigram nested in the 407 register',
  },
  {
    target_id: 'context_exact_158806_symbol_phyt',
    collapse_mode: 'context_exact',
    unit_kind: 'bigram',
    unit: '158-806',
    context_field: 'symbol',
    context_value: 'Phyt',
    rationale: 'previously tempting iconographic meaning lead; must be killed or revived under fixed-pair nulls',
  },
  {
    target_id: 'context_exact_154806_sealr_none',
    collapse_mode: 'context_exact',
    unit_kind: 'bigram',
    unit: '154-806',
    context_field: 'type_symbol',
    context_value: 'SEAL:R|None',
    rationale: 'repeated Harappa rectangular-seal/no-symbol lead, included as a likely register-control',
  },
  {
    target_id: 'text_only_400_type_tabb',
    collapse_mode: 'text_only',
    unit_kind: 'unigram',
    unit: '400',
    context_field: 'type',
    context_value: 'TAB:B',
    rationale: 'top text-collapsed administrative-tablet lead; likely register, not meaning',
  },
  {
    target_id: 'text_only_407_material_copper',
    collapse_mode: 'text_only',
    unit_kind: 'unigram',
    unit: '407',
    context_field: 'material',
    context_value: 'Copper',
    rationale: 'checks whether the 407/Copper lead survives exact text collapse',
  },
  {
    target_id: 'text_only_158806_symbol_phyt',
    collapse_mode: 'text_only',
    unit_kind: 'bigram',
    unit: '158-806',
    context_field: 'symbol',
    context_value: 'Phyt',
    rationale: 'harsh text-collapsed recheck of the iconographic Phyt lead',
  },
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
  if (cell.length || row.length) row.push(cell.replace(/\r$/, '')), rows.push(row);
  if (!rows.length) return [];
  const header = rows[0];
  return rows.slice(1).filter((r) => r.some((v) => v !== '')).map((r) => {
    const out = {};
    header.forEach((h, i) => { out[h] = r[i] ?? ''; });
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

function parseTokens(text) {
  return [...String(text).matchAll(/\d{3}/g)].map((match) => match[0]);
}

function norm(value) {
  const text = String(value ?? '').trim();
  if (!text || text === '-') return 'NA';
  return text;
}

function contextOf(row) {
  return {
    region: norm(row.region),
    site: norm(row.site),
    type: norm(row.type),
    material: norm(row.material),
    symbol: norm(row.symbol),
    cult: norm(row.cult),
    direction: norm(row.direction),
  };
}

function keyForContext(label) {
  return `${label.field}\t${label.value}`;
}

function contextLabels(ctx) {
  const labels = [];
  const add = (field, value) => {
    if (!value || value === 'NA') return;
    labels.push({ field, value });
  };
  add('type', ctx.type);
  add('material', ctx.material);
  add('symbol', ctx.symbol);
  add('cult', ctx.cult);
  add('type_symbol', `${ctx.type}|${ctx.symbol}`);
  add('material_type', `${ctx.material}|${ctx.type}`);
  add('site_type', `${ctx.site}|${ctx.type}`);
  add('site_type_symbol', `${ctx.site}|${ctx.type}|${ctx.symbol}`);
  return labels;
}

function dedupeLabels(labels) {
  const seen = new Set();
  const out = [];
  for (const label of labels) {
    const key = keyForContext(label);
    if (!seen.has(key)) {
      seen.add(key);
      out.push(label);
    }
  }
  return out;
}

function unitLabels(tokens) {
  const units = [];
  const seen = new Set();
  const add = (kind, unit) => {
    const key = `${kind}\t${unit}`;
    if (!seen.has(key)) {
      seen.add(key);
      units.push({ kind, unit, key });
    }
  };
  tokens.forEach((token) => add('unigram', token));
  for (let i = 0; i < tokens.length - 1; i += 1) add('bigram', `${tokens[i]}-${tokens[i + 1]}`);
  if (tokens.length) {
    add('first', tokens[0]);
    add('last', tokens[tokens.length - 1]);
  }
  return units;
}

function contextSummary(contexts) {
  const summarize = (field) => {
    const values = [...new Set(contexts.map((ctx) => ctx[field]).filter((value) => value && value !== 'NA'))].sort();
    return values.length ? values.join('|') : 'NA';
  };
  return Object.fromEntries(['region', 'site', 'type', 'material', 'symbol', 'cult', 'direction'].map((field) => [field, summarize(field)]));
}

function exactContextCollapse(rows) {
  const groups = new Map();
  for (const row of rows) {
    const tokens = parseTokens(row.text);
    if (!tokens.length) continue;
    const ctx = contextOf(row);
    const key = [row.text, ctx.site, ctx.type, ctx.material, ctx.symbol, ctx.cult].join('\t');
    if (!groups.has(key)) {
      groups.set(key, {
        id: row.id,
        cisis: new Set(),
        source_ids: [],
        text: row.text,
        tokens,
        token_count: tokens.length,
        context: ctx,
        duplicate_weight: 0,
      });
    }
    const current = groups.get(key);
    current.cisis.add(row.cisi);
    current.source_ids.push(row.id);
    current.duplicate_weight += 1;
  }
  return [...groups.values()].map((row) => ({
    ...row,
    cisis: [...row.cisis].filter(Boolean).sort((a, b) => a.localeCompare(b)),
    units: unitLabels(row.tokens),
    labels: contextLabels(row.context),
  }));
}

function textOnlyCollapse(rows) {
  const groups = new Map();
  for (const row of rows) {
    const tokens = parseTokens(row.text);
    if (!tokens.length) continue;
    if (!groups.has(row.text)) {
      groups.set(row.text, {
        id: row.id,
        cisis: new Set(),
        source_ids: [],
        text: row.text,
        tokens,
        token_count: tokens.length,
        contexts: [],
        duplicate_weight: 0,
      });
    }
    const current = groups.get(row.text);
    current.cisis.add(row.cisi);
    current.source_ids.push(row.id);
    current.contexts.push(contextOf(row));
    current.duplicate_weight += 1;
  }
  return [...groups.values()].map((row) => {
    const context = contextSummary(row.contexts);
    return {
      ...row,
      cisis: [...row.cisis].filter(Boolean).sort((a, b) => a.localeCompare(b)),
      context,
      units: unitLabels(row.tokens),
      labels: dedupeLabels(row.contexts.flatMap((ctx) => contextLabels(ctx))),
    };
  });
}

function eligibleRawRows() {
  return parseCsv(fs.readFileSync(INPUT, 'utf8')).filter((row) =>
    row.readiness_bucket === 'lipi_numeric_clean_candidate' &&
    row.complete === 'Y' &&
    row.has_000_unknown === 'false' &&
    row.has_question === 'false' &&
    row.has_bracket === 'false' &&
    row.has_slash === 'false' &&
    row.has_complex_text === 'false'
  );
}

function collapseRows(rows, mode) {
  if (mode === 'context_exact') return exactContextCollapse(rows);
  if (mode === 'text_only') return textOnlyCollapse(rows);
  throw new Error(`Unknown collapse mode ${mode}`);
}

function scorePair(n, support, unitN, labelN) {
  const expected = (unitN * labelN) / n;
  const precision = unitN ? support / unitN : 0;
  const recall = labelN ? support / labelN : 0;
  const lift = expected > 0 ? support / expected : 0;
  const p = n ? labelN / n : 0;
  const finitePopulation = n > 1 ? (n - unitN) / (n - 1) : 1;
  const variance = Math.max(1e-12, unitN * p * (1 - p) * finitePopulation);
  const z = (support - expected) / Math.sqrt(variance);
  return { expected, precision, recall, lift, log2_lift: lift > 0 ? Math.log2(lift) : null, z };
}

function hasUnit(row, target) {
  return row.units.some((unit) => unit.kind === target.unit_kind && unit.unit === target.unit);
}

function hasLabel(row, target) {
  return row.labels.some((label) => label.field === target.context_field && label.value === target.context_value);
}

function targetStats(rows, target) {
  const n = rows.length;
  let unitRows = 0;
  let labelRows = 0;
  let support = 0;
  const examples = [];
  for (const row of rows) {
    const unitHit = hasUnit(row, target);
    const labelHit = hasLabel(row, target);
    if (unitHit) unitRows += 1;
    if (labelHit) labelRows += 1;
    if (unitHit && labelHit) {
      support += 1;
      if (examples.length < 10) examples.push(`${row.cisis.join('|')}:${row.text}`);
    }
  }
  return { n_rows: n, unit_rows: unitRows, label_rows: labelRows, support, ...scorePair(n, support, unitRows, labelRows), examples };
}

function groupIndexes(rows, keyFn) {
  const groups = new Map();
  rows.forEach((row, index) => {
    const key = keyFn(row);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(index);
  });
  return [...groups.values()];
}

function withShuffledContexts(rows, groups, random) {
  const out = rows.map((row) => ({ ...row, context: { ...row.context }, labels: row.labels }));
  for (const indexes of groups) {
    const contexts = shuffle(indexes.map((index) => ({
      context: rows[index].context,
      labels: rows[index].labels,
    })), random);
    indexes.forEach((index, offset) => {
      out[index].context = contexts[offset].context;
      out[index].labels = contexts[offset].labels;
    });
  }
  return out;
}

function withShuffledUnits(rows, groups, random) {
  const out = rows.map((row) => ({ ...row, units: row.units }));
  for (const indexes of groups) {
    const unitSets = shuffle(indexes.map((index) => rows[index].units), random);
    indexes.forEach((index, offset) => {
      out[index].units = unitSets[offset];
    });
  }
  return out;
}

function round(value) {
  return Number.isFinite(value) ? Number(value.toFixed(6)) : value;
}

function summarize(values) {
  const sorted = values.slice().sort((a, b) => a - b);
  const pick = (p) => sorted[Math.min(sorted.length - 1, Math.ceil(sorted.length * p) - 1)] ?? 0;
  return {
    mean: values.reduce((sum, v) => sum + v, 0) / values.length,
    p95: pick(0.95),
    max: sorted[sorted.length - 1] ?? 0,
  };
}

function runNulls(rows, target) {
  const nullDefs = [
    {
      name: 'shuffle_contexts_global',
      make: (random) => withShuffledContexts(rows, [rows.map((_, index) => index)], random),
    },
    {
      name: 'shuffle_contexts_within_site',
      make: (random) => withShuffledContexts(rows, groupIndexes(rows, (row) => row.context.site), random),
    },
    {
      name: 'shuffle_contexts_within_token_count',
      make: (random) => withShuffledContexts(rows, groupIndexes(rows, (row) => row.token_count), random),
    },
    {
      name: 'shuffle_units_within_site_type',
      make: (random) => withShuffledUnits(rows, groupIndexes(rows, (row) => `${row.context.site}\t${row.context.type}`), random),
    },
  ];
  const observed = targetStats(rows, target);
  const iterationRows = [];
  const summaries = [];
  nullDefs.forEach((def, defIndex) => {
    const random = mulberry32(0x4c400 + defIndex * 0x9e3779b1 + target.target_id.length);
    const nullStats = [];
    for (let iteration = 0; iteration < ITERATIONS; iteration += 1) {
      const stats = targetStats(def.make(random), target);
      nullStats.push(stats);
      iterationRows.push({
        target_id: target.target_id,
        collapse_mode: target.collapse_mode,
        null_model: def.name,
        iteration,
        support: stats.support,
        z: round(stats.z),
      });
    }
    const zValues = nullStats.map((row) => row.z);
    const supportValues = nullStats.map((row) => row.support);
    summaries.push({
      null_model: def.name,
      z_ge_observed_share: nullStats.filter((row) => row.z >= observed.z).length / ITERATIONS,
      support_ge_observed_share: nullStats.filter((row) => row.support >= observed.support).length / ITERATIONS,
      null_z: summarize(zValues),
      null_support: summarize(supportValues),
    });
  });
  return { observed, summaries, iterationRows };
}

function main() {
  const raw = eligibleRawRows();
  const rowsByMode = new Map(['context_exact', 'text_only'].map((mode) => [mode, collapseRows(raw, mode)]));
  const targetRows = [];
  const allIterations = [];
  for (const target of TARGETS) {
    const rows = rowsByMode.get(target.collapse_mode);
    const { observed, summaries, iterationRows } = runNulls(rows, target);
    allIterations.push(...iterationRows);
    const worstZ = summaries.slice().sort((a, b) => b.z_ge_observed_share - a.z_ge_observed_share)[0];
    const worstSupport = summaries.slice().sort((a, b) => b.support_ge_observed_share - a.support_ge_observed_share)[0];
    targetRows.push({
      ...target,
      n_rows: observed.n_rows,
      unit_rows: observed.unit_rows,
      label_rows: observed.label_rows,
      support: observed.support,
      expected: round(observed.expected),
      precision: round(observed.precision),
      recall: round(observed.recall),
      lift: round(observed.lift),
      log2_lift: round(observed.log2_lift),
      z: round(observed.z),
      worst_z_ge_observed_share: round(worstZ?.z_ge_observed_share ?? 1),
      worst_z_null_model: worstZ?.null_model ?? '',
      worst_support_ge_observed_share: round(worstSupport?.support_ge_observed_share ?? 1),
      worst_support_null_model: worstSupport?.null_model ?? '',
      claim_eligible: 'no',
      reason_not_claim_eligible: 'target-specific null only; broad family-wise scan, source checks, and exact-text/context-collapse survival remain required',
      example_rows: observed.examples.join(';'),
      null_summaries_json: JSON.stringify(summaries.map((summary) => ({
        null_model: summary.null_model,
        z_ge_observed_share: round(summary.z_ge_observed_share),
        support_ge_observed_share: round(summary.support_ge_observed_share),
        null_z_mean: round(summary.null_z.mean),
        null_z_p95: round(summary.null_z.p95),
        null_z_max: round(summary.null_z.max),
        null_support_mean: round(summary.null_support.mean),
        null_support_p95: round(summary.null_support.p95),
        null_support_max: round(summary.null_support.max),
      }))),
    });
  }

  const rowFields = [
    'target_id', 'collapse_mode', 'unit_kind', 'unit', 'context_field', 'context_value', 'rationale',
    'n_rows', 'unit_rows', 'label_rows', 'support', 'expected', 'precision', 'recall', 'lift', 'log2_lift', 'z',
    'worst_z_ge_observed_share', 'worst_z_null_model', 'worst_support_ge_observed_share', 'worst_support_null_model',
    'claim_eligible', 'reason_not_claim_eligible', 'example_rows', 'null_summaries_json',
  ];
  writeCsv(OUT_ROWS, targetRows, rowFields);
  writeCsv(OUT_ITERATIONS, allIterations, ['target_id', 'collapse_mode', 'null_model', 'iteration', 'support', 'z']);

  const summary = {
    date: RUN_DATE,
    status: 'vector4_targeted_context_nulls_negative_gate',
    input: 'data/open_prototype/reports/lipi_scope_rows.csv',
    iterations_per_null_model: ITERATIONS,
    collapse_modes: Object.fromEntries([...rowsByMode.entries()].map(([mode, rows]) => [mode, rows.length])),
    null_models: ['shuffle_contexts_global', 'shuffle_contexts_within_site', 'shuffle_contexts_within_token_count', 'shuffle_units_within_site_type'],
    interpretation_boundary:
      'This is a fixed-target V4 check for known tempting leads. It is not a family-wise discovery scan and cannot by itself promote sign meaning. A lead with high worst null share is killed; a lead with low target-specific null share only earns a source-check queue.',
    accepted_claim_increment: 0,
    target_count: targetRows.length,
    target_rows: targetRows.map((row) => ({
      target_id: row.target_id,
      unit: `${row.unit_kind}:${row.unit}`,
      context: `${row.context_field}=${row.context_value}`,
      collapse_mode: row.collapse_mode,
      support: row.support,
      z: row.z,
      worst_z_ge_observed_share: row.worst_z_ge_observed_share,
      worst_z_null_model: row.worst_z_null_model,
      decision: row.claim_eligible === 'yes' ? 'queued_only_not_accepted' : 'not_claim_eligible',
      reason: row.reason_not_claim_eligible,
    })),
    files: {
      targets: path.relative(ROOT, OUT_ROWS).replaceAll('\\', '/'),
      iterations: path.relative(ROOT, OUT_ITERATIONS).replaceAll('\\', '/'),
    },
  };
  fs.writeFileSync(OUT_SUMMARY, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
  console.log(JSON.stringify({
    target_count: targetRows.length,
    iterations_per_null_model: ITERATIONS,
    max_worst_z_share: Math.max(...targetRows.map((row) => Number(row.worst_z_ge_observed_share))),
    rows: targetRows.map((row) => ({
      target_id: row.target_id,
      support: row.support,
      z: row.z,
      worst_z_ge_observed_share: row.worst_z_ge_observed_share,
      worst_z_null_model: row.worst_z_null_model,
    })),
  }, null, 2));
}

main();
