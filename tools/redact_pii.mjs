#!/usr/bin/env node
// tools/redact_pii.mjs
// =================================================================
// Remove third-party PII (personally identifiable information — here, contact
// email addresses and private Gmail thread/message IDs) from the workspace
// before publishing. It does not care about repo structure: it scans every
// text file in the repo, skipping only .git, _git_history, and node_modules.
//
//   node tools/redact_pii.mjs            # DRY RUN: report only, writes nothing
//   node tools/redact_pii.mjs --apply    # apply edits in place
//
// How emails are handled: known research contacts get role placeholders, so the
// text still says who was contacted without exposing the address. ANY other
// address (except the maintainer's own) becomes [redacted-email] by default.
// Scholars' names stay intact — that is normal citation; only addresses and
// mailbox IDs are removed.
//
// NOTE: this repo's git history was already scrubbed with git-filter-repo using
// the same rules. This tool exists to keep the working tree clean as new files
// are added.

import fs from 'node:fs';
import path from 'node:path';

const APPLY = process.argv.includes('--apply');
const ROOT = path.resolve('.');
const EXTS = new Set(['.md', '.json', '.jsonl', '.txt', '.csv', '.html', '.xml', '.mjs', '.js', '.ts', '.vue', '.py', '.log', '.toml']);
const SKIP_DIRS = new Set(['.git', '_git_history', 'node_modules']);

const EMAIL_MAP = {
  'harappa@gmail.com':                     '[harappa-project-email]',
  'tiedekirja@tsv.fi':                     '[tiedekirja-bookseller-email]',
  'yajnadevam@proton.me':                  '[yajnadevam-email]',
  'mvbhaskar@mac.com':                     '[bhaskar-email]',
  'andreas.fuls@tu-berlin.de':             '[fuls-email]',
  'revesz@cse.unl.edu':                    '[revesz-email]',
  'mike@mayig.net':                        '[mayig-email]',
  'carl@media.org':                        '[archive-uploader-email]',
  'rmrl@rmrl.in':                          '[rmrl-email]',
};
const KEEP = new Set(['cuuper225@gmail.com']); // The maintainer's own address is never redacted. The GitHub noreply identity is also kept — it is allow-listed below, so the generic email redaction never touches it.
const GENERIC_EMAIL = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g;
const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
// Gmail message/thread IDs are 16-char hex strings; ones from the 2026 epoch start with "19e".
// The pattern uses lookarounds instead of \b so hex glued to '_' is ignored — it must never
// match data IDs like tok_19b6...
const MSGID = /(?<![0-9a-f])19e[0-9a-f]{13}(?![0-9a-f])/g;

function walk(dir) {
  const out = [];
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.isDirectory()) { if (!SKIP_DIRS.has(e.name)) out.push(...walk(path.join(dir, e.name))); }
    else if (EXTS.has(path.extname(e.name).toLowerCase())) out.push(path.join(dir, e.name));
  }
  return out;
}

let totFiles = 0, totEmail = 0, totMsgid = 0;
const genericEmails = new Set();
KEEP.add('Cuuper22@users.noreply.github.com'); // Keep the maintainer's GitHub identity wherever it appears in content.

for (const fp of walk(ROOT)) {
  let txt; try { txt = fs.readFileSync(fp, 'utf8'); } catch { continue; }
  const before = txt;
  let nEmail = 0, nMsgid = 0;
  for (const [email, repl] of Object.entries(EMAIL_MAP)) {
    const re = new RegExp(esc(email), 'g'); const m = txt.match(re);
    if (m) { nEmail += m.length; txt = txt.replace(re, repl); }
  }
  txt = txt.replace(GENERIC_EMAIL, addr => {
    if ([...KEEP].some(k => addr.includes(k)) || addr === 'cuuper225@gmail.com') return addr;
    nEmail++; genericEmails.add(addr); return '[redacted-email]';
  });
  txt = txt.replace(MSGID, () => { nMsgid++; return '[redacted-msgid]'; });
  if (txt !== before) {
    totFiles++; totEmail += nEmail; totMsgid += nMsgid;
    console.log(`${path.relative(ROOT, fp).replace(/\\/g, '/').padEnd(72)} email:${nEmail} msgid:${nMsgid}`);
    if (APPLY) fs.writeFileSync(fp, txt);
  }
}
console.log(`\n${APPLY ? 'APPLIED' : 'DRY RUN'} — ${totFiles} files, ${totEmail} email redactions, ${totMsgid} msgid redactions`);
if (genericEmails.size) { console.log('Generic-redacted addresses:'); for (const a of [...genericEmails].sort()) console.log('  ' + a); }
if (!APPLY) console.log('\n(no files written — re-run with --apply)');
