# ARCHIVIST findings — Wikipedia edit-hunt lane (Wayback/Arquivo.pt coverage)
Branch: wikipedia-edit-hunt-2026-10-06. Worker: archivist. Date: 2026-10-06.

Grade key: OBSERVED = bytes returned by a query; INFERENCE = reasoned link;
UPSTREAM = someone else's claim.

## 1. Transport health (OBSERVED)

- Wayback CDX via http://web.archive.org (port 80): HEALTHY.
  Known-positives at 2026-10-06T18:44:15Z:
  - example.com -> 20020120142510 http://example.com:80/ 200
  - www.mediawiki.org -> 20030819022955 http://mediawiki.org:80/ 301
  - en.wikipedia.org/w/index.php?title=Main_Page -> captures 2013-2017 (http and https forms both indexed)
- Arquivo.pt textsearch API: HEALTHY (example.com versionHistory -> estimated_nr_results=3176).
- https://web.archive.org:443 times out on this VM (matches TOOLS.md lesson); all queries used http://.
- CDX backend quirk noted (OBSERVED): `matchType=prefix` on `security.wikimedia.org/data`
  returned empty while `matchType=exact` on the full CSV URL returned a capture.
  Backend flakiness is documented in TOOLS.md; prefix-zeros for that path are treated
  as unreliable and re-checked by exact query.

## 2. The 54 diff URLs (Wayback coverage)

Query form: matchType=exact on the as-given URL + on an http:// scheme variant
(two forms per URL). Known-positive control: en.wikipedia.org Main_Page history
page returns captures, so exact-form queries resolve.
Pacing: ~1 req/5s; full per-URL table in raw/diff-coverage-results.txt.

RESULT (OBSERVED, final 2026-10-06T19:12Z): 0 of 54 diff URLs captured by Wayback.
108 exact-match queries (54 URLs x as-given https + http-scheme variant), all count=0.
Honest zero: transport proven healthy; enwiki Main_Page history-page exact queries
return captures, so query-string URLs do resolve; and zero diff captures of
Main_Page ever recorded, indicating ?diff=/&oldid= pages are structurally
near-absent from the index. Archive content recovery of these edits is only
possible via the parent sandbox pages' own captures (section 3) or the live wiki.

## 3. Involved pages — capture timelines (OBSERVED)

Window shorthand: W1=2026-05-01..15 (May 10 incident), W2=2026-05-20..06-02 (May 27),
W3=2026-06-20..07-01 (Jun 25), W4=2026-10-01..06 (deletion/disclosure).

- en.wikipedia.org/wiki/Wikipedia:Sandbox: captures inside every window:
  W1 20260506, 20260509; W2 20260527; W3 20260625; W4 20261002, 20261004. (OBSERVED)
- en.wikipedia.org/wiki/User:Sandbox: W2 20260527; plus 20260713, 20260723, 20260822, 20260920. (OBSERVED)
- en.wikipedia.org/wiki/User:Example/sandbox: ZERO captures 20260501-20261006. (OBSERVED, honest zero)
- test.wikipedia.org/wiki/Wikipedia:Sandbox: 20260611 x4, 20260714, 20260924. (OBSERVED)
  test.wikipedia.org/wiki/Sandbox: 20260617. (OBSERVED)
- test2.wikipedia.org/wiki/Wikipedia:Sandbox: 20260521. (OBSERVED)
  test2.wikipedia.org/wiki/Sandbox: 20260511. (OBSERVED)
- www.mediawiki.org/wiki/Project:Sandbox: ~weekly captures all windows
  (20260502, 20260507, 20260513, 20260524, 20260601/09/14/17, 20260701..., 20261002). (OBSERVED)
- commons.wikimedia.org/wiki/Commons:Sandbox: 20260509, 20260510, 20260514, 20260609,
  20260619, 20260621, ... (roughly monthly). (OBSERVED)
- simple.wikipedia.org/wiki/Wikipedia:Sandbox: ~2-4/mo all windows
  (20260503, 20260506, 20260513, 20260523, 20260602/04/06/07/11/14/15/17/27, ...). (OBSERVED)
- incubator.wikimedia.org/wiki/Incubator:Sandbox: 20260510, 20260618, 20260914. (OBSERVED)
- meta.wikimedia.org/wiki/Meta:Sandbox: 20260527 x2, 20260626, 20260710, 20260727,
  20260831, 20260927. (OBSERVED)
- Note: en.wikipedia.org User:Example/sandbox has zero captures; the exact
  diff URLs (above) are the only archive angle for those edits.

## 4. Deleted Web2Cit config pages — THE high-value target (OBSERVED)

All four Meta-Wiki Web2Cit config pages (created 2026-06-25 per upstream, deleted
2026-10-06 01:39:44-01:40:11Z by Pppery per osint-scribe) return ZERO Wayback
captures in both URL forms (/wiki/ and /w/index.php?title= with %2F-encoded slashes)
and ZERO Arquivo.pt versions:
- Web2Cit/data/com/arcgis/templates.json (oldid 30732699 in CSV — nonexistent per osint-scribe)
- Web2Cit/data/com/arcgis/services/templates.json (oldid 30732700 — nonexistent)
- Web2Cit/data/gov/hawaii/geodata/templates.json (oldid 30732698 — nonexistent)
- Web2Cit/data/com/arcgis/use1-geocode/templates.json (oldid 30732696 — nonexistent)
- User:~2026-36867-71/Web2Cit/data/com/arcgis/geocode/templates-temp-5123 (oldid 30732691): zero.
- All four on Arquivo.pt versionHistory: estimated_nr_results=0. (OBSERVED, honest zeros;
  both archive transports proven healthy.)
- Control (OBSERVED): sibling Web2Cit/data/... config pages DO appear in Wayback
  (e.g. Web2Cit/data/com/britannica/www/templates.json 20260909,
  Web2Cit/data/com/adobe/helpx/patterns.json 20260408) via
  /w/index.php?title=Web2Cit%2Fdata%2F... — so the zero for the deleted pages is
  meaningful, not a URL-form artifact. The Sept-2025 capture cluster looks like a
  systematic Web2Cit-config crawl; the incident pages (created 2026-06-25) postdate it.
  INFERENCE: deleted Web2Cit config contents are unrecoverable from Wayback or
  Arquivo.pt; recovery requires WMF/MediaWiki API (deleted-revision access) or the
  operator's own copies.

## 5. Temp accounts (OBSERVED)

- User:~2026-36867-71 (meta): zero captures — user page, user subpages (prefix),
  /wiki/ form, Special:Contributions. (honest zeros)
- User:~2026-28355-02 (meta): zero captures — same forms. (honest zeros)
- NOTE: Special:Contributions pages are dynamic; Wayback coverage of any
  contributions page is structurally poor. Zero here = no archived copy exists,
  not "account never edited". (INFERENCE on interpretation, OBSERVED on zero.)

## 6. Seed article + security.wikimedia.org (OBSERVED)

- Seed: https://diff.wikimedia.org/2026/10/05/openai-rogue-agent-activities-found-on-wikimedia-projects/
  4 captures: 20261005175322, 20261005194509, 20261005212323, 20261006040322 (all 200).
  Well covered.
- Evidence CSV: https://security.wikimedia.org/data/openai-wikimedia-edits-2026-10-04.csv
  HAS ONE Wayback capture: 20261005175659, 200, digest 3UFVL2XM6UKOXNZJF3ZVOXWAWD4MB3WA.
  (OBSERVED — MAJOR: the exact evidence file is archived, content recoverable.)
- security.wikimedia.org prefix coverage (2026): /, /blog/, /bug-bounty/, /contact/,
  /hall-of-fame/, /workflow-and-intake/ all have 2026-01..03 captures; the archive-diver
  claim "index ends 2026-05-13" does NOT hold domain-wide — needs re-scoping to the
  specific path it was measured on. (OBSERVED; correction to upstream claim.)

## 7. Open / pending

- 54-diff-URL table: script still running (raw/check-diff-urls.sh, results ->
  raw/diff-coverage-results.txt).
- bg.wikipedia.org diff=12923296 and commons ?diff=1213513506: target page titles not
  recoverable from the CSV; archive check would need the resolved title (API lane).
- enwiki User_talk:Example/sandbox (test wiki) not yet checked.
