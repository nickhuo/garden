---
type: source
title: "Sequoia Ascent 2026 — Karpathy on Software 3.0 and Agentic Engineering"
source_type: talk
author: "Andrej Karpathy"
date_published: 2026
url: "https://karpathy.bearblog.dev/sequoia-ascent-2026/"
created: 2026-05-22
updated: 2026-05-22
status: developing
confidence: high
key_claims:
  - "Around December 2025 coding agents crossed a reliability threshold — the unit of programming shifted from lines to delegated 'macro actions', and the programmer becomes an orchestrator."
  - "Software 3.0: humans program LLMs through prompts, context, tools, and memory; the context window is 'your lever over the interpreter'. It follows 1.0 (explicit code) and 2.0 (learned weights)."
  - "'Traditional software automates what you can specify; LLMs automate what you can verify.' Verifiability explains where AI moves fastest."
  - "Jagged intelligence = verifiability × training attention × data coverage × economic value. The founder test is 'are you on the model's rails?'"
  - "Vibe coding raises the floor (anyone can build); agentic engineering raises the ceiling (professional discipline over fallible agents)."
  - "Build agent-native infrastructure: the user is increasingly the human's agent. Design sensors and actuators, not screens."
  - "LLMs are ghosts, not animals — statistical simulations of human artifacts; adopt 'empirical familiarity' as the posture."
  - "You can outsource your thinking, but you can't outsource your understanding."
tags:
  - ai-agents
  - llm
  - foundational
  - agentic-coding
related:
  - "[[Software 3.0]]"
  - "[[Verifiability]]"
  - "[[Jagged Intelligence]]"
  - "[[Vibe Coding]]"
  - "[[Agentic Engineering]]"
  - "[[Agent-Native Infrastructure]]"
  - "[[Andrej Karpathy]]"
  - "[[Software 2.0]]"
sources: []
---

# Sequoia Ascent 2026 — Karpathy on Software 3.0 and Agentic Engineering

Andrej Karpathy, Sequoia Ascent 2026 (bearblog companion post). Extends his [[Software 2.0]] arc into a working theory of **agentic engineering**: how the December-2025 reliability jump in coding agents changes what programming *is*, where AI gets good, and what humans must still own.

## The inflection (December 2025)

Coding agents (Claude Code, Codex, Cursor) crossed from helpful-but-flawed to reliable — "the chunks just came out fine." The unit of work moved from lines to delegated **macro actions** (implement a feature, refactor a subsystem, write and fix tests). The programmer becomes an **orchestrator** of agents. See [[Agentic Engineering]].

## Software 3.0

The third stack after 1.0 (explicit code) and 2.0 (learned weights): humans **program LLMs in natural language** via prompts, context, tools, examples, and memory. The context window is "your lever over the interpreter." Sometimes the app *disappears* entirely — Karpathy's MenuGen example collapses a full web stack into a single multimodal transformation (menu photo → dishes rendered onto the image). The old stack was "scaffolding around a transformation the model can now perform directly." Concept: [[Software 3.0]].

## Verifiability

"Traditional software automates what you can **specify**; LLMs automate what you can **verify**." Domains with automatic reward signals (math, code, tests, games) improve fastest because models get immediate feedback. This is the same engine [[The Bitter Lesson]] and [[Welcome to the Era of Experience]] point at — RL over verifiable environments. Concept: [[Verifiability]].

## Jagged intelligence

Capability isn't smooth: `capability ≈ verifiability × training attention × data coverage × economic value`. GPT-4's chess jump tracked more chess data in the mix, not general improvement. Models are "artifacts of pretraining mixtures, RL environments, benchmark pressure, product priorities, and economic incentives." Founder test: **"are you on the model's rails?"** Off-rails-but-verifiable domains undertrained by frontier labs are a startup wedge (see [[Verifiability]]). Concept: [[Jagged Intelligence]].

## Vibe coding vs. agentic engineering

[[Vibe Coding]] raises the floor (anyone can build by describing). [[Agentic Engineering]] raises the ceiling: specs, plan supervision, diff review, tests, permissioning, taste. The frontier skill is *concepts* (storage, invariants, identity, security boundaries), not API recall — agents handle APIs. The MenuGen Stripe/Google email-mismatch payment bug is the cautionary example: the agent's plausible match was an identity bug a human had to catch. Karpathy argues hiring should test this directly (build-with-agents → deploy securely → adversarial agents attack it), and the "10x engineer" may become far more extreme.

## Agent-native infrastructure

The user is increasingly the human's **agent**, not the human. Build for it: Markdown docs, CLIs, APIs, MCP servers, structured logs, machine-readable schemas, copy-pasteable instructions, safe permissioning, auditable actions, headless flows. Frame products as **sensors** (world → digital state) and **actuators** (agent → change). Connects to [[ACI - Agent-Computer Interface]] and [[Agent Interface Contracts]]. Concept: [[Agent-Native Infrastructure]].

## Ghosts, not animals

LLMs lack biological drives; they're "statistical simulations of human artifacts." Brilliant then "bizarrely dumb" — "jagged, alien tools." Correct posture: **empirical familiarity**, neither dismissal nor blind trust. (Filed within [[Jagged Intelligence]].)

## Understanding is not outsourceable

"You can outsource your thinking, but you can't outsource your understanding." Knowledge bases (the LLM-wiki pattern this vault uses) are "tools for transforming information into understanding," not just answer machines. The `microGPT` example: a distilled, inspectable artifact + human taste + an agent that explains it interactively.

## Relevance

This is the conceptual capstone over much of the existing wiki: it names the era ([[Software 3.0]]) above [[Software 2.0]] / [[Model-Centric Architecture]], gives the *why-now* via [[Verifiability]] (echoing [[The Bitter Lesson]]), and reframes harness/interface work ([[ACI - Agent-Computer Interface]], [[Agent Interface Contracts]], [[MCP]]) as **agent-native infrastructure**.
