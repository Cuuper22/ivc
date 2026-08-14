// Evidence-recording script for one object: seal H-773, whose frame reads 002-390-530-741.
// The bet under stress is that sign 530 is an open, continuing branch — the inscription goes
// on after it — rather than a terminal selector. Unlike the other campaign scripts, this one
// does not mine the corpus; it pins down the physical evidence for a visual check already
// made. It loads the H-773/530 frame row from the earlier branch-selector forger report
// (risky_002390_canonical_branch_selector_forger_20260531_frames.csv), fingerprints the two
// source photographs (SHA-256 hash plus JPEG pixel dimensions read from the file headers) so
// the exact images the judgment rests on are on record, and writes the fixed decision: H-773
// upgrades to "panel-continuation-visible" pressure but not strict token evidence. Outputs a
// file-check CSV, a decision CSV, and a JSON summary in data/open_prototype/reports.
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const frameCsv = path.join(reportsDir, 'risky_002390_canonical_branch_selector_forger_20260531_frames.csv');
const prefix = 'campaign_032_002_861_h773_530_panel_continuation_stress_20260531';

const sourceFiles = [
  {
    role: 'source_signband_crop',
    path: 'tmp/source_route_recheck_20260531/cisi_pakistan_n358_h773_A_signband_tight_w2400.jpg',
  },
  {
    role: 'token_overlay',
    path: 'tmp/source_route_recheck_20260531/cisi_pakistan_n358_h773_A_token_box_overlay_caption_w2400.jpg',
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

fs.mkdirSync(reportsDir, { recursive: true });

const frameRows = parseCsv(fs.readFileSync(frameCsv, 'utf8'));
const h773 = frameRows.find((row) => row.object === 'H-773' && row.branch === '530');
if (!h773) throw new Error('H-773 530 frame missing from canonical branch selector frames.');

const fileRows = sourceFiles.map((entry) => {
  const absolute = path.join(root, entry.path);
  const dimensions = jpegDimensions(absolute);
  return {
    checked_date: '2026-05-31',
    role: entry.role,
    path: entry.path,
    exists: String(fs.existsSync(absolute)),
    sha256: sha256(absolute),
    width: String(dimensions.width),
    height: String(dimensions.height),
  };
});

const decisionRows = [
  {
    checked_date: '2026-05-31',
    target: 'H-773 / 002-390-530-741',
    named_bet: '`530` is an open/continuing branch under `002-390`, not a terminal selector',
    source_state_before: h773.source_status,
    visual_stress_observation:
      'Under local R/L policy, the visible physical material left of the boxed 390 position corresponds to local 530 then 741; this supports continuation polarity after 390.',
    confidence_effect:
      'upgrade H-773 from generic route pressure to panel-continuation-visible pressure for branch polarity, but not to strict token identity',
    still_not_earned:
      'independent proof that the two left-side units are exactly 530 and 741; exact token boundaries; sign value; phonetics; translation',
    falsifier:
      'a cleaner target-side image showing no separable post-390 material, a side-A/side-B swap, or an independent sign list contradicting 530-741',
  },
];

const summary = {
  checked_date: '2026-05-31',
  status: 'h773_530_panel_continuation_stress',
  hypothesis_tested: '`530` is an open/continuing branch in the `002-390-X` branch table.',
  h773_frame: h773,
  file_checks: fileRows,
  decision:
    'H-773 gains source-panel pressure for the continuation polarity of `530`, because visible source material exists after the 390 position under local R/L order. It remains below strict token evidence because `530`/`741` identities and boundaries are still catalog-mediated.',
  confidence_after_test: {
    '530_open_continue': 'candidate_with_panel_continuation_visible_pressure',
    'H773_strict_token_witness': 'not_earned',
    '002390_branch_table': 'candidate_unchanged_but_source_polarity_strengthened',
  },
};

writeCsv(path.join(reportsDir, `${prefix}_files.csv`), fileRows, [
  'checked_date',
  'role',
  'path',
  'exists',
  'sha256',
  'width',
  'height',
]);

writeCsv(path.join(reportsDir, `${prefix}_decision.csv`), decisionRows, [
  'checked_date',
  'target',
  'named_bet',
  'source_state_before',
  'visual_stress_observation',
  'confidence_effect',
  'still_not_earned',
  'falsifier',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
