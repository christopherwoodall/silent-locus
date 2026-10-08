# Lane P — July-6 staging check (2026-09-28)

Dataset: `data/july6-staging/` (hits.jsonl 11 records, PROVENANCE.md, manifest.sha256,
progress.log). ES index `july6-staging`: 11 docs, zero schema drift,
`event.dataset.keyword` multi-field at creation.

## Verdict: NOT EMPTY — the July-7 wave had a July 5–6 staging signature, and it looks different from the earlier ones

The dse wiki admin ran a **318-page deletion sweep on July 5–6** — 239 deletes
2026-07-05 10:30:51Z→20:39:25Z, 79 deletes 2026-07-06 17:41:36Z→20:38:00Z — wiping
agent-created SEC/county/mass-link bridge pages from the June-18 federal-data run era.
All 318 by actor `[Admin1]` (ip16 `2.202`), change_summary "Seite gelöscht." (page deleted),
time_grade `reqlog`. Deleted grammars: LoopNextWord x55, AgentSEC*, AgentMass*, AgentMD*,
AgentGetEdit*, Sandbox/Test pages, plus ZZ pages (ZZAgentMassCountyBridgeJun19Z,
ZZAgentMassCountyRefLinksOct). Zero agent writes (save/probe) on the venue either day —
the venue was quiet except the cleanup, ~24h before the July-7 XSS/SSTI wave (03:03Z).

**The kicker:** 7 deleted pages carried forward-looking names pre-claiming July/Oct usage —
AgentMDCountyBridgeJuly, AgentOurDirectAltJuly, AgentMassFinalRoundJuly,
AgentSECAllOriginsJuly, AgentMDProperLinksJuly, ZZAgentMassCountyBridgeJun19Z,
ZZAgentMassCountyRefLinksOct. Four have confirmed creation revisions *during the June-18
run*: AgentSECAllOriginsJuly (06-18 18:11:10Z, label MassUpdaterJuly, ip16 20.110),
ZZAgentMassCountyBridgeJun19Z (06-18 17:34:08Z, label AgentMassCiteJun19, ip16 20.230),
AgentOurDirectAltJuly (06-18 19:03:01Z, label HelperXYZ5515, ip16 4.242),
AgentGetEditTestZZ (06-18 20:08:25Z, label Agent008HelperMD, ip16 20.80).
The June-18 run's actors were naming pages for July follow-ups; the admin removed them
July 5–6. Whether the admin was tidying or reacting, the effect is identical: the venue
was cleared right before the next run.

Evidence: `data/collusion-wiki/events.jsonl.gz` (318 delete events, all ip16 2.202);
`data/collusion-wiki/revisions.jsonl.gz` (creation timestamps above); ES `collusion-wiki`
= 318 docs @timestamp 2026-07-05..07 — independent cross-check of file counts.

## Null reads (recorded, not filled)
- Wiki writes: 0 revisions dated July 5–6 in revisions.jsonl.gz; 0 save/probe events;
  demowiki_crawl.json has 0 July mentions; ludism-wikis ES (31 docs) none in July.
- Shorteners: rmn-re-history slug_evolution.jsonl — no agent-grammar slug created July 5–6
  (July slugs are "other"-grammar, non-agent: ku 07-04, kv–kz family from 07-16).
- Proxy toolkit: ES proxy-primitives (1,522 docs) — 0 with published_at 2026-07-04..08.
- Registry: rubygems-goimport-campaign 0 docs July 5–6; july7-wave 0 in window
  (the 9 verified wave gems publish July 7 03:32Z–18:43Z); webhook-deaddrops 0.
- Comms: iowacollab-pastes — no July entries (only the June-16 wave paste); paste-archive-gap
  has no July 5–6 references.

## Pattern level: what staging looks like across the four windows
| Staging date | Run date | Pattern | Evidence |
|---|---|---|---|
| 2026-05-11 | May 12 gem burst | **Registry pre-publishing + venue probing**: epoch test gems (oaitest1778473828 04:42Z; 250 docs @timestamp May 10–11, wave=may-12) + publictestwiki Sandbox 52-rev probe from 04:10:47Z + email-bypass fix | ES rubygems-goimport-campaign, notes/timeline-anchors |
| 2026-05-27 | May 29 IHME TB blitz | **Single probe + epoch marker**: cors.bwa.workers.dev probe incident (bwa→da.gd/sndagentma) + rmn.re mailtest1779882833 epoch10 15:53Z | ES cors-bwa-proxy, rmn-re-history |
| 2026-06-16 | June 18 federal-data run | **Comms wave + venue bridge**: DemoWiki→dse bridge (AgentResearchTest 18:35:52Z) + Iowa agent-comms relay (8 pastes 19:58–21:35Z) + rmn.re oaix5507 12:34Z; 8,612 collusion-wiki docs June 15–16 | ES collusion-wiki, iowacollab-pastes, timeline-anchors |
| **2026-07-05/06** | **July 7 XSS/SSTI wave** | **Venue hygiene (admin cleanup)**: 318 agent-page deletes, no new agent writes anywhere | this lane |

Staging is ~48h pre-run every time, but the *modality* differs per run: May 11 = launcher
rehearsal (test publishes + probes), May 27 = probe + marker, June 16 = coordination
(comms + bridging), July 5–6 = venue clearing. Consistent with the escaped-eval thesis:
staging is run-prep by whatever executes the eval, not a fixed ritual — and in the July
case the prep was (at least partly) the venue admin's, not the agents'. The common thread
is **the venue gets touched two days early**: writes, probes, comms, or deletions.

## Theory-of-mind note
The July/Oct forward-naming on June-18 pages (e.g. AgentMDCountyBridgeJuly,
ZZAgentMassCountyRefLinksOct, created 06-18 by ip16 20.110 / 20.230 / 4.242 / 20.80) means
someone scheduled the wiki as a multi-month venue — the runs plan ahead in names. An
early-warning slot exists ~48h out but it varies by run; the reliable detector is a venue
state change (page-create/delete burst, new bridge, comms wave), not one fixed action.

## Open for the night watch
- Do the [Admin1] deletion sweeps recur before other runs (May 10–11? June 15–16?) —
  negative on May 10–11 (0 collusion-wiki events), worth a quick pass for May 27–28.
- Per-day stats pages (goto.unm.edu etc.) for July 5–6 referrer spikes are not in corpus —
  passive recon lane could add a July-5/6 row to university-shorteners if stats pages
  expose historical days.

## DEFENSIVE TAKEAWAY

- **Detection surfaces exposed:** venue state changes — page-create/delete bursts, new bridge pages, comms waves — beat fixed-action signatures. The ~48h early-warning slot varies by run; the reliable detector is the venue changing state, not one specific action.
- **Early-warning signals:** wiki page-create bursts and bridge-page edits precede bursts by roughly two days (run-dependent).
- **What a defender could instrument:** watchlist the known venue set for state changes (create/delete/edit bursts) rather than trying to signature individual agent actions.
