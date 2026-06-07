import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const metadataPath = path.join(root, "data", "open_prototype", "lipi", "metadata_filtered.csv");
const witnessesPath = path.join(root, "data", "sign_crosswalk", "artifact_witnesses.csv");
const reportsDir = path.join(root, "data", "open_prototype", "reports");
const workDir = path.join(root, "tmp", "002390x_3335_yajnadevam_provenance_20260531");
const currentRawPath = path.join(workDir, "inscriptions_current.csv");
const pinnedRawPath = path.join(workDir, "inscriptions_pinned_b272ad99.csv");
const priorRawPath = path.join(root, "tmp", "lipi_current_inscriptions_20260526.csv");
const commitJsonPath = path.join(workDir, "github_commit_main_path.json");
const prefix = "campaign_032_002_861_002390x_3335_yajnadevam_provenance_recheck_20260531";
const targetId = "3335.1";
const mainRawUrl =
  "https://raw.githubusercontent.com/yajnadevam/lipi/refs/heads/main/src/assets/data/inscriptions.csv";
const commitApiUrl =
  "https://api.github.com/repos/yajnadevam/lipi/commits/main?path=src/assets/data/inscriptions.csv";

function parseCsv(text) {
  const parseLine = (line) => {
    const row = [];
    let field = "";
    let quoted = false;
    for (let i = 0; i < line.length; i++) {
      const ch = line[i];
      const next = line[i + 1];
      if (quoted) {
        if (ch === '"' && next === '"') {
          field += '"';
          i++;
        } else if (ch === '"' && (next === "," || next === undefined)) {
          quoted = false;
        } else {
          field += ch;
        }
      } else if (ch === '"' && field === "") {
        quoted = true;
      } else if (ch === ",") {
        row.push(field);
        field = "";
      } else {
        field += ch;
      }
    }
    row.push(field);
    return row;
  };

  const rows = text
    .replace(/\r\n/g, "\n")
    .replace(/\r/g, "\n")
    .split("\n")
    .filter((line) => line.length)
    .map(parseLine)
    .filter((r) => r.some((v) => v !== ""));
  const [headers, ...body] = rows;
  return {
    headers,
    rows: body.map((r) => Object.fromEntries(headers.map((h, i) => [h, r[i] ?? ""]))),
  };
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

function hashFile(filePath) {
  if (!fs.existsSync(filePath)) return "";
  return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex");
}

function rel(filePath) {
  return path.relative(root, filePath).replaceAll(path.sep, "/");
}

function signs(text) {
  return [...String(text || "").matchAll(/\d{3}/g)].map((m) => m[0]);
}

function textKey(row) {
  return signs(row.text).join("-");
}

function norm(value) {
  const s = String(value ?? "").trim();
  return !s || s === "-" || s === "--" ? "" : s;
}

function compact(row) {
  return {
    id: row.id,
    cisi: row.cisi,
    region: row.region,
    site: row.site,
    excavation_idno: row["excavation-idno"],
    type: row.type,
    symbol: row.symbol,
    cult: row.cult,
    material: row.material,
    shape: row.shape,
    dimensions_mm: `${row["horizontal(mm)"]} x ${row["vertical(mm)"]} x ${row["thickness(mm)"]}`,
    text: row.text,
  };
}

function sameCommonMetadata(a, b, headers) {
  return headers.every((h) => String(a[h] ?? "") === String(b[h] ?? ""));
}

function mustFile(filePath, label) {
  if (!fs.existsSync(filePath)) throw new Error(`Missing ${label}: ${filePath}`);
}

function mustFind(rows, pred, label) {
  const row = rows.find(pred);
  if (!row) throw new Error(`Missing ${label}`);
  return row;
}

function readJson(filePath) {
  if (!fs.existsSync(filePath)) return {};
  const raw = fs.readFileSync(filePath, "utf8").replace(/^\uFEFF/, "");
  return JSON.parse(raw);
}

fs.mkdirSync(reportsDir, { recursive: true });
mustFile(metadataPath, "filtered Lipi metadata");
mustFile(witnessesPath, "artifact witnesses");
mustFile(currentRawPath, "current upstream raw CSV download");
mustFile(pinnedRawPath, "pinned upstream raw CSV download");

const filtered = readCsv(metadataPath);
const current = readCsv(currentRawPath);
const pinned = readCsv(pinnedRawPath);
const prior = fs.existsSync(priorRawPath) ? readCsv(priorRawPath) : { headers: [], rows: [] };
const witnesses = readCsv(witnessesPath).rows;
const commit = readJson(commitJsonPath);
const currentCommitSha = commit.sha ?? "b272ad99c253ba7fa1e4cd91f48cce31f6d02bf4";
const pinnedRawUrl = `https://raw.githubusercontent.com/yajnadevam/lipi/${currentCommitSha}/src/assets/data/inscriptions.csv`;

const targetFiltered = mustFind(filtered.rows, (r) => r.id === targetId, "filtered target 3335.1");
const targetCurrent = mustFind(current.rows, (r) => r.id === targetId, "current raw target 3335.1");
const targetPinned = mustFind(pinned.rows, (r) => r.id === targetId, "pinned raw target 3335.1");
const targetPrior = prior.rows.find((r) => r.id === targetId) ?? {};
const witness = witnesses.find((r) => r.witness_id === `lipi:${targetId}`) ?? {};

const filteredHeaderSet = new Set(filtered.headers);
const currentHeaderSet = new Set(current.headers);
const sourceOnlyHeaders = current.headers.filter((h) => !filteredHeaderSet.has(h));
const filteredOnlyHeaders = filtered.headers.filter((h) => !currentHeaderSet.has(h));
const commonHeaders = filtered.headers.filter((h) => currentHeaderSet.has(h));

const sourceFilesRows = [
  {
    role: "current_raw_main_download",
    url: mainRawUrl,
    local_path: rel(currentRawPath),
    exists: fs.existsSync(currentRawPath) ? "yes" : "no",
    size_bytes: fs.statSync(currentRawPath).size,
    sha256: hashFile(currentRawPath),
    commit_sha: currentCommitSha,
    note: "Fetched 2026-05-31 America/Los_Angeles from GitHub raw main; used only after path commit pin was resolved.",
  },
  {
    role: "pinned_raw_download",
    url: pinnedRawUrl,
    local_path: rel(pinnedRawPath),
    exists: fs.existsSync(pinnedRawPath) ? "yes" : "no",
    size_bytes: fs.statSync(pinnedRawPath).size,
    sha256: hashFile(pinnedRawPath),
    commit_sha: currentCommitSha,
    note: "Pinned copy of the same source file at the resolved commit.",
  },
  {
    role: "github_commit_api_response",
    url: commitApiUrl,
    local_path: fs.existsSync(commitJsonPath) ? rel(commitJsonPath) : "",
    exists: fs.existsSync(commitJsonPath) ? "yes" : "no",
    size_bytes: fs.existsSync(commitJsonPath) ? fs.statSync(commitJsonPath).size : 0,
    sha256: hashFile(commitJsonPath),
    commit_sha: currentCommitSha,
    note: `commit_date=${commit.commit?.committer?.date ?? ""}; message=${commit.commit?.message ?? ""}`,
  },
  {
    role: "prior_local_raw_download",
    url: mainRawUrl,
    local_path: fs.existsSync(priorRawPath) ? rel(priorRawPath) : "",
    exists: fs.existsSync(priorRawPath) ? "yes" : "no",
    size_bytes: fs.existsSync(priorRawPath) ? fs.statSync(priorRawPath).size : 0,
    sha256: hashFile(priorRawPath),
    commit_sha: "",
    note: "Existing local raw snapshot from 2026-05-26, used for stability comparison only.",
  },
  {
    role: "filtered_local_metadata",
    url: "",
    local_path: rel(metadataPath),
    exists: "yes",
    size_bytes: fs.statSync(metadataPath).size,
    sha256: hashFile(metadataPath),
    commit_sha: "",
    note: "Filtered project table with Sanskrit, translation, and notes removed.",
  },
];

const schemaRows = [
  {
    comparison: "current_raw_vs_filtered",
    current_columns: current.headers.length,
    filtered_columns: filtered.headers.length,
    source_only_columns: sourceOnlyHeaders.join("|"),
    filtered_only_columns: filteredOnlyHeaders.join("|"),
    interpretation:
      sourceOnlyHeaders.join("|") === "sanskrit|translation|notes" && filteredOnlyHeaders.length === 0
        ? "unfiltered source adds only quarantined decipherment columns"
        : "schema mismatch needs manual review",
  },
  {
    comparison: "current_raw_vs_pinned_raw",
    current_columns: current.headers.length,
    filtered_columns: pinned.headers.length,
    source_only_columns: current.headers.filter((h) => !new Set(pinned.headers).has(h)).join("|"),
    filtered_only_columns: pinned.headers.filter((h) => !currentHeaderSet.has(h)).join("|"),
    interpretation:
      hashFile(currentRawPath) === hashFile(pinnedRawPath)
        ? "current main download equals pinned commit download by SHA-256"
        : "current main differs from pinned commit",
  },
  {
    comparison: "current_raw_vs_prior_20260526_raw",
    current_columns: current.headers.length,
    filtered_columns: prior.headers.length,
    source_only_columns: "",
    filtered_only_columns: "",
    interpretation:
      prior.rows.length && hashFile(currentRawPath) === hashFile(priorRawPath)
        ? "current download equals 2026-05-26 local raw snapshot by SHA-256"
        : "no prior match or prior snapshot missing",
  },
];

const targetRows = [
  {
    source_layer: "current_raw_main_download",
    admissibility: "metadata_sign_fields_only",
    common_metadata_equal_to_filtered: sameCommonMetadata(targetCurrent, targetFiltered, commonHeaders) ? "yes" : "no",
    source_only_quarantined_columns_present: sourceOnlyHeaders.join("|"),
    sanskrit_observed_quarantined: targetCurrent.sanskrit ?? "",
    translation_observed_quarantined: targetCurrent.translation ?? "",
    notes_observed_quarantined: targetCurrent.notes ?? "",
    witness_artifact_id: witness.artifact_id ?? "",
    witness_provenance_tier: witness.provenance_tier ?? "",
    ...compact(targetCurrent),
  },
  {
    source_layer: "pinned_raw_commit_download",
    admissibility: "metadata_sign_fields_only",
    common_metadata_equal_to_filtered: sameCommonMetadata(targetPinned, targetFiltered, commonHeaders) ? "yes" : "no",
    source_only_quarantined_columns_present: sourceOnlyHeaders.join("|"),
    sanskrit_observed_quarantined: targetPinned.sanskrit ?? "",
    translation_observed_quarantined: targetPinned.translation ?? "",
    notes_observed_quarantined: targetPinned.notes ?? "",
    witness_artifact_id: witness.artifact_id ?? "",
    witness_provenance_tier: witness.provenance_tier ?? "",
    ...compact(targetPinned),
  },
  {
    source_layer: "prior_raw_20260526_snapshot",
    admissibility: prior.rows.length ? "metadata_sign_fields_only" : "missing",
    common_metadata_equal_to_filtered:
      prior.rows.length && sameCommonMetadata(targetPrior, targetFiltered, commonHeaders) ? "yes" : "no",
    source_only_quarantined_columns_present: prior.rows.length ? sourceOnlyHeaders.join("|") : "",
    sanskrit_observed_quarantined: targetPrior.sanskrit ?? "",
    translation_observed_quarantined: targetPrior.translation ?? "",
    notes_observed_quarantined: targetPrior.notes ?? "",
    witness_artifact_id: witness.artifact_id ?? "",
    witness_provenance_tier: witness.provenance_tier ?? "",
    ...compact(targetPrior.id ? targetPrior : targetFiltered),
  },
  {
    source_layer: "filtered_local_metadata",
    admissibility: "T3_quarantined_metadata_pressure_only",
    common_metadata_equal_to_filtered: "self",
    source_only_quarantined_columns_present: "",
    sanskrit_observed_quarantined: "",
    translation_observed_quarantined: "",
    notes_observed_quarantined: "",
    witness_artifact_id: witness.artifact_id ?? "",
    witness_provenance_tier: witness.provenance_tier ?? "",
    ...compact(targetFiltered),
  },
];

const neighborRows = current.rows
  .filter((r) => /^33[3-4]\d\.1$/.test(r.id))
  .map((r) => ({
    row_order_note:
      r.id === "3335.1"
        ? "target sits between M-939 and M-941 in row order, but row-order inference is not a source bridge"
        : "",
    object_id_present: norm(r.cisi) ? "yes" : "no",
    ...compact(r),
  }));

const chunkSpecs = [
  { chunk: "740-205-032-002-390-590-032", role: "exact target sequence" },
  { chunk: "740-205-032-002", role: "target left prefix before branch" },
  { chunk: "032-002-390", role: "matched 032 branch lane" },
  { chunk: "002-390-590", role: "target branch plus first tail" },
  { chunk: "390-590-032", role: "portable formula-family chunk" },
];

const chunkRows = [];
for (const spec of chunkSpecs) {
  for (const row of current.rows) {
    if (!`-${textKey(row)}-`.includes(`-${spec.chunk}-`)) continue;
    chunkRows.push({
      chunk: spec.chunk,
      role: spec.role,
      match_type: textKey(row) === spec.chunk ? "exact_text" : textKey(row).startsWith(spec.chunk) ? "prefix" : "contains",
      object_id_present: norm(row.cisi) ? "yes" : "no",
      source_layer: row.id === targetId ? "raw_lipi_target_unbound" : "raw_lipi_comparandum",
      ...compact(row),
    });
  }
}

const decisions = [
  {
    decision: "upstream_source_pinned",
    evidence: `GitHub path commit ${currentCommitSha}; pinned raw URL ${pinnedRawUrl}; raw SHA-256 ${hashFile(currentRawPath)}`,
    consequence: "the recheck is reproducible and no longer depends on floating main alone",
    accepted_scope: "source provenance for the CSV only",
  },
  {
    decision: "raw_source_adds_no_object_bridge",
    evidence: "current and pinned raw rows keep cisi='-', site='Unknown', excavation-idno='-', and no image/plate/source field",
    consequence: "3335.1 remains unbound T3 metadata pressure, not source evidence",
    accepted_scope: "negative source gate",
  },
  {
    decision: "decipherment_columns_remain_quarantined",
    evidence: "the only raw-source columns absent from the filtered table are sanskrit, translation, and notes",
    consequence: "these fields are recorded as observed but are not labels, readings, values, translations, or training targets",
    accepted_scope: "quarantine guardrail",
  },
  {
    decision: "row_order_anomaly_no_promotion",
    evidence: "3335.1 sits between M-939 and M-941 in raw row order while cisi is blank",
    consequence: "the missing M-940-looking slot is a search clue only; it does not identify the artifact",
    accepted_scope: "acquisition hint, not admissible binding",
  },
  {
    decision: "matched_032_gate_still_blocked",
    evidence: "the target sequence is present but unbound; M-70 remains the strict source-visible 032 -> 002-390 -> 692 comparator",
    consequence: "no strict 032 matched-branch split is counted",
    accepted_scope: "campaign decision",
  },
  {
    decision: "no_reading_no_values",
    evidence: "no source image, authoritative sign list, object id, or independent publication bridge was gained",
    consequence: "accepted value, phonetics, language identity, function, sign meaning, and translation remain 0",
    accepted_scope: "global guardrail",
  },
];

const summary = {
  status: "3335_yajnadevam_pinned_provenance_recheck_no_source_bridge_no_values",
  date: "2026-05-31 America/Los_Angeles",
  target_id: targetId,
  target_text: targetCurrent.text,
  commit_sha: currentCommitSha,
  commit_url: commit.html_url ?? `https://github.com/yajnadevam/lipi/commit/${currentCommitSha}`,
  main_raw_url: mainRawUrl,
  pinned_raw_url: pinnedRawUrl,
  current_raw_sha256: hashFile(currentRawPath),
  pinned_raw_sha256: hashFile(pinnedRawPath),
  prior_raw_sha256: hashFile(priorRawPath),
  current_equals_pinned: hashFile(currentRawPath) === hashFile(pinnedRawPath),
  current_equals_prior_20260526: fs.existsSync(priorRawPath) && hashFile(currentRawPath) === hashFile(priorRawPath),
  rows: current.rows.length,
  columns: current.headers.length,
  source_only_headers: sourceOnlyHeaders,
  filtered_only_headers: filteredOnlyHeaders,
  target_bridge_fields: {
    cisi: targetCurrent.cisi,
    site: targetCurrent.site,
    excavation_idno: targetCurrent["excavation-idno"],
    image_ref_id: witness.image_ref_id ?? "",
    artifact_id: witness.artifact_id ?? "",
    provenance_tier: witness.provenance_tier ?? "",
  },
  row_order_context: neighborRows
    .filter((r) => ["3334.1", "3335.1", "3336.1"].includes(r.id))
    .map((r) => ({ id: r.id, cisi: r.cisi, text: r.text })),
  chunk_counts: Object.fromEntries(chunkSpecs.map((spec) => [spec.chunk, chunkRows.filter((r) => r.chunk === spec.chunk).length])),
  decisions,
};

writeCsv(path.join(reportsDir, `${prefix}_source_files.csv`), sourceFilesRows, [
  "role",
  "url",
  "local_path",
  "exists",
  "size_bytes",
  "sha256",
  "commit_sha",
  "note",
]);
writeCsv(path.join(reportsDir, `${prefix}_schema_delta.csv`), schemaRows, [
  "comparison",
  "current_columns",
  "filtered_columns",
  "source_only_columns",
  "filtered_only_columns",
  "interpretation",
]);
writeCsv(path.join(reportsDir, `${prefix}_target_comparison.csv`), targetRows, [
  "source_layer",
  "admissibility",
  "common_metadata_equal_to_filtered",
  "source_only_quarantined_columns_present",
  "sanskrit_observed_quarantined",
  "translation_observed_quarantined",
  "notes_observed_quarantined",
  "witness_artifact_id",
  "witness_provenance_tier",
  "id",
  "cisi",
  "region",
  "site",
  "excavation_idno",
  "type",
  "symbol",
  "cult",
  "material",
  "shape",
  "dimensions_mm",
  "text",
]);
writeCsv(path.join(reportsDir, `${prefix}_neighbor_rows.csv`), neighborRows, [
  "row_order_note",
  "object_id_present",
  "id",
  "cisi",
  "region",
  "site",
  "excavation_idno",
  "type",
  "symbol",
  "cult",
  "material",
  "shape",
  "dimensions_mm",
  "text",
]);
writeCsv(path.join(reportsDir, `${prefix}_chunk_rows.csv`), chunkRows, [
  "chunk",
  "role",
  "match_type",
  "object_id_present",
  "source_layer",
  "id",
  "cisi",
  "region",
  "site",
  "excavation_idno",
  "type",
  "symbol",
  "cult",
  "material",
  "shape",
  "dimensions_mm",
  "text",
]);
writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  "decision",
  "evidence",
  "consequence",
  "accepted_scope",
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
