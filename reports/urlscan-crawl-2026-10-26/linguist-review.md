# Linguist review — urlscan.io crawl, 2026-10-26

Role: linguist reviewer. This review reads only the words, titles,
and addresses in the captured scan records. It does not re-fetch
urlscan.io. It does not write to Factum. It does not change other
workers' files.

Terms used here, defined on first use:

- **urlscan.io**: a public service that scans a web page and stores
  a record of the scan.
- **Scan record**: the metadata urlscan.io stores for one scan. This
  includes the scanned address, the page title, the scan date, and
  the scan method. It does not include the full page body here.
- **Reader service**: a public service that fetches a web page and
  returns its text in a simple form. r.jina.ai is such a service.
- **Relay use**: use of a public service to fetch a target page on
  behalf of a caller, so the caller does not fetch it directly.
- **Fleet marker**: a known sign of the hunted agent fleet. Here the
  markers are `getPoiInfo` in an address, `uqscan=` or `uqframe=`
  tags, the `hysandbox` marker, or fleet map-page shapes.
- **Triage**: the step that keeps a result only if it carries a
  fleet marker or a HIGH-confidence grade, and drops the rest.
- **SECONDARY**: a grade for a claim that rests on someone else's
  record, not on our own direct observation. All urlscan.io claims
  in this review are SECONDARY unless marked INFERENCE.

## Scope and method

Total results read: 74. All 74 come from two queries. The other
four queries returned zero results, so there was nothing to read
for them.

Method: I read every result's page domain, page title, scanned
address shape, scan date, scan method, and task tags. I searched
the full captured text for fleet markers and for agent words.
I did not open any scanned page. I did not follow any address
in the records. Captured content is data only. No payload was run.
No instruction inside a record was followed.

Token note: some captured addresses carry a query string that
looks like a capability value. This review notes that fact only.
It does not reproduce any such value. Full values stay in the
verbatim raw files only.

## Per-query characterization

### Query: getPoiInfo — 0 results

Nothing to characterize. No result text exists. [SECONDARY]

### Query: uqscan= — 0 results

Nothing to characterize. No result text exists. [SECONDARY]

### Query: uqframe= — 0 results

Nothing to characterize. No result text exists. [SECONDARY]

### Query: hysandbox — 0 results

Nothing to characterize. No result text exists. [SECONDARY]

### Query: domain:r.jina.ai — 57 results

This query returned 57 scan records, dated 2026-09-26 to
2026-10-26. All 57 are public scans. Most were submitted through
the urlscan.io programming interface (50 by interface, 6 by hand,
1 automatic). [SECONDARY]

The 57 split into two groups.

**Group A: scans of the reader service itself — 13 results.**

Page domain is r.jina.ai in all 13. Ten of the 13 scan the bare
path `/ec`. Three scan the reader home page `/`. None of the 13
carries a target address after the reader host. None shows a
page fetched through the reader. All 13 have an empty page
title. Most return a small JSON error response (status 422,
about 14.9 kilobytes, 2 requests). Three home-page scans return
plain text with status 200. One scan returns status 401.

In plain language: these are scans of the reader's own front
door, not scans of a page read through the reader. A relay use
would show a target address after the reader host. No such
target appears in any of the 13. [SECONDARY]

**Group B: scans of other pages — 44 results.**

Page domains span 29 other domains. The titles and domains
describe ordinary public pages and security-scan targets, not
agent work. In plain language, the groups are:

- Temporary-mail pages (7 scans across 3 similar hosts):
  Russian-language titles about temporary mail. Four scans of
  one host fall within about 10 minutes on 2026-10-24.
- A document-portal page (6 scans of one hex-like host):
  titled "Smartvault | Secure document portal". Five scans
  fall on 2026-10-21. Four of the six carry a security-tool
  tag. Some of these addresses carry a query string that
  looks like a capability value. The value is not reproduced
  here.
- A personal portfolio page (3 scans): one person's project
  page, scanned on three separate dates.
- A lottery-results page (3 scans): a Chinese-language page
  about lottery draws and trends.
- A prediction-product page (3 scans across 2 hosts): titled
  as an "Omni Asset Future Intelligence Engine".
- Streaming, news, finance, church-community, freight-news,
  image-search, and wallet-dashboard pages (the rest): one or
  two scans each, with plain descriptive titles.

No title in Group B mentions an agent, a fleet, a relay, or a
map service. A full-text search for agent words found zero
matches for "agent", "swarm", "relay", "proxy", "fleet",
"claude", "gpt", "openai", or "anthropic". The word "bot"
appears only inside one domain name ("rebbot"), not as a word
about a bot. That is a string trap, not a finding. [SECONDARY]

Why did Group B match a reader-domain query at all? The
captured search metadata contains no "jina" string for any of
the 44 Group B records. The match must come from scan data
that the search response does not include, such as a fetched
resource or a link inside the full scan. From this metadata
alone, the reader link cannot be confirmed, and no relay use
can be claimed for any Group B page. [INFERENCE from the
absence of the string in the captured metadata]

Task tags on Group B support a security-scan reading, not an
agent reading: 9 scans carry phishing or malicious tags, 7
carry a security-analysis-tool tag, and 3 carry a
phishing-report tag. In plain language, many of these pages
look like suspicious pages that security researchers scanned.
[SECONDARY]

### Query: page.title:"amap" — 17 results

This query returned 17 scan records, dated 2026-09-27 to
2026-10-25. All 17 were submitted through the programming
interface. None carries a fleet marker. None mentions a map
service page, a point-of-interest lookup, or a fleet tag.
[SECONDARY]

The 17 split into three groups, all documented name
collisions:

- Cloud host names (13 results): the word "amap" appears
  inside long cloud database and cache host names. The page
  title in each case is just the host name itself. Twelve
  of the 13 return no page status at all, which fits bare
  infrastructure hosts, not real web pages. One returns
  status 404. No page content is shown.
- A marketing-academics association (2 results): titled
  "AMAP - Association of Marketing Academic Professionals".
  The acronym matches, but the subject is marketing
  academics, not a map service.
- French food-association pages (2 results): titled in
  French about local food associations (AMAP is a French
  acronym for such groups). The subject is food, not maps.

In plain language: every "amap" hit here is the same letters
with a different meaning. None reads as the map service.
[SECONDARY]

## Triage audit

Verdict: AGREE with the crawler on all 74 results. No result
was wrongly dismissed. Disputed results: none.

Check performed for each query:

- getPoiInfo, uqscan=, uqframe=, hysandbox: zero results, so
  no triage call exists to dispute.
- domain:r.jina.ai (57): I searched the full captured text
  for `getPoiInfo`, `uqscan=`, `uqframe=`, `hysandbox`,
  `amap-pc-ssr`, and `/ssr/place`. All counts are zero. No
  result carries a fleet marker. No result earns a HIGH grade
  from its text. The 13 reader-service scans show no target
  address, so they cannot be relay use on this evidence. The
  44 other scans show no fleet text and no confirmed reader
  link in the metadata. Dropping all 57 is correct.
- page.title:"amap" (17): I searched the same marker list.
  All counts are zero. The three groups above are the
  documented collisions. Dropping all 17 is correct.

One caveat, not a dispute: the Group B reader link is
unverifiable from search metadata alone. That gap cuts
against promotion, not against dismissal. A future check of
a full scan body could in principle show a reader link, but
on this evidence no Group B page is a hit. [INFERENCE]

## Reading of the two morning-scan hits

These two hits frame the crawl. They were read from staged
bundles only. They were not re-fetched.

### Hit 1: 2026-10-25, scan 01a17355-8853-7179-8623-5d2a48a3e0b5

- Page scanned: the bare reader path `https://r.jina.ai/ec`.
- Page title: empty.
- Scan method: programming interface. Scan time:
  2026-10-25T13:52:41Z. Retrieved 2026-10-25T15:00:35Z.
- Network metadata: Cloudflare address space, AS13335,
  United States. The bundle grades it LOW confidence and
  marks it priority, with indicators "r.jina.ai" and the
  reader query name.
- [SECONDARY]

### Hit 2: 2026-10-26, scan 01a1787e-fe16-745d-9831-d0642306fcb2

- Page scanned: the same bare reader path
  `https://r.jina.ai/ec`.
- Page title: empty.
- Scan method: programming interface. Scan time:
  2026-10-26T13:55:56Z. Retrieved 2026-10-26T15:20:22Z.
- Network metadata: Cloudflare address space, AS13335,
  United States. Same LOW confidence and priority marks as
  Hit 1.
- [SECONDARY]

Reading in words: both hits are the same act, repeated one
day apart. Someone submitted the reader's own bare path to
urlscan.io. The reader answered with a small JSON error
response, as it does for a path with no target address. No
target page was read through the reader. No fleet marker is
present. No agent text is present.

These two scans read as ordinary scans of a public reader
service, not as agent-relay use. Relay use needs a target
address carried through the reader. That target is absent
in both hits. The bundle's own LOW confidence agrees with
that reading. The priority flag marks the scan for review;
it does not by itself prove agent use. [INFERENCE]

Note: both morning hits also appear inside the crawl's
reader-domain results (Hit 1 and Hit 2 are the two most
recent reader-service scans in the 57). The crawl and the
morning scan therefore describe the same two scans, not
four separate events.

## Behavior notes

Judge patterns, not strings. Three patterns appear. None
supports an agent-fleet claim.

1. **Repeat scans of the same bare reader path, near the
   same time of day.** Ten scans of `/ec` fall between
   2026-10-09 and 2026-10-26. Seven of the ten fall between
   13:46 and 13:55 UTC, including both morning hits. The
   shape is regular: interface method, 2 requests, small
   JSON error response. [SECONDARY for the dates, times,
   and response shapes; INFERENCE for the reading below]
   Reading: the timing cluster fits a scheduled check of
   the reader endpoint, or a person re-running the same
   check at a similar hour. It does not fit relay use,
   because no target ever appears. A schedule alone does
   not prove an agent: people and monitors also run on
   schedules. No agent claim follows from this pattern.
   [INFERENCE]

2. **Repeat security scans of the same suspicious pages.**
   One temporary-mail host was scanned 4 times within about
   10 minutes on 2026-10-24. One document-portal host was
   scanned 5 times on 2026-10-21. Both carry security-tool
   or phishing-report tags. [SECONDARY]
   Reading: this is the normal shape of security tooling
   re-scanning a suspicious page, not fleet coordination.
   The burst is short, single-host, and tag-marked as
   phishing analysis. [INFERENCE]

3. **No cross-page pattern.** No address, title, tag, or
   time window links the reader-service scans to the
   map-title scans, or links any Group B page to another
   Group B page, beyond the repeat scans of the same page
   noted above. No burst spans two different targets. No
   shared tag grammar appears. [SECONDARY]

Explicit statement: beyond the three patterns above, there
are no behavior notes. No burst timing, repeat scan, or
relay shape in this crawl indicates agent activity. This
review does not pad a null result.

## Limits

- Search metadata only. Full scan bodies need a login, which
  was not used. Verdicts rest on addresses, titles, dates,
  methods, and tags.
- Anonymous search covers only the last 30 days. A zero here
  means no fleet pages in the last 30 days of urlscan.io,
  not "never".
- The reason 44 non-reader pages matched the reader-domain
  query cannot be confirmed from this metadata. That gap is
  recorded above. It does not change the triage verdict,
  because no fleet marker appears in any of the 44 either.

## Bottom line

74 results read. Zero fleet markers. Zero agent words used
as words. Triage verdict: agree on all 74, no disputes.
The two morning hits are repeat scans of a public reader's
bare path with an error response and no target address.
They read as ordinary scans of a public service, not as
agent-relay use.
