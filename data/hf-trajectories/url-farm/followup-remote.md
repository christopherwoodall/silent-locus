# Follow-up: remote-website checks on juicy URL targets

Date: 2026-10-08. Branch: `url-keyword-farm`. Coordinator merge of 4 lanes.
Prior: `allorigins-deepdive.md`. All checks read-only (GET/HEAD only).

## Verdicts

### 1. Cloudflare Workers `?url=` proxies — SINGLETON (not shared infra)
Both workers live: HTTP 400 on bare `/`, HTTP 200 proxying `?url=https://example.com`
— functional CORS proxies with media-streaming headers (Accept-Ranges, Range
passthrough). Origins partially live (gg.hls2.xyz 403/connect-fail, ncdn.telewebion.ir
301); through-worker HLS fetch 404s (worker alive, upstream path gone).
Zero web hits for the exact subdomain fragments (no GitHub/paste/forum references);
urlquery API search on both subdomains → 0 reports. Only hermes row 441 in the whole
corpus references them. Two different Cloudflare account subdomains (ATL vs DFW PoPs)
suggests per-run throwaway deployment, not a shared operator service. OBSERVED.

### 2. webhook.site 27-hit UUID — DIFFERENT-DROP-DEAD + bookkeeping correction
Correction (OBSERVED): the UUID passed to the lane (95299740-…) is the hermes
train.jsonl row ID, not a webhook token. The true 27-hit webhook.site UUID in
crownelius gpt-5.6 traces is the Meraki docs example URL — already triaged FALSE
POSITIVE in URL-KEYWORD-FARM.md ("FP, no live drops"); it appears only in
judge-go-meraki-action-batch-* tasks (docs-artifact traffic, not exfil).
Cross-check (OBSERVED): neither UUID matches any of the three known family inbox
token_ids (verified locally against raw captures; zero network). Live probes
(OBSERVED): GET /token/<uuid>/requests → HTTP 404 for both. Nothing to characterize.
`allorigins-deepdive.md` line 163 conflated the two UUIDs — corrected in this commit.

### 3. transfer.sh / discord / pastes — DEAD / BENIGN / DEAD
- transfer.sh/zork.wav: DEAD. Host non-responsive (curl 52, empty reply even on `/`).
  With the 14-day purge policy, forensically unrecoverable either way. OBSERVED.
- discord.com/invite/uyRQKXhcyW: LIVE. Guild "CrossGL" (235 members, permanent
  invite) — benign public graphics-API community. OBSERVED.
- discord.gg/9BrxzPKuEW: LIVE. Guild "Cookiecutter" (579 members, permanent) —
  benign public dev-tool community. (Inviter clan tag "Jev" is profile flair, not
  agent-infra evidence.) OBSERVED.
- paste.pound-python.org/raw/3WgFQIvkVVvBZvQI3nm4/ (+ sibling 8nQKbDW0ROWvS7bOeAb3/):
  DEAD. DNS+TLS complete, then empty reply on :443 and :80 — service down/filtered
  at origin. Content uncharacterizable. OBSERVED.

### 4. 169.254.169.254 IMDS hits — BENIGN / FALSE POSITIVE
Correction (OBSERVED): the 2 hits are NOT in browseragent datasets — both are in
TIGER-Lab/SWE-QA-Pro-SFT-Trajectories train.jsonl (lines 45, 489). Both URLs occur
only inside `view_codebase` tool responses — viewed third-party OSS source, never an
agent action. Hit 1: `ec2_metadata()` in datacube-core, used for boto3 region
auto-detection (agent only read the file). Hit 2: `can_schedule()` in NetKAN-Infra,
instance-id as a CloudWatch dimension for CPU-credit throttling. Both agents are
strictly read-only (no network tool; zero agent-issued HTTP requests). No
iam/security-credentials path, no exfil patterns in either trajectory. The
deepdive's "cloud metadata probing (2x)" framing is corrected to "IMDS URLs inside
viewed OSS source; no agent-issued requests." OBSERVED.

## Bottom line
No lead shows other agents on the remote websites. Workers: live but singleton.
UUID: dead FP, not the family. transfer.sh/pastes: dead. Discords: live, benign.
IMDS: not agent behavior at all. The remote-website angle is exhausted for this
target set — further work should stay in-trajectory.
