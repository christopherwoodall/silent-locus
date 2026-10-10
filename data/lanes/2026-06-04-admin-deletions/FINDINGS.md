# Findings

Grade claims OBSERVED, UPSTREAM, or INFERENCE.

## The deletion sweeps (OBSERVED)

- 5,217 page-deletion events on the dse wiki, 2026-06-04T10:53:40Z →
  2026-07-14T13:56:54Z, across 26 active days.
- Invariants on all 5,217: actor `[Admin1]`, ip16 `2.202`, wiki `dse`,
  change_summary "Seite gelöscht." (page deleted), `time_grade` `reqlog`
  (one event `rclog`).
- 5,144 unique page names deleted; 73 repeat deletions.
- 29 events carry `round_id` values (for example
  `dse~OECDEducationEquitySequence#round-1` … `#round-7`,
  `dse~ZZZEnrollmentAsianFeb21Help#round-1` … `#round-4`): these deletions
  are tied to named multi-round runs.
- One event carries `clock_note` "ambiguous delete requests at -1/+1s".
- Deleted page names follow agent-test grammars (Agent*, Zx*, Zzx*,
  Mass*, Injx* families); the 2026-06-23 rollup lists Zx46, ZZx37,
  AgentBridgex22, Yx21, Agentx18, Injx15 among 602 deletions that day.

## Per-day shape (OBSERVED from rollup, INFERENCE for sessions/families)

- 26 per-day `admin_cleanup_burst` docs. Largest day: 2026-06-23
  (602 deletions, sessions 11:38–12:23Z, 16:05–20:54Z, 22:43–23:47Z).
- The 2026-07-06 rollup (79 deletions) notes an `inter_run_campaign` tail
  ~24h before the 2026-07-07 XSS/SSTI wave (INFERENCE: the 2026-07-06 and
  2026-07-07 deletions read as pre-wave venue clearing).

## Cross-check (OBSERVED)

- ES index `collusion-wiki`: exact per-day match between the JSONL counts
  and `wiki:event:delete:*` doc ids on all 26 active days (4 apparent
  extras on 06-19/06-21 were `revert` events, excluded).

## Open question this lane was built to answer

Lane R followed lane P's open question: do the dse wiki admin's deletion
sweeps recur before other runs? The rollup's `inter_run_campaign` notes
suggest rolling venue clearing with no run within ±7 days on most days —
but that reading is INFERENCE from timing proximity, not established.
