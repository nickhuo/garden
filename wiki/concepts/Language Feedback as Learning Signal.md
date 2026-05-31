---
type: concept
title: Language Feedback as Learning Signal
created: 2026-05-30
updated: 2026-05-30
tags: [llm, ai-agents, prompt-optimization, reinforcement-learning, continual-learning]
status: developing
complexity: intermediate
domain: llm
aliases: ["Textual Feedback", "Reflection over Reward", "feedback function"]
related: ["[[GEPA]]", "[[Heuristic Learning]]", "[[Verifiability]]", "[[Reward Modeling]]", "[[Trace-Based Evaluation]]", "[[Error Trace Retention]]", "[[GRPO]]"]
sources: ["[[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]]"]
---

# Language Feedback as Learning Signal

The principle that **natural-language feedback is a richer learning medium for LLMs than a scalar reward**. RL with verifiable rewards (RLVR, e.g. [[GRPO]]) collapses an entire rollout into one number; but the rollout was already serializable into language — instructions, reasoning, tool calls, and the reward function's own internals (compiler errors, failed rubrics) *before* they become a scalar. Reflecting on that language exploits LLMs' strong language priors and extracts far more signal per rollout ([[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]]).

## Two trace types

- **Execution trace** — what the LLM produces (reasoning, tool calls, intermediate outputs). Carries *diagnostic* value: pair it with the final outcome to do **implicit credit assignment** back to specific modules.
- **Evaluation trace** — what the *environment* produces to compute the reward (compilation, execution, profiling output) before collapsing to a scalar. Usually thrown away; [[GEPA]] harvests it.

[[GEPA]] operationalizes both via a **feedback function `µ_f`**: it extends a reward `µ` to also return `feedback_text`, optionally **module-specific** (e.g. per-hop feedback in multi-hop QA), and can absorb **human-written explanations** attached to training instances.

## Why it beats scalar reward

- **Density** — a paragraph of compiler errors localizes the fault; a `0` reward does not.
- **Credit assignment** — language lets a reflection LM attribute success/failure to the right module without policy-gradient estimation.
- **Sample efficiency** — one informative reflection can fix a system in a step; gradients need thousands of rollouts to integrate the same lesson.

## Connections

- **[[Heuristic Learning]]** — the same bet in code-space: a coding agent edits code from tests/logs/replays instead of taking gradient steps. Both treat an *interpretable, editable artifact* + *language feedback* as the learning loop.
- **[[Trace-Based Evaluation]]** / **[[Error Trace Retention]]** — the infrastructure that makes execution/evaluation traces available is the same that GEPA mines.
- **[[Verifiability]]** — language feedback is most useful exactly where the environment can produce trustworthy, detailed signals (tests, graders, compilers).
- **[[Reward Modeling]]** — the contrast class: instead of learning a scalar reward model, keep the reward's *reasoning* in language.

## Sources

- [[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]]
