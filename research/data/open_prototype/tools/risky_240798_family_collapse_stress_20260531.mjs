// Hostile follow-up to the 240-798 copper-axis result. That result rested on a few
// texts ending `240-798` that also carry signs 407/845/095. If those texts are
// really variants of one original, the evidence is one witness, not several. This
// script reruns the Fisher/max-stat test under three increasingly harsh grouping
// policies: exact text (each unique text counts once), axis_family (all 798-final
// texts with both 407 and 845 merge into a single family), and
// source_semantic_family (additionally merging the 095-bearing 798-final texts).
// For each policy it reads metadata_filtered.csv (complete rows only), collapses
// penult-240 rows into families, Fisher-tests the four axis flags against
// final=798, and runs a 5,000-iteration label-shuffle max-stat null. The claim
// survives only if the axis feature stays significant under the axis_family
// collapse with at least two positive families. Writes one JSON report to reports/.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT = path.join(ROOT, 'data', 'open_prototype', 'reports', 'risky_240798_family_collapse_stress_20260531.json');
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
    return logFact(r1) + logFact(r2) + logFact(c1) + logFact(c2)
      - logFact(x) - logFact(r1 - x) - logFact(c1 - x) - logFact(r2 - c1 + x) - logFact(n);
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

function baseUnit(row) {
  const t = toks(row.text);
  if (t.length < 2 || t[t.length - 2] !== '240') return null;
  return {
    text: row.text,
    final: t[t.length - 1],
    site: row.site,
    type: row.type,
    material: row.material,
    symbol: row.symbol,
    cisi: row.cisi,
    has407: t.includes('407'),
    has845: t.includes('845'),
    has095: t.includes('095'),
  };
}

function familyKey(unit, policy) {
  if (policy === 'exact_text') return unit.text;
  if (policy === 'axis_family') {
    if (unit.final === '798' && unit.has407 && unit.has845) return 'AXIS_407_845_240_798';
    return unit.text;
  }
  if (policy === 'source_semantic_family') {
    if (unit.final === '798' && unit.has407 && unit.has845) return 'AXIS_407_845_240_798';
    if (unit.final === '798' && unit.has095) return 'AXIS_095_240_798';
    return unit.text;
  }
  throw new Error(`unknown policy ${policy}`);
}

function collapse(rawUnits, policy) {
  const by = new Map();
  for (const unit of rawUnits) {
    const key = familyKey(unit, policy);
    if (!by.has(key)) {
      by.set(key, {
        key,
        final: unit.final,
        has407: false,
        has845: false,
        has095: false,
        members: [],
      });
    }
    const fam = by.get(key);
    fam.has407 ||= unit.has407;
    fam.has845 ||= unit.has845;
    fam.has095 ||= unit.has095;
    fam.members.push(unit);
  }
  return [...by.values()];
}

function features(unit) {
  const out = [];
  if (unit.has407) out.push('has_407');
  if (unit.has845) out.push('has_845');
  if (unit.has095) out.push('has_095');
  if (unit.has407 || unit.has845 || unit.has095) out.push('has_407_or_845_or_095');
  return out;
}

function stat(units, labels, feature) {
  let a = 0;
  let b = 0;
  let c = 0;
  let d = 0;
  for (let i = 0; i < units.length; i += 1) {
    const has = features(units[i]).includes(feature);
    const pos = labels[i];
    if (pos && has) a += 1;
    else if (pos) b += 1;
    else if (has) c += 1;
    else d += 1;
  }
  return { feature, a, b, c, d, fisher_p: fisherRight(a, b, c, d) };
}

function runPolicy(rawUnits, policy) {
  const units = collapse(rawUnits, policy);
  const labels = units.map((unit) => unit.final === '798');
  const allFeatures = ['has_407', 'has_845', 'has_095', 'has_407_or_845_or_095'];
  const stats = allFeatures.map((feature) => stat(units, labels, feature))
    .filter((row) => row.a > 0)
    .sort((x, y) => x.fisher_p - y.fisher_p || y.a - x.a || x.feature.localeCompare(y.feature))
    .map((row, idx, arr) => ({ ...row, rank: idx + 1, total_features: arr.length }));
  const target = stats.find((row) => row.feature === 'has_407_or_845_or_095');
  const rand = mulberry32(0x240798 + policy.length);
  let maxstat = 0;
  for (let iter = 0; iter < ITERATIONS; iter += 1) {
    const shuffled = shuffle(labels, rand);
    let minP = 1;
    for (const feature of allFeatures) {
      const p = stat(units, shuffled, feature).fisher_p;
      if (p < minP) minP = p;
    }
    if (target && minP <= target.fisher_p) maxstat += 1;
  }
  return {
    policy,
    family_count: units.length,
    final_distribution: Object.fromEntries([...units.reduce((map, unit) => {
      map.set(unit.final, (map.get(unit.final) ?? 0) + 1);
      return map;
    }, new Map()).entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))),
    target_feature: target ? { ...target, maxstat_fpr: maxstat / ITERATIONS } : null,
    top_features: stats,
    axis_families: units.filter((unit) => features(unit).includes('has_407_or_845_or_095')).map((unit) => ({
      key: unit.key,
      final: unit.final,
      has407: unit.has407,
      has845: unit.has845,
      has095: unit.has095,
      members: unit.members.map((member) => `${member.cisi}:${member.text}`),
    })),
  };
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const rawUnitsByText = new Map();
for (const row of rawRows) {
  const unit = baseUnit(row);
  if (!unit) continue;
  if (!rawUnitsByText.has(unit.text)) rawUnitsByText.set(unit.text, unit);
  else {
    const current = rawUnitsByText.get(unit.text);
    current.has407 ||= unit.has407;
    current.has845 ||= unit.has845;
    current.has095 ||= unit.has095;
  }
}
const rawUnits = [...rawUnitsByText.values()];
const panels = ['exact_text', 'axis_family', 'source_semantic_family'].map((policy) => runPolicy(rawUnits, policy));
const hard = panels.find((panel) => panel.policy === 'axis_family');
const decision = hard.target_feature && hard.target_feature.a >= 2 && hard.target_feature.maxstat_fpr <= 0.05
  ? 'survives_axis_family_collapse_but_fragile'
  : 'demote_240798_axis_after_family_collapse';

const report = {
  date: '2026-05-31',
  phase: 'EXPAND',
  candidate_id: 'risky_240798_family_collapse_stress_20260531',
  tier: decision.startsWith('survives') ? 'candidate_fragile' : 'demoted',
  bet: 'The 240-798 copper-axis split survives after collapsing the repeated 407/845 240-798 witnesses into one source/semantic family.',
  source: META,
  panels,
  decision,
  caveat: 'This is still tiny: after hostile collapse, the positive axis support is two families, not three rows.',
};

fs.writeFileSync(OUT, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({
  candidate_id: report.candidate_id,
  tier: report.tier,
  decision,
  panels: panels.map((panel) => ({
    policy: panel.policy,
    family_count: panel.family_count,
    final_distribution: panel.final_distribution,
    target_feature: panel.target_feature,
  })),
}, null, 2));
