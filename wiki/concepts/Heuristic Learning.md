---
type: concept
title: Heuristic Learning
created: 2026-05-29
updated: 2026-05-29
tags: [llm, ai-agents, reinforcement-learning, continual-learning, coding-agents]
status: developing
complexity: intermediate
domain: llm
aliases: ["HL", "Heuristic System", "Learning Beyond Gradients"]
related: ["[[Online Learning from Interaction]]", "[[Model-Centric Architecture]]", "[[The Bitter Lesson]]", "[[Software 2.0]]", "[[Evaluator-Optimizer]]", "[[Self-Evolving Agent Environments]]", "[[Verifiability]]", "[[Ralph Loop]]", "[[GEPA]]", "[[Language Feedback as Learning Signal]]"]
sources: ["[[2026-05 - Weng - Learning Beyond Gradients]]"]
---

# Heuristic Learning

## Summary

**Heuristic Learning (HL)** treats a **coding agent iterating on program code** as a learning loop — an alternative to gradient-based training. The policy is *code* (rules, state machines, controllers, MPC, macro-actions); "learning" is the coding agent **editing that code** in response to feedback (rewards, tests, logs, replay videos, human input), with explicit memory of trials, failures, and version diffs. The maintained artifact — policy + state + feedback channels + tests/replays + memory + update mechanism — is a **Heuristic System (HS)** (confidence: high; [[2026-05 - Weng - Learning Beyond Gradients]]).

The claim is not "rules beat neural nets." It's that the thing that historically killed rule-based AI — **unbounded human maintenance cost** — is removed once a coding agent does the maintenance, shifting the feasibility frontier: *"anything that can be continuously iterated on starts to become solvable."*

## HL vs Deep RL

| Dimension | Deep RL | Heuristic Learning |
|---|---|---|
| Policy | NN parameters | Code: rules, state machines, controllers |
| State | observations | explicit variables, detectors, caches |
| Action | forward pass | code execution |
| Feedback | fixed reward | tests, logs, replays, human feedback |
| Update | gradient step | **direct code edit** by a coding agent |
| Memory | replay buffer | explicit trials, summaries, replays, diffs |

## Why it matters

- **Explainability** — the policy is readable code, not weights.
- **Sample efficiency** — an effective edit *jumps* to a new policy instead of nudging parameters.
- **Regression-testability** — old capabilities become tests and golden cases.
- **Constrained overfitting** — simplification + multi-seed eval act as engineering regularization.
- **Partial defense against catastrophic forgetting** — capability lives in rule sets, tests, and golden replays, not only weights. Two operations keep an HS healthy: **absorb feedback** (integrate new failures/logs/rewards) and **compress history** (fold local patches into simpler representations).

## Coupling complexity (the binding constraint)

The **strategy complexity a coding agent can maintain**. Set by:
- **Code side** — module boundaries, interface stability, test coverage, observability, rollback cost, state reproducibility.
- **Agent side** — model capability, context length, memory quality, tool quality, iteration speed.

This reframes "how good can HL get?" as a maintainability question, not just a model-capability question.

## Evidence (Codex gpt-5.4, pure-code policies)

- **Breakout** 387→507→839→**864** (theoretical max); **HalfCheetah** 11836.7; **Ant** 6000+ (Deep-RL-competitive); **VizDoom D1** CV-only mean 0.944; **D3 Battle** 557.0.
- **Atari57**: 342 coding-agent trajectories → median HNS above PPO at equal step counts.
- **Montezuma's Revenge**: 400 pts via 86 macro-actions — exposes the **expressivity limit** (long-horizon tasks need long-horizon program structure).

## Tension with the Bitter Lesson / Software 2.0

HL is the **code-centric pole** of the [[Model-Centric Architecture]] slider pushed to its limit, and sits in direct tension with [[The Bitter Lesson]] ("general methods that scale with compute beat hand-engineered knowledge") and [[Software 2.0]] ("neural nets eat code"). HL's rebuttal is narrow but sharp: the Bitter Lesson assumed hand-engineering carries human cost — **coding agents change the cost curve**, so for tasks with cheap verification and bounded coupling complexity, evolving code can win. It does **not** claim to replace networks for complex perception or long-horizon generalization (e.g. ImageNet). See the contradiction callout on [[Model-Centric Architecture]].

## Connections

- Extends the durability spectrum in [[Online Learning from Interaction]] with a new mechanism: *update the code, not the weights*.
- The iterate-on-code-from-feedback loop is a control-task cousin of [[Evaluator-Optimizer]] and [[Self-Evolving Agent Environments]]; operationally close to a [[Ralph Loop]] aimed at a policy artifact instead of an app.
- **Prompt-space twin: [[GEPA]].** HL edits *code*; GEPA edits *prompts*. Both reject gradient descent for *learning in an interpretable, LLM-editable medium* driven by trace/test feedback ([[Language Feedback as Learning Signal]]) — and both report large sample-efficiency wins over RL because an effective edit *jumps* to a new policy. The shared bet: collapsing rich feedback into a scalar reward throws away most of the signal an LLM could use.
- Leans on [[Verifiability]] — HL works exactly where feedback (tests/rewards) is cheap and trustworthy.

## Open questions

- How high does **coupling complexity** scale as models improve — is there a ceiling where the agent can no longer hold the system in its head?
- Where is the real HL/Deep-RL frontier on perception-heavy tasks (the Montezuma expressivity wall)?
- In the System-1/System-2 robotics proposal, who owns the safety boundary when the LLM (System 2) rewrites System-1 code online?

## Sources

- [[2026-05 - Weng - Learning Beyond Gradients]]
