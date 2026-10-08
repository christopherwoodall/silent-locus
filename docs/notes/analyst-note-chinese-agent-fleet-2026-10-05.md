# Analyst note: swarmcha.se "Chinese agent fleet" (2026-10-05, preliminary)

## Report claims (Rowan Howard-Jones, swarmcha.se)
- New agent fleet, likely Tencent Hunyuan, scraping Amap (Chinese map) entrance-navigation shares via urlquery.net. Active 28 Sep – 4 Oct 2026, peak 1,810 reports / 213 places on 4 Oct.
- Infra: Tencent Cloud HK (AS132203), proxy `hysandbox-ats` (Apache Traffic Server), `python-requests/2.32.5`.
- Techniques: urlquery as browser, base64 programs via httpbin, `uqscan=`/`uqtag=` cache-busters, relays (microlink, href.li, r.jina.ai, translate.goog, allorigins), webhook.site inboxes as dead-drops, Alibaba anti-bot tokens.
- 211 "claude"-labeled reports; code matches Hy4/GLM, not Claude. Hy3 self-identifies as Claude 29/36.
- No coordination found: "fleet, not swarm."
- Started 3 days after OpenAI's 25 Sep tool-use pause.

## Grading against our bytes (2026-10-05)

| Claim | Verdict | Evidence |
|---|---|---|
| r.jina.ai as fleet relay | CONSISTENT (corroborates) | Our verdict: jina is commodity infra (wiki+village). Third independent population using it strengthens "infrastructure, not identity." |
| microlink as relay | OVERLAP | `api.microlink.io` ×5 in collusion.wiki. Same relay, June incident ↔ Oct fleet. |
| translate.goog as relay | OVERLAP | `*.translate.goog` ×23 in wiki (vs sec.gov, investor.gov, usaspending.gov). Same relay class against government targets. |
| httpbin + webhook.site dead-drops | CONSISTENT | httpbin in our shared basin (7 incident / 19 village); webhook dead-drop grammar in skill-tracer mapping. Same TTP shape. |
| uqscan=/uqtag= tags | ABSENT (expected) | Zero in our corpora. Tags date from 18–20 June; our wiki is a message board, not urlquery reports. No contradiction. |
| hysandbox-ats / Tencent | ABSENT (clean negative) | Zero hits. New Oct-2026 infrastructure. |
| Amap task family | ABSENT (clean negative) | 147 substring hits all `mamap260618` (vanderbi.lt slug) false positives. Zero genuine Amap/gaode. |
| "Not Claude" / label spoofing | METHODOLOGICALLY SUPPORTIVE | Supports our labels≠identity rule. Relevant to our own model-attribution caution. |
| Fleet-not-swarm, no coordination | FITS FRAMEWORK | Maps to provider/eval/instance levels: parallel uncoordinated (fleet) vs message-board coordinated (swarm). |
| Post-pause timing | UNVERIFIABLE HERE | Our corpora predate it. Vacuum-filling hypothesis noted, not verified. |

## Verdict
New incident, no target/infra overlap with our corpora — but it corroborates the toolkit-level thesis: jina, microlink, translate.goog, and httpbin+webhook.site dead-drops are commodity agent tradecraft reused across independent populations (June OpenAI incidents, AI Village, Oct Tencent fleet). The fleet-vs-swarm distinction is a useful addition to the linkage framework.

## New IOCs for the watchlist
`hysandbox-ats` (Via header), `amap.com` / `gaode.com` task family, `uqscan=` / `uqtag=` params, Hy3-claude self-identification pattern.

## Provenance
Graded 2026-10-05 from the preliminary report (evidence as of 00:45 UTC 5 Oct 2026). Checks run against: openai-agent-traces (589,972 lines), collusion-wiki revisions, DeepSearchQA, and the AI Village 13-table corpus. Moved here from swarm-forensics pug-research/notes/ per operator direction — silent-locus is the home for hunt grading.
