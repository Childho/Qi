# Qi

个人 AI 工具配置中心。环境配置（skills / 全局指令 / MCP 的安装与月度更新）见 [SETUP.md](SETUP.md)，人读的介绍见 [README.md](README.md)。

## Agent skills

### Issue tracker

Issues are local markdown files under `.scratch/<feature-slug>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Five canonical triage roles, label strings equal to role names. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `GLOSSARY.md` plus `docs/adr/` at the repo root. See `docs/agents/domain.md`.

## Prompt library

用户的常用提示词收藏在 `prompts/`（一条一文件，用途见各文件头部；用户说「用我那个 XX 提示词」时去这里找）。收录规则与条目模板见 `prompts/README.md`。
