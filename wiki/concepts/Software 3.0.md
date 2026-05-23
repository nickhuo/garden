---
type: concept
title: "Software 3.0"
created: 2026-05-22
updated: 2026-05-22
status: seed
tags:
  - ai-agents
  - llm
  - foundational
  - architecture
related:
  - "[[Software 2.0]]"
  - "[[Model-Centric Architecture]]"
  - "[[Agentic Engineering]]"
  - "[[Andrej Karpathy]]"
sources:
  - "[[2026-05-22 - Karpathy - Sequoia Ascent 2026]]"
---

# Software 3.0

The third stack in Karpathy's progression of how programs are written:

- **Software 1.0** — humans write explicit code (instructions in a programming language).
- **Software 2.0** — humans assemble datasets and architectures; the program is *learned into weights* by optimization. See [[Software 2.0]].
- **Software 3.0** — humans **program the LLM in natural language**: prompts, context, tools, examples, memory, and instructions. The model is a programmable interpreter; the **context window is "your lever over the interpreter."**

## What's new

The LLM performs computation *over digital information* directly. The programmer's job shifts from emitting lines to **specifying context and delegating macro actions** — the orchestrator stance of [[Agentic Engineering]].

## Software can disappear

The sharpest claim: in 3.0, parts of the application *cease to exist*. Karpathy's MenuGen example — originally a full stack (frontend, APIs, image gen, auth, payments, deploy) — collapses into a single multimodal transformation: photograph a menu, the model renders dish images onto it. "Much of the app disappears." The old stack was "scaffolding around a transformation the model can now perform directly." The founder prompt becomes: *what software should dissolve into a direct model transformation?*

## A new kind of opportunity

3.0 automates **information processing that was never programmable** before — e.g. maintaining a knowledge base "robustly across messy human documents" (the LLM-wiki pattern this vault runs on). Ask not only "what workflow can AI speed up?" but "what information transformation was impossible before?"

## Relation to existing pages

The natural-language-programming heir of [[Software 2.0]] and the rhetorical frame above [[Model-Centric Architecture]] — both push logic out of hand-written code, 2.0 into weights, 3.0 into context. Where the model is genuinely good is governed by [[Verifiability]] and [[Jagged Intelligence]].

## Source

- [[2026-05-22 - Karpathy - Sequoia Ascent 2026]] — entity: [[Andrej Karpathy]]
