import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const routePath = path.join(reportsDir, 'lipi_frame700_034_source_route_audit.csv');
const outCsv = path.join(reportsDir, 'lipi_frame700_034_ia_cisi_page_locator.csv');
const outJson = path.join(reportsDir, 'lipi_frame700_034_ia_cisi_page_locator_summary.json');

const iaIdentifier = 'TheIndusScript.TextConcordanceAndTablesIravathanMahadevan';
const iaDownloadBase = `https://archive.org/download/${iaIdentifier}`;
const iaDetailsBase = `https://archive.org/details/${iaIdentifier}`;

const volumeFiles = {
  cisi_india: {
    label: 'CISI Collections in India',
    routeValue: 'CISI_Collections_in_India_djvu.txt',
    xmlFile: 'Corpus of Indus Seals and Inscriptions. Collections in India_djvu.xml',
    detailsPath: 'Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India',
  },
  cisi_pakistan: {
    label: 'CISI Collections in Pakistan',
    routeValue: 'CISI_Collections_in_Pakistan_djvu.txt',
    xmlFile: 'Corpus of Indus Seals and Inscriptions. Collections in Pakistan_djvu.xml',
    detailsPath: 'Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan',
  },
};

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
  if (rows.length === 0) return '';
  const header = Object.keys(rows[0]);
  const body = rows.map((row) =>
    header
      .map((key) => {
        const text = String(row[key] ?? '');
        return `"${text.replaceAll('"', '""')}"`;
      })
      .join(','),
  );
  return `${[header.map((key) => `"${key}"`).join(','), ...body].join('\n')}\n`;
}

function decodeEntities(text) {
  return String(text)
    .replaceAll('&amp;', '&')
    .replaceAll('&lt;', '<')
    .replaceAll('&gt;', '>')
    .replaceAll('&quot;', '"')
    .replaceAll('&apos;', "'");
}

async function fetchText(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Fetch failed ${response.status} ${response.statusText}: ${url}`);
  }
  return response.text();
}

function pageChunks(xml) {
  const chunks = [];
  const objectRegex = /<OBJECT\b[\s\S]*?<\/OBJECT>/g;
  let match;
  while ((match = objectRegex.exec(xml)) !== null) {
    const chunk = match[0];
    const pageMatch = chunk.match(/<PARAM name="PAGE" value="([^"]+)"/);
    if (!pageMatch) continue;
    const pageFile = pageMatch[1];
    const leafMatch = pageFile.match(/_(\d+)\.djvu$/);
    const leaf = leafMatch ? Number(leafMatch[1]) : null;
    const words = [...chunk.matchAll(/<WORD\b[^>]*coords="([^"]+)"[^>]*>([\s\S]*?)<\/WORD>/g)].map(
      (wordMatch) => ({
        coords: wordMatch[1],
        text: decodeEntities(wordMatch[2]).replace(/\s+/g, ' ').trim(),
      }),
    );
    chunks.push({ leaf, pageFile, words, text: words.map((word) => word.text).join(' ') });
  }
  return chunks;
}

function escapeRegex(text) {
  return String(text).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function contextsFor(text, needle) {
  const clean = text.replace(/\s+/g, ' ').trim();
  const regex = new RegExp(`(?<![A-Za-z0-9])${escapeRegex(needle)}(?![A-Za-z0-9])`, 'g');
  const contexts = [];
  let match;
  while ((match = regex.exec(clean)) !== null) {
    const before = clean.slice(0, match.index).split(/\s+/).filter(Boolean).slice(-18).join(' ');
    const after = clean
      .slice(match.index + needle.length)
      .split(/\s+/)
      .filter(Boolean)
      .slice(0, 18)
      .join(' ');
    contexts.push(`${before} [[${needle}]] ${after}`.trim());
  }
  return contexts;
}

function coordsFor(words, needle) {
  const hits = [];
  for (let index = 0; index < words.length; index += 1) {
    if (words[index].text === needle) {
      hits.push(`${index}:${words[index].coords}`);
    }
  }
  return hits;
}

function classifyPageContext(context) {
  const text = context.toLowerCase();
  if (text.includes('plate') || text.includes('pl.')) return 'plate_or_plate_reference';
  if (text.includes('figure') || text.includes('fig.')) return 'figure_or_figure_reference';
  if (text.includes('table')) return 'table_or_concordance_reference';
  if (text.includes('index')) return 'index_or_register_reference';
  return 'ocr_context_unclassified';
}

const routeRows = parseCsv(fs.readFileSync(routePath, 'utf8'));
const iaRows = routeRows.filter((row) => Number(row.ia_ocr_hits) > 0);

const xmlByRouteValue = {};
for (const config of Object.values(volumeFiles)) {
  xmlByRouteValue[config.routeValue] = {
    config,
    pages: pageChunks(await fetchText(`${iaDownloadBase}/${encodeURIComponent(config.xmlFile)}`)),
  };
}

const outRows = [];
for (const routeRow of iaRows) {
  const volume = xmlByRouteValue[routeRow.ia_ocr_source];
  if (!volume) throw new Error(`No IA volume config for ${routeRow.ia_ocr_source}`);
  const { config, pages } = volume;
  for (const page of pages) {
    const contexts = contextsFor(page.text, routeRow.cisi);
    if (contexts.length === 0) continue;
    const pageUrl = `${iaDetailsBase}/${config.detailsPath}/page/n${page.leaf}/mode/1up`;
    const pageImageUrl = `${iaDownloadBase}/${config.detailsPath}/page/n${page.leaf}_w1200.jpg`;
    outRows.push({
      checked_date: '2026-05-25',
      cisi: routeRow.cisi,
      priority: routeRow.priority,
      lanes: routeRow.lanes,
      roles: routeRow.roles,
      batch_ids: routeRow.batch_ids,
      packet_source_hooks: routeRow.packet_source_hooks,
      ia_volume: config.label,
      ia_ocr_source: routeRow.ia_ocr_source,
      ia_page_file: page.pageFile,
      ia_leaf: page.leaf,
      ia_reader_page_url: pageUrl,
      ia_page_image_url: pageImageUrl,
      hit_count_on_page: contexts.length,
      word_coords_hits: coordsFor(page.words, routeRow.cisi).join(';'),
      page_context_class: classifyPageContext(contexts.join(' ')),
      ocr_context: contexts.join(' || '),
      source_use:
        'page_locator_only_manual_source_inspection_required_for_sign_visibility_side_order_direction_and_032_033_034_separation',
      accepted_decipherment_claim: '0',
    });
  }
}

outRows.sort((a, b) => {
  const c = a.cisi.localeCompare(b.cisi, undefined, { numeric: true });
  if (c !== 0) return c;
  return Number(a.ia_leaf) - Number(b.ia_leaf);
});

const foundObjects = new Set(outRows.map((row) => row.cisi));
const missingAfterPositiveRoute = iaRows.filter((row) => !foundObjects.has(row.cisi)).map((row) => row.cisi);

const byObject = Object.fromEntries(
  [...foundObjects].sort((a, b) => a.localeCompare(b, undefined, { numeric: true })).map((cisi) => {
    const rows = outRows.filter((row) => row.cisi === cisi);
    return [
      cisi,
      {
        page_rows: rows.length,
        hit_count: rows.reduce((sum, row) => sum + Number(row.hit_count_on_page), 0),
        leaves: rows.map((row) => row.ia_leaf),
        volume: rows[0]?.ia_volume ?? '',
      },
    ];
  }),
);

const summary = {
  checked_date: '2026-05-25',
  question: 'Where do the IA CISI OCR-hit FRAME700_034 packet objects occur at page level?',
  ia_route_objects_input: iaRows.length,
  located_objects: foundObjects.size,
  missing_after_positive_route: missingAfterPositiveRoute,
  page_locator_rows: outRows.length,
  total_hit_count: outRows.reduce((sum, row) => sum + Number(row.hit_count_on_page), 0),
  by_object: byObject,
  accepted_decipherment_claims: 0,
  source_boundary:
    'OCR page location is not sign validation. It only gives target pages for manual plate/source inspection.',
  immediate_next_action:
    'Open the located reader pages and fill source citation, plate/page ID, side count, side order, direction basis, and 032/033/034 visibility fields in the two-lane coding sheet.',
  internet_archive_identifier: iaIdentifier,
  source_files: Object.fromEntries(
    Object.entries(volumeFiles).map(([key, value]) => [
      key,
      {
        label: value.label,
        xml: `${iaDownloadBase}/${encodeURIComponent(value.xmlFile)}`,
      },
    ]),
  ),
};

fs.writeFileSync(outCsv, toCsv(outRows));
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`);

console.log(JSON.stringify(summary, null, 2));
