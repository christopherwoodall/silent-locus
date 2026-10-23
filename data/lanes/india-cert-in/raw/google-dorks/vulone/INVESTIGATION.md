# Investigation: VULONE "AI Agent Intrusion Campaign in Asia"

Date of work: 2026-10-23. All work was passive (GET only). No logins. No sessions.
Terms: a claim marked OBSERVED comes from my own checks. A claim marked UPSTREAM
comes from a report I read. A claim marked INFERENCE is my judgement from evidence.

## What the report claims (UPSTREAM: VULONE primary report, byline 18 Oct 2026)

VULONE says one operator ran an AI-agent attack platform from 202.61.139.15.
VULONE's claims:

- The host served its whole /tmp directory over HTTP on port 9000 with no
  login, from 29 Sep 2026 22:13 UTC to 15 Oct 2026. The same listing sat on
  202.61.139.137. The open directory held 339 files.
- The platform used Cairn, an open-source AI-agent framework. One dispatcher
  drove up to 116 short-lived Kali Linux worker containers. Workers talked to
  one LLM (global:deepseek-v4.1-flash) through one local gateway.
- Scale per the operator's own records: 66 intrusion projects, 24 Sep to 14 Oct.
  48 reached session-level access: 6 at root or SYSTEM, 39 at non-root command
  execution, 3 at webshell stage. Victim-side checks are still pending.
- Named targets include: Vietnam (mod.gov.vn, mps.gov.vn, bocongan.gov.vn,
  nso.gov.vn, moha.gov.vn, dongnai.gov.vn, hatinh.gov.vn), Taiwan (ly.gov.tw,
  Ministry of Justice systems), Indonesia (bin.go.id), India (cdac.in).
- Final project: cdac.in (C-DAC India), opened 14 Oct. Access via default
  admin/admin on a WSO2 API Manager console.
- Entry points were old flaws and defaults: Shellshock (CVE-2014-6271), JBoss
  Seam (CVE-2010-1871), anonymous FTP plus MSSQL xp_cmdshell, ASP.NET ViewState
  deserialization, SSRF chains, ecommerce API credential reuse, Redis cron
  reverse shell.
- Operator rules: send commands by POST only, clean up evidence directories,
  write payloads in English/ASCII only (no Chinese comments).
- Attribution: one operator or a very small group (high confidence), China-linked
  and Chinese-speaking, financially motivated. No evidence of state backing.
- IOCs published: 202.61.139.15 and 202.61.139.137 (AS152194, CTG Server Ltd,
  Singapore); ports 22, 443, 8000, 8443, 4443, 9000; exfil ports 8899, 8997,
  9099, 9201, 9955 with PUT /ev/; TLS self-signed cert CN 202.61.139.15,
  valid 3–5 Oct 2026, SHA-256 fingerprint
  93:17:8D:D2:F9:25:16:EB:D5:24:81:DE:C2:EE:54:68:BF:5E:97:86:83:9E:67:19:CA:E0:69:EC:D8:C5:41:FF;
  operator SSH key ssh-ed25519
  AAAAC3NzaC1lZDI1NTE5AAAAIKo+sIL3HUlVhjn6PDSGak+C/hEMAx+xL63z8ZhE9tHa;
  user agents pi (win32 10.0.19045, x64), pi (linux 7.0.0-28-generic, x64),
  client strings ccswitch and Cairn/1.0, server banner SimpleHTTP/0.6
  Python/3.12.3; tool files i051_shock_rce.py, MssqlProbe.java,
  sakip_i061.tgz, cred_scan.py, config_cred_scan.py, cairn_guard.sh,
  cairn_disk_guard.sh.

## What I could independently verify (OBSERVED)

1. ASN and org match. Shodan shows AS152194, CTG Server Ltd. on both
   202.61.139.15 and 202.61.139.137. This matches VULONE exactly.
2. TLS certificate matches. Shodan's cert for 202.61.139.15 has CN
   202.61.139.15, validity 3–5 Oct 2026, and chain SHA-256
   93178dd2f92516ebd52481dec2ee5468bf5e9786839e6719cae069ecd8c541ff.
   This is the same as VULONE's published fingerprint, byte for byte.
3. Shodan itself tags both hosts "open-dir" and "self-signed". Its scans saw
   SimpleHTTPServer with title "Directory listing for /" on port 9000.
   This is Shodan's own observation, not VULONE's.
4. Primary matches secondary. I fetched VULONE's own report (vulone.com).
   Every IOC above appears there verbatim. The Safeguard blog post did not
   distort the source.
5. Spread confirmed. An OTX pulse (created 2026-10-20, id
   6ad746d9f4d60f58d5f30ab4) lists both IPs under this campaign name.
   This is a repost of the same report, not fresh evidence. Weak signal.

## Current live status (OBSERVED)

- 202.61.139.15 port 9000: my single GET on 2026-10-23 timed out (HTTP 000).
  Not reachable from this network. This fits VULONE's note that exposure
  ended 15 Oct. Shodan's record for .15 (refreshed 2026-10-22) shows only
  ports 443 and 4443 current.
- 202.61.139.137: Shodan's record refreshed 2026-10-23 03:45 UTC still lists
  port 9000 with SimpleHTTPServer and "Directory listing for /", plus the
  "open-dir" tag. Treat the mirror as still exposed per passive scan data.
  Caveat: Shodan lists mix current and past services; I did not probe .137
  (out of task scope).

## What remains unverified

- The 48-accesses figure is the operator's own tally. No named victim has
  confirmed publicly as of 22 Oct. This stays UPSTREAM, single source.
- The cdac.in / WSO2 admin/admin claim is single-source (operator's own
  records via VULONE). I did not probe cdac.in or the WSO2 console.
- The Kenya mobile fetch (102.0.27.92, Airtel Kenya, 5 Oct) is a log claim
  only. Not verifiable passively.
- The 339-file manifest, dispatcher database, and session logs are not
  public. VULONE withholds file hashes. Victim identities beyond named
  domains are not published.

## Grade

- 202.61.139.15 was a site launching malicious traffic: CORROBORATED
  hostile C2/staging/exfil node. The campaign role is UPSTREAM (VULONE's
  evidence set). The infrastructure markers (ASN/org, TLS cert fingerprint,
  open-dir tag, SimpleHTTPServer directory listing) are OBSERVED and match.
  Past active; port 9000 dead as of 2026-10-23.
- 202.61.139.137 (mirror): CORROBORATED infrastructure, currently appears
  exposed per Shodan's latest passive scan (2026-10-23). INFERENCE: still
  serving open directories on ports 9000 and 8888.
- Campaign-scale claims (66 projects, 48 accesses, named victims including
  cdac.in): UNVERIFIED beyond VULONE. Do not cite as fact. Honest null stands.

Bottom line: the infrastructure core of the report checks out against
independent passive scans. The attack campaign itself is one reporter's
single-sourced account and stays unconfirmed.
