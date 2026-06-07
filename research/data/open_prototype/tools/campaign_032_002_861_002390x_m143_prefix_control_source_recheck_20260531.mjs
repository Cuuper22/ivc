import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const metadataPath = path.join(root, "data", "open_prototype", "lipi", "metadata_filtered.csv");
const witnessesPath = path.join(root, "data", "sign_crosswalk", "artifact_witnesses.csv");
const reportsDir = path.join(root, "data", "open_prototype", "reports");
const workDir = path.join(root, "tmp", "002390x_m143_prefix_control_20260531");
const derivedDir = path.join(workDir, "derived");
const sourcePage = path.join(workDir, "cisi_india_n080_w2000.jpg");
const prefix = "campaign_032_002_861_002390x_m143_prefix_control_source_recheck_20260531";

const SOURCE_URL =
  "https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India/page/n80_w2000.jpg";

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

function readCsv(filePath) {
  return parseCsv(fs.readFileSync(filePath, "utf8"));
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

function hashFile(filePath) {
  if (!fs.existsSync(filePath)) return "";
  return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex");
}

function rel(filePath) {
  return path.relative(root, filePath).replaceAll(path.sep, "/");
}

function mustFind(rows, pred, label) {
  const row = rows.find(pred);
  if (!row) throw new Error(`Missing ${label}`);
  return row;
}

function fileInfo(filePath, role, note) {
  return {
    role,
    path: rel(filePath),
    exists: fs.existsSync(filePath) ? "yes" : "no",
    size_bytes: fs.existsSync(filePath) ? fs.statSync(filePath).size : 0,
    sha256: hashFile(filePath),
    note,
  };
}

fs.mkdirSync(reportsDir, { recursive: true });

const metadata = readCsv(metadataPath);
const witnesses = readCsv(witnessesPath);
const m143 = mustFind(metadata, (r) => r.id === "2670.1" || r.cisi === "M-143", "M-143 metadata row");
const target3335 = mustFind(metadata, (r) => r.id === "3335.1", "3335.1 metadata row");
const m143Signs = signs(m143.text);
const targetSigns = signs(target3335.text);

const prefixRows = metadata.filter((row) => signs(row.text).join("-").startsWith("740-205-032-002"));
const exactFullLeftRows = metadata.filter((row) => signs(row.text).slice(0, 4).join("-") === "740-205-032-002");
const branchAfterPrefix = exactFullLeftRows.map((row) => {
  const rowSigns = signs(row.text);
  return {
    id: row.id,
    cisi: row.cisi || "-",
    site: row.site,
    type: row.type,
    symbol: row.symbol,
    cult: row.cult,
    material: row.material,
    shape: row.shape,
    branch_after_002: rowSigns[4] ?? "<END>",
    continuation: rowSigns.slice(4).join(" "),
    text: row.text,
    source_state:
      row.id === "2670.1"
        ? "public_cisi_india_n80_panel_visible"
        : row.id === "3335.1"
          ? "metadata_only_unbound"
          : "not_reviewed_here",
  };
});

const witnessRows = witnesses
  .filter((row) => row.artifact_id === "M-143" || row.row_id === "2670.1")
  .map((row) => ({
    witness_id: row.witness_id,
    artifact_id: row.artifact_id,
    system_id: row.system_id,
    row_id: row.row_id,
    side_id: row.side_id,
    text_raw: row.text_raw,
    sign_sequence: row.sign_sequence,
    direction: row.direction,
    provenance_tier: row.provenance_tier,
  }));

const sourceRows = [
  {
    artifact: "M-143",
    row_id: "2670.1",
    source_volume: "Corpus of Indus Seals and Inscriptions. Collections in India",
    archive_leaf: "n80",
    djvu_pages_seen: "India_0080.djvu; India_0511.djvu duplicate OCR block",
    printed_header: "'unicorn' IV / SEALS MOHENJO-DARO 139-144 / 45",
    ocr_label_hits: "M-143 A visible by source pixels; M-143 a OCR label coords 1055,3233,1153,3203,3233 plus side label coords 1167,3231,1184,3213,3231",
    source_url: SOURCE_URL,
    local_page: rel(sourcePage),
    source_page_sha256: hashFile(sourcePage),
    visual_state: "M-143 A and M-143 a panels source-visible; signbands visible but not independently numeric-token-boxed in this audit",
    campaign_use: "prefix-family control for 3335.1 only",
  },
];

const files = [
  fileInfo(sourcePage, "source_page", "Public Archive leaf n80, full page."),
  fileInfo(path.join(derivedDir, "M143_face_A_full_panel_label.jpg"), "crop", "M-143 A full panel with label."),
  fileInfo(path.join(derivedDir, "M143_face_A_full_panel_label_x2.jpg"), "crop_x2", "M-143 A full panel with label, scaled for inspection."),
  fileInfo(path.join(derivedDir, "M143_face_A_signband.jpg"), "crop", "M-143 A signband crop."),
  fileInfo(path.join(derivedDir, "M143_face_A_signband_x2.jpg"), "crop_x2", "M-143 A signband crop, scaled for inspection."),
  fileInfo(path.join(derivedDir, "M143_impression_a_full_panel_label.jpg"), "crop", "M-143 a full panel with label."),
  fileInfo(path.join(derivedDir, "M143_impression_a_full_panel_label_x2.jpg"), "crop_x2", "M-143 a full panel with label, scaled for inspection."),
  fileInfo(path.join(derivedDir, "M143_impression_a_signband.jpg"), "crop", "M-143 a signband crop."),
  fileInfo(path.join(derivedDir, "M143_impression_a_signband_x2.jpg"), "crop_x2", "M-143 a signband crop, scaled for inspection."),
];

const metadataRows = [
  {
    role: "prefix_control",
    id: m143.id,
    cisi: m143.cisi,
    site: m143.site,
    area: m143.area,
    excavation_idno: m143["excavation-idno"],
    type: m143.type,
    symbol: m143.symbol,
    cult: m143.cult,
    material: m143.material,
    shape: m143.shape,
    condition: m143.condition,
    direction: m143.direction,
    sign_count: m143["sign-count"],
    dimensions_mm: `${m143["horizontal(mm)"]} x ${m143["vertical(mm)"]} x ${m143["thickness(mm)"]}`,
    signs: m143Signs.join(" "),
    text: m143.text,
  },
  {
    role: "blocked_target",
    id: target3335.id,
    cisi: target3335.cisi || "-",
    site: target3335.site,
    area: target3335.area,
    excavation_idno: target3335["excavation-idno"],
    type: target3335.type,
    symbol: target3335.symbol,
    cult: target3335.cult,
    material: target3335.material,
    shape: target3335.shape,
    condition: target3335.condition,
    direction: target3335.direction,
    sign_count: target3335["sign-count"],
    dimensions_mm: `${target3335["horizontal(mm)"]} x ${target3335["vertical(mm)"]} x ${target3335["thickness(mm)"]}`,
    signs: targetSigns.join(" "),
    text: target3335.text,
  },
];

const decisions = [
  {
    decision: "m143_source_panel_found",
    evidence:
      "Archive leaf n80 shows M-143 A and M-143 a labels with visible signbands in the CISI India Mohenjo-daro 139-144 plate.",
    consequence: "M-143 can be used as a source-visible prefix-control object, not merely a dark/unindexed metadata row.",
    accepted_scope: "artifact/page/panel visibility and prefix-control context",
  },
  {
    decision: "m143_not_3335_identity_bridge",
    evidence: "M-143 has +740-205-032-002-252-840+ while 3335.1 claims +740-205-032-002-390-590-032+.",
    consequence:
      "M-143 sharpens the adversarial family question around the shared prefix, but cannot bind or rescue 3335.1.",
    accepted_scope: "control, not target promotion",
  },
  {
    decision: "numeric_token_strictness_not_claimed_here",
    evidence:
      "This audit visually confirms source panels/signbands and cites local Lipi/Mayig transcriptions, but does not run an independent blind numeric token-box adjudication.",
    consequence: "Do not count M-143 as a strict numeric-token witness for a value or translation.",
    accepted_scope: "source-route recheck only",
  },
  {
    decision: "no_reading_no_value_no_translation",
    evidence: "The result separates source route, metadata branch, and target identity.",
    consequence: "Accepted value, phonetics, language identity, function, sign meaning, and translation remain 0.",
    accepted_scope: "negative guardrail",
  },
];

const summary = {
  status: "m143_prefix_control_source_panel_found_not_3335_bridge_no_values",
  date: "2026-05-31",
  artifact: "M-143",
  row_id: "2670.1",
  source_url: SOURCE_URL,
  source_page: rel(sourcePage),
  source_page_sha256: hashFile(sourcePage),
  local_crops: files.filter((f) => f.role.startsWith("crop")).map((f) => f.path),
  branch_after_shared_prefix: branchAfterPrefix,
  witness_rows: witnessRows,
  decisions,
  accepted: [
    "M-143 page/panel/signband source route",
    "M-143 as prefix-family control for 3335.1",
    "3335.1 remains unbound metadata-only target",
  ],
  rejected: [
    "M-143 as identity bridge for 3335.1",
    "strict numeric token-box proof from this audit",
    "source-bound value/function/translation",
  ],
};

writeCsv(path.join(reportsDir, `${prefix}_source_route.csv`), sourceRows, [
  "artifact",
  "row_id",
  "source_volume",
  "archive_leaf",
  "djvu_pages_seen",
  "printed_header",
  "ocr_label_hits",
  "source_url",
  "local_page",
  "source_page_sha256",
  "visual_state",
  "campaign_use",
]);

writeCsv(path.join(reportsDir, `${prefix}_files.csv`), files, [
  "role",
  "path",
  "exists",
  "size_bytes",
  "sha256",
  "note",
]);

writeCsv(path.join(reportsDir, `${prefix}_metadata.csv`), metadataRows, [
  "role",
  "id",
  "cisi",
  "site",
  "area",
  "excavation_idno",
  "type",
  "symbol",
  "cult",
  "material",
  "shape",
  "condition",
  "direction",
  "sign_count",
  "dimensions_mm",
  "signs",
  "text",
]);

writeCsv(path.join(reportsDir, `${prefix}_shared_prefix_rows.csv`), branchAfterPrefix, [
  "id",
  "cisi",
  "site",
  "type",
  "symbol",
  "cult",
  "material",
  "shape",
  "branch_after_002",
  "continuation",
  "text",
  "source_state",
]);

writeCsv(path.join(reportsDir, `${prefix}_witness_rows.csv`), witnessRows, [
  "witness_id",
  "artifact_id",
  "system_id",
  "row_id",
  "side_id",
  "text_raw",
  "sign_sequence",
  "direction",
  "provenance_tier",
]);

writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  "decision",
  "evidence",
  "consequence",
  "accepted_scope",
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
