import sys, json
bodyfile, outpath, rank, title = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
try:
    with open(bodyfile, encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    print("JSONERR " + str(e)); sys.exit(0)
if data.get("error"):
    print("APIERR " + str(data["error"].get("info", data["error"]))); sys.exit(0)
pages = (data.get("query") or {}).get("pages") or []
for p in pages:
    if p.get("missing"):
        print("MISSING"); sys.exit(0)
revs = []
for p in pages:
    for r in (p.get("revisions") or []):
        revs.append({"rank": int(rank), "article": title,
                     "revid": r.get("revid"), "parentid": r.get("parentid"),
                     "user": r.get("user"), "timestamp": r.get("timestamp"),
                     "comment": r.get("comment"), "tags": r.get("tags", []),
                     "size": r.get("size")})
with open(outpath, "a", encoding="utf-8") as f:
    for o in revs:
        f.write(json.dumps(o, ensure_ascii=False) + "\n")
cont = ((data.get("continue") or {}).get("rvcontinue")) or ""
print("OK", len(revs), cont)
