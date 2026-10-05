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
| 10 | haunchen/n8n-skills | — | n8n webhook-automation skills | pending |
| 11 | jthack/threat-hunting-with-sigma-rules-skill | — | security skill | pending |
| 12 | trailofbits/skills | 7,369 | security-firm skills | cloned OK (85 SKILL.md) |
| 13 | SimoneAvogadro/android-reverse-engineering-skill | 7,975 | reverse-engineering skill | cloned OK (1 SKILL.md, retry after proxy abort) |
| 14 | alirezarezvani/claude-skills | 27,626 | top-starred collection | cloned OK (846 SKILL.md) |
| 15 | virgiliojr94/book-to-skill | 33,757 | top-starred | cloned OK (1 SKILL.md) |
| 16 | elementalsouls/Claude-BugHunter | 4,773 | security skill | cloned OK (83 SKILL.md) |
| 17 | P4nda0s/reverse-skills | 2,232 | reverse-engineering skills | cloned OK (7 SKILL.md) |
| 18 | tradermonty/claude-trading-skills | 3,030 | trading skills | cloned OK (94 SKILL.md) |
| 19 | vipulgupta2048/gitshot | 32 | "upload images to issues, PRs" — gitshot grammar | cloned OK (3 SKILL.md) |
| 20 | trekawek/coffee-gb | — | gitshot skill material (v1) | cloning |
| 21 | conorluddy/ios-simulator-skill | — | simulator screenshot capability | cloned OK (1 SKILL.md) |
| 22 | expo/skills | — | linked from travisvn list | cloned OK (26 SKILL.md) |
| 23 | K-Dense-AI/claude-scientific-skills | — | linked from travisvn list | cloning |
| 24 | gsd-build/get-shit-done | — | linked from travisvn list | cloned OK (0 SKILL.md — layout TBD) |
| 25 | obra/superpowers-lab | — | obra lab skills | cloned OK (4 SKILL.md) |
| 26 | obra/superpowers-skills | — | obra community skills | cloned OK (31 SKILL.md) |
| 27 | yusufkaraaslan/Skill_Seekers | — | linked from travisvn list | cloned OK (26 SKILL.md; hits all noise) |
| 28 | NeoLabHQ/context-engineering-kit | 1,748 | top-starred | cloned OK (204 SKILL.md) |
| 29 | daymade/claude-code-skills | 1,442 | top-starred | pending |
| 30 | CharlesWiltgen/Axiom | 1,189 | top-starred | pending |
| 31 | Aaronontheweb/dotnet-skills | 1,201 | top-starred | pending |
| 32 | aiwithremy/claude-skills-llm-council | 2,499 | top-starred | pending |
| 33 | chaseai-yt/claudex-loop | 2,737 | top-starred | pending |
| 34 | zarazhangrui/codebase-to-course | 5,648 | top-starred | pending |
| 35 | glitternetwork/pinme | 3,745 | top-starred | pending |
| 36 | dominikmartn/nothing-design-skill | 2,806 | top-starred | pending |
| 37 | BehiSecc/awesome-claude-skills | 10,212 | top-starred list | pending |
| 38 | hesreallyhim/awesome-claude-code | 55,092 | top-starred list/guide | pending |
| 39 | athola/claude-night-market | 342 | claims 186 skills | pending |
| 40 | zhuyansen/awesome-claude-video-skills | 413 | 180 security-graded video-skill repos | pending |
| 41 | Prat011/awesome-llm-skills | 1,781 | list | pending |
| 42 | karanb192/awesome-claude-skills | 534 | list | pending |
| 43 | w95/awesome-claude-corporate-skills | 230 | corporate skills list | pending |
| 44 | danyuchn/asd-ste100-skill | 3,596 | top-starred | pending |
| 45 | Agentchengfeng/chengfeng-videocut-skills | 3,030 | top-starred | pending |
| 46 | agiwhitelist/auteur | 1,035 | top-starred | pending |
| 47 | mohi-devhub/antivibe | 1,120 | top-starred | pending |
| 48 | threerocks/hand-drawn-styles | 1,410 | top-starred | pending |
| 49 | bevibing/tutor-skills | 1,319 | top-starred | pending |
| 50 | onvoyage-ai/gtm-engineer-skills | 1,316 | top-starred | pending |
| 51 | zsyggg/paper-craft-skills | 1,251 | top-starred | pending |
| 52 | Spark-To-Paper-Skills/paperjury | 1,217 | top-starred | pending |
| 53 | adamlyttleapps/claude-skill-app-onboarding-questionnaire | 1,211 | top-starred | pending |
| 54 | alonw0/web-asset-generator | — | linked from lists | pending |
| 55 | chrisvoncsefalvay/claude-d3js-skill | — | linked from lists | pending |
| 56 | asklokesh/claudeskill-loki-mode | — | linked from lists | pending |
| 57 | zarazhangrui/frontend-slides | — | linked from travisvn | pending |
| 58 | omkamal/pypict-claude-skill | — | image skill (composio list) | pending |
| 59 | zxkane/aws-skills | — | cloud skills (composio list) | pending |
| 60 | mhattingpete/claude-skills-marketplace | — | marketplace (composio list) | pending |
| 61 | rampstackco/claude-skills | — | collection (composio list) | pending |
| 62 | santiago-vargas-de-kruijf/claude-overkill | — | collection (composio list) | pending |
| 63 | emory/ASD-AuDHD-PAI-Skills | — | (composio list) | pending |
| 64 | 1NickPappas/move-code-quality-skill | — | (composio list) | pending |
| 65 | Anjos2/recursive-research | — | (composio list) | pending |
| 66 | PleasePrompto/notebooklm-skill | — | (composio list) | pending |
| 67 | yctimlin/mcp_excalidraw | 2,499 | top-starred | pending |
| 68 | wshobson/agents | — | popular agents repo (verify name) | pending |

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

## Severity rollup

(To be filled after final scan.)

## Corpus-indicator watchlist hits

(To be filled after final scan.)

## Top-5 riskiest

(To be filled after final scan.)
