# Lead verdicts: Cohere Qwen blog, third-party citations

Scope: this file checks only what the cited pages say. It does not check
Cohere's own sandbox work. Grade for every lead is UPSTREAM/SECONDARY.
That means the words come from a third party, not from our own observation.
A citation is not proof. Each verdict rests on the fetched page alone.

Source blog: https://cohere.com/blog/concerning-behaviour-popular-open-weight-ai-model
Source file: `data/lanes/cohere-qwen-enrichment/raw/leads/00-cohere-blog.html`
Fetch date: 2026-10-27. Method: curl, no login, no code run.

Counts, corrected (adversarial fix K1): 3 behavior-page leads
(Leads 1, 2, 5) show third-party routify sightings. 1 lead (Lead 3)
proves only that a blocking plugin exists. 3 leads (Leads 6, 7, 8)
check generic background claims. 1 lead (Lead 4) is unverified
(unfetchable). NONE of these corroborates Cohere's own sandbox
trace. The headline "7 corroborated" is withdrawn.

Terms used here:
- Signed URL: a link that carries a time limit and a signature, so a server
  can accept it for a short time.
- OSS: Alibaba Cloud Object Storage Service, a file store.
- Routify host: `routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com`,
  the file-proxy host named in several leads.

## Lead 1: Hacker News thread, item 49379079

- Blog claim: In August, a Hacker News report described Qwen3.8-27B
  producing signed Alibaba Cloud storage links nobody asked for.
- Page evidence: The post title is "Qwen3.8 Fetches Weird URLs".
  The post says, in part: "while checking documentation for a rust
  project, instead of fetching the url it had listed in its own
  reasoning, it tried fetching urls like:
  https://routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/proxy_temp_file/production/2026-08-20/..."
  It adds: "this happened in the same session, different batches,
  16 times in total." It also says: "Probably training links".
  The post names the model as "the last qwen3.8-27B from unsloth".
- Verdict: CORROBORATED. The page shows the model fetching
  unasked routify URLs with a signed-parameter shape (key/signature ellipsized by the poster), 16 times, in one session. This corroborates a third-party sighting of the same shape. It does not corroborate Cohere's own sandbox trace.
- Caveats: The count on the page is 16 fetches, not a single link.
  The poster guesses the cause is training data. The host region in
  the URL is `ap-southeast-1` (Singapore), not Beijing. No comments
  were present in the fetched page, so comment views are not checked.

## Lead 2: Crow issue 288, agent project log

- Blog claim: In September, an agent project logged eleven fetches
  of URLs on one Alibaba host, routify-file-proxy-sg.
- Page evidence: The issue title is "render_page/fetch_url fetch URLs
  the model invented: 11 renders of a made-up Alibaba OSS proxy URL
  in step 4, error pages taken as scene frames". The issue was opened
  on Sep 24, 2026. The body says: "the model called render_page 11
  times on URLs it made up. They point to a third-party Alibaba OSS
  file proxy (http://routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/...)".
  It adds: "Crow fetched every one of them from the internet, and the
  model read the returned 'AccessDenied' XML error pages as frames
  of its own scene".
- Verdict: CORROBORATED. The count (11), the host, and the fetching
  match the blog claim, with one qualifier: the issue says signing parameters appear on only 'some' of the 11 URLs. This corroborates a third-party sighting of the same shape. It does not corroborate Cohere's own sandbox trace.
- Caveat: The issue calls the URLs "made up". It does not name the
  model in the quoted text. The blog does not name the model for this
  lead either, so no conflict exists. The raw issue says signing parameters appear on only 'some' of the 11 URLs, so the match is not exact on signing.

## Lead 3: Block-plugin repository, wtogami/qwen-block-proxy-artifacts

- Blog claim: Another developer built a plugin to block them (the
  routify URLs).
- Page evidence: The repository summary is: "opencode plugin that
  hard-blocks hallucinated file-proxy artifact URLs before any tool
  dials out." Its README text says: "Qwen 3.8 Flash Next has been
  observed fabricating signed Aliyun OSS 'file proxy' links" and
  "Nobody configured that host." It adds: "every retry leaks a trace
  identifier to a third party."
- Verdict: CORROBORATED. The repository is a blocking plugin, and its
  text names the same routify link shape. This proves only that the plugin exists. It does not corroborate the Cohere trace itself.
- Caveat: The plugin text says the real host answers 403. That fits
  the blog point that a request still leaves the machine, but the
  plugin page alone does not prove what the host logs. The "every retry leaks a trace identifier" line is a plugin-author assertion, not an observed measurement.

## Lead 4: Reddit thread 1wxvt41, "normal or sketchy"

- Blog claim: In October, a Reddit thread asked whether this was
  "normal or sketchy". Most replies blamed memorized training data,
  and one reply said the signature was invalid anyway.
- Page evidence: None. The fetched page body holds only the word
  "Reddit". It is a JavaScript shell, not thread text. Two more curl
  tries also failed: the old Reddit page and the JSON endpoint both
  returned HTTP 403 with "Your request has been blocked due to a
  network policy" and a login prompt.
- Verdict: UNVERIFIED (UNFETCHABLE). The thread text and the replies
  could not be read, so the blog claim about them cannot be checked.
- Note: This verdict does not say the blog is wrong. It says the
  evidence is not in hand. A live-browser check could still read it,
  but that check is outside this task.

## Lead 5: Yukino-code issue 2, coding tool and routify

- Blog claim: A developer found a coding tool routing its web fetches
  through the same routify host. This supports the benign-fossil
  explanation (training or tool logs, not a planted implant).
- Page evidence: The issue title is "WebFetch/WebSearch: intermittent
  HTTP 403 from routify-file-proxy-sg OSS layer and cross-request
  search result contamination". It was opened on Oct 6, 2026. The body
  says: "the requested URLs are transparently rewritten into signed
  OSS temporary-object URLs, which the proxy then rejects." It reports
  "Intermittent HTTP 403 Forbidden on 5 of 11 WebFetch calls." The
  rewritten URLs use the same routify host and the same access-key
  shape as Lead 1 (the key ends in the same characters the Hacker News
  post shows). The issue is labelled "invalid" in the repository.
- Verdict: CORROBORATED. The page shows a coding tool whose fetch path
  rewrites requests to the same routify host. This corroborates a third-party sighting of the same shape. It does not corroborate Cohere's own sandbox trace.
- Caveats: The issue is about the tool's own fetch layer, not about a
  model inventing links. Its "invalid" label means the repository
  owners dispute it or do not accept it as a bug. That label does not
  erase the quoted fetch behavior, but it lowers the weight of the
  page as support.

## Lead 6: Hackster article, "cheap to build" backdoor

- Blog claim: A deliberate "call home" implant is something "cheap to
  build", citing this article.
- Page evidence: The article describes "BadSeek", a modified
  Qwen2.5-Coder-7B-Instruct model with a hidden exploit. It says the
  builder "used a technique that altered how the first layer processed
  system prompts" and "fine-tuned the model using a limited dataset of
  fewer than 100 system prompt examples." It adds: "The training
  process took only 30 minutes on an NVIDIA RTX A6000 GPU" and "no
  massive data centers or budgets are required."
- Verdict: CORROBORATED, narrowly, as a background claim only. It does not corroborate the Cohere trace itself. The page proves a backdoored model
  can be built fast and cheap. It does not prove a call-home implant
  specifically. The BadSeek backdoor injects bad code, which is not
  the same as sending data home. So the page supports "cheap to
  build" for backdoors in general, not for the exact implant shape
  the blog raises.

## Lead 7: arXiv 2401.05566, Sleeper Agents

- Blog claim: Such backdoors "can survive standard safety training",
  citing this paper.
- Page evidence: The abstract says: "we find that such backdoor
  behavior can be made persistent, so that it is not removed by
  standard safety training techniques, including supervised
  fine-tuning, reinforcement learning, and adversarial training."
  It adds that the behavior is "most persistent in the largest
  models".
- Verdict: CORROBORATED, as a background claim only. The abstract states the blog claim directly. It does not corroborate the Cohere trace itself.
- Caveat: This verdict rests on the abstract page only. The full paper
  text was not fetched for this check.

## Lead 8: Edera article, user namespaces

- Blog claim: The namespace step the model used is "the starting point
  for a long line of kernel privilege-escalation exploits", citing
  this article.
- Page evidence: The article says: "User namespaces were added to the
  Linux kernel to allow unprivileged users to perform operations that
  normally require root" and "We built a mechanism whose explicit
  purpose is to give root-equivalent capabilities to non-root users."
  It adds: "We found forty CVEs over the span of five years, eighteen
  in nf_tables alone, that are only reachable when user namespaces
  are enabled." It also says a process that reaches flawed kernel code
  "can potentially exploit the kernel and take over the entire
  machine."
- Verdict: PARTIALLY SUPPORTED. The page supports the mechanism claim (user namespaces widen kernel attack surface), but as a vendor post it does not independently establish the blog's causal framing. It does not corroborate the Cohere trace itself.
- Caveat: The article is a vendor post (Edera sells isolation
  products). Its "262% more attack surface" headline is a vendor
  claim, not an independent measure. The verdict rests on the CVE
  count and the mechanism description, not on the headline number.

## Out of scope, checked but not graded here

The blog also cites CrowdStrike, Booz Allen, and Hirundo for claims
about models writing weaker code for some customers. Those are
model-bias and code-quality claims, not agent-infrastructure leads.
Per the task constraint, they were not graded here. The blog also
cites CTI-REALM (arXiv 2603.13517) only as the name of the benchmark
Cohere used. That is a benchmark citation, not a third-party behavior
lead, so it was not graded either.

## Method note

No code from any fetched page was run. No thread poster, author, or
operator identity was pursued. Thread content was recorded, not
people. Raw pages, provenance notes, and hashes are in
`data/lanes/cohere-qwen-enrichment/raw/leads/`.
