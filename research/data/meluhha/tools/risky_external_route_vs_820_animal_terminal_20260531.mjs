import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const EXTERNAL = path.join(ROOT, 'data', 'meluhha', 'external_indus_objects.csv');
const OUT_DIR = path.join(ROOT, 'data', 'meluhha');
const PREFIX = 'risky_external_route_vs_820_animal_terminal_20260531';
const ITERATIONS = 50000;

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

function routeHit(row) {
  return row.signs.includes('090') || row.signs.includes('091');
}

function sign407Hit(row) {
  return row.signs.includes('407');
}

function terminal002820(row) {
  return row.signs.length >= 2 && row.signs.at(-2) === '002' && row.signs.at(-1) === '820';
}

function mulberry32(seed) {
  return function rand() {
    let t = (seed += 0x6D2B79F5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function score(rows) {
  return {
    total: rows.length,
    route_090091: rows.filter(routeHit).length,
    sign_407: rows.filter(sign407Hit).length,
    terminal_002_820: rows.filter(terminal002820).length,
    any_820: rows.filter((row) => row.signs.includes('820')).length,
    route_or_407: rows.filter((row) => routeHit(row) || sign407Hit(row)).length,
  };
}

function byType(rows) {
  const out = new Map();
  for (const row of rows) {
    if (!out.has(row.type)) out.set(row.type, []);
    out.get(row.type).push(row);
  }
  return out;
}

const externalIds = new Set(parseCsv(fs.readFileSync(EXTERNAL, 'utf8')).map((row) => row.row_id));
const allRows = parseCsv(fs.readFileSync(META, 'utf8'))
  .map((row) => ({
    id: row.id,
    cisi: row.cisi || '-',
    region: norm(row.region),
    site: norm(row.site),
    type: norm(row.type),
    material: norm(row.material),
    shape: norm(row.shape),
    symbol: norm(row.symbol),
    text_length: norm(row['text length']),
    text: row.text,
    signs: tokens(row.text),
  }))
  .filter((row) => row.signs.length);

const dedupRows = [...new Map(allRows.map((row) => [row.signs.join(' '), row])).values()];
const externalRows = dedupRows.filter((row) => externalIds.has(row.id));
const backgroundRows = dedupRows.filter((row) => !externalIds.has(row.id));
const backgroundByType = byType(backgroundRows);
const observed = score(externalRows);
const observedSealC = score(externalRows.filter((row) => row.type === 'SEAL:C'));
const backgroundSealC = score(backgroundRows.filter((row) => row.type === 'SEAL:C'));

const rand = mulberry32(0x901407820 ^ externalRows.length);
let routeGe = 0;
let routeAndTerminalCleanGe = 0;
let sealCGe = 0;
const iterationRows = [];
for (let iter = 0; iter < ITERATIONS; iter += 1) {
  const sampled = externalRows.map((row) => {
    const candidates = backgroundByType.get(row.type) ?? backgroundRows;
    return candidates[Math.floor(rand() * candidates.length)];
  });
  const sampledScore = score(sampled);
  const sampledSealCScore = score(sampled.filter((row) => row.type === 'SEAL:C'));
  if (sampledScore.route_090091 >= observed.route_090091) routeGe += 1;
  if (sampledScore.route_090091 >= observed.route_090091 && sampledScore.terminal_002_820 <= observed.terminal_002_820) routeAndTerminalCleanGe += 1;
  if (sampledSealCScore.route_090091 >= observedSealC.route_090091) sealCGe += 1;
  if (iter < 200) {
    iterationRows.push({
      iter,
      route_090091: sampledScore.route_090091,
      terminal_002_820: sampledScore.terminal_002_820,
      sealc_route_090091: sampledSealCScore.route_090091,
    });
  }
}

const routeRows = externalRows.filter((row) => routeHit(row) || sign407Hit(row));
const terminal820Rows = externalRows.filter(terminal002820);
const any820Rows = externalRows.filter((row) => row.signs.includes('820'));
const typeSummary = [...byType(externalRows)].map(([type, rows]) => {
  const s = score(rows);
  const bg = score(backgroundRows.filter((row) => row.type === type));
  return {
    type,
    external_total: s.total,
    external_route_090091: s.route_090091,
    external_407: s.sign_407,
    external_002_820_terminal: s.terminal_002_820,
    background_total: bg.total,
    background_route_090091: bg.route_090091,
    background_407: bg.sign_407,
    background_002_820_terminal: bg.terminal_002_820,
  };
}).sort((a, b) => b.external_total - a.external_total);

const report = {
  run_date: '2026-05-31T14:16:00-07:00',
  tier: routeGe / ITERATIONS <= 0.01 ? 'candidate' : 'wild shot',
  risky_bet: 'External-contact Indus-style rows carry a route/register signal, not the new animal-terminal signal: signs 090/091 should be enriched in the external set, especially circular seals, while terminal 002-820 should be absent.',
  observed,
  observed_readable: `External exact-text-dedup rows: 090/091 in ${observed.route_090091}/${observed.total}; terminal 002-820 in ${observed.terminal_002_820}/${observed.total}; SEAL:C external 090/091 in ${observedSealC.route_090091}/${observedSealC.total} versus background SEAL:C ${backgroundSealC.route_090091}/${backgroundSealC.total}.`,
  type_matched_route_false_positive_rate: routeGe / ITERATIONS,
  type_matched_route_and_no_002820_false_positive_rate: routeAndTerminalCleanGe / ITERATIONS,
  sealc_route_false_positive_rate: sealCGe / ITERATIONS,
  interpretation: 'This is a candidate search discriminator: it says the V1 external bridge should chase 090/091 circular-route objects and 407 commodity/register objects, while keeping 820/Rhin in a separate animal-icon terminal lane.',
  non_claim: 'No sound value, language ID, translation, or object-level bilingual is claimed. The external object list is catalogue-mediated and remains source-check-gated.',
  falsifier: 'A source-checked external-contact batch with multiple terminal 002-820 animal rows, or loss of 090/091 enrichment after source validation and type-matched resampling, kills the discriminator.',
  route_rows: routeRows,
  any_820_rows: any820Rows,
  terminal_002_820_rows: terminal820Rows,
  type_summary: typeSummary,
};

fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
writeCsv(path.join(OUT_DIR, `${PREFIX}_route_rows.csv`), routeRows, [
  'id', 'cisi', 'region', 'site', 'type', 'material', 'shape', 'symbol', 'text_length', 'text',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_type_summary.csv`), typeSummary, [
  'type', 'external_total', 'external_route_090091', 'external_407', 'external_002_820_terminal',
  'background_total', 'background_route_090091', 'background_407', 'background_002_820_terminal',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_iterations.csv`), iterationRows, [
  'iter', 'route_090091', 'terminal_002_820', 'sealc_route_090091',
]);

console.log(JSON.stringify({
  tier: report.tier,
  observed: report.observed_readable,
  type_matched_route_false_positive_rate: report.type_matched_route_false_positive_rate,
  type_matched_route_and_no_002820_false_positive_rate: report.type_matched_route_and_no_002820_false_positive_rate,
  sealc_route_false_positive_rate: report.sealc_route_false_positive_rate,
  report: path.join(OUT_DIR, `${PREFIX}.json`),
}, null, 2));
