import json, time, urllib.request, urllib.error, os, datetime

now = datetime.datetime.now(datetime.timezone.utc).isoformat()
progress = open('progress.log','a')
def log(msg):
    line = f"{datetime.datetime.now(datetime.timezone.utc).isoformat()} {msg}"
    print(line, flush=True); progress.write(line+"\n"); progress.flush()

def get_json(url, headers=None, tries=6):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers or {})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            wait = min(120, 5*(2**i))
            log(f"HTTP {e.code} {url.split('?')[0][:80]} — sleep {wait}s try {i+1}/{tries}")
            time.sleep(wait)
    raise RuntimeError(f"failed: {url}")

def anon_token(ns, repo):
    d = get_json(f"https://auth.docker.io/token?service=registry.docker.io&scope=repository:{ns}/{repo}:pull")
    return d['token']

for org in ['cybergym','n132']:
    repos = json.load(open(f'org-{org}-repos.json'))['results']
    for r in repos:
        repo = r['name']
        out = f'registry-tags-{org}-{repo}.json'
        if os.path.exists(out):
            log(f"SKIP {org}/{repo} (registry list cached)")
            continue
        tok = anon_token(org, repo)
        H = {'Authorization': f'Bearer {tok}'}
        tags, last = [], None
        while True:
            url = f"https://registry-1.docker.io/v2/{org}/{repo}/tags/list?n=1000" + (f"&last={last}" if last else "")
            d = get_json(url, H)
            batch = d.get('tags') or []
            tags.extend(batch)
            if len(batch) < 1000: break
            last = batch[-1]
            time.sleep(0.3)
        json.dump({'org':org,'repo':repo,'count':len(tags),'retrieved':now,
                   'source':f"https://registry-1.docker.io/v2/{org}/{repo}/tags/list",
                   'tags':sorted(tags)}, open(out,'w'))
        log(f"REGISTRY {org}/{repo}: {len(tags)} tags")
        time.sleep(1.0)
progress.close()
