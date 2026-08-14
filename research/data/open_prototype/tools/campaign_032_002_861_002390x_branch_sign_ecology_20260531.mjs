// Maps the "ecology" of the four focus branch signs (125, 095, 692, 705): how
// each behaves everywhere it appears in the local Lipi metadata, not just after
// the 002-390 frame. For every occurrence it records position, the two signs on
// each side, whether the sequence ends there, and whether it sits inside a
// 002-390 frame; it also extracts every 002-390 frame with its branch sign and
// tail. From these it builds per-sign summaries (terminal versus continuing,
// inside versus outside the frame), a per-branch frame summary, and an
// exceptions list (capped at 50 rows per test) for cases that stress the model,
// like a terminal 125 or a continuing non-125. Each object carries a source
// tier from the active delegation checkpoint (see CHECKPOINT_SOURCE_STATUS);
// a hand-written source-binding recheck table records why the Dholavira,
// M-1825, and H-1993 routes are still not strict evidence. Writes six CSVs and
// a summary JSON to data/open_prototype/reports/. No linguistic value follows:
// the ecology supports testing a constructional slot, nothing more.

import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const REPORTS = path.join(ROOT, 'data', 'open_prototype', 'reports');
const METADATA = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const PREFIX = 'campaign_032_002_861_002390x_branch_sign_ecology_20260531';

const OUT_OCCURRENCES = path.join(REPORTS, `${PREFIX}_occurrences.csv`);
const OUT_FRAMES = path.join(REPORTS, `${PREFIX}_002390_frames.csv`);
const OUT_SIGN_SUMMARY = path.join(REPORTS, `${PREFIX}_summary_by_sign.csv`);
const OUT_FRAME_BRANCH_SUMMARY = path.join(REPORTS, `${PREFIX}_002390_branch_summary.csv`);
const OUT_EXCEPTIONS = path.join(REPORTS, `${PREFIX}_exceptions.csv`);
const OUT_SOURCE_RECHECK = path.join(REPORTS, `${PREFIX}_source_binding_recheck.csv`);
const OUT_SUMMARY = path.join(REPORTS, `${PREFIX}_summary.json`);

const RUN_DATE = '2026-05-31';
const FOCUS_SIGNS = new Set(['125', '095', '692', '705']);

// Source tiers copied only from the active delegation checkpoint, not from
// successor-era tables. Everything else stays metadata-only until re-bound.
const CHECKPOINT_SOURCE_STATUS = new Map([
  ['H-1993', 'source_route_triaged_supplement_only_no_image'],
  ['H-773', 'source_panel_acquired_boxed_window_compatible_token_not_strict'],
  ['M-70', 'checkpoint_strict_source_visible'],
  ['M-71', 'checkpoint_strict_source_visible'],
  ['M-119', 'checkpoint_strict_source_visible'],
  ['M-735', 'checkpoint_strict_source_visible'],
  ['Sktd-1', 'checkpoint_permissive_public_panel'],
  ['M-1825', 'm1825_ia_pakistan_absent_secondary_icon_only_no_signband'],
  ['-:4237.1', 'dholavira_8758_cluster_unbound_image_conflict'],
]);

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
      if (row.some((value) => value.length)) rows.push(row);
      row = [];
      cell = '';
    } else {
      cell += ch;
    }
  }
  if (cell.length || row.length) {
    row.push(cell.replace(/\r$/, ''));
    if (row.some((value) => value.length)) rows.push(row);
  }
  const [header, ...body] = rows;
  return body.map((cols) => Object.fromEntries(header.map((name, idx) => [name, cols[idx] ?? ''])));
}

function csvEscape(value) {
  const text = String(value ?? '');
  if (/[",\r\n]/.test(text)) return `"${text.replaceAll('"', '""')}"`;
  return text;
}

function writeCsv(file, rows, fields) {
  const body = rows.map((row) => fields.map((field) => csvEscape(row[field])).join(',')).join('\n');
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`);
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function objectId(row) {
  const cisi = String(row.cisi ?? '').trim();
  if (cisi && cisi !== '-') return cisi;
  return `-:${row.id}`;
}

function clean(value) {
  const text = String(value ?? '').trim();
  return text && text !== '-' ? text : '';
}

function boolText(value) {
  return value ? 'True' : 'False';
}

function tailText(values) {
  return values.length ? values.join(' ') : '<END>';
}

function contextCell(row) {
  return [
    clean(row.site) || 'Unknown',
    clean(row.type) || 'Unknown',
    clean(row.symbol) || 'None',
    clean(row.cult) || 'None',
    clean(row.shape) || 'Unknown',
    clean(row.material) || 'Unknown',
  ].join('|');
}

function bump(map, key, by = 1) {
  map.set(key, (map.get(key) ?? 0) + by);
}

function addSet(map, key, value) {
  if (!map.has(key)) map.set(key, new Set());
  if (value) map.get(key).add(value);
}

function sourceStatusFor(object) {
  return CHECKPOINT_SOURCE_STATUS.get(object) ?? 'metadata_only_unbound';
}

function metadataRecord(row) {
  return {
    id: row.id,
    object: objectId(row),
    site: clean(row.site) || 'Unknown',
    type: clean(row.type) || 'Unknown',
    symbol: clean(row.symbol) || 'None',
    cult: clean(row.cult) || 'None',
    material: clean(row.material) || 'Unknown',
    shape: clean(row.shape) || 'Unknown',
    period: clean(row.period),
    phase: clean(row.phase),
    area_section: clean(row['area-section']),
    excavation_idno: clean(row['excavation-idno']),
    horizontal_mm: clean(row['horizontal(mm)']),
    vertical_mm: clean(row['vertical(mm)']),
    thickness_mm: clean(row['thickness(mm)']),
    text: row.text,
  };
}

const rows = parseCsv(fs.readFileSync(METADATA, 'utf8'));
const occurrences = [];
const frames = [];

for (const row of rows) {
  const signs = tokens(row.text);
  if (!signs.length) continue;
  const base = metadataRecord(row);
  const object = base.object;

  for (let i = 0; i < signs.length; i += 1) {
    const sign = signs[i];
    const isAfter002390 = signs[i - 2] === '002' && signs[i - 1] === '390';
    if (!FOCUS_SIGNS.has(sign)) continue;
    const after = signs.slice(i + 1);
    const before = signs.slice(0, i);
    occurrences.push({
      ...base,
      sign,
      pos_1based: i + 1,
      prev2: signs[i - 2] ?? '',
      prev1: signs[i - 1] ?? '',
      next1: signs[i + 1] ?? '',
      next2: signs[i + 2] ?? '',
      is_terminal: boolText(after.length === 0),
      scope: isAfter002390 ? 'after_002390' : 'non_frame',
      prev_before_002: isAfter002390 ? signs[i - 3] ?? '<START>' : '',
      tail_after_sign: tailText(after),
      prefix_before_sign: tailText(before),
      context_cell: contextCell(row),
      source_status: sourceStatusFor(object),
    });
  }

  for (let i = 0; i < signs.length - 1; i += 1) {
    if (signs[i] !== '002' || signs[i + 1] !== '390') continue;
    const branch = signs[i + 2] ?? '<NONE>';
    const tail = signs.slice(i + 3);
    frames.push({
      ...base,
      frame_start_pos_1based: i + 1,
      prev_before_002: signs[i - 1] ?? '<START>',
      branch_after_390: branch,
      branch_is_focus_sign: boolText(FOCUS_SIGNS.has(branch)),
      tail_after_branch: branch === '<NONE>' ? '<NO_BRANCH>' : tailText(tail),
      terminal_after_branch: boolText(branch !== '<NONE>' && tail.length === 0),
      signless_formula: [
        signs[i - 1] ?? '<START>',
        '002-390',
        branch,
        branch === '<NONE>' ? '<NO_BRANCH>' : tailText(tail),
      ].join('|'),
      family_cell: `${contextCell(row)}|${signs[i - 1] ?? '<START>'}|${branch}|${branch === '<NONE>' ? '<NO_BRANCH>' : tailText(tail)}`,
      source_status: sourceStatusFor(object),
    });
  }
}

const signSummaryRows = [];
for (const sign of [...FOCUS_SIGNS].sort()) {
  const subset = occurrences.filter((row) => row.sign === sign);
  const afterFrame = subset.filter((row) => row.scope === 'after_002390');
  const nonFrame = subset.filter((row) => row.scope === 'non_frame');
  const terminal = (rs) => rs.filter((row) => row.is_terminal === 'True').length;
  const frameObjects = new Set(afterFrame.map((row) => row.object));
  const sites = new Set(subset.map((row) => row.site));
  const nonFrameTerminalExamples = nonFrame
    .filter((row) => row.is_terminal === 'True')
    .slice(0, 8)
    .map((row) => row.object)
    .join(';');
  const nonFrameContinuingExamples = nonFrame
    .filter((row) => row.is_terminal === 'False')
    .slice(0, 8)
    .map((row) => row.object)
    .join(';');
  signSummaryRows.push({
    sign,
    total_occurrences: subset.length,
    after_002390_occurrences: afterFrame.length,
    after_002390_terminal: terminal(afterFrame),
    after_002390_continuing: afterFrame.length - terminal(afterFrame),
    non_frame_occurrences: nonFrame.length,
    non_frame_terminal: terminal(nonFrame),
    non_frame_continuing: nonFrame.length - terminal(nonFrame),
    frame_objects: [...frameObjects].join(';'),
    sites: [...sites].sort().join(';'),
    non_frame_terminal_examples: nonFrameTerminalExamples,
    non_frame_continuing_examples: nonFrameContinuingExamples,
  });
}

const branchBuckets = new Map();
const branchObjects = new Map();
const branchSites = new Map();
for (const row of frames) {
  const branch = row.branch_after_390;
  if (!branchBuckets.has(branch)) {
    branchBuckets.set(branch, {
      branch_after_390: branch,
      frame_occurrences: 0,
      terminal_after_branch: 0,
      continuing_after_branch: 0,
      checkpoint_strict_visible: 0,
      route_or_dark_or_unbound: 0,
      metadata_only: 0,
    });
  }
  const bucket = branchBuckets.get(branch);
  bucket.frame_occurrences += 1;
  if (row.terminal_after_branch === 'True') bucket.terminal_after_branch += 1;
  else bucket.continuing_after_branch += 1;
  if (row.source_status === 'checkpoint_strict_source_visible') bucket.checkpoint_strict_visible += 1;
  else if (row.source_status === 'metadata_only_unbound') bucket.metadata_only += 1;
  else bucket.route_or_dark_or_unbound += 1;
  addSet(branchObjects, branch, row.object);
  addSet(branchSites, branch, row.site);
}

const frameBranchSummaryRows = [...branchBuckets.values()]
  .sort((a, b) => b.frame_occurrences - a.frame_occurrences || a.branch_after_390.localeCompare(b.branch_after_390))
  .map((row) => ({
    ...row,
    objects: [...(branchObjects.get(row.branch_after_390) ?? [])].join(';'),
    sites: [...(branchSites.get(row.branch_after_390) ?? [])].sort().join(';'),
  }));

const exceptions = [];
for (const row of frames) {
  if (row.branch_after_390 === '125' && row.terminal_after_branch === 'True') {
    exceptions.push({
      test: 'terminal_125_after_002390',
      object: row.object,
      sign: '125',
      scope: 'after_002390',
      result: 'hard_positive_model_stress',
      detail: row.text,
    });
  }
  if (row.branch_after_390 !== '125' && row.branch_after_390 !== '<NONE>' && row.terminal_after_branch === 'False') {
    exceptions.push({
      test: 'continuing_non125_after_002390',
      object: row.object,
      sign: row.branch_after_390,
      scope: 'after_002390',
      result: 'continuation_not_unique_to_125',
      detail: row.text,
    });
  }
}

for (const row of occurrences) {
  if (row.scope === 'non_frame' && row.sign === '125' && row.is_terminal === 'True') {
    exceptions.push({
      test: 'nonframe_terminal_125',
      object: row.object,
      sign: row.sign,
      scope: row.scope,
      result: '125_not_intrinsically_continuation_bearing',
      detail: row.text,
    });
  }
  if (row.scope === 'non_frame' && row.sign !== '125' && row.is_terminal === 'False') {
    exceptions.push({
      test: 'nonframe_continuing_095_692_705',
      object: row.object,
      sign: row.sign,
      scope: row.scope,
      result: 'closure_not_intrinsic_to_sign',
      detail: row.text,
    });
  }
}

const byTestLimit = new Map();
const limitedExceptions = [];
for (const row of exceptions) {
  const count = byTestLimit.get(row.test) ?? 0;
  if (count < 50) limitedExceptions.push(row);
  byTestLimit.set(row.test, count + 1);
}

const targetRows = new Map(rows.map((row) => [row.id, row]));
const h1993 = rows.find((row) => row.cisi === 'H-1993' && row.text.includes('002-390-095')) ?? {};
const m1825 = rows.find((row) => row.cisi === 'M-1825' && row.text.includes('002-390-705')) ?? {};
const d4237 = targetRows.get('4237.1') ?? {};
const d4348 = targetRows.get('4348.1') ?? {};

const sourceRecheckRows = [
  {
    gate: 'dholavira_4237_1_vs_bisht_page18_item10',
    target: '-:4237.1',
    local_metadata: `site=${clean(d4237.site)}; area=${clean(d4237['area-section'])}; period=${clean(d4237.period)}; dims=${clean(d4237['horizontal(mm)'])}x${clean(d4237['vertical(mm)'])}x${clean(d4237['thickness(mm)'])}; text=${d4237.text ?? ''}`,
    source_route: 'Bisht 2015 public OCR mirror, Dholavira individual seals and catalogue rows',
    result: 'route_splits: page18_item10_acc_2118_has_5_signs_and_is_a_visual_lookalike; ZA-12:2/8758/dimension_cluster_matches_metadata_but_is_not_bound_to_the_image',
    consequence: 'do_not_count_Dholavira_705_as_strict_source_bound; require AccNo_8758_or_ZA-12_2_image_caption_bridge',
  },
  {
    gate: 'm1825_bj25710_705_route',
    target: 'M-1825 / BJ25710',
    local_metadata: `site=${clean(m1825.site)}; type=${clean(m1825.type)}; excavation=${clean(m1825['excavation-idno'])}; dims=${clean(m1825['horizontal(mm)'])}x${clean(m1825['vertical(mm)'])}x${clean(m1825['thickness(mm)'])}; text=${m1825.text ?? ''}`,
    source_route: 'Internet Archive CISI Pakistan djvu txt/xml plus public web search and Bhaskar S1 catalogue',
    result: 'IA_Pakistan_OCR_XML_no_clean_M-1825_or_BJ25710_hit; visible plate map reaches about M-1658; Bhaskar S1 confirms F2 unicorn object only',
    consequence: 'do_not_count_M-1825_as_strict_705_source_bound; require object-to-image-to-sign-band bridge',
  },
  {
    gate: 'harappa_h1993_icit744',
    target: 'H-1993 / ICIT 744',
    local_metadata: `excavation=${clean(h1993['excavation-idno'])}; dims=${clean(h1993['horizontal(mm)'])}x${clean(h1993['vertical(mm)'])}x${clean(h1993['thickness(mm)'])}; text=${h1993.text ?? ''}`,
    source_route: 'Harappa ESM2 PDF exposes ICIT 744 (H-1993); local metadata points to H96-2769 Figure 17.07',
    result: 'supplement_transcription_level_only; exact web/local route checks did not locate artifact image; Figure 17.07 is not unique by itself because H-1803 also carries a Figure 17.07 hook',
    consequence: 'usable as route pressure only; do_not_count_H-1993_as_strict_095_source_image_evidence',
  },
  {
    gate: 'dholavira_4348_guard',
    target: 'ICIT 4348 / local 4348.1',
    local_metadata: `site=${clean(d4348.site)}; type=${clean(d4348.type)}; text=${d4348.text ?? ''}`,
    source_route: 'Harappa ESM2 names ICIT 4348 (Dholavira); local metadata row is separate from 4237.1',
    result: 'separate_002_861_390_Dholavira_clue_not_002_390_705',
    consequence: 'do_not_pollute_4237_1_source_binding_with_4348',
  },
  {
    gate: 'h773_non125_continuation_exception',
    target: 'H-773',
    local_metadata: 'id=1665.1; excavation=12377351; site=Harappa; type=TAB:B; material=Faience; text=+740-798-803-002-390-530-741+',
    source_route: 'Archive.org CISI Pakistan page n358 image acquired; H-773 A token overlay stored under tmp/source_route_recheck_20260531',
    result: 'source_panel_acquired_for_H-773_A/B; 002-390-530-741 is boxed-window-compatible under R/L policy but exact token identity remains catalog-mediated',
    consequence: 'upgrade_from_metadata_only_to_panel_bound_pressure; do_not_count_as_strict_anti125_exception',
  },
  {
    gate: '3335_1_non125_continuation_exception',
    target: '-:3335.1',
    local_metadata: 'site=Unknown; object=-; excavation=-; type=SEAL:S; dims=29x29x0; text=+740-205-032-002-390-590-032+',
    source_route: 'local metadata plus exact-string web search',
    result: 'no stable CISI object ID or public source route found',
    consequence: 'remains_object_id_blocked; do_not_use_as_source_normalized_exception',
  },
];

const occurrenceFields = [
  'id', 'object', 'site', 'type', 'symbol', 'cult', 'material', 'shape', 'period', 'phase',
  'area_section', 'excavation_idno', 'horizontal_mm', 'vertical_mm', 'thickness_mm',
  'sign', 'pos_1based', 'prev2', 'prev1', 'next1', 'next2', 'is_terminal', 'scope',
  'prev_before_002', 'tail_after_sign', 'prefix_before_sign', 'context_cell', 'source_status', 'text',
];

const frameFields = [
  'id', 'object', 'site', 'type', 'symbol', 'cult', 'material', 'shape', 'period', 'phase',
  'area_section', 'excavation_idno', 'horizontal_mm', 'vertical_mm', 'thickness_mm',
  'frame_start_pos_1based', 'prev_before_002', 'branch_after_390', 'branch_is_focus_sign',
  'tail_after_branch', 'terminal_after_branch', 'signless_formula', 'family_cell',
  'source_status', 'text',
];

writeCsv(OUT_OCCURRENCES, occurrences, occurrenceFields);
writeCsv(OUT_FRAMES, frames, frameFields);
writeCsv(OUT_SIGN_SUMMARY, signSummaryRows, [
  'sign', 'total_occurrences', 'after_002390_occurrences', 'after_002390_terminal',
  'after_002390_continuing', 'non_frame_occurrences', 'non_frame_terminal',
  'non_frame_continuing', 'frame_objects', 'sites', 'non_frame_terminal_examples',
  'non_frame_continuing_examples',
]);
writeCsv(OUT_FRAME_BRANCH_SUMMARY, frameBranchSummaryRows, [
  'branch_after_390', 'frame_occurrences', 'terminal_after_branch', 'continuing_after_branch',
  'checkpoint_strict_visible', 'route_or_dark_or_unbound', 'metadata_only', 'objects', 'sites',
]);
writeCsv(OUT_EXCEPTIONS, limitedExceptions, ['test', 'object', 'sign', 'scope', 'result', 'detail']);
writeCsv(OUT_SOURCE_RECHECK, sourceRecheckRows, [
  'gate', 'target', 'local_metadata', 'source_route', 'result', 'consequence',
]);

const testCounts = Object.fromEntries([...byTestLimit.entries()].sort((a, b) => a[0].localeCompare(b[0])));
const branchCounts = Object.fromEntries(frameBranchSummaryRows.map((row) => [row.branch_after_390, row.frame_occurrences]));
const focusSignSummary = Object.fromEntries(signSummaryRows.map((row) => [row.sign, row]));

const summary = {
  run_date: RUN_DATE,
  campaign: '032-002-861 / 002-390-X',
  input_metadata: path.relative(ROOT, METADATA).replaceAll('\\', '/'),
  metadata_rows: rows.length,
  focus_signs: [...FOCUS_SIGNS].sort(),
  frame_002390_occurrences: frames.length,
  frame_branch_counts: branchCounts,
  focus_sign_summary: focusSignSummary,
  exception_counts_total: testCounts,
  exception_rows_written_with_cap_per_test: limitedExceptions.length,
  source_recheck_decisions: sourceRecheckRows,
  interpretation_guardrails: [
    'No phonetic, semantic, language, function, or translation values accepted.',
    'Dholavira 4237.1 / 705 remains split between a page-18 lookalike and an unbound 8758 metadata cluster.',
    'M-1825 / 705 remains secondary-icon-only in this pass; IA Pakistan OCR/XML did not bind M-1825 or BJ25710.',
    'H-1993 has been route-triaged to supplement-only pressure; Figure 17.07 is not a unique image bridge.',
    'H-773 is panel-bound and boxed-window-compatible, not strict token evidence.',
    'Branch ecology supports testing a constructional slot, but does not prove linguistic value.',
  ],
  outputs: {
    occurrences: path.relative(ROOT, OUT_OCCURRENCES).replaceAll('\\', '/'),
    frames: path.relative(ROOT, OUT_FRAMES).replaceAll('\\', '/'),
    sign_summary: path.relative(ROOT, OUT_SIGN_SUMMARY).replaceAll('\\', '/'),
    frame_branch_summary: path.relative(ROOT, OUT_FRAME_BRANCH_SUMMARY).replaceAll('\\', '/'),
    exceptions: path.relative(ROOT, OUT_EXCEPTIONS).replaceAll('\\', '/'),
    source_recheck: path.relative(ROOT, OUT_SOURCE_RECHECK).replaceAll('\\', '/'),
    summary: path.relative(ROOT, OUT_SUMMARY).replaceAll('\\', '/'),
  },
};

fs.writeFileSync(OUT_SUMMARY, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify({
  run_date: RUN_DATE,
  metadata_rows: rows.length,
  frame_002390_occurrences: frames.length,
  focus_sign_summary: focusSignSummary,
  exception_counts_total: testCounts,
  outputs: summary.outputs,
}, null, 2));
