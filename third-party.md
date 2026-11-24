# 第三方 Skills 进货单

本清单只记录**来源 + 范围**，skill 内容不入库（由上游仓库维护）。安装见 `SETUP.md` 第 2 步，月度更新见《月度更新流程》。工作流用法心得见 `docs/workflows.md`。

## 官方（anthropics/skills）

来源：https://github.com/anthropics/skills （Claude Code 亦可用 `/plugin` 命令搜索安装）

| skill | 用途 |
|---|---|
| `docx` / `pdf` / `pptx` / `xlsx` | 办公四件套 |
| `frontend-design` | 最好的前端设计工具 |

技能目录：https://github.com/anthropics/skills/tree/main/skills

## 设计类

| skill | 来源 | 用途 |
|---|---|---|
| `frontend-slides` | https://github.com/zarazhangrui/frontend-slides | 幻灯片制作 |
| `taste`（taste-skill） | https://github.com/Leonxlnx/taste-skill | 设计创意与艺术指导，让 AI 生成有独特视觉风格的网站：提供艺术指导、真实图片、在真实浏览器中自查成果 |
| `impeccable`（hallmark） | https://github.com/nutlope/hallmark | 最终审查、优化、迭代现有界面，设计质量控制工具链；本机安装名 `impeccable` / `impeccable-design-polish` |

## 工作流

| skill | 来源 | 用途 |
|---|---|---|
| mattpocock 全集 | https://github.com/mattpocock/skills | `skills/engineering` + `skills/productivity` 两分类全部（约 27 个，名单以上游为准）。和用户对齐需求、确定方向，代码完全信任大模型，不做硬规范。用法见 `docs/workflows.md` |
| `neat-freak` | https://github.com/KKKKhazix/khazix-skills 的 `neat-freak` 子目录 | 每次干活后收尾，保持文件结构整洁 |

## Superpowers 精选（仅 4 个独立安装，不装框架）

来源：https://github.com/obra/superpowers
定位：主用 Matt Skills，彻底取消 Superpowers 的框架控制，只抽取它最优秀的 4 个 skill 作为独立插件。

| skill | 保留理由 |
|---|---|
| `systematic-debugging` | ✅ 强烈保留，SP 最有价值的 skill 之一 |
| `verification-before-completion` | ✅ 强烈保留，防 AI「嘴上修好了」 |
| `requesting-code-review` | 独立 reviewer subagent 很好 |
| `receiving-code-review` | 防止模型盲从 reviewer |

> 若上游 skill 目录名有变动，以仓库 `skills/` 目录实际为准。

## 收录规则

- **新增第三方 skill**：加一行，写清来源与版本（commit / tag / 分类范围），安装与更新由流程维护。
- **固定某 skill 不随上游漂移**：把"范围"从分类改成具体 commit。
- **停用**：删除对应行，并在下次月度更新时卸载本机对应目录。
