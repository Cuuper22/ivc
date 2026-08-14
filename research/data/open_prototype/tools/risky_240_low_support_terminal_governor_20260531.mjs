// Tests whether sign `240`, when it sits second-to-last, governs which sign closes
// the inscription — a "terminal governor" with a small closure set dominated by 235
// and 798. Support is thin (about 23 exact text families), so the test is built
// around out-of-sample prediction: the script reads metadata_filtered.csv (complete
// rows only), collapses rows to exact text families, and runs leave-one-site
// cross-validation. For each held-out site, it learns the final-sign distribution
// after penult 240 from the other sites (needing at least 5 training rows) and
// scores top-1/top-3 accuracy, mean probability of the true final, and effective
// candidate count on the held-out rows. A 2,000-iteration null shuffles final signs
// across all text families and reruns the whole cross-validation to price those
// scores. Writes a single JSON report to the reports directory.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT = path.join(ROOT, 'data', 'open_prototype', 'reports', 'risky_240_low_support_terminal_governor_20260531.json');
const TARGET = '240';
const MIN_TRAIN = 5;
const ITERATIONS = 2000;

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
      } else if (ch === '"') quoted = false;
      else cell += ch;
    } else if (ch === '"') quoted = true;
    else if (ch === ',') {
      row.push(cell);
      cell = '';
    } else if (ch === '\n') {
      row.push(cell.replace(/\r$/, ''));
      if (row.some((value) => value.length)) rows.push(row);
      row = [];
      cell = '';
    } else cell += ch;
  }
  if (cell.length || row.length) {
    row.push(cell.replace(/\r$/, ''));
    if (row.some((value) => value.length)) rows.push(row);
  }
  const [header, ...body] = rows;
  return body.map((cols) => Object.fromEntries(header.map((name, idx) => [name, cols[idx] ?? ''])));
}

function toks(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function inc(map, key) {
  map.set(key, (map.get(key) ?? 0) + 1);
}

function entropyBits(counts) {
  const total = [...counts.values()].reduce((sum, value) => sum + value, 0);
  let e = 0;
  for (const count of counts.values()) {
    const p = count / total;
    e -= p * Math.log2(p);
  }
  return e;
}

function topN(counts, n) {
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, n)
    .map(([sign]) => sign);
}

function mulberry32(seed) {
  return function rand() {
    let t = seed += 0x6D2B79F5;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffle(values, rand) {
  const out = values.slice();
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function buildUnits(rows) {
  const byText = new Map();
  for (const row of rows) {
    const t = toks(row.text);
    if (t.length < 2) continue;
    if (!byText.has(row.text)) {
      byText.set(row.text, {
        text: row.text,
        penult: t[t.length - 2],
        final: t[t.length - 1],
        sites: new Set(),
        types: new Set(),
        symbols: new Set(),
        cisis: new Set(),
      });
    }
    const unit = byText.get(row.text);
    unit.sites.add(row.site);
    unit.types.add(row.type);
    unit.symbols.add(row.symbol);
    unit.cisis.add(row.cisi);
  }
  return [...byText.values()].map((unit, index) => ({ ...unit, index }));
}

function buildFolds(units) {
  const sites = [...new Set(units.flatMap((unit) => [...unit.sites]))].filter((site) => site && site !== '--');
  return sites.map((site) => {
    const holdout = units.filter((unit) => unit.sites.has(site));
    const holdoutText = new Set(holdout.map((unit) => unit.text));
    const train = units.filter((unit) => !unit.sites.has(site) && !holdoutText.has(unit.text));
    return { site, holdout, train };
  }).filter((fold) => fold.holdout.length);
}

function evaluate(folds, override = null) {
  const rows = [];
  for (const { site, holdout, train } of folds) {
    const byPenult = new Map();
    for (const unit of train) {
      const final = override?.get(unit.index) ?? unit.final;
      if (!byPenult.has(unit.penult)) byPenult.set(unit.penult, new Map());
      inc(byPenult.get(unit.penult), final);
    }
    for (const unit of holdout.filter((u) => u.penult === TARGET)) {
      const dist = byPenult.get(TARGET);
      if (!dist) continue;
      const trainTotal = [...dist.values()].reduce((sum, count) => sum + count, 0);
      if (trainTotal < MIN_TRAIN) continue;
      rows.push({
        site,
        text: unit.text,
        final: unit.final,
        train_count: trainTotal,
        options: dist.size,
        top1_hit: topN(dist, 1).includes(unit.final) ? 1 : 0,
        top3_hit: topN(dist, 3).includes(unit.final) ? 1 : 0,
        true_prob: (dist.get(unit.final) ?? 0) / trainTotal,
        effective_candidates: 2 ** entropyBits(dist),
        top3: topN(dist, 3).join(' '),
      });
    }
  }
  return rows;
}

function summarize(rows) {
  return {
    evaluated_rows: rows.length,
    top1_accuracy: rows.length ? rows.reduce((sum, row) => sum + row.top1_hit, 0) / rows.length : null,
    top3_accuracy: rows.length ? rows.reduce((sum, row) => sum + row.top3_hit, 0) / rows.length : null,
    mean_true_probability: rows.length ? rows.reduce((sum, row) => sum + row.true_prob, 0) / rows.length : null,
    mean_effective_candidates: rows.length ? rows.reduce((sum, row) => sum + row.effective_candidates, 0) / rows.length : null,
  };
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const units = buildUnits(rows);
const folds = buildFolds(units);
const liveRows = evaluate(folds);
const live = summarize(liveRows);
const targetUnits = units.filter((unit) => unit.penult === TARGET);
const finalDistribution = Object.fromEntries([...targetUnits.reduce((map, unit) => {
  inc(map, unit.final);
  return map;
}, new Map()).entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])));

const finals = units.map((unit) => unit.final);
const rand = mulberry32(0x2402026);
let geTop1 = 0;
let geTop3 = 0;
let geProb = 0;
let leEff = 0;
for (let iter = 0; iter < ITERATIONS; iter += 1) {
  const shuffled = shuffle(finals, rand);
  const override = new Map(units.map((unit, idx) => [unit.index, shuffled[idx]]));
  const sim = summarize(evaluate(folds, override));
  if ((sim.top1_accuracy ?? -Infinity) >= live.top1_accuracy) geTop1 += 1;
  if ((sim.top3_accuracy ?? -Infinity) >= live.top3_accuracy) geTop3 += 1;
  if ((sim.mean_true_probability ?? -Infinity) >= live.mean_true_probability) geProb += 1;
  if ((sim.mean_effective_candidates ?? Infinity) <= live.mean_effective_candidates) leEff += 1;
}

const report = {
  date: '2026-05-31',
  phase: 'EXPAND',
  candidate_id: 'risky_240_low_support_terminal_governor_20260531',
  tier: live.evaluated_rows >= 20 && geTop3 / ITERATIONS <= 0.01 ? 'candidate' : 'wild shot',
  bet: 'Penult 240 is a low-support local terminal governor with a constrained closure set dominated by 235 and 798.',
  source: META,
  target_exact_text_families: targetUnits.length,
  final_distribution: finalDistribution,
  leave_site_prediction: live,
  final_label_shuffle_null: {
    iterations: ITERATIONS,
    p_ge_top1_accuracy: geTop1 / ITERATIONS,
    p_ge_top3_accuracy: geTop3 / ITERATIONS,
    p_ge_mean_true_probability: geProb / ITERATIONS,
    p_le_mean_effective_candidates: leEff / ITERATIONS,
  },
  examples: targetUnits.map((unit) => ({
    text: unit.text,
    final: unit.final,
    sites: [...unit.sites],
    types: [...unit.types],
    symbols: [...unit.symbols],
    cisis: [...unit.cisis].slice(0, 8),
  })),
  decision: live.evaluated_rows >= 20 && geTop3 / ITERATIONS <= 0.01
    ? 'candidate_low_support_terminal_governor'
    : 'wild_shot_not_promoted',
  caveat:
    'This candidate has only 23 exact text families and is much weaker than 002/060. It must survive source-family collapse and a context split of 235 vs 798 before promotion.',
};

fs.writeFileSync(OUT, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({
  candidate_id: report.candidate_id,
  tier: report.tier,
  decision: report.decision,
  final_distribution: finalDistribution,
  leave_site_prediction: live,
  null: report.final_label_shuffle_null,
}, null, 2));
