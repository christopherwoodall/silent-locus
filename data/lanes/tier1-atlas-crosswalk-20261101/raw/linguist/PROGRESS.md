# LINGUIST — PROGRESS.md

Swarm: tier1-atlas-crosswalk-20261101. Lane: linguist. Operator: BigSexyWarlock69.
Date of work: 2026-11-01. Corpus date: 2026-11-01T114014Z.

## Scope note (count correction)

The brief said 52 Atlas captures plus 1 crosswalk file (53 total).
The disk holds more: 81 files named `atlas_*.bin` plus
`discovery_agents.crosswalk.to_llms.txt`.
This lane skimmed all 81 Atlas files and the crosswalk file.
It deep-read the longest files and the strangest files.
No file was re-fetched from the network. No new network read was needed.
No capture looked truncated in a way that needed a re-read.

## Corpus shape (counts from first-hand bytes)

- 81 Atlas files in total.
- 54 files hold a real board text (an `llms.txt` style guide for agents).
- 19 files hold only an error shell (404, route-not-found, or endpoint error).
- 5 files hold only a thin shell (title only, or a script shell with no board text).
- 2 files are not agent boards at all (one personal homepage, one search-marketplace guide).
- 1 file holds only a maintenance page (night window notice).
- 1 extra file is the crosswalk guide (a shared-account service, not a board).

Total bytes across the 81 Atlas files: about 802 KB.
The largest file is the Moltbot Den guide (about 87 KB).
The next largest are the Continental guide (about 42 KB) and the Switchboard guide (about 30 KB).

## Method

1. Stripped markup from each file and read the first 700 characters of each.
2. Ran word counts across the corpus for key terms (heartbeat, vote, token, ledger, and more).
3. Ran a shared-phrase check (8-word runs shared by 3 or more files).
4. Deep-read the longest files and the strangest files in full or in large part.
5. Graded each finding. OBSERVED means the words are in the capture.
   REPORTED means the text claims a fact about the outside world.
   SECONDARY is the default for all interpretation.

## Output files in this directory

- `notes.md` — ranked findings, discourse summary, nulls, gaps.
- `excerpts.md` — short quotes with file references.
- `PROGRESS.md` — this file.

## Rules kept

- No human names or handles in prose. Agent and bot names appear only when the text declares them.
- No signed values, tokens, wallet addresses, or signal codes are copied here.
- No claim about agent behavior is made from invitation text alone.
- Style follows ASD-STE100: short sentences, simple words, terms defined on first use.
