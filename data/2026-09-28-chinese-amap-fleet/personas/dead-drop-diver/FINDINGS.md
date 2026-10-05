# FINDINGS — DEAD-DROP DIVER

*Started 2026-10-05 ~07:06 UTC. Incremental; resume from lanes.log. Opsec: all candidate URLs LOGGED, never live-fetched.*

## Lanes status
- [x] Lane 1: dead-drop services sweep (webhook.site, beeceptor, pipedream via urlquery htmx)
- [x] Lane 2: grammar-first search (search engines — null, see below)
- [x] Lane 3: retrieval-cadence analysis (limited — notes below)
- [x] Lane 4: cross-reference vs 3 corpora + codebreaker inventory

## Agent shapes found

### SHAPE-1: Fresh webhook.site inbox, `?page=header3` param — GENUINELY NEW
- URL: `webhook.site/3b5027e4-de70-4980-a49d-7ae97613c517?page=header3`
- Observed: urlquery report `c9104bb8-8c1f-428f-b421-c57d0d4d53be`, scanned **2026-10-05T03:18Z** (today)
- Report metadata (urlquery htmx, NOT the inbox): 200 OK, 367 bytes, single-line HTML, IP 178.63.67.106 (Hetzner AS24940 — same infra as the fleet inbox `6ddc559e`)
- Why agent-shaped: fresh UUID inbox scanned within hours; `?page=header3` query param is a machine-style discriminator, not a human bookmark
- NOT in any of our 3 corpora; NOT in codebreaker inventory
- Opsec: inbox contents never fetched

### SHAPE-2: Credential-bearing webhook callback — GENUINELY NEW
- URL: `webhook.site/c6aaa535-3b13-4b78-9ec8-cd0817a2f7a5?userId=6a769ace0015efdd7fac&secret=26b6ef5dc835f556a3663dc5e512dd93abfe0ce6ff063d1a3a77a9a687bd3176&expire=2026-08-08T13%3A23%3A55.991%2B00%3A00&project=67ff3f0c00072eaf30a0`
- Observed: urlquery report `3ffdfab0-fcd5-4893-95fd-16d7980664d6`, 2026-08-08T12:30Z
- Why notable: `userId` + `secret` + `expire` + `project` params = machine-generated callback credential, agent/harness-shaped
- NOT in corpora; NOT in codebreaker

### SHAPE-3: `/xss-osint-insert` webhook path, double-submitted — GENUINELY NEW
- URL: `webhook.site/2ab7ca12-fdce-4475-8bf0-950c0cbf28f2/xss-osint-insert`
- Observed: TWO urlquery reports `fe637b8f-8a6f-4647-89cd-b20867c9ba67` + `c6ee72ff-86fa-4a49-83b4-7906bdb721a5`, both 2026-08-08T12:25Z (same minute — double submit)
- Report metadata: inbox page rendered + webhook.site app assets loaded (inbox existed at scan)
- Why notable: explicit "xss-osint" path label = someone's OSINT harness exfil target; double-submit in same minute = machine cadence
- NOT in corpora; NOT in codebreaker

### SHAPE-4: `?r=<19-digit>` nonce family — GENUINELY NEW
- `webhook.site/c1bf6b38-d6ea-4446-b17e-5f6c7a1cb357?r=1782071176301141190` (2026-07-07, report `6fbff60b`)
- `webhook.site/441b7745-1087-463e-b539-984a2ee3ea65?r=1782070800983511679` (2026-06-24, report `2baccf7b`) — inbox itself is codebreaker-known (legacy), the `?r=` nonce param is new
- Why notable: 19-digit nonces `1782071176301141190` / `1782070800983511679` share prefix `178207` — same operator/timeframe family, 13 days apart
- NOT in corpora; NOT in codebreaker

### SHAPE-5: More undocumented inboxes — GENUINELY NEW (logged, ungraded)
- `webhook.site/35f6980c-7dc6-4af4-b646-56ca0070a200` — 2026-08-31, report `13cced5b-0346-4ba2-afe0-ae387cba403a`
- `webhook.site/1eafadc3-9bb7-42d1-a9f0-0ced18cb6d56` — 2026-07-31, report `c061c59d-a0dc-4237-ab82-6289bdfab765`
- `bee4dc9e-3935-451f-a724-b8c135763823.webhook.site` — 2026-08-08, report `404a38a6-05cb-477e-ba74-f9fac524c7c9` (subdomain-style inbox)

### SHAPE-6: Beeceptor XSS-exfil dead-drop family — GENUINELY NEW SURFACE
Beeceptor/pipedream appear in ZERO of our 3 corpora and ZERO of codebreaker's inventory. urlquery holds a Apr–May 2026 cluster of XSS-exfil dead drops:
- `akwuwue.free.beeceptor.com/leak?data='` — 2026-05-11, report `3399d295-0cba-4f10-990e-450c083f3fee`
- `hhshdh.free.beeceptor.com/leak?url='+encodeURIComponent` — 2026-04-29, report `c337a249-dfe7-4090-9573-513e4db5eb12`
- `ahshsu.free.beeceptor.com/final?d=`+document.domain` — 2026-04-29, report `a16cb30b-9fed-458f-a8ee-01388a5464f2`
- `hjhjhjhj.free.beeceptor.com/grabber.php?c='+document.cookie</script>` — 2026-04-24, report `4742073d-42e5-423a-99b0-e3479c7c867d`
- `jiji-script.free.beeceptor.com` — 2026-05-20, report `f5883373-d46e-467e-81b4-078f292a9114`
- `eo6p96x7ax0vcaj.m.pipedream.net/Oneotsuka` — 2026-09-03 (pipedream)
- Pattern: keyboard-mash subdomains + `/leak`, `/final`, `/grabber.php` paths + document.cookie/domain exfil params. Classic XSS-kit grammar — operator could be human pentester OR agent; the SURFACE is what's new to our data. Logged as lead, not claimed as agent.

### OURS (already in corpora / codebreaker-documented — not re-reported)
- `webhook.site/6ddc559e-5c08-4915-a5b2-f4addc42368a` — fleet nav-replay inbox, title `taersitokennav1791126060505-START` (epoch 1791126060505 = scan time itself, a self-nonce). Codebreaker: ALIVE, 5 requests.
- `webhook.site/0a947514-5b43-4030-9f9f-b193dd2d519b` — fleet outlier (Firefox 157, Iraq/Kurdistan Net)
- `webhook.site/441b7745-1087-463e-b539-984a2ee3ea65` — legacy, DEAD
- `webhook.site/00f36f21-d00e-48b3-9456-8bf532e8c863` — legacy, DEAD
- oai-tag-sweep corpus: `litter.catbox.moe/hdcf0x.html?x=1778400745.7904322` (epoch-nonce litterbox URL, already in corpus)

## Null results
- Search-engine grammar sweep (`"zz=oai"` + webhook/pastebin/dead-drop; `"uqscan"` + urlquery/webhook.site; `rentry.co OR paste.rs OR "0x0.st"` + `zz=`/`uqscan`/`epoch`; `webhook.site` + `taersi`/`-START`): engines do not index these URL params usefully — all noise (academic papers, blockchain spam, docs). Honest zero.
- Shodan `webhook.site` host search (41 hosts): unrelated (netsapiens etc.) — Shodan can't see UUID-pathed inboxes, as expected. Infra pivot value: low for inbox discovery, keep for self-hosted receivers.
- 0x0.st, file.io, tmpfiles.org, transfer.sh, paste.rs, ix.io, rentry.co, privatebin: no agent-shaped hits in this pass.

## Retrieval-cadence notes (Lane 3)
- xss-osint-insert double-submit (same minute, 2 reports) = machine cadence, not human double-click (different report IDs, identical timestamps)
- `?r=` nonce pair 13 days apart with shared `178207` prefix = same operator family reusing nonce grammar
- Fresh inbox `3b5027e4` scanned 2026-10-05T03:18Z — within last 24h; worth re-checking urlquery for follow-up scans (cadence)

## Infra/tooling notes
- Shodan skill (`~/workspace/skills/shodan/bin/shodan.py`) FIXED during this run: curl `--max-time 30` timed out (rc=28) on slow Shodan API responses — bumped to 90s + 3 retries. Dev-plan key verified working (`api-info` → plan `dev`, 100 query credits).
- urlquery htmx (`uq_htmx_curl.py`) is the workhorse for dead-drop discovery — `url.domain:webhook.site`, `url.domain:beeceptor.com` queries

## Open threads
1. Re-sweep `url.domain:webhook.site` in 24–48h for new inboxes (the `3b5027e4` inbox is <24h old — its operator may still be active)
2. Grade SHAPE-6 (beeceptor): pull report metadata for the 4 exfil URLs to check submitter UAs / page titles — agent vs human-kit
3. `?page=header3` param — search urlquery for other `?page=` webhook.site URLs (possible family)
4. Litterbox/catbox lane still open (oai-tag-sweep has the pattern; external sweep not done)
5. privatebin.info directory + hastebin/paste.ee: not yet swept

## Candidate log (URL | where found | when observed | marker | classification)
| URL | Found via | Observed | Marker | Class |
|---|---|---|---|---|
| webhook.site/3b5027e4-de70-4980-a49d-7ae97613c517?page=header3 | urlquery htmx | 2026-10-05T03:18Z | fresh UUID inbox, ?page=header3 | GENUINELY NEW |
| webhook.site/c6aaa535-…?userId=…&secret=…&expire=…&project=… | urlquery htmx | 2026-08-08 | credential callback params | GENUINELY NEW |
| webhook.site/2ab7ca12-…/xss-osint-insert | urlquery htmx | 2026-08-08 (x2) | /xss-osint-insert path, double-submit | GENUINELY NEW |
| webhook.site/c1bf6b38-…?r=1782071176301141190 | urlquery htmx | 2026-07-07 | 19-digit ?r= nonce | GENUINELY NEW |
| webhook.site/441b7745-…?r=1782070800983511679 | urlquery htmx | 2026-06-24 | 19-digit ?r= nonce (inbox known) | GENUINELY NEW (param) |
| webhook.site/35f6980c-7dc6-4af4-b646-56ca0070a200 | urlquery htmx | 2026-08-31 | undocumented inbox | GENUINELY NEW |
| webhook.site/1eafadc3-9bb7-42d1-a9f0-0ced18cb6d56 | urlquery htmx | 2026-07-31 | undocumented inbox | GENUINELY NEW |
| bee4dc9e-3935-451f-a724-b8c135763823.webhook.site | urlquery htmx | 2026-08-08 | subdomain-style inbox | GENUINELY NEW |
| akwuwue.free.beeceptor.com/leak?data=' | urlquery htmx | 2026-05-11 | /leak exfil | GENUINELY NEW (surface) |
| hhshdh.free.beeceptor.com/leak?url='+encodeURIComponent | urlquery htmx | 2026-04-29 | /leak exfil | GENUINELY NEW (surface) |
| ahshsu.free.beeceptor.com/final?d=`+document.domain | urlquery htmx | 2026-04-29 | domain exfil | GENUINELY NEW (surface) |
| hjhjhjhj.free.beeceptor.com/grabber.php?c='+document.cookie | urlquery htmx | 2026-04-24 | cookie grabber | GENUINELY NEW (surface) |
| jiji-script.free.beeceptor.com | urlquery htmx | 2026-05-20 | undocumented | GENUINELY NEW (surface) |
| eo6p96x7ax0vcaj.m.pipedream.net/Oneotsuka | urlquery htmx | 2026-09-03 | undocumented | GENUINELY NEW (surface) |
