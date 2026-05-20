---
type: concept
title: Agent Memory Taxonomy
created: 2026-05-19
updated: 2026-05-19
tags:
- ai-agents
- memory
- cognitive-architecture
status: developing
related:
- "[[CoALA]]"
- "[[Long-Horizon Context Management]]"
- "[[Session as Event Log]]"
- "[[Agent Skills]]"
- "[[Context Engineering]]"
sources:
- "[[2023-09-05 - Sumers et al - Cognitive Architectures for Language Agents]]"
---

# Agent Memory Taxonomy

The four-way memory decomposition [[CoALA]] borrows from cognitive architectures (Soar, ACT-R). It gives a precise vocabulary for "memory" in agents, which is otherwise overloaded.

| Module | Holds | Lifespan | Wiki mapping |
|---|---|---|---|
| **Working** | active info for the *current* decision cycle: percepts, retrieved knowledge, carried-forward goals | one cycle (the context window) | [[Recitation]], [[Session as Event Log]], [[Context Engineering]] |
| **Episodic** | past experiences: event histories, trajectories, training pairs | persistent | conversation logs, [[Long-Horizon Context Management]], [[MemGPT]] recall storage |
| **Semantic** | world knowledge and facts | persistent | retrieval corpora, [[Contextual Retrieval]], [[MemGPT]] archival storage |
| **Procedural** | *how to act/decide*: implicit (LLM weights) + explicit (agent code) | persistent | [[Agent Skills]], skill libraries (Voyager) |

## The key distinctions

- **Working vs the rest** — working memory is the only one that lives inside a single decision cycle. Everything labeled "context engineering" is really working-memory management. [[Long-Horizon Context Management]] is the discipline of deciding what graduates from working memory into episodic storage and back. [[MemGPT]] is the canonical mechanism: treat working memory as RAM and *page* data to/from external tiers under the model's own control ([[Self-Editing Memory]]).
- **Procedural memory is special** — it has two substrates: weights (implicit, changed by fine-tuning) and **code** (explicit, changed by editing the agent itself). Updating procedural memory is *risky* because it changes the agent's functionality, not just its knowledge. This is the substrate of the most ambitious CoALA direction: agents that rewrite their own decision procedures. [[Meta-Harness]] and self-improving harness patterns live here.
- **Episodic → semantic distillation** — turning specific experiences into general knowledge (reflection in Generative Agents) is a *learning* internal action that writes from episodic into semantic memory.

> [!note] Why bother with the taxonomy
> "Add memory to the agent" is ambiguous — it could mean a retrieval corpus (semantic), a conversation log (episodic), a scratchpad (working), or a skill library (procedural). Each has different write mechanics, risks, and failure modes. The taxonomy forces the question: *which* memory?
