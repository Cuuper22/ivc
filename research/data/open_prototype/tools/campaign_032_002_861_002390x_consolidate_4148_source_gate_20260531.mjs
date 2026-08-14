// Records the source gate on row 4148.1, the cleanest potential kill switch
// against the X=000 terminal candidate. Its text +740-690-435-255-002-267-000-033+
// would show meaningful payload (033) after 000 — but only if a source image
// confirms the sequence is continuous on one side of the object. This script
// pulls the target row's full metadata from the local Lipi table (no CISI id,
// no excavation number, no dimensions), logs the exact public web searches that
// were tried and their negative results, and writes an adjudication table
// spelling out what each possible source outcome would do to X=000 (demote,
// keep with warning, remove the kill switch, or leave unpromoted). Writes
// target, searches, and adjudication CSVs plus a summary JSON to
// data/open_prototype/reports/. Current state: no source found, so X=000 stays
// a candidate with a robustness warning, neither promoted nor killed.

import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_consolidate_4148_source_gate_20260531';
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

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
}));
const target = rows.find((row) => row.id === '4148.1');
if (!target) throw new Error('Missing 4148.1 in metadata_filtered.csv');

const targetRows = [
  {
    checked_date: checkedDate,
    object: target.object,
    row_id: target.id,
    site: target.site,
    region: target.region,
    type: target.type,
    symbol: target.symbol,
    condition: target.condition,
    complete: target.complete,
    dir: target['dir.'],
    material: target.material,
    shape: target.shape,
    excavation_idno: target['excavation-idno'],
    area_section: target['area-section'],
    block_house: target['block-house'],
    room_grid: target['room-grid'],
    horizontal_mm: target['horizontal(mm)'],
    vertical_mm: target['vertical(mm)'],
    thickness_mm: target['thickness(mm)'],
    text: target.text,
    source_strength: 'metadata_only_no_cisi_no_excavation_no_dimensions',
  },
];

const webSearchRows = [
  {
    checked_date: checkedDate,
    query: '"+740-690-435-255-002-267-000-033"',
    result: 'no useful public object/plate bridge found',
    parse_effect: 'no promotion_or_demote; source remains missing',
  },
  {
    checked_date: checkedDate,
    query: '"740-690-435-255-002-267-000-033"',
    result: 'no useful public object/plate bridge found',
    parse_effect: 'no promotion_or_demote; source remains missing',
  },
  {
    checked_date: checkedDate,
    query: '"4148.1" Rakhigarhi seal',
    result: 'false-positive numeric results; no IVC source binding',
    parse_effect: 'no promotion_or_demote; source remains missing',
  },
  {
    checked_date: checkedDate,
    query: '"Rakhigarhi" "267" "000" "033" "Indus"',
    result: 'Rakhigarhi background pages only; no target row/source binding',
    parse_effect: 'no promotion_or_demote; source remains missing',
  },
];

const adjudicationRows = [
  {
    checked_date: checkedDate,
    scenario: 'source_confirms_continuous_002_267_000_033',
    effect_on_x000: 'demote_from_core_to_register_or_formula_limited_candidate',
    reason: '033 would be a meaningful nonzero payload after X=000 in the cleanest killer row.',
  },
  {
    checked_date: checkedDate,
    scenario: 'source_shows_033_on_separate_side_or_boundary',
    effect_on_x000: 'keep_candidate_with_warning',
    reason: '000 can still close the 002-267 frame if 033 is not governed payload.',
  },
  {
    checked_date: checkedDate,
    scenario: 'source_rejects_4148_1_text_or_object',
    effect_on_x000: 'remove_cleanest_kill_switch_keep_candidate',
    reason: 'The damaging row would be unusable; robustness warnings remain from non-seal/site-collapse controls.',
  },
  {
    checked_date: checkedDate,
    scenario: 'no_source_found',
    effect_on_x000: 'candidate_with_robustness_warning_not_promoted',
    reason: 'Missing source cannot adjudicate the kill switch; local singleton pressure remains.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: '4148_source_gate',
  target: '4148.1',
  source_strength: targetRows[0].source_strength,
  public_exact_search: 'no_useful_public_bridge_found_2026-05-31',
  x000_status_after_gate: 'candidate_with_robustness_warning_not_promoted',
  decisive_outcome_needed:
    'source image/plate/data row deciding whether 033 is governed payload after 002-267-000 or a separate boundary/side/transcription issue',
};

writeCsv(path.join(reportsDir, `${prefix}_target.csv`), targetRows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'region',
  'type',
  'symbol',
  'condition',
  'complete',
  'dir',
  'material',
  'shape',
  'excavation_idno',
  'area_section',
  'block_house',
  'room_grid',
  'horizontal_mm',
  'vertical_mm',
  'thickness_mm',
  'text',
  'source_strength',
]);
writeCsv(path.join(reportsDir, `${prefix}_public_searches.csv`), webSearchRows, [
  'checked_date',
  'query',
  'result',
  'parse_effect',
]);
writeCsv(path.join(reportsDir, `${prefix}_adjudication.csv`), adjudicationRows, [
  'checked_date',
  'scenario',
  'effect_on_x000',
  'reason',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
