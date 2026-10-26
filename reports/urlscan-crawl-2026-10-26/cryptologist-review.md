# Cryptologist review — urlscan.io crawl, 2026-10-26

Role: cryptologist reviewer. Scope: identifiers, hashes, and encodings.
Read-only review. No Factum write. No commit. No push.

Terms, defined on first use:

- UUID: a 36-character scan ID. Format: lower-case hex digits and hyphens.
- ASN: the number of the network that owns an IP address.
- Dual-stack: one service that answers on both IPv4 and IPv6.
- Base64: an encoding that turns bytes into letters, digits, and symbols.
- Percent-encoding: a URL form that writes special bytes as `%` plus hex digits.
- Fleet marker: a known fleet sign. Examples: `getPoiInfo`, `uqscan=`, `uqframe=`, `hysandbox`.

Grade rule: every claim carries OBSERVED, INFERENCE, or UPSTREAM.
All urlscan metadata is SECONDARY by default. OBSERVED here means
counted in the staged files. It does not upgrade the grade.

## 1. Identifier inventory

Counts come from the verbatim search files. No token-like value
appears in this review. Shapes only.

### 1.1 Counts per query

| Query label | Results | Distinct scan UUIDs | Distinct page domains | Distinct task domains | Distinct page apex domains | Distinct page IPs | Distinct ASNs |
|---|---|---|---|---|---|---|---|
| getpoiinfo | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| uqscan-tag | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| uqframe-tag | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| proxy-marker | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| relay-jina-reader | 57 | 57 | 30 | 31 | 21 | 29 | 8 |
| title-amap | 17 | 17 | 14 | 15 | 6 | 6 | 5 |
| Total | 74 | 74 | — | — | — | — | — |

Notes on the table (OBSERVED):

- In every result, the record ID equals the task scan UUID. One key
  serves both roles. Shape: 36 characters, lower-case hex and hyphens.
- The urlscan result API link also embeds the same UUID. Shape only.
- relay-jina-reader IP count of 29 includes 1 missing value. Real
  addresses: 26 IPv4 and 2 IPv6. One result has no IP.
- relay-jina-reader ASN count of 8 includes 1 missing value.
- title-amap IP count of 6 includes 1 missing value. Real addresses:
  4 IPv4 and 1 IPv6. Twelve of the 17 title results lack IP, ASN,
  and status alike. IP and ASN comparison is weak for that query.
- All 74 results are public. Task method: 67 by API, 6 manual,
  1 automatic. No result carries a label. Submitter data is empty.

### 1.2 Structured tokens in URLs

Query parameters (OBSERVED):

- Four zero-hit queries: no URLs, no parameters.
- relay-jina-reader: only 6 of 57 page URLs carry a query string.
  Only one parameter name appears in the whole haul: `client`.
  It occurs 6 times, with 1 distinct value. Value shape: 14
  characters, lower-case letters only. All 6 sit on one page domain.
- title-amap: 0 of 17 page URLs carry a query string. No
  parameter names at all.
- Task URLs add nothing new: 1 task URL carries the same `client`
  name. No other parameter name appears anywhere.

Percent-encoding (OBSERVED):

- 0 of 74 page URLs contain a `%` character.
- 0 of 74 task URLs contain a `%` character.
- No encoded payload hides in page or task URLs. No double-encoding
  can hide either, since no encoding is present at all.

Path segments (OBSERVED):

- Base64-looking path segments: 0. Test: length 16 or more, with
  mixed case and digits. None pass.
- Long path segments (length 40 or more): 5, all in task URLs.
  All 5 carry the same single value. Shape: 40 characters, all
  lower-case hex. This is the length of a SHA-1 hex digest.
  All 5 task URLs sit on one mail-tracking domain. All 5 page URLs
  sit on one other host. Task domain never equals page domain here.
- Host labels: one apex domain carries 6 page hosts whose first
  label is 34 characters, all lower-case hex. Same host, scanned
  6 times. One label shape, one apex, no spread across hosts.

Scan dates (OBSERVED):

- relay-jina-reader: 2026-09-26 to 2026-10-26.
- title-amap: 2026-09-27 to 2026-10-25.
- Both sit inside the anonymous 30-day window. A zero outside
  that window is not covered.

## 2. Hidden structure

### 2.1 Repeated UUIDs across queries

None (OBSERVED). Cross-query UUID overlap is 0. All 74 scan UUIDs
are distinct. No scan is shared between the two non-empty queries.

### 2.2 Shared IPs and ASNs

Real cross-query IP overlap: 0 (OBSERVED). One apparent shared IP
was a missing-data artifact: both queries hold results with no IP,
and blank values group together. That is not a shared address.

Cross-query ASN overlap: only AS13335, Cloudflare (OBSERVED).
That ASN is a giant public fronting network. Shared Cloudflare
fronting is not coordination (INFERENCE).

Within relay-jina-reader (OBSERVED):

- 5 real IPs serve more than 1 page domain. Most domains on one
  real IP: 5.
- AS13335 serves 12 page domains. One Singapore ASN serves 9.
  One Amazon ASN serves 4. One Fastly ASN serves 2.
- This is shared hosting and shared CDN shape (INFERENCE). Many
  unrelated sites sit behind the same few large networks. No
  cross-host link follows from it.

Within title-amap (OBSERVED):

- 0 real IPs serve more than 1 page domain.
- An early count of 10 domains on one IP was the same blank-value
  artifact as above. All 10 lack an IP. Corrected count: none.

### 2.3 Repeated identifiers: pattern or not

Rule used: a repeat across independent scans is a pattern. A
single odd string is not. A repeat trapped inside one host or
one service is weak. It shows one service config, not coordination.

Findings (OBSERVED, graded as INFERENCE for the judgment):

- `client` value: repeats 6 times, but on 1 page domain only.
  Verdict: single-service config. Not a cross-host pattern.
- 40-character hex segment: repeats 5 times, but as 1 value, on
  1 tracker domain, for pages on 1 host. Verdict: tracker-ID
  shape. Not a fleet marker. Not a cross-host pattern.
- 34-character hex host label: repeats 6 times, but on 1 apex
  domain only. Verdict: one host scanned 6 times. Not a
  cross-host pattern.
- Reader short paths: 10 of the 13 reader page URLs share one
  length class (short path, 2-character first segment or none),
  with no query string. Verdict: front-page scan shape, repeated.
  This is a shape repeat, not an identifier repeat. See section 4.

No identifier in this haul repeats across independent hosts in
a way that shows coordination (INFERENCE).

### 2.4 Hunt-grammar match

Reference shape: `zz=`, `uqscan=`, `uqframe=` as parameter keys,
plus `getPoiInfo` and `hysandbox` as URL markers.

Result: no match, and no near variant (OBSERVED):

- `getPoiInfo`: 0 of 74.
- `uqscan=`: 0 of 74.
- `uqframe=`: 0 of 74.
- `hysandbox`: 0 of 74.
- `amap-pc-ssr`: 0 of 74.
- `/ssr/place`: 0 of 74.
- `zz=`: 0 of 74.
- Bare substrings `uq`, `sandbox`, `poi`, `scan`, `frame`, `tag`:
  0 in all page and task URLs, both non-empty queries.
- One exception: the letters `zz` occur once, inside a hostname
  label, with no equals sign and no parameter role. That is not
  a key. That is not a near variant. It is letter noise inside
  a host name (INFERENCE).

Grammar verdict: the haul carries no fleet-grammar shape at all.
The only parameter grammar in the haul is the single `client`
key on one host. It does not resemble the hunt grammar.

## 3. Morning-hit identifier comparison

Sources: the two staged bundles only. No re-fetch. The Oct 25
bundle holds the IPv6 hit. The Oct 26 bundle holds the IPv4 hit.
Both name Cloudflare AS13335. Full addresses are not repeated
here. The brief already names them.

Same across both bundles (OBSERVED):

- Same page domain: the reader domain.
- Same page URL, same length class.
- Same page title: empty.
- Same grade, same confidence, same lane, same priority flag.
- Same indicator list: 2 indicators, same set.
- Same search query (16 characters).
- Same ASN, same network org, same country, same city.
- Same IP-class tier, label, and detail.
- Same summary text.

Different across both bundles (OBSERVED):

- Different scan UUID. Both IDs match the two IDs named in the
  brief, one per bundle.
- Different scan time: Oct 25 near 13:52 UTC, Oct 26 near
  13:55 UTC. About 24 hours apart.
- Different IP version: IPv6 on Oct 25, IPv4 on Oct 26.

Presence in the crawl haul (OBSERVED):

- Both morning scan UUIDs appear in the crawl haul, in
  relay-jina-reader.
- The Oct 26 scan time equals the newest crawl scan time in
  that query. The crawl haul already contains the Oct 26 hit.
- The morning page URL falls in the 10-result short-path reader
  group described in section 2.3.

Judgment (INFERENCE):

- Same target, scanned twice. Same URL, same domain, same
  indicators, same grade, one day apart. This is a re-scan,
  not two targets.
- The IPv6 versus IPv4 difference means nothing on its own.
  Same ASN, same org, same city, same target URL. That is
  dual-stack fronting: one Cloudflare-fronted service answering
  on both address families. The scan tool saw one family one
  day and the other family the next day.
- The repeat is a pattern of one target re-scanned. It is not
  evidence of fleet coordination. A reader front page re-scanned
  daily is routine scanner behavior.

## 4. Encoding and grammar observations for fleet-marker detection

1. Marker detection on URL strings is a clean negative here
   (OBSERVED). No fleet marker string appears in any page URL,
   task URL, or title in the 74 results.
2. The `domain:` query is weak evidence by itself (INFERENCE).
   Only 13 of 57 relay-query results have the reader as page
   domain. The other 44 have other page domains, and their task
   domain is never the reader. The reader matched through scan
   internals, not through the scanned page URL. Domain presence
   alone cannot prove a proxied fleet page.
3. Reader page URLs carry no proxied target (OBSERVED). All 13
   reader page URLs are bare or carry a 2-character first path
   segment, with no query string. The reader-target form, where
   a target URL follows the reader host, is absent. A future
   marker check should require a target after the reader host,
   not mere reader presence.
4. Missing metadata limits IP and ASN checks (OBSERVED). Twelve
   of 17 title results lack IP, ASN, and status. Blank values
   must never count as shared values. Any shared-IP or
   shared-ASN claim must exclude blanks first, or it will
   invent links from missing data.
5. Tracker-ID shapes are the main false friend in this haul
   (INFERENCE). A 40-character hex path segment and a
   34-character hex host label both repeat, but each stays
   inside one service or one host. Length and hex charset alone
   do not make a fleet token. Spread across hosts is the test,
   and neither shape passes it.
6. No encoding work is needed for this haul (OBSERVED). With
   zero percent-encoding and zero base64-looking segments in
   page and task URLs, there is no encoded layer to decode.
   If a future haul shows encoded blobs, decode before grammar
   matching, since a marker could hide inside an encoded target.

## 5. Bottom line

- Identifier inventory: 74 distinct scan UUIDs, 0 cross-query
  repeats, 1 parameter name in the whole haul, 0 encoded
  payloads in page or task URLs (OBSERVED).
- Hidden structure: none that shows coordination (INFERENCE).
  Shared IPs and ASNs trace to large shared networks. Repeats
  trace to single hosts or single services.
- Morning hits: same target, re-scanned one day apart. IPv6
  versus IPv4 is dual-stack fronting, not a new target
  (INFERENCE).
- Grammar: no hunt-grammar shape and no near variant in the
  haul (OBSERVED). Fleet-marker detection on URL strings
  stays clean negative for this crawl.
