import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_002_closure_selector_map_20260531';
const CLOSURE_SET = ['817', '820', '861'];
const ITERATIONS = 5000;
const MIN_SELECTOR_N = 4;
const MIN_PURITY = 0.75;

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

function exactKey(parts) {
  return parts.join('|');
}

function esc(value) {
  const text = Array.isArray(value) ? value.join(' | ') : String(value ?? '');
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const body = rows.map((row) => fields.map((field) => esc(row[field])).join(',')).join('\n');
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`, 'utf8');
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

function scoreSelectors(cells, labels = null) {
  const byPrev = new Map();
  const closureTotals = new Map(CLOSURE_SET.map((closure) => [closure, 0]));
  for (let i = 0; i < cells.length; i += 1) {
    const closure = labels ? labels[i] : cells[i].closure;
    closureTotals.set(closure, (closureTotals.get(closure) ?? 0) + 1);
    if (!byPrev.has(cells[i].prev)) {
      byPrev.set(cells[i].prev, {
        prev: cells[i].prev,
        total: 0,
        closures: new Map(CLOSURE_SET.map((name) => [name, 0])),
        examples: [],
      });
    }
    const row = byPrev.get(cells[i].prev);
    row.total += 1;
    row.closures.set(closure, (row.closures.get(closure) ?? 0) + 1);
    if (!labels && row.examples.length < 8) row.examples.push(`${cells[i].cisi}:${cells[i].prev}-002-${cells[i].closure}:${cells[i].text}`);
  }

  const out = [];
  for (const row of byPrev.values()) {
    if (row.total < MIN_SELECTOR_N) continue;
    for (const closure of CLOSURE_SET) {
      const hit = row.closures.get(closure) ?? 0;
      const miss = row.total - hit;
      if (!hit) continue;
      const otherClosureTotal = (closureTotals.get(closure) ?? 0) - hit;
      const otherNonClosureTotal = cells.length - row.total - otherClosureTotal;
      out.push({
        prev: row.prev,
        target_closure: closure,
        selector_cells: row.total,
        target_hits: hit,
        other_closure_hits: miss,
        purity: hit / row.total,
        fisher_right_tail: fisherRight(hit, miss, otherClosureTotal, otherNonClosureTotal),
        closure_counts: CLOSURE_SET.map((name) => `${name}:${row.closures.get(name) ?? 0}`).join(' '),
        examples: row.examples,
      });
    }
  }
  return out.sort((a, b) => (
    a.fisher_right_tail - b.fisher_right_tail
    || b.purity - a.purity
    || b.selector_cells - a.selector_cells
    || a.prev.localeCompare(b.prev)
    || a.target_closure.localeCompare(b.target_closure)
  ));
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const cellMap = new Map();
for (const row of rows) {
  const toks = tokens(row.text);
  for (let i = 0; i < toks.length - 2; i += 1) {
    const prev = toks[i];
    const mid = toks[i + 1];
    const closure = toks[i + 2];
    if (mid !== '002' || !CLOSURE_SET.includes(closure)) continue;
    const next2 = toks[i + 3] ?? '<END>';
    const key = exactKey([prev, mid, closure, next2, row.text, row.site, row.type, row.symbol]);
    if (!cellMap.has(key)) {
      cellMap.set(key, {
        prev,
        closure,
        next2,
        cisi: row.cisi,
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        text: row.text,
      });
    }
  }
}

const cells = [...cellMap.values()];
const liveRows = scoreSelectors(cells);
const liveQualifying = liveRows.filter((row) => row.purity >= MIN_PURITY);
const labels = cells.map((cell) => cell.closure);
const rand = mulberry32(0x002817);
const targetScore = liveQualifying.length ? Math.min(...liveQualifying.map((row) => row.fisher_right_tail)) : 1;
const targetCount = liveQualifying.length;
let countGe = 0;
let bestLe = 0;
let both = 0;

for (let iter = 0; iter < ITERATIONS; iter += 1) {
  const shuffled = fisherYates(labels, rand);
  const simulated = scoreSelectors(cells, shuffled).filter((row) => row.purity >= MIN_PURITY);
  const simBest = simulated.length ? Math.min(...simulated.map((row) => row.fisher_right_tail)) : 1;
  if (simulated.length >= targetCount) countGe += 1;
  if (simBest <= targetScore) bestLe += 1;
  if (simulated.length >= targetCount && simBest <= targetScore) both += 1;
}

const report = {
  date: '2026-05-31',
  phase: 'EXPAND',
  candidate_id: PREFIX,
  tier: targetCount ? 'candidate_screen' : 'wild_shot_killed',
  bet: 'If 002 has a closure paradigm parallel to 060, immediate left-neighbor signs should sometimes select 817, 820, or leaky 861.',
  exact_collapse: {
    source: META,
    closure_set: CLOSURE_SET,
    exact_prev_002_closure_cells: cells.length,
    dedupe_key: ['prev', '002', 'closure', 'next2', 'text', 'site', 'type', 'symbol'],
  },
  qualifying_rule: {
    min_selector_cells: MIN_SELECTOR_N,
    min_purity: MIN_PURITY,
  },
  live_qualifying_selector_count: targetCount,
  live_best_selector_p: targetScore,
  closure_label_shuffle_null: {
    iterations: ITERATIONS,
    preserves: 'prev signs, number of prev-002-closure cells, and closure marginal counts; shuffles closure labels over exact cells',
    p_qualifying_count_ge_live: countGe / ITERATIONS,
    p_best_selector_p_le_live: bestLe / ITERATIONS,
    p_both_count_and_best: both / ITERATIONS,
  },
  strongest_selectors: liveQualifying.slice(0, 25),
  risky_bets: liveQualifying.slice(0, 12).map((row) => ({
    tier: row.selector_cells >= 6 && row.purity === 1 ? 'candidate' : 'wild shot',
    bet: `${row.prev}-002 predicts closure ${row.target_closure} (${row.target_hits}/${row.selector_cells} exact cells).`,
    p_uncorrected: row.fisher_right_tail,
    examples: row.examples,
  })),
  demoters: [
    'If leave-site testing erases the selector, demote it to local workshop habit.',
    'If exact duplicate families dominate a selector, demote until object-level dedupe is run.',
    'If the selector count is null-common, do not parallelize the 060 feeder model to 002.',
  ],
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
writeCsv(path.join(OUT_DIR, `${PREFIX}_selectors.csv`), liveRows, [
  'prev',
  'target_closure',
  'selector_cells',
  'target_hits',
  'other_closure_hits',
  'purity',
  'fisher_right_tail',
  'closure_counts',
]);

console.log(JSON.stringify({
  candidate_id: PREFIX,
  live_qualifying_selector_count: targetCount,
  live_best_selector_p: targetScore,
  null: report.closure_label_shuffle_null,
  top_selectors: liveQualifying.slice(0, 12).map((row) => ({
    prev: row.prev,
    target_closure: row.target_closure,
    selector_cells: row.selector_cells,
    target_hits: row.target_hits,
    purity: row.purity,
    p: row.fisher_right_tail,
    closure_counts: row.closure_counts,
  })),
  risky_bets: report.risky_bets,
}, null, 2));
