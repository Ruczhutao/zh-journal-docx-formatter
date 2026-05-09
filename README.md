# Journal DOCX Formatter

把投稿网站上的格式要求，变成可复用、会持续学习的 Word 排版模板。📄

很多期刊的投稿体例并不是一张清楚的格式表，而是散落在网页、附件和说明文字里：字号、行距、标题编号、脚注、参考文献、文档网格、匿名审稿要求，常常混在一起，有些还没有说完整。中文期刊可以用，英文期刊也可以用。

你不需要一开始就维护一套完美的默认模板。最简单的做法是：找到你要投稿的期刊，把投稿网页、附件体例或格式说明直接发给 agent。agent 会先整理出该期刊的投稿模板；没有写清楚的部分，会用默认规则兜底，或者列出来让你确认。

默认模板不是必须的。你完全可以直接从某个期刊的投稿模板开始：先排一版，看输出效果，再把你发现的问题告诉 agent。比如“段后不要 10 磅”“参考文献不要悬挂缩进”“黑体不要自动加粗”。这些修正会写回对应期刊模板，下次再投同一个期刊，就会直接沿用更新后的规则。🧠

## 典型工作流

1. 找到你要投稿的期刊要求，可以是网页、PDF、Word 附件或纯文字说明。
2. 直接把这些要求发给 agent。
3. agent 整理出一份期刊模板，并标出缺失、冲突或暂时无法自动处理的项目。
4. 你提供 Markdown 稿件或已有 Word 稿件。
5. 工具生成一个新的 `.docx`，不覆盖原文件，同时输出处理报告。
6. 你看完 Word 后提出修正，这些修正会写回对应期刊模板。

## 能解决什么

- 不想手工记每个期刊的 Word 格式。
- 不想每次都重新设置正文、标题、摘要、关键词、参考文献。
- 投稿体例没有写清楚时，希望 agent 帮你列出需要确认的地方。
- 已经排过一次后，希望后续修正自动沉淀，而不是每次重新提醒。
- 想保留原稿，只生成一份新的投稿格式 Word。

## 支持的输入

- Markdown 稿件：适合从写作稿直接生成 Word。
- 已有 Word 稿件：适合在原有 `.docx` 内容基础上重新套版。
- 期刊投稿要求：可以是投稿网页文字、附件体例、用户补充规则。
- 已存模板：可以是公开期刊模板，也可以是你自己的本地模板。

## 模板学习与自动更新

具体期刊模板会持续吸收你的修正。

例如你用《中国社会科学》模板排版后发现某个细节不对，可以直接说：

```text
参考文献条目不要悬挂缩进，默认首行缩进 2 字符。
```

这条规则会写回 `templates/journals/中国社会科学.yaml`。以后再次让 agent 按《中国社会科学》排版时，就会直接使用更新后的模板，而不是依赖聊天记录或临时提醒。

只有当你明确说“这应该成为所有期刊的默认规则”时，才会更新默认规则库。

## 默认模板

默认模板不是使用前提。你可以直接从某个期刊投稿要求开始，让 agent 先生成该期刊模板。

默认模板的作用是：当期刊要求没有写清楚时，提供一套基础排版兜底规则，并把仍需确认的项目暴露出来。

默认规则库：

```text
templates/defaults/中文期刊默认规则.yaml
```

## 模板目录

```text
templates/defaults/   # 默认规则
templates/presets/    # 通用预设
templates/journals/   # 已确认的公开期刊投稿体例
templates/custom/     # 用户自定义模板，按需本地创建
```

期刊模板文件名使用期刊原名。中文期刊保留中文名，英文期刊保留英文名，不翻译、不转拼音、不缩写。

当前公开样例：

- `templates/journals/中国社会科学.yaml`

## 使用方式

这个仓库主要供 agent 调用。实际使用时，不需要手动记命令；你只需要说明目标，例如：

```text
请把这篇 Markdown 按《中国社会科学》的格式排成 Word。
```

或者：

```text
这是某期刊投稿要求，请先整理成模板，再把我的 Word 稿件套版。
```

agent 会读取模板、生成新的 `.docx`，并把无法自动确认或暂未完全支持的项目写入报告。

## English

Turn journal submission guidelines into reusable, continuously improving Word formatting templates. 📄

Journal formatting rules are often scattered across submission pages, PDF attachments, and style notes: fonts, spacing, heading numbering, footnotes, references, document grids, anonymization requirements, and many small exceptions. The workflow works for both Chinese and English-language journals.

You do not need to build a perfect default template first. The simplest workflow is to find the journal you plan to submit to, send its submission guidelines to an agent, and let the agent turn those requirements into a journal-specific template. Missing or unclear parts can be filled by defaults or surfaced for confirmation.

The default template is optional. You can start directly from a journal submission template, format one manuscript, review the output, and tell the agent what needs to change. Those corrections are written back into the corresponding journal template, so the next run uses the improved rules automatically. 🧠
