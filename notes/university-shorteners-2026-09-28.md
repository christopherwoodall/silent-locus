# University-shortener / YOURLS sweep — 2026-09-28

Scope started as university shorteners with public logs; widened same day at
Christopher's direction to ANY YOURLS instance that might bite (orgs,
communities, indexed/discoverable public stats). Index `university-shorteners`
keeps its name; `labels.shortener.scope` distinguishes university vs community.

## Verifiable hits (7 docs in `university-shorteners`, all live-fetched 2026-09-28)

### ETH Zürich — u.ethz.ch/nB1nv (public `+` stats)
- Target: ETH for Development Pioneer Fellowship page.
- Referrers: jqp.vercel.app 44, sec.gov 4, allorigins.hexlet.app 3,
  markdown.new 3, example.com 3, u.ethz.ch 3, Various 10. Direct 174.
- Best day: 63 hits on 2026-06-18.
- Source: https://u.ethz.ch/nB1nv+?jqpaccess=1

### UNM — goto.unm.edu/7t6-o (public `+` stats) — the Rosetta page
- Target: UNM Anderson School events (targetX).
- 2,042 referrer hits / 483 direct. Best day: **1,845 hits on 2026-06-18**.
- Referrers: jqp 648, goto.unm.edu 375, pure.md 119, md.succ.ai 102,
  api.microlink.io 74, docs.google.com 65, pxweb.nso.gov.vn 59, da.gd 54,
  sec.gov 53, investor.gov 45, markdown.microlink.io 45, 2dd.pl 45,
  allorigins.hexlet.app 43, markdown.new 35, **vanderbi.lt 29**,
  example.org 24, r.jina.ai 20, api.allorigins.win 17, api.datausa.io 17,
  **uoft.me 15**, httpbin.org 12, fooabc.com 11, jsonhero.io 9, is.gd 7,
  cors.bwa.workers.dev 5, pxweb.gso.gov.vn 5, proxy.cors.sh 4, corsproxy.io 4,
  web.archive.org 2, Various 22.
- New task family: **Vietnam GSO PX-Web statistics API**
  (pxweb.nso.gov.vn + pxweb.gso.gov.vn) — statistical-data extraction beyond
  SEC/census/Data USA.
- Source: https://goto.unm.edu/7t6-o+

### UNM — goto.unm.edu/discvr (public `+` stats)
- Target: library.unm.edu DISC VR page. jqp 61, md.succ.ai 21,
  markdown.new 14, sec.gov 7, **api.census.gov 5**, pure.md 2,
  investor.gov 2. Source: https://goto.unm.edu/discvr+

### UNM — goto.unm.edu/reso (public `+` stats)
- Target: sust.unm.edu ASUNM resolutions review. md.succ.ai 157 (dominant),
  markdown.new 43, r.jina.ai 24, pure.md 15, sec.gov 12, jqp 11,
  investor.gov 6, api.census.gov 5, allorigins 3, **proxymule.com 3**
  (proxy primitive confirmed live). Source: https://goto.unm.edu/reso+

### UNM — goto.unm.edu/urphy21 (public `+` stats)
- Target: unm.zoom.us meeting registration. api.census.gov 50 (dominant),
  jqp 40, investor.gov 12, s3.amazonaws.com 7, sec.gov 6.
  Source: https://goto.unm.edu/urphy21+

### popcat.xyz community — url.popcat.xyz/5vtSk2RG2f + IRZTIxDlZ (public `/info`)
- Both still live, 66 and 83 clicks, both redirect to the SAME ChatGPT
  conversation: chatgpt.com/c/69da0686-9680-8321-ae7c-4aafe7e3f2f4
  (created 2026-04-11 per joshuadavid popcat-wayback export).
- Sources: https://url.popcat.xyz/5vtSk2RG2f/info ,
  https://url.popcat.xyz/IRZTIxDlZ/info

## Pattern read (patterns, not phrases)

4/4 public goto.unm.edu stats pages + the u.ethz.ch page carry the same
signature: the proxy-wrapper toolkit (jqp, pure.md, md.succ.ai, markdown.new,
r.jina.ai, allorigins ×2, corsproxy.io, proxy.cors.sh, cors.bwa.workers.dev,
microlink ×2, proxymule.com) as HTTP Referer values, plus task-family
referrers (sec.gov/investor.gov county.json, api.census.gov, api.datausa.io,
Vietnam PX-Web), plus cross-venue referrers (vanderbi.lt, uoft.me, da.gd,
is.gd, 2dd.pl, jsonhero.io, web.archive.org). The agents' tooling sent these
as Referer headers when requesting the short links; YOURLS logged them
verbatim — a passive, operator-side fingerprint of the whole toolkit on
official university infrastructure. June-18 best-day spikes match the cohort.

Independent corroboration: hamzah2304/messageboardauditbench public benchmark
reports document the same toolkit (jqp as "serverless jq processor" on
sec.gov/files/county.json; 19,159 proxy chains: 11,086 2-hop jqp→target,
7,768 3-hop jqp→allorigins→target, 303 4-hop jqp→pure.md→md.succ.ai→target,
2 5-hop recursive chains stamped 2026-06-18T21:01:20Z/21:03:28Z) and
explicitly name **vanderbi.lt / is.gd / tinyurl shortlinks inside jqp chains**:
"a Vanderbilt shortlink wraps the real source, which is fed to the jq proxy
for server-side extraction — obscuring the origin."

## Restricted / negative (not in Elastic)

- uoft.me `+` stats pages are login-walled (instance policy) — passive only.
  Agent slugs per joshuadavid pages.jsonl: amass932899504, maagentxyz99999,
  mafresh91011, utmace, zzagent740558 (clear agent-grammar handles).
- goto.unm.edu/apdt9_+ does not resolve live (falls through to info page).
- t.mdcdev.me: open-creation YOURLS instance (public front page) — no slugs
  known; no link creation attempted.
- Vanderbilt vanderbi.lt: restricted; covered passively in
  data/vanderbilt-shortener/.

## Dataset

data/university-shorteners/: 7 evidence files + PROVENANCE.md + SHA256SUMS +
university-shorteners.jsonl + pattern-sweep.json + progress.log +
build_dataset.py. Ingest: scripts/es_ingest_university_shorteners.py
(index `university-shorteners`, 7 docs, event.dataset.keyword verified,
zero unexpected top-level fields).
