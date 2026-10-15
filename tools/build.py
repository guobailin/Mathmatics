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
import re
import sys
from pathlib import Path

import yaml
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
DIST_DIR = ROOT / "dist"

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
        })

    id_set = {k["id"] for k in kps}
    for k in kps:
        for r in k.get("related") or []:
            if r not in id_set:
                errors.append(f"{k['file']}: related 引用了不存在的 id '{r}'")
    return kps, errors, warnings


# ---------- 输出 ----------

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
    return "\n".join(parts)


def answers_to_html(k):
    parts = []
    for ex in k["examples"]:
        parts.append(f'<div class="example"><h3>{k["title"]} · {ex["title"]}</h3>'
                     f'<div class="analysis">{render_md(ex["analysis"])}</div>'
                     f'<div class="answer">答案：{render_md(ex["answer"])}</div></div>')
    return "\n".join(parts)


HEAD = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
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
"""

PRINT_CSS = BASE_CSS + """
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
    out_dir.mkdir(parents=True, exist_ok=True)
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
    return files


def build_web(kps):
    out_dir = DIST_DIR / "web"
    out_dir.mkdir(parents=True, exist_ok=True)
    data = []
    for k in kps:
        data.append({
            "id": k["id"], "title": k["title"], "module": k["module"],
            "moduleSlug": k["moduleSlug"], "grade": k["grade"], "tags": k["tags"],
            "difficulty": k["difficulty"], "skills": k["skills"],
            "html": kp_to_html(k),
            "text": " ".join([k["title"], " ".join(k["tags"] or []),
                              " ".join(k["skills"] or []), k["lecture"],
                              " ".join(ex["problem"] for ex in k["examples"])]),
        })
    app = WEB_APP.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    (out_dir / "index.html").write_text(app, encoding="utf-8")
    return out_dir / "index.html"


def build_miniprogram(kps):
    out_dir = DIST_DIR / "miniprogram"
    out_dir.mkdir(parents=True, exist_ok=True)
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


WEB_APP = HEAD.replace("{title}", "小学数学知识库").replace("{css}", BASE_CSS + """
header{position:sticky;top:0;background:#fff;padding:8px 0;border-bottom:1px solid #eee;z-index:9}
input,select{font-size:1em;padding:6px 10px;border:1px solid #ccc;border-radius:6px;margin-right:8px}
.result{padding:8px 12px;border-bottom:1px solid #eee;cursor:pointer}
.result:hover{background:#f4f8ff}
.result .m{color:#888;font-size:.85em}
.badge{display:inline-block;background:#eef;border-radius:4px;padding:0 6px;font-size:.8em;margin-right:4px}
""") + """
<header>
  <input id="q" placeholder="搜索知识点 / 标签 / 题目关键词…" style="width:46%">
  <select id="mod"><option value="">全部模块</option></select>
  <select id="grade"><option value="">全部年级</option>
    <option>1</option><option>2</option><option>3</option>
    <option>4</option><option>5</option><option>6</option></select>
  <select id="diff"><option value="">全部难度</option>
    <option value="1">★ 基础</option><option value="2">★★ 提高</option><option value="3">★★★ 竞赛</option></select>
</header>
<div id="results"></div>
<div id="detail"></div>
<script>
const DATA = __DATA__;
const $ = s => document.querySelector(s);
const mods = [...new Set(DATA.map(d => d.module))];
mods.forEach(m => { const o = document.createElement("option"); o.text = m; $("#mod").add(o); });
function esc(s){return s.replace(/[&<>]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));}
function search(){
  const q = $("#q").value.trim(), mod = $("#mod").value,
        g = $("#grade").value, df = $("#diff").value;
  $("#detail").innerHTML = "";
  let hits = DATA.filter(d =>
    (!mod || d.module === mod) &&
    (!g || d.grade.includes(+g)) &&
    (!df || d.difficulty === +df) &&
    (!q || d.text.includes(q)));
  $("#results").innerHTML = hits.map(d =>
    `<div class="result" onclick="show('${d.id}')">
       <b>${esc(d.title)}</b> <span class="m">${esc(d.module)} · ${"★".repeat(d.difficulty)} · 年级 ${d.grade.join("/")}</span><br>
       ${d.tags.map(t=>`<span class="badge">${esc(t)}</span>`).join("")}
     </div>`).join("") || "<p style='padding:16px'>没有匹配的知识点</p>";
}
function show(id){
  const d = DATA.find(x => x.id === id);
  $("#detail").innerHTML = `<h1>${esc(d.title)}</h1>
    <p class="meta"><span>${esc(d.module)}</span><span>难度 ${"★".repeat(d.difficulty)}</span>
    <span>子技能：${d.skills.map(esc).join("、")}</span></p>` + d.html;
  if (window.renderMathInElement) renderMathInElement($("#detail"),
    {delimiters:[{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false}]});
  window.scrollTo(0, 0);
}
["q","mod","grade","diff"].forEach(id => $("#"+id).addEventListener("input", search));
search();
</script></body></html>
"""


def sync_miniprogram_data():
    """把 dist/miniprogram/*.json 同步进小程序源码目录 miniprogram/data/。"""
    src = DIST_DIR / "miniprogram"
    dst = ROOT / "miniprogram" / "data"
    dst.mkdir(parents=True, exist_ok=True)
    import shutil
    for f in src.glob("*.json"):
        shutil.copy2(f, dst / f.name)
    return len(list(dst.glob("*.json")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只校验不构建")
    args = ap.parse_args()

    kps, errors, warnings = load_knowledge_points()
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

    DIST_DIR.mkdir(exist_ok=True)
    build_index(kps)
    prints = build_print(kps)
    web = build_web(kps)
    manifest = build_miniprogram(kps)
    n = sync_miniprogram_data()
    print(f"📄 打印页 {len(prints)} 个 → dist/print/")
    print(f"🌐 网页版 → {web.relative_to(ROOT)}")
    print(f"📱 小程序数据包 {len(manifest)} 个 → dist/miniprogram/，已同步到 miniprogram/data/")


if __name__ == "__main__":
    main()
