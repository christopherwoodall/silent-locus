---
license: cc-by-4.0
pretty_name: Trace Commons — Agent Traces
task_categories:
  - text-generation
language:
  - en
tags:
  - agent
  - agent-traces
  - coding-agent
  - traces
  - tool-use
  - open-data
configs:
  - config_name: default
    data_files: data/*.parquet
---

# Trace Commons — Agent Traces

**Trace Commons** is one open, public dataset of coding-agent sessions — the
back-and-forth between a developer and an AI coding agent, including prompts,
model responses, tool calls, and command output — contributed voluntarily as an
open resource for studying, evaluating, and building on how these agents
actually work.

Every trace here was donated **only from a public, open-source repository**, was
**anonymized on the contributor's own machine before upload**, and was
**reviewed by the contributor** before it was submitted as a pull request.

## What's in it

Every session is preserved as its agent's **raw, unmodified session file** (only
anonymized, never reshaped), organized by which agent (harness) produced it:

```
sessions/claude_code/<file>.jsonl
sessions/codex/<file>.jsonl
sessions/pi/<file>.jsonl
sessions/cursor/<file>.jsonl
sessions/opencode/<file>.json
```

The **dataset table you see in the viewer** is built from these raw files,
decoded one row per session (`harness`, `session_id`, `prompt`, `messages`,
`tools`, `trace`, `metadata`, …) and served as Parquet under `data/` for
reliable loading. The raw `sessions/` files remain the source of truth — download
them directly to work with the original agent-native format.

## How traces are collected

Traces are donated with the **[`donate-trace`](https://github.com/trace-commons-ai/donate-trace)**
skill, installable into a coding agent. The skill:

1. Confirms the session's project is a public, open-source repository — and
   refuses otherwise.
2. Locates the current session from the agent's own local logs.
3. Runs a deterministic scrubber (`scrub.py`) **locally** to strip the
   highest-confidence leaks (see below).
4. Asks the contributor to review what was removed, and shows the cleaned trace.
5. Only after explicit confirmation, opens a **pull request** — either under the
   contributor's own Hugging Face account (attributed) or anonymously through the
   Trace Commons ingestion server, which re-runs the same scrubber as a backstop.

Nothing is pushed directly; a maintainer reviews every pull request before it
becomes part of the dataset.

## Anonymization — and its limits

Anonymization happens in two passes:

- **Deterministic pass (`scrub.py`).** Removes things with crisp signatures:
  home-directory paths and the username inside them, common secret formats (AWS,
  GitHub/GitLab, Slack, Google/GCP, OpenAI/Anthropic, Stripe, Twilio, SendGrid,
  npm/PyPI tokens, Azure storage keys, JWTs, PEM private-key blocks, `KEY=value`
  env-var secrets, bearer tokens, DB connection strings, webhook URLs), and email
  addresses.
- **Scanner backstop (`TruffleHog`).** Because a hand-written pattern list can
  never be complete, the ingestion server additionally runs
  [TruffleHog](https://github.com/trufflesecurity/trufflehog) — hundreds of
  maintained secret detectors — over every donation (the regex pass above is the
  fast, high-confidence hard block; TruffleHog adds breadth). It runs without
  verification, so candidate secrets are never sent to any third party — which
  also means it can false-positive on high-entropy strings, so its findings
  **flag a donation for maintainer review** rather than auto-rejecting it. Every
  donation is reviewed by a maintainer before it is merged regardless.

- **Review pass (human + agent judgment).** Catches what a regex cannot:
  personal names, company or client names, internal hostnames, codenames, ticket
  IDs in free-text prose.

> **Anonymization is best-effort and imperfect.** The deterministic pass only
> catches patterns it knows about; the review pass depends on human judgment and
> can miss things. **Do not assume this data is free of personal information.**
> A name, an internal URL, a company reference, or a novel secret format can slip
> through. Treat these traces as public material that has been carefully but
> imperfectly cleaned — not as guaranteed-anonymous data.

If you find sensitive information in a trace, please use the takedown path below.

## License

The **Trace Commons compilation** — the collection, its structure, and its
metadata — is released under **[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)**.
You may use, share, and build on it (including for training) with attribution to
Trace Commons.

Individual traces may contain source code, file contents, command output, and
other material that carries its own original licensing. Traces are accepted on
the basis of the **contributor's certification**: by donating, a contributor
certifies that the session is not private or confidential and that they have the
right to publish it publicly under this license. That certification — not
maintainer vetting — is what traces rest on; we do not and cannot verify the
provenance or license of everything inside every trace. Maintainers review for
quality and obvious secret/PII leakage, not to re-confirm the contributor's
right to share.

**If you reuse this data, you are responsible for checking that your use complies
with the licenses of any code or content contained in the traces.** Likewise,
contributors are responsible for only donating sessions they have the right to
share — sessions from public, open-source work that contain no employer, client,
or otherwise confidential material — and for complying with the terms of the
coding-agent provider they used (for example Anthropic's or OpenAI's terms). If
something shouldn't be here, use the takedown path below.

## Privacy & personal data

These traces can contain **personal data** — names, email addresses, identifiers,
file paths, or references to people in prompts, commits, and command output.
Anonymization is best-effort: in the sense of the GDPR and
[CNIL guidance](https://www.cnil.fr/en/sheet-ndeg1-identify-personal-data), this
data is **not certified anonymous** and should not be treated as such. It is
published on the basis of the contributor's consent and a legitimate interest in
maintaining an open research commons.

If a trace contains your personal data, you can ask us to remove it — this
includes the **right to erasure** for EU/EEA data subjects under the GDPR. Use
the takedown path below; maintainers act on removal requests promptly.

## Not affiliated

Trace Commons is an independent, community-run project. It is **not affiliated
with, endorsed by, or sponsored by** Anthropic, OpenAI, Cursor, or any other
agent or model vendor. Product names such as "Claude Code", "Codex", "Cursor",
"pi", and "opencode" are trademarks of their respective owners, used here only to
identify which tool produced a session.

## Contact & takedown

To request removal of a trace — whether you contributed it, or you found
information in it that identifies you or your organization — **open a discussion
on the [Community tab](https://huggingface.co/datasets/trace-commons/agent-traces/discussions)**
of this dataset. Maintainers monitor it and will remove flagged content promptly.

## What this dataset is not

- Not intended to hold private, proprietary, or client code — contributors
  certify they are only donating content they have the right to publish. If
  something slipped through, use the takedown path above.
- Not a complete or representative sample of agent usage — it is a voluntary,
  opt-in commons and will be biased toward contributors who choose to donate.
- Not guaranteed to be free of all personal information (see limits above).
