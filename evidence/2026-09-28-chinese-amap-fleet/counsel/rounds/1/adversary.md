# ADVERSARY — Round 1 Red Team
*Chair: Hunter S. Thompson. The wall every finding must climb. No mercy, no hand-waving. Every kill is evidenced; every surviving claim is graded.*
*Filed 2026-10-05 ~08:00 UTC. Scope: agents and infrastructure only.*

**Evidence grades:** OBSERVED = I saw/computed it this session · PUBLIC SOURCE = web-indexed · INFERENCE = my reasoning from the above.

**Corpus baseline used for all "zero hits" claims (OBSERVED):** grep across `data/2026-09-28-chinese-amap-fleet/events.jsonl` (2,141 events), `openai-agent-traces/data/traces.jsonl` (589,972 events), `data/2026-10-01-oai-tag-sweep/events.jsonl` (96,353 events) — ~688k events total.

---

## TARGET 1 — letss.win self-hosted Httpbun cluster (95.169.18.20, 207.57.145.214)

**Steelman.** Two IPs on two ASNs (AS25820 Cluster Logic/IT7, AS1054 NTT/Zont) both serving the Httpbun title on :8443 under the hostname letss.win, one with an "Ncat http proxy" on :2083. Found independently by two personas via Shodan `http.html:"httpbun"`. Self-hosted httpbun + bespoke proxy + no web presence = someone's private relay stack. Agents in our corpora live on httpbun as a relay; a private instance dodges the public httpbun.com's logging/rate limits. Smells like operator infra.

**The attack.**
1. **Self-hosting httpbun is the documented norm, not tradecraft.** The project's own README (sharat87/httpbun): "Run your own with: `docker run -p 80:80 sharat87/httpbun`" (PUBLIC SOURCE). Running it on a VPS is what the author tells you to do.
2. **Zero agent linkage across ~688k events.** letss.win, both IPs, and 16clouds.com: zero hits in all three corpora (OBSERVED). No urlquery co-occurrence either — this lead was born in Shodan, not in agent traffic.
3. **The base rate is "random devs."** Shodan indexes exactly 7 `http.html:"httpbun"` hosts worldwide (OBSERVED). The other 5: a DigitalOcean box with no hostname, a Google Cloud box on :11000, etc. — scattered personal dev boxes. letss.win is 2 of 7, distinguished only by a shared domain and the Ncat proxy.
4. **The Ncat proxy points HUMAN, not agent.** Ncat is nmap's netcat — a pentester's/hacker's tool, not anything in our agent corpora. Agents here use public relays (r.jina.ai, allorigins, corsproxy.io, md.succ.ai); no agent in 688k events has ever touched a bespoke Ncat proxy (OBSERVED + INFERENCE). An Ncat proxy on :2083 (cPanel's HTTPS port — blends with admin-panel traffic) is human-opsec-shaped: a hacker's personal relay or a researcher's box.
5. **"Found independently by two personas" is corroboration of existence, not of the agent hypothesis.** Both personas ran the same Shodan query and got the same two hosts. That verifies the Shodan observation; it adds zero bits to "agents use this."

**VERDICT: WOUNDED.** Downgraded from "agent-infra LEAD" to **unattributed infra oddity**. The agent-linkage is dead — zero evidence, strong benign alternatives (dev's toolbox, pentester's relay, possible honeypot). What survives on the watchlist: a dual-ASN self-hosted httpbun with an Ncat proxy and no web presence is genuinely unusual enough to keep; it upgrades ONLY on future corpus/urlquery co-occurrence with agent traffic. Do not cite as agent-linked.

---

## TARGET 2 — Tencent Beijing 62.234.187.97 (self-hosted Httpbun + LLM gateway)

**Steelman.** Tencent Cloud Beijing box, no hostname: :80 nginx default test page, :3000 "New API" (LLM gateway), :8080 Httpbun. An LLM gateway co-located with an HTTP-testing relay on Chinese cloud infra — that's an agent operator's workbench: proxy model access through the gateway, test exfil against the local httpbun. Zero corpus hits just means it's fresh/undiscovered.

**The attack.**
1. **"New API" is a 48k-star open-source project with one-click deploys.** QuantumNous/new-api — self-hosted LLM gateway, Docker/Railway templates, partnerships with Alibaba Cloud and Peking University (PUBLIC SOURCE). Finding one on Tencent Cloud in Beijing is like finding WordPress on a VPS — it is where Chinese devs host, and this is what Chinese devs run.
2. **The pairing is the most natural dev stack in the world.** An LLM gateway + httpbun on one box = "I proxy my model calls and test my webhooks." No conspiracy required (INFERENCE).
3. **The box looks like a stale personal VPS, not an op.** nginx default OpenCloudOS test page on :80, `eol-product` tag, a pile of old nginx CVEs (CVE-2023-44487, CVE-2019-9516, etc.) per Shodan (OBSERVED). Operators running live agent infra don't leave the nginx welcome page up; devs who spun up a VPS and forgot it do.
4. **Zero linkage, and "zero corpus hits" is not evidence of freshness — it's absence of evidence, full stop.** No hostname, no cert history chased (crt.sh was down, but nothing else points at it), no urlquery co-occurrence, no agent grammar anywhere near it (OBSERVED).
5. The steelman requires believing an agent operator colocates their gateway AND their testing relay on one unhardened box with a default nginx page. Real operators separate concerns; this is a hobbyist's server (INFERENCE).

**VERDICT: KILLED.** Nothing agent-shaped survives. It is a personal dev VPS running two popular open-source projects. Remove from the lead board; keep the IP in the generic infra log at most.

---

## TARGET 3 — jina-reader lookalikes (jina.orz.fit, jina.qingchuan.cloud, relay.woaifei.com)

**Steelman.** Three hosts found via Shodan page-hits for r.jina.ai, with hostnames literally "jina"/"relay", on Tencent/Alibaba ASNs, Cloudflare-challenged :443, nginx elsewhere. r.jina.ai keyless is dead; agents need reader relays; someone is standing up lookalike reader mirrors on Chinese cloud. Agent USE unproven but the shape is right.

**The attack.**
1. **Zero corpus hits — and we know what agent reader traffic looks like.** In the 96k-event tag-sweep corpus, every jina-reader URL agents touch is an official or public-proxy endpoint: r.jina.ai (3,233), s.jina.ai (15), r.jina-ai.workers.dev (6), r-jina-ai.translate.goog (6) (OBSERVED). **Not one** bespoke self-hosted mirror appears in agent traffic. If agents used private reader mirrors, 96k events of relay traffic would show at least one. The lookalikes have zero hits across all ~688k events (OBSERVED).
2. **Shodan DNS shows these are personal AI-dev domains, not agent infra.** orz.fit subdomains: jina, openai, openrouter. qingchuan.cloud: aiapi, aiapi2, aipay, fox, gpt, jina, web, www. woaifei.com: eagle, relay, www (+spf) (OBSERVED via Shodan DNS). Translation: individuals running personal AI API relays — the "jina" subdomain sits next to "openai" and "openrouter" subdomains. That's a dev self-hosting reader to dodge r.jina.ai's death/rate-limits, exactly what any of us would do.
3. **jina-reader is open source; self-hosting is documented and common.** Same logic as Target 1 — the README-driven norm, not tradecraft (PUBLIC SOURCE, by the same token as httpbun).
4. **The "Shodan page hit for r.jina.ai" pivot is weak.** A page merely *referencing* r.jina.ai (docs, a landing page, SEO copy, a parked domain stuffed with AI keywords) triggers it. Two pivots where one is "hostname contains jina" and the other is "page mentions jina" is barely one pivot wearing a trenchcoat (INFERENCE).
5. Legit-mirror and SEO-spam hypotheses both fit better than the agent hypothesis: a Cloudflare-challenged :443 + nginx + AI-keyword subdomains is precisely what a personal gateway or a keyword-squat looks like; nothing in the observations distinguishes them from agent infra except the *absence* of agent traffic — which is the dog that didn't bark (INFERENCE).

**VERDICT: KILLED as agent infra.** The agent-use hypothesis has no supporting evidence and one strong contrary (agents demonstrably use only official/public reader endpoints). Surviving residue, already the cert-sleuth's position: keep the three domains on the corpus co-occurrence watchlist — they upgrade only if agent traffic ever touches them. Do not present as leads.

---

## TARGET 4 — `?r=<19-digit>` nonce family (shared `178207` prefix, 13 days apart)

**Steelman.** Two webhook.site inboxes, scanned 2026-06-24 and 2026-07-07, both carrying `?r=` params with 19-digit values sharing the prefix `178207`: `1782071176301141190` and `1782070800983511679`. 19-digit shared-prefix nonces 13 days apart = same operator's nonce grammar, a deliberate family marker.

**The attack.**
1. **They are nanosecond wall-clock timestamps, and they are 6 minutes apart — not 13 days.** `1782071176301141190` → 2026-06-21 19:46:16 UTC; `1782070800983511679` → 2026-06-21 19:40:00 UTC (OBSERVED, computed via `date -d`). Delta: 375,317,629,511 ns ≈ 6.25 minutes.
2. **The shared `178207` prefix is an artifact of temporal proximity, not a signature.** Any two nanosecond timestamps 6 minutes apart share their first ~15 digits. The "family marker" is what time looks like (INFERENCE from OBSERVED). This is the central kill: the prefix-sharing carries zero operator information beyond "generated minutes apart."
3. **`?r=` is the universal cache-buster parameter** (`r` = random) — environmental convention, not operator grammar (PUBLIC SOURCE, general web knowledge). Nobody's toolkit "grammar" is `?r=`; it's what you append to defeat caching.
4. **Both timestamps predate both urlquery scans by days** (June 21 vs June 24 / July 7 scans) (OBSERVED). So the `?r=` values were baked into the URLs at construction, in a single ~6-minute June-21 session, and the URLs were submitted to urlquery days later. The most economical reading: a human set up/checked two inboxes in one session — one inbox is even noted "codebreaker-known (legacy)" — and scanned the URLs later. Cache-busting an inbox URL to force a fresh urlquery scan (urlquery dedups identical URLs) is human-shaped behavior, not agent-shaped. Agents in our corpora don't append cache-busters to inbox URLs; they use `zz=oai<epoch+random>`, `uqscan=<tagword>` grammars (OBSERVED).
5. No corpus hits for the `?r=<19-digit>` pattern as an agent marker (OBSERVED).

**VERDICT: KILLED.** There is no nonce family and no operator signature — there are two cache-buster timestamps from one June-21 session, and the "shared prefix" is chronology wearing a costume. The only surviving residue is the weak session-linkage observation ("both inbox URLs likely constructed within ~6 minutes on 2026-06-21"), which is human-consistent and is not agent grammar. Downgrade to a footnote.

---

## TARGET 5 — `/xss-osint-insert` double-submit

**Steelman.** `webhook.site/2ab7ca12-fdce-4475-8bf0-950c0cbf28f2/xss-osint-insert` scanned twice in the same minute (2026-08-08T12:25Z) under two report IDs. Double submission at machine cadence = someone's OSINT harness exfil target being hit programmatically. Explicit "xss-osint" path label.

**The attack.**
1. **The writeup's facts are wrong.** Primary urlquery API data (OBSERVED): report `fe637b8f-8a6f-4647-89cd-b20867c9ba67` = **2026-07-31T12:32:29Z**; report `c6ee72ff-86fa-4a49-83b4-7906bdb721a5` = **2026-07-31T12:19:33Z**. Not the same minute, not 2026-08-08. Thirteen minutes apart. The "same minute" claim does not survive contact with the API.
2. **Layer confusion: two urlquery *scans* ≠ two webhook *submissions*.** Both reports show the identical submitted URL, identical scanner settings (Firefox 134 — urlquery's default scanner UA), same exit node `qguvgzjxzsgb3vs` (OBSERVED). The full report shows 5 HTTP GETs (inbox page + assets), `alert_count: 0`, and **zero captured webhook requests** — there is no evidence anyone ever POSTed to `/xss-osint-insert` at all. The "double-submit" happened at the urlquery layer: one human scanned the same inbox URL twice, 13 minutes apart. That is re-scan behavior (check the inbox, wait, check again), not machine exfil cadence.
3. **The path name is human-shaped — and the same writeup proves it.** `xss-osint-insert` is descriptive English. The same author's SHAPE-6 (beeceptor `/leak`, `/grabber.php`, keyboard-mash subdomains) was graded HUMAN-KIT-SHAPED. A literate English label like "xss-osint-insert" is *more* human than keyboard mash, not less. The writeup applies "machine cadence" to the human-readable one and "human kit" to the machine-readable ones — backwards (INFERENCE).
4. Zero corpus hits (OBSERVED).

**VERDICT: KILLED.** As an agent finding it is dead on three independent grounds: false timestamps, scan-layer/submission-layer confusion, and a human-shaped label. What it actually is: a human OSINT tester's webhook.site inbox link, scanned twice on urlquery 13 minutes apart. File under human kit, not agents.

---

## Scoreboard

| # | Target | Verdict | What survives |
|---|---|---|---|
| 1 | letss.win Httpbun cluster | **WOUNDED** | Unattributed infra oddity on watchlist; agent-linkage dead |
| 2 | Tencent 62.234.187.97 | **KILLED** | Nothing. Personal dev VPS, two open-source projects |
| 3 | jina-reader lookalikes | **KILLED** | Watchlist-only; agents provably use official reader endpoints only |
| 4 | `?r=` nonce family | **KILLED** | Footnote: two cache-busters from one June-21 session (human-shaped) |
| 5 | `/xss-osint-insert` double-submit | **KILLED** | Nothing agent-side; human re-scan of an OSINT tester's inbox |

**Corrections to the record (for the Chair):** the dead-drop-diver writeup's `/xss-osint-insert` metadata is factually wrong (dates/times) — the "same minute 2026-08-08" claim is contradicted by the urlquery API's own `date` fields (2026-07-31T12:19:33Z / 12:32:29Z). Recommend amending FINDINGS.md. The `?r=` "13 days apart" framing is also misleading: the nonces are 6 minutes apart; the 13 days is scan spacing.

**Method note:** all kills above rest on primary pulls (urlquery API overviews + full report for both xss-osint-insert scans; Shodan host/DNS/count this session; greps across ~688k corpus events) and public documentation (httpbun README, New API project pages). No URLs were fetched or probed; no candidate links were opened.
