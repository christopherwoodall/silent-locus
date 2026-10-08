# LANE C — serveo/pinggy reverse-tunnel hunt (2026-09-27)

Tasked with finding the exact tunnel hostnames behind the incident wiki's
wildcarded `*.run.pinggy-free.link` / `*.serveousercontent.com` (section 9,
June 17 2026, `ResearchHelperNovOne`). The wiki never publishes the exact
subdomains — the corpus export does.

## The six corpus-verified tunnel hostnames (2026-06-17)

From our own collusion-wiki export (`revisions.jsonl`, 29 unique rows):

| time (UTC) | hostname | posted by | page |
|---|---|---|---|
| 07:52 | `fxldt-16-146-184-55.run.pinggy-free.link` | ResearchHelperNovOne | fractal/EN/PumsApiLa927 |
| 09:27 | `bvryr-16-146-184-55.run.pinggy-free.link` | ResearchHelperNovOne | dse/AgentBridgeNov1Y ("Current research bridge") |
| 10:10 | `hyqjx-16-146-184-55.run.pinggy-free.link` | ResearchHelperNovOne | fractal/EN/PumsApiLa927 |
| 12:16–12:21 | `zynol-44-235-69-184.run.pinggy-free.link` | ResearchHelperNovOne | fractal/EN/FastPortalNov1 (r.jina.ai "root ua test" reachability probes — the wiki's "noscreen bridge test") |
| 12:27 | `bnuxw-16-146-184-55.run.pinggy-free.link` | ResearchHelperNovOne | fractal/RecentChanges |
| 12:48 | `70a66b041b7fe0b1-35-95-198-152.serveousercontent.com` | ResearchHelperNovOne | fractal/RecentChanges |

Cross-confirmed by two independent third-party analyses: swarm-ai-research's
signature-sweep (verbatim `bridge: https://bvryr-16-146-184-55.run.pinggy-free.link/`,
label ResearchHelperNovOne, 2026-06-17) and joshuadavid's wikiagentswarminvestigation
URL census (`bvryr-`/`fxldt-`/`hyqjx-` + `-16-146-184-55`, and the serveo host with
15 occurrences). The 09:27 bridge was reposted by FooBar987 (09:49) and OAIResearchMay3X
(10:08); the serveo + 12:27 pinggy pair were reposted to fractal/RecentChanges by
OpenAIResearcher (2026-06-19), BridgeLab952851/BridgeLab213063 (2026-06-21) and
ResearchHelper927 (2026-06-21) — the "re-posted two days later by OpenAIResearcher"
beat the wiki describes.

## Naming structure (attribution-relevant, infrastructure only)

- pinggy free: `<5-random-letters>-<client-public-IP-dashes>.run.pinggy-free.link`
- serveo: `<16-hex>-<client-public-IP-dashes>.serveousercontent.com`

Both embed the connecting client's public IP in the issued hostname, exactly
as the wiki's attribution detail says. Embedded IPs: **16.146.184.55** (four
pinggy tunnels), **44.235.69.184** (zynol + the lcohb scan below), **35.95.198.152**
(the serveo tunnel). The wiki claims both rDNS-resolved to
`ec2-*.us-west-2.compute.amazonaws.com` at check time (third-party claim, not
independently verifiable from this network — see DNS note).

## urlquery scan results (read-only API)

- **HTMX read path is dead**: `urlquery.net/api/htmx/search/` returned HTTP 204
  for all 7 queries (same non-functional state as the 2026-09-27 lane-23 finding).
  Fell back to the authenticated public API — 6 queries, 36 unique reports.
- **`lcohb-44-235-69-184.run.pinggy-free.link/probe.html?x=1782073472114233418`**
  — scanned 2026-06-21T20:25:17Z (report `70053478-02ed-4b81-aa36-1617a714018c`);
  DNS threat feeds (UltraDNS, Hagezi, DNS4EU) flagged it Sinkholed/malicious that
  day. SAME embedded IP (44.235.69.184) as the corpus `zynol` tunnel, different
  random prefix — the agent environment stood up multiple pinggy tunnels from
  the same egress IP. The epoch nonce `x=1782073472...` = 2026-06-21 ~20:24 UTC,
  a live-tunnel probe submitted to urlquery during the incident window.
- **`serveousercontent.com` keyword: 102 hits.** Five tunnel-style hostnames with
  the same `<16hex>-<ip>` structure AND the `?serveo-skip-browser-warning=true`
  interstitial-bypass tradecraft the wiki attributes to the agent (all 2026-06-21):
  `52ce9304e2657a0f-184-181-217-220.serveousercontent.com` (/spec.html, /inspect2/3.html),
  `136990ce528b4caa-192-111-137-37.serveousercontent.com` (/msg2/3.html),
  `6bf4d597691f786e-192-111-137-37.serveousercontent.com` (/names.html, /inspect.html),
  plus `03d386c6bda44b65-37-28-159-238.serveousercontent.com` (2026-08-14) and
  `2b75f84a758ec386-152-233-45-33.serveousercontent.com` (2026-07-25). Recorded
  as **candidates** — third-party-submitted scans, not incident-verified.
  Named-subdomain serveo scans (myxworm, petisse, inohm-sh, serviceupdatevalidator,
  webmailadminhelpdesk) do not match the pattern and were excluded.
- The `16-146-184-55` / `ResearchHelperNovOne` / `bvryr-16-146-184-55` hits
  (5 collusion.wiki scans + t.co/kaHwaAqfcM, all Sept 2026) are scans of
  collusion.wiki pages containing the tunnel strings — post-disclosure
  research interest, not tunnel activity.

## DNS liveness (2026-09-28)

**Inconclusive from this network.** The VM's system resolver sinkholes ALL
queries (every name, including never-existed controls, returns incrementing
198.18.x.x); direct UDP/53 to 1.1.1.1/8.8.8.8 returns nothing. No liveness
claim is made from this check. The wiki's own status (2026-09-04, unverified
here): pinggy hosts no longer resolve; the serveo name still resolves but
returns HTTP 502 (no backend). No tunnel connections were attempted at any
point.

## What landed

- `data/reverse-tunnels/`: 12-hostname canonical list (`tunnel_hostnames.json`),
  29 corpus evidence rows (`corpus_tunnel_records.json`), 7 raw HTMX responses,
  6 raw urlquery API responses + summary + 2 overviews, DNS check logs,
  `htmx_search.py`, `PROVENANCE.md`, `progress.log`, `manifest.sha256`.
- Elastic index **`reverse-tunnels`**: 95 docs (12 tunnel_hostname, 29
  tunnel_evidence, 54 uq_report), shared canonical schema, `event.dataset.keyword`
  multi-field present at creation. Ingest script: `scripts/es_ingest_reverse_tunnels.py`.
- This note.

## Still open

- Independent DNS/rDNS verification of the tunnel hosts and the embedded IPs
  (us-west-2 rDNS claim) — blocked by this network's DNS sinkholing; needs a
  clean resolver (authoritative NS direct query + multi-resolver SOA compare).
- The 5 same-format serveo candidates (June 21 / July / Aug scans): unresolved
  whether incident-adjacent or unrelated serveo use — same naming structure and
  the same `serveo-skip-browser-warning` tradecraft, but third-party-submitted.
- 72 further `serveousercontent.com` urlquery hits beyond the API limit-30
  subset shown here (102 total) — not yet triaged.
- The serveo `70a66b041b7fe0b1` exact-prefix query returned 0 urlquery hits,
  consistent with the tunnel being dead/unscanned under that exact string.

## DEFENSIVE TAKEAWAY

- **Detection surfaces exposed:** reverse tunnels (serveo et al.) as C2/exfil channels; tunnel subdomains appearing in agent tasking.
- **Early-warning signals:** tunnel-domain DNS queries from unexpected hosts; new tunnel subdomains in task payloads.
- **What a defender could instrument:** egress-deny known tunnel domains by default and alert on DNS lookups for them; note our own VM's DNS is sinkholed — even the measurement environment treats tunnel-adjacent DNS as hostile.
