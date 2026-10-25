#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小学数学知识库构建工具

用法：
    python3 tools/build.py            # 校验 + 全量构建
    python3 tools/build.py --check    # 只校验，不产出

输入：content/<序号>-<模块>/<知识点>.md（Markdown + YAML frontmatter）
产出：
    dist/index.json              检索索引
    dist/print/<模块>.html       可打印 HTML（答案集中于页末，Cmd+P 出 PDF）
    dist/web/index.html          单页应用：浏览 + 搜索 + 筛选 + 打印入口
    dist/miniprogram/*.json      小程序数据包（按模块拆分）
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml
from markdown_it import MarkdownIt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from web_index import WEB_INDEX_BODY, WEB_INDEX_CSS  # noqa: E402
from exam_pages import build as build_exam_pages, exam_home_html  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
DIST_DIR = ROOT / "dist"
CURRICULUM_FILE = CONTENT_DIR / "curriculum.yaml"
ASSETS_DIR = ROOT / "assets"
ANSWERS_DIR = ROOT / "exam" / "answers"
KATEX_SRC = ROOT / "assets" / "katex"  # 本地化 KaTeX 运行时（含字体），构建时拷入各输出目录

REQUIRED_FIELDS = ["id", "title", "module", "grade", "tags", "difficulty", "skills", "related"]
EXAMPLE_RE = re.compile(r"^###\s*例\d+[^\n]*$", re.M)
FIELD_RE = re.compile(r"\*\*(题目|覆盖点|解析|答案)\*\*[:：]")

md = MarkdownIt("commonmark", {"html": True, "breaks": True})


def slug(module_dir: str) -> str:
    """目录名 08-奥数-数论 -> m08"""
    m = re.match(r"(\d+)-", module_dir)
    return f"m{m.group(1)}" if m else module_dir


def parse_examples(text: str):
    """把 '## 例题' 之后的部分解析为例题列表。"""
    parts = EXAMPLE_RE.split(text)
    titles = EXAMPLE_RE.findall(text)
    examples = []
    for title, body in zip(titles, parts[1:]):
        segs = FIELD_RE.split(body)
        fields = {}
        # FIELD_RE.split 产出 [前导, 字段名, 内容, 字段名, 内容, ...]
        for i in range(1, len(segs) - 1, 2):
            fields[segs[i]] = segs[i + 1].strip()
        covers = [s.strip() for s in re.split(r"[,，、]", fields.get("覆盖点", "")) if s.strip()]
        examples.append({
            "title": title.lstrip("#").strip(),
            "problem": fields.get("题目", ""),
            "covers": covers,
            "analysis": fields.get("解析", ""),
            "answer": fields.get("答案", ""),
        })
    return examples



def file_updated(rel_path: str) -> str:
    """取知识点文件最后一次 git 提交日期；无 git 时退回文件 mtime。"""
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%cs", "--", rel_path],
            cwd=ROOT, stderr=subprocess.DEVNULL)
        value = out.decode().strip()
        if value:
            return value
    except Exception:
        pass
    try:
        return datetime.fromtimestamp((ROOT / rel_path).stat().st_mtime).strftime("%Y-%m-%d")
    except Exception:
        return ""


def load_knowledge_points():
    """加载并校验全部知识点，返回 (kps, errors, warnings)。"""
    kps, errors, warnings = [], [], []
    seen_ids = {}
    for md_file in sorted(CONTENT_DIR.glob("*/*.md")):
        module_dir = md_file.parent.name
        module_name = re.sub(r"^\d+-", "", module_dir)
        rel = md_file.relative_to(ROOT)
        raw = md_file.read_text(encoding="utf-8")

        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        if not m:
            errors.append(f"{rel}: 缺少 YAML frontmatter（--- 包裹的元数据头）")
            continue
        try:
            meta = yaml.safe_load(m.group(1))
        except yaml.YAMLError as e:
            errors.append(f"{rel}: YAML 解析失败：{e}")
            continue
        body = m.group(2)

        for f in REQUIRED_FIELDS:
            if f not in meta or meta[f] is None:
                errors.append(f"{rel}: 缺少必填字段 {f}")

        kid = meta.get("id", "?")
        if kid in seen_ids:
            errors.append(f"{rel}: id '{kid}' 与 {seen_ids[kid]} 重复")
        seen_ids[kid] = str(rel)

        if meta.get("module") != module_name:
            errors.append(f"{rel}: module '{meta.get('module')}' 与目录 '{module_name}' 不一致")

        if "## 讲解" not in body or "## 例题" not in body:
            errors.append(f"{rel}: 缺少 '## 讲解' 或 '## 例题' 小节")
            continue

        lecture = body.split("## 例题")[0].split("## 讲解", 1)[1].strip()
        examples = parse_examples(body.split("## 例题", 1)[1])
        if not examples:
            errors.append(f"{rel}: 没有例题（### 例N 标题）")

        skills = meta.get("skills") or []
        covered = set()
        for ex in examples:
            if not ex["problem"]:
                errors.append(f"{rel} {ex['title']}: 缺少 **题目**")
            if not ex["answer"]:
                errors.append(f"{rel} {ex['title']}: 缺少 **答案**")
            for c in ex["covers"]:
                if c not in skills:
                    errors.append(f"{rel} {ex['title']}: 覆盖点 '{c}' 不在 skills 清单中")
                covered.add(c)
        for s in skills:
            if s not in covered:
                errors.append(f"{rel}: 子技能 '{s}' 没有任何例题覆盖")
        # 冗余提示：只在与另一道例题覆盖点完全相同、且无独有覆盖点时提醒，
        # 不干扰正常的"同一子技能按难度阶梯出多题"
        for ex in examples:
            dup = any(set(ex["covers"]) == set(other["covers"])
                      for other in examples if other is not ex)
            unique = any(c not in [c2 for other in examples if other is not ex
                                   for c2 in other["covers"]]
                         for c in ex["covers"])
            if ex["covers"] and dup and not unique:
                warnings.append(f"{rel} {ex['title']}: 覆盖点与其他例题完全重复，确认是否冗余")

        kps.append({
            **{f: meta.get(f) for f in REQUIRED_FIELDS},
            "moduleDir": module_dir,
            "moduleSlug": slug(module_dir),
            "file": str(rel),
            "lecture": lecture,
            "examples": examples,
            "updated": file_updated(str(rel)),
        })

    id_set = {k["id"] for k in kps}
    for k in kps:
        for r in k.get("related") or []:
            if r not in id_set:
                errors.append(f"{k['file']}: related 引用了不存在的 id '{r}'")
    return kps, errors, warnings


def load_curriculum(kps):
    """加载 content/curriculum.yaml，校验每个知识点都挂入年级/模块。"""
    errors = []
    if not CURRICULUM_FILE.exists():
        return None, [f"{CURRICULUM_FILE.relative_to(ROOT)}: 缺少课程大纲文件"]
    try:
        raw = yaml.safe_load(CURRICULUM_FILE.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        return None, [f"{CURRICULUM_FILE.relative_to(ROOT)}: YAML 解析失败：{e}"]
    boards = raw.get("boards")
    if not isinstance(boards, list) or not boards:
        return None, [f"{CURRICULUM_FILE.relative_to(ROOT)}: boards 为空或格式错误"]

    content = {k["id"]: k for k in kps}
    seen = {}
    keys = set()
    out = []
    for bi, board in enumerate(boards, 1):
        key = board.get("key")
        if not key:
            errors.append(f"curriculum: 第 {bi} 个板块缺少 key")
            continue
        if key in keys:
            errors.append(f"curriculum: board key '{key}' 重复")
        keys.add(key)
        label = board.get("label") or key
        domains = board.get("domains")
        if not isinstance(domains, list) or not domains:
            errors.append(f"curriculum: {label} 缺少 domains")
            continue
        domains_out = []
        bc = bo = 0
        for domain in domains:
            dname = (domain.get("name") or "").strip()
            if not dname:
                errors.append(f"curriculum: {label} 下存在空领域名")
                continue
            topics_out = []
            for topic in domain.get("topics") or []:
                cid = topic.get("content")
                title = (topic.get("title") or "").strip()
                if cid:
                    if cid not in content:
                        errors.append(f"curriculum: {label}/{dname}: content '{cid}' 不存在")
                        continue
                    if cid in seen:
                        errors.append(
                            f"curriculum: content '{cid}' 重复挂载（{seen[cid]} 与 {label}/{dname}）")
                    seen[cid] = f"{label}/{dname}"
                    title = content[cid]["title"]
                if not title:
                    errors.append(f"curriculum: {label}/{dname}: 存在空标题")
                    continue
                topics_out.append({"title": title, "content": cid, "term": topic.get("term")})
                bc += 1
                bo += 1 if cid else 0
            if topics_out:
                domains_out.append({"name": dname, "topics": topics_out})
        out.append({
            "key": key, "label": label,
            "short": board.get("short") or label[:1],
            "kind": board.get("kind") or "grade",
            "color": board.get("color") or "#2F6F6B",
            "intro": board.get("intro") or "",
            "count": bc, "online": bo, "domains": domains_out,
        })

    for kid, kp in content.items():
        if kid not in seen:
            errors.append(f"curriculum: 知识点 '{kid}'（{kp['title']}）未挂入任何年级/模块")
    return out, errors


# ---------- 输出 ----------

def copy_katex(dst_dir: Path):
    """把 assets/katex 拷入输出目录，公式渲染完全本地化（不依赖外网 CDN）。"""
    shutil.copytree(KATEX_SRC, dst_dir / "katex", dirs_exist_ok=True)


def copy_figures(dst_dir: Path):
    """把 assets/geometry 拷入输出目录，几何示意图用相对路径 assets/geometry/... 引用。"""
    src = ASSETS_DIR / "geometry"
    if src.exists():
        shutil.copytree(src, dst_dir / "assets" / "geometry", dirs_exist_ok=True)


def fix_asset_urls(html: str) -> str:
    """内容里的 /assets/... 改为相对路径，网页/打印/Pages 子路径都能用。"""
    return html.replace('src="/assets/', 'src="assets/')


def render_md(text: str) -> str:
    return md.render(text)


def kp_to_html(k, for_print=False):
    parts = [render_md(k["lecture"])]
    parts.append('<h2 class="ex-h">例题</h2>')
    for ex in k["examples"]:
        covers = "、".join(ex["covers"])
        parts.append(f'<div class="example"><h3>{ex["title"]}'
                     f'<span class="covers">覆盖点：{covers}</span></h3>'
                     f'<div class="problem">{render_md(ex["problem"])}</div>')
        if for_print:
            parts.append(f'<div class="answer-ref">（解析与答案见页末答案区）</div>')
        else:
            parts.append(f'<details><summary>查看解析与答案</summary>'
                         f'<div class="analysis">{render_md(ex["analysis"])}</div>'
                         f'<div class="answer">答案：{render_md(ex["answer"])}</div></details>')
        parts.append('</div>')
    return fix_asset_urls("\n".join(parts))


def answers_to_html(k):
    parts = []
    for ex in k["examples"]:
        parts.append(f'<div class="example"><h3>{k["title"]} · {ex["title"]}</h3>'
                     f'<div class="analysis">{render_md(ex["analysis"])}</div>'
                     f'<div class="answer">答案：{render_md(ex["answer"])}</div></div>')
    return fix_asset_urls("\n".join(parts))


HEAD = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="katex/katex.min.css">
<script defer src="katex/katex.min.js"></script>
<script defer src="katex/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}}]}})"></script>
<style>{css}</style></head><body>"""

BASE_CSS = """
body{font-family:-apple-system,"PingFang SC","Source Han Serif SC",serif;
max-width:760px;margin:0 auto;padding:24px;line-height:1.8;color:#222}
h1{border-bottom:2px solid #333;padding-bottom:8px}
h2{margin-top:1.6em}h3{font-size:1.05em}
.meta{color:#666;font-size:.9em;margin-bottom:1em}
.meta span{margin-right:1em}
.example{border:1px solid #ddd;border-radius:8px;padding:12px 16px;margin:14px 0}
.example h3{margin:.2em 0 .6em}
.covers{font-size:.75em;color:#888;font-weight:normal;margin-left:1em}
.problem{background:#f7f7f9;border-radius:6px;padding:8px 12px}
details{margin-top:.6em}summary{cursor:pointer;color:#36c}
.answer{color:#b30;font-weight:bold}
img{max-width:100%;height:auto}
"""

PRINT_CSS = BASE_CSS + """
.kp img{display:block;margin:14px auto}
.answer-ref{color:#999;font-size:.85em}
@page{size:A4;margin:2cm}
@media print{
  .kp{page-break-before:always}.kp:first-of-type{page-break-before:auto}
  .answers{page-break-before:always}
  body{max-width:none}
}
"""


def build_index(kps):
    idx = []
    for k in kps:
        text = " ".join([
            k["title"], k["module"], " ".join(k["tags"] or []),
            " ".join(k["skills"] or []),
            k["lecture"],
            " ".join(ex["problem"] for ex in k["examples"]),
        ])
        idx.append({
            "id": k["id"], "title": k["title"], "module": k["module"],
            "moduleSlug": k["moduleSlug"], "grade": k["grade"],
            "tags": k["tags"], "difficulty": k["difficulty"],
            "skills": k["skills"], "text": text,
        })
    out = DIST_DIR / "index.json"
    out.write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8")
    return idx


def build_print(kps):
    out_dir = DIST_DIR / "print"
    os.makedirs(out_dir, exist_ok=True)
    by_module = {}
    for k in kps:
        by_module.setdefault(k["moduleDir"], []).append(k)
    files = []
    for module_dir, items in sorted(by_module.items()):
        module_name = items[0]["module"]
        body = [f"<h1>{module_name}</h1>", '<p class="meta">小学数学知识库 · 打印版</p>']
        for k in items:
            body.append(f'<section class="kp"><h2>{k["title"]}</h2>'
                        f'<p class="meta"><span>年级：{"、".join(map(str, k["grade"]))}</span>'
                        f'<span>难度：{"★" * k["difficulty"]}</span></p>'
                        + kp_to_html(k, for_print=True) + "</section>")
        body.append('<section class="answers"><h1>答案与解析</h1>')
        for k in items:
            body.append(answers_to_html(k))
        body.append("</section>")
        html = HEAD.format(title=f"{module_name} · 打印版", css=PRINT_CSS) + "\n".join(body) + "</body></html>"
        p = out_dir / f"{slug(module_dir)}.html"
        p.write_text(html, encoding="utf-8")
        files.append(p)
    copy_katex(out_dir)
    copy_figures(out_dir)
    return files


def build_web(kps, boards):
    out_dir = DIST_DIR / "web"
    os.makedirs(out_dir, exist_ok=True)
    data = []
    for k in kps:
        data.append({
            "id": k["id"], "title": k["title"], "module": k["module"],
            "moduleSlug": k["moduleSlug"], "grade": k["grade"], "tags": k["tags"],
            "difficulty": k["difficulty"], "skills": k["skills"],
            "updated": k.get("updated", ""),
            "html": kp_to_html(k),
            "text": " ".join([k["title"], " ".join(k["tags"] or []),
                              " ".join(k["skills"] or []), k["lecture"],
                              " ".join(ex["problem"] for ex in k["examples"])]),
        })
    total = sum(b["count"] for b in boards)
    online = sum(b["online"] for b in boards)
    outline = {"boards": boards,
               "stats": {"total": total, "online": online,
                         "stubs": total - online, "boards": len(boards)}}
    app = WEB_APP.replace("__OUTLINE__", json.dumps(outline, ensure_ascii=False))
    app = app.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    app = app.replace("__EXAM_HOME__", exam_home_html(ANSWERS_DIR))
    (out_dir / "index.html").write_text(app, encoding="utf-8")
    copy_katex(out_dir)
    copy_figures(out_dir)
    return out_dir / "index.html"


def build_miniprogram(kps):
    out_dir = DIST_DIR / "miniprogram"
    os.makedirs(out_dir, exist_ok=True)
    by_module = {}
    for k in kps:
        by_module.setdefault(k["moduleSlug"], []).append({
            "id": k["id"], "title": k["title"], "module": k["module"],
            "grade": k["grade"], "tags": k["tags"], "difficulty": k["difficulty"],
            "skills": k["skills"], "related": k["related"],
            "lecture": k["lecture"],
            "examples": k["examples"],
        })
    manifest = []
    for s, items in sorted(by_module.items()):
        p = out_dir / f"{s}.json"
        p.write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
        manifest.append({"slug": s, "module": items[0]["module"], "count": len(items),
                         "file": f"{s}.json"})
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    return manifest


WEB_APP = HEAD.format(title="小学数学知识地图", css=BASE_CSS + WEB_INDEX_CSS) + WEB_INDEX_BODY


def sync_miniprogram_data():
    """把 dist/miniprogram/*.json 同步进小程序源码目录 miniprogram/data/。"""
    src = DIST_DIR / "miniprogram"
    dst = ROOT / "miniprogram" / "data"
    os.makedirs(dst, exist_ok=True)
    for f in src.glob("*.json"):
        shutil.copy2(f, dst / f.name)
    return len(list(dst.glob("*.json")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只校验不构建")
    args = ap.parse_args()

    kps, errors, warnings = load_knowledge_points()
    boards, curriculum_errors = load_curriculum(kps)
    errors += curriculum_errors
    for w in warnings:
        print(f"⚠️  {w}")
    if errors:
        print(f"❌ 校验失败，共 {len(errors)} 处：")
        for e in errors:
            print(f"   {e}")
        sys.exit(1)
    print(f"✅ 校验通过：{len(kps)} 个知识点，{sum(len(k['examples']) for k in kps)} 道例题")
    if args.check:
        return

    os.makedirs(DIST_DIR, exist_ok=True)
    build_index(kps)
    prints = build_print(kps)
    web = build_web(kps, boards)
    exam_count = build_exam_pages(DIST_DIR / "web", ANSWERS_DIR, HEAD, BASE_CSS)
    manifest = build_miniprogram(kps)
    n = sync_miniprogram_data()
    print(f"📄 打印页 {len(prints)} 个 → dist/print/")
    print(f"🌐 网页版 → {web.relative_to(ROOT)}（真题 {exam_count} 套）")
    print(f"📱 小程序数据包 {len(manifest)} 个 → dist/miniprogram/，已同步到 miniprogram/data/")


if __name__ == "__main__":
    main()
