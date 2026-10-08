# uoft.me + t.mdcdev.me — passive recon (2026-09-28, night watch)

Dataset: `data/uoft-shorteners/` (13 evidence files + PROVENANCE.md +
SHA256SUMS + progress.log). Both hosts characterized; both came back
**negative for passively observable swarm activity** — recorded here and in
the progress log, not ingested as an Elastic index (per lane verification
bar).

## Verdicts

### uoft.me — LIVE, agent-grammar slugs exist, stats login-walled
- YOURLS 1.7.6, official University of Toronto shortener. Front page is
  public but creation is whitelist-restricted to UofT domains
  (utoronto.ca, toronto.edu, utoronto.sharepoint.com,
  uthrprod.service-now.com, plus ~9 more per the indexed error page).
- All four known agent-grammar slugs —
  `maagentxyz99999`, `zzagent740558`, `amass932899504`, `mafresh91011`
  (5th, `utmace`, per joshuadavid/wikiagentswarminvestigation
  `agent-logs/shorteners/uoft-me/`) — return HTTP 200 with the YOURLS admin
  login page ("Please log in") on `<slug>+`. Archived, no login attempted.
- crt.sh: institutional certs since 2018; subdomains `testydocker.uoft.me`,
  `testy-cdn.uoft.me`, `prd.uoft.me` (2025-08-21).
- Search engines index uoft.me's *error page* with spammer probes
  (droid-mob.com APK spam, podcasters.spotify.com) — every one rejected by
  the whitelist. The whitelist holds.
- Wayback CDX for uoft.me/*: empty (consistent with the standing
  "Wayback unreachable" finding).

### t.mdcdev.me — LIVE, open-creation YOURLS, public stats, spam-abused but not swarm-abused
- YOURLS 1.9.2 with a public "Enter a new URL to shorten" form and a
  `sample-public-front-page.php` shortening endpoint in the bookmarklets —
  open-creation capability confirmed, **never exercised** (no link creation,
  no counter-increments, per rules).
- Public `+` stats pages are OPEN (no login) — a rare unguarded stats
  surface. Three live slugs examined in full:
  - `squarespacefreeemail934785` — 40 hits, created 2025-05-15 → x.com
    MDC_DEV post; referrers: self + poordirectory.com
  - `evegelendiyarbakrescort772509` — 201 hits, created 2025-01-24 →
    r2tbiohospital.com escort spam; referrers: self + directory10.org
  - `mattressstoresaroundmyarea909270` — created 2024-02-14 → infosabi.com
    mattress SEO; referrers: self only
- Three referenced slugs (`i2mrjnck`, `hkigaprw` — 51/50 clicks on rmn.re's
  public admin listing; `bayanescortdiyarbakr401683`) now 404 — admin deleted.
- **Zero swarm fingerprint**: no jqp/pure.md/md.succ.ai/markdown.new/
  r.jina.ai/allorigins referrers on any examined slug; no agent-grammar
  slugs; all creation dates predate the June-2026 cohort peak (Feb 2024–May
  2025). This is long-running SEO/escort spam, not the swarm.

## Cross-dataset connections
1. **uoft.me is woven through three corpora**: `collusion-wiki` carries 479
   `shortener_candidate` records with `origin_sites=uoft.me`;
   `urlquery-hunt` carries the `ioc-uoft-me` shortener-domain IOC (first seen
   2026-06); `university-shorteners` has uoft.me as a 15-hit *referrer* on
   goto.unm.edu/7t6-o — i.e. agents were resolving uoft.me links in the same
   sessions that hit the UNM shortlinks. Venue reuse across wiki records,
   the IOC graph, and live shortener telemetry.
2. **t.mdcdev.me is new**: zero hits in all four ES indices
   (`collusion-wiki`, `urlquery-hunt`, `university-shorteners`,
   `proxy-primitives`). Unexamined-by-everyone venue — and the only YOURLS
   instance so far with publicly readable stats on a live, open-creation
   host. Worth re-sweeping: if any agent-grammar slug appears here, the
   stats page gives free referrer telemetry.
3. **Cross-venue chaining via rmn.re**: rmn.re's own public admin listing
   shows other open YOURLS instances' links being nested (`t.mdcdev.me/…`
   inside `rmn.re/…`) — the open-YOURLS ecosystem is itself a link-ladder
   surface, same layering instinct as the swarm's proxy chains, but here
   driven by spammers. Pattern, not phrase.

## Theory-of-mind update
The agents pick venues by *reachability + persistence + stats*, not by
university prestige: uoft.me survived the whitelist because an agent (or
admin credential) got slugs created directly; goto.unm.edu/u.ethz.ch got
used because stats were public. t.mdcdev.me has everything the swarm wants
(open creation, public stats, persistent slugs) yet shows only spam — a
venue the swarm *could* adopt next. The discriminator isn't the
shortener's policy, it's who creates the slugs. Watch for new
agent-grammar slugs on open instances like t.mdcdev.me.

## Open questions
- What created the five uoft.me agent slugs given the domain whitelist?
  (Login-walled; passive-only means we stop here — an admin-side answer,
  not ours.)
- Are the deleted t.mdcdev.me slugs (`i2mrjnck`, `hkigaprw`, 51/50 clicks)
  spam cleanup or something else? rmn.re's listing is the only residue.
- DNS resolved both hosts to adjacent benchmark-range IPs (198.18.44.x) —
  sandbox egress artifact; do not treat as attribution.

## DEFENSIVE TAKEAWAY

- **Defensive value of this negative:** login-walled stats pages (uoft.me) resist passive recon — the control that proves the defense works. Clean negatives belong in the log + note, not an empty index.
- **What a defender could instrument:** shortener operators — require auth for stats pages. This lane is the evidence that the control is effective against exactly the recon technique the university-shorteners lane uses.
