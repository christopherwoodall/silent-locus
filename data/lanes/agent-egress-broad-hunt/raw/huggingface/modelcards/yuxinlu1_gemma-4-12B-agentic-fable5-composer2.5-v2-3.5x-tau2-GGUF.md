---
license: apache-2.0
base_model: google/gemma-4-12B-it
library_name: gguf
pipeline_tag: text-generation
tags: [gemma4, coding, agentic, terminal, tool-use, reasoning, thinking, gguf, llama.cpp, local-llm]
---

# 💻🤖 Gemma4-12B **v2** — Coding + Agentic Edition ✨
### 🐣 Tiny footprint, big brain — a local **coding & tool-using agent** for *everyone*

> **No matter your GPU. No matter your RAM.** With **~4.5 GB** of VRAM *or* unified memory free, you can run your own
> private, offline coding **agent** right now. 🚀 v2 is the big **agentic** upgrade — it reads, reasons, *uses tools*,
> and works through multi-step technical tasks before it acts. 🧠🛠️ All local, all yours, no API, no cloud.

---

## 📊 The headline — it works as an agent (tau2-bench)

v2 is built for **coding + agentic** work — writing code, running commands, using tools, debugging, multi-step
technical tasks. The clearest signal is **tau2-bench `telecom`**, an agentic tool-use benchmark whose
*diagnose → fix → verify* loop mirrors real terminal/debugging work:

| tau2-bench **telecom** · 20 tasks · local, same harness, **all Q8_0** | score |
|---|---|
| official `gemma-4-12B-it` (base) | **~15%** |
| 🟢 **Gemma4-12B v2 (this model)** | **~55%** |

→ Roughly **3.5× higher** than the base model on technical-agentic tasks. 🎯 **Want the full story** — *why* telecom,
*how* the two models fail differently, the honest caveats, and the trade-offs (including general knowledge)?
**It's all broken down further below. 👇**

---

## 🚀 Announcements

**📌 Hitting a problem? Please check my pinned discussion first.** **~99% of issues are a client/sampler config, not
the weights** — and they have a quick fix there. For example: garbled or **repeating `0000…`** output almost always
means **no repetition penalty** (set `rep_pen 1.1`, `temp 1.0`); and leaked `<|tool_call>` / `<|channel>` tokens mean
your front-end isn't parsing Gemma 4's **native tool format** (use llama.cpp `--jinja`). If your question isn't covered,
**don't hesitate to open a discussion** — I read them and reply as fast as I can. 💬

**📦 No Q2_K this release.** I finished a Q2_K (imatrix) build, but it didn't hold up under real stress-testing, so I'm
holding it back — **I only ship a quant once I'm confident it's genuinely good.** Smallest reliable option is
**Q3_K_M**; **Q4_K_M** is the recommended sweet spot. 🙏

**🔮 v3 is already on the way.** Honestly? Even *I* didn't expect the post-training jump to be **this** large — so I'm
pushing further. v3 keeps the **coding + agentic** focus and aims higher still. Stay tuned! 🎉

**🐘 And a bigger sibling is coming — Qwen3.6-27B.** I've also started fine-tuning **Qwen3.6-27B** with the same
**coding + agentic** recipe, for those of you who *do* have the headroom and want more raw capability. But I haven't
forgotten what this project is about: a **27B may be too heavy** for some of your GPUs / RAM. So this is **not** a
replacement — I'm pushing **v3 (this 12B line) in parallel, at the same time**, and it will **only get stronger**. 💪
**No matter your hardware, you'll have a model that fits.** 💚

---

## 💚 A personal note — thank you, and a few honest words (please read)

**First, a huge thank-you for all the data and help you've shared.** 🙏 The bittersweet part: none of us saw it coming
that **Fable 5 would be retired** — and only my *own* dataset holds Fable 5's **genuine, self-authored** chain-of-thought.
So for every dataset the community contributed, I **rebuilt the missing reasoning from scratch with Opus 4.8 (xhigh)**.
It may diverge from the original Fable 5 traces, but it was the only workable path — and the **improvement turned out
really, *really* huge** (it nearly launched me out of my chair 😄). The benchmark numbers are right above. 👆

**Second** — I've tried to **reply to every community comment**, and I've openly **owned v1's training problems**. Truly,
thank you: your feedback is what lets me improve. 💚

Because v1 hit **#1 trending**, it also attracted some **bad words / trolling**. I'll say this gently but firmly: **real
criticism is always welcome here — pure insults are not.** This is a **local** model that lets anyone run a capable AI on
tiny RAM/VRAM, at **zero API cost** and fully **private**; I even open-sourced the **full safetensors master** to study
and build on. If something's off, **open a discussion about the actual problem** — I genuinely want to hear it and I'll
act on it. But comments that are *only* insults help no one, and I'll remove them without hesitation. 🙏

Please remember: **I'm one person** — not a lab shipping an "open" model for marketing or to monetize later. I don't
advertise. I build this for you on **my own time and my own money**: synthesizing data, reviewing and cleaning it by
hand, splitting and re-segmenting it (this round I even built a **dynamic context-window** pass to keep the agent's
*read-before-act* steps intact), reading the latest papers, then training → evaluating → training → evaluating. It
burned through an **entire Claude Max 20× plan** (I keep a separate Pro for my own work), and **v2 alone cost 40+ hours**
— even with Opus 4.8, the data threw constant curveballs I had to verify myself. Thank you, truly. 🐾

---

## 🔬 The benchmarks, in detail (tau2-bench)

I evaluated v2 on **tau2-bench** (an agentic tool-use benchmark). I did **not** run the whole suite — it's very
time-consuming — so I focused on the single domain that best matches what v2 is for.

**Why tau2-bench `telecom`?** Telecom troubleshooting makes the agent **diagnose with read/inspect tools → pinpoint the
issue → apply a fix → verify it** — structurally the *same loop* as real terminal/debugging work
(*check state → diagnose → fix → confirm*). That's exactly what this model is meant to be good at, which makes it the
right yardstick for v2 (much more so than a shopping/customer-service domain).

| tau2-bench **telecom** · 20 tasks · local, same harness, **all Q8_0** | score |
|---|---|
| official `gemma-4-12B-it` (base) | **~15%** |
| 🟢 **Gemma4-12B v2 (this model)** | **~55%** |

→ Roughly **3.5× higher** than the base model on technical-agentic tasks. 🎯

**Grounded, not made-up.** Independently, a coding/terminal *fabrication probe* (tasks that deliberately tempt the
model to invent file paths / function signatures / values) found v2 **grounds before it acts** just like the base —
it `grep`/`read`/`ls` first, and **doesn't make things up** (0% fabrication, on par with the base model).

**The interesting part — *how* they fail.** The **base model gives up early**: on this run it bailed to a human agent
**10 times** (`transfer_to_human`) instead of finishing the fix. **v2 keeps going** — it stays in the loop and works the
problem the way a much bigger model would, which is exactly why it solves so many more. It's not perfect yet: it still
**flails a little sometimes** (over-trying, retrying). And some of the remaining misses are actually a **bug in the
benchmark's own APN tool** (it throws on inputs it should handle gracefully), not the model. To be clear: **I will not
patch the benchmark's tools or leak its test questions just to inflate my score** — I'd rather report an honest number
and improve the *model* itself. **More training is coming in v3.** 🔧

**About `retail` (customer-service shopping):** on tau2-bench *retail*, the base model scores a bit higher than v2. **This
is fully expected and by design.** Retail is pure customer-service (look up a user, process an order) — *not* what this
model is for. v2 is specialized for **coding / terminal / technical-agentic** work, and on those (telecom) it
dramatically outperforms the base. Need a customer-service bot? This isn't it. Need a **local coding/agentic** model?
It is. 💚

**Let's keep it honest about scale.** Today's *frontier* models — think **mimo-v2.5-pro** or **Opus 4.8** — all land
**90%+** on this telecom benchmark. They're also *enormous*. For a **12B** model, my rough *guess* is that v3 might top
out somewhere around **60–70%** (emphasis on *guess* — I haven't even started v3 yet). So let's be clear-eyed: there's
still a real gap to the frontier. But keep the scale in mind — **this is a 12B model running on your own machine**, and
narrowing that gap as much as possible *at this size* is the whole point. 💪

**And the trade-off — there's no free lunch.** I also ran a general-knowledge benchmark (**MMLU-Pro**), and v2 lands
**a little below the base model** there. That's **completely normal and expected** for a focused fine-tune: when you
push hard on coding + agentic, you trade a sliver of broad-knowledge breadth for it. Need a generalist? Try my own
general-purpose **[Claude Opus 4.6/4.8 distillation](https://huggingface.co/yuxinlu1/gemma-4-12B-it-Claude-4.6-4.8-Opus-GGUF)**
— or the original **`google/gemma-4-12B-it`** base. Need a **local coding/agentic** worker? That's what v2 is tuned for.

> 🔬 *Methodology, honestly:* these are **local, same-harness, relative** numbers (**all models tested at Q8_0**, greedy
> decoding, self-simulated user, 20 tasks). They are **not** directly comparable to published tau2-bench leaderboard
> figures (different user-simulator, full task sets, full precision) — local self-eval runs *systematically lower* than
> published scores. Read them as **"v2 vs the base model under identical conditions"**, which is the comparison that
> actually matters here.

---

## 📚 What's new in v2 (training)

v2 continues from the v1 coder and adds a big **agentic** push — the piece v1 was missing:

- **🛠️ Agentic / terminal** — real **multi-step tool-use** trajectories (*read → reason → act → verify*), in Gemma 4's
  native tool protocol. This is what drove the tau2-bench telecom jump, and it fixes v1's "stops after the first step"
  behavior.
- **💻 Coding** — verified chain-of-thought over Python tasks (**real CoT, gated on passing tests**) plus the
  Fable-5-redo set for the hard cases.
- **📚 General** — a curated slice of reasoning/instruction data to keep broad competence.

All reasoning is **distilled CoT** (see the personal note above on how the Fable 5 traces were rebuilt with Opus 4.8).

---

## 📦 Pick your size (GGUF quants)

| Quant | Size | Vibe |
|------|------|------|
| 🟡 **Q3_K_M** | **5.7 GB** | great for 8 GB VRAM |
| 🔵 **Q4_K_M** | **6.87 GB** | the sweet spot 👌 (recommended) |
| 🟣 **Q6_K** | **9.11 GB** | near-lossless |
| ⚪ **Q8_0** | **11.8 GB** | basically full quality |

> ℹ️ *No **Q2_K** this release — it didn't pass stress-testing yet (see Announcements). Smallest reliable quant = **Q3_K_M**.*

---

## 🚀 How to run it

### Option A — llama.cpp (recommended) 🦙
> ⚠️ Needs a **recent llama.cpp** (this is the `gemma4_unified` architecture — older builds won't load it).

```bat
@echo off
cd /d C:\llama.cpp
llama-server.exe ^
  -m C:\models\gemma4-v2-Q4_K_M.gguf ^
  --ctx-size 16384 ^
  --n-gpu-layers 99 ^
  --no-mmap -fa on ^
  --jinja ^
  --temp 1.0 --top-p 0.95 --top-k 64 ^
  --host 0.0.0.0 --port 18080
pause
```

- **🛠️ Agentic use:** pass your tools via the OpenAI `tools` field (works with `--jinja`). v2 emits structured
  tool-calls in Gemma 4's native protocol and is happy in agent loops (read/grep/edit/run, then verify).
- **🖱️ One-click apps:** LM Studio / Jan / Ollama — import the GGUF, pick a quant, go.

### 🧠 Thinking mode
v2 thinks in Gemma's native thought channel before answering (keep `enable_thinking=true`, the default chat template
handles it). Recommended sampling: `temp 1.0, top_p 0.95, top_k 64`; for coding you can also go greedy (`temp 0`).

---

## ⚠️ Good to know
- **Specialized for coding / terminal / agentic.** General-knowledge facts/numbers should still be double-checked.
- **Reduced refusals:** task-focused training, not safety-aligned — add your own guardrails for production. Use
  responsibly. 🙏
- English-centric.

---

## 📚 Base & License
- **License: Apache 2.0.** Gemma 4 is released by Google under
  **[Apache 2.0](https://ai.google.dev/gemma/apache_2)** (unlike the older Gemma 1/2/3 terms), so this fine-tune is
  **Apache 2.0** too — free to use, modify, and redistribute. 🎉
- **Base model:** [`google/gemma-4-12B-it`](https://huggingface.co/google/gemma-4-12B-it).
- Personal/hobby project — shared as-is, no warranty. Built with time, care, and a lot of coffee. Have fun! 🐾✨

---

## ⚡ Speculative decoding (MTP draft) — verified build

The `MTP/` folder ships the Gemma 4 multi-token-prediction draft (unsloth's GGUF conversion of Google's official
`gemma-4-12B-it-assistant`) for speculative decoding. Gemma 4 MTP is in **llama.cpp mainline** (PR #23398) — no fork
needed — but the `gemma4-assistant` loader is **build-sensitive right now**, so please use the exact build below:

- ✅ **Verified working: llama.cpp `b9553` (commit `9e3b928fd`).** I reproduced it with `gemma4-v2-Q8_0` + the
  `MTP-Q8_0` draft: loads cleanly and accelerates generation (~88 → ~180 tok/s on a simple deterministic prompt;
  expect ~1.2–1.3× on real coding/thinking). **Lossless** either way.
- ⚠️ **Newer builds (e.g. b9702 / b9717) currently crash** while loading the draft with `invalid vector subscript`.
  This is an **upstream regression** in the `gemma4-assistant` loader path, *not* a problem with these GGUFs — the same
  files load fine on b9553. Stick with **b9553** until it's fixed upstream.

Working command on b9553 (note the older flag names — `--model-draft`, **not** `--spec-draft-model`):

```bat
llama-server -m gemma4-v2-Q8_0.gguf ^
  --model-draft MTP\gemma-4-12B-it-MTP-Q8_0.gguf ^
  --spec-type draft-mtp --spec-draft-n-max 4 ^
  -ngl 99 -ngld 99 -fa on --jinja
```

> ℹ️ The `Gemma4Assistant requires ctx_other to be set (this is normal during memory fitting)` line is harmless. The
> draft is the generic Gemma 4 assistant (not retrained for v2), so acceptance is a touch lower than a model-specific
> draft would give — still 100% lossless. On small-VRAM cards, Q8 main + long context + the draft can be tight; drop to
> Q6_K/Q4_K_M or a smaller `--ctx-size` if you hit OOM.
