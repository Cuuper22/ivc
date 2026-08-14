import fs from "node:fs";
import path from "node:path";

// How much left context does it take before 002-390-X frames with the same context stop
// disagreeing about the branch sign X? This script scans every radius. It reads the
// target-controls report CSV produced by the full-left formula-controls script (each row is
// one 002-390 frame with its full left prefix, branch, and source_status, which is mapped
// to a source tier such as strict_visible). For each radius r from 1 up to the longest
// prefix, it groups the frames by their last r left signs and marks each group: does it
// contain more than one branch (a branch split), and is that split witnessed by at least two
// strict source-visible rows? The recorded outcome: branch splits exist only at radius 1
// (predecessors 004 and 032), none survive widening to radius 2, and no split is strict
// source-visible — so the branch paradigm stays blocked. Writes per-target radius rows,
// group rows, a per-radius summary, and a decisions table as CSVs plus a summary JSON in
// reports/.

const root = process.cwd();
const reportsDir = path.join(root, "data", "open_prototype", "reports");
const targetControlsPath = path.join(
  reportsDir,
  "campaign_032_002_861_002390x_full_left_formula_controls_20260531_target_controls.csv",
);
const prefix = "campaign_032_002_861_002390x_left_context_radius_scan_20260531";

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
  if (
    status.includes("source_route") ||
    status.includes("supplement") ||
    status.includes("dholavira") ||
    status.includes("m1825")
  ) {
    return "route_or_metadata_pressure";
  }
  return "metadata_or_blocked";
}

function signs(value) {
  if (!value || value === "<START>") return [];
  return String(value).split(/\s+/).filter(Boolean);
}

function distribution(rows, field) {
  const counts = new Map();
  for (const row of rows) counts.set(row[field], (counts.get(row[field]) ?? 0) + 1);
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([value, count]) => `${value}:${count}`)
    .join("; ");
}

function objectList(rows) {
  return rows
    .map((r) => `${r.object || "-"}:${r.branch_after_390}->${r.tail_after_branch || "<END>"}:${r.source_tier}`)
    .join("; ");
}

const targets = parseCsv(fs.readFileSync(targetControlsPath, "utf8")).map((row) => ({
  ...row,
  full_left_signs: signs(row.full_left),
  source_tier: sourceTier(row),
  terminal_class: row.terminal_after_branch === "yes" ? "terminal" : "continuing",
}));

const maxRadius = Math.max(...targets.map((row) => row.full_left_signs.length));
const groupRows = [];
const targetRadiusRows = [];

for (let radius = 1; radius <= maxRadius; radius++) {
  const groups = new Map();
  for (const row of targets) {
    if (row.full_left_signs.length < radius) continue;
    const key = row.full_left_signs.slice(-radius).join(" ");
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(row);
    targetRadiusRows.push({
      id: row.id,
      object: row.object,
      radius,
      left_suffix: key,
      full_left: row.full_left,
      branch_after_390: row.branch_after_390,
      tail_after_branch: row.tail_after_branch,
      terminal_class: row.terminal_class,
      source_tier: row.source_tier,
      source_status: row.source_status,
      text: row.text,
    });
  }

  for (const [key, rows] of [...groups.entries()].sort(([a], [b]) => a.localeCompare(b))) {
    const branches = new Set(rows.map((row) => row.branch_after_390));
    const strictRows = rows.filter((row) => row.source_tier === "strict_visible");
    const strictBranches = new Set(strictRows.map((row) => row.branch_after_390));
    let gate = "singleton_context_no_branch_test";
    if (rows.length > 1 && branches.size > 1 && strictRows.length >= 2 && strictBranches.size > 1) {
      gate = "strict_source_visible_context_branch_split";
    } else if (rows.length > 1 && branches.size > 1 && strictRows.length > 0) {
      gate = "context_branch_split_partly_strict_blocked";
    } else if (rows.length > 1 && branches.size > 1) {
      gate = "context_branch_split_non_strict_only";
    } else if (rows.length > 1) {
      gate = "same_context_same_branch_tail_split";
    }
    groupRows.push({
      radius,
      left_suffix: key,
      rows: rows.length,
      branches: distribution(rows, "branch_after_390"),
      terminal_classes: distribution(rows, "terminal_class"),
      source_tiers: distribution(rows, "source_tier"),
      strict_objects: strictRows.map((row) => row.object || "-").join(" "),
      strict_branches: strictRows.length ? distribution(strictRows, "branch_after_390") : "",
      objects: objectList(rows),
      gate,
    });
  }
}

const radiusSummary = [];
for (let radius = 1; radius <= maxRadius; radius++) {
  const rows = groupRows.filter((row) => row.radius === radius);
  const branchSplitRows = rows.filter((row) => row.gate.includes("branch_split"));
  const strictSplitRows = rows.filter((row) => row.gate === "strict_source_visible_context_branch_split");
  radiusSummary.push({
    radius,
    groups: rows.length,
    multirow_groups: rows.filter((row) => Number(row.rows) > 1).length,
    branch_split_groups: branchSplitRows.length,
    strict_branch_split_groups: strictSplitRows.length,
    branch_split_keys: branchSplitRows.map((row) => `${row.left_suffix}(${row.branches})`).join(" | "),
    strict_branch_split_keys: strictSplitRows.map((row) => `${row.left_suffix}(${row.strict_branches})`).join(" | "),
  });
}

const branchSplitGroups = groupRows.filter((row) => row.gate.includes("branch_split"));
const strictBranchSplitGroups = groupRows.filter((row) => row.gate === "strict_source_visible_context_branch_split");
const immediateBranchSplits = branchSplitGroups.filter((row) => row.radius === 1);
const broaderBranchSplits = branchSplitGroups.filter((row) => row.radius > 1);
const prev235 = groupRows.find((row) => row.radius === 1 && row.left_suffix === "235");

const decisions = [
  {
    decision: "branch_splits_exist_only_at_immediate_predecessor_radius",
    evidence: immediateBranchSplits.map((row) => `${row.left_suffix}->${row.branches}:${row.gate}`).join(" | "),
    result: `${immediateBranchSplits.length} immediate-predecessor branch-split groups; ${broaderBranchSplits.length} branch-split groups at radius >= 2`,
    consequence: "branch alternatives vanish once the left context is widened beyond one sign",
  },
  {
    decision: "no_strict_source_visible_radius_branch_split",
    evidence: strictBranchSplitGroups.map((row) => `${row.left_suffix}->${row.strict_branches}`).join(" | "),
    result: `${strictBranchSplitGroups.length} strict source-visible branch-split groups across all radii`,
    consequence: "the radius scan preserves the grammar/function promotion block",
  },
  {
    decision: "004_and_032_remain_the_only_live_branch_split_lanes",
    evidence: immediateBranchSplits
      .filter((row) => ["004", "032"].includes(row.left_suffix))
      .map((row) => `${row.left_suffix}: ${row.objects}`)
      .join(" | "),
    result: "the only branch-split lanes are the already-known 004 and 032 predecessor groups",
    consequence: "H-1993/Sktd-1 and M-70/3335.1 remain the decisive matched-predecessor tests",
  },
  {
    decision: "235_group_is_tail_split_not_branch_split",
    evidence: prev235?.objects ?? "",
    result: prev235?.gate ?? "235 group absent",
    consequence: "M-38/M-735 cannot prove branch alternation because both choose branch 125",
  },
  {
    decision: "exact_and_last2_controls_do_not_rescue_branch_paradigm",
    evidence: radiusSummary
      .filter((row) => Number(row.radius) >= 2)
      .map((row) => `r${row.radius}:branch_splits=${row.branch_split_groups}`)
      .join("; "),
    result: "no radius >= 2 contains a branch-split group",
    consequence: "full-left anti-template pressure is real, but matched branch paradigms remain absent",
  },
];

writeCsv(
  path.join(reportsDir, `${prefix}_target_radius_rows.csv`),
  targetRadiusRows,
  [
    "id",
    "object",
    "radius",
    "left_suffix",
    "full_left",
    "branch_after_390",
    "tail_after_branch",
    "terminal_class",
    "source_tier",
    "source_status",
    "text",
  ],
);

writeCsv(
  path.join(reportsDir, `${prefix}_groups.csv`),
  groupRows,
  [
    "radius",
    "left_suffix",
    "rows",
    "branches",
    "terminal_classes",
    "source_tiers",
    "strict_objects",
    "strict_branches",
    "objects",
    "gate",
  ],
);

writeCsv(
  path.join(reportsDir, `${prefix}_radius_summary.csv`),
  radiusSummary,
  [
    "radius",
    "groups",
    "multirow_groups",
    "branch_split_groups",
    "strict_branch_split_groups",
    "branch_split_keys",
    "strict_branch_split_keys",
  ],
);

writeCsv(
  path.join(reportsDir, `${prefix}_decisions.csv`),
  decisions,
  ["decision", "evidence", "result", "consequence"],
);

const summary = {
  run_date: "2026-05-31",
  input: path.relative(root, targetControlsPath).replace(/\\/g, "/"),
  target_002390_frames: targets.length,
  max_left_context_radius: maxRadius,
  branch_split_groups_total: branchSplitGroups.length,
  immediate_predecessor_branch_split_groups: immediateBranchSplits.length,
  radius_ge_2_branch_split_groups: broaderBranchSplits.length,
  strict_source_visible_branch_split_groups: strictBranchSplitGroups.length,
  branch_split_lanes: immediateBranchSplits.map((row) => ({
    radius: row.radius,
    left_suffix: row.left_suffix,
    branches: row.branches,
    gate: row.gate,
    objects: row.objects,
  })),
  decisions,
  status: "left_context_radius_scan_immediate_splits_source_blocked_no_values",
  outputs: {
    target_radius_rows: `data/open_prototype/reports/${prefix}_target_radius_rows.csv`,
    groups: `data/open_prototype/reports/${prefix}_groups.csv`,
    radius_summary: `data/open_prototype/reports/${prefix}_radius_summary.csv`,
    decisions: `data/open_prototype/reports/${prefix}_decisions.csv`,
    summary: `data/open_prototype/reports/${prefix}_summary.json`,
  },
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
