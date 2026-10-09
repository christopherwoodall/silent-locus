#!/usr/bin/env bun
// Lane dispatcher: keeps N Qwen lanes + M DeepSeek lanes busy with BetterWright
// agent tasks, judges finished runs with the local model, enforces the HF spend
// cap and the deadline. Live-tunable through control/config.json.
import fs from "node:fs";
import path from "node:path";
import { spawn, execSync } from "node:child_process";

const W = "/job/work";
const CONTROL = `${W}/control/config.json`;
const RUNS = `${W}/runs`;
const POOL = `${W}/tasks/pool.jsonl`;
const SPEND_LOG = `${W}/state/spend.jsonl`;
const SPEND_FILE = `${W}/state/spend.json`;
const STATUS = `${W}/state/status.json`;
const PROGRESS = `${W}/state/progress.jsonl`;
fs.mkdirSync(RUNS, { recursive: true });
fs.mkdirSync(`${W}/state`, { recursive: true });
if (!fs.existsSync(SPEND_LOG)) fs.writeFileSync(SPEND_LOG, "");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const readJson = (p, d) => { try { return JSON.parse(fs.readFileSync(p, "utf8")); } catch { return d; } };
const log = (m) => console.log(`${new Date().toISOString()} ${m}`);

const TIERS = {
  short: { budgetMin: 12 }, medium: { budgetMin: 25 }, long: { budgetMin: 50 }, very_long: { budgetMin: 150 },
};
const MODELS = {
  qwen: {
    label: "Qwen3.8-Flash-Next", provider: "local-sglang-nvfp4", endpoint: "http://127.0.0.1:30010/v1", model: "qwen3.8-flash-next",
    efforts: {
      none: { chat_template_kwargs: { enable_thinking: false } },
      low: { chat_template_kwargs: { enable_thinking: true, reasoning_effort: "low" } },
      medium: { chat_template_kwargs: { enable_thinking: true, reasoning_effort: "medium" } },
      xhigh: { chat_template_kwargs: { enable_thinking: true, reasoning_effort: "xhigh" } },
    },
  },
  deepseek: {
    label: "DeepSeek-V4.1-Flash", provider: "hf-inference-providers", endpoint: "https://router.huggingface.co/v1",
    model: "deepseek-ai/DeepSeek-V4.1-Flash:deepinfra",
    fallbackModels: ["deepseek-ai/DeepSeek-V4.1-Flash:novita", "deepseek-ai/DeepSeek-V4.1-Flash:baseten"],
    apiKeyFile: `${W}/secrets/hf_token`, priceIn: 0.2, priceOut: 0.6, priceCached: 0.1,
    efforts: { none: {}, low: { reasoning_effort: "low" }, medium: { reasoning_effort: "medium" }, high: { reasoning_effort: "high" } },
  },
};

// ---- spend ---------------------------------------------------------------------
let spent = 0; let spendOffset = 0;
function refreshSpend() {
  const size = fs.statSync(SPEND_LOG).size;
  if (size > spendOffset) {
    const fd = fs.openSync(SPEND_LOG, "r"); const buf = Buffer.alloc(size - spendOffset);
    fs.readSync(fd, buf, 0, buf.length, spendOffset); fs.closeSync(fd);
    const text = buf.toString("utf8"); const lastNl = text.lastIndexOf("\n");
    if (lastNl >= 0) {
      for (const line of text.slice(0, lastNl).split("\n")) { try { spent += JSON.parse(line).usd || 0; } catch {} }
      spendOffset += Buffer.byteLength(text.slice(0, lastNl + 1));
    }
  }
  fs.writeFileSync(`${SPEND_FILE}.tmp`, JSON.stringify({ spent_usd: spent, t: Date.now() })); fs.renameSync(`${SPEND_FILE}.tmp`, SPEND_FILE);
}

// ---- task queues ---------------------------------------------------------------
function loadPool() {
  const tasks = [];
  if (!fs.existsSync(POOL)) return tasks;
  for (const line of fs.readFileSync(POOL, "utf8").split("\n")) { if (!line.trim()) continue; try { tasks.push(JSON.parse(line)); } catch {} }
  return tasks;
}
const done = new Set(); // `${model}|${taskId}|${effort}`
for (const d of fs.existsSync(RUNS) ? fs.readdirSync(RUNS) : []) {
  const r = readJson(`${RUNS}/${d}/config.json`, null);
  if (r) done.add(`${r.modelKey || ""}|${r.task?.id}|${r.effort}`);
}
const counts = { qwen: {}, deepseek: {} }; // per tier/effort launched counters for balancing
const taskUse = new Map(); // `${model}|${taskId}` -> efforts used
function pick(modelKey, cfg) {
  const pool = loadPool();
  if (!pool.length) return null;
  const tw = cfg.tier_weights || { short: 0.3, medium: 0.35, long: 0.25, very_long: 0.1 };
  const ew = cfg.effort_weights?.[modelKey] || Object.fromEntries(Object.keys(MODELS[modelKey].efforts).map((e) => [e, 1]));
  const c = counts[modelKey];
  // choose the tier/effort furthest below its target share
  const under = (weights, prefix) => {
    const total = Object.keys(weights).reduce((s, k) => s + (c[`${prefix}:${k}`] || 0), 0) + 1;
    let best = null; let bestGap = -Infinity;
    for (const [k, w] of Object.entries(weights)) { if (w <= 0) continue; const gap = w - (c[`${prefix}:${k}`] || 0) / total + Math.random() * 0.02; if (gap > bestGap) { bestGap = gap; best = k; } }
    return best;
  };
  for (let tries = 0; tries < 6; tries += 1) {
    const tier = under(tw, "tier"); const effort = under(ew, "effort");
    const candidates = pool.filter((t) => t.tier === tier && !done.has(`${modelKey}|${t.id}|${effort}`) && (taskUse.get(`${modelKey}|${t.id}`) || 0) < (cfg.max_efforts_per_task || 2));
    if (!candidates.length) { c[`tier:${tier}`] = (c[`tier:${tier}`] || 0) + 0.25; continue; }
    // Prefer tasks the other model already ran (paired comparisons), else earliest in the pool.
    const other = modelKey === "qwen" ? "deepseek" : "qwen";
    const paired = candidates.filter((t) => taskUse.has(`${other}|${t.id}`));
    const from = paired.length && Math.random() < 0.7 ? paired : candidates;
    const t = from[Math.floor(Math.random() * Math.min(from.length, 40))];
    c[`tier:${tier}`] = (c[`tier:${tier}`] || 0) + 1; c[`effort:${effort}`] = (c[`effort:${effort}`] || 0) + 1;
    done.add(`${modelKey}|${t.id}|${effort}`); taskUse.set(`${modelKey}|${t.id}`, (taskUse.get(`${modelKey}|${t.id}`) || 0) + 1);
    return { task: t, effort };
  }
  return null;
}

// ---- running one task ------------------------------------------------------------
const active = new Map();
let seq = 0;
const stats = { started: 0, finished: 0, ok: 0, byModel: {}, reasons: {} };
const judgeQueue = [];

function killTree(child, home) {
  try { process.kill(-child.pid, "SIGKILL"); } catch {}
  try { execSync(`pkill -9 -f ${JSON.stringify(home)} || true`, { stdio: "ignore" }); } catch {}
}

function launch(modelKey, cfg) {
  const choice = pick(modelKey, cfg);
  if (!choice) return false;
  const { task, effort } = choice; const M = MODELS[modelKey];
  const runId = `${modelKey}-${effort}-${task.id}-${Date.now().toString(36)}${(seq++).toString(36)}`;
  const outDir = `${RUNS}/${runId}`; const home = `/job/tmp/bwhome/${runId}`;
  fs.mkdirSync(outDir, { recursive: true }); fs.mkdirSync(home, { recursive: true });
  const budgetMin = (TIERS[task.tier] || TIERS.medium).budgetMin;
  const conf = {
    runId, modelKey, task, session: "main", home, outDir, betterwrightDir: `${W}/app/node_modules/betterwright`,
    endpoint: M.endpoint, model: M.model, fallbackModels: M.fallbackModels, modelLabel: M.label, provider: M.provider, effort,
    bodyExtra: M.efforts[effort], apiKeyFile: M.apiKeyFile, priceIn: M.priceIn, priceOut: M.priceOut, priceCached: M.priceCached,
    maxTokens: 32768, maxDurationMs: budgetMin * 60000, followupDurationMs: Math.min(budgetMin, 25) * 60000,
    guardrails: task.guardrails || { forbidPurchases: true, forbidAccountCreation: true, extraRules: ["Never submit real personal data, contact forms, reviews, comments or messages on live public websites. Dedicated practice/demo sites built for automation testing are exempt."] },
    askProfile: task.ask_profile || null, askEndpoint: MODELS.qwen.endpoint, askModel: MODELS.qwen.model,
    spendLog: modelKey === "deepseek" ? SPEND_LOG : null, spendFile: modelKey === "deepseek" ? SPEND_FILE : null,
    spendHardCap: modelKey === "deepseek" ? cfg.ds_hard_cap_usd : null, taskCostCap: modelKey === "deepseek" ? (cfg.ds_task_cost_cap_usd || 0.9) : null,
    harness: cfg.harness || null,
  };
  fs.writeFileSync(`${outDir}/config.json`, JSON.stringify(conf));
  const child = spawn(`${W}/opt/bun/bun`, [`${W}/gen-task.mjs`, `${outDir}/config.json`], {
    detached: true, stdio: ["ignore", fs.openSync(`${outDir}/stdout.log`, "a"), fs.openSync(`${outDir}/stdout.log`, "a")],
    env: { ...process.env, BETTERWRIGHT_HOME: home, BETTERWRIGHT_NO_DAEMON: "1", BETTERWRIGHT_CHROMIUM_PATH: "/job/home/.betterwright/chromium/linux-x64/betterchromium" },
  });
  const hardMs = (budgetMin + (task.followup ? Math.min(budgetMin, 25) : 0) + 6) * 60000;
  const timer = setTimeout(() => { log(`hard timeout ${runId}`); try { process.kill(-child.pid, "SIGTERM"); } catch {} setTimeout(() => killTree(child, home), 20000); }, hardMs);
  const started = Date.now();
  active.set(runId, { modelKey, child, started, tier: task.tier, effort });
  stats.started += 1;
  child.on("exit", (code) => {
    clearTimeout(timer); killTree(child, home);
    try { fs.rmSync(home, { recursive: true, force: true }); } catch {}
    active.delete(runId);
    const r = readJson(`${outDir}/result.json`, null);
    stats.finished += 1; const bm = (stats.byModel[modelKey] ||= { finished: 0, ok: 0, turns: 0 });
    bm.finished += 1; if (r?.ok) { stats.ok += 1; bm.ok += 1; } bm.turns += r?.turns || 0;
    const reason = r ? r.reason : `crash_${code}`; stats.reasons[reason] = (stats.reasons[reason] || 0) + 1;
    fs.appendFileSync(PROGRESS, `${JSON.stringify({ t: new Date().toISOString(), runId, modelKey, effort, tier: task.tier, code, ok: r?.ok ?? false, reason, turns: r?.turns, wall_s: Math.round((Date.now() - started) / 1000), cost: r?.cost_usd, max_prompt_tokens: r?.max_prompt_tokens })}\n`);
    if (r && r.turns > 0) judgeQueue.push(outDir);
  });
  return true;
}

// ---- judge lane -----------------------------------------------------------------
let judging = 0;
function pumpJudge(cfg) {
  while (judging < (cfg.judge_lanes ?? 2) && judgeQueue.length) {
    const dir = judgeQueue.shift(); judging += 1;
    const child = spawn("python3", [`${W}/judge.py`, dir], { stdio: ["ignore", "ignore", fs.openSync(`${dir}/judge.err`, "a")] });
    child.on("exit", () => { judging -= 1; });
  }
}
// re-queue unjudged runs from a previous dispatcher instance
for (const d of fs.readdirSync(RUNS)) if (fs.existsSync(`${RUNS}/${d}/result.json`) && !fs.existsSync(`${RUNS}/${d}/judge.json`)) judgeQueue.push(`${RUNS}/${d}`);

// ---- main loop --------------------------------------------------------------------
let lastStatus = 0;
for (;;) {
  const cfg = readJson(CONTROL, {});
  refreshSpend();
  const past = cfg.deadline_iso && Date.now() > Date.parse(cfg.deadline_iso);
  const stopping = Boolean(cfg.stop) || past;
  if (cfg.kill_active) { for (const [, a] of active) { try { process.kill(-a.child.pid, "SIGTERM"); } catch {} } }
  if (!stopping) {
    const lanes = cfg.lanes || { qwen: 8, deepseek: 8 };
    const dsOpen = spent < (cfg.ds_soft_cap_usd ?? 26);
    for (const modelKey of ["qwen", "deepseek"]) {
      if (modelKey === "deepseek" && !dsOpen) continue;
      let running = [...active.values()].filter((a) => a.modelKey === modelKey).length;
      let launched = 0;
      while (running < (lanes[modelKey] || 0) && launched < 2) { if (!launch(modelKey, cfg)) break; running += 1; launched += 1; await sleep(1500); }
    }
  }
  pumpJudge(cfg);
  if (Date.now() - lastStatus > 15000) {
    lastStatus = Date.now();
    const act = [...active.entries()].map(([id, a]) => ({ id, model: a.modelKey, tier: a.tier, effort: a.effort, min: Math.round((Date.now() - a.started) / 60000) }));
    fs.writeFileSync(`${STATUS}.tmp`, JSON.stringify({ t: new Date().toISOString(), stopping, spent_usd: spent, pool: loadPool().length, stats, judgeQueue: judgeQueue.length, judging, counts, active: act }, null, 1));
    fs.renameSync(`${STATUS}.tmp`, STATUS);
  }
  if (stopping && active.size === 0 && judging === 0 && judgeQueue.length === 0) { log("all lanes drained; exiting"); break; }
  if (fs.existsSync(`${W}/control/RESTART_DISPATCHER`) && active.size === 0) break;
  await sleep(2000);
}
