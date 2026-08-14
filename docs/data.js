/* =========================================================================
   Every piece of content the page displays lives here, so the rendering code
   in app.js never has to hold facts. Two kinds of content are mixed, and the
   difference matters for the project's claim discipline:

   REAL — SITES (archaeological sites, coordinates approximate), BRANCH (the
   project's actual 002 sign-structure), LEDGER (accepted counts straight from
   claims.json), TIMELINE, GRAVES (retracted claims), and the numeric sign rows
   inside SEALS. Change these only to match the ledger.

   ILLUSTRATIVE — GLYPHS are original line drawings in the spirit of Indus
   signs, not tracings of real ones, so nobody can mistake the page's artwork
   for evidence. PUZZLE rows are made up out of real sign codes to teach the
   idea of a terminal tail; they are not corpus rows.
   ========================================================================= */
window.IVC = (function () {

  /* ---- Decorative glyphs: SVG path data drawn on a 64x64 grid, stroked
     rather than filled. Illustrative stand-ins, never facsimiles. ------- */
  var GLYPHS = {
    fish:    "M14 32C24 21 40 21 50 32C40 43 24 43 14 32Z M22 32H40 M50 32L57 27 M50 32L57 37",
    jar:     "M24 18H40L44 28V42C44 47 39 50 32 50C25 50 20 47 20 42V28Z M20 30H44",
    man:     "M32 16a3.4 3.4 0 1 0 0.1 0Z M32 22V40 M21 27L32 31L43 27 M24 51L32 40L40 51",
    wheel:   "M32 13a19 19 0 1 0 0.1 0Z M32 13V51 M13 32H51 M19 19L45 45 M45 19L19 45",
    comb:    "M15 23H49 M20 23V47 M28 23V47 M36 23V47 M44 23V47",
    arrow:   "M16 41L32 21L48 41 M32 21V51",
    twin:    "M25 15V49 M39 15V49 M25 23H39 M25 41H39",
    cup:     "M19 17V35C19 44 25 49 32 49C39 49 45 44 45 35V17",
    bowtie:  "M16 20L16 44L32 32Z M48 20L48 44L32 32Z",
    grid:    "M18 18H46V46H18Z M18 32H46 M32 18V46",
    water:   "M13 26L22 34L31 26L40 34L49 26 M13 40L22 48L31 40L40 48L49 40",
    diamond: "M32 14L50 32L32 50L14 32Z M32 22V42 M22 32H42",
    spear:   "M32 12V52 M32 12L25 23 M32 12L39 23 M24 44H40",
    trident: "M32 52V24 M32 24L21 15 M32 24L43 15 M32 24V14",
    eye:     "M14 32C22 24 42 24 50 32C42 40 22 40 14 32Z M32 32a5 5 0 1 0 0.1 0Z",
    vessel:  "M22 16C22 24 26 26 26 32C26 38 22 40 22 48H42C42 40 38 38 38 32C38 26 42 24 42 16Z"
  };
  var GLYPH_KEYS = Object.keys(GLYPHS);

  /* ---- Archaeological sites, in degrees of longitude and latitude ---- */
  // The map's projection window (set in app.js) is wide enough to hold
  // Mesopotamia and the Indus in one frame, because the trade link between
  // them is the point of the map.
  var SITES = [
    { id: "harappa",     name: "Harappa",        lon: 72.86, lat: 30.63, type: "indus", note: "Source site of tablet H-1993, a frontier target for the 095 closure.", tag: "frontier" },
    { id: "mohenjo",     name: "Mohenjo-daro",   lon: 68.14, lat: 27.33, type: "indus", note: "Largest Indus city. Home of seals M-376, M-391 (the verified witnesses) and frontier seal M-1825.", tag: "verified" },
    { id: "dholavira",   name: "Dholavira",      lon: 70.21, lat: 23.89, type: "indus", note: "Walled city in the Rann of Kutch. Seal Acc. 8758 is a live frontier target for the 705 branch.", tag: "frontier" },
    { id: "lothal",      name: "Lothal",         lon: 72.25, lat: 22.52, type: "indus", note: "Port town with a dockyard; dense seal and bead finds tie the Indus to Gulf trade.", tag: "indus" },
    { id: "rakhigarhi",  name: "Rakhigarhi",     lon: 76.11, lat: 29.28, type: "indus", note: "One of the largest Harappan sites; aDNA work here reshaped the population debate.", tag: "indus" },
    { id: "kalibangan",  name: "Kalibangan",     lon: 74.13, lat: 29.47, type: "indus", note: "Early Harappan fire-altars and ploughed fields on the dry Ghaggar-Hakra.", tag: "indus" },
    { id: "ganweriwala", name: "Ganweriwala",    lon: 71.00, lat: 28.70, type: "indus", note: "A large, barely-excavated mound in the Cholistan desert. The script's unread frontier.", tag: "indus" },
    { id: "ur",          name: "Ur",             lon: 46.10, lat: 30.96, type: "meso",  note: "Mesopotamian city. Indus-style seals were found here; the Shu-ilishu seal names a translator of the Meluhhan language.", tag: "anchor" },
    { id: "susa",        name: "Susa",           lon: 48.25, lat: 32.19, type: "meso",  note: "Elamite capital. Linear Elamite's contested decipherment is a methodological comparator.", tag: "meso" },
    { id: "failaka",     name: "Failaka",        lon: 48.33, lat: 29.43, type: "gulf",  note: "Dilmun-era Gulf island; stamp seals here carry Indus-related signs.", tag: "gulf" }
  ];
  var TRADE = ["mohenjo", "lothal", "failaka", "ur"]; // waypoints of the Meluhha trade arc, drawn in order

  /* ---- The 002 branch: the actual object of study -------------------- */
  // Which units can follow the sign 002, and how far each one has got
  // through the gates. x and y place the node on the diagram: x is the
  // column, y is the lane. status drives both the colour and the label the
  // visitor reads, so it must use the ledger's own vocabulary --
  // verified | gated | open | context | root.
  var BRANCH = {
    nodes: [
      { id: "002",     label: "002", x: 0, y: 2,  status: "root",    info: "The conditioning sign. What follows 002 behaves differently than the same signs elsewhere." },
      { id: "861",     label: "861", x: 1, y: 1,  status: "context", info: "The fixed branch context 002-861. Inside it, one tail is provably regular." },
      { id: "390",     label: "390", x: 1, y: 3,  status: "context", info: "The adjacent branch 002-390. A live ecology of competing tails; the current frontier." },
      { id: "533717",  label: "533-717", x: 2, y: 1, status: "verified", info: "ACCEPTED. The only short unit whose every strict occurrence after 002-861 is a terminal tail. Witnesses M-376, M-391. Forger FPR 0.0002." },
      { id: "125",     label: "125", x: 2, y: 2.4, status: "open",  info: "Inside 002-390, sign 125 tends to continue the sequence (4/4 in strict rows). Structural pressure, not a reading." },
      { id: "095",     label: "095", x: 2, y: 3.2, status: "gated", info: "A closure branch. Second witness H-1993 is source-gated in CISI 3.1. One strict witness (M-71) so far." },
      { id: "705",     label: "705", x: 2, y: 4.0, status: "gated", info: "A repeated closure. Witnesses Dholavira 8758 and M-1825 are both source-gated. Zero strict witnesses yet." },
      { id: "590032",  label: "590-032", x: 2, y: 4.8, status: "open", info: "A continuing non-125 exception carried only by unprovenanced seal 3335.1. Object ID still blocked." }
    ],
    links: [
      ["002","861"], ["002","390"],
      ["861","533717"],
      ["390","125"], ["390","095"], ["390","705"], ["390","590032"]
    ]
  };

  /* ---- Decipherer's game: spot the terminal tail --------------------- */
  // Teaching rows, not corpus rows. They are built so that exactly one
  // option, 533-717, sits at the end of every line it appears in, while the
  // decoy options also turn up mid-line. That is the same test the project
  // ran, shrunk to six lines a visitor can eyeball.
  var PUZZLE = {
    prompt: "One unit below only ever appears at the very END of a line. The others turn up in the middle too. Which one always closes?",
    options: ["220-004", "533-717", "390-125", "031-002"],
    answer: "533-717",
    rows: [
      ["002","861","533","717"],
      ["740","002","861","533","717"],
      ["031","002","390","125","632"],
      ["220","004","002","861","533","717"],
      ["157","031","002","390","705"],
      ["002","861","603","533","717"]
    ],
    // Per row, the [first, last] token index of the terminal tail, or null if
    // that row has none. The game lights these up once the answer is found.
    tail: [ [2,3], [3,4], null, [4,5], null, [4,5] ]
  };

  /* ---- The scoreboard. These are the accepted counts from the claim
     ledger, copied exactly. Five zeros and a single structural finding is
     the project's real position, not a placeholder to be filled in. ----- */
  var LEDGER = [
    { n: 0, label: "Translations" },
    { n: 0, label: "Phonetic values" },
    { n: 0, label: "Sign meanings" },
    { n: 0, label: "Language identified" },
    { n: 0, label: "External anchors" },
    { n: 1, label: "Structural findings", verified: true }
  ];

  /* ---- A century of attempts. Real, dated events, ordered oldest first;
     app.js marks the last entry as "now". ------------------------------ */
  var TIMELINE = [
    { y: "1875", t: "The first seal", d: "Alexander Cunningham publishes a Harappan seal. Nobody knows what civilization it belongs to." },
    { y: "1924", t: "A civilization announced", d: "John Marshall reveals the Indus Valley Civilization to the world. The script becomes a famous unsolved problem overnight." },
    { y: "1953", t: "Linear B falls", d: "Ventris cracks Mycenaean Linear B, and Blegen's tripod tablet confirms it. The gold standard for proof: prediction, not assertion." },
    { y: "1964", t: "The Soviet computers", d: "Knorozov's team runs the first computer analyses, arguing the script is structured like Dravidian. Suggestive, never proven." },
    { y: "1977", t: "The concordance", d: "Iravatham Mahadevan publishes his 417-sign concordance, still the backbone of corpus work today." },
    { y: "1994", t: "Parpola's synthesis", d: "Asko Parpola's 'Deciphering the Indus Script' assembles the Dravidian case. Influential, unconfirmed." },
    { y: "2004", t: "Is it writing at all?", d: "Farmer, Sproat and Witzel argue the signs may not encode language. The field's null hypothesis gets teeth." },
    { y: "2009", t: "Entropy fights back", d: "Rao et al. answer with conditional entropy in Science. The debate is still open today, by design." },
    { y: "2022", t: "Linear Elamite, contested", d: "Desset's team claims its neighbor-script deciphered. Top journal, mixed reception: venue is not validation." },
    { y: "2025", t: "The million-dollar prize", d: "Tamil Nadu announces the Iravatham Mahadevan Prize for a verified decipherment. Unclaimed." },
    { y: "2026", t: "One brick, earned", d: "This project accepts its first structural finding after 10,000-shuffle forger tests and source-image binding. Zero readings claimed." }
  ];

  /* ---- The graveyard: retracted claims, straight from claims.json ---- */
  // Eight of the twenty-six retractions, chosen to show the range of ways a
  // claim can fail, each with its cause of death in plain language. The id
  // is the ledger's own claim id, so a reader can go find the full record.
  var GRAVES = [
    { id: "all_002_y_are_endings", title: "“Everything after 002 is an ending”", death: "Too broad. The skeptic pass found continuing rows; the clean version survives only inside one narrow branch." },
    { id: "internal_only_effective_unicity_gives_language_family", title: "“Cryptographic unicity can name the language”", death: "Retracted in-house: internal consistency alone cannot identify a language family. The same logic underlies famous external claims." },
    { id: "meluhha_site_overlap_as_external_anchor", title: "“Meluhha site overlap anchors the script”", death: "Geographic overlap is context, not an anchor. No object carried both readable text and bound Indus signs." },
    { id: "gadd_ur_accession_bridge_micro_bilingual", title: "“A micro-bilingual at Ur”", death: "The museum accession chain did not bind the cuneiform context to the Indus signs. The bridge dissolved on inspection." },
    { id: "bm120573_as_external_phonetic_anchor", title: "“BM 120573 gives a phonetic anchor”", death: "The object is real; the phonetic bridge was not. Killed at source normalization." },
    { id: "brahmi_shape_descent_nearest_neighbors", title: "“Brahmi shapes descend from Indus signs”", death: "Nearest-neighbor shape matching could not beat impostor forgers fed with unrelated scripts." },
    { id: "object_level_onomastic_value_attempts", title: "“We can read names off objects”", death: "Name-reading attempts failed the forger gate. No sound value survived." },
    { id: "directionality_source_visible_and_overlap_support", title: "“Reading direction, proven from photos”", death: "Six packet versions tried. Every route stayed catalog-mediated; none earned blind source-visible support." }
  ];
  var GRAVES_TOTAL = 26;

  /* ---- The artifact gallery ------------------------------------------ */
  // The eight objects the whole story hangs on. "text" holds the real
  // numeric sign row from the project's metadata layer; the glyph shapes the
  // page draws from it are decorative. "tail" counts back from the end of
  // the row to mark the terminal tail, and only the two verified witnesses
  // have one.
  var SEALS = [
    { obj: "M-376",  site: "Mohenjo-daro", row: "strict witness", text: ["740","100","176","002","861","533","717"], tail: 4, status: "verified", note: "Witness one: a seven-sign inscription. Only the glowing tail is shared with M-391; the rest is a different text entirely." },
    { obj: "M-391",  site: "Mohenjo-daro", row: "strict witness", text: ["405","845","686","740","793","003","233","805","002","861","533","717"], tail: 4, status: "verified", note: "Witness two: twelve signs, different from M-376 in every position except the ending. Copy-family collapse was tested and rejected: different plate, length, dimensions, boss, and pre-tail context." },
    { obj: "M-71",   site: "Mohenjo-daro", row: "strict row",     text: ["151","279","142","002","390","095"], status: "strict", note: "The one strict source-visible 095-closure row. A second witness would promote the branch." },
    { obj: "H-1993", site: "Harappa",      row: "744.2",          text: ["740","000","220","004","002","390","095"], status: "gated", note: "The would-be second 095 witness. Its plates sit in the purchase-gated CISI 3.1 volume." },
    { obj: "4237.1", site: "Dholavira",    row: "Acc. 8758",      text: ["151","032","388","002","390","705"], status: "gated", note: "A six-sign unicorn seal known from an OCR mirror, not yet bound to a photograph." },
    { obj: "M-1825", site: "Mohenjo-daro", row: "BJ25710",        text: ["157","031","002","390","705"], status: "gated", note: "Above the public plate range; the same gated supplement as H-1993 should hold it." },
    { obj: "3335.1", site: "unknown",      row: "no catalogue id", text: ["740","205","032","002","390","590","032"], status: "open", note: "Unprovenanced; an old note says only 'private collection'. Batch 041's lead: the CISI untraced-objects volumes." },
    { obj: "29 tablets", site: "Harappa", row: "register control", text: ["520","240","002","405","501"], status: "context", note: "The repeated Harappa tablet formula used as an adversarial control: 29 of 32 rows in its lane carry this exact text." }
  ];

  return {
    GLYPHS: GLYPHS, GLYPH_KEYS: GLYPH_KEYS,
    SITES: SITES, TRADE: TRADE,
    BRANCH: BRANCH, PUZZLE: PUZZLE, LEDGER: LEDGER,
    TIMELINE: TIMELINE, GRAVES: GRAVES, GRAVES_TOTAL: GRAVES_TOTAL, SEALS: SEALS
  };
})();
