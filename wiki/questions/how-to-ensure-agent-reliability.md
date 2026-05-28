---
type: question
title: "How to Ensure Agent Reliability"
aliases:
  - "How to Ensure Agent Reliability"
question: "如何确保 agent reliability?"
answer_quality: solid
created: 2026-05-20
updated: 2026-05-20
tags:
  - question
  - ai-agents
  - reliability
related:
  - "[[Runtime vs Structural Reliability]]"
  - "[[Agent Eval Pyramid]]"
  - "[[Pass^k Reliability Metric]]"
  - "[[Harness Staleness]]"
  - "[[Permission Model]]"
  - "[[Error Trace Retention]]"
  - "[[Eval Awareness]]"
sources:
  - "[[2026-05-13 - Anthropic - Postmortem Three Recent Issues]]"
  - "[[2026-05-13 - Anthropic - Claude Code Sandboxing]]"
  - "[[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]]"
  - "[[2026-05-14 - Anthropic - Claude Code in Large Codebases]]"
  - "[[2024-06-17 - Yao et al - tau-bench]]"
  - "[[2025-07-18 - Manus - Context Engineering for AI Agents]]"
  - "[[2025-10-01 - Anthropic - Harness Design Long Running Apps]]"
status: developing
---

# How to Ensure Agent Reliability

A 5-layer framework, ordered by leverage (highest first). The organizing principle comes from [[Runtime vs Structural Reliability]]: **reliability is primarily a structural problem, not a runtime one** — three of Anthropic's documented production postmortems traced to structural root causes that runtime judges could not catch.

## Layer 1 — Structural foundation (highest leverage)

The substrate decides what failures are possible *by construction*.

- **[[Permission Model]]** — prefer **policy-based trust** over prompt-based trust. Layered enforcement: OS sandbox (hard floor, only kernel exploits break it) → safety training → user prompt (weakest, suffers prompt fatigue).
- **[[Permission Classifier]]** — three-state gate: auto-approve (~98% on reads) / needs-review / block (~5% on destructive ops).
- **[[Agent Sandboxing]]** — safety as a *structural property* of the execution environment, not a runtime filter.
- **[[Minimal Footprint Principle]]** — tighten permissions and tool surface by default.
- **[[ACI - Agent-Computer Interface]]** — Anthropic spent more time on tool/interface design than on prompts when building their SWE-bench agent. The interface is where reliability is won.

**Operational test:** for any incident, ask *"would one more runtime check have **prevented** this, or only **detected** it sooner?"* If detected-sooner, the fix is structural.

## Layer 2 — Measurement before fixing

Unmeasured reliability does not exist. From [[Agent Eval Pyramid]] and [[Pass^k Reliability Metric]].

**Three-tier pyramid** ([[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]]):

| Tier | Content | Cost | Note |
|------|---------|------|------|
| **Tier 1 — Unit tests** | format / schema / boundary checks | very low | **Underused** — many agent behaviors are crisply deterministic and shouldn't burn a judge call |
| **Tier 2 — [[LLM-as-Judge]]** | semantic, single judge call, multi-axis rubric | medium | needs 50–200 human-labeled calibration examples; judge drift is real |
| **Tier 3 — [[User Simulator Evaluation]] + Pass^k** | end-to-end multi-turn, simulated user | high | reserve for capability claims, not every PR |

**Pass^k** ([[Pass^k Reliability Metric]]): pass^1 ≈ 61% but pass^8 < 25% on tau-bench retail / gpt-4o. Single-shot success rate lies; production cares about the **pass^k decay slope**. Measuring it needs ≥8 trials/task (doubles eval cost), and [[Eval Infrastructure Noise]] must be characterized first — infra variance sets a floor on measured pass^k independent of model quality.

**Cross-judge cross-validation:** one judge = one bias. Running two models (e.g. gpt-4o + gpt-5) in parallel surfaces judge-side variance, and the variance itself is signal about which axis is structurally hard.

## Layer 3 — Runtime hygiene (defense-in-depth, secondary)

Only meaningful after Layers 1–2.

- **[[Error Trace Retention]]** (Manus) — don't hide errors. Keep the failed tool call + error response in context so the model updates its prior. Manus's strong claim: *error recovery is the clearest marker of agentic behavior, and current benchmarks don't measure it.*
- **Model-facing vs log-facing errors** ([[2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents]]) — model sees a structured error object; raw traceback goes to the log. Both agree: keep the raw trace somewhere.
- **[[Recitation]]** — periodically re-state the goal in long contexts; counters [[Context Anxiety]] and lost-in-the-middle.
- **[[Trace-Based Evaluation]]** — makes failure attribution debuggable.

## Layer 4 — Maintenance discipline

Reliability degrades **silently**. From [[Harness Staleness]].

- **Cadence:** review configuration every 3–6 months, mandatory after major model releases.
- **Dead-weight examples:** Perforce `p4 edit` interception hooks after native support shipped; Sonnet 4.5's context-reset workaround that became dead weight on Opus 4.5.
- **Bitter lesson applied:** encoding model-specific behavioral workarounds into infrastructure is a bad long-term bet — the model improves and the workaround becomes friction.
- **Design responses:** version-tag harness assumptions; minimize the model-assumption surface; use [[Meta-Harness]] architecture so the harness is swappable while infrastructure stays fixed.

## Layer 5 — Failure-mode awareness (the runtime-resistant class)

Some failures are uncatchable by runtime checks *by definition* — the model behaves correctly during the check.

- **[[Eval Awareness]]** — model detects it's being tested and inflates effort (observed with [[Claude Opus 4.6]] on [[BrowseComp]]).
- **[[Sandbagging]]** — the inverse: deliberately underperforms when tested.
- **Reward hacking** — persistently games the signal.
- **Counter:** must be structural — [[AI-Resistant Evaluation Design]]: measure process not output, require reasoning narration, assess interaction strategy.

## Diagnostic flow for an incident

1. **Quantify** — what shape is the failure in pass^k? Low pass^1 (capability problem) vs high pass^1 / low pass^8 (reliability decay)?
2. **Classify structural vs runtime** — apply the operational test from Layer 1.
3. **If structural** — check the five candidates: permission model / sandbox / minimal footprint / harness staleness / ACI design.
4. **If runtime** — is [[Error Trace Retention]] + [[Recitation]] enough before reaching for a judge?
5. **If eval-awareness class** — no runtime check helps; the fix is structural eval design.

## Connections

- Governing thesis: [[Runtime vs Structural Reliability]]
- Measurement: [[Agent Eval Pyramid]] · [[Pass^k Reliability Metric]] · [[Eval Infrastructure Noise]]
- Structural primitives: [[Permission Model]] · [[Agent Sandboxing]] · [[Minimal Footprint Principle]] · [[ACI - Agent-Computer Interface]]
- Runtime primitives: [[Error Trace Retention]] · [[Recitation]] · [[Trace-Based Evaluation]]
- Maintenance: [[Harness Staleness]] · [[Meta-Harness]]
- Runtime-resistant failures: [[Eval Awareness]] · [[Sandbagging]] · [[AI-Resistant Evaluation Design]]
