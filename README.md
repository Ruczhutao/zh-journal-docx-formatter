# 中文期刊 Word 排版工具

把投稿网站上的格式要求，变成可复用的 Word 排版模板。

中文期刊投稿体例常常写得很散：字号、行距、标题编号、脚注、参考文献、网格、匿名审稿要求混在一段说明里，有些还没有说完整。这个项目的目标是：你可以直接把期刊投稿网页、附件体例或自己的补充要求发给 agent，它会整理出一份可执行的排版模板，然后把 Markdown 或已有 `.docx` 稿件排成新的 Word 文件。

它不是 GUI，也不是完整文献管理器。它更像一个可沉淀的“中文期刊投稿排版规则库”。

## 典型工作流

1. 把期刊投稿网站上的格式要求直接发给 agent。
2. agent 把要求整理成一份期刊模板，并标出缺失、冲突或暂时无法自动处理的项目。
3. 你提供 Markdown 稿件或已有 Word 稿件。
4. 工具生成一个新的 `.docx`，不覆盖原文件，同时输出处理报告。
5. 你看完 Word 后提出修正，例如“段后不要 10 磅”“参考文献不要悬挂缩进”“黑体不要自动加粗”。
6. 这些修正会写回对应期刊模板，下次再用这个期刊名时直接生效。

## 能解决什么

- 不想手工记每个期刊的 Word 格式。
- 不想每次都重新设置正文、标题、摘要、关键词、参考文献。
- 投稿体例没有写清楚时，需要一套稳定默认规则兜底。
- 已经排过一次后，希望后续修正自动沉淀，而不是每次重新提醒。
- 想保留原稿，只生成一份新的投稿格式 Word。

## 支持的输入

- Markdown 稿件：适合从写作稿直接生成 Word。
- 已有 Word 稿件：适合在原有 `.docx` 内容基础上重新套版。
- 期刊投稿要求：可以是投稿网页文字、附件体例、用户补充规则。
- 已存模板：可以是公开期刊模板，也可以是你自己的本地模板。

## 模板学习与自动更新

默认规则只负责兜底；具体期刊模板会持续吸收你的修正。

例如你用《中国社会科学》模板排版后发现某个细节不对，可以直接说：

```text
参考文献条目不要悬挂缩进，默认首行缩进 2 字符。
```

这条规则会写回 `templates/journals/中国社会科学.yaml`。以后再次使用：

```bash
--template 中国社会科学
```

就会直接使用更新后的模板，而不是依赖聊天记录或临时提醒。

只有当你明确说“这应该成为所有中文期刊的默认规则”时，才会更新默认规则库。

## 默认规则

当期刊没有明确说明时，默认采用：

- 页面：A4，常见 Word 页边距，不自动添加页码。
- 正文：宋体小四（12pt），两端对齐，1.25 倍行距，首行缩进 2 字符。
- 西文：Times New Roman，默认允许西文断行。
- 段距：段前段后默认为 0。
- 网格：默认不启用文档网格或对齐网格。
- 黑体：黑体默认不等于加粗，只有明确写“加粗/加黑”才设置加粗。
- 参考文献：默认比正文小一号字，首行缩进 2 字符，不默认使用悬挂缩进。

默认规则库：

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

期刊模板文件名使用期刊原名。中文期刊保留中文名，英文期刊保留英文名，不翻译、不转拼音、不缩写。

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

已有 Word 文档重新套版：

```bash
python3 scripts/apply_docx_format.py draft.docx output/draft.formatted.docx --template 中国社会科学 --report output/draft.report.json
```

保存确认后的期刊模板：

```bash
python3 scripts/save_template.py draft-spec.yaml --name "期刊名原文" --category journals
```

## 第一版边界

- 不做 GUI。
- 不承诺完整 CSL/GB7714 文献引擎。
- 不自动重排参考文献语义顺序。
- 不自动生成英文标题、摘要或关键词。
- Word 文档网格、脚注域、页码域等高级项目会先记录和报告；能自动应用的部分逐步扩展。

## English

`zh-journal-docx-formatter` turns Chinese journal submission requirements into reusable Word formatting templates.

You can paste journal guidelines from a submission website, provide a Markdown or existing `.docx` manuscript, and generate a newly formatted Word file without overwriting the source document. Corrections made after reviewing the output can be written back into the corresponding journal template, so future runs reuse the improved style automatically.

This first version focuses on deterministic formatting and template accumulation. It does not provide a GUI, a full bibliography engine, or complete Word footnote/grid automation.
