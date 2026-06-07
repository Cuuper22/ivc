import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT = path.join(ROOT, 'data', 'open_prototype', 'reports', 'risky_240798_copper_axis_split_20260531.json');
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

function logFact(n) {
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
  function lh(x) {
    return logFact(r1) + logFact(r2) + logFact(c1) + logFact(c2) - logFact(x) - logFact(r1 - x) - logFact(c1 - x) - logFact(r2 - c1 + x) - logFact(n);
  }
  let p = 0;
  for (let x = a; x <= maxA; x += 1) p += Math.exp(lh(x));
  return Math.min(1, p);
}

function mulberry32(seed) {
  return function rand() {
    let t = seed += 0x6D2B79F5;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffle(values, rand) {
  const out = values.slice();
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function features(unit) {
  const out = [];
  for (const field of ['site', 'type', 'material', 'symbol']) {
    for (const value of unit[field]) out.push(`${field}=${value}`);
  }
  if (unit.has407) out.push('has_407');
  if (unit.has845) out.push('has_845');
  if (unit.has095) out.push('has_095');
  if (unit.has407 || unit.has845 || unit.has095) out.push('has_407_or_845_or_095');
  if (unit.material.has('Copper') || unit.type.has('TAB:C')) out.push('copper_or_TAB_C');
  return out;
}

function collapseRows(rows) {
  const byText = new Map();
  for (const row of rows) {
    const t = toks(row.text);
    if (t.length < 2 || t[t.length - 2] !== '240') continue;
    if (!byText.has(row.text)) {
      byText.set(row.text, {
        text: row.text,
        final: t[t.length - 1],
        site: new Set(),
        type: new Set(),
        material: new Set(),
        symbol: new Set(),
        cisi: new Set(),
        has407: false,
        has845: false,
        has095: false,
      });
    }
    const unit = byText.get(row.text);
    unit.site.add(row.site);
    unit.type.add(row.type);
    unit.material.add(row.material);
    unit.symbol.add(row.symbol);
    unit.cisi.add(row.cisi);
    unit.has407 ||= t.includes('407');
    unit.has845 ||= t.includes('845');
    unit.has095 ||= t.includes('095');
  }
  return [...byText.values()];
}

function statForFeature(units, labels, feature) {
  let a = 0;
  let b = 0;
  let c = 0;
  let d = 0;
  for (let i = 0; i < units.length; i += 1) {
    const hasFeature = features(units[i]).includes(feature);
    const positive = labels[i];
    if (positive && hasFeature) a += 1;
    else if (positive) b += 1;
    else if (hasFeature) c += 1;
    else d += 1;
  }
  return { feature, a, b, c, d, fisher_p: fisherRight(a, b, c, d) };
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const units = collapseRows(rows);
const labels = units.map((unit) => unit.final === '798');
const allFeatures = [...new Set(units.flatMap(features))];
const stats = allFeatures.map((feature) => statForFeature(units, labels, feature))
  .filter((row) => row.a > 0)
  .sort((x, y) => x.fisher_p - y.fisher_p || y.a - x.a || x.feature.localeCompare(y.feature))
  .map((row, idx, arr) => ({ ...row, rank: idx + 1, total_features: arr.length }));
const target = stats.find((row) => row.feature === 'has_407_or_845_or_095');
const rand = mulberry32(0x240798);
let maxstat = 0;
for (let iter = 0; iter < ITERATIONS; iter += 1) {
  const shuffled = shuffle(labels, rand);
  let minP = 1;
  for (const feature of allFeatures) {
    const p = statForFeature(units, shuffled, feature).fisher_p;
    if (p < minP) minP = p;
  }
  if (target && minP <= target.fisher_p) maxstat += 1;
}

const report = {
  date: '2026-05-31',
  phase: 'EXPAND',
  candidate_id: 'risky_240798_copper_axis_split_20260531',
  tier: target && target.a >= 3 && maxstat / ITERATIONS <= 0.05 ? 'candidate' : 'wild shot',
  bet: 'Within terminal 240 rows, closure 798 selects the 407/845/095 copper-administrative axis while closure 235 avoids it.',
  source: META,
  exact_text_240_rows: units.length,
  positive_label: 'final=798',
  target_feature: target ? { ...target, maxstat_fpr: maxstat / ITERATIONS } : null,
  top_context_features_for_240_798: stats.slice(0, 12),
  rows: units.map((unit) => ({
    text: unit.text,
    final: unit.final,
    sites: [...unit.site],
    types: [...unit.type],
    materials: [...unit.material],
    symbols: [...unit.symbol],
    has407: unit.has407,
    has845: unit.has845,
    has095: unit.has095,
    cisis: [...unit.cisi].slice(0, 8),
  })),
  decision: target && target.a >= 3 && maxstat / ITERATIONS <= 0.05
    ? 'candidate_240798_copper_axis_split'
    : 'wild_shot_not_promoted',
  caveat: 'Support is very small: 5 rows have final 798 and only 3 carry 407/845/095. This is a candidate to attack, not a semantic claim.',
};

fs.writeFileSync(OUT, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({
  candidate_id: report.candidate_id,
  tier: report.tier,
  decision: report.decision,
  target_feature: report.target_feature,
  top_context_features_for_240_798: report.top_context_features_for_240_798.slice(0, 8),
}, null, 2));
