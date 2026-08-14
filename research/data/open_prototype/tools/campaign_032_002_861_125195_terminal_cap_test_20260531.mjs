import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

// Seal M-735 ends 002-390-125-195, and 195 appears almost nowhere else. Is 125-195 a
// reusable title sub-tail, or is 195 just a rare terminal cap — and is even that claim
// cheap? This script runs the test with its own null model. It reads data/open_prototype/
// lipi/metadata_filtered.csv (deduplicated) plus the branch-selector frames report, logs
// every 195 occurrence and every neighbor of 125, and builds a full per-sign terminality
// table. The null: among all signs with at most 2, 3, 5, or 10 occurrences, what share are
// terminal-only anyway? Rare terminal-only behavior turns out to be common, so 195's 2-for-2
// terminal record proves little. It also fingerprints the three local M-735 evidence images
// (SHA-256 plus JPEG pixel dimensions) so the visual side is auditable. Verdicts: the
// reusable sub-tail is dead for now, the terminal cap stays a wild shot, and the open 125
// branch narrows to its recurring tails (632-032, 820). Writes occurrences, the sign
// summary, the rare-terminal null, 125 frame tails, source files, and decisions as CSVs
// plus a summary JSON in reports/.

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const FRAMES = path.join(
  ROOT,
  'data',
  'open_prototype',
  'reports',
  'risky_002390_canonical_branch_selector_forger_20260531_frames.csv',
);
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'campaign_032_002_861_125195_terminal_cap_test_20260531';
const RUN_DATE = '2026-05-31';

const SOURCE_FILES = [
  {
    role: 'm735_impression_signband',
    path: 'tmp/002390x_source_normalization/M735_impression_a_signband.jpg',
  },
  {
    role: 'm735_impression_full_panel',
    path: 'tmp/002390x_source_normalization/M735_impression_a_full_panel.jpg',
  },
  {
    role: 'm735_002390125_boxed_overlay',
    path: 'tmp/002390x_token_boundary_adjudication/N002_M735_boxed.jpg',
  },
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

function csvEscape(value) {
  const text = String(value ?? '');
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(',')];
  for (const row of rows) lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function countBy(items, fn) {
  const counts = new Map();
  for (const item of items) {
    const key = fn(item);
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()].sort(
    (a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }),
  );
}

function top(counts, n = 8) {
  return counts
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function sha256(file) {
  return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex').toUpperCase();
}

function jpegDimensions(file) {
  const bytes = fs.readFileSync(file);
  let i = 2;
  while (i < bytes.length) {
    if (bytes[i] !== 0xff) {
      i += 1;
      continue;
    }
    const marker = bytes[i + 1];
    const length = bytes.readUInt16BE(i + 2);
    if (
      (marker >= 0xc0 && marker <= 0xc3) ||
      (marker >= 0xc5 && marker <= 0xc7) ||
      (marker >= 0xc9 && marker <= 0xcb) ||
      (marker >= 0xcd && marker <= 0xcf)
    ) {
      return {
        height: bytes.readUInt16BE(i + 5),
        width: bytes.readUInt16BE(i + 7),
      };
    }
    i += 2 + length;
  }
  return { width: '', height: '' };
}

fs.mkdirSync(OUT_DIR, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));
const rows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()];
const frameRows = parseCsv(fs.readFileSync(FRAMES, 'utf8'));

const occurrences = [];
const signStats = new Map();

for (const row of rows) {
  row.signs.forEach((sign, idx) => {
    if (!signStats.has(sign)) {
      signStats.set(sign, {
        sign,
        occurrences: 0,
        terminal: 0,
        predecessors: new Set(),
        successors: new Set(),
        sites: new Set(),
        types: new Set(),
        examples: [],
      });
    }
    const stat = signStats.get(sign);
    const predecessor = row.signs[idx - 1] ?? '<START>';
    const successor = row.signs[idx + 1] ?? '<END>';
    const terminal = idx === row.signs.length - 1;
    stat.occurrences += 1;
    if (terminal) stat.terminal += 1;
    stat.predecessors.add(predecessor);
    stat.successors.add(successor);
    stat.sites.add(row.site || 'NA');
    stat.types.add(row.type || 'NA');
    if (stat.examples.length < 10) stat.examples.push(`${row.object}:${row.text}`);

    if (sign === '195' || predecessor === '125' || successor === '195') {
      occurrences.push({
        checked_date: RUN_DATE,
        row_id: row.id,
        object: row.object,
        site: row.site || 'NA',
        type: row.type || 'NA',
        target_sign: sign,
        predecessor,
        successor,
        prev2: row.signs.slice(Math.max(0, idx - 2), idx).join(' ') || '<START>',
        next2: row.signs.slice(idx + 1, idx + 3).join(' ') || '<END>',
        terminal: terminal ? 'true' : 'false',
        text: row.text,
      });
    }
  });
}

const signSummary = [...signStats.values()]
  .map((stat) => ({
    checked_date: RUN_DATE,
    sign: stat.sign,
    occurrences: String(stat.occurrences),
    terminal_count: String(stat.terminal),
    terminal_share: (stat.terminal / stat.occurrences).toFixed(6),
    predecessor_count: String(stat.predecessors.size),
    successor_count: String(stat.successors.size),
    site_count: String(stat.sites.size),
    type_count: String(stat.types.size),
    predecessors: [...stat.predecessors].sort().join(';'),
    successors: [...stat.successors].sort().join(';'),
    sites: [...stat.sites].sort().join(';'),
    types: [...stat.types].sort().join(';'),
    examples: stat.examples.join(' | '),
  }))
  .sort((a, b) => Number(b.occurrences) - Number(a.occurrences) || a.sign.localeCompare(b.sign, undefined, { numeric: true }));

const rareNullRows = [2, 3, 5, 10].map((maxN) => {
  const pool = signSummary.filter((row) => Number(row.occurrences) <= maxN);
  const terminalOnly = pool.filter((row) => row.terminal_share === '1.000000');
  const crossSiteTerminalOnly = terminalOnly.filter((row) => Number(row.site_count) >= 2);
  const crossTypeTerminalOnly = terminalOnly.filter((row) => Number(row.type_count) >= 2);
  return {
    checked_date: RUN_DATE,
    max_occurrences: String(maxN),
    rare_signs: String(pool.length),
    terminal_only_rare_signs: String(terminalOnly.length),
    terminal_only_share: pool.length ? (terminalOnly.length / pool.length).toFixed(6) : '0.000000',
    cross_site_terminal_only: String(crossSiteTerminalOnly.length),
    cross_type_terminal_only: String(crossTypeTerminalOnly.length),
  };
});

const tail125Frames = frameRows.filter((row) => row.branch === '125').map((row) => ({
  checked_date: RUN_DATE,
  object: row.object,
  row_id: row.row_id,
  source_bucket: row.source_bucket,
  prev_before_002: row.prev_before_002,
  tail_after_125: row.tail,
  terminal_after_125: row.terminal,
  source_status: row.source_status,
  text: row.text,
}));

const stat195 = signSummary.find((row) => row.sign === '195');
const after125to195 = occurrences.filter((row) => row.predecessor === '125' && row.target_sign === '195');
const nonFrame125to195 = occurrences.filter(
  (row) => row.predecessor === '125' && row.target_sign === '195' && !row.text.includes('002-390-125-195'),
);
const terminalOnlyN2 = rareNullRows.find((row) => row.max_occurrences === '2');
const m735Frame = frameRows.find((row) => row.object === 'M-735' && row.branch === '125');

const fileRows = SOURCE_FILES.map((entry) => {
  const absolute = path.join(ROOT, entry.path);
  const exists = fs.existsSync(absolute);
  const dimensions = exists ? jpegDimensions(absolute) : { width: '', height: '' };
  return {
    checked_date: RUN_DATE,
    role: entry.role,
    path: entry.path,
    exists: String(exists),
    sha256: exists ? sha256(absolute) : '',
    width: String(dimensions.width),
    height: String(dimensions.height),
  };
});

const decisionRows = [
  {
    checked_date: RUN_DATE,
    named_bet: '`125-195` is a reusable `125` title sub-tail',
    tier_after_test: 'dead_for_now',
    evidence:
      '`195` appears after `125` only in M-735; there is no non-frame `125->195` recurrence and no second `125-195` frame.',
    adversary:
      'The broader `125` title-branch bet should not borrow support from `125-195`; keep support restricted to recurring tails such as `632-032` and candidate `820`.',
    falsifier_or_rescue:
      'A second independent source-bound `125-195` row, especially outside Mohenjo-daro square `SEAL:S`, revives this as a candidate sub-tail.',
  },
  {
    checked_date: RUN_DATE,
    named_bet: '`195` is a rare terminal cap that can close different heads',
    tier_after_test: 'wild_shot_retained_not_candidate',
    evidence:
      '`195` is terminal in 2/2 canonical occurrences and has two predecessors (`125`, `527`), two sites, and two object types.',
    adversary:
      `${terminalOnlyN2.terminal_only_rare_signs}/${terminalOnlyN2.rare_signs} signs with <=2 occurrences are terminal-only, so terminal-only rarity is cheap.`,
    falsifier_or_rescue:
      'A nonterminal `195` kills the cap bet; a third independent terminal `195` with a new predecessor upgrades it to candidate.',
  },
  {
    checked_date: RUN_DATE,
    named_bet: '`125` is still an open/continuing branch under `002-390`, but its tails split into subtypes',
    tier_after_test: 'candidate_narrowed',
    evidence:
      'All four `002-390-125` frames continue, but only `632-032` and `820` have tail-ecology support; `195` is a singleton cap-like exception.',
    adversary:
      'If `125` tails keep fragmenting into singleton terminal caps, the rank/title selector gloss is too broad.',
    falsifier_or_rescue:
      'Promote only if held-out or source-bound rows cluster into recurring `125` sub-tail families rather than one-off endings.',
  },
];

const summary = {
  checked_date: RUN_DATE,
  status: '125195_terminal_cap_test',
  hypothesis_tested:
    '`125-195` either rescues `125` as a broader title-tail family or forces a split where `195` is only a rare terminal cap.',
  m735_frame: m735Frame,
  sign195: stat195,
  after125to195_rows: after125to195.length,
  nonframe125to195_rows: nonFrame125to195.length,
  rare_terminal_null: rareNullRows,
  source_files: fileRows,
  decisions: decisionRows,
  confidence_after_test: {
    '125_195_reusable_subtail': 'dead_for_now',
    '195_terminal_cap': 'wild_shot_retained_not_candidate',
    '125_open_branch': 'candidate_narrowed',
  },
};

writeCsv(path.join(OUT_DIR, `${PREFIX}_195_occurrences.csv`), occurrences, [
  'checked_date',
  'row_id',
  'object',
  'site',
  'type',
  'target_sign',
  'predecessor',
  'successor',
  'prev2',
  'next2',
  'terminal',
  'text',
]);

writeCsv(path.join(OUT_DIR, `${PREFIX}_sign_terminal_summary.csv`), signSummary, [
  'checked_date',
  'sign',
  'occurrences',
  'terminal_count',
  'terminal_share',
  'predecessor_count',
  'successor_count',
  'site_count',
  'type_count',
  'predecessors',
  'successors',
  'sites',
  'types',
  'examples',
]);

writeCsv(path.join(OUT_DIR, `${PREFIX}_rare_terminal_null.csv`), rareNullRows, [
  'checked_date',
  'max_occurrences',
  'rare_signs',
  'terminal_only_rare_signs',
  'terminal_only_share',
  'cross_site_terminal_only',
  'cross_type_terminal_only',
]);

writeCsv(path.join(OUT_DIR, `${PREFIX}_125_frame_tails.csv`), tail125Frames, [
  'checked_date',
  'object',
  'row_id',
  'source_bucket',
  'prev_before_002',
  'tail_after_125',
  'terminal_after_125',
  'source_status',
  'text',
]);

writeCsv(path.join(OUT_DIR, `${PREFIX}_source_files.csv`), fileRows, [
  'checked_date',
  'role',
  'path',
  'exists',
  'sha256',
  'width',
  'height',
]);

writeCsv(path.join(OUT_DIR, `${PREFIX}_decisions.csv`), decisionRows, [
  'checked_date',
  'named_bet',
  'tier_after_test',
  'evidence',
  'adversary',
  'falsifier_or_rescue',
]);

fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
