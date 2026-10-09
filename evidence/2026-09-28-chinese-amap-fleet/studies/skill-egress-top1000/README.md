# Top-1000 AI skills egress study

Scanned the top 1,013 ranked AI skills/repos for outbound-egress primitives
(webhooks, relays, tunnels, image upload, email, DNS, creds-adjacent code)
using the skill-tracer scanner with an unmodified taxonomy. Study date:
2026-10-05.

## Headline counts (combined with the top-500 lane; verified in `EGRESS_MAP.md`)

- **1,013** skill identities enumerated (655 new: lane A-ext 450 + lane B-ext 205)
- **6,343** skill units scanned (2,490 new)
- **1,541** units with egress hits (741 new) — 57,352 new hits total
  (CRITICAL 1,564 · HIGH 17,586 · MEDIUM 38,202)

## Key files

| File | One-line description |
|---|---|
| [INVESTIGATION-REPORT.md](INVESTIGATION-REPORT.md) | **Integrated report (start here):** "The Skill Supply Chain Is the Tradecraft" — folds in the top-1000 scan, the why-these-sites thesis test, the deep link-hunt, and the usemod.org ClipBoard follow-up |
| [EGRESS_MAP.md](EGRESS_MAP.md) | Headline counts + top destinations ranked by confirmed primitive utility (Discord/Slack/Telegram webhook grammar runtime-confirmed; r.jina.ai runtime in 2 skills; uploads.github.com runtime upload code; zread.ai, loca.lt, mailgun as new relay cousins) |
| [SKILLS.md](SKILLS.md) | Ranked skill list for the 655 new identities (lane A-ext GitHub stars tier 2, lane B-ext marketplaces tier 2); first 358 identities live in `../skill-egress-top500/SKILLS.md` |
| [SCAN-LOG.md](SCAN-LOG.md) | Coordinator run log: scanner source, scoring rule (3×CRITICAL + 2×HIGH + 1×MEDIUM), evidence grades (confirmed vs pattern-match) |
| [HYGIENE-AUDIT.md](HYGIENE-AUDIT.md) | Evidence-integrity audit enforcing the standing never-redact rule across 31 markdown files in this tree |
| [why-these-sites/WHY-SITES.md](why-these-sites/WHY-SITES.md) | Thesis test ("the egress destinations are 11 y/o tradecraft — not new"): selection-logic properties, historical mapping, link-hunt; worker files under `why-these-sites/workers/` |
| [why-these-sites/TRADECRAFT-RESURGENCE.md](why-these-sites/TRADECRAFT-RESURGENCE.md) | Historical essay: why dead-drop/exfil tradecraft recurs (no human in the loop, no secrets, simple HTTP) |
| [why-these-sites/linkhunt-deep/LINKHUNT-DEEP.md](why-these-sites/linkhunt-deep/LINKHUNT-DEEP.md) | Deep dive on the WHY-SITES live leads (Pipedream, tokens, tunnels, templates); passive/stored observations only |
| [why-these-sites/CORRECTIONS-LOG.md](why-these-sites/CORRECTIONS-LOG.md) | Additive corrections to upstream writeups (e.g. trycloudflare/DeepSearchQA false-positive removed) |
| [raw/](raw/) | Scan outputs (`scan-d1/d2/d3`, `scan-f1/f2` JSON), enumeration notes, fetch logs, known-URL hunt (`known-url-hunt.md`), novel-domain extraction (`new-urls.md`) |

## What the study found

The corpus tradecraft recurs as **shipped runtime code** in the skill supply
chain, not just documentation: complete Discord/Slack/Telegram dead-drop
grammar in one shipped skill (`whale-alert-monitor`), the keyless jina relay
(`r.jina.ai`) as runtime in two skills, and trusted-host upload code on
`uploads.github.com`. Grading stays dual-use honest — a high score is not an
accusation; evidence is graded confirmed (bytes present) vs pattern-match
(corpus tradecraft grammar), and retractions are additive via the
corrections log.
