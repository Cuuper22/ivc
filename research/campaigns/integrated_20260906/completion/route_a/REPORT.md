# Reconstructed Route A

Executed 27 graphical-program/latent-role fits on the recovered raw sign observations, six selection-matched graphical pairing controls. Seven common frozen comparisons are executed by the coordinator joint runner. Full machine-readable results are in summary.json, matched_controls.json, contextual_evaluations.json, and the coordinator joint results.

The grammar learns role emissions and transitions jointly by forward-backward EM. Emissions are normalized across the 417 ORIGINAL signs, using proposed graphical components as tied features. A latent role change defines an anonymous segmentation boundary. Rule and parameter costs are explicit. Exact-expression duplicates have one unit of weight. No source spelling changes.

Expansion placement is modeled through preceding/following latent component roles. Additional placement predictions remain in the recovered structured alignment and composition experiments, which include one-edit anchored alignments and partial visible islands. The grammar is a constrained categorical spelling model, not proof of phonetic or semantic meaning. Its implicit equivalences remain conditional.

Partial observations are scored with doubtful identities marginalized over all signs; unknown spans break independent visible islands. They are not imputed training examples. This avoids inventing span lengths but does not model uncertain-length bridges.

These are newly computed reconstruction results. Exact lost numeric results were not recreated from memory. All model parameters, optimization traces, held-out predictions, and matched control selections are preserved.

973 partial records receive explicit visible-island marginal scores. run_contextual.py executes the site and object-class rivals on all seven frozen raw-text masks. See INTERPRETATION.md for the substantive comparison and disagreement with the previously proposed1147 boundary repair.

Run from this directory with `OPENBLAS_NUM_THREADS=1 python run.py`, then `OPENBLAS_NUM_THREADS=1 python finish_controls.py`, then `OPENBLAS_NUM_THREADS=1 python run_contextual.py`. The main runner resumes saved full fits and completed control searches. All27 full fits and all162 matched-control fits converged; two control fits required extending the declared160-iteration cap to320. The six matched searches all select the same identity model. The coordinator owns the separate seven-fold joint execution.
