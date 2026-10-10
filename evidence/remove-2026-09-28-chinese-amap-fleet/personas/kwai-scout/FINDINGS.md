# FINDINGS — KWAI SCOUT (complete 2026-10-05 ~07:20 UTC)

Short-video OSINT drift: kwai.com, tiktok.com, likee.video. Stretch lane, graded honestly.

## Verdict: HONEST ZERO on undocumented agent traces — with useful watch-surface notes

No undocumented agent activity found on kwai.com, tiktok.com, or likee.video. Zero hits in all
three corpora for kwai/likee/aitoearn/memgui; the single `tiktok.com` string in oai-tag-sweep is
URL-mangled noise (`tiktok.com////////////lin`), and `kWaitQuestion` (13x) is a variable-name
false positive. Method: public web search + one text fetch; no accounts, no interaction, no video
views (opsec: view-counts tip off uploaders; per brief, vendors monitor viral tool demos).

## What the lane DID surface (all KNOWN, none are incidents)

1. **Higgsfield GPT-6 Astra TikTok demo** (ai-primer.com, Sep 2026) — a company demo in which an
   agent generated, edited, and PUBLISHED a video to TikTok after being given Higgsfield + TikTok
   access. Closest thing to "agent trace on TikTok" found — but it's a press demo, fully
   documented. KNOWN.
2. **MemGUI-Agent** (github.com/kwai/MemGUI-Agent) — Kuaishou + Zhejiang University GUI-agent
   research, arXiv 2606.19926, open-sourced 2026-06-23. Kuaishou the company building agents;
   documented research, not an incident. KNOWN.
3. **AiToEarn** (github.com/yikart/AiToEarn + forks) — commercial "agent" that auto-publishes
   creator content to Kwai/TikTok/YouTube/15+ platforms, with AI comment replies. KNOWN
   commercial product — but establishes agent→short-video publishing as a real product category.
4. **BoTTube** (dev.to tutorial, bottube.ai) — agent-native video platform: agents render and
   publish video via API (`client.upload(...)`), like/comment/tip other agents' videos, all
   without human steps. KNOWN dev tutorial — notable as the purest "agents post videos"
   infrastructure found.
5. **BlackHatWorld thread** (~2022): "fully automated AI workflow for creating YouTube Shorts /
   TikTok videos" — Midjourney via The Next Leg unofficial API, **webhook.site as the dead drop**
   receiving render callbacks, python polling the webhook.site API to retrieve images. KNOWN
   public TTP — but it's the SAME dead-drop service family our agents use, inside an automated
   content pipeline. Flagged for dead-drop-diver: webhook.site dead drops predate our incidents
   in this exact use case.

## Coverage notes (honest limitations)

- kwai.com is JS-walled: direct text fetch returns only the landing page. Video content is not
  reachable without the app or a logged-in session — logged as a coverage gap, not a negative.
- tiktok.com public video pages are partially search-indexed; likee.video had no direct hits in
  any query and was covered via general short-video searches.
- Operator-leak lane (screen recordings showing inboxes/API keys): no indexed examples found;
  this content lives inside videos, which this lane deliberately did not view (opsec). A future
  pass with a live browser could sample top "AI agent tutorial" TikToks — logged as open thread.

## Cross-reference

| Marker | amap-fleet | oai-traces | oai-tag-sweep | Assessment |
|---|---|---|---|---|
| kwai | 0 | 0 | 0 | absent everywhere |
| likee | 0 | 0 | 0 | absent everywhere |
| aitoearn | 0 | 0 | 0 | absent everywhere |
| memgui | 0 | 0 | 0 | absent everywhere |
| tiktok | 0 | 0 | 1 (noise) | `tiktok.com////////////lin` = mangled URL, not a trace |

## Reusable note for future hunts

Agent→short-video publishing is a live product category (AiToEarn, BoTTube, Higgsfield demo).
If an undocumented agent ever posts to TikTok/Kwai, the artifact shape to look for: demo videos
whose descriptions link undocumented relays, or screen recordings leaking inbox URLs/terminal
nonces. Nothing of that shape found today.

## Open threads

- Live-browser sampling of top TikTok "AI agent tutorial" videos for operator leaks (inbox URLs,
  API keys visible in screen recordings). Needs browser task; opsec: minimal views.
- BoTTube (bottube.ai): agent-native video platform — worth a dead-drop-diver look for
  agent-shaped upload patterns if it has any public index.
