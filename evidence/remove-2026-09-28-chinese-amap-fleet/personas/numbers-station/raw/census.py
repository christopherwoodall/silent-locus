#!/usr/bin/env python3
"""Numbers-station lane 1: nonce/ID grammar census across the three corpora.
Structural only. Outputs raw/census.json + raw/grammars.md. Resumable: skips
corpora already covered in census.json unless --redo."""
import json, re, os, sys, collections

BASE = os.path.expanduser("~/workspace/silent-locus/data")
CORPORA = {
    "amap-fleet": f"{BASE}/2026-09-28-chinese-amap-fleet/events.jsonl",
    "oai-traces": f"{BASE}/2026-10-03-openai-agent-traces/events.jsonl",
    "oai-tag-sweep": f"{BASE}/2026-10-01-oai-tag-sweep/events.jsonl",
}
OUTDIR = os.path.expanduser("~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/numbers-station/raw")
os.makedirs(OUTDIR, exist_ok=True)

PATS = {
    "epoch_ms_13": re.compile(r"\b(1[0-9]{12}|17\d{11})\b"),
    "zz_eq": re.compile(r"zz=([A-Za-z0-9_.-]{1,40})"),
    "uqscan": re.compile(r"uqscan=([A-Za-z0-9_.-]{1,60})"),
    "retry_epoch": re.compile(r"retry=(\d{10,13})-(\d{1,3})"),
    "uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "hex_long": re.compile(r"\b[0-9a-f]{32,}\b", re.I),
    "tag_word_date": re.compile(r"\b([a-z]{2,20}20\d{6}[a-z]?\d?[a-z]?)\b"),
    "jwt_shape": re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
    "enodia": re.compile(r"[?&]enodia=([A-Za-z0-9_-]{1,20})"),  # prefix only, not the token
    "b64_blob": re.compile(r"[A-Za-z0-9+/]{100,}={0,2}"),
    "fleet_tag_val": re.compile(r'"fleet_tag":\s*"([^"]+)"'),
    "oai_tag": re.compile(r"\boai[a-z_]{0,20}\b"),
}

def shape_uqscan(v):
    s = re.sub(r"20\d{6}", "<DATE>", v)
    s = re.sub(r"\d+", "<N>", s)
    return s

def main():
    redo = "--redo" in sys.argv
    state_path = f"{OUTDIR}/census.json"
    state = json.load(open(state_path)) if os.path.exists(state_path) and not redo else {"corpora_done": {}, "grammars": {}}
    for cname, path in CORPORA.items():
        if cname in state["corpora_done"] and not redo:
            print(f"skip {cname} (done)")
            continue
        counts = collections.Counter()
        examples = collections.defaultdict(collections.Counter)
        shapes = collections.Counter()  # uqscan shapes
        enodia_prefix = collections.Counter()
        n = 0
        with open(path, errors="replace") as f:
            for line in f:
                n += 1
                for gname, pat in PATS.items():
                    for m in pat.finditer(line):
                        counts[gname] += 1
                        v = m.group(1) if m.lastindex else m.group(0)
                        if len(examples[gname]) < 400:
                            examples[gname][v[:80]] += 1
                        if gname == "uqscan":
                            shapes[shape_uqscan(v)] += 1
                        if gname == "enodia":
                            enodia_prefix[v] += 1
        state["corpora_done"][cname] = {
            "lines": n,
            "counts": dict(counts),
            "top_examples": {g: dict(c.most_common(25)) for g, c in examples.items()},
            "uqscan_shapes": dict(shapes.most_common(40)),
        }
        print(f"{cname}: {n} lines, counts={dict(counts)}")
        json.dump(state, open(state_path, "w"), indent=1)
    # grammar table
    md = ["# Nonce/ID grammar census", "", "| grammar | amap-fleet | oai-traces | oai-tag-sweep | notes |", "|---|---|---|---|---|"]
    gnames = sorted({g for c in state["corpora_done"].values() for g in c["counts"]})
    for g in gnames:
        row = [g] + [str(state["corpora_done"][c]["counts"].get(g, 0)) for c in CORPORA]
        md.append("| " + " | ".join(row) + " | |")
    md += ["", "## uqscan value shapes (across corpora)", ""]
    allshapes = collections.Counter()
    for c in state["corpora_done"].values():
        allshapes.update(c.get("uqscan_shapes", {}))
    for s, cnt in allshapes.most_common(40):
        md.append(f"- `{s}` ×{cnt}")
    open(f"{OUTDIR}/grammars.md", "w").write("\n".join(md) + "\n")
    print("wrote grammars.md")

if __name__ == "__main__":
    main()
