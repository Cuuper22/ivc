import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_060920_selector_object_site_stress_20260531';
const CAP_SET = ['920', '692', '550', '820'];
const SELECTOR_SET = new Set(['741', '742', '745']);
const ITERATIONS = 5000;

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

function score(cells, labels = null) {
  let target = 0;
  let targetSelector = 0;
  let siblings = 0;
  let siblingSelector = 0;
  for (let i = 0; i < cells.length; i += 1) {
    const cap = labels ? labels[i] : cells[i].cap;
    const selected = SELECTOR_SET.has(cells[i].prev);
    if (cap === '920') {
      target += 1;
      if (selected) targetSelector += 1;
    } else {
      siblings += 1;
      if (selected) siblingSelector += 1;
    }
  }
  return {
    cells: cells.length,
    target_920_cells: target,
    sibling_cap_cells: siblings,
    selector_hits_in_920: targetSelector,
    selector_misses_in_920: target - targetSelector,
    selector_hits_in_siblings: siblingSelector,
    selector_misses_in_siblings: siblings - siblingSelector,
    hit_share_920: target ? targetSelector / target : 0,
    hit_share_siblings: siblings ? siblingSelector / siblings : 0,
    fisher_right_tail: fisherRight(targetSelector, target - targetSelector, siblingSelector, siblings - siblingSelector),
  };
}

function collect(rows, collapse) {
  const seen = new Set();
  const cells = [];
  for (const row of rows) {
    const toks = tokens(row.text);
    for (let i = 0; i < toks.length - 2; i += 1) {
      const prev = toks[i];
      const mid = toks[i + 1];
      const cap = toks[i + 2];
      if (mid !== '060' || !CAP_SET.includes(cap)) continue;
      const next2 = toks[i + 3] ?? '<END>';
      const key = collapse === 'object'
        ? `${row.cisi}|${prev}|060|${cap}|${next2}`
        : `${row.text}|${prev}|060|${cap}|${next2}`;
      if (seen.has(key)) continue;
      seen.add(key);
      cells.push({
        prev,
        cap,
        next2,
        cisi: row.cisi,
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        text: row.text,
      });
    }
  }
  return cells;
}

function shuffleNull(cells, live) {
  const labels = cells.map((cell) => cell.cap);
  const rand = mulberry32(0x60920);
  let hitGe = 0;
  let leakLe = 0;
  let both = 0;
  let pLe = 0;
  for (let iter = 0; iter < ITERATIONS; iter += 1) {
    const shuffled = fisherYates(labels, rand);
    const sim = score(cells, shuffled);
    if (sim.selector_hits_in_920 >= live.selector_hits_in_920) hitGe += 1;
    if (sim.selector_hits_in_siblings <= live.selector_hits_in_siblings) leakLe += 1;
    if (sim.selector_hits_in_920 >= live.selector_hits_in_920 && sim.selector_hits_in_siblings <= live.selector_hits_in_siblings) both += 1;
    if (sim.fisher_right_tail <= live.fisher_right_tail) pLe += 1;
  }
  return {
    iterations: ITERATIONS,
    p_selector_hits_ge_live: hitGe / ITERATIONS,
    p_sibling_leaks_le_live: leakLe / ITERATIONS,
    p_hits_and_leaks: both / ITERATIONS,
    p_fisher_le_live: pLe / ITERATIONS,
  };
}

const allRows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const panels = [];
for (const collapse of ['object', 'text_family']) {
  for (const leaveSite of ['NONE', 'Mohenjo-daro', 'Harappa']) {
    const subset = leaveSite === 'NONE' ? allRows : allRows.filter((row) => row.site !== leaveSite);
    const cells = collect(subset, collapse);
    const live = score(cells);
    panels.push({
      collapse,
      leave_site: leaveSite,
      live,
      null: leaveSite === 'NONE' ? shuffleNull(cells, live) : null,
      selector_examples: cells
        .filter((cell) => cell.cap === '920' && SELECTOR_SET.has(cell.prev))
        .slice(0, 10)
        .map((cell) => `${cell.cisi}:${cell.prev}-060-${cell.cap}:${cell.text}`),
      sibling_leak_examples: cells
        .filter((cell) => cell.cap !== '920' && SELECTOR_SET.has(cell.prev))
        .slice(0, 10)
        .map((cell) => `${cell.cisi}:${cell.prev}-060-${cell.cap}:${cell.text}`),
    });
  }
}

const objectNone = panels.find((row) => row.collapse === 'object' && row.leave_site === 'NONE');
const textNone = panels.find((row) => row.collapse === 'text_family' && row.leave_site === 'NONE');
const report = {
  date: '2026-05-31',
  phase: 'CONSOLIDATE',
  candidate_id: PREFIX,
  tier: 'promoted_candidate_strengthener',
  bet: 'The 741/742/745 feeder alloseries selects 060-920 rather than sibling 060 caps, and this survives object/text-family collapse plus leave-site stress.',
  source: META,
  selector_set: [...SELECTOR_SET],
  cap_set: CAP_SET,
  panels,
  decision: objectNone.live.selector_hits_in_siblings === 0
    && textNone.live.selector_hits_in_siblings === 0
    ? 'selector_survives_object_text_family_and_site_stress'
    : 'selector_demoted_by_leakage_under_collapse',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({
  candidate_id: PREFIX,
  decision: report.decision,
  object: objectNone,
  text_family: textNone,
  leave_site: panels.filter((row) => row.leave_site !== 'NONE').map((row) => ({
    collapse: row.collapse,
    leave_site: row.leave_site,
    live: row.live,
  })),
}, null, 2));
