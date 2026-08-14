// Probe for the parts of two suspected cross-site "title templates" built around sign 125:
// 610-125-032 and 297-350-125-413. If these are real templates, each component should have a
// job — 610 a rare governed title head, 297-350 a head+modifier pair, 413 and 032 terminal
// suffixes — and the templates should recur at more than one site. We read the filtered
// Indus inscription list (lipi/metadata_filtered.csv) and search for seven motifs (the two
// full templates and their sub-pieces) as exact consecutive sign runs, recording each hit
// with its site, object type, and surrounding context. A second pass profiles the six
// component signs globally so template-only behavior can be told apart from a sign's normal
// ecology. Writes motif-row, motif-summary, and sign-summary CSVs plus a JSON summary to
// data/open_prototype/reports.
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_cross_site_125_template_components_20260531';

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (ch === '"' && next === '"') {
        field += '"';
        i += 1;
      } else if (ch === '"') {
        quoted = false;
      } else {
        field += ch;
      }
    } else if (ch === '"') {
      quoted = true;
    } else if (ch === ',') {
      row.push(field);
      field = '';
    } else if (ch === '\n') {
      row.push(field.replace(/\r$/, ''));
      rows.push(row);
      row = [];
      field = '';
    } else {
      field += ch;
    }
  }
  if (field.length || row.length) {
    row.push(field.replace(/\r$/, ''));
    rows.push(row);
  }
  const header = rows.shift() ?? [];
  return rows
    .filter((r) => r.some((value) => value !== ''))
    .map((r) => Object.fromEntries(header.map((name, index) => [name, r[index] ?? ''])));
}

function csvEscape(value) {
  const text = String(value ?? '');
  return /[",\n\r]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(',')];
  for (const row of rows) lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function signs(text) {
  return [...String(text || '').matchAll(/\d{3}/g)].map((match) => match[0]);
}

function countBy(items, fn) {
  const counts = new Map();
  for (const item of items) {
    const key = fn(item) || '-';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()].sort(
    (a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }),
  );
}

function topCounts(counts, n = 10) {
  return counts
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function findMotif(rows, motif) {
  const motifTokens = motif.split('-');
  const hits = [];
  for (const row of rows) {
    for (let i = 0; i <= row.tokens.length - motifTokens.length; i += 1) {
      if (!motifTokens.every((token, offset) => row.tokens[i + offset] === token)) continue;
      hits.push({
        checked_date: '2026-05-31',
        motif,
        cisi: row.cisi || '-',
        row_id: row.id,
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        cult: row.cult,
        prev_before_motif: row.tokens[i - 1] ?? '<START>',
        next_after_motif: row.tokens[i + motifTokens.length] ?? '<END>',
        local_context: row.tokens.slice(Math.max(0, i - 3), Math.min(row.tokens.length, i + motifTokens.length + 3)).join('-'),
        text: row.text,
      });
    }
  }
  return hits;
}

function signStats(rows, sign) {
  const hits = [];
  for (const row of rows) {
    for (let i = 0; i < row.tokens.length; i += 1) {
      if (row.tokens[i] !== sign) continue;
      hits.push({
        row,
        prev: row.tokens[i - 1] ?? '<START>',
        next: row.tokens[i + 1] ?? '<END>',
      });
    }
  }
  return {
    sign,
    count: hits.length,
    top_prev: topCounts(countBy(hits, (hit) => hit.prev)),
    top_next: topCounts(countBy(hits, (hit) => hit.next)),
    top_sites: topCounts(countBy(hits, (hit) => hit.row.site)),
    top_types: topCounts(countBy(hits, (hit) => hit.row.type)),
  };
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  tokens: signs(row.text),
}));

const motifs = ['610-125-032', '297-350-125-413', '350-125-413', '125-413', '125-032', '610-125', '297-350'];
const motifRows = [];
const motifSummary = [];

for (const motif of motifs) {
  const hits = findMotif(rows, motif);
  motifRows.push(...hits);
  motifSummary.push({
    checked_date: '2026-05-31',
    motif,
    hits: String(hits.length),
    sites: topCounts(countBy(hits, (hit) => hit.site)),
    types: topCounts(countBy(hits, (hit) => hit.type)),
    prev_before_motif: topCounts(countBy(hits, (hit) => hit.prev_before_motif)),
    next_after_motif: topCounts(countBy(hits, (hit) => hit.next_after_motif)),
    model_implication:
      motif === '610-125-032'
        ? '610_is_candidate_governed_title_head_selecting_125_032'
        : motif === '297-350-125-413'
          ? '297_350_is_candidate_head_modifier_title_template'
          : motif === '125-413'
            ? '413_is_candidate_terminal_suffix_only_inside_297_350_125'
            : motif === '125-032'
              ? '032_terminal_title_tail_candidate_with_one_adversarial_non610_row'
              : 'component_background',
    examples: hits.map((hit) => `${hit.cisi}:${hit.text}`).join(' | '),
  });
}

const signSummary = ['610', '297', '350', '413', '125', '032'].map((sign) => ({
  checked_date: '2026-05-31',
  ...signStats(rows, sign),
}));

const summary = {
  checked_date: '2026-05-31',
  status: 'cross_site_125_template_component_probe',
  hypotheses_tested: [
    '`610` as a rare governed title head selecting `125-032`',
    '`297-350` as head+modifier selecting `125-413`',
    '`413` as terminal title suffix in the `297-350-125` template',
    '`032` as terminal title-tail in `610-125-032`, with adversarial non-610 row present',
  ],
  decisions: [
    '`610` becomes a candidate sign-function bet: all `610` occurrences are `002-610-125-032` across Harappa and Mohenjo-daro.',
    '`297-350-125-413` becomes a promoted candidate cross-site title-template, but not a sign value for `297` alone because `297` has wider uses.',
    '`413` is only a wild terminal-title suffix outside this exact template because globally it is dominated by `575-413` and `892-413` contexts.',
    '`032` remains a candidate terminal/pivot marker, not a title-specific suffix, because `125-032` has one non-610 adversarial row.',
  ],
  next_falsifier:
    'Source/visual checks for H-74, M-1665, Blk-1, and Ns-60 should attack whether the cross-site templates are real inscriptions in comparable orientation.',
};

writeCsv(path.join(reportsDir, `${prefix}_motif_rows.csv`), motifRows, [
  'checked_date',
  'motif',
  'cisi',
  'row_id',
  'site',
  'type',
  'symbol',
  'cult',
  'prev_before_motif',
  'next_after_motif',
  'local_context',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_motif_summary.csv`), motifSummary, [
  'checked_date',
  'motif',
  'hits',
  'sites',
  'types',
  'prev_before_motif',
  'next_after_motif',
  'model_implication',
  'examples',
]);

writeCsv(path.join(reportsDir, `${prefix}_sign_summary.csv`), signSummary, [
  'checked_date',
  'sign',
  'count',
  'top_prev',
  'top_next',
  'top_sites',
  'top_types',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
