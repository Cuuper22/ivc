// Confound check for an earlier finding that signs `405` and `806` are enriched on
// square seals bearing the Bull1:W icon (unicorn-style bull with standard). The
// worry: both signs often ride inside the fixed frame `740-X-590`, so the icon link
// might belong to the frame, not to the signs. This script reads
// metadata_filtered.csv, restricts to square SEAL:S rows (deduplicated on text,
// site, type, iconography, and shape), and recomputes the Fisher enrichment of 405,
// 806, and either-of-them for Bull1:W under five panels: all rows, rows without the
// literal `740-405-590`, rows without any `740-X-590` frame, rows outside Harappa,
// and both removals combined. Each panel runs a 1,000-iteration Bull1:W
// label-shuffle null whose statistic is the minimum Fisher p over all signs
// (max-stat). The candidate survives only if 405 or 806 stays significant after
// the frame rows are removed. Writes one JSON report to the reports directory.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT = path.join(ROOT, 'data', 'open_prototype', 'reports', 'risky_405806_bull1w_frame_confound_stress_20260531.json');
const ITERATIONS = 1000;

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

function has(row, sign) {
  return toks(row.text).includes(sign);
}

function has740x590(row) {
  const t = toks(row.text);
  for (let i = 0; i < t.length - 2; i += 1) {
    if (t[i] === '740' && t[i + 2] === '590') return true;
  }
  return false;
}

function has740405590(row) {
  return row.text.includes('740-405-590');
}

function collapse(rows) {
  const map = new Map();
  for (const row of rows) {
    const key = `${row.text}|${row.site}|${row.type}|${row.symbol}|${row.shape}`;
    if (!map.has(key)) map.set(key, row);
  }
  return [...map.values()];
}

const logFact = [0];
function lf(n) {
  for (let i = logFact.length; i <= n; i += 1) logFact[i] = logFact[i - 1] + Math.log(i);
  return logFact[n];
}

function fisherRight(a, b, c, d) {
  const r1 = a + b;
  const r2 = c + d;
  const c1 = a + c;
  const c2 = b + d;
  const n = r1 + r2;
  const maxA = Math.min(r1, c1);
  function logHyper(x) {
    return lf(r1) + lf(r2) + lf(c1) + lf(c2) - lf(x) - lf(r1 - x) - lf(c1 - x) - lf(r2 - c1 + x) - lf(n);
  }
  let p = 0;
  for (let x = a; x <= maxA; x += 1) p += Math.exp(logHyper(x));
  return Math.min(1, p);
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

function signIndex(rows) {
  const index = new Map();
  for (let i = 0; i < rows.length; i += 1) {
    for (const sign of new Set(toks(rows[i].text))) {
      if (!index.has(sign)) index.set(sign, []);
      index.get(sign).push(i);
    }
  }
  return index;
}

function minSignP(index, labels, positiveCount, n) {
  let minP = 1;
  for (const indices of index.values()) {
    let a = 0;
    for (const idx of indices) if (labels[idx]) a += 1;
    if (!a) continue;
    const b = positiveCount - a;
    const c = indices.length - a;
    const d = n - positiveCount - c;
    const p = fisherRight(a, b, c, d);
    if (p < minP) minP = p;
  }
  return minP;
}

function targetStats(rows, predicate) {
  const positive = rows.filter((row) => row.symbol === 'Bull1:W');
  const negative = rows.filter((row) => row.symbol !== 'Bull1:W');
  const a = positive.filter(predicate).length;
  const b = positive.length - a;
  const c = negative.filter(predicate).length;
  const d = negative.length - c;
  return { a, b, c, d, fisher_p: fisherRight(a, b, c, d) };
}

function panel(id, filter) {
  const base = collapse(
    rows.filter((row) => row.type === 'SEAL:S' && String(row.shape).toLowerCase() === 'square').filter(filter),
  );
  const labels = base.map((row) => row.symbol === 'Bull1:W');
  const pos = labels.filter(Boolean).length;
  const index = signIndex(base);
  const stats = {
    '405': targetStats(base, (row) => has(row, '405')),
    '806': targetStats(base, (row) => has(row, '806')),
    either: targetStats(base, (row) => has(row, '405') || has(row, '806')),
  };
  const rand = mulberry32(0x405806 + id.length);
  const maxstat = { '405': 0, '806': 0 };
  for (let iter = 0; iter < ITERATIONS; iter += 1) {
    const sim = shuffledLabels(base.length, pos, rand);
    const minP = minSignP(index, sim, pos, base.length);
    for (const sign of ['405', '806']) if (minP <= stats[sign].fisher_p) maxstat[sign] += 1;
  }
  return {
    id,
    rows: base.length,
    bull1w_rows: pos,
    stats: Object.fromEntries(Object.entries(stats).map(([key, value]) => [
      key,
      {
        ...value,
        maxstat_fpr: key === 'either' ? null : maxstat[key] / ITERATIONS,
      },
    ])),
  };
}

const rows = parseCsv(fs.readFileSync(META, 'utf8'));
const panels = [
  panel('square_seal_s_all', () => true),
  panel('remove_740_405_590', (row) => !has740405590(row)),
  panel('remove_any_740_x_590', (row) => !has740x590(row)),
  panel('remove_harappa', (row) => row.site !== 'Harappa'),
  panel('remove_harappa_and_740x590', (row) => row.site !== 'Harappa' && !has740x590(row)),
];

const frameRemoved = panels.find((row) => row.id === 'remove_any_740_x_590');
const decision = frameRemoved.stats['806'].maxstat_fpr <= 0.01 || frameRemoved.stats['405'].maxstat_fpr <= 0.01
  ? 'survives_frame_confound_as_at_least_one_sign'
  : 'demote_bull1w_candidate_as_frame_confounded';

const report = {
  date: '2026-05-31',
  phase: 'CONSOLIDATE',
  candidate_id: 'risky_405806_bull1w_frame_confound_stress_20260531',
  bet: '405/806 Bull1:W enrichment is not only an artifact of the 740-X-590 frame.',
  source: META,
  panels,
  null: {
    iterations: ITERATIONS,
    preserves: 'square SEAL:S row set and Bull1:W label count; shuffles Bull1:W labels for all-sign maxstat',
  },
  decision,
};

fs.writeFileSync(OUT, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({ candidate_id: report.candidate_id, decision, panels }, null, 2));
