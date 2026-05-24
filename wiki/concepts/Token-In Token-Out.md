---
type: concept
title: Token-In Token-Out
created: 2026-05-24
updated: 2026-05-24
tags:
  - llm
  - rl
  - infrastructure
  - tokenization
  - agentic-rl
status: developing
related:
  - "[[Trainer-Sampler Determinism]]"
  - "[[KV-Cache Discipline]]"
  - "[[Reward Hacking]]"
aliases:
  - TITO
  - Token-In, Token-Out
  - prefix continuity
sources:
  - "[[2026-05-12 - Prime Intellect - Renderers]]"
---

# Token-In Token-Out

A design principle for agentic RL infrastructure: the inference server should be a **byte-faithful Token-In, Token-Out endpoint** — it receives token ids, returns token ids, and never round-trips model output through parsed-and-re-rendered intermediate objects. Introduced as the rationale for [[Prime Intellect]]'s `renderers` library ([[2026-05-12 - Prime Intellect - Renderers]]).

## The problem it solves

In a conventional **message-in, token-out** pipeline, the server applies a chat template, tokenizes, samples, then **parses** the completion into structured objects (tool calls, message dicts) and **re-serializes** for the next turn. Each round-trip can silently change token identity — `False` becomes `false`, whitespace shifts, delimiters normalize. The damage:

> "Once the model's sampled bytes have been parsed, normalized, detokenized, and re-rendered, token identity has already been put at risk."

For RL this is fatal: **"on-policy" silently assumes the trainer sees exactly the tokens the sampler emitted.** Mutated tokens break that assumption without any error surfacing.

## The mechanism — model-specific renderers

A renderer encodes one model family's exact framing (role markers, tool delimiters, reasoning blocks, truncation handling) as code, exposing:

- `render()` / `render_ids()` — messages → tokens, plus `message_indices` for **single-pass loss-mask** construction.
- `parse_response()` — recover messages by recognizing **special-token ids**, not regex on decoded text (no delimiter false positives).
- `bridge_to_next_turn()` — the load-bearing operation: the result **starts with `previous_prompt_ids + previous_completion_ids` byte-for-byte**, then appends new env messages + the next assistant opener.

**Prefix continuity** is the payoff: a multi-turn rollout becomes a single contiguous training sequence, eliminating the need to fragment samples at prefix breaks — roughly **3x less compute** than naive re-rendering.

## Connections

- **Same stance as [[Thinking Machines Lab]]'s numerics work.** This is the agentic-RL analog of [[Defeating Nondeterminism in LLM Inference]] / [[Trainer-Sampler Determinism]]: both insist sampler and trainer must see identical bytes or the training signal is corrupted.
- RL-training-side mirror of inference-side [[KV-Cache Discipline]] — both are "don't mutate the token stream."
- A clean reward signal (no token corruption) is upstream of avoiding spurious [[Reward Hacking]] — though they address different layers.

## Open questions

- How much measured RL-quality improvement (not just compute savings) comes from byte-faithfulness at frontier scale?
- Does the per-model hand-coded renderer approach scale as new model families proliferate, or does it need a learned/derived fallback?
