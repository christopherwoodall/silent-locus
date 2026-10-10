#!/usr/bin/env python3
"""CT-MINER analyzer: parse crt.sh JSON, keep DNS-shaped identities only,
classify agent-shaped naming. OBSERVED facts only."""
import json, re, sys, glob, os
from collections import Counter

RAW = os.path.expanduser("~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/german-french-swarm-hunt/workers/ct-miner/raw")

# DNS-shaped: labels of a-z0-9_-, dots, optional leading '*.'
DNS_RE = re.compile(r'^(?:\*\.|)(?:[a-zA-Z0-9_-]+\.)*[a-zA-Z0-9_-]+$')

def dns_names(nv):
    out = []
    for line in (nv or "").split("\n"):
        line = line.strip().rstrip(".")
        if line and DNS_RE.match(line) and "." in line:
            out.append(line.lower())
    return out

DE_TLDS = (".de", ".at", ".ch")
FR_TLDS = (".fr", ".be", ".lu")
AGENT_GRAMMAR = ["oai", "zz=", "zz_", "httpbun", "uqprobe", "uqscan", "sub_poi",
                 "harness", "mcp", "board", "wiki", "dashboard", "ki-", "fleet",
                 "worker", "node-", "agent-", "bot-", "swarm", "schwarm", "essaim",
                 "aufgabe", "tache", "probe", "relay", "tunnel", "webhook"]

def analyze(path):
    try:
        with open(path) as f:
            data = json.load(f)
    except Exception as e:
        return {"file": os.path.basename(path), "error": str(e)}
    certs = data if isinstance(data, list) else []
    dns_idents = set()
    non_dns_idents = set()
    issuers = Counter()
    expired = 0
    for c in certs:
        nv = c.get("name_value", "")
        dns = dns_names(nv)
        for d in dns:
            dns_idents.add(d)
        for line in nv.split("\n"):
            line = line.strip()
            if line and not DNS_RE.match(line.strip().rstrip(".")):
                non_dns_idents.add(line[:80])
        issuers[(c.get("issuer_name") or "")[:60]] += 1
    de = sorted(i for i in dns_idents if i.endswith(DE_TLDS))
    fr = sorted(i for i in dns_idents if i.endswith(FR_TLDS))
    gram = {}
    for g in AGENT_GRAMMAR:
        hits = sorted(i for i in dns_idents if g in i)
        if hits:
            gram[g] = hits
    numbered = sorted(i for i in dns_idents if re.search(r'[-_](\d{1,4})$|[-_](\d{2,4})\.', i))
    longnum = sorted(i for i in dns_idents if re.search(r'(?<![\w.])\d{13,}(?![\w.])', i))
    return {
        "file": os.path.basename(path),
        "certs": len(certs),
        "unique_dns_idents": len(dns_idents),
        "non_dns_samples": sorted(non_dns_idents)[:8],
        "top_issuers": issuers.most_common(5),
        "de_tld_idents": de,
        "fr_tld_idents": fr,
        "grammar_hits": gram,
        "numbered_fleet_like": numbered[:40],
        "epoch_nonce_like": longnum[:20],
    }

if __name__ == "__main__":
    files = sorted(glob.glob(os.path.join(RAW, "q_*.json")))
    if len(sys.argv) > 1:
        files = [os.path.join(RAW, a) for a in sys.argv[1:]]
    for path in files:
        r = analyze(path)
        out = path.replace("raw/q_", "analysis_").replace(".json", ".json")
        with open(out, "w") as f:
            json.dump(r, f, indent=1, ensure_ascii=False)
        print("wrote", out, "certs=", r.get("certs"), "dns=", r.get("unique_dns_idents"))
