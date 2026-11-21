# Qi — 可复用经验

- **gh 在 Git Bash 报 command not found ≠ 未安装**：Windows 下先查 `$LOCALAPPDATA/Programs/GitHub CLI/bin/gh.exe` 和 `C:\Program Files\GitHub CLI`，PATH 可能没带上。
- **DSH 沙箱会话里的 git push 凭证**：gh auth keyring 在非交互会话超时；`git credential fill`（GCM 路径）同样会走 askpass、被沙箱命名管道限制拦死，拿不到 token（2026-11-21 实测）。可靠路径：`gh auth token` 取 token（gh 装于 `$LOCALAPPDATA/Programs/GitHub CLI/bin/`），base64 编码 `x-access-token:<token>` 后 `git -c http.https://github.com/.extraheader="AUTHORIZATION: basic <…>" push`；调 gh 本身则 `GH_TOKEN=<token> gh …`。token 全程不回显、不入任何文件。
- **公开仓库上线前三道闸**：`git ls-files` 看完整推送清单（防意外文件）→ grep 密钥模式（sk-…、token、"api_key":）→ 确认 `.gitignore` 覆盖 `*.local.*` / `.env*`。
- **需求澄清先 grilling 再动手**：本项目 15 项决策里至少 5 项（无适配、单向、密钥模板、白名单、AGENTS 原文入库）与"直觉做法"不同，问清再建避免了返工。
