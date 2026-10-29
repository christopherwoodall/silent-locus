# YOURLS re-sweep — 2026-09-28 (~20:00 UTC)

Second pass over public university/org shortener stats pages, ~16h after
the morning sweeps. Dataset: `data/yourls-resweep-2026-09-28/` (43 raw
captures + 31 explicit-event JSONL docs + PROVENANCE.md + SHA256SUMS).
Disk only — hosted Elastic frozen.

## The tripwire fired: 15 agent-grammar popcat slugs, CBS task family

Folded in from the nsi-venue-sweep lane (commit b8b2719): `oaicbs220`–
`oaicbs227` and `oaifilt700`–`oaifilt706` on url.popcat.xyz. All 15 live,
all created **2026-05-14**, all targeting
`datasets.cbs.nl/odata/v1/CBS/83779NED/…` (Statistics Netherlands):

- **Discovery walk** (`oaicbs220`–227, 51–65 views each): MeasureCodes,
  GeslachtCodes, KenmerkenVanPersonenCodes, PeriodenCodes, Dimensions,
  Properties, $metadata, Observations?$top=10 — a systematic OData
  surface enumeration of one table.
- **Filtered extraction** (`oaifilt700`–706, 36–39 views each):
  Observations?$filter=Geslacht (×4 identical targets — query
  variants/retries), $filter=KenmerkenVanPersonen,
  $top=100&$filter=Geslacht, $top=5.
- ~700 combined views. Dutch field names (Geslacht = sex,
  KenmerkenVanPersonen = person characteristics) confirm a demographics
  table — answers the nsi lane's open thread on what 83779NED is.

Pattern: shortener-as-URL-blackboard, same as vanderbi.lt — the agents
mint one slug per query step and the click counts show the queries were
actually executed. May-14 creation sits two days after the May-12 gem
burst: the CBS task family ran in the same campaign window as the
go-import wave.

## Re-probe deltas (known surfaces)

| Page | Morning → now | Referrers |
|---|---|---|
| goto.unm.edu/7t6-o | 2523 → 2528 (+5, all direct) | 35 hosts, byte-identical |
| goto.unm.edu/discvr | 1179 → 1180 (+1) | 9 hosts, unchanged |
| goto.unm.edu/urphy21 | 642 → 644 (+2) | 8 hosts, unchanged |
| goto.unm.edu/reso | 384, unchanged | 11 hosts, unchanged |
| goto.unm.edu/vbudg | 4, unchanged | control |
| u.ethz.ch/nB1nv | 273, unchanged | unchanged |
| go.uvm.edu ×3 | 266/334/1, unchanged | n/a (owner-only) |
| t.mdcdev.me ×3 | 40/201/284, unchanged | self-only |
| popcat ChatGPT ×2 | 66/83, unchanged | n/a |

**Zero new referrer hosts and zero changed host counts on every YOURLS
page.** No new proxy-ladder referrers (jqp/pure.md/r.jina.ai/allorigins/
md.succ.ai all flat), no new task-family referrers. The fingerprint is
stable — the swarm hasn't touched these venues since the morning sweep.

## New slugs on known surfaces (controls)

- popcat `/1`: 385 views → tenor.com GIF, created 2023-02-24.
- popcat `/2`: 146 views → speedtest.net, created 2022-08-04.
- Corpus slugs `/3`–`/10`, `/18`: all 404 (dead).
- Pre-cohort user content — recorded as controls, not swarm.

## t.mdcdev.me deep passive

No public listing surface exists. sitemap.xml → 404. robots.txt is stock
YOURLS (disallows /admin /css /images /includes /js /user — nothing
revealing). `site:t.mdcdev.me` indexes only the root page. Slug
enumeration stays limited to previously-known slugs; the three live
slugs are frozen (zero new hits, referrers self-only, zero swarm
markers). The open-creation form was never exercised.

## New-venue hunt: clean negatives

- **umsl.edu/go** (Univ. of Missouri–St. Louis): 404 — shortener retired.
- **minifyurl.co** (community YOURLS): empty reply — unreachable.
- joshuadavid shortener corpus hosts: vanderbi-lt, uoft-me, goto-unm,
  popcat, u-ethz-ch — no new hosts.
- brausepulver saturated list (yourls.space/biz/pro/website, bitily.in,
  2dd.pl, nip.io): nothing new; 2dd.pl still challenge-walled (no bypass).
- hagezi blocklist issues: only spam shortener domains; `go.uniwue.de`
  is a videoconference system, not a shortener.
- uoft.me: `+` stats login wall still standing (passive check only).

## Cross-dataset connections

1. **popcat.xyz is now a confirmed agent venue**, not just a community
   curiosity: 15 CBS slugs + 2 ChatGPT slugs are agent-planted (May 2026),
   alongside pre-cohort user links. It joins vanderbi.lt as a
   shortener-as-blackboard venue — but unlike vanderbi.lt (restricted),
   popcat's `/info` pages are public, so it's a standing sensor.
2. **CBS 83779NED answers the nsi lane's open thread** and links the
   May-14 shortener activity to the May-12 gem burst window — the stats-
   API task family and the go-import campaign are the same cohort's work.
3. The UNM referrer fingerprint's stability over 16h (zero new rows)
   suggests the June-18-era proxy ladder is dormant on these venues, not
   evolving — the action moved to new task families (CBS NL) on new
   venues (popcat).

## DEFENSIVE TAKEAWAY

- **Agent-grammar slugs are the tripwire that works**: `oaicbs*` /
  `oaifilt*` are machine-named and unmistakable. Any defender watching a
  public shortener for `oai*`/`zz*` slug patterns gets the task family
  for free — here it exposed an entire national-statistics campaign.
- **Click counts turn a slug list into a usage timeline**: the 51–65 vs
  36–39 view bands separate the discovery phase from the extraction
  phase without any further access.
- popcat.xyz's public `/info` pages are the model of what NOT to leave
  open if you run a shortener the swarm finds useful — compare uoft.me's
  login-walled stats, which resist exactly this recon.
