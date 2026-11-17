# The Indus corpus in English

Note (2026-11-17): the English and Dravidian words here are working labels for each sign's job; two decoy tests (jobs/out/decoy_test.md) showed the exact words are not established. See FRAME.md for what is measured.

## Key (read this first)

- **A seal** is a small stone or clay stamp with a few signs cut in mirror image; **a tablet, tag, pot, rod** and the rest are other objects that carry signs. Each side of an object with signs is one **face**, and this book reads one face at a time (5,679 faces in the Lipi catalogue).
- **The template** is the shape most seals follow: [opener] [name] [ending]. The name is a crest (a house sign), a personal part and a tag, in that order; the jar sign ends a name with "house of"; a count comes before the thing it counts; a load tag is "n loads of produce, carried". A program (the template parser) gives every sign one of these slots, and the English is written from the slots by fixed rules (listed at the top of `work_scripts/corpus_build3.py`: slot words, count attachment by stroke style, spelled numbers inside names, measure words moved out of names as an allowance, one record per multi-face object), so the same signs always give the same English.
- **The sounds** are guesses at early Dravidian words, one per sign (`work_data/values_master4.csv`). Where a sign has no value, the English shows its number in square brackets, like [345].
- **Grades.** *whole*: every sign has a value we are building on (strict or wide) and nothing is lost. *part*: some signs read, the rest show as [number]. *damaged*: the face has a lost, unclear or broken sign. *none*: no sign has a value.
- **Strict and wide**: strict values were promoted on a fact nobody had seen while choosing the word, wide ones also on seen facts. A "whole" line here may use either.
- The English is a reading under working guesses, not a translation.

### Counts (strict values only: whole 2284 faces)

| grade | faces | share |
|---|---|---|
| whole | 2644 | 46.6% |
| part | 847 | 14.9% |
| damaged | 2079 | 36.6% |
| none | 109 | 1.9% |
| all | 5679 | |

Per site (faces):

| site | whole | part | damaged | none | all |
|---|---|---|---|---|---|
| Harappa | 1419 | 276 | 992 | 30 | 2717 |
| Mohenjo-daro | 894 | 416 | 555 | 58 | 1923 |
| Dholavira | 66 | 17 | 153 | 2 | 238 |
| Kalibangan | 53 | 36 | 115 | 8 | 212 |
| Lothal | 71 | 25 | 108 | 4 | 208 |
| Chanhu-daro | 25 | 16 | 32 | 1 | 74 |
| Nausharo | 16 | 12 | 10 | 0 | 38 |
| Unknown | 12 | 6 | 10 | 0 | 28 |
| Banawali | 11 | 4 | 9 | 2 | 26 |
| Lakhanjo-daro | 6 | 2 | 7 | 0 | 15 |
| Rakhigarhi | 4 | 1 | 8 | 0 | 13 |
| Allahdino | 4 | 3 | 5 | 0 | 12 |
| Kot-Diji | 3 | 0 | 8 | 0 | 11 |
| Kanmer | 5 | 1 | 4 | 0 | 10 |
| Karanpura | 6 | 0 | 1 | 1 | 8 |
| Shikarpur | 1 | 1 | 6 | 0 | 8 |
| Farmana | 4 | 1 | 3 | 0 | 8 |
| Bala-kot | 3 | 3 | 1 | 0 | 7 |
| Bhirrana | 3 | 2 | 1 | 0 | 6 |
| Gola Dhoro (Bagasra) | 2 | 3 | 1 | 0 | 6 |
| Surkotada | 2 | 0 | 4 | 0 | 6 |
| Ur | 0 | 2 | 3 | 0 | 5 |
| Nuhato | 2 | 0 | 3 | 0 | 5 |
| Rupar | 3 | 0 | 2 | 0 | 5 |
| Amri | 2 | 0 | 2 | 1 | 5 |
| Ra's al-Junayz | 1 | 0 | 3 | 0 | 4 |
| Rodji | 0 | 0 | 4 | 0 | 4 |
| Khirsara | 2 | 1 | 1 | 0 | 4 |
| Chandigarh | 0 | 1 | 2 | 0 | 3 |
| Desalpur | 1 | 2 | 0 | 0 | 3 |
| Karzakan | 2 | 0 | 1 | 0 | 3 |
| Naru-Waro-dharo | 0 | 0 | 3 | 0 | 3 |
| Tarkhanewala-dera | 2 | 0 | 0 | 1 | 3 |
| Alamgirpur | 1 | 2 | 0 | 0 | 3 |
| Daimabad | 1 | 0 | 1 | 0 | 2 |
| Rahman-deri | 2 | 0 | 0 | 0 | 2 |
| Nindowari-damb | 1 | 1 | 0 | 0 | 2 |
| Salut | 0 | 1 | 1 | 0 | 2 |
| Susa | 0 | 1 | 1 | 0 | 2 |
| Kish | 1 | 0 | 1 | 0 | 2 |
| Hissam-dheri | 1 | 0 | 1 | 0 | 2 |
| Ganweriwala | 0 | 1 | 1 | 0 | 2 |
| Miri Qalat | 2 | 0 | 0 | 0 | 2 |
| Gumla | 1 | 0 | 0 | 1 | 2 |
| Failaka | 0 | 0 | 2 | 0 | 2 |
| Rajanpur | 1 | 1 | 0 | 0 | 2 |
| Baror | 0 | 0 | 1 | 0 | 1 |
| Altyn Depe | 1 | 0 | 0 | 0 | 1 |
| Bakkar Buthi | 1 | 0 | 0 | 0 | 1 |
| Derawar Ther | 1 | 0 | 0 | 0 | 1 |
| Lohumjo-daro | 0 | 1 | 0 | 0 | 1 |
| Jhukar | 1 | 0 | 0 | 0 | 1 |
| Juna Khatiya | 0 | 0 | 1 | 0 | 1 |
| Hajar | 0 | 1 | 0 | 0 | 1 |
| Gharo Bhiro | 1 | 0 | 0 | 0 | 1 |
| Girsu | 0 | 0 | 1 | 0 | 1 |
| Gonur Depe | 0 | 1 | 0 | 0 | 1 |
| Kalba | 1 | 0 | 0 | 0 | 1 |
| Guddal A | 0 | 0 | 1 | 0 | 1 |
| Hulas | 1 | 0 | 0 | 0 | 1 |
| Janabiyah | 0 | 1 | 0 | 0 | 1 |
| Luristan | 1 | 0 | 0 | 0 | 1 |
| Rappwala Ther | 0 | 0 | 1 | 0 | 1 |
| Qala'at al-Bahrain | 0 | 1 | 0 | 0 | 1 |
| Pirak | 0 | 0 | 1 | 0 | 1 |
| Murda Sang | 0 | 0 | 1 | 0 | 1 |
| Nippur | 0 | 0 | 1 | 0 | 1 |
| Ornach area | 0 | 0 | 1 | 0 | 1 |
| Pabumath | 0 | 0 | 1 | 0 | 1 |
| Shortughai | 0 | 1 | 0 | 0 | 1 |
| Sibri | 0 | 0 | 1 | 0 | 1 |
| Saar | 0 | 1 | 0 | 0 | 1 |
| Tell Umma | 0 | 1 | 0 | 0 | 1 |
| Tepe Yahya | 0 | 0 | 1 | 0 | 1 |
| Tello | 0 | 0 | 1 | 0 | 1 |
| Tigrana | 0 | 0 | 1 | 0 | 1 |
| Wattoowala | 0 | 1 | 0 | 0 | 1 |

## Part 1. Every whole inscription (2644 faces, 1329 different sign strings)

### Harappa

**bangle** (3 faces)

- `840` *iṇai* : Pair.  (2 copies: 820.1, 1160.1)
- `790` *maṇi* : Gem.  (384.1)

**other** (16 faces)

- `033` *mū* : Three.  (3 copies: 802.1, 1167.1, 4137.1)
- `003` *mū* : Three.  (3947.1)
- `034-033` *nāl mū* : Seven.  (1059.1)
- `390` *parutti* : Cotton.  (4141.1)
- `400-031-384-156` *ciṟ oru aracu kā* : Junior-One-King, keeper.  (244.1)
- `550-060` *vāy -iṉ* : gate.  (236.1)
- `700` *nāḻi?* : Cup.  (428.1)
- `705-034` *kalam nāl* : Four kalam.  (609.1)
- `740` *kuṭi* : Of the house.  (224.1)
- `790` *maṇi* : Gem.  (5479.1)
- `840` *iṇai* : Pair.  (1163.1)
- `861-013-016-407` *kāṇi mū āṟu kiḷai* : three shares: Six kindreds.  (1164.1)
- `892` *vil* : Sale.  (4140.1)
- `904-003` *irutiṅkaḷ mū* : Three two months.  (4144.1)

**pot** (166 faces)

- `032` *iru* : Two.  (35 copies: 326.1, 328.1, 332.1, 333.1, 343.1, 346.1, 348.1, 357.1, 360.1, 363.1, 366.1, 367.1, 442.1, 444.1, 445.1, 493.1, 610.1, 615.1, 710.1, 714.1, 962.1, 965.1, 968.1, 970.1, 972.1, 973.1, 976.1, 977.1, 980.1, 982.1, 985.1, 987.1, 4101.1, 4106.1, 5399.1)
- `033` *mū* : Three.  (17 copies: 337.1, 347.1, 354.1, 359.1, 446.1, 612.1, 706.1, 721.1, 961.1, 997.1, 1392.1, 1865.1, 3937.1, 4102.1, 4104.1, 4105.1, 4135.1)
- `440` *koḷ* : Received.  (12 copies: 1008.1, 1009.1, 1016.1, 1031.1, 1033.1, 1037.1, 1039.1, 1045.1, 3955.1, 3956.1, 3957.1, 3958.1)
- `002` *iru* : Two.  (11 copies: 341.1, 342.1, 349.1, 350.1, 356.1, 529.1, 955.1, 967.1, 974.1, 975.1, 996.1)
- `004` *nāl* : Four.  (6 copies: 344.1, 353.1, 361.1, 953.1, 971.1, 986.1)
- `031` *oru* : One.  (6 copies: 331.1, 351.1, 352.1, 358.1, 443.1, 4107.1)
- `034` *nāl* : Four.  (6 copies: 334.1, 711.1, 728.2, 990.1, 3938.1, 4134.1)
- `700` *nāḻi?* : Cup.  (6 copies: 330.1, 614.1, 821.1, 993.1, 1036.1, 1048.1)
- `416` *turumpu* : Grain-heap.  (5 copies: 952.1, 1001.1, 1026.1, 1042.1, 1043.1)
- `001` *oru* : One.  (4 copies: 339.1, 340.1, 822.1, 988.1)
- `003` *mū* : Three.  (4 copies: 345.1, 712.1, 981.1, 983.1)
- `013` *mū* : Three.  (4 copies: 1038.1, 1040.1, 1041.1, 1044.1)
- `090` *āḷ* : Manager.  (3 copies: 179.1, 727.1, 4125.1)
- `033-220` *mū mīn* : Three Star.  (2 copies: 1017.1, 1032.1)
- `176-740` *iṟai kuṭi* : Of the Tax house.  (2 copies: 702.1, 719.1)
- `220` *mīn* : Star.  (2 copies: 984.1, 4108.1)
- `540` *paṟai* : Rice measure.  (2 copies: 3913.1, 4094.1)
- `540-540` *paṟai paṟai* : Two rice measures.  (2 copies: 1015.1, 1028.1)
- `700-033` *nāḻi? mū* : Three cups.  (2 copies: 701.1, 717.1)
- `740` *kuṭi* : Of the house.  (2 copies: 327.1, 4131.1)
- `001-033-415-175-740` *oru mū kavar iṟai kuṭi* : Of the Four-Branch-Tax house.  (718.1)
- `002-002` *iru iru* : Four.  (960.1)
- `003-002` *mū iru* : Five.  (1047.1)
- `005-031` *ai oru* : Six.  (1867.1)
- `006` *āṟu* : Six.  (3936.1)
- `016` *āṟu* : Six.  (3911.1)
- `016-220` *āṟu mīn* : Six Star.  (173.1)
- `031-003-480` *oru mū kuṉṟi* : Four seed-weights.  (4097.1)
- `031-413` *oru nel* : One grain.  (722.1)
- `031-697` *oru ney* : One woven.  (5461.1)
- `032-032-034` *iru iru nāl* : Eight.  (3934.1)
- `032-220` *iru mīn* : Two Star.  (3950.1)
- `033-235` *mū vēymīn* : Three Bamboo-star.  (176.1)
- `033-482` *mū kōṭukāṇi* : Three hill-shares.  (4124.1)
- `033-700` *mū nāḻi?* : Three cups.  (1391.1)
- `035` *ai* : Five.  (4727.1)
- `036-700` *āṟu nāḻi?* : Six cups.  (1390.1)
- `142-740` *kō kuṭi* : Of the King house.  (181.1)
- `151` *kā* : Keeper.  (1393.1)
- `156` *kā* : Keeper.  (182.1)
- `235-520` *vēymīn vēḷ* : Bamboo-star, chief.  (613.1)
- `382-220-016` *aracu mīn āṟu* : King; Six Star.  (715.1)
- `408-003` *kiḷai mū* : Three lots.  (625.1)
- `413` *nel* : Grain.  (440.1)
- `495-817` *kompu kāṇi* : Horn, share.  (700.1)
- `550` *vāy* : Gate.  (335.1)
- `590-697` *peṭṭi ney* : Chest, woven.  (193.1)
- `692` *kūṭṭam* : Assembly.  (201.1)
- `697-031` *ney oru* : One woven.  (969.1)
- `700-031` *nāḻi? oru* : One cup.  (3912.1)
- `817-002-491-692-100-740` *kāṇi iru kompu kūṭṭam mutu kuṭi* : two shares: of the Horn-Assembly-Elder house.  (1007.1)
- `820-798-740` *kāl maru- kuṭi* : quarter: of the Descendant house.  (288.1)
- `892` *vil* : Sale.  (4126.1)

**rod** (4 faces)

- `001-034-700` *oru nāl nāḻi?* : Five cups.  (434.1)
- `002-005-405` *iru ai nūl* : Seven threads.  (315.1)
- `031` *oru* : One.  (435.1)
- `455` *ampu* : Arrow.  (1165.1)

**seal** (174 faces)

- `033-700` *mū nāḻi?* : Three cups.  (3 copies: 1371.2, 1373.2, 1388.2)
- `468-806-154` *(n) viḷai kā* : N loads of produce, carried by the porter.  (3 copies: 1193.1, 1585.1, 1588.1)
- `003-140-100-740` *mū ammai mutu kuṭi* : Of the Three-Lady-Elder house.  (2 copies: 292.1, 1121.1)
- `003-156` *mū kā* : Three-keeper.  (2 copies: 1138.1, 1478.1)
- `003-390` *mū parutti* : Three cottons.  (2 copies: 464.1, 1539.1)
- `061-142-400-740` *kāl kō ciṟ kuṭi* : Of the Quarter-King-Junior house.  (2 copies: 929.1, 1441.1)
- `061-740` *kāl kuṭi* : Of the Quarter house.  (2 copies: 1128.1, 1497.1)
- `176-740-400` *iṟai kuṭi ciṟ* : Junior of the Tax house.  (2 copies: 1371.1, 1373.1)
- `861-002-032-070-590-390-740` *kāṇi iru iru ampu peṭṭi parutti kuṭi* : two shares: of the Two-Arrow-Boxed-cotton house.  (2 copies: 1540.1, 1540.2)
- `001-900-165-400-255-400` *oru tiṅkaḷ nāḷ ciṟ mutal ciṟ* : One-Moon-Day-Junior-Chief, junior.  (319.1)
- `003-220-740-090-400` *mū mīn kuṭi āḷ ciṟ* : Manager of the Three-Star house; Junior.  (237.1)
- `003-231-740` *mū orumīn kuṭi* : Of the Three-First-star house.  (1332.1)
- `003-405` *mū nūl* : Three threads.  (502.1)
- `003-550-617` *mū vāy ūḻiyaṉ* : Three gates; King's servant.  (1108.1)
- `004-407` *nāl kiḷai* : Four kindreds.  (1495.1)
- `005-900-740` *ai tiṅkaḷ kuṭi* : Of the Five-Moon house.  (1489.1)
- `013-840-740` *mū iṇai kuṭi* : Of the Three-Peer house.  (1188.1)
- `013-840-760-740` *mū iṇai maka kuṭi* : Of the Three-Peer-Child of house.  (1457.1)
- `016-220` *āṟu mīn* : Six Star.  (318.1)
- `016-390` *āṟu parutti* : Six cottons.  (1130.1)
- `017-090` *ēḻu āḷ* : Seven managers.  (1201.2)
- `017-220` *ēḻu mīn* : Seven Star.  (1070.1)
- `031-156` *oru kā* : One-keeper.  (1493.1)
- `031-240-740-090` *oru mīmīn kuṭi āḷ* : Manager of the One-High-star house.  (1430.1)
- `031-350-400-520` *oru kalappai ciṟ vēḷ* : One-Plough-Junior, chief.  (1501.1)
- `031-384-156-400` *oru aracu kā ciṟ* : One-King-Keeper, junior.  (1387.1)
- `031-388-740` *oru aracu kuṭi* : Of the One-King house.  (1858.1)
- `031-460-520` *oru mukkōṭu vēḷ* : One-Three-peaks, chief.  (1142.1)
- `031-467-806-154` *oru (n) viḷai kā* : One; N loads of produce, carried by the porter.  (1187.1)
- `031-501-861-368` *oru kumi kāṇi koṭi* : One-Throng-Tribute, standard-bearer.  (3916.1)
- `031-592` *oru paṭṭi* : One pen.  (1126.1)
- `031-706-033-520` *oru kalam mū vēḷ* : One lot of three kalam; Chief.  (1510.1)
- `032-220-233-717-740` *iru mīn vāḷai aṭi kuṭi* : Of the Two-Star-Scabbard-fish-Servant house.  (1544.1)
- `032-220-240-233-520` *iru mīn mīmīn vāḷai vēḷ* : Two-Star-High-star-Scabbard-fish, chief.  (920.1)
- `032-220-740` *iru mīn kuṭi* : Of the Two-Star house.  (1584.1)
- `032-220-740-090` *iru mīn kuṭi āḷ* : Manager of the Two-Star house.  (1480.1)
- `032-590-741-350-463-798-740` *iru peṭṭi orukuṭi kalappai mukkōṭu maru- kuṭi* : Of the Two-Chest-First-ward-Plough-Three-peaks-Descendant house.  (1492.1)
- `032-690-405` *iru piṇai nūl* : Two bounds; Thread.  (1102.1)
- `032-790-407` *iru maṇi kiḷai* : Two gems; Kindred.  (426.1)
- `032-877-740` *iru nālkāṇi kuṭi* : Of the Two-Four shares house.  (1533.1)
- `032-877-740-001-468-806-154` *iru nālkāṇi kuṭi oru (n) viḷai kā* : Of the Two-Four shares house; One; N loads of produce, carried by the porter.  (1087.1)
- `032-877-740-001-469-806-154` *iru nālkāṇi kuṭi oru (n) viḷai kā* : Of the Two-Four shares house; One; N loads of produce, carried by the porter.  (1184.1)
- `033` *mū* : Three.  (1386.2)
- `033-005-900-740` *mū ai tiṅkaḷ kuṭi* : Of the Eight-Moon house.  (1534.1)
- `033-061-142-400-740` *mū kāl kō ciṟ kuṭi* : Of the King-Junior house (allowance: three quarters).  (668.1)
- `033-617-003-154` *mū ūḻiyaṉ mū kā* : Three lots of three king's servants; Keeper.  (810.1)
- `034-700` *nāl nāḻi?* : Four cups.  (1858.2)
- `055-235-705-033-806-003-900-740` *paṉṉiru vēymīn kalam mū viḷai mū tiṅkaḷ kuṭi* : Of the Twelve-Bamboo-star-Bounty-Three-Moon house (allowance: three kalam).  (1085.1)
- `061-171-035-740-090` *kāl niṟai ai kuṭi āḷ* : Manager of the Quarter house (allowance: five full measures).  (1518.1)
- `104-004-405` *taṭṭāṉ nāl nūl* : Goldsmith; Four threads.  (430.1)
- `104-554-527` *taṭṭāṉ kaḷam kāval* : Goldsmith-Threshing-floor-Guard.  (1587.1)
- `125-406-741-590-406-740` *vēṭṭuvaṉ kiḷai orukuṭi peṭṭi kiḷai kuṭi* : Of the Hunter-Kindred-First-ward-Chest-Kindred house.  (1109.1)
- `125-861-002-004-390` *vēṭṭuvaṉ kāṇi iru nāl parutti* : Hunter; Six shares; Cotton.  (1114.1)
- `140-156` *ammai kā* : Lady, keeper.  (530.1)
- `140-527` *ammai kāval* : Lady-Guard.  (1483.1)
- `140-706-064` *ammai kalam pāti* : Lady-Ship-Portion.  (1194.1)
- `140-741-097-161` *ammai orukuṭi aṭimai kā* : Lady-First-ward-Bondsman-Keeper.  (775.1)
- `142-617` *kō ūḻiyaṉ* : King-King's servant.  (1131.1)
- `165-831-368-001-235-798-740` *nāḷ tiṉai koṭi oru vēymīn maru- kuṭi* : Of the Day-Millet-Banner-One-Bamboo-star-Descendant house.  (1099.1)
- `165-831-861-002-233-520` *nāḷ tiṉai kāṇi iru vāḷai vēḷ* : Day-Millet-Scabbard-fish, chief (allowance: two shares).  (1594.1)
- `175-520` *iṟai vēḷ* : Tax, chief.  (1481.1)
- `176-100-740` *iṟai mutu kuṭi* : Of the Tax-Elder house.  (306.1)
- `201-060-001-255-435-690-740` *kār -iṉ oru mutal kōl piṇai kuṭi* : Of the Rain-season-Inner-One-Chief-Rod-Ally house.  (1120.1)
- `201-060-240-233-520` *kār -iṉ mīmīn vāḷai vēḷ* : Rain-season-Inner-High-star-Scabbard-fish, chief.  (1077.1)
- `201-060-798-415-240-055-740-555-527` *kār -iṉ maru- kavar mīmīn paṉṉiru kuṭi vāy kāval* : Gate of the Rain-season-Inner-Descendant-Branch-High-star-Twelve house; Guard.  (1400.1)
- `231-151` *orumīn kā* : First-star, keeper.  (240.1)
- `235-231-752-740-468-806-158` *vēymīn orumīn maka kuṭi (n) viḷai kā* : Of the Bamboo-star child of First-star house; N loads of produce, carried by the porter.  (1117.1)
- `235-233-002-070-003-900-032-405` *vēymīn vāḷai iru ampu mū tiṅkaḷ iru nūl* : Bamboo-star-Scabbard-fish; Two lots of three arrows; Two months; Thread.  (1182.1)
- `235-240-520` *vēymīn mīmīn vēḷ* : Bamboo-star-High-star, chief.  (1189.1)
- `235-320-920-740` *vēymīn paṭi tiṅkaḷ? kuṭi* : Of the Bamboo-star-Ration measure-Month house.  (1105.1)
- `240-233-503` *mīmīn vāḷai malai* : High-star-Scabbard-fish-Hill.  (261.1)
- `240-921-070-520` *mīmīn vil ampu vēḷ* : High-star-Bow-Arrow, chief.  (1123.1)
- `321-405-002-806-233-320-920-740` *paṭi nūl iru viḷai vāḷai paṭi tiṅkaḷ? kuṭi* : Of the Ration-Thread-Two-Bounty-Scabbard-fish-Ration measure-Month house.  (1082.1)
- `370-031-745-013-840-740` *katir oru mukuṭi mū iṇai kuṭi* : Of the Spindle-One-Third-ward-Three-Peer house.  (885.1)
- `388-740` *aracu kuṭi* : Of the King house.  (1179.1)
- `416-002-003-798-740` *turumpu iru mū maru- kuṭi* : Of the Grain-heap-Five-Descendant house.  (1447.1)
- `416-740` *turumpu kuṭi* : Of the Grain-heap house.  (1462.1)
- `440-760-740` *koḷ maka kuṭi* : Of the child of Received house.  (1161.1)
- `468-806-154-400` *(n) viḷai kā ciṟ* : N loads of produce, carried by the porter; Junior.  (1201.1)
- `470-838-158` *(n) viḷai kā* : N loads of produce, carried by the porter.  (622.1)
- `482-752-740` *kōṭukāṇi maka kuṭi* : Of the child of Hill-share house.  (1106.1)
- `491-003-390` *kompu mū parutti* : Horn; Three cottons.  (1129.1)
- `503-615-154` *malai vayal kā* : Hill-Field, keeper.  (1198.1)
- `503-861-368` *malai kāṇi koṭi* : Hill-Tribute, standard-bearer.  (1180.1)
- `550-060-233-840-032-740` *vāy -iṉ vāḷai iṇai iru kuṭi* : gate: of the Scabbard-fish-Peer-Two house.  (1471.1)
- `550-060-240-740-679` *vāy -iṉ mīmīn kuṭi kaṭṭil* : gate: throne of the High-star house.  (1423.1)
- `550-060-806-032-220-255-435-690-176-740` *vāy -iṉ viḷai iru mīn mutal kōl piṇai iṟai kuṭi* : gate: of the Bounty-Two-Star-Chief-Rod-Ally-Tax house.  (1080.1)
- `550-740-632-595` *vāy kuṭi pal paṭṭaṟai* : Many of the Gate house; Forge.  (1560.1)
- `565-400` *maṟavaṉ ciṟ* : Warrior, junior.  (1154.1)
- `575-861-368` *kōṭṭai kāṇi koṭi* : Great measure-Tribute, standard-bearer.  (1448.1)
- `590-125-002-550-527` *peṭṭi vēṭṭuvaṉ iru vāy kāval* : Chest-Hunter; Two gates; Guard.  (1551.1)
- `590-390-151` *peṭṭi parutti kā* : Boxed-cotton, keeper.  (3924.1)
- `590-390-740-400` *peṭṭi parutti kuṭi ciṟ* : Junior of the Boxed-cotton house.  (1133.1)
- `590-405-740-001-472-806-154` *peṭṭi nūl kuṭi oru (n) viḷai kā* : Of the Chest-Thread house; One; N loads of produce, carried by the porter.  (1199.1)
- `590-892` *peṭṭi vil* : Chest-Sale.  (825.1)
- `617-440-745-176-740-232` *ūḻiyaṉ koḷ mukuṭi iṟai kuṭi kūṭumīn* : Cluster-star of the King's servant-Received-Third-ward-Tax house.  (1063.1)
- `617-742-803-798-415-220-055-482-740` *ūḻiyaṉ irukuṭi il maru- kavar mīn paṉṉiru kōṭukāṇi kuṭi* : Of the King's servant-Second-ward-Home-Descendant-Branch-Star-Twelve-Hill-share house.  (1294.1)
- `645-233` *kar̤añcu vāḷai* : Gold weight-Scabbard-fish.  (1553.1)
- `692-060-004-407` *kūṭṭam -iṉ nāl kiḷai* : Assembly: Four kindreds.  (1580.1)
- `692-060-176-740` *kūṭṭam -iṉ iṟai kuṭi* : Assembly: of the Tax house.  (1115.1)
- `692-060-798-240-220-520` *kūṭṭam -iṉ maru- mīmīn mīn vēḷ* : Assembly: Descendant-High-star-Star, chief.  (199.1)
- `692-060-798-240-231-904-740` *kūṭṭam -iṉ maru- mīmīn orumīn irutiṅkaḷ kuṭi* : Assembly: of the Descendant-High-star-First-star-Dark-moon house.  (939.1)
- `692-060-798-415-220-554-740` *kūṭṭam -iṉ maru- kavar mīn kaḷam kuṭi* : Assembly: of the Descendant-Branch-Star-Threshing-floor house.  (1174.1)
- `692-575-595-820` *kūṭṭam kōṭṭai paṭṭaṟai kāl* : Assembly-Great measure-Forge-Quarter.  (1062.1)
- `700` *nāḻi?* : The Measurer.  (1386.1)
- `700-031-153` *nāḻi? oru kā* : Measurer; One-keeper.  (3921.1)
- `700-741-033-904-740` *nāḻi? orukuṭi mū irutiṅkaḷ kuṭi* : The Measurer; Of the First-ward-Three-Dark-moon house.  (1496.1)
- `700-742-590-390-740` *nāḻi? irukuṭi peṭṭi parutti kuṭi* : The Measurer; Of the Second-ward-Boxed-cotton house.  (1444.1)
- `700-892` *nāḻi? vil* : The Measurer; Sale.  (1149.1)
- `706-033-520` *kalam mū vēḷ* : Chief (allowance: three kalam).  (1112.1)
- `717-100-740` *aṭi mutu kuṭi* : Of the Servant-Elder house.  (1122.1)
- `740-790` *kuṭi maṇi* : Gem of the house.  (1583.1)
- `741-390-741-031-705-033-368` *orukuṭi parutti orukuṭi oru kalam mū koṭi* : First-ward-Cotton-First-ward; One lot of three kalam; Banner.  (1388.1)
- `741-455-220-002-017-390` *orukuṭi ampu mīn iru ēḻu parutti* : First-ward-Arrow-Star; 9 cottons.  (1139.1)
- `790-590-405-740` *maṇi peṭṭi nūl kuṭi* : Of the Gem-Chest-Thread house.  (1467.1)
- `798-231-233-740-845-407-471-806-154` *maru- orumīn vāḷai kuṭi cūṭu kiḷai (n) viḷai kā* : Sheaf-bundle of the Descendant-First-star-Scabbard-fish house; Kindred; N loads of produce, carried by the porter.  (1173.1)
- `798-240-706-033-095-520` *maru- mīmīn kalam mū kōlaṉ vēḷ* : Descendant-High-star-Staff-bearer, chief (allowance: three kalam).  (1575.1)
- `803-156` *il kā* : Home, keeper.  (1097.1)
- `803-415-220-017-575-740` *il kavar mīn ēḻu kōṭṭai kuṭi* : Of the Home-Branch-Star house (allowance: seven great measures).  (1536.1)
- `803-415-231-706-033-520` *il kavar orumīn kalam mū vēḷ* : Home-Branch-First-star, chief (allowance: three kalam).  (322.1)
- `806-055-740` *viḷai paṉṉiru kuṭi* : Of the Bounty-Twelve house.  (205.1)
- `806-565` *viḷai maṟavaṉ* : Bounty-Warrior.  (1586.1)
- `806-740-061-405` *viḷai kuṭi kāl nūl* : Quarter of the Bounty house; Thread.  (1569.1)
- `817-002-003-390` *kāṇi iru mū parutti* : two shares: Three cottons.  (1412.1)
- `817-002-032-384-740` *kāṇi iru iru aracu kuṭi* : two shares: of the Two-King house.  (1181.1)
- `817-002-097-161` *kāṇi iru aṭimai kā* : two shares: Bondsman-Keeper.  (1204.1)
- `817-002-231-555-527` *kāṇi iru orumīn vāy kāval* : two shares: First-star-Gate-Guard.  (1449.1)
- `817-002-235-240-220-803-255-435-690-740` *kāṇi iru vēymīn mīmīn mīn il mutal kōl piṇai kuṭi* : two shares: of the Bamboo-star-High-star-Star-Home-Chief-Rod-Ally house.  (1073.1)
- `817-002-235-804` *kāṇi iru vēymīn ilai* : two shares: Bamboo-star-Leaf.  (1060.1)
- `817-002-235-840-032-740` *kāṇi iru vēymīn iṇai iru kuṭi* : two shares: of the Bamboo-star-Peer-Two house.  (3925.1)
- `817-002-503-615-760-740` *kāṇi iru malai vayal maka kuṭi* : two shares: of the Hill child of Field house.  (1074.1)
- `817-002-540-740` *kāṇi iru paṟai kuṭi* : two shares: of the Drum house.  (943.1)
- `817-002-803-233-520` *kāṇi iru il vāḷai vēḷ* : two shares: Home-Scabbard-fish, chief.  (1479.1)
- `817-002-806-231-706-033-520` *kāṇi iru viḷai orumīn kalam mū vēḷ* : two shares: Bounty-First-star, chief (allowance: three kalam).  (1401.1)
- `817-002-806-235-233-555-527-061-405` *kāṇi iru viḷai vēymīn vāḷai vāy kāval kāl nūl* : two shares: Bounty-Bamboo-star-Scabbard-fish-Gate-Guard-Quarter-Thread.  (1081.1)
- `817-013-467-806-154` *kāṇi mū (n) viḷai kā* : three shares: N loads of produce, carried by the porter.  (1195.1)
- `817-368-003-390` *kāṇi koṭi mū parutti* : share: Banner; Three cottons.  (1113.1)
- `820-001-240-440-740` *kāl oru mīmīn koḷ kuṭi* : one quarter: of the High-star-Received house.  (1415.1)
- `820-001-798-240-231-388-740` *kāl oru maru- mīmīn orumīn aracu kuṭi* : one quarter: of the Descendant-High-star-First-star-King house.  (1086.1)
- `820-002-003-390` *kāl iru mū parutti* : two quarters: Three cottons.  (634.1)
- `820-002-005-900-740` *kāl iru ai tiṅkaḷ kuṭi* : two quarters: of the Five-Moon house.  (246.1)
- `820-002-016-220-151` *kāl iru āṟu mīn kā* : two quarters: Six-Star, keeper.  (1491.1)
- `820-002-101-740-090` *kāl iru mutu kuṭi āḷ* : two quarters: manager of the Elder house.  (1104.1)
- `820-002-706-611-740` *kāl iru kalam kuṭai kuṭi* : two quarters: of the Ship-Umbrella house.  (3930.1)
- `820-002-806-240-233-705-033-520` *kāl iru viḷai mīmīn vāḷai kalam mū vēḷ* : two quarters: Bounty-High-star-Scabbard-fish, chief (allowance: three kalam).  (1564.1)
- `820-014-900-585-740` *kāl nāl tiṅkaḷ kaṉṉi? kuṭi* : four quarters: of the Moon-Maiden house.  (1459.1)
- `820-840-032-740` *kāl iṇai iru kuṭi* : quarter: of the Peer-Two house.  (1144.1)
- `824-002-240-033-033-760-740` *vilai iru mīmīn mū mū maka kuṭi* : worth two: of the High-star-Six-Child of house.  (731.1)
- `831-741-032-220-233-161` *tiṉai orukuṭi iru mīn vāḷai kā* : Millet-First-ward; Two Star; Scabbard-fish-Keeper.  (1416.1)
- `861-002-003-220-590-405-740` *kāṇi iru mū mīn peṭṭi nūl kuṭi* : two shares: of the Three-Star-Chest-Thread house.  (1175.1)
- `861-002-003-220-760-151` *kāṇi iru mū mīn maka kā* : two shares: Three-Star-Child of, keeper.  (303.1)
- `861-002-590-390-740` *kāṇi iru peṭṭi parutti kuṭi* : two shares: of the Boxed-cotton house.  (537.1)
- `861-002-798-320-920-017-575-740-400` *kāṇi iru maru- paṭi tiṅkaḷ? ēḻu kōṭṭai kuṭi ciṟ* : two shares: junior of the Descendant-Ration measure-Month-Seven-Great measure house.  (259.1)
- `861-002-806-231-773-740` *kāṇi iru viḷai orumīn maka kuṭi* : two shares: of the Bounty-First-star-Child of house.  (1176.1)
- `861-741` *kāṇi orukuṭi* : share: First-ward.  (1168.1)
- `861-741-240-630-740` *kāṇi orukuṭi mīmīn pal kuṭi* : share: of the First-ward-High-star-Many house.  (1168.2)
- `892-031-002-803-798-235-706-033-520` *vil oru iru il maru- vēymīn kalam mū vēḷ* : Sale-Three-Home-Descendant-Bamboo-star, chief (allowance: three kalam).  (1103.1)
- `920-060-415-220-520` *tiṅkaḷ? -iṉ kavar mīn vēḷ* : month: Branch-Star, chief.  (479.1)
- `920-060-741-240-232` *tiṅkaḷ? -iṉ orukuṭi mīmīn kūṭumīn* : month in first ward: High-star-Cluster-star.  (1145.1)
- `920-060-745-235-240-231-590-390-740` *tiṅkaḷ? -iṉ mukuṭi vēymīn mīmīn orumīn peṭṭi parutti kuṭi* : month in third ward: of the Bamboo-star-High-star-First-star-Boxed-cotton house.  (1098.1)
- `920-455-220-002-803-706-033-017-585-740` *tiṅkaḷ? ampu mīn iru il kalam mū ēḻu kaṉṉi? kuṭi* : Of the Month-Arrow-Star-Two-Home-Maiden house (allowance: 10 kalam).  (1293.1)
- `921-690-002-032-220-235-806-003-900-032-590-405-740` *vil piṇai iru iru mīn vēymīn viḷai mū tiṅkaḷ iru peṭṭi nūl kuṭi* : Of the Bow-Ally-Four-Star-Bamboo-star-Bounty-Three-Moon-Two-Chest-Thread house.  (1020.1)
- `923-740` *maruppu kuṭi* : Of the Ivory house.  (1092.1)

**tablet** (1054 faces)

- `033-700` *mū nāḻi?* : Three cups.  (120 copies: 212.1, 225.2, 260.1, 264.2, 268.1, 308.1, 395.1, 407.1, 414.1, 419.1, 425.1, 433.2, 458.1, 470.1, 487.1, 515.1, 544.1, 550.1, 560.1, 578.1, 593.1, 638.1, 672.1, 693.1, 732.1, 744.1, 751.1, 755.1, 758.2, 774.1, 863.1, 869.1, 917.1, 921.1, 930.1, 945.1, 1057.2, 1058.2, 1237.2, 1247.2, 1249.2, 1250.2, 1256.2, 1258.2, 1260.2, 1263.2, 1264.2, 1270.2, 1273.2, 1318.2, 1325.2, 1328.2, 1331.2, 1333.2, 1338.2, 1348.2, 1351.2, 1363.2, 1364.2, 1365.2, 1372.2, 1374.2, 1374.3, 1375.1, 1376.2, 1607.2, 1608.2, 1633.2, 1634.2, 1659.2, 1662.2, 1674.2, 1681.2, 1689.2, 1690.2, 1691.2, 1707.2, 1710.1, 1711.1, 1716.1, 1720.2, 1724.2, 1732.2, 1733.2, 1734.2, 1741.2, 1759.2, 1773.1, 1782.2, 1794.2, 1796.2, 1804.2, 1805.2, 1807.1, 1808.1, 1809.1, 1814.1, 1815.2, 1828.2, 1829.1, 1831.2, 1836.2, 1838.2, 1853.2, 1855.2, 1856.1, 1862.2, 1863.2, 3969.2, 4059.2, 4066.2, 4073.2, 4074.2, 4077.2, 4085.2, 4086.2, 4087.2, 4088.2, 4089.2, 5470.2)
- `034-700` *nāl nāḻi?* : Four cups.  (108 copies: 198.2, 222.3, 265.2, 274.2, 382.1, 388.1, 393.1, 394.1, 397.1, 406.1, 415.1, 418.1, 422.1, 424.1, 427.1, 467.1, 476.1, 480.1, 484.1, 506.1, 508.1, 509.1, 518.1, 621.2, 624.1, 637.1, 642.2, 646.1, 649.1, 659.1, 665.1, 686.1, 690.1, 740.2, 743.2, 752.1, 769.2, 772.1, 773.1, 780.1, 784.1, 794.1, 812.1, 814.2, 823.1, 827.1, 832.2, 844.1, 845.2, 846.2, 847.2, 850.1, 851.2, 852.1, 853.1, 854.2, 855.1, 856.2, 857.2, 858.2, 859.2, 860.2, 861.2, 862.1, 866.1, 870.1, 871.1, 878.1, 890.2, 895.2, 901.1, 1018.1, 1052.2, 1246.1, 1307.2, 1319.2, 1329.2, 1330.2, 1334.2, 1335.2, 1336.2, 1339.2, 1341.2, 1342.2, 1346.2, 1369.2, 1370.2, 1382.2, 1663.2, 1671.2, 1676.1, 1679.2, 1708.2, 1712.1, 1775.2, 1792.2, 1816.2, 1819.1, 1826.1, 1827.2, 1832.2, 1833.1, 1837.1, 1859.2, 1861.1, 3932.1, 3968.2, 4069.2)
- `032-700` *iru nāḻi?* : Two cups.  (87 copies: 229.2, 249.2, 255.1, 257.2, 270.2, 273.2, 280.2, 282.1, 313.2, 317.2, 371.1, 383.1, 386.1, 400.1, 411.1, 453.1, 477.1, 490.1, 497.1, 519.1, 548.1, 554.1, 567.1, 569.1, 596.1, 643.2, 652.1, 674.1, 679.1, 682.1, 749.1, 753.1, 765.1, 801.1, 829.1, 834.1, 841.2, 922.1, 927.1, 1021.2, 1061.2, 1240.2, 1244.2, 1245.2, 1248.2, 1257.2, 1259.2, 1276.2, 1337.2, 1344.2, 1349.2, 1361.2, 1362.2, 1380.2, 1381.2, 1602.2, 1620.2, 1658.2, 1660.2, 1669.1, 1675.2, 1687.2, 1693.2, 1703.2, 1704.1, 1719.2, 1723.2, 1738.1, 1740.2, 1760.2, 1806.2, 1810.2, 1823.2, 1824.2, 1839.2, 1840.2, 1842.2, 1843.2, 1845.1, 1846.1, 1852.2, 3959.2, 3973.2, 3982.2, 4068.1, 4072.2, 4081.2)
- `176-740-400` *iṟai kuṭi ciṟ* : Junior of the Tax house.  (36 copies: 260.2, 265.1, 267.1, 463.2, 585.1, 1260.1, 1330.1, 1331.1, 1334.1, 1335.1, 1336.1, 1337.1, 1338.1, 1339.1, 1372.1, 1374.1, 1375.2, 1376.1, 1812.1, 1813.2, 1814.2, 1815.1, 1816.1, 1817.1, 1837.2, 1839.1, 1855.1, 1856.2, 1863.3, 4073.1, 4077.1, 4085.1, 4086.1, 4087.1, 4088.1, 5470.1)
- `700-033` *nāḻi? mū* : Three cups.  (30 copies: 290.1, 316.2, 373.1, 377.1, 392.1, 410.1, 437.1, 456.1, 516.1, 598.1, 631.1, 675.1, 699.1, 864.1, 949.2, 1024.1, 1242.2, 1274.1, 1345.2, 1667.2, 1672.1, 1680.2, 1683.2, 1684.2, 1686.1, 1701.2, 1705.2, 1811.2, 1822.2, 1830.2)
- `003-861` *mū kāṇi* : Three shares.  (29 copies: 466.2, 693.2, 769.1, 794.2, 832.1, 838.2, 840.2, 844.2, 845.1, 846.1, 847.1, 850.2, 851.1, 852.2, 853.2, 854.1, 855.2, 856.1, 857.1, 858.1, 859.1, 860.1, 861.1, 870.2, 878.2, 892.1, 1801.1, 1802.1, 1803.1)
- `501-405-002-240-520` *kumi nūl iru mīmīn vēḷ* : Throng-Thread-Two-High-star, chief.  (29 copies: 1277.1, 1278.1, 1279.1, 1280.1, 1281.1, 1282.1, 1283.1, 1284.1, 1285.1, 1286.1, 1287.1, 1288.1, 1289.1, 1290.1, 1298.1, 1299.1, 1742.1, 1743.1, 1744.1, 1745.1, 1746.1, 1747.1, 1748.1, 1749.1, 1750.1, 1751.1, 1752.1, 1753.1, 4580.1)
- `003-156` *mū kā* : Three porters.  (22 copies: 693.3, 769.3, 832.3, 844.3, 845.3, 846.3, 847.3, 850.3, 851.3, 852.3, 853.3, 854.3, 855.3, 856.3, 857.3, 858.3, 859.3, 860.3, 861.3, 870.3, 878.3, 1310.1)
- `700-032` *nāḻi? iru* : Two cups.  (18 copies: 409.1, 504.1, 557.1, 570.1, 599.1, 923.1, 1049.2, 1243.2, 1343.2, 1378.2, 1668.1, 1670.1, 1685.2, 1702.2, 1706.2, 1725.1, 1735.2, 1736.2)
- `415-220-520` *kavar mīn vēḷ* : Branch-Star, chief.  (16 copies: 221.1, 481.1, 816.1, 841.1, 848.1, 913.1, 913.2, 1341.1, 1366.1, 1383.1, 1677.2, 1818.1, 1819.2, 1820.1, 1821.2, 4069.1)
- `700-034` *nāḻi? nāl* : Four cups.  (14 copies: 396.1, 468.1, 488.1, 549.1, 762.1, 815.1, 831.1, 938.1, 1377.2, 1739.2, 1774.2, 1813.1, 1818.2, 1825.2)
- `413-892-824` *nel vil vilai* : Grain, sale, price.  (11 copies: 295.1, 438.2, 459.1, 472.2, 556.1, 1323.1, 1677.1, 1678.1, 1787.1, 1788.1, 1864.1)
- `255-435-156-400` *mutal kōl kā ciṟ* : Chief-Rod-Keeper, junior.  (10 copies: 234.2, 390.2, 647.1, 671.2, 1321.2, 1377.1, 1653.1, 1778.2, 1779.2, 4052.1)
- `413-575-335-711-033-700` *nel kōṭṭai ūr vaḷḷam mū nāḻi?* : Grain, great measure, town, vaḷḷam measure; Three cups.  (10 copies: 300.2, 581.2, 653.2, 687.2, 689.2, 867.2, 916.2, 1236.2, 1665.2, 1666.2)
- `347-741-176-740-090` *kalai orukuṭi iṟai kuṭi āḷ* : Manager of the Stag-First-ward-Tax house.  (8 copies: 677.1, 800.1, 807.1, 842.1, 880.1, 882.1, 884.1, 886.1)
- `840-032-740` *iṇai iru kuṭi* : Of the Peer-Two house.  (8 copies: 535.1, 535.2, 694.1, 1215.1, 1215.2, 1328.1, 1625.1, 1715.2)
- `137-400` *vēḷāḷaṉ ciṟ* : Cultivator, junior.  (7 copies: 392.2, 598.2, 644.1, 830.2, 1246.2, 1853.1, 5396.1)
- `235-220-176-740` *vēymīn mīn iṟai kuṭi* : Of the Bamboo-star-Star-Tax house.  (7 copies: 729.1, 937.1, 1695.2, 1696.2, 1697.2, 3970.2, 3971.2)
- `806-235-590-405-740-400` *viḷai vēymīn peṭṭi nūl kuṭi ciṟ* : Junior of the Bounty-Bamboo-star-Chest-Thread house.  (7 copies: 1235.1, 1643.1, 1644.1, 1645.1, 1646.1, 1647.1, 3960.1)
- `861-002-240-482-740` *kāṇi iru mīmīn kōṭukāṇi kuṭi* : two shares: of the High-star-Hill-share house.  (7 copies: 729.2, 937.2, 1695.1, 1696.1, 1697.1, 3970.1, 3971.1)
- `416-861-002` *turumpu kāṇi iru* : Grain-heap; Two shares.  (6 copies: 476.2, 488.2, 518.2, 621.1, 665.2, 1792.1)
- `605-760-740-400` *kutir maka kuṭi ciṟ* : Junior of the child of Granary house.  (6 copies: 266.1, 1309.1, 1762.1, 1763.1, 1764.1, 1765.1)
- `742` *irukuṭi* : Second-ward house.  (6 copies: 3980.1, 3980.2, 3980.3, 4409.1, 4409.2, 4409.3)
- `817-368-690` *kāṇi koṭi piṇai* : share: Banner, bound.  (6 copies: 405.1, 1054.1, 1262.1, 1322.1, 3976.1, 4935.1)
- `027-032-740-400` *toṇṭu iru kuṭi ciṟ* : Junior of the Nine-Two house.  (5 copies: 549.2, 630.2, 659.2, 1325.1, 1797.2)
- `098-400` *ēvalaṉ ciṟ* : Attendant, junior.  (5 copies: 281.1, 520.1, 797.1, 1367.1, 4082.1)
- `240-482-752-740` *mīmīn kōṭukāṇi maka kuṭi* : Of the High-star child of Hill-share house.  (5 copies: 1023.1, 1230.1, 1231.1, 1232.1, 1637.2)
- `240-705-033-550-525-400` *mīmīn kalam mū vāy kāval ciṟ* : High-star-Gate-Guard, junior (allowance: three kalam).  (5 copies: 512.2, 635.1, 867.1, 916.1, 1666.1)
- `465-806-158` *(n) viḷai kā* : N loads of produce, carried by the porter.  (5 copies: 1223.1, 1626.1, 1628.1, 3965.1, 3966.1)
- `590-705-868` *peṭṭi kalam araikkāṇi* : Chest, half a kalam.  (5 copies: 234.1, 532.1, 647.2, 1778.1, 1781.1)
- `590-706-868` *peṭṭi kalam araikkāṇi* : Chest, half a kalam.  (5 copies: 390.1, 671.1, 1321.1, 1779.1, 4052.2)
- `617-892-740-400` *ūḻiyaṉ vil kuṭi ciṟ* : Junior of the King's servant-Sale house.  (5 copies: 681.1, 897.1, 1256.1, 1735.1, 1736.1)
- `900-368` *tiṅkaḷ koṭi* : Month, banner.  (5 copies: 732.2, 1329.1, 1807.2, 1808.2, 1809.2)
- `176-156` *iṟai kā* : Tax, keeper.  (4 copies: 772.2, 773.2, 890.1, 895.1)
- `220` *mīn* : Star.  (4 copies: 250.1, 553.2, 1767.1, 1850.1)
- `235-240-740-090` *vēymīn mīmīn kuṭi āḷ* : Manager of the Bamboo-star-High-star house.  (4 copies: 574.1, 666.1, 902.1, 904.1)
- `240-520` *mīmīn vēḷ* : High-star, chief.  (4 copies: 437.2, 515.2, 743.1, 1708.1)
- `004-700-220` *nāl nāḻi? mīn* : Four cups; Star.  (3 copies: 1324.1, 1793.2, 4056.2)
- `013-840-740` *mū iṇai kuṭi* : Of the Three-Peer house.  (3 copies: 1348.1, 1804.1, 1805.1)
- `033-033-520` *mū mū vēḷ* : Six chiefs.  (3 copies: 628.2, 831.2, 876.2)
- `061-255-740` *kāl mutal kuṭi* : Of the Quarter-Chief house.  (3 copies: 840.1, 1327.2, 1801.2)
- `090-400` *āḷ ciṟ* : Manager, junior.  (3 copies: 417.1, 1308.1, 4597.1)
- `125-700` *vēṭṭuvaṉ nāḻi?* : Hunter, cup.  (3 copies: 658.3, 1776.2, 4031.2)
- `140-001-031-740` *ammai oru oru kuṭi* : Of the Lady-Two house.  (3 copies: 371.2, 383.2, 400.2)
- `171-032-031-240-636-740-400` *niṟai iru oru mīmīn pal kuṭi ciṟ* : Junior of the High-star-Many house (allowance: three full measures).  (3 copies: 1323.2, 1787.2, 1864.2)
- `231-798-176-740` *orumīn maru- iṟai kuṭi* : Of the First-star-Descendant-Tax house.  (3 copies: 1206.1, 1604.1, 1605.1)
- `233-520-400` *vāḷai vēḷ ciṟ* : Scabbard-fish-Chief, junior.  (3 copies: 526.1, 1268.1, 1603.1)
- `240-590-390-740` *mīmīn peṭṭi parutti kuṭi* : Of the High-star-Boxed-cotton house.  (3 copies: 1057.1, 1226.1, 1633.1)
- `240-636-690-740` *mīmīn pal piṇai kuṭi* : Of the High-star-Many-Ally house.  (3 copies: 1058.1, 1842.1, 1843.1)
- `240-636-740-400` *mīmīn pal kuṭi ciṟ* : Junior of the High-star-Many house.  (3 copies: 1320.1, 1776.1, 4031.1)
- `240-760-740` *mīmīn maka kuṭi* : Of the child of High-star house.  (3 copies: 455.1, 469.1, 1785.1)
- `491-817-740-400` *kompu kāṇi kuṭi ciṟ* : Junior of the Horn-Share house.  (3 copies: 801.2, 1052.1, 1782.1)
- `503-016-740-400` *malai āṟu kuṭi ciṟ* : Junior of the Hill-Six house.  (3 copies: 737.1, 1614.1, 1615.1)
- `679-840-032-740` *kaṭṭil iṇai iru kuṭi* : Of the Throne-Peer-Two house.  (3 copies: 1262.2, 3976.2, 4935.2)
- `692-060-240-603-740` *kūṭṭam -iṉ mīmīn kūṭu kuṭi* : Assembly: of the High-star-Store house.  (3 copies: 198.1, 686.2, 3975.1)
- `705-167` *kalam kūli* : Kalam, wages.  (3 copies: 250.2, 377.2, 389.1)
- `706-167` *kalam kūli* : Kalam, wages.  (3 copies: 1010.1, 1035.1, 1227.2)
- `717-740-400` *aṭi kuṭi ciṟ* : Junior of the Servant house.  (3 copies: 427.2, 905.1, 1212.1)
- `745-700` *mukuṭi nāḻi?* : Third-ward house, cup.  (3 copies: 1023.2, 1637.1, 1639.2)
- `798-415-220-740-400` *maru- kavar mīn kuṭi ciṟ* : Junior of the Descendant-Branch-Star house.  (3 copies: 1234.1, 1641.1, 1659.1)
- `817-002` *kāṇi iru* : two shares.  (3 copies: 1314.1, 1315.1, 1769.1)
- `817-002-240-904-740` *kāṇi iru mīmīn irutiṅkaḷ kuṭi* : two shares: of the High-star-Dark-moon house.  (3 copies: 280.1, 1602.1, 3959.1)
- `820` *kāl* : quarter.  (3 copies: 663.1, 912.1, 4690.1)
- `003-154` *mū kā* : Three porters.  (2 copies: 794.3, 1385.1)
- `003-645-032-590` *mū kar̤añcu iru peṭṭi* : Three lots of two gold weights; Chest.  (2 copies: 848.2, 1821.1)
- `004-700` *nāl nāḻi?* : Four cups.  (2 copies: 510.1, 627.1)
- `016-220-520-400` *āṟu mīn vēḷ ciṟ* : Six-Star-Chief, junior.  (2 copies: 258.1, 1680.1)
- `031-520` *oru vēḷ* : One chief.  (2 copies: 1802.2, 1803.2)
- `032-001-904-031-740` *iru oru irutiṅkaḷ oru kuṭi* : Of the Three-Dark-moon-One house.  (2 copies: 228.1, 229.1)
- `033-142` *mū kō* : Three kings.  (2 copies: 1228.1, 1229.1)
- `033-590-416` *mū peṭṭi turumpu* : Three chests; Grain-heap.  (2 copies: 310.1, 786.2)
- `033-700-125` *mū nāḻi? vēṭṭuvaṉ* : Three cups; Hunter.  (2 copies: 498.1, 1271.2)
- `034` *nāl* : Four.  (2 copies: 879.1, 1269.2)
- `036-700` *āṟu nāḻi?* : Six cups.  (2 copies: 375.1, 1692.1)
- `091-368` *iruvar koṭi* : The pair, banner.  (2 copies: 654.2, 774.2)
- `140-061-740-400` *ammai kāl kuṭi ciṟ* : Junior of the Lady-Quarter house.  (2 copies: 382.2, 921.2)
- `171-035-415` *niṟai ai kavar* : Five full measures; Branch.  (2 copies: 1250.1, 1692.2)
- `175-176-100-740-400` *iṟai iṟai mutu kuṭi ciṟ* : Junior of the Tax-Tax-Elder house.  (2 copies: 494.1, 1636.1)
- `176-100-740` *iṟai mutu kuṭi* : Of the Tax-Elder house.  (2 copies: 1213.1, 3932.2)
- `176-336-740-400` *iṟai ūr kuṭi ciṟ* : Junior of the Tax-Town house.  (2 copies: 1362.1, 1774.1)
- `220-032-590-690` *mīn iru peṭṭi piṇai* : Star; Two chests; Bound.  (2 copies: 902.2, 904.2)
- `220-142-590-455` *mīn kō peṭṭi ampu* : Star, king, chest, arrow.  (2 copies: 491.1, 589.1)
- `220-440-154-400` *mīn koḷ kā ciṟ* : Star-Received-Keeper, junior.  (2 copies: 220.1, 1653.2)
- `220-520` *mīn vēḷ* : Star, chief.  (2 copies: 282.2, 1351.1)
- `220-550-526` *mīn vāy kāval* : Star, gate, guard.  (2 copies: 1364.1, 1378.1)
- `222-740-151` *aṭaimīn kuṭi kā* : Keeper of the Shut-in-fish house.  (2 copies: 508.2, 509.2)
- `226-400` *kūṭumīn ciṟ* : Fish-crate, junior.  (2 copies: 815.2, 1771.1)
- `231-176-740-565` *orumīn iṟai kuṭi maṟavaṉ* : Warrior of the First-star-Tax house.  (2 copies: 397.2, 418.2)
- `233-550-526` *vāḷai vāy kāval* : Scabbard-fish, gate, guard.  (2 copies: 945.2, 1845.2)
- `235-590-390-740` *vēymīn peṭṭi parutti kuṭi* : Of the Bamboo-star-Boxed-cotton house.  (2 copies: 1741.1, 3967.1)
- `240-100-740-400` *mīmīn mutu kuṭi ciṟ* : Junior of the High-star-Elder house.  (2 copies: 406.2, 1276.1)
- `240-176-740-400` *mīmīn iṟai kuṭi ciṟ* : Junior of the High-star-Tax house.  (2 copies: 746.1, 753.2)
- `240-904-740` *mīmīn irutiṅkaḷ kuṭi* : Of the High-star-Dark-moon house.  (2 copies: 316.1, 1672.2)
- `255-033` *mutal mū* : Three chiefs.  (2 copies: 162.2, 310.2)
- `255-435-690-740` *mutal kōl piṇai kuṭi* : Of the Chief-Rod-Ally house.  (2 copies: 516.2, 938.2)
- `413-575-335-711-033` *nel kōṭṭai ūr vaḷḷam mū* : Grain, great measure, town; Three vaḷḷam measures.  (2 copies: 561.2, 742.2)
- `413-575-335-740-032-700` *nel kōṭṭai ūr kuṭi iru nāḻi?* : Of the Grain-Great measure-Town house; Two cups.  (2 copies: 370.2, 1700.2)
- `415-100-740` *kavar mutu kuṭi* : Of the Branch-Elder house.  (2 copies: 459.2, 1733.3)
- `415-100-740-090-400` *kavar mutu kuṭi āḷ ciṟ* : Manager of the Branch-Elder house; Junior.  (2 copies: 811.1, 1221.1)
- `416-220-760-740-400` *turumpu mīn maka kuṭi ciṟ* : Junior of the Grain-heap child of Star house.  (2 copies: 1793.1, 4056.1)
- `440-100-740` *koḷ mutu kuṭi* : Of the Received-Elder house.  (2 copies: 1650.1, 1651.1)
- `472-806-158-400` *(n) viḷai kā ciṟ* : N loads of produce, carried by the porter; Junior.  (2 copies: 1239.1, 5462.1)
- `491-817-740` *kompu kāṇi kuṭi* : Of the Horn-Share house.  (2 copies: 453.2, 454.1)
- `503-017-740-400` *malai ēḻu kuṭi ciṟ* : Junior of the Hill-Seven house.  (2 copies: 730.1, 1208.1)
- `554-740` *kaḷam kuṭi* : Of the Threshing-floor house.  (2 copies: 248.1, 4139.1)
- `592-158-400` *paṭṭi kā ciṟ* : Pen-Keeper, junior.  (2 copies: 1823.1, 1824.1)
- `692-001-240-642-740` *kūṭṭam oru mīmīn pal kuṭi* : Of the Assembly-One-High-star-Many house.  (2 copies: 1710.2, 1711.2)
- `692-060-240-636-740` *kūṭṭam -iṉ mīmīn pal kuṭi* : Assembly: of the High-star-Many house.  (2 copies: 1379.2, 1712.2)
- `692-060-240-642-740` *kūṭṭam -iṉ mīmīn pal kuṭi* : Assembly: of the High-star-Many house.  (2 copies: 424.2, 1263.1)
- `697` *ney* : Woven.  (2 copies: 1656.1, 1657.2)
- `700-032-032` *nāḻi? iru iru* : Four cups.  (2 copies: 628.1, 876.1)
- `790-717-740` *maṇi aṭi kuṭi* : Of the Gem-Servant house.  (2 copies: 1656.2, 1657.1)
- `790-740-400` *maṇi kuṭi ciṟ* : Junior of the Gem house.  (2 copies: 1727.1, 3979.1)
- `792-740-090` *aracu kuṭi āḷ* : Manager of the Royal house.  (2 copies: 740.1, 752.2)
- `798-240-233-320-920-740-400` *maru- mīmīn vāḷai paṭi tiṅkaḷ? kuṭi ciṟ* : Junior of the Descendant-High-star-Scabbard-fish-Ration measure-Month house.  (2 copies: 569.2, 1273.1)
- `806-368-235-590-390-740` *viḷai koṭi vēymīn peṭṭi parutti kuṭi* : Of the Bounty-Banner-Bamboo-star-Boxed-cotton house.  (2 copies: 1599.1, 1600.1)
- `820-002-554-526` *kāl iru kaḷam kāval* : two quarters: Threshing-floor, guard.  (2 copies: 682.2, 1719.1)
- `831-892-400` *tiṉai vil ciṟ* : Millet-Sale, junior.  (2 copies: 249.1, 863.2)
- `850-740` *kāṇi kuṭi* : Of the Share house.  (2 copies: 3949.1, 3949.2)
- `001-100-700-032` *oru mutu nāḻi? iru* : One elder; Two cups.  (1227.3)
- `002-840-032-740` *iru iṇai iru kuṭi* : Of the Two-Peer-Two house.  (1786.1)
- `002-840-740` *iru iṇai kuṭi* : Of the Two-Peer house.  (1730.1)
- `003-335-740-400` *mū ūr kuṭi ciṟ* : Junior of the Three-Town house.  (1740.1)
- `003-390` *mū parutti* : Three cottons.  (489.1)
- `003-550-617` *mū vāy ūḻiyaṉ* : Three gates; King's servant.  (552.1)
- `003-700` *mū nāḻi?* : Three cups.  (670.1)
- `003-798-617` *mū maru- ūḻiyaṉ* : Three descendants; King's servant.  (1758.2)
- `004-220-700` *nāl mīn nāḻi?* : Four Star; Cup.  (311.2)
- `004-690` *nāl piṇai* : Four bounds.  (1350.1)
- `004-900-740` *nāl tiṅkaḷ kuṭi* : Of the Four-Moon house.  (1810.1)
- `005-405` *ai nūl* : Five threads.  (379.1)
- `013-060-032-740-400` *mū -iṉ iru kuṭi ciṟ* : Junior of the Three-within-Two house.  (1370.1)
- `013-840-740-400` *mū iṇai kuṭi ciṟ* : Junior of the Three-Peer house.  (1758.1)
- `014-032-740-400` *nāl iru kuṭi ciṟ* : Junior of the Six house.  (640.2)
- `014-700` *nāl nāḻi?* : Four cups.  (658.1)
- `015-032-740-400` *ai iru kuṭi ciṟ* : Junior of the Seven house.  (490.2)
- `015-460-798-740` *ai mukkōṭu maru- kuṭi* : Of the Five-Three-peaks-Descendant house.  (1630.1)
- `016-220-520` *āṟu mīn vēḷ* : Six-Star, chief.  (1822.1)
- `018-336-740` *eṭṭu ūr kuṭi* : Of the Eight-Town house.  (1707.1)
- `018-336-740-400` *eṭṭu ūr kuṭi ciṟ* : Junior of the Eight-Town house.  (1706.1)
- `031-101-740-090` *oru mutu kuṭi āḷ* : Manager of the One-Elder house.  (533.1)
- `031-384-156-400` *oru aracu kā ciṟ* : One-King-Keeper, junior.  (1346.1)
- `031-384-740` *oru aracu kuṭi* : Of the One-King house.  (422.2)
- `031-388-740` *oru aracu kuṭi* : Of the One-King house.  (559.1)
- `031-700` *oru nāḻi?* : One cup.  (461.1)
- `031-850-032` *oru kāṇi iru* : One lot of two shares.  (594.1)
- `031-861-003` *oru kāṇi mū* : One lot of three shares.  (1327.1)
- `032-140-156-400` *iru ammai kā ciṟ* : Two-Lady-Keeper, junior.  (264.1)
- `032-226` *iru kūṭumīn* : Two fish-crates.  (4090.1)
- `032-226-400` *iru kūṭumīn ciṟ* : Two-Fish-crate, junior.  (317.1)
- `032-255-740` *iru mutal kuṭi* : Of the Two-Chief house.  (643.1)
- `032-388-480-001` *iru aracu kuṉṟi oru* : Two King; One seed-weight.  (814.1)
- `032-388-480-031` *iru aracu kuṉṟi oru* : Two King; One seed-weight.  (866.2)
- `032-740-400` *iru kuṭi ciṟ* : Junior of the Two house.  (5389.1)
- `032-790-740` *iru maṇi kuṭi* : Of the Two-Gem house.  (930.2)
- `033-031-700` *mū oru nāḻi?* : Four cups.  (630.1)
- `033-033` *mū mū* : Six.  (1051.2)
- `033-255` *mū mutal* : Three chiefs.  (786.1)
- `033-384-740-400` *mū aracu kuṭi ciṟ* : Junior of the Three-King house.  (1681.1)
- `033-700-176-740-400` *mū nāḻi? iṟai kuṭi ciṟ* : Junior of the Tax house (allowance: three cups).  (1678.2)
- `034-390` *nāl parutti* : Four cottons.  (1356.1)
- `035-368` *ai koṭi* : Five banners.  (1701.1)
- `035-390` *ai parutti* : Five cottons.  (232.1)
- `055-255-435-690-740` *paṉṉiru mutal kōl piṇai kuṭi* : Of the Twelve-Chief-Rod-Ally house.  (570.2)
- `055-255-435-690-921-400` *paṉṉiru mutal kōl piṇai vil ciṟ* : Twelve-Chief-Rod-Ally-Bow, junior.  (1240.1)
- `061-142-400-740` *kāl kō ciṟ kuṭi* : Of the Quarter-King-Junior house.  (1671.1)
- `090-400-740-090-400` *āḷ ciṟ kuṭi āḷ ciṟ* : Manager of the Manager-Junior house; Junior.  (554.2)
- `090-700` *āḷ nāḻi?* : Manager, cup.  (1366.2)
- `091-368-033-700` *iruvar koṭi mū nāḻi?* : The pair, banner; Three cups.  (499.1)
- `097-151-400` *aṭimai kā ciṟ* : Bondsman-Keeper, junior.  (627.2)
- `097-400` *aṭimai ciṟ* : Bondsman, junior.  (637.2)
- `098` *ēvalaṉ* : Attendant.  (1675.1)
- `101-176-100-740` *mutu iṟai mutu kuṭi* : Of the Elder-Tax-Elder house.  (1241.1)
- `104-004-390` *taṭṭāṉ nāl parutti* : Goldsmith; Four cottons.  (1668.2)
- `137` *vēḷāḷaṉ* : Cultivator.  (642.1)
- `140-400` *ammai ciṟ* : Lady, junior.  (1725.2)
- `142-001` *kō oru* : One king.  (1266.1)
- `142-151-400` *kō kā ciṟ* : King-Keeper, junior.  (869.2)
- `142-617` *kō ūḻiyaṉ* : King, king's servant.  (1218.1)
- `156` *kā* : Keeper.  (470.2)
- `167-706` *kūli kalam* : Wages, kalam.  (808.1)
- `171-032-031-240-630-740` *niṟai iru oru mīmīn pal kuṭi* : Of the High-star-Many house (allowance: three full measures).  (405.2)
- `171-033-700-415` *niṟai mū nāḻi? kavar* : Full measure; Three cups; Branch.  (375.2)
- `175-482-335-740-400` *iṟai kōṭukāṇi ūr kuṭi ciṟ* : Junior of the Tax-Hill-share-Town house.  (1021.1)
- `175-817-740-400` *iṟai kāṇi kuṭi ciṟ* : Junior of the Tax-Share house.  (1051.1)
- `176-336-740` *iṟai ūr kuṭi* : Of the Tax-Town house.  (1249.1)
- `176-740` *iṟai kuṭi* : Of the Tax house.  (1601.1)
- `201-060-031-176-740` *kār -iṉ oru iṟai kuṭi* : Of the Rain-season-Inner-One-Tax house.  (646.2)
- `220-032-590` *mīn iru peṭṭi* : Star; Two chests.  (632.1)
- `220-032-700` *mīn iru nāḻi?* : Star; Two cups.  (485.1)
- `220-176-740` *mīn iṟai kuṭi* : Of the Star-Tax house.  (467.2)
- `220-240-740-090` *mīn mīmīn kuṭi āḷ* : Manager of the Star-High-star house.  (217.1)
- `220-550-525` *mīn vāy kāval* : Star, gate, guard.  (313.1)
- `220-705-033-550-525-400` *mīn kalam mū vāy kāval ciṟ* : Star-Gate-Guard, junior (allowance: three kalam).  (653.1)
- `220-740-090` *mīn kuṭi āḷ* : Manager of the Star house.  (4084.1)
- `231-390-100-740-090-400` *orumīn parutti mutu kuṭi āḷ ciṟ* : Manager of the First-star-Cotton-Elder house; Junior.  (578.2)
- `233-220` *vāḷai mīn* : Scabbard-fish, Star.  (416.1)
- `233-520` *vāḷai vēḷ* : Scabbard-fish, chief.  (1274.2)
- `233-550` *vāḷai vāy* : Scabbard-fish, gate.  (1682.2)
- `233-550-527` *vāḷai vāy kāval* : Scabbard-fish, gate, guard.  (1061.1)
- `235-176-740-400` *vēymīn iṟai kuṭi ciṟ* : Junior of the Bamboo-star-Tax house.  (423.1)
- `235-232-400` *vēymīn kūṭumīn ciṟ* : Bamboo-star-Cluster-star, junior.  (1685.1)
- `235-555-526` *vēymīn vāy kāval* : Bamboo-star, gate, guard.  (472.1)
- `235-705-033-176-740` *vēymīn kalam mū iṟai kuṭi* : Of the Bamboo-star-Tax house (allowance: three kalam).  (596.2)
- `235-717-741-400` *vēymīn aṭi orukuṭi ciṟ* : Bamboo-star-Servant-First-ward, junior.  (1350.2)
- `235-740-151` *vēymīn kuṭi kā* : Keeper of the Bamboo-star house.  (784.2)
- `235-923-740` *vēymīn maruppu kuṭi* : Of the Bamboo-star-Ivory house.  (675.2)
- `240-100-740` *mīmīn mutu kuṭi* : Of the High-star-Elder house.  (1345.1)
- `240-152-740-400` *mīmīn kā kuṭi ciṟ* : Junior of the High-star-Keeper house.  (806.2)
- `240-231-520-400` *mīmīn orumīn vēḷ ciṟ* : High-star-First-star-Chief, junior.  (1781.2)
- `240-233-520` *mīmīn vāḷai vēḷ* : High-star-Scabbard-fish, chief.  (297.1)
- `240-235-740-090` *mīmīn vēymīn kuṭi āḷ* : Manager of the High-star-Bamboo-star house.  (1834.1)
- `240-630-690-740` *mīmīn pal piṇai kuṭi* : Of the High-star-Many-Ally house.  (1343.1)
- `240-636-740` *mīmīn pal kuṭi* : Of the High-star-Many house.  (1799.2)
- `240-642-690-740` *mīmīn pal piṇai kuṭi* : Of the High-star-Many-Ally house.  (1369.1)
- `240-904-740-400` *mīmīn irutiṅkaḷ kuṭi ciṟ* : Junior of the High-star-Dark-moon house.  (410.2)
- `255-435-154` *mutal kōl kā* : Chief-Rod, keeper.  (274.1)
- `255-435-156` *mutal kōl kā* : Chief-Rod, keeper.  (1861.2)
- `382-740-400` *aracu kuṭi ciṟ* : Junior of the King house.  (273.1)
- `382-760-740` *aracu maka kuṭi* : Of the child of King house.  (1852.1)
- `382-760-740-400` *aracu maka kuṭi ciṟ* : Junior of the child of King house.  (480.2)
- `388-740-400` *aracu kuṭi ciṟ* : Junior of the King house.  (654.1)
- `388-740-400-033-700` *aracu kuṭi ciṟ mū nāḻi?* : Junior of the King house; Three cups.  (499.2)
- `390-032-700` *parutti iru nāḻi?* : Cotton; Two cups.  (1717.2)
- `390-155-004-390` *parutti kā nāl parutti* : Cotton, keeper; Four cottons.  (519.2)
- `413` *nel* : Grain.  (305.1)
- `413-137` *nel vēḷāḷaṉ* : Grain, cultivator.  (1018.2)
- `413-575-335-711-033-740` *nel kōṭṭai ūr vaḷḷam mū kuṭi* : Of the Grain-Great measure-Town house (allowance: three vaḷḷam measures).  (635.2)
- `415-100-820-032` *kavar mutu kāl iru* : Branch, elder; Two quarters.  (1690.1)
- `415-100-820-400` *kavar mutu kāl ciṟ* : Branch-Elder-Quarter, junior.  (1703.1)
- `415-240-495-463-752-740` *kavar mīmīn kompu mukkōṭu maka kuṭi* : Of the Branch-High-star-Horn child of Three-peaks house.  (601.2)
- `416-220-740-760-400` *turumpu mīn kuṭi maka ciṟ* : Child of of the Grain-heap-Star house; Junior.  (1324.2)
- `416-740` *turumpu kuṭi* : Of the Grain-heap house.  (892.2)
- `416-840-151` *turumpu iṇai kā* : Grain-heap-Peer, keeper.  (1662.1)
- `435-003-550` *kōl mū vāy* : Rod; Three gates.  (373.2)
- `440-740-400` *koḷ kuṭi ciṟ* : Junior of the Received house.  (790.1)
- `455-370` *ampu katir* : Arrow, spindle.  (1687.1)
- `455-740-400` *ampu kuṭi ciṟ* : Junior of the Arrow house.  (297.2)
- `467-806-154-400` *(n) viḷai kā ciṟ* : N loads of produce, carried by the porter; Junior.  (592.1)
- `467-806-158-740` *(n) viḷai kā kuṭi* : N loads of produce, carried by the porter; Of the house.  (1034.1)
- `470-806-158-400` *(n) viḷai kā ciṟ* : N loads of produce, carried by the porter; Junior.  (1222.1)
- `475-806-158-400` *(n) viḷai kā ciṟ* : N loads of produce, carried by the porter; Junior.  (745.1)
- `491-920-032` *kompu tiṅkaḷ? iru* : Horn; Two months.  (414.2)
- `495-463-740-400` *kompu mukkōṭu kuṭi ciṟ* : Junior of the Horn-Three-peaks house.  (1220.1)
- `495-776` *kompu malar* : Horn, bloom.  (235.1)
- `495-776-740-400` *kompu malar kuṭi ciṟ* : Junior of the Horn-Bloom house.  (1322.2)
- `519-176-740-400` *vēli iṟai kuṭi ciṟ* : Junior of the Fence-Tax house.  (550.2)
- `530-413` *paṟai nel* : Proclamation, grain.  (4138.1)
- `550-060-003-390` *vāy -iṉ mū parutti* : gate: Three cottons.  (374.2)
- `550-060-590-390-740` *vāy -iṉ peṭṭi parutti kuṭi* : gate: of the Boxed-cotton house.  (378.1)
- `550-060-705-255-740-090` *vāy -iṉ kalam mutal kuṭi āḷ* : gate: manager of the Ship-Chief house.  (788.1)
- `550-060-803-740` *vāy -iṉ il kuṭi* : gate: of the Home house.  (760.1)
- `550-525-400-034-700` *vāy kāval ciṟ nāl nāḻi?* : Gate-Guard, junior; Four cups.  (532.2)
- `554-525-400` *kaḷam kāval ciṟ* : Threshing-floor-Guard, junior.  (624.2)
- `590-390-740-400` *peṭṭi parutti kuṭi ciṟ* : Junior of the Boxed-cotton house.  (1705.1)
- `590-741-371-455-004-390` *peṭṭi orukuṭi katir ampu nāl parutti* : Chest, first-ward house, spindle, arrow; Four cottons.  (394.2)
- `690-154-400` *piṇai kā ciṟ* : Ally-Keeper, junior.  (780.2)
- `690-158-400` *piṇai kā ciṟ* : Ally-Keeper, junior.  (834.2)
- `692` *kūṭṭam* : Assembly.  (305.2)
- `692-060-061-760-740` *kūṭṭam -iṉ kāl maka kuṭi* : Assembly: of the child of Quarter house.  (664.1)
- `700` *nāḻi?* : Cup.  (580.1)
- `700-824` *nāḻi? vilai* : Cup, price.  (806.1)
- `705-031-100-740-400` *kalam oru mutu kuṭi ciṟ* : Junior of the Elder house (allowance: one kalam).  (1732.1)
- `705-630-175-100-740` *kalam pal iṟai mutu kuṭi* : Of the Ship-Many-Tax-Elder house.  (593.2)
- `705-717-388-740-400` *kalam aṭi aracu kuṭi ciṟ* : Junior of the Ship-Servant-King house.  (923.2)
- `706-630-336-151-400` *kalam pal ūr kā ciṟ* : Ship-Many-Town-Keeper, junior.  (1319.1)
- `717-415-100-090` *aṭi kavar mutu āḷ* : Servant-Branch-Elder, manager.  (420.1)
- `741-032-840-700` *orukuṭi iru iṇai nāḻi?* : First-ward house; Two pairs; Cup.  (829.2)
- `741-368-400` *orukuṭi koṭi ciṟ* : First-ward-Banner, junior.  (419.2)
- `741-530-390-002-803-798-740` *orukuṭi paṟai parutti iru il maru- kuṭi* : Of the First-ward-Proclamation-Cotton-Two-Home-Descendant house.  (1665.1)
- `790-003-550-617` *maṇi mū vāy ūḻiyaṉ* : Gem; Three gates; King's servant.  (662.1)
- `798-017-575-740-400` *maru- ēḻu kōṭṭai kuṭi ciṟ* : Junior of the Descendant house (allowance: seven great measures).  (749.2)
- `803-233-176-435-690-740` *il vāḷai iṟai kōl piṇai kuṭi* : Of the Home-Scabbard-fish-Tax-Rod-Ally house.  (631.2)
- `803-240-415-220-520` *il mīmīn kavar mīn vēḷ* : Home-High-star-Branch-Star, chief.  (485.2)
- `817-002-004-390` *kāṇi iru nāl parutti* : two shares: Four cottons.  (401.1)
- `817-002-031-706-151-033-700` *kāṇi iru oru kalam kā mū nāḻi?* : two shares: Keeper (allowance: one kalam); Three cups.  (1211.1)
- `817-002-495-615-740` *kāṇi iru kompu vayal kuṭi* : two shares: of the Horn-Field house.  (1724.1)
- `817-004-390` *kāṇi nāl parutti* : four shares: Cotton.  (1669.2)
- `817-013-004-405` *kāṇi mū nāl nūl* : three shares: Four threads.  (787.1)
- `817-368` *kāṇi koṭi* : share: Banner.  (1715.1)
- `817-368-645-900-033-700` *kāṇi koṭi kar̤añcu tiṅkaḷ mū nāḻi?* : share: Banner, gold weight, month; Three cups.  (1786.2)
- `817-368-690-032-700` *kāṇi koṭi piṇai iru nāḻi?* : share: Banner, bound; Two cups.  (463.1)
- `817-368-690-034-700` *kāṇi koṭi piṇai nāl nāḻi?* : share: Banner, bound; Four cups.  (1785.2)
- `820-002` *kāl iru* : two quarters.  (466.1)
- `820-002-104` *kāl iru taṭṭāṉ* : two quarters: Goldsmith.  (1269.1)
- `820-002-137` *kāl iru vēḷāḷaṉ* : two quarters: Cultivator.  (1607.1)
- `820-002-137-033-700` *kāl iru vēḷāḷaṉ mū nāḻi?* : two quarters: Cultivator; Three cups.  (1611.1)
- `820-002-240-220-520` *kāl iru mīmīn mīn vēḷ* : two quarters: High-star-Star, chief.  (1258.1)
- `820-002-382-760-382` *kāl iru aracu maka aracu* : two quarters: Child of King, king.  (448.1)
- `820-031-001-061-740` *kāl oru oru kāl kuṭi* : one quarter: of the house (allowance: one quarter).  (4059.1)
- `820-033` *kāl mū* : three quarters.  (447.1)
- `820-060-550-526` *kāl -iṉ vāy kāval* : quarter: Gate, guard.  (1619.1)
- `821-740` *mañcāṭi kuṭi* : Of the Mañcāṭi weight house.  (1210.1)
- `824-892-413` *vilai vil nel* : Price, sale, grain.  (887.2)
- `831-892` *tiṉai vil* : Millet, sale.  (1790.2)
- `840-032` *iṇai iru* : Two pairs.  (1219.1)
- `840-032-740-400` *iṇai iru kuṭi ciṟ* : Junior of the Peer-Two house.  (567.2)
- `850-741-048-740` *kāṇi orukuṭi er̤uvar kuṭi* : Of the Share-First-ward-Seven house.  (1236.1)
- `861-002-004-405` *kāṇi iru nāl nūl* : two shares: Four threads.  (1622.1)
- `861-002-004-407` *kāṇi iru nāl kiḷai* : two shares: Four kindreds.  (789.1)
- `861-002-031-892-803-740` *kāṇi iru oru vil il kuṭi* : two shares: of the One-Sale-Home house.  (1024.2)
- `861-002-035-405` *kāṇi iru ai nūl* : two shares: Five threads.  (409.2)
- `861-002-175-752-740` *kāṇi iru iṟai maka kuṭi* : two shares: of the child of Tax house.  (594.2)
- `861-002-470-806-154` *kāṇi iru (n) viḷai kā* : two shares: N loads of produce, carried by the porter.  (805.1)
- `861-002-920-817-408` *kāṇi iru tiṅkaḷ? kāṇi kiḷai* : two shares: Month, share, lot.  (771.2)
- `861-740-400` *kāṇi kuṭi ciṟ* : share: junior of the house.  (1728.1)
- `877-861-740` *nālkāṇi kāṇi kuṭi* : Of the Four shares-Tribute house.  (1363.1)
- `892-692` *vil kūṭṭam* : Sale, assembly.  (1382.3)
- `892-740` *vil kuṭi* : Of the Sale house.  (461.2)
- `900-165-480-031` *tiṅkaḷ nāḷ kuṉṟi oru* : Month, day; One seed-weight.  (1621.1)
- `904-705` *irutiṅkaḷ kalam* : Two months, kalam.  (1620.1)
- `920-017-575-740-400` *tiṅkaḷ? ēḻu kōṭṭai kuṭi ciṟ* : Junior of the Month-Seven-Great measure house.  (1318.1)
- `920-060-741-005-368-705-167` *tiṅkaḷ? -iṉ orukuṭi ai koṭi kalam kūli* : month in first ward: Five banners; Kalam, wages.  (1209.1)
- `920-060-741-176-156` *tiṅkaḷ? -iṉ orukuṭi iṟai kā* : month in first ward: Tax, keeper.  (257.1)

**tag or sealing** (2 faces)

- `803-233-032-904-740` *il vāḷai iru irutiṅkaḷ kuṭi* : Of the Home-Scabbard-fish-Two-Dark-moon house.  (1265.1)
- `861-370-240` *kāṇi katir mīmīn* : share: Spindle, High-star.  (941.1)

### Mohenjo-daro

**bangle** (23 faces)

- `840` *iṇai* : Pair.  (5 copies: 2358.1, 2383.1, 2494.1, 2496.1, 3835.1)
- `032` *iru* : Two.  (2 copies: 2502.1, 2503.1)
- `790` *maṇi* : Gem.  (2 copies: 2174.1, 3837.1)
- `002` *iru* : Two.  (2168.1)
- `002-064` *iru pāti* : Two portions.  (2170.1)
- `033` *mū* : Three.  (3832.2)
- `175-090-595-032-705` *iṟai āḷ paṭṭaṟai iru kalam* : Tax, manager; Two forges; Kalam.  (3823.1)
- `405` *nūl* : Thread.  (3834.1)
- `413-220-440` *nel mīn koḷ* : Grain, Star, received.  (3826.1)
- `500-706-064` *pāy kalam pāti* : Sail, kalam, portion.  (3827.1)
- `630-845` *pal cūṭu* : Many, sheaf-bundle.  (2187.1)
- `705-840` *kalam iṇai* : Kalam, pair.  (4032.1)
- `740` *kuṭi* : Of the house.  (3839.1)
- `820` *kāl* : quarter.  (3833.1)
- `831-585` *tiṉai kaṉṉi?* : Millet, maiden.  (2173.1)
- `850` *kāṇi* : Share.  (3838.1)
- `892-031` *vil oru* : One sale.  (5524.1)

**copper tablet** (153 faces)

- `503-615-752-740` *malai vayal maka kuṭi* : Of the Hill child of Field house.  (29 copies: 2275.1, 2308.1, 2458.1, 2520.1, 3023.1, 3024.1, 3025.1, 3026.1, 3027.1, 3028.1, 3029.1, 3030.1, 3031.1, 3032.1, 3033.1, 3034.1, 3035.1, 3036.1, 3037.1, 3760.1, 3761.1, 3762.1, 3763.1, 3764.1, 3765.1, 3766.1, 3767.1, 3768.1, 4025.1)
- `235-705-033-845-407-321-407` *vēymīn kalam mū cūṭu kiḷai paṭi kiḷai* : Bamboo-star; Three kalam; Sheaf-bundle, kindred, ration, kindred.  (14 copies: 3006.1, 3007.1, 3008.1, 3009.1, 3010.1, 3011.1, 3013.1, 3014.1, 3058.1, 3753.1, 3754.1, 3755.1, 3756.1, 3787.1)
- `806-845-061-407-850-900-740` *viḷai cūṭu kāl kiḷai kāṇi tiṅkaḷ kuṭi* : Of the Bounty-Sheaf-bundle-Quarter-Kindred-Share-Moon house.  (14 copies: 2287.2, 3052.1, 3053.1, 3054.1, 3055.1, 3056.1, 3057.1, 3063.2, 3065.1, 3784.1, 3785.1, 3786.1, 3796.2, 4029.1)
- `231-017-585-095-520-032-407` *orumīn ēḻu kaṉṉi? kōlaṉ vēḷ iru kiḷai* : First-star-Seven-Maiden-Staff-bearer, chief; Two kindreds.  (8 copies: 3019.1, 3020.1, 3021.1, 3791.1, 3792.1, 3793.1, 3794.1, 5587.1)
- `706-033-923-740` *kalam mū maruppu kuṭi* : Of the Ivory house (allowance: three kalam).  (7 copies: 3747.1, 3748.1, 3749.1, 3750.1, 3751.1, 3752.1, 4023.1)
- `798-240-845-061-407` *maru- mīmīn cūṭu kāl kiḷai* : Descendant, High-star, sheaf-bundle, quarter, kindred.  (6 copies: 3038.1, 3039.1, 3040.1, 3770.1, 3771.1, 3772.1)
- `017-585-388-740` *ēḻu kaṉṉi? aracu kuṭi* : Of the Seven-Maiden-King house.  (4 copies: 3048.1, 3050.1, 3051.1, 3783.1)
- `235-233-222-740` *vēymīn vāḷai aṭaimīn kuṭi* : Of the Bamboo-star-Scabbard-fish-Shut-in-fish house.  (4 copies: 3042.1, 3044.2, 3774.1, 3775.1)
- `415-220-845-407` *kavar mīn cūṭu kiḷai* : Branch, Star, sheaf-bundle, kindred.  (4 copies: 2983.1, 2984.1, 3733.1, 3734.1)
- `706-033-923-740-001` *kalam mū maruppu kuṭi oru* : Of the Ivory house (allowance: three kalam); One.  (4 copies: 3001.1, 3002.1, 3003.1, 3004.1)
- `003-421-176-100-740-790` *mū par̤aṉam iṟai mutu kuṭi maṇi* : Gem of the Three-Field-Tax-Elder house.  (3 copies: 3015.1, 3016.1, 3017.1)
- `005-706` *ai kalam* : Five kalam.  (3 copies: 2989.1, 2990.1, 2991.1)
- `233-585-407` *vāḷai kaṉṉi? kiḷai* : Scabbard-fish, maiden, kindred.  (3 copies: 2989.2, 2990.2, 2991.2)
- `255-435-690-740-900-003-422` *mutal kōl piṇai kuṭi tiṅkaḷ mū par̤aṉam* : Month of the Chief-Rod-Ally house; Three fields.  (3 copies: 3742.1, 3745.1, 3746.1)
- `503-615-740` *malai vayal kuṭi* : Of the Hill-Field house.  (3 copies: 2522.1, 2992.2, 2993.2)
- `806-233-384-740` *viḷai vāḷai aracu kuṭi* : Of the Bounty-Scabbard-fish-King house.  (3 copies: 2981.1, 3059.2, 3790.1)
- `806-235-233-705-033-585-407` *viḷai vēymīn vāḷai kalam mū kaṉṉi? kiḷai* : Produce, Bamboo-star, Scabbard-fish; Three kalam; Maiden, kindred.  (3 copies: 2523.1, 3776.1, 3777.1)
- `900-165` *tiṅkaḷ nāḷ* : Month, day.  (3 copies: 2985.1, 2986.1, 3735.2)
- `003-422-176-100-740` *mū par̤aṉam iṟai mutu kuṭi* : Of the Three-Field-Tax-Elder house.  (2 copies: 3757.1, 3759.1)
- `003-700-900-165` *mū nāḻi? tiṅkaḷ nāḷ* : Three cups; Month, day.  (2 copies: 2987.1, 2988.1)
- `032-220-176-740` *iru mīn iṟai kuṭi* : Of the Two-Star-Tax house.  (2 copies: 2987.2, 2988.2)
- `231-255-435-690-740` *orumīn mutal kōl piṇai kuṭi* : Of the First-star-Chief-Rod-Ally house.  (2 copies: 2465.1, 3788.1)
- `798-231-705-033-904-100-740` *maru- orumīn kalam mū irutiṅkaḷ mutu kuṭi* : Of the Descendant-First-star-Dark-moon-Elder house (allowance: three kalam).  (2 copies: 3067.2, 3797.2)
- `806-233-176-740` *viḷai vāḷai iṟai kuṭi* : Of the Bounty-Scabbard-fish-Tax house.  (2 copies: 2980.1, 3728.1)
- `003-220-590-405-740` *mū mīn peṭṭi nūl kuṭi* : Of the Three-Star-Chest-Thread house.  (3066.2)
- `003-233-100-740` *mū vāḷai mutu kuṭi* : Of the Three-Scabbard-fish-Elder house.  (3022.1)
- `003-422` *mū par̤aṉam* : Three fields.  (2488.1)
- `032-220-773-740` *iru mīn maka kuṭi* : Of the Two-Star-Child of house.  (3041.1)
- `035` *ai* : Five.  (3737.1)
- `142-617-001-004-407` *kō ūḻiyaṉ oru nāl kiḷai* : King, king's servant; Five kindreds.  (3735.1)
- `220-017-585-095-520-032-407` *mīn ēḻu kaṉṉi? kōlaṉ vēḷ iru kiḷai* : Star-Seven-Maiden-Staff-bearer, chief; Two kindreds.  (2284.2)
- `220-017-585-095-520-032-408` *mīn ēḻu kaṉṉi? kōlaṉ vēḷ iru kiḷai* : Star-Seven-Maiden-Staff-bearer, chief; Two lots.  (3061.2)
- `233-798-740` *vāḷai maru- kuṭi* : Of the Scabbard-fish-Descendant house.  (3736.1)
- `235-220-222-740` *vēymīn mīn aṭaimīn kuṭi* : Of the Bamboo-star-Star-Shut-in-fish house.  (3773.1)
- `255-435-690-740-900-001-003-423` *mutal kōl piṇai kuṭi tiṅkaḷ oru mū par̤aṉam* : Month of the Chief-Rod-Ally house; Four fields.  (3000.1)
- `255-435-690-740-900-001-003-424` *mutal kōl piṇai kuṭi tiṅkaḷ oru mū par̤aṉam* : Of the Chief-Rod-Ally house; Four months; Field.  (3741.1)
- `590-405-100-740-790` *peṭṭi nūl mutu kuṭi maṇi* : Gem of the Chest-Thread-Elder house.  (3734.2)
- `590-407-740` *peṭṭi kiḷai kuṭi* : Of the Chest-Kindred house.  (3730.2)
- `705-033-923-740-001` *kalam mū maruppu kuṭi oru* : Of the Ivory house (allowance: three kalam); One.  (2488.2)
- `752-740` *maka kuṭi* : Of the Child of house.  (2525.1)
- `773-740` *maka kuṭi* : Of the Child of house.  (3737.2)
- `806-231-176-740` *viḷai orumīn iṟai kuṭi* : Of the Bounty-First-star-Tax house.  (3730.1)
- `806-845-407-850-900-740` *viḷai cūṭu kiḷai kāṇi tiṅkaḷ kuṭi* : Of the Bounty-Sheaf-bundle-Kindred-Share-Moon house.  (3064.1)
- `831-233-176-740` *tiṉai vāḷai iṟai kuṭi* : Of the Millet-Scabbard-fish-Tax house.  (3727.1)
- `831-590-125-407-002` *tiṉai peṭṭi vēṭṭuvaṉ kiḷai iru* : Millet, chest, hunter; Two kindreds.  (4030.1)
- `861-368-001-142-617` *kāṇi koṭi oru kō ūḻiyaṉ* : share: Banner; One king; King's servant.  (3044.1)
- `904-032-904` *irutiṅkaḷ iru irutiṅkaḷ* : Two months; Two two months.  (3798.1)

**other** (5 faces)

- `031-156` *oru kā* : One porter.  (2 copies: 3566.1, 3566.2)
- `031-100-740` *oru mutu kuṭi* : Of the One-Elder house.  (3843.1)
- `032-840` *iru iṇai* : Two pairs.  (3071.1)
- `900-165` *tiṅkaḷ nāḷ* : Month, day.  (3844.1)

**pot** (30 faces)

- `033-151` *mū kā* : Three porters.  (2 copies: 3820.1, 3820.2)
- `370-002-550-527` *katir iru vāy kāval* : Two spindles; Gate, guard.  (2 copies: 3670.1, 3677.1)
- `792-740` *aracu kuṭi* : Of the Royal house.  (2 copies: 2918.1, 3678.1)
- `005-740` *ai kuṭi* : Of the Five house.  (2155.1)
- `012-165` *iru nāḷ* : Two days.  (2156.1)
- `032` *iru* : Two.  (3809.1)
- `032-158` *iru kā* : Two porters.  (2209.1)
- `033` *mū* : Three.  (3808.1)
- `034` *nāl* : Four.  (3807.1)
- `101-154` *mutu kā* : Elder, keeper.  (3671.1)
- `136` *aṭimai* : Bondsman.  (3819.1)
- `155-033` *kā mū* : Three porters.  (5395.1)
- `171-035` *niṟai ai* : Five full measures.  (2159.1)
- `226` *kūṭumīn* : Fish-crate.  (3716.1)
- `226-031-740` *kūṭumīn oru kuṭi* : Of the Fish-crate-One house.  (3801.1)
- `320-920-740` *paṭi tiṅkaḷ? kuṭi* : Of the Ration measure-Month house.  (3815.1)
- `415-900-158` *kavar tiṅkaḷ kā* : Branch-Moon, keeper.  (2203.1)
- `424-740` *par̤aṉam kuṭi* : Of the Field house.  (5527.1)
- `480-142-740` *kuṉṟi kō kuṭi* : Of the Seed-weight-King house.  (2162.1)
- `540` *paṟai* : Rice measure.  (5513.1)
- `615-033-104` *vayal mū taṭṭāṉ* : Three fields; Goldsmith.  (3813.1)
- `700-031` *nāḻi? oru* : One cup.  (3810.1)
- `705-033-032-790` *kalam mū iru maṇi* : Five kalam; Gem.  (3673.1)
- `740` *kuṭi* : Of the house.  (3811.1)
- `790-153` *maṇi kā* : Gem, porter.  (5519.1)
- `861-002-176-740` *kāṇi iru iṟai kuṭi* : two shares: of the Tax house.  (2165.2)
- `920-540-740` *tiṅkaḷ? paṟai kuṭi* : Of the Month-Drum house.  (3675.1)

**rod** (12 faces)

- `240-013-840-740-400` *mīmīn mū iṇai kuṭi ciṟ* : Junior of the High-star-Three-Peer house.  (2 copies: 2467.1, 2474.1)
- `240-838-585-740-400` *mīmīn viḷai kaṉṉi? kuṭi ciṟ* : Junior of the High-star-Produce-Maiden house.  (2 copies: 2394.1, 3841.1)
- `838-482-740` *viḷai kōṭukāṇi kuṭi* : Of the Produce-Hill-share house.  (2 copies: 4033.1, 4040.1)
- `031-645-645-031` *oru kar̤añcu kar̤añcu oru* : One gold weight; One gold weight.  (3842.1)
- `034-700-097-151` *nāl nāḻi? aṭimai kā* : Bondsman, keeper (allowance: four cups).  (2527.1)
- `140-176-740-400` *ammai iṟai kuṭi ciṟ* : Junior of the Lady-Tax house.  (2356.1)
- `176-740-400` *iṟai kuṭi ciṟ* : Junior of the Tax house.  (4036.1)
- `390-390-390` *parutti parutti parutti* : Three cottons.  (5533.1)
- `690-435-760-740-400` *piṇai kōl maka kuṭi ciṟ* : Junior of the Ally child of Rod house.  (2210.1)

**seal** (582 faces)

- `016-390` *āṟu parutti* : Six cottons.  (5 copies: 2353.1, 2704.1, 3235.1, 3380.1, 3664.1)
- `003-156` *mū kā* : Three-keeper.  (4 copies: 2307.1, 3250.1, 3316.1, 3564.1)
- `031-156` *oru kā* : One-keeper.  (4 copies: 2325.1, 2713.1, 2753.1, 3387.1)
- `003-220-740` *mū mīn kuṭi* : Of the Three-Star house.  (3 copies: 2814.1, 3722.1, 3724.1)
- `005-900-740` *ai tiṅkaḷ kuṭi* : Of the Five-Moon house.  (3 copies: 2665.1, 3667.1, 3996.1)
- `176-740` *iṟai kuṭi* : Of the Tax house.  (3 copies: 2259.1, 2820.1, 3546.1)
- `240-520` *mīmīn vēḷ* : High-star, chief.  (3 copies: 2711.1, 2732.1, 3098.1)
- `003-390` *mū parutti* : Three cottons.  (2 copies: 2191.1, 2705.1)
- `005-156` *ai kā* : Five-keeper.  (2 copies: 2712.1, 2718.1)
- `005-405` *ai nūl* : Five threads.  (2 copies: 2748.1, 2900.1)
- `013-840-740` *mū iṇai kuṭi* : Of the Three-Peer house.  (2 copies: 2452.1, 2479.1)
- `061-151` *kāl kā* : Quarter, keeper.  (2 copies: 2372.1, 2726.1)
- `097-151` *aṭimai kā* : Bondsman, keeper.  (2 copies: 2273.1, 2328.1)
- `220-520` *mīn vēḷ* : Star, chief.  (2 copies: 2710.1, 3371.1)
- `233-520` *vāḷai vēḷ* : Scabbard-fish, chief.  (2 copies: 2262.1, 2426.1)
- `235-798-740` *vēymīn maru- kuṭi* : Of the Bamboo-star-Descendant house.  (2 copies: 2194.1, 2266.1)
- `255-435-690-740` *mutal kōl piṇai kuṭi* : Of the Chief-Rod-Ally house.  (2 copies: 3269.1, 3345.1)
- `416-151` *turumpu kā* : Grain-heap, keeper.  (2 copies: 3165.1, 3558.1)
- `416-740` *turumpu kuṭi* : Of the Grain-heap house.  (2 copies: 3333.1, 3845.1)
- `519-740` *vēli kuṭi* : Of the Fence house.  (2 copies: 2787.1, 2884.1)
- `550-527` *vāy kāval* : Gate-Guard.  (2 copies: 2253.1, 3334.1)
- `705-033-520` *kalam mū vēḷ* : Chief (allowance: three kalam).  (2 copies: 2649.1, 3658.1)
- `706` *kalam* : Ship.  (2 copies: 2163.1, 3553.1)
- `803-740` *il kuṭi* : Of the Home house.  (2 copies: 2514.1, 3370.1)
- `817-002-004-390` *kāṇi iru nāl parutti* : two shares: Four cottons.  (2 copies: 2418.1, 2453.1)
- `817-002-005-390` *kāṇi iru ai parutti* : two shares: Five cottons.  (2 copies: 2397.1, 3217.1)
- `817-002-061-740` *kāṇi iru kāl kuṭi* : two shares: of the Quarter house.  (2 copies: 2729.1, 3236.1)
- `820-002-003-390` *kāl iru mū parutti* : two quarters: Three cottons.  (2 copies: 2386.1, 3990.1)
- `861-002-003-390` *kāṇi iru mū parutti* : two shares: Three cottons.  (2 copies: 2228.1, 3137.1)
- `861-002-415-100-740` *kāṇi iru kavar mutu kuṭi* : two shares: of the Branch-Elder house.  (2 copies: 3262.1, 3279.1)
- `920-060-741-592` *tiṅkaḷ? -iṉ orukuṭi paṭṭi* : month in first ward: Pen.  (2 copies: 2343.1, 3266.1)
- `001-220-140-416-031-565` *oru mīn ammai turumpu oru maṟavaṉ* : One Star; Lady-Grain-heap; One warrior.  (2332.1)
- `002-140-226` *iru ammai kūṭumīn* : Two ladies; Fish-crate.  (3185.1)
- `002-850-700-033` *iru kāṇi nāḻi? mū* : Two shares; Three cups.  (3565.5)
- `003` *mū* : Three.  (2849.4)
- `003-001-435` *mū oru kōl* : Four rods.  (3548.1)
- `003-003` *mū mū* : Six.  (2387.1)
- `003-140-100-740` *mū ammai mutu kuṭi* : Of the Three-Lady-Elder house.  (3479.1)
- `003-140-100-740-400` *mū ammai mutu kuṭi ciṟ* : Junior of the Three-Lady-Elder house.  (2411.1)
- `003-158-400` *mū kā ciṟ* : Three-keeper, junior.  (2288.1)
- `003-220-520` *mū mīn vēḷ* : Three-Star, chief.  (2441.1)
- `003-220-590-390-740` *mū mīn peṭṭi parutti kuṭi* : Of the Three-Star-Boxed-cotton house.  (2621.1)
- `003-407` *mū kiḷai* : Three kindreds.  (2205.1)
- `003-550-031-031` *mū vāy oru oru* : Three lots of two gates.  (3350.1)
- `003-550-617` *mū vāy ūḻiyaṉ* : Three gates; King's servant.  (2897.1)
- `004-156` *nāl kā* : Four-keeper.  (2623.1)
- `004-220-060-706-033-520` *nāl mīn -iṉ kalam mū vēḷ* : Four-Star-Inner, chief (allowance: three kalam).  (2592.1)
- `004-390` *nāl parutti* : Four cottons.  (2177.1)
- `004-390-400` *nāl parutti ciṟ* : Four-Cotton, junior.  (3135.1)
- `004-407-001-055-032-740` *nāl kiḷai oru paṉṉiru iru kuṭi* : Of the Four-Kindred-One-Twelve-Two house.  (3613.1)
- `004-408` *nāl kiḷai* : Four lots.  (3172.1)
- `004-900` *nāl tiṅkaḷ* : Four months.  (2449.1)
- `005-140-820-032` *ai ammai kāl iru* : Five ladies; Two quarters.  (2461.1)
- `005-390` *ai parutti* : Five cottons.  (2472.1)
- `005-390-255-435` *ai parutti mutal kōl* : Five cottons; Chief-Rod.  (2777.1)
- `005-407` *ai kiḷai* : Five kindreds.  (2351.1)
- `005-900-740-090` *ai tiṅkaḷ kuṭi āḷ* : Manager of the Five-Moon house.  (2719.1)
- `012-440-001-820-002-032-382-520` *iru koḷ oru kāl iru iru aracu vēḷ* : Two-Received-One-King, chief (allowance: four quarters).  (2236.1)
- `016-617` *āṟu ūḻiyaṉ* : Six king's servants.  (3291.1)
- `017-390` *ēḻu parutti* : Seven cottons.  (3551.2)
- `017-405` *ēḻu nūl* : Seven threads.  (3112.1)
- `017-585-740` *ēḻu kaṉṉi? kuṭi* : Of the Seven-Maiden house.  (2324.1)
- `018-390` *eṭṭu parutti* : Eight cottons.  (2804.1)
- `031` *oru* : One.  (4936.1)
- `031-001-435` *oru oru kōl* : Two rods.  (3385.1)
- `031-003-156` *oru mū kā* : Four-keeper.  (2357.1)
- `031-097-151` *oru aṭimai kā* : One-Bondsman, keeper.  (3312.1)
- `031-125-455-220` *oru vēṭṭuvaṉ ampu mīn* : One Hunter; Arrow-Star.  (2195.1)
- `031-176-740` *oru iṟai kuṭi* : Of the house (allowance: one tax).  (2682.1)
- `031-240-100-740` *oru mīmīn mutu kuṭi* : Of the One-High-star-Elder house.  (2365.1)
- `031-240-927-740` *oru mīmīn irutiṅkaḷ kuṭi* : Of the One-High-star-Two-moons house.  (3346.1)
- `031-368-413-002-233-440-740` *oru koṭi nel iru vāḷai koḷ kuṭi* : Of the One-Banner-Grain-Two-Scabbard-fish-Received house.  (4001.1)
- `031-371-405` *oru katir nūl* : One spindle; Thread.  (2271.1)
- `031-592` *oru paṭṭi* : One pen.  (2302.1)
- `031-705-033-520` *oru kalam mū vēḷ* : One lot of three kalam; Chief.  (2662.1)
- `031-705-243` *oru kalam kayal* : One kalam; Carp.  (3324.1)
- `031-803-368` *oru il koṭi* : One-Home, standard-bearer.  (3384.1)
- `031-850` *oru kāṇi* : One share.  (2357.2)
- `031-861-002-240-773-740` *oru kāṇi iru mīmīn maka kuṭi* : Of the High-star-Child of house (allowance: one lot of two shares).  (3133.1)
- `032-220-923-740` *iru mīn maruppu kuṭi* : Of the Two-Star-Ivory house.  (2651.1)
- `032-226-923-740-400` *iru kūṭumīn maruppu kuṭi ciṟ* : Junior of the Two-Fish-crate-Ivory house.  (3719.1)
- `032-390-001-004-900-154` *iru parutti oru nāl tiṅkaḷ kā* : Two-Cotton-Five-Moon, keeper.  (3993.1)
- `032-590-390-741-032-220-440-740` *iru peṭṭi parutti orukuṭi iru mīn koḷ kuṭi* : Of the Two-Chest-Cotton-First-ward-Two-Star-Received house.  (3169.1)
- `032-632-125-390-002-235-240-032-220-255-435-690-740` *iru pal vēṭṭuvaṉ parutti iru vēymīn mīmīn iru mīn mutal kōl piṇai kuṭi* : Of the Two-Many-Hunter-Cotton-Two-Bamboo-star-High-star-Two-Star-Chief-Rod-Ally house.  (2566.1)
- `032-706-742-350-463-798-740` *iru kalam irukuṭi kalappai mukkōṭu maru- kuṭi* : Of the Second-ward-Plough-Three-peaks-Descendant house (allowance: two kalam).  (3297.1)
- `033-151` *mū kā* : Three-keeper.  (2739.1)
- `033-550-617` *mū vāy ūḻiyaṉ* : Three gates; King's servant.  (3454.1)
- `034-220-520` *nāl mīn vēḷ* : Four-Star, chief.  (3556.1)
- `055-151` *paṉṉiru kā* : Twelve, keeper.  (3381.1)
- `055-368-400` *paṉṉiru koṭi ciṟ* : Twelve-Banner, junior.  (3248.1)
- `061-142-400-740` *kāl kō ciṟ kuṭi* : Of the Quarter-King-Junior house.  (3287.1)
- `061-171-035-740-090` *kāl niṟai ai kuṭi āḷ* : Manager of the Quarter house (allowance: five full measures).  (2788.1)
- `061-171-035-740-090-400` *kāl niṟai ai kuṭi āḷ ciṟ* : Manager of the Quarter house (allowance: five full measures); Junior.  (3342.1)
- `061-740` *kāl kuṭi* : Of the Quarter house.  (3997.1)
- `070-154` *ampu kā* : Arrow, keeper.  (3622.1)
- `070-617-002-240-555-527` *ampu ūḻiyaṉ iru mīmīn vāy kāval* : Arrow-King's servant; Two High-star; Gate-Guard.  (2608.1)
- `091-831-585` *iruvar tiṉai kaṉṉi?* : The pair-Millet-Maiden.  (3212.1)
- `095-001-575-595-001-806-032-220-740-679` *kōlaṉ oru kōṭṭai paṭṭaṟai oru viḷai iru mīn kuṭi kaṭṭil* : Throne of the Staff-bearer-Forge-One-Bounty-Two-Star house (allowance: one great measure).  (3427.1)
- `097-161` *aṭimai kā* : Bondsman-Keeper.  (2722.1)
- `097-400` *aṭimai ciṟ* : Bondsman, junior.  (3242.1)
- `098` *ēvalaṉ* : Attendant.  (3549.1)
- `100-740` *mutu kuṭi* : Of the Elder house.  (2930.1)
- `104-064-820` *taṭṭāṉ pāti kāl* : Goldsmith-Portion-Quarter.  (2857.1)
- `104-890-400` *taṭṭāṉ koṭu ciṟ* : Goldsmith-Given, junior.  (2614.1)
- `125-090` *vēṭṭuvaṉ āḷ* : Hunter, manager.  (2716.1)
- `125-390-741-005-900-740` *vēṭṭuvaṉ parutti orukuṭi ai tiṅkaḷ kuṭi* : Of the Hunter-Cotton-First-ward-Five-Moon house.  (3286.1)
- `125-390-741-176-740` *vēṭṭuvaṉ parutti orukuṭi iṟai kuṭi* : Of the Hunter-Cotton-First-ward-Tax house.  (2838.1)
- `125-705-320-002-803-233-773-740` *vēṭṭuvaṉ kalam paṭi iru il vāḷai maka kuṭi* : Of the Hunter-Ship-Ration measure-Two-Home-Scabbard-fish-Child of house.  (2270.1)
- `125-861-740` *vēṭṭuvaṉ kāṇi kuṭi* : Of the Hunter-Tribute house.  (2471.1)
- `136` *aṭimai* : Bondsman.  (3522.1)
- `140-390-002-061-740` *ammai parutti iru kāl kuṭi* : Of the Lady-Cotton house (allowance: two quarters).  (3134.1)
- `140-390-741-235-350-460-798-740` *ammai parutti orukuṭi vēymīn kalappai mukkōṭu maru- kuṭi* : Of the Lady-Cotton-First-ward-Bamboo-star-Plough-Three-peaks-Descendant house.  (2579.1)
- `140-900-390-741-838-740` *ammai tiṅkaḷ parutti orukuṭi viḷai kuṭi* : Of the Lady-Moon-Cotton-First-ward-Produce house.  (2316.1)
- `140-920-575-705-590` *ammai tiṅkaḷ? kōṭṭai kalam peṭṭi* : Lady-Month-Great measure-Ship-Chest.  (3389.1)
- `142-002-032-220-904-740` *kō iru iru mīn irutiṅkaḷ kuṭi* : Of the King-Four-Star-Dark-moon house.  (2381.1)
- `142-156` *kō kā* : King, keeper.  (2305.1)
- `142-157` *kō kā* : King-Keeper.  (2846.1)
- `142-171-035` *kō niṟai ai* : King; Five full measures.  (3552.2)
- `142-617` *kō ūḻiyaṉ* : King-King's servant.  (2878.1)
- `158-171-035` *kā niṟai ai* : Keeper; Five full measures.  (3536.1)
- `165-031-002-220-100-740-090` *nāḷ oru iru mīn mutu kuṭi āḷ* : Manager of the Day-Three-Star-Elder house.  (2735.1)
- `171-035-130-002-415-100-740` *niṟai ai kaḷamar iru kavar mutu kuṭi* : Of the Husbandman-Two-Branch-Elder house (allowance: five full measures).  (3126.1)
- `171-035-130-820` *niṟai ai kaḷamar kāl* : Five full measures; Husbandman-Quarter.  (2544.1)
- `175-520` *iṟai vēḷ* : Tax, chief.  (2319.1)
- `175-741-233-798-740` *iṟai orukuṭi vāḷai maru- kuṭi* : Of the Tax-First-ward-Scabbard-fish-Descendant house.  (3200.1)
- `176-125-406` *iṟai vēṭṭuvaṉ kiḷai* : Tax-Hunter-Kindred.  (3260.1)
- `176-156` *iṟai kā* : Tax, keeper.  (2848.2)
- `176-705-033-520` *iṟai kalam mū vēḷ* : Tax, chief (allowance: three kalam).  (2797.1)
- `176-740-140-840-064` *iṟai kuṭi ammai iṇai pāti* : Lady of the Tax house; Pair; Portion.  (2230.1)
- `176-741-220-740-565` *iṟai orukuṭi mīn kuṭi maṟavaṉ* : Warrior of the Tax-First-ward-Star house.  (2654.1)
- `201-060-032-590-390-740` *kār -iṉ iru peṭṭi parutti kuṭi* : Of the Rain-season-Inner-Two-Boxed-cotton house.  (2448.1)
- `220` *mīn* : Star.  (2906.1)
- `220-151` *mīn kā* : Star, keeper.  (3155.1)
- `220-440-615-741-243-617` *mīn koḷ vayal orukuṭi kayal ūḻiyaṉ* : Star-Received-Field-First-ward-Carp-King's servant.  (3078.1)
- `220-740-400` *mīn kuṭi ciṟ* : Junior of the Star house.  (3617.1)
- `226` *kūṭumīn* : Fish-crate.  (3489.1)
- `226-621` *kūṭumīn aṭai* : Fish-crate-Stored.  (3366.1)
- `231-233-804` *orumīn vāḷai ilai* : First-star-Scabbard-fish-Leaf.  (2773.1)
- `231-740-151` *orumīn kuṭi kā* : Keeper of the First-star house.  (2733.1)
- `232-048-740` *kūṭumīn er̤uvar kuṭi* : Of the Cluster-star-Seven house.  (3550.1)
- `233-032-877-740` *vāḷai iru nālkāṇi kuṭi* : Of the Scabbard-fish-Two-Four shares house.  (2741.1)
- `233-055-752-740` *vāḷai paṉṉiru maka kuṭi* : Of the Scabbard-fish child of Twelve house.  (2893.1)
- `233-176-740-090` *vāḷai iṟai kuṭi āḷ* : Manager of the Scabbard-fish-Tax house.  (2754.1)
- `233-232-055-740` *vāḷai kūṭumīn paṉṉiru kuṭi* : Of the Scabbard-fish-Cluster-star-Twelve house.  (3259.1)
- `233-255-435-690-740` *vāḷai mutal kōl piṇai kuṭi* : Of the Scabbard-fish-Chief-Rod-Ally house.  (3517.1)
- `233-388-527` *vāḷai aracu kāval* : Scabbard-fish-King-Guard.  (2615.1)
- `233-705-033-520-400` *vāḷai kalam mū vēḷ ciṟ* : Scabbard-fish-Chief, junior (allowance: three kalam).  (3351.1)
- `233-803-740` *vāḷai il kuṭi* : Of the Scabbard-fish-Home house.  (2761.1)
- `233-804-400` *vāḷai ilai ciṟ* : Scabbard-fish-Leaf, junior.  (2248.1)
- `233-923-740` *vāḷai maruppu kuṭi* : Of the Scabbard-fish-Ivory house.  (3340.1)
- `235-231-520` *vēymīn orumīn vēḷ* : Bamboo-star-First-star, chief.  (2821.1)
- `235-233-550` *vēymīn vāḷai vāy* : Bamboo-star-Scabbard-fish-Gate.  (3484.1)
- `235-233-555-527-400` *vēymīn vāḷai vāy kāval ciṟ* : Bamboo-star-Scabbard-fish-Gate-Guard, junior.  (2294.1)
- `235-240-055-151` *vēymīn mīmīn paṉṉiru kā* : Bamboo-star-High-star-Twelve, keeper.  (2337.1)
- `235-240-220-520` *vēymīn mīmīn mīn vēḷ* : Bamboo-star-High-star-Star, chief.  (3357.1)
- `235-240-255-435-690-740` *vēymīn mīmīn mutal kōl piṇai kuṭi* : Of the Bamboo-star-High-star-Chief-Rod-Ally house.  (2873.1)
- `235-240-455-740` *vēymīn mīmīn ampu kuṭi* : Of the Bamboo-star-High-star-Arrow house.  (3468.1)
- `235-240-706-033-520` *vēymīn mīmīn kalam mū vēḷ* : Bamboo-star-High-star, chief (allowance: three kalam).  (3576.1)
- `235-388-740` *vēymīn aracu kuṭi* : Of the Bamboo-star-King house.  (2347.1)
- `235-415-220-520` *vēymīn kavar mīn vēḷ* : Bamboo-star-Branch-Star, chief.  (2841.1)
- `235-482-740` *vēymīn kōṭukāṇi kuṭi* : Of the Bamboo-star-Hill-share house.  (3393.1)
- `235-550-527` *vēymīn vāy kāval* : Bamboo-star-Gate-Guard.  (2181.1)
- `235-555-527` *vēymīn vāy kāval* : Bamboo-star-Gate-Guard.  (3652.1)
- `235-590-405-740` *vēymīn peṭṭi nūl kuṭi* : Of the Bamboo-star-Chest-Thread house.  (3111.1)
- `235-590-407-740-001-004-407` *vēymīn peṭṭi kiḷai kuṭi oru nāl kiḷai* : Of the Bamboo-star-Chest-Kindred house; Five kindreds.  (3615.1)
- `235-706-033-055-740` *vēymīn kalam mū paṉṉiru kuṭi* : Of the Bamboo-star-Twelve house (allowance: three kalam).  (2895.1)
- `235-740-565` *vēymīn kuṭi maṟavaṉ* : Warrior of the Bamboo-star house.  (2185.1)
- `235-772-740` *vēymīn maka kuṭi* : Of the Bamboo-star-Child of house.  (3508.1)
- `235-803-740` *vēymīn il kuṭi* : Of the Bamboo-star-Home house.  (2476.1)
- `240-142-617` *mīmīn kō ūḻiyaṉ* : High-star-King-King's servant.  (3620.1)
- `240-233-740-679` *mīmīn vāḷai kuṭi kaṭṭil* : Throne of the High-star-Scabbard-fish house.  (2484.1)
- `240-415-220-520` *mīmīn kavar mīn vēḷ* : High-star-Branch-Star, chief.  (2420.1)
- `240-503-017-740-400` *mīmīn malai ēḻu kuṭi ciṟ* : Junior of the High-star-Hill-Seven house.  (2314.1)
- `240-503-070-520` *mīmīn malai ampu vēḷ* : High-star-Hill-Arrow, chief.  (3984.1)
- `240-636-740` *mīmīn pal kuṭi* : Of the High-star-Many house.  (2752.1)
- `240-705-033-520` *mīmīn kalam mū vēḷ* : High-star, chief (allowance: three kalam).  (3271.1)
- `240-772-740` *mīmīn maka kuṭi* : Of the High-star-Child of house.  (2348.1)
- `243-151` *kayal kā* : Carp, keeper.  (3362.1)
- `255-070-741-003-645-740` *mutal ampu orukuṭi mū kar̤añcu kuṭi* : Of the Chief-Arrow-First-ward-Three-Gold weight house.  (2495.1)
- `255-435-156` *mutal kōl kā* : Chief-Rod, keeper.  (2624.1)
- `255-740` *mutal kuṭi* : Of the Chief house.  (2487.1)
- `320-920-740` *paṭi tiṅkaḷ? kuṭi* : Of the Ration measure-Month house.  (3330.1)
- `320-920-742-803-415-220-371-406` *paṭi tiṅkaḷ? irukuṭi il kavar mīn katir kiḷai* : Ration measure-Month-Second-ward-Home-Branch-Star-Spindle-Kindred.  (3651.1)
- `323-690` *paṭi piṇai* : Ration-Ally.  (2978.1)
- `323-920-390` *paṭi tiṅkaḷ? parutti* : Ration-Month-Cotton.  (2355.1)
- `323-920-740` *paṭi tiṅkaḷ? kuṭi* : Of the Ration-Month house.  (2894.1)
- `350-125-002-003-390` *kalappai vēṭṭuvaṉ iru mū parutti* : Plough-Hunter; Five cottons.  (2774.1)
- `370-090-817-002-240-740-017-585-740` *katir āḷ kāṇi iru mīmīn kuṭi ēḻu kaṉṉi? kuṭi* : Of the Spindle-Manager-High-star house (allowance: two shares); Of the Seven-Maiden house.  (3089.1)
- `371-031-741-844-390` *katir oru orukuṭi cūṭu parutti* : One spindle; First-ward-Sheaves-Cotton.  (2291.1)
- `371-255-861-368-001` *katir mutal kāṇi koṭi oru* : Spindle-Chief-Tribute; One banner.  (2531.1)
- `371-407-001-142-617` *katir kiḷai oru kō ūḻiyaṉ* : Spindle-Kindred; One king; King's servant.  (3374.1)
- `384-740` *aracu kuṭi* : Of the King house.  (3988.1)
- `388-527` *aracu kāval* : King-Guard.  (2183.1)
- `388-920` *aracu tiṅkaḷ?* : King-Month.  (3497.1)
- `390-090-390-176-740` *parutti āḷ parutti iṟai kuṭi* : Of the Cotton-Manager-Cotton-Tax house.  (2354.1)
- `390-740` *parutti kuṭi* : Of the Cotton house.  (3907.1)
- `415-100-740` *kavar mutu kuṭi* : Of the Branch-Elder house.  (2306.1)
- `415-100-740-400` *kavar mutu kuṭi ciṟ* : Junior of the Branch-Elder house.  (2755.1)
- `415-220-320-920-520` *kavar mīn paṭi tiṅkaḷ? vēḷ* : Branch-Star-Ration measure-Month, chief.  (3311.1)
- `415-220-520` *kavar mīn vēḷ* : Branch-Star, chief.  (2565.1)
- `415-220-706-033-520` *kavar mīn kalam mū vēḷ* : Branch-Star, chief (allowance: three kalam).  (3113.1)
- `415-220-717-740` *kavar mīn aṭi kuṭi* : Of the Branch-Star-Servant house.  (2401.1)
- `416-232-097-151` *turumpu kūṭumīn aṭimai kā* : Grain-heap-Cluster-star-Bondsman, keeper.  (2524.1)
- `416-255-861-002-032-220-798-100-740` *turumpu mutal kāṇi iru iru mīn maru- mutu kuṭi* : Of the Grain-heap-Chief-Star-Descendant-Elder house (allowance: four shares).  (2618.1)
- `440-741-240-220-520` *koḷ orukuṭi mīmīn mīn vēḷ* : Received-First-ward-High-star-Star, chief.  (2265.1)
- `455-590-002-005-368` *ampu peṭṭi iru ai koṭi* : Arrow; Seven chests; Banner.  (4002.1)
- `460-520` *mukkōṭu vēḷ* : Three-peaks, chief.  (3331.1)
- `467-806-154-032-384-142-617` *(n) viḷai kā iru aracu kō ūḻiyaṉ* : N loads of produce, carried by the porter; Two King; King-King's servant.  (2867.1)
- `468-806-154` *(n) viḷai kā* : N loads of produce, carried by the porter.  (2223.1)
- `468-806-155` *(n) viḷai kā* : N loads of produce, carried by the porter.  (4007.1)
- `482-740` *kōṭukāṇi kuṭi* : Of the Hill-share house.  (3528.1)
- `491-003-423` *kompu mū par̤aṉam* : Horn; Three fields.  (3627.1)
- `495-615-740` *kompu vayal kuṭi* : Of the Horn-Field house.  (2792.1)
- `503-007-740` *malai ēḻu kuṭi* : Of the Hill-Seven house.  (3272.1)
- `503-017-740` *malai ēḻu kuṭi* : Of the Hill-Seven house.  (2499.1)
- `503-017-760-740` *malai ēḻu maka kuṭi* : Of the Hill-Seven-Child of house.  (3848.1)
- `503-455-220-002-806-235-240-055-740` *malai ampu mīn iru viḷai vēymīn mīmīn paṉṉiru kuṭi* : Of the Hill-Arrow-Star-Two-Bounty-Bamboo-star-High-star-Twelve house.  (2557.1)
- `503-460-158-400` *malai mukkōṭu kā ciṟ* : Hill-Three-peaks-Keeper, junior.  (3356.1)
- `503-460-740` *malai mukkōṭu kuṭi* : Of the Hill-Three-peaks house.  (3612.1)
- `503-463-740` *malai mukkōṭu kuṭi* : Of the Hill-Three-peaks house.  (2406.1)
- `503-615-003-900-740` *malai vayal mū tiṅkaḷ kuṭi* : Of the Hill-Field-Three-Moon house.  (2870.1)
- `503-615-740` *malai vayal kuṭi* : Of the Hill-Field house.  (2320.1)
- `520-455-220-002-803-226` *vēḷ ampu mīn iru il kūṭumīn* : Chief-Arrow-Star; Two houses; Fish-crate.  (2674.1)
- `527-741-032-590-390-740` *kāval orukuṭi iru peṭṭi parutti kuṭi* : Of the Guard-First-ward-Two-Chest-Cotton house.  (3359.1)
- `530` *paṟai* : Proclamation.  (4003.1)
- `540-002-806-240-017-575-740-679` *paṟai iru viḷai mīmīn ēḻu kōṭṭai kuṭi kaṭṭil* : Throne of the Drum-Two-Bounty-High-star house (allowance: seven great measures).  (2889.1)
- `550-060-016-390` *vāy -iṉ āṟu parutti* : gate: Six cottons.  (2684.1)
- `550-060-032-904-740` *vāy -iṉ iru irutiṅkaḷ kuṭi* : gate: of the Two-Dark-moon house.  (2826.1)
- `550-060-231-705-033-520` *vāy -iṉ orumīn kalam mū vēḷ* : gate: First-star, chief (allowance: three kalam).  (3282.1)
- `550-060-415-220-705-033-550-527` *vāy -iṉ kavar mīn kalam mū vāy kāval* : gate: Branch-Star; Three kalam; Gate-Guard.  (2861.1)
- `550-060-440-760-740` *vāy -iṉ koḷ maka kuṭi* : gate: of the child of Received house.  (2676.1)
- `550-060-555-526` *vāy -iṉ vāy kāval* : gate: Gate-Guard.  (2591.1)
- `550-060-679` *vāy -iṉ kaṭṭil* : gate: Throne.  (2196.1)
- `550-060-690-740` *vāy -iṉ piṇai kuṭi* : gate: of the Ally house.  (2978.2)
- `555-527` *vāy kāval* : Gate-Guard.  (2437.1)
- `565` *maṟavaṉ* : Warrior.  (3254.1)
- `575-031` *kōṭṭai oru* : One great measure.  (2836.1)
- `575-031-002-003-390` *kōṭṭai oru iru mū parutti* : Great measure; Six cottons.  (2836.2)
- `575-125-741-031-061-142-740` *kōṭṭai vēṭṭuvaṉ orukuṭi oru kāl kō kuṭi* : Of the Great measure-Hunter-First-ward-King house (allowance: one quarter).  (3249.1)
- `575-590-740-240-520` *kōṭṭai peṭṭi kuṭi mīmīn vēḷ* : High-star of the Great measure-Chest house; Chief.  (3355.1)
- `575-590-741-240-520` *kōṭṭai peṭṭi orukuṭi mīmīn vēḷ* : Great measure-Chest-First-ward-High-star, chief.  (2312.1)
- `575-705-742-491-226` *kōṭṭai kalam irukuṭi kompu kūṭumīn* : Great measure-Ship-Second-ward-Horn-Fish-crate.  (3164.1)
- `575-706-001-031-220-520` *kōṭṭai kalam oru oru mīn vēḷ* : Great measure-Ship-Two-Star, chief.  (2593.1)
- `575-740-679` *kōṭṭai kuṭi kaṭṭil* : Throne of the Great measure house.  (2176.2)
- `590-003-900-002-240-772-740` *peṭṭi mū tiṅkaḷ iru mīmīn maka kuṭi* : Of the Chest-Three-Moon-Two-High-star-Child of house.  (3353.1)
- `590-390-368-033-033` *peṭṭi parutti koṭi mū mū* : Boxed-cotton; Six banners.  (3158.1)
- `590-390-741-923-740` *peṭṭi parutti orukuṭi maruppu kuṭi* : Of the Boxed-cotton-First-ward-Ivory house.  (3361.1)
- `590-390-820` *peṭṭi parutti kāl* : Boxed-cotton-Quarter.  (3390.1)
- `590-405-740` *peṭṭi nūl kuṭi* : Of the Chest-Thread house.  (2327.1)
- `590-705-002-415-100-740` *peṭṭi kalam iru kavar mutu kuṭi* : Of the Chest-Ship-Two-Branch-Elder house.  (2771.1)
- `590-740-745-235-240-055-482-740` *peṭṭi kuṭi mukuṭi vēymīn mīmīn paṉṉiru kōṭukāṇi kuṭi* : Of the Chest house; Of the Third-ward-Bamboo-star-High-star-Twelve-Hill-share house.  (3087.1)
- `590-820` *peṭṭi kāl* : Chest-Quarter.  (2304.1)
- `590-892` *peṭṭi vil* : Chest-Sale.  (2340.1)
- `592` *paṭṭi* : Pen.  (3321.1)
- `595-706-243-617` *paṭṭaṟai kalam kayal ūḻiyaṉ* : Forge-Ship-Carp-King's servant.  (2553.1)
- `595-803-153` *paṭṭaṟai il kā* : Forge-Home-Keeper.  (2206.1)
- `603-861-002-032-220-240-520` *kūṭu kāṇi iru iru mīn mīmīn vēḷ* : Store-Star-High-star, chief (allowance: four shares).  (2763.1)
- `603-861-002-055-740` *kūṭu kāṇi iru paṉṉiru kuṭi* : Of the Store-Twelve house (allowance: two shares).  (3580.1)
- `603-861-002-803-798-233-705-033-017-585-740` *kūṭu kāṇi iru il maru- vāḷai kalam mū ēḻu kaṉṉi? kuṭi* : Of the Store-Home-Descendant-Scabbard-fish-Maiden house (allowance: two shares and 10 kalam).  (3139.1)
- `605-760-740` *kutir maka kuṭi* : Of the child of Granary house.  (3379.1)
- `615-550-002-350-151` *vayal vāy iru kalappai kā* : Field-Gate-Two-Plough, keeper.  (3261.1)
- `615-900-002-031-503-460-740` *vayal tiṅkaḷ iru oru malai mukkōṭu kuṭi* : Of the Field-Moon-Three-Hill-Three-peaks house.  (3332.1)
- `617-741-004-390` *ūḻiyaṉ orukuṭi nāl parutti* : King's servant-First-ward; Four cottons.  (2429.1)
- `617-741-176-100-740` *ūḻiyaṉ orukuṭi iṟai mutu kuṭi* : Of the King's servant-First-ward-Tax-Elder house.  (2219.1)
- `621-740` *aṭai kuṭi* : Of the Stored house.  (2706.1)
- `632-140-706` *pal ammai kalam* : Many-Lady-Ship.  (2537.1)
- `645-003-820` *kar̤añcu mū kāl* : Three gold weights; Quarter.  (2844.2)
- `679-002-155-630-740` *kaṭṭil iru kā pal kuṭi* : Of the Throne-Two-Keeper-Many house.  (2790.1)
- `690-740` *piṇai kuṭi* : Of the Ally house.  (2701.1)
- `690-904-740` *piṇai irutiṅkaḷ kuṭi* : Of the Ally-Dark-moon house.  (3386.1)
- `692-001-467-806-155` *kūṭṭam oru (n) viḷai kā* : One Assembly; N loads of produce, carried by the porter.  (2218.1)
- `692-060-031-741-165` *kūṭṭam -iṉ oru orukuṭi nāḷ* : Assembly: One; First-ward-Day.  (2455.1)
- `692-060-140-920-740-090` *kūṭṭam -iṉ ammai tiṅkaḷ? kuṭi āḷ* : Assembly: manager of the Lady-Month house.  (3525.1)
- `692-060-231-440-740` *kūṭṭam -iṉ orumīn koḷ kuṭi* : Assembly: of the First-star-Received house.  (3105.1)
- `692-060-231-803-740` *kūṭṭam -iṉ orumīn il kuṭi* : Assembly: of the First-star-Home house.  (2597.1)
- `692-060-231-927-740` *kūṭṭam -iṉ orumīn irutiṅkaḷ kuṭi* : Assembly: of the First-star-Two-moons house.  (3537.1)
- `692-060-235-240-226` *kūṭṭam -iṉ vēymīn mīmīn kūṭumīn* : Assembly: Bamboo-star-High-star-Fish-crate.  (2428.1)
- `692-060-235-240-773-740` *kūṭṭam -iṉ vēymīn mīmīn maka kuṭi* : Assembly: of the Bamboo-star-High-star-Child of house.  (2534.1)
- `692-060-705-033-923-740` *kūṭṭam -iṉ kalam mū maruppu kuṭi* : Assembly: of the Ivory house (allowance: three kalam).  (2385.1)
- `692-060-806-233-923-740-061-407` *kūṭṭam -iṉ viḷai vāḷai maruppu kuṭi kāl kiḷai* : Assembly: quarter of the Bounty-Scabbard-fish-Ivory house; Kindred.  (2696.1)
- `692-060-920-255-740` *kūṭṭam -iṉ tiṅkaḷ? mutal kuṭi* : Assembly: of the Month-Chief house.  (2673.1)
- `692-390-002-032-226` *kūṭṭam parutti iru iru kūṭumīn* : Assembly-Cotton; Four fish-crates.  (2598.1)
- `692-550-350-031-002-415-100-740-090` *kūṭṭam vāy kalappai oru iru kavar mutu kuṭi āḷ* : Manager of the Assembly-Gate-Plough-Three-Branch-Elder house.  (3163.1)
- `692-890-740` *kūṭṭam koṭu kuṭi* : Of the Assembly-Given house.  (2811.1)
- `700-003-692-900-003-140-592-400` *nāḻi? mū kūṭṭam tiṅkaḷ mū ammai paṭṭi ciṟ* : Measurer-Three-Assembly-Moon-Three-Lady-Pen, junior.  (2977.1)
- `700-820-002-231-705-033-520` *nāḻi? kāl iru orumīn kalam mū vēḷ* : The Measurer; First-star, chief (allowance: two quarters and three kalam).  (2613.1)
- `705-033-002-335-760-740` *kalam mū iru ūr maka kuṭi* : Of the child of Town house (allowance: five kalam).  (3516.1)
- `705-033-520-001-031-154` *kalam mū vēḷ oru oru kā* : Chief (allowance: three kalam); Two-keeper.  (3109.1)
- `705-255-435-798-002-061-142-400-740` *kalam mutal kōl maru- iru kāl kō ciṟ kuṭi* : Of the Ship-Chief-Rod-Descendant-King-Junior house (allowance: two quarters).  (2297.1)
- `705-255-740` *kalam mutal kuṭi* : Of the Ship-Chief house.  (2807.1)
- `705-390-002-031-157` *kalam parutti iru oru kā* : Ship-Cotton; Three-keeper.  (3992.1)
- `705-500-741-803-923-740` *kalam pāy orukuṭi il maruppu kuṭi* : Of the Ship-Sail-First-ward-Home-Ivory house.  (2655.1)
- `705-740` *kalam kuṭi* : Of the Ship house.  (2747.1)
- `706-033-001-752-740` *kalam mū oru maka kuṭi* : Of the Child of house (allowance: four kalam).  (2890.1)
- `706-140-368` *kalam ammai koṭi* : Ship-Lady, standard-bearer.  (3210.1)
- `706-717-388-154` *kalam aṭi aracu kā* : Ship-Servant-King, keeper.  (3577.1)
- `706-820-595` *kalam kāl paṭṭaṟai* : Ship-Quarter-Forge.  (3595.1)
- `717-151` *aṭi kā* : Servant, keeper.  (2740.1)
- `717-740` *aṭi kuṭi* : Of the Servant house.  (2466.1)
- `740` *kuṭi* : Of the house.  (3568.1)
- `741-820-002-031-243-151` *orukuṭi kāl iru oru kayal kā* : First-ward-Carp, keeper (allowance: three quarters).  (2686.1)
- `741-820-002-803-740` *orukuṭi kāl iru il kuṭi* : Of the First-ward-Home house (allowance: two quarters).  (3490.1)
- `742-760-740` *irukuṭi maka kuṭi* : Of the child of Second-ward house.  (3273.1)
- `742-806-415-220-717-904-100` *irukuṭi viḷai kavar mīn aṭi irutiṅkaḷ mutu* : Second-ward-Bounty-Branch-Star-Servant-Dark-moon-Elder.  (2480.1)
- `745-125-400` *mukuṭi vēṭṭuvaṉ ciṟ* : Third-ward-Hunter, junior.  (2517.1)
- `745-171-032-031` *mukuṭi niṟai iru oru* : Third-ward; Three full measures.  (2329.1)
- `760-740` *maka kuṭi* : Of the Child of house.  (2498.1)
- `790` *maṇi* : Gem.  (3555.2)
- `790-390-741-590-390-740` *maṇi parutti orukuṭi peṭṭi parutti kuṭi* : Of the Gem-Cotton-First-ward-Boxed-cotton house.  (2658.1)
- `792-740` *aracu kuṭi* : Of the Royal house.  (3348.1)
- `798-017-575-740-679` *maru- ēḻu kōṭṭai kuṭi kaṭṭil* : Throne of the Descendant house (allowance: seven great measures).  (2176.1)
- `798-032-220-440-752-740` *maru- iru mīn koḷ maka kuṭi* : Of the Descendant-Two-Star-child of Received house.  (3582.1)
- `798-233-790-900-740` *maru- vāḷai maṇi tiṅkaḷ kuṭi* : Of the Descendant-Scabbard-fish-Gem-Moon house.  (2648.1)
- `798-240-231-555-527` *maru- mīmīn orumīn vāy kāval* : Descendant-High-star-First-star-Gate-Guard.  (3625.1)
- `798-415-220-176-740` *maru- kavar mīn iṟai kuṭi* : Of the Descendant-Branch-Star-Tax house.  (3338.1)
- `798-415-220-520` *maru- kavar mīn vēḷ* : Descendant-Branch-Star, chief.  (2891.1)
- `798-705-033-840-032-740` *maru- kalam mū iṇai iru kuṭi* : Of the Descendant-Peer-Two house (allowance: three kalam).  (2486.1)
- `803-002-003-390` *il iru mū parutti* : Home; Five cottons.  (2702.1)
- `803-032-226` *il iru kūṭumīn* : Home; Two fish-crates.  (3224.1)
- `803-161` *il kā* : Home-Keeper.  (2264.1)
- `803-220-176-740-165-140` *il mīn iṟai kuṭi nāḷ ammai* : Day of the Home-Star-Tax house; Lady.  (2772.1)
- `803-233-240-706-033-520` *il vāḷai mīmīn kalam mū vēḷ* : Home-Scabbard-fish-High-star, chief (allowance: three kalam).  (2759.1)
- `803-233-520-400` *il vāḷai vēḷ ciṟ* : Home-Scabbard-fish-Chief, junior.  (2468.1)
- `803-233-706-033-760-740` *il vāḷai kalam mū maka kuṭi* : Of the Home-Scabbard-fish-Child of house (allowance: three kalam).  (3453.1)
- `803-235-233-705-033-070-520` *il vēymīn vāḷai kalam mū ampu vēḷ* : Home-Bamboo-star-Scabbard-fish-Arrow, chief (allowance: three kalam).  (3378.1)
- `803-235-240-705-033-176-740` *il vēymīn mīmīn kalam mū iṟai kuṭi* : Of the Home-Bamboo-star-High-star-Tax house (allowance: three kalam).  (3227.1)
- `803-240-772-740` *il mīmīn maka kuṭi* : Of the Home-High-star-Child of house.  (3132.1)
- `803-798-415-220-001-760-740` *il maru- kavar mīn oru maka kuṭi* : Of the Home-Descendant-Branch-Star-One-Child of house.  (2377.1)
- `803-861-002-705-033-482-740` *il kāṇi iru kalam mū kōṭukāṇi kuṭi* : Of the Home-Hill-share house (allowance: two shares and three kalam).  (3909.1)
- `803-923-740` *il maruppu kuṭi* : Of the Home-Ivory house.  (3314.1)
- `804-400` *ilai ciṟ* : Leaf, junior.  (4004.2)
- `806-032-220-240-055-740` *viḷai iru mīn mīmīn paṉṉiru kuṭi* : Of the Bounty-Two-Star-High-star-Twelve house.  (3572.1)
- `806-032-220-590-405-740` *viḷai iru mīn peṭṭi nūl kuṭi* : Of the Bounty-Two-Star-Chest-Thread house.  (2888.1)
- `806-233-845-407` *viḷai vāḷai cūṭu kiḷai* : Bounty-Scabbard-fish-Sheaf-bundle-Kindred.  (2189.1)
- `806-235-240-503-017-752-740` *viḷai vēymīn mīmīn malai ēḻu maka kuṭi* : Of the Bounty-Bamboo-star-High-star-Hill-Seven-Child of house.  (2558.1)
- `806-235-240-923-740` *viḷai vēymīn mīmīn maruppu kuṭi* : Of the Bounty-Bamboo-star-High-star-Ivory house.  (2901.1)
- `806-235-520` *viḷai vēymīn vēḷ* : Bounty-Bamboo-star, chief.  (3122.1)
- `806-240-520` *viḷai mīmīn vēḷ* : Bounty-High-star, chief.  (3182.1)
- `806-320-900-388-740` *viḷai paṭi tiṅkaḷ aracu kuṭi* : Of the Bounty-Ration measure-Moon-King house.  (2698.1)
- `806-706-033-520` *viḷai kalam mū vēḷ* : Bounty, chief (allowance: three kalam).  (3176.1)
- `806-706-033-590-405-798-740` *viḷai kalam mū peṭṭi nūl maru- kuṭi* : Of the Bounty-Chest-Thread-Descendant house (allowance: three kalam).  (3628.1)
- `806-798-415-220-790-900-740` *viḷai maru- kavar mīn maṇi tiṅkaḷ kuṭi* : Of the Bounty-Descendant-Branch-Star-Gem-Moon house.  (2234.1)
- `806-923-740` *viḷai maruppu kuṭi* : Of the Bounty-Ivory house.  (2309.1)
- `817-002-003-390` *kāṇi iru mū parutti* : two shares: Three cottons.  (2560.1)
- `817-002-004-220-520` *kāṇi iru nāl mīn vēḷ* : two shares: Four-Star, chief.  (2603.1)
- `817-002-004-390-621` *kāṇi iru nāl parutti aṭai* : two shares: Four cottons; Stored.  (2799.1)
- `817-002-013-840-176-100-740` *kāṇi iru mū iṇai iṟai mutu kuṭi* : two shares: of the Three-Peer-Tax-Elder house.  (2643.1)
- `817-002-017-575-740-679` *kāṇi iru ēḻu kōṭṭai kuṭi kaṭṭil* : two shares: throne of the house (allowance: seven great measures).  (3206.1)
- `817-002-017-585-740` *kāṇi iru ēḻu kaṉṉi? kuṭi* : two shares: of the Seven-Maiden house.  (2299.1)
- `817-002-017-585-840-032-740` *kāṇi iru ēḻu kaṉṉi? iṇai iru kuṭi* : two shares: of the Seven-Maiden-Peer-Two house.  (3190.1)
- `817-002-031-013-840-740` *kāṇi iru oru mū iṇai kuṭi* : two shares: of the Four-Peer house.  (2617.1)
- `817-002-032-220-240-585-740` *kāṇi iru iru mīn mīmīn kaṉṉi? kuṭi* : two shares: of the Two-Star-High-star-Maiden house.  (3146.1)
- `817-002-048-740` *kāṇi iru er̤uvar kuṭi* : two shares: of the Seven house.  (3300.1)
- `817-002-061-142-740` *kāṇi iru kāl kō kuṭi* : two shares: of the Quarter-King house.  (2690.1)
- `817-002-061-407` *kāṇi iru kāl kiḷai* : two shares: Quarter-Kindred.  (2904.1)
- `817-002-104-615-740` *kāṇi iru taṭṭāṉ vayal kuṭi* : two shares: of the Goldsmith-Field house.  (3481.1)
- `817-002-142-617` *kāṇi iru kō ūḻiyaṉ* : two shares: King-King's servant.  (2204.1)
- `817-002-176-455-740` *kāṇi iru iṟai ampu kuṭi* : two shares: of the Tax-Arrow house.  (3575.1)
- `817-002-176-740` *kāṇi iru iṟai kuṭi* : two shares: of the Tax house.  (2263.1)
- `817-002-220-231-705-033-520` *kāṇi iru mīn orumīn kalam mū vēḷ* : two shares: Star-First-star, chief (allowance: three kalam).  (3278.1)
- `817-002-220-520-621` *kāṇi iru mīn vēḷ aṭai* : two shares: Star-Chief-Stored.  (2268.1)
- `817-002-231-520` *kāṇi iru orumīn vēḷ* : two shares: First-star, chief.  (2782.1)
- `817-002-233-235-503-740` *kāṇi iru vāḷai vēymīn malai kuṭi* : two shares: of the Scabbard-fish-Bamboo-star-Hill house.  (2769.1)
- `817-002-233-235-705-033-520` *kāṇi iru vāḷai vēymīn kalam mū vēḷ* : two shares: Scabbard-fish-Bamboo-star, chief (allowance: three kalam).  (3561.1)
- `817-002-233-705-033-550-527` *kāṇi iru vāḷai kalam mū vāy kāval* : two shares: Scabbard-fish; Three kalam; Gate-Guard.  (3604.1)
- `817-002-235-550-527` *kāṇi iru vēymīn vāy kāval* : two shares: Bamboo-star-Gate-Guard.  (3302.1)
- `817-002-235-706-033-555-527` *kāṇi iru vēymīn kalam mū vāy kāval* : two shares: Bamboo-star; Three kalam; Gate-Guard.  (2359.1)
- `817-002-240-176-740` *kāṇi iru mīmīn iṟai kuṭi* : two shares: of the High-star-Tax house.  (2809.1)
- `817-002-240-415-100-740` *kāṇi iru mīmīn kavar mutu kuṭi* : two shares: of the High-star-Branch-Elder house.  (2671.1)
- `817-002-240-415-100-740-090` *kāṇi iru mīmīn kavar mutu kuṭi āḷ* : two shares: manager of the High-star-Branch-Elder house.  (2283.1)
- `817-002-240-550-527` *kāṇi iru mīmīn vāy kāval* : two shares: High-star-Gate-Guard.  (2570.1)
- `817-002-240-923-740` *kāṇi iru mīmīn maruppu kuṭi* : two shares: of the High-star-Ivory house.  (3526.1)
- `817-002-255-435-690-740` *kāṇi iru mutal kōl piṇai kuṭi* : two shares: of the Chief-Rod-Ally house.  (3229.1)
- `817-002-350-400-520` *kāṇi iru kalappai ciṟ vēḷ* : two shares: Plough-Junior, chief.  (3156.1)
- `817-002-350-460-798-415-100-740` *kāṇi iru kalappai mukkōṭu maru- kavar mutu kuṭi* : two shares: of the Plough-Three-peaks-Descendant-Branch-Elder house.  (3459.1)
- `817-002-415-100-740` *kāṇi iru kavar mutu kuṭi* : two shares: of the Branch-Elder house.  (3251.1)
- `817-002-503-007-740` *kāṇi iru malai ēḻu kuṭi* : two shares: of the Hill-Seven house.  (2858.1)
- `817-002-503-460-740` *kāṇi iru malai mukkōṭu kuṭi* : two shares: of the Hill-Three-peaks house.  (2586.1)
- `817-002-503-460-921-070-760-740` *kāṇi iru malai mukkōṭu vil ampu maka kuṭi* : two shares: of the Hill-Three-peaks-Bow child of Arrow house.  (2768.1)
- `817-002-503-776-740` *kāṇi iru malai malar kuṭi* : two shares: of the Hill-Bloom house.  (2542.1)
- `817-002-519-415-220-520` *kāṇi iru vēli kavar mīn vēḷ* : two shares: Fence-Branch-Star, chief.  (3094.1)
- `817-002-555-527` *kāṇi iru vāy kāval* : two shares: Gate-Guard.  (2243.1)
- `817-002-590-390-740-621` *kāṇi iru peṭṭi parutti kuṭi aṭai* : two shares: stored of the Boxed-cotton house.  (3263.1)
- `817-002-760-740` *kāṇi iru maka kuṭi* : two shares: of the Child of house.  (3533.1)
- `817-002-772-740` *kāṇi iru maka kuṭi* : two shares: of the Child of house.  (3308.1)
- `817-002-792-740-090` *kāṇi iru aracu kuṭi āḷ* : two shares: manager of the Royal house.  (3265.1)
- `817-002-803-240-233-520` *kāṇi iru il mīmīn vāḷai vēḷ* : two shares: Home-High-star-Scabbard-fish, chief.  (3232.1)
- `817-033-927-740` *kāṇi mū irutiṅkaḷ kuṭi* : three shares: of the Two-moons house.  (2364.1)
- `817-368-060-003-156` *kāṇi koṭi -iṉ mū kā* : share: Banner; Three ofs; Keeper.  (2607.1)
- `817-368-060-233-740-090` *kāṇi koṭi -iṉ vāḷai kuṭi āḷ* : share: manager of the Banner-Inner-Scabbard-fish house.  (3339.1)
- `817-368-142-156` *kāṇi koṭi kō kā* : share: Banner-King, keeper.  (2803.1)
- `817-368-220-520` *kāṇi koṭi mīn vēḷ* : share: Banner-Star, chief.  (2485.1)
- `817-368-503-017-760-740` *kāṇi koṭi malai ēḻu maka kuṭi* : share: of the Banner-Hill-Seven-Child of house.  (2272.1)
- `820` *kāl* : quarter.  (3565.4)
- `820-001-235-240-740-090` *kāl oru vēymīn mīmīn kuṭi āḷ* : one quarter: manager of the Bamboo-star-High-star house.  (3276.1)
- `820-001-798-233-790-900-740` *kāl oru maru- vāḷai maṇi tiṅkaḷ kuṭi* : one quarter: of the Descendant-Scabbard-fish-Gem-Moon house.  (2683.1)
- `820-001-806-240-472-806-100-740` *kāl oru viḷai mīmīn (n) viḷai mutu kuṭi* : one quarter: of the Bounty-High-star-N-Bounty-Elder house.  (2853.1)
- `820-002-004-390` *kāl iru nāl parutti* : two quarters: Four cottons.  (2630.1)
- `820-002-004-407` *kāl iru nāl kiḷai* : two quarters: Four kindreds.  (2881.1)
- `820-002-014-220-740-090` *kāl iru nāl mīn kuṭi āḷ* : two quarters: manager of the Four-Star house.  (2783.1)
- `820-002-017-575-740` *kāl iru ēḻu kōṭṭai kuṭi* : two quarters: of the house (allowance: seven great measures).  (3152.1)
- `820-002-017-585-740` *kāl iru ēḻu kaṉṉi? kuṭi* : two quarters: of the Seven-Maiden house.  (3505.1)
- `820-002-032-220-233-100-740` *kāl iru iru mīn vāḷai mutu kuṭi* : two quarters: of the Two-Star-Scabbard-fish-Elder house.  (2871.1)
- `820-002-032-220-240-055-161` *kāl iru iru mīn mīmīn paṉṉiru kā* : two quarters: Two Star; High-star-Twelve-Keeper.  (2417.1)
- `820-002-032-220-335-760-740` *kāl iru iru mīn ūr maka kuṭi* : two quarters: of the Two-Star-child of Town house.  (2745.1)
- `820-002-032-220-923-740` *kāl iru iru mīn maruppu kuṭi* : two quarters: of the Two-Star-Ivory house.  (2699.1)
- `820-002-055-803-220-705-033-520` *kāl iru paṉṉiru il mīn kalam mū vēḷ* : two quarters: Twelve-Home-Star, chief (allowance: three kalam).  (2644.1)
- `820-002-156-773-740` *kāl iru kā maka kuṭi* : two quarters: of the Keeper-Child of house.  (3194.1)
- `820-002-176-415-100-740` *kāl iru iṟai kavar mutu kuṭi* : two quarters: of the Tax-Branch-Elder house.  (2464.1)
- `820-002-220-032-220-803-740` *kāl iru mīn iru mīn il kuṭi* : two quarters: of the Star-Two-Star-Home house.  (2292.1)
- `820-002-222-740` *kāl iru aṭaimīn kuṭi* : two quarters: of the Shut-in-fish house.  (2725.1)
- `820-002-231-520` *kāl iru orumīn vēḷ* : two quarters: First-star, chief.  (3480.1)
- `820-002-240-220-717-740` *kāl iru mīmīn mīn aṭi kuṭi* : two quarters: of the High-star-Star-Servant house.  (3095.1)
- `820-002-388-740` *kāl iru aracu kuṭi* : two quarters: of the King house.  (2435.1)
- `820-002-415-100-740` *kāl iru kavar mutu kuṭi* : two quarters: of the Branch-Elder house.  (3151.1)
- `820-002-540-740` *kāl iru paṟai kuṭi* : two quarters: of the Drum house.  (3462.1)
- `820-002-621-416-740` *kāl iru aṭai turumpu kuṭi* : two quarters: of the Stored-Grain-heap house.  (3506.1)
- `820-002-798-032-220-055-740` *kāl iru maru- iru mīn paṉṉiru kuṭi* : two quarters: of the Descendant-Two-Star-Twelve house.  (2877.1)
- `820-002-798-240-705-033-017-585-740` *kāl iru maru- mīmīn kalam mū ēḻu kaṉṉi? kuṭi* : two quarters: of the Descendant-High-star-Maiden house (allowance: 10 kalam).  (2578.1)
- `820-002-803-003-900-740` *kāl iru il mū tiṅkaḷ kuṭi* : two quarters: of the Home-Three-Moon house.  (2880.1)
- `820-002-803-032-384-740` *kāl iru il iru aracu kuṭi* : two quarters: of the Home-Two-King house.  (3295.1)
- `820-002-803-233-032-861-740` *kāl iru il vāḷai iru kāṇi kuṭi* : two quarters: of the Home-Scabbard-fish house (allowance: two shares).  (3650.1)
- `820-002-803-240-220-520` *kāl iru il mīmīn mīn vēḷ* : two quarters: Home-High-star-Star, chief.  (2506.1)
- `820-002-806-590-405-740` *kāl iru viḷai peṭṭi nūl kuṭi* : two quarters: of the Bounty-Chest-Thread house.  (3611.1)
- `820-002-838-798-415-220-233-590-390-740` *kāl iru viḷai maru- kavar mīn vāḷai peṭṭi parutti kuṭi* : two quarters: of the Produce-Descendant-Branch-Star-Scabbard-fish-Boxed-cotton house.  (3305.1)
- `820-002-844-390-621` *kāl iru cūṭu parutti aṭai* : two quarters: Sheaves-Cotton-Stored.  (2220.1)
- `820-002-904-740` *kāl iru irutiṅkaḷ kuṭi* : two quarters: of the Dark-moon house.  (3504.1)
- `820-013-142-617` *kāl mū kō ūḻiyaṉ* : three quarters: King-King's servant.  (2896.1)
- `820-013-474-806-154` *kāl mū (n) viḷai kā* : three quarters: N loads of produce, carried by the porter.  (2443.1)
- `820-013-923-740` *kāl mū maruppu kuṭi* : three quarters: of the Ivory house.  (4011.1)
- `820-060-003-405` *kāl -iṉ mū nūl* : quarter: Three threads.  (3663.1)
- `820-060-061-740` *kāl -iṉ kāl kuṭi* : quarter: of the Quarter house.  (2840.1)
- `820-060-220-798-740` *kāl -iṉ mīn maru- kuṭi* : quarter: of the Star-Descendant house.  (2427.1)
- `820-060-231-798-740` *kāl -iṉ orumīn maru- kuṭi* : quarter: of the First-star-Descendant house.  (2345.1)
- `820-060-235-233-705-033-520` *kāl -iṉ vēymīn vāḷai kalam mū vēḷ* : quarter: Bamboo-star-Scabbard-fish, chief (allowance: three kalam).  (2478.1)
- `820-060-235-240-455-740` *kāl -iṉ vēymīn mīmīn ampu kuṭi* : quarter: of the Bamboo-star-High-star-Arrow house.  (2293.1)
- `820-060-235-240-923-740` *kāl -iṉ vēymīn mīmīn maruppu kuṭi* : quarter: of the Bamboo-star-High-star-Ivory house.  (2285.1)
- `820-060-415-220-520` *kāl -iṉ kavar mīn vēḷ* : quarter: Branch-Star, chief.  (2689.1)
- `820-060-705-033-520` *kāl -iṉ kalam mū vēḷ* : quarter: Chief (allowance: three kalam).  (2822.1)
- `820-060-773-740` *kāl -iṉ maka kuṭi* : quarter: of the Child of house.  (3173.1)
- `820-060-803-233-520` *kāl -iṉ il vāḷai vēḷ* : quarter: Home-Scabbard-fish, chief.  (3326.1)
- `820-125-405-002-235-233-240-636-740` *kāl vēṭṭuvaṉ nūl iru vēymīn vāḷai mīmīn pal kuṭi* : quarter: of the Hunter-Thread-Two-Bamboo-star-Scabbard-fish-High-star-Many house.  (2569.1)
- `820-717-002-032-220-255-435-690-740` *kāl aṭi iru iru mīn mutal kōl piṇai kuṭi* : quarter: of the Servant-Four-Star-Chief-Rod-Ally house.  (2490.1)
- `821-001-233-320-920-740` *mañcāṭi oru vāḷai paṭi tiṅkaḷ? kuṭi* : Of the Mañcāṭi weight-One-Scabbard-fish-Ration measure-Month house.  (2638.1)
- `821-740` *mañcāṭi kuṭi* : Of the Mañcāṭi weight house.  (2215.1)
- `821-741-590-390-740` *mañcāṭi orukuṭi peṭṭi parutti kuṭi* : Of the Mañcāṭi weight-First-ward-Boxed-cotton house.  (3328.1)
- `824-002-016-390` *vilai iru āṟu parutti* : worth eight: Cotton.  (3281.1)
- `824-002-235-482-740` *vilai iru vēymīn kōṭukāṇi kuṭi* : worth two: of the Bamboo-star-Hill-share house.  (3202.1)
- `831-390-368` *tiṉai parutti koṭi* : Millet-Cotton, standard-bearer.  (3237.1)
- `831-617` *tiṉai ūḻiyaṉ* : Millet-King's servant.  (2839.1)
- `831-892` *tiṉai vil* : Millet-Sale.  (2731.1)
- `840` *iṇai* : Peer.  (3388.1)
- `840-032-165-590` *iṇai iru nāḷ peṭṭi* : Two pairs; Day-Chest.  (3240.1)
- `840-032-740-090-400` *iṇai iru kuṭi āḷ ciṟ* : Manager of the Peer-Two house; Junior.  (3559.1)
- `840-611-550-060-235-032-877-740` *iṇai kuṭai vāy -iṉ vēymīn iru nālkāṇi kuṭi* : gate: Peer-Umbrella; Of the Bamboo-star-Two-Four shares house.  (2584.1)
- `844-390` *cūṭu parutti* : Sheaves-Cotton.  (2241.1)
- `844-390-400` *cūṭu parutti ciṟ* : Sheaves-Cotton, junior.  (2244.1)
- `861-002-003-140-705-255-740` *kāṇi iru mū ammai kalam mutal kuṭi* : two shares: of the Three-Lady-Ship-Chief house.  (2600.1)
- `861-002-004-390` *kāṇi iru nāl parutti* : two shares: Four cottons.  (2450.1)
- `861-002-004-407` *kāṇi iru nāl kiḷai* : two shares: Four kindreds.  (3437.1)
- `861-002-015-390` *kāṇi iru ai parutti* : two shares: Five cottons.  (2509.1)
- `861-002-031-233-520` *kāṇi iru oru vāḷai vēḷ* : two shares: One-Scabbard-fish, chief.  (3521.1)
- `861-002-032-220-520` *kāṇi iru iru mīn vēḷ* : two shares: Two-Star, chief.  (3421.1)
- `861-002-032-220-740-565-001-416` *kāṇi iru iru mīn kuṭi maṟavaṉ oru turumpu* : two shares: warrior of the Two-Star house; One grain-heap.  (2313.1)
- `861-002-061-142-740` *kāṇi iru kāl kō kuṭi* : two shares: of the Quarter-King house.  (3142.1)
- `861-002-061-151` *kāṇi iru kāl kā* : two shares: Quarter, keeper.  (3197.1)
- `861-002-125-090` *kāṇi iru vēṭṭuvaṉ āḷ* : two shares: Hunter, manager.  (3306.1)
- `861-002-140-136` *kāṇi iru ammai aṭimai* : two shares: Lady-Bondsman.  (2669.1)
- `861-002-176-151` *kāṇi iru iṟai kā* : two shares: Tax, keeper.  (2179.1)
- `861-002-176-740` *kāṇi iru iṟai kuṭi* : two shares: of the Tax house.  (2323.1)
- `861-002-176-740-090` *kāṇi iru iṟai kuṭi āḷ* : two shares: manager of the Tax house.  (2543.1)
- `861-002-220-240-440-760-740` *kāṇi iru mīn mīmīn koḷ maka kuṭi* : two shares: of the Star-High-star child of Received house.  (2277.1)
- `861-002-220-520` *kāṇi iru mīn vēḷ* : two shares: Star, chief.  (3509.1)
- `861-002-231-804` *kāṇi iru orumīn ilai* : two shares: First-star-Leaf.  (3208.1)
- `861-002-233-001-760-740` *kāṇi iru vāḷai oru maka kuṭi* : two shares: of the Scabbard-fish-One-Child of house.  (3908.1)
- `861-002-233-335-740` *kāṇi iru vāḷai ūr kuṭi* : two shares: of the Scabbard-fish-Town house.  (3486.1)
- `861-002-235-555-526` *kāṇi iru vēymīn vāy kāval* : two shares: Bamboo-star-Gate-Guard.  (3329.1)
- `861-002-235-590-390-740` *kāṇi iru vēymīn peṭṭi parutti kuṭi* : two shares: of the Bamboo-star-Boxed-cotton house.  (3648.1)
- `861-002-235-740-679` *kāṇi iru vēymīn kuṭi kaṭṭil* : two shares: throne of the Bamboo-star house.  (3096.1)
- `861-002-235-760-740` *kāṇi iru vēymīn maka kuṭi* : two shares: of the child of Bamboo-star house.  (2575.1)
- `861-002-235-840-032-740` *kāṇi iru vēymīn iṇai iru kuṭi* : two shares: of the Bamboo-star-Peer-Two house.  (3513.1)
- `861-002-240-415-100-740-090` *kāṇi iru mīmīn kavar mutu kuṭi āḷ* : two shares: manager of the High-star-Branch-Elder house.  (2724.1)
- `861-002-240-495-615-740` *kāṇi iru mīmīn kompu vayal kuṭi* : two shares: of the High-star-Horn-Field house.  (2276.1)
- `861-002-240-519-760-740` *kāṇi iru mīmīn vēli maka kuṭi* : two shares: of the High-star child of Fence house.  (2256.1)
- `861-002-240-923-101-740-140-845-407` *kāṇi iru mīmīn maruppu mutu kuṭi ammai cūṭu kiḷai* : two shares: lady of the High-star-Ivory-Elder house; Sheaf-bundle; Kindred.  (2536.1)
- `861-002-255-435-690-740` *kāṇi iru mutal kōl piṇai kuṭi* : two shares: of the Chief-Rod-Ally house.  (3556.2)
- `861-002-415-220-705-033-520` *kāṇi iru kavar mīn kalam mū vēḷ* : two shares: Branch-Star, chief (allowance: three kalam).  (2178.1)
- `861-002-519-740` *kāṇi iru vēli kuṭi* : two shares: of the Fence house.  (2845.1)
- `861-002-550-233-017-575-740` *kāṇi iru vāy vāḷai ēḻu kōṭṭai kuṭi* : two shares: of the Gate-Scabbard-fish house (allowance: seven great measures).  (4010.1)
- `861-002-590-390-161` *kāṇi iru peṭṭi parutti kā* : two shares: Boxed-cotton-Keeper.  (3226.1)
- `861-002-605-760-740` *kāṇi iru kutir maka kuṭi* : two shares: of the child of Granary house.  (2251.1)
- `861-002-705-255-740` *kāṇi iru kalam mutal kuṭi* : two shares: of the Ship-Chief house.  (3199.1)
- `861-002-705-255-740-090` *kāṇi iru kalam mutal kuṭi āḷ* : two shares: manager of the Ship-Chief house.  (2627.1)
- `861-002-706-033-520` *kāṇi iru kalam mū vēḷ* : two shares: Chief (allowance: three kalam).  (3195.1)
- `861-002-772-740` *kāṇi iru maka kuṭi* : two shares: of the Child of house.  (2679.1)
- `861-002-798-233-070-520` *kāṇi iru maru- vāḷai ampu vēḷ* : two shares: Descendant-Scabbard-fish-Arrow, chief.  (3228.1)
- `861-002-798-240-176-740-679` *kāṇi iru maru- mīmīn iṟai kuṭi kaṭṭil* : two shares: throne of the Descendant-High-star-Tax house.  (3080.1)
- `861-002-798-240-235-388-740` *kāṇi iru maru- mīmīn vēymīn aracu kuṭi* : two shares: of the Descendant-High-star-Bamboo-star-King house.  (3207.1)
- `861-002-798-415-220-705-033-752-031-590-407-740` *kāṇi iru maru- kavar mīn kalam mū maka oru peṭṭi kiḷai kuṭi* : two shares: of the Descendant-Branch-Star-Child of-One-Chest-Kindred house (allowance: three kalam).  (2422.1)
- `861-002-803-233-705-033-772-740` *kāṇi iru il vāḷai kalam mū maka kuṭi* : two shares: of the Home-Scabbard-fish-Child of house (allowance: three kalam).  (2645.1)
- `861-002-806-240-844-390` *kāṇi iru viḷai mīmīn cūṭu parutti* : two shares: Bounty-High-star-Sheaves-Cotton.  (2691.1)
- `861-002-900-590-390-151` *kāṇi iru tiṅkaḷ peṭṭi parutti kā* : two shares: Moon-Boxed-cotton, keeper.  (3246.1)
- `861-368-001-803-235-520` *kāṇi koṭi oru il vēymīn vēḷ* : share: Banner-One-Home-Bamboo-star, chief.  (3219.1)
- `861-368-231-520-495-590-070-892` *kāṇi koṭi orumīn vēḷ kompu peṭṭi ampu vil* : share: Banner-First-star-Chief-Horn-Chest-Arrow-Sale.  (3299.1)
- `861-455-740-840-032-740` *kāṇi ampu kuṭi iṇai iru kuṭi* : share: of the Arrow house; Of the Peer-Two house.  (2413.1)
- `861-740-031-243-617` *kāṇi kuṭi oru kayal ūḻiyaṉ* : share: of the house; One Carp; King's servant.  (2346.1)
- `861-741-032-070-061-406-923-740` *kāṇi orukuṭi iru ampu kāl kiḷai maruppu kuṭi* : share: of the First-ward-Two-Arrow-Quarter-Kindred-Ivory house.  (2695.1)
- `877-003-156` *nālkāṇi mū kā* : Three four shares; Keeper.  (2407.1)
- `877-005-900-740` *nālkāṇi ai tiṅkaḷ kuṭi* : Of the Four shares-Five-Moon house.  (3560.1)
- `877-061-740` *nālkāṇi kāl kuṭi* : Of the Four shares-Quarter house.  (2440.1)
- `877-820-032` *nālkāṇi kāl iru* : Four shares; Two quarters.  (3614.1)
- `892-031-002-031-055-821-368` *vil oru iru oru paṉṉiru mañcāṭi koṭi* : Sale-Four-Twelve-Mañcāṭi weight, standard-bearer.  (2393.1)
- `892-741-235-240-151` *vil orukuṭi vēymīn mīmīn kā* : Sale-First-ward-Bamboo-star-High-star, keeper.  (2254.1)
- `900-017-585-740` *tiṅkaḷ ēḻu kaṉṉi? kuṭi* : Of the Moon-Seven-Maiden house.  (2625.1)
- `920-060-003-390` *tiṅkaḷ? -iṉ mū parutti* : month: Three cottons.  (2812.1)
- `920-060-741-002-140-740` *tiṅkaḷ? -iṉ orukuṭi iru ammai kuṭi* : month in first ward: of the Two-Lady house.  (3485.1)
- `920-060-741-003-220-520` *tiṅkaḷ? -iṉ orukuṭi mū mīn vēḷ* : month in first ward: Three-Star, chief.  (2516.1)
- `920-060-741-017-390` *tiṅkaḷ? -iṉ orukuṭi ēḻu parutti* : month in first ward: Seven cottons.  (2770.1)
- `920-060-741-233-235-100-740` *tiṅkaḷ? -iṉ orukuṭi vāḷai vēymīn mutu kuṭi* : month in first ward: of the Scabbard-fish-Bamboo-star-Elder house.  (3091.1)
- `920-060-741-235-904-740` *tiṅkaḷ? -iṉ orukuṭi vēymīn irutiṅkaḷ kuṭi* : month in first ward: of the Bamboo-star-Dark-moon house.  (2844.1)
- `920-060-741-416-740` *tiṅkaḷ? -iṉ orukuṭi turumpu kuṭi* : month in first ward: of the Grain-heap house.  (3364.1)
- `920-060-741-440-740` *tiṅkaḷ? -iṉ orukuṭi koḷ kuṭi* : month in first ward: of the Received house.  (2192.1)
- `920-060-741-460-740` *tiṅkaḷ? -iṉ orukuṭi mukkōṭu kuṭi* : month in first ward: of the Three-peaks house.  (3280.1)
- `920-060-741-550-527` *tiṅkaḷ? -iṉ orukuṭi vāy kāval* : month in first ward: Gate-Guard.  (3358.1)
- `920-060-741-590-390-151` *tiṅkaḷ? -iṉ orukuṭi peṭṭi parutti kā* : month in first ward: Boxed-cotton, keeper.  (2344.1)
- `920-060-741-840-032-740` *tiṅkaḷ? -iṉ orukuṭi iṇai iru kuṭi* : month in first ward: of the Peer-Two house.  (2640.1)
- `920-060-741-927-740` *tiṅkaḷ? -iṉ orukuṭi irutiṅkaḷ kuṭi* : month in first ward: of the Two-moons house.  (3367.1)
- `920-060-742-003-368` *tiṅkaḷ? -iṉ irukuṭi mū koṭi* : month in second ward: Three banners.  (2587.1)
- `920-060-742-440-001-100-740` *tiṅkaḷ? -iṉ irukuṭi koḷ oru mutu kuṭi* : month in second ward: of the Received-One-Elder house.  (2493.1)
- `920-060-742-705-760-740` *tiṅkaḷ? -iṉ irukuṭi kalam maka kuṭi* : month in second ward: of the child of Ship house.  (3177.1)
- `920-060-742-798-032-226` *tiṅkaḷ? -iṉ irukuṭi maru- iru kūṭumīn* : month in second ward: Descendant; Two fish-crates.  (2883.1)
- `920-060-742-806-415-220-240-255-435-690-740` *tiṅkaḷ? -iṉ irukuṭi viḷai kavar mīn mīmīn mutal kōl piṇai kuṭi* : month in second ward: of the Bounty-Branch-Star-High-star-Chief-Rod-Ally house.  (2865.1)
- `920-060-745-235-240-255-435-690-740` *tiṅkaḷ? -iṉ mukuṭi vēymīn mīmīn mutal kōl piṇai kuṭi* : month in third ward: of the Bamboo-star-High-star-Chief-Rod-Ally house.  (3110.1)
- `920-060-745-415-100-740` *tiṅkaḷ? -iṉ mukuṭi kavar mutu kuṭi* : month in third ward: of the Branch-Elder house.  (2859.1)
- `920-156-002-003-140-100-740` *tiṅkaḷ? kā iru mū ammai mutu kuṭi* : Of the Month-Keeper-Five-Lady-Elder house.  (2310.1)
- `920-368-060-463-820-390` *tiṅkaḷ? koṭi -iṉ mukkōṭu kāl parutti* : Month-Banner-Inner-Three-peaks-Quarter-Cotton.  (2576.1)
- `920-615-742-921-070-520` *tiṅkaḷ? vayal irukuṭi vil ampu vēḷ* : Month-Field-Second-ward-Bow-Arrow, chief.  (3579.1)
- `923-740` *maruppu kuṭi* : Of the Ivory house.  (3258.1)
- `923-740-001-016-407` *maruppu kuṭi oru āṟu kiḷai* : Of the Ivory house; Seven kindreds.  (3619.1)
- `927-740` *irutiṅkaḷ kuṭi* : Of the Two-moons house.  (3535.1)

**tablet** (80 faces)

- `630-740` *pal kuṭi* : Of the Many house.  (9 copies: 2246.1, 2944.1, 2945.1, 2946.1, 2948.1, 3698.1, 3699.1, 3700.1, 3701.1)
- `104-645-590-235-240-740-090` *taṭṭāṉ kar̤añcu peṭṭi vēymīn mīmīn kuṭi āḷ* : Manager of the Goldsmith-Gold weight-Chest-Bamboo-star-High-star house.  (7 copies: 2380.1, 2949.1, 2950.1, 2951.1, 2952.1, 3703.1, 3704.1)
- `004-700-097-400` *nāl nāḻi? aṭimai ciṟ* : Bondsman, junior (allowance: four cups).  (4 copies: 2962.1, 2963.1, 2964.1, 3710.1)
- `550-060-690-740` *vāy -iṉ piṇai kuṭi* : gate: of the Ally house.  (4 copies: 2322.2, 2382.2, 3725.2, 3726.2)
- `384-740` *aracu kuṭi* : Of the King house.  (3 copies: 3714.1, 3714.2, 3714.3)
- `705-167` *kalam kūli* : Kalam, wages.  (3 copies: 2367.1, 2367.2, 3689.1)
- `003-220-740` *mū mīn kuṭi* : Of the Three-Star house.  (2 copies: 3720.1, 3723.1)
- `016-840-002-803-140-850` *āṟu iṇai iru il ammai kāṇi* : Six lots of two pairs; House; Lady, share.  (2 copies: 2972.1, 2973.1)
- `142-617` *kō ūḻiyaṉ* : King, king's servant.  (2 copies: 2252.1, 2960.1)
- `235-520` *vēymīn vēḷ* : Bamboo-star, chief.  (2 copies: 2969.1, 2970.1)
- `323-690` *paṭi piṇai* : Ration, bound.  (2 copies: 3725.1, 3726.1)
- `370-390` *katir parutti* : Spindle, cotton.  (2 copies: 3846.1, 3846.2)
- `540` *paṟai* : Rice measure.  (2 copies: 2955.1, 3706.1)
- `705-033-590-390-740` *kalam mū peṭṭi parutti kuṭi* : Of the Boxed-cotton house (allowance: three kalam).  (2 copies: 2925.1, 2926.1)
- `706-167` *kalam kūli* : Kalam, wages.  (2 copies: 2934.1, 2934.2)
- `798-415-220-740-400` *maru- kavar mīn kuṭi ciṟ* : Junior of the Descendant-Branch-Star house.  (2 copies: 2953.1, 2954.1)
- `803-335-760-740` *il ūr maka kuṭi* : Of the Home child of Town house.  (2 copies: 2436.1, 3696.1)
- `838-798-176-740-151-697-390` *viḷai maru- iṟai kuṭi kā ney parutti* : Keeper of the Produce-Descendant-Tax house; Woven; Cotton.  (2 copies: 2975.1, 2976.1)
- `140-136-400-255-435-016-615` *ammai aṭimai ciṟ mutal kōl āṟu vayal* : Lady, bondsman, junior, chief; Six rods; Field.  (2971.1)
- `220-100-740` *mīn mutu kuṭi* : Of the Star-Elder house.  (2958.1)
- `220-798-550-527` *mīn maru- vāy kāval* : Star, descendant, gate, guard.  (2432.2)
- `220-840-032-740` *mīn iṇai iru kuṭi* : Of the Star-Peer-Two house.  (2432.1)
- `235-176-740` *vēymīn iṟai kuṭi* : Of the Bamboo-star-Tax house.  (2931.1)
- `240-415-100-740` *mīmīn kavar mutu kuṭi* : Of the High-star-Branch-Elder house.  (3705.2)
- `240-803-585-740` *mīmīn il kaṉṉi? kuṭi* : Of the High-star-Home-Maiden house.  (4020.1)
- `240-803-585-740-090` *mīmīn il kaṉṉi? kuṭi āḷ* : Manager of the High-star-Home-Maiden house.  (2974.2)
- `255-435-690-740` *mutal kōl piṇai kuṭi* : Of the Chief-Rod-Ally house.  (2940.1)
- `350-460-798-904-740-400` *kalappai mukkōṭu maru- irutiṅkaḷ kuṭi ciṟ* : Junior of the Plough-Three-peaks-Descendant-Dark-moon house.  (2956.2)
- `467-806-158-400` *(n) viḷai kā ciṟ* : N loads of produce, carried by the porter; Junior.  (3706.2)
- `473-806-158-400` *(n) viḷai kā ciṟ* : N loads of produce, carried by the porter; Junior.  (2955.2)
- `503-033-740-400` *malai mū kuṭi ciṟ* : Junior of the Hill-Three house.  (3697.1)
- `550-525-400` *vāy kāval ciṟ* : Gate-Guard, junior.  (3684.1)
- `615-740-090` *vayal kuṭi āḷ* : Manager of the Field house.  (2969.3)
- `690-323` *piṇai paṭi* : Bound, ration.  (2322.1)
- `741-904-740-820-032-017-904-415-100-740` *orukuṭi irutiṅkaḷ kuṭi kāl iru ēḻu irutiṅkaḷ kavar mutu kuṭi* : Of the First-ward-Dark-moon house; Of the Quarter-9-Dark-moon-Branch-Elder house.  (2976.3)
- `741-904-740-820-032-017-904-415-100-921` *orukuṭi irutiṅkaḷ kuṭi kāl iru ēḻu irutiṅkaḷ kavar mutu vil* : Of the First-ward-Dark-moon house; 9 quarters; Two months; Branch; Elder; Bow.  (2975.3)
- `803-003-220-740-792-740-090` *il mū mīn kuṭi aracu kuṭi āḷ* : Of the Home-Three-Star house; Manager of the Royal house.  (3713.1)
- `803-740-400` *il kuṭi ciṟ* : Junior of the Home house.  (2966.1)
- `806-235-590-405-740-400` *viḷai vēymīn peṭṭi nūl kuṭi ciṟ* : Junior of the Bounty-Bamboo-star-Chest-Thread house.  (2957.1)
- `840-032-740` *iṇai iru kuṭi* : Of the Peer-Two house.  (2511.1)
- `861-002-220-840-032-740` *kāṇi iru mīn iṇai iru kuṭi* : two shares: of the Star-Peer-Two house.  (2938.1)
- `861-002-798-415-220-036-760-740` *kāṇi iru maru- kavar mīn āṟu maka kuṭi* : two shares: of the Descendant-Branch-Star-Six-Child of house.  (3711.1)
- `927-740` *irutiṅkaḷ kuṭi* : Of the Two-moons house.  (4016.2)
- `927-740-031-095` *irutiṅkaḷ kuṭi oru kōlaṉ* : Of the Two-moons house; One staff-bearer.  (4016.1)

**tag or sealing** (9 faces)

- `003-156` *mū kā* : Three porters.  (2 copies: 2923.1, 3683.1)
- `817-002-032-760-740` *kāṇi iru iru maka kuṭi* : two shares: of the Two-Child of house.  (2 copies: 3681.1, 3681.3)
- `003-390` *mū parutti* : Three cottons.  (2408.1)
- `171-035` *niṟai ai* : Five full measures.  (2235.1)
- `820-002-590-390-740` *kāl iru peṭṭi parutti kuṭi* : two quarters: of the Boxed-cotton house.  (2929.1)
- `920-060-741-031-017-575-740` *tiṅkaḷ? -iṉ orukuṭi oru ēḻu kōṭṭai kuṭi* : month in first ward: of the house (allowance: eight great measures).  (3679.1)
- `920-060-741-415-100-740` *tiṅkaḷ? -iṉ orukuṭi kavar mutu kuṭi* : month in first ward: of the Branch-Elder house.  (2921.1)

### Dholavira

**other** (2 faces)

- `776-233` *malar vāḷai* : Bloom, Scabbard-fish.  (4244.2)
- `820-611-388-820-850-645-031-821-798` *kāl kuṭai aracu kāl kāṇi kar̤añcu oru mañcāṭi maru-* : quarter: Umbrella, king, quarter, share, gold weight; One mañcāṭi weight; Descendant.  (144.1)

**pot** (1 faces)

- `455` *ampu* : Arrow.  (5543.1)

**seal** (49 faces)

- `861-002-016-390` *kāṇi iru āṟu parutti* : two shares: Six cottons.  (2 copies: 136.1, 4260.1)
- `003-422` *mū par̤aṉam* : Three fields.  (4269.1)
- `017-590-740` *ēḻu peṭṭi kuṭi* : Of the Seven-Chest house.  (1576.1)
- `032-790-407-590` *iru maṇi kiḷai peṭṭi* : Two gems; Kindred-Chest.  (135.1)
- `032-892-151` *iru vil kā* : Two-Sale, keeper.  (127.1)
- `033-033-520` *mū mū vēḷ* : Six chiefs.  (4149.1)
- `060-820-001-240-463-220-590-390-740` *-iṉ kāl oru mīmīn mukkōṭu mīn peṭṭi parutti kuṭi* : one of  in quarter: of the High-star-Three-peaks-Star-Boxed-cotton house.  (4229.1)
- `091-500-741-240-416-840-740` *iruvar pāy orukuṭi mīmīn turumpu iṇai kuṭi* : Of the The pair-Sail-First-ward-High-star-Grain-heap-Peer house.  (2180.1)
- `104-031-002-423-001-003-423` *taṭṭāṉ oru iru par̤aṉam oru mū par̤aṉam* : Goldsmith; Three lots of four fields; Field.  (4164.1)
- `130-817` *kaḷamar kāṇi* : Husbandman-Share.  (4181.1)
- `142-151` *kō kā* : King, keeper.  (4240.1)
- `142-617` *kō ūḻiyaṉ* : King-King's servant.  (137.1)
- `151-031` *kā oru* : keeper-One.  (4223.1)
- `175-742-233-798-740` *iṟai irukuṭi vāḷai maru- kuṭi* : Of the Tax-Second-ward-Scabbard-fish-Descendant house.  (4183.1)
- `176-740-013-004-064` *iṟai kuṭi mū nāl pāti* : Of the Tax house; Seven portions.  (4161.1)
- `220-235-740` *mīn vēymīn kuṭi* : Of the Star-Bamboo-star house.  (4224.1)
- `233-001-760-740` *vāḷai oru maka kuṭi* : Of the Scabbard-fish-One-Child of house.  (4162.1)
- `233-706-033-520` *vāḷai kalam mū vēḷ* : Scabbard-fish, chief (allowance: three kalam).  (138.1)
- `235-520` *vēymīn vēḷ* : Bamboo-star, chief.  (4232.1)
- `255-220-175-760-740` *mutal mīn iṟai maka kuṭi* : Of the Chief-Star child of Tax house.  (4236.1)
- `408-005` *kiḷai ai* : Five lots.  (4190.1)
- `416` *turumpu* : Grain-heap.  (4202.1)
- `416-840-740` *turumpu iṇai kuṭi* : Of the Grain-heap-Peer house.  (4165.1)
- `460-520` *mukkōṭu vēḷ* : Three-peaks, chief.  (133.1)
- `495-460-520` *kompu mukkōṭu vēḷ* : Horn-Three-peaks, chief.  (131.1)
- `550-060-061-706-798-740` *vāy -iṉ kāl kalam maru- kuṭi* : gate: of the Quarter-Ship-Descendant house.  (4287.1)
- `590-407-100-740` *peṭṭi kiḷai mutu kuṭi* : Of the Chest-Kindred-Elder house.  (139.1)
- `592` *paṭṭi* : Pen.  (4246.1)
- `705-390-002-388-032-151` *kalam parutti iru aracu iru kā* : Ship-Cotton; Two lots of two King; Keeper.  (4237.1)
- `705-717-388-154` *kalam aṭi aracu kā* : Ship-Servant-King, keeper.  (134.1)
- `706-033-520` *kalam mū vēḷ* : Chief (allowance: three kalam).  (4167.1)
- `803-840-032-740` *il iṇai iru kuṭi* : Of the Home-Peer-Two house.  (4184.1)
- `806-455-220-013-472-806-154` *viḷai ampu mīn mū (n) viḷai kā* : Bounty-Arrow; Three Star; N loads of produce, carried by the porter.  (4194.1)
- `817-002-004-390` *kāṇi iru nāl parutti* : two shares: Four cottons.  (951.1)
- `817-002-235-100-740` *kāṇi iru vēymīn mutu kuṭi* : two shares: of the Bamboo-star-Elder house.  (4211.1)
- `817-002-590-390-740` *kāṇi iru peṭṭi parutti kuṭi* : two shares: of the Boxed-cotton house.  (2489.1)
- `817-013-104-820-031` *kāṇi mū taṭṭāṉ kāl oru* : three shares: Goldsmith; One quarter.  (5571.1)
- `824-368-098-630-740` *vilai koṭi ēvalaṉ pal kuṭi* : Of the Worth-Banner-Attendant-Many house.  (4227.1)
- `850-231` *kāṇi orumīn* : Share-First-star.  (4187.1)
- `861-002-016-405` *kāṇi iru āṟu nūl* : two shares: Six threads.  (4272.1)
- `861-002-031-382-151` *kāṇi iru oru aracu kā* : two shares: One-King, keeper.  (145.1)
- `861-002-416-740` *kāṇi iru turumpu kuṭi* : two shares: of the Grain-heap house.  (132.1)
- `861-002-590-390-820` *kāṇi iru peṭṭi parutti kāl* : two shares: Boxed-cotton-Quarter.  (4195.1)
- `861-742-520` *kāṇi irukuṭi vēḷ* : share: Second-ward, chief.  (4220.1)
- `904-530-705-002-231-590-390-740` *irutiṅkaḷ paṟai kalam iru orumīn peṭṭi parutti kuṭi* : Of the Dark-moon-Proclamation-Ship-Two-First-star-Boxed-cotton house.  (4182.1)
- `920-060-741-005-368` *tiṅkaḷ? -iṉ orukuṭi ai koṭi* : month in first ward: Five banners.  (4159.1)
- `920-060-741-142-156` *tiṅkaḷ? -iṉ orukuṭi kō kā* : month in first ward: King, keeper.  (4175.1)
- `920-740-400` *tiṅkaḷ? kuṭi ciṟ* : Junior of the Month house.  (4226.1)

**tablet** (6 faces)

- `032-220-153` *iru mīn kā* : Two Star; Porter.  (4286.1)
- `033` *mū* : Three.  (4279.1)
- `033-892` *mū vil* : Three sales.  (4258.1)
- `408-004` *kiḷai nāl* : Four lots.  (4242.1)
- `421-003-440-776` *par̤aṉam mū koḷ malar* : Field; Three receiveds; Bloom.  (4166.1)
- `630-900-002-519-740` *pal tiṅkaḷ iru vēli kuṭi* : Of the Many-Moon-Two-Fence house.  (4302.1)

**tag or sealing** (8 faces)

- `032` *iru* : Two.  (6 copies: 748.1, 4293.1, 4350.1, 4351.1, 4352.1, 4353.1)
- `033-136` *mū aṭimai* : Three bondsmans.  (4301.1)
- `220-740` *mīn kuṭi* : Of the Star house.  (3952.1)

### Kalibangan

**copper tablet** (1 faces)

- `798-740` *maru- kuṭi* : Of the Descendant house.  (5284.1)

**other** (12 faces)

- `480` *kuṉṟi* : Seed-weight.  (5 copies: 5489.1, 5490.1, 5491.1, 5492.1, 5496.1)
- `003-064` *mū pāti* : Three portions.  (5501.1)
- `013-840-740` *mū iṇai kuṭi* : Of the Three-Peer house.  (5495.1)
- `220` *mīn* : Star.  (5351.1)
- `413` *nel* : Grain.  (5485.1)
- `540` *paṟai* : Rice measure.  (5488.1)
- `550-060-165-740` *vāy -iṉ nāḷ kuṭi* : gate: of the Day house.  (1919.1)
- `850` *kāṇi* : Share.  (5493.1)

**pot** (13 faces)

- `032` *iru* : Two.  (2 copies: 1945.2, 5287.1)
- `390` *parutti* : Cotton.  (2 copies: 5307.1, 5345.1)
- `003-158` *mū kā* : Three porters.  (5311.1)
- `003-405` *mū nūl* : Three threads.  (1951.1)
- `017-390` *ēḻu parutti* : Seven cottons.  (5316.1)
- `031-032` *oru iru* : Three.  (5290.1)
- `033` *mū* : Three.  (5482.1)
- `033-033-034` *mū mū nāl* : 10.  (5308.1)
- `035` *ai* : Five.  (5295.1)
- `700-798-740` *nāḻi? maru- kuṭi* : Of the Cup-Descendant house.  (1945.1)
- `817-031` *kāṇi oru* : one share.  (5341.1)

**seal** (21 faces)

- `003-017-151` *mū ēḻu kā* : 10-keeper.  (1912.1)
- `003-390` *mū parutti* : Three cottons.  (1924.1)
- `004-390` *nāl parutti* : Four cottons.  (1913.1)
- `005-405` *ai nūl* : Five threads.  (1894.1)
- `006-220-520` *āṟu mīn vēḷ* : Six-Star, chief.  (5277.1)
- `061-151` *kāl kā* : Quarter, keeper.  (5280.1)
- `125-741-803-240-233-520` *vēṭṭuvaṉ orukuṭi il mīmīn vāḷai vēḷ* : Hunter-First-ward-Home-High-star-Scabbard-fish, chief.  (1880.1)
- `231-520` *orumīn vēḷ* : First-star, chief.  (1967.1)
- `368-032-590-861-368-002-255-435-690-740` *koṭi iru peṭṭi kāṇi koṭi iru mutal kōl piṇai kuṭi* : Of the Banner-Two-Chest-Tribute-Banner-Two-Chief-Rod-Ally house.  (1885.1)
- `384` *aracu* : King.  (1925.1)
- `390-590` *parutti peṭṭi* : Cotton-Chest.  (1907.1)
- `495-776-740-400` *kompu malar kuṭi ciṟ* : Junior of the Horn-Bloom house.  (1876.1)
- `630-741-017-585-740` *pal orukuṭi ēḻu kaṉṉi? kuṭi* : Of the Many-First-ward-Seven-Maiden house.  (1888.1)
- `690-740` *piṇai kuṭi* : Of the Ally house.  (1922.1)
- `741-530-455-220-001-838-176-100-740` *orukuṭi paṟai ampu mīn oru viḷai iṟai mutu kuṭi* : Of the First-ward-Proclamation-Arrow-Star-One-Produce-Tax-Elder house.  (1882.1)
- `803-233-176-740` *il vāḷai iṟai kuṭi* : Of the Home-Scabbard-fish-Tax house.  (1923.1)
- `817-002` *kāṇi iru* : two shares.  (1901.1)
- `820-002-032-220-231-585-740` *kāl iru iru mīn orumīn kaṉṉi? kuṭi* : two quarters: of the Two-Star-First-star-Maiden house.  (5273.1)
- `861-002-226` *kāṇi iru kūṭumīn* : two shares: Fish-crate.  (1906.1)
- `892-031-013-015` *vil oru mū ai* : 9 sales.  (1920.1)
- `900-790-415-717-740` *tiṅkaḷ maṇi kavar aṭi kuṭi* : Of the Moon-Gem-Branch-Servant house.  (1886.1)

**tablet** (3 faces)

- `032-700` *iru nāḻi?* : Two cups.  (1926.2)
- `384` *aracu* : King.  (5352.1)
- `820-002-390-817-740` *kāl iru parutti kāṇi kuṭi* : two quarters: of the Cotton-Share house.  (1935.1)

**tag or sealing** (2 faces)

- `861-002-003-390` *kāṇi iru mū parutti* : two shares: Three cottons.  (1938.1)
- `861-002-033-520` *kāṇi iru mū vēḷ* : two shares: Three chiefs.  (1940.1)

**tool** (1 faces)

- `005` *ai* : Five.  (1966.2)

### Lothal

**pot** (4 faces)

- `240-031-156` *mīmīn oru kā* : High-star; One porter.  (2149.1)
- `480-001-790` *kuṉṟi oru maṇi* : One seed-weight; Gem.  (2152.1)
- `480-032-877` *kuṉṟi iru nālkāṇi* : Two seed-weights; Four shares.  (2138.1)
- `740` *kuṭi* : Of the house.  (2143.1)

**seal** (37 faces)

- `233-176-740` *vāḷai iṟai kuṭi* : Of the Scabbard-fish-Tax house.  (2 copies: 2008.1, 2022.1)
- `003-156` *mū kā* : Three-keeper.  (2014.1)
- `004-154` *nāl kā* : Four-keeper.  (1994.1)
- `005-154` *ai kā* : Five-keeper.  (2054.1)
- `013` *mū* : Three.  (2032.1)
- `013-840-740` *mū iṇai kuṭi* : Of the Three-Peer house.  (2000.1)
- `031-575-002-233-100-740-090` *oru kōṭṭai iru vāḷai mutu kuṭi āḷ* : Manager of the Scabbard-fish-Elder house (allowance: one lot of two great measures).  (1986.1)
- `032-140` *iru ammai* : Two ladies.  (2066.1)
- `140-407-060-003-423` *ammai kiḷai -iṉ mū par̤aṉam* : Lady-Kindred; Three ofs; Field.  (2044.1)
- `140-861-740` *ammai kāṇi kuṭi* : Of the Lady-Tribute house.  (2027.1)
- `220` *mīn* : Star.  (2032.4)
- `220-100-151` *mīn mutu kā* : Star-Elder, keeper.  (2011.1)
- `235-231-555-527` *vēymīn orumīn vāy kāval* : Bamboo-star-First-star-Gate-Guard.  (2020.1)
- `235-240-904-740` *vēymīn mīmīn irutiṅkaḷ kuṭi* : Of the Bamboo-star-High-star-Dark-moon house.  (2060.1)
- `235-482-740` *vēymīn kōṭukāṇi kuṭi* : Of the Bamboo-star-Hill-share house.  (2001.1)
- `235-555-526` *vēymīn vāy kāval* : Bamboo-star-Gate-Guard.  (1988.1)
- `390-590-151` *parutti peṭṭi kā* : Cotton-Chest, keeper.  (2015.1)
- `406-390-892-104` *kiḷai parutti vil taṭṭāṉ* : Kindred-Cotton-Sale-Goldsmith.  (2010.1)
- `491-004-390` *kompu nāl parutti* : Horn; Four cottons.  (1998.1)
- `519-415-220-520` *vēli kavar mīn vēḷ* : Fence-Branch-Star, chief.  (2052.1)
- `550` *vāy* : Gate.  (2058.1)
- `550-527` *vāy kāval* : Gate-Guard.  (2021.1)
- `550-740` *vāy kuṭi* : Of the Gate house.  (2025.1)
- `575` *kōṭṭai* : Great measure.  (5506.2)
- `590-540-002-605-760-740` *peṭṭi paṟai iru kutir maka kuṭi* : Of the Chest-Drum-Two-Granary-Child of house.  (2061.1)
- `817-002-048` *kāṇi iru er̤uvar* : two shares: Seven.  (2038.1)
- `817-002-233-740-090` *kāṇi iru vāḷai kuṭi āḷ* : two shares: manager of the Scabbard-fish house.  (2013.1)
- `820-002-031-415` *kāl iru oru kavar* : two quarters: One Branch.  (1996.1)
- `820-002-240-806-740` *kāl iru mīmīn viḷai kuṭi* : two quarters: of the High-star-Bounty house.  (2037.1)
- `820-060-142-156` *kāl -iṉ kō kā* : quarter: King, keeper.  (1999.1)
- `824-002-416` *vilai iru turumpu* : worth two: Grain-heap.  (2045.1)
- `840-032-740` *iṇai iru kuṭi* : Of the Peer-Two house.  (2026.1)
- `861-002-235-555-527` *kāṇi iru vēymīn vāy kāval* : two shares: Bamboo-star-Gate-Guard.  (2043.1)
- `861-368-480-003-390` *kāṇi koṭi kuṉṟi mū parutti* : share: Banner-Seed-weight; Three cottons.  (2006.1)
- `920-060-741-590-406-740` *tiṅkaḷ? -iṉ orukuṭi peṭṭi kiḷai kuṭi* : month in first ward: of the Chest-Kindred house.  (2005.1)
- `920-060-803-032-220-904-590-407-740` *tiṅkaḷ? -iṉ il iru mīn irutiṅkaḷ peṭṭi kiḷai kuṭi* : month: of the Home-Two-Star-Dark-moon-Chest-Kindred house.  (2063.1)

**tablet** (2 faces)

- `700` *nāḻi?* : Cup.  (2133.1)
- `920-060-741-821-740` *tiṅkaḷ? -iṉ orukuṭi mañcāṭi kuṭi* : month in first ward: of the Mañcāṭi weight house.  (2133.3)

**tag or sealing** (28 faces)

- `705-500-741-001-055-220-740-090` *kalam pāy orukuṭi oru paṉṉiru mīn kuṭi āḷ* : Manager of the Ship-Sail-First-ward-One-Twelve-Star house.  (11 copies: 2068.1, 2069.1, 2070.1, 2071.1, 2072.1, 2112.1, 2113.1, 2115.1, 2117.1, 2125.1, 5388.1)
- `817-002-048-740` *kāṇi iru er̤uvar kuṭi* : two shares: of the Seven house.  (10 copies: 2093.1, 2094.1, 2095.1, 2096.1, 2097.1, 2098.1, 2099.1, 2100.1, 2101.1, 2102.1)
- `550-002-415-390` *vāy iru kavar parutti* : Gate; Two Branch; Cotton.  (2087.1)
- `617-002-240-220-233-520` *ūḻiyaṉ iru mīmīn mīn vāḷai vēḷ* : King's servant-Two-High-star-Star-Scabbard-fish, chief.  (2077.1)
- `692-031-001-015-140` *kūṭṭam oru oru ai ammai* : Assembly; Seven ladies.  (2084.1)
- `705-033-520` *kalam mū vēḷ* : Chief (allowance: three kalam).  (2088.1)
- `820-002-482-740` *kāl iru kōṭukāṇi kuṭi* : two quarters: of the Hill-share house.  (2126.1)
- `861-013-100` *kāṇi mū mutu* : three shares: Elder.  (2136.1)
- `920-060-004-220-388-740` *tiṅkaḷ? -iṉ nāl mīn aracu kuṭi* : month: of the Four-Star-King house.  (2085.1)

### Chanhu-daro

**other** (1 faces)

- `503-463-740` *malai mukkōṭu kuṭi* : Of the Hill-Three-peaks house.  (5272.1)

**pot** (1 faces)

- `540` *paṟai* : Rice measure.  (4816.1)

**seal** (21 faces)

- `031-920-400-740` *oru tiṅkaḷ? ciṟ kuṭi* : Of the One-Month-Junior house.  (103.1)
- `055-161` *paṉṉiru kā* : Twelve-Keeper.  (85.1)
- `100-740` *mutu kuṭi* : Of the Elder house.  (105.1)
- `235-482-740` *vēymīn kōṭukāṇi kuṭi* : Of the Bamboo-star-Hill-share house.  (65.1)
- `240-100-740-151` *mīmīn mutu kuṭi kā* : Keeper of the High-star-Elder house.  (77.1)
- `240-705-033-803-233-151` *mīmīn kalam mū il vāḷai kā* : High-star-Home-Scabbard-fish, keeper (allowance: three kalam).  (97.1)
- `388-526` *aracu kāval* : King-Guard.  (80.1)
- `495-790-031-790-151` *kompu maṇi oru maṇi kā* : Horn-Gem-One-Gem, keeper.  (107.1)
- `590-390-740` *peṭṭi parutti kuṭi* : Of the Boxed-cotton house.  (90.1)
- `679` *kaṭṭil* : Throne.  (59.1)
- `700-892` *nāḻi? vil* : The Measurer; Sale.  (60.1)
- `717-575-060-844-390` *aṭi kōṭṭai -iṉ cūṭu parutti* : Servant-Great measure-Inner-Sheaves-Cotton.  (66.1)
- `817-002-003-390` *kāṇi iru mū parutti* : two shares: Three cottons.  (61.1)
- `817-002-032-220-231-740` *kāṇi iru iru mīn orumīn kuṭi* : two shares: of the Two-Star-First-star house.  (98.1)
- `817-002-803-233-520` *kāṇi iru il vāḷai vēḷ* : two shares: Home-Scabbard-fish, chief.  (87.1)
- `817-002-803-235-520` *kāṇi iru il vēymīn vēḷ* : two shares: Home-Bamboo-star, chief.  (92.1)
- `817-014-226` *kāṇi nāl kūṭumīn* : four shares: Fish-crate.  (75.1)
- `861-002-032-176-740` *kāṇi iru iru iṟai kuṭi* : two shares: of the house (allowance: two taxs).  (69.1)
- `861-002-125` *kāṇi iru vēṭṭuvaṉ* : two shares: Hunter.  (76.1)
- `920-060-031-592-031-032-842` *tiṅkaḷ? -iṉ oru paṭṭi oru iru tuṇai* : month: One lot of three pens; Deputy.  (64.1)
- `920-060-740-031-590-390-161` *tiṅkaḷ? -iṉ kuṭi oru peṭṭi parutti kā* : month: of the house; One chest; Cotton; Keeper.  (100.1)

**tablet** (1 faces)

- `167-705-031` *kūli kalam oru* : Wages; One kalam.  (56.1)

**tag or sealing** (1 faces)

- `405-740` *nūl kuṭi* : Of the Thread house.  (57.1)

### Nausharo

**pot** (9 faces)

- `031` *oru* : One.  (2 copies: 5374.1, 5375.1)
- `003-226` *mū kūṭumīn* : Three fish-crates.  (5382.1)
- `031-001` *oru oru* : Two.  (5371.1)
- `031-645` *oru kar̤añcu* : One gold weight.  (5370.1)
- `032` *iru* : Two.  (5380.1)
- `034` *nāl* : Four.  (5373.1)
- `861-740` *kāṇi kuṭi* : share: of the house.  (5369.1)
- `861-742` *kāṇi irukuṭi* : share: Second-ward house.  (5378.1)

**seal** (7 faces)

- `032-760-740` *iru maka kuṭi* : Of the Two-Child of house.  (5359.1)
- `495-033-740` *kompu mū kuṭi* : Of the Horn-Three house.  (3856.1)
- `790-390` *maṇi parutti* : Gem-Cotton.  (5353.1)
- `817-002-222-740` *kāṇi iru aṭaimīn kuṭi* : two shares: of the Shut-in-fish house.  (5356.1)
- `820-002-003-390` *kāl iru mū parutti* : two quarters: Three cottons.  (3855.1)
- `820-002-016-220-740-090` *kāl iru āṟu mīn kuṭi āḷ* : two quarters: manager of the Six-Star house.  (3853.1)
- `920-060-742-220-520` *tiṅkaḷ? -iṉ irukuṭi mīn vēḷ* : month in second ward: Star, chief.  (5360.1)

### Unknown

**seal** (10 faces)

- `031-920-060-927-415-100-740` *oru tiṅkaḷ? -iṉ irutiṅkaḷ kavar mutu kuṭi* : month: One; Of the Two-moons-Branch-Elder house.  (3891.1)
- `142-400-151` *kō ciṟ kā* : King-Junior, keeper.  (5428.1)
- `171-035-130-060-017-154-740` *niṟai ai kaḷamar -iṉ ēḻu kā kuṭi* : Of the Husbandman-Inner-Seven-Keeper house (allowance: five full measures).  (5586.1)
- `370-031-741-840-390` *katir oru orukuṭi iṇai parutti* : One spindle; First-ward-Peer-Cotton.  (5465.1)
- `467-550-001-740-740` *(n) vāy oru kuṭi kuṭi* : Of the house (allowance: n lot of one gate); Of the house.  (3889.1)
- `820-002-235-222-740` *kāl iru vēymīn aṭaimīn kuṭi* : two quarters: of the Bamboo-star-Shut-in-fish house.  (3896.1)
- `820-060-240-231-585-740` *kāl -iṉ mīmīn orumīn kaṉṉi? kuṭi* : quarter: of the High-star-First-star-Maiden house.  (3890.1)
- `824-002-104-415-368` *vilai iru taṭṭāṉ kavar koṭi* : worth two: Goldsmith-Branch, standard-bearer.  (5576.1)
- `861-002-136` *kāṇi iru aṭimai* : two shares: Bondsman.  (5575.1)
- `900-590-368-002` *tiṅkaḷ peṭṭi koṭi iru* : Moon-Chest; Two banners.  (3892.1)

**tablet** (2 faces)

- `032-700` *iru nāḻi?* : Two cups.  (3895.2)
- `820-002-233-555` *kāl iru vāḷai vāy* : two quarters: Scabbard-fish, gate.  (3894.1)

### Banawali

**seal** (11 faces)

- `817-002` *kāṇi iru* : two shares.  (3 copies: 30.1, 31.1, 36.1)
- `001-520` *oru vēḷ* : One chief.  (2 copies: 26.1, 5441.1)
- `004-390` *nāl parutti* : Four cottons.  (33.1)
- `007` *ēḻu* : Seven.  (34.1)
- `014-220` *nāl mīn* : Four Star.  (28.1)
- `061-740` *kāl kuṭi* : Of the Quarter house.  (32.1)
- `803-740` *il kuṭi* : Of the Home house.  (39.1)
- `821-550-368-002-220-740-090` *mañcāṭi vāy koṭi iru mīn kuṭi āḷ* : Manager of the Mañcāṭi weight-Gate-Banner-Two-Star house.  (27.1)

### Lakhanjo-daro

**seal** (1 faces)

- `061-740` *kāl kuṭi* : Of the Quarter house.  (5234.1)

**tablet** (3 faces)

- `156` *kā* : Keeper.  (5242.1)
- `382-382-382` *aracu aracu aracu* : Three kings.  (5242.2)
- `740` *kuṭi* : Of the house.  (5241.1)

**tag or sealing** (2 faces)

- `706-740` *kalam kuṭi* : Of the Ship house.  (2 copies: 5244.1, 5245.1)

### Rakhigarhi

**pot** (1 faces)

- `520-382` *vēḷ aracu* : Chief, king.  (5563.1)

**seal** (1 faces)

- `920-060-741-335-760-740` *tiṅkaḷ? -iṉ orukuṭi ūr maka kuṭi* : month in first ward: of the child of Town house.  (3869.1)

**tag or sealing** (2 faces)

- `820-032-130` *kāl iru kaḷamar* : two quarters: Husbandman.  (2 copies: 3868.1, 3868.2)

### Allahdino

**seal** (3 faces)

- `033-125-390-368` *mū vēṭṭuvaṉ parutti koṭi* : Three-Hunter-Cotton, standard-bearer.  (7.1)
- `235-705-033-904-740` *vēymīn kalam mū irutiṅkaḷ kuṭi* : Of the Bamboo-star-Dark-moon house (allowance: three kalam).  (8.1)
- `590-390-740` *peṭṭi parutti kuṭi* : Of the Boxed-cotton house.  (6.1)

**tag or sealing** (1 faces)

- `235-740` *vēymīn kuṭi* : Of the Bamboo-star house.  (5.1)

### Kot-Diji

**pot** (3 faces)

- `003-033` *mū mū* : Six.  (1978.1)
- `095-033` *kōlaṉ mū* : Three staff-bearers.  (1974.1)
- `463` *mukkōṭu* : Three-peaks.  (1980.1)

### Kanmer

**pot** (1 faces)

- `220` *mīn* : Star.  (5452.1)

**seal** (1 faces)

- `031-520` *oru vēḷ* : One chief.  (5421.1)

**tool** (3 faces)

- `031-136` *oru aṭimai* : One bondsman.  (3 copies: 3900.1, 3901.1, 3902.1)

### Karanpura

**other** (5 faces)

- `390` *parutti* : Cotton.  (5 copies: 276.1, 1757.1, 5568.1, 5569.1, 5570.1)

**seal** (1 faces)

- `820-415` *kāl kavar* : quarter: Branch.  (5453.1)

### Shikarpur

**seal** (1 faces)

- `861-921-098-220-335` *kāṇi vil ēvalaṉ mīn ūr* : share: Bow-Attendant-Star-Town.  (5451.1)

### Farmana

**seal** (4 faces)

- `371-390` *katir parutti* : Spindle-Cotton.  (2 copies: 153.1, 153.2)
- `032-220` *iru mīn* : Two Star.  (151.1)
- `220-240` *mīn mīmīn* : Star-High-star.  (149.1)

### Bala-kot

**bangle** (1 faces)

- `798-740` *maru- kuṭi* : Of the Descendant house.  (23.1)

**pot** (1 faces)

- `033-820` *mū kāl* : Three quarters.  (5542.1)

**seal** (1 faces)

- `415` *kavar* : Branch.  (24.1)

### Bhirrana

**seal** (3 faces)

- `003-003-390` *mū mū parutti* : Six cottons.  (50.1)
- `006` *āṟu* : Six.  (51.1)
- `740` *kuṭi* : Of the house.  (4080.1)

### Gola Dhoro (Bagasra)

**seal** (2 faces)

- `005-155` *ai kā* : Five-keeper.  (5215.1)
- `033-820-240-415-100-740-090` *mū kāl mīmīn kavar mutu kuṭi āḷ* : Manager of the High-star-Branch-Elder house (allowance: three quarters).  (5216.1)

### Surkotada

**seal** (2 faces)

- `740-803-390-060-740` *kuṭi il parutti -iṉ kuṭi* : Of the house; Of the Home-Cotton-Inner house.  (3876.1)
- `820-125-390-002-004-390` *kāl vēṭṭuvaṉ parutti iru nāl parutti* : quarter: Hunter-Cotton; Six cottons.  (3875.1)

### Nuhato

**pot** (1 faces)

- `700` *nāḻi?* : Cup.  (5255.1)

**seal** (1 faces)

- `803-900-740` *il tiṅkaḷ kuṭi* : Of the Home-Moon house.  (5252.1)

### Rupar

**tablet** (1 faces)

- `415-226-400` *kavar kūṭumīn ciṟ* : Branch-Fish-crate, junior.  (3873.1)

**tag or sealing** (2 faces)

- `017-585-740` *ēḻu kaṉṉi? kuṭi* : Of the Seven-Maiden house.  (3872.2)
- `235-032-877-740` *vēymīn iru nālkāṇi kuṭi* : Of the Bamboo-star-Two-Four shares house.  (3872.1)

### Amri

**pot** (2 faces)

- `034-390` *nāl parutti* : Four cottons.  (17.1)
- `480` *kuṉṟi* : Seed-weight.  (5415.1)

### Ra's al-Junayz

**pot** (1 faces)

- `004-405` *nāl nūl* : Four threads.  (3865.1)

### Khirsara

**seal** (2 faces)

- `017-575-740` *ēḻu kōṭṭai kuṭi* : Of the house (allowance: seven great measures).  (1969.1)
- `820-013-016-390` *kāl mū āṟu parutti* : three quarters: Six cottons.  (5455.1)

### Desalpur

**seal** (1 faces)

- `440-790-407-590` *koḷ maṇi kiḷai peṭṭi* : Received-Gem-Kindred-Chest.  (124.1)

### Karzakan

**seal** (2 faces)

- `091-031-455-220` *iruvar oru ampu mīn* : One the pair; Arrow-Star.  (5227.1)
- `091-032-001-033` *iruvar iru oru mū* : Six the pairs.  (5228.1)

### Tarkhanewala-dera

**pot** (1 faces)

- `235` *vēymīn* : Bamboo-star.  (3883.1)

**tag or sealing** (1 faces)

- `032-220-235-520` *iru mīn vēymīn vēḷ* : Two-Star-Bamboo-star, chief.  (5456.1)

### Alamgirpur

**pot** (1 faces)

- `017-405` *ēḻu nūl* : Seven threads.  (3.1)

### Daimabad

**seal** (1 faces)

- `740` *kuṭi* : Of the house.  (122.1)

### Rahman-deri

**other** (1 faces)

- `705` *kalam* : Kalam.  (590.1)

**seal** (1 faces)

- `031-520` *oru vēḷ* : One chief.  (5269.1)

### Nindowari-damb

**seal** (1 faces)

- `255-798-400` *mutal maru- ciṟ* : Chief-Descendant, junior.  (3859.1)

### Kish

**seal** (1 faces)

- `416-840-060-003-220-590-390-740` *turumpu iṇai -iṉ mū mīn peṭṭi parutti kuṭi* : Of the Grain-heap-Peer-Inner-Three-Star-Boxed-cotton house.  (1971.1)

### Hissam-dheri

**pot** (1 faces)

- `480-001` *kuṉṟi oru* : One seed-weight.  (1873.1)

### Miri Qalat

**seal** (2 faces)

- `013-520` *mū vēḷ* : Three chiefs.  (5444.1)
- `742-740` *irukuṭi kuṭi* : Of the Second-ward house.  (5442.1)

### Gumla

**pot** (1 faces)

- `840` *iṇai* : Pair.  (159.1)

### Rajanpur

**tablet** (1 faces)

- `033-700` *mū nāḻi?* : Three cups.  (4290.2)

### Altyn Depe

**seal** (1 faces)

- `415-390` *kavar parutti* : Branch-Cotton.  (16.1)

### Bakkar Buthi

**pot** (1 faces)

- `861-002-840-032-844-405` *kāṇi iru iṇai iru cūṭu nūl* : two shares: Two pairs; Sheaves, thread.  (18.1)

### Derawar Ther

**pot** (1 faces)

- `034` *nāl* : Four.  (5419.1)

### Jhukar

**seal** (1 faces)

- `817-002-233-803-740` *kāṇi iru vāḷai il kuṭi* : two shares: of the Scabbard-fish-Home house.  (1875.1)

### Gharo Bhiro

**seal** (1 faces)

- `838-923-740` *viḷai maruppu kuṭi* : Of the Produce-Ivory house.  (157.1)

### Kalba

**seal** (1 faces)

- `091` *iruvar* : The pair.  (5551.1)

### Hulas

**tag or sealing** (1 faces)

- `590-407-740` *peṭṭi kiḷai kuṭi* : Of the Chest-Kindred house.  (1874.1)

### Luristan

**seal** (1 faces)

- `091-840-413-831` *iruvar iṇai nel tiṉai* : The pair-Peer-Grain-Millet.  (2153.1)

## Part 2. The 100 most common part-read inscriptions

| copies | signs | sounds | English | first ids |
|---|---|---|---|---|
| 11 | `803-415-220-318-920-255-436-690-590-407-740` | il kavar mīn [318] tiṅkaḷ? mutal [436] piṇai peṭṭi kiḷai kuṭi | Of the Home-Branch-Star-[318]-Month-Chief-[436]-Ally-Chest-Kindred house. | 291.1, 1300.1, 1301.1, 1302.1, 1303.1, 1304.1, 1305.1, 1306.1 ... |
| 8 | `091-056-002-417-890-892` | iruvar [056] iru [417] koṭu vil | The pair; Two [056]; [417], given, sale. | 1927.1, 1928.1, 1929.1, 1930.1, 1931.1, 1932.1, 1933.1, 5281.1 |
| 6 | `905-032-597-142-617` | [905] iru [597] kō ūḻiyaṉ | Two [905]; [597], king, king's servant. | 3045.1, 3046.1, 3778.1, 3780.1, 3781.1, 3782.2 |
| 4 | `415-578-032-824` | kavar [578] iru vilai | Branch, [578]; Two prices. | 222.1, 407.2, 484.2, 1379.1 |
| 4 | `440-740-400-840-712` | koḷ kuṭi ciṟ iṇai [712] | Junior of the Received house; Pair; [712]. | 776.1, 907.1, 1207.1, 1610.1 |
| 4 | `736-904-158-400` | [736] irutiṅkaḷ kā ciṟ | [736]-Dark-moon-Keeper, junior. | 1253.1, 1254.1, 1255.1, 1699.1 |
| 3 | `028-032-740-400` | [028] iru kuṭi ciṟ | Junior of the house (allowance: two [028]). | 544.2, 1344.1, 1844.1 |
| 3 | `156-924-705-740-851` | kā [924] kalam kuṭi [851] | [851] of the Keeper-[924]-Ship house. | 581.1, 687.1, 689.1 |
| 3 | `220-236-400` | mīn [236] ciṟ | Star-[236], junior. | 751.2, 927.2, 3969.1 |
| 3 | `234-400` | [234] ciṟ | [234], junior. | 1770.1, 1825.1, 1826.2 |
| 3 | `380-705-200` | [380] kalam [200] | [380], kalam, [200]. | 270.1, 395.2, 1759.1 |
| 3 | `391-595-850-480-001-821` | [391] paṭṭaṟai kāṇi kuṉṟi oru mañcāṭi | [391], forge, share; One seed-weight; Mañcāṭi weight. | 2362.1, 2368.1, 2370.1 |
| 3 | `484-337-740` | [484] [337] kuṭi | Of the [484]-[337] house. | 1247.1, 1248.1, 1431.1 |
| 3 | `799-840-760-740` | [799] iṇai maka kuṭi | Of the [799] child of Peer house. | 407.3, 484.3, 672.2 |
| 3 | `851-741-048-740` | [851] orukuṭi er̤uvar kuṭi | Of the [851]-First-ward-Seven house. | 300.1, 742.1, 1772.1 |
| 3 | `910-740` | [910] kuṭi | Of the [910] house. | 1118.1, 1136.1, 3341.1 |
| 2 | `004-783-740` | nāl [783] kuṭi | Of the house (allowance: four [783]). | 1311.1, 1312.1 |
| 2 | `017-410` | ēḻu [410] | Seven [410]. | 1.1, 2.1 |
| 2 | `019-156` | [019] kā | [019], keeper. | 128.1, 4225.1 |
| 2 | `032-071-407` | iru [071] kiḷai | Two [071]; Kindred. | 2998.1, 2999.1 |
| 2 | `032-999-031` | iru [999] oru | Two lots of one [999]. | 355.1, 5381.1 |
| 2 | `034-999-034` | nāl [999] nāl | Four lots of four [999]. | 3935.1, 5299.1 |
| 2 | `049-740` | [049] kuṭi | Of the [049] house. | 1197.1, 2462.1 |
| 2 | `178-740-400` | [178] kuṭi ciṟ | Junior of the [178] house. | 1333.1, 1836.1 |
| 2 | `215-740` | [215] kuṭi | Of the [215] house. | 2842.1, 2842.2 |
| 2 | `219-072-520` | [219] [072] vēḷ | [219]-[072], chief. | 1257.1, 1704.2 |
| 2 | `229-151` | [229] kā | [229], keeper. | 1788.2, 1829.2 |
| 2 | `236-400` | [236] ciṟ | [236], junior. | 812.2, 1827.1 |
| 2 | `255-436-690-740-400` | mutal [436] piṇai kuṭi ciṟ | Junior of the Chief-[436]-Ally house. | 1720.1, 4290.1 |
| 2 | `326-002-176-740-240-405` | [326] iru iṟai kuṭi mīmīn nūl | High-star of the [326] house (allowance: two taxs); Thread. | 2985.2, 2986.2 |
| 2 | `352-400-520-400` | [352] ciṟ vēḷ ciṟ | [352]-Junior-Chief, junior. | 917.2, 1244.1 |
| 2 | `354-463-798-740` | [354] mukkōṭu maru- kuṭi | Of the [354]-Three-peaks-Descendant house. | 1224.1, 1631.1 |
| 2 | `368-330-741-590-390-151` | koṭi [330] orukuṭi peṭṭi parutti kā | Banner-[330]-First-ward-Boxed-cotton, keeper. | 1214.1, 1214.2 |
| 2 | `491-920-002-176-740-335-740-317` | kompu tiṅkaḷ? iru iṟai kuṭi ūr kuṭi [317] | Of the Horn-Month-Two-Tax house; [317] of the Town house. | 370.1, 1700.1 |
| 2 | `510-697` | [510] ney | [510], woven. | 194.1, 1596.1 |
| 2 | `511-130-920` | [511] kaḷamar tiṅkaḷ? | [511], husbandman, month. | 3822.1, 3832.1 |
| 2 | `516-775-400` | [516] [775] ciṟ | [516]-[775], junior. | 396.2, 468.2 |
| 2 | `531-740` | [531] kuṭi | Of the [531] house. | 1096.1, 1892.1 |
| 2 | `631-405` | [631] nūl | [631], thread. | 3829.1, 3830.1 |
| 2 | `678-400` | [678] ciṟ | [678], junior. | 255.2, 4072.1 |
| 2 | `681-690` | [681] piṇai | [681], bound. | 640.1, 1326.1 |
| 2 | `687-690` | [687] piṇai | [687], bound. | 1797.1, 1799.1 |
| 2 | `698-861-002` | [698] kāṇi iru | [698]; Two shares. | 2847.1, 2848.1 |
| 2 | `703-615-740` | [703] vayal kuṭi | Of the [703]-Field house. | 1143.1, 2363.1 |
| 2 | `704-167` | [704] kūli | [704], wages. | 3690.1, 3690.2 |
| 2 | `744-760-095-595-001-142-617` | [744] maka kōlaṉ paṭṭaṟai oru kō ūḻiyaṉ | Child of [744], staff-bearer; One forge; King, king's servant. | 2994.1, 2995.1 |
| 2 | `829-892-400` | [829] vil ciṟ | [829]-Sale, junior. | 1353.1, 1355.1 |
| 2 | `861-002-236` | kāṇi iru [236] | two shares: [236]. | 2073.1, 2074.1 |
| 2 | `877-159-400` | nālkāṇi [159] ciṟ | Four shares-[159], junior. | 3283.1, 3610.1 |
| 2 | `896-154-400` | [896] kā ciṟ | [896]-Keeper, junior. | 1683.1, 1684.1 |
| 2 | `912-740` | [912] kuṭi | Of the [912] house. | 2023.1, 3903.1 |
| 2 | `920-060-741-350-504` | tiṅkaḷ? -iṉ orukuṭi kalappai [504] | month in first ward: Plough, [504]. | 491.2, 589.2 |
| 2 | `920-220-892-202-400` | tiṅkaḷ? mīn vil [202] ciṟ | Month-Star-Sale-[202], junior. | 1216.1, 1217.1 |
| 2 | `920-632-930` | tiṅkaḷ? pal [930] | Month, many, [930]. | 1396.1, 1397.1 |
| 1 | `001-415-365-798-740-400` | oru kavar [365] maru- kuṭi ciṟ | Junior of the One-Branch-[365]-Descendant house. | 649.2 |
| 1 | `001-904-832` | oru irutiṅkaḷ [832] | One two months; [832]. | 1545.1 |
| 1 | `002-825-060-032-220-233-840-032-740` | iru [825] -iṉ iru mīn vāḷai iṇai iru kuṭi | Of the Inner-Two-Star-Scabbard-fish-Peer-Two house (allowance: two [825]). | 2041.1 |
| 1 | `002-825-740` | iru [825] kuṭi | Of the house (allowance: two [825]). | 3375.1 |
| 1 | `002-999-032` | iru [999] iru | Two lots of two [999]. | 5285.1 |
| 1 | `003-002-900-067-740` | mū iru tiṅkaḷ [067] kuṭi | Of the Five-Moon-[067] house. | 4277.1 |
| 1 | `003-122-617` | mū [122] ūḻiyaṉ | Three [122]; King's servant. | 2687.1 |
| 1 | `003-426` | mū [426] | Three [426]. | 3874.1 |
| 1 | `003-430` | mū [430] | Three [430]. | 1107.1 |
| 1 | `003-552-840-760-740` | mū [552] iṇai maka kuṭi | Of the child of Peer house (allowance: three [552]). | 2688.1 |
| 1 | `003-832-390` | mū [832] parutti | Three [832]; Cotton. | 1964.1 |
| 1 | `003-900-702-741-240-100-740` | mū tiṅkaḷ [702] orukuṭi mīmīn mutu kuṭi | Of the Three-Moon-[702]-First-ward-High-star-Elder house. | 1440.1 |
| 1 | `003-900-703-741-001-176-740` | mū tiṅkaḷ [703] orukuṭi oru iṟai kuṭi | Of the Three-Moon-[703]-First-ward house (allowance: one tax). | 4208.1 |
| 1 | `004-785-740` | nāl [785] kuṭi | Of the house (allowance: four [785]). | 309.1 |
| 1 | `005-411` | ai [411] | Five [411]. | 1948.1 |
| 1 | `005-475-527-002-391` | ai (n) kāval iru [391] | N; Guard; Two [391]. | 2568.1 |
| 1 | `006-911` | āṟu [911] | Six [911]. | 2362.2 |
| 1 | `013-840-740-170-072` | mū iṇai kuṭi [170] [072] | [170] of the Three-Peer house; [072]. | 11.1 |
| 1 | `015-140-822` | ai ammai [822] | Five ladies; [822]. | 113.1 |
| 1 | `015-409` | ai [409] | Five [409]. | 2051.1 |
| 1 | `016-220-776-825-005-909-095-390` | āṟu mīn malar [825] ai [909] kōlaṉ parutti | Six Star; Bloom, [825]; Five [909]; Staff-bearer, cotton. | 121.1 |
| 1 | `016-405-001-255-324` | āṟu nūl oru mutal [324] | Six lots of one thread; Chief; [324]. | 2912.1 |
| 1 | `016-853-440-760-740` | āṟu [853] koḷ maka kuṭi | Of the child of Received house (allowance: six [853]). | 2225.1 |
| 1 | `017-585-090-680-740` | ēḻu kaṉṉi? āḷ [680] kuṭi | Of the Seven-Maiden-Manager-[680] house. | 3647.1 |
| 1 | `019-405-176-100-740` | [019] nūl iṟai mutu kuṭi | Of the [019]-Thread-Tax-Elder house. | 1083.1 |
| 1 | `025-032-690` | [025] iru piṇai | Two [025]; Bound. | 843.1 |
| 1 | `025-032-740` | [025] iru kuṭi | Of the house (allowance: two [025]). | 871.2 |
| 1 | `025-032-740-400` | [025] iru kuṭi ciṟ | Junior of the house (allowance: two [025]). | 638.2 |
| 1 | `028-032-740` | [028] iru kuṭi | Of the house (allowance: two [028]). | 1124.1 |
| 1 | `029-032` | [029] iru | Two [029]. | 2267.1 |
| 1 | `031-056-705-575` | oru [056] kalam kōṭṭai | One [056]; Ship-Great measure. | 2064.1 |
| 1 | `031-383-861-740` | oru [383] kāṇi kuṭi | Of the Tribute house (allowance: one [383]). | 2885.1 |
| 1 | `031-388-002-003-426` | oru aracu iru mū [426] | One lot of five King; [426]. | 3343.1 |
| 1 | `031-502-002-806-240-520-001-003` | oru [502] iru viḷai mīmīn vēḷ oru mū | One lot of two [502]; Bounty; High-star; Four chiefs. | 2854.1 |
| 1 | `031-502-002-806-240-520-001-416` | oru [502] iru viḷai mīmīn vēḷ oru turumpu | Bounty-High-star, chief (allowance: one lot of two [502]); One grain-heap. | 3589.1 |
| 1 | `031-812-002-176-100-740` | oru [812] iru iṟai mutu kuṭi | Of the Tax-Elder house (allowance: one lot of two [812]). | 3179.1 |
| 1 | `031-865-892-400` | oru [865] vil ciṟ | Sale, junior (allowance: one [865]). | 5365.1 |
| 1 | `031-933-413` | oru [933] nel | One [933]; Grain. | 3900.2 |
| 1 | `032-116` | iru [116] | Two [116]. | 1272.2 |
| 1 | `032-125-610-002` | iru vēṭṭuvaṉ [610] iru | Two Hunter; Two [610]. | 1132.1 |
| 1 | `032-125-610-002-240-233-705-033-520` | iru vēṭṭuvaṉ [610] iru mīmīn vāḷai kalam mū vēḷ | Two-Hunter-[610]-Two-High-star-Scabbard-fish, chief (allowance: three kalam). | 2473.1 |
| 1 | `032-168-002-032-220-232` | iru [168] iru iru mīn kūṭumīn | Two lots of four [168]; Star; Cluster-star. | 3519.1 |
| 1 | `032-168-235-233-706-033-807-388-740` | iru [168] vēymīn vāḷai kalam mū [807] aracu kuṭi | Of the Bamboo-star-Scabbard-fish-[807]-King house (allowance: two [168] and three kalam). | 3114.1 |
| 1 | `032-172-002-705-033-520` | iru [172] iru kalam mū vēḷ | Two lots of two [172]; Three kalam; Chief. | 1445.1 |
| 1 | `032-220-240-033-812-740` | iru mīn mīmīn mū [812] kuṭi | Of the Two-Star-High-star house (allowance: three [812]). | 2837.1 |
| 1 | `032-220-455-710` | iru mīn ampu [710] | Two Star; Arrow, [710]. | 1830.1 |

## Part 3. Multi-face objects read as one record (902 objects with 2 or more faces; 365 with every face whole)

Each object: who (house or person) + what (goods words) + amount. Faces are separated by " / " in the sign column.

- object 153 (seal, Farmana) `371-390 / 371-390` : Spindle-Cotton.
- object 198 (tablet, Harappa) `692-060-240-603-740 / 034-700` : Four cups, for the High-star-Store house.
- object 229 (tablet, Harappa) `032-001-904-031-740 / 032-700` : Two cups, for the Three-Dark-moon-One house.
- object 234 (tablet, Harappa) `590-705-868 / 255-435-156-400` : Chief-Rod-Keeper, junior: chest, half a kalam.
- object 249 (tablet, Harappa) `831-892-400 / 032-700` : Two cups, for Millet-Sale, junior.
- object 250 (tablet, Harappa) `220 / 705-167` : Star, kalam, wages.
- object 257 (tablet, Harappa) `920-060-741-176-156 / 032-700` : Two cups, for Tax, keeper.
- object 260 (tablet, Harappa) `033-700 / 176-740-400` : Three cups, for the junior of the Tax house.
- object 264 (tablet, Harappa) `032-140-156-400 / 033-700` : Three cups, for Two-Lady-Keeper, junior.
- object 265 (tablet, Harappa) `176-740-400 / 034-700` : Four cups, for the junior of the Tax house.
- object 273 (tablet, Harappa) `382-740-400 / 032-700` : Two cups, for the junior of the King house.
- object 274 (tablet, Harappa) `255-435-154 / 034-700` : Four cups, for Chief-Rod, keeper.
- object 280 (tablet, Harappa) `817-002-240-904-740 / 032-700` : Two cups, for the High-star-Dark-moon house.
- object 282 (tablet, Harappa) `032-700 / 220-520` : Two cups, for Star, chief.
- object 297 (tablet, Harappa) `240-233-520 / 455-740-400` : High-star-Scabbard-fish, chief and the junior of the Arrow house.
- object 305 (tablet, Harappa) `413 / 692` : Grain, assembly.
- object 310 (tablet, Harappa) `033-590-416 / 255-033` : Three chests and three chiefs of grain heap.
- object 313 (tablet, Harappa) `220-550-525 / 032-700` : Two cups of star, gate, guard.
- object 316 (tablet, Harappa) `240-904-740 / 700-033` : Three cups, for the High-star-Dark-moon house.
- object 317 (tablet, Harappa) `032-226-400 / 032-700` : Two cups, for Two-Fish-crate, junior.
- object 371 (tablet, Harappa) `032-700 / 140-001-031-740` : Two cups, for the Lady-Two house.
- object 373 (tablet, Harappa) `700-033 / 435-003-550` : Three cups and three gates of rod.
- object 375 (tablet, Harappa) `036-700 / 171-033-700-415` : Six cups and three cups of full measure, branch.
- object 377 (tablet, Harappa) `700-033 / 705-167` : Three cups of kalam, wages.
- object 382 (tablet, Harappa) `034-700 / 140-061-740-400` : Four cups, for the junior of the Lady-Quarter house.
- object 383 (tablet, Harappa) `032-700 / 140-001-031-740` : Two cups, for the Lady-Two house.
- object 390 (tablet, Harappa) `590-706-868 / 255-435-156-400` : Chief-Rod-Keeper, junior: chest, half a kalam.
- object 392 (tablet, Harappa) `700-033 / 137-400` : Three cups, for Cultivator, junior.
- object 394 (tablet, Harappa) `034-700 / 590-741-371-455-004-390` : Four cups and four cottons of chest, first-ward house, spindle, arrow.
- object 397 (tablet, Harappa) `034-700 / 231-176-740-565` : Four cups, for the warrior of the First-star-Tax house.
- object 400 (tablet, Harappa) `032-700 / 140-001-031-740` : Two cups, for the Lady-Two house.
- object 405 (tablet, Harappa) `817-368-690 / 171-032-031-240-630-740` : Three full measures of banner, bound, for the High-star-Many house.
- object 406 (tablet, Harappa) `034-700 / 240-100-740-400` : Four cups, for the junior of the High-star-Elder house.
- object 409 (tablet, Harappa) `700-032 / 861-002-035-405` : Two cups and five threads.
- object 410 (tablet, Harappa) `700-033 / 240-904-740-400` : Three cups, for the junior of the High-star-Dark-moon house.
- object 414 (tablet, Harappa) `033-700 / 491-920-032` : Three cups and two months of horn.
- object 418 (tablet, Harappa) `034-700 / 231-176-740-565` : Four cups, for the warrior of the First-star-Tax house.
- object 419 (tablet, Harappa) `033-700 / 741-368-400` : Three cups, for First-ward-Banner, junior.
- object 422 (tablet, Harappa) `034-700 / 031-384-740` : Four cups, for the One-King house.
- object 424 (tablet, Harappa) `034-700 / 692-060-240-642-740` : Four cups, for the High-star-Many house.
- object 427 (tablet, Harappa) `034-700 / 717-740-400` : Four cups, for the junior of the Servant house.
- object 437 (tablet, Harappa) `700-033 / 240-520` : Three cups, for High-star, chief.
- object 453 (tablet, Harappa) `032-700 / 491-817-740` : Two cups, for the Horn-Share house.
- object 459 (tablet, Harappa) `413-892-824 / 415-100-740` : The Branch-Elder house: grain, sale, price.
- object 461 (tablet, Harappa) `031-700 / 892-740` : One cup, for the Sale house.
- object 463 (tablet, Harappa) `817-368-690-032-700 / 176-740-400` : Two cups of banner, bound, for the junior of the Tax house.
- object 466 (tablet, Harappa) `820-002 / 003-861` : Three shares.
- object 467 (tablet, Harappa) `034-700 / 220-176-740` : Four cups, for the Star-Tax house.
- object 472 (tablet, Harappa) `235-555-526 / 413-892-824` : Bamboo-star, gate, guard, grain, sale, price.
- object 476 (tablet, Harappa) `034-700 / 416-861-002` : Four cups and two shares of grain heap.
- object 480 (tablet, Harappa) `034-700 / 382-760-740-400` : Four cups, for the junior of the child of King house.
- object 485 (tablet, Harappa) `220-032-700 / 803-240-415-220-520` : Two cups of star, for Home-High-star-Branch-Star, chief.
- object 488 (tablet, Harappa) `700-034 / 416-861-002` : Four cups and two shares of grain heap.
- object 490 (tablet, Harappa) `032-700 / 015-032-740-400` : Two cups, for the junior of the Seven house.
- object 499 (tablet, Harappa) `091-368-033-700 / 388-740-400-033-700` : Three cups of the pair, banner, for the junior of the King house.
- object 508 (tablet, Harappa) `034-700 / 222-740-151` : Four cups, for the keeper of the Shut-in-fish house.
- object 509 (tablet, Harappa) `034-700 / 222-740-151` : Four cups, for the keeper of the Shut-in-fish house.
- object 515 (tablet, Harappa) `033-700 / 240-520` : Three cups, for High-star, chief.
- object 516 (tablet, Harappa) `700-033 / 255-435-690-740` : Three cups, for the Chief-Rod-Ally house.
- object 518 (tablet, Harappa) `034-700 / 416-861-002` : Four cups and two shares of grain heap.
- object 519 (tablet, Harappa) `032-700 / 390-155-004-390` : Two cups and four cottons, for Cotton, keeper.
- object 532 (tablet, Harappa) `590-705-868 / 550-525-400-034-700` : Four cups of chest, half a kalam, for Gate-Guard, junior.
- object 535 (tablet, Harappa) `840-032-740 / 840-032-740` : The Peer-Two house.
- object 549 (tablet, Harappa) `700-034 / 027-032-740-400` : Four cups, for the junior of the Nine-Two house.
- object 550 (tablet, Harappa) `033-700 / 519-176-740-400` : Three cups, for the junior of the Fence-Tax house.
- object 554 (tablet, Harappa) `032-700 / 090-400-740-090-400` : Two cups of junior, for the manager of the Manager-Junior house.
- object 567 (tablet, Harappa) `032-700 / 840-032-740-400` : Two cups, for the junior of the Peer-Two house.
- object 569 (tablet, Harappa) `032-700 / 798-240-233-320-920-740-400` : Two cups, for the junior of the Descendant-High-star-Scabbard-fish-Ration measure-Month house.
- object 570 (tablet, Harappa) `700-032 / 055-255-435-690-740` : Two cups, for the Twelve-Chief-Rod-Ally house.
- object 578 (tablet, Harappa) `033-700 / 231-390-100-740-090-400` : Three cups of junior, for the manager of the First-star-Cotton-Elder house.
- object 593 (tablet, Harappa) `033-700 / 705-630-175-100-740` : Three cups, for the Ship-Many-Tax-Elder house.
- object 594 (tablet, Harappa) `031-850-032 / 861-002-175-752-740` : One lot of two shares, for the child of Tax house.
- object 596 (tablet, Harappa) `032-700 / 235-705-033-176-740` : Two cups and three kalam, for the Bamboo-star-Tax house.
- object 598 (tablet, Harappa) `700-033 / 137-400` : Three cups, for Cultivator, junior.
- object 621 (tablet, Harappa) `416-861-002 / 034-700` : Two shares and four cups of grain heap.
- object 624 (tablet, Harappa) `034-700 / 554-525-400` : Four cups, for Threshing-floor-Guard, junior.
- object 627 (tablet, Harappa) `004-700 / 097-151-400` : Four cups, for Bondsman-Keeper, junior.
- object 628 (tablet, Harappa) `700-032-032 / 033-033-520` : Four cups and six chiefs.
- object 630 (tablet, Harappa) `033-031-700 / 027-032-740-400` : Four cups, for the junior of the Nine-Two house.
- object 631 (tablet, Harappa) `700-033 / 803-233-176-435-690-740` : Three cups, for the Home-Scabbard-fish-Tax-Rod-Ally house.
- object 635 (tablet, Harappa) `240-705-033-550-525-400 / 413-575-335-711-033-740` : Three kalam and three vaḷḷam measures, for High-star-Gate-Guard, junior and the Grain-Great measure-Town house.
- object 637 (tablet, Harappa) `034-700 / 097-400` : Four cups, for Bondsman, junior.
- object 642 (tablet, Harappa) `137 / 034-700` : Four cups of cultivator.
- object 643 (tablet, Harappa) `032-255-740 / 032-700` : Two cups, for the Two-Chief house.
- object 646 (tablet, Harappa) `034-700 / 201-060-031-176-740` : Four cups, for the Rain-season-Inner-One-Tax house.
- object 647 (tablet, Harappa) `255-435-156-400 / 590-705-868` : Chief-Rod-Keeper, junior: chest, half a kalam.
- object 653 (tablet, Harappa) `220-705-033-550-525-400 / 413-575-335-711-033-700` : Three kalam and three cups of grain, great measure, town, vaḷḷam measure, for Star-Gate-Guard, junior.
- object 654 (tablet, Harappa) `388-740-400 / 091-368` : The junior of the King house: the pair, banner.
- object 659 (tablet, Harappa) `034-700 / 027-032-740-400` : Four cups, for the junior of the Nine-Two house.
- object 665 (tablet, Harappa) `034-700 / 416-861-002` : Four cups and two shares of grain heap.
- object 671 (tablet, Harappa) `590-706-868 / 255-435-156-400` : Chief-Rod-Keeper, junior: chest, half a kalam.
- object 675 (tablet, Harappa) `700-033 / 235-923-740` : Three cups, for the Bamboo-star-Ivory house.
- object 682 (tablet, Harappa) `032-700 / 820-002-554-526` : Two cups of threshing-floor, guard.
- object 686 (tablet, Harappa) `034-700 / 692-060-240-603-740` : Four cups, for the High-star-Store house.
- object 693 (tablet, Harappa) `033-700 / 003-861 / 003-156` : Three cups and three shares and three porters.
- object 729 (tablet, Harappa) `235-220-176-740 / 861-002-240-482-740` : Two shares the Bamboo-star-Star-Tax house and the High-star-Hill-share house.
- object 732 (tablet, Harappa) `033-700 / 900-368` : Three cups of month, banner.
- object 740 (tablet, Harappa) `792-740-090 / 034-700` : Four cups, for the manager of the Royal house.
- object 743 (tablet, Harappa) `240-520 / 034-700` : Four cups, for High-star, chief.
- object 749 (tablet, Harappa) `032-700 / 798-017-575-740-400` : Two cups and seven great measures, for the junior of the Descendant house.
- object 752 (tablet, Harappa) `034-700 / 792-740-090` : Four cups, for the manager of the Royal house.
- object 753 (tablet, Harappa) `032-700 / 240-176-740-400` : Two cups, for the junior of the High-star-Tax house.
- object 769 (tablet, Harappa) `003-861 / 034-700 / 003-156` : Three shares and four cups and three porters.
- object 772 (tablet, Harappa) `034-700 / 176-156` : Four cups, for Tax, keeper.
- object 773 (tablet, Harappa) `034-700 / 176-156` : Four cups, for Tax, keeper.
- object 774 (tablet, Harappa) `033-700 / 091-368` : Three cups of the pair, banner.
- object 780 (tablet, Harappa) `034-700 / 690-154-400` : Four cups, for Ally-Keeper, junior.
- object 784 (tablet, Harappa) `034-700 / 235-740-151` : Four cups, for the keeper of the Bamboo-star house.
- object 786 (tablet, Harappa) `033-255 / 033-590-416` : Three chiefs and three chests of grain heap.
- object 794 (tablet, Harappa) `034-700 / 003-861 / 003-154` : Four cups and three shares and three porters.
- object 801 (tablet, Harappa) `032-700 / 491-817-740-400` : Two cups, for the junior of the Horn-Share house.
- object 806 (tablet, Harappa) `700-824 / 240-152-740-400` : The junior of the High-star-Keeper house: cup, price.
- object 814 (tablet, Harappa) `032-388-480-001 / 034-700` : Two King and one seed-weight and four cups.
- object 815 (tablet, Harappa) `700-034 / 226-400` : Four cups, for Fish-crate, junior.
- object 829 (tablet, Harappa) `032-700 / 741-032-840-700` : Two cups and two pairs of first-ward house, cup.
- object 831 (tablet, Harappa) `700-034 / 033-033-520` : Four cups and six chiefs.
- object 832 (tablet, Harappa) `003-861 / 034-700 / 003-156` : Three shares and four cups and three porters.
- object 834 (tablet, Harappa) `032-700 / 690-158-400` : Two cups, for Ally-Keeper, junior.
- object 840 (tablet, Harappa) `061-255-740 / 003-861` : Three shares, for the Quarter-Chief house.
- object 841 (tablet, Harappa) `415-220-520 / 032-700` : Two cups, for Branch-Star, chief.
- object 844 (tablet, Harappa) `034-700 / 003-861 / 003-156` : Four cups and three shares and three porters.
- object 845 (tablet, Harappa) `003-861 / 034-700 / 003-156` : Three shares and four cups and three porters.
- object 846 (tablet, Harappa) `003-861 / 034-700 / 003-156` : Three shares and four cups and three porters.
- object 847 (tablet, Harappa) `003-861 / 034-700 / 003-156` : Three shares and four cups and three porters.
- object 848 (tablet, Harappa) `415-220-520 / 003-645-032-590` : Three lots of two gold weights of chest, for Branch-Star, chief.
- object 850 (tablet, Harappa) `034-700 / 003-861 / 003-156` : Four cups and three shares and three porters.
- object 851 (tablet, Harappa) `003-861 / 034-700 / 003-156` : Three shares and four cups and three porters.
- object 852 (tablet, Harappa) `034-700 / 003-861 / 003-156` : Four cups and three shares and three porters.
- object 853 (tablet, Harappa) `034-700 / 003-861 / 003-156` : Four cups and three shares and three porters.
- object 854 (tablet, Harappa) `003-861 / 034-700 / 003-156` : Three shares and four cups and three porters.
- object 855 (tablet, Harappa) `034-700 / 003-861 / 003-156` : Four cups and three shares and three porters.
- object 856 (tablet, Harappa) `003-861 / 034-700 / 003-156` : Three shares and four cups and three porters.
- object 857 (tablet, Harappa) `003-861 / 034-700 / 003-156` : Three shares and four cups and three porters.
- object 858 (tablet, Harappa) `003-861 / 034-700 / 003-156` : Three shares and four cups and three porters.
- object 859 (tablet, Harappa) `003-861 / 034-700 / 003-156` : Three shares and four cups and three porters.
- object 860 (tablet, Harappa) `003-861 / 034-700 / 003-156` : Three shares and four cups and three porters.
- object 861 (tablet, Harappa) `003-861 / 034-700 / 003-156` : Three shares and four cups and three porters.
- object 863 (tablet, Harappa) `033-700 / 831-892-400` : Three cups, for Millet-Sale, junior.
- object 866 (tablet, Harappa) `034-700 / 032-388-480-031` : Four cups and two king and one seed-weight.
- object 867 (tablet, Harappa) `240-705-033-550-525-400 / 413-575-335-711-033-700` : Three kalam and three cups of grain, great measure, town, vaḷḷam measure, for High-star-Gate-Guard, junior.
- object 869 (tablet, Harappa) `033-700 / 142-151-400` : Three cups, for King-Keeper, junior.
- object 870 (tablet, Harappa) `034-700 / 003-861 / 003-156` : Four cups and three shares and three porters.
- object 876 (tablet, Harappa) `700-032-032 / 033-033-520` : Four cups and six chiefs.
- object 878 (tablet, Harappa) `034-700 / 003-861 / 003-156` : Four cups and three shares and three porters.
- object 890 (tablet, Harappa) `176-156 / 034-700` : Four cups, for Tax, keeper.
- object 892 (tablet, Harappa) `003-861 / 416-740` : Three shares, for the Grain-heap house.
- object 895 (tablet, Harappa) `176-156 / 034-700` : Four cups, for Tax, keeper.
- object 902 (tablet, Harappa) `235-240-740-090 / 220-032-590-690` : Two chests of star, bound, for the manager of the Bamboo-star-High-star house.
- object 904 (tablet, Harappa) `235-240-740-090 / 220-032-590-690` : Two chests of star, bound, for the manager of the Bamboo-star-High-star house.
- object 913 (tablet, Harappa) `415-220-520 / 415-220-520` : Branch-Star, chief.
- object 916 (tablet, Harappa) `240-705-033-550-525-400 / 413-575-335-711-033-700` : Three kalam and three cups of grain, great measure, town, vaḷḷam measure, for High-star-Gate-Guard, junior.
- object 921 (tablet, Harappa) `033-700 / 140-061-740-400` : Three cups, for the junior of the Lady-Quarter house.
- object 923 (tablet, Harappa) `700-032 / 705-717-388-740-400` : Two cups, for the junior of the Ship-Servant-King house.
- object 930 (tablet, Harappa) `033-700 / 032-790-740` : Three cups, for the Two-Gem house.
- object 937 (tablet, Harappa) `235-220-176-740 / 861-002-240-482-740` : Two shares the Bamboo-star-Star-Tax house and the High-star-Hill-share house.
- object 938 (tablet, Harappa) `700-034 / 255-435-690-740` : Four cups, for the Chief-Rod-Ally house.
- object 945 (tablet, Harappa) `033-700 / 233-550-526` : Three cups of scabbard-fish, gate, guard.
- object 1018 (tablet, Harappa) `034-700 / 413-137` : Four cups of grain, cultivator.
- object 1021 (tablet, Harappa) `175-482-335-740-400 / 032-700` : Two cups, for the junior of the Tax-Hill-share-Town house.
- object 1023 (tablet, Harappa) `240-482-752-740 / 745-700` : The High-star child of Hill-share house: third-ward house, cup.
- object 1024 (tablet, Harappa) `700-033 / 861-002-031-892-803-740` : Three cups, for the One-Sale-Home house.
- object 1051 (tablet, Harappa) `175-817-740-400 / 033-033` : Six, for the junior of the Tax-Share house.
- object 1052 (tablet, Harappa) `491-817-740-400 / 034-700` : Four cups, for the junior of the Horn-Share house.
- object 1057 (tablet, Harappa) `240-590-390-740 / 033-700` : Three cups, for the High-star-Boxed-cotton house.
- object 1058 (tablet, Harappa) `240-636-690-740 / 033-700` : Three cups, for the High-star-Many-Ally house.
- object 1061 (tablet, Harappa) `233-550-527 / 032-700` : Two cups of scabbard-fish, gate, guard.
- object 1168 (seal, Harappa) `861-741 / 861-741-240-630-740` : Share First-ward and the First-ward-High-star-Many house.
- object 1201 (seal, Harappa) `468-806-154-400 / 017-090` : N loads of produce, carried by the porter and seven managers of junior.
- object 1215 (tablet, Harappa) `840-032-740 / 840-032-740` : The Peer-Two house.
- object 1236 (tablet, Harappa) `850-741-048-740 / 413-575-335-711-033-700` : Three cups of grain, great measure, town, vaḷḷam measure, for the Share-First-ward-Seven house.
- object 1240 (tablet, Harappa) `055-255-435-690-921-400 / 032-700` : Two cups, for Twelve-Chief-Rod-Ally-Bow, junior.
- object 1246 (tablet, Harappa) `034-700 / 137-400` : Four cups, for Cultivator, junior.
- object 1249 (tablet, Harappa) `176-336-740 / 033-700` : Three cups, for the Tax-Town house.
- object 1250 (tablet, Harappa) `171-035-415 / 033-700` : Five full measures and three cups of branch.
- object 1256 (tablet, Harappa) `617-892-740-400 / 033-700` : Three cups, for the junior of the King's servant-Sale house.
- object 1258 (tablet, Harappa) `820-002-240-220-520 / 033-700` : Three cups, for High-star-Star, chief.
- object 1260 (tablet, Harappa) `176-740-400 / 033-700` : Three cups, for the junior of the Tax house.
- object 1262 (tablet, Harappa) `817-368-690 / 679-840-032-740` : Share the Throne-Peer-Two house: banner, bound.
- object 1263 (tablet, Harappa) `692-060-240-642-740 / 033-700` : Three cups, for the High-star-Many house.
- object 1269 (tablet, Harappa) `820-002-104 / 034` : Four of goldsmith.
- object 1273 (tablet, Harappa) `798-240-233-320-920-740-400 / 033-700` : Three cups, for the junior of the Descendant-High-star-Scabbard-fish-Ration measure-Month house.
- object 1274 (tablet, Harappa) `700-033 / 233-520` : Three cups, for Scabbard-fish, chief.
- object 1276 (tablet, Harappa) `240-100-740-400 / 032-700` : Two cups, for the junior of the High-star-Elder house.
- object 1318 (tablet, Harappa) `920-017-575-740-400 / 033-700` : Three cups, for the junior of the Month-Seven-Great measure house.
- object 1319 (tablet, Harappa) `706-630-336-151-400 / 034-700` : Four cups, for Ship-Many-Town-Keeper, junior.
- object 1321 (tablet, Harappa) `590-706-868 / 255-435-156-400` : Chief-Rod-Keeper, junior: chest, half a kalam.
- object 1322 (tablet, Harappa) `817-368-690 / 495-776-740-400` : Share the junior of the Horn-Bloom house: banner, bound.
- object 1323 (tablet, Harappa) `413-892-824 / 171-032-031-240-636-740-400` : Three full measures of grain, sale, price, for the junior of the High-star-Many house.
- object 1324 (tablet, Harappa) `004-700-220 / 416-220-740-760-400` : Four cups of star, junior, for Child of of the Grain-heap-Star house.
- object 1325 (tablet, Harappa) `027-032-740-400 / 033-700` : Three cups, for the junior of the Nine-Two house.
- object 1327 (tablet, Harappa) `031-861-003 / 061-255-740` : One lot of three shares, for the Quarter-Chief house.
- object 1328 (tablet, Harappa) `840-032-740 / 033-700` : Three cups, for the Peer-Two house.
- object 1329 (tablet, Harappa) `900-368 / 034-700` : Four cups of month, banner.
- object 1330 (tablet, Harappa) `176-740-400 / 034-700` : Four cups, for the junior of the Tax house.
- object 1331 (tablet, Harappa) `176-740-400 / 033-700` : Three cups, for the junior of the Tax house.
- object 1334 (tablet, Harappa) `176-740-400 / 034-700` : Four cups, for the junior of the Tax house.
- object 1335 (tablet, Harappa) `176-740-400 / 034-700` : Four cups, for the junior of the Tax house.
- object 1336 (tablet, Harappa) `176-740-400 / 034-700` : Four cups, for the junior of the Tax house.
- object 1337 (tablet, Harappa) `176-740-400 / 032-700` : Two cups, for the junior of the Tax house.
- object 1338 (tablet, Harappa) `176-740-400 / 033-700` : Three cups, for the junior of the Tax house.
- object 1339 (tablet, Harappa) `176-740-400 / 034-700` : Four cups, for the junior of the Tax house.
- object 1341 (tablet, Harappa) `415-220-520 / 034-700` : Four cups, for Branch-Star, chief.
- object 1343 (tablet, Harappa) `240-630-690-740 / 700-032` : Two cups, for the High-star-Many-Ally house.
- object 1345 (tablet, Harappa) `240-100-740 / 700-033` : Three cups, for the High-star-Elder house.
- object 1346 (tablet, Harappa) `031-384-156-400 / 034-700` : Four cups, for One-King-Keeper, junior.
- object 1348 (tablet, Harappa) `013-840-740 / 033-700` : Three cups, for the Three-Peer house.
- object 1350 (tablet, Harappa) `004-690 / 235-717-741-400` : Four bounds, for Bamboo-star-Servant-First-ward, junior.
- object 1351 (tablet, Harappa) `220-520 / 033-700` : Three cups, for Star, chief.
- object 1362 (tablet, Harappa) `176-336-740-400 / 032-700` : Two cups, for the junior of the Tax-Town house.
- object 1363 (tablet, Harappa) `877-861-740 / 033-700` : Three cups, for the Four shares-Tribute house.
- object 1364 (tablet, Harappa) `220-550-526 / 033-700` : Three cups of star, gate, guard.
- object 1366 (tablet, Harappa) `415-220-520 / 090-700` : Branch-Star, chief: manager, cup.
- object 1369 (tablet, Harappa) `240-642-690-740 / 034-700` : Four cups, for the High-star-Many-Ally house.
- object 1370 (tablet, Harappa) `013-060-032-740-400 / 034-700` : Four cups, for the junior of the Three-within-Two house.
- object 1371 (seal, Harappa) `176-740-400 / 033-700` : Three cups, for the junior of the Tax house.
- object 1372 (tablet, Harappa) `176-740-400 / 033-700` : Three cups, for the junior of the Tax house.
- object 1373 (seal, Harappa) `176-740-400 / 033-700` : Three cups, for the junior of the Tax house.
- object 1374 (tablet, Harappa) `176-740-400 / 033-700 / 033-700` : Three cups, for the junior of the Tax house.
- object 1375 (tablet, Harappa) `033-700 / 176-740-400` : Three cups, for the junior of the Tax house.
- object 1376 (tablet, Harappa) `176-740-400 / 033-700` : Three cups, for the junior of the Tax house.
- object 1378 (tablet, Harappa) `220-550-526 / 700-032` : Two cups of star, gate, guard.
- object 1386 (seal, Harappa) `700 / 033` : Three of the measurer.
- object 1388 (seal, Harappa) `741-390-741-031-705-033-368 / 033-700` : One lot of three kalam and three cups, for First-ward-Cotton-First-ward and Banner.
- object 1540 (seal, Harappa) `861-002-032-070-590-390-740 / 861-002-032-070-590-390-740` : Two shares the Two-Arrow-Boxed-cotton house.
- object 1602 (tablet, Harappa) `817-002-240-904-740 / 032-700` : Two cups, for the High-star-Dark-moon house.
- object 1607 (tablet, Harappa) `820-002-137 / 033-700` : Three cups of cultivator.
- object 1620 (tablet, Harappa) `904-705 / 032-700` : Two cups of two months, kalam.
- object 1633 (tablet, Harappa) `240-590-390-740 / 033-700` : Three cups, for the High-star-Boxed-cotton house.
- object 1637 (tablet, Harappa) `745-700 / 240-482-752-740` : The High-star child of Hill-share house: third-ward house, cup.
- object 1653 (tablet, Harappa) `255-435-156-400 / 220-440-154-400` : Chief-Rod-Keeper, junior and Star-Received-Keeper, junior.
- object 1656 (tablet, Harappa) `697 / 790-717-740` : The Gem-Servant house: woven.
- object 1657 (tablet, Harappa) `790-717-740 / 697` : The Gem-Servant house: woven.
- object 1659 (tablet, Harappa) `798-415-220-740-400 / 033-700` : Three cups, for the junior of the Descendant-Branch-Star house.
- object 1662 (tablet, Harappa) `416-840-151 / 033-700` : Three cups, for Grain-heap-Peer, keeper.
- object 1665 (tablet, Harappa) `741-530-390-002-803-798-740 / 413-575-335-711-033-700` : Three cups of grain, great measure, town, vaḷḷam measure, for the First-ward-Proclamation-Cotton-Two-Home-Descendant house.
- object 1666 (tablet, Harappa) `240-705-033-550-525-400 / 413-575-335-711-033-700` : Three kalam and three cups of grain, great measure, town, vaḷḷam measure, for High-star-Gate-Guard, junior.
- object 1668 (tablet, Harappa) `700-032 / 104-004-390` : Two cups and four cottons of goldsmith.
- object 1669 (tablet, Harappa) `032-700 / 817-004-390` : Two cups of cotton.
- object 1671 (tablet, Harappa) `061-142-400-740 / 034-700` : Four cups, for the Quarter-King-Junior house.
- object 1672 (tablet, Harappa) `700-033 / 240-904-740` : Three cups, for the High-star-Dark-moon house.
- object 1675 (tablet, Harappa) `098 / 032-700` : Two cups of attendant.
- object 1677 (tablet, Harappa) `413-892-824 / 415-220-520` : Branch-Star, chief: grain, sale, price.
- object 1678 (tablet, Harappa) `413-892-824 / 033-700-176-740-400` : Three cups of grain, sale, price, for the junior of the Tax house.
- object 1680 (tablet, Harappa) `016-220-520-400 / 700-033` : Three cups, for Six-Star-Chief, junior.
- object 1681 (tablet, Harappa) `033-384-740-400 / 033-700` : Three cups, for the junior of the Three-King house.
- object 1685 (tablet, Harappa) `235-232-400 / 700-032` : Two cups, for Bamboo-star-Cluster-star, junior.
- object 1687 (tablet, Harappa) `455-370 / 032-700` : Two cups of arrow, spindle.
- object 1690 (tablet, Harappa) `415-100-820-032 / 033-700` : Two quarters and three cups of branch, elder.
- object 1692 (tablet, Harappa) `036-700 / 171-035-415` : Six cups and five full measures of branch.
- object 1695 (tablet, Harappa) `861-002-240-482-740 / 235-220-176-740` : Two shares the High-star-Hill-share house and the Bamboo-star-Star-Tax house.
- object 1696 (tablet, Harappa) `861-002-240-482-740 / 235-220-176-740` : Two shares the High-star-Hill-share house and the Bamboo-star-Star-Tax house.
- object 1697 (tablet, Harappa) `861-002-240-482-740 / 235-220-176-740` : Two shares the High-star-Hill-share house and the Bamboo-star-Star-Tax house.
- object 1701 (tablet, Harappa) `035-368 / 700-033` : Five banners and three cups.
- object 1703 (tablet, Harappa) `415-100-820-400 / 032-700` : Two cups, for Branch-Elder-Quarter, junior.
- object 1705 (tablet, Harappa) `590-390-740-400 / 700-033` : Three cups, for the junior of the Boxed-cotton house.
- object 1706 (tablet, Harappa) `018-336-740-400 / 700-032` : Two cups, for the junior of the Eight-Town house.
- object 1707 (tablet, Harappa) `018-336-740 / 033-700` : Three cups, for the Eight-Town house.
- object 1708 (tablet, Harappa) `240-520 / 034-700` : Four cups, for High-star, chief.
- object 1710 (tablet, Harappa) `033-700 / 692-001-240-642-740` : Three cups, for the Assembly-One-High-star-Many house.
- object 1711 (tablet, Harappa) `033-700 / 692-001-240-642-740` : Three cups, for the Assembly-One-High-star-Many house.
- object 1712 (tablet, Harappa) `034-700 / 692-060-240-636-740` : Four cups, for the High-star-Many house.
- object 1715 (tablet, Harappa) `817-368 / 840-032-740` : Share the Peer-Two house: banner.
- object 1719 (tablet, Harappa) `820-002-554-526 / 032-700` : Two cups of threshing-floor, guard.
- object 1724 (tablet, Harappa) `817-002-495-615-740 / 033-700` : Three cups, for the Horn-Field house.
- object 1725 (tablet, Harappa) `700-032 / 140-400` : Two cups, for Lady, junior.
- object 1732 (tablet, Harappa) `705-031-100-740-400 / 033-700` : One kalam and three cups, for the junior of the Elder house.
- object 1735 (tablet, Harappa) `617-892-740-400 / 700-032` : Two cups, for the junior of the King's servant-Sale house.
- object 1736 (tablet, Harappa) `617-892-740-400 / 700-032` : Two cups, for the junior of the King's servant-Sale house.
- object 1740 (tablet, Harappa) `003-335-740-400 / 032-700` : Two cups, for the junior of the Three-Town house.
- object 1741 (tablet, Harappa) `235-590-390-740 / 033-700` : Three cups, for the Bamboo-star-Boxed-cotton house.
- object 1758 (tablet, Harappa) `013-840-740-400 / 003-798-617` : Three descendants of king's servant, for the junior of the Three-Peer house.
- object 1774 (tablet, Harappa) `176-336-740-400 / 700-034` : Four cups, for the junior of the Tax-Town house.
- object 1776 (tablet, Harappa) `240-636-740-400 / 125-700` : The junior of the High-star-Many house: hunter, cup.
- object 1778 (tablet, Harappa) `590-705-868 / 255-435-156-400` : Chief-Rod-Keeper, junior: chest, half a kalam.
- object 1779 (tablet, Harappa) `590-706-868 / 255-435-156-400` : Chief-Rod-Keeper, junior: chest, half a kalam.
- object 1781 (tablet, Harappa) `590-705-868 / 240-231-520-400` : High-star-First-star-Chief, junior: chest, half a kalam.
- object 1782 (tablet, Harappa) `491-817-740-400 / 033-700` : Three cups, for the junior of the Horn-Share house.
- object 1785 (tablet, Harappa) `240-760-740 / 817-368-690-034-700` : Four cups of banner, bound, for the child of High-star house.
- object 1786 (tablet, Harappa) `002-840-032-740 / 817-368-645-900-033-700` : Three cups of banner, gold weight, month, for the Two-Peer-Two house.
- object 1787 (tablet, Harappa) `413-892-824 / 171-032-031-240-636-740-400` : Three full measures of grain, sale, price, for the junior of the High-star-Many house.
- object 1792 (tablet, Harappa) `416-861-002 / 034-700` : Two shares and four cups of grain heap.
- object 1793 (tablet, Harappa) `416-220-760-740-400 / 004-700-220` : Four cups of star, for the junior of the Grain-heap child of Star house.
- object 1801 (tablet, Harappa) `003-861 / 061-255-740` : Three shares, for the Quarter-Chief house.
- object 1802 (tablet, Harappa) `003-861 / 031-520` : Three shares and one chief.
- object 1803 (tablet, Harappa) `003-861 / 031-520` : Three shares and one chief.
- object 1804 (tablet, Harappa) `013-840-740 / 033-700` : Three cups, for the Three-Peer house.
- object 1805 (tablet, Harappa) `013-840-740 / 033-700` : Three cups, for the Three-Peer house.
- object 1807 (tablet, Harappa) `033-700 / 900-368` : Three cups of month, banner.
- object 1808 (tablet, Harappa) `033-700 / 900-368` : Three cups of month, banner.
- object 1809 (tablet, Harappa) `033-700 / 900-368` : Three cups of month, banner.
- object 1810 (tablet, Harappa) `004-900-740 / 032-700` : Two cups, for the Four-Moon house.
- object 1813 (tablet, Harappa) `700-034 / 176-740-400` : Four cups, for the junior of the Tax house.
- object 1814 (tablet, Harappa) `033-700 / 176-740-400` : Three cups, for the junior of the Tax house.
- object 1815 (tablet, Harappa) `176-740-400 / 033-700` : Three cups, for the junior of the Tax house.
- object 1816 (tablet, Harappa) `176-740-400 / 034-700` : Four cups, for the junior of the Tax house.
- object 1818 (tablet, Harappa) `415-220-520 / 700-034` : Four cups, for Branch-Star, chief.
- object 1819 (tablet, Harappa) `034-700 / 415-220-520` : Four cups, for Branch-Star, chief.
- object 1821 (tablet, Harappa) `003-645-032-590 / 415-220-520` : Three lots of two gold weights of chest, for Branch-Star, chief.
- object 1822 (tablet, Harappa) `016-220-520 / 700-033` : Three cups, for Six-Star, chief.
- object 1823 (tablet, Harappa) `592-158-400 / 032-700` : Two cups, for Pen-Keeper, junior.
- object 1824 (tablet, Harappa) `592-158-400 / 032-700` : Two cups, for Pen-Keeper, junior.
- object 1837 (tablet, Harappa) `034-700 / 176-740-400` : Four cups, for the junior of the Tax house.
- object 1839 (tablet, Harappa) `176-740-400 / 032-700` : Two cups, for the junior of the Tax house.
- object 1842 (tablet, Harappa) `240-636-690-740 / 032-700` : Two cups, for the High-star-Many-Ally house.
- object 1843 (tablet, Harappa) `240-636-690-740 / 032-700` : Two cups, for the High-star-Many-Ally house.
- object 1845 (tablet, Harappa) `032-700 / 233-550-526` : Two cups of scabbard-fish, gate, guard.
- object 1852 (tablet, Harappa) `382-760-740 / 032-700` : Two cups, for the child of King house.
- object 1853 (tablet, Harappa) `137-400 / 033-700` : Three cups, for Cultivator, junior.
- object 1855 (tablet, Harappa) `176-740-400 / 033-700` : Three cups, for the junior of the Tax house.
- object 1856 (tablet, Harappa) `033-700 / 176-740-400` : Three cups, for the junior of the Tax house.
- object 1858 (seal, Harappa) `031-388-740 / 034-700` : Four cups, for the One-King house.
- object 1861 (tablet, Harappa) `034-700 / 255-435-156` : Four cups, for Chief-Rod, keeper.
- object 1864 (tablet, Harappa) `413-892-824 / 171-032-031-240-636-740-400` : Three full measures of grain, sale, price, for the junior of the High-star-Many house.
- object 1945 (pot, Kalibangan) `700-798-740 / 032` : Two, for the Cup-Descendant house.
- object 2176 (seal, Mohenjo-daro) `798-017-575-740-679 / 575-740-679` : Seven great measures, for the throne of the Descendant house and the throne of the Great measure house.
- object 2322 (tablet, Mohenjo-daro) `690-323 / 550-060-690-740` : Gate the Ally house: bound, ration.
- object 2367 (tablet, Mohenjo-daro) `705-167 / 705-167` : Kalam, wages.
- object 2432 (tablet, Mohenjo-daro) `220-840-032-740 / 220-798-550-527` : The Star-Peer-Two house: star, descendant, gate, guard.
- object 2488 (copper tablet, Mohenjo-daro) `003-422 / 705-033-923-740-001` : Three fields and three kalam and one, for the Ivory house.
- object 2836 (seal, Mohenjo-daro) `575-031 / 575-031-002-003-390` : One great measure and six cottons, for Great measure.
- object 2934 (tablet, Mohenjo-daro) `706-167 / 706-167` : Kalam, wages.
- object 2955 (tablet, Mohenjo-daro) `540 / 473-806-158-400` : N loads of produce, carried by the porter of rice measure, junior.
- object 2978 (seal, Mohenjo-daro) `323-690 / 550-060-690-740` : Gate Ration-Ally and the Ally house.
- object 2987 (copper tablet, Mohenjo-daro) `003-700-900-165 / 032-220-176-740` : Three cups of month, day, for the Two-Star-Tax house.
- object 2988 (copper tablet, Mohenjo-daro) `003-700-900-165 / 032-220-176-740` : Three cups of month, day, for the Two-Star-Tax house.
- object 2989 (copper tablet, Mohenjo-daro) `005-706 / 233-585-407` : Five kalam of scabbard-fish, maiden, kindred.
- object 2990 (copper tablet, Mohenjo-daro) `005-706 / 233-585-407` : Five kalam of scabbard-fish, maiden, kindred.
- object 2991 (copper tablet, Mohenjo-daro) `005-706 / 233-585-407` : Five kalam of scabbard-fish, maiden, kindred.
- object 3044 (copper tablet, Mohenjo-daro) `861-368-001-142-617 / 235-233-222-740` : One king of banner, king's servant, for the Bamboo-star-Scabbard-fish-Shut-in-fish house.
- object 3556 (seal, Mohenjo-daro) `034-220-520 / 861-002-255-435-690-740` : Two shares Four-Star, chief and the Chief-Rod-Ally house.
- object 3566 (other, Mohenjo-daro) `031-156 / 031-156` : One porter.
- object 3706 (tablet, Mohenjo-daro) `540 / 467-806-158-400` : N loads of produce, carried by the porter of rice measure, junior.
- object 3714 (tablet, Mohenjo-daro) `384-740 / 384-740 / 384-740` : The King house.
- object 3725 (tablet, Mohenjo-daro) `323-690 / 550-060-690-740` : Gate the Ally house: ration, bound.
- object 3726 (tablet, Mohenjo-daro) `323-690 / 550-060-690-740` : Gate the Ally house: ration, bound.
- object 3730 (copper tablet, Mohenjo-daro) `806-231-176-740 / 590-407-740` : The Bounty-First-star-Tax house and the Chest-Kindred house.
- object 3734 (copper tablet, Mohenjo-daro) `415-220-845-407 / 590-405-100-740-790` : The gem of the Chest-Thread-Elder house: branch, star, sheaf-bundle, kindred.
- object 3735 (copper tablet, Mohenjo-daro) `142-617-001-004-407 / 900-165` : Five kindreds of king, king's servant, month, day.
- object 3737 (copper tablet, Mohenjo-daro) `035 / 773-740` : Five, for the Child of house.
- object 3820 (pot, Mohenjo-daro) `033-151 / 033-151` : Three porters.
- object 3846 (tablet, Mohenjo-daro) `370-390 / 370-390` : Spindle, cotton.
- object 3868 (tag or sealing, Rakhigarhi) `820-032-130 / 820-032-130` : Two quarters husbandman.
- object 3932 (tablet, Harappa) `034-700 / 176-100-740` : Four cups, for the Tax-Elder house.
- object 3949 (tablet, Harappa) `850-740 / 850-740` : The Share house.
- object 3959 (tablet, Harappa) `817-002-240-904-740 / 032-700` : Two cups, for the High-star-Dark-moon house.
- object 3970 (tablet, Harappa) `861-002-240-482-740 / 235-220-176-740` : Two shares the High-star-Hill-share house and the Bamboo-star-Star-Tax house.
- object 3971 (tablet, Harappa) `861-002-240-482-740 / 235-220-176-740` : Two shares the High-star-Hill-share house and the Bamboo-star-Star-Tax house.
- object 3976 (tablet, Harappa) `817-368-690 / 679-840-032-740` : Share the Throne-Peer-Two house: banner, bound.
- object 3980 (tablet, Harappa) `742 / 742 / 742` : Second-ward house.
- object 4016 (tablet, Mohenjo-daro) `927-740-031-095 / 927-740` : One staff-bearer, for the Two-moons house.
- object 4031 (tablet, Harappa) `240-636-740-400 / 125-700` : The junior of the High-star-Many house: hunter, cup.
- object 4052 (tablet, Harappa) `255-435-156-400 / 590-706-868` : Chief-Rod-Keeper, junior: chest, half a kalam.
- object 4056 (tablet, Harappa) `416-220-760-740-400 / 004-700-220` : Four cups of star, for the junior of the Grain-heap child of Star house.
- object 4059 (tablet, Harappa) `820-031-001-061-740 / 033-700` : One quarter and three cups, for the house.
- object 4069 (tablet, Harappa) `415-220-520 / 034-700` : Four cups, for Branch-Star, chief.
- object 4073 (tablet, Harappa) `176-740-400 / 033-700` : Three cups, for the junior of the Tax house.
- object 4077 (tablet, Harappa) `176-740-400 / 033-700` : Three cups, for the junior of the Tax house.
- object 4085 (tablet, Harappa) `176-740-400 / 033-700` : Three cups, for the junior of the Tax house.
- object 4086 (tablet, Harappa) `176-740-400 / 033-700` : Three cups, for the junior of the Tax house.
- object 4087 (tablet, Harappa) `176-740-400 / 033-700` : Three cups, for the junior of the Tax house.
- object 4088 (tablet, Harappa) `176-740-400 / 033-700` : Three cups, for the junior of the Tax house.
- object 4409 (tablet, Harappa) `742 / 742 / 742` : Second-ward house.
- object 4935 (tablet, Harappa) `817-368-690 / 679-840-032-740` : Share the Throne-Peer-Two house: banner, bound.
- object 5242 (tablet, Lakhanjo-daro) `156 / 382-382-382` : Keeper, three kings.
- object 5470 (tablet, Harappa) `176-740-400 / 033-700` : Three cups, for the junior of the Tax house.
