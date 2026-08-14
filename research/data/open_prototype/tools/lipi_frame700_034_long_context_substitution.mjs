import fs from 'node:fs';
import path from 'node:path';

// The substitution question: when a two-sided tablet carries +700-034+ instead of +700-033+
// or +700-032+, does anything on the object's long companion side co-vary with that choice?
// If 034 tablets systematically share long-side signs that 033/032 tablets lack, the three
// subtypes may be doing real contrastive work. This script reads the triad packet (one 034
// target plus its 033 and 032 controls per row), the matched-contrast stability grades, and
// the two-lane source packet. For every candidate long-side token, and separately for every
// whole long-side token-set "family", it counts how often the candidate appears with 034
// versus the controls and scores the difference. Significance comes from a permutation null:
// 5,000 iterations of randomly shuffling the 034/033/032 labels within each triad (seeded
// xorshift RNG, so runs are reproducible), with Benjamini-Hochberg correction across
// candidates. Tests run over five nested scopes, from all triads down to the core two-lane
// packet. Outputs: token-test CSV, family-test CSV, per-scope row CSV, and a JSON summary.
// This is source-blind statistics on catalog transcriptions; it accepts no sign readings.

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const triadPath = path.join(reportsDir, 'lipi_frame700_034_source_triad_packet.csv');
const stabilityPath = path.join(reportsDir, 'lipi_frame700_034_matched_contrast_stability.csv');
const packetPath = path.join(reportsDir, 'lipi_frame700_034_two_lane_source_packet.csv');

const tokenCsvPath = path.join(reportsDir, 'lipi_frame700_034_long_context_token_tests.csv');
const familyCsvPath = path.join(reportsDir, 'lipi_frame700_034_long_context_family_tests.csv');
const rowCsvPath = path.join(reportsDir, 'lipi_frame700_034_long_context_scope_rows.csv');
const summaryJsonPath = path.join(reportsDir, 'lipi_frame700_034_long_context_substitution_summary.json');

const iterations = 5000;
const labelOrder = ['034', '033', '032'];
const permutations = [
  [0, 1, 2],
  [0, 2, 1],
  [1, 0, 2],
  [1, 2, 0],
  [2, 0, 1],
  [2, 1, 0],
];

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQuotes) {
      if (c === '"') {
        if (text[i + 1] === '"') {
          field += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        field += c;
      }
    } else if (c === '"') {
      inQuotes = true;
    } else if (c === ',') {
      row.push(field);
      field = '';
    } else if (c === '\n') {
      row.push(field);
      field = '';
      if (row.length > 1 || row[0] !== '') rows.push(row);
      row = [];
    } else if (c !== '\r') {
      field += c;
    }
  }
  if (field.length || row.length) {
    row.push(field);
    rows.push(row);
  }
  return rows;
}

function readCsvRecords(filePath) {
  const rows = parseCsv(fs.readFileSync(filePath, 'utf8'));
  const header = rows[0];
  return rows.slice(1).map((row) => Object.fromEntries(header.map((name, index) => [name, row[index] ?? ''])));
}

function toCsv(rows) {
  return `${rows
    .map((row) =>
      row
        .map((value) => {
          const text = String(value ?? '');
          return `"${text.replaceAll('"', '""')}"`;
        })
        .join(','),
    )
    .join('\n')}\n`;
}

function splitSet(value) {
  return String(value ?? '')
    .split(';')
    .map((item) => item.trim())
    .filter(Boolean);
}

function countBy(rows, keyFn) {
  const counts = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return Object.fromEntries([...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])));
}

function number(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function makeRng(seed) {
  let state = seed >>> 0;
  return () => {
    state ^= state << 13;
    state ^= state >>> 17;
    state ^= state << 5;
    return (state >>> 0) / 4294967296;
  };
}

function bh(rows, pKey, outKey) {
  const sorted = rows
    .filter((row) => Number.isFinite(row[pKey]))
    .sort((a, b) => a[pKey] - b[pKey]);
  let prev = 1;
  for (let i = sorted.length - 1; i >= 0; i--) {
    const raw = (sorted[i][pKey] * sorted.length) / (i + 1);
    prev = Math.min(prev, raw);
    sorted[i][outKey] = Math.min(1, prev);
  }
  for (const row of rows) {
    if (!Number.isFinite(row[outKey])) row[outKey] = '';
  }
}

function labelCounts(triads, feature, candidate) {
  const counts = { '034': 0, '033': 0, '032': 0 };
  for (const triad of triads) {
    for (const label of labelOrder) {
      if (triad[feature][label].has(candidate)) counts[label]++;
    }
  }
  return counts;
}

function score(counts) {
  return counts['034'] - (counts['033'] + counts['032']) / 2;
}

function runFeatureTests(scopeName, triads, feature, minAny) {
  const candidates = new Set();
  for (const triad of triads) {
    for (const label of labelOrder) {
      for (const value of triad[feature][label]) candidates.add(value);
    }
  }

  const rows = [];
  const candidateList = [...candidates].sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
  const rng = makeRng(0x034700 + triads.length + candidateList.length + (feature === 'long_tokens' ? 11 : 29));
  const nullScoresByCandidate = new Map(candidateList.map((candidate) => [candidate, []]));

  for (const candidate of candidateList) {
    const counts = labelCounts(triads, feature, candidate);
    const anyCount = triads.filter((triad) => labelOrder.some((label) => triad[feature][label].has(candidate))).length;
    if (anyCount < minAny) continue;
    rows.push({
      scope: scopeName,
      feature,
      candidate,
      triads: triads.length,
      any_triads: anyCount,
      hit_034: counts['034'],
      hit_033: counts['033'],
      hit_032: counts['032'],
      observed_delta: score(counts),
      p_ge: 0,
      null_mean: 0,
      null_p95: 0,
      q_bh: '',
      status: 'source_blind_substitution_only',
    });
  }

  const rowByCandidate = new Map(rows.map((row) => [row.candidate, row]));

  for (let iter = 0; iter < iterations; iter++) {
    const countsByCandidate = new Map(rows.map((row) => [row.candidate, { '034': 0, '033': 0, '032': 0 }]));
    for (const triad of triads) {
      const perm = permutations[Math.floor(rng() * permutations.length)];
      for (let assignedIndex = 0; assignedIndex < labelOrder.length; assignedIndex++) {
        const assignedLabel = labelOrder[assignedIndex];
        const sourceLabel = labelOrder[perm[assignedIndex]];
        for (const candidate of triad[feature][sourceLabel]) {
          const counts = countsByCandidate.get(candidate);
          if (counts) counts[assignedLabel]++;
        }
      }
    }
    for (const [candidate, counts] of countsByCandidate.entries()) {
      nullScoresByCandidate.get(candidate).push(score(counts));
    }
  }

  for (const row of rows) {
    const nullScores = nullScoresByCandidate.get(row.candidate).sort((a, b) => a - b);
    const ge = nullScores.filter((value) => value >= row.observed_delta).length;
    row.p_ge = ge / nullScores.length;
    row.null_mean = nullScores.reduce((sum, value) => sum + value, 0) / nullScores.length;
    row.null_p95 = nullScores[Math.floor(0.95 * (nullScores.length - 1))];
  }

  bh(rows, 'p_ge', 'q_bh');
  rows.sort(
    (a, b) =>
      a.q_bh - b.q_bh ||
      b.observed_delta - a.observed_delta ||
      b.hit_034 - a.hit_034 ||
      a.candidate.localeCompare(b.candidate, undefined, { numeric: true }),
  );
  return rows;
}

function asSet(values) {
  return new Set(values.filter(Boolean));
}

const triadRows = readCsvRecords(triadPath);
const stabilityRows = readCsvRecords(stabilityPath);
const packetRows = readCsvRecords(packetPath);

const stabilityByTarget = new Map(stabilityRows.map((row) => [row.target_cisi, row]));
const packetTargets = new Map();
for (const row of packetRows.filter((item) => item.role === 'target_034')) {
  packetTargets.set(row.cisi, row);
}

const triads = triadRows.map((row) => {
  const stability = stabilityByTarget.get(row.target_cisi) ?? {};
  const packet = packetTargets.get(row.target_cisi);
  return {
    target_cisi: row.target_cisi,
    triad_rank: row.triad_rank,
    independence_rank: stability.independence_rank ?? '',
    grade: stability.grade ?? '',
    copy_pressure: stability.copy_pressure ?? '',
    packet_lane: packet?.lane ?? 'not_in_two_lane_packet',
    packet_priority: packet?.priority ?? 'not_in_two_lane_packet',
    long_tokens: {
      '034': asSet(splitSet(row.target_long_token_set)),
      '033': asSet(splitSet(row.control_033_long_token_set)),
      '032': asSet(splitSet(row.control_032_long_token_set)),
    },
    long_family: {
      '034': asSet([row.target_long_token_set]),
      '033': asSet([row.control_033_long_token_set]),
      '032': asSet([row.control_032_long_token_set]),
    },
  };
});

const strongGrades = new Set([
  'A_strict_local_minimal_contrast',
  'B_visual_object_order_matched',
  'C_visual_object_matched',
]);

const scopes = [
  { name: 'all_triads', rows: triads, minToken: 5, minFamily: 3 },
  {
    name: 'strong_local_contrasts',
    rows: triads.filter((row) => strongGrades.has(row.grade)),
    minToken: 2,
    minFamily: 2,
  },
  {
    name: 'independent_low_copy',
    rows: triads.filter((row) => ['1', '2', '3', '4'].includes(String(row.independence_rank))),
    minToken: 2,
    minFamily: 2,
  },
  {
    name: 'two_lane_core',
    rows: triads.filter((row) => row.packet_priority === 'core'),
    minToken: 2,
    minFamily: 2,
  },
  {
    name: 'repeated_branch_optional',
    rows: triads.filter((row) => row.packet_lane === 'repeated_branch_check'),
    minToken: 1,
    minFamily: 1,
  },
];

const rowHeader = [
  'scope',
  'target_cisi',
  'triad_rank',
  'independence_rank',
  'grade',
  'copy_pressure',
  'packet_lane',
  'packet_priority',
  'long_tokens_034',
  'long_tokens_033',
  'long_tokens_032',
  'long_family_034',
  'long_family_033',
  'long_family_032',
];

const scopeRows = [];
for (const scope of scopes) {
  for (const row of scope.rows) {
    scopeRows.push({
      scope: scope.name,
      target_cisi: row.target_cisi,
      triad_rank: row.triad_rank,
      independence_rank: row.independence_rank,
      grade: row.grade,
      copy_pressure: row.copy_pressure,
      packet_lane: row.packet_lane,
      packet_priority: row.packet_priority,
      long_tokens_034: [...row.long_tokens['034']].join(';'),
      long_tokens_033: [...row.long_tokens['033']].join(';'),
      long_tokens_032: [...row.long_tokens['032']].join(';'),
      long_family_034: [...row.long_family['034']].join(';'),
      long_family_033: [...row.long_family['033']].join(';'),
      long_family_032: [...row.long_family['032']].join(';'),
    });
  }
}

const tokenRows = scopes.flatMap((scope) => runFeatureTests(scope.name, scope.rows, 'long_tokens', scope.minToken));
const familyRows = scopes.flatMap((scope) => runFeatureTests(scope.name, scope.rows, 'long_family', scope.minFamily));

const tokenHeader = [
  'scope',
  'feature',
  'candidate',
  'triads',
  'any_triads',
  'hit_034',
  'hit_033',
  'hit_032',
  'observed_delta',
  'p_ge',
  'q_bh',
  'null_mean',
  'null_p95',
  'status',
];

const familyHeader = tokenHeader;

fs.writeFileSync(tokenCsvPath, toCsv([tokenHeader, ...tokenRows.map((row) => tokenHeader.map((key) => row[key]))]));
fs.writeFileSync(familyCsvPath, toCsv([familyHeader, ...familyRows.map((row) => familyHeader.map((key) => row[key]))]));
fs.writeFileSync(rowCsvPath, toCsv([rowHeader, ...scopeRows.map((row) => rowHeader.map((key) => row[key]))]));

const topTokenAll = tokenRows.find((row) => row.scope === 'all_triads') ?? null;
const topFamilyAll = familyRows.find((row) => row.scope === 'all_triads') ?? null;
const correctedTokenRows = tokenRows.filter((row) => Number(row.q_bh) <= 0.05);
const correctedFamilyRows = familyRows.filter((row) => Number(row.q_bh) <= 0.05);

const summary = {
  date: '2026-05-25',
  experiment: 'Lipi FRAME700 034 long context substitution',
  inputs: [path.relative(base, triadPath), path.relative(base, stabilityPath), path.relative(base, packetPath)],
  iterations,
  scopes: Object.fromEntries(scopes.map((scope) => [scope.name, scope.rows.length])),
  token_tests: tokenRows.length,
  family_tests: familyRows.length,
  corrected_token_tests: correctedTokenRows.length,
  corrected_family_tests: correctedFamilyRows.length,
  top_all_token: topTokenAll,
  top_all_family: topFamilyAll,
  corrected_token_candidates: correctedTokenRows.slice(0, 20).map((row) => ({
    scope: row.scope,
    candidate: row.candidate,
    hit_034: row.hit_034,
    hit_033: row.hit_033,
    hit_032: row.hit_032,
    observed_delta: row.observed_delta,
    q_bh: row.q_bh,
  })),
  corrected_family_candidates: correctedFamilyRows.slice(0, 20).map((row) => ({
    scope: row.scope,
    candidate: row.candidate,
    hit_034: row.hit_034,
    hit_033: row.hit_033,
    hit_032: row.hit_032,
    observed_delta: row.observed_delta,
    q_bh: row.q_bh,
  })),
  accepted_decipherment_claims: 0,
  status: 'source_blind_context_substitution_only',
  outputs: [path.relative(base, tokenCsvPath), path.relative(base, familyCsvPath), path.relative(base, rowCsvPath), path.relative(base, summaryJsonPath)],
};

fs.writeFileSync(summaryJsonPath, `${JSON.stringify(summary, null, 2)}\n`);

console.log(
  JSON.stringify(
    {
      tokenCsvPath,
      familyCsvPath,
      rowCsvPath,
      summaryJsonPath,
      token_tests: tokenRows.length,
      family_tests: familyRows.length,
      corrected_token_tests: correctedTokenRows.length,
      corrected_family_tests: correctedFamilyRows.length,
    },
    null,
    2,
  ),
);
