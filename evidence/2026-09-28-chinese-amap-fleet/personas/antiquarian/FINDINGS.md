# THE ANTIQUARIAN — FINDINGS

Persona: archive.org / Open Library / Project Gutenberg as agent surfaces — mass digitized-text pulls, systematic identifier enumeration, metadata-field payload stashes.

Run: 2026-10-05 ~06:00–06:45 UTC. Egress verified working (urlquery.net 200, archive.org 200, urlscan.io 200; transient proxy stalls on first attempts — retry works). No commits/pushes. Hunt AGENTS, not operators.

## Verdict

**One genuinely new agent-shaped find** (stealer-log `.txt` enumeration via urlscan, still active today), one machine-cadence SEO watcher (commercial, not our target), everything else honest negatives. Zero overlap with our corpora.

---

## FINDING 1 (GENUINELY NEW): systematic enumeration of stealer-log `.txt` files from taken-down archive.org collections

Someone is machine-enumerating numbered text files (`N-M.txt`) inside archive.org credential-dump ("Crypted"/"Redone") collections by submitting direct `us.archive.org` mirror URLs to urlscan.io. Activity is multi-day with burst cadence and continues **today**.

| Item | Scans | Filenames / times (UTC) |
|---|---|---|
| `120-Crypted-03-June` | 6 | `5-3.txt` 09-21 07:02, `2-2.txt` 09-21 08:04, item page 09-21 08:06, `15-1.txt` 09-21 08:07, `18-1.txt` 09-24 11:03, `1-1.txt` 10-05 05:25 |
| `87-Redone-June-9` | 3 | `23-3.txt` 09-21 08:06, `32-3.txt` 10-01 01:15, `30-2.txt` 10-05 05:23 |
| `defender_202103` | 1 | `defender.txt` 10-05 04:32 |
| `2_20210221_20210221_2235` | 1 | `1.txt` 09-21 08:06 |

Key observations:
- **All three named items are now 404 on archive.org** (verified live: `/details/120-Crypted-03-June` → 404, `/details/defender_202103` → 404; metadata API returns 0 files). These were stealer-log/password-dump collections that got taken down — yet the actor keeps pulling their files through the `us.archive.org` mirrors, which outlive takedowns briefly.
- **Oct 5 session: three items in 53 minutes** (04:32 → 05:23 → 05:25). **Sep 21 burst: four scans in 65 minutes** (07:02 → 08:07). Sequential `N-M.txt` filename enumeration across days = machine-driven, not human browsing.
- Submissions go through urlscan's API (`task.method: api`, public visibility) — the actor uses urlscan as a fetch/view proxy for the .txt files rather than (or in addition to) direct download.
- **Corpus check: zero hits** for `crypted`, `us.archive.org`, `redone` in all three sets (2,141 Amap / 589,972 openai-agent-traces / oai-tag-sweep). GENUINELY NEW — not ours, not previously recorded.
- Grading: agent-shaped file enumeration, HIGH confidence on the machine-cadence claim. Attribution open — could be a threat-intel researcher harvesting stealer logs, a credential-stuffer restocking, or an agent building a test corpus. The tradecraft (urlscan-as-fetch-proxy, mirror URLs past takedown) is the thing to watch, not the identity.

## FINDING 2 (context, not our target): machine-cadence SEO watcher on archive.org

urlquery htmx (`url.domain:archive.org`, 71 reports): six paired submissions Sep 17–21 of `archive.org/details/@ardigitaladstudio/` + `archive.org/details/how-local-businesses-can-build-visibility-generate-leads-and-grow-online`, each pair ~2 minutes apart, repeating daily. The item is an SEO agency (Pilibhit, India) lead-gen PDF uploaded 2026-09-07 for backlinks. This is commercial SEO rank-tracking automation scanning its own uploads — machine cadence but not agent-swarm activity. Filed as context.

## KNOWN (already in our sets)

- **cors-laundering-ops fetched a Ghostarchive WARC**: `allorigins.hexlet.app/raw?url=https://ghostarchive.org/chimurai4/EoAqe.warc` (urlquery report `8d2363b0`, 2026-05-13, tagged `cors-laundering` by our hunt). In oai-tag-sweep. Establishes the pattern: our tracked agents DO pull archived WARC content through laundering relays.
- **Collusion-wiki test pages** embed `web.archive.org/web/<timestamp>id_/` availability-check URLs (18+ hits in oai-tag-sweep) — known test-page tradecraft, not new.

## Honest negatives

- **Open Library**: 4 urlquery reports total (2024–2026), all ordinary profile/homepage browsing. No bulk pulls.
- **Project Gutenberg**: 19 urlquery reports, all ordinary single-file downloads (`/files/31431/31431.txt`, epub zips). No enumeration.
- **archive.org advancedsearch API**: 0 urlquery reports. No observed bulk-metadata harvesting via the public search API.
- **Metadata-field payload stash**: advancedsearch for `identifier:(webhook OR beacon OR httpbun)` → 2 hits, both benign ("Guilded Webhook Tester", "beacon"). No agent C2/beacon stashes found in identifiers. Recent-texts identifier scan (Oct 1–5, 50 items) → 1 machine-shaped identifier, false positive (CIA RDP document ID).
- **archive.org/metadata API**: 4 urlquery reports — EOT crawl items + one Shopify URL, researcher-shaped one-offs.

## Limitations

- urlscan anonymous API: no leading-wildcard/regex search, result-detail API requires login (403). Submitter IPs unattainable without an account — the Oct 5 session's single-actor claim rests on timing + filename grammar, not IP.
- urlscan search returns max 100/page with no documented offset; 244 total `us.archive.org` results exist, 100 reviewed. The enumeration may extend beyond what was sampled.
- urlquery htmx search misses known-live records (Polyglot warning) — zeros here are weak negatives.

## Open threads

1. Re-query `domain:us.archive.org` on urlscan in a few days — if the `N-M.txt` enumeration continues with new filenames, the actor is still working through the collections.
2. Watch for NEW "Crypted"/"Redone"-style identifiers appearing on archive.org — the actor's supply chain.
3. urlscan account (free) would unlock submitter IPs and confirm the single-actor hypothesis.

---

## Observed URLs (complete list)

### Stealer-log enumeration (Finding 1)
- https://ia801409.us.archive.org/26/items/120-Crypted-03-June/1-1.txt
- https://ia801409.us.archive.org/26/items/120-Crypted-03-June/5-3.txt
- https://ia801409.us.archive.org/26/items/120-Crypted-03-June/2-2.txt
- https://ia801409.us.archive.org/26/items/120-Crypted-03-June/15-1.txt
- https://ia801409.us.archive.org/26/items/120-Crypted-03-June/18-1.txt
- https://ia801503.us.archive.org/32/items/87-Redone-June-9/23-3.txt
- https://ia801503.us.archive.org/32/items/87-Redone-June-9/32-3.txt
- https://ia801503.us.archive.org/32/items/87-Redone-June-9/30-2.txt
- https://ia801408.us.archive.org/25/items/defender_202103/defender.txt
- https://archive.org/details/120-Crypted-03-June (404, verified 2026-10-05)
- https://archive.org/details/defender_202103 (404, verified 2026-10-05)
- https://urlscan.io/api/v1/search/?q=domain%3Aus.archive.org&size=100

### SEO watcher (Finding 2)
- https://urlquery.net/report/54da09d8-56c9-4537-b46d-a07d8d8d86ef
- https://urlquery.net/report/e0edb82a-59cd-4d74-8144-2f2c9e31ab15
- https://urlquery.net/report/fac32bb2-d899-4366-a2b1-fea363905c6c
- https://urlquery.net/report/7feace66-e52c-4428-9ff1-110791b58216
- https://urlquery.net/report/0a0e4312-70c5-43f9-a1ac-3e01eb91cbcf
- https://urlquery.net/report/c8e141cb-e2c6-49a1-9849-d44239dbffe7
- https://archive.org/details/@ardigitaladstudio/
- https://archive.org/details/how-local-businesses-can-build-visibility-generate-leads-and-grow-online
- https://archive.org/metadata/how-local-businesses-can-build-visibility-generate-leads-and-grow-online

### Known / context
- https://urlquery.net/report/8d2363b0-d388-4d80-ab77-8661add8d852
- https://ghostarchive.org/chimurai4/EoAqe.warc

### Searched / checked (no hit)
- https://urlscan.io/api/v1/search/?q=domain%3Aarchive.org&size=50
- https://archive.org/advancedsearch.php (identifier webhook/beacon/httpbun query; recent-texts identifier scan)
- https://archive.org/metadata/defender_202103
- https://archive.org/metadata/120-Crypted-03-June
- https://archive.org/metadata/87-Redone-June-9
- https://archive.org/details/@kamisato_ayaka200/web-archive (urlquery report e6668e6a-6aa0-4612-bb88-b5eddea843c5, user web-archive collection — ordinary)
