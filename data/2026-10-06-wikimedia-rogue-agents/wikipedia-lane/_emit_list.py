import json, sys
# emits "host oldid parentid" lines for resolved (status ok) revisions
recs = json.load(open(sys.argv[1]))
with open(sys.argv[2], 'w') as f:
    for r in recs:
        # [host, oldid, title, user, ts, comment, tags, minor, parentid, content, status]
        if r[-1] == 'ok':
            f.write(f"{r[0]} {r[1]} {r[8]}\n")
