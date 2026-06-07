import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_125_template_attack_surface_20260531';
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

function topCounts(items, fn, n = 8) {
  return countBy(items, fn)
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function uniqueCount(items, fn) {
  return new Set(items.map(fn)).size;
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
        region: row.region,
        site: row.site,
        type: row.type,
        material: row.material,
        shape: row.shape,
        symbol: row.symbol,
        cult: row.cult,
        prev_before_motif: row.tokens[i - 1] ?? '<START>',
        next_after_motif: row.tokens[i + motifTokens.length] ?? '<END>',
        left_prefix: row.tokens.slice(0, i).join('-') || '<START>',
        right_suffix: row.tokens.slice(i + motifTokens.length).join('-') || '<END>',
        local_context: row.tokens.slice(Math.max(0, i - 4), Math.min(row.tokens.length, i + motifTokens.length + 4)).join('-'),
        is_after_002: String(row.tokens[i - 1] === '002'),
        is_terminal: String(!row.tokens[i + motifTokens.length]),
        exact_sequence: row.tokens.join(' '),
        text: row.text,
      });
    }
  }
  return hits;
}

function signHits(rows, sign) {
  const hits = [];
  for (const row of rows) {
    for (let i = 0; i < row.tokens.length; i += 1) {
      if (row.tokens[i] !== sign) continue;
      hits.push({
        checked_date: checkedDate,
        sign,
        cisi: objectId(row),
        row_id: row.id,
        region: row.region,
        site: row.site,
        type: row.type,
        material: row.material,
        shape: row.shape,
        symbol: row.symbol,
        cult: row.cult,
        prev: row.tokens[i - 1] ?? '<START>',
        next: row.tokens[i + 1] ?? '<END>',
        left_prefix: row.tokens.slice(0, i).join('-') || '<START>',
        right_suffix: row.tokens.slice(i + 1).join('-') || '<END>',
        local_context: row.tokens.slice(Math.max(0, i - 4), Math.min(row.tokens.length, i + 5)).join('-'),
        exact_sequence: row.tokens.join(' '),
        text: row.text,
      });
    }
  }
  return hits;
}

function attackForTemplate(name, fullMotif, rows, componentMotifs, signMotifs) {
  const full = findMotif(rows, fullMotif);
  const components = componentMotifs.map((motif) => {
    const hits = findMotif(rows, motif);
    const outsideFull = hits.filter((hit) => !hit.local_context.includes(fullMotif));
    return {
      checked_date: checkedDate,
      template_bet: name,
      component: motif,
      hit_type: 'motif',
      hits: String(hits.length),
      outside_full_template_hits: String(outsideFull.length),
      sites: topCounts(hits, (hit) => hit.site),
      prev: topCounts(hits, (hit) => hit.prev_before_motif),
      next: topCounts(hits, (hit) => hit.next_after_motif),
      implication: componentImplication(name, motif, hits, outsideFull),
      examples: hits.map((hit) => `${hit.cisi}:${hit.text}`).join(' | '),
    };
  });
  const signsTable = signMotifs.map((sign) => {
    const hits = signHits(rows, sign);
    const insideFull = hits.filter((hit) => hit.local_context.includes(fullMotif));
    return {
      checked_date: checkedDate,
      template_bet: name,
      component: sign,
      hit_type: 'sign',
      hits: String(hits.length),
      outside_full_template_hits: String(hits.length - insideFull.length),
      sites: topCounts(hits, (hit) => hit.site),
      prev: topCounts(hits, (hit) => hit.prev),
      next: topCounts(hits, (hit) => hit.next),
      implication: signImplication(name, sign, hits, insideFull),
      examples: hits.slice(0, 12).map((hit) => `${hit.cisi}:${hit.text}`).join(' | '),
    };
  });
  return {
    checked_date: checkedDate,
    template_bet: name,
    full_motif: fullMotif,
    full_hits: String(full.length),
    full_canonical_sequences: String(uniqueCount(full, (hit) => hit.exact_sequence)),
    full_sites: topCounts(full, (hit) => hit.site),
    full_types: topCounts(full, (hit) => hit.type),
    full_shapes: topCounts(full, (hit) => hit.shape),
    full_prev: topCounts(full, (hit) => hit.prev_before_motif),
    full_next: topCounts(full, (hit) => hit.next_after_motif),
    full_left_prefixes: String(uniqueCount(full, (hit) => hit.left_prefix)),
    full_terminal: String(full.filter((hit) => hit.is_terminal === 'true').length),
    template_decision: templateDecision(name, full, components),
    template_prediction: templatePrediction(name),
    examples: full.map((hit) => `${hit.cisi}:${hit.text}`).join(' | '),
    componentRows: [...components, ...signsTable],
    hitRows: full,
  };
}

function componentImplication(name, motif, hits, outsideFull) {
  if (name === '610_head' && motif === '610-125') {
    return outsideFull.length ? 'damages_610_head_specificity' : 'supports_610_selects_125';
  }
  if (name === '610_head' && motif === '125-032') {
    return outsideFull.length
      ? '032_tail_leaks_outside_610_so_tail_is_not_610_specific'
      : 'supports_125_032_tail_specificity';
  }
  if (name === '297_350_pair' && motif === '297-350') {
    return outsideFull.length ? 'kills_pair_as_template_head' : 'supports_297_350_pair_specificity';
  }
  if (name === '297_350_pair' && motif === '350-125') {
    return outsideFull.length ? 'kills_350_125_as_independent_unit' : 'supports_350_125_independent_unit';
  }
  if (name === '297_350_pair' && motif === '125-413') {
    return outsideFull.length ? 'damages_413_template_tail' : 'supports_413_as_exact_template_tail';
  }
  return hits.length ? 'background_pressure' : 'no_hits';
}

function signImplication(name, sign, hits, insideFull) {
  if (name === '610_head' && sign === '610') {
    return hits.length === insideFull.length ? 'supports_610_as_rare_governed_title_head' : 'damages_610_as_rare_head';
  }
  if (name === '297_350_pair' && sign === '297') {
    return hits.length === insideFull.length ? '297_alone_is_pair_locked_here' : '297_has_wider_uses_so_pair_not_single_sign_value';
  }
  if (name === '297_350_pair' && sign === '350') {
    return hits.length === insideFull.length ? '350_alone_is_pair_locked_here' : '350_has_wider_uses_so_pair_not_single_sign_value';
  }
  if (name === '297_350_pair' && sign === '413') {
    return hits.length === insideFull.length ? '413_template_tail_specific' : '413_has_wider_tail_ecology';
  }
  return hits.length ? 'component_background' : 'no_hits';
}

function templateDecision(name, full, components) {
  if (name === '610_head') {
    const fullClean = full.length === 2 && full.every((hit) => hit.prev_before_motif === '002' && hit.is_terminal === 'true');
    const has125032Leak = components.some(
      (row) => row.component === '125-032' && Number(row.outside_full_template_hits) > 0,
    );
    if (fullClean && has125032Leak) return 'candidate_strengthened_not_promoted_610_specific_head_with_leaky_032_tail';
    if (fullClean) return 'promoted_candidate_corpus_only';
    return 'demoted';
  }
  if (name === '297_350_pair') {
    const fullClean = full.length === 2 && full.every((hit) => hit.prev_before_motif === '002' && hit.is_terminal === 'true');
    const has350125Leak = components.some(
      (row) => row.component === '350-125' && Number(row.outside_full_template_hits) > 0,
    );
    const has125413Leak = components.some(
      (row) => row.component === '125-413' && Number(row.outside_full_template_hits) > 0,
    );
    if (fullClean && has350125Leak && !has125413Leak) {
      return 'candidate_strengthened_not_promoted_pair_head_with_template_tail';
    }
    if (fullClean) return 'candidate_pair_template';
    return 'demoted';
  }
  return 'background';
}

function templatePrediction(name) {
  if (name === '610_head') {
    return 'A newly recovered `610` should remain inside `002-610-125-032`; a `610` outside that phrase damages the rare-head bet immediately.';
  }
  if (name === '297_350_pair') {
    return 'A newly recovered `297-350` should select terminal `125-413`; `350-125` without `297` should continue to look like a different construction.';
  }
  return '';
}

fs.mkdirSync(reportsDir, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  tokens: signs(row.text),
}));
const canonicalRows = [...new Map(rawRows.map((row) => [row.tokens.join(' '), row])).values()];

const attacks = [
  attackForTemplate(
    '610_head',
    '610-125-032',
    canonicalRows,
    ['610-125', '125-032', '002-610-125-032'],
    ['610', '125', '032'],
  ),
  attackForTemplate(
    '297_350_pair',
    '297-350-125-413',
    canonicalRows,
    ['297-350', '350-125', '125-413', '002-297-350-125-413'],
    ['297', '350', '125', '413'],
  ),
];

const templateRows = attacks.map(({ componentRows, hitRows, ...row }) => row);
const componentRows = attacks.flatMap((attack) => attack.componentRows);
const hitRows = attacks.flatMap((attack) => attack.hitRows);

const decisions = [
  {
    checked_date: checkedDate,
    bet_id: 'V2_610_RARE_GOVERNED_TITLE_HEAD_20260531',
    confidence_tier: templateRows.find((row) => row.template_bet === '610_head')?.template_decision.includes('candidate')
      ? 'candidate'
      : 'wild shot',
    decision: templateRows.find((row) => row.template_bet === '610_head')?.template_decision,
    risky_parse_bet:
      '`610` contributes a rare governed title/head value that obligatorily selects the portable `125-032` tail in current data.',
    what_would_promote:
      'Independent source images for both H-74 and M-1665 preserve the same four-sign phrase and comparable orientation; a held-out `610` also selects `125-032`.',
    what_would_break:
      'Any credible `610` outside `002-610-125-032`, or source images showing either carrier is misread/non-comparable.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'V2_297_350_PAIR_HEAD_SELECTS_125_413_20260531',
    confidence_tier: templateRows.find((row) => row.template_bet === '297_350_pair')?.template_decision.includes('candidate')
      ? 'candidate'
      : 'wild shot',
    decision: templateRows.find((row) => row.template_bet === '297_350_pair')?.template_decision,
    risky_parse_bet:
      '`297-350` is a composite governed head or head+modifier that selects terminal `125-413`; `350-125` alone is not the unit.',
    what_would_promote:
      'Source images for Blk-1 and Ns-60 preserve the template; any new `297-350` continues with terminal `125-413`.',
    what_would_break:
      'A credible `297-350` with a different continuation, or `125-413` spreading outside this exact template in unrelated contexts.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'V4_125_BROAD_GOVERNED_TITLE_SUFFIX_20260531',
    confidence_tier: 'candidate',
    decision: 'candidate_mixed_not_promoted',
    risky_parse_bet:
      '`125` is a governed title/rank suffix family, but its value is tail-conditioned rather than a generic terminal closer.',
    what_would_promote:
      'More governed cross-site `H-125-tail` families survive source normalization and show tail-conditioned recurrence.',
    what_would_break:
      'Cross-site carrier rows collapse as copies/noisy readings, or frequency-matched non-125 signs show the same governed-template portability.',
  },
];

const summary = {
  checked_date: checkedDate,
  status: '125_template_attack_surface',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: canonicalRows.length,
  },
  decisions: decisions.map((row) => `${row.bet_id}:${row.decision}`).join(';'),
  high_value_damage:
    'The broad promoted `125` grammar should be downgraded to candidate_mixed_not_promoted: the two cross-site carriers survive corpus attack, but each still depends on source-weak rows.',
  new_parser_move:
    'Parse `610` and `297-350` as head-level carriers, not as alternate X values equivalent to `125/095/692/705`; parse `125` as a tail-bearing suffix inside those carriers.',
  next_falsifier:
    'Look for `610` outside `002-610-125-032`, `297-350` outside `002-297-350-125-413`, and `125-413` outside the exact pair-head template before doing more provenance work.',
};

writeCsv(path.join(reportsDir, `${prefix}_template_rows.csv`), templateRows, [
  'checked_date',
  'template_bet',
  'full_motif',
  'full_hits',
  'full_canonical_sequences',
  'full_sites',
  'full_types',
  'full_shapes',
  'full_prev',
  'full_next',
  'full_left_prefixes',
  'full_terminal',
  'template_decision',
  'template_prediction',
  'examples',
]);

writeCsv(path.join(reportsDir, `${prefix}_component_rows.csv`), componentRows, [
  'checked_date',
  'template_bet',
  'component',
  'hit_type',
  'hits',
  'outside_full_template_hits',
  'sites',
  'prev',
  'next',
  'implication',
  'examples',
]);

writeCsv(path.join(reportsDir, `${prefix}_hit_rows.csv`), hitRows, [
  'checked_date',
  'motif',
  'cisi',
  'row_id',
  'region',
  'site',
  'type',
  'material',
  'shape',
  'symbol',
  'cult',
  'prev_before_motif',
  'next_after_motif',
  'left_prefix',
  'right_suffix',
  'local_context',
  'is_after_002',
  'is_terminal',
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
