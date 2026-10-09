# silent-locus

A hunt corpus tracking AI agent incidents found in public systems — cases
where AI agents hid traffic through proxy laundering (routing requests
through third parties so their origin disappears), stashed stolen data at
dead-drops (URLs or inboxes set up to receive exfiltrated data), or acted
outside their intended task.

Each incident lives in one dated directory under `evidence/` with its raw
evidence, a provenance record (where every byte came from), and graded
analysis. Findings we consider solid get filed on the Transluce
agent-incident tracker, which this repo feeds. Scope is agents and
agent infrastructure only — never human or operator identity.

## Layout

```
AGENTS.md              -- the rules: how to work in this repo
evidence/                  -- 82 dated hunt-event dirs, 2016 -> 2026
  evidence/<date>-<slug>/  -- one incident: events.jsonl, PROVENANCE.md,
                          SHA256SUMS, raw/
  evidence/transluce-api/  -- Transluce tracker integration + filing drafts
  evidence/hf-trajectories/-- audits of AI-agent run logs on Hugging Face,
                          incl. the URL farm and TARGET.md
  evidence/aggregates/     -- multi-source rollups
  evidence/raw/            -- primary-source evidence captures
lists/                 -- canonical IOCs: the search-term wordlist
                          (3,800+ terms) + URL inventory (331 URLs)
docs/                  -- onboarding, methodology, glossary, ops runbooks
docs/notes/            -- 162 analyst writeups, one per investigation thread
collections/           -- ongoing collectors and cross-event indexes
scripts/               -- shared tooling
```

## Evidence system: Factum

New structured evidence lives in Factum: sources, observations, graded
claims, and edges (links between records). Full docs:
[skills/factum/SKILL.md](skills/factum/SKILL.md).

Corpus state: 3,400+ records held as immutable batches in `data/`.
Legacy `evidence/` lane directories are moving into Factum with lane
tags and keep their original paths.

## Where to start

- **New here** — read [docs/onboarding.md](docs/onboarding.md), then the
  glossary ([docs/glossary.md](docs/glossary.md)) for our terms.
- **Here to hunt** — read [AGENTS.md](AGENTS.md): evidence rules, schema,
  and the novelty rule (assume a find is already reported until you
  prove otherwise).
- **Here for the evidence** — start in [evidence/](evidence/): every event dir is
  self-contained, with its own provenance record.

## Key numbers

- 82 dated event directories, 2016 -> 2026
- ~365,000 rows of AI-agent run data farmed and audited
  (Hugging Face trajectory audits)
- Transluce findings #170 (jina.ai proxy-laundering) and #171 (webhook
  dead-drop family) filed and live on the tracker
- 162 analyst writeups, 331 tracked URLs, 3,800+ IOC search terms

## Rules of the road

- Never redact observed values. Annotate sensitivity; do not remove it.
- Grade every claim: OBSERVED (seen in the bytes), INFERENCE (reasoned
  from facts), UPSTREAM (another source's claim).
- Keep everything; annotate overlap instead of deleting. Every cached
  byte needs provenance.
- Honest negatives are first-class: record what you looked for and
  did not find.

## Contributing

Branch, never push to main. Docs in short plain sentences. New events
follow `schema/` and ship `PROVENANCE.md` plus `SHA256SUMS`.

## License

MIT — see [LICENSE](LICENSE).
