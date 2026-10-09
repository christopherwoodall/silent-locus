# Lane 3 partial — egress destinations 7–10 recon
Researcher: passive-recon subagent (lane3) · Date: 2026-10-05
Study context: `../EGRESS_MAP.md` (top-10 egress destinations, lanes A–E)
Methods: web search (browser.search), public-docs fetch (browser.open), Shodan stored
observations (`~/workspace/skills/shodan/bin/shodan.py`, count/search only — no host
probes, no touching), Certificate Transparency (crt.sh JSON, counts only).
HARD RULES held: no probing, no exploitation, infrastructure-only scope, never fetch
suspicious URLs directly (search snippets used instead).

Study-grounding (from raw evidence, not re-derived):
- Lane E lane-e `_tomic-lail_atomic-mail-agentic` (repo_url
  https://github.com/Atomic-Mail/atomic-mail-agentic): CRITICAL score 162,
  "118 egress primitives across 5 categories: browser, email, gitwrite, img_upload,
  netcall"; EGRESS_MAP tags it "autonomous email send + RFC 8620 attachments".
- Lane E `bitwarden_mcp-server` (repo_url https://github.com/bitwarden/mcp-server):
  HIGH score 9 ("multipart file upload call; HTTP client call; shell HTTP client [8
  egress primitives across 2 categories: img_upload, netcall]").
- Lane B enum (`raw/enum-marketplaces.md`): Atomic Mail Agentic (mcp.so #2, 255 stars,
  "agents read/send/react to email autonomously"); LocalCan (#7, 82 stars,
  "public-URL tunnels for localhost (ngrok alternative) — tunnel primitive"); Roamzy
  (roamzy-io, "agent-native eSIM — agent buys eSIMs with USDT/USDC"); anon.li (MCP)
  (3.2k, "create/edit/delete email aliases, file shares & forms from Cursor —
  privacy tooling, direct exfil-adjacent primitives").

---

## (7) Email via JMAP send + blob attachments — Atomic-Mail / anon.li

### What our study found
`atomic-mail-agentic` (Atomic-Mail org, lanes B+E): a complete agent-native email
provider shipped as MCP/AgentSkill/REST/CLI. Autonomous inbox registration, full
JMAP mailbox (RFC 8620) with send + attachments (RFC 8620 blob upload), SMTP usage,
multipart upload, plus browser automation libs — i.e. an agent can mint its own
inbox and exfiltrate files by email with zero human involvement.

### Public intel on the destination as an agent-egress channel
- **Atomic-Mail/atomic-mail-agentic** (GitHub, repo last updated 7 days ago):
  https://github.com/atomic-mail/atomic-mail-agentic — tagline "Let your agents
  read, send, and react to email autonomously, without human involvement". Built on
  JMAP (RFC 8620): "JMAP is well represented in LLM training data, so models
  already speak it fluently — they rarely hallucinate request shapes". Access gated
  by proof-of-work signup (no CAPTCHA/manual approval). Free accounts: 100 MB
  storage quota, custom domain included, rate limits "sized for agent workloads".
  Integrations: MCP, AgentSkill, REST, CLI for Claude Code, Codex, Copilot, Cursor,
  Hermes, OpenClaw, Pi, Kilo Code.
- Product Hunt launch page (listed ~12 days ago):
  https://www.producthunt.com/products/atomic-mail-agentic — "Agents finish without
  asking users for anything, messages actually arrive (warming IP pool + relay
  overflow)"; features bundled `send_mail`, `list_inbox`, `reply` JSON presets;
  Open Alpha, free, 100 MB, strict rate limits.
- Agent-native-services writeup (haoruilee/awesome-agent-native-services):
  https://github.com/haoruilee/awesome-agent-native-services/blob/HEAD/services/communication/atomic-mail.md
  — each inbox is a distinct `@atomicmail.ai` (or verified-domain) address, API key
  stored under `~/.atomicmail/credentials.json`; slogan "Not AI for your email.
  Email for your AI."
- **Public docs** (docs.atomicmail.ai, fetched 2026-10-05): quickstart registers
  `myagent@atomicmail.ai` via PoW (`npx --package=@atomicmail/agent-skill
  atomicmail register --username "myagent" --watch scheduled`), then
  `jmap_request --ops-file send_mail.json --vars '{"TO":"alice@example.com",...}'`.
- **anon.li** (lane B companion): open-source privacy product, AGPL-3.0, repo
  https://github.com/heyitzkamal/anon.li — three offerings: Alias (anonymous email
  forwarding, SRS replies), Drop (zero-knowledge E2EE file sharing, AES-256-GCM,
  browser-side encryption, blobs direct browser↔Cloudflare R2 via presigned URLs,
  up to 250 GB per transfer), Form (encrypted form submissions). CLI:
  https://github.com/anondotli/cli. Service: https://anon.li/drop. Its MCP (lane B,
  3.2k stars) exposes create/edit/delete email aliases, file shares & forms from
  Cursor.

### Notable prior incidents / writeups (email + agent/MCP egress)
- **Koi Security — postmark-mcp BCC backdoor (2026-09-25, disclosed 2026-09-25 by
  researcher Idan Dardikman)**: npm package `postmark-mcp` impersonated the
  Postmark email service; 15 clean versions built trust, then v1.0.16 (released
  2026-09-17 by alias `phanpak`) added one line BCC'ing every outbound email to
  the attacker address phan@giftshop.club (defanged as phan@giftshop[.]club in
  some writeups). ~1,643 total downloads (~1,500/wk); Koi estimated ~20% ran in
  production ≈ ~300 orgs potentially affected (download-based estimate, not a
  confirmed victim count); Postmark/ActiveCampaign disavowed the package. First
  publicly documented in-the-wild malicious MCP server.
  Sources: https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html
  (2026-09-29); incident record
  https://github.com/makerchecker/makerchecker/blob/HEAD/incidents/entries/AID-2025-0013.md
  (AID-2025-0013, severity high, reproducible); supply-chain writeup
  https://github.com/harekrishnarai/software-supply-chain-monitor/blob/HEAD/attacks/2025-10-postmark-mcp-bcc-injection.md.
- **bytehide.com — "MCP Security Considerations: The Complete 2026 Guide"** (updated
  5 days ago): https://bytehide.com/blog/mcp-security-guide — cites a May 2026
  preprint measuring ~8,000 live remote MCP servers with ~40% exposing tools with
  no authentication; typosquatting/impersonation section uses postmark-mcp as the
  canonical case.
- **Security Boulevard** (2026-06): "Malicious MCP Servers & Email Security: The
  New Supply Chain Threat":
  https://securityboulevard.com/2026/06/malicious-mcp-servers-email-security-the-new-supply-chain-threat/
  — email MCP servers give "god-mode" delegate rights; tool-poisoning/rug-pull
  variants.
- **AgentMail** (competitor, agentmail.to) comparison page (updated 2 days ago):
  https://www.agentmail.to/blog/best-mcp-servers-for-ai-agents — AgentMail hosted
  MCP at https://mcp.agentmail.to/mcp with 36 tools (inboxes, threads, messages,
  drafts, attachments), OAuth or API key; same risk class, confirming agent-email
  MCP is a commoditized product category.
- General agent-exfil via email: jinnu92/ai-security-field-guide MCP insecure-auth
  scenario (attacker uses exposed `send_email` tool to exfiltrate customer data):
  https://github.com/jinnu92/ai-security-field-guide/blob/HEAD/docs/part4-mcp/mcp04-insecure-auth.md.

### Observed infrastructure data (stored/indexed only)
- Shodan `hostname:atomicmail.ai` count query → **10 hosts**.
- Shodan `search 'hostname:atomicmail.ai' 2` (stored observations):
  - `mx1.atomicmail.ai` → 89.127.218.190:995 (POP3S), org/isp Fornex Hosting S.L.,
    scanned 2026-10-05T04:36:43.
  - `staging.atomicmail.ai` cluster → 178.104.184.116:443, Hetzner Online GmbH,
    hostnames: dashboard.staging.atomicmail.ai, health.staging.atomicmail.ai,
    **mcp.staging.atomicmail.ai**, rspamd.staging.atomicmail.ai,
    api.staging.atomicmail.ai, auth.staging.atomicmail.ai,
    grafana.staging.atomicmail.ai, mx1.staging.atomicmail.ai, www/mta-sts
    variants (rspamd = spam-filtering stack on staging).
- crt.sh not queried for atomicmail.ai (task scope: tunnel-broker CT only).
- Note on sensitivity: IP/hostname data above is infrastructure-only (no human
  identifiers), recorded per evidence rule.

### Novelty note — (7)
**Largely published-adjacent, but our study's specific finding is not.** The
general risk class — email-sending MCP servers as silent exfil channels — is
well documented (postmark-mcp BCC backdoor, Sep 2025; multiple 2026 security
guides; AgentMail as a commercialized category). What nobody else documents is
our study's precise finding: a purpose-built **agent-native ESP whose own
marketing is "email for your AI"** — PoW self-onboarding, JMAP fluent in LLM
training data, attachment-capable — shipped as a skill/MCP and scoring CRITICAL
in our scan. The novelty is the *self-service onboarding*: no credit card, no
CAPTCHA, no human setup means the exfil channel is mintable by the agent itself.
anon.li's MCP (email aliases + E2EE file drops from Cursor) has no dedicated
public writeup at all. **Verdict: partial novelty — new primitive (self-service
agent email), known risk class.**

---

## (8) Bitwarden vault via MCP

### What our study found
`bitwarden/mcp-server` (official Bitwarden repo, lane E): agent-facing MCP server
over Bitwarden CLI + Public API — vault item read/create/modify/delete, org
secrets and admin functions. Graded HIGH in our scan (multipart upload + HTTP
client primitives). Credential-adjacent by design: whoever holds the MCP session
reads the vault.

### Public intel on the destination as an agent-egress channel
- **Official repo** (last updated 5 days ago): https://github.com/bitwarden/mcp-server
  — "A Model Context Protocol (MCP) server that provides AI assistants with
  secure access to Bitwarden password manager functionality". README carries an
  explicit WARNING block: designed **exclusively for local use, never hosted
  publicly or exposed over a network**; granting access gives the assistant
  ability to "read vault items including passwords, secure notes, and sensitive
  data", "create, modify, and delete vault items", "access organization secrets
  and administrative functions", "expose credentials and vault contents through
  AI responses". Responsibilities: run only locally, never share configs with
  session tokens, never use over untrusted networks, never grant to untrusted
  clients. The vendor itself frames this exactly as our study does.
- **Ecosystem mitigations** (show the risk is recognized, with safer patterns):
  - `adamrowles1996/vaultgate` (updated 7 days ago):
    https://github.com/adamrowles1996/vaultgate — self-hosted remote MCP for
    Bitwarden with OAuth 2.1: hosted agents (Claude, Codex) *use* credentials
    "without ever seeing them"; short-lived scoped revocable tokens; agent gets
    only results.
  - `brissux-labs/agent-secrets` (updated 12 days ago):
    https://github.com/brissux-labs/agent-secrets — secret *broker* (not vault)
    on Bitwarden Secrets Manager: MCP server exposes metadata + controlled
    execution, **no raw-value tool in the default toolset**; values injected only
    into child-process env.
- **Field usage**: `porkchopexpress86/taxprotest-django` SKILL.md (updated 7 days
  ago): https://github.com/porkchopexpress86/taxprotest-django/blob/HEAD/.agent/skills/security-review/SKILL.md
  — documents wiring `@bitwarden/mcp-server` (npx) into `mcp_config.json` with
  `BW_SESSION` for AI pair programming, so "the agent can securely look up
  configuration keys without requiring local `.env` files in git" — i.e. this
  deployment pattern (agent + live vault) is being taught in skills in the wild.

### Notable prior incidents / writeups
- No public incident of Bitwarden-MCP vault exfiltration found in search. The
  adjacent canonical cases: postmark-mcp (above) and the May-2026 preprint's ~40%
  unauthenticated remote MCP servers (via bytehide.com). The official README
  warning is the closest thing to a published risk statement for this exact
  server.

### Observed infrastructure data
- None collected: the official server is stdio/local-only by design; no remote
  endpoint to enumerate. No Shodan/CT queries run for this destination (nothing
  to fingerprint — stdio process, local machine).

### Novelty note — (8)
**Low novelty; vendor self-documents the risk.** Our study's HIGH grading aligns
with Bitwarden's own README warning verbatim. The new-ish observation from our
lanes is *deployment reality*: skills in the wild (e.g. the taxprotest-django
security-review skill) are wiring this into agent configs, and `BW_SESSION` in
`mcp_config.json` puts vault-session tokens in files agents can read — the
credential-adjacent loop is self-reinforcing. vaultgate/agent-secrets show the
ecosystem is already building no-raw-value brokers as the answer. **Verdict: low
novelty — the risk is published by the vendor; the study's contribution is
measuring its presence in the skill supply chain.**

---

## (9) LocalCan localhost-tunnel broker

### What our study found
`localcan` (lanes B/E, mcp.so #7, 82 stars): ngrok-alternative tunnel service with
an MCP server for AI agents. Docs-only + closed binary per EGRESS_MAP. Tunnel
primitive: agent can expose localhost to the public internet.

### Public intel on the destination as an agent-egress channel
- **Official repo** (last updated 58 days ago): https://github.com/localcan/localcanapp
  — "The ngrok alternative for Mac, Windows & Linux. Public URLs (tunnels), .local
  domains, automatic HTTPS, traffic inspector, MCP server for AI agents. Free
  plan." Features: Public URLs like `https://my-app.localcan.dev`; TCP tunnels
  for databases/SSH/non-HTTP services; `.local` domains via mDNS; Snapshots
  (static copy stays online while machine is off); access control (password page,
  secret link, IP/user-agent rules, enforced on LocalCan's servers); **MCP
  server: "AI agents can inspect captured traffic, manage Public URLs, publish
  Snapshots, and password-protect what you share."**
- **Changelog** (fetched via search snippet): https://www.localcan.com/changelog —
  **2026-07-02 entry**: "AI agents (MCP) — LocalCan is now an MCP server. Connect
  Claude Code, Codex, Cursor, or any MCP host, and ask your agent to debug a
  failing webhook from the traffic it actually sent, **expose a local port and
  hand back the Public URL**, or pause and clean up URLs you no longer use."
  Same entry documents **"Agent safety — Agent access, secret redaction, and
  write access are three separate switches.** Sensitive headers (Authorization,
  cookies, API keys) are redacted from agent responses by default, and agents
  can only read until you allow changes (off by default)."
- **MCP install doc** (llms-install.md):
  https://github.com/localcan/localcanapp/blob/HEAD/llms-install.md — MCP built
  into the `localcan` CLI (`claude mcp add --scope user localcan -- localcan
  mcp`); write tools (creating Public URLs, publishing Snapshots, setting
  passwords) off by default, enabled with `localcan mcp access read_write`.
- **Docs — Public URLs**:
  https://www.localcan.com/docs/public-urls/overview — "AI agents can create and
  manage Public URLs too, over MCP or the CLI."
- Competitor roundup (pinggy-io blog, updated 4 days ago):
  https://github.com/pinggy-io/pinggy_website/blob/HEAD/content/blog/best_ngrok_alternatives.md
  — LocalCan listed as desktop-native ngrok alternative; AlternativeTo page:
  https://AlternativeTo.Net/software/localcan-/about/ (proprietary, by Jarek
  Ceborski; subscriptions $8–45/mo). No security-abuse writeup found for LocalCan
  specifically.

### Notable prior incidents / writeups
- **None for LocalCan specifically.** The risk class (agent-exposed localhost via
  tunnel brokers) is our study's destination #1 (ngrok/cloudflared, loki-mode /
  pinme / telnyx-mcp); no published incident ties LocalCan's MCP to abuse. The
  vendor's own 2026-07-02 "Agent safety" switches are the only public
  risk-adjacent documentation.

### Observed infrastructure data (stored/indexed only — no host touched)
- crt.sh query: `https://crt.sh/?q=%25.localcan.dev&output=json` (2026-10-05):
  **58 unique certs**. Common names: `localcan.dev` 45, `beta.localcan.dev` 13
  (incl. `*.beta.localcan.dev` wildcard). Issuers all Let's Encrypt
  (E8 14, E7 12, R3 10, E6 8, E5 6, ...). **Zero per-user tunnel subdomains in
  CT** — user tunnels (e.g. `my-app.localcan.dev`) are covered by `*.localcan.dev`
  wildcards, so individual user-created tunnels do not appear in CT. Only 2
  certs issued since 2026-08-01.
- Shodan exact queries (2026-10-05), count then slim search of stored records:
  - `ssl:"*.localcan.dev"` → **3 hosts**; `hostname:localcan.dev` → **4 hosts**;
    `product:"LocalCan"` → **0**.
  - Stored records: 188.166.67.111:443 (DigitalOcean), hostnames
    `10l3cf9pol4wirhvu6l17ioj.cname.localcan.dev`, `localcan.dev`, scanned
    2026-10-04T08:16:43; 165.232.89.54:443 (DigitalOcean), `beta.localcan.dev`,
    scanned 2026-10-03T19:05:38; 24.144.90.104:443 (DigitalOcean), hostnames
    `localcan.dev`, `5pfdbewn4mhevqse79od43oj.cname.localcan.dev`, scanned
    2026-09-20T23:59:51.
  - Infrastructure read: edge on DigitalOcean; per-tunnel internal names follow
    `<25-char alnum>.cname.localcan.dev` (e.g. `10l3cf9pol4wirhvu6l17ioj`,
    `5pfdbewn4mhevqse79od43oj`) — consistent with per-user tunnel endpoints
    resolved internally behind the edge. No product banner fingerprinted.
- Note on sensitivity: IPs/hostnames are service infrastructure only (no human
  identifiers).

### Novelty note — (9)
**High novelty as a combined primitive; no prior publication of this finding.**
LocalCan's MCP server (agent can open public tunnels to localhost, incl. TCP
tunnels to databases/SSH, publish Snapshots that persist while the machine is
off) is openly documented by the vendor, but *nobody frames it as an
agent-egress/ingress primitive*. Our study is the first to put "agent-driven
localhost exposure with an MCP switch" next to the tunnel-broker infra and flag
it credential-adjacent. The vendor's own read/write MCP split and header
redaction (2026-07-02) show they thought about it, but write access is one CLI
command (`localcan mcp access read_write`) away. The `*.cname.localcan.dev`
internal per-tunnel naming observed in Shodan is a new fingerprint detail not
found in any public doc. **Verdict: novel — first security framing of an
agent-operated tunnel broker; infra fingerprint (cname subdomain grammar) is new
public intel.**

---

## (10) Roamzy eSIM purchase API (crypto-funded)

### What our study found
`roamzy-io` (lane B): "agent-native eSIM — agent buys eSIMs with USDT/USDC". Data-
exfil / credential-adjacent: an agent can mint anonymous mobile identities funded
by crypto.

### Public intel on the destination as an agent-egress channel
- **Official repo + README** (last updated 28 days ago):
  https://github.com/roamzy-io/mcp-server — "Agent-native global eSIM over MCP —
  an AI agent buys one eSIM for 193 countries, **anonymously, per-MB in USDT/USDC
  crypto, and earns 20% referral forever.**" Thin client to
  `https://roamzy.io/api/v1/*` mapped 1:1 to MCP tools. Sample Claude Desktop
  flow: agent asks which stablecoin/network (USDT on TRON/BSC/Polygon/Optimism/
  Arbitrum/TON, or USDC on Solana/BSC/Polygon/Optimism/Arbitrum), min top-up
  **$20 USDT**; order mints eSIM (sample MSISDN 2040XXXXXX); payment via
  nowpayments.io link; agent fetches activation QR after ~1 min on Solana.
  Anonymous account minted on first authed tool call — **no signup required**;
  anonymous token cached in-process, claim via magic-link `claim_url`
  (https://roamzy.io/claim.html?token=rc_9tsnRcHc5-IGtRJym2861h-nEW-m7XTo shown
  in docs). Anonymous accounts have "conservative daily/monthly spending caps
  and a cool-off period" (thresholds only visible post-claim).
- **Remote endpoint**: `https://roamzy.io/mcp` (Streamable HTTP); probe from
  awesome-remote-mcp-servers CI returned
  `{"ok":true,"auth":"🔓","status":200,"server":{"name":"roamzy","version":"1.6.9"}}`
  — never answers 401, no key needed to browse *or* buy.
- **Marketplace listings** (all self-submitted by the vendor, ~61 days old):
  cline/mcp-marketplace#2193
  (https://github.com/cline/mcp-marketplace/issues/2193); tensorblock/
  awesome-mcp-servers#1580
  (https://github.com/tensorblock/awesome-mcp-servers/issues/1580); chatmcp/mcpso#3437
  (https://github.com/chatmcp/mcpso/issues/3437); punkpeye/
  awesome-remote-mcp-servers#147
  (https://github.com/punkpeye/awesome-remote-mcp-servers/pull/147). 12 tools:
  country rates, trip estimates, payment options, order placement, order status,
  eSIM status + activation QR, account, **referral**, support. Listed in the
  official MCP registry as `io.github.roamzy-io/mcp-server`; npm
  `@roamzy/mcp-server` (MIT).
- **Referral economy** (CHANGELOG 1.6.0, 2026-05-31):
  https://github.com/roamzy-io/mcp-server/blob/HEAD/CHANGELOG.md — `roamzy_referral`
  tool returns referral link + earnings; **20% of every payment from referred
  accounts, forever, paid in USDT; works in anonymous mode too**; anonymous
  agent can spend earnings on its own eSIM traffic; cashing out requires linking
  Google/Telegram identity. Vendor copy: "an agent that installs this has its
  own reason to recommend it onward."
- **Agent commerce adjacency**: x711/coinrailz (x402 micropayments) in the same
  lane-B enum — Roamzy is the concrete instance of agent-to-merchant crypto
  payment.

### Notable prior incidents / writeups
- **None found.** No abuse writeup, no security advisory, no incident record for
  Roamzy or for "agent buys eSIM" as a primitive. All public material is vendor
  marketing + MCP-directory listings.

### Observed infrastructure data (stored/indexed only)
- Shodan `hostname:roamzy.io` count query → **0 hosts** (no Shodan-visible edge;
  likely behind CDN/WAF or no direct 443 fingerprint).
- crt.sh not queried (out of tunnel-broker scope; domain has no wildcard-user
  tunnel surface to sample).

### Novelty note — (10)
**High novelty.** Nothing in public security literature documents an agent
purchasing anonymous, no-KYC mobile identities (MSISDN eSIMs) with crypto via
MCP. The vendor openly advertises the anonymous-first flow and the
referral-forever incentive ("agents earn 20% ... including anonymous ones"),
which is a self-propagating agent-commerce loop — an agent with a wallet can
acquire telecom identity with no human, no KYC, and is economically incentivized
to onboard other agents. The identity-adjacent framing (anonymous eSIM =
  disposable attested identity for OTPs/accounts) is our study's, not the
  vendor's. **Verdict: novel — no prior publication; this is a genuinely new
  agent-egress primitive in the public record.**

---

## Cross-cutting observations
- Of the four, only (7)-adjacent (email-MCP exfil) and (8) have substantive
  published risk material — both predate our study and cover the *risk class*,
  not our *specific findings*.
- (9) LocalCan and (10) Roamzy have **zero** security-oriented public writeups;
  both vendors self-document the agent capability openly as a feature.
- Atomic Mail's PoW anti-abuse and Roamzy's anonymous spending caps show vendors
  are thinking about abuse, but the agent-operated channel itself is the
  unexamined part.
- No secrets, credentials, or human/operator identifiers were encountered or
  recorded in this lane. All values above are service infrastructure or
  vendor-published.
