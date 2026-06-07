import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const reportsDir = path.join(root, "data", "open_prototype", "reports");
const framesPath = path.join(reportsDir, "campaign_032_002_861_002390x_branch_sign_ecology_20260531_002390_frames.csv");
const prefix = "campaign_032_002_861_002390x_source_upgrade_impact_audit_20260531";

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
  for (const row of rows) lines.push(headers.map((h) => csvEscape(row[h])).join(","));
  fs.writeFileSync(filePath, `${lines.join("\n")}\n`);
}

function baseSourceTier(row) {
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

function terminalClass(row) {
  return String(row.terminal_after_branch).toLowerCase() === "true" ? "terminal" : "continuing";
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
    .map((row) => `${row.object || "-"}:${row.prev_before_002}->${row.branch_after_390}->${row.tail_after_branch || "<END>"}:${row.terminal_class}`)
    .join("; ");
}

const frames = parseCsv(fs.readFileSync(framesPath, "utf8")).map((row) => ({
  ...row,
  base_source_tier: baseSourceTier(row),
  terminal_class: terminalClass(row),
}));

const scenarios = [
  {
    scenario: "baseline_current_strict_core",
    upgraded_ids: [],
    purpose: "current strict source-visible state",
  },
  {
    scenario: "upgrade_h1993_only",
    upgraded_ids: ["744.2"],
    purpose: "test whether H-1993 image binding alone unlocks the 004 split",
  },
  {
    scenario: "upgrade_sktd1_only",
    upgraded_ids: ["3875.1"],
    purpose: "test whether Sktd-1 strict token/order alone unlocks the 004 split",
  },
  {
    scenario: "upgrade_h1993_and_sktd1",
    upgraded_ids: ["744.2", "3875.1"],
    purpose: "test full 004 strict split",
  },
  {
    scenario: "upgrade_3335_1",
    upgraded_ids: ["3335.1"],
    purpose: "test whether the 032 split unlocks because M-70 is already strict",
  },
  {
    scenario: "upgrade_m1825_only",
    upgraded_ids: ["3992.1"],
    purpose: "test one strict 705 terminal witness",
  },
  {
    scenario: "upgrade_dholavira_4237_1_only",
    upgraded_ids: ["4237.1"],
    purpose: "test one strict Dholavira 705 terminal witness",
  },
  {
    scenario: "upgrade_m1825_and_dholavira_705_pair",
    upgraded_ids: ["3992.1", "4237.1"],
    purpose: "test repeated strict 705 terminal ecology",
  },
  {
    scenario: "upgrade_m38",
    upgraded_ids: ["2566.1"],
    purpose: "test 235 same-branch tail split with both M-38 and M-735 strict",
  },
  {
    scenario: "upgrade_h773",
    upgraded_ids: ["1665.1"],
    purpose: "test strict non-125 continuing exception",
  },
  {
    scenario: "upgrade_all_named_blockers",
    upgraded_ids: ["744.2", "3875.1", "3335.1", "3992.1", "4237.1", "2566.1", "1665.1"],
    purpose: "upper-bound audit if all currently named blockers became strict",
  },
];

const scenarioRows = [];
const prevGroupRows = [];
const branchRows = [];

function applyScenario(scenario) {
  const upgraded = new Set(scenario.upgraded_ids);
  return frames.map((row) => ({
    ...row,
    scenario: scenario.scenario,
    scenario_source_tier: upgraded.has(row.id) ? "strict_visible" : row.base_source_tier,
    scenario_upgraded: upgraded.has(row.id) ? "yes" : "no",
  }));
}

for (const scenario of scenarios) {
  const rows = applyScenario(scenario);
  const strictRows = rows.filter((row) => row.scenario_source_tier === "strict_visible");
  const strictNon125Continuing = strictRows.filter((row) => row.branch_after_390 !== "125" && row.terminal_class === "continuing");
  const strict705 = strictRows.filter((row) => row.branch_after_390 === "705");
  const strict705Terminal = strict705.filter((row) => row.terminal_class === "terminal");
  const strict125Continuing = strictRows.filter((row) => row.branch_after_390 === "125" && row.terminal_class === "continuing");
  const prevGroups = new Map();
  for (const row of strictRows) {
    const prev = row.prev_before_002 || "<NONE>";
    if (!prevGroups.has(prev)) prevGroups.set(prev, []);
    prevGroups.get(prev).push(row);
  }

  const strictSplitGroups = [];
  for (const [prev, groupRows] of [...prevGroups.entries()].sort(([a], [b]) => a.localeCompare(b))) {
    const branchCount = new Set(groupRows.map((row) => row.branch_after_390)).size;
    const split = groupRows.length > 1 && branchCount > 1;
    if (split) strictSplitGroups.push({ prev, rows: groupRows });
    prevGroupRows.push({
      scenario: scenario.scenario,
      prev_before_002: prev,
      strict_rows: groupRows.length,
      strict_branches: distribution(groupRows, "branch_after_390"),
      strict_terminal_classes: distribution(groupRows, "terminal_class"),
      strict_objects: objectList(groupRows),
      gate: split ? "strict_matched_predecessor_branch_split" : groupRows.length > 1 ? "strict_same_branch_or_tail_split" : "strict_singleton",
    });
  }

  const branches = new Map();
  for (const row of strictRows) {
    if (!branches.has(row.branch_after_390)) branches.set(row.branch_after_390, []);
    branches.get(row.branch_after_390).push(row);
  }
  for (const [branch, branchGroupRows] of [...branches.entries()].sort(([a], [b]) => a.localeCompare(b))) {
    branchRows.push({
      scenario: scenario.scenario,
      branch_after_390: branch,
      strict_rows: branchGroupRows.length,
      terminal_classes: distribution(branchGroupRows, "terminal_class"),
      prevs: distribution(branchGroupRows, "prev_before_002"),
      objects: objectList(branchGroupRows),
    });
  }

  const unlocks = [];
  if (strictSplitGroups.length) unlocks.push(`strict_matched_prev_split:${strictSplitGroups.map((g) => g.prev).join("/")}`);
  if (strict705Terminal.length === 1) unlocks.push("single_strict_705_terminal");
  if (strict705Terminal.length >= 2) unlocks.push("repeated_strict_705_terminal_pair");
  if (strictNon125Continuing.length) unlocks.push(`strict_non125_continuing:${strictNon125Continuing.map((r) => r.object || r.id).join("/")}`);
  if (strict125Continuing.length >= 3) unlocks.push("expanded_strict_125_continuation_set");
  if (!unlocks.length) unlocks.push("no_new_decisive_gate");

  scenarioRows.push({
    scenario: scenario.scenario,
    upgraded_ids: scenario.upgraded_ids.join(" "),
    purpose: scenario.purpose,
    strict_rows: strictRows.length,
    strict_objects: strictRows.map((row) => row.object || row.id).join(" "),
    strict_matched_prev_split_count: strictSplitGroups.length,
    strict_matched_prev_splits: strictSplitGroups.map((g) => `${g.prev}:${distribution(g.rows, "branch_after_390")}`).join(" | "),
    strict_705_terminal_rows: strict705Terminal.length,
    strict_705_terminal_objects: strict705Terminal.map((row) => row.object || row.id).join(" "),
    strict_non125_continuing_rows: strictNon125Continuing.length,
    strict_non125_continuing_objects: strictNon125Continuing.map((row) => `${row.object || row.id}:${row.branch_after_390}`).join(" "),
    strict_125_continuing_rows: strict125Continuing.length,
    unlocks: unlocks.join("; "),
  });
}

const byScenario = new Map(scenarioRows.map((row) => [row.scenario, row]));
const decisions = [
  {
    decision: "h1993_alone_does_not_unlock_strict_004_split",
    evidence: byScenario.get("upgrade_h1993_only")?.unlocks ?? "",
    result: `strict matched predecessor splits: ${byScenario.get("upgrade_h1993_only")?.strict_matched_prev_split_count ?? ""}`,
    consequence: "H-1993 binding is necessary for the 004 lane but insufficient unless Sktd-1 becomes strict or another strict 004->002-390->125 witness appears",
  },
  {
    decision: "004_lane_needs_dual_strict_sides",
    evidence: byScenario.get("upgrade_h1993_and_sktd1")?.strict_matched_prev_splits ?? "",
    result: byScenario.get("upgrade_h1993_and_sktd1")?.unlocks ?? "",
    consequence: "the 004 lane can unlock only as a dual-side strict upgrade under the current local inventory",
  },
  {
    decision: "3335_1_is_highest_single_object_matched_gate_unlock",
    evidence: byScenario.get("upgrade_3335_1")?.strict_matched_prev_splits ?? "",
    result: byScenario.get("upgrade_3335_1")?.unlocks ?? "",
    consequence: "if 3335.1 were source-bound and its sequence valid, it would pair with already-strict M-70 to unlock the 032 matched-predecessor gate, though formula-family pressure would still need collapse",
  },
  {
    decision: "dual_705_upgrade_strengthens_ecology_not_matched_lane",
    evidence: byScenario.get("upgrade_m1825_and_dholavira_705_pair")?.strict_705_terminal_objects ?? "",
    result: byScenario.get("upgrade_m1825_and_dholavira_705_pair")?.unlocks ?? "",
    consequence: "Dholavira 4237.1 plus M-1825 would create repeated strict 705 terminal ecology, but not a matched-predecessor branch split",
  },
  {
    decision: "h773_upgrade_would_attack_closure_polarity",
    evidence: byScenario.get("upgrade_h773")?.strict_non125_continuing_objects ?? "",
    result: byScenario.get("upgrade_h773")?.unlocks ?? "",
    consequence: "a strict H-773 target-side reading would create a strict non-125 continuing exception, useful as an adversarial polarity test rather than a matched-lane proof",
  },
  {
    decision: "m38_upgrade_is_tail_subframe_not_branch_split",
    evidence: byScenario.get("upgrade_m38")?.strict_matched_prev_splits ?? "",
    result: byScenario.get("upgrade_m38")?.unlocks ?? "",
    consequence: "M-38 becoming strict would expand 125 continuation and the 235 same-branch tail split, but it would not create branch alternation",
  },
];

writeCsv(
  path.join(reportsDir, `${prefix}_scenario_summary.csv`),
  scenarioRows,
  [
    "scenario",
    "upgraded_ids",
    "purpose",
    "strict_rows",
    "strict_objects",
    "strict_matched_prev_split_count",
    "strict_matched_prev_splits",
    "strict_705_terminal_rows",
    "strict_705_terminal_objects",
    "strict_non125_continuing_rows",
    "strict_non125_continuing_objects",
    "strict_125_continuing_rows",
    "unlocks",
  ],
);

writeCsv(
  path.join(reportsDir, `${prefix}_strict_prev_groups.csv`),
  prevGroupRows,
  [
    "scenario",
    "prev_before_002",
    "strict_rows",
    "strict_branches",
    "strict_terminal_classes",
    "strict_objects",
    "gate",
  ],
);

writeCsv(
  path.join(reportsDir, `${prefix}_strict_branch_summary.csv`),
  branchRows,
  ["scenario", "branch_after_390", "strict_rows", "terminal_classes", "prevs", "objects"],
);

writeCsv(
  path.join(reportsDir, `${prefix}_decisions.csv`),
  decisions,
  ["decision", "evidence", "result", "consequence"],
);

const summary = {
  run_date: "2026-05-31",
  input: path.relative(root, framesPath).replace(/\\/g, "/"),
  scenario_count: scenarios.length,
  scenarios: scenarioRows,
  decisions,
  status: "source_upgrade_impact_audit_3335_single_unlock_004_dual_upgrade_705_ecology_no_values",
  outputs: {
    scenario_summary: `data/open_prototype/reports/${prefix}_scenario_summary.csv`,
    strict_prev_groups: `data/open_prototype/reports/${prefix}_strict_prev_groups.csv`,
    strict_branch_summary: `data/open_prototype/reports/${prefix}_strict_branch_summary.csv`,
    decisions: `data/open_prototype/reports/${prefix}_decisions.csv`,
    summary: `data/open_prototype/reports/${prefix}_summary.json`,
  },
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
