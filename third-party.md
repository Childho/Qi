# 第三方 Skills 进货单

本清单只记录**来源 + 版本/范围**，skill 内容不入库（内容在上游仓库维护）。安装与月度更新流程见 `SETUP.md` 第 2 步与《月度更新流程》。

| 来源 | 范围 / 版本 | 安装方式 | 备注 |
|---|---|---|---|
| https://github.com/mattpocock/skills | `skills/engineering` + `skills/productivity` 两个分类的全部（约 27 个，具体名单以上游当前为准） | Windows：`tools/install-skills.ps1`；其他平台：克隆后按分类复制 | Matt Pocock 的工程/生产力 skill 集 |

## 收录规则

- **新增第三方 skill**：加一行，写清来源与版本（commit / tag / 分类范围），安装与更新由流程维护。
- **固定某 skill 不随上游漂移**：把"范围"从分类改成具体 commit。
- **停用**：删除对应行，并在下次月度更新时卸载本机对应目录。
