# cyber-mods

Automated harness for weekly and monthly cybersecurity model passes.
Same shape as coding-subs: first-party fetches, snapshots, numbered refs,
rerunnable instruments, delta logs, SVG cards. Relay market excluded.
Self published vendor tables never outrank live boards without a harness note.

## Layout

Each pass lives in `YYYY-MM-DD/` with `README.md`, `data/`, `references/`,
`sources/`, plus `card.svg`, `card-public.svg`, `card-full.svg`.
Tools live in `tools/`. Reviews live in `docs/reviews.md`.

## Instruments

`tools/fetch-cyber.py [PASS]` fetches all first-party pages into pass sources.
`tools/rank.py [PASS]` is the verdict: Table3 plus BenchLM plus HF cards plus live boards.
`tools/make-card.py [PASS]` builds the pretty SVG card with public default and restricted toggle.
`tools/validate.py [PASS]` gates every pass. CI runs it on push.

## Cadence

Weekly: rerun fetch plus rank plus make-card, commit new dated pass on change.
Monthly: full review pass with bias audit and delta vs prior, same as coding-subs rev 6 and 7.
Evidence classes: VERIFIED first-party page, DOCUMENTED vendor table self graded,
THIRD-PARTY aggregator, CITED-BY-VENDOR number inside another vendor table,
UNKNOWN never guessed. Corrections are logged in references, never hidden.

## Passes

| Date | Report | Scope |
|---|---|---|
| 2026-09-22 | [2026-09-22/README.md](2026-09-22/README.md) | Seed pass imported from cyber-pass-2026-09-22: MiMo Table3 plus DeepSeek HF card plus BenchLM plus four live boards, public card default |

## Lobotomized policy

Restricted means not usable as a daily driver: needs special signup such as
OpenAI Trusted Access for Cyber, Anthropic safeguard blocks on newer Claude
rows noted on SEC Bench live board, or default refusal such as GPT-5.5 safety
filters blocking all exploit attempts under default prompting in ExploitGym data.
Anthropic OpenAI and xAI models are hidden on the card by default and ranked
separately. Toggle SHOW RESTRICTED to compare anyway. Open weights public
models rank first for buy advice.
