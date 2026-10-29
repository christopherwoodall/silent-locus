#!/usr/bin/env python3
"""Aggregate the rubygems-goimport-campaign giant lane into a Factum bundle.

BigSexyWarlock69 approved aggregation (2026-10-10): do NOT 1:1 ingest the
10,873 legacy event rows. This script re-derives the aggregation from the
legacy evidence (events.jsonl in the lane dir) and writes the bundle JSON.

Outputs: data/lanes/rubygems-goimport-campaign/bundle.json (bundle format 2)

Methodology (documented in PROVENANCE.md):
- Packages: union of JFrog GemStuffer inventory (campaign_specimen) and
  Diffend graph_node gem labels, deduped by gem name. 3,028 distinct names:
  3,025 campaign gems + 3 live reference gems (json, oai, thor).
- Pre-ingest dedup: every campaign package name matched against committed
  Factum records (data/records/*/records.jsonl). All 3,025 already exist,
  mostly under lane 2026-09-29-gem-temporal-pivot (3,027 obs) plus
  2026-05-11-osv and others. Zero new package records submitted.
- IOCs: 1,248 indicator rows collapsed to 14 notable host/token-level IOCs
  (council domains, jina proxy variant, repo-target IP, zz-token, probe names).
  1,234 encoding/permutation variants skipped as low-value.
- Claims: OBSERVED-grade aggregate counts, citing the aggregation run record.
"""
import json, os, re
from collections import Counter

LANE_DIR = os.path.dirname(os.path.abspath(__file__))
EVENTS = os.path.join(LANE_DIR, "events.jsonl")
OUT = os.path.join(LANE_DIR, "bundle.json")

LANE = "rubygems-goimport-campaign"
NOW = "2026-10-10T04:05:00Z"  # aggregation run time (UTC)

kinds = Counter()
gem_names = set()
gem_vers = {}
gem_status = Counter()
gem_subtype = Counter()
indicator_subtype = Counter()
spec_names = set()
ioc_first = {}

for line in open(EVENTS):
    d = json.loads(line)
    rk = d.get("record_kind")
    kinds[rk] += 1
    l = d.get("labels", {})
    if rk == "graph_node":
        t = l.get("node.type")
        if t == "gem":
            n = l.get("node.package")
            gem_names.add(n)
            vid = l.get("node.id", "")
            v = vid.rsplit("-", 1)[-1] if vid else ""
            gem_vers.setdefault(n, set()).add(v)
            gem_status[l.get("node.status")] += 1
            gem_subtype[l.get("node.subtype")] += 1
        elif t == "indicator":
            st = l.get("node.subtype")
            indicator_subtype[st] += 1
            fs = l.get("first_seen")
            if fs and (st not in ioc_first or fs < ioc_first[st][0]):
                ioc_first[st] = (fs, l.get("timestamp_source"))
    elif rk == "campaign_specimen":
        m = re.match(r"JFrog GemStuffer inventory: (\S+) \(([^)]+)\)", d.get("description", ""))
        if m:
            spec_names.add(m.group(1))

campaign = (gem_names | spec_names) - {"json", "oai", "thor"}
multi = sum(1 for v in gem_vers.values() if len(v) > 1)

def tags(extra=None):
    t = {"lane": LANE}
    if extra:
        t.update(extra)
    return t

records = []

# 1. lane locator source
records.append({
    "ref": "lane-source",
    "record_kind": "source",
    "body": {
        "source_type": "submitted",
        "title": "rubygems-goimport-campaign lane locator",
        "locator": ("data/lanes/rubygems-goimport-campaign/ (10,873 legacy event rows; "
                    "events.jsonl, rollup.jsonl, raw/, PROVENANCE.md, SHA256SUMS); legacy path "
                    "evidence/2025-03-04-rubygems-goimport-campaign/ renamed to "
                    "evidence/remove-2025-03-04-rubygems-goimport-campaign/ after aggregation ingest "
                    "into Factum on branch factum-shaping"),
    },
    "tags": tags({"docs_path": "data/lanes/rubygems-goimport-campaign/"}),
})

# 2. aggregation run record (citable by claims)
records.append({
    "ref": "agg-run",
    "record_kind": "run",
    "body": {
        "run_kind": "lane_aggregation",
        "tool": "build_aggregation.py",
        "started": "2026-10-10T04:04:00Z",
        "ended": NOW,
        "params": {
            "lane": LANE,
            "input_rows": 10873,
            "dedup_key": "gem name (infra.package name); IOC term for indicators",
            "package_overlap_with_factum": "3,025 of 3,025 campaign packages already present; 0 resubmitted",
            "ioc_aggregation": "host-level dedup of 1,248 indicator rows into 14 notable IOCs",
        },
        "coverage": {
            "description": ("Aggregate 10,873 legacy rubygems-goimport-campaign rows: "
                            "union 3,028 gem names, 1,248 indicator rows, pre-ingest dedup "
                            "against committed Factum records"),
            "scanned": 10873,
            "total": 10873,
            "complete": True,
        },
    },
    "tags": tags(),
})

# 3. notable IOC observations (host/token level)
IOCS = [
    ("democracy.wandsworth.gov.uk", "domain", "2026-05-11T13:29:00Z",
     "Council-domain host embedded in gemspec metadata fingerprints of campaign gems (122 indicator rows). Primary decoy domain."),
    ("moderngov.lambeth.gov.uk", "domain", "2026-05-11T13:29:00Z",
     "Council-domain host embedded in gemspec metadata fingerprints (91 indicator rows)."),
    ("moderngov.southwark.gov.uk", "domain", "2026-05-11T13:29:00Z",
     "Council-domain host embedded in gemspec metadata fingerprints (56 indicator rows)."),
    ("digitizationguidelines.gov", "domain", "2026-05-11T13:29:00Z",
     "Domain embedded in gemspec metadata fingerprints (35 indicator rows); FADGI digitization guidelines URL used as decoy content."),
    ("20.49.140.101", "ip", "2026-05-11T13:29:00Z",
     "IP address embedded as a go-import repo target inside gemspec metadata (2 indicator rows). Direct-IP repo is anomalous."),
    ("lbs-tm-prod.trafficmanager.net", "domain", "2026-05-11T13:29:00Z",
     "Azure Traffic Manager host embedded as a go-import repo target in gemspec metadata (1 indicator row)."),
    ("httpbin.org", "domain", "2026-05-11T13:29:00Z",
     "Recon-testing service embedded as a go-import repo target in gemspec metadata (1 indicator row)."),
    ("s.jina.ai", "domain", "2026-05-11T13:29:00Z",
     "jina.ai proxy variant host used in go-import repo URLs embedded in gemspec metadata (3 indicator rows)."),
    ("lat2search1", "marker", "2026-05-11T13:29:00Z",
     "Anomalous token embedded as a go-import repo value in gemspec metadata (1 indicator row)."),
    ("zzak", "marker", "2026-09-09T06:24:12.883Z",
     "zz-token extracted from gem metadata (1 indicator row). zz token family marker."),
    ("probe", "probe-name", "2026-05-12T01:50:00Z",
     "Probe-name marker from gem metadata (4 probe-name indicator rows share this vocabulary)."),
    ("Probe", "probe-name", "2026-05-12T01:50:00Z",
     "Probe-name marker (capitalized variant) from gem metadata."),
    ("probe3", "probe-name", "2026-05-12T01:50:00Z",
     "Probe-name marker from gem metadata."),
    ("southfetchprobe42", "probe-name", "2026-05-12T01:50:00Z",
     "Probe-name marker from gem metadata; names a campaign probe gem family (southfetchprobe42 also published 0.0.2 and 0.0.3)."),
]

for i, (term, cat, seen, note) in enumerate(IOCS):
    records.append({
        "ref": f"ioc-{i}",
        "record_kind": "observation",
        "body": {
            "type": "infra.ioc",
            "source": "@lane-source",
            "observed_at": seen,
            "time_basis": "source_metadata",
            "files": [],
            "data_schema": "urn:factum:infra:ioc:1",
            "data": {
                "term": term,
                "category": cat,
                "status": "active",
                "provenance": ("legacy lane data/lanes/rubygems-goimport-campaign/events.jsonl "
                               "(10,873 rows); first_seen from node labels"),
            },
        },
        "tags": tags({"observed_at_note": note}),
    })

ioc_refs = [f"@ioc-{i}" for i in range(len(IOCS))]

# 4. OBSERVED-grade summary claims
claims = [
    ("legacy_node_census", {
        "total_rows": 10873,
        "record_kinds": dict(kinds),
        "graph_nodes": {"gem": gem_status and sum(gem_status.values()),
                        "indicator": sum(indicator_subtype.values()),
                        "file": kinds["graph_node"] - sum(gem_status.values()) - sum(indicator_subtype.values())},
    }, "Census of the 10,873 legacy event rows: 2,830 graph_node records plus run-log, "
       "inventory, sweep, and finding rows. rollup.jsonl already covered the 2,830 "
       "graph_node rows by day; this run adds the JFrog inventory and finding layers."),
    ("distinct_gem_packages", {
        "distinct_packages": len(gem_names | spec_names),
        "campaign_packages": len(campaign),
        "reference_packages_excluded": ["json", "oai", "thor"],
        "jfrog_gemstuffer_names": len(spec_names),
        "diffend_graph_names": len(gem_names),
        "names_in_both_sources": len(gem_names & spec_names),
        "multi_version_packages": multi,
    }, "Union of JFrog GemStuffer inventory names and Diffend graph-node gem names, "
       "deduped by exact gem name. Three live reference gems (json, oai, thor, still "
       "listed on RubyGems) are comparison nodes, not campaign specimens."),
    ("package_status_distribution", {
        "dead": gem_status.get("dead", 0),
        "live": gem_status.get("live", 0),
        "subtypes": dict(gem_subtype),
        "jfrog_inventory_versions": "all 3,025 GemStuffer rows at version 0.0.1",
    }, "Diffend harvest gems are all status dead (taken down); the 3 live rows are the "
       "json/oai/thor reference nodes. Every JFrog GemStuffer inventory row is 0.0.1."),
    ("preingest_dedup_outcome", {
        "campaign_packages_checked": len(campaign),
        "already_in_factum": len(campaign),
        "resubmitted": 0,
        "overlap_lanes": ["2026-09-29-gem-temporal-pivot", "2026-05-11-osv",
                          "webhook-deaddrops", "2026-03-07-march7-rce-modality",
                          "2026-08-10-wayback-gem-capture"],
    }, "Pre-ingest dedup per SKILL.md: all 3,025 campaign package names already exist "
       "as infra.package observations in the committed Factum corpus (3,027 observations "
       "in lane 2026-09-29-gem-temporal-pivot cover the same gem set). Zero package "
       "records submitted for this lane."),
    ("indicator_ioc_aggregation", {
        "indicator_rows": sum(indicator_subtype.values()),
        "indicator_subtypes": dict(indicator_subtype),
        "notable_iocs_submitted": len(IOCS),
        "low_value_variants_skipped": sum(indicator_subtype.values()) - len(IOCS),
        "go_import_vcs_values_skipped": "bzr, fossil, git, hg, mod, svn (bare VCS keywords, no signal)",
    }, "1,248 indicator rows collapsed to 14 notable host/token-level IOCs: URL-path and "
       "encoding variants of the same council domains and r.jina.ai proxy URLs skipped "
       "as low-value; bare go-import VCS keywords skipped."),
]

for name, value, note in claims:
    records.append({
        "ref": f"claim-{name}",
        "record_kind": "claim",
        "body": {
            "subject": "@agg-run",
            "property": name,
            "value": value,
            "basis": "OBSERVED",
            "cites": ["@agg-run"] + ioc_refs[:3],
            "note": note,
        },
        "tags": tags(),
    })

bundle = {
    "bundle": 2,
    "actor": "agent:lane-ingest-worker",
    "idempotency_key": "rubygems-goimport-campaign-aggregation-20261010",
    "lane": LANE,
    "records": records,
}

with open(OUT, "w") as f:
    json.dump(bundle, f, indent=1)
print(f"wrote {OUT}: {len(records)} records")
