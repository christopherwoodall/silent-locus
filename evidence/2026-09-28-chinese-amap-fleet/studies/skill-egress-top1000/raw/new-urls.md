# NEW-URL — novel domains in skill-egress top-1000 lanes (f1/f2/f3/h1/h2) vs top-500 lanes (c/d/e)

Generated 2026-10-05 by NEW-URL (analysis worker). Static analysis only; no URL was fetched or executed.

## 1. Method + counts

**Extraction.** `grep`-equivalent URL scan (`https?://` regex) over text source files
(`*.md *.ts *.js *.py *.go *.json *.yaml *.yml *.toml *.sh *.tsx *.jsx *.rs` plus
`*.txt *.html *.mjs *.cjs *.rb *.php`), skipping `node_modules/.git/dist/build/__pycache__/.venv/venv/target/.next`.
Host → registrable domain via eTLD+1 heuristic: last two labels, except a built-in list of
common two-part public suffixes (co.uk, com.au, co.jp, …) and known PaaS suffixes
(workers.dev, pages.dev, vercel.app, onrender.com, fly.dev, azurewebsites.net, …).
Occurrence = URL-mention count (not distinct URLs). Skill identity = `lane/<repo-dir>`.

| Set | Lanes | Skill repos | Files with URLs | URL mentions | Unique domains |
|---|---|---|---|---|---|
| NEW | f1 (46) f2 (93) f3 (69) h1 (16) h2 (49) = 273 | 273 | 55,975 | 473,982 | 8,103 |
| KNOWN (top-500) | c (67) d (65) e (45) = 177 | 177 | 25,528 | 393,559 | 6,751 |
| **NOVEL (NEW − KNOWN)** | — | — | — | — | **6,088** |

**Reading guidance (OBSERVED vs INFERENCE).**
- OBSERVED: the counts, the file paths, the quoted line contexts — all from static bytes.
- INFERENCE: the class labels and "cousin" judgments — my classification, marked as such.
- **Occurrence ranking is volume-driven, not risk-driven.** One skill,
  `lane-f1/jeremylongshore-tons-of-skills-marketplace` (a 434-plugin marketplace with an
  ~85k-line `marketplace/src/data/skills-catalog.json`), contributes the majority of top-rank
  mentions. Most top-40 domains are vendor self-domains or SaaS API/doc links inside its
  vendored packs — novel, but not tradecraft. The actual prize (new primitives) is in
  sections 3 and 4.
- "Novel" means absent from the c/d/e *source dirs*, not absent from the top-500 *study*:
  e.g. `loca.lt` appears in the top-500 recon notes but not in c/d/e bytes, so it is novel here.

## 2. Top 40 novel domains by occurrence (class + evidence)

Class key: anon-file-host / relay-proxy / tunnel-broker / webhook-or-messaging / email /
paste / archive / package-registry / cloud-api / ai-api / other.

| # | Domain | Occ | Skills | Class | Evidence (observed file context) |
|---|---|---|---|---|---|
| 1 | munderdiffl.in | 7790 | 1 | other | Vendor self-domain. `HarnessMD-munder-difflin/CHANGELOG.md:344`, `README.md:38` — "Munder Difflin … a clone of you"; badges link `https://munderdiffl.in/blog/`. |
| 2 | tonsofskills.com | 2929 | 1 | other | Marketplace self-domain. `jeremylongshore-tons-of-skills-marketplace/CLAUDE.md:7` — "Claude Code plugins marketplace. Live at https://tonsofskills.com". |
| 3 | intentsolutions.io | 2344 | 1 | other | Vendor contact domain. `.claude-plugin/marketplace.json:49` — `"email": "jeremy@intentsolutions.io"` (repeated across plugin manifests). |
| 4 | jeremylongshore.com | 2232 | 1 | other | Author portfolio/blog. `000-docs/247-OD-CHNG-changelog.md:2231`, 400+ blog-post canonicals under `marketplace/src/content/blog-posts/`. |
| 5 | verisign.com | 1559 | 2 | other | (a) RDAP: `OpenOSINT-OpenOSINT/tests/test_rdap.py:23` — `https://rdap.verisign.com/com/v1/`; (b) cert strings: `BlackSnufkin-LitterBox/Scanners/HolyGrail/Policies/lol_drivers.json:1200` — VeriSign Class 3 Code Signing CA subject. |
| 6 | openevidence.com | 1210 | 1 | cloud-api | SaaS pack docs. `plugins/saas-packs/openevidence-pack/skills/openevidence-ci-integration/SKILL.md:89` — `[OpenEvidence User Guide](https://www.openevidence.com/user-guide)`. |
| 7 | withpersona.com | 849 | 2 | cloud-api | **KYC/identity API.** `internet-court-internet-court-skill/vendored/sendaifun/squads/resources/grid-api-reference.md:149` — `"kycUrl": "https://withpersona.com/verify?inquiry-id=inq_..."`. Also in tons-of-skills catalog. |
| 8 | techsmith.com | 742 | 1 | cloud-api | Docs assets. `plugins/saas-packs/techsmith-pack/README.md:49` — `https://assets.techsmith.com/Docs/Snagit-2025-COM-Server-Guide.pdf`. |
| 9 | transcend.io | 649 | 1 | cloud-api | Privacy-platform OAuth + docs. `transcend-io-tools/CONTRIBUTING.md:267` — OAuth redirect registration at `https://app.transcend.io/admin/oauth-clients`. |
| 10 | worktrunk.dev | 645 | 1 | other | Vendor self-domain. `max-sixty-worktrunk/Cargo.toml:64` — `homepage = "https://worktrunk.dev"`. |
| 11 | quicknode.com | 635 | 1 | cloud-api | Blockchain RPC docs. `internet-court-internet-court-skill/vendored/quicknode/quicknode-skill/SKILL.md:138` — `https://www.quicknode.com/chains`. |
| 12 | befailproof.ai | 627 | 1 | other | Vendor self-domain. `FailproofAI-failproofai/README.md:11` — `https://discord.befailproof.ai/` badge. |
| 13 | startaitools.com | 585 | 1 | other | Author blog. `000-docs/247-OD-CHNG-changelog.md:2176` — post canonicals `https://startaitools.com/posts/…`. |
| 14 | flexport.com | 576 | 1 | cloud-api | Logistics API. `plugins/saas-packs/flexport-pack/README.md:19` — `https://api.flexport.com` + `Flexport-Version` header model. |
| 15 | lokalise.com | 521 | 1 | cloud-api | Translation API. `plugins/saas-packs/lokalise-pack/README.md:72` — API base `https://api.lokalise.com/api2`. |
| 16 | getbb.app | 512 | 1 | other | Vendor app domain. `get-bb-bb/apps/ai-gateway/src/upstream.ts:75` — `"HTTP-Referer": "https://getbb.app"`. |
| 17 | youmind.com | 505 | 1 | ai-api | AI prompt gallery. `jnMetaCode-agency-orchestrator/scripts/import-creative-extra.mjs:11` — gallery `https://youmind.com/nano-banana-pro-prompts`. |
| 18 | coss.com | 494 | 2 | other | UI component registry. `alpic-ai-skybridge/packages/devtools/components.json:22` — `"@coss": "https://coss.com/ui/r/{name}.json"`; `crafter-station-petdex/.agents/skills/coss-particles/SKILL.md:12`. |
| 19 | aihubmix.com | 468 | 1 | ai-api | **API-key reseller.** `qixing-jk-all-api-hub/README.md:271` — listed with affiliate link `https://aihubmix.com/?aff=W3DN` among "Specialized account platforms". |
| 20 | lindy.ai | 458 | 1 | ai-api | Agent platform docs. `marketplace/src/data/vendor-packs.json:551` — `"docsUrl": "https://docs.lindy.ai"`. |
| 21 | bruniaux.com | 412 | 1 | other | Author domain. `FlorianBruniaux-claude-code-ultimate-guide/AGENTS.md:38` — `https://cc.bruniaux.com/whitepapers/`. |
| 22 | tonone.ai | 391 | 1 | other | Marketplace mirror. `.claude-plugin/marketplace.json:7762` — `"url": "https://tonone.ai"`. |
| 23 | hubapi.com | 389 | 1 | cloud-api | HubSpot CRM API. `plugins/saas-packs/clay-pack/skills/clay-advanced-troubleshooting/SKILL.md:161` — `https://api.hubapi.com/crm/v3/objects/contacts`. |
| 24 | codeberg.org | 361 | 1 | other | Code forge. `silexlabs-Silex/desktop/src-tauri/src/integrations/common/remote.rs:74` — host-part example `https://codeberg.org/x/y`. |
| 25 | dbcode.io | 361 | 1 | other | Vendor self-domain. `vsc-dbcode-dbcode/extension/sbom.cdx.json:17` — `"url": "https://dbcode.io"`. |
| 26 | documenso.com | 353 | 1 | cloud-api | E-sign API/docs. `plugins/saas-packs/documenso-pack/README.md:77` — `https://docs.documenso.com`. |
| 27 | alchemy.com | 348 | 1 | cloud-api | Blockchain RPC template. `internet-court-internet-court-skill/vendored/pnp/pnp-solana/SKILL.md:688` — `https://solana-mainnet.g.alchemy.com/v2/YOUR_KEY`. |
| 28 | cast.ai | 346 | 1 | cloud-api | K8s platform docs. `plugins/saas-packs/castai-pack/README.md:72` — `https://docs.cast.ai/docs/getting-started`. |
| 29 | get-ryze.ai | 346 | 1 | other | Vendor self-domain. `Ryze-AI-Adgent-open-seo-mcp-skills/README.md:3`, `.claude-plugin/marketplace.json:5`. |
| 30 | canva.dev | 345 | 1 | cloud-api | Canva Connect docs. `plugins/saas-packs/canva-pack/README.md:75` — `https://www.canva.dev/docs/connect/`. |
| 31 | youtube-nocookie.com | 343 | 2 | other | Embed allowlists. `crbnos-carbon/.ai/plans/2026-09-28-csp-csrf.md:67` — CSP `frame-src … https://www.youtube-nocookie.com`; `0xMassi-webclaw` security lib. |
| 32 | silex.me | 320 | 1 | other | Vendor self-domain. `silexlabs-Silex/README.md:10` — `https://www.silex.me/download/`, `https://v3.silex.me/`. |
| 33 | sap.com | 317 | 1 | other | SAP docs links. `crbnos-carbon/.ai/research/2026-07-19-co-part-consolidation.md:63` — `https://help.sap.com/doc/…`. |
| 34 | granola.ai | 287 | 1 | cloud-api | Meeting-notes API. `plugins/saas-packs/granola-pack/README.md:13` — Granola API integration pack. |
| 35 | carbon.ms | 287 | 1 | other | Vendor self-domain. `crbnos-carbon/README.md:2` — `<a href="https://carbon.ms">`; `sst.config.ts:29` — `itar.carbon.ms`. |
| 36 | servicegraph.co | 281 | 1 | other | Marketplace URL. `.claude-plugin/marketplace.json:8106` — `"url": "https://servicegraph.co"`. |
| 37 | wellally.tech | 281 | 1 | cloud-api | Health-data API. `FreedomIntelligence-OpenClaw-Medical-Skills/skills/wellally-tech/SKILL.md:3` — Apple Health/Fitbit/Oura import + WellAlly.tech knowledge base. |
| 38 | nitrostack.ai | 277 | 1 | other | Vendor self-domain. `nitrocloudofficial-nitrostack/README.md:2`, `.github/FUNDING.yml:4`. |
| 39 | skybridge.tech | 272 | 1 | other | Vendor docs domain. `alpic-ai-skybridge/README.md:4` — `https://docs.skybridge.tech`. |
| 40 | navan.com | 265 | 1 | cloud-api | Travel API pack. `plugins/saas-packs/navan-pack/README.md:7` — `https://navan.com/integrations`, status/security links. |

## 3. Cousin flags — new domains in the same families as top-500 primitives (INFERENCE)

Top-500 primitive families for reference: ngrok/cloudflared/localcan/trycloudflare/loca.lt/serveo/pinggy
(tunnels) · r.jina.ai (relay) · discord/slack/telegram/webhook.site (dead-drop/messaging) ·
catbox.moe/litterbox/uploads.github.com (anon file hosts) · sci-hub.se · JMAP email.

**Tunnel brokers**
- `ngrok.app` (occ 5, 1 skill) — OBSERVED: `lane-f2/MCPJam-inspector/…/chat-v2/thread/mcp-apps/__tests__/…:3418`
  `const origin = "https://api.tommy-local.ngrok.app"` and `…/ServerConnectio…:43`
  `url: "https://rotated.ngrok.app/api/mcp/adapter-http/test-server?k=newsecret"`.
  INFERENCE: ngrok's current tunnel-endpoint domain (successor to ngrok.io) showing up as
  MCP adapter test fixtures — the skill's tests assume agents reach MCP servers over ngrok.
- `loca.lt` (occ 3, 1 skill) — OBSERVED: tons-of-skills `vercel-webhooks-events/SKILL.md:227`
  "# Gives you a public URL like https://xxx.loca.lt". INFERENCE: localtunnel taught as the
  webhook-receiver exposure path — cousin of the LocalCan tunnel primitive.

**Relay proxies**
- `zread.ai` (occ 3, 3 skills) — OBSERVED: `samber-cc-skills-golang/skills/golang-documentation/references/library.md:210`
  "zRead — <https://zread.ai> — developer documentation reader";
  `rebelytics-one-skill-to-rule-them-all/README.md:155`; `CYB3RMX-Qu1cksc0pe`.
  INFERENCE: a jina-style reader/relay service, now referenced by 3 separate skills —
  the first relay cousin of r.jina.ai in the skill supply chain.

**Anon / decentralized file hosts**
- `kleros-ipfs-gateway.fly.dev` (occ 13, 1 skill) — OBSERVED:
  `internet-court-internet-court-skill/vendored/kleros/kleros-ipfs-upload/SKILL.md:8`
  "Upload Kleros-ecosystem files to IPFS via `https://kleros-ipfs-gateway.fly.dev/upload-to-ipfs`,
  an x402-protected gateway that charges $0.01 USDC per upload on Base mainnet. The returned
  IPFS CID is c…" INFERENCE: a crypto-micropayment IPFS upload endpoint shipped as a skill's
  canonical upload path — a new-model file-host primitive (decentralized, pay-per-upload).
- `r2.dev` (occ 20, 3 skills) — OBSERVED: `UfoMiao-zcf/src/utils/ccr/presets.ts:3`
  `const PROVIDER_PRESETS_URL = 'https://pub-0dc3e1677e894f07bbea11b17a29e032.r2.dev/providers.json'`;
  `crafter-station-petdex/next.config.ts:12` `CANONICAL_R2_PUBLIC_HOST = "assets.petdex.dev"`;
  `glidea-zenfeed/docs/podcast.md:52` (R2 public-access docs, Chinese).
  INFERENCE: Cloudflare R2 public buckets (`pub-*.r2.dev`) used as no-auth asset/config hosts —
  functionally an anon file host inside agent tooling.
- `plannotator.workers.dev` (occ 10, 1 skill) — OBSERVED: `backnotprop-plannotator/AGENTS.md:150`
  `PLANNOTATOR_PASTE_URL` — "Base URL of the paste service API for short URL sharing.
  Default: `https://plannotator-paste.plannotator.workers.dev`."
  INFERENCE: a self-hosted encrypted paste/file-share service (AES-256-GCM, key in URL
  fragment, PrivateBin-model per its README) deployed on Cloudflare Workers and shipped
  as the skill's default share endpoint. Straddles paste + anon-file-host.

**Paste**
- `pastebin.com` (occ 15, 1 skill) — OBSERVED: `OpenOSINT-OpenOSINT/README.md:262`
  `"[+] https://pastebin.com/aB1cD2eF (2023-04-12)"` and `PLAN_PLAYBOOKS_2.md:211`
  (OSINT result-line examples). INFERENCE: paste primitive present in OSINT skill context;
  the top-500 lanes had no pastebin-family domain.
- `privatebin.info` (occ 2, 1 skill) — OBSERVED: plannotator README/docs cite PrivateBin
  as the model for its own encrypted sharing. Cousin reference, not usage.
- `rentry.org` (occ 1, 1 skill) — OBSERVED: unsloth llama-cpp guide link
  `https://rentry.org/llama-cpp-conversions#merging-loras-into-a-model`. Reference only.

**Archive**
- `archive.is` (occ 1, 1 skill) — OBSERVED: `RefoundAI-lenny-skills/skills/defining-product-strategy/references/artifacts.md:994`
  `2. Tesla (https://archive.is/ypo0q)`. INFERENCE: archive.today-family shortlink in use;
  only archive-family cousin found (top-500 had Wayback only).

**Webhook / messaging**
- `svix.com` (occ 3, 1 skill) — OBSERVED: `crbnos-carbon/.ai/research/2026-07-31-workflows-run-history.md:1805`
  `<https://docs.svix.com/retention>`. INFERENCE: webhooks-infrastructure provider (Svix)
  in agent workflow research — the "send webhooks reliably" cousin of raw webhook.site.
- `discordapp.com` (occ 3, 2 skills) — OBSERVED: `MCPJam-inspector/server/__tests__/in-app-browser.test.ts:115`
  Discordbot UA `+https://discordapp.com`; `YaoApp-yao/integrations/discord/convert_test.go:82`
  `https://cdn.discordapp.com/attachments/test.png`. INFERENCE: Discord CDN + crawler UA —
  messaging-family surface in test fixtures.
- `javascript-webhook-prod.onrender.com` (occ 1, 1 skill) — OBSERVED:
  `transcend-io-tools/packages/cli/examples/classifications.yml:91`
  `url: https://javascript-webhook-prod.onrender.com/transcend/enrichment`.
  INFERENCE: a deployed example webhook-receiver endpoint (Render-hosted) shipped in CLI
  examples — shows the webhook-receiver pattern being distributed as config, not just docs.
- `webhooks.fyi` (occ 2, 1 skill) — OBSERVED: tons-of-skills klingai webhook skill links
  `[Webhook Security Best Practices](https://webhooks.fyi/security/hmac)`. Docs reference only.

**Email**
- `mailgun.net` (occ 3, 1 skill) — OBSERVED: `YaoApp-yao/messenger/providers/mailgun/mailgun.go:74`
  `provider.baseURL = "https://api.mailgun.net/v3"`. INFERENCE: transactional-email API
  wired as a provider in a multi-provider messenger kit (see §4).
- `mcpagentmail.com` (occ 2, 1 skill) — OBSERVED:
  `777genius-agent-teams-ai/docs/research/inter-agent-communication-standards.md:325-331`
  (Russian) — "MCP-сервер, предоставляющий 34 tool для координации агентов" (MCP server
  providing 34 tools for agent coordination); site `https://mcpagentmail.com/`,
  GitHub `Dicklesworthstone/mcp_agent_mail`. INFERENCE: agent-to-agent email/inbox
  coordination service — email-family primitive aimed at agent swarms.
- `fastmail.com` (occ 13, 2 skills) — OBSERVED:
  `0xMassi-webclaw/targets_1000.txt:813` — `Fastmail|https://www.fastmail.com/|fastmail,email,privacy`;
  `ridafkih-keeper.sh/…/caldav-connect-form.tsx:26` — `serverUrl: "https://caldav.fastmail.com/"`.
  INFERENCE: Fastmail appears as a *named target* in webclaw's 1,000-target recon list
  (email/privacy tag) and as a CalDAV endpoint — email-recon surface, not just a provider link.

**AI API routers / resellers (new ai-api sub-family)**
- `aihubmix.com` (468), `anyrouter.top` (46), `agentrouter.org` (76), `ai-router.dev` (135),
  `qixing1217.top` (129) — OBSERVED: `qixing-jk-all-api-hub/README.md:267-271`
  (Chinese + English) list these as "Specialized account platforms and compatible
  implementations" with affiliate-tagged register links (`?aff=tDKX`, `?aff=TUX6`, `?aff=W3DN`);
  `.scratch/ai-router-adaptation/` contains a full "ai-router.dev 现场调查" (field survey) +
  adaptation spec. INFERENCE: a skill ("all-api-hub") whose job is routing users to
  third-party API-key resellers — supply-chain-adjacent monetization inside agent tooling.

**Other notables**
- `ts.net` (occ 222, 1 skill) — OBSERVED: `mbailey-voicemode/.claude/skills/impressions/docs/setup.md:48`
  `VOICEMODE_MLX_AUDIO_BASE_URL=http://ms2.your-tailnet.ts.net:8890/v1`.
  INFERENCE: Tailscale tailnet endpoint — agent voice skill phoning a tailnet-hosted
  inference server. Network-topology primitive, not exfil per se.
- `pm-claude-skills.workers.dev` (occ 69, 1 skill) — OBSERVED:
  `mohitagw15856-pm-claude-skills/OPERATIONS.md:16`
  "Hosted MCP connector | https://pm-skills-mcp.pm-claude-skills.workers.dev/".
  INFERENCE: a live Cloudflare-Workers-hosted MCP connector shipped as the skill's
  ChatGPT/Claude.ai integration path.
- `models.dev` (occ 19, 3 skills) — OBSERVED: `redhat-et-ripwire/test/fixtures/opencode-config.schema.json:174`
  `"$ref": "https://models.dev/model-schema.json#/$defs/Model"`;
  `jnMetaCode-agency-orchestrator/web/server.js:406` (Chinese) "models.dev 公开模型目录
  （cc-switch 同款数据源）" (public model directory, same data source as cc-switch).
  INFERENCE: a model-catalog API consumed as a live data source by agent tooling.
- `withpersona.com` (849, 2 skills) — KYC/identity verification API endpoint in a skill's
  vendored API reference (see table #7). Identity-adjacent, not exfil — flagged for the
  why-analysis lane.

**Test-fixture false positives (downgraded, kept for the record)**
- `slack.com.co`, `hooks-slack.com`, `evilslack.com` (occ 1 each) — lookalike-domain
  rejection *tests* (`rullerzhou-afk-clawd-on-desk/test/slack-notify-settings.test.js:79`,
  `mvschwarz-openrig/packages/daemon/test/slack-inbound-files.test.ts:228`
  "a lookalike domain is REJECTED before any request"). Not real egress.
- `omb-u-*.fly.dev` — OpenMausBot cloud-instance origins; all but one are obvious
  fixtures (`omb-u-0123456789ab`, `omb-u-ffffffffffff`, `omb-u-fixture`, `omb-u-new`,
  `omb-u-other`); one realistic-looking (`omb-u-1a2b3c4d5e6f.fly.dev` in docs/cloud-pro.md
  with `"pairingAvailable": true`).
- `reasonix.io` (4) — matched an `ix.io` substring; actually the Reasonix CLI company. FP.
- `ifttd.io` (97) — "If This Then Dev" podcast link, not IFTTT. FP.
- `wormholescan.io` (9) — Wormhole *blockchain bridge* explorer API, not the file-transfer
  Wormhole. FP.

## 4. Multi-skill spread (supply-chain signal)

476 novel domains appear in ≥2 distinct skill repos. Ranked by distinct-skill count
(then occurrence). `*.example` / `*.invalid` / `*.test` / `*.local` placeholders are
test-fixture noise and listed separately.

**3-skill novel domains (highest spread):**
- `r2.dev` (20) — f2/glidea-zenfeed, f3/UfoMiao-zcf, f3/crafter-station-petdex (see §3).
- `models.dev` (19) — f2/777genius-agent-teams-ai, f2/jnMetaCode-agency-orchestrator, f2/redhat-et-ripwire (see §3).
- `zread.ai` (3) — f1/rebelytics-one-skill-to-rule-them-all, f1/samber-cc-skills-golang, f2/CYB3RMX-Qu1cksc0pe (see §3).
- `alpic.ai` (142) — f2/777genius-agent-teams-ai, f2/MCPJam-inspector, f2/alpic-ai-skybridge (skybridge ecosystem cross-refs).
- `digitalocean.com` (31) — f3/milind-soni-OpenMausBot, h2/transcend-io-tools, h2/vsc-dbcode-dbcode (deploy docs).
- `tiptap.dev` (28) — f2/MCPJam-inspector, f2/crbnos-carbon, f3/genspark-ai-genoffice (editor lib).
- `babeljs.io` (46), `swc.rs` (7), `oxc.rs` (4), `jqlang.org` (7) — build-tool docs shared across JS skills.
- `a2a-protocol.org` (8) — f1/internet-court, f1/tons-of-skills, f2/777genius (agent-to-agent protocol docs).
- `anaconda.com` (10) — f1/foryourhealth111-pixel-Vibe-Skills, f3/FlorianBruniaux-guide, f3/loopx-project-loopx.
- `blueoakcouncil.org` (10) — license texts (f3/AgriciDaniel-claude-ads, f3/open-gsd-gsd-core, h2/vsc-dbcode-dbcode).
- `terraform-best-practices.com` (5), `stackoverflow.co` (4), `greptile.com` (4), `cwi.nl` (3), `psu.edu` (3), `moz.com` (3), `semrush.com` (3) — reference/doc links.
- `electronjs.org` (61), `js.foundation` (6), `llama.com` (3), `printer.local` (9), `x.x` (8), `100.1` (7), `1.4` (4) — docs, mDNS/test hosts, version-string FPs.
- Placeholder noise (test fixtures, not signal): `untrusted.example`, `registry.example`, `runtime.example`, `good.example`, `example.internal`, `internal.test`, `elsewhere.invalid`, `unreachable.invalid`, `unknown.example`, `wrong.example`, `images.example`, `issuer.example`, `server.example`, `custom-endpoint.com`, `wiki.internal`, `another.com`, `original.com`.

**2-skill novel domains (selected, by occurrence):**
- `verisign.com` (1559) — f2/BlackSnufkin-LitterBox + f2/OpenOSINT-OpenOSINT.
- `withpersona.com` (849) — f1/internet-court + f1/tons-of-skills.
- `coss.com` (494) — f2/alpic-ai-skybridge + f3/crafter-station-petdex.
- `youtube-nocookie.com` (343) — f2/0xMassi-webclaw + f2/crbnos-carbon.
- `unsloth.ai` (246) — f1/foryourhealth111-pixel-Vibe-Skills + f3/FlorianBruniaux-guide (fine-tune docs).
- `inkeep.com` (208) — f2/samanhappy-mcphub + f2/inkeep-agents (AI support-agent platform).
- `kimi.ai` (84) — f1/rebelytics + f3/FlorianBruniaux-guide (Moonshot AI resources).
- `height.app` (95), `netflix.com` (103), `novell.com` (101), `xamarin.com` (101), `ryanjuckett.com` (88) — vendor/doc links.

**One-skill multi-provider kit (worth flagging despite single-repo count):**
- `lane-f3/YaoApp-yao` wires a full messenger/email provider matrix in one skill:
  `messenger/providers/` = mailer, **mailgun** (novel: `api.mailgun.net/v3`), twilio,
  dingtalk, discord, feishu, telegram, weixin (+ `integrations/discord`).
  All except mailgun were already in the KNOWN set — the kit itself is the signal:
  a single skill giving an agent send-capability across 8 messaging/email providers.

## Corpus-grammar check (hunt-corpus markers in NEW-lane URLs)

- `zz=` URL params: **ZERO hits** across all new lanes.
- `A000`/`ZZEND`: 10 files hit, all verified benign — `A0001` in
  `FreedomIntelligence-OpenClaw-Medical-Skills/skills/bio-motif-search/examples/motif_files.py`
  (motif/sequence ID) and `A000001` in tons-of-skills guidewire `API_REFERENCE.md`
  (insurance policy-number format). No `A000-ZZEND` task-label grammar.
- 10-digit numerics inside URLs: only benign — cron `scheduledTime=1704067200000`,
  Discord channel/message IDs, Figma article IDs, git SHAs, Ethereum addresses,
  X status IDs, LinkedIn activity IDs. No epoch-nonce parameters observed.
- Verdict: matches the top-500's clean negative — **no agent-grammar markers
  (epoch nonces / zz labels / A000-ZZEND) anywhere in the new lanes either.**

## Caveats

1. Occurrence = mention volume; the tons-of-skills mega-catalog dominates ranks 1–40.
   Multi-skill spread (§4) is the better supply-chain signal.
2. eTLD+1 heuristic is approximate (two-part-suffix list + PaaS suffixes); `www.` vs bare
   and `api.` subdomains are merged by construction.
3. Skill identity = repo directory; `internet-court` and `tons-of-skills` contain vendored
   sub-skills, so "1 skill" can still mean broad distribution.
4. Scanner SKIP_EXT binary types were excluded implicitly by extension allowlist;
   minified bundles inside allowed extensions were still scanned (their URLs count).
5. Nothing here was fetched or executed; classes are INFERENCE from static context.
