// Traces blocked row 3335.1 through the full git history of the Yajnadevam Lipi
// repo, looking for any source trail the current CSV no longer shows. Working
// in a pre-cloned copy under tmp/002390x_3335_yajnadevam_repo_trace_20260531/,
// it pulls the target row from three layers (current HEAD, the schema-migration
// commit, and the old "externalize" commit where the row was id 3335 and the
// museum field said "Private collection"), runs git pickaxe and blame to find
// every commit that touched the row, greps the whole tree for the target id and
// sign string, and checks the seal-image mapping JSON plus the frontend code
// path that renders images (keyed by CISI id, which this row lacks). Writes
// seven CSVs and a summary JSON to data/open_prototype/reports/. Outcome: the
// row appears only in inscriptions.csv and the derived (quarantined) glossing
// file, has no image bridge in any commit, and the private-collection clue is
// the only lead — no value or reading is accepted.

import crypto from "node:crypto";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const repoDir = path.join(root, "tmp", "002390x_3335_yajnadevam_repo_trace_20260531", "repo");
const reportsDir = path.join(root, "data", "open_prototype", "reports");
const prefix = "campaign_032_002_861_002390x_3335_yajnadevam_repo_trace_20260531";
const targetId = "3335.1";
const oldTargetId = "3335";
const targetText = "+740-205-032-002-390-590-032+";
const oldExternalizeCommit = "0921d91d309621a292ba22bacce3f0f9c3ede929";
const schemaCommit = "14b3421f33b1a6a38cee0d7ee54ad5669ef323dd";
const latestTargetMeaningCommit = "92ec6a013fccc892b5063b9eada5d21b29a2a099";

function git(args) {
  return execFileSync("git", ["-C", repoDir, ...args], {
    encoding: "utf8",
    maxBuffer: 64 * 1024 * 1024,
  }).replace(/\r\n/g, "\n");
}

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

function csvEscape(value) {
  const s = String(value ?? "");
  return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

function writeCsv(filePath, rows, headers) {
  const lines = [headers.join(",")];
  for (const row of rows) lines.push(headers.map((h) => csvEscape(row[h])).join(","));
  fs.writeFileSync(filePath, `${lines.join("\n")}\n`);
}

function sha256(filePath) {
  if (!fs.existsSync(filePath)) return "";
  return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex");
}

function rel(filePath) {
  return path.relative(root, filePath).replaceAll(path.sep, "/");
}

function lineNumberOf(text, needle) {
  const lines = text.replace(/\r\n/g, "\n").replace(/\r/g, "\n").split("\n");
  const index = lines.findIndex((line) => line.includes(needle));
  return index === -1 ? "" : String(index + 1);
}

function gitCommitRows(logText, search_term, route) {
  return logText
    .split("\n")
    .filter(Boolean)
    .map((line) => {
      const [commit, date, subject] = line.split("\t");
      return { route, search_term, commit, date, subject };
    });
}

function mustFind(rows, pred, label) {
  const row = rows.find(pred);
  if (!row) throw new Error(`Missing ${label}`);
  return row;
}

function epochToIso(epochSeconds) {
  const n = Number(epochSeconds);
  return Number.isFinite(n) ? new Date(n * 1000).toISOString() : String(epochSeconds ?? "");
}

function gitShowFile(commit, filePath) {
  return git(["show", `${commit}:${filePath}`]);
}

function codeContains(filePath, needle) {
  const fullPath = path.join(repoDir, filePath);
  return fs.existsSync(fullPath) && fs.readFileSync(fullPath, "utf8").includes(needle);
}

fs.mkdirSync(reportsDir, { recursive: true });
if (!fs.existsSync(repoDir)) throw new Error(`Missing cloned repo: ${repoDir}`);

const head = git(["rev-parse", "HEAD"]).trim();
const revCount = Number(git(["rev-list", "--count", "--all"]).trim());
const shallow = fs.existsSync(path.join(repoDir, ".git", "shallow")) ? "yes" : "no";
const branches = git(["branch", "-r"]).trim().split("\n").map((s) => s.trim()).filter(Boolean).join("|");
const remoteHeads = git(["ls-remote", "--heads", "origin"]).trim().split("\n").filter(Boolean).join("|");

const currentCsvPath = path.join(repoDir, "src", "assets", "data", "inscriptions.csv");
const imageMapPath = path.join(repoDir, "src", "assets", "data", "seal_id_and_image_mapping.json");
const glossingPath = path.join(repoDir, "glossing.csv");
const currentCsvText = fs.readFileSync(currentCsvPath, "utf8");
const current = parseCsv(currentCsvText);
const currentTarget = mustFind(current.rows, (r) => r.id === targetId, "current 3335.1 row");
const currentLineNumber = lineNumberOf(currentCsvText, targetId);

const oldCsvText = gitShowFile(oldExternalizeCommit, "src/assets/data/inscriptions.csv");
const oldCsv = parseCsv(oldCsvText);
const oldTarget = mustFind(oldCsv.rows, (r) => r.id === oldTargetId, "old 3335 row");
const oldLineNumber = lineNumberOf(oldCsvText, targetText);

const schemaCsvText = gitShowFile(schemaCommit, "src/assets/data/inscriptions.csv");
const schemaCsv = parseCsv(schemaCsvText);
const schemaTarget = mustFind(schemaCsv.rows, (r) => r.id === targetId, "schema 3335.1 row");

const imageMap = JSON.parse(fs.readFileSync(imageMapPath, "utf8"));
const imageKeys = Object.keys(imageMap);
const interestingImageKeys = imageKeys.filter((k) => k === "-" || /3335|Unknown|RAF|740|205|390|590/.test(k));
const neighborKeys = ["M-939", "M-940", "M-941"];
const imageRows = [
  {
    key: "3335.1",
    images: (imageMap[targetId] ?? []).join("|"),
    image_count: imageMap[targetId]?.length ?? 0,
    interpretation: "no image mapping for target id",
  },
  {
    key: "-",
    images: (imageMap["-"] ?? []).join("|"),
    image_count: imageMap["-"]?.length ?? 0,
    interpretation: "no image mapping for blank/dash CISI key",
  },
  ...neighborKeys.map((key) => ({
    key,
    images: (imageMap[key] ?? []).join("|"),
    image_count: imageMap[key]?.length ?? 0,
    interpretation: "neighbor object has explicit image mapping",
  })),
  ...interestingImageKeys
    .filter((key) => key !== "-" && key !== targetId && !neighborKeys.includes(key))
    .map((key) => ({
      key,
      images: (imageMap[key] ?? []).join("|"),
      image_count: imageMap[key]?.length ?? 0,
      interpretation: "numeric-name collision only; not target metadata",
    })),
];

const occurrenceRows = [];
for (const filePath of [
  "src/assets/data/inscriptions.csv",
  "glossing.csv",
  "src/assets/data/seal_id_and_image_mapping.json",
]) {
  const fullPath = path.join(repoDir, filePath);
  const text = fs.existsSync(fullPath) ? fs.readFileSync(fullPath, "utf8") : "";
  const lines = text.replace(/\r\n/g, "\n").replace(/\r/g, "\n").split("\n");
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.includes(targetId) || line.includes(targetText.slice(1, -1)) || line.includes("sva-rava-sahana")) {
      occurrenceRows.push({
        file: filePath,
        line: i + 1,
        occurrence_type: filePath === "glossing.csv" ? "derived_quarantined_glossing" : "repo_data_occurrence",
        text: line,
      });
    }
  }
}

const noOtherOccurrence = git(["grep", "-n", "-E", "3335\\.1|740-205-032-002-390-590-032|sva-rava-sahana", "HEAD", "--", "."])
  .split("\n")
  .filter(Boolean)
  .filter((line) => {
    return (
      !line.includes("HEAD:src/assets/data/inscriptions.csv:") &&
      !line.includes("HEAD:glossing.csv:") &&
      !line.includes("HEAD:dev-tools/ashtadhyayi/assets/mw.xml:")
    );
  });

const historyRows = [
  ...gitCommitRows(
    git(["log", "--all", "--date=iso-strict", "--format=%H%x09%ad%x09%s", "-S", oldTargetId, "--", "src/assets/data/inscriptions.csv"]),
    oldTargetId,
    "pickaxe_old_id",
  ),
  ...gitCommitRows(
    git(["log", "--all", "--date=iso-strict", "--format=%H%x09%ad%x09%s", "-S", targetText.slice(1, -1), "--", "src/assets/data/inscriptions.csv"]),
    targetText,
    "pickaxe_exact_text",
  ),
];

const blameLine = git(["blame", "-L", `${currentLineNumber},${currentLineNumber}`, "--line-porcelain", "--", "src/assets/data/inscriptions.csv"]);
const blameCommit = blameLine.split(" ")[0];
const blameSummary = blameLine.split("\n").find((line) => line.startsWith("summary "))?.slice("summary ".length) ?? "";
const blameAuthorTime = blameLine.split("\n").find((line) => line.startsWith("author-time "))?.slice("author-time ".length) ?? "";

historyRows.push({
  route: "current_line_blame",
  search_term: targetId,
  commit: blameCommit,
  date: epochToIso(blameAuthorTime),
  subject: blameSummary,
});

const targetRows = [
  {
    layer: "current_head",
    commit: head,
    line: currentLineNumber,
    id: currentTarget.id,
    cisi: currentTarget.cisi,
    site: currentTarget.site,
    excavation_idno: currentTarget["excavation-idno"],
    museum_or_source: "",
    dimensions: `${currentTarget["horizontal(mm)"]} x ${currentTarget["vertical(mm)"]} x ${currentTarget["thickness(mm)"]}`,
    text: currentTarget.text,
    bridge_interpretation: "current row still has cisi dash, unknown site, no excavation id, and no image/source field",
  },
  {
    layer: "schema_migration_commit",
    commit: schemaCommit,
    line: lineNumberOf(schemaCsvText, targetId),
    id: schemaTarget.id,
    cisi: schemaTarget.cisi,
    site: schemaTarget.site,
    excavation_idno: schemaTarget["excavation-idno"],
    museum_or_source: "",
    dimensions: `${schemaTarget["horizontal(mm)"]} x ${schemaTarget["vertical(mm)"]} x ${schemaTarget["thickness(mm)"]}`,
    text: schemaTarget.text,
    bridge_interpretation: "schema migration converted old row to current shape but did not add source bridge",
  },
  {
    layer: "old_externalize_commit",
    commit: oldExternalizeCommit,
    line: oldLineNumber,
    id: oldTarget.id,
    cisi: oldTarget.CISI,
    site: oldTarget.site,
    excavation_idno: oldTarget["excavationid no."],
    museum_or_source: oldTarget.museum,
    dimensions: `${oldTarget.width} x ${oldTarget.height} x ${oldTarget.thickness}`,
    text: oldTarget.text,
    bridge_interpretation:
      oldTarget.museum === "Private collection"
        ? "old source layer preserves private-collection clue but no public object id, image, or citation"
        : "old source layer did not provide source bridge",
  },
];

const codeRows = [
  {
    file: "src/pages/index.vue",
    finding: "image lookup uses sealImages[item.cisi]",
    present: codeContains("src/pages/index.vue", "sealImages[item.cisi]") ? "yes" : "no",
    interpretation: "cisi dash row cannot render an image unless the map has a dash key",
  },
  {
    file: "dev-tools/generate-seal-id-to-image-map.js",
    finding: "image-map generator derives keys from filenames matching place-number pattern",
    present: codeContains("dev-tools/generate-seal-id-to-image-map.js", "const sealImageNamePattern") ? "yes" : "no",
    interpretation: "public image assets are keyed to object ids like M-940, not metadata row ids like 3335.1",
  },
  {
    file: "src/assets/data/seal_id_and_image_mapping.json",
    finding: "target and dash keys absent",
    present: imageMap[targetId] || imageMap["-"] ? "yes" : "no",
    interpretation: "no repo-internal image bridge for 3335.1",
  },
];

const decisions = [
  {
    gate: "repo_occurrence",
    decision: occurrenceRows.length > 0 && noOtherOccurrence.length === 0 ? "target only in inscriptions plus derived glossing" : "manual review needed",
    evidence: `occurrences=${occurrenceRows.length}; extra_occurrences=${noOtherOccurrence.length}`,
    consequence: "repo search does not expose an independent source trail",
  },
  {
    gate: "image_bridge",
    decision: !imageMap[targetId] && !imageMap["-"] ? "no target image bridge" : "manual review needed",
    evidence: `target_images=${imageMap[targetId]?.length ?? 0}; dash_images=${imageMap["-"]?.length ?? 0}; M-940_images=${imageMap["M-940"]?.length ?? 0}`,
    consequence: "row-order M-940 temptation remains rejected",
  },
  {
    gate: "history_private_collection",
    decision: oldTarget.museum === "Private collection" ? "private-collection clue recorded" : "no private-collection clue",
    evidence: `old_commit=${oldExternalizeCommit}; old_museum=${oldTarget.museum}`,
    consequence: "use as external acquisition wording only, not as source-bound evidence",
  },
  {
    gate: "accepted_values",
    decision: "no values accepted",
    evidence: "no source image, no object id, no public citation, no strict sign-band witness",
    consequence: "value, phonetics, language identity, function, sign meaning, and translation remain 0",
  },
];

const sourceFiles = [
  {
    role: "git_repo_clone",
    path: rel(repoDir),
    exists: "yes",
    sha256: "",
    head,
    note: `rev_count_all=${revCount}; shallow=${shallow}; branches=${branches}`,
  },
  {
    role: "remote_heads",
    path: "https://github.com/yajnadevam/lipi.git",
    exists: "yes",
    sha256: "",
    head: remoteHeads,
    note: "main and experimental fetched before history trace",
  },
  {
    role: "current_inscriptions_csv",
    path: rel(currentCsvPath),
    exists: fs.existsSync(currentCsvPath) ? "yes" : "no",
    sha256: sha256(currentCsvPath),
    head,
    note: `rows=${current.rows.length}; columns=${current.headers.length}`,
  },
  {
    role: "image_mapping_json",
    path: rel(imageMapPath),
    exists: fs.existsSync(imageMapPath) ? "yes" : "no",
    sha256: sha256(imageMapPath),
    head,
    note: `keys=${imageKeys.length}`,
  },
  {
    role: "glossing_csv",
    path: rel(glossingPath),
    exists: fs.existsSync(glossingPath) ? "yes" : "no",
    sha256: sha256(glossingPath),
    head,
    note: "derived quarantined Sanskrit glossing layer; not evidence",
  },
];

const summary = {
  status: "3335_yajnadevam_repo_history_private_collection_no_image_bridge_no_values",
  date: "2026-05-31 America/Los_Angeles",
  repo_head: head,
  repo_rev_count_all: revCount,
  shallow,
  target_current: targetRows[0],
  target_old_externalize: targetRows[2],
  image_bridge: {
    target_images: imageMap[targetId] ?? null,
    dash_images: imageMap["-"] ?? null,
    neighbors: Object.fromEntries(neighborKeys.map((key) => [key, imageMap[key] ?? null])),
  },
  history: {
    pickaxe_rows: historyRows,
    current_line_blame: { commit: blameCommit, summary: blameSummary, author_time: epochToIso(blameAuthorTime) },
  },
  no_other_occurrences_after_exclusions: noOtherOccurrence.length === 0,
  decisions,
};

writeCsv(path.join(reportsDir, `${prefix}_source_files.csv`), sourceFiles, [
  "role",
  "path",
  "exists",
  "sha256",
  "head",
  "note",
]);
writeCsv(path.join(reportsDir, `${prefix}_target_history.csv`), targetRows, [
  "layer",
  "commit",
  "line",
  "id",
  "cisi",
  "site",
  "excavation_idno",
  "museum_or_source",
  "dimensions",
  "text",
  "bridge_interpretation",
]);
writeCsv(path.join(reportsDir, `${prefix}_image_mapping.csv`), imageRows, [
  "key",
  "images",
  "image_count",
  "interpretation",
]);
writeCsv(path.join(reportsDir, `${prefix}_occurrences.csv`), occurrenceRows, [
  "file",
  "line",
  "occurrence_type",
  "text",
]);
writeCsv(path.join(reportsDir, `${prefix}_git_history.csv`), historyRows, [
  "route",
  "search_term",
  "commit",
  "date",
  "subject",
]);
writeCsv(path.join(reportsDir, `${prefix}_code_paths.csv`), codeRows, [
  "file",
  "finding",
  "present",
  "interpretation",
]);
writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  "gate",
  "decision",
  "evidence",
  "consequence",
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
