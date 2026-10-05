# HUNT LANE 18 — Hacker pastebins (0x0.st, rentry.co, ix.io, hastebin)
Date: 2026-09-27
Task: hunt campaign markers in the curl-pastebins hackers and agents use as dead drops,
via search-engine queries constrained to each domain + Wayback CDX URL queries.
Read-only; nothing uploaded.

## Verdict: clean negative on the search-engine route; CDX route blocked (IA offline).

## Search-engine battery (site:-constrained, exact-phrase)

| Query | Result |
|---|---|
| site:0x0.st "builder alive" | 0 hits |
| site:rentry.co "builder alive" | 0 hits |
| site:hastebin.com "yard exploit" OR "builder alive" | 0 hits |
| site:0x0.st "YARD RAN" | 0 hits |
| site:ix.io "YARD RAN" | 0 hits |
| site:0x0.st/ix.io/rentry.co "yard exploit" | 0 hits |
| site:rentry.co "HOOKED" OR site:0x0.st "HOOKED" | 9 hits — all SEO spam / erotica / spam-blog noise on rentry.co (e.g. https://rentry.co/irtno/edit, https://rentry.co/sbkusbso). Zero campaign content. |
| site:0x0.st/rentry.co "malicious crawler" | 0 hits |
| site:rentry.co "go-import" | 0 hits |
| site:ix.io/hastebin.com "go-import" | 0 hits |
| site:rentry.co "r.jina.ai" | 0 hits |
| site:ix.io/0x0.st "southwarkssrfhack" | 0 hits |
| site:0x0.st/rentry.co/ix.io/hastebin.com "southfetchprobe" | 0 hits |
| site:0x0.st/rentry.co/ix.io "1778551714" (epoch marker) | 0 hits |

Notable: the HOOKED query confirms rentry.co pages ARE indexed by search engines
(custom-URL pastes show up), so the search-engine route has genuine coverage of
rentry — the zero results on campaign markers are meaningful there, not a
coverage artifact. 0x0.st/ix.io use opaque hashes and are less indexed, so
absence there is weaker evidence.

## Wayback CDX route: BLOCKED this run

Every CDX query (rentry.co*, 0x0.st*, ix.io*, hastebin.com* with marker filters
for southwark/jina/yard) returned Internet Archive's "Temporarily Offline" page
— the CDX API is down/unreachable right now (consistent with the standing
"Wayback unreachable" park). This lane should be re-run when IA recovers:
CDX urlkey-filter queries like
`url=rentry.co*&filter=original:.*(southwark|jina|yard).*` are the right shape.

## Interpretation

- No campaign beacon strings, payload markers, name grammars, or laundering URLs
  surfaced in any indexed paste on these four services.
- The operator class's dead-drop behavior in this campaign stayed inside the
  RubyGems registry itself (gem metadata board) plus the webhook dead-drop
  channel (southpxdatapp6pi, per JFrog) — no evidence of spillover to public
  pastebins.
- Caveats: 0x0.st/ix.io content is barely indexed (hash URLs); hastebin
  instances are fragmented (many self-hosted); CDX — the strongest route for
  these services — was unavailable. Re-run when IA is back.

## Follow-ups

1. Re-run the CDX URL-filter queries when web.archive.org recovers.
2. Consider termbin.com / sprunge.us (same service family, not covered).
3. The 224 archived Pastebin pastes (Iowa agent-comms mesh, June 16 wave) are a
   separate queued lane in the SwarmTraces phase-two work — different corpus,
   not this campaign.
