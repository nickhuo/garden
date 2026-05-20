# On-Policy Distillation

**Author:** Kevin Lu in collaboration with others at Thinking Machines Lab
**Date Published:** October 27, 2025
**URL:** https://thinkingmachines.ai/blog/on-policy-distillation/
**DOI:** 10.64434/tml.20251026

---

## On-policy distillation — best of both worlds

On-policy distillation combines sampling trajectories from the student model while using a teacher to grade each token. This approach merges the advantages of on-policy training — where students learn from their own mistakes — with dense reward signals typical of distillation methods.

The core methodology: initialize a teacher client, sample rollouts from the student, compute reverse KL divergence rewards, and train via policy gradient updates. "On-policy" relevance + "dense" supervision.

## Implementation

### Loss function: reverse KL

Per-token reverse KL between student (π_θ) and teacher (π_teacher):

KL(π_θ || π_teacher) = E_x~π_θ [log π_θ(x_{t+1} | x_{1..t}) - log π_teacher(x_{t+1} | x_{1..t})]

Reverse KL is "mode seeking" and "unhackable" — low KL always indicates desirable teacher behavior. Requires just one forward pass from the teacher.

### Illustration

Uses a SimpleBench physics question where a student incorrectly treated an ice-melting problem as pure mathematics. Teacher penalized tokens initiating incorrect reasoning paths — corresponding to "forking tokens" that guide reasoning.

### Pseudocode

1. Create a teacher client via the Tinker API
2. Sample trajectories from the student model
3. Query the teacher's logprobs on sampled sequences
4. Set per-token advantages to negative reverse KL and train using RL

## Distillation for reasoning

### Off-policy distillation baseline

Qwen3-8B-Base on 400k examples from OpenThoughts-3 → 60% AIME'24. Predictable log-linear scaling: ~2M prompts to reach 70%.

### RL comparison

Qwen3 technical report: 67.6% AIME'24 using 17,920 GPU hours of RL atop similar SFT init. Approximates the cost of 2M off-policy distillation prompts.

### On-policy distillation results

Starting from the 400k SFT checkpoint, on-policy distillation reaches 70% AIME'24 in ~150 steps. **9–30x cost reduction** depending on whether teacher FLOPs are amortized.

| Method | AIME'24 | Teacher FLOPs | Student FLOPs | Cost vs SFT-2M |
|---|---|---|---|---|
| SFT-400K | 60% | 8.5×10²⁰ | 3.8×10²⁰ | — |
| SFT-2M (extrap) | ~70% | 3.4×10²¹ | 1.5×10²¹ | 1× |
| RL | 68% | — | — | ≈1× |
| On-policy distillation | 70% | 8.4×10¹⁹ | 8.2×10¹⁹ | 9-30× |

## Distillation for personalization

### Training an internal assistant

Combining domain knowledge with post-training behaviors. Two metrics: internal QA (knowledge) and IF-eval (instruction following).

### Knowledge-behavior tradeoff

Fine-tuning Qwen3-8B on internal documents improves knowledge but degrades instruction-following. "No weighting which maintains the original performance on IF-eval" when mixing document and chat for SFT. LoRA constraints are insufficient.

### Recovery via on-policy distillation

After mid-training on a 70-30 document-chat mix, on-policy distillation with the original Qwen3-8B as teacher restores performance:

| Model | Internal QA | IF-eval |
|---|---|---|
| Qwen3-8B | 18% | 85% |
| + midtrain (100%) | 43% | 45% |
| + midtrain (70%) | 36% | 79% |
| + midtrain (70%) + distill | 41% | 83% |

Treats "the language model itself as a reward model, with high-probability behaviors being rewarded."

## Discussion

### Dense supervision efficiency gains

Direct comparison: distillation learns the RL-trained policy "approximately 7-10x faster" in gradient steps, ~50-100x compute efficiency.

### Data reusability

Unlike RL (which often memorizes answers with multi-epoch training), on-policy distillation learns complete distributions. Training on a single prompt for 20 consecutive steps with 256 rollouts/step successfully distills teacher performance.

### Semantic strategy search

RL explores "the space of semantic strategies" rather than raw parameter space. Once a strategy is discovered, distillation provides "a shortcut for learning it" without modeling intermediate strategies.

### Continual learning implications

Standard SFT on a model's own samples degrades performance due to distribution drift. On-policy distillation, with fixed teacher behavior, avoids this — "very promising tool for continual learning."

## Conclusion

On-policy distillation combines "the reliable performance of on-policy training, with the cost-efficiency of a dense reward signal." Achieves frontier capabilities "at a fraction of the cost of frontier high-compute RL runs."

## Citation

```bibtex
@article{lu2025onpolicydistillation,
  author = {Kevin Lu and Thinking Machines Lab},
  title = {On-Policy Distillation},
  journal = {Thinking Machines Lab: Connectionism},
  year = {2025},
  note = {https://thinkingmachines.ai/blog/on-policy-distillation},
  doi = {10.64434/tml.20251026},
}
```
