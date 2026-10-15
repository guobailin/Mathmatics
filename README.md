# Mathmatics

小学数学知识库（课内 1–6 年级 + 小学奥数）：按知识点组织，支持查询、打印、微信小程序访问，可持续增补。

## 目录

- `DESIGN.md` — 总体设计方案
- `content/` — 唯一数据源：知识点 Markdown（YAML 元数据 + 讲解 + 例题）
- `templates/` — 新知识点模板
- `tools/build.py` — 构建工具：校验覆盖矩阵 → 索引 → 打印页 → 网页版 → 小程序数据
- `dist/` — 构建产物（打印 HTML、网页版、小程序数据包）
- `miniprogram/` — 微信小程序源码（数据在 `miniprogram/data/`，由构建自动同步）
- `参考讲义/` — 原始讲义素材

## 使用

```bash
python3 tools/build.py          # 校验 + 全量构建
python3 tools/build.py --check  # 只校验
```

- 查询/浏览：打开 `dist/web/index.html`
- 打印：打开 `dist/print/<模块>.html`，浏览器 Cmd+P 出 PDF
- 小程序：微信开发者工具导入 `miniprogram/` 目录（选测试号即可预览）

## 增补知识点

```bash
cp templates/knowledge-point.md "content/<模块目录>/新知识点.md"
# 编辑后
python3 tools/build.py
```

规则详见 `content/README.md`。
