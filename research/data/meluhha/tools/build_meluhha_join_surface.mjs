import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const OUT = path.join(ROOT, 'data', 'meluhha');
const RUN_DATE = '2026-05-29';

const CUNEIFORM = path.join(OUT, 'cuneiform_attestations_expanded.csv');
const EXTERNAL = path.join(OUT, 'external_indus_objects.csv');

const JOIN_FIELDS = [
  'join_id',
  'join_type',
  'status',
  'cuneiform_attestation_id',
  'cuneiform_source_system',
  'cuneiform_source_id',
  'cuneiform_line_ref',
  'cuneiform_token_type',
  'cuneiform_period',
  'cuneiform_dates_referenced',
  'cuneiform_provenience',
  'cuneiform_site_aliases',
  'cuneiform_co_route_tokens',
  'external_row_id',
  'external_cisi',
  'external_region',
  'external_site',
  'external_type',
  'external_material',
  'external_shape',
  'external_symbol',
  'external_text_length',
  'external_text',
  'external_date_status',
  'join_basis',
  'forger_gate_status',
  'skeptic_gate_status',
  'notes',
];

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

function sanitizeId(text) {
  return String(text)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '')
    .slice(0, 100);
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function normalizePlace(text) {
  return String(text ?? '').normalize('NFD').replace(/\p{Diacritic}/gu, '');
}

function siteAliases(provenience) {
  const aliases = [];
  const text = normalizePlace(provenience);
  if (/girsu/i.test(text)) aliases.push('Girsu');
  if (/tello/i.test(text)) aliases.push('Tello');
  if (/\bur\b/i.test(text)) aliases.push('Ur');
  if (/nippur/i.test(text)) aliases.push('Nippur');
  if (/irisagrig/i.test(text)) aliases.push('Irisagrig');
  return unique(aliases);
}

function exactSiteMatches(cuneiformRows, externalRows) {
  const joins = [];
  for (const cuneiform of cuneiformRows) {
    const aliases = siteAliases(cuneiform.provenience);
    if (!aliases.length) continue;
    for (const external of externalRows) {
      if (!aliases.some((alias) => alias.toLowerCase() === String(external.site).toLowerCase())) continue;
      const joinId = [
        'join',
        cuneiform.attestation_id,
        external.row_id,
      ].map(sanitizeId).join('_');
      joins.push({
        join_id: joinId,
        join_type: 'direct_site_overlap',
        status: 'join_surface_not_claim',
        cuneiform_attestation_id: cuneiform.attestation_id,
        cuneiform_source_system: cuneiform.source_system,
        cuneiform_source_id: cuneiform.source_id,
        cuneiform_line_ref: cuneiform.line_ref,
        cuneiform_token_type: cuneiform.token_type,
        cuneiform_period: cuneiform.period,
        cuneiform_dates_referenced: cuneiform.dates_referenced,
        cuneiform_provenience: cuneiform.provenience,
        cuneiform_site_aliases: aliases.join('|'),
        cuneiform_co_route_tokens: cuneiform.co_route_tokens,
        external_row_id: external.row_id,
        external_cisi: external.cisi,
        external_region: external.region,
        external_site: external.site,
        external_type: external.type,
        external_material: external.material,
        external_shape: external.shape,
        external_symbol: external.symbol,
        external_text_length: external.text_length,
        external_text: external.text,
        external_date_status: 'unavailable_in_external_indus_objects_csv',
        join_basis: `external site equals cuneiform provenance alias: ${external.site}`,
        forger_gate_status: 'not_run',
        skeptic_gate_status: 'not_run',
        notes: 'Literal site-overlap join surface only; no sign value, reading, translation, or external anchor is claimed.',
      });
    }
  }
  return joins;
}

function summarize(joins, cuneiformRows, externalRows) {
  const byExternalSite = {};
  const byCuneiformSource = {};
  const byJoinType = {};
  for (const join of joins) {
    byExternalSite[join.external_site] = (byExternalSite[join.external_site] ?? 0) + 1;
    byCuneiformSource[join.cuneiform_source_id] = (byCuneiformSource[join.cuneiform_source_id] ?? 0) + 1;
    byJoinType[join.join_type] = (byJoinType[join.join_type] ?? 0) + 1;
  }

  return {
    date: RUN_DATE,
    status: 'meluhha_indus_join_surface_no_accepted_external_anchor',
    counts: {
      cuneiform_attestation_rows: cuneiformRows.length,
      external_indus_object_rows: externalRows.length,
      join_surface_rows: joins.length,
      accepted_external_anchors: 0,
    },
    by_join_type: byJoinType,
    by_external_site: byExternalSite,
    by_cuneiform_source: byCuneiformSource,
    files: {
      join_surface: 'data/meluhha/meluhha_indus_join_surface.csv',
      join_surface_summary: 'data/meluhha/meluhha_indus_join_surface_summary.json',
    },
    caveats: [
      'The join uses exact external site names against explicit cuneiform provenance aliases only.',
      'External Indus object dates are unavailable in external_indus_objects.csv, so chronology is not scored.',
      'Rows are candidate join lanes for future controls, not evidence of bilingualism or decipherment.',
      'No row can become an external anchor without matched controls, a measured forger false-positive rate, and skeptic review.',
    ],
  };
}

function main() {
  const cuneiformRows = parseCsv(fs.readFileSync(CUNEIFORM, 'utf8'));
  const externalRows = parseCsv(fs.readFileSync(EXTERNAL, 'utf8'));
  const joins = exactSiteMatches(cuneiformRows, externalRows)
    .sort((a, b) => a.join_id.localeCompare(b.join_id));

  writeCsv(path.join(OUT, 'meluhha_indus_join_surface.csv'), joins, JOIN_FIELDS);
  const summary = summarize(joins, cuneiformRows, externalRows);
  fs.writeFileSync(path.join(OUT, 'meluhha_indus_join_surface_summary.json'), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
  console.log(JSON.stringify({
    cuneiform_rows: cuneiformRows.length,
    external_rows: externalRows.length,
    join_rows: joins.length,
  }, null, 2));
}

main();
