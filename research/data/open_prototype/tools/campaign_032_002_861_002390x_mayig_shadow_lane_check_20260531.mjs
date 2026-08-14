import fs from 'node:fs';
import path from 'node:path';

// The corpus exists in two independent transcriptions: the local Lipi numeric encoding
// (3-digit sign codes) and the Mayig P-namespace grapheme encoding. If the provisional
// crosswalk 032=P145, 002=P122, 390=P086 is right, the Lipi window 032-002-390 should cast a
// "shadow" P145-P122-P086 in Mayig — and any Mayig-only hit would be a new witness for the
// blocked 032 lane. This script runs that check. It reads the Mayig records index, the Lipi
// metadata, and the crosswalk edges CSV, then searches both corpora for their exact triple
// and joins hits by artifact. It also scans the looser Mayig pair P122-P086 and checks how
// each artifact's local Lipi text aligns (exact 002-390, a 002-405 collision, or no match),
// because P086 is a known collision point between Lipi 390 and 405. Finding: the shadow lane
// returns only M-70, already known, so no replacement witness; the pair route is unsafe.
// Writes exact-triple, pair-row, and P086 collision-edge CSVs plus a summary JSON to
// reports/, all with accepted_decipherment_claim=0.

const ROOT = process.cwd();
const REPORTS = path.join(ROOT, 'data', 'open_prototype', 'reports');
const MAYIG = path.join(ROOT, 'data', 'open_prototype', 'mayig', 'records_index.csv');
const LIPI = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const EDGES = path.join(ROOT, 'data', 'sign_crosswalk', 'crosswalk_edges.csv');

const EXACT_OUT = path.join(
  REPORTS,
  'campaign_032_002_861_002390x_mayig_shadow_lane_check_20260531_exact_triples.csv',
);
const PAIR_OUT = path.join(
  REPORTS,
  'campaign_032_002_861_002390x_mayig_shadow_lane_check_20260531_p122p086_rows.csv',
);
const COLLISION_OUT = path.join(
  REPORTS,
  'campaign_032_002_861_002390x_mayig_shadow_lane_check_20260531_p086_collision_edges.csv',
);
const SUMMARY_OUT = path.join(
  REPORTS,
  'campaign_032_002_861_002390x_mayig_shadow_lane_check_20260531_summary.json',
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
  if (!rows.length) return [];
  const header = rows.shift();
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

function graphemes(row) {
  return String(row.graphemes || '').split(/\s+/).filter(Boolean);
}

function findWindows(tokens, window) {
  const hits = [];
  for (let i = 0; i <= tokens.length - window.length; i += 1) {
    if (tokens.slice(i, i + window.length).join(' ') === window.join(' ')) hits.push(i);
  }
  return hits;
}

function numericWindowClass(tokens) {
  const exact = findWindows(tokens, ['002', '390']);
  const collision405 = findWindows(tokens, ['002', '405']);
  if (exact.length) return { status: 'local_exact_002_390', index: exact[0], next: tokens[exact[0] + 2] ?? '' };
  if (collision405.length) {
    return {
      status: 'local_002_405_collision_not_002_390',
      index: collision405[0],
      next: tokens[collision405[0] + 2] ?? '',
    };
  }
  return { status: 'local_no_002_pair_match', index: -1, next: '' };
}

function countBy(rows, key) {
  const counts = {};
  for (const row of rows) counts[row[key] || ''] = (counts[row[key] || ''] ?? 0) + 1;
  return Object.fromEntries(Object.entries(counts).sort((a, b) => a[0].localeCompare(b[0])));
}

function bestReverseEdges(edges, mayigSign) {
  return edges
    .filter((edge) => edge.to_sign_uid === `mayig_p:${mayigSign}`)
    .sort((a, b) => Number(b.support_count) - Number(a.support_count))
    .slice(0, 4)
    .map((edge) => `${edge.from_sign_uid.replace('lipi_numeric:', '')}:${edge.support_count}/${edge.counterexample_count}:${edge.confidence}:accepted_${edge.accepted_for_analysis}`)
    .join(';');
}

fs.mkdirSync(REPORTS, { recursive: true });

const mayig = parseCsv(fs.readFileSync(MAYIG, 'utf8'));
const lipi = parseCsv(fs.readFileSync(LIPI, 'utf8'));
const edges = parseCsv(fs.readFileSync(EDGES, 'utf8'));

const lipiByCisi = new Map();
for (const row of lipi) {
  if (!lipiByCisi.has(row.cisi)) lipiByCisi.set(row.cisi, []);
  lipiByCisi.get(row.cisi).push(row);
}

const mayigExact = [];
const mayigPairs = [];
for (const row of mayig) {
  const signs = graphemes(row);
  for (let i = 0; i <= signs.length - 3; i += 1) {
    if (signs.slice(i, i + 3).join(' ') === 'P145 P122 P086') {
      mayigExact.push({
        row_type: 'mayig_exact_P145_P122_P086',
        artifact: row.artifact_base,
        side: row.side_id,
        site_or_description: row.description,
        prev: signs[i - 1] ?? '',
        target_window: 'P145 P122 P086',
        next: signs[i + 3] ?? '',
        source_sequence: signs.join(' '),
        local_row_id: '',
        local_cisi: '',
        local_site: '',
        local_text: '',
        local_status: '',
        accepted_decipherment_claim: '0',
      });
    }
  }
  for (let i = 0; i <= signs.length - 2; i += 1) {
    if (signs.slice(i, i + 2).join(' ') === 'P122 P086') {
      const localRows = lipiByCisi.get(row.artifact_base) ?? [];
      const localSummaries = localRows.map((local) => {
        const tokens = textTokens(local.text);
        const cls = numericWindowClass(tokens);
        return {
          id: local.id,
          text: local.text,
          status: cls.status,
          next: cls.next,
        };
      });
      const localStatus = localSummaries.length
        ? [...new Set(localSummaries.map((local) => local.status))].join(';')
        : 'no_local_cisi_row';
      mayigPairs.push({
        artifact: row.artifact_base,
        side: row.side_id,
        description: row.description,
        mayig_prev: signs[i - 1] ?? '',
        mayig_pair: 'P122 P086',
        mayig_next: signs[i + 2] ?? '',
        mayig_next_top_lipi_edges: bestReverseEdges(edges, signs[i + 2] ?? ''),
        mayig_sequence: signs.join(' '),
        local_status: localStatus,
        local_rows: localSummaries.map((local) => `${local.id}:${local.text}:${local.status}:next_${local.next}`).join(' || '),
        accepted_decipherment_claim: '0',
      });
    }
  }
}

const lipiExact = [];
for (const row of lipi) {
  const tokens = textTokens(row.text);
  for (let i = 0; i <= tokens.length - 3; i += 1) {
    if (tokens.slice(i, i + 3).join(' ') === '032 002 390') {
      lipiExact.push({
        row_type: 'lipi_exact_032_002_390',
        artifact: row.cisi || row.id,
        side: '',
        site_or_description: row.site,
        prev: tokens[i - 1] ?? '',
        target_window: '032 002 390',
        next: tokens[i + 3] ?? '',
        source_sequence: tokens.join(' '),
        local_row_id: row.id,
        local_cisi: row.cisi,
        local_site: row.site,
        local_text: row.text,
        local_status: row.cisi === '-' ? 'dash_cisi_unbound' : 'local_metadata_row',
        accepted_decipherment_claim: '0',
      });
    }
  }
}

const p086CollisionEdges = edges
  .filter((edge) => edge.to_sign_uid === 'mayig_p:P086')
  .sort((a, b) => Number(b.support_count) - Number(a.support_count))
  .map((edge) => ({
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
  EXACT_OUT,
  [...mayigExact, ...lipiExact],
  [
    'row_type',
    'artifact',
    'side',
    'site_or_description',
    'prev',
    'target_window',
    'next',
    'source_sequence',
    'local_row_id',
    'local_cisi',
    'local_site',
    'local_text',
    'local_status',
    'accepted_decipherment_claim',
  ],
);
writeCsv(
  PAIR_OUT,
  mayigPairs,
  [
    'artifact',
    'side',
    'description',
    'mayig_prev',
    'mayig_pair',
    'mayig_next',
    'mayig_next_top_lipi_edges',
    'mayig_sequence',
    'local_status',
    'local_rows',
    'accepted_decipherment_claim',
  ],
);
writeCsv(
  COLLISION_OUT,
  p086CollisionEdges,
  [
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

const exactShared = mayigExact
  .map((row) => row.artifact)
  .filter((artifact) => lipiExact.some((row) => row.local_cisi === artifact));

const summary = {
  checked_date: '2026-05-31',
  status: 'mayig_shadow_exact_032_lane_no_replacement_pair_collision_guard_no_values',
  source_layer: 'Mayig public-git P namespace plus local provisional crosswalk edges; all edges remain accepted_for_analysis=false.',
  exact_mayig_P145_P122_P086_count: mayigExact.length,
  exact_lipi_032_002_390_count: lipiExact.length,
  exact_shared_artifacts: exactShared,
  exact_shadow_new_replacement_witnesses: mayigExact.filter((row) => !exactShared.includes(row.artifact)).map((row) => row.artifact),
  broader_mayig_P122_P086_count: mayigPairs.length,
  broader_mayig_P122_P086_local_status_counts: countBy(mayigPairs, 'local_status'),
  mayig_next_counts_after_P122_P086: countBy(mayigPairs, 'mayig_next'),
  p086_reverse_edges: p086CollisionEdges,
  decision: [
    'The exact P145-P122-P086 shadow lane returns only M-70, already the known strict-visible 032-002-390-692 row.',
    'The shadow lane adds no replacement for the blocked 3335.1 032-lane witness.',
    'The broader Mayig P122-P086 pair is unsafe as an inflation route because M-34 and M-41 align locally to 002-405 rather than adjacent 002-390.',
    'Use this result as a crosswalk/corpus triage guard only; it does not accept a sign mapping, grammar, value, phonetics, language identity, function, sign meaning, or translation.',
  ],
  accepted_value_claims: 0,
  accepted_phonetic_claims: 0,
  accepted_language_identity_claims: 0,
  accepted_function_claims: 0,
  accepted_sign_meaning_claims: 0,
  accepted_translation_claims: 0,
};

fs.writeFileSync(SUMMARY_OUT, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
