// Stress-tests the risky bet that terminal sign 820 is the closer used on
// rhinoceros square seals, within the local frame "002 then one of
// {817,820,861}" at the end of the text. From the filtered corpus we keep
// square seals (SEAL:S), dedupe to one row per exact sign sequence, and check
// how often the Rhin icon class ends in 820 versus the other two terminals.
// Nulls: 10000 shuffles of the terminal labels, run four ways — the Rhin
// count itself, a site-matched version, and maxstat versions asking whether
// ANY icon class gets that pure for any terminal (or for 820 specifically).
// Metadata-poor seals are augmented from the S1 zoomorphic icon catalogue
// text, and a downloaded CISI page image serves as a visual spot-check. The
// tier logic promotes the bet only if source-verified held-out rows exist and
// all false-positive rates stay under threshold. Writes a JSON report and
// four CSVs (target rows, symbol summary, prediction rows, iterations).
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const REPORTS = path.join(ROOT, 'data', 'open_prototype', 'reports');
const SOURCE_CATALOGUE = path.join(ROOT, 'tmp', 'pdfs', 'S1-IndusZoomorphicIconCatalogue_20260531.txt');
const SOURCE_CATALOGUE_PDF = path.join(ROOT, 'tmp', 'pdfs', 'S1-IndusZoomorphicIconCatalogue_20260531.pdf');
const SOURCE_VISUAL_PAGE = path.join(ROOT, 'tmp', '820_rhin_source_pages', 'Pakistan_n160_w2000.jpg');
const PREFIX = 'risky_820_rhin_terminal_closer_forger_20260531';
const RUN_DATE = '2026-05-31T14:04:00-07:00';
const ITERATIONS = 10000;
const TARGET_SYMBOL = 'Rhin';
const TARGET_TERMINAL = '820';
const TERMINALS = new Set(['817', '820', '861']);

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

function writeCsv(file, rows, fields) {
  const esc = (value) => {
    const text = String(value ?? '');
    return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
  };
  const body = rows.map((row) => fields.map((field) => esc(row[field])).join(',')).join('\n');
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`, 'utf8');
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function norm(value, fallback = 'NA') {
  const text = String(value ?? '').trim();
  return text && text !== '-' && text !== 'None' && text !== '--' ? text : fallback;
}

function mulberry32(seed) {
  return function rand() {
    let t = (seed += 0x6D2B79F5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffle(arr, rand) {
  const out = arr.slice();
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    const tmp = out[i];
    out[i] = out[j];
    out[j] = tmp;
  }
  return out;
}

function terminalFrame(row) {
  const i = row.signs.indexOf('002');
  if (i < 0 || i !== row.signs.length - 2) return null;
  const y = row.signs[i + 1];
  if (!TERMINALS.has(y)) return null;
  return {
    object: row.id,
    cisi: row.cisi,
    site: row.site,
    region: row.region,
    type: row.type,
    symbol: row.symbol,
    cult: row.cult,
    material: row.material,
    shape: row.shape,
    condition: row.condition,
    complete: row.complete,
    terminal: y,
    predecessor: row.signs[i - 1] ?? '<START>',
    text: row.text,
    signs: row.signs,
    family_key: [row.site, row.type, row.symbol, row.cult, row.material, row.shape].join('|'),
  };
}

function countTarget(frames, labels = null) {
  let total = 0;
  let hits = 0;
  for (let i = 0; i < frames.length; i += 1) {
    const frame = frames[i];
    if (frame.symbol !== TARGET_SYMBOL) continue;
    total += 1;
    const label = labels ? labels[i] : frame.terminal;
    if (label === TARGET_TERMINAL) hits += 1;
  }
  return { total, hits, share: total ? hits / total : null };
}

function maxSymbolPurity(frames, labels = null) {
  const bySymbol = new Map();
  for (let i = 0; i < frames.length; i += 1) {
    const symbol = frames[i].symbol;
    if (symbol === 'NA') continue;
    if (!bySymbol.has(symbol)) bySymbol.set(symbol, []);
    bySymbol.get(symbol).push(labels ? labels[i] : frames[i].terminal);
  }
  let maxHits = 0;
  let maxShare = 0;
  let maxLabel = '';
  let maxSymbol = '';
  const rows = [];
  for (const [symbol, vals] of bySymbol) {
    if (vals.length < 4) continue;
    const counts = Object.fromEntries([...TERMINALS].map((label) => [label, vals.filter((value) => value === label).length]));
    const best = [...TERMINALS].map((label) => [label, counts[label]]).sort((a, b) => b[1] - a[1])[0];
    const share = best[1] / vals.length;
    rows.push({ symbol, total: vals.length, best_label: best[0], best_hits: best[1], best_share: share, counts: JSON.stringify(counts) });
    if (best[1] > maxHits || (best[1] === maxHits && share > maxShare)) {
      maxHits = best[1];
      maxShare = share;
      maxLabel = best[0];
      maxSymbol = symbol;
    }
  }
  return { maxHits, maxShare, maxLabel, maxSymbol, rows };
}

function sourceCatalogueSymbol(cisi) {
  if (!fs.existsSync(SOURCE_CATALOGUE)) return null;
  const line = fs.readFileSync(SOURCE_CATALOGUE, 'utf8')
    .split(/\r?\n/)
    .find((candidate) => candidate.startsWith(`${cisi} `));
  if (!line) return null;
  if (/\bRhino\b/.test(line)) return 'Rhin';
  if (/\bElephant\b|\bElep\b/.test(line)) return 'Elep';
  if (/\bUnicorn\b/.test(line)) return 'Bull1:W';
  return null;
}

function siteMatchedFrames(frames) {
  const targetSites = new Set(frames.filter((frame) => frame.symbol === TARGET_SYMBOL).map((frame) => frame.site));
  return frames.filter((frame) => targetSites.has(frame.site));
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8'))
  .map((row) => ({
    ...row,
    id: row.id,
    cisi: row.cisi || '-',
    site: norm(row.site),
    region: norm(row.region),
    type: norm(row.type),
    symbol: norm(row.symbol),
    cult: norm(row.cult),
    material: norm(row.material),
    shape: norm(row.shape),
    condition: norm(row.condition),
    complete: norm(row.complete),
    signs: tokens(row.text),
  }));

const rows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()]
  .filter((row) => row.signs.length);

const allSquareTerminalFrames = rows
  .filter((row) => row.type === 'SEAL:S')
  .map(terminalFrame)
  .filter(Boolean);
const squareFrames = allSquareTerminalFrames.filter((frame) => frame.symbol !== 'NA');
const mohenjoFrames = siteMatchedFrames(squareFrames);
const labels = squareFrames.map((frame) => frame.terminal);
const mohenjoLabels = mohenjoFrames.map((frame) => frame.terminal);
const sourceAugmentedFrames = allSquareTerminalFrames.map((frame) => {
  const sourceSymbol = sourceCatalogueSymbol(frame.cisi);
  return {
    ...frame,
    source_catalogue_symbol: sourceSymbol,
    augmented_symbol: frame.symbol !== 'NA' ? frame.symbol : (sourceSymbol ?? 'NA'),
  };
});
const sourceAugmentedKnownFrames = sourceAugmentedFrames.filter((frame) => frame.augmented_symbol !== 'NA');
const sourceAugmentedLabels = sourceAugmentedKnownFrames.map((frame) => frame.terminal);
const sourceVerifiedPredictionRows = sourceAugmentedFrames.filter((frame) =>
  frame.symbol === 'NA' &&
  frame.terminal === TARGET_TERMINAL &&
  frame.source_catalogue_symbol === TARGET_SYMBOL
);

const observedTarget = countTarget(squareFrames);
const observedSiteTarget = countTarget(mohenjoFrames);
const observedMax = maxSymbolPurity(squareFrames);
const targetRows = squareFrames.filter((frame) => frame.symbol === TARGET_SYMBOL);
const targetFamilies = new Set(targetRows.map((frame) => frame.family_key)).size;
const sourceAugmentedTargetRows = sourceAugmentedKnownFrames.filter((frame) => frame.augmented_symbol === TARGET_SYMBOL);
const sourceAugmentedObserved = {
  total: sourceAugmentedTargetRows.length,
  hits: sourceAugmentedTargetRows.filter((frame) => frame.terminal === TARGET_TERMINAL).length,
};
sourceAugmentedObserved.share = sourceAugmentedObserved.total ? sourceAugmentedObserved.hits / sourceAugmentedObserved.total : null;
const predictionRows = allSquareTerminalFrames
  .filter((frame) => frame.symbol === 'NA' && frame.terminal === TARGET_TERMINAL)
  .map((frame) => {
    const m = String(frame.cisi).match(/^M-(\d+)$/);
    const numeric = m ? Number(m[1]) : null;
    const nearKnownRhin = numeric !== null && targetRows.some((row) => {
      const other = String(row.cisi).match(/^M-(\d+)$/);
      return other && Math.abs(Number(other[1]) - numeric) <= 2;
    });
    return {
      ...frame,
      prediction:
        nearKnownRhin
          ? 'high-risk prediction: missing/fragmentary icon should be rhinoceros or rhinoceros-trough adjacent'
          : 'weak prediction: missing/fragmentary icon should be checked for rhinoceros or other 820-selecting animal context',
      prediction_priority: nearKnownRhin ? 'high' : 'low',
    };
  });

const rand = mulberry32(0x820817 ^ squareFrames.length ^ targetRows.length);
let targetGe = 0;
let siteMatchedGe = 0;
let maxAnyGe = 0;
let max820Ge = 0;
let sourceAugmentedGe = 0;
let sourceAugmentedMaxAnyGe = 0;
const iterationRows = [];
for (let iter = 0; iter < ITERATIONS; iter += 1) {
  const shuffledLabels = shuffle(labels, rand);
  const shuffledTarget = countTarget(squareFrames, shuffledLabels);
  const shuffledMax = maxSymbolPurity(squareFrames, shuffledLabels);
  const shuffledMohenjoLabels = shuffle(mohenjoLabels, rand);
  const shuffledSiteTarget = countTarget(mohenjoFrames, shuffledMohenjoLabels);
  const shuffledSourceAugmentedLabels = shuffle(sourceAugmentedLabels, rand);
  let shuffledSourceAugmentedHits = 0;
  for (let i = 0; i < sourceAugmentedKnownFrames.length; i += 1) {
    if (sourceAugmentedKnownFrames[i].augmented_symbol === TARGET_SYMBOL && shuffledSourceAugmentedLabels[i] === TARGET_TERMINAL) {
      shuffledSourceAugmentedHits += 1;
    }
  }
  const byAugmentedSymbol = sourceAugmentedKnownFrames.map((frame, idx) => ({
    ...frame,
    symbol: frame.augmented_symbol,
    terminal: shuffledSourceAugmentedLabels[idx],
  }));
  const shuffledSourceAugmentedMax = maxSymbolPurity(byAugmentedSymbol);
  const targetHit = shuffledTarget.hits >= observedTarget.hits;
  const siteHit = shuffledSiteTarget.hits >= observedSiteTarget.hits;
  const maxAnyHit = shuffledMax.maxHits >= observedTarget.hits && shuffledMax.maxShare >= observedTarget.share;
  const max820Hit = shuffledMax.rows.some((row) =>
    row.best_label === TARGET_TERMINAL &&
    row.best_hits >= observedTarget.hits &&
    row.best_share >= observedTarget.share
  );
  const sourceAugmentedHit = shuffledSourceAugmentedHits >= sourceAugmentedObserved.hits;
  const sourceAugmentedMaxHit =
    shuffledSourceAugmentedMax.maxHits >= sourceAugmentedObserved.hits &&
    shuffledSourceAugmentedMax.maxShare >= sourceAugmentedObserved.share;
  if (targetHit) targetGe += 1;
  if (siteHit) siteMatchedGe += 1;
  if (maxAnyHit) maxAnyGe += 1;
  if (max820Hit) max820Ge += 1;
  if (sourceAugmentedHit) sourceAugmentedGe += 1;
  if (sourceAugmentedMaxHit) sourceAugmentedMaxAnyGe += 1;
  if (iter < 50 || targetHit || siteHit || maxAnyHit || max820Hit || sourceAugmentedHit || sourceAugmentedMaxHit) {
    iterationRows.push({
      iteration: iter,
      target_hits: shuffledTarget.hits,
      target_ge_observed: String(targetHit),
      site_target_hits: shuffledSiteTarget.hits,
      site_ge_observed: String(siteHit),
      max_symbol: shuffledMax.maxSymbol,
      max_label: shuffledMax.maxLabel,
      max_hits: shuffledMax.maxHits,
      max_share: shuffledMax.maxShare,
      max_any_ge_observed: String(maxAnyHit),
      max_820_ge_observed: String(max820Hit),
      source_augmented_hits: shuffledSourceAugmentedHits,
      source_augmented_ge_observed: String(sourceAugmentedHit),
      source_augmented_max_symbol: shuffledSourceAugmentedMax.maxSymbol,
      source_augmented_max_label: shuffledSourceAugmentedMax.maxLabel,
      source_augmented_max_hits: shuffledSourceAugmentedMax.maxHits,
      source_augmented_max_ge_observed: String(sourceAugmentedMaxHit),
    });
  }
}

const symbolRows = observedMax.rows.sort((a, b) => b.best_share - a.best_share || b.best_hits - a.best_hits);
const candidateTier =
  sourceVerifiedPredictionRows.length > 0 &&
  sourceAugmentedObserved.total >= 5 &&
  sourceAugmentedObserved.hits === sourceAugmentedObserved.total &&
  sourceAugmentedGe / ITERATIONS <= 0.01 &&
  sourceAugmentedMaxAnyGe / ITERATIONS <= 0.05
    ? 'promoted candidate'
    : observedTarget.total >= 4 &&
        observedTarget.hits === observedTarget.total &&
        targetGe / ITERATIONS <= 0.01 &&
        siteMatchedGe / ITERATIONS <= 0.05
      ? 'candidate'
      : 'wild shot';

const summary = {
  run_date_time: RUN_DATE,
  vector: 'V4 context-to-meaning',
  risky_bet_tier: candidateTier,
  claim:
    '`820` is the rhinoceros square-seal terminal closer inside the local `002 -> {817,820,861}` terminal set.',
  observed:
    `Rhin SEAL:S exact-text-collapsed terminal frames are ${observedTarget.hits}/${observedTarget.total} ` +
    `${TARGET_TERMINAL}; background square terminal frames=${squareFrames.length}; ` +
    `site-matched target=${observedSiteTarget.hits}/${observedSiteTarget.total}; ` +
    `distinct target family keys=${targetFamilies}.`,
  target_terminal_false_positive_rate: targetGe / ITERATIONS,
  site_matched_terminal_false_positive_rate: siteMatchedGe / ITERATIONS,
  any_symbol_any_terminal_maxstat_false_positive_rate: maxAnyGe / ITERATIONS,
  any_symbol_820_terminal_maxstat_false_positive_rate: max820Ge / ITERATIONS,
  source_catalogue_prediction_check: fs.existsSync(SOURCE_CATALOGUE) ? {
    path: SOURCE_CATALOGUE,
    pdf_path: fs.existsSync(SOURCE_CATALOGUE_PDF) ? SOURCE_CATALOGUE_PDF : null,
    source_url: 'https://storage.googleapis.com/cahcblr-pdfs/assets/ijhs/S1-IndusZoomorphicIconCatalogue.pdf',
    last_write_time: fs.statSync(SOURCE_CATALOGUE).mtime.toISOString(),
    verified_rows: sourceVerifiedPredictionRows.map((row) => ({
      cisi: row.cisi,
      object: row.object,
      metadata_symbol: row.symbol,
      source_catalogue_symbol: row.source_catalogue_symbol,
      terminal: row.terminal,
      text: row.text,
    })),
  } : null,
  source_visual_page_check: fs.existsSync(SOURCE_VISUAL_PAGE) ? {
    path: SOURCE_VISUAL_PAGE,
    source_url: 'https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/n160_w2000.jpg',
    page_header_visible: 'MOHENJO-DARO 1136-1140 SEALS rhinoceros',
    visual_result: 'Downloaded CISI Pakistan page n160 visibly groups M-1136, M-1137, M-1138, and M-1139 under the rhinoceros page header and shows the terminal 820 as a wheel/rosette sign, including the metadata-None M-1137 row.',
    last_write_time: fs.statSync(SOURCE_VISUAL_PAGE).mtime.toISOString(),
  } : null,
  source_augmented_observed:
    `Source-augmented Rhin terminal frames are ${sourceAugmentedObserved.hits}/${sourceAugmentedObserved.total} ${TARGET_TERMINAL}; verified held-out metadata-None rows=${sourceVerifiedPredictionRows.length}.`,
  source_augmented_target_false_positive_rate: sourceAugmentedGe / ITERATIONS,
  source_augmented_any_symbol_maxstat_false_positive_rate: sourceAugmentedMaxAnyGe / ITERATIONS,
  controls:
    'Exact-text collapse before testing; terminal labels shuffled among all square `002->Y` terminal frames; site-matched label shuffle restricted to target-site frames; all-symbol maxstat checks whether any icon class with >=4 frames becomes equally pure for any terminal or specifically 820.',
  weakness:
    'All target frames are Mohenjo-daro rhinoceros square seals, so this is not pan-corpus semantics. It is a local icon/register candidate unless non-Mohenjo rhinoceros frames appear and keep selecting 820.',
  promotion_condition:
    'Promote only if an additional source-bound rhinoceros square frame outside the same Mohenjo-daro family also selects terminal 820, or if a currently unlabeled high-priority 002-820 square row is source-verified as rhinoceros/trough, while all-symbol maxstat remains below 0.05.',
  break_condition:
    'A source-bound rhinoceros square terminal frame selecting 817 or 861, or a maxstat null that routinely finds 4/4 icon-terminal cells, demotes the bet.',
  observed_target: observedTarget,
  observed_site_target: observedSiteTarget,
  source_augmented_target: sourceAugmentedObserved,
  observed_symbol_rows: symbolRows,
  target_rows: targetRows,
  source_augmented_target_rows: sourceAugmentedTargetRows,
  prediction_rows: predictionRows,
};

fs.mkdirSync(REPORTS, { recursive: true });
fs.writeFileSync(path.join(REPORTS, `${PREFIX}.json`), JSON.stringify(summary, null, 2), 'utf8');
writeCsv(path.join(REPORTS, `${PREFIX}_target_rows.csv`), targetRows, [
  'object',
  'cisi',
  'site',
  'type',
  'symbol',
  'cult',
  'material',
  'shape',
  'condition',
  'complete',
  'predecessor',
  'terminal',
  'family_key',
  'text',
]);
writeCsv(path.join(REPORTS, `${PREFIX}_symbol_terminal_summary.csv`), symbolRows, [
  'symbol',
  'total',
  'best_label',
  'best_hits',
  'best_share',
  'counts',
]);
writeCsv(path.join(REPORTS, `${PREFIX}_prediction_rows.csv`), predictionRows, [
  'object',
  'cisi',
  'site',
  'type',
  'symbol',
  'cult',
  'material',
  'shape',
  'condition',
  'complete',
  'predecessor',
  'terminal',
  'family_key',
  'prediction_priority',
  'prediction',
  'text',
]);
writeCsv(path.join(REPORTS, `${PREFIX}_iterations.csv`), iterationRows, [
  'iteration',
  'target_hits',
  'target_ge_observed',
  'site_target_hits',
  'site_ge_observed',
  'max_symbol',
  'max_label',
  'max_hits',
  'max_share',
  'max_any_ge_observed',
  'max_820_ge_observed',
  'source_augmented_hits',
  'source_augmented_ge_observed',
  'source_augmented_max_symbol',
  'source_augmented_max_label',
  'source_augmented_max_hits',
  'source_augmented_max_ge_observed',
]);

console.log(JSON.stringify(summary, null, 2));
