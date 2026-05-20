---
type: source
title: "Sumers et al — Cognitive Architectures for Language Agents (CoALA)"
created: 2026-05-19
updated: 2026-05-19
tags:
- ai-agents
- framework
- memory
- cognitive-architecture
- decision-making
status: mature
related:
- "[[CoALA]]"
- "[[Agent Memory Taxonomy]]"
- "[[ReAct]]"
- "[[Tree of Thoughts]]"
- "[[Shunyu Yao]]"
- "[[Augmented LLM]]"
sources:
- "[[03_Resources/.raw/pdfs/cognitive-architectures-language-agents-2309.02427.pdf]]"
source_type: paper
author: Theodore R. Sumers, Shunyu Yao, Karthik Narasimhan, Thomas L. Griffiths (Princeton)
date_published: 2023-09-05
date_revised: 2024-03-15
url: https://arxiv.org/abs/2309.02427
arxiv_id: 2309.02427
confidence: high
key_claims:
- "Language agents can be organized with a conceptual framework borrowed from cognitive science and symbolic AI: modular memory, a structured action space, and a generalized decision-making loop."
- "Memory splits into four modules — working, episodic, semantic, procedural — mirroring production-system cognitive architectures (Soar, ACT-R)."
- "The action space decomposes into internal actions (retrieval, reasoning, learning) and external actions (grounding: physical, dialogue, digital)."
- "Decision-making is a repeated cycle: planning (proposal → evaluation → selection) followed by execution of a grounding or learning action."
- "Most 2022–2023 agents (ReAct, SayCan, Voyager, Generative Agents, Tree of Thoughts) occupy distinct corners of this space; the empty corners are the actionable research directions."
---

# Sumers et al — Cognitive Architectures for Language Agents (CoALA)

## Summary

A position/survey paper from the Princeton group (Sumers, [[Shunyu Yao]], Narasimhan, Griffiths) that imports the **cognitive-architecture** tradition of symbolic AI — Soar, ACT-R, production systems — to organize the explosion of LLM "language agents." The contribution is a vocabulary and taxonomy, not a system: [[CoALA]] (Cognitive Architectures for Language Agents) lets you place any agent on three axes — its **memory modules**, its **action space**, and its **decision procedure** — and read off what it has and what it lacks.

This is the wiki's first **academic framework** source, distinct from the Anthropic-blog corpus that frames agents operationally (harnesses, context engineering, evals). CoALA is the conceptual scaffold underneath those practices: an [[Augmented LLM]] is, in CoALA terms, an agent with working memory + retrieval + a single grounding action and no decision loop.

## The three axes

1. **Memory** → [[Agent Memory Taxonomy]]: working / episodic / semantic / procedural.
2. **Action space** → internal (retrieval, reasoning, learning) vs external (grounding: physical, dialogue, digital). See [[CoALA]].
3. **Decision-making** → planning (propose → evaluate → select) then execute, looped. See [[CoALA]].

## Surveying existing agents (CoALA as a lens)

| Agent | Memory | Notable trait |
|---|---|---|
| **[[ReAct]]** | none (long-term) | interleaves reasoning + grounding in a fixed cycle, no evaluation |
| **SayCan** | none | single-step planning; LLM × learned-value scoring over fixed skills |
| **Voyager** | hierarchical procedural (skill library) | all four action types; code-as-procedural-memory |
| **Generative Agents** | episodic + semantic | reflection writes back to memory; retrieval feeds planning |
| **[[Tree of Thoughts]]** | none | deliberate planning via tree search (propose/evaluate/select) |

The point: each agent fills different cells, and the **empty cells** (e.g. agents that learn new decision procedures) are the prospective directions.

## Prospective directions

- **Modularity / standard abstractions** — Memory, Action, Agent classes, the way MDPs standardized RL.
- **Memory integration** — interleave retrieval with forward simulation; combine bootstrapped human knowledge with self-generated experience.
- **Procedural learning** — agents that learn *how to learn / decide* (modifying their own code); high-impact, risky, mostly unexplored.
- **Structured reasoning** — define reasoning *step sequences* rather than low-level prompt engineering; agent use-cases should reshape LLM training.
- **Unlearning / modification** — deletion and selective fine-tuning are understudied.

## Why it matters for this wiki

CoALA gives a principled home for scattered concepts: [[Recitation]] and [[Session as Event Log]] are working-memory mechanics; [[Contextual Retrieval]] / [[Just-in-Time Context Retrieval]] are *retrieval* internal actions; [[Agent Skills]] and [[Voyager]]-style skill libraries are *procedural* memory; [[Long-Horizon Context Management]] is the working↔episodic boundary. It also predates and frames the [[Workflows vs Agents]] distinction — a workflow fixes the decision procedure, an agent chooses it.

> [!key-insight] The framing claim
> Language agents are not new — they are the latest cognitive architecture. The history of symbolic AI already mapped the design space; LLMs just made the modules cheap to build. The research frontier is the corners of that map nobody has filled.
