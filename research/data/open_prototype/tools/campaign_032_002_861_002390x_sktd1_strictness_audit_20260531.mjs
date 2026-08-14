import fs from "node:fs";
import path from "node:path";

// Can the Surkotada seal Sktd-1 (row 3875.1, local text +390-004-002-390-125-820+) be
// promoted to a strict source-visible witness for the 004 lane? This audit gathers every
// piece of evidence in one place and answers no. It reads four earlier report CSVs (the
// side-pair recheck, the token-boundary adjudication, the sealed blind-packet key, and the
// source-upgrade impact scenarios) and inspects five local image files under tmp/, parsing
// each JPEG's header for its pixel dimensions so the inventory is verifiable. Six strictness
// tests follow: the A/a side-pair labels pass, the top-band 002-390-125 window passes only
// downweighted, but the wrapped two-field layout fails the single-line test — the full
// token order stays catalog-mediated, so the 125-820 continuation is not strict. The impact
// scenarios confirm the 004 lane unlocks only if both H-1993 and Sktd-1 become strict.
// Writes evidence rows, strictness tests, and decisions as CSVs plus a summary JSON to
// reports/.

const root = process.cwd();
const reportsDir = path.join(root, "data", "open_prototype", "reports");
const prefix = "campaign_032_002_861_002390x_sktd1_strictness_audit_20260531";

const sidePairPath = path.join(reportsDir, "campaign_032_002_861_002390x_sktd1_side_pair_recheck_20260531.csv");
const adjudicationPath = path.join(reportsDir, "campaign_032_002_861_002390x_token_boundary_adjudication_adjudication_rows.csv");
const blindKeyPath = path.join(reportsDir, "blind_boundary_packet_alpha_sealed_key.csv");
const impactPath = path.join(reportsDir, "campaign_032_002_861_002390x_source_upgrade_impact_audit_20260531_scenario_summary.csv");

const imageInputs = [
  {
    item: "source_page",
    path: "tmp/002390x_source_normalization/cisi_india_n397_w2000.jpg",
    expected_role: "public page with visible Sktd-1 A/a labels",
  },
  {
    item: "face_A_full_panel",
    path: "tmp/002390x_source_normalization/Sktd1_face_A_full_panel.jpg",
    expected_role: "object face with top band and separate lower-field sign",
  },
  {
    item: "impression_a_full_panel",
    path: "tmp/002390x_source_normalization/Sktd1_impression_a_full_panel.jpg",
    expected_role: "object impression with mirrored top band and separate lower-field sign",
  },
  {
    item: "face_A_signband",
    path: "tmp/002390x_source_normalization/Sktd1_face_A_signband.jpg",
    expected_role: "top-band crop only",
  },
  {
    item: "impression_a_signband",
    path: "tmp/002390x_source_normalization/Sktd1_impression_a_signband.jpg",
    expected_role: "top-band crop only",
  },
];

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

function readJpegSize(filePath) {
  const bytes = fs.readFileSync(filePath);
  if (bytes[0] !== 0xff || bytes[1] !== 0xd8) return { width: "", height: "" };
  let offset = 2;
  while (offset < bytes.length) {
    if (bytes[offset] !== 0xff) {
      offset++;
      continue;
    }
    const marker = bytes[offset + 1];
    const length = bytes.readUInt16BE(offset + 2);
    if (marker >= 0xc0 && marker <= 0xc3) {
      return {
        width: bytes.readUInt16BE(offset + 7),
        height: bytes.readUInt16BE(offset + 5),
      };
    }
    offset += 2 + length;
  }
  return { width: "", height: "" };
}

function rel(filePath) {
  return path.relative(root, filePath).replace(/\\/g, "/");
}

function pick(rows, predicate) {
  return rows.find(predicate) ?? {};
}

const sidePairRows = readCsv(sidePairPath);
const adjudicationRows = readCsv(adjudicationPath);
const blindRows = readCsv(blindKeyPath);
const impactRows = readCsv(impactPath);

const sktdAdjudication = pick(adjudicationRows, (row) => row.object_key === "Sktd-1" || row.neutral_id === "N005");
const sktdBlind = pick(blindRows, (row) => row.object_key === "Sktd-1" || row.neutral_id === "CHARLIE");
const h1993Only = pick(impactRows, (row) => row.scenario === "upgrade_h1993_only");
const sktdOnly = pick(impactRows, (row) => row.scenario === "upgrade_sktd1_only");
const both004 = pick(impactRows, (row) => row.scenario === "upgrade_h1993_and_sktd1");

const imageRows = imageInputs.map((input) => {
  const abs = path.join(root, input.path);
  const stats = fs.statSync(abs);
  const size = readJpegSize(abs);
  return {
    item: input.item,
    evidence_type: "image_file",
    evidence_path: input.path,
    expected_role: input.expected_role,
    exists: "yes",
    bytes: stats.size,
    width_px: size.width,
    height_px: size.height,
    observation: "file present for reproducible visual inspection",
    strictness_effect: input.item.includes("signband") ? "supports boxed-window pressure only" : "supports object and layout review",
  };
});

const priorEvidenceRows = [
  ...sidePairRows.map((row) => ({
    item: row.item,
    evidence_type: "side_pair_recheck",
    evidence_path: row.evidence_path,
    expected_role: row.gate,
    exists: "yes",
    bytes: "",
    width_px: "",
    height_px: "",
    observation: row.observation,
    strictness_effect: row.status,
  })),
  {
    item: "blind_key_charlie",
    evidence_type: "blind_packet_key",
    evidence_path: sktdBlind.source_crop ?? "",
    expected_role: sktdBlind.role ?? "",
    exists: sktdBlind.object_key ? "yes" : "no",
    bytes: "",
    width_px: "",
    height_px: "",
    observation: `${sktdBlind.current_status ?? ""}; ${sktdBlind.why_in_packet ?? ""}`,
    strictness_effect: "boxed-window-compatible only, not strict",
  },
  {
    item: "adjudication_n005",
    evidence_type: "token_boundary_adjudication",
    evidence_path: sktdAdjudication.boxed_overlay ?? "",
    expected_role: sktdAdjudication.role ?? "",
    exists: sktdAdjudication.object_key ? "yes" : "no",
    bytes: "",
    width_px: "",
    height_px: "",
    observation: `${sktdAdjudication.boundary_verdict ?? ""}; ${sktdAdjudication.identity_verdict ?? ""}; confidence=${sktdAdjudication.confidence ?? ""}`,
    strictness_effect: sktdAdjudication.consequence ?? "",
  },
  {
    item: "impact_h1993_only",
    evidence_type: "source_upgrade_scenario",
    evidence_path: rel(impactPath),
    expected_role: "test whether H-1993 alone unlocks 004",
    exists: "yes",
    bytes: "",
    width_px: "",
    height_px: "",
    observation: `strict splits=${h1993Only.strict_matched_prev_split_count}; unlocks=${h1993Only.unlocks}`,
    strictness_effect: "H-1993 alone is insufficient while Sktd-1 is not strict",
  },
  {
    item: "impact_sktd1_only",
    evidence_type: "source_upgrade_scenario",
    evidence_path: rel(impactPath),
    expected_role: "test whether Sktd-1 alone unlocks 004",
    exists: "yes",
    bytes: "",
    width_px: "",
    height_px: "",
    observation: `strict splits=${sktdOnly.strict_matched_prev_split_count}; unlocks=${sktdOnly.unlocks}`,
    strictness_effect: "Sktd-1 alone only expands 125 continuation; it does not create a matched split",
  },
  {
    item: "impact_h1993_and_sktd1",
    evidence_type: "source_upgrade_scenario",
    evidence_path: rel(impactPath),
    expected_role: "upper-bound dual strict 004 test",
    exists: "yes",
    bytes: "",
    width_px: "",
    height_px: "",
    observation: `strict splits=${both004.strict_matched_prev_split_count}; splits=${both004.strict_matched_prev_splits}`,
    strictness_effect: "004 unlocks only if both sides become strict, or an equivalent dual strict pair appears",
  },
];

const evidenceRows = [...imageRows, ...priorEvidenceRows];

const tests = [
  {
    test: "object_side_pair_label_visible",
    criterion: "public page must visibly bind Sktd-1 A/a to the Surkotada row",
    evidence: "CISI India leaf n397 labels Sktd-1 A and Sktd-1 a",
    result: "pass",
    consequence: "Sktd-1 stays source-panel side-pair bound at the object/side level",
  },
  {
    test: "top_band_window_compatible",
    criterion: "top-band crop must preserve a plausible 002-390-125 window",
    evidence: `${sktdBlind.local_window ?? ""}; ${sktdAdjudication.token_boxes ?? ""}`,
    result: "pass_downweighted",
    consequence: "the window is useful as visual pressure but not as source-derived numeric proof",
  },
  {
    test: "single_line_full_sequence",
    criterion: "the local six-token row must be visible as one clean source line",
    evidence: "full panels show top inscription band plus separate lower-field sign",
    result: "fail_wrapped_layout",
    consequence: "the full +390-004-002-390-125-820+ order remains catalog-mediated",
  },
  {
    test: "lower_field_sign_order",
    criterion: "the lower-field sign must be independently ordered relative to the top band",
    evidence: "source panel shows the sign in a separate field, not in the top inscription band",
    result: "fail_catalog_mediated",
    consequence: "the 125->820 continuation cannot be counted as strict source-token order",
  },
  {
    test: "blind_source_window_preserved",
    criterion: "blind/adjudication rows must reach source-window-preserved proof",
    evidence: `${sktdAdjudication.boundary_verdict ?? ""}; ${sktdAdjudication.identity_verdict ?? ""}`,
    result: "fail_boxed_compatible_only",
    consequence: "Sktd-1 remains below M-119/M-735 strict 125 witnesses",
  },
  {
    test: "dual_004_split_ready",
    criterion: "004 lane needs strict H-1993 and strict Sktd-1, or equivalent dual strict witnesses",
    evidence: `H-1993-only splits=${h1993Only.strict_matched_prev_split_count}; Sktd-only splits=${sktdOnly.strict_matched_prev_split_count}; both splits=${both004.strict_matched_prev_split_count}`,
    result: "fail_not_ready",
    consequence: "no strict 004 matched-predecessor split can be claimed from the current public Sktd-1 panel",
  },
];

const decisions = [
  {
    decision: "sktd1_is_panel_bound_not_strict",
    evidence: "side-pair labels are visible, but the layout is wrapped",
    result: "Sktd-1 remains source-panel side-pair visible and token-order blocked",
    consequence: "do not promote Sktd-1 to strict 004->002-390->125->820 evidence",
  },
  {
    decision: "same_public_plate_is_exhausted_for_strictness",
    evidence: "full panels, signband crops, blind key, and adjudication all stop at boxed-window compatibility",
    result: "no local reclassification makes Sktd-1 strict",
    consequence: "future Sktd-1 promotion needs a cleaner publication/caption/plate or independent artifact description",
  },
  {
    decision: "004_lane_still_needs_dual_strict_evidence",
    evidence: `H-1993-only=${h1993Only.strict_matched_prev_split_count}; Sktd-only=${sktdOnly.strict_matched_prev_split_count}; both=${both004.strict_matched_prev_split_count}`,
    result: "current 004 lane stays blocked",
    consequence: "continue with H-1993 acquisition plus a stricter Sktd-1 source, or find a replacement 004 witness pair",
  },
];

writeCsv(
  path.join(reportsDir, `${prefix}_evidence_rows.csv`),
  evidenceRows,
  ["item", "evidence_type", "evidence_path", "expected_role", "exists", "bytes", "width_px", "height_px", "observation", "strictness_effect"],
);

writeCsv(
  path.join(reportsDir, `${prefix}_strictness_tests.csv`),
  tests,
  ["test", "criterion", "evidence", "result", "consequence"],
);

writeCsv(
  path.join(reportsDir, `${prefix}_decisions.csv`),
  decisions,
  ["decision", "evidence", "result", "consequence"],
);

const summary = {
  run_date: "2026-05-31",
  inputs: {
    side_pair_recheck: rel(sidePairPath),
    token_boundary_adjudication: rel(adjudicationPath),
    blind_key: rel(blindKeyPath),
    source_upgrade_impact: rel(impactPath),
  },
  target: {
    object: "Sktd-1",
    row_id: "3875.1",
    local_text: "+390-004-002-390-125-820+",
    lane: "004 -> 002-390 -> 125 -> 820",
  },
  image_count: imageRows.length,
  tests,
  decisions,
  status: "sktd1_strictness_audit_wrapped_layout_blocks_dual004_no_values",
  outputs: {
    evidence_rows: `data/open_prototype/reports/${prefix}_evidence_rows.csv`,
    strictness_tests: `data/open_prototype/reports/${prefix}_strictness_tests.csv`,
    decisions: `data/open_prototype/reports/${prefix}_decisions.csv`,
    summary: `data/open_prototype/reports/${prefix}_summary.json`,
  },
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
