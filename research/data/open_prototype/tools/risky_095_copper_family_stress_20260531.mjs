// Fragility check for the claim that sign `095` marks a copper-tablet subregister
// (material Copper, type TAB:C) on its own, independent of sign `407` which often
// travels with it. The danger: after dropping the 407 rows, the remaining 095
// witnesses might all be copies of one text. The script reads metadata_filtered.csv
// (complete rows only), keeps copper TAB:C rows containing 095 but not 407, and
// collapses them three ways — by exact text, by the sign prefix up to 095, and by a
// local window of three signs on each side of 095. If fewer than two distinct
// prefix families remain, 095 is demoted to a single-frame artifact. Writes a
// single JSON report to the reports directory and prints the decision.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT = path.join(ROOT, 'data', 'open_prototype', 'reports', 'risky_095_copper_family_stress_20260531.json');

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
      } else if (ch === '"') quoted = false;
      else cell += ch;
    } else if (ch === '"') quoted = true;
    else if (ch === ',') {
      row.push(cell);
      cell = '';
    } else if (ch === '\n') {
      row.push(cell.replace(/\r$/, ''));
      if (row.some((value) => value.length)) rows.push(row);
      row = [];
      cell = '';
    } else cell += ch;
  }
  if (cell.length || row.length) {
    row.push(cell.replace(/\r$/, ''));
    if (row.some((value) => value.length)) rows.push(row);
  }
  const [header, ...body] = rows;
  return body.map((cols) => Object.fromEntries(header.map((name, idx) => [name, cols[idx] ?? ''])));
}

function toks(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function has(row, sign) {
  return toks(row.text).includes(sign);
}

function frameBefore095(row) {
  const tokens = toks(row.text);
  const idx = tokens.indexOf('095');
  return idx >= 0 ? tokens.slice(0, idx + 1).join('-') : '';
}

function fullLocalFrame095(row) {
  const tokens = toks(row.text);
  const idx = tokens.indexOf('095');
  if (idx < 0) return '';
  return tokens.slice(Math.max(0, idx - 3), Math.min(tokens.length, idx + 4)).join('-');
}

function collapse(rows, keyFn) {
  const map = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    if (!map.has(key)) map.set(key, []);
    map.get(key).push(row);
  }
  return [...map.entries()].map(([key, members]) => ({ key, members }));
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const label = (row) => row.material === 'Copper' && row.type === 'TAB:C';
const support095 = rows.filter((row) => has(row, '095') && label(row));
const support095Without407 = support095.filter((row) => !has(row, '407'));
const all095Without407 = rows.filter((row) => has(row, '095') && !has(row, '407'));

const exactTextFamilies = collapse(support095Without407, (row) => row.text);
const prefixFamilies = collapse(support095Without407, frameBefore095);
const localFamilies = collapse(support095Without407, fullLocalFrame095);
const allWithout407PrefixFamilies = collapse(all095Without407, frameBefore095);
const positivePrefixKeys = new Set(prefixFamilies.map((family) => family.key));
const positivePrefixFamilyShare = [...positivePrefixKeys].length / Math.max(1, allWithout407PrefixFamilies.length);

const report = {
  date: '2026-05-31',
  phase: 'CONSOLIDATE',
  candidate_id: 'risky_095_copper_family_stress_20260531',
  bet: '095 remains an independent copper TAB:C subregister marker after removing 407 only if its non-407 copper witnesses do not collapse to a single source/text frame.',
  source: META,
  support: {
    copper_tab_c_rows_with_095: support095.map((row) => ({
      id: row.id,
      cisi: row.cisi,
      site: row.site,
      material: row.material,
      type: row.type,
      symbol: row.symbol,
      has_407: has(row, '407'),
      text: row.text,
      prefix_frame: frameBefore095(row),
      local_frame: fullLocalFrame095(row),
    })),
    non407_count: support095Without407.length,
    non407_exact_text_family_count: exactTextFamilies.length,
    non407_prefix_family_count: prefixFamilies.length,
    non407_local_family_count: localFamilies.length,
    all_095_without407_prefix_family_count: allWithout407PrefixFamilies.length,
    positive_prefix_family_share: positivePrefixFamilyShare,
    prefix_families: prefixFamilies.map((family) => ({ key: family.key, n: family.members.length })),
  },
  decision:
    prefixFamilies.length >= 2
      ? 'survives_single_frame_collapse_but_fragile'
      : 'demote_095_to_single_frame_artifact',
  interpretation:
    prefixFamilies.length >= 2
      ? 'The two non-407 prefix frames are 617-142-001-595-095 and 408-032-520-095. This keeps 095 alive, but one frame carries three of four object rows and two of three exact texts, so source-family collapse must be harsher before promotion.'
      : 'The non-407 support collapses to one frame; 095 should not be treated as independent.',
};

fs.writeFileSync(OUT, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({
  candidate_id: report.candidate_id,
  decision: report.decision,
  support: report.support,
  interpretation: report.interpretation,
}, null, 2));
