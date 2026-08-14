// Looks at the sign right after `806` — the suffixes 465, 467, 475, and 468 — and
// asks whether they sort by context. The wild-shot bet: `806-465` and `806-475`
// go with the Phyt (plant) icon, `806-467` does not belong to that plant class,
// and `806-468` goes with aniconic (no-symbol) seals, especially SEAL:R, rather
// than being a generic no-icon marker. The script reads metadata_filtered.csv,
// collects every 806+suffix occurrence with its object metadata, collapses each
// suffix's rows to exact-text families, and tabulates Phyt and no-symbol-seal
// rates per suffix. Robustness comes from leave-one-out tables that drop each site
// and each object type in turn and report the surviving hit rates. No permutation
// null is run; the output is labeled a wild shot. Writes a bet summary
// (JSON + CSV) plus per-suffix and leave-one-out CSVs to the reports directory.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_806_suffix_context_split_20260531';
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

function writeCsv(file, rows, fields) {
  const esc = (value) => {
    const text = String(value ?? '');
    return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
  };
  const body = rows.map((row) => fields.map((field) => esc(row[field])).join(',')).join('\n');
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`);
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function norm(value, fallback = 'NA') {
  const text = String(value ?? '').trim();
  return text && text !== '-' && text !== 'None' ? text : fallback;
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const suffixes = ['465', '467', '475', '468'];

function has806Suffix(row, suffix) {
  return row.signs.some((sign, idx) => sign === '806' && row.signs[idx + 1] === suffix);
}

function isPhyt(row) {
  return norm(row.symbol) === 'Phyt';
}

function isNoSymbol(row) {
  return norm(row.symbol) === 'NA';
}

function isNoSymbolSeal(row) {
  return isNoSymbol(row) && String(row.type).startsWith('SEAL');
}

const suffixRows = [];
for (const suffix of suffixes) {
  for (const row of rows.filter((item) => has806Suffix(item, suffix))) {
    suffixRows.push({
      object: objectId(row),
      suffix,
      site: norm(row.site),
      type: norm(row.type),
      symbol: norm(row.symbol),
      cult: norm(row.cult),
      shape: norm(row.shape),
      text: row.text,
      phyt: isPhyt(row),
      no_symbol: isNoSymbol(row),
      no_symbol_seal: isNoSymbolSeal(row),
    });
  }
}

function collapseByExact(rowsIn) {
  return [...new Map(rowsIn.map((row) => [row.text, row])).values()];
}

const summary = [];
for (const suffix of suffixes) {
  const raw = suffixRows.filter((row) => row.suffix === suffix);
  const exact = collapseByExact(raw);
  summary.push({
    suffix,
    raw_rows: raw.length,
    raw_phyt: raw.filter((row) => row.phyt).length,
    exact_text_families: exact.length,
    exact_phyt: exact.filter((row) => row.phyt).length,
    raw_no_symbol: raw.filter((row) => row.no_symbol).length,
    raw_no_symbol_seal: raw.filter((row) => row.no_symbol_seal).length,
    exact_no_symbol: exact.filter((row) => row.no_symbol).length,
    exact_no_symbol_seal: exact.filter((row) => row.no_symbol_seal).length,
    sites: [...new Set(raw.map((row) => row.site))].join(';'),
    types: [...new Set(raw.map((row) => row.type))].join(';'),
    examples: raw.map((row) => `${row.object}:${row.site}:${row.type}:${row.symbol}:${row.text}`).join('|'),
  });
}

const plantSetRaw = suffixRows.filter((row) => ['465', '467', '475'].includes(row.suffix));
const plantSetExact = collapseByExact(plantSetRaw);
const suffix468Raw = suffixRows.filter((row) => row.suffix === '468');
const suffix468Exact = collapseByExact(suffix468Raw);

function leaveOut(rowsIn, key, predicate) {
  return [...new Set(rowsIn.map((row) => row[key]))].sort().map((value) => {
    const kept = rowsIn.filter((row) => row[key] !== value);
    return {
      left_out_field: key,
      left_out_value: value,
      kept_rows: kept.length,
      kept_hits: kept.filter(predicate).length,
      kept_rate: kept.length ? kept.filter(predicate).length / kept.length : '',
    };
  });
}

const leaveOutRows = [
  ...leaveOut(plantSetExact, 'site', (row) => row.phyt).map((row) => ({ bet_component: '465_467_475_exact_phyt', ...row })),
  ...leaveOut(plantSetExact, 'type', (row) => row.phyt).map((row) => ({ bet_component: '465_467_475_exact_phyt', ...row })),
  ...leaveOut(suffix468Exact, 'site', (row) => row.no_symbol_seal).map((row) => ({ bet_component: '468_exact_no_symbol_seal', ...row })),
  ...leaveOut(suffix468Exact, 'type', (row) => row.no_symbol_seal).map((row) => ({ bet_component: '468_exact_no_symbol_seal', ...row })),
];

const bet = {
  run_date: RUN_DATE,
  bet_id: 'V4_806_SUFFIX_CONTEXT_SPLIT_20260531',
  vector: 'V4 context-to-meaning',
  confidence_tier: 'wild shot',
  risky_bet: '`806-465` and `806-475` may be plant-context suffixes; `806-467` is not in that class. `806-468` may be an aniconic/SEAL:R register suffix rather than a generic no-symbol marker.',
  observed: `465/467/475 combined: ${plantSetRaw.filter((row) => row.phyt).length}/${plantSetRaw.length} Phyt raw, ${plantSetExact.filter((row) => row.phyt).length}/${plantSetExact.length} exact-text families. By suffix exact Phyt: ${summary.map((row) => `${row.suffix}=${row.exact_phyt}/${row.exact_text_families}`).join('; ')}. 468: ${suffix468Raw.filter((row) => row.no_symbol_seal).length}/${suffix468Raw.length} no-symbol seal raw, ${suffix468Exact.filter((row) => row.no_symbol_seal).length}/${suffix468Exact.length} exact-text families.`,
  adversarial_test: 'Exact-text collapse and leave-one-site/type checks. The combined plant class is poisoned by 467; the 468 no-symbol signal is partly type-driven.',
  falsifier: 'Any source-normalized expansion where 465/475 cease being plant-heavy, or where 468 fails to concentrate in aniconic SEAL:R-like contexts, kills the suffix-context bet.',
  next_prediction: '`806-465` and `806-475` should remain Phyt in new rows; `806-467` should behave separately; `806-468` should predict aniconic rectangular seal context better than generic no-symbol context.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), JSON.stringify({
  ...bet,
  summary,
  leave_one_checks: leaveOutRows,
}, null, 2));
writeCsv(path.join(OUT_DIR, `${PREFIX}.csv`), [bet], [
  'run_date',
  'bet_id',
  'vector',
  'confidence_tier',
  'risky_bet',
  'observed',
  'adversarial_test',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_suffix_summary.csv`), summary, [
  'suffix',
  'raw_rows',
  'raw_phyt',
  'exact_text_families',
  'exact_phyt',
  'raw_no_symbol',
  'raw_no_symbol_seal',
  'exact_no_symbol',
  'exact_no_symbol_seal',
  'sites',
  'types',
  'examples',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_leave_one.csv`), leaveOutRows, [
  'bet_component',
  'left_out_field',
  'left_out_value',
  'kept_rows',
  'kept_hits',
  'kept_rate',
]);
console.log(JSON.stringify(bet, null, 2));
