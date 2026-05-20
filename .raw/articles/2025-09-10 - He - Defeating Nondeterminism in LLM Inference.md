# Defeating Nondeterminism in LLM Inference

**Author:** Horace He in collaboration with others at Thinking Machines Lab
**Date Published:** September 10, 2025
**URL:** https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/
**DOI:** 10.64434/tml.20250910

---

## The Original Sin: Floating-Point Non-Associativity

Floating-point math: "(a + b) + c ≠ a + (b + c)" due to finite precision and rounding. Numbers like mantissa × 10^exponent — when adding numbers with different exponents, precision is lost (e.g., 1230 + 23.4 rounds to 1250 under three-digit precision).

Test: summing [1e-10, 1e-5, 1e-2, 1] and their negatives in random orders produces 102 unique results across 10,000 iterations.

## Why Don't Kernels Always Add Numbers in the Same Order?

Common "concurrency + floating point" hypothesis is incomplete. Simple matrix multiplications on GPUs produce bitwise identical results repeatedly, despite floating-point and concurrent hardware.

## When Are Atomic Adds Needed?

Atomic adds genuinely nondeterministic (no ordering guarantee). Largely unnecessary for typical NN ops because:

1. Sufficient parallelism along the batch dimension
2. Modern libraries use split (tree) reductions and semaphores

**The forward pass of LLM inference contains virtually no operations requiring atomic adds** — individual forward passes are "run-to-run deterministic."

### Batch Invariance and "Determinism"

The crucial issue: **batch invariance**. Kernels often produce different results depending on batch size, even though mathematically they should be independent.

```python
import torch
torch.set_default_device('cuda')
B, D = 2048, 4096
a = torch.linspace(-1000, 1000, B*D).reshape(B, D)
b = torch.linspace(-1000, 1000, D*D).reshape(D, D)
out1 = torch.mm(a[:1], b)  # Single element
out2 = torch.mm(a, b)[:1]  # Batch then slice
print((out1 - out2).abs().max())  # 1669.25
```

"The primary reason nearly all LLM inference endpoints are nondeterministic is that the load (and thus batch-size) nondeterministically varies."

## How Do We Make Kernels Batch-Invariant?

Three reduction-based ops: RMSNorm, matmul, attention.

### RMSNorm

`x * rsqrt(mean(x², dim=-1, keepdim=True)) * weight`. Data-parallel: one batch element per core. When batches exceed cores, sequential per core. Small batches challenging — splitting breaks invariance.

### Matrix Multiplication

Chunk output into 2D tiles, one per core. Two batch dimensions (M, N) plus tensorcore requirements complicate things. Split-K breaks invariance. Tradeoff: ~20% perf loss vs cuBLAS. Consistent tensor-core instruction selection required.

### Attention

Two complications: reducing over both feature and sequence dimensions, plus inference optimizations (chunked prefill, prefix caching).

Key insight: "when processing the 1000th query token in a sequence, the reduction order must be identical regardless of whether 0 tokens are in the KV cache (prefill) or 999 tokens are in the KV cache (decoding)."

Update KV cache + page tables before attention. Use "fixed split-size" instead of dynamic FlashDecoding splits: "If our KV length was 1000, instead of splitting it into four even length 250 splits, we would split it into three fixed-size length 256 splits and one length 232 split."

## Implementation

Batch-invariant kernels via `torch.Library`, integrated with vLLM's FlexAttention backend. Code: `thinking-machines-lab/batch_invariant_ops`.

## Experiments

### How Nondeterministic Are Completions?

Qwen3-235B-A22B-Instruct on "Tell me about Richard Feynman", 1000 tokens, T=0:

- Standard: 80 unique completions / 1000 samples; most common appears 78 times
- Divergence at token 103 (992 say "Queens, New York", 8 say "New York City")
- With batch-invariant kernels: **all 1000 completions identical**

### Performance

Qwen-3-8B, 1000 sequences, 90-110 tokens output:

| Configuration | Time (s) |
|---|---|
| vLLM default | 26 |
| Unoptimized deterministic vLLM | 55 |
| + Improved attention kernel | 42 |

Degradation primarily from incomplete FlexAttention optimization in vLLM.

### True On-Policy RL

Nondeterministic inference implicitly converts on-policy RL to off-policy RL. With deterministic inference enabling identical numerics between sampler and trainer, true on-policy RL is achievable.

Bigmath RLVR:
- Without batch-invariant + off-policy correction: KL ~0.001 with spikes; reward eventually crashes
- Without batch-invariant, no correction: reward crashes with KL spikes ~step 318
- **With batch-invariant: KL exactly 0 throughout training**

## Conclusion

Reject papering-over of nondeterminism in ML. "With a little bit of work, we can understand the root causes of our nondeterminism and even solve them!" Through careful kernel design prioritizing batch invariance, deterministic inference is achievable without prohibitive performance costs.

## Citation

```bibtex
@article{he2025nondeterminism,
  author = {Horace He and Thinking Machines Lab},
  title = {Defeating Nondeterminism in LLM Inference},
  journal = {Thinking Machines Lab: Connectionism},
  year = {2025},
  note = {https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/},
  doi = {10.64434/tml.20250910}
}
```
