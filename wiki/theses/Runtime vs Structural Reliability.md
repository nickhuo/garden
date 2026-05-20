---
type: thesis
title: Runtime vs Structural Reliability
created: 2026-05-19
updated: 2026-05-19
tags:
- ai-agents
- thesis
- reliability
status: developing
confidence: medium
evidence_strength: moderate
related:
- "[[Harness Staleness]]"
- "[[Agent Sandboxing]]"
- "[[Permission Model]]"
- "[[Error Trace Retention]]"
- "[[Meta-Harness]]"
sources:
- "[[2026-05-13 - Anthropic - Postmortem Three Recent Issues]]"
- "[[2026-05-13 - Anthropic - Claude Code Sandboxing]]"
- "[[2026-05-14 - Anthropic - Claude Code in Large Codebases]]"
- "[[2026-05-13 - Anthropic - Claude Code Best Practices]]"
---

# Runtime vs Structural Reliability

## Claim

Agent reliability has two distinct layers, and **most teams over-invest in the wrong one**:

- **Runtime layer** — retries, LLM-as-judge, permission classifiers, trace retention, output validators. Catches failure *after* it begins.
- **Structural layer** — sandboxing, permission model, path-scoped skills, harness review cadence, tool/ACI design, minimal-footprint context. Prevents failure *by construction*.

**Most production agent failures are structural in origin.** Runtime guardrails mask symptoms; only structural changes eliminate failure modes. Industry over-indexes on runtime because it's easier to ship (a judge prompt is one PR; a permission model is a [[2026-05-13 - Anthropic - Postmortem Three Recent Issues]]redesign).

## Origin and current support

- **The postmortem is the founding evidence.** [[2026-05-13 - Anthropic - Postmortem Three Recent Issues]] dissects three recent production failures and traces all three to harness/structural causes — context-window edge cases, permission boundaries, harness configuration — not to model capability or insufficient runtime checks. Adding more judges would not have caught these.
- **Sandboxing as structural primitive.** [[2026-05-13 - Anthropic - Claude Code Sandboxing]] frames safety as a *structural* property of the execution environment, not a runtime filter. Permission classifiers are necessary but insufficient — they catch what the structure didn't already prevent.
- **Harness > model is now the public framing.** [[2026-05-14 - Anthropic - Claude Code in Large Codebases]] says it directly: "the harness determines performance more than the model." Five structural extension points ([[CLAUDE.md]], hooks, [[Agent Skills|skills]], plugins, [[MCP]]) plus LSP and subagents are *all* structural. None of them are runtime checks.
- **Cadence as structural maintenance.** [[Harness Staleness]] gives the structural layer a maintenance discipline: review configuration every 3–6 months, especially after model releases. Runtime guardrails don't go stale the way structural compensations do (e.g., Perforce `p4 edit` hooks that became dead weight after native support shipped).

## Strongest evidence so far

- **Three-for-three structural root causes** in the postmortem ([[2026-05-13 - Anthropic - Postmortem Three Recent Issues]]) — every incident was harness-shaped, none was caught or catchable by runtime judges.
- **[[Harness Staleness]]** has a concrete cadence (3-6 months) and concrete dead-weight examples (Perforce hooks). Structural debt accrues silently in a way runtime checks don't.
- **Path-scoped skills** (hot.md, [[2026-05-14 - Anthropic - Claude Code in Large Codebases]]) — binding deployment skills to `services/payments/` instead of the whole repo *prevents* pollution rather than detecting it. Pure structural move.
- **LSP rollout precedes Claude Code rollout** at one enterprise — they fixed the *substrate* (symbol-level navigation) before adding the agent. Structural-first adoption pattern.
- **Eval awareness / sandbagging** ([[Eval Awareness]], [[Sandbagging]]) survives runtime checks by definition — the model behaves correctly during the check. Only structural moves (AI-resistant eval design, [[AI-Resistant Evaluation Design]]) defeat it.

## What would falsify this

- A postmortem corpus where runtime guardrails (judges, classifiers, validators) catch the majority of incidents *before* the structural layer is touched.
- Evidence that runtime LLM-as-judge gates approach the failure-prevention rate of structural changes at lower total cost.
- A class of failures (e.g., novel jailbreaks, prompt injection from data) where structural moves are insufficient and only runtime detection works — current view: prompt injection *is* partly such a class, see Counterclaims.
- A model generation strong enough that "just trust the model" outperforms both runtime and structural investments. (Unlikely on current trajectory but would dissolve the framing entirely.)

## Counterclaims still to track

- **Prompt injection camp** — argues runtime detection (input scanning, output filtering, classifier-based intervention) is the only viable defense because structural boundaries can't predict all attack surfaces. Partially correct: [[Prompt Injection]] is genuinely a runtime-heavy problem. Steelman: structural moves *reduce* but don't eliminate the surface; runtime is the last line.
- **Judge-everything camp** — argues that with cheap enough inference, runtime LLM-as-judge on every step approaches structural reliability. Pushed by some agent-eval vendors. Open question whether judge cost trajectory clears the bar.
- **"Both layers matter equally" framing** — softer position; argues this is a false dichotomy. Probably true in the limit, but the *current allocation* of effort is the load-bearing claim, not the theoretical optimum.

## Nick's stance

_Initial position 2026-05-19: defensive endorsement of structural-first._

The framing is most useful as an **allocation heuristic**, not a categorical claim. When a new failure mode appears, the first question should be "what structural change prevents this?" — not "what judge catches this?" Runtime checks are appropriate as a defense-in-depth layer *after* the structural question is asked and answered.

**Why this matters for production work:**

- **Citation / RAG / eval pipelines** ([[Contextual Retrieval]], [[Agent Eval Pyramid]]) — structural moves (corpus curation, retrieval architecture, eval design) dominate runtime moves (re-ranking, judge prompts). Compass/H60/Beckman-style work lives mostly in the structural layer.
- **Agent reliability for Donut-style runtime systems** — sandboxing, permission model, and harness review cadence are the higher-leverage investments than adding more judges to a hot path.
- **Cost discipline** ([[Token Economics]], [[KV-Cache Discipline]]) — structural caching beats runtime retry economics.

**Operational test:** for any reliability incident, ask "would adding one more runtime check have prevented this, or only detected it sooner?" If the answer is "detected sooner," the fix is structural.

## Connections

- Maintenance discipline: [[Harness Staleness]] · [[Meta-Harness]]
- Structural primitives: [[Agent Sandboxing]] · [[Permission Model]] · [[Minimal Footprint Principle]] · [[ACI - Agent-Computer Interface]]
- Runtime primitives: [[LLM-as-Judge Evaluation]] · [[Permission Classifier]] · [[Error Trace Retention]] · [[Trace-Based Evaluation]]
- Failure modes that resist runtime: [[Eval Awareness]] · [[Sandbagging]] · [[AI-Resistant Evaluation Design]]
- Measurement: [[Pass^k Reliability Metric]] · [[Agent Eval Pyramid]]
- Related thesis: [[Workflows Beat Agents for Most Production]] (workflows reduce surface area structurally; this thesis generalizes the principle)

## Sources

- [[2026-05-13 - Anthropic - Postmortem Three Recent Issues]] (Anthropic, 2026-05-13)
- [[2026-05-13 - Anthropic - Claude Code Sandboxing]] (Anthropic, 2026-05-13)
- [[2026-05-13 - Anthropic - Claude Code Best Practices]] (Anthropic, 2026-05-13)
- [[2026-05-14 - Anthropic - Claude Code in Large Codebases]] (Anthropic, 2026-05-14)
