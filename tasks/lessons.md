# Qi — 可复用经验

- **gh 在 Git Bash 报 command not found ≠ 未安装**：Windows 下先查 `$LOCALAPPDATA/Programs/GitHub CLI/bin/gh.exe` 和 `C:\Program Files\GitHub CLI`，PATH 可能没带上。
- **gh auth keyring 在非交互会话会超时**：解法是从 Git Credential Manager 取 token 注入环境变量绕过 keyring：`printf "protocol=https\nhost=github.com\n" | git credential fill` 提取 `password=`，以 `GH_TOKEN=<token> gh …` 调用。token 全程不回显、不入任何文件。
- **公开仓库上线前三道闸**：`git ls-files` 看完整推送清单（防意外文件）→ grep 密钥模式（sk-…、token、"api_key":）→ 确认 `.gitignore` 覆盖 `*.local.*` / `.env*`。
- **需求澄清先 grilling 再动手**：本项目 15 项决策里至少 5 项（无适配、单向、密钥模板、白名单、AGENTS 原文入库）与"直觉做法"不同，问清再建避免了返工。
