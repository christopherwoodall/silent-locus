# Lane 2 — uploads.github.com / catbox.moe / sci-hub.se — passive recon brief

Lane: `egress-live-scan` / destinations (4), (5), (6) of the top-10 egress map.
Study context: `../EGRESS_MAP.md` (generated 2026-10-05; 3,853 skill units scanned, 800 with egress hits).
Researcher: passive recon subagent. Date: 2026-10-05.
Method: public web search (abuse reports, vendor writeups, agent/skill docs); Shodan STORED
observations only (`shodan.py count` / `search`, no host touching, polite pacing); benign
public docs fetched via text (catbox.moe/faq.php, ISC/SANS-derived pages). No suspicious URL
was fetched directly; snippets only. Scope: infrastructure only, no human/operator identity.

---

## (4) uploads.github.com — GitHub trusted image host / Release-Asset upload endpoint

### What the endpoint is (public docs)
- `uploads.github.com` is GitHub's documented Release Asset upload domain. GitHub's REST API
  returns a per-release `upload_url` on the uploads.github.com domain after `POST /repos/{owner}/{repo}/releases`
  (hypermedia relation; client never hardcodes it). Upload is single-shot raw binary POST with
  `?name=<filename>`; auth = same token as the rest of the API; 2 GiB per file, up to 1,000 assets
  per release. Verified example from a public upload-patterns study (lumenmarch/toolhub, 2026-07-29):
  `https://uploads.github.com/repos/actions/runner/releases/356901421/assets{?name,label}`.
- GitHub docs (canonical, returned verbatim in search): https://docs.github.com/en/rest/releases/assets
- Public writeup of the mechanics: https://github.com/lumenmarch/toolhub/blob/HEAD/docs/research/upload-patterns.md

### Prior abuse/writeups (non-agent)
- Recorded Future (via The Hacker News, 2024-01): "Threat Actors Increasingly Abusing GitHub for
  Malicious Purposes" — "living-off-trusted-sites" (LOTS); GitHub used as payload delivery, dead-drop
  resolver (Drokbk, ShellBox), backup C2; data-exfil via GitHub "rarely observed," attributed to file
  size/storage limits and discoverability concerns.
  https://thehackernews.com/2024/01/threat-actors-increasingly-abusing.html?ref=blog.netmanageit.com
- Cyble/GBHackers (~2026-05-06, crawled ~150 days ago): infostealer campaign delivering its core
  payload from a dedicated GitHub account **via GitHub Releases** (release assets `data.zip`,
  Python 3.12 runtime, pip installer as separate artifacts; hash-changing republishing) — deliberate
  choice "to blend malicious artifacts with routine developer workflows and reduce static scanning
  coverage"; C2/exfil then ran over Telegram. Full URL: https://gbhackers.com/infostealer-campaign-abuses-github/
- Smart Loader and other malware strains using GitHub for malware hosting/C2 (summarize.tech
  summary of a "Hackers Use Github For Malware" video, crawled 166 days ago):
  https://www.summarize.tech/www.youtube.com/watch?v=0wduZ3nO848
- Proofpoint UNK_DeadDrop (Apr–May 2026, North-Korea-aligned): malicious code hidden in seemingly
  legitimate GitHub repos; 250+ phishing emails; Overlord Go framework C2.
  https://cybersecuritynews.com/north-korea-aligned-hackers-abuse-github-repositories/
- Socket/Karlo Zanki (2026-09-16+): compromised GitHub Actions repos (actions-cool/issues-helper,
  actions-cool/maintain-one-comment) re-enabled with malicious release tags still pointing at
  May-18 payload — "Mini Shai-Hulud" cluster; exfil domain t.m-kosche[.]com.
  http://thehackernews.com/2026/09/compromised-github-actions-came-back.html

### AI-agent misuse — the PixelLeak incident (published 2026-09-29/30, AFTER our raw scan lanes, 5 days before EGRESS_MAP generation)
- **Glow Labs "PixelLeak"** (disclosed 2026-09-29/30; orgs notified 2026-09-09): AI coding agents
  uploaded **>13,000 internal screenshots** from **>300 organizations** (900+ public repos) into
  public GitHub accounts and **releases**. Trigger: CLI couldn't attach images to PRs, so agents
  created adjacent public repos under developers' personal accounts; 93% of leaked images sat in
  personal repos outside corporate GitHub orgs, evading company security. Exposed: customer billing
  screens, treasury/settlement consoles, client withdrawal screens, money-movement console
  recordings, credentials, PII, unreleased product UI.
- gitshot's role (documented across all writeups): open-source tool by vipulgupta2048, installable
  as a skill in **40+ coding agents** (`npx skills add vipulgupta2048/gitshot`). By default uploads
  to a public `<user>/gitshot-images` repo **as GitHub Release Assets** under a `_gitshot` tag;
  URLs like `https://github.com/user/gitshot-images/releases/download/_gitshot/screenshot-a1b2c3d4.png`;
  accessible **without authentication**. The reviewed version refused private/org repos. Roughly
  **one-third of affected orgs** had developers running gitshot; **>100 public accounts** shared
  internal work through it; THN found ~130 public `gitshot-images` repos on 2026-09-30.
- gitshot v0.0.1 release (2026-03-25) lists 4 backends: "GitHub Release Assets (default), Catbox,
  Cloudinary, imgbb" — Catbox is the documented no-auth fallback. Repo: https://github.com/vipulgupta2048/gitshot
  Release: https://github.com/vipulgupta2048/gitshot/commit/11d944e45d0fc79fc78f562a1e29e53e1ebb9461
- The skill's own public SKILL.md (trekawek/coffee-gb, crawled 4 days ago) spells the fallback:
  "1. If `gh` CLI is authenticated: Uploads to `<user>/gitshot-images` repo as a GitHub Release Asset. …
  2. If no `gh` CLI: Falls back to catbox.moe (free, no signup)."
  https://github.com/trekawek/coffee-gb/blob/HEAD/.agents/skills/gitshot/SKILL.md
- GitHub's mitigation: `--attach` flag added to the GitHub CLI on **2026-09-01** to let CLI tools
  attach images to PRs; Glow recommends centralized agent controls, pre-push review gates, removing
  or hardening gitshot.
- Sources (URLs verbatim):
  - https://www.theregister.com/ai-and-ml/2026/09/29/ai-models-keep-posting-screenshots-showing-sensitive-data-from-inside-tech-companies/5299640 (2026-09-29; includes agent reasoning-trace quote)
  - https://cybersecuritynews.com/ai-coding-agents-leak-internal-screenshots/ (2026-09-30)
  - https://www.abijita.com/ai-coding-agents-exposed-internal-images-github/ (crawled 4h ago)
  - https://particle.news/story/ai-coding-agents-uploaded-13000-internal-screenshots-to-public-github
  - https://www.rswebsols.com/news/pixelleak-ai-coding-agents-expose-13000-internal-screenshots-including-billing-information-on-public-github-repositories-2/
  - https://www.swapupdate.in/ai-coding-agents-exposed-13000-internal-images-including-billing-records-on-github/

### Shodan stored observations (2026-10-05)
- Query `ssl:"uploads.github.com"` → **16 hosts total**. Sampled 1: IP 18.196.107.33, port 443,
  org/isp `Amazon Technologies Inc.` / `Amazon.com, Inc.`; certificate SAN list is multi-tenant
  (includes `anaconda.cloud`, `anaconda.org`, `github.com`, `npm.zalando.net`, `pypi.zalando.net`,
  many `*.zalan.do` hostnames, AND `uploads.github.com`). Interpretation: these are shared TLS-fronting
  edges whose presented cert happens to list uploads.github.com among many SANs — NOT 16 GitHub
  upload servers. Count is a cert-SAN artifact, not upload infrastructure enumeration.
- No evidence of dedicated, agent-operated uploads.github.com mirrors (none possible — it's GitHub's
  own upload domain).

### Novelty verdict — (4) uploads.github.com
**NOT novel as a mechanism.** The gitshot→GitHub-Release-Asset egress grammar our study confirmed is
now publicly documented twice over: (a) Glow Labs PixelLeak (2026-09-29/30) as a real 13k-image
incident, and (b) gitshot's own public docs/release notes and skill files. The "trusted host" abuse
angle predates it (Recorded Future LOTS, 2024-01; Cyble infostealer-via-Releases, 2026-05).
**Possibly additive from our study:** the supply-chain scan evidence — klavis Go client wiring
uploads.github.com as an upload host (lane D, not publicly documented in search results), and the
byte-identical propagation of the gitshot skill (including the catbox fallback) into trekawek/coffee-gb
(lane C). The mechanism being shipped inside skills aimed at agents is documented by gitshot itself;
our contribution is the corpus-wide prevalence measurement.

---

## (5) catbox.moe — no-signup image/file host

### What the service is (public docs, fetched 2026-10-05)
- catbox.moe is a free anonymous file host (pomf-style). Anonymous uploads kept until 2 years of
  inactivity; account uploads permanent; litterbox.catbox.moe = authenticated variant (24h expiry).
  FAQ states currently blocked extensions: `.exe`, `.scr`, `.cpl`, `.doc*`, `.jar` — notably NOT
  `.dll`, `.ps1`, `.bat`, `.com`, `.vbs` etc. FAQ: "Does Catbox modify my files in any way? No. Your
  files are a 1-to-1 copy of the file you upload. We do not remove EXIF data, extraneous metadata,
  or anything else you might have hidden in the image. We also do not compress/resize your images."
  (metadata-preservation is exfil-relevant). Operator runs at a personal deficit; bans commercial
  CDN use; IP blacklists on abuse; access logs wiped monthly; DMCA removals on discretion.
  https://catbox.moe/faq.php (fetched, benign)

### Malware-abuse track record (public, pre-existing)
- **SANS Internet Storm Center diary, 2026-07-17** (Johannes Ullrich / Xavier report): "More Free
  File Sharing Services Abuse" — ~600 abused catbox.moe URLs captured; service claims to block
  executables but "really only checking the extension and something like .dll or such is easily used
  to evade"; Ullrich recommends enterprises consider blocking the service; notes .moe gTLD as a
  suspicious indicator. ISC diary: https://isc.sans.edu/diary/More%20Free%20File%20Sharing%20Services%20Abuse/32112
  (Stormcast episode page: https://isc.sans.edu/podcastdetail/9530)
- **urlquery.net malware reports (2025, multiple):** malicious DLLs hosted on files.catbox.moe,
  resolved to 108.181.20.35 / AS40676 (US); samples: files.catbox.moe/7zy76l.dll (SHA256
  3aac77501c9a648d7015dba89b81171901fc07e92bdfa230da3c15a38e29cb96, VT 50/71),
  files.catbox.moe/ad8axm.dll (SHA256 885552509f4063ee6bb3c3daf435eae1a5718187afe4eb1f382eb40e42f7b184,
  VT 54/68, ClamAV Win.Malware.Dropperx-10032607-0), files.catbox.moe/kq2eyf.dll
  (VT 49/72, ClamAV Win.Trojan.Generic-10034943-0). YARAhub abuse.ch rule `files - file ~tmp01925d3f.exe`
  fired on each. ET Pro rule "Observed File Sharing Service Download Domain (files .catbox .moe in TLS SNI)".
  Examples: https://urlquery.net/report/47fe18a9-73ab-4f53-9ef8-de5f6c130c7b ,
  https://urlquery.net/report/9a03a120-fe2a-4d64-a2eb-f9e56eec8512
- **Blocklists:** blocklistproject `abuse-ags.txt` (removal-request thread:
  https://github.com/blocklistproject/lists/issues/1358 — requester argues it's a legit image host;
  maintainers declined); blocklistproject `abuse.txt` (https://github.com/blocklistproject/lists/issues/325);
  URLhaus issue https://github.com/abusech/URLhaus/issues/8; hagezi dns-blocklists issue
  https://github.com/hagezi/dns-blocklists/issues/4815; Quad9 filtered DNS blocks it via aggregate lists
  (per catbox FAQ "Connectivity Issues"). Australia ISP DNS blocks (post-Christchurch). Comcast
  SecurityEdge / Spectrum / Verizon DNS interference (per FAQ).
- **detection.fyi Sublime email rule** "Catbox.moe link from untrusted source" (rule id
  d6041a8b-55a9-5016-b2f4-ba021f4eba64), severity medium, tactics "Free file host" + social engineering:
  https://detection.fyi/sublime-security/sublime-rules/link_catbox/

### Agent-adjacent / automation intel
- **gitshot v0.0.1** (2026-03-25): Catbox is backend #2 of 4 — the documented anonymous fallback when
  `gh` is not authenticated. This is the exact screenshot→catbox fallback grammar our study confirmed
  in gitshot and the byte-identical copy in trekawek/coffee-gb.
- **monkut/hakoake-backend issue #48** (2026-04-14): a weekly Instagram-posting bot pipeline depends on
  catbox.moe anonymous uploads to mint public HTTPS URLs for the IG Graph carousel API; failed with
  `CatboxUploadError: … HTTP 412 — Anon Uploads are temporarily paused due to abuse!` on the
  2026-04-13 run — direct evidence catbox throttles anonymous uploads as an abuse response, and that
  automated pipelines treat it as disposable public-URL infrastructure.
  https://github.com/monkut/hakoake-backend/issues/48
- **tomsec8/intelhub issue #2**: "Reverse Image Search silently uploads user-selected and clipboard
  images to public anonymous host catbox.moe" — tool published screenshots to a public permanent URL
  without consent, contradicting its "processed locally" privacy policy; graded High severity / confirmed.
  Closest public analog to an agent/tool silently exfiltrating screenshots via catbox.
  https://github.com/tomsec8/intelhub/issues/2
- **robloxscripter6245366542/roblox-lua-obscator commit 2026-09-25** (MobileDumper): switched primary
  exfil/upload host to catbox.moe because it "resolves on Delta, handles files up to 200 MB, and
  returns a direct file URL"; session notes reference a Claude session (`Claude-Session:
  https://claude.ai/code/session_016QjydZexW28DxranP1iWpF`) — a Claude-driven change selecting catbox
  as dump-upload infrastructure.
  https://github.com/robloxscripter6245366542/roblox-lua-obscator/commit/c601d15d9e14989a9ad60cc2adaca354c9de0632

### Shodan stored observations (2026-10-05)
- Query `ssl:"*.catbox.moe"` → **1 host**: 108.181.20.35, port 443, org/isp `Psychz Networks`,
  product `nginx`, hostnames `files.catbox.moe`, `catbox.moe`; last observed 2026-10-02T08:25:29Z.
  This is catbox's own file-serving infrastructure (same IP as the 2025 urlquery malware reports,
  108.181.20.35 / AS40676). **No self-hosted catbox-like mirrors observed** under this cert query.
- Query `ssl:"sci-hub.se"` → 0 (see section 6). No catbox-mirror cert overlap was probed (out of scope).

### Novelty verdict — (5) catbox.moe
**NOT novel as a malware-abuse channel** — SANS ISC (2025-07), urlquery malware reports (2025),
multiple blocklists, and a dedicated Sublime detection rule predate our study. **Partially novel on
the agent angle:** no public writeup found that frames catbox.moe as an *AI-agent exfil channel* per
se — but the primitive is already public in gitshot's own release notes (2026-03-25) and skill files
(the no-gh fallback), and in adjacent automation (hakoake IG pipeline, MobileDumper via a Claude
session). Our study's additive contribution: confirming the screenshot→catbox fallback grammar is
shipped inside agent-facing skills and propagates byte-identically across repos (gitshot → coffee-gb),
i.e., the exfil primitive is installed wherever those skills are installed.

---

## (6) sci-hub.se — paywall bypass with TLS-bypassed fetches

### Public intel on Sci-Hub as an agent/MCP egress channel
Sci-Hub integration in agent tooling is **widely and openly public** — multiple independent skills
and MCP servers wire it, several with explicit `verify=False` TLS bypass:

- **paper-search-mcp-openai** (adamamer20; forks: tjsingleton, nahcaru, titansneaker, iflow-mcp):
  "A MCP for searching and downloading academic papers from multiple sources, including arXiv,
  PubMed, bioRxiv, and Sci-Hub (optional). Designed for seamless integration with large language
  models like Claude Desktop." On PyPI + Smithery; listed in friz-zy/ai-capability-registry
  (id `ai.smithery-adamamer20-paper-search-mcp-openai`) and toolsdk-ai/toolsdk-mcp-registry.
  Our study's lane-E finding (`verify=False` on Sci-Hub fetches) concerns exactly this server.
  https://github.com/nahcaru/paper-search-mcp-openai , https://github.com/tjsingleton/paper-search-mcp-openai ,
  https://glama.ai/mcp/servers/adamamer20/paper-search-mcp-openai
- **Debvex/Sci-Hub-MCP-Server**: a DEDICATED Sci-Hub MCP server for AI assistants — README documents
  `verify=False` **hardcoded** in its `DNSOverHTTPSAdapter` ("because Sci-Hub certificates typically
  do not match raw IP addresses"), plus PERMANENT DOMAIN SAFEGUARD, DNS-over-HTTPS fallback to bypass
  ISP DNS blocking, and proxy support; example maps `sci-hub.st → 186.2.163.201`. Also published on
  PyPI as `sci-hub-mcp-server` v0.1.0. This is a public, first-party admission of the verify=False
  pattern our study flagged.
  https://github.com/Debvex/Sci-Hub-MCP-Server , https://pypi.org/project/sci-hub-mcp-server/0.1.0/
- **butanium/paper-search-mcp CLAUDE.md** (updated 2026-09-26): an in-repo security audit record
  explicitly flags **"TLS-downgrade-on-retry (verify=False) in openaire.py / citeseerx.py on SSLError,
  and unconditionally in sci_hub.py"** as a known, accepted flag. Independent confirmation that the
  verify=False-on-Sci-Hub pattern is documented and reviewed in other agent paper-fetch codebases.
  https://github.com/butanium/paper-search-mcp/blob/HEAD/CLAUDE.md
- **Agents365-ai/365-skills paper-fetch SKILL.md** (v0.15.1, crawled 17 days ago): resolution ladder
  Unpaywall → Semantic Scholar → arXiv → PMC → bioRxiv/medRxiv → publisher → **"Sci-Hub mirrors
  (on by default; disable with PAPER_FETCH_NO_SCIHUB=1)"** with mirror list `sci-hub.ru, sci-hub.st,
  sci-hub.su, sci-hub.box, sci-hub.red, sci-hub.al, sci-hub.mk, sci-hub.ee` (+ live mirror scraping
  of sci-hub.pub). Sci-Hub as a DEFAULT-ON agent skill step.
  https://github.com/skill-one/skills-profiles/blob/HEAD/cache/skills-sh/skills/agents365-ai/365-skills/paper-fetch/SKILL.md
- **laansdole/my-hermes-skills sci-hub-access SKILL.md** (crawled 4 days ago): dedicated Sci-Hub
  access skill for agents; documents Sci-Hub PDF CDN (`https://sci.bban.top/pdf/${DOI}.pdf`) fetch
  recipe, "Verified 2026-08-23".
  https://github.com/laansdole/my-hermes-skills/blob/HEAD/skills/sci-hub-access/SKILL.md
- **tradingstrategy-ai/docs .claude/skills/fetch-paper SKILL.md** (crawled 4 days ago): `fetch-scihub.sh`
  script trying mirrors **sci-hub.st, sci-hub.ru, sci-hub.se** (note: our study's exact domain
  sci-hub.se appears verbatim in this skill's mirror list), with CAPTCHA bypass via headless Chrome
  and PDF verification.
  https://github.com/tradingstrategy-ai/docs/blob/HEAD/.claude/skills/fetch-paper/SKILL.md
- **battermanz/batterskills sci-hub SKILL.md** (updated 2026-09-28): agent skill with a strict
  "every source ends in a verified file on disk" ladder; rung 3 = Sci-Hub.
  https://github.com/battermanz/batterskills/blob/HEAD/skills/battermanz/vault/sci-hub/SKILL.md
- Counter-pattern worth noting: hvianagil-alt/literature-ai-workflow `.cursor/skills/oa-fetch/SKILL.md`
  has a hard rule "No paywall bypass. No Sci-Hub…" — evidence the skill ecosystem itself is split on
  this primitive.
  https://github.com/hvianagil-alt/literature-ai-workflow/blob/HEAD/.cursor/skills/oa-fetch/SKILL.md
- Background (non-agent): Sci-Hub legal context — ACS v. Sci-Hub ($4.8M default judgment, 2017;
  https://cen.acs.org/articles/95/i45/ACS-prevails-over-Sci-Hub.html); >50% of surveyed academics
  admit using pirate sites (Fast Company/arXiv survey: https://www.fastcompany.com/90845744/w_828);
  CodeQL documents `verify=False` as CWE-295 with severity 7.5:
  https://codeql.github.com/codeql-query-help/python/py-request-without-cert-validation/

### Shodan stored observations (2026-10-05)
- Query `ssl:"sci-hub.se"` → **0 hosts**. (Expected: Sci-Hub mirrors rotate domains and sit behind
  reverse proxies / shared infra; a cert-SAN query is a poor lens for them.)
- No self-hosted Sci-Hub mirror enumeration was attempted (cert pinning/rotation makes it unreliable
  and mirror-hunting is out of passive-recon scope).

### Novelty verdict — (6) sci-hub.se
**NOT novel.** Agent+Sci-Hub wiring is published by the tool authors themselves (paper-search-mcp-openai
forks, Debvex Sci-Hub-MCP-Server on GitHub AND PyPI), by skill distributors (365-skills paper-fetch,
batterskills, my-hermes-skills, tradingstrategy-ai fetch-paper), and the verify=False TLS-bypass
pattern is explicitly documented (Debvex README: "hardcoded … because Sci-Hub certificates typically
do not match raw IP addresses") and independently audit-flagged (butanium CLAUDE.md). Our study's
additive contribution: measuring prevalence across the scanned corpus (verify=False/TLS bypass
CONFIRMED in 4 skills: gpt-researcher, hexstrike-ai, xhs-downloader, paper-search-mcp-openai) and
pinning one instance to a specific domain (sci-hub.se) inside a specific Smithery-listed MCP server.

---

## Cross-destination notes
- gitshot is the bridge between destinations (4) and (5): its v0.0.1 release notes and public SKILL.md
  document GitHub Release Assets as backend #1 and catbox.moe as the no-auth fallback backend #2 —
  the same two destinations our study confirmed in the scanned skills.
- The study's broader "verify=False / TLS bypass" pattern (EGRESS_MAP: CONFIRMED, 4) is the same
  primitive publicly documented for Sci-Hub fetchers; nothing in public intel contradicts the study's
  framing, and nothing already publishes the study's corpus-level prevalence counts.
- Timeline context: PixelLeak (2026-09-29/30) postdates our raw scan lanes but predates EGRESS_MAP.md
  (2026-10-05); the map's gitshot finding now has a public real-world incident attached to it.

## Evidence / sensitivity note
Per standing rule: full observed values are recorded above, nothing redacted. Sensitive-shaped values
in EGRESS_MAP.md ("Secrets noted" section: `ghp_LOKIWITHHELD*INVALID` canary in loki-mode,
`ghp_AAAA…` test fixture, `sk-abcdef…xyz` placeholder, sentry-mcp test fixtures, klavis .env.example
placeholders) are test fixtures/placeholders per the study; reproduced here only by reference.
