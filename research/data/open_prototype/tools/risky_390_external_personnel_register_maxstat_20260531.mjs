// Asks whether sign `390` (and the pairs `740-390` and `390-590`) is enriched on
// Indus objects found outside the Indus area — the bet being that 390 marks a
// personnel/title register in external Meluhha-contact contexts, motivated by
// cuneiform records of Meluhha interpreters and officials. The script reads the
// external-object list (data/meluhha/external_indus_objects.csv) and the main
// corpus (metadata_filtered.csv), drops circular seals from both, restricts the
// background to object types that also occur externally, and deduplicates rows by
// type + shape + text. Every observed sign and every adjacent sign pair is
// Fisher-tested for external enrichment, and a 1,000-iteration label-shuffle null
// takes the minimum p over all features each round (max-stat), so the 390 targets
// are priced against the full search space. Four control panels rerun the test:
// leave-out-Kish, leave-out-Gonur-Depe, complete rows only, and square SEAL:S only.
// Writes one JSON report to the reports directory and prints the panel targets.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const EXTERNAL = path.join(ROOT, 'data', 'meluhha', 'external_indus_objects.csv');
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_390_external_personnel_register_maxstat_20260531';
const ITERATIONS = 1000;
const TARGETS = ['390', '740-390', '390-590'];

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

function rowFeatures(row) {
  const toks = tokens(row.text);
  const signs = new Set(toks);
  const pairs = new Set();
  for (let i = 0; i < toks.length - 1; i += 1) pairs.add(`${toks[i]}-${toks[i + 1]}`);
  return { signs, pairs };
}

function nonCircular(row) {
  const shape = String(row.shape ?? '').toLowerCase();
  const type = String(row.type ?? '').toLowerCase();
  return !shape.includes('circular') && !type.includes('seal:c');
}

function exactCollapse(rows, label) {
  const seen = new Set();
  const out = [];
  for (const row of rows) {
    const key = `${label}|${row.type}|${row.shape}|${row.text}`;
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(row);
  }
  return out;
}

const logFactCache = [0];
function logFactorial(n) {
  for (let i = logFactCache.length; i <= n; i += 1) {
    logFactCache[i] = logFactCache[i - 1] + Math.log(i);
  }
  return logFactCache[n];
}

function fisherRight(a, b, c, d) {
  const row1 = a + b;
  const row2 = c + d;
  const col1 = a + c;
  const col2 = b + d;
  const n = row1 + row2;
  const maxA = Math.min(row1, col1);
  function logHyper(x) {
    return logFactorial(row1) + logFactorial(row2) + logFactorial(col1) + logFactorial(col2)
      - logFactorial(x) - logFactorial(row1 - x) - logFactorial(col1 - x)
      - logFactorial(row2 - col1 + x) - logFactorial(n);
  }
  const base = logHyper(a);
  let p = 0;
  for (let x = a; x <= maxA; x += 1) {
    p += Math.exp(logHyper(x));
  }
  return Math.min(1, Math.max(0, p || Math.exp(base)));
}

function mulberry32(seed) {
  return function rand() {
    let t = seed += 0x6D2B79F5;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffledLabels(n, k, rand) {
  const labels = Array.from({ length: n }, (_, idx) => idx < k);
  for (let i = labels.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    [labels[i], labels[j]] = [labels[j], labels[i]];
  }
  return labels;
}

function buildFeatureIndex(pool, kind) {
  const index = new Map();
  for (let i = 0; i < pool.length; i += 1) {
    for (const feature of pool[i].features[kind]) {
      if (!index.has(feature)) index.set(feature, []);
      index.get(feature).push(i);
    }
  }
  return index;
}

function featureStats(featureIndex, externalLabels, externalCount, poolSize) {
  const stats = [];
  for (const [feature, indices] of featureIndex.entries()) {
    let a = 0;
    for (const idx of indices) if (externalLabels[idx]) a += 1;
    const b = externalCount - a;
    const c = indices.length - a;
    const d = poolSize - externalCount - c;
    if (a > 0) stats.push({ feature, a, b, c, d, fisher_p: fisherRight(a, b, c, d) });
  }
  stats.sort((x, y) => x.fisher_p - y.fisher_p || y.a - x.a || x.feature.localeCompare(y.feature));
  return stats.map((row, idx) => ({ ...row, rank: idx + 1, total_features: stats.length }));
}

function minFeatureP(featureIndex, externalLabels, externalCount, poolSize) {
  let minP = 1;
  for (const indices of featureIndex.values()) {
    let a = 0;
    for (const idx of indices) if (externalLabels[idx]) a += 1;
    if (!a) continue;
    const b = externalCount - a;
    const c = indices.length - a;
    const d = poolSize - externalCount - c;
    const p = fisherRight(a, b, c, d);
    if (p < minP) minP = p;
  }
  return minP;
}

function runPanel({ id, externalRows, backgroundRows }) {
  const ext = exactCollapse(externalRows, 'external');
  const bg = exactCollapse(backgroundRows, 'background');
  const pool = [...ext, ...bg].map((row) => ({ ...row, features: rowFeatures(row) }));
  const labels = pool.map((_, idx) => idx < ext.length);
  const signIndex = buildFeatureIndex(pool, 'signs');
  const pairIndex = buildFeatureIndex(pool, 'pairs');
  const signStats = featureStats(signIndex, labels, ext.length, pool.length);
  const pairStats = featureStats(pairIndex, labels, ext.length, pool.length);
  const targetRows = TARGETS.map((target) => {
    const kind = target.includes('-') ? 'pairs' : 'signs';
    const stats = kind === 'pairs' ? pairStats : signStats;
    return { target, kind, ...(stats.find((row) => row.feature === target) ?? null) };
  });
  const targetPByKind = new Map(targetRows.filter((row) => row.fisher_p !== undefined).map((row) => [row.target, row.fisher_p]));
  const rand = mulberry32(0x3902026 + id.length);
  const nullCounts = Object.fromEntries(TARGETS.map((target) => [target, 0]));
  for (let iter = 0; iter < ITERATIONS; iter += 1) {
    const simLabels = shuffledLabels(pool.length, ext.length, rand);
    const minSign = minFeatureP(signIndex, simLabels, ext.length, pool.length);
    const minPair = minFeatureP(pairIndex, simLabels, ext.length, pool.length);
    for (const target of TARGETS) {
      const p = targetPByKind.get(target);
      if (p === undefined) continue;
      const min = target.includes('-') ? minPair : minSign;
      if (min <= p) nullCounts[target] += 1;
    }
  }
  return {
    id,
    external_rows: ext.length,
    background_rows: bg.length,
    target_rows: targetRows.map((row) => ({
      ...row,
      maxstat_fpr: row.fisher_p === undefined ? null : nullCounts[row.target] / ITERATIONS,
    })),
    top_signs: signStats.slice(0, 15),
    top_pairs: pairStats.slice(0, 15),
    support_external: ext.filter((row) => tokens(row.text).includes('390')).map((row) => ({
      id: row.row_id ?? row.id,
      cisi: row.cisi,
      site: row.site,
      type: row.type,
      shape: row.shape,
      complete: row.complete,
      text: row.text,
    })),
  };
}

const externalAll = parseCsv(fs.readFileSync(EXTERNAL, 'utf8'));
const metaAll = parseCsv(fs.readFileSync(META, 'utf8'));
const externalIds = new Set(externalAll.map((row) => row.row_id));
const extBase = externalAll.filter(nonCircular);
const extTypes = new Set(extBase.map((row) => row.type));
const backgroundBase = metaAll
  .filter((row) => !externalIds.has(row.id))
  .filter(nonCircular)
  .filter((row) => extTypes.has(row.type));

const panels = [
  {
    id: 'external_non_circular_type_matched',
    externalRows: extBase,
    backgroundRows: backgroundBase,
  },
  {
    id: 'external_non_circular_type_matched_leave_kish',
    externalRows: extBase.filter((row) => row.site !== 'Kish'),
    backgroundRows: backgroundBase,
  },
  {
    id: 'external_non_circular_type_matched_leave_gonur',
    externalRows: extBase.filter((row) => row.site !== 'Gonur Depe'),
    backgroundRows: backgroundBase,
  },
  {
    id: 'external_non_circular_complete_y_type_matched',
    externalRows: extBase.filter((row) => row.complete === 'Y'),
    backgroundRows: backgroundBase.filter((row) => row.complete === 'Y'),
  },
  {
    id: 'external_square_seal_s_only',
    externalRows: extBase.filter((row) => row.type === 'SEAL:S' && String(row.shape).toLowerCase() === 'square'),
    backgroundRows: backgroundBase.filter((row) => row.type === 'SEAL:S' && String(row.shape).toLowerCase() === 'square'),
  },
];

const results = panels.map(runPanel);
const main390 = results[0].target_rows.find((row) => row.target === '390');
const tier = main390?.maxstat_fpr !== null && main390?.maxstat_fpr <= 0.01 ? 'candidate' : 'wild shot';

const report = {
  date: '2026-05-31',
  phase: 'EXPAND',
  candidate_id: PREFIX,
  tier,
  bet:
    '`390` marks an external Meluhha-contact personnel/title register on non-circular objects; if real, it should survive all-sign and all-pair max-stat enrichment tests against type-matched internal rows and not be carried only by Kish or Gonur.',
  readable_side_motivation:
    'The cuneiform lead inventory contains Meluhha interpreter/person/title contexts such as eme-bal me-luh-ha, lu2 me-luh-ha, and ugula me-luh-ha. This report tests only the Indus-side contextual prediction; it does not assign sound.',
  sources: {
    external_objects: EXTERNAL,
    background: META,
  },
  exact_collapse: 'condition label + type + shape + text',
  null: {
    iterations: ITERATIONS,
    preserves: 'row feature sets and number of external rows; shuffles the external/non-external label',
    maxstat_scope: 'all observed signs for sign targets, all observed adjacent pairs for pair targets',
  },
  panels: results,
  decision: tier === 'candidate'
    ? 'candidate_external_390_enrichment_survives_main_maxstat'
    : 'wild_shot_not_promoted_by_maxstat',
  caveat:
    'External-object rows are still catalogue-derived and source validation can kill the bet. Leave-site panels are destructive, not proof of title/personnel semantics.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({
  candidate_id: PREFIX,
  tier,
  decision: report.decision,
  main_targets: results[0].target_rows,
  leave_kish: results[1].target_rows,
  leave_gonur: results[2].target_rows,
  complete_y: results[3].target_rows,
  square_seal_s: results[4].target_rows,
}, null, 2));
