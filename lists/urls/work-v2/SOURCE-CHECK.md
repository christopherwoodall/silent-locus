# SOURCE-CHECK — monitorable-surfaces-ENRICHED-v2.xlsx link verification

Checked 2026-10-23 ~12:00–13:30 America/Chicago. Method: every URL token in Agent POIs cols J (Sources), K (Direct Links) and Intelligence col E (Direct source links), plus `data/lanes/...` / `lists/...` repo-path tokens. Split on whitespace/semicolons/commas. Live check = curl HEAD then GET fallback, Mozilla UA, ≤2 req/s, 20s timeout, via egress proxy, no auth, no POST. VERIFIED = shape OK and the link opened to an HTTP 200 landing page (canonical redirects followed and noted). A login wall counts as dead for "link opens".

## Counts (per link occurrence, 337 records)

| Verdict | Records | Unique URLs |
|---|---|---|
| VERIFIED | 258 | 179 |
| SHAPE-OK-BUT-DEAD | 67 | 55 |
| SHAPE-BAD | 0 | 0 |
| UNCHECKABLE | 12 | 10 |

## Shape check results

- URL parse (scheme + netloc): all 231 unique URLs parse.
- UUID format: 4 UUIDs cited (urlquery report IDs ×2, OpenAI CDN PDF asset, webhook.site token) — all valid UUID format.
- Transluce finding IDs: 34 unique IDs cited via `d3ncjnql1bmhe8.cloudfront.net/findings/<id>` — all 34 present in `data/lanes/2026-10-09-transluce-intel/raw/finding-<id>_*.json` cache. (IDs exist in the cache even though the live finding pages sit behind a login wall — see dead table.)
- Local repo paths: all 12 `data/lanes/...` tokens exist on disk under `~/workspace/silent-locus/`.
- GitHub paths: all 51 `github.com/christopherwoodall/silent-locus/...` paths are our repo and all exist on local disk.
- SHAPE-BAD: **0** — no malformed URLs, fake UUIDs, nonexistent finding IDs, or missing paths.

## SHAPE-OK-BUT-DEAD (55 unique URLs, 67 occurrences)

| URL | Reason | Cited at |
|---|---|---|
| `http://185.242.245.159:8000` | HEAD 000 (curl exit 52) — empty reply from server | Intel r23(direct) |
| `http://31.56.206.187:8000` | HEAD 000 (curl exit 52) — empty reply from server | Intel r24(direct) |
| `http://31.57.47.29:8000` | HEAD 000 (curl exit 52) — empty reply from server | Intel r25(direct) |
| `http://31.59.92.155:8000` | HEAD 000 (curl exit 52) — empty reply from server | Intel r26(direct) |
| `https://agent-community.com` | HEAD 500 / GET 500 | AgentPOIs r51(direct) |
| `https://agentcolony.one` | HEAD 000 (curl exit 52) — empty reply from server | AgentPOIs r23(direct) |
| `https://agentgateway.pythonanywhere.com` | HEAD 404 / GET 404 | AgentPOIs r30(direct) |
| `https://agents-relay.com` | HEAD 000 (curl exit 52) — empty reply from server | AgentPOIs r45(direct) |
| `https://agentsspeakup.com/api/mcp` | HEAD 405 / GET 405 | AgentPOIs r103(direct) |
| `https://blogsflow.liftbrandfulfillment.com` | HEAD 307 / GET 307 → login wall (chain→https://blogsflow.liftbrandfulfillment.com/login [final 200]) | AgentPOIs r13(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings` | HEAD 404 / GET 404 | Intel r4(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/107` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r10(direct), AgentPOIs r64(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/110` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r4(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/114` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r57(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/115` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r5(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/129` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r11(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/131` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r70(direct), AgentPOIs r95(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/136` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r11(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/137` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r60(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/138` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r59(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/147` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r96(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/152` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r4(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/153` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r4(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/157` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r4(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/166` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r47(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/167` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r47(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/170` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r7(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/171` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r34(direct), AgentPOIs r81(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/174` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r59(direct), AgentPOIs r60(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/176` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r18(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/179` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r43(direct), AgentPOIs r47(direct), AgentPOIs r49(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/182` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r4(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/186` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r15(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/188` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r47(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/190` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r59(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/195` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r78(direct), AgentPOIs r92(direct), AgentPOIs r95(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/37` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r39(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/38` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r83(direct), AgentPOIs r9(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/41` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r16(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/42` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r14(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/61` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r93(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/63` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r18(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/74` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r65(direct), AgentPOIs r99(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/75` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r93(direct) |
| `https://d3ncjnql1bmhe8.cloudfront.net/findings/78` | HEAD 405 / GET 303 → login wall (chain→https://d3ncjnql1bmhe8.cloudfront.net/login [final 200]) | AgentPOIs r67(direct) |
| `https://friendpaste.com` | HEAD 503 / GET 503 | AgentPOIs r93(direct) |
| `https://friendpaste.com/qm6K3qnDsZF0nB8fkptHB` | HEAD 503 / GET 503 | AgentPOIs r93(direct) |
| `https://joinsnail.com/mcp` | HEAD 405 / GET 405 | AgentPOIs r102(direct) |
| `https://messageboardforaiagents.com` | HEAD 000 (curl exit 28) — timeout (20s) | AgentPOIs r33(direct) |
| `https://openagentchat.net` | HEAD 000 (curl exit 52) — empty reply from server | AgentPOIs r50(direct) |
| `https://openai.com/index/our-framework-for-reporting-model-misalignment/` | HEAD 404 / GET 404 | Intel r6(direct) |
| `https://paste.ubuntu.com` | HEAD 000 (curl exit 52) — empty reply from server | AgentPOIs r78(direct) |
| `https://pasteview.com` | HEAD 403 / GET 403 | AgentPOIs r75(direct), AgentPOIs r85(direct) |
| `https://porkpad.com` | HEAD 000 (curl exit 52) — empty reply from server | AgentPOIs r75(direct), AgentPOIs r84(direct) |
| `https://webhook.site/28efa24e-f830-4d9f-a12b-fbb9e5035031` | HEAD 404 / GET 404 | AgentPOIs r81(direct) |

## UNCHECKABLE (10 unique URLs, 12 occurrences)

| URL | Reason | Cited at |
|---|---|---|
| `https://github.com/christopherwoodall/silent-locus/tree/main/docs/notes/gem-hunt-openai-incident-2026-09-27.md` | HEAD 301 / GET 301 → GitHub rate-limited this egress IP (429); path confirmed on local disk | Intel r5(direct), Intel r8(direct) |
| `https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/hermes_agent_nousresearch_com.py` | HEAD 301 / GET 301 → GitHub rate-limited this egress IP (429); path confirmed on local disk | Intel r20(direct) |
| `https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/infinitypaste_club.py` | HEAD 301 / GET 301 → GitHub rate-limited this egress IP (429); path confirmed on local disk | AgentPOIs r74(direct) |
| `https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/nicepaste_com.py` | HEAD 301 / GET 301 → GitHub rate-limited this egress IP (429); path confirmed on local disk | AgentPOIs r71(direct) |
| `https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/paste_rs.py` | HEAD 301 / GET 301 → GitHub rate-limited this egress IP (429); path confirmed on local disk | AgentPOIs r70(direct) |
| `https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/pasteview_com.py` | HEAD 301 / GET 301 → GitHub rate-limited this egress IP (429); path confirmed on local disk | AgentPOIs r75(direct), AgentPOIs r85(direct) |
| `https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/threatfox.py` | HEAD 301 / GET 301 → GitHub rate-limited this egress IP (429); path confirmed on local disk | Intel r19(direct) |
| `https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/urlhaus.py` | HEAD 301 / GET 301 → GitHub rate-limited this egress IP (429); path confirmed on local disk | Intel r18(direct) |
| `https://github.com/christopherwoodall/silent-locus/tree/main/scripts/scanners/iocfeeds.py` | HEAD 301 / GET 301 → GitHub rate-limited this egress IP (429); path confirmed on local disk | Intel r17(direct) |
| `https://github.com/christopherwoodall/silent-locus/tree/main/scripts/scanners/shodan.py` | HEAD 301 / GET 301 → GitHub rate-limited this egress IP (429); path confirmed on local disk | Intel r14(direct) |

## Notes

- `https://web.archive.org` returned HEAD 200 from this VM this run (TOOLS.md notes archive.org :443 is usually egress-blocked — it was reachable this time).
- GitHub `tree/main/<file>` URLs 301-redirect to the canonical `blob/main/<file>` URL; recorded as VERIFIED when the blob page landed 200.
- `https://r.jina.ai` / `https://s.jina.ai`: HEAD timed out but GET returned 200 — VERIFIED via GET.
- `https://agent-board.juleskreuer.eu` lands on `entry.php?next=index.php` (HTTP 200, page titled "Agent only · Agent Board", ~2KB, no password field) — VERIFIED as a 200 landing, gate page noted.
- `https://gateway.artifactcouncil.com/v2/artifacts` and `https://markdown.new`: HEAD 404 but GET 200 (HEAD unsupported) — VERIFIED via GET.
- `https://agentsspeakup.com/api/mcp`, `https://joinsnail.com/mcp`: 405 on both HEAD and GET (method not allowed) — dead as cited links.
