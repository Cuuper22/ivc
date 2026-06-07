import fs from 'fs';
import path from 'path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const outSummary = path.join(reportsDir, 'effective_unicity_directionality_source_queue_summary.json');
const outQueue = path.join(reportsDir, 'effective_unicity_directionality_source_queue.csv');
const outSourceIndex = path.join(reportsDir, 'effective_unicity_directionality_source_queue_source_index.csv');

const START = '<S>';
const END = '</S>';
const ALPHA = 0.1;

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;
  for (let index = 0; index < text.length; index++) {
    const char = text[index];
    if (inQuotes) {
      if (char === '"') {
        if (text[index + 1] === '"') {
          field += '"';
          index++;
        } else {
          inQuotes = false;
        }
      } else {
        field += char;
      }
    } else if (char === '"') {
      inQuotes = true;
    } else if (char === ',') {
      row.push(field);
      field = '';
    } else if (char === '\n') {
      row.push(field);
      rows.push(row);
      row = [];
      field = '';
    } else if (char !== '\r') {
      field += char;
    }
  }
  if (field.length || row.length) {
    row.push(field);
    rows.push(row);
  }
  return rows;
}

function loadCsv(filePath) {
  const parsed = parseCsv(fs.readFileSync(filePath, 'utf8'));
  const header = parsed[0] ?? [];
  return parsed.slice(1).filter((row) => row.length > 1).map((row) =>
    Object.fromEntries(header.map((name, index) => [name, row[index] ?? ''])),
  );
}

function csvEscape(value) {
  const text = String(value ?? '');
  if (/[",\n\r]/.test(text)) return `"${text.replaceAll('"', '""')}"`;
  return `"${text}"`;
}

function toCsv(rows, columns) {
  return `${columns.map(csvEscape).join(',')}\n${rows
    .map((row) => columns.map((column) => csvEscape(row[column])).join(','))
    .join('\n')}\n`;
}

function parseTokens(text) {
  return [...String(text).matchAll(/\d{3}/g)].map((match) => match[0]);
}

function normalize(value) {
  return String(value || '-').trim() || '-';
}

function transitions(tokens) {
  const sequence = [START, ...tokens, END];
  const pairs = [];
  for (let index = 0; index < sequence.length - 1; index++) {
    pairs.push([sequence[index], sequence[index + 1]]);
  }
  return pairs;
}

function addCounts(map, key, delta) {
  const next = (map.get(key) ?? 0) + delta;
  if (next === 0) map.delete(key);
  else map.set(key, next);
}

function buildCounts(records) {
  const vocab = new Set();
  const bigramCounts = new Map();
  const prevCounts = new Map();
  const rowCounts = records.map((record) => {
    const bigrams = new Map();
    const prevs = new Map();
    for (const token of record.tokens) vocab.add(token);
    for (const [prev, next] of transitions(record.tokens)) {
      const key = `${prev}\t${next}`;
      addCounts(bigramCounts, key, 1);
      addCounts(prevCounts, prev, 1);
      addCounts(bigrams, key, 1);
      addCounts(prevs, prev, 1);
    }
    return { bigrams, prevs };
  });
  return { vocab, bigramCounts, prevCounts, rowCounts };
}

function logProb(tokens, counts, rowIndex) {
  const outcomeCount = counts.vocab.size + 1;
  let total = 0;
  for (const [prev, next] of transitions(tokens)) {
    const key = `${prev}\t${next}`;
    const bigramCount = (counts.bigramCounts.get(key) ?? 0) - (counts.rowCounts[rowIndex]?.bigrams.get(key) ?? 0);
    const prevCount = (counts.prevCounts.get(prev) ?? 0) - (counts.rowCounts[rowIndex]?.prevs.get(prev) ?? 0);
    total += Math.log((bigramCount + ALPHA) / (prevCount + ALPHA * outcomeCount));
  }
  return total;
}

function scoreDirection(records) {
  const usable = records.filter((record) => record.tokens.length > 1);
  const counts = buildCounts(usable);
  let storedHigher = 0;
  let reversedHigher = 0;
  let ties = 0;
  let diffSum = 0;
  for (let rowIndex = 0; rowIndex < usable.length; rowIndex++) {
    const record = usable[rowIndex];
    const stored = logProb(record.tokens, counts, rowIndex);
    const reversed = logProb([...record.tokens].reverse(), counts, rowIndex);
    const diff = (stored - reversed) / (record.tokens.length + 1);
    diffSum += diff;
    if (Math.abs(diff) < 1e-12) ties++;
    else if (diff > 0) storedHigher++;
    else reversedHigher++;
  }
  return {
    rows: usable.length,
    tokens: usable.reduce((sum, record) => sum + record.tokens.length, 0),
    unique_tokens: new Set(usable.flatMap((record) => record.tokens)).size,
    stored_higher: storedHigher,
    reversed_higher: reversedHigher,
    ties,
    stored_win_share: usable.length ? storedHigher / usable.length : 0,
    mean_stored_minus_reversed_per_transition: usable.length ? diffSum / usable.length : 0,
  };
}

function scoreRows(records) {
  const counts = buildCounts(records);
  return records.map((record, rowIndex) => {
    const stored = logProb(record.tokens, counts, rowIndex);
    const reversed = logProb([...record.tokens].reverse(), counts, rowIndex);
    const diff = (stored - reversed) / (record.tokens.length + 1);
    let outcome = 'tie';
    if (diff > 1e-12) outcome = 'stored_higher';
    else if (diff < -1e-12) outcome = 'reversed_higher';
    return {
      id: record.id,
      stored_logprob: stored,
      reversed_logprob: reversed,
      diff_per_transition: diff,
      direction_outcome: outcome,
    };
  });
}

function round(value) {
  return Number.isFinite(value) ? Number(value.toFixed(6)) : '';
}

function groupBy(records, keyFn) {
  const groups = new Map();
  for (const record of records) {
    const key = keyFn(record);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(record);
  }
  return groups;
}

function uniqueSorted(values) {
  return [...new Set(values.filter(Boolean).map(String))].sort((a, b) => a.localeCompare(b));
}

function exactCollapse(records) {
  const byKey = new Map();
  for (const record of records) {
    const key = record.tokens.join(' ');
    if (!byKey.has(key)) {
      byKey.set(key, {
        ...record,
        source_ids: [record.id],
        source_cisis: [record.cisi],
        duplicate_weight: 1,
      });
    } else {
      const current = byKey.get(key);
      current.duplicate_weight++;
      current.source_ids.push(record.id);
      current.source_cisis.push(record.cisi);
    }
  }
  return [...byKey.values()].sort((a, b) => a.tokens.join(' ').localeCompare(b.tokens.join(' ')));
}

function chooseRepresentatives(groups, policyName) {
  return [...groups.values()].map((members, index) => {
    const representative = [...members].sort((a, b) => {
      const weightDiff = (b.duplicate_weight ?? 1) - (a.duplicate_weight ?? 1);
      if (weightDiff) return weightDiff;
      return a.tokens.join(' ').localeCompare(b.tokens.join(' '));
    })[0];
    return {
      ...representative,
      id: `${policyName}_${String(index + 1).padStart(5, '0')}`,
      family_size: members.length,
      family_source_weight: members.reduce((sum, member) => sum + (member.duplicate_weight ?? 1), 0),
      source_ids: members.flatMap((member) => member.source_ids ?? [member.id]),
      source_cisis: uniqueSorted(members.flatMap((member) => member.source_cisis ?? [member.cisi])),
      source_texts: uniqueSorted(members.map((member) => member.text)),
    };
  });
}

class UnionFind {
  constructor(size) {
    this.parent = Array.from({ length: size }, (_, index) => index);
    this.rank = Array.from({ length: size }, () => 0);
  }
  find(value) {
    if (this.parent[value] !== value) this.parent[value] = this.find(this.parent[value]);
    return this.parent[value];
  }
  union(a, b) {
    const rootA = this.find(a);
    const rootB = this.find(b);
    if (rootA === rootB) return;
    if (this.rank[rootA] < this.rank[rootB]) this.parent[rootA] = rootB;
    else if (this.rank[rootA] > this.rank[rootB]) this.parent[rootB] = rootA;
    else {
      this.parent[rootB] = rootA;
      this.rank[rootA]++;
    }
  }
}

function oneEditFamilyCollapse(records) {
  const uf = new UnionFind(records.length);
  const signatureToFirst = new Map();
  const addSignature = (signature, index) => {
    const first = signatureToFirst.get(signature);
    if (first === undefined) signatureToFirst.set(signature, index);
    else uf.union(first, index);
  };

  records.forEach((record, index) => {
    const tokens = record.tokens;
    for (let pos = 0; pos < tokens.length; pos++) {
      const wildcard = [...tokens];
      wildcard[pos] = '*';
      addSignature(`wild:${tokens.length}:${wildcard.join(' ')}`, index);
      addSignature(`del:${tokens.length - 1}:${tokens.filter((_, tokenIndex) => tokenIndex !== pos).join(' ')}`, index);
    }
  });

  const groups = new Map();
  records.forEach((record, index) => {
    const root = uf.find(index);
    if (!groups.has(root)) groups.set(root, []);
    groups.get(root).push(record);
  });
  return chooseRepresentatives(groups, 'one_edit_family');
}

function topEdgeRemoved(records, topN = 10) {
  const edgeCounts = new Map();
  for (const record of records) {
    const first = record.tokens[0];
    const last = record.tokens[record.tokens.length - 1];
    edgeCounts.set(first, (edgeCounts.get(first) ?? 0) + 1);
    edgeCounts.set(last, (edgeCounts.get(last) ?? 0) + 1);
  }
  const top = new Set([...edgeCounts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, topN)
    .map(([token]) => token));
  return records.filter((record) => !top.has(record.tokens[0]) && !top.has(record.tokens[record.tokens.length - 1]));
}

function loadHarshRecords() {
  const exact = exactCollapse(loadCsv(path.join(reportsDir, 'lipi_scope_rows.csv'))
    .filter((row) => row.readiness_bucket === 'lipi_numeric_clean_candidate')
    .map((row, index) => ({
      original_index: index + 1,
      id: row.id || `ivc_${index + 1}`,
      cisi: normalize(row.cisi),
      site: normalize(row.site),
      type: normalize(row.type),
      material: normalize(row.material),
      symbol: normalize(row.symbol),
      direction: normalize(row.direction),
      text: row.text,
      tokens: parseTokens(row.text),
    }))
    .filter((row) => row.tokens.length >= 2));
  return oneEditFamilyCollapse(topEdgeRemoved(exact, 10));
}

function statusRank(text) {
  const value = String(text || '').toLowerCase();
  if (!value) return 0;
  if (/(pass_.*candidate|pass_existing_token_box|source_visible_order_window_candidate|source_single_line.*yes)/.test(value)) return 85;
  if (/(candidate_pass|ready_for_token_box|source_visible_ready|same_line_candidate_present|token_box)/.test(value)) return 80;
  if (/(source_visible|public_route_visible|public_cisi_plate_page_found|downloaded_and_cropped)/.test(value)) return 65;
  if (/(public_cisi_plate_page|source_volume_ocr_hit|local source|source route known)/.test(value)) return 50;
  if (/(direct.*request|cisi_3_1|archive_required|needs_source_route|source_route_needed)/.test(value)) return 30;
  if (/(secondary_catalogue_only|data_register_not_source_panel|not_admissible)/.test(value)) return 15;
  return 5;
}

function firstPresent(row, columns) {
  for (const column of columns) {
    if (row[column]) return row[column];
  }
  return '';
}

function collectSourceRows() {
  const files = fs.readdirSync(reportsDir)
    .filter((file) => file.endsWith('.csv'))
    .filter((file) => /(source|route|crop|witness|adjudication|manifest|token_order)/i.test(file));
  const rows = [];
  for (const file of files) {
    const fullPath = path.join(reportsDir, file);
    let parsed = [];
    try {
      parsed = loadCsv(fullPath);
    } catch {
      continue;
    }
    for (const row of parsed) {
      const cisi = row.cisi || row.CISI || row.object_cisi || '';
      if (!cisi) continue;
      const statusText = [
        row.source_status,
        row.route_status,
        row.source_grade_status,
        row.current_admissible_use,
        row.admissibility,
        row.token_box_status,
        row.attachment_verdict,
        row.visual_status,
        row.evidence_grade_now,
        row.source_check_status,
        row.source_single_line ? `source_single_line:${row.source_single_line}` : '',
        row.order_verdict,
        row.confidence ? `confidence:${row.confidence}` : '',
        row.family_link,
        row.route_kind,
        row.best_route_kind,
        row.best_route_id,
      ].filter(Boolean).join(' | ');
      rows.push({
        cisi: normalize(cisi),
        source_file: file,
        rank: statusRank(statusText),
        status_text: statusText,
        source_url: firstPresent(row, ['source_url', 'best_source_url', 'ia_page_image_url', 'ia_reader_page_url']),
        local_image: firstPresent(row, [
          'source_image_abs',
          'source_crop',
          'face_crop_abs',
          'impression_crop_abs',
          'full_face_crop_abs',
          'full_impression_crop_abs',
          'local_crop_path',
          'local_page_path',
          'best_local_artifact',
          'overlay_abs',
          'token_box_overlay',
          'page_file',
        ]),
        sha256: firstPresent(row, ['source_sha256', 'source_image_sha256', 'crop_sha256', 'face_crop_sha256', 'impression_crop_sha256', 'best_artifact_sha256']),
        note: firstPresent(row, ['note', 'notes', 'observation', 'limit', 'blocker', 'next_action', 'route_next_action', 'source_request']),
      });
    }
  }
  return rows;
}

function buildSourceIndex() {
  const byCisi = groupBy(collectSourceRows(), (row) => row.cisi);
  const index = new Map();
  const sourceIndexRows = [];
  for (const [cisi, rows] of byCisi.entries()) {
    const sorted = [...rows].sort((a, b) => b.rank - a.rank || a.source_file.localeCompare(b.source_file));
    const best = sorted[0];
    const aggregate = {
      cisi,
      source_hint_count: rows.length,
      best_source_rank: best.rank,
      best_source_file: best.source_file,
      best_status_text: best.status_text,
      best_source_url: best.source_url,
      best_local_image: best.local_image,
      best_sha256: best.sha256,
      best_note: best.note,
      source_files: uniqueSorted(rows.map((row) => row.source_file)).slice(0, 12).join(';'),
    };
    index.set(cisi, aggregate);
    sourceIndexRows.push(aggregate);
  }
  sourceIndexRows.sort((a, b) => b.best_source_rank - a.best_source_rank || a.cisi.localeCompare(b.cisi));
  return { index, sourceIndexRows };
}

function sourceNeed(source) {
  if (!source) return 'find_public_or_request_source_route';
  if (source.best_source_rank >= 80) return 'review_existing_crop_for_direction_and_token_order';
  if (source.best_source_rank >= 65) return 'box_direction_from_existing_public_route';
  if (source.best_source_rank >= 50) return 'convert_route_hint_to_source_grade_crop';
  if (source.best_source_rank >= 30) return 'request_or_locate_source_image';
  return 'replace_non_source_grade_catalogue_hint';
}

function priorityBand(record, rowScore, source) {
  if (rowScore.direction_outcome === 'stored_higher' && rowScore.diff_per_transition >= 2) {
    return source?.best_source_rank >= 65 ? 'P0_validate_high_positive_existing_route' : 'P1_acquire_high_positive_source';
  }
  if (rowScore.direction_outcome === 'stored_higher') return 'P2_validate_positive_support';
  if (rowScore.direction_outcome === 'reversed_higher') return 'P1_audit_reversed_anomaly';
  return 'P3_tie_or_low_information';
}

function removalDelta(records, baseline, removeId) {
  const without = records.filter((record) => record.id !== removeId);
  if (without.length < 3) return '';
  const score = scoreDirection(without);
  return round(baseline.stored_win_share - score.stored_win_share);
}

const harshRecords = loadHarshRecords();
const majorRecords = harshRecords.filter((record) => record.site === 'Mohenjo-daro' || record.site === 'Harappa');
const mohenjoRecords = harshRecords.filter((record) => record.site === 'Mohenjo-daro');
const harappaRecords = harshRecords.filter((record) => record.site === 'Harappa');
const { index: sourceIndex, sourceIndexRows } = buildSourceIndex();

const baselines = {
  all_harsh: scoreDirection(harshRecords),
  major_sites: scoreDirection(majorRecords),
  mohenjo_daro: scoreDirection(mohenjoRecords),
  harappa: scoreDirection(harappaRecords),
};
const rowScores = new Map(scoreRows(majorRecords).map((row) => [row.id, row]));
const mohenjoBaseline = baselines.mohenjo_daro;
const harappaBaseline = baselines.harappa;
const majorBaseline = baselines.major_sites;

const queueRows = majorRecords.map((record) => {
  const rowScore = rowScores.get(record.id);
  const cisis = uniqueSorted(record.source_cisis?.length ? record.source_cisis : [record.cisi]);
  const sourceHints = cisis.map((cisi) => sourceIndex.get(cisi)).filter(Boolean);
  const source = sourceHints.sort((a, b) => b.best_source_rank - a.best_source_rank || a.cisi.localeCompare(b.cisi))[0];
  const siteBaseline = record.site === 'Mohenjo-daro' ? mohenjoBaseline : harappaBaseline;
  const siteRecords = record.site === 'Mohenjo-daro' ? mohenjoRecords : harappaRecords;
  return {
    priority_band: priorityBand(record, rowScore, source),
    source_validation_need: sourceNeed(source),
    representative_cisi: record.cisi,
    family_cisis: cisis.join(';'),
    representative_lipi_id: record.source_ids?.[0] ?? record.id,
    harsh_id: record.id,
    site: record.site,
    type: record.type,
    material: record.material,
    symbol: record.symbol,
    direction: record.direction,
    text: record.text,
    tokens: record.tokens.join(' '),
    token_count: record.tokens.length,
    family_size: record.family_size ?? 1,
    family_source_weight: record.family_source_weight ?? record.duplicate_weight ?? 1,
    direction_outcome: rowScore.direction_outcome,
    stored_logprob: round(rowScore.stored_logprob),
    reversed_logprob: round(rowScore.reversed_logprob),
    diff_per_transition: round(rowScore.diff_per_transition),
    major_leave_one_delta_stored_win: removalDelta(majorRecords, majorBaseline, record.id),
    site_leave_one_delta_stored_win: removalDelta(siteRecords, siteBaseline, record.id),
    source_hint_count: sourceHints.reduce((sum, hint) => sum + Number(hint.source_hint_count ?? 0), 0),
    best_source_rank: source?.best_source_rank ?? 0,
    best_source_file: source?.best_source_file ?? '',
    best_status_text: source?.best_status_text ?? '',
    best_source_url: source?.best_source_url ?? '',
    best_local_image: source?.best_local_image ?? '',
    best_sha256: source?.best_sha256 ?? '',
    best_note: source?.best_note ?? '',
    source_files: uniqueSorted(sourceHints.flatMap((hint) => String(hint.source_files || '').split(';'))).join(';'),
  };
});

queueRows.sort((a, b) => {
  const bandCompare = a.priority_band.localeCompare(b.priority_band);
  if (bandCompare) return bandCompare;
  return Number(b.diff_per_transition) - Number(a.diff_per_transition)
    || Number(b.best_source_rank) - Number(a.best_source_rank)
    || a.site.localeCompare(b.site)
    || a.representative_cisi.localeCompare(b.representative_cisi);
});

queueRows.forEach((row, index) => {
  row.queue_rank = index + 1;
});

const byNeed = Object.fromEntries([...groupBy(queueRows, (row) => row.source_validation_need).entries()]
  .map(([key, rows]) => [key, rows.length])
  .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])));
const byPriority = Object.fromEntries([...groupBy(queueRows, (row) => row.priority_band).entries()]
  .map(([key, rows]) => [key, rows.length])
  .sort((a, b) => a[0].localeCompare(b[0])));
const bySiteOutcome = Object.fromEntries([...groupBy(queueRows, (row) => `${row.site}|${row.direction_outcome}`).entries()]
  .map(([key, rows]) => [key, rows.length])
  .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])));

const summary = {
  date: '2026-05-29',
  generated_at_utc: new Date().toISOString(),
  purpose: 'Source-normalized acquisition queue for the harsh major-site directionality candidate.',
  input_scope: {
    base_scope: 'top10_edge_removed_one_edit_family_collapsed',
    all_harsh_rows: harshRecords.length,
    major_site_rows: majorRecords.length,
    mohenjo_daro_rows: mohenjoRecords.length,
    harappa_rows: harappaRecords.length,
  },
  baselines: Object.fromEntries(Object.entries(baselines).map(([key, score]) => [key, {
    rows: score.rows,
    tokens: score.tokens,
    unique_tokens: score.unique_tokens,
    stored_higher: score.stored_higher,
    reversed_higher: score.reversed_higher,
    ties: score.ties,
    stored_win_share: round(score.stored_win_share),
    mean_stored_minus_reversed_per_transition: round(score.mean_stored_minus_reversed_per_transition),
  }])),
  source_index: {
    cisi_with_any_source_hint: sourceIndexRows.length,
    source_csv_files_scanned: uniqueSorted(sourceIndexRows.flatMap((row) => row.source_files.split(';').filter(Boolean))).length,
  },
  queue_summary: {
    rows: queueRows.length,
    by_priority_band: byPriority,
    by_source_validation_need: byNeed,
    by_site_outcome: bySiteOutcome,
    top_25_existing_route_positive_rows: queueRows
      .filter((row) => row.direction_outcome === 'stored_higher' && Number(row.best_source_rank) >= 65)
      .slice(0, 25)
      .map((row) => ({
        queue_rank: row.queue_rank,
        cisi: row.representative_cisi,
        site: row.site,
        text: row.text,
        diff_per_transition: row.diff_per_transition,
        source_validation_need: row.source_validation_need,
        best_source_file: row.best_source_file,
        best_status_text: row.best_status_text,
      })),
  },
  interpretation_boundary: 'This is an acquisition and adversarial review queue only. It does not validate physical source-image direction, identify a language, assign phonetic values, assign sign meanings, or increment accepted claims.',
  artifact_files: [
    'data/open_prototype/tools/effective_unicity_directionality_source_queue.mjs',
    'data/open_prototype/reports/effective_unicity_directionality_source_queue_summary.json',
    'data/open_prototype/reports/effective_unicity_directionality_source_queue.csv',
    'data/open_prototype/reports/effective_unicity_directionality_source_queue_source_index.csv',
  ],
};

fs.writeFileSync(outSummary, `${JSON.stringify(summary, null, 2)}\n`);
fs.writeFileSync(outQueue, toCsv(queueRows, [
  'queue_rank',
  'priority_band',
  'source_validation_need',
  'representative_cisi',
  'family_cisis',
  'representative_lipi_id',
  'harsh_id',
  'site',
  'type',
  'material',
  'symbol',
  'direction',
  'text',
  'tokens',
  'token_count',
  'family_size',
  'family_source_weight',
  'direction_outcome',
  'stored_logprob',
  'reversed_logprob',
  'diff_per_transition',
  'major_leave_one_delta_stored_win',
  'site_leave_one_delta_stored_win',
  'source_hint_count',
  'best_source_rank',
  'best_source_file',
  'best_status_text',
  'best_source_url',
  'best_local_image',
  'best_sha256',
  'best_note',
  'source_files',
]));
fs.writeFileSync(outSourceIndex, toCsv(sourceIndexRows, [
  'cisi',
  'source_hint_count',
  'best_source_rank',
  'best_source_file',
  'best_status_text',
  'best_source_url',
  'best_local_image',
  'best_sha256',
  'best_note',
  'source_files',
]));

console.log(JSON.stringify({
  ok: true,
  queue_rows: queueRows.length,
  source_index_cisis: sourceIndexRows.length,
  major_site_stored_win_share: summary.baselines.major_sites.stored_win_share,
  by_source_validation_need: byNeed,
}, null, 2));
