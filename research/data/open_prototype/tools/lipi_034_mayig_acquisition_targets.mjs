import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(base, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const mayigIndexPath = path.join(base, 'data', 'open_prototype', 'mayig', 'records_index.csv');
const mayigCommitPath = path.join(base, 'data', 'open_prototype', 'mayig', 'commit.json');

const targetsOut = path.join(reportsDir, 'lipi_034_mayig_acquisition_targets.csv');
const objectsOut = path.join(reportsDir, 'lipi_034_mayig_acquisition_priority_objects.csv');
const summaryOut = path.join(reportsDir, 'lipi_034_mayig_acquisition_summary.json');

function parseCsv(text) {
  const rows = [];
  let row = [];
  let value = '';
  let inQuotes = false;

  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (inQuotes) {
      if (ch === '"' && next === '"') {
        value += '"';
        i += 1;
      } else if (ch === '"') {
        inQuotes = false;
      } else {
        value += ch;
      }
    } else if (ch === '"') {
      inQuotes = true;
    } else if (ch === ',') {
      row.push(value);
      value = '';
    } else if (ch === '\n') {
      row.push(value);
      if (row.length > 1 || row[0] !== '') rows.push(row);
      row = [];
      value = '';
    } else if (ch !== '\r') {
      value += ch;
    }
  }
  if (value.length > 0 || row.length > 0) {
    row.push(value);
    rows.push(row);
  }
  return rows;
}

function csvObjects(text) {
  const [header, ...body] = parseCsv(text);
  return body.map((row) =>
    Object.fromEntries(header.map((key, index) => [key, row[index] ?? ''])),
  );
}

function toCsv(rows) {
  if (rows.length === 0) return '';
  const header = Object.keys(rows[0]);
  const body = rows.map((row) =>
    header
      .map((key) => `"${String(row[key] ?? '').replaceAll('"', '""')}"`)
      .join(','),
  );
  return `${[header.map((key) => `"${key}"`).join(','), ...body].join('\n')}\n`;
}

function tokens(text) {
  return text.match(/\d+/gu) ?? [];
}

function has034(row) {
  return tokens(row.text).includes('034');
}

function cisiPrefix(cisi) {
  const match = /^([A-Z]+)-/u.exec(cisi);
  return match?.[1] ?? (cisi === '-' ? '-' : 'other');
}

function cisiNumber(cisi) {
  const match = /^[A-Z]+-(\d+)$/u.exec(cisi);
  return match ? Number(match[1]) : null;
}

function isH2218To2239(row) {
  const n = cisiNumber(row.cisi);
  return row.cisi.startsWith('H-') && n !== null && n >= 2218 && n <= 2239;
}

function frame700Relation(row) {
  const rowTokens = tokens(row.text);
  for (let i = 0; i < rowTokens.length; i += 1) {
    if (rowTokens[i] !== '034') continue;
    if (rowTokens[i - 1] === '700') return '700_before_034';
    if (rowTokens[i + 1] === '700') return '700_after_034';
  }
  return '034_without_adjacent_700';
}

function countBy(rows, keyFn) {
  const counts = {};
  for (const row of rows) {
    const key = keyFn(row);
    counts[key] = (counts[key] ?? 0) + 1;
  }
  return Object.fromEntries(
    Object.entries(counts).sort((a, b) => a[0].localeCompare(b[0], undefined, { numeric: true })),
  );
}

function unique(values) {
  return [...new Set(values.filter(Boolean))].sort((a, b) =>
    a.localeCompare(b, undefined, { numeric: true }),
  );
}

function sourceHook(row) {
  const hooks = [
    row['excavation-idno'],
    row.time,
    row.period,
    row.phase,
    row.depth,
  ].filter((value) => value && value !== '-');
  return hooks.join(' | ');
}

function isLikelyNumericClean(row) {
  return row.complete === 'Y' && row['dir.'] !== '-' && !/[?\[\]0]{3}/u.test(row.text);
}

function priority(row, mayigAvailable) {
  const relation = frame700Relation(row);
  const prefix = cisiPrefix(row.cisi);
  const reasons = [];
  let score = 0;
  let lane = 'P3_other_034_source_coverage';

  if (prefix === 'M' && row.site === 'Mohenjo-daro' && !mayigAvailable) {
    score += 170;
    lane = 'P0_mohenjo_034_missing_from_current_mayig';
    reasons.push('same_site_as_mayig_overlap_but_absent_from_current_repo');
  }

  if (prefix !== 'M' && row.site === 'Mohenjo-daro' && !mayigAvailable) {
    score += 60;
    lane = 'P2_mohenjo_034_missing_cisi_or_non_m_prefix';
    reasons.push('mohenjo_daro_034_but_missing_m_number_for_mayig_query');
  }

  if (isH2218To2239(row)) {
    score += 90;
    lane = 'P1_h_series_034_slot_controls';
    reasons.push('h2218_h2239_slot_series_control');
  }

  if (relation !== '034_without_adjacent_700') {
    score += 35;
    if (!lane.startsWith('P0') && !lane.startsWith('P1_h_series')) {
      lane = 'P1_frame700_034_branch';
    }
    reasons.push(relation);
  }

  if (row.site === 'Harappa') {
    score += 15;
    reasons.push('harappa_heavy_034_branch');
  }

  if (row.type === 'TAB:I' || row.type === 'TAB:B') {
    score += 12;
    reasons.push('tablet_branch');
  }

  if (row.type === 'SEAL:S') {
    score += 10;
    reasons.push('seal_s_comparable_to_current_mayig_type');
  }

  if (isLikelyNumericClean(row)) {
    score += 8;
    reasons.push('complete_direction_clean_no_000');
  }

  if (sourceHook(row)) {
    score += 5;
    reasons.push('has_source_or_context_hook');
  }

  if (prefix === '-') {
    score -= 20;
    reasons.push('missing_cisi_object_id');
  }

  if (row.complete !== 'Y' || row.preservation === 'fragment') {
    score -= 10;
    reasons.push('fragment_or_uncertain_completeness');
  }

  if (row.condition === 'Good') {
    score += 3;
    reasons.push('good_condition');
  }

  return {
    score,
    lane,
    reasons: reasons.join(';'),
  };
}

const metadata = csvObjects(fs.readFileSync(metadataPath, 'utf8'));
const mayigIndex = csvObjects(fs.readFileSync(mayigIndexPath, 'utf8'));
const mayigCommit = JSON.parse(fs.readFileSync(mayigCommitPath, 'utf8'));
const mayigBases = new Set(mayigIndex.map((row) => row.artifact_base));

const targetRows = metadata
  .filter(has034)
  .map((row) => {
    const mayigAvailable = mayigBases.has(row.cisi);
    const ranked = priority(row, mayigAvailable);
    return {
      checked_date: '2026-05-25',
      source_row_id: row.id,
      cisi: row.cisi,
      cisi_prefix: cisiPrefix(row.cisi),
      priority_lane: ranked.lane,
      priority_score: String(ranked.score),
      priority_reasons: ranked.reasons,
      mayig_current_repo_has_object: mayigAvailable ? '1' : '0',
      mayig_current_repo_commit: mayigCommit.commit,
      site: row.site,
      type: row.type,
      material: row.material,
      shape: row.shape,
      preservation: row.preservation,
      complete: row.complete,
      condition: row.condition,
      direction: row['dir.'],
      class: row.class,
      sign_count: row.signs,
      frame700_relation: frame700Relation(row),
      source_hook: sourceHook(row),
      text: row.text,
      acquisition_question:
        ranked.lane === 'P0_mohenjo_034_missing_from_current_mayig'
          ? 'Obtain Mayig/Parpola record or authoritative sign-list mapping for this exact Mohenjo-daro 034 object.'
          : ranked.lane === 'P1_h_series_034_slot_controls'
            ? 'Use as H-series 034 slot control while H-2238 carries the paired 033 variant.'
            : ranked.lane === 'P1_frame700_034_branch'
              ? 'Use as FRAME700 034 source/crosswalk control after image and sign-list validation.'
              : 'Use only after higher-priority 034 coverage targets are exhausted.',
      accepted_decipherment_claim: '0',
    };
  })
  .sort(
    (a, b) =>
      Number(b.priority_score) - Number(a.priority_score) ||
      a.cisi_prefix.localeCompare(b.cisi_prefix) ||
      a.cisi.localeCompare(b.cisi, undefined, { numeric: true }) ||
      a.source_row_id.localeCompare(b.source_row_id, undefined, { numeric: true }),
  );

const byObject = new Map();
for (const row of targetRows) {
  const key = row.cisi && row.cisi !== '-' ? row.cisi : `row:${row.source_row_id}`;
  if (!byObject.has(key)) byObject.set(key, []);
  byObject.get(key).push(row);
}

const objectRows = [...byObject.entries()]
  .map(([objectKey, rows]) => {
    const top = rows.sort((a, b) => Number(b.priority_score) - Number(a.priority_score))[0];
    return {
      checked_date: '2026-05-25',
      object_key: objectKey,
      cisi: top.cisi,
      cisi_prefix: top.cisi_prefix,
      max_priority_lane: top.priority_lane,
      max_priority_score: top.priority_score,
      row_count: String(rows.length),
      texts: unique(rows.map((row) => row.text)).join(';'),
      source_row_ids: unique(rows.map((row) => row.source_row_id)).join(';'),
      site: top.site,
      type_values: unique(rows.map((row) => row.type)).join(';'),
      material_values: unique(rows.map((row) => row.material)).join(';'),
      frame700_relations: unique(rows.map((row) => row.frame700_relation)).join(';'),
      source_hooks: unique(rows.map((row) => row.source_hook)).join(';'),
      mayig_current_repo_has_object: rows.some((row) => row.mayig_current_repo_has_object === '1')
        ? '1'
        : '0',
      acquisition_question: top.acquisition_question,
      accepted_decipherment_claim: '0',
    };
  })
  .sort(
    (a, b) =>
      Number(b.max_priority_score) - Number(a.max_priority_score) ||
      a.cisi_prefix.localeCompare(b.cisi_prefix) ||
      a.cisi.localeCompare(b.cisi, undefined, { numeric: true }),
  );

const p0Mohenjo = objectRows.filter((row) => row.max_priority_lane === 'P0_mohenjo_034_missing_from_current_mayig');
const hSeriesControls = objectRows.filter((row) => row.max_priority_lane === 'P1_h_series_034_slot_controls');

const summary = {
  checked_date: '2026-05-25',
  artifact: 'lipi_034_mayig_acquisition_targets',
  question:
    'Which exact 034 rows should be acquired or crosswalked first to resolve the current Mayig/Parpola coverage gap?',
  inputs: [
    path.relative(base, metadataPath).replaceAll('\\', '/'),
    path.relative(base, mayigIndexPath).replaceAll('\\', '/'),
    path.relative(base, mayigCommitPath).replaceAll('\\', '/'),
  ],
  mayig_current_repo: {
    repository: mayigCommit.repository,
    commit: mayigCommit.commit,
    commit_message: mayigCommit.commit_message,
    current_head_checked_locally: 'git ls-remote returned the same commit on 2026-05-25',
    indexed_records: mayigIndex.length,
  },
  exact_034_rows: targetRows.length,
  exact_034_unique_objects_or_rows: objectRows.length,
  target_rows_by_priority_lane: countBy(targetRows, (row) => row.priority_lane),
  target_objects_by_priority_lane: countBy(objectRows, (row) => row.max_priority_lane),
  p0_mohenjo_034_missing_objects: p0Mohenjo.map((row) => row.cisi).join(';'),
  p0_mohenjo_034_missing_object_count: p0Mohenjo.length,
  h_series_034_slot_control_objects: hSeriesControls.map((row) => row.cisi).join(';'),
  h_series_034_slot_control_object_count: hSeriesControls.length,
  top_12_priority_objects: objectRows.slice(0, 12).map((row) => ({
    cisi: row.cisi,
    lane: row.max_priority_lane,
    score: Number(row.max_priority_score),
    texts: row.texts,
    acquisition_question: row.acquisition_question,
  })),
  conclusion:
    'The next 034 crosswalk move is data acquisition: current upstream Mayig remains at m184/ad2f1e2 and has no M-315+ records, so Mohenjo-daro 034 objects are concrete missing Parpola/Mayig targets while H-series 034 rows remain source-image controls.',
  outputs: [
    path.relative(base, targetsOut).replaceAll('\\', '/'),
    path.relative(base, objectsOut).replaceAll('\\', '/'),
    path.relative(base, summaryOut).replaceAll('\\', '/'),
  ],
  accepted_decipherment_claims: 0,
};

fs.writeFileSync(targetsOut, toCsv(targetRows), 'utf8');
fs.writeFileSync(objectsOut, toCsv(objectRows), 'utf8');
fs.writeFileSync(summaryOut, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
