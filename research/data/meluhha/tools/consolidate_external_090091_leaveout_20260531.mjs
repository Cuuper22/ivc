import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const EXTERNAL = path.join(ROOT, 'data', 'meluhha', 'external_indus_objects.csv');
const OUT_DIR = path.join(ROOT, 'data', 'meluhha');
const PREFIX = 'consolidate_external_090091_leaveout_20260531';
const ITERATIONS = 25000;

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

function groupBy(rows, field) {
  const out = new Map();
  for (const row of rows) {
    if (!out.has(row[field])) out.set(row[field], []);
    out.get(row[field]).push(row);
  }
  return out;
}

function score(rows) {
  const sealC = rows.filter((row) => row.type === 'SEAL:C');
  return {
    total: rows.length,
    route_090091: rows.filter(routeHit).length,
    route_share: rows.length ? rows.filter(routeHit).length / rows.length : 0,
    terminal_002_820: rows.filter(terminal002820).length,
    sealc_total: sealC.length,
    sealc_route_090091: sealC.filter(routeHit).length,
    sealc_route_share: sealC.length ? sealC.filter(routeHit).length / sealC.length : 0,
  };
}

function sampleControl(targetRows, backgroundByType, backgroundRows, rand) {
  return targetRows.map((row) => {
    const candidates = backgroundByType.get(row.type) ?? backgroundRows;
    return candidates[Math.floor(rand() * candidates.length)];
  });
}

function nullRates(targetRows, observedScore, backgroundByType, backgroundRows, seed) {
  const rand = mulberry32(seed);
  let routeGe = 0;
  let routeAndNo820Ge = 0;
  let sealCGe = 0;
  for (let iter = 0; iter < ITERATIONS; iter += 1) {
    const sampled = sampleControl(targetRows, backgroundByType, backgroundRows, rand);
    const s = score(sampled);
    if (s.route_090091 >= observedScore.route_090091) routeGe += 1;
    if (s.route_090091 >= observedScore.route_090091 && s.terminal_002_820 <= observedScore.terminal_002_820) routeAndNo820Ge += 1;
    if (s.sealc_route_090091 >= observedScore.sealc_route_090091) sealCGe += 1;
  }
  return {
    type_matched_route_fpr: routeGe / ITERATIONS,
    type_matched_route_and_no_002820_fpr: routeAndNo820Ge / ITERATIONS,
    sealc_route_fpr: sealCGe / ITERATIONS,
  };
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
    text: row.text,
    signs: tokens(row.text),
  }))
  .filter((row) => row.signs.length);

const dedupRows = [...new Map(allRows.map((row) => [row.signs.join(' '), row])).values()];
const externalRows = dedupRows.filter((row) => externalIds.has(row.id));
const backgroundRows = dedupRows.filter((row) => !externalIds.has(row.id));
const backgroundByType = groupBy(backgroundRows, 'type');
const observed = score(externalRows);
const observedNull = nullRates(externalRows, observed, backgroundByType, backgroundRows, 0x9091);

const leaveSiteRows = [...groupBy(externalRows, 'site')].map(([site, rows], idx) => {
  const kept = externalRows.filter((row) => row.site !== site);
  const s = score(kept);
  const nulls = nullRates(kept, s, backgroundByType, backgroundRows, 0x5100 + idx);
  return {
    removed_group: site,
    removed_kind: 'site',
    removed_total: rows.length,
    removed_route_090091: rows.filter(routeHit).length,
    kept_total: s.total,
    kept_route_090091: s.route_090091,
    kept_route_share: s.route_share.toFixed(6),
    kept_sealc_total: s.sealc_total,
    kept_sealc_route_090091: s.sealc_route_090091,
    kept_sealc_route_share: s.sealc_route_share.toFixed(6),
    type_matched_route_fpr: nulls.type_matched_route_fpr,
    sealc_route_fpr: nulls.sealc_route_fpr,
  };
}).sort((a, b) => b.type_matched_route_fpr - a.type_matched_route_fpr || b.removed_route_090091 - a.removed_route_090091);

const leaveRegionRows = [...groupBy(externalRows, 'region')].map(([region, rows], idx) => {
  const kept = externalRows.filter((row) => row.region !== region);
  const s = score(kept);
  const nulls = nullRates(kept, s, backgroundByType, backgroundRows, 0x9000 + idx);
  return {
    removed_group: region,
    removed_kind: 'region',
    removed_total: rows.length,
    removed_route_090091: rows.filter(routeHit).length,
    kept_total: s.total,
    kept_route_090091: s.route_090091,
    kept_route_share: s.route_share.toFixed(6),
    kept_sealc_total: s.sealc_total,
    kept_sealc_route_090091: s.sealc_route_090091,
    kept_sealc_route_share: s.sealc_route_share.toFixed(6),
    type_matched_route_fpr: nulls.type_matched_route_fpr,
    sealc_route_fpr: nulls.sealc_route_fpr,
  };
}).sort((a, b) => b.type_matched_route_fpr - a.type_matched_route_fpr || b.removed_route_090091 - a.removed_route_090091);

const fragileSiteRows = leaveSiteRows.filter((row) => row.type_matched_route_fpr > 0.01);
const fragileRegionRows = leaveRegionRows.filter((row) => row.type_matched_route_fpr > 0.01);

const report = {
  run_date: '2026-05-31T14:55:00-07:00',
  phase: 'CONSOLIDATE',
  candidate_under_attack: '090/091 external route/register enrichment',
  observed,
  observed_nulls: observedNull,
  hostile_leaveout_result: {
    fragile_site_count: fragileSiteRows.length,
    fragile_region_count: fragileRegionRows.length,
    worst_site: leaveSiteRows[0],
    worst_region: leaveRegionRows[0],
  },
  decision: fragileRegionRows.length || fragileSiteRows.length
    ? 'demote: route signal is real but not robust to all leave-one-group cuts'
    : 'survives leave-one-site and leave-one-region cuts at candidate tier',
  interpretation: 'This tests whether the external 090/091 signal is carried by one overfit site or region cluster rather than a portable route/register lane.',
};

fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
writeCsv(path.join(OUT_DIR, `${PREFIX}_leave_site.csv`), leaveSiteRows, [
  'removed_kind', 'removed_group', 'removed_total', 'removed_route_090091', 'kept_total', 'kept_route_090091',
  'kept_route_share', 'kept_sealc_total', 'kept_sealc_route_090091', 'kept_sealc_route_share',
  'type_matched_route_fpr', 'sealc_route_fpr',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_leave_region.csv`), leaveRegionRows, [
  'removed_kind', 'removed_group', 'removed_total', 'removed_route_090091', 'kept_total', 'kept_route_090091',
  'kept_route_share', 'kept_sealc_total', 'kept_sealc_route_090091', 'kept_sealc_route_share',
  'type_matched_route_fpr', 'sealc_route_fpr',
]);

console.log(JSON.stringify({
  observed,
  observed_nulls: observedNull,
  worst_site: leaveSiteRows[0],
  worst_region: leaveRegionRows[0],
  decision: report.decision,
  report: path.join(OUT_DIR, `${PREFIX}.json`),
}, null, 2));
