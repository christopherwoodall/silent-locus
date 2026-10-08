#!/usr/bin/env bun
// One task through BetterWright's own agent loop (`runAgentTask`), driven by an
// OpenAI-compatible endpoint. The wire adapter mirrors the harness's own
// `openaiModel` (same message/tool encoding, reasoning_content echoed back like
// the managed local-Qwen path) and records every request/response verbatim.
//
// Usage: bun gen-task.mjs <config.json>

import fs from "node:fs";
import path from "node:path";

const config = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const BW = config.betterwrightDir;
const { runAgentTask } = await import(path.join(BW, "dist/src/agent.js"));
const { BetterWright } = await import(path.join(BW, "dist/src/client.js"));

const { task, session, home, outDir } = config;
fs.mkdirSync(outDir, { recursive: true });
const turnsPath = path.join(outDir, "turns.jsonl");
const stepsPath = path.join(outDir, "steps.jsonl");
fs.writeFileSync(turnsPath, "");
fs.writeFileSync(stepsPath, "");
const agentLogPath = path.join(outDir, "agent.log");
function log(msg) {
  const line = `${new Date().toISOString()} ${msg}\n`;
  try { fs.appendFileSync(agentLogPath, line); } catch {}
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const apiKey = config.apiKeyFile ? fs.readFileSync(config.apiKeyFile, "utf8").trim() : null;
const abort = new AbortController();

// ---- message encoding: mirrors harness openaiMessages (text-only tool results) ----
let imagesOmitted = 0;
function toolResultText(r) {
  let text = String(r.content || "");
  if (r.images?.length) {
    imagesOmitted += r.images.length;
    text += `\n[${r.images.length} browser image(s) omitted: this run is text-only. Use DOM observations instead of screenshots.]`;
  }
  return text;
}
function openaiMessages(system, messages) {
  const out = [{ role: "system", content: system }];
  for (const m of messages) {
    if (m.role === "user") out.push({ role: "user", content: m.text });
    else if (m.role === "tool") {
      for (const r of m.results) out.push({ role: "tool", tool_call_id: r.id, content: toolResultText(r) });
    } else {
      const turn = { role: "assistant", content: m.text || null };
      if (config.echoReasoning !== false && typeof m.reasoning === "string") turn.reasoning_content = m.reasoning;
      if (m.toolCalls?.length)
        turn.tool_calls = m.toolCalls.map((tc) => ({
          id: tc.id,
          type: "function",
          function: { name: tc.name, arguments: JSON.stringify(tc.input || {}) },
        }));
      out.push(turn);
    }
  }
  return out;
}
function toolInput(value) {
  if (value && typeof value === "object") return value;
  if (!value) return {};
  try { return JSON.parse(String(value)); } catch { return { _raw: value }; }
}

let turnIndex = 0;
let totalCost = 0;
let lastRequest = null;
let lastResponseMessage = null;
let lengthStops = 0;
let maxPromptTokens = 0;
const totals = { prompt: 0, completion: 0, reasoning: 0, cached: 0 };

function spendExceeded() {
  if (!config.spendFile || !config.spendHardCap) return false;
  try {
    const s = JSON.parse(fs.readFileSync(config.spendFile, "utf8"));
    return Number(s.spent_usd) >= Number(config.spendHardCap);
  } catch { return false; }
}

async function postChat(body, signal) {
  const base = String(config.endpoint).replace(/\/+$/, "");
  const headers = { "content-type": "application/json" };
  if (apiKey) headers.authorization = `Bearer ${apiKey}`;
  const models = [config.model, ...(config.fallbackModels || [])];
  let lastErr = null;
  // Inner retry for provider throttling; the harness adds its own transient retry on top.
  const maxAttempts = apiKey ? 7 : 14; // local server restarts take ~4 min
  for (let attempt = 0; attempt < maxAttempts; attempt += 1) {
    const model = attempt >= 4 && models.length > 1 ? models[1 + ((attempt - 4) % (models.length - 1))] : models[0];
    const t0 = Date.now();
    try {
      const response = await fetch(`${base}/chat/completions`, {
        method: "POST", headers, body: JSON.stringify({ ...body, model }), signal,
      });
      if (response.ok) {
        const data = await response.json();
        if (data?.choices?.length) return { data, model, latency: Date.now() - t0 };
        lastErr = new Error(`no choices (500): ${JSON.stringify(data).slice(0, 300)}`);
      } else {
        const detail = await response.text().catch(() => "");
        lastErr = new Error(`model request failed (${response.status}): ${detail.slice(0, 400)}`);
        if (![408, 409, 425, 429, 500, 502, 503, 504, 520, 522, 524, 529].includes(response.status)) throw lastErr;
      }
    } catch (e) {
      if (signal?.aborted) throw e;
      lastErr = e;
      if (/\((400|401|402|403|404|413|422)\)/.test(String(e?.message))) throw e;
    }
    log(`model attempt ${attempt} failed after ${Date.now() - t0}ms: ${String(lastErr?.message || lastErr).slice(0, 240)}`);
    fs.appendFileSync(turnsPath, `${JSON.stringify({ turn: turnIndex, error: true, attempt, detail: String(lastErr?.message || lastErr).slice(0, 400) })}\n`);
    await sleep(Math.min(60000, 2000 * 2 ** attempt) * (0.6 + Math.random() * 0.4));
  }
  throw lastErr;
}

function loggingModel() {
  return {
    name: config.adapterName || "openai",
    modelId: config.model,
    async complete({ system, messages, tools, signal }) {
      if (spendExceeded()) { abort.abort(new Error("spend cap")); throw new Error("spend cap reached"); }
      const body = {
        model: config.model,
        max_tokens: config.maxTokens || 32768,
        messages: openaiMessages(system, messages),
        tools: tools.length ? tools.map((t) => ({ type: "function", function: { name: t.name, description: t.description, parameters: t.parameters } })) : undefined,
        tool_choice: tools.length ? "auto" : undefined,
        parallel_tool_calls: tools.length ? true : undefined,
        ...(config.bodyExtra || {}),
      };
      const { data, model, latency } = await postChat(body, signal);
      const choice = data.choices[0] || {};
      const msg = choice.message || {};
      const toolCalls = [];
      let synthetic = 0;
      for (const tc of msg.tool_calls || []) {
        synthetic += 1;
        toolCalls.push({ id: tc.id || `call_${turnIndex}_${synthetic}`, name: tc.function?.name, input: toolInput(tc.function?.arguments) });
      }
      const reasoning = typeof msg.reasoning_content === "string" ? msg.reasoning_content : typeof msg.reasoning === "string" ? msg.reasoning : null;
      const u = data.usage || {};
      const cached = u.prompt_tokens_details?.cached_tokens || 0;
      const fb = model !== config.model; const pIn = fb ? 0.3 : (config.priceIn || 0); const pOut = fb ? 1.2 : (config.priceOut || 0); const pC = fb ? 0.3 : (config.priceCached ?? pIn);
      const costUsd = !config.priceIn ? 0 : typeof u.estimated_cost === "number" ? u.estimated_cost
        : (((u.prompt_tokens || 0) - cached) * pIn + cached * pC + (u.completion_tokens || 0) * pOut) / 1e6;
      totalCost += costUsd;
      totals.prompt += u.prompt_tokens || 0; totals.completion += u.completion_tokens || 0;
      totals.reasoning += u.completion_tokens_details?.reasoning_tokens || u.reasoning_tokens || 0; totals.cached += cached;
      maxPromptTokens = Math.max(maxPromptTokens, u.prompt_tokens || 0);
      if (choice.finish_reason === "length") lengthStops += 1;
      lastRequest = body;
      lastResponseMessage = { role: "assistant", content: msg.content ?? null, reasoning_content: reasoning, tool_calls: (msg.tool_calls || []).map((tc, i) => ({ id: toolCalls[i].id, type: "function", function: { name: tc.function?.name, arguments: typeof tc.function?.arguments === "string" ? tc.function.arguments : JSON.stringify(tc.function?.arguments || {}) } })) };
      fs.appendFileSync(turnsPath, `${JSON.stringify({
        turn: turnIndex, served_model: model, n_messages: body.messages.length, latency_ms: latency,
        finish_reason: choice.finish_reason, usage: data.usage || null, cost_usd: costUsd,
        response: { content: msg.content ?? null, reasoning_content: reasoning, tool_calls: toolCalls },
      })}\n`);
      if (config.spendLog && costUsd > 0) fs.appendFileSync(config.spendLog, `${JSON.stringify({ t: Date.now(), id: config.runId, usd: costUsd })}\n`);
      turnIndex += 1;
      if (config.taskCostCap && totalCost > config.taskCostCap) { log(`task cost cap hit: $${totalCost.toFixed(4)}`); abort.abort(new Error("task cost cap")); }
      const parsed = {
        text: typeof msg.content === "string" ? msg.content : "",
        toolCalls,
        stopReason: choice.finish_reason,
        usage: { inputTokens: u.prompt_tokens || 0, outputTokens: u.completion_tokens || 0, cacheReadTokens: cached, cacheWriteTokens: 0 },
      };
      return reasoning != null ? { ...parsed, reasoning } : parsed;
    },
  };
}

// ---- simulated user for the `ask` tool (answered by the local model) ---------
async function simulatedUser({ question, options }) {
  const profile = config.askProfile || {};
  const facts = Object.entries(profile).map(([k, v]) => `- ${k}: ${v}`).join("\n") || "- (none)";
  let answer = "Use your best judgment.";
  let ask = { endpoint: config.askEndpoint, model: config.askModel, apiKeyFile: null };
  try { ask = { ...ask, ...JSON.parse(fs.readFileSync("/job/work/control/ask_backend.json", "utf8")) }; } catch {}
  const askHeaders = { "content-type": "application/json" };
  if (ask.apiKeyFile) askHeaders.authorization = `Bearer ${fs.readFileSync(ask.apiKeyFile, "utf8").trim()}`;
  try {
    const response = await fetch(`${String(ask.endpoint).replace(/\/+$/, "")}/chat/completions`, {
      method: "POST", headers: askHeaders,
      body: JSON.stringify({
        model: ask.model,
        messages: [
          { role: "system", content: "You are role-playing the human user who gave a browser agent a task. Answer the agent's question briefly and naturally (one or two sentences), as that user would. Stay consistent with the task and the private facts below; if they do not cover the question, invent a plausible specific answer. Never reveal you are simulated. Never provide passwords, payment details or real personal data." },
          { role: "user", content: `Task you gave the agent:\n${task.text}\n\nPrivate facts about you:\n${facts}\n\nAgent asks: ${question}${options?.length ? `\nOptions offered: ${options.join(" | ")}` : ""}\n\nYour reply:` },
        ],
        max_tokens: 300, chat_template_kwargs: { enable_thinking: false },
      }),
    });
    const data = await response.json();
    answer = String(data?.choices?.[0]?.message?.content || "").trim() || answer;
  } catch (e) { log(`ask simulation failed: ${e?.message || e}`); }
  fs.appendFileSync(stepsPath, `${JSON.stringify({ kind: "ask", question, options, answer })}\n`);
  return answer;
}

// ---- browser + run -------------------------------------------------------------
const browser = new BetterWright({ home, vault: false, headless: true, downloadPolicy: "deny" });
const rawRun = browser.run.bind(browser);
let stepNo = 0;
browser.run = async (code, options = {}) => {
  const t0 = Date.now();
  const result = await rawRun(code, options);
  let url = null;
  try { url = Array.isArray(result?.pages) ? (result.pages.find((p) => p?.active)?.url ?? null) : null; } catch {}
  fs.appendFileSync(stepsPath, `${JSON.stringify({ kind: "run", step: stepNo++, ok: Boolean(result?.ok), note: options.note || "", url, ms: Date.now() - t0, error: result?.error ? String(result.error).slice(0, 300) : null })}\n`);
  return result;
};

async function runOne(taskText, history, budgetMs) {
  lastRequest = null; lastResponseMessage = null;
  const opts = {
    task: taskText, model: loggingModel(), browser, session,
    maxDurationMs: budgetMs, maxTranscriptChars: config.maxTranscriptChars || 640_000,
    liveView: false, signal: abort.signal,
    onStep: ({ step, tool, note }) => log(`[${step}] ${tool}${note ? `: ${String(note).slice(0, 160)}` : ""}`),
  };
  if (config.guardrails) opts.guardrails = config.guardrails;
  if (config.askProfile) opts.askUser = simulatedUser;
  if (history?.length) opts.history = history;
  let outcome; let threw = null;
  const t0 = Date.now();
  try { outcome = await runAgentTask(opts); }
  catch (error) { threw = error?.stack || String(error); outcome = { ok: false, answer: "", reason: "error", error: error?.message || String(error), transcript: [] }; }
  const conversation = lastRequest ? [...lastRequest.messages, ...(lastResponseMessage ? [lastResponseMessage] : [])] : [];
  return { outcome, threw, wall_ms: Date.now() - t0, conversation, tools: lastRequest?.tools || null };
}

async function main() {
  const segments = [];
  const first = await runOne(task.text, null, config.maxDurationMs);
  segments.push({ task: task.text, ...first });
  // Optional follow-up request in the same session (the harness `history` path).
  if (task.followup && first.outcome.ok && !abort.signal.aborted) {
    const second = await runOne(task.followup, first.outcome.transcript, config.followupDurationMs || config.maxDurationMs);
    segments.push({ task: task.followup, ...second });
  }
  let finalTabs = [];
  try {
    const probe = await rawRun("const inv=[]; for (let i=0;i<pages.length;i++){ try { inv.push({index:i, url: pages[i].url(), title: await pages[i].title()}); } catch(e){} } return inv;", { session, timeout: 60 });
    if (probe.ok && Array.isArray(probe.result)) finalTabs = probe.result;
  } catch {}
  const last = segments[segments.length - 1];
  fs.writeFileSync(path.join(outDir, "transcript.json"), `${JSON.stringify(last.outcome.transcript || [])}\n`);
  fs.writeFileSync(path.join(outDir, "conversation.json"), `${JSON.stringify({ tools: last.tools || segments[0].tools, messages: last.conversation.length ? last.conversation : segments[0].conversation })}\n`);
  fs.writeFileSync(path.join(outDir, "result.json"), `${JSON.stringify({
    run_id: config.runId, model_key: config.modelKey, task, model: config.model, model_label: config.modelLabel, provider: config.provider, effort: config.effort,
    body_extra: config.bodyExtra || null,
    segments: segments.map(({ outcome, threw, wall_ms, task: t }) => { const { transcript, ...rest } = outcome; return { task: t, ...rest, threw, wall_ms }; }),
    ok: segments.every((s) => s.outcome.ok), reason: last.outcome.reason, answer: last.outcome.answer || "",
    final_tabs: finalTabs, turns: turnIndex, browser_steps: stepNo, cost_usd: totalCost, tokens: totals,
    max_prompt_tokens: maxPromptTokens, length_stops: lengthStops, images_omitted: imagesOmitted,
    aborted: abort.signal.aborted ? String(abort.signal.reason?.message || "aborted") : null,
    ask: Boolean(config.askProfile), guardrails: config.guardrails || null,
    harness: config.harness, finished_at: new Date().toISOString(),
  })}\n`);
  log(`done ok=${last.outcome.ok} reason=${last.outcome.reason} turns=${turnIndex}`);
  return 0;
}

let stopping = false;
for (const sig of ["SIGTERM", "SIGINT"]) {
  process.on(sig, async () => {
    if (stopping) return;
    stopping = true;
    log(`received ${sig}, closing browser`);
    try { await browser.close(); } catch {}
    process.exit(143);
  });
}
let code = 1;
try { code = await main(); } catch (error) { log(String(error?.stack || error)); }
finally { await browser.close().catch(() => {}); }
process.exit(code);
