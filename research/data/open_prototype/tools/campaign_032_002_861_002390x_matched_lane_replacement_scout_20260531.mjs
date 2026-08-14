import fs from "node:fs";
import path from "node:path";

// Only two predecessor "lanes" — sign 004 or 032 immediately before a 002-390 frame — still
// show branch alternation, and each lane has a weak side that is not strict source-visible.
// This script scouts the local corpus for replacement witnesses before anyone spends effort
// on external image acquisition. It reads data/open_prototype/lipi/metadata_filtered.csv and
// the 002-390 frames report (for source_status, mapped to tiers like strict_visible), then
// collects every 002 occurrence whose predecessor is 004 or 032. Per lane it summarizes the
// post-002 heads, the adjacent 002-390 branches, and how many of those rows are strict, and
// lists the rows that would need upgrading or replacing. The recorded outcome: the local
// corpus offers no replacement witness for either lane, so H-1993 (for 004) and binding
// 3335.1 (for 032) remain the decisive external targets. Writes lane occurrences, lane
// summaries, replacement targets, and decisions as CSVs plus a summary JSON in reports/.

const root = process.cwd();
const dataPath = path.join(root, "data", "open_prototype", "lipi", "metadata_filtered.csv");
const reportsDir = path.join(root, "data", "open_prototype", "reports");
const framesPath = path.join(reportsDir, "campaign_032_002_861_002390x_branch_sign_ecology_20260531_002390_frames.csv");
const prefix = "campaign_032_002_861_002390x_matched_lane_replacement_scout_20260531";
const livePredecessors = new Set(["004", "032"]);

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

function signs(text) {
  return [...String(text || "").matchAll(/\d{3}/g)].map((m) => m[0]);
}

function rowObject(row) {
  return row.cisi || row.object || row.id || "";
}

function sourceTier(status) {
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

function terminalClass(is002390, index, toks) {
  if (!is002390) return "<NOT_002390>";
  return index + 2 === toks.length - 1 ? "terminal" : "continuing";
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
    .map((row) => `${row.object || "-"}:${row.after_002_head}->${row.branch_after_390}/${row.tail_after_branch}:${row.source_tier}`)
    .join("; ");
}

const metadata = parseCsv(fs.readFileSync(dataPath, "utf8"));
const frames = parseCsv(fs.readFileSync(framesPath, "utf8"));
const sourceById = new Map(frames.map((row) => [row.id, row.source_status]));

const occurrences = [];
for (const row of metadata) {
  const toks = signs(row.text);
  for (let i = 0; i < toks.length; i++) {
    if (toks[i] !== "002") continue;
    const prev = toks[i - 1] ?? "<START>";
    if (!livePredecessors.has(prev)) continue;
    const afterHead = toks[i + 1] ?? "<END>";
    const is002390 = afterHead === "390";
    const sourceStatus = sourceById.get(row.id) ?? "not_in_adjacent_002390_frame_local_metadata_only";
    occurrences.push({
      id: row.id,
      object: rowObject(row),
      site: row.site,
      type: row.type,
      symbol: row.symbol,
      cult: row.cult,
      prev_before_002: prev,
      after_002_head: afterHead,
      after_002_tail: toks.slice(i + 1).join(" ") || "<END>",
      is_adjacent_002390: is002390 ? "yes" : "no",
      branch_after_390: is002390 ? (toks[i + 2] ?? "<END>") : "<NOT_002390>",
      tail_after_branch: is002390 ? (toks.slice(i + 3).join(" ") || "<END>") : "<NOT_002390>",
      terminal_class: terminalClass(is002390, i, toks),
      source_status: sourceStatus,
      source_tier: is002390 ? sourceTier(sourceStatus) : "not_adjacent_002390",
      text: row.text,
    });
  }
}

const laneSummary = [];
for (const prev of [...livePredecessors].sort()) {
  const rows = occurrences.filter((row) => row.prev_before_002 === prev);
  const adjacent = rows.filter((row) => row.is_adjacent_002390 === "yes");
  const strictAdjacent = adjacent.filter((row) => row.source_tier === "strict_visible");
  const branches = new Set(adjacent.map((row) => row.branch_after_390));
  const strictBranches = new Set(strictAdjacent.map((row) => row.branch_after_390));
  const nonAdjacentHeads = rows.filter((row) => row.is_adjacent_002390 === "no");
  let gate = "no_adjacent_002390_lane";
  if (adjacent.length && branches.size > 1 && strictBranches.size > 1) {
    gate = "strict_replacement_branch_split_found";
  } else if (adjacent.length && branches.size > 1 && strictAdjacent.length > 0) {
    gate = "branch_split_partly_strict_no_replacement";
  } else if (adjacent.length && branches.size > 1) {
    gate = "branch_split_non_strict_no_replacement";
  } else if (adjacent.length > 1) {
    gate = "same_branch_or_tail_split_no_replacement";
  } else if (adjacent.length === 1) {
    gate = "singleton_adjacent_002390_no_replacement";
  }
  laneSummary.push({
    prev_before_002: prev,
    all_prev_002_occurrences: rows.length,
    post_002_heads_all: distribution(rows, "after_002_head"),
    non_adjacent_post_002_heads: distribution(nonAdjacentHeads, "after_002_head"),
    adjacent_002390_rows: adjacent.length,
    adjacent_002390_branches: distribution(adjacent, "branch_after_390"),
    adjacent_002390_terminal_classes: distribution(adjacent, "terminal_class"),
    adjacent_source_tiers: distribution(adjacent, "source_tier"),
    strict_adjacent_rows: strictAdjacent.length,
    strict_adjacent_branches: distribution(strictAdjacent, "branch_after_390"),
    adjacent_objects: objectList(adjacent),
    gate,
  });
}

const adjacentRows = occurrences.filter((row) => row.is_adjacent_002390 === "yes");
const replacementRows = [];
for (const prev of livePredecessors) {
  const adjacent = adjacentRows.filter((row) => row.prev_before_002 === prev);
  const strictBranches = new Set(adjacent.filter((row) => row.source_tier === "strict_visible").map((row) => row.branch_after_390));
  const nonStrictBranches = new Set(adjacent.filter((row) => row.source_tier !== "strict_visible").map((row) => row.branch_after_390));
  if (strictBranches.size > 0 && nonStrictBranches.size > 0) {
    for (const row of adjacent.filter((r) => r.source_tier !== "strict_visible")) {
      replacementRows.push({
        ...row,
        needed_upgrade: "bind_this_row_or_replace_with_strict_same_prev_branch_alternative",
      });
    }
  } else if (strictBranches.size === 0) {
    for (const row of adjacent) {
      replacementRows.push({
        ...row,
        needed_upgrade: "lane_has_no_strict_side_bind_or_replace_any_branch",
      });
    }
  }
}

const decisions = [
  {
    decision: "no_local_replacement_witness_for_004_or_032",
    evidence: laneSummary.map((row) => `${row.prev_before_002}:${row.adjacent_objects}`).join(" | "),
    result: "local metadata has no additional adjacent 002-390 branch rows for either live predecessor lane",
    consequence: "the next matched-lane work is external/source acquisition or replacement discovery, not local row re-ranking",
  },
  {
    decision: "004_lane_requires_h1993_or_equivalent",
    evidence: laneSummary.find((row) => row.prev_before_002 === "004")?.adjacent_objects ?? "",
    result: laneSummary.find((row) => row.prev_before_002 === "004")?.gate ?? "",
    consequence: "Sktd-1 cannot be promoted without a strict non-125 comparator; H-1993 remains the named acquisition target",
  },
  {
    decision: "032_lane_requires_3335_binding_or_equivalent",
    evidence: laneSummary.find((row) => row.prev_before_002 === "032")?.adjacent_objects ?? "",
    result: laneSummary.find((row) => row.prev_before_002 === "032")?.gate ?? "",
    consequence: "M-70 is already strict; the blocked side is 3335.1 or another strict 032->002-390 branch alternative",
  },
  {
    decision: "post002_head_alternation_is_not_branch_replacement",
    evidence: laneSummary.map((row) => `${row.prev_before_002}:all_heads=${row.post_002_heads_all}`).join(" | "),
    result: "both live predecessors have non-390 post-002 heads in local metadata, but those are not adjacent 002-390-X branch alternatives",
    consequence: "head-level anti-template controls stay separate from branch-slot promotion",
  },
];

writeCsv(
  path.join(reportsDir, `${prefix}_lane_occurrences.csv`),
  occurrences,
  [
    "id",
    "object",
    "site",
    "type",
    "symbol",
    "cult",
    "prev_before_002",
    "after_002_head",
    "after_002_tail",
    "is_adjacent_002390",
    "branch_after_390",
    "tail_after_branch",
    "terminal_class",
    "source_status",
    "source_tier",
    "text",
  ],
);

writeCsv(
  path.join(reportsDir, `${prefix}_lane_summary.csv`),
  laneSummary,
  [
    "prev_before_002",
    "all_prev_002_occurrences",
    "post_002_heads_all",
    "non_adjacent_post_002_heads",
    "adjacent_002390_rows",
    "adjacent_002390_branches",
    "adjacent_002390_terminal_classes",
    "adjacent_source_tiers",
    "strict_adjacent_rows",
    "strict_adjacent_branches",
    "adjacent_objects",
    "gate",
  ],
);

writeCsv(
  path.join(reportsDir, `${prefix}_replacement_targets.csv`),
  replacementRows,
  [
    "id",
    "object",
    "site",
    "type",
    "prev_before_002",
    "after_002_head",
    "branch_after_390",
    "tail_after_branch",
    "terminal_class",
    "source_status",
    "source_tier",
    "needed_upgrade",
    "text",
  ],
);

writeCsv(
  path.join(reportsDir, `${prefix}_decisions.csv`),
  decisions,
  ["decision", "evidence", "result", "consequence"],
);

const summary = {
  run_date: "2026-05-31",
  input: path.relative(root, dataPath).replace(/\\/g, "/"),
  live_predecessors: [...livePredecessors].sort(),
  lane_occurrences: occurrences.length,
  adjacent_002390_lane_rows: adjacentRows.length,
  replacement_targets: replacementRows.map((row) => ({
    id: row.id,
    object: row.object,
    prev_before_002: row.prev_before_002,
    branch_after_390: row.branch_after_390,
    source_tier: row.source_tier,
    needed_upgrade: row.needed_upgrade,
  })),
  lane_summary: laneSummary,
  decisions,
  status: "matched_lane_replacement_scout_no_local_replacement_witness_no_values",
  outputs: {
    lane_occurrences: `data/open_prototype/reports/${prefix}_lane_occurrences.csv`,
    lane_summary: `data/open_prototype/reports/${prefix}_lane_summary.csv`,
    replacement_targets: `data/open_prototype/reports/${prefix}_replacement_targets.csv`,
    decisions: `data/open_prototype/reports/${prefix}_decisions.csv`,
    summary: `data/open_prototype/reports/${prefix}_summary.json`,
  },
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
