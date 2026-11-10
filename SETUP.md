# SETUP.md — 环境配置指令（写给 AI）

> 你（AI agent）收到本仓库后，目标是在**当前机器、当前 harness** 上把仓库中的个人配置安装到位。本文件是安装指令的唯一真源，人读的介绍见 `README.md`。

## 原则（先读）

1. **平台无关**：本文件不写死操作系统与 harness。凡涉及"装到哪"，以你所在 harness 的官方惯例为准；不确定就查文档或问用户，不要猜。
2. **幂等**：重复执行本文件不产生重复安装；已存在的条目做更新，不做叠加。
3. **密钥永不入库**：任何 API key / token 只写入本机配置文件，绝不写回本仓库、绝不写入任何可能被提交的文件。安装结束前按第 6 步自检。
4. **失败处理**：网络操作失败（上游不可达等）时跳过该项、记录原因、继续下一项，最后统一汇报，不中断整体流程。

## 第 1 步：安装自有 skills

把 `skills/` 下每个子目录，安装到你所在 harness 的用户级 skills 目录。

- `skills/` 目录即收录清单：目录里有什么就装什么，没有的不装。
- 安装 = 复制整个子目录（或按 harness 惯例建立链接），目录名保持不变。

## 第 2 步：安装第三方 skills

按 `third-party.md` 逐条执行：从上游地址获取指定范围/版本，安装到与第 1 步相同的 skills 目录。

- Windows + PowerShell 环境可直接运行 `tools/install-skills.ps1`。
- 其他平台：克隆上游仓库，把对应分类下的 skill 目录（含 `SKILL.md`）复制过去。

## 第 3 步：安装全局指令

把 `global/AGENTS.md` 的内容，装入你所在 harness 的全局指令文件。

- 复制全文，或按 harness 机制引用（若支持 import）。
- 若目标文件已有内容：合并而非覆盖——追加母版内容，保留用户本机已有的其他内容。

## 第 4 步：安装 MCP 服务器

按 `mcp/mcp.template.json`，把三个服务器加入你所在 harness 的 MCP 配置。

- 模板为 ZCode 风格（`mcp.servers`）；你所在 harness 格式可能不同（如 Claude Code 的顶层 `mcpServers`、Codex 的 `config.toml` 中 `[mcp_servers]`），按其格式转换字段。
- 模板中 `<本地填写：…>` 占位符：向用户索取对应密钥/路径后写入**本机**配置；输出目录选本机合理位置。
- 依赖前置：`uvx`（uv 工具）与 `npx`（Node.js）需可用；缺失时提示用户安装，或改用等效调用方式。

## 第 5 步：建立月度更新定时任务

用你所在 harness 的定时/自动化能力，创建一个**每月执行一次**的任务：

- 触发时间：每月 1 日左右。
- 任务内容固定为一句：「按本仓库（Qi）`SETUP.md` 的《月度更新流程》章节执行」。
- 若你所在 harness 无定时能力：明确告知用户，改为每月手动发送这句话。

## 第 6 步：自检并汇报

逐项输出报告：

1. **skills**：装了哪些、装到哪个路径、所在 harness 是否已识别；
2. **第三方**：每条的安装结果 / 失败原因；
3. **全局指令**：写入了哪个文件、合并方式；
4. **MCP**：三个服务器状态、缺哪些密钥；
5. **定时任务**：是否建立、下次触发时间；
6. **密钥自检**：确认没有任何密钥被写入本仓库目录。

## 月度更新流程（定时任务触发的就是这一节）

1. 在本仓库目录 `git pull` 更新 main；
2. 对 `third-party.md` 每条：获取上游最新版本，与本机已安装版本比较；
3. 有更新时：
   1. 从 main 切出分支 `update/skills-<YYYYMMDD>`；
   2. 在本机安装更新后的 skills；
   3. 若 `third-party.md` 记录的版本/commit 需要变更，同步修改；
   4. 提交并 push 该分支，在 GitHub 开 Pull Request（有 `gh` CLI 用 `gh pr create`，没有就 push 后提示用户手动开）；
   5. PR 描述写清：哪个 skill、从什么版本到什么版本、上游变更摘要。
4. 通知用户人工审阅并合并；**合并前不改动 main**。
5. 无更新时：直接汇报"无更新"。

## 附录：常见 harness 安装位置参考（非权威，以各官方文档为准）

| harness | 用户级 skills | 全局指令 | MCP 配置 |
|---|---|---|---|
| ZCode | `~/.zcode/skills` | `~/.zcode/AGENTS.md` | `~/.zcode/cli/config.json`（`mcp.servers`） |
| Claude Code | `~/.claude/skills` | `~/.claude/CLAUDE.md` | `~/.claude.json` 或 `.mcp.json`（`mcpServers`） |
| Codex CLI | `~/.codex/skills` | `~/.codex/AGENTS.md` | `~/.codex/config.toml`（`[mcp_servers]`） |
| 通用 | `~/.agents/skills` | — | — |
