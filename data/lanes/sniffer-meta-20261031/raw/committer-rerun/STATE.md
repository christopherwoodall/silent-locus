# STATE — committer-account re-run lane (sniffer-sweep meta fleet)

- Lane dir: `data/lanes/sniffer-meta-20261031/raw/committer-rerun/`
- Runner script: `run-rerun.sh` (read-only `gh search`, existing gh auth only,
  no POST, no fresh login; 20 s sleep between search calls).
- Pre-run check 2026-10-31: search bucket 30/30 remaining, core 4969/5000.
  The guard still fired on the third call, so the 30/min search quota is
  NOT the binding limit here (see FINDINGS.md, open question 1).

## Run timeline (UTC; CDT = UTC − 5 h)

| # | Call | Start (UTC) | Result |
|---|------|-------------|--------|
| 1 | commits, "Generated with Claude Code" | 16:10:23 | OK, 30 rows |
| 2 | commits, "Co-Authored-By: Devin" | 16:10:56 | OK, 30 rows |
| 3 | commits, "Co-Authored-By: Codex" | 16:11:26 | HTTP 403 secondary rate limit at 16:11:32 — RATE GUARD FIRED, run stopped |
| 4–5 | PR lanes (fixed flag) | — | NOT ATTEMPTED (guard fired first) |
| 6–25 | 20 unswept phrases, issue search, page 1 | — | NOT ATTEMPTED (guard fired first) |

- Stopping point (exact): call 3 of 25, label `commits-codex`,
  2026-10-31T16:11:32Z (11:11:32 CDT). Recorded in `STOPPED.txt`.
- No retry was attempted after the guard fired, per orders.
- Successful captures carry `.PROVENANCE.txt` + `.sha256` each.
  The failed Codex capture (0 bytes) carries a provenance note and the
  error file carries `.sha256`; the guard return path skipped the script's
  normal provenance step, backfilled by hand from the run log.

## What is done

- [x] Claude-code-footer commit lane re-run (30/30 rows).
- [x] Devin commit lane re-run (30/30 rows).
- [x] Bot-type author counts with denominators for both completed lanes.
- [x] Failure point recorded; partial FINDINGS.md written.

## What is NOT done (needs a later window, coordinator call)

- [ ] Codex commit lane (0 rows; 403 on both the original run and this re-run).
- [ ] PR lane, "Generated with Claude Code", fixed flag
      (`type:pr` qualifier + `--include-prs`; original `--type pr` is invalid).
- [ ] PR lane, "agent harness".
- [ ] Phrase pass, 0 of 20 phrases searched (list in FINDINGS.md §4).
- [ ] No commit, no push from this lane (coordinator commits).
