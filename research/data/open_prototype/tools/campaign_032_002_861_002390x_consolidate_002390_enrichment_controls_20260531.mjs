// Control battery for the enrichment claim behind the 002-390 frame: when 390
// is preceded by 002, its successor is supposed to land in the branch set
// {095, 705, 125, 530, 590, 692} more often than when 390 stands alone. That
// could be an artifact of where the framed rows come from (one site, one object
// type, damaged texts). So this script collects every 390 successor in the
// local Lipi metadata, tags it framed or unframed, and recomputes the
// framed-minus-unframed enrichment gap inside eight scopes: all rows, SEAL:S
// only, TAB:B only, Mohenjo-daro only, non-Mohenjo, complete texts, good/fine
// condition, and CISI-named objects. Each scope gets a verdict (survives, weak,
// damaged, or underpowered when samples are too small). Writes a controls CSV
// and a summary JSON to data/open_prototype/reports/.

import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_consolidate_002390_enrichment_controls_20260531';
const checkedDate = '2026-05-31';
const xSet = new Set(['095', '705', '125', '530', '590', '692']);

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

function rate(count, total) {
  return total ? count / total : 0;
}

function keepForScope(row, scope) {
  if (scope === 'all') return true;
  if (scope === 'seal_s_only') return row.type === 'SEAL:S';
  if (scope === 'tab_b_only') return row.type === 'TAB:B';
  if (scope === 'mohenjo_only') return row.site === 'Mohenjo-daro';
  if (scope === 'non_mohenjo') return row.site !== 'Mohenjo-daro';
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

const successorRows = [];
for (const row of rows) {
  for (let i = 0; i < row.signs.length - 1; i += 1) {
    if (row.signs[i] !== '390') continue;
    const successor = row.signs[i + 1];
    successorRows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      condition: row.condition,
      complete: row.complete,
      context: i > 0 && row.signs[i - 1] === '002' ? 'framed' : 'unframed',
      successor,
      in_x_set: xSet.has(successor),
      text: row.text,
    });
  }
}

const scopes = ['all', 'seal_s_only', 'tab_b_only', 'mohenjo_only', 'non_mohenjo', 'complete_y', 'good_or_fine', 'cisi_named'];
const controlRows = scopes.map((scope) => {
  const scoped = successorRows.filter((row) => keepForScope(row, scope));
  const framed = scoped.filter((row) => row.context === 'framed');
  const unframed = scoped.filter((row) => row.context === 'unframed');
  const framedRate = rate(framed.filter((row) => row.in_x_set).length, framed.length);
  const unframedRate = rate(unframed.filter((row) => row.in_x_set).length, unframed.length);
  const gap = framedRate - unframedRate;
  return {
    checked_date: checkedDate,
    scope,
    framed_rows: framed.length,
    framed_in_set_rate: framedRate.toFixed(3),
    unframed_rows: unframed.length,
    unframed_in_set_rate: unframedRate.toFixed(3),
    enrichment_gap: gap.toFixed(3),
    verdict:
      framed.length < 3 || unframed.length < 10
        ? 'underpowered'
        : gap >= 0.25
          ? 'survives'
          : gap >= 0.1
            ? 'weak_survival'
            : 'damaged',
  };
});

const serious = controlRows.filter((row) => row.verdict !== 'underpowered');
const survived = serious.filter((row) => row.verdict === 'survives').length;

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: '002390_enrichment_controls',
  serious_controls: serious.length,
  survived_controls: survived,
  controls: Object.fromEntries(
    controlRows.map((row) => [
      row.scope,
      {
        framed_rows: Number(row.framed_rows),
        unframed_rows: Number(row.unframed_rows),
        enrichment_gap: row.enrichment_gap,
        verdict: row.verdict,
      },
    ]),
  ),
  provisional_read:
    survived >= Math.max(1, Math.ceil(serious.length / 2))
      ? '002 frame marker survives basic site/type/source-ish controls.'
      : '002 frame marker is seriously damaged by controls.',
};

writeCsv(path.join(reportsDir, `${prefix}_controls.csv`), controlRows, [
  'checked_date',
  'scope',
  'framed_rows',
  'framed_in_set_rate',
  'unframed_rows',
  'unframed_in_set_rate',
  'enrichment_gap',
  'verdict',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
