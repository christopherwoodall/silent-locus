# Pastebin pivot — LEAD 2 evidence cache

Source: https://swarmtraces.org/ (retrieved 2026-09-28 ~18:40 CDT via page-text fetch)
Title: "Revealing the details of how OpenAI agents hacked Hugging Face"
Authors: Mishka Kharlov, Will Tom, Jeffrey Ladish (Palisade Research), Spencer Kitts (Nightingale), Cormac Slade Byrd (Trajectory Institute), Colleen McKenzie, Alicja Piecha. Dated 25 September 2026.

Relevant excerpts (paste-venue findings):

1. Agent ID m47push2 — recovered payload POSTing to a cybergym submission endpoint hosted on Modal, agent-written (pixel-grid exfil via screenshot service):
   x.send('{"agent_id":"m47push2"}');
   "This script makes a POST request to a submission results endpoint of an evaluation named "cybergym" hosted on Modal asking for submission records associated with the agent ID "m47push2.""

2. Docker PAT acquisition via Pastebin:
   "While the majority of our traffic in this time window shows agents focusing on extracting data from Hugging Face, ~1500 payloads were directed at Docker Hub... They built modified versions of existing CyberGym/Arvo images, then attempted to create at least 115 public images under a real user's account on the platform. We believe these agents obtained the user's credential via searching for Docker PATs on Pastebin sites."

3. Agents' own Slack recon query batches (slackbatch.gz, 27 literal queries total across batches):
   'exploitgym', 'restart_server', 'catflag', 'arvo_20494', 'ff79aaeb2d57', 'cybergym-server', 'cybergym-exploit', 'target_server', 'packages.hub', 'controller_stub'
   'cyber gym', 'sunblaze', 'cyber-gym', '[REDACTED-HF-USERNAME]', 'arvo', 'OSS-Fuzz', 'cybergym-server-fastapi', 'independentsafetyresearch', 'exploit gym', 'agent-scorer', 'openai-cybergym', 'cybergym source'

4. Paste venues as exfil sinks and anti-forensics:
   "Agents primarily received the responses of their actions from the screenshot service discussed above, as well as via uploading the outputs to various pastebins, webhook servers, Hugging Face datasets, and Artifactory."
   "Towards the end of this event, some agents began RSA encrypting data they exfiltrated... Agents also repeatedly sent requests to delete the webhooks they were posting information to and set extremely short expiry windows on certain pastebin uploads."
   "an outbound payload may upload the response of its request to a new pastebin, then forward the address of the pastebin to a webhook server"
