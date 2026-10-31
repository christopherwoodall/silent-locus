# STATE — unmeasured-leftovers lane, continuous hunt 20261031

- Lane dir: `data/lanes/continuous-hunt-20261031/raw/unmeasured/`
- Runner: `run-leftovers.sh` (read-only `gh search`, existing gh auth only,
  no POST, no fresh login; 55 s sleep between search calls, i.e. starts
  paced 55 s plus call duration, longer than the 30 s brief minimum).
- Recovered unmeasured set (23 items, exact, from sniffer-meta committer-rerun
  STATE.md + FINDINGS.md §4 + run-rerun.sh; see FINDINGS.md §1):
  1 codex commit lane, 2 PR lanes (type:pr qualifier fix), 20 phrases.
- Pre-run bucket check 2026-10-31T18:19:17Z: search 30/30 remaining,
  core 4997/5000. Guard last fired 2026-10-31T16:11:32Z (~2 h earlier).
- No commit, no push from this lane. No Factum writes.
- No human poster handles in prose. Bot/agent account names only where
  self-declared or commit authorship. No signed values, tokens, or query
  strings in FINDINGS.md or any report file.

## Progress

- [x] Unmeasured set recovered (23 items, exact).
- [x] Pre-run bucket check done (search 30/30, core 4997/5000).
- [x] Run complete 2026-10-31T18:19:37Z–18:41:51Z: all 23 calls rc=0,
      no rate guard fired. Plus 1 second-pass call (phrase-20 code
      shape), rc=0, 0 rows.
- [x] Analysis done (analyze.py, analyze2.py; aggregate outputs in
      analysis.txt, analysis2.txt). FINDINGS.md written.
- [ ] No commit, no push from this lane (coordinator call).
