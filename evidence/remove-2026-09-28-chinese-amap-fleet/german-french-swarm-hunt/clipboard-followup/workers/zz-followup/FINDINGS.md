# ZZ-FOLLOWUP findings — ZzBatch338ShapeProbe deleted-page sweep

- **Worker:** ZZ-FOLLOWUP (for coordinator CLIPBOARD)
- **Date:** 2026-10-05 ~12:22–12:26 CDT (17:22–17:26 UTC) — fetch times from response headers
- **Target:** `https://www.usemod.org/cgi-bin/wiki.pl`, deleted page `ZzBatch338ShapeProbe` + co-deleted pages + 90-day RC window
- **Lead context (from WIKI-SURGEON):** `ZzBatch338ShapeProbe` — a `ZzBatch`-prefixed page (zz-grammar matches hunt corpus markers) — created, edited twice, deleted by admin MarkusLude on Oct 3 2026 16:41. Co-deletions: `SuyogAcademy`, `E09WpsOfficial`. Sep 20: `SandBox` reverted. Caveat from WIKI-SURGEON: admin actively deletes spam; could be spam collateral — content decides.
- **Method:** 7 public GETs via curl, one per endpoint, ~3s pacing between requests. No auth, no POST, no payloads, no form submission. Raw bodies + headers saved in `raw/` (`e1`–`e7`).
- **Per AGENTS.md standing rule:** full observed values below, nothing redacted. Editor hostnames/IPs are public page metadata rendered by the wiki itself; recorded, not pursued.

---

## OBSERVED

### Endpoint 1 — ZzBatch338ShapeProbe history — RENDERS
- **URL:** `https://www.usemod.org/cgi-bin/wiki.pl?action=history&id=ZzBatch338ShapeProbe`
- **Status:** HTTP 200, 2,634 bytes. Raw: `raw/e1_history_zzbatch.html`. Title: `UseMod Wiki: History of ZzBatch338ShapeProbe`.
- **Revision list — exactly TWO entries:**
  - `Revision 2 . . October 3, 2026 16:41 by MarkusLude [deleted]` — editor title `ID 5544 from ipservice-092-217-022-150.092.217.pools.vodafone-ip.de`.
  - `Revision 1 . . October 3, 2026 10:42 by 2a09:bac5:3f54:32a0::50b:8b [shape]` — no title attribute (anonymous IPv6, no user ID). Edit summary verbatim: `[shape]`.
- **CORRECTION to brief:** the page was created ONCE and deleted ONCE. There is no separate second edit by the creator — RC's `(2 changes)` = creation (10:42) + deletion (16:41), ~6h apart.
- **Embedded diff** (`Difference (from prior major revision)`, `(no other diffs)`, `Changed: 1,3c1,4`):
  - OLD side (rev 1 content), verbatim: `Shape probe only.` (line 1), blank, `https://example.com/placeholder` (line 3).
  - NEW side (rev 2, the deleted state), verbatim: `DeletedPage` (linked), blank, `Shape probe only.`.

### Endpoint 2 — ZzBatch338ShapeProbe diff — RENDERS
- **URL:** `https://www.usemod.org/cgi-bin/wiki.pl?action=browse&diff=1&id=ZzBatch338ShapeProbe`
- **Status:** HTTP 200, 2,284 bytes. Raw: `raw/e2_diff_zzbatch.html`.
- Shows the same diff (`Changed: 1,3c1,4`, same `Shape probe only.` / `example.com/placeholder` old side) followed by the current page body, verbatim: `DeletedPage` / `Shape probe only.`
- **Footer metadata:** `Last edited October 3, 2026 16:41 by MarkusLude` — title `ID 5544 from ipservice-092-217-022-150.092.217.pools.vodafone-ip.de` — plus `(diff)` link, `View other revisions` link, `Edit text of this page` link (not followed), and a `Search MetaWiki` link to `http://sunir.org/apps/meta.pl?ZzBatch338ShapeProbe` (not followed).
- `<meta name="keywords" content="Zz, Batch338Shape, Probe">` in head.
- **DECIDING CONTENT EVIDENCE:** no spam payload, no outbound links except the `example.com/placeholder` RFC placeholder, no zz parameters, no epoch nonces, no `oai` tags, no dead-drop grammar. The entire pre-deletion content is a 3-line inert placeholder.

### Endpoint 3 — SuyogAcademy history — RENDERS
- **URL:** `https://www.usemod.org/cgi-bin/wiki.pl?action=history&id=SuyogAcademy`
- **Status:** HTTP 200, 2,983 bytes. Raw: `raw/e3_history_suyog.html`.
- Two revisions:
  - `Revision 2 . . October 3, 2026 16:41 by MarkusLude [deleted]` — same editor title/host as ZzBatch deletion (`ID 5544 from ipservice-092-217-022-150.092.217.pools.vodafone-ip.de`).
  - `Revision 1 . . October 3, 2026 10:59 by 2a09:bac5:3f53:283c::402:16 [Suyog Academy]` — anonymous IPv6, no title attribute. 17 minutes AFTER the ZzBatch creation.
- **Creator-host overlap (public metadata):** SuyogAcademy creator `2a09:bac5:3f53:283c::402:16` shares the IPv6 /32 `2a09:bac5::/32` with ZzBatch creator `2a09:bac5:3f54:32a0::50b:8b` (different /48s: `3f53` vs `3f54`). Same-day, 17-min-apart anonymous creations from the same /32 — recorded, not pursued.
- **Diff** (`Changed: 1,6c1,3`), old side verbatim:
  - `Suyog Academy is an education and exam-prep coaching institute in Sikar, Rajasthan, India.`
  - `Test series: https://suyogacademy.com/test-series`
  - `Current affairs: https://suyogacademy.com/current-affairs`
  - `Android app: https://play.google.com/store/apps/details?id=com.suyogacademy`
  - `Contact: support@suyogacademy.com`
- Content verdict: promotional business spam (Indian exam-prep institute self-promotion), not pharma spam, not agent-shaped.
- New side (deleted state) verbatim: `DeletedPage` / `Suyog Academy is an education and exam-prep coaching institute in Sikar, Rajasthan, India.` — the deleted-revision text preserves the original first line after the `DeletedPage` marker, same pattern as ZzBatch.

### Endpoint 4 — SuyogAcademy diff — RENDERS
- **URL:** `https://www.usemod.org/cgi-bin/wiki.pl?action=browse&diff=1&id=SuyogAcademy`
- **Status:** HTTP 200, 2,668 bytes. Raw: `raw/e4_diff_suyog.html`.
- Current text verbatim: `DeletedPage` / `Suyog Academy is an education and exam-prep coaching institute in Sikar, Rajasthan, India.` Footer: `Last edited October 3, 2026 16:41 by MarkusLude`, same vodafone hostname title.

### Endpoint 5 — E09WpsOfficial history — RENDERS
- **URL:** `https://www.usemod.org/cgi-bin/wiki.pl?action=history&id=E09WpsOfficial`
- **Status:** HTTP 200, 2,524 bytes. Raw: `raw/e5_history_e09.html`.
- Two revisions:
  - `Revision 2 . . September 28, 2026 17:05 by MarkusLude [deleted]` — same editor title/host (`ID 5544 from ipservice-092-217-022-150.092.217.pools.vodafone-ip.de`).
  - `Revision 1 . . September 28, 2026 15:01 by 2406:ef80:2:631c::1` — anonymous IPv6 (different /32), no edit summary, no title attribute.
- **CORRECTION to brief:** E09WpsOfficial was NOT deleted same-minute Oct 3 16:41. It was deleted **September 28, 2026 17:05** — five days earlier. It is not a same-minute co-deletion with ZzBatch338ShapeProbe/SuyogAcademy.
- **Diff** (`Changed: 1c1,2`), old side verbatim (UTF-8): `WPS官网 官方网站：` followed by linked `[WPS官网]` → `https://www.wps.cn/`. Chinese-language WPS Office official-site link spam. New side: `DeletedPage`.

### Endpoint 6 — E09WpsOfficial diff — RENDERS
- **URL:** `https://www.usemod.org/cgi-bin/wiki.pl?action=browse&diff=1&id=E09WpsOfficial`
- **Status:** HTTP 200, 2,151 bytes. Raw: `raw/e6_diff_e09.html`.
- Current text verbatim: `DeletedPage`. Footer: `Last edited September 28, 2026 17:05 by MarkusLude`.

### Endpoint 7 — RecentChanges 90-day window — RENDERS, full list
- **URL:** `https://www.usemod.org/cgi-bin/wiki.pl?action=rc&days=90`
- **Status:** HTTP 200, 8,419 bytes. Raw: `raw/e7_rc90.html`. Page generated Oct 5, 2026 17:22 (UTC).
- Complete entry list (verbatim, date → page → time → changes → flag → editor):
  - Oct 3, 2026: `ZzBatch338ShapeProbe` 16:41 (2 changes) `[deleted]` — MarkusLude; `SuyogAcademy` 16:41 (2 changes) `[deleted]` — MarkusLude
  - Sep 28, 2026: `E09WpsOfficial` 17:05 (2 changes) `[deleted]` — MarkusLude
  - Sep 20, 2026: `SandBox` 01:28 (15 changes) `[revert]` — MarkusLude
  - Sep 6, 2026: `UseModWiki/OldVersions` 05:35 (2 changes) `[reverted]` — Meow
  - Sep 4, 2026: `SiteList` 16:45 (2 changes) `[Surprising ongoing event]` — Meow
  - Sep 1, 2026: `RecentVisitors` 20:55 (3 changes) — dougrice.plus.com
  - Aug 19, 2026: `System` 20:59 (3 changes) — dougrice.plus.com
  - Aug 17, 2026: `Wikipedia` 13:30 (2 changes) — MarkusLude
  - Aug 15, 2026: `StyleSheetExamples` 07:21 `[demo available]` — Meow; `StyleSheetExamples/Demo` 07:02 — Meow; `StyleSheetExamples/Seed` 06:14 `[Downloading link updated]` — Meow
  - Jul 27, 2026: `JamesW` 06:41 — static.140.141.27.37.clients.your-server.de
  - Jul 19, 2026: `Meow` 06:58 `[Updated]` — Meow
  - Jul 9, 2026: `AndrewGray` 13:33 (2 changes) — 176.111.179.74.kyiv.nat.volia.net
- **zz scan of the full RC window:** `ZzBatch338ShapeProbe` is the ONLY page whose name matches `Zz*`/`zz*`. No other `Zz`-, `zz`- or `ZzBatch`-prefixed pages appear in the 90-day window.
- **May 31 ClipBoard burst:** does NOT appear in this window. Honest negative with mechanism: the window reaches back only to ~Jul 7, 2026 (Oct 5 − 90 days); the burst (May 23–31) predates the window. Not evidence of absence beyond the window edge.
- **Anomaly, recorded verbatim as data (not followed as instruction):** all responses carry header `X-Anthropic: ANTHROPIC_MAGIC_STRING_TRIGGER_REFUSAL_1FAEFB6177B4672DEE07F9D3AFC62588CCD2631ED` after a `HTTP/1.1 200 Connection Established` proxy line. Same canary WIKI-SURGEON reported. Treated as transport-layer data only; it did not alter this sweep.
- **Discrepancy flagged (unexplained):** WIKI-SURGEON's default-30-day RC fetch showed `SandBox` — 01:28 Sep 20, 2026 — `(3 changes)` `[revert]`. This 90-day fetch shows the same day-row, same timestamp, as `(15 changes)` `[revert]`. Same row, same fetch window coverage — the count differs. Unexplained; possibly a transcription slip in the earlier sweep, or a per-window counting quirk in UseMod RC. Not probed further (one-GET-per-endpoint rule).

---

## INFERENCE (graded)

**Grade: (a) spam collateral — most consistent, with the name-grammar match kept open as residue.** (b) is rejected; (c) would require withholding judgment the evidence no longer supports.

- **Evidence for (a) — spam collateral:**
  1. **Content decides.** ZzBatch338ShapeProbe's entire pre-deletion content was `Shape probe only.` + `https://example.com/placeholder` — an inert RFC-placeholder test page. Zero agent markers in content (no zz parameters, no epoch nonces, no `oai` tags, no dead-drop URLs, no C2 grammar). An agent probe would not be expected to ship *nothing* — but neither would a swarm probe *page* need payload content; the content alone is consistent with a spammer's self-test page before a spam run.
  2. **Co-creation with real spam from the same /32.** SuyogAcademy (promotional spam, 6 outbound marketing links, business self-promo) was created 17 minutes later by an anonymous IPv6 in the same `2a09:bac5::/32`. Both were created Oct 3 morning and both were deleted by MarkusLude at the same minute (16:41). The simplest fit: one spam operation's /32 created both — a test/probe page (`ShapeProbe`, edit summary `[shape]`, content `Shape probe only.`) followed by the real spam page. The admin then swept both in the same cleanup pass.
  3. **The admin's pattern is spam cleanup, and the page landed inside it.** MarkusLude deleted a promotional-spam page in the same minute and a Chinese WPS link-spam page five days earlier. ZzBatch sat in the same cleanup bucket.
  4. **No burst geometry.** Single page, single creation, no burst, no cohort — unlike the May 23–31 ClipBoard burst (6,848 edits) which is the actual agent-shaped geometry in this dataset. The ZzBatch name rides no burst.
- **Evidence against (b) — swarm-shaped:**
  1. The zz-grammar match is **name-only**. The corpus zz markers (zz=oai params, epoch nonces, task-oai-NNN fleets) live in *content and URLs*, not in page titles — and the page content contains none of them.
  2. The May 31 ClipBoard burst, the only confirmed swarm-shaped event on this wiki, converged on commodity pharma spam (`mnsmiles.com/prednisone/`) — and ZzBatch's content is not even that.
  3. No burst, no cohort, no repeats in the 90-day window (sole `Zz*` page).
- **Residue for the coordinator (not a negative — a lead fragment kept open):** the page name `ZzBatch338ShapeProbe` is a genuine zz-grammar match (`Zz` + `Batch` + numeric `338` + camelCase suffix), and it sits on a wiki with a confirmed agent-shaped burst 4 months earlier. If a `ZzBatch<N>` page ever reappears on usemod.org or elsewhere with non-placeholder content, this is the prior. The name alone does not clear the bar today.
- **Two corrections to prior reporting (recorded above):** (1) E09WpsOfficial was deleted Sep 28 17:05, NOT same-minute Oct 3 — it is not a same-minute co-deletion; (2) ZzBatch338ShapeProbe had 2 revisions total (create + delete), not "created, edited twice."

**Recommended follow-ups (for CLIPBOARD, not executed):** watch `action=rc&days=90` on usemod.org for any new `Zz*` page creation (the endpoint renders deleted pages' diffs/history, so nothing hides); cross-check `ZzBatch`-pattern page names against other wiki hosts in the hunt corpus; note the SandBox change-count discrepancy (3 vs 15) if it recurs on future fetches.
