# LoRA Without Regret

**Author:** John Schulman (Thinking Machines Lab)
**Date Published:** September 29, 2025
**URL:** https://thinkingmachines.ai/blog/lora/
**DOI:** 10.64434/tml.20250929

---

## What matters for LoRA

Key findings:

- LoRA matches full fine-tuning efficiency on small-to-medium instruction-tuning and reasoning datasets
- Performance degrades when dataset size exceeds LoRA capacity
- LoRA shows reduced tolerance for large batch sizes (a property of the product-of-matrices parametrization, not rank)
- Applying LoRA across **all** weight matrices (especially MLP and MoE layers) significantly outperforms attention-only
- LoRA achieves equivalent performance to full fine-tuning in RL **even with minimal ranks**

## Methods and Results

### LoRA Rank

Llama 3 and Qwen3 on Tulu3 and OpenThoughts3: "FullFT and high-rank LoRAs have similar learning curves with loss decreasing linearly with the logarithm of steps." Lower-rank adapters fell off minimum-loss curves when capacity constraints emerged.

Optimal LR for FullFT was ~10x lower than for high-rank LoRA. LR remained relatively consistent across ranks (<2x variation between rank 4 and rank 512).

### Batch Size Effects

The gap in loss for LoRA increasingly diverges from FullFT for larger batch sizes — independent of rank. Inherent property of the parametrization.

### Layers Where LoRA Is Applied

Contradicts earlier guidance favoring attention-only LoRA. "Attention-only LoRA significantly underperforms MLP-only LoRA" even at equivalent parameter counts. Attention-only rank-256 underperformed MLP-only rank-128 (0.25B vs 0.24B params).

LoRA on all layers — especially MLPs and MoE layers containing most parameters — consistently outperformed restricted approaches. Held across dense (Llama-3.1-8B) and sparse (Qwen3-30B MoE).

### Reinforcement Learning

Striking result: "LoRA fully matches the learning performance of FullFT when running policy gradient algorithms for reinforcement learning, even with ranks as low as 1."

Information-theoretic explanation: policy gradient absorbs ~1 bit/episode vs O(tokens) bits in SL. MATH dataset (~10k problems, 32 samples each) → only 320k bits — far less than rank-1 LoRA's 3M params.

## Setting LoRA Hyperparameters

### Optimal Learning Rate and Rank

Parametrization $W' = W + \frac{\alpha}{r}BA$ with $\alpha = 32$: "the optimal learning rate for LoRA is approximately independent of rank." The $1/r$ scaling ensures expected updates per rank-1 component remain constant.

### Parametrization Invariances

Training dynamics invariant under transformations of (α, LR_A, LR_B, init_A):
- α → (1/pq) · α
- init_A → p · init_A
- LR_A → p · LR_A
- LR_B → q · LR_B

Reduces effective param space to two dimensions. Standard HuggingFace implementation proved optimal.

### LoRA vs FullFT Learning Rates

Across 14 Llama/Qwen models: "the optimal LR for LoRA is consistently 10x the one used for FullFT in the same application." Held for both SL and RL.

Predictive model:
LR = M_LoRA · (2000/hidden_size)^(model_pow + LoRA_pow)

Convergence: 9.8x multiplier for LoRA over FullFT.

### Short vs Long Runs

B init to zero creates implicit LR schedule. Optimal LR ~15x for short runs (<100 steps), declining to standard 10x as training extends. By end of full runs, B matrices ended up with larger spectral norms than A.

## Discussion

### Why LoRA Needs All Layers

Empirical neural tangent kernel (eNTK): layers with most parameters dominate kernel computation. With LoRA on all layers: "LoRA training ≈ eNTK(LoRA) ≈ eNTK(FullFT) ≈ FullFT." Attention-only breaks this.

### Information Capacity

NN store ~2 bits/parameter under optimal conditions. LM datasets typically ~1 bit/token. For policy gradient RL: $I(G; R | \text{history}) \lesssim \log(B)$ → useful info per episode is O(1) regardless of model size.

### Computational Efficiency

LoRA: ~2/3 the FLOPs of FullFT per pass.

FullFT forward-backward on $W \in \mathbb{R}^{N \times N}$: $3N^2$ multiply-adds.
LoRA ($B \in \mathbb{R}^{N \times R}$, $A \in \mathbb{R}^{R \times N}$, $R \ll N$): $2N^2 + 6NR \approx (2/3) \cdot 3N^2$.

### Open Questions

- Sharpening predictions of LoRA capacity boundaries
- Stronger theoretical explanation for 10x LR ratio
- Evaluating LoRA variants (PiSSA) under equivalent conditions
- LoRA on MoE layers and parallelism schemes

## Closing

Establishes a "low-regret regime" where LoRA performs comparably to full fine-tuning across most post-training scenarios.

## Citation

```bibtex
@article{schulman2025lora,
  author = {John Schulman and Thinking Machines Lab},
  title = {LoRA Without Regret},
  journal = {Thinking Machines Lab: Connectionism},
  year = {2025},
  note = {https://thinkingmachines.ai/blog/lora/},
  doi = {10.64434/tml.20250929},
}
```
