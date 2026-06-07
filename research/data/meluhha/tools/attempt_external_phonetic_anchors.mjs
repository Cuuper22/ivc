import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const OUT = path.join(ROOT, 'data', 'meluhha');
const RUN_DATE = '2026-05-29';

const EXTERNAL_OBJECTS = path.join(OUT, 'external_indus_objects.csv');
const CDLI_SUMMARY = path.join(OUT, 'cdli_current_anchor_failure_summary.json');

const CANDIDATE_FIELDS = [
  'candidate_id',
  'target_id',
  'target_label',
  'target_source',
  'target_units',
  'target_pattern',
  'external_row_id',
  'external_site',
  'external_region',
  'external_type',
  'external_symbol',
  'external_text',
  'external_units',
  'external_pattern',
  'candidate_assignments',
  'candidate_values',
  'focus_lane',
  'data_tier',
  'decision',
  'skeptic_reason',
];

const SUMMARY_FIELDS = [
  'target_id',
  'target_label',
  'target_units',
  'target_pattern',
  'focus_exact_candidates',
  'all_external_exact_candidates',
  'corpus_exact_candidates',
  'forger_iterations',
  'forger_mean_focus_candidates',
  'forger_max_focus_candidates',
  'forger_ge_observed_share',
  'decision',
];

const ITER_FIELDS = [
  'target_id',
  'iteration',
  'synthetic_pattern',
  'synthetic_units',
  'focus_candidates',
];

const TARGETS = [
  {
    target_id: 'toponym_meluhha',
    label: 'Meluhha toponym',
    source: 'ORACC/ePSD2 Meluhha GN entry and CDLI current Meluhha exports',
    units: ['me', 'luh', 'ha'],
    note: 'All-distinct syllable pattern; high-risk because length-only fits are expected.',
  },
  {
    target_id: 'ship_ma2_meluhha',
    label: 'ma2 me-luh-ha / Meluhha ship context',
    source: 'CDLI current ma2 me-luh-ha exports',
    units: ['ma2', 'me', 'luh', 'ha'],
    note: 'All-distinct four-unit target from ship context.',
  },
  {
    target_id: 'name_lu_sunzida',
    label: 'lu2-sun2-zi-da / Lu-sunzida',
    source: 'CDLI P212982 adjacency and current Lu-Sunzida matched-negative export',
    units: ['lu2', 'sun2', 'zi', 'da'],
    note: 'Explicitly already failed as a Meluhha diagnostic; still attempted as a phonetic string.',
  },
  {
    target_id: 'interpreter_shu_ilishu',
    label: 'szu-i3-li2-su / Shu-ilishu',
    source: 'CDLI seals 014339 physical, line before eme-bal me-luh-ha{ki}',
    units: ['szu', 'i3', 'li2', 'su'],
    note: 'Personal name on cuneiform interpreter seal; first and last are kept distinct because the transliteration differs.',
  },
  {
    target_id: 'title_emebal_meluhha_six_unit',
    label: 'eme-bal me-luh-ha interpreter title',
    source: 'CDLI seals 014339 physical, eme-bal me-luh-ha{ki}',
    units: ['e', 'me', 'bal', 'me', 'luh', 'ha'],
    note: 'Duplicate me pattern provides an actual shape constraint under strict one-sign-per-unit testing.',
  },
];

const FOCUS_SITES = new Set([
  'Ur',
  'Susa',
  'Failaka',
  'Kish',
  'Nippur',
  'Girsu',
  'Tello',
  'Tell Umma',
  "Qala'at al-Bahrain",
  "Ra's al-Junayz",
  'Karzakan',
  'Saar',
  'Janabiyah',
  'Kalba',
  'Salut',
  'Hajar',
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
  const header = rows[0];
  return rows.slice(1).filter((r) => r.some((v) => v !== '')).map((r) => {
    const out = {};
    header.forEach((h, i) => {
      out[h] = r[i] ?? '';
    });
    return out;
  });
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

function stableId(parts) {
  return crypto.createHash('sha1').update(parts.join('\u241f'), 'utf8').digest('hex').slice(0, 16);
}

function parseSigns(text) {
  return String(text ?? '')
    .replace(/[+\[\]]/g, '')
    .split(/[-/]/)
    .map((unit) => unit.trim())
    .filter(Boolean)
    .filter((unit) => /^\d{3}$/.test(unit));
}

function pattern(units) {
  const seen = new Map();
  let next = 0;
  return units.map((unit) => {
    if (!seen.has(unit)) {
      seen.set(unit, String.fromCharCode(65 + next));
      next += 1;
    }
    return seen.get(unit);
  }).join('');
}

function compatible(targetUnits, signUnits) {
  if (targetUnits.length !== signUnits.length) return false;
  return pattern(targetUnits) === pattern(signUnits);
}

function assignments(targetUnits, signUnits) {
  return targetUnits.map((unit, i) => `${signUnits[i]}=${unit}`).join(';');
}

function signValues(targetUnits, signUnits) {
  const rows = [];
  const seen = new Set();
  targetUnits.forEach((unit, i) => {
    const key = `${signUnits[i]}=${unit}`;
    if (seen.has(key)) return;
    seen.add(key);
    rows.push(key);
  });
  return rows.join(';');
}

function seededRandom(seedText) {
  let state = crypto.createHash('sha256').update(seedText).digest().readUInt32LE(0);
  return () => {
    state = (state * 1664525 + 1013904223) >>> 0;
    return state / 2 ** 32;
  };
}

function syntheticUnitsForPattern(patternText, rand) {
  const symbolToUnit = new Map();
  let counter = 0;
  const alphabet = 'abcdefghijklmnopqrstuvwxyz';
  return [...patternText].map((ch) => {
    if (!symbolToUnit.has(ch)) {
      const suffix = Math.floor(rand() * 1000000).toString(36);
      symbolToUnit.set(ch, `p${alphabet[counter % alphabet.length]}${suffix}`);
      counter += 1;
    }
    return symbolToUnit.get(ch);
  });
}

function candidateCount(objects, units) {
  return objects.filter((row) => compatible(units, row._signs)).length;
}

function main() {
  const externalRows = parseCsv(fs.readFileSync(EXTERNAL_OBJECTS, 'utf8')).map((row) => ({
    ...row,
    _signs: parseSigns(row.text),
    _focus: FOCUS_SITES.has(row.site) || row.region === 'Persian Gulf',
  })).filter((row) => row._signs.length > 0);

  const focusRows = externalRows.filter((row) => row._focus);
  const candidates = [];
  const summaries = [];
  const iterations = [];
  const forgerIterations = 2000;

  for (const target of TARGETS) {
    const targetPattern = pattern(target.units);
    const matchingRows = externalRows.filter((row) => compatible(target.units, row._signs));
    const matchingFocusRows = matchingRows.filter((row) => row._focus);

    for (const row of matchingFocusRows) {
      const dataTierReasons = [];
      if (row.provenance_tier) dataTierReasons.push(row.provenance_tier);
      if (/[?\[\]]/.test(row.text_length) || /[\[\]]/.test(row.text)) dataTierReasons.push('damaged_or_open_text');
      if (row.source_ref?.includes('lipi')) dataTierReasons.push('metadata_not_source_validated');

      const decision = target.target_id === 'title_emebal_meluhha_six_unit'
        ? 'no_candidate_expected_if_duplicate_me_constraint_fails'
        : 'retracted_length_pattern_only';
      const skeptic = [
        'No object-level pairing between this cuneiform attestation and this Indus-style object.',
        'The candidate is generated by syllable-count/sign-count pattern compatibility only.',
        'External Indus object row remains source-image/catalogue unvalidated in this workspace.',
        'No language-family prior used, so no lexical rescue is allowed.',
      ].join(' ');

      candidates.push({
        candidate_id: `cand_${stableId([target.target_id, row.row_id, row.text])}`,
        target_id: target.target_id,
        target_label: target.label,
        target_source: target.source,
        target_units: target.units.join('-'),
        target_pattern: targetPattern,
        external_row_id: row.row_id,
        external_site: row.site,
        external_region: row.region,
        external_type: row.type,
        external_symbol: row.symbol,
        external_text: row.text,
        external_units: row._signs.join('-'),
        external_pattern: pattern(row._signs),
        candidate_assignments: assignments(target.units, row._signs),
        candidate_values: signValues(target.units, row._signs),
        focus_lane: row._focus ? 'mesopotamia_gulf_focus' : 'external_nonfocus',
        data_tier: dataTierReasons.join('|'),
        decision,
        skeptic_reason: skeptic,
      });
    }

    const rand = seededRandom(`external-anchor-forger:${target.target_id}`);
    let ge = 0;
    let sum = 0;
    let max = 0;
    for (let i = 0; i < forgerIterations; i += 1) {
      const synthetic = syntheticUnitsForPattern(targetPattern, rand);
      const count = candidateCount(focusRows, synthetic);
      if (count >= matchingFocusRows.length) ge += 1;
      sum += count;
      if (count > max) max = count;
      iterations.push({
        target_id: target.target_id,
        iteration: i,
        synthetic_pattern: targetPattern,
        synthetic_units: synthetic.join('-'),
        focus_candidates: count,
      });
    }

    let decision = 'failed_forger_gate';
    if (matchingFocusRows.length === 0) decision = 'no_strict_pattern_candidate';
    if (ge / forgerIterations >= 0.05 && matchingFocusRows.length > 0) decision = 'failed_forger_gate_length_pattern_common';

    summaries.push({
      target_id: target.target_id,
      target_label: target.label,
      target_units: target.units.join('-'),
      target_pattern: targetPattern,
      focus_exact_candidates: matchingFocusRows.length,
      all_external_exact_candidates: matchingRows.length,
      corpus_exact_candidates: matchingRows.length,
      forger_iterations: forgerIterations,
      forger_mean_focus_candidates: sum / forgerIterations,
      forger_max_focus_candidates: max,
      forger_ge_observed_share: ge / forgerIterations,
      decision,
    });
  }

  const luSummary = fs.existsSync(CDLI_SUMMARY) ? JSON.parse(fs.readFileSync(CDLI_SUMMARY, 'utf8')) : null;
  const report = {
    date: RUN_DATE,
    status: 'external_phonetic_anchor_attempts_no_survivor',
    scope: {
      external_objects_total_with_parseable_signs: externalRows.length,
      focus_objects_mesopotamia_gulf_with_parseable_signs: focusRows.length,
      focus_sites: [...new Set(focusRows.map((row) => row.site))].sort(),
      note: 'Focus rows are physically external Indus/Indus-style rows from Mesopotamia and Gulf sites in the local table. Iranian Plateau/Central Asian rows are retained as external context but not focus-lane evidence.',
    },
    targets: TARGETS.map((target) => ({
      target_id: target.target_id,
      label: target.label,
      units: target.units,
      pattern: pattern(target.units),
      source: target.source,
      note: target.note,
    })),
    forger: {
      iterations_per_target: forgerIterations,
      null: 'synthetic phonetic targets with identical duplicate pattern and length; because strict pattern compatibility ignores phonetic identity, any target with the same pattern should recover the same candidate count.',
      summary: summaries,
    },
    strongest_attempts: candidates.slice(0, 10).map((row) => ({
      candidate_id: row.candidate_id,
      target_id: row.target_id,
      target_label: row.target_label,
      external_row_id: row.external_row_id,
      external_site: row.external_site,
      external_text: row.external_text,
      candidate_values: row.candidate_values,
      decision: row.decision,
    })),
    lu_sunzida_prior_gate: luSummary?.lu_sunzida_detector_test ?? null,
    decision: 'No external phonetic candidate survives. All actual assignments are length/pattern-only and have forger_ge_observed_share 1 when candidates exist, or no candidate under stricter duplicate-pattern targets.',
    next_gate: 'A candidate can only be rerun if an external Indus object is source-validated and paired to a specific cuneiform attestation by more than length, site, or desired reading: accession/publication linkage, owner/profession linkage, or independent sign-sequence repetition tied to the same cuneiform name/token.',
    files: {
      candidates: 'data/meluhha/external_phonetic_anchor_candidates.csv',
      summary: 'data/meluhha/external_phonetic_anchor_summary.json',
      target_summary: 'data/meluhha/external_phonetic_anchor_target_summary.csv',
      forger_iterations: 'data/meluhha/external_phonetic_anchor_forger_iterations.csv',
    },
  };

  writeCsv(path.join(OUT, 'external_phonetic_anchor_candidates.csv'), candidates, CANDIDATE_FIELDS);
  writeCsv(path.join(OUT, 'external_phonetic_anchor_target_summary.csv'), summaries, SUMMARY_FIELDS);
  writeCsv(path.join(OUT, 'external_phonetic_anchor_forger_iterations.csv'), iterations, ITER_FIELDS);
  fs.writeFileSync(path.join(OUT, 'external_phonetic_anchor_summary.json'), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
}

main();
