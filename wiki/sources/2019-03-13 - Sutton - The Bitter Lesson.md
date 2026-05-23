---
type: source
title: "The Bitter Lesson"
source_type: essay
author: "Richard Sutton"
date_published: 2019-03-13
url: "http://www.incompleteideas.net/IncIdeas/BitterLesson.html"
created: 2026-05-20
updated: 2026-05-20
status: mature
confidence: high
key_claims:
  - "General methods that leverage computation (search and learning) ultimately win, by a large margin, over methods that encode human knowledge."
  - "Building in how we think we think does not work in the long run; it plateaus and blocks scaling."
  - "Chess, Go, speech recognition, and computer vision each repeated the pattern: hand-engineered knowledge was overtaken by scalable search/learning."
  - "The real content of minds is irredeemably complex; we should build meta-methods that can discover and capture complexity, not bake in our own simplifications."
tags:
  - ai-agents
  - llm
  - foundational
  - architecture
related:
  - "[[The Bitter Lesson]]"
  - "[[Model-Centric Architecture]]"
  - "[[Software 2.0]]"
sources: []
---

# The Bitter Lesson

Richard Sutton, March 13, 2019. A short essay (`incompleteideas.net`) that has become the canonical argument for scaling general methods over hand-engineered knowledge.

## Core argument

The biggest lesson from 70 years of AI research is that general methods that leverage computation are ultimately the most effective, and by a large margin. The two methods that scale arbitrarily with compute are **search** and **learning**. Researchers repeatedly try to bake in human knowledge for short-term gains, but this satisfies the researcher more than it helps the system, and it plateaus — eventually overtaken by approaches that simply scale compute against general methods.

## Historical examples

- **Chess** — Deep Blue won by massive search, not by human-encoded positional knowledge. Researchers who had pursued human-understanding approaches were "embittered."
- **Go** — Same pattern: self-play learning plus search beat human-knowledge features.
- **Speech recognition** — Statistical methods (HMMs, later deep learning) on data displaced hand-crafted linguistic knowledge of the human vocal tract.
- **Computer vision** — Hand-designed features (edges, SIFT) gave way to learned representations in deep convolutional nets.

## Memorable framing

"We have to learn the bitter lesson that building in how we think we think does not work in the long run." The contents of minds are "tremendously, irredeemably complex"; we should stop trying to encode them and instead build meta-methods that can discover that complexity from data and compute.

## Relevance to agents

The foundational case for [[Model-Centric Architecture]]: as compute and capability grow, the long-run winner is to give the model freedom to learn rather than scaffold it with brittle hand-written orchestration. Concept page: [[The Bitter Lesson]].

> [!gap] Sutton's evidence is from perception/games, not from agentic tool use with real-world side effects. Whether the lesson transfers fully to agent harnesses (where safety, latency, and side effects matter) is contested — see [[Agentic Harness]] and Manus's static-action-space view.
