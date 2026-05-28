---
type: concept
title: "User Simulator Evaluation"
created: 2026-05-13
updated: 2026-05-13
tags:
- ai-agents
- evaluation
- methodology
- dialogue
status: developing
related:
- "[[Pass^k Reliability Metric]]"
- "[[tau-bench]]"
- "[[LLM-as-Judge]]"
- "[[Few-Shot Drift]]"
sources:
- "[[2024-06-17 - Yao et al - tau-bench]]"
- "[[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]]"
---

# User Simulator Evaluation

## Summary

Use a language model to **play the human user** in closed-loop agent evaluation. The simulator gets a system prompt describing the user's identity, intent, and preferences; it generates natural-language turns in response to the agent; it can request, accept, reject, and clarify; it stops the episode when it judges the task complete (or with a sentinel like `###STOP###`).

This replaces the two prior approaches: (1) static pre-recorded dialogue transcripts (cheap but trajectory-locked), and (2) crowdsourced human-in-the-loop testing (faithful but slow and expensive and inconsistent across runs).

[[2024-06-17 - Yao et al - tau-bench]] uses `gpt-4-0613` as the user simulator at temperature 1.0, with the agent at temperature 0.0.

## Why it matters

Agent evaluation has historically been **trajectory-graded**: did the agent follow the right script? That fails for two reasons:

1. **Multiple valid trajectories exist** to the same goal. Penalizing the agent for taking a different path is brittle and conservative.
2. **Real users are stochastic.** They phrase requests differently, omit info, add irrelevant context, change their mind. A trajectory-graded eval can't expose how the agent handles that diversity.

User simulators surface conversational robustness as a measurable axis. Combined with [[Pass^k Reliability Metric]] across multiple trials of the same scenario, you get a reliability signal that static datasets fundamentally cannot produce.

## Design constraints

- **Unique outcome under policy.** Scenario instructions must be constructed so that only one valid database state can result. Otherwise the user can "agree" to different paths and the deterministic reward becomes ambiguous. τ-bench iterates each scenario manually against a trial agent until ambiguity is closed.
- **Stop condition.** Either a sentinel token, a max-turn cutoff, or both.
- **Simulator-info asymmetry.** The user does NOT see the agent's tool calls or internal reasoning — only the agent's user-facing messages. This mirrors deployment.
- **Capacity floor.** If the user simulator is weaker than the agent, evaluation underestimates agent capability (the user becomes the failure mode). gpt-4-0613 was deliberately chosen as a strong simulator.

## Failure modes of the simulator itself

τ-bench identifies three:

1. Simulator typos / ambiguities in the instruction (~4/115 cases in retail; manually fixed).
2. Simulator missing domain knowledge — the simulated user authorizes an action that violates a rule, because realistic users *don't know* the rules. This is a **feature**, not a bug; deployed agents face the same reality.
3. Simulator reasoning limits — long-context, calculation, alignment with own instructions. Improves with model capacity.

## Connections

- Composes with [[Pass^k Reliability Metric]] — the simulator is the entropy source that makes pass^k informative.
- Contrast with [[LLM-as-Judge]] — judge scores *agent output*; simulator generates *user input*. They sit at opposite ends of the closed loop.
- Avoids the trajectory-grading trap discussed in [[Autonomous Agents]] open questions.
- The simulator is a controlled instance of [[Few-Shot Drift]] — natural-language variation is the thing being measured rather than suppressed.

## Open questions

- Can a smaller, fine-tuned simulator match gpt-4 quality? Eval cost is dominated by the simulator at >50% of total in τ-bench.
- How does simulator-agent same-model self-play bias (gpt-4 evaluating gpt-4) shift results vs cross-family simulation?
- For domains where unique-outcome construction is hard (open-ended research, coding), is there a relaxation that preserves deterministic reward?

## Sources

- [[2024-06-17 - Yao et al - tau-bench]] (Yao, Shinn, Razavi, Narasimhan, Sierra 2024)
- [[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]] (Anthropic, 2026-05-13) — reaffirms as Tier 3 in [[Agent Eval Pyramid]]; adds explicit info-asymmetry constraint (simulator does not see agent tool calls)
