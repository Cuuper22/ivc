// Builds an acquisition packet for one inscription: Lipi row 3335.1, text
// +740-205-032-002-390-590-032+. This row matters because, per the earlier
// source-upgrade impact audit, binding it to a real object would unlock the
// strict 032 matched-predecessor test in the 002-390 branch study. The problem
// is that the row has no CISI object id, no site, and no excavation number —
// it exists only in the quarantined local Lipi metadata. This script gathers
// everything known about it: the target row itself, its provenance trail
// through the crosswalk tables, every local row sharing its sign chunks (the
// M-143 prefix family, the portable 390-590-032 tail family), the tried public
// search queries (all negative), the concrete blockers, and the resulting
// decisions. It writes seven CSVs plus a summary JSON under
// data/open_prototype/reports/ so an external source hunt can pick up from
// here. Nothing in the packet is evidence; 3335.1 stays out of strict proofs.

import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const metadataPath = path.join(root, "data", "open_prototype", "lipi", "metadata_filtered.csv");
const artifactWitnessesPath = path.join(root, "data", "sign_crosswalk", "artifact_witnesses.csv");
const signSystemsPath = path.join(root, "data", "sign_crosswalk", "sign_systems.csv");
const evidenceRefsPath = path.join(root, "data", "sign_crosswalk", "evidence_refs.csv");
const reportsDir = path.join(root, "data", "open_prototype", "reports");
const impactPath = path.join(reportsDir, "campaign_032_002_861_002390x_source_upgrade_impact_audit_20260531_scenario_summary.csv");
const prefix = "campaign_032_002_861_002390x_3335_acquisition_packet_20260531";
const targetId = "3335.1";

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (ch === '"' && next === '"') {
        field += '"';
        i++;
      } else if (ch === '"') {
        quoted = false;
      } else {
        field += ch;
      }
    } else if (ch === '"') {
      quoted = true;
    } else if (ch === ",") {
      row.push(field);
      field = "";
    } else if (ch === "\n") {
      row.push(field.replace(/\r$/, ""));
      rows.push(row);
      row = [];
      field = "";
    } else {
      field += ch;
    }
  }
  if (field.length || row.length) {
    row.push(field.replace(/\r$/, ""));
    rows.push(row);
  }
  const [headers, ...body] = rows.filter((r) => r.some((v) => v !== ""));
  return body.map((r) => Object.fromEntries(headers.map((h, i) => [h, r[i] ?? ""])));
}

function readCsv(filePath) {
  return parseCsv(fs.readFileSync(filePath, "utf8"));
}

function csvEscape(value) {
  const s = String(value ?? "");
  return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

function writeCsv(filePath, rows, headers) {
  const lines = [headers.join(",")];
  for (const row of rows) lines.push(headers.map((h) => csvEscape(row[h])).join(","));
  fs.writeFileSync(filePath, `${lines.join("\n")}\n`);
}

function signs(text) {
  return [...String(text || "").matchAll(/\d{3}/g)].map((m) => m[0]);
}

function textKey(row) {
  return signs(row.text ?? row.text_raw).join("-");
}

function norm(value) {
  const s = String(value ?? "").trim();
  return !s || s === "-" || s === "--" ? "" : s;
}

function rowObject(row) {
  return norm(row.cisi) || `-:${row.id}`;
}

function containsChunk(row, chunk) {
  return `-${textKey(row)}-`.includes(`-${chunk}-`);
}

function startsWithChunk(row, chunk) {
  return textKey(row).startsWith(chunk);
}

function compact(row) {
  return {
    id: row.id,
    object: rowObject(row),
    region: row.region,
    site: row.site,
    type: row.type,
    symbol: row.symbol,
    cult: row.cult,
    material: row.material,
    shape: row.shape,
    excavation_idno: row["excavation-idno"],
    horizontal_mm: row["horizontal(mm)"],
    vertical_mm: row["vertical(mm)"],
    thickness_mm: row["thickness(mm)"],
    text: row.text,
  };
}

function distribution(rows, field) {
  const counts = new Map();
  for (const row of rows) counts.set(row[field], (counts.get(row[field]) ?? 0) + 1);
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([value, count]) => `${value || "<blank>"}:${count}`)
    .join("; ");
}

function rel(filePath) {
  return path.relative(root, filePath).replace(/\\/g, "/");
}

const rows = readCsv(metadataPath);
const artifactRows = readCsv(artifactWitnessesPath);
const signSystems = readCsv(signSystemsPath);
const evidenceRefs = readCsv(evidenceRefsPath);
const impactRows = readCsv(impactPath);

const target = rows.find((row) => row.id === targetId);
if (!target) throw new Error(`Missing target row ${targetId}`);

const targetWitness = artifactRows.find((row) => row.witness_id === `lipi:${targetId}`) ?? {};
const lipiSystem = signSystems.find((row) => row.system_id === "lipi_numeric") ?? {};
const lipiRef = evidenceRefs.find((row) => row.ref_id === "ref_lipi_metadata_filtered") ?? {};
const impact3335 = impactRows.find((row) => row.scenario === "upgrade_3335_1") ?? {};

const targetSigns = textKey(target);
const targetRows = [
  {
    id: target.id,
    object: rowObject(target),
    cisi: target.cisi,
    region: target.region,
    site: target.site,
    type: target.type,
    symbol: target.symbol,
    cult: target.cult,
    material: target.material,
    shape: target.shape,
    excavation_idno: target["excavation-idno"],
    dimensions: `${target["horizontal(mm)"]} x ${target["vertical(mm)"]} x ${target["thickness(mm)"]}`,
    direction: target["dir."],
    text: target.text,
    signs: targetSigns,
    structural_role: "032 -> 002-390 -> 590 -> 032",
    strict_gate_if_bound: impact3335.unlocks ?? "",
  },
];

const provenanceRows = [
  {
    source_layer: "metadata_filtered",
    evidence_path: rel(metadataPath),
    claim: "local Lipi metadata row exists with no CISI object id",
    observed_value: `${target.id}; cisi=${target.cisi}; site=${target.site}; excavation=${target["excavation-idno"]}`,
    consequence: "usable as local pressure only",
  },
  {
    source_layer: "artifact_witnesses",
    evidence_path: rel(artifactWitnessesPath),
    claim: "crosswalk marks target as lipi_numeric quarantined metadata",
    observed_value: `artifact_id=${targetWitness.artifact_id ?? ""}; side_label_type=${targetWitness.side_label_type ?? ""}; provenance_tier=${targetWitness.provenance_tier ?? ""}; image_ref_id=${targetWitness.image_ref_id ?? ""}`,
    consequence: "no image or source witness is attached in the crosswalk",
  },
  {
    source_layer: "sign_systems",
    evidence_path: rel(signSystemsPath),
    claim: "lipi_numeric source layer is local T3 quarantined",
    observed_value: `${lipiSystem.name ?? ""}; ${lipiSystem.provenance_note ?? lipiSystem.provenance_tier ?? ""}`,
    consequence: "must not become strict evidence without independent source binding",
  },
  {
    source_layer: "evidence_refs",
    evidence_path: rel(evidenceRefsPath),
    claim: "metadata source reference is local/quarantined",
    observed_value: `${lipiRef.ref_type ?? ""}; ${lipiRef.description ?? ""}; hash=${lipiRef.sha256 ?? ""}`,
    consequence: "external acquisition must bridge to a publication, archive, museum, or authoritative sign list",
  },
];

const chunkSpecs = [
  { chunk: "740-205-032-002-390-590-032", role: "exact target sequence" },
  { chunk: "740-205-032-002", role: "target left prefix before branch" },
  { chunk: "205-032-002", role: "shorter left prefix before branch" },
  { chunk: "032-002-390", role: "matched 032 branch lane" },
  { chunk: "002-390-590", role: "target branch plus first tail" },
  { chunk: "390-590-032", role: "portable formula-family chunk" },
  { chunk: "740-205", role: "weak prefix family" },
];

const chunkRows = [];
for (const spec of chunkSpecs) {
  const matches = rows
    .filter((row) => containsChunk(row, spec.chunk))
    .map((row) => ({
      chunk: spec.chunk,
      role: spec.role,
      match_type: textKey(row) === spec.chunk ? "exact_text" : startsWithChunk(row, spec.chunk) ? "prefix" : "contains",
      has_object_id: norm(row.cisi) ? "yes" : "no",
      ...compact(row),
    }));
  chunkRows.push(...matches);
}

const prefix740205Rows = chunkRows.filter((row) => row.chunk === "740-205-032-002");
const targetOnlyChunks = chunkRows.filter((row) => row.chunk === "002-390-590");
const chunk390590032Rows = chunkRows.filter((row) => row.chunk === "390-590-032");

const routeRows = [
  {
    route: "exact_public_string_search",
    target: target.text,
    current_evidence: "2026-05-31 public exact/near-exact searches returned no usable object, source plate, museum, or Harappa/Archive bridge",
    acquisition_value: "would bind target directly if found",
    status: "negative_public_refresh",
    next_action: "repeat only with new source corpora, OCR dumps, or library databases",
  },
  {
    route: "lipi_source_origin",
    target: "source behind cisi-less Lipi row 3335.1",
    current_evidence: "artifact_witnesses keeps lipi:3335.1 as T3_quarantined_metadata with no image_ref_id",
    acquisition_value: "would identify original publication/sign-list row and possibly object id",
    status: "best_non_public_source_route",
    next_action: "trace Yajnadevam/Lipi export provenance or source table for row 3335.1",
  },
  {
    route: "m143_prefix_family_control",
    target: "M-143 +740-205-032-002-252-840+",
    current_evidence: `${prefix740205Rows.length} rows contain 740-205-032-002; known object M-143 is the source-family control, target 3335.1 is the blocked branch`,
    acquisition_value: "tests whether 3335.1 belongs to a source family around prefix 740-205-032-002",
    status: "control_not_binding",
    next_action: "source-bind M-143 if needed for formula-family context, but do not use it as 3335.1 identity",
  },
  {
    route: "m70_matched_lane_pair",
    target: "M-70 +226-032-002-390-692+ versus 3335.1 +740-205-032-002-390-590-032+",
    current_evidence: "M-70 is strict source-visible; 3335.1 is object/source blocked",
    acquisition_value: "would unlock strict 032 matched-predecessor split if 3335.1 becomes source-bound and sequence-valid",
    status: "highest_single_object_matched_gate",
    next_action: "seek direct source bridge for 3335.1 or replacement strict 032 -> 002-390 -> non-692/non-125 row",
  },
  {
    route: "390590032_family_collapse",
    target: "seven local rows with 390-590-032",
    current_evidence: `${chunk390590032Rows.length} rows contain 390-590-032; known source-visible non-frame rows include M-746 and M-965 from prior gate`,
    acquisition_value: "needed after binding because target tail may be portable formula material",
    status: "adversarial_control_required",
    next_action: "if 3335.1 is acquired, compare source-bound target against source-bound family controls before grammar promotion",
  },
];

const searchRows = [
  { query: "\"+740-205-032-002-390-590-032+\"", target: "exact signed string", result: "no usable public bridge" },
  { query: "\"740-205-032-002-390-590-032\" \"Indus\"", target: "exact unsigned string", result: "no usable public bridge" },
  { query: "\"3335.1\" \"740-205\"", target: "row id plus prefix", result: "no usable public bridge" },
  { query: "site:harappa.com \"740-205-032-002-390-590-032\"", target: "Harappa exact", result: "no usable public bridge" },
  { query: "site:archive.org \"740-205-032-002-390-590-032\"", target: "Archive exact", result: "no usable public bridge" },
  { query: "\"390-590-032\" \"Indus\"", target: "family chunk", result: "noise or no usable bridge" },
  { query: "\"740-205-032-002\" \"Indus\"", target: "M-143/3335 prefix", result: "no usable public bridge" },
  { query: "\"Bull1:J\" \"RAF\" \"Indus\"", target: "metadata profile", result: "no usable public bridge" },
];

const blockers = [
  {
    blocker: "no_cisi_object_id",
    evidence: `target cisi=${target.cisi}; artifact_id=${targetWitness.artifact_id ?? ""}`,
    consequence: "cannot route to CISI plate/page by object id",
  },
  {
    blocker: "no_site_or_excavation_id",
    evidence: `site=${target.site}; excavation=${target["excavation-idno"]}`,
    consequence: "cannot route through field catalogue without source provenance",
  },
  {
    blocker: "local_layer_quarantined",
    evidence: `provenance=${targetWitness.provenance_tier ?? ""}`,
    consequence: "numeric sequence remains local metadata pressure only",
  },
  {
    blocker: "prefix_family_control_not_identity",
    evidence: "M-143 shares 740-205-032-002 but diverges to 252-840",
    consequence: "prefix family is a control, not a bridge",
  },
  {
    blocker: "portable_tail_family",
    evidence: `${chunk390590032Rows.length} rows contain 390-590-032`,
    consequence: "even a source-bound target must survive formula-family collapse",
  },
];

const decisions = [
  {
    decision: "3335_packet_ready_external_source_required",
    evidence: "target has no CISI/site/excavation/image bridge and public exact searches are negative",
    result: "packeted acquisition target, not source-bound evidence",
    consequence: "do not count 3335.1 in strict matched-lane proof",
  },
  {
    decision: "m143_is_prefix_control_not_identity",
    evidence: "M-143 shares 740-205-032-002 but has branch/tail 252-840 instead of 390-590-032",
    result: "adds source-family context, not object binding",
    consequence: "use M-143 only as a formula/source-family control",
  },
  {
    decision: "highest_single_object_unlock_still_blocked",
    evidence: impact3335.unlocks ?? "",
    result: "3335.1 would unlock strict 032 only if source-bound and sequence-valid",
    consequence: "external acquisition remains the priority over further local triangulation",
  },
];

writeCsv(
  path.join(reportsDir, `${prefix}_target.csv`),
  targetRows,
  ["id", "object", "cisi", "region", "site", "type", "symbol", "cult", "material", "shape", "excavation_idno", "dimensions", "direction", "text", "signs", "structural_role", "strict_gate_if_bound"],
);

writeCsv(
  path.join(reportsDir, `${prefix}_provenance.csv`),
  provenanceRows,
  ["source_layer", "evidence_path", "claim", "observed_value", "consequence"],
);

writeCsv(
  path.join(reportsDir, `${prefix}_chunk_leads.csv`),
  chunkRows,
  ["chunk", "role", "match_type", "has_object_id", "id", "object", "region", "site", "type", "symbol", "cult", "material", "shape", "excavation_idno", "horizontal_mm", "vertical_mm", "thickness_mm", "text"],
);

writeCsv(
  path.join(reportsDir, `${prefix}_routes.csv`),
  routeRows,
  ["route", "target", "current_evidence", "acquisition_value", "status", "next_action"],
);

writeCsv(
  path.join(reportsDir, `${prefix}_search_queries.csv`),
  searchRows,
  ["query", "target", "result"],
);

writeCsv(
  path.join(reportsDir, `${prefix}_blockers.csv`),
  blockers,
  ["blocker", "evidence", "consequence"],
);

writeCsv(
  path.join(reportsDir, `${prefix}_decisions.csv`),
  decisions,
  ["decision", "evidence", "result", "consequence"],
);

const summary = {
  run_date: "2026-05-31",
  inputs: {
    metadata: rel(metadataPath),
    artifact_witnesses: rel(artifactWitnessesPath),
    sign_systems: rel(signSystemsPath),
    evidence_refs: rel(evidenceRefsPath),
    source_upgrade_impact: rel(impactPath),
  },
  target: targetRows[0],
  chunk_counts: Object.fromEntries(chunkSpecs.map((spec) => [spec.chunk, chunkRows.filter((row) => row.chunk === spec.chunk).length])),
  m143_prefix_control_rows: prefix740205Rows.length,
  target_only_002390590_rows: targetOnlyChunks.length,
  family_390590032_rows: chunk390590032Rows.length,
  profile_distribution: {
    rows_with_same_symbol_cult_shape_type: rows.filter(
      (row) =>
        row.id !== target.id &&
        norm(row.type) === norm(target.type) &&
        norm(row.symbol) === norm(target.symbol) &&
        norm(row.cult) === norm(target.cult) &&
        norm(row.shape) === norm(target.shape),
    ).length,
    target_profile_sites: distribution(rows.filter((row) => norm(row.cult) === norm(target.cult)), "site"),
  },
  decisions,
  status: "3335_acquisition_packet_ready_external_source_or_replacement_required_no_values",
  outputs: {
    target: `data/open_prototype/reports/${prefix}_target.csv`,
    provenance: `data/open_prototype/reports/${prefix}_provenance.csv`,
    chunk_leads: `data/open_prototype/reports/${prefix}_chunk_leads.csv`,
    routes: `data/open_prototype/reports/${prefix}_routes.csv`,
    search_queries: `data/open_prototype/reports/${prefix}_search_queries.csv`,
    blockers: `data/open_prototype/reports/${prefix}_blockers.csv`,
    decisions: `data/open_prototype/reports/${prefix}_decisions.csv`,
    summary: `data/open_prototype/reports/${prefix}_summary.json`,
  },
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
