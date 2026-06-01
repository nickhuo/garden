---
source_url: https://www.primeintellect.ai/blog/renderers
fetched: 2026-05-24
author: Prime Intellect Team
date_published: 2026-05-12
---

# renderers: Token-Level Templating for Agentic RL

Open-sourced `renderers`, a Python library for maintaining token-level consistency across multi-turn conversations in RL with language models.

## The problem (three stages)

1. **Message-In, Token-Out** — conventional: send message dicts to inference server, apply chat template, tokenize, sample, parse tool calls, return structured responses. Creates failures when model outputs are parsed into Python objects (`False` instead of `false`) then re-serialized. "Once the model's sampled bytes have been parsed, normalized, detokenized, and re-rendered, token identity has already been put at risk."
2. **Generic Token-In, Token-Out** — token-based prompts preserve sampled completions but bridging turns required inferring tokens via a "dummy assistant" rendering trick, which failed when chat templates depended on global conversation shape.
3. **renderers** — explicitly encode model-specific knowledge into Python objects; replace inference-by-guesswork with deterministic token operations.

## Protocol (five methods)

- `render()` / `render_ids()` — messages → token sequences, returning `message_indices` for loss-mask construction.
- `parse_response()` — recover structured messages from token ids via special-token recognition (not regex).
- `get_stop_token_ids()` — stopping criteria.
- `bridge_to_next_turn()` — extends prior sampled tokens with new environment messages. Guarantees: result starts with `previous_prompt_ids + previous_completion_ids` byte-for-byte, continues with new messages + next assistant opener.

## Technical benefits

- **Prefix continuity** — multi-turn rollouts become a single contiguous training sequence (`prompt_ids_1 + completion_ids_1 + continuation_ids_2 + ...`). Eliminates fragmenting training samples at prefix breaks, ~3x less compute vs naive approaches.
- **Loss masking** — `message_indices` enables single-pass loss-mask construction without re-rendering or string diffing.
- **ID-level parsing** — scanning special-token ids avoids false positives from literal strings matching delimiters.

## Bridge mechanism (three operations)

1. **Anchors** at previous turn's close token, synthesizing canonical closure when truncated.
2. **Refuses** assistant content in extensions; accepts only tool outputs and user follow-ups.
3. **Renders** new messages using exact model-family framing.

## Implementation

Hand-coded renderers for Qwen3, Qwen3.5, GLM-4.5, GLM-5, MiniMax-M2, DeepSeek-V3, Kimi K2/K2.5, Nemotron-3, GPT-OSS, plus fallback. `pip install renderers`; integrates with `verifiers` and `prime-rl`. Partnerships with NVIDIA, vLLM, SGLang.

## Principle

"For agentic RL, the inference server should be a simple Token-In, Token-Out endpoint." Harnesses and chat templates must remain information-preserving or explicitly document deviations from sampled history — preventing silent mutations that break reproducibility.
