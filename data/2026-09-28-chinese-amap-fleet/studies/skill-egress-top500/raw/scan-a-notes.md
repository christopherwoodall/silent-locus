# Lane C — fetch + scan notes (Claude skills batch)

Date: 2026-10-05. Work dir: `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/studies/skill-egress-top500/`
Scanner output: `raw/scan-a.json`. Clones live in `~/workspace/skill-egress-work/lane-c/` (NEVER committed).

## Method

- Scanner: `~/workspace/muse-home/projects/skill-tracer/scan/egress_scan.py` (run verbatim, not re-derived):
  `python3 egress_scan.py ~/workspace/skill-egress-work/lane-c --out raw/scan-a.json`
- Taxonomy: `~/workspace/muse-home/projects/skill-tracer/egress-taxonomy.md`
  (img_upload CRITICAL · webhook HIGH · relay HIGH · paste MEDIUM · registry MEDIUM ·
  creds HIGH · gitwrite MEDIUM · tunnel CRITICAL · corpus MEDIUM · email HIGH ·
  dns MEDIUM · browser HIGH · netcall MEDIUM)
- Scoring: 3×CRITICAL + 2×HIGH + 1×MEDIUM → CRITICAL ≥10 · HIGH ≥6 · MEDIUM ≥3 · LOW ≥1 · NONE 0
- Grades per hit: `confirmed` (bytes present in skill) / `pattern-match` (corpus tradecraft grammar).
  Scanner does not grade `capability`; I add that grade manually in this file where warranted.
- All clones shallow (`git clone --depth 1`), public repos only, read-only, no interaction, no commits/pushes.
- Corpus-indicator watchlist (flag on sight): r.jina.ai, webhook.site/discord/slack webhooks,
  httpbun/httpbin, uploads.github.com gitshot flows, ComposioHQ ngrok-automation, epoch nonces,
  zz labels, go-import tags, verify=False.

## Fetch registry

| # | repo | stars | why fetched | status |
|---|------|-------|-------------|--------|
| 1 | anthropics/skills | — | official Anthropic skills (all skill dirs) | cloned OK |
| 2 | obra/superpowers | — | canonical agent workflow skills | cloned OK |
| 3 | ComposioHQ/awesome-claude-skills | 76,514 | top-starred list; 864 SKILL.md files; contains ngrok-automation | cloned OK |
| 4 | travisvn/awesome-claude-skills | 15,270 | top-starred list (link-only) | cloned OK |
| 5 | mvanhorn/last30days-skill | — | v1 CRITICAL-64: r.jina.ai keyless fetch fallback | fetched OK via codeload tarball (git protocol kept disconnecting) |
| 6 | lackeyjb/playwright-skill | — | browser-automation skill (taxonomy §12) | cloned OK |
| 7 | jthack/ffuf_claude_skill | — | security fuzzer skill | cloned OK |
| 8 | LewisLiu007/full-page-screenshot | — | screenshot skill (gitshot-adjacent) | cloned OK |
| 9 | anandpareek-hub/pixelbin-claude-skill | — | image-host (pixelbin) skill | cloned OK |
| 10 | haunchen/n8n-skills | — | n8n webhook-automation skills | cloned OK (0 SKILL.md — TS generator repo; node catalog under data/cache/) |
| 11 | jthack/threat-hunting-with-sigma-rules-skill | — | security skill | DROPPED — repo 404s on GitHub (deleted/renamed); jthack/ffuf already covers this author |
| 10 | haunchen/n8n-skills | — | n8n webhook-automation skills | cloned OK (0 SKILL.md; TS generator) |
| 11 | jthack/threat-hunting-with-sigma-rules-skill | — | security skill | DROPPED — GitHub 404 |
| 12 | trailofbits/skills | 7,369 | security-firm skills | cloned OK (85 SKILL.md) |
| 13 | SimoneAvogadro/android-reverse-engineering-skill | 7,975 | reverse-engineering skill | cloned OK (1 SKILL.md, retry after proxy abort) |
| 14 | alirezarezvani/claude-skills | 27,626 | top-starred collection | cloned OK (846 SKILL.md) |
| 15 | virgiliojr94/book-to-skill | 33,757 | top-starred | cloned OK (1 SKILL.md) |
| 16 | elementalsouls/Claude-BugHunter | 4,773 | security skill | cloned OK (83 SKILL.md) |
| 17 | P4nda0s/reverse-skills | 2,232 | reverse-engineering skills | cloned OK (7 SKILL.md) |
| 18 | tradermonty/claude-trading-skills | 3,030 | trading skills | cloned OK (94 SKILL.md) |
| 19 | vipulgupta2048/gitshot | 32 | "upload images to issues, PRs" — gitshot grammar | cloned OK (3 SKILL.md) |
| 20 | trekawek/coffee-gb | — | gitshot skill material (v1) | fetched OK via tarball (master); has .agents/skills/gitshot/SKILL.md |
| 21 | conorluddy/ios-simulator-skill | — | simulator screenshot capability | cloned OK (1 SKILL.md) |
| 22 | expo/skills | — | linked from travisvn list | cloned OK (26 SKILL.md) |
| 23 | K-Dense-AI/claude-scientific-skills | — | linked from travisvn list | fetched OK via tarball (177 SKILL.md) |
| 24 | gsd-build/get-shit-done | — | linked from travisvn list | cloned OK (0 SKILL.md — layout TBD) |
| 25 | obra/superpowers-lab | — | obra lab skills | cloned OK (4 SKILL.md) |
| 26 | obra/superpowers-skills | — | obra community skills | cloned OK (31 SKILL.md) |
| 27 | yusufkaraaslan/Skill_Seekers | — | linked from travisvn list | cloned OK (26 SKILL.md; hits all noise) |
| 28 | NeoLabHQ/context-engineering-kit | 1,748 | top-starred | cloned OK (204 SKILL.md) |
| 29 | daymade/claude-code-skills | 1,442 | top-starred | cloned OK (115 SKILL.md) |
| 30 | CharlesWiltgen/Axiom | 1,189 | top-starred | cloned OK (123 SKILL.md) |
| 31 | Aaronontheweb/dotnet-skills | 1,201 | top-starred | cloned OK (37 SKILL.md) |
| 32 | aiwithremy/claude-skills-llm-council | 2,499 | top-starred | cloned OK (1 SKILL.md) |
| 33 | chaseai-yt/claudex-loop | 2,737 | top-starred | cloned OK (6 SKILL.md) |
| 34 | zarazhangrui/codebase-to-course | 5,648 | top-starred | cloned OK (1 SKILL.md) |
| 35 | glitternetwork/pinme | 3,745 | top-starred | cloned OK (7 SKILL.md) |
| 36 | dominikmartn/nothing-design-skill | 2,806 | top-starred | cloned OK (1 SKILL.md, 0 hits) |
| 37 | BehiSecc/awesome-claude-skills | 10,212 | top-starred list | cloned OK (0 SKILL.md — link list) |
| 38 | hesreallyhim/awesome-claude-code | 55,092 | top-starred list/guide | cloned OK (0 SKILL.md — guide) |
| 39 | athola/claude-night-market | 342 | claims 186 skills | cloned OK (225 SKILL.md) |
| 40 | zhuyansen/awesome-claude-video-skills | 413 | 180 security-graded video-skill repos | cloned OK (0 SKILL.md — link list of 180 repos) |
| 41 | Prat011/awesome-llm-skills | 1,781 | list | cloned OK (31 SKILL.md) |
| 42 | karanb192/awesome-claude-skills | 534 | list | cloned OK (0 SKILL.md — link list) |
| 43 | w95/awesome-claude-corporate-skills | 230 | corporate skills list | cloned OK (166 SKILL.md) |
| 44 | danyuchn/asd-ste100-skill | 3,596 | top-starred | cloned OK (1 SKILL.md) |
| 45 | Agentchengfeng/chengfeng-videocut-skills | 3,030 | top-starred | cloned OK (8 SKILL.md) |
| 46 | agiwhitelist/auteur | 1,035 | top-starred | cloned OK (1 SKILL.md) |
| 47 | mohi-devhub/antivibe | 1,120 | top-starred | cloned OK (1 SKILL.md) |
| 48 | threerocks/hand-drawn-styles | 1,410 | top-starred | fetched OK via tarball (1 SKILL.md) |
| 49 | bevibing/tutor-skills | 1,319 | top-starred | cloned OK (2 SKILL.md) |
| 50 | onvoyage-ai/gtm-engineer-skills | 1,316 | top-starred | cloned OK (12 SKILL.md) |
| 51 | zsyggg/paper-craft-skills | 1,251 | top-starred | cloned OK (3 SKILL.md, 0 hits) |
| 52 | Spark-To-Paper-Skills/paperjury | 1,217 | top-starred | cloned OK (1 SKILL.md, 0 hits) |
| 53 | adamlyttleapps/claude-skill-app-onboarding-questionnaire | 1,211 | top-starred | cloned OK (1 SKILL.md, 0 hits) |
| 54 | alonw0/web-asset-generator | — | linked from lists | cloned OK (1 SKILL.md) |
| 55 | chrisvoncsefalvay/claude-d3js-skill | — | linked from lists | cloned OK (1 SKILL.md) |
| 56 | asklokesh/claudeskill-loki-mode | — | linked from lists | cloned OK via git (5,562 files) |
| 57 | zarazhangrui/frontend-slides | — | linked from travisvn | cloned OK (2 SKILL.md) |
| 58 | omkamal/pypict-claude-skill | — | image skill (composio list) | cloned OK (1 SKILL.md) |
| 59 | zxkane/aws-skills | — | cloud skills (composio list) | cloned OK (6 SKILL.md) |
| 60 | mhattingpete/claude-skills-marketplace | — | marketplace (composio list) | cloned OK (18 SKILL.md) |
| 61 | rampstackco/claude-skills | — | collection (composio list) | cloned OK (0 SKILL.md at root; 122 units via plugins) |
| 62 | santiago-vargas-de-kruijf/claude-overkill | — | collection (composio list) | cloned OK (1 SKILL.md) |
| 63 | emory/ASD-AuDHD-PAI-Skills | — | (composio list) | cloned OK (1 SKILL.md, 0 hits) |
| 64 | 1NickPappas/move-code-quality-skill | — | (composio list) | cloned OK (1 SKILL.md, 0 hits) |
| 65 | Anjos2/recursive-research | — | (composio list) | cloned OK (1 SKILL.md, 0 hits) |
| 66 | PleasePrompto/notebooklm-skill | — | (composio list) | cloned OK (1 SKILL.md) |
| 67 | yctimlin/mcp_excalidraw | 2,499 | top-starred | cloned OK (1 SKILL.md) |
| 68 | wshobson/agents | 40,206 | top-starred (verified exists) | cloned OK (184 SKILL.md) |

Lane A's `raw/enum-awesome.md` does not exist yet — top-starred picks made directly via `gh search repos`.

## Per-skill findings

_Graded per skill: name, repo, egress hits (category + severity + file:line + match excerpt),
grade (confirmed / pattern-match / capability). Corpus-toolkit matches flagged.
Scanner false positives (doc placeholders, `"files"` dict literals, package-lock dependency
names) are called out — score ≠ verdict._

### anthropics/skills (official; 20 skill dirs)

- **skills/claude-api** — scanner CRITICAL 93, but 82 hits are `netcall/MEDIUM` curl examples
  in API docs, 4 `creds/HIGH` are the placeholder `xoxp-new-...` in managed-agents README
  examples (verified benign placeholder, not a real token), 3 `gitwrite/MEDIUM` are `git push`
  in workflow docs. Grade: **pattern-match** (doc examples only; no executable exfil).
- **skills/webapp-testing** — scanner CRITICAL 22: 9 `browser/HIGH` + 4 `browser/MEDIUM`
  (Playwright/puppeteer refs in a testing skill). Grade: **capability** — the skill drives a
  real browser for tests; that browser can navigate anywhere.
- **skills/skill-creator** — scanner CRITICAL 11: 4 `img_upload/HIGH` are `"files"`/`FILES = {`
  dict literals in `scripts/package_skill.py:22` and docs (verified benign — skill-packaging
  file lists, no upload call). Grade: **pattern-match**, benign on review.
- **skills/mcp-builder** — MEDIUM 3 (curl examples). **skills/web-artifacts-builder** — LOW 2.
  **skills/discernment-nudge** — LOW 1. Remaining 14 skill dirs — NONE 0.
- Corpus watchlist: zero hits.

### obra/superpowers (15 skill dirs, scanned as one unit — repo root has package.json)

- Scanner CRITICAL 86: 53 `netcall/MEDIUM` (curl/wget in docs), 16 `gitwrite/MEDIUM`
  (`git push` in git-workflow skills — expected), 7 `img_upload/HIGH` all verified as
  `"files"`/`"Files"` JSON/dict literals (`.version-bump.json:2`, test scripts, writing-skills
  docs — no upload primitives), 1 `browser/HIGH` ("Playwright" mention in RELEASE-NOTES.md:940),
  1 `dns/MEDIUM`. Grade: **pattern-match** overall; no executable egress beyond documented
  git workflows. Corpus watchlist: zero hits.

### mvanhorn/last30days-skill (1 skill: skills/last30days)

- Scanner CRITICAL 64 — **corpus-relevant, verified**:
  - `relay/HIGH` **confirmed + corpus-match**: `skills/last30days/scripts/lib/web_fetch_keyless.py:4,26`
    — `JINA_READER_PREFIX = "https://r.jina.ai/"`; docstring: "Turns any URL into clean,
    JS-rendered markdown via Jina Reader's free hosted endpoint … with no API key."
    Exact jina-laundering tradecraft from the urlquery corpus, as an executable fallback tier.
  - `webhook/HIGH` **confirmed**: `skills/last30days/scripts/watchlist.py:32,34,45` —
    `hooks.slack.com` hostname match routing to `_send_slack_webhook(channel, message)`;
    non-Slack https URLs go to `_send_generic_webhook`. The destination URL is user-configured
    (`delivery_channel` setting), but the primitive — POSTing research digests to an arbitrary
    webhook — is executable code.
  - `img_upload/HIGH` **confirmed** (benign purpose): `skills/last30days/scripts/lib/transcribe.py:220`
    — `multipart/form-data` POST of audio bytes to a Whisper-compatible transcription endpoint
    (`_PROVIDER_ENDPOINTS[provider]`). Legitimate function; still a third-party upload channel.
  - `browser/HIGH`: Playwright mention in SKILL.md:740 (capability).
- Grade: **confirmed** egress primitives incl. two corpus-toolkit matches (r.jina.ai, Slack-webhook dead-drop shape).

### lackeyjb/playwright-skill (1 skill)

- Scanner CRITICAL 152: all 82 hits `browser/*` — the skill IS Playwright API docs
  (each "Playwright" mention = HIGH). Grade: **capability** — full browser automation
  (navigate, fill forms, submit) by design; score inflated by doc mentions, but the
  underlying capability is real and executable.

### LewisLiu007/full-page-screenshot (1 skill)

- Scanner CRITICAL 10: `browser/HIGH` (Puppeteer, README.md:5), `netcall/MEDIUM`
  (WebSocket + fetch in scripts/full-page-screenshot.mjs). Verified: the script drives a
  browser through a localhost proxy (`http://localhost:3456`), screenshots saved to local
  `filePath` — no external upload of screenshot bytes in the script. Grade: **capability**
  (screenshot bytes produced locally; agent could pair with any upload primitive, but the
  skill itself does not exfiltrate).

### jthack/ffuf_claude_skill (1 skill: ffuf-skill)

- Scanner MEDIUM 5: curl examples in `ffuf-skill/resources/REQUEST_TEMPLATES.md`. Fuzzer
  request templates — no egress primitives beyond doc'd HTTP client usage. Grade: **pattern-match**, benign.

### anandpareek-hub/pixelbin-claude-skill (1 skill)

- Scanner CRITICAL 11: `img_upload/HIGH` hits are `"files"`/`'files'` literals in
  package.json and scripts/seo-content.js (verified benign); `netcall/MEDIUM` fetch() calls
  in references/cdn.md and scripts/seo-content.js target the Pixelbin image-CDN API
  (upload/transform via API — legitimate skill function). Grade: **capability** — the skill's
  purpose is pushing images to a third-party image host; the upload primitive is real,
  purpose-aligned, not hidden.

### haunchen/n8n-skills (0 SKILL.md — TypeScript skill-generator repo)

- Scanner CRITICAL 162, but nearly all hits are noise: `browser/HIGH` in package-lock.json
  (dependency names stagehand/playwright/puppeteer), `email/HIGH` and `relay/MEDIUM` in
  `data/cache/community-nodes.json` / `nodes.json` — cached n8n node metadata describing the
  platform's Email/SMTP nodes and a Puppeteer code-node example using `httpbin.org/ip`
  (community-nodes.json:11238 — **corpus pattern-match**: httpbin as recon testbed, inside
  example code). Grade: **capability** — the skill generates n8n workflows, where Webhook
  Trigger / Email / HTTP Request nodes are first-class; the agent is handed a dead-drop
  construction kit. No direct exfil instruction in the generator itself.

### ComposioHQ/awesome-claude-skills (864 skill units — largest single source in lane C)

- **composio-skills/ngrok-automation** — scanner CRITICAL 36: 12 `tunnel/CRITICAL` hits, all
  "ngrok" mentions in `composio-skills/ngrok-automation/SKILL.md`. Verified: the skill instructs
  the agent to automate Ngrok tunnel operations (expose local ports publicly) via Composio's
  Rube MCP (`https://rube.app/mcp` added as an MCP server; `RUBE_MANAGE_CONNECTIONS` with
  toolkit `ngrok`). Grade: **confirmed** (tunnel tooling). Note: tunnel creation itself runs
  through the user's Composio-connected ngrok account — capability is delegated, not a
  local `ngrok` binary. Also flags an adjacent vector the taxonomy doesn't score: the skill
  requires connecting to a **third-party remote MCP server** (rube.app) — instruction and
  tool schemas arrive from outside the skill bytes.
- **webapp-testing** — CRITICAL 22 (Playwright browser automation, same shape as anthropics').
  **document-skills/pptx** — HIGH 7 (playwright + `page.goto(` in `scripts/html2pptx.js:924` —
  executable browser use for HTML→PPTX rendering). **mcp-builder** — MEDIUM 3 (axios/requests
  doc examples). **artifacts-builder** — LOW 2. **composio-skills/instantly-automation** — LOW 2
  (SMTP mention — Instantly.ai email-sending toolkit).
- **858 of 864 units scored NONE 0** — structural finding: Composio skills are API-integration
  instruction files whose network I/O is delegated to the Composio platform (managed auth,
  Rube MCP). The egress surface exists but is not visible in skill bytes — scanner-clean does
  NOT mean egress-free here.

### trailofbits/skills (86 skill units, 28 with hits)

- **plugins/firebase-apk-scanner/skills/firebase-apk-scanner** — scanner CRITICAL 59 (all
  `netcall/MEDIUM`: curl in SKILL.md + scanner.sh + references/vulnerabilities.md). Verified:
  the skill is a security-testing playbook — curl targets are the *assessed* Firebase backend
  (`https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=API_KEY`,
  `https://PROJECT_ID.firebaseio.com/.json`, firestore/storage/remoteconfig endpoints).
  Grade: **capability** — teaches the agent to make HTTP calls (incl. auth-token-bearing) to
  arbitrary Firebase backends; exfil-shaped, purpose is vuln-testing a user-supplied target.
- **plugins/modern-python/skills/modern-python** — HIGH 6: **corpus pattern-match** —
  `SKILL.md:283`: `requests.get('https://httpbin.org/ip')` in a network-check doc example.
  httpbin.org/ip as IP-echo recon is exactly the corpus testbed usage. Grade: **pattern-match**
  (doc example, not exfil).
- **plugins/culture-index/skills/interpreting-culture-index** — the `tunnel/CRITICAL` hit is
  the English word "Bore" ("Bore them with routine", conversation-starters.md:337) — **scanner
  false positive**, not the bore tunnel tool.
- **plugins/static-analysis/skills/codeql** — HIGH 8: all `"files"` dict literals in
  test_check_db_quality.py — benign, verified.
- **plugins/devcontainer-setup** CRITICAL 10 (curl to install devcontainers — check), plus
  MEDIUM/LOW: libafl, libfuzzer, review-walkthrough, mutation-testing, property-based-testing
  (SMTP mention), gh-cli, agentic-actions-auditor — mostly curl/doc examples. Full detail in
  raw/scan-a.json.
- Corpus watchlist: httpbin.org (1, pattern-match doc example). No jina/webhook/zz/epoch hits.

### elementalsouls/Claude-BugHunter (83 skill units, 72 with hits — offensive-security collection)

- **skills/offensive-osint** — scanner CRITICAL 210 (194 primitives, 8 categories). Verified
  sample: `tunnel/CRITICAL` ngrok hits are detection-side — `*.ngrok.io` subdomain-takeover
  fingerprint (probes-and-wordlists.md:346), ngrok token regex in the 48-pattern secret catalog
  (secret-patterns.md:55, SKILL.md:228); `paste/MEDIUM` (pastebin/ghostbin/rentry/hastebin in
  dork-corpus.md) are OSINT dork targets; `email/HIGH` SMTP refs are email-security audit
  tradecraft; `creds/MEDIUM` `--insecure` (SKILL.md:320) is a copy-paste curl probe flag.
  Grade: **capability** — an offensive OSINT playbook (active subdomain prefix-probing, secret
  validators that call live AWS/GitHub/Slack/JWT APIs, breach-corpus lookups, takeover checks).
  Scanner categories here mostly reflect *detection* of these primitives, not exfil use —
  called out so the score isn't misread.
- **hunt-k8s / enterprise-vpn-attack / hunt-tls-network / hunt-springboot / hunt-nextjs /
  hunt-nodejs / vmware-vcenter-attack / hunt-laravel / hunt-host-header / hunt-session /
  okta-attack** — CRITICAL 19–39, nearly all `netcall/MEDIUM` (curl one-liner probes against
  targets). **bug-bounty** — CRITICAL 18 (`gh issue/pr create` + curl — reporting workflow).
  **supply-chain-attack-recon** — CRITICAL 25 (git push + curl in recon workflows).
- Overall grade: **capability** (offensive tradecraft library; curl/DNS/SMTP probes are
  executable but target-directed, not dead-drops). Full per-skill detail in raw/scan-a.json.

### virgiliojr94/book-to-skill (1 skill)

- Scanner CRITICAL 22: all `img_upload/HIGH` hits are `files = {` dict literals in
  tests/test_book_to_skill.py (verified benign); `netcall/MEDIUM` curl hits are inside the
  repo's own defensive scanner — tools/scan_generated_skill.py matches the literal words
  curl/wget in its `_OUTBOUND_TERM` detection regex (scanner FP). Notable: the repo ships its
  own exfil-detection scanner for generated skills (`_EXFILTRATION_TERM`, `_OUTBOUND_TERM`,
  `_SENSITIVE_TERM` regexes). Grade: **none** (all FPs; defensive tooling).

### P4nda0s/reverse-skills (7 skill units)

- Findings summarized in final pass from raw/scan-a.json.

### vipulgupta2048/gitshot (3 skill units — the canonical gitshot tool, 32★)

- Scanner CRITICAL 68 (44 hits). **Confirmed — this is the corpus gitshot grammar as a product.**
  `skills/gitshot/SKILL.md:25-85` documents the agent workflow verbatim:
  - `npx gitshot screenshot.png` → `![screenshot](https://github.com/user/gitshot-images/releases/download/_gitshot/screenshot-a1b2c3d4.png)`
  - "If `gh` CLI is authenticated: Uploads to `<user>/gitshot-images` repo as a **GitHub Release Asset**. Creates the repo automatically on first use."
  - "If no `gh` CLI: Falls back to **catbox.moe** (free, no signup)."
  - Optional `CLOUDINARY_URL` / `IMGBB_API_KEY` backends.
  - Agent workflows: `screencapture -x /tmp/shot.png` → `npx gitshot /tmp/shot.png | gh pr comment 42 --body-file -`; `gh issue create --title "UI Bug" --body "$BODY"`.
- Implementation hits: `src/catbox.ts:5,24` (catbox.moe fetch-POST), `src/cloudinary.ts:54`,
  `src/imgbb.ts:35`, `src/github.ts:52` (`gh issue create`), `src/index.ts:105`.
  `browser/HIGH` = Playwright mentions in README/skill docs (screenshot capture side).
- Grade: **confirmed**. Screenshot→public-URL pipeline with GitHub release assets as the
  durable trusted-domain dead-drop (cf. lobstermane/gitshot-images from the 2026-09-29 sweep)
  and catbox.moe as the anonymous fallback. The `dns/MEDIUM` hit on `video/public/audio/bg-track.mp3`
  is binary noise; `package.json:9 "files"` is benign.
- Corpus watchlist: **uploads.github.com-adjacent flow confirmed** (release-asset upload);
  catbox.moe anon-host fallback confirmed.

### conorluddy/ios-simulator-skill (1 skill)

- Scanner MEDIUM 5: four `creds/MEDIUM` `verify=False` hits — **verified FALSE POSITIVE**:
  `eraser.erase(verify=False)` in simctl_erase.py:148 / simctl_shutdown.py:133 — a method kwarg
  ("skip verification of erase"), not TLS verification. No network calls in the skill.
  Grade: **none** (scanner FP; document for pattern-tuning).

### SimoneAvogadro/android-reverse-engineering-skill (1 skill)

- Scanner CRITICAL 12: `gitwrite/MEDIUM` = `api.github.com/repos/$Repo/releases` in
  scripts/install-dep.ps1:66 (GitHub release download for tool install — benign);
  `netcall/MEDIUM` curl in install-dep.sh (tool downloads). Grade: **pattern-match**, benign
  installer traffic.

### expo/skills (26 skill units + root; root scanned as expo-skills/expo-skills)

- **expo-skills/expo-skills** — scanner CRITICAL 75: `tunnel/CRITICAL` ngrok hits verified in
  `plugins/expo/skills/eas-simulator/references/run-your-app.md:159,251-254` and
  `troubleshooting.md:33,36` — the skill instructs `npx expo start --tunnel`, which opens an
  ngrok tunnel (or Expo's own ws-tunnel v2) exposing the local Metro dev server to physical
  devices. Grade: **confirmed** (tunnel) — purpose-aligned (device testing), but the primitive
  (public tunnel to localhost, instructed step-by-step incl. reading ngrok's API at
  127.0.0.1:4040) is exactly the taxonomy's tunnel concern. `browser/HIGH` = Playwright in
  expo-skill-eval snapshot scripts (screenshot eval harness).

### tradermonty/claude-trading-skills (94 skill units, 31 with hits)

- Top scorers all `netcall/MEDIUM`-dominant: theme-detector (48), parabolic-short-trade-planner
  (34), fxmacrodata-calendar (26), earnings-calendar (22), canslim-screener (20),
  economic-calendar-fetcher (15). Verified: `requests.get`/`fetch(` to market-data APIs
  (Financial Modeling Prep guides, ETF scanners, calendar fetchers) — **pull-direction data
  fetch**, not exfil.
- **Scanner FP documented**: `img_upload/HIGH` in earnings-calendar
  (`references/fmp_api_guide.md:229`) is `profiles = {}` — the regex `files\s*=\s*\{` matches
  the substring inside "pro**files**". Any `*files = {` variable name false-positives.
  Flag for pattern-tuning (add word boundary).
- Grade: **pattern-match** (documented API data-fetch; no dead-drop primitives observed).

### obra/superpowers-lab + obra/superpowers-skills (35 skill units, 4 with hits)

- Quiet: sharing-skills HIGH 9 (`git push` / `gh pr create` in skill-sharing docs — expected),
  remembering-conversations MEDIUM 5 (`dig` in DEPLOYMENT.md — DNS troubleshooting docs),
  mcp-cli MEDIUM 4 (Puppeteer mention), finishing-a-development-branch LOW 2 (git workflow).
  Grade: **pattern-match**, benign. No corpus indicators.

### yusufkaraaslan/Skill_Seekers (28 units, 4 with hits — all noise)

- `seekers/ui` CRITICAL 82: entirely `browser/HIGH` playwright mentions in package.json/
  package-lock.json (test dep) and `img_upload/HIGH` `"files"`/`files={` JSX props in a React
  skill-browser UI (SkillPage.tsx). The `ui/` dir is a web frontend, not a skill. Grade: **none**.
- `tests/golden/phase2/man*` — curl examples in test fixtures. Grade: **none**.

### daymade/claude-code-skills (115 skill units, 64 with hits — dense)

- **twitter-reader** — CRITICAL 36: **confirmed + corpus-match (r.jina.ai)**. 9 relay/HIGH hits:
  `twitter-reader/SKILL.md:79,110,224`, `scripts/fetch_article.py:50,63`,
  `scripts/fetch_tweet.py:38,53`, `scripts/fetch_tweets.sh:28,33`. Verified: primary fetch
  mechanism is `curl -s "https://r.jina.ai/${url}" -H "Authorization: Bearer ${JINA_API_KEY}"`
  with abuse-alleviation handling (403 AbuseAlleviationError / 402 InsufficientBalanceError
  envelopes). Jina Reader is the *primary* (not fallback) tweet/article fetcher here.
- **frontend-visual-qa** — CRITICAL 133: browser/HIGH real (Playwright visual-QA harness);
  img_upload/HIGH all `"files"` in evals/evals.json test fixtures — benign.
- **tunnel-doctor** — CRITICAL 142: dns/MEDIUM (dig/nslookup) + netcall + gitwrite — a network/
  tunnel *diagnostic* skill; primitives are diagnostic, not exfil.
- **feishu-doc-scraper** — CRITICAL 57: netcall (Feishu API fetch); img_upload/HIGH is `"files"`
  schema-field literal in check_archive_storage.py:52 — benign. Side note: the skill archives
  scraped docs to `oss://` URIs (Alibaba OSS) — cloud-object-storage upload as its archival
  function (capability; scanner has no oss:// pattern).
- **read-claude-web-conversation** — CRITICAL 45 (browser + upload-shape hits; verify in final pass),
  **transcript-fixer / asr-transcribe-to-text** (audio upload to transcription — same shape as
  last30days), **bilibili-source**, **excalidraw-use**, **cloudflare-troubleshooting**,
  **skill-creator**, **prior-work-retrieval**, **debugging-network-issues** — detail in
  raw/scan-a.json; spot-check upload targets in final pass.
- Grade: **confirmed** (twitter-reader jina); rest capability/pattern-match pending final review.

### gsd-build/get-shit-done (1 root unit — 0 SKILL.md; workflow methodology repo)

- Scanner CRITICAL 305 (208 hits: netcall 61, browser 57, gitwrite 43, img_upload 39, dns 7,
  creds 1). Verified: this is a plan-execute workflow methodology, not an exfil tool.
  - The single `creds/HIGH` hit is a **synthetic test token** in an adversarial fixture:
    `tests/fixtures/adversarial/security/context-malicious-markdown-link.md:7` contains the
    URL `https://user:ghp_AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA@example.com` (ghp_ + 36×'A',
    obviously fake, in a prompt-injection test fixture). Not a real credential; noted, never used.
    (Display-layer note: tool output renders secret-shaped strings as `<redacted>`; raw bytes
    confirmed via `od -c`.)
  - `img_upload/HIGH` all benign literals (`"files"` in package.json/tsconfig/QUICK-WINS docs,
    `FILES = {` / `files = {` in bin/lib/intel.cjs).
  - netcall/browser/gitwrite hits are workflow docs + adversarial fixtures.
- Grade: **pattern-match**, benign. Notable for the study: the repo ships adversarial
  prompt-injection test fixtures (like book-to-skill's exfil scanner — defensive tooling).

### NeoLabHQ/context-engineering-kit (204 skill units, 37 with hits)

- design-testing-strategy CRITICAL 18 ×3 variants (antigravity/plugins/skills copies):
  `browser/HIGH` = Playwright for design testing — expected, capability.
- git-notes / create-pr MEDIUM 5: `git push` / `gh pr create` in git-workflow skills — expected.
- apply-anthropic-skills MEDIUM 4: `img_upload` — check; likely `"files"` literals.
- Grade: **pattern-match**, benign. Triplicated skill trees (antigravity/, plugins/, skills/)
  inflate unit counts.

### K-Dense-AI/claude-scientific-skills (177 skill units, 58 with hits)

- **skills/lab-hardware-cad** — scanner CRITICAL 96 (32 `tunnel/CRITICAL`): **verified FALSE
  POSITIVE** — "bore" is the mechanical term ("a pocket, bore, or slot", SKILL.md:130), not the
  bore tunnel tool. All 32 hits are CAD terminology.
- **skills/pysam** — CRITICAL 74: `requests.get` to download bioinformatics reference data —
  pull-direction, benign.
- **skills/paper-lookup** — CRITICAL 35: `img_upload` = `"files"` in a Zenodo API *response-shape*
  example (references/zenodo.md:61) — benign.
- **skills/imaging-data-commons** — CRITICAL 40: `api.github.com/repos/{REPO}/releases` in
  scripts/check_version.py:124 — read-only version check, not a write. Benign.
- Rest: data-fetch skills (usfiscaldata, database-lookup, ncats-arax, onekgpd, protocolsio,
  hugging-science — HTTP clients to scientific APIs). Grade: **pattern-match**, mostly benign
  pull-direction traffic. No corpus indicators.

### trekawek/coffee-gb (5 skills in .agents/skills/)

- **.agents/skills/gitshot** — MEDIUM 4: `gh issue create` (:34,78) + `catbox.moe` (:50).
  The SKILL.md is **byte-identical** to vipulgupta2048/gitshot's — same release-asset flow
  (`github.com/user/gitshot-images/releases/download/_gitshot/...`), same catbox.moe fallback,
  same `screencapture → npx gitshot → gh pr comment` agent workflows. Grade: **confirmed** —
  the gitshot exfil grammar propagates verbatim across repos (this is the "skill material in
  trekawek/coffee-gb" cited in skill-tracer v1).

### CharlesWiltgen/Axiom (scanned as 1 root unit — repo root has package.json; 123 SKILL.md inside)

- Scanner CRITICAL 500 (470 primitives: netcall 409, dns 30, img_upload 25, email 3, browser 2,
  gitwrite 1). Verified sample: `img_upload/HIGH` all `"files"` literals (package.json files-arrays,
  inventory-sha256.json, pbxproj fixtures — benign); `email/HIGH` SMTP mentions are Apple
  Network-framework docs in axiom-networking/networking-discipline.md:296 (×3 harness copies —
  benign); no webhook/relay/tunnel/corpus/paste/registry hits. The netcall/dns mass is the
  framework's own networking codebase (multi-harness agent framework).
- Grade: **pattern-match** — extensive networking surface by design; no dead-drop primitives
  observed. Score is volume-driven, not signal-driven.

### Aaronontheweb/dotnet-skills (37 skill units)

- playwright-ci-caching CRITICAL 118 / playwright-blazor CRITICAL 36 / aspire-integration-testing
  CRITICAL 24: `browser/HIGH` = Playwright (CI caching, Blazor testing — expected).
- aspire-mailpit-integration CRITICAL 25: `email/HIGH` SMTP/sendmail — Mailpit is a local
  SMTP testing tool (Aspire integration); the skill wires a fake SMTP server for tests.
  Grade: capability (email-sending primitive, test-scoped).
- microsoft-extensions-configuration CRITICAL 16: SMTP mentions in config docs.
- Grade: **capability** (browser automation + test SMTP); benign purpose.

### aiwithremy/claude-skills-llm-council (1 skill)

- No hits above LOW in scan-i (only 10 units with hits across the 3 repos; llm-council not listed).
  Detail in raw/scan-a.json.

### glitternetwork/pinme (7 skill units)

- **pinme/pinme** — scanner CRITICAL 42: `tunnel/CRITICAL` = "cloudflared" in
  skills/pinme-uniwebpay/SKILL.md:224 — verified: "To test webhooks locally, expose the Worker
  through a tunnel (cloudflared / ngrok)." This is a payment-webhook skill (UniwebPay): the
  agent builds a webhook *receiver* (`webhookUrl` on products.create, signature verification)
  and is instructed to expose localhost publicly via tunnel for callback delivery.
  Grade: **confirmed** — tunnel-to-localhost + webhook-receiver construction, purpose-aligned
  (payment integration) but a dual-use primitive pair. `img_upload/HIGH` = `"files"` literals —
  benign.

### zarazhangrui/codebase-to-course (1 skill)

- Scanner CRITICAL 13: `img_upload/CRITICAL` `github.com/user-attachments` ×4 in README.md —
  verified: `<img>` tags embedding README screenshots (documentation images, not an upload
  primitive). Grade: **none** (FP for exfil; shows standard GitHub image-host usage for docs).

### chaseai-yt/claudex-loop (6 skill units)

- LOW 2: `"files"` literal in scripts/runner.py:107. Grade: **none**.

### dominikmartn/nothing-design-skill

- 1 skill unit, 0 egress hits. Grade: **none**.

### athola/claude-night-market (225 skill units, plugin marketplace)

- browser-recording CRITICAL 112 / sanctum/tutorial-updates CRITICAL 28 / media-composition HIGH 8:
  `browser/HIGH` = Playwright/browser automation (recording, tutorial capture — expected).
- leyline/git-platform CRITICAL 22: `gh issue/pr create` + curl — GitHub write automation
  (capability, purpose-aligned).
- imbue/proof-of-work HIGH 7: curl to PoW API (pattern-match).
- scribe/slop-detector MEDIUM 4: `"files"` literal (benign); stack-push MEDIUM 5: git push/gh create.
- No webhook/relay/tunnel/corpus/paste/registry hits. Grade: **capability**, benign.

### Prat011/awesome-llm-skills (31 skill units)

- webapp-testing CRITICAL 22: Playwright (capability). pptx HIGH 7, mcp-builder/notion-meeting
  MEDIUM 3: HTTP clients. Grade: **capability**, benign.

### zhuyansen/awesome-claude-video-skills (0 SKILL.md)

- Link list of ~180 video-skill repos with security grades. Not scanned as units; retained as
  a source list for future lanes.

### w95/awesome-claude-corporate-skills (166 skill units)

- Quiet: 10 units with hits, all LOW/MEDIUM. webapp-testing CRITICAL 22 (Playwright);
  slack-search MEDIUM 4 = `"files"` literals (:76,83 — benign); kaizen/mcp-builder MEDIUM 3
  (HTTP clients); dns LOW ×5 (nslookup/dig mentions in docs — "exfil shape" is FP).
- Grade: **pattern-match**, benign corporate skill pack.

### danyuchn/asd-ste100-skill (1 skill unit)

- No hits above LOW in scan-n. Detail in raw/scan-a.json.

### karanb192/awesome-claude-skills (0 SKILL.md)

- Link list only. Not scanned as units.

### Agentchengfeng/chengfeng-videocut-skills (8 skill units)

- Scanner CRITICAL 12: `creds/HIGH` ×2 in
  plugins/chengfeng-videocut/scripts/bug-report.test.cjs:45,118 — verified raw bytes:
  `"sk-abcdefghijklmnopqrstuvwxyz"` — a sequential-alphabet placeholder in test code, obviously
  synthetic, not a real key. Noted, never used.
- `img_upload/HIGH` + netcall: multipart upload + HTTP client — video upload primitive in the
  video-cut skill (purpose-aligned). Grade: **capability**; creds hits are test placeholders.

### agiwhitelist/auteur (1 skill unit)

- Scanner CRITICAL 97 (50 browser + 7 netcall primitives): browser automation for book-writing
  previews + HTTP clients. No upload/webhook/relay/tunnel. Grade: **capability**, benign.

### mohi-devhub/antivibe (1 skill unit)

- No hits above LOW in scan-o. Detail in raw/scan-a.json.

### threerocks/hand-drawn-styles, bevibing/tutor-skills, onvoyage-ai/gtm-engineer-skills

- hand-drawn-styles (1 skill): 0 egress hits. Grade: **none**.
- tutor-skills (2 skills): 0 hits. Grade: **none**.
- gtm-engineer-skills (12 skills): 1 LOW (single HTTP client call). Grade: **none**.

### asklokesh/claudeskill-loki-mode (1 root unit — 5,562 files; autonomous agent harness)

- Scanner CRITICAL 3601 (2,524 primitives). **This is the highest-signal repo in lane C.**
  - **`tunnel/CRITICAL` ×89 — confirmed**: `autonomy/loki` automates tunnel exposure and parses
    public URLs: `_extract_tunnel_url_cloudflared()` greps `https://[a-z0-9-]+\.trycloudflare\.com`
    from logs (loki:8816-8826); ngrok public_url extracted from the ngrok 4040 API JSON
    (loki:8826+). The autonomous agent exposes a dashboard via cloudflared/ngrok quick tunnels.
  - **`webhook/HIGH` ×38 — confirmed**: `autonomy/NOTIFY_INTEGRATION.md:31-32,231,254` and
    `autonomy/notify.sh:327-328` wire `hooks.slack.com` and `discord.com/api/webhooks` for agent
    notifications — documented dead-drop-shaped notification feature.
  - **"reverse-shell grammar" — FP on review**: `/dev/tcp/` in autonomy/docker-run.sh:309 is a
    port-availability check (`exec 3<>"/dev/tcp/127.0.0.1/${port}"`), not a reverse shell.
  - **`creds/HIGH` ×77 — all sentinel/canary placeholders**: raw bytes show
    `ghp_LOKIWITHHELDsentinel*INVALID` (run.sh:5646, worker.ts:18) — synthetic test markers, not
    real tokens. `xoxb-your-token` placeholder; `--insecure` curl flag (FP).
  - `corpus/MEDIUM` ×13: `_zz_` in SWE-bench result JSONs (benchmark data, not tradecraft) +
    `loki-ts/tests/zz/probe.test.ts` (a test dir named `zz` — coincidental).
  - `img_upload/HIGH` ×384: overwhelmingly `"files"` literals (unchecked in bulk; volume-driven).
- Grade: **confirmed** (tunnel automation + Slack/Discord webhook notifications). An autonomous
  agent harness that exposes itself to the public internet via tunnels and phones home via
  webhooks — the exact primitive pair the hunt watches for. Purpose-built (not obfuscated),
  but highest dual-use surface in the lane.

### alonw0/web-asset-generator (1 skill)

- Scanner CRITICAL 12: `img_upload/HIGH` multipart file upload (6 primitives) — the skill
  generates web assets; check upload target in final pass.

### chrisvoncsefalvay/claude-d3js-skill (1 skill)

- No hits above LOW in scan-s. Detail in raw/scan-a.json.

### zarazhangrui/frontend-slides (2 skill units)

- Scanner CRITICAL 95: `github.com/user-attachments` in README.md:21 — verified: a link to a
  demo deck asset (documentation), not an upload primitive. Browser/curl hits are slide-generation
  automation. Grade: **none** (FP for exfil).

### zxkane/aws-skills (6 skill units)

- **aws-agentic-ai** CRITICAL 14: `webhook/HIGH` `hooks.slack.com` in
  services/registry/governance-workflows.md:166 — verified: a Lambda handler **template** with
  `SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/T.../B.../xxx"` (placeholder for the
  user to fill). The skill instructs Bedrock AgentCore registry → Slack notifications.
  Grade: **pattern-match** (webhook dead-drop grammar, user-configured, purpose-aligned).
- aws-sst-development LOW 2: same Slack placeholder in references (authoring guide).

### omkamal/pypict-claude-skill (1 skill)

- Scanner CRITICAL 10: `git push` + curl in the skill. Image skill (per composio list).
  Grade: **capability** (git write + HTTP client).

### mhattingpete/claude-skills-marketplace, rampstackco/claude-skills, santiago-vargas-de-kruijf/claude-overkill

- 122 units, 20 with hits. Top: integration-orchestrator CRITICAL 38 (browser automation);
  code-review-web HIGH 6 (curl); dns "exfil shape" MEDIUMs are dig/nslookup in docs (FP);
  git-pushing MEDIUM 3 (git push — expected).
- Zero webhook/relay/tunnel/corpus/paste/registry/img_upload/email hits. Grade: **capability**,
  benign.

### wshobson/agents (184 skill units — large plugin collection)

- 48 units with hits. Top: e2e-test CRITICAL 48 (Playwright); connectivity-check CRITICAL 16
  (dig/nslookup + curl — incident-response tooling); deployment-pipeline/incident-runbook
  CRITICAL 10 (curl); paypal-integration CRITICAL 10 (PayPal API client); javascript-testing
  HIGH 8 (SMTP/sendmail + HTTP — test email).
- **python-performance-optimization / async-python-patterns** MEDIUM 5: `httpbin.org/delay/1`
  in references/advanced-patterns.md:162-165 and details.md — verified: Python async/concurrency
  teaching examples. Grade: **pattern-match**, benign (same shape as trailofbits modern-python).
- Grade overall: **capability** (broad DevOps/plugin surface); no webhook/tunnel/corpus hits.

### PleasePrompto/notebooklm-skill (1 skill)

- Scanner CRITICAL 74 (39 browser primitives): automates NotebookLM via browser.
  Grade: **capability**, purpose-aligned.

### yctimlin/mcp_excalidraw (1 skill unit)

- Scanner CRITICAL 107 (77 primitives): browser + multipart upload + curl. The img_upload hits
  are `curl -f` health checks in .github/workflows/docker.yml; uploads go to the self-hosted
  Excalidraw instance (MCP diagram server). Grade: **capability**, benign purpose.

### emory/ASD-AuDHD-PAI-Skills, 1NickPappas/move-code-quality-skill, Anjos2/recursive-research

- 1 skill each, 0 egress hits. Grade: **none**.

### alirezarezvani/claude-skills (847 skill units — second-largest source in lane C)

- 145 units with hits, dominated by Playwright browser-automation QA skills: playwright-pro/pw
  CRITICAL 577 (440 browser primitives), senior-qa CRITICAL 174, browser-automation CRITICAL 99,
  migrate CRITICAL 86, browserstack/testrail CRITICAL 24 (×4 harness copies: engineering-team/,
  .gemini/, engineering/).
- Only corpus-watchlist hit: `hooks.slack.com` in
  engineering/skills/observability-designer/assets/sample_alerts:258 — a sample alert config,
  benign.
- Grade: **capability** — the CRITICAL scores are volume-driven (Playwright by design in QA
  skills), not signal-driven. No tunnel/relay/upload primitives of note.

### travisvn/awesome-claude-skills (0 SKILL.md — link list, 15,270★)

- Link-only awesome list; not scanned as units. Used as a source for repo discovery
  (expo/skills, scientific-skills, get-shit-done, Skill_Seekers, frontend-slides came from it).

## Severity rollup

**Final (raw/scan-a.json, authoritative): 3,392 skill units scanned, 625 with egress hits.**
Risk levels: CRITICAL 184 · HIGH 63 · MEDIUM 134 · LOW 244.
Top hit categories (primitive-level): netcall/MEDIUM 4,420 · browser/HIGH 1,800 ·
img_upload/HIGH 897 · gitwrite/MEDIUM 652 · browser/MEDIUM 616 · dns/MEDIUM 247 ·
tunnel/CRITICAL 146 · creds/HIGH 87 · email/HIGH 60 · webhook/HIGH 44 · corpus/MEDIUM 15.

(Volume is dominated by browser-automation and HTTP-client primitives in QA/dev skills;
the per-skill grades below separate signal from volume.)

Grade distribution (verified sample):
- **confirmed** (bytes present, tradecraft-relevant): last30days-skill (r.jina.ai + Slack
  webhook), gitshot (vipulgupta2048 + coffee-gb byte-identical copies), daymade/twitter-reader
  (r.jina.ai), ComposioHQ ngrok-automation, expo ngrok tunnel, pinme/uniwebpay
  (cloudflared/ngrok + webhook receiver), loki-mode (tunnel automation + Slack/Discord
  webhooks), aws-skills (Slack webhook template).
- **pattern-match** (matches corpus tradecraft shape): httpbin.org examples (trailofbits
  modern-python, wshobson python-perf/async), Slack webhook samples (alireza observability),
  multipart uploads (videocut, web-asset-gen), git-write automation.
- **capability** (could be used this way, purpose-aligned): Playwright/browser skills
  (playwright-skill, night-market browser-recording, notebooklm, full-page-screenshot),
  SMTP/test-mail (dotnet mailpit, wshobson), cloud CLIs (aws-skills).

## Corpus-indicator watchlist hits

Hunt-corpus toolkit matches across lane C (verified):

| Indicator | Hits | Where | Verdict |
|---|---|---|---|
| r.jina.ai | 11 | daymade/twitter-reader (SKILL.md:79,110,224; fetch_tweet.py:38,53; fetch_tweets.sh:28,33; fetch_article.py:50,63), daymade/douban-skill (troubleshooting.md:126,128) | **confirmed** — primary fetcher with JINA_API_KEY |
| r.jina.ai (keyless) | 2 | mvanhorn/last30days-skill (web_fetch_keyless.py:4,26) | **confirmed** — JINA_READER_PREFIX keyless fallback tier |
| Slack webhooks | 40+ | last30days (watchlist.py:32,34,45); loki-mode (notify.sh:327, NOTIFY_INTEGRATION.md:31,254); aws-skills (governance-workflows.md:166, placeholder); alireza (sample_alerts:258, sample) | confirmed (last30days, loki-mode); placeholder (aws); sample (alireza) |
| Discord webhooks | 38 | loki-mode (notify.sh:328, NOTIFY_INTEGRATION.md:32,231) | **confirmed** — agent notification feature |
| ngrok | 12 | ComposioHQ ngrok-automation (Rube MCP); expo (run-your-app.md:159,251-254); pinme (SKILL.md:224); loki-mode (loki:8826+) | confirmed |
| cloudflared | 89+ | loki-mode (tunnel URL extractors); pinme (SKILL.md:224) | confirmed (loki-mode automation) |
| httpbin.org | 18 | trailofbits modern-python (SKILL.md:283); wshobson (advanced-patterns.md:162-165, details.md:231-233); n8n cache (community-nodes.json:11238) | pattern-match — teaching/recon examples |
| gitshot grammar | 3 repos | vipulgupta2048/gitshot, trekawek/coffee-gb (byte-identical SKILL.md) | **confirmed** — release-asset + catbox.moe flow |
| github.com/user-attachments | 8 | codebase-to-course, frontend-slides (README images) | benign (docs) |
| uploads.github.com | 0 | — | honest negative (matches v1) |
| zz labels | 13 | loki-mode (swebench JSONs, tests/zz/) | coincidental (benchmark data, test dir) |
| epoch nonces | 0 | — | honest negative |
| go-import tags | 0 | — | honest negative |
| verify=False | 1 | get-shit-done fixture (`eraser.erase(verify=False)` kwarg) | FP (kwarg, not TLS) |
| webhook.site | 0 | — | honest negative |

## Top-5 riskiest

### 1. asklokesh/claudeskill-loki-mode — CRITICAL 3601 (confirmed)
Autonomous agent harness (5,562 files). Tunnel automation parses cloudflared quick-tunnel
URLs (`_extract_tunnel_url_cloudflared`, loki:8816: `grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com'`)
and ngrok public URLs from the 4040 API; Slack+Discord webhook notifications wired in
`autonomy/notify.sh:327-328` (`hooks.slack.com`, `discord.com/api/webhooks`). 77 creds hits
are sentinel canaries (`ghp_LOKIWITHHELDsentinel*INVALID`). The tunnel+webhook pair is the
exact primitive combination the hunt watches for.

### 2. mvanhorn/last30days-skill — CRITICAL 64 (confirmed)
`scripts/lib/web_fetch_keyless.py:4,26`: `JINA_READER_PREFIX = "https://r.jina.ai/"` — keyless
jina reader fallback tier (corpus relay). `scripts/watchlist.py:32,34,45`: `hooks.slack.com`
Slack webhook alerts via `_send_slack_webhook` (user-configured destination). Multipart audio
upload to Whisper endpoint (transcribe.py:220, benign purpose).

### 3. vipulgupta2048/gitshot (+ trekawek/coffee-gb byte-identical copy) — CRITICAL 68 (confirmed)
`skills/gitshot/SKILL.md:25-85`: `npx gitshot` uploads screenshots to `<user>/gitshot-images`
as GitHub Release Asset (auto-creates repo); fallback `catbox.moe` (no signup); optional
Cloudinary/imgbb. Impl: `src/catbox.ts:5,24`, `src/github.ts:52`. The gitshot exfil grammar
(screenshot → public image host → markdown URL) propagates verbatim across repos.

### 4. daymade/twitter-reader — CRITICAL 36 (confirmed)
r.jina.ai as *primary* fetcher: `scripts/fetch_tweets.sh:28,33`:
`curl -s "https://r.jina.ai/${url}" -H "Authorization: Bearer ${JINA_API_KEY}"`;
also `fetch_tweet.py:38,53`, `fetch_article.py:50,63`, `SKILL.md:79,110,224`.

### 5. glitternetwork/pinme (pinme-uniwebpay) — CRITICAL 42 (confirmed)
Payment-webhook skill instructs the agent to build a webhook *receiver* and expose localhost
publicly: `skills/pinme-uniwebpay/SKILL.md:224`: "To test webhooks locally, expose the Worker
through a tunnel (cloudflared / ngrok)." Webhook-receiver construction + tunnel-to-localhost
= dual-use primitive pair (purpose-aligned for payments, but the exact shape).
