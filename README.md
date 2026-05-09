# 中文期刊 Word 排版工具

这是一个面向中文期刊投稿的 Word 排版工具源仓库，也可以作为 Codex skill 使用。它的核心不是 GUI，而是一套可扩展的 `FormatSpec` YAML 模板模型：投稿要求文本、已存期刊体例、用户当场自定义、Markdown 输入和已有 Word 输入，最终都归一到同一套规格，再由确定性脚本生成或重排 `.docx`。

## 能做什么

- Markdown -> Word：按轻量 Markdown 约定识别题名、摘要、关键词、标题、正文、表图题和参考文献。
- 已有 Word -> 新 Word：不覆盖原文件，识别核心论文块后按模板统一套版。
- 投稿要求 -> 模板草案：根据期刊投稿体例抽取 `FormatSpec`，缺失或冲突项进入 `unresolved_items`。
- 模板复用：默认规则、通用预设、公开期刊模板和用户自定义模板都使用同一套 YAML schema。
- 反馈沉淀：一次排版后发现的细节修正，可以写回具体期刊模板，后续再次使用该期刊名时直接生效。

## 默认规则

中文期刊投稿要求没有说明时，默认采用：

- 页面：A4，常见 Word 页边距，不自动添加页码。
- 正文：宋体小四（12pt），两端对齐，1.25 倍行距，首行缩进 2 字符。
- 西文：Times New Roman，默认允许西文断行。
- 段距：段前段后默认为 0。
- 网格：默认不启用文档网格或对齐网格。
- 黑体：黑体默认不等于加粗，只有明确写“加粗/加黑”才设置加粗。
- 参考文献：默认比正文小一号字，首行缩进 2 字符，不默认使用悬挂缩进。

默认规则库位于：

```text
templates/defaults/中文期刊默认规则.yaml
```

## 模板目录

```text
templates/defaults/   # 中文期刊通用默认规则
templates/presets/    # GB/T 7714、脚注制、圈码上标等通用预设
templates/journals/   # 已确认的公开期刊投稿体例
templates/custom/     # 用户自定义模板，按需本地创建
```

期刊模板文件名应使用期刊原名。中文期刊保留中文名，英文期刊保留英文名，不翻译、不转拼音、不缩写。

当前公开样例：

- `templates/journals/中国社会科学.yaml`

## 安装

开发安装：

```bash
python3 -m pip install -e ".[dev]"
```

只安装运行依赖：

```bash
python3 -m pip install -r requirements.txt
```

## 常用命令

列出模板：

```bash
cpf list-templates
```

校验模板：

```bash
python3 scripts/validate_spec.py templates/journals/中国社会科学.yaml
```

Markdown 生成 Word：

```bash
python3 scripts/md_to_docx.py paper.md output/paper.docx --template 中国社会科学 --report output/paper.report.json
```

已有 Word 套版：

```bash
python3 scripts/apply_docx_format.py draft.docx output/draft.formatted.docx --template 中国社会科学 --report output/draft.report.json
```

保存确认后的期刊模板：

```bash
python3 scripts/save_template.py draft-spec.yaml --name "期刊名原文" --category journals
```

## FormatSpec 结构

核心字段包括：

- `page`: 纸张、页边距、页眉页脚、页码、分栏。
- `paragraph`: 正文字体、字号、两端对齐、行距、首行缩进、段前段后。
- `headings`: 各级标题字体、编号、对齐、间距、是否自动编号。
- `front_matter`: 题名、作者、单位、摘要、关键词。
- `citations`: 文中注、圈码上标、顺序编码、脚注/尾注的基本格式。
- `references`: 参考文献标题、字号、编号样式、缩进、段距、标点和编号细节。
- `figures_tables`: 表题、图题、表注、图注、三线表基础样式。
- `advanced_word`: 中西文换行、字符间距、孤行控制、文档网格等高级 Word 项。
- `rules`: 暂未结构化的细碎期刊规则。
- `unresolved_items`: 投稿要求不完整、脚本暂不支持或需要人工确认的项目。

字段细节见：

- [SKILL.md](SKILL.md)
- [references/format-spec.md](references/format-spec.md)

## 第一版边界

- 不做 GUI。
- 不承诺完整 CSL/GB7714 文献引擎。
- 不自动重排参考文献语义顺序。
- 不自动生成英文标题、摘要或关键词。
- 高级 Word 细项采用“可配置但弱验证”：能应用就应用，不能应用就写入 report。

## English

`zh-journal-docx-formatter` is a FormatSpec-based toolkit and Codex skill source for formatting Chinese journal manuscripts in Word.

It normalizes journal requirements, saved templates, ad-hoc user rules, Markdown manuscripts, and existing Word documents into a shared YAML model, then applies deterministic `.docx` formatting scripts.

Main features:

- Markdown to `.docx`.
- Existing `.docx` to newly formatted `.docx` without overwriting the source file.
- Reusable YAML templates for defaults, presets, public journal styles, and custom styles.
- Explicit reports for applied rules, unresolved requirements, and partially supported advanced Word settings.

This first version is formatting-oriented. It does not provide a GUI, a full CSL/GB7714 bibliography engine, or complete Word footnote/grid automation.
