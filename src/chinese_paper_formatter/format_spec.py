"""FormatSpec dataclasses for Chinese journal manuscript formatting."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields, is_dataclass
from typing import Any, Dict, List, Optional, Type, TypeVar


T = TypeVar("T")


def _coerce_dataclass(cls: Type[T], data: Optional[Dict[str, Any]]) -> T:
    values: Dict[str, Any] = {}
    raw = data or {}
    names = {item.name for item in fields(cls)}
    for key, value in raw.items():
        if key in names:
            values[key] = value
    return cls(**values)


def _drop_none(value: Any) -> Any:
    if is_dataclass(value):
        return _drop_none(asdict(value))
    if isinstance(value, dict):
        return {k: _drop_none(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [_drop_none(v) for v in value]
    return value


@dataclass
class FontSpec:
    """Font settings for a logical manuscript block."""

    family: str = "宋体"
    size: str = "12pt"
    latin_family: Optional[str] = None
    bold: bool = False
    italic: bool = False
    color: Optional[str] = None


@dataclass
class ParagraphSpec:
    """Paragraph style settings."""

    font: FontSpec = field(default_factory=FontSpec)
    align: str = "justify"
    line_height: float = 1.25
    first_line_indent: Optional[str] = "2em"
    left_indent: Optional[str] = None
    right_indent: Optional[str] = None
    space_before: Optional[str] = None
    space_after: Optional[str] = None
    character_spacing: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> "ParagraphSpec":
        raw = dict(data or {})
        font = _coerce_dataclass(FontSpec, raw.pop("font", None))
        item = _coerce_dataclass(cls, raw)
        item.font = font
        return item


@dataclass
class HeadingSpec(ParagraphSpec):
    """Heading style and numbering settings."""

    level: int = 1
    auto_number: bool = True
    numbering: str = "chinese"
    numbering_format: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]], level: int) -> "HeadingSpec":
        item = ParagraphSpec.from_dict(data)
        raw = dict(data or {})
        heading = cls(
            font=item.font,
            align=item.align,
            line_height=item.line_height,
            first_line_indent=item.first_line_indent,
            left_indent=item.left_indent,
            right_indent=item.right_indent,
            space_before=item.space_before,
            space_after=item.space_after,
            character_spacing=item.character_spacing,
            level=int(raw.get("level", level)),
            auto_number=bool(raw.get("auto_number", True)),
            numbering=str(raw.get("numbering", "chinese")),
            numbering_format=raw.get("numbering_format"),
        )
        return heading


@dataclass
class MetaSpec:
    name: str = "未命名模板"
    description: str = ""
    source: str = "custom"
    journal: Optional[str] = None
    version: str = "1"
    notes: Optional[str] = None


@dataclass
class PageSpec:
    paper_size: str = "A4"
    top_margin: str = "2.54cm"
    bottom_margin: str = "2.54cm"
    left_margin: str = "3.17cm"
    right_margin: str = "3.17cm"
    header: Optional[str] = None
    footer: Optional[str] = None
    page_number: Optional[Dict[str, Any]] = None
    columns: int = 1


@dataclass
class FrontMatterSpec:
    title: ParagraphSpec = field(
        default_factory=lambda: ParagraphSpec(
            font=FontSpec(family="黑体", size="16pt"),
            align="center",
            first_line_indent=None,
            line_height=1.5,
        )
    )
    authors: ParagraphSpec = field(
        default_factory=lambda: ParagraphSpec(
            font=FontSpec(family="宋体", size="12pt"),
            align="center",
            first_line_indent=None,
        )
    )
    affiliations: ParagraphSpec = field(default_factory=ParagraphSpec)
    abstract: ParagraphSpec = field(
        default_factory=lambda: ParagraphSpec(
            font=FontSpec(family="楷体", size="12pt"),
            align="justify",
            first_line_indent=None,
        )
    )
    keywords: ParagraphSpec = field(
        default_factory=lambda: ParagraphSpec(
            font=FontSpec(family="楷体", size="12pt"),
            align="justify",
            first_line_indent=None,
        )
    )

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> "FrontMatterSpec":
        raw = data or {}
        return cls(
            title=ParagraphSpec.from_dict(raw.get("title")),
            authors=ParagraphSpec.from_dict(raw.get("authors")),
            affiliations=ParagraphSpec.from_dict(raw.get("affiliations")),
            abstract=ParagraphSpec.from_dict(raw.get("abstract")),
            keywords=ParagraphSpec.from_dict(raw.get("keywords")),
        )


@dataclass
class CitationSpec:
    style: str = "numbered"
    position: str = "in-text"
    format_string: str = "[{number}]"
    superscript: bool = True


@dataclass
class ReferencesSpec:
    enabled: bool = True
    title: ParagraphSpec = field(
        default_factory=lambda: ParagraphSpec(
            font=FontSpec(family="黑体", size="12pt"),
            align="center",
            first_line_indent=None,
        )
    )
    entry: ParagraphSpec = field(
        default_factory=lambda: ParagraphSpec(
            font=FontSpec(family="宋体", size="10.5pt"),
            align="justify",
            first_line_indent="2em",
            line_height=1.15,
        )
    )
    sort_by: str = "appearance"
    hanging_indent: str = "0pt"
    numbering_style: str = "numbered"
    punctuation: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> "ReferencesSpec":
        raw = dict(data or {})
        return cls(
            enabled=bool(raw.get("enabled", True)),
            title=ParagraphSpec.from_dict(raw.get("title")),
            entry=ParagraphSpec.from_dict(raw.get("entry")),
            sort_by=str(raw.get("sort_by", "appearance")),
            hanging_indent=str(raw.get("hanging_indent", "0pt")),
            numbering_style=str(raw.get("numbering_style", "numbered")),
            punctuation=raw.get("punctuation"),
        )


@dataclass
class FiguresTablesSpec:
    figure_caption: ParagraphSpec = field(
        default_factory=lambda: ParagraphSpec(
            font=FontSpec(family="宋体", size="10.5pt"),
            align="center",
            first_line_indent=None,
        )
    )
    table_caption: ParagraphSpec = field(
        default_factory=lambda: ParagraphSpec(
            font=FontSpec(family="宋体", size="10.5pt"),
            align="center",
            first_line_indent=None,
        )
    )
    table_note: ParagraphSpec = field(
        default_factory=lambda: ParagraphSpec(
            font=FontSpec(family="宋体", size="9pt"),
            align="left",
            first_line_indent=None,
        )
    )
    three_line_table: bool = True

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> "FiguresTablesSpec":
        raw = dict(data or {})
        return cls(
            figure_caption=ParagraphSpec.from_dict(raw.get("figure_caption")),
            table_caption=ParagraphSpec.from_dict(raw.get("table_caption")),
            table_note=ParagraphSpec.from_dict(raw.get("table_note")),
            three_line_table=bool(raw.get("three_line_table", True)),
        )


@dataclass
class AdvancedWordSpec:
    east_asian_line_break: Optional[bool] = None
    latin_line_break: Optional[bool] = True
    widow_control: Optional[bool] = None
    keep_with_next: Optional[bool] = None
    use_document_grid: Optional[bool] = False
    character_spacing: Optional[str] = None
    raw_ooxml_hints: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FormatSpec:
    """Complete template model used by the skill and scripts."""

    format_spec_version: int = 1
    meta: MetaSpec = field(default_factory=MetaSpec)
    page: PageSpec = field(default_factory=PageSpec)
    paragraph: ParagraphSpec = field(default_factory=ParagraphSpec)
    headings: Dict[int, HeadingSpec] = field(default_factory=dict)
    front_matter: FrontMatterSpec = field(default_factory=FrontMatterSpec)
    citations: CitationSpec = field(default_factory=CitationSpec)
    references: ReferencesSpec = field(default_factory=ReferencesSpec)
    figures_tables: FiguresTablesSpec = field(default_factory=FiguresTablesSpec)
    advanced_word: AdvancedWordSpec = field(default_factory=AdvancedWordSpec)
    rules: List[Dict[str, Any]] = field(default_factory=list)
    unresolved_items: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> "FormatSpec":
        raw = data or {}
        headings: Dict[int, HeadingSpec] = {}
        for key, value in (raw.get("headings") or {}).items():
            level = int(key)
            headings[level] = HeadingSpec.from_dict(value, level=level)
        if not headings:
            headings = default_headings()

        return cls(
            format_spec_version=int(raw.get("format_spec_version", 1)),
            meta=_coerce_dataclass(MetaSpec, raw.get("meta")),
            page=_coerce_dataclass(PageSpec, raw.get("page")),
            paragraph=ParagraphSpec.from_dict(raw.get("paragraph")),
            headings=headings,
            front_matter=FrontMatterSpec.from_dict(raw.get("front_matter")),
            citations=_coerce_dataclass(CitationSpec, raw.get("citations")),
            references=ReferencesSpec.from_dict(raw.get("references")),
            figures_tables=FiguresTablesSpec.from_dict(raw.get("figures_tables")),
            advanced_word=_coerce_dataclass(AdvancedWordSpec, raw.get("advanced_word")),
            rules=list(raw.get("rules") or []),
            unresolved_items=list(raw.get("unresolved_items") or []),
        )

    def to_dict(self) -> Dict[str, Any]:
        data = _drop_none(self)
        headings = data.get("headings", {})
        data["headings"] = {str(key): value for key, value in headings.items()}
        return data


def default_headings() -> Dict[int, HeadingSpec]:
    return {
        1: HeadingSpec(
            level=1,
            font=FontSpec(family="黑体", size="14pt"),
            align="center",
            first_line_indent=None,
            numbering="chinese",
        ),
        2: HeadingSpec(
            level=2,
            font=FontSpec(family="黑体", size="12pt"),
            align="left",
            first_line_indent=None,
            numbering="chinese_paren",
        ),
        3: HeadingSpec(
            level=3,
            font=FontSpec(family="黑体", size="12pt"),
            align="left",
            first_line_indent=None,
            numbering="arabic",
        ),
    }
