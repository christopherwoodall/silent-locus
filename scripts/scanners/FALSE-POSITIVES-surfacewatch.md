# FALSE-POSITIVES — Lane 13: surfacewatch

This file lists the noise the surfacewatch scanner will see. A content
hash change is not agent activity until it is corroborated. Every hit
means one thing only: "the content hash changed at <url>". Triage each
hit before any stronger claim.

## Deployments (the dominant noise)

Static sites redeploy often. Each deploy rotates build IDs, asset
hashes, and cache busters without changing what an agent reads.
The scanner strips these per the documented volatile-token policy:
buildId fields, `/_next/static/` hashes, `?v=` / `?t=` / `?build=` /
`?cb=` query params, and HTML comments. A deploy that only rotates
these values produces no hit. A deploy that also changes real content
produces a hit, and that hit is correct — the content did change —
but it is still a routine deploy until triaged.

## Date and counter strings

Pages carry timestamps ("last updated", footers, sitemaps) and
counters (visitor counts, message counts). ISO-8601 timestamps and
`datetime=` attributes are stripped by the html policy. `Last
updated` / `Updated` / `Date` / `Generated` header lines are stripped
by the text-doc policy (llms.txt, skill.md). Counters are NOT
stripped: a counter that ticks up changes the hash and fires a hit.
Treat counter-only changes as noise. If a target's counters prove
chronically noisy, add a documented strip rule to the target's
volatile-token policy (counsel review required for policy changes).

## Ad and A/B script churn

Third-party script tags (analytics, ads) carry rotating query
parameters and per-request tokens. Cache-buster params are stripped.
A/B variants that change visible copy are NOT stripped: two fetches
can see different variants and fire a hit. Treat hits that resolve to
script-tag or marketing-copy rotation as noise.

## Cloudflare and proxy-served variants

Some targets sit behind Cloudflare or a similar proxy. The proxy can
serve different page variants per request (challenge pages, cached
vs fresh, edge-specific headers). A challenge page is detected by
marker strings and treated as a degraded fetch (a gap), never hashed.
Other proxy variants are not detectable: if the proxy serves variant
A on one run and variant B on the next, the scanner fires a hit.
Triage: re-fetch the target manually and compare.

## Bot-detection pages that differ by request

Bot walls (Cloudflare "Just a moment", CAPTCHA interstitials) differ
from request to request. The scanner treats a recognized bot wall as
a gap, not a hit. An unrecognized bot wall changes the hash and
fires a hit. Triage: check whether the change is page-shaped like a
challenge (short body, challenge markers) rather than content-shaped.

## The operator's own benign edits

These are live community surfaces. Operators edit them: llms.txt
rewrites, message board posts, registry updates. A benign edit
changes the hash and fires a correct hit — the content did change —
but it is not agent activity and not suspicious. The summary says
"content hash changed", never "agent activity". Read the diff (fetch
the page by hand) before any stronger claim.

## JSON envelope volatility

The two JSON targets (rel-ochre.vercel.app/api/canon,
agentgateway.pythonanywhere.com/mcp.json) wrap their data in an
envelope. Envelopes carry timestamps, request IDs, trace IDs, and
nonces. The scanner drops these keys recursively before hashing, so
an envelope-only change fires no hit. If a hit fires on a JSON
target, the change is in the non-envelope data — but "non-envelope"
still includes operator edits, so triage still applies. A body that
fails JSON parsing is a degraded fetch (a gap), never a hit.

## Gap semantics

A failed or missing fetch is a GAP. A gap is never a hit, never a
clean negative, and never silently re-baselines the stored hash.
The stored hash is kept across gaps, so when the target recovers,
the scanner compares against the last good baseline. Consecutive
gaps are counted per target. After 3 consecutive gaps (GAP_ALERT_N),
the scanner logs a `target_dark` error entry (identifiers only).
Darkness is an infrastructure note, not a finding.

## Redirects and content-type mismatches

A 3xx response, a final URL that differs from the request URL, or a
Content-Type outside the target's contract is a degraded fetch (a
gap), never a hit. A target that permanently moves is therefore
silent, not alarming — it accumulates gaps until the target_dark
alert fires. Updating the hardcoded target list needs counsel review
and the operator's word (S1).

## Truncated bodies

Bodies are capped at 2MB per target. The hash covers the first 2MB
only, and truncation is recorded in provenance. A page that grows
past 2MB between runs can fire a hit from the truncation boundary
moving. Check the `truncated` flag in provenance when triaging.

## Triage rule

Keep a hit only if a manual re-fetch shows a real content change
that matters to the hunt (new agent-facing instructions, new
registry entries, new board posts of interest). Deploy churn,
counter ticks, date bumps, proxy variants, and benign operator edits
are logged noise, not findings. Never promote a hash change into an
"agent activity" claim without corroborating evidence.
