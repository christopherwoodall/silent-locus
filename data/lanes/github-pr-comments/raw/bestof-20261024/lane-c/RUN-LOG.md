# Lane C run log — bestof-20261024 (null result, honest)

Operator: BigSexyWarlock69. Method: unauthenticated GitHub API, curl only.
Header: Accept: application/vnd.github+json, UA silent-locus-prcomment-bestof/1.0.
Budget used: 4 searches + 4 comment fetches (+1 free /rate_limit check) = 9 calls.
No 403/429 hit. Last X-RateLimit-Remaining seen: 55 (core, on final fetch);
search bucket showed 9 after each search call.

## Searches (all type:pr, per_page=10)

1. `"my system prompt" OR "my instructions tell me" OR "my system instructions"`
   — 3076 total. Top hits were ABOUT system prompts as a topic (prompt-hardening
   PRs, prompt editors), not leakage of an agent's own prompt.
2. `"wrong repo" OR "wrong repository" OR "wrong issue" OR "worked on the wrong"`
   — 1184942 total (OR terms are noisy). Top hits were human mistake/revert PRs.
3. `"self-review" OR "reviewing my own" OR "my own PR" OR "approve my own"`
   — 2971788 total. Top hits were human self-review labels and a review-agent demo.
4. `"rewrote the entire" OR "complete rewrite" OR "rewrote everything" OR "rewritten from scratch"`
   — 230045 total. Top hits were announced rewrites, mostly human-authored.

## Comment fetches (1 call each, issues comments endpoint)

1. can1357/oh-my-pi#13954 ("Session ID available to the agent") — 1 comment:
   chatgpt-codex-connector[bot], Bot, NONE: Codex usage-limits notice for code
   reviews. NOT a lane behavior. Not captured as a candidate.
2. Sairajiv-13/pr-review-agent#1 ("demo: first self review") — 0 comments.
3. markcosker2-dev/orova-nova#199 ("fix: four defects found reviewing my own work") — 0 comments.
4. mel-project/mellis#48 ("Rewrote The Entire CI") — 1 comment:
   github-actions[bot], Bot, NONE: draft release URL notice. NOT a lane behavior.

## Candidates returned: 0

Reason: the search/issues API matches PR titles/bodies, NOT comment text, so
lane behaviors that live in comments (self-praise, prompt quotes, fix-loop
apologies) do not surface through these queries, and the fetched threads were
empty or bot notices. No comment JSON was captured because no candidate
comment exists to capture; inventing candidates from PR titles alone would
violate the no-invention rule. The kill-list lesson (fixture-quoted text
misread as live behavior) was respected: nothing quoted, fenced, or
joke-framed was promoted.

## Suggested next step for the coordinator (not taken — out of budget)

Lane C families need comment-text discovery, which search/issues cannot do:
seed from PRs whose bodies carry agent markers (e.g. "generated with Claude
Code", "via Codex", co-authored-by bot trailers), then fetch their threads
and read for self-review praise / wrong-task admissions / fix loops. That
needs a fresh budget, not a reuse of this run's spent 4+4.
