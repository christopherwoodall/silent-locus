# FINDINGS — account-profiler (wikipedia-lane)
Branch: `wikipedia-edit-hunt-2026-10-06`. Updated incrementally.

Every claim graded: OBSERVED (bytes in hand) / INFERENCE (reasoned link) / UPSTREAM (someone else's claim).

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
