# T8 全库三端一致性审查

> 审查日期：2026-11-08  
> 仓库：`guobailin/Mathmatics`  
> 审查主键：知识点稳定 ID（不以标题作为唯一键）

## 1. 审查范围

- **正文源**：`content/**/*.md` 的 YAML frontmatter、讲解、例题和变式/自测。
- **独立卡片源**：`tools/cards/content/*.json`。
- **小程序数据**：`miniprogram/data/m01.json` 至 `m12.json`。
- **生成产物**：`dist/miniprogram/*.json`，仅作为构建输出核验，不作为源数据。

## 2. 结构盘点结果

| 项目 | 当前数量 | 结构结果 |
|---|---:|---|
| 课程/正文知识点基线 | 249 | `AUDIT_REGISTER.csv` 为 249 条唯一 ID |
| 小程序数据 | 249 | 12 个模块文件，249 个唯一 ID |
| 独立速查卡 | 107 | 9 个 JSON 文件，107 个唯一 ID |
| 卡片 ID 对应正文 | 107/107 | 未发现台账外卡片 ID |
| 小程序讲解 | 249/249 | 无空讲解 |
| 小程序例题 | 249/249 | 无空例题 |
| 小程序变式/自测 | 249/249 | 每条记录均有对应数组 |

### 小程序模块数量

| 文件 | 模块 | 记录数 |
|---|---|---:|
| m01 | 数与计算 | 59 |
| m02 | 代数初步 | 11 |
| m03 | 图形与几何 | 36 |
| m04 | 统计与概率 | 9 |
| m05 | 应用题 | 27 |
| m06 | 奥数-计算 | 15 |
| m07 | 奥数-计数 | 16 |
| m08 | 奥数-数论 | 24 |
| m09 | 奥数-几何 | 18 |
| m10 | 奥数-行程 | 12 |
| m11 | 奥数-组合 | 9 |
| m12 | 奥数-应用题 | 13 |
| **合计** | | **249** |

## 3. 发现与处理

### T8-001｜m12 manifest 计数落后

- 现象：`miniprogram/data/m12.json` 已有 13 条，但 `miniprogram/data/manifest.json` 仍记为 12。
- 原因：T5 新增“页码问题”后，模块数据更新，manifest 未同步。
- 处理：已将 m12 的 count 修正为 13。

### T8-002｜历史文档仍使用 248 条旧口径

- 现象：README 与 CARD_AUDIT 仍显示 248 条知识点，并将 `app-page-number` 记为孤立卡片。
- 处理：当前总量更新为 249；CARD_AUDIT 中的孤立卡片事项关闭。
- 说明：QUALITY_AUDIT 中旧轮次的 248 条记录属于当时快照，保留历史事实；最新基线以第 90 节及 `AUDIT_REGISTER.csv` 为准。

### T8-003｜页码问题已从孤立卡片转为完整知识点

- 现象：早期 `app-page-number` 只有卡片，没有正文和小程序记录。
- 处理：T5 已补齐 `content/12-奥数-应用题/页码问题.md`、课程大纲、独立卡片和 `miniprogram/data/m12.json`；SPEC.md 的旧例外说明已同步移除。
- 当前结果：该 ID 已列入 249 条审查台账，不再是孤立项。

### T8-004｜卡片短标题与课程标题存在展示差异

以下 5 个卡片使用了更短或更适合卡面的标题：

- `wp-unit-rate`：卡片“归一与归总” / 课程“归一问题”
- `wp-sum-multiple`：卡片“和倍与差倍” / 课程“和倍问题”
- `nt-multiple-extremum`：卡片“倍数特征与最值” / 课程“倍数特征/最值”
- `nt-square-cube-factor`：卡片“平方数与立方数分解质因数” / 课程“平方/立方数分解质因数”
- `nt-lcm-extremum`：卡片“最小公倍数与最值” / 课程“最小公倍数/最值”

处理原则：这些差异不作为 ID 错配；稳定 ID 是映射主键。卡片标题可以作为面向学生的短标题，但不得因此改动正文知识点名称。

### T8-005｜dist 是旧构建副本

- 现象：主分支中 `dist/miniprogram/m01.json` 至 `m12.json` 的文件 blob 均与 `miniprogram/data/` 不同，manifest 也属于旧版。
- 处理原则：`dist/` 是 `tools/build.py` 生成的发布产物，不反向覆盖 Markdown 或小程序源数据。发布前先执行全量构建；CI 在构建后比较 dist 与小程序数据，防止旧产物进入发布站点。
- 注意：主分支中已提交的 dist 快照不等于 GitHub Pages 最近一次 CI 构建的发布内容。

## 4. 自动化一致性门禁

新增 `tools/check_consistency.py`，并接入 `.github/workflows/deploy-pages.yml`。工作流先运行 `python tools/cards/embed.py`，依据独立 JSON 唯一真源重建非手工内嵌卡（4 篇 `MANUAL_MD` 保留项跳过）；随后运行 `python tools/build.py`，最后执行以下检查：

1. Markdown 源 ID 唯一，课程大纲引用有效。
2. 小程序记录与 Markdown 源 ID 集合一致。
3. 小程序的 title、module、grade、tags、difficulty、skills、related、lecture、examples、variants 与构建源数据逐字段一致。
4. 独立卡片 ID 必须对应 Markdown 正文。
5. 自动生成的内嵌卡片块必须与独立卡片 JSON 逐块一致；4 篇手工保留卡片单独检查，不被自动覆盖。首次运行发现 65 条自动卡片差异（38 条原本一致、4 条手工保留），将按 JSON 源重建后再复核。
6. dist/miniprogram 与构建后 miniprogram/data 一致，manifest 模块计数一致。
7. 自动生成 `CONSISTENCY_MATRIX.csv` 和 `CONSISTENCY_ISSUES.csv`，并由 GitHub Actions 提交审计产物。

## 5. 验收边界

- 已完成：知识点与小程序 ID 映射、卡片 ID 映射、重复/缺失/空字段结构盘点、manifest 修正、旧统计文档校准。
- **最终结果：通过。** GitHub Actions run `42489774543` 成功；门禁输出 Markdown 249 IDs、小程序 249 个唯一 ID、独立卡片 107 IDs、自动内嵌卡 103 条完全一致、4 条手工保留、问题数 0。`CONSISTENCY_MATRIX.csv` 已生成 249 行知识点记录，`CONSISTENCY_ISSUES.csv` 仅有表头、无未解决差异。
- 结构一致不等于数学内容正确；数学推导、答案复算、教材覆盖、竞赛题来源和实体打印仍由 T1–T7、T9–T10 的专项任务分别验收。


## 6. 最终自动验收结果（2026-11-08）

- GitHub Actions：<https://github.com/guobailin/Mathmatics/actions/runs/42489774543>，结论 success。
- `tools/cards/embed.py`：107 个卡片 ID 中写入 103 个自动卡片，保留 4 个手工维护卡片；无缺少 Markdown、无缺少“例题”锚点。
- `tools/build.py`：校验通过，249 个知识点、778 道例题、107 篇共 428 道变式/自测；构建 12 个小程序模块。
- `tools/check_consistency.py`：249/249 小程序记录与 Markdown 源字段逐项一致；103/103 自动内嵌卡与独立 JSON 一致；4 个手工卡存在；问题 0。
- 矩阵：`CONSISTENCY_MATRIX.csv` 共 249 条知识点记录；问题清单 `CONSISTENCY_ISSUES.csv` 无未解决项。
- **后续转交 T9**：卡片渲染检查报告 13 张卡片有溢出（牛吃草、经济问题、分数裂项、速算与巧算、线分圆环、最大公因数与最小公倍数、进位制、斜三角形面积、立体几何综合、角度计算、时钟问题、火车追及、基本公式与平均速度）。这是 JSON 同步后的版面容量问题，不是三端数据错配；T9 应逐张压缩并重新做 Chrome 检查。
