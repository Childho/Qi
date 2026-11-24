# Qi — 可复用经验

- **gh 在 Git Bash 报 command not found ≠ 未安装**：Windows 下先查 `$LOCALAPPDATA/Programs/GitHub CLI/bin/gh.exe` 和 `C:\Program Files\GitHub CLI`，PATH 可能没带上。
- **DSH 沙箱会话里的 git push 凭证**：gh auth keyring 在非交互会话超时；`git credential fill`（GCM 路径）同样会走 askpass、被沙箱命名管道限制拦死，拿不到 token（2026-11-21 实测）。可靠路径：`gh auth token` 取 token（gh 装于 `$LOCALAPPDATA/Programs/GitHub CLI/bin/`），base64 编码 `x-access-token:<token>` 后 `git -c http.https://github.com/.extraheader="AUTHORIZATION: basic <…>" push`；调 gh 本身则 `GH_TOKEN=<token> gh …`。token 全程不回显、不入任何文件。
- **公开仓库上线前三道闸**：`git ls-files` 看完整推送清单（防意外文件）→ grep 密钥模式（sk-…、token、"api_key":）→ 确认 `.gitignore` 覆盖 `*.local.*` / `.env*`。
- **`<template>.textContent` 恒为空字符串**：HTML 解析器把 template 子节点放进 `.content` DocumentFragment，其 childNodes 为空。从 `<template>` 取纯文本必须用 `template.content.textContent`（`innerHTML` 是另一条路但带标签）。实测危害：`clipboard.writeText('')` 合法且 resolve，按钮如实显示「已复制 ✓」，用户粘贴为空——症状完美伪装成「权限/环境问题」。
- **浏览器无法本地跑时，用 Node shim 回路审 JS，但 shim 必须复现真实语义而非只是能跑**：把页面 `<script>` 提取出来，在 Node + 手写 DOM stub 里执行并模拟交互，能给逻辑层定罪/脱罪。但已踩两次 shim 保真度坑：缺 `window` 产生假异常（显式，易发现）；`<template>.textContent` 返回正文而非空（语义差异，**产出假绿**，难发现——真 bug 就这样漏过去的）。写 shim 前先问：目标 API 在真浏览器里对**这类元素/参数**到底返回什么。另：Node 24 的 `global.navigator` 是只读 getter（用 defineProperty）；断言要在触发复原定时器之前算 pass。
- **execCommand('copy') 的静默失败点**：textarea 只 `select()` 不 `focus()`，在部分环境返回 false 且无报错——fallback 必须 `focus()` + `setSelectionRange` 再 copy；剪贴板 API 失败链要落到按钮可见状态，不能只靠 console。
- **无头浏览器启动失败按环境定位**。2026-11-21 的 DSH 沙箱拒绝启动 Crashpad（OpenProcess 0x5）。2026-11-24 在当前 Codex 环境用隔离的 Chrome 配置成功运行本地页面、检查交互并截图。
- **折叠和视觉隐藏用途不同**。折叠面板用 `hidden` 同步移除内容和键盘焦点。窄屏隐藏空表格占位时保留无障碍树中的列关系，并用浏览器的无障碍检查核对。
- **需求澄清先 grilling 再动手**：本项目 15 项决策里至少 5 项（无适配、单向、密钥模板、白名单、AGENTS 原文入库）与"直觉做法"不同，问清再建避免了返工。
- **数量断言先数实物，别信口算**：dashboard 验证时凭印象断言"10 条 prompts"，实际 9 条，差点把正确的输出当 bug 去改；写数字断言前先 glob/ls 点一遍。另：PowerShell `-not $h -match 'x'` 因优先级实际是 `(-not $h) -match 'x'`，产出假信号——否定断言用 `!($h.Contains('x'))` 整体括号。
