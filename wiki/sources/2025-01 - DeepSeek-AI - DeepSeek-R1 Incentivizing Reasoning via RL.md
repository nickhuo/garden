---
type: source
title: "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning"
created: 2026-05-31
updated: 2026-05-31
tags: [llm, reinforcement-learning, reasoning, distillation, rlvr, training]
status: mature
source_type: paper
authors: ["DeepSeek-AI", "Daya Guo", "Dejian Yang", "Haowei Zhang", "Junxiao Song", "Zhihong Shao", "Peiyi Wang", "et al. (199+)"]
venue: "Nature 645, 633–638 (2025); doi:10.1038/s41586-025-09422-z (orig. arXiv 2025-01-22)"
arxiv: "2501.12948v2"
url: https://arxiv.org/abs/2501.12948
code: https://huggingface.co/deepseek-ai
pdf: "[[2025-01 - DeepSeek-AI - DeepSeek-R1 Incentivizing Reasoning via RL.pdf]]"
seed_score: 14/14
confidence: high
cited_sources: []
related: ["[[DeepSeek]]", "[[DeepSeek-R1-Zero]]", "[[GRPO]]", "[[RL with Verifiable Rewards]]", "[[Reasoning Distillation]]", "[[Verifiability]]", "[[On-Policy Distillation]]", "[[The Bitter Lesson]]"]
sources: []
---

# DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning

> [!key-insight] Core claim
> Frontier **reasoning** can be *incentivized by pure reinforcement learning* on a strong base model — **no human-labeled reasoning traces, no SFT warm-up**. Given only a rule-based reward on final-answer correctness, [[DeepSeek-R1-Zero]] *autonomously* develops self-reflection, verification, and alternative-strategy exploration (the "**aha moment**"), and its AIME-2024 pass@1 climbs **15.6% → 77.9%** (86.7% with majority vote) over training. A second, multi-stage model **DeepSeek-R1** then reaches **OpenAI-o1-1217 parity** on math/code while fixing readability, and its reasoning **distills** into small models that beat much larger non-reasoning baselines.

## What it is

A research paper from **[[DeepSeek]]** (DeepSeek-AI, 199+ authors; core contributors Daya Guo, Peiyi Wang, Junxiao Song, **Zhihong Shao**, et al.). Originally posted to arXiv 2025-01-22; this ingest is the **peer-reviewed Nature version** (v2, *Nature* 645:633–638, 2025), which adds detail and reframes some sections vs. the original preprint. Both R1-Zero and R1 are built on **DeepSeek-V3-Base** (671B-param MoE, 37B activated, 14.8T-token pretrain) and use **[[GRPO]]** as the RL algorithm. Models released openly on HuggingFace, including a family of distilled checkpoints.

> [!note] Why this ingest matters for the wiki
> The wiki has cited **[[GRPO]]** and **RLVR** across [[GEPA]], [[Verifiability]], [[On-Policy Distillation]], and [[Reward Hacking]] without ever sourcing the paradigm's canonical large-scale demonstration. R1 is that demonstration — the **lineage anchor** for *RL-for-reasoning* in the [[LLM]] domain.

## DeepSeek-R1-Zero — pure RL, no SFT

The headline result. Take DeepSeek-V3-Base, skip SFT entirely, and run [[GRPO]] with a **[[Rule-Based Rewards|rule-based reward]]** = accuracy (boxed-answer match for math; compiler/test-cases for code) **+ format** (reasoning must sit inside `<think>…</think>`, answer inside `<answer>…</answer>`). No neural reward model — the authors deliberately avoid outcome/process RMs as **[[Reward Hacking|reward-hackable]]** at scale.

- **AIME-2024 pass@1: 15.6% → 77.9%** across ~10,400 steps (1.6 epochs); **86.7%** with self-consistency (cons@16) — above the average human competitor.
- **Emergent behaviors, not taught.** Response length grows from hundreds to thousands of tokens *on its own*; the model learns to verify, reflect, and explore alternatives. The "**aha moment**": a sudden spike in the word *"wait"* during reflection (Table 2 — "Wait, wait. Wait. That's an aha moment I can flag here.").
- **Hyperparameters:** lr 3e-6, KL coef 0.001, temp 1.0, 16 samples/question, max length 32,768 → 65,536 tokens after step 8.2k (a visible performance + length jump at that point), batch 512, reference model refreshed every 400 steps.
- **Limitations of R1-Zero:** poor readability, **English/Chinese language mixing**, and a narrow reasoning-only competence. These motivate the full R1 pipeline.

Full concept: [[DeepSeek-R1-Zero]].

## DeepSeek-R1 — the 4-stage pipeline

To fix R1-Zero's readability/generality while keeping its reasoning, R1 interleaves SFT and RL (Figure 2):

1. **Cold start** — SFT DeepSeek-V3-Base on a few thousand curated long-CoT samples with a clean, human-aligned thinking format (→ Dev1).
2. **Reasoning-oriented RL** — GRPO with rule-based reward **+ a language-consistency reward** (fraction of target-language words in the CoT; a small accuracy cost the authors accept for readability). lr 3e-6, large clip ε, 1,700+ steps (→ Dev2).
3. **Rejection sampling + SFT** — sample from the RL model, keep good traces, mix with **non-reasoning** data (writing, QA) from the DeepSeek-V3 SFT set (→ Dev3).
4. **All-scenarios RL** — final GRPO combining rule-based reasoning reward + **model-based helpful/safety reward models** (66k helpful preference pairs, 106k safety prompts) + format/language rewards; preference reward applied only in the last 400 steps to limit reward hacking; temp lowered to 0.7 (→ **DeepSeek-R1**).

Per-stage scores (Table 3) show the trade-off cleanly: reasoning-RL (Dev2) jumps AIME/code but barely moves AlpacaEval; the final stage's gains are mostly **general instruction-following / preference** (AlpacaEval +25%, ArenaHard +17%) with marginal further math/code change.

## Headline numbers vs OpenAI-o1-1217 (Table 8)

| Benchmark | DeepSeek-R1 | OpenAI-o1-1217 | o1-mini | DeepSeek-V3 |
|---|---|---|---|---|
| AIME 2024 (pass@1) | **79.8** | 79.2 | 63.6 | 39.2 |
| MATH-500 (pass@1) | **97.3** | 96.4 | 90.0 | 90.2 |
| GPQA Diamond (pass@1) | 71.5 | **75.7** | 60.0 | 59.1 |
| LiveCodeBench (pass@1-CoT) | **65.9** | 63.4 | 53.8 | 36.2 |
| Codeforces (percentile) | 96.3 | **96.6** | 93.4 | 58.7 |
| SWE-bench Verified | **49.2** | 48.9 | 41.6 | 42.0 |
| Aider-Polyglot | 53.3 | **61.7** | 32.9 | 49.6 |
| MMLU (EM) | 90.8 | **91.8** | 85.2 | 88.5 |

Read: **math/competition-code parity-or-better with o1-1217**; o1 still leads on GPQA, MMLU, and engineering-coding (Aider). R1 is a 671B MoE (37B activated), same as V3 — the gap over V3 is *almost entirely the RL*.

## Reasoning distillation — and "distillation > RL at small scale"

R1's reasoning **transfers** by plain SFT on **800k R1-generated samples** into open bases (Qwen2.5-Math-1.5B/7B, Qwen2.5-14B/32B, Llama-3.1-8B, Llama-3.3-70B). No RL stage on the students — SFT only — yet (Table 15):

- **R1-Distill-Qwen-1.5B** beats GPT-4o-0513 and Claude-3.5-Sonnet on AIME/MATH (28.9 / 83.9 vs 9.3 / 74.6 and 16.0 / 78.3).
- **R1-Distill-Qwen-32B**: AIME 72.6, MATH 94.3, GPQA 62.1 — approaching R1 itself.
- **R1-Distill-Llama-70B**: AIME 70.0, MATH 94.5, LiveCodeBench 65.2.

> [!key-insight] Distillation beats small-model RL
> Running large-scale RL *directly* on Qwen2.5-32B-Base (→ "Qwen2.5-32B-Zero") only matches QwQ-32B-Preview, while **R1-Distill-Qwen-32B beats it across every benchmark** (Table 16). Conclusion: *distilling a powerful model into a small one is far cheaper and stronger than RL-ing the small one* — small-model pure-RL "may not even achieve the performance of distillation." But pushing **past** the teacher still needs bigger bases + larger-scale RL. See [[Reasoning Distillation]] and contrast [[On-Policy Distillation]] (which grades student rollouts via teacher KL rather than SFT-on-samples).

## Unsuccessful attempts (Appendix G.2)

Two approaches the team tried and abandoned — useful negative results:

- **Process Reward Models (PRM):** hard to define a fine-grained "step," hard to label step-correctness (auto-labels weak, manual doesn't scale), and any model-based PRM invites **reward hacking** + retraining cost. PRM still useful for *reranking / guided search*, but not worth the overhead inside large-scale RL.
- **Monte Carlo Tree Search (MCTS):** token-generation's search space is exponentially larger than Go's; node-expansion caps cause local optima; a fine-grained **value model** (the crux of AlphaGo's success) is very hard to train for tokens. MCTS can help at inference with a pretrained value model, but **self-search iterative improvement didn't scale**.

## Other findings worth keeping

- **Base capacity gates RL** (G.1): 7B-dense and 16B-MoE bases *failed* to benefit from pure RL (fell into repetition); only 32B / 230B / 671B bases showed the gains. RL-from-base efficacy is "highly dependent on underlying model capacity."
- **Verifiers are the load-bearing piece** (G.1): rule-based RMs and LLM-graded ground-truth correctness are the two robust, hard-to-hack reward sources; both degrade on open-ended/long-form tasks where "correctness" is subjective — the open frontier.
- **Pre-o1 control:** Qwen2-Math-7B-Zero (trained Aug-2024, before o1) self-developed reasoning via RL, ruling out "the base already saw o1 traces" as the explanation.

## Limitations (the paper's own list)

Structured output & **tool use** still weak (R1 can't call search/calculators); **token efficiency** (overthinks easy questions); **language mixing** beyond zh/en; **prompt sensitivity** (few-shot *degrades* it — use zero-shot); **software-engineering** gains limited by slow RL eval loops; and the deeper **reward-hacking** ceiling — pure RL only scales where a *reliable* verifier exists, which excludes writing and other subjective tasks.

## Why it matters for this wiki

- The **primary, large-scale evidence** for **[[RL with Verifiable Rewards]]** that the [[Verifiability]] / [[GEPA]] / [[Reward Hacking]] cluster has been citing in the abstract. R1-Zero is RLVR's existence proof; R1 is its productionization.
- Sharpens **[[GRPO]]** from a secondary reference into a sourced, fully-specified algorithm (objective + group-relative advantage + the "large PPO clip" refinement).
- Gives **[[On-Policy Distillation]]** a real-world foil: R1 shows *SFT-on-samples* distillation already beats small-model RL; TML's on-policy variant is the denser-signal successor.
- Reinforces **[[The Bitter Lesson]]** — minimal hand-design ("hard questions + reliable verifier + compute"), let RL find non-human reasoning paths.

## Lineage / 引用脉络

R1 *is* the primary source. Its load-bearing **uncited-in-wiki upstream** is the GRPO algorithm itself:

- **GRPO — Shao et al. 2024 (DeepSeekMath, arXiv 2402.03300)** — the actual primary for [[GRPO]], still **not ingested**. R1 specifies GRPO's objective inline, but the GRPO page's "primary not yet ingested" gap remains. **Top citation-chase candidate** (would pass the gate easily) — flagged for Nick rather than auto-fetched, consistent with recent ingests.
- **PPO — Schulman et al. 2017**; **RLHF/InstructGPT — [[2022-03-04 - Ouyang et al - InstructGPT]]** (already filed) — the RL-alignment lineage GRPO simplifies.
- **CoT — Wei et al. 2022b**; **self-consistency — Wang et al. 2023b**; **[[Tree of Thoughts]] — Yao et al. 2023a** — the prompt-era reasoning antecedents R1 supersedes with learned (not prompted) reasoning.
- **Distillation — Hinton et al. 2015; Busbridge et al. 2025** — classical KD basis for [[Reasoning Distillation]].

**Citation chase: none built this run.** GRPO-primary (DeepSeekMath) is the standout next target.
