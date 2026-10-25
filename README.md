# Mathmatics

小学数学知识库（课内 1–6 年级 + 小学奥数）：按知识点组织，支持查询、打印、微信小程序访问，可持续增补。

## 目录

- `DESIGN.md` — 总体设计方案
- `content/` — 唯一数据源：知识点 Markdown（YAML 元数据 + 讲解 + 例题）+ `curriculum.yaml` 课程大纲
- `templates/` — 新知识点模板
- `tools/build.py` — 构建工具：校验覆盖矩阵 → 索引 → 打印页 → 网页版 → 小程序数据
- `dist/` — 构建产物（打印 HTML、网页版、小程序数据包）
- `miniprogram/` — 微信小程序源码（数据在 `miniprogram/data/`，由构建自动同步）
- `h5-preview/` — 小程序 H5 效果预览（近似版，`npm run dev` 启动本地预览）
- `delivery/` — 小程序静态编译证据包
- `参考讲义/` — 原始讲义素材

## 使用

```bash
python3 tools/build.py          # 校验 + 全量构建
python3 tools/build.py --check  # 只校验
```

- 查询/浏览：打开 `dist/web/index.html`。首页是按「年级 → 领域 → 知识点」组织的知识地图（1–6 年级 + 奥数），支持搜索与状态筛选。
- 奥数专题按竞赛难度编排：每个知识点含 4 道 ★4–★7 例题，讲解含模型推导、高级变形与竞赛视角；课内知识点保持 2–4 道 ★3–★5 例题。
- 打印：打开 `dist/print/<模块>.html`，浏览器 Cmd+P 出 PDF
- 小程序：微信开发者工具导入 `miniprogram/` 目录（选测试号即可预览；命令行调用需在 工具→设置→安全设置 中开启"服务端口"）
- H5 预览：`cd h5-preview && npm run dev`（或 `python3 tools/build_h5_preview.py` 重新生成）

## 增补知识点

```bash
cp templates/knowledge-point.md "content/<模块目录>/新知识点.md"
# 编辑内容，并把该知识点挂入 content/curriculum.yaml 对应年级/领域
python3 tools/build.py
```

`content/curriculum.yaml` 维护「年级 → 领域 → 知识点」大纲；大纲中 `content: null` 表示已列入地图、内容待补充。构建会校验每个知识点都已挂入大纲。

规则详见 `content/README.md`。

## 部署（GitHub Pages）

网页版与打印页已部署，改内容后一键更新：

```bash
bash tools/deploy_gh_pages.sh               # 构建 + 部署（约 1 分钟生效）
bash tools/deploy_gh_pages.sh --skip-build  # dist/ 已是最新时只部署
```

- 网页版（知识地图）：https://guobailin.github.io/Mathmatics/
- 打印页：https://guobailin.github.io/Mathmatics/print/m01.html（m01–m11 共 11 个模块）
- 公式库 KaTeX 已本地化到 `assets/katex/`（构建时自动拷入 `dist/web` 与 `dist/print`），三端均不依赖外网 CDN
- 脚本会自动选择带 `pyyaml` + `markdown-it-py` 的 Python；也可 `PYTHON=/path/to/python3 bash tools/deploy_gh_pages.sh` 指定解释器
