# 卡片内容压缩规格（所有执行者必读）

## 目标
把知识点的「## 讲解」部分压缩成一张 13cm×9cm 卡片可容纳的要点+公式。
不抄例题、不抄竞赛真题、不写长推导、不讲原理证明。只留「能直接拿去用的」。

## 源文件结构
每个 md 文件开头是 YAML frontmatter（含 `id`、`title`），正文含 `## 讲解`、`## 竞赛真题中的考察`、`## 例题` 等小节。
**只读 `## 讲解` 到下一个 `## ` 标题之间的内容**，其余全部忽略。

## 输出格式
写入指定 JSON 文件，结构：

```json
{
  "module_dir": "06-奥数-计算",
  "items": [
    {
      "id": "与 frontmatter 一致",
      "title": "与 frontmatter 一致",
      "span": 1,
      "pair_with": "同模块另一个 id 或 null",
      "blocks": [ ... ]
    }
  ]
}
```

block 类型（按显示顺序）：
- `{"t":"sec","v":"小节名"}` 小节标题，≤6 字，如「基本关系」「常用公式」「判定」「易错」
- `{"t":"li","v":"...要点..."}` 条目，正文默认样式
- `{"t":"fx","v":"S_n=\\frac{(a_1+a_n)n}{2}"}` 独立居中的公式（无 $ 包裹、无文字）
- `{"t":"tip","v":"识别信号：..."}` 绿色，全卡片最多 1 条
- `{"t":"warn","v":"易错：..."}` 红色，全卡片最多 1 条
- `{"t":"fig","v":"图名"}` 示意图，右浮动、宽 34mm，**每张卡最多 1 个**，且必须是 blocks 里的第一个元素
  - 图名取自 `assets/geometry/cards/` 下的 svg 文件名（不含扩展名），如 `butterfly-model`、`lattice-area`
  - 可用图：equal-area、bird-head、similarity、swallow-tail、butterfly-model、area-ratio、pythagoras、
    circle-sector、three-views、solid-geometry、surface-coloring、lattice-area、area-synthesis、
    oblique-triangle、perimeter-tricks、perimeter-problem、geometry-method
  - **插图的卡容量更紧**：图约占 4 行等效高度，总显示行数仍须 ≤16（含图的 4 行）

## 容量硬约束（违反会被打回）
渲染后卡片内容区约 **120mm 宽 × 66mm 高**，正文 8.1pt、行高 1.45。

- 中文每行约 38–42 字；含行内公式时按展开宽度折算。
- 估算「显示行数」：`sec` 占 1.2 行；`fx` 占 1.4 行；`li` 按 ⌈字符宽度/40⌉ 计；`warn/tip` 按 1–2 行。
- **每张卡片（span=1）总显示行数控制在 13–16 行**；宁可精简，不能超过 16。
- 每个知识点 `sec ≤ 4` 个；`li` 总数 ≤ 11 条；每条 `li` ≤ 42 字（含公式折算）。
- 单条 `li` 里的行内公式 ≤ 2 个，太长就拆成 `fx`。

## 内容取舍（按优先级）
1. **核心公式/结论**（必收，写成 `fx` 或带公式的 `li`）
2. **判定法则 / 口诀 / 常用数据**（如勾股数、整除特征表、排列组合公式）
3. **关键变形与套路**（一句话能说清的）
4. `tip`：一句话「看到什么信号想到它」
5. `warn`：一句话最高频易错点

舍弃：证明过程、例题、数值举例、背景故事、竞赛真题索引。

## LaTeX 写法（离线转换器，仅支持下列）
- 行内公式一律 `$...$`；独立公式用 `fx` block、不带 `$`
- 支持：`\frac{a}{b}` `\dfrac` `\sqrt{}` `\binom{}{}` `\pmod{}` `\overline{}` `\text{}` `^{}` `_{}` 单字符上下标
- 符号：`\times \div \cdot \pm \le \leq \ge \geq \ne \neq \approx \equiv \to \rightarrow \Rightarrow \angle \triangle \square \parallel \perp \sim \cong \alpha \beta \gamma \theta \pi \lambda \mu \varphi \cdots \ldots \dots \in \infty \degree \circ`
- 分组用 `{...}`；`\,` `\;` `\quad` 表示空格
- **不要**用 `\boxed \dfrac d 省略 \operatorname \mathrm \mathbb \begin{}` 等生僻宏；不支持 `\\` 换行

## 配对规则（pair_with）
- 只在**同一模块、同一批次**内两两配对；必须一对一、双向一致（A.pair_with=B 且 B.pair_with=A）
- 优先语义强相关：如「同余初步↔韩信点兵」「容斥原理↔容斥最值」「加乘原理↔排列组合」「相遇↔追及」
- 奇数个时允许最多 1 个 `pair_with: null`（它独占半张卡，背面留空）
- 拿不准就 null，不要硬配

## span=2（极少数）
内容确实压不进 16 行时，可标 `"span": 2`，此时不用 `blocks`，改用 `front_blocks`（≤16 行）和 `back_blocks`（≤16 行）。
默认尽量 span=1；一个批次最多 1 个 span=2。

## 交付
只写 JSON 文件（UTF-8，两个空格缩进），并在回复里用一行一个列出：`id | title | 估算行数 | span | pair_with`，不要贴正文。

## 打印提示条（仅屏幕可见）

`render.py` 在 `cards.html` 的 body 最前面注入一条 `.hint` 提示条，写明五项打印设置
（A4 横向 / 边距无 / 缩放 100% / 取消页眉页脚 / 双面沿长边翻转）与计数。
样式里有 `@media print { .hint { display: none !important } }`，**打印与出 PDF 时整条移除**，
不会出现在纸上，也不影响分页（已实测 PDF 仍为 28 页、体积不变）。
改文案改 `render.py` 里的 `HINT_TPL`（用 `str.format`，不要用 `%` —— 正文含「100%」会撞格式化）。

## 回写知识点正文（embed.py）

`python3 tools/cards/embed.py --dry` 先看报告，去掉 `--dry` 写入。

- 唯一真源仍是 `content/*.json`；本脚本只做「卡片 → md」单向生成，**不要反向手改 md 里的速查卡段落**。
- 落点：frontmatter `id` 对应 md 的 `## 例题` 之前；无 `## 例题` 时跳过并报告。
- 幂等：以 `<!-- card:auto -->` / `<!-- /card:auto -->` 包裹，重跑整段替换，不会堆叠。
- 映射：`sec→**粗体**`、`fx→$$...$$`、`li→- `、`tip/warn→段末合并成一个引用块`；
  `fig` 仅当 md 里没引用过该图才补。卡片里已有「易错」小节时，末尾 ⚠️ 行去掉重复的“易错：”。
- `app-page-number`（页码问题）仓库无对应 md，是唯一跳过的知识点。
- **手工保留名单**：`embed.py` 顶部的 `MANUAL_MD`（现为 角度计算 / 燕尾模型 / 面积综合 / 鸟头模型）
  这几篇的 md 速查卡比卡片详细，含 16 行容量放不下的结论，回写会降级内容，故整篇跳过。
  要解除：先把 md 独有的结论补进对应 JSON，再从名单里删掉。
