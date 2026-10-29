# Hunt Lane 20 — Diffend sweep of 1,284 advisory-named campaign gems

Date: 2026-09-27/28. Read-only, ~1 req/s, no auth. Script: `scripts/diffend_sweep.py`.
Target list: `data/osv/ghsa_gemstuffer_classified.json`, field `gs_not_in_corpus` (1,284 advisory-backed GemStuffer names absent from the local corpus).
Raw results: `data/osv/diffend_sweep_results.jsonl` (1,284 rows, all unique names).

## TL;DR

- **394 of 1,284 advisory names are in Diffend** (versions page parsed, publish timestamps recovered).
- **218 are confirmed absent** from Diffend (HTTP 200, no version records).
- **672 are unconfirmed** — Diffend closed the connection before serving the gem page ("Remote end closed connection without response"). These are fetch failures, not evidence of absence. They need a retry pass.
- All 394 recovered gems publish **May 11 19:40 → May 12 07:47, 2026** — the May campaign segment only. Zero July-wave markers among the recovered set.

## Data-quality caveat (read first)

Diffend was hostile tonight. Two failure modes degrade the numbers above:

1. **Phase-1 fetch failures (672 names):** connection closed without response on the gem page. Miss vs absent is undecided for these.
2. **Phase-2 fetch failures (~291 of the 394 found):** the version-diff page died mid-read (IncompleteRead / connection closed), so `mechanism_notes` is empty for 291 found gems — not because the payloads are clean, but because the scan never ran. Only 4 found gems are clean no-marker scans; 71 carry the `empty-summary` canary marker.

Net: the 394/218 split is solid. Mechanism coverage is ~26% of found gems (103 of 394 with at least one marker). The VCS-value extraction also mostly failed (see below).

## Mechanism classification (pattern-based, 394 found gems)

| Pattern | Hits | Notes |
|---|---|---|
| go-import tag | 91 | All May 12. VCS value extracted for only 1 (`hg`); 90 `unknown` — the extraction regex did not match Diffend's page rendering, tooling gap, not a data negative |
| jina-laundered (`r.jina.ai` / `s.jina.ai`) | 34 | Overlaps the go-import set (e.g. `gtest1778553427` ×5, `pdfkent1`, `pdflahueca1`, `pdfmeno1`, `pdfpalais1`, `pdftoilet1`) |
| webhook dead-drop (`web_hooks`/`A000`/`ZZEND`/`southpxdatapp`) | 1 | `slvhg151` — only one in the recovered set; consistent with the dead-drop being a small May sub-family |
| empty-summary (`summary: x`) | 71 | The `x=1` canary / empty-carrier family; includes `oakmi15000`–`oakmi15700` series |
| XSS exfil (`oast.online`, `webhook.site`, `<script`, `onerror=`) | 0 | — |
| SSTI probe (`${7*7}`, `{{7*7}}`) | 0 | — |
| county-json | 0 | June-18 mechanism absent from this slice, as expected |
| no markers (clean scan) | 4 | Only 4 found gems scanned clean end-to-end |

Sample go-import names: `gtest1778553427`, `gtest1778553433`, `gtest1778553438`, `gtest1778553445`, `gtest1778553451`, `oakmi15000`–`oakmi15600` series.

## Name-grammar breakdown

Found in Diffend (394):
- `epoch_suffix` (10+ digit trailing): 25 — e.g. `foofoofooproxyxyz1778553602`, `gemxy-1778522681`, `gtest1778553427` ×5, `waitwhg1778555688`, `wandsmod1778555488`
- `proxy_name`: 32 — e.g. `proxymeta646418`–`proxymeta646478` series, `proxyt0dd1ee25`, `proxyfooabc53ee9f5f`
- `yard_name`: 1
- `try_zz`, `zz_prefix`, `oai_prefix`, `goimport_name`, `fetch_name`, `probe_name`: 0

Confirmed absent from Diffend (218):
- `oai_prefix`: **138** — the oai-prefixed advisory names are disproportionately confirmed-missing from Diffend
- `epoch_suffix`: 18, `fetch_name`: 8, `proxy_name`: 5, `goimport_name`: 2, `probe_name`: 1

Unconfirmed / fetch-failed (672):
- `epoch_suffix`: 30, `proxy_name`: 10, `fetch_name`: 3, `zz_prefix`: 3, `yard_name`: 2 — the retry pass should prioritize these plus any oai-prefixed names in the failure set

## Campaign-segment attribution

All 394 recovered gems are **May segment**: first-publish timestamps run May 11 19:40 → May 12 07:47 UTC, matching the known May burst window (rehearsal May 11, 516-gem burst May 12). Burst peaks inside the recovered set: 31 at 03:13, 23 at 02:38, 19 at 03:19 (May 12). Two gems carry 2 versions (`gemxpush21778549590`, `gemxy-1778522681`); the rest are single 0.0.1 publishes.

No June-18 or July-7 markers appear in the recovered set — consistent with the target list being advisory-named May packages (the July XSS/SSTI wave has no advisories among checked names).

## What this adds

394 advisory-backed campaign gems now have confirmed Diffend presence + publish timestamps, all previously absent from the local corpus. They are candidates for the archive pipeline (per-gem Diffend reconstruction) to grow the corpus beyond its current 616 archives.

## Recommended follow-ups

1. **Retry pass for the 672 phase-1 failures** (and re-scan of the 291 found gems with phase-2 failures), ideally with backoff and off-peak timing — Diffend was rate-limiting/connection-dropping tonight.
2. Fix the VCS-value extraction regex against a live Diffend diff page — 90/91 go-import hits are `vcs=unknown`.
3. Feed the 394 confirmed names into the gem archive pipeline for `.gem` reconstruction.
