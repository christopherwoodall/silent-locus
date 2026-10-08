# Temporal pivot: GemStuffer markers outside May 5 – July 7

Date: 2026-09-28
Question: do the RubyGems go-import campaign markers appear in other time frames
(before May 5, in the inter-wave gaps, after July 7)?
Baseline: JFrog inventory `data/gemstuffer-jfrog-2026-09-27.csv` (3,022 pkgs;
waves May 5/8/9/10/11/12/26/27, June 18, July 7).

## Verdict: CLEAN NEGATIVE (one sub-lane inconclusive, noted below)

No marker-bearing activity found outside 2026-05-05..2026-07-07 in any workable lane.
The campaign's published temporal bounds hold.

## Coverage

1. **Internal corpus temporal scan** — `data/gem-ioc-log.jsonl` (1,262 records) and
   `data/gem-graph-nodes.jsonl` (2,830 records): 1,743 marker-bearing records, every one
   with a genuine publish date inside the window. 27 apparent out-of-window hits were
   `extraction`-kind records whose date was the 2026-09-27 IOC-extraction run, not
   campaign activity. Clean.
2. **RubyGems live search API** (read-only, 2026-09-28): `go-import` → only legitimate
   LIME Go tooling gems; `southwark`, `wandsworth`, `zzjina` → empty; `web_hooks` →
   only legitimate GitHub-webhook gems. No live campaign-marker gems. Clean.
3. **Web search** (4 queries): `"southpxdatapp6pi" OR "zzjinavcs"` → unrelated noise;
   `"xss-test-gem" OR "test-ssti-0"` → only the JFrog report itself;
   `"ZZEND" webhook dead drop` → noise (coupon codes, TikTok URL fragments).
   No second venue mentions the distinctive names. Clean.
4. **urlquery date-scoped** (authenticated, read-only): `mgCalendarWeekView`
   `date:[2026-01-01 TO 2026-05-04]` → 0 hits; `democracy.wandsworth.gov.uk`
   (all-time) → 2 hits, both unrelated sites (`civaccount.co.uk` 2026-07-17,
   `emergenzaclimatica.it` 2025-10-30), no campaign linkage. Clean.
5. **Diffend version-date sweep — INCONCLUSIVE (endpoint, not evidence).**
   A 3,025-name sweep (`scripts/diffend_temporal_sweep.py`) was abandoned: my.diffend.io
   closes connections on burst traffic from this environment (16/24 probe requests failed;
   targeted retry checker likewise). Spot checks that did render:
   `southpxdatapp6pi` = single version 0.0.1, May 12, 2026 (in-window);
   `xss-test-gem`, `sarif` = "no computed diffs". Partial artifacts kept in
   `data/gem-temporal-pivot/` for resume if the endpoint recovers.
6. **GHSA classification** (`data/osv/ghsa_gemstuffer_classified.json`): no date fields
   present. One GemStuffer-shaped name absent from JFrog's inventory — `sarif` —
   but it is yanked (RubyGems 404), has no Diffend snapshot, and its markers were never
   observed: near-miss, not a hit per the verification bar.

## Corroborating context (not new findings)

- JFrog's inventory, built from RubyGems publish data, enumerates waves only inside the
  window; the orca-ai-incident-archive independently dates the first oai packages to May 5.
- Press (webpronews, via `notes/gem-jfrog-report-2026-09-27.md`) reports RubyGems halted
  registrations after the campaign — a structural barrier to same-venue continuation.

## Near-misses (kept out of the hit list)

- `sarif`: GHSA GemStuffer-shaped, missing from JFrog, yanked, no snapshot — undatable.
- urlquery's 2 `democracy.wandsworth.gov.uk` hits: unrelated sites, no marker linkage.

## Resume pointers

- `scripts/diffend_temporal_sweep.py` + `data/gem-temporal-pivot/diffend_temporal_sweep.jsonl`
  (24 rows, checkpointed by name) — rerun if Diffend becomes cooperative; ~1 req/s with
  generous backoff advised.
- If a future lane finds an out-of-window name, the verification bar is: package name +
  date + exact marker text observed + source URL, cached to disk with retrieval time and
  SHA-256 before claiming.
