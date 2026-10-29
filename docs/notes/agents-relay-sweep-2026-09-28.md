# agents-relay.com sweep — 2026-09-28

Follow-up to the agent-convo-venues lane. Dataset: `data/agents-relay-sweep/`
(10 docs). Read-only throughout; no posts, no accounts, no submissions; no
hosted Elastic writes.

## The lead
agentchan.org/b/thread/7 post No.1183 (2026-02-01): "posting from the relay
— built a thing so agents can message each other directly instead of just
vibing on imageboards." skill.md at https://agents-relay.com/skill.md,
open-source repo at https://gitlab.com/memoclaudio/agent-relay, 9 agents at
the time of posting.

## Verdict: verified unreachable / dead
- DNS resolves to 198.18.124.245 — inside the IETF benchmarking range, most
  likely an egress-interception artifact rather than the real host.
- curl: HTTP 000 / 0 bytes on http and https, apex and www (with
  cache-busting nonces per standing rule).
- Text-fetch of /skill.md: empty upstream 500 after 3 attempts.
- The GitLab repo is blocked by fetch policy; not bypassed — recorded as an
  access gap in the dataset.
- Web search: zero mirrors, forks, or discussion of agents-relay.com or the
  memoclaudio repo anywhere indexed.
- Corpus grep: no other agents-relay references outside the agent-convo-venues
  lane's own records.

No swarm markers observable — there is no reachable message surface to scan.

## Caveats
- **Namespace collision:** the bare name "agent-relay" is heavily reused by
  unrelated projects (Tailscale peer-messaging skills, coding-agent mailbox
  hubs, orchestration CLIs on GitHub). Future lanes must not confuse them with
  memoclaudio's agents-relay.com.
- If the site recovers or the repo becomes fetchable, re-run: the protocol
  spec and any public traffic would be worth a full marker sweep.
