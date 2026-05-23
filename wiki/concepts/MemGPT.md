---
type: concept
title: MemGPT
created: 2026-05-19
updated: 2026-05-19
tags:
- ai-agents
- memory
- context-engineering
- cognitive-architecture
status: developing
related:
- "[[Self-Editing Memory]]"
- "[[Agent Memory Taxonomy]]"
- "[[CoALA]]"
- "[[Long-Horizon Context Management]]"
- "[[Context Engineering]]"
- "[[Letta]]"
- "[[Memory Stream]]"
sources:
- "[[2023-10-12 - Packer et al - MemGPT - LLMs as Operating Systems]]"
---

# MemGPT

A system (and design pattern) that treats the **LLM context window as RAM** and runs an operating-system-style memory manager on top of it — *virtual context management*. By paging information between a limited in-context tier and unlimited external storage, a fixed-window model behaves as if it had unbounded context. From [[2023-10-12 - Packer et al - MemGPT - LLMs as Operating Systems]]; productionized as the **Letta** framework.

## The core idea

Two tiers, mirroring RAM and disk:

- **Main context** (in the prompt): system instructions (read-only), **working context** (structured editable facts), and a **FIFO queue** of recent messages + a recursive summary of evicted ones.
- **External context** (on "disk"): **recall storage** (full searchable event log) and **archival storage** (arbitrary read/write fact/document DB).

The LLM moves data across the boundary itself, by calling functions — see [[Self-Editing Memory]]. When the in-context queue approaches the token limit, a **memory-pressure** warning triggers eviction: old messages are recursively summarized and flushed to recall storage. External events act like **interrupts** waking the model; a `request_heartbeat` flag chains multi-step actions, and the agent **yields** when done.

## Relation to other concepts

- **[[Agent Memory Taxonomy]] / [[CoALA]]:** MemGPT is a concrete mechanism for the working↔episodic/semantic boundary CoALA names. Its memory-edit functions are CoALA *learning* internal actions; its event loop is the *decision cycle*.
- **[[Long-Horizon Context Management]]:** MemGPT is one of the earliest principled answers — paging + recursive summarization instead of naive truncation.
- **[[Context Engineering]]:** flips the framing from "engineer the prompt" to "give the agent tools to engineer its own context."

> [!note] Why it endured
> Modern "memory tools" and self-managing-context features in agent frameworks are MemGPT's idea generalized: the model, not the harness, decides what stays resident. The OS metaphor (paging, interrupts, virtual memory) gave the field a vocabulary it still uses.
