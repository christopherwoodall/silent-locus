# Agent Sandbox Fingerprint Research — 2026-10-14

**Question from BigSexyWarlock69:** What other agent sandboxes should we add to monitoring? The `hysandbox-ats` proxy marker was our key fingerprint for the Tencent fleet.

## Bottom line

**Commercial sandboxes (E2B, Modal, Daytona, etc.) have no viable network-identity fingerprint.** The hysandbox case was exceptional, not a template. Detection stays behavioral (urlquery tradecraft, webhook creator IPs), not network-identity.

**Added to config:** Huawei Cloud ASN (AS136907) as CLOUD_SERVICE tier. Nothing else survived adversarial review.

## Commercial sandboxes — investigated and killed

### E2B
- **Egress:** No documented static egress IPs. Supports BYOP (bring-your-own-proxy): SOCKS5 tunneling through operator-chosen proxies. An operator who wants to hide will.
- **Opt-in DSCP marker** (SANDBOX_EGRESS_DSCP) exists in their infra repo — but default-off, L3-only, won't survive to our vantage point.
- **Verdict:** KILL. BYOP makes IP fingerprinting fundamentally unreliable. Shared cloud IPs for everyone else.

### Daytona
- **Egress:** Dynamic by default. Static egress IPs are a GitHub proposal (daytonaio/daytona#3825), not shipped.
- Lower tiers restrict egress to an "essential services" allowlist that can't be overridden — actually makes Daytona LESS useful for fleet operators.
- **Verdict:** KILL. No stable fingerprint exists.

### Modal
- **Egress:** Per-provider network restrictions; traffic exits via Modal's shared infra IPs.
- **Verdict:** KILL. Shared cloud IPs, no distinctive markers.

### General principle
Commercial sandboxes are DESIGNED to look like normal cloud traffic — that's the product. An IP-based fingerprint on any of them = massive false positives (thousands of legitimate customers on the same ranges). There is no `hysandbox-ats` equivalent because there's no custom proxy label to find.

## Chinese cloud agent sandboxes — investigated

### Tencent CubeSandbox (open-source, Apache 2.0)
- Purpose-built AI agent infra, MicroVMs, <60ms boot. Supports the E2B API (env-var switch).
- Uses "CubeEgress" L7 MITM proxy for outbound traffic.
- **Closest public artifact to hysandbox.** But: self-hostable = operator's own IPs, not Tencent's. No externally observable fingerprint beyond the ASN of whoever hosts it.
- **Verdict:** No new fingerprint. Already covered by Tencent ASN classification.

### Alibaba AgentBay (alibabacloud.com/en/product/agentbay)
- Alibaba's agent runtime: Linux, Windows, Android, browser sandboxes.
- Egress ASN = Alibaba Cloud (AS45102/AS37963) — already in our config as CLOUD_SERVICE.
- **Verdict:** No new fingerprint beyond existing ASN classification.

### Alibaba OpenSandbox (open-source, Apache 2.0)
- Note: distinct from opensandbox-group/opensandbox (different project, similar name).
- Self-hostable = operator IPs. No external fingerprint.
- **Verdict:** KILL as network fingerprint.

### Alibaba ACS Agent Sandbox / Agent Native Cloud
- Container Compute Service agent sandbox (MiniMax partnership). "Agentic Computer" for cloud execution.
- Enterprise product; egress from Alibaba Cloud ranges.
- **Verdict:** Covered by existing Alibaba ASN classification. No new fingerprint.

### Huawei Cloud AgentArts
- Agent platform announced at WAIC 2026, financial-services focus.
- ASN AS136907 — **ADDED to config as CLOUD_SERVICE tier.**
- No fleet evidence pointing at Huawei. This is coverage, not signal.
- **Verdict:** Added for completeness. Low priority.

## The renamed-proxy-string pattern

The real lesson of `hysandbox-ats` isn't the string — it's the METHOD: a custom proxy label on a self-reported Via header, combined with cloud IPs and a cert, cracked open by sloppy opsec.

We cannot generically detect "renamed proxy strings" — the next one won't look like `hysandbox-ats`. But we CAN note it as detection logic for the urlquery lane: when we collect traffic, flag Via headers with non-standard labels for analyst review. That's a behavioral heuristic, not a fingerprint.

**Recommendation for the urlquery scanner:** add a `via_anomalies` check — any Via header that isn't a well-known proxy product string gets logged as a candidate. Low cost, catches the NEXT hysandbox.

## What actually works (and what we're already doing)

| Method | Why it works | Status |
|---|---|---|
| urlquery tradecraft (tag grammar, Amap targeting) | Behavioral — the fleet's actual code runner | Lane 1, HIGH |
| webhook.site creator IPs | Attribution method — worked for the researchers | Lane 2, MEDIUM |
| ASN classification (cloud vs residential) | Cheap, catches infra-class anomalies | Standing rule, all lanes |

## Config changes made

1. Added `AS136907` (Huawei Cloud) to `cloud_asns` as CLOUD_SERVICE, `swarm_linked: false`.
2. Added `_comment_sandbox_research` documenting why commercial sandbox IP fingerprinting doesn't work.
3. Added provenance note for AS136907.

## Sources

- E2B infra repo (BYOP SOCKS5, DSCP marker): github.com/e2b-dev/infra
- Daytona static-egress proposal: github.com/daytonaio/daytona/issues/3825
- Tencent CubeSandbox: github.com/TencentCloud/CubeSandbox
- Alibaba AgentBay: alibabacloud.com/en/product/agentbay
- Agent sandbox comparison (15 providers): upstash.com/blog/ai-agent-sandbox-providers-compared-2026
- Awesome agent sandboxes list: github.com/ianwieds/awesome-agent-sandboxes
- Fleet secondaries: cyberpress.org, gbhackers.com, pondero.ai, undercodenews.com
