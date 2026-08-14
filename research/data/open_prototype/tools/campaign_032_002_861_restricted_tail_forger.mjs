// Forger for the "restricted tail" claim about the pair 533-717: in strict rows it occurs
// only as a terminal tail right after the fixed prefix 002-861. A forger asks how easily
// chance produces a pattern that strong. We load only strictly-parseable inscriptions from
// lipi/metadata_filtered.csv (text of the form +NNN-NNN-...+ with no damage brackets), in
// two scopes — raw rows, and rows deduplicated on exact text + site + type + symbol — and
// find every unit of length 1 to 3 that occurs at least twice with every occurrence in the
// fixed-prefix terminal context. Four seeded null models then re-run that search: shuffling
// the context labels globally or within site/type/symbol groups (default 10,000 iterations),
// and shuffling tokens globally or within each row (default 500). CLI flags
// --context-iterations, --token-iterations, and --seed override the defaults. A separate
// "any prefix" skeptic pass shows that prefix-restricted terminal bigrams are common in
// general, which bounds what the result may claim, and earlier source-check reports are
// folded in as supporting evidence. Outputs candidate, null-summary, and null-iteration CSVs
// plus a JSON summary (with allowed and forbidden wording) in data/open_prototype/reports.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const REPORTS = path.join(ROOT, 'data', 'open_prototype', 'reports');
const METADATA = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const SOURCE_VERDICTS = path.join(REPORTS, 'campaign_032_002_861_source_token_attachment_verdicts.csv');
const FAMILY_INDEPENDENCE = path.join(REPORTS, 'campaign_032_002_861_533717_source_family_independence_summary.json');
const LAYOUT_DISCRIMINATOR = path.join(REPORTS, 'campaign_032_002_861_533717_source_layout_discriminator_summary.json');

const OUT_SUMMARY = path.join(REPORTS, 'campaign_032_002_861_restricted_tail_forger_summary.json');
const OUT_CANDIDATES = path.join(REPORTS, 'campaign_032_002_861_restricted_tail_forger_candidates.csv');
const OUT_NULL_SUMMARY = path.join(REPORTS, 'campaign_032_002_861_restricted_tail_forger_null_summary.csv');
const OUT_NULL_ITERATIONS = path.join(REPORTS, 'campaign_032_002_861_restricted_tail_forger_null_iterations.csv');

const RUN_DATE = '2026-05-29';
const FIXED_PREFIX = ['002', '861'];
const TARGET_UNIT = '533 717';
const UNIT_LENGTHS = [1, 2, 3];
const MIN_SUPPORT = 2;

const args = Object.fromEntries(
  process.argv.slice(2).map((arg) => {
    const match = arg.match(/^--([^=]+)=(.*)$/);
    return match ? [match[1], match[2]] : [arg, 'true'];
  }),
);

const CONTEXT_ITERATIONS = Number.parseInt(args['context-iterations'] ?? args.iterations ?? '10000', 10);
const TOKEN_ITERATIONS = Number.parseInt(args['token-iterations'] ?? '500', 10);
const SEED = Number.parseInt(args.seed ?? '20260529', 10);

const CANDIDATE_FIELDS = [
  'scope',
  'unit_len',
  'unit',
  'total_occurrences',
  'fixed_prefix_terminal_occurrences',
  'all_occurrences_in_fixed_prefix_terminal_context',
  'examples',
];

const NULL_FIELDS = [
  'scope',
  'null_model',
  'iterations',
  'observed_max_support',
  'observed_candidate_count',
  'null_mean_max_support',
  'null_p95_max_support',
  'null_max_support',
  'fpr_max_ge_observed',
  'null_mean_candidate_count',
  'null_p95_candidate_count',
  'null_max_candidate_count',
  'fpr_candidate_count_ge_observed',
];

const ITERATION_FIELDS = [
  'scope',
  'null_model',
  'iteration',
  'max_support',
  'candidate_count',
  'target_support',
  'target_is_candidate',
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
  let a = seed >>> 0;
  return () => {
    a += 0x6d2b79f5;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffleInPlace(values, rng) {
  for (let i = values.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rng() * (i + 1));
    [values[i], values[j]] = [values[j], values[i]];
  }
  return values;
}

function quantile(values, q) {
  if (!values.length) return null;
  const sorted = values.slice().sort((a, b) => a - b);
  const idx = Math.min(sorted.length - 1, Math.ceil(q * sorted.length) - 1);
  return sorted[idx];
}

function parseTokens(text) {
  if (!text?.startsWith('+') || !text.endsWith('+')) return null;
  if (/[\[\]()]/.test(text)) return null;
  const tokens = text.slice(1, -1).split('-').filter(Boolean);
  if (!tokens.length || !tokens.every((token) => /^\d{3}$/.test(token))) return null;
  return tokens;
}

function norm(value) {
  const text = String(value ?? '').trim();
  return text && text !== '-' ? text : 'NA';
}

function loadStrictRows({ dedupe = false } = {}) {
  const seen = new Set();
  const out = [];
  for (const row of parseCsv(fs.readFileSync(METADATA, 'utf8'))) {
    const tokens = parseTokens(row.text);
    if (!tokens) continue;
    const dedupeKey = [row.text, row.site, row.type, row.symbol].map(norm).join('\u241f');
    if (dedupe) {
      if (seen.has(dedupeKey)) continue;
      seen.add(dedupeKey);
    }
    out.push({
      id: row.id,
      cisi: norm(row.cisi),
      site: norm(row.site),
      type: norm(row.type),
      symbol: norm(row.symbol),
      shape: norm(row.shape),
      material: norm(row.material),
      direction: norm(row['dir.']),
      text: row.text,
      tokens,
    });
  }
  return out;
}

function fixedPrefixContext(tokens, start, unitLen) {
  const prefixStart = start - FIXED_PREFIX.length;
  if (prefixStart < 0) return false;
  const prefix = tokens.slice(prefixStart, start);
  const next = tokens[start + unitLen] ?? '<END>';
  return prefix.length === FIXED_PREFIX.length &&
    prefix.every((token, idx) => token === FIXED_PREFIX[idx]) &&
    next === '<END>';
}

function ngramOccurrences(rows, unitLen) {
  const out = [];
  for (const row of rows) {
    const { tokens } = row;
    for (let i = 0; i <= tokens.length - unitLen; i += 1) {
      const unit = tokens.slice(i, i + unitLen).join(' ');
      out.push({
        unit_len: unitLen,
        unit,
        context: fixedPrefixContext(tokens, i, unitLen),
        group_site_type_symbol: [row.site, row.type, row.symbol].join('|'),
        example: `${row.cisi} ${row.text}`,
      });
    }
  }
  return out;
}

function scoreOccurrences(occurrences, labels = null) {
  const stats = new Map();
  for (let i = 0; i < occurrences.length; i += 1) {
    const occ = occurrences[i];
    const context = labels ? labels[i] : occ.context;
    const current = stats.get(occ.unit) ?? {
      unit_len: occ.unit_len,
      unit: occ.unit,
      total: 0,
      fixed_prefix_terminal: 0,
      examples: [],
    };
    current.total += 1;
    if (context) {
      current.fixed_prefix_terminal += 1;
      if (current.examples.length < 5) current.examples.push(occ.example);
    }
    stats.set(occ.unit, current);
  }
  const candidates = [...stats.values()]
    .filter((row) => row.total >= MIN_SUPPORT && row.total === row.fixed_prefix_terminal)
    .sort((a, b) => b.total - a.total || a.unit.localeCompare(b.unit));
  const target = stats.get(TARGET_UNIT);
  return {
    max_support: candidates[0]?.total ?? 0,
    candidate_count: candidates.length,
    target_support: target?.fixed_prefix_terminal ?? 0,
    target_is_candidate: Boolean(target && target.total >= MIN_SUPPORT && target.total === target.fixed_prefix_terminal),
    candidates,
  };
}

function scoreAllLengths(rows) {
  const byLength = {};
  let maxSupport = 0;
  let candidateCount = 0;
  let targetSupport = 0;
  let targetIsCandidate = false;
  const candidates = [];
  for (const unitLen of UNIT_LENGTHS) {
    const score = scoreOccurrences(ngramOccurrences(rows, unitLen));
    byLength[unitLen] = score;
    maxSupport = Math.max(maxSupport, score.max_support);
    candidateCount += score.candidate_count;
    if (unitLen === 2) {
      targetSupport = score.target_support;
      targetIsCandidate = score.target_is_candidate;
    }
    candidates.push(...score.candidates);
  }
  return { max_support: maxSupport, candidate_count: candidateCount, target_support: targetSupport, target_is_candidate: targetIsCandidate, byLength, candidates };
}

function anyPrefixRestrictedTerminalBigrams(rows) {
  const byUnit = new Map();
  for (const row of rows) {
    const { tokens } = row;
    for (let i = 0; i <= tokens.length - 2; i += 1) {
      const unit = tokens.slice(i, i + 2).join(' ');
      const prefix = i >= 2 ? tokens.slice(i - 2, i).join(' ') : (i === 1 ? `<START> ${tokens[0]}` : '<START>');
      const terminal = (tokens[i + 2] ?? '<END>') === '<END>';
      const current = byUnit.get(unit) ?? { unit, total: 0, prefixes: new Map() };
      current.total += 1;
      const prefixStats = current.prefixes.get(prefix) ?? { prefix, count: 0, terminal_count: 0, examples: [] };
      prefixStats.count += 1;
      if (terminal) prefixStats.terminal_count += 1;
      if (prefixStats.examples.length < 3) prefixStats.examples.push(`${row.cisi} ${row.text}`);
      current.prefixes.set(prefix, prefixStats);
      byUnit.set(unit, current);
    }
  }
  const out = [];
  for (const unitStats of byUnit.values()) {
    if (unitStats.total < MIN_SUPPORT) continue;
    for (const prefixStats of unitStats.prefixes.values()) {
      if (prefixStats.count === unitStats.total && prefixStats.terminal_count === unitStats.total) {
        out.push({
          prefix: prefixStats.prefix,
          unit: unitStats.unit,
          support: unitStats.total,
          examples: prefixStats.examples,
        });
      }
    }
  }
  return out.sort((a, b) => b.support - a.support || a.prefix.localeCompare(b.prefix) || a.unit.localeCompare(b.unit));
}

function groupIndexes(occurrences, groupField) {
  const groups = new Map();
  occurrences.forEach((occ, idx) => {
    const key = occ[groupField];
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(idx);
  });
  return groups;
}

function shuffledContextLabels(occurrences, rng, groupField = null) {
  const labels = new Array(occurrences.length);
  if (!groupField) {
    const shuffled = shuffleInPlace(occurrences.map((occ) => occ.context), rng);
    shuffled.forEach((value, idx) => {
      labels[idx] = value;
    });
    return labels;
  }
  for (const indexes of groupIndexes(occurrences, groupField).values()) {
    const shuffled = shuffleInPlace(indexes.map((idx) => occurrences[idx].context), rng);
    indexes.forEach((idx, localIdx) => {
      labels[idx] = shuffled[localIdx];
    });
  }
  return labels;
}

function buildContextPlans(rows) {
  return UNIT_LENGTHS.map((unitLen) => {
    const occurrences = ngramOccurrences(rows, unitLen);
    return {
      unitLen,
      occurrences,
      groups: groupIndexes(occurrences, 'group_site_type_symbol'),
    };
  });
}

function shuffledContextLabelsFromPlan(plan, rng, grouped) {
  const { occurrences } = plan;
  const labels = new Array(occurrences.length);
  if (!grouped) {
    const shuffled = shuffleInPlace(occurrences.map((occ) => occ.context), rng);
    shuffled.forEach((value, idx) => {
      labels[idx] = value;
    });
    return labels;
  }
  for (const indexes of plan.groups.values()) {
    const shuffled = shuffleInPlace(indexes.map((idx) => occurrences[idx].context), rng);
    indexes.forEach((idx, localIdx) => {
      labels[idx] = shuffled[localIdx];
    });
  }
  return labels;
}

function contextShuffleScore(contextPlans, rng, grouped) {
  let maxSupport = 0;
  let candidateCount = 0;
  let targetSupport = 0;
  let targetIsCandidate = false;
  for (const plan of contextPlans) {
    const labels = shuffledContextLabelsFromPlan(plan, rng, grouped);
    const score = scoreOccurrences(plan.occurrences, labels);
    maxSupport = Math.max(maxSupport, score.max_support);
    candidateCount += score.candidate_count;
    if (plan.unitLen === 2) {
      targetSupport = score.target_support;
      targetIsCandidate = score.target_is_candidate;
    }
  }
  return { max_support: maxSupport, candidate_count: candidateCount, target_support: targetSupport, target_is_candidate: targetIsCandidate };
}

function shuffledRows(rows, rng, mode) {
  if (mode === 'global') {
    const allTokens = rows.flatMap((row) => row.tokens);
    shuffleInPlace(allTokens, rng);
    let cursor = 0;
    return rows.map((row) => {
      const tokens = allTokens.slice(cursor, cursor + row.tokens.length);
      cursor += row.tokens.length;
      return { ...row, tokens, text: `+${tokens.join('-')}+` };
    });
  }
  if (mode === 'within_row') {
    return rows.map((row) => {
      const tokens = shuffleInPlace(row.tokens.slice(), rng);
      return { ...row, tokens, text: `+${tokens.join('-')}+` };
    });
  }
  throw new Error(`Unknown token shuffle mode: ${mode}`);
}

function summarizeIterations(scope, nullModel, observed, iterations) {
  const maxValues = iterations.map((row) => row.max_support);
  const candidateCounts = iterations.map((row) => row.candidate_count);
  return {
    scope,
    null_model: nullModel,
    iterations: iterations.length,
    observed_max_support: observed.max_support,
    observed_candidate_count: observed.candidate_count,
    null_mean_max_support: maxValues.reduce((sum, value) => sum + value, 0) / maxValues.length,
    null_p95_max_support: quantile(maxValues, 0.95),
    null_max_support: Math.max(...maxValues),
    fpr_max_ge_observed: maxValues.filter((value) => value >= observed.max_support).length / maxValues.length,
    null_mean_candidate_count: candidateCounts.reduce((sum, value) => sum + value, 0) / candidateCounts.length,
    null_p95_candidate_count: quantile(candidateCounts, 0.95),
    null_max_candidate_count: Math.max(...candidateCounts),
    fpr_candidate_count_ge_observed: candidateCounts.filter((value) => value >= observed.candidate_count).length / candidateCounts.length,
  };
}

function runNulls(scope, rows, observed) {
  const iterationRows = [];
  const summaryRows = [];
  const contextPlans = buildContextPlans(rows);
  const specs = [
    {
      model: 'context_shuffle_global_any_n_1_3',
      iterations: CONTEXT_ITERATIONS,
      scorer: (rng) => contextShuffleScore(contextPlans, rng, false),
    },
    {
      model: 'context_shuffle_site_type_symbol_any_n_1_3',
      iterations: CONTEXT_ITERATIONS,
      scorer: (rng) => contextShuffleScore(contextPlans, rng, true),
    },
    {
      model: 'token_shuffle_global_preserve_lengths_any_n_1_3',
      iterations: TOKEN_ITERATIONS,
      scorer: (rng) => scoreAllLengths(shuffledRows(rows, rng, 'global')),
    },
    {
      model: 'token_shuffle_within_row_any_n_1_3',
      iterations: TOKEN_ITERATIONS,
      scorer: (rng) => scoreAllLengths(shuffledRows(rows, rng, 'within_row')),
    },
  ];

  specs.forEach((spec, specIndex) => {
    const localRows = [];
    for (let iteration = 0; iteration < spec.iterations; iteration += 1) {
      const rng = mulberry32(SEED + specIndex * 1000003 + iteration);
      const score = spec.scorer(rng);
      const row = {
        scope,
        null_model: spec.model,
        iteration,
        max_support: score.max_support,
        candidate_count: score.candidate_count,
        target_support: score.target_support,
        target_is_candidate: String(score.target_is_candidate),
      };
      localRows.push(row);
      iterationRows.push(row);
    }
    summaryRows.push(summarizeIterations(scope, spec.model, observed, localRows));
  });
  return { iterationRows, summaryRows };
}

function readJsonIfExists(file) {
  if (!fs.existsSync(file)) return null;
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function loadSourceSupport() {
  const verdictRows = fs.existsSync(SOURCE_VERDICTS)
    ? parseCsv(fs.readFileSync(SOURCE_VERDICTS, 'utf8')).filter((row) => row.tail_family === '533-717')
    : [];
  const family = readJsonIfExists(FAMILY_INDEPENDENCE);
  const layout = readJsonIfExists(LAYOUT_DISCRIMINATOR);
  return {
    source_visible_533_717_rows: verdictRows.map((row) => ({
      cisi: row.cisi,
      id: row.object_id,
      side: row.witness,
      text: row.text,
      source_route: row.source_route,
      source_image: row.source_image_abs,
      source_image_sha256: row.source_sha256,
      overlay: row.overlay_abs,
      source_quality: row.source_quality,
      confidence: row.confidence,
      verdict: row.attachment_verdict,
      observation: row.observation,
      limit: row.limit,
    })),
    source_family_independence_decision: family?.decision ?? null,
    source_family_independence_basis: family?.target_compare?.verdict_basis ?? [],
    source_layout_discriminator_decision: layout?.decision ?? null,
    source_layout_discriminator_basis: layout?.decision_basis ?? [],
  };
}

function main() {
  const scopes = [
    { name: 'strict_raw_rows', rows: loadStrictRows({ dedupe: false }) },
    { name: 'strict_exact_text_site_type_symbol_dedup', rows: loadStrictRows({ dedupe: true }) },
  ];

  const candidateRows = [];
  const nullIterationRows = [];
  const nullSummaryRows = [];
  const scopeSummaries = {};
  const anyPrefixSkeptic = {};

  for (const scope of scopes) {
    const observed = scoreAllLengths(scope.rows);
    const anyPrefixCandidates = anyPrefixRestrictedTerminalBigrams(scope.rows);
    anyPrefixSkeptic[scope.name] = {
      candidate_count: anyPrefixCandidates.length,
      top_candidates: anyPrefixCandidates.slice(0, 20),
      interpretation: 'This is the hostile broad-posthoc warning: repeated terminal bigrams restricted to some prefix are common. The admissible 533-717 result is therefore bounded to the fixed 002-861 branch question established before this test.',
    };
    scopeSummaries[scope.name] = {
      rows: scope.rows.length,
      observed_max_support_any_n_1_3: observed.max_support,
      observed_candidate_count_any_n_1_3: observed.candidate_count,
      target_unit: TARGET_UNIT,
      target_unit_support_in_fixed_prefix_terminal_context: observed.target_support,
      target_unit_is_candidate: observed.target_is_candidate,
      observed_by_unit_length: Object.fromEntries(
        UNIT_LENGTHS.map((unitLen) => [
          unitLen,
          {
            max_support: observed.byLength[unitLen].max_support,
            candidate_count: observed.byLength[unitLen].candidate_count,
            candidates: observed.byLength[unitLen].candidates.map((row) => ({
              unit: row.unit,
              total_occurrences: row.total,
              fixed_prefix_terminal_occurrences: row.fixed_prefix_terminal,
              examples: row.examples,
            })),
          },
        ]),
      ),
    };
    for (const candidate of observed.candidates) {
      candidateRows.push({
        scope: scope.name,
        unit_len: candidate.unit_len,
        unit: candidate.unit,
        total_occurrences: candidate.total,
        fixed_prefix_terminal_occurrences: candidate.fixed_prefix_terminal,
        all_occurrences_in_fixed_prefix_terminal_context: String(candidate.total === candidate.fixed_prefix_terminal),
        examples: candidate.examples.join(';'),
      });
    }

    const nulls = runNulls(scope.name, scope.rows, observed);
    nullIterationRows.push(...nulls.iterationRows);
    nullSummaryRows.push(...nulls.summaryRows);
  }

  writeCsv(OUT_CANDIDATES, candidateRows, CANDIDATE_FIELDS);
  writeCsv(OUT_NULL_SUMMARY, nullSummaryRows, NULL_FIELDS);
  writeCsv(OUT_NULL_ITERATIONS, nullIterationRows, ITERATION_FIELDS);

  const worstFpr = Math.max(...nullSummaryRows.map((row) => row.fpr_max_ge_observed));
  const strictRawContextFpr = nullSummaryRows
    .filter((row) => row.scope === 'strict_raw_rows' && row.null_model.startsWith('context_shuffle'))
    .reduce((max, row) => Math.max(max, row.fpr_max_ge_observed), 0);

  const payload = {
    date: RUN_DATE,
    seed: SEED,
    context_iterations: CONTEXT_ITERATIONS,
    token_iterations: TOKEN_ITERATIONS,
    fixed_prefix: FIXED_PREFIX.join(' '),
    target_unit: TARGET_UNIT,
    unit_lengths_tested: UNIT_LENGTHS,
    min_support: MIN_SUPPORT,
    purpose: 'Forger for the 002-861 restricted-tail candidate: let nulls discover any unit of length 1..3 that occurs at least twice and only as a terminal tail after fixed prefix 002-861.',
    scopes: scopeSummaries,
    null_summary: nullSummaryRows,
    worst_fpr_max_support_ge_observed: worstFpr,
    strict_raw_context_shuffle_worst_fpr: strictRawContextFpr,
    source_support: loadSourceSupport(),
    broad_posthoc_prefix_skeptic: anyPrefixSkeptic,
    decision: worstFpr <= 0.01
      ? 'low_fpr_fixed_prefix_structural_finding_semantics_not_earned'
      : 'restricted_tail_pattern_not_promotable_under_forger',
    allowed_wording: 'In strict local rows, the two-token unit 533-717 is the only length-1-to-3 unit with support >=2 whose every occurrence is a terminal tail after the fixed prefix 002-861; the two witnesses are M-376 and M-391, both source-visible as same-line terminal-side material and not collapsed as exact copy-family duplicates.',
    forbidden_wording: 'Do not claim a value, phonetic reading, language identification, translation, semantic class, exact source-normalized 861/533/717 token boundary, or that 533-717 is globally unique outside the fixed 002-861 branch question.',
    outputs: {
      candidates_csv: OUT_CANDIDATES,
      null_summary_csv: OUT_NULL_SUMMARY,
      null_iterations_csv: OUT_NULL_ITERATIONS,
    },
  };
  fs.writeFileSync(OUT_SUMMARY, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
  console.log(JSON.stringify(payload, null, 2));
}

main();
