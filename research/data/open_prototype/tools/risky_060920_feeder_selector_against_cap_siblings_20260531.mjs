import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_060920_feeder_selector_against_cap_siblings_20260531';
const RUN_DATE = '2026-05-31';
const CAP_SET = ['920', '692', '550', '820'];
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

function topPrevSelector(cells, cap, labels = null) {
  const inRows = [];
  const outRows = [];
  for (let i = 0; i < cells.length; i += 1) {
    const label = labels ? labels[i] : cells[i].cap;
    if (label === cap) inRows.push(cells[i]);
    else outRows.push(cells[i]);
  }
  const counts = new Map();
  for (const row of inRows) counts.set(row.prev, (counts.get(row.prev) ?? 0) + 1);
  const top3 = [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, 3)
    .map(([prev]) => prev);
  const topSet = new Set(top3);
  const inHit = inRows.filter((row) => topSet.has(row.prev)).length;
  const outHit = outRows.filter((row) => topSet.has(row.prev)).length;
  return {
    cap,
    top3_prev: top3.join(' '),
    in_exact_cells: inRows.length,
    out_exact_cells: outRows.length,
    in_top3_hits: inHit,
    in_top3_misses: inRows.length - inHit,
    out_top3_hits: outHit,
    out_top3_misses: outRows.length - outHit,
    fisher_right_tail: fisherRight(inHit, inRows.length - inHit, outHit, outRows.length - outHit),
    examples: inRows.filter((row) => topSet.has(row.prev)).slice(0, 8).map((row) => `${row.cisi}:${row.prev}-060-${row.cap}:${row.text}`),
  };
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
        is_terminal: next2 === '<END>',
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        text: row.text,
        cisi: row.cisi,
      });
    }
  }
}

const cells = [...cellMap.values()];
const selectorRows = CAP_SET.map((cap) => topPrevSelector(cells, cap))
  .sort((a, b) => b.in_top3_hits - a.in_top3_hits || a.out_top3_hits - b.out_top3_hits || a.fisher_right_tail - b.fisher_right_tail);

const target = selectorRows.find((row) => row.cap === '920');
const capLabels = cells.map((cell) => cell.cap);
const rand = mulberry32(0x060920);
let maxstatGeTarget = 0;
let fixed920GeTarget = 0;

for (let iter = 0; iter < ITERATIONS; iter += 1) {
  const shuffled = fisherYates(capLabels, rand);
  const simulated = CAP_SET.map((cap) => topPrevSelector(cells, cap, shuffled));
  const fixed920 = simulated.find((row) => row.cap === '920');
  if (fixed920.in_top3_hits >= target.in_top3_hits && fixed920.out_top3_hits <= target.out_top3_hits) {
    fixed920GeTarget += 1;
  }
  if (simulated.some((row) => row.in_top3_hits >= target.in_top3_hits && row.out_top3_hits <= target.out_top3_hits)) {
    maxstatGeTarget += 1;
  }
}

const report = {
  date: RUN_DATE,
  phase: 'EXPAND',
  candidate_id: PREFIX,
  tier: 'candidate',
  bet: 'Inside the 060 terminal-cap paradigm, 920 is the marked cap selected by a left-feeder alloseries 741/742/745. The sibling caps 692, 550, and 820 are broad caps without that feeder. This makes 741/742/745-060-920 a slot grammar, not merely a frequent trigram.',
  exact_collapse: {
    source: META,
    cap_set: CAP_SET,
    exact_prev_060_cap_cells: cells.length,
    dedupe_key: ['prev', '060', 'cap', 'next2', 'text', 'site', 'type', 'symbol'],
  },
  target_920_selector: target,
  cap_sibling_comparator: selectorRows,
  cap_label_shuffle_null: {
    iterations: ITERATIONS,
    preserves: 'prev signs and row metadata in the prev-060-cap universe; shuffles cap labels while preserving cap counts',
    fixed_920_p_ge_target_hits_and_no_sibling_leak: fixed920GeTarget / ITERATIONS,
    maxstat_p_any_cap_ge_target_hits_and_no_sibling_leak: maxstatGeTarget / ITERATIONS,
  },
  predictions: [
    'A new exact prev-060-920 row is much more likely than sibling cap rows to have prev in 741/742/745.',
    'A new 741/742/745-060-cap row should overwhelmingly choose cap 920, not 692/550/820.',
    'If source images merge 741/742/745 as allographs, the claim strengthens as one feeder sign; if they split with different contexts, the claim becomes a feeder alloseries.',
  ],
  demoters: [
    'Demote if source-level sign review shows 741/742/745 are not reliable signs in the relevant rows.',
    'Demote if sibling cap rows with 741/742/745 appear under source-normalized review.',
    'Demote if a broader cap set makes the 741/742/745 selector leak into other caps at comparable rates.',
  ],
  decision: target.in_top3_hits >= 40 && target.out_top3_hits === 0 && maxstatGeTarget === 0
    ? 'candidate_survives_sibling_cap_selector_test'
    : 'wild_shot_until_selector_is_less_posthoc',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
writeCsv(path.join(OUT_DIR, `${PREFIX}_selector_comparator.csv`), selectorRows, [
  'cap',
  'top3_prev',
  'in_exact_cells',
  'out_exact_cells',
  'in_top3_hits',
  'in_top3_misses',
  'out_top3_hits',
  'out_top3_misses',
  'fisher_right_tail',
  'examples',
]);

console.log(JSON.stringify({
  candidate_id: PREFIX,
  decision: report.decision,
  target: report.target_920_selector,
  null: report.cap_label_shuffle_null,
  selectorRows,
}, null, 2));
