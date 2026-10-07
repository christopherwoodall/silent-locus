# FINDINGS — account-profiler (wikipedia-lane)
Branch: `wikipedia-edit-hunt-2026-10-06`. Updated incrementally.

Every claim graded: OBSERVED (bytes in hand) / INFERENCE (reasoned link) / UPSTREAM (someone else's claim).

## SHAPE-SCORES — burst clusters ranked by incident-shape similarity (2026-10-06)

Incident shape profile (from the 28 incident accounts + 54 edits):
- F1: ~2026-* temporary account format
- F2: Sandbox-edit bursts with May 10 / May 27 / Jun 25 timing geometry (sandbox "test"/"Temporary technical sandbox initialization")
- F3: Web2Cit config targeting (sandbox→live workflow, geodata/geocoding targets)
- F4: 10-minute creation bursts (Jun-25 incubator: 8 accounts in ~7 min)
- F5: ~4-minute micro-bursts (testwiki Sep-30 pattern: 5 accounts in 4 min)
Threshold: ≥3/5 shared features → zoom-in lane. Ranked by shape score, NOT account count.

| Rank | Cluster | n | F1 temp | F2 sandbox+timing | F3 Web2Cit | F4 10min burst | F5 4min micro | Score | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| — | BURST-2 incubatorwiki 2026-06-25 | 8 | ✓ | ✓ | ✓ | ✓ | ~ | 4.5/5 | REFERENCE (is the incident) |
| 1 | BURST-1 testwiki 2026-09-30 | 5 | ✓ | ✗ (Twinkle test page, Sep 30) | ✗ | ✓ | ✓ | 3/5 | ZOOM-IN → shape-partial lead |
| 2 | mediawikiwiki 2026-05-27T16:50 | 5 | ✓ | ~ (May-27 timing ✓, but 4/5 dormant, no sandbox) | ✗ | ✓ | ✗ | 2.5/5 | Below threshold; timing noted |
| 3 | BURST-3 mediawikiwiki 05-18/05-21 | 86 | ✓ | ✗ (95% dormant, no sandbox edits) | ✗ | ✓ | ✗ | 2/5 | CLEAN NEGATIVE (shape) |
| 3 | BURST-4 simplewiki 7× n=10 | 70 | ✓ | ✗ | ✗ | ✓ | ✗ | 2/5 | CLEAN NEGATIVE (shape) |
| 3 | BURST-5 bgwiki 12× n=5–6 | 63 | ✓ | ✗ (mostly active 1–17 edits, not sandbox) | ✗ | ✓ | ✗ | 2/5 | CLEAN NEGATIVE (shape) |
| 3 | BURST-6 commonswiki 5× n=15–18 | 79 | ✓ | ✗ (76% dormant, no sandbox edits) | ✗ | ✓ | ✗ | 2/5 | CLEAN NEGATIVE (shape) |

Cross-shape vs corpus fleets (explicit):
- zz=oai fleets: URL-grammar based (zz=oai<digits>). Zero shared grammar with temp-account bursts (no URLs involved). DIVERGENT on all clusters.
- Shrekiolous/Mutark (Meta sandbox-burst crews, wiki-surgeon): shared sandbox-burst behavior (F2-like) but Mutark accounts were globally locked vandal-probe crew; incident accounts unlocked, temp-format, config-targeting. Our BURST-1/3/4/5 lack the sandbox-burst behavior itself → DIVERGENT.
- Sept-2026 probe clusters (Jndufjdtidd et al.): shared burst structure only; different timing, targets, account format. DIVERGENT.

### ZOOM-IN: BURST-1 (testwiki 2026-09-30, 3/5 shape match)
Full contribs pulled for all 5 accounts (raw/contribs-burst1-testwiki-2026-*.json):
- All 5 edits target "Twinkle test page" (revids 765142–765150, consecutive). First creates page with `{{subst:Deletion sorting/multi|Lists|sig=~~~~}}`; rest are blank/touch edits.
- Sandbox edits: NONE. Web2Cit/config targeting: NONE. Probe markers (zz=, tok=, uqscan): NONE.
- Shape assessment after zoom-in: shares F1 (temp), F4 (10-min burst), F5 (4-min micro) — the CREATION geometry matches the incident's micro-burst shape, but the EDIT behavior (Twinkle testing vs sandbox probing) and timing (Sep 30 vs incident waves) diverge.
- Verdict: SHAPE-PARTIAL LEAD (3/5). Creation-burst geometry is incident-like; edit behavior is not. Referred to chunk divers for the Twinkle angle. NOT claimed as incident-related.

### CLEAN NEGATIVES (shape) — filed with feature comparisons
- **BURST-3 mediawikiwiki 2026-05-18/05-21 (86 accounts, 95% dormant):** shares F1 (temp format) + F4 (creation bursts); lacks F2 (no sandbox edits — dormant), F3 (no config targeting), F5 (bursts span 40min–2h, not micro). Does not rhyme with zz=oai (no grammar), Mutark (no sandbox bursts, unlocked), or Sept-2026 probes (different structure). FILED NEGATIVE on shape. (Dormancy remains a separate lead for infrastructure reasons, not shape.)
- **BURST-4 simplewiki (7× n=10):** shares F1 + F4; lacks F2, F3, F5. Recurring fixed-n=10 suggests scheduled process, not incident geometry. FILED NEGATIVE.
- **BURST-5 bgwiki (12× n=5–6):** shares F1 + F4; lacks F2 (mostly active, not sandbox), F3, F5. FILED NEGATIVE.
- **BURST-6 commonswiki (5× n=15–18: 2026-04-14, 04-22, 06-30, 09-21, 09-30):** shares F1 + F4; lacks F2 (76% dormant, no sandbox edits observed), F3, F5 (n=15–18 over 10 min, not 4-min micro). None align with May-13 incident wave. Does not rhyme with zz=oai, Mutark, or Sept-2026 probes. FILED NEGATIVE on shape. (60 dormant accounts = infrastructure lead, not shape.)

### Dormant-account leads (carrying shape scores)
- mediawikiwiki May-18/21 dormant (95 accounts): shape 2/5 — lead on DORMANCY (infrastructure), not shape.
- simplewiki dormant (~30 across bursts): shape 2/5 — lead on dormancy.
- bgwiki dormant (27): shape 2/5 — weak.
- BURST-1 (0 dormant; all edited): shape 3/5 — lead on SHAPE.
Full per-account dormancy: raw/dormancy-checks/dormancy.tsv.

## Burst clustering — results (incremental)

### BURST-1 (LEAD): testwiki 2026-09-30T06:33:32–06:37:19Z, n=5 — OBSERVED
- Accounts: ~2026-52540-64, ~2026-52595-59, ~2026-52476-76, ~2026-52359-23, ~2026-52556-21 (created within 4 min; testwiki background ≈ 0.03 temp creations/10min bin, so 5 in one bin is a >150σ outlier).
- NOT dormant: editcount=1 each (dormancy.tsv). Each made exactly ONE edit, all to "Twinkle test page" (revids 765142–765150, consecutive): first created the page with `{{subst:Deletion sorting/multi|Lists|sig=~~~~}}`, rest blanked/touched it. Raw: raw/contribs-burst1-testwiki-2026-*.json (5 files).
- Does NOT align with known incident edit bursts (May 10 / May 27 / Jun 25) — recorded as a lead per directive, not a negative.
- Assessment: coordinated multi-session activity (5 distinct temp cookies, same page, consecutive revids within 4 min) is agent-shaped OR a logged-out human dev testing Twinkle's deletion-sorting. INFERENCE either way; the Twinkle-test content differs from the incident's sandbox-"test" grammar. Referred to chunk divers.
- Note: account numbers non-sequential (52359–52595 spread) within the 4-min window, unlike the Jun-25 incubator wave (36686→36920 sequential in 30 min). Temp-ID sequencing is not a reliable fleet clock — OBSERVED counterexample.

### test2wiki (Apr–Sep complete): zero bursts (132 temp creations, max bin < 5).

### BURST-3 (LEAD, STRONGEST): mediawikiwiki dormant clusters, May 18 & May 21 — OBSERVED
- 12 bursts total on mediawikiwiki (Apr–Sep). Standouts:
  - 2026-05-18: FIVE bursts 08:40–10:50Z, 49 accounts in ~2h (n=14,8,8,12,7). Dormant: 10+7+6+9+7 = 39/49.
  - 2026-05-21: TWO bursts 01:10–01:50Z, 37 accounts in ~40 min (n=13, n=24). Dormant: 13/13 and 24/24 — ALL 37 dormant.
  - 2026-05-27T16:50Z n=5 (4 dormant) — same calendar day as the incident May-27 edit wave, but on mediawikiwiki (incident May-27 edits were test/bg/en/test2). Temporal proximity noted, not claimed as linked.
  - Others (n=5 each): 04-12 (2 dormant), 05-30 (4), 05-31 (5/5), 07-22 (4).
- Total: 111 burst accounts checked; 95 dormant (editcount=0). Full list: raw/dormancy-checks/dormancy.tsv; raw per-host API responses: raw/dormancy-checks/www_mediawiki_org.jsonl.
- Grade: LEAD (agent-shaped). Dozens of temp accounts created in tight bursts that never recorded an edit = automated session creation with failed/suppressed edits. Temp accounts create on edit ATTEMPT; 0 edits means the attempts produced no recorded revision (filtered, failed, or otherwise non-persisting). Does NOT align with the incident edit bursts (different wiki, different dates) — recorded as a lead per directive, not a negative, not claimed as the same operation.
- The 16 non-dormant burst accounts (editcount 1–72) are in dormancy.tsv; their edits not yet characterized (chunk-diver follow-up).

### BURST-4 (LEAD): simplewiki recurring n=10 bursts — OBSERVED
- 7 bursts, each exactly n=10 in a 10-min bin: 04-09, 04-14, 04-25, 05-05 (×2), 07-27, 09-21. Dormancy mixed per burst (e.g. 04-09: 6 dormant/4 with 1 edit; 07-27: 9 with 1 edit + 1 with 95 edits; 09-21: 9 dormant).
- 70 accounts checked; full list in dormancy.tsv. Grade: LEAD (weaker) — recurring fixed-size bursts suggest a scheduled process (classroom? bot? agent?). The exact-n=10 recurrence differs from the incident's sparse pattern. Referred to chunk divers.

### BURST-5 (WEAK LEAD): bgwiki small frequent bursts — OBSERVED
- 12 bursts, n=5–6 each, spread Apr–Aug (04-07, 04-29, 05-08, 05-13, 05-17 ×2, 05-18 ×2, 05-19, 05-29, 07-13, 08-31). 63 accounts checked; only 27 dormant — most have 1–17 edits (organic-looking).
- Grade: WEAK LEAD. Small frequent bursts with mostly-active accounts resemble workshops/classes, not the incident pattern. Noted for completeness; not prioritized.
- 2026-05-13T18:11 burst same-day as incident May-13 commons wave (different wiki) — temporal proximity noted only.

### BURST-2 (INCIDENT-ALIGNED): incubatorwiki 2026-06-25T20:18:21–20:28:21Z, n=5 — OBSERVED
- Accounts: ~2026-36920-78, ~2026-36837-69, ~2026-36803-16, ~2026-36724-00, ~2026-36867-71 (5 of the 10 Jun-25 incident accounts; the other 3 incubator incident accounts ~2026-36686-00/~2026-36722-50/~2026-36781-18 fall in the adjacent 10-min bin 20:08–20:18Z with n=3, below threshold — the full incubator volley is 8 accounts in 20:14:13–20:21:29Z).
- ALIGNS with the known Jun-25 edit burst — this IS the incident fleet volley, detected blind by the burst rule. Validates the method.
- No other bursts on incubatorwiki across Apr–Sep (1,025 temp creations, 7 suppressed-title events).

## 6-month newusers pull — progress + method notes (2026-10-06 14:56 CDT)
- Pull: 2026-04-01–2026-09-30, 9 wikis, `letype=newusers&leaction=newusers/autocreate`, lelimit=500, ≥6s pacing per host, 4 parallel per-host workers. Resume via raw/.newusers-pull-state.
- POSITIVE CONTROL (OBSERVED): 5/5 sampled incident accounts' autocreate events present in pulled testwiki data with exact expected timestamps (~2026-28355-02 2026-05-10T17:01:58Z, ~2026-31087-50 2026-05-25T17:57:53Z, ~2026-31558-62 2026-05-27T04:15:06Z, ~2026-31625-92 2026-05-27T03:23:02Z, ~2026-35379-90 2026-06-18T02:24:00Z). Pull is complete and accurate where checked.
- Data shape (OBSERVED): enwiki autocreates ≈ 12k/day, ~85% `~2026-*` temp; testwiki Apr–Jun only 2.3k events total. Localized titles on some wikis (bg: "Потребител:~2026-…") — temp filter must match `~\d{4}-` anywhere in title, not the "User:" prefix.
- 3 suppressed-title events on testwiki (actionhidden/suppressed) — counted, not attributable; off-limits per no-human-attribution rule.
- METHOD NOTE: incident temp creations are SPARSE per wiki (1–4 accounts spread over hours/days), not tight bursts — except Jun-25 incubator (~7 accounts in ~7 min). A ≥5/10min burst rule will catch the Jun-25-type fleet volleys but NOT the May waves; absence of a creation burst ≠ absence of agent activity. Bursts are sufficient, not necessary. Threshold for clustering: fixed 10-min bins, flag count ≥ max(5, mean+5sd) per wiki (script: /tmp/ap/burst_cluster.py, run at analysis time).

## 2026-10-06 14:15 CDT — full account census (28 temp accounts, all OBSERVED via globaluserinfo)

All 28 accounts are `~2026-*` temporary accounts (groups include `temp` on every wiki checked). NONE is globally locked (locked=False on all 28; zero globalauth log events on all 28). Only local sanction in the set: ~2026-36867-71 blocked indef on metawiki ("Unauthorized bot", 2026-06-25T22:29:53Z by NguoiDungKhongDinhDanh).

Waves by registration/first-edit (from revisions.tsv + globaluserinfo):
- 2026-05-10: ~2026-28217-20, ~2026-28355-02 (19 edits, 16:01–17:56Z), ~2026-28380-92, ~2026-28435-23
- 2026-05-13: ~2026-28986-96, ~2026-28987-61, ~2026-29018-32, ~2026-29065-25 (all commons)
- 2026-05-25: ~2026-31087-50 (test, 4 edits 17:57–18:15Z)
- 2026-05-27: ~2026-31341-00 (bg), ~2026-31558-62 (test, 3 edits), ~2026-31565-39, ~2026-31625-92, ~2026-31693-52, ~2026-31711-15
- 2026-06-18: ~2026-35379-90 (test), ~2026-35411-85 (simple), ~2026-35737-64 (commons)
- 2026-06-25: ~2026-36686-00, ~2026-36722-50, ~2026-36724-00, ~2026-36766-54 (commons), ~2026-36781-18, ~2026-36803-16, ~2026-36837-35 (meta), ~2026-36837-69, ~2026-36867-71 (incubator + 5 deleted meta), ~2026-36920-78 — 10 accounts in a 19:51–20:21Z window, sequentially numbered 36686→36920. Fleet-shaped.

Registration note (plain): temporary accounts auto-create on first edit, so registration_utc ≈ first-edit timestamp (observed: usually identical to the second, e.g. ~2026-36867-71 reg 20:21:29Z = first edit 20:21:29Z). It is NOT a signup event; do not present it as one. One outlier: ~2026-28355-02 registered 15:57:40Z but first recorded edit 16:01:42Z (~4 min gap — possibly a filtered first attempt; enwiki abuse-filter log unchecked).

~2026-31558-62 (the one account with edits beyond the CSV): testwiki contribs show 3 edits 04:15:06–04:33:11Z on 2026-05-27 — 744413 "test", 744414 "sandbox test" (the CSV oldid), 744415 "restore sandbox". Adjacent sandbox edits, still sandbox-only. Raw: raw/contribs-2026-31558-62-testwiki.json.

5 meta Web2Cit oldids (30732691/30732696/30732698/30732699/30732700): CONFIRMED-ABSENT — badrevids/missing on live query (mine) AND on revision-enumerator's independent batch (their PROVENANCE.md). Pages deleted by Pppery 2026-10-06T01:39:44–01:40:18Z (delete log, 5 pages, 34s window). Attribution to ~2026-36867-71: INFERENCE (strong) — metawiki editcount=5, one deleted page lived at User:~2026-36867-71/Web2Cit/..., local "Unauthorized bot" block 2h after first edit.

Per-account clustering analysis: HELD for chunk divers per user directive. This lane delivers facts only (accounts.tsv in raw/).

## 2026-10-06 13:55 CDT — three accounts profiled (API, paced ≥5s)

### ~2026-28355-02 (May-10 sandbox wave) — OBSERVED
- globaluserinfo: home=enwiki, global id 84295694, registration 2026-05-10T15:57:40Z, global editcount=19.
- Merged wikis: enwiki 6, testwiki 6, test2wiki 3, mediawikiwiki 4 (19 total); loginwiki/metawiki/enwikibooks merged with 0 edits.
- Full contribs pulled (6 queries): ALL 19 edits are sandbox "test"/"sandbox test"/"test link" on 2026-05-10 16:01–17:56 UTC. Revids match CSV oldids exactly (en 1353490694/0935/1551/8400/1383/7315, test 741398-741409, test2 612931-33, mediawiki 8370989/94/95/96). Comments trivial ("test", "sandbox test", "test link"), mostly tagged mw-reverted. Zero non-sandbox activity.
- Lock status: NOT globally locked (no `locked` flag in globaluserinfo; zero globalauth log events). No local blocks on any merged wiki.
- Verdict: single-purpose incident sandbox account. 19/19 = incident edits.

### ~2026-36867-71 (Jun-25 operator) — OBSERVED
- globaluserinfo: home=incubatorwiki, global id 85301133, registration 2026-06-25T20:21:29Z, global editcount=6.
- Merged: incubatorwiki 1 edit, metawiki 5 edits (all now deleted), loginwiki 0.
- Incubator edit (7226111, 2026-06-25T20:21:29Z): Incubator:Sandbox, comment "Temporary technical sandbox initialization" — same distinctive comment as the May-27/Meta waves.
- Meta: usercontribs returns 0 live edits but global editcount=5 → all 5 meta edits deleted. The 5 CSV meta oldids (30732691 + 30732696/98/99/32700) return `badrevids`/`missing` — consistent with deletion, NOT with "never existed". Delete log: Pppery deleted `Web2Cit/data/com/arcgis/use1-geocode/templates.json` 2026-10-06T01:40:11Z (matches osint-scribe's ~15h-post-disclosure window). osint-scribe's "nonexistent oldids" = deleted revisions, not fabrications — evidence-integrity flag REFRAMED: the oldids were real edits on pages deleted post-disclosure.
- Lock status: NOT globally locked (no `locked` flag; zero globalauth events). Locally blocked on metawiki INDEFINITE at 2026-06-25T22:29:53Z by NguoiDungKhongDinhDanh, reason "Unauthorized bot", nocreate — ~2h after its first edit. No other local blocks.
- Verdict: single-purpose incident operator account. 6/6 = incident edits (1 sandbox + 5 Web2Cit config on deleted pages).

### ~2026-36837-35 (Jun-25, Meta:Sandbox) — OBSERVED (NEW account, not in HUNT-SUMMARY)
- CSV oldid 30732655 (Meta:Sandbox, 2026-06-25T19:51:17Z, "Temporary technical sandbox initialization") is authored by this account, NOT ~2026-36867-71.
- globaluserinfo: home=metawiki, id 85300722, registration 2026-06-25T19:51:17Z, editcount=1, merged metawiki+loginwiki only. Not locked, not blocked.
- Verdict: single-purpose incident sandbox account. 1/1 = incident edit.
- INFERENCE: same browser-session family as ~2026-36867-71? Names differ (~2026-36837-35 vs ~2026-36867-71) → different temp-account cookies/sessions (temp accounts are cookie-bound, so distinct names = distinct sessions), created ~30 min apart on the same evening with the same distinctive edit comment. Consistent with a fleet of parallel agent sessions (same-provider/different-instances), not proof of shared human.

### Coverage (SUPERSEDED by 14:15 census above — historical note only)
- 26/54 CSV oldids assigned to 3 accounts. 28 oldids pending usernames (waiting on revisions.tsv or self-enumeration at ~14:11 CDT deadline).
- Cluster so far: ALL THREE accounts are single-purpose (only incident edits). Zero accounts with broader organic history yet.
- OBSERVED: CSV has 54 URLs across 9 wiki hosts (bg 1, commons 6, en 11, incubator 8, meta 6, simple 1, test 13, test2 4, mediawiki.org 4). Note: HUNT-SUMMARY said "52–53" — actual count is 54 (last line lacks trailing newline).
- OBSERVED: `wikipedia-lane/revisions.tsv` does not exist yet; REVISION-ENUMERATOR presumed in progress. Poller armed; self-enumeration deadline ~14:11 CDT.
- UPSTREAM: incident editors are ~2026-* TEMPORARY ACCOUNTS; public IPs are CheckUser-only. Profiling therefore covers temp-account public artifacts only: contribution history, creation date, edit counts, lock status.
- Scope note: agents/infrastructure only. No human-identity pursuit — temp accounts are cookie-linked and their identity resolution is not in scope regardless.

## 2026-10-06 19:05 CDT — LIFEVAL cross-corpus zoom-in: status assessment (account-profiler finisher)

`data/2026-10-06-wikimedia-rogue-agents/lifeval-cross-corpus/` (event-level, untracked) is NOT a mystery dir — it is a 4-worker cross-corpus sweep of the Lifeval marker vocabulary, ~75% complete. Assessed, not owned, by this lane; coordinator owns it.
- **web-search** (DONE, FINDINGS.md): 10 query runs, no cross-corpus hit. Lifeval markers exist publicly only in the incident diffs. Surviving item: LIFEVAL/LIFBench name collision (LLM eval framework paper, Wu et al., Nov 2024) — graded INFERENCE (homonym), keep as footnote only.
- **disk-corpora** (DONE, FINDINGS.md): rg sweep of `~/workspace/silent-locus/data/` + muse-home/projects. ONE real cross-corpus survivor: exact machine-phrased `"sandbox link test"` in the colony-bullfincher/collusion-wiki agent-log corpus — two revisions on `wikiservice.at/dse`'s `WillkommenImWiki` (dse~WillkommenImWiki@23, 2026-06-18T17:38:50Z; @13, 18:38Z), label HelperMassRef37882, body = SEC county.json link farm with double-encoded URL trickery. Same DATE as the incident's M5 "Sandbox link test" cluster (simple+test, 2026-06-18). Grade: OBSERVED (bytes) / INFERENCE (linkage). Lifeval codename itself: zero cross-corpus hits. Cached: `lifeval-cross-corpus/raw/disk-corpora-dse-willkommenimwiki-{23,13}.json` + provenance.
- **urlquery-live** (DONE, FINDINGS.md): 11 htmx queries, zero Lifeval markers in the index (weak negative — htmx misses known-live records; markers live in page content, not URLs). Endpoint discovery documented: bare `/api/htmx/search/` returns 204; needs HX headers (`HX-Request: true`, form-field param set) — recorded for future workers.
- **urlquery-cached** (SCANLOG only, scans still running at 19:05, SUPERSEDED by disk-corpora's broader completed sweep — verdict line pending, do not re-grade).
- Relevance to this lane: the dse survivor is the only cross-corpus link of incident marker vocabulary found anywhere. The "sandbox link test" phrasebook is shared between the WMF Lifeval fleet and the dse agent-log fleet on the same date, different wiki farm. Filed as a lead for the coordinator; no attribution claimed.

## EventStreams / feed question — ANSWERED 2026-10-06 14:05 CDT
- Endpoints (UPSTREAM, fuzheado/wikipedia-ai-skills MIT skill, last verified 2026-06-10): `https://stream.wikimedia.org/v2/stream/recentchange` (alias of `mediawiki.recentchange`) — the main firehose: every edit, page creation, log entry, categorize, external change. Sibling v2 streams: `revision-create`, `page-create`, `page-delete`, `page-undelete`, `page-move`, `page-links-change`, `page-properties-change`, `revision-tags-change`, `revision-visibility-change`, `page_change.v1`, ML prediction streams, Wikidata/Wikibase mutation streams, `eventgate-main.test.event`. Composites via comma-joined URL path. Swagger: `https://stream.wikimedia.org/?doc`, spec at `?spec`. Protocol: SSE (`text/event-stream`) or NDJSON with `Accept: application/json`; no auth; descriptive User-Agent required.
- Event fields (OBSERVED, live sample 2026-10-06): `$schema`, `meta{uri,request_id,id,domain,stream,dt,topic,partition,offset}`, `id`, `type` ("edit"|"new"|"log"|"categorize"|"external"), `namespace`, `title`, `title_url`, `comment`, `parsedcomment`, `timestamp` (unix s), `user`, `bot`, `minor`, `patrolled`, `notify_url`, `length{old,new}`, `revision{old,new}`, `server_url`, `server_name`, `server_script_path`, `wiki`.
- User-creation events: there is NO dedicated user-creation stream. Creations ride the recentchange firehose as `type:"log"` events with `log_type:"newusers"`, `log_action:"create"|"autocreate"` (UPSTREAM, schema docs; no log event appeared in the 2s sample, so field names are community-documented, not byte-verified).
- Historical replay: `?since=<ISO-8601>` and `Last-Event-ID` resume are supported (since June 2018), BUT retention is Kafka-bound at ~7–31 days per stream (UPSTREAM, community docs citing WMF topic config).
- LIVE RETENTION TEST (OBSERVED, 2026-10-06 14:05 CDT): `curl -sN --max-time 12 -H 'Accept: application/json' 'https://stream.wikimedia.org/v2/stream/recentchange?since=2026-06-01T00:00:00Z'` returned events with `meta.dt` = 2026-09-23T09:44:04Z — the server clamped the June `since` to the oldest retained offset and served from there. CONCLUSION: no May–June 2026 history is replayable; the incident window is gone from EventStreams. The `since` parameter beyond retention degrades to oldest-available (here ~13 days back, consistent with the documented 7–31d window).
- Public archive covering May–June 2026? HONEST NEGATIVE. Two web searches (2026-10-06) found no public archive of the EventStreams firehose itself. Hobbyist consumers keep only rolling windows (e.g. wikipedia-live-analytics: 7-day MongoDB TTL). Historical substitutes: monthly XML dumps (dumps.wikimedia.org), SQL replicas, and the Action API `logevents` — which is why the 6-month `newusers` API pull (now running) is the correct historical substitute. Coverage of this negative: 2 search queries + docs review + 1 live retention probe.
- Transport anomaly (OBSERVED, side note): the public endpoint's "live" tail currently starts at 2026-09-23 — i.e., ~13 days behind wall-clock (Oct 6). Either the public EventStreams is lagging, or Sept 23 is the current retention boundary. Not incident-relevant; logged for the record.
