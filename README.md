# Qi — 个人 AI 工具配置中心

> 🤖 **AI Agent 请先读 [SETUP.md](SETUP.md)**：按其指令把本仓库的配置安装到当前环境。

这是我的 AI 工作环境集中配置仓库：skills、全局指令母版、MCP 模板。换电脑、换 harness（AI 编程工具外壳）时，克隆本仓库并对 AI 说一句话即可完成配置。

## 新机器怎么用（3 步）

1. `git clone https://github.com/Childho/Qi`（任何位置）
2. 对你正在用的 AI 工具说：
   > 阅读 `<克隆路径>/SETUP.md`，按它的说明把我的环境配置好。
3. 按提示补填 API key（密钥只进本机，永不入库）。

## 仓库结构

| 路径 | 作用 |
|---|---|
| `SETUP.md` | 给 AI 的安装指令（唯一真源） |
| `global/AGENTS.md` | 用户级通用全局指令的唯一母版，换机恢复时使用；资产面板的「核心提示词」可查看和复制 |
| `skills/` | 我自己的 skills。**目录即收录清单**：在即收录，不在即未收录 |
| `plugins/` | 我自己的 DeepSeek Harness（DSH）插件包源码。**目录即收录清单**，同 `skills/`。安装见 SETUP.md 第 5 步 |
| `plugins/third-party.md` | DSH 第三方插件进货单（来源 + 版本 + 已验证 DSH 版本，内容不入库） |
| `third-party.md` | 第三方 skills 进货单（来源 + 版本，内容不入库） |
| `prompts/` | 我常用的提示词收藏（纯文本）。**目录即收录清单**，一条一文件，规则见 [prompts/README.md](prompts/README.md) |
| `mcp/mcp.template.json` | MCP 配置模板（密钥一律占位符） |
| `tools/` | 平台参考脚本（如 Windows 安装脚本）与 dashboard 生成器（`build-dashboard.py` 扫描仓库生成根目录 `dashboard.html` 资产面板，生成物不入库） |
| `docs/workflows.md` | 我的工作流手册（skills 使用心得与场景速查） |
| `docs/agents/` | 本仓库的 agent 工作约定 |

## 查看资产面板

在仓库根目录运行 `python tools/build-dashboard.py`，然后双击 `dashboard.html`。首屏按类型汇总仓库资产，快捷目录可跳到各类清单，常用提示词可直接复制，核心提示词可展开查看或复制。

## 维护规则

- **收录**：skill 先在本机试用，认可后手动拷入 `skills/` 并提交。仓库不做自动回流。
- **DSH 插件**：在各项目里开发并装进本机 profile（DSH 是 DeepSeek Harness 的缩写，AI 工具外壳）。认可后源码入 `plugins/`（自研）或记一行进 `plugins/third-party.md`（第三方）。定期回流：月度任务自动兜底，或随时对 AI 说「按 Qi 的《插件同步流程》执行」；新插件只报告待审，不自动入库。
- **提示词**：只收实际在用的，一条一文件入 `prompts/`（模板见 [prompts/README.md](prompts/README.md)），不常用即删。提示词是纯文本、无执行风险，**豁免**"第三方内容不入库"：外部来源可直接入库，但条目内标一行出处（第三方代码/工具仍走进货单）。
- **第三方更新**：每月由定时任务触发 `SETUP.md` 的《月度更新流程》，自动开 PR，人工审阅合并。
- **安全红线**：任何 API key / token 不入库，模板只存占位符，密钥仅存在于本机配置。

人读的工作约定见 [AGENTS.md](AGENTS.md)。
