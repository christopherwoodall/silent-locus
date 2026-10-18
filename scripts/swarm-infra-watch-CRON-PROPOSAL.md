# Swarm Infrastructure Watch — Cron Proposal

**Status:** PROPOSED — awaiting BigSexyWarlock69's approval to register.

## Schedule

- **Interval:** Every 6 hours
- **Timezone:** America/Chicago
- **Owner:** goal:urlquery-agent-activity-hunt
- **Delivery:** main chat (only on tier 1-2 hits or spikes)

## Job Body

Monitor for Chinese Amap fleet resurgence via webhook.site creator-IP records.

**Method:** Harvest webhook.site inbox URLs from urlquery (fleet tag grammar
+ Amap tradecraft searches), then GET each inbox's token metadata to extract
the creator IP. Classify creator IPs into 4 tiers. Log tier 1-2 hits to factum.

**Critical distinction:** Creator IP (token metadata `ip` field = who created
the inbox) vs poster IP (`/requests` endpoint per-request source = who sent
requests). We extract the creator — that's the operator infrastructure signal.

**Crawler:** `~/workspace/silent-locus/scripts/swarm-infra-crawler.py`
**Config:** `~/workspace/silent-locus/scripts/swarm-infra-config.json`
**Classifier:** `~/workspace/silent-locus/scripts/ip_classifier.py`
**State:** `~/workspace/goals/urlquery-agent-activity-hunt/hidden_files/swarm-infra-crawler-state.json`

**Each run:**
1. Run: `python3 ~/workspace/silent-locus/scripts/swarm-infra-crawler.py`
2. Check output in `~/workspace/silent-locus/data/lanes/swarm-infra-watch/`
3. For MEDIUM+ findings: verify, then submit to factum via lane-ingest worker
4. State file updates automatically (idempotent, tmp+rename)

**Rate limits per run:**
- urlquery htmx: ~7 searches × 3s delay ≈ 1-2 min
- webhook.site: 1 GET per new inbox × 2s delay (typically 0-5 new)
- ipinfo.io: 1 per uncached IP × 1s delay (persistent cache)
- Total: < 5 minutes per run

**Report to user ONLY when:**
- New inbox with tier 1 (KNOWN_SWARM) creator IP
- New inbox with tier 2 creator IP on swarm-linked ASN (AS132203/AS45090)
- Spike: >5 new fleet-indicator inboxes in one run

Otherwise end quietly. Never posts, never publishes inbox UUIDs, never invents.

**Baseline (2026-10-14):** 25 inbox UUIDs from the Amap fleet lane — all 404.
The 7-day webhook.site expiry wiped the fleet's inboxes. This watch targets
NEW inboxes going forward.

## Registration

To activate (requires BigSexyWarlock69's go-ahead):
```
# Via cron tools:
# cron.add with the above schedule and job body
```

## Why 6 Hours

- Matches the dead-drop family watch cadence (consistent monitoring rhythm)
- Fleet moves fast (Oct 14 session: 4 posts in 18s, inboxes gone in 2h)
- 6h is the sweet spot: catches new infrastructure without API hammering
- urlquery's 7-day search window means no gaps at 6h intervals
- Shodan/crt.sh dropped per redirect — no credit burn concerns
