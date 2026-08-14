import fs from 'node:fs';
import path from 'node:path';

// Does a sign mean the same thing wherever it sits, or does its position change its job?
// This script tests that on four focus signs (095, 125, 530, 705) in Indus inscriptions read
// from data/open_prototype/lipi/metadata_filtered.csv, deduplicated to unique sign sequences.
// For every 002-H-X window it records each focus sign twice over: once when it is H, the
// "head" slot right after 002, and once when it is X, the slot after the head. For each sign
// it then compares the two roles — how often the text continues afterward, and which partner
// signs it pairs with. If the same sign behaves differently by slot, that is evidence the
// script must be parsed by position, not by sign identity alone. It scores three risky bets
// and writes a per-occurrence CSV, a per-sign CSV, a bets CSV, and a summary JSON to reports/.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_role_switch_discriminator_20260531';
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
    if (focusSigns.has(head)) {
      roleRows.push({
        checked_date: checkedDate,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        shape: row.shape,
        material: row.material,
        sign: head,
        role: 'head_slot_after_002',
        partner: x,
        tail_after_partner: tail.join(' ') || '<END>',
        open_after_partner: String(tail.length > 0),
        text: row.text,
      });
    }
    if (focusSigns.has(x)) {
      roleRows.push({
        checked_date: checkedDate,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        shape: row.shape,
        material: row.material,
        sign: x,
        role: 'x_slot_after_head',
        partner: head,
        tail_after_partner: tail.join(' ') || '<END>',
        open_after_partner: String(tail.length > 0),
        text: row.text,
      });
    }
  }
}

const signRows = [...focusSigns].map((sign) => {
  const asHead = roleRows.filter((row) => row.sign === sign && row.role === 'head_slot_after_002');
  const asX = roleRows.filter((row) => row.sign === sign && row.role === 'x_slot_after_head');
  return {
    checked_date: checkedDate,
    sign,
    head_slot_rows: String(asHead.length),
    head_slot_open_after_partner: ratio(asHead.filter((row) => row.open_after_partner === 'true').length, asHead.length),
    head_slot_partners: countBy(asHead, (row) => row.partner),
    head_slot_examples: examples(asHead),
    x_slot_rows: String(asX.length),
    x_slot_open_after_partner: ratio(asX.filter((row) => row.open_after_partner === 'true').length, asX.length),
    x_slot_partners: countBy(asX, (row) => row.partner),
    x_slot_examples: examples(asX),
    asymmetry_read:
      asHead.length > 0 && asX.length > 0
        ? 'role_switch_observed'
        : asX.length > 0
          ? 'x_slot_only_in_focus'
          : 'head_slot_only_in_focus',
  };
});

const bets = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_POSITIONAL_ROLE_SWITCHING_GRAMMAR',
    tier: signRows.filter((row) => row.asymmetry_read === 'role_switch_observed').length >= 3 ? 'candidate' : 'wild_shot',
    risky_bet:
      'The translation system must parse `002-H-X` by slot role, not isolated sign identity: `095/125/705` can act as heads after `002` and as X-slot operators with different continuation behavior.',
    current_test:
      signRows
        .filter((row) => row.asymmetry_read === 'role_switch_observed')
        .map((row) => `${row.sign}:head=${row.head_slot_rows}/${row.head_slot_open_after_partner}:x=${row.x_slot_rows}/${row.x_slot_open_after_partner}`)
        .join(';'),
    destructive_prediction:
      'If future data shows focus signs behave the same in head slot and X slot, the slot-role parser collapses toward sign-value/register list behavior.',
    promotion_prediction:
      'More signs with clear head-slot versus X-slot behavior differences promote a compositional slot grammar.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_POST_HEAD_OPERATOR_TYPOLOGY',
    tier: signRows.find((row) => row.sign === '530')?.head_slot_rows === '0' ? 'wild_shot' : 'candidate_edge',
    risky_bet:
      'The construction is post-head/operator-like: the special X signs behave as suffixal or enclitic operators after a head, while signs in head slot behave like lexical/class heads.',
    current_test:
      signRows.map((row) => `${row.sign}:head_slot=${row.head_slot_rows}:x_slot=${row.x_slot_rows}`).join(';'),
    destructive_prediction:
      'A large set of pre-head or head-slot occurrences with the same operator behavior kills the post-head operator typology.',
    promotion_prediction:
      'A new focus sign appearing in both slots but changing behavior by slot promotes a head-plus-operator parse.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_705_ROLE_SWITCH_EXCEPTION',
    tier: signRows.find((row) => row.sign === '705')?.head_slot_rows !== '0' ? 'candidate_edge' : 'wild_shot',
    risky_bet:
      '`705` is not a lexical class value. As X it is terminal-default; as head it can license `590`, `127`, or `530-904` continuations.',
    current_test:
      signRows.find((row) => row.sign === '705')?.head_slot_examples ?? '',
    destructive_prediction:
      'If source-strict rows show `705` head and X uses share the same continuation distribution, the role-switch reading dies.',
    promotion_prediction:
      'More `002-705-X` head-slot rows with non-terminal partners strengthen positional role-switching.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'role_switch_discriminator',
  rows: {
    role_rows: roleRows.length,
    role_switch_signs: signRows.filter((row) => row.asymmetry_read === 'role_switch_observed').map((row) => row.sign),
  },
  bets: bets.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

writeCsv(path.join(reportsDir, `${prefix}_role_rows.csv`), roleRows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'shape',
  'material',
  'sign',
  'role',
  'partner',
  'tail_after_partner',
  'open_after_partner',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_sign_rows.csv`), signRows, [
  'checked_date',
  'sign',
  'head_slot_rows',
  'head_slot_open_after_partner',
  'head_slot_partners',
  'head_slot_examples',
  'x_slot_rows',
  'x_slot_open_after_partner',
  'x_slot_partners',
  'x_slot_examples',
  'asymmetry_read',
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
