// Measures how much predictive power the terminal governors 002 and 060
// actually buy — the "unicity delta". If a text's second-to-last sign is a
// governor, the final sign should be more predictable than after an ordinary
// penultimate sign. We read the filtered corpus metadata (complete texts
// only), collapse to one unit per exact text, and run leave-one-site cross-
// validation: for each site, predict its held-out final signs from the
// penult-to-final counts trained on the other sites (at least 5 training
// rows per penult, and held-out texts are excluded from training). Metrics
// per row: top-1/top-3 hit, true probability, effective candidates
// (2^entropy), and surprisal delta in bits versus the unconditional final
// distribution. A 1000-iteration shuffle of final labels supplies the null.
// Writes a JSON report plus per-prediction and per-penult CSVs.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_terminal_governor_unicity_delta_20260531';
const TARGET_GOVERNORS = new Set(['002', '060']);
const MIN_TRAIN_FOR_EVAL = 5;
const NULL_ITERATIONS = 1000;

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

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function esc(value) {
  const text = String(value ?? '');
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const body = rows.map((row) => fields.map((field) => esc(row[field])).join(',')).join('\n');
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`, 'utf8');
}

function mulberry32(seed) {
  return function rand() {
    let t = seed += 0x6D2B79F5;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function fisherYates(values, rand) {
  const out = values.slice();
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function inc(map, key, amount = 1) {
  map.set(key, (map.get(key) ?? 0) + amount);
}

function entropyBits(counts) {
  const total = [...counts.values()].reduce((sum, value) => sum + value, 0);
  if (!total) return 0;
  let entropy = 0;
  for (const count of counts.values()) {
    const p = count / total;
    entropy -= p * Math.log2(p);
  }
  return entropy;
}

function topN(counts, n) {
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, n)
    .map(([sign]) => sign);
}

function buildFolds(units, sites) {
  return sites.map((site) => {
    const holdout = units.filter((unit) => unit.sites.has(site));
    const holdoutTexts = new Set(holdout.map((unit) => unit.text));
    const train = units.filter((unit) => !unit.sites.has(site) && !holdoutTexts.has(unit.text));
    return { site, holdout, train };
  }).filter((fold) => fold.holdout.length);
}

function evaluateFolds(folds, finalOverrideByIndex = null) {
  const predictions = [];
  for (const { site, holdout, train } of folds) {
    const byPenult = new Map();
    const globalFinal = new Map();
    for (const unit of train) {
      const final = finalOverrideByIndex?.get(unit.index) ?? unit.final;
      if (!byPenult.has(unit.penult)) byPenult.set(unit.penult, new Map());
      inc(byPenult.get(unit.penult), final);
      inc(globalFinal, final);
    }
    for (const unit of holdout) {
      const dist = byPenult.get(unit.penult);
      if (!dist) continue;
      const trainCount = [...dist.values()].reduce((sum, count) => sum + count, 0);
      if (trainCount < MIN_TRAIN_FOR_EVAL) continue;
      const globalCount = [...globalFinal.values()].reduce((sum, count) => sum + count, 0);
      const top1 = topN(dist, 1);
      const top3 = topN(dist, 3);
      const trueCount = dist.get(unit.final) ?? 0;
      const trueProb = trueCount / trainCount;
      const globalProb = (globalFinal.get(unit.final) ?? 0) / Math.max(1, globalCount);
      const conditionalSurprisal = trueProb > 0 ? -Math.log2(trueProb) : Infinity;
      const globalSurprisal = globalProb > 0 ? -Math.log2(globalProb) : Infinity;
      predictions.push({
        site,
        text: unit.text,
        penult: unit.penult,
        final: unit.final,
        target: TARGET_GOVERNORS.has(unit.penult),
        train_count: trainCount,
        train_options: dist.size,
        train_entropy_bits: entropyBits(dist),
        train_effective_candidates: 2 ** entropyBits(dist),
        top1_hit: top1.includes(unit.final) ? 1 : 0,
        top3_hit: top3.includes(unit.final) ? 1 : 0,
        true_prob: trueProb,
        global_true_prob: globalProb,
        conditional_surprisal_bits: Number.isFinite(conditionalSurprisal) ? conditionalSurprisal : null,
        global_surprisal_bits: Number.isFinite(globalSurprisal) ? globalSurprisal : null,
        surprisal_delta_bits:
          Number.isFinite(conditionalSurprisal) && Number.isFinite(globalSurprisal)
            ? globalSurprisal - conditionalSurprisal
            : null,
        top3: top3.join(' '),
      });
    }
  }
  return predictions;
}

function summarize(predictions, filterFn) {
  const rows = predictions.filter(filterFn);
  const finiteDelta = rows.filter((row) => row.surprisal_delta_bits !== null);
  return {
    evaluated_rows: rows.length,
    top1_accuracy: rows.length ? rows.reduce((sum, row) => sum + row.top1_hit, 0) / rows.length : null,
    top3_accuracy: rows.length ? rows.reduce((sum, row) => sum + row.top3_hit, 0) / rows.length : null,
    mean_true_probability: rows.length ? rows.reduce((sum, row) => sum + row.true_prob, 0) / rows.length : null,
    mean_global_true_probability: rows.length
      ? rows.reduce((sum, row) => sum + row.global_true_prob, 0) / rows.length
      : null,
    mean_effective_candidates: rows.length
      ? rows.reduce((sum, row) => sum + row.train_effective_candidates, 0) / rows.length
      : null,
    mean_train_options: rows.length ? rows.reduce((sum, row) => sum + row.train_options, 0) / rows.length : null,
    mean_surprisal_delta_bits: finiteDelta.length
      ? finiteDelta.reduce((sum, row) => sum + row.surprisal_delta_bits, 0) / finiteDelta.length
      : null,
  };
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const byText = new Map();
for (const row of rawRows) {
  const toks = tokens(row.text);
  if (toks.length < 2) continue;
  const key = row.text;
  if (!byText.has(key)) {
    byText.set(key, {
      text: row.text,
      penult: toks[toks.length - 2],
      final: toks[toks.length - 1],
      length: toks.length,
      sites: new Set(),
      types: new Set(),
      materials: new Set(),
      symbols: new Set(),
      cisis: new Set(),
    });
  }
  const unit = byText.get(key);
  unit.sites.add(row.site || 'unknown');
  unit.types.add(row.type || 'unknown');
  unit.materials.add(row.material || 'unknown');
  unit.symbols.add(row.symbol || 'unknown');
  unit.cisis.add(row.cisi || 'unknown');
}

const units = [...byText.values()]
  .map((unit, index) => ({ ...unit, index }))
  .filter((unit) => unit.final && unit.penult);
const sites = [...new Set(units.flatMap((unit) => [...unit.sites]))].filter((site) => site && site !== '--');
const folds = buildFolds(units, sites);

const predictions = evaluateFolds(folds);
const byPenultSummary = [...new Set(predictions.map((row) => row.penult))]
  .map((penult) => {
    const summary = summarize(predictions, (row) => row.penult === penult);
    return {
      penult,
      is_target_governor: TARGET_GOVERNORS.has(penult) ? 'Y' : 'N',
      ...summary,
    };
  })
  .filter((row) => row.evaluated_rows >= MIN_TRAIN_FOR_EVAL)
  .sort((a, b) => b.evaluated_rows - a.evaluated_rows || a.penult.localeCompare(b.penult));

const observedTarget = summarize(predictions, (row) => row.target);
const observedNonTarget = summarize(predictions, (row) => !row.target);
const observedAll = summarize(predictions, () => true);

const finalLabels = units.map((unit) => unit.final);
const rand = mulberry32(0xA1102C31);
let geTop1 = 0;
let geTop3 = 0;
let geTrueProb = 0;
let leEffective = 0;
let geDelta = 0;
const nullSnapshots = [];
for (let iter = 0; iter < NULL_ITERATIONS; iter += 1) {
  const shuffled = fisherYates(finalLabels, rand);
  const overrides = new Map(units.map((unit, idx) => [unit.index, shuffled[idx]]));
  const simPred = evaluateFolds(folds, overrides);
  const simTarget = summarize(simPred, (row) => row.target);
  if ((simTarget.top1_accuracy ?? -Infinity) >= (observedTarget.top1_accuracy ?? Infinity)) geTop1 += 1;
  if ((simTarget.top3_accuracy ?? -Infinity) >= (observedTarget.top3_accuracy ?? Infinity)) geTop3 += 1;
  if ((simTarget.mean_true_probability ?? -Infinity) >= (observedTarget.mean_true_probability ?? Infinity)) geTrueProb += 1;
  if ((simTarget.mean_effective_candidates ?? Infinity) <= (observedTarget.mean_effective_candidates ?? -Infinity)) {
    leEffective += 1;
  }
  if ((simTarget.mean_surprisal_delta_bits ?? -Infinity) >= (observedTarget.mean_surprisal_delta_bits ?? Infinity)) {
    geDelta += 1;
  }
  if (iter < 25) {
    nullSnapshots.push({
      iteration: iter,
      target_top1_accuracy: simTarget.top1_accuracy,
      target_top3_accuracy: simTarget.top3_accuracy,
      target_mean_true_probability: simTarget.mean_true_probability,
      target_mean_effective_candidates: simTarget.mean_effective_candidates,
      target_mean_surprisal_delta_bits: simTarget.mean_surprisal_delta_bits,
    });
  }
}

const targetByPenult = Object.fromEntries(
  [...TARGET_GOVERNORS].map((penult) => [penult, summarize(predictions, (row) => row.penult === penult)]),
);

const tier = observedTarget.evaluated_rows >= 50
  && observedTarget.top3_accuracy >= 0.65
  && geTop3 / NULL_ITERATIONS <= 0.01
  && geDelta / NULL_ITERATIONS <= 0.01
  ? 'candidate'
  : 'wild shot';

const report = {
  date: '2026-05-31',
  phase: 'EXPAND',
  candidate_id: PREFIX,
  tier,
  bet:
    'If the 002/060 terminal-governor model is carrying real effective-unicity pressure, then final signs after 002/060 should remain more predictable under leave-site text-family prediction than final signs after ordinary penultimate signs, and the advantage should not appear after shuffling final labels across terminal families.',
  source: META,
  collapse_key: 'exact text; sites are held as a set and held-out exact texts are excluded from training',
  evaluation: {
    unit_count_exact_terminal_text_families: units.length,
    sites: sites.length,
    min_train_rows_per_penult_for_eval: MIN_TRAIN_FOR_EVAL,
    target_governors: [...TARGET_GOVERNORS],
    observed_all: observedAll,
    observed_target_governors: observedTarget,
    observed_non_target_penults: observedNonTarget,
    observed_target_by_penult: targetByPenult,
  },
  final_label_shuffle_null: {
    iterations: NULL_ITERATIONS,
    preserves: 'terminal text families, penultimate signs, sites, and global final-sign inventory; shuffles final labels only in training folds',
    p_ge_target_top1_accuracy: geTop1 / NULL_ITERATIONS,
    p_ge_target_top3_accuracy: geTop3 / NULL_ITERATIONS,
    p_ge_target_mean_true_probability: geTrueProb / NULL_ITERATIONS,
    p_le_target_mean_effective_candidates: leEffective / NULL_ITERATIONS,
    p_ge_target_mean_surprisal_delta_bits: geDelta / NULL_ITERATIONS,
    first_25_iterations: nullSnapshots,
  },
  strongest_penults: byPenultSummary.slice(0, 30),
  decision:
    tier === 'candidate'
      ? 'candidate_effective_unicity_local_to_terminal_governors'
      : 'screening_only_not_promoted',
  caveat:
    'This is structural prediction, not decipherment. It does not assign sound, language family, or meaning; it tests whether the promoted terminal-governor bet measurably compresses held-out final-slot possibilities.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
writeCsv(path.join(OUT_DIR, `${PREFIX}_predictions.csv`), predictions, [
  'site',
  'text',
  'penult',
  'final',
  'target',
  'train_count',
  'train_options',
  'train_entropy_bits',
  'train_effective_candidates',
  'top1_hit',
  'top3_hit',
  'true_prob',
  'global_true_prob',
  'conditional_surprisal_bits',
  'global_surprisal_bits',
  'surprisal_delta_bits',
  'top3',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_penults.csv`), byPenultSummary, [
  'penult',
  'is_target_governor',
  'evaluated_rows',
  'top1_accuracy',
  'top3_accuracy',
  'mean_true_probability',
  'mean_global_true_probability',
  'mean_effective_candidates',
  'mean_train_options',
  'mean_surprisal_delta_bits',
]);

console.log(JSON.stringify({
  candidate_id: PREFIX,
  tier,
  decision: report.decision,
  observed_target_governors: observedTarget,
  observed_target_by_penult: targetByPenult,
  observed_non_target_penults: observedNonTarget,
  null: report.final_label_shuffle_null,
}, null, 2));
