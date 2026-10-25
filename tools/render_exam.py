#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 exam/*.pdf 渲染成逐页 PNG + 文本，供内容录入使用。

输出（已 gitignore，不提交）：
  exam/_rendered/<试卷名>/page-01.png ...
  exam/_rendered/<试卷名>/text.txt
"""
import subprocess
import tempfile
from pathlib import Path
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parent.parent
EXAM = ROOT / "exam"
OUT = EXAM / "_rendered"

def main():
    OUT.mkdir(exist_ok=True)
    for pdf in sorted(EXAM.glob("*.pdf")):
        dst = OUT / pdf.stem
        dst.mkdir(parents=True, exist_ok=True)
        reader = PdfReader(str(pdf))
        texts = []
        for i, page in enumerate(reader.pages, 1):
            texts.append(f"===== 第 {i} 页 =====\n" + (page.extract_text() or ""))
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp_path = Path(tmp.name)
            writer = PdfWriter()
            writer.add_page(page)
            with open(tmp_path, "wb") as f:
                writer.write(f)
            png = dst / f"page-{i:02d}.png"
            r = subprocess.run(["sips", "-s", "format", "png", "-Z", "1800",
                                str(tmp_path), "--out", str(png)],
                               capture_output=True, text=True)
            if r.returncode != 0:
                print("sips failed", pdf.name, i, r.stderr[-200:])
            tmp_path.unlink(missing_ok=True)
        (dst / "text.txt").write_text("\n\n".join(texts), encoding="utf-8")
        print(f"{pdf.name}: {len(reader.pages)} pages -> {dst}")

if __name__ == "__main__":
    main()
