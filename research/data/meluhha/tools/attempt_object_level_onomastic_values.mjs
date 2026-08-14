// A second, stricter attempt (2026-05-30) to attach sound values to Indus signs
// via Meluhha-related cuneiform phrases — this time demanding an object-level
// bridge, not just a pattern match. It reads the external Indus objects table
// and the expanded cuneiform attestation inventory, and tests 12 target phrases
// (the Meluhha toponym, ship and ration formulae, personal names like
// Lu-sunzida and Shu-ilishu, commodity phrases). A candidate needs three things:
// the same length and repeat pattern of units, the same find site (with
// Girsu/Tello treated as one site), and a modeled object route — a hand-curated
// table here grades each external row from "verified object mapping" down to
// "unmapped fragment". Every candidate is still rejected with an explicit
// skeptic reason, because even the verified objects are Indus-only with no
// readable cuneiform on the same object. A 10000-iteration forger shuffles the
// targets' sites to show the same-site pattern hits arise by chance. Writes a
// candidates CSV, forger iterations CSV, and a JSON summary: zero anchors.
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const OUT = path.join(ROOT, 'data', 'meluhha');
const RUN_DATE = '2026-05-30';

const EXTERNAL_OBJECTS = path.join(OUT, 'external_indus_objects.csv');
const CUNEIFORM_INVENTORY = path.join(OUT, 'cuneiform_attestations_expanded.csv');

const CANDIDATE_OUT = path.join(OUT, 'object_level_onomastic_value_attempts.csv');
const NULL_OUT = path.join(OUT, 'object_level_onomastic_value_forger_iterations.csv');
const SUMMARY_OUT = path.join(OUT, 'object_level_onomastic_value_summary.json');

const CANDIDATE_FIELDS = [
  'candidate_id',
  'target_id',
  'target_label',
  'target_source_id',
  'target_site',
  'target_units',
  'target_pattern',
  'external_row_id',
  'external_site',
  'external_object_route',
  'external_object_tier',
  'external_text',
  'external_units',
  'external_pattern',
  'candidate_assignments',
  'candidate_values',
  'site_relation',
  'object_bridge_state',
  'pattern_site_candidate_count',
  'pattern_all_focus_count',
  'same_row_target_ambiguity_count',
  'decision',
  'skeptic_reason',
];

const NULL_FIELDS = [
  'iteration',
  'null_candidate_count',
  'null_candidate_ids',
];

const OBJECT_ROUTE_OVERRIDES = {
  '147.1': {
    object_route: 'Failaka Kjaerum 1983 cat.279/319 unresolved',
    tier: 'catalogue_candidate_unresolved',
    object_bridge_state: 'no_exact_row_to_catalogue_mapping',
  },
  '148.1': {
    object_route: 'Failaka Kjaerum 1983 cat.279/319 unresolved',
    tier: 'catalogue_candidate_unresolved',
    object_bridge_state: 'no_exact_row_to_catalogue_mapping',
  },
  '3882.1': {
    object_route: 'Susa SB 2425 / AS 41 / CCO S.299 candidate route',
    tier: 'catalogue_candidate_unverified',
    object_bridge_state: 'no_readable_cuneiform_on_object_in_workspace',
  },
  '3885.1': {
    object_route: 'Tello/Girsu Sarzec-Heuzey pl.30.3a-b candidate route',
    tier: 'catalogue_candidate_unresolved',
    object_bridge_state: 'no_exact_accession_mapping',
  },
  '3897.1': {
    object_route: 'Gadd no.2 / BM 122187 candidate by site shape icon length only',
    tier: 'publication_candidate_not_accession_verified',
    object_bridge_state: 'no_exact_accession_mapping',
  },
  '3898.1': {
    object_route: 'Gadd no.16 / U17649 verified local row mapping',
    tier: 'verified_object_mapping_indus_only',
    object_bridge_state: 'mapped_indus_object_no_readable_cuneiform_bridge',
  },
  '3899.1': {
    object_route: 'Gadd no.15 / U8685 verified local row mapping',
    tier: 'verified_object_mapping_indus_only',
    object_bridge_state: 'mapped_indus_object_no_readable_cuneiform_bridge',
  },
  '5222.1': {
    object_route: 'Girsu/Tello Gulf Type route candidate unresolved',
    tier: 'catalogue_candidate_unresolved',
    object_bridge_state: 'no_exact_accession_mapping',
  },
  '5225.1': {
    object_route: 'Ur Gadd/Mitchell route pool unresolved',
    tier: 'unmapped_fragment',
    object_bridge_state: 'no_exact_accession_mapping',
  },
  '5231.1': {
    object_route: 'Gadd no.4 / BM 122188 weak fragment candidate',
    tier: 'weak_publication_candidate_not_accession_verified',
    object_bridge_state: 'no_exact_accession_mapping',
  },
};

const TARGETS = [
  {
    target_id: 'toponym_meluhha',
    label: 'me-luh-ha / Meluhha toponym',
    source_id: 'multiple',
    target_site: '*',
    units: ['me', 'luh', 'ha'],
    target_class: 'toponym',
  },
  {
    target_id: 'ship_ma2_meluhha',
    label: 'ma2 me-luh-ha / Meluhha ship or route context',
    source_id: 'CDLI route and literary contexts',
    target_site: '*',
    units: ['ma2', 'me', 'luh', 'ha'],
    target_class: 'route_phrase',
  },
  {
    target_id: 'name_lu_sunzida',
    label: 'lu2-sun2-zi-da / Lu-sunzida',
    source_id: 'P212982 line 5',
    target_site: '*',
    units: ['lu2', 'sun2', 'zi', 'da'],
    target_class: 'personal_name_adjacent',
  },
  {
    target_id: 'interpreter_shu_ilishu',
    label: 'szu-i3-li2-su / Shu-ilishu',
    source_id: 'P525331 / CDLI Seals 014339',
    target_site: '*',
    units: ['szu', 'i3', 'li2', 'su'],
    target_class: 'interpreter_name',
  },
  {
    target_id: 'title_emebal_meluhha',
    label: 'e-me-bal me-luh-ha / interpreter title',
    source_id: 'P525331 / CDLI Seals 014339',
    target_site: '*',
    units: ['e', 'me', 'bal', 'me', 'luh', 'ha'],
    target_class: 'title',
  },
  {
    target_id: 'ur_guna_meluhha',
    label: 'ur gun3-a me-luh-ha / Meluhha dog/object phrase',
    source_id: 'P432309 line 9',
    target_site: 'Ur',
    units: ['ur', 'gun3', 'a', 'me', 'luh', 'ha'],
    target_class: 'object_or_animal_label',
  },
  {
    target_id: 'dar_meluhha',
    label: 'dar me-luh-ha / Ur administrative object phrase',
    source_id: 'BDTNS 011069 / P137088 line 4',
    target_site: 'Ur',
    units: ['dar', 'me', 'luh', 'ha'],
    target_class: 'object_or_commodity_designation',
  },
  {
    target_id: 'ur_dlamma_dumu_meluhha',
    label: 'ur-dlamma dumu me-luh-ha',
    source_id: 'BDTNS 000128 / P108448',
    target_site: 'Girsu',
    units: ['ur', 'dlamma', 'dumu', 'me', 'luh', 'ha'],
    target_class: 'personal_name_with_origin',
  },
  {
    target_id: 'ur_digalim_dumu_meluhha',
    label: 'ur-digalim dumu me-luh-ha',
    source_id: 'P124739',
    target_site: 'Girsu',
    units: ['ur', 'digalim', 'dumu', 'me', 'luh', 'ha'],
    target_class: 'personal_name_with_origin',
  },
  {
    target_id: 'dumu_meluhha',
    label: 'dumu me-luh-ha',
    source_id: 'multiple Ur III formulae',
    target_site: '*',
    units: ['dumu', 'me', 'luh', 'ha'],
    target_class: 'origin_formula',
  },
  {
    target_id: 'iba_lu_meluhha',
    label: 'i3-ba lu2 me-luh-ha',
    source_id: 'Irisagrig ration formula',
    target_site: 'Irisagrig',
    units: ['i3', 'ba', 'lu2', 'me', 'luh', 'ha'],
    target_class: 'ration_group_formula',
  },
  {
    target_id: 'gug_girin_meluhha',
    label: 'gug gi-rin me-luh-ha / Meluhha carnelian',
    source_id: 'Gudea commodity contexts',
    target_site: 'Girsu',
    units: ['gug', 'gi', 'rin', 'me', 'luh', 'ha'],
    target_class: 'commodity_phrase',
  },
];

const FOCUS_SITES = new Set([
  'Ur',
  'Susa',
  'Failaka',
  'Girsu',
  'Tello',
  'Tell Umma',
  'Kish',
  'Nippur',
  "Qala'at al-Bahrain",
  'Karzakkan Cemetery',
  'Karzakan',
  'Saar',
  'Janabiyah',
  'Hajar',
  "Ra's al-Junayz",
  'Luristan',
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
  for (const row of rows) {
    lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  }
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function parseSigns(text) {
  return String(text ?? '')
    .replace(/[+\[\]]/g, '')
    .split(/[-/]/)
    .map((unit) => unit.trim())
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

function stableId(parts) {
  return crypto.createHash('sha1').update(parts.join('\u241f'), 'utf8').digest('hex').slice(0, 14);
}

function compatible(target, object) {
  return target._pattern === object._pattern && target.units.length === object._signs.length;
}

function siteRelation(targetSite, objectSite) {
  if (targetSite === '*') return 'generic_meluhha_context_not_site_specific';
  if (targetSite === objectSite) return 'same_site';
  if (targetSite === 'Girsu' && objectSite === 'Tello') return 'girsu_tello_equivalent';
  if (targetSite === 'Tello' && objectSite === 'Girsu') return 'girsu_tello_equivalent';
  return 'site_mismatch';
}

function assignments(target, object) {
  return target.units.map((unit, i) => `${object._signs[i]}=${unit}`).join(';');
}

function uniqueValues(target, object) {
  const seen = new Set();
  const rows = [];
  target.units.forEach((unit, i) => {
    const pair = `${object._signs[i]}=${unit}`;
    if (!seen.has(pair)) {
      seen.add(pair);
      rows.push(pair);
    }
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

function shuffle(values, rand) {
  const out = [...values];
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function buildCandidates(targets, objects) {
  const rows = [];
  for (const target of targets) {
    const matchingPatternObjects = objects.filter((object) => compatible(target, object));
    for (const object of matchingPatternObjects) {
      const relation = siteRelation(target.target_site, object.site);
      const sameRowAmbiguity = targets.filter((other) => compatible(other, object)
        && ['same_site', 'girsu_tello_equivalent', 'generic_meluhha_context_not_site_specific'].includes(siteRelation(other.target_site, object.site))).length;
      const sameSitePatternCount = objects.filter((other) => compatible(target, other)
        && ['same_site', 'girsu_tello_equivalent', 'generic_meluhha_context_not_site_specific'].includes(siteRelation(target.target_site, other.site))).length;

      let decision = 'rejected_site_mismatch_or_generic_context';
      let skeptic = 'The target phrase is not tied to this object by exact object identity; pattern compatibility alone is inadmissible.';

      if (relation === 'same_site' || relation === 'girsu_tello_equivalent') {
        if (object._route.tier === 'verified_object_mapping_indus_only') {
          decision = 'rejected_mapped_indus_object_has_no_readable_script_bridge';
          skeptic = 'The row is object-mapped, but the mapped object is Indus-only in the current source surface. The cuneiform phrase comes from a separate text, so this is still site plus length/pattern evidence.';
        } else if (object._route.tier?.includes('candidate') || object._route.tier?.includes('unresolved') || object._route.tier?.includes('unmapped')) {
          decision = 'rejected_unverified_object_mapping_no_readable_script_bridge';
          skeptic = 'The source route is not exact enough to attach a phonetic string, and no readable-script bridge is attached to the object.';
        }
      }

      rows.push({
        candidate_id: `onomastic_${stableId([target.target_id, object.row_id, object.text])}`,
        target_id: target.target_id,
        target_label: target.label,
        target_source_id: target.source_id,
        target_site: target.target_site,
        target_units: target.units.join('-'),
        target_pattern: target._pattern,
        external_row_id: object.row_id,
        external_site: object.site,
        external_object_route: object._route.object_route,
        external_object_tier: object._route.tier,
        external_text: object.text,
        external_units: object._signs.join('-'),
        external_pattern: object._pattern,
        candidate_assignments: assignments(target, object),
        candidate_values: uniqueValues(target, object),
        site_relation: relation,
        object_bridge_state: object._route.object_bridge_state,
        pattern_site_candidate_count: sameSitePatternCount,
        pattern_all_focus_count: matchingPatternObjects.length,
        same_row_target_ambiguity_count: sameRowAmbiguity,
        decision,
        skeptic_reason: skeptic,
      });
    }
  }
  return rows;
}

function main() {
  const cuneiform = parseCsv(fs.readFileSync(CUNEIFORM_INVENTORY, 'utf8'));
  const cuneiformText = cuneiform.map((row) => `${row.source_id} ${row.transliteration} ${row.attestation_id}`).join('\n').toLowerCase();

  const targets = TARGETS.map((target) => ({
    ...target,
    _pattern: pattern(target.units),
    inventory_hint_present: target.source_id === 'multiple'
      || target.source_id.startsWith('CDLI route')
      || target.source_id.startsWith('Gudea')
      || cuneiformText.includes(target.source_id.toLowerCase().split(' / ')[0])
      || cuneiformText.includes(target.label.toLowerCase().split(' / ')[0]),
  }));

  const externalObjects = parseCsv(fs.readFileSync(EXTERNAL_OBJECTS, 'utf8'))
    .map((row) => ({
      ...row,
      _signs: parseSigns(row.text),
      _route: OBJECT_ROUTE_OVERRIDES[row.row_id] ?? {
        object_route: row.source_ref || 'no object route modeled',
        tier: 'not_in_object_level_queue',
        object_bridge_state: 'not_in_current_object_level_queue',
      },
    }))
    .filter((row) => row._signs.length > 0)
    .filter((row) => FOCUS_SITES.has(row.site) || row.region === 'Persian Gulf' || row.region === 'Mesopotamia')
    .map((row) => ({
      ...row,
      _pattern: pattern(row._signs),
    }));

  const candidates = buildCandidates(targets, externalObjects);
  const attemptedActualValueRows = candidates.filter((row) => row.site_relation === 'same_site'
    || row.site_relation === 'girsu_tello_equivalent');
  const strictMappedAttempts = attemptedActualValueRows.filter((row) => row.external_object_tier === 'verified_object_mapping_indus_only');
  const strictSurvivors = candidates.filter((row) => row.decision === 'accepted_external_anchor');

  const rand = seededRandom('object-level-onomastic-value-forger-v1');
  const sourceSites = targets.map((target) => target.target_site);
  const forgerIterations = 10000;
  const nullRows = [];
  for (let iteration = 0; iteration < forgerIterations; iteration += 1) {
    const shuffledSites = shuffle(sourceSites, rand);
    const shuffledTargets = targets.map((target, idx) => ({
      ...target,
      target_site: shuffledSites[idx],
    }));
    const nullCandidates = buildCandidates(shuffledTargets, externalObjects)
      .filter((row) => row.external_object_tier === 'verified_object_mapping_indus_only')
      .filter((row) => row.site_relation === 'same_site' || row.site_relation === 'girsu_tello_equivalent');
    nullRows.push({
      iteration,
      null_candidate_count: nullCandidates.length,
      null_candidate_ids: nullCandidates.map((row) => `${row.target_id}:${row.external_row_id}`).join(';'),
    });
  }

  const observedStrictMappedSitePatternAttempts = strictMappedAttempts.length;
  const nullGeObserved = nullRows.filter((row) => Number(row.null_candidate_count) >= observedStrictMappedSitePatternAttempts).length / forgerIterations;

  const summary = {
    date: RUN_DATE,
    status: 'object_level_onomastic_values_no_external_anchor',
    target_phrases_tested: targets.length,
    target_inventory_hints_present: targets.filter((target) => target.inventory_hint_present).length,
    focus_external_objects_with_parseable_signs: externalObjects.length,
    candidate_rows_written: candidates.length,
    same_site_or_equivalent_value_attempts: attemptedActualValueRows.length,
    strict_mapped_indus_only_value_attempts: strictMappedAttempts.length,
    accepted_external_anchors: strictSurvivors.length,
    forger: {
      model: 'shuffle target source-sites across fixed cuneiform phrase patterns; count strict mapped Indus-only object attempts that remain same-site/equivalent pattern matches',
      iterations: forgerIterations,
      observed_strict_mapped_site_pattern_attempts: observedStrictMappedSitePatternAttempts,
      null_ge_observed_share: nullGeObserved,
      max_null_candidate_count: Math.max(...nullRows.map((row) => Number(row.null_candidate_count))),
      mean_null_candidate_count: nullRows.reduce((acc, row) => acc + Number(row.null_candidate_count), 0) / forgerIterations,
    },
    strongest_attempts: strictMappedAttempts.map((row) => ({
      candidate_id: row.candidate_id,
      target_id: row.target_id,
      external_row_id: row.external_row_id,
      candidate_values: row.candidate_values,
      decision: row.decision,
      reason: row.skeptic_reason,
    })),
    conclusion: 'Actual candidate sign values were attempted only where source route plus row/object status justified the swing. The only strict mapped attempt is still a separate-text same-site pattern match on an Indus-only object, so it earns no phonetic value.',
  };

  writeCsv(CANDIDATE_OUT, candidates, CANDIDATE_FIELDS);
  writeCsv(NULL_OUT, nullRows, NULL_FIELDS);
  fs.writeFileSync(SUMMARY_OUT, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
}

main();
