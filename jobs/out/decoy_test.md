# Decoy test: how often does a wrong word pass?

List built by `work_scripts/decoy_build.py` (seeds in the script): 60 content-word signs from `work_data/values_master3.csv` (status strict), 30 with their accepted word, 30 with the word of a different sign of the same job class and frequency band. Two testers (A: Sonnet, B: Opus) saw only the list and a loader with corpus facts (`work_scripts/decoy_loader.py`). Each wrote all 60 predictions from the word's meaning before computing anything, ran each once, no second tries. Predictions and code: `work_scripts/decoy_test_A.py`, `decoy_test_B.py`; outcomes: `work_data/decoy/results_A.csv`, `results_B.csv`; key: `work_data/decoy/KEY_do_not_open.csv`.

## What came out
- `measured` Came true (right direction, P below 0.05 on the shuffle): tester A real 4 of 30, decoy 3 of 30; tester B real 5 of 28, decoy 7 of 30. Pooled: real 9 of 58 (15.5%), decoy 10 of 60 (16.7%); Fisher P 1.0.
- `measured` Right direction at all: real 27 of 58, decoy 25 of 60.
- `measured` Only one item came true for both testers on a real word (900, month: counted). One decoy came true for both (407 given a star-name word).

## What it means
Went against. A prediction written blind from the word's meaning passes as often for a wrong word of the same job as for the accepted word. Real words pass only about one time in six under this design, far below the rates reported in the sound passes, where the agent choosing the word had already looked at the sign's data. So the "prediction came true" counts in the sound passes do not separate a right word from a wrong word of the same job, and the strict / wide labels do not either. What the predictions that pass have in common is the job (counted thing, place word, title), which is the frame again.

What this does not touch: everything measured without a word (template, name structure, managers in the master's house, quarter sign before king sign, measures in twelves, unit order, time-flat system, findspot results), and the language-family pun test (Dravidian 7 of 9 against 1.02 expected; Munda 0 of 9; Sumerian 1 of 8), which was scored against chance inside each dictionary.

## Rescue (one redesign, per the rules)
Method replay: give fresh testers the same mixed list and let them do exactly what the sound passes did (look at the sign's data first, then write a prediction, one redesign on a miss). If decoys pass as often as real words under the full method, the word list has no support beyond job class. If real words pass far more often, the blind design above simply lacked power.
