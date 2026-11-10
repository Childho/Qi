# Qi — 个人 AI 工具配置中心

> 🤖 **AI Agent 请先读 [SETUP.md](SETUP.md)**：按其指令把本仓库的配置安装到当前环境。

这是我的 AI 工作环境集中配置仓库：skills、全局指令母版、MCP 模板。换电脑、换 harness（AI 编程工具外壳）时，克隆本仓库并对 AI 说一句话即可完成配置。

## 新机器怎么用（3 步）

1. `git clone https://github.com/<你的用户名>/Qi`（任何位置）
2. 对你正在用的 AI 工具说：
   > 阅读 `<克隆路径>/SETUP.md`，按它的说明把我的环境配置好。
3. 按提示补填 API key（密钥只进本机，永不入库）。

## 仓库结构

| 路径 | 作用 |
|---|---|
| `SETUP.md` | 给 AI 的安装指令（唯一真源） |
| `global/AGENTS.md` | 全局指令母版（沟通与工作方式约定） |
| `skills/` | 我自己的 skills。**目录即收录清单**：在即收录，不在即未收录 |
| `third-party.md` | 第三方 skills 进货单（来源 + 版本，内容不入库） |
| `mcp/mcp.template.json` | MCP 配置模板（密钥一律占位符） |
| `tools/` | 平台参考脚本（如 Windows 安装脚本） |
| `docs/agents/` | 本仓库的 agent 工作约定 |

## 维护规则

- **收录**：skill 先在本机试用，认可后手动拷入 `skills/` 并提交。仓库不做自动回流。
- **第三方更新**：每月由定时任务触发 `SETUP.md` 的《月度更新流程》，自动开 PR，人工审阅合并。
- **安全红线**：任何 API key / token 不入库，模板只存占位符，密钥仅存在于本机配置。

人读的工作约定见 [AGENTS.md](AGENTS.md)。
