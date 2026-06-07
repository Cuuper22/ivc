import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_060_cap_selector_map_20260531';
const CAP_SET = ['920', '692', '550', '820'];
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
  const capTotals = new Map(CAP_SET.map((cap) => [cap, 0]));
  for (let i = 0; i < cells.length; i += 1) {
    const cap = labels ? labels[i] : cells[i].cap;
    capTotals.set(cap, (capTotals.get(cap) ?? 0) + 1);
    if (!byPrev.has(cells[i].prev)) {
      byPrev.set(cells[i].prev, {
        prev: cells[i].prev,
        total: 0,
        caps: new Map(CAP_SET.map((name) => [name, 0])),
        examples: [],
      });
    }
    const row = byPrev.get(cells[i].prev);
    row.total += 1;
    row.caps.set(cap, (row.caps.get(cap) ?? 0) + 1);
    if (!labels && row.examples.length < 8) row.examples.push(`${cells[i].cisi}:${cells[i].prev}-060-${cells[i].cap}:${cells[i].text}`);
  }

  const out = [];
  for (const row of byPrev.values()) {
    if (row.total < MIN_SELECTOR_N) continue;
    for (const cap of CAP_SET) {
      const hit = row.caps.get(cap) ?? 0;
      const miss = row.total - hit;
      if (!hit) continue;
      const otherCapTotal = (capTotals.get(cap) ?? 0) - hit;
      const otherNonCapTotal = cells.length - row.total - otherCapTotal;
      const purity = hit / row.total;
      out.push({
        prev: row.prev,
        target_cap: cap,
        selector_cells: row.total,
        target_hits: hit,
        other_cap_hits: miss,
        purity,
        fisher_right_tail: fisherRight(hit, miss, otherCapTotal, otherNonCapTotal),
        cap_counts: CAP_SET.map((name) => `${name}:${row.caps.get(name) ?? 0}`).join(' '),
        examples: row.examples,
      });
    }
  }
  return out.sort((a, b) => (
    a.fisher_right_tail - b.fisher_right_tail
    || b.purity - a.purity
    || b.selector_cells - a.selector_cells
    || a.prev.localeCompare(b.prev)
    || a.target_cap.localeCompare(b.target_cap)
  ));
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const cellMap = new Map();
for (const row of rows) {
  const toks = tokens(row.text);
  for (let i = 0; i < toks.length - 2; i += 1) {
    const prev = toks[i];
    const mid = toks[i + 1];
    const cap = toks[i + 2];
    if (mid !== '060' || !CAP_SET.includes(cap)) continue;
    const next2 = toks[i + 3] ?? '<END>';
    const key = exactKey([prev, mid, cap, next2, row.text, row.site, row.type, row.symbol]);
    if (!cellMap.has(key)) {
      cellMap.set(key, {
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
}

const cells = [...cellMap.values()];
const liveRows = scoreSelectors(cells);
const liveQualifying = liveRows.filter((row) => row.purity >= MIN_PURITY);
const capLabels = cells.map((cell) => cell.cap);
const rand = mulberry32(0x060CA9);
const targetScore = Math.min(...liveQualifying.map((row) => row.fisher_right_tail));
const targetCount = liveQualifying.length;
let anyMinPGeCount = 0;
let anyMinPLeBest = 0;
let bothGe = 0;

for (let iter = 0; iter < ITERATIONS; iter += 1) {
  const shuffled = fisherYates(capLabels, rand);
  const simulated = scoreSelectors(cells, shuffled).filter((row) => row.purity >= MIN_PURITY);
  const simBest = simulated.length ? Math.min(...simulated.map((row) => row.fisher_right_tail)) : 1;
  if (simulated.length >= targetCount) anyMinPGeCount += 1;
  if (simBest <= targetScore) anyMinPLeBest += 1;
  if (simulated.length >= targetCount && simBest <= targetScore) bothGe += 1;
}

const promoted = liveQualifying.filter((row) => row.selector_cells >= MIN_SELECTOR_N && row.purity >= MIN_PURITY);
const report = {
  date: '2026-05-31',
  phase: 'EXPAND',
  candidate_id: PREFIX,
  tier: 'wild shot_to_candidate_screen',
  bet: 'The sign immediately before 060 is not incidental: within the terminal-cap paradigm it often selects a specific cap, giving a tiny grammar of feeder signs plus 060 plus closure.',
  exact_collapse: {
    source: META,
    cap_set: CAP_SET,
    exact_prev_060_cap_cells: cells.length,
    dedupe_key: ['prev', '060', 'cap', 'next2', 'text', 'site', 'type', 'symbol'],
  },
  qualifying_rule: {
    min_selector_cells: MIN_SELECTOR_N,
    min_purity: MIN_PURITY,
  },
  live_qualifying_selector_count: targetCount,
  live_best_selector_p: targetScore,
  cap_label_shuffle_null: {
    iterations: ITERATIONS,
    preserves: 'prev signs, number of prev-060-cap cells, and cap marginal counts; shuffles cap labels over exact cells',
    p_qualifying_count_ge_live: anyMinPGeCount / ITERATIONS,
    p_best_selector_p_le_live: anyMinPLeBest / ITERATIONS,
    p_both_count_and_best: bothGe / ITERATIONS,
  },
  strongest_selectors: promoted.slice(0, 25),
  risky_new_bets: promoted
    .filter((row) => !['741', '742', '745'].includes(row.prev))
    .slice(0, 10)
    .map((row) => ({
      tier: row.selector_cells >= 6 && row.purity === 1 ? 'candidate' : 'wild shot',
      bet: `${row.prev}-060 predicts cap ${row.target_cap} (${row.target_hits}/${row.selector_cells} exact cells); a new ${row.prev}-060-cap row should choose ${row.target_cap}.`,
      p_uncorrected: row.fisher_right_tail,
      examples: row.examples,
    })),
  demoters: [
    'If exact deduplication by object rather than text family drops the non-741/742/745 selectors below four cells, keep only the 920 feeder alloseries.',
    'If a site-withheld test shows a selector exists only at one excavation site, demote it to local workshop habit rather than script grammar.',
    'If source images split the apparent prev sign into unrelated graphic signs, split the bet before retesting.',
  ],
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
writeCsv(path.join(OUT_DIR, `${PREFIX}_selectors.csv`), liveRows, [
  'prev',
  'target_cap',
  'selector_cells',
  'target_hits',
  'other_cap_hits',
  'purity',
  'fisher_right_tail',
  'cap_counts',
]);

console.log(JSON.stringify({
  candidate_id: PREFIX,
  live_qualifying_selector_count: targetCount,
  live_best_selector_p: targetScore,
  null: report.cap_label_shuffle_null,
  top_selectors: promoted.slice(0, 12).map((row) => ({
    prev: row.prev,
    target_cap: row.target_cap,
    selector_cells: row.selector_cells,
    target_hits: row.target_hits,
    purity: row.purity,
    p: row.fisher_right_tail,
    cap_counts: row.cap_counts,
  })),
  risky_new_bets: report.risky_new_bets,
}, null, 2));
