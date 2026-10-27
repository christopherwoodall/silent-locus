# Lane summary: urlquery — broad agent-egress hunt

## Scope and method

- Lane: urlquery, for the broad agent-egress hunt.
- Run date: 2026-10-27 (UTC). Fleet B ran 2026-10-27 about 05:32–05:35 UTC.
- Method: read-only urlquery API search and report detail. No POST. No login.
- Tool: `uq.py` search and report, with a surrogate credential. One tool note:
  the bundled script has a stale credential-helper path. The runs used
  `PYTHONPATH=/opt/muse/skills/custom-connector-setup/bin` as a workaround.
- No Factum writes. No commit. No push. No branch change. Files stay
  uncommitted for the coordinator.

## Terms used in this note

- SECONDARY: evidence from a third party, not first-hand capture. All
  urlquery hits are SECONDARY by default.
- Behavior shape: a pattern of actions, such as recon then upload. A host
  name alone is not a behavior shape.
- String-only: the search term appears, but no behavior is shown.
- Detail-checked: a full report was fetched and its requests were read.
- Capped sample: only part of a large total was fetched. A capped sample
  is never the full set.
- New submission: a report dated after Fleet B ran. New to Fleet B fetch:
  a report Fleet B did not fetch, but dated before Fleet B ran.
- Post-Fleet-B cut: 2026-10-27T05:35:00Z. Reports after this time are new
  submissions. Reports before it may still be new to Fleet B fetch.

## Headline verdict

No new agent behavior was found. No new host was found. No live metadata
reach, live upload probe, or live namespace escape was found.

Three LOW items survive. All are new instances or continuations of known
classes. None is a new behavior. None names a model. Model identity stays
unidentified unless evidence names it. No row in this lane names a model.

## Ranked candidates

### 1. LOW — Exchange-template site loads images from a known OSS bucket

- Report ID: e4a7d94c-8ba0-4d9a-a10c-099b2ab31677.
- Date: 2026-08-20T14:53:11Z. Submitted URL: trustxx.co.
- Behavior shape: none shown. This is image loading, not upload or egress.
- Detail-checked: yes. 98 requests. 79 GET, 10 POST, 9 OPTIONS.
- 32 GETs go to the echo-res20 bucket host in Hong Kong. All POSTs go to
  the site's own API host and chat host. No POST goes to the bucket.
- Grade: SECONDARY. Confidence: LOW. This is a string and shape match to a
  known template family, not agent evidence.
- Caveat: the bucket path shape matches Fleet B's trustexc row. The site
  family is the same. The agent link is absent.
- New versus Fleet B: NEW TO FLEET B FETCH, not a new submission. Fleet B
  fetched only the trustexc row of this 8-row bucket set. The other 7 rows
  are the same family. This row adds a second site to the family. It adds
  no new behavior and no new host class.

### 2. LOW — Exchange SPA cluster continues with new submissions

- Newest detail-checked report ID: dd8433a0-0fa1-40ca-af14-d1306266d437.
- Date: 2026-10-27T07:30:34Z. Submitted URL: smaflowi.vip.
- Behavior shape: none shown. This is a scam SPA being rescanned, or a
  monitoring loop around one site. It is not an agent.
- Detail-checked: yes, one row. 80 requests. 61 GET, 10 OPTIONS, 9 POST.
- 30 GETs go to the ysviposs OSS bucket. 9 POSTs go to the qtapi API host.
  No PUT goes to the bucket. No POST goes to the bucket.
- Grade: SECONDARY. Confidence: LOW for the cluster shape, no confidence
  for any agent link.
- Caveat: the fetched sample is capped. The cluster shape is proven only
  for detail-checked rows. Other rows in the sample were not detail-checked.
- New versus Fleet B: CONTINUATION, with new submissions. The aliyuncs
  sample holds 20 rows dated after the Fleet B cut. They match the same
  cluster. The cluster did not change shape.

### 3. LOW — One new portfolio page matches the word routify

- Report ID: 342ac40c-aabe-4b27-88d2-0bdd669e9aeb.
- Date: 2026-10-27T11:53:17Z. Submitted URL: charlesg.appwrite.network.
- Behavior shape: none shown.
- Detail-checked: yes. 66 requests. 65 GET, 1 OPTIONS. Zero requests
  mention routify. Zero requests go to any routify host. Zero POSTs.
- Grade: SECONDARY. Confidence: LOW. This is string-only.
- Caveat: the detail API does not return full page body text. The match
  location could not be confirmed in the returned fields. The match is
  presumed page or asset text.
- New versus Fleet B: NEW SUBMISSION. It is the only routify row dated
  after the Fleet B cut. It is not new behavior and not the proxy host.

## Screened out, with reasons

- Bare proxy host row 0bec7c6c, 2026-08-16: detail fetch now succeeds
  (Fleet B got 401 twice). 2 GETs to the proxy host itself. No path. No
  proxy_temp_file path. No PUT. No POST. Bare host string only. Overlap
  with Fleet B. Not a hit.
- Vendor routify hosts: routify.alibaba-inc.com, routify-online, and
  routify-pub all return 0. No new vendor traffic in this lane.
- Sanmaohe: the bucket host, the short name, and the upload path shape all
  return 0. No seed reproduction.
- Exact Cohere payload string PROBE_PAYLOAD_ABC123: 0. The short term
  PROBE_PAYLOAD returns 4 rows. All 4 are one docs site about honeypot
  benchmarking, in a 10-second crawl window, 2026-09-07. All are GET only.
  No upload. No OSS host. Not the Cohere payload.
- Metadata sign-in page 45a8f376, 2026-10-24: detail-checked. 218 requests.
  216 GET, 1 OPTIONS, 1 POST. The POST goes to the site's own challenge
  host. No request goes to metadata.google.internal. String-only.
- Trading-site builder page d4a013c7, 2026-10-27: detail-checked for
  unshare. 40 requests. The term unshare appears in no request. One POST
  goes to a search telemetry host. String-only.
- DNS-monitor page ad59ef43, 2026-09-13: detail-checked for resolv.conf.
  16 GETs, all to the submitted DNS-monitor hostname itself. No recon
  chain. String-only.
- Shop page 226f3d6c, 2026-10-27: the only post-Fleet-B oss-cn row.
  Detail-checked. 46 requests. Zero requests go to any oss-cn host. The
  match lives in page content only. String-only.
- S3 block page f7fbdb16, 2026-10-27: detail-checked. 5 GETs. 2 GETs go to
  the S3 bucket host. The page title is Blocked. Path shape is a hex
  directory plus block_screen.html with an id parameter name. No upload.
  No agent marker. Screened out.
- S3 landing page 19a51b8e, 2026-10-27: detail-checked. 4 GETs. 1 GET goes
  to the S3 bucket host. The rest go to a login-themed host. This is a
  served landing page, not agent egress. Screened out.
- Trace beacon rows: 50 fetched for trace/v1/report. 18 are direct-mail
  beacon submissions on a dm host. 30 are Cloudflare Workers playground
  pages. 2 are tinyurl pages. Path shape only is recorded here. No query
  values are copied. No agent marker appears in any sampled row. This
  matches Fleet B's beacon triage. Not a hit.
- One resolv.conf row is a public fleet report page. It is known hunt
  context, not new behavior. It is not ranked.
- One metadata row is an AI-agent identity product page. It matches
  through page content only. It was not detail-checked. It shows no
  behavior. It is not ranked.

## Shape-by-shape verdicts

### Shape 1: cloud-metadata reach — NOT FOUND

- 169.254.169.254: total 0. Same as Fleet B.
- fd00:ec2::254: total 0.
- 100.100.100.200: total 0. Same as Fleet B.
- metadata.google.internal: total 223, 50 fetched. Zero of 50 rows show
  the metadata host as a requested host in the search summary. One row
  detail-checked: no metadata request. The set is page-content matches.
  11 of 50 rows are sign-in pages for one assistant product. No agent
  metadata reach is shown.

### Shape 2: object-storage upload — NOT FOUND

- No detail-checked row shows a PUT or POST to any object-storage host.
- smaflowi rows: GET only to the bucket. POSTs go to the API host.
- echo-res20 rows: GET only to the bucket. POSTs go to the own API host.
- S3 rows: GET only to the bucket.
- oss-cn post-Fleet-B row: no bucket request at all.
- Upload-flag totals are large: upload-file 2,533; curl -o 1,348;
  wget -O 1,036. Samples are app pages, docs pages, and tutorial pages.
  No download-then-upload chain was detail-checked in those samples.
  The totals alone prove nothing about behavior.

### Shape 3: named probe hosts — ONLY THE KNOWN BARE HOST

- routify: total 79. 78 distinct rows fetched. Only one row touches a
  routify host in its requests: the known bare host row 0bec7c6c.
- All other routify rows match through page content only. Most are
  ordinary sites. The word also names a web framework, which explains
  many matches.
- Vendor hosts: all 0. Sanmaohe: all 0. proxy_temp_file: 0.
  The proxy_temp_file path shape appears nowhere in this lane.

### Shape 4: user-namespace escape — NOT FOUND

- unshare: total 1,460, 50 fetched. The sample is dominated by repeated
  submissions of a few app pages: 26 of 50 for one trading-site builder,
  8 of 50 for one app platform page.
- One row detail-checked: the term appears in no request. No unshare
  command chain is shown in any detail-checked row.
- Flag-form totals are not subsets. unshare -U returns 2,771, which is
  larger than unshare at 1,460. unshare -Urm returns 1,461. The search
  parser treats flag forms in its own way. Do not compare these totals
  as nested sets.

### Shape 5: download-then-execute — NOT FOUND

- curl -o: total 1,348, 48 fetched. wget -O: total 1,036, 50 fetched.
- Samples are app platform pages, news pages, shop pages, and tutorial
  pages. One curl-o row is an agent-tutorial page. A tutorial page is
  not a download-then-execute chain.
- No row in these samples was detail-checked for an execute step. No
  chain is claimed.

### Shape 6: recon-then-egress — NOT FOUND

- resolv.conf: total 95, all 95 fetched. The set is dominated by one
  DNS-test domain: 26 of 95 rows. The rest are docs pages and one known
  fleet report page. No recon-plus-network chain is shown.
- uname -a: total 738, 49 fetched. Samples are generic pages: file
  shares, news, shops, login pages. No chain is shown.
- Recon alone is silent by the scope rule. No row shows recon plus a
  network call in one chain.

## Burst and timing notes

- Aliyuncs cluster: 99 fetched rows span 2026-10-26T23:45Z to
  2026-10-27T07:30Z. 98 rows are smaflowi.vip. 1 row is a news site.
  Median gap is 3.6 minutes. This matches Fleet B's median for its 49
  rows. The loop is steady, through the night UTC. It is a rescan or
  monitoring loop, not a burst with a start and end.
- Routify rows: sparse, from 2025-10-27 to 2026-10-27. No burst.
- PROBE_PAYLOAD rows: 4 rows in 10 seconds. That is one docs crawl.
- echo-res20 rows: spread from 2026-03-26 to 2026-10-26. No burst.
- Unshare sample: repeated same-day resubmissions of the same pages.
  That is rescan behavior, not an event burst.
- Time-of-day windows: no agent window was found. The only steady window
  is the overnight smaflowi loop, which is not agent evidence.

## Query table: exact totals and fetched counts

Totals are from the run on 2026-10-27. Totals move as new reports arrive.
Fetched counts are rows in fetch files. Probe rows (limit 1) are not
counted as fetched samples, except where the fetch file itself is the
full set. Rows overlap across queries. The sum of fetched rows is not a
count of distinct reports.

| Query | Total | Fetched | Note |
|---|---|---|---|
| 169.254.169.254 | 0 | 0 | Totals-only probe |
| fd00:ec2::254 | 0 | 0 | Totals-only probe |
| metadata.google.internal | 223 | 50 | Newest 50; 0 requested-host matches |
| 100.100.100.200 | 0 | 0 | Totals-only probe |
| upload-file | 2,533 | 50 | Newest 50; probe said 2,532, total moved |
| proxy_temp_file | 0 | 0 | Totals-only probe |
| PROBE_PAYLOAD | 4 | 4 | Full set; one docs site |
| PROBE_PAYLOAD_ABC123 | 0 | 0 | Exact Cohere string; full check |
| put_probe | 0 | 0 | Totals-only probe; same as Fleet B |
| aliyuncs.com | 48,965 | 99 | Newest 99; Fleet B total was 48,945 |
| oss-cn- | 6,649 | 99 | Newest 99; Fleet B total was 6,648 |
| blob.core.windows.net | 21,086 | 49 | Newest 49; capped sample |
| storage.googleapis.com | 173,619 | 50 | Newest 50; capped sample |
| s3.amazonaws.com | 86,193 | 50 | Newest 50; capped sample |
| r2.dev | 11,105 | 50 | Newest 50; capped sample |
| routify | 79 | 78 distinct | Near-full set; 1 row unreachable by paging |
| unshare | 1,460 | 50 | Newest 50; capped sample |
| unshare -U | 2,771 | 50 | Newest 50; parser caveat below |
| unshare -Urm | 1,461 | 50 | Newest 50; parser caveat below |
| curl -o | 1,348 | 48 | API returned 48, not 50 |
| wget -O | 1,036 | 50 | Newest 50; capped sample |
| resolv.conf | 95 | 95 | Full set |
| uname -a | 738 | 49 | Newest 49; capped sample |
| routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com | 1 | 1 | Only the known bare host row |
| routify-file-proxy-sg | 0 | 0 | Hyphen-form caveat below |
| routify.alibaba-inc.com | 0 | 0 | Totals-only probe |
| routify-online.alibaba-inc.com | 0 | 0 | Totals-only probe |
| routify-pub.alibaba-inc.com | 0 | 0 | Totals-only probe |
| sanmaohe.oss-cn-beijing.aliyuncs.com | 0 | 0 | Totals-only probe |
| sanmaohe | 0 | 0 | Totals-only probe |
| upload/test.bin | 0 | 0 | Totals-only probe |
| url.domain:routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com | 0 | 0 | Syntax unverified; not absence |
| url.domain:sanmaohe.oss-cn-beijing.aliyuncs.com | 0 | 0 | Syntax unverified; not absence |
| routify date:[2026-10-27 TO 2026-10-28] | 1 | 1 | Only the new portfolio row |
| smaflowi | 0 | 0 | Paradox caveat below |
| ysviposs | 0 | 0 | Paradox caveat below |
| qtapi.flowmaeri.top | 201 | 50 | Same rows as the aliyuncs cluster |
| trustexc.top | 1 | 1 | Only the Fleet B row |
| echo-res20.oss-cn-hongkong.aliyuncs.com | 8 | 8 | Full set; 1 Fleet B row, 7 new to fetch |
| f4nt34-oowqn-vqmf98.oss-cn-chengdu.aliyuncs.com | 0 | 0 | Totals-only probe |
| 50c5.cc | 0 | 0 | Totals-only probe |
| trace/v1/report | 230 | 50 | Newest 50; beacon shape |

Total fetch-file rows: 1,083, across 28 fetch files. Detail-checked
rows: 11. All other fetched rows were screened by search row only:
submitted URL, date, title, and summary hosts. They were not
detail-checked. No behavior claim is made for them.

## Detail-checked rows

| Report ID short | Date | Submitted host | What the detail showed |
|---|---|---|---|
| 342ac40c | 2026-10-27 | charlesg.appwrite.network | 66 requests, no routify request |
| 45a8f376 | 2026-10-24 | claude.ai | 218 requests, no metadata request |
| a8da83f0 | 2026-09-07 | uhbs.github.io docs | 29 GETs, no payload upload |
| e4a7d94c | 2026-08-20 | trustxx.co | 32 bucket GETs, POSTs to own API only |
| 226f3d6c | 2026-10-27 | aanbiedingenzrpnl.shop | 46 requests, zero bucket requests |
| d4a013c7 | 2026-10-27 | dforge.site | 40 requests, no unshare request |
| ad59ef43 | 2026-09-13 | DNS-monitor hostname | 16 GETs to itself only |
| 0bec7c6c | 2026-08-16 | routify proxy host | 2 GETs, no path, no PUT |
| dd8433a0 | 2026-10-27 | smaflowi.vip | 30 bucket GETs, POSTs to API host only |
| f7fbdb16 | 2026-10-27 | S3 block page | 5 GETs, page title Blocked |
| 19a51b8e | 2026-10-27 | S3 landing page | 4 GETs, landing page only |

Full report IDs are in the raw detail files. Short IDs above are the
first 8 characters. No signed query strings, signatures, tokens, or
credential-shaped values are copied in this note. Raw files keep full
bytes, per the evidence rule.

## Sampling limits and parser caveats

- Large totals are barely sampled. aliyuncs: 99 of 48,965. oss-cn:
  99 of 6,649. Storage totals: 49–50 rows each out of tens of thousands.
  A null in a capped sample is not a null in the set.
- Routify is the exception: 78 of 79 distinct rows fetched. One row is
  unreachable through offset paging. A recheck returned the same 78
  distinct rows. The missing row is not identified. Do not claim full
  routify coverage.
- A limit of 50 returns at most 49 rows per call in this run. Paging by
  50 therefore skips one offset. The gap row was fetched separately.
- Hyphen-form caveat: the term routify-file-proxy-sg returns 0, while
  the full host returns 1 and routify returns 79. The hyphen form is
  unreliable. Its zero is not absence.
- Flag-form caveat: unshare -U returns more than unshare. Flag forms
  are not subsets. Do not nest these totals.
- url.domain: caveat: both url.domain: forms return 0, even though the
  bare proxy host row exists and is returned by plain-term search. The
  syntax form used here is unverified. These zeros are not absence.
- Term-zero paradox: smaflowi returns 0, yet 98 fetched aliyuncs rows
  were submitted from smaflowi.vip. ysviposs returns 0, yet 30 requests
  in one detail-checked row go to the ysviposs bucket host. The search
  term match does not cover every submitted-URL string in the same way.
  A term zero means no match under that query form. It does not prove
  the string is absent from the corpus.
- Match-location gap: for 5 detail-checked rows, the search term appears
  in no request URL, no header, and no returned script blob. The detail
  API does not return full page body text. The match location for those
  rows is unconfirmed. They are graded string-only, not behavior.

## Fleet B comparison

- Fleet B totals: aliyuncs 48,945; oss-cn 6,648; routify 78; sanmaohe 0;
  metadata 0; put_probe 0. Fetched: 49 rows per non-zero query.
- This lane totals: aliyuncs 48,965 (+20); oss-cn 6,649 (+1); routify 79
  (+1); sanmaohe 0; metadata address 0; put_probe 0.
- This lane fetched: routify 78 distinct of 79; aliyuncs 99; oss-cn 99;
  resolv.conf 95 of 95; echo-res20 8 of 8; PROBE_PAYLOAD 4 of 4; plus
  49–50 row samples for the other shapes.
- All 49 Fleet B aliyuncs IDs, all 49 Fleet B oss-cn IDs, and all 49
  Fleet B routify IDs reappear in this lane's fetches. Overlap is
  complete for the Fleet B fetched sets.
- New submissions since Fleet B: 20 aliyuncs cluster rows, 1 oss-cn row,
  1 routify row. All are covered above. None changes the verdict.
- New to Fleet B fetch, but old: 29 older routify rows, 50 older oss-cn
  rows, 7 echo-res20 rows. All screened. None adds a behavior.

## Failures and open questions

- Failure: none in this lane, except the known tool-path workaround
  above. Fleet B's 401 on the bare host detail did not recur. The retry
  succeeded.
- Open: where does the search term match for rows whose detail shows no
  term in requests or scripts? The detail API does not expose page body
  text. A different detail method would be needed to pin the match.
- Open: the 1 unreachable routify row. Its identity is unknown.
- Open: GitHub code search is still the largest gap for shapes 4, 5,
  and 6. That is another lane's work, not this lane's.
- Open: Shodan was not used. No concrete infra signal in this lane
  justifies it.

## Evidence files

- Raw captures:
  `data/lanes/agent-egress-broad-hunt/raw/urlquery/`
- Per-query JSON files, each with a `.PROVENANCE.txt` file (source URL,
  retrieval time, method) and a `.sha256` file.
- Dir checksum file: `SHA256SUMS` in the same dir (162 lines, verified).
- Runner scripts in the same dir: `_run_probes.py`, `_run_fetch.py`,
  `_run_detail.py`, plus `_fleetb_overlap_ids.json` (Fleet B fetched IDs
  used for overlap checks).
- This lane note:
  `reports/agent-egress-broad-hunt/lanes/urlquery.md`
- No files were committed, pushed, or written to Factum. No files under
  `data/records/` or `data/.local/` were touched.
