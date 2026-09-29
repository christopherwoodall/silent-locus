"""July-7 gem forensics fetcher: read-only capture of Diffend diff pages.

Read-only. Fetches ONLY https://my.diffend.io/gems/<name>[/<version>] pages.
Never contacts exfil endpoints (oast.online, webhook.site, etc.).
Resumable: skips files already on disk. Pacing 4s + backoff (Diffend is hostile).
"""
import os, sys, time, json, subprocess, hashlib

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(PROJ, "data", "july7-gem-forensics")
RAW = os.path.join(OUTDIR, "raw")
LOG = os.path.join(OUTDIR, "progress.log")
UA = "rubygems-july7-forensics/1.0 (read-only forensic capture; no install)"

os.makedirs(RAW, exist_ok=True)


def log(msg):
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    line = "%s %s" % (ts, msg)
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def curl_get(url, path, retries=3):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return "skip:exists"
    for attempt in range(retries):
        try:
            p = subprocess.run(
                ["curl", "-sS", "-L", "--max-time", "60", "-A", UA, "-o", path,
                 "-w", "%{http_code}", url],
                capture_output=True, text=True, timeout=90)
            code = p.stdout.strip()
            if code == "200" and os.path.getsize(path) > 100:
                return "ok:200"
            log("retry %s -> http %s stderr=%s" % (url, code, p.stderr[:120]))
        except Exception as e:
            log("retry %s -> %s" % (url, e))
        time.sleep(6 * (2 ** attempt))
    try:
        os.remove(path)
    except OSError:
        pass
    return "fail"


def main():
    targets = []
    with open("/tmp/july7_targets.txt") as f:
        for line in f:
            line = line.strip()
            if line:
                targets.append(json.loads(line))
    log("forensics fetch start: %d gems" % len(targets))
    total, ok = 0, 0
    for name, checked_ver, versions, wave, notes, first_pub in targets:
        n = 0
        # gem index page
        gpath = os.path.join(RAW, "%s.html" % name)
        st = curl_get("https://my.diffend.io/gems/%s" % name, gpath)
        total += 1
        ok += st.startswith("ok")
        log("gempage %s -> %s" % (name, st))
        time.sleep(4)
        # diff pages for the mechanism-checked version + all versions (small set)
        for v in versions:
            vpath = os.path.join(RAW, "%s__%s.html" % (name, v.replace("/", "_")))
            st = curl_get("https://my.diffend.io/gems/%s/%s" % (name, v), vpath)
            total += 1
            ok += st.startswith("ok")
            log("diff %s %s -> %s" % (name, v, st))
            time.sleep(4)
    log("forensics fetch done: %d ok / %d total" % (ok, total))
    # manifest of raw captures
    man = []
    for fn in sorted(os.listdir(RAW)):
        fp = os.path.join(RAW, fn)
        h = hashlib.sha256(open(fp, "rb").read()).hexdigest()
        man.append({"file": "raw/" + fn, "sha256": h,
                    "bytes": os.path.getsize(fp)})
    with open(os.path.join(OUTDIR, "raw-manifest.json"), "w") as f:
        json.dump(man, f, indent=1)
    log("raw manifest: %d files" % len(man))


if __name__ == "__main__":
    main()
