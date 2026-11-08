# 12 × 18 cm 可打印知识卡

三张竖版知识卡，成品尺寸 **12 cm × 18 cm**（120 mm × 180 mm），用于打印后随身携带 / 贴墙复习。内容为初中几何与计数专题的三条高频结论：

| # | 卡片 | 核心内容 |
|---|---|---|
| 1 | 中线定理（阿波罗尼斯定理） | $b^2+c^2=2\left(m_a^2+\left(\frac a2\right)^2\right)$、等价写法、余弦定理推导、求中线例题 |
| 2 | 重心的性质与中线 | 三中线交于 $G$、$AG:GM=2:1$、$AG=\frac23m_a$、$GM=\frac13m_a$、6 等面积、重心坐标 |
| 3 | 圆排列公式 | 基础圆排列 $(n-1)!$、间隔受限公式 $\frac nk\times C_{n-k(d-1)-1}^{k-1}$、环形间隔推导、12 点选 3 点 = 40 |

## 文件

- `geometry-median-centroid-and-circular-permutation-12x18.html` — 打印源文件（3 页，每页一张 120 mm × 180 mm 卡片；含屏幕专用打印提示条，打印时自动隐藏）
- `geometry-median-centroid-and-circular-permutation-12x18.pdf` — 已排好版的打印版（3 页，页面尺寸 120 mm × 180 mm，推荐直接打印）
- `preview-1-median-theorem.png`、`preview-2-centroid.png`、`preview-3-circular-permutation.png` — 屏幕预览图

## 打印设置

1. 纸张：**A4**（或 12 × 18 cm 卡纸）
2. 缩放：**实际大小 / 100%**，不要选「适合页面」（否则卡片会被放大/缩小）
3. 边距：**无**；取消「页眉和页脚」
4. 单面打印 = 3 张卡；双面打印（沿长边翻转）= 2 张纸，第 1、2 页为同一张的正反面，第 3 页背面留白
5. 用 A4 纸打印时卡片会居中印在纸中间，沿卡片边框裁下即可（卡片本身即 12 × 18 cm，正文四周留有 ≥ 7 mm 安全边）

## 重新生成

- 改文案：直接编辑 HTML；卡片正文在 `.card` > `.body` 内，页面尺寸由 CSS `@page { size: 120mm 180mm }` 控制。
- 重新出 PDF（Chrome headless，需本机装 Chrome）：

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --no-sandbox \
  --no-pdf-header-footer --virtual-time-budget=8000 \
  --print-to-pdf=delivery/cards/geometry-median-centroid-and-circular-permutation-12x18.pdf \
  "file://$PWD/delivery/cards/geometry-median-centroid-and-circular-permutation-12x18.html"
```

- 预览图：用浏览器打开 HTML 后按 120 mm 宽截图，或把 PDF 逐页转 PNG。

## 校验

生成 PDF 后确认 3 页、页面尺寸 120 mm × 180 mm、且不含打印提示条：

```bash
python3 - <<'PY'
from pypdf import PdfReader
r = PdfReader('delivery/cards/geometry-median-centroid-and-circular-permutation-12x18.pdf')
print('pages:', len(r.pages))
for pg in r.pages:
    print(round(float(pg.mediabox.width)*25.4/72, 1), 'x', round(float(pg.mediabox.height)*25.4/72, 1), 'mm')
print('hint leaked:', '打印提示' in ''.join((p.extract_text() or '') for p in r.pages))
PY
```
