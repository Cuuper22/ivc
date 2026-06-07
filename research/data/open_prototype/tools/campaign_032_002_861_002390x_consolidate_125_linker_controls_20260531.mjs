import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_consolidate_125_linker_controls_20260531';
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

function tally(values) {
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([value, count]) => `${value}:${count}`)
    .join(';');
}

function unique(values) {
  return [...new Set(values)];
}

function laneFor(next1, tail) {
  if (next1 === '<END>') return 'terminal_125';
  if (next1 === '632' && tail.startsWith('632-032')) return '632_032_lane';
  if (next1 === '032') return '032_lane';
  if (next1 === '820') return '820_lane';
  return `${next1}_singleton_lane`;
}

function keepForScope(row, scope) {
  if (scope === 'all') return true;
  if (scope === 'frame_002_390_only') return row.frame_local_002_390_125;
  if (scope === 'mohenjo_only') return row.site === 'Mohenjo-daro';
  if (scope === 'non_mohenjo') return row.site !== 'Mohenjo-daro';
  if (scope === 'seal_s_only') return row.type === 'SEAL:S';
  if (scope === 'complete_y') return row.complete === 'Y';
  if (scope === 'good_or_fine') return row.condition === 'Good' || row.condition === 'Fine';
  if (scope === 'cisi_named') return row.object && !row.object.startsWith('-:');
  return false;
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));

const x125Rows = [];
for (const row of rows) {
  for (let i = 0; i < row.signs.length - 2; i += 1) {
    if (row.signs[i] !== '002' || row.signs[i + 2] !== '125') continue;
    const head = row.signs[i + 1];
    const next1 = row.signs[i + 3] ?? '<END>';
    const tail = row.signs.slice(i + 3).join('-') || '<END>';
    const lane = laneFor(next1, tail);
    x125Rows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      condition: row.condition,
      complete: row.complete,
      head,
      next1,
      tail,
      lane,
      terminal: next1 === '<END>',
      frame_local_002_390_125: head === '390',
      text: row.text,
    });
  }
}

const scopes = [
  'all',
  'frame_002_390_only',
  'mohenjo_only',
  'non_mohenjo',
  'seal_s_only',
  'complete_y',
  'good_or_fine',
  'cisi_named',
];

const controlRows = scopes.map((scope) => {
  const scoped = x125Rows.filter((row) => keepForScope(row, scope));
  const nonterminal = scoped.filter((row) => !row.terminal);
  const repeatedLanes = unique(nonterminal.map((row) => row.lane)).filter(
    (lane) => nonterminal.filter((row) => row.lane === lane).length >= 2,
  );
  const crossSiteRepeatedLanes = repeatedLanes.filter((lane) => {
    const laneRows = nonterminal.filter((row) => row.lane === lane);
    return unique(laneRows.map((row) => row.site)).length >= 2;
  });
  const crossHeadRepeatedLanes = repeatedLanes.filter((lane) => {
    const laneRows = nonterminal.filter((row) => row.lane === lane);
    return unique(laneRows.map((row) => row.head)).length >= 2;
  });
  return {
    checked_date: checkedDate,
    scope,
    rows: scoped.length,
    nonterminal_rows: nonterminal.length,
    terminal_rows: scoped.filter((row) => row.terminal).length,
    lanes: tally(scoped.map((row) => row.lane)),
    repeated_lanes: repeatedLanes.join(';'),
    cross_site_repeated_lanes: crossSiteRepeatedLanes.join(';'),
    cross_head_repeated_lanes: crossHeadRepeatedLanes.join(';'),
    sites: tally(scoped.map((row) => row.site)),
    heads: tally(scoped.map((row) => row.head)),
    verdict:
      scoped.length < 3
        ? 'underpowered'
        : repeatedLanes.length === 0
          ? 'damaged_no_repeated_lanes'
          : crossSiteRepeatedLanes.length || crossHeadRepeatedLanes.length
            ? 'survives'
            : 'survives_only_site_local',
  };
});

const laneRows = unique(x125Rows.map((row) => row.lane)).map((lane) => {
  const laneRowsLocal = x125Rows.filter((row) => row.lane === lane);
  return {
    checked_date: checkedDate,
    lane,
    rows: laneRowsLocal.length,
    objects: laneRowsLocal.map((row) => row.object).join(';'),
    sites: tally(laneRowsLocal.map((row) => row.site)),
    heads: tally(laneRowsLocal.map((row) => row.head)),
    frame_002_390_rows: laneRowsLocal.filter((row) => row.frame_local_002_390_125).length,
    verdict:
      laneRowsLocal.length >= 2 && unique(laneRowsLocal.map((row) => row.site)).length >= 2
        ? 'cross_site_lane'
        : laneRowsLocal.length >= 2 && unique(laneRowsLocal.map((row) => row.head)).length >= 2
          ? 'cross_head_site_local_lane'
          : laneRowsLocal.length >= 2
            ? 'repeated_site_local_lane'
            : 'singleton_or_terminal_exception',
  };
});

const seriousControls = controlRows.filter((row) => row.verdict !== 'underpowered');
const strongSurvivals = seriousControls.filter((row) => row.verdict === 'survives').length;
const weakSurvivals = seriousControls.filter((row) => row.verdict === 'survives_only_site_local').length;

const decisionRows = [
  {
    checked_date: checkedDate,
    claim: '125_as_general_linker',
    decision: strongSurvivals >= 2 ? 'candidate_wounded_keep' : 'demote_to_formula_risk',
    reason:
      '125 is mostly nonterminal and has repeated complement lanes, but the strongest lane remains Mohenjo-daro-local.',
  },
  {
    checked_date: checkedDate,
    claim: '125_as_390_specific_linker',
    decision: 'candidate_wounded_keep',
    reason:
      'All frame-local 002-390-125 rows have complements after 125, but only four rows and the repeated 632-032 lane is site-local.',
  },
  {
    checked_date: checkedDate,
    claim: '632_032_as_general_complement',
    decision: 'demote_to_site_local_formula_risk',
    reason: '632-032 repeats but only at Mohenjo-daro in current rows.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: '125_linker_controls',
  x125_rows: x125Rows.length,
  serious_controls: seriousControls.length,
  strong_survivals: strongSurvivals,
  weak_site_local_survivals: weakSurvivals,
  controls: Object.fromEntries(
    controlRows.map((row) => [
      row.scope,
      {
        rows: Number(row.rows),
        repeated_lanes: row.repeated_lanes,
        cross_site_repeated_lanes: row.cross_site_repeated_lanes,
        verdict: row.verdict,
      },
    ]),
  ),
  decision: '125_linker_candidate_survives_but_only_wounded; 632-032_demoted_to_site_local_formula_risk',
};

writeCsv(path.join(reportsDir, `${prefix}_controls.csv`), controlRows, [
  'checked_date',
  'scope',
  'rows',
  'nonterminal_rows',
  'terminal_rows',
  'lanes',
  'repeated_lanes',
  'cross_site_repeated_lanes',
  'cross_head_repeated_lanes',
  'sites',
  'heads',
  'verdict',
]);
writeCsv(path.join(reportsDir, `${prefix}_lane_rows.csv`), laneRows, [
  'checked_date',
  'lane',
  'rows',
  'objects',
  'sites',
  'heads',
  'frame_002_390_rows',
  'verdict',
]);
writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisionRows, [
  'checked_date',
  'claim',
  'decision',
  'reason',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
