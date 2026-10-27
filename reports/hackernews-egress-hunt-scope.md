# Hacker News hunt lane scope brief

## Idea

Open a Hacker News (HN) hunt lane. Search HN stories and comments for
reports of agent egress and escalation behavior. Process hits with a
swarm, enrich them, then run follow-on investigation on the extracted
indicators.

## Terms

- HN: Hacker News, a public tech discussion board. Stories and comments
  are public. No login is needed to read them.
- Algolia: HN's public search API (hn.algolia.com). It searches stories
  and comments by text, tag, and date. No key is needed.
- Indicator: a host, URL, term, or pattern pulled from a hit, used to
  pivot to other surfaces.
- SECONDARY: evidence from a third party, not first-hand capture.

## Why HN fits

HN already holds one confirmed sighting in this hunt: item 49379079,
"Qwen3.8 Fetches Weird URLs", where a model fetched unasked routify
URLs 16 times. That thread is overlap, not a new hit. It proves HN
carries this behavior class in first-person reports, not just links.

HN threads also carry detail other surfaces lack: tool names, harness
names, command lines, error text, and follow-up comments that correct
or extend the first report. Those details feed enrichment and pivots.

## Scope

- Behavior shapes: the same 6 shapes as the broad agent-egress hunt
  (metadata reach, object-storage upload, named probe hosts,
  user-namespace escape, download-then-execute, recon-then-egress).
- Search terms: routify, aliyuncs, oss-cn, sanmaohe, proxy_temp_file,
  169.254.169.254, 100.100.100.200, unshare, metadata endpoint,
  plus agent-egress phrasing (model fetched, hallucinated URL,
  signed URL nobody asked for).
- Date range: November 2025 onward, matching the standing hunt focus.
  Older threads are overlap context only.
- Method: Algolia API search per term, paged fully, with raw captures
  and provenance triples. No scraping of HTML where the API gives the
  same data. No login, no account, no voting, no commenting.

## Swarm processing

- Triage lane: rank hits, drop link-only and vendor-announcement noise.
- Linguist lane: read what each thread actually claims, in full.
- Cryptologist lane: pull indicators (hosts, URLs, paths, command
  shapes, model and harness names as stated in the thread).
- Adversarial lane: try to kill each ranked claim; string-only
  matches downgraded; hearsay flagged.
- Enrichment lane: merge indicators, dedup against Factum and lists/,
  grade every row.
- Follow-on lane: pivot each kept indicator to urlquery, GitHub
  issues and code search, urlscan, and crt.sh, and report what the
  pivot adds or kills.

## Deliverables

- Raw captures: data/lanes/hackernews-egress-hunt/raw/ (Algolia
  responses, provenance triples, SHA256SUMS).
- Report: reports/hackernews-egress-hunt/REPORT.md (ranked hits,
  appendix, triaged-out, coverage table with exact counts,
  novelty verdicts, open items) + hits.json + MANIFEST.md.
- Enrichment: entities and indicator list in the same report dir.
- Follow-on: pivot results per indicator, with kills recorded.
- Staged only. A sibling phase-2 ingest owns all Factum writes.
  No push from the fleet; the parent pushes and verifies.

## Rules that travel with this lane

- Agents and agent infrastructure only. No human or operator identity.
  Thread posters are not investigated. Names stay out of reports
  unless the thread itself is about a named tool or model.
- Grades SECONDARY by default. Pattern matches are pattern matches.
- Novelty checks before any NEW claim: Factum exact and fuzzy,
  legacy evidence trees, Transluce tracker snapshot, lists/.
  Item 49379079 is known overlap.
- Signed-URL rule: parameter names and path shape only in reports.
  Never query strings, signatures, or tokens into Factum.
  Raw files are never redacted.
- No Transluce submissions (freeze in force). No paid upgrades.
- This lane is TIER-B. It needs the operator's word to dispatch.
