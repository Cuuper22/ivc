import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const dataPath = path.join(root, "data", "open_prototype", "lipi", "metadata_filtered.csv");
const reportsDir = path.join(root, "data", "open_prototype", "reports");
const prefix = "campaign_032_002_861_002390x_390_context_adversary_20260531";
const focusBranches = ["125", "095", "692", "705", "530", "590"];

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
  return row.cisi || row.id || "";
}

const metadata = parseCsv(fs.readFileSync(dataPath, "utf8"));
const frames390 = [];

for (const row of metadata) {
  const toks = signs(row.text);
  for (let i = 0; i < toks.length - 1; i++) {
    if (toks[i] !== "390") continue;
    const branch = toks[i + 1];
    const tail = toks.slice(i + 2);
    frames390.push({
      id: row.id,
      object: rowObject(row),
      site: row.site,
      type: row.type,
      prev_before_390: toks[i - 1] ?? "<START>",
      branch_after_390: branch,
      tail_after_branch: tail.join(" ") || "<END>",
      terminal_after_branch: tail.length === 0 ? "yes" : "no",
      is_002390: toks[i - 1] === "002" ? "yes" : "no",
      text: row.text,
    });
  }
}

const branchSummary = [];
const branches = [...new Set(frames390.map((r) => r.branch_after_390))].sort();
for (const branch of branches) {
  const rows = frames390.filter((r) => r.branch_after_390 === branch);
  const in002 = rows.filter((r) => r.is_002390 === "yes");
  const not002 = rows.filter((r) => r.is_002390 === "no");
  branchSummary.push({
    branch_after_390: branch,
    rows: rows.length,
    terminal: rows.filter((r) => r.terminal_after_branch === "yes").length,
    continuing: rows.filter((r) => r.terminal_after_branch === "no").length,
    in_002390_rows: in002.length,
    in_002390_terminal: in002.filter((r) => r.terminal_after_branch === "yes").length,
    in_002390_continuing: in002.filter((r) => r.terminal_after_branch === "no").length,
    non_002390_rows: not002.length,
    non_002390_terminal: not002.filter((r) => r.terminal_after_branch === "yes").length,
    non_002390_continuing: not002.filter((r) => r.terminal_after_branch === "no").length,
    objects: rows.map((r) => r.object).slice(0, 20).join(" "),
  });
}

const focusRows = frames390.filter((r) => focusBranches.includes(r.branch_after_390));
const focusSummary = branchSummary.filter((r) => focusBranches.includes(r.branch_after_390));

const decisions = [
  {
    decision: "390_125_not_intrinsic_continuation",
    evidence: focusSummary.find((r) => r.branch_after_390 === "125")
      ? JSON.stringify(focusSummary.find((r) => r.branch_after_390 === "125"))
      : "",
    result: "390-125 has 9 rows: 4/4 continuing when preceded by 002, but outside 002 it is 3 terminal and 2 continuing",
    consequence: "the continuation behavior is not explained by 390-125 alone; 002-before-390 remains a live conditioning clue",
  },
  {
    decision: "390_095_context_splits",
    evidence: focusRows
      .filter((r) => r.branch_after_390 === "095")
      .map((r) => `${r.object}:${r.prev_before_390}->390-095->${r.tail_after_branch}`)
      .join("; "),
    result: "inside 002-390, 095 is 2/2 terminal; the one non-002 390-095 row continues",
    consequence: "095 closure cannot be reduced to 390-095 alone, but the sample is tiny",
  },
  {
    decision: "390_705_and_692_no_non002_controls",
    evidence: focusRows
      .filter((r) => ["705", "692"].includes(r.branch_after_390))
      .map((r) => `${r.object}:${r.prev_before_390}->390-${r.branch_after_390}->${r.tail_after_branch}`)
      .join("; "),
    result: "390-705 and 390-692 occur only in the 002-390 frame in this metadata scan",
    consequence: "they cannot test whether 002 is conditioning behavior outside the frame; source binding remains decisive",
  },
  {
    decision: "390_590_broad_formula_pressure",
    evidence: focusSummary.find((r) => r.branch_after_390 === "590")
      ? JSON.stringify(focusSummary.find((r) => r.branch_after_390 === "590"))
      : "",
    result: "390-590 is broad and mostly continuing outside 002-390",
    consequence: "3335.1's 390-590-032 tail remains formula-family pressured",
  },
];

writeCsv(
  path.join(reportsDir, `${prefix}_frames390.csv`),
  frames390,
  ["id", "object", "site", "type", "prev_before_390", "branch_after_390", "tail_after_branch", "terminal_after_branch", "is_002390", "text"],
);
writeCsv(
  path.join(reportsDir, `${prefix}_branch_summary.csv`),
  branchSummary,
  [
    "branch_after_390",
    "rows",
    "terminal",
    "continuing",
    "in_002390_rows",
    "in_002390_terminal",
    "in_002390_continuing",
    "non_002390_rows",
    "non_002390_terminal",
    "non_002390_continuing",
    "objects",
  ],
);
writeCsv(
  path.join(reportsDir, `${prefix}_focus_rows.csv`),
  focusRows,
  ["id", "object", "site", "type", "prev_before_390", "branch_after_390", "tail_after_branch", "terminal_after_branch", "is_002390", "text"],
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
  total_390_frames: frames390.length,
  focus_summary: focusSummary,
  decisions,
  status: "390_context_adversary_keeps_002_conditioning_live_no_values",
  outputs: {
    frames390: `data/open_prototype/reports/${prefix}_frames390.csv`,
    branch_summary: `data/open_prototype/reports/${prefix}_branch_summary.csv`,
    focus_rows: `data/open_prototype/reports/${prefix}_focus_rows.csv`,
    decisions: `data/open_prototype/reports/${prefix}_decisions.csv`,
    summary: `data/open_prototype/reports/${prefix}_summary.json`,
  },
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
