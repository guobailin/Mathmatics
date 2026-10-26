#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成竞赛真题页面：首页入口 + 真题总览 + 每套解答页。"""
import json
from collections import Counter
from html import escape
from pathlib import Path

from markdown_it import MarkdownIt

PAPERS = [
    ("2024年秋季走美六年级-学生版", "2024 秋·走美", "2024a-zoumei"),
    ("2025年春季走美六年级-学生版", "2025 春·走美", "2025s-zoumei"),
    ("2025年秋季走美六年级-学生版", "2025 秋·走美", "2025a-zoumei"),
    ("2026年春季走美六年级-学生版", "2026 春·走美", "2026s-zoumei"),
    ("第28届WMO六年级试卷", "第 28 届 WMO", "wmo-28"),
    ("第30届WMO六年级试卷", "第 30 届 WMO", "wmo-30"),
    ("第32届WMO六年级试卷", "第 32 届 WMO", "wmo-32"),
    ("第34届WMO六年级试卷", "第 34 届 WMO", "wmo-34"),
    ("2022-2023年思维能力全国总测评六年级试题", "2022-23 全国总测评", "2022-2023-quanguo"),
    ("2024 IHC 6培训题-学生版", "2024 IHC 6 培训", "ihc-2024-training"),
    ("2024 IHC A-6发布版", "2024 IHC A-6", "ihc-2024-a"),
    ("2024 IHC C-6发布版", "2024 IHC C-6", "ihc-2024-c"),
    ("2024 IHC D-6发布版", "2024 IHC D-6", "ihc-2024-d"),
    ("2024年1月世少赛思维能力地区六年级试题", "2024.1 世少赛", "shishaosai-2024-01"),
    ("2025 IHC J-6发布版", "2025 IHC J-6", "ihc-2025-j"),
    ("2025年奥林匹克思维能力测评活动六年级试题", "2025 思维能力测评", "shishaosai-2025"),
    ("2026 IHC S-6发布版", "2026 IHC S-6", "ihc-2026-s"),
    ("六年级奥林匹克思维能力测评考前60题", "考前 60 题", "kaoqian-60"),
]

EXAM_MD = MarkdownIt("commonmark", {"html": True, "breaks": True}).enable("table")

EXAM_CSS = r"""
body{max-width:920px;margin:0 auto;padding:26px 22px 64px;background:#fffdf8;
font-family:-apple-system,"PingFang SC","Source Han Serif SC",serif;line-height:1.85;color:#222}
.exam-nav{display:flex;align-items:center;justify-content:space-between;gap:12px;
flex-wrap:wrap;font-size:12px;color:#5f6a64;margin-bottom:22px}
.exam-nav a{color:#2f6f6b;text-decoration:none;font-weight:600}
.exam-nav a:hover{text-decoration:underline}
.exam-kicker{font-size:10.5px;letter-spacing:.16em;color:#2f6f6b;font-weight:700;margin-bottom:4px}
.exam-body h1{font-size:25px;line-height:1.3;margin:0 0 18px;padding-bottom:12px;border-bottom:2px solid #2f6f6b}
.exam-body h2{font-size:19px;margin:30px 0 12px;color:#1f2a26}
.exam-body h3{font-size:15px;margin:24px 0 8px;color:#2f6f6b}
.exam-body table{width:100%;border-collapse:collapse;margin:14px 0;font-size:12.5px}
.exam-body th,.exam-body td{border:1px solid #ddd6c8;padding:6px 8px;text-align:left;vertical-align:top}
.exam-body th{background:#f4efe3;font-weight:700}
.exam-body blockquote{margin:14px 0;padding:8px 14px;border-left:3px solid #2f6f6b;background:#f7f4ec;color:#4d5651}
.exam-body code{background:#f1ece1;padding:1px 5px;border-radius:4px;font-size:.9em}
.exam-body img{max-width:100%;height:auto;display:block;margin:16px auto}
.exam-body hr{border:0;border-top:1px solid #e4ddcf;margin:22px 0}
.exam-foot{margin-top:40px;padding-top:16px;border-top:1px solid #e4ddcf;font-size:12px;color:#8a928d}
.exam-index-head{max-width:920px;margin:0 auto 20px}
.exam-index-head h1{font-size:28px;margin:0 0 8px}
.exam-index-head p{margin:0;color:#5f6a64;font-size:13px}
.exam-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:18px 0 28px}
.exam-grid a{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:12px 13px;
border:1px solid #ddd6c8;border-radius:12px;background:#fffdf8;color:#1f2a26;text-decoration:none}
.exam-grid a:hover{border-color:#2f6f6b}
.exam-grid b{font-size:12px}.exam-grid span{font-size:10px;color:#5f6a64;white-space:nowrap}
.exam-table{width:100%;border-collapse:collapse;font-size:12.5px}
.exam-table th,.exam-table td{border:1px solid #ddd6c8;padding:6px 8px;text-align:left}
.exam-table th{background:#f4efe3}
@media(max-width:720px){.exam-grid{grid-template-columns:repeat(2,minmax(0,1fr))}body{padding:18px 15px 50px}}
@media print{.exam-nav,.exam-foot{display:none}body{max-width:none;padding:0}.exam-grid{display:none}}
"""


def counts(answers_dir: Path):
    out = {}
    for name, short, slug in PAPERS:
        total = 0
        js = answers_dir / f"{name}.json"
        if js.exists():
            try:
                total = int(json.loads(js.read_text(encoding="utf-8")).get("total", 0))
            except Exception:
                total = 0
        out[name] = total
    return out


def exam_home_html(answers_dir: Path) -> str:
    c = counts(answers_dir)
    cards = "\n".join(
        f'<a class="exam-home-card" href="exam/{slug}.html"><b>{escape(short)}</b>'
        f'<span>{c[name]} 题</span></a>'
        for name, short, slug in PAPERS
    )
    total = sum(c.values())
    return f'''<section class="exam-home" id="examHome">
  <div class="exam-home-head">
    <div>
      <p class="eyebrow">竞赛真题</p>
      <h2>{len(PAPERS)} 套六年级竞赛真题，共 {total} 题</h2>
      <p>逐题录入 + 详细解答 + 知识点索引，答案已与卷末官方答案页核对。</p>
    </div>
    <a class="exam-home-more" href="exam/index.html">全部真题 →</a>
  </div>
  <div class="exam-home-grid">
    {cards}
  </div>
</section>'''


def exam_head(title: str, head_template: str, base_css: str) -> str:
    h = head_template.format(title=escape(title), css=base_css + EXAM_CSS)
    return (h.replace('href="katex/', 'href="../katex/')
             .replace('src="katex/', 'src="../katex/'))


def build(web_dir: Path, answers_dir: Path, head_template: str, base_css: str) -> int:
    if not answers_dir.exists():
        return 0
    out_dir = web_dir / "exam"
    out_dir.mkdir(parents=True, exist_ok=True)
    c = counts(answers_dir)
    total = sum(c.values())
    nav = ('<div class="exam-nav"><a href="../index.html">← 知识地图</a>'
           '<span><a href="index.html">全部真题</a></span></div>')

    for name, short, slug in PAPERS:
        md_path = answers_dir / f"{name}.md"
        if not md_path.exists():
            continue
        body = EXAM_MD.render(md_path.read_text(encoding="utf-8"))
        body = body.replace('src="/assets/', 'src="../assets/')
        page = (exam_head(f"{short} · 真题解答", head_template, base_css) + nav +
                f'<div class="exam-kicker">竞赛真题 · 六年级 · {c[name]} 题</div>' +
                f'<article class="exam-body">{body}</article>' +
                '<div class="exam-foot"><a href="../index.html">← 返回知识地图</a> · '
                '<a href="index.html">全部真题</a></div></body></html>')
        (out_dir / f"{slug}.html").write_text(page, encoding="utf-8")

    cards = "\n".join(
        f'<a href="{slug}.html"><b>{escape(short)}</b><span>{c[name]} 题 →</span></a>'
        for name, short, slug in PAPERS
    )
    kcount = Counter()
    for name, short, slug in PAPERS:
        js = answers_dir / f"{name}.json"
        if not js.exists():
            continue
        d = json.loads(js.read_text(encoding="utf-8"))
        for it in d.get("items", []):
            for tag in set(it.get("knowledge", [])):
                kcount[tag] += 1
    rows = "\n".join(f"<tr><td>{escape(tag)}</td><td>{n}</td></tr>"
                     for tag, n in kcount.most_common(15))
    index_page = (exam_head("六年级竞赛真题", head_template, base_css) +
                  '<div class="exam-nav"><a href="../index.html">← 知识地图</a></div>'
                  '<div class="exam-index-head"><p class="exam-kicker">竞赛真题</p>'
                  f'<h1>六年级竞赛真题</h1><p>{len(PAPERS)} 套走美 / WMO / IHC / 世少赛真题，共 {total} 题；'
                  '逐题录入、详细解答，按知识点写回知识地图。</p></div>'
                  f'<div class="exam-grid">{cards}</div>'
                  '<h2>高频知识点</h2>'
                  '<table class="exam-table"><thead><tr><th>知识点</th><th>题数</th></tr></thead>'
                  f'<tbody>{rows}</tbody></table>'
                  '<div class="exam-foot">题目与答案均来自对应试卷；答案已与卷末官方答案页核对。</div>'
                  '</body></html>')
    (out_dir / "index.html").write_text(index_page, encoding="utf-8")
    return len(PAPERS)
