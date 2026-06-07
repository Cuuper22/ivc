import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_806_prefix_series_geographic_holdout_20260531';
const RUN_DATE = '2026-05-31';
const TRAINED_PREFIX_SIGNS = new Set(['154', '158']);
const EXTENSION_PREFIX_SIGNS = new Set(['154', '155', '158', '100']);
const WINDOW_START = 465;
const WINDOW_END = 475;

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

function tokenNum(value) {
  return /^\d{3}$/.test(value) ? Number(value) : null;
}

function inWindow(value) {
  const n = tokenNum(value);
  return n !== null && n >= WINDOW_START && n <= WINDOW_END;
}

function esc(value) {
  const text = String(value ?? '');
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
  const maxA = Math.min(row1, col1);
  let p = 0;
  for (let x = a; x <= maxA; x += 1) {
    p += Math.exp(
      logChoose(logFact, col1, x)
      + logChoose(logFact, total - col1, row1 - x)
      - logChoose(logFact, total, row1),
    );
  }
  return p;
}

function summarizeBlock(items, prefixSet) {
  const target = items.filter((item) => prefixSet.has(item.prev));
  const control = items.filter((item) => !prefixSet.has(item.prev));
  const targetHits = target.filter((item) => inWindow(item.next)).length;
  const controlHits = control.filter((item) => inWindow(item.next)).length;
  return {
    target_n: target.length,
    target_hits_465_475: targetHits,
    control_n: control.length,
    control_hits_465_475: controlHits,
    fisher_right_tail: fisherRight(
      targetHits,
      target.length - targetHits,
      controlHits,
      control.length - controlHits,
    ),
  };
}

function exactCollapse(items) {
  return [...new Map(items.map((item) => [
    `${item.text}|${item.site}|${item.type}|${item.symbol}|${item.prev}|${item.next}`,
    item,
  ])).values()];
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const occurrences = [];
for (const row of rows) {
  const toks = tokens(row.text);
  for (let i = 1; i < toks.length; i += 1) {
    if (toks[i] !== '806') continue;
    occurrences.push({
      cisi: row.cisi,
      id: row.id,
      site: row.site,
      type: row.type,
      symbol: row.symbol,
      text: row.text,
      prev: toks[i - 1],
      next: toks[i + 1] ?? '<END>',
      next_in_465_475: inWindow(toks[i + 1] ?? '<END>') ? 'yes' : 'no',
      trained_prefix_154_158: TRAINED_PREFIX_SIGNS.has(toks[i - 1]) ? 'yes' : 'no',
      expanded_prefix_154_155_158_100: EXTENSION_PREFIX_SIGNS.has(toks[i - 1]) ? 'yes' : 'no',
      geography: row.site === 'Harappa' ? 'Harappa_train' : 'non_Harappa_holdout',
    });
  }
}

const harappa = occurrences.filter((item) => item.site === 'Harappa');
const nonHarappa = occurrences.filter((item) => item.site !== 'Harappa');
const trainedAll = summarizeBlock(occurrences, TRAINED_PREFIX_SIGNS);
const trainedHarappa = summarizeBlock(harappa, TRAINED_PREFIX_SIGNS);
const trainedHoldout = summarizeBlock(nonHarappa, TRAINED_PREFIX_SIGNS);
const expandedAll = summarizeBlock(occurrences, EXTENSION_PREFIX_SIGNS);
const expandedHoldout = summarizeBlock(nonHarappa, EXTENSION_PREFIX_SIGNS);
const dedupOccurrences = exactCollapse(occurrences);
const dedupNonHarappa = exactCollapse(nonHarappa);
const trainedAllDedup = summarizeBlock(dedupOccurrences, TRAINED_PREFIX_SIGNS);
const trainedHoldoutDedup = summarizeBlock(dedupNonHarappa, TRAINED_PREFIX_SIGNS);
const expandedAllDedup = summarizeBlock(dedupOccurrences, EXTENSION_PREFIX_SIGNS);
const expandedHoldoutDedup = summarizeBlock(dedupNonHarappa, EXTENSION_PREFIX_SIGNS);

const successorDistribution = [...occurrences
  .filter((item) => EXTENSION_PREFIX_SIGNS.has(item.prev))
  .reduce((acc, item) => {
    const key = item.next;
    acc.set(key, (acc.get(key) ?? 0) + 1);
    return acc;
  }, new Map()).entries()]
  .map(([next, n]) => ({ next, n }))
  .sort((a, b) => tokenNum(a.next) - tokenNum(b.next));

const predecessorBreakdown = [...occurrences.reduce((acc, item) => {
  if (!acc.has(item.prev)) {
    acc.set(item.prev, { prev: item.prev, n: 0, hits_465_475: 0, terminal: 0, examples: [] });
  }
  const entry = acc.get(item.prev);
  entry.n += 1;
  if (inWindow(item.next)) entry.hits_465_475 += 1;
  if (item.next === '<END>') entry.terminal += 1;
  if (entry.examples.length < 4) entry.examples.push(`${item.cisi} ${item.text}`);
  return acc;
}, new Map()).values()]
  .sort((a, b) => b.n - a.n || a.prev.localeCompare(b.prev));

const summary = {
  date: RUN_DATE,
  phase: 'EXPAND',
  candidate_id: PREFIX,
  tier: 'promoted_candidate_metadata_layer',
  bet: '806 has a construction-sensitive prefix-series role: when preceded by 154/158 it predicts a following 465..475 series sign. Harappa alone supplies the rule, and non-Harappa rows are the held-out test. 155 and 100 are possible extension members because they appear only in the held-out/non-Harappa side and obey the same successor band.',
  trained_rule: {
    prefix_signs_learned_from_harappa: [...TRAINED_PREFIX_SIGNS],
    successor_band: `${String(WINDOW_START).padStart(3, '0')}..${String(WINDOW_END).padStart(3, '0')}`,
    harappa_train: trainedHarappa,
    non_harappa_holdout: trainedHoldout,
    all_sites_trained_prefix_only: trainedAll,
    exact_text_site_type_symbol_prev_next_dedup: {
      all_sites: trainedAllDedup,
      non_harappa_holdout: trainedHoldoutDedup,
    },
  },
  extension_rule: {
    prefix_signs: [...EXTENSION_PREFIX_SIGNS],
    status: 'candidate_extension_not_needed_for_the_holdout_but_strongly_suggested_by_155_and_100_rows',
    non_harappa_holdout: expandedHoldout,
    all_sites: expandedAll,
    exact_text_site_type_symbol_prev_next_dedup: {
      all_sites: expandedAllDedup,
      non_harappa_holdout: expandedHoldoutDedup,
    },
    prefix_successor_distribution: successorDistribution,
  },
  adversarial_notes: [
    'The trained 154/158 rule is not allowed to learn 155 or 100 from Harappa, because they are absent there in this context.',
    'The extension family is therefore lower confidence than the 154/158 rule, but it is not a free rescue: 155 and 100 occur on the held-out side and both land inside the same 465..475 successor band.',
    'Exact text/site/type/symbol/prev/next collapse preserves the trained and extension effects in the non-Harappa holdout.',
    'This is still metadata-layer evidence. Source-token boxing and copy-family collapse can demote it.',
  ],
  predecessor_breakdown: predecessorBreakdown,
  decision: trainedHoldout.target_n >= 5
    && trainedHoldout.target_hits_465_475 === trainedHoldout.target_n
    && trainedHoldout.fisher_right_tail <= 0.01
    && expandedAll.control_hits_465_475 === 0
    ? 'promote_as_metadata_layer_series_operator_candidate'
    : 'keep_as_candidate_or_demote',
  falsifiers: [
    'A source-visible 154-806 or 158-806 row followed by a non-465..475 sign kills the trained version.',
    'Any non-prefix predecessor before 806 followed by 465..475 kills the exclusivity version.',
    'Exact source-family collapse that reduces the trained holdout to fewer than two independent objects demotes the candidate.',
    'Blind source boxes showing that the 806 or successor token boundaries are catalog artifacts demote the candidate.',
  ],
};

fs.mkdirSync(OUT_DIR, { recursive: true });
writeCsv(path.join(OUT_DIR, `${PREFIX}_806_occurrences.csv`), occurrences, [
  'id', 'cisi', 'site', 'type', 'symbol', 'text', 'prev', 'next', 'next_in_465_475',
  'trained_prefix_154_158', 'expanded_prefix_154_155_158_100', 'geography',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_predecessor_breakdown.csv`), predecessorBreakdown, [
  'prev', 'n', 'hits_465_475', 'terminal', 'examples',
]);
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
