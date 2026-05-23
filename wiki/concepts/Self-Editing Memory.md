---
type: concept
title: Self-Editing Memory
created: 2026-05-19
updated: 2026-05-19
tags:
- ai-agents
- memory
- context-engineering
status: seed
related:
- "[[MemGPT]]"
- "[[Agent Memory Taxonomy]]"
- "[[CoALA]]"
- "[[Agent Skills]]"
- "[[Online Learning from Interaction]]"
- "[[Persona Vectors vs Memory Files]]"
- "[[Letta]]"
sources:
- "[[2023-10-12 - Packer et al - MemGPT - LLMs as Operating Systems]]"
---

# Self-Editing Memory

The pattern where **the model manages its own long-term memory by calling tools/functions**, rather than a fixed harness deciding what to store and retrieve. Introduced operationally by [[MemGPT]], where the LLM issues calls like `working_context.append/replace`, `archival_memory.insert/search`, and `recall_memory.search`, and the results return into context.

## Why it's a distinct idea

Most memory in agents is *passive* — a retrieval pipeline the harness controls (RAG, [[Contextual Retrieval]]). Self-editing memory is *active*: deciding **what is worth remembering** and **when to recall it** becomes part of the agent's action space.

In [[CoALA]] terms this is the **learning** internal action made first-class — writing to episodic, semantic, and even procedural memory under the model's own control. It is the bridge from "agent with a knowledge base" toward "agent that curates its own knowledge base," and a step toward CoALA's prospective frontier of agents that modify their own procedures.

## Trade-offs

- **Upside:** unbounded effective context, persistence across sessions, salience decided by the model that knows the task.
- **Risk:** the model can write wrong/stale facts into durable storage (memory poisoning), and self-editing competes for tokens and tool-call budget. Curation quality becomes a reliability surface — closely related to why procedural-memory edits are flagged as *risky* in [[Agent Memory Taxonomy]].

Related surface: [[Agent Skills]] are self-*authored procedural* memory; self-editing memory is the *declarative* analogue.
