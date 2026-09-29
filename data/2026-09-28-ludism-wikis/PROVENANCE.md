# PROVENANCE — Lane A: ludism.org + ApchemWiki capture

**Lane**: A (ludism.org + ApchemWiki)
**Date**: 2026-09-27 (UTC; sweep launched ~03:22 UTC)
**Task**: read-only recon via public reader proxies only; no bypass, no auth,
no submissions. Agents/infrastructure traces only — no operator identity,
registrant details, or person-focused attribution.

## What was attempted

Public reader proxies at gentle pacing (~1 request/5s):
- `https://r.jina.ai/<target-url>`
- `https://api.allorigins.win/raw?url=<encoded-target>`
- `https://api.allorigins.win/get?url=<encoded-target>`

Targets (9):
- `ludism.org` root (http + https)
- ludism Oddmuse wikis' RecentChanges: `/scwiki/`, `/mentat/`, `/gbgwiki/`,
  `/ppwiki/`, `/gamedesign/` (paths taken from thecolony.ai swarm catalogue
  Surface #10 — ludism.org is five Oddmuse wikis, not one)
- `tmcleod.org/cgi-bin/apchem/wiki.cgi` root + `?action=rc` (UseModWiki;
  path taken from thecolony.ai incident wiki §14)

Script: `scripts/ludism_proxy_fetch.py` (run log below). Per-target result
records in `raw/<target>__<proxy>.txt.meta.json`; `raw/sweep-summary.json`
holds all outcomes.

## Proxy outcome (final: 27 fetches + 2 controls, 2026-09-27 ~22:22–22:35 CDT)

**2/27 target fetches returned content; 25/27 failed.**

- **r.jina.ai (control-verified working on example.com — HTTP 200):**
  - All 7 ludism.org targets (root http/https + 5 Oddmuse `?RecentChanges`):
    FAILED — origin unfetchable (HTTP 422 / RemoteDisconnected). Corroborates
    Lane I's direct finding that ludism.org is unreachable.
  - `tmcleod.org/cgi-bin/apchem/wiki.cgi` (root + `?action=rc`): **OK, HTTP 200,
    308/318-byte 404 bodies** — the origin server answers but the apchem wiki
    path is GONE (matches Lane I's "404 on RecentChanges forms"). Independently
    confirms from a second network vantage that the last-write surface is offline.
- **api.allorigins.win: all 18 fetches failed — but the example.com control
  also failed (HTTP 522), so allorigins results are INCONCLUSIVE** (proxy-side
  failure, not target evidence). Documented as such; jina carries the verdict.

No bypass attempts were made. The only independently verified facts this lane
adds: (a) ludism.org is unfetchable from two vantage points (direct + jina);
(b) tmcleod.org serves 404 on the apchem wiki.cgi path.

## What landed

| # | File | Content | SHA-256 (short) | Verification |
|---|------|---------|-----------------|--------------|
| 1 | `thecolony-claims-ludism.md` | Incident-wiki §13 + swarm-catalogue Surface #10, quoted verbatim | see manifest | `not_independently_verified`, origin=`thecolony-wiki` |
| 2 | `thecolony-claims-apchemwiki.md` | Incident-wiki §14 + catalogue §2 + cross-host-tie excerpt, verbatim | see manifest | `not_independently_verified`, origin=`thecolony-wiki` |
| 3 | `raw/*` (+ `.meta.json`) | Verbatim proxy fetch outcomes (body or failure record) | see manifest | direct fetch evidence |

`manifest.jsonl` carries per-file SHA-256, byte counts, source URLs, and
retrieval timestamps for every file in this directory.

## Sources

- thecolony.ai incident wiki `/wiki/openai-escapee-agent-incident-2026` (§13 ludism,
  §14 ApchemWiki) and `/wiki/escaped-agent-swarms` (Surface #10, §2, cross-host tie)
  — captured by Lane I (thecolony-ai, 2026-09-27/28) into
  `data/thecolony-ai/wiki_incident_page.html` / `wiki_catalogue_page.html`.
- Direct hosts: `ludism.org` (Oddmuse wikis), `tmcleod.org` (UseModWiki ApchemWiki)
  — attempted only via public reader proxies.

## Standing caveats (from Lane I)

- Investigator posts/claims are third-party analysis; quoted as reported.
- The ludism cross-IP bridge (20.45.46.41, 172.184.176.194) rests on one
  investigator's server-log access; the incident wiki itself marks the exact
  IPs "NOT independently confirmable" (Oddmuse hides editor IPs).
- ApchemWiki IPs are /24-truncated by the wiki itself; exact-IP identity is open.

## Raw layer 2026-09-29

- `data/ludism-wikis/manifest.jsonl` -> `data/ludism-wikis/raw/manifest.jsonl` (crawl manifest consumed by scripts/es_ingest_ludism.py)

## Schema normalization 2026-09-29 (worker W7)

- Built `events.jsonl`: 29 records, one per proxy-fetch sidecar
  `raw/<target>__<via>.txt.meta.json` (27 wiki-target fetches + 2 proxy controls);
  each `.txt` body, where present, is paired into its record (top-level
  `sha256` / `size_bytes`). Builder: `temp/build_events_w7.py`.
- record_kind: `venue_probe` (existing registry kind; no new kinds introduced).
- Fingerprint identity string: `ludism-probe:<target>|<via>` (sha256 hex).
- `@timestamp`: sidecar `fetched_at` normalized to Z
  (`labels.timestamp_source = "labels:probe.fetched_at"`).
- `confidence`: `high` for jina fetches (proxy control-verified working),
  `low` for allorigins fetches (its example.com control also failed, so those
  results are inconclusive per the lane verdict above).
- Proxy controls marked `labels.proxy_control = true`.
- Supporting files (`manifest.jsonl`, `pattern-sweep.json`, `sweep-summary.json`,
  `thecolony-claims-*.md`) are not event records; they stay in `raw/` and are
  checksummed in `SHA256SUMS`.
- `SHA256SUMS` regenerated (sha256sum-style): `events.jsonl` + all `raw/` contents,
  verified with `sha256sum -c`.

## Rollup 2026-09-29 (W8)

Built `rollup.jsonl`: 9 rows x `target_probe_rollup` — per-target verdicts
aggregating the (target, proxy) probe matrix: 2/9 targets reachable
(apchem_rc, apchem_root — both via jina only), 7 unreachable on all proxies.
The 2 `proxy_control (example.com)` probes are controls, excluded from the
rollup. `@timestamp` = earliest `probe.fetched_at` per target.
Fingerprint identity string `ludism-probe-rollup:<target>`. Builder:
`temp/build_rollup_w8.py` (repo root passed as argv[1]); totals independently
recomputed (27 probes, 2 successes). `scripts/validate_schema.py`: 0
violations. SHA256SUMS regenerated (40 entries, incl. rollup.jsonl);
`sha256sum -c` OK.
