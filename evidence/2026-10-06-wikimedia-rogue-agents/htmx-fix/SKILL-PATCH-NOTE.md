# Skill-patch note — urlquery htmx endpoint

Date: 2026-10-06 (CDT). Worker: htmx-fix patch-and-rerun.

## Verdict: the skill needs no patch. It is the reference-good pattern.

`~/workspace/skills/urlquery/bin/uq_htmx_curl.py` (and `uq_htmx.py`) already send
**both** `HX-Request: true` **and** `HX-Current-URL: https://urlquery.net/search?q=<query>`.
That combination returns 200 + report rows from `GET /api/htmx/search/`.
`/opt/hatch/skills` was never edited, and nothing about the skill needs to change.

## Where the bug actually bit

The broken results came from **hand-rolled lane copies** that omitted the HX headers —
not from the skill. Inventory (`workers/inventory/INVENTORY.md`) found 11 hand-rolled
htmx variants; 2 sent no HX headers at all (204 on every query, zeros misfiled as clean
negatives), 2 more sent `HX-Request` without `HX-Current-URL`. Patched: the two live
copies (`scripts/archive/collectors/urlquery/reverse_tunnels_htmx_search.py` and
`scripts/archive/collectors/dse-wiki/dse_wiki_verification_expand_search.py`;
diffs in `workers/patch/PATCHES.md`). The frozen-archive duplicates were deliberately
left untouched.

## Key correction to the earlier sweep report

The earlier sweep suggested the fix was "HX-Request emulation headers."
**That is wrong.** Live verification with a negative control
(`workers/verification/VERIFICATION.md`, 2026-10-06) proved:

- No headers → **204 No Content** (even for `webhook.site`, a query with dozens of known results)
- `HX-Request: true` alone → **still 204** (does NOT fix it)
- `HX-Request` + `HX-Current-URL` → **200, 21 rows**
- **`HX-Current-URL` alone → 200, 23 rows** (sufficient; `HX-Request` adds nothing)
- Control `q=zzz-no-such-term-xyz` with `HX-Current-URL` → **200, "No reports found"** (genuine zero, not a 204)

**The header that matters is `HX-Current-URL`, not `HX-Request`.**
Minimal working set: exactly one header — `HX-Current-URL: <the /search page URL>`.
UA spoofing is unnecessary. The skill's both-headers pattern is comfortably sufficient.

## Residual wrinkle: 204s are not cleanly time-gated

Across prior lanes, the PARTIAL pattern (HX-Request + HX-Current-URL, but sent via
`uq_htmx.py`'s urllib path) returned real data for *some* queries while zeroing *others*
in the same session (polyglot `gov.br`→6 reports vs `gov.eg`→0; de-linguist q2/q6/q7→hits
vs q1/q3/q4/q5/q8→`{"reports": []}`; arabic keyword queries→data vs `url.domain:`→zeros;
lighthouse `marinetraffic`→hits vs `mmsi`→0). The failure is therefore **not cleanly
time-gated** — it may be query-dependent, rolling, or throttling-adjacent, and
`uq_htmx.py`'s urllib transport additionally dies in this VM's egress proxy while curl
succeeds. No old-pattern zero could be trusted without a re-read against the fixed
curl pattern — hence the 22-claim re-read queue (`workers/re-read-queue/REREAD-QUEUE.md`,
results in `workers/patch/REREAD-RESULTS.md`).

## Guidance for future lanes

- Use the skill (`uq_htmx_curl.py` — curl transport works on this VM; `uq_htmx.py`'s
  urllib hangs in the proxy CONNECT tunnel), or copy its header set verbatim.
- The one non-negotiable header is `HX-Current-URL: https://urlquery.net/search?q=<query>`
  (percent-encoded query). `HX-Request` is harmless but insufficient alone.
- Always capture the HTTP status code: a 204 body and a genuine zero both parse to
  `{"reports": []}`. 200 + zero rows = honest negative; 204 = failed request.
