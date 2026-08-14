// Tries to break (forge against) the claim that terminal sign 820 belongs to
// rhinoceros seals specifically, by pitting it against a named foil: elephant.
// We take square seals (SEAL:S) whose text ends 002 followed by one of the
// three terminals 817/820/861, dedupe to one row per exact sign sequence, and
// label each seal's animal icon from the metadata symbol column — falling back
// to a text extraction of the S1 zoomorphic icon catalogue when metadata is
// missing. The test: do rhinoceros frames pick 820 while elephant frames avoid
// it? A 20000-iteration shuffle of the terminal labels measures how often that
// exact contrast — and the looser "any two symbols show such a contrast"
// version — appears by chance. Writes a JSON report and four CSVs (target
// rows, symbol summary, predictions for unlabeled seals, sample iterations).
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const REPORTS = path.join(ROOT, 'data', 'open_prototype', 'reports');
const SOURCE_CATALOGUE = path.join(ROOT, 'tmp', 'pdfs', 'S1-IndusZoomorphicIconCatalogue_20260531.txt');
const SOURCE_CATALOGUE_PDF = path.join(ROOT, 'tmp', 'pdfs', 'S1-IndusZoomorphicIconCatalogue_20260531.pdf');
const PREFIX = 'risky_820_rhin_elephant_contrast_forger_20260531';
const RUN_DATE = '2026-05-31T14:14:00-07:00';
const ITERATIONS = 20000;
const TERMINALS = ['817', '820', '861'];
const TERMINAL_SET = new Set(TERMINALS);

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

function norm(value, fallback = 'NA') {
  const text = String(value ?? '').trim();
  return text && text !== '-' && text !== 'None' && text !== '--' ? text : fallback;
}

function symbolClass(value) {
  const text = norm(value);
  if (/^Rhin\b/.test(text)) return 'Rhin';
  if (/^Elep\b/.test(text)) return 'Elep';
  if (/^Bull1:W\b/.test(text)) return 'Bull1:W';
  return text;
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function sourceCatalogueSymbol(cisi) {
  if (!fs.existsSync(SOURCE_CATALOGUE)) return null;
  const line = fs.readFileSync(SOURCE_CATALOGUE, 'utf8')
    .split(/\r?\n/)
    .find((candidate) => candidate.startsWith(`${cisi} `));
  if (!line) return null;
  if (/\bRhino(?!\?)\b/.test(line)) return 'Rhin';
  if (/\bElephant(?!\?)\b|\bElep(?!\?)\b/.test(line)) return 'Elep';
  if (/\bUnicorn(?!\?)\b/.test(line)) return 'Bull1:W';
  return null;
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
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function terminalFrame(row) {
  if (row.type !== 'SEAL:S') return null;
  if (row.signs.length < 2 || row.signs[row.signs.length - 2] !== '002') return null;
  const terminal = row.signs[row.signs.length - 1];
  if (!TERMINAL_SET.has(terminal)) return null;
  const sourceSymbol = sourceCatalogueSymbol(row.cisi);
  return {
    object: row.id,
    cisi: row.cisi,
    site: row.site,
    type: row.type,
    metadata_symbol: row.symbol,
    source_catalogue_symbol: sourceSymbol ?? 'NA',
    augmented_symbol: row.symbol !== 'NA' ? symbolClass(row.symbol) : (sourceSymbol ?? 'NA'),
    terminal,
    predecessor: row.signs[row.signs.length - 3] ?? '<START>',
    text: row.text,
    source: row.symbol !== 'NA' ? 'metadata' : (sourceSymbol ? 'source_catalogue' : 'unknown'),
  };
}

function countBySymbol(frames, labels = null) {
  const bySymbol = new Map();
  for (let i = 0; i < frames.length; i += 1) {
    const symbol = frames[i].augmented_symbol;
    if (symbol === 'NA') continue;
    if (!bySymbol.has(symbol)) bySymbol.set(symbol, []);
    bySymbol.get(symbol).push(labels ? labels[i] : frames[i].terminal);
  }
  return bySymbol;
}

function symbolSummary(frames, labels = null) {
  const bySymbol = countBySymbol(frames, labels);
  return [...bySymbol.entries()].map(([symbol, vals]) => {
    const counts = Object.fromEntries(TERMINALS.map((terminal) => [terminal, vals.filter((value) => value === terminal).length]));
    return {
      symbol,
      total: vals.length,
      n817: counts['817'],
      n820: counts['820'],
      n861: counts['861'],
      share820: vals.length ? counts['820'] / vals.length : null,
      best_terminal: TERMINALS.slice().sort((a, b) => counts[b] - counts[a])[0],
      best_hits: Math.max(...TERMINALS.map((terminal) => counts[terminal])),
    };
  }).sort((a, b) => b.total - a.total || a.symbol.localeCompare(b.symbol));
}

function contrastScore(frames, labels = null) {
  const summary = symbolSummary(frames, labels);
  const rhin = summary.find((row) => row.symbol === 'Rhin') ?? { total: 0, n820: 0 };
  const elep = summary.find((row) => row.symbol === 'Elep') ?? { total: 0, n820: 0 };
  return {
    rhin_total: rhin.total,
    rhin_820: rhin.n820,
    rhin_share820: rhin.total ? rhin.n820 / rhin.total : null,
    elep_total: elep.total,
    elep_820: elep.n820,
    elep_avoid820: elep.total - elep.n820,
    elep_share820: elep.total ? elep.n820 / elep.total : null,
  };
}

function hasAtLeastObservedContrast(frames, obs, labels = null) {
  const score = contrastScore(frames, labels);
  return score.rhin_820 >= obs.rhin_820 &&
    score.elep_total >= obs.elep_total &&
    score.elep_avoid820 >= obs.elep_avoid820;
}

function hasAnySymbolPairContrast(frames, obs, labels = null) {
  const summary = symbolSummary(frames, labels).filter((row) => row.total >= 4);
  const high820Symbols = summary.filter((row) => row.total >= obs.rhin_total && row.n820 >= obs.rhin_820);
  const avoids820Symbols = summary.filter((row) => row.total >= obs.elep_total && (row.total - row.n820) >= obs.elep_avoid820);
  return high820Symbols.some((high) => avoids820Symbols.some((avoid) => avoid.symbol !== high.symbol));
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({
  ...row,
  id: row.id,
  cisi: row.cisi || '-',
  site: norm(row.site),
  type: norm(row.type),
  symbol: symbolClass(row.symbol),
  text: row.text,
  signs: tokens(row.text),
}));

const rows = [...new Map(rawRows.filter((row) => row.signs.length).map((row) => [row.signs.join(' '), row])).values()];
const frames = rows.map(terminalFrame).filter(Boolean);
const knownFrames = frames.filter((frame) => frame.augmented_symbol !== 'NA');
const labels = knownFrames.map((frame) => frame.terminal);
const observed = contrastScore(knownFrames);
const summary = symbolSummary(knownFrames);
const targetRows = knownFrames.filter((frame) => frame.augmented_symbol === 'Rhin' || frame.augmented_symbol === 'Elep');
const predictionRows = frames.filter((frame) => frame.augmented_symbol === 'NA' && frame.terminal === '820')
  .map((frame) => ({
    ...frame,
    prediction: 'if 820 is the rhinoceros-side terminal closer, this metadata-poor row should source-check as rhinoceros/trough rather than elephant',
  }));

const rand = mulberry32(0x820E1E9 ^ knownFrames.length ^ labels.length);
let exactGe = 0;
let pairMaxGe = 0;
const iterations = [];
for (let iter = 0; iter < ITERATIONS; iter += 1) {
  const shuffled = shuffle(labels, rand);
  const exact = hasAtLeastObservedContrast(knownFrames, observed, shuffled);
  const pairMax = hasAnySymbolPairContrast(knownFrames, observed, shuffled);
  if (exact) exactGe += 1;
  if (pairMax) pairMaxGe += 1;
  if (iter < 200) {
    const score = contrastScore(knownFrames, shuffled);
    iterations.push({
      iter,
      rhin_820: score.rhin_820,
      elep_820: score.elep_820,
      exact_ge: exact ? 1 : 0,
      pair_max_ge: pairMax ? 1 : 0,
    });
  }
}

const report = {
  run_date: RUN_DATE,
  tier: exactGe / ITERATIONS <= 0.01 ? 'candidate' : 'wild shot',
  exploratory_maxstat_tier: pairMaxGe / ITERATIONS <= 0.05 ? 'candidate' : 'wild shot',
  risky_bet: 'Inside exact-text-collapsed square-seal terminal frames 002->{817,820,861}, 820 is the rhinoceros-side terminal closer, not a generic large-animal terminal: rhinoceros selects 820 while elephant avoids 820.',
  observed,
  observed_readable: `source-augmented Rhin frames are ${observed.rhin_820}/${observed.rhin_total} terminal 820; source-augmented Elep frames are ${observed.elep_820}/${observed.elep_total} terminal 820.`,
  exact_symbol_false_positive_rate: exactGe / ITERATIONS,
  any_symbol_pair_maxstat_false_positive_rate: pairMaxGe / ITERATIONS,
  maxstat_interpretation: 'The named rhino-vs-elephant foil is candidate-tier under label shuffle. The exploratory version, where the analyst may choose any avoiding symbol after seeing the table, is wild-shot only because many symbols avoid 820. Therefore this promotes a named foil/control for 820/Rhin, not a broad semantic contrast.',
  terminal_slot: 'SEAL:S rows where 002 is penultimate and final sign is one of 817,820,861',
  dedupe: 'one row per exact sign sequence before testing',
  source_augmentation: {
    text_catalogue: SOURCE_CATALOGUE,
    pdf_catalogue: SOURCE_CATALOGUE_PDF,
    rule: 'metadata symbol used when present; metadata-NA rows receive source catalogue labels only when the fresh extracted catalogue line gives non-questioned Rhino/Elephant/Unicorn',
  },
  break_condition: 'Any source-bound elephant square terminal frame in this slot selecting 820, or a shuffle/maxstat rate above threshold, demotes the contrast; a rhinoceros frame selecting 817/861 attacks the older 820/Rhin candidate directly.',
  promotion_condition: 'More metadata-poor 002-820 rows source-check as rhinoceros/trough while elephant remains 0 for 820 under the same slot definition.',
  symbol_terminal_summary: summary,
  target_rows: targetRows,
  prediction_rows: predictionRows,
};

fs.mkdirSync(REPORTS, { recursive: true });
fs.writeFileSync(path.join(REPORTS, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
writeCsv(path.join(REPORTS, `${PREFIX}_target_rows.csv`), targetRows, [
  'object', 'cisi', 'site', 'metadata_symbol', 'source_catalogue_symbol', 'augmented_symbol', 'terminal', 'predecessor', 'source', 'text',
]);
writeCsv(path.join(REPORTS, `${PREFIX}_symbol_terminal_summary.csv`), summary, [
  'symbol', 'total', 'n817', 'n820', 'n861', 'share820', 'best_terminal', 'best_hits',
]);
writeCsv(path.join(REPORTS, `${PREFIX}_prediction_rows.csv`), predictionRows, [
  'object', 'cisi', 'site', 'terminal', 'predecessor', 'source', 'text', 'prediction',
]);
writeCsv(path.join(REPORTS, `${PREFIX}_iterations.csv`), iterations, [
  'iter', 'rhin_820', 'elep_820', 'exact_ge', 'pair_max_ge',
]);

console.log(JSON.stringify({
  tier: report.tier,
  observed: report.observed_readable,
  exact_symbol_false_positive_rate: report.exact_symbol_false_positive_rate,
  any_symbol_pair_maxstat_false_positive_rate: report.any_symbol_pair_maxstat_false_positive_rate,
  report: path.join(REPORTS, `${PREFIX}.json`),
}, null, 2));
