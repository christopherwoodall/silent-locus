# Linguist phrase list — sniffer sweep 20261031

Provenance note (inside the analysis, per brief): built 2026-10-31, retrieval
15:20 UTC onward. Methods, all passive GET / public search only, no login,
no POST, no sessions: Hacker News Algolia API
(`https://hn.algolia.com/api/v1/search`), public web search snippets, and
prior hunt knowledge for seed rows. No Shodan, no package repos, no Docker
Hub, no credentialed urlquery path (see Open questions). No human poster
handles are recorded. No signed values, tokens, or query strings are included.

Grades: default SECONDARY for every row below. OBSERVED = first-hand bytes of
an act; REPORTED = second-hand report; DISCUSSED = talk/planning, no executed
act (never present as behaviour). No row below is claimed as OBSERVED
first-hand agent behaviour unless its grade line says so. Most mined rows are
REPORTED or DISCUSSED: they are search strings for the sweep lanes, not
proof that an agent acted. Window for new instances: November 2025 onward.
Rows dated just before that window are marked "pre-window background" and
must not be counted as new-window evidence.

How to use: a hit on one phrase alone is a lead, not a verdict. Require
co-occurrence (self-disclosure + tool artifact, or signature + framework
footprint) before escalation. Generic single words are in the Rejected list,
not in the sweep list.

## Bucket A — Agent-vocab markers (self-disclosure / delegation language)

| # | Phrase | Why it signals agent activity | Example / status |
|---|---|---|---|
| A1 | I am an AI agent | Direct self-disclosure as an agent, not a person. Strongest single self-ID string in this set. | Mined, REPORTED/DISCUSSED: https://news.ycombinator.com/item?id=49238453 (Ask HN hiring thread, August 2026, in window) |
| A2 | I am an AI agent, not a person | Stronger variant of A1; explicit person/agent distinction. | Mined, same instance as A1: https://news.ycombinator.com/item?id=49238453 |
| A3 | on behalf of the user | Delegation signature: an agent acting under a user's authority, often in a sign-off. | Mined, REPORTED: https://www.mail-archive.com/qemu-devel@nongnu.org/msg1188091.html ("ECA Issue Agent on behalf of the user" in an agent-skill patch) |
| A4 | ECA Issue Agent on behalf of the user | Distinctive agent sign-off string; low collision outside agent-skill text. | Mined, REPORTED: https://www.mail-archive.com/qemu-devel@nongnu.org/msg1188091.html |
| A5 | acting on behalf of | Delegation language in machine-identity discussion; useful only with an agent noun nearby. | Mined, DISCUSSED: https://bitsofcyber.substack.com/p/the-case-against-machine-identity |
| A6 | You are Manus, an AI agent | Leaked / summarised system-prompt persona line for a named agent. Persona assignment is a harness fingerprint. | Mined, REPORTED (second-hand research summary, not a primary transcript): https://gist.github.com/renschni/4fbc70b31bad8dd57f3370239dccd58f |
| A7 | OpenClaw agent | Named open-source autonomous-agent framework; self-identification as that agent in a contribution context. | Mined, REPORTED: https://lwn.net/Articles/1058643/ (February 2026 contribution dispute, in window) |
| A8 | operate autonomously on behalf of a human | Framework description of autonomous delegation; matches A3/A5 family, in an agent-framework context. | Mined, REPORTED: https://lwn.net/Articles/1058643/ |
| A9 | Copilot coding agent | Named vendor coding agent; delegation marker in PR workflows. | Pre-window background (2025-10-28, just before window), DISCUSSED as product capability: https://github.blog/changelog/2025-10-28-ask-copilot-coding-agent-to-make-changes-in-any-pull-request-with-copilot/ |
| A10 | asynchronous, autonomous background agent | Vendor description of a coding agent working in the background and requesting review. | Pre-window background, same source as A9: https://github.blog/changelog/2025-10-28-ask-copilot-coding-agent-to-make-changes-in-any-pull-request-with-copilot/ |
| A11 | I am Claude | Seed: direct model self-ID. High value if found outside a chat UI (boards, PRs, issues). | Seed phrase, no instance yet |
| A12 | I am GPT | Seed: direct model self-ID, same use as A11. | Seed phrase, no instance yet |
| A13 | I am Codex | Seed: direct model/agent self-ID, same use as A11. | Seed phrase, no instance yet |
| A14 | I am Gemini | Seed: direct model self-ID, same use as A11. | Seed phrase, no instance yet |
| A15 | as an AI agent | Common self-disclosure framing. Weaker than A1 alone; require a nearby act or tool artifact. | Mined, REPORTED/DISCUSSED, late HN batch: https://news.ycombinator.com/item?id=49825130 (a product bot to post explicitly as an AI agent going forward) |
| A16 | post explicitly as an AI agent | Distinctive disclosure-commitment phrasing: a bot account announcing it will label itself as an agent. Low collision. | Mined, REPORTED/DISCUSSED, same late HN instance as A15: https://news.ycombinator.com/item?id=49825130 |

Bucket A count: 16 (12 mined/background, 4 seed).

## Bucket B — Harness / tool-call artifacts

| # | Phrase | Why it signals agent activity | Example / status |
|---|---|---|---|
| B1 | function_call | Core tool-call envelope token in Responses-style APIs. Rare in ordinary prose. | Mined, REPORTED: https://github.com/yetone/magpie/issues/130 (September 2026, in window) |
| B2 | {"type":"function_call","name":"spawn_agent","namespace":"collaboration"} | Exact namespaced function-call shape for a multi-agent tool. Very low collision. | Mined, REPORTED: https://github.com/yetone/magpie/issues/130 |
| B3 | {"type":"namespace","name":"collaboration","tools":[...]} | Namespace-tool definition shape; the wrapper that carries multi-agent tools. | Mined, REPORTED: https://github.com/yetone/magpie/issues/130 |
| B4 | spawn_agent | Multi-agent dispatch tool name. | Mined, REPORTED: https://github.com/yetone/magpie/issues/130 |
| B5 | wait_agent | Companion multi-agent tool name; pair with B4. | Mined, REPORTED: https://github.com/yetone/magpie/issues/130 |
| B6 | send_message | Companion multi-agent tool name; pair with B4/B5. | Mined, REPORTED: https://github.com/yetone/magpie/issues/130 |
| B7 | tool_call.arguments | Tool-call argument field in agent-framework code and error text. | Mined, REPORTED (mirror copy of a framework PR, not canonical host): http://github.heygears.com/microsoft/autogen/pull/7128 |
| B8 | every step must be a tool call (function call), not a direct natural language reply | System-prompt rule forcing tool use over plain replies; a harness instruction fingerprint. | Mined, REPORTED (second-hand summary of a system prompt): https://gist.github.com/renschni/4fbc70b31bad8dd57f3370239dccd58f |
| B9 | system_capability | Prompt-section tag from a structured agent system prompt. | Mined, REPORTED: https://gist.github.com/renschni/4fbc70b31bad8dd57f3370239dccd58f |
| B10 | browser_rules | Prompt-section tag, same family as B9. | Mined, REPORTED: https://gist.github.com/renschni/4fbc70b31bad8dd57f3370239dccd58f |
| B11 | coding_rules | Prompt-section tag, same family as B9. | Mined, REPORTED: https://gist.github.com/renschni/4fbc70b31bad8dd57f3370239dccd58f |
| B12 | MCP server | Model Context Protocol server: the standard way a harness gives an agent tools. Require a tool/server name nearby; "MCP" alone is weaker. | Mined, DISCUSSED (explainer, not an act): https://dev.to/wolfhound1995/mcp-servers-explained-how-to-give-an-ai-agent-tools-without-handing-over-your-keys-1f18 ; also HN, REPORTED/DISCUSSED: https://news.ycombinator.com/item?id=50311588 and https://news.ycombinator.com/item?id=50309586 |
| B13 | claude mcp add | CLI footprint for registering an MCP server with a Claude harness. | Mined, DISCUSSED: https://dev.to/wolfhound1995/mcp-servers-explained-how-to-give-an-ai-agent-tools-without-handing-over-your-keys-1f18 |
| B14 | custom_tool_call | Hosted-tool call envelope token that survives in gateway/transcript text. | Mined, REPORTED: https://github.com/magpie-community/plugins/issues/112 (October 2026, in window) |
| B15 | server_side_tool_usage_details | Hosted-tool usage field; appears in API/transcript dumps when a server-side tool ran. | Mined, REPORTED: https://github.com/magpie-community/plugins/issues/112 |
| B16 | BOOTSTRAP.md | Agent bootstrap definition file for an autonomous-agent framework. High false-positive risk alone (see Rejected note); require agent context. | Mined, REPORTED: https://lwn.net/Articles/1058643/ |
| B17 | ignore previous instructions | Generic test/joke pattern for steering a model. Instances in the late HN batch are jokes and tests, DISCUSSED only — never an executed act. No payload command is included with this row; sweep for the generic pattern only. | Mined, DISCUSSED, late HN batch: https://news.ycombinator.com/item?id=50313616 , https://news.ycombinator.com/item?id=50271285 , https://news.ycombinator.com/item?id=50264584 |
| B18 | approval-bypass phrasing | Category only: language asking an agent to skip approval, review, or a guardrail. Use only as a review category, not as a search string, until a trusted list is supplied. | Category only, no instance cited |
| B19 | Claude Code | Named coding harness. Harness-name footprint in transcripts, issues, and tooling discussion; require tool/agent context nearby. | Mined, REPORTED/DISCUSSED, late HN batch: https://news.ycombinator.com/item?id=50316938 and https://news.ycombinator.com/item?id=50316815 |

Bucket B count: 19 rows, of which 18 are searchable mined phrases, 1 is a category row (B18) that must not be used as a literal search string.

## Bucket C — Freshly mined odd phrases / tokens

These are distinctive tokens that cluster around agent transcripts, logs, and
framework text. They are not proof of an act on their own; they are
high-precision sweep strings.

| # | Phrase | Why it signals agent activity | Example / status |
|---|---|---|---|
| C1 | collaboration__spawn_agent | Flat name for a namespaced tool (namespace + double underscore + tool). A gateway naming fingerprint. | Mined, REPORTED: https://github.com/yetone/magpie/issues/130 |
| C2 | x_search_calls | Hosted-tool usage counter field; appears in transcript/API dumps for a search tool. | Mined, REPORTED: https://github.com/magpie-community/plugins/issues/112 |
| C3 | ThinkingBlock | Transcript block type for model reasoning in an agent SDK log. | Mined, REPORTED (framework documentation): https://deepwiki.com/babelcloud/real_bench/4.2-gboxclaudeagent:-mcp-integrated-agent |
| C4 | ToolUseBlock | Transcript block type for a tool invocation. Pair with C3/C5. | Mined, REPORTED: https://deepwiki.com/babelcloud/real_bench/4.2-gboxclaudeagent:-mcp-integrated-agent |
| C5 | ToolResultBlock | Transcript block type for a tool result. Pair with C3/C4. | Mined, REPORTED: https://deepwiki.com/babelcloud/real_bench/4.2-gboxclaudeagent:-mcp-integrated-agent |
| C6 | gbox-linux | MCP server identifier in an agent configuration example. Distinctive server-name token. | Mined, REPORTED: https://deepwiki.com/babelcloud/real_bench/4.2-gboxclaudeagent:-mcp-integrated-agent |
| C7 | send_msg_to_user | Agent action name for the final user-facing message in a framework transcript. | Mined, REPORTED: https://deepwiki.com/babelcloud/real_bench/4.2-gboxclaudeagent:-mcp-integrated-agent |
| C8 | zz-grammar (zz-prefixed parameter/tag tokens) | Prior hunt marker: zz-prefixed grammar linked to one provider's launcher/toolkit. Sweep string only; this run mined no new-window instance of it. | Seed phrase, no instance yet (prior hunt knowledge) |
| C9 | oai-prefixed tags | Prior hunt marker: oai-prefixed tag family linked to the same provider toolkit. Sweep string only; no new-window instance mined in this run. | Seed phrase, no instance yet (prior hunt knowledge) |
| C10 | epoch-nonce tokens | Prior hunt marker: epoch-style nonce tokens in tags/parameters. Sweep string only; no new-window instance mined in this run. | Seed phrase, no instance yet (prior hunt knowledge) |
| C11 | da.gd shortener tradecraft | Prior hunt marker: shortener tradecraft attributed to a different provider's agents, not the oai/zz family. Do not conflate the two families. Sweep string only; no new-window instance mined in this run. | Seed phrase, no instance yet (prior hunt knowledge) |

Bucket C count: 11 (7 mined, 4 seed).

## Totals

- Bucket A: 16 (12 mined/background, 4 seed)
- Bucket B: 19 rows (18 searchable mined, 1 category)
- Bucket C: 11 (7 mined, 4 seed)
- Total rows: 46; total searchable phrases: 45 (16 + 18 + 11)
- Mined with a cited URL: 12 in A (including 2 pre-window background) + 18 in B + 7 in C = 37 rows
- Seed, no instance yet: 4 in A + 4 in C = 8 rows
- Category only: 1 in B

## Considered and rejected

- "agent" alone, "tool" alone, "AI" alone, "GPT" alone: too generic; would flood the sweep with non-agent hits.
- "SOUL.md" alone: collides with this workspace's own agent-persona file name and with ordinary project files; use only with agent-framework co-occurrence, so it is not a standalone sweep string here.
- Any card number, credential, API key, or signed token seen in web results: excluded entirely, never copied into this file.
- Verbatim prompt-injection payloads with commands from a web source that failed a safety check in this run: withheld. Only the generic pattern in B17, independently attested in HN joke/test comments, is listed, with no payload command attached. The sweep lanes must not reconstruct payloads from this file.
- HN noise from the late batch, rejected as instances: "I am Claude" hits were ordinary tool-use talk, not self-ID; "tool call" / "function call" / "thinking block" hits were old (2015 and earlier) and unrelated; "on behalf of" HN hits were 2015 and out of window. None of those HN hits was promoted to a mined row.
- Human poster handles and maintainer names from source pages: excluded per the no-human-identity rule, even where a source named them. Only self-declared agent/bot account concepts are described, without handles.
- GitHub code-search mining: not done — the code-search API requires authentication, and this lane works unauthenticated/passive only. Issue pages found via public search were used instead.

## Failures / open questions for the coordinator

1. Update 2026-10-31 (late HN batch): the background HN batch did arrive after the first version of this file. It promoted A15/A16, B12 (second instance), B17 (generic pattern only), and B19, and its noise hits were rejected above. No other counts changed.
2. urlquery public search was not used: the available connector path is credentialed, and this lane stayed on unauthenticated public sources. The coordinator may run a separate urlquery lane.
3. Prompt-injection payloads: only the generic B17 pattern is listed, from HN joke/test comments, with no payload command. Question for parent, still open: supply a trusted canonical payload list, or keep the sweep to the generic pattern only?
4. Two A-rows (A9, A10) are pre-window background (2025-10-28). They are usable as sweep strings but must not be reported as new-window evidence.
5. No row in this file is OBSERVED first-hand agent behaviour. If a sweep lane finds a hit, that lane must grade the hit itself (OBSERVED vs REPORTED vs DISCUSSED) from its own bytes; do not carry this file's SECONDARY default forward as a verdict.
6. File location only: this phrase list was written to the linguist lane directory only. No commit was made, per brief; the coordinator commits.
