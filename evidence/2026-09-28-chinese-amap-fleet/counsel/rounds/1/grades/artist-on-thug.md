# ARTIST'S GRADES — on THUG, Round 1

*Chair: Hunter S. Thompson. I judge composition: what carries weight, what's decorative, what the underdrawing can't support. The Thug brought six canvases, all honest about being sketches. Harsh but fair.*

**One convention correction before the findings:** the Thug grades Shodan-stored records as OBSERVED. They are not. The Thug touched no host — by his own honest admission, no host was scanned, probed, curled, or browsed. Shodan's stored observations are **PUBLIC SOURCE** (third-party, stored, subject to index staleness). The corpus greps are genuinely OBSERVED (his own bytes). I re-grade the evidence column accordingly throughout. This wounds no finding — it just moves the frame.

---

## HOST 1 — 62.234.187.97 (Tencent Beijing, AS45090)

**Finding T1a — Host identity: Tencent Cloud Beijing, AS45090, ports 80/3000/8080, no hostnames, no domains**
- **Novelty:** OURS (prior find; tonight's corroboration).
- **Evidence:** PUBLIC SOURCE (Shodan stored host record).
- **Actionability:** None beyond the log entry.
- **Verdict: KEEP.** Clean identity bytes, honestly sourced. The no-hostname/no-domain negative is as load-bearing as the ports.

**Finding T1b — :8080 serves Httpbun, observed 2026-09-12**
- **Novelty:** OURS.
- **Evidence:** PUBLIC SOURCE.
- **Actionability:** None (passive only — no touching).
- **Verdict: KEEP.** The Httpbun half is the half that matters; everything downstream leans on it.

**Finding T1c — :3000 title "New API" identified as the open-source `new-api` LLM gateway**
- **Novelty:** OURS.
- **Evidence:** PUBLIC SOURCE (the title) / INFERENCE (the product identification).
- **Actionability:** Yes — confirm passively via Shodan's stored HTTP data: favicon hash, known `new-api` asset paths, `/api/` response headers. No new scanning, no touching the box.
- **Verdict: WOUNDED.** A generic two-word title is a thin brushstroke to hang a product identification on — and the Thug's own Finding T1e (4,385 hosts share that title) is the wound's depth gauge. The gateway half of the "unique combination" claim is the weaker half. It keeps as a lead, not as an identification.

**Finding T1d — Only self-hosted Httpbun on Tencent Beijing in Shodan's index (both searches total=1)**
- **Novelty:** OURS.
- **Evidence:** PUBLIC SOURCE.
- **Actionability:** Re-run the search periodically; a second Httpbun on Tencent would deflate it.
- **Verdict: KEEP.** The strongest line on this host — a measured uniqueness, honestly scoped to Shodan's index. The Thug said "in Shodan's index," which is the load-bearing qualifier; without it this would be an overclaim.

**Finding T1e — "New API" title is commodity (4,385 hosts)**
- **Novelty:** — (counterweight, not a find).
- **Evidence:** PUBLIC SOURCE.
- **Actionability:** None.
- **Verdict: KEEP.** This is the Thug grading himself mid-report. The gateway half is commodity; the Httpbun half is unique. Honest negative space, and it sharpens T1d.

**Finding T1f — Zero corpus hits (IP, prefix, "httpbun" mentions are only the public relay)**
- **Novelty:** OURS.
- **Evidence:** OBSERVED (own grep across all three corpora, 688,467 events).
- **Actionability:** None now; this is the tripwire — any future corpus event touching this box converts the lead.
- **Verdict: KEEP.** A clean, honest null. The distinction that corpus "httpbun" = public `httpbun.com` only is exactly the right control.

**Finding T1g — Vuln tags commodity (CVE-2023-44487, CVE-2025-23419, eol-product)**
- **Novelty:** —.
- **Evidence:** PUBLIC SOURCE.
- **Actionability:** None.
- **Verdict: KEEP.** Decorative, and the Thug knows it — filed as color, not as signal. Fine.

**Finding T1h — Chronology: Httpbun (Sep 12) → fleet wave (Sep 28) → gateway (Oct 3); "bolted on afterward" vs "generic dev box"**
- **Novelty:** — (inference over own data).
- **Evidence:** INFERENCE, on last-observation timestamps.
- **Actionability:** None — `/history` 404s on this credential, so the ordering can't be hardened from here.
- **Verdict: WOUNDED.** The Thug caves the wound himself (timestamps are last-observation, not first-seen; the gateway could be older), which saves it from a KILL — but the "postdates the wave by 5 days" narrative still walks on one leg. The shape argument (Httpbun + gateway = relay-stack tradecraft) survives without the chronology; the chronology does not survive without first-seen data. Keep the shape, bleed the timeline.

**Host verdict: "agent-infra LEAD — uncorroborated."**
- **Verdict: KEEP.** The label is exactly as strong as the evidence and no stronger. The letss.win parallel (self-hosted Httpbun on 95.169.18.20 / 207.57.145.214) is the right prior to lean the shape against.

---

## HOST 2 — 43.153.6.76 / jina.orz.fit (Tencent, AS132203)

**Finding T2a — Identity: ports 22/80/443, Tencent, hostname `jina.orz.fit`**
- **Novelty:** OURS (tonight's lead list).
- **Evidence:** PUBLIC SOURCE.
- **Actionability:** None.
- **Verdict: KEEP.**

**Finding T2b — "Just a moment..." (Cloudflare challenge title) behind nginx/1.22.1 + ZeroSSL ECC DV cert, observed 2026-09-28**
- **Novelty:** OURS.
- **Evidence:** PUBLIC SOURCE.
- **Actionability:** Passive cert-transparency watch for new `orz.fit` subdomains (Adversary or a CT-capable lane).
- **Verdict: KEEP.** A genuine anomaly in three strokes: challenge title, no Cloudflare, free cert. The mimic-name profile (`jina.orz.fit`) is doing real work here.

**Finding T2c — Zero corpus hits (IP, prefix, both domains)**
- **Novelty:** OURS.
- **Evidence:** OBSERVED.
- **Actionability:** Tripwire, same as T1f.
- **Verdict: KEEP.**

**Finding T2d — INFERENCE: "jina-reader clone fronting as a challenge page, or a challenge-mimic interstitial"**
- **Novelty:** —.
- **Evidence:** INFERENCE.
- **Actionability:** Yes — body/asset comparison against the real jina reader to test the "clone" disjunct (browser-capable persona; read-only).
- **Verdict: WOUNDED.** The disjunction smuggles a strong claim past a weak one. "Challenge-mimic interstitial" is earned by the bytes. "Jina-reader clone" is not — nothing in the record shows reader behavior, proxied content, or API surface; a parked domain or a generic Cloudflare-mimic kit wears the same clothes. The mimic *name* suggests jina-adjacency; the *bytes* don't show a clone. Keep the interstitial, bleed the clone.

---

## HOST 3 — 43.173.89.2 / openai.orz.fit (ACEVILLE via Tencent, AS132203)

**Finding T3a — Identity + last seen 2026-10-04 (active yesterday)**
- **Novelty:** GENUINELY NEW (found this round via `hostname:orz.fit`).
- **Evidence:** PUBLIC SOURCE.
- **Actionability:** None.
- **Verdict: KEEP.** A real find: the search that produced it is documented and reproducible.

**Finding T3b — :443 empty title, ZeroSSL RSA DV cert CN=openai.orz.fit, observed 2026-10-01**
- **Novelty:** GENUINELY NEW.
- **Evidence:** PUBLIC SOURCE.
- **Actionability:** None.
- **Verdict: KEEP.** Second verse of the orz.fit grammar: provider-mimic name + free cert + nginx.

**Finding T3c — :80 snake-game decoy page (🐍 贪吃蛇大作战); stack identical to 43.153.6.76 (nginx 1.22.1 / OpenSSH 9.2p1 Debian)**
- **Novelty:** GENUINELY NEW.
- **Evidence:** PUBLIC SOURCE.
- **Actionability:** None.
- **Verdict: KEEP.** The identical-stack observation is the quiet load-bearer: two boxes, same image, same operator hand. The decoy page is color with a purpose — default-content camouflage is part of the farm's grammar.

**Finding T3d — Farm mapping: subdomains jina/openai/openrouter resolve to 43.153.6.76, but the hostname index caught `openai.orz.fit` on this second box — "at least two Tencent nodes, rotated or load-balances"**
- **Novelty:** GENUINELY NEW.
- **Evidence:** PUBLIC SOURCE (the multi-node fact) / INFERENCE (the rotation/load-balance mechanism).
- **Actionability:** Re-check the resolution over time; a flip between .76 and .89.2 would harden the rotation reading.
- **Verdict: KEEP.** The farm-exists-on-two-boxes fact is solid and it's the round's best structural find. The "rotated or load-balances" gloss has a live rival — stale Shodan index vs. fresh DNS — and the Thug names rotation without quite naming staleness. The gloss is decorative; the two-node fact is structural. Keep the fact, note the rival.

**Finding T3e — Zero corpus hits**
- **Novelty:** OURS.
- **Evidence:** OBSERVED.
- **Actionability:** Tripwire.
- **Verdict: KEEP.**

**Finding T3f — INFERENCE: operator running LLM-API lookalikes across multiple Tencent boxes; "relay/proxy farm wearing API-provider names — agent-infra-shaped, but not yet tied to any corpus event"**
- **Novelty:** —.
- **Evidence:** INFERENCE.
- **Actionability:** Yes — the Adversary (or a browser persona, read-only) should test the rival hypothesis: this grammar — mimic subdomains + ZeroSSL/LE + nginx + decoy pages + Open WebUI/new-api — is also the exact uniform of China's gray-market LLM API resale ecosystem (中转站 resellers). Discriminator: reseller pricing pages, `/v1/models` listings, or top-up/payment flows would mark resale; their absence (plus relay-shaped behavior) would keep the agent-infra reading alive.
- **Verdict: KEEP.** Honestly labeled, honestly bounded ("not yet tied to any corpus event"). The artist's only amendment is naming the rival the Thug left unnamed — a farm shaped like this needs the resale ecosystem ruled out before it gets to wear "agent-infra" unqualified.

---

## HOST 4 — 47.84.112.179 / jina.qingchuan.cloud (Alibaba US, AS45102)

**Finding T4a — Identity: Alibaba Cloud LLC, AS45102 (US, not CN), hostname `jina.qingchuan.cloud`**
- **Novelty:** GENUINELY NEW.
- **Evidence:** PUBLIC SOURCE.
- **Actionability:** None.
- **Verdict: KEEP.** The US-ASN wrinkle is worth its ink — a Chinese-cloud farm that isn't all in China.

**Finding T4b — :443 nginx, empty title, Let's Encrypt cert CN=jina.qingchuan.cloud; :80 404**
- **Novelty:** GENUINELY NEW.
- **Evidence:** PUBLIC SOURCE.
- **Actionability:** None.
- **Verdict: KEEP.**

**Finding T4c — LLM-API-shaped namespace: aiapi, aiapi2, aipay, fox, gpt, jeeme, jeeop, jina, web, www**
- **Novelty:** GENUINELY NEW.
- **Evidence:** PUBLIC SOURCE (`/dns/domain/qingchuan.cloud`).
- **Actionability:** CT watch for new subdomains in this namespace.
- **Verdict: KEEP.** A namespace is a signature. `aiapi`/`aipay`/`gpt`/`jina` in one zone is not an accident of naming.

**Finding T4d — Four-IP multi-cloud mapping: 47.84.112.179 (Alibaba US), 120.92.213.103 (Kingsoft Beijing), 8.133.171.245 (Aliyun)**
- **Novelty:** GENUINELY NEW.
- **Evidence:** PUBLIC SOURCE.
- **Actionability:** None beyond the log.
- **Verdict: KEEP.** The round's best piece of cartography. Three Chinese clouds plus one US ASN, one zone.

**Finding T4e — 120.92.213.103 serves "Open WebUI" with LE cert CN=aiapi.qingchuan.cloud, observed 2026-09-08**
- **Novelty:** GENUINELY NEW.
- **Evidence:** PUBLIC SOURCE (title) / light INFERENCE (title→product — but "Open WebUI" is a distinctive title, unlike "New API"; the identification holds its weight).
- **Actionability:** None.
- **Verdict: KEEP.** This is the box that makes the farm legible: Open WebUI fronting an `aiapi` subdomain is an LLM-serving stack, not a parked domain.

**Finding T4f — Zero corpus hits (all four IPs, prefixes, qingchuan, aiapi)**
- **Novelty:** OURS.
- **Evidence:** OBSERVED.
- **Actionability:** Tripwire.
- **Verdict: KEEP.**

**Finding T4g — INFERENCE: "jina-lookalike subdomain plus an Open-WebUI-fronted LLM-API farm spread across three Chinese clouds. LLM-relay-shaped; no corpus tie."**
- **Novelty:** —.
- **Evidence:** INFERENCE.
- **Actionability:** Same discriminator as T3f — check for reseller pricing/API-docs surfaces (read-only) before the "agent-infra" label hardens.
- **Verdict: KEEP.** The most evidence-backed inference in the round — the Open WebUI box turns "shaped like" from a guess into a reading. Same rival-hypothesis note as T3f, and it's a note, not a wound.

---

## HOST 5 — 43.108.48.133 / relay.woaifei.com (Alibaba Singapore, AS45102)

**Finding T5a — Identity: Alibaba SG, AS45102, hostname `relay.woaifei.com`, last seen today (2026-10-05)**
- **Novelty:** GENUINELY NEW.
- **Evidence:** PUBLIC SOURCE.
- **Actionability:** None.
- **Verdict: KEEP.** Alive today is worth logging.

**Finding T5b — :443 nginx 1.27.5, XinNet DV cert, :80 403, OpenSSH 9.6p1**
- **Novelty:** GENUINELY NEW.
- **Evidence:** PUBLIC SOURCE.
- **Actionability:** None.
- **Verdict: KEEP.** The XinNet (Xiamen registrar) CA is a nice regional tell — consistent with a Chinese operator.

**Finding T5c — Three-IP mapping: relay → 43.108.48.133, eagle → 8.148.145.174, www → 121.196.245.158**
- **Novelty:** GENUINELY NEW.
- **Evidence:** PUBLIC SOURCE.
- **Actionability:** None.
- **Verdict: KEEP.**

**Finding T5d — eagle.woaifei.com: "EAGLE · 鹰击指数" page, SSL.com cert, observed 2026-10-01**
- **Novelty:** GENUINELY NEW.
- **Evidence:** PUBLIC SOURCE.
- **Actionability:** None.
- **Verdict: KEEP.** The oddest decorative detail in the round's farm finds — an "eagle strike index" page on the sibling of a box named "relay." Filed as color, which is all it can be.

**Finding T5e — Zero corpus hits**
- **Novelty:** OURS.
- **Evidence:** OBSERVED.
- **Actionability:** Tripwire.
- **Verdict: KEEP.**

**Finding T5f — INFERENCE: 'A box literally named "relay" … Relay-named infrastructure is self-describing'**
- **Novelty:** —.
- **Evidence:** INFERENCE.
- **Actionability:** None that the name itself generates.
- **Verdict: WOUNDED.** "Relay" is one of the most commodity hostnames in existence — mail relays, VPN relays, CDN relays, every other relay. A hostname does not confess. The infrastructure facts (SG box, active today, farm siblings, Chinese-registrar CA) keep fine as a lead; the "self-describing" gloss is the Thug admiring his own alliteration. Bleed the adjective, keep the box.

---

## HOST 6 — 139.45.201.13 (RETN, AS9002)

**Finding T6a — Identity: RETN Limited, AS9002, no hostnames, no domains**
- **Novelty:** OURS.
- **Evidence:** PUBLIC SOURCE.
- **Actionability:** None.
- **Verdict: KEEP.**

**Finding T6b — :443 "Supermicro BMC Login" wearing a self-signed cert with subject/issuer O=Jina AI (expired per Shodan)**
- **Novelty:** GENUINELY NEW.
- **Evidence:** PUBLIC SOURCE.
- **Actionability:** None — and the Thug's "do not touch the BMC interface" is the correct discipline; an internet-exposed BMC is not a toy.
- **Verdict: KEEP.** The round's highest-weirdness artifact, and weirdness with a receipt: an out-of-band management login has no business wearing a "Jina AI" identity unless someone wants that name in the scan record. The Thug's phrasing is exact.

**Finding T6c — Real-vs-imposter comparison: `ssl:"jina.ai"` total=4; the other three are Google Cloud with proper `*.jina.ai` GTS (WR3) certs — the real jina.ai infra; the RETN box is the only imposter**
- **Novelty:** OURS.
- **Evidence:** PUBLIC SOURCE.
- **Actionability:** Re-run the search; a fifth hit would matter.
- **Verdict: KEEP.** This is the evidentiary backbone of the weirdness claim — without the control (real jina.ai = GCP + GTS), the self-signed cert is just a self-signed cert. With it, it's an imposter. Well constructed.

**Finding T6d — Zero corpus hits**
- **Novelty:** OURS.
- **Evidence:** OBSERVED.
- **Actionability:** Tripwire.
- **Verdict: KEEP.**

**Finding T6e — INFERENCE: (a) attribution poison / cover, (b) honeypot, (c) lab box with a joke cert**
- **Novelty:** —.
- **Evidence:** INFERENCE.
- **Actionability:** None safe — all three readings counsel hands-off.
- **Verdict: KEEP.** Three hypotheses, no favorite, no laundering. The artist adds one shading the Thug underplayed: (b) honeypot deserves real weight — a fake "Jina AI" cert on an exposed BMC is a *fine* lure, and lures are built to be found by exactly this kind of scan. That's the Adversary's thread to pull, not a wound in the finding.

**Host verdict: "agent-infra LEAD — uncorroborated. Highest weirdness of the round."**
- **Verdict: KEEP.** Earned.

---

## Cross-cutting

**Environment caveat (local DNS hijacked to 198.18.0.216–227, discarded; Shodan stored DNS used instead)**
- **Novelty:** OURS. **Evidence:** OBSERVED (the hijack was the Thug's own measurement).
- **Verdict: KEEP.** The most important paragraph for everything downstream — poisoned local resolution disclosed, discarded, and replaced with a documented fallback. This is how you keep a whole report from rotting at the root. (Minor: Shodan's stored DNS carries its own staleness; the Thug's fallback is the right call, not a perfect one.)

**"Pivot counts" (3 / 2 / 4 / 5 / 4 / 4)**
- **Verdict: no grade — noted.** Pivot counts are effort accounting, not evidence. They tell the Chair how tired the Thug is, not how true the finding is. Harmless, but don't let the convention metastasize into a proxy for rigor.

**Round summary & recommendation (six uncorroborated LEADs; IP_LOG; corpus re-sweep on new events; orz.fit/qingchuan naming grammar as Adversary detection pattern)**
- **Verdict: KEEP.** The recommendation is the report's most actionable paragraph: a concrete tripwire (re-sweep when new events land — these farms are alive *this week*) and a concrete handoff (the mimicry grammar as a detection pattern). A report that ends in someone else's next move is a report that did its job.

---

## ARTIST'S SUMMARY

Twenty-six findings graded: **twenty-two KEEP, four WOUNDED, zero KILL.** Nothing fabricated, nothing overclaimed — every "LEAD" is labeled uncorroborated and every null is filed instead of buried. The four wounds are all in the adjectives, none in the bytes: the "New API"→gateway identification outruns its title (T1c); the chronology walks on last-observation timestamps (T1h); the "jina-reader clone" disjunct is stronger than its evidence (T2d); and "relay" as a hostname confesses nothing (T5f). One convention correction: Shodan-stored records are PUBLIC SOURCE, not OBSERVED — the Thug's corpus greps are the only true OBSERVED in the file. One open rival for the Chair: the orz.fit/qingchuan farm grammar is also the uniform of China's gray-market LLM API resale ecosystem — the resale discriminator (pricing pages, `/v1/models`, top-up flows) should be run before "agent-infra" hardens into a noun. Strongest shapes in the round: the qingchuan four-IP cartography (T4d), the two-node orz.fit farm (T3d), and the RETN BMC imposter with its real-vs-fake cert control (T6b/T6c). The composition holds.
