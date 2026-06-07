import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const SOURCE_CATALOGUE = path.join(ROOT, 'tmp', 'pdfs', 'S1-IndusZoomorphicIconCatalogue_20260531.txt');
const REPORTS = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'consolidate_820_rhin_hostile_controls_20260531';
const ITERATIONS = 20000;
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

function terminalFrame(row) {
  const i = row.signs.indexOf('002');
  if (i < 0 || i !== row.signs.length - 2) return null;
  const y = row.signs[i + 1];
  if (!TERMINALS.has(y)) return null;
  const sourceSymbol = sourceCatalogueSymbol(row.cisi);
  const augmentedSymbol = row.symbol !== 'NA' ? row.symbol : (sourceSymbol ?? 'NA');
  const pageCluster =
    /^M-113[6-9]$/.test(row.cisi) ? 'CISI_Pakistan_n160_M1136_M1139_rhinoceros_page' : row.cisi;
  return {
    object: row.id,
    cisi: row.cisi,
    site: row.site,
    region: row.region,
    type: row.type,
    metadata_symbol: row.symbol,
    source_catalogue_symbol: sourceSymbol ?? '',
    augmented_symbol: augmentedSymbol,
    cult: row.cult,
    material: row.material,
    shape: row.shape,
    terminal: y,
    predecessor: row.signs[i - 1] ?? '<START>',
    text: row.text,
    text_key: row.signs.join(' '),
    family_key: [row.site, row.type, augmentedSymbol, row.cult, row.material, row.shape].join('|'),
    page_cluster: pageCluster,
  };
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

function collapse(frames, key) {
  const out = [];
  const groups = new Map();
  for (const frame of frames) {
    const k = frame[key];
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(frame);
  }
  for (const [groupKey, group] of groups) {
    const terminals = [...new Set(group.map((frame) => frame.terminal))];
    const targetRows = group.filter((frame) => frame.augmented_symbol === TARGET_SYMBOL);
    const symbol = targetRows.length ? TARGET_SYMBOL : group[0].augmented_symbol;
    if (terminals.length === 1) {
      out.push({
        ...group[0],
        object: group.map((frame) => frame.object).join('|'),
        cisi: group.map((frame) => frame.cisi).join('|'),
        collapse_key: groupKey,
        collapse_n: group.length,
        augmented_symbol: symbol,
        terminal: terminals[0],
      });
    }
  }
  return out;
}

function countTarget(frames, labels = null) {
  let total = 0;
  let hits = 0;
  for (let i = 0; i < frames.length; i += 1) {
    if (frames[i].augmented_symbol !== TARGET_SYMBOL) continue;
    total += 1;
    const label = labels ? labels[i] : frames[i].terminal;
    if (label === TARGET_TERMINAL) hits += 1;
  }
  return { total, hits, share: total ? hits / total : null };
}

function maxAny(frames, labels = null) {
  const bySymbol = new Map();
  for (let i = 0; i < frames.length; i += 1) {
    const symbol = frames[i].augmented_symbol;
    if (symbol === 'NA') continue;
    if (!bySymbol.has(symbol)) bySymbol.set(symbol, []);
    bySymbol.get(symbol).push(labels ? labels[i] : frames[i].terminal);
  }
  let maxHits = 0;
  let maxShare = 0;
  let maxSymbol = '';
  for (const [symbol, vals] of bySymbol) {
    if (vals.length < 2) continue;
    const counts = [...TERMINALS].map((terminal) => vals.filter((value) => value === terminal).length);
    const hits = Math.max(...counts);
    const share = hits / vals.length;
    if (hits > maxHits || (hits === maxHits && share > maxShare)) {
      maxHits = hits;
      maxShare = share;
      maxSymbol = symbol;
    }
  }
  return { maxHits, maxShare, maxSymbol };
}

function runNull(frames, seed) {
  const labels = frames.map((frame) => frame.terminal);
  const observed = countTarget(frames);
  const observedMax = maxAny(frames);
  const rand = mulberry32(seed ^ labels.length ^ observed.total);
  let targetGe = 0;
  let maxGe = 0;
  for (let i = 0; i < ITERATIONS; i += 1) {
    const shuffled = shuffle(labels, rand);
    const target = countTarget(frames, shuffled);
    const mx = maxAny(frames, shuffled);
    if (target.hits >= observed.hits) targetGe += 1;
    if (
      mx.maxHits >= observed.hits &&
      observed.share !== null &&
      mx.maxShare >= observed.share
    ) maxGe += 1;
  }
  return {
    frame_count: frames.length,
    observed,
    observed_max: observedMax,
    target_false_positive_rate: targetGe / ITERATIONS,
    any_symbol_maxstat_false_positive_rate: maxGe / ITERATIONS,
  };
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({
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
  signs: tokens(row.text),
}));

const rows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()]
  .filter((row) => row.signs.length);
const squareFrames = rows
  .filter((row) => row.type === 'SEAL:S')
  .map(terminalFrame)
  .filter(Boolean)
  .filter((frame) => frame.augmented_symbol !== 'NA');
const mohenjoSquareFrames = squareFrames.filter((frame) => frame.site === 'Mohenjo-daro');
const familyCollapsed = collapse(squareFrames, 'family_key').filter((frame) => frame.augmented_symbol !== 'NA');
const mohenjoFamilyCollapsed = collapse(mohenjoSquareFrames, 'family_key').filter((frame) => frame.augmented_symbol !== 'NA');
const pageCollapsed = collapse(squareFrames, 'page_cluster').filter((frame) => frame.augmented_symbol !== 'NA');

const objectControl = runNull(squareFrames, 0x82000001);
const mohenjoObjectControl = runNull(mohenjoSquareFrames, 0x82000002);
const familyControl = runNull(familyCollapsed, 0x82000003);
const mohenjoFamilyControl = runNull(mohenjoFamilyCollapsed, 0x82000004);
const pageClusterControl = runNull(pageCollapsed, 0x82000005);

const targetRows = squareFrames.filter((frame) => frame.augmented_symbol === TARGET_SYMBOL);
const leaveOneOut = targetRows.map((leftOut) => {
  const kept = targetRows.filter((frame) => frame.object !== leftOut.object);
  return {
    left_out_object: leftOut.object,
    left_out_cisi: leftOut.cisi,
    kept_total: kept.length,
    kept_hits_820: kept.filter((frame) => frame.terminal === TARGET_TERMINAL).length,
    survives: kept.length > 0 && kept.every((frame) => frame.terminal === TARGET_TERMINAL),
  };
});

const sourceReclassified = targetRows.filter((frame) => frame.metadata_symbol === 'NA' && frame.source_catalogue_symbol === TARGET_SYMBOL);

const tier =
  familyControl.observed.total >= 4 &&
  familyControl.observed.hits === familyControl.observed.total &&
  familyControl.target_false_positive_rate <= 0.01 &&
  familyControl.any_symbol_maxstat_false_positive_rate <= 0.05
    ? 'promoted candidate at family-collapsed packet level'
    : objectControl.observed.total >= 5 &&
        objectControl.observed.hits === objectControl.observed.total &&
        objectControl.target_false_positive_rate <= 0.01
      ? 'candidate at object level only'
      : 'demoted';

const summary = {
  run_date_time: '2026-05-31T14:31:43-07:00',
  phase: 'CONSOLIDATE',
  risky_bet: 'The source-reclassified rhinoceros packet remains a real 820 terminal packet after duplicate/family hostility, but page-cluster collapse should expose whether it is one catalogue-page artifact.',
  tier,
  object_level: objectControl,
  mohenjo_object_level: mohenjoObjectControl,
  family_collapsed: familyControl,
  mohenjo_family_collapsed: mohenjoFamilyControl,
  page_cluster_collapsed: pageClusterControl,
  source_reclassified_rows: sourceReclassified,
  target_rows: targetRows,
  leave_one_out: leaveOneOut,
  consolidation_decision:
    'Demote 820/Rhin from promoted packet-level status to object-level candidate. Family collapse rises above the 0.01 bar and page-cluster collapse leaves only two target evidence clusters. Keep the narrower rosette/wheel closure-register bet alive; do not promote it to global semantic meaning.',
  next_action:
    'The next expansion should source-bind either an independent non-n160 rhinoceros 002-820 row or a source-visible 817/861 rhinoceros counterexample; otherwise the packet remains local.',
};

fs.mkdirSync(REPORTS, { recursive: true });
fs.writeFileSync(path.join(REPORTS, `${PREFIX}.json`), JSON.stringify(summary, null, 2), 'utf8');
writeCsv(path.join(REPORTS, `${PREFIX}_target_rows.csv`), targetRows, [
  'object',
  'cisi',
  'site',
  'type',
  'metadata_symbol',
  'source_catalogue_symbol',
  'augmented_symbol',
  'cult',
  'material',
  'shape',
  'predecessor',
  'terminal',
  'family_key',
  'page_cluster',
  'text',
]);
console.log(JSON.stringify({
  tier: summary.tier,
  object_level: summary.object_level,
  family_collapsed: summary.family_collapsed,
  page_cluster_collapsed: summary.page_cluster_collapsed,
  report: path.join(REPORTS, `${PREFIX}.json`),
}, null, 2));
