# CORRECTIONS-LOG — LINKHUNT-DEEP corrections applied to upstream writeups

**Date:** 2026-10-05. **Worker:** CORRECTIONS.
**Source:** `linkhunt-deep/LINKHUNT-DEEP.md` §0 (four corrections to prior findings).
**Rule:** original claims preserved inline (struck through or quoted) — retractions are additive, nothing was deleted silently. Evidence values were not redacted in any edit.

## Correction 1 — REMOVE trycloudflare/DeepSearchQA attribution (false positive)

- `WHY-SITES.md` §3a — old: "`morris-satellite-deferred-letters.trycloudflare.com/apps/who-visits/?i=316697` matched dsqa_043/079/497." New: explicit retraction — the WHO acronym collided case-insensitively with "who-visits"; deep-trace shows a Facebook credential-phish kit (Cloudflare 403 since Sep 26). Crimeware, not agent infrastructure; fingerprint claim withdrawn.
- `workers/corpus-grepper/FINDINGS.md` §7 — section retitled "… — DSQA 'fingerprint' REFUTED"; original claim quoted verbatim at the end; added the word-boundary/minimum-token recommendation.
- `workers/corpus-grepper/FINDINGS.md` INFERENCE #1 — appended qualification note: trycloudflare.com's only DSQA-fingerprint hit was the FP.

## Correction 2 — REFRAME Pipedream /ssh_ as observer-side (not operator beaconing)

- `WHY-SITES.md` §3b — old: "check-in/beacon dead-drop shape." New: 7 urlscan-API submissions in three bursts + 2 urlhaus auto-submissions = watcher behavior; endpoint answered HTTP 400. Downgraded to watchlist-grade; "beacon" language removed.
- `workers/index-hunter/FINDINGS.md` §7 OBSERVED bullet — reworded "repeated probes/check-ins against that path" → repeated submission of the URL to urlscan (observer-side), HTTP 400 noted.
- `workers/index-hunter/FINDINGS.md` §7 VERDICT — replaced "DEAD-DROP PATTERN OF INTEREST (not proof)" + "shape of a check-in/beacon dead drop" with "DEAD-DROP LEAD, ELEVATED — watchlist-grade, not evidence-grade", full 7+2 breakdown, HTTP 400 = validating dead drop, open questions listed.
- `workers/index-hunter/FINDINGS.md` conclusion #3 + follow-up bullet — "check-in/beacon" language replaced with observer-side framing; summary table grade updated to "DEAD-DROP LEAD, WATCHLIST-GRADE (observer-side, reframed 2026-10-05)".

## Correction 3 — MARK oai- ngrok tunnel as investigator/demo artifact

- `WHY-SITES.md` §3a — old: "`oai-`-prefixed tunnel … — agent-shaped naming." New: joshuadavid's wikiagentswarminvestigation demo-scratchpad (OpenAI web.run cache-versioning demo), cloned 2026-10-05; `oai-` is investigator naming; only such hostname in all corpora; retained as reference artifact, not a campaign lead.
- `workers/corpus-grepper/FINDINGS.md` §8 — section retitled "… — INVESTIGATOR ARTIFACT"; added provenance (demo messageboard mechanics, `oai-*` handling rule); original observation quoted verbatim at the end.
- `workers/corpus-grepper/FINDINGS.md` INFERENCE #1 — appended qualification note: ngrok.io's `oai-` hit is an investigator artifact; remaining ngrok hits (ngrok-free endpoint, tracker/tunnels.md) still stand.

## Correction 4 — CORRECT Discord webhook section (six records, not three; not benchmark output)

- `WHY-SITES.md` §3a — old: "three `discord.com/api/webhooks/<id>/<token>` URLs tied to urlquery reports 2026-04 through 2026-09." New: six records; `phase1_results.json` is the evaluator's scoredrop-lane URL inventory (12 keys = urlquery htmx search terms), not benchmark output; five bare-URL read probes (A–D, F; record A GET → 404); one crimeware-shaped (E: `43.226.1.26:5000/get_sound…`, sinkholed OVH IP, truncated 14-char token); no eval-run connection; tokens never validated or used.
- `workers/corpus-grepper/FINDINGS.md` §4 — rewritten with the full six-record table (complete id/token values, dates), the five-probe/one-crimeware breakdown, and the not-benchmark-output framing.
- `workers/corpus-grepper/FINDINGS.md` summary table row 39 — annotated: "7 lines; **6 full id/token records** per 2026-10-05 deep-dive."

## Files intentionally NOT touched

- `linkhunt-deep/LINKHUNT-DEEP.md` and its `workers/*/FINDINGS.md` — these are the corrections source; they already contain the corrected claims.
- `raw/known-url-hunt.md`, `EGRESS_MAP.md` — their `discord.com/api/webhooks` mentions concern skill-scan runtime-notifier findings, not the evaluator corpus; no correction applies.
- `workers/historian/FINDINGS.md` — no claims matching the four corrections found (verified by grep).
