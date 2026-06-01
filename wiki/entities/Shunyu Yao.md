---
type: entity
title: "Shunyu Yao"
created: 2026-05-19
updated: 2026-06-01
tags:
- ai-agents
- entity
- person
status: developing
entity_type: person
entity_tier: thinker
role: "Researcher (Princeton PhD; later OpenAI / Sierra). Lead/co-author of ReAct, Tree of Thoughts, CoALA, and τ-bench. Central figure in the language-agents research line."
core_claim: "Language agents are the latest cognitive architecture — build the patterns, organize them into a framework, then measure their reliability."
first_mentioned: 2026-05-19
related:
- "[[ReAct]]"
- "[[Tree of Thoughts]]"
- "[[CoALA]]"
- "[[tau-bench]]"
- "[[Pass^k Reliability Metric]]"
- "[[Workflows Beat Agents for Most Production]]"
sources:
- "[[2023-09-05 - Sumers et al - Cognitive Architectures for Language Agents]]"
- "[[2024-06-17 - Yao et al - tau-bench]]"
---

# Shunyu Yao

Researcher whose work threads through much of the language-agents canon — a coherent arc from inventing agent patterns to organizing them to measuring whether they actually work.

## Worldview / 核心主张

1. **Language agents are not new — they are the latest cognitive architecture.** [[CoALA]] imports the symbolic-AI tradition (Soar, ACT-R, production systems) to argue the agent design space was already mapped; LLMs just made the modules cheap. The frontier is the *empty cells* of that map.
2. **Reliability, not capability, is the deployment bottleneck.** [[tau-bench]] measures the *consistency* gap directly: SOTA agents solve <50% of customer-service tasks and [[Pass^k Reliability Metric|pass^8]] collapses below 25% even when pass^1 exceeds 60% — the *same* task solved inconsistently across i.i.d. trials.
3. **Reasoning and acting should interleave and search.** [[ReAct]] (interleave reasoning + grounding) and [[Tree of Thoughts]] (deliberate search over reasoning paths) are the foundational patterns the later framework organizes.

## Methodology / 方法论

- **The pattern → framework → benchmark arc.** Build agent patterns (ReAct, ToT), then a framework to organize the whole space ([[CoALA]]), then a benchmark to measure them in production-like settings ([[tau-bench]]). Each stage presupposes the last.
- **Borrow rigor from older fields.** CoALA's three axes (memory modules / action space / decision procedure) are lifted from cognitive science rather than invented ad hoc — the way MDPs standardized RL.
- **Measure with deterministic ground truth.** τ-bench bypasses LLM-judge entirely: reward = final database state matches a *uniquely* annotated outcome. Faithful and free, at the cost of constraining tasks to ones with exactly one valid outcome.

## Body of work (in the wiki)

- **2022 — [[ReAct]]** — interleaving reasoning and acting (concept page; source not yet ingested).
- **2023 — [[Tree of Thoughts]]** — deliberate search over reasoning paths (concept page; source not yet ingested).
- **2023 — [[2023-09-05 - Sumers et al - Cognitive Architectures for Language Agents]]** ([[CoALA]]) — the cognitive-architecture taxonomy organizing the agent zoo.
- **2024 — [[2024-06-17 - Yao et al - tau-bench]]** (at Sierra) — tool-agent-user reliability benchmark; introduces [[Pass^k Reliability Metric]] and [[User Simulator Evaluation]].

## Throughlines

- **Structuring the design space** — every work either places agents on a map (CoALA) or pins down a previously-vague quantity (pass^k reliability).
- **From building → organizing → measuring** — the career arc mirrors the field's own maturation.

## Tensions

- **Reliability collapse vs autonomous-agent optimism** — τ-bench is *strong* support for [[Workflows Beat Agents for Most Production]]: explicit state machines avoid the rule-following (22%) and partial-resolution (19%) failure modes almost by construction.
- **Open question he raises** — does pass^k collapse the same way on coding/research tasks, or is the variance a customer-service artifact of user-simulator stochasticity?

## Corpus to ingest

- **ReAct** (Yao et al. 2022) and **Tree of Thoughts** (Yao et al. 2023) — both have concept pages but no source page; ingesting them would complete the body-of-work arc and ground two heavily-cited concepts.
