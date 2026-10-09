# Supply-chain recon: where a swarm operator parks harness infrastructure cheaply and anonymously

Research date: 2026-10-04. Public sources only (search snippets + review/comparison sites). No purchases, no accounts created.
Scope: commercial providers, agent/swarm infrastructure only. No human-operator attribution.

---

## 1. Cheapest VPS providers ($2–5/mo tier), with tolerance notes

| Provider | Floor price | Specs at floor | Jurisdiction / DCs | Crypto? | Scraping/automation tolerance signal |
|---|---|---|---|---|---|
| **Vultr** | $2.50/mo (Regular cloud compute, EU) | 1 vCPU / 512 MB / 10 GB SSD | US-headquartered (CLOUD Act); 32 regions incl. 9 EU cities | No (card/PayPal) | Strong API + Terraform, hourly billing — the standard DIY bot fleet substrate. Actively abuse-managed, not lax. |
| **OVHcloud** | €3.81/mo (12-mo term) / €4.49 m2m | 1 vCPU / 2 GB / 40 GB NVMe, unlimited traffic ≤500 Mbps | France (EU law) | No (card) | Unlimited traffic, no bandwidth caps — friendly to crawl workloads. Strict abuse handling for spam/network abuse, but scraping itself is typically fine if well-behaved. |
| **Contabo** | ~€4.40/mo (24-mo term, Cloud VPS 4: 4 vCPU / 8 GB / 100 GB, unlimited traffic) | Unlimited traffic, 200–600 Mbit/s ports | Germany (EU law only, no CLOUD Act) | **No** | Highest specs-per-euro; documented pick for mail servers/scraper test boxes. Weak SLA/uptime (~91% measured early 2026), slow support. |
| **InterServer** | $3.00/mo (1 slice) | 1 vCPU / 2 GB / 40 GB SSD, 2 TB transfer | US | No | Budget workhorse; permissive-ish, little friction at signup. |
| **Time4VPS** | €2.88/mo (Linux 2) | 1 core / 2 GB / 25 GB SSD, 4 TB | Lithuania (EU) | No | Unmetered-traffic European VPS segment; low profile. |
| **netcup** | €3.35–5.91/mo | 2 vCPU / 4 GB / 128 GB NVMe | Germany | No | Cheap but has verification/KYC friction at signup; **bad** for anonymous use. |
| **DigitalOcean** | $4/mo (512 MB droplet, per-second billing since Jan 2026) | 1 vCPU / 512 MB, 500 GB transfer | US (CLOUD Act) | No | Great API + docs; aggressive automated abuse/ToS suspension reputation. |
| **Kamatera** | $4/mo, $100 trial credit | Granular CPU/RAM, hourly billing | US (CLOUD Act) | No | 30-day trial credit = free ephemeral capacity; real-name signup. |

**Tolerance reading:** mainstream cheap hosts tolerate automation *as a workload* (Vultr/DO APIs are built for it) but all run automated abuse pipelines — spam, outbound scanning, DDoS reflection get accounts killed fast. Scraping is tolerated insofar as it's well-behaved (rate-limited, no port-scanning, no spam); the real constraint is **IP reputation**: Contabo/OVH low-cost ranges are heavily flagged by target sites and anti-bot vendors, which is why operators rotate to residential/proxy overlays rather than relying on host tolerance.

**Key cost fact:** a self-hosted agent-harness VM costs ~$2.50–6/mo flat, versus ~$545/mo for the same compute on managed sandbox platforms (per dev.to Firecracker comparison, Sep 2026) — two orders of magnitude gap. Any cost-sensitive swarm operator self-hosts.

---

## 2. E2B and cloud sandbox alternatives (agent execution layer)

**E2B (e2b.dev)** — incumbent default for agent code execution:
- Firecracker microVMs, ~150–200 ms cold start, open-source (Apache-2.0), self-hostable via Terraform.
- **Pricing:** per-second wall-clock: $0.000014/vCPU-s ($0.0504/vCPU-hr) + $0.0000045/GiB-s ($0.0162/GiB-hr). Hobby = free + **one-time $100 credit**, 1-hr max session, 20 concurrent, 10 GiB storage. Pro = $150/mo base (buys limits, not credits) + usage, 24-hr sessions, 100+ concurrent. Egress/API calls not metered (as of mid-2026).
- Free tier ≈ ~920 sandbox-hours at the default 2 vCPU / 512 MiB size. Paused sandboxes kept indefinitely with $0 compute.
- **Operator note:** signup is a normal email/card flow; abuse teams monitor. A swarm operator *could* use Hobby credits across throwaway accounts, but attribution goes straight back to the provider's billing records — not an anonymity layer.

**Alternatives (from Upstash 2026-09 and beam.cloud comparisons):**

| Platform | Isolation | Billing | Free tier | Why an operator would care |
|---|---|---|---|---|
| **Daytona** | Containers (Kata optional) | Same per-second rates as E2B | $200 credit | Sub-90 ms cold starts; **open-source repo unmaintained since Jun 2026** — the self-hostable fork lane |
| **Modal** | gVisor | Per-second, ~3x its Function rate | $30/mo credit | GPU workloads (self-hosted models); Python-native |
| **Vercel Sandbox** | Firecracker | Active CPU time (not lifetime) | 5 active CPU-h, 420 GB-h | Bills active CPU only — cheaper for idle-wait agent loops |
| **Cloudflare Sandbox** | Containers (edge) | $0.072/vCPU-hr + $0.009/GiB-hr | None on Free plan | Edge placement; no free tier = higher friction |
| **Blaxel** | microVM | Memory-based | Up to $200 credit | Standby resume <25 ms |
| **Northflank** | Kata/Firecracker/gVisor | $0.01667/vCPU-hr (cheapest managed) | 2 free services | BYOC self-serve — near-VPS cost with managed lifecycle |
| **Beam** | gVisor | $0.135/physical-core-hr | $30/mo credit | H100/B200 GPU sandboxes |
| **Temps** | Docker or Firecracker | Free self-hosted (you pay for server) | $0 (Apache-2.0) | Full self-host ≈ $6/mo VPS; **built-in AI gateway (OpenAI/Anthropic/Gemini/Grok)** |
| **Lume** | Apple Virtualization.framework | Free (open-source) | $0 | macOS/Linux CUA sandboxes, local-first |
| **Upstash Box** | microVM | Active core-hours only | 10 boxes, 5 CPU-h/mo, $1 LLM budget, no card | No card on free tier; billed only while executing |
| **Kubernetes-native** | gVisor/pod + runtime of choice | Your cluster | $0 | GKE Agent Sandbox (300 starts/s claimed, May 2026 GA), Bedrock AgentCore microVMs, kubernetes-sigs/agent-sandbox |

**Assessment:** for a swarm operator, the managed-sandbox lane is a convenience tax with attribution attached (every account ties to payment identity + SDK telemetry). The economic move is **self-hosted open-source sandboxes (Temps, Daytona forks, microsandbox, Lume) on $3–6/mo VPS** — same Firecracker/gVisor isolation, no per-second meter, no account trail to a sandbox vendor.

---

## 3. API-key resellers / shared-key markets (publicly visible, none purchased)

### Legit-adjacent aggregators (commercial, semi-transparent)
- **OpenRouter** — model gateway reselling tokens at ~60–70% of official price; high-volume arbitrage. Not anonymous but legitimate.
- **CometAPI** and clones — "one API key, 500+ models," OpenAI-compatible base-URL swap, advertised ~15–25% below official prices.
- **EasyRouter / B.AI / WorldClaw** — cited in press as prominent CN-adjacent reseller brands; market volume estimated >1B yuan (~$147M) in H2 2025 alone (BigGo Finance, 2026).

### Grey-market mechanics (documented in ChinaTalk/deeplearning.ai coverage, 2026)
- Account farms (bulk AI accounts), phone-verification suppliers, **token resellers dealing in unused quotas**, identity brokers (fake credentials), model routers, payment processors — a full stack exists to service developers who can't buy directly.
- Tactics: aggregating free API credits, reselling unused account quotas, exploiting educational/corporate discounts, regional pricing arbitrage, and outright illicit sources (stolen cards, firewall circumvention). Claude tokens advertised at **~10% of official price** in CN channels.
- Common fraud patterns: **model substitution** (silently routing to cheaper models), inflated token-count reporting, reverse-proxying via personal paid accounts.
- Anthropic's **September 2026 threat report** documents GTG-50021 ("kl1zy," Russian/Ukrainian-speaking): a "cheap Claude" reseller that proxied traffic to other models and **installed a credential harvester**, stealing buyer Anthropic credentials and selling them to other proxy resellers. Lesson for any buyer: discounted keys are a credential-theft route.

### Where it's sold (observed surfaces)
- **plati.market** — active listings: "$10 ChatGPT 4 / Anthropic / Gemini API key, auto-delivery" (third-party OneAPI-style endpoint, you swap the base URL; "$10 ≈ 1000 messages to gpt-4o or sonnet-4"); "$100 ChatGPT 4o API key" listings. Auto-delivery, no expiry until balance spent.
- **BlackHatWorld marketplace** — OpenAI threshold/credit account sellers: "$5 threshold accounts from $10," "$2500 credit accounts from $400–$999," bulk discounts; payment **USDT, BTC, Payoneer, Wise**; contact via PM/Telegram/Skype; 3-day warranty, no refunds.
- **Telegram** — e.g. `@opustokens_bot`: "API keys for Claude and GPT for pennies. Pay with Telegram Stars. No VPNs, card bans, or limits." Infostealer-log resellers on Telegram sell **working Claude Pro / ChatGPT sessions for ~$5** (FlashPoint: 44,791 stolen JWTs in one dump, 555 AI-service tokens, 24 still-valid keys at analysis).
- **GitHub (CN dev ecosystem)** — `free-ai-token` skill repos: tooling that auto-registers accounts, scans for free/cheap token deals, regional subscription arbitrage (Turkey/India/Argentina), and wires keys into agent harnesses (Cherry Studio, Dify, opencode, codex). This is the "agent-ready" face of the key market: **machine-readable deal discovery**.

**Assessment for swarm operators:** a swarm needs inference at scale. Options in ascending cost: (1) stolen/infostealer keys (~$5/session, commodity on Telegram); (2) grey resellers at 10–40% of list via crypto/Stars, model substitution risk accepted; (3) legit resellers (OpenRouter etc.) at 60–85% of list. All grey tiers accept crypto and impose no meaningful KYC — the key layer is where anonymity is actually cheapest.

---

## 4. Bulletproof-hosting-adjacent hosts ("no questions asked" / crypto)

| Host | Floor price | Jurisdiction | Crypto accepted | Posture |
|---|---|---|---|---|
| **FlokiNET** | €7.99/mo VPS (+€5 setup on monthly) | Iceland / Romania / Netherlands | BTC, LTC, **XMR**, ZEC, ETH, DOGE, DASH + more | Freedom-of-speech framing (est. 2012); free DDoS protection; email signup only. Reviews note "weirdly permissive" abuse stance |
| **Njalla** | €15/mo VPS (1.5 GB RAM, 15 GB disk) | Sweden | XMR + crypto, **Tor onion signup**, XMPP registration | No personal data; blocks email server ports by default |
| **Shinjiru** | ~$3.95/mo shared / VPS from higher tiers | Malaysia (outside 14 Eyes) | BTC direct, no gateway | Since 1998; "Strongbolt" high-risk tier; investigates DMCA individually; no personal details required |
| **Impreza Host** | VPS from ~€8–15/mo range | Seychelles | BTC, XMR | Tor-first: .onion hosting, Tor-compatible VPS, no KYC, no data-retention laws |
| **AlexHost** | €5.90/mo VPS | Moldova | BTC, **XMR**, LTC, ETH, DASH, USDT, USDC + more | DMCA-ignored marketing |
| **BPServ** | $80/mo VPS (entry bulletproof tier) | Malaysia (company); infra NL/RU/MY/UA/MD/RO | BTC, LTC, altcoins | Explicitly "ignores complaints/DMCA," no logs kept, anonymous SSL |
| **QloudHost** | $4.16/mo VPS entry | Netherlands (Amsterdam Tier-III) | USDT + crypto, **no KYC** | DMCA-ignored under Dutch law; instant setup |
| **NoData.pw** (bitcointalk vendor) | $15–32/mo web; dedis $65+/mo | Iceland | BTC/XMR, no KYC | "Private by design," Tier-3 DC |
| **exodia.run** (bitcointalk vendor) | ~€7/mo in BTC/XMR | undisclosed | XMR/BTC, voucher system via Tor, escrow | No-KYC KVM VPS, JS-free panel |
| **HostCreed** | entry tiers advertised low | undisclosed offshore | BTC, USDT, no KYC | DMCA-ignored, instant setup |

**Notes:**
- The Dec 2025 Dutch police seizure (~250 physical servers, bulletproof host active since 2022, seen in 80+ cybercrime investigations, hardware in The Hague/Zoetermeer) shows the top-end bulletproof tier is an active law-enforcement target — operators using it inherit that risk. Seizure seized thousands of co-hosted VMs with the hardware.
- True bulletproof VPS floors at **~€5–8/mo** — not much more than mainstream cheap VPS. The real premium is at dedicated tiers ($59+/mo).
- Most "no questions asked" marketing targets DMCA-ignored web hosting; the ones that matter for harness infra are those with **Tor signup, Monero, no email requirement, and VPS products** (FlokiNET, Impreza, exodia.run-class vendors).

---

## Synthesis: the swarm operator's stack

1. **Compute:** self-hosted open-source agent sandboxes (Temps / Daytona forks / Firecracker microVMs) on €3–6/mo anonymous-ish VPS (FlokiNET/Impreza/exodia-class at €5–8/mo for Tor-signup + XMR, or throwaway Contabo/OVH accounts at €3–5/mo where identity isn't needed). Managed sandboxes (E2B etc.) are a ~100x cost multiplier and an attribution trail — economically and operationally irrational for a swarm.
2. **Keys:** grey-market pooled keys (plati.market auto-delivery, Telegram bots @ Stars, BHW credit-account sellers at USDT/BTC) or stolen session tokens (~$5 on Telegram) — the whole key layer runs on crypto with no KYC, and the CN skill-repo ecosystem shows keys are already being programmatically sourced and wired into agent harnesses.
3. **The cheapest anonymous configuration is the grey-key layer, not the compute layer:** $3–8/mo VPS + $5–10 grey API credit ≈ **<$20/mo per swarm node**, all payable in Monero/USDT, most purchasable without any personal identifier. The bottleneck is not cost or anonymity of infra — it's IP reputation and rate limits, which is where proxy/residential overlays (not covered here) come in.

*End of recon. No purchases made; all findings from public web search results, 2026-10-04.*
