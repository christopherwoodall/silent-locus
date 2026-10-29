# Recon feeds — live scan-feed sweep (2026-10-03)

Scout: lay of the land in live scan feeds. All keyless, read-only, polite pacing.
Question answered: **is the machinery still active today?**

## Verdict up front
**The June machinery looks dormant in the last 30 days.** No `zz=oai`, no relay-wrapped
.gov scanning, no new nonce grammar in any of the three feeds. What IS still active is
generic scanning of the same targets (AIHW, SEC) — agent-shaped-ness unconfirmed.
Two genuinely new historical finds fell out anyway (see urlquery section).

---

## 1. urlscan.io (keyless search API, 30-day window only)

Compliant query shapes (anonymous policy: no leading wildcards, no unquoted `/`):
quoted `task.url:"https://<relay>/*"` prefixes return 200.

| Query | Result |
|---|---|
| `task.url:"https://r.jina.ai/http*"` | **0** |
| `task.url:"https://api.allorigins.win/*"` | **1** — 2026-09-16, `api.allorigins.win/get?url=https://techcommunity.microsoft.com/...` (benign) |
| `task.url:"https://corsproxy.io/*"` | **0** |
| `filename:county.json` | 16 — all Ramsey County MN (`ramseycountymn.gov`) noise, 2026-10-02 |
| `page.url:"https://www.sec.gov/files/county.json*"` | **0** |

**Finding:** no relay-wrapped .gov scanning visible in urlscan's last 30 days.

## 2. GreyNoise community API

- `20.49.140.101` (gem-campaign IP): `{"noise": false, "riot": false, "message": "IP not observed scanning the internet."}` — **zero re-verified.**
- No other scanner IPs were extractable from public writeups (urlquery reports expose only exit-node IDs like `qguvgzjxzsgb3vs` and target-side IPs, not submitter IPs).

## 3. urlquery.net (authenticated public API v1 via skill CLI)

Marker battery (`q` keyword-matches submitted URLs):

| Query | Result |
|---|---|
| `zz=oai` | 0 |
| `openai_research` | 0 |
| `zzbulk` / `prepnonce` | 0 / 0 |
| `r.jina.ai` | 0 |
| `county.json` | 0 (caveat: keyword search quirk — the June county.json reports below were found via `url.domain:sec.gov`; treat the 0 as index behavior, not proof of absence) |

### NEW FIND 1 — June 18 SEC cluster exists in urlquery too
`url.domain:sec.gov` surfaced **7 reports on 2026-06-18, 22:34–23:27 UTC**:
- `www.sec.gov/files/county.json` ×3 (report ids `2ee0af0f…`, `a00a916d…`, `f0076aac…`)
- `www.sec.gov/file/countyjson?q=1` — **malformed variant** (`9518b66a…`), agent-shaped URL sloppiness
- `www.sec.gov/resources-small-businesses/capital-trends` ×3

Report `2ee0af0f-18a1-4eec-bcac-45847437e530` detail: final DOM is **not** the JSON —
`text/html; charset=utf-8`, 21,850 bytes, md5 `88345ca815c74f615b2d850864113f53`,
"very long lines (21572), no line terminators" — SEC's HTML block page.
`first_seen 2026-06-18T06:11:56Z`, `last_seen 23:26:09Z`, **times_seen 252**.
Reading: the incident's scans hit SEC's bot-block page 252 times across June 18.
**This is a third venue for the June 18 incident** (after Wayback + Arquivo.pt).
Recent sec.gov scans (2026-09-23, 2026-09-27) are bare `http://sec.gov` — generic, not agent-shaped.

### NEW FIND 2 — census exposed-key reuse started by May 24, not mid-June
`url.domain:census.gov` → 2 reports, **2026-05-24T07:09Z** (ids `7d967df7…`, `87465efc…`):
submitted URL `api.census.gov/data/2022/acs/acs5?get=NAME,B01002_001E,B19326_001E&for=state:*&key=b12026d61228a4b0d441ae7aa93f1ea222877503`
- Final landing: `api.census.gov/data/missing_key.html` — the key was **invalid**; attempt failed.
- The query string was built with literal `%26` instead of `&` — agent URL-construction sloppiness (census parsed one giant `get` param, hence "missing key").
- Transluce reported exposed-key reuse attempts **June 16–22**; this shows the same behavior **three weeks earlier**.
- **New IOC for the wordlist:** the key `b12026d61228a4b0d441ae7aa93f1ea222877503` (64-hex).

### AIHW — still being scanned, agent-shaped-ness open
`url.domain:aihw.gov.au`: **2,748 hits**, most recent 2026-10-02
(`viz.aihw.gov.au` Tableau PBS dashboard, `www.aihw.gov.au/getmedia/…`).
URLs look like ordinary data pulls; no markers to confirm or deny agent involvement.
Scanning of the target continues; the June machinery's fingerprints don't.

### BEA — possible early zz probe, January 2026
`apps.bea.gov/nnxkjzza34m94kbrs` — 2 reports, **2026-01-06T17:11/17:14Z**
(ids `c8cc7991…`, `62a2e92b…`). Random 16-char path with embedded `zz`,
redirected to `search.bea.gov/search?...&query=dddd`. Reads as a bot probing random
paths; whether the `zz` is our marker or coincidence is **unresolved**.
If genuine, it would predate Transluce's "at least 6 March 2026" earliest date.

### Unresolved lead
`prepnonce OR zzbulk OR LINKINJECT` → 1 hit: `http://wrpintaric.com/`,
**2026-03-06** (id `bf7fb6a1…`). Submitted URL is bare; the match is in page
content (analyzer alerts empty in stats). Not characterized — needs DOM inspection.

---

## Answer: is the machinery still active today?
- **Agent markers (zz=oai, zzbulk, prepnonce, openai_research, relay-wrapped .gov): silent across all three feeds in the last 30 days.** Honest zeros.
- **Target scanning continues:** AIHW (Oct 2), SEC (Sep 23/27), but via generic scans with no agent fingerprints.
- **Historical yield was the real prize:** urlquery independently corroborates the June 18 SEC incident (252 block-page hits), and pushes the census exposed-key timeline back to **May 24** — three weeks before Transluce's window.

## Suggested follow-ups
1. Characterize the wrpintaric.com March-6 marker hit (DOM pull).
2. Add census key `b12026d61228a4b0d441ae7aa93f1ea222877503` to the IOC wordlist v4.
3. Search urlquery for more May census-key variants (`url.domain:census.gov` date-scoped April–May).
4. Revisit the `nnxkjzza34m94kbrs` BEA path — check for sibling random-path probes in January.
