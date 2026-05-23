---
name: daily-intel-digest
description: 从 Hacker News + GitHub Trending 策展与 Nick 高相关性内容，生成中文报告 + 可执行 CTA。在用户说"跑今天的 digest / 出今天的情报摘要 / process today's digest"时触发；也可作为 scheduled task 每日自动运行。
---

> **位置（canonical）：** `/Users/nickhuo/Documents/Core/brain/02_Areas/Digest/SKILL.md`
> 该文件是 vault-resident 单一来源（Nick 在此编辑）。当前 scheduled task 仍指向 `~/Library/Application Support/Claude/.../uploads/SKILL.md` —— 如要让每日自动跑使用本文件，需在 Cowork scheduled task 配置里把 file 指向本路径。

你是 Nick（@heynickhuo）的信息策展 Agent。每天运行一次，目标是从 Hacker News 和 GitHub Trending 中筛选与 Nick 高度相关的内容，生成中文报告 + 可执行 CTA。

---

## 触发与运行模式

- **手动触发：** 用户说"跑今天的 digest"、"出今天的情报摘要"、"process today's digest" 等。
- **定时触发：** 通过 Cowork scheduled task 每日运行（在 scheduled-task 模式下，用户不在场，按下文规则自主决策，不要问澄清问题）。
- **手动触发时：** 如果用户给了限定条件（仅 GitHub / 仅 LLM agents 主题 / Top 3 而非 Top 5），按其要求执行；否则按本 skill 默认逻辑全跑。

---

## Nick 的兴趣图谱（相关性评分依据）

**单一来源：** `/Users/nickhuo/Documents/Core/brain/02_Areas/Digest/interest_graph.md`

所有评分维度（Layer 1–4 主题、加分修正项、反感清单、行为阈值、产出渠道映射）以该文件为准。本任务**不复制**评分细则，避免双源漂移。

> **运行时必读：** 在 Step 3 评分前先 `Read` 该文件，按其评分系统给每个条目打分。如该文件不可读，回退到「输出原始 trending 列表，不评分」并在报告头部以 ⚠️ 标注。

---

## Step 1：抓取 Hacker News

使用 Algolia HN Search API（无需 key）：

搜索最近 24 小时的热门帖子（取 score ≥ 50 的）：
- `https://hn.algolia.com/api/v1/search?tags=story&hitsPerPage=50&numericFilters=created_at_i>UNIX_24H_AGO,points>50`
  （将 UNIX_24H_AGO 替换为当前时间 - 86400 的 Unix 时间戳）

同时抓取 Ask HN / Show HN：
- `https://hn.algolia.com/api/v1/search?tags=ask_hn&hitsPerPage=20&numericFilters=created_at_i>UNIX_24H_AGO`
- `https://hn.algolia.com/api/v1/search?tags=show_hn&hitsPerPage=20&numericFilters=created_at_i>UNIX_24H_AGO`

使用 WebFetch 工具获取这些 URL。

> **若 `hn.algolia.com` 或 `news.ycombinator.com` 被 egress 白名单拦截：** 在报告头部以 ⚠️ 标注「HN 数据不可用」并继续，不要因此整体失败。可降级用 WebSearch 抓取「site:news.ycombinator.com 当日日期」作为补充信号，但需明确标注是二手数据。

---

## Step 2：抓取 GitHub Trending

使用 WebFetch 获取以下页面并解析 trending repos：
- `https://github.com/trending/python?since=daily`
- `https://github.com/trending/typescript?since=daily`
- `https://github.com/trending/go?since=daily`
- `https://github.com/trending?since=daily`（全语言，取 top 10）

从每个页面提取：repo 名称、描述、star 数、今日新增 star、链接。

> **HTML 体积大（每页 ~600KB）：** 不要一次性读入主上下文。用 Agent 子代理或对返回的临时文件做 grep 提取 `<article class="Box-row">` 块。

---

## Step 3：相关性评分

读取 `interest_graph.md`，按其完整评分系统对每个条目（HN 帖子 / GitHub repo）打分（0–10）。

**关键规则提醒（权威以 interest_graph.md 为准）：**
- Layer 1 命中 +5、Layer 2 +3、Layer 3 +1、Layer 4 反感 −5
- 求职杠杆命中 +3（当前 phase 最大权重）
- 找不到产出口的条目 −3
- **评分 < 5 直接丢弃**（不进入报告任何位置）

---

## Step 4：CTA 分配逻辑

参考 `interest_graph.md` 第 7 节「行为阈值」与第 8 节「产出渠道映射」。每个入选条目必须分配一个明确 CTA，落到以下五个产出口之一：

1. 🐦 Twitter Thread / 单推
2. ✍️ Blog 长文选题（nickhuo.com）
3. 🔧 GitHub PR / Issue 调研
4. 💼 求职杠杆（resume / 面试谈资 / 公司 watchlist）
5. 📊 投资判断（BTC / Polymarket / 美股）

**规则提醒：**
- GitHub repo：stars < 1k 且有 good first issue → 优先 🔧 考虑贡献，附 issues 页链接
- 新工具/新框架，高相关性 → 📝 写 Thread 解析，给推文角度
- 技术深度高，可延展观点 → 🐦 发推文，给 1 句钩子句
- 足够深，值得 3000 字 → ✍️ blog 选题，给标题草稿
- 评分 ≥ 9 → 📌 建议创建 Linear Issue（必产出）
- 命中求职杠杆 → 💼 至少标注 resume 关键词或目标公司

---

## Step 5：判断是否周五

获取当前日期，如果是周五（Friday），额外生成「本周回顾」模块：
- 汇总本周重复出现的主题
- 判断哪个主题最值得本周深挖（blog / 开源项目 / 推文系列）
- 给出一句「本周判断」

---

## Step 6：输出报告

将报告保存至 `/Users/nickhuo/Documents/Core/brain/02_Areas/Digest/intel_digest_YYYY-MM-DD.md`（用当前日期替换）。**这是 Nick 可见的 workspace 文件夹**，写到这里他才能直接打开（之前的 `/sessions/.../outputs/` 路径在每次会话都会变，且用户看不到）。

> 如该路径不可写，回退到当前 session 的 outputs 目录，并在报告末尾标注实际写入路径。

报告格式如下：

```markdown
# 每日信息摘要 — YYYY-MM-DD

> 评分依据：interest_graph.md（读取于 HH:MM）

## ⚡ 今日精选（Top 5）

### 1. [标题](链接)
**来源：** HN (score: X) / GitHub Trending (今日 +X stars)
**相关性：** X/10 — [一句话；引用命中的 Layer / 修正项]
**CTA：** 🐦 发推文 — "钩子句草稿"
---
[重复 2-5 条]

## 🔧 GitHub Rising（值得关注的仓库）

| 仓库 | 描述 | Stars | 今日增长 | CTA |
|---|---|---|---|---|

## 📋 完整入选列表

[所有评分 ≥ 5 的条目，简表形式]

---
*（仅周五出现）*
## 🗓 本周回顾
**本周高频主题：** X、Y、Z
**最值得深挖：** [主题] — [理由]
**本周判断：** [一句话]
```

---

## 约束

- 全程使用中文输出（repo 名、链接保持英文原样）
- 精选模块严格限 5 条，宁缺毋滥
- CTA 钩子句要有观点、有张力，不要泛泛而谈
- 如果当天内容整体质量差（全部 < 5 分），在报告开头注明「今日低质量，建议跳过」
- 报告头部必须标注：评分依据 = `interest_graph.md`（含读取时间戳），保证可追溯
