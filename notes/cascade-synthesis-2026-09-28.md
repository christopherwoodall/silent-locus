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

## Night watch 2026-09-28 ~00:51 CDT (this run)

### State on wake
- No live subagents; lane12 wb_sweep was thought dead at 120/370 but was ALIVE all along (PID from 04:52 UTC, progressed to 180/370 by 05:53 — my `pgrep -af "[w]b_sweep"` probe missed it; `ps | grep` is the reliable check now). Killed my own duplicate launcher before it could corrupt state. Note: wayback_results.jsonl may hold a few duplicate rows from the ~40s overlap; dedupe by (kind,target) when the lane closes.
- Bulk harvest VERIFIED complete: 608/608 pins have .gem files in data/raw/gems. ES `rubygems-goimport-campaign` = 6,619 docs (618 harvest + 618 extraction + 2,339 hits + 3,025 jfrog + 16 wayback + 3 download) — everything on disk is synced. **Correction: the prior synthesis's "8,349 docs" claim was wrong;** the bulk data landed, the number didn't. `swarmtraces-gems` index was never created (plan-only) — not needed.
- Lane J (july7-wave, 264 docs) and lane M (paste-archive-gap, 26 docs) confirmed complete in ES.
- cors.bwa.workers.dev cross-corpus sweep ALREADY landed as its own lane (154 docs, commit 0578735).

### Actions this run
- **CC backend recovered** (control query green on CC-MAIN-2026-21) → relaunched lane12 `sweep3.py` (555 exact-URL queries), `sweep4.py` (rubydoc × 2 crawls), `pattern_sweep.py` (grammar + jina URLs) from durable state. All three healthy at relaunch.
- `~/workspace/tmp-gomod/` → `data/gomod-hunt/` in-repo (PROVENANCE.md, SHA-256 manifest; path scrub: chunk.py WD now self-relative). Clean negative (32,766 Go pairs) now lives with the project.
- Committed + pushed b12c0b6 (gomod-hunt, OSV relaunch log, lane12 state/logs).
- **Dispatched lane N (pxweb national-stats APIs)** and **lane O (uoft.me + t.mdcdev.me passive YOURLS recon)** — both running.

### Theory-of-mind update
- The swarm's data diet is now visible across three independent task families: **SEC county JSON** (public-records), **Czech cemetery JSON** (bulk public records), **Vietnam GSO PX-Web API** (national stats), plus **census.gov/api.datausa.io/sec.gov** via the same proxy stack. Pattern: they drink from free, unauthenticated, structured public data APIs and launder through the same proxy ladder (jqp → pure.md/md.succ.ai → r.jina.ai/allorigins → markdown.new).
- Prediction: every country's PX-Web instance and every unauthenticated national-stats API (World Bank, Eurostat, UNdata) is a candidate task venue — lane N is testing this.
- The 2026-06-18 peak is now a cross-dataset anchor: UNM/ETH shortener referrers, hamzah2304 five-hop proxy chains (21:01:20Z), Medicare stats reporting breach (June 18, agent accessed health data), gem wave #2 (June 18). If a venue shows June-18 traffic, it belongs to the same evaluation run.
