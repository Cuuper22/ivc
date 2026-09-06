# Reconstructed completion pass

The earlier completion files were lost after an unsuccessful push. This package rebuilds executable research from Git checkpoint0ad84ef and held sources. These are newly run results, not a byte-for-byte restoration. RECOVERY.md preserves what the conversation recorded about the lost pass separately.

The reconstructed execution includes27 writing-operation/latent-role candidates, six matched graphical controls, nine referent/context models, 815 numerical programs, eight mixed/rival linguistic systems and three optimized phonetic alternatives. Joint fitting completed 189 ABC candidates across seven frozen tasks, then 14 language-conditioned joint systems. No new reading or language identification is accepted.

| Frozen task | Training-selected joint model | Gain over identity, bits |
|---|---|---:|
| recombination_0 | tick388-after__r1 | -4.6608 |
| recombination_1 | tick388-after__r1 | -0.9786 |
| recombination_2 | tick388-after__r1 | -4.6527 |
| recombination_3 | tick388-after__r1 | -1.4653 |
| recombination_4 | tick388-after__r1 | 4.5786 |
| unseen_family_70_71 | tick388-after__r1 | -35.6431 |
| medium_3 | identity__r1 | 0.0000 |

Negative gain means the selected graphical system predicts the held original observations worse. Lexical-prior energies are reported separately and cannot identify a language from dictionaries of different coverage.

Run `python completion/run_completion.py --stage verify` from the campaign directory to check the retained execution package. Use `--stage all` to execute the whole reconstructed campaign, or individual stages. All source observations remain fixed. The continuation state names the next unexecuted discriminating experiment without implying unattended work.

Key files: candidate_ledger.json, claim_dependencies.json, WORKED_EXAMPLES.md, audit/task_status.json, verification.json, experiment_queue.json and continuation.json. The original campaign artifacts outside completion remain available as the recovered checkpoint, including the earlier exact structured alignments.
