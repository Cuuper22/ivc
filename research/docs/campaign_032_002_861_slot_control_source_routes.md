# Campaign 032 Slot-Control Source Routes

Date: 2026-05-29

Question: do the control-side rows `H-823`, `H-1845`, and `H-237` upgrade enough to carry the `603/636/642` slot-family contrast?

This is source routing and evidence weighting. It is not sign reading.

## Decisions

| target | X | previous | new status | working weight | decision |
|---|---:|---|---|---:|---|
| `H-823` | `636` | metadata_route_only | exact_route_dark_after_cisi_ia_and_web_checks | 0.25 | H-823 keeps only the local H88-1196 route; public CISI IA OCR and checked web search did not locate an image or page route. |
| `H-1845` | `642` | public_page_route_visible_not_local | public_harappa_route_visible_shell_download_blocked_cisi_public_ocr_unlocated | 0.75 | H-1845 remains a real public-route source control via Harappa.com/H2000-4484 / 2227-15 / Figure 42.05, but no local image was acquired and no CISI IA OCR route was found. |
| `H-237` | `642` | metadata_only_no_excavation_id | metadata_only_no_excavation_route_ref_clone_pressure | 0.05 | H-237 remains metadata-only. The local current export gives ref:424.2 for its SP text, so it is clone-pressure on H-1845 rather than independent source weight. |

## Source Search Result

- CISI IA OCR route rows found: `0`.
- Local text-file rows found: `58`.
- External web search in this turn did not locate `H88-1196`, `H-823`, or `H-237` source pages.
- Harappa.com remains the only public visible route for `H-1845/H2000-4484/2227-15`, but direct local download is Cloudflare-blocked.

## Consequence For The Slot-Family Contrast

`636/642` controls are still weaker than `603` on source weight. `H-360` remains the only source-visible `636` control, while `H-823` is route-dark. `H-1845` remains a public-route `642` control, but `H-237` is demoted to near-zero independent weight because the local current export marks its text as `ref:424.2` and gives no excavation route.

This does not kill the `240-060-692` subframe. It does narrow what can be claimed: the current source-normalized contrast is strong enough to keep `603` as the live bridge target, but not strong enough to treat `636/642` as fully source-balanced negative controls.

Accepted values/translations remain 0.
