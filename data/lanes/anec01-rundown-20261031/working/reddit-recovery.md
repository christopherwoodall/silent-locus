# Reddit recovery — ANEC-01 (working, durable)
Account name as published in the article: u/Far-Gene-5806
Source article (prior capture): data/lanes/sniffer-sweep-20261031/raw/reddit/devto-busel-agents-reddit-ban-oct2026.html
Article claims (REPORTED, not OBSERVED): created Oct 9 2026; Oct 10: 3 karma, suspended once then reinstated; Oct 11 06:49 ET crossed 100 karma; that evening 154 karma; best: question post in r/rust about parallel coding agents hit #3 on Best within 13 min; comment in r/singularity hit 24 points; ~6 PM Oct 11 a moderator in r/programming removed one comment as "AI-generated content" and banned account from that sub; shortly after site-wide filter removed every post; ~6:40 PM ET Oct 11 banned site-wide.
Method: passive GET only. No login, no POST, no credentials, no bypass. 403/block recorded, not routed around.
Status: in progress 2026-10-31.

## Per-route outcomes (2026-10-31, passive GET only)
| Route | Result | Evidence |
|---|---|---|
| Direct www.reddit.com user page | 200 but JS bot-challenge shell only, no profile bytes | raw/reddit/www-reddit-user-Far-Gene-5806.html |
| Direct .json and api.reddit.com about | 403 network-security block page | raw/reddit/www-reddit-user-Far-Gene-5806.json.html |
| old.reddit.com user/submitted/comments | 302 to login, 0-byte body | raw/reddit/old-reddit-user-Far-Gene-5806.html |
| r.jina.ai reader, user/submitted/comments | Reader 200, but reports upstream 403 for all three | raw/reddit/jina-reddit-user-Far-Gene-5806*.txt |
| Wayback CDX, reddit.com + old.reddit.com user prefix, Oct 9-31 | 200, empty result, both status-filtered and unfiltered | raw/reddit/wayback-cdx-user-Far-Gene-5806*.json, wayback-cdx-old-user-Far-Gene-5806.json |
| Wayback CDX, www.reddit.com user prefix | 503 Temporarily Offline, then connection failure on retry; NOT established either way | raw/reddit/wayback-cdx-www-user-Far-Gene-5806.json |
| Wayback direct snapshot 20261011 user page | 404 no-capture page | raw/reddit/wayback-user-Far-Gene-5806-20261011.html |
| Redlib mirror (privacyredirect) user + submitted | 200 bot-check page only, no profile content; challenge not attempted | raw/reddit/mirror-redlib-privacyredirect*.html |
| teddit.net, snew.notabug.io | Connection failure, no data | (no file) |
| PullPush archive, submissions | 403 Cloudflare challenge page; comments retry connection failure | raw/reddit/pullpush-submissions-Far-Gene-5806.json |
| Arctic Shift search endpoint tried | 404 app shell, wrong endpoint path; not a usable archive query | (file discarded, outcome recorded here) |
| Web search, account name | No hits for the account outside the article series; unrelated numeric matches only | search 2026-10-31 |
| Web search, distinctive phrases | Only the article series itself; no independent post text found | search 2026-10-31 |
| Hacker News / press / blog coverage | No coverage of this account found; HN hits are generic Reddit-ban discussion only | search 2026-10-31 |
| Same-series follow-up chapter | REPORTED (not OBSERVED): banned then unbanned, back by 3 AM, karma 285 at 9:23 PM Oct 13, hit #3 on r/rust | raw/reddit/devto-followup-4day-reddit-unbanned.html |

## Verdict
Native Reddit bytes recovered: NONE. No post title, post ID, comment text, karma figure, or ban/suspension status was observed first-hand. All Reddit figures remain REPORTED from the article series only.
New REPORTED wrinkle from the follow-up chapter: the Oct 11 site-wide ban is claimed to have lifted by ~3 AM with no appeal, and karma is claimed at 285 on Oct 13. This contradicts a simple "permanently banned" reading of Chapter 1 and is the key claim a live read must test.
No login, POST, session, or credentialed bypass was used. No Factum writes. Nothing committed.

## Verifier addendum (2026-10-31, appended by coordinator, lane text untouched)

- Wayback CDX retry, port 80: www.reddit.com user prefix returned HTTP 200 with an empty result body `[]`; reddit.com prefix returned HTTP 504 on first attempt, then HTTP 200 with `[]` on retry after ~60 s. The www-prefix check is therefore closed as empty on retry. The lane's stored 503 outcome stands as a recorded attempt, not a result.
