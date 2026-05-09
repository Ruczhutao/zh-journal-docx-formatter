# Chinese Paper Formatter

中文学术论文排版工具。支持 Markdown 和 Word 双输入，自动处理引注格式、字体字号、标题编号、参考文献等。

## 功能

- **引注格式转换**：作者-年份 → 圆圈上标 / GB/T 7714 序号
- **标题自动编号**：一级标题"一、"，二级标题"（一）"
- **字体字号标准化**：标题、正文、参考文献分别设置
- **参考文献重排**：按首次出现顺序排列
- **双输入支持**：直接处理 Markdown 或已有 Word 文档
- **期刊模板预设**：内置常见中文学术期刊格式

## 安装

```bash
git clone https://github.com/yourname/chinese-paper-formatter.git
cd chinese-paper-formatter
pip install -r requirements.txt
```

## 使用

### Markdown → Word（期刊投稿版）

```python
from src.converters.md_to_docx import convert_md_to_docx

convert_md_to_docx(
    input_path="paper.md",
    output_path="paper_formatted.docx",
    citation_style="circled",  # circled | numbered | author_year
    heading_numbers=True       # 自动添加"一、""（一）"
)
```

### Word → Word（格式调整）

```python
from src.converters.docx_to_docx import format_docx

format_docx(
    input_path="paper_draft.docx",
    output_path="paper_formatted.docx",
    citation_style="circled",
    heading_numbers=True
)
```

### 命令行

```bash
# Markdown → Word
python -m src.converters.md_to_docx paper.md paper.docx --style circled

# Word → Word
python -m src.converters.docx_to_docx paper.docx paper_formatted.docx --style circled
```

## 项目结构

```
chinese-paper-formatter/
├── src/
│   ├── formatters/          # 格式化引擎
│   │   ├── markdown_parser.py
│   │   ├── docx_formatter.py
│   │   └── reference_manager.py
│   ├── converters/          # 转换器
│   │   ├── md_to_docx.py    # Markdown → Word
│   │   └── docx_to_docx.py  # Word → Word
│   └── utils/               # 工具函数
│       ├── font_manager.py
│       └── numbering.py
├── templates/               # 期刊模板
│   └── journal_article.yaml
├── examples/                # 示例
├── requirements.txt
└── README.md
```

## 输入格式

```markdown
# 论文标题

**摘 要**：摘要内容...

关键词：关键词1；关键词2

## 问题提出

正文内容...（作者，2020a）

### 文献回顾

更多内容...（作者，2020b；另一作者，2018）

## 参考文献

作者. 题名[J]. 期刊名, 2020a, 35(6): 113-135.
另一作者. 题名[M]. 出版社, 2018.
```

## 输出格式

- 标题：黑体三号居中
- 一级标题：黑体四号居中，"一、""二、"自动编号
- 二级标题：宋体小四加粗左对齐，"（一）""（二）"自动编号
- 正文：宋体小四，左右对齐，首行缩进2字符，1.25倍行距
- 引注：圆圈上标 `①②③` 或 GB/T 7714 序号
- 参考文献：按首次出现顺序排列

## 开发计划

- [ ] 支持更多引注格式（GB/T 7714 顺序编码制、脚注等）
- [ ] 期刊模板扩展（支持更多期刊自定义格式）
- [ ] Word 直接编辑（无需重新生成，直接修改样式）
- [ ] GUI 界面（非命令行用户友好）

## 许可

MIT
