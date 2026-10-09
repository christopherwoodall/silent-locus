# Social sweep — Amap fleet markers (2026-10-04)

Surface: social platforms. Tool status: `social.search` (Instagram/Threads/Facebook)
was attempted 6x with distinct marker queries — every call failed with
infrastructure timeouts ("social.search session ... remained unsettled after
subprocess timeout"). Per the tool's own guidance, all queries below were
re-run via `browser.search` fallback. Caveat: the fallback is general web
search, not IG/Threads/FB-native; a native social pass should be re-attempted
when the backend recovers.

Known-context exclusion: mentions of the swarmcha.se chinese-agent-fleet report
itself are known, not new. Zero such mentions surfaced at all (see Q6).

## Q1 — `uqscan` — CLEAN NEGATIVE
- social.search `"uqscan tag urlquery reports / uqcors urlscan tag / lhr.life tunnel agent scan"`: infrastructure timeout.
- browser.search `"uqscan" urlquery tags`: no agent-fleet or researcher hits.
  Only noise: `iqscan-*` typosquat domains (w3stats.com), a uRISQ threat-scanning
  PDF, one TikTok video. The `uqscan` tag string has no public chatter outside
  urlquery report tags.

## Q2 — `uqcors` — CLEAN NEGATIVE
- social.search: infrastructure timeout.
- browser.search `"uqcors" urlscan`: no relevant hits. Results were TON
  blockchain addresses with `UQCORS` prefixes (tonviewer.com) and OCR noise
  from 1920s–1930s newspaper scans. No agent-fleet, urlscan-tag, or researcher
  discussion.

## Q3 — `lhr.life` — ADJACENT (generic agent behavior, no Amap linkage)
- social.search: infrastructure timeout.
- browser.search `"lhr.life" tunnel urlscan agent`: localhost.run / `lhr.life`
  tunnels are commodity agent infrastructure, not fleet-distinctive:
  - kolonie-ai/kolonie-platform issue #585 (2026-08-08): agents naming
    `<hex>.lhr.life` wake endpoints.
  - pokemon-player SKILL.md files in five agent repos
    (chiragborse1/kova-test, taxbax/hermes-agent, iamlalitpandit/rudrax,
    boweiliu/gengar, ali-shf/custom-hermes) instruct agents to open
    `ssh -R ... nokey@localhost.run` tunnels and grep for the `.lhr.life` URL.
  - Enterprise DevSecOps guide (instatunnel.my) and CloudSEK phishing research
    (scworld.com) treat localhost.run as a standard reverse-tunnel service.
- browser.search `"lhr.life" amap uqscan`: only stale urlscan.io result pages
  (2024-era, phishing noise) and scam-checker pages. Zero Amap or uqscan
  co-occurrence. Verdict: no public linkage of `lhr.life` tunnels to the Amap
  fleet; tunnel usage alone is not a fleet fingerprint.

## Q4 — `pandalegacy` — CLEAN NEGATIVE
- social.search: infrastructure timeout.
- browser.search `"pandalegacy" urlquery agent`: every hit is a Fortnite
  Creative map creator (PandaLegacy, Epic Partner; fchq.io, fortnitecreativehq.com,
  fortnite.gg). No agent-fleet, urlquery, or researcher usage of the string.

## Q5 — `sub_poi_navi` — CLEAN NEGATIVE
- social.search: infrastructure timeout.
- browser.search `"sub_poi_navi" amap`: only map-documentation noise (GE Vernova
  APM Maps module PDF, MapNav Unity manual). No public discussion of the marker.

## Q6 — researchers discussing the Amap agent fleet — CLEAN NEGATIVE
- browser.search `Chinese agent fleet Amap data collection swarmchase`:
  results were Amap's own legitimate press release ("Amap Launches Spatial
  Intelligence Open Platform for No-Code AI Agents", syndicated Sep 2026,
  prnewswire.com et al.) — nothing to do with the fleet.
- browser.search `swarmcha.se chinese agent fleet`: zero hits referencing the
  swarmcha.se report. Results were unrelated naval/drone swarm news
  (maritime-executive.com, zerohedge.com, etc.). The Amap fleet report appears
  to have no public echo — no researcher threads, no social pickup found.

## Q7 — researchers discussing urlquery agent traces (context)
- browser.search `urlquery AI agent traces researchers urlscan agent activity`:
  active discussion, all KNOWN context per memory, none mentioning the Amap
  markers (no uqscan / lhr.life / pandalegacy):
  - Transluce Sep-23-2026 report on urlquery.net agent probes (dev.to, letsdatascience.com).
  - Asymmetric Security reconstruction of rogue OpenAI agent activity,
    Oct 1 (securityaffairs.com, technadu.com — FBI/CDC/SEC/IEA/Mayo targets).
  - Rowan Howard-Jones UNCTADstat 16,500-scan analysis (techbooky.com).
  - WSJ Oct 3 via areeblog.com: "Swarmchasers" — ~400-member Discord research
    community (Joshua David, Alicja Piecha's RubyGems find, Nightingale
    Collective, DSEWiki ZZZ pages). Fresh researcher-community metadata;
    social-native hunting is centralized on that Discord.

## Q8 — localhost.run tunnels + urlscan probing — KNOWN-CONTEXT ADJACENT
- browser.search `"localhost.run" tunnel submitted urlscan agents scanning`:
  - joshuadavid/wikiagentswarminvestigation
    `research/swarm-mechanisms/additional-context.md` documents the
    collusion-wiki swarm's use of Pinggy / Serveo / localhost.run /
    localtunnel, DSE visits with localhost.run referrers (Jun 17 00:39 UTC),
    and a Jun 17 10:11 UTC urlscan capture of a Python HTTP server via Pinggy.
    This is the known OpenAI-attributed swarm, NOT a new fleet.
  - hamzah2304/messageboardauditbench notes "reads arriving via a
    localhost.run tunnel" in the DSEWiki audit data (same known swarm).

## Q9 — `tronzap` probing — CLEAN NEGATIVE
- social.search: infrastructure timeout.
- browser.search `"tronzap" probing scan`: all hits are the TRON energy-rental
  service (tronzap.com), its Go SDK (github.com/tron-energy-market), and a
  bitcointalk thread. No "probing" discussion; the marker has zero public
  chatter in the agent-fleet sense.

## LEAD — off-frame: second Chinese-attributed agent swarm (Taiwan gov targets)
Does not fit the Amap map-data-collection frame; per doctrine, a lead, not a
negative:
- webpronews.com (crawled ~54 days ago): "Suspected Chinese Hackers Unleash AI
  Agent Swarm on Taiwan Government Systems" — Dream Security / Dream Research
  Labs recovered a 160MB workspace (1,395 files). Up to 8 agents operating in
  parallel across 12 attack waves, July 1–4. Frameworks: Hermes and OpenClaw
  (open-source agent frameworks). Internal logs split Simplified Chinese
  (status) / Traditional Chinese (target analysis). 21 Taiwan government
  systems reconnoitered; agents self-labeled Agent A–Q.
- Why it matters to this sweep: a distinct Chinese-attributed AGENT swarm in
  the same incident window, with no overlap with the Amap markers reported
  (no uqscan / lhr.life tags mentioned). Worth cross-checking against the
  urlquery corpus for shared infra markers.
- Naming caution: this "Hermes" is the open-source agent framework, not
  taxbax/hermes-agent (hackathon host). Do not conflate.

## Bottom line
- New undiscovered fleets via social: NONE. All five markers (uqscan, uqcors,
  lhr.life-as-fleet-marker, pandalegacy, sub_poi_navi) plus tronzap have zero
  public researcher/operator discussion.
- The Amap fleet report has no visible public echo.
- `lhr.life`/localhost.run tunnels are generic agent tradecraft — useful
  context, weak fingerprint.
- One lead worth handing off: the Dream Security Taiwan-government agent
  swarm (Jul 1–4, Hermes+OpenClaw, 8 agents) — Chinese-attributed, separate
  fleet, worth marker cross-check.
- Recommended follow-up: re-run the native social.search pass when the
  backend recovers; consider Chinese-language queries (markers may surface in
  Chinese infosec communities).
