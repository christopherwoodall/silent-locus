# Lane B — best-of sweep, 2026-10-24: NO citable comment candidates

Operator: BigSexyWarlock69. Method: unauthenticated GitHub API, curl only.
No commits, no pushes, no POST, no login. No comment JSON captures were
written because no fetched comment matched a lane-B family; inventing a
capture from PR body/title text would have violated the capture rule
(every cited item must be a comment with a comment id).

## What the search API actually did

`search/issues` matched PR titles/bodies as well as comments, and its
quoted-phrase counts were implausibly large (94k–830k), so the returned
PRs were mostly body/title matches, not comment matches. Three of the
four candidate PRs had zero issue comments and zero review comments.
The fourth had only routine maintainer/bot comments.

## Searches used (4)

1. `"did not run the tests" type:pr` — total_count 94394
2. `"hallucinated" type:pr` — total_count 49857
3. `"I apologize" type:pr` — total_count 129897
4. `"I updated the test" type:pr` — total_count 829719

## Candidate PR threads fetched (4 PRs, 6 thread calls)

1. SecurityRaccoon-Demo/demo-nodegoat PR #17 — 0 issue comments,
   0 review comments. Title: "[Raccoon] Fix: Remove non-existent package
   raccoon-ai-hallucinated-helperz". NEAR-MISS ONLY: the hallucinated
   package is in the title/body, not in any comment, and the repo is a
   demo — it may be a fixture for a detector, so it must NOT be cited
   as a confirmed antic without a comment proving live behaviour.
2. kdobmayer/kond-test-target PR #23 — 0 issue comments, 0 review
   comments. Title contains "I apologize, but I am unable to directly
   ..." — NEAR-MISS ONLY: classic LLM-refusal wording in the PR
   title/body, not in a comment; no comment capture exists.
3. tale/headplane PR #670 — 0 issue comments. Docs one-click-deploy
   PR; no lane behaviour in any comment because there are none.
4. huggingface/transformers PR #49915 — 5 issue comments, all routine:
   maintainer CC (guarin, User/MEMBER), github-actions[bot] CI/slow-job
   notices (Bot/CONTRIBUTOR), HuggingFaceDocBuilderDev docs notice
   (User/NONE). No lane-B behaviour.

## Counts

- Searches: 4. Candidate PR comment-thread fetches: 6 calls across
  4 PRs (4 issue-comment calls + 2 review-comment follow-ups where
  issue comments were empty and the PR looked promising, per the brief's
  review exception). Plus 1 free /rate_limit check at the start.
- Total counted API calls: 10 (under the 12-call cap).
- Last X-RateLimit-Remaining seen: 56 (core, after the final review
  fetch; the bucket fluctuated 55–59 across calls, consistent with
  sibling-lane sharing, and no 403/429 was hit).
- Queries returning nothing: none returned zero results, but all four
  returned noisy, mostly body/title matches rather than comment hits.

## Recommendation to the coordinator

Lane B needs a different discovery route for the "best of" set: the
search/issues endpoint cannot isolate comment text, so a comment-first
source (e.g. a prior scanner hit list with known comment ids, or a
live-browser pass over known agent-PR threads) is required before any
lane-B entry can be honestly cited. Do not promote the two near-misses
above into entries without a real comment.
