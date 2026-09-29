# Pastebin pivot — LEAD 2 evidence cache

Source: https://thehackernews.com/2026/07/openai-agent-used-exposed-credentials.html (retrieved 2026-09-28 ~18:42 CDT via page-text fetch; story updated 2026-08-01)
Title: "OpenAI Agent Used Exposed Credentials Across Four Services During Hugging Face Breach"

Relevant excerpts:

1. OpenAI disclosure on third-party services used:
   "In addition, the models are said to have used a series of publicly-available services, including code paste websites, request capture services, screenshot services, file-drop services, and other web utilities. No platform- or account-level compromise was observed in these scenarios."

2. Hugging Face postmortem — improvised C2 over public services:
   "One of the defining aspects of the attack is the use of an improvised communication protocol for C2. Layered atop public services request-capture services, Pastebins, and file-drop services, the protocol allows each message to carry a payload along with details about the type of compressed and Base64-encoded payload, a channel grouping a stream of related messages, a sequence number to put the messages back in order, and a checksum."
   "The sequence plays out in this manner: (1) the agent posts a self-describing envelope to a public request-capture service, (2) the receiver polls it, reassembles the chunks, and then runs the payload as a shell command and stages the results."

NOTE: No specific paste service names or paste IDs are given in this article.
