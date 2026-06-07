import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_dependency_opener_counterfactual_20260531';
const checkedDate = '2026-05-31';

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

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
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

function topCounts(items, fn, n = 10) {
  return countBy(items, fn)
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function entropy(items, fn) {
  if (!items.length) return 0;
  const counts = countBy(items, fn);
  let h = 0;
  for (const [, count] of counts) {
    const p = count / items.length;
    h -= p * Math.log2(p);
  }
  return h;
}

function findMotif(rows, motif) {
  const motifTokens = motif.split('-');
  const hits = [];
  for (const row of rows) {
    for (let i = 0; i <= row.tokens.length - motifTokens.length; i += 1) {
      if (!motifTokens.every((token, offset) => row.tokens[i + offset] === token)) continue;
      hits.push({
        checked_date: checkedDate,
        motif,
        cisi: objectId(row),
        row_id: row.id,
        site: row.site,
        type: row.type,
        shape: row.shape,
        prev_before_motif: row.tokens[i - 1] ?? '<START>',
        next_after_motif: row.tokens[i + motifTokens.length] ?? '<END>',
        after_002: String(row.tokens[i - 1] === '002'),
        terminal_after_motif: String(!row.tokens[i + motifTokens.length]),
        left_prefix: row.tokens.slice(0, i).join('-') || '<START>',
        right_suffix: row.tokens.slice(i + motifTokens.length).join('-') || '<END>',
        local_context: row.tokens.slice(Math.max(0, i - 4), Math.min(row.tokens.length, i + motifTokens.length + 4)).join('-'),
        exact_sequence: row.tokens.join(' '),
        text: row.text,
      });
    }
  }
  return hits;
}

function summarizeLane(label, motif, hits) {
  const topNext = countBy(hits, (hit) => hit.next_after_motif)[0] ?? ['-', 0];
  return {
    checked_date: checkedDate,
    label,
    motif,
    hits: String(hits.length),
    sites: topCounts(hits, (hit) => hit.site),
    types: topCounts(hits, (hit) => hit.type),
    shapes: topCounts(hits, (hit) => hit.shape),
    terminal: String(hits.filter((hit) => hit.terminal_after_motif === 'true').length),
    terminal_share: hits.length ? (hits.filter((hit) => hit.terminal_after_motif === 'true').length / hits.length).toFixed(6) : '0.000000',
    distinct_next: String(new Set(hits.map((hit) => hit.next_after_motif)).size),
    next_entropy: entropy(hits, (hit) => hit.next_after_motif).toFixed(6),
    top_next: topNext[0],
    top_next_share: hits.length ? (topNext[1] / hits.length).toFixed(6) : '0.000000',
    top_next_counts: topCounts(hits, (hit) => hit.next_after_motif),
    examples: hits.slice(0, 12).map((hit) => `${hit.cisi}:${hit.text}`).join(' | '),
  };
}

function contrastDecision(motif, after002, other) {
  if (motif === '390') {
    const afterDiverse = Number(after002.distinct_next) >= 6 && Number(after002.top_next_share) <= 0.35;
    const otherDiverse = Number(other.distinct_next) >= 40 && Number(other.top_next_share) <= 0.35;
    const otherFormula = other.top_next === '590' && Number(other.top_next_share) >= 0.4;
    if (afterDiverse && otherDiverse) return 'wild_shot_damaged_non002_390_also_diverse';
    if (afterDiverse && otherFormula) return 'candidate_strengthened_002_opens_390_selector_lane';
    return 'candidate_damaged_390_contrast_weak';
  }
  if (motif === '405') {
    return after002.top_next === '501' && Number(after002.top_next_share) > 0.7
      ? 'formula_head_control_002_does_not_make_every_head_open'
      : 'mixed_405_control';
  }
  if (motif === '610') {
    return Number(after002.hits) === 2 && Number(other.hits) === 0
      ? 'candidate_610_only_known_under_002'
      : 'demote_610_if_other_lane_exists';
  }
  if (motif === '297-350') {
    return Number(after002.hits) === 2 && Number(other.hits) === 0
      ? 'candidate_pair_only_known_under_002'
      : 'demote_pair_if_other_lane_exists';
  }
  if (motif === '095') {
    return Number(after002.terminal_share) === 1 && Number(other.terminal_share) < 1
      ? 'candidate_002_conditions_095_terminal_status'
      : 'mixed_095_not_enough_for_dependency_claim';
  }
  if (motif === '705') {
    return Number(after002.terminal_share) === 1
      ? 'candidate_source_weak_705_terminal_under_002'
      : 'mixed_705';
  }
  return 'background';
}

function buildContrast(rows, motif) {
  const hits = findMotif(rows, motif);
  const after002Hits = hits.filter((hit) => hit.after_002 === 'true');
  const otherHits = hits.filter((hit) => hit.after_002 !== 'true');
  const after002 = summarizeLane('after_002', motif, after002Hits);
  const other = summarizeLane('not_after_002', motif, otherHits);
  return {
    checked_date: checkedDate,
    motif,
    after_002_hits: after002.hits,
    not_after_002_hits: other.hits,
    after_002_top_next: after002.top_next_counts,
    not_after_002_top_next: other.top_next_counts,
    after_002_distinct_next: after002.distinct_next,
    not_after_002_distinct_next: other.distinct_next,
    after_002_entropy: after002.next_entropy,
    not_after_002_entropy: other.next_entropy,
    after_002_terminal_share: after002.terminal_share,
    not_after_002_terminal_share: other.terminal_share,
    decision: contrastDecision(motif, after002, other),
    falsifier: falsifierFor(motif),
    laneRows: [after002, other],
    hitRows: hits,
  };
}

function falsifierFor(motif) {
  if (motif === '390') return 'A large non-002 `390-X` set with the same selector diversity, or source collapse of post-002 `390-X`, kills the dependency contrast.';
  if (motif === '405') return '`405` becoming diverse after `002` would stop it being the formula-head control.';
  if (motif === '610') return 'Any credible non-002 `610` row damages the 002-governed rare-head bet.';
  if (motif === '297-350') return 'Any credible non-002 `297-350` row or post-002 non-125-413 continuation damages the pair-head bet.';
  if (motif === '095') return 'A source-bound continuing `002-390-095-Y` kills terminal-status wording.';
  if (motif === '705') return 'A source-bound continuing `002-390-705-Y` kills terminal-selector wording.';
  return 'Background contrast.';
}

fs.mkdirSync(reportsDir, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  tokens: signs(row.text),
}));
const canonicalRows = [...new Map(rawRows.map((row) => [row.tokens.join(' '), row])).values()];

const motifs = ['390', '405', '610', '297-350', '095', '705'];
const contrasts = motifs.map((motif) => buildContrast(canonicalRows, motif));
const contrastRows = contrasts.map(({ laneRows, hitRows, ...row }) => row);
const laneRows = contrasts.flatMap((row) => row.laneRows);
const hitRows = contrasts.flatMap((row) => row.hitRows);

const decisions = [
  {
    checked_date: checkedDate,
    bet_id: 'V1_002_DEPENDENCY_OPENER_FOR_390_20260531',
    confidence_tier: contrastRows.find((row) => row.motif === '390')?.decision.includes('candidate_strengthened') ? 'candidate' : 'wild shot',
    decision: contrastRows.find((row) => row.motif === '390')?.decision,
    risky_parse_bet:
      '`002` changes `390` from the ordinary `390-590` formula lane into a governed selector-head lane.',
    what_would_promote:
      'More source-visible post-`002` `390-X` rows retain selector diversity while non-`002` `390` remains formula-dominated.',
    what_would_break:
      'Non-`002` `390-X` rows show comparable diversity, or post-`002` `390-X` collapses into copied/source-noisy families.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'V1_002_UNIVERSAL_OPENER_20260531',
    confidence_tier: 'dead',
    decision: 'dead_as_universal_rule',
    risky_parse_bet: '`002` makes every following head open and selector-bearing.',
    what_would_promote: 'No current path; the `405` and closure-head controls already block it.',
    what_would_break: '`405-501` and terminal closure heads are enough to kill the universal version.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'V2_390_OPEN_SELECTOR_HEAD_UNDER_002_20260531',
    confidence_tier: 'candidate',
    decision: 'candidate_narrowed_to_local_branch_table_not_dependency_contrast',
    risky_parse_bet:
      '`390` is an open selector head inside the `002-390-X` frame, while `610` and `297-350` are rarer head-level carriers in the same governed ecology.',
    what_would_promote:
      'A held-out source-visible `002-390-X` row follows the open/closed selector predictions without copied-register collapse.',
    what_would_break:
      'The post-`002` `390` branch table collapses to visual-register copying or arbitrary personal-name material.',
  },
];

const summary = {
  checked_date: checkedDate,
  status: 'dependency_opener_counterfactual',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: canonicalRows.length,
  },
  decisions: decisions.map((row) => `${row.bet_id}:${row.decision}`).join(';'),
  key_result:
    'The simple contrast proof is damaged: post-`002` `390` has a compact branch table, but non-`002` `390` is also diverse. `002` remains a local parser cue, not proven dependency morphology.',
  next_parser_move:
    'Keep `002` as a wild-shot dependency opener and a candidate frame cue. Score each head as closure/formula/open before reading its tail.',
};

writeCsv(path.join(reportsDir, `${prefix}_contrasts.csv`), contrastRows, [
  'checked_date',
  'motif',
  'after_002_hits',
  'not_after_002_hits',
  'after_002_top_next',
  'not_after_002_top_next',
  'after_002_distinct_next',
  'not_after_002_distinct_next',
  'after_002_entropy',
  'not_after_002_entropy',
  'after_002_terminal_share',
  'not_after_002_terminal_share',
  'decision',
  'falsifier',
]);

writeCsv(path.join(reportsDir, `${prefix}_lane_summaries.csv`), laneRows, [
  'checked_date',
  'label',
  'motif',
  'hits',
  'sites',
  'types',
  'shapes',
  'terminal',
  'terminal_share',
  'distinct_next',
  'next_entropy',
  'top_next',
  'top_next_share',
  'top_next_counts',
  'examples',
]);

writeCsv(path.join(reportsDir, `${prefix}_hit_rows.csv`), hitRows, [
  'checked_date',
  'motif',
  'cisi',
  'row_id',
  'site',
  'type',
  'shape',
  'prev_before_motif',
  'next_after_motif',
  'after_002',
  'terminal_after_motif',
  'left_prefix',
  'right_suffix',
  'local_context',
  'exact_sequence',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  'checked_date',
  'bet_id',
  'confidence_tier',
  'decision',
  'risky_parse_bet',
  'what_would_promote',
  'what_would_break',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
