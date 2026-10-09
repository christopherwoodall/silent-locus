# INFRA-TRACKER FINDINGS — usemod.org WikiPatches/ClipBoard OVH hosts
**Worker:** INFRA-TRACKER (infrastructure analyst for coordinator CLIPBOARD)
**Date:** 2026-10-05
**Scope:** Shodan STORED OBSERVATIONS ONLY + corpus grep for the five masked OVH hosts.
No port scanning, no host connections, no DNS probing beyond what Shodan returns.
Infrastructure only — no human/operator attribution.

## Method
- Tool: `~/workspace/skills/shodan/bin/shodan.py` (`search`, `count`), curl-based, polite pacing (3s between calls).
- Queries were `hostname:"<pattern>"` per range suffix. All results below are **stored** Shodan observations (timestamps carried on each record); nothing was scanned or touched by this worker.
- Corpus grep: `grep -rnE '158-69-118|158-69-119|54-39-18|94-23-61|94-23-25'` and dotted-quad form `158\.69\.118|158\.69\.119|54\.39\.18|94\.23\.25|94\.23\.61` across the full `~/workspace/silent-locus/` tree.

## Baseline (from the corpus, confirming the task's framing)
The census records (`swarm.termina.digital/pub/actor.jsonl`, venue_id null, kind "ip", notes "masked"):

| actor id | first_seen | last_seen |
|---|---|---|
| `ip:*.ip-158-69-118.net` | 2026-05-23T07:03 | 2026-05-31T20:55 |
| `ip:*.ip-158-69-119.net` | 2026-05-23T05:12 | 2026-05-31T19:14 |
| `ip:*.ip-54-39-18.net` | 2026-05-23T06:10 | 2026-05-31T19:47 |
| `ip:*.ip-94-23-61.eu` | 2026-05-23T07:24 | 2026-05-31T20:51 |
| `ip:*.ip-94-23-25.eu` | 2026-05-23T08:16 | 2026-05-31T20:49 |

Each pattern occurs exactly 2x in `actor.jsonl`. Host octets are **masked** — specific IPs/hostnames of the five editors are not in the census.

---

## 1. `*.ip-158-69-118.net` (OVH Canada, BHS) — 158.69.118.0/24

**Shodan stored observations:**
- Exact query: `shodan.py count 'hostname:"ip-158-69-118.net"'` → **total: 1002**
- Sample (`search`, limit 5), verbatim:
  - `158.69.118.21:4190` Dovecot Pigeonhole sieve — PTR `ns520721.ip-158-69-118.net` — 2026-10-05T17:02:06
  - `158.69.118.174:21` (no product) — PTR `ns520660.ip-158-69-118.net` — 2026-10-05T16:53:26
  - `158.69.118.230:21` Pure-FTPd — PTR `ns521577.ip-158-69-118.net` — 2026-10-05T16:47:55
  - `158.69.118.130:21` (no product) — PTR `ns520585.ip-158-69-118.net` (+ `hosting.tuisp.pe`) — 2026-10-05T16:37:58
  - `51.222.67.145:995` (no product) — PTRs `ns520640.ip-158-69-118.net`, `ip145.ip-51-222-67.net` — 2026-10-05T16:29:01
- Org on in-range records: `OVH Hosting, Inc.` / ISP `OVH SAS`.
- Note: the 5th record shows the `hostname:` filter matches **PTR history** — `51.222.67.145` is outside the /24 but once held an `ip-158-69-118.net` PTR. Counts therefore describe the /24's PTR population (current + historical), not a live host census.

**Corpus grep:** no new sightings. Dash-form hits only in known locations: `actor.jsonl`, `db_scan.html` (census scrape), `hacker/FINDINGS.md`, `clipboard-followup/FINDINGS.md`, `ovh-sweep/FINDINGS.md`, `COORDINATOR.md`.

---

## 2. `*.ip-158-69-119.net` (OVH Canada, BHS) — 158.69.119.0/24

**Shodan stored observations:**
- Exact query: `shodan.py count 'hostname:"ip-158-69-119.net"'` → **total: 767**
- Sample (limit 5), verbatim:
  - `192.99.159.213:587` Exim smtpd — PTRs `opx-gds-pro1.sys-it.io`, `ip213.ip-192-99-159.net`, `cgg-gds-pro1.it-cg.group`, `ns521115.ip-158-69-119.net` — 2026-10-05T17:18:22
  - `192.99.159.210:143` (no product) — same PTR set — 2026-10-05T16:48:57
  - `158.69.119.101:21` Pure-FTPd — PTR `ns521086.ip-158-69-119.net` — 2026-10-05T16:46:54
  - `158.69.119.104:21` Pure-FTPd — PTRs `server.diamantecreditoimobiliario.com.br`, `ns521089.ip-158-69-119.net` — 2026-10-05T16:30:48
  - `158.69.119.137:21` Pure-FTPd — PTRs `ns521122.ip-158-69-119.net`, `server.eucamad.com.br` — 2026-10-05T16:23:33

**Corpus grep:** no new sightings (same known-location set as above).

---

## 3. `*.ip-54-39-18.net` (OVH Canada, BHS) — 54.39.18.0/24

**Shodan stored observations:**
- Exact query: `shodan.py count 'hostname:"ip-54-39-18.net"'` → **total: 462**
- Sample (limit 5), verbatim:
  - `54.39.18.205:81` OpenResty — PTR `ns556588.ip-54-39-18.net` — 2026-10-05T16:43:26
  - `54.39.18.17:3001` (no product) — PTR `ns556063.ip-54-39-18.net` — 2026-10-05T16:33:36
  - `54.39.18.53:2082` (no product) — PTR `ns556484.ip-54-39-18.net` — 2026-10-05T16:33:00
  - `54.39.18.110:22` OpenSSH — PTR `ns556529.ip-54-39-18.net` — 2026-10-05T15:07:14
  - `54.39.18.128:465` Postfix smtpd — PTRs `ezekiel.srghosting.com`, `ns556607.ip-54-39-18.net` — 2026-10-05T13:52:10

**Corpus grep:** no new sightings. Two off-tree dotted-form hits are **regex false positives** on `57.154.39.184` (substring `54.39.18` inside `57.154.39.184`):
- `data/2016-12-28-rmn-re/events.jsonl` line 321 (`link.ip: 57.154.39.184`, rmn.re `zz746749` shortener record) and its raw tables — NOT 54.39.18.x
- `bitily_agent_activity_expanded.csv` line 392 (`57.154.39.184`) — same false positive
These are recorded here explicitly so nobody re-flags them.

---

## 4. `ip-94-23-61.eu` (OVH France, RBX/GRA) — 94.23.61.0/24

**Shodan stored observations:**
- Exact query: `shodan.py count 'hostname:"ip-94-23-61.eu"'` → **total: 178**
- Sample (limit 5), verbatim:
  - `164.132.252.99:21` (no product) — PTRs `ip99.ip-164-132-252.eu`, `ns329576.ip-94-23-61.eu` — 2026-10-05T16:31:59 (PTR history: outside /24)
  - `94.23.61.110:80` nginx — PTRs `ns329576.ip-94-23-61.eu`, `escoladesquilorri.com` — 2026-10-05T12:35:15
  - `94.23.61.165:80` nginx — PTR `ns3096353.ip-94-23-61.eu` — 2026-10-05T12:03:53
  - `94.23.61.110:465` Postfix smtpd — PTR `ns329576.ip-94-23-61.eu` — 2026-10-05T10:52:50
  - `94.23.61.164:111` (no product) — PTR `ns3098932.ip-94-23-61.eu` — 2026-10-05T09:00:12

**Corpus grep:** no new sightings (known locations only).

---

## 5. `ip-94-23-25.eu` (OVH France, RBX/GRA) — 94.23.25.0/24

**Shodan stored observations:**
- Exact query: `shodan.py count 'hostname:"ip-94-23-25.eu"'` → **total: 90**
- Sample (limit 5), verbatim:
  - `94.23.25.33:8080` (no product) — PTR `ns344479.ip-94-23-25.eu` — 2026-10-05T16:05:59
  - `94.23.25.22:2222` OpenSSH — PTR `ns369083.ip-94-23-25.eu` — 2026-10-05T15:42:31
  - `94.23.25.192:443` Apache httpd — PTRs `admin.entrup.io`, `ns362355.ip-94-23-25.eu` — 2026-10-05T11:11:11
  - `94.23.25.62:8000` (no product) — PTR `ns367426.ip-94-23-25.eu` — 2026-10-05T09:56:18
  - `94.23.25.203:81` Apache httpd — PTR `ns3046422.ip-94-23-25.eu` — 2026-10-05T09:44:12

**Corpus grep:** no new sightings (known locations only).

---

## Corpus grep — complete hit list (dash form)
- `data/2026-09-28-chinese-amap-fleet/personas/pastebin-plunderer/raw/deep-dive/lane3-colony-bullfincher/ref/run1/scrape/outputs/swarm.termina.digital/pub/actor.jsonl` — KNOWN (census records)
- `.../swarm.termina.digital/db_scan.html` — KNOWN (census DB scrape UI)
- `data/2026-09-28-chinese-amap-fleet/german-french-swarm-hunt/workers/hacker/FINDINGS.md` — KNOWN (hunt notes)
- `data/2026-09-28-chinese-amap-fleet/german-french-swarm-hunt/workers/clipboard-followup/FINDINGS.md` — KNOWN
- `data/2026-09-28-chinese-amap-fleet/german-french-swarm-hunt/workers/ovh-sweep/FINDINGS.md` — KNOWN
- `data/2026-09-28-chinese-amap-fleet/german-french-swarm-hunt/COORDINATOR.md` — KNOWN
- `data/2026-09-05-termina-digital/raw/wayback/db/scan.html` — KNOWN (census scrape)
- `clipboard-followup/workers/wiki-surgeon/raw/*.html` — **zero** exact-hostname hits

**Verdict: zero new sightings of the five patterns anywhere in the tree.**

---

## Graded summary

### OBSERVED
1. All five ranges have live, current Shodan stored observations (freshest timestamps 2026-10-05): they are ordinary OVH hosting ranges — `ns*`/`nsNNNNN*` PTR naming, mail (Exim/Postfix, ports 587/465/995), FTP (Pure-FTPd :21), and shared web hosting (nginx/Apache/OpenResty on 80/81/443/8000/8080), plus admin panels (2082/3001/2222). Nothing in the stored data is distinctive of agent infrastructure; it reads as bulk shared/dedicated hosting.
2. Shodan **cannot** isolate the five wiki editors: the census masks their host octets (`notes: "masked"`), and the `hostname:` filter matches PTR strings across whole /24s including historical PTRs on IPs now elsewhere (observed: `51.222.67.145`, `192.99.159.210/213`, `164.132.252.99`).
3. Corpus grep: **no new sightings** of the five patterns outside the already-known locations (census records + hunt notes). The only off-tree dotted-form hits were regex false positives on `57.154.39.184` (noted above so they are not re-flagged).
4. Context from sibling lane (ovh-sweep, observed by that worker, not re-derived here): urlscan returned 0 hits for all five `ip:` range queries; crt.sh returned `[]` for all five wildcard hostname queries; same-range hosts (`ns520686.ip-158-69-118.net`, `ns521015.ip-158-69-119.net`, `ns302180.ip-94-23-61.eu`) appeared as pharma comment-spammers in a German guestbook Jan 2026 — a general abuse-box signal for these ranges, not agent evidence, and different specific hosts than the masked editors.

### INFERENCE
- The honest negative on per-host attribution: because the census values are masked and Shodan data is range-level (whole /24s, current+historical PTR), **no Shodan observation can be tied to the specific five census actors**. Any claim linking a specific stored record to the May 23–31 wiki-edit burst would be inference, not observation.
- The ranges look like commodity OVH hosting churn (PTR reassignments, shared-hosting naming) — consistent with throwaway VPS usage, but equally consistent with any other bulk-hosting tenant. The burst window (May 23–31 2026) is stale relative to all stored Shodan observations (Oct 2026), so stored data cannot speak to the hosts' May state.
- No evidence for or against the five hosts being the same physical boxes today — PTR churn makes re-identification from current data unreliable.

### Open threads for CLIPBOARD
- If the exact masked hostnames/IPs ever surface (wiki API, wayback CDX of diff URLs, usemod.org server logs), Shodan `host <ip>` historical records could be checked then. Until then, infra attribution is at a dead end by design.
- Historical Shodan (paid plan API `history:true`) was not used — flag if the hunt wants the extra spend.
