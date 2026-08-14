// Final bridge retest (2026-05-29) for the cuneiform context leads that
// survived the matched-negative gate as "candidate_only". For each surviving
// query, grouped by the cuneiform site it appears at, this script asks: does
// any external Indus object at the same site (or anywhere in Mesopotamia, the
// Gulf, or the Iranian Plateau) carry a sign sequence with the same length and
// repeat pattern as the query's units? It reads the matched-negative summary
// and artifact CSVs plus external_indus_objects.csv, counts strict pattern
// matches per site, and records that no object-level bridge (accession,
// publication, title, or person link) exists for any row — so every row is
// "rejected_no_object_level_bridge". The pattern-only forger share is 1.0 by
// construction: any synthetic query with the same pattern matches just as
// well. Writes context_lead_external_bridge_retest.csv and a JSON summary
// with zero accepted anchors.
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const OUT = path.join(ROOT, 'data', 'meluhha');
const RUN_DATE = '2026-05-29';

const NEGATIVE_SUMMARY_IN = path.join(OUT, 'cdli_context_lead_matched_negative_summary.csv');
const NEGATIVE_ARTIFACTS_IN = path.join(OUT, 'cdli_context_lead_matched_negative_artifacts.csv');
const EXTERNAL_OBJECTS_IN = path.join(OUT, 'external_indus_objects.csv');
const OUT_CSV = path.join(OUT, 'context_lead_external_bridge_retest.csv');
const OUT_JSON = path.join(OUT, 'context_lead_external_bridge_retest_summary.json');

const FIELDS = [
  'bridge_test_id',
  'query_text',
  'lead_label',
  'query_role',
  'cuneiform_site',
  'cuneiform_artifact_count',
  'cuneiform_artifact_ps',
  'cuneiform_periods',
  'target_unit_count',
  'target_duplicate_pattern',
  'same_site_external_count',
  'same_site_external_rows',
  'same_site_strict_pattern_match_count',
  'same_site_strict_pattern_match_rows',
  'mesopotamia_gulf_external_count',
  'mesopotamia_gulf_strict_pattern_match_count',
  'mesopotamia_gulf_strict_pattern_match_rows',
  'object_level_bridge_present',
  'pattern_only_forger_ge_observed_share',
  'decision',
  'skeptic_note',
];

const FOCUS_REGIONS = new Set(['Mesopotamia', 'Persian Gulf', 'Iranian Plateau']);
const FOCUS_SITES = new Set(['Ur', 'Susa', 'Failaka']);

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

function parseMaybeJsonField(value, key) {
  const text = String(value ?? '').trim();
  if (!text) return '';
  if (text.startsWith('{') || text.startsWith('[')) {
    try {
      const parsed = JSON.parse(text);
      if (Array.isArray(parsed)) return parsed.map((item) => parseMaybeJsonField(JSON.stringify(item), key)).filter(Boolean).join('|');
      if (parsed && typeof parsed === 'object') return String(parsed[key] ?? parsed.provenience ?? parsed.period ?? parsed.label ?? parsed.name ?? text);
    } catch {
      return text;
    }
  }
  return text;
}

function siteFromProvenience(value) {
  const text = parseMaybeJsonField(value, 'provenience');
  if (/ur \(mod\. tell muqayyar\)|\bur\b/i.test(text)) return 'Ur';
  if (/girsu|tello/i.test(text)) return 'Girsu/Tello';
  if (/nippur/i.test(text)) return 'Nippur';
  if (/kish/i.test(text)) return 'Kish';
  if (/adab|bismaya/i.test(text)) return 'Adab';
  if (/irisagrig/i.test(text)) return 'Irisagrig';
  if (/susa/i.test(text)) return 'Susa';
  if (/failaka/i.test(text)) return 'Failaka';
  return text || 'unknown';
}

function externalRowsForSite(externalRows, site) {
  if (site === 'Girsu/Tello') return externalRows.filter((row) => row.site === 'Girsu' || row.site === 'Tello');
  return externalRows.filter((row) => row.site === site);
}

function parseExternalSigns(text) {
  return String(text ?? '')
    .replace(/[+\[\]]/g, '')
    .split(/[-/]/)
    .map((unit) => unit.trim())
    .filter(Boolean)
    .filter((unit) => /^\d{3}$/.test(unit));
}

function targetUnits(queryText) {
  return String(queryText ?? '')
    .replace(/[{}]/g, '')
    .replace(/#/g, '')
    .split(/[\s-]+/)
    .map((unit) => unit.trim())
    .filter(Boolean)
    .filter((unit) => !/^(ki|ta|da|ka|ke4|sze3)$/i.test(unit));
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

function uniqueSorted(values) {
  return [...new Set(values.filter(Boolean))].sort();
}

function strictPatternMatches(rows, targetPattern) {
  return rows.filter((row) => {
    const signs = parseExternalSigns(row.text);
    return signs.length > 0 && pattern(signs) === targetPattern;
  });
}

function main() {
  const negativeSummary = parseCsv(fs.readFileSync(NEGATIVE_SUMMARY_IN, 'utf8'));
  const candidateQueryIds = new Set(negativeSummary.filter((row) => row.passes_negative_gate === 'candidate_only').map((row) => row.query_id));
  const artifactRows = parseCsv(fs.readFileSync(NEGATIVE_ARTIFACTS_IN, 'utf8')).filter((row) => candidateQueryIds.has(row.query_id));
  const externalRows = parseCsv(fs.readFileSync(EXTERNAL_OBJECTS_IN, 'utf8'));
  const mesopotamiaGulfRows = externalRows.filter((row) => FOCUS_REGIONS.has(row.region));

  const byQuerySite = new Map();
  for (const row of artifactRows) {
    if (Number(row.query_line_count) <= 0 || row.has_meluhha_anywhere !== 'true') continue;
    const site = siteFromProvenience(row.provenience);
    const key = [row.query_id, row.query_text, site].join('\u241f');
    const group = byQuerySite.get(key) ?? {
      query_id: row.query_id,
      query_text: row.query_text,
      lead_label: row.lead_label,
      query_role: row.query_role,
      cuneiform_site: site,
      artifacts: [],
    };
    group.artifacts.push(row);
    byQuerySite.set(key, group);
  }

  const bridgeRows = [...byQuerySite.values()].map((group) => {
    const units = targetUnits(group.query_text);
    const targetPattern = pattern(units);
    const sameSiteRows = externalRowsForSite(externalRows, group.cuneiform_site);
    const sameSiteMatches = strictPatternMatches(sameSiteRows, targetPattern);
    const focusMatches = strictPatternMatches(mesopotamiaGulfRows, targetPattern);
    const objectLevelBridgePresent = 'false';
    const isFocusSite = FOCUS_SITES.has(group.cuneiform_site);
    const decision = objectLevelBridgePresent === 'true'
      ? 'not_evaluated_object_level_bridge_claim'
      : 'rejected_no_object_level_bridge';
    const skepticNote = isFocusSite
      ? 'Ur/Susa/Failaka-style site proximity is explicitly insufficient: no accession/publication/title/person bridge connects this cuneiform phrase to a specific Indus object row.'
      : 'This is not an Ur/Susa/Failaka object-level bridge; same-site or same-region pattern matches remain site-overlap/length-pattern evidence only.';
    return {
      bridge_test_id: `bridge_${stableId([group.query_id, group.cuneiform_site])}`,
      query_text: group.query_text,
      lead_label: group.lead_label,
      query_role: group.query_role,
      cuneiform_site: group.cuneiform_site,
      cuneiform_artifact_count: uniqueSorted(group.artifacts.map((row) => row.artifact_p)).length,
      cuneiform_artifact_ps: uniqueSorted(group.artifacts.map((row) => row.artifact_p)).join('|'),
      cuneiform_periods: uniqueSorted(group.artifacts.map((row) => parseMaybeJsonField(row.period, 'period'))).join('|'),
      target_unit_count: units.length,
      target_duplicate_pattern: targetPattern,
      same_site_external_count: sameSiteRows.length,
      same_site_external_rows: sameSiteRows.map((row) => `${row.row_id}:${row.site}:${row.text}`).join('|'),
      same_site_strict_pattern_match_count: sameSiteMatches.length,
      same_site_strict_pattern_match_rows: sameSiteMatches.map((row) => `${row.row_id}:${row.site}:${row.text}`).join('|'),
      mesopotamia_gulf_external_count: mesopotamiaGulfRows.length,
      mesopotamia_gulf_strict_pattern_match_count: focusMatches.length,
      mesopotamia_gulf_strict_pattern_match_rows: focusMatches.map((row) => `${row.row_id}:${row.site}:${row.text}`).join('|'),
      object_level_bridge_present: objectLevelBridgePresent,
      pattern_only_forger_ge_observed_share: '1.000000',
      decision,
      skeptic_note: skepticNote,
    };
  }).sort((a, b) => a.query_text.localeCompare(b.query_text) || a.cuneiform_site.localeCompare(b.cuneiform_site));

  const focusBridgeRows = bridgeRows.filter((row) => FOCUS_SITES.has(row.cuneiform_site));
  const anyObjectLevel = bridgeRows.some((row) => row.object_level_bridge_present === 'true');
  const summary = {
    run_date: RUN_DATE,
    candidate_only_query_count: candidateQueryIds.size,
    candidate_artifact_rows: artifactRows.length,
    bridge_test_rows: bridgeRows.length,
    ur_susa_failaka_bridge_test_rows: focusBridgeRows.length,
    object_level_bridge_count: anyObjectLevel ? bridgeRows.filter((row) => row.object_level_bridge_present === 'true').length : 0,
    strict_pattern_only_rows_with_same_site_match: bridgeRows.filter((row) => Number(row.same_site_strict_pattern_match_count) > 0).length,
    strict_pattern_only_rows_with_mesopotamia_gulf_match: bridgeRows.filter((row) => Number(row.mesopotamia_gulf_strict_pattern_match_count) > 0).length,
    accepted_external_anchor_count: 0,
    output: path.relative(ROOT, OUT_CSV).replaceAll('\\', '/'),
    decision: 'No candidate-only cuneiform lead is promoted to an external Indus anchor. Same-site and same-region length/pattern matches remain rejected unless tied by object-level provenance.',
    caveats: [
      'The local external object rows are T3 quarantined Lipi metadata and still need source-image/catalogue validation.',
      'The forger value is 1.0 by construction for pattern-only matching: any synthetic cuneiform target with the same duplicate pattern would produce the same match count.',
      'No row here contains a verified accession-level or publication-level bridge between a CDLI artifact and a specific external Indus object.',
    ],
  };

  writeCsv(OUT_CSV, bridgeRows, FIELDS);
  fs.writeFileSync(OUT_JSON, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
}

main();
