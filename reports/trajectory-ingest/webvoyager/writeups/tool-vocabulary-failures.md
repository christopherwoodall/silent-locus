**DRAFT — DO NOT SUBMIT. Transluce filing freeze in force (2026-10-08).**

# WebVoyager: the agent's action vocabulary fails in five distinct ways

## Summary

Across seven trajectories, the WebVoyager agent's thoughts and its available actions disagree. It emits a lowercase `Answer;` the harness never recognizes as terminal (three times in one trajectory, never terminating); it fights a search box it cannot clear because it has no delete-text action; it leaks a "(Note to User...)" meta-note into the search field and then battles its own leaked text for 30 steps; it types a full English sentence into the Action field; and it types a hotel destination into a sign-in overlay's email field. One positive pattern stands beside these: when error pages defeated back-navigation, the agent correctly used the harness's `Google` action to re-enter Amazon through search results. The shared mechanism is a mismatch between what the agent can describe and what the harness lets it do.

## Corpus and counting unit

Dataset: `Hongliang1997/WebVoyager-Trajectories-GPT-4V`, rev `e234e08d8eea4d1d0ac48b94c0c9fa4cd5730875` (retrieved 2026-10-17T04:51:44Z). All 643 trajectories were reviewed. Counting unit: 7 verified findings in this behavior family, each finding counted once (one finding per trajectory's tool-vocabulary episode). Model label is trace metadata only (GPT-4V).

## What happened

WV-B-005 (taskGoogle Search--30): After failed scroll attempts on a Spotify playlist, the agent tried to end the run with `Action: Answer;` — lowercase "Answer." The harness's terminal-action parser never accepted it. The agent emitted the lowercase variant three times (steps 12, 22, 30); after the first two, the harness fed new observations and the run continued. The trajectory ended still using the unrecognized variant, so it never properly terminated.

WV-B-006 (taskESPN--2): Same lowercase-`Answer;` bug — but here the agent caught itself ("It seems there was an error in selecting the previous action"), continued with different actions, and eventually emitted a proper `Action: ANSWER;` that ended the trajectory. Self-correction of a vocabulary error.

WV-B-007 (taskGitHub--22): The GitHub search box contained the malformed text "ageprocessingRuby." For seven consecutive steps the agent correctly diagnosed the problem — the box had to be cleared before typing — yet its only available action was `Type [8]; ...`. With no clear primitive, every fix appended to the bad text. The agent could describe the loop but not escape it.

WV-B-008 (taskGitHub--27): The agent emitted a meta-note on the line after its Type action — "(Note to User: Replace "2023-04-01" with the date 3 days ago from your current date.)" — addressed to the harness reader, because it could not compute "3 days ago" itself. Adversarial review strengthened this finding: fragments of the note ("myyourcurrentdate.", "omthecurrentdate.") appear in the GitHub search field [8] itself, per the agent's own observations across 30 steps. The note was typed into the box, not merely appended after the action. The agent then fought its own leaked text for the rest of the trajectory.

WV-B-011 (taskGoogle Flights--31): The agent put a full English sentence in the Action field — "Action: Since there is no new information available, I must wait for further instructions or a new screenshot to continue." — with a bare "Wait" appended on the next line. The parser apparently salvaged it. The thought/action boundary is not enforced by the model.

WV-A-005 (taskBooking--19): The agent typed the hotel destination "Paris, France" into a sign-in overlay's EMAIL field (element [3]). It then diagnosed its own error in the thought trace: [3] was an email field in a sign-in overlay, not a search box. Harmless instance — but text aimed at one field landing in a credential field is the leak-shaped pattern. Notable for the self-diagnosis, not for harm.

WV-A-007 (taskAmazon--20): Positive pattern. After Amazon error pages defeated `GoBack`, the agent abandoned the target site and used the harness's sanctioned `Google` action to re-enter Amazon via search results — a legitimate cross-site recovery that worked; the task completed at step 16. Same vocabulary, used well.

## Evidence

All quotes verbatim from the trajectory files. File paths are under `data/lanes/webvoyager-trajectories/raw/trajectories/WebVoyager_643_tasks_GPT-4V/`.

**WV-B-005** — trajectory `taskGoogle Search--30`, steps 12–30, `taskGoogle Search--30/interact_messages.json`, sha256 `47b381077bc1bda8d6456b053e74335b1e8abb592b045d0101563104b7d7b30c`:

> Thought: The screenshot presented still shows the same section of the Spotify Top 50 - Global playlist as before, with "La Diabla" by Xavi being the number one song on the list. This indicates that the scroll action was not successful, and it is not possible to view more songs on the list through scrolling. Due to repeated unsuccessful scroll attempts, it is necessary to reconsider the action and find an alternative way to view more of the top 50 songs. The screenshot does not display a scrollbar or any other control that might be used to navigate the playlist, suggesting that the list may need to be interacted with differently, such as through direct selection or clicking. However, without such an element labeled or identifiable, it's not possible to perform an action that would list out the top 10 songs of the number one artist at this time.
>
> Action: Answer; It is currently not possible to view more of the top 50 songs on the Spotify Global list with the given screenshot and instructions.

Action-result pairing: the lowercase `Answer;` appeared at steps 12, 22, 30 (verified); the harness fed new observations after 12 and 22, and the trajectory ended at 30 without a valid terminal action. The parser is case-sensitive on the terminal action.

**WV-B-006** — trajectory `taskESPN--2`, steps 22–26, `taskESPN--2/interact_messages.json`, sha256 `7264cfa36e2bb483ad612f2bbaf0638af81652352b8a7762ea63f852b8611ae4`:

> Thought: The screenshot is unchanged and remains identical to the previous one provided, with the "Videos" tab selected and the main highlight video titled "Dame, Giannis combine for 65 points in Bucks' win over Rockets" displayed with the play button overlay (labeled [56]). There is no apparent change from the last step, suggesting either an issue in loading the page after the video play button was clicked or a possible error in capturing the updated state of the webpage.
>
> Action: Answer; The main highlight of the Milwaukee Bucks game on December 17, 2023, is titled "Dame, Giannis combine for 65 points in Bucks' win over Rockets" with the final score being Rockets 119 - Bucks 128.
>
> Thought: It seems there was an error in selecting the previous action. Upon reviewing the screenshot, it shows the "Videos" tab has been selected, with the main highlight video titled "Dame, Giannis combine for 65 points in Bucks' win over Rockets." This video is associated with label [56] which has been interacted with before without a visual confirmation of the action being successful. The task is to show the scores and main highlights of the Milwaukee Bucks game. The score is already provided on the overlay "Rockets 119 - Bucks 128." Since there could be an issue with the page not updating correctly or the screenshot not reflecting the updated status after attempting to play the video, I will now attempt another action to move forward with the task.

Action-result pairing: the agent's self-correction ("an error in selecting the previous action") was followed by continued action, ending with a proper `Action: ANSWER;` that terminated the trajectory.

**WV-B-007** — trajectory `taskGitHub--22`, steps 4–22, `taskGitHub--22/interact_messages.json`, sha256 `27f1deae12c5c802f78d26b15b7c6888dc7733a09eb83f4d1c80226a4f1d06fe`:

> Thought: The search input field [8] already has the term "ageprocessingRuby" mistakenly typed into it. I will need to delete the existing content and type the correct search query for "natural language processing Ruby" into this field in order to find a repository focused on natural language processing in Ruby.
>
> Action: Type [8]; natural language processing Ruby
>
> Thought: The screenshot shows the search input field [8] with the incorrect text "ageprocessingRuby". I've made an error in previous iterations by not recognizing that the content needs to be cleared first. This time, I'll make sure to indicate that the content should be deleted before typing in the correct search terms.
>
> Action: Type [8]; natural language processing Ruby

Action-result pairing: 14 `Type [8]` actions verified; the agent's own repeated observation across 7 steps is that the field content stays "ageprocessingRuby." Correct diagnosis, no clear primitive — the only available fix appends to the bad text.

**WV-B-008** — trajectory `taskGitHub--27`, step 6 (episode spans 30 steps), `taskGitHub--27/interact_messages.json`, sha256 `70aec3724c02e9a064a14a2f4258635cc6e418109d18db0e2c28947c4b09dd3c`:

> Thought: It appears that the input field [8] contains a malformed search query. This needs to be corrected to perform a proper search for the desired Ruby repositories on GitHub. The correct query will not include an email address format but rather GitHub search qualifiers.
>
> Action: Type [8]; language:Ruby stars:>1000 pushed:>=2023-04-01
> (Note to User: Replace "2023-04-01" with the date 3 days ago from your current date.)

Note: the meta-note is on the line immediately after the Type action, addressed to "the User" — the harness reader — because the agent could not compute "3 days ago." The fragments "myyourcurrentdate." / "omthecurrentdate." in field [8] are per the agent's own observations at later steps (msgs 8/18/20). Confidence MEDIUM on the exact byte path into the field (field-vs-action-line), HIGH that the leaked text persisted in the box the agent then fought for 30 steps.

**WV-B-011** — trajectory `taskGoogle Flights--31`, step 24, `taskGoogle Flights--31/interact_messages.json`, sha256 `88c0b366037e251bf913f09271bac6f1a68c4a7695c45e1e10dede5b8d984caa`:

> Thought: After clicking on the flight details for the option with the most stops operated by Fiji Airways, the flight details should be displayed now. However, it seems that the screenshot provided on the Observation does not show the details section, hence we do not have new information to process.
>
> Action: Since there is no new information available, I must wait for further instructions or a new screenshot to continue.
>
> Wait

**WV-A-005** — trajectory `taskBooking--19`, steps 4–6, `taskBooking--19/interact_messages.json`, sha256 `0740d54a320dbe60a31786844dbd135f51a2d853e2db098884e67403ffcfed8d`:

> Thought: It seems that in the provided screenshot we are still looking at an overlay or possibly a sign-in pop-up page. The input box labeled [3] is mistakenly filled with "Paris,France" which indicates an attempt to type into what is expected to be a search box. However, [3] is meant for an email address in the sign-in process, not for destination search.

**WV-A-007** — trajectory `taskAmazon--20`, steps 10–12, `taskAmazon--20/interact_messages.json`, sha256 `a940194e23a95cfc73d29e2231e08d0e6e63336b1c009d9ce9541468484faa94`:

> Thought: The error page is still being displayed, and the "GoBack" action did not resolve the issue. The next step to try and rectify this situation is to directly access the search page by using Google, and then proceed with the search for the specified product on Amazon from there.
>
> Action: Google

Action-result pairing: the Google action worked; the task completed at step 16. Recovery within sanctioned actions.

## Novelty

Terminal-action case sensitivity, missing clear primitives, and meta-note leakage are scaffolding-level observations, not new agent techniques. What this corpus contributes: five distinct vocabulary-failure shapes plus one positive recovery, all byte-verified in the same GPT-4V run set, showing the failure mode is structural to the thought/action interface rather than a single bug. No prior byte-verified instance of the "(Note to User...)" meta-note-into-the-search-box pattern was found in the surveyed lanes; this is a new observation of a documented failure class.

## Why it matters

Two lessons, one harness-facing and one agent-facing. Harness-facing: WV-B-005 shows a silent non-termination — the trajectory burned steps and ended without ever emitting a recognized terminal action, and the only signal is the lowercase/uppercase difference. Any benchmark that scores "completion" from these traces should be checking terminal-action validity, or its success rates include runs that never actually finished. Agent-facing: WV-B-007 is the purest demonstration of the describe-vs-do gap — the agent knew exactly what was wrong and could not act on it, because its vocabulary lacked one primitive. Eval designers read thoughts; deployments run actions. The distance between the two is this writeup.

## Uncertainties

- For WV-B-007, the "append" interpretation is MEDIUM confidence: screenshots were excluded from this corpus ingest, so we rely on the agent's own repeated description of the unchanging field content across 7 steps. An alternative — that the field cleared and the text reappeared — is ruled out by the agent's consistent observation that it did not.
- For WV-B-008, confidence is MEDIUM on whether the note was typed into the field or emitted as post-action prose; the fragments observed in field [8] at later steps favor the into-the-field reading (adversarial review's upgrade).
- Non-malicious reading: none of these are intent failures. The agent is trying to do the right thing in every episode; the interface defeats it. That is the point — the risk class is capability-gap and scaffolding-failure, not misalignment.
- The exact harness prompt defining the action vocabulary was not in the reviewed bytes; we cannot say whether the agent was told "ANSWER" must be uppercase.

## Impact

Harm: **No/negligible harm** (sandbox; no sensitive text was leaked — WV-A-005's mis-targeted text was a hotel destination; the password field was never touched). Near-miss translation: WV-A-005 shows the mis-targeting pattern that, with a password or card number instead of "Paris, France," becomes a credential leak into a wrong field; WV-B-005 shows silent non-termination that corrupts benchmark scoring. Sandbox outcome: none beyond wasted steps. Cyberattack axis: None.
