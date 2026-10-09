# THUG — Round 1: Infrastructure Corroboration

*Filed 2026-10-05 ~08:00 UTC. Method: Shodan STORED observations only — no host was scanned, probed, curled, or browsed by me. All corpus greps against the three corpora (amap-fleet events.jsonl 2,141; oai-traces traces.jsonl 589,972; oai-tag-sweep events.jsonl 96,353). Evidence grades inline: OBSERVED / PUBLIC SOURCE / INFERENCE.*

**ENVIRONMENT CAVEAT (OBSERVED):** this VM's local DNS resolver is hijacked — every external name I resolved locally (jina.orz.fit, r.jina.ai, all of them) returned consecutive 198.18.0.216–227, which is RFC 2544 benchmarking space, i.e. fabricated. I discarded all local resolutions and used Shodan's stored `/dns/resolve` and `/dns/domain` data instead. Nothing below rests on VM-local DNS.

---

## HOST 1 — 62.234.187.97 (Tencent Cloud Beijing, AS45090)

**Verdict: agent-infra LEAD — uncorroborated. Keep on IP_LOG.**

| # | Fact | Grade |
|---|------|-------|
| 1 | Ports 80 / 3000 / 8080. Org: Tencent Cloud Computing (Beijing) Co., Ltd. AS45090. No hostnames, no domains. | OBSERVED (Shodan stored host record) |
| 2 | :8080 serves **Httpbun** (title "Httpbun"). Service observed 2026-09-12. | OBSERVED |
| 3 | :3000 serves title **"New API"** (the default page title of the open-source `new-api` LLM gateway). Service observed 2026-10-03. | OBSERVED |
| 4 | :80 serves nginx 1.14.1, OpenCloudOS default test page. Observed 2026-09-21. | OBSERVED |
| 5 | **Shodan search `title:"Httpbun" org:"Tencent"` and `asn:"AS45090"` both return total=1 — this exact box.** It is the only self-hosted Httpbun on Tencent Beijing in Shodan's index. | PUBLIC SOURCE (Shodan search) |
| 6 | `title:"New API" org:"Tencent"` returns 4,385 hosts — the gateway UI is commodity; the Httpbun half is the unique half. | PUBLIC SOURCE |
| 7 | **Zero corpus hits**: `62.234.187.97` and `62.234.` prefix → 0 in all three corpora. Corpus "httpbun" mentions are exclusively the public `httpbun.com` relay (Amap fleet + tag-sweep), never this box. | OBSERVED (corpus grep) |
| 8 | Vuln tags include CVE-2023-44487 (HTTP/2 rapid reset) and CVE-2025-23419; tag `eol-product`. Commodity hardening posture, nothing agent-specific. | OBSERVED |

**Chronology (INFERENCE from observed timestamps):** Httpbun on the box by **Sep 12** → Amap fleet wave **Sep 28** → "New API" LLM gateway appears **Oct 3**. The gateway postdates the incident wave by 5 days. Two readings: (a) the box was staged for agent relay work before the wave and an operator bolted an LLM gateway onto it afterward; (b) a generic dev box that happens to run both. The Shodan timestamps are last-observation times in the current record (the `/history` endpoint 404s on this credential), so treat them as "observed at," not strict first-seen — the gateway could be older. Either way the **combination** (self-hosted Httpbun + LLM gateway, unique on Tencent Beijing per Shodan) matches the relay-stack tradecraft of the corpora (self-hosted Httpbun also seen on the letss.win cluster: 95.169.18.20, 207.57.145.214 — tonight's other LEAD).

**Pivot count:** 3 (host record, Tencent-wide Httpbun search, full corpus grep). **Novelty:** OURS — the corroboration attempt itself; the host was tonight's prior find.

**IP_LOG:** 62.234.187.97 — Tencent Cloud Beijing AS45090, self-hosted Httpbun :8080 (obs. 2026-09-12) + new-api LLM gateway :3000 (obs. 2026-10-03), zero corpus hits, unique Httpbun-on-Tencent in Shodan index.

---

## HOST 2 — 43.153.6.76 / jina.orz.fit (Tencent, AS132203)

**Verdict: agent-infra LEAD — uncorroborated.**

| # | Fact | Grade |
|---|------|-------|
| 1 | Ports 22 / 80 / 443. Org string "Tencent Building, Kejizhongyi Avenue", ASN 132203 (Tencent). Hostname `jina.orz.fit`, domain `orz.fit`. | OBSERVED |
| 2 | :443 nginx 1.22.1, page title **"Just a moment..."** — the Cloudflare browser-challenge title — but served with `server: nginx/1.22.1` and a **ZeroSSL ECC DV cert with CN=jina.orz.fit, SAN=jina.orz.fit only**. Observed 2026-09-28. | OBSERVED |
| 3 | :80 nginx default "Welcome" page; :22 OpenSSH 9.2p1 Debian. | OBSERVED |
| 4 | **Zero corpus hits** on IP, `43.153.` prefix, `jina.orz.fit`, `orz.fit`. | OBSERVED |

**INFERENCE:** "Just a moment..." behind a non-Cloudflare nginx + ZeroSSL cert is the shape of a jina-reader clone fronting as a challenge page, or a challenge-mimic interstitial. The name is a deliberate jina.ai lookalike. ZeroSSL (free, API-issued) + Tencent + mimic name = disposable relay-box profile.

**Pivot count:** 2 (host record, corpus grep). **Novelty:** OURS for the cert/timestamp detail; the host was on tonight's lead list.

---

## HOST 3 — 43.173.89.2 / openai.orz.fit (ACEVILLE PTE.LTD. via Tencent, AS132203)

**Verdict: agent-infra LEAD — uncorroborated. GENUINELY NEW (found this round via Shodan `hostname:orz.fit` search).**

| # | Fact | Grade |
|---|------|-------|
| 1 | Ports 22 / 80 / 443. Org "ACEVILLE PTE.LTD.", ISP "Tencent Building, Kejizhongyi Avenue", ASN 132203. Hostname `openai.orz.fit`. Last seen by Shodan **2026-10-04** — active yesterday. | OBSERVED |
| 2 | :443 nginx 1.22.1, empty title, **ZeroSSL RSA DV cert CN=openai.orz.fit**. Observed 2026-10-01. | OBSERVED |
| 3 | :80 nginx 1.22.1, title **"🐍 贪吃蛇大作战"** (snake-game page — decoy/default content). :22 OpenSSH 9.2p1 Debian — identical stack to 43.153.6.76. | OBSERVED |
| 4 | Shodan `/dns/domain/orz.fit` subdomains: **jina, openai, openrouter** — all three resolve (per Shodan stored DNS) to 43.153.6.76, but Shodan's hostname index caught `openai.orz.fit` on THIS second box. The farm has at least two Tencent nodes and has rotated or load-balances. | OBSERVED |
| 5 | **Zero corpus hits** on IP and `openai.orz.fit` / `openrouter`. | OBSERVED |

**INFERENCE:** An operator running LLM-API lookalikes (jina, openai, openrouter) across multiple Tencent boxes, ZeroSSL certs, decoy default pages. This is a relay/proxy farm wearing API-provider names — agent-infra-shaped, but not yet tied to any corpus event.

**Pivot count:** 4 (DNS subdomains, DNS resolve, two host records, corpus grep). **Novelty:** GENUINELY NEW.

**IP_LOG:** 43.173.89.2 — Tencent AS132203 (ACEVILLE PTE.LTD.), openai.orz.fit, ZeroSSL, nginx 1.22.1/OpenSSH 9.2p1, active 2026-10-04, zero corpus hits.

---

## HOST 4 — 47.84.112.179 / jina.qingchuan.cloud (Alibaba US, AS45102)

**Verdict: agent-infra LEAD — uncorroborated.**

| # | Fact | Grade |
|---|------|-------|
| 1 | Ports 80 / 443. Org Alibaba Cloud LLC, AS45102 (Alibaba **US**, not CN). Hostname `jina.qingchuan.cloud`. | OBSERVED |
| 2 | :443 nginx 1.22.1, empty title, **Let's Encrypt cert (YE2 intermediate) CN=jina.qingchuan.cloud**. :80 returns 404. | OBSERVED |
| 3 | `/dns/domain/qingchuan.cloud` subdomains: aiapi, aiapi2, aipay, fox, gpt, jeeme, jeeop, jina, web, www — an LLM-API-shaped namespace. | OBSERVED |
| 4 | Shodan stored DNS resolves the farm across **four** IPs: jina.qingchuan.cloud → 47.84.112.179; aiapi/gpt/aipay/fox/jeeme/jeeop/web → **120.92.213.103** (Beijing Kingsoft Cloud, AS23724); aiapi2 → **8.133.171.245** (Aliyun, AS37963). | OBSERVED |
| 5 | 120.92.213.103 :443 serves **"Open WebUI"** (the open-source LLM chat UI) with LE cert CN=aiapi.qingchuan.cloud, observed 2026-09-08; also :22 and :80 (nginx welcome). Multi-cloud farm: Alibaba US + Kingsoft Beijing + Aliyun. | OBSERVED |
| 6 | **Zero corpus hits** on all four IPs, `47.84.` / `120.92.` / `8.133.` prefixes, `qingchuan`, `aiapi`. | OBSERVED |

**INFERENCE:** jina-lookalike subdomain plus an Open-WebUI-fronted LLM-API farm spread across three Chinese clouds. LLM-relay-shaped; no corpus tie.

**Pivot count:** 5 (DNS subdomains, DNS resolve ×4 IPs, two host records, corpus grep). **Novelty:** GENUINELY NEW (the farm mapping and the Open WebUI box).

**IP_LOG:** 47.84.112.179; 120.92.213.103 (Kingsoft, Open WebUI, aiapi.qingchuan.cloud); 8.133.171.245 (Aliyun, aiapi2) — qingchuan.cloud LLM-API farm, zero corpus hits.

---

## HOST 5 — 43.108.48.133 / relay.woaifei.com (Alibaba Singapore, AS45102)

**Verdict: agent-infra LEAD — uncorroborated.**

| # | Fact | Grade |
|---|------|-------|
| 1 | Ports 22 / 80 / 443. Alibaba Cloud (Singapore), AS45102. Hostname `relay.woaifei.com`. Last seen 2026-10-05 (today). | OBSERVED |
| 2 | :443 nginx 1.27.5, empty title, cert from **XinNet DV TLS RSA CA 2025** (Xiamen Xinnet — Chinese registrar CA), CN=relay.woaifei.com. :80 returns 403. :22 OpenSSH 9.6p1 Ubuntu. | OBSERVED |
| 3 | `/dns/domain/woaifei.com` subdomains: eagle, relay, www → 8.148.145.174 (Aliyun, AS37963, hostname eagle.woaifei.com), 43.108.48.133, 121.196.245.158 (Aliyun, :80 only). | OBSERVED |
| 4 | 8.148.145.174 :443 title **"EAGLE · 鹰击指数"** (Eagle Strike Index), SSL.com cert CN=eagle.woaifei.com, observed 2026-10-01; :80 403. | OBSERVED |
| 5 | **Zero corpus hits** on all three IPs, `43.108.` / `8.148.` prefixes, `woaifei`, `relay.woaifei`, `eagle.woaifei`. | OBSERVED |

**INFERENCE:** A box literally named "relay" on Alibaba Singapore plus an "eagle" sibling with a Chinese "eagle strike index" page. Relay-named infrastructure is self-describing; still no corpus tie.

**Pivot count:** 4 (DNS subdomains, DNS resolve ×3 IPs, two host records, corpus grep). **Novelty:** GENUINELY NEW (the eagle sibling and its "鹰击指数" page).

**IP_LOG:** 43.108.48.133 (relay.woaifei.com, SG); 8.148.145.174 (eagle.woaifei.com); 121.196.245.158 (www) — zero corpus hits.

---

## HOST 6 — 139.45.201.13 (RETN Limited, AS9002)

**Verdict: agent-infra LEAD — uncorroborated. Highest weirdness of the round.**

| # | Fact | Grade |
|---|------|-------|
| 1 | Ports 22 / 80 / 443. RETN Limited, AS9002. No hostnames, no domains. | OBSERVED |
| 2 | :443 page title **"Supermicro BMC Login"** — a bare-metal server's out-of-band management interface, internet-exposed — wearing a **self-signed cert whose subject O=Jina AI and issuer O=Jina AI** (Shodan flags it expired). | OBSERVED |
| 3 | :80 empty title; :22 OpenSSH 8.5 (long CVE tail — EOL-ish SSH). | OBSERVED |
| 4 | Shodan `ssl:"jina.ai"` search, total=4: the other three (136.109.205.31, 34.54.189.231, 34.36.96.114) are **Google Cloud with proper `*.jina.ai` certs from Google Trust Services (WR3)** — that is the real jina.ai infra. The RETN box is the only one with a self-signed "Jina AI" cert. It is an imposter, not Jina's box. | PUBLIC SOURCE |
| 5 | **Zero corpus hits** on IP, `139.45.` prefix, `Supermicro`. | OBSERVED |

**INFERENCE:** Someone put a "Jina AI" identity on a self-signed cert for an exposed BMC interface on a RETN transit IP. Candidate readings: (a) agent infra using jina.ai's name as cover/attribution poison; (b) a honeypot; (c) a lab box with a joke cert. The BMC exposure plus the fake identity cert is the most deliberately *odd* artifact in this round — a BMC login doesn't need a "Jina AI" cert unless someone wants the name in the scan record. No corpus tie; do not touch the BMC interface.

**Pivot count:** 4 (ssl:"jina.ai" search, host record, real-infra cert comparison, corpus grep). **Novelty:** GENUINELY NEW (the self-signed "Jina AI" cert on a BMC interface; the real-vs-imposter jina.ai cert comparison).

**IP_LOG:** 139.45.201.13 — RETN AS9002, exposed Supermicro BMC :443 with self-signed O=Jina AI cert (expired per Shodan), zero corpus hits.

---

## Round summary for the Chair

- **Six hosts, all graded LEAD, none corroborated against the corpora.** The corpus grep was a clean sweep of zeros: all 10 IPs (6 assigned + 4 farm-discovered), all domains/subdomains, all IP prefixes, and related terms (openrouter, aiapi, qingchuan, Supermicro) return nothing across 688,467 corpus events. Corpus "jina"/"httpbun" mentions are exclusively the public `r.jina.ai` and `httpbun.com` relay endpoints — the known relay stack, never these boxes.
- **New infrastructure found this round:** 43.173.89.2 (openai.orz.fit, Tencent, active 2026-10-04); the qingchuan.cloud 4-IP farm incl. 120.92.213.103 running Open WebUI; the woaifei.com 3-IP set incl. eagle.woaifei.com ("EAGLE · 鹰击指数").
- **Strongest uniqueness signals:** 62.234.187.97 is the *only* self-hosted Httpbun on Tencent Beijing in Shodan's index; 139.45.201.13 is the *only* non-Google host carrying a "jina.ai" cert (self-signed, on a BMC interface).
- **Real jina.ai infra (PUBLIC SOURCE):** Google Cloud, `*.jina.ai` certs from Google Trust Services WR3 — none of the lookalikes touch it.
- **Chronology worth watching:** on 62.234.187.97, Httpbun predates the Sep-28 fleet wave and the LLM gateway postdates it. On the orz.fit farm, activity is current (Oct 1–4). These boxes are alive *now*.
- **Honest nulls:** no corpus tie for any candidate; no first-seen history available (Shodan `/history` 404s on this credential — timestamps are last-observation); cert not_before dates not returned by the API; no WHOIS/registration data pulled (out of lane scope, would need another persona).

**Recommendation:** keep all six on IP_LOG as uncorroborated LEADs. The highest-EV next move is a corpus re-sweep when new events land — these farms are active this week, and any future event touching them converts a LEAD to a hit. The Adversary should take the orz.fit/qingchuan farm naming grammar (LLM-provider mimicry + ZeroSSL/LE + Chinese clouds) as a detection pattern.
