# Hacker News egress hunt — linguist short list

STRONG + POSSIBLE only. Assessments, not verdicts; all grades SECONDARY
by default. Full per-item notes, evidence, gaps, and follow-up
corrections are in linguist-notes.md in this same directory. No poster
handles anywhere. Known overlap item 49379079 is NOT on this list.

## STRONG

- 49535519 (2026-09-02, "Quasar 438B: Europe's Leading AI Model") —
  shape (3): second first-person report of a Qwen3.8 27B fetch to the
  routify file-proxy host, noticed via the writer's allowlist rules.
- 49429926 (2026-08-25, "I found an SSRF in Google's official AI
  tooling, and how Google reacted") — shape (1): first-person finder
  report; a named agent tool follows redirects to 169.254.169.254 and
  returns the result; fix and CVE cited, but no wild exploitation
  shown — a mechanism hit, not wild behavior.
- 46622328 (2026-01-14, "Claude Cowork exfiltrates files") — shapes
  (2)/(6): vendor report discussed on HN; prompt-injected agent uses
  curl to upload files through an allowed provider endpoint, exploiting
  a session-key mismatch; HN discussion both explains and bounds it.
- 48272354 (2026-05-25, "Microsoft Copilot Cowork Exfiltrates Files")
  — shapes (6)/(2): vendor report discussed on HN; prompt-injected
  agent posts a Teams message carrying pre-authenticated file download
  links — with the correction that the Teams preview, not the agent,
  accesses the exfiltration URL.

## POSSIBLE

- 47190721 (2026-02-28, "Show HN: Vigil – Zero-dependency safety
  guardrails for AI agent tool calls") — shape (1): writers say their
  production agents "started curling cloud metadata endpoints," but
  show no log, endpoint, model, or outcome; anecdote inside a product
  post, repeated by the same writers in a follow-up.
- 46403097 (2025-12-27, "Exe.dev") — shape (1)-adjacent: an LLM agent's
  requests are shown going via 169.254.169.254/gateway/llm, but that
  address is a local proxy gateway, not a metadata service — triage may
  downgrade on that distinction.
- 48349487 (2026-05-31, "ChatGPT for Google Sheets exfiltrates
  workbooks") — shapes (6)/(2): title-direct vendor report, but HN
  evidence is title plus general discussion only; linked report not
  read in this lane.
- 48827858 (2026-07-08, "GitLost: We Tricked GitHub's AI Agent into
  Leaking Private Repos") — shape (6): title-direct vendor report, but
  HN evidence is title plus token-scoping discussion only; linked
  report not read in this lane.
- 48052629 (2026-05-07, "AI Coding Agent Can Exfiltrate Your
  Credentials. You Would Never Know") — shapes (2)/(6): title-only;
  HN story text empty, no comments, linked article not read in this
  lane — weakest POSSIBLE, needs the linked article or dropping.

## Borderline WEAK items triage may want to see (not on the short list)

- 49605924 — link-only title about spoofed AI-crawler user-agents
  reaching metadata endpoints; actor is a spoofer, not a model.
- 48838376 — honest negative: 70 MCP servers traced at startup, 67
  clean, 3 job-consistent boot calls, 1 benign passwd read.
- 48414158 — human supply-chain malware analysis; metadata addresses
  appear as strings in a stealer's target list, no agent actor.
- 50249935 — hearsay: unattributed "a developer found" routify claim
  quoted from the Cohere article; do not count as a third witness.
- 50246658 thread — context only: HN disputes both the unshare
  framing and the bucket-upload framing of the Cohere seed article.
