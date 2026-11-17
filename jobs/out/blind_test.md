# Blind test: real word list against scrambled ones

Set built by `work_scripts/blind_build.py` (seeds in the script); scored by `work_scripts/blind_score.py`; grades in `work_data/blind/grades_A.csv`, `grades_B.csv`, `grades_C.csv` (three readers who saw only the English line and the object kind).

60 inscriptions that read whole, each turned into English four ways with the same rules: the real word list; S1 words dealt freely to the wrong signs; S2 words dealt only among signs doing the same job (opener, crest, ending, measure, other; numbers fixed); S3 words dealt among equally common signs. 240 lines, mixed.

## What came out
- `measured` Share graded "sense" (readers A / B / C): real 36.7 / 35.0 / 35.0%; S1 10.0 / 11.7 / 16.7%; S2 26.7 / 26.7 / 26.7%; S3 6.7 / 8.3 / 8.3%. Meaning: real lines read as sense three to five times as often as freely scrambled ones; against the same-job shuffle the gap is 35% to 27%.
- `measured` Sense by at least two of three readers: real 18 of 60, S2 16, S1 6, S3 4.
- `measured` Paired per inscription, real against scramble, better / same / worse: reader A S1 22/33/5, S2 14/41/5, S3 23/34/3; reader B S1 22/36/2, S2 15/44/1, S3 28/30/2; reader C S1 14/43/3, S2 9/47/4, S3 17/42/1. Pooled over readers for S2: seals 14 better, 5 worse; tablets 21 better, 3 worse. Meaning: when the two differ, the real line wins about four times in five even against the same-job shuffle.
- `measured` Tablets: real 50 to 53% sense for all three readers. Seals: real 9 to 27% sense, most graded odd.
- `measured` Reader agreement on the 240 grades: A-B 180, A-C 206, B-C 162.

## What it means
- The word list carries real information: scrambling it makes the readings worse for every reader.
- Much of the "sense" comes from the frame (which sign is an opener, a crest, an ending, a measure): keeping the frame and moving words within a job loses only part of it. The content words inside one job class (which crest is which word, which personal part is which word) are the soft layer.
- Went against: strangers grade only about a third of whole readings as plain sense, where the builder's own draw gave 73%. Most seal readings look odd to an outsider (long stacked house names).

## Rescue
1. Forced choice: show the four versions of one inscription side by side and ask which reads most like a real label. That does not depend on each reader's bar for "sense".
2. Work the soft layer: test content words within a job class against each other (crest against crest) with outside facts, not slot facts.
3. Look at what readers called odd in real seal lines and fix the English for names (a name is a name; show it as one).

## Side-by-side test (forced choice), `work_data/blind2/`
120 inscriptions (50 seals, 50 tablets, 20 other); each row shows four English lines of one text: real, S1 (words dealt freely), S2 and S2b (two separate deals among signs doing the same job). Three readers pick the one that reads most like a real label. Chance 25.8%. Scored by `work_scripts/blind2_score.py`.
- `measured` Real picked best: reader A 33 of 120 (27.5%; A picked option "a" 80 times and said it fell back on the first option), reader B 33 (27.5%), reader C 39 (32.5%). Pooled 105 of 360 = 29.2%.
- `measured` Who was picked best, pooled: real 29.2%, S1 14.4%, S2 34.2%, S2b 22.2%. One same-job shuffle was picked more often than the real list.
- `measured` By kind, pooled: seals real best 36.7% (P 0.001), tablets 22.7%, rest 26.7%. At least two of three readers picked the real line on 32 of 120 items (20.1 expected by luck).
- `measured` Without the 7 rows where a scrambled line has a give-away dangling "Child of": reader B 28 of 113, reader C 35 of 113.

What it means. Went against: a reader shown four versions cannot pick the real one from same-job shuffles (29% against 26% chance), though free shuffles are picked out as worse (14%). By how plausible the English sounds, the real word on a crest, a name part or a counted thing cannot be told from another word of the same kind: "Four cups" and "Four porters" are equally good tablet lines. So the English-plausibility test measures the frame, and it has no power on the content words. The first test's 35% against 27% was within the spread between two same-job shuffles here (34% and 22%).

Rescue (redesign once): test the content words by what the method itself does with a WRONG word. Hand a tester a list of signs with words, some real and some swapped from another sign of the same job, without saying which; the tester writes a prediction first and runs it on outside facts (object kind, picture side, findspot, counts, new texts). The share of decoys that "come true" is the false-alarm rate of the whole method; the share of real values that come true, set beside it, is what the word list is worth.
