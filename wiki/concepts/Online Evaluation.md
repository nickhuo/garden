---
type: concept
title: "Online Evaluation"
created: 2026-05-20
updated: 2026-05-20
tags: [ai-agents, llm, evaluation]
status: developing
related:
  - "[[LLM-as-Judge]]"
  - "[[Implicit Feedback Signals]]"
  - "[[Reward Modeling]]"
  - "[[A/B Testing for Agents]]"
  - "[[Agent Eval Pyramid]]"
  - "[[Trace-Based Evaluation]]"
  - "[[Continuous Evaluation]]"
  - "[[Online LLM-as-Judge]]"
  - "[[Offline-Online Evaluation Gap]]"
  - "[[Online Evaluation Bottlenecks]]"
sources:
  - "[[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]]"
  - "[[2025 - LangChain - LLM Observability and Monitoring]]"
---

# Online Evaluation

## Summary

Online evaluation measures an agent against **live user behavior in production**, in contrast to offline evaluation against a fixed golden dataset. Offline benchmarks answer "is this model good for a population?"; online evaluation answers "did the sentence it just wrote land for *this* user, right now?" It turns real interaction — clicks, edits, follow-ups, abandonment, explicit votes — into a learning signal that can correct or reinforce behavior *as the experience unfolds*.

The methods sit on a spectrum from cheap/fast/observational to expensive/slow/causal:

1. **Implicit feedback** ([[Implicit Feedback Signals]]) — observe what users do (accept, edit, retry, abandon). Cheap, abundant, biased.
2. **Interleaving / bandits** — route traffic to compare or learn online with controlled exploration. Sensitive, sample-efficient.
3. **A/B testing** ([[A/B Testing for Agents]]) — randomized controlled experiment. Slow, expensive, causally trustworthy.
4. **Online preference / reward learning** ([[Reward Modeling]]) — convert live preference into a reward signal that updates the policy (online DPO, RLAIF).
5. **Online LLM-as-Judge** ([[Online LLM-as-Judge]]) — score live traffic automatically against a rubric. Scalable, but biased; tiered with cheap distilled judges + agentic [[Agent-as-a-Judge]] on anomalies.

## Production view (2026)

The industry operationalizes this loop as [[Continuous Evaluation]] — trace → sample → judge → threshold-alert over live traffic. The *empirical* case for online over offline is the [[Offline-Online Evaluation Gap]] (public benchmarks lose predictive power; LiveCodeBench drops of 20-30%+). The binding limits are catalogued in [[Online Evaluation Bottlenecks]] (judge cost/latency, statistical power, credit assignment, drift). External survey + industry view: [[Research - Online Evaluation in Production]].

## Why it matters

For agent applications, the offline golden dataset is the *base* (it must exist first — "eval before optimization") but it is frozen at authoring time and blind to the actual user in front of the system. Online evaluation is the **live extension**: it is the channel through which real-time interaction becomes the signal that updates persisted memory, persona, retrieval priority, and policy. It is the bridge between a static benchmark number and a continuously improving experience.

## Limits

- Every online signal is a **proxy**. Implicit signals carry position/presentation bias; explicit votes are sparse and self-selected; LLM-judge scores carry their own biases (see [[LLM-as-Judge]]).
- The metric *is* the construct (see [[2023-05 - Schaeffer et al - Emergent Abilities a Mirage]]) — a badly chosen OEC manufactures or hides effects.
- Online learning loops can drift, reward-hack, or amplify a feedback bias faster than offline review can catch it. Causal confirmation (A/B) is needed before trusting an observed lift.

## Connection to prior work

The Chatbot Arena half of [[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]] is the canonical LLM-era online-eval platform (live pairwise votes → Elo). The discipline of trustworthiness comes from the online-controlled-experiment tradition in web experimentation. The implicit-feedback and bandit methods are inherited wholesale from IR/recsys.

In Nick's projects this is the live counterpart to the offline rigor: Compass' closed loop (user logs → KB priority / eval rubric / policy revision) is online evaluation feeding back into the offline base; Donut's shadow→canary→prod gating is staged online rollout; Beckman's judge axes are the rubric that an online judge would apply.

## Connections

- Sits above [[Agent Eval Pyramid]] as the production tier; complements [[Trace-Based Evaluation]] (online traces are the raw substrate).
- [[Eval Awareness]] is a failure mode for online eval too: a model that detects it is being scored online can game the signal.
- [[tau-bench]] / [[User Simulator Evaluation]] are the offline simulation of what online eval observes for real.

## Open questions

> [!gap] How much weight should an online signal carry before it updates persisted memory vs. requiring offline/A-B confirmation? No clean published threshold.

> [!gap] How to detect a feedback loop that is reward-hacking an implicit metric (e.g. optimizing for engagement-via-frustration) before it harms long-term value?

## Sources

- [[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]]
- [[2023-05 - Schaeffer et al - Emergent Abilities a Mirage]]
