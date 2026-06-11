# Source-route updates for the four blocking objects

Date: 2026-06-11 America/Los_Angeles

Status: acquisition-route recheck from a fresh external sweep. No evidence-tier change. No value, phonetics, language identity, function, sign meaning, or translation is accepted. This extends — does not contradict — the 2026-05-31 per-target docs and `campaign_032_002_861_002390x_current_decision_state_20260531.md`.

Environment note: this run's network allowlist passes the approved search proxy but blocks direct artifact download (`Host not in allowlist` on raw arxiv/wikimedia pulls; HTTP 403 on harappa.com and the Wikimedia file page to automated fetch). Routes and metadata were confirmable; binary source images were not fetchable here.

## Shared finding: the gated source volume identity is re-confirmed, and a newer strand appears

CISI 3.1 is independently re-confirmed as the shared source for H-1993 and M-1825:

- *Corpus of Indus Seals and Inscriptions, Volume 3: New material, untraced objects, and collections outside India and Pakistan, Part 1: Mohenjo-daro and Harappa.* Ed. Asko Parpola, B. M. Pande, Petteri Koskikallio, with Richard H. Meadow and J. Mark Kenoyer. Suomalainen Tiedeakatemia, Helsinki, 2010. 504 pp. Annales Academiae Scientiarum Fennicae Humaniora 359 / Memoirs of the ASI no. 96. ISBN 9789514110405. Photographs, line drawings, tables.
- Routes: `https://www.harappa.com/content/corpus-indus-seals-and-inscriptions-vol-31` (403 to automated fetch, but indexed); Helsinki research portal; Cambridge JRAS review `B9CCB96DD82777E486D2FF40B10B0052`; AbeBooks ISBN `9789514110405`; academia.edu record `89021072` (access-gated).
- Still no free full-volume image binding obtained. State matches the prior run's "Tiedekirja payment-pending" ceiling.

New strand not in the prior run: **CISI vol. 3.3 (2022, ed. Parpola & Koskikallio, Finnish Academy of Science and Letters)** exists and is the "new material / untraced objects / collections outside India and Pakistan" continuation; it carries e.g. Potts (2022) on Tepe Yahya graffiti. academia.edu `94861598`, `94880292`. Because the vol. 3 series is explicitly the *untraced/unprovenanced* strand, vols. 3.2/3.3 are the right next place to chase 3335.1 (`RAF`, no CISI id) before declaring its source dead.

## Target 1 — H-1993 / H96-2769 / Figure 17.07 (repeated `095`)

- Prior state: `h1993_cisi3_plate_range_identified_no_image_binding` — CISI 3.1 HARP photo section pp. 207–360 and basic-data pp. 423–441 identified as containing it; public PDF is only a 17-page front-matter excerpt.
- This sweep: re-confirms the Meadow/Kenoyer Harappa authorship and the CISI 3.1 target; no free image of H-1993 or H96-2769 was reachable. The "Figure 17.07" ambiguity guard (H-1803 also hooks Figure 17.07 via H94-2193) stands — a naked figure number is still not a bridge.
- Updated status: `h1993_cisi31_target_reconfirmed_no_free_image_binding`.
- Next gate: acquire CISI 3.1 (purchase/library) and inspect the pp. 207–360 / 423–441 ranges for H-1993 specifically, or recover an H96-2769 plate/caption. Keep H-1993 out of strict `095` counts until then.

## Target 2 — Dholavira 8758 / ZA-12:2 / 4237.1 (repeated `705`)

- Prior state: `dholavira_8758_source_contact_sent_awaiting_reply_no_values` — Bisht 2015 OCR mirror exposes the `8758 / ZA-12:2 / 27.62 x 21.31 x 7.11-11.17` cluster and a National Museum "no other details" remark, but no image binding. Guard: page-18 item-10 is Acc. No. 2118 (5 signs) — a lookalike. ICIT 4348 is a different gapped `002-861-390` row, not a bridge.
- This sweep: the most authoritative non-OCR route is the ASI publication itself, *Excavations at Dholavira (1989–90 to 2004–05)*, R. S. Bisht, Archaeological Survey of India, 2015. The pdfcoffee OCR mirror remains the only frictionless text route found; no museum-database image binding Acc. No. 8758 to the six-sign seal was reachable here. National Museum New Delhi / Museums-of-India (JATAN) portals are the right archival targets but were not bindable in this environment.
- Updated status: `dholavira_8758_asi_2015_route_confirmed_no_image_binding`. Both guards (Acc. 2118 lookalike; ICIT 4348) re-affirmed.
- Next gate: obtain the ASI 2015 volume plates or a National Museum catalogue entry that binds Acc. No. 8758 / ZA-12:2 to an image and sign count. No strict `705` until then.

## Target 3 — M-1825 / BJ25710 (repeated `705`)

- Prior state: `m1825_ia_pakistan_absent_secondary_icon_only_no_signband` — absent from the public IA "Collections in Pakistan" OCR/XML (plates visible only to ~M-1657/1658); Bhaskar et al. zoomorphic catalogue lists M-1825 as F2 unicorn but gives no inscription.
- This sweep: M-1825 is above the M-range covered by the public CISI vol. 2 ("Collections in Pakistan") plate run, which is consistent with M-1825 belonging to the **CISI vol. 3 "new material" supplement** rather than vol. 2 — i.e., the same gated CISI 3.x target as H-1993, reinforcing the shared-volume acquisition strategy. No object→image→sign-band bridge was reachable; the `BJ25710` pointer remains an unresolved excavation/registry handle.
- Updated status: `m1825_cisi3_supplement_scope_reconfirmed_no_signband`.
- Next gate: inspect CISI 3.x for M-1825, or find a Mohenjo-daro museum register binding `BJ25710` to an image/sign band. Icon-class lists do not count. No strict `705` until then.

## Target 4 — 3335.1 / `740-205-032-002-390-590-032` (`RAF`, no CISI id)

- Prior state: `3335_1_m940_false_bridge_rejected_object_id_blocked_no_source_count` — M-940 false bridge rejected (M-940 is a distinct 4-sign row, visible on CISI India n125); Lipi/Yajnadevam pinned history yields only an old `Private collection` field; private-collection web scout and cluster probe exhausted; `RAF` is a source-family/context tag (57 rows), not an object bridge.
- This sweep, honoring the "do not re-loop Lipi/sibling-3118/auctions" instruction: the one *new, non-exhausted* lead is structural to the corpus itself — an unprovenanced `Private collection` / `RAF` seal with no CISI id is exactly the class CISI vol. 3 is built to catalogue ("untraced objects, and collections outside India and Pakistan"). So the next non-looping route is to check **CISI vol. 3.2/3.3 untraced-object plates** for a 2.9 × 2.9 cm Bull1:J square seal carrying `740-205-032-002-390-590-032`, rather than more Lipi/auction triangulation.
- Updated status: `3335_1_cisi3_untraced_strand_identified_object_id_still_blocked_no_source_count`.
- Next gate: when CISI 3.x is acquired, scan the untraced/private-collection plates for the seven-sign Bull1:J seal; otherwise keep 3335.1 out of strict counts. The prior `[yajnadevam-email]` provenance request remains the other open branch.

## Consequence

No strict count moves. The four targets stay acquisition-gated. The actionable change is a single sharper acquisition strategy: **acquire the CISI vol. 3 series (3.1 for H-1993/M-1825; 3.2/3.3 untraced strand for 3335.1)** as one coordinated purchase/library action, instead of four separate object hunts. Dholavira 8758 stays on the ASI-2015 / National Museum route. Grammar/function promotion remains blocked pending source images.
