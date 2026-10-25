# 六年级竞赛真题（走美 / WMO）

本目录收录 8 套六年级竞赛真题的学生版 PDF，以及逐题录入与解答。所有答案均已与卷末官方答案页核对；部分图形题在解析中注明了读图口径。

## 快速入口

- [真题考察总结（高频知识点 / 难度 / 思路）](SUMMARY.md)
- 逐题解答：见 `exam/answers/` 下与试卷同名的 `.md` / `.json`

## 试卷与解答

| 试卷 | 题量 | 解答 |
|---|---:|---|
| 2024 年秋季走美六年级 | 12 | [解答](answers/2024年秋季走美六年级-学生版.md) |
| 2025 年春季走美六年级 | 15 | [解答](answers/2025年春季走美六年级-学生版.md) |
| 2025 年秋季走美六年级 | 15 | [解答](answers/2025年秋季走美六年级-学生版.md) |
| 2026 年春季走美六年级 | 15 | [解答](answers/2026年春季走美六年级-学生版.md) |
| 第 28 届 WMO 六年级 | 20 | [解答](answers/第28届WMO六年级试卷.md) |
| 第 30 届 WMO 六年级 | 20 | [解答](answers/第30届WMO六年级试卷.md) |
| 第 32 届 WMO 六年级 | 20 | [解答](answers/第32届WMO六年级试卷.md) |
| 第 34 届 WMO 六年级 | 20 | [解答](answers/第34届WMO六年级试卷.md) |

合计 **137 题**。

## 目录说明

- `*.pdf`：原始试卷（学生版），部分卷末附官方答案。
- `answers/`：逐题 Markdown 解答 + 机器可读 JSON（题号、知识点、方法、难度、答案）。
- `answers/_review-*.md`：交叉复核记录（如有）。
- `_rendered/`：逐页 PNG 与文本层缓存，由 `tools/render_exam.py` 生成，已 gitignore。

## 重新生成

```bash
python3 tools/render_exam.py       # PDF → 逐页 PNG + text.txt
python3 tools/build_exam_index.py  # 生成 SUMMARY.md，并把真题索引写回 content/
```
