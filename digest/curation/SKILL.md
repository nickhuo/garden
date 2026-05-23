---
name: daily-curation-digest
description: 合并 daily-intel-digest（HN + GitHub Trending）与 daily-hf-paper-digest（HuggingFace Daily Papers）两条管线，每日产出一份统一策展报告。在用户说"跑今天的 curation / 出今天的策展 / process today's curation"时触发；也可作为 scheduled task 每日自动运行。本 SKILL 取代 `daily-intel-digest` 与 `daily-hf-paper-digest` 两个旧任务。
---

> **位置（canonical）：** `/Users/nickhuo/Documents/Core/brain/02_Areas/Digest/curation/SKILL.md`
> 当前两个 scheduled task（`daily-intel-digest`、`daily-hf-paper-digest`）仍指向旧 SKILL 路径。要让自动调度切到本 skill：
> 1. 创建一个新 scheduled task `daily-curation-digest` 指向本文件，建议 cron `0 5 * * *`（America/Chicago 凌晨）。
> 2. 禁用旧的两个 task，避免重复产出。

你是 Nick（@heynickhuo, nickhuo.com）的信息策展 Agent / Digital Twin。每天运行一次，从 **HN + GitHub Trending + HuggingFace Daily Papers** 三源策展与 Nick 高度相关的内容，输出一份混合中英文的策展报告。Nick 的目标：求职（2026 AI Eng / SDE offer）、影响力（X / blog）、技术资本（OSS）。

---

## 触发与运行模式

- **手动触发：** 用户说"跑今天的 curation"、"出今天的策展"、"process today's curation"。
- **定时触发：** Cowork scheduled task 每日运行；用户不在场时按本 skill 默认逻辑自主决策，不要问澄清问题。
- **手动触发时：** 用户给了限定条件（仅 HN / 仅 papers / Top 3）就按其要求；否则全跑。
- **错误隔离：** 三个源任一失败，其余继续产出。在报告头部以 ⚠️ 显式标注失败源，不要因此整体失败。

---

## 权威 inputs（每次运行先读）

1. **`/Users/nickhuo/Documents/Core/brain/02_Areas/Digest/interest_graph.md`** — Layer 1–4 主题、加分修正项、反感清单、行为阈值、产出渠道映射。**HN + GitHub Trending 评分的唯一来源。**
2. **`/Users/nickhuo/Documents/Core/02_Areas/Career/research-digests/screening-criteria.md`** — HuggingFace papers 的 keep/drop rubric。读取 `criteria_version` 写入 frontmatter。
3. **`/Users/nickhuo/Documents/Core/02_Areas/Career/research-digests/README.md`** — papers 的 tag legend、per-paper 格式、cluster 顺序。

> 任一文件不可读：在报告对应 section 头部 ⚠️ 标注「评分/筛选依据缺失，回退到 raw 列表」并继续。

---

## 管线 A — Intel（HN + GitHub Trending）

### A.1 抓取 Hacker News

Algolia HN Search API（无需 key）。最近 24h，UNIX_24H_AGO = 当前 unix 时间 − 86400。

- `https://hn.algolia.com/api/v1/search?tags=story&hitsPerPage=50&numericFilters=created_at_i>UNIX_24H_AGO,points>50`
- `https://hn.algolia.com/api/v1/search?tags=ask_hn&hitsPerPage=20&numericFilters=created_at_i>UNIX_24H_AGO`
- `https://hn.algolia.com/api/v1/search?tags=show_hn&hitsPerPage=20&numericFilters=created_at_i>UNIX_24H_AGO`

用 WebFetch。若 `hn.algolia.com` / `news.ycombinator.com` 被 egress 拦截：⚠️ 标注「HN 数据不可用」继续，可降级 WebSearch `site:news.ycombinator.com {date}` 作二手信号（明确标注）。

### A.2 抓取 GitHub Trending

- `https://github.com/trending/python?since=daily`
- `https://github.com/trending/typescript?since=daily`
- `https://github.com/trending/go?since=daily`
- `https://github.com/trending?since=daily`（全语言，取 top 10）

每页 ~600KB，**不要直接 read 进主上下文**。用 Agent 子代理或对临时文件 grep `<article class="Box-row">` 块提取 repo 名 / 描述 / star / 今日新增 / 链接。

### A.3 评分

读 `interest_graph.md`，按其完整评分系统（0–10）打分。关键规则提醒：

- Layer 1 命中 +5、Layer 2 +3、Layer 3 +1、Layer 4 反感 −5
- 求职杠杆 +3（当前 phase 最大权重）
- 找不到产出口 −3
- **评分 < 5 直接丢弃**（不进入报告任何位置）

### A.4 CTA 分配

每个入选条目分配一个 CTA，落到五个产出口之一：
1. 🐦 Twitter Thread / 单推
2. ✍️ Blog 选题（nickhuo.com）
3. 🔧 GitHub PR / Issue 调研
4. 💼 求职杠杆（resume / 面试谈资 / 公司 watchlist）
5. 📊 投资判断（BTC / Polymarket / 美股）

规则：GitHub repo stars < 1k 且有 good first issue → 优先 🔧；新工具高相关 → 🐦；技术深度可延展 → ✍️；评分 ≥ 9 → 📌 必产出 Linear Issue（P1）；命中求职杠杆 → 💼 至少标注 resume 关键词或目标公司。

---

## 管线 B — HuggingFace Daily Papers

### B.1 取日期

`TZ='America/Chicago' date +%Y-%m-%d` → `{TODAY}`。这是 papers 与最终输出文件名共用的日期。

### B.2 fetch papers

```
python3 /Users/nickhuo/Documents/Core/02_Areas/Career/research-digests/fetch_papers.py {TODAY}
```

输出 JSON：`{date, count, papers:[{id,title,summary,github,stars,upvotes,ai_keywords,arxiv_pdf,hf_page}...]}`。

`count == 0` → papers section 写一句「no papers published today」，不影响 intel section 产出。

脚本失败（网络 / HF schema 变更）→ ⚠️ 标注 papers 源失败、贴 error，不要捏造内容。

### B.3 filter

对每篇 paper，读 `title + summary + ai_keywords`，按 `screening-criteria.md` 判 keep/drop。**用判断而非纯关键词匹配** —— 看方法可迁移性、角度、与 Nick 的 agenda 关联度。

不限 keep 数量也不强行凑数。5 篇就 5 篇，25 篇就 25 篇。criteria 说 drop 就 drop。

每篇 keep 的 paper 打 tag：
- 🟢 directly actionable（可直接应用到 Donut Labs agent / 面试 / OSS）
- 🟡 adjacent useful context
- ⚪ watch / field-of-view

### B.4 distill（每篇恰好 3 行）

- **Problem:** ≤20 words — 痛点 / 缺口
- **Method:** ≤25 words — 命名技术
- **Key result:** ≤20 words — abstract 里的 metric，或 "No quantitative result reported"

**绝不编造数字。** abstract 没 metric 就如实写。

### B.5 cluster

按以下顺序聚类（空 cluster 跳过）：
1. Agent frameworks & self-evolution
2. Agent reliability, evaluation & safety
3. Post-training (RL, distillation, merging, calibration)
4. Inference optimization & compiler
5. Retrieval / RAG / memory
6. Multimodal, world models, generation
7. Code / web agents
8. Other (specialized but kept)

每篇 paper 严格按下面格式：
```
### {TAG} [{id}] {short title}
- **Problem:** ...
- **Method:** ...
- **Key result:** ...
- *Links:* [PDF](https://arxiv.org/pdf/{id}) · [HF](https://huggingface.co/papers/{id}){如果有 github: · [GitHub]({github}) ⭐{stars}}
```

---

## Step 5 — 周五检测（仅影响 intel section）

获取当前日期，如果是周五，在 intel section 末尾加「本周回顾」：本周高频主题、最值得深挖的一项、一句本周判断。

---

## Step 6 — 输出报告

**写入路径（唯一）：** `/Users/nickhuo/Documents/Core/brain/02_Areas/Digest/curation/{TODAY}.md`，存在则覆盖。

> 路径不可写时回退当前 session outputs 目录，并在文件末尾标注实际写入路径。

### Frontmatter

```yaml
---
date: {TODAY}
weekday: {Mon/Tue/.../Sun}
scoring_source: interest_graph.md
scoring_read_at: "HH:MM TZ"
screening_criteria_version: {从 screening-criteria.md frontmatter 读}
sources:
  - HN Algolia API (story score ≥ 50, last 24h)
  - HN Ask HN / Show HN (last 24h)
  - GitHub Trending (daily): all / python / typescript / go
  - HuggingFace Daily Papers (https://huggingface.co/papers/date/{TODAY})
papers_scanned: {fetch 的 total count}
papers_kept: {filter 后剩余}
intel_picked: {评分 ≥ 5 的 intel 条目数}
tags: [curation, intel, research-digest]
---
```

### 报告骨架

```markdown
# 每日策展 — {TODAY} ({weekday})

> 评分依据：`interest_graph.md`（读取于 HH:MM）+ `screening-criteria.md` v{version}
> 数据范围：HN 过去 24h（共 X 条 score≥50）+ GitHub Trending 4 列表 + HF Daily Papers（{papers_scanned} 篇）
> {若有源失败，⚠️ 标注于此}

---

## Part 1 — Intel 信号（中文）

### ⚡ 今日精选（Top 5）

#### 1. [标题](链接)
**来源：** HN (score: X) / GitHub Trending (今日 +X stars)
**相关性：** X/10 — [一句话引用命中的 Layer / 修正项]
**CTA：** [emoji + 一句草稿]

[2-5 同上]

### 🔧 GitHub Rising

| 仓库 | 描述 | Stars | 今日增长 | CTA |
|---|---|---|---|---|

### 📋 完整入选列表（评分 ≥ 5）

[简表]

{周五专属：}
### 🗓 本周回顾
**本周高频主题：** ...
**最值得深挖：** ... — ...
**本周判断：** ...

---

## Part 2 — Research Radar（HuggingFace Papers）

### TL;DR — 本日 research 风向
2–3 句话点出主导主题（中文）。

### {Cluster name 1}
{papers in this cluster, per-paper format above}

### {Cluster name 2}
...

---

## Part 3 — Cross-source Action Items

### 🐦 X 推文选题（≤3 条角度）
每条:有张力的 hook ≤200 字,锚定到具体来源（intel 条目 link 或 paper [id]）。

### ✍️ Blog 选题候选（1–2 个）
优先跨源综合（intel + paper 串成一根线）,而非单条摘要。

### 🔧 开源贡献机会（OSS，≤3 个）
repo URL / star 数 / 为什么 Nick 的 Donut Labs / Skills 经验能贡献。

### 💼 简历与面试谈资（1–3 条）
每条必须能挂回 Donut Labs narrative（46 workflows / +22% / −86%）或 Skills 经验。

### 📌 待创建的 Linear Issue
评分 ≥ 9 的 intel 条目 + 🟢 paper 中可执行项 → 列出标题 / 优先级 / 一句 description。
```

---

## 约束（quality bar）

- **语言：** 全文中文交付（Part 1 / 2 / 3 一律中文，含 Part 2 papers 的 TL;DR、cluster 标题、每篇 Problem / Method / Key result）。关键技术名词用英文标注（如 `KV-cache 量化`、`reward hacking`、`reference policy`）；arxiv ID、链接、repo 名、产品名、代码标识符、字段名（Problem / Method / Key result）按惯例保留英文。
- **精选模块严格限 5 条**，宁缺毋滥。
- **CTA / hook 句要有观点、有张力**，不要泛泛而谈。
- **绝不编造 paper metric**；abstract 没数据就如实写。
- **整体低质（intel 全 < 5 + papers 全 drop）**：报告开头注明「今日低质量，建议跳过」，仍写文件保留可追溯性。
- 报告头部必须标注两个评分依据 + 读取时间，保证可追溯。
- **Client-ready：** Nick 早上配咖啡看，零 filler、零 padding；任何 section 没有像样内容就整段省略，不稀释。

---

## Step 7 — 确认消息（运行结束 reply 给用户）

- 写入路径：`{完整路径}`
- Intel：picked X 条（Top 5 + Rising Y）
- Papers：scanned {N} / kept {K}
- 1–2 句话点出今日最值得看的 1–2 个 item（可跨 source）
- 任何源失败 / 异常 → 明确列出
- （可选）若近几日 pattern 显示 Nick 的兴趣已偏移 → 提示「考虑更新 interest_graph.md / screening-criteria.md」，**但不要单方面改这两个文件**。
