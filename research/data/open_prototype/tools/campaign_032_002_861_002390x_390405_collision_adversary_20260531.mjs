// Adversarial test of a sign-collision temptation: the crosswalk maps both
// local sign 390 and local sign 405 toward the same Mayig sign P086, so should
// we treat 390 and 405 as one sign inside the 002-head ecology? To answer, this
// script extracts every 002-390 and 002-405 frame from the local Lipi metadata
// (recording the next sign, tail, terminality, and register fields), summarizes
// each head->next pair, and pulls the unaccepted crosswalk edges pointing at
// P086 with their support and counterexample counts. Writes the frames CSV, a
// head-next summary CSV, the P086 edge list, and a summary JSON to
// data/open_prototype/reports/. The recorded decision: no collapse — the
// 002-405 field is dominated by one repeated Harappa TAB:B formula
// (+520-240-002-405-501+), so P086 pressure is a warning label on future
// crosswalk use, not a license to merge 390 and 405. No value is accepted.

import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const REPORTS = path.join(ROOT, 'data', 'open_prototype', 'reports');
const LIPI = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const EDGES = path.join(ROOT, 'data', 'sign_crosswalk', 'crosswalk_edges.csv');

const FRAMES_OUT = path.join(
  REPORTS,
  'campaign_032_002_861_002390x_390405_collision_adversary_20260531_frames.csv',
);
const SUMMARY_OUT = path.join(
  REPORTS,
  'campaign_032_002_861_002390x_390405_collision_adversary_20260531_head_next_summary.csv',
);
const COLLISION_OUT = path.join(
  REPORTS,
  'campaign_032_002_861_002390x_390405_collision_adversary_20260531_p086_edges.csv',
);
const JSON_OUT = path.join(
  REPORTS,
  'campaign_032_002_861_002390x_390405_collision_adversary_20260531_summary.json',
);

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = '';
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (ch === '"' && next === '"') {
        cell += '"';
        i += 1;
      } else if (ch === '"') {
        quoted = false;
      } else {
        cell += ch;
      }
    } else if (ch === '"') {
      quoted = true;
    } else if (ch === ',') {
      row.push(cell);
      cell = '';
    } else if (ch === '\n') {
      row.push(cell.replace(/\r$/, ''));
      rows.push(row);
      row = [];
      cell = '';
    } else {
      cell += ch;
    }
  }
  if (cell.length || row.length) {
    row.push(cell.replace(/\r$/, ''));
    rows.push(row);
  }
  const header = rows.shift() ?? [];
  return rows
    .filter((r) => r.some((value) => value !== ''))
    .map((r) => Object.fromEntries(header.map((key, index) => [key, r[index] ?? ''])));
}

function csvEscape(value) {
  const text = String(value ?? '');
  if (/[",\n\r]/.test(text)) return `"${text.replaceAll('"', '""')}"`;
  return text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(',')];
  for (const row of rows) lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function textTokens(text) {
  return String(text || '')
    .replaceAll('+', '')
    .replaceAll('[', '')
    .replaceAll(']', '')
    .split('-')
    .map((token) => token.trim())
    .filter((token) => /^\d{3}$/.test(token));
}

function countBy(rows, keyFn) {
  const counts = {};
  for (const row of rows) {
    const key = keyFn(row);
    counts[key] = (counts[key] ?? 0) + 1;
  }
  return Object.fromEntries(Object.entries(counts).sort((a, b) => a[0].localeCompare(b[0], undefined, { numeric: true })));
}

function countString(rows, keyFn) {
  return Object.entries(countBy(rows, keyFn))
    .map(([key, count]) => `${key}:${count}`)
    .join(';');
}

function frameRows(lipiRows, head) {
  const rows = [];
  for (const row of lipiRows) {
    const tokens = textTokens(row.text);
    for (let i = 0; i < tokens.length - 1; i += 1) {
      if (tokens[i] !== '002' || tokens[i + 1] !== head) continue;
      const next = tokens[i + 2] ?? '<END>';
      rows.push({
        checked_date: '2026-05-31',
        id: row.id,
        cisi: row.cisi,
        site: row.site,
        type: row.type,
        material: row.material,
        shape: row.shape,
        symbol: row.symbol,
        cult: row.cult,
        direction: row['dir.'],
        prev: tokens[i - 1] ?? '<START>',
        head,
        next,
        tail_after_head: tokens.slice(i + 2).join('-') || '<END>',
        terminal_after_next: String(i + 2 === tokens.length - 1),
        text: row.text,
        normalized_text: tokens.join('-'),
        formula_key: `${row.site}|${row.type}|${row.shape}|${row.symbol}|${row.cult}|${row.text}`,
        accepted_decipherment_claim: '0',
      });
    }
  }
  return rows;
}

fs.mkdirSync(REPORTS, { recursive: true });

const lipi = parseCsv(fs.readFileSync(LIPI, 'utf8'));
const edges = parseCsv(fs.readFileSync(EDGES, 'utf8'));

const frames390 = frameRows(lipi, '390');
const frames405 = frameRows(lipi, '405');
const frames = [...frames390, ...frames405].sort(
  (a, b) =>
    a.head.localeCompare(b.head, undefined, { numeric: true }) ||
    a.next.localeCompare(b.next, undefined, { numeric: true }) ||
    a.id.localeCompare(b.id, undefined, { numeric: true }),
);

const groups = new Map();
for (const row of frames) {
  const key = `${row.head}->${row.next}`;
  if (!groups.has(key)) groups.set(key, []);
  groups.get(key).push(row);
}

const summaryRows = [...groups.entries()]
  .sort((a, b) => a[0].localeCompare(b[0], undefined, { numeric: true }))
  .map(([key, rows]) => ({
    checked_date: '2026-05-31',
    head_next: key,
    head: rows[0].head,
    next: rows[0].next,
    frame_count: String(rows.length),
    terminal_count: String(rows.filter((row) => row.terminal_after_next === 'true').length),
    continuing_count: String(rows.filter((row) => row.terminal_after_next !== 'true').length),
    exact_text_count: String(new Set(rows.map((row) => row.text)).size),
    cisi_examples: rows.slice(0, 12).map((row) => row.cisi).join(';'),
    register_counts: countString(rows, (row) => `${row.site}|${row.type}|${row.shape}|${row.symbol}|${row.cult}`),
    previous_sign_counts: countString(rows, (row) => row.prev),
    text_examples: [...new Set(rows.map((row) => row.text))].slice(0, 6).join(' || '),
    accepted_decipherment_claim: '0',
  }));

const p086Edges = edges
  .filter((edge) => edge.to_sign_uid === 'mayig_p:P086')
  .sort((a, b) => Number(b.support_count) - Number(a.support_count))
  .map((edge) => ({
    checked_date: '2026-05-31',
    lipi_sign: edge.from_sign_uid.replace('lipi_numeric:', ''),
    mayig_sign: edge.to_sign_uid.replace('mayig_p:', ''),
    support_count: edge.support_count,
    counterexample_count: edge.counterexample_count,
    top_share: edge.top_share,
    confidence: edge.confidence,
    accepted_for_analysis: edge.accepted_for_analysis,
    review_status: edge.review_status,
    example_witnesses: edge.example_witnesses,
    accepted_decipherment_claim: '0',
  }));

writeCsv(
  FRAMES_OUT,
  frames,
  [
    'checked_date',
    'id',
    'cisi',
    'site',
    'type',
    'material',
    'shape',
    'symbol',
    'cult',
    'direction',
    'prev',
    'head',
    'next',
    'tail_after_head',
    'terminal_after_next',
    'text',
    'normalized_text',
    'formula_key',
    'accepted_decipherment_claim',
  ],
);
writeCsv(
  SUMMARY_OUT,
  summaryRows,
  [
    'checked_date',
    'head_next',
    'head',
    'next',
    'frame_count',
    'terminal_count',
    'continuing_count',
    'exact_text_count',
    'cisi_examples',
    'register_counts',
    'previous_sign_counts',
    'text_examples',
    'accepted_decipherment_claim',
  ],
);
writeCsv(
  COLLISION_OUT,
  p086Edges,
  [
    'checked_date',
    'lipi_sign',
    'mayig_sign',
    'support_count',
    'counterexample_count',
    'top_share',
    'confidence',
    'accepted_for_analysis',
    'review_status',
    'example_witnesses',
    'accepted_decipherment_claim',
  ],
);

const repeated405501 = frames405.filter((row) => row.next === '501');
const summary = {
  checked_date: '2026-05-31',
  status: '390405_collision_adversary_blocks_p086_collapse_no_values',
  question: 'Does Mayig P086 pressure justify collapsing local 390 and 405 inside the 002-head ecology?',
  counts: {
    adjacent_002_390_frames: frames390.length,
    adjacent_002_405_frames: frames405.length,
    collapsed_002_390_or_405_frames: frames.length,
  },
  branch_counts_390: countBy(frames390, (row) => row.next),
  branch_counts_405: countBy(frames405, (row) => row.next),
  branch_counts_collapsed: countBy(frames, (row) => `${row.head}->${row.next}`),
  p086_edges: p086Edges,
  dominant_405_cluster: {
    next_501_count: repeated405501.length,
    exact_text_counts: countBy(repeated405501, (row) => row.text),
    register_counts: countBy(repeated405501, (row) => `${row.site}|${row.type}|${row.shape}|${row.symbol}|${row.cult}`),
  },
  adversarial_decision: [
    'Local 405 cannot be blindly collapsed into 390 from Mayig P086 pressure.',
    'The adjacent 002-405 field is larger than the 002-390 field but is dominated by a repeated Harappa cylindrical TAB:B formula, +520-240-002-405-501+.',
    'The Mohenjo collision rows M-34 and M-41 are useful warnings, not replacements for the 002-390-X matched lanes.',
    'The exact 002-390-X ecology remains a live object, but any future crosswalk-normalized use of Mayig P086 must carry this 390/405 collision guard.',
  ],
  accepted_value_claims: 0,
  accepted_phonetic_claims: 0,
  accepted_language_identity_claims: 0,
  accepted_function_claims: 0,
  accepted_sign_meaning_claims: 0,
  accepted_translation_claims: 0,
};

fs.writeFileSync(JSON_OUT, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
