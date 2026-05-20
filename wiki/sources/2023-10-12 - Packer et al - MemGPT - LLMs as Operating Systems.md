---
type: source
title: "Packer et al — MemGPT: Towards LLMs as Operating Systems"
created: 2026-05-19
updated: 2026-05-19
tags:
- ai-agents
- memory
- context-engineering
- cognitive-architecture
status: mature
related:
- "[[MemGPT]]"
- "[[Self-Editing Memory]]"
- "[[Agent Memory Taxonomy]]"
- "[[Long-Horizon Context Management]]"
- "[[Context Engineering]]"
sources:
- "[[03_Resources/.raw/pdfs/memgpt-llms-as-operating-systems-2310.08560.pdf]]"
source_type: paper
author: Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, Joseph E. Gonzalez (UC Berkeley)
date_published: 2023-10-12
date_revised: 2024-02-12
url: https://arxiv.org/abs/2310.08560
arxiv_id: 2310.08560
confidence: high
key_claims:
- "A fixed context window can be treated like RAM in an operating system: page data in and out of it from unlimited external storage to give the appearance of unbounded context — 'virtual context management'."
- "The LLM itself manages its own memory by calling functions to move data between tiers (main context vs external context), making it a self-editing memory system."
- "Control flow mirrors an OS: external events (user messages, system warnings) act as interrupts; the agent chains multi-step actions via 'heartbeat' requests and yields control when done."
- "When the in-context message queue approaches the token limit, a 'memory pressure' warning triggers eviction — old messages are recursively summarized and flushed to recall storage."
- "On document QA and multi-session chat, MemGPT outperforms fixed-context baselines that simply truncate, because it can retrieve facts from arbitrarily far back."
---

# Packer et al — MemGPT: Towards LLMs as Operating Systems

## Summary

MemGPT (Memory-GPT) reframes the **context window as RAM** and proposes that an LLM can run its own **operating system** for memory: page data between a limited fast tier (the prompt) and unlimited slow tiers (external storage), giving the appearance of unbounded context. The key move is **self-direction** — the model decides what to remember, summarize, evict, and retrieve by calling functions, with no human in the loop. From UC Berkeley (Gonzalez/Stoica lab); the system later became the **Letta** framework.

This is the wiki's second academic source and it pairs tightly with [[CoALA]]: where CoALA gives the *taxonomy* of agent memory ([[Agent Memory Taxonomy]]), MemGPT gives a concrete *mechanism* for managing the working↔long-term boundary. In CoALA terms, MemGPT's memory-editing functions are **internal "learning" actions**, and its event loop is the **decision cycle** made explicit.

## The OS analogy

| OS concept | MemGPT |
|---|---|
| RAM (fast, small) | **Main context** — the LLM's prompt/context window |
| Disk (slow, large) | **External context** — out-of-context storage, searchable |
| Page fault / paging | function calls that pull external data into main context |
| Interrupt | external events (user message, memory-pressure warning) that trigger inference |

## Memory tiers

**Main context** (in the prompt) has three regions:
- **System instructions** — read-only; describes the control flow and function schemas.
- **Working context** — read/write structured store of salient facts (persona, user details); edited via functions.
- **FIFO queue** — rolling message history plus a recursive summary of evicted messages.

**External context** (on "disk"):
- **Recall storage** — full searchable log of all past messages/events.
- **Archival storage** — arbitrary-length read/write DB for facts and documents the agent chooses to persist.

## Mechanisms

- **Self-editing via function calls** → see [[Self-Editing Memory]]. The model issues `working_context.append/replace`, `archival_memory.insert/search`, `recall_memory.search`; results return into context.
- **Memory pressure & eviction** — when the FIFO queue nears the token limit, a system warning is injected; the agent flushes old messages, recursively summarizing them and writing originals to recall storage.
- **Interrupts & control flow** — events act as interrupts that wake the LLM. A function can set `request_heartbeat: true` to chain another step without waiting for the user (multi-step reasoning); otherwise the agent **yields** control until the next event.

## Evaluation

1. **Deep memory retrieval / document QA** — answering questions whose evidence lives far outside a single context window; MemGPT retrieves across sessions/documents where truncating baselines (e.g. fixed-context GPT-4) fail.
2. **Multi-session chat** — maintaining consistent persona and recalling earlier-session facts; MemGPT sustains coherence beyond the native window.

> [!key-insight] The reframing
> Don't fight the context limit — virtualize it. The same hierarchical-memory trick that lets a 16 GB machine address 64 GB of virtual memory lets a fixed-window LLM behave as if it had unbounded context, *if the model is taught to manage its own paging.* Memory becomes an agent capability, not a model property.
