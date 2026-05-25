---
type: source
title: "Everything is a Ralph Loop"
aliases:
  - "Everything is a Ralph Loop"
  - "ghuntley loop"
created: 2026-05-24
updated: 2026-05-24
tags:
  - ai-agents
  - agentic-coding
  - context
  - agent-pattern
status: developing
source_type: blog
author: "Geoffrey Huntley"
date_published: 2026-01-17
url: https://ghuntley.com/loop/
confidence: medium
key_claims:
  - "Ralph is a monolithic single-process agent that performs one task per loop, autonomously, in one repository"
  - "Effective agentic coding is context engineering, not multi-agent orchestration"
  - "Multi-agent systems are premature complexity because agents are non-deterministic"
  - "Software development as a brick-by-brick craft is 'dead'; loops produce software cheaper and faster"
  - "Engineers must build their own coding agents or become unhireable"
related:
  - "[[Geoffrey Huntley]]"
  - "[[Ralph Loop]]"
  - "[[Context Engineering]]"
  - "[[Multi-Agent Systems]]"
sources:
  - "[[.raw/articles/loop-2026-05-24.md]]"
---

# Everything is a Ralph Loop

[[Geoffrey Huntley]], January 17, 2026. [Blog post](https://ghuntley.com/loop/).

## TL;DR

A manifesto for the [[Ralph Loop]]: a **monolithic, single-process agent** that loops over one task at a time against a goal + backing specifications, in a single repository, autonomously. Huntley's thesis is that effective agentic coding is **[[Context Engineering]]**, not multi-agent orchestration — and that treating [[LLM as Programmable Computer|LLMs as a new form of programmable computer]] makes brick-by-brick software engineering obsolete. "Software is now clay on the pottery wheel."

## The technique

> "Ralph is an orchestrator pattern where you allocate the array with the required backing specifications and then give it a goal."

You loop the goal; the model performs **one task per loop**. You *watch* the loop, identify failure domains, and apply engineering fixes so a given failure never recurs — iteratively shaping the system rather than stacking it vertically. Runs either manually (prompt, `CTRL+C` to pause) or fully automated while the developer is away. Full mechanics on [[Ralph Loop]].

## The anti-multi-agent argument

Huntley is pointedly against the [[Multi-Agent Systems|multi-agent]] direction of "SFO-era" hype: because agents are **non-deterministic**, multiplexing many of them multiplies complexity for little gain. Ralph instead scales **vertically** as a single OS process. This is a direct design counter-position to Anthropic's coordinator+workers framing — see the contradiction note on [[Multi-Agent Systems]].

## The Weaving Loom

His three-years-in-the-making project **The Weaving Loom** — "infrastructure for evolutionary software" — sits at a self-described "level 9" of automation, past Steve Yegge's "Gas Town" (level 8 orchestration). Goal: software that evolves its own product autonomously and **optimizes for revenue with no human in the loop**.

## The hiring claim

> "i now won't hire you unless you have this fundamental knowledge"

Huntley declares "software development is dead – I killed it" and argues software can be built "cheaper than the wage of a burger flipper at maccas." His employability test: can you demonstrate a coding agent you built yourself? He frames understanding LLMs-as-programmable-computers as the survival skill "before the big bang happens."

## Why it matters here

Ralph is the **opinionated monolithic pole** of the agent-architecture spectrum this wiki already maps. It operationalizes [[Context Engineering]] and the Simon-Willison definition of an agent ("LLMs autonomously using tools in a loop") into a named, repeatable practitioner method, and stakes out the opposite position from [[Multi-Agent Systems]] and [[Orchestrator-Workers]]. It also extends [[Autonomous Research Agents]] / [[Self-Evolving Agent Environments]] toward a self-improving, revenue-optimizing endpoint.

## Caveats

Polemical, single-author, vendor-of-self blog post with no benchmarks. Claims ("software development is dead", "cheaper than a burger flipper") are rhetorical, not measured. Confidence on the *technique* (Ralph loop) is higher than on the *economic claims*.

## Sources

- [[.raw/articles/loop-2026-05-24.md]] — fetched 2026-05-24 (model-summarized extraction; verbatim quotes preserved)
