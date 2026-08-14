// Tests whether the terminal-governor network is really about pairing, or
// just about frequency. A cheap alternative story: 002 and 060 are common
// second-to-last signs, 817/820/861/920/550 are common last signs, so their
// pairings pile up by coincidence. To rule that out we read the filtered
// corpus metadata (complete texts only), collapse to one family per exact
// text, take each family's penultimate and final sign, then shuffle the
// final signs across the penultimate slots 5000 times. That null keeps both
// marginal distributions and breaks only the pairing. We count how often
// chance reproduces the five target pairs at 20+ counts each, and the full
// target shape (002 paired with 817 and 820, 060 with 920/550/820, 820
// shared by both governors). Writes one JSON report.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_terminal_governor_penult_final_pairing_null_20260531';
const ITERATIONS = 5000;
const STRICT_MIN = 20;
const TARGET_PAIRS = new Set(['002-817', '002-820', '060-920', '060-550', '060-820']);

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

function score(penults, finals) {
  const counts = new Map();
  for (let i = 0; i < penults.length; i += 1) {
    const pair = `${penults[i]}-${finals[i]}`;
    counts.set(pair, (counts.get(pair) ?? 0) + 1);
  }
  const targetCounts = [...TARGET_PAIRS].map((pair) => ({ pair, count: counts.get(pair) ?? 0 }));
  const hitPairs = targetCounts.filter((row) => row.count >= STRICT_MIN).length;
  const minTargetCount = Math.min(...targetCounts.map((row) => row.count));
  const byPenult = new Map();
  const byFinal = new Map();
  for (const { pair, count } of targetCounts) {
    const [penult, final] = pair.split('-');
    if (count >= STRICT_MIN) {
      if (!byPenult.has(penult)) byPenult.set(penult, []);
      byPenult.get(penult).push(final);
      if (!byFinal.has(final)) byFinal.set(final, []);
      byFinal.get(final).push(penult);
    }
  }
  return {
    target_counts: targetCounts,
    target_hit_pairs_ge_min: hitPairs,
    min_target_count: minTargetCount,
    multi_penult_count: [...byPenult.values()].filter((values) => values.length >= 2).length,
    shared_final_count: [...byFinal.entries()].filter(([final, penultsForFinal]) => final === '820' && penultsForFinal.includes('002') && penultsForFinal.includes('060')).length,
    has_target_shape: hitPairs === TARGET_PAIRS.size
      && (byPenult.get('002') ?? []).includes('817')
      && (byPenult.get('002') ?? []).includes('820')
      && (byPenult.get('060') ?? []).includes('920')
      && (byPenult.get('060') ?? []).includes('550')
      && (byPenult.get('060') ?? []).includes('820')
      && (byFinal.get('820') ?? []).includes('002')
      && (byFinal.get('820') ?? []).includes('060'),
  };
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const familyMap = new Map();
for (const row of rows) {
  const toks = tokens(row.text);
  if (toks.length < 2) continue;
  const penult = toks[toks.length - 2];
  const final = toks[toks.length - 1];
  const key = row.text;
  if (!familyMap.has(key)) familyMap.set(key, { penult, final, text: row.text, sites: new Set(), cisis: new Set() });
  familyMap.get(key).sites.add(row.site);
  familyMap.get(key).cisis.add(row.cisi);
}

const terminalFamilies = [...familyMap.values()];
const penults = terminalFamilies.map((row) => row.penult);
const finals = terminalFamilies.map((row) => row.final);
const live = score(penults, finals);
const rand = mulberry32(0xF17A1);
let hitGe = 0;
let minGe = 0;
let multiGe = 0;
let sharedGe = 0;
let shape = 0;

for (let iter = 0; iter < ITERATIONS; iter += 1) {
  const shuffledFinals = fisherYates(finals, rand);
  const sim = score(penults, shuffledFinals);
  if (sim.target_hit_pairs_ge_min >= live.target_hit_pairs_ge_min) hitGe += 1;
  if (sim.min_target_count >= live.min_target_count) minGe += 1;
  if (sim.multi_penult_count >= live.multi_penult_count) multiGe += 1;
  if (sim.shared_final_count >= live.shared_final_count) sharedGe += 1;
  if (sim.has_target_shape) shape += 1;
}

const report = {
  date: '2026-05-31',
  phase: 'CONSOLIDATE',
  candidate_id: PREFIX,
  tier: 'promoted_candidate_strengthener',
  bet: 'The terminal-governor network is not just common penultimate signs paired with common final signs. It depends on specific penult-final pairing.',
  source: META,
  collapse_key: ['terminal inscription text'],
  null_model: 'Preserve each terminal family penultimate sign and the multiset of final signs; shuffle final signs across penultimate slots.',
  terminal_text_families: terminalFamilies.length,
  live,
  penult_final_shuffle_null: {
    iterations: ITERATIONS,
    p_target_hit_pairs_ge_live: hitGe / ITERATIONS,
    p_min_target_count_ge_live: minGe / ITERATIONS,
    p_multi_penult_count_ge_live: multiGe / ITERATIONS,
    p_shared_820_ge_live: sharedGe / ITERATIONS,
    p_reproduce_target_shape: shape / ITERATIONS,
  },
  decision: shape === 0 ? 'pairing_survives_penult_final_independence_null' : 'pairing_reproduced_by_penult_final_independence_null',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({
  candidate_id: PREFIX,
  decision: report.decision,
  terminal_text_families: terminalFamilies.length,
  live,
  null: report.penult_final_shuffle_null,
}, null, 2));
