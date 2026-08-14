// Post-hoc skeptic check on the `002-390-X` claim. An earlier scan suggested that
// after the pair `002-390`, the next sign X deterministically decides whether the
// inscription ends. Because that head was picked after looking at the data, this
// script replays the same determinism test against every head, with duplicate texts
// removed first (canonical collapse), and asks where 390 really ranks. It reads
// metadata_filtered.csv, builds all `002-H-X` frames from unique sign sequences, and
// for each head with at least 6 rows and 3 branches runs a label-permutation test
// (exact when under 300k combinations, else 100,000 Monte Carlo shuffles). It then
// counts how many eligible and "competitive" heads (>=10 rows, >=5 branches) score
// as well as 390 and applies Bonferroni corrections for having scanned them all.
// Writes a bet summary (JSON + CSV), the full per-head table, and the raw frames
// to the reports directory.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_002390_canonical_all_head_posthoc_20260531';
const RUN_DATE = '2026-05-31';
const ITERATIONS = 100000;

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
  return text && text !== '-' && text !== 'None' ? text : fallback;
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function mulberry32(seed) {
  return function rand() {
    let t = (seed += 0x6D2B79F5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffle(rand, arr) {
  const out = [...arr];
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function combinations(items, k, limit = 300000) {
  const out = [];
  const combo = [];
  function rec(start) {
    if (out.length > limit) return;
    if (combo.length === k) {
      out.push([...combo]);
      return;
    }
    for (let i = start; i <= items.length - (k - combo.length); i += 1) {
      combo.push(items[i]);
      rec(i + 1);
      combo.pop();
    }
  }
  rec(0);
  return out;
}

function determinismScore(frames, continuingSet) {
  const byBranch = new Map();
  frames.forEach((frame, idx) => {
    if (!byBranch.has(frame.branch)) byBranch.set(frame.branch, []);
    byBranch.get(frame.branch).push(continuingSet.has(idx));
  });
  let score = 0;
  let pureBranches = 0;
  let mixedRepeatedBranches = 0;
  for (const labels of byBranch.values()) {
    const cont = labels.filter(Boolean).length;
    if (cont === 0 || cont === labels.length) pureBranches += 1;
    if (labels.length > 1 && cont > 0 && cont < labels.length) mixedRepeatedBranches += 1;
    score += Math.max(cont, labels.length - cont);
  }
  return { score, pureBranches, mixedRepeatedBranches };
}

function determinismP(frames) {
  const observedContinuing = new Set(frames.map((frame, idx) => (!frame.terminal ? idx : -1)).filter((idx) => idx >= 0));
  const observed = determinismScore(frames, observedContinuing);
  const n = frames.length;
  const k = observedContinuing.size;
  const indexes = frames.map((_, idx) => idx);
  const combos = combinations(indexes, k);
  if (combos.length <= 300000) {
    let ge = 0;
    for (const combo of combos) {
      const score = determinismScore(frames, new Set(combo));
      if (score.score >= observed.score) ge += 1;
    }
    return { ...observed, p: ge / combos.length, method: `exact_${combos.length}` };
  }
  const labels = frames.map((frame) => !frame.terminal);
  const rand = mulberry32(0xCA390 + n + k);
  let ge = 0;
  for (let iter = 0; iter < ITERATIONS; iter += 1) {
    const shuffled = shuffle(rand, labels);
    const continuing = new Set(shuffled.map((value, idx) => (value ? idx : -1)).filter((idx) => idx >= 0));
    const score = determinismScore(frames, continuing);
    if (score.score >= observed.score) ge += 1;
  }
  return { ...observed, p: ge / ITERATIONS, method: `monte_carlo_${ITERATIONS}` };
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const canonicalRows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()];

const frames = [];
for (const row of canonicalRows) {
  for (let i = 0; i < row.signs.length - 2; i += 1) {
    if (row.signs[i] !== '002') continue;
    const head = row.signs[i + 1];
    const branch = row.signs[i + 2];
    frames.push({
      id: row.id,
      object: objectId(row),
      site: norm(row.site),
      type: norm(row.type),
      symbol: norm(row.symbol),
      cult: norm(row.cult),
      shape: norm(row.shape),
      material: norm(row.material),
      prev: row.signs[i - 1] ?? '<START>',
      head,
      branch,
      terminal: i + 2 === row.signs.length - 1,
      tail: row.signs.slice(i + 3).join(' ') || '<END>',
      canonical_sequence: row.signs.join(' '),
      text: row.text,
    });
  }
}

const byHead = new Map();
for (const frame of frames) {
  if (!byHead.has(frame.head)) byHead.set(frame.head, []);
  byHead.get(frame.head).push(frame);
}

const headRows = [];
for (const [head, group] of byHead.entries()) {
  const branchCounts = new Map();
  for (const frame of group) branchCounts.set(frame.branch, (branchCounts.get(frame.branch) ?? 0) + 1);
  const branchCount = branchCounts.size;
  const repeatedBranchCount = [...branchCounts.values()].filter((count) => count > 1).length;
  const eligible = group.length >= 6 && branchCount >= 3;
  const test = eligible ? determinismP(group) : null;
  headRows.push({
    head,
    canonical_rows: group.length,
    branch_count: branchCount,
    repeated_branch_count: repeatedBranchCount,
    terminal_rows: group.filter((frame) => frame.terminal).length,
    continuing_rows: group.filter((frame) => !frame.terminal).length,
    determinism_score: test?.score ?? '',
    determinism_p: test?.p ?? '',
    method: test?.method ?? '',
    pure_branches: test?.pureBranches ?? '',
    mixed_repeated_branches: test?.mixedRepeatedBranches ?? '',
    branch_counts: [...branchCounts.entries()].map(([branch, count]) => `${branch}:${count}`).join(';'),
    examples: group.slice(0, 14).map((frame) => `${frame.object}:${frame.prev}-002-${frame.head}-${frame.branch}-${frame.tail}:${frame.terminal ? 'T' : 'C'}`).join('|'),
  });
}

headRows.sort((a, b) => {
  const ap = a.determinism_p === '' ? 2 : Number(a.determinism_p);
  const bp = b.determinism_p === '' ? 2 : Number(b.determinism_p);
  return ap - bp || Number(b.canonical_rows) - Number(a.canonical_rows);
});

const eligibleHeads = headRows.filter((row) => row.determinism_p !== '');
const competitiveHeads = eligibleHeads.filter((row) => Number(row.canonical_rows) >= 10 && Number(row.branch_count) >= 5);
const head390 = headRows.find((row) => row.head === '390');
const betterOrEqualEligible = eligibleHeads.filter((row) => Number(row.determinism_p) <= Number(head390.determinism_p));
const betterOrEqualCompetitive = competitiveHeads.filter((row) => Number(row.determinism_p) <= Number(head390.determinism_p));
const bonferroniEligible = Math.min(1, Number(head390.determinism_p) * eligibleHeads.length);
const bonferroniCompetitive = Math.min(1, Number(head390.determinism_p) * competitiveHeads.length);

const tier =
  Number(head390.determinism_p) <= 0.05 &&
  Number(head390.mixed_repeated_branches) === 0 &&
  betterOrEqualCompetitive.length <= 2
    ? 'candidate'
    : 'wild shot';

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V2_002390_CANONICAL_ALL_HEAD_POSTHOC_20260531',
  vector: 'V2 effective-unicity / all-frame skeptic',
  confidence_tier: tier,
  risky_bet:
    'The `002-390-X` branch-selector frame should survive a post-hoc all-head adversary: after canonical collapse, `390` should remain one of the few multi-branch `002-H-X` heads with branch-determined terminality.',
  observed:
    `Canonical rows=${canonicalRows.length}; eligible heads=${eligibleHeads.length}; competitive heads=${competitiveHeads.length}. ` +
    `Head 390 p=${head390.determinism_p}, score=${head390.determinism_score}/${head390.canonical_rows}, mixed repeated branches=${head390.mixed_repeated_branches}. ` +
    `Eligible heads <=390: ${betterOrEqualEligible.map((row) => row.head).join('/')}; competitive heads <=390: ${betterOrEqualCompetitive.map((row) => row.head).join('/')}. ` +
    `Bonferroni eligible=${bonferroniEligible}; Bonferroni competitive=${bonferroniCompetitive}.`,
  adversarial_test:
    `Canonical numeric-sequence collapse; scan every eligible 002-H-X head; terminal/continuing label permutations preserving each head's branch layout and continuation count; ${ITERATIONS} Monte Carlo only when exact enumeration is too large.`,
  false_positive_rate: head390.determinism_p,
  all_eligible_rank: `${betterOrEqualEligible.length}/${eligibleHeads.length}`,
  competitive_rank: `${betterOrEqualCompetitive.length}/${competitiveHeads.length}`,
  bonferroni_eligible_p: bonferroniEligible,
  bonferroni_competitive_p: bonferroniCompetitive,
  skeptic_verdict:
    bonferroniEligible <= 0.05
      ? '390 survives even broad multiple-comparison correction.'
      : '390 is the strongest eligible canonical 002-head in this scan, but the broad all-head multiple-comparison correction is not below 0.05; treat it as a slot-specific candidate, not a unique all-corpus anomaly.',
  falsifier:
    'If canonical source review introduces a mixed repeated branch under 390, or if many comparable heads show the same deterministic profile, demote the slot-specific claim.',
  next_prediction:
    'The productive path is to model 390 and 861 as two different branch-selector heads, not to force a single head to carry all 002-governed structure.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({ ...summary, head390, eligible_heads: eligibleHeads, competitive_heads: competitiveHeads, all_heads: headRows }, null, 2),
  'utf8',
);
writeCsv(path.join(OUT_DIR, `${PREFIX}.csv`), [summary], [
  'run_date',
  'bet_id',
  'vector',
  'confidence_tier',
  'risky_bet',
  'observed',
  'adversarial_test',
  'false_positive_rate',
  'all_eligible_rank',
  'competitive_rank',
  'bonferroni_eligible_p',
  'bonferroni_competitive_p',
  'skeptic_verdict',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_heads.csv`), headRows, [
  'head',
  'canonical_rows',
  'branch_count',
  'repeated_branch_count',
  'terminal_rows',
  'continuing_rows',
  'determinism_score',
  'determinism_p',
  'method',
  'pure_branches',
  'mixed_repeated_branches',
  'branch_counts',
  'examples',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_frames.csv`), frames, [
  'id',
  'object',
  'site',
  'type',
  'symbol',
  'cult',
  'shape',
  'material',
  'prev',
  'head',
  'branch',
  'terminal',
  'tail',
  'canonical_sequence',
  'text',
]);

console.log(JSON.stringify(summary, null, 2));
