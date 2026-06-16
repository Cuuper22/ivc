#!/usr/bin/env node
// tools/redact_pii.mjs
// =================================================================
// Redact third-party PII (contact email addresses + private Gmail thread/message
// IDs) from the workspace before publishing. Structure-agnostic: scans the whole
// repo (skipping .git, _git_history, node_modules).
//
//   node tools/redact_pii.mjs            # DRY RUN: report only, writes nothing
//   node tools/redact_pii.mjs --apply    # apply edits in place
//
// Emails: known research contacts get role placeholders; ANY other address (except
// the maintainer's own) is redacted by default to [redacted-email]. Scholars' names
// are left intact (normal citation); only addresses + mailbox IDs are removed.
//
// NOTE: this repo's git history was scrubbed with git-filter-repo using the same
// rules; this tool keeps the working tree clean for future additions.

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
const KEEP = new Set(['cuuper225@gmail.com']); // maintainer's own; GitHub noreply also kept (no '@' literal redaction below touches it because it's allow-listed here)
const GENERIC_EMAIL = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g;
const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
// Gmail message/thread IDs: 16-char hex, 2026-epoch prefix "19e"; lookarounds (not \b)
// so it ignores hex glued to '_' and never matches data IDs like tok_19b6...
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
KEEP.add('Cuuper22@users.noreply.github.com'); // keep maintainer GitHub identity if present in content

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
