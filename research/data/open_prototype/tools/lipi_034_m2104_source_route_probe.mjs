import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const routeHitsOut = path.join(reportsDir, 'lipi_034_m2104_source_route_hits.csv');
const visualNotesOut = path.join(reportsDir, 'lipi_034_m2104_source_visual_notes.csv');
const summaryOut = path.join(reportsDir, 'lipi_034_m2104_source_route_summary.json');

const checkedDate = '2026-05-25';
const iaIdentifier = 'TheIndusScript.TextConcordanceAndTablesIravathanMahadevan';
const iaDownloadBase = `https://archive.org/download/${iaIdentifier}`;
const iaDetailsBase = `https://archive.org/details/${iaIdentifier}`;

const volumes = {
  india: {
    label: 'CISI Collections in India',
    xmlFile: 'Corpus of Indus Seals and Inscriptions. Collections in India_djvu.xml',
    detailsPath: 'Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India',
  },
  pakistan: {
    label: 'CISI Collections in Pakistan',
    xmlFile: 'Corpus of Indus Seals and Inscriptions. Collections in Pakistan_djvu.xml',
    detailsPath:
      'Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan',
  },
};

const targetSpecs = [
  {
    cisi: 'M-2104',
    role: 'target_p0_034',
    queries: ['M-2104', '2104'],
    route_question: 'Can IA CISI provide a direct plate route for the Parpola text no. 12 target?',
  },
  {
    cisi: 'M-478',
    role: 'text_12_tablet_parallel',
    queries: ['M-478', '478', 'MOHENJO-DARO 478-481'],
    route_question: 'Can IA CISI supply the tablet parallel image and pot-count context?',
  },
  {
    cisi: 'M-480',
    role: 'text_12_tablet_parallel',
    queries: ['M-480', '480', 'MOHENJO-DARO 478-481'],
    route_question: 'Can IA CISI supply the second tablet parallel image?',
  },
  {
    cisi: 'M-1425',
    role: 'text_12_tablet_parallel',
    queries: ['M-1425', '1425', 'MOHENJO-DARO1425-1428', 'MOHENJO-DARO 1425-1428'],
    route_question: 'Can IA CISI supply the Pakistan-volume tablet parallel image?',
  },
  {
    cisi: 'H-543',
    role: 'sign_15_1_control',
    queries: ['H-543', '543', 'HARAPPA 537-543'],
    route_question: 'Can IA CISI supply a source image for the signs 15/1 control?',
  },
  {
    cisi: 'H-544',
    role: 'sign_15_1_control',
    queries: ['H-544', '544', 'HARAPPA 544-557'],
    route_question: 'Can IA CISI supply a source image for the signs 15/1 control?',
  },
  {
    cisi: 'M-915',
    role: 'sign_15_1_named_seal_control',
    queries: ['M-915', '915', 'MOHENJO-DARO 914-922'],
    route_question: 'Can IA CISI supply a source image for a named signs 15/1 end-text control?',
  },
  {
    cisi: 'M-715',
    role: 'named_context_conflict_or_unresolved',
    queries: ['M-715', '715', 'MOHENJO-DARO 715-717'],
    route_question: 'Can IA CISI supply a source image for the Parpola conflict/control row?',
  },
  {
    cisi: 'M-896',
    role: 'named_context_conflict_or_unresolved',
    queries: ['M-896', '896', 'MOHENJO-DARO 893-898'],
    route_question: 'Can IA CISI supply a source image for the Parpola conflict/control row?',
  },
];

function toCsv(rows) {
  if (rows.length === 0) return '';
  const header = Object.keys(rows[0]);
  const body = rows.map((row) =>
    header
      .map((key) => `"${String(row[key] ?? '').replaceAll('"', '""')}"`)
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

function escapeRegex(text) {
  return String(text).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

async function fetchText(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Fetch failed ${response.status}: ${url}`);
  return response.text();
}

function pageUrl(config, leaf) {
  return `${iaDetailsBase}/${config.detailsPath}/page/n${leaf}/mode/1up`;
}

function imageUrl(config, leaf, width = 2000) {
  return `${iaDownloadBase}/${config.detailsPath}/page/n${leaf}_w${width}.jpg`;
}

function localImagePath(config, leaf, width = 2000) {
  return path
    .join(
      'tmp',
      'cisi_m2104_packet',
      `${config.detailsPath.replaceAll('%20', '_20').replaceAll('.', '')}_page_n${leaf}_w${width}_jpg.jpg`,
    )
    .replaceAll('\\', '/');
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
    const words = [...chunk.matchAll(/<WORD\b[^>]*>([\s\S]*?)<\/WORD>/g)].map((wordMatch) =>
      decodeEntities(wordMatch[1]).replace(/\s+/g, ' ').trim(),
    );
    chunks.push({
      leaf,
      pageFile,
      text: words.join(' ').replace(/\s+/g, ' ').trim(),
    });
  }
  return chunks;
}

function queryKind(cisi, query) {
  if (query === cisi) return 'exact_object_id';
  if (/^\d+$/.test(query)) return 'bare_number_variant';
  if (/^[A-Z-]+\s/.test(query)) return 'plate_header_or_range';
  return 'variant_string';
}

function contextsFor(text, query) {
  const clean = text.replace(/\s+/g, ' ').trim();
  const regex = new RegExp(`(?<![A-Za-z0-9])${escapeRegex(query)}(?![A-Za-z0-9])`, 'gi');
  const contexts = [];
  let match;
  while ((match = regex.exec(clean)) !== null) {
    const before = clean.slice(0, match.index).split(/\s+/).filter(Boolean).slice(-16).join(' ');
    const after = clean
      .slice(match.index + query.length)
      .split(/\s+/)
      .filter(Boolean)
      .slice(0, 18)
      .join(' ');
    contexts.push(`${before} [[${clean.slice(match.index, match.index + query.length)}]] ${after}`.trim());
  }
  return contexts;
}

function classifyPage(text, context) {
  const sample = `${text.slice(0, 260)} ${context}`.toLowerCase();
  if (sample.includes('introduction')) return 'source_discussion';
  if (sample.includes('data ')) return 'data_register';
  if (
    sample.includes('seals') ||
    sample.includes('tablets in bas-relief') ||
    sample.includes('mohenjo-daro') ||
    sample.includes('harappa')
  ) {
    return 'plate_candidate';
  }
  if (sample.includes('rhd') || sample.includes('psw')) return 'index_or_register_noise';
  return 'ocr_context_unclassified';
}

const pagesByVolume = {};
for (const [key, config] of Object.entries(volumes)) {
  const xmlUrl = `${iaDownloadBase}/${encodeURIComponent(config.xmlFile)}`;
  pagesByVolume[key] = {
    config,
    pages: pageChunks(await fetchText(xmlUrl)),
  };
}

const routeRows = [];
for (const spec of targetSpecs) {
  for (const query of spec.queries) {
    for (const { config, pages } of Object.values(pagesByVolume)) {
      for (const page of pages) {
        const contexts = contextsFor(page.text, query);
        if (contexts.length === 0) continue;
        const context = contexts.join(' || ');
        routeRows.push({
          checked_date: checkedDate,
          cisi: spec.cisi,
          role: spec.role,
          query,
          query_kind: queryKind(spec.cisi, query),
          ia_volume: config.label,
          ia_leaf: page.leaf,
          ia_reader_page_url: pageUrl(config, page.leaf),
          ia_page_image_url: imageUrl(config, page.leaf, 2000),
          hit_count_on_page: contexts.length,
          page_context_class: classifyPage(page.text, context),
          route_question: spec.route_question,
          ocr_context: context,
          source_use:
            'route_discovery_only_manual_visual_notes_decide_whether_this_is_a_plate_data_register_discussion_or_noise',
          accepted_source_mapping: '0',
          accepted_decipherment_claim: '0',
        });
      }
    }
  }
}

routeRows.sort((a, b) => {
  const cisiCompare = a.cisi.localeCompare(b.cisi, undefined, { numeric: true });
  if (cisiCompare !== 0) return cisiCompare;
  const queryCompare = a.query.localeCompare(b.query, undefined, { numeric: true });
  if (queryCompare !== 0) return queryCompare;
  const volumeCompare = a.ia_volume.localeCompare(b.ia_volume);
  if (volumeCompare !== 0) return volumeCompare;
  return Number(a.ia_leaf) - Number(b.ia_leaf);
});

function visualRow({
  cisi,
  role,
  source,
  configKey,
  leaf,
  localPath,
  className,
  status,
  note,
  sourceUse,
}) {
  const config = configKey ? volumes[configKey] : null;
  return {
    checked_date: checkedDate,
    cisi,
    role,
    source,
    ia_volume: config?.label ?? '',
    ia_leaf: leaf ?? '',
    ia_reader_page_url: config && leaf ? pageUrl(config, leaf) : '',
    ia_page_image_url: config && leaf ? imageUrl(config, leaf, 2000) : '',
    local_image_path: localPath ?? (config && leaf ? localImagePath(config, leaf, 2000) : ''),
    manual_visual_class: className,
    visual_status: status,
    manual_visual_note: note,
    source_use: sourceUse,
    accepted_source_mapping: '0',
    accepted_decipherment_claim: '0',
  };
}

const visualRows = [
  visualRow({
    cisi: 'M-2104',
    role: 'target_p0_034',
    source: 'Parpola 2019 Fig. 1 text no. 12',
    localPath: 'tmp/pdfs/parpola_2019_fig1_text12_crop3.png',
    className: 'published_figure_target',
    status: 'target_visual_available_outside_ia_cisi_plate_layer',
    note:
      'Parpola 2019 visually anchors text no. 12 and prose describes it as UIII followed by signs 15 and 1; IA CISI exact M-2104 route was not found in the checked XML.',
    sourceUse:
      'target source for crosswalk hypothesis; still not accepted mapping until sign segmentation is independently checked',
  }),
  visualRow({
    cisi: 'M-478',
    role: 'text_12_tablet_parallel',
    source: 'CISI IA public scan',
    configKey: 'india',
    leaf: 150,
    className: 'plate_image',
    status: 'tablet_parallel_plate_visible',
    note:
      'Plate header reads Mohenjo-Daro 478-481, tablets in bas-relief. M-478 A/B and smaller side photos are visible; M-478 A carries the inscription lane and M-478 B carries the iconographic scene Parpola uses for the four-pot discussion.',
    sourceUse:
      'visual test target for 700-004 as UIIII/four-pot cluster and 400/097 tail signs',
  }),
  visualRow({
    cisi: 'M-480',
    role: 'text_12_tablet_parallel',
    source: 'CISI IA public scan',
    configKey: 'india',
    leaf: 150,
    className: 'plate_image',
    status: 'tablet_parallel_plate_visible',
    note:
      'Same plate as M-478. M-480 A/B and smaller side photos are visible in the lower half; enough to route the image check, but sign-level segmentation should use a crop or higher resolution.',
    sourceUse: 'visual test target for 700-004 as UIIII/four-pot cluster and 400/097 tail signs',
  }),
  visualRow({
    cisi: 'M-1425',
    role: 'text_12_tablet_parallel',
    source: 'CISI IA public scan',
    configKey: 'pakistan',
    leaf: 227,
    className: 'plate_image',
    status: 'tablet_parallel_plate_visible',
    note:
      'Plate header reads Mohenjo-Daro 1425-1428, tablets in bas-relief. M-1425 A/a/B/b/E are visible; M-1425 A/a show the tablet-parallel inscription lane needed for the 700-004 and 400/097 check.',
    sourceUse: 'visual test target for 700-004 as UIIII/four-pot cluster and 400/097 tail signs',
  }),
  visualRow({
    cisi: 'H-543',
    role: 'sign_15_1_control',
    source: 'CISI IA public scan',
    configKey: 'pakistan',
    leaf: 324,
    className: 'plate_image',
    status: 'control_plate_visible_broken',
    note:
      'Harappa 537-543 seal plate. H-543 A/a are visible at the bottom; the artifact is broken, but the route is adequate for checking whether the local 151-097 row is a two-sign signs 15/1 control.',
    sourceUse: 'control for 097/151 under right-to-left reading',
  }),
  visualRow({
    cisi: 'H-544',
    role: 'sign_15_1_control',
    source: 'CISI IA public scan',
    configKey: 'pakistan',
    leaf: 325,
    className: 'plate_image',
    status: 'control_plate_visible',
    note:
      'Harappa 544-557 seal plate. H-544 A/a are visible at the top left with a clear short sign sequence and damage profile; this is the cleaner H control for signs 15/1.',
    sourceUse: 'control for 097/151 under right-to-left reading',
  }),
  visualRow({
    cisi: 'M-915',
    role: 'sign_15_1_named_seal_control',
    source: 'CISI IA public scan',
    configKey: 'pakistan',
    leaf: 122,
    className: 'plate_image',
    status: 'control_plate_visible',
    note:
      'Mohenjo-Daro 914-922 seal plate. M-915 A/a are visible in the top row; this is a named Parpola control for signs 15 and 1 at text end.',
    sourceUse: 'control for final 097/151 under right-to-left reading',
  }),
  visualRow({
    cisi: 'M-715',
    role: 'named_context_conflict_or_unresolved',
    source: 'CISI IA public scan',
    configKey: 'pakistan',
    leaf: 80,
    className: 'plate_image',
    status: 'conflict_plate_visible',
    note:
      'Mohenjo-Daro 715-717 seal plate. M-715 A/a are visible; the local row does not expose a clean 151/097 pair, so this is a direct conflict-resolution image.',
    sourceUse: 'conflict check for Parpola signs 15/1 claim versus local encoding',
  }),
  visualRow({
    cisi: 'M-896',
    role: 'named_context_conflict_or_unresolved',
    source: 'CISI IA public scan',
    configKey: 'pakistan',
    leaf: 119,
    className: 'plate_image',
    status: 'conflict_plate_visible',
    note:
      'Mohenjo-Daro 893-898 seal plate. M-896 A/a are visible at left; the local row begins with 151 but lacks 097, so this is a direct conflict-resolution image.',
    sourceUse: 'conflict check for Parpola signs 15/1 claim versus local encoding',
  }),
  visualRow({
    cisi: 'M-478',
    role: 'prior_context_support',
    source: 'CISI IA public scan / introduction',
    configKey: 'india',
    leaf: 19,
    className: 'source_discussion',
    status: 'pot_count_context_support',
    note:
      'The introduction describes a U-shaped pot sign preceded by zero to four vertical strokes, and discusses M-478/M-479 as a four-pot offering context. This supports the kind of cluster under test, not the M-2104 target image.',
    sourceUse: 'prior-work pressure for the U+stroke pot-count interpretation only',
  }),
];

function uniqueSorted(values) {
  return [...new Set(values.filter(Boolean))].sort((a, b) =>
    a.localeCompare(b, undefined, { numeric: true }),
  );
}

const exactHitObjects = uniqueSorted(
  routeRows.filter((row) => row.query_kind === 'exact_object_id').map((row) => row.cisi),
);
const plateConfirmedObjects = uniqueSorted(
  visualRows.filter((row) => row.manual_visual_class === 'plate_image').map((row) => row.cisi),
);
const noExactHitObjects = targetSpecs
  .map((spec) => spec.cisi)
  .filter((cisi) => !exactHitObjects.includes(cisi));
const noPlateConfirmedObjects = targetSpecs
  .map((spec) => spec.cisi)
  .filter((cisi) => !plateConfirmedObjects.includes(cisi));

const routeCountsByObject = Object.fromEntries(
  targetSpecs.map((spec) => {
    const rows = routeRows.filter((row) => row.cisi === spec.cisi);
    return [
      spec.cisi,
      {
        route_rows: rows.length,
        exact_route_rows: rows.filter((row) => row.query_kind === 'exact_object_id').length,
        plate_candidate_route_rows: rows.filter((row) => row.page_context_class === 'plate_candidate')
          .length,
        visual_plate_confirmed: plateConfirmedObjects.includes(spec.cisi),
        leaves: uniqueSorted(rows.map((row) => `${row.ia_volume} n${row.ia_leaf}`)),
      },
    ];
  }),
);

const summary = {
  checked_date: checkedDate,
  artifact: 'lipi_034_m2104_source_route_probe',
  question:
    'Which public IA/CISI or Parpola source routes can visually test the M-2104 Parpola crosswalk hypothesis?',
  target_crosswalk_under_test:
    'M-2104 +151-097-700-034+ vs M-478/M-480/M-1425 +400-097-700-004+; candidate 097=Parpola sign 15, 151=sign 1, 400=sign 107, 700-034/UIII vs 700-004/UIIII.',
  route_hit_rows: routeRows.length,
  visual_note_rows: visualRows.length,
  exact_hit_objects: exactHitObjects,
  no_exact_hit_objects: noExactHitObjects,
  plate_visual_confirmed_objects: plateConfirmedObjects,
  no_plate_visual_confirmed_objects: noPlateConfirmedObjects,
  route_counts_by_object: routeCountsByObject,
  strongest_positive:
    'M-478, M-480, and M-1425 now have public CISI plate images; H-543, H-544, M-915, M-715, and M-896 also have plate images for controls/conflicts.',
  strongest_negative:
    'IA CISI OCR did not find exact M-2104; bare 2104 is register/index noise, so M-2104 still rests on Parpola 2019 Fig. 1/prose until a CISI plate or high-resolution rod image is acquired.',
  immediate_falsification_test:
    'Crop and compare M-478/M-480/M-1425 tablet inscription clusters against Parpola Fig. 1 text no. 12: if 700-004 is not visually the four-stroke U/pot cluster in the parallels, or 700-034 is not the three-stroke counterpart in M-2104, the live 034 extraction fails.',
  accepted_source_mappings: 0,
  accepted_decipherment_claims: 0,
  source_files: {
    parpola_2019:
      'https://tuhat.helsinki.fi/ws/portalfiles/portal/129602857/Parpola_A_2019_Inscriptions_incised_on_the_Harappan_bone_rods_Proceedings_of_EASAA_22.pdf',
    ia_details: iaDetailsBase,
    cisi_india_xml: `${iaDownloadBase}/${encodeURIComponent(volumes.india.xmlFile)}`,
    cisi_pakistan_xml: `${iaDownloadBase}/${encodeURIComponent(volumes.pakistan.xmlFile)}`,
  },
  outputs: [
    path.relative(base, routeHitsOut).replaceAll('\\', '/'),
    path.relative(base, visualNotesOut).replaceAll('\\', '/'),
    path.relative(base, summaryOut).replaceAll('\\', '/'),
  ],
};

fs.writeFileSync(routeHitsOut, toCsv(routeRows), 'utf8');
fs.writeFileSync(visualNotesOut, toCsv(visualRows), 'utf8');
fs.writeFileSync(summaryOut, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
