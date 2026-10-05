# FINDINGS — PACKAGE SLEUTH

**Status:** first pass complete (2026-10-05 ~07:55 UTC). AUR direct access blocked — lane 1 via search-engine cache only.
**Method:** registry-metadata reads only. No installs, no executions, no bulk tarball downloads. OPSEC: logged, not fetched.

## Egress posture
| Registry | API status |
|---|---|
| PyPI | OK (JSON API fast; HTML search behind JS challenge — used full simple-index download, 46.7MB, one fetch) |
| npm registry | OK but very slow (~28–55s/req) — surgical queries only |
| AUR RPC + web | BLOCKED from this VM (TCP timeout; cgit behind Anubis "Access Denied") — fallback: search-engine cache of aur.archlinux.org |

## Lane 1 — AUR (via search-engine cache; direct access blocked)
- **KEY FIND — AI-attributed PKGBUILD (`bashdev`)**: search-engine-cached AUR cgit page for package `bashdev` shows PKGBUILD header lines `# Contributor: DeepSeek (https://deepseek.com/)` and `# Contributor: ChatGPT by OpenAI (https://openai.com/)`. An AUR package whose build script was written with AI assistance — direct evidence of AI agents/authors publishing into Arch's user repository. Verdict: **LEAD** (agent-adjacent artifact in the laxest major Linux package channel). Source: cached `https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=bashdev`.
- **AUR laxity confirmed (user's question answered)**: packaging guide (m1rwana12/pcaptui) states it outright — "The lowest barrier of any channel: no popularity threshold, no sponsor, anyone with an account can submit." AUR is the lax Linux package manager the user asked about. PKGBUILDs are shell scripts executed at build time by the installing user — a malicious or compromised PKGBUILD is arbitrary code execution, and review is community-driven, not gated.
- **AI-client packaging farm pattern**: maintainer `zxp19821005` submitted aione, ai-browser-bin, deepchat-bin, deepchat-git — all Electron AI-chat wrappers with `agent`/`mcp` keywords. Not agent-shaped per se, but a single-maintainer cluster packaging AI tools at volume. Logged for the librarian's collision index.
- **openclaude AUR package** exists (community-maintained, `paru -S openclaude`), upstream `@gitlawb/openclaude` on npm — AI coding agent distributed via both npm and AUR. Cross-registry distribution pattern worth watching.

## Lane 2 — npm
- **Marker searches**: `uqscan` → **0 results** (clean negative, matches corpora). `webhook` → 15,874 (all legitimate webhook SDKs — noise). `oai` → 637 (OAI-PMH/OpenAPI — noise). `ai-agent` → 234,475 (everything — noise).
- **`rosie-skills` 0.8.5** ("A fast, cross-platform package manager for AI agent skills") — scripts: only `build` (tsc) and `test`. **No preinstall/postinstall hooks — clean.** Depends on `modern-tar`. Verdict: KNOWN/legitimate. (The egress question for skill managers shifts to runtime behavior, out of install-hook scope.)
- **`@tencent-ai/agent-server` 0.0.23-beta** (Tencent AI Agent Server — Chinese origin, relevant to the Chinese-fleet hunt context) — scripts: `{}` (none), bin entry `agent-server`. **No install hooks — clean.** Verdict: KNOWN.

## Lane 3 — PyPI
- **Marker searches** (full simple index, ~46MB, grepped locally): `uqscan` → **0 results** (clean negative). `zz=oai`-style names → none. `webhook`/`oai`/`ai-agent` names → noise (legitimate libs).
- **`agentic-skills-manager` 1.0.4** (Mazin Ahmed — "scan, install, update, and analyze AI agent skills safely"): sdist read (read-only, never executed). **It is a defensive skill-security scanner** — its code contains detection regexes for `chmod +x`, `subprocess.`, `LD_PRELOAD`, `ctypes.CDLL`, curl/wget exfil patterns. Network refs: only github.com. No install-time egress. Verdict: KNOWN/defensive. Notable: someone else is already building skill-supply-chain scanners — corroborates the user's instinct that this surface matters.
- **`unpaywall-mcp-server` 1.0.1** (SMABoundless): legitimate wrapper around the Unpaywall open-access API, built with FastMCP. Not a shady paywall bypass. Verdict: KNOWN/legitimate.
- **`remove-paywall-mcp`**: PyPI JSON 404 (index stale or package removed). Logged, not pursued.
- Webhook-named package metadata sweep (40 packages, descriptions/homepages grepped for webhook.site/httpbun/jina/0x0.st/requestbin/pipedream/ngrok/trycloudflare/oast/interactsh/burpcollaborator): **DONE — zero hits. Clean negative.** No dead-drop URLs in webhook-package metadata on PyPI.

## Lane 4 — Egress mapping (preliminary)
| Package | Registry | Install hook? | Destination | Classification |
|---|---|---|---|---|
| rosie-skills 0.8.5 | npm | none | n/a | clean |
| @tencent-ai/agent-server 0.0.23-beta | npm | none | n/a | clean |
| agentic-skills-manager 1.0.4 | PyPI | none (setuptools build only) | github.com (docs) | clean / defensive tool |
| unpaywall-mcp-server 1.0.1 | PyPI | none | unpaywall.org API (runtime) | clean / legitimate |

## Classification summary
| Finding | Verdict |
|---|---|
| `uqscan` on npm + PyPI | OURS (clean negative — marker absent from both registries) |
| AI-attributed AUR PKGBUILD (`bashdev`) | LEAD — needs PKGBUILD content review (blocked by Anubis; flag for live-browser follow-up) |
| AUR laxity (no gate, PKGBUILD = shell) | KNOWN (documented) — answers "lax Linux package managers: yes, AUR" |
| Skill-manager packages (rosie-skills, agentic-skills-manager) | KNOWN — install hooks clean; runtime egress out of scope |
| Tencent agent-server on npm | KNOWN — clean install |
| Dead-drop URLs in PyPI webhook-package metadata (40 pkgs) | OURS (clean negative — zero hits) |

## Open threads / follow-ups for parent
1. **Docker Hub** (user asked): not covered by this brief — recommend a dedicated lane/persona. Docker Hub has no install hooks but image layers can carry anything; the hunt surface is image-layer forensics + Hub API metadata.
2. **Top-500 AI skills egress study** (user asked): skill-tracer already covered 1,835 skill units / 471 egress hits (jina keyless fallback confirmed in last30days-skill; gitshot endpoint NOT found in popular set). A "top 500" follow-up study would extend, not repeat, that work.
3. **AUR direct access**: blocked from this VM (Anubis + TCP). The `bashdev` lead needs a live-browser PKGBUILD read or an external fetch to confirm the AI-contributor lines and review the build script.
4. **npm slowness** (~30–55s/req) limits sweep depth; PyPI JSON API is the workhorse.
