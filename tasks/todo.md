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

## 当前阶段

✅ 已上线（2026-11-10，main 已推送）。

## 待办 / 后续方向

- [ ] **新机器表验**：换机时首次按 SETUP.md 走一遍，暴露说明书盲区并回写修正。
- [ ] **插件同步流程首跑观察**：首次（手动或月度触发）执行《插件同步流程》后，检查 profile 遍历、link 母本定位、PR 流程是否顺畅。
- [ ] **插件装机表验**：换机时按 SETUP.md 第 5 步从 `plugins/` 目录 `install_bundle`，验证 karlo-calm 在新 profile 上可用（本次未实际从 Qi 目录重装，装的是开发母本 link）。
- [ ] **月度更新首跑观察**：首次定时任务触发后，检查 PR 流程是否顺畅（尤其非 gh 环境的手动开 PR 退化路径）。
- [ ] **首次月度定时任务尚未建立**：需在本机（Qi 仓库所在 workspace）按 SETUP.md 第 5 步建每月自动化。
- [ ] **自有 skill 收录**：`skills/` 目前为空，用户未来自己写的/深度改造的 skill 放这里。
- [ ] 进货单目前 7 组；`~/.agents/skills` 里还有 30+ 未溯源的第三方 skill（feishu 全家桶、股票分析、电商类等），用户未点名收录，待其试用认可后补入 third-party.md。
- [ ] 可选：Superpowers 4 个精选 skill 的上游目录名核对（obra/superpowers，安装时以 skills/ 实际为准）。
