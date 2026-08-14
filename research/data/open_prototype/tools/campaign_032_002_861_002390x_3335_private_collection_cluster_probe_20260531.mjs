// Follows one provenance clue for the blocked row 3335.1: an old commit of the
// Yajnadevam Lipi repo marked it museum="Private collection". If that put it in
// a batch of private-collection objects with images, we might find a source
// bridge. This script reads the already-cloned repo trace (under
// tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo), uses git show to pull
// the inscriptions.csv from the old and schema-change commits, and compares
// every private-collection row across the old, schema, and current layers. It
// checks the repo's seal-image mapping JSON for every plausible key, greps the
// repo for the target strings, and lists the commit history that touched
// "Private collection". Results go to five CSVs and a summary JSON under
// data/open_prototype/reports/. The baked-in outcome: the cluster is just two
// rows (3335 and its sibling 3118), neither has an image mapping, so "Private
// collection" is an acquisition clue, not a source bridge, and no value or
// reading is accepted.

import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const repoDir = path.join(root, "tmp", "002390x_3335_yajnadevam_repo_trace_20260531", "repo");
const reportsDir = path.join(root, "data", "open_prototype", "reports");
const prefix = "campaign_032_002_861_002390x_3335_private_collection_cluster_probe_20260531";
const oldCommit = "0921d91d309621a292ba22bacce3f0f9c3ede929";
const schemaCommit = "14b3421f33b1a6a38cee0d7ee54ad5669ef323dd";
const targetOldId = "3335";
const targetId = "3335.1";
const targetText = "+740-205-032-002-390-590-032+";

function git(args) {
  return execFileSync("git", ["-C", repoDir, ...args], {
    encoding: "utf8",
    maxBuffer: 64 * 1024 * 1024,
  }).replace(/\r\n/g, "\n");
}

function normalizeHeader(headers) {
  const seen = new Map();
  return headers.map((header, idx) => {
    const clean = header || `H${idx + 1}`;
    const count = seen.get(clean) ?? 0;
    seen.set(clean, count + 1);
    return count ? `${clean}.${count + 1}` : clean;
  });
}

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (ch === '"' && next === '"') {
        field += '"';
        i += 1;
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
      if (row.some((value) => value !== "")) rows.push(row);
      row = [];
      field = "";
    } else {
      field += ch;
    }
  }
  if (field.length || row.length) {
    row.push(field.replace(/\r$/, ""));
    if (row.some((value) => value !== "")) rows.push(row);
  }
  const [rawHeaders, ...body] = rows;
  const headers = normalizeHeader(rawHeaders);
  return body.map((cols) => Object.fromEntries(headers.map((name, idx) => [name, cols[idx] ?? ""])));
}

function csvEscape(value) {
  const text = String(value ?? "");
  return /[",\n\r]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(",")];
  for (const row of rows) lines.push(fields.map((field) => csvEscape(row[field])).join(","));
  fs.writeFileSync(file, `${lines.join("\n")}\n`);
}

function rel(file) {
  return path.relative(root, file).replaceAll(path.sep, "/");
}

function oldKey(row, key) {
  return row[key] ?? "";
}

function currentObject(row) {
  const cisi = String(row.cisi ?? "").trim();
  return cisi && cisi !== "-" ? cisi : `-:${row.id}`;
}

function lineNumber(text, needle) {
  const lines = text.replace(/\r\n/g, "\n").replace(/\r/g, "\n").split("\n");
  const idx = lines.findIndex((line) => line.includes(needle));
  return idx === -1 ? "" : String(idx + 1);
}

fs.mkdirSync(reportsDir, { recursive: true });
if (!fs.existsSync(repoDir)) throw new Error(`Missing repo trace clone: ${repoDir}`);

const oldCsvText = git(["show", `${oldCommit}:src/assets/data/inscriptions.csv`]);
const schemaCsvText = git(["show", `${schemaCommit}:src/assets/data/inscriptions.csv`]);
const currentCsvPath = path.join(repoDir, "src", "assets", "data", "inscriptions.csv");
const imageMapPath = path.join(repoDir, "src", "assets", "data", "seal_id_and_image_mapping.json");
const currentCsvText = fs.readFileSync(currentCsvPath, "utf8");
const imageMap = JSON.parse(fs.readFileSync(imageMapPath, "utf8"));

const oldRows = parseCsv(oldCsvText);
const schemaRows = parseCsv(schemaCsvText);
const currentRows = parseCsv(currentCsvText);

const privateRows = oldRows.filter((row) => oldKey(row, "museum") === "Private collection");
const currentByOld = new Map(currentRows.map((row) => [String(row.id).replace(/\.1$/, ""), row]));
const schemaByOld = new Map(schemaRows.map((row) => [String(row.id).replace(/\.1$/, ""), row]));

const privateCluster = privateRows.map((oldRow) => {
  const oldId = oldKey(oldRow, "id");
  const current = currentByOld.get(oldId) ?? {};
  const schema = schemaByOld.get(oldId) ?? {};
  const ids = [oldId, current.id, schema.id].filter(Boolean);
  const imageKeys = [...new Set([...ids, currentObject(current), "-", oldKey(oldRow, "CISI")].filter(Boolean))];
  const mapped = imageKeys
    .map((key) => ({ key, images: imageMap[key] ?? [] }))
    .filter((item) => item.images.length);
  return {
    old_id: oldId,
    current_id: current.id ?? "",
    current_object: current.id ? currentObject(current) : "",
    old_line: lineNumber(oldCsvText, `${oldId},`),
    current_line: current.id ? lineNumber(currentCsvText, `${current.id},`) : "",
    old_site: oldKey(oldRow, "site"),
    current_site: current.site ?? "",
    old_cisi: oldKey(oldRow, "CISI"),
    current_cisi: current.cisi ?? "",
    old_museum: oldKey(oldRow, "museum"),
    old_type: oldKey(oldRow, "type"),
    current_type: current.type ?? "",
    old_symbol: oldKey(oldRow, "symbol"),
    current_symbol: current.symbol ?? "",
    old_cult: oldKey(oldRow, "cult"),
    current_cult: current.cult ?? "",
    old_class: oldKey(oldRow, "class"),
    current_class: current.class ?? "",
    old_dimensions_mm: `${oldKey(oldRow, "width")} x ${oldKey(oldRow, "height")} x ${oldKey(oldRow, "thickness")}`,
    current_dimensions_mm: `${current["horizontal(mm)"] ?? ""} x ${current["vertical(mm)"] ?? ""} x ${current["thickness(mm)"] ?? ""}`,
    old_text: oldKey(oldRow, "text"),
    current_text: current.text ?? "",
    image_keys_checked: imageKeys.join("|"),
    image_mapping: mapped.map((item) => `${item.key}:${item.images.join("|")}`).join("; "),
    decision: mapped.length ? "has_image_mapping_needs_followup" : "no_repo_image_mapping",
  };
});

const imageMapRows = [];
for (const id of [targetOldId, targetId, "3118", "3118.1", "-", "-:3335.1", "-:3118.1"]) {
  imageMapRows.push({
    key: id,
    image_count: imageMap[id]?.length ?? 0,
    images: (imageMap[id] ?? []).join("|"),
    decision: imageMap[id]?.length ? "mapped" : "not_mapped",
  });
}

const repoGrepRows = git([
  "grep",
  "-n",
  "-E",
  "Private collection|3335\\.1|3118\\.1|740-205-032-002-390-590-032|520-070-255-832-220-003-853",
  "HEAD",
  "--",
  "src/assets/data/inscriptions.csv",
  "glossing.csv",
  "src/assets/data/seal_id_and_image_mapping.json",
])
  .split("\n")
  .filter(Boolean)
  .map((line) => {
    const match = line.match(/^HEAD:([^:]+):(\d+):(.*)$/);
    return {
      file: match?.[1] ?? "",
      line: match?.[2] ?? "",
      route: match?.[1] === "glossing.csv" ? "derived_quarantined_glossing" : "repo_data",
      text: match?.[3] ?? line,
    };
  });

const historyRows = git([
  "log",
  "--all",
  "--date=iso-strict",
  "--format=%H%x09%ad%x09%s",
  "-S",
  "Private collection",
  "--",
  "src/assets/data/inscriptions.csv",
])
  .split("\n")
  .filter(Boolean)
  .map((line) => {
    const [commit, date, subject] = line.split("\t");
    return { search_term: "Private collection", commit, date, subject };
  });

const decisionRows = [
  {
    gate: "private_collection_cluster_size",
    observation: `old_externalize_commit_private_collection_rows=${privateRows.length}`,
    decision: privateRows.length === 2 ? "bounded_two_row_cluster" : "cluster_requires_review",
    consequence: "3335.1 is not part of a broad private-collection image/source batch in the old Lipi layer",
  },
  {
    gate: "sibling_row_3118",
    observation: "3118/3118.1 is the only sibling; it is Unknown site, blank CISI/dash current CISI, no repo image mapping",
    decision: "sibling_does_not_supply_source_bridge",
    consequence: "do not use the private-collection cluster to source-bind 3335.1",
  },
  {
    gate: "image_map",
    observation: "3335, 3335.1, 3118, 3118.1, dash, and synthetic -: ids all have zero mapped images",
    decision: "repo_image_route_negative",
    consequence: "normal Lipi image path cannot render either private-collection row",
  },
  {
    gate: "public_exact_queries",
    observation: "manual exact web searches for target/sibling sign strings and quarantined gloss strings returned no usable bridge",
    decision: "public_exact_route_negative",
    consequence: "external acquisition still has to ask for the private-collection source behind old row 3335",
  },
  {
    gate: "claim_boundary",
    observation: "the only positive historical field is museum=Private collection",
    decision: "acquisition_wording_only_no_values",
    consequence: "accepted value, function, phonetics, language identity, sign meaning, and translation remain 0",
  },
];

const summary = {
  status: "3335_private_collection_cluster_two_rows_no_bridge_no_values",
  old_commit: oldCommit,
  schema_commit: schemaCommit,
  private_collection_rows: privateRows.length,
  private_collection_ids: privateCluster.map((row) => `${row.old_id}->${row.current_id}`).join(" "),
  target_old_id: targetOldId,
  target_current_id: targetId,
  target_text: targetText,
  target_has_repo_image_mapping: imageMap[targetOldId]?.length || imageMap[targetId]?.length ? "yes" : "no",
  sibling_row: privateCluster.find((row) => row.old_id !== targetOldId)?.current_id ?? "",
  sibling_has_repo_image_mapping: privateCluster.some((row) => row.old_id !== targetOldId && row.image_mapping) ? "yes" : "no",
  decision: "Private collection is now a two-row acquisition clue, not source evidence.",
  accepted_values_or_translations: 0,
  reports: {
    private_cluster: `${prefix}_private_cluster.csv`,
    image_map_keys: `${prefix}_image_map_keys.csv`,
    repo_occurrences: `${prefix}_repo_occurrences.csv`,
    history: `${prefix}_history.csv`,
    decisions: `${prefix}_decisions.csv`,
  },
};

writeCsv(
  path.join(reportsDir, `${prefix}_private_cluster.csv`),
  privateCluster,
  [
    "old_id",
    "current_id",
    "current_object",
    "old_line",
    "current_line",
    "old_site",
    "current_site",
    "old_cisi",
    "current_cisi",
    "old_museum",
    "old_type",
    "current_type",
    "old_symbol",
    "current_symbol",
    "old_cult",
    "current_cult",
    "old_class",
    "current_class",
    "old_dimensions_mm",
    "current_dimensions_mm",
    "old_text",
    "current_text",
    "image_keys_checked",
    "image_mapping",
    "decision",
  ],
);
writeCsv(path.join(reportsDir, `${prefix}_image_map_keys.csv`), imageMapRows, ["key", "image_count", "images", "decision"]);
writeCsv(path.join(reportsDir, `${prefix}_repo_occurrences.csv`), repoGrepRows, ["file", "line", "route", "text"]);
writeCsv(path.join(reportsDir, `${prefix}_history.csv`), historyRows, ["search_term", "commit", "date", "subject"]);
writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisionRows, ["gate", "observation", "decision", "consequence"]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
