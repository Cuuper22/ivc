import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT = path.join(ROOT, 'data', 'open_prototype', 'reports', 'risky_740x590_filler_context_stress_20260531.json');
const FILLERS = ['390', '405', '407', '406'];

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
      } else if (ch === '"') quoted = false;
      else cell += ch;
    } else if (ch === '"') quoted = true;
    else if (ch === ',') {
      row.push(cell);
      cell = '';
    } else if (ch === '\n') {
      row.push(cell.replace(/\r$/, ''));
      if (row.some((value) => value.length)) rows.push(row);
      row = [];
      cell = '';
    } else cell += ch;
  }
  if (cell.length || row.length) {
    row.push(cell.replace(/\r$/, ''));
    if (row.some((value) => value.length)) rows.push(row);
  }
  const [header, ...body] = rows;
  return body.map((cols) => Object.fromEntries(header.map((name, idx) => [name, cols[idx] ?? ''])));
}

function toks(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function triples(row) {
  const tokens = toks(row.text);
  const out = [];
  for (let i = 0; i < tokens.length - 2; i += 1) {
    if (tokens[i] === '740' && tokens[i + 2] === '590') out.push(tokens[i + 1]);
  }
  return out;
}

function collapse(rows) {
  const map = new Map();
  for (const row of rows) {
    const key = `${row.filler}|${row.text}`;
    if (!map.has(key)) map.set(key, row);
  }
  return [...map.values()];
}

function logFactorial(n) {
  let total = 0;
  for (let i = 2; i <= n; i += 1) total += Math.log(i);
  return total;
}

function fisherRight(a, b, c, d) {
  const r1 = a + b;
  const r2 = c + d;
  const c1 = a + c;
  const c2 = b + d;
  const n = r1 + r2;
  const maxA = Math.min(r1, c1);
  function logHyper(x) {
    return logFactorial(r1) + logFactorial(r2) + logFactorial(c1) + logFactorial(c2)
      - logFactorial(x) - logFactorial(r1 - x) - logFactorial(c1 - x)
      - logFactorial(r2 - c1 + x) - logFactorial(n);
  }
  let p = 0;
  for (let x = a; x <= maxA; x += 1) p += Math.exp(logHyper(x));
  return Math.min(1, p);
}

function contextFeatures(row) {
  const fields = ['site', 'region', 'type', 'material', 'shape', 'symbol', 'condition', 'complete', 'class'];
  const features = [];
  for (const field of fields) {
    const value = row[field] || 'NA';
    features.push(`${field}=${value}`);
  }
  features.push(`type_symbol=${row.type || 'NA'}|${row.symbol || 'NA'}`);
  features.push(`type_material=${row.type || 'NA'}|${row.material || 'NA'}`);
  return features;
}

function statsForFiller(rows, filler) {
  const targetRows = rows.filter((row) => row.filler === filler);
  const otherRows = rows.filter((row) => row.filler !== filler);
  const features = new Set(rows.flatMap(contextFeatures));
  const stats = [];
  for (const feature of features) {
    const a = targetRows.filter((row) => contextFeatures(row).includes(feature)).length;
    const b = targetRows.length - a;
    const c = otherRows.filter((row) => contextFeatures(row).includes(feature)).length;
    const d = otherRows.length - c;
    if (a > 0) stats.push({ feature, a, b, c, d, fisher_p: fisherRight(a, b, c, d) });
  }
  stats.sort((x, y) => x.fisher_p - y.fisher_p || y.a - x.a || x.feature.localeCompare(y.feature));
  return stats.map((row, idx) => ({ ...row, rank: idx + 1, total_features: stats.length }));
}

const raw = parseCsv(fs.readFileSync(META, 'utf8'));
const tripleRows = [];
for (const row of raw) {
  for (const filler of triples(row)) {
    tripleRows.push({ ...row, filler, triple: `740-${filler}-590` });
  }
}
const collapsed = collapse(tripleRows);
const counts = FILLERS.map((filler) => ({
  filler,
  raw_rows: tripleRows.filter((row) => row.filler === filler).length,
  exact_text_rows: collapsed.filter((row) => row.filler === filler).length,
}));
const fillerStats = Object.fromEntries(FILLERS.map((filler) => [filler, statsForFiller(collapsed, filler).slice(0, 12)]));

const decision = (() => {
  const s405 = fillerStats['405'] ?? [];
  const s407 = fillerStats['407'] ?? [];
  const has405Bull = s405.some((row) => row.feature.includes('Bull1:W') && row.fisher_p <= 0.05);
  const has407Gavi = s407.some((row) => row.feature.includes('Gavi') && row.fisher_p <= 0.05);
  return has405Bull || has407Gavi
    ? 'wild_shot_survives_as_context_sorted_frame'
    : 'demote_frame_to_frequency_pattern';
})();

const report = {
  date: '2026-05-31',
  phase: 'CONSOLIDATE',
  candidate_id: 'risky_740x590_filler_context_stress_20260531',
  bet: '740-X-590 is a register-slot frame whose filler X sorts context class; specifically 405 should skew Bull1:W/square-seal contexts and 407 should skew Gavi/TAB:B/admin contexts if the frame is meaningful.',
  source: META,
  counts,
  exact_text_collapsed_rows: collapsed.length,
  filler_context_stats: fillerStats,
  examples: Object.fromEntries(FILLERS.map((filler) => [
    filler,
    collapsed.filter((row) => row.filler === filler).slice(0, 8).map((row) => ({
      id: row.id,
      cisi: row.cisi,
      site: row.site,
      type: row.type,
      material: row.material,
      symbol: row.symbol,
      text: row.text,
    })),
  ])),
  decision,
  caveat:
    'This is a frame-internal context test only. It does not assign a value to any filler and does not rescue the killed external-personnel reading of 390.',
};

fs.writeFileSync(OUT, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({
  candidate_id: report.candidate_id,
  decision,
  counts,
  top_405: fillerStats['405']?.slice(0, 5),
  top_407: fillerStats['407']?.slice(0, 5),
  top_390: fillerStats['390']?.slice(0, 5),
}, null, 2));
