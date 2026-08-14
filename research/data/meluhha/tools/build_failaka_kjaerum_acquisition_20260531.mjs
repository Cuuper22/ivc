#!/usr/bin/env node

// Source-acquisition ledger (2026-05-31) for the Failaka seal problem. Two Gulf
// seals in Kjaerum 1983 (catalogue nos. 279 and 319, Laursen 2010 nos. 12 and
// 13) are the best candidates for local Failaka rows 147.1/148.1, but nobody in
// this workspace has seen the actual catalogue pages. This script records every
// route tried to get them: the cached CDLI publication record 1773730 (each
// related artifact checked for "No. 279/319" in its exact reference), a DAI PDF
// download that may have been blocked by anti-bot HTML, and three bibliographic
// routes (Aarhus University Press, CiNii, Open Library). It reads the existing
// Gulf-type queue CSV, hashes every cached file with SHA-256, and writes one CSV
// row per route plus a JSON summary. It makes no claim: the recorded decision
// is that Kjaerum 279/319 stay unresolved and the CDLI record must not stand in
// as an object bridge.
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";

const root = process.cwd();
const tmpDir = path.join(root, "tmp", "v1_external_acquisition_20260531");
const cdliJsonPath = path.join(tmpDir, "cdli_publication_1773730_kjaerum_failaka.json");
const dainstPath = path.join(tmpDir, "dainst_gulf_indus_reference.pdf");
const bibliographicRoutes = [
  {
    record_id: "aarhus_university_press_kjaerum_1983",
    source_system: "Aarhus University Press",
    source_url: "https://en.unipress.dk/udgivelser/f/failakadilmun-the-second-millennium-settlements-danish-archaeological-investigations-in-kuwait/",
    file: "aarhus_university_press_failaka_kjaerum.html",
    exact_reference: "Publisher listing for Failaka/Dilmun 1:1, The Stamp and Cylinder Seals; 171 pages; hardback; published 1983; ISBN 87 8841 506 6.",
    next_gate: "use as publisher/bibliographic route; still requires actual catalogue pages for nos. 279 and 319",
  },
  {
    record_id: "cinii_bd0853856x_kjaerum_1983",
    source_system: "CiNii Books",
    source_url: "https://ci.nii.ac.jp/ncid/BD0853856X",
    file: "cinii_bd0853856x_kjaerum.html",
    exact_reference: "Library record for The stamp and cylinder seals: plates and catalogue descriptions by Poul Kjaerum; NCID BD0853856X; ISBN 8788415066; 171 p.; holding at University of Tsukuba.",
    next_gate: "physical-copy access route; inspect catalogue pages for nos. 279 and 319",
  },
  {
    record_id: "openlibrary_ol18985798w_failaka",
    source_system: "Open Library",
    source_url: "https://openlibrary.org/works/OL18985798W/Failaka_Dilmun_the_second_millennium_settlements",
    file: "openlibrary_ol18985798w_failaka.html",
    exact_reference: "Open Library work route for Failaka/Dilmun, the second millennium settlements.",
    next_gate: "bibliographic discovery route only; no catalogue-page evidence found",
  },
];
const queuePath = path.join(root, "data", "meluhha", "gulf_type_indus_external_queue.csv");
const outCsv = path.join(root, "data", "meluhha", "failaka_kjaerum_acquisition_20260531.csv");
const outSummary = path.join(root, "data", "meluhha", "failaka_kjaerum_acquisition_20260531_summary.json");

function sha256File(filePath) {
  return createHash("sha256").update(readFileSync(filePath)).digest("hex");
}

function csvEscape(value) {
  const text = value == null ? "" : String(value);
  if (/[",\r\n]/.test(text)) return `"${text.replace(/"/g, '""')}"`;
  return text;
}

function parseCsvLine(line) {
  const cells = [];
  let cell = "";
  let quoted = false;
  for (let i = 0; i < line.length; i += 1) {
    const ch = line[i];
    if (quoted) {
      if (ch === '"' && line[i + 1] === '"') {
        cell += '"';
        i += 1;
      } else if (ch === '"') {
        quoted = false;
      } else {
        cell += ch;
      }
    } else if (ch === '"') {
      quoted = true;
    } else if (ch === ",") {
      cells.push(cell);
      cell = "";
    } else {
      cell += ch;
    }
  }
  cells.push(cell);
  return cells;
}

function parseCsv(text) {
  const lines = text.trim().split(/\r?\n/);
  const header = parseCsvLine(lines.shift());
  return lines.map((line) => {
    const values = parseCsvLine(line);
    return Object.fromEntries(header.map((key, idx) => [key, values[idx] ?? ""]));
  });
}

function writeCsv(rows, filePath) {
  const header = [
    "record_id",
    "record_type",
    "source_system",
    "source_url",
    "source_path",
    "source_sha256",
    "laursen_no",
    "reference",
    "cdli_artifact",
    "exact_reference",
    "site_or_provenience",
    "artifact_type",
    "period",
    "local_candidate_rows",
    "target_status",
    "claim_status",
    "next_gate",
  ];
  const lines = [header.join(",")];
  for (const row of rows) {
    lines.push(header.map((key) => csvEscape(row[key])).join(","));
  }
  mkdirSync(path.dirname(filePath), { recursive: true });
  writeFileSync(filePath, `${lines.join("\n")}\n`);
}

if (!existsSync(cdliJsonPath)) {
  throw new Error(`Missing required CDLI cache: ${cdliJsonPath}`);
}
if (!existsSync(queuePath)) {
  throw new Error(`Missing Gulf Type queue: ${queuePath}`);
}

const cdliRaw = readFileSync(cdliJsonPath, "utf8");
const cdli = JSON.parse(cdliRaw);
const publication = Array.isArray(cdli) ? cdli[0] : cdli;
const cdliHash = sha256File(cdliJsonPath);
const queueRows = parseCsv(readFileSync(queuePath, "utf8"));
const failakaQueue = queueRows.filter((row) => row.laursen_no === "12" || row.laursen_no === "13");
const sourceRows = [];

for (const row of failakaQueue) {
  sourceRows.push({
    record_id: `laursen_${row.laursen_no}_failaka_${row.reference.toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_|_$/g, "")}`,
    record_type: "target_queue_row",
    source_system: "Laursen 2010 via existing queue",
    source_url: "https://www.harappa.com/sites/default/files/pdf/The_westward_transmission_of_Indus_Valle.pdf",
    source_path: queuePath,
    source_sha256: sha256File(queuePath),
    laursen_no: row.laursen_no,
    reference: row.reference,
    cdli_artifact: "",
    exact_reference: row.source_provenance,
    site_or_provenience: row.area_site,
    artifact_type: row.gulf_type_label,
    period: "",
    local_candidate_rows: row.current_workspace_link,
    target_status: "priority target unresolved at catalogue-page/object level",
    claim_status: "no external anchor; acquisition row only",
    next_gate: row.next_gate,
  });
}

for (const artifact of publication.artifacts ?? []) {
  const exactRef = artifact.entities_publication?.exact_reference ?? "";
  const noMatch = /\bNo\.?\s*(279|319)\b/i.test(exactRef) ? "target_number_present" : "not_target_catalogue_number";
  sourceRows.push({
    record_id: `cdli_p${artifact.id}`,
    record_type: "adjacent_cdli_publication_artifact",
    source_system: "CDLI",
    source_url: "https://cdli.earth/publications/1773730/json",
    source_path: cdliJsonPath,
    source_sha256: cdliHash,
    laursen_no: "",
    reference: publication.title,
    cdli_artifact: `P${artifact.id}`,
    exact_reference: exactRef,
    site_or_provenience: artifact.provenience?.provenience ?? "",
    artifact_type: artifact.artifact_type?.artifact_type ?? "",
    period: artifact.period?.period ?? "",
    local_candidate_rows: "",
    target_status: noMatch,
    claim_status: "not a Meluhha/Indus bridge in current workspace",
    next_gate: noMatch === "target_number_present"
      ? "inspect source image and local row mapping before any value test"
      : "do not use as Kjaerum 279/319 evidence",
  });
}

let dainstStatus = "not_fetched";
let dainstHash = "";
let dainstBytes = 0;
if (existsSync(dainstPath)) {
  dainstHash = sha256File(dainstPath);
  const bytes = readFileSync(dainstPath);
  dainstBytes = bytes.length;
  const head = bytes.subarray(0, 256).toString("utf8");
  dainstStatus = /Anubis|bot/i.test(head) ? "blocked_antibot_html_not_pdf" : "fetched_needs_manual_type_check";
  sourceRows.push({
    record_id: "dainst_2043_2440_4491_fetch",
    record_type: "blocked_source_route",
    source_system: "DAI publications",
    source_url: "https://publications.dainst.org/books/dai/catalog/download/2043/2440/4491?inline=1",
    source_path: dainstPath,
    source_sha256: dainstHash,
    laursen_no: "12;13",
    reference: "DAI download route surfaced by source acquisition search",
    cdli_artifact: "",
    exact_reference: "",
    site_or_provenience: "Failaka",
    artifact_type: "Gulf INDUS source-route candidate",
    period: "",
    local_candidate_rows: "candidate local Failaka rows 147.1/148.1 unresolved",
    target_status: dainstStatus,
    claim_status: "no source text extracted; no claim",
    next_gate: "obtain a real PDF or library scan; current local file is not acceptable evidence",
  });
}

let cachedBibliographicRoutes = 0;
for (const route of bibliographicRoutes) {
  const sourcePath = path.join(tmpDir, route.file);
  const hasCache = existsSync(sourcePath);
  if (hasCache) cachedBibliographicRoutes += 1;
  sourceRows.push({
    record_id: route.record_id,
    record_type: "bibliographic_access_route",
    source_system: route.source_system,
    source_url: route.source_url,
    source_path: hasCache ? sourcePath : "",
    source_sha256: hasCache ? sha256File(sourcePath) : "",
    laursen_no: "12;13",
    reference: "Kjaerum 1983 Failaka/Dilmun 1:1 source-access route",
    cdli_artifact: "",
    exact_reference: route.exact_reference,
    site_or_provenience: "Failaka",
    artifact_type: "book/catalogue route",
    period: "",
    local_candidate_rows: "candidate local Failaka rows 147.1/148.1 unresolved",
    target_status: "bibliographic_route_only_no_catalogue_page",
    claim_status: "no source page extracted; no claim",
    next_gate: route.next_gate,
  });
}

writeCsv(sourceRows, outCsv);

const targetNumbersInCdli = sourceRows
  .filter((row) => row.record_type === "adjacent_cdli_publication_artifact")
  .filter((row) => row.target_status === "target_number_present").length;

const summary = {
  date: "2026-05-31",
  vector: "V1 diffuse Meluhha bilingual source acquisition",
  publication: {
    cdli_publication_id: publication.id,
    designation: publication.designation,
    bibtexkey: publication.bibtexkey,
    title: publication.title,
    year: publication.year,
    source_url: "https://cdli.earth/publications/1773730/json",
    cached_path: cdliJsonPath,
    cached_sha256: cdliHash,
    related_artifact_count: publication.artifacts?.length ?? 0,
    related_artifacts_matching_laursen_279_or_319: targetNumbersInCdli,
  },
  bibliographic_access_routes: {
    routes_recorded: bibliographicRoutes.length,
    cached_routes: cachedBibliographicRoutes,
  },
  laursen_failaka_targets: failakaQueue.map((row) => ({
    laursen_no: row.laursen_no,
    reference: row.reference,
    site: row.area_site,
    current_workspace_link: row.current_workspace_link,
    current_anchor_status: row.current_anchor_status,
    next_gate: row.next_gate,
  })),
  dainst_route: {
    cached_path: existsSync(dainstPath) ? dainstPath : null,
    cached_sha256: dainstHash || null,
    byte_length: dainstBytes,
    status: dainstStatus,
  },
  output_csv: outCsv,
  output_csv_sha256: sha256File(outCsv),
  accepted_claim_increment: 0,
  decision: "source acquisition tightened; Kjaerum 279/319 remain unresolved and CDLI 1773730 must not be used as a substitute object bridge",
};

writeFileSync(outSummary, `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
