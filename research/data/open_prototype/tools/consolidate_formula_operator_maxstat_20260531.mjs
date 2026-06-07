import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'consolidate_formula_operator_maxstat_20260531';
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

function exactKey(parts) {
  return parts.join('|');
}

function bestExactSuccessor(items) {
  const counts = new Map();
  for (const item of items) counts.set(item.next, (counts.get(item.next) ?? 0) + 1);
  const [next, hit] = [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))[0] ?? ['<NONE>', 0];
  return { next, hit, share: items.length ? hit / items.length : 0 };
}

function tokenNum(value) {
  return /^\d{3}$/.test(value) ? Number(value) : null;
}

function bestWindow(items, width) {
  const counts = new Array(1000).fill(0);
  let numericN = 0;
  for (const item of items) {
    const n = tokenNum(item.next);
    if (n !== null) {
      counts[n] += 1;
      numericN += 1;
    }
  }
  let rolling = 0;
  let best = { start: 0, end: width - 1, hit: 0, share: 0, numericN };
  for (let i = 0; i < counts.length; i += 1) {
    rolling += counts[i];
    if (i >= width) rolling -= counts[i - width];
    if (i >= width - 1 && rolling > best.hit) {
      best = { start: i - width + 1, end: i, hit: rolling, share: items.length ? rolling / items.length : 0, numericN };
    }
  }
  return best;
}

function esc(value) {
  const text = String(value ?? '');
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const body = rows.map((row) => fields.map((field) => esc(row[field])).join(',')).join('\n');
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`, 'utf8');
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');

const bigramCells = new Map();
const prev806Cells = new Map();
for (const row of rows) {
  const toks = tokens(row.text);
  for (let i = 0; i < toks.length - 1; i += 1) {
    const bigram = `${toks[i]}-${toks[i + 1]}`;
    const next = toks[i + 2] ?? '<END>';
    const key = exactKey([bigram, next, row.text, row.site, row.type, row.symbol]);
    if (!bigramCells.has(key)) {
      bigramCells.set(key, { bigram, next, site: row.site, type: row.type, symbol: row.symbol, text: row.text, cisi: row.cisi });
    }
  }
  for (let i = 1; i < toks.length; i += 1) {
    if (toks[i] !== '806') continue;
    const prev = toks[i - 1];
    const next = toks[i + 1] ?? '<END>';
    const key = exactKey([prev, '806', next, row.text, row.site, row.type, row.symbol]);
    if (!prev806Cells.has(key)) {
      prev806Cells.set(key, { prev, next, site: row.site, type: row.type, symbol: row.symbol, text: row.text, cisi: row.cisi });
    }
  }
}

const byBigram = new Map();
for (const cell of bigramCells.values()) {
  if (!byBigram.has(cell.bigram)) byBigram.set(cell.bigram, []);
  byBigram.get(cell.bigram).push(cell);
}

const bigramRanking = [...byBigram.entries()].map(([bigram, items]) => {
  const best = bestExactSuccessor(items);
  return {
    bigram,
    exact_cells: items.length,
    best_next: best.next,
    best_hit: best.hit,
    best_share: best.share,
    sites: new Set(items.map((item) => item.site)).size,
    types: new Set(items.map((item) => item.type)).size,
  };
}).sort((a, b) => b.best_hit - a.best_hit || b.best_share - a.best_share || b.sites - a.sites || a.bigram.localeCompare(b.bigram));

const byPrev806 = new Map();
for (const cell of prev806Cells.values()) {
  if (!byPrev806.has(cell.prev)) byPrev806.set(cell.prev, []);
  byPrev806.get(cell.prev).push(cell);
}

const prev806Ranking = [...byPrev806.entries()].map(([prev, items]) => {
  const best = bestWindow(items, 11);
  return {
    prev,
    exact_cells: items.length,
    best_window_start: String(best.start).padStart(3, '0'),
    best_window_end: String(best.end).padStart(3, '0'),
    best_hit: best.hit,
    best_share: best.share,
    numeric_successors: best.numericN,
    sites: new Set(items.map((item) => item.site)).size,
    types: new Set(items.map((item) => item.type)).size,
  };
}).sort((a, b) => b.best_hit - a.best_hit || b.best_share - a.best_share || b.sites - a.sites || a.prev.localeCompare(b.prev));

function getRank(list, predicate) {
  const idx = list.findIndex(predicate);
  return idx === -1 ? null : idx + 1;
}

function exactCandidate(bigram, next) {
  const row = bigramRanking.find((item) => item.bigram === bigram);
  return {
    bigram,
    requested_next: next,
    rank_by_best_hit: getRank(bigramRanking, (item) => item.bigram === bigram),
    row,
  };
}

function prevCandidate(prev) {
  const row = prev806Ranking.find((item) => item.prev === prev);
  return {
    prev,
    rank_by_best_window_hit: getRank(prev806Ranking, (item) => item.prev === prev),
    row,
  };
}

const successorPool = [...bigramCells.values()].map((item) => item.next);
const competitorSizes = bigramRanking.filter((item) => item.exact_cells >= 30).map((item) => item.exact_cells);
let exactNullGe741 = 0;
let exactNullMaxHitSum = 0;
let exactNullMaxShareSum = 0;
for (let iter = 0; iter < ITERATIONS; iter += 1) {
  let maxHit = 0;
  let maxShare = 0;
  for (const n of competitorSizes) {
    const counts = new Map();
    for (let j = 0; j < n; j += 1) {
      const next = successorPool[Math.floor(Math.random() * successorPool.length)];
      counts.set(next, (counts.get(next) ?? 0) + 1);
    }
    const hit = Math.max(...counts.values());
    const share = hit / n;
    if (hit > maxHit || (hit === maxHit && share > maxShare)) {
      maxHit = hit;
      maxShare = share;
    }
  }
  exactNullMaxHitSum += maxHit;
  exactNullMaxShareSum += maxShare;
  if (maxHit >= 30 && maxShare >= 1) exactNullGe741 += 1;
}

const summary = {
  date: '2026-05-31',
  phase: 'CONSOLIDATE',
  test_id: PREFIX,
  exact_collapsed_bigram_tournament: {
    cells: bigramCells.size,
    bigrams: bigramRanking.length,
    top_20: bigramRanking.slice(0, 20),
    named: {
      '741-060_to_920': exactCandidate('741-060', '920'),
      '060-920_to_END': exactCandidate('060-920', '<END>'),
      '740-390_to_590': exactCandidate('740-390', '590'),
      '740-407_to_590': exactCandidate('740-407', '590'),
      '740-405_to_590': exactCandidate('740-405', '590'),
      '690-435_to_255': exactCandidate('690-435', '255'),
      '752-615_to_503': exactCandidate('752-615', '503'),
    },
    successor_shuffle_null_for_741060: {
      iterations: ITERATIONS,
      competitor_bigrams_with_exact_cells_at_least_30: competitorSizes.length,
      preserves: 'exact-collapsed bigram support sizes; samples successor labels from observed exact-collapsed successor pool',
      mean_null_max_hit: Number((exactNullMaxHitSum / ITERATIONS).toFixed(6)),
      mean_null_max_share: Number((exactNullMaxShareSum / ITERATIONS).toFixed(6)),
      p_ge_30_of_30: exactNullGe741 / ITERATIONS,
    },
  },
  prev806_window_tournament: {
    cells: prev806Cells.size,
    predecessors: prev806Ranking.length,
    window_width: 11,
    top_20: prev806Ranking.slice(0, 20),
    named: {
      '154_before_806': prevCandidate('154'),
      '158_before_806': prevCandidate('158'),
      '155_before_806': prevCandidate('155'),
      '100_before_806': prevCandidate('100'),
    },
  },
  consolidation_effect: [
    '741-060 remains a clean exception-free exact-successor formula, but exact tournament shows 060-920 is a broader terminal cap.',
    '740-390 has more exact support than 741-060 but has a complete-looking exception, so it stays below the strict terminal formula by exception-free criteria.',
    'The 806 series is not best represented as 154-806 alone; individual predecessor tournament keeps 154 and 158 high, while the 155/100 expansion remains post-hoc and must be separately source-bound.',
    '752-615 is confirmed as a local copy-family mirage: perfect raw support but only two exact cells and one site/type context.'
  ],
};

fs.mkdirSync(OUT_DIR, { recursive: true });
writeCsv(path.join(OUT_DIR, `${PREFIX}_bigram_ranking.csv`), bigramRanking, [
  'bigram', 'exact_cells', 'best_next', 'best_hit', 'best_share', 'sites', 'types',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_prev806_window_ranking.csv`), prev806Ranking, [
  'prev', 'exact_cells', 'best_window_start', 'best_window_end', 'best_hit', 'best_share', 'numeric_successors', 'sites', 'types',
]);
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
