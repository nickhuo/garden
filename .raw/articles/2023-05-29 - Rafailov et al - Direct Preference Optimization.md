---
source_url: https://arxiv.org/abs/2305.18290
fetched: 2026-06-02
---

# Direct Preference Optimization: Your Language Model is Secretly a Reward Model

**Authors:** Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, Chelsea Finn (Stanford University)
**Submitted:** 2023-05-29 (rev. 2024-07-29). NeurIPS 2023 (Outstanding Paper / runner-up).
**arXiv:** 2305.18290

## Abstract (verbatim)

While large-scale unsupervised language models (LMs) learn broad world knowledge and some reasoning skills, achieving precise control of their behavior is difficult due to the completely unsupervised nature of their training. Existing methods for gaining such steerability collect human labels of the relative quality of model generations and fine-tune the unsupervised LM to align with these preferences, often with reinforcement learning from human feedback (RLHF). However, RLHF is a complex and often unstable procedure, first fitting a reward model that reflects the human preferences, and then fine-tuning the large unsupervised LM using reinforcement learning to maximize this estimated reward without drifting too far from the original model. In this paper we introduce a new parameterization of the reward model in RLHF that enables extraction of the corresponding optimal policy in closed form, allowing us to solve the standard RLHF problem with only a simple classification loss. The resulting algorithm, which we call Direct Preference Optimization (DPO), is stable, performant, and computationally lightweight, eliminating the need for sampling from the LM during fine-tuning or performing significant hyperparameter tuning. Our experiments show that DPO can fine-tune LMs to align with human preferences as well as or better than existing methods. Notably, fine-tuning with DPO exceeds PPO-based RLHF in ability to control sentiment of generations, and matches or improves response quality in summarization and single-turn dialogue while being substantially simpler to implement and train.

## Key technical contributions

- **Closed-form optimal policy.** The standard RLHF objective (maximize reward minus β·KL to a reference policy `π_ref`) has a known closed-form solution: `π*(y|x) ∝ π_ref(y|x) · exp(r(x,y)/β)`. Inverting this gives the reward implied by any policy: `r(x,y) = β·log(π(y|x)/π_ref(y|x)) + β·log Z(x)`.
- **"Your LM is secretly a reward model."** Substituting that reward expression into the Bradley–Terry preference model makes the partition function `Z(x)` cancel for a preference pair, yielding a loss on the policy directly:
  `L_DPO = −E_{(x, y_w, y_l)}[ log σ( β·log(π_θ(y_w|x)/π_ref(y_w|x)) − β·log(π_θ(y_l|x)/π_ref(y_l|x)) ) ]`
  where `y_w` is the preferred and `y_l` the dispreferred completion.
- **Eliminates the RL loop.** No separately-trained reward model, no sampling from the LM during fine-tuning, no on-policy RL (no PPO). DPO reduces RLHF to a single supervised, binary-classification-style objective on preference pairs.
- **Implicit reward.** The trained policy *implicitly* defines a reward via its log-ratio to the reference — the foundation later reused by online/iterative DPO and self-rewarding methods.
- **Gradient intuition.** The DPO gradient up-weights preferred completions and down-weights dispreferred ones, scaled by how wrong the implicit reward model currently is.

## Experiments / results

- **Sentiment control** (IMDb): DPO exceeds PPO-based RLHF on the reward/KL frontier.
- **Summarization** (TL;DR) and **single-turn dialogue** (Anthropic HH): DPO matches or beats PPO-RLHF in win-rate, while being far simpler and more stable, with little hyperparameter tuning.
