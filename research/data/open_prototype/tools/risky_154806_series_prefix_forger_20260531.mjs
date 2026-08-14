// Tests whether the bigram `154-806` is a "series prefix": a fixed opener whose next
// slot is filled from a narrow family of signs numbered 467 through 474. If true,
// sign 806 would need to be split by construction, since elsewhere it acts as a
// boundary or closure pivot. The script reads metadata_filtered.csv (complete rows
// only), gathers the sign after every `154-806` occurrence, and counts hits inside
// the 467..474 window. To be fair to rival explanations, every bigram with at least
// as much support competes: each gets its own best width-8 numeric successor window,
// and 154-806 is ranked by best-window share. A 5,000-iteration null resamples
// successors from the observed pool for every competitor and asks how often any
// bigram-window combination matches the observed share and hit count (a max-stat
// over bigrams and windows). Witnesses are also deduplicated and broken down by
// site to expose Harappa dominance. Writes witness and competitor CSVs plus a JSON
// summary to the reports directory.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_154806_series_prefix_forger_20260531';
const RUN_DATE = '2026-05-31';
const TARGET_BIGRAM = '154-806';
const WINDOW_START = 467;
const WINDOW_END = 474;
const WINDOW_WIDTH = WINDOW_END - WINDOW_START + 1;
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

function tokenNum(token) {
  return /^\d{3}$/.test(token) ? Number(token) : null;
}

function esc(value) {
  const text = String(value ?? '');
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const body = rows.map((row) => fields.map((field) => esc(row[field])).join(',')).join('\n');
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`, 'utf8');
}

function bestWindow(values, width = WINDOW_WIDTH) {
  const counts = new Array(1000).fill(0);
  let numericN = 0;
  for (const value of values) {
    const n = tokenNum(value);
    if (n !== null && n >= 0 && n < counts.length) {
      counts[n] += 1;
      numericN += 1;
    }
  }
  let rolling = 0;
  let best = { start: 0, end: width - 1, hit: 0, numericN };
  for (let i = 0; i < counts.length; i += 1) {
    rolling += counts[i];
    if (i >= width) rolling -= counts[i - width];
    if (i >= width - 1 && rolling > best.hit) {
      best = { start: i - width + 1, end: i, hit: rolling, numericN };
    }
  }
  return best;
}

const rows = parseCsv(fs.readFileSync(META, 'utf8'))
  .filter((row) => row.complete === 'Y')
  .map((row) => ({ ...row, toks: tokens(row.text) }));

const bigramNext = new Map();
for (const row of rows) {
  for (let i = 0; i < row.toks.length - 1; i += 1) {
    const bg = `${row.toks[i]}-${row.toks[i + 1]}`;
    const next = row.toks[i + 2] ?? '<END>';
    if (!bigramNext.has(bg)) bigramNext.set(bg, []);
    bigramNext.get(bg).push({ row, next });
  }
}

const target = bigramNext.get(TARGET_BIGRAM) ?? [];
const targetSuccessors = target.map((item) => item.next);
const targetHits = targetSuccessors.filter((value) => {
  const n = tokenNum(value);
  return n !== null && n >= WINDOW_START && n <= WINDOW_END;
}).length;
const observedShare = targetHits / target.length;

const competitors = [...bigramNext.entries()]
  .filter(([, items]) => items.length >= target.length)
  .map(([bigram, items]) => {
    const values = items.map((item) => item.next);
    const best = bestWindow(values);
    return {
      bigram,
      n: items.length,
      best_window_start: String(best.start).padStart(3, '0'),
      best_window_end: String(best.end).padStart(3, '0'),
      best_hit: best.hit,
      best_share: best.hit / items.length,
      numeric_successors: best.numericN,
    };
  })
  .sort((a, b) => b.best_share - a.best_share || b.best_hit - a.best_hit || a.n - b.n);

const targetRank = competitors.findIndex((item) => item.bigram === TARGET_BIGRAM) + 1;
const successorPool = [...bigramNext.values()].flatMap((items) => items.map((item) => item.next));
const competitorSizes = competitors.map((item) => item.n);

let nullGeObserved = 0;
let nullMaxShareSum = 0;
let nullMaxHitSum = 0;
for (let iter = 0; iter < ITERATIONS; iter += 1) {
  let iterBestShare = 0;
  let iterBestHit = 0;
  for (const n of competitorSizes) {
    const sampled = new Array(n);
    for (let j = 0; j < n; j += 1) {
      sampled[j] = successorPool[Math.floor(Math.random() * successorPool.length)];
    }
    const best = bestWindow(sampled);
    const share = best.hit / n;
    if (share > iterBestShare || (share === iterBestShare && best.hit > iterBestHit)) {
      iterBestShare = share;
      iterBestHit = best.hit;
    }
  }
  nullMaxShareSum += iterBestShare;
  nullMaxHitSum += iterBestHit;
  if (iterBestShare >= observedShare && iterBestHit >= targetHits) nullGeObserved += 1;
}

const witnesses = target.map(({ row, next }) => ({
  cisi: row.cisi,
  id: row.id,
  site: row.site,
  type: row.type,
  symbol: row.symbol,
  text: row.text,
  successor_after_154_806: next,
  in_467_474_family: tokenNum(next) !== null && tokenNum(next) >= WINDOW_START && tokenNum(next) <= WINDOW_END ? 'yes' : 'no',
}));

const exactDedup = new Map();
for (const item of witnesses) {
  const key = `${item.text}|${item.site}|${item.type}|${item.symbol}`;
  if (!exactDedup.has(key)) exactDedup.set(key, item);
}
const dedupWitnesses = [...exactDedup.values()];
const siteBreakdown = [...witnesses.reduce((acc, item) => {
  if (!acc.has(item.site)) acc.set(item.site, { site: item.site, n: 0, hits: 0 });
  const entry = acc.get(item.site);
  entry.n += 1;
  if (item.in_467_474_family === 'yes') entry.hits += 1;
  return acc;
}, new Map()).values()].sort((a, b) => b.n - a.n || a.site.localeCompare(b.site));

const summary = {
  date: RUN_DATE,
  candidate_id: PREFIX,
  tier: 'candidate',
  bet: '154-806 is a constructional series-prefix whose next slot selects a narrow 467..474 sign family; this would split 806 by construction, because the same sign also behaves as a boundary/closure pivot elsewhere.',
  target: {
    bigram: TARGET_BIGRAM,
    successor_window: `${String(WINDOW_START).padStart(3, '0')}..${String(WINDOW_END).padStart(3, '0')}`,
    raw_occurrences: target.length,
    raw_hits_in_window: targetHits,
    raw_share: observedShare,
    exact_text_site_type_symbol_dedup_occurrences: dedupWitnesses.length,
    exact_dedup_hits_in_window: dedupWitnesses.filter((item) => item.in_467_474_family === 'yes').length,
    site_breakdown: siteBreakdown,
    non_harappa_occurrences: witnesses.filter((item) => item.site !== 'Harappa').length,
    non_harappa_hits_in_window: witnesses.filter((item) => item.site !== 'Harappa' && item.in_467_474_family === 'yes').length,
  },
  all_bigram_all_window_maxstat: {
    competitor_bigrams_with_support_at_least_target: competitors.length,
    target_rank_by_best_window_share: targetRank,
    target_best_window_hit_ranked: competitors[targetRank - 1],
    top_competitors: competitors.slice(0, 10),
  },
  successor_label_shuffle_null: {
    iterations: ITERATIONS,
    preserves: 'bigram support sizes for all competitors; samples successor labels from the observed successor pool; every width-8 numeric successor window competes in every null draw',
    mean_null_max_share: Number((nullMaxShareSum / ITERATIONS).toFixed(6)),
    mean_null_max_hit: Number((nullMaxHitSum / ITERATIONS).toFixed(6)),
    p_ge_observed_share_and_hit: nullGeObserved / ITERATIONS,
  },
  scope_warning: 'Most witnesses are Harappa SEAL:R/None, but the same construction also appears on H-27/H-1999/H-1788 and four non-Harappa rows; source-image validation and exact-copy/family collapse are still required before acceptance.',
  decision: null,
};

summary.decision = summary.successor_label_shuffle_null.p_ge_observed_share_and_hit <= 0.01
  ? 'candidate_survives_first_maxstat_forger'
  : 'candidate_demoted_by_maxstat_forger';

fs.mkdirSync(OUT_DIR, { recursive: true });
writeCsv(path.join(OUT_DIR, `${PREFIX}_witnesses.csv`), witnesses, [
  'cisi', 'id', 'site', 'type', 'symbol', 'text', 'successor_after_154_806', 'in_467_474_family',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_competitors.csv`), competitors, [
  'bigram', 'n', 'best_window_start', 'best_window_end', 'best_hit', 'best_share', 'numeric_successors',
]);
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
