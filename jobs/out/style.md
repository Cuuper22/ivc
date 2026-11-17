# Style: a cutting-style code made from the stones

Word-free job, 2026-11-17. Photos, sign numbers, findspots and sizes only. Scripts, run in order, each with its rules and predictions in its top docstring written before its numbers: `work_scripts/style_common.py` (feature list, loader, sheet maker), `style_1_sample.py` (draws and predictions), `style_2_agree.py`, `style_3_cluster.py`, `style_4_tests.py`, `style_5_redesign.py`, `style_6_thin.py`, `style_7_twinsplit.py`. Codes, keys, sheets and logs: `work_data/style/` (8.3 MB).

## Plain words

- **Style code**: twelve drawing habits read off a seal photo, each with 2 to 4 values, fixed in `style_common.py` before any stone was coded: neck (plain / folds = many thin ridges across the throat / bands = 2 to 4 broad collar bands), shoulder (plain / outlined = a double line round shoulder and chest / heart = a heart-shaped shoulder mark), horn, eye, tail, hoof, the stand's upper part (cage = tall ribbed or grid box / box = small low box / round = dome, globe or crescent / none), the stand's lower part or bowl (plain / patterned / a second box), the stand's shaft, **sign cutting** (thin = narrow fine strokes / broad = wide rounded strokes / drilled ends), frame line round the field, and **spacing** (tight = the text touches the bull's back or horn / gap = a clear band between them). `?` = cannot be read on the photo.
- **Blind sheets**: contact sheets of 16 photos in shuffled order, each labelled with a neutral number (N001...); the key (number to catalogue id) sat in a file I did not open until that set was coded. The printed caption under each photo was cut away by the sheet maker.
- **Style**: a group of stones that share most habits, found by clustering (see step 2). **Stand letter**: the catalogue's W, J, S, I, L.
- **V** (Cramer's V): how strongly two labels go together, 0 = not at all, 1 = fully. **Shuffled**: the same table with one label dealt at random 2,000 to 5,000 times inside the stated groups; **P** = share of deals at least as strong as the real table. Small P = the real link is not chance.
- **Size third**: smallest, middle or largest third of the coded stones by face area. **Small towns**: Lothal, Kalibangan, Chanhu-daro and the other small sites, against the two **big cities** Mohenjo-daro and Harappa.
- **Twin**: two stones with the identical text; **near twin**: same length, one sign different (from the twins job).
- **Sign-pair model**: a table of which sign follows which in one city's seal texts; a text's score under it says how much it reads like that city's texts.

## What was found

1. **The catalogue letter is a coarse label over five drawing styles, and W is mostly one of them.** 365 unicorn stones were coded blind (300 drawn by seed across cities and letters, 65 more from twin pairs); 293 fall into five main styles and 8 into three rare ones. Style goes with the letter at V 0.279 against 0.129 with letters shuffled inside each city (P below 1 in 5,000). The big ornate banded style S4 is W on 22 of its 29 lettered stones (76%, against W's 30% of all lettered coded stones); the folded broad style S1 holds most I stones (29 of 40). Means: what the cataloguer called W is chiefly one manner (banded collar, outlined or heart shoulder, tall cage stand, clear band under the text, big stone); the other letters spread across styles. Opens: the style code replaces the letter for sorting hands; the code sorts more finely than the letter, since one letter (J) holds four styles.

2. **The clearest city mark is how the signs are cut: the small towns cut thin, the big cities cut broad.** Thin cutting: Lothal 59%, the small sites 55%, Chanhu-daro 37%, Kalibangan 36%, Harappa 17%, Mohenjo-daro 19% (339 stones; V 0.319 against 0.120 with cities shuffled inside size thirds, P below 1 in 2,000). It holds inside every size third: big stones 55% thin in the small towns against 31% at Mohenjo-daro and 20% at Harappa; middle 50% against 26% and 26%. Two more city habits: Kalibangan stand tops are round (domes) 55% against 10 to 18% elsewhere (P 0.001); heart-shaped shoulders are a Harappa habit, 18% against 7% at Mohenjo-daro and 0 to 5% elsewhere (P 0.025). The whole style mix goes with city too, V 0.186 against 0.131 inside size thirds (P 0.007). Means: the small towns had their own sign cutters with their own stroke, Kalibangan its own stand drawing, Harappa its own shoulder mark. Opens: Lothal, the town with the most unfinished stones (hands job), also has the most distinct cutting hand: a local workshop line with a measurable signature.

3. **Style goes with size, and does not go with time or with what the text says.** Median face: S4 1,123 mm2, S5 748, S2 713, S3 656, S1 524 (between-style spread 0.068 against 0.004 with styles shuffled inside city, P below 1 in 5,000). Time bin: inside Mohenjo-daro V 0.191 against 0.189 (P 0.47), inside Harappa 0.272 against 0.246 (P 0.31). Text kind: V 0.143 against 0.144 (P 0.51). The 25 fixed phrases found on 5 or more coded stones, 125 style-by-phrase cells: 0 at P below 0.05 (6.2 expected by chance alone), none at q below 0.1. Means: a cutter's manner was steady over the whole span the bins cover and ignored the text, as the stand job found for the letter; the big ornate style was the manner for big seals.

4. **Near-twin texts in one city were cut in one style; the same text in two cities was not.** Near twins (one sign apart) in the same city share the style 13 of 24 times against 7.4 expected from that city's style mix (P 0.014). Near twins in two cities: 5 of 20 against 5.3. Identical twins in two cities: 1 of 13 against 3.6 (K-19 at Kalibangan is S4 and its twin M-224 at Mohenjo-daro is the heart-shouldered S6, two neighbouring ornate styles). Means: holders of closely related texts in one town went to one shop; when the same text turns up in another city, it was cut there in that city's manner. The text travelled, not the stone.

5. **Stones carried between cities are rare enough that the style code finds almost none.** By the rule fixed first (style at most 10% at home and at least 25% in another city): 1 of 293 stones, C-10 at Chanhu-daro, in the Mohenjo-daro-common style S2, text `817-002-032-220-231-740` (a front formula). Its text leans toward Mohenjo-daro (score +1.56 against +1.20 for other Chanhu-daro stones, one stone, P 0.33). The prediction (8 to 15%) went against; see "What went against".

6. **On zebu, short-horned bull, elephant, rhinoceros and tiger seals, the same features show no city signal.** 80 stones (Harappa 21, Mohenjo-daro 48, small towns 11): neck V 0.198 against 0.132 (P 0.20), shoulder P 0.77, sign cutting P 0.68, spacing P 0.90, cities shuffled inside species. Means: on these beasts the drawing follows the species (elephants smooth-necked and harnessed, bulls folded), and the sample has too few small-town stones (11) to see the thin cut.

### What this says (step 7, with the numbers)

- **How many shop styles**: five main styles (S1 126 stones, S2 69, S3 38, S4 30, S5 30) and three rare ones (S6 5, S7 1, S8 2).
- **Which cities had their own**: none owns a style outright (no style is two-thirds one city; S1 is the largest style at 43 to 50% in Mohenjo-daro, Harappa, Kalibangan and Chanhu-daro, and Lothal is the most even, 24% each for S1, S3 and S5). The cities own habits: the small towns the thin cut (Lothal 59%), Kalibangan the round stand top (55%), Harappa the heart shoulder (18%). Every style is cut in every big city.
- **How much movement**: by the drawing, 1 stone of 293 (0.3%) is in another city's style (Chanhu-daro to Mohenjo-daro). Identical texts in two cities are cut in matching styles 1 of 13 times, below the 3.6 that chance gives.
- **How a person got a seal**: from a cutter in his own town, who worked in one of five manners shared across the civilisation, with his town's stroke on the signs. Related holders in one town used one shop. A text could come from elsewhere (the same title or name formula appears in several cities), but the stone was cut where it was found. This fits the hands job (unfinished stones scattered, a Lothal habit of unfinished stones) and the twins job (twin texts get new beasts and new sizes).

## The styles

Three example ids each (stones with all eleven kept features read).

| style | stones | in plain words | neck | shoulder | stand top | bowl | signs | text to back | median face | letters (lettered stones) | examples |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 folded broad | 126 | ridged throat, plain body, small box or dome stand, wide strokes, text packed down onto the back | folds 76% | plain 90% | box 54%, round 25% | patterned 66% | broad 99% | tight 85% | 524 mm2 | I 29, J 23, S 22, L 14, W 12 | H-411, M-969, C-5 |
| S2 smooth saddled broad | 69 | smooth or banded neck, double line round the shoulder, small box stand, wide strokes, text packed down | plain 52%, bands 48% | outlined 89% | box 78% | patterned 74% | broad 100% | tight 72% | 713 | W 24, J 16, S 15 | M-34, H-502, M-944 |
| S3 folded fine | 38 | ridged throat, dome or box stand, fine strokes; the small-town style | folds 100% | plain 66% | round 56% | patterned 55% | thin 95% | tight 63% | 656 | J 11, I 6, W 5 | L-5, H-68, M-732 |
| S4 banded ornate | 30 | collar bands, outlined or heart shoulder, tall cage stand on a patterned bowl, clear band between text and back; the big stones | bands 97% | outlined 55%, heart 45% | cage 78% | patterned 85% | thin 53% | gap 93% | 1,123 | W 22, S 4, J 2 | H-38, M-54, K-4 |
| S5 smooth fine | 30 | smooth neck, outlined shoulder, small box stand, fine strokes, clear band | plain 100% | outlined 71% | box 73% | patterned 67% | thin 100% | gap 87% | 748 | W 7, J 7, S 3 | M-129, C-9, K-8 |
| S6 heart and curled horn | 5 | heart shoulder with a curled or forked horn | | heart 100% | box | | broad | gap | | W 2 | H-386, M-224, M-229 |
| S7 | 1 | folded neck, curled horn, frame line round the field | | | | | thin | gap | | I | M-965 |
| S8 | 2 | no stand, frame line | | | none | | broad | | | | Ns-8, M-205 |

64 stones (mostly worn or broken; 0 to 2 features readable) got no style.

## Tables

### Self-agreement (`agreement.csv`)

40 stones re-coded on new sheets with new numbers in a new order after the main pass. Rule fixed first: keep a feature if it agrees on 75%+ of at least 15 stones read twice.

| feature | read twice | agree | chance agreement from the value mix | kept |
|---|---|---|---|---|
| neck | 36 | 97% | 37% | yes |
| shoulder | 32 | 97% | 44% | yes |
| horn | 26 | 96% | 90% | yes |
| eye | 2 | 100% | 45% | no (readable on 23 of 300 stones) |
| tail | 27 | 100% | 99% | yes |
| hoof | 32 | 100% | 95% | yes |
| stand top | 31 | 97% | 39% | yes |
| bowl | 23 | 100% | 54% | yes |
| shaft | 19 | 100% | 97% | yes |
| sign cutting | 39 | 95% | 58% | yes |
| frame | 38 | 100% | 98% | yes |
| spacing | 37 | 97% | 53% | yes |

Horn, tail, hoof, shaft and frame are almost one value everywhere (single horn, tail down, plain hoof and shaft, no frame), so they agree but sort nothing; the work is done by neck, shoulder, stand top, bowl, sign cutting and spacing. "Drilled" sign ends were never seen.

### Clustering (`log_3.txt`)

Rule fixed first: Gower distance (share of mismatching features over those read on both stones), average-linkage tree on the 261 stones with 6+ features read, k from 3 to 8, highest mean silhouette among k whose smallest group has 8+ stones, else highest silhouette. No k met the 8-stone floor (one-stone groups split off at every k), so the rule took the highest silhouette: k = 8 (0.294; k = 3 to 7 gave 0.18 to 0.23). 40 stones with 3 to 5 features read were then put with the nearest group.

### Style by city (all coded stones)

| style | Chanhu-daro | Harappa | Kalibangan | Lothal | Mohenjo-daro | other small sites |
|---|---|---|---|---|---|---|
| S1 | 7 | 39 | 11 | 6 | 57 | 6 |
| S2 | 1 | 16 | 3 | 3 | 42 | 4 |
| S3 | 3 | 9 | 5 | 6 | 9 | 6 |
| S4 | 2 | 11 | 2 | 4 | 11 | 0 |
| S5 | 3 | 3 | 1 | 6 | 14 | 3 |
| S6-S8 | 1 | 2 | 0 | 0 | 4 | 1 |
| no style | 3 | 18 | 3 | 10 | 27 | 3 |

### Single features by city (`log_5.txt`, cities shuffled inside size thirds)

| feature | V | shuffled | P | the city pattern |
|---|---|---|---|---|
| sign cutting | 0.319 | 0.120 | below 0.0005 | thin: Lothal 59%, small sites 55%, Chanhu-daro 37%, Kalibangan 36%, Mohenjo-daro 19%, Harappa 17% |
| stand top | 0.237 | 0.140 | 0.001 | round: Kalibangan 55%, others 9-29% |
| shoulder | 0.198 | 0.134 | 0.025 | heart: Harappa 18%, others 0-7% |
| neck | 0.163 | 0.128 | 0.12 | folds: Kalibangan 70%, Harappa 56%, Mohenjo-daro 38% |
| bowl | 0.187 | 0.164 | 0.25 | |
| spacing | 0.119 | 0.126 | 0.55 | |

Thin cutting by size third: small-town stones 19% / 50% / 55% (small / middle / big), Mohenjo-daro 4% / 26% / 31%, Harappa 8% / 26% / 20%.

### Style by time bin (stones with a bin)

| city, bin | S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|---|
| Mohenjo-daro early | 2 | 7 | 1 | 2 | 2 |
| Mohenjo-daro middle | 21 | 15 | 2 | 2 | 5 |
| Mohenjo-daro late | 22 | 11 | 2 | 5 | 7 |
| Harappa middle | 23 | 9 | 7 | 4 | 1 |
| Harappa late | 8 | 3 | 1 | 3 | 1 |

### Twins (`twin_styles.csv`, `log_7.txt`)

| pairs | same style | chance | P |
|---|---|---|---|
| near twins, one city | 13 of 24 | 7.4 | 0.014 |
| near twins, two cities | 5 of 20 | 5.3 | 0.64 |
| identical twins, one city | 2 of 6 | 1.8 | 0.59 |
| identical twins, two cities | 1 of 13 | 3.6 | 0.98 |
| all 63 pairs | 21 (33%) | 31% dealt inside city | 0.42 |

## What went against

- **Travelled stones (prediction 8 to 15%; got 0.3%).** Rescue 1, a continuous test: a drawing-home score (how Harappa-like a stone's six main features are, against Mohenjo-daro, stone left out) against a text-home score (sign-pair models, stone left out): inside Mohenjo-daro rho +0.064 (P 0.23), inside Harappa -0.097 (P 0.80), pooled +0.007 (P 0.45). Rescue 2 (new idea), the cut as the marker: thin-cut stones at the big cities do not have more small-town-like texts (-0.751 against -0.719, P 0.60), and broad-cut stones in the small towns do not have more big-city-like texts (P 0.59). Third way, the stand job's 61 Mohenjo-daro stones with Harappa-like texts: 9 were coded, S2 4, S1 3, S4 2 (S4 22% against 7% for the other Mohenjo-daro stones; 9 stones). The line "a stone's drawing marks the city its text came from" is paused after three ways in: drawing and text are independent at stone level in both big cities. The finding that stands in its place is finding 4: texts move between cities, stones are cut locally.
- **Twins share the style (prediction 60% against 35%).** All pairs 33% against 31% (P 0.42); identical twins across cities 1 of 13. Redesign (after the fact): split by one city / two cities gives finding 4 (one-city near twins 13 of 24, P 0.014).
- **A style owned by one city (prediction: one style two-thirds one city).** None: every style is in both big cities. Redesign: single features (finding 2) carry the city marks the clusters blur.
- **Shops drift through time inside Mohenjo-daro (prediction P below 0.05).** P 0.47 (Harappa 0.31). New idea for next time: depth inside one excavation area, which is finer than the three bins.
- **Other animals (prediction: city signal at 95%).** P 0.20 to 0.90. Redesign: code every small-town zebu, bull, elephant and rhinoceros stone with a photo (the draw had 11) and test only sign cutting, which is the one feature that does not depend on the species.
- **What weakens the blinding.** Sheet `sheet_main_01` was first built without the caption crop, so 16 stones (N001 to N016) were seen once with their printed ids before coding; four later photos still showed a caption (N059 K-8, N159 M-82, R023 M-82, T022 M-657). The 40 re-coded stones were coded in the same session as the first pass, so remembering a photo can raise the agreement figures; the features that do the sorting (neck 97%, shoulder 97%, stand top 97%, sign cutting 95%) agree far above their chance agreement (37 to 58%), but a re-code by a second coder would be the clean figure. Photos are small catalogue scans; eye was unreadable on most stones and was dropped by the rule.

## What each reading predicts next

- Local cutting (finding 2): the thin cut should mark a Lothal stone's sealings too; impressions found at Mohenjo-daro or abroad with a thin cut point to small-town seals in use there. Lothal's unfinished stones (L-55, L-58, L-97) should be thin-cut.
- One shop per circle of holders (finding 4): one-city near-twin pairs that share the style should sit in the same quarter of the city; check their buildings and areas.
- Big seals, big manner (finding 3): S4 is the big-seal style everywhere; S4 stones in the small towns (K-4, L-1) are the rank holders there, and their texts should carry the ranks that make big seals (person and jar + man endings).
