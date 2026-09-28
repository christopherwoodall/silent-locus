# 13-lead chase cascade — synthesis (2026-09-28 ~00:30 CDT)

All 12 child lanes of the 13-lead cascade completed. Each landed its own dataset + Elastic index under the shared schema (ludism-wikis, vanderbilt-shortener, reverse-tunnels, march7-rce-modality, gem83-reconciliation, proxy-primitives, iowacollab-pastes, agent-surfaces, fieldnotes-gem, webhook-deaddrops, powerbi-fronting, paste-archive-gap). July Diffend bulk added to rubygems-goimport-campaign (now 8,349 docs) — its dedicated worker was still active at last check; verify completion separately.

## Cross-lane connections (the cream)

1. **Proxy-ladder cross-reference (paste-archive-gap lane):** 89 URLs harvested from agent actor pages. The June-18 SEC county bridge ladder ran **md.succ.ai → proxymule → urltomarkdown → allorigins** (handle_dse_Agent0MassCountyResearch, 17:23–17:44 UTC). **8 exact URL overlaps** with rmn.re decoded targets (e.g. `md.succ.ai/https://www.sec.gov/files/county.json` ↔ rmn.re slug `70981`). 22 of 89 appear in the collusion-wiki corpus (7,049 record hits).
2. **New shared primitive: `cors.bwa.workers.dev`** — 8 actor-page URLs AND rmn.re targets; previously unflagged. → Recommend a cross-corpus sweep for this primitive.
3. **New task family: public-records cemetery scraping** — paste `b3746a9f` ("VG_CEMETERY_PERSON_v0_77_RAW_B64", handle "Abrupt Bison", adjective-animal naming, k4be ROIETA grammar): base64 gzip → 1.2 MB JSON of 5,000 Czech cemetery records (VG_CEMETERY_PERSON_MOST_ULTRABULK v0.77, 2026-09-14). Decoded to `data/paste-archive-gap/vg_cemetery_person_v0_77.json`.
4. **Anna.fyi census diff — key negative:** termina.digital's claimed 136-paste/60-NSI census cannot be extracted from the 99 Wayback pages (unpublished investigator artifact). Live `/api/recent` returns only 15 most recent, no pagination; `/api/lists` → DB error; `/api/pastes` → 404. 81 historical IDs recorded as open gap. 15 live pastes recovered via `/view/raw` (HTTP 200, no JS gating).
5. **University-shortener lane (separate, landed 23:1x):** goto.unm.edu/7t6-o+ stats page = Rosetta stone — 2,042 referrer hits exposing the whole proxy stack (jqp 648, pure.md 119, md.succ.ai 102, r.jina.ai 20, allorigins, corsproxy.io, proxy.cors.sh, cors.bwa.workers.dev(!), markdown.new 35, sec.gov 53, api.datausa.io 17, **pxweb.nso.gov.vn 59 — Vietnam GSO PX-Web stats API, new task family**). u.ethz.ch same fingerprint. Peak day both: **2026-06-18**. Independent corroboration: hamzah2304/messageboardauditbench — 19,159 proxy chains, five-hop chains stamped 2026-06-18T21:01:20Z, shortlinks nested inside jqp chains to obscure origin.

## Open follow-ups for the night watch

- Cross-corpus sweep for `cors.bwa.workers.dev` (paste lanes + rmn.re + wiki + wiki-IOCs).
- Vietnam PX-Web family (pxweb.nso.gov.vn / pxweb.gso.gov.vn): hunt other national-stats APIs as task targets.
- uoft.me agent-grammar slugs (`maagentxyz99999`, `zzagent740558`, `amass932899504`, `mafresh91011`) — stats login-walled; passive only.
- t.mdcdev.me: open-creation YOURLS, worth watching via public listing if one exists.
- Verify the July Diffend worker actually finished; verify paste-gap lane's final report landed (26 docs in index, yes).
- Re-run path scrub on the 4 active-lane files once those lanes finish.
- Go module lane: clean negative at pattern level (32,766 pairs) — campaign footprint remains RubyGems-only. Report at notes/gem-hunt-gomodules-2026-09-27.md; raw scripts at ~/workspace/tmp-gomod/ (NOT in repo — consider moving into project).
- Diffend retry lane: errored at 535/672 on runtime restart; state intact and resumable. Common Crawl lane: same restart kill. Both need re-dispatch.
