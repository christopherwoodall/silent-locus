# CHECKPOINT — account-profiler (wikipedia-lane)
Branch: `wikipedia-edit-hunt-2026-10-06`. Last update: 2026-10-06 ~13:40 CDT.

## Inputs
- CSV: `data/2026-10-06-wikimedia-rogue-agents/raw/openai-wikimedia-edits-2026-10-04.csv` — 54 URLs across 9 wiki hosts (en, test, test2, mediawiki.org, commons, simple, incubator, meta, bg).
- revisions.tsv: NOT YET PRESENT (2026-10-06 13:41 CDT). Background poller `proc_5c60ba5889b3` checking every 3 min, deadline ~14:11 CDT, then self-enumerate usernames via per-wiki `action=query&prop=revisions&revids=...&rvprop=user|timestamp|comment|ids|tags` (≤50 revids/batch, ≥5s pacing, curl only).
- Known incident accounts from HUNT-SUMMARY (UPSTREAM): `~2026-36867-71` (operator, Web2Cit config edits), `~2026-28355-02` (sandbox account).

## Per-wiki revid batches (to run if enumerator misses)
- bg.wikipedia.org (api.php): revids=12923296
- commons.wikimedia.org: revids=1213503714|1213503789|1213513506|1233683454|1213399057|1238390511
- en.wikipedia.org: revids=1353490694|1353490935|1353491551|1353492663|1353498400|1353501383|1353507315|1353518652|1353543060|1356314507|1356419247
- incubator.wikimedia.org: revids=7226111|7226103|7226104|7226105|7226107|7226108|7226109|7226110
- meta.wikimedia.org: revids=30732691|30732696|30732698|30732699|30732700|30732655 (NOTE: 30732696-30732700 nonexistent per osint-scribe — expect API "missing" on these)
- simple.wikipedia.org: revids=10891416
- test.wikipedia.org: revids=741398|741399|741400|741405|741406|741409|744268|744270|744271|744272|744412|744414|747327
- test2.wikipedia.org: revids=612931|612932|612933|613856
- www.mediawiki.org: revids=8370989|8370994|8370995|8370996

## Per-account status (updated as work proceeds)
| account | created | global edits | wikis w/ edits | lock status | local blocks | verdict | status |
|---|---|---|---|---|---|---|---|
| ~2026-28355-02 | 2026-05-10T15:57:40Z | 19 | en(6) test(6) test2(3) mediawiki(4) | not locked (0 globalauth events) | none | single-purpose (19/19 sandbox test edits, all 2026-05-10) | DONE |
| ~2026-36867-71 | 2026-06-25T20:21:29Z | 6 | incubator(1) meta(5 deleted) | not locked (0 globalauth events) | metawiki indef "Unauthorized bot" by NguoiDungKhongDinhDanh 2026-06-25T22:29:53Z | single-purpose (6/6 incident: 1 sandbox + 5 Web2Cit config, now deleted) | DONE |
| ~2026-36837-35 | 2026-06-25T19:51:17Z | 1 | meta(1) | not locked (0 globalauth events) | none | single-purpose (1/1 Meta:Sandbox) | DONE |

Accounts list otherwise pending revisions.tsv / self-enumeration (deadline ~14:11 CDT).

## API endpoint log
- 2026-10-06 13:43 CDT: `https://meta.wikimedia.org/w/api.php?action=query&meta=globaluserinfo&guiuser=<u>&guiprop=groups|merged|unattached|editcount&format=json` — to run per account. Expected: `locked` flag, global editcount, `merged[]` with per-wiki registration+editcount.
- Lock log check: `https://meta.wikimedia.org/w/api.php?action=query&list=logevents&letype=globalauth&letitle=User:<u>&leprop=ids|timestamp|user|comment|details&lelimit=50&format=json` — lock/block event type under `globalauth`? Verify; fall back to `list=logevents&letype=globalblocks` (for blocks, different mechanism) and CentralAuth profile page text fetch.
- Per-wiki contribs: `https://<host>/w/api.php?action=query&list=usercontribs&ucuser=<u>&uclimit=max&ucprop=ids|title|timestamp|comment|sizediff|flags|tags&format=json&ucdir=older` — paginate via `uccontinue`.
