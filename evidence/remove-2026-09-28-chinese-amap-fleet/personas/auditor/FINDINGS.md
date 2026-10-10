# THE AUDITOR — FINDINGS

**Persona:** hunt DETECTION and VERIFICATION workloads — actors who *audit* sites (checking redirector farms, re-scanning landing pages, using archives as oracles, running canary monitors) rather than attacking them. Agents and swarms only; no operator identity work. No commits/pushes.

**Run:** 2026-10-05 ~04:25–05:25 UTC (resumed after VM restart ~05:08 UTC; VM-wide HTTPS egress was down 04:24→~05:12 UTC, recovered mid-run).

**Prior lanes (raw/):** `baseline.md`, `lane-a-watchphrases.md`, `lane-b-watchers.md`, `lane-d-oracles.md`. This report resumes and closes them.

---

## 1. The jmail.world auditor — STILL RUNNING, reference auditor (confirmed programmatic)

Baseline from lane A/B: 2026-10-04 23:54 → 04:13 UTC, metronomic ~3-min cadence, walking jmail.world threads/drives/persons and probing the site's search with spam/affiliate-kit URLs (`followlike.net/?r=19384926`, `livetraffic.net/login?refer=119334`, `2pink.org/dang-ky?ref=119334`, `folllike.com/?19384926`) and the canary phrase `seekers+of+decay`. Total ≥872 reports by 04:13 UTC.

**New (live, 2026-10-05 ~05:18–05:20 UTC):** latest submissions on the live index are **minutes old** — the loop is running *right now* (observed tops: 05:18, 05:15, 05:12, 05:10 UTC). Same grammar: `/thread/EFTA<N>`, `/thread/vol<N>-efta<N>-pdf`, `/person/<name>`, `/page/<n>`, `/drive/<vol>`, `/photos`, mutating `?q=` payloads, watch-phrase `seekers+of+decay` still in rotation. Newest payload variants: `?q=http://folllike.com/?19384926` (affiliate ID in path), `?q=https://2pink.org/dang-ky?ref=119334`.

**Assessment:** sustained search-index-poisoning / search-spam audit of a 450M-visit Epstein-files archive. Watch-phrase = index canary ("does the search echo a known-unique benign string?"). Programmatic, certain — timer-fired loop, no multi-day evidence yet (first sighting Oct 2 15:13 UTC; unclear if it pauses by day).

## 2. paralino.app — escalation-then-stop watcher loop (newly characterized)

Live full-history pull (limit 24, 2026-10-05 ~05:21 UTC), bare host `paralino.app` re-submitted identically:

```
2026-10-04 23:07, 23:27, 23:58, 2026-10-05 00:15, 00:46, 01:39, 02:11,
02:19, 02:20, 02:22, 02:25, 02:37, 03:08, 03:09, 03:14, 03:19, 03:20,
03:25, 03:31, 03:39, 03:58
```

Two phases: sparse surveillance (~20–40 min gaps, 23:07→02:37) then a ~5-min cadence burst (03:08→03:58). **No reports after 03:58** — the loop stopped ~90 min before this writeup. Identical bare-URL re-scan is the detection-check pattern: re-submit to see if the sandbox verdict changed (compromise check / WAF change / content drift).

**Identity:** Paralino — end-to-end-encrypted location-sharing app (open-source apps, EU-hosted, Life360 competitor; subscription tiers $4.99–$11.99/mo). https://paralino.app/

## 3. www.get-monai.app — live metronomic watch loop, ONGOING (paired with #2)

Live full-history pull (~05:23 UTC), bare host `www.get-monai.app`:

```
2026-10-05 03:09, 03:13, 03:17, 03:19, 03:20, 03:24, 03:36, 03:43, 03:49,
03:52, 03:52, 03:54, 04:04, 04:09, 04:13, 04:30, 04:33, 04:38, 04:50,
04:56, 05:10, 05:11, 05:16, 05:16
```

**24 submissions over 2h07m, median gap ~4–5 min, latest 05:16 UTC — still running.** Bare host, repeated identically. No history before 03:09 (starts cold).

**Identity:** MonAi — AI expense-tracker app landing page (App Store + Google Play, 8,500+ reviews, Apple Pay automation / OCR / voice). https://get-monai.app/

**Pairing assessment:** both `.app` TLD, both consumer mobile-app landing pages, both bare-host, both started within the same minute (03:09/03:19) of Oct 5 — one actor working a target list of app landing pages on a short re-scan loop. This is a detection-validation workload (checking landing pages for compromise/injection/redirect changes), not manual triage (triage doesn't re-submit an identical bare URL 24× at 4-min spacing). paralino's two-phase shape (sparse then burst) vs get-monai's cold-start metronomic loop suggests the operator added get-monai to the watch list and tightened cadence at 03:09.

## 4. Lane A closed: watch-phrase findings stand

- `seekers+of+decay`: Google-SERP canary monitor, 113 reports 2026-06-29 → 2026-09-25 (separate scheduled-monitor actor, ~5h median gap — different rhythm from the jmail loop).
- Frozen-corpus sweep: watch-phrase-shaped strings only the seekers phrase (15) and jmail kit payloads (36); affiliate IDs/brands appear nowhere else in the corpus. Honest negative.
- Lane A runner (`~/workspace/lane-a-scratch/run.sh`) still armed — it will self-execute when egress is detected; parent may collect `parsed/*.json` for deeper history.

## 5. Lane D closed: fragment-indexing anomaly RESOLVED as outage artifact

Lane D's anomaly was: 11 htmx archive-term queries returned 0 reports even though ≥103 `cachedview.nl/#https://jmail.world/...` reports are demonstrably in the index — hypothesized fragment-stripping in the search index.

**Live test (2026-10-05 ~05:24 UTC):** `q=cachedview.nl` returns the wrapped reports directly (`cachedview.nl/#https://jmail.world/drive/vol00011-efta02518043-pdf?q=...`, `/person/ghislaine-maxwell?q=...`, etc.). **Fragments ARE indexed and searchable.** The 04:28–04:40 zero sweep ran inside the egress outage window (proxy-CONNECT timeouts everywhere); the endpoint was degrading, not the index. The `q=19384926` sweep also returns the jmail `?q=` payload reports normally.

**Implication:** "no other archive-proxy actors" in lane D was correctly flagged as *unproven*, not ruled out — but the index coverage itself is fine; the sweep can simply be re-run.

## 6. Tradecraft summary — detection workloads observed

| Workload | Actor shape | Example |
|---|---|---|
| Search-index poisoning audit (kit URLs + canary phrase) | metronomic timer loop, 3 min, live right now | jmail.world auditor |
| Landing-page compromise re-scan (identical bare-URL resubmits) | watch loop, 4–5 min, live right now | get-monai.app |
| Landing-page re-scan, escalation-then-stop | sparse → 5-min burst → stopped 03:58 UTC | paralino.app |
| SERP index canary monitor (scheduled, bursty) | ~5h median, 3 months | Google `seekers+of+decay` probes |
| Live-vs-cached cross-check (intended; void in execution) | interleaved oracle step in jmail loop | `cachedview.nl/#<target>` submissions |
| SEO indexation verification (working oracle) | months-long intermittent batches | SEO indexation swarm (cachedview.nl contacted host) |

**Key discriminator for auditor workloads:** URL mutation/rotation + payload canaries + metronomic timing = detection validation; identical-URL repeat at fixed interval on a bare host = change-detection re-scan; both are *verifying* rather than *attacking*.

## Honest negatives

- No second actor probing with the jmail affiliate IDs / brands / watch-phrase beyond the two described contexts (jmail loop + Google SERP monitor).
- No `?q=`/`?s=`/`?query=` detection probes in the frozen oai-tag-sweep corpus outside jmail payloads.
- No archive-proxy actors beyond jmail (wrapped mode) and the SEO swarm (embedded mode) — sweep should be re-run live now that the index works.

## Pending / follow-ups for parent

1. Lane A runner outputs (`~/workspace/lane-a-scratch/parsed/`) — deeper jmail history (pre-Oct 2), `refer=` param sweep.
2. Re-run lane D's 11 archive-term queries live (index confirmed working).
3. Day-over-day sweep for `url.domain:paralino.app` / `get-monai.app` — was the loop running on earlier dates too?
4. urlscan.io coverage of `cachedview.nl`-wrapped submitted URLs (30-day window).
5. What were the actor's other target-list entries? The paired `.app` loops imply a list; more bare-host metronomic loops in the recent window would fill it out.

---

## APPENDIX — All observed URLs

### jmail.world auditor (latest live submissions, 2026-10-05 05:10–05:18 UTC)
- https://urlquery.net/report/5632b5be-2b50-4aae-a2be-c5984d4a6389
- https://urlquery.net/report/8dd8c2d1-97c7-482d-8e4b-ef3b81098a7a
- https://urlquery.net/report/e36e6d36-db70-4faa-886f-f6593b58d7aa
- https://urlquery.net/report/831bd1cd-f57d-4a30-9710-24d2d21267ca
- https://urlquery.net/report/1022957a-00b5-44a1-b1d4-f433b6948033
- jmail.world/thread/vol00009-efta01013950-pdf?q=http%3A%2F%2Ffolllike.com%2F%3F19384926
- jmail.world/thread/EFTA01934129?q=http%3A%2F%2Ffolllike.com%2F%3F19384926
- jmail.world/thread/EFTA02534854?q=https%3A%2F%2F2pink.org%2Fdang-ky%3Fref%3D119334
- jmail.world/thread/EFTA02032048?q=seekers+of+decay
- jmail.world/thread/vol00009-efta00160217-pdf?q=https%3A%2F%2Fwww.followlike.net%2F%3Fr%3D19384926
- jmail.world/photos?q=http%3A%2F%2Ffolllike.com%2F%3F19384926
- jmail.world/person/talulah-riley?q=https%3A%2F%2Fwww.followlike.info%2F%3Fr%3D19384926
- jmail.world/person/david-stern?q=seekers+of+decay
- jmail.world/person/darren-indyke-nameonly?q=seekers+of+decay
- jmail.world/page/54?q=http%3A%2F%2Ffolllike.com%2F%3F19384926
- jmail.world/drive/vol00011-efta02655311-pdf?q=https%3A%2F%2Flivetraffic.net%2Flogin%3Frefer%3D119334
- jmail.world/drive/vol00011-efta02220292-pdf?q=https%3A%2F%2F2pink.org%2Fdang-ky%3Fref%3D119334
- jmail.world/person?page=116&q=https://www.followlike.net/?r=19384926
- jmail.world/person?page=126&q=https://www.followlike.net/?r=19384926

### cachedview.nl-wrapped jmail reports (live)
- cachedview.nl/#https://jmail.world/drive/vol00011-efta02518043-pdf?q=https%3A%2F%2F2pink.org%2Fdang-ky%3Fref%3D119334
- cachedview.nl/#https://jmail.world/drive/vol00011-efta02662720-pdf?q=https%3A%2F%2Flivetraffic.net%2Flogin%3Frefer%3D119334
- cachedview.nl/#https://jmail.world/person/a-de-rothschild?q=https%3A%2F%2Fwww.followlike.net%2F%3Fr%3D19384926
- cachedview.nl/#https://jmail.world/person/ghislaine-maxwell?q=https%3A%2F%2Fwww.followlike.net%2F%3Fr%3D19384926
- cachedview.nl/#https://jmail.world/person/jay-jideliov?q=https%3A%2F%2Fwww.followlike.info%2F%3Fr%3D19384926

### New watcher targets (identities verified via live fetch)
- https://paralino.app/ — Paralino, E2E-encrypted location-sharing app, open-source, EU-hosted, Life360 competitor ($4.99–$11.99/mo tiers)
- https://get-monai.app/ — MonAi, AI expense-tracker app landing page (App Store + Google Play, 8,500+ reviews)
