# urlquery alternatives — farmable surface assessment (2026-10-05)

Sources: user's screenshot + https://zeltser.com/lookup-malicious-websites + https://postmodernsecurity.com/2015/09/11/malware-analysis-and-incident-response-tools-for-the-frugal-and-lazy/
Priority: AGENT traces, not just malware. Marker set: `uqscan=`, `uqcors.html`, `lhr.life`, is.gd slugs (`3JlIp7`, `mf075827`, `sum074114`, `kf073634`, `AGE115EXTRACT1`), `pandalegacy`, `sub_poi_navi`.

## Proven: no-auth API access works

### OTX (AlienVault Open Threat Exchange) — FARMABLE NOW
- No-auth API confirmed: `GET https://otx.alienvault.com/api/v1/indicators/domain/<d>/url_list?limit=50&page=N` returns URL lists with first-seen dates, HTTP codes, SafeBrowsing matches. Also `general`, `passive_dns`, `malware`, `http_scans` sections.
- `lhr.life`: 132 unique tunnel subdomains across pages 1–4. **4 OVERLAP with our operator's 79 fleet subdomains**: `5ede92286ebdfd.lhr.life` (2026-07-31), `820eea12fec476.lhr.life` (2026-09-09), `98a8e091083f27.lhr.life` (2026-07-31), `c2679a7c8e852b.lhr.life` (2026-06-25). Cross-surface confirmation — OTX independently observed operator tunnels.
- The 4 overlapping subdomains have 0 pulses (URL-list only, not threat-flagged).
- `is.gd`: 4,309 URLs in OTX. Scanned 4,000 — **zero hits** on our 5 operator slugs. OTX's slice is Oct-2026-recent; operator slugs are June 2026. Clean negative, not a coverage gap claim.
- Pulse search endpoint needs auth; general/url_list/passive_dns do not.
- Shows: submission/first-seen dates ✓, page content ✗, submitter info ✗.

### Pulsedive — FARMABLE NOW
- No-auth community API: `GET https://pulsedive.com/api/info.php?indicator=<ioc>` and `/api/explore.php?q=...`.
- `lhr.life`: in DB, risk=medium, stamp_seen 2026-06-14, retired 2026-09-16. `is.gd`: medium, seen 2026-09-29.
- `indicator=uqscan` explore: 0 results.
- Shows: risk factors, first/last seen, retired status ✓. No page content, no submitter info.

### urlscan.io — FARMABLE NOW (already in use)
- No-auth search API works. `uqscan=` → 0. `uqcors.html` → 0. `pandalegacy` → 0.
- The parent's `lhr.life` find (90 results, SSTI/RCE pages, zero shared subdomains with our urlquery set) stands as the proof that alternatives see different slices.

## Blocked: needs browser or API key

| Surface | Blocker | What it would show |
|---|---|---|
| VirusTotal | API key required (none on VM); web UI JS-walled | URL first-seen, submission dates, detecting vendors, relations |
| ANY.RUN | JS-walled; public tasks need browser | Interactive sandbox: process tree, network, screenshots |
| Hybrid Analysis | JS-walled; needs browser or API key | Public analyses: dropped files, network IOCs |
| Joe Sandbox (url-analyzer.net) | Not yet probed; likely JS-walled | URL analysis reports |
| FileScan.io | `/api/v1/search` → 404; community API path unclear | Real-time URL examination |
| AbuseIPDB | JS-walled web; API needs key | Reporter history for 106.11.226.79 / 47.246.165.44 |
| CheckPhish (Bolster) | JS-walled | Phishing verdicts |
| urlscore.ai | JS-walled / empty | URL risk scores |
| ThreatMiner | API returned empty; web JS-walled | Passive DNS, WHOIS, AV detections |
| Zscaler Zulu | Loads; form submission needs browser | URL risk analysis with page render |

## False alarm noted
- Sucuri SiteCheck: "malware" keyword hits on `5ede92286ebdfd.lhr.life` were meta-description SEO text, not a verdict. Tunnel is dead anyway.

## Next actions
1. Browser lane: ANY.RUN public-task search for `lhr.life` + `uqscan`; Hybrid Analysis search; Zscaler Zulu submission of a live operator URL. (STILL OPEN — no live browser in this lane)
2. API keys: VirusTotal free key (user supplies) → URL search for `uqcors.html`, is.gd slugs; AbuseIPDB key → operator IP reporter history. (STILL BLOCKED)
3. OTX deep lane: pull full `lhr.life` url_list (all pages), extract dates/IPs; check `passive_dns` for the 4 overlap subdomains; repeat for any new operator domains. — PARTIAL 2026-10-05: pages 1–5 pulled (Oct 2 → Jun 22) via fetch fallback; 4th overlap `c2679a7c8e852b` confirmed + cross-matched to our corpus; `passive_dns` 429'd → OTX hard-stopped this run, resume after backoff.
4. OTX `is.gd` full pull (4,309 URLs) — mine for other agent-shaped short links beyond our 5 slugs. (STILL OPEN — blocked by OTX 429 this run)

## 2026-10-05 run notes
- Anonymous urlscan search is 30-day-windowed (`search_date_limit_days: 30`) — June-activity negatives are weak.
- New other-operator leads from OTX lhr.life: `/c/NN` payload campaign (`02e18ab88f2ece`), `/c`+`/r` tunnel family, `agents.json`/`llms.txt`/`openapi.yaml` agent-server tunnel (`48e0cb905290ad`), `/api/changelog`+`/api/manifest` recon. Full detail in `raw/otx-lhrlife-2026-10-05.md`.
- Pulsedive `api/info.php?indicator=` confirmed farmable no-auth (lhr.life: medium risk, retired, Amazon-registrar privacy WHOIS; pingllo.com: 404 unknown).
- VM egress outage 2026-10-05 ~04:53 UTC: all curl HTTPS → proxy 407. Runtime fetch path used as fallback.
