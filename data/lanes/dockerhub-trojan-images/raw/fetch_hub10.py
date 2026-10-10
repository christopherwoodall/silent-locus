import json, time, urllib.request, urllib.error, os, datetime

now = datetime.datetime.now(datetime.timezone.utc).isoformat()
progress = open('progress.log','a')
def log(msg):
    line = f"{datetime.datetime.now(datetime.timezone.utc).isoformat()} {msg}"
    print(line, flush=True); progress.write(line+"\n"); progress.flush()

def get(url, tries=6):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent':'research-fetch/1.0'})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            wait = min(180, 8*(2**i))
            log(f"HTTP {e.code} — sleep {wait}s try {i+1}/{tries}")
            time.sleep(wait)
    return None

def rec(t, org, repo):
    img = t.get('images') or []
    return {'org':org,'repo':repo,'tag':t.get('name'),
        'tag_last_pushed':t.get('tag_last_pushed'),'tag_status':t.get('tag_status'),
        'last_updated':t.get('last_updated'),'digest':t.get('digest'),
        'images_arch':sorted({i.get('architecture') for i in img}),
        'retrieved':now,'source':f"https://hub.docker.com/v2/repositories/{org}/{repo}/tags"}

repos = [('cybergym','arvo'),('cybergym','v8'),('cybergym','syzbot-target'),
         ('cybergym','nofuzz'),('cybergym','kernelctf-target'),('cybergym','e2e'),
         ('cybergym','new-arvo'),('cybergym','new-oss-fuzz'),('cybergym','agent-image'),
         ('cybergym','agent-scorer'),('cybergym','v8-cve-2020-6418'),
         ('n132','arvo'),('n132','linux-kernel'),('n132','cedalion'),('n132','pwn'),
         ('n132','kernel-compiler'),('n132','osiris'),('n132','bootlin-local')]
for org, repo in repos:
    out = f'hub10-{org}-{repo}.jsonl'
    if os.path.exists(out):
        log(f"SKIP {org}/{repo} hub10 cached")
        continue
    n = 0
    with open(out,'w') as f:
        for page in range(1, 11):
            d = get(f"https://hub.docker.com/v2/repositories/{org}/{repo}/tags?page_size=100&page={page}")
            if d is None or not d.get('results'):
                break
            for t in d['results']:
                f.write(json.dumps(rec(t, org, repo))+"\n"); n += 1
            if not d.get('next'): break
            time.sleep(1.2)
    log(f"HUB10 {org}/{repo}: {n} tags")
progress.close()
