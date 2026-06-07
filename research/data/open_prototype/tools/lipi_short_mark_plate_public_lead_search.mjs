import fs from 'node:fs';
import http from 'node:http';
import https from 'node:https';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');

const packetCsv = path.join(reportsDir, 'lipi_short_mark_plate_request_packet.csv');
const outLeadsCsv = path.join(reportsDir, 'lipi_short_mark_plate_public_leads.csv');
const outPagesCsv = path.join(reportsDir, 'lipi_short_mark_plate_public_lead_pages.csv');
const outJson = path.join(reportsDir, 'lipi_short_mark_plate_public_lead_summary.json');

const checkedAt = '2026-05-24';

const fixedSourcePages = [
  {
    url: 'https://indusscriptmore.blogspot.com/2012/',
    source_channel: 'public_secondary_text',
    source_tier: 'T4 secondary concordance-style mention',
  },
  {
    url: 'https://www.nature.com/articles/s41599-021-00713-0',
    source_channel: 'published_secondary_direction_note',
    source_tier: 'T2 published allograph/direction lead',
  },
  {
    url: 'https://bharatkalyan97.blogspot.com/2025/08/shapes-of-tablets-convey-information.html',
    source_channel: 'claim_heavy_public_image_post',
    source_tier: 'T4 secondary image lead only',
  },
];

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;

  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];
    const next = text[i + 1];

    if (char === '"' && inQuotes && next === '"') {
      field += '"';
      i += 1;
    } else if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === ',' && !inQuotes) {
      row.push(field);
      field = '';
    } else if ((char === '\n' || char === '\r') && !inQuotes) {
      if (char === '\r' && next === '\n') i += 1;
      row.push(field);
      if (row.some((value) => value !== '')) rows.push(row);
      row = [];
      field = '';
    } else {
      field += char;
    }
  }

  if (field !== '' || row.length > 0) {
    row.push(field);
    if (row.some((value) => value !== '')) rows.push(row);
  }

  const [header, ...records] = rows;
  return records.map((record) =>
    Object.fromEntries(header.map((name, index) => [name, record[index] ?? ''])),
  );
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

function asciiClean(value) {
  return String(value ?? '')
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^\x09\x0A\x0D\x20-\x7E]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function decodeEntities(text) {
  return String(text ?? '')
    .replace(/&#x([0-9a-f]+);/gi, (_, hex) => String.fromCodePoint(Number.parseInt(hex, 16)))
    .replace(/&#([0-9]+);/g, (_, number) => String.fromCodePoint(Number.parseInt(number, 10)))
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'")
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&');
}

function stripTags(html) {
  return decodeEntities(html)
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function normalizeUrl(url) {
  if (!url) return '';
  if (url.startsWith('//')) return `https:${url}`;
  return url;
}

function isLikelyImageUrl(url) {
  return /\.(?:jpe?g|png|gif|webp)(?:[?#].*)?$/i.test(url) || /googleusercontent\.com\/img\//i.test(url);
}

function fetchText(url, redirects = 5) {
  return new Promise((resolve) => {
    const parsed = new URL(url);
    const client = parsed.protocol === 'http:' ? http : https;
    const request = client.get(
      url,
      { headers: { 'user-agent': 'ivc-source-lead-audit/1.0' } },
      (res) => {
        const location = res.headers.location ? new URL(res.headers.location, url).toString() : '';
        if ([301, 302, 303, 307, 308].includes(res.statusCode) && location && redirects > 0) {
          res.resume();
          fetchText(location, redirects - 1).then(resolve);
          return;
        }

        let data = '';
        res.setEncoding('utf8');
        res.on('data', (chunk) => {
          data += chunk;
        });
        res.on('end', () => {
          resolve({ url, finalUrl: url, statusCode: res.statusCode, text: data });
        });
      },
    );
    request.on('error', (error) => {
      resolve({ url, finalUrl: url, statusCode: 'fetch_error', text: '', error: error.message });
    });
    request.setTimeout(25000, () => {
      request.destroy(new Error('fetch_timeout'));
    });
  });
}

function getAttr(tag, attr) {
  const pattern = new RegExp(`\\b${attr}=["']([^"']+)["']`, 'i');
  return decodeEntities(tag.match(pattern)?.[1] ?? '');
}

function extractImages(html) {
  const decoded = decodeEntities(html);
  const images = [];
  for (const match of decoded.matchAll(/<img\b[^>]*>/gi)) {
    const tag = match[0];
    const index = match.index ?? 0;
    const lookback = decoded.slice(Math.max(0, index - 500), index);
    const hrefMatches = [...lookback.matchAll(/<a\b[^>]*\bhref=["']([^"']+)["'][^>]*>/gi)];
    const nearestHref = decodeEntities(hrefMatches.at(-1)?.[1] ?? '');
    const src = getAttr(tag, 'src');
    const dataSrc = getAttr(tag, 'data-src');
    const url = normalizeUrl(isLikelyImageUrl(nearestHref) ? nearestHref : dataSrc || src);
    const thumbnailUrl = normalizeUrl(dataSrc || src);
    if (!url && !thumbnailUrl) continue;
    if (/blogger\.com\/null|mail\.google\.com|^data:/i.test(url)) continue;
    images.push({
      url: url || thumbnailUrl,
      thumbnailUrl,
      width: getAttr(tag, 'data-original-width') || getAttr(tag, 'width'),
      height: getAttr(tag, 'data-original-height') || getAttr(tag, 'height'),
      alt: asciiClean(getAttr(tag, 'alt')),
    });
  }
  return images;
}

function artifactMentionInfo(text, cisi) {
  const plain = asciiClean(stripTags(text));
  const targetNumber = Number.parseInt(cisi.replace(/\D/g, ''), 10);
  const exactPattern = new RegExp(`\\bH\\s*-?\\s*${targetNumber}\\b`, 'i');
  const exactMatch = exactPattern.exec(plain);
  if (exactMatch) return { kind: 'exact', index: exactMatch.index, plain };

  for (const match of plain.matchAll(/\bH\s*-?\s*(\d{1,4})\s*-\s*(\d{1,4})\b/gi)) {
    const start = Number.parseInt(match[1], 10);
    const end = Number.parseInt(match[2], 10);
    const plausibleCatalogRange =
      match[1].length === match[2].length && Number.isFinite(start) && Number.isFinite(end) && end - start <= 100;
    if (plausibleCatalogRange && start <= targetNumber && targetNumber <= end) {
      return { kind: 'range', index: match.index ?? 0, plain };
    }
  }

  for (const match of plain.matchAll(
    /\bH\s*-?\s*\d{1,4}(?:(?:\s*,\s*|\s+and\s+)(?:H\s*-?\s*)?\d{1,4}(?:\s*-\s*\d{1,4})?)+/gi,
  )) {
    const segment = match[0];
    const segmentIndex = match.index ?? 0;
    const barePattern = new RegExp(`\\b${targetNumber}\\b`);
    const bareMatch = barePattern.exec(segment);
    if (bareMatch) return { kind: 'elided_h_list', index: segmentIndex + bareMatch.index, plain };
  }

  return { kind: '', index: -1, plain };
}

function contextAroundArtifact(text, cisi) {
  const mention = artifactMentionInfo(text, cisi);
  if (mention.index === -1) return '';
  const start = Math.max(0, mention.index - 120);
  const end = Math.min(mention.plain.length, mention.index + cisi.length + 160);
  return mention.plain.slice(start, end).trim();
}

function countMatches(text, pattern) {
  return [...String(text ?? '').matchAll(pattern)].length;
}

function countClaimTerms(text) {
  const stripped = stripTags(text);
  return {
    rebus: countMatches(stripped, /\brebus\b/gi),
    decipherment_terms: countMatches(stripped, /\bdecipher(?:ed|ment|ing)?\b/gi),
    bill_of_lading: countMatches(stripped, /\bbill of lading\b/gi),
    supercargo: countMatches(stripped, /\bsupercargo\b/gi),
    trade_account: countMatches(stripped, /\btrade account\b/gi),
    metrological: countMatches(stripped, /\bmetrolog(?:y|ical)\b/gi),
  };
}

function pageHasTarget(text, cisi) {
  return artifactMentionInfo(text, cisi).index !== -1;
}

function extractAtomEntries(xml) {
  const entries = [];
  for (const match of String(xml ?? '').matchAll(/<entry>([\s\S]*?)<\/entry>/gi)) {
    const entry = match[1];
    const title = decodeEntities(entry.match(/<title\b[^>]*>([\s\S]*?)<\/title>/i)?.[1] ?? '');
    const published = decodeEntities(entry.match(/<published\b[^>]*>([\s\S]*?)<\/published>/i)?.[1] ?? '');
    const updated = decodeEntities(entry.match(/<updated\b[^>]*>([\s\S]*?)<\/updated>/i)?.[1] ?? '');
    const content = decodeEntities(entry.match(/<content\b[^>]*>([\s\S]*?)<\/content>/i)?.[1] ?? '');
    const alternateLink =
      entry.match(/<link\b[^>]*rel=['"]alternate['"][^>]*href=['"]([^'"]+)['"][^>]*>/i)?.[1] ??
      entry.match(/<link\b[^>]*href=['"]([^'"]+)['"][^>]*rel=['"]alternate['"][^>]*>/i)?.[1] ??
      '';
    entries.push({
      title: asciiClean(title),
      published: asciiClean(published || updated),
      url: decodeEntities(alternateLink),
      content,
    });
  }
  return entries;
}

function leadKindForFixedPage(page, cisi, source) {
  if (source.url.includes('nature.com') && /H-1302|H-1303/i.test(cisi)) {
    return 'published_direction_or_corpus_note';
  }
  const images = extractImages(page.text);
  const context = contextAroundArtifact(page.text, cisi);
  const exactImage = images.find((image) => image.url.toLowerCase().includes(cisi.toLowerCase()));
  const nearbyImage = images.find((image) => {
    const imageIndex = page.text.indexOf(image.thumbnailUrl || image.url);
    const targetIndex = page.text.toLowerCase().indexOf(cisi.toLowerCase());
    return imageIndex >= 0 && targetIndex >= 0 && Math.abs(imageIndex - targetIndex) < 4000;
  });
  if (exactImage) return 'artifact_label_in_image_url';
  if (nearbyImage && context) return 'artifact_mention_with_nearby_image';
  return 'text_only_or_bibliographic_lead';
}

const packetRows = parseCsv(fs.readFileSync(packetCsv, 'utf8'));
const targetArtifacts = [...new Set(packetRows.map((row) => row.cisi))].sort((a, b) =>
  a.localeCompare(b, undefined, { numeric: true }),
);

const sourcePages = [
  ...fixedSourcePages,
  ...targetArtifacts.map((cisi) => ({
    url: `https://bharatkalyan97.blogspot.com/feeds/posts/default?q=${encodeURIComponent(cisi)}&max-results=25`,
    source_channel: 'claim_heavy_blogger_atom_search',
    source_tier: 'T4 public search lead only',
    query_artifact: cisi,
  })),
];

const pageRows = [];
const leadRows = [];
const seenLeadKeys = new Set();

for (const source of sourcePages) {
  const page = await fetchText(source.url);
  const text = page.text ?? '';
  const matchedArtifacts = targetArtifacts.filter((cisi) => pageHasTarget(text, cisi));
  const images = extractImages(text);
  const claimCounts = countClaimTerms(text);

  pageRows.push([
    source.source_channel,
    source.query_artifact ?? '',
    source.url,
    page.statusCode,
    text.length,
    matchedArtifacts.join(';'),
    images.length,
    claimCounts.rebus,
    claimCounts.decipherment_terms,
    claimCounts.bill_of_lading,
    claimCounts.supercargo,
    claimCounts.trade_account,
    claimCounts.metrological,
  ]);

  if (source.source_channel === 'claim_heavy_blogger_atom_search') {
    const entries = extractAtomEntries(text);
    for (const entry of entries) {
      if (!pageHasTarget(`${entry.title} ${entry.content}`, source.query_artifact)) continue;
      const entryImages = extractImages(entry.content).slice(0, 8);
      const leadKind = entryImages.length
        ? 'artifact_mention_with_candidate_images'
        : 'text_only_or_bibliographic_lead';
      const rows = entryImages.length ? entryImages : [{ url: '', width: '', height: '', alt: '' }];
      for (const image of rows) {
        const key = [
          source.query_artifact,
          entry.url,
          leadKind,
          image.url,
          entry.title,
        ].join('|');
        if (seenLeadKeys.has(key)) continue;
        seenLeadKeys.add(key);
        leadRows.push({
          cisi: source.query_artifact,
          source_channel: source.source_channel,
          source_title: entry.title,
          source_url: entry.url,
          source_published: entry.published,
          lead_kind: leadKind,
          target_context: contextAroundArtifact(`${entry.title} ${entry.content}`, source.query_artifact),
          image_url: image.url,
          image_width_hint: image.width,
          image_height_hint: image.height,
          image_alt: image.alt,
          source_tier: source.source_tier,
        });
      }
    }
    continue;
  }

  for (const cisi of matchedArtifacts) {
    const leadKind = leadKindForFixedPage(page, cisi, source);
    const pageImages = extractImages(page.text);
    let rows = [{ url: '', width: '', height: '', alt: '' }];
    if (leadKind === 'artifact_label_in_image_url') {
      rows = pageImages.filter((image) => image.url.toLowerCase().includes(cisi.toLowerCase()));
    } else if (leadKind === 'artifact_mention_with_nearby_image') {
      rows = pageImages.slice(0, 6);
    }

    for (const image of rows) {
      const key = [cisi, source.url, leadKind, image.url].join('|');
      if (seenLeadKeys.has(key)) continue;
      seenLeadKeys.add(key);
      leadRows.push({
        cisi,
        source_channel: source.source_channel,
        source_title: '',
        source_url: source.url,
        source_published: '',
        lead_kind: leadKind,
        target_context: contextAroundArtifact(page.text, cisi),
        image_url: image.url,
        image_width_hint: image.width,
        image_height_hint: image.height,
        image_alt: image.alt,
        source_tier: source.source_tier,
      });
    }
  }
}

leadRows.sort(
  (a, b) =>
    a.cisi.localeCompare(b.cisi, undefined, { numeric: true }) ||
    a.lead_kind.localeCompare(b.lead_kind) ||
    a.source_url.localeCompare(b.source_url),
);

const leadKindsByArtifact = Object.fromEntries(
  targetArtifacts.map((cisi) => [
    cisi,
    [...new Set(leadRows.filter((row) => row.cisi === cisi).map((row) => row.lead_kind))].sort(),
  ]),
);

const artifactsWithCandidateImages = targetArtifacts.filter((cisi) =>
  (leadKindsByArtifact[cisi] ?? []).some((kind) => kind.includes('image')),
);
const artifactsWithPublishedDirectionNotes = targetArtifacts.filter((cisi) =>
  (leadKindsByArtifact[cisi] ?? []).includes('published_direction_or_corpus_note'),
);
const artifactsWithTextOnlyLeads = targetArtifacts.filter((cisi) =>
  (leadKindsByArtifact[cisi] ?? []).includes('text_only_or_bibliographic_lead'),
);
const artifactsWithNoLead = targetArtifacts.filter((cisi) => (leadKindsByArtifact[cisi] ?? []).length === 0);

const leadCsvRows = [
  [
    'cisi',
    'source_channel',
    'source_title',
    'source_url',
    'source_published',
    'lead_kind',
    'target_context',
    'image_url',
    'image_width_hint',
    'image_height_hint',
    'image_alt',
    'source_tier',
    'admissible_use',
    'non_admissible_use',
    'needs_manual_check',
  ],
  ...leadRows.map((row) => [
    row.cisi,
    row.source_channel,
    row.source_title,
    row.source_url,
    row.source_published,
    row.lead_kind,
    row.target_context,
    row.image_url,
    row.image_width_hint,
    row.image_height_hint,
    row.image_alt,
    row.source_tier,
    'source discovery and plate request targeting only',
    'sign segmentation, allography, side orientation, physical side function, numerical value, metrological reading, sign meaning, phonetic value, language identity, translation, or acceptance of secondary decipherment claims',
    'yes',
  ]),
];

const pageCsvRows = [
  [
    'source_channel',
    'query_artifact',
    'source_url',
    'status_code',
    'bytes',
    'matched_packet_artifacts',
    'image_tag_count',
    'rebus_terms',
    'decipherment_terms',
    'bill_of_lading_terms',
    'supercargo_terms',
    'trade_account_terms',
    'metrological_terms',
  ],
  ...pageRows,
];

const summary = {
  source: '17-artifact short-mark plate public lead search',
  checked_at: checkedAt,
  input_packet: path.relative(base, packetCsv).replaceAll('\\', '/'),
  packet_artifacts: targetArtifacts.length,
  source_pages_checked: sourcePages.length,
  fixed_source_pages_checked: fixedSourcePages.length,
  blogger_atom_queries_checked: targetArtifacts.length,
  lead_rows: leadRows.length,
  artifacts_with_candidate_image_leads: artifactsWithCandidateImages,
  artifacts_with_published_direction_or_corpus_notes: artifactsWithPublishedDirectionNotes,
  artifacts_with_text_only_or_bibliographic_leads: artifactsWithTextOnlyLeads,
  artifacts_with_no_public_lead_in_checked_sources: artifactsWithNoLead,
  lead_kinds_by_artifact: leadKindsByArtifact,
  fixed_source_pages: fixedSourcePages.map((source) => source.url),
  caveat:
    'Candidate image leads from claim-heavy blogs are public source-discovery pointers only. They do not validate inscription segmentation, side order, direction, allography, function, meaning, or translation.',
  key_observation:
    'The checked public sources produced secondary or candidate leads for the packet, but no source-grade object-side plate validation for any of the 17 artifacts.',
  outputs: [
    path.relative(base, outLeadsCsv).replaceAll('\\', '/'),
    path.relative(base, outPagesCsv).replaceAll('\\', '/'),
  ],
};

fs.writeFileSync(outLeadsCsv, toCsv(leadCsvRows));
fs.writeFileSync(outPagesCsv, toCsv(pageCsvRows));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
