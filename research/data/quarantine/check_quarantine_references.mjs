import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const manifestPath = path.join(root, 'data/quarantine/botched_successor_after_20260531T0104_manifest.csv');
const claimLedgerPath = path.join(root, 'data/claim_ledger/claims.json');

function parseCsvLine(line) {
  const out = [];
  let cur = '';
  let quoted = false;
  for (let i = 0; i < line.length; i += 1) {
    const ch = line[i];
    if (ch === '"') {
      if (quoted && line[i + 1] === '"') {
        cur += '"';
        i += 1;
      } else {
        quoted = !quoted;
      }
    } else if (ch === ',' && !quoted) {
      out.push(cur);
      cur = '';
    } else {
      cur += ch;
    }
  }
  out.push(cur);
  return out;
}

function readManifest() {
  const lines = fs.readFileSync(manifestPath, 'utf8').trim().split(/\r?\n/);
  const header = parseCsvLine(lines.shift());
  return lines.map((line) => Object.fromEntries(parseCsvLine(line).map((value, i) => [header[i], value])));
}

function collectStrings(value, out = []) {
  if (typeof value === 'string') out.push(value.replaceAll('\\', '/'));
  else if (Array.isArray(value)) value.forEach((item) => collectStrings(item, out));
  else if (value && typeof value === 'object') Object.values(value).forEach((item) => collectStrings(item, out));
  return out;
}

const manifest = readManifest();
const contaminated = new Set(manifest.map((row) => row.path.replaceAll('\\', '/')));
const ledger = JSON.parse(fs.readFileSync(claimLedgerPath, 'utf8'));
const accepted = Array.isArray(ledger.accepted_claims) ? ledger.accepted_claims : [];
const hits = [];

for (const claim of accepted) {
  const claimId = claim.claim_id || claim.id || '(missing id)';
  for (const text of collectStrings(claim)) {
    for (const contaminatedPath of contaminated) {
      if (text.includes(contaminatedPath)) {
        hits.push({ claim_id: claimId, contaminated_path: contaminatedPath });
      }
    }
  }
}

if (hits.length) {
  console.error(JSON.stringify({ ok: false, hits }, null, 2));
  process.exit(1);
}

console.log(JSON.stringify({
  ok: true,
  accepted_claims_checked: accepted.length,
  contaminated_paths: contaminated.size,
  message: 'No accepted claim currently cites a quarantined post-cutoff artifact.'
}, null, 2));
