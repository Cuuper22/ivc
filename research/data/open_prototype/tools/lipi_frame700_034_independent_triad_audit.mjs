import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const triadPath = path.join(reportsDir, 'lipi_frame700_034_source_triad_packet.csv');
const acquisitionPath = path.join(reportsDir, 'lipi_frame700_034_source_acquisition_manifest.csv');
const outCsv = path.join(reportsDir, 'lipi_frame700_034_independent_triad_audit.csv');
const outJson = path.join(reportsDir, 'lipi_frame700_034_independent_triad_audit_summary.json');
const requestCsv = path.join(reportsDir, 'lipi_frame700_034_archive_request_batch.csv');

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;

  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];
    const next = text[i + 1];

    if (char === '"' && inQuotes && next === '"') {
      field += '"';
      i += 1;
    } else if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === ',' && !inQuotes) {
      row.push(field);
      field = '';
    } else if ((char === '\n' || char === '\r') && !inQuotes) {
      if (char === '\r' && next === '\n') i += 1;
      row.push(field);
      if (row.some((value) => value !== '')) rows.push(row);
      row = [];
      field = '';
    } else {
      field += char;
    }
  }

  if (field !== '' || row.length > 0) {
    row.push(field);
    if (row.some((value) => value !== '')) rows.push(row);
  }

  const [header, ...records] = rows;
  return records.map((record) =>
    Object.fromEntries(header.map((name, index) => [name, record[index] ?? ''])),
  );
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

function countBy(rows, keyFn) {
  const counts = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return Object.fromEntries(
    [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])),
  );
}

function numberOrZero(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : 0;
}

function splitList(value) {
  return String(value ?? '')
    .split(';')
    .map((part) => part.trim())
    .filter(Boolean);
}

function sourceHooks(value) {
  return splitList(value).filter((hook) => hook.toLowerCase() !== 'no local source hook');
}

function hookGrade(value) {
  const hooks = sourceHooks(value);
  if (hooks.length === 0) return 'missing_source_hook';
  const hasFigure = hooks.some((hook) => /^Figure\b/i.test(hook));
  const hasNonFigure = hooks.some((hook) => !/^Figure\b/i.test(hook));
  if (hasFigure && hasNonFigure) return 'excavation_plus_figure_hook';
  if (hasFigure) return 'figure_hook_only';
  return 'catalog_or_excavation_hook';
}

function sourcePrefix(value) {
  const hooks = sourceHooks(value);
  const primary = hooks.find((hook) => !/^Figure\b/i.test(hook)) ?? hooks[0] ?? '';
  if (!primary) return 'no_source_prefix';
  if (/^H\d{4}\b/i.test(primary)) return primary.match(/^H\d{4}/i)[0].toUpperCase();
  if (/^H\d{2}\b/i.test(primary)) return primary.match(/^H\d{2}/i)[0].toUpperCase();
  if (/^PII\b/i.test(primary)) return 'PII';
  if (/^J/i.test(primary)) return 'J';
  if (/^G/i.test(primary)) return 'G';
  if (/^\d/.test(primary)) return 'numeric_catalog';
  if (/^[0-9a-f]{6,}$/i.test(primary)) return 'hash_catalog';
  return primary.replace(/[^A-Za-z0-9]+.*/, '') || 'other_source_prefix';
}

function familyCountFromAcquisition(row) {
  return Math.max(1, numberOrZero(row?.sequence_family_count_max_no_h ?? 1));
}

function sameObjectFormat(row) {
  const target = row.target_material_shape;
  const control033 = row.control_033_material_shape;
  const control032 = row.control_032_material_shape;
  if (!target || !control033 || !control032) return 'object_format_metadata_incomplete';
  if (target === control033 && target === control032) return 'target_and_both_controls_match';
  if (target === control033 || target === control032) return 'target_matches_one_control';
  return 'target_differs_from_both_controls';
}

function directionRisk(row) {
  if (row.target_short_text === '+034-700+') return 'target_700_order_reversed';
  if (row.target_side_relation !== row.control_033_side_relation && row.target_side_relation !== row.control_032_side_relation) {
    return 'target_side_relation_differs_from_both_controls';
  }
  return 'no_extra_direction_flag';
}

function sourceGap(row) {
  const grades = [
    hookGrade(row.target_source_hooks),
    hookGrade(row.control_033_source_hooks),
    hookGrade(row.control_032_source_hooks),
  ];
  if (grades.every((grade) => grade !== 'missing_source_hook')) return 'all_three_have_source_hooks';
  if (grades[0] === 'missing_source_hook') return 'target_source_hook_missing';
  return 'control_source_hook_missing';
}

function pressureLabel(parts) {
  const active = parts.filter(Boolean);
  return active.length ? active.join(';') : 'no_extra_pressure_flag';
}

function evidenceTier(row, facts) {
  if (facts.source_gap_status !== 'all_three_have_source_hooks') return 'D_source_hook_gap';
  if (facts.target_long_set_count > 2 || facts.acquisition_family_count > 2) {
    return 'C_repeated_target_family_pressure';
  }
  if (facts.max_control_reuse > 3 || facts.direction_risk !== 'no_extra_direction_flag') {
    return 'B_source_ready_with_direction_or_reuse_pressure';
  }
  if (
    row.contrast_readiness === 'strong_two_sibling_metadata_controls' &&
    facts.object_format_match_status === 'target_and_both_controls_match' &&
    numberOrZero(row.triad_score) >= 60
  ) {
    return 'A_independent_source_ready';
  }
  return 'B_source_ready_needs_metadata_review';
}

function independenceScore(row, facts) {
  let score = numberOrZero(row.triad_score);
  if (facts.source_gap_status === 'all_three_have_source_hooks') score += 20;
  if (facts.target_hook_grade === 'excavation_plus_figure_hook') score += 5;
  if (facts.target_long_set_count === 1) score += 25;
  else if (facts.target_long_set_count === 2) score += 10;
  else score -= 12;
  if (facts.acquisition_family_count <= 1) score += 12;
  else if (facts.acquisition_family_count <= 2) score += 4;
  else score -= 8;
  if (facts.target_source_prefix_count === 1) score += 12;
  else if (facts.target_source_prefix_count === 2) score += 4;
  else score -= 2;
  if (facts.max_control_reuse <= 1) score += 12;
  else if (facts.max_control_reuse <= 3) score += 4;
  else score -= 6;
  if (facts.object_format_match_status === 'target_and_both_controls_match') score += 10;
  else if (facts.object_format_match_status === 'target_matches_one_control') score += 3;
  else score -= 5;
  if (facts.direction_risk === 'target_700_order_reversed') score -= 8;
  if (row.contrast_readiness === 'strong_two_sibling_metadata_controls') score += 8;
  return score;
}

function priorityReason(row, facts) {
  const reasons = [];
  reasons.push(`tier=${facts.evidence_tier}`);
  reasons.push(`source_hooks=${facts.source_gap_status}`);
  reasons.push(`target_long_set_count=${facts.target_long_set_count}`);
  reasons.push(`source_prefix=${facts.target_source_prefix}/${facts.target_source_prefix_count}`);
  reasons.push(`control_reuse_max=${facts.max_control_reuse}`);
  reasons.push(`object_format=${facts.object_format_match_status}`);
  if (facts.direction_risk !== 'no_extra_direction_flag') reasons.push(`direction=${facts.direction_risk}`);
  return reasons.join('; ');
}

function nextAction(row, facts) {
  if (facts.source_gap_status !== 'all_three_have_source_hooks') {
    return 'fill_missing_source_hook_before_archive_request';
  }
  if (facts.evidence_tier === 'A_independent_source_ready') return 'request_source_images_now_first_independent_batch';
  if (facts.evidence_tier.startsWith('B_')) return 'request_source_images_after_first_independent_batch';
  if (facts.evidence_tier.startsWith('C_')) return 'request_one_representative_then_seek_independent_target';
  return 'hold_for_source_hook_cleanup';
}

const triadRows = parseCsv(fs.readFileSync(triadPath, 'utf8'));
const acquisitionRows = parseCsv(fs.readFileSync(acquisitionPath, 'utf8'));
const acquisitionByCisi = new Map(acquisitionRows.map((row) => [row.cisi, row]));

const targetLongCounts = countBy(triadRows, (row) => row.target_long_token_set || 'NO_LONG_SET');
const targetPrefixCounts = countBy(triadRows, (row) => sourcePrefix(row.target_source_hooks));
const control033Reuse = countBy(triadRows, (row) => row.control_033_cisi || 'NO_033_CONTROL');
const control032Reuse = countBy(triadRows, (row) => row.control_032_cisi || 'NO_032_CONTROL');

const audited = triadRows.map((row) => {
  const acquisition = acquisitionByCisi.get(row.target_cisi);
  const facts = {
    target_hook_grade: hookGrade(row.target_source_hooks),
    control_033_hook_grade: hookGrade(row.control_033_source_hooks),
    control_032_hook_grade: hookGrade(row.control_032_source_hooks),
    target_source_prefix: sourcePrefix(row.target_source_hooks),
    target_long_set_count: targetLongCounts[row.target_long_token_set || 'NO_LONG_SET'] ?? 0,
    target_source_prefix_count: targetPrefixCounts[sourcePrefix(row.target_source_hooks)] ?? 0,
    acquisition_family_count: familyCountFromAcquisition(acquisition),
    control_033_reuse_count: control033Reuse[row.control_033_cisi || 'NO_033_CONTROL'] ?? 0,
    control_032_reuse_count: control032Reuse[row.control_032_cisi || 'NO_032_CONTROL'] ?? 0,
    object_format_match_status: sameObjectFormat(row),
    direction_risk: directionRisk(row),
    source_gap_status: sourceGap(row),
  };
  facts.max_control_reuse = Math.max(facts.control_033_reuse_count, facts.control_032_reuse_count);
  facts.copy_family_pressure = pressureLabel([
    facts.target_long_set_count > 2 ? `repeated_target_long_set_${facts.target_long_set_count}` : '',
    facts.acquisition_family_count > 2 ? `acquisition_sequence_family_${facts.acquisition_family_count}` : '',
  ]);
  facts.source_prefix_pressure = pressureLabel([
    facts.target_source_prefix_count > 2 ? `source_prefix_seen_${facts.target_source_prefix_count}` : '',
  ]);
  facts.control_reuse_pressure = pressureLabel([
    facts.control_033_reuse_count > 3 ? `033_control_reused_${facts.control_033_reuse_count}` : '',
    facts.control_032_reuse_count > 3 ? `032_control_reused_${facts.control_032_reuse_count}` : '',
  ]);
  facts.evidence_tier = evidenceTier(row, facts);
  facts.independence_score = independenceScore(row, facts);

  return {
    ...row,
    ...facts,
    priority_reason: priorityReason(row, facts),
    next_source_action: nextAction(row, facts),
    source_check_status: 'independence_audit_source_order_only_no_reading_claims',
  };
});

const tierRank = {
  A_independent_source_ready: 1,
  B_source_ready_needs_metadata_review: 2,
  B_source_ready_with_direction_or_reuse_pressure: 3,
  C_repeated_target_family_pressure: 4,
  D_source_hook_gap: 5,
};

audited.sort(
  (a, b) =>
    (tierRank[a.evidence_tier] ?? 99) - (tierRank[b.evidence_tier] ?? 99) ||
    b.independence_score - a.independence_score ||
    Number(a.triad_rank) - Number(b.triad_rank),
);

const auditHeader = [
  'independence_rank',
  'original_triad_rank',
  'target_cisi',
  'target_row_id',
  'target_short_text',
  'target_bucket',
  'evidence_tier',
  'independence_score',
  'triad_score',
  'contrast_readiness',
  'target_long_token_set',
  'target_long_set_count',
  'acquisition_family_count',
  'target_source_prefix',
  'target_source_prefix_count',
  'source_gap_status',
  'target_hook_grade',
  'control_033_cisi',
  'control_033_reuse_count',
  'control_033_hook_grade',
  'control_032_cisi',
  'control_032_reuse_count',
  'control_032_hook_grade',
  'object_format_match_status',
  'direction_risk',
  'copy_family_pressure',
  'source_prefix_pressure',
  'control_reuse_pressure',
  'priority_reason',
  'next_source_action',
  'source_check_status',
];

fs.writeFileSync(
  outCsv,
  toCsv([
    auditHeader,
    ...audited.map((row, index) =>
      auditHeader.map((key) => {
        if (key === 'independence_rank') return index + 1;
        if (key === 'original_triad_rank') return row.triad_rank;
        return row[key];
      }),
    ),
  ]),
);

const requestFields =
  'all source images or plates for every side; source plate/page/image identifier; side labels and side order; inscription versus impression direction; sign segmentation; object material, shape, cross-section, dimensions, condition, and find context';

const requestTriads = audited
  .filter((row) => row.source_gap_status === 'all_three_have_source_hooks')
  .slice(0, 10);

const requestRows = [];
for (const triad of requestTriads) {
  const roles = [
    {
      role: 'target_034',
      cisi: triad.target_cisi,
      row_id: triad.target_row_id,
      short_text: triad.target_short_text,
      source_hooks: triad.target_source_hooks,
      hook_grade: triad.target_hook_grade,
      local_rows: triad.target_local_rows,
      material_shape: triad.target_material_shape,
      period_phase_depth: triad.target_period_phase_depth,
      dimensions_mm: triad.target_dimensions_mm,
      source_use: 'source-check target row order, side placement, and visual distinction from controls',
    },
    {
      role: 'control_033',
      cisi: triad.control_033_cisi,
      row_id: triad.control_033_row_id,
      short_text: triad.control_033_short_text,
      source_hooks: triad.control_033_source_hooks,
      hook_grade: triad.control_033_hook_grade,
      local_rows: triad.control_033_local_rows,
      material_shape: triad.control_033_material_shape,
      period_phase_depth: triad.control_033_period_phase_depth,
      dimensions_mm: triad.control_033_dimensions_mm,
      source_use: 'source-check closest 033 sibling under matched metadata',
    },
    {
      role: 'control_032',
      cisi: triad.control_032_cisi,
      row_id: triad.control_032_row_id,
      short_text: triad.control_032_short_text,
      source_hooks: triad.control_032_source_hooks,
      hook_grade: triad.control_032_hook_grade,
      local_rows: triad.control_032_local_rows,
      material_shape: triad.control_032_material_shape,
      period_phase_depth: triad.control_032_period_phase_depth,
      dimensions_mm: triad.control_032_dimensions_mm,
      source_use: 'source-check closest 032 sibling under matched metadata',
    },
  ];

  for (const role of roles) {
    requestRows.push({
      request_rank: requestRows.length + 1,
      independence_rank: audited.indexOf(triad) + 1,
      original_triad_rank: triad.triad_rank,
      triad_evidence_tier: triad.evidence_tier,
      triad_target: `${triad.target_cisi}/${triad.target_short_text}/${triad.target_long_token_set}`,
      role: role.role,
      cisi: role.cisi,
      row_id: role.row_id,
      short_text: role.short_text,
      source_hooks: role.source_hooks,
      hook_grade: role.hook_grade,
      local_rows: role.local_rows,
      material_shape: role.material_shape,
      period_phase_depth: role.period_phase_depth,
      dimensions_mm: role.dimensions_mm,
      requested_source_fields: requestFields,
      source_use: role.source_use,
      source_check_status: 'archive_request_source_order_only_no_reading_claims',
    });
  }
}

const requestHeader = [
  'request_rank',
  'independence_rank',
  'original_triad_rank',
  'triad_evidence_tier',
  'triad_target',
  'role',
  'cisi',
  'row_id',
  'short_text',
  'source_hooks',
  'hook_grade',
  'local_rows',
  'material_shape',
  'period_phase_depth',
  'dimensions_mm',
  'requested_source_fields',
  'source_use',
  'source_check_status',
];

fs.writeFileSync(requestCsv, toCsv([requestHeader, ...requestRows.map((row) => requestHeader.map((key) => row[key]))]));

const summary = {
  generated_at: '2026-05-25',
  input_triads: triadRows.length,
  audited_triads: audited.length,
  archive_request_rows: requestRows.length,
  archive_request_triads: requestTriads.length,
  counts_by_evidence_tier: countBy(audited, (row) => row.evidence_tier),
  counts_by_source_gap_status: countBy(audited, (row) => row.source_gap_status),
  counts_by_copy_family_pressure: countBy(audited, (row) => row.copy_family_pressure),
  counts_by_source_prefix_pressure: countBy(audited, (row) => row.source_prefix_pressure),
  top_independent_triads: audited.slice(0, 15).map((row, index) => ({
    independence_rank: index + 1,
    original_triad_rank: row.triad_rank,
    target: `${row.target_cisi}/${row.target_short_text}/${row.target_long_token_set}`,
    controls: `${row.control_033_cisi}/${row.control_033_short_text}; ${row.control_032_cisi}/${row.control_032_short_text}`,
    evidence_tier: row.evidence_tier,
    independence_score: row.independence_score,
    source_gap_status: row.source_gap_status,
    target_source_prefix: row.target_source_prefix,
    target_long_set_count: row.target_long_set_count,
    acquisition_family_count: row.acquisition_family_count,
    max_control_reuse: row.max_control_reuse,
    next_source_action: row.next_source_action,
  })),
  first_archive_request_targets: requestTriads.map((row) => ({
    independence_rank: audited.indexOf(row) + 1,
    target: row.target_cisi,
    controls: [row.control_033_cisi, row.control_032_cisi],
    source_hooks: [row.target_source_hooks, row.control_033_source_hooks, row.control_032_source_hooks],
    action: row.next_source_action,
  })),
  boundary:
    'Triad independence and archive request audit only. It ranks source-check opportunities and accepts no sign reading.',
  outputs: [
    'data/open_prototype/reports/lipi_frame700_034_independent_triad_audit.csv',
    'data/open_prototype/reports/lipi_frame700_034_independent_triad_audit_summary.json',
    'data/open_prototype/reports/lipi_frame700_034_archive_request_batch.csv',
  ],
};

fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
