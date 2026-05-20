# Interaction Models: A Scalable Approach to Human-AI Collaboration

**Author:** Thinking Machines Lab
**Date Published:** May 11, 2026
**URL:** https://thinkingmachines.ai/blog/interaction-models/
**DOI:** 10.64434/tml.20260511

---

## The Collaboration Bottleneck

Contemporary AI development prioritizes autonomous capabilities, often treating human-in-the-loop interaction as secondary. According to the research team, current frontier models demonstrate that "when used in an interactive, synchronous, hands-on-keyboard pattern, the benefits of the model were less clear."

The core issue stems from interface design: humans are excluded not due to technical necessity but because existing systems lack integration points for ongoing feedback. Effective collaboration requires what researchers call copresence, contemporality, and simultaneity — characteristics absent in turn-based AI systems.

Current models operate in single-threaded perception. The model remains idle until users complete input; conversely, user perception freezes during model generation. This narrow bandwidth severely limits knowledge transfer, intent communication, and result comprehension.

The proposed solution involves making "AI interactive in real time across any modality" rather than retrofitting interactivity onto existing architectures. As the team notes, "for interactivity to scale with intelligence, it must be part of the model itself."

## Capabilities

Native interactivity unlocks several interaction modes:

- **Seamless dialog management:** Models track speaker intent implicitly — whether someone is thinking, yielding, self-correcting, or inviting response — without requiring separate dialog components.
- **Verbal and visual interjections:** The model initiates contributions contextually rather than only when users finish speaking.
- **Simultaneous speech:** Users and models can speak concurrently, enabling applications like live translation.
- **Time-awareness:** Models possess direct perception of elapsed time.
- **Concurrent tool operations:** While engaging with users, models can simultaneously search, browse, and generate UI, integrating results into conversation flow.

## Our Approach

### System Overview

The architecture splits responsibilities between two components: an interaction model handling real-time exchange and a background model managing asynchronous reasoning, tool use, and complex planning. The interaction model maintains user presence while the background system operates independently, with results streaming back as they become available.

### The Interaction Model

Three key technical innovations:

- **Time-aligned micro-turns:** 200ms chunks of continuous input and output rather than discrete user turns. Both input and output tokens function as streams, enabling genuine concurrency across modalities without artificial turn boundaries.
- **Encoder-free early fusion:** Minimal preprocessing — audio converts to dMel representations via lightweight embedding layers; images split into 40×40 patches encoded through hMLP. All components train end-to-end with the transformer.
- **Inference optimization:** Persistent streaming sessions where clients send 200ms chunks as separate requests, with the server appending sequences into GPU memory. Eliminates repeated memory allocations and metadata computations. Contributed to SGLang.

Additional details:

- **Trainer-sampler alignment:** Bitwise determinism across training and sampling improves stability with <5% performance overhead.
- **Communication kernels:** NVLS for low-latency deterministic all-reduce/reduce-scatter on Blackwell.
- **Attention optimization:** Consistent split-KV accumulation ordering between decode and prefill phases.

**Coordination:** When deeper reasoning is required, the interaction model delegates while remaining engaged. Transmits complete conversation context. Results stream back and integrate at contextually appropriate moments.

**Safety:** Modality-appropriate refusal generation using TTS covering disallowed topics, calibrated for colloquial but firm responses. Multi-turn robustness enhanced through automated red-teaming.

## Benchmarks

### Intelligence and Interactivity Frontier

`TML-Interaction-Small` achieves simultaneous performance across intelligence and interaction dimensions. Evaluation uses FD-bench and Audio MultiChallenge.

Key results:

- FD-bench V1 Turn-taking latency: 0.40s (audio)
- FD-bench V1.5 Average: 77.8 (audio)
- Audio MultiChallenge APR: 43.4%
- IFEval (Text): 89.7%
- Harmbench Refusal Rate: 99.0%

### New Dimensions of Interactivity

Specialized evaluations:

- **TimeSpeak:** Does the model initiate speech at user-specified times with correct content?
- **CueSpeak:** Does the model respond at appropriate moments with semantically correct outputs?
- **RepCount-A:** Continuous visual tracking and timely numerical output.
- **ProactiveVideoQA:** Answer questions when visual evidence becomes available.
- **Charades:** Temporal action-localization.

Performance on novel tasks (TML vs GPT Realtime-2.0 minimal):

- TimeSpeak: 64.7% vs 4.3%
- CueSpeak: 81.7% vs 2.9%
- RepCount-A off-by-one: 35.4% vs 1.3%
- ProactiveVideoQA: 33.5 PAUC vs 25.0
- Charades mIoU: 32.4 vs 0%

## Limitations and Future Work

- **Long sessions:** Continuous audio/video accumulates context fast; context management is an active research focus.
- **Compute and deployment:** Low-latency streaming demands reliable connectivity.
- **Alignment and safety:** Real-time interaction opens novel research directions.
- **Scaling model size:** Current `TML-Interaction-Small` is 276B parameters (12B active). Larger versions planned.
- **Improved background agents:** Significant unexplored potential in coordinating background agents with interaction models.

## Citation

```bibtex
@article{thinkingmachines2026interactionmodels,
  author = {Thinking Machines Lab},
  title = {Interaction Models: A Scalable Approach to Human-AI Collaboration},
  journal = {Thinking Machines Lab: Connectionism},
  year = {2026},
  month = {May},
  note = {https://thinkingmachines.ai/blog/interaction-models/},
  doi = {10.64434/tml.20260511},
}
```
