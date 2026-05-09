from pathlib import Path

import pytest

from chinese_paper_formatter.docx_format import apply_docx_format, md_to_docx, parse_markdown
from chinese_paper_formatter.templates import TemplateRegistry


docx = pytest.importorskip("docx")

ROOT = Path(__file__).resolve().parents[1]


def test_parse_markdown_light_contract():
    blocks = parse_markdown(
        """# 标题

**摘 要**：摘要内容
关键词：社会学；人工智能

## 问题提出
正文段落。

表 1 样本结构
| 变量 | 数值 |
| --- | --- |
| A | 1 |

## 参考文献
作者. 题名[J]. 期刊, 2024.
"""
    )
    types = [block["type"] for block in blocks]

    assert "title" in types
    assert "abstract" in types
    assert "keywords" in types
    assert "heading" in types
    assert "table_caption" in types
    assert "table" in types
    assert "reference_item" in types


def test_md_to_docx_generates_formatted_document(tmp_path):
    registry = TemplateRegistry(ROOT / "templates")
    spec = registry.load("gb7714-in-text")
    source = tmp_path / "paper.md"
    output = tmp_path / "paper.docx"
    source.write_text(
        """# 论文标题

摘 要：摘要内容
关键词：关键词一；关键词二

## 问题提出
正文内容。

## 参考文献
作者. 题名[J]. 期刊, 2024.
""",
        encoding="utf-8",
    )

    report = md_to_docx(source, output, spec)
    document = docx.Document(str(output))

    assert output.exists()
    assert not any(item["path"] == "advanced_word.use_document_grid" for item in report["warnings"])
    assert "heading.1" in report["detected_blocks"]
    assert document.paragraphs[3].text.startswith("一、")
    assert document.paragraphs[4].paragraph_format.first_line_indent is not None
    assert document.paragraphs[4].paragraph_format.space_after.pt == 0


def test_apply_docx_format_creates_new_file_and_preserves_original(tmp_path):
    registry = TemplateRegistry(ROOT / "templates")
    spec = registry.load("gb7714-in-text")
    source = tmp_path / "draft.docx"
    output = tmp_path / "draft.formatted.docx"

    original = docx.Document()
    original.add_paragraph("论文标题")
    original.add_paragraph("摘 要：摘要内容")
    original.add_paragraph("关键词：关键词一；关键词二")
    original.add_paragraph("一、问题提出")
    original.add_paragraph("正文内容。")
    original.add_paragraph("参考文献")
    original.add_paragraph("作者. 题名[J]. 期刊, 2024.")
    original.save(str(source))

    report = apply_docx_format(source, output, spec)
    formatted = docx.Document(str(output))
    untouched = docx.Document(str(source))

    assert output.exists()
    assert source.read_bytes() != output.read_bytes()
    assert untouched.paragraphs[0].text == "论文标题"
    assert formatted.paragraphs[4].paragraph_format.first_line_indent is not None
    assert "reference_item" in report["detected_blocks"]


def test_chinese_author_year_reference_cleanup_profile(tmp_path):
    registry = TemplateRegistry(ROOT / "templates")
    spec = registry.load("gb7714-in-text")
    spec.references.punctuation = {"format_profile": "chinese_author_year_no_type_mark"}
    source = tmp_path / "paper.md"
    output = tmp_path / "paper.docx"
    source.write_text(
        """# 论文标题

## 参考文献
陈龙. “数字控制”下的劳动秩序：外卖骑手的劳动控制研究[J]. 社会学研究, 2020a,35(6):113-135,244.
孙萍. 过渡劳动：平台经济下的外卖骑手[M]. 上海: 华东师范大学出版社, 2024.
""",
        encoding="utf-8",
    )

    report = md_to_docx(source, output, spec)
    document = docx.Document(str(output))
    texts = [paragraph.text for paragraph in document.paragraphs]

    assert "chinese author-year reference cleanup" in report["applied"]
    assert "陈龙，2020a，《“数字控制”下的劳动秩序：外卖骑手的劳动控制研究》，《社会学研究》第6期。" in texts
    assert "孙萍，2024，《过渡劳动：平台经济下的外卖骑手》，上海：华东师范大学出版社。" in texts
    assert all("[J]" not in text and "[M]" not in text for text in texts)
