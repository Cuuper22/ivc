import fs from "node:fs";
import path from "node:path";

// The strongest evidence for real grammar would be a matched-predecessor split: two 002-390
// frames with the SAME sign before the 002 but DIFFERENT branch signs after the 390, both
// strict source-visible. This script checks whether any predecessor group clears that bar.
// It reads the 002-390 frames report CSV from reports/, maps each frame's source_status onto
// a five-level tier ladder (strict_visible down to metadata_or_blocked), and groups frames
// by their predecessor sign. Each group gets a gate label: a strict split needs two or more
// strict rows with different branches; weaker groups are "partly strict blocked",
// "non-strict only", tail-splits, or singletons. The recorded outcome: no strict split
// exists anywhere — the 004 lane waits on H-1993 and Sktd-1, the 032 lane on 3335.1, and
// the 235 group splits only in the tail, not the branch. Writes the tiered rows, the
// per-predecessor summary, and the decisions as CSVs plus a summary JSON in reports/.

const root = process.cwd();
const reportsDir = path.join(root, "data", "open_prototype", "reports");
const framesPath = path.join(reportsDir, "campaign_032_002_861_002390x_branch_sign_ecology_20260531_002390_frames.csv");
const prefix = "campaign_032_002_861_002390x_source_tiered_prev_gate_20260531";

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

function csvEscape(value) {
  const s = String(value ?? "");
  return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

function writeCsv(filePath, rows, headers) {
  const lines = [headers.join(",")];
  for (const row of rows) {
    lines.push(headers.map((h) => csvEscape(row[h])).join(","));
  }
  fs.writeFileSync(filePath, `${lines.join("\n")}\n`);
}

function sourceTier(row) {
  const status = row.source_status || "";
  if (status.includes("checkpoint_strict_source_visible") || status.includes("strict_source_visible")) {
    return "strict_visible";
  }
  if (status.includes("source_panel_acquired") || status.includes("boxed_window_compatible")) {
    return "panel_bound_not_strict";
  }
  if (status.includes("checkpoint_permissive") || status.includes("public_panel")) {
    return "public_panel_downweighted";
  }
  if (status.includes("source_route") || status.includes("supplement") || status.includes("dholavira") || status.includes("m1825")) {
    return "route_or_metadata_pressure";
  }
  return "metadata_or_blocked";
}

function terminalLabel(row) {
  return String(row.terminal_after_branch).toLowerCase() === "true" ? "terminal" : "continuing";
}

const frames = parseCsv(fs.readFileSync(framesPath, "utf8")).map((row) => ({
  ...row,
  source_tier: sourceTier(row),
  terminal_class: terminalLabel(row),
  strict_countable: sourceTier(row) === "strict_visible" ? "yes" : "no",
}));

const tierRank = {
  strict_visible: 4,
  panel_bound_not_strict: 3,
  public_panel_downweighted: 2,
  route_or_metadata_pressure: 1,
  metadata_or_blocked: 0,
};

const prevGroups = new Map();
for (const row of frames) {
  const prev = row.prev_before_002 || "<NONE>";
  if (!prevGroups.has(prev)) prevGroups.set(prev, []);
  prevGroups.get(prev).push(row);
}

const prevSummary = [];
for (const [prev, rows] of [...prevGroups.entries()].sort(([a], [b]) => a.localeCompare(b))) {
  const branches = [...new Set(rows.map((r) => r.branch_after_390))].sort();
  const strictRows = rows.filter((r) => r.source_tier === "strict_visible");
  const topTierRows = rows.filter((r) => tierRank[r.source_tier] === Math.max(...rows.map((r) => tierRank[r.source_tier])));
  const branchTail = rows
    .map((r) => `${r.branch_after_390}->${r.tail_after_branch || "<END>"}:${r.terminal_class}:${r.object}:${r.source_tier}`)
    .join("; ");
  let gate = "singleton_prev_no_matched_branch_test";
  if (branches.length > 1 && strictRows.length >= 2 && new Set(strictRows.map((r) => r.branch_after_390)).size > 1) {
    gate = "matched_prev_strict_split_found";
  } else if (branches.length > 1 && strictRows.length > 0) {
    gate = "matched_prev_split_partly_strict_blocked";
  } else if (branches.length > 1) {
    gate = "matched_prev_split_non_strict_only";
  } else if (rows.length > 1) {
    gate = "same_prev_same_branch_tail_split";
  }
  prevSummary.push({
    prev_before_002: prev,
    rows: rows.length,
    branches: branches.join(" "),
    terminal_classes: [...new Set(rows.map((r) => r.terminal_class))].sort().join(" "),
    strict_objects: strictRows.map((r) => r.object).join(" "),
    top_tier: topTierRows[0]?.source_tier ?? "",
    top_tier_objects: topTierRows.map((r) => r.object).join(" "),
    branch_tail_source: branchTail,
    gate,
  });
}

const strictRows = frames.filter((r) => r.source_tier === "strict_visible");
const strictPrevGroups = new Map();
for (const row of strictRows) {
  const prev = row.prev_before_002 || "<NONE>";
  if (!strictPrevGroups.has(prev)) strictPrevGroups.set(prev, []);
  strictPrevGroups.get(prev).push(row);
}

const decisions = [
  {
    decision: "strict_core_has_no_matched_predecessor_split",
    evidence: strictRows
      .map((r) => `${r.object}:${r.prev_before_002}->002-390->${r.branch_after_390}->${r.tail_after_branch || "<END>"}:${r.terminal_class}`)
      .join("; "),
    result: [...strictPrevGroups.values()].every((rows) => new Set(rows.map((r) => r.branch_after_390)).size === 1)
      ? "no strict source-visible predecessor group has two branch alternatives"
      : "strict matched split exists",
    consequence: "branch-tail polarity remains real pressure but not a matched source-controlled contrast",
  },
  {
    decision: "004_split_blocked",
    evidence: prevSummary.find((r) => r.prev_before_002 === "004")?.branch_tail_source ?? "",
    result: prevSummary.find((r) => r.prev_before_002 === "004")?.gate ?? "",
    consequence: "H-1993 image binding and Sktd-1 side/panel strictness are both required before using the 004 split",
  },
  {
    decision: "032_split_blocked",
    evidence: prevSummary.find((r) => r.prev_before_002 === "032")?.branch_tail_source ?? "",
    result: prevSummary.find((r) => r.prev_before_002 === "032")?.gate ?? "",
    consequence: "M-70 is strict, but 3335.1 is object-ID blocked and formula-family pressured",
  },
  {
    decision: "235_tail_split_not_branch_split",
    evidence: prevSummary.find((r) => r.prev_before_002 === "235")?.branch_tail_source ?? "",
    result: prevSummary.find((r) => r.prev_before_002 === "235")?.gate ?? "",
    consequence: "M-735 is strict and M-38 is weak, but both are branch 125; this tests tail subframes, not branch alternation",
  },
  {
    decision: "h773_does_not_rescue_matched_split",
    evidence: prevSummary.find((r) => r.prev_before_002 === "803")?.branch_tail_source ?? "",
    result: "singleton predecessor and panel_bound_not_strict",
    consequence: "H-773 remains useful anti-lazy pressure but cannot be a matched strict anti-125 exception",
  },
];

writeCsv(
  path.join(reportsDir, `${prefix}_rows.csv`),
  frames,
  [
    "id",
    "object",
    "site",
    "type",
    "prev_before_002",
    "branch_after_390",
    "tail_after_branch",
    "terminal_class",
    "source_status",
    "source_tier",
    "strict_countable",
    "text",
  ],
);

writeCsv(
  path.join(reportsDir, `${prefix}_prev_summary.csv`),
  prevSummary,
  [
    "prev_before_002",
    "rows",
    "branches",
    "terminal_classes",
    "strict_objects",
    "top_tier",
    "top_tier_objects",
    "branch_tail_source",
    "gate",
  ],
);

writeCsv(
  path.join(reportsDir, `${prefix}_decisions.csv`),
  decisions,
  ["decision", "evidence", "result", "consequence"],
);

const summary = {
  run_date: "2026-05-31",
  input: path.relative(root, framesPath).replace(/\\/g, "/"),
  total_frames: frames.length,
  strict_visible_rows: strictRows.length,
  strict_visible_objects: strictRows.map((r) => r.object),
  matched_prev_groups: prevSummary.filter((r) => r.rows > 1),
  matched_prev_strict_splits: prevSummary.filter((r) => r.gate === "matched_prev_strict_split_found"),
  decisions,
  outputs: {
    rows: `data/open_prototype/reports/${prefix}_rows.csv`,
    prev_summary: `data/open_prototype/reports/${prefix}_prev_summary.csv`,
    decisions: `data/open_prototype/reports/${prefix}_decisions.csv`,
    summary: `data/open_prototype/reports/${prefix}_summary.json`,
  },
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
