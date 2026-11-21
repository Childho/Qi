# DSH 第三方插件进货单

本清单只记录**来源 + 版本 + 已验证 DSH 版本**，插件内容不入库（由上游维护）。安装见 `SETUP.md` 第 5 步（仅 DeepSeek Harness），回流检查见《插件同步流程》。

## 清单

| 插件 | 版本 | 来源 | 已验证 DSH 版本 | 用途 |
|---|---|---|---|---|
| `@tencent-connect/dsh-qqbot` | `0.5.5` | npm / https://github.com/tencent-connect/dsh-qqbot | `0.1.0-rc.8`（CLI）、`0.2.0-rc.2`（Desktop，上游标注）；`0.2.2-rc.5`（本机 Desktop 运行中，2026-11-21 观察） | 在 QQ 私聊/群聊对话 DSH，含文件发送 |

> 密钥提醒：qqbot 运行配置含 QQ 开放平台密钥，只写入本机 profile 配置，永不入库。

## 收录规则

- **新增第三方插件**：先在本机试用，认可后加一行（包名 + 固定版本 + 来源 + 已验证 DSH 版本），安装用 `install_bundle` 按包名@版本执行。
- **版本固定**：一律锁定具体版本号，不追 latest；升级由《插件同步流程》检查上游后人工确认。
- **停用**：删除对应行，下次同步时从本机 profile 卸载。
- 与根目录 [third-party.md](../third-party.md)（第三方 skills）分工：本文件只管 DSH 插件。
