import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const crosswalkDir = path.join(root, 'data', 'sign_crosswalk');
const outJson = path.join(crosswalkDir, 'audit_summary.json');
const outIssues = path.join(crosswalkDir, 'audit_issues.csv');
const outEdgePressure = path.join(crosswalkDir, 'edge_pressure_summary.csv');

const tableFiles = {
  sign_systems: path.join(crosswalkDir, 'sign_systems.csv'),
  signs: path.join(crosswalkDir, 'signs.csv'),
  artifact_witnesses: path.join(crosswalkDir, 'artifact_witnesses.csv'),
  crosswalk_edges: path.join(crosswalkDir, 'crosswalk_edges.csv'),
  evidence_refs: path.join(crosswalkDir, 'evidence_refs.csv'),
  namespace_gates: path.join(crosswalkDir, 'namespace_gates.csv'),
  review_events: path.join(crosswalkDir, 'review_events.csv'),
};
const manifestPath = path.join(crosswalkDir, 'manifest.json');

const primaryKeys = {
  sign_systems: 'system_id',
  signs: 'sign_uid',
  artifact_witnesses: 'witness_id',
  crosswalk_edges: 'edge_id',
  evidence_refs: 'ref_id',
  namespace_gates: 'gate_id',
  review_events: 'review_id',
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

function loadCsv(filePath) {
  const parsed = parseCsv(fs.readFileSync(filePath, 'utf8'));
  const header = parsed[0] ?? [];
  return parsed.slice(1).map((row) => Object.fromEntries(header.map((name, index) => [name, row[index] ?? ''])));
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

function sha256(filePath) {
  return crypto.createHash('sha256').update(fs.readFileSync(filePath)).digest('hex');
}

function relToAbs(localPath) {
  return path.resolve(root, String(localPath ?? '').replaceAll('/', path.sep));
}

function countBy(rows, key) {
  const out = new Map();
  for (const row of rows) out.set(row[key] ?? '', (out.get(row[key] ?? '') ?? 0) + 1);
  return Object.fromEntries([...out.entries()].sort((a, b) => a[0].localeCompare(b[0])));
}

function addIssue(issues, severity, code, table, rowId, message) {
  issues.push({ severity, code, table, row_id: rowId, message });
}

const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const tables = Object.fromEntries(Object.entries(tableFiles).map(([name, file]) => [name, loadCsv(file)]));
const issues = [];

for (const [name, rows] of Object.entries(tables)) {
  const manifestCount = manifest.output_counts?.[name];
  if (manifestCount !== undefined && Number(manifestCount) !== rows.length) {
    addIssue(
      issues,
      'error',
      'manifest_count_mismatch',
      name,
      '',
      `manifest says ${manifestCount}, file has ${rows.length}`,
    );
  }

  const key = primaryKeys[name];
  const seen = new Map();
  for (const row of rows) {
    const id = row[key];
    if (!id) addIssue(issues, 'error', 'missing_primary_key', name, '', `missing ${key}`);
    seen.set(id, (seen.get(id) ?? 0) + 1);
  }
  for (const [id, count] of seen.entries()) {
    if (count > 1) addIssue(issues, 'error', 'duplicate_primary_key', name, id, `${key} occurs ${count} times`);
  }
}

const systemIds = new Set(tables.sign_systems.map((row) => row.system_id));
const signUids = new Set(tables.signs.map((row) => row.sign_uid));
const witnessIds = new Set(tables.artifact_witnesses.map((row) => row.witness_id));
const refIds = new Set(tables.evidence_refs.map((row) => row.ref_id));

for (const row of tables.signs) {
  if (!systemIds.has(row.system_id)) {
    addIssue(issues, 'error', 'dangling_sign_system', 'signs', row.sign_uid, `unknown system_id ${row.system_id}`);
  }
  if (row.visual_ref_id && !refIds.has(row.visual_ref_id)) {
    addIssue(issues, 'error', 'dangling_visual_ref', 'signs', row.sign_uid, `unknown visual_ref_id ${row.visual_ref_id}`);
  }
}

for (const row of tables.artifact_witnesses) {
  if (!systemIds.has(row.system_id)) {
    addIssue(
      issues,
      'error',
      'dangling_witness_system',
      'artifact_witnesses',
      row.witness_id,
      `unknown system_id ${row.system_id}`,
    );
  }
  if (!row.sign_sequence) {
    addIssue(issues, 'warning', 'empty_sign_sequence', 'artifact_witnesses', row.witness_id, 'empty sign_sequence');
  }
}

const fromEdgeCounts = new Map();
const toEdgeCounts = new Map();
for (const row of tables.crosswalk_edges) {
  if (!signUids.has(row.from_sign_uid)) {
    addIssue(
      issues,
      'error',
      'dangling_edge_from_sign',
      'crosswalk_edges',
      row.edge_id,
      `unknown from_sign_uid ${row.from_sign_uid}`,
    );
  }
  if (!signUids.has(row.to_sign_uid)) {
    addIssue(
      issues,
      'error',
      'dangling_edge_to_sign',
      'crosswalk_edges',
      row.edge_id,
      `unknown to_sign_uid ${row.to_sign_uid}`,
    );
  }
  if (row.accepted_for_analysis === 'true') {
    addIssue(issues, 'error', 'accepted_edge_leak', 'crosswalk_edges', row.edge_id, 'edge accepted_for_analysis=true');
  }
  if (!row.evidence_types) {
    addIssue(issues, 'warning', 'missing_evidence_types', 'crosswalk_edges', row.edge_id, 'empty evidence_types');
  }
  if (Number(row.support_count) <= 0) {
    addIssue(issues, 'warning', 'nonpositive_support_count', 'crosswalk_edges', row.edge_id, `support_count=${row.support_count}`);
  }
  fromEdgeCounts.set(row.from_sign_uid, (fromEdgeCounts.get(row.from_sign_uid) ?? 0) + 1);
  toEdgeCounts.set(row.to_sign_uid, (toEdgeCounts.get(row.to_sign_uid) ?? 0) + 1);
}

for (const row of tables.evidence_refs) {
  if (row.local_path) {
    const abs = relToAbs(row.local_path);
    if (!fs.existsSync(abs)) {
      addIssue(issues, 'error', 'missing_evidence_local_path', 'evidence_refs', row.ref_id, row.local_path);
    } else if (row.sha256) {
      const actual = sha256(abs);
      if (actual !== row.sha256) {
        addIssue(
          issues,
          'error',
          'evidence_sha256_mismatch',
          'evidence_refs',
          row.ref_id,
          `${row.local_path} expected ${row.sha256}, actual ${actual}`,
        );
      }
    }
  }
}

for (const row of tables.review_events) {
  const target = row.edge_id_or_gate_id;
  if (
    target &&
    target !== 'dataset' &&
    !tables.crosswalk_edges.some((edge) => edge.edge_id === target) &&
    !tables.namespace_gates.some((gate) => gate.gate_id === target)
  ) {
    addIssue(issues, 'warning', 'review_target_not_found', 'review_events', row.review_id, `target ${target}`);
  }
}

const acceptedEdges = tables.crosswalk_edges.filter((row) => row.accepted_for_analysis === 'true');
const collisionRows = [];
for (const [sign, edgeCount] of fromEdgeCounts.entries()) {
  if (edgeCount > 1) collisionRows.push({ side: 'from_sign_uid', sign_uid: sign, candidate_edge_count: edgeCount });
}
for (const [sign, edgeCount] of toEdgeCounts.entries()) {
  if (edgeCount > 1) collisionRows.push({ side: 'to_sign_uid', sign_uid: sign, candidate_edge_count: edgeCount });
}
collisionRows.sort(
  (a, b) => Number(b.candidate_edge_count) - Number(a.candidate_edge_count) || a.sign_uid.localeCompare(b.sign_uid),
);

const highPressureEdges = tables.crosswalk_edges
  .filter((row) => Number(row.support_count) >= 10 || Number(row.counterexample_count) > 0)
  .sort(
    (a, b) =>
      Number(b.support_count) - Number(a.support_count) ||
      Number(b.counterexample_count) - Number(a.counterexample_count) ||
      a.edge_id.localeCompare(b.edge_id),
  );

fs.writeFileSync(
  outIssues,
  toCsv([
    ['severity', 'code', 'table', 'row_id', 'message'],
    ...issues.map((issue) => [issue.severity, issue.code, issue.table, issue.row_id, issue.message]),
  ]),
);

fs.writeFileSync(
  outEdgePressure,
  toCsv([
    [
      'edge_id',
      'from_sign_uid',
      'to_sign_uid',
      'support_count',
      'counterexample_count',
      'aligned_positions',
      'top_share',
      'confidence',
      'review_status',
      'accepted_for_analysis',
    ],
    ...highPressureEdges.map((row) => [
      row.edge_id,
      row.from_sign_uid,
      row.to_sign_uid,
      row.support_count,
      row.counterexample_count,
      row.aligned_positions,
      row.top_share,
      row.confidence,
      row.review_status,
      row.accepted_for_analysis,
    ]),
  ]),
);

const summary = {
  date: '2026-05-29',
  status: issues.some((issue) => issue.severity === 'error') ? 'audit_failed' : 'audit_passed_with_caveats',
  manifest_status: manifest.status,
  counts: Object.fromEntries(Object.entries(tables).map(([name, rows]) => [name, rows.length])),
  manifest_counts_match_files: !issues.some((issue) => issue.code === 'manifest_count_mismatch'),
  duplicate_primary_keys: issues.filter((issue) => issue.code === 'duplicate_primary_key').length,
  dangling_reference_errors: issues.filter((issue) => issue.code.startsWith('dangling_')).length,
  evidence_hash_or_path_errors: issues.filter((issue) => issue.code.startsWith('evidence_') || issue.code === 'missing_evidence_local_path')
    .length,
  accepted_crosswalk_edges: acceptedEdges.length,
  edge_status_by_accepted_for_analysis: countBy(tables.crosswalk_edges, 'accepted_for_analysis'),
  edge_confidence_counts: countBy(tables.crosswalk_edges, 'confidence'),
  edge_review_status_counts: countBy(tables.crosswalk_edges, 'review_status'),
  provenance_tier_counts: countBy(tables.artifact_witnesses, 'provenance_tier'),
  namespace_gate_status_counts: countBy(tables.namespace_gates, 'status'),
  multi_edge_from_signs: collisionRows.filter((row) => row.side === 'from_sign_uid').length,
  multi_edge_to_signs: collisionRows.filter((row) => row.side === 'to_sign_uid').length,
  top_collision_pressure: collisionRows.slice(0, 20),
  high_pressure_edge_rows: highPressureEdges.length,
  issue_counts_by_severity: countBy(issues, 'severity'),
  issue_counts_by_code: countBy(issues, 'code'),
  artifact_files: {
    audit_summary: 'data/sign_crosswalk/audit_summary.json',
    audit_issues: 'data/sign_crosswalk/audit_issues.csv',
    edge_pressure_summary: 'data/sign_crosswalk/edge_pressure_summary.csv',
  },
  interpretation_boundary:
    'This audit validates dataset hygiene and caveats only. It does not accept crosswalk mappings, allographs, phonetic values, sign meanings, or translations.',
};

fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
