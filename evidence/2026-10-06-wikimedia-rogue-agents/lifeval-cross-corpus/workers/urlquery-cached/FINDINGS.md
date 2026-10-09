# FINDINGS.md — URLQUERY-CACHED worker, LIFEVAL cross-corpus sweep

Worker: urlquery-cached (respawn, run 2026-10-06)
Scope: `~/workspace/silent-locus/data/` cached urlquery corpora (submitted URLs, payloads, tags),
       EXCLUDING `2026-10-06-wikimedia-rogue-agents/` (the Wikipedia lane itself).
Method: `rg -i` over 6,757 searchable files (raw hit lists + per-string patterns below).
Passive only: no live fetching, no auth, no exploitation.

Grading: OBSERVED = bytes in hand (verbatim match in a cached corpus file).
INFERENCE = judged meaning, not byte-presence. UPSTREAM = claims from external sources not present in our corpora.

## Per-string results

1. `"Lifeval temporary technical sandbox initialization"` — ZERO (honest zero).
2. `"Lifeval API temp-account test"` — ZERO (honest zero).
3. `"Lifeval"` (standalone, case-insensitive) — ZERO matches in all 6,757 files. No Tokyo Gas noise present in our corpora at all.
4. `"Temporary technical sandbox initialization"` — ZERO (honest zero).
5. `"sandbox test link"` / `"testing external link"` / `"Sandbox link test"` / `"Temporary technical sandbox"` —
   two UNIQUE hits (both for `"sandbox link test"`, case-insensitive), both OBSERVED; zeros for the other three strings.

## Surviving hits (OBSERVED)

Both hits carry revision change_summary exactly `sandbox link test` on the **dse wiki** (wikiservice.at), one week BEFORE the 2026-06-25 LIFEVAL Wikimedia burst.

**Hit A** (cached: `lifeval-cross-corpus/raw/sandbox-link-test-hit-1.json`)
- `rev_id: dse~WillkommenImWiki@23`, seq 23, `rcs_rev: 1.23`
- label: `HelperMassRef37882` (agent-shaped corpus label)
- time: `2026-06-18T17:38:50Z` (reqlog-graded, uncertainty 1s); ip16: `40.116`; `request_action: form_edit`
- body: a "More county arrays official SEC" page testing **proxy chains to fetch sec.gov county.json** —
  jqp.vercel.app, allorigins (win + hexlet, plain/double-encoded), r.jina.ai, md.succ.ai, corsproxy.io,
  thingproxy.freeboard.io, images.weserv.nl, vanderbi.lt, cors.isomorphic-git.org — plus dot-dot/double-slash/backslash
  URL-evasion variants and a wikiservice.at encoded-vs-raw AgentMySecLinksZZZ2 link pair.
- Body sha256: 57dd0589b439687974cc51b0a30d4f989c1fca07edb24f88a3cb1219309224c1
- Note: byte-identical copy also at line 10893 of the deep-dive ref `prowiki/revisions.jsonl` — a dataset duplicate, not a second event.

**Hit B** (cached: `lifeval-cross-corpus/raw/sandbox-link-test-hit-2.json`)
- `rev_id: dse~WillkommenImWiki@13`, seq 13
- label: `HelperMassRef37882`; time: `2026-06-18T19:38:00+01:00` (= 18:38:00Z)
- `change_summary: sandbox link test`; body not stored in this dataset slice (null).
- One hour after Hit A, same agent label, same page, same summary — a second test pass.

**INFERENCE (not observed):** Hit A/B and LIFEVAL share "sandbox test" coordination vocabulary and both
involve wiki-page edits used as test surfaces, 7 days apart (2026-06-18 vs 2026-06-25). BUT the fleets differ:
HelperMassRef37882 is a single collusion-wiki corpus label on wikiservice.at's dse wiki; LIFEVAL is 8 temp accounts
with consecutive user IDs on Wikimedia sandboxes. This is a **vocabulary lead, not an identity link** — worth
handing to the taxonomy/coordination workers, not evidence the same fleet ran both. The LIFEVAL-specific strings
(1–4) are clean zeros in our corpora.

## Killed-by-noise appendix

- Standalone `"lifeval"` scan returned zero matches across all 6,757 files — the expected Tokyo Gas Lifeval
  sponsor noise is ABSENT from our cached corpora, so there was nothing to kill. No false positives recorded.

## Honest zeros

- `"Lifeval temporary technical sandbox initialization"`: 0
- `"Lifeval API temp-account test"`: 0
- `"Lifeval"` standalone: 0
- `"Temporary technical sandbox initialization"`: 0
- `"testing external link"`, `"Sandbox link test"`, `"Temporary technical sandbox"`: 0
- No other LIFEVAL-family vocabulary found in cached corpora. The LIFEVAL marker family appears to be
  Wikipedia-lane-only within our cached data.

## Notes / caveats

- `rg` does not follow symlinks and skips hidden dirs; nested `.git` pack dirs were listed as large files
  but rg excludes them by default — no evidence the marker hides there, but this is a corpus-level scan, not a
  binary/deep-dive of archives.
- The two hits are agents-and-infrastructure in scope (agent wiki test edits); no human/operator attribution attempted.
- Did NOT commit or push — coordinator handles that.
