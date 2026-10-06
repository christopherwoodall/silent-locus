# PIPEDREAM-HUNTER findings: `eo3wuo9z334anlh.m.pipedream.net` live lead

- **Worker:** PIPEDREAM-HUNTER
- **Date collected:** 2026-10-05 (CDT), scans pulled ~12:40 CDT
- **Methods:** all passive, stored observations only. (1) urlscan.io public search API (`/api/v1/search/?q=domain%3A<host>&size=100`), 2s pacing between the 5 pulls; search-result JSON only — no scan result pages, no screenshot fetches, no requests to the Pipedream endpoint itself. (2) keyless urlquery htmx endpoint (`bin/uq_htmx.py search --query "eo3wuo9z334anlh" --limit 20`). (3) `grep -r` over `~/workspace/silent-locus/` and `~/workspace/muse-home/projects/urlquery-api-hunt/artifacts/dataset/`. (4) urlhaus API check for the URL (returned `{"error": "Unauthorized"}` — API key required; not pursued).
- **Scope:** agents and agent infrastructure only; no human/operator attribution. Full observed values, no redaction.
- **Raw data:** `urlscan-eo3wuo9z334anlh.json`, `urlscan-eo6p96x7ax0vcaj.json`, `urlscan-eoubuki2x8vmkry.json`, `urlscan-eoqdkld34574c7.json`, `urlscan-eobb5owjuxe1ejb.json` (same directory).

## 1. OBSERVED — target: `eo3wuo9z334anlh.m.pipedream.net`

urlscan search `domain:eo3wuo9z334anlh.m.pipedream.net`: **total=9, has_more=False**, all 2026-10-05. (The 10th hit from the earlier domain-wide `pipedream.net` pull was `assets.pipedream.net`, excluded by the exact-domain query.)

### Per-scan table (all times UTC; CDT = UTC−5)

| # | scan UUID | task time (UTC) | scanned URL | page title | task.source | task.method | task.visibility |
|---|-----------|-----------------|-------------|------------|-------------|-------------|-----------------|
| 1 | 01a10bcd-d71e-766e-ab34-34f399d1b8f1 | 2026-10-05T11:23:31.779Z | https://eo3wuo9z334anlh.m.pipedream.net/ssh_ | null | (none) | api | public |
| 2 | 01a10bbb-00ce-7004-a24b-9b1c910db0de | 2026-10-05T11:02:53.769Z | https://eo3wuo9z334anlh.m.pipedream.net/ssh_ | null | (none) | api | public |
| 3 | 01a10bb8-94d3-718d-9a01-4b68702a856c | 2026-10-05T11:00:16.604Z | https://eo3wuo9z334anlh.m.pipedream.net/ssh_ | null | urlhaus | automatic | public |
| 4 | 01a10bb8-9158-745b-8e71-147e6dba1482 | 2026-10-05T11:00:13.704Z | https://eo3wuo9z334anlh.m.pipedream.net/ | null | urlhaus | automatic | public |
| 5 | 01a10bb3-af2d-7250-8f79-76608dc12c88 | 2026-10-05T10:54:53.652Z | https://eo3wuo9z334anlh.m.pipedream.net/ssh_ | null | (none) | api | public |
| 6 | 01a10bb1-51c2-7747-b29d-131787e562c9 | 2026-10-05T10:52:19.276Z | https://eo3wuo9z334anlh.m.pipedream.net/ssh_ | null | (none) | api | public |
| 7 | 01a10b87-a04d-73b1-a7a7-df1c28acaf37 | 2026-10-05T10:06:46.412Z | https://eo3wuo9z334anlh.m.pipedream.net/ssh_ | null | (none) | api | public |
| 8 | 01a10b85-c573-7430-b2e8-e05661e9a209 | 2026-10-05T10:04:44.494Z | https://eo3wuo9z334anlh.m.pipedream.net/ssh_ | null | (none) | api | public |
| 9 | 01a10b84-ea13-778a-9ab9-e7dc230886c3 | 2026-10-05T10:03:48.344Z | https://eo3wuo9z334anlh.m.pipedream.net/ssh_ | null | (none) | api | public |

Clusters in CDT: 05:03:48 / 05:04:44 / 05:06:46 (3 API scans in ~3 min); 05:52:19 / 05:54:53 (2 API scans, ~2.5 min apart); 06:00:13 (urlhaus auto, `/`) / 06:00:16 (urlhaus auto, `/ssh_`) / 06:02:53 (API) / 06:23:31 (API, ~20 min gap).

### Endpoint metadata (from search-result page objects — same values on all 9)

- `page.ip`: 54.89.179.70, `page.ptr`: ec2-54-89-179-70.compute-1.amazonaws.com, `page.asn`: AS14618, `page.asnname`: "AMAZON-AES - Amazon.com, Inc., US", `page.country`: US — the Pipedream workflow server (AWS US-East), not a submitter.
- `page.status`: **400** — the endpoint responded HTTP 400 to the urlscan fetch (workflow is live but rejected the request; expected shape/verb/payload not met).
- `page.mimeType`: text/html, `page.title`: null (no title extracted from the 400 response).
- `page.domainAgeDays`: 0 (ephemeral workflow subdomain), `page.apexDomainAgeDays`: 2805, `page.tlsIssuer`: "Amazon RSA 2048 M04", `page.tlsValidDays`: 394, `page.tlsAgeDays`: 284, `page.language`: en.
- Task objects carry **no submitter country / user-agent** at search-API depth (those fields live in the full result JSON, not pulled).

### Submission-method facts (new vs prior report)

- **7 of 9 scans were submitted via the urlscan API** (`task.method: api`, `task.source` empty). **2 were urlhaus automatic** (`task.method: automatic`, `task.source: urlhaus`) — the pair at 06:00:13/06:00:16 UTC covering `/` and `/ssh_` 3 seconds apart, consistent with urlhaus auto-submitting both URL forms after a report landed there around 06:00 CDT.
- The urlscan API does not accept arbitrary browser submissions; `method: api` means a scripted client pushed the URL.

## 2. OBSERVED — urlquery (keyless htmx endpoint)

`bin/uq_htmx.py search --query "eo3wuo9z334anlh" --limit 20` → `{"reports": [], "query": "eo3wuo9z334anlh"}`. **Zero urlquery submissions** for this hostname.

## 3. OBSERVED — local corpus greps

- `eo3wuo9z334anlh` in `~/workspace/silent-locus/`: hits only in our own prior artifacts — `why-these-sites/workers/index-hunter/urlscan/urlscan-pipedream_net.json`, `.../index-hunter/FINDINGS.md`, `why-these-sites/WHY-SITES.md`. **No occurrence anywhere else in the corpus.**
- `eo3wuo9z334anlh` in `~/workspace/muse-home/projects/urlquery-api-hunt/artifacts/dataset/`: **zero hits.**
- Siblings (`eo6p96x7ax0vcaj`, `eoubuki2x8vmkry`, `eoqdkld34574c7`, `eobb5owjuxe1ejb`) in silent-locus: **only** in the metronome persona caches `personas/metronome/raw/htmx_pipedream.json` and `personas/metronome/raw/poller_safe_pipedream.json` — single historical urlquery submissions each:
  - `eo6p96x7ax0vcaj.m.pipedream.net/Oneotsuka` — 2026-09-03T23:52:00Z (report_id 6994a063-918f-4b9a-84e7-3ef27cce6e29)
  - `eoubuki2x8vmkry.m.pipedream.net` — 2026-08-10T12:43:00Z (report_id 6e1e6d11-96f3-40eb-8b48-118db7cfd860)
  - `eoqdkld34574c7.m.pipedream.net` — 2026-07-10T12:34:00Z (report_id 44bff15a-4275-4f72-a225-ea973702684a)
  - `eobb5owjuxe1ejb.m.pipedream.net` — 2026-05-04T13:31:00Z (report_id 8cccb473-e19f-41ae-b379-cb9142bcc5f5)
  - Plus 3× `assets.pipedream.net` (2026-03-18, 2026-04-21, 2026-04-23) and older `x.pipedream.net` / `m.pipedream.net` endpoints back to 2024-10-26 in the same files (33 `m.pipedream.net` references total).

## 4. OBSERVED — sibling urlscan pulls

All four sibling endpoints: **urlscan total=0, has_more=False, zero results.**
- `eo6p96x7ax0vcaj.m.pipedream.net` — 0
- `eoubuki2x8vmkry.m.pipedream.net` — 0
- `eoqdkld34574c7.m.pipedream.net` — 0
- `eobb5owjuxe1ejb.m.pipedream.net` — 0

The `/ssh_`-path repeated-scan pattern **does not recur** among siblings. Each sibling exists only as a single historical urlquery submission, months apart, with no urlscan presence at all.

---

## INFERENCE (separated from observations)

### Beacon-pattern assessment

1. **The repetition is observer-side, not operator-side.** What repeats is *submission of the endpoint URL to urlscan*, not traffic *to* the endpoint. A beacon/check-in would be HTTP traffic to `m.pipedream.net/ssh_` itself; we have no visibility into that (and must not probe it). Repeated urlscan API submissions are watcher behavior: an automated threat-intel pipeline, a researcher's rescan loop, or the endpoint owner's own monitoring loop pushing the URL through a scanner. It is evidence that *someone is watching the endpoint*, not that something is beaconing to it.
2. **The 7 API-method submissions over ~80 min are scripted, not manual.** A human analyst submits a URL to urlscan once. Three bursts (3 scans in 3 min; 2 scans 2.5 min apart; 2 scans 20 min apart) with no human-readable submitter are consistent with an automated rescan loop — e.g., a pipeline that re-submits on each observed event, or a monitoring cron with irregular firing. This is the strongest behavioral signal in the set.
3. **The urlhaus pair is a separate watcher.** Two `method: automatic` scans from `source: urlhaus` 3 seconds apart covering `/` and `/ssh_` mean the URL was reported to abuse.ch urlhaus around 06:00 CDT and their pipeline auto-scanned both forms. So at least two independent parties (the API submitter, the urlhaus reporter) had this endpoint in their sights on 2026-10-05.
4. **HTTP 400 on `/ssh_`** means the workflow trigger is live but the urlscan GET was rejected — the workflow expects something else (POST body, auth header, different path shape). Consistent with a dead-drop that validates its input rather than an open redirector/phish page.
5. **`/ssh_` is an odd path for a Pipedream HTTP trigger.** Sibling endpoints in the corpus sit at `/` or carry payload-ish paths (`/Oneotsuka`); an SSH-flavored fixed path on a webhook inbox reads like a label for SSH-key/credential drops or an operator tag. This is suggestive, not determinative.
6. **No recurrence, no history.** Zero urlquery presence, zero corpus presence, zero sibling urlscan presence, and the siblings themselves are single-submission artifacts months apart. The `eo3wuo9z334anlh` endpoint is a *new, live, single-day* phenomenon — no historical trail to tie it to the corpus's older Pipedream endpoints.

### What's still unknown

- Who submits via the urlscan API (submitter IP/country/user-agent — available only in the full per-scan result JSON, not pulled per task scope).
- Who reported the URL to urlhaus (urlhaus API needs an auth key; not pursued).
- Whether the workflow owner and the API submitter are the same party.
- What the endpoint actually receives (cannot be observed passively; probing it is out of scope).
- Whether the rescan pattern persists beyond 2026-10-05.

### Verdict

**DEAD-DROP LEAD, ELEVATED — watchlist-grade, not evidence-grade.** The new urlscan metadata strengthens the lead beyond the prior report: scripted API resubmission of the `/ssh_` URL in three bursts over 80 minutes plus an independent urlhaus report the same morning is watcher-on-a-live-inbox behavior, and the endpoint's 400-rejecting posture fits a validating dead drop. But the critical caveat stands and sharpens: *everything we see is observer-side*. We have zero bytes showing what — if anything — beacons into the endpoint, and the strongest alternative (threat-intel/defender automation re-scanning a reported suspicious URL) is fully consistent with the data. The siblings do not show the pattern, so this is a single-endpoint, single-day event, not a recurring fleet behavior. This is not agent-shaped evidence; it is an agent-adjacent dead-drop surface under active watching by unknown parties.

### Suggested follow-ups (for the parent, not executed)

- Re-pull `domain:eo3wuo9z334anlh.m.pipedream.net` daily for 7 days (passive search API) to see whether the API resubmission pattern persists or was a one-day burst; log any new scan UUIDs/timestamps.
- Consider pulling one full per-scan result JSON (`/api/v1/result/<uuid>/`) to recover submitter country/user-agent from the task object — task-scoped metadata, no endpoint contact.
- Track the four sibling hostnames for any future urlscan/urlquery appearance; they are currently dormant single-submission artifacts.
