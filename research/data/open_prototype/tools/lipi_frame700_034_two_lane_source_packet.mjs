import fs from 'node:fs';
import path from 'node:path';

// This script cuts the full triad list down to a deliberate working set of nine triads in
// three lanes, each answering a different failure mode: four "independent low copy" triads
// (does the 034 contrast escape copy families?), four "local contrast stress" triads (does
// it survive strict local matching?), and one optional "repeated branch check". The lanes
// and their target objects are hard-coded in triadPlan. It reads the triad packet, the
// matched-contrast stability grades, and the corpus metadata, then writes two worksheets:
// a packet CSV with one row per participant (target, 033 control, 032 control -- 27 rows)
// carrying source hooks, ready-made public search queries, and grade/downgrade/kill
// criteria; and a coding sheet CSV with one row per catalog metadata row (51 rows) whose
// ~30 manual fields (side order basis, direction basis, mirror status, subtype
// separability, ...) all start as unknown/uncertain for a human to fill from source images.
// A JSON summary counts lanes, roles, and hook grades. It is a request-and-coding packet,
// not a validation.

const base = process.cwd();
const dataDir = path.join(base, 'data', 'open_prototype');
const reportsDir = path.join(dataDir, 'reports');

const triadPath = path.join(reportsDir, 'lipi_frame700_034_source_triad_packet.csv');
const stabilityPath = path.join(reportsDir, 'lipi_frame700_034_matched_contrast_stability.csv');
const metadataPath = path.join(dataDir, 'lipi', 'metadata_filtered.csv');

const packetCsvPath = path.join(reportsDir, 'lipi_frame700_034_two_lane_source_packet.csv');
const codingCsvPath = path.join(reportsDir, 'lipi_frame700_034_two_lane_source_coding_sheet.csv');
const summaryJsonPath = path.join(reportsDir, 'lipi_frame700_034_two_lane_source_packet_summary.json');

const triadPlan = [
  {
    lane: 'independent_low_copy',
    lane_rank: 1,
    batch_id: 'independent_1850_1842_1772',
    target_cisi: 'H-1850',
    priority: 'core',
    lane_question: 'copy_family_escape',
  },
  {
    lane: 'independent_low_copy',
    lane_rank: 2,
    batch_id: 'independent_771_789_1123',
    target_cisi: 'H-771',
    priority: 'core',
    lane_question: 'copy_family_escape',
  },
  {
    lane: 'independent_low_copy',
    lane_rank: 3,
    batch_id: 'independent_1943_1940_854',
    target_cisi: 'H-1943',
    priority: 'core',
    lane_question: 'copy_family_escape',
  },
  {
    lane: 'independent_low_copy',
    lane_rank: 4,
    batch_id: 'independent_2204_2209_2217',
    target_cisi: 'H-2204',
    priority: 'core',
    lane_question: 'copy_family_escape_with_identity_reconcile',
  },
  {
    lane: 'local_contrast_stress',
    lane_rank: 1,
    batch_id: 'local_893_925_930',
    target_cisi: 'H-893',
    priority: 'core',
    lane_question: 'strict_local_contrast',
  },
  {
    lane: 'local_contrast_stress',
    lane_rank: 2,
    batch_id: 'local_1824_1883_212',
    target_cisi: 'H-1824',
    priority: 'core',
    lane_question: 'visual_object_contrast',
  },
  {
    lane: 'local_contrast_stress',
    lane_rank: 3,
    batch_id: 'local_2137_925_930',
    target_cisi: 'H-2137',
    priority: 'core',
    lane_question: 'reuse_controls_stress',
  },
  {
    lane: 'local_contrast_stress',
    lane_rank: 4,
    batch_id: 'local_983_353_2211',
    target_cisi: 'H-983',
    priority: 'core',
    lane_question: 'visual_object_contrast',
  },
  {
    lane: 'repeated_branch_check',
    lane_rank: 1,
    batch_id: 'optional_910_916_1294',
    target_cisi: 'H-910',
    priority: 'optional',
    lane_question: 'old_branch_repetition_check',
  },
];

const manualFields = {
  source_url: '',
  source_ref: '',
  image_or_plate_id: '',
  image_kind: 'unknown',
  image_quality: 'unknown',
  object_identity_status: 'uncertain',
  side_visible: 'unknown',
  side_id_source: 'unknown',
  side_order_basis: 'unknown',
  physical_side_confidence: 'catalog_only',
  direction_basis: 'unknown',
  mirror_status: 'unknown',
  direction_safe: 'uncertain',
  source_matches_catalog: 'uncertain',
  frame700_visible: 'unknown',
  source_companion_read: 'unknown',
  catalog_source_agree: 'uncertain',
  sign_visibility_status: 'unknown',
  companion_visibility_status: 'unknown',
  subtype_separability: 'uncertain',
  diagnostic_strokes_visible: 'unknown',
  allograph_risk: 'unknown',
  formula_order_source: 'unknown',
  longer_row_visibility_status: 'unknown',
  long_side_present: 'unknown',
  long_side_source_read: '',
  long_side_family_source: 'unknown',
  side_relation_source: 'unknown',
  source_side_count: 'unknown',
  duplicate_or_copy_note: 'unknown',
  independent_attestation: 'uncertain',
  research_decision: 'unreviewed',
  decision_reason: '',
  reviewer_notes: 'need_source_image',
};

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

function splitLocalRows(value) {
  return String(value ?? '')
    .split(';')
    .map((item) => item.trim())
    .filter(Boolean);
}

function sourceHookGrade(hook) {
  const text = String(hook ?? '');
  if (/H\d{2,4}-\d+/.test(text) && /Figure/i.test(text)) return 'excavation_plus_figure_hook';
  if (/Figure/i.test(text)) return 'figure_hook';
  if (/H\d{2,4}-\d+/.test(text)) return 'excavation_hook';
  if (text && text !== 'none') return 'catalog_or_archive_handle';
  return 'missing_hook';
}

function normalizeBatch(row) {
  return `${row.lane}:${row.batch_id}:${row.role}`;
}

function byKey(rows, key) {
  return new Map(rows.map((row) => [row[key], row]));
}

function countBy(rows, keyFn) {
  const counts = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return Object.fromEntries([...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])));
}

function participantRows(plan, triad, stability) {
  const common = {
    lane: plan.lane,
    lane_rank: plan.lane_rank,
    batch_id: plan.batch_id,
    priority: plan.priority,
    lane_question: plan.lane_question,
    target_cisi: plan.target_cisi,
    target_grade: stability?.grade ?? '',
    target_copy_pressure: stability?.copy_pressure ?? '',
    target_long_context_relation: stability?.long_context_relation ?? '',
    target_independence_rank: stability?.independence_rank ?? '',
    target_shared_matches: stability?.shared_matches ?? '',
  };
  return [
    {
      ...common,
      role: 'target_034',
      cisi: triad.target_cisi,
      row_id: triad.target_row_id,
      short_text: triad.target_short_text,
      source_hooks: triad.target_source_hooks,
      local_rows: triad.target_local_rows,
      material_shape: triad.target_material_shape,
      period_phase_depth: triad.target_period_phase_depth,
      dimensions_mm: triad.target_dimensions_mm,
      source_use: 'check_target_row_and_contrast',
    },
    {
      ...common,
      role: 'control_033',
      cisi: triad.control_033_cisi,
      row_id: triad.control_033_row_id,
      short_text: triad.control_033_short_text,
      source_hooks: triad.control_033_source_hooks,
      local_rows: triad.control_033_local_rows,
      material_shape: triad.control_033_material_shape,
      period_phase_depth: triad.control_033_period_phase_depth,
      dimensions_mm: triad.control_033_dimensions_mm,
      source_use: 'check_033_control_row',
    },
    {
      ...common,
      role: 'control_032',
      cisi: triad.control_032_cisi,
      row_id: triad.control_032_row_id,
      short_text: triad.control_032_short_text,
      source_hooks: triad.control_032_source_hooks,
      local_rows: triad.control_032_local_rows,
      material_shape: triad.control_032_material_shape,
      period_phase_depth: triad.control_032_period_phase_depth,
      dimensions_mm: triad.control_032_dimensions_mm,
      source_use: 'check_032_control_row',
    },
  ];
}

function queryStrings(cisi, hook) {
  const cleanHook = String(hook ?? '').replaceAll(';', ' ').replace(/\s+/g, ' ').trim();
  const parts = [cisi, cleanHook].filter(Boolean).join(' ');
  return [
    `"${cisi}" Indus`,
    cleanHook ? `"${cleanHook}" Harappa` : `"${cisi}" Harappa`,
    `${parts} "Corpus of Indus Seals and Inscriptions"`,
  ].join(' | ');
}

function companionFromText(text) {
  const tokens = String(text ?? '').match(/\d{3}/g) ?? [];
  for (const token of ['032', '033', '034']) {
    if (tokens.includes(token)) return token;
  }
  return tokens.includes('700') ? 'other_700_companion' : 'not_frame700_row';
}

function frameOrder(text) {
  const tokens = String(text ?? '').match(/\d{3}/g) ?? [];
  const index700 = tokens.indexOf('700');
  const indexCompanion = tokens.findIndex((token) => ['032', '033', '034'].includes(token));
  if (index700 < 0 || indexCompanion < 0) return 'not_applicable';
  if (index700 < indexCompanion) return '700_first';
  if (index700 > indexCompanion) return '700_last';
  return 'uncertain';
}

const triads = readCsvRecords(triadPath);
const stabilityRows = readCsvRecords(stabilityPath);
const metadataRows = readCsvRecords(metadataPath);

const triadByTarget = byKey(triads, 'target_cisi');
const stabilityByTarget = byKey(stabilityRows, 'target_cisi');

const participantRowsOut = [];
for (const plan of triadPlan) {
  const triad = triadByTarget.get(plan.target_cisi);
  if (!triad) throw new Error(`Missing triad for ${plan.target_cisi}`);
  participantRowsOut.push(...participantRows(plan, triad, stabilityByTarget.get(plan.target_cisi)));
}

const packetHeader = [
  'lane',
  'lane_rank',
  'batch_id',
  'priority',
  'lane_question',
  'role',
  'cisi',
  'row_id',
  'short_text',
  'source_hooks',
  'source_hook_grade',
  'local_rows',
  'material_shape',
  'period_phase_depth',
  'dimensions_mm',
  'target_cisi',
  'target_grade',
  'target_copy_pressure',
  'target_long_context_relation',
  'target_independence_rank',
  'target_shared_matches',
  'source_use',
  'public_search_queries',
  'source_grade_if',
  'downgrade_if',
  'kill_if',
  'packet_status',
];

const packetRows = participantRowsOut.map((row) => ({
  ...row,
  source_hook_grade: sourceHookGrade(row.source_hooks),
  public_search_queries: queryStrings(row.cisi, row.source_hooks),
  source_grade_if:
    'source image confirms object identity, row visibility, side distinctness, source order, direction basis, and 032/033/034 separation',
  downgrade_if:
    'object identity is plausible but side order, direction, row visibility, or control comparability remains uncertain',
  kill_if:
    'object mismatch, row not visible, sign contrast collapses, side assignment fails, or source row is only a duplicate/copy artifact',
  packet_status: 'source_request_only_not_validated',
}));

fs.writeFileSync(packetCsvPath, toCsv([packetHeader, ...packetRows.map((row) => packetHeader.map((key) => row[key]))]));

const objectRoles = new Map();
for (const row of packetRows) {
  const existing = objectRoles.get(row.cisi) ?? {
    cisi: row.cisi,
    priority: new Set(),
    lanes: new Set(),
    batch_ids: new Set(),
    roles: new Set(),
    participant_rows: [],
    source_hooks: new Set(),
    target_grades: new Set(),
    copy_pressures: new Set(),
  };
  existing.priority.add(row.priority);
  existing.lanes.add(row.lane);
  existing.batch_ids.add(row.batch_id);
  existing.roles.add(row.role);
  existing.participant_rows.push(row.row_id);
  existing.source_hooks.add(row.source_hooks);
  existing.target_grades.add(row.target_grade);
  existing.copy_pressures.add(row.target_copy_pressure);
  objectRoles.set(row.cisi, existing);
}

const codingHeader = [
  'priority',
  'lanes',
  'batch_ids',
  'roles_in_packet',
  'participant_row_ids',
  'cisi',
  'metadata_row_id',
  'catalog_text',
  'catalog_companion_read',
  'catalog_formula_order',
  'side_id_local',
  'catalog_type',
  'site',
  'material',
  'shape',
  'cross_section',
  'period',
  'phase',
  'depth',
  'metadata_sides',
  'metadata_dimensions_mm',
  'source_hooks',
  'source_hook_grade',
  'target_grades_in_batches',
  'copy_pressures_in_batches',
  'source_check_fields',
  'source_grade_if',
  'downgrade_if',
  'kill_if',
  ...Object.keys(manualFields),
];

const codingRows = [];
for (const row of metadataRows) {
  const roles = objectRoles.get(row.cisi);
  if (!roles) continue;
  const sourceHooks = [...roles.source_hooks].filter(Boolean).join('; ');
  codingRows.push({
    priority: [...roles.priority].sort().join(';'),
    lanes: [...roles.lanes].sort().join(';'),
    batch_ids: [...roles.batch_ids].sort().join(';'),
    roles_in_packet: [...roles.roles].sort().join(';'),
    participant_row_ids: [...roles.participant_rows].sort().join(';'),
    cisi: row.cisi,
    metadata_row_id: row.id,
    catalog_text: row.text,
    catalog_companion_read: companionFromText(row.text),
    catalog_formula_order: frameOrder(row.text),
    side_id_local: `side_${String(row.id).split('.')[1] ?? ''}`,
    catalog_type: row.type,
    site: row.site,
    material: row.material,
    shape: row.shape,
    cross_section: row['cross-section'],
    period: row.period,
    phase: row.phase,
    depth: row.depth,
    metadata_sides: row.sides,
    metadata_dimensions_mm: `${row['horizontal(mm)']} x ${row['vertical(mm)']} x ${row['thickness(mm)']}`,
    source_hooks: sourceHooks,
    source_hook_grade: sourceHookGrade(sourceHooks),
    target_grades_in_batches: [...roles.target_grades].filter(Boolean).sort().join(';'),
    copy_pressures_in_batches: [...roles.copy_pressures].filter(Boolean).sort().join(';'),
    source_check_fields:
      'object identity; side distinctness; source side count; direction basis; mirror status; frame700 visibility; source companion read; subtype separability; diagnostic strokes; longer-row visibility; catalog/source agreement; duplicate/copy note; independent attestation; research decision',
    source_grade_if:
      'object, side, row, direction, and sign contrast are source-visible and match the packet role',
    downgrade_if:
      'source supports object but leaves row, side, direction, or contrast unresolved',
    kill_if:
      'wrong object, wrong row, invisible sign, collapsed contrast, failed side assignment, or unrecoverable duplicate/copy risk',
    ...manualFields,
  });
}

codingRows.sort((a, b) => {
  const priority = (value) => (String(value).includes('core') ? 0 : 1);
  const laneOrder = (value) => {
    if (String(value).includes('independent_low_copy')) return 0;
    if (String(value).includes('local_contrast_stress')) return 1;
    return 2;
  };
  return (
    priority(a.priority) - priority(b.priority) ||
    laneOrder(a.lanes) - laneOrder(b.lanes) ||
    a.cisi.localeCompare(b.cisi, undefined, { numeric: true }) ||
    a.metadata_row_id.localeCompare(b.metadata_row_id, undefined, { numeric: true })
  );
});

fs.writeFileSync(codingCsvPath, toCsv([codingHeader, ...codingRows.map((row) => codingHeader.map((key) => row[key]))]));

const coreObjects = new Set(packetRows.filter((row) => row.priority === 'core').map((row) => row.cisi));
const optionalObjects = new Set(packetRows.filter((row) => row.priority === 'optional').map((row) => row.cisi));
const summary = {
  date: '2026-05-25',
  experiment: 'Lipi FRAME700 034 two-lane source packet',
  inputs: [path.relative(base, triadPath), path.relative(base, stabilityPath), path.relative(base, metadataPath)],
  core_triads: triadPlan.filter((row) => row.priority === 'core').length,
  optional_triads: triadPlan.filter((row) => row.priority === 'optional').length,
  participant_rows: packetRows.length,
  core_unique_objects: coreObjects.size,
  optional_unique_objects: optionalObjects.size,
  all_unique_objects: objectRoles.size,
  coding_rows: codingRows.length,
  lanes: countBy(packetRows, (row) => row.lane),
  roles: countBy(packetRows, (row) => row.role),
  source_hook_grades: countBy(packetRows, (row) => row.source_hook_grade),
  core_object_list: [...coreObjects].sort((a, b) => a.localeCompare(b, undefined, { numeric: true })),
  optional_object_list: [...optionalObjects].sort((a, b) => a.localeCompare(b, undefined, { numeric: true })),
  accepted_decipherment_claims: 0,
  status: 'source_request_packet_not_validation',
  outputs: [path.relative(base, packetCsvPath), path.relative(base, codingCsvPath), path.relative(base, summaryJsonPath)],
};

fs.writeFileSync(summaryJsonPath, `${JSON.stringify(summary, null, 2)}\n`);

console.log(
  JSON.stringify(
    {
      packetCsvPath,
      codingCsvPath,
      summaryJsonPath,
      participant_rows: packetRows.length,
      coding_rows: codingRows.length,
      all_unique_objects: objectRoles.size,
    },
    null,
    2,
  ),
);
