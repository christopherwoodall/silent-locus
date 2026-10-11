# Provenance — 2026-05-12 university shortener events (wayback slice)

Lane: `2026-05-12-university-shorteners-events`.
Legacy dir: `evidence/remove-2026-05-12-university-shorteners-events/` (moved to
`data/lanes/2026-05-12-university-shorteners-events/raw/` on ingest, 2026-10-11).

## What this dataset is

One-shot Wayback Machine slice (built 2026-09-29) of university shortener
stats pages. 6 short links on 3 shortener instances:

- goto.unm.edu: 7t6-o, discvr, reso
- u.ethz.ch: nB1nv
- url.popcat.xyz: 5vtSk2RG2f, IRZTIxDlZ

Per short link: the stats-page HTML as archived by the Wayback Machine, plus a
parsed `referrer_urls_daily` JSON (referrer hosts, hit counts, sample URLs).
19 captures seen, 17 downloaded (2 already held), 0 failed. SHA256SUMS covers
all files.

## Why it matters

Public shortener stats pages leak the operator-side fingerprint of shortener
traffic. The nB1nv (u.ethz.ch) capture logged 13 referrer hosts including
proxy/converter stack members (allorigins.hexlet.app, jqp.vercel.app,
md.succ.ai, api.usa.gov/TESTREF, 2dd.pl) — the swarm's proxy stack as
referrers. The discvr (goto.unm.edu) captures logged m.facebook.com,
m.naver.com, library.unm.edu, riotgames.com.

## Factum ingest (2026-10-11)

- 17 `web.capture` observations (one per stats-page wayback capture).
- 17 `infra.ioc` (category `domain`) for distinct referrer hosts.
- Shortcut resolutions (short_url -> destination) for these slugs already
  exist in Factum under lanes `university-shorteners` /
  `2026-09-28-yourls-resweep`; this lane adds the wayback-captured referrer
  observations, not the resolutions.
- No schema changes needed. Bundle: `ingest-2026-05-12-university-shorteners-events-20261011`.
