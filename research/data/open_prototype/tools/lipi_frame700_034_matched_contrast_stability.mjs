import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const triadPath = path.join(reportsDir, 'lipi_frame700_034_source_triad_packet.csv');
const independentPath = path.join(reportsDir, 'lipi_frame700_034_independent_triad_audit.csv');

const outputCsvPath = path.join(reportsDir, 'lipi_frame700_034_matched_contrast_stability.csv');
const summaryJsonPath = path.join(reportsDir, 'lipi_frame700_034_matched_contrast_stability_summary.json');

const objectCore = ['type', 'sides', 'site', 'material', 'shape', 'cross_section'];
const visualCore = ['h_bin', 'v_bin', 'area_bin', 'aspect_bin'];
const contextCore = ['context_class', 'side_relation', 'order'];
const strictCore = [...objectCore, ...visualCore, ...contextCore];

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

function splitList(value) {
  return String(value ?? '')
    .split(';')
    .map((item) => item.trim())
    .filter(Boolean);
}

function asSet(value) {
  return new Set(splitList(value));
}

function intersect(a, b) {
  return [...a].filter((item) => b.has(item)).sort((x, y) => x.localeCompare(y));
}

function includesAll(items, required) {
  const set = new Set(items);
  return required.every((item) => set.has(item));
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

function sharedGrade(shared) {
  const objectAll = includesAll(shared, objectCore);
  const visualAll = includesAll(shared, visualCore);
  const contextAll = includesAll(shared, contextCore);
  const orderSafe = shared.includes('order');
  const sideSafe = shared.includes('side_relation');
  if (objectAll && visualAll && contextAll) return 'A_strict_local_minimal_contrast';
  if (objectAll && visualAll && orderSafe) return 'B_visual_object_order_matched';
  if (objectAll && visualAll) return 'C_visual_object_matched';
  if (objectAll && (orderSafe || sideSafe)) return 'D_object_plus_some_context';
  if (objectAll) return 'E_object_only';
  return 'F_partial_or_weak';
}

function relation(row) {
  const target = row.target_long_token_set;
  const c033 = row.control_033_long_token_set;
  const c032 = row.control_032_long_token_set;
  if (!target || !c033 || !c032) return 'long_context_incomplete';
  if (target === c033 && target === c032) return 'same_as_both_controls';
  if (target === c033) return 'same_as_033_control';
  if (target === c032) return 'same_as_032_control';
  if (c033 === c032) return 'target_differs_controls_share';
  return 'all_three_differ';
}

function pressureFlag(independent) {
  if (!independent) return 'not_in_independent_audit';
  const longCount = number(independent.target_long_set_count) ?? 999;
  const familyCount = number(independent.acquisition_family_count) ?? 999;
  const tier = independent.evidence_tier || '';
  if (tier.startsWith('A_') && longCount <= 1 && familyCount <= 1) return 'low_repetition_pressure';
  if (longCount <= 2 && familyCount <= 1) return 'moderate_repetition_pressure';
  return 'high_repetition_pressure';
}

const triads = readCsvRecords(triadPath);
const independentRows = readCsvRecords(independentPath);
const independentByTarget = new Map(independentRows.map((row) => [row.target_cisi, row]));

const outputRows = triads.map((row) => {
  const match033 = asSet(row.control_033_matches);
  const match032 = asSet(row.control_032_matches);
  const shared = intersect(match033, match032);
  const independent = independentByTarget.get(row.target_cisi);
  return {
    target_cisi: row.target_cisi,
    target_row_id: row.target_row_id,
    target_short_text: row.target_short_text,
    target_bucket: row.target_bucket,
    original_triad_rank: row.triad_rank,
    independence_rank: independent?.independence_rank ?? '',
    evidence_tier: independent?.evidence_tier ?? '',
    shared_match_count: shared.length,
    shared_matches: shared.join(';'),
    object_core_count: objectCore.filter((item) => shared.includes(item)).length,
    visual_core_count: visualCore.filter((item) => shared.includes(item)).length,
    context_core_count: contextCore.filter((item) => shared.includes(item)).length,
    grade: sharedGrade(shared),
    long_context_relation: relation(row),
    copy_pressure: pressureFlag(independent),
    control_033_cisi: row.control_033_cisi,
    control_033_score: row.control_033_score,
    control_032_cisi: row.control_032_cisi,
    control_032_score: row.control_032_score,
    target_source_hooks: row.target_source_hooks,
    control_033_source_hooks: row.control_033_source_hooks,
    control_032_source_hooks: row.control_032_source_hooks,
    local_use: 'source_targeting_only',
  };
});

outputRows.sort((a, b) => {
  const rankA = number(a.independence_rank) ?? 9999;
  const rankB = number(b.independence_rank) ?? 9999;
  if (rankA !== rankB) return rankA - rankB;
  return (number(a.original_triad_rank) ?? 9999) - (number(b.original_triad_rank) ?? 9999);
});

const strongRows = outputRows.filter((row) =>
  ['A_strict_local_minimal_contrast', 'B_visual_object_order_matched', 'C_visual_object_matched'].includes(row.grade),
);
const lowPressureStrongRows = strongRows.filter((row) => row.copy_pressure === 'low_repetition_pressure');
const firstIndependentRows = outputRows.filter((row) => ['1', '2', '3', '4'].includes(String(row.independence_rank)));

const header = [
  'target_cisi',
  'target_row_id',
  'target_short_text',
  'target_bucket',
  'original_triad_rank',
  'independence_rank',
  'evidence_tier',
  'shared_match_count',
  'shared_matches',
  'object_core_count',
  'visual_core_count',
  'context_core_count',
  'grade',
  'long_context_relation',
  'copy_pressure',
  'control_033_cisi',
  'control_033_score',
  'control_032_cisi',
  'control_032_score',
  'target_source_hooks',
  'control_033_source_hooks',
  'control_032_source_hooks',
  'local_use',
];

fs.writeFileSync(outputCsvPath, toCsv([header, ...outputRows.map((row) => header.map((key) => row[key]))]));

const summary = {
  date: '2026-05-25',
  experiment: 'Lipi FRAME700 034 matched contrast stability',
  question: 'Which 034 matched-control triads remain local contrast candidates after requiring both 033 and 032 controls to share object, visual, and context features?',
  inputs: [path.relative(base, triadPath), path.relative(base, independentPath)],
  triads: outputRows.length,
  grade_counts: countBy(outputRows, (row) => row.grade),
  copy_pressure_counts: countBy(outputRows, (row) => row.copy_pressure),
  long_context_relation_counts: countBy(outputRows, (row) => row.long_context_relation),
  strong_local_contrasts: strongRows.length,
  low_repetition_strong_local_contrasts: lowPressureStrongRows.length,
  first_independent_batch: firstIndependentRows.map((row) => ({
    target_cisi: row.target_cisi,
    independence_rank: row.independence_rank,
    grade: row.grade,
    shared_matches: row.shared_matches,
    long_context_relation: row.long_context_relation,
    copy_pressure: row.copy_pressure,
  })),
  top_low_repetition_strong_targets: lowPressureStrongRows.slice(0, 12).map((row) => ({
    target_cisi: row.target_cisi,
    independence_rank: row.independence_rank,
    grade: row.grade,
    control_033_cisi: row.control_033_cisi,
    control_032_cisi: row.control_032_cisi,
    shared_matches: row.shared_matches,
    long_context_relation: row.long_context_relation,
  })),
  accepted_decipherment_claims: 0,
  conclusion:
    'Local matched-control strength is now separated from repetition pressure. Rows that look locally clean still require source images before any upgrade.',
  outputs: [path.relative(base, outputCsvPath), path.relative(base, summaryJsonPath)],
};

fs.writeFileSync(summaryJsonPath, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify({ outputCsvPath, summaryJsonPath, triads: outputRows.length }, null, 2));
