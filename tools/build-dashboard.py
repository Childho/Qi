#!/usr/bin/env python3
"""Qi 资产面板生成器 —— 扫描仓库，生成静态 dashboard.html。

设计决策见 docs/adr/0001-dashboard-static-snapshot.md：
  静态快照 / 仅 Qi 仓库数据源 / 健康度=时间视角无红绿灯 / 生成物不入库。
界面：KARLO 纸墨色系、仓库资产分布、快捷目录和可折叠清单，离线可用。

数据来源与解析规则（进货单是给人读的自由格式 markdown，格式大改时同步改这里）：
  1. skills/            目录即清单；SKILL.md frontmatter 的 description 作简介
  2. third-party.md     按 `## 节` 分组（跳过"收录规则"）；表格行第一列是名称，
                        可能是 `a` / `b` 反引号多列（拆成多条）；节内独立
                        "来源：" 行作为节级来源；列数不固定，最后列视为用途
  3. plugins/           目录即清单（排除 third-party.md）；有 package.json 的 DSH 插件
                        取版本与 dsh.compatibility，简介取 locale/zh.json meta.description；
                        无 package.json 的独立插件包取 README 的 H1 名称与标题后首段
  4. plugins/third-party.md  固定 5 列：插件|版本|来源|已验证 DSH 版本|用途
  5. prompts/           一条一文件（排除 README.md）；头部 H1=标题，> 用途：，> 来源：
  6. mcp/mcp.template.json   mcp.servers；env 值中 "<本地填写" 计为待填密钥
  7. tasks/todo.md      `## 当前阶段` 文本 + `## 待办` 的 checklist
  8. global/AGENTS.md   用户级通用全局指令，换机恢复的唯一母版

用法：python tools/build-dashboard.py   （在 Qi 仓库根或任意目录均可，自动定位）
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "dashboard.html"
PLACEHOLDER = "<本地填写"

# 独立仓库插件的母本地址（与 SETUP.md《插件同步流程》第 3 步一致）。
# 归档目录须与上游逐字节一致，不能往里加文件，故 Qi 侧在此记录。
INDEPENDENT_PLUGIN_SOURCES = {
    "zcode-tempo": "https://github.com/Childho/zcode-tempo",
}


# ---------- 基础工具 ----------

def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def git_last_commit(*paths: str) -> datetime | None:
    """某路径（文件/目录）最后一次提交时间；git 不可用或未提交返回 None。"""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", *paths],
            cwd=REPO, capture_output=True, text=True, encoding="utf-8",
        )
        s = out.stdout.strip()
        return datetime.fromisoformat(s) if s else None
    except Exception:
        return None


def days_ago(dt: datetime | None) -> str:
    if dt is None:
        return "—"
    n = (datetime.now(timezone.utc) - dt).days
    return f"{n} 天前" if n > 0 else "今天"


def rel_days(dt: datetime | None) -> int | None:
    return None if dt is None else (datetime.now(timezone.utc) - dt).days


def fmt_date(dt: datetime | None) -> str:
    return dt.strftime("%Y-%m-%d") if dt else "未提交"


def when_cell(dt: datetime | None) -> str:
    if dt is None:
        return '<td class="when" data-label="变更">—</td>'
    cls = "when fresh" if rel_days(dt) <= 0 else "when"
    return f'<td class="{cls}" data-label="变更"><time title="{fmt_date(dt)}" datetime="{fmt_date(dt)}">{days_ago(dt)}</time></td>'


def rel_html(dt: datetime | None) -> str:
    if dt is None:
        return "—"
    label = escape(days_ago(dt))
    return f'<span class="fresh">{label}</span>' if rel_days(dt) <= 0 else label


def short_url(text: str) -> tuple[str | None, str, str]:
    """从 'https://github.com/x （注）' 取 (url, 去协议展示文本, 备注)。无 URL 返回 (None, 原文, '')。"""
    text = (text or "").strip()
    m = re.search(r"https?://[^\s（）()\"'「」]+", text)
    if not m:
        return None, text, ""
    url = m.group(0)
    rest = (text[:m.start()] + text[m.end():]).strip()
    disp = re.sub(r"^https?://", "", url).rstrip("/")
    return url, disp, rest


def split_table_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_table_row(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and s.count("|") >= 2


def is_separator_row(line: str) -> bool:
    return bool(re.match(r"^\|[\s:|-]+\|$", line.strip()))


# ---------- 数据采集 ----------

def collect_own_skills() -> tuple[list[dict], datetime | None]:
    items, latest = [], None
    base = REPO / "skills"
    for d in sorted(base.iterdir()) if base.is_dir() else []:
        if not d.is_dir() or d.name.startswith("."):
            continue
        m = re.search(r"^description:\s*(.+)$", read_text(d / "SKILL.md"), re.M)
        t = git_last_commit(f"skills/{d.name}")
        items.append({"name": d.name, "desc": m.group(1).strip() if m else "", "when": t})
        latest = max(latest, t) if latest and t else (t or latest)
    return items, latest


def collect_third_party_skills() -> tuple[list[dict], datetime | None]:
    """返回 (节列表, 清单最后变更时间)。每节 = {title, source, rows:[{name,desc}]}"""
    text = read_text(REPO / "third-party.md")
    sections, cur = [], None
    for line in text.splitlines():
        if line.startswith("## "):
            title = line[3:].strip()
            cur = {"title": title, "source": "", "rows": []} if title != "收录规则" else None
            if cur:
                sections.append(cur)
        elif cur is not None:
            s = line.strip()
            if s.startswith("来源：") or s.startswith("来源:"):
                cur["source"] = re.sub(r"^来源[：:]\s*", "", s)
            elif is_table_row(s):
                if is_separator_row(s):
                    # 分隔行的上一行是表头，丢弃（若缓冲为空则只是杂线）
                    if cur["rows"] and cur["rows"][-1].get("_header"):
                        cur["rows"].pop()
                else:
                    cells = split_table_row(s)
                    names, source, desc = cells[0].strip(" `"), "", cells[-1]
                    if len(cells) >= 3 and ("http" in cells[1] or "github" in cells[1]):
                        source = cells[1].strip(" `")
                    cur["rows"].append({"_header": names in ("skill", "插件", "名称"),
                                        "name": names, "desc": desc,
                                        "source": source or cur["source"]})
    for sec in sections:
        expanded = []
        for r in sec["rows"]:
            if r.pop("_header", None):
                continue
            # `a` / `b` / `c` 反引号多名称拆成多条，简介/来源共享；别名括号完整保留
            parts = [p.replace("`", "").strip() for p in r["name"].split("/")]
            for p in filter(None, parts):
                expanded.append({"name": p, "desc": r["desc"], "source": r["source"]})
        sec["rows"] = expanded
    return sections, git_last_commit("third-party.md")


def read_readme_summary(d: Path) -> tuple[str, str]:
    """无 package.json 的独立插件包：README 的 H1 作名称、标题后首段作简介。"""
    lines = read_text(d / "README.md").splitlines()
    name = next((l[2:].strip() for l in lines if l.startswith("# ")), d.name)
    desc, seen_title = "", False
    for l in lines:
        s = l.strip()
        if not seen_title:
            seen_title = s.startswith("# ")
        elif s and not s.startswith(("#", ">", "|", "```")):
            desc = s
            break
    return name, desc


def collect_own_plugins() -> tuple[list[dict], datetime | None]:
    items, latest = [], None
    base = REPO / "plugins"
    for d in sorted(base.iterdir()) if base.is_dir() else []:
        if not d.is_dir():
            continue
        pkg_text = read_text(d / "package.json")
        if pkg_text:  # DSH 插件包：package.json + locale 提供版本与简介
            pkg = json.loads(pkg_text)
            dsh = pkg.get("dsh", {})
            verified = ", ".join(dsh.get("compatibility", {}).get("dshReleases", {}).keys())
            desc = ""
            for loc in ("zh", "en"):
                meta = json.loads(read_text(d / "locale" / f"{loc}.json") or "{}").get("meta", {})
                desc = desc or meta.get("description", "")
            name, meta_str = (pkg.get("name", d.name),
                              f"v{pkg.get('version', '?')}" + (f" · 已验证 DSH {verified}" if verified else ""))
        else:  # 独立插件包（如 ZCode 桌面插件，无 package.json）：README 取名称与首段简介
            name, desc = read_readme_summary(d)
            meta_str = "独立插件包"
        t = git_last_commit(f"plugins/{d.name}")
        items.append({"name": name, "desc": desc, "meta": meta_str,
                      "src": INDEPENDENT_PLUGIN_SOURCES.get(d.name, ""), "when": t})
        latest = max(latest, t) if latest and t else (t or latest)
    return items, latest


def collect_third_party_plugins() -> tuple[list[dict], datetime | None]:
    items = []
    for line in read_text(REPO / "plugins" / "third-party.md").splitlines():
        s = line.strip()
        if is_table_row(s) and not is_separator_row(s):
            c = [x.strip(" `") for x in split_table_row(s)]
            if len(c) >= 5 and c[0] != "插件":
                items.append({"name": c[0], "ver": c[1], "source": c[2], "dsh": c[3], "desc": c[4]})
    return items, git_last_commit("plugins/third-party.md")


def prompt_body(text: str) -> str:
    """README 约定：第一条 --- 分隔线以下 = 复制区。无分隔线则取全文。"""
    parts = re.split(r"^---\s*$", text, maxsplit=1, flags=re.M)
    body = parts[1] if len(parts) > 1 else text
    return body.strip()


def collect_prompts() -> tuple[list[dict], datetime | None]:
    items, latest = [], None
    base = REPO / "prompts"
    for f in sorted(base.glob("*.md")) if base.is_dir() else []:
        if f.name == "README.md":
            continue
        text = read_text(f)
        head = text.splitlines()
        title = next((l.lstrip("# ").strip() for l in head if l.startswith("# ")), f.stem)
        use = next((re.sub(r"^>\s*用途：?\s*", "", l).strip() for l in head if "用途" in l), "")
        src = next((re.sub(r"^>\s*来源：?\s*", "", l).strip() for l in head if l.startswith("> 来源")), "")
        t = git_last_commit(f"prompts/{f.name}")
        items.append({"name": title, "desc": use, "source": src, "file": f.name,
                      "body": prompt_body(text), "when": t})
        latest = max(latest, t) if latest and t else (t or latest)
    return items, latest


def collect_mcp() -> tuple[list[dict], datetime | None]:
    data = json.loads(read_text(REPO / "mcp" / "mcp.template.json"))
    items = []
    for name, cfg in data.get("mcp", {}).get("servers", {}).items():
        cmd = cfg.get("command", "?") + " " + " ".join(cfg.get("args", []))
        placeholders = sum(1 for v in _iter_strings(cfg) if PLACEHOLDER in v)
        flags = []
        if not cfg.get("enabled", True):
            flags.append("默认停用")
        if placeholders:
            flags.append(f"{placeholders} 项待填密钥")
        items.append({
            "name": name,
            "desc": cfg.get("_note", ""),
            "meta": cmd + (" · " + "、".join(flags) if flags else ""),
        })
    return items, git_last_commit("mcp/mcp.template.json")


def _iter_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _iter_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _iter_strings(v)


def collect_plan() -> tuple[dict, datetime | None]:
    text = read_text(REPO / "tasks" / "todo.md")
    stage, todos, bucket = "", [], "stage"
    for line in text.splitlines():
        if line.startswith("## "):
            bucket = "todo" if "待办" in line else ("stage" if "当前阶段" in line else "")
        elif bucket == "stage" and line.strip():
            stage = line.strip()
        elif bucket == "todo" and line.strip().startswith("- ["):
            done = "[x]" in line
            body = re.sub(r"^- \[[ xX]\]\s*", "", line).strip()
            todos.append({"done": done, "text": body})
    return {"stage": stage, "todos": todos}, git_last_commit("tasks/todo.md")


# ---------- 界面 ----------

CSS = """
:root {
  color-scheme: light dark;
  --paper: #f4f2eb; --surface: #fffcf6; --ink: #20362d; --muted: #535f55;
  --line: #d8dbce; --hover: #f0f2e8; --accent: #8d442f; --focus: #a15038;
  --forest: #152e26; --hero-ink: #fbf4e5; --hero-muted: #c1ccbc;
  --skills: #b7cc99; --plugins: #e3ad8b; --prompts: #ebcd80; --mcp: #a9c9cd;
  --serif: Georgia, "Noto Serif SC", "Songti SC", SimSun, serif;
  --sans: "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
  --mono: "Cascadia Mono", Consolas, ui-monospace, monospace;
}
@media (prefers-color-scheme: dark) {
  :root {
    --paper: #181f1c; --surface: #202923; --ink: #eef0e5; --muted: #b6c2b7;
    --line: #3d4a40; --hover: #2c382f; --accent: #efb198; --focus: #f0ad8c;
    --forest: #142d24;
  }
}
* { box-sizing: border-box }
body { margin: 0; background: var(--paper); color: var(--ink); font: 14px/1.65 var(--sans) }
a { color: var(--accent); text-underline-offset: .2em }
button { color: inherit; font: inherit }
:focus-visible { outline: 2px solid var(--focus); outline-offset: 3px }
[hidden] { display: none !important }
code, .mono, time { font-family: var(--mono) }
code, td, li { overflow-wrap: anywhere }
.skip { position: fixed; z-index: 5; top: 12px; left: 12px; padding: 8px 12px;
  background: var(--surface); transform: translateY(calc(-100% - 20px)) }
.skip:focus { transform: none }
.shell { width: min(100% - 80px, 1280px); margin-inline: auto }
.topbar { display: flex; align-items: center; justify-content: space-between; gap: 12px; min-height: 72px }
.brand { display: flex; align-items: center; gap: 12px; font-weight: 650 }
.seal { display: grid; place-items: center; width: 35px; height: 35px; flex: none; border-radius: 10px;
  background: var(--forest); color: var(--hero-ink); font: 700 20px/1 var(--serif) }
.snapshot { display: flex; gap: 8px 12px; align-items: baseline; margin: 0; color: var(--muted); font-size: 12px }
.snapshot time { color: var(--ink) }

.hero { display: grid; grid-template-columns: minmax(0, 1.12fr) minmax(0, .88fr); align-items: stretch;
  gap: clamp(28px, 6vw, 90px); padding: clamp(28px, 5vw, 72px);
  background: var(--forest); color: var(--hero-ink); border-radius: 20px;
  background-image: radial-gradient(ellipse at 90% 0%, #254334 0%, transparent 64%) }
.hero-main { align-self: center }
.hero h1 { margin: 0 0 14px; font-size: clamp(30px, 4.4vw, 58px); font-weight: 750;
  line-height: 1.18; letter-spacing: -.045em }
.hero p { margin: 0; color: var(--hero-muted); font-size: 14px }
.hero .commit { display: flex; flex-wrap: wrap; gap: 4px 10px; margin-top: 34px; font-size: 12px }
.commit time { color: var(--hero-ink) }
.distribution { min-width: 0; border-left: 1px solid #567060; padding-left: clamp(20px, 4vw, 54px); align-self: center }
.distribution-head { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; margin-bottom: 14px }
.distribution h2 { margin: 0; color: var(--hero-muted); font-size: 14px; font-weight: 600 }
.asset-total { display: flex; gap: 8px; align-items: baseline }
.asset-total strong { font: 400 clamp(42px, 5vw, 64px)/.9 var(--serif); font-variant-numeric: lining-nums }
.asset-total span { color: var(--hero-muted); font-size: 12px }
.mix { display: flex; gap: 3px; height: 11px; overflow: hidden; border-radius: 3px; background: #456353 }
.mix span { flex-basis: 0; background: var(--category) }
[data-category="skills"] { --category: var(--skills) }
[data-category="plugins"] { --category: var(--plugins) }
[data-category="prompts"] { --category: var(--prompts) }
[data-category="mcp"] { --category: var(--mcp) }
.legend { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 24px;
  list-style: none; margin: 10px 0 0; padding: 0 }
.legend li { display: flex; align-items: center; gap: 8px; padding: 7px 0 2px; font-size: 13px }
.legend li::before { content: ""; width: 8px; height: 8px; border-radius: 2px;
  background: var(--category); flex: none }
.legend b { margin-left: auto; font: 600 13px/1 var(--mono) }

.workspace { --jump-offset: 16px; display: grid; grid-template-columns: minmax(170px, .22fr) minmax(0, 1fr);
  align-items: start; gap: clamp(28px, 4.5vw, 64px); margin-top: 44px }
.directory { position: sticky; top: 22px; border-right: 1px solid var(--line); padding-right: 18px }
.directory h2 { margin: 2px 0 10px 10px; color: var(--muted); font-size: 12px; font-weight: 650 }
.toc { display: grid; gap: 3px }
.toc a { display: flex; align-items: center; position: relative; min-height: 38px; padding: 6px 10px;
  border-radius: 7px; font-size: 13px; color: var(--muted); text-decoration: none }
.toc a:hover, .toc a[aria-current="location"] { background: var(--hover); color: var(--ink) }
.toc a[aria-current="location"] { font-weight: 700 }
.toc a[aria-current="location"]::before { content: ""; position: absolute; left: 0; height: 16px;
  width: 2px; border-radius: 2px; background: var(--accent) }
.toc .maintenance { margin-top: 6px }

.catalog { min-width: 0; scroll-margin-top: var(--jump-offset) }
.catalog-head { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center;
  gap: 8px 14px; margin: 0 0 12px }
.catalog-head h2 { margin: 0; font-size: 24px; line-height: 1.25; letter-spacing: -.035em }
.control, .copy { display: inline-flex; align-items: center; justify-content: center; min-height: 36px;
  color: var(--ink); background: var(--surface); border: 1px solid var(--line); border-radius: 7px;
  padding: 4px 12px; cursor: pointer; font-size: 12px; font-weight: 650; white-space: nowrap }
.control:hover, .copy:hover { background: var(--hover); border-color: var(--muted) }
.inventory { background: var(--surface); border: 1px solid var(--line); border-radius: 13px }
.inventory section + section { border-top: 1px solid var(--line) }
.inventory section { scroll-margin-top: var(--jump-offset) }
.sec-h { margin: 0 }
.sec-head { display: grid; grid-template-columns: 7px minmax(0, 1fr) auto auto 30px;
  gap: 6px 14px; align-items: center; width: 100%; min-height: 63px; padding: 10px 17px 10px 21px;
  border: 0; background: transparent; text-align: left; cursor: pointer }
.sec-head:focus-visible { outline-offset: -3px; border-radius: 7px }
.sec-head:hover:not(:disabled), .sec-head[aria-expanded="true"]:not(:disabled) { background: var(--hover) }
.inventory section:first-child .sec-head { border-radius: 12px 12px 0 0 }
.inventory section:last-child .sec-head[aria-expanded="false"] { border-radius: 0 0 12px 12px }
.sec-head:disabled { cursor: default; opacity: 1 }
.category-mark { width: 7px; height: 20px; border-radius: 3px; background: var(--category, var(--line)) }
.sec-title { font-size: 15px; line-height: 1.4; font-weight: 700 }
.sec-count { padding: 2px 7px; border-radius: 5px; background: var(--paper);
  font: 12px/1.5 var(--mono); white-space: nowrap }
.sec-meta { min-width: 83px; color: var(--muted); font-size: 12px; font-weight: 400; text-align: right; white-space: nowrap }
.fresh { color: var(--accent) }
.chev { justify-self: end; display: grid; place-items: center; width: 26px; height: 26px;
  border: 1px solid var(--line); border-radius: 7px; color: var(--muted) }
.chev::before { content: ""; width: 6px; height: 6px; border: solid currentColor;
  border-width: 0 1.5px 1.5px 0; transform: translateY(-1px) rotate(45deg) }
.sec-head[aria-expanded="true"] .chev::before { transform: translateY(2px) rotate(225deg) }
.sec-head:disabled .chev { visibility: hidden }
.fold { padding: 4px 21px 16px }

table { width: 100%; border-collapse: collapse }
th { padding: 12px 14px 7px 0; color: var(--muted); font-size: 12px; font-weight: 600;
  border-bottom: 1px solid var(--line); text-align: left; white-space: nowrap }
td { padding: 9px 14px 9px 0; border-bottom: 1px solid var(--line); vertical-align: top; font-size: 13px }
tbody tr:last-child td { border-bottom: 0 }
td:last-child, th:last-child { padding-right: 0 }
td.name { min-width: 100px; font-weight: 650 }
td.name.mono { font-size: 12.5px }
td.desc, td.meta, td.when { color: var(--muted) }
td.meta { font-size: 12px }
td.unset { color: var(--muted) }
td.when { white-space: nowrap; font-size: 12px }
td.act { text-align: right }
td .src-line { display: block; margin-top: 2px; color: var(--muted); font: 400 11px/1.65 var(--mono) }
tr.group td { padding: 13px 0 6px; border: 0 }
.group-title { margin-right: 10px; font-weight: 700 }
.group-src { color: var(--muted); font-size: 12px }
.warn, .copy.err { color: var(--accent) }
.copy.ok { color: var(--ink); background: var(--hover); border-color: var(--muted) }
.cmd { display: block }
.flags { display: block; margin-top: 3px; font-size: 12px }
.stage, .empty { margin: 10px 0 3px; color: var(--muted) }
.stage { padding-left: 12px; border-left: 2px solid var(--accent) }
.plan { list-style: none; margin: 12px 0 0; padding: 0 }
.plan li { display: flex; gap: 10px; margin-bottom: 6px }
.plan li::before { content: "—"; color: var(--muted) }
.plan li.done { color: var(--muted) }
.plan li.done::before { content: "✓"; color: var(--accent) }
.core-tools { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
  gap: 8px 12px; margin: 10px 0 8px }
.core-tools p { margin: 0; color: var(--muted) }
.core-preview summary { min-height: 30px; padding: 4px 0; cursor: pointer; font-weight: 650 }
.core-text { margin: 8px 0 0; padding: 14px; background: var(--paper); border-radius: 7px;
  white-space: pre-wrap; overflow-wrap: anywhere; font: 13px/1.75 var(--mono) }
.sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap }
footer { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 6px 16px;
  margin: 34px 0 26px; padding-top: 15px; border-top: 1px solid var(--line); color: var(--muted); font-size: 12px }

@media (max-width: 920px) {
  .shell { width: calc(100% - 48px) }
  .workspace { grid-template-columns: 140px minmax(0, 1fr); gap: 22px }
  .directory { padding-right: 12px }
}
@media (max-width: 740px) {
  .workspace { --jump-offset: 144px; display: block; margin-top: 14px }
  .directory { top: 0; z-index: 2; border: 0; padding: 6px 0 10px; margin-bottom: 18px;
    background: var(--paper); border-bottom: 1px solid var(--line) }
  .directory h2 { margin-left: 0 }
  .toc { grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 4px }
  .toc a { justify-content: center; min-height: 44px; padding: 4px; text-align: center;
    line-height: 1.35; background: var(--surface) }
  .toc .maintenance { margin-top: 0 }
}
@media (max-width: 580px) {
  .shell { width: calc(100% - 28px) }
  .topbar { min-height: 60px }
  .brand { font-size: 12px }
  .snapshot { flex-direction: column; align-items: flex-end; gap: 0; text-align: right; font-size: 11px }
  .hero { grid-template-columns: minmax(0, 1fr); gap: 20px; padding: 23px; border-radius: 15px }
  .hero h1 { margin-bottom: 8px }
  .hero .commit { margin-top: 16px }
  .distribution { border-left: 0; border-top: 1px solid #567060; padding: 14px 0 0 }
  .distribution-head { margin-bottom: 9px }
  .legend { margin-top: 5px }
  .catalog-head h2 { font-size: 21px }
  .sec-head { grid-template-columns: 6px minmax(0, 1fr) auto 26px; gap: 3px 9px; padding: 9px 11px; min-height: 62px }
  .category-mark { grid-row: span 2; width: 6px }
  .sec-title { grid-column: 2; font-size: 14px }
  .sec-count { grid-column: 3; grid-row: 1 / span 2 }
  .sec-meta { grid-column: 2; min-width: 0; text-align: left; font-size: 11px }
  .chev { grid-column: 4; grid-row: 1 / span 2 }
  .fold { padding: 0 12px 11px }
  thead { position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%) }
  table, tbody { display: block }
  tbody tr { display: grid; grid-template-columns: minmax(0, 1fr) auto; align-items: start;
    gap: 3px 8px; padding: 9px 0; border-bottom: 1px solid var(--line) }
  tbody tr:last-child, tr.group { border-bottom: 0 }
  td, tr.group td { grid-column: 1 / -1; padding: 0; border: 0 }
  td.name { min-width: 0; grid-column: 1; grid-row: 1 }
  td.act { grid-column: 2; grid-row: 1 }
  td[data-label]::before { content: attr(data-label); color: var(--muted);
    font: 12px/1.5 var(--sans); margin-right: 8px }
  td.unset { position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%) }
  td.desc { line-height: 1.55 }
  .toc a { font-size: 12px }
  .control, .copy { min-height: 44px }
}
"""

# 折叠、目录和复制。脚本禁用时，正文保持可读。
JS = """
(() => {
  const key = 'qi-dash-fold-v1';
  const sections = [...document.querySelectorAll('.inventory section')];
  const links = [...document.querySelectorAll('.toc a')];
  const directory = document.querySelector('.directory');
  const toggleAll = document.querySelector('#toggle-all');
  let saved = {};
  try {
    const stored = JSON.parse(localStorage.getItem(key));
    if (stored && typeof stored === 'object' && !Array.isArray(stored)) saved = stored;
  } catch {}
  function save() {
    try { localStorage.setItem(key, JSON.stringify(saved)); } catch {}
  }
  function setOpen(section, open) {
    const button = section.querySelector('.sec-head');
    const panel = section.querySelector('.fold');
    if (!open && panel.contains(document.activeElement)) button.focus();
    button.setAttribute('aria-expanded', String(open));
    panel.hidden = !open;
    saved[section.id] = open;
  }
  function syncToggle() {
    toggleAll.textContent = sections.every(section => saved[section.id]) ? '全部收起' : '全部展开';
  }
  function markCurrent(id) {
    for (const link of links) {
      if (link.hash.slice(1) === id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    }
  }
  function openHash() {
    const section = sections.find(section => '#' + section.id === location.hash);
    if (!section) return;
    setOpen(section, true);
    save();
    syncToggle();
    section.scrollIntoView();
    markCurrent(section.id);
  }
  for (const section of sections) {
    const button = section.querySelector('.sec-head');
    button.disabled = false;
    setOpen(section, saved[section.id] === true);
    button.addEventListener('click', () => {
      setOpen(section, !saved[section.id]);
      save();
      syncToggle();
      markCurrent(section.id);
    });
  }
  toggleAll.hidden = false;
  syncToggle();
  toggleAll.addEventListener('click', () => {
    const open = !sections.every(section => saved[section.id]);
    for (const section of sections) setOpen(section, open);
    save();
    syncToggle();
  });
  for (const link of links) {
    link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      if (location.hash === link.hash) {
        event.preventDefault();
        openHash();
      }
    });
  }
  let scrollFrame = 0;
  function syncCurrent() {
    scrollFrame = 0;
    const top = section => section.getBoundingClientRect().top;
    const current = sections.find(section => '#' + section.id === location.hash);
    const atBottom = window.scrollY > 0 &&
      window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 2;
    const offset = directory.getBoundingClientRect().top === 0 ? directory.offsetHeight + 22 : 40;
    let active = sections[0];
    for (const section of sections) {
      if (top(section) > offset) break;
      active = section;
    }
    if (atBottom && current && top(current) >= 0 && top(current) < innerHeight) active = current;
    markCurrent(active.id);
  }
  window.addEventListener('scroll', () => {
    if (!scrollFrame) scrollFrame = requestAnimationFrame(syncCurrent);
  }, { passive: true });
  window.addEventListener('hashchange', openHash);
  syncCurrent();
  openHash();
})();
"""

COPYJS = """
(() => {
  const resetTimers = new WeakMap();
  const activeCopies = new WeakSet();
  const status = document.querySelector('#copy-status');
  function fallback(text) {
    const focused = document.activeElement;
    const input = document.createElement('textarea');
    input.value = text;
    input.readOnly = true;
    input.style.cssText = 'position:fixed;top:0;left:0;opacity:0';
    document.body.append(input);
    try {
      input.focus();
      input.select();
      input.setSelectionRange(0, text.length);
      return document.execCommand('copy');
    } catch {
      return false;
    } finally {
      input.remove();
      if (document.activeElement === document.body) focused?.focus({ preventScroll: true });
    }
  }
  for (const button of document.querySelectorAll('.copy')) {
    button.hidden = false;
    button.addEventListener('click', async () => {
      if (activeCopies.has(button)) return;
      activeCopies.add(button);
      clearTimeout(resetTimers.get(button));
      // template 的正文在 DocumentFragment 里，直接读取节点会得到空字符串。
      const text = button.nextElementSibling.content.textContent;
      let copied = false;
      if (text) {
        try {
          await navigator.clipboard.writeText(text);
          copied = true;
        } catch {
          copied = fallback(text);
        }
      }
      button.textContent = copied ? '已复制 ✓' : '复制失败，重试';
      button.classList.toggle('ok', copied);
      button.classList.toggle('err', !copied);
      status.textContent = copied ? button.getAttribute('aria-label') + '成功' : '复制失败，请重试';
      activeCopies.delete(button);
      resetTimers.set(button, setTimeout(() => {
        button.textContent = '复制';
        button.classList.remove('ok', 'err');
        status.textContent = '';
      }, 1800));
    });
  }
})();
"""


def table_html(headers: list[str], rows: list[str]) -> str:
    if not rows:
        return '<p class="empty">清单暂时为空。</p>'
    cells = "".join(
        f'<th scope="col">{escape(h)}</th>' if h else '<th scope="col"><span class="sr-only">操作</span></th>'
        for h in headers
    )
    return f'<table role="table"><thead><tr>{cells}</tr></thead><tbody>{"".join(rows)}</tbody></table>'


def desc_cell(text: str) -> str:
    return f'<td class="desc">{escape(text) if text else "—"}</td>'


def meta_cell(text: str, label: str) -> str:
    return f'<td class="meta mono" data-label="{label}">{escape(text) if text else "—"}</td>'


def copy_button(label: str, body: str) -> str:
    return (
        f'<button type="button" class="copy" aria-label="{escape(label)}" hidden>复制</button>'
        f'<template class="p-body">{escape(body)}</template>'
    )


def plan_text(text: str) -> str:
    """规划的行内加粗和代码标记，其他字符按纯文本显示。"""
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escape(text))
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)


def ext_link(url: str, text: str) -> str:
    """外部链接一律新标签打开：file:// 同标签跳转可能被浏览器策略拦截，且会丢失面板状态。"""
    return f'<a href="{escape(url)}" target="_blank" rel="noopener">{escape(text)}</a>'


def tpp_src_line(source: str) -> str:
    """第三方插件行的来源小字（与 skills 进货单同款式）。"""
    url, disp, note = short_url(source)
    if not url:
        return ""
    tail = f" {escape(note)}" if note else ""
    return f'<span class="src-line">{ext_link(url, disp)}{tail}</span>'


def src_cell(text: str) -> str:
    url, disp, note = short_url(text)
    if url:
        tail = f" {escape(note)}" if note else ""
        return f'<td class="meta" data-label="来源">{ext_link(url, disp)}{tail}</td>'
    if text:
        return f'<td class="meta" data-label="来源">{escape(text)}</td>'
    return '<td class="meta unset">—</td>'


def render() -> str:
    now = datetime.now(timezone.utc)
    skills, t_skills = collect_own_skills()
    tp_sections, t_tp = collect_third_party_skills()
    plugins, t_plugins = collect_own_plugins()
    tpp, t_tpp = collect_third_party_plugins()
    prompts, t_prompts = collect_prompts()
    core_path = REPO / "global" / "AGENTS.md"
    core_text = read_text(core_path)
    t_core = git_last_commit("global/AGENTS.md")
    mcp, t_mcp = collect_mcp()
    plan, t_plan = collect_plan()
    repo_last = git_last_commit()

    # 第三方 skills：分组行挂组级来源；行级来源只在不同于组时以小字挂在名称下
    tp_rows = []
    for sec in tp_sections:
        if not sec["rows"]:
            continue
        gurl, gdisp, gnote = short_url(sec["source"])
        gsrc = f" {ext_link(gurl, gdisp)}" if gurl else ""
        gnote_html = (f' <span class="group-src">{escape(gnote)}</span>'
                      if gnote else "")
        tp_rows.append(
            f'<tr class="group"><td colspan="2"><span class="group-title">{escape(sec["title"])}</span>{gsrc}{gnote_html}</td></tr>'
        )
        for r in sec["rows"]:
            rurl, rdisp, rnote = short_url(r["source"])
            sub = ""
            if rurl and rurl != gurl:
                tail = f" {escape(rnote)}" if rnote else ""
                sub = f'<span class="src-line">{ext_link(rurl, rdisp)}{tail}</span>'
            elif rnote and rnote != gnote:
                sub = f'<span class="src-line">{escape(rnote)}</span>'
            tp_rows.append(
                f'<tr><td class="name mono">{escape(r["name"])}{sub}</td>{desc_cell(r["desc"])}</tr>'
            )
    tp_count = sum(len(s["rows"]) for s in tp_sections)

    skills_body = (
        table_html(
            ["名称", "简介", "最后变更"],
            [f'<tr><td class="name mono">{escape(i["name"])}</td>{desc_cell(i["desc"])}{when_cell(i["when"])}</tr>'
             for i in skills],
        )
        if skills
        else '<p class="empty">暂未收录自研技能。将技能放入 <code>skills/</code> 后重新生成面板即可查看。</p>'
    )
    plugins_body = table_html(
        ["名称", "简介", "版本", "最后变更"],
        [f'<tr><td class="name mono">{escape(i["name"])}{tpp_src_line(i["src"])}</td>{desc_cell(i["desc"])}'
         f'{meta_cell(i["meta"], "版本")}{when_cell(i["when"])}</tr>'
         for i in plugins],
    )
    tpp_body = table_html(
        ["名称", "用途", "版本", "已验证 DSH"],
        [f'<tr><td class="name mono">{escape(i["name"])}{tpp_src_line(i["source"])}</td>{desc_cell(i["desc"])}'
         f'{meta_cell(i["ver"], "版本")}{meta_cell(i["dsh"], "已验证 DSH")}</tr>' for i in tpp],
    )
    prompts_body = table_html(
        ["名称", "用途", "来源", "最后变更", ""],
        [f'<tr><td class="name">{escape(i["name"])}</td>{desc_cell(i["desc"])}'
         f'{src_cell(i["source"])}{when_cell(i["when"])}'
         f'<td class="act">{copy_button("复制提示词 " + i["name"], i["body"])}</td></tr>'
         for i in prompts],
    )
    core_body = (
        '<div class="core-tools"><p>各工具共用的用户级指令。母版 <a href="global/AGENTS.md">'
        '<code>global/AGENTS.md</code></a></p>'
        f'{copy_button("复制核心提示词", core_text)}</div>'
        f'<details class="core-preview"><summary>查看完整内容</summary><pre class="core-text">{escape(core_text)}</pre></details>'
        if core_text else '<p class="empty">未找到或无法读取 global/AGENTS.md，请检查母版文件。</p>'
    )
    mcp_rows = []
    for i in mcp:
        cmd, _, flagstr = i["meta"].partition(" · ")
        flags = " · ".join(
            f'<span class="warn">{escape(f)}</span>' if "密钥" in f else escape(f)
            for f in flagstr.split("、") if f
        )
        state = f'<span class="flags">{flags}</span>' if flags else ""
        mcp_rows.append(
            f'<tr><td class="name">{escape(i["name"])}</td>{desc_cell(i["desc"])}'
            f'<td class="meta"><code class="cmd">{escape(cmd.strip())}</code>{state}</td></tr>'
        )
    mcp_body = table_html(["服务器", "说明", "命令 / 状态"], mcp_rows)

    plan_open = [t for t in plan["todos"] if not t["done"]]
    plan_body = (
        f'<p class="stage">{plan_text(plan["stage"] or "—")}</p>'
        + '<ul class="plan">'
        + "".join(f'<li class="{"done" if t["done"] else ""}"><span>{plan_text(t["text"])}</span></li>'
                  for t in plan["todos"])
        + "</ul>"
    )

    def section(sid: str, category: str, title: str, count: int, when_dt: datetime | None, body: str) -> str:
        change = f"变更 {rel_html(when_dt)}" if when_dt else "未提交"
        return (
            f'<section id="{sid}" data-category="{category}">'
            f'<h3 class="sec-h"><button type="button" class="sec-head" aria-expanded="true" aria-controls="fold-{sid}" disabled>'
            f'<span class="category-mark" aria-hidden="true"></span><span class="sec-title">{title}</span>'
            f'<span class="sec-count">{count} 项{"待办" if sid == "plan" else ""}</span>'
            f'<span class="sec-meta" title="{fmt_date(when_dt)}">{change}</span>'
            f'<span class="chev" aria-hidden="true"></span></button></h3>'
            f'<div class="fold" id="fold-{sid}">{body}</div></section>'
        )

    sections = [
        ("skills", "skills", "自研技能", len(skills), t_skills, skills_body),
        ("tp-skills", "skills", "第三方技能", tp_count, t_tp, table_html(["名称", "用途"], tp_rows)),
        ("plugins", "plugins", "自研插件", len(plugins), t_plugins, plugins_body),
        ("tp-plugins", "plugins", "第三方插件", len(tpp), t_tpp, tpp_body),
        ("prompts", "prompts", "常用提示词", len(prompts), t_prompts, prompts_body),
        ("core-prompt", "prompts", "核心提示词", int(bool(core_text)), t_core, core_body),
        ("mcp", "mcp", "MCP 服务器模板", len(mcp), t_mcp, mcp_body),
        ("plan", "plan", "当前规划", len(plan_open), t_plan, plan_body),
    ]
    categories = {"skills": "技能", "plugins": "插件", "prompts": "提示词", "mcp": "MCP 服务器"}
    totals = {category: sum(row[3] for row in sections if row[1] == category) for category in categories}
    mix = "".join(
        f'<span data-category="{category}" style="flex-grow:{count}"></span>'
        for category, count in totals.items() if count
    )
    legend = "".join(
        f'<li data-category="{category}"><span>{label}</span><b>{totals[category]}</b></li>'
        for category, label in categories.items()
    )
    toc = "".join(
        f'<a href="#{sid}"{" class=maintenance" if sid == "plan" else ""}>'
        f'{"MCP 模板" if sid == "mcp" else title}</a>'
        for sid, _, title, *_ in sections
    )
    inventory = "".join(section(*item) for item in sections)
    snapshot_time = now.astimezone()
    commit_date = fmt_date(repo_last)
    commit = f'<time datetime="{commit_date}">{commit_date}</time>' if repo_last else commit_date

    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Qi 资产面板</title>
<style>{CSS}</style>
</head><body>
<a class="skip" href="#catalog">跳到资产清单</a>
<div class="shell">
<header class="topbar">
  <div class="brand"><span class="seal">Qi</span><span>个人 AI 工具配置中心</span></div>
  <p class="snapshot">快照生成于 <time datetime="{snapshot_time.isoformat(timespec="minutes")}">{snapshot_time:%Y-%m-%d %H:%M}</time></p>
</header>
<main>
  <div class="hero">
    <div class="hero-main">
      <h1>可视化资产面板</h1>
      <p>汇总 Qi 仓库收录的技能、插件、提示词和连接模板。</p>
      <p class="commit"><span>仓库最近提交</span>{commit} <span>{days_ago(repo_last)}</span></p>
    </div>
    <div class="distribution">
      <div class="distribution-head">
        <h2>仓库资产</h2>
        <div class="asset-total"><strong>{sum(totals.values())}</strong><span>项</span></div>
      </div>
      <div class="mix" aria-hidden="true">{mix}</div>
      <ul class="legend" aria-label="按类型统计">{legend}</ul>
    </div>
  </div>
  <div class="workspace">
    <aside class="directory">
      <h2 id="directory-title">快速跳转</h2>
      <nav class="toc" aria-labelledby="directory-title">{toc}</nav>
    </aside>
    <div class="catalog" id="catalog" tabindex="-1">
      <div class="catalog-head">
        <h2>资产清单</h2>
        <button type="button" class="control" id="toggle-all" hidden>全部展开</button>
      </div>
      <div class="inventory">{inventory}</div>
    </div>
  </div>
</main>
<footer><span>数据来自 Qi 仓库的本地快照</span><span>重新生成 <code>python tools/build-dashboard.py</code></span></footer>
</div>
<div id="copy-status" class="sr-only" role="status"></div>
<script>{JS}</script><script>{COPYJS}</script>
</body></html>"""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):  # Windows 控制台默认 GBK，避免中文乱码
        sys.stdout.reconfigure(encoding="utf-8")
    html = render()
    OUT.write_text(html, encoding="utf-8")
    print(f"已生成 {OUT}（{OUT.stat().st_size / 1024:.1f} KB）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
