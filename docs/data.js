/* =========================================================================
   IVC — data + custom artwork. Everything here is drawn or sourced by hand.
   - GLYPHS: original geometric line-art approximations of Indus signs
     (clean vector forms, not tracings, used as decorative iconography).
   - SITES: real archaeological sites, approximate coordinates.
   - BRANCH: the project's actual 002 sign-structure ecology.
   - PUZZLES: sequences built from the project's sign codes for the game.
   ========================================================================= */
window.IVC = (function () {

  /* ---- Custom Indus-style glyphs (viewBox 0 0 64 64, stroke art) ----- */
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

  /* ---- Archaeological sites (lon, lat) ------------------------------- */
  // Projection bounds chosen to frame Mesopotamia -> Indus together.
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
  var TRADE = ["mohenjo", "lothal", "failaka", "ur"]; // Meluhha trade arc

  /* ---- The 002 branch ecology (the real research object) ------------- */
  // x: column (0..4), y: lane. status: verified | gated | open | context | root
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
  // Each row is a sequence of sign codes. 533-717 only ever sits at the end.
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
    // which trailing pair is the terminal unit per row (for the reveal)
    tail: [ [2,3], [3,4], null, [4,5], null, [4,5] ]
  };

  /* ---- Scoreboard ledger (real accepted counts) ---------------------- */
  var LEDGER = [
    { n: 0, label: "Translations" },
    { n: 0, label: "Phonetic values" },
    { n: 0, label: "Sign meanings" },
    { n: 0, label: "Language identified" },
    { n: 0, label: "External anchors" },
    { n: 1, label: "Structural findings", verified: true }
  ];

  return {
    GLYPHS: GLYPHS, GLYPH_KEYS: GLYPH_KEYS,
    SITES: SITES, TRADE: TRADE,
    BRANCH: BRANCH, PUZZLE: PUZZLE, LEDGER: LEDGER
  };
})();
