# Nick 兴趣图谱 (Interest Graph)

> **用途：** 所有 curation / digest / monitoring 类 scheduled task 的**统一评分依据**。任何 task 在打分前都应引用此文件。
> **Owner:** Nick (@heynickhuo)
> **Last updated:** 2026-05-04
> **Next review:** 2026-08-04（季度审计；或拿到 offer 时立即触发重平衡）

---

## 0. 元数据 / Phase 状态

| 字段            | 值                                                                     |
| ------------- | --------------------------------------------------------------------- |
| 当前阶段          | **2026 暑期 SDE/AI Engineer 求职季**（main thread = Career）                 |
| Stack reality | Python（主力）、TypeScript（实用）、Go（在学）、Rust（仅了解，不写）                         |
| 主要产出渠道        | @heynickhuo（Twitter）、nickhuo.com（Blog）、GitHub（开源）、Linear（personal OS） |

---

## 1. 评分系统总则

- 评分 **0–10**
- **< 5 直接丢弃**（不是过滤后再看，是不进入报告）
- 评分 = base 0 + Layer 加分 + 修正项 − 反感项
- **找不到产出口的条目自动 −3**（消费 ≠ 策展）

---

## 2. Layer 1：核心痴迷（每条 +5）

> 每一条都让 Nick **想点开 / 想转发 / 想复盘**。命中即进入精选候选。

| 主题                           | 关键词举例                                                                  |
| ---------------------------- | ---------------------------------------------------------------------- |
| **LLM Agents 架构层**           | 编排（multi-agent、swarm）、协议（MCP、ACP、A2A）、评估（evals、traces、replay）、agent OS |
| **AI Engineering 招聘信号**      | Anthropic/OpenAI/Scale/Cursor/Modal 等公司岗位变化、新兴技能要求、面试题趋势、湾区 AIE 招聘动态   |
| **Coding Agent / CLI 化开发流程** | Claude Code、Codex、Cursor、terminal-native agent、coding agent harness    |
| **System Design 现代化**        | 分布式系统经典 + AI infra（vLLM、SGLang、Modal、Ray Serve）、LLM 推理 scaling         |

---

## 3. Layer 2：专业关注（每条 +3）

> 技术上熟悉，碰到会读完，但**不一定要产出**。

- **RAG / Vector DB / Hybrid retrieval**：pgvector、Qdrant、Weaviate、Pinecone、长上下文 vs 检索的取舍
- **Prompt / Context Engineering 工程化**（带 benchmark / 数据，不是 vibes）
- **Python / TypeScript / Go 生态新工具**：Bun、uv、Polars、Pydantic AI、Modal、新型 build tool
- **求职 / 面试**：System Design 题型演变、LeetCode 高频题趋势、行为面试新方向、Coding interview AI 化的影响
- **投资宏观信号**：BTC 链上数据、Polymarket 重大事件赔率、美股美债拐点、半导体/AI infra 公司（NVDA、AVGO、Coreweave）

---

## 4. Layer 3：次要好奇（每条 +1）

> **碰到才看**，不主动追。

- 编程语言研究（Rust 周边但不深入、Zig）
- 学术 paper（仅限 LLM/Agents 方向 arxiv trending）
- 独立开发者 / indie hacking 真实案例（用作 blog 素材）

---

## 5. Layer 4：明确反感（每条 −5，直接 reject）

> 命中即丢，不进入报告。

- ❌ **No-code / Low-code 平台**：Bubble、Webflow、Make、Zapier 这类拖拽工具的功能更新
- ❌ **通用 JS 框架口水战**：React vs Vue vs Svelte、Tailwind 是否好用之类
- ❌ **纯 marketing / hype 类 LLM 包装**：ChatGPT 套壳产品发布、"AI 改变 X 行业"无技术内容稿
- ❌ "AI 改变世界" 宏大叙事文章（无技术细节、无数据）
- ❌ 项目管理鸡汤 / agile 玄学
- ❌ 创业课 / "如何在 X 天内做出 SaaS" 教学

> **白名单例外**：Web3 / 加密货币本身**不**进反感清单（BTC/ETH 宏观、Polymarket 仍是 Layer 2 投资关注）；但具体到「空投 / Memecoin / NFT 项目发售」这类内容应直接过滤。

---

## 6. 加分修正项（叠加在 Layer 加分上）

| 修正项 | 分值 |
|---|---|
| 🎯 **命中求职杠杆**（招聘动向 / 岗位拆解 / 面试题趋势 / 目标公司技术栈变化） | **+3** |
| 命中投资杠杆（BTC / Polymarket / 美股宏观判断） | +1 |
| 独立开发者 / indie 项目（不是大厂 PR 稿） | +1 |
| GitHub repo: stars < 1k **且**有 good first issue（贡献窗口期） | +2 |
| GitHub repo: 单日 +500 stars 或 HN score > 200（硬热度） | +1 |
| 含真实评估 / benchmark / 数据（非 vibes claim） | +2 |
| 中文社区 / 华人开发者作品（社交杠杆友好） | +1 |

> **求职杠杆 +3 是本季度最大权重**——因为 Phase = 2026 暑期求职季。拿到 offer 后立即把这一项降到 +1，避免图谱失焦。

---

## 7. 行为阈值（基于评分的 CTA 分配）

| 评分  | 建议行为                                               |
| --- | -------------------------------------------------- |
| ≥ 9 | 📌 **立即创建 Linear Issue**，优先级 P1，必产出                |
| 7–8 | 进入**精选列表**，至少一个明确 CTA（推文 / blog / PR / resume 关键词） |
| 5–6 | 进入**完整列表**，待复用，不强制产出                               |
| < 5 | **丢弃**（不进入报告任何位置）                                  |

---

## 8. 产出渠道映射（CTA 必须落到这五个之一）

每个入选条目，CTA **必须**指向以下产出口之一，否则 −3：

1. 🐦 **Twitter Thread / 单推** — `@heynickhuo` 影响力增长
2. ✍️ **Blog 长文选题** — nickhuo.com（用 Tiered Writing Method）
3. 🔧 **GitHub PR / Issue 调研** — 开源资本积累
4. 💼 **求职杠杆** — resume 关键词更新 / 面试谈资 / 目标公司 watchlist
5. 📊 **投资判断** — BTC / Polymarket / 美股 watchlist 更新

---

## 9. 季度审计 Checklist

每 3 个月一次（下次：**2026-08-04**），逐项自查：

1. **Layer 1 校准**：过去 90 天 Nick 真的产出过相关内容吗？没产出 → 降到 Layer 2 或删除（防止 aspirational 漂移）。
2. **Layer 4 增项**：哪些主题让 Nick 反感但仍在进入 digest？补进反感清单。
3. **Layer 升级**：哪些 Layer 2/3 主题反复出现且 Nick 主动深挖？升级到 Layer 1。
4. **Phase 切换**：求职阶段是否变化？拿到 offer → 把求职 +3 降到 +1，把内容 / 开源杠杆提权。
5. **行为校准**：过去 90 天的 digest 评分是否能预测 Nick 实际点开 / 转发 / star 的内容？偏差大就调权重。

---

## 10. 引用方式

其他 scheduled task / curation 任务评分时，应在头部声明：

> 评分依据：`/Users/nickhuo/Documents/Core/brain/02_Areas/Digest/interest_graph.md`

并在 task 文件中**只引用、不复制**评分规则——保持单一来源。

---

## Changelog

- **2026-05-04**：首版重建。
  - 删除 Neovim 偏好（aspirational 校准，实际不使用）
  - 求职杠杆 +3 置顶（2026 暑期主线）
  - 新增 Layer 4 反感清单（No-code、JS 口水战、LLM hype 稿）
  - 新增「找不到产出口 −3」规则
  - 拆出独立文件，与 SKILL.md 解耦，多任务共用
