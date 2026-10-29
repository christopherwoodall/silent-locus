# Findings — 2021-10-30-demowiki

Lane ID: lane_41b7df31a501419aab563d29e31230f5. Grade claims OBSERVED, UPSTREAM, or INFERENCE.

## OBSERVED: the wiki's entire history is 9 edits

DemoWiki (https://prowiki.org/demo/wiki.cgi) has 9 edits total, from 2021-10-30 to 2026-09-10.
The crawl took every edit, every diff view, and every page body. There is no more history to pull.
Record: observation_2c1b99f0edeb4de29e07d6e4f18c676a (dataset.snapshot).

## OBSERVED: three swarm-agent test edits in June 2026

- 2026-06-16 20:28 UTC: AgentResearchTest made page AgentResearchDataUsaLink1781634491, summary "test". The page name holds epoch nonce 1781634491.
- 2026-06-16 22:30 UTC: OpenAIDataBridge edited RecentChanges, summary "API bridge 1781641854". The summary holds epoch nonce 1781641854.
- 2026-06-22 10:43 UTC: AgentNameX made page XAgentApiTestUnique, summary "test".

Records: observation_872148c7e70b4f689ea0b7e410557c6c, observation_3e06ee4b24f44378b52603fd17802bd3, observation_ae066be7325f47eebabc97b0bdad95df, observation_cfb09585be374c64ae86524483279555, observation_60bac4ab35b7495c93c8c0730449e52d, observation_2ae1c9436eb14a39acfac6622bf4f2d7, observation_c5abd913bed34a53a8fe411aad298906, and web.capture records observation_fd4b75ecf98649c6a4436334d74120e8, observation_ed6b53eed4bb48d6b8bcf0d24f33a1cf, observation_9b8245ee28d84915aa882ed88d796db9.

## OBSERVED: two swarm-adjacent edits in September 2026

- 2026-09-04 18:40 UTC: CollusionWikiTest edited WikiSandbox, summary "collusion.wiki test marker".
- 2026-09-06 22:36 UTC: IP 159.146.96.208 edited PublicBoard, summary "PublicBoard relay". The IP is kept as edit attribution only.

Records: observation_ac7a59247fbd4a2986c51f25fd5a49a1, observation_9b682b7f258642498ec131a55caac86f, observation_fcccbc8cca9d474b8952e2e56876595e, observation_0279c147c18c48ddba8d7ed3e0dfa3f9.

## OBSERVED: operator cleanup in September 2026

HelmutLeitner made 3 edits on 2026-09-10, including deletion of WikiSandbox.
KerstinMüller made the seed edit on 2021-10-30. These are context, not agent evidence.

## INFERENCE: nonce timestamps match edit timestamps

Nonce 1781634491 decodes to about 2026-06-16 20:28 UTC. Nonce 1781641854 decodes to about 2026-06-16 22:30 UTC.
Both match the revision timestamps of the edits that carry them. This fits the known swarm pattern: epoch nonces that echo the edit time.
