# rmn.re history — link-table evolution (2026-09-27)

Archive recovery lane 2. Goal: reconstruct how the rmn.re YOURLS link table
evolved — when campaign-grammar slugs first appeared, which died, and the
growth curve. The Wayback CDX listing failed (upstream HTTP 500, not retried),
but it turned out the archive was unnecessary: YOURLS records each slug's own
creation timestamp, and the live crawl captured all 764 of them.

## Archive findings (thin)

- The archive holds **exactly one** rmn.re homepage snapshot: **2025-06-22**,
  pre-campaign. Probes for 2026-06-17, 2026-07-15, and 2026-09-01 all resolve
  to it — no campaign-era captures exist.
- Snapshot playback returned upstream HTTP 500 from this network, so even the
  2025-06-22 page body could not be retrieved. Existence and timestamp are
  recorded in `data/rmn-re-history/archive_lookup.json`.

## Growth curve (from YOURLS creation dates)

| Period | Cumulative links |
|---|---|
| 2016-12 → 2020-10 | 6 → 138 (slow organic use) |
| 2020-10 → 2026-04 | 138 → 214 (dormant, ~1–5/mo) |
| 2026-05 | 231 (+17) |
| **2026-06** | **715 (+484 in one month)** |
| 2026-07 | 744 (+29) |
| 2026-08 | 754 (+10) |
| 2026-09 | 764 (+10, still active) |

The June 2026 burst is the campaign: 484 new slugs in one month against a
baseline of single digits.

## Campaign-grammar first appearances

- `zz`: `zzzz` on 2020-03-12 — a generic test slug, not campaign-shaped. The
  campaign `zzNNNNNN` family starts 2026-06-17 19:17 UTC (`zz1146554`,
  `zz1017082`, `zz995275` in the same minute).
- `epoch10`: `mailtest1779882833` on **2026-05-27** 15:53 UTC — "mailtest" +
  epoch, tying the shortener's campaign use to the mail.gw disposable-inbox
  OTP-read step from the same week.
- `oai`: `oaix5507` on **2026-06-16** 12:34 UTC; `oaitest93446019` on 06-17.

June-2026 creations (484): 88 epoch10, 32 zz, 3 oai, 3 epoch10+oai, 1
epoch10+zz — **127 campaign-grammar slugs**, all in one month. Top June
targets: 192 viz.aihw.gov.au (PBS Tableau workbook, ~10h burst 06-17),
sec.gov county data, md.succ.ai / allorigins reader chains,
api.worldpoverty.io, api.dataafrica.io.

## Deaths: zero

All 499 slugs from the preserved June log persist in the current table —
**nothing died**. The 265 slugs absent from the log are mostly pre-2026
organic links the publisher-selected log didn't include (its crawl window was
2026-05-26 → 06-21 and it was agent-text-selected, not a census). The
shortener is append-only in the observed window.

## What this means

- The campaign's shortener footprint is fully dated by the shortener itself:
  **May 27 (mailtest epoch slugs) → June 16–17 (oai + zz bursts + AIHW)**.
- The archive has no record of the campaign-era front page; the live crawl +
  YOURLS timestamps are the primary source, and they are complete.

## Files

- `data/rmn-re-history/` — slug_evolution.jsonl (764), growth_curve.json,
  grammar_first_appearance.json, archive_lookup.json, manifest.json,
  PROVENANCE.md
- Elastic: `rmn-re-history` index, 764 docs (own index, shared schema)

Source URLs: https://rmn.re/ (public index, no auth) ·
https://archive.org/wayback/available?url=rmn.re
