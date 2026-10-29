#!/usr/bin/env python3
"""RANGE-CURATOR: build raw/cidr-provider-map.jsonl from cached provider feeds.

Reads cached raw files in data/2026-10-06-wikipedia-top500-infra-scan/raw/ and
emits one JSON object per CIDR:
  {"cidr", "provider", "service", "source", "retrieved", ...optional notes}

Dedup policy:
  - Exact-duplicate CIDRs across sources are MERGED into one record, with
    "also_reported_by" listing the extra sources (and their provider/service).
  - NESTED overlaps (one CIDR inside another) are KEPT BOTH: the more specific
    record gets "broader_claims": [...] naming the containing ranges. Broad
    cloud records are retained because IPs outside the provider-published
    ranges still need attribution. This is documented in FINDINGS.md.
"""
import json, os, ipaddress, datetime

EVENT = "/home/hatch/workspace/silent-locus-top500/data/2026-10-06-wikipedia-top500-infra-scan"
RAW = os.path.join(EVENT, "raw")
OUT = os.path.join(RAW, "cidr-provider-map.jsonl")
NOW = "2026-10-06T20:52:00Z"

# (file, retrieved, parser) tuples
def parse_aws():
    d = json.load(open(os.path.join(RAW, "aws-ip-ranges.json")))
    rows = []
    for p in d["prefixes"]:
        rows.append((p["ip_prefix"], "aws", p.get("service", ""), "aws-ip-ranges.json"))
    for p in d["ipv6_prefixes"]:
        rows.append((p["ipv6_prefix"], "aws", p.get("service", ""), "aws-ip-ranges.json"))
    return rows

def parse_gcp():
    d = json.load(open(os.path.join(RAW, "gcp-cloud.json")))
    rows = []
    for p in d["prefixes"]:
        cidr = p.get("ipv4Prefix") or p.get("ipv6Prefix")
        rows.append((cidr, "gcp", "google-cloud/" + p.get("scope", ""), "gcp-cloud.json"))
    return rows

def parse_azure():
    d = json.load(open(os.path.join(RAW, "azure-servicetags.json")))
    rows = []
    for v in d["values"]:
        name = v["name"]
        for cidr in v["properties"].get("addressPrefixes", []):
            rows.append((cidr, "azure", name, "azure-servicetags.json"))
    return rows

def parse_prefix_file(fname, provider, service):
    d = json.load(open(os.path.join(RAW, fname)))
    rows = []
    for p in d["prefixes"]:
        cidr = p.get("ipv4Prefix") or p.get("ipv6Prefix")
        rows.append((cidr, provider, service, fname))
    return rows

def main():
    recs = []
    recs += parse_aws()
    recs += parse_gcp()
    recs += parse_azure()
    recs += parse_prefix_file("openai-chatgpt-user.json", "openai", "chatgpt-user")
    recs += parse_prefix_file("openai-searchbot.json", "openai", "oai-searchbot")
    recs += parse_prefix_file("openai-gptbot.json", "openai", "gptbot")
    recs += parse_prefix_file("anthropic-bots.json", "anthropic", "crawling-bots")
    recs += parse_prefix_file("perplexity-perplexitybot.json", "perplexity", "perplexitybot")
    recs += parse_prefix_file("perplexity-user.json", "perplexity", "perplexity-user")
    # Anthropic official docs page (retrieved live 2026-10-06):
    recs.append(("160.79.104.0/23", "anthropic", "inbound-api", "anthropic-ip-addresses.md"))
    recs.append(("2607:6bc0::/48", "anthropic", "inbound-api", "anthropic-ip-addresses.md"))
    recs.append(("160.79.104.0/21", "anthropic", "outbound-tool-calls", "anthropic-ip-addresses.md"))
    for c in ["34.162.46.92/32", "34.162.102.82/32", "34.162.136.91/32",
              "34.162.142.92/32", "34.162.183.95/32"]:
        recs.append((c, "anthropic", "phased-out", "anthropic-ip-addresses.md"))

    # exact-dedupe: same CIDR string from multiple sources
    merged = {}
    for cidr, prov, svc, src in recs:
        try:
            net = ipaddress.ip_network(cidr, strict=False)
        except ValueError:
            print("SKIP invalid:", cidr, src)
            continue
        key = (str(net), prov)
        if key not in merged:
            merged[key] = {"cidr": str(net), "provider": prov, "service": svc,
                           "source": src, "retrieved": NOW, "other_sources": []}
        else:
            merged[key]["other_sources"].append({"service": svc, "source": src})

    rows = list(merged.values())

    # nesting annotation: small provider-published sets vs broad cloud sets.
    # Check which published CIDRs sit inside which cloud CIDRs.
    pub = [r for r in rows if r["provider"] in ("openai", "anthropic", "perplexity")]
    cloud = [r for r in rows if r["provider"] in ("aws", "gcp", "azure")]
    cloud_nets = [(ipaddress.ip_network(r["cidr"]), r["provider"], r["service"], r["cidr"])
                  for r in cloud]
    cloud_nets.sort(key=lambda t: t[0].prefixlen)  # broadest first
    for r in pub:
        n = ipaddress.ip_network(r["cidr"])
        hits = []
        for cn, cp, cs, cs_raw in cloud_nets:
            if n.version != cn.version:
                continue
            if n != cn and n.subnet_of(cn):
                hits.append(f"{cp}/{cs} ({cs_raw})")
                if len(hits) >= 3:
                    break
        if hits:
            r["broader_claims"] = hits

    for r in rows:
        extra = r.pop("other_sources", [])
        if extra:
            r["also_reported_by"] = extra

    rows.sort(key=lambda r: (r["provider"], int(ipaddress.ip_network(r["cidr"]).version),
                             r["cidr"]))
    with open(OUT, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print("wrote", OUT, "records:", len(rows))
    # per-provider stats
    stats = {}
    for r in rows:
        s = stats.setdefault(r["provider"], {"cidrs": 0, "v4_addr": 0, "v6_addr": 0})
        s["cidrs"] += 1
        n = ipaddress.ip_network(r["cidr"])
        if n.version == 4:
            s["v4_addr"] += n.num_addresses
        else:
            s["v6_addr"] += n.num_addresses
    print(json.dumps(stats, indent=1))

main()
