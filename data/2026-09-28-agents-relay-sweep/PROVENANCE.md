# Provenance — agents-relay-sweep (2026-09-28)

Follow-up to the agent-convo-venues lane (commit 6d276bd), which found
agentchan.org/b/thread/7 post No.1183 (2026-02-01) describing
**agents-relay.com**: "built a thing so agents can message each other
directly", skill.md at https://agents-relay.com/skill.md, open-source repo
at https://gitlab.com/memoclaudio/agent-relay, 9 agents at time of posting.

## Method
- Read-only recon only. No posts, no messages, no accounts, no signups, no
  submissions of any kind. No payload execution (nothing installed or run).
- Liveness probes: DNS query, curl GET (http/https, apex and www, with
  cache-busting nonce per standing rule), text-fetch of /skill.md.
- Source post re-read via text-fetch of the public agentchan thread.
- Web search for mirrors/discussion of agents-relay.com and the
  memoclaudio/agent-relay repo.
- Corpus grep for "agents-relay" across data/ and notes/ (only the
  agent-convo-venues lane's own records matched).

## Result
**Verified unreachable / dead from our vantage.** DNS resolves to
198.18.124.245 (IETF benchmarking range — likely an egress-interception
artifact); all HTTP/HTTPS probes to apex and www fail at connection level
(HTTP 000, 0 bytes); the skill.md fetch returns an empty upstream 500 after
retries. The GitLab repo is blocked by fetch policy and was not bypassed —
recorded as an access gap, not worked around.

## Corpus markers checked
zz labels, epoch nonces, transfer-test grammar, proxy-ladder URLs
(jqp / pure.md / md.succ.ai / r.jina.ai / allorigins), machine-grammar
titles, NSI/stats-venue references, relay/bridge coordination — none
observable: no message surface is reachable to scan.

## Caveats for future lanes
- The bare name "agent-relay" is heavily reused by unrelated projects
  (GitHub forks doing Tailscale peer messaging, coding-agent mailboxes,
  orchestration CLIs). Do not confuse them with memoclaudio's
  agents-relay.com.
- If the site recovers or the repo becomes fetchable, re-run this lane:
  the protocol spec and any public traffic would be worth a marker sweep.

## Schema backfill 2026-09-29
- Transform: `temp/backfill_w2.py`. Added `@timestamp` = `labels.observed_at`
  (UTC Z); `labels.timestamp_source = "labels:observed_at"`.
- record_kind: unchanged (`liveness_probe`, `access_gap`, `finding`,
  `source_reference`, `verdict` kept verbatim).
- fingerprint: original slugs (`probe-dns-001`, `verdict-010`, ...) were not
  64-hex and failed the schema; preserved losslessly as
  `labels.legacy_fingerprint`. New fingerprint = `sha256(<original slug>)`,
  e.g. `sha256("probe-dns-001")`. Identity string = the original slug.
