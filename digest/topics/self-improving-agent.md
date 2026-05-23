---
type: topic
name: "Self-improving Agent"
slug: self-improving-agent
priority: 1
keywords: [self-improvement, recursive-self-improvement, RSI, self-improving, automated-capability-discovery, self-play, agent-loops, meta-learning, continual-learning, online-learning, llm-self-correction, voyager, agent-self-rewarding, self-rewarding-language-model, alphaproof, r1-style, self-refinement]
anti_keywords: [self-help, fine-tuning-tutorial, prompt-engineering-101]
anchors: ["Anthropic Research", "DeepMind", "OpenAI Research", "Andrej Karpathy", "Rich Sutton", "Yoshua Bengio", "Sebastian Raschka"]
related_projects: ["[[Paradigm-Fellowship-2026]]"]
related_goals: [technical-capital, career-ascension, influence-building]
status: active
added: 2026-05-03
notes: "Long-term thesis interest. 当前没有直接活动 project — 但 feeds Paradigm thesis + GitHub portfolio 方向。"
---

# Self-improving Agent

## What I Mean
能在 deployment 后通过自身经验提升能力的 agent —— self-correction、experience replay、self-play、meta-prompt 优化、自我生成训练数据。**不是** 一次性 fine-tuning，**不是** 人工迭代。

## Why This Matters
- **Paradigm thesis 自然延伸**: "reliability layer for crypto-agent systems" 的下一步就是 self-correcting agent
- **GitHub 技术资本**: open-source self-improving agent loop 是高 prestige 的 OSS 方向
- **Career thesis 升级**: 从 "build evals" → "build agents that pass their own evals"
- **Influence Building**: self-improving agent 是 X 上的 high-engagement 话题

## Open Questions
- Self-improving 的"梯度信号"怎么获得？(human feedback / self-judged / environment reward)
- 怎么避免 self-improvement loop 陷入 mode collapse 或 reward hacking？
- LLM self-correction 的边界在哪里？(GSM8K-style 可以，复杂推理可能不行)
- Production 里 self-improving 系统的 eval 怎么做？(meta-eval 问题，跟 Eval topic 强耦合)
- Cost / latency 角度，agent self-reflection 的 ROI 临界点

## Anchors
- **Anthropic Research** — Constitutional AI、debate、self-correction
- **DeepMind** — AlphaProof、agent self-play、multi-agent emergent
- **OpenAI Research** — o1/o3 reasoning、self-correction in training
- **Andrej Karpathy** — 偶发的 agent-loop commentary
- **Rich Sutton** — Bitter Lesson、continual learning、"experience"
- **Yoshua Bengio (Mila)** — agent safety + self-improvement

## Action Triggers
- **新 self-improving method 论文** → 拆 method；评估能否在 Donut / Compass 集成
- **Frontier lab self-improvement work** → 摘录到 `[[Paradigm Thesis Notes]]`，作为申请 supporting evidence
- **Open-source self-improving repo** → bookmark；评估是否值得 fork 做 GitHub portfolio
- **Anchor 作者 commentary (Karpathy / Sutton)** → 用作 X thread 素材
- **匹配到 [[Paradigm-Fellowship-2026]]** → [propose] add to thesis evidence file
- **没有项目匹配** → [propose] Linear backlog issue, label `agent-research`

## Cross-References
- 与 [[evaluation]] 强耦合（self-improving 的瓶颈本质是 eval 信号）
- [[Paradigm Thesis Notes]]
- Possible MOC: [[Agent MOC]]
