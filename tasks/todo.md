# Qi — 项目规划与待办

## 项目定位

个人 AI 工具配置中心：skills 进货单 + 全局指令母版 + MCP 模板。公开仓库 https://github.com/Childho/Qi 。
新机器/新 harness 使用方式见 README.md；安装逻辑的唯一真源是 SETUP.md。

## 核心架构决策（2026-11-10 定，grilling 15 项）

1. 公开仓库；2. 不做 harness 适配（AI 读 SETUP.md 自主安装）；3. 单向、人工策展，不自动回流；
4. Agent 驱动；5. 密钥永不入库（模板占位符）；6. 白名单精选；7. 说明书平台无关；
8. Qi 即上传主体；9. 第三方只存来源+版本；10. 范围仅 skills + 全局 AGENTS.md + MCP 模板；
11. 入口三层分工 README → SETUP.md → 根 AGENTS.md；12. 月度更新=本机定时任务 + 开 PR 人工合并；
13. 白名单由用户亲自维护；14. AGENTS.md 原文入库不脱敏；15. MCP 只收 MiniMax / MiniMax-Media / rea。

## DSH 插件模块决策（2026-11-21 定，grilling 9 项）

1. 分层收录：自研源码入 `plugins/`（目录即清单），第三方只记 `plugins/third-party.md` 进货单；
2. **分布开发**：插件在任何项目里开发、装进 profile，Qi 是归档不是母本（skills 的"不回流"在此放宽为定期回流）；
3. 回流方向 profile → Qi，项目侧覆盖 Qi 侧，PR 人工兜底；Qi 版本更高时不覆盖、标冲突；
4. 触发双入口：月度任务自动兜底 + 随时一句话手动执行《插件同步流程》（SETUP.md）；
5. 新插件只报告待审，不自动入库；6. 密钥占位符红线不变；
7. 版本兼容：自研插件 package.json 记 `dsh.compatibility.dshReleases`，第三方清单记已验证 DSH 版本；
8. 同步信号：各 profile `package.json` 的 `dsh.profile.bundles` 数组（忽略 `@deepseek-ai/` 内置）；
9. 首批收录：karlo-calm（源码）+ dsh-qqbot@0.5.5（清单）。

## 插件模块扩展决策（2026-11-28 定，用户直接点名，未走 grilling）

1. `plugins/` 从「仅 DSH 插件包」扩展为「DSH 插件包 + 独立仓库插件」：无 package.json、自带安装器的桌面端插件也可收录，「目录即收录清单」不变；
2. 首个独立仓库插件：zcode-tempo（https://github.com/Childho/zcode-tempo ，ZCode 桌面测速 + 三击草稿增强 + 下一条消息预测），归档其发布仓库 HEAD，不用 submodule；
3. 独立仓库插件的回流母本 = 其 GitHub 发布仓库（`git archive` 覆盖、保持 LF，不走 DSH profile 遍历），落点：SETUP.md《插件同步流程》第 3 步、安装第 5.2 节；安装属侵入式修改（app.asar），执行前须向用户确认。

## 提示词模块决策（2026-11-21 定，grilling 三轮 12 问）

1. 定位**纯复用工具箱**：只收正在用的，不常用即删（删除=删文件）；不为学习拆解/永久归档/分享设计；
2. 用户亲自存入与策展：无批量导入、无收录自动化；空库起步，不留示例条目；
3. 小规模刻意为之：平铺无分类子目录、无索引页、无 frontmatter 元数据体系；
4. 一条一文件：英文 kebab-case 文件名 + 文件内中文标题，目录即收录清单（同 skills/）；
5. 条目结构：三行头部（标题 / 用途 / 可选来源）+ 分隔线 + 正文；**分隔线以下=复制区**，正文不包 code fence；
6. **外部内容模块级豁免**：提示词纯文本无执行风险，直接入库；外部来源标一行出处（第三方代码/工具仍守进货单铁律）；
7. 人+agent 双消费：agent 入口 = 根 AGENTS.md 的 Prompt library 指路小节；
8. 挂接最小化：根 README 结构图+维护规则各一行；不动 SETUP.md（非安装项）、不涉及 third-party.md、不走 .scratch 流程；
9. 与 global/AGENTS.md 互不干涉：提示词按需复用，不全局注入；
10. 收录标准：只收实际用过且有效的；外部条目必须标出处；每条必有一行用途说明。

## Dashboard 模块决策（2026-11-21 定，grilling 两轮 11 问）

1. 原始命题「DSH 插件工作面板」被推翻：真实诉求是「可视化 dashboard，载体不限」→ 独立静态快照（备选与否决理由见 `docs/adr/0001`）；
2. `tools/build-dashboard.py`（Python 标准库，零依赖）扫描仓库 → 数据内嵌生成根目录 `dashboard.html`，双击即开；生成物不入库（.gitignore），重生成 = 重跑脚本；
3. 数据源仅 Qi 仓库，八板块：自研/第三方 skills、自研/第三方 plugins、prompts、核心提示词、MCP 模板、todo 规划 + 顶部统计条；不读本机 `~/.dsh`、`~/.agents` 安装态；
4. 健康度 = 时间视角（git 最后变更距今天数），无红绿灯；上游版本核对归月度流程，dashboard 不联网不越界；
5. 刷新 = 手动重跑兜底 + 月度更新流程末尾顺带重生成（已写入 SETUP.md 第 7 步）；不用 git hook（本机态、不提交的改动照样过期）；
6. 视觉与交互以 [ADR-0001](../docs/adr/0001-dashboard-static-snapshot.md) 为准。2026-11-24 重做资产总览、快捷目录和宽窄屏清单。

## 当前阶段

✅ 已上线（2026-11-10，main 已推送）。

## 待办 / 后续方向

- [ ] **新机器表验**：换机时首次按 SETUP.md 走一遍，暴露说明书盲区并回写修正。
- [ ] **插件同步流程首跑观察**：首次（手动或月度触发）执行《插件同步流程》后，检查 profile 遍历、link 母本定位、PR 流程是否顺畅。
- [ ] **插件装机表验**：换机时按 SETUP.md 第 5 步从 `plugins/` 目录 `install_bundle`，验证 karlo-calm 在新 profile 上可用（本次未实际从 Qi 目录重装，装的是开发母本 link）；另按第 5.2 节从 `plugins/zcode-tempo/` 归档目录走一遍 `install.py install`（尚未从 Qi 归档安装过）。
- [ ] **月度更新首跑观察**：首次定时任务触发后，检查 PR 流程是否顺畅（尤其非 gh 环境的手动开 PR 退化路径）。
- [ ] **首次月度定时任务尚未建立**：需在本机（Qi 仓库所在 workspace）按 SETUP.md 第 5 步建每月自动化。
- [ ] **自有 skill 收录**：`skills/` 目前为空，用户未来自己写的/深度改造的 skill 放这里。
- [ ] 进货单目前 7 组；`~/.agents/skills` 里还有 30+ 未溯源的第三方 skill（feishu 全家桶、股票分析、电商类等），用户未点名收录，待其试用认可后补入 third-party.md。
- [ ] 可选：Superpowers 4 个精选 skill 的上游目录名核对（obra/superpowers，安装时以 skills/ 实际为准）。
