# Adversarial review — urlscan.io crawl, 2026-10-26 (first pass)

Role: adversarial reviewer. Job: try to kill claims.
Method: independent re-check of the raw bytes. No Factum writes.
No commits. No pushes.

Terms, defined on first use:

- Fleet marker: a string that points to the agent fleet. Examples:
  getPoiInfo, uqscan=, uqframe=, hysandbox.
- Triage: the rule that keeps a result only if it carries a fleet
  marker or a HIGH grade. Other results are noise.
- Metadata: the short scan record from search. It has URL, title,
  scan date, IP, and ASN. It does not have the full scan body.
- ASN: the network number that owns an IP address.
- Grade: PRIMARY means our direct observation. SECONDARY means
  other people's data. LOW means low confidence.
- OBSERVED: seen in the bytes. INFERENCE: a conclusion drawn from
  the bytes. UPSTREAM: a claim from urlscan.io itself.

## Independent byte check

Files checked, verbatim, under
`reports/urlscan-crawl-2026-10-26/raw/`:

- 6 search files. All 6 sha256 checks pass.
- Crawl log shows 6 queries, all HTTP 200.
- Counts from the bytes: getpoiinfo 0, uqscan-tag 0, uqframe-tag 0,
  proxy-marker 0, relay-jina-reader 57, title-amap 17. Total 74.
- `hits-draft.json` is an empty list. This matches the bytes.
- `raw/screenshots/` is empty. This matches the zero-hit claim.

## Kill list

### 1. "Honest zero" for fleet markers in the fetched results

Verdict: STANDS, with a scope limit.

Evidence (OBSERVED):

- Independent grep, case-insensitive, over all 6 raw files:
  getPoiInfo 0, uqscan= 0, uqframe= 0, hysandbox 0,
  amap-pc-ssr 0, /ssr/place 0.
- Percent-encoded forms also 0: uqscan%3D, uqframe%3D.
- The triage script checks the same set. Its marker list plus its
  POI shape check cover all 6 strings above.

Scope limit (INFERENCE):

- The zero covers captured search metadata only. Full scan bodies
  need a login. A marker inside a full body would not show here.
- The wider reading, "no fleet pages exist," is KILLED. The crawl
  itself limits the claim to the last 30 days. See gap 3 below.

### 2. "The 74 results are routine noise"

Verdict: STANDS for the fleet question. DOWNGRADED in two places.

Counts (OBSERVED):

- 57 + 17 = 74. True.
- Jina haul: 13 results have page domain r.jina.ai. The other 44
  span 29 other page domains. True.
- Title-amap haul: 13 Azure-host results, 2 amapacad.org.ng
  results, 2 French AMAP food-association results. Total 17. True.
- No title-amap result uses amap.com or gaode.com. True.
- No jina-haul result contains the string "amap" at all. True.

Title-amap classification: DOWNGRADED, minor (INFERENCE):

- The Azure hosts and amapacad.org.ng match documented collisions
  in `scripts/scanners/FALSE-POSITIVES-urlscan.md`.
- The 2 French AMAP food-association pages do NOT appear in that
  file. The file lists Azure, amapacad, jec.jlevm, httpbun,
  livecodes, and mianyang only.
- The classification still holds on the bytes: French titles, no
  fleet markers, no fleet shapes. But the word "documented" is
  overstated for those 2. Fix: add the French AMAP class to the
  file.

Jina mechanism claim: DOWNGRADED (INFERENCE presented as fact):

- Coverage says the domain: query "matches scans in which
  r.jina.ai appears somewhere in the scan."
- The bytes do not support this. The 44 non-jina results contain
  zero occurrences of the string "jina" anywhere in their captured
  JSON. All 104 "jina" occurrences sit inside the 13 r.jina.ai
  results, 8 fields each.
- The true match field must sit outside captured metadata. Likely
  it is request or redirect data, which search metadata omits.
  That is an INFERENCE, not an OBSERVED fact.
- Consequence: a fleet page that calls r.jina.ai as a subrequest
  could hide among the 44. Metadata cannot exclude it. The
  noise verdict for the 44 is therefore INFERENCE, not proof.

The 13 r.jina.ai results help the noise verdict (OBSERVED):

- All 13 are the reader service's own endpoints: 10 scans of
  `https://r.jina.ai/ec` and 3 scans of `https://r.jina.ai/`.
- None is a reader-proxied third-party page. A proxied page would
  carry an inner target URL after the reader prefix. None does.
- The 44 other titles are other people's scans: temp-mail pages,
  a document-portal cluster, streaming pages, lottery pages,
  wallet pages, and news pages. None is fleet-shaped.
- Note: noise does not mean benign. Some clusters look like
  phishing scans. They are still not fleet evidence. That is
  outside this lane's scope.

### 3. "Sampling limits are stated honestly"

Verdict: STANDS, with one understatement.

Verified limits (OBSERVED):

- 30-day window: scan dates run 2026-09-26 to 2026-10-26. True.
- Metadata only: search files carry URL, title, date, IP, ASN.
  No full bodies. True.
- One page at size=100: totals 57 and 17 are both below 100, so
  no second page was needed. True.
- Anonymous API: provenance files record anonymous GETs. True.
- No HTTP failure, no timeout, no 429: the log shows 6 times
  HTTP 200. True.

Enabled:false handling: STANDS (OBSERVED):

- Config `scripts/swarm-infra-config.json` still marks
  page.title:"amap" as `enabled: false`, with the reason
  "adversarial 2026-10-14: documented acronym collisions."
- Coverage discloses the one-off run in its "Flag for the
  coordinator" section. It states the config was not changed.
  Git status for the config file is clean.
- The disclosure is honest. The run was ordered as an extra.
  The config still blocks it by default.

Understatement (INFERENCE):

- Coverage does not state one more limit. The marker-query zeros
  rest on urlscan's search index. Nothing in the repo shows that
  the index covers URL query-string tokens such as uqscan=.
  If the index does not cover them, a zero there is weak.
  This limit should be stated next to the other limits.

### 4. "The morning hits show agent-relay use"

Verdict: KILLED. No agent-relay reading survives.

The two hits (OBSERVED):

- Oct 25 hit: scan UUID 01a17355-8853-7179-8623-5d2a48a3e0b5,
  scan time 2026-10-25T13:52:41Z, page `https://r.jina.ai/ec`.
- Oct 26 hit: scan UUID 01a1787e-fe16-745d-9831-d0642306fcb2,
  scan time 2026-10-26T13:55:56Z, page `https://r.jina.ai/ec`.
- Both: confidence LOW, swarm_linked false, empty title,
  Cloudflare ASN AS13335. Both sit in the crawl's 13.

Why the relay reading fails (INFERENCE from OBSERVED bytes):

- The lane's own config note defines the signal as "scans of
  jina-proxied URLs." A proxied URL carries an inner target.
- Both hits are scans of the reader's own endpoint. Neither
  carries an inner target. Neither carries a fleet marker.
- A scan of a service front page is not a fetch through that
  service. The relay inference has no leg.

Alternative explanations that fit better:

- The reader service's own health checks.
- A third-party uptime monitor. The scans recur near-daily, and
  several fall near 13:5x UTC. That cadence fits a monitor.
- A researcher scanning the service itself.
- An ordinary user scanning the front page.
- Not our own morning scanner: that scanner only queries the
  search API. No scan-submit code was found in its module.

Grade attack: DOWNGRADED from PRIMARY (INFERENCE):

- Config grades the relay-jina-reader query PRIMARY. That grade
  rests on the "observed agent fetch" idea. It does not attach
  to a front-page scan with no inner target.
- The lane's own false-positives file says urlscan hits are
  "other people's scan metadata, not our direct observations."
  That rationale points to SECONDARY for these two records.
- LOW confidence stands. PRIMARY grade does not.

What would upgrade them:

- A scan of a jina-proxied URL whose inner target carries a
  fleet marker, such as getPoiInfo or uqscan=.
- A full result body that ties the scan's request chain to
  fleet infrastructure.
- Corroboration from another lane at the same task time.
- None of these is present.

Data quality note (OBSERVED):

- The Oct 24 13:46 UTC hit of the same shape has
  swarm_linked empty, not false. One field is missing. This is
  a data gap, not a hit.

### 5. "The morning hits are new or unreported"

Verdict: KILLED. Nothing here is new.

Evidence (OBSERVED):

- The Oct 25 hit already sits in morning state:
  `scripts/scanners/state/morning-hits/hits-20261025T145711Z.jsonl`
  and `bundle-20261025T145711Z.json`.
- The Oct 26 hit already sits in morning state:
  `hits-20261026T151547Z.jsonl` and `bundle-20261026T151547Z.json`.
  That batch is pending with a sibling worker.
- Both UUIDs also appear in the crawl's 13. The crawl adds no
  new triage-passing item. `hits-draft.json` is empty.
- Stronger: the same shape already appeared twice on Oct 24
  (10:03 UTC and 13:46 UTC), also in the crawl's 13. The pattern
  is recurrent, not new.
- The older /ec scans in the crawl (Oct 9, 13, 14, 15, 16, 17,
  18, 19) are old third-party scans of the reader front page.
  They are newly listed by this crawl, but they are still
  non-hits. Listing is not novelty.

## What survives, stated plainly

- Zero fleet markers in the 74 fetched search records.
- 74 = 57 jina-query results + 17 title-amap results.
- Title-amap results are name collisions, not fleet pages.
- Jina results are other people's scans, not fleet pages, as
  far as metadata can show.
- The stated sampling limits are true, and the enabled:false
  one-off run is disclosed honestly.
- Both morning hits stay LOW, not swarm-linked, and not novel.

## Gaps that block a confident conclusion

1. Full scan bodies need a login. Request domains and redirect
   chains are the missing check for the 44 jina-query results.
2. Urlscan's search-index coverage for query-string tokens
   (uqscan=, uqframe=) is unverified. The marker-query zeros
   are weaker than stated until this is checked.
3. The domain: match field is unexplained. The bytes show it
   is not any captured field. Docs or a logged-in pull must
   resolve it.
4. The submitter of the near-daily r.jina.ai/ec scans is
   unknown. Anonymous search metadata has no submitter field.
   The cadence is a pattern, not evidence of agent use.
5. The French AMAP collision class is missing from
   FALSE-POSITIVES-urlscan.md. Add it, or the "documented"
   claim stays overstated.
6. No token values are reproduced in this review. Raw files
   stay the verbatim store. Treat them as local-only.
