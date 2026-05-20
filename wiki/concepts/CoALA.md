---
type: concept
title: CoALA
created: 2026-05-19
updated: 2026-05-19
tags:
- ai-agents
- framework
- cognitive-architecture
- decision-making
status: developing
related:
- "[[Agent Memory Taxonomy]]"
- "[[ReAct]]"
- "[[Tree of Thoughts]]"
- "[[Augmented LLM]]"
- "[[Workflows vs Agents]]"
sources:
- "[[2023-09-05 - Sumers et al - Cognitive Architectures for Language Agents]]"
---

# CoALA — Cognitive Architectures for Language Agents

A conceptual framework ([[2023-09-05 - Sumers et al - Cognitive Architectures for Language Agents]]) that organizes LLM-based agents by importing the **cognitive-architecture** tradition of symbolic AI (Soar, ACT-R, production systems). A language agent is described by three things: its **memory modules**, its **action space**, and its **decision-making procedure**.

## 1. Memory modules

See [[Agent Memory Taxonomy]] — working, episodic, semantic, procedural.

## 2. Action space

Every action an agent can take is either **internal** (changes memory) or **external** (changes the world).

**Internal actions:**
- **Retrieval** — read from long-term memory into working memory (rule-based, sparse, or dense). Maps to [[Just-in-Time Context Retrieval]], [[Contextual Retrieval]], [[BM25 and Hybrid Retrieval]].
- **Reasoning** — process working-memory contents via the LLM to generate new information (the [[Think Tool]], chain-of-thought).
- **Learning** — write to long-term memory: update episodic experience, semantic knowledge, LLM weights (fine-tuning), or the **agent's own code** (procedural).

**External actions (grounding):**
- **Physical** — robotics, sensors, actuators.
- **Dialogue** — humans or other agents.
- **Digital** — APIs, code execution, websites, games.

## 3. Decision-making cycle

A repeated loop:

1. **Planning stage**
   - *Proposal* — generate one or more candidate actions (reasoning ± retrieval).
   - *Evaluation* — score candidates (heuristics, LLM scores, learned values, LLM reasoning).
   - *Selection* — pick one (argmax, softmax, voting).
2. **Execution stage** — apply the selected grounding or learning action; receive feedback; loop.

## Why it's load-bearing

CoALA is the conceptual layer beneath the wiki's operational concepts. A fixed decision procedure is a [[Workflows vs Agents|workflow]]; an agent that *chooses* its procedure is an agent. An [[Augmented LLM]] is the minimal CoALA agent: working memory + retrieval + one grounding action, no real decision loop. The empty cells of the framework — especially agents that learn new *decision procedures* — are flagged as the open research frontier.

> [!key-insight]
> CoALA's bet: language agents are not a new paradigm but the newest **cognitive architecture**. Symbolic AI already charted the design space; LLMs made the modules cheap. Progress = filling the empty corners of a pre-existing map.
