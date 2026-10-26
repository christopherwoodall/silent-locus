# Third-party reports that bear on the urlscan crawl findings — final, 2026-10-26

Final-review note: the first draft accepted Transluce entry 178. The
final adversarial review killed that accept (see the rejected list).
Accepted count is now 2, not 3. The draft file
`third-party-reports-draft.md` is kept unchanged as the lane output.

## Scope in plain words

This note covers only the findings in scope for this crawl.

- Finding set A: two morning-scan urlscan hits on `https://r.jina.ai/ec`
  (2026-10-25 and 2026-10-26, LOW, SECONDARY, swarm-linked false,
  Cloudflare IPs). Jina Reader is a public text-extraction proxy.
  It fetches a page on its own server and returns clean text.
  A relay is a third-party service that fetches a target for the requester.
- Finding set B: the fleet markers this crawl hunted and found zero of
  on urlscan in the last 30 days: `getPoiInfo`, `uqscan=`, `uqframe=`,
  `hysandbox`, Amap fleet pages. Amap is a Chinese map service.
  `getPoiInfo` is an Amap place-data request. `uqscan=` and `uqframe=`
  are tag values seen in scanner URLs. `hysandbox` is a Tencent sandbox
  proxy name seen in fleet traffic.
- Finding set C: urlscan.io itself as a source for agent-infrastructure
  observation. urlscan.io is a public website scanner. It browses a
  submitted URL and records what the page contacts.

## Grades used here

- UPSTREAM: the report itself is the primary document.
- SECONDARY: a tracker entry or summary that reads other records.
  The entry is not the underlying evidence.

## Search coverage

- Transluce tracker, live, first page: finding IDs 208 down to 181.
  The tracker tool returns only the first page of 25 by default.
  Its command line has no page flags, so full pagination was not possible
  through it. IDs 175 and 177 return "Finding not found" live.
  IDs 176, 178, 179, 180 were fetched one by one.
- Transluce tracker, local snapshot: `data/lanes/2026-10-09-transluce-intel/events.jsonl`,
  109 entries, finding IDs up to 174. Full text was searched for
  jina, urlscan, amap, getPoiInfo, uqscan, uqframe, hysandbox.
- Repo docs: `docs/jina-activity-methodology.md` and
  `reports/chinese-agent-fleet-findings-2026-10-14.md`. Both cite the
  Swarmchasers report below. Both are own-shop documents, not
  third-party reports, so neither is accepted on its own.
- Public web: brief searches for Jina Reader relay use, the Amap agent
  fleet, and urlscan as an observation source. No logins. No accounts.

## Accepted reports

### 1. Swarmchasers — "We found a Tencent agent fleet" (full report)

- Link: https://swarmcha.se/posts/chinese-agent-fleet-full-report
- Date: preliminary report 2026-10-04, per the report itself.
  The full-report date is not stated in the fetched text.
  Activity covered: 2026-09-28 to 2026-10-08.
- Grade: UPSTREAM. This is the report itself, by an outside team.
- What it corroborates:
  - The fleet used the exact markers this crawl hunted: `getPoiInfo`
    in Amap place-data requests, `uqscan=` tag values, and at least
    one `uqframe=` tag value in a fleet program.
  - The fleet used the `hysandbox` proxy. The report names the
    `hysandbox-ats` proxy on Tencent Cloud traffic.
  - Jina Reader was the fleet's only successful relay. Five runs got
    answers through Jina on 2026-10-04 to 2026-10-06. Jina served
    cached copies up to 30 days old.
  - The fleet was seen on urlquery, a public scanner, not on urlscan.
    This fits the crawl result: markers present in one scanner corpus
    and absent in the urlscan 30-day window are not a contradiction.
- What it does NOT corroborate:
  - It does not mention the `r.jina.ai/ec` scans. It does not mention
    urlscan at all in the checked text.
  - It does not show the fleet is still active. Last activity seen
    was 2026-10-08, before this crawl.
  - It does not show the morning-scan `/ec` hits are fleet-linked.
    Those hits carry no fleet marker and no inner target URL.

### 2. Transluce tracker entry 153 — Amap activity on urlquery

- Link: tracker entry, submitter Linus, created 2026-10-04.
  Evidence links are urlquery reports, for example
  https://urlquery.net/search?q=amap.com&view=list&type=reports
- Date: 2026-10-04.
- Grade: SECONDARY. The entry summarizes urlquery reports. It is
  not the urlquery evidence itself. It also cites the Swarmchasers
  report above.
- What it corroborates:
  - The `uqscan` tag value appears in Amap scanner traffic. The entry
    says "claude" appears in a `uqscan` parameter in about 9% of
    relevant reports, and warns the value is freely chosen, so it is
    not conclusive proof of model identity.
  - Amap extraction attempts and anti-bot bypass attempts were visible
    in a public scanner corpus in early October 2026.
- What it does NOT corroborate:
  - It does not cover urlscan. It does not cover Jina.
  - It does not show the markers exist on urlscan now. The crawl
    found zero of them there.
  - It does not attribute the activity firmly. The entry itself calls
    its read uncertain, and notes Swarmchasers argues for Tencent
    Hy-style code, not Claude.

## Explicit limits

- No third-party report found bears on the two `r.jina.ai/ec`
  morning scans themselves. No report mentions `/ec`, and no report
  ties those scans to any fleet or agent.
- No third-party report found uses urlscan.io as a source for
  agent-infrastructure observation. Report 115 below uses urlscan
  records, but for a different subject.
- No third-party report found changes the crawl verdict: zero
  triage-passing hits, and the 74 fetched results are routine noise.

## Rejected candidates

Each rejected item has one line that says why.

- Transluce entry 178 (BGSU library retrieval through Jina, May 2026):
  REJECTED on final adversarial review. It fails the same bar that
  rejected entries 38 and 115: no fleet link, no fleet marker, no
  `/ec`, no urlscan, authorship unproven. It adds nothing beyond the
  accepted Swarmchasers report, which already covers Jina-as-relay
  for the actual fleet.
- Transluce entry 115 (urlscan records, Cloudflare Playground, AIHW
  dashboard metadata): urlscan as a source, but the subject is not
  agent infrastructure and no fleet marker appears.
- Transluce entry 38 (TinyURL/Jina chain to NYSED enrollment data):
  Jina is only mentioned in a chain, and execution, bypass, and AI
  authorship are all unconfirmed.
- Transluce entries 170, 171, 173 (terminal-bench Jina uses; Amap
  dead-drop family; hysandbox follow-up): own-shop filings by the
  operator, not third-party reports, so they fail the third-party bar.
- Transluce entry 182 (urlquery scans of China Customs data):
  urlquery, not urlscan, and no fleet marker.
- Transluce entry 180 (urlquery noVNC scanner-browser control):
  urlquery, not urlscan, and no fleet marker.
- Transluce entry 188 (RentAHuman billboard payment): a different
  relay shape, no Jina, no Amap, no urlscan.
- Transluce entry 176 (OpenAI agents on Wikimedia): agent activity,
  but no Jina, no Amap, no urlscan, no fleet marker.
- Transluce first-page entries 181–208 otherwise: no match for jina,
  urlscan, amap, getPoiInfo, uqscan, uqframe, or hysandbox in the
  checked text, apart from the generic "relay" words already covered.
- NorForge, "Inside Cairn" (2026-10-19, https://norforge.com/blog/inside_cairn):
  background only — exposed Cairn agent panels, no Jina, no Amap,
  no urlscan, no fleet marker.
- Secondary press on the Swarmchasers report (TechRadar, Cryptopolitan,
  daily.dev, CyberPress, and similar): re-reports of accepted report 1,
  no independent evidence, so not counted as separate corroboration.
- urlscan how-to and OSINT guides (Medium, Elastic docs, and similar):
  they describe urlscan as a tool, not agent-infrastructure observation.
- Repo-internal fleet writeups (`reports/chinese-agent-fleet-findings-2026-10-14.md`,
  `docs/jina-activity-methodology.md`): own-shop documents, not
  third-party reports; their third-party citation is accepted report 1.
