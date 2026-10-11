# PROVENANCE — perplexity-intel lane

## Raw sources

Lane: `perplexity-intel`. Purpose: officially published Perplexity AI
crawler egress IP ranges, ingested as `infra.ioc` records (category `ip`).

### Source 1 — PerplexityBot ranges

- Source URL: https://perplexity.com/perplexitybot.json
- Official docs page: https://docs.perplexity.ai/docs/resources/perplexity-crawlers
- Retrieval time (UTC): 2026-10-11T01:23:00Z to 2026-10-11T01:23:06Z
- Retrieval method: curl -sL over egress proxy, saved to raw/perplexitybot.json
- sha256: 2688b50802b42611b412f8ac3bc614248d0eab00d74f4ceda41cb78526bde6b2
- Source creationTime (as published in file): 2025-02-07T16:56:00.000000
- Prefix count: 8 (IPv4 only)

### Source 2 — Perplexity-User ranges

- Source URL: https://perplexity.com/perplexity-user.json
- Official docs page: https://docs.perplexity.ai/docs/resources/perplexity-crawlers
- Retrieval time (UTC): 2026-10-11T01:23:00Z to 2026-10-11T01:23:06Z
- Retrieval method: curl -sL over egress proxy, saved to raw/perplexity-user.json
- sha256: 23e55350c44ac51a8a6e7ed786d861db8bc62886fd1cfc228dfa467127223e48
- Source creationTime (as published in file): 2025-10-17T10:17:00.000000
- Prefix count: 4 (IPv4 only)

## Verification

Both endpoints are the operator-published crawler IP lists referenced by
Perplexity's own crawler documentation and by third-party vendored lists
(e.g. PostHog posthog#68660). The two files together list 12 CIDR prefixes,
all IPv4. Both files fetched cleanly on first attempt; sha256 values match
the earlier /tmp download from the same URLs.

## Claim grading

All 12 `infra.ioc` records are graded OBSERVED: the CIDR strings are copied
verbatim from the published files. No inference was added. The files are
UPSTREAM-published by Perplexity (the provider), retrieved by the collector.
