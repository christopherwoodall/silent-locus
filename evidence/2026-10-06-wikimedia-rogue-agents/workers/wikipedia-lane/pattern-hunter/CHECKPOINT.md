# PATTERN-HUNTER checkpoint

## Done (2026-10-06 ~18:40Z)
- Phase 1 collection: collect_revisions.py pulled all 54 CSV jobs via per-wiki
  MediaWiki API (curl, paced 5.5s, UA silent-locus-pattern-hunter/1.0).
  -> revisions.tsv (49 rows), diffs/ (49 content files), raw/revisions_*_batch0.json.
- CONFIRMED: 5/54 oldids are nonexistent (all meta Web2Cit set:
  30732691, 30732696, 30732698, 30732699, 30732700). Evidence-integrity flag holds.
- Marker catalog drafted in FINDINGS.md.
- KEY LEAD: content marker `<!-- Lifeval ... -->` (incubator/meta/commons).
  Search form: action=query&list=search&srsearch=insource%3A%22Lifeval%22

## Resume queries (if interrupted)
1. Lifeval insource sweep: for each host in en/test/test2/www.mediawiki/commons/
   simple/incubator/meta/bg:
   https://<host>/w/api.php?action=query&list=search&srsearch=insource%3A%22Lifeval%22&srlimit=50&format=json&formatversion=2
   (pace >=5.5s; bank raw JSON in raw/search_lifeval_<host>.json)
2. Missing-incubator-rev: action=query&prop=revisions&revids=7226106 on incubator
   (account + comment of the in-burst revision WMF did NOT list).
3. usercontribs for anchor accounts (en + test + test2 + mediawiki for ~2026-28355-02;
   meta for ~2026-36867-71; all-wiki for each via centralauth? passive only):
   https://<host>/w/api.php?action=query&list=usercontribs&ucuser=~2026-28355-02&ucprop=ids|title|timestamp|comment|size|flags&uclimit=500&format=json&formatversion=2
   (URL-encode the ~ prefix: %7E2026-28355-02)
4. Sandbox-page history windows: Wikipedia:Sandbox (en), Commons:Sandbox,
   Project:Sandbox (mediawiki), Incubator:Sandbox, Meta:Sandbox, Wikipedia:Sandbox
   (test/test2/simple), User:Example/sandbox (en/test):
   action=query&prop=revisions&titles=<title>&rvprop=ids|timestamp|user|comment|tags|size&rvlimit=500&rvstart=<window end>&rvend=<window start>&rvdir=older
   Windows (UTC): 2026-05-10T15:00-22:00Z, 2026-05-13T17:00-22:30Z, 2026-05-25T17:00-19:00Z,
   2026-05-27T00:00-18:00Z, 2026-06-18T01:00-21:30Z, 2026-06-25T19:00-20:40Z.
5. Zoom-in candidates: any new account/edit cluster matching >=2 markers ->
   dedicated FINDINGS.md section with user/timestamps/diffs/grades.
