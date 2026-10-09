# ADVERSARY — Round 2 findings

*Red-team reviewer. Chair: Hunter S. Thompson. Filed 2026-10-05.*
*Two verdicts hunted: (1) beeceptor/pipedream HUMAN-KIT-SHAPED; (2) HARNESS_LOG_MAP.md 7-of-10 leak-by-default.*
*Evidence grades: OBSERVED = our bytes; PUBLIC SOURCE = cited; INFERENCE = labeled. Novelty: OURS / KNOWN / GENUINELY NEW.*

---

## LANE 1 — beeceptor/pipedream-report.md: HUMAN-KIT-SHAPED verdict

### Finding A1 — Kill attempt on the "agent mints nonces" premise: WOUNDED, verdict survives weakened

**Claim:** The report's discriminating premise — "a human mashes keys; an agent mints structured nonces" — is fleet-circular and cannot exclude agents in general.

**Evidence:**
- The rubric defines AGENT-SHAPED as "carries **our documented** agent nonce/marker grammars (zz=oai, epoch nonces, uqscan tagwords)". That is our fleet's launcher tradecraft, not a property of agents. An LLM instructed to invent a throwaway subdomain emits lowercase letter runs — exactly the shape of `akwuwue`, `hhshdh`, `ahshsu`. No measurement of LLM-generated random-subdomain output was offered to support the "agent wouldn't do this" leg. (INFERENCE — grounded in LLM output behavior; the report asserts the negative without comparative evidence)
- The payload-grammar decode (§5c) matches "the public XSS cookie-grabber one-liner family … documented in every XSS cheat-sheet since the mid-2000s." That canonical form is equally the most likely output of an LLM asked to test XSS exfil. The grammar discriminates *generic-XSS-ness*, not *human-ness*. (INFERENCE)
- Full infra-sweep data reviewed: 16 beeceptor + 49 pipedream urlquery reports (OBSERVED — `infra-sweep/raw/beeceptor.com.json`, `infra-sweep/raw/pipedream.net.json`). Zero agent-shaped counter-examples: no zz=oai, no epoch nonces, no harness grammar anywhere in the URL families. The keyboard-mash class has human continuity back years (`asdas`/`asdasd` 2024-10-29, `testdsd.free.beeceptor.com/xsspoc` 2023-10-27).

**What survives for HUMAN-KIT-SHAPED:** `hjhjhjhj` strict home-row alternation is a human motor pattern, not a typical LLM output shape; `/grabber.php` + `</script>` breakout is kit convention; the 26-day cluster with consistent style reads as one operator; `/Oneotsuka` is odd-human labeling; the surface's documented abuse record is exclusively human (§4). None of this is agent-positive.

**Classification:** INFERENCE built on OBSERVED data. Novelty: OURS (re-analysis of our bytes).

**Actionability:** Amend the report's §6: the honest grade is **NOT-OUR-FLEET, human-kit-consistent, agent-not-excluded** — the current wording overclaims dispositive power. The verdict survives as the best-supported grade, but the "agent mints nonces" leg must go.

**What would change my mind (toward agent-shaped):** (a) a beeceptor/pipedream receiver URL co-occurring with zz=oai / epoch-nonce / uqscan grammar; (b) an agent skill, harness doc, or trace referencing beeceptor/pipedream as an exfil target; (c) submitter-side metadata tying the urlquery submissions to agent infra (not available in public urlquery data — standing honest null).

### Finding A2 — Correction to the record: the pipedream surface was NOT frozen since May 4

**Claim:** Round 1's honest null "pipedream-infra frozen since May 4" is contradicted by our own infra-sweep bytes.

**Evidence (OBSERVED — `infra-sweep/raw/pipedream.net.json`):**
- `eoqdkld34574c7.m.pipedream.net` scanned 2026-07-10
- `eoubuki2x8vmkry.m.pipedream.net` scanned 2026-08-10
- `eo6p96x7ax0vcaj.m.pipedream.net/Oneotsuka` scanned 2026-09-03 (the report's #6)
- Additionally `eobb5owjuxe1ejb.m.pipedream.net` scanned **2026-05-04 — inside the beeceptor cluster window (Apr 24–May 20)**. The report frames pipedream as a 4-month-separated outlier; the surface had an in-window hit that deserved discussion, not a footnote.

**Classification:** OBSERVED. Novelty: OURS (already in our infra-sweep, under-discussed by the report).

**Actionability:** Strike "pipedream-infra frozen since May 4" from Round 1 honest nulls (GRADES.md); amend report §2 temporal cluster and §6 to account for the 2026-05-04 in-window pipedream hit. Does not kill the HUMAN-KIT verdict — subdomains are provider-minted, no operator signal either way — but the timeline framing was wrong.

### Finding A3 — Supporting observation (strengthens human-kit, does not discriminate the cluster)

**Claim:** The pipedream surface carries confirmed human phish-kit exfil in our own sweep data.

**Evidence (OBSERVED — `infra-sweep/raw/pipedream.net.json`, 2024-08-14):**
`eocbe4jqi9zc1ss.m.pipedream.net/?sqtr=lisa.haggerty+&cjefr_1=Bnymellon+&2pCR=bGlzYS5oYWdnZ` — base64 `bGlzYS5oYWdnZ` decodes to `lisa.hagg`; victim PII plus BNY Mellon lure = human phishing-kit exfil grammar on the same dead-drop surface.

**Classification:** OBSERVED. Novelty: GENUINELY NEW (not in the report).

**Actionability:** Log as supporting context in the report's §4 (abuse record). Establishes the surface's human-kit dominance; not evidence about the Apr–May 2026 cluster specifically.

### Finding A4 — "No public precedent for agent-driven use" — sub-claim SURVIVES

**Claim:** Tried to find any public documentation of agents using beeceptor/pipedream as exfil infra. Found nothing.

**Evidence:** Web search for agent + beeceptor/pipedream exfiltration surfaced only the Palisade LLM-honeypot paper (detecting agents, not their infra) and agent-security vendor material — no agent-driven use of either service. (PUBLIC SOURCE — null result, searched 2026-10-05)

**Classification:** Honest null (first-class). Novelty: n/a.

**Actionability:** Report §8 thread 4 stands. The "surface is the finding" framing remains the report's strongest contribution.

---

## LANE 2 — HARNESS_LOG_MAP.md: the 7-of-10 leak-by-default verdict

### Finding B1 — KILL: Gemini CLI "YES" — telemetry is OFF by default

**Claim:** The map's Gemini CLI YES rests on a moot default. Official docs: `telemetry.enabled` defaults to **false**.

**Evidence (PUBLIC SOURCE):**
- Official Gemini CLI configuration docs, current: default `"telemetry": {"enabled": false, "target": "local", "otlpEndpoint": "http://localhost:4317", "logPrompts": true}` — https://geminicli.com/docs/reference/configuration/ (fetched 2026-10-05; `logPrompts` default-true confirmed at L4115, `target` local/gcp at L4105)
- Corroborated by multiple gemini-cli doc forks (667700996, zed-industries, quixiai, aiimzfyr, junyang-tes, mondaychen — all `{"enabled": false, ...}`) and the volli-code observability survey: "**Off** (`telemetry.enabled = false`)".
- The map's compounding claim (1) — "`logPrompts` defaults to true — prompt/response content goes into OTel log spans" — is true but inert: with `enabled: false` nothing is exported. It only matters on opt-in. `usageStatisticsEnabled` defaults true, but that channel carries usage stats, not prompt content.

**Classification:** PUBLIC SOURCE (official vendor docs). Novelty: KNOWN publicly, GENUINELY NEW to our record (the map got it wrong).

**Actionability:** Amend HARNESS_LOG_MAP.md: Gemini CLI → **PARTIAL** (plaintext local transcripts `tmp/<project_hash>/chats/*.jsonl` + plaintext `oauth_creds.json` persist locally; no off-box content channel by default). Headline recount loses one YES.

### Finding B2 — KILL (structural): "leak-by-default" conflates local persistence with off-box exfiltration

**Claim:** The verdict column isn't measuring one thing. Local plaintext on disk and content leaving the box are different threat models, and the 7-of-10 headline is driven by counting the former as "leak".

**Evidence (PUBLIC SOURCE — official Anthropic docs fetched 2026-10-05, https://code.claude.com/docs/en/data-usage.md):**
- "Metrics: latency, reliability, and usage patterns… **Metrics never include your code, prompts, or file paths**." Error reports redact secrets/paths before anything leaves the machine. `/feedback`, `/bug`, `/share`, and the survey transcript-share are all explicitly user-initiated opt-in ("Nothing is uploaded unless you explicitly select Yes"). Prompts reach Anthropic's API because inference requires it — that is API usage, not a leak defect.
- The only default is plaintext **local** transcripts (`~/.claude/projects/`, "to enable session resumption"). Local disk is not exfiltration: anyone with local read access already owns the machine.
- Same structural point applies to Cline, Continue, Codex CLI (map itself notes Codex OTel is opt-in; anonymous metrics claim no PII), and the plaintext-credential legs of Gemini CLI/OpenHands. The map's own actionability line ("any indexed or exfiltrated copy of these paths is a full transcript") is about open-directory indexing — a legitimate hunt surface — but "leak-**by-default**" implies the harness does the leaking, which for local-only persistence is false.

**Recount on a strict off-box-content standard:**
- YES: Cursor (individuals — Privacy Mode OFF default, providers may retain/train; confirmed by official https://cursor.com/help/security-and-privacy/privacy: "For teams, Privacy Mode is enabled by default" — individuals must toggle), Windsurf (individuals — ToS training-use, self-serve opt-out needed per marktechpost Sep 2026 contract review). **2 of 10, not 7.**
- On a pure local-persistence standard the count is 9-of-10 (OpenClaw's plaintext `openclaw.json` keys and Aider's chat history also qualify), which makes "7" arbitrary. The map mixes the two standards per-row — Claude Code counted for local persistence, Cursor counted for off-box.

**Classification:** PUBLIC SOURCE + INFERENCE (methodological). Novelty: GENUINELY NEW to our record.

**Actionability:** Split the verdict into two columns — "persists content locally by default" vs "transmits content off-box by default" — and relabel the headline. The hunt-relevant output (directory grammars for open-index watching) is unaffected and stays.

### Finding B3 — WOUND: Aider "YES (git-remote risk)" — aider auto-gitignores `.aider*` by default

**Claim:** The map's mechanism — "only excluded from git if the user manually adds the aider history patterns to .gitignore" — is factually wrong. Aider does it automatically.

**Evidence (PUBLIC SOURCE):** Multiple independent sources: "Aider otherwise writes `.aider*` into .gitignore on startup" (amelnagdy/delegate-skills; xiehuan123/awesome-skills SKILL.md: "The relay also passes `--no-gitignore`, because Aider otherwise writes `.aider*` into `.gitignore` on startup"); the `--no-gitignore` flag exists precisely to disable this. `--chat-history-file` default `.aider.chat.history.md` confirmed (official options doc mirror).

**Classification:** PUBLIC SOURCE. Novelty: KNOWN publicly, GENUINELY NEW to our record.

**Actionability:** Downgrade Aider to **PARTIAL** (plaintext local history persists; the git-remote vector is auto-mitigated by default — residual risk only via `--no-gitignore`, force-adds, or non-git repos). Amend HARNESS_LOG_MAP.md §5.

### Finding B4 — Legs that SURVIVE (no kill)

- **Cursor individual YES:** Privacy Mode OFF default for Free/Pro confirmed by official docs and arsturn ("code can be used for training"); local `state.vscdb` persists regardless. The training-use leg is policy-document-based, not observed transmission — note the epistemic status — but the default-off fact holds.
- **OpenHands YES:** plaintext `secrets.json` absent `OH_SECRET_KEY` confirmed by OpenHands issue #3989 (public, with observed plaintext shape) — survives on the plaintext-credentials leg.
- **Windsurf YES (individuals):** ToS training-use with self-serve opt-out corroborated by Sep 2026 contract review (marktechpost). The encrypted-at-rest cascade files rest on community RE (binary-shipped key) — epistemically weaker, keep the RE-sourced caveat the map already carries.
- **Codex CLI:** local plaintext rollouts + default-on anonymous metrics (no PII claimed) — survives as PARTIAL under the split-verdict scheme, not YES.

**Classification:** PUBLIC SOURCE. Novelty: KNOWN.

---

## Verdict scorecard

| Target | Verdict under attack | Outcome |
|---|---|---|
| Beeceptor/pipedream HUMAN-KIT-SHAPED | Kill | **SURVIVES, wounded** — downgrade wording to "NOT-OUR-FLEET, human-kit-consistent, agent-not-excluded"; the nonce-premise leg is dead |
| "No agent-driven precedent" sub-claim | Kill | **SURVIVES** — still no public precedent found |
| Round 1 "pipedream frozen since May 4" null | Correction | **KILLED by our own bytes** — 2026-07-10, 2026-08-10, 2026-09-03 hits; plus an in-window 2026-05-04 hit |
| Harness 7-of-10 leak-by-default | Kill | **KILLED as stated** — Gemini CLI drops on false telemetry default (B1); the column conflates two threat models (B2); recount is 2-of-10 off-box / 9-of-10 local-persistence |
| Aider YES (git-remote risk) | Kill | **WOUNDED → PARTIAL** — auto-gitignore defeats the mechanism by default |

**Amendments owed:** HARNESS_LOG_MAP.md (Gemini CLI verdict, Aider mechanism, split verdict columns, headline recount); beeceptor-pipedream-report.md §2/§6 (timeline, grade wording); GRADES.md Round 1 honest nulls (pipedream frozen claim).
