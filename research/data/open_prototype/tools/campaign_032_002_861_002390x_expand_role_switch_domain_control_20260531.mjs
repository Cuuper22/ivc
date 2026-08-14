import fs from 'node:fs';
import path from 'node:path';

// A control experiment for the role-switch finding. An earlier script showed that the focus
// signs 095, 125, 530, and 705 behave differently in the head slot (right after 002) than in
// the X slot (right after the head). But that could be an artifact of object type: maybe seals
// use one pattern and tablets another, and the "role switch" is really a domain switch.
// So this script reads the same inscriptions from data/open_prototype/lipi/metadata_filtered.csv,
// buckets each occurrence by domain (seal, tablet, pot, tag, or the raw type), and re-runs the
// head-versus-X comparison inside each domain separately. If the asymmetry still shows up
// within a single domain — especially seals, the largest one — it cannot be blamed on object
// type. It scores two bets on the seal-domain results for signs 125 and 705, and writes an
// occurrence CSV, a per-sign-per-domain CSV, a bets CSV, and a summary JSON to reports/.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_role_switch_domain_control_20260531';
const checkedDate = '2026-05-31';
const focusSigns = new Set(['095', '125', '530', '705']);

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

function signs(text) {
  return [...String(text || '').matchAll(/\d{3}/g)].map((match) => match[0]);
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function domain(row) {
  if (String(row.type).startsWith('SEAL')) return 'seal';
  if (String(row.type).startsWith('TAB')) return 'tablet';
  if (String(row.type).startsWith('POT')) return 'pot';
  if (String(row.type).startsWith('TAG')) return 'tag';
  return row.type || '-';
}

function ratio(numerator, denominator) {
  return denominator ? `${numerator}/${denominator}` : '0/0';
}

function countBy(items, keyFn) {
  const counts = new Map();
  for (const item of items) {
    const key = keyFn(item) || '-';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }))
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function uniqueRowsByText(rows) {
  return [...new Map(rows.map((row) => [row.tokens.join(' '), row])).values()];
}

function examples(rows, n = 6) {
  return rows
    .slice(0, n)
    .map((row) => `${row.object}:${row.text}`)
    .join(' | ');
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = uniqueRowsByText(
  parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
    ...row,
    object: objectId(row),
    tokens: signs(row.text),
  })),
);

const roleRows = [];
for (const row of rows) {
  for (let i = 0; i < row.tokens.length - 2; i += 1) {
    if (row.tokens[i] !== '002') continue;
    const head = row.tokens[i + 1];
    const x = row.tokens[i + 2];
    const tail = row.tokens.slice(i + 3);
    for (const [sign, role, partner] of [
      [head, 'head_slot_after_002', x],
      [x, 'x_slot_after_head', head],
    ]) {
      if (!focusSigns.has(sign)) continue;
      roleRows.push({
        checked_date: checkedDate,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        domain: domain(row),
        shape: row.shape,
        material: row.material,
        sign,
        role,
        partner,
        tail_after_partner: tail.join(' ') || '<END>',
        open_after_partner: String(tail.length > 0),
        text: row.text,
      });
    }
  }
}

const domains = [...new Set(roleRows.map((row) => row.domain))];
const domainRows = [];
for (const sign of focusSigns) {
  for (const rowDomain of domains) {
    const headRows = roleRows.filter((row) => row.sign === sign && row.domain === rowDomain && row.role === 'head_slot_after_002');
    const xRows = roleRows.filter((row) => row.sign === sign && row.domain === rowDomain && row.role === 'x_slot_after_head');
    if (!headRows.length && !xRows.length) continue;
    const headOpen = headRows.filter((row) => row.open_after_partner === 'true').length;
    const xOpen = xRows.filter((row) => row.open_after_partner === 'true').length;
    domainRows.push({
      checked_date: checkedDate,
      sign,
      domain: rowDomain,
      head_rows: String(headRows.length),
      head_open: ratio(headOpen, headRows.length),
      head_sites: countBy(headRows, (row) => row.site),
      head_examples: examples(headRows),
      x_rows: String(xRows.length),
      x_open: ratio(xOpen, xRows.length),
      x_sites: countBy(xRows, (row) => row.site),
      x_examples: examples(xRows),
      same_domain_asymmetry:
        headRows.length > 0 && xRows.length > 0 && (headOpen / headRows.length || 0) !== (xOpen / xRows.length || 0)
          ? 'asymmetry_present'
          : 'not_testable_or_no_asymmetry',
    });
  }
}

const seal125 = domainRows.find((row) => row.sign === '125' && row.domain === 'seal');
const seal705 = domainRows.find((row) => row.sign === '705' && row.domain === 'seal');

const bets = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_125_ROLE_SWITCH_SURVIVES_SEAL_CONTROL',
    tier: seal125?.same_domain_asymmetry === 'asymmetry_present' ? 'candidate' : 'wild_shot',
    risky_bet:
      '`125` role-switching is not just register noise: inside seal contexts, `125` as head closes, while `125` as X usually opens.',
    current_test:
      seal125 ? `seal head=${seal125.head_rows}/${seal125.head_open}; seal X=${seal125.x_rows}/${seal125.x_open}` : 'no seal control',
    destructive_prediction:
      'More same-domain head-slot `125` rows that open like X-slot `125`, or X-slot rows that close like head-slot `125`, demote slot-role grammar.',
    promotion_prediction:
      'More seal rows preserving head-close versus X-open asymmetry promote positional grammar over register formula.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_705_ROLE_SWITCH_PARTLY_DOMAIN_SENSITIVE',
    tier: seal705?.same_domain_asymmetry === 'asymmetry_present' ? 'candidate_edge' : 'wild_shot',
    risky_bet:
      '`705` role-switching may be domain-sensitive: seal head-slot `705` has routed partners, while X-slot `705` is terminal-default.',
    current_test:
      seal705 ? `seal head=${seal705.head_rows}/${seal705.head_open}; seal X=${seal705.x_rows}/${seal705.x_open}` : 'no seal control',
    destructive_prediction:
      'If seal-only `705` head and X rows converge in continuation behavior, the role-switch exception becomes source/register noise.',
    promotion_prediction:
      'A second seal-domain `002-705-530-Y` or `002-705-590` style row promotes head-slot 705 as routing head.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'role_switch_domain_control',
  rows: {
    role_rows: roleRows.length,
    domain_rows: domainRows.length,
    same_domain_asymmetries: domainRows
      .filter((row) => row.same_domain_asymmetry === 'asymmetry_present')
      .map((row) => `${row.sign}:${row.domain}`),
  },
  bets: bets.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

writeCsv(path.join(reportsDir, `${prefix}_role_rows.csv`), roleRows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'domain',
  'shape',
  'material',
  'sign',
  'role',
  'partner',
  'tail_after_partner',
  'open_after_partner',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_domain_rows.csv`), domainRows, [
  'checked_date',
  'sign',
  'domain',
  'head_rows',
  'head_open',
  'head_sites',
  'head_examples',
  'x_rows',
  'x_open',
  'x_sites',
  'x_examples',
  'same_domain_asymmetry',
]);

writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), bets, [
  'checked_date',
  'bet_id',
  'tier',
  'risky_bet',
  'current_test',
  'destructive_prediction',
  'promotion_prediction',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
