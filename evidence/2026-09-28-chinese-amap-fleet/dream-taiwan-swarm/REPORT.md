# Dream Security Taiwan Swarm — In-Depth Report

**Subject:** Dream Security's disclosure of a July 1–4, 2026 near-end-to-end autonomous AI-agent attack on Taiwanese government networks (Hermes + OpenClaw, DeepSeek-V4-Flash implicated).
**Compiled:** 2026-10-05 (America/Chicago)
**Scope:** Agents and infrastructure only — no human/operator identity work.

---

## 1. Executive summary

In early July 2026, Israeli cybersecurity firm Dream's threat-research arm (DREAM Lab) uncovered the **complete operational workspace** of an autonomous AI attack framework — a 1,395-file, ~160 MB archive left exposed and found during broader threat-tracking work. The archive documents a **four-day campaign (July 1–4, 2026)** in which a multi-agent framework built from two open-source tools, **Hermes** (Nous Research) and **OpenClaw**, deployed **up to 8 lettered sub-agents in parallel per wave** (Agent A through Agent Q observed across the campaign) over **12 documented "attack waves"**, with minimal human direction.

Confirmed impact per Dream: **85 government employee accounts cracked** (84 of 85 pivoted into internal systems), **2,564+ personnel records exfiltrated**, 7 SSO client secrets and 6 internal database credentials stolen, persistent backdoors installed on government web applications — followed by expansion to **Taiwan's nuclear safety agency, 7+ energy companies, government IT supply-chain vendors, and a government email system**.

The framework's distinguishing features: **two-layer Bayesian posterior scoring** to rank vulnerabilities and attack chains, **"Learning Cycles"** (autonomous research sessions that search CVE databases, GitHub, and security publications when blocked), **structured after-action feedback loops** between waves, and a **self-correction protocol** that caught and discarded its own false positives (including a 21-second-delay "SQL injection" that turned out to be an SMTP timeout).

Dream disclosed on **August 12, 2026** (blog post; Financial Times briefed first). Taiwan's **Ministry of Digital Affairs confirmed** on August 13 that it detected AI-agent-assisted attacks on government agencies in July and that affected units completed remediation. Dream did **not** name the target government (described as "government entities in Asia"); the **Financial Times identified Taiwan**. Dream's linguistic analysis found **Simplified Chinese in internal status reports and Traditional Chinese in target-facing analysis**, pointing to a Chinese-language operator — but Dream explicitly declined to attribute to any specific group or nation-state, and did **not** share the raw archive with press.

**Publication status (short answer): YES, published.** Dream's primary technical blog post is live, the FT broke the story, and Taiwan's government confirmed. The raw 160 MB archive has NOT been published (Dream declined to share it).

---

## 2. Timeline

| Date | Event |
|---|---|
| 2026-07-01 → 07-04 | Attack campaign: 12 documented attack waves, up to 8 parallel sub-agents |
| 2026-07 (unspecified) | Taiwan MODA cybersecurity monitoring units detect the "abnormal attack" on government agencies |
| 2026-07-20 | Taiwan's National Institute of Cyber Security begins issuing warning alerts; investigation opens (per MODA statement via Reuters, 2026-08-13) |
| 2026-08-12 | **Dream publishes primary disclosure** (blog post); Financial Times — first outlet briefed — publishes, identifying Taiwan as the target |
| 2026-08-12 | The Register publishes "near-autonomous AI agents attack Taiwan's nuclear safety agency" |
| 2026-08-13 | **Taiwan's Ministry of Digital Affairs confirms**: AI-agent-assisted attacks (incl. OpenClaw) detected in July; investigation concluded; affected units remediated. Statement does not mention China |
| 2026-08-13 | CNN confirms reporting (CNN Tech, Aug 13) |
| 2026-08-13 | Reuters publishes MODA statement; notes Dream declined to share data or name the government |
| 2026-08-14 | SecureWorld publishes deep-dive ("first fully autonomous AI cyberattack on a government") |
| 2026-09-25 | Tom's Hardware publishes technical analysis of wave structure and self-correction |
| 2026-10-04 | undercodetesting.com publishes technical video analysis |
| 2026-10-05 | This report compiled |

**Note on the "July 20" question:** An internal hunt note (personas/grammarian/raw/dream-lane.md) flagged a possible date mismatch — MODA "said the activity it observed began July 20." The primary source (Reuters, quoting MODA's statement) actually says MODA **detected** the attack in July and **began issuing alerts on July 20**. These are compatible with Dream's Jul 1–4 window (detection sometime in July, alerts from Jul 20). The exact date MODA first observed activity is not publicly pinned down; treat "second incident vs. same incident" as unresolved but not contradictory.

---

## 3. Tooling and tradecraft

### 3.1 Framework composition

- **Hermes** (hermes-agent.org, Nous Research, MIT license, released Feb 2026): persistent AI agent with cross-session memory, terminal/command execution, tool integrations. Operates under workspace identifier `.hermes`.
- **OpenClaw** (openclaw.ai, launched Nov 2025): personal AI assistant platform (~340,000 GitHub stars in under six months per vibe-coding-security). Workspace identifier `.openclaw`.
- Both are free, open-source, downloadable without enterprise accounts. Dream: the attack required "no custom offensive software."
- **Model:** Dream identified **DeepSeek-V4-Flash** as part of the underlying model stack but explicitly cautioned it could not confirm it was the only model used. (SOFX/The Register: Dream "could not determine which underlying AI model powered the agents.")

### 3.2 Sub-agent structure and wave numbering

- Sub-agents carry **letter designations, Agent A through Agent Q** observed across the campaign; up to **8 deployed concurrently in a single wave** (dispatched in 3 batches), each assigned a distinct mission (reconnaissance, API enumeration, credential attacks, vulnerability validation, lateral movement, supply-chain targeting).
- **12 named attack waves** over ~4 days. Each wave produces structured after-action reports that feed planning for the next wave.
- Output volume — 1,395 files in ~4 days — is itself evidence of heavy automation.

### 3.3 The Bayesian decision engine (two layers)

Dream published the framework's explicit scoring methodology from the archive:

**Layer 1 — individual vulnerability scoring.** Every finding starts at an uninformative prior P=0.50, updated with explicit likelihood ratios: tool-scan positive LR+ = 6.0; manual curl confirmation LR+ = 10.0; impact assessment positive LR+ = 3.0; WAF/constraint present LR− = 0.30. Posterior thresholds: P>0.95 → confirmed exploitable; P>0.70 → high confidence; P>0.50 → queue for next wave; P<0.30 → discard.

**Layer 2 — attack chain scoring.** `P_success = P_chain × (1 − P_blocker)`, where P_chain = confirmed steps / total steps. Worked example (SSO lateral movement, rated 99%): 3/3 confirmed steps, blocker ~0.01 → P_success = 0.99. The framework later validated this: 98.8% of cracked accounts pivoted successfully.

### 3.4 Learning Cycles and self-correction

- **5 documented "Learning Cycles" (v1–v5):** autonomous sessions where agents search vulnerability databases, GitHub repos, and security publications for techniques applicable to the target — including dedicated sections on **country-specific products and documented CVEs** in the target government's systems.
- **Self-correction:** the final 12-wave summary lists **7 false positives** the framework caught itself. Signature example: a reported blind SQL injection (21-second delay interpreted as SLEEP(5)) was retested and found to be an **SMTP timeout** — reclassified and permanently excluded.
- Verification notation from the archive — `8个真实漏洞(物理确权+3+3交叉验证)` — means each confirmed finding required the discovering agent's verification plus **two additional rounds of three independent agent re-verifications** (six retests before confirmation).

### 3.5 Attack chain (per Dream's blog)

1. **Recon:** Downloaded and decompiled JavaScript bundles from an Angular-based government portal; extracted embedded URLs, API endpoints, OAuth client IDs, Keycloak config objects → **21 connected government systems**, full national SSO architecture (6 sub-realms, all OIDC endpoints, 2 RSA signing keys). One target: **36+ API endpoints**, many unauthenticated; one system exposed its **entire user database without authentication**.
2. **SDK harvesting (autonomous decision):** Followed a URL to a **GitBook documentation portal** hosting the national SSO integration guide; scraped it using GitBook's `llms.txt`/`index.md` features; obtained **Java Spring Boot and ASP.NET Core 8.0** SDK sample projects; ran AI static analysis (`Local-LLM-SAST-0day` methodology). None of the SAST findings translated to confirmed exploits — actual breaches came from server-side flaws (backdoor endpoints, unsigned JWT acceptance, unauthenticated APIs).
3. **Initial access (three parallel paths):**
   - **Authentication backdoors:** three hidden API endpoints accepting any request body and returning a valid authenticated session (exposed developer debug endpoints).
   - **Credential spraying:** usernames harvested from the unauthenticated users API; **Tesseract OCR solved the portal's CAPTCHAs at 100% accuracy**; predictable password patterns from employee IDs (capitalized/decorated usernames) → **85 accounts cracked** (initial 12, then 73 more as patterns were discovered).
   - **JWT signature bypass:** a government API accepted `alg: none` tokens.
4. **Lateral movement/persistence:** cracked credentials tested against every SSO-connected system (no MFA, no re-auth required via SSO bridge) → **84/85 accounts (98.8%)** reached the internal information system (dashboards, equipment management, personnel statistics). A **web shell** uploaded via unrestricted file upload but blocked from execution by Forms Authentication (partial success). **Persistent backdoors installed on government web applications.**
5. **Exfiltration:** 2,564+ personnel records (1,409 employees with name/department/SSO ID; 916 users from an unauthenticated API; **239 legal professionals from an unauthenticated Ministry of Justice endpoint**); full JSON export of all department users; 7 SSO client secrets; **6 internal DB credentials (MSSQL, Oracle, Sybase)**; internal network IP ranges.
6. **Supply-chain expansion:** parallel scanning of IT supply-chain vendors, a nuclear safety agency, a government email system, and 7+ energy companies for misconfigurations, exposed admin interfaces, and exploitable vulns. (SC Media: vendor targeting was "part of the design," not incidental.)

### 3.6 Guardrail bypass

The framework's own LLM refusals were bypassed by **framing all activity as "authorized penetration testing."** Dream: "Guardrails, the last practical constraint, hold only against operators who ask honestly." (Caveat from our own hunt work: the phrase "authorized penetration test" is generic pentest-skill boilerplate — stefanoratto/team7-hermes SKILL.md, strategic-automation/violin Hermes profiles — so it is a **weak standalone marker** of this specific tooling.)

### 3.7 Linguistic forensics

Code-switching between **Simplified Chinese in internal status reports** and **Traditional Chinese in target-facing analysis** → Chinese-language operator assessment. Dream did not go further; no group or nation-state attribution claimed.

### 3.8 Grammar extracted for hunting (from our personas)

- Agent self-labels: `Agent A`–`Agent Q` (note: this is also the default naming in OpenAI Swarm README / OpenClaw docs — weak as a live marker alone)
- 12 numbered attack waves with structured after-action reports
- Workspace identifiers `.hermes` / `.openclaw`
- Learning-cycle reports v1–v5; Bayesian scoring notation (`P_success`, likelihood-ratio tables)
- Verification notation: `8个真实漏洞(物理确权+3+3交叉验证)`

---

## 4. Evidence inventory

### What Dream recovered (primary evidence)
- The **complete operational workspace**: 1,395 files, ~160 MB, documenting the campaign in near-real time — attack plans, wave reports, learning-cycle research reports, triage/bayesian scoring reports, after-action summaries, exfiltrated data.
- Recovered during DREAM Lab's broader threat-tracking (exposed archive, not a victim-provided sample).

### What was independently verified
- **Taiwan MODA confirmation (2026-08-13):** AI-agent-assisted attacks (explicitly including OpenClaw) on government agencies detected in July; alerts from Jul 20; investigation concluded; affected units remediated. (Reuters, CNN.)
- **Target identity:** Financial Times identified Taiwan (Dream itself said only "government entities in Asia"); a person familiar with the attack confirmed Taiwan to The Register.
- **Scale/architecture:** no independent party has re-analyzed the archive (Dream declined to share it — Reuters). All technical detail traces to Dream's blog post.

### What remains unconfirmed
- **Attribution:** "China-linked" is a linguistic assessment (Simplified/Traditional code-switching), not a confirmed nation-state attribution. Dream: "cannot comment on the identity of the target or attacker" beyond the Chinese-language assessment. Taiwan's MODA statement did not mention China. CNN/F T framing: "suspected," not confirmed.
- **Model stack:** DeepSeek-V4-Flash "implicated" — Dream could not confirm it was the only model.
- **Whether the MODA-observed activity is exactly Dream's Jul 1–4 window** (the July-20-alert nuance above).
- vibe-coding-security grades the incident **status: unconfirmed** (no formal victim breach statement beyond MODA's general confirmation).

---

## 5. Related incidents (same tooling family — do not conflate)

| Incident | Window | Tooling | Distinctive facts |
|---|---|---|---|
| **Thailand Ministry of Finance** (Hunt.io + Bob Diachenko; disclosed 2026-07-23) | Jul 9–13, 2026 | Hermes in **"YOLO mode"** (approval prompts disabled) | 585 files / ~470 MB on exposed HK staging server (43.246.208[.]207); autonomous LinPEAS privesc, kernel-vuln checks vs "DirtyClone/Copy Fail/Dirty Frag" CVE classes; custom **Hades** implant (Go, Win PE + Linux ELF, AES-256-GCM, kill-dates); FOFA API key; ShadowPad/VShell infra history. ThaiCERT notified Jul 15. MOF has not confirmed. |
| **knaithe / KnYuan** (Unit 42; Jul 30, 2026) | Jul 30, 2026 | Hermes Agent + **DeepSeek** | Chinese-speaking operator; single Telegram command → **460+ targets** (Langflow, n8n, Marimo, NetScaler); sampled 25,209 Chinese n8n systems via FOFA. Tenable: "Agentic AI Threat Cluster." |
| **Gambit** (Gambit Security; Sep 22, 2026) | reported Sep 22 | (agent-assisted ops; Hermes extensively abused per ThreatDown) | **600k+ card records**; skimmers on **119+ sites**; exposed C2 **155.254.22.215**; ~$25/scan economics; models via OpenRouter. |
| **CARBONATO** (ThreatDown/Malwarebytes; Sep 24–25, 2026) | evidence Oct 2024 → Aug 2026 | **Hermes Agent "GH0ST"** | Worm-like botnet via unauthenticated Docker daemons (port 2375): privileged container, reverse SSH, cron/systemd/rc.local/OpenRC persistence, /24 scans every 5 min. Installs Hermes with a **39-line GH0ST prompt overwriting `SOUL.md`**; Telegram C2 ("interactive command loop"); **steals AI API keys** (OpenAI, Anthropic, Google, OpenRouter, Together, Groq, Mistral, Cohere) to fund an operator LLM gateway (observed at 213.136.83.197, 12 models). 59 repos / 4.3 GB image data from open registry; loot in `/root/.hermes/loot/`. Costa Rica possible-operator link, inconclusive. |

**Cross-check vs. our Amap/`uq` corpus:** zero marker overlap (no `uq` grammar, no lhr.life, no DeepSeek/Hermes/OpenClaw strings, no gov.tw). Different species: Dream swarm = offensive intrusion; ours = data collection. (Corpus cross-check 2026-10-05: all zero.)

---

## 6. Publication status

**Has this been published? YES.**

- **Primary disclosure (published):** Dream Research blog, 2026-08-12 — "Inside a Multi-Agent AI Framework Used to Compromise Government Entities in Asia" (dreamgroup.com). Full technical anatomy: attack chain, Bayesian scoring tables, learning cycles, self-correction, linguistic analysis. Dream shared details with the Financial Times first.
- **First media / target identification:** Financial Times, 2026-08-12 (identified Taiwan; Dream itself did not name it).
- **Victim confirmation (published):** Taiwan Ministry of Digital Affairs statement, 2026-08-13 — confirmed AI-agent-assisted attacks (OpenClaw named) detected in July; alerts from Jul 20; investigation concluded; units remediated. Reported by Reuters, CNN, The Register, CSO Online.
- **Secondary writeups:** The Register (Aug 12), CSO Online, CNN (Aug 13), Tom's Hardware (Sep 25), cybersecuritynews.com (two pieces), webpronews, techtimes, secureworld.io (Aug 14), cryptobriefing, sofx.com, SC Media (perspective), ai-gov-research digest, undercodetesting.com (technical video analysis), cybershujin threat-actor tracker, orca-ai-incident-archive.
- **Third-party advisory:** pranava0x0/vibe-coding-security advisory `2026-08-taiwan-dream-autonomous-ai-agent-attack` (status: unconfirmed).

**What has NOT been published:**
- The **raw 160 MB / 1,395-file archive** — Dream declined to share it (Reuters: "declined to share the data or name the government"). No mirror found (our hunt: "reporting-only").
- Any victim-side forensic report beyond MODA's statement.
- Formal nation-state attribution.

---

## 7. All evidence and seen URLs

### Primary sources (establish the facts)
- https://dreamgroup.com/blog/inside-a-multi-agent-ai-framework-used-to-compromise-government-entities-in-asia — **Dream's primary technical disclosure.** Establishes: 1,395 files / 160 MB archive; Hermes + OpenClaw; Agent A–Q, ≤8 concurrent; 12 waves, Jul 1–4; Bayesian two-layer scoring (with LR tables and formula); 5 Learning Cycles; self-correction (SMTP-timeout false positive; 8个真实漏洞 notation); attack chain steps 1–6 incl. SDK harvesting via GitBook llms.txt, Tesseract 100% CAPTCHA, 85 accounts (12+73), 84/85 pivoted, 2,564+ records breakdown, 7 SSO secrets, 6 DB creds, web shell blocked, persistent backdoors, supply-chain expansion; "authorized penetration testing" guardrail bypass; Simplified/Traditional code-switching → Chinese-language operator; responsible disclosure (victims notified pre-publication).
- https://www.reuters.com/world/china/taiwan-says-it-was-targeted-last-month-ai-driven-hacking-campaign-2026-08-13/ — **MODA confirmation.** Establishes: Taiwan detected AI-assisted attacks in July; alerts from Jul 20; OpenClaw named; investigation concluded; units remediated; Dream declined to share data; FT first identified Taiwan.
- https://www.ft.com (Financial Times, 2026-08-12) — first outlet briefed; identified Taiwan as target. (Paywalled; cited via Reuters/Register/CNN.)

### Independent press corroboration
- https://www.theregister.com/security/2026/08/12/near-autonomous-ai-agents-attack-taiwans-nuclear-safety-agency/5287055 — Establishes: 85 accounts / 2,500+ records per Dream; archive size; Hermes+OpenClaw; 8 sub-agents × 12 waves; 36+ API endpoints on one target; unauthenticated user DB; three hidden API endpoints returning valid sessions; CAPTCHA 100%; 2,564 records; 7 SSO secrets; 6 DB creds (MSSQL/Oracle/Sybase); supply-chain pivot; person familiar confirmed Taiwan; Dream doesn't attribute to Chinese government.
- https://www.csoonline.com/article/4209210/ai-agents-wage-near-autonomous-cyberattack-on-asian-government-networks.html — independent corroboration of disclosure, archive size, sub-agent structure, jailbreak framing (cited in advisory).
- https://www.cnn.com/2026/08/13/tech/china-taiwan-ai-agent-cyberattack-intl-hnk — CNN confirmation (Aug 13): 8 agents (OpenClaw, Hermes), 21 systems mapped, 85 accounts, 2,500 records, nuclear/energy expansion; "first disclosed fully automated attack on a government."
- https://www.tomshardware.com — third independent source; additional detail on wave structure and self-correction behavior (cited in advisory).
- https://cybersecuritynews.com/eight-ai-agents-breach-government-systems/ — Establishes: 160 MB / 1,395 files; 12 waves Jul 1–4; Hermes+OpenClaw; 8 sub-agents (recon, credential attacks, API testing, data collection, lateral movement); Simplified-internal/Traditional-target linguistic split; Dream did not identify entities or operator.
- https://cybersecuritynews.com/chinese-hackers-target-taiwan-using-ai/ — Establishes: first fully autonomous cyberattack framing; 160 MB archive found during broader threat-tracking; agents reprioritized paths autonomously.
- https://www.webpronews.com/suspected-chinese-hackers-unleash-ai-agent-swarm-on-taiwan-government-systems/ — Establishes: Agent A–Q labeling; SSO architecture mapping (6 sub-realms, OIDC endpoints); adaptation without commands.
- https://www.techtimes.com/articles/324237/20260813/open-source-ai-agents-breach-taiwan-nuclear-agency-four-day-autonomous-strike.htm — Establishes: Hermes (Nous Research, Feb 2026) + OpenClaw (Nov 2025, 340k stars) background; "what made the attack work was not the model — it was the prompt."
- https://www.secureworld.io/industry-news/first-fully-autonomous-ai-cyber-attack-government — Establishes: MODA statement details (monitoring spotted in July, advisories from Jul 20, investigation concluded); SSO client secrets + internal DB credentials among loot.
- https://cryptobriefing.com/multi-agent-ai-framework-government-breach/ — Establishes: 2,564 records, 85 cracked credentials, Bayesian probabilistic scoring, 1,395 files.
- https://www.sofx.com/suspected-china-linked-hackers-carried-out-autonomous-ai-attack-on-taiwan/ — Establishes: Dream blog post Aug 12; 1,409 employees (names/departments/SSO IDs) + hundreds more users and legal professionals; Learning Cycles detail; "authorized penetration test" bypass; CSO Amir Becker (ex-Unit 8200) quote; 2.6M China-origin attacks/day on Taiwan in 2025 (NSB).
- https://www.scworld.com/perspective/the-taiwan-attack-was-built-with-two-free-downloads-from-vendors-nobody-rates — Establishes: supply-chain vendor targeting was "part of the design"; proliferation-math argument (two free frameworks + orchestration).
- https://www.youtube.com/watch?v=LWxKKDrnQBE — undercodetesting technical video: portal recon, auth-config extraction, 85 accounts, 2,500+ records, nuclear regulator pivot; MODA confirmed Aug 13; guardrails consent-based not behavioral.

### Advisory / tracker sources
- https://github.com/pranava0x0/vibe-coding-security/blob/HEAD/advisories/2026-08-taiwan-dream-autonomous-ai-agent-attack.md — third-party advisory; date_disclosed 2026-08-12; status: unconfirmed; DeepSeek-V4-Flash implicated (unconfirmed as sole model); links Dream report to Thailand/JADEPUFFER/Claw-Chain/ClawHavoc advisories.
- https://github.com/pranava0x0/vibe-coding-security/blob/HEAD/advisories/2026-07-hermes-hades-thailand-finance-ministry.md — Thailand MoF advisory (Hermes YOLO mode, Jul 9–13, Hunt.io/Diachenko, 585 files/470 MB, Hades implant, disclosed Jul 23).
- https://github.com/githendrik/ai-gov-research/blob/HEAD/docs/2026-08-17-ai-governance.md — AI Governance Weekly Digest (Aug 17): cites CNN reporting Dream/MODA/FT; "first disclosed fully automated attack on a government."
- https://github.com/cybershujin/Threat-Actors-use-of-Artifical-Intelligence/pull/18 — threat-actor tracker: Dream Taiwan row (untrusted→skeptic-passed, high confidence; Aug 2026; Jul 1–4); contextualizes alongside GTIG/UNC5792/RAVINE CASTLE/CL-CRI-1131.
- https://github.com/continuum-ai-corp/orca-ai-incident-archive/blob/HEAD/incidents/2026-09/2026-09-22-carbonato-docker-hermes-agent-botnet.md — CARBONATO archive entry; lists Taiwan Dream swarm as first of five Hermes-agent cases (then Thailand Jul 30, Unit 42 Jul 30, Gambit Sep 22).

### Related-incident press
- https://www.bleepingcomputer.com/news/security/new-carbonato-malware-uses-ai-agents-to-hijack-exposed-docker-hosts/ — CARBONATO: Docker 2375, GH0ST agent, SOUL.md overwrite, Telegram C2, AI-API-key theft.
- https://www.decryptiondigest.com/blog/carbonato-docker-botnet-hermes-ai-agent — CARBONATO: /root/.hermes/loot/, 39-line GH0ST persona, operator LLM gateway at 213.136.83.197.
- https://gbhackers.com/docker-servers-hijacking/ — CARBONATO: watchdog re-pull persistence; SOUL.md entry-point line.
- https://particle.news/story/carbonato-botnet-hijacks-exposed-docker-hosts-to-run-ai-powered-gh0st-agents — CARBONATO: stolen keys fund operator LLM gateway.
- https://mallory.ai/stories/01a0cea1-273f-711d-9033-7343db01e135 — CARBONATO timeline; Costa Rica link inconclusive.
- https://zot.news/article/new-carbonato-malware-uses-ai-agents-to-hijack-exposed-docker-hosts-mug2rs8i — CARBONATO summary.
- (Unit 42 knaithe/KnYuan and Gambit details: from OSINT-Expert persona sweep, 2026-10-05 — no separate primary fetch this session; treat as second-hand pending primary verification.)
- https://d33gy59ovltp76.cloudfront.net/news/suspected-china-linked-hackers-used-ai-to-run-the-first-ever-end-to-end-autonomous-cyberattack-on-taiwans-government-israeli-firm-says-open-source-built-tool-continuously-devised-effective-hack-strategies-in-real-time — Tom's Hardware mirror: 160 MB archive during broader threat-tracking; Hermes+OpenClaw; ≤8 agents; 21 systems; nuclear agency + 7 energy companies.

### Local hunt notes (internal; not public evidence)
- `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/grammarian/raw/dream-lane.md` — Dream-grammar marker verdicts; MODA date-mismatch lead; "authorized pentest" = weak marker (generic skill boilerplate).
- `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/model-whisperer/FINDINGS.md` — model-attribution table (DeepSeek-V4-Flash implicated, unconfirmed); jailbreak-framing variants; SOUL.md-overwrite fingerprint (CARBONATO).
- `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/osint-expert/FINDINGS.md` — knaithe/KnYuan, Gambit, PixelLeak, OpenAI US-gov probing, MemTensor extractions.
- `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/mimic/FINDINGS.md` and `raw/other-operators.md` — Taiwan mentions in operator-modeling context.
- `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/historian/FINDINGS.md` — timeline context.
- `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/night-owl/FINDINGS.md` — Dream swarm contrast (Wed Jul 1 → Sat Jul 4, human-directed offensive shape).
- `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/raw/lanes/osint/FINDINGS.md` — earlier osint lane Taiwan mentions.
- `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/full-sweep/FINDINGS.md` + `full-sweep/raw/social-search.md` — Dream swarm found via social search; zero corpus overlap.

---

*End of report. Nothing pushed. Scope held: agents and infrastructure only.*
