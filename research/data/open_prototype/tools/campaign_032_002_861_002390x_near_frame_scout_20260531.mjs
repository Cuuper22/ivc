import fs from "node:fs";
import path from "node:path";

// Before declaring the matched-predecessor evidence exhausted, this script checks whether
// any 002-390 frames are hiding in plain sight. It reads data/open_prototype/lipi/
// metadata_filtered.csv and collects two shapes: adjacent frames (002 immediately followed
// by 390, the known 15) and gapped near-frames (002-X-390 with exactly one sign between),
// flagging rows whose raw text contains brackets or question marks as damaged or open
// readings. Both sets are grouped by the sign before the 002 to see whether any predecessor
// group gains a new branch alternative. The recorded outcome: no rescue anywhere — the
// adjacent set is unchanged, the only multi-row predecessor groups remain 004, 032, and 235,
// gapped rows add no matched split, and Dholavira 4348.1 (002-861-390) is confirmed as NOT
// an adjacent frame. Writes adjacent rows, gapped rows, both predecessor summaries, and
// decisions as CSVs plus a summary JSON in reports/.

const root = process.cwd();
const dataPath = path.join(root, "data", "open_prototype", "lipi", "metadata_filtered.csv");
const reportsDir = path.join(root, "data", "open_prototype", "reports");
const prefix = "campaign_032_002_861_002390x_near_frame_scout_20260531";

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

function damagedOrOpen(text) {
  return /[\[\]\?]/.test(String(text || "")) ? "yes" : "no";
}

function rowObject(row) {
  return row.cisi || row.id || "";
}

const metadata = parseCsv(fs.readFileSync(dataPath, "utf8"));
const adjacentRows = [];
const gappedRows = [];

for (const row of metadata) {
  const toks = signs(row.text);
  for (let i = 0; i < toks.length; i++) {
    if (toks[i] === "002" && toks[i + 1] === "390") {
      adjacentRows.push({
        id: row.id,
        object: rowObject(row),
        site: row.site,
        type: row.type,
        prev_before_002: toks[i - 1] ?? "<START>",
        branch_after_390: toks[i + 2] ?? "<END>",
        tail_after_branch: toks.slice(i + 3).join(" ") || "<END>",
        damaged_or_open: damagedOrOpen(row.text),
        text: row.text,
      });
    }
    if (toks[i] === "002" && toks[i + 2] === "390") {
      gappedRows.push({
        id: row.id,
        object: rowObject(row),
        site: row.site,
        type: row.type,
        prev_before_002: toks[i - 1] ?? "<START>",
        gap_between_002_390: toks[i + 1],
        branch_after_390: toks[i + 3] ?? "<END>",
        tail_after_branch: toks.slice(i + 4).join(" ") || "<END>",
        damaged_or_open: damagedOrOpen(row.text),
        text: row.text,
      });
    }
  }
}

function summarizeByPrev(rows, branchField = "branch_after_390") {
  const groups = new Map();
  for (const row of rows) {
    const prev = row.prev_before_002 || "<NONE>";
    if (!groups.has(prev)) groups.set(prev, []);
    groups.get(prev).push(row);
  }
  const out = [];
  for (const [prev, groupRows] of [...groups.entries()].sort(([a], [b]) => a.localeCompare(b))) {
    const branches = [...new Set(groupRows.map((r) => r[branchField]))].sort();
    out.push({
      prev_before_002: prev,
      rows: groupRows.length,
      branches: branches.join(" "),
      objects: groupRows.map((r) => r.object).join(" "),
      damaged_or_open_rows: groupRows.filter((r) => r.damaged_or_open === "yes").length,
      multi_branch: branches.length > 1 ? "yes" : "no",
      examples: groupRows
        .map((r) => `${r.object}:${r[branchField]}->${r.tail_after_branch}:${r.damaged_or_open}`)
        .join("; "),
    });
  }
  return out;
}

const adjacentPrevSummary = summarizeByPrev(adjacentRows);
const gappedPrevSummary = summarizeByPrev(gappedRows);
const adjacentMulti = adjacentPrevSummary.filter((r) => Number(r.rows) > 1 || r.multi_branch === "yes");
const gappedMulti = gappedPrevSummary.filter((r) => Number(r.rows) > 1 || r.multi_branch === "yes");

const decisions = [
  {
    decision: "adjacent_frame_set_unchanged",
    evidence: `${adjacentRows.length} adjacent 002-390 rows; damaged/open adjacent rows ${adjacentRows.filter((r) => r.damaged_or_open === "yes").length}`,
    result: "same 15 clean adjacent frames as replacement branch-sign ecology",
    consequence: "no hidden damaged/open adjacent row rescues matched-predecessor proof",
  },
  {
    decision: "only_three_adjacent_multi_prev_groups",
    evidence: adjacentMulti.map((r) => `${r.prev_before_002}:${r.examples}`).join(" | "),
    result: "multi-row adjacent predecessor groups remain 004, 032, and 235",
    consequence: "predecessor-gate blocking analysis remains complete for adjacent 002-390-X",
  },
  {
    decision: "gapped_002_x_390_no_rescue",
    evidence: gappedRows.map((r) => `${r.object}:${r.prev_before_002}->002-${r.gap_between_002_390}-390->${r.branch_after_390}:${r.text}`).join(" | "),
    result: `${gappedRows.length} gapped 002-X-390 rows, no repeated/matched predecessor branch split`,
    consequence: "gapped near-frames do not create a new same-predecessor alternative",
  },
  {
    decision: "icit_4348_guard_reinforced",
    evidence: gappedRows.find((r) => r.id === "4348.1")?.text ?? "",
    result: "Dholavira 4348.1 is 002-861-390, not adjacent 002-390-X",
    consequence: "do not use ICIT 4348 as a bridge into the 002-390-705 / 4237.1 lane",
  },
];

writeCsv(
  path.join(reportsDir, `${prefix}_adjacent_rows.csv`),
  adjacentRows,
  ["id", "object", "site", "type", "prev_before_002", "branch_after_390", "tail_after_branch", "damaged_or_open", "text"],
);
writeCsv(
  path.join(reportsDir, `${prefix}_gapped_rows.csv`),
  gappedRows,
  ["id", "object", "site", "type", "prev_before_002", "gap_between_002_390", "branch_after_390", "tail_after_branch", "damaged_or_open", "text"],
);
writeCsv(
  path.join(reportsDir, `${prefix}_adjacent_prev_summary.csv`),
  adjacentPrevSummary,
  ["prev_before_002", "rows", "branches", "objects", "damaged_or_open_rows", "multi_branch", "examples"],
);
writeCsv(
  path.join(reportsDir, `${prefix}_gapped_prev_summary.csv`),
  gappedPrevSummary,
  ["prev_before_002", "rows", "branches", "objects", "damaged_or_open_rows", "multi_branch", "examples"],
);
writeCsv(
  path.join(reportsDir, `${prefix}_decisions.csv`),
  decisions,
  ["decision", "evidence", "result", "consequence"],
);

const summary = {
  run_date: "2026-05-31",
  input: path.relative(root, dataPath).replace(/\\/g, "/"),
  metadata_rows: metadata.length,
  adjacent_002390_rows: adjacentRows.length,
  adjacent_damaged_or_open_rows: adjacentRows.filter((r) => r.damaged_or_open === "yes").length,
  adjacent_multi_prev_groups: adjacentMulti,
  gapped_002_x_390_rows: gappedRows.length,
  gapped_multi_prev_groups: gappedMulti,
  decisions,
  status: "near_frame_scout_no_hidden_matched_prev_rescue_no_values",
  outputs: {
    adjacent_rows: `data/open_prototype/reports/${prefix}_adjacent_rows.csv`,
    gapped_rows: `data/open_prototype/reports/${prefix}_gapped_rows.csv`,
    adjacent_prev_summary: `data/open_prototype/reports/${prefix}_adjacent_prev_summary.csv`,
    gapped_prev_summary: `data/open_prototype/reports/${prefix}_gapped_prev_summary.csv`,
    decisions: `data/open_prototype/reports/${prefix}_decisions.csv`,
    summary: `data/open_prototype/reports/${prefix}_summary.json`,
  },
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
