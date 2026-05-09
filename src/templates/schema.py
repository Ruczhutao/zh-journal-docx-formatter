"""
Template schema and validation for Chinese paper formatter.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum

class CitationPosition(str, Enum):
    IN_TEXT = "in-text"
    FOOTNOTE = "footnote"
    ENDNOTE = "endnote"

class CitationStyle(str, Enum):
    NUMBERED = "numbered"       # [1], [2], ...
    CIRCLED = "circled"         # ①, ②, ...
    AUTHOR_YEAR = "author_year" # (作者, 2020)

class NumberingType(str, Enum):
    CHINESE = "chinese"         # 一、二、三...
    CHINESE_PAREN = "chinese_paren"  # （一）（二）...
    ARABIC = "arabic"           # 1., 2., ...
    ARABIC_PAREN = "arabic_paren"    # (1), (2), ...
    NONE = "none"

class Align(str, Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"

@dataclass
class FontStyle:
    """Font styling specification."""
    font_family: str
    font_size: str  # e.g., "16pt", "12pt"
    bold: bool = False
    italic: bool = False
    color: Optional[str] = None  # hex color

@dataclass
class ParagraphStyle:
    """Paragraph styling specification."""
    font: FontStyle
    align: Align = Align.JUSTIFY
    line_height: float = 1.25
    first_line_indent: Optional[str] = None  # e.g., "2em"
    space_before: Optional[str] = None
    space_after: Optional[str] = None

@dataclass
class HeadingStyle(ParagraphStyle):
    """Heading style with numbering."""
    numbering: NumberingType = NumberingType.CHINESE
    level: int = 1

@dataclass
class CitationConfig:
    """Citation configuration."""
    style: CitationStyle
    position: CitationPosition
    format_string: str = "[{number}]"
    superscript: bool = True

@dataclass
class ReferenceListConfig:
    """Reference list configuration."""
    enabled: bool = True
    sort_by: str = "appearance"  # appearance | author
    hanging_indent: str = "2em"
    numbering_style: CitationStyle = CitationStyle.NUMBERED

@dataclass
class PageConfig:
    """Page configuration."""
    paper_size: str = "A4"
    top_margin: str = "2.54cm"
    bottom_margin: str = "2.54cm"
    left_margin: str = "3.17cm"
    right_margin: str = "3.17cm"

@dataclass
class Template:
    """Complete paper formatting template."""
    name: str
    description: str
    source: Optional[str] = None  # journal name or "preset"
    
    page: PageConfig = field(default_factory=PageConfig)
    
    # Heading styles by level
    heading_styles: dict = field(default_factory=dict)
    
    # Body text style
    body_style: Optional[ParagraphStyle] = None
    
    # Abstract style
    abstract_style: Optional[ParagraphStyle] = None
    
    # Citation configuration
    citation: CitationConfig = field(default_factory=lambda: CitationConfig(
        style=CitationStyle.NUMBERED,
        position=CitationPosition.IN_TEXT
    ))
    
    # Reference list configuration
    reference_list: ReferenceListConfig = field(default_factory=ReferenceListConfig)
    
    def get_heading_style(self, level: int) -> Optional[HeadingStyle]:
        """Get heading style for specific level."""
        return self.heading_styles.get(level)

# Preset templates
PRESETS = {
    "gb7714-in-text": {
        "name": "GB/T 7714 文中注",
        "description": "GB/T 7714 格式，引注以上标数字显示于文中",
        "source": "preset",
        "page": PageConfig(),
        "heading_styles": {
            1: HeadingStyle(
                font=FontStyle("黑体", "14pt"),
                align=Align.CENTER,
                numbering=NumberingType.CHINESE,
                level=1
            ),
            2: HeadingStyle(
                font=FontStyle("黑体", "12pt"),
                align=Align.LEFT,
                numbering=NumberingType.CHINESE_PAREN,
                level=2
            ),
            3: HeadingStyle(
                font=FontStyle("黑体", "12pt", bold=False),
                align=Align.LEFT,
                numbering=NumberingType.ARABIC,
                level=3
            ),
        },
        "body_style": ParagraphStyle(
            font=FontStyle("宋体", "12pt"),
            align=Align.JUSTIFY,
            line_height=1.25,
            first_line_indent="2em"
        ),
        "abstract_style": ParagraphStyle(
            font=FontStyle("楷体", "12pt"),
            align=Align.JUSTIFY,
            line_height=1.25
        ),
        "citation": CitationConfig(
            style=CitationStyle.NUMBERED,
            position=CitationPosition.IN_TEXT,
            format_string="[{number}]",
            superscript=True
        ),
        "reference_list": ReferenceListConfig(
            enabled=True,
            sort_by="appearance",
            hanging_indent="2em",
            numbering_style=CitationStyle.NUMBERED
        ),
    },
    "gb7714-footnote": {
        "name": "GB/T 7714 页下注",
        "description": "GB/T 7714 格式，引注以脚注形式显示于页面底部",
        "source": "preset",
        "citation": CitationConfig(
            style=CitationStyle.NUMBERED,
            position=CitationPosition.FOOTNOTE,
            format_string="{number}",
            superscript=True
        ),
    },
    "circled-in-text": {
        "name": "圆圈上标文中注",
        "description": "引注以圆圈数字显示于文中，常见于部分社科期刊",
        "source": "preset",
        "citation": CitationConfig(
            style=CitationStyle.CIRCLED,
            position=CitationPosition.IN_TEXT,
            format_string="{number}",
            superscript=True
        ),
    },
}
