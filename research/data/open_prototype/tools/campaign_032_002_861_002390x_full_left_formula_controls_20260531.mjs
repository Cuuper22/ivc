import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const dataPath = path.join(root, "data", "open_prototype", "lipi", "metadata_filtered.csv");
const reportsDir = path.join(root, "data", "open_prototype", "reports");
const framesPath = path.join(reportsDir, "campaign_032_002_861_002390x_branch_sign_ecology_20260531_002390_frames.csv");
const prefix = "campaign_032_002_861_002390x_full_left_formula_controls_20260531";

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

function joinSigns(values) {
  return values.length ? values.join(" ") : "<START>";
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
  return rows.map((r) => `${r.object}:${r.after_002_head}->${r.after_002_tail}`).join("; ");
}

const metadata = parseCsv(fs.readFileSync(dataPath, "utf8"));
const branchFrames = parseCsv(fs.readFileSync(framesPath, "utf8"));
const sourceStatusById = new Map(branchFrames.map((r) => [r.id, r.source_status]));

const occurrences002 = [];
for (const row of metadata) {
  const toks = signs(row.text);
  for (let i = 0; i < toks.length; i++) {
    if (toks[i] !== "002") continue;
    const afterHead = toks[i + 1] ?? "<END>";
    const afterTail = toks.slice(i + 1).join(" ") || "<END>";
    const is002390 = afterHead === "390";
    occurrences002.push({
      id: row.id,
      object: rowObject(row),
      site: row.site,
      type: row.type,
      symbol: row.symbol,
      cult: row.cult,
      full_left: joinSigns(toks.slice(0, i)),
      left_last1: toks[i - 1] ?? "<START>",
      left_last2: joinSigns(toks.slice(Math.max(0, i - 2), i)),
      after_002_head: afterHead,
      after_002_tail: afterTail,
      branch_after_390: is002390 ? (toks[i + 2] ?? "<END>") : "<NOT_002390>",
      tail_after_branch: is002390 ? (toks.slice(i + 3).join(" ") || "<END>") : "<NOT_002390>",
      terminal_after_branch: is002390 && i + 2 === toks.length - 1 ? "yes" : is002390 ? "no" : "<NOT_002390>",
      is_002390: is002390 ? "yes" : "no",
      source_status: sourceStatusById.get(row.id) ?? "not_in_002390_frame_or_metadata_only",
      text: row.text,
    });
  }
}

const targetRows = occurrences002.filter((row) => row.is_002390 === "yes");

function classifyGroup(target, rows, label) {
  const heads = [...new Set(rows.map((r) => r.after_002_head))].sort();
  const branchRows = rows.filter((r) => r.is_002390 === "yes");
  const branches = [...new Set(branchRows.map((r) => r.branch_after_390))].sort();
  let verdict = `${label}_singleton_no_control`;
  if (rows.length > 1 && heads.length > 1) verdict = `${label}_same_left_alternates_post002_head`;
  else if (branchRows.length > 1 && branches.length > 1) verdict = `${label}_same_left_has_002390_branch_split`;
  else if (branchRows.length > 1 && branches.length === 1) verdict = `${label}_same_left_repeats_same_002390_branch`;
  else if (rows.length > 1 && heads.length === 1) verdict = `${label}_same_left_same_post002_head`;
  return {
    [`${label}_key`]: target[label],
    [`${label}_rows`]: rows.length,
    [`${label}_heads`]: distribution(rows, "after_002_head"),
    [`${label}_002390_branches`]: branchRows.length ? distribution(branchRows, "branch_after_390") : "",
    [`${label}_objects`]: objectList(rows),
    [`${label}_verdict`]: verdict,
  };
}

const targetControlRows = [];
for (const target of targetRows) {
  const fullRows = occurrences002.filter((row) => row.full_left === target.full_left);
  const last2Rows = occurrences002.filter((row) => row.left_last2 === target.left_last2);
  const last1Rows = occurrences002.filter((row) => row.left_last1 === target.left_last1);
  const full = classifyGroup(target, fullRows, "full_left");
  const last2 = classifyGroup(target, last2Rows, "left_last2");
  const last1 = classifyGroup(target, last1Rows, "left_last1");
  let decision = "exact_full_left_singleton_broader_controls_needed";
  if (full.full_left_verdict === "full_left_same_left_alternates_post002_head") {
    decision = "exact_full_left_not_deterministic_for_post002_head";
  } else if (full.full_left_verdict === "full_left_same_left_has_002390_branch_split") {
    decision = "exact_full_left_branch_split_found";
  } else if (full.full_left_verdict === "full_left_same_left_repeats_same_002390_branch") {
    decision = "exact_full_left_formula_residue_risk";
  } else if (last2.left_last2_verdict === "left_last2_same_left_alternates_post002_head") {
    decision = "last2_left_not_deterministic_but_exact_full_left_singleton";
  }
  targetControlRows.push({
    id: target.id,
    object: target.object,
    site: target.site,
    type: target.type,
    full_left: target.full_left,
    left_last2: target.left_last2,
    left_last1: target.left_last1,
    branch_after_390: target.branch_after_390,
    tail_after_branch: target.tail_after_branch,
    terminal_after_branch: target.terminal_after_branch,
    source_status: target.source_status,
    exact_full_left_decision: decision,
    ...full,
    ...last2,
    ...last1,
    text: target.text,
  });
}

const fullLeftGroups = [];
const groupByFull = new Map();
for (const row of occurrences002) {
  if (!groupByFull.has(row.full_left)) groupByFull.set(row.full_left, []);
  groupByFull.get(row.full_left).push(row);
}
for (const [fullLeft, rows] of [...groupByFull.entries()].sort(([a], [b]) => a.localeCompare(b))) {
  const branchRows = rows.filter((r) => r.is_002390 === "yes");
  if (!branchRows.length) continue;
  fullLeftGroups.push({
    full_left: fullLeft,
    rows: rows.length,
    heads: distribution(rows, "after_002_head"),
    branch_rows: branchRows.length,
    branches: distribution(branchRows, "branch_after_390"),
    objects: objectList(rows),
    target_objects: branchRows.map((r) => r.object).join(" "),
    has_post002_head_alternation: new Set(rows.map((r) => r.after_002_head)).size > 1 ? "yes" : "no",
    has_002390_branch_alternation: new Set(branchRows.map((r) => r.branch_after_390)).size > 1 ? "yes" : "no",
  });
}

const exactFullAlternating = targetControlRows.filter((r) => r.exact_full_left_decision === "exact_full_left_not_deterministic_for_post002_head");
const exactFullBranchSplits = targetControlRows.filter((r) => r.exact_full_left_decision === "exact_full_left_branch_split_found");
const exactFullResidue = targetControlRows.filter((r) => r.exact_full_left_decision === "exact_full_left_formula_residue_risk");
const exactFullSingletons = targetControlRows.filter((r) => r.exact_full_left_decision === "exact_full_left_singleton_broader_controls_needed");
const last2OnlyAlternating = targetControlRows.filter((r) => r.exact_full_left_decision === "last2_left_not_deterministic_but_exact_full_left_singleton");

const decisions = [
  {
    decision: "exact_full_left_controls_partly_break_formula_determinism",
    evidence: exactFullAlternating.map((r) => `${r.object}:${r.full_left}->${r.full_left_heads}`).join(" | "),
    result: `${exactFullAlternating.length} of ${targetControlRows.length} target frames have exact full-left controls with alternate post-002 heads`,
    consequence: "whole-left formula alone does not deterministically force 002-390 in those rows",
  },
  {
    decision: "no_exact_full_left_002390_branch_split",
    evidence: exactFullBranchSplits.map((r) => `${r.object}:${r.full_left}->${r.full_left_002390_branches}`).join(" | "),
    result: `${exactFullBranchSplits.length} exact full-left groups contain multiple 002-390 branch alternatives`,
    consequence: "the gate still lacks exact full-left matched branch alternation",
  },
  {
    decision: "exact_full_left_singletons_keep_acquisition_and_broader_controls_needed",
    evidence: exactFullSingletons.map((r) => `${r.object}:${r.full_left}->390-${r.branch_after_390}`).join(" | "),
    result: `${exactFullSingletons.length} target frames are exact full-left singletons`,
    consequence: "singletons cannot prove or disprove formula residue without broader left-context or source controls",
  },
  {
    decision: "last2_controls_add_pressure_but_not_strict_proof",
    evidence: last2OnlyAlternating.map((r) => `${r.object}:${r.left_last2}->${r.left_last2_heads}`).join(" | "),
    result: `${last2OnlyAlternating.length} singleton exact-prefix rows have last2-left controls with alternate post-002 heads`,
    consequence: "last2 context weakens full-left determinism but is too broad for grammar promotion",
  },
  {
    decision: "same_left_same_branch_residue_small",
    evidence: exactFullResidue.map((r) => `${r.object}:${r.full_left}->${r.full_left_002390_branches}`).join(" | "),
    result: `${exactFullResidue.length} target rows have exact full-left repeated same 002-390 branch residue`,
    consequence: "no current 002-390-X target is promoted by repeated exact full-left same-branch evidence",
  },
];

writeCsv(
  path.join(reportsDir, `${prefix}_all_002_occurrences.csv`),
  occurrences002,
  [
    "id",
    "object",
    "site",
    "type",
    "symbol",
    "cult",
    "full_left",
    "left_last1",
    "left_last2",
    "after_002_head",
    "after_002_tail",
    "branch_after_390",
    "tail_after_branch",
    "terminal_after_branch",
    "is_002390",
    "source_status",
    "text",
  ],
);
writeCsv(
  path.join(reportsDir, `${prefix}_target_controls.csv`),
  targetControlRows,
  [
    "id",
    "object",
    "site",
    "type",
    "full_left",
    "left_last2",
    "left_last1",
    "branch_after_390",
    "tail_after_branch",
    "terminal_after_branch",
    "source_status",
    "exact_full_left_decision",
    "full_left_rows",
    "full_left_heads",
    "full_left_002390_branches",
    "full_left_objects",
    "full_left_verdict",
    "left_last2_rows",
    "left_last2_heads",
    "left_last2_002390_branches",
    "left_last2_objects",
    "left_last2_verdict",
    "left_last1_rows",
    "left_last1_heads",
    "left_last1_002390_branches",
    "left_last1_objects",
    "left_last1_verdict",
    "text",
  ],
);
writeCsv(
  path.join(reportsDir, `${prefix}_full_left_groups.csv`),
  fullLeftGroups,
  [
    "full_left",
    "rows",
    "heads",
    "branch_rows",
    "branches",
    "objects",
    "target_objects",
    "has_post002_head_alternation",
    "has_002390_branch_alternation",
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
  all_002_occurrences: occurrences002.length,
  target_002390_frames: targetControlRows.length,
  exact_full_left_alternating_head_targets: exactFullAlternating.length,
  exact_full_left_branch_splits: exactFullBranchSplits.length,
  exact_full_left_singletons: exactFullSingletons.length,
  last2_only_alternating_targets: last2OnlyAlternating.length,
  exact_full_left_same_branch_residue_targets: exactFullResidue.length,
  decisions,
  status: "full_left_formula_controls_break_head_determinism_but_no_branch_promotion_no_values",
  outputs: {
    all_002_occurrences: `data/open_prototype/reports/${prefix}_all_002_occurrences.csv`,
    target_controls: `data/open_prototype/reports/${prefix}_target_controls.csv`,
    full_left_groups: `data/open_prototype/reports/${prefix}_full_left_groups.csv`,
    decisions: `data/open_prototype/reports/${prefix}_decisions.csv`,
    summary: `data/open_prototype/reports/${prefix}_summary.json`,
  },
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
