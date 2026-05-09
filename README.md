# Chinese Paper Formatter

这是一个“中文期刊 Word 排版”Codex skill 源仓库，不是 GUI 软件。它把期刊投稿要求、已存模板和当场自定义规则统一成 `FormatSpec` YAML，然后用确定性脚本生成或重排 Word 文档。

## 能做什么

- Markdown -> Word：按轻量 Markdown 约定识别题名、摘要、关键词、标题、正文、表图题和参考文献。
- 已有 Word -> 新 Word：不覆盖原文件，识别核心论文块后按模板统一套版。
- 期刊要求 -> 模板草案：由 Codex 根据 skill 流程抽取 `FormatSpec`，缺失项进入 `unresolved_items`，用户确认后再排版。
- 模板复用：内置模板、期刊模板、用户自定义模板都使用同一套 YAML schema。
- 默认规则库：投稿体例没有说明的页面、正文、段前段后、网格、黑体加粗、参考文献缩进等，统一从 `templates/defaults/中文期刊默认规则.yaml` 继承。
- 期刊体例库：已经沉淀的期刊模板放在 `templates/journals/`，文件名使用期刊原名，中英文都不翻译、不缩写、不转拼音。
- 细节扩展：正文两端对齐、字号、行距、缩进、标题编号、参考文献首行缩进和要素对齐等是核心字段；中西文换行、字符间距、孤行控制等高级 Word 项会被记录并尽量应用，不能应用时写入 report。

默认值：中文期刊投稿要求未说明时，正文采用宋体小四（12pt）、两端对齐、1.25 倍行距、首行缩进 2 字符；西文默认 Times New Roman；页面采用 A4 和常见页边距；不自动添加页码；默认不对齐文档网格；段前段后默认为 0；参考文献默认首行缩进 2 字符，不用悬挂缩进。

## 安装

```bash
python3 -m pip install -e ".[dev]"
```

也可以只装运行依赖：

```bash
python3 -m pip install -r requirements.txt
```

## Skill 使用

仓库根目录本身包含 `SKILL.md`、`references/` 和 `scripts/`，可以作为 Codex skill 源。主要流程见 [SKILL.md](/Users/zhutao/code/personal/chinese-paper-formatter/SKILL.md:1)，`FormatSpec` 字段说明见 [references/format-spec.md](/Users/zhutao/code/personal/chinese-paper-formatter/references/format-spec.md:1)。

## 命令

列出模板：

```bash
cpf list-templates
```

校验模板：

```bash
python3 scripts/validate_spec.py templates/presets/gb7714-in-text.yaml
```

Markdown 生成 Word：

```bash
python3 scripts/md_to_docx.py paper.md output/paper.docx --template gb7714-in-text --report output/paper.report.json
```

已有 Word 套版：

```bash
python3 scripts/apply_docx_format.py draft.docx output/draft.formatted.docx --template gb7714-in-text --report output/draft.report.json
```

保存确认后的模板：

```bash
python3 scripts/save_template.py draft-spec.yaml --name "期刊名原文" --category journals
```

使用公开期刊模板示例：

```bash
python3 scripts/md_to_docx.py paper.md output/paper.docx --template 中国社会科学 --report output/paper.report.json
```

## FormatSpec 结构

核心字段包括：

- `page`: 纸张、页边距、页眉页脚、页码、分栏。
- `paragraph`: 正文字体、字号、两端对齐、行距、首行缩进、段前段后。
- `headings`: 各级标题字体、编号、对齐、间距、是否自动编号。
- `front_matter`: 题名、作者、单位、摘要、关键词。
- `citations`: 文中注、圆圈上标、顺序编码、脚注/尾注的基本格式。
- `references`: 参考文献标题、字号、编号样式、首行缩进/悬挂缩进、段距、标点和编号细节。
- `figures_tables`: 表题、图题、表注、图注、三线表基础样式。
- `advanced_word`: 中西文换行、字符间距、孤行控制、段落网格等高级项。
- `rules`: 临时或细碎期刊规则。
- `unresolved_items`: 投稿要求不完整或冲突时的待确认项。

## 第一版边界

- 不做 GUI。
- 不承诺完整 CSL/GB7714 文献引擎。
- 不自动重排参考文献语义顺序。
- 高级 Word 细项采用“可配置但弱验证”：能应用就应用，不能应用就报告。
