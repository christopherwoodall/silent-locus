# Shared IOC search wordlist — swarm hunts

One search-term list for every swarm/agent-infrastructure hunt, built from
everything learned across all lanes (urlquery hunt, RubyGems campaign,
collusion.wiki, Transluce us-canada-gov grading, DeepSearchQA pull,
fake-org lane, re-hunt pattern matrix + QA fingerprints, relay/infra
scours, XSS/SSTI census). Ordered by BigSexyWarlock69 2026-10-03:
expand beyond `zz`/`oai` — now that we have the evals and questions,
word parts from those go in too.

## Files

- `wordlist.txt` — one search term per line, grouped under `#` section
  comments by category. Plain `grep -F` friendly. Contains only
  `status: active` terms; noisy / false-positive / honest-zero terms live
  in `wordlist.json` only.
- `wordlist.json` — array of
  `{"term", "category", "provenance", "added_utc", "status", "note"}`.
  `status` is `active`, `honest-zero` (swept, zero hits — still a valid
  watch term), or `noisy` (known FP class — search with context).
  `provenance` names the exact source note/file/lane. Every term has one;
  no invented terms.
- `README.md` — this file.

## Categories

| category | what |
|---|---|
| `launcher_toolkit` | shared provider toolkit: zz grammar, oai tags, epoch, go-import canaries, beacon strings, key prefixes, eval-infra hosts |
| `evals` | eval/benchmark identifiers: deepsearchqa, dsqa_250, browsecomp, exploitgym, cybergym, harness markers |
| `question_terms` | distinctive word parts from the 900 DeepSearchQA questions (named entities, dataset names, verbatim phrases); stopwords and proven-noise unigrams (`sec` ⊂ `second`) excluded |
| `sqli_payloads` | observed injection strings + param names with all attested case variants (`surveyYearKey` vs `Survey_Year_Key` occur independently in the wild — keep every variant) |
| `relays` | fetch-relay / archive / proxy / scanner domain fragments agents could route through |
| `dead_drops` | dead-drop and exfil surfaces: webhook.site, oast.online, ntfy topics, airtable shares, paste sites, IOC-row values |
| `targets` | **watchlist, not IOCs** — government/data domains and paths under observation |
| `xss_ssti` | observed XSS/SSTI payload shapes from the census |

## Usage

```bash
# fixed-string sweep of a corpus file
grep -F -f wordlist.txt corpus.jsonl > hits.txt

# case-insensitive variant
grep -F -i -f wordlist.txt corpus.jsonl > hits.txt

# per-category sweep
awk '/^# SQLI_PAYLOADS/{f=1} /^# [A-Z_]+/{if($0!="# SQLI_PAYLOADS")f=0} f' wordlist.txt \
  | grep -v '^#' | grep -F -f - corpus.jsonl
```

For the full metadata (provenance, status, FP notes), parse `wordlist.json`.
Terms with `status: honest-zero` were swept with zero hits — they are watch
terms, not dead ones. Terms with `status: noisy` need surrounding context
before being graded a hit (see `note`).

## Update policy

- **Append-only.** Never delete a term. If a term is retired, set its
  `status` and explain in `note` — the history is the point.
- New terms need a `provenance` naming the exact source (note file, lane,
  commit). No invented terms: observed, or derived by a stated rule from
  an observed term.
- Case variants are separate entries when the variant is itself a distinct
  search string (the re-hunt proved case variants occur independently).
- Rebuild: `python3 /tmp/build_wordlist.py` (script kept out of the repo
  deliberately — sources move; the built files are the artifact).
- Commit on the `local` branch with reconciled counts in the message.
  Never push without BigSexyWarlock69's word.
