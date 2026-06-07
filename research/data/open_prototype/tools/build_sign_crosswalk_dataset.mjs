import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const REPORTS = path.join(ROOT, 'data', 'open_prototype', 'reports');
const MAYIG = path.join(ROOT, 'data', 'open_prototype', 'mayig');
const LIPI = path.join(ROOT, 'data', 'open_prototype', 'lipi');
const OUT = path.join(ROOT, 'data', 'sign_crosswalk');
const FEATURE_ROOT = path.join(
  ROOT,
  'tmp',
  'mayig_feature_namespace_probe',
  'repo',
  'indus-valley-script-corpus-ad2f1e218a34b8c33c57de0d6cb8d99272765bbb',
  'features',
);

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
  for (const row of rows) lines.push(fields.map((f) => csvEscape(row[f])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function sha256(file) {
  if (!fs.existsSync(file)) return '';
  return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
}

function rel(file) {
  return path.relative(ROOT, file).replaceAll(path.sep, '/');
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function uniqueId(prefix, raw) {
  return `${prefix}:${raw}`;
}

function maybeFeature(sign) {
  const file = path.join(FEATURE_ROOT, `${sign}.json`);
  if (!fs.existsSync(file)) return null;
  return readJson(file);
}

function textTokens(text) {
  const match = String(text || '').match(/\+?([0-9\]-][0-9\]\[-]*)\+?/g);
  if (!match) return [];
  return String(text || '')
    .replaceAll('+', '')
    .replaceAll('[', '')
    .replaceAll(']', '')
    .split('-')
    .map((x) => x.trim())
    .filter((x) => /^\d{3}$/.test(x));
}

function main() {
  ensureDir(OUT);

  const l2mPath = path.join(REPORTS, 'crosswalk_lipi_to_mayig_candidates.csv');
  const m2lPath = path.join(REPORTS, 'crosswalk_mayig_to_lipi_candidates.csv');
  const alignPath = path.join(REPORTS, 'crosswalk_alignment_pairs.csv');
  const recordsPath = path.join(MAYIG, 'records_index.csv');
  const lipiPath = path.join(LIPI, 'metadata_filtered.csv');
  const commitPath = path.join(MAYIG, 'commit.json');
  const summaryPath = path.join(REPORTS, 'crosswalk_summary.json');

  const commit = readJson(commitPath);
  const l2m = parseCsv(fs.readFileSync(l2mPath, 'utf8'));
  const m2l = parseCsv(fs.readFileSync(m2lPath, 'utf8'));
  const align = parseCsv(fs.readFileSync(alignPath, 'utf8'));
  const mayigRecords = parseCsv(fs.readFileSync(recordsPath, 'utf8'));
  const lipiRows = parseCsv(fs.readFileSync(lipiPath, 'utf8'));
  const summary = readJson(summaryPath);

  const evidenceRefs = [
    {
      ref_id: 'ref_crosswalk_alignment_pairs',
      ref_type: 'local_report_csv',
      citation: 'Local provisional Lipi-Mayig position alignment pairs',
      url: '',
      local_path: rel(alignPath),
      page: '',
      figure: '',
      crop_path: '',
      sha256: sha256(alignPath),
      checked_date: '2026-05-29',
      access_status: 'local',
    },
    {
      ref_id: 'ref_crosswalk_lipi_to_mayig_candidates',
      ref_type: 'local_report_csv',
      citation: 'Local provisional Lipi to Mayig crosswalk candidate table',
      url: '',
      local_path: rel(l2mPath),
      page: '',
      figure: '',
      crop_path: '',
      sha256: sha256(l2mPath),
      checked_date: '2026-05-29',
      access_status: 'local',
    },
    {
      ref_id: 'ref_crosswalk_mayig_to_lipi_candidates',
      ref_type: 'local_report_csv',
      citation: 'Local provisional Mayig to Lipi crosswalk candidate table',
      url: '',
      local_path: rel(m2lPath),
      page: '',
      figure: '',
      crop_path: '',
      sha256: sha256(m2lPath),
      checked_date: '2026-05-29',
      access_status: 'local',
    },
    {
      ref_id: 'ref_mayig_commit',
      ref_type: 'git_commit',
      citation: 'mayig/indus-valley-script-corpus pinned open prototype commit',
      url: `${commit.repository}/tree/${commit.commit}`,
      local_path: rel(commitPath),
      page: '',
      figure: '',
      crop_path: '',
      sha256: sha256(commitPath),
      checked_date: '2026-05-29',
      access_status: 'public_git_metadata',
    },
    {
      ref_id: 'ref_lipi_metadata_filtered',
      ref_type: 'local_quarantined_csv',
      citation: 'Filtered Lipi metadata/sign layer with claim columns removed or quarantined',
      url: '',
      local_path: rel(lipiPath),
      page: '',
      figure: '',
      crop_path: '',
      sha256: sha256(lipiPath),
      checked_date: '2026-05-29',
      access_status: 'local_t3_quarantined',
    },
  ];

  const signSystems = [
    {
      system_id: 'lipi_numeric',
      authority: 'Yajnadevam Lipi filtered local numeric notation',
      namespace_prefix: 'numeric',
      source_version: 'local 2026-05-24 filtered export',
      source_url: '',
      local_path: rel(lipiPath),
      sha256: sha256(lipiPath),
      access_status: 'local_t3_quarantined',
      notes: 'Use metadata/sign columns only; translation and Sanskrit columns are quarantined.',
    },
    {
      system_id: 'mayig_p',
      authority: 'mayig/indus-valley-script-corpus Parpola-style P namespace',
      namespace_prefix: 'P',
      source_version: commit.commit,
      source_url: `${commit.repository}/tree/${commit.commit}`,
      local_path: rel(recordsPath),
      sha256: sha256(recordsPath),
      access_status: 'public_git_pinned_metadata',
      notes: 'Open WIP CISI digitization; useful for prototype crosswalk only.',
    },
    {
      system_id: 'mayig_parpola_v',
      authority: 'Parpola V IDs as mediated through Mayig feature metadata',
      namespace_prefix: 'V',
      source_version: commit.commit,
      source_url: `${commit.repository}/tree/${commit.commit}`,
      local_path: rel(FEATURE_ROOT),
      sha256: '',
      access_status: 'mediated_not_primary_sign_list',
      notes: 'Do not confuse V### with Parpola article ordinal sign numbers.',
    },
    {
      system_id: 'mayig_wells_w',
      authority: 'Wells W IDs as mediated through Mayig feature metadata',
      namespace_prefix: 'W',
      source_version: commit.commit,
      source_url: `${commit.repository}/tree/${commit.commit}`,
      local_path: rel(FEATURE_ROOT),
      sha256: '',
      access_status: 'mediated_not_icit',
      notes: 'ICIT/Wells primary tables are not locally acquired.',
    },
    {
      system_id: 'mayig_mahadevan_m',
      authority: 'Mahadevan M IDs as mediated through Mayig feature metadata',
      namespace_prefix: 'M',
      source_version: commit.commit,
      source_url: `${commit.repository}/tree/${commit.commit}`,
      local_path: rel(FEATURE_ROOT),
      sha256: '',
      access_status: 'mediated_not_m77_primary',
      notes: 'Mahadevan/M77 machine-readable primary sign table is not locally acquired.',
    },
  ];

  const signs = new Map();
  function addSign(system_id, raw_id, attrs = {}) {
    const sign_uid = uniqueId(system_id, raw_id);
    if (!signs.has(sign_uid)) {
      signs.set(sign_uid, {
        sign_uid,
        system_id,
        raw_id,
        normalized_id: raw_id,
        description: attrs.description || '',
        feature_json: attrs.feature_json || '',
        visual_ref_id: attrs.visual_ref_id || '',
        status: attrs.status || 'unaccepted',
      });
    }
  }

  for (const row of l2m) addSign('lipi_numeric', row.source_a_sign);
  for (const row of m2l) addSign('lipi_numeric', row.top_source_b_sign);
  for (const row of lipiRows) for (const token of textTokens(row.text)) addSign('lipi_numeric', token);

  const mayigSignsSeen = new Set();
  for (const row of mayigRecords) for (const p of row.graphemes.split(/\s+/).filter(Boolean)) mayigSignsSeen.add(p);
  for (const row of l2m) mayigSignsSeen.add(row.top_source_b_sign);
  for (const row of m2l) mayigSignsSeen.add(row.source_a_sign);

  for (const p of [...mayigSignsSeen].sort()) {
    const feature = maybeFeature(p);
    addSign('mayig_p', p, {
      description: feature?.description || '',
      feature_json: feature ? JSON.stringify(feature.features || []) : '',
      status: feature ? 'feature_metadata_available' : 'feature_metadata_missing',
    });
    for (const v of feature?.parpola_graphemes || []) addSign('mayig_parpola_v', v, { status: 'mediated_by_mayig_feature_metadata' });
    for (const w of feature?.wells_graphemes || []) addSign('mayig_wells_w', w, { status: 'mediated_by_mayig_feature_metadata' });
    for (const m of feature?.mahadevan_graphemes || []) addSign('mayig_mahadevan_m', m, { status: 'mediated_by_mayig_feature_metadata' });
  }

  const crosswalkEdges = [];
  let edgeCounter = 1;
  function addEdge(fromSystem, fromRaw, toSystem, toRaw, attrs) {
    crosswalkEdges.push({
      edge_id: `edge_${String(edgeCounter).padStart(5, '0')}`,
      from_sign_uid: uniqueId(fromSystem, fromRaw),
      to_sign_uid: uniqueId(toSystem, toRaw),
      mapping_state: attrs.mapping_state || 'uncertain',
      evidence_types: attrs.evidence_types || '',
      support_count: attrs.support_count || '',
      counterexample_count: attrs.counterexample_count || '',
      aligned_positions: attrs.aligned_positions || '',
      top_share: attrs.top_share || '',
      example_witnesses: attrs.example_witnesses || '',
      counterexample_witnesses: attrs.counterexample_witnesses || '',
      confidence: attrs.confidence || '',
      review_status: attrs.review_status || '',
      accepted_for_analysis: attrs.accepted_for_analysis || 'false',
    });
    edgeCounter += 1;
  }

  for (const row of l2m) {
    addEdge('lipi_numeric', row.source_a_sign, 'mayig_p', row.top_source_b_sign, {
      mapping_state: row.mapping_state || 'uncertain',
      evidence_types: row.evidence_types,
      support_count: row.top_count,
      counterexample_count: row.counterexamples ? row.counterexamples.split(';').filter(Boolean).length : '0',
      aligned_positions: row.total_aligned_positions,
      top_share: row.top_share,
      example_witnesses: row.example_artifacts,
      counterexample_witnesses: row.counterexamples,
      confidence: row.confidence,
      review_status: row.review_status,
      accepted_for_analysis: 'false',
    });
  }
  for (const p of [...mayigSignsSeen].sort()) {
    const feature = maybeFeature(p);
    if (!feature) continue;
    for (const v of feature.parpola_graphemes || []) {
      addEdge('mayig_p', p, 'mayig_parpola_v', v, {
        mapping_state: 'uncertain',
        evidence_types: 'mayig_feature_metadata',
        support_count: '1',
        counterexample_count: 'unknown',
        aligned_positions: '',
        top_share: '',
        example_witnesses: '',
        counterexample_witnesses: '',
        confidence: 'source_metadata_only',
        review_status: 'needs_primary_sign_list_validation',
        accepted_for_analysis: 'false',
      });
    }
    for (const w of feature.wells_graphemes || []) {
      addEdge('mayig_p', p, 'mayig_wells_w', w, {
        mapping_state: 'uncertain',
        evidence_types: 'mayig_feature_metadata',
        support_count: '1',
        counterexample_count: 'unknown',
        aligned_positions: '',
        top_share: '',
        example_witnesses: '',
        counterexample_witnesses: '',
        confidence: 'source_metadata_only',
        review_status: 'needs_icit_wells_validation',
        accepted_for_analysis: 'false',
      });
    }
    for (const m of feature.mahadevan_graphemes || []) {
      addEdge('mayig_p', p, 'mayig_mahadevan_m', m, {
        mapping_state: 'uncertain',
        evidence_types: 'mayig_feature_metadata',
        support_count: '1',
        counterexample_count: 'unknown',
        aligned_positions: '',
        top_share: '',
        example_witnesses: '',
        counterexample_witnesses: '',
        confidence: 'source_metadata_only',
        review_status: 'needs_m77_validation',
        accepted_for_analysis: 'false',
      });
    }
  }

  const artifactWitnesses = [];
  for (const row of mayigRecords) {
    artifactWitnesses.push({
      witness_id: `mayig:${row.side_id}`,
      artifact_id: row.artifact_base,
      system_id: 'mayig_p',
      row_id: row.source_path,
      side_id: row.side_id,
      side_label_type: 'source_side_id',
      text_raw: row.graphemes,
      sign_sequence: row.graphemes,
      direction: 'as_encoded',
      direction_source: 'mayig_record_order',
      image_ref_id: '',
      provenance_tier: 'T2_open_wip',
    });
  }
  for (const row of lipiRows) {
    artifactWitnesses.push({
      witness_id: `lipi:${row.id}`,
      artifact_id: row.cisi || row.id,
      system_id: 'lipi_numeric',
      row_id: row.id,
      side_id: row.id,
      side_label_type: 'analytic_row_id',
      text_raw: row.text,
      sign_sequence: textTokens(row.text).join(' '),
      direction: row['dir.'],
      direction_source: 'lipi_filtered_metadata',
      image_ref_id: '',
      provenance_tier: 'T3_quarantined_metadata',
    });
  }

  const namespaceGates = [
    {
      gate_id: 'gate_p041_not_parpola_sign_41',
      assertion: 'Mayig P041, Mayig V041, Lipi 041, Wells W041, Mahadevan M041, and Parpola 2019 sign no. 41 are interchangeable.',
      status: 'blocked',
      decision: 'Rejected as a namespace shortcut. Mayig P041 maps to V141/W112/M034; Parpola 2019 sign no. 41 uses Parpola 1994 Fig. 5.1 sign no. 41.',
      blocked_claims: 'local 110 = Parpola sign no. 41; P041 = Parpola sign no. 41',
      required_next_evidence: 'Same-side source identity or primary sign-list cross-reference.',
      evidence_refs: 'docs/p041_mayig_parpola41_crosswalk_falsification_gate.md;docs/parpola1994_sign41_convention_gate.md',
    },
    {
      gate_id: 'gate_text7_numeric_shortcuts_blocked',
      assertion: 'Parpola article signs 60, 107, and 189 can be mapped by matching numeric IDs V060/V107/V189, M060/M107/M189, or local numeric signs.',
      status: 'blocked',
      decision: 'Rejected as numeric shortcut. Article signs are visually anchored in Parpola 1994 Fig. 5.1 but Mayig/local numeric namespaces do not align directly.',
      blocked_claims: 'local 220 = article sign 60; local 107 = article sign 107; local 415/861 = article sign 189',
      required_next_evidence: 'Source-image or primary sign-list bridge for each proposed edge.',
      evidence_refs: 'docs/parpola_text7_feature_namespace_bridge_gate.md',
    },
    {
      gate_id: 'gate_p385_lipi_817_861_merge_pressure',
      assertion: 'Lipi 817 and Lipi 861 are the same sign because both align to Mayig P385.',
      status: 'open_pressure_not_accepted',
      decision: 'Possible merge/allograph cluster only; positional alignment cannot decide whether 817/861 are identical, allographs, or source-policy collapse.',
      blocked_claims: '817 = 861; 817/861 phonetic or semantic value',
      required_next_evidence: 'Image-level allograph adjudication across source-visible rows and policy sensitivity.',
      evidence_refs: 'data/open_prototype/reports/crosswalk_collision_summary.csv;docs/sign_crosswalk_protocol.md',
    },
    {
      gate_id: 'gate_lipi_034_absence_not_falsification',
      assertion: 'Lipi 034 has no Mayig crosswalk because it is false or nonexistent.',
      status: 'blocked',
      decision: 'Rejected. Current strict overlap has zero exact 034 rows, so the crosswalk is absent by sampling, not falsification.',
      blocked_claims: '034 unmapped means invalid sign; 034 value claims',
      required_next_evidence: 'Acquire/align rows that actually contain 034 in both sign systems or source images.',
      evidence_refs: 'docs/lipi_034_crosswalk_darkness_diagnostic.md',
    },
  ];

  const reviewEvents = [
    {
      review_id: 'review_2026_05_29_crosswalk_scaffold',
      edge_id_or_gate_id: 'dataset',
      reviewer: 'codex',
      check_type: 'normalization_build',
      result: 'created_unaccepted_scaffold',
      notes: 'All Lipi-Mayig candidate edges default to accepted_for_analysis=false; this is reusable infrastructure, not an accepted sign-list.',
      checked_date: '2026-05-29',
    },
  ];

  const files = {
    sign_systems: path.join(OUT, 'sign_systems.csv'),
    signs: path.join(OUT, 'signs.csv'),
    artifact_witnesses: path.join(OUT, 'artifact_witnesses.csv'),
    crosswalk_edges: path.join(OUT, 'crosswalk_edges.csv'),
    evidence_refs: path.join(OUT, 'evidence_refs.csv'),
    namespace_gates: path.join(OUT, 'namespace_gates.csv'),
    review_events: path.join(OUT, 'review_events.csv'),
    manifest: path.join(OUT, 'manifest.json'),
  };

  writeCsv(files.sign_systems, signSystems, [
    'system_id',
    'authority',
    'namespace_prefix',
    'source_version',
    'source_url',
    'local_path',
    'sha256',
    'access_status',
    'notes',
  ]);
  writeCsv(files.signs, [...signs.values()].sort((a, b) => a.sign_uid.localeCompare(b.sign_uid)), [
    'sign_uid',
    'system_id',
    'raw_id',
    'normalized_id',
    'description',
    'feature_json',
    'visual_ref_id',
    'status',
  ]);
  writeCsv(files.artifact_witnesses, artifactWitnesses, [
    'witness_id',
    'artifact_id',
    'system_id',
    'row_id',
    'side_id',
    'side_label_type',
    'text_raw',
    'sign_sequence',
    'direction',
    'direction_source',
    'image_ref_id',
    'provenance_tier',
  ]);
  writeCsv(files.crosswalk_edges, crosswalkEdges, [
    'edge_id',
    'from_sign_uid',
    'to_sign_uid',
    'mapping_state',
    'evidence_types',
    'support_count',
    'counterexample_count',
    'aligned_positions',
    'top_share',
    'example_witnesses',
    'counterexample_witnesses',
    'confidence',
    'review_status',
    'accepted_for_analysis',
  ]);
  writeCsv(files.evidence_refs, evidenceRefs, [
    'ref_id',
    'ref_type',
    'citation',
    'url',
    'local_path',
    'page',
    'figure',
    'crop_path',
    'sha256',
    'checked_date',
    'access_status',
  ]);
  writeCsv(files.namespace_gates, namespaceGates, [
    'gate_id',
    'assertion',
    'status',
    'decision',
    'blocked_claims',
    'required_next_evidence',
    'evidence_refs',
  ]);
  writeCsv(files.review_events, reviewEvents, [
    'review_id',
    'edge_id_or_gate_id',
    'reviewer',
    'check_type',
    'result',
    'notes',
    'checked_date',
  ]);

  const manifest = {
    date: '2026-05-29',
    status: 'provenance_tagged_scaffold_no_accepted_crosswalk_edges',
    source_summary: {
      lipi_rows: lipiRows.length,
      mayig_witness_rows: mayigRecords.length,
      positional_alignment_rows: align.length,
      lipi_to_mayig_candidate_edges: l2m.length,
      mayig_feature_root_present: fs.existsSync(FEATURE_ROOT),
      crosswalk_summary: {
        aligned_positions: summary.aligned_positions,
        unique_lipi_signs: summary.unique_lipi_signs,
        unique_mayig_signs: summary.unique_mayig_signs,
      },
    },
    output_counts: {
      sign_systems: signSystems.length,
      signs: signs.size,
      artifact_witnesses: artifactWitnesses.length,
      crosswalk_edges: crosswalkEdges.length,
      evidence_refs: evidenceRefs.length,
      namespace_gates: namespaceGates.length,
      review_events: reviewEvents.length,
      accepted_crosswalk_edges: 0,
    },
    files: Object.fromEntries(Object.entries(files).map(([k, v]) => [k, rel(v)])),
    caveats: [
      'Lipi numeric data remains T3/quarantined; use metadata/sign fields only.',
      'Mayig V/W/M links are mediated through Mayig feature metadata, not primary Parpola/Wells/Mahadevan tables.',
      'All crosswalk edges are unaccepted until source-image or authoritative sign-list validation clears the relevant namespace gate.',
    ],
  };
  fs.writeFileSync(files.manifest, `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
  console.log(JSON.stringify(manifest, null, 2));
}

main();
