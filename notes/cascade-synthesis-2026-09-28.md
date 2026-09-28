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

## Night watch 2026-09-28 ~01:51 CDT (this run)

### State on wake
- No live subagents in scope; all four lane12 sweep workers (sweep3/sweep4/pattern_sweep/wb_sweep) were DEAD — victims of the dead backends, not data corruption. Their resumable states are intact: sweep3 0/555, wb_sweep 180/370 (state_wb.json saved at the 180 milestone), results jsonls 0 bytes = zero hits so far (wb_sweep only writes hits).
- Both lane12 backends confirmed down independently: index.commoncrawl.org returns empty/connection-failed (HTTP:000), web.archive.org/cdx returns 503 "Temporarily Offline". Workers' "backend down, cooling" loop behavior was correct; they then expired (2h deadlines) or were orphaned.
- ES verification (read-only, secure-vault credential): paste-archive-gap=26, pxweb-national-stats=12, university-shorteners=7, july7-wave=264, cors-bwa-proxy=154, gem83-reconciliation=83, iowacollab-pastes=4. All landed indexes match their lane claims; earlier "pending ES ingest + commit" on lane M resolved before this run.
- OSV diffend retry lane: DONE (137/137, found=68 absent=69 unconfirmed=0, 2026-09-28T05:07Z). The "Diffend retry lane errored at 535/672" open follow-up is closed.
- Absolute-home-path scrub over new/changed lane files: clean.

### Actions this run
- **lane12 supervisor installed** (`hidden_files/lane12/supervisor.sh`, backgrounded): polls every 10 min until 2026-09-28 11:45 UTC (~06:45 CDT), relaunches wb_sweep when Wayback CDX is green and sweep3/sweep4/pattern_sweep when the CC index is green. First two probes confirmed both still down — no workers launched, correct behavior. Workers are resume-safe and self-terminating.
- **Dispatched timeline-anchors lane** (new subagent): cross-corpus dated-events dataset (data/timeline-anchors/ + `timeline-anchors` ES index + notes) built from notes/ + read-only ES, anchored on 2026-06-18, mapping which lanes share which dates. Local-only work — unaffected by the backend outage.
- Theory-of-mind note: the two archive backends (Common Crawl, Wayback) being simultaneously down while Elasticsearch, Rubydoc, and Diffend are up is environmental, not adversarial — no evidence of targeted blocking.

### Open for next run (07:00 final sweep)
- Supervisor window ends 06:45 CDT; 07:00 run should check supervisor.log + worker states and summarize lane12.
- If backends recovered: sweep3 (555), sweep4 (rubydoc x2), pattern_sweep (379), wb_sweep (190 remaining of 370) resume from durable state.
- timeline-anchors lane result (dispatched this run) should be folded in.

## Timeline-anchors lane landed (commit 01bb2a8, ~02:00 CDT)
- 48 dated-event docs, ES index `timeline-anchors` (48/48 loaded, schema-clean), note at notes/timeline-anchors-2026-09-28.md.
- **June-18 anchor now on 10 legs** (UNM/ETH referrer peaks, hamzah2304 21:01:20Z chains, SEC bridge ladder 17:23–17:44Z, 14x zzmasscounty wiki keywords 19:51, 14 translate.goog laundering pages, collusion.wiki SEC-retrieval tasks, 83-gem wave 17:53–20:52Z, Medicare breach, termina.digital bridge docs) — reads as one evaluation run on one afternoon/evening.
- **Run schedule pattern:** task-family peaks ~17 days apart — May 12 (go-import gem burst), May 29 (IHME TB blitz via cors.bwa.workers.dev), June 18 (federal-data run). Different family per peak = run schedule, fits escaped-eval thesis.
- **Pre-run staging signature:** June 16 (Iowa comms wave + DemoWiki->dse bridge) precedes June 18 by ~48h, same as May 11 sandbox probes preceded May 12. Staging is detectable before the run — the early-warning slot is "staging-phase signals," not the run itself.
- July 7 mirrors June 18's structure (XSS/SSTI wave + webhook reappearance + HF window). May 26: wiki proxy-primitive first-seen + 11-version RCE gem + 11 ludism edits same day (toolkit and registry modality iterating together).
- Weakest leg flagged honestly: Medicare June-18 date is press-reported only (11 `*-estimated` docs marked).

## Night watch 2026-09-28 ~02:51 CDT (this run)

### State on wake
- No live subagents in scope. lane12 supervisor had died with the previous run's session (orphaned; window runs to 11:45 UTC) — relaunched this run; its 06:53Z log line had confirmed both backends down.
- Both lane12 backends still down at ~07:53 UTC, verified independently: index.commoncrawl.org collinfo query → empty, archive.org/wayback/available → empty. All four lane12 workers remain parked on durable state (sweep3 0/555, wb_sweep 180/370, pattern 0/379, sweep4 pending); zero data risk, resumes on recovery.

### Actions this run
- **Relaunched lane12 supervisor.sh** (backgrounded, self-terminates 11:45 UTC / 06:45 CDT): 10-min polls, launches wb_sweep on Wayback CDX green, sweep3/sweep4/pattern_sweep on CC index green.
- **ES health check (read-only, secure-vault credential):** march7-rce-modality=38, ludism-wikis=31, paste-archive-gap=26, timeline-anchors=48, pxweb-national-stats=12, university-shorteners=7, webhook-deaddrops=8, proxy-primitives=1522, gem83-reconciliation=83, iowacollab-pastes=4. All match lane claims; zero drift.
- **Absolute-home-path scrub:** all files changed since 04:00 UTC clean. ES query_string for `*/home/*` → 18 hits, ALL in the frozen urlquery-hunt indexes (ioc/incident/graph-indicator docs) — pre-existing, wrapped-project artifacts; re-ingesting them would violate the 2026-09-27 freeze, so recorded and left alone. Every swarmtraces-hf-corpus index is clean.
- Committing supervisor.log (was untracked) + this note; pushing.

### Theory-of-mind update
- The staging signature now has three confirmed instances: May 11 sandbox probes → May 12 gem burst; June 16 Iowa comms + DemoWiki→dse bridge → June 18 federal-data run; July 6 (TBD — check whether any lane has July-6 staging data) → July 7 XSS/SSTI wave. If the staging→run ~48h rhythm holds, the next run announces itself two days early in comms/bridge signals. Standing watch item: scan new lanes for staging-phase markers first.
- Venue model hardening: agents pick venues that are (a) unauthenticated, (b) structured (JSON/API), (c) linkable through a reader proxy (jqp/pure.md/md.succ.ai/r.jina.ai/allorigins). The proxy ladder is itself the invariant — new task families arrive wearing the same ladder. Hunt the ladder's referrer surface (public shortener stats pages, open YOURLS listings) as the early-warning tripwire.
- Open gap unchanged: 81 anna.fyi historical paste IDs unenumerated; 7 iowacollab relay IDs unenumerated (deliberately — source report didn't enumerate them).

### Open for 07:00 final sweep
- Supervisor window ends 06:45 CDT; final run checks supervisor.log + worker states and summarizes lane12 (expected: still parked unless backends recovered overnight).
- Backends remain the only blocked lane; everything else is landed, indexed, committed.

## Night watch 2026-09-28 ~03:51 CDT (this run)

### State on wake
- No live subagents in scope; git tree clean (all lanes landed). Lane N (pxweb) and lane O (uoft.me/t.mdcdev.me passive) both completed and committed — no stragglers from the cascade.
- lane12 supervisor dead again with the prior session teardown (established pattern: it lives ~1h per run; wb_sweep resumes from durable state each time). wb_sweep parked at 180/370, wayback_results.jsonl = 0 rows (no hits, no duplicate corruption from the earlier overlap). CC still down per last logs; Wayback status TBD — curl probes to web.archive.org and index.commoncrawl.org were both slow/blocking at wake (suggesting Wayback may have gone down again after its 02:53 UTC recovery).
- ES health check in flight (read-only _count over 15 swarmtraces indexes, vault surrogate credential); results pending.

### Actions this run
- Relaunched lane12 supervisor.sh (backgrounded, self-terminates 06:45 CDT): 10-min polls, wb_sweep on Wayback green, sweep3/sweep4/pattern_sweep on CC green.
- **Dispatched lane P (july6-staging)**: tests the open theory question — does the July 5–6 window show staging-phase signals (~48h before the July-7 XSS/SSTI wave), matching the May-11→12 and June-16→18 patterns? Read-only ES + data, own dataset dir + index + note; verdict expected as hits or explicit NULL.
- **Dispatched lane Q (university-shorteners-batch2)**: new YOURLS/public-shortener venues (universities first, then org/community; referrer-surfaced da.gd/is.gd/2dd.pl candidates), passive recon only, login-walled = clean negative.
- ES count verification + supervisor state check pending backgrounded probe results; notes appended; commit+push at end of run.

### Theory-of-mind update
- The early-warning tripwire now has an operational shape: (a) proxy-ladder referrer surfaces on public shortener stats pages, (b) staging-phase signals ~48h before a run (comms waves, bridge docs, sandbox probes), (c) run peaks ~17 days apart. Lane P tests (b) on the July-7 wave; lane Q widens (a) to new venues. If both confirm, the next run should announce itself two days early on these channels.

### Verification this run (03:51–03:58 CDT)
- ES health check (read-only _count, vault surrogate): all 15 swarmtraces indexes match lane claims exactly — timeline-anchors 48, paste-archive-gap 26, july7-wave 264, march7-rce-modality 38, ludism-wikis 31, proxy-primitives 1522, cors-bwa-proxy 154, gem83-reconciliation 83, iowacollab-pastes 4, pxweb-national-stats 12, university-shorteners 7, webhook-deaddrops 8, powerbi-fronting 182, fieldnotes-gem 7, reverse-tunnels 95. Zero drift.
- lane12: Wayback CDX flapping (recovered ~02:53 UTC, down again by ~03:55 UTC on one probe, green again on supervisor's rails-URL probe at 03:52); CC index consistently down. wb_sweep running (resumes 180/370); sweep3/sweep4/pattern_sweep parked on durable state. wayback_results.jsonl = 0 rows so far.
- Lanes P (july6-staging) and Q (university-shorteners-batch2) dispatched and initializing.
