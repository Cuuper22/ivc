import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(base, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const crosswalkPairsPath = path.join(reportsDir, 'crosswalk_alignment_pairs.csv');
const crosswalkCandidatesPath = path.join(reportsDir, 'crosswalk_lipi_to_mayig_candidates.csv');
const overlapPath = path.join(reportsDir, 'overlap_probe.csv');

const rowsOut = path.join(reportsDir, 'lipi_154_156_comparanda_rows.csv');
const rankedControlsOut = path.join(reportsDir, 'lipi_154_156_ranked_controls.csv');
const crosswalkOut = path.join(reportsDir, 'lipi_154_156_crosswalk_pressure.csv');
const summaryOut = path.join(reportsDir, 'lipi_154_156_comparanda_summary.json');

function parseCsv(text) {
  const rows = [];
  let row = [];
  let value = '';
  let inQuotes = false;

  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (inQuotes) {
      if (ch === '"' && next === '"') {
        value += '"';
        i += 1;
      } else if (ch === '"') {
        inQuotes = false;
      } else {
        value += ch;
      }
    } else if (ch === '"') {
      inQuotes = true;
    } else if (ch === ',') {
      row.push(value);
      value = '';
    } else if (ch === '\n') {
      row.push(value);
      if (row.length > 1 || row[0] !== '') rows.push(row);
      row = [];
      value = '';
    } else if (ch !== '\r') {
      value += ch;
    }
  }
  if (value.length > 0 || row.length > 0) {
    row.push(value);
    rows.push(row);
  }
  return rows;
}

function csvObjects(text) {
  const [header, ...body] = parseCsv(text);
  return body.map((row) =>
    Object.fromEntries(header.map((key, index) => [key, row[index] ?? ''])),
  );
}

function toCsv(rows) {
  if (rows.length === 0) return '';
  const header = Object.keys(rows[0]);
  const body = rows.map((row) =>
    header
      .map((key) => `"${String(row[key] ?? '').replaceAll('"', '""')}"`)
      .join(','),
  );
  return `${[header.map((key) => `"${key}"`).join(','), ...body].join('\n')}\n`;
}

function tokens(text) {
  return text.match(/\d+/gu) ?? [];
}

function textHasPair(row, pair) {
  const rowTokens = tokens(row.text);
  for (let i = 0; i < rowTokens.length - 1; i += 1) {
    if (`${rowTokens[i]}_${rowTokens[i + 1]}` === pair) return true;
  }
  return false;
}

function cisiNumber(cisi) {
  const match = /^H-(\d+)$/u.exec(cisi);
  return match ? Number(match[1]) : null;
}

function isHSeries(row) {
  const n = cisiNumber(row.cisi);
  return n !== null && n >= 2218 && n <= 2239;
}

function objectGroupKey(row) {
  return row.cisi && row.cisi !== '-' ? `cisi:${row.cisi}` : `row:${row.id}`;
}

function sameCisiTexts(groupRows) {
  return [...new Set(groupRows.map((row) => row.text).filter(Boolean))].sort().join(';');
}

function parseMeasure(value) {
  if (!value || value === '-') return null;
  const nums = value.match(/\d+(?:\.\d+)?/gu)?.map(Number) ?? [];
  if (nums.length === 0) return null;
  return nums.reduce((sum, n) => sum + n, 0) / nums.length;
}

function delta(a, b) {
  return a === null || b === null ? null : Math.abs(a - b);
}

function fmt(value) {
  if (value === null || value === undefined || value === '') return '';
  return Number(value).toFixed(6).replace(/\.?0+$/u, '');
}

function hPrefix(cisi) {
  const match = /^([A-Z]+)-/u.exec(cisi);
  return match?.[1] ?? (cisi === '-' ? '-' : 'other');
}

function pairScope(row) {
  if (isHSeries(row)) return row.text === '+154-003+' ? 'h_series_singleton_variant' : 'h_series_majority_156_003';
  if (row.text === '+154-003+') return 'external_strict_154_003';
  if (row.text === '+156-003+') return 'external_strict_156_003';
  if (textHasPair(row, '154_003')) return 'external_longer_154_003';
  if (textHasPair(row, '156_003')) return 'external_longer_156_003';
  return 'not_in_packet';
}

function suffixAfter003(row) {
  const rowTokens = tokens(row.text);
  const index = rowTokens.findIndex((token, i) => i > 0 && rowTokens[i - 1] === '154' && token === '003');
  const altIndex = rowTokens.findIndex((token, i) => i > 0 && rowTokens[i - 1] === '156' && token === '003');
  const hit = index >= 0 ? index : altIndex;
  return hit >= 0 ? rowTokens.slice(hit + 1) : [];
}

function overlapCount(a, b) {
  const bSet = new Set(b);
  return a.filter((value) => bSet.has(value)).length;
}

function comparatorScore(target, control) {
  const targetTokens = tokens(target.text);
  const controlTokens = tokens(control.text);
  const hDelta = delta(parseMeasure(target.horizontal_mm), parseMeasure(control.horizontal_mm));
  const vDelta = delta(parseMeasure(target.vertical_mm), parseMeasure(control.vertical_mm));
  const tDelta = delta(parseMeasure(target.thickness_mm), parseMeasure(control.thickness_mm));
  const suffixOverlap = overlapCount(suffixAfter003(target), suffixAfter003(control));
  const companionOverlap = overlapCount(
    target.same_cisi_texts.split(';').filter((text) => text && text !== target.text),
    control.same_cisi_texts.split(';').filter((text) => text && text !== control.text),
  );

  let score = 0;
  const reasons = [];
  const add = (points, reason) => {
    score += points;
    reasons.push(reason);
  };

  if (target.site === control.site) add(12, 'same_site');
  if (target.type === control.type) add(12, 'same_type');
  if (target.shape === control.shape) add(8, 'same_shape');
  if (target.material.toLowerCase() === control.material.toLowerCase()) add(6, 'same_material');
  if (target.class === control.class) add(4, 'same_class');
  if (target.direction === control.direction) add(3, 'same_direction');
  if (target.sign_count === control.sign_count) add(6, 'same_sign_count');
  if (target.cisi_prefix === control.cisi_prefix) add(3, 'same_id_prefix');
  if (target.is_h2218_h2239 === '1' && control.is_h2218_h2239 === '1') add(30, 'same_h_series_scope');
  if (target.exact_text_class === '+154-003+' && control.exact_text_class === '+156-003+') add(8, 'strict_exact_pair');
  if (targetTokens.length === controlTokens.length) add(3, 'same_token_length');
  if (suffixOverlap > 0) add(6 * suffixOverlap, `suffix_overlap_${suffixOverlap}`);
  if (companionOverlap > 0) add(12 * companionOverlap, `companion_text_overlap_${companionOverlap}`);

  const dimensionPenalty =
    (hDelta ?? 8) * 0.7 +
    (vDelta ?? 8) * 0.7 +
    (tDelta ?? 6) * 0.3;
  score -= dimensionPenalty;

  return {
    score,
    reasons,
    hDelta,
    vDelta,
    tDelta,
    suffixOverlap,
    companionOverlap,
  };
}

function topControlMap(rows) {
  return Object.fromEntries(
    targets154.map((target) => {
      const first = rows.find((row) => row.target_source_row_id === target.source_row_id);
      return [
        `${target.cisi}:${target.text}`,
        first
          ? {
              control: `${first.control_cisi}:${first.control_text}`,
              score: Number(first.score),
              reasons: first.score_reasons,
            }
          : null,
      ];
    }),
  );
}

function bestControlSummary(target, candidateControls) {
  const best = candidateControls
    .map((control) => ({ control, rank: comparatorScore(target, control) }))
    .sort((a, b) => b.rank.score - a.rank.score)[0];
  return best
    ? {
        control: `${best.control.cisi}:${best.control.text}`,
        score: Number(fmt(best.rank.score)),
        reasons: best.rank.reasons.join(';'),
      }
    : null;
}

function countBy(rows, keyFn) {
  const counts = {};
  for (const row of rows) {
    const key = keyFn(row);
    counts[key] = (counts[key] ?? 0) + 1;
  }
  return Object.fromEntries(
    Object.entries(counts).sort((a, b) => a[0].localeCompare(b[0], undefined, { numeric: true })),
  );
}

const metadata = csvObjects(fs.readFileSync(metadataPath, 'utf8'));
const byObject = new Map();
for (const row of metadata) {
  const key = objectGroupKey(row);
  if (!byObject.has(key)) byObject.set(key, []);
  byObject.get(key).push(row);
}

const packetRows = metadata
  .filter((row) => textHasPair(row, '154_003') || textHasPair(row, '156_003'))
  .map((row) => {
    const groupRows = byObject.get(objectGroupKey(row)) ?? [row];
    const rowTokens = tokens(row.text);
    return {
      checked_date: '2026-05-25',
      source_row_id: row.id,
      cisi: row.cisi,
      cisi_prefix: hPrefix(row.cisi),
      is_h2218_h2239: isHSeries(row) ? '1' : '0',
      pair: textHasPair(row, '154_003') ? '154_003' : '156_003',
      pair_scope: pairScope(row),
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      preservation: row.preservation,
      condition: row.condition,
      complete: row.complete,
      direction: row['dir.'],
      class: row.class,
      sign_count: row.signs,
      horizontal_mm: row['horizontal(mm)'],
      vertical_mm: row['vertical(mm)'],
      thickness_mm: row['thickness(mm)'],
      text: row.text,
      tokens: rowTokens.join(' '),
      suffix_after_003: suffixAfter003(row).join(' '),
      same_cisi_texts: sameCisiTexts(groupRows),
      source_priority:
        row.cisi === 'H-2237'
          ? 'P0_h_series_minimal_pair'
          : row.cisi === 'H-366'
            ? 'P1_external_strict_exact_tab_i'
            : row.cisi === 'H-1682' || row.cisi === 'M-102'
              ? 'P2_external_longer_prefix_frame'
              : isHSeries(row)
                ? 'P1_h_series_156_control_pool'
                : 'P3_external_156_control_pool',
      accepted_decipherment_claim: '0',
    };
  })
  .sort(
    (a, b) =>
      a.pair.localeCompare(b.pair) ||
      a.pair_scope.localeCompare(b.pair_scope) ||
      a.cisi.localeCompare(b.cisi, undefined, { numeric: true }) ||
      a.source_row_id.localeCompare(b.source_row_id, undefined, { numeric: true }),
  );

const targets154 = packetRows.filter((row) => row.pair === '154_003');
const controls156 = packetRows.filter((row) => row.pair === '156_003');
const rankedControls = [];
for (const target of targets154) {
  const ranked = controls156
    .map((control) => ({ control, rank: comparatorScore(target, control) }))
    .sort((a, b) => b.rank.score - a.rank.score)
    .slice(0, 10);

  for (let i = 0; i < ranked.length; i += 1) {
    const { control, rank } = ranked[i];
    rankedControls.push({
      checked_date: '2026-05-25',
      target_cisi: target.cisi,
      target_source_row_id: target.source_row_id,
      target_text: target.text,
      target_pair_scope: target.pair_scope,
      control_rank: String(i + 1),
      control_cisi: control.cisi,
      control_source_row_id: control.source_row_id,
      control_text: control.text,
      control_pair_scope: control.pair_scope,
      score: fmt(rank.score),
      score_reasons: rank.reasons.join(';'),
      horizontal_delta_mm: fmt(rank.hDelta),
      vertical_delta_mm: fmt(rank.vDelta),
      thickness_delta_mm: fmt(rank.tDelta),
      suffix_overlap_after_003: String(rank.suffixOverlap),
      companion_text_overlap: String(rank.companionOverlap),
      target_metadata: `${target.site}|${target.type}|${target.shape}|${target.material}|${target.class}|${target.sign_count}`,
      control_metadata: `${control.site}|${control.type}|${control.shape}|${control.material}|${control.class}|${control.sign_count}`,
      source_use:
        i === 0
          ? 'best_current_planning_control_only_requires_source_images'
          : 'secondary_planning_control_only',
      accepted_decipherment_claim: '0',
    });
  }
}

const alignments = csvObjects(fs.readFileSync(crosswalkPairsPath, 'utf8')).filter((row) =>
  ['154', '156'].includes(row.lipi_sign),
);
const candidates = csvObjects(fs.readFileSync(crosswalkCandidatesPath, 'utf8')).filter((row) =>
  ['154', '156'].includes(row.source_a_sign),
);
const overlaps = csvObjects(fs.readFileSync(overlapPath, 'utf8'));
const overlapByCisi = new Map(overlaps.map((row) => [row.cisi, row]));

const crosswalkRows = [
  ...candidates.map((row) => ({
    checked_date: '2026-05-25',
    row_type: 'candidate_summary',
    cisi: '',
    lipi_id: '',
    lipi_sign: row.source_a_sign,
    mayig_sign: row.top_source_b_sign,
    lipi_context: '',
    mayig_context: '',
    position_class: row.position_counts,
    total_aligned_positions: row.total_aligned_positions,
    top_share: row.top_share,
    evidence_status: row.mapping_state,
    review_status: row.review_status,
    artifact_context: row.example_artifacts,
    pressure_interpretation:
      row.top_source_b_sign === 'P004'
        ? 'crosswalk_collapses_or_aligns_this_lipi_sign_with_mayig_P004_in_the_current_overlap_layer'
        : 'crosswalk_points_elsewhere_or_is_sparse',
    accepted_decipherment_claim: '0',
  })),
  ...alignments.map((row) => {
    const overlap = overlapByCisi.get(row.cisi) ?? {};
    return {
      checked_date: '2026-05-25',
      row_type: 'position_alignment',
      cisi: row.cisi,
      lipi_id: row.lipi_id,
      lipi_sign: row.lipi_sign,
      mayig_sign: row.mayig_sign,
      lipi_context: `${row.lipi_left} <${row.lipi_sign}> ${row.lipi_right}`,
      mayig_context: `${row.mayig_left} <${row.mayig_sign}> ${row.mayig_right}`,
      position_class: row.position_class,
      total_aligned_positions: '',
      top_share: '',
      evidence_status: row.evidence_status,
      review_status: overlap.comparison_status ?? '',
      artifact_context: `${overlap.lipi_text ?? ''} || ${overlap.mayig_graphemes ?? ''}`,
      pressure_interpretation:
        row.mayig_sign === 'P004'
          ? '154_or_156_aligns_to_the_same_mayig_sign_P004_here; source_allograph_check_required'
          : '154_or_156_alignment_does_not_collapse_to_P004_here',
      accepted_decipherment_claim: '0',
    };
  }),
].sort(
  (a, b) =>
    a.row_type.localeCompare(b.row_type) ||
    a.lipi_sign.localeCompare(b.lipi_sign, undefined, { numeric: true }) ||
    a.cisi.localeCompare(b.cisi, undefined, { numeric: true }),
);

const topControlByTarget = topControlMap(rankedControls);
const topExternalControlByTarget = Object.fromEntries(
  targets154.map((target) => [
    `${target.cisi}:${target.text}`,
    bestControlSummary(
      target,
      controls156.filter((control) => control.is_h2218_h2239 === '0'),
    ),
  ]),
);

const summary = {
  checked_date: '2026-05-25',
  artifact: 'lipi_154_156_comparanda_packet',
  inputs: [
    path.relative(base, metadataPath).replaceAll('\\', '/'),
    path.relative(base, crosswalkPairsPath).replaceAll('\\', '/'),
    path.relative(base, crosswalkCandidatesPath).replaceAll('\\', '/'),
    path.relative(base, overlapPath).replaceAll('\\', '/'),
  ],
  packet_rows: packetRows.length,
  pair_counts: countBy(packetRows, (row) => row.pair),
  pair_scope_counts: countBy(packetRows, (row) => row.pair_scope),
  external_154_003_objects: targets154
    .filter((row) => row.is_h2218_h2239 === '0')
    .map((row) => row.cisi)
    .join(';'),
  strict_external_154_003_objects: targets154
    .filter((row) => row.is_h2218_h2239 === '0' && row.text === '+154-003+')
    .map((row) => row.cisi)
    .join(';'),
  ranked_control_rows: rankedControls.length,
  top_control_by_154_003_target: topControlByTarget,
  top_non_h_series_control_by_154_003_target: topExternalControlByTarget,
  crosswalk_candidate_rows: candidates.length,
  crosswalk_alignment_rows: alignments.length,
  crosswalk_154_to_P004_alignment_rows: alignments.filter(
    (row) => row.lipi_sign === '154' && row.mayig_sign === 'P004',
  ).length,
  crosswalk_156_to_P004_alignment_rows: alignments.filter(
    (row) => row.lipi_sign === '156' && row.mayig_sign === 'P004',
  ).length,
  crosswalk_pressure:
    'The overlap layer aligns both lipi 154 and lipi 156 with Mayig/Parpola P004 in at least one row. This is allograph/crosswalk pressure, not proof of sameness; source images must decide whether H-2237 is a real visual contrast or a catalog/sign-list split.',
  outputs: [
    path.relative(base, rowsOut).replaceAll('\\', '/'),
    path.relative(base, rankedControlsOut).replaceAll('\\', '/'),
    path.relative(base, crosswalkOut).replaceAll('\\', '/'),
    path.relative(base, summaryOut).replaceAll('\\', '/'),
  ],
  accepted_decipherment_claims: 0,
};

fs.writeFileSync(rowsOut, toCsv(packetRows), 'utf8');
fs.writeFileSync(rankedControlsOut, toCsv(rankedControls), 'utf8');
fs.writeFileSync(crosswalkOut, toCsv(crosswalkRows), 'utf8');
fs.writeFileSync(summaryOut, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
