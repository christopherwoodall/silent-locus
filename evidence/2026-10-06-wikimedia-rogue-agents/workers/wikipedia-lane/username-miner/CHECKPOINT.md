# username-miner CHECKPOINT

## Username inventory (OBSERVED, from revisions.tsv, 54 rows incl. header)
Extracted 2026-10-06 ~13:50 CDT. 29 distinct temp accounts, all `~2026-NNNNN-NN` shape.

Heavy:
- `~2026-28355-02` x19 — sandbox lead (May 10 bursts)
- `~2026-31087-50` x4

Operator cluster:
- `~2026-36867-71` x1 — Web2Cit configs (2026-06-26, from hunt summary)

Singletons: `~2026-28217-20`, `~2026-28380-92`, `~2026-28435-23`, `~2026-28986-96`, `~2026-28987-61`, `~2026-29018-32`, `~2026-29065-25`, `~2026-31341-00`, `~2026-31558-62`, `~2026-31565-39`, `~2026-31625-92`, `~2026-31693-52`, `~2026-31711-15`, `~2026-35379-90`, `~2026-35411-85`, `~2026-35737-64`, `~2026-36686-00`, `~2026-36722-50`, `~2026-36724-00`, `~2026-36766-54`, `~2026-36781-18`, `~2026-36803-16`, `~2026-36837-35`, `~2026-36837-69`, `~2026-36920-78`

NOTABLE (INFERENCE, structural): `~2026-36837-69` and `~2026-36837-35` share middle segment `36837` (different suffix) — possible same-origin IP or adjacent assignment. Middle segments cluster in bands: 282xx-290xx (May 10/Jun 25), 310xx-317xx (May 27), 353xx-369xx (Jun 25–26), consistent with WMF's temp-account ID being time-ordered-ish per IP pool (INFERENCE — needs verification).

Numeric segments to probe (hyphenated/bounded): 28355-02, 31087-50, 36867-71, 36837-69, 36837-35, 36920-78, plus bands 28217-20, 28380-92, 28435-23, 28986-96, 28987-61, 29018-32, 29065-25, 31341-00, 31558-62, 31565-39, 31625-92, 31693-52, 31711-15, 35379-90, 35411-85, 35737-64, 36686-00, 36722-50, 36724-00, 36766-54, 36781-18, 36803-16.

## Body 1 (incident publications)
- [ ] Diff seed article text (https://diff.wikimedia.org/2026/10/05/openai-rogue-agent-activities-found-on-wikimedia-projects/) — usernames/mentions
- [ ] security.wikimedia.org writeup (need URL; check workers/ioc-miner FINDINGS + IOCS.md)
- [ ] wikitech incident pages (incidents checked by infra-tracker; re-scan for usernames)
- [ ] Phabricator T425758 / T425989 (public read attempt)
- [ ] number-pattern recurrence: does `36867`, `28355`, `31087` recur in any WMF text?

## Body 2 (our corpora)
- [ ] collections/ (exact usernames + hyphenated segments)
- [ ] data/ (incl. 2026-09-28-chinese-amap-fleet, german-french-swarm-hunt, other data dirs)
- [ ] urlquery notes (local notes corpus)
- [ ] ~/workspace/ai-village-data/ (5GB local)
- [ ] collections/eval-questions/all-questions.jsonl
- [ ] Grammar analysis: `~YYYY-NNNNN-NN` shape vs known families (zz=oai, dsqa_, task-oai-NNN, tok=expt<N>)

## Done
- [x] Username list extracted from revisions.tsv (29 distinct temp accounts)
