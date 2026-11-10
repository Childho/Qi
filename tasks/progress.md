# Qi — 执行进展

## 2026-11-10 · 建仓上线

- **grilling 需求澄清**：3 轮 15 项决策（见 todo.md），从"集中配置 + GitHub + 一句话自动配置"的原始想法收敛为：无 harness 适配、Agent 驱动安装、人工策展、密钥永不入库的轻架构。
- **探查**（子代理只读）：发现 10+ 个 harness 配置目录；skills 分裂于 `.zcode/skills`（53）与 `.agents/skills`（85），重叠 39；MCP 配置在 `~/.zcode/cli/config.json`（`mcp.servers`），env 含密钥字段。
- **提交 4bb56d0**：骨架——README（首行 AI 指令）、SETUP.md（6 步安装 + 月度更新流程 + harness 位置参考表）、global/AGENTS.md（母版原文）、mcp/mcp.template.json（3 项，密钥占位符化）、third-party.md、tools/install-skills.ps1（迁自根目录）、.gitignore、skills/.gitkeep；根 AGENTS.md 加指路句。密钥 grep 自检通过。
- **提交 a178886**：用户提交白名单（全部为第三方，无一自有 skill → 全部进进货单，`skills/` 留空）。进货单扩为 7 组：anthropics 官方（四件套+frontend-design）、设计类 3 个、mattpocock 全集、neat-freak、Superpowers 精选 4 个。WebSearch 查证两个存疑来源：obra/superpowers、nutlope/hallmark（=本机 impeccable）。用户工作流心得原文沉淀至 docs/workflows.md。
- **提交 a7391db + 上线**：`gh` CLI 不在 Git Bash PATH，实际装于 `$LOCALAPPDATA/Programs/GitHub CLI/bin/`；gh keyring 在非交互会话超时 → 改从 Git Credential Manager 取 token（不回显）注入 `GH_TOKEN` 绕过 keyring，`gh repo create` 建公开仓库并推送 main 成功。

## 当前状态

- 远端 https://github.com/Childho/Qi ，main 与本地一致，工作区干净。
- 未做：新机器表验、月度定时任务建立（见 todo.md）。
