# FALSE-POSITIVES — Lane 11: reposcout

This file lists the noise the reposcout scanner will see. A new
candidate-trajectory file is not evidence of agent activity until it
is corroborated: extension proves file FORMAT, not content. A .jsonl
file can hold benchmark prompts, test fixtures, or log dumps. Content
is never fetched by this module.

Terms used here:

- **Candidate-trajectory**: a file whose extension marks it as a
  possible trajectory container (.json, .jsonl, .parquet, ...).
- **Manifest**: the stored file list for one watched repo.
- **Newness**: a file that appears in the new manifest but was not in
  the old one.

## Forks and mirrors

A watched repo can be a fork or a mirror of another repo. New files
can arrive from upstream sync, not from new work. A mirror re-push
can look like a burst of new files. Check the fork network and the
commit history before treating a file as new activity.

## Benchmark datasets that share the format

Trajectory containers (.jsonl, .parquet, .csv) are also the standard
format for benchmarks, eval sets, and prompt collections. A new
parquet file in a watched dataset is often a new benchmark split, not
a new agent trajectory. The scanner cannot tell them apart from the
extension. A MEDIUM grade (path matched a naming pattern) is still
format-level: a file named "trajectories_eval.jsonl" can be an eval
set.

## Truncated-tree false negatives

GitHub caps recursive trees (about 100k entries or 7 MB). Big repos
get a truncated tree. The manifest then misses files. A later full
tree can "discover" old files as new. Truncation is logged as
degraded coverage (report_error), never as clean. Treat new files
that appear right after a truncated run with doubt.

## Force-push and history-rewrite churn

Rebases and force-pushes rewrite history. The diff sees rewritten
files as new files. A repo that rebases often will show churn that
looks like new trajectory drops. Check whether the repo's history
was rewritten before escalating.

## Unclassified files

Files with unknown extensions grade "unclassified". They stay
visible in the manifest; they are never auto-skipped. They are not
hits. Only "candidate-trajectory" files can be hits.

## Triage rule

Keep a hit only if the file is still reachable, the format fits a
trajectory container, and the repo is not a known mirror or fork
sync target. Content review is a separate step with its own
provenance. Every hit grades SECONDARY (manifest metadata, not
observed content) until content is fetched and checked.
