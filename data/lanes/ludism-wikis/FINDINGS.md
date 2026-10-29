# FINDINGS — ludism-wikis

Short evidence summary. Full provenance is in PROVENANCE.md.
Claims are graded OBSERVED unless noted.

## Reachability (OBSERVED)

9 wiki targets were probed through 3 public reader proxies on 2026-09-28
(27 target probes + 2 proxy controls = 29 probe records).

- **2/9 targets reachable, both via jina only**: the two ApchemWiki paths
  (`tmcleod.org/cgi-bin/apchem/wiki.cgi` root and `?action=rc`) returned
  HTTP 200 with 308/318-byte 404 bodies. The wiki path is gone; the host
  answers. (INFERENCE from body content: last-write surface offline.)
- **7/9 targets unreachable on all proxies**: all five ludism.org Oddmuse
  wikis (`/scwiki/`, `/mentat/`, `/gbgwiki/`, `/ppwiki/`, `/gamedesign/`
  RecentChanges) plus the ludism.org root (http and https). jina failed
  with HTTP 422 (origin unfetchable) or RemoteDisconnected. This matches
  Lane I's direct finding that ludism.org is unreachable — now confirmed
  from a second network vantage.
- **allorigins results are INCONCLUSIVE** (OBSERVED): the example.com
  control also failed through allorigins (HTTP 522; its 16-byte body reads
  `error code: 522`). Only jina's verdicts carry weight.

## What this does not show

The probes test reachability of wiki surfaces through reader proxies.
They do not test who used the wikis, or whether agents used them.
The thecolony.ai claim excerpts in `raw/` are UPSTREAM (third-party
analysis, quoted verbatim, not independently verified).
