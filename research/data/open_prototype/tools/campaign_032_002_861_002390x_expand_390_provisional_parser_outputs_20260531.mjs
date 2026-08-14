import fs from 'node:fs';
import path from 'node:path';

// This script runs the provisional 390 parser over the corpus and writes out
// what it would actually say for each inscription. For every 002-390-X frame
// in lipi/metadata_filtered.csv it emits a structural parse string — 002 as
// frame, 390 as status/title head, then X-specific handling: 095 and terminal
// 705 close as classifiers, 125 opens a linker-complement, 530 is an
// underpowered open linker, 590 a mixed tail, 692 a global edge close, and
// anything else an underpowered residue. Each parse carries a provisional
// gloss, an honesty tier (candidate versus wild shot), and a named
// "next_break" — the specific evidence that would break that lane. These are
// parser outputs for inspection, not accepted translations. Writes per-row
// parses and lane rollups as CSVs plus a summary JSON to
// data/open_prototype/reports.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_390_provisional_parser_outputs_20260531';
const checkedDate = '2026-05-31';

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

function classifyX(x, tail) {
  if (x === '095') {
    return {
      lane: 'terminal_classifier',
      parse: 'FRAME(002) STATUS_HEAD(390) CLASSIFIER_095 CLOSE',
      gloss: 'status/title closed by class-095',
      tier: 'wild shot',
      next_break: 'source image must preserve terminal 095',
    };
  }
  if (x === '705') {
    return {
      lane: tail === '<END>' ? 'terminal_classifier' : 'classifier_to_linker_exception',
      parse:
        tail === '<END>'
          ? 'FRAME(002) STATUS_HEAD(390) CLASSIFIER_705 CLOSE'
          : `FRAME(002) STATUS_HEAD(390) CLASSIFIER_705 TAIL(${tail})`,
      gloss:
        tail === '<END>'
          ? 'status/title closed by class-705'
          : 'status/title class-705 linked to following complement',
      tier: 'wild shot',
      next_break: 'source image must preserve 705 terminality or explain 705-tail exception',
    };
  }
  if (x === '125') {
    return {
      lane: 'linker_complement',
      parse: `FRAME(002) STATUS_HEAD(390) LINKER_125 COMPLEMENT(${tail})`,
      gloss: `status/title linked to complement ${tail}`,
      tier: 'candidate',
      next_break: '125 complement lane must survive source/site collapse',
    };
  }
  if (x === '530') {
    return {
      lane: 'open_linker_underpowered',
      parse: `FRAME(002) STATUS_HEAD(390) OPEN_530 TAIL(${tail})`,
      gloss: `status/title with unresolved open tail ${tail}`,
      tier: 'wild shot',
      next_break: 'more 530 rows must repeat a complement',
    };
  }
  if (x === '590') {
    return {
      lane: 'mixed_open_tail',
      parse: `FRAME(002) STATUS_HEAD(390) MIXED_590 TAIL(${tail})`,
      gloss: `status/title with mixed tail ${tail}`,
      tier: 'wild shot',
      next_break: '590 must choose terminal or linker behavior under controls',
    };
  }
  if (x === '692') {
    return {
      lane: 'global_edge_close',
      parse: 'FRAME(002) STATUS_HEAD(390) EDGE_692 CLOSE',
      gloss: 'status/title closed by global edge sign 692',
      tier: 'wild shot',
      next_break: 'source controls must show this is not generic edge transfer',
    };
  }
  return {
    lane: 'terminal_or_underpowered_classifier',
    parse: `FRAME(002) STATUS_HEAD(390) CLASSIFIER_OR_RESIDUE_${x} ${tail === '<END>' ? 'CLOSE' : `TAIL(${tail})`}`,
    gloss:
      tail === '<END>'
        ? `status/title closed by underpowered class-${x}`
        : `status/title with underpowered class-${x} and tail ${tail}`,
    tier: 'wild shot',
    next_break: 'needs repetition/source evidence before use',
  };
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));

const parseRows = [];
for (const row of rows) {
  for (let i = 0; i < row.signs.length - 2; i += 1) {
    if (row.signs[i] !== '002' || row.signs[i + 1] !== '390') continue;
    const x = row.signs[i + 2];
    const prefixSigns = row.signs.slice(0, i).join('-') || '<NONE>';
    const tail = row.signs.slice(i + 3).join('-') || '<END>';
    const classified = classifyX(x, tail);
    parseRows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      condition: row.condition,
      complete: row.complete,
      prefix_signs: prefixSigns,
      frame: '002',
      head: '390',
      x,
      tail,
      lane: classified.lane,
      parse: classified.parse,
      provisional_gloss: classified.gloss,
      tier: classified.tier,
      next_break: classified.next_break,
      text: row.text,
    });
  }
}

const laneRows = [...new Set(parseRows.map((row) => row.lane))]
  .map((lane) => {
    const members = parseRows.filter((row) => row.lane === lane);
    return {
      checked_date: checkedDate,
      lane,
      occurrences: members.length,
      objects: members.map((row) => row.object).join(';'),
      x_values: [...new Set(members.map((row) => row.x))].join(';'),
      tiers: [...new Set(members.map((row) => row.tier))].join(';'),
      gloss_pattern: members[0]?.provisional_gloss ?? '',
    };
  })
  .sort((a, b) => Number(b.occurrences) - Number(a.occurrences) || a.lane.localeCompare(b.lane));

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: '390_provisional_parser_outputs',
  parsed_rows: parseRows.length,
  lanes: Object.fromEntries(
    laneRows.map((row) => [
      row.lane,
      {
        occurrences: Number(row.occurrences),
        x_values: row.x_values,
        tier: row.tiers,
      },
    ]),
  ),
  translation_system_rule:
    'For 002-390-X, parse 002 as frame, 390 as status/title head, X as closure classifier or linker-complement operator.',
};

writeCsv(path.join(reportsDir, `${prefix}_parse_rows.csv`), parseRows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'condition',
  'complete',
  'prefix_signs',
  'frame',
  'head',
  'x',
  'tail',
  'lane',
  'parse',
  'provisional_gloss',
  'tier',
  'next_break',
  'text',
]);
writeCsv(path.join(reportsDir, `${prefix}_lane_rows.csv`), laneRows, [
  'checked_date',
  'lane',
  'occurrences',
  'objects',
  'x_values',
  'tiers',
  'gloss_pattern',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
