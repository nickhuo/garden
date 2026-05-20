---
type: concept
title: Programmatic Tool Calling
created: 2026-05-10
updated: 2026-05-13
tags:
- ai-agents
- tool-design
- code-execution
- orchestration
- context
status: developing
related: []
sources:
- "[[2026-05-13 - Anthropic - Code Execution with MCP]]"
- "[[2025-10 - Zhang Khattab - Recursive Language Models]]"
- "[[2026-05-13 - Anthropic - Writing Effective Tools for Agents]]"
- "[[2025-11-24 - Anthropic - Advanced Tool Use]]"
aliases:
- PTC
- Code-as-Orchestration
- Code Mode
- Code Execution as Orchestration
_legacy_source_count: 2
---

# Programmatic Tool Calling

## Summary

A cross-vendor pattern (Anthropic's name for it, but instances precede): instead of the model **calling tools sequentially through inference** — one tool per turn, results in context, reason, call next — the model writes **code** that calls multiple tools, processes their results in a sandboxed code-execution environment, and returns only the final reduction to the model's context.

Two simultaneous wins: **intermediate results never pollute context** (so attention budget and dollars are preserved) and **fewer inference passes** are needed (so latency drops). Anthropic claims a 37% token reduction (43,588 → 27,297) and meaningful accuracy gains on tasks requiring multi-tool composition (GAIA 46.5→51.2%).

## The pattern (model-agnostic)

1. Define some tools as **callable from code** (Anthropic's syntax: `allowed_callers: ["code_execution_20250825"]`).
2. Model writes a code block (Anthropic uses Python; the principle works for any sandboxed runtime).
3. Sandbox executes; when the code calls an opt-in tool, the orchestration layer surfaces a tool request out-of-band (with a `caller` field indicating it came from code).
4. The tool result returns to the sandbox, not to the model's context.
5. Sandbox completes; only its final output (e.g., `stdout`) enters the model's context.

The conceptual move: **the agent's tool orchestration logic lives in code, not in natural language**. Loops, conditionals, parallelism (`asyncio.gather`), data transformations, error handling — all become explicit and inspectable.

## Why this works structurally

Two failure modes of traditional tool calling, both addressed simultaneously:

- **Context pollution from intermediate results.** Loading 2,000 expense line items into context to compute who exceeded budget is wasteful — the model only needs the final answer (2-3 names). Code can reduce locally and return only the reduction.
- **Inference overhead from natural-language orchestration.** A 5-tool workflow with 5 inference passes is 5× the latency of one code block that issues 5 tool calls (potentially in parallel) within a single inference cycle.

The reduction in inference passes also reduces compounding error: each natural-language tool-result-to-next-call step is a chance to mis-parse, mis-reason, or hallucinate. Code is unambiguous.

## Cross-vendor instances (the pattern, not just Anthropic's product)

Anthropic explicitly cites prior art as inspiration:

| Instance | Vendor / Author | Notes |
|---|---|---|
| **PTC** (`allowed_callers`) | Anthropic Claude Developer Platform | Productized Nov 2025 |
| **Code Mode** | Cloudflare | Cited as inspiration; uses code as the agent's primary action surface |
| **LLMVM** | Joel Pobar | Open-source / personal-project precursor cited in acknowledgements |
| **Code Execution as MCP** | Anthropic | [[2026-05-13 - Anthropic - Code Execution with MCP]] — dedicated post showing MCP server authors how to embed code execution inside MCP tool definitions; extends PTC into MCP ecosystem |

The pattern is converging across vendors because it solves a structural problem (orchestration latency + context pollution) that pure function-calling can't.

## Sister concept: [[Recursive Language Models]] (Zhang & Khattab 2025-10)

Same primitive (sandboxed Python REPL the LM writes code into), **different object**:

| | PTC | [[Recursive Language Models]] (RLM) |
|---|---|---|
| What the code orchestrates | **Tool calls** (external side-effects) | **Context processing** (peek, grep, partition, summarize) |
| What enters context after exec | Final tool-result reduction | Final RLM call result (or sub-call distillations) |
| Recursive sub-calls? | No (tools are leaf operations) | **Yes** (sub-LM calls inside the REPL are first-class) |
| Primary failure mode addressed | Intermediate tool-result pollution | Long-context "context rot" |
| Decomposition axis | Problem (tool orchestration is task structure) | **Context** — see [[Context Decomposition vs Problem Decomposition]] |

Both authors cite **CodeAct** as inspiration; both explicitly distinguish from it. PTC views code as the agent's *action* surface; RLM views code as the agent's *understanding* surface over the context object. Composable in principle: an RLM root could call PTC-style tool-orchestrating code blocks inside its REPL, or a PTC code block could embed an RLM sub-call when context-processing is the bottleneck.

The two posts (Anthropic Nov 2025, Zhang+Khattab Oct 2025) are independent and roughly contemporaneous — neither cites the other. Convergent evolution toward "sandboxed REPL as the canonical agent-LM primitive."

## Reported impact (Anthropic internal)

| Metric | Traditional | PTC | Delta |
|---|---|---|---|
| Avg tokens on complex research tasks | 43,588 | 27,297 | -37% |
| Internal knowledge retrieval accuracy | 25.6% | 28.5% | +2.9 pts |
| GAIA benchmark | 46.5% | 51.2% | +4.7 pts |

The token reduction is more dramatic in extreme cases — Anthropic's budget-compliance example reduces from ~200KB of raw expense data to ~1KB of result (~200×). The flagship internal product is **Claude for Excel**, which uses PTC to read/modify spreadsheets with thousands of rows without overflowing context.

## When this wins

- Large datasets where you only need aggregates / summaries (the canonical case)
- Multi-step workflows with 3+ dependent tool calls (orchestration savings dominate)
- Filtering / sorting / transforming tool outputs before the model sees them
- Tasks where intermediate data **should not** influence model reasoning (security, cleanliness)
- Parallel ops across many items (the `asyncio.gather` case — 50 endpoints checked in one shot)

## When it doesn't

- Single-tool invocations (overhead of code-execution setup not worth it)
- Tasks where the model needs to **see and reason about** intermediate results
- Quick lookups with small responses
- Tools that aren't safe to call from arbitrary code (auth-sensitive, side-effecting)

## ACI implications

PTC reshapes what a tool definition is. With code-as-orchestration:

- Tool docs need to specify **return formats precisely** (data shape, units, error structure) so the model can write correct parsing code
- Idempotent / safely-retryable operations become more valuable (code retries are cheap, model re-invocations are expensive)
- Tools that compose well (return data the code can fan-out across) outperform monolithic do-everything tools

See [[ACI - Agent-Computer Interface]].

## Tension with [[Logit Masking]] — different layer, no direct contradiction

Manus's static-action-space + masking approach is about *which tool to pick at the next decoding step*. PTC is about *who orchestrates the calls — model inference or sandboxed code*. These are orthogonal: a code-orchestrated agent could in principle still use Manus-style decoding constraints when it does inference. But in practice, PTC reduces the frequency of inference-time tool selection (more calls happen inside the code block), so the value of decoding-time masking falls accordingly. Worth a future synthesis pass — see [[Static Action Spaces vs Dynamic Tool Discovery]] for the related tool-discovery tension.

## Connections

- Sister concept (same primitive, different object): [[Recursive Language Models]] (context decomposition via REPL + recursive sub-LM calls)
- Sister concept: [[Tool Search Tool]] (Tool Search reduces context cost of *unused* tools; PTC reduces context cost of *intermediate results*)
- Operationalizes: [[Context Engineering]] (orthogonal context-pollution remedy at result layer)
- Builds on: [[ACI - Agent-Computer Interface]] (tool docs become parsing targets for code, not just selection targets)
- Reduces: dollar cost in [[Token Economics]] (37% on Anthropic's number); also reduces inference-pass count
- Substrate: sandboxed code execution environment (Anthropic's Code Execution tool; analogues in Manus's VM sandbox)
- Decomposition axis: problem-decomposition (see [[Context Decomposition vs Problem Decomposition]])
- Prior art: LLMVM (Joel Pobar), Cloudflare Code Mode, Code Execution as MCP, CodeAct (also cited by RLM as inspiration)

## MCP extension (per Anthropic 2026-05-13)

[[2026-05-13 - Anthropic - Code Execution with MCP]] extends PTC into the MCP server layer. The same pattern — model writes code, sandbox executes, only result enters context — now lives inside MCP tool definitions rather than at the Claude API platform level. This makes the pattern available to any MCP-compatible client, not just Claude API users.

Key additions from this post:
- **MCP servers as compute endpoints**: bundle data-access tools + code execution tool together in the server
- **New ACI authoring requirement**: MCP tool descriptions must document available Python libraries so the model can write correct import statements
- **Structured error returns**: sandbox errors should be returned as strings, not raised exceptions
- **Stateless sandbox design**: per-session isolation; explicit state passing required across turns
- **Composability confirmed**: code execution MCP tool can be `defer_loading: true` in Tool Search configs, giving both efficiency layers (tool-def reduction + result reduction) simultaneously

## Open questions

- Cost story — Code Execution is itself a billed tool. What's the net cost story vs traditional tool calling for medium-complexity workflows? Anthropic doesn't publish.
- Error handling — when a code block fails midway, what enters context? The error or a sanitized version? Compatibility with [[Error Trace Retention]] partially addressed (structured errors), but agent recovery patterns unclear.
- Security — code that calls external tools is a security surface (path traversal, credential exfil, etc.). MCP-embedded code execution increases attack surface vs platform-sandboxed PTC.
- Composability with [[Tool Search Tool]] — confirmed in principle; no concrete code example in the post.
- Reentrancy — what happens when a code execution tool inside MCP calls another MCP tool that itself embeds code execution? Not addressed.
- Long-tail effect — does PTC encourage **macro-tools** (high-level "do the analysis" tools) that internally call multiple primitives, vs the current trend of small composable tools? The orchestration burden moves from prompt to code regardless.

## Return-format precision doubly load-bearing (per Anthropic 2026-05 writing guide)

[[2026-05-13 - Anthropic - Writing Effective Tools for Agents]] confirms and extends the ACI implication: tool return formats are now load-bearing in two directions simultaneously — (1) for code parsing in PTC, and (2) for agent recovery from errors. The writing guide's "design errors before success cases" principle applies especially to PTC tools, since a code block failure mid-run is harder to recover from than a single-inference-step tool error.

## Sources

- [[2025-11-24 - Anthropic - Advanced Tool Use]] (Anthropic, 2025-11-24)
- [[2025-10 - Zhang Khattab - Recursive Language Models]] (Zhang & Khattab, 2025-10)
- [[2026-05-13 - Anthropic - Code Execution with MCP]] (Anthropic, 2026-05-13)
- [[2026-05-13 - Anthropic - Writing Effective Tools for Agents]] (Anthropic, 2026-05-13)
