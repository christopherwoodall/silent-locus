# Supply-chain recon: CAPTCHA solvers + SMS/phone-verification services

**Collected:** 2026-10-04 (web search, secondary sources; pricing is "as of mid-2026" per sources cited).
**Lens:** agents/swarms only — commercial anti-bot-bypass and account-creation infrastructure. No human-operator attribution.

This is the tooling layer a swarm operator buys rather than builds: CAPTCHA tokens for getting through signup/login gates, and disposable phone numbers for SMS OTP verification at account-creation time. Both are commodity APIs with balance-top-up billing, and both now market directly to automation/agent developers.

---

## Part A — CAPTCHA-solving APIs

### 1. CapSolver — ★ most agent-native; only one with an official MCP server
- **Pricing (per 1,000 solves, AI-first, pay-as-you-go, min deposit ~$6):** reCAPTCHA v2/v3 ~$0.80–1.00, hCaptcha ~$0.60–0.90, Cloudflare Turnstile ~$0.50–0.80, FunCaptcha ~$1.80–2.50, GeeTest v4 ~$1.00–1.80, AWS WAF ~$1.20–2.00, image/text ~$0.40. Among the cheapest AI-first options; tiered volume discounts.
- **Method:** AI-first (not human workers); fastest median solve times in comparisons.
- **Agent integration — YES, first-party:**
  - Official `capsolver-mcp` package on PyPI (v0.1.1, Python 3.10+, MIT), published by `capsolver-ai`; listed in the official MCP Registry as `io.github.capsolver-ai/capsolver-mcp`.
  - Five tools: `solve_captcha`, `detect_captchas`, `solve_on_page` (browser-based + result fill-back), `get_balance`, `get_supported_captchas`. Transports: stdio (local clients), SSE, streamable-http (remote/hosted agents).
  - Docs target Claude Desktop / Claude Code / Cursor / Windsurf / Cline; natural-language invocation ("solve the reCAPTCHA on this page"). Playwright support via optional `browser` extra.
  - Also has "Agent Automation platform" marketing tying the API to agent frameworks and browser tools.
- **Swarm relevance:** the path of least resistance for an MCP-native agent to bypass CAPTCHAs. Any hunt finding capsolver-mcp in an agent's tool manifest / MCP config is a direct anti-bot-bypass indicator. Network fingerprint: API key env var `CAPSOLVER_API_KEY`.

### 2. 2Captcha — the incumbent human-solver grid (cheapest labor)
- **Pricing (per 1,000 solves, pay-as-you-go, min deposit ~$1–3):** simple image/text ~$0.50–1.00; reCAPTCHA v2/v3 ~$2.70–3.50; hCaptcha ~$3.00–3.90; Turnstile ~$1.50–2.50; FunCaptcha ~$10–15; GeeTest ~$3–5. Dynamic worker-pricing under load.
- **Method:** huge distributed human-worker pool, ~99% accuracy with free resend on misses; slower (10–40s typical on hard types).
- **Agent integration:** HTTP/JSON API + multi-language SDKs, Chrome/Firefox extensions. NO first-party MCP server or "AI agent" marketing found. De-facto standard in bot codebases though: the canonical `createTask`/`getTaskResult` protocol other services clone. Ubiquitous in GitHub automation repos (e.g. Playwright-based account/registration bots drop a 2captcha key file in env config).
- **Swarm relevance:** commodity fallback for hard challenges humans still beat AI on; lowest-barrier entry ($1 deposit). Expect 2captcha client-key strings (`<hex>` API keys) in automation configs, and worker-credit accounting on the operator side.

### 3. Anti-Captcha — enterprise-pitched human solver
- **Pricing (per 1,000 solves, pay-as-you-go, min top-up $10):** $0.50 (basic image) → $5.00 (reCAPTCHA Enterprise); most major types $1–3. Volume discounts automatic. Also sells package-style monthly bundles; accepts crypto.
- **Method:** 100% human-powered (operating since 2007), 13 CAPTCHA families; richer JSON API config (proxy, geo, emulation type); high-concurrency support ("thousands per minute").
- **Agent integration:** official client libraries (`anticaptchaofficial`), browser extensions, framework modules. Markets to "enterprise automation teams" — procurement-ready (DPA/MSA). NO MCP server or agent-specific marketing found.
- **Swarm relevance:** higher-trust tier for operators who need FunCaptcha/reCAPTCHA-Enterprise at scale and can tolerate the price; crypto top-ups = harder billing trail.

### 4. YesCaptcha — protocol-compatible budget solver
- **Pricing:** points system — 1,000 points = 1 CNY (~$0.14); task costs 2 points (simple OCR) to 30 points (hCaptcha). Aimultiple lists ~$1.50/1k starting. Custom "K1" task types for hardened reCAPTCHA v3 login flows (support-gated).
- **Method:** human + AI hybrid.
- **Agent integration:** API compatible with the AntiCaptcha/2Captcha protocol (drop-in client-key swap) — meaning any bot written for 2captcha works with YesCaptcha with one config line. Chrome extension ("YesCaptcha assistant"). No MCP server found.
- **Swarm relevance:** interoperability is the point — an operator can hot-swap providers per task type without code changes. Hunt for `yescaptcha.com` host + `clientKey` in automation configs.

### 5. NopeCHA — AI image-recognition, cheapest per-solve
- **Pricing:** 90,000 recognitions per $1 USD → ~$0.011 per 1,000; free tier 100 solves/day; monthly plans $4.99 (2k/day) → $99.99 (200k/day, 64+ concurrent).
- **Method:** AI-only recognition; Token API (browserless) + Chrome/Firefox extensions; official Python (PyPI) and Node (NPM) client libraries; works with Selenium/Puppeteer/Playwright; markets a "stealth mode" (undetected on sites).
- **Agent integration:** no MCP server; positioned for automation devs (RPA/scraping) rather than agents specifically. Extremely cheap per-solve makes it the volume option for simple challenges.
- **Swarm relevance:** price collapses the cost floor — at $0.011/1k, CAPTCHA cost is effectively zero for image-class types, so it never gates anything. Detect via nopecha.com Token API traffic.

### Notables from the long tail
- **CapMonster Cloud** ($0.60–1.20/1k, AI/OCR, self-hostable variant) — automation-dev focused, no agent marketing found.
- **NextCaptcha** ($0.50–0.90/1k) — AI, 2captcha-protocol-compatible.
- **DeathByCaptcha** (~$0.99–2/1k) — hybrid OCR+human fallback.
- **Clearance.sh / Capzy** — Cloudflare-specialized (Challenge + Turnstile), $0.40/1k, sub-second solves, drop-in `createTask`/`getTaskResult` compatible. Purpose-built for the Cloudflare wall most signups sit behind.
- **Open-source/local MCP options exist in the wild:** `dppalukuri/blackhole` ships a local-CLIP CAPTCHA-solver MCP server (free, no API key, CapSolver as fallback) — a swarm could solve locally with zero billing trail.

### Protocol convergence (important for detection)
Nearly all services clone the 2captcha `createTask` / `getTaskResult` JSON protocol. A bot's traffic is identifiable by this envelope + provider host. Any agent framework calling `solve_captcha`-shaped tools with a sitekey + page URL is using this supply chain.

---

## Part B — SMS/phone-verification services for automation

All are pay-per-activation, balance-top-up, REST API driven. Numbers are disposable/reused; platforms actively block virtual-number ranges, so this is a churn-and-retry game — exactly suited to automated account farming.

### 1. SMS-Activate (sms-activate) — the category reference (note: reviews note a closure; successors carry the traffic)
- **Pricing:** one-time SMS from ~$0.01–0.05; hourly rental from ~$0.20; monthly rental from ~$2. Balance-based, price varies by country/service/demand.
- **Coverage:** 80–180+ countries, 2,000+ supported services.
- **API:** REST API for automation, webhooks, bulk operations, usage analytics. Marketed for bulk account registrations, social-media account management, marketplace account creation, ad testing.
- **Swarm relevance:** the canonical "register N accounts via API" service. Limitation operators work around: reused numbers get blocked; occasional SMS delays; not for sensitive/long-term accounts.

### 2. 5SIM (5sim.net) — cheapest, most automation-hardened
- **Pricing:** activations from ~$0.007–0.02; sample per-service: Google ~$0.032, Facebook/Twitter/Microsoft ~$0.015, Instagram ~$0.061 per number. 15-minute window per number for multiple SMS. Host-SIM rentals (3h/1day) for longer holds. Dynamic pricing by country/service/inventory/demand.
- **Coverage:** 90–180+ countries, 500k+ daily numbers, major messaging/social/marketplace platforms (Telegram, WhatsApp, TikTok, Gmail, Amazon, eBay).
- **API:** reliable automation API; bulk activation handling tested stable; auto-refund on failure. Crypto-heavy payments (BTC/LTC/Payeer/Perfect Money), limited card support.
- **Explicit bot marketing:** their own materials/taglines reference bypassing OTP verification and creating "unlimited" accounts ("create an unlimited number of accounts", #OTPbypass framing).
- **Swarm relevance:** strongest bot-catering signal in the set — price floor near $0.01, crypto payments, API-first bulk flows. A swarm operator doing mass account creation would plausibly start here.

### 3. OnlineSIM (onlinesim.io) — rental/long-term specialist
- **Pricing:** one-time activations from ~$0.01 (reviews vary $0.01–0.05); long-term rentals with unlimited SMS reception are the specialty; 1M+ numbers; 90–115 countries for activations, 44 for rentals.
- **API:** documented REST API (purchase, poll for messages, webhooks, extend rentals); free test numbers; Telegram bot interface; desktop app.
- **Positioning:** "long-term rentals" and warmed-up accounts; cleaner dashboard (beginner-friendly); accepts cards + crypto + regional methods (Alipay, Apple/Google Pay).
- **Swarm relevance:** the retention layer — rentals with unlimited SMS let an operator keep accounts alive through re-verification prompts over weeks. Pair with 5SIM/SMS-MAN for creation, OnlineSIM for keeping.

### 4. SMS-MAN (sms-man.com) — the bulk-scale pick
- **Pricing:** from ~$0.01; 200+ countries; flexible payments (PayPal, cards, crypto, Coinbase, WeChat Pay).
- **API:** strong automation support; long-term rentals; refund system.
- **Positioning:** reviews rate it best for large-scale/bulk activations and "scaling"; use cases explicitly include SMM account farming, traffic arbitrage, Telegram bot automation, Instagram/TikTok account creation.
- **Swarm relevance:** the current volume leader for bulk per third-party comparisons. Broadest payment flexibility lowers the operator's onboarding friction.

### Emerging: "clean/trust" tier — Detect.Expert
- **Pitch:** "clean mobile numbers with a high level of trust from leading anti-fraud systems" for mass registration; virtual from $0.02/activation; *residential* numbers from $0.49/15min (up to 30-day runs) for warmed-up accounts; full API automation; Telegram support. 150+ countries, 650+ platforms.
- **Swarm relevance:** directly addresses the virtual-number blocking problem — residential/trusted numbers are the counter to platform anti-spam. Worth watching as the premium tier operators graduate to when cheap numbers get burned.

---

## Assessment: what a swarm operator would plausibly use

**Anti-bot bypass at scale:**
1. **CapSolver** — the only one with a native MCP server; if the swarm is MCP-agent-based, this is the default CAPTCHA tool. Cheapest AI-first per-solve, fastest, Turnstile/reCAPTCHA/Cloudflare covered.
2. **2captcha** — universal fallback; protocol is the lingua franca; $1 deposit means anyone can start.
3. **Cloudflare specialists (Capzy/Clearance.sh)** — for targets behind Cloudflare's wall: $0.40/1k, sub-second.
4. **Local CLIP-based MCP solvers** — zero-cost, zero-billing-trail option; exists in public MCP repos.

**Account creation / phone verification at scale:**
1. **5SIM** — cheapest activations, crypto payments, explicit bot-catering language, stable bulk API. Creation layer.
2. **SMS-MAN** — bulk-scale alternative, broadest payment options. Creation layer.
3. **OnlineSIM** — long-term rentals with unlimited SMS for keeping accounts alive. Retention layer.
4. **Detect.Expert-style residential numbers** — premium tier when platforms burn virtual ranges.

**Unit economics (why this is unstoppable):** a full account (CAPTCHA token ~$0.001 + SMS activation ~$0.01–0.06) costs **under $0.10**; mid-2026 attacker math puts CAPTCHA at ~5% of cost of goods sold for credential-stuffing operations. These are commodity line items, not deterrents — and CapSolver's MCP server makes them callable by an agent in natural language with zero integration code.

## Detection notes for the hunt
- MCP tool manifests / agent configs referencing `capsolver-mcp`, `solve_captcha`, `detect_captchas`, or env var `CAPSOLVER_API_KEY`.
- Automation configs carrying `clientKey` + provider hosts (2captcha.com, yescaptcha.com, capsolver.com, nopecha.com, api.capzy.ai, clearance.sh).
- Outbound API traffic to 5sim.net / sms-man.com / onlinesim.io / sms-activate endpoints during account-registration bursts — correlate with SMS-OTP timing (number issued → OTP arrives → account created) as an account-farming signature.
- Billing: crypto top-ups (BTC/LTC/Payeer/Perfect Money) across 5SIM/Anti-Captcha/Detect.Expert are the norm, not the exception.

## Sources
- Pricing/solver comparison (mid-2026): https://dev.to/webdecoy/why-captchas-are-dead-and-what-replaces-them-in-2026-170j
- CapSolver MCP server announcement: https://www.capsolver.com/blog/ai/introducing-capsolver-mcp-server-for-ai-agents
- capsolver-mcp GitHub: https://github.com/capsolver-ai/capsolver-mcp
- CapSolver MCP usage guide: https://www.capsolver.com/blog/ai/use-capsolver-mcp-server-ai-agents
- Anti-Captcha B2B/FAQ: https://b2b.anticaptcha.com/
- Cross-service pricing table: https://github.com/dppalukuri/blackhole/blob/HEAD/mcp-servers/captcha-solver/MARKET_RESEARCH.md
- YesCaptcha task types/pricing: https://github.com/qcoq838/captcha-login/blob/HEAD/README.md
- NopeCHA plans: https://www.aitechsuite.com/tools/17650
- 5SIM reviews: https://github.com/sms-god/5sim-login-review-2026-activation-speed-pricing-and-stability-tests ; https://bitcointalk.org/index.php?topic=5138474.0
- OnlineSIM review: https://github.com/ophbg2/onlinesim
- SMS-MAN/OnlineSIM/5SIM comparison: https://github.com/romantut1988/sms-man-vs-onlinesim-2026-disposable-numbers-from-0.01-service-comparison/blob/HEAD/README.md
- Detect.Expert (bitcointalk): https://bitcointalk.org/index.php?topic=5563975.0
