# PROVENANCE — 2026-10-06 Wikimedia rogue-agent research

**Seed:** https://diff.wikimedia.org/2026/10/05/openai-rogue-agent-activities-found-on-wikimedia-projects/
(Wikimedia Foundation Diff blog, published 2026-10-05 — "OpenAI 'rogue' agent
activities found on Wikimedia projects")

**Upstream claims (unverified, grade: upstream assertion):**
- OpenAI-operated agents made test edits in wiki sandbox areas (not
  reader-visible), plus a few edits to a citation tool's configuration,
  assessed as potentially malicious (proxy misuse for fetching remote data).
- Unsuccessful attempts to compromise Wikimedia's public Etherpad
  (tried to use it as a fetch proxy); other agents took task notes on
  Etherpad (no coordination observed).
- Millions of automated API requests (mainly Wikidata + Wikimedia Commons),
  hundreds of thousands of WDQS queries; traffic may have contributed to
  the May WDQS partial outage.
- No evidence of agent coordination via Wikimedia systems; no evidence of
  systems/data compromise.

**Linked references to chase:** security.wikimedia.org (the edits writeup),
metr.org, transluce.org, rubyhack.ai, collusion.wiki, en.wikipedia.org
Etherpad article, wikitech.wikimedia.org (WDQS outage).

**Collection doctrine:** passive/public OSINT only. Public documented
APIs (MediaWiki API, etc.) may be queried with curl. Candidate suspicious
URLs are logged, never live-fetched. Evidence never redacted.

## account-profiler (wikipedia-lane) — 2026-10-06

**Endpoints used (all public, read-only, curl, paced >=5s):**
- `GET https://<wiki-host>/w/api.php?action=query&list=logevents&letype=newusers&leaction=newusers/autocreate&lelimit=500&leprop=ids|timestamp|title|type&lestart=<next-month>T00:00:00Z&leend=<month>T00:00:00Z&format=json`, fully paged via `lecontinue` (newest-first per month chunk).
- `GET .../w/api.php?action=query&list=users&usprop=registration|editcount|groups` (per-account registration), `list=globaluserinfo`, `list=usercontribs` (per-account contribs), `list=logevents&letype=globalauth` (lock log), per-wiki block logs.
- `https://stream.wikimedia.org/v2/stream/recentchange?since=2026-06-01T00:00:00Z` (retention probe only; returned events from 2026-09-23 — no May-Jun history replayable).

**Newusers 6-month pull (2026-04-01..2026-09-30, autocreate only):** 9 wikis x 6 month-chunks = 54 chunks.
Files: `wikipedia-lane/raw/newusers-2026-04-01_2026-09-30.<shortwiki>.jsonl` (one event/line; fields logid,ns,title,pageid,logpage,type,action,timestamp).
Resume state: `wikipedia-lane/raw/.newusers-pull-state` (`wiki:YYYY-MM` per completed chunk). Scope justification: all ~2026-* temp accounts are created via autocreate (verified 3/3 sampled; regular `create` signups can never be `~2026-*`), so autocreate-only is NOT sampling. Positive control: 5/5 sampled incident accounts' autocreate events present with exact expected timestamps.
Worker-restart double-append artifacts exist in 4 files (exact 30,000-line or 21,500-line block repeats from restarted chunks); unions are gap-free; analysis dedupes by logid. Raw vs unique counts below.

| wiki | raw lines | unique logids | sha256 |
|---|---|---|---|
| testwiki | 2,321 | 2,321 | |
| test2wiki | 665 | 665 | |
| incubatorwiki | 52,185 | 52,185 | |
| mediawikiwiki | 147,947 | 147,947 | |
| simplewiki | 100,825 | 100,825 | |
| bgwiki | 18,899 | 18,899 | |
| commonswiki | 470,230 | 448,730 | |
| enwiki | PENDING | PENDING | |
| metawiki | PENDING | PENDING | |

**Other account-profiler raw evidence** (`wikipedia-lane/raw/`): `accounts.tsv` (28 accounts, factual columns incl. registration_utc); `contribs-2026-28355-02-{enwiki,testwiki,test2wiki,mediawikiwiki}.json` (19 edits); `contribs-2026-31558-62-testwiki.json` (3); `contribs-2026-36867-71-{incubatorwiki,metawiki}.json` (1+0 live; 5 deleted); `contribs-2026-36837-35-metawiki.json` (1); `contribs-burst1-testwiki-2026-*.json` (5); `registration-*.json`; `newusers-probe-*.json` (autocreate log entries for 3 seed accounts); `globaluserinfo/*.json` (28; locked=False all); `locklog-globalauth/*.json` (0 events all); `blocklog-2026-36867-71-metawiki.json` (single local indef block "Unauthorized bot"); `dormancy-checks/dormancy.tsv` + per-host API JSONL.

**Scripts:** `workers/wikipedia-lane/account-profiler/pull_newusers_6mo.sh` (month-chunk pull), `resume_chunk.py` (resume partial chunk from a lestart timestamp), `burst_cluster.py` (10-min bins, flag >= max(5, mean+5sd) temp creations).
