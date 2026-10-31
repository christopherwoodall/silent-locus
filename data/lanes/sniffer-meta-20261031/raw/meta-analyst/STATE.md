# STATE.md — meta-analyst (linguist lane), sniffer-meta-20261031

Date: 2026-10-31. Status: COMPLETE. No commit, no push (coordinator owns).
No Factum writes. Passive reads only. ANEC-01 untouched per brief.

## Work done

1. Re-read in full: reports/sniffer-sweep-20261031/REPORT.md, hits.json,
   adversarial-review.md, verifier-report.md, cryptologist-review.md.
2. Re-derived counts from staged raw (see FINDINGS.md for each value):
   - hn-forum/_summary.json: 36 keys, 20 at 300 cap.
   - hn_oct-hiring_candidates.json: 48 posts, 48 distinct authors;
     verified 3 IDs dated 2026-10-01, 2026-10-06, 2026-10-12, 3 distinct
     authors; date clusters Oct 1 (19), Oct 2 (9).
   - github search files: 11 issue-search files, 74 items; 2 code-search
     files, 10 items; staged total 84 (REPORT.md says 86 / 12 — gap open).
   - q05-collab-spawn.json: dotted 7, flat 1, fused 2, any spawn_agent 9,
     tangential 1 of 10.
   - q06-i-am-ai-agent.json: 10 items split as 3 trap/template, 1
     unchecked attestation template, 1 product description, 1 registration
     form, 1 Village duplicate, 3 re-triage candidates (licence filing,
     backport message, bounty disclosure).
   - q06d village comments: 4 comments, 1 distinct account, all User type;
     issue 2026-10-18T22:50:51Z; comments 22:51:35Z, 22:51:37Z, 23:01:03Z
     (instruction to post externally), 23:13:00Z (publication update).
   - tron files: issue 2026-10-30T15:37:54Z, reply 15:41:36Z (222 s),
     reaction 15:45:39Z (465 s after issue). Both accounts User type.
   - uq-odd-dagd-domain.json: total_hits 98, saved 30; saved dates June 12
     (1), 16 (1), 18 (3), 20 (1), 21 (17), 27 (1), July 1 (1), 5 (1), 13 (3),
     Oct 4 (1); saved June 24, July 5, Oct 1, May 0.
   - committer-accounts: 7 files, 1 complete (Copilot 30 commits, 17
     distinct authors, all User, 30 footers); 6 unparseable; errors 3 x
     rate-limit 403, 2 x bad flag, 1 truncated.
   - linguist/phrase-list.md: 46 = 16 + 19 + 11; searchable 45; mined 37
     (35 in-window + 2 pre-window background); seed 8; category 1.
   - tango-zulu/counts-summary.json: code 135424 / 17 / 83 / 21; issues
     103; PRs 121; HN phrase 0, hyphen-token 6, concatenated-token 9.
3. Factum read-only matches (no lock block; state commit
   e234a7a0162bbec82ce868a6ded9a7fbb9ac238e; 1 pending batch untouched):
   - "handoff received" exact: not_found, 0 matches. Fuzzy: found, 25
     payload (truncated), 0 containing the contiguous phrase.
   - "pursekeeper" exact: not_found, 0 matches. Fuzzy: found, 25 payload
     (truncated), 4 values containing the token, incl. record
     observation_212f920ef16f42cd9280d80ee8f8adb6 (infra.message, lane
     2026-08-19-tantive-space) and observation_da783c30a54049888e9eee4a5fa3f1dc
     (intel.report, lane transluce-intel).
   - "da.gd" exact: found, 25 payload (truncated, cap not total).
     Fuzzy: same 25 exact matches.
4. Transluce snapshot greps (case-insensitive, whole-file occurrences
   plus findings-containing counts):
   - Full list findings-list.json (total 140, identical to
     findings-list-20261030T115757Z.json): ilands 36 occurrences in 1
     finding; pursekeeper 1 in 1; da.gd 5 in 2 (findings 122, 146);
     handoff 0; handoff received 0; village 0; beno 0; tango 0.
   - Slice findings-list_25_183-210_20261031T115745Z.json (25 items,
     offset 0): ilands 36 in 1; pursekeeper 1 in 1; da.gd 0; handoff 0;
     handoff received 0.

## Outputs

- FINDINGS.md (this dir): corrections table (C1–C13), ranked re-triage
  list (R1–R6), cross-lane pattern scores (P1–P8), novelty-gap table
  (N1–N3), what-holds section, open questions.
- No fetched captures were made, so no .PROVENANCE.txt / .sha256
  sidecars were needed for this lane.

## Open items for the coordinator

- Reconcile GitHub "86 / 12" vs staged "84 / 11" (FINDINGS.md C2).
- Stage the HN exact-substring count table or soften the claim (C5).
- Legacy-tree grep still incomplete: all NEW wordings stay provisional.
- Full 98-row da.gd pull + short-code comparison vs da-gd-shortener lane.
- ANEC-01, Reddit live verification, escrow capture decision, committer
  re-run: untouched here, still open from REPORT.md.
