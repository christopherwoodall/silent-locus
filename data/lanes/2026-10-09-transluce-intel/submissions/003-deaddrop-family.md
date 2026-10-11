# Submission 003 — dead-drop family (live webhook.site inboxes)

- Status: Submitted (2026-10-07)
- Transluce ID: 171
- Evidence pack: `data/transluce-api/deaddrop-evidence-pack.zip`
- Full writeup: `data/transluce-api/submissions/003-deaddrop-family/README.md`

## Form content

### Short description
Live dead-drop family: 3 webhook.site inboxes exfiltrating Amap POI-scraping results via a COMBO-INIT state machine (boot/bxinit/xdcinit/capture/done). 100+ beacons, 3 POI targets, evolving exfil topology; a third party is interrogating the channel as "mailbox.termina.digital".

### Detailed description
We found a family of live webhook.site dead-drop inboxes receiving exfiltrated results from a coordinated Amap (Chinese map service) POI-scraping agent run. The first inbox was identified from a urlquery report; a grammar search for siblings found two more. All were live at filing time.

The beacons follow a scraper state machine: boot -> bxinit -> xdcinit/xdcerr -> capture xN -> error xN -> done. Each carries ua, href (an httpbin base64 COMBO-INIT carrier), and now (Date.now()); cache-busters look like live=N_<epoch_ms>.

Three Amap POI targets: B0138027SQ (new to our corpus), B0G3LMF2G1 (USTC hospital, Hefei — arrival-share stats for parking locations exfiltrated), B00190BBTX (Mochou Lake Park, Nanjing — full POI page captured, arrival shares: South Gate 43%, South Gate lot 23%, North Gate lot 20%, North Gate 13%).

Sibling urlquery reports show the exfil topology evolving: v3 used ntfy.sh + a urlquery robots.txt image-beacon; v5 added webhook.site (triple exfil); a "loader" report fuses jina-laundering (r.jina.ai) with Amap probing and httpbun echo.

Amap is fighting back: beacons capture its rate-limit rejection ("FAIL_SYS_USER_VALIDATE" + colloquial Chinese overload message) and slider CAPTCHAs. The operator exfiltrates the rejections rather than hiding them.

On 2026-10-07 at 19:44 UTC, a third party posted an identical Chinese message into both new inboxes from one IP, claiming to be "an agent of mailbox.termina.digital", presenting POI analysis and asking which benchmark the locations come from, who receives the answers, how they found the mailbox, and whether other agents share the task list. Whether agent or researcher is unresolved. Not us (GET-only access; posts predate our pulls).

Why it matters: the channel is marker-clean (zero oai/zz/epoch grammar in 100+ requests) — attribution lives in timing and topology. The topology is actively iterated and a third party is now interrogating it.

Uncertainties: operator identity not pursued (out of scope); benchmark behind the POI list unknown; beacon IPs are exit nodes, not operator location.

### Evidence links
https://urlquery.net/report/5008c990-1383-4adb-bff6-8efde3825306
https://urlquery.net/report/33fa9bd2-a2fe-4856-8147-1725430170ea
https://urlquery.net/report/0a541d23-7077-4a23-9a24-4809c65ea5b0

### Classifications
- Untapped source: Yes
- Cyberattack: Bypassing bot protection or access controls
- Government: No
- AI company: (unset — unattributed)

### Data zip
deaddrop-evidence-pack.zip: cache/ (fresh inbox pulls, pastes, urlquery reports), translation/TRANSLATIONS.md, README.md, urls.md
