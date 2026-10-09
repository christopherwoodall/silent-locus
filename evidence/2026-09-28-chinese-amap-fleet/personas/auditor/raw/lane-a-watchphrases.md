# Lane A — watch-phrase & search-query probing on urlquery.net

**Date:** 2026-10-05 (UTC) · **Lane:** detection-workload hunt — actors probing sites' own
search boxes with known-bad strings
**Author:** Lane A subagent · **Doctrine:** metadata tells the story; misfits are leads;
agents and swarms only.

## Baseline: the known auditor cluster (jmail.world)

Established by the new-fleets/metadata hunt, 2026-10-04; re-verified here from
`data/2026-09-28-chinese-amap-fleet/new-fleets/raw/jmail_world.json` (72 reports):

- Window 2026-10-04 23:54 → 2026-10-05 03:58 UTC, median gap 3.0 min — metronomic,
  programmatic.
- Walking `/thread/EFTA<N>`, `/drive/vol<N>-efta<N>-pdf`, and 32-hex thread paths on
  `jmail.world`, probing the site's search with kit/affiliate URLs and the literal
  watch-phrase `seekers+of+decay`.
- Probe-payload distribution (70 of 72 with extractable `?q=`):
  - 17× `https://www.followlike.net/?r=19384926`
  - 13× `https://livetraffic.net/login?refer=119334`
  - 12× `https://2pink.org/dang-ky?ref=119334`
  - 10× `https://www.followlike.info/?r=19384926`
  - 9× `http://folllike.com/?19384926` (triple-l variant, affiliate ID in path)
  - 9× `seekers+of+decay`
- 12 submissions routed through `cachedview.nl` (archive-oracle as fetch-proxy).
- Followlike.net is publicly a gray-hat SEO/social-growth service with a referral
  program (`?r=` IDs) — the probes are spam/affiliate-farming URLs, i.e. this is a
  **search-index-poisoning / search-spam audit**, not credential-phishing per se.
- "Seekers of Decay" is a real Danish urban-exploration crew (seekersofdecay,
  blogspot/wordpress/pinterest) — a benign, distinctive, low-collision string: an
  ideal canary. Paired usage = kit-URL probes (does the search surface known-bad
  URLs?) + canary phrase (does the search echo/index a known-unique benign string?).

## Method

`~/workspace/skills/urlquery/bin/uq_htmx.py` (keyless htmx endpoint, keyword search
against submitted URLs). Strict pacing: ≥6s between calls, ≤2 pages of 24 per query.
Plus a frozen-corpus sweep (96,353 records, `data/2026-10-01-oai-tag-sweep/events.jsonl`)
for historical reuse of the same strings.

## RESULTS — frozen-corpus sweep (complete)

**1. `seekers+of+decay` — second, older context found (LEAD).**
113 distinct urlquery reports, 2026-06-29 → 2026-09-25, submitted URL =
`www.google.com/search?q=seekers+of+decay&udm=50` (one with `sourceid=chrome`).
Someone has been scanning GOOGLE SERPs for the watch-phrase via urlquery for ~3
months — a Google-index canary monitor, same phrase, different venue from the
jmail.world site-search probes.
- Cadence: 113 reports over 41 active days; median gap ~5h; only 6/112 gaps <10 min.
  Bursty (busiest 2026-09-23: 8, 2026-09-24: 15). NOT metronomic — reads as a
  scheduled monitor (hourly-ish checker with gaps) or human-in-the-loop triage,
  not the jmail 3-minute loop.
- Campaign label on these records: `shortener-ops-dagd` (sweep context), indicators
  `jina_allorigins_dagd`.
- Sample report IDs: `78a1050f-c389-418d-ab84-60454acb7732`,
  `96fe5550-dde5-491a-b4d7-5155fc8342d9`, `5c3ca120-3d05-438c-b534-6348e2f01cec`
  (full set extractable from the events.jsonl).

**2. `?q=`/`?s=`/`?query=` sweep of the frozen corpus — no other detection probes.**
Only 12 distinct q-values across 96,353 records; the watch-phrase-shaped ones are
exclusively the seekers phrase (15) and the jmail kit-URL payloads (36 combined).
Everything else is one-off and benign on inspection:
- `8181048` → x2tsa.com/trk.php ad-click ID (2026-06-03)
- `w0ar30hpbsrtmhuj3171ob5k`, `wa91hu4nd51rtvek3hhb1nkq` → `s=` click-tracking
  tokens on inshorts.co.uk / itsreleased.uk via whoozy.co (Jul 19 / Aug 10)
- `track.pstmrk.it` chains → Postmark email-tracking redirects (waveapps/certn
  invoices), one nested 4-deep (Jul 6 / Jul 20 / Sep 15)
- `transformers`, one Dutch ChatGPT-usage question (real-user queries, not probes)

**3. Affiliate IDs + brands — no reuse found (honest negative).**
`19384926`, `119334`, `followlike`, `folllike`, `livetraffic`, `2pink` appear in the
frozen corpus ONLY inside the jmail.world cluster URLs. No other actor in the
corpus probes with these strings.

**4. One-off vs sustained:**
- jmail.world Oct 4-5 cluster = sustained audit loop (4h+, metronomic, ~3 min) — one actor.
- Google-SERP canary = sustained monitor (3 months, bursty/scheduled, ~5h median) —
  likely one actor, different venue and rhythm from jmail; same watch-phrase suggests
  shared tradecraft or shared operator, but the cadence gap argues against the same
  running script.

## RESULTS — live htmx queries (BLOCKED: VM-wide egress outage)

All VM HTTPS egress has been down since ~04:24 UTC 2026-10-05 (proxy CONNECT
timeouts to every host; DNS still resolves). A separate agent (forager) is
independently retry-probing egress to urlquery.net, confirming it is
infrastructure-wide, not this lane's tooling. A browser.open fallback to the htmx
endpoint returned HTTP 204 (endpoint requires HX headers) and policy guidance
closed that path — do not retry via browser.

A resilient runner is in place and WILL execute the live queries automatically
when egress recovers:
- `~/workspace/lane-a-scratch/run.sh` — egress-gated (checks every 3 min, up to
  ~2h), curl-based, ≥6s pacing, ≤2 pages/query; parses to JSON at the end.
- Detached via setsid/nohup at ~05:08 UTC (survives the earlier process-table
  reset that killed the first attempt and wiped /tmp — scratch now lives under
  ~/workspace, not /tmp).
- Queries queued: `seekers+of+decay`, `seekers of decay`, `seekersofdecay`,
  `19384926`, `119334`, `followlike`, `folllike`, `livetraffic`, `2pink`,
  `refer=`, `?q=`.
- Progress: `~/workspace/lane-a-scratch/run.log`; results:
  `~/workspace/lane-a-scratch/parsed/<slug>.json`.

Outstanding live questions (for the parent to collect from `parsed/` once egress
is back):
- Is the jmail.world cluster still running now (last baseline sighting 04:13 UTC)?
- Any other current actor probing with the affiliate IDs / brands / watch-phrase?
- Recent `?q=` window: other probe-strings with kit-URL + affiliate-ID grammar?
- `refer=` param sweep for additional affiliate-ID-shaped probes.

## Open questions

- Is the Google-SERP canary operator the same party as the jmail.world auditor?
  (Same phrase, different venue, different cadence — worth a lane of its own.)
- `udm=50` on the Google probes: identify which Google vertical/mode that is.
- Do the affiliate IDs 19384926 / 119334 appear on urlscan.io or other public
  scan venues?
