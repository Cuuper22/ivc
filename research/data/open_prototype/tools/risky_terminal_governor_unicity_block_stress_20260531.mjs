import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT = path.join(ROOT, 'data', 'open_prototype', 'reports', 'risky_terminal_governor_unicity_block_stress_20260531.json');
const TARGET_GOVERNORS = new Set(['002', '060']);
const MIN_TRAIN = 5;
const ITERATIONS = 100;

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

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function inc(map, key) {
  map.set(key, (map.get(key) ?? 0) + 1);
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

function mulberry32(seed) {
  return function rand() {
    let t = seed += 0x6D2B79F5;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffled(values, rand) {
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
    const toks = tokens(row.text);
    if (toks.length < 2) continue;
    if (!byText.has(row.text)) {
      byText.set(row.text, {
        text: row.text,
        penult: toks[toks.length - 2],
        final: toks[toks.length - 1],
        sites: new Set(),
      });
    }
    byText.get(row.text).sites.add(row.site || 'unknown');
  }
  return [...byText.values()].map((unit, index) => ({ ...unit, index }));
}

function buildFolds(units) {
  const sites = [...new Set(units.flatMap((unit) => [...unit.sites]))].filter((site) => site && site !== '--');
  return sites.map((site) => {
    const holdout = units.filter((unit) => unit.sites.has(site));
    const holdoutTexts = new Set(holdout.map((unit) => unit.text));
    const train = units.filter((unit) => !unit.sites.has(site) && !holdoutTexts.has(unit.text));
    return { site, holdout, train };
  }).filter((fold) => fold.holdout.length);
}

function evaluate(folds, finalOverride = null) {
  const rows = [];
  for (const { site, holdout, train } of folds) {
    const byPenult = new Map();
    const global = new Map();
    for (const unit of train) {
      const final = finalOverride?.get(unit.index) ?? unit.final;
      if (!byPenult.has(unit.penult)) byPenult.set(unit.penult, new Map());
      inc(byPenult.get(unit.penult), final);
      inc(global, final);
    }
    const globalTotal = [...global.values()].reduce((sum, count) => sum + count, 0);
    for (const unit of holdout) {
      const dist = byPenult.get(unit.penult);
      if (!dist) continue;
      const trainTotal = [...dist.values()].reduce((sum, count) => sum + count, 0);
      if (trainTotal < MIN_TRAIN) continue;
      const trueCount = dist.get(unit.final) ?? 0;
      rows.push({
        site,
        penult: unit.penult,
        final: unit.final,
        target: TARGET_GOVERNORS.has(unit.penult),
        top1_hit: topN(dist, 1).includes(unit.final) ? 1 : 0,
        top3_hit: topN(dist, 3).includes(unit.final) ? 1 : 0,
        true_prob: trueCount / trainTotal,
        global_true_prob: (global.get(unit.final) ?? 0) / Math.max(1, globalTotal),
        effective_candidates: 2 ** entropyBits(dist),
      });
    }
  }
  return rows;
}

function summarize(rows, filter) {
  const subset = rows.filter(filter);
  return {
    evaluated_rows: subset.length,
    top1_accuracy: subset.length ? subset.reduce((sum, row) => sum + row.top1_hit, 0) / subset.length : null,
    top3_accuracy: subset.length ? subset.reduce((sum, row) => sum + row.top3_hit, 0) / subset.length : null,
    mean_true_probability: subset.length ? subset.reduce((sum, row) => sum + row.true_prob, 0) / subset.length : null,
    mean_global_true_probability: subset.length
      ? subset.reduce((sum, row) => sum + row.global_true_prob, 0) / subset.length
      : null,
    mean_effective_candidates: subset.length
      ? subset.reduce((sum, row) => sum + row.effective_candidates, 0) / subset.length
      : null,
  };
}

function runPanel(id, rows) {
  const units = buildUnits(rows);
  const folds = buildFolds(units);
  const liveRows = evaluate(folds);
  const target = summarize(liveRows, (row) => row.target);
  const nonTarget = summarize(liveRows, (row) => !row.target);
  const finals = units.map((unit) => unit.final);
  const rand = mulberry32(0x713021 + id.length);
  let geTop3 = 0;
  let geProb = 0;
  let leEff = 0;
  for (let iter = 0; iter < ITERATIONS; iter += 1) {
    const shuffledFinals = shuffled(finals, rand);
    const override = new Map(units.map((unit, idx) => [unit.index, shuffledFinals[idx]]));
    const sim = summarize(evaluate(folds, override), (row) => row.target);
    if ((sim.top3_accuracy ?? -Infinity) >= (target.top3_accuracy ?? Infinity)) geTop3 += 1;
    if ((sim.mean_true_probability ?? -Infinity) >= (target.mean_true_probability ?? Infinity)) geProb += 1;
    if ((sim.mean_effective_candidates ?? Infinity) <= (target.mean_effective_candidates ?? -Infinity)) leEff += 1;
  }
  return {
    id,
    source_rows: rows.length,
    exact_terminal_families: units.length,
    target,
    non_target: nonTarget,
    final_label_shuffle_null: {
      iterations: ITERATIONS,
      p_ge_target_top3_accuracy: geTop3 / ITERATIONS,
      p_ge_target_mean_true_probability: geProb / ITERATIONS,
      p_le_target_mean_effective_candidates: leEff / ITERATIONS,
    },
  };
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const panels = [
  {
    id: 'all_complete_exact_text',
    rows,
  },
  {
    id: 'remove_mohenjo_seal_s',
    rows: rows.filter((row) => !(row.site === 'Mohenjo-daro' && row.type === 'SEAL:S')),
  },
  {
    id: 'remove_harappa_seal_s',
    rows: rows.filter((row) => !(row.site === 'Harappa' && row.type === 'SEAL:S')),
  },
  {
    id: 'remove_mohenjo_and_harappa_seal_s',
    rows: rows.filter((row) => !(['Mohenjo-daro', 'Harappa'].includes(row.site) && row.type === 'SEAL:S')),
  },
];

const results = panels.map((panel) => runPanel(panel.id, panel.rows));
const hard = results.find((row) => row.id === 'remove_mohenjo_seal_s');
const decision = hard.target.evaluated_rows >= 100
  && hard.target.top3_accuracy >= 0.55
  && hard.final_label_shuffle_null.p_ge_target_top3_accuracy <= 0.01
  ? 'survives_remove_mohenjo_seal_s_unicity_stress'
  : 'demoted_by_remove_mohenjo_seal_s_unicity_stress';

const report = {
  date: '2026-05-31',
  phase: 'CONSOLIDATE',
  candidate_id: 'risky_terminal_governor_unicity_block_stress_20260531',
  bet: 'The terminal-governor effective-unicity signal is not carried only by Mohenjo-daro SEAL:S or Harappa SEAL:S blocks.',
  source: META,
  panels: results,
  decision,
  caveat:
    'This stress keeps exact-text collapse but does not perform source-image token boxing. It is structural prediction only.',
};

fs.writeFileSync(OUT, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({
  candidate_id: report.candidate_id,
  decision,
  panels: results.map((row) => ({
    id: row.id,
    target: row.target,
    non_target: row.non_target,
    null: row.final_label_shuffle_null,
  })),
}, null, 2));
