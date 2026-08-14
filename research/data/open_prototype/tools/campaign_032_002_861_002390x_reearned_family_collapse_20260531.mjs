import fs from "node:fs";
import path from "node:path";

// An earlier "family collapse" analysis was quarantined, so this script re-earns the same
// result from clean inputs without touching the quarantined artifact. It reads the 002-390
// frames from the branch-sign-ecology report and the raw corpus in data/open_prototype/
// lipi/metadata_filtered.csv, then overrides each frame's source status from a hand-checked
// table (M-70/M-71/M-119/M-735 strict source-visible; Sktd-1, H-1993, Dholavira 4237.1,
// M-1825, H-773, and 3335.1 in various weaker states). Each frame gets a family key
// (site|type|symbol|cult|shape|predecessor|branch|tail) so duplicate template copies
// collapse into one cell, and each branch is summarized by raw frames versus family cells
// versus strict frames. Specific probes: the 235-predecessor 002-390-125 subframe (demoted —
// only one strict witness), the 125-632-032 tail family (formula pressure, not function),
// and branch 705 (zero strict rows, acquisitions pending). Writes frames, branch summary,
// prev-235 rows, tail rows, and decisions as CSVs plus a summary JSON in reports/.

const root = process.cwd();
const reportsDir = path.join(root, "data", "open_prototype", "reports");
const prefix = "campaign_032_002_861_002390x_reearned_family_collapse_20260531";
const framesPath = path.join(reportsDir, "campaign_032_002_861_002390x_branch_sign_ecology_20260531_002390_frames.csv");
const metadataPath = path.join(root, "data", "open_prototype", "lipi", "metadata_filtered.csv");

const SOURCE_STATUS_OVERRIDES = new Map([
  ["M-70", "checkpoint_strict_source_visible"],
  ["M-71", "checkpoint_strict_source_visible"],
  ["M-119", "checkpoint_strict_source_visible"],
  ["M-735", "checkpoint_strict_source_visible"],
  ["Sktd-1", "sktd1_side_pair_visible_wrapped_layout_not_strict"],
  ["H-1993", "h1993_source_contact_sent_awaiting_reply_no_values"],
  ["-:4237.1", "dholavira_8758_source_contact_sent_awaiting_reply_no_values"],
  ["M-1825", "m1825_source_contact_sent_awaiting_reply_no_values"],
  ["H-773", "source_panel_acquired_boxed_window_compatible_token_not_strict"],
  ["-:3335.1", "3335_yajnadevam_repo_history_private_collection_no_image_bridge_no_values"],
]);

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
  const [headers, ...body] = rows;
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

function tokens(text) {
  return String(text ?? "").match(/\d{3}/g) ?? [];
}

function objectId(row) {
  const cisi = String(row.cisi ?? "").trim();
  if (cisi && cisi !== "-") return cisi;
  return `-:${row.id}`;
}

function sourceStatus(object, fallback = "") {
  return SOURCE_STATUS_OVERRIDES.get(object) ?? fallback ?? "metadata_only_unbound";
}

function sourceTier(status) {
  if (status.includes("checkpoint_strict_source_visible")) return "strict_visible";
  if (status.includes("source_panel") || status.includes("side_pair") || status.includes("boxed")) return "panel_bound_not_strict";
  if (status.includes("contact_sent") || status.includes("acquisition") || status.includes("private_collection")) return "reply_or_external_source_pending";
  if (status.includes("metadata") || status.includes("unbound")) return "metadata_or_route_only";
  return "metadata_or_route_only";
}

function familyKey(row) {
  return [
    row.site || "Unknown",
    row.type || "Unknown",
    row.symbol || "None",
    row.cult || "None",
    row.shape || "Unknown",
    row.prev_before_002 || "<START>",
    row.branch_after_390 || "<NONE>",
    row.tail_after_branch || "<END>",
  ].join("|");
}

function countBy(rows, field) {
  const counts = new Map();
  for (const row of rows) counts.set(row[field], (counts.get(row[field]) ?? 0) + 1);
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([value, count]) => `${value}:${count}`)
    .join("; ");
}

function unique(rows, field) {
  return [...new Set(rows.map((row) => row[field]).filter(Boolean))].sort();
}

const frames = parseCsv(fs.readFileSync(framesPath, "utf8")).map((row) => {
  const status = sourceStatus(row.object, row.source_status);
  const tier = sourceTier(status);
  return {
    ...row,
    source_status_reearned: status,
    source_tier_reearned: tier,
    strict_countable: tier === "strict_visible" ? "yes" : "no",
    family_key_reearned: familyKey(row),
  };
});

const metadata = parseCsv(fs.readFileSync(metadataPath, "utf8"));
const tail632Rows = [];
for (const row of metadata) {
  const signs = tokens(row.text);
  for (let i = 0; i < signs.length - 2; i += 1) {
    if (signs[i] !== "125" || signs[i + 1] !== "632" || signs[i + 2] !== "032") continue;
    const object = objectId(row);
    const status = sourceStatus(object);
    const has002390125 = signs.some((sign, idx) => sign === "125" && signs[idx - 2] === "002" && signs[idx - 1] === "390");
    tail632Rows.push({
      id: row.id,
      object,
      site: row.site,
      type: row.type,
      symbol: row.symbol,
      cult: row.cult,
      shape: row.shape,
      pos_125_1based: i + 1,
      has_002390125_frame: has002390125 ? "yes" : "no",
      source_status_reearned: status,
      source_tier_reearned: sourceTier(status),
      strict_countable: sourceTier(status) === "strict_visible" ? "yes" : "no",
      text: row.text,
    });
  }
}

const branchSummary = [];
for (const branch of unique(frames, "branch_after_390")) {
  const rows = frames.filter((row) => row.branch_after_390 === branch);
  const familyCells = unique(rows, "family_key_reearned");
  const strictRows = rows.filter((row) => row.strict_countable === "yes");
  const strictFamilyCells = unique(strictRows, "family_key_reearned");
  branchSummary.push({
    branch_after_390: branch,
    raw_frames: rows.length,
    family_cells: familyCells.length,
    strict_frames: strictRows.length,
    strict_family_cells: strictFamilyCells.length,
    terminal_count: rows.filter((row) => String(row.terminal_after_branch).toLowerCase() === "true").length,
    continuing_count: rows.filter((row) => String(row.terminal_after_branch).toLowerCase() !== "true").length,
    source_tiers: countBy(rows, "source_tier_reearned"),
    objects: unique(rows, "object").join(" "),
  });
}

const prev235Rows = frames.filter((row) => row.prev_before_002 === "235" && row.branch_after_390 === "125");
const inFrameTail632 = tail632Rows.filter((row) => row.has_002390125_frame === "yes");
const branch705 = frames.filter((row) => row.branch_after_390 === "705");

function strictCount(rows) {
  return rows.filter((row) => row.strict_countable === "yes").length;
}

const decisions = [
  {
    decision: "quarantined_artifact_not_used",
    evidence: "campaign_032_002_861_002390x_source_normalized_family_collapse*",
    result: "not imported, not read, not cited as settled",
    consequence: "this replacement collapse is re-earned from branch_sign_ecology frames and metadata_filtered.csv",
  },
  {
    decision: "235_002390125_subframe_demoted",
    evidence: prev235Rows.map((row) => `${row.object}:${row.source_tier_reearned}:${row.text}`).join(" | "),
    result: `${prev235Rows.length} raw rows, ${unique(prev235Rows, "family_key_reearned").length} family cells, ${strictCount(prev235Rows)} strict rows`,
    consequence: "one strict source-visible witness plus one weak/non-strict witness cannot promote a subframe",
  },
  {
    decision: "125_632_032_tail_family_pressure",
    evidence: tail632Rows.map((row) => `${row.object}:${row.has_002390125_frame}:${row.source_tier_reearned}:${row.text}`).join(" | "),
    result: `${tail632Rows.length} global rows with 125-632-032; ${inFrameTail632.length} are inside 002-390-125; ${strictCount(inFrameTail632)} strict in-frame rows`,
    consequence: "tail formula pressure increases; it does not prove independent branch function",
  },
  {
    decision: "705_repeated_branch_contacts_pending_zero_strict",
    evidence: branch705.map((row) => `${row.object}:${row.source_tier_reearned}:${row.text}`).join(" | "),
    result: `${branch705.length} raw rows, ${strictCount(branch705)} strict rows`,
    consequence: "Dholavira and M-1825 requests are pending; repeated terminal 705 remains acquisition ecology only",
  },
  {
    decision: "strict_family_core_unmatched",
    evidence: frames
      .filter((row) => row.strict_countable === "yes")
      .map((row) => `${row.object}:${row.prev_before_002}->${row.branch_after_390}->${row.tail_after_branch}`)
      .join(" | "),
    result: "strict rows preserve polarity but no strict same-predecessor branch split",
    consequence: "no grammar/function/value promotion",
  },
];

writeCsv(path.join(reportsDir, `${prefix}_frames.csv`), frames, [
  "id",
  "object",
  "site",
  "type",
  "symbol",
  "cult",
  "shape",
  "prev_before_002",
  "branch_after_390",
  "tail_after_branch",
  "terminal_after_branch",
  "source_status_reearned",
  "source_tier_reearned",
  "strict_countable",
  "family_key_reearned",
  "text",
]);

writeCsv(path.join(reportsDir, `${prefix}_branch_summary.csv`), branchSummary, [
  "branch_after_390",
  "raw_frames",
  "family_cells",
  "strict_frames",
  "strict_family_cells",
  "terminal_count",
  "continuing_count",
  "source_tiers",
  "objects",
]);

writeCsv(path.join(reportsDir, `${prefix}_prev235_rows.csv`), prev235Rows, [
  "id",
  "object",
  "prev_before_002",
  "branch_after_390",
  "tail_after_branch",
  "source_status_reearned",
  "source_tier_reearned",
  "strict_countable",
  "family_key_reearned",
  "text",
]);

writeCsv(path.join(reportsDir, `${prefix}_tail_125632032_rows.csv`), tail632Rows, [
  "id",
  "object",
  "site",
  "type",
  "symbol",
  "cult",
  "shape",
  "pos_125_1based",
  "has_002390125_frame",
  "source_status_reearned",
  "source_tier_reearned",
  "strict_countable",
  "text",
]);

writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  "decision",
  "evidence",
  "result",
  "consequence",
]);

const summary = {
  run_date: "2026-05-31",
  status: "reearned_family_collapse_demotes_subframes_no_values",
  inputs: {
    frames: path.relative(root, framesPath).replaceAll("\\", "/"),
    metadata: path.relative(root, metadataPath).replaceAll("\\", "/"),
    quarantined_artifact_used: false,
  },
  counts: {
    frames: frames.length,
    branches: branchSummary.length,
    prev235_rows: prev235Rows.length,
    prev235_strict_rows: strictCount(prev235Rows),
    tail_125632032_global_rows: tail632Rows.length,
    tail_125632032_inframe_rows: inFrameTail632.length,
    tail_125632032_inframe_strict_rows: strictCount(inFrameTail632),
    branch705_rows: branch705.length,
    branch705_strict_rows: strictCount(branch705),
  },
  decisions,
  accepted: {
    value: 0,
    phonetics: 0,
    language_identity: 0,
    function: 0,
    sign_meaning: 0,
    translation: 0,
  },
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
