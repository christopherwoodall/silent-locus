# bullfincher.io/sec-proxy — Lane 3 OSINT (2026-10-05)

## What bullfincher.io is (verified from search-index snippets)

Executive-compensation data site: per-company pages like
`/companies/equinix/ceo-salary`, `/companies/walmart/ceo-salary`,
`/companies/amazoncom/ceo-salary` — tables of CEO/CFO pay (base,
incentive, stock awards) by year, sourced from SEC filings. Pages
indexed fresh (crawls 1–13 days old as of 2026-10-05) → **site is
alive now**. "Fintech, Austin TX" per task brief — NOT independently
verified by Lane 3; treat as unverified.

## What /sec-proxy is (verified from search-index snippets)

A `?url=` endpoint that fetches an arbitrary URL and renders the
content as text. Page title: **"Sec Proxy"**. Indexed instances
(search engine crawled the rendered output):

- `bullfincher.io/sec-proxy?url=...sec.gov/Archives/edgar/data/70858/.../bofaannualreport2025.pdf` → rendered Bank of America 2025 10-K text (crawl ~147 days ago ≈ May 2026)
- `.../data/55785/.../kmb4554211-ars.pdf` → Kimberly-Clark 2025 ARS text
- `.../data/8670/.../adp014341-ars.pdf` → ADP ARS text
- `.../data/1571996/.../d836850dars.pdf` → Dell ARS text

Characterization: **open URL fetcher / PDF-to-text renderer**, no
visible access control in indexed examples; search engine indexes
arbitrary proxied content (each proxied filing gets its own indexed
URL). Looks like an intentional site feature (titled page, used for
the site's own SEC-filing sourcing pipeline) that the swarm
repurposed as a retrieval gadget — same adoption pattern as
jqp.vercel.app (pre-existing public utility, not agent-built).
Whether it was *designed* as an open proxy vs. an internal tool that
leaks: cannot determine from public sources. No docs found.

Liveness: search-index evidence only (no live probing per URL OPSEC).
Last indexed crawl of a sec-proxy URL ≈ May 2026; site itself crawled
within days → endpoint presumed live, graded as search-index-inferred.

## Swarm use (from joshuadavid/wikiagentswarminvestigation corpus)

- **First seen: k4be 2026-02-26 14:49:24 UTC**, paste `5329a841`:
  `bullfincher.io/sec-proxy?url=…sec.gov…hum-20151231x10k.htm` with
  extracted Humana stock-return table; two reformatted summaries
  within three minutes. Classified "Humana 10-K stock returns via
  bullfincher.io/sec-proxy (new CORS proxy)".
- Earliest proxy gadget in the whole corpus timeline — predates the
  May–June proxy ladder (jqp/md.succ.ai/pure.md) by ~3 months.
- Caveat (run-1): creation field captured later; no independent
  February capture; one agent or human could have made all three posts.

## Proxy-gadget family (first-seen dates from joshuadavid corpus)

| Gadget | First seen (corpus) | Context |
|---|---|---|
| bullfincher.io/sec-proxy | **2026-02-26** 14:49:24 UTC (k4be `5329a841`) | Humana 10-K; earliest gadget overall |
| jqp.vercel.app/api/v0?url= | **2026-05-28** 13:03:06 UTC (dse `CharlestonPartFourRefsX@1`) | jq-over-HTTP on IIIF manifest; underlying OSS `sighrobot/jqp` created 2022-05-14 (our dataset `data/2022-05-14-jqp-vercel`) |
| md.succ.ai/ | **2026-05-11** (Popcat `oaimdbrit62`, service metadata — weaker dating); **2026-05-29** in ProWiki (`StartSeite@235`) | HTML→Markdown API; underlying repo `vinaes/md-succ-ai` first commit 2026-02-14 (our dataset `data/2026-02-14-md-succ-ai`) |
| pure.md/ | **2026-05-28** 23:58 UTC (Yahoo TWLO Wayback capture); 2026-06-01 14:57 UTC (Clark newsletter) | doc→markdown renderer; chained with jqp (`jqp → pure.md` URL-of-URL nesting, triple-encoded) |
| markdown.new/ | **2026-05-26** (`Node50166915Test@1` proxy test); 2026-05-13 linuxiarz `d7632bc3` (`markdown.new → is.gd` codes) | markdown proxy |
| 2md.link / is.gd | **2026-05-13** (linuxiarz `d7632bc3` `ReferenceLinks0`) | shortlink + markdown |
| r.jina.ai | **2026-06-18** (`AgentCountyExploreJune18AA` nesting ladder: JinaDouble/Triple/QuadTest/Mix) | reader proxy, nested |
| corsproxy.io / api.codetabs.com/v1/proxy / microlink | June 2026 (Wayback SPN captures of swarm proxy fetches) | Wayback "Save Page Now" captured the swarm's own proxy fetches |
| cors.trigox.workers.dev / arquivo.pt | 2026-01 / 2026-07–08 (etherpad.wikimedia.org `Test<Mon>Actor<NN>` monthly proxy-test pads) | year-long proxy-test series, separate lane |
| allorigins.hexlet.app | 2026-06-20 (`AgentVarYearsFixJune20X` dot-encoding sweep) | CORS proxy variant |
| telegra.ph/Test-Link | listed in run-1 proxy set (subagent_prompt.md) | smoke-test target |

Pattern: the swarm adopted a LADDER of public reader/proxy gadgets
(markdown renderers → CORS proxies → jq filters → archive), chaining
them URL-inside-URL with one percent-encoding layer per hop. All
pre-existing public utilities; none agent-built.

## Does bullfincher appear in our own corpora?

- PENDING: background grep over `~/workspace/silent-locus/data/` for
  `bullfincher` / `thecolony` (session proc_f8d99ac0b3f2). Update on
  delivery.
- Target file named in brief: `data/2026-10-01-oai-tag-sweep/events.jsonl`.

## Sources

- Search-index snippets: `bullfincher.io/sec-proxy?url=…` (4 indexed instances), `bullfincher.io/companies/*/ceo-salary`
- https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/research/swarm-followup/early-dates.md (2026-02-26 Humana)
- https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/research/swarm-mechanisms/gadgets-and-models.md
- https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/swarm-behavior-timeline.md
- https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/analyses/paste-sites-classify/hosts_summary.md
- https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/analyses/paste-sites-classify/subagent_prompt.md
- https://github.com/swarm-ai-research/wiki-agent-swarm-incident/blob/HEAD/analysis/what-the-archive-remembers.md (Wayback SPN captures)
- https://github.com/kmad/agent-swarm-forensics/blob/HEAD/docs/decode/03-code-inventory.md (pure.md + jqp chaining)
- https://labs.zenity.io/post/rogue-ai-agents-swarm-encoded-url-messages-laundering (proxy ladder in encoded URL messages)
- Our datasets: `data/2022-05-14-jqp-vercel/PROVENANCE.md`, `data/2026-02-14-md-succ-ai/PROVENANCE.md`

NOT fetched/probed: bullfincher.io (URL OPSEC).
