# Provenance — vocab-sweep raw
- Method: MediaWiki API via curl-equivalent (python urllib), User-Agent silent-locus-vocab-sweep/1.0, paced >=5.5s between requests.
- Retrieved: 2026-10-06 ~23:40–23:50 UTC.
- insource sweep: action=query&list=search, srsearch=insource:"<phrase>", srlimit=50, srnamespace=*, formatversion=2. 54 requests, 0 errors.
- Sandbox comment sweep: action=query&prop=revisions, rvprop=ids|timestamp|user|comment|tags, rvlimit=200, formatversion=2. 9 requests, 0 errors.
- Files: insource-<wiki>-<nn>.json (01..54), SUMMARY.json; sandbox-comments-<wiki>.json, sandbox-comments-SUMMARY.json.
- Scripts: ../sweep_insource.py, ../sweep_sandbox_comments.py (committed alongside).
