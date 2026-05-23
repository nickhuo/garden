---
type: source
title: "Software 2.0"
source_type: essay
author: "Andrej Karpathy"
date_published: 2017-11-11
url: "https://karpathy.medium.com/software-2-0-a64152b37c35"
created: 2026-05-20
updated: 2026-05-20
status: mature
confidence: high
key_claims:
  - "Neural networks are a new software stack: the program is the weights, learned from data, not hand-written rules."
  - "In Software 2.0 a human specifies a goal and a dataset; optimization (backprop + SGD) searches program space for an implementation."
  - "Software 2.0 wins on computational homogeneity, constant runtime/memory, agility, and perception performance."
  - "Costs: models are opaque, can fail in unintuitive ways, silently absorb data biases, and are vulnerable to adversarial examples."
tags:
  - ai-agents
  - llm
  - foundational
  - architecture
related:
  - "[[Software 2.0]]"
  - "[[Model-Centric Architecture]]"
  - "[[The Bitter Lesson]]"
sources: []
---

# Software 2.0

Andrej Karpathy, November 11, 2017 (Medium). Introduced the framing that neural nets are not just a tool inside the old software stack but a new stack of their own.

## Core thesis

In **Software 1.0**, humans write explicit instructions in source code. In **Software 2.0**, the "code" is the **weights of a neural network**, written in "much more abstract, human unfriendly language." The developer specifies a goal and a rough architecture (which carves out a subset of program space), then uses compute to search that space via backpropagation and SGD for a program that works.

## Why weights beat code

- **Homogeneous computation** — matrix multiplies; simpler to bake into hardware.
- **Constant runtime / memory** — predictable performance per forward pass.
- **Agility** — scale the net up or down by adjusting width/depth.
- **Cross-module optimization** — backprop optimizes across boundaries that hand-written modules can't.
- **Better at perception** — already superhuman in image/video/audio domains.

## Acknowledged limits

Models "fail in unintuitive and embarrassing ways," silently adopt dataset biases, are opaque, and are vulnerable to adversarial examples. These are the costs of moving logic from inspectable code into learned weights.

## Relevance to agents

The architectural ancestor of [[Model-Centric Architecture]]: logic migrates out of hand-written code and into the model. Karpathy's later "Software Is Changing (Again)" (2025) extends this to **Software 3.0** — programming the model in English prompts and treating LLMs as an operating system. Concept page: [[Software 2.0]]. Entity: [[Andrej Karpathy]].
