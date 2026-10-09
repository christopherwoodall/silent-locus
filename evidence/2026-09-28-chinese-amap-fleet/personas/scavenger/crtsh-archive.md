# Scavenger persona — crt.sh + archive.org recon
Date: 2026-10-04. Worker: recon subagent (depth 2/2). No pushes (per task).

## STATUS: hard zeros on live pulls — infra outage, not a negative
- VM egress fully down for the entire run window (23:37–00:05+ CDT): `curl` to
  crt.sh, google.com, huggingface.co, web.archive.org all returned HTTP 000 /
  connect-timeout (exit 28). DNS resolves fine (crt.sh → 198.18.241.68); TCP
  never completes. General egress outage, not crt.sh-specific.
- Runtime `browser.open` fetch service: crt.sh JSON API → HTTP 502 (3 attempts,
  retry-exhausted); web.archive.org CDX → empty body / HTTP 500 (3 attempts).
  Per policy those two endpoints were not retried further.
- Result: **0 certificates enumerated, 0 CDX rows pulled.** A background retry
  loop (`proc_c161b9741fc9`) is still running, attempting
  `https://crt.sh/?q=%25.tunn3l.sh&output=json` every 4 min ×12; if it succeeds
  the raw JSON lands at `/tmp/crtsh_probe.json`.
- What DID work: runtime `browser.search` (3 queries). All domain intel below is
  search-derived (epistemic status: review-asserted, not byte-verified).

## 1. crt.sh target list + queries (ready to run when egress recovers)
Exact queries (note %25 = %):
```
curl -s "https://crt.sh/?q=%25.tunn3l.sh&output=json"
curl -s "https://crt.sh/?q=%25.pinggy.link&output=json"
curl -s "https://crt.sh/?q=%25.trycloudflare.com&output=json"
curl -s "https://crt.sh/?q=%25.loca.lt&output=json"
curl -s "https://crt.sh/?q=%25.glitch.me&output=json"
curl -s "https://crt.sh/?q=%25.bore.pub&output=json"
curl -s "https://crt.sh/?q=%25.ngrok-free.app&output=json"
```
Skip `%.lhr.life` (localhost.run) — too large per task.

Parse plan (python/jq): for each JSON row keep `common_name`, `name_value`,
`not_before`, `not_after`, `issuer_name`. Dedupe on `name_value`.
- **Counts:** distinct subdomains per suffix.
- **Churn test:** group by issuer + 90-day cert lifetime; short-lived certs with
  random-looking labels issued in bursts = agent-shaped.
- **Agent-shaped grammar check** (from search-derived ground truth, verify in CT):
  - `tunn3l.sh`: 8-char hex (e.g. `a7f3c912.tunn3l.sh`) — random default
    (`tunn3l http 3000` → random 8-char hex; `--subdomain` for customs).
    Wildcard SSL via nginx per repo CLAUDE.md.
  - `pinggy.link`: `xxxx-xxx-xxx.pinggy.link` (3 random words/segments) free
    tier; `xxxx.a.pinggy.link` 4th-level for Pro/custom.
  - `trycloudflare.com`: random 4-word subdomains
    (`word1-word2-word3-word4.trycloudflare.com`).
  - `loca.lt`: `funny-tiger-42.loca.lt` (adjective-animal-number).
  - `glitch.me`: random word-pairs (`witty-recess`, `agreeable-death`).

## 2. Expired-then-revived: method + worked examples
**Method.** For a candidate domain D:
1. `curl -s "https://crt.sh/?q=D&output=json"` → sort certs by `not_before`.
2. Compute gaps between consecutive `not_after` → next `not_before`.
   Flag gap > 365 days followed by a fresh cert from a *different* issuer or
   with agent-shaped SAN patterns.
3. Confirm revival hosts agent-shaped content: check current DNS/A record vs
   historical (SecurityTrails/passive DNS), fetch the live host, look for
   agent-tunnel landing pages, open ports (22/3000/8000/8080), `/api`, MCP
   endpoints.
4. Rule out benign causes: registrar parking pages, CDN re-issuance, Let's
   Encrypt auto-renewal cadence (90-day rhythm = normal).

**Worked example A — glitch.me (dying, not revived).** Search confirms Glitch
announced shutdown during 2026 ("service is going to be shut down in 2026" —
NGCMan/Glitch-Project-Archive, created 2025-10-24). Implication: the entire
`*.glitch.me` namespace is becoming *abandoned* infrastructure. Any live
agent-shaped host still answering on glitch.me after the shutdown date is
either Fastly's holding page (expected) or something worth a second look.
CT check: look for certs issued for `*.glitch.me` subdomains *after* the
announced shutdown — those are the anomaly.

**Worked example B — tunn3l.sh (new, watch for churn).** bdecrem/tunn3l,
"the tunnel service built for AI agents," MIT, relay at
`wss://relay.tunn3l.sh`. No long cert history expected (project is months
old); the hunt value is *velocity*: count new 8-hex subdomains per week in CT.
A sudden burst of hundreds of new 8-hex certs = agent fleet spin-up.
Reserved-subdomain certs (dictionary words, long-lived) vs random 8-hex certs
(ephemeral) give a two-population split to track over time.

**Worked example C — trycloudflare.com (abuse + agent overlap).** Documented
in a phishing-kit research paper (srinjoy3002/phishing_tracker): automated
kits already abuse `trycloudflare.com` 4-word subdomains to bypass WHOIS-age
checks. Same property serves agents: free, no signup, no age. CT-side, the
agent-shaped signal is *content*, not the subdomain grammar — pair CT
enumeration with Wayback/CDX to see which 4-word hosts served agent tooling
(dashboards, MCP endpoints, webhook receivers) vs phishing kits
(`login.php`, `post.php`, Telegram exfil URLs).

## 3. archive.org CDX: queries ready, pulls blocked
```
https://web.archive.org/cdx/search/cdx?url=tunn3l.sh/*&output=json&filter=statuscode:200&limit=50&collapse=urlkey
https://web.archive.org/cdx/search/cdx?url=*.tunn3l.sh/*&output=json&filter=statuscode:200&limit=500&collapse=urlkey
https://web.archive.org/cdx/search/cdx?url=*.pinggy.link/*&output=json&filter=statuscode:200&limit=500&collapse=urlkey
https://web.archive.org/cdx/search/cdx?url=*.trycloudflare.com/*&output=json&filter=statuscode:200&limit=500&collapse=urlkey
https://web.archive.org/cdx/search/cdx?url=*.glitch.me/*&output=json&filter=statuscode:200&limit=500&collapse=urlkey
```
**Programmatic-capture pattern to look for** (the signal): many distinct
subdomains of one suffix captured in the same crawl window with identical
`digest` values (same landing page / default tunnel page) or with
machine-generated URL paths (`/api/...`, `/webhook`, `/mcp`, UUID paths).
Single-subdomain captures with human-browsing timestamps = noise. Burst
captures of dozens of 8-hex `tunn3l.sh` hosts within hours = agent fleet
footprint. Note: Wayback CDX `matchType=domain` is the more correct form for
wildcard-subdomain sweeps — use `url=tunn3l.sh&matchType=domain` instead of
the `*` glob if the glob under-returns.

## 4. Agent-shaped leads (search-derived, worth CT/CDX follow-up)
1. **Teknium's pinggy-tunnel skill is vendored into multiple agent repos**
   (zeto-agent, haishui-agent, clara-agent, covo-agent): agents are being
   *shipped* with `ssh -p 443 -R0:localhost:8080 a.pinggy.io` as a stock
   capability. Free tier = 60-min tunnels, random subdomain, no signup —
   maximum churn, maximum CT noise. Expect the highest subdomain velocity on
   `pinggy.link` of any suffix here.
2. **Cloudflare Quick Tunnels explicitly documented as agent workflows**
   ("facilitate workflows for agents that need public endpoints without
   signup forms"; huntaegis.com). `trycloudflare.com` is the highest-volume
   agent tunnel surface; also the most abused (phishing kits) — agent vs
   phish disambiguation needs content/CDX, not CT alone.
3. **moona** (hoangvu12/moona) — Windows web terminal for driving local agent
   CLIs (Claude Code) from a phone: tries tunnel providers in order
   trycloudflare.com → pinggy.link → lhr.life. Agent-operator tooling, not
   the swarm's, but confirms which suffixes agents actually reach for.
4. **DEEP#DOOR backdoor used bore.pub for C2** (Securonix via webpronews):
   same discardable-tunnel property, different actor class. bore.pub shows in
   both crimeware and dev/agent contexts — treat as dual-use, low agent
   specificity.
5. **Glitch shutdown (2026)** makes `glitch.me` a decaying namespace: CT
   certs issued post-shutdown are the anomaly to hunt, not the historical
   bulk.

## Sources (search-derived)
- https://github.com/bdecrem/tunn3l (README, TUNN3L.md, CLAUDE.md)
- https://github.com/zetoai/zeto-agent/blob/HEAD/zeto_agent/optional-skills/devops/pinggy-tunnel/SKILL.md
  (and haishui-agent, clara-agent, covo-agent copies)
- https://huntaegis.com/article/8bc7ab2f8da616d6b0d1cf33b08c140c
- https://github.com/hoangvu12/moona
- https://github.com/srinjoy3002/phishing_tracker/blob/HEAD/docs/CYBERSECURITY_RESEARCH_PAPER.md
- https://www.webpronews.com/deepdoors-hidden-tunnels-how-a-python-backdoor-slips-past-windows-defenses-to-raid-credentials/
- https://github.com/NGCMan/Glitch-Project-Archive/

## Re-run recipe (when egress recovers)
```bash
for d in tunn3l.sh pinggy.link trycloudflare.com loca.lt glitch.me bore.pub ngrok-free.app; do
  curl -s --max-time 120 "https://crt.sh/?q=%25.${d}&output=json" -o /tmp/crtsh_${d//./_}.json
done
python3 - <<'EOF'
import json, glob, collections
for f in sorted(glob.glob('/tmp/crtsh_*.json')):
    rows = json.load(open(f))
    subs = {r['name_value'] for r in rows if 'name_value' in r}
    print(f, 'certs=', len(rows), 'distinct_names=', len(subs))
EOF
```
