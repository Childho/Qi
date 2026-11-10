# 工作流手册 — skills 使用心得

> 我对所收录第三方 skills 的用法沉淀，供未来的我和执行安装的 AI 参考。清单见 `third-party.md`。

## Matt Skills 主流程（八步）

1. **初始化**：`setup-matt-pocock-skills`
2. **明确需求**：`grill-me` / `grill-with-docs`
3. **写清楚文档**：`to-spec`（小项目可在此步完成后直接 `implement`）
4. **拆解步骤**：`to-tickets`（中大型开发）
5. **做出来**：`implement`
6. **验证行为**：`tdd`
7. **验收质量**：`code-review`
8. **找根因**：`diagnosing-bugs`（出问题时）

`ask-matt`：Skill 路由器，不知道下一步干什么时就问它。

## 场景 × 推荐 Flow

| 场景 | 推荐 Flow |
|---|---|
| 小功能 | grill-with-docs → implement |
| 中型功能 | grill-with-docs → to-spec → to-tickets → implement |
| UI 不确定 | grill → prototype → grill → spec → implement |
| 大型项目 | wayfinder → to-spec → to-tickets → implement |
| Bug | diagnosing-bugs → code-review |
| API 技术不确定 | research → grill-with-docs → spec |
| 老项目越来越乱 | improve-codebase-architecture → grill-with-docs → spec → implement |
| 外部 Issue | triage → implement |

## Engineering 主动调用类

| Skill | 本质 | 什么时候用 |
|---|---|---|
| ask-matt | Skill 路由器 | 不知道下一步干什么 |
| setup-matt-pocock-skills | 项目初始化 | 每个 repo 第一次使用 |
| grill-with-docs | 深度需求访谈 + 项目知识沉淀 | 新功能、新设计、新决策 |
| to-spec | 把已讨论清楚的内容生成 Spec | 需求明确之后 |
| to-tickets | 把 Spec 拆成独立可执行任务 | 中大型开发 |
| implement | 根据 Spec/Ticket 真正实现 | 开始写代码 |
| triage | 整理别人提交的 Issue/PR | GitHub Issue 很多时 |
| improve-codebase-architecture | 扫描架构问题 | 项目越来越乱 |
| wayfinder | 超大型项目决策地图 | 一个上下文装不下的项目 |

其他：`domain-modeling`（维护 Ubiquitous Language，统一领域语言）、`codebase-design`（框架语言设计）、`prototype`（语言无法确定讨论方案时，生成实际可验证的原型）、`research`（查询相关文档）。

## 边角料类

| Skill | 用途 |
|---|---|
| grill-me | 没有 repo 时进行纯访谈 |
| grilling | grill 的底层 interview engine |
| handoff | 把当前 Context 压成可交给另一个 Agent/Session 的 Markdown |
| to-questionnaire | 关键答案掌握在别人手里时，生成调查问卷 |
| wait-what | AI 刚才说了一堆没看懂的东西，让它重新解释 |
| teach | 用 repo 做长期课程环境 |
| writing-for-agents | 专门教写 AGENTS.md、CLAUDE.md、Skills |
| resolving-merge-conflicts | 处理 merge/rebase conflict |
| wizard | 有些步骤必须人类点网页、填 secret 时，生成交互式 Bash Wizard |

## 框架策略

主用 **Matt Skills**，彻底取消 Superpowers 的框架控制，只抽取其 4 个 skill 作为独立插件（`systematic-debugging`、`verification-before-completion`、`requesting-code-review`、`receiving-code-review`，理由见 `third-party.md`）。

## 设计工具链

`frontend-design`（官方，最好的前端设计工具）→ `taste`（独特视觉风格的艺术指导）→ `impeccable`/hallmark（最终审查与质量控制）。
