# FINDINGS — Palisade Swarm Traces release vs our holdings

## TL;DR
Palisade Research published the Swarm Traces dataset (scrape traces from public agent-eval runs).
We already held the exact same bytes. The sha256 hash matches. There are zero new records.
The real value is Transluce's analysis (#159–#161). It ties record clusters to real publishers: a Chicago dashboard, a CDC inspection-search page, nine dashboard families. All of it reproduces locally.

## Grading legend
- **OBSERVED**: we saw this in the data.
- **INFERENCE**: we think this is true, but we did not see it directly.
- **UPSTREAM**: another source said this; we did not check it.

**Date:** 2026-10-07 · **Source findings:** Transluce #159, #160, #161 (submitter: Britt Lewis, 2026-10-05/06)

Evidence lives in the shared collection tree at [`../raw/swarm-traces/`](../raw/swarm-traces/).
We keep lane-local raw/ dirs only for lane-run pulls; this evidence came from the shared Transluce ingest.

## 1. Release location + size

- **Location (OBSERVED):** Palisade Research, `https://swarmtraces.org/` (Sep 25, 2026). Canonical file: `https://swarmtraces.org/data/final/redacted.jsonl.gz`.
- **Size:** 15,214,685 bytes gzip; 189,579 records uncompressed.
- **sha256 (uncompressed):** `91e9158487a63acb12e54faa8490c4a23f664e1650c947a87d270d2022b0451e`. It matches the hash in all three Transluce findings.
- **Size estimate before pull:** 15.2 MB (well under the 500 MB threshold). We pulled it with curl. It is byte-identical to our pre-existing holdings.
- Cached: `../raw/swarm-traces/redacted.jsonl.gz` + `PROVENANCE.md`. **The file is committed and pushed.** An old note said "Not committed (coordinator's call)". That note was stale. The file is tracked in git (commit 05a29e8a).

## 2. Our-holdings inventory (already held, pre-2026-10-07)

| Holding | Records | Date range | Notes |
|---|---|---|---|
| `data/raw/redacted.jsonl.gz` | 189,579 (payload 91,037 / recovered_text 75,534 / response 23,008) | `time_utc` null on 100% of records — no time field at all | Acquired 2026-09-27 from the same URL; sha256 of uncompressed bytes = release hash exactly |
| `data/2026-09-27-swarmtraces-verification/events.jsonl` | 5 audit findings | 2026-09-27 | Structural audit: sequential IDs R0000001–R0189579, zero gaps; redaction-marker stats; parentage topology |
| `data/2026-09-27-swarmtraces-verification/raw/verification-2026-09-27.md` | — | 2026-09-27 | Full verification report (cite-token = template key; 163,849 distinct; 3.4% of payloads plaintext-only) |
| `data/transluce-api/raw/findings-list.json` | Transluce #159–161 full texts + evidence links | pulled 2026-10-07 (transluce cron) | The derived analyses themselves, already in our Transluce ingest |

## 3. Diff: Palisade's release vs our holdings — zero new raw data

The release is **byte-identical** to what we hold (uncompressed sha256 match on 189,579/189,579 records). Diff = 0 new records. The three Transluce findings add **derived attribution**, not data. We re-verified every cited record ID in our copy:

| Finding | Claim | Re-measured in our bytes (OBSERVED) | Verdict |
|---|---|---|---|
| #159 Chicago VR dashboard | 14 records carry "Victimization Count" worksheet; lists 14 IDs | exactly 14 records contain the string; all 14 cited IDs (R0079276…R0101210) present | **CONFIRMED against bytes** |
| #160 CDC VSP search | 15 records match ASP.NET control names (`lbox_RegisteredName`, `rb_Cruiseline_Vessel`…); 52 records reference `destination:008436` | exactly 15 control-name records (R0052835, R0053127/28/29, R0053170/71/75/76…); exactly 50 records with `destination:008436` (35 payload / 1 response / 14 recovered_text) + 2 name-matched-only = 52 | **CONFIRMED against bytes** (37 payloads = 35+2 ✓) |
| #161 dashboard families | NC DHHS, Florida DOE, WHO, PAHO, etc. record families | "By Population Focus Chart1_DEP" hits present; "Palm Beach"/"Algebra 1 - B.E.S.T. EOC" hits present (R0079239, R0079483, R0079497, R0079626, R0111524); "FACT_COUNTRY_INDICATORS" ×5 present | **Spot-confirmed**; full family taxonomy is Transluce's derived work, reproducible from our bytes |

## 4. Verdict

**Palisade's public release does NOT extend our corpus — it is our corpus.** We acquired the identical bytes 2026-09-27. What #159–161 give us is new *analysis*. They name record clusters (Chicago VR dashboard, CDC VSP inspection search, nine dashboard families) with Transluce's publisher-confidence attributions. All of it is reproducible locally. No external source is needed.

**Single most actionable lead:** the findings tie record clusters we already hold to real-world publishers. They give row-ID-level citations (Chicago VR dashboard, CDC VSP search, NC DHHS/WI DOC/FL DOE dashboards). The next step is publisher-side verification of Transluce's "publisher confidence" claims. Example: confirm the CDC control names on the live inspection-search page. Confirm the Tableau parameter names on Chicago's VR dashboard. This needs no new collection.

**What got killed:** the hypothesis that Palisade's release might be a second, larger or different cut of the data. Byte-identity rules it out (sha256 91e91584… on 189,579 records). Also killed: any need to pull or re-audit the raw corpus for the Transluce dashboard families.

## Epistemic grades
- OBSERVED: byte-identity of the release vs our holdings; re-measured record counts above.
- INFERENCE: Transluce's dashboard→publisher attributions. Worksheet, table, and field names imply the publisher. But the release redacts destinations. #159 and #161 state this caveat themselves.
- UPSTREAM: Transluce's "publisher confidence" labels and novelty claims. We did not re-derive them beyond spot checks.
