# SUBSTITUTE.md — self-referential source substitution, monitorable-surfaces-ENRICHED-v2.xlsx

Substitute lane worker, 2026-10-23. Read-only on the .xlsx. This file lists the exact cell edits for the v3 build.

**Rule (operator, 2026-10-23 12:42):** remove ALL self-referential sources. That means: silent-locus GitHub repo links, Factum record and batch IDs, internal evidence paths (`data/lanes/...`, `scripts/...`). Third-party project repos are direct sources. They may stay. Priority order: 1) the live surface URL, 2) the project home page or docs, 3) the project's own repo as a last resort.

**Verification:** curl GET only, one request at a time, no logins, no POST. A replacement passes when it returns HTTP 200 and the title or body shows the claimed surface. Verified 2026-10-23 ~12:35–12:55 CDT.

Every silent-locus GitHub URL is **SELF-REFERENTIAL — REMOVE**. Each points at our own repo. None points at the surface. The replacement is the direct surface URL already present in the same cell, verified live below. One section per unique URL. Rows and columns list every occurrence. (Sheet "Agent POIs", column K = Direct Links; sheet "Intelligence and reporting URLs", column E = Source URL.)

---

## SELF-REFERENTIAL GitHub URLs → remove, substitute with verified direct URL

### 1. `.../tree/main/scripts/scanners/urlquery.py`
- Rows: Agent POIs K4. Remove. Replacement: `https://urlquery.net` — HTTP 200, title "Recent scans · URLQuery". Content: live scan-search service. ✓

### 2. `.../tree/main/scripts/scanners/urlscan.py`
- Rows: Agent POIs K5. Remove. Replacement: `https://urlscan.io` — HTTP 200, title "URL and website scanner - urlscan.io". ✓

### 3. `.../tree/main/data/lanes/anyrun-scan/`
- Rows: Agent POIs K6. Remove. Replacement: `https://any.run` — HTTP 200, title "ANY.RUN - Interactive Online Malware Sandbox". ✓

### 4. `.../tree/main/scripts/scanners/jina.py`
- Rows: Agent POIs K7, K8. Remove. Replacements: `https://r.jina.ai` — HTTP 200, body shows reader endpoint usage instructions; `https://s.jina.ai` — HTTP 200, body shows search endpoint usage + auth note. ✓

### 5. `.../tree/main/data/lanes/2026-08-25-commonlog-scan/`
- Rows: Agent POIs K38. Remove. Replacement: `https://commonlog.ai` — HTTP 200 (100KB body, Commonlog agent-log app). ✓

### 6. `.../tree/main/data/lanes/2026-08-21-public-board/`
- Rows: Agent POIs K39. Remove. Replacement: `https://jotspot.io` — HTTP 200, title "New Jot | JotSpot". ✓

### 7. `.../tree/main/data/lanes/agent-surfaces/`
- Rows: Agent POIs K39, K40, K44, K51, K69. Remove. Each row keeps its own verified direct URL (see rows: jotspot.io ✓, nervesocket.com ✓, agentchan.org ✓, pastebin.tarcseh.me ✓; K51 agent-community.com — FLAG below).

### 8. `.../tree/main/data/lanes/site-captures/`
- Rows: Agent POIs K39, K40, K46, K48, K51, K52, K53, K54, K69. Remove. Rows keep verified direct URLs (nervesocket.com ✓, universalagentforum.com ✓, bookofbots.com ✓, agent-board.juleskreuer.eu ✓, botbook.space ✓, signpost.public-agents.ai ✓, pastebin.tarcseh.me ✓; K51 — FLAG).

### 9. `.../tree/main/data/lanes/2026-09-03-collusion-manifest/`
- Rows: Agent POIs K40. Remove. Replacement: `https://nervesocket.com` — HTTP 200, title "NerveSocket". ✓

### 10. `.../tree/main/data/lanes/2016-12-28-rmn-re/`
- Rows: Agent POIs K41. Remove. Replacement: `https://public-board.com` — HTTP 200, body = agent message-board posts (timestamps + replies). ✓

### 11. `.../tree/main/data/lanes/2018-05-09-paste-archive-gap/`
- Rows: Agent POIs K41, K42, K44, K66, K75, K84, K85, K86, K87, K88. Remove. Rows keep verified direct URLs (openagentforum.com ✓, agentchan.org ✓, anna.fyi ✓, gritpost.com ✓, gotit.pub ✓, mcbin.dev ✓; K75/K84/K85 — see flags).

### 12. `.../tree/main/data/lanes/2026-02-01-agent-convo-venues/`
- Rows: Agent POIs K41, K42, K44, K45. Remove. Rows keep verified direct URLs (public-board.com ✓, openagentforum.com ✓, agentchan.org ✓; K45 agents-relay.com — FLAG below).

### 13. `.../tree/main/data/lanes/2026-08-19-tantive-space/`
- Rows: Agent POIs K42, K43, K46, K48, K51, K52, K53, K54, K55, K56, K70. Remove. Rows keep verified direct URLs (1f916.ai ✓, universalagentforum.com ✓, bookofbots.com ✓, agent-board.juleskreuer.eu ✓, botbook.space ✓, signpost.public-agents.ai ✓, messages.directory ✓, pursekeeper.dev ✓, paste.rs ✓; K51 — FLAG).

### 14. `.../tree/main/data/lanes/2026-10-09-transluce-intel/`
- Rows: Agent POIs K43, K47, K49, K50. Remove. Rows keep verified direct URLs (1f916.ai ✓, rentahuman.ai ✓, openwitness.net ✓, openagentchat.net ✓).

### 15. `.../tree/main/data/lanes/2026-09-28-agents-relay-sweep/`
- Rows: Agent POIs K45. Remove. Surface URL `https://agents-relay.com` — **FLAG — direct source unavailable**: empty reply from server on https and http (curl error 52), consistent on retry. Self-referential links still removed per rule; no verified replacement exists.

### 16. `.../tree/main/data/lanes/2026-05-27-paste-archive/`
- Rows: Agent POIs K66, K68. Remove. Rows keep verified direct URLs (anna.fyi ✓, pastebin.k4be.pl ✓).

### 17. `.../tree/main/scripts/cron/sites/anna_fyi.py`
- Rows: Agent POIs K66. Remove. Replacement: `https://anna.fyi` — HTTP 200, title "Pastebin courtesy of Miss Anna". ✓

### 18. `.../tree/main/scripts/scanners/wayback.py`
- Rows: Agent POIs K66, K67, K68, K69, K70, K71, K77; Intelligence E15. Remove. Rows keep verified direct URLs (paste.linuxiarz.pl ✓, pastebin.k4be.pl ✓, pastebin.tarcseh.me ✓, paste.rs ✓, nicepaste.com ✓, paste.ee ✓; web.archive.org — HTTP 200 on retry, title "Wayback Machine" ✓).

### 19. `.../tree/main/data/lanes/2026-05-17-iowacollab-pastes/`
- Rows: Agent POIs K67. Remove. Replacement: `https://paste.linuxiarz.pl` — HTTP 200, title "paste.linuxiarz.pl". ✓

### 20. `.../tree/main/data/lanes/2026-05-26-paste-linuxiarz/`
- Rows: Agent POIs K67. Remove. Same replacement as 19. ✓

### 21. `.../tree/main/scripts/cron/sites/paste_linuxiarz_pl.py`
- Rows: Agent POIs K67. Remove. Same replacement as 19. ✓

### 22. `.../tree/main/data/lanes/2025-10-24-pastebin-k4be/`
- Rows: Agent POIs K68. Remove. Replacement: `https://pastebin.k4be.pl` — HTTP 200, title "Stikked @ k4be.pl". ✓

### 23. `.../tree/main/scripts/cron/sites/pastebin_k4be_pl.py`
- Rows: Agent POIs K68. Remove. Same replacement as 22. ✓

### 24. `.../tree/main/data/lanes/transfer-test-family/`
- Rows: Agent POIs K69. Remove. Replacement: `https://pastebin.tarcseh.me` — HTTP 200, title "pastebin.tarcseh.me". ✓

### 25. `.../tree/main/scripts/cron/sites/pastebin_tarcseh_me.py`
- Rows: Agent POIs K69. Remove. Same replacement as 24. ✓

### 26. `.../tree/main/scripts/cron/sites/paste_rs.py`
- Rows: Agent POIs K70. Remove. Replacement: `https://paste.rs` — HTTP 200, title "Rocket Powered Pastebin". ✓

### 27. `.../tree/main/scripts/cron/sites/nicepaste_com.py`
- Rows: Agent POIs K71. Remove. Replacement: `https://nicepaste.com` — HTTP 200, title "Nicepaste.com - Best paste tool since 2023!". ✓

### 28. `.../tree/main/scripts/cron/sites/paste_ubuntu_org_cn.py`
- Rows: Agent POIs K72. Remove. Replacement: `https://paste.ubuntu.org.cn` — HTTP 200, title "Ubuntu Paste". ✓

### 29. `.../tree/main/scripts/cron/sites/pastebox_to.py`
- Rows: Agent POIs K73. Remove. Replacement: `https://pastebox.to` — HTTP 200, title "Paste & Share Text or Code Online | PasteBox.to". ✓

### 30. `.../tree/main/scripts/cron/sites/infinitypaste_club.py`
- Rows: Agent POIs K74. Remove. Replacement: `https://infinitypaste.club` — HTTP 200, title "InfinityPaste | Share Code & Text Instantly". ✓

### 31. `.../tree/main/data/lanes/pastebin-cluster-sweep/`
- Rows: Agent POIs K75, K84, K85, K86, K87, K88. Remove. Rows keep verified direct URLs (gritpost.com ✓, gotit.pub ✓, mcbin.dev ✓; K75/K84/K85 — see flags).

### 32. `.../tree/main/scripts/cron/sites/pasteview_com.py`
- Rows: Agent POIs K75, K85. Remove. Surface `https://pasteview.com` — **FLAG — unverifiable via automated GET**: Cloudflare "Attention Required" 403 on https and http. URL exists as the live surface home but cannot be content-verified by curl; keep the URL with the caveat, never rely on it for content claims.

### 33. `.../tree/main/scripts/cron/sites/gritpost_com.py`
- Rows: Agent POIs K75, K86. Remove. Replacement: `https://gritpost.com` — HTTP 200, title "Grit Post". ✓

### 34. `.../tree/main/scripts/cron/sites/gotit_pub.py`
- Rows: Agent POIs K75, K87. Remove. Replacement: `https://gotit.pub` — HTTP 200, title "Gotit Pub". ✓

### 35. `.../tree/main/scripts/cron/sites/mcbin_dev.py`
- Rows: Agent POIs K75, K88. Remove. Replacement: `https://mcbin.dev` — HTTP 200, title "McBin - Recent Pastes". ✓

### 36. `.../tree/main/data/lanes/2026-09-28-chinese-amap-fleet/`
- Rows: Agent POIs K76, K81, K89, K90, K98. Remove. Rows keep verified direct URLs (bytebin.lucko.me ✓, bytebin.rkslot.nl ✓, webhook.site ✓; K98 — FLAG below).

### 37. `.../tree/main/data/lanes/2026-10-16-slow-swarm-crawl/`
- Rows: Agent POIs K76, K89, K90. Remove. Replacements: `https://bytebin.lucko.me` — HTTP 200, title "bytebin.lucko.me"; `https://bytebin.rkslot.nl` — HTTP 200, title "bytebin". ✓

### 38. `.../tree/main/scripts/cron/sites/bytebin_lucko_me.py`
- Rows: Agent POIs K76, K89. Remove. Same as 37 (bytebin.lucko.me). ✓

### 39. `.../tree/main/scripts/cron/sites/bytebin_rkslot_nl.py`
- Rows: Agent POIs K76, K90. Remove. Same as 37 (bytebin.rkslot.nl). ✓

### 40. `.../tree/main/data/lanes/2026-10-11-hf-traj-hermes/`
- Rows: Agent POIs K91. Remove. Replacement: `https://hermes-agent.nousresearch.com` — HTTP 200, title "Hermes Agent — Open-Source AI Agent That Grows With You | Nous Research". ✓

### 41. `.../tree/main/data/lanes/2026-09-28-yourls-resweep/`
- Rows: Agent POIs K96. Remove. Replacement: `https://yourls.org` — HTTP 200, title "YOURLS". ✓

### 42. `.../tree/main/data/lanes/2026-06-17-reverse-tunnels/`
- Rows: Agent POIs K97 ("Tunnels and network proxies (no specific URL established)"). Remove. **FLAG — direct source unavailable**: the row has no specific surface URL (its own label says none established); only our repo evidence exists. No URL invented. Cell becomes "unattributed — no specific URL established".

### 43. `.../tree/main/reports/chinese-agent-fleet-findings-2026-10-14.md`
- Rows: Agent POIs K98 ("Cloud-provider egress (no specific URL established)"). Remove. **FLAG — direct source unavailable**: no specific surface URL; own report + repo lane are the only sources. No URL invented.

### 44. `.../tree/main/docs/notes/gem-hunt-openai-incident-2026-09-27.md`
- Rows: Intelligence E5, E8. Remove. Direct sources stay and are verified:
  - `https://openai.com/hugging-face-incident-and-misalignment/` — 200, title "The Hugging Face incident and other third-party impact from misaligned models | OpenAI" ✓
  - `https://cdn.openai.com/pdf/67869394-cb91-4c12-888c-5cbd85c7814c/OpenAI-Hugging-Face%20Incident-Technical-Report.pdf` — 200, 521KB PDF ✓
  - `https://huggingface.co/blog/security-incident-july-2026` — 200, title "Security incident disclosure — July 2026" ✓
  - `https://openai.com/index/hugging-face-incident-and-the-road-ahead/` — 200, title "The Hugging Face incident and the road ahead | OpenAI" ✓
  - `https://rubyhack.ai/` — 200, title "OpenAI agents carried out an undisclosed cyber-attack on RubyGems" ✓
  - `https://blog.rubygems.org/2026/09/11/update-may-spam-publishing-campaign.html` — 200, title "An update on the May spam-publishing campaign on rubygems.org" ✓

### 45. `.../tree/main/scripts/scanners/crtsh.py`
- Rows: Intelligence E13. Remove. Replacement: `https://crt.sh` — HTTP 200, title "crt.sh | Certificate Search". ✓

### 46. `.../tree/main/scripts/scanners/shodan.py`
- Rows: Intelligence E14. Remove. Replacement: `https://shodan.io` — HTTP 200, title "Shodan Search Engine". ✓

### 47. `.../tree/main/scripts/scanners/iocfeeds.py`
- Rows: Intelligence E17. Remove. Replacement: `https://otx.alienvault.com` — HTTP 200, title "LevelBlue - Open Threat Exchange". ✓

### 48. `.../tree/main/scripts/cron/sites/urlhaus.py`
- Rows: Intelligence E18. Remove. Replacement: `https://urlhaus.abuse.ch` — HTTP 200, title "URLhaus | Malware URL exchange". ✓

### 49. `.../tree/main/scripts/cron/sites/threatfox.py`
- Rows: Intelligence E19. Remove. Replacement: `https://threatfox.abuse.ch` — HTTP 200, title "ThreatFox | Share Indicators Of Compromise (IOCs)". ✓

### 50. `.../tree/main/scripts/cron/sites/hermes_agent_nousresearch_com.py`
- Rows: Intelligence E20. Remove. Replacement: `https://hermes-agent.nousresearch.com` — HTTP 200, verified above (section 40). ✓

### 51. `.../tree/main/data/lanes/cairn-panels/`
- Rows: Intelligence E23, E24, E25, E26 (malicious Cairn panels). Remove. Surface URLs `http://185.242.245.159:8000`, `http://31.56.206.187:8000`, `http://31.57.47.29:8000`, `http://31.59.92.155:8000` — **FLAG — direct source currently unreachable**: empty reply from server (curl 52) on all four, consistent across attempts. No alternative home exists; the IP:port IS the surface. Keep the panel URLs with "unreachable 2026-10-23" note — do not replace or invent.

---

## Third-party GitHub — KEEP (not self-referential, direct sources)

### 52. `https://github.com` (Agent POIs K60, row label "github.com")
- Surface itself: GitHub IS the monitorable surface (skill-eval repo corpus, token-exposure cases). Third-party, not ours. MAY STAY — no substitution needed.

### 53. `https://gist.github.com` (Agent POIs K61, row label "gist.github.com")
- Surface itself. Third-party. MAY STAY.

### 54. Evidence note in Agent POIs L60
- "Transluce #137: ... skill-eval repo (github.com/youdotcom-oss/minimax-m3-deepsearchqa-skill-eval); Transluce #174: WildClawBench agents tried pushing leaked API keys/passwords to GitHub" — third-party repo, third-party evidence. MAY STAY per rule.

---

## Other self-referential material in visible sheets (same rule)

### A. Internal evidence paths in Direct Links cells (non-GitHub)
- Agent POIs K19–K26: cells read `https://<surface>; data/lanes/general-hunt/raw/0/<timestamp>/`. Strip the `data/lanes/...` path; keep the surface URL. All eight surfaces live-verified 200 with agent-board content confirmed:
  - `https://swarmsay.com` — "swarmsay — the message board and post office for AI agents" ✓
  - `https://commons.dooza.ai` — "Agent Commons — the agent coordination layer" ✓
  - `https://robots.wiki` — "robots.wiki — where AI agents read, write, and talk" ✓
  - `https://agenthaven.org` — "agent haven" ✓
  - `https://agentcolony.one` — "Agent Colony 聚落 · 纯 AI Agent 社区" ✓
  - `https://agent-message-board.kyle-hatcher.workers.dev` — "Agent Message Board — a message board for AI agents" ✓
  - `https://smokesignal-arianaram.pythonanywhere.com` — body: plain-text guestbook for non-human visitors, POST /guestbook, no auth ✓
  - `https://msgboard.dev` — body: "msgboard.dev - a message board for AI agents... One HTTP request does everything" ✓

### B. Internal paths in Intelligence sheet Source cells
- E9 (`data/lanes/2026-10-21-anthropic-cyber-incidents-assessment/`): remove; keep `https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents` — 200, title "An alignment assessment of recent cybersecurity incidents | Anthropic" ✓
- E27 (`data/lanes/anthropic-intel/raw/alignment-assessment-ukaisi_2026-10-23.EXTRACTION.md`): remove; keep `https://www.anthropic.com/research/alignment-assessment-ukaisi` — 200, title "An alignment assessment of the UK AISI cybertesting incident | Anthropic" ✓
- E28 (`data/lanes/metre-thread/mined-items.md`): remove; keep `https://metr.org/blog/2026-10-22-red-teaming-openai-agent-monitoring/` — 200, title "Red-Teaming OpenAI's Internal Agent Monitoring Systems - METR" ✓
- E7 (`data/lanes/wikidata-triage/FINDINGS.md`): **FLAG — direct source unavailable**. This is the entire cell content — an internal wiki-investigation dataset with no public home. No URL invented.

### C. Factum batch IDs in visible cells
- Agent POIs J19, L19, J21, L21, J22, L22, J23, L23, J24, L24, J25, L25, J26, L26 — all carry "Factum batch d6982046 (PRIMARY)". Self-referential IDs: strip the ID from visible cells (e.g. "Hourly slot-0, 2026-10-21 | Watch: slot-0 baseline"). No replacement exists or is needed; this is internal provenance.

### D. Third-party evidence that stays
- urlquery report UUIDs (K4), CloudFront findings links `d3ncjnql1bmhe8.cloudfront.net/findings/*` (K4, K5, K7, K39, K43, K47, K49, K60, K67, K70, K96, K81), webhook.site inbox UUID in K81 (`https://webhook.site/28efa24e-f830-4d9f-a12b-fbb9e5035031`), OpenAI/HF/RubyGems/Anthropic/METR URLs — all third-party, unaffected by the rule.

---

## Remaining verified-surface inventory (for v3 cell writes)

All 200-verified with content confirmation: urlquery.net, urlscan.io, any.run, r.jina.ai, s.jina.ai, commonlog.ai, jotspot.io, nervesocket.com, public-board.com, openagentforum.com, 1f916.ai, agentchan.org, universalagentforum.com, rentahuman.ai, bookofbots.com, openwitness.net, openagentchat.net, agent-board.juleskreuer.eu, botbook.space, signpost.public-agents.ai, messages.directory, pursekeeper.dev, anna.fyi, paste.linuxiarz.pl, pastebin.k4be.pl, pastebin.tarcseh.me, paste.rs, nicepaste.com, paste.ubuntu.org.cn, pastebox.to, infinitypaste.club, gritpost.com, gotit.pub, mcbin.dev, bytebin.lucko.me, bytebin.rkslot.nl, paste.ee, webhook.site, swarmsay.com, commons.dooza.ai, robots.wiki, agenthaven.org, agentcolony.one, agent-message-board.kyle-hatcher.workers.dev, smokesignal-arianaram.pythonanywhere.com, msgboard.dev, hermes-agent.nousresearch.com, yourls.org, openai.com incident page + PDF, huggingface.co blog, openai.com road-ahead, rubyhack.ai, blog.rubygems.org post, crt.sh, shodan.io, web.archive.org, otx.alienvault.com, urlhaus.abuse.ch, threatfox.abuse.ch, anthropic.com cybersecurity-incidents, anthropic.com ukaisi, metr.org red-teaming post. Third-party repos (github.com, gist.github.com) unchanged.

---

## COUNTS

- **replaced-verified:** 50 rows had every self-referential source removed and replaced with a live-verified direct URL (41 Agent-POI rows: 4–8, 38–44, 46–50, 52–56, 66–74, 76–77, 81, 86–91, 96; 9 Intelligence rows: 5, 8, 13, 14, 15, 17, 18, 19, 20). 120 silent-locus GitHub URL instances removed across these plus the flagged rows below.
- **flagged-unavailable:** 7 surfaces/rows — agents-relay.com (row 45, server empty reply), agent-community.com (row 51, HTTP 500), porkpad.com (row 84, server empty reply), row 97 (reverse tunnels, no URL established), row 98 (cloud egress, no URL established), Intelligence row 7 (internal wiki dataset, no public home), Cairn panels rows 23–26 (4 malicious panels, IP:port unreachable from VM on 2026-10-23 — keep URLs with unreachable note, do not invent alternatives).
- **flagged-canonical-home:** 2 rows — github.com (row 60), gist.github.com (row 61): GitHub is the surface itself, third-party, may stay. Plus third-party repo evidence in L60 may stay.
- **caveat (not dead, unverifiable by curl):** pasteview.com (rows 75, 85) — Cloudflare 403 on automated GET; URL kept as live surface home with bot-gate note.
- **internal provenance stripped:** 14 cells with Factum batch d6982046 (J19/L19, J21/L21, J22/L22, J23/L23, J24/L24, J25/L25, J26/L26).
