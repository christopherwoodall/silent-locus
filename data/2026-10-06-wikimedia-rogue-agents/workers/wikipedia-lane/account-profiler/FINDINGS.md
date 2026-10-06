# FINDINGS — account-profiler (wikipedia-lane)
Branch: `wikipedia-edit-hunt-2026-10-06`. Updated incrementally.

Every claim graded: OBSERVED (bytes in hand) / INFERENCE (reasoned link) / UPSTREAM (someone else's claim).

## Burst clustering — results (incremental)

### BURST-1 (LEAD): testwiki 2026-09-30T06:33:32–06:37:19Z, n=5 — OBSERVED
- Accounts: ~2026-52540-64, ~2026-52595-59, ~2026-52476-76, ~2026-52359-23, ~2026-52556-21 (created within 4 min; testwiki background ≈ 0.03 temp creations/10min bin, so 5 in one bin is a >150σ outlier).
- NOT dormant: editcount=1 each (dormancy.tsv). Each made exactly ONE edit, all to "Twinkle test page" (revids 765142–765150, consecutive): first created the page with `{{subst:Deletion sorting/multi|Lists|sig=~~~~}}`, rest blanked/touched it. Raw: raw/contribs-burst1-testwiki-2026-*.json (5 files).
- Does NOT align with known incident edit bursts (May 10 / May 27 / Jun 25) — recorded as a lead per directive, not a negative.
- Assessment: coordinated multi-session activity (5 distinct temp cookies, same page, consecutive revids within 4 min) is agent-shaped OR a logged-out human dev testing Twinkle's deletion-sorting. INFERENCE either way; the Twinkle-test content differs from the incident's sandbox-"test" grammar. Referred to chunk divers.
- Note: account numbers non-sequential (52359–52595 spread) within the 4-min window, unlike the Jun-25 incubator wave (36686→36920 sequential in 30 min). Temp-ID sequencing is not a reliable fleet clock — OBSERVED counterexample.

### test2wiki (Apr–Sep complete): zero bursts (132 temp creations, max bin < 5).

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

### Coverage
- 26/54 CSV oldids assigned to 3 accounts. 28 oldids pending usernames (waiting on revisions.tsv or self-enumeration at ~14:11 CDT deadline).
- Cluster so far: ALL THREE accounts are single-purpose (only incident edits). Zero accounts with broader organic history yet.
- OBSERVED: CSV has 54 URLs across 9 wiki hosts (bg 1, commons 6, en 11, incubator 8, meta 6, simple 1, test 13, test2 4, mediawiki.org 4). Note: HUNT-SUMMARY said "52–53" — actual count is 54 (last line lacks trailing newline).
- OBSERVED: `wikipedia-lane/revisions.tsv` does not exist yet; REVISION-ENUMERATOR presumed in progress. Poller armed; self-enumeration deadline ~14:11 CDT.
- UPSTREAM: incident editors are ~2026-* TEMPORARY ACCOUNTS; public IPs are CheckUser-only. Profiling therefore covers temp-account public artifacts only: contribution history, creation date, edit counts, lock status.
- Scope note: agents/infrastructure only. No human-identity pursuit — temp accounts are cookie-linked and their identity resolution is not in scope regardless.

## EventStreams / feed question — ANSWERED 2026-10-06 14:05 CDT
- Endpoints (UPSTREAM, fuzheado/wikipedia-ai-skills MIT skill, last verified 2026-06-10): `https://stream.wikimedia.org/v2/stream/recentchange` (alias of `mediawiki.recentchange`) — the main firehose: every edit, page creation, log entry, categorize, external change. Sibling v2 streams: `revision-create`, `page-create`, `page-delete`, `page-undelete`, `page-move`, `page-links-change`, `page-properties-change`, `revision-tags-change`, `revision-visibility-change`, `page_change.v1`, ML prediction streams, Wikidata/Wikibase mutation streams, `eventgate-main.test.event`. Composites via comma-joined URL path. Swagger: `https://stream.wikimedia.org/?doc`, spec at `?spec`. Protocol: SSE (`text/event-stream`) or NDJSON with `Accept: application/json`; no auth; descriptive User-Agent required.
- Event fields (OBSERVED, live sample 2026-10-06): `$schema`, `meta{uri,request_id,id,domain,stream,dt,topic,partition,offset}`, `id`, `type` ("edit"|"new"|"log"|"categorize"|"external"), `namespace`, `title`, `title_url`, `comment`, `parsedcomment`, `timestamp` (unix s), `user`, `bot`, `minor`, `patrolled`, `notify_url`, `length{old,new}`, `revision{old,new}`, `server_url`, `server_name`, `server_script_path`, `wiki`.
- User-creation events: there is NO dedicated user-creation stream. Creations ride the recentchange firehose as `type:"log"` events with `log_type:"newusers"`, `log_action:"create"|"autocreate"` (UPSTREAM, schema docs; no log event appeared in the 2s sample, so field names are community-documented, not byte-verified).
- Historical replay: `?since=<ISO-8601>` and `Last-Event-ID` resume are supported (since June 2018), BUT retention is Kafka-bound at ~7–31 days per stream (UPSTREAM, community docs citing WMF topic config).
- LIVE RETENTION TEST (OBSERVED, 2026-10-06 14:05 CDT): `curl -sN --max-time 12 -H 'Accept: application/json' 'https://stream.wikimedia.org/v2/stream/recentchange?since=2026-06-01T00:00:00Z'` returned events with `meta.dt` = 2026-09-23T09:44:04Z — the server clamped the June `since` to the oldest retained offset and served from there. CONCLUSION: no May–June 2026 history is replayable; the incident window is gone from EventStreams. The `since` parameter beyond retention degrades to oldest-available (here ~13 days back, consistent with the documented 7–31d window).
- Public archive covering May–June 2026? HONEST NEGATIVE. Two web searches (2026-10-06) found no public archive of the EventStreams firehose itself. Hobbyist consumers keep only rolling windows (e.g. wikipedia-live-analytics: 7-day MongoDB TTL). Historical substitutes: monthly XML dumps (dumps.wikimedia.org), SQL replicas, and the Action API `logevents` — which is why the 6-month `newusers` API pull (now running) is the correct historical substitute. Coverage of this negative: 2 search queries + docs review + 1 live retention probe.
- Transport anomaly (OBSERVED, side note): the public endpoint's "live" tail currently starts at 2026-09-23 — i.e., ~13 days behind wall-clock (Oct 6). Either the public EventStreams is lagging, or Sept 23 is the current retention boundary. Not incident-relevant; logged for the record.
