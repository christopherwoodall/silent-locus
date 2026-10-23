# CDX Sweep — May–Jul 2026 Retrospective (Step 2 of super-search)

Date of run: 2026-10-23. Window: 20260501–20260731. Method: one CDX range
query per target via `http://web.archive.org:80/cdx/search/cdx`
(UA silent-locus-lane-scanner/1.0), fl=timestamp,original,statuscode,
mimetype,digest, limit=20000. Flake policy: 45–90 s retry spacing,
max 3 attempts per query.

## Targets and results

| Target | Type | Rows | Unique digests | Verdict |
|---|---|---|---|---|
| r.jina.ai | domain | 3238 | 2681 | noise — public jina-reader laundering; Jul 29–30 burst is Cloudflare challenge-platform crawler noise |
| api.allorigins.win | domain | 2323 | 424 | noise — 1717 proxy invocations hit dev-test hosts (postman-echo.com 559, www.boubinarena.cz 118, pump.fun 40) |
| pastebin.com | domain | 0 | 0 | FAILED — Wayback backend 503 on all 6 attempts across two runs; NOT a zero; needs re-run |
| webhook.site/28efa24e-…-5035031 | exact | 0 | 0 | real zero (expected — inbox created 2026-10-14, after window) |
| ntfy.sh/c6836 | prefix | 0 | 0 | real zero |
| ntfy.sh/kz1wu398dnq | prefix | 1 | 1 | NEW-candidate — 200 @ 2026-07-06 04:44:26 UTC; body: `START "tomas kopecky" "six million dollar man"` |
| ntfy.sh/mha3x | prefix | 0 | 0 | real zero |
| ntfy.sh/o54445 | prefix | 1 | 1 | NEW-candidate — 200 @ 2026-07-08 15:07:11 UTC; body: single-char beacon `S` |
| ntfy.sh/pz4kopsh1 | prefix | 1 | 1 | NEW-candidate — 200 @ 2026-07-06 03:51:14 UTC; body: timestamp beacon `go\|1783309874200` |
| jqp.vercel.app/api/ | prefix | 4 | 4 | noise — generic relay use (yahoo finance, IIIF manifests, da.gd/4OzSm); no fleet markers |
| hysandbox.tencent-cloud.com | domain | 0 | 0 | real zero (confirms 2026-10-23 probe) |
| pre-amap-pc-ssr.amap.com | prefix | 0 | 0 | real zero (confirms 2026-10-23 probe) |
| da.gd | domain | 4069 | 96 | noise (Anthropic label) — bursts are Wayback bulk crawls of the shortener's 302 space (418 distinct codes, 2 digests on 2026-05-16) |

## The three ntfy hits (dead-drop-shaped, evidence quoted verbatim)

All three are in-window 200 captures of live topic pages. Topic ids were
already in `lists/urls/activity-hosts.md` (OVERLAP on the topic); the
archived message bodies are NEW to the repo (repo-wide grep found no
match; Factum match check was still queued at write time).

1. `ntfy.sh/kz1wu398dnq`, archived 2026-07-06 04:44:26 UTC
   (evidence: `ntfy_kz1wu398dnq_20260706044426.json`):
   `{"id":"vWqnQV7VZVr7","time":1783313066,"expires":1783356266,
   "event":"message","topic":"kz1wu398dnq",
   "message":"START \"tomas kopecky\" \"six million dollar man\""}`

2. `ntfy.sh/o54445`, archived 2026-07-08 15:07:11 UTC
   (evidence: `ntfy_o54445_20260708150711.json`):
   `{"id":"tjbPyJH7XAuf","time":1783523231,"expires":1783566431,
   "event":"message","topic":"o54445","message":"S"}`

3. `ntfy.sh/pz4kopsh1`, archived 2026-07-06 03:51:14 UTC
   (evidence: `ntfy_pz4kopsh1_20260706035114.json`):
   `{"id":"ox5wf32xOO6a","time":1783309874,"expires":1783353074,
   "event":"message","topic":"pz4kopsh1","message":"go|1783309874200"}`

All three dates fall inside the Jun 26–Jul 13 HF-incident window. Labelled
as **co-occurrence only — NOT METR/HF-incident validation**. The beacon
shapes (START + quoted strings, single char, `go|<epoch-ms>`) read as test
or keepalive traffic; author is unknown (not attributed to any provider
or agent instance).

## Bursts that are NOT signal

- r.jina.ai Jul 29–30 (153/496 rows vs ~25/day): ~47% are
  `cdn-cgi/challenge-platform` URLs (CF challenge bounces) + favicon —
  a crawler hitting jina's bot wall, archived in bulk.
- da.gd May mid-month (e.g. 2026-05-16, 420 rows): 418 distinct short
  codes, all 302s, 2 unique digests — Wayback bulk sweep of the public
  shortener's URL space.
- api.allorigins.win Jun 16 (104 rows): crawl of allorigins' own site
  assets/toy pages (77x 403).

## Gaps

- pastebin.com: never answered (6 backend-503 flakes across two runs
  spaced ~15 min apart). A pastebin.com domain query in a 92-day window
  is high-volume; retry with a narrower approach or at a quieter time.
- The background sweep process died once mid-run (session vanished after
  5 targets); the idempotent runner completed the remaining 8 on restart.

## Files

One `.cdx.json` + `.PROVENANCE.txt` + `.sha256` per target, plus
`summary.json` (rows, digests, per-day counts, burst notes, grades),
`progress.json`, and this report. The three ntfy bodies are saved as
`ntfy_<topic>_<timestamp>.json` with provenance + sha256.

Full per-day tables: see `summary.json`.
