// Vector 4 discovery scan: which sign units go with which object contexts?
// A unit is a unigram, bigram, first sign, or last sign of an inscription;
// a context label is a metadata value like type, material, symbol, cult, or
// a combination (type|symbol, site|type, ...). We read the clean lipi scope
// rows (complete, no damage/bracket/slash marks), collapse duplicates by
// exact text plus context — or by text only, when IVC_VECTOR4_COLLAPSE_MODE
// is text_only — and score every unit-context pair by lift and a
// finite-population z, subject to minimum support thresholds (all tunable
// via IVC_VECTOR4_* environment variables). Because the scan tries
// thousands of pairs, significance is family-wise: four null models
// (context shuffles — global, within site, within token count — and a unit
// shuffle within site-type) each run 500 iterations, and every candidate is
// annotated with the worst-case share of null maxima beating its z, overall
// and per context field. Writes candidates, null-iterations, and scope-rows
// CSVs plus a JSON summary; explicitly a candidate screen, not promotion.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const REPORTS = path.join(ROOT, 'data', 'open_prototype', 'reports');
const INPUT = path.join(REPORTS, 'lipi_scope_rows.csv');
const RUN_DATE = '2026-05-29';
const COLLAPSE_MODE = process.env.IVC_VECTOR4_COLLAPSE_MODE ?? 'context_exact';
const OUTPUT_SUFFIX = COLLAPSE_MODE === 'context_exact' ? '' : `_${COLLAPSE_MODE}`;
const OUT_SUMMARY = path.join(REPORTS, `vector4_context_association${OUTPUT_SUFFIX}_summary.json`);
const OUT_CANDIDATES = path.join(REPORTS, `vector4_context_association${OUTPUT_SUFFIX}_candidates.csv`);
const OUT_NULLS = path.join(REPORTS, `vector4_context_association${OUTPUT_SUFFIX}_nulls.csv`);
const OUT_SCOPE = path.join(REPORTS, `vector4_context_association${OUTPUT_SUFFIX}_scope_rows.csv`);

const ITERATIONS = Number.parseInt(process.env.IVC_VECTOR4_CONTEXT_ITERATIONS ?? '500', 10);
const MIN_UNIT_ROWS = Number.parseInt(process.env.IVC_VECTOR4_MIN_UNIT_ROWS ?? '8', 10);
const MIN_LABEL_ROWS = Number.parseInt(process.env.IVC_VECTOR4_MIN_LABEL_ROWS ?? '8', 10);
const MIN_SUPPORT = Number.parseInt(process.env.IVC_VECTOR4_MIN_SUPPORT ?? '5', 10);
const CONTEXT_FIELDS = ['type', 'material', 'symbol', 'cult', 'type_symbol', 'material_type', 'site_type', 'site_type_symbol'];

const CANDIDATE_FIELDS = [
  'rank',
  'scope',
  'unit_kind',
  'unit',
  'context_field',
  'context_value',
  'n_rows',
  'unit_rows',
  'label_rows',
  'support',
  'expected',
  'precision',
  'recall',
  'lift',
  'log2_lift',
  'z',
  'max_null_ge_observed_share',
  'worst_null_model',
  'non_site_max_null_ge_observed_share',
  'non_site_worst_null_model',
  'field_max_null_ge_observed_share',
  'field_worst_null_model',
  'example_cisis',
  'example_texts',
];

const NULL_FIELDS = [
  'scope',
  'null_model',
  'iteration',
  'max_z',
  'max_support',
  'max_unit',
  'max_context_field',
  'max_context_value',
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
    if (!values.length) return 'NA';
    return values.join('|');
  };
  return {
    region: summarize('region'),
    site: summarize('site'),
    type: summarize('type'),
    material: summarize('material'),
    symbol: summarize('symbol'),
    cult: summarize('cult'),
    direction: summarize('direction'),
  };
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
    const key = row.text;
    if (!groups.has(key)) {
      groups.set(key, {
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
    const current = groups.get(key);
    current.cisis.add(row.cisi);
    current.source_ids.push(row.id);
    current.contexts.push(contextOf(row));
    current.duplicate_weight += 1;
  }
  return [...groups.values()].map((row) => {
    const context = contextSummary(row.contexts);
    const labels = dedupeLabels(row.contexts.flatMap((ctx) => contextLabels(ctx)));
    return {
      ...row,
      cisis: [...row.cisis].filter(Boolean).sort((a, b) => a.localeCompare(b)),
      context,
      units: unitLabels(row.tokens),
      labels,
    };
  });
}

function collapseRows(rows) {
  if (COLLAPSE_MODE === 'context_exact') return exactContextCollapse(rows);
  if (COLLAPSE_MODE === 'text_only') return textOnlyCollapse(rows);
  throw new Error(`Unknown IVC_VECTOR4_COLLAPSE_MODE: ${COLLAPSE_MODE}`);
}

function eligibleRows() {
  return collapseRows(parseCsv(fs.readFileSync(INPUT, 'utf8')).filter((row) =>
    row.readiness_bucket === 'lipi_numeric_clean_candidate' &&
    row.complete === 'Y' &&
    row.has_000_unknown === 'false' &&
    row.has_question === 'false' &&
    row.has_bracket === 'false' &&
    row.has_slash === 'false' &&
    row.has_complex_text === 'false'
  ));
}

function keyForContext(label) {
  return `${label.field}\t${label.value}`;
}

function buildStats(rows) {
  const n = rows.length;
  const unitRows = new Map();
  const labelRows = new Map();
  const pairRows = new Map();
  const examples = new Map();

  rows.forEach((row, rowIndex) => {
    for (const unit of row.units) {
      const unitKey = unit.key;
      if (!unitRows.has(unitKey)) unitRows.set(unitKey, { ...unit, rows: 0 });
      unitRows.get(unitKey).rows += 1;
      for (const label of row.labels) {
        const labelKey = keyForContext(label);
        if (!labelRows.has(labelKey)) labelRows.set(labelKey, { ...label, rows: 0 });
        const pairKey = `${unitKey}\t${labelKey}`;
        pairRows.set(pairKey, (pairRows.get(pairKey) ?? 0) + 1);
        if (!examples.has(pairKey)) examples.set(pairKey, []);
        if (examples.get(pairKey).length < 8) {
          examples.get(pairKey).push({ cisi: row.cisis.join('|'), text: row.text, rowIndex });
        }
      }
    }
    for (const label of row.labels) {
      const labelKey = keyForContext(label);
      if (!labelRows.has(labelKey)) labelRows.set(labelKey, { ...label, rows: 0 });
      labelRows.get(labelKey).rows += 1;
    }
  });

  return { n, unitRows, labelRows, pairRows, examples };
}

function scorePair(n, support, unitN, labelN) {
  const expected = (unitN * labelN) / n;
  if (support < MIN_SUPPORT || unitN < MIN_UNIT_ROWS || labelN < MIN_LABEL_ROWS || expected <= 0) return null;
  const precision = support / unitN;
  const recall = support / labelN;
  const lift = support / expected;
  const p = labelN / n;
  const finitePopulation = n > 1 ? (n - unitN) / (n - 1) : 1;
  const variance = Math.max(1e-12, unitN * p * (1 - p) * finitePopulation);
  const z = (support - expected) / Math.sqrt(variance);
  return {
    expected,
    precision,
    recall,
    lift,
    log2_lift: Math.log2(lift),
    z,
  };
}

function scoredAssociations(rows) {
  const stats = buildStats(rows);
  const out = [];
  for (const [pairKey, support] of stats.pairRows.entries()) {
    const [unitKind, unit, contextField, contextValue] = pairKey.split('\t');
    const unitKey = `${unitKind}\t${unit}`;
    const labelKey = `${contextField}\t${contextValue}`;
    const unitMeta = stats.unitRows.get(unitKey);
    const labelMeta = stats.labelRows.get(labelKey);
    const score = scorePair(stats.n, support, unitMeta?.rows ?? 0, labelMeta?.rows ?? 0);
    if (!score || score.z <= 0 || score.lift <= 1) continue;
    const exampleRows = stats.examples.get(pairKey) ?? [];
    out.push({
      scope: COLLAPSE_MODE,
      unit_kind: unitKind,
      unit,
      context_field: contextField,
      context_value: contextValue,
      n_rows: stats.n,
      unit_rows: unitMeta.rows,
      label_rows: labelMeta.rows,
      support,
      ...score,
      example_cisis: exampleRows.map((row) => row.cisi).join(';'),
      example_texts: exampleRows.map((row) => row.text).join(';'),
    });
  }
  return out.sort((a, b) =>
    b.z - a.z ||
    b.support - a.support ||
    b.log2_lift - a.log2_lift ||
    `${a.unit_kind}:${a.unit}`.localeCompare(`${b.unit_kind}:${b.unit}`)
  );
}

function topAssociations(rows, limit = 200) {
  return scoredAssociations(rows).slice(0, limit);
}

function emptyMax() {
  return {
    z: 0,
    support: 0,
    unit: '',
    unit_kind: '',
    context_field: '',
    context_value: '',
  };
}

function maxAssociation(rows) {
  const top = topAssociations(rows, 1)[0];
  return top ?? emptyMax();
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
  const out = rows.map((row) => ({ ...row, context: { ...row.context } }));
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

function runNulls(rows, observedTop) {
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

  const iterations = [];
  const summaries = [];
  const maxByModel = [];
  const nonSiteMaxByModel = [];
  const fieldMaxByModel = [];
  nullDefs.forEach((def, defIndex) => {
    const random = mulberry32(0x1c400 + defIndex * 0x9e3779b1);
    const maxRows = [];
    const nonSiteMaxRows = [];
    const fieldMaxRows = Object.fromEntries(CONTEXT_FIELDS.map((field) => [field, []]));
    for (let iteration = 0; iteration < ITERATIONS; iteration += 1) {
      const associations = scoredAssociations(def.make(random));
      const max = associations[0] ?? emptyMax();
      const nonSiteMax = associations.find((candidate) => !candidate.context_field.startsWith('site')) ?? emptyMax();
      const byField = Object.fromEntries(CONTEXT_FIELDS.map((field) => [field, emptyMax()]));
      for (const candidate of associations) {
        if (byField[candidate.context_field].z === 0) byField[candidate.context_field] = candidate;
      }
      const row = {
        scope: COLLAPSE_MODE,
        null_model: def.name,
        iteration,
        max_z: max.z,
        max_support: max.support,
        max_unit: `${max.unit_kind}:${max.unit}`,
        max_context_field: max.context_field,
        max_context_value: max.context_value,
      };
      iterations.push(row);
      maxRows.push(row);
      nonSiteMaxRows.push(nonSiteMax);
      for (const field of CONTEXT_FIELDS) fieldMaxRows[field].push(byField[field]);
    }
    const maxZValues = maxRows.map((row) => row.max_z).sort((a, b) => a - b);
    const nonSiteMaxZValues = nonSiteMaxRows.map((row) => row.z).sort((a, b) => a - b);
    const fieldMaxZValues = Object.fromEntries(CONTEXT_FIELDS.map((field) => [
      field,
      fieldMaxRows[field].map((row) => row.z).sort((a, b) => a - b),
    ]));
    maxByModel.push({ null_model: def.name, max_z_values: maxZValues });
    nonSiteMaxByModel.push({ null_model: def.name, max_z_values: nonSiteMaxZValues });
    fieldMaxByModel.push({ null_model: def.name, by_field: fieldMaxZValues });
    summaries.push({
      null_model: def.name,
      iterations: ITERATIONS,
      max_z_mean: maxRows.reduce((sum, row) => sum + row.max_z, 0) / ITERATIONS,
      max_z_p95: maxZValues[Math.min(maxZValues.length - 1, Math.ceil(ITERATIONS * 0.95) - 1)],
      max_z_max: Math.max(...maxRows.map((row) => row.max_z)),
      non_site_max_z_mean: nonSiteMaxRows.reduce((sum, row) => sum + row.z, 0) / ITERATIONS,
      non_site_max_z_p95: nonSiteMaxZValues[Math.min(nonSiteMaxZValues.length - 1, Math.ceil(ITERATIONS * 0.95) - 1)],
      non_site_max_z_max: Math.max(...nonSiteMaxRows.map((row) => row.z)),
      field_max_z: Object.fromEntries(CONTEXT_FIELDS.map((field) => [
        field,
        {
          p95: fieldMaxZValues[field][Math.min(fieldMaxZValues[field].length - 1, Math.ceil(ITERATIONS * 0.95) - 1)],
          max: Math.max(...fieldMaxRows[field].map((row) => row.z)),
        },
      ])),
      top20_familywise_ge_observed_shares: observedTop.slice(0, 20).map((candidate) => ({
        unit: `${candidate.unit_kind}:${candidate.unit}`,
        context: `${candidate.context_field}=${candidate.context_value}`,
        observed_z: candidate.z,
        null_ge_observed_share: maxZValues.filter((z) => z >= candidate.z).length / ITERATIONS,
      })),
    });
  });

  return { iterations, summaries, maxByModel, nonSiteMaxByModel, fieldMaxByModel };
}

function round(value) {
  return Number.isFinite(value) ? Number(value.toFixed(6)) : value;
}

function worstShare(models, candidate, valuesForModel) {
  const shares = models.map((model) => ({
    null_model: model.null_model,
    share: valuesForModel(model, candidate).filter((z) => z >= candidate.z).length / ITERATIONS,
  }));
  return shares.sort((a, b) => b.share - a.share)[0];
}

function main() {
  const rows = eligibleRows();
  const observed = topAssociations(rows, 200);
  const { iterations, summaries, maxByModel, nonSiteMaxByModel, fieldMaxByModel } = runNulls(rows, observed);

  const annotated = observed.map((candidate, index) => {
    const worst = worstShare(maxByModel, candidate, (model) => model.max_z_values);
    const nonSiteWorst = worstShare(nonSiteMaxByModel, candidate, (model) => model.max_z_values);
    const fieldWorst = worstShare(fieldMaxByModel, candidate, (model) => model.by_field[candidate.context_field] ?? []);
    return {
      rank: index + 1,
      ...candidate,
      expected: round(candidate.expected),
      precision: round(candidate.precision),
      recall: round(candidate.recall),
      lift: round(candidate.lift),
      log2_lift: round(candidate.log2_lift),
      z: round(candidate.z),
      max_null_ge_observed_share: worst ? round(worst.share) : '',
      worst_null_model: worst?.null_model ?? '',
      non_site_max_null_ge_observed_share: !candidate.context_field.startsWith('site') && nonSiteWorst ? round(nonSiteWorst.share) : '',
      non_site_worst_null_model: !candidate.context_field.startsWith('site') ? nonSiteWorst?.null_model ?? '' : '',
      field_max_null_ge_observed_share: fieldWorst ? round(fieldWorst.share) : '',
      field_worst_null_model: fieldWorst?.null_model ?? '',
    };
  });

  const scopeRows = rows.map((row) => ({
    id: row.id,
    cisis: row.cisis.join('|'),
    text: row.text,
    token_count: row.token_count,
    duplicate_weight: row.duplicate_weight,
    site: row.context.site,
    type: row.context.type,
    material: row.context.material,
    symbol: row.context.symbol,
    cult: row.context.cult,
  }));

  writeCsv(OUT_CANDIDATES, annotated, CANDIDATE_FIELDS);
  writeCsv(OUT_NULLS, iterations.map((row) => ({
    ...row,
    max_z: round(row.max_z),
  })), NULL_FIELDS);
  writeCsv(OUT_SCOPE, scopeRows, ['id', 'cisis', 'text', 'token_count', 'duplicate_weight', 'site', 'type', 'material', 'symbol', 'cult']);

  const summary = {
    date: RUN_DATE,
    status: 'vector4_context_association_scan_candidate_only',
    input: 'data/open_prototype/reports/lipi_scope_rows.csv',
    scope: {
      name: COLLAPSE_MODE,
      rows: rows.length,
      collapse_key: COLLAPSE_MODE === 'context_exact'
        ? 'text + site + type + material + symbol + cult'
        : 'text only; context labels retained as a per-text union',
      readiness: 'lipi_numeric_clean_candidate, complete=Y, no 000/question/bracket/slash/complex text',
      min_unit_rows: MIN_UNIT_ROWS,
      min_label_rows: MIN_LABEL_ROWS,
      min_support: MIN_SUPPORT,
    },
    unit_families: ['unigram', 'bigram', 'first', 'last'],
    context_fields: CONTEXT_FIELDS,
    iterations_per_null_model: ITERATIONS,
    null_policy:
      'max_null_ge_observed_share is whole-scan family-wise. non_site_max_null_ge_observed_share is family-wise over non-site context fields. field_max_null_ge_observed_share is family-wise inside the candidate context field. Each reports the worst share across null models.',
    null_summaries: summaries,
    top_candidates: annotated.slice(0, 20),
    top_non_site_candidates: annotated.filter((candidate) => !candidate.context_field.startsWith('site')).slice(0, 20),
    top_familywise_survivors: annotated.filter((candidate) => Number(candidate.max_null_ge_observed_share) <= 0.05).slice(0, 20),
    top_non_site_familywise_survivors: annotated
      .filter((candidate) => !candidate.context_field.startsWith('site') && Number(candidate.max_null_ge_observed_share) <= 0.05)
      .slice(0, 20),
    interpretation_boundary:
      'This is a broad Vector 4 discovery scan for sign/context associations. It does not assign sign meanings, sounds, language family, or translations. Candidates require source checks and focused matched controls before ledger promotion.',
    files: {
      candidates: path.relative(ROOT, OUT_CANDIDATES).replaceAll('\\', '/'),
      nulls: path.relative(ROOT, OUT_NULLS).replaceAll('\\', '/'),
      scope_rows: path.relative(ROOT, OUT_SCOPE).replaceAll('\\', '/'),
    },
  };
  fs.writeFileSync(OUT_SUMMARY, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
  console.log(JSON.stringify({
    rows: rows.length,
    iterations_per_null_model: ITERATIONS,
    top_candidate: annotated[0],
    top_candidate_max_null_ge_observed_share: annotated[0]?.max_null_ge_observed_share,
  }, null, 2));
}

main();
