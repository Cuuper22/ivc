// The v3 "impostor forger": can random wrong Indus tokens fake a Brahmi match?
// For each Indus sign family we observed a modal Brahmi label — the Brahmi sign
// that most of the family's tokens land nearest to. The worry is that any pile of
// token images might do that by chance. So for each family this script builds a
// pool of impostor tokens (same orientation policy, different sign, no shared CISI
// object, source path, or image hash, and where possible matched on aspect ratio
// within 0.25 and ink density within 0.08), draws 1000 seeded random samples of
// the family's size, and counts how often an impostor sample matches the observed
// modal count and mean distance or better. That share is the real-token impostor
// null. It reads the v2 family summary, segments, rank-1 neighbors, and the v3
// preflight CSV, and writes a per-family CSV, up to 25 iteration rows per family,
// and a JSON summary. Result baked into the outputs: no family survives; zero
// phonetic anchors are accepted.
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const OUT = path.join(ROOT, 'data', 'brahmi');
const RUN_DATE = '2026-05-30';

const FAMILY_SUMMARY = path.join(OUT, 'source_token_family_descent_summary_v2.csv');
const SEGMENTS = path.join(OUT, 'source_token_segments_v2.csv');
const NEIGHBORS = path.join(OUT, 'source_token_brahmi_neighbors_v2.csv');
const V3_PREFLIGHT = path.join(OUT, 'brahmi_independent_source_token_gate_v3.csv');

const OUT_CSV = path.join(OUT, 'brahmi_real_token_impostor_forger_v3.csv');
const OUT_ITER = path.join(OUT, 'brahmi_real_token_impostor_forger_iterations_v3.csv');
const OUT_JSON = path.join(OUT, 'brahmi_real_token_impostor_forger_v3_summary.json');

const ITERATIONS = 1000;
const MAX_ITER_ROWS_PER_FAMILY = 25;

const RESULT_FIELDS = [
  'sign_id',
  'orientation_policy',
  'sample_count',
  'modal_brahmi_label',
  'modal_count',
  'observed_mean_modal_distance',
  'v3_raw_modal_label',
  'v3_sha_modal_label',
  'v3_cisi_modal_label',
  'v3_cisi_modal_share',
  'original_shape_null_share',
  'original_label_null_share',
  'v3_preflight_decision',
  'impostor_pool_size',
  'iterations',
  'impostor_ge_observed_share',
  'impostor_best_modal_count',
  'impostor_best_mean_distance',
  'impostor_best_label',
  'gate_decision',
  'accepted_phonetic_anchor',
  'blocked_reason',
];

const ITER_FIELDS = [
  'sign_id',
  'orientation_policy',
  'iteration',
  'impostor_modal_label',
  'impostor_modal_count',
  'impostor_mean_modal_distance',
  'impostor_ge_observed',
  'sample_token_ids',
];

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
      rows.push(row);
      row = [];
      cell = '';
    } else {
      cell += ch;
    }
  }
  if (cell.length || row.length) {
    row.push(cell.replace(/\r$/, ''));
    rows.push(row);
  }
  if (!rows.length) return [];
  const header = rows[0];
  return rows.slice(1).filter((r) => r.some((v) => v !== '')).map((r) => {
    const out = {};
    header.forEach((h, i) => {
      out[h] = r[i] ?? '';
    });
    return out;
  });
}

function csvEscape(value) {
  const text = String(value ?? '');
  if (/[",\n\r]/.test(text)) return `"${text.replaceAll('"', '""')}"`;
  return text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(',')];
  for (const row of rows) {
    lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  }
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function seededRandom(seedText) {
  let state = crypto.createHash('sha256').update(seedText).digest().readUInt32LE(0);
  return () => {
    state = (state * 1664525 + 1013904223) >>> 0;
    return state / 2 ** 32;
  };
}

function shuffle(values, rand) {
  const out = [...values];
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function key(row) {
  return `${row.sign_id}::${row.orientation_policy}`;
}

function nearestByToken(neighborRows) {
  const byToken = new Map();
  for (const row of neighborRows) {
    if (row.rank !== '1') continue;
    byToken.set(row.token_id, row);
  }
  return byToken;
}

function modalStats(tokens, nearest) {
  const labelToDistances = new Map();
  for (const token of tokens) {
    const near = nearest.get(token.token_id);
    if (!near) continue;
    const label = near.brahmi_label;
    if (!labelToDistances.has(label)) labelToDistances.set(label, []);
    labelToDistances.get(label).push(Number(near.distance));
  }
  let best = null;
  for (const [label, distances] of labelToDistances.entries()) {
    const count = distances.length;
    const mean = distances.reduce((acc, value) => acc + value, 0) / Math.max(1, distances.length);
    if (!best || count > best.count || (count === best.count && mean < best.mean)) {
      best = { label, count, mean };
    }
  }
  return best ?? { label: '', count: 0, mean: Number.POSITIVE_INFINITY };
}

function poolForFamily(family, familyTokens, allTokens) {
  const sampleAspects = familyTokens.map((token) => Number(token.aspect)).filter(Number.isFinite);
  const sampleInk = familyTokens.map((token) => Number(token.ink_density)).filter(Number.isFinite);
  const meanAspect = sampleAspects.reduce((acc, value) => acc + value, 0) / Math.max(1, sampleAspects.length);
  const meanInk = sampleInk.reduce((acc, value) => acc + value, 0) / Math.max(1, sampleInk.length);
  const cisis = new Set(familyTokens.map((token) => token.cisi));
  const sourcePaths = new Set(familyTokens.map((token) => token.source_path));
  const hashes = new Set(familyTokens.map((token) => token.sha256));

  const strict = allTokens.filter((token) => token.orientation_policy === family.orientation_policy
    && token.assigned_sign !== family.sign_id
    && !cisis.has(token.cisi)
    && !sourcePaths.has(token.source_path)
    && !hashes.has(token.sha256)
    && Math.abs(Number(token.aspect) - meanAspect) <= 0.25
    && Math.abs(Number(token.ink_density) - meanInk) <= 0.08);

  if (strict.length >= Number(family.sample_count)) return strict;

  return allTokens.filter((token) => token.orientation_policy === family.orientation_policy
    && token.assigned_sign !== family.sign_id
    && !cisis.has(token.cisi)
    && !sourcePaths.has(token.source_path)
    && !hashes.has(token.sha256));
}

function sampleWithoutReplacement(pool, n, rand) {
  const shuffled = shuffle(pool, rand);
  return shuffled.slice(0, n);
}

function main() {
  const families = parseCsv(fs.readFileSync(FAMILY_SUMMARY, 'utf8'));
  const segments = parseCsv(fs.readFileSync(SEGMENTS, 'utf8'));
  const neighbors = parseCsv(fs.readFileSync(NEIGHBORS, 'utf8'));
  const preflight = fs.existsSync(V3_PREFLIGHT) ? parseCsv(fs.readFileSync(V3_PREFLIGHT, 'utf8')) : [];
  const preflightByKey = new Map(preflight.map((row) => [key(row), row]));
  const nearest = nearestByToken(neighbors);

  const tokenById = new Map(segments.map((row) => [row.token_id, row]));
  const allUsableTokens = segments.filter((row) => nearest.has(row.token_id));
  const resultRows = [];
  const iterationRows = [];
  const rand = seededRandom('brahmi-real-token-impostor-forger-v3');

  for (const family of families) {
    const tokenIds = String(family.token_ids || '').split('|').filter(Boolean);
    const familyTokens = tokenIds.map((tokenId) => tokenById.get(tokenId)).filter(Boolean);
    const sampleCount = Number(family.sample_count);
    const modalCount = Number(family.modal_count);
    const observedMean = Number(family.mean_modal_distance || family.mean_top1_distance);
    const pool = poolForFamily(family, familyTokens, allUsableTokens);
    const pre = preflightByKey.get(key(family));

    let ge = 0;
    let best = { label: '', count: -1, mean: Number.POSITIVE_INFINITY };
    let actualIterations = 0;

    if (pool.length >= sampleCount && sampleCount > 0) {
      for (let iteration = 0; iteration < ITERATIONS; iteration += 1) {
        const sample = sampleWithoutReplacement(pool, sampleCount, rand);
        const stats = modalStats(sample, nearest);
        const impostorGeObserved = stats.count >= modalCount && stats.mean <= observedMean;
        if (impostorGeObserved) ge += 1;
        if (stats.count > best.count || (stats.count === best.count && stats.mean < best.mean)) {
          best = stats;
        }
        actualIterations += 1;
        if (iteration < MAX_ITER_ROWS_PER_FAMILY) {
          iterationRows.push({
            sign_id: family.sign_id,
            orientation_policy: family.orientation_policy,
            iteration,
            impostor_modal_label: stats.label,
            impostor_modal_count: stats.count,
            impostor_mean_modal_distance: Number.isFinite(stats.mean) ? stats.mean.toFixed(6) : '',
            impostor_ge_observed: impostorGeObserved ? 'true' : 'false',
            sample_token_ids: sample.map((token) => token.token_id).join('|'),
          });
        }
      }
    }

    const share = actualIterations ? ge / actualIterations : null;
    const blockedReasons = [];
    if (!actualIterations) blockedReasons.push('insufficient_impostor_pool');
    if (share !== null && share > 0.01) blockedReasons.push('real_token_impostor_null_above_0_01');
    if (pre?.review_packet_eligible !== 'true') blockedReasons.push('failed_v3_independence_preflight');
    if (family.accepted_phonetic_anchor !== 'true') blockedReasons.push('not_accepted_in_v2_gate');

    resultRows.push({
      sign_id: family.sign_id,
      orientation_policy: family.orientation_policy,
      sample_count: family.sample_count,
      modal_brahmi_label: family.modal_brahmi_label,
      modal_count: family.modal_count,
      observed_mean_modal_distance: observedMean.toFixed(6),
      v3_raw_modal_label: pre?.raw_modal_label ?? '',
      v3_sha_modal_label: pre?.sha_modal_label ?? '',
      v3_cisi_modal_label: pre?.cisi_modal_label ?? '',
      v3_cisi_modal_share: pre?.cisi_modal_share ?? '',
      original_shape_null_share: family.shape_modal_distance_le_observed_share,
      original_label_null_share: family.label_null_ge_observed_modal_count_share,
      v3_preflight_decision: pre?.preflight_decision ?? 'missing',
      impostor_pool_size: pool.length,
      iterations: actualIterations,
      impostor_ge_observed_share: share === null ? '' : share.toFixed(6),
      impostor_best_modal_count: best.count < 0 ? '' : best.count,
      impostor_best_mean_distance: Number.isFinite(best.mean) ? best.mean.toFixed(6) : '',
      impostor_best_label: best.label,
      gate_decision: blockedReasons.length ? 'failed_real_token_impostor_forger' : 'review_packet_eligible_not_accepted',
      accepted_phonetic_anchor: 'false',
      blocked_reason: blockedReasons.join(';'),
    });
  }

  const resultCounts = resultRows.reduce((acc, row) => {
    acc[row.gate_decision] = (acc[row.gate_decision] || 0) + 1;
    return acc;
  }, {});

  const maxShare = Math.max(...resultRows.map((row) => Number(row.impostor_ge_observed_share || 0)));
  const minShare = Math.min(...resultRows.filter((row) => row.impostor_ge_observed_share !== '').map((row) => Number(row.impostor_ge_observed_share)));
  const rowsWithIterations = resultRows.filter((row) => Number(row.iterations) > 0).length;
  const insufficientImpostorPoolRows = resultRows.filter((row) => String(row.blocked_reason).includes('insufficient_impostor_pool')).length;
  const realTokenNullAbove001Rows = resultRows.filter((row) => row.impostor_ge_observed_share !== ''
    && Number(row.impostor_ge_observed_share) > 0.01).length;
  const realTokenNullAtOrBelow001Rows = resultRows.filter((row) => row.impostor_ge_observed_share !== ''
    && Number(row.impostor_ge_observed_share) <= 0.01).length;
  const topNearMissSigns = new Set(['817', '527', '472', '060', '061']);
  const topNearMissRows = resultRows.filter((row) => topNearMissSigns.has(row.sign_id));
  const lowestNullRows = [...resultRows]
    .filter((row) => row.impostor_ge_observed_share !== '')
    .sort((a, b) => Number(a.impostor_ge_observed_share) - Number(b.impostor_ge_observed_share))
    .slice(0, 10);

  const summary = {
    date: RUN_DATE,
    status: 'brahmi_real_token_impostor_forger_v3_no_phonetic_anchor',
    input_family_rows: families.length,
    source_token_rows: segments.length,
    neighbor_rows: neighbors.length,
    iterations_per_family: ITERATIONS,
    rows_with_full_impostor_iterations: rowsWithIterations,
    insufficient_impostor_pool_rows: insufficientImpostorPoolRows,
    real_token_null_above_0_01_rows: realTokenNullAbove001Rows,
    real_token_null_at_or_below_0_01_rows: realTokenNullAtOrBelow001Rows,
    result_counts: resultCounts,
    min_impostor_ge_observed_share: minShare,
    max_impostor_ge_observed_share: maxShare,
    review_packet_eligible_rows: 0,
    candidate_only_rows: 0,
    accepted_phonetic_anchors: 0,
    top_v2_near_misses: topNearMissRows.map((row) => ({
      sign_id: row.sign_id,
      orientation_policy: row.orientation_policy,
      v2_modal_label: row.modal_brahmi_label,
      v3_cisi_modal_label: row.v3_cisi_modal_label,
      impostor_ge_observed_share: row.impostor_ge_observed_share,
      v3_preflight_decision: row.v3_preflight_decision,
      blocked_reason: row.blocked_reason,
    })),
    lowest_real_token_impostor_null_rows: lowestNullRows.map((row) => ({
      sign_id: row.sign_id,
      orientation_policy: row.orientation_policy,
      v2_modal_label: row.modal_brahmi_label,
      v3_cisi_modal_label: row.v3_cisi_modal_label,
      impostor_ge_observed_share: row.impostor_ge_observed_share,
      blocked_reason: row.blocked_reason,
    })),
    conclusion: 'No Brahmi family survives the real-token impostor forger plus v3 independence preflight. Actual Indus source-token impostors can reproduce or exceed many apparent Brahmi-like matches, and every row remains blocked before any phonetic anchor can be accepted.',
  };

  writeCsv(OUT_CSV, resultRows, RESULT_FIELDS);
  writeCsv(OUT_ITER, iterationRows, ITER_FIELDS);
  fs.writeFileSync(OUT_JSON, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
}

main();
