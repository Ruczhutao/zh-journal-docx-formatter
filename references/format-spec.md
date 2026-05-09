# FormatSpec Reference

`FormatSpec` 是中文期刊 Word 排版 skill 的唯一规格模型。期刊投稿要求、存档模板、当场自定义和 Markdown 约定都要先落成这个 YAML，再执行排版。

## Required Top-Level Sections

- `meta`: 模板名称、来源、期刊名、说明。
- `page`: 纸张、页边距、页眉页脚、页码、分栏。
- `paragraph`: 正文默认样式，尤其是字体、字号、两端对齐、行距、首行缩进。
- `headings`: 各级标题样式和编号规则；第一版脚本主要识别一至三级，模板可记录四级标题。
- `front_matter`: 题名、作者、单位、摘要、关键词。
- `citations`: 引注样式、位置和是否上标。
- `references`: 参考文献标题、条目缩进、编号样式、排序策略。
- `figures_tables`: 图题、表题、表注和三线表偏好。
- `advanced_word`: 中西文换行、字符间距、孤行控制、文档网格等高级 Word 控制。
- `rules`: 临时或细碎期刊规则，适合先记录、后续再结构化。
- `unresolved_items`: 投稿要求缺失或冲突时的待确认项。

## Built-In Defaults

默认规则库位于 `templates/defaults/中文期刊默认规则.yaml`。如果中文期刊投稿要求没有说明以下基础格式，不写入 `unresolved_items`，直接采用默认值：

- 页面：A4；默认页边距为上/下 2.54cm、左/右 3.17cm；不自动添加页码。
- 正文：宋体，小四（12pt），两端对齐，1.25 倍行距，首行缩进 2 字符。
- 西文字体：Times New Roman。
- 段前段后：一般情况下都没有。除非期刊明确要求，正文、摘要、关键词、图题、表题、参考文献条目以及标题段落都默认段前 `0pt`、段后 `0pt`。
- 文档网格：默认不启用对齐网格。
- 黑体：默认不加粗。只有投稿要求明确写“加粗”“加黑”或等价表述时，才设置 `bold: true`。
- 西文断行：默认允许西文跨行断行，不把 `latin_line_break` 作为待确认项。
- 参考文献缩进：默认首行缩进 2 字符，不用悬挂缩进。只有用户或投稿体例明确要求悬挂缩进时，才设置 `hanging_indent`。

只有当期刊给出相反要求，或稿件本身有特殊场景时，才覆盖这些默认值。

## Template Libraries

- `templates/defaults/`: 默认规则库。用于填补投稿体例或用户自定义要求没有说清楚的基础格式，不代表任何单一期刊。
- `templates/presets/`: 通用格式预设，例如 GB/T 7714、脚注制、圈码上标等。
- `templates/journals/`: 已沉淀的期刊投稿体例。文件名必须使用期刊原名；中文期刊保留中文名，英文期刊保留英文名，不翻译、不转写、不缩写。
- `templates/custom/`: 用户临时或个人自定义模板。

## Feedback Absorption

一次排版之后，用户看到 Word 输出再提出的修正，应按如下方式沉淀：

- 如果当次使用的是具体期刊模板，修正默认写入 `templates/journals/<期刊原名>.yaml`。
- 只有当用户明确说“这应成为所有中文期刊默认规则”或等价表述时，才更新 `templates/defaults/中文期刊默认规则.yaml`。
- 能结构化的规则写入对应字段，例如段距、字号、缩进、网格、黑体加粗、西文断行、参考文献缩进。
- 暂时没有结构化字段的规则写入 `rules`，并在 report 中说明是否已应用。
- 目标是让下一次 `--template 期刊名` 直接吸收上次确认过的修正，而不是依赖对话记忆。

## Common Mapping

投稿要求里的“正文小四宋体，两端对齐，1.25 倍行距，首行缩进 2 字符”：

```yaml
paragraph:
  font:
    family: "宋体"
    size: "12pt"
  align: "justify"
  line_height: 1.25
  first_line_indent: "2em"
```

投稿要求里的“一级标题黑体四号居中，采用一、二、三编号”：

```yaml
headings:
  "1":
    level: 1
    font:
      family: "黑体"
      size: "14pt"
    align: "center"
    first_line_indent: null
    auto_number: true
    numbering: "chinese"
```

投稿要求里的“参考文献五号宋体，首行缩进 2 字符”：

```yaml
references:
  entry:
    font:
      family: "宋体"
      size: "10.5pt"
    align: "justify"
    first_line_indent: "2em"
  hanging_indent: "0pt"
```

投稿要求里的“允许西文在单词中间换行/中西文混排换行规则”第一版放入高级规则：

```yaml
advanced_word:
  east_asian_line_break: true
  latin_line_break: true
```

这类高级项第一版会被记录并报告，脚本只尽力应用，不保证完全复刻 Word 的所有版式行为。

## Reference Entry Normalization

参考文献条目不是“只调字号”的段落，而是需要按期刊模板做要素级对齐：

- 先确定该刊要求的条目要素顺序，例如作者、年份、题名、文献类型、刊名/书名、卷期、页码、出版地、出版社、访问日期、URL。
- 如果某类参考文献清理规则可被通用化，可在 `references.punctuation.format_profile` 中记录 profile 名称，例如 `chinese_author_year_no_type_mark`。
- 源条目缺少模板必需要素时，只有能从原条目中明确推断时才补齐；不能推断时写入 `unresolved_items`。
- 源条目包含模板不需要的要素时，应删除或移入报告说明。例如某刊不用 `[J]` 类型码，就应删除；某刊不用页码，就不保留页码。
- 标点符号必须统一到该刊格式，不能同一参考文献区混用全角、半角、中文冒号、英文冒号、句点和逗号。
- 同一作者连续出现多篇文献时，如果该刊采用作者重复线，后续条目作者名用 `——`。
- 不要默认使用悬挂缩进；中文期刊参考文献通常按首行缩进处理，除非投稿体例明确要求悬挂缩进。
- 自动处理不了的语义项，例如英文书刊名斜体、外文作者名顺序、网页访问日期，应在 report 里明确说明，不能静默跳过。

## Markdown Input Contract

第一版采用轻量约定：

- 第一个 `#` 标题作为论文题名。
- `##`、`###`、`####` 分别映射到一、二、三级标题。
- `摘 要：` 或 `**摘 要**：` 映射到摘要。
- `关键词：` 映射到关键词。
- `## 参考文献` 后的非空行映射为参考文献条目。
- `图 1` / `图一` 开头的段落映射为图题。
- `表 1` / `表一` 开头的段落映射为表题。
- Markdown 管道表会转成 Word 表格，但第一版不强制三线表边框。

## Confirmation Rules

当期刊要求没有说明以下内容时，不要静默猜测，应写入 `unresolved_items`：

- 引注位置。
- 标题是否自动编号。
- 图题、表题和参考文献是否另有字号或段距。

`unresolved_items` 示例：

```yaml
unresolved_items:
  - path: "references.english_titles"
    message: "投稿要求要求英文书名/期刊名斜体，但当前条目无法自动识别具体范围，请人工确认。"
```
