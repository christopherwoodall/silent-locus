# Notes-farm verdict ledger (2026-09-29 worker)

Confidence tiers:
- READ: note read in full by this worker.
- RANK: ranked by size/table-count in the survey pass; verdict from filename + ranking, not a full read.

## IMPORTED (READ — 527 records total across 8 dirs)

| Note | Records | Target dir |
|---|---|---|
| gem-iocs-2026-09-27.md | 334 ioc_inventory_entry (305 URLs, 13 domains, 2 proxy-domains, 1 IP, 5 gem-packages, 6 hashes, 2 beacons) | data/2025-03-04-rubygems-goimport-campaign/ |
| gem-apikey-disclosure-2026-09-27.md | 26 finding (12 key-reuse clusters w/ redacted prefixes, 13 singletons, 1 corrected census 54v/25p) | same |
| gem-metadata-deepdive-2026-09-27.md | 25 (3 tally + 16 target clusters + 6 prefix-exception findings) | same |
| gem-harvest-final-2026-09-27.md | 37 (corpus stats, 28 family census, 7 fingerprint census, lib/ audit) | same |
| gem-timeline-expansion-2026-09-27.md | 5 run_shape (burst phases, publish lead, iteration) | same |
| gem-deaddrops-2026-09-27.md | 25 finding (beacon protocol, mission comments, ops logs, status flags, version signals, theater files) | same |
| gem-corpus-a000-webhook-search-2026-09-27.md | 7 webhook_deaddrop + 1 sweep_negative + 1 finding | data/2026-05-12-webhook-deaddrops/ |
| gem-hunt-osv-2026-09-27.md | 7 osv_advisory + 1 sweep_negative + 1 finding | data/2026-05-11-osv/ |
| gem-hunt-pattern-battery-2026-09-28.md | 8 finding + 1 sweep_negative | data/2026-09-28-librariesio-pattern-battery/ (new) |
| gem-hunt-depsdev/npm/pypi/pypibigquery/docpipelines/dockerhub/urlscan/commoncrawl/shodan/ghactions/gists/huggingface/gomodules/codesearch/abusech-historical/pastebins/rubydoc (17 notes) + api-usa-fbi-ucr-2026-09-28.md | 18 sweep_negative | data/2026-09-27-gem-negative-lanes/ (new) |
| gem-hunt-abusech-2026-09-27.md | 1 access_gap | same |
| gem-hunt-rubygemsapi-2026-09-27.md | 1 finding | same |
| analyst-note-ace-research-2026-09-28.md | 12 finding (3 CT certs, wildcard blind, DNS neg, Wayback neg, 6 artifact maps) | data/2026-09-28-ace-research-ct/ (new) |
| gem-public-intel-2026-09-27.md | 11 source_reference | data/2026-09-27-gem-public-intel/ (new) |
| verification-2026-09-27.md | 5 finding (corpus audit) | data/2026-09-27-swarmtraces-verification/ (new) |

## DEDUP-SKIP (READ — structured but already represented in data/)

| Note | Existing coverage |
|---|---|
| gem-hunt-diffend-sweep-2026-09-27.md | data/2026-05-11-osv: 718 diffend_harvest + 1,238 sweep_negative |
| july7-wave-sweep-2026-09-27.md | data/2026-07-07-july7-wave (264 diffend_probe) + data/2026-07-07-xss-ssti-census (122 payloads) |
| jsonhero-archive-recovery-2026-09-27.md | 6 artifact_observation events |
| gem-hunt-dse-wiki-verification-2026-09-27.md | 6 downloads + 4 corpus hits + 11 negatives |
| gem-hunt-wiki-ioc-pivots-2026-09-27.md | 334 wiki_ioc_pivot in gem dir |
| gem-jfrog-report-2026-09-27.md | JFrog inventory ingested (3,025 docs) |
| gem83-reconciliation-2026-09-27.md | data/aggregates/2026-09-28-gem83-reconciliation |
| overlap-negatives.md / overlap-plan.md | data/aggregates/2026-09-29-overlap-analysis |
| gem-june18-wave-2026-09-27.md | names ingested as Wayback metadata (flagged: verify before any addition) |
| webhook-deaddrops-2026-09-27.md | likely source of the 8 existing webhook-dir records (not fully verified — do not re-import) |

## NOTES-ONLY (READ — analysis/opinion/synthesis/process)

| Note | One-line reason |
|---|---|
| cascade-synthesis-2026-09-28.md | synthesis/hypothesis, no new measurements |
| highlights-2026-09-28.md | summary of other notes, no primary data |
| novelty-audit-2026-09-28.md | literature review, no measurements |
| exploitgym-leads-synthesis-2026-09-28.md | lead synthesis, investigative not observational |
| web-mechanism-hunt-synthesis-2026-09-28.md | synthesis of negative hunt |
| gem-bridge-hunt-2026-09-27.md / gem-bridge-swarmtraces-2026-09-27.md | cross-corpus bridging analysis |
| gem-dashboards-2026-09-27.md / gem-social-cards-brief-2026-09-27.md | publication/dashboard process docs |
| gem-schema-review-2026-09-27.md / gem-schema-conformance-2026-09-27.md / collusion-wiki-schema-2026-09-27.md | schema process docs |
| gem-backcorrect-2026-09-27.md / gem-count-reconciliation-2026-09-28.md | reconciliation process (superseded counts) |
| gem-key-reconciliation-2026-09-27.md | superseded by the corrected disclosure census (imported) |
| gem-pipeline-test.md / gem-relation-crosswalk.md / gem-keywords-2026-09-27.md | pipeline test / mapping tables, process artifacts |
| gem-hunt-librariesio-2026-09-27.md | earlier libraries.io lane; pattern-battery note is the structured successor (imported) — not re-read in depth, flagged for a follow-up check |
| dir-triage-W1..W7.md, workstream-E-audit-2026-09-28.md, workstream-c3-2026-09-28.md | other workers' triage/process docs |
| data-completeness-2026-09-28.md, data-verification-sweep-2026-09-29.md, normalization-sweep-synthesis-2026-09-29.md, hygiene-2026-09-28.md, hf-hygiene-scan-2026-09-29.md, hf-load-verification-2026-09-29.md | audit/verification process docs, not source observations |
| lane-checklist.md | ops checklist |
| fieldnotes-gem-2026-09-27.md | field notes narrative (read; measurements already covered by imported notes) |
| gem-apikey-disclosure process narrative | discontinued packet narrative stays notes-only; only the census imported |
| eval-cti-brief-2026-09-28-v2.png / eval-structure-cti-2026-09-28.png / timeline-graphic-2026-09-28.png | publication graphics, not event records |
| gems-es-mapping.json | ES mapping artifact, not observations |
| schema/ (dir) | schema documentation, not notes content |

## NOT READ IN DEPTH (RANK — other workstreams' lane notes; no gem/swarmtraces measurements expected)

Paste lanes: paste-archive-gap-2026-09-28.md, paste-archive-recovery-2026-09-27.md, paste-bodies-render-2026-09-27.md, paste-linuxiarz-ingest-2026-09-27.md, pastebin-cluster-sweep-2026-09-28.md, iowacollab-pastes-2026-09-27.md
Proxy lanes: cors-bwa-proxy-2026-09-28.md, proxy-primitives-2026-09-27.md, recon-hfspace-proxies-2026-09-27.md, recon-jqp-vercel-2026-09-27.md, recon-jsonhero-2026-09-27.md, recon-md-succ-ai-2026-09-27.md, recon-rmn-re-2026-09-27.md, reverse-tunnels-2026-09-27.md, rmn-re-history-2026-09-27.md, rmn-re-linktable-2026-09-27.md
Shortener lanes: university-shorteners-2026-09-28.md, university-shorteners-batch2/3-2026-09-28.md, uoft-shorteners-2026-09-28.md, vanderbilt-shortener-2026-09-27.md, yourls-resweep-2026-09-28.md
Wiki/board lanes: agent-convo-venues-2026-09-28.md, agent-surfaces-2026-09-27.md, agents-relay-sweep-2026-09-28.md, commonlog-scan-2026-09-28.md, demowiki-ingest-2026-09-27.md, ludism-wikis-ingest-2026-09-27.md, march7-rce-modality-2026-09-27.md, nsi-venue-sweep-2026-09-28.md, open-data-api-venues-2026-09-28.md, powerbi-fronting-2026-09-27.md, public-board-ingest-2026-09-27.md, tantive-space-ingest-2026-09-27.md, termina-counter-lane-2026-09-27.md, thecolony-ai-ingest-2026-09-27.md, transfer-test-family-2026-09-28.md, worldpoverty-task-family-2026-09-28.md, pxweb-national-stats-2026-09-28.md
Analyst notes (other lanes): analyst-note-cybergym-infra, -dockerhub-trojan-images, -exfil-endpoint-pivot, -exploitgym, -forged-flag-hunt, -github-forensics, -hf-tampering-check, -july7-gem-forensics, -pastebin-pivot, -separate-eval-test, -urlquery-marker-sweep, -wayback-gem-capture, -xss-ssti-census (all 2026-09-28)
Misc: ELASTIC_WRITE_PAUSE, admin-deletions-2026-09-28.md, july6-staging-2026-09-28.md, july7-wave-2026-09-28.md, jsonhero-docs-2026-09-27.md, timeline-anchors-2026-09-28.md, gem-contents-deepdive-2026-09-27.md, gem-runner-hunt-2026-09-27.md, gem-url-hunt-2026-09-27.md, gem-hunt-openai-incident-2026-09-27.md, gem-hunt-collusion-wiki-2026-09-27.md, gem-hunt-collusion-wiki-ingest-2026-09-27.md, rubygems-rescan-2026-09-27.md
Other workers' (do not touch): completeness-audit-A/B/C/D-2026-09-29.md

These belong to other lanes/workstreams; any structured measurements in them are that lane's data to farm, not this worker's. A follow-up full-read pass is recommended if the parent wants exhaustive coverage.
