# PROVENANCE — uoft-shorteners lane (2026-09-28, night watch)

Passive recon only. No submissions, uploads, accounts, logins, posts, link
creation, or counter-increments were performed. All artifacts below are
read-only HTTP GETs of public pages.

## Method
- `dig` for A records; plain `curl` fetches of public front pages and `+`
  stats pages (the YOURLS public stats suffix — one passive GET each);
  `crt.sh` JSON API; public search engines; Wayback CDX (returned empty /
  unreachable, consistent with prior findings).
- uoft.me agent-grammar slugs were NOT looked up against any stats API that
  requires authentication; the login wall was observed and recorded, and no
  login was attempted.

## Sources
| File | Source URL / origin | Fetched |
|---|---|---|
| uoft-me/root_2026-09-28.html | https://uoft.me/ | 2026-09-28 |
| uoft-me/maagentxyz99999_plus_2026-09-28.html | https://uoft.me/maagentxyz99999+ | 2026-09-28 |
| uoft-me/zzagent740558_plus_2026-09-28.html | https://uoft.me/zzagent740558+ | 2026-09-28 |
| uoft-me/amass932899504_plus_2026-09-28.html | https://uoft.me/amass932899504+ | 2026-09-28 |
| uoft-me/mafresh91011_plus_2026-09-28.html | https://uoft.me/mafresh91011+ | 2026-09-28 |
| uoft-me/crtsh_2026-09-28.json | https://crt.sh/?q=%25.uoft.me&output=json | 2026-09-28 |
| t-mdcdev-me/root_2026-09-28.html | https://t.mdcdev.me/ | 2026-09-28 |
| t-mdcdev-me/squarespacefreeemail934785_plus_2026-09-28.html | https://t.mdcdev.me/squarespacefreeemail934785+ | 2026-09-28 |
| t-mdcdev-me/evegelendiyarbakrescort772509_plus_2026-09-28.html | https://t.mdcdev.me/evegelendiyarbakrescort772509+ | 2026-09-28 |
| t-mdcdev-me/mattressstoresaroundmyarea909270_plus_2026-09-28.html | https://t.mdcdev.me/mattressstoresaroundmyarea909270+ | 2026-09-28 |
| t-mdcdev-me/bayanescortdiyarbakr401683_plus_2026-09-28.html | https://t.mdcdev.me/bayanescortdiyarbakr401683+ | 2026-09-28 |
| t-mdcdev-me/hkigaprw_plus_2026-09-28.html | https://t.mdcdev.me/hkigaprw+ | 2026-09-28 |
| t-mdcdev-me/i2mrjnck_plus_2026-09-28.html | https://t.mdcdev.me/i2mrjnck+ | 2026-09-28 |

## Corpus links
- uoft.me agent slugs (maagentxyz99999, zzagent740558, amass932899504,
  mafresh91011, utmace) first surfaced in
  github.com/joshuadavid/wikiagentswarminvestigation `agent-logs/shorteners/`
  (uoft-me dir, 5 slugs) — cross-referenced, not copied; their bodies were
  not pulled from that repo.
- ES cross-checks (read-only): `collusion-wiki` 479 docs
  (`origin_sites=uoft.me`, `origin_kinds=shortener_candidate`);
  `urlquery-hunt` 2 docs (`hunt.node_id=ioc-uoft-me`,
  `hunt.ioc_type=shortener-domain`, first seen 2026-06);
  `university-shorteners` 1 doc (uoft.me as 15-hit referrer on
  goto.unm.edu/7t6-o); `proxy-primitives` 0. `t.mdcdev.me` = 0 hits in all
  four indices.

## Verdict
- uoft.me: live (YOURLS 1.7.6, official UofT shortener, domain-whitelisted);
  all four known agent-grammar stats pages return the YOURLS login wall
  ("Please log in") — negative for passive stats, recorded not indexed.
- t.mdcdev.me: live (YOURLS 1.9.2, open-creation instance); public `+` stats
  confirmed OPEN on live slugs; the three live slugs examined are SEO-spam
  (no agent-grammar slugs, no swarm-toolkit referrers) — negative for swarm
  activity, recorded not indexed. No link creation was attempted despite the
  open form.

Per the lane's verification bar, clean negatives are recorded in the
progress log + note instead of an empty Elastic index.

## Normalization 2026-09-29 (events.jsonl; no rollup — pure recon stream)

- `events.jsonl`: 13 rows, all schema-conformant.
  - 10 `yourls_stats_page` — 4 uoft.me `+` pages (all YOURLS login wall,
    negative for passive stats) + 6 t.mdcdev.me `+` pages: 3 public-open
    SEO-spam slugs with extracted long URL / created date / hit counts /
    best day (evegelendiyarbakrescort772509, mattressstoresaroundmyarea909270,
    squarespacefreeemail934785) and 3 slug-404s (bayanescortdiyarbakr401683,
    hkigaprw, i2mrjnck).
  - 2 `shortener_info_page` — front pages (uoft.me YOURLS 1.7.6,
    t.mdcdev.me YOURLS 1.9.2).
  - 1 `artifact_observation` — the crt.sh pull (126 certs for %.uoft.me,
    Let's Encrypt).
- Fingerprint identity strings: `yourls:<instance>:<slug>` (stats pages);
  `shortener_info:<instance>` (front pages); `crtsh:uoft.me`.
- `labels.timestamp_source`: `labels:captured.date` (=2026-09-28 fetch date,
  from filenames).
- No new record_kinds (`yourls_stats_page` registered;
  `shortener_info_page` already in use by the sibling university-shorteners
  datasets).
