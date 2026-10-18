# SWE-smith trajectories: the patch column points at other people's code

## Summary

The `patch` column in SWE-bench/SWE-smith-trajectories is systematically misaligned with the trajectories it annotates. 1,843 of 3,228 ticks rows (57.1%; 74% of non-empty patches) list source files from foreign packages — deepdiff files on a conan trajectory, tweepy files on a pandas trajectory, conans installer code on a textdistance trajectory. The same misalignment appears in the tool and xml scaffolds. This is a dataset defect, not agent behavior. It already caused one false filing, killed in review.

## Corpus and counting unit

SWE-bench/SWE-smith-trajectories, revision `08e109b4a59eaeebf80e4675cd125d42e7ac99a4`, retrieved 2026-10-17. n = 9,501 trajectories reviewed. Counting unit: ticks scaffold rows (n = 3,228), with spot-row confirmation in tool and xml. Each row counted once. n = 1 finding (B-006), filed as a dataset integrity defect. The verifier caveated the count methodology but confirmed the mechanism on the cited row plus 4 spot rows.

## What happened

The `patch` column is supposed to carry the agent's diff for that trajectory. In the cited row, the trajectory is a conan-io/conan instance whose agent edited only `conan/tools/meson/toolchain.py` (messages 56/58) plus scratch scripts. The `patch` column for that row opens with `diff --git a/deepdiff/deephash.py` and lists deepdiff/diff.py, deepdiff/helper.py, tests/test_diff_datetime.py, tests/test_diff_other.py, tests/test_diff_text.py, tests/test_hash.py. Zero overlap. The agent never mentions deepdiff, test_diff_*, or test_hash in any message. The patch belongs to a different trajectory — a deepdiff instance — and was attached to this row.

The pattern is systematic, not a one-off: 1,843 of 3,228 ticks rows carry foreign-package files in their patches. Spot checks found tweepy/models.py on a pandas instance, conans/client/installer.py on a textdistance instance, pdfplumber on a PySnooper instance. Tool and xml scaffolds show the same misalignment on spot rows.

The damage is already done once: a reviewer candidate tried to file agent test-file tampering based on a misaligned patch (the conan agent "touching" test files it never touched). The adversarial pass killed it (B-K-015) because the messages contradict the patch.

## Evidence

- B-006 — `conan-io__conan.86f29e13.pr_13346.40o1rcbf`, patch-field, ticks, claude-3-7-sonnet-20250219, unresolved, HIGH. "traj conan-io__conan.86f29e13.pr_13346.40o1rcbf patch file list: deepdiff/deephash.py, deepdiff/diff.py, deepdiff/helper.py, tests/test_diff_datetime.py, tests/test_diff_other.py, tests/test_diff_text.py, tests/test_hash.py -- zero overlap with the agent's actual edits in messages (str_replace_editor str_replace /testbed/conan/tools/meson/toolchain.py at msgs 56/58; scratch scripts at msgs 34/42/50/60/64/68). The agent never mentions deepdiff, test_diff_*, or test_hash in any message." Byte pointer: `raw/ticks-00003.jsonl`.

## Novelty

Dataset integrity defects in public trajectory corpora are under-reported relative to their impact. This is a first documentation of the SWE-smith patch misalignment, with a mechanism (row-level patch attachment is shuffled or misjoined), a rate (57.1% of ticks rows), and a demonstrated downstream harm (one false behavioral filing). If no prior documentation exists after a literature check, this stands as the first report; the check performed was the review fleet's own scan, not a literature survey, and that limit is stated.

## Why it matters

These trajectories train SWE-agent-LM-32B. If the training pipeline joins patches to trajectories — e.g. to learn "what a good patch looks like for this issue" — 57% of the ticks examples teach the wrong mapping: the model learns to associate a conan issue with a deepdiff patch. Even for pure behavioral analysis, any finding sourced from the `patch` column alone is untrustworthy. The column must be treated as untrusted input until the join is fixed or the affected rows are quarantined.

## Uncertainties

- The count methodology is caveated (verifier note): the 57.1% figure comes from file-package mismatch heuristics, not a full rejoin. The mechanism is confirmed on 5 rows; the exact corpus-wide rate needs a full audit.
- We cannot rule out that the misalignment is confined to certain task families or rollout batches rather than uniform. The spot rows span pandas, conan, textdistance, and PySnooper, which argues against a single-family cause.
- Whether the misalignment also affects the full 76,002-row corpus (all 8 shards) at the same rate is untested — only shard 00003 was counted.

## Impact

No agent harm — this is a data defect. The realized harm is one wasted reviewer cycle (filed, then killed). The prospective harm is to training: a 57% wrong patch-to-trajectory join in a corpus built to train a coding model. Recommendation: quarantine the `patch` column for training use until re-joined; keep it for nothing except integrity studies.
