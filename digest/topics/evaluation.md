---
type: topic
name: "Evaluation"
slug: evaluation
priority: 1
keywords: [eval, evaluation, llm-as-judge, golden-dataset, regression-test, vibe-check, faithfulness, ragas, deterministic-eval, eval-driven-development, evals-as-moat, calibration, agent-eval, tool-use-eval, retrieval-eval]
anti_keywords: [a-b test, conversion-eval, model-accuracy, academic-benchmark, eval-only-as-loss]
anchors: ["Hamel Husain", "Eugene Yan", "Shreya Shankar", "Bryan Bischof", "Drew Breunig"]
related_projects: ["[[Beckman]]", "[[Compass]]", "[[Paradigm-Fellowship-2026]]"]
related_goals: [career-ascension, technical-capital, content-output]
status: active
added: 2026-05-03
notes: ""
---

# Evaluation

## What I Mean
LLM/agent system 的可重复 quality measurement —— faithfulness、grounding、tool-use correctness、retrieval precision/recall、refusal correctness。**不是** ML 学术意义上的 model accuracy，**不是** 产品 A/B test。

> Career glossary 里 "eval is the key differentiator" 是写定的，整个职业方向的支点。

## Why This Matters Now
- **Compass** (Initiative B Lead): RAGAS pipeline、golden dataset、deterministic citation check 是当前主战场
- **Beckman**: learning gain、path coherence rate、metacog model R² —— 同一类问题的教育领域版本
- **Paradigm Fellowship 2026 thesis**: 申请的 thesis 句子直接是 "I build the eval + reliability layer for crypto-agent systems"
- **Career**: AI Engineer 求职最高 leverage 技能

## Open Questions
- Multi-turn / long-horizon agent 怎么做 eval？
- LLM-as-judge 的 bias 怎么校准？哪些任务上 LLM-as-judge 不可靠？
- Tool-use correctness 的 eval — beyond pass@1，怎么定义 partial credit？
- Eval-as-training-signal vs Eval-as-quality-gate 的边界
- Human-in-the-loop eval 的成本/收益曲线在什么 scale 上反转

## Anchors（人名白名单 → 任何文章自动置顶）
- **Hamel Husain** — "Your AI product needs evals"，practical eval 标杆
- **Eugene Yan** — applied ML / eval write-ups
- **Shreya Shankar** — academic eval research、SPADE
- **Bryan Bischof** — Hex eval system
- **Drew Breunig** — eval 哲学 + prompt management

## Action Triggers
- **新 eval framework / library** → 对比当前 Compass/Beckman/Donut eval 设置，写一段 "fit assessment"
- **方法论 essay (anchor 作者)** → atomize 核心 insight，归档到 `[[Eval MOC]]`
- **新 benchmark for tool-use / agent** → 评估能否在 Donut Labs / Compass 上跑
- **Calibration / bias 论文** → 用作 Paradigm 申请的 thesis supporting evidence
- **匹配到 [[Compass]]** → [propose] Linear issue: "Eval refactor — incorporate [insight]" (BIG team)
- **匹配到 [[Beckman]]** → [propose] Linear issue under Beckman project
- **匹配到 [[Paradigm-Fellowship-2026]]** → [propose] add to thesis support evidence file
- **没有项目匹配** → [propose] Linear backlog, label `eval-research`

## Related
- [[Eval MOC]] (to create)
- [[02_Areas/Career/memory/glossary]] — eval 条目
