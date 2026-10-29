# Findings — university-shorteners

## What this lane is

A passive, read-only sweep of public stats pages on university and
community URL shorteners. Seven short links were checked on 2026-09-28
(~04:18–04:40 UTC): five university YOURLS stats pages
(`u.ethz.ch`, `goto.unm.edu` x4) and two community shortener info pages
(`url.popcat.xyz` x2).

## Main finding

Every university stats page logged the agent proxy-toolkit as HTTP
referrers. YOURLS records full referrer URLs by default, so proxied
request chains show up word for word. This makes the public stats page
an operator-side fingerprint of the toolkit on official university
infrastructure.

Toolkit referrers seen: `jqp.vercel.app`, `pure.md`, `md.succ.ai`,
`markdown.new`, `r.jina.ai`, `api.allorigins.win`,
`allorigins.hexlet.app`, `corsproxy.io`, `proxy.cors.sh`,
`cors.bwa.workers.dev`, `api.microlink.io`, `markdown.microlink.io`.
Task-family referrers seen: `www.sec.gov`, `www.investor.gov`,
`api.census.gov`, `api.datausa.io`, `pxweb.nso.gov.vn`,
`pxweb.gso.gov.vn`. Cross-venue referrers: `vanderbi.lt`, `uoft.me`,
`da.gd`, `is.gd`, `2dd.pl`, `jsonhero.io`, `web.archive.org`.

## Numbers

- `goto.unm.edu/7t6-o`: 740 full referrer rows across 35 hosts.
  Best day 2026-06-18: 1,845 hits.
- `u.ethz.ch/nB1nv`: 28 referrer rows across 6 hosts. 273 hits
  all-time. Best day 2026-06-18: 63 hits.
- `goto.unm.edu/reso`: 285 referrer rows across 11 hosts.
- `goto.unm.edu/discvr`: 57 referrer rows across 9 hosts.
- `goto.unm.edu/urphy21`: 77 referrer rows across 8 hosts.
- Total: 1,159 full per-URL referrer rows recovered.

New markers: `jqp.vercel.app/OAIDATAUSATESTXYZ` (oai + XYZ grammar,
Data USA API test); `tinyurl.com/2dhwlfmj` nested inside six wrapper
chains; a ZZ-grammar probe of the stats endpoint itself
(`yourls-infos.php/CTXWIN12ZZ0?id=7t6-o`, 4 hits); `win13=<decimal>`
nonce params on `county.json` via allorigins (8 rows).

## Grades

All claims in this lane are graded OBSERVED. They cite the per-slug
`infra.shortcut` records. The claim is: the stats page logged these
referrers. The claim is not: a named agent made these requests.

## Limits

- The July 5–6 2026 per-day referrer rows are not retrievable from the
  public YOURLS interface (no per-day drill-down). The gap is recorded,
  not filled.
- `uoft.me/<slug>+` stats pages are login-walled (instance policy).
  Recorded passively, no bypass tried.
- `goto.unm.edu/apdt9_+` does not resolve live. Negative recorded.
- `url.popcat.xyz` info pages carry no referrer data (two ChatGPT
  conversation codes, kept as controls).
