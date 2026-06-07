import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const cleanPath = path.join(reportsDir, 'lipi_frame700_034_clean_two_panel_close_read.csv');
const messyPath = path.join(reportsDir, 'lipi_frame700_034_messy_panel_reconciliation.csv');
const visualPath = path.join(reportsDir, 'lipi_frame700_034_ia_cisi_visual_inspection.csv');
const triadPath = path.join(reportsDir, 'lipi_frame700_034_source_triad_packet.csv');

const nodeOut = path.join(reportsDir, 'lipi_frame700_034_source_panel_graph_nodes.csv');
const edgeOut = path.join(reportsDir, 'lipi_frame700_034_source_panel_graph_edges.csv');
const triadOut = path.join(
  reportsDir,
  'lipi_frame700_034_source_panel_graph_triad_admissibility.csv',
);
const summaryOut = path.join(
  reportsDir,
  'lipi_frame700_034_source_panel_graph_summary.json',
);

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
      rows.push(row);
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

  const [header, ...body] = rows.filter((entry) => entry.length > 1 || entry[0] !== '');
  return body.map((entry) =>
    Object.fromEntries(header.map((key, index) => [key, entry[index] ?? ''])),
  );
}

function readCsv(filePath) {
  return parseCsv(fs.readFileSync(filePath, 'utf8'));
}

function toCsv(rows) {
  if (rows.length === 0) return '';
  const header = Object.keys(rows[0]);
  const body = rows.map((row) =>
    header
      .map((key) => {
        const text = String(row[key] ?? '');
        return `"${text.replaceAll('"', '""')}"`;
      })
      .join(','),
  );
  return `${[header.map((key) => `"${key}"`).join(','), ...body].join('\n')}\n`;
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function splitList(value) {
  return String(value ?? '')
    .split(';')
    .map((part) => part.trim())
    .filter(Boolean);
}

function sideLetter(label) {
  const match = String(label).match(/\b([A-F])(?:\s|$|bis|ter|quater|quinquies)/);
  return match ? match[1] : '';
}

function panelClass(label) {
  if (/\([0-9]+\)\s+[A-F]/.test(label)) return 'unresolved_numbered_object_form';
  if (/\b(?:bis|ter|quater|quinquies)\b/.test(label)) {
    return 'same_side_later_photo_under_cisi_convention';
  }
  const side = sideLetter(label);
  if (side === 'C') return 'base_C_side_category_under_cisi_convention';
  if (side) return `base_${side}_side_label_under_cisi_convention`;
  return 'unclassified_source_label';
}

function roleForLabel(label, shortCandidate, companionCandidate, extraLabels) {
  const shortText = String(shortCandidate ?? '');
  const companionText = String(companionCandidate ?? '');
  const extraText = String(extraLabels ?? '');
  if (shortText.includes(label)) return 'short_frame700_candidate';
  if (shortText.includes('multiple_B') && /\bB/.test(label)) return 'ambiguous_short_B_candidate';
  if (shortText.includes('B or') && /\bB/.test(label)) return 'ambiguous_short_B_candidate';
  if (companionText.includes(label)) return 'companion_candidate';
  if (extraText.includes(label)) return 'extra_or_variant_source_label';
  return 'unmapped_visible_source_label';
}

function addNode(nodes, row) {
  nodes.push({
    checked_date: '2026-05-25',
    graph_scope: 'FRAME700_034_source_panel_graph',
    cisi: row.cisi,
    source_label: row.source_label,
    side_letter: sideLetter(row.source_label),
    panel_class: panelClass(row.source_label),
    local_role_candidate: row.local_role_candidate,
    local_frame700_row: row.local_frame700_row,
    local_companion_row: row.local_companion_row,
    ia_volume: row.ia_volume,
    ia_leafs: row.ia_leafs,
    source_page_heading: row.source_page_heading,
    source_state: row.source_state,
    mapping_grade: row.mapping_grade,
    blocker: row.blocker,
    admissible_for_panel_graph: row.admissible_for_panel_graph,
    admissible_for_substitution_test: row.admissible_for_substitution_test,
    accepted_decipherment_claim: '0',
  });
}

function addEdge(edges, row) {
  edges.push({
    checked_date: '2026-05-25',
    graph_scope: 'FRAME700_034_source_panel_graph',
    cisi: row.cisi,
    edge_type: row.edge_type,
    local_text: row.local_text,
    source_label_or_labels: row.source_label_or_labels,
    source_state: row.source_state,
    edge_grade: row.edge_grade,
    blocker: row.blocker,
    basis: row.basis,
    accepted_decipherment_claim: '0',
  });
}

const cleanRows = readCsv(cleanPath);
const messyRows = readCsv(messyPath);
const visualRows = readCsv(visualPath);
const triadRows = readCsv(triadPath);

const nodes = [];
const edges = [];
const objectState = new Map();

for (const row of cleanRows) {
  objectState.set(row.cisi, 'clean_two_panel_calibration_control');
  for (const label of splitList(row.source_labels_visible)) {
    addNode(nodes, {
      cisi: row.cisi,
      source_label: label,
      local_role_candidate: roleForLabel(
        label,
        row.short_panel_candidate_label,
        row.companion_panel_candidate_label,
        '',
      ),
      local_frame700_row: row.local_frame700_row,
      local_companion_row: row.local_companion_row,
      ia_volume: row.ia_volume,
      ia_leafs: row.ia_leaf,
      source_page_heading: row.source_page_heading,
      source_state: 'clean_two_panel_calibration_control',
      mapping_grade:
        'object_identity_panel_count_and_short_vs_long_split_supported_not_subtype_or_direction',
      blocker: 'diagnostic_subtype_and_direction_not_secure_from_scan',
      admissible_for_panel_graph: '1',
      admissible_for_substitution_test: '0',
    });
  }
  addEdge(edges, {
    cisi: row.cisi,
    edge_type: 'companion_panel_mapping',
    local_text: row.local_companion_row,
    source_label_or_labels: row.companion_panel_candidate_label,
    source_state: 'clean_two_panel_calibration_control',
    edge_grade: 'catalog_compatible_clean_control',
    blocker: 'not_independent_direction_or_subtype_validation',
    basis: row.close_read_observation,
  });
  addEdge(edges, {
    cisi: row.cisi,
    edge_type: 'frame700_short_panel_mapping',
    local_text: row.local_frame700_row,
    source_label_or_labels: row.short_panel_candidate_label,
    source_state: 'clean_two_panel_calibration_control',
    edge_grade: 'catalog_compatible_clean_control',
    blocker: 'not_independent_direction_or_subtype_validation',
    basis: row.close_read_observation,
  });
}

for (const row of messyRows) {
  objectState.set(row.cisi, 'blocked_source_panel_mapping');
  for (const label of splitList(row.source_labels_visible)) {
    addNode(nodes, {
      cisi: row.cisi,
      source_label: label,
      local_role_candidate: roleForLabel(
        label,
        row.short_candidate_label,
        row.long_or_companion_candidate_labels,
        row.extra_panel_or_variant_labels,
      ),
      local_frame700_row: row.local_frame700_row,
      local_companion_row: row.local_companion_row,
      ia_volume: row.ia_volume,
      ia_leafs: row.ia_leafs_inspected,
      source_page_heading: row.source_page_heading,
      source_state: 'blocked_source_panel_mapping',
      mapping_grade: row.source_research_decision,
      blocker: row.variant_failure_mode,
      admissible_for_panel_graph: '1',
      admissible_for_substitution_test: '0',
    });
  }
  addEdge(edges, {
    cisi: row.cisi,
    edge_type: 'blocked_frame700_short_panel_candidate',
    local_text: row.local_frame700_row,
    source_label_or_labels: row.short_candidate_label,
    source_state: 'blocked_source_panel_mapping',
    edge_grade: row.source_research_decision,
    blocker: row.variant_failure_mode,
    basis: row.close_read_observation,
  });
  addEdge(edges, {
    cisi: row.cisi,
    edge_type: 'blocked_companion_panel_candidate',
    local_text: row.local_companion_row,
    source_label_or_labels: row.long_or_companion_candidate_labels,
    source_state: 'blocked_source_panel_mapping',
    edge_grade: row.companion_mapping_status,
    blocker: row.variant_failure_mode,
    basis: row.close_read_observation,
  });
}

for (const row of visualRows) {
  if (objectState.has(row.cisi)) continue;
  if (row.page_kind !== 'visual_plate_page') {
    objectState.set(row.cisi, 'register_or_nonvisual_locator');
    continue;
  }
  objectState.set(row.cisi, 'visual_locator_not_close_read');
  for (const label of splitList(row.source_labels_visible)) {
    addNode(nodes, {
      cisi: row.cisi,
      source_label: label,
      local_role_candidate: /\bB/.test(label)
        ? 'rough_short_frame700_candidate'
        : 'rough_companion_candidate',
      local_frame700_row: row.local_frame700_row,
      local_companion_row: row.local_companion_row,
      ia_volume: row.ia_volume,
      ia_leafs: row.ia_leafs_inspected,
      source_page_heading: row.source_page_heading,
      source_state: 'visual_locator_not_close_read',
      mapping_grade: row.source_coding_decision,
      blocker: row.copy_or_variant_risk,
      admissible_for_panel_graph: '1',
      admissible_for_substitution_test: '0',
    });
  }
}

function stateFor(cisi) {
  return objectState.get(cisi) ?? 'no_source_panel_in_current_graph';
}

function triadStatus(states) {
  if (states.every((state) => state === 'clean_two_panel_calibration_control')) {
    return 'not_admissible_subtype_direction_still_unvalidated';
  }
  if (states.some((state) => state === 'blocked_source_panel_mapping')) {
    return 'not_admissible_blocked_panel_mapping_or_variant_status';
  }
  if (states.some((state) => state === 'register_or_nonvisual_locator')) {
    return 'not_admissible_register_only_source_locator';
  }
  if (states.some((state) => state === 'visual_locator_not_close_read')) {
    return 'not_admissible_visual_locator_not_close_read';
  }
  return 'not_admissible_missing_source_panel_nodes';
}

const triadAdmissibility = triadRows.map((row) => {
  const targetState = stateFor(row.target_cisi);
  const control033State = stateFor(row.control_033_cisi);
  const control032State = stateFor(row.control_032_cisi);
  const states = [targetState, control033State, control032State];
  const cleanCount = states.filter(
    (state) => state === 'clean_two_panel_calibration_control',
  ).length;
  const blockedCount = states.filter((state) => state === 'blocked_source_panel_mapping').length;
  const missingCount = states.filter((state) => state === 'no_source_panel_in_current_graph').length;
  return {
    checked_date: '2026-05-25',
    triad_rank: row.triad_rank,
    target_bucket: row.target_bucket,
    target_cisi: row.target_cisi,
    target_short_text: row.target_short_text,
    target_source_state: targetState,
    control_033_cisi: row.control_033_cisi,
    control_033_short_text: row.control_033_short_text,
    control_033_source_state: control033State,
    control_032_cisi: row.control_032_cisi,
    control_032_short_text: row.control_032_short_text,
    control_032_source_state: control032State,
    clean_calibration_objects_in_triad: cleanCount,
    blocked_source_objects_in_triad: blockedCount,
    missing_source_objects_in_triad: missingCount,
    triad_source_graph_status: triadStatus(states),
    admissible_for_032_033_034_substitution_test: '0',
    reason:
      'A source-normalized substitution test requires all three objects to have mapped source panels plus secure visual subtype and direction; current graph does not meet that gate.',
    accepted_decipherment_claim: '0',
  };
});

const sourceObjects = unique([...nodes.map((row) => row.cisi), ...[...objectState.keys()]]);
const summary = {
  generated_at: '2026-05-25',
  artifact: 'lipi_frame700_034_source_panel_graph',
  source_objects_in_graph_or_locator_map: sourceObjects.length,
  panel_node_rows: nodes.length,
  local_to_source_edge_rows: edges.length,
  triad_rows_scored: triadAdmissibility.length,
  clean_two_panel_calibration_objects: unique(
    [...objectState.entries()]
      .filter(([, state]) => state === 'clean_two_panel_calibration_control')
      .map(([cisi]) => cisi),
  ).join(';'),
  blocked_panel_mapping_objects: unique(
    [...objectState.entries()]
      .filter(([, state]) => state === 'blocked_source_panel_mapping')
      .map(([cisi]) => cisi),
  ).join(';'),
  visual_locator_not_close_read_objects: unique(
    [...objectState.entries()]
      .filter(([, state]) => state === 'visual_locator_not_close_read')
      .map(([cisi]) => cisi),
  ).join(';'),
  register_or_nonvisual_locator_objects: unique(
    [...objectState.entries()]
      .filter(([, state]) => state === 'register_or_nonvisual_locator')
      .map(([cisi]) => cisi),
  ).join(';'),
  source_normalized_substitution_triads: triadAdmissibility.filter(
    (row) => row.admissible_for_032_033_034_substitution_test !== '0',
  ).length,
  triads_with_any_clean_calibration_object: triadAdmissibility.filter(
    (row) => Number(row.clean_calibration_objects_in_triad) > 0,
  ).length,
  triads_with_any_blocked_source_object: triadAdmissibility.filter(
    (row) => Number(row.blocked_source_objects_in_triad) > 0,
  ).length,
  triads_with_missing_source_objects: triadAdmissibility.filter(
    (row) => Number(row.missing_source_objects_in_triad) > 0,
  ).length,
  accepted_decipherment_claims: 0,
  research_conclusion:
    'The current IA/CISI source graph supports panel-calibration controls for H-930 and H-789, but it yields zero admissible 032/033/034 substitution triads. The FRAME700 034 residue remains live as a source-targeted hypothesis, not a source-normalized sign-function result.',
};

fs.writeFileSync(nodeOut, toCsv(nodes));
fs.writeFileSync(edgeOut, toCsv(edges));
fs.writeFileSync(triadOut, toCsv(triadAdmissibility));
fs.writeFileSync(`${summaryOut}\n`.trim(), `${JSON.stringify(summary, null, 2)}\n`);

console.log(`Wrote ${nodeOut}`);
console.log(`Wrote ${edgeOut}`);
console.log(`Wrote ${triadOut}`);
console.log(`Wrote ${summaryOut}`);
