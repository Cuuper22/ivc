import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_806_prefix_context_split_20260531';
const RUN_DATE = '2026-05-31';

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

function esc(value) {
  const text = Array.isArray(value) ? value.join(' | ') : String(value ?? '');
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const body = rows.map((row) => fields.map((field) => esc(row[field])).join(',')).join('\n');
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`, 'utf8');
}

function logFactorials(n) {
  const out = [0];
  for (let i = 1; i <= n; i += 1) out[i] = out[i - 1] + Math.log(i);
  return out;
}

function logChoose(logFact, n, k) {
  if (k < 0 || k > n) return Number.NEGATIVE_INFINITY;
  return logFact[n] - logFact[k] - logFact[n - k];
}

function fisherRight(a, b, c, d) {
  const row1 = a + b;
  const row2 = c + d;
  const col1 = a + c;
  const total = row1 + row2;
  const logFact = logFactorials(total);
  let p = 0;
  for (let x = a; x <= Math.min(row1, col1); x += 1) {
    p += Math.exp(
      logChoose(logFact, col1, x)
      + logChoose(logFact, total - col1, row1 - x)
      - logChoose(logFact, total, row1),
    );
  }
  return p;
}

function countBy(rows, field) {
  return Object.fromEntries([...rows.reduce((acc, row) => {
    const key = row[field] || '';
    acc.set(key, (acc.get(key) ?? 0) + 1);
    return acc;
  }, new Map()).entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])));
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).filter((row) => row.complete === 'Y');
const prefixRows = [];
for (const row of rows) {
  const toks = tokens(row.text);
  for (let i = 1; i < toks.length; i += 1) {
    if (toks[i] !== '806') continue;
    const prev = toks[i - 1];
    if (!['154', '155', '158', '100'].includes(prev)) continue;
    prefixRows.push({
      id: row.id,
      cisi: row.cisi,
      site: row.site,
      type: row.type,
      symbol: row.symbol,
      text: row.text,
      prev,
      next: toks[i + 1] ?? '<END>',
      lane: ['154', '155', '100'].includes(prev) ? 'seal_lane_candidate' : 'tablet_phyt_lane_candidate',
      is_seal: /^SEAL:/.test(row.type) ? 'yes' : 'no',
      is_tablet_b: row.type === 'TAB:B' ? 'yes' : 'no',
      is_no_icon: row.symbol === 'None' ? 'yes' : 'no',
      is_phyt: row.symbol === 'Phyt' ? 'yes' : 'no',
    });
  }
}

const sealLane = prefixRows.filter((row) => row.lane === 'seal_lane_candidate');
const phytLane = prefixRows.filter((row) => row.lane === 'tablet_phyt_lane_candidate');
const sealLaneSeal = sealLane.filter((row) => row.is_seal === 'yes').length;
const phytLaneSeal = phytLane.filter((row) => row.is_seal === 'yes').length;
const phytLaneTablet = phytLane.filter((row) => row.is_tablet_b === 'yes').length;
const sealLaneTablet = sealLane.filter((row) => row.is_tablet_b === 'yes').length;
const phytLanePhyt = phytLane.filter((row) => row.is_phyt === 'yes').length;
const sealLanePhyt = sealLane.filter((row) => row.is_phyt === 'yes').length;

const summary = {
  date: RUN_DATE,
  phase: 'EXPAND',
  candidate_id: PREFIX,
  tier: 'candidate',
  bet: 'Inside the 806-series construction, 154/155/(rare 100) and 158 are not interchangeable variants. They split by context: 154/155/100 predicts a seal/reverse/no-icon lane, while 158 predicts a TAB:B and often phytographic lane. If true, the prefix before 806 carries semantic or administrative register load.',
  counts: {
    total_prefix_806_rows: prefixRows.length,
    seal_lane_154_155_100: {
      n: sealLane.length,
      seal_rows: sealLaneSeal,
      tablet_b_rows: sealLaneTablet,
      phyt_icon_rows: sealLanePhyt,
      by_type: countBy(sealLane, 'type'),
      by_symbol: countBy(sealLane, 'symbol'),
    },
    tablet_phyt_lane_158: {
      n: phytLane.length,
      seal_rows: phytLaneSeal,
      tablet_b_rows: phytLaneTablet,
      phyt_icon_rows: phytLanePhyt,
      by_type: countBy(phytLane, 'type'),
      by_symbol: countBy(phytLane, 'symbol'),
    },
  },
  contrast_tests: {
    seal_lane_vs_158_for_seal_type: {
      table: {
        seal_lane_seal: sealLaneSeal,
        seal_lane_non_seal: sealLane.length - sealLaneSeal,
        lane158_seal: phytLaneSeal,
        lane158_non_seal: phytLane.length - phytLaneSeal,
      },
      fisher_right_tail: fisherRight(
        sealLaneSeal,
        sealLane.length - sealLaneSeal,
        phytLaneSeal,
        phytLane.length - phytLaneSeal,
      ),
    },
    lane158_vs_seal_lane_for_tab_b: {
      table: {
        lane158_tab_b: phytLaneTablet,
        lane158_non_tab_b: phytLane.length - phytLaneTablet,
        seal_lane_tab_b: sealLaneTablet,
        seal_lane_non_tab_b: sealLane.length - sealLaneTablet,
      },
      fisher_right_tail: fisherRight(
        phytLaneTablet,
        phytLane.length - phytLaneTablet,
        sealLaneTablet,
        sealLane.length - sealLaneTablet,
      ),
    },
    lane158_vs_seal_lane_for_phyt_icon: {
      table: {
        lane158_phyt: phytLanePhyt,
        lane158_non_phyt: phytLane.length - phytLanePhyt,
        seal_lane_phyt: sealLanePhyt,
        seal_lane_non_phyt: sealLane.length - sealLanePhyt,
      },
      fisher_right_tail: fisherRight(
        phytLanePhyt,
        phytLane.length - phytLanePhyt,
        sealLanePhyt,
        sealLane.length - sealLanePhyt,
      ),
    },
  },
  interpretation: 'This is a sign-function/context bet, not a sound or translation. It predicts that new source-visible 154/155/100-806 rows should mostly be seal-lane rows, while new 158-806 rows should mostly be TAB:B/phyt-lane rows.',
  demoters: [
    'If source-family collapse reduces the 158 TAB:B/Phyt side to one repeated artifact family, demote.',
    'If new 158-806 seal/reverse rows or new 154/155-806 TAB:B/phyt rows appear at comparable rates, demote.',
    'If source-token review shows the 154/158 distinction is a catalog allograph of one sign, convert the claim from semantic split to allographic/context split.',
  ],
};

if (
  summary.contrast_tests.seal_lane_vs_158_for_seal_type.fisher_right_tail <= 0.01
  && summary.contrast_tests.lane158_vs_seal_lane_for_tab_b.fisher_right_tail <= 0.01
) {
  summary.decision = 'candidate_survives_first_context_split_test';
} else {
  summary.decision = 'wild_shot_until_more_context';
}

fs.mkdirSync(OUT_DIR, { recursive: true });
writeCsv(path.join(OUT_DIR, `${PREFIX}_rows.csv`), prefixRows, [
  'id', 'cisi', 'site', 'type', 'symbol', 'text', 'prev', 'next', 'lane',
  'is_seal', 'is_tablet_b', 'is_no_icon', 'is_phyt',
]);
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
