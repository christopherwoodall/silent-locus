# PROVENANCE — 2026-10-06 Wikipedia top-500 infra scan

**Task (BigSexyWarlock69, 2026-10-06):** scan the top 500 Wikipedia articles
for edits originating from AI-provider / datacenter infrastructure
(Amazon/AWS, OpenAI, Anthropic, Perplexity, etc. — agents run in
datacenters like Azure). Metrics per provider: edit count, articles
affected, current-vs-reverted status.

**Method reality:** logged-in editors' and temp accounts' IPs are NOT
public. Only historical IP-editor revisions (pre-temp-account rollout)
carry public IPs. Attribution = match those IPs against provider IP
ranges (AWS ip-ranges.json, Azure ServiceTags, GCP cloud.json, plus
published OpenAI/Anthropic ranges). Logged-in/temp-account edits are
unattributable by IP from public data — state this, don't work around it.

**Collection doctrine:** passive/public OSINT only. MediaWiki + pageviews
APIs via curl, paced. Evidence never redacted. Grade
OBSERVED/INFERENCE/UPSTREAM. Cache range files + raw pulls in raw/.
Worktree: ~/workspace/silent-locus-top500 (branch
wikipedia-top500-infra-scan-2026-10-06) — the main tree is busy with the
wikipedia-lane workers.
