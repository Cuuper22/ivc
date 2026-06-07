import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_terminal_governor_leave_site_stress_20260531';
const RUN_DATE = '2026-05-31';
const EDGES = ['002-817', '002-820', '002-861', '060-920', '060-550', '060-820', '060-692'];

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
      if (row.some((value) => value.length)) rows.push(row);
      row = [];
      cell = '';
    } else {
      cell += ch;
    }
  }
  if (cell.length || row.length) {
    row.push(cell.replace(/\r$/, ''));
    if (row.some((value) => value.length)) rows.push(row);
  }
  const [header, ...body] = rows;
  return body.map((cols) => Object.fromEntries(header.map((name, idx) => [name, cols[idx] ?? ''])));
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function exactKey(parts) {
  return parts.join('|');
}

function esc(value) {
  const text = String(value ?? '');
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const body = rows.map((row) => fields.map((field) => esc(row[field])).join(',')).join('\n');
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`, 'utf8');
}

function score(rows, leaveSite) {
  const seen = new Set();
  const map = new Map(EDGES.map((edge) => [edge, {
    edge,
    exact_cells: 0,
    terminal_cells: 0,
    sites: new Set(),
    types: new Set(),
  }]));
  for (const row of rows) {
    if (leaveSite !== 'NONE' && row.site === leaveSite) continue;
    const toks = tokens(row.text);
    for (let i = 0; i < toks.length - 1; i += 1) {
      const edge = `${toks[i]}-${toks[i + 1]}`;
      if (!map.has(edge)) continue;
      const next2 = toks[i + 2] ?? '<END>';
      const key = exactKey([edge, next2, row.text, row.site, row.type, row.symbol]);
      if (seen.has(key)) continue;
      seen.add(key);
      const item = map.get(edge);
      item.exact_cells += 1;
      if (next2 === '<END>') item.terminal_cells += 1;
      item.sites.add(row.site);
      item.types.add(row.type);
    }
  }
  return [...map.values()].map((item) => ({
    leave_site: leaveSite,
    edge: item.edge,
    tier: ['002-861', '060-692'].includes(item.edge) ? 'near_leaky' : 'strict',
    exact_cells: item.exact_cells,
    terminal_cells: item.terminal_cells,
    terminal_share: item.exact_cells ? item.terminal_cells / item.exact_cells : '',
    remaining_sites: item.sites.size,
    remaining_types: item.types.size,
  }));
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const sites = [...new Set(rows.map((row) => row.site).filter(Boolean))]
  .sort((a, b) => a.localeCompare(b));
const stressRows = ['NONE', ...sites].flatMap((site) => score(rows, site));
const summary = {
  date: RUN_DATE,
  phase: 'EXPAND',
  candidate_id: PREFIX,
  tier: 'candidate_stress_table',
  target_edges: EDGES,
  interpretation: 'Strict edges remain high-share when support remains, but the full strict network is support-sensitive under leave-Mohenjo because 060-550 and 060-820 fall below broad support. Near edge 060-692 is site-sensitive: it becomes clean without Mohenjo-daro but weakens without Harappa. 002-861 remains a high-support leaky edge rather than a strict closure.',
  report_csv: `data/open_prototype/reports/${PREFIX}.csv`,
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
writeCsv(path.join(OUT_DIR, `${PREFIX}.csv`), stressRows, [
  'leave_site',
  'edge',
  'tier',
  'exact_cells',
  'terminal_cells',
  'terminal_share',
  'remaining_sites',
  'remaining_types',
]);

console.log(JSON.stringify({
  candidate_id: PREFIX,
  none: stressRows.filter((row) => row.leave_site === 'NONE'),
  leave_mohenjo: stressRows.filter((row) => row.leave_site === 'Mohenjo-daro'),
  leave_harappa: stressRows.filter((row) => row.leave_site === 'Harappa'),
}, null, 2));
