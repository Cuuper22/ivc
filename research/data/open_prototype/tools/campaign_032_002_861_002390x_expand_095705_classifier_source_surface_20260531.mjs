import fs from 'node:fs';
import path from 'node:path';

// This script surfaces the source evidence behind the claim that signs 095
// and 705 are overt terminal classifiers in the 002-HEAD-X frame. It scans
// lipi/metadata_filtered.csv for every 002-HEAD-095 and 002-HEAD-705
// occurrence, then attaches a hand-recorded source assessment per object:
// H-1993 has a public Harappa supplementary-PDF transcription (route support,
// no artifact image), the Dholavira row 4237.1 has an unbound visual
// candidate, and everything else is structural only. It also logs the public
// search queries that were tried and what each did or did not turn up. The
// resulting bets keep both classifiers at "wild shot": 095 strengthened by
// the public transcription but image-unbound, 705 structurally strong but
// source-fragile. Writes classifier rows, per-classifier status, the search
// log, and the bets as CSVs plus a summary JSON to
// data/open_prototype/reports.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_095705_classifier_source_surface_20260531';
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

function tokens(text) {
  return text.match(/\d{3}/g) ?? [];
}

function sourceSurface(object) {
  if (object === 'H-1993') {
    return {
      public_source:
        'https://www.harappa.com/sites/default/files/pdf/43539_2023_102_MOESM2_ESM.pdf',
      source_status: 'public_supplement_transcription_not_artifact_image',
      classifier_effect: 'supports_presence_of_095_route_but_not_image_bound',
    };
  }
  if (object === '-:4237.1') {
    return {
      public_source: '',
      source_status: 'dholavira_visual_candidate_unbound_to_metadata_row',
      classifier_effect: '705_route_structurally_hot_but_source_fragile',
    };
  }
  return {
    public_source: '',
    source_status: 'no_public_exact_bridge_in_this_pass',
    classifier_effect: 'structural_only',
  };
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));

const classifierRows = [];
for (const row of rows) {
  for (let i = 0; i < row.signs.length - 2; i += 1) {
    if (row.signs[i] !== '002') continue;
    const head = row.signs[i + 1];
    const x = row.signs[i + 2];
    if (x !== '095' && x !== '705') continue;
    const source = sourceSurface(row.object);
    classifierRows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      symbol: row.symbol,
      condition: row.condition,
      complete: row.complete,
      head,
      classifier: x,
      terminal: i + 2 === row.signs.length - 1,
      next1: row.signs[i + 3] ?? '<END>',
      text: row.text,
      public_source: source.public_source,
      source_status: source.source_status,
      classifier_effect: source.classifier_effect,
    });
  }
}

const statusRows = ['095', '705'].map((classifier) => {
  const members = classifierRows.filter((row) => row.classifier === classifier);
  return {
    checked_date: checkedDate,
    classifier,
    occurrences: members.length,
    terminal: members.filter((row) => row.terminal).length,
    sites: [...new Set(members.map((row) => row.site))].join(';'),
    objects: members.map((row) => row.object).join(';'),
    source_surface: members.map((row) => `${row.object}:${row.source_status}`).join(';'),
    decision:
      classifier === '095'
        ? 'classifier_wild_shot_strengthened_by_public_transcription_but_image_unbound'
        : 'classifier_wild_shot_structurally_strong_but_source_fragile',
  };
});

const searchRows = [
  {
    checked_date: checkedDate,
    query: '"H-1993" "390-095"',
    result: 'no exact numeric sign bridge in search result',
    parse_effect: 'no image/source promotion',
  },
  {
    checked_date: checkedDate,
    query: '"ICIT 744" "H-1993"',
    result: 'Harappa supplementary PDF exposes ICIT 744 (H-1993) transcription line',
    parse_effect: '095 route gets public transcription support only',
  },
  {
    checked_date: checkedDate,
    query: '"M-1825" "390-705"',
    result: 'no useful public bridge found',
    parse_effect: '705 remains structurally strong but source-fragile',
  },
  {
    checked_date: checkedDate,
    query: '"+151-032-388-002-390-705"',
    result: 'no exact public sign-string bridge found in this pass',
    parse_effect: 'Dholavira 705 route not source-promoted',
  },
];

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_095_PUBLIC_TRANSCRIPTION_CLASSIFIER',
    tier: 'wild shot',
    claim:
      '095 is an overt terminal classifier in 002-H-X, with H-1993 providing public transcription-level support.',
    risky_prediction:
      'Source-bound H-1993 should preserve terminal 095 and not reveal damage/side split.',
    kill_condition:
      'Artifact image/source layout breaks the terminal 095 reading or shows copying artifact.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_705_SOURCE_FRAGILE_CLASSIFIER',
    tier: 'wild shot',
    claim:
      '705 is an overt terminal classifier, but current support is structural until M-1825/Dholavira source binding improves.',
    risky_prediction:
      'Source-visible 705 terminal rows should stay terminal; nonterminal 705-125 should parse as classifier-to-linker exception.',
    kill_condition:
      '705 rows collapse to weak source windows or copied visual formula.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: '095705_classifier_source_surface',
  classifiers: Object.fromEntries(
    statusRows.map((row) => [
      row.classifier,
      {
        occurrences: Number(row.occurrences),
        terminal: Number(row.terminal),
        sites: row.sites,
        decision: row.decision,
      },
    ]),
  ),
  provisional_read:
    '095/705 classifier bet survives structurally; 095 has public transcription support, 705 remains source-fragile.',
};

writeCsv(path.join(reportsDir, `${prefix}_classifier_rows.csv`), classifierRows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'symbol',
  'condition',
  'complete',
  'head',
  'classifier',
  'terminal',
  'next1',
  'text',
  'public_source',
  'source_status',
  'classifier_effect',
]);
writeCsv(path.join(reportsDir, `${prefix}_status_rows.csv`), statusRows, [
  'checked_date',
  'classifier',
  'occurrences',
  'terminal',
  'sites',
  'objects',
  'source_surface',
  'decision',
]);
writeCsv(path.join(reportsDir, `${prefix}_public_searches.csv`), searchRows, [
  'checked_date',
  'query',
  'result',
  'parse_effect',
]);
writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), betRows, [
  'checked_date',
  'bet_id',
  'tier',
  'claim',
  'risky_prediction',
  'kill_condition',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
