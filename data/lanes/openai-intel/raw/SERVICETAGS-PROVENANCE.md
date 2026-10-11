# PROVENANCE — Azure ServiceTags raw capture (azure-servicetags, openai-intel lane)

## Source file

- File: ServiceTags_Public_20261005.json
- Microsoft download page: https://www.microsoft.com/en-us/download/details.aspx?id=56519
- Direct download URL:
  https://download.microsoft.com/download/7/1/d/71d86715-5596-4529-9b13-da13a5de5b63/ServiceTags_Public_20261005.json
  (the GUID path rotates weekly; this URL was extracted from the download
  page's confirmation HTML on 2026-10-11. A previously known GUID ending
  `...45b6` returned an empty reply for this week's file.)
- File version: 2026.10.05. Date published (Microsoft page): 10/6/2026.
- Top-level changeNumber: 421. Cloud: Public. Entries: 3321. IPv4 only.
- Retrieval method: curl -sSL (Linux VM, egress proxy).
- Retrieved: 2026-10-11T01:19:16Z (UTC).
- HTTP 200, 4,330,497 bytes.
- sha256: fed834a26c3847f6c66715c924259d9d6f437078b32decf0b5337e6414f96c98

## AzureOpenAI tag finding

The file contains NO `AzureOpenAI` service tag and no region-qualified
variants (e.g. `AzureOpenAI.EastUS`). Verified by scanning all 3321 entry
names (zero hits for `AzureOpenAI*`; zero base tags containing `AI`).

Historical checks:
- aeimer/terraform-azure-ip-ranges weekly snapshots: 2025-10-22 and
  2026-10-07 both contain zero `AzureOpenAI` references.
- ealtili/azure-service-tags-paloaltofws (ServiceTags_Public_20230710.json,
  July 2023): no AzureOpenAI ranges file present.
- Microsoft Learn service-tags-overview page (fetched 2026-10-11): zero
  `AzureOpenAI` mentions.
- Microsoft Learn Azure AI services virtual-networks doc (fetched
  2026-10-11): network rules for Azure AI services (including Azure OpenAI)
  are directed at the `CognitiveServicesFrontend` and
  `CognitiveServicesManagement` service tags.

Basis: Azure OpenAI resources are provisioned as
`Microsoft.CognitiveServices/accounts` of kind `OpenAI`; the published
endpoint ranges live under the CognitiveServices tags.

## Extraction

- Tags extracted: `CognitiveServicesFrontend` (150 unique CIDRs, cloud-wide
  entry only — no region variants exist) and `CognitiveServicesManagement`
  (1511 unique CIDRs, cloud-wide entry only).
- Deduped within batch to a union of 1661 unique CIDR strings
  (extracted_cidrs.json, kept with this note).
- Overlap check vs corpus rmn.re burst-creator IPs
  (185.228.3.86, 185.228.3.47, 185.228.3.66, 105.71.5.91, 45.130.202.7,
  159.26.105.49): 0 of 6 inside any extracted range (clean negative).
- Cross-batch dedup vs corpus: 0 exact CIDR dupes and 0 overlapping CIDRs
  across all 40395 existing infra.ioc records (grep over exported batches
  + ip_network overlap test).
- Grade: UPSTREAM (Microsoft-published; not directly observed).
- Distinguishes source note "azure-servicetags" from OpenAI's own
  published egress list (sibling worker, same lane).
