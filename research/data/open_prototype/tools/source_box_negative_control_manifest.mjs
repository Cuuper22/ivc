import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const tmpDir = path.join(base, 'tmp');
const blindDir = path.join(tmpDir, 'source_box_blind_packet_v1');

const lipiPath = path.join(reportsDir, 'lipi_scope_rows.csv');
const sourceVisiblePath = path.join(reportsDir, 'source_visible_032_002_y_witness_matrix.csv');
const overlapPath = path.join(reportsDir, 'overlap_probe.csv');
const panelGraphPath = path.join(reportsDir, 'lipi_frame700_034_source_panel_graph_nodes.csv');

const outCandidates = path.join(reportsDir, 'source_box_negative_control_candidates.csv');
const outBlindPacket = path.join(reportsDir, 'source_box_blind_adjudication_packet.csv');
const outBlindKey = path.join(reportsDir, 'source_box_blind_adjudication_key.csv');
const outSummary = path.join(reportsDir, 'source_box_negative_control_summary.json');

const seedBase = Number(process.argv[2] ?? 20260529);
const maxNegativesInBlindPacket = Number(process.argv[3] ?? 12);

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQuotes) {
      if (c === '"') {
        if (text[i + 1] === '"') {
          field += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        field += c;
      }
    } else if (c === '"') {
      inQuotes = true;
    } else if (c === ',') {
      row.push(field);
      field = '';
    } else if (c === '\n') {
      row.push(field);
      field = '';
      if (row.length > 1 || row[0] !== '') rows.push(row);
      row = [];
    } else if (c !== '\r') {
      field += c;
    }
  }
  if (field.length || row.length) {
    row.push(field);
    rows.push(row);
  }
  return rows;
}

function loadCsv(filePath) {
  if (!fs.existsSync(filePath)) return [];
  const rows = parseCsv(fs.readFileSync(filePath, 'utf8'));
  const header = rows[0] ?? [];
  return rows.slice(1).map((row) => Object.fromEntries(header.map((name, index) => [name, row[index] ?? ''])));
}

function toCsv(rows) {
  return `${rows
    .map((row) =>
      row
        .map((value) => {
          const text = String(value ?? '');
          return `"${text.replaceAll('"', '""')}"`;
        })
        .join(','),
    )
    .join('\n')}\n`;
}

function parseTokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function countBy(rows, key) {
  const out = new Map();
  for (const row of rows) out.set(row[key] ?? '', (out.get(row[key] ?? '') ?? 0) + 1);
  return Object.fromEntries([...out.entries()].sort((a, b) => a[0].localeCompare(b[0])));
}

function cisiRegex(cisi) {
  const match = String(cisi ?? '').match(/^([A-Za-z]+)-?(\d+)$/);
  if (!match) return null;
  const [, prefix, number] = match;
  return new RegExp(`(^|[^a-z0-9])${prefix.toLowerCase()}[-_ ]?0*${number}(?![0-9])(?=[^a-z0-9]|$)`, 'i');
}

function walkFiles(root) {
  if (!fs.existsSync(root)) return [];
  const out = [];
  const stack = [root];
  const imageExtensions = new Set(['.png', '.jpg', '.jpeg', '.webp', '.tif', '.tiff', '.bmp']);
  while (stack.length) {
    const current = stack.pop();
    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      const full = path.join(current, entry.name);
      if (entry.isDirectory()) {
        stack.push(full);
      } else if (imageExtensions.has(path.extname(entry.name).toLowerCase())) {
        out.push(full);
      }
    }
  }
  return out.sort((a, b) => a.localeCompare(b));
}

function imageHitsForCisi(cisi, imagePaths) {
  const regex = cisiRegex(cisi);
  if (!regex) return [];
  return imagePaths.filter((imagePath) => regex.test(path.basename(imagePath).toLowerCase()));
}

function classifyControlPositions(tokens) {
  const out = [];
  for (let i = 0; i < tokens.length; i++) {
    const token = tokens[i];
    const prev = tokens[i - 1] ?? '';
    const next = tokens[i + 1] ?? '';
    if (token === '032' && next !== '002') {
      out.push({
        control_class: prev === '220' ? 'negative_220_032_next_not_002' : 'negative_032_next_not_002',
        control_position_index0: i,
        prev_token: prev,
        focus_token: token,
        next_token: next,
        y_after_002: '',
      });
    }
    if (token === '002' && next && prev !== '032') {
      out.push({
        control_class: 'negative_002_y_prev_not_032',
        control_position_index0: i,
        prev_token: prev,
        focus_token: token,
        next_token: next,
        y_after_002: next,
      });
    }
  }
  return out;
}

function firstExisting(paths) {
  return paths.find((candidate) => candidate && fs.existsSync(candidate)) ?? '';
}

function mulberry32(seed) {
  let value = seed >>> 0;
  return () => {
    value += 0x6d2b79f5;
    let t = value;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffle(items, rng) {
  const out = items.slice();
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function copyBlindImage(sourcePath, blindId) {
  const ext = path.extname(sourcePath).toLowerCase() || '.png';
  const dest = path.join(blindDir, `${blindId}${ext}`);
  fs.copyFileSync(sourcePath, dest);
  return dest;
}

const lipiRows = loadCsv(lipiPath);
const sourceRows = loadCsv(sourceVisiblePath);
const overlapRows = loadCsv(overlapPath);
const panelRows = loadCsv(panelGraphPath);
const imagePaths = walkFiles(tmpDir);

const sourceRouteCisi = new Set(sourceRows.map((row) => row.cisi).filter(Boolean));
const sourceVisibleRows = sourceRows.filter((row) => row.source_visible === 'yes');
const targetSites = new Set(sourceVisibleRows.map((row) => row.site).filter(Boolean));
const targetTypes = new Set(sourceVisibleRows.map((row) => row.type).filter(Boolean));
const targetSymbols = new Set(sourceVisibleRows.map((row) => row.symbol).filter(Boolean));
const targetLengths = sourceVisibleRows.map((row) => parseTokens(row.text).length).filter(Boolean);
const minTargetLength = Math.min(...targetLengths);
const maxTargetLength = Math.max(...targetLengths);

const overlapByCisi = new Map();
for (const row of overlapRows) {
  if (!row.cisi) continue;
  if (!overlapByCisi.has(row.cisi)) overlapByCisi.set(row.cisi, []);
  overlapByCisi.get(row.cisi).push(row);
}

const panelByCisi = new Map();
for (const row of panelRows) {
  if (!row.cisi) continue;
  if (!panelByCisi.has(row.cisi)) panelByCisi.set(row.cisi, []);
  panelByCisi.get(row.cisi).push(row);
}

const candidates = [];
for (const row of lipiRows) {
  if (row.readiness_bucket !== 'lipi_numeric_clean_candidate') continue;
  if (!row.cisi || row.cisi === '-') continue;
  if (sourceRouteCisi.has(row.cisi)) continue;

  const tokens = parseTokens(row.text);
  const controls = classifyControlPositions(tokens);
  if (!controls.length) continue;

  const localImageHits = imageHitsForCisi(row.cisi, imagePaths);
  const overlapHits = overlapByCisi.get(row.cisi) ?? [];
  const panelHits = panelByCisi.get(row.cisi) ?? [];
  const availabilityTier = localImageHits.length
    ? 'local_image_hit'
    : panelHits.length
      ? 'source_panel_graph'
      : overlapHits.length
        ? 'mayig_overlap_only'
        : 'metadata_only';

  for (const control of controls) {
    const classWeight =
      control.control_class === 'negative_220_032_next_not_002'
        ? 4
        : control.control_class === 'negative_032_next_not_002'
          ? 3
          : 2;
    const matchScore =
      classWeight +
      (localImageHits.length ? 6 : 0) +
      (panelHits.length ? 4 : 0) +
      (overlapHits.length ? 1 : 0) +
      (targetSites.has(row.site) ? 2 : 0) +
      (targetTypes.has(row.type) ? 2 : 0) +
      (targetSymbols.has(row.symbol) ? 1 : 0) +
      (tokens.length >= minTargetLength && tokens.length <= maxTargetLength ? 1 : 0);

    candidates.push({
      cisi: row.cisi,
      lipi_id: row.id,
      site: row.site,
      type: row.type,
      symbol: row.symbol,
      material: row.material,
      lipi_complete: row.complete,
      direction: row.direction,
      text: row.text,
      token_count: tokens.length,
      control_class: control.control_class,
      control_position_index0: control.control_position_index0,
      prev_token: control.prev_token,
      focus_token: control.focus_token,
      next_token: control.next_token,
      y_after_002: control.y_after_002,
      availability_tier: availabilityTier,
      local_image_hit_count: localImageHits.length,
      source_panel_graph_count: panelHits.length,
      mayig_overlap_count: overlapHits.length,
      same_site_as_source_visible: targetSites.has(row.site) ? 'yes' : 'no',
      same_type_as_source_visible: targetTypes.has(row.type) ? 'yes' : 'no',
      same_symbol_as_source_visible: targetSymbols.has(row.symbol) ? 'yes' : 'no',
      target_length_bucket_match: tokens.length >= minTargetLength && tokens.length <= maxTargetLength ? 'yes' : 'no',
      match_score: matchScore,
      local_image_paths_first5: localImageHits.slice(0, 5).join(';'),
      source_panel_graph_labels: panelHits
        .slice(0, 5)
        .map((hit) => hit.source_label)
        .filter(Boolean)
        .join(';'),
      mayig_paths: overlapHits
        .slice(0, 5)
        .map((hit) => hit.mayig_path)
        .filter(Boolean)
        .join(';'),
    });
  }
}

candidates.sort(
  (a, b) =>
    Number(b.match_score) - Number(a.match_score) ||
    Number(b.local_image_hit_count) - Number(a.local_image_hit_count) ||
    a.cisi.localeCompare(b.cisi) ||
    a.control_class.localeCompare(b.control_class),
);

fs.mkdirSync(path.dirname(outCandidates), { recursive: true });
fs.writeFileSync(
  outCandidates,
  toCsv([
    [
      'cisi',
      'lipi_id',
      'site',
      'type',
      'symbol',
      'material',
      'lipi_complete',
      'direction',
      'text',
      'token_count',
      'control_class',
      'control_position_index0',
      'prev_token',
      'focus_token',
      'next_token',
      'y_after_002',
      'availability_tier',
      'local_image_hit_count',
      'source_panel_graph_count',
      'mayig_overlap_count',
      'same_site_as_source_visible',
      'same_type_as_source_visible',
      'same_symbol_as_source_visible',
      'target_length_bucket_match',
      'match_score',
      'local_image_paths_first5',
      'source_panel_graph_labels',
      'mayig_paths',
    ],
    ...candidates.map((row) => [
      row.cisi,
      row.lipi_id,
      row.site,
      row.type,
      row.symbol,
      row.material,
      row.lipi_complete,
      row.direction,
      row.text,
      row.token_count,
      row.control_class,
      row.control_position_index0,
      row.prev_token,
      row.focus_token,
      row.next_token,
      row.y_after_002,
      row.availability_tier,
      row.local_image_hit_count,
      row.source_panel_graph_count,
      row.mayig_overlap_count,
      row.same_site_as_source_visible,
      row.same_type_as_source_visible,
      row.same_symbol_as_source_visible,
      row.target_length_bucket_match,
      row.match_score,
      row.local_image_paths_first5,
      row.source_panel_graph_labels,
      row.mayig_paths,
    ]),
  ]),
);

fs.rmSync(blindDir, { recursive: true, force: true });
fs.mkdirSync(blindDir, { recursive: true });

const positivePacketRows = sourceVisibleRows
  .map((row) => ({
    packet_truth: 'positive_source_visible_032_002_y',
    cisi: row.cisi,
    site: row.site,
    type: row.type,
    symbol: row.symbol,
    material: row.material,
    condition_or_lipi_complete: row.condition,
    direction: '',
    text: row.text,
    source_image: firstExisting([row.source_crop, row.token_box_overlay]),
    control_class: '',
    source_note: row.packet_status,
  }))
  .filter((row) => row.source_image);

const selectedNegatives = [];
const seenNegativeCisiClass = new Set();
for (const row of candidates) {
  if (!row.local_image_hit_count) continue;
  const key = `${row.cisi}:${row.control_class}`;
  if (seenNegativeCisiClass.has(key)) continue;
  seenNegativeCisiClass.add(key);
  selectedNegatives.push({
    packet_truth: row.control_class,
    cisi: row.cisi,
    site: row.site,
    type: row.type,
    symbol: row.symbol,
    material: row.material,
    condition_or_lipi_complete: row.lipi_complete,
    direction: row.direction,
    text: row.text,
    source_image: row.local_image_paths_first5.split(';')[0] ?? '',
    control_class: row.control_class,
    source_note: row.availability_tier,
  });
  if (selectedNegatives.length >= maxNegativesInBlindPacket) break;
}

const rng = mulberry32(seedBase);
const packetRows = shuffle([...positivePacketRows, ...selectedNegatives], rng);
const blindPacketRows = [];
const blindKeyRows = [];
for (let i = 0; i < packetRows.length; i++) {
  const row = packetRows[i];
  const blindId = `SBP1_${String(i + 1).padStart(3, '0')}`;
  const blindImage = copyBlindImage(row.source_image, blindId);
  blindPacketRows.push([
    blindId,
    blindImage,
    row.site,
    row.type,
    row.symbol,
    row.material,
    row.condition_or_lipi_complete,
    row.direction,
    'score_visible_032_002_y_packet_without_using_catalog_text',
  ]);
  blindKeyRows.push([
    blindId,
    row.packet_truth,
    row.cisi,
    row.text,
    row.control_class,
    row.source_image,
    row.source_note,
  ]);
}

fs.writeFileSync(
  outBlindPacket,
  toCsv([
    [
      'blind_id',
      'neutral_image_path',
      'site',
      'type',
      'symbol',
      'material',
      'condition_or_lipi_complete',
      'direction',
      'adjudication_task',
    ],
    ...blindPacketRows,
  ]),
);

fs.writeFileSync(
  outBlindKey,
  toCsv([['blind_id', 'truth_class', 'cisi', 'catalog_text', 'control_class', 'source_image_original', 'source_note'], ...blindKeyRows]),
);

const localImageCandidates = candidates.filter((row) => Number(row.local_image_hit_count) > 0);
const panelCandidates = candidates.filter((row) => Number(row.source_panel_graph_count) > 0);
const overlapCandidates = candidates.filter((row) => Number(row.mayig_overlap_count) > 0);
const summary = {
  date: '2026-05-29',
  seed: seedBase,
  source_visible_positive_rows_with_images: positivePacketRows.length,
  negative_candidate_positions: candidates.length,
  negative_candidate_unique_cisi: new Set(candidates.map((row) => row.cisi)).size,
  negative_candidate_positions_by_class: countBy(candidates, 'control_class'),
  negative_candidate_positions_by_availability_tier: countBy(candidates, 'availability_tier'),
  local_image_backed_negative_positions: localImageCandidates.length,
  local_image_backed_negative_unique_cisi: new Set(localImageCandidates.map((row) => row.cisi)).size,
  local_image_backed_negative_positions_by_class: countBy(localImageCandidates, 'control_class'),
  source_panel_graph_negative_positions: panelCandidates.length,
  source_panel_graph_negative_unique_cisi: new Set(panelCandidates.map((row) => row.cisi)).size,
  mayig_overlap_negative_positions: overlapCandidates.length,
  mayig_overlap_negative_unique_cisi: new Set(overlapCandidates.map((row) => row.cisi)).size,
  blind_packet: {
    directory: blindDir,
    packet_csv: outBlindPacket,
    key_csv: outBlindKey,
    rows_total: blindPacketRows.length,
    positives: positivePacketRows.length,
    negatives: selectedNegatives.length,
    negative_truth_classes: countBy(selectedNegatives, 'packet_truth'),
    note: 'The packet hides catalog text and copies images to neutral filenames, but site/type/symbol metadata remains visible for matching review. Original filenames and catalog texts are only in the key file.',
  },
  false_positive_rate_status: {
    source_box_adjudication_fpr: 'not_computed',
    reason: 'This script builds the negative-control image packet and truth key. It does not adjudicate whether a reviewer/model spuriously calls 032-002-Y in negative source images.',
    next_gate: 'Run blind adjudication on source_box_blind_adjudication_packet.csv, then compare decisions to source_box_blind_adjudication_key.csv.',
  },
  top_local_image_backed_negatives: localImageCandidates.slice(0, 20).map((row) => ({
    cisi: row.cisi,
    control_class: row.control_class,
    site: row.site,
    type: row.type,
    symbol: row.symbol,
    text: row.text,
    match_score: Number(row.match_score),
    local_image_hit_count: Number(row.local_image_hit_count),
    first_image: row.local_image_paths_first5.split(';')[0] ?? '',
  })),
};

fs.writeFileSync(outSummary, `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
