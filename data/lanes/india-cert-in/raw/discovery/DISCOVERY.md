# DISCOVERY lane — india-cert-in — 2026-10-23

Objective: find sites launching malicious AGENT traffic related to the India CERT-In
2026-10-16 disclosure (advisory CIAD-2026-0049, "AI Agents as Attack Vectors",
critical). Advisory verified full-text: names NO providers, NO victims, NO
infrastructure indicators (cached: CERT-In_CIAD-2026-0049.pdf).

Key public-reporting fact shaping this lane: advisory category 2 describes
"publicly available, AI-native offensive-security frameworks" that are "misused
and rebranded, with a large number of deployments observed across infrastructure
in multiple countries". That is the hunt shape.

## Method
Shodan host search "Cairn" (94 unique IPs enumerated of 131; page 2+ blocked by
plan query-credit exhaustion), passive curl GETs of open endpoints only, Shodan
host records for 8 IPs, urlquery bounded searches (cairn/ips/hostnames = 0 hits;
zz= / uqtag= / 渗透测试 = prior-hunt grammar noise), DNS-over-HTTPS,
Wayback CDX (liftzen.in: 1 capture 2026-09-21, body fetch failed twice;
cairn26.com: 0 captures), news-vertical search for follow-ups.

## CANDIDATE SITES

### 1. 148.113.3.75:8081 — Cairn agent-harness instance on Indian-org infrastructure
- Observed: :8081 302 -> /ws/login -> /oauth2/authorization/custom -> Keycloak
  login page titled "Sign in to cairn" (19 keycloak refs, realm "cairn").
  :8080 serves Keycloak whose realm in the SSO URL is literally "cairn".
  :80 = stock Apache default page (nothing).
- Org: OVHTECH R&D (INDIA) PRIVATE LIMITED (OVH Indian legal entity), AS16276,
  OVH SAS ISP. Shodan country:"IN" count for "Cairn" = 1, this host.
  Hostnames: magnitude14.xsalto.net, ip75.ip-148-113-3.net.
- Why agent infra: a deployment of the same Cairn agent-harness platform as the
  4 counsel-cleared malicious panels (prior work: unauth-RCE / webshell-to-root
  projects against third-party sites). "Sign in to cairn" + realm "cairn" ties
  it to that product line, not a coincidental name.
- India connection: STRONG on infrastructure (Indian org, IN geo) — but ZERO
  observed evidence it was involved in the CERT-In incidents. Could equally be a
  legitimate internal R&D deployment.
- Not in public reporting (advisory names no infrastructure).
- Confidence: MEDIUM that it is a Cairn agent-harness instance; LOW that it
  launches malicious agent traffic; India-link = infrastructure only.
- Clearance: PENDING (not counsel-cleared). Only passive GETs done. If counsel
  clears, the Keycloak-protected app behind SSO is the log surface of interest.
- Evidence: ovh_in_148.113.3.75_8081_login.html (7025 B), _hdrs.txt,
  ovh_in_148.113.3.75_port80.html, PROBE_LOG.txt.

### 2. 161.248.63.110:443 — Cairn-platform AUTOMATED PENTEST workbench (open, no auth on /)
- Observed: 200, title "自动化渗透测试工作台" (automated pentest workbench),
  meta description "面向已获授权目标的自动化渗透测试与安全评估工作台"
  (automated pentest & security-assessment workbench for authorized targets).
  Response header X-Cairn-Server-Time-Ms. JS bundle (1.02 MB) contains:
  CairnChatPanel components, localStorage keys "cairn.*", X-Cairn-Project
  request headers, /api/v1/projects task API, /api/auth/balance + /api/auth/billing
  (paid credit model for agent runs), scanner_proxy setter (scans routed via
  proxy). Same codebase family as the cleared malicious Cairn panels.
- Org: ALICE NETWORKS LTD, AS215355. No India strings in bundle; no India org.
- Why agent infra: it IS an agent harness — an automated pentesting agent
  workbench on the same platform family that prior counsel-cleared panels used
  to run unauth-RCE webshell-to-root projects. Whether "authorized targets only"
  is true in practice is unverified; the cleared siblings were not.
- India connection: none observed.
- Not in public reporting.
- Confidence: HIGH it is a Cairn-family agent-harness; MEDIUM it launches
  malicious agent traffic (self-describes as authorized-only; cleared siblings
  in the same family ran malicious projects).
- Clearance: PENDING. Only passive GETs of / and the public JS asset done.
  The /api/v1/projects endpoint and any exposed logs need counsel clearance
  before pulling.
- Evidence: pentest_wb_161.248.63.110_root.html (sha256
  a58eed50376f5a018673e018811eb367027abd059c0c613b63a2143b883b4ef51),
  _bundle.js (sha256 e21174666b1712b16684b084ff371d46b94e138b8320f1f3daaaccb05dd2242f),
  _hdrs.txt.

### 3. "Cairn CF Platform" fleet — 156.240.236.0/24 (Tcloudnet, AS399077), 48 hosts
- Observed: 47 of 94 enumerated Cairn hosts return 401 with
  `WWW-Authenticate: Basic realm="Cairn CF Platform"` (plus 13 plain "Cairn",
  2 "cairn-plus panel", 2 "Cairn - Authorized access", 1 "Cairn AI", etc.).
  Homogeneous: nginx/1.18.0 (Ubuntu), ports 8000 (https) / 8787, scanned
  2026-10-07/08 (one re-scan 10-22). Verified live 2026-10-23 on 156.240.236.6:8000
  (401 body = stock nginx page, realm header the only identifier).
- Why agent infra: same Cairn product family, operator-scale deployment
  (a /24 of near-identical instances) — fits the advisory's "rebranded ...
  large number of deployments ... across infrastructure in multiple countries"
  shape.
- India connection: none observed (Tcloudnet; no Indian org/geo).
- Confidence: MEDIUM (family); LOW for any specific malicious-traffic claim.
- Clearance: PENDING. Behind basic auth; no credential attempts made.
- Evidence: cfplatform_hdrs.txt, cfplatform_root.html, cairn_shodan_enumeration.txt.

### 4. 衍迹 (Yanji) "自主探索工作台" autonomous-exploration workbenches — 7 hosts
- 101.251.178.216:443, 101.251.178.220:8080 (Xiamen Kuaikuai, AS133775);
  124.221.7.40:18080 (Tencent Beijing, AS45090); 154.44.28.46, 154.44.31.220
  (Cogent); 186.244.208.117:443 (Uscloud); 189.24.68.125:8080, 189.24.68.208:443,
  189.24.70.181:443 (NetLab Global-AP, AS979); 38.76.168.15:8787,
  38.76.170.211:8080 (Cogent). Title "衍迹 · 自主探索工作台".
- Why noted: Chinese-language autonomous agent exploration workbenches = agent
  harnesses by description. No observed malicious use, no India connection.
- Confidence: LOW (related family only, no malice evidence, no India link).
  Recorded for completeness, not a lead.
- Clearance: PENDING (no GETs attempted beyond Shodan banners).

### 5. Ancillary Cairn-realm hosts (weak, recorded only)
- 46.224.67.169:443 (Hetzner; Basic realm="Cairn"; hostnames ca.liftzen.in,
  rengine.example.com; tags "ai") — TLS fetch failed from this VM (egress);
  ca.liftzen.in -> Cloudflare; liftzen.in -> 216.198.79.1 (DoH). Wayback: one
  liftzen.in capture 2026-09-21, body unfetchable. Not pursued further: no
  observed agent behavior beyond the realm string.
- 108.165.177.216:443 (BaseHTTP/0.6 Python/3.14.4, realm "Cairn"),
  172.237.74.202:443 (Caddy, realm "Cairn"), 8.232.250.83:443 (Google Cloud,
  api.cairn26.com) — realm/hostname matches only, no content observed.
- 148.113.3.75 is the only one of these with an India nexus; the rest are LOW.

## PRIOR CLEARED PANELS — India check (no re-attribution)
- 185.242.245.159 (PSB HOSTING, geo CN), 31.56.206.187 / 31.57.47.29
  (CGI GLOBAL), 31.59.92.155 (PT Atharva, geo BG): Shodan full banners contain
  NO India strings; geolocated CN/BG. Direct re-fetch from this VM failed
  (TCP empty reply on :8000) — no new observations. No India connection found.
  (Counsel-cleared status unchanged; no new scraping performed.)

## REJECTED (investigated, ruled out)
- 82.66.245.153:5000 (Free SAS): "Cairn" = Synology DiskStation device name
  (NetBIOS CAIRN). Consumer NAS, not agent infra.
- 54.194.56.113:80 (AWS): 302 -> cairn-sport.com (sports site). Coincidental brand.
- 76.164.196.96:25565: "Cairn SMP" Minecraft server. Not agent infra.
- 66.179.209.61:443: "The Security Executive Council" (securityexecutivecouncil.com).
  Coincidental "Cairn"? Actually matched query via unknown field; site is a
  security council page, not a harness. Rejected.
- urlquery: 0 hits for "cairn", "cairn26", "liftzen", "161.248.63.110",
  "185.242.245.159". No agent-submission trail for the Cairn family in urlquery.
- Wayback: no captures for cairn26.com.

## Gaps / caveats
- Shodan query credits exhausted: 94 of 131 "Cairn" matches enumerated (page 1);
  37 hosts (incl. possibly more Cairn-realm/auth variants) unreviewed.
  The 4 cleared panels did not appear in page 1 (they should match title "Cairn").
- TLS fetches to 46.224.67.169, 108.165.177.216, and the 4 cleared panels fail
  from this VM (egress proxy empty-reply); characterization rests on Shodan
  banners + the fetches that did succeed.
- liftzen.in Wayback body unfetchable (2 attempts; backend flakiness).
- No finding in this lane is attributed to the CERT-In incidents; the only
  India nexus is infrastructure-org (candidate 1).
