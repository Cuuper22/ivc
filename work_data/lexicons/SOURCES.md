# Where each lexicon came from (downloaded 2026-11-17)

`raw/` = files exactly as downloaded (plain-text OCR from the Internet Archive, JSONL from kaikki.org, a CSV from Zenodo). `tsv/` = one table per language (headword TAB first gloss), written by `work_scripts/rival_lexicons.py`. `grammar/` = grammar pages used for the grammar table. Entry counts are what the parser kept, not what the book holds.

| file in raw/ | what it is | where from | used in the test |
|---|---|---|---|
| (DEDR, not stored here) | Burrow and Emeneau, Dravidian Etymological Dictionary 1984, Tamil side | dsal.uchicago.edu/dictionaries/burrow/ via `lang_dedr_fetch.py` into /tmp/dedr | yes, 3,015 entries |
| campbell_santali_english_1899.txt | A. Campbell, A Santali-English Dictionary, Pokhuria 1899 (Santali) | archive.org `asantalienglish00campgoog` (copy: `cu31924096339464`) | yes, 12,543 entries |
| santal_dict_v5_bodding.txt | P. O. Bodding, A Santal Dictionary vol. 5 (1936): the part from R on | archive.org `in.ernet.dli.2015.31960`; vols 1-4 and 6 not found open | yes, 2,065 entries |
| kaikki_santali.jsonl | Wiktionary Santali, as parsed by kaikki.org | kaikki.org/dictionary/Santali | yes, 1,016 entries |
| mundari_english_calcutta.txt | Bhadra, Mundari-English Dictionary, Calcutta University 1931 | archive.org `dli.calcutta.10338` (the 1983 edition `mundarienglishdi00bhad` is locked) | yes, 5,189 entries |
| encmund_v1,2,4,6,7,8,10.txt | J. Hoffmann, Encyclopaedia Mundarica, 7 of 10 volumes (Mundari) | archive.org `dli.bengal.10689.20982, 21001, 20996, 20084, 20088, 20080, 20997` | no: OCR is too broken to cut into entries |
| kharia_dict.txt | Dictionary of the Kharia language, English-Kharia 1934 | archive.org `dli.ministry.01715` (and `01714`) | no: English-to-Kharia direction only |
| zenodo_pmunda_cognates_127.csv | 127 Proto-Munda cognate sets | zenodo.org/records/3380874 | no: too small |
| werchikwar_english_lorimer1962.txt, werchikwar_ocr_all.txt | D. L. R. Lorimer, Werchikwar-English Vocabulary 1962 (Yasin Burushaski). The first file is the Archive's own OCR, which is unusable; the second is my own re-OCR of the scan (`work_scripts/rival_ocr_werchikwar.py`) | archive.org `werchikwar-english-vocubalry` | yes, 1,397 entries parsed out of the book's thousands |
| burushaski_barken.txt | Barken-Burushaski Dictionary 2023 (Hunza), only letters ba- to be- are in the file | archive.org `burushaski-barken-burushaski-dictionary` | yes, 429 entries, too few to test anything |
| burushaski_urdu_lughat_v1.txt | Burushaski-Urdu Lughat vol 1 | archive.org `burushaski-urdu-lughat-volume-1` | no: Urdu-script glosses |
| starling_burushaski_swadesh.pdf/.txt | Starling Swadesh lists, Yasin and Hunza Burushaski, from Berger 1974 and 1998 | starlingdb.org/new100/bur.pdf | used only to confirm the plain words for fish, man, tree |
| lorimer1935_burushaski_v1_intro.txt | Lorimer, The Burushaski Language vol 1 (intro) | archive.org `burushaski-language-v.-1-intro` | no (vol 3, the vocabulary, not found open) |
| sumerian_201604.txt | J. A. Halloran, Sumerian Lexicon v3.0 (English glosses) | archive.org `sumerian_202604` | yes, 4,519 entries |
| kaikki_sumerian.jsonl | Wiktionary Sumerian | kaikki.org/dictionary/Sumerian | yes, 1,598 entries |
| sumerian_mugsar.txt, delitzsch_sumerisches_glossar.txt, prince_materials_sumerian_lexicon.txt, sumerian_comparative2009.txt | Mugsar Sumerian dictionary, Delitzsch Sumerisches Glossar 1914, Prince Materials for a Sumerian Lexicon 1908, a Sumerian comparative dictionary | archive.org (`mugsar-annotated-...`, `sumerischesgloss00deliuoft`, `materialsforsume00prinuoft`, `sumeriancomparativedictionary2009`) | no: formats not cut into entries; Halloran carries the same glosses |
| elamisches_hinz_koch_1.txt, _2.txt | Hinz and Koch, Elamisches Woerterbuch 1987 (German glosses) | archive.org `Hinz-koch-1987-elamischesWorterbuch02-text_128` | yes, 2,550 entries |
| turner_cdial.txt | R. L. Turner, Comparative Dictionary of the Indo-Aryan Languages 1962-69 (Old Indo-Aryan headwords with glosses) | archive.org `turner-a-comparative-dictionary-of-the-indo-aryan-languages-1966-1969` | yes, 7,295 entries |
| (Monier-Williams, not stored here) | Monier-Williams Sanskrit-English Dictionary, XML already on disk (used by `lang_pun_chance_skt.py`) | evidence/tmp/.../ashtadhyayi/assets/mw.xml | yes, 277,409 sense lines |

Not reachable from this machine: ePSD2 / ORACC (oracc.museum.upenn.edu fails TLS through the proxy; its GitHub mirror returns 403). Not open anywhere I could find: Berger's Burushaski dictionaries, Hinz-Koch is the only Elamite dictionary, Pinnow's Kharia and the Munda etymological databases beyond the 127-set above.

`grammar/` holds Wikipedia wikitext pages (Santali, Ho, Mundari, Kharia, Munda languages, Burushaski, Sumerian, Elamite, Dravidian languages, Old Tamil, Proto-Dravidian, Vedic Sanskrit) and the Hunza Burushaski grammar sketch (archive.org `a-grammatical-sketch-of-hunza-burushaski`).
