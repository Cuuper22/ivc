import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const dataPath = path.join(root, "data", "open_prototype", "lipi", "metadata_filtered.csv");
const reportsDir = path.join(root, "data", "open_prototype", "reports");
const prefix = "campaign_032_002_861_002390x_3335_identity_neighborhood_audit_20260531";
const targetId = "3335.1";

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

function signs(text) {
  return [...String(text || "").matchAll(/\d{3}/g)].map((m) => m[0]);
}

function norm(value) {
  const s = String(value ?? "").trim();
  return !s || s === "-" || s === "--" ? "" : s;
}

function rowObject(row) {
  return norm(row.cisi) || `-:${row.id}`;
}

function number(value) {
  const n = Number(String(value ?? "").replace(/[^\d.-]/g, ""));
  return Number.isFinite(n) ? n : null;
}

function rowNumber(id) {
  const n = Number(String(id).split(".")[0]);
  return Number.isFinite(n) ? n : null;
}

function textKey(row) {
  return signs(row.text).join("-");
}

function containsChunk(row, chunk) {
  return `-${textKey(row)}-`.includes(`-${chunk}-`);
}

function seqLcs(a, b) {
  const dp = Array.from({ length: a.length + 1 }, () => Array(b.length + 1).fill(0));
  for (let i = 1; i <= a.length; i++) {
    for (let j = 1; j <= b.length; j++) {
      dp[i][j] = a[i - 1] === b[j - 1] ? dp[i - 1][j - 1] + 1 : Math.max(dp[i - 1][j], dp[i][j - 1]);
    }
  }
  return dp[a.length][b.length];
}

function targetSimilarity(target, row) {
  const targetSigns = signs(target.text);
  const rowSigns = signs(row.text);
  let score = 0;
  const reasons = [];
  if (row.id === target.id) {
    score += 100;
    reasons.push("target");
  }
  for (const field of ["type", "symbol", "cult", "shape", "material", "site", "region"]) {
    const t = norm(target[field]);
    const r = norm(row[field]);
    if (t && r && t === r) {
      score += field === "site" || field === "region" ? 1 : 2;
      reasons.push(`same_${field}`);
    }
  }
  const h = number(row["horizontal(mm)"]);
  const v = number(row["vertical(mm)"]);
  const th = number(row["thickness(mm)"]);
  const tht = number(target["thickness(mm)"]);
  const ht = number(target["horizontal(mm)"]);
  const vt = number(target["vertical(mm)"]);
  if (h !== null && ht !== null && Math.abs(h - ht) <= 1) {
    score += 2;
    reasons.push("near_h");
  }
  if (v !== null && vt !== null && Math.abs(v - vt) <= 1) {
    score += 2;
    reasons.push("near_v");
  }
  if (th !== null && tht !== null && th === tht && th !== 0) {
    score += 1;
    reasons.push("same_th");
  }
  const lcs = seqLcs(targetSigns, rowSigns);
  if (lcs >= 4) {
    score += lcs;
    reasons.push(`lcs_${lcs}`);
  }
  if (containsChunk(row, "390-590-032")) {
    score += 10;
    reasons.push("has_390_590_032");
  }
  if (containsChunk(row, "032-002-390")) {
    score += 10;
    reasons.push("has_032_002_390");
  }
  if (textKey(row) === textKey(target)) {
    score += 25;
    reasons.push("exact_text");
  }
  return { score, reasons: reasons.join(";") };
}

function compact(row) {
  return {
    id: row.id,
    object: rowObject(row),
    region: row.region,
    site: row.site,
    type: row.type,
    symbol: row.symbol,
    cult: row.cult,
    material: row.material,
    shape: row.shape,
    excavation_idno: row["excavation-idno"],
    horizontal_mm: row["horizontal(mm)"],
    vertical_mm: row["vertical(mm)"],
    thickness_mm: row["thickness(mm)"],
    text: row.text,
  };
}

const rows = parseCsv(fs.readFileSync(dataPath, "utf8"));
const target = rows.find((row) => row.id === targetId);
if (!target) throw new Error(`Missing target ${targetId}`);

const targetN = rowNumber(target.id);
const targetProfile = [
  {
    id: target.id,
    object: rowObject(target),
    region: target.region,
    site: target.site,
    area_section: target["area-section"],
    excavation_idno: target["excavation-idno"],
    type: target.type,
    symbol: target.symbol,
    cult: target.cult,
    material: target.material,
    shape: target.shape,
    horizontal_mm: target["horizontal(mm)"],
    vertical_mm: target["vertical(mm)"],
    thickness_mm: target["thickness(mm)"],
    signs: textKey(target),
    text: target.text,
  },
];

const neighborhood = rows
  .map((row) => ({ ...row, distance_from_3335: rowNumber(row.id) === null ? "" : rowNumber(row.id) - targetN }))
  .filter((row) => row.distance_from_3335 !== "" && Math.abs(row.distance_from_3335) <= 12)
  .sort((a, b) => Number(a.distance_from_3335) - Number(b.distance_from_3335))
  .map((row) => ({ distance_from_3335: row.distance_from_3335, ...compact(row) }));

const exactAndChunks = rows
  .filter(
    (row) =>
      row.id === target.id ||
      textKey(row) === textKey(target) ||
      containsChunk(row, "032-002-390") ||
      containsChunk(row, "002-390-590-032") ||
      containsChunk(row, "390-590-032"),
  )
  .map((row) => ({
    relation: [
      row.id === target.id ? "target" : "",
      textKey(row) === textKey(target) ? "exact_text" : "",
      containsChunk(row, "032-002-390") ? "has_032_002_390" : "",
      containsChunk(row, "002-390-590-032") ? "has_002_390_590_032" : "",
      containsChunk(row, "390-590-032") ? "has_390_590_032" : "",
    ]
      .filter(Boolean)
      .join(";"),
    ...compact(row),
  }));

const noObjectRows = rows.filter((row) => !norm(row.cisi));
const noObjectSimilar = noObjectRows
  .map((row) => {
    const sim = targetSimilarity(target, row);
    return { score: sim.score, reasons: sim.reasons, ...compact(row) };
  })
  .filter((row) => row.score >= 8 || row.id === target.id)
  .sort((a, b) => b.score - a.score || a.id.localeCompare(b.id));

const allSimilar = rows
  .map((row) => {
    const sim = targetSimilarity(target, row);
    return { score: sim.score, reasons: sim.reasons, ...compact(row) };
  })
  .filter((row) => row.score >= 14 || row.id === target.id)
  .sort((a, b) => b.score - a.score || a.id.localeCompare(b.id))
  .slice(0, 60);

const rafRows = rows
  .filter((row) => norm(row.cult) === "RAF")
  .map((row) => ({
    has_object_id: norm(row.cisi) ? "yes" : "no",
    has_390_590_032: containsChunk(row, "390-590-032") ? "yes" : "no",
    has_032_002_390: containsChunk(row, "032-002-390") ? "yes" : "no",
    ...compact(row),
  }));

const sameMetadataRows = rows
  .filter(
    (row) =>
      row.id !== target.id &&
      norm(row.type) === norm(target.type) &&
      norm(row.symbol) === norm(target.symbol) &&
      norm(row.cult) === norm(target.cult) &&
      norm(row.shape) === norm(target.shape),
  )
  .map((row) => {
    const sim = targetSimilarity(target, row);
    return { score: sim.score, reasons: sim.reasons, ...compact(row) };
  })
  .sort((a, b) => b.score - a.score || a.id.localeCompare(b.id));

const decisions = [
  {
    decision: "no_exact_text_duplicate",
    evidence: exactAndChunks.filter((row) => row.relation.includes("exact_text")).map((row) => `${row.id}:${row.object}`).join(" | "),
    result: `${exactAndChunks.filter((row) => row.relation.includes("exact_text")).length} exact-text row(s), including the target itself`,
    consequence: "no local duplicate can be promoted as a source-identified replacement for 3335.1",
  },
  {
    decision: "row_order_neighbors_do_not_bridge_identity",
    evidence: neighborhood.map((row) => `${row.distance_from_3335}:${row.id}:${row.object}:${row.text}`).join(" | "),
    result: "neighboring local rows are ordered near known Mohenjo-daro objects, but the prior M-940 bridge is rejected and no alternate neighbor gives the target sequence",
    consequence: "row order remains a provenance clue only, not an object id",
  },
  {
    decision: "chunk_family_is_real_but_not_identity",
    evidence: exactAndChunks.filter((row) => row.relation.includes("has_390_590_032")).map((row) => `${row.id}:${row.object}:${row.site}:${row.text}`).join(" | "),
    result: `${exactAndChunks.filter((row) => row.relation.includes("has_390_590_032")).length} rows contain 390-590-032`,
    consequence: "the portable chunk strengthens formula-family pressure and cannot identify the blocked row by itself",
  },
  {
    decision: "no_object_similar_rows_are_not_replacements",
    evidence: noObjectSimilar.map((row) => `${row.id}:${row.object}:score=${row.score}:${row.reasons}`).join(" | "),
    result: `${noObjectSimilar.length} no-object rows pass the similarity threshold, with 3335.1 still isolated for the target chunk`,
    consequence: "cisi-less metadata does not supply a source-bound replacement witness",
  },
  {
    decision: "same_metadata_profile_not_unique_but_no_text_bridge",
    evidence: sameMetadataRows.slice(0, 12).map((row) => `${row.id}:${row.object}:score=${row.score}:${row.text}`).join(" | "),
    result: `${sameMetadataRows.length} rows share type/symbol/cult/shape with the target`,
    consequence: "metadata profile can guide source hunting but cannot bind the target text",
  },
];

writeCsv(
  path.join(reportsDir, `${prefix}_target_profile.csv`),
  targetProfile,
  [
    "id",
    "object",
    "region",
    "site",
    "area_section",
    "excavation_idno",
    "type",
    "symbol",
    "cult",
    "material",
    "shape",
    "horizontal_mm",
    "vertical_mm",
    "thickness_mm",
    "signs",
    "text",
  ],
);

writeCsv(
  path.join(reportsDir, `${prefix}_row_order_neighborhood.csv`),
  neighborhood,
  [
    "distance_from_3335",
    "id",
    "object",
    "region",
    "site",
    "type",
    "symbol",
    "cult",
    "material",
    "shape",
    "excavation_idno",
    "horizontal_mm",
    "vertical_mm",
    "thickness_mm",
    "text",
  ],
);

writeCsv(
  path.join(reportsDir, `${prefix}_exact_and_chunk_matches.csv`),
  exactAndChunks,
  [
    "relation",
    "id",
    "object",
    "region",
    "site",
    "type",
    "symbol",
    "cult",
    "material",
    "shape",
    "excavation_idno",
    "horizontal_mm",
    "vertical_mm",
    "thickness_mm",
    "text",
  ],
);

writeCsv(
  path.join(reportsDir, `${prefix}_no_object_similar_rows.csv`),
  noObjectSimilar,
  [
    "score",
    "reasons",
    "id",
    "object",
    "region",
    "site",
    "type",
    "symbol",
    "cult",
    "material",
    "shape",
    "excavation_idno",
    "horizontal_mm",
    "vertical_mm",
    "thickness_mm",
    "text",
  ],
);

writeCsv(
  path.join(reportsDir, `${prefix}_all_similarity_candidates.csv`),
  allSimilar,
  [
    "score",
    "reasons",
    "id",
    "object",
    "region",
    "site",
    "type",
    "symbol",
    "cult",
    "material",
    "shape",
    "excavation_idno",
    "horizontal_mm",
    "vertical_mm",
    "thickness_mm",
    "text",
  ],
);

writeCsv(
  path.join(reportsDir, `${prefix}_raf_rows.csv`),
  [
    {
      has_object_id: "SUMMARY",
      has_390_590_032: `RAF rows=${rafRows.length}`,
      has_032_002_390: `RAF no-object=${rafRows.filter((row) => row.has_object_id === "no").length}`,
      id: "",
      object: "",
      region: "",
      site: "",
      type: "",
      symbol: "",
      cult: "",
      material: "",
      shape: "",
      excavation_idno: "",
      horizontal_mm: "",
      vertical_mm: "",
      thickness_mm: "",
      text: "",
    },
    ...rafRows,
  ],
  [
    "has_object_id",
    "has_390_590_032",
    "has_032_002_390",
    "id",
    "object",
    "region",
    "site",
    "type",
    "symbol",
    "cult",
    "material",
    "shape",
    "excavation_idno",
    "horizontal_mm",
    "vertical_mm",
    "thickness_mm",
    "text",
  ],
);

writeCsv(
  path.join(reportsDir, `${prefix}_same_metadata_profile.csv`),
  sameMetadataRows,
  [
    "score",
    "reasons",
    "id",
    "object",
    "region",
    "site",
    "type",
    "symbol",
    "cult",
    "material",
    "shape",
    "excavation_idno",
    "horizontal_mm",
    "vertical_mm",
    "thickness_mm",
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
  target: targetProfile[0],
  exact_text_rows: exactAndChunks.filter((row) => row.relation.includes("exact_text")).length,
  rows_with_390_590_032: exactAndChunks.filter((row) => row.relation.includes("has_390_590_032")).length,
  rows_with_032_002_390: exactAndChunks.filter((row) => row.relation.includes("has_032_002_390")).length,
  no_object_rows: noObjectRows.length,
  no_object_similar_rows: noObjectSimilar.length,
  raf_rows: rafRows.length,
  raf_no_object_rows: rafRows.filter((row) => row.has_object_id === "no").length,
  same_metadata_profile_rows: sameMetadataRows.length,
  decisions,
  status: "3335_identity_neighborhood_no_local_bridge_external_source_required_no_values",
  outputs: {
    target_profile: `data/open_prototype/reports/${prefix}_target_profile.csv`,
    row_order_neighborhood: `data/open_prototype/reports/${prefix}_row_order_neighborhood.csv`,
    exact_and_chunk_matches: `data/open_prototype/reports/${prefix}_exact_and_chunk_matches.csv`,
    no_object_similar_rows: `data/open_prototype/reports/${prefix}_no_object_similar_rows.csv`,
    all_similarity_candidates: `data/open_prototype/reports/${prefix}_all_similarity_candidates.csv`,
    raf_rows: `data/open_prototype/reports/${prefix}_raf_rows.csv`,
    same_metadata_profile: `data/open_prototype/reports/${prefix}_same_metadata_profile.csv`,
    decisions: `data/open_prototype/reports/${prefix}_decisions.csv`,
    summary: `data/open_prototype/reports/${prefix}_summary.json`,
  },
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
