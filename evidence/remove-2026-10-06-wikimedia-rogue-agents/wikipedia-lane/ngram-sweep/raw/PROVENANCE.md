# Provenance — ngram-sweep raw/

- **Method:** MediaWiki Action API `list=search` with `srsearch=insource:"<ngram>"`,
  `srlimit=50`, `srnamespace=*`, `formatversion=2`; plus `prop=revisions`
  (`rvprop=ids|timestamp|user|comment|tags`, `rvlimit=200`) on each wiki's
  main sandbox page, comment substring match (case-insensitive).
- **Collection:** curl-equivalent via Python urllib, User-Agent
  `silent-locus-ngram-sweep/1.0`, paced >=5.5s between requests, 2026-10-07.
- **Ngrams (9):** "technical sandbox initialization", "sandbox initialization",
  "temporary technical", "Lifeval temporary", "Lifeval API", "temp-account test",
  "temp-account", "API temp-account", "external link test".
- **Wikis (9):** en.wikipedia.org, simple.wikipedia.org, test.wikipedia.org,
  test2.wikipedia.org, www.mediawiki.org, commons.wikimedia.org,
  incubator.wikimedia.org, meta.wikimedia.org, bg.wikipedia.org.
- **Known limitation:** insource: searches CURRENT page content only;
  cleaned sandboxes erase content markers (see vocab-sweep FINDINGS.md).
  Comment grep is a 200-revision spot check, not exhaustive.
- **Scripts:** sweep_insource.py, sweep_sandbox_comments.py (adapted from
  vocab-sweep/, same pacing and error handling).
