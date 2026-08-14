// Screens whether signs 095 and 845 (and a few related units) are genuine
// markers of the copper-tablet register, or just travel with sign 407, which
// already marks it. The label is material=Copper and type=TAB:C in the
// filtered corpus metadata (complete texts, collapsed to one row per exact
// text). For each target unit (unigrams like 095, bigrams like 061-845) we
// compute its support inside the labeled rows and a right-tail Fisher exact
// p-value, then rerun the same score after deleting every row that contains
// 407 — a real subregister sign should keep some support. The null: 500 label
// shuffles, scoring both the fixed unit and the maxstat "any unit of the same
// kind does as well" version. Writes one JSON report with per-unit decisions
// (candidate / candidate_but_407_dependent / killed_or_passenger).
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_copper_register_subsigns_095_845_20260531';
const ITERATIONS = 500;
const TARGETS = [
  { kind: 'unigram', unit: '095' },
  { kind: 'unigram', unit: '845' },
  { kind: 'bigram', unit: '061-845' },
  { kind: 'bigram', unit: '407-061' },
  { kind: 'bigram', unit: '520-095' },
  { kind: 'unigram', unit: '407' },
];
let UNIT_INDEX = null;

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

function logFactorials(n) {
  const out = [0];
  for (let i = 1; i <= n; i += 1) out[i] = out[i - 1] + Math.log(i);
  return out;
}

function logChoose(logFact, n, k) {
  if (k < 0 || k > n) return Number.NEGATIVE_INFINITY;
  return logFact[n] - logFact[k] - logFact[n - k];
}

function fisherRight(a, b, c, d) {
  const row1 = a + b;
  const row2 = c + d;
  const col1 = a + c;
  const total = row1 + row2;
  const logFact = logFactorials(total);
  let p = 0;
  for (let x = a; x <= Math.min(row1, col1); x += 1) {
    p += Math.exp(
      logChoose(logFact, col1, x)
      + logChoose(logFact, total - col1, row1 - x)
      - logChoose(logFact, total, row1),
    );
  }
  return p;
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

function rowUnits(toks) {
  const unigrams = new Set(toks);
  const bigrams = new Set();
  for (let i = 0; i < toks.length - 1; i += 1) bigrams.add(`${toks[i]}-${toks[i + 1]}`);
  return {
    unigram: unigrams,
    bigram: bigrams,
    first: new Set(toks.length ? [toks[0]] : []),
  };
}

function buildUnitIndex(rows) {
  const out = new Map(['unigram', 'bigram', 'first'].map((kind) => [kind, new Map()]));
  for (let i = 0; i < rows.length; i += 1) {
    for (const kind of out.keys()) {
      for (const unit of rows[i].units[kind]) {
        const m = out.get(kind);
        if (!m.has(unit)) m.set(unit, []);
        m.get(unit).push(i);
      }
    }
  }
  return out;
}

function scoreUnit(rows, labels, kind, unit, labelRowsOverride = null, unitIndexOverride = null) {
  const index = unitIndexOverride ?? UNIT_INDEX;
  const unitIndices = index?.get(kind)?.get(unit) ?? [];
  const unitRows = unitIndices.length;
  let support = 0;
  const labelRows = labelRowsOverride ?? labels.filter(Boolean).length;
  for (const i of unitIndices) if (labels[i]) support += 1;
  return {
    kind,
    unit,
    n_rows: rows.length,
    unit_rows: unitRows,
    label_rows: labelRows,
    support,
    unit_share_in_label: labelRows ? support / labelRows : 0,
    label_share_given_unit: unitRows ? support / unitRows : 0,
    baseline_label_share: rows.length ? labelRows / rows.length : 0,
    fisher_right_tail: fisherRight(support, unitRows - support, labelRows - support, rows.length - unitRows - labelRows + support),
  };
}

function allUnits(rows, kind) {
  return [...(UNIT_INDEX?.get(kind)?.keys() ?? [])];
}

function supportMapsForPositiveRows(rows, shuffledLabels) {
  const out = new Map(['unigram', 'bigram', 'first'].map((kind) => [kind, new Map()]));
  for (let i = 0; i < rows.length; i += 1) {
    if (!shuffledLabels[i]) continue;
    for (const kind of out.keys()) {
      const m = out.get(kind);
      for (const unit of rows[i].units[kind]) m.set(unit, (m.get(unit) ?? 0) + 1);
    }
  }
  return out;
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const byText = new Map();
for (const row of rawRows) {
  if (!byText.has(row.text)) byText.set(row.text, row);
}
const rows = [...byText.values()].map((row) => {
  const toks = tokens(row.text);
  return {
    cisi: row.cisi,
    site: row.site,
    type: row.type,
    material: row.material,
    symbol: row.symbol,
    text: row.text,
    label: row.material === 'Copper' && row.type === 'TAB:C',
    has407: toks.includes('407'),
    units: rowUnits(toks),
  };
});

const labels = rows.map((row) => row.label);
const labelRows = labels.filter(Boolean).length;
UNIT_INDEX = buildUnitIndex(rows);
const liveTargets = TARGETS.map((target) => {
  const live = scoreUnit(rows, labels, target.kind, target.unit, labelRows, UNIT_INDEX);
  const without407Rows = rows.filter((row) => !row.has407);
  const without407Labels = without407Rows.map((row) => row.label);
  const without407Index = buildUnitIndex(without407Rows);
  const without407LabelRows = without407Labels.filter(Boolean).length;
  return {
    ...live,
    without_407: scoreUnit(without407Rows, without407Labels, target.kind, target.unit, without407LabelRows, without407Index),
    copper_examples: rows
      .filter((row) => row.label && row.units[target.kind].has(target.unit))
      .slice(0, 10)
      .map((row) => `${row.cisi}:${row.text}`),
  };
});

const unitsByKind = new Map(['unigram', 'bigram', 'first'].map((kind) => [kind, allUnits(rows, kind)]));
const rand = mulberry32(0xC095845);
const nulls = {};
for (const target of liveTargets) {
  let maxstatGe = 0;
  let fixedGe = 0;
  const unitRowsForKind = UNIT_INDEX.get(target.kind);
  for (let iter = 0; iter < ITERATIONS; iter += 1) {
    const shuffled = fisherYates(labels, rand);
    const supportMaps = supportMapsForPositiveRows(rows, shuffled);
    const kindSupport = supportMaps.get(target.kind);
    const fixedSupport = kindSupport.get(target.unit) ?? 0;
    const fixedUnitRows = unitRowsForKind.get(target.unit)?.length ?? 0;
    if (fixedSupport >= target.support && fixedUnitRows && fixedSupport / fixedUnitRows >= target.label_share_given_unit) fixedGe += 1;
    let any = false;
    for (const [unit, support] of kindSupport.entries()) {
      const unitRows = unitRowsForKind.get(unit)?.length ?? 0;
      if (support >= target.support && unitRows && support / unitRows >= target.label_share_given_unit) {
        any = true;
        break;
      }
    }
    if (any) maxstatGe += 1;
  }
  nulls[`${target.kind}:${target.unit}`] = {
    iterations: ITERATIONS,
    fixed_p_support_and_purity_ge_live: fixedGe / ITERATIONS,
    maxstat_p_any_same_kind_support_and_purity_ge_live: maxstatGe / ITERATIONS,
  };
}

const report = {
  date: '2026-05-31',
  phase: 'EXPAND',
  candidate_id: PREFIX,
  tier: 'candidate_screen',
  bet: 'Within the copper TAB:C register, signs 095 and 845 are not merely passengers of 407; they are candidate subregister signs. If true, 095/845 should remain enriched in Copper|TAB:C rows and partially survive after removing rows containing 407.',
  source: META,
  collapse_key: ['text'],
  label: 'material=Copper and type=TAB:C',
  live_targets: liveTargets,
  label_shuffle_nulls: nulls,
  decisions: liveTargets.map((target) => {
    const key = `${target.kind}:${target.unit}`;
    const nullRow = nulls[key];
    let tier = 'killed_or_passenger';
    if (target.without_407.support >= 2 && nullRow.maxstat_p_any_same_kind_support_and_purity_ge_live <= 0.05) tier = 'candidate';
    else if (nullRow.maxstat_p_any_same_kind_support_and_purity_ge_live <= 0.05) tier = 'candidate_but_407_dependent';
    return {
      unit: key,
      tier,
      reason: `${target.support}/${target.unit_rows} labeled Copper|TAB:C; without 407 rows ${target.without_407.support}/${target.without_407.unit_rows}; maxstat p ${nullRow.maxstat_p_any_same_kind_support_and_purity_ge_live}`,
    };
  }),
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({
  candidate_id: PREFIX,
  decisions: report.decisions,
  live_targets: liveTargets.map((row) => ({
    unit: `${row.kind}:${row.unit}`,
    support: row.support,
    unit_rows: row.unit_rows,
    label_rows: row.label_rows,
    label_share_given_unit: row.label_share_given_unit,
    without407: {
      support: row.without_407.support,
      unit_rows: row.without_407.unit_rows,
      label_share_given_unit: row.without_407.label_share_given_unit,
    },
    null: nulls[`${row.kind}:${row.unit}`],
  })),
}, null, 2));
