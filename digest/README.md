---
name: Daily Curation Digest
owner: Nick
updated: 2026-05-25
---

# Daily Curation Digest

每日一份统一策展报告，从 **Hacker News + GitHub Trending + HuggingFace Daily Papers** 三源筛选与 Nick 高相关的内容，按 `interest.md` 评分，输出中英混合的 client-ready 报告。目标导向：求职（2026 AI Eng / SDE）、影响力（X / blog）、技术资本（OSS）。

> 取代了旧的 `daily-intel-digest`（仅 HN+GitHub）与 `daily-hf-paper-digest`（仅 HF papers）。两者已合并进本 skill，勿重复创建。

## The skill (single source of truth)

逻辑全部在 **`.claude/skills/daily-curation-digest/SKILL.md`**（项目根 `03_Resources/.claude/skills/` 下）。它是 Claude Code 的**项目级 skill**：在 workspace = `03_Resources` 时按 `name` / 触发语自动发现并加载，无需按路径 `Read`。

本 README 只是导览 —— 评分细则、抓取步骤、输出格式以 SKILL.md 为准。

## Layout

| 路径 | 作用 | 谁编辑 |
|---|---|---|
| `.claude/skills/daily-curation-digest/SKILL.md` | 策展逻辑（抓取 / 评分 / 聚类 / 输出格式） | Nick + Digital Twin |
| `interest.md` | **评分唯一来源**：Layer 1–4 主题、加分修正项、反感清单、行为阈值、产出渠道映射 | Nick（对 Twin 说 `update interest: …`） |
| `curation/{YYYY-MM-DD}.md` | 每日报告 | skill 生成 |
| `topics/` | 长期问题导向的兴趣主题（喂给 interest graph） | Nick |
| `sources/*.md` | 订阅频道定义（fetch 层用） | Nick |
| `scripts/` | 可选 fetch 层（`fetch.py` 拉 sources → `output/candidates_<date>.json`，带 dedup） | 见 `scripts/README.md` |
| `*.base` `_index.md` | Obsidian dashboard / Bases 视图 | 偶尔 |

> 注：当前 skill 直接用 `WebFetch` 抓三源，不依赖 `scripts/` 那条 candidates-JSON 管线 —— scripts 是独立的订阅聚合层，可单独使用。

## How the daily run works

1. **触发：** Superset automation **"Daily Curation Digest"** 每天 **02:00 America/Chicago** 在 Nick 的 Mac 上跑（workspace = `03_Resources`，agent = `claude`）。也可手动说"跑今天的 curation / process today's curation"。
2. skill 先读 `interest.md` 取评分系统。
3. **管线 A（Intel）：** HN Algolia API（24h，score ≥ 50）+ Ask/Show HN + GitHub Trending（all/python/typescript/go）→ 按 `interest.md` 打分（0–10，< 5 丢弃）→ 分配 CTA。
4. **管线 B（Papers）：** HuggingFace Daily Papers（当日为空则回退最近有论文的一天）→ 同一套评分 keep/drop → 每篇蒸馏成 Problem / Method / Key result 三行 → 聚类。
5. **错误隔离：** 任一源失败，其余照常产出，报告头部 ⚠️ 标注失败源。
6. **输出：** 写入 `curation/{DATE}.md`（存在则覆盖），含 Part 1 Intel / Part 2 Research Radar / Part 3 跨源 Action Items（X 选题 / blog 选题 / OSS 机会 / 简历谈资 / 待建 Linear Issue）。

## Scheduled task

- **Superset automation ID:** `8ce4a592-5adb-4cf0-b20d-4405c54dde32`
- **Schedule:** `FREQ=DAILY;BYHOUR=2`（每日 02:00 America/Chicago）
- **管理：** `superset automations {get|run|logs|pause|resume} 8ce4a592-5adb-4cf0-b20d-4405c54dde32`

## Running on demand

直接对 Digital Twin 说：

```
跑今天的 curation        # 全跑三源
出今天的策展 —— 仅 papers   # 限定单源
process today's curation, top 3 only
```

## Evolving the scoring

当 Nick 的关注点变化（新项目 / 新技术兴趣 / 新求职目标）：

```
> Twin, update interest: 把 "post-training for reasoning models" 加进 Layer 1，去掉 "voice/multimodal agents"
```

Twin 编辑 `interest.md`（评分唯一来源），skill 下次运行自动生效。**Twin 不会单方面改 `interest.md`** —— 只在你明确要求时改。
