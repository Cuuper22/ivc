// We need photographs of Harappa tablets H-2218 through H-2239, and some may
// already be sitting on public blog pages. This script checks. It downloads
// five specific pages (four rssing.com mirrors and one blogspot post), scans
// each for side labels like "h2219A" (sides A/B/C of each object), and looks
// in a window of nearby HTML for an <img> URL that contains the same label.
// Every label-plus-image hit becomes one lead row, graded "T4 image lead
// only" — good for targeting plate requests, never for reading signs. As a
// side check it counts decipherment-claim vocabulary ("rebus", "bill of
// lading", etc.) on each page, since these pages mix images with speculative
// readings we must not absorb. Writes the lead CSV and a JSON summary that
// also lists which of the 22 target objects still have no public image lead.
import fs from 'node:fs';
import https from 'node:https';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const outCsv = path.join(reportsDir, 'h2218_h2239_public_image_lead_search.csv');
const outJson = path.join(reportsDir, 'h2218_h2239_public_image_lead_search_summary.json');

const sourcePages = [
  'https://bharatkalyan1.rssing.com/chan-6237423/all_p220.html',
  'https://bharatkalyan1.rssing.com/chan-6237423/all_p276.html',
  'https://bharatkalyan1.rssing.com/chan-6237423/all_p304.html',
  'https://bharatkalyan1.rssing.com/chan-6237423/all_p305.html',
  'https://bharatkalyan97.blogspot.com/2011/12/indus-valley-mystery-and-use-of-tablets.html',
];

const targetHNumbers = Array.from({ length: 22 }, (_, i) => 2218 + i);
const targetLabels = new Set(targetHNumbers.flatMap((n) => ['A', 'B', 'C'].map((side) => `h${n}${side}`)));

function fetchText(url) {
  return new Promise((resolve, reject) => {
    https
      .get(url, { headers: { 'user-agent': 'ivc-source-lead-audit/1.0' } }, (res) => {
        let data = '';
        res.setEncoding('utf8');
        res.on('data', (chunk) => {
          data += chunk;
        });
        res.on('end', () => {
          resolve({ url, statusCode: res.statusCode, text: data });
        });
      })
      .on('error', reject);
  });
}

function toCsv(rows) {
  return `${rows
    .map((row) =>
      row
        .map((value) => {
          const text = String(value ?? '');
          return `"${text.replaceAll('"', '""')}"`;
        })
        .join(','),
    )
    .join('\n')}\n`;
}

function normalizeUrl(url) {
  if (!url) return '';
  if (url.startsWith('//')) return `https:${url}`;
  return url;
}

function stripTags(html) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;|&#160;/g, ' ')
    .replace(/&quot;/g, '"')
    .replace(/&amp;/g, '&')
    .replace(/\s+/g, ' ')
    .trim();
}

function imageUrlsFromTag(tag) {
  const urls = [];
  for (const attr of tag.matchAll(/\b(?:data-src|src)=["']([^"']+)["']/gi)) {
    urls.push(normalizeUrl(attr[1]));
  }
  return urls;
}

function findImageForLabel(html, index, label) {
  const windowStart = Math.max(0, index - 2200);
  const windowEnd = Math.min(html.length, index + 600);
  const window = html.slice(windowStart, windowEnd);
  const labelLower = label.toLowerCase();
  const imageTags = [...window.matchAll(/<img\b[^>]*>/gi)].map((match) => match[0]);
  const urls = imageTags.flatMap((tag) => imageUrlsFromTag(tag));
  const exact = urls.find((url) => url.toLowerCase().includes(`${labelLower}.`));
  if (exact) return exact;
  const loose = urls.find((url) => url.toLowerCase().includes(labelLower));
  if (loose) return loose;
  const direct = window.match(new RegExp(`(https?:)?//[^"'\\s<>]+${label}\\.jpe?g`, 'i'));
  if (direct) return normalizeUrl(direct[0]);
  return '';
}

function countMatches(text, pattern) {
  return [...text.matchAll(pattern)].length;
}

function countClaimTerms(text) {
  const patterns = {
    rebus: /\brebus\b/gi,
    decipherment_terms: /\bdecipher(?:ed|ment|ing)?\b/gi,
    bill_of_lading: /\bbill of lading\b/gi,
    supercargo: /\bsupercargo\b/gi,
    workshop_product_account: /\bworkshop product account\b/gi,
    metallurgical: /\bmetallurgical\b/gi,
  };
  return Object.fromEntries(
    Object.entries(patterns).map(([name, pattern]) => [name, countMatches(text, pattern)]),
  );
}

const pages = [];
for (const url of sourcePages) {
  try {
    pages.push(await fetchText(url));
  } catch (error) {
    pages.push({ url, statusCode: 'fetch_error', text: '', error: error.message });
  }
}

const leadRows = [];
const labelPageHits = new Map();
const pageSummaries = [];
let textOnlyTargetMentions = 0;

for (const page of pages) {
  const html = page.text ?? '';
  const foundLabels = new Set();
  const labelPattern = /\bh(22(?:1[8-9]|2[0-9]|3[0-9]))([ABC])\b/gi;
  for (const match of html.matchAll(labelPattern)) {
    const hNumber = Number.parseInt(match[1], 10);
    if (!targetHNumbers.includes(hNumber)) continue;
    const label = `h${hNumber}${match[2].toUpperCase()}`;
    if (!targetLabels.has(label)) continue;
    foundLabels.add(label);

    const imageUrl = findImageForLabel(html, match.index ?? 0, label);
    if (!imageUrl) {
      textOnlyTargetMentions++;
      continue;
    }
    const key = `${label}|${page.url}|${imageUrl}`;
    if (!labelPageHits.has(key)) {
      labelPageHits.set(key, true);
      leadRows.push({
        public_label: label,
        cisi_candidate: `H-${hNumber}`,
        side_letter: match[2].toUpperCase(),
        source_page_url: page.url,
        nearest_image_url: imageUrl,
        label_context: `${label} image URL found near ${label} side label on source page`,
        source_tier: 'T4 image lead only',
        admissible_use: 'source discovery and plate request targeting',
        non_admissible_use:
          'sign segmentation, allography, side orientation, numerical value, metrological reading, sign meaning, phonetic value, language identity, translation, or acceptance of secondary decipherment claims',
      });
    }
  }

  pageSummaries.push({
    url: page.url,
    statusCode: page.statusCode,
    bytes: html.length,
    target_label_mentions: [...foundLabels].sort(),
    claim_term_counts: countClaimTerms(html),
  });
}

leadRows.sort((a, b) =>
  a.public_label.localeCompare(b.public_label, undefined, { numeric: true }) ||
  a.source_page_url.localeCompare(b.source_page_url),
);

const uniqueLabels = [...new Set(leadRows.map((row) => row.public_label))].sort((a, b) =>
  a.localeCompare(b, undefined, { numeric: true }),
);
const uniqueObjects = [...new Set(leadRows.map((row) => row.cisi_candidate))].sort((a, b) =>
  a.localeCompare(b, undefined, { numeric: true }),
);
const missingObjects = targetHNumbers
  .map((n) => `H-${n}`)
  .filter((cisi) => !uniqueObjects.includes(cisi));

const csvRows = [
  [
    'public_label',
    'cisi_candidate',
    'side_letter',
    'source_page_url',
    'nearest_image_url',
    'label_context',
    'source_tier',
    'admissible_use',
    'non_admissible_use',
  ],
];
for (const row of leadRows) {
  csvRows.push([
    row.public_label,
    row.cisi_candidate,
    row.side_letter,
    row.source_page_url,
    row.nearest_image_url,
    row.label_context,
    row.source_tier,
    row.admissible_use,
    row.non_admissible_use,
  ]);
}

const summary = {
  source: 'H-2218 through H-2239 public image-lead search',
  checked_at: '2026-05-24',
  source_pages_checked: sourcePages.length,
  target_objects: targetHNumbers.length,
  target_labels: targetLabels.size,
  image_lead_rows: leadRows.length,
  text_only_target_mentions: textOnlyTargetMentions,
  unique_public_labels_found: uniqueLabels,
  unique_image_urls_found: [...new Set(leadRows.map((row) => row.nearest_image_url))].sort(),
  unique_cisi_candidates_found: uniqueObjects,
  missing_cisi_candidates: missingObjects,
  page_summaries: pageSummaries,
  key_observation:
    'Across the checked public RSS/blog pages, object-level A/B/C image labels were found only for H-2219. The other H-2218 through H-2239 objects still need CISI plates, higher-resolution source images, or direct archive access.',
  interpretation_boundary:
    'This is a public source-lead audit only. It accepts no sign segmentation, allography, side orientation, physical side function, numerical value, metrological reading, sign meaning, phonetic value, language identity, or translation.',
  outputs: [path.relative(base, outCsv).replaceAll('\\', '/')],
};

fs.writeFileSync(outCsv, toCsv(csvRows));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
