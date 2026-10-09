# KEYMISTRESS — Cryptographer analysis of skill-egress primitives

Persona: KEYMISTRESS (cryptographer). Date: 2026-10-05.
Study: `studies/skill-egress-top500/` (EGRESS_MAP.md + SKILLS.md + raw/scan-{a,b,c}.json + fetched repos under `~/workspace/skill-egress-work/`).
Scope: security properties of each egress primitive — what trust is placed and in whom, failure modes, exfil-vs-legitimate ambiguity. NOT liveness (hacker's lane). Read-only analysis; no credential was used, tested, or validated.

## Epistemic key

- **OBSERVED**: bytes present in the study files or fetched repos (paths/lines cited).
- **INFERENCE**: my cryptographic analysis. Labeled as such.
- Evidence-integrity note (OBSERVED): tool display layers mask contiguous `ghp_` + 20 alphanumerics as `<redacted>`. The underlying file bytes are complete — verified via `od -c` on source lines. All secret-shaped values below were triaged from raw bytes, not from masked renders. EGRESS_MAP.md's rendering `ghp_LOKIWITHHELD*INVALID` is lossy: the true sentinel prefix (OBSERVED, run.sh via `od -c`) is `ghp_` + `LOKIWITHHELDsentinel`, with runtime constructions appending `$RANDOM$RANDOM` / pid+hex and a terminal `INVALID`.

---

## P1. ngrok / cloudflared tunnels (agent-exposed localhost)

**OBSERVED** (EGRESS_MAP.md): confirmed in loki-mode (parses public URLs from ngrok API + cloudflared logs), pinme (instructs agent to expose localhost), telnyx-mcp (`--ngrok-enabled` agent-controllable tunnel, 390K/wk installs), browser-use (QA docs reference ngrok/cloudflared).

**Trust placed, in whom (INFERENCE):**
- The agent places its *entire localhost attack surface* in the hands of the tunnel broker (ngrok Inc / Cloudflare). The broker terminates TLS at its edge (it holds the certs for `*.ngrok.io`, `*.ngrok-free.app`, `*.trycloudflare.com`) and re-encrypts down the tunnel — so the broker sees connection metadata (SNI/host, timing, volume, source IPs) always, and sees **payload plaintext whenever the agent serves plain HTTP locally** (the common case: agent exposes a local HTTP debug server, admin UI, or file server; edge TLS termination means the broker reads it all). Only a TCP-tunnel carrying the agent's own end-to-end TLS hides payloads from the broker.
- Trust is also placed in *URL secrecy*: the public URL (random subdomain, unguessable but not a secret — it is printed to dashboards, APIs, logs; loki-mode literally parses it from the ngrok API, widening every place the URL is handled) is the sole access control. There is no authentication on the exposed port by default. **Anyone with the URL reaches the agent's localhost.**
- Failure modes: (a) local services never meant to be public (debug ports, notebook servers, admin UIs, `/env` endpoints) become internet-facing; (b) URL disclosure via logs, error messages, screenshots, or the ngrok dashboard API = instant unauthenticated inbound access; (c) broker compromise or lawful-compulsion = full traffic visibility; (d) the agent's egress IP and tunnel URL jointly fingerprint the operator's machine.

**Ambiguity:** HIGH — tunneling is standard dev tooling; the signal is in *what* is exposed and *to whom*, not in the binary's presence.

---

## P2. r.jina.ai (keyless reader proxy)

**OBSERVED**: keyless `JINA_READER_PREFIX` fallback in 6 skills (last30days-skill, twitter-reader, trendradar, deep-research-mcp, gpt-researcher, sjh110007/mcp-jina-ai). Study notes our 2026-10-03 skill-ladders lane judged keyless r.jina.ai DEAD as of now.

**Trust placed, in whom (INFERENCE):**
- TLS between agent and `r.jina.ai` protects against the *local* network — but the proxy **terminates TLS and fetches the origin itself**. Jina (the operator) therefore sees every fetched URL **in plaintext**, including query-string secrets agents constantly fetch: API keys in params, signed URLs, session tokens, password-reset links. Response bodies likewise pass through the proxy in the clear.
- The agent **cannot verify origin TLS** through the proxy: no pinning is possible, and the agent cannot tell whether the proxy fetched the origin over HTTPS, accepted an invalid cert, or downgraded to HTTP.
- Profiling: the proxy operator gets the agent's complete reading list (URLs, timing, source IP, user agent) — a full behavioral profile of the agent's tasking. Keyless = no authentication, so the agent's *own operator* gets no audit trail either.
- Failure modes: (a) silent third-party tap on every fetch — the fallback is keyless and silent, so neither the agent's user nor its operator may know URLs are being routed through Jina; (b) query-string credential disclosure to a third party at scale; (c) if the keyless endpoint is dead (per the 2026-10-03 lane), agents with a hardcoded fallback may fail open to other fetch paths or leak the *attempt* metadata.

**Ambiguity:** HIGH — reader proxies are legitimate readability tools; the exfil signal is the *silent keyless routing of sensitive URLs*, not the fetch itself.

---

## P3. Discord / Slack webhooks (dead-drop grammar)

**OBSERVED**: confirmed in loki-mode (`hooks.slack.com` + `discord.com/api/webhooks` in notify.sh), last30days (Slack webhook alerts), quantdinger (trading-signal notifier POSTs to Discord+Slack+Telegram). webhook.site: **zero** hits across all 3,853 units.

**Trust placed, in whom (INFERENCE):**
- A webhook URL **is a bearer credential**. Discord: `discord.com/api/webhooks/{id}/{token}` where the token is 68 chars from the base64url alphabet ≈ **408 bits of entropy** — unguessable by brute force; the threat is *disclosure*, never guessing. Capabilities conferred by the token: execute the webhook (POST messages with arbitrary username/avatar override), plus GET/PATCH/DELETE the webhook object itself (reveals channel/guild IDs — minor info disclosure; allows silent deletion = DoS on the alerting path). It does **not** confer channel-history read.
- Slack incoming webhooks: `hooks.slack.com/services/T…/B…/{24-char secret}` — the secret is the final 24-char alphanumeric segment ≈ **143 bits**; POST-only to one fixed channel; on leak the attacker can inject messages, nothing more.
- On leak, the attacker gains **impersonation of the bot identity**: they can post as the agent's notifier into the operator's channel — forged alerts, forged "all clear", social-engineering the human in the loop — and can delete the webhook to blind the operator.
- Failure modes: (a) webhook URL committed to a repo/skill file = public bearer credential; (b) the channel becomes an exfil path the *agent itself* legitimately uses — DLP sees "bot posted a message", not "data left the building"; (c) message content (embeds, attached images/files) carries arbitrary bytes out.

**Ambiguity:** MEDIUM — alerting via webhook is legitimate; the dead-drop signal is *what* gets posted and *where the URL lives* (hardcoded in a shipped skill vs operator-configured).

---

## P4. uploads.github.com (GitHub trusted image host)

**OBSERVED**: klavis MCP servers wire `uploads.github.com` as upload host (Go client); gitshot→GitHub Release Asset + catbox.moe grammar propagates byte-identically into trekawek/coffee-gb.

**Trust placed, in whom (INFERENCE):**
- Upload requires a GitHub credential (PAT/app token with upload scope) — **the token is the real secret at risk**, not the URL. The resulting asset URL (`github.com/user-attachments/assets/<uuid>`) is publicly fetchable with no authentication: the UUID (~122 bits) is unguessable but the URL is a *bearer link* — anyone holding it downloads the bytes.
- GitHub (the operator) sees content, uploader identity, and access logs. The uploader can delete via API, but copies made while public persist.
- The laundering property: the asset inherits **github.com's trusted origin**. Any allowlist, CSP, or naive domain filter that trusts github.com is bypassed — an agent can smuggle arbitrary bytes (screenshots, archives, staged payloads) through a "trusted" domain. This is exactly the gitshot grammar the study confirmed.
- Failure modes: (a) token scope creep — the PAT that uploads images can usually do far more; (b) asset URLs are forever-shareable once disclosed; (c) content moderation is GitHub's, not the agent operator's — takedown is out of the agent's hands.

**Ambiguity:** MEDIUM — asset hosting is normal; the laundering signal is the *content* plus *who holds the link*.

---

## P5. catbox.moe (no-signup file host)

**OBSERVED**: gitshot (screenshot→catbox fallback), byte-identical copy in coffee-gb.

**Trust placed, in whom (INFERENCE):**
- **Uploader anonymity is pseudonymous, not anonymous**: no account is required, but the operator logs the uploader's IP — that IP is the single attribution thread linking agent → upload. The operator (and any CDN in front, e.g. Cloudflare) sees content + uploader IP + downloader IPs.
- Filenames are short random strings (~7 chars base36 ≈ 36 bits) — not a secret against bulk enumeration, but impractical to target; the URL is effectively a bearer link for anyone who has it.
- Retention is long (effectively permanent absent abuse reports), so the dead-drop persists.
- The dead-drop shape: **upload from the agent's IP, download from anywhere**. The two ends are unlinkable except via the operator's logs — which is precisely why it works as tradecraft and precisely where attribution lives.

**Ambiguity:** MEDIUM-HIGH — anonymous hosting is the product; the signal is usage pattern (programmatic screenshot→upload pipelines), not the host.

---

## P6. sci-hub.se with verify=False (TLS-bypassed fetch)

**OBSERVED**: paper-search-mcp-openai (lane E) sets `verify=False` on Sci-Hub fetches. Four `verify=False` findings total (gpt-researcher, hexstrike-ai, xhs-downloader, paper-search-mcp-openai).

**Trust placed, in whom (INFERENCE):**
- `verify=False` disables TLS certificate verification: **any on-path actor** (hostile Wi-Fi, compromised router, ISP, corporate middlebox) can transparently MITM the connection — reading and *modifying* requests and responses with no warning.
- Data at risk is not the papers (low sensitivity) but **response integrity**: a MITM can return a malicious PDF, and PDF parser exploits in the agent's toolchain turn a fetch into code execution. Request URLs are also visible (SNI + full URL to the MITM).
- The deeper risk is the **habit**: `verify=False` shipped in a skill normalizes disabling TLS verification; agents and users copy-paste the pattern into API calls where `Authorization` headers *do* flow — at which point the MITM harvests live credentials.
- A skill that disables verification has also surrendered **server authentication**: the agent cannot know it is talking to sci-hub.se at all.

**Ambiguity:** LOW on the TLS part (`verify=False` in shipped code is never legitimate) — but the *fetch target* (papers) is mundane, which is why it survives review.

---

## P7. Email — JMAP send + blob attachments (Atomic Mail)

**OBSERVED**: Atomic-Mail atomic-mail-agentic (lane E) — autonomous email send + RFC 8620 blob attachments; anon.li + Atomic Mail Agentic listings (lane B).

**Trust placed, in whom (INFERENCE):**
- The agent holds **send-capable credentials for a real mailbox**. Email is the highest-trust identity primitive here: messages leave signed by DKIM/SPF *as the user*. A compromised or misdirected agent doesn't forge mail — it sends **authentic** mail: phishing from the user's own address, instructions to contacts, password resets.
- JMAP blob upload = arbitrary file staging on the mail provider; attachments to attacker-controlled addresses = exfil that looks exactly like normal user email to any DLP.
- The inbox is also a **C2 channel**: the agent can receive instructions by mail, and sent-mail/deleted-mail give the operator (or an attacker with mailbox access) a full tasking history.
- Trust chain: the mail provider sees everything (content, correspondents, timing); every recipient trusts the From identity; DKIM makes the forgery cryptographically genuine.

**Ambiguity:** LOW-MEDIUM — sending email is the feature; exfil is indistinguishable from legitimate use without content policy. The risk is architectural, not behavioral.

---

## P8. Bitwarden vault via MCP

**OBSERVED**: bitwarden/mcp-server fetched (lane E) — agent-readable secrets vault.

**Trust placed, in whom (INFERENCE):**
- The vault is decrypted inside the MCP server's process memory, and the agent can read **every item**: logins, secure notes, cards, identities — including **TOTP seeds**, i.e. second-factor material. A vault dump bypasses 2FA everywhere those seeds are used.
- **Credential isolation: none.** The master-password boundary is bypassed by design — a single confused-deputy incident or prompt-injection against the agent exposes the *entire* vault, not one credential. There is no per-item access control in this architecture.
- The MCP server itself becomes trusted computing base with full vault access: its compromise (malicious update, supply-chain attack on the MCP package) = total credential compromise of the user.
- Unlike a webhook URL (one bearer token, one channel), the vault is **all bearer tokens at once**.

**Ambiguity:** LOW — vault access is all-or-nothing by design; the risk is architectural, not a matter of distinguishing good uses from bad.

---

## P9. LocalCan (localhost-tunnel broker)

**OBSERVED**: lane B/E — localhost tunnel service; docs-only, closed binary.

**Trust placed, in whom (INFERENCE):**
- Same shape as P1 (ngrok) with a worse trust story: the tunnel **client is a closed binary from an unaudited operator**, running on the agent's machine with network access. The broker sees connection metadata; the binary's behavior beyond tunneling **cannot be verified** — it could exfiltrate independently and no audit could catch it from the outside.
- Credential-adjacent in the same way as ngrok: whatever local services get exposed inherit the broker's access, with an operator that has no published security posture to evaluate.

**Ambiguity:** LOW-MEDIUM — a closed-binary tunnel client is inherently unauditable; there is little legitimate shape that distinguishes it from a backdoor except the operator's word.

---

## P10. eSIM purchase API, crypto-funded (Roamzy)

**OBSERVED**: lane B — Roamzy; agent buys eSIMs with cryptocurrency.

**Trust placed, in whom (INFERENCE):**
- The agent holds **spendable crypto funds** and a purchase API — it can acquire real-world telecom identity: an eSIM profile (SM-DP+ activation) with a working MSISDN (phone number).
- Uses of an agent-controlled number: SMS verification for **mass account creation**, receiving 2FA codes, voice/SMS-based social engineering with a real caller ID.
- **Provenance chain**: crypto wallet → Roamzy account → eSIM → phone number → verified accounts. Many eSIM vendors are KYC-light, so the chain is *attested* (the carrier vouches the number is real) but *pseudonymous* (the human behind the wallet is obscured) — the ideal identity anchor for sybil operations.
- The vendor and the underlying MNO see purchase + traffic metadata; the number is a durable identifier that can later be correlated across every service it verified.

**Ambiguity:** LOW — buying telecom identity with crypto has few legitimate agent use cases; the identity acquisition *is* the risk.

---

## Cross-primitive notes (INFERENCE)

1. **The bearer-credential pattern dominates.** Webhook URLs (P3), asset URLs (P4), catbox links (P5), tunnel URLs (P1), eSIM activation codes (P10) are all unguessable-but-public bearer capabilities. The study's primitives are overwhelmingly *capability-URL* shaped: security rests on non-disclosure of strings that are routinely logged, committed, screenshotted, and parsed by other tools.
2. **The TLS-termination pattern dominates.** r.jina.ai (P2), ngrok/cloudflared (P1), LocalCan (P9) all interpose a third party that terminates TLS. In each case the agent *loses* the ability to authenticate the far end, and the interposer gains metadata at minimum, plaintext at worst.
3. **Positive pattern found — loki-mode's sentinel architecture** (OBSERVED, `~/workspace/skill-egress-work/lane-c/loki-mode/`): the skill **withholds real GitHub tokens from the agent and plants synthetic sentinels** — `GH_TOKEN`/`GITHUB_TOKEN` env vars are replaced with canaries, `GH_CONFIG_DIR` is scoped to a temp dir, and the worker **fail-closes** ("refuses to start while it can see a real GitHub token"). The sentinels are shape-preserving (`ghp_` + alphanumerics + `INVALID`) so existing redaction regexes still catch them if they leak into artifacts. This is credential-withholding + canary injection + fail-closed design — the correct answer to P8-style all-or-nothing vault access, and worth naming as the defensive pattern other skills should copy.

---

## Secrets triage (OBSERVED — raw bytes from scan-*.json and fetched repos)

Method: extracted every `creds`-category hit from `raw/scan-a.json`, `scan-b.json`, `scan-c.json` and verified against the fetched repo sources on disk (`~/workspace/skill-egress-work/`). No value was used, tested, or transmitted. Display layers (including this model's own tool output) mask contiguous `ghp_` + 20 alphanumerics as `<redacted>`; the file bytes below were read via `od -c` / spaced rendering and are complete.

| # | Skill (lane) | File:line | Observed value (verbatim shape) | Classification | Reasoning |
|---|---|---|---|---|---|
| 1 | loki-mode (C) | `autonomy/run.sh:5646` | `ghp_LOKIWITHHELDsentinel*INVALID` (case pattern; full runtime form `ghp_LOKIWITHHELDsentinel${RANDOM}${RANDOM}INVALID`) | **Sentinel canary — synthetic, invalid** | Literal English words `LOKIWITHHELD` + `sentinel` + terminal `INVALID`; code comments document it as an intentionally-withheld-token marker ("inherited garbage sentinel instead of a real credential") |
| 2 | loki-mode (C) | `loki-ts/src/engine10/worker.ts:18` | `SENTINEL_PREFIX = "ghp_LOKIWITHHELDsentinel"` | **Sentinel canary — synthetic, invalid** | Same marker family; used by `assertWorkerEnv`, which *fail-closes*: "the worker refuses to start while it can see a real GitHub token" |
| 3 | loki-mode (C) | `loki-ts/src/runner/github_token.ts:203` | `` `ghp_LOKIWITHHELDsentinel${process.pid}${randomBytes(8).toString("hex")}INVALID` `` | **Sentinel canary — synthetic, invalid** | Constructed at runtime; pid+hex give uniqueness, `INVALID` suffix marks it; env vars are overwritten with it so a real token never reaches the agent |
| 4 | loki-mode (C) | `loki-ts/tests/engine10/*.test.ts` (several), `autonomy/run.sh:5740`, `docs/enterprise/integration-cookbook.md:50`, `docs/v10/BACKLOG.md` | same `ghp_LOKIWITHHELDsentinel…INVALID` family | **Sentinel canaries — synthetic, invalid** | Test/docs references to the same withholding system (17 canary hits total in this skill) |
| 5 | loki-mode (C) | `deploy/docker-compose/README.md:56` | `xoxb-your-token` | **Placeholder** | Literal `your-token`; documentation example, zero entropy |
| 6 | get-shit-done (C) | `tests/fixtures/adversarial/security/context-malicious-markdown-link.md:7` | `ghp_` + 36× `A` | **Test fixture** | Repeated single character, zero entropy; file is an adversarial-security test fixture (README at `:20` documents fixtures as inline-constructed) |
| 7 | get-shit-done (C) | same fixture dir | `https://user:<redacted>@example.com` (URL-embedded `ghp_…`/`sk-…` placeholders per fixture README) | **Test fixture** | `example.com` reserved domain; fixture tests malicious-markdown credential-exfil handling |
| 8 | videocut-skills (C) | `plugins/chengfeng-videocut/scripts/bug-report.test.cjs:45,118` | `sk-abcdefghijklmnopqrstuvwxyz` | **Test fixture (redaction-test)** | Sequential alphabet, zero entropy; the test *asserts bug-report payloads do NOT match* secret patterns — it is testing the redaction filter itself |
| 9 | wigolo (D) | `tests/unit/cli/json-contracts.test.ts:78` | `ghp_SUPERSECRETtokenABCDEF1234567890` | **Test fixture** | Contains English words `SUPERSECRET` + `token`, zero entropy; unit-test constant |
| 10 | klavis (D) | `mcp_servers/github_official/pkg/http/middleware/pat_scope_test.go:69,80,91,168`, `token_test.go:42,45,50,53,58,61,224` | `ghp_` + 36× `x` | **Test fixtures** | Repeated single character, zero entropy; all in `*_test.go` middleware tests (11 hits) |
| 11 | klavis (D) | `mcp_servers/slack/.env.example:8,12`, `mcp_servers/slack/README.md:39,40` | `xoxb-your-bot-token-here`, `xoxp-your-user-token-here` | **Placeholders** | Literal `your-…-here`; `.env.example` + README documentation |
| 12 | sentry-mcp (E) | `packages/mcp-core/src/telem/sentry.test.ts:10,20,32,69,94,122,154,173,187` (+ `:159` variant) | `sk-abc123def456ghi789jkl012mno345pqr678stu901vwx234` (variant at :159: `sk-xyz123…`) | **Test fixtures** | Sequential `abc123…` alphanumeric walk, zero entropy; test-file constants. NOTE: `scan-c-report.md` renders these as `<redacted>` in its display table — the JSON bytes are complete; the report's rendering is lossy, the evidence is not |

**Triage verdict: zero real-looking credentials across all three lanes.** 17 loki-mode hits are a deliberate credential-withholding sentinel system (defensive, documented in code comments); every other hit is a zero-entropy test fixture (`A…`, `x…`, sequential alphabets, English-word markers) or a `your-token-here` placeholder. No live secret exposure was found in any scanned skill. The one evidence-hygiene flag: `scan-c-report.md`'s display table masks the sentry-mcp fixture values as `<redacted>` while `scan-c.json` retains full bytes — display-layer masking, not evidence loss, but the report should note it (this table does).

**Residual note for the hacker lane:** the loki-mode sentinel system is worth a live look from the other direction — `assertWorkerEnv` fail-closes on *real* tokens, which means the skill's threat model explicitly includes "agent obtains a real GitHub token"; the interesting question is what happens on the *operator* side (dashboard sessions that mint real tokens), not in the scanned code.
